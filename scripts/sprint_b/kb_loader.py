# -*- coding: utf-8 -*-
"""
kb_loader.py — Carga determinística del KB PDOT a pdot_indicadores · Sprint B.2
===============================================================================
Vía SIN API (costo $0): el KB estructurado (producto de la ingesta /graphify
del Excel KB del PDOT) ya ES extracción verificada. Este loader la parsea
determinísticamente y la carga con confianza ALTA.

Complementa al extractor Haiku (pdot_extractor.py):
    KB estructurado  → kb_loader (determinístico, $0)   → confianza alta
    Corpus narrativo → pdot_extractor (Haiku, reanudable) → confianza media

Formatos parseados:
    F1: | GAD-MNT-180650 | SISTEMA | Indicador | unidad | valor | año | fuente | territorio | pág |
    F2: tabla servicios p.115: | GAD | Parroquia | Agua_% | Saneamiento_% | Pluvial_% | Elec_% | Equip | año | fuente | pág |
    F3: KB_NBI: | GAD | Geo_ID | Territorio | Año | NBI_Total_% | ... | Sistema | Pagina |

Uso:
    python scripts/sprint_b/kb_loader.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

import psycopg2

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
KB_FILE = ROOT / "graphify-out" / "converted" / "PDOT_MONTECRISTI_KB_a59cd286.md"
KB_SHA = "KB:a59cd286"
SIGLA = "PDOT-KB-EXCEL"
VER = "v1-kb-parser"

SISTEMA_MAP = {
    "FÍSICO AMBIENTAL": "BIOFISICO",
    "FISICO AMBIENTAL": "BIOFISICO",
    "BIOFÍSICO": "BIOFISICO",
    "BIOFISICO": "BIOFISICO",
    "SOCIOCULTURAL": "SOCIOCULTURAL",
    "SOCIO CULTURAL": "SOCIOCULTURAL",
    "ECONÓMICO PRODUCTIVO": "ECONOMICO_PRODUCTIVO",
    "ECONOMICO PRODUCTIVO": "ECONOMICO_PRODUCTIVO",
    "ASENTAMIENTOS HUMANOS": "ASENTAMIENTOS_HUMANOS",
    "POLÍTICO INSTITUCIONAL": "POLITICO_INSTITUCIONAL",
    "POLITICO INSTITUCIONAL": "POLITICO_INSTITUCIONAL",
    "MOVILIDAD ENERGÍA Y CONECTIVIDAD": "MOVILIDAD_ENERGIA_CONECTIVIDAD",
    "MOVILIDAD, ENERGÍA Y CONECTIVIDAD": "MOVILIDAD_ENERGIA_CONECTIVIDAD",
}


def _num(s: str):
    s = (s or "").strip().replace(",", ".")
    if re.fullmatch(r"-?\d+(\.\d+)?", s):
        return float(s)
    return None


def _celdas(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_kb(path: Path) -> list[dict]:
    rows: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.lstrip().startswith("|") or "---" in line:
                continue
            c = _celdas(line)
            if not c or c[0] != "GAD-MNT-180650":
                continue

            # F1 — indicador genérico (9 celdas): gad|SISTEMA|indicador|unidad|valor|año|fuente|territorio|pág
            if len(c) == 9 and c[1].upper() in SISTEMA_MAP:
                valor = c[4]
                if not valor:
                    continue
                rows.append({
                    "sistema": SISTEMA_MAP[c[1].upper()],
                    "indicador": c[2][:300],
                    "unidad": c[3] or None,
                    "valor_texto": valor[:500],
                    "valor_num": _num(valor),
                    "anio": c[5] or None,
                    "territorio": c[7] or "cantonal",
                    "fuente": c[6] or None,
                    "pagina": c[8] or None,
                    "confianza": "alta",
                })
                continue

            # F2 — servicios por parroquia p.115 (10 celdas):
            # gad|Parroquia|Agua_%|Saneamiento_%|Pluvial_%|Electricidad_%|Equip_m2hab|año|fuente|pág
            if len(c) == 10 and _num(c[2]) is not None and _num(c[3]) is not None \
                    and not c[1].upper() in SISTEMA_MAP and c[1] and not c[1].isdigit():
                parroquia = c[1]
                anio = c[7] if re.fullmatch(r"\d{4}", c[7] or "") else "2023"
                flag_est = "" if re.fullmatch(r"\d{4}", c[7] or "") else " [EST]"
                servicios = [
                    ("Cobertura de agua por red (parroquial)" + flag_est, "%", c[2]),
                    ("Cobertura de saneamiento (parroquial)" + flag_est, "%", c[3]),
                    ("Cobertura de drenaje pluvial (parroquial)", "%", c[4]),
                    ("Cobertura eléctrica (parroquial)", "%", c[5]),
                    ("Equipamiento por habitante (parroquial)", "m2/hab", c[6]),
                ]
                for nombre, unidad, val in servicios:
                    if val == "":
                        continue
                    rows.append({
                        "sistema": "ASENTAMIENTOS_HUMANOS",
                        "indicador": nombre,
                        "unidad": unidad,
                        "valor_texto": val[:500],
                        "valor_num": _num(val),
                        "anio": anio,
                        "territorio": parroquia[:120],
                        "fuente": (c[8] or "PDOT 2023-2027 Cap. Diagnóstico")[:200],
                        "pagina": c[9] or "115",
                        "confianza": "alta",
                    })
                continue

            # F4 — POLÍGONOS CUP (10 celdas): gad|Parroquia_Poligono|Area_ha|Barrios|Tipo|Zona|Año|Fuente|Pág|Notas
            # GeoTwin v1: geometría administrativa-urbana (nombres + ha + barrios)
            if len(c) == 10 and _num(c[2]) is not None and _num(c[3]) is None \
                    and c[4] in ("parroquia", "poligono_crecimiento"):
                poligono = c[1]
                anio = c[6] if re.fullmatch(r"\d{4}", c[6] or "") else "2023"
                rows.append({
                    "sistema": "PUGS",
                    "indicador": f"Área del polígono urbano CUP ({c[4]})",
                    "unidad": "ha",
                    "valor_texto": c[2][:500],
                    "valor_num": _num(c[2]),
                    "anio": anio,
                    "territorio": poligono[:120],
                    "fuente": (c[7] or "PDOT Cap. Asentamientos Humanos")[:200],
                    "pagina": c[8] or "115",
                    "confianza": "alta",
                })
                if c[3]:
                    rows.append({
                        "sistema": "PUGS",
                        "indicador": "Barrios y sectores del polígono CUP",
                        "unidad": None,
                        "valor_texto": c[3][:500],
                        "valor_num": None,
                        "anio": anio,
                        "territorio": poligono[:120],
                        "fuente": (c[7] or "PDOT Cap. Asentamientos Humanos")[:200],
                        "pagina": c[8] or "115",
                        "confianza": "alta",
                    })
                continue

            # F5 — KB_RIESGOS (9 celdas): gad|Riesgo_ID|Tipo_Amenaza|Nivel|Territorio|Pobl_Expuesta|Area_ha|Medida|Pág
            # GeoTwin v1: capa de riesgo con nombre de lugar
            if len(c) >= 9 and (c[1] or "").startswith("RISK-"):
                territorio_r = c[4] or "cantonal"
                rows.append({
                    "sistema": "BIOFISICO",
                    "indicador": f"Riesgo territorial: {c[2][:220]}",
                    "unidad": "nivel",
                    "valor_texto": (c[3] or "registrado")[:500],
                    "valor_num": None,
                    "anio": "s/f",   # evita NULL en clave de dedup (re-corridas)
                    "territorio": territorio_r[:120],
                    "fuente": "PDOT — matriz de riesgos (KB_RIESGOS)",
                    "pagina": c[8] if len(c) > 8 else None,
                    "confianza": "alta",
                })
                if _num(c[6]) is not None:
                    rows.append({
                        "sistema": "BIOFISICO",
                        "indicador": f"Área afectada — {c[2][:200]}",
                        "unidad": "ha",
                        "valor_texto": c[6][:500],
                        "valor_num": _num(c[6]),
                        "anio": "s/f",
                        "territorio": territorio_r[:120],
                        "fuente": "PDOT — matriz de riesgos (KB_RIESGOS)",
                        "pagina": c[8] if len(c) > 8 else None,
                        "confianza": "alta",
                    })
                continue

            # F3 — KB_NBI (11-12 celdas): gad|Geo_ID|Territorio|Año|NBI_Total|NBI_Agua|NBI_Alc|NBI_Viv|NBI_Edu|NBI_Salud|Sistema|Pág
            if len(c) >= 11 and c[1].startswith("GEO_") and re.fullmatch(r"\d{4}", c[3] or ""):
                territorio, anio = c[2], c[3]
                nbi_campos = [
                    ("NBI total", c[4]), ("NBI agua", c[5]), ("NBI alcantarillado", c[6]),
                    ("NBI vivienda", c[7]), ("NBI educación", c[8]), ("NBI salud", c[9]),
                ]
                for nombre, val in nbi_campos:
                    if not val:
                        continue
                    rows.append({
                        "sistema": "SOCIOCULTURAL",
                        "indicador": f"{nombre} (territorial)",
                        "unidad": "%",
                        "valor_texto": val[:500],
                        "valor_num": _num(val),
                        "anio": anio,
                        "territorio": territorio[:120],
                        "fuente": "INEC vía PDOT (KB_NBI)",
                        "pagina": c[-1] or None,
                        "confianza": "alta",
                    })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = parse_kb(KB_FILE)
    print(f"KB parseado: {len(rows)} indicadores candidatos")

    por_sistema: dict[str, int] = {}
    for r in rows:
        por_sistema[r["sistema"]] = por_sistema.get(r["sistema"], 0) + 1
    for s_, n in sorted(por_sistema.items(), key=lambda x: -x[1]):
        print(f"  {s_}: {n}")

    if args.dry_run:
        print("\n-- DRY RUN: muestra --")
        for r in rows[:8]:
            print(f"  {r['sistema']} | {r['indicador']} = {r['valor_texto']} "
                  f"({r['territorio']}, {r['anio']}) p.{r['pagina']}")
        return

    with open(ROOT / ".streamlit" / "secrets.toml", "rb") as f:
        s = tomllib.load(f)
    conn = psycopg2.connect(s["database"]["supabase_uri"])
    cur = conn.cursor()
    nuevos = 0
    for r in rows:
        cur.execute(
            """
            INSERT INTO pdot_indicadores
                (canton_id, norma_sigla, chunk_id, chunk_sha256, sistema, indicador,
                 unidad, valor_texto, valor_num, anio, territorio, fuente_original,
                 pagina_pdot, confianza, validado, extractor_ver)
            VALUES ('MCR-001', %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, %s)
            ON CONFLICT (canton_id, indicador, territorio, anio, valor_texto) DO NOTHING
            """,
            (SIGLA, KB_SHA, r["sistema"], r["indicador"], r["unidad"],
             # anio nunca NULL: NULL rompe el dedup de la UNIQUE (lección
             # corrida 2: 443 duplicados por claves con NULL)
             r["valor_texto"], r["valor_num"], r["anio"] or "s/f", r["territorio"],
             r["fuente"], r["pagina"], r["confianza"], VER),
        )
        nuevos += cur.rowcount
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM pdot_indicadores")
    total = cur.fetchone()[0]
    print(f"\nINSERTADOS: {nuevos} nuevos · total en tabla: {total}")
    conn.close()


if __name__ == "__main__":
    main()
