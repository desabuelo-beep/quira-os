# -*- coding: utf-8 -*-
"""
vault_fondos_loader.py — Carga VALIDADA del módulo 06 del vault · Sprint B.2
============================================================================
Los 18 fondos del vault Obsidian (06_Fuentes_Financiamiento) son la revisión
HUMANA de Javo (mayo 2026): fuente identificada + criterio experto = VALIDADA
(taxonomía mesa 2026-06-10). Primera capa REAL del radar D02 — sin API, $0.

Mapeo:
    nota .md (frontmatter YAML) → fondos_emisores (upsert) +
                                  fondos_convocatorias origen=VALIDADA
    metadata_json conserva: estado_gestion · sector_pdot · score_quira ·
    contraparte · condiciones · archivo fuente (trazabilidad).

Regla de honestidad: montos ambiguos NO se interpretan — van a metadata
con flag montos_revisar. VALIDADA ≠ VIGENTE: la promoción a VIGENTE exige
verificar vigencia contra el sitio oficial (ciclo semanal del radar).

Uso:  python scripts/sprint_b/vault_fondos_loader.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path

import psycopg2
import yaml

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
VAULT = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi\06_Fuentes_Financiamiento")

# archivo → (emisor_codigo, emisor_nombre, es_nuevo_probable)
NOTAS: dict[str, tuple[str, str]] = {
    "AECID-Cooperacion-Espanola.md":   ("AECID", "Agencia Española de Cooperación Internacional para el Desarrollo"),
    "BDE-Credito-Directo.md":          ("BDE", "Banco de Desarrollo del Ecuador"),
    "BDE-PremioVerde-Manglar.md":      ("BDE", "Banco de Desarrollo del Ecuador"),
    "BEI-PROGAPSA-Alcantarillado.md":  ("BEI", "Banco Europeo de Inversiones"),
    "BID-Infraestructura-Clima.md":    ("BID", "Banco Interamericano de Desarrollo"),
    "CAF-Credito-Desarrollo.md":       ("CAF", "CAF — Banco de Desarrollo de América Latina"),
    "CELEC-Compensacion-Estudios.md":  ("CELEC", "Corporación Eléctrica del Ecuador"),
    "COSUDE-Cooperacion-Suiza.md":     ("COSUDE", "Agencia Suiza para el Desarrollo y la Cooperación"),
    "Embajada-Canada-CFLI.md":         ("EMBASSY_CANADA", "Embajada de Canadá — Canada Fund for Local Initiatives"),
    "Embajada-Japon-GGP.md":           ("EMBASSY_JAPON", "Embajada del Japón — Programa GGP"),
    "Ford-Foundation.md":              ("FORD", "Ford Foundation"),
    "GCF-Fondo-Verde-Clima.md":        ("GCF", "Green Climate Fund — Fondo Verde para el Clima"),
    "GEF-SGP-Pequenas-Donaciones.md":  ("GEF", "Global Environment Facility"),
    "GIZ-Cooperacion-Alemana.md":      ("GIZ", "Deutsche Gesellschaft für Internationale Zusammenarbeit"),
    "NED-Democracia-Sociedad-Civil.md": ("NED", "National Endowment for Democracy"),
    "Open-Society-Foundations.md":     ("OSF", "Open Society Foundations"),
    "PNUD-Desarrollo-Local.md":        ("PNUD", "Programa de las Naciones Unidas para el Desarrollo"),
    "USAID-Gobernanza-Inclusion.md":   ("USAID", "Agencia de los Estados Unidos para el Desarrollo Internacional"),
}


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    return yaml.safe_load(text[3:end]) or {}


def _monto(v):
    """Solo acepta montos inequívocos (>= 1000 USD). Lo ambiguo → metadata."""
    if isinstance(v, (int, float)) and v >= 1000:
        return v
    return None


def _estado_conv(fm: dict) -> str:
    ventana = str(fm.get("ventana_convocatoria", "")).lower()
    if "permanente" in ventana or "recurrente" in ventana:
        return "recurrente"
    if fm.get("fecha_cierre_proxima"):
        return "abierta"
    return "recurrente"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(ROOT / ".streamlit" / "secrets.toml", "rb") as f:
        s = tomllib.load(f)
    conn = psycopg2.connect(s["database"]["supabase_uri"])
    cur = conn.cursor()

    cur.execute("SELECT codigo, id FROM fondos_emisores")
    emisores_db = dict(cur.fetchall())

    nuevos_emisores, nuevas_conv, errores = 0, 0, 0
    for archivo, (cod_emisor, nombre_emisor) in NOTAS.items():
        path = VAULT / archivo
        if not path.exists():
            print(f"  ⚠️ no encontrado: {archivo}")
            errores += 1
            continue
        fm = _frontmatter(path)
        if not fm:
            print(f"  ⚠️ sin frontmatter: {archivo}")
            errores += 1
            continue

        temas = [str(t)[:40].lower().replace(" ", "_") for t in (fm.get("temas") or [])][:8]
        m_min, m_max = _monto(fm.get("monto_min_usd")), _monto(fm.get("monto_max_usd"))
        meta = {
            "fuente": "vault_obsidian_06",
            "archivo": archivo,
            "estado_gestion": fm.get("estado_gestion"),
            "sector_pdot": fm.get("sector_pdot"),
            "score_quira": fm.get("score_quira"),
            "score_version": fm.get("score_version"),
            "contraparte_pct": fm.get("contraparte_pct"),
            "eligibilidad_montecristi": fm.get("eligibilidad_montecristi"),
            "riesgo_elegibilidad": fm.get("riesgo_elegibilidad"),
            "condiciones_elegibilidad": fm.get("condiciones_elegibilidad"),
            "ods": fm.get("ods_vinculados"),
            "categoria": fm.get("categoria"),
            "montos_revisar": (fm.get("monto_min_usd"), fm.get("monto_max_usd"))
                              if (m_min is None and m_max is None) else None,
            "revision_humana": "Javo · vault 2026-05",
        }
        nombre_conv = fm.get("name") or fm.get("nombre") or archivo.replace(".md", "")
        estado = _estado_conv(fm)

        if args.dry_run:
            print(f"  [{cod_emisor}] {nombre_conv} · estado={estado} · "
                  f"gestion={fm.get('estado_gestion')} · max={m_max}")
            continue

        # 1. emisor (insertar si no existe)
        if cod_emisor not in emisores_db:
            tipo_apoyo = str(fm.get("tipo_apoyo") or "").lower()
            naturaleza = {"mixto": "ambas", "crédito": "reembolsable",
                          "credito": "reembolsable"}.get(tipo_apoyo, "no_reembolsable")
            cur.execute(
                """INSERT INTO fondos_emisores
                       (codigo, nombre, tipo_emisor, naturaleza, pais_origen,
                        region, temas, elegibles, frecuencia, web, activo, notas)
                   VALUES (%s, %s, %s, %s, %s, 'AL', %s, ARRAY['GAD'],
                           'continua', %s, TRUE, %s)
                   RETURNING id""",
                (cod_emisor, nombre_emisor,
                 "bilateral" if "EMBASSY" in cod_emisor or cod_emisor in
                     ("GIZ", "COSUDE", "AECID", "USAID") else "multilateral",
                 naturaleza,
                 str(fm.get("pais_origen") or "")[:60],
                 temas or ["otros"],
                 str(fm.get("contacto_organismo") or "")[:200],
                 f"Cargado desde vault Obsidian módulo 06 · {archivo}"),
            )
            emisores_db[cod_emisor] = cur.fetchone()[0]
            nuevos_emisores += 1

        # 2. convocatoria/línea VALIDADA (dedup semántico vía constraint codigo)
        codigo_conv = f"{cod_emisor}-VAULT-{archivo.replace('.md','')[:24].upper()}"
        cur.execute("SELECT 1 FROM fondos_convocatorias WHERE codigo=%s", (codigo_conv,))
        if cur.fetchone():
            continue
        cur.execute(
            """INSERT INTO fondos_convocatorias
                   (codigo, emisor_id, nombre, estado, monto_min_usd, monto_max_usd,
                    moneda, elegibles, temas, url, descripcion, origen_oportunidad,
                    snapshot_date, proxima_revision, metadata_json, notas)
               VALUES (%s, %s, %s, %s, %s, %s, 'USD', ARRAY['GAD'], %s, %s, %s,
                       'VALIDADA', CURRENT_DATE, CURRENT_DATE + 7, %s, %s)""",
            (codigo_conv, emisores_db[cod_emisor], str(nombre_conv)[:200], estado,
             m_min, m_max, temas or ["otros"],
             str(fm.get("url_convocatoria") or fm.get("contacto_organismo") or "")[:300],
             str(fm.get("description") or "")[:400],
             json.dumps(meta, ensure_ascii=False, default=str),
             "Revisión humana vault 06 — VALIDADA pendiente verificación de vigencia"),
        )
        nuevas_conv += 1

    if not args.dry_run:
        conn.commit()
        cur.execute("SELECT origen_oportunidad, COUNT(*) FROM fondos_convocatorias GROUP BY 1")
        dist = cur.fetchall()
        print(f"\nEMISORES nuevos: {nuevos_emisores} · CONVOCATORIAS VALIDADA nuevas: {nuevas_conv} · errores: {errores}")
        print(f"distribución origen: {dist}")
    conn.close()


if __name__ == "__main__":
    main()
