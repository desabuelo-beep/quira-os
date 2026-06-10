# -*- coding: utf-8 -*-
"""
pdot_extractor.py — Operación Minera del PDOT · Sprint B.2 · QUIRA OS
=====================================================================
Aprobado por mesa (Javo + Colega + Director) 2026-06-10.

Arquitectura (idéntica hoy y a escala nacional — ADR-024):
    normativa_corpus (chunks PDOT) → Haiku → pdot_indicadores

Es el PROTOTIPO del módulo de ingesta industrializada de Sprint C:
si funciona para Montecristi, funciona para cualquier PDOT cantonal.

Reglas duras del extractor:
    - Extrae SOLO indicadores con valor presente en el texto. No interpreta.
    - No inventa años, fuentes ni territorios — null antes que adivinar.
    - Tabla partida por chunking → confianza 'baja'.
    - Trazabilidad total: chunk_id + sha256 (Regla de Oro 3).
    - Reanudable: chunks ya procesados (pdot_extract_log) se saltan.

Uso:
    python scripts/sprint_b/pdot_extractor.py --sample 20         # calibración
    python scripts/sprint_b/pdot_extractor.py --limit 200         # por lotes
    python scripts/sprint_b/pdot_extractor.py                     # corrida total
    python scripts/sprint_b/pdot_extractor.py --dry-run --sample 5
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
import tomllib
from pathlib import Path

import psycopg2
import psycopg2.extras

sys.stdout.reconfigure(encoding="utf-8")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("pdot_extractor")

ROOT = Path(__file__).resolve().parents[2]

HAIKU_MODEL = "claude-haiku-4-5"
EXTRACTOR_VER = "v1"
SIGLAS_PDOT = ("PDOT-MONTECRISTI", "PLAN-BICENTENARIO-MCR", "PAI-PLURIANUAL-GAD")
VENTANA_CHARS = 500          # cola del chunk previo + cabeza del siguiente
MAX_RETRIES = 3

SISTEMAS_VALIDOS = {
    "BIOFISICO", "SOCIOCULTURAL", "ECONOMICO_PRODUCTIVO",
    "ASENTAMIENTOS_HUMANOS", "MOVILIDAD_ENERGIA_CONECTIVIDAD",
    "POLITICO_INSTITUCIONAL", "PUGS", "OTRO",
}
CONFIANZAS = {"alta", "media", "baja"}

_SYSTEM_PROMPT = """Eres un extractor de indicadores territoriales de planes de \
desarrollo municipal ecuatorianos (PDOT). Recibes un fragmento del diagnóstico y \
devuelves SOLO un array JSON de indicadores con valor explícito en el texto.

SCHEMA por indicador:
{
  "sistema": "BIOFISICO|SOCIOCULTURAL|ECONOMICO_PRODUCTIVO|ASENTAMIENTOS_HUMANOS|MOVILIDAD_ENERGIA_CONECTIVIDAD|POLITICO_INSTITUCIONAL|PUGS|OTRO",
  "indicador": "nombre descriptivo corto del indicador (string, requerido)",
  "unidad": "%|casos|km|Tn|USD|habitantes|tasa/100k|ordenanzas|... o null",
  "valor_texto": "valor tal como aparece, series incluidas, ej: '34.9' o '120 (2022) -> 198 (2023)' (requerido)",
  "valor_num": número escalar si aplica, si es serie o rango usar null,
  "anio": "año o rango, ej: '2022' o '2014-2023', o null si no consta",
  "territorio": "cantonal|provincial|nombre de parroquia/recinto si está explícito",
  "fuente_original": "INEC|MSP|ANT|GADM|PDOT|... como conste en el texto, o null",
  "pagina_pdot": "número de página si aparece en el texto, o null",
  "confianza": "alta|media|baja"
}

REGLAS DURAS:
1. Extrae SOLO lo que tiene valor numérico o categórico EXPLÍCITO en el texto.
2. NUNCA inventes años, fuentes, territorios ni páginas — usa null.
3. NO extraigas opiniones, interpretaciones ni texto del consultor sin dato.
4. Si una tabla aparece cortada o con números sueltos sin encabezado claro → confianza "baja".
5. Si el dato es claramente de OTRO cantón o solo provincial, territorio="provincial" o nómbralo.
6. Texto sin ningún indicador → devuelve [].
7. Responde SOLO el array JSON. Sin markdown, sin explicación."""


# ── Infraestructura ───────────────────────────────────────────────────────────

def _secrets() -> dict:
    with open(ROOT / ".streamlit" / "secrets.toml", "rb") as f:
        return tomllib.load(f)


def _conn(secrets: dict):
    return psycopg2.connect(secrets["database"]["supabase_uri"])


def _client(secrets: dict):
    import anthropic
    key = secrets.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY no encontrada en secrets.toml")
    return anthropic.Anthropic(api_key=key)


# ── Carga de chunks con ventana ───────────────────────────────────────────────

def cargar_chunks(cur, limit: int | None, sample: int | None) -> list[dict]:
    """Chunks PDOT no procesados, con vecinos para ventana de contexto."""
    siglas = "', '".join(SIGLAS_PDOT)
    q = f"""
        SELECT nc.id, nc.norma_sigla, nc.chunk_seq, nc.contenido, nc.sha256
        FROM normativa_corpus nc
        LEFT JOIN pdot_extract_log lg ON lg.chunk_id = nc.id
        WHERE nc.norma_sigla IN ('{siglas}') AND lg.chunk_id IS NULL
        ORDER BY nc.norma_sigla, nc.chunk_seq
    """
    if sample:
        q += f" LIMIT {sample}"
    elif limit:
        q += f" LIMIT {limit}"
    cur.execute(q)
    rows = [
        {"id": r[0], "sigla": r[1], "seq": r[2], "contenido": r[3], "sha256": r[4]}
        for r in cur.fetchall()
    ]
    # vecinos para ventana (cola previa + cabeza siguiente)
    if rows:
        ids_seq = {(r["sigla"], r["seq"]): i for i, r in enumerate(rows)}
        seqs_necesarios = set()
        for r in rows:
            seqs_necesarios.add((r["sigla"], r["seq"] - 1))
            seqs_necesarios.add((r["sigla"], r["seq"] + 1))
        seqs_necesarios -= set(ids_seq.keys())
        if seqs_necesarios:
            conds = " OR ".join(
                f"(norma_sigla='{s}' AND chunk_seq={q_})" for s, q_ in seqs_necesarios
            )
            cur.execute(
                f"SELECT norma_sigla, chunk_seq, contenido FROM normativa_corpus WHERE {conds}"
            )
            vecinos = {(r[0], r[1]): r[2] for r in cur.fetchall()}
        else:
            vecinos = {}
        for r in rows:
            prev = vecinos.get((r["sigla"], r["seq"] - 1), "")
            nxt = vecinos.get((r["sigla"], r["seq"] + 1), "")
            # también puede ser vecino dentro del mismo lote
            i = ids_seq.get((r["sigla"], r["seq"] - 1))
            if i is not None:
                prev = rows[i]["contenido"]
            i = ids_seq.get((r["sigla"], r["seq"] + 1))
            if i is not None:
                nxt = rows[i]["contenido"]
            r["ventana"] = (
                (("..." + prev[-VENTANA_CHARS:]) if prev else "")
                + "\n<<FRAGMENTO PRINCIPAL>>\n" + r["contenido"]
                + "\n<<FIN FRAGMENTO>>\n"
                + ((nxt[:VENTANA_CHARS] + "...") if nxt else "")
            )
    return rows


# ── Extracción Haiku ──────────────────────────────────────────────────────────

def extraer_chunk(client, chunk: dict) -> list[dict]:
    """Un chunk (con ventana) → lista de indicadores via Haiku."""
    user_msg = (
        f"Documento: {chunk['sigla']} · fragmento #{chunk['seq']}\n\n{chunk['ventana']}"
    )
    for intento in range(1, MAX_RETRIES + 1):
        try:
            resp = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=2048,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            )
            texto = resp.content[0].text.strip()
            # tolerar fences de markdown
            texto = re.sub(r"^```(json)?|```$", "", texto, flags=re.M).strip()
            data = json.loads(texto)
            if not isinstance(data, list):
                return []
            return [d for d in data if _valido(d)]
        except json.JSONDecodeError:
            logger.warning("JSON inválido chunk %s (intento %d)", chunk["id"], intento)
        except Exception as e:  # rate limit / red — backoff
            logger.warning("API error chunk %s: %s (intento %d)", chunk["id"], e, intento)
            time.sleep(2 * intento)
    return []


def _valido(d: dict) -> bool:
    if not isinstance(d, dict):
        return False
    if not d.get("indicador") or not d.get("valor_texto"):
        return False
    if d.get("sistema") not in SISTEMAS_VALIDOS:
        d["sistema"] = "OTRO"
    if d.get("confianza") not in CONFIANZAS:
        d["confianza"] = "baja"
    if not d.get("territorio"):
        d["territorio"] = "cantonal"
    return True


# ── Persistencia ──────────────────────────────────────────────────────────────

def guardar(cur, chunk: dict, indicadores: list[dict]) -> int:
    n = 0
    for d in indicadores:
        try:
            valor_num = d.get("valor_num")
            if isinstance(valor_num, str):
                valor_num = float(valor_num.replace(",", ".")) if re.match(
                    r"^-?\d+[.,]?\d*$", valor_num.strip()) else None
            cur.execute(
                """
                INSERT INTO pdot_indicadores
                    (canton_id, norma_sigla, chunk_id, chunk_sha256, sistema,
                     indicador, unidad, valor_texto, valor_num, anio, territorio,
                     fuente_original, pagina_pdot, confianza, extractor_ver)
                VALUES ('MCR-001', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (canton_id, indicador, territorio, anio, valor_texto)
                DO NOTHING
                """,
                (
                    chunk["sigla"], chunk["id"], chunk["sha256"], d["sistema"],
                    str(d["indicador"])[:300], d.get("unidad"),
                    str(d["valor_texto"])[:500], valor_num,
                    str(d["anio"])[:40] if d.get("anio") else None,
                    str(d["territorio"])[:120],
                    str(d["fuente_original"])[:200] if d.get("fuente_original") else None,
                    str(d["pagina_pdot"])[:40] if d.get("pagina_pdot") else None,
                    d["confianza"], EXTRACTOR_VER,
                ),
            )
            n += cur.rowcount
        except Exception as e:
            logger.warning("insert falló (%s): %s", d.get("indicador"), e)
    return n


def log_chunk(cur, chunk: dict, n_ind: int, status: str, err: str | None = None):
    cur.execute(
        """
        INSERT INTO pdot_extract_log
            (chunk_id, norma_sigla, chunk_seq, n_indicadores, status, error_msg, extractor_ver)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (chunk_id) DO UPDATE
            SET n_indicadores = EXCLUDED.n_indicadores,
                status = EXCLUDED.status,
                processed_at = now()
        """,
        (chunk["id"], chunk["sigla"], chunk["seq"], n_ind, status,
         (err or "")[:500] or None, EXTRACTOR_VER),
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Extractor PDOT → pdot_indicadores")
    ap.add_argument("--sample", type=int, help="solo N chunks (calibración)")
    ap.add_argument("--limit", type=int, help="máximo de chunks esta corrida")
    ap.add_argument("--dry-run", action="store_true", help="no escribe en DB")
    args = ap.parse_args()

    secrets = _secrets()
    conn = _conn(secrets)
    conn.autocommit = False
    cur = conn.cursor()
    client = _client(secrets)

    chunks = cargar_chunks(cur, args.limit, args.sample)
    logger.info("chunks a procesar: %d", len(chunks))
    if not chunks:
        print("Nada pendiente — corrida completa o ya procesado.")
        return

    total_ind = 0
    t0 = time.time()
    for i, ch in enumerate(chunks, 1):
        try:
            inds = extraer_chunk(client, ch)
            if args.dry_run:
                print(f"[{ch['sigla']} #{ch['seq']}] -> {len(inds)} indicadores")
                for d in inds[:4]:
                    print("   ", d.get("sistema"), "|", d.get("indicador"),
                          "=", d.get("valor_texto"), f"({d.get('territorio')})")
                continue
            n = guardar(cur, ch, inds)
            log_chunk(cur, ch, n, "ok" if inds else "vacio")
            conn.commit()
            total_ind += n
            if i % 25 == 0:
                rate = i / (time.time() - t0) * 60
                logger.info("progreso %d/%d · %d indicadores · %.0f chunks/min",
                            i, len(chunks), total_ind, rate)
        except KeyboardInterrupt:
            conn.commit()
            print(f"\nInterrumpido — {i-1} chunks procesados (reanudable).")
            return
        except Exception as e:
            logger.error("chunk %s fatal: %s", ch["id"], e)
            if not args.dry_run:
                log_chunk(cur, ch, 0, "error", str(e))
                conn.commit()

    dt = time.time() - t0
    print(f"\n{'='*60}")
    print(f"CORRIDA COMPLETA: {len(chunks)} chunks · {total_ind} indicadores nuevos · {dt/60:.1f} min")
    if not args.dry_run:
        cur.execute("SELECT sistema, COUNT(*) FROM pdot_indicadores GROUP BY sistema ORDER BY 2 DESC")
        for s, n in cur.fetchall():
            print(f"  {s}: {n}")
    conn.close()


if __name__ == "__main__":
    main()
