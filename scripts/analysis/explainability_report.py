# -*- coding: utf-8 -*-
"""
explainability_report.py — Gate 6.6C: Auditoría Explicable del Motor ICPI
QUIRA Gov · Dylus Lab © 2026

Responde la pregunta central de ADR-023:
  "¿Por qué este indicador del Gold Master tiene este valor?"

Ejemplo:
  ¿Por qué D4 (Equidad) = 44.79%?
  ¿Por qué ICPI 2025 = 69.93%?
  ¿Qué evidencia respalda el score de la meta AH-I-N-01?

Flujo:
  Indicador Gold Master
      ↓
  Metas PDOT relacionadas (SIGLA_MAP)
      ↓
  Documentos con MNT_UUID (corpus_mnt_mapping)
      ↓
  Chunks de evidencia (normativa_corpus)
      ↓
  Reporte explicable

Uso:
  python -X utf8 scripts/analysis/explainability_report.py --meta AH-I-N-01
  python -X utf8 scripts/analysis/explainability_report.py --silo S8
  python -X utf8 scripts/analysis/explainability_report.py --icpi
  python -X utf8 scripts/analysis/explainability_report.py --d4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

import toml, streamlit as st
_raw = toml.load(str(ROOT / ".streamlit" / "secrets.toml"))
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k): return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection
from app.connectors.gold_master import fetch_gold_master_data


# ── MAPEO TGI D1-D5 → Metas/Silos relacionados ───────────────────────────────

TGI_DIMENSION_MAP = {
    "D1": {
        "nombre": "Legalidad y Coherencia",
        "descripcion": "Trust_Score_Metodologico — calidad metodologica del modelo",
        "silos": ["S1", "S3"],
        "metas": [],
        "nota": "D1 mide coherencia legal del acto de gobierno (Trust Score)"
    },
    "D2": {
        "nombre": "Fidelidad de Planificacion",
        "descripcion": "ICPI_Real_2025 — ejecucion ponderada metas PDOT",
        "silos": ["S3", "S3b", "S4", "S6"],
        "metas": ["todos"],
        "nota": "D2 = ICPI 2025 = 69.93%. Mide si lo que se hizo estaba en el PDOT."
    },
    "D3": {
        "nombre": "Ejecucion Presupuestaria",
        "descripcion": "Ti_Inversion_2025 — devengado/codificado entidades",
        "silos": ["S5"],
        "metas": ["SC-I-N-01", "AH-I-X-02", "AH-I-N-01"],
        "nota": "D3 = 59.85%. Mide si lo planificado se ejecuto en tiempo y forma."
    },
    "D4": {
        "nombre": "Equidad Territorial",
        "descripcion": "IET_Rural_Avg — distribucion inversion en territorio",
        "silos": ["S5", "S3"],
        "metas": ["AH-I-X-02", "SC-I-N-01", "SC-L-G-01", "AH-C-X-01"],
        "nota": "D4 = 44.79% (gap critico). IRS = 79.7 (Muy Regresivo). Inversion no llego a parroquias rurales."
    },
    "D5": {
        "nombre": "Capacidad Institucional",
        "descripcion": "ICM_SNP_SIGAD — cumplimiento reporte al SNP",
        "silos": ["S6"],
        "metas": ["todos"],
        "nota": "D5 = 100% (SIGAD ICM=1.0). Las 11 direcciones evaluadas."
    },
}


# ── QUERIES ───────────────────────────────────────────────────────────────────

def get_docs_for_meta(conn, meta_pdot: str) -> list[dict]:
    """Retorna documentos mapeados a una meta PDOT."""
    c = conn.cursor()
    c.execute("""
        SELECT m.document_sigla, m.mnt_uuid, m.actividad_id,
               m.silo, m.variable_icpi, m.confidence, m.source_entity,
               COUNT(n.id) AS chunks
        FROM corpus_mnt_mapping m
        LEFT JOIN normativa_corpus n ON n.norma_sigla = m.document_sigla
        WHERE m.meta_pdot = %s OR m.meta_pdot IS NULL
        GROUP BY m.document_sigla, m.mnt_uuid, m.actividad_id,
                 m.silo, m.variable_icpi, m.confidence, m.source_entity
        ORDER BY m.silo, m.document_sigla
    """, (meta_pdot,))
    return c.fetchall()


def get_docs_for_silo(conn, silo: str) -> list[dict]:
    """Retorna documentos que alimentan un silo específico."""
    c = conn.cursor()
    c.execute("""
        SELECT m.document_sigla, m.mnt_uuid, m.meta_pdot,
               m.variable_icpi, m.confidence, m.source_entity,
               COUNT(n.id) AS chunks
        FROM corpus_mnt_mapping m
        LEFT JOIN normativa_corpus n ON n.norma_sigla = m.document_sigla
        WHERE m.silo LIKE %s
        GROUP BY m.document_sigla, m.mnt_uuid, m.meta_pdot,
                 m.variable_icpi, m.confidence, m.source_entity
        ORDER BY m.document_sigla
    """, (f"%{silo}%",))
    return c.fetchall()


def get_evidence_sample(conn, sigla: str, keywords: list[str], n: int = 3) -> list[str]:
    """Retorna muestra de chunks relevantes de un documento."""
    c = conn.cursor()
    # Buscar chunks con palabras clave
    for kw in keywords[:3]:
        c.execute("""
            SELECT contenido FROM normativa_corpus
            WHERE norma_sigla = %s AND contenido ILIKE %s
            LIMIT %s
        """, (sigla, f"%{kw}%", n))
        rows = c.fetchall()
        if rows:
            return [r["contenido"][:200] for r in rows]
    return []


# ── REPORTES ──────────────────────────────────────────────────────────────────

def report_dimension(dim_key: str) -> None:
    """Reporte explicable para una dimension TGI (D1-D5)."""
    dim = TGI_DIMENSION_MAP.get(dim_key.upper())
    if not dim:
        print(f"Dimension no reconocida: {dim_key}. Use D1-D5.")
        return

    # Obtener valor del Gold Master
    gm = fetch_gold_master_data()
    raw = gm["data"].get("_raw_h73", {})
    tgi = gm["data"].get("tgi", {})
    dim_key_lower = dim_key.lower()
    valor = tgi.get(dim_key_lower, "?")

    conn = get_connection()

    print(f"\n{'='*62}")
    print(f"  REPORTE EXPLICABLE — {dim_key}: {dim['nombre']}")
    print(f"  Valor Gold Master: {valor:.2f}%")
    print(f"  {dim['nota']}")
    print(f"{'='*62}")

    for silo in dim["silos"]:
        docs = get_docs_for_silo(conn, silo)
        if docs:
            print(f"\n  Silo {silo} — {len(docs)} documento(s):")
            for d in docs:
                conf_str = f"conf={d['confidence']:.1f}"
                meta_str = f"meta={d['meta_pdot']}" if d.get('meta_pdot') else ""
                print(f"    {d['document_sigla']:40s} var={d['variable_icpi']:12s} "
                      f"{meta_str:20s} {conf_str}  [{d['chunks']} chunks]")

    conn.close()
    print(f"\n  Interpretacion:")
    print(f"  Los documentos listados son la evidencia territorial que")
    print(f"  el Gold Master usa para calcular {dim_key} = {valor:.2f}%.\n")


def report_meta(meta_id: str) -> None:
    """Reporte explicable para una meta PDOT específica."""
    conn = get_connection()

    # Buscar en el mapeo
    docs = get_docs_for_meta(conn, meta_id)

    # Obtener el Vi y otros valores de la meta desde corpus
    gm = fetch_gold_master_data()

    print(f"\n{'='*62}")
    print(f"  REPORTE EXPLICABLE — Meta: {meta_id}")
    print(f"{'='*62}")
    print(f"\n  Documentos que evidencian esta meta:")

    for d in docs:
        print(f"    [{d['silo']:8s}] {d['document_sigla']:40s} → {d['variable_icpi']:10s} "
              f"({d['chunks']} chunks, conf={d['confidence']:.1f})")

    if not docs:
        print("  Sin documentos mapeados. Ejecutar tag_mnt_uuid.py primero.")

    conn.close()
    print(f"\n  Para ver el impacto en ICPI:")
    print(f"  Ver H12_MOTOR_ICPI_CANONICO fila correspondiente a {meta_id}")
    print(f"  Vi = f(V_eSIGEF, V_SERCOP, V_LOTAIP, V_CPCCS)\n")


def report_icpi_evidence() -> None:
    """Resumen de evidencia que respalda el ICPI completo."""
    gm = fetch_gold_master_data()
    raw = gm["data"].get("_raw_h73", {})
    icpi_2025 = raw.get("ICPI_2025", 0) * 100

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT silo, COUNT(*) as docs, SUM(chunks) as total_chunks
        FROM (
            SELECT m.silo, COUNT(n.id) as chunks
            FROM corpus_mnt_mapping m
            LEFT JOIN normativa_corpus n ON n.norma_sigla = m.document_sigla
            GROUP BY m.document_sigla, m.silo
        ) sub
        GROUP BY silo ORDER BY silo
    """)
    rows = c.fetchall()
    conn.close()

    print(f"\n{'='*62}")
    print(f"  EVIDENCIA COMPLETA — ICPI 2025 = {icpi_2025:.2f}%")
    print(f"  Pregunta: ¿Qué documentos respaldan este valor?")
    print(f"{'='*62}")
    print(f"\n  {'Silo':10s} {'Docs':>5} {'Chunks':>8}  Función")
    print(f"  {'-'*50}")
    silo_labels = {
        "S1": "Promesas electorales (IFE)",
        "S2": "Planificacion PDOT (Pi_plan)",
        "S3": "POA operativo (Pi)",
        "S3b": "PAC contratacion",
        "S3b+S4": "PAC + SERCOP (V_SERCOP)",
        "S4": "SERCOP procesos",
        "S5": "Cedulas ejecucion (Ti)",
        "S6": "SIGAD autoreporte (ICM)",
        "S8": "Rendicion de cuentas (V_CPCCS)",
        "S8b": "Presupuesto participativo (IGP)",
    }
    for r in rows:
        label = silo_labels.get(r["silo"], "")
        print(f"  {r['silo']:10s} {r['docs']:>5} {r['total_chunks'] or 0:>8}  {label}")

    print(f"\n  Para ver el calculo completo:")
    print(f"  → Gold Master H12_MOTOR_ICPI_CANONICO")
    print(f"  → app/connectors/gold_master.py → H73_OUTPUT_API\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 6.6C: Explainability Report ICPI")
    parser.add_argument("--meta",  help="Meta PDOT (ej. AH-I-N-01)")
    parser.add_argument("--silo",  help="Silo Excel (S3/S5/S8/etc.)")
    parser.add_argument("--d1",    action="store_true")
    parser.add_argument("--d2",    action="store_true")
    parser.add_argument("--d3",    action="store_true")
    parser.add_argument("--d4",    action="store_true")
    parser.add_argument("--d5",    action="store_true")
    parser.add_argument("--icpi",  action="store_true")
    args = parser.parse_args()

    if args.meta:
        report_meta(args.meta)
    elif args.silo:
        docs = get_docs_for_silo(get_connection(), args.silo)
        print(f"\n  Silo {args.silo}: {len(docs)} documentos")
        for d in docs:
            print(f"  {d['document_sigla']:40s} meta={d['meta_pdot']}  var={d['variable_icpi']}")
    elif args.d1: report_dimension("D1")
    elif args.d2: report_dimension("D2")
    elif args.d3: report_dimension("D3")
    elif args.d4: report_dimension("D4")
    elif args.d5: report_dimension("D5")
    elif args.icpi: report_icpi_evidence()
    else:
        print("\nUso: python -X utf8 explainability_report.py [--meta ID | --d1..d5 | --icpi]")
        report_icpi_evidence()


if __name__ == "__main__":
    main()
