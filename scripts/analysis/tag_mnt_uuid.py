# -*- coding: utf-8 -*-
"""
tag_mnt_uuid.py — Gate 6.6A: SIGLA → MNT_UUID → Meta → Silo → Indicador
QUIRA Gov · Dylus Lab © 2026

Transforma cada sigla del corpus MCR en un nodo de trazabilidad completo:
  SIGLA → MNT_UUID → Meta PDOT → Dominio → Silo Excel → Variable ICPI

Fuente de verdad: MATRIZ_CANONICA del Gold Master (SIAP-ICPI v5.5).
No hay IA. No hay embeddings. Solo trazabilidad exacta, confidence=1.0.

Crea tabla: corpus_mnt_mapping
  document_sigla    — SIGLA en normativa_corpus
  mnt_uuid          — ID canónico en MATRIZ_CANONICA del Excel
  actividad_id      — ID actividad (POA-2024, PAC-2025, RENDIC-2023, etc.)
  meta_pdot         — Meta PDOT relacionada (SC-I-N-01, etc.) o NULL si doc transversal
  source_entity     — GAD_MCR / BOMBEROS_MCR / EP_ASEO_MCR / PATRONATO_MCR
  silo              — Silo Excel que alimenta (S2/S3/S3b/S4/S5/S6/S8/S8b)
  variable_icpi     — Variable que actualiza (Pi/V_SERCOP/Ti/ICM/V_CPCCS/IGP)
  confidence        — 1.0 = MATRIZ_CANONICA exacta | 0.8 = inferencia meta-entidad
  mapping_source    — MATRIZ_CANONICA | META_ENTIDAD

Uso:
  python -X utf8 scripts/analysis/tag_mnt_uuid.py
  python -X utf8 scripts/analysis/tag_mnt_uuid.py --status
  python -X utf8 scripts/analysis/tag_mnt_uuid.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
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

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── MAPEO CANÓNICO: SIGLA → MNT (desde MATRIZ_CANONICA del Excel) ─────────────
#
# Estructura: (mnt_uuid, actividad_id, meta_pdot, source_entity, silo, variable, confidence, source)
#
# Regla silos:
#   S2  = PDOT/planificación → Pi_plan
#   S3  = POA operativo       → Pi (presupuesto)
#   S3b = PAC contratación    → V_SERCOP (junto con S4)
#   S4  = SERCOP procesos     → V_SERCOP
#   S5  = eSIGEF cédulas      → Ti (devengado/codificado) + V_eSIGEF
#   S6  = SIGAD autoreporte   → ICM por meta
#   S8  = CPCCS/RDC           → V_CPCCS (mencionada en rendición)
#   S8b = PP participativo    → IGP (gobernanza participativa)

SIGLA_MAP: dict[str, tuple] = {

    # ── GAD Montecristi ────────────────────────────────────────────────────────
    "RC-GAD-2023":         ("MNT-DOC-2023-0016", "RENDIC-2023",  None, "GAD_MCR",       "S8",      "V_CPCCS",    1.0, "MATRIZ_CANONICA"),
    "RC-GAD-2024":         ("MNT-DOC-2024-0021", "RENDIC-2024",  None, "GAD_MCR",       "S8",      "V_CPCCS",    1.0, "MATRIZ_CANONICA"),
    "POA-GAD-2023":        ("MNT-DOC-2023-0015", "POA-2023",     None, "GAD_MCR",       "S3",      "Pi",         1.0, "MATRIZ_CANONICA"),
    "POA-GAD-2024":        ("MNT-DOC-2024-0020", "POA-2024",     None, "GAD_MCR",       "S3",      "Pi",         1.0, "MATRIZ_CANONICA"),
    "POA-GAD-2025":        ("MNT-DOC-2025-0025", "POA-2025",     None, "GAD_MCR",       "S3",      "Pi",         1.0, "MATRIZ_CANONICA"),
    "POA-GAD-2026-v2":     ("MNT-DOC-2026-0028", "POA-2026",     None, "GAD_MCR",       "S3",      "Pi",         1.0, "MATRIZ_CANONICA"),
    "PAC-GAD-2023":        ("MNT-DOC-2023-0013", "PAC-2023",     None, "GAD_MCR",       "S3b+S4",  "V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-GAD-2024":        ("MNT-DOC-2024-0019", "PAC-2024",     None, "GAD_MCR",       "S3b+S4",  "V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-GAD-2025":        ("MNT-DOC-2025-0024", "PAC-2025",     None, "GAD_MCR",       "S3b+S4",  "V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-GAD-2026":        ("MNT-DOC-2026-0027", "PAC-2026",     None, "GAD_MCR",       "S3b+S4",  "V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "SIGAD-GAD-2023-DOC":  ("MNT-DOC-2023-0017", "ICM_SI-2023",  None, "GAD_MCR",       "S6",      "ICM",        1.0, "MATRIZ_CANONICA"),
    "SIGAD-GAD-2024-DOC":  ("MNT-DOC-2024-0022", "ICM_SI-2024",  None, "GAD_MCR",       "S6",      "ICM",        1.0, "MATRIZ_CANONICA"),
    "PAI-GAD-2023":        ("MNT-DOC-2023-0014", "PAI-2023",     None, "GAD_MCR",       "S2",      "Pi_plan",    1.0, "MATRIZ_CANONICA"),
    "PP-GAD-2024":         ("MNT-DOC-2024-0018", "PRESUP-2024",  "SC-I-N-03", "GAD_MCR","S8b",    "IGP",        1.0, "MATRIZ_CANONICA"),
    "PP-GAD-2025":         ("MNT-DOC-2025-0023", "PRESUP-2025",  "SC-I-N-03", "GAD_MCR","S8b",    "IGP",        1.0, "MATRIZ_CANONICA"),
    "PP-GAD-2026":         ("MNT-DOC-2026-PP",   "PRESUP-2026",  "SC-I-N-03", "GAD_MCR","S8b",    "IGP",        0.8, "META_ENTIDAD"),
    "RES-ORG-GAD-2025":    ("MNT-DOC-2025-0026", "RESOLU-2025",  None, "GAD_MCR",       "S3",      "Pi_org",     1.0, "MATRIZ_CANONICA"),
    "PDOT-MONTECRISTI":    ("MNT-PDOT-CANON",    "PDOT-2023",    None, "GAD_MCR",       "S2",      "Pi_plan",    0.8, "META_ENTIDAD"),
    "PAI-GAD-2025":        ("MNT-DOC-2025-PAI",  "PAI-2025",     None, "GAD_MCR",       "S2",      "Pi_plan",    0.8, "META_ENTIDAD"),
    "PAI-GAD-2026":        ("MNT-DOC-2026-PAI",  "PAI-2026",     None, "GAD_MCR",       "S2",      "Pi_plan",    0.8, "META_ENTIDAD"),
    "PAI-PLURIANUAL-GAD":  ("MNT-DOC-PAI-PLURI", "PAI-PLURIANUAL",None,"GAD_MCR",       "S2",      "Pi_plan",    0.8, "META_ENTIDAD"),
    "PLAN-BICENTENARIO-MCR":("MNT-DOC-BICENT",   "PLAN-CNE",     None, "GAD_MCR",       "S1",      "IFE_CNE",    0.8, "META_ENTIDAD"),
    "PLAN-GOB-MCR":        ("MNT-DOC-PLANGOB",   "PLAN-CNE-2023",None, "GAD_MCR",       "S1",      "IFE_CNE",    0.8, "META_ENTIDAD"),

    # ── Bomberos Montecristi ───────────────────────────────────────────────────
    "PAC-BOMBEROS-2023":   ("MNT-DOC-2023-0001", "PAC-2023",     "FA-I-X-01", "BOMBEROS_MCR","S3b","V_SERCOP",  1.0, "MATRIZ_CANONICA"),
    "PAC-BOMBEROS-2024":   ("MNT-DOC-2024-0002", "PAC-2024",     "FA-I-X-01", "BOMBEROS_MCR","S3b","V_SERCOP",  1.0, "MATRIZ_CANONICA"),
    "POA-BOMBEROS-2024":   ("MNT-DOC-2024-0003", "POA-2024",     "FA-I-X-01", "BOMBEROS_MCR","S3", "Pi",        1.0, "MATRIZ_CANONICA"),
    "PAC-BOMBEROS-2025":   ("MNT-DOC-2025-0004", "PAC-2025",     "FA-I-X-01", "BOMBEROS_MCR","S3b","V_SERCOP",  1.0, "MATRIZ_CANONICA"),
    "POA-BOMBEROS-2025":   ("MNT-DOC-2025-0005", "POA-2025",     "FA-I-X-01", "BOMBEROS_MCR","S3", "Pi",        1.0, "MATRIZ_CANONICA"),
    "PAC-BOMBEROS-2026":   ("MNT-DOC-2026-0006", "PAC-2026",     "FA-I-X-01", "BOMBEROS_MCR","S3b","V_SERCOP",  1.0, "MATRIZ_CANONICA"),
    "POA-BOMBEROS-2026":   ("MNT-DOC-2026-0007", "POA-2026",     "FA-I-X-01", "BOMBEROS_MCR","S3", "Pi",        1.0, "MATRIZ_CANONICA"),
    # RCs Bomberos — evidencia S8 para meta FA-I-X-01 (Gestión del riesgo)
    "RC-BOMBEROS-2023":    ("MNT-DOC-2023-BOMB-RC","RENDIC-2023","FA-I-X-01", "BOMBEROS_MCR","S8", "V_CPCCS",   0.8, "META_ENTIDAD"),
    "RC-BOMBEROS-2024":    ("MNT-DOC-2024-BOMB-RC","RENDIC-2024","FA-I-X-01", "BOMBEROS_MCR","S8", "V_CPCCS",   0.8, "META_ENTIDAD"),

    # ── EP Aseo Montecristi ────────────────────────────────────────────────────
    "PAC-ASEO-2023":       ("MNT-DOC-2023-0008", "PAC-2023",     "AH-I-N-01", "EP_ASEO_MCR","S3b","V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-ASEO-2024":       ("MNT-DOC-2024-0009", "PAC-2024",     "AH-I-N-01", "EP_ASEO_MCR","S3b","V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-ASEO-2025":       ("MNT-DOC-2025-0010", "PAC-2025",     "AH-I-N-01", "EP_ASEO_MCR","S3b","V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "PAC-ASEO-2026":       ("MNT-DOC-2026-0011", "PAC-2026",     "AH-I-N-01", "EP_ASEO_MCR","S3b","V_SERCOP",   1.0, "MATRIZ_CANONICA"),
    "POA-ASEO-2026":       ("MNT-DOC-2026-0012", "POA-2026",     "AH-I-N-01", "EP_ASEO_MCR","S3", "Pi",         1.0, "MATRIZ_CANONICA"),
    # POA Aseo 2024/2025 — en MATRIZ pero nombre distinto
    "POA-ASEO-2024":       ("MNT-DOC-2024-ASEO-POA","POA-2024",  "AH-I-N-01", "EP_ASEO_MCR","S3", "Pi",         0.8, "META_ENTIDAD"),
    "POA-ASEO-2025":       ("MNT-DOC-2025-ASEO-POA","POA-2025",  "AH-I-N-01", "EP_ASEO_MCR","S3", "Pi",         0.8, "META_ENTIDAD"),
    # RCs Aseo — evidencia S8 para meta AH-I-N-01 (desechos sólidos)
    "RC-ASEO-2023":        ("MNT-DOC-2023-ASEO-RC","RENDIC-2023","AH-I-N-01", "EP_ASEO_MCR","S8", "V_CPCCS",    0.8, "META_ENTIDAD"),
    "RC-ASEO-2024":        ("MNT-DOC-2024-ASEO-RC","RENDIC-2024","AH-I-N-01", "EP_ASEO_MCR","S8", "V_CPCCS",    0.8, "META_ENTIDAD"),

    # ── Patronato Montecristi ──────────────────────────────────────────────────
    "PAC-PATRONATO-2023":  ("MNT-DOC-2023-0029", "PAC-2023",     "AH-C-X-01", "PATRONATO_MCR","S3b","V_SERCOP", 1.0, "MATRIZ_CANONICA"),
    "POA-PATRONATO-2023":  ("MNT-DOC-2023-0030", "POA-2023",     "AH-C-X-01", "PATRONATO_MCR","S3", "Pi",       1.0, "MATRIZ_CANONICA"),
    "PAC-PATRONATO-2024":  ("MNT-DOC-2024-0031", "PAC-2024",     "AH-C-X-01", "PATRONATO_MCR","S3b","V_SERCOP", 1.0, "MATRIZ_CANONICA"),
    "POA-PATRONATO-2024":  ("MNT-DOC-2024-0032", "POA-2024",     "AH-C-X-01", "PATRONATO_MCR","S3", "Pi",       1.0, "MATRIZ_CANONICA"),
    "PAC-PATRONATO-2025":  ("MNT-DOC-2025-0033", "PAC-2025",     "AH-C-X-01", "PATRONATO_MCR","S3b","V_SERCOP", 1.0, "MATRIZ_CANONICA"),
    "PAC-PATRONATO-2026":  ("MNT-DOC-2026-0035", "PAC-2026",     "AH-C-X-01", "PATRONATO_MCR","S3b","V_SERCOP", 1.0, "MATRIZ_CANONICA"),
    # RCs Patronato — evidencia S8 para metas AH-I-X-03 (salud) + AH-C-X-01 (derechos)
    "RC-PATRONATO-2023":   ("MNT-DOC-2023-PAT-RC","RENDIC-2023", "AH-C-X-01", "PATRONATO_MCR","S8","V_CPCCS",   0.8, "META_ENTIDAD"),
    "RC-PATRONATO-2024":   ("MNT-DOC-2024-PAT-RC","RENDIC-2024", "AH-C-X-01", "PATRONATO_MCR","S8","V_CPCCS",   0.8, "META_ENTIDAD"),
    "PRESUP-PATRONATO-2024-DOC":("MNT-DOC-2024-PAT-PRESUP","PRESUP-2024","AH-C-X-01","PATRONATO_MCR","S5","Ti",  0.8, "META_ENTIDAD"),

    # ── Normativa de referencia (no alimenta silos directamente) ──────────────
    "RES-ORG-GADMCM-2025": ("MNT-DOC-2025-NORMA","RESOLU-2025",  None, "GAD_MCR",       "S3",      "Pi_org",     0.8, "META_ENTIDAD"),
}


# ── CREAR TABLA ───────────────────────────────────────────────────────────────

DDL = """
CREATE TABLE IF NOT EXISTS corpus_mnt_mapping (
    id                SERIAL PRIMARY KEY,
    document_sigla    TEXT NOT NULL,
    mnt_uuid          TEXT NOT NULL,
    actividad_id      TEXT,
    meta_pdot         TEXT,
    source_entity     TEXT,
    silo              TEXT,
    variable_icpi     TEXT,
    confidence        FLOAT  DEFAULT 1.0,
    mapping_source    TEXT   DEFAULT 'MATRIZ_CANONICA',
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (document_sigla)
);
CREATE INDEX IF NOT EXISTS idx_mnt_uuid ON corpus_mnt_mapping(mnt_uuid);
CREATE INDEX IF NOT EXISTS idx_mnt_sigla ON corpus_mnt_mapping(document_sigla);
CREATE INDEX IF NOT EXISTS idx_mnt_silo ON corpus_mnt_mapping(silo);
CREATE INDEX IF NOT EXISTS idx_mnt_meta ON corpus_mnt_mapping(meta_pdot);
"""


def create_table(conn) -> None:
    for stmt in DDL.strip().split(";"):
        stmt = stmt.strip()
        if stmt:
            conn.execute(stmt + ";")
    conn.commit()
    print("  Tabla corpus_mnt_mapping: OK")


# ── POBLAR TABLA ──────────────────────────────────────────────────────────────

def tag_all(conn, dry_run: bool = False) -> None:
    # Siglas que existen en el corpus MCR
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT norma_sigla FROM normativa_corpus
        WHERE canton_id = 'MCR'
    """)
    corpus_siglas = {r["norma_sigla"] for r in c.fetchall()}

    inserted = skipped = missing = 0
    print(f"\n  Siglas en corpus MCR: {len(corpus_siglas)}")
    print(f"  Siglas en SIGLA_MAP:  {len(SIGLA_MAP)}")
    print()

    for sigla, mapping in SIGLA_MAP.items():
        mnt_uuid, actividad_id, meta_pdot, source_entity, silo, variable, confidence, source = mapping

        if sigla not in corpus_siglas:
            print(f"  [SKIP-no-corpus] {sigla}")
            missing += 1
            continue

        if dry_run:
            print(f"  [DRY] {sigla:45s} → {mnt_uuid}  silo={silo}  var={variable}  conf={confidence}")
            continue

        try:
            conn.execute("""
                INSERT INTO corpus_mnt_mapping
                    (document_sigla, mnt_uuid, actividad_id, meta_pdot,
                     source_entity, silo, variable_icpi, confidence, mapping_source)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (document_sigla) DO UPDATE SET
                    mnt_uuid       = EXCLUDED.mnt_uuid,
                    actividad_id   = EXCLUDED.actividad_id,
                    meta_pdot      = EXCLUDED.meta_pdot,
                    source_entity  = EXCLUDED.source_entity,
                    silo           = EXCLUDED.silo,
                    variable_icpi  = EXCLUDED.variable_icpi,
                    confidence     = EXCLUDED.confidence,
                    mapping_source = EXCLUDED.mapping_source
            """, (sigla, mnt_uuid, actividad_id, meta_pdot,
                  source_entity, silo, variable, confidence, source))
            conn.commit()
            print(f"  [OK]  {sigla:45s} → {mnt_uuid}  silo={silo}")
            inserted += 1
        except Exception as e:
            print(f"  [ERR] {sigla}: {e}")

    # Siglas en corpus sin mapeo
    unmapped = corpus_siglas - set(SIGLA_MAP.keys())
    if unmapped:
        print(f"\n  Sin mapeo (necesitan revisión):")
        for s in sorted(unmapped):
            print(f"    {s}")

    print(f"\n  {'='*50}")
    print(f"  Mapeados: {inserted}  |  Sin corpus: {missing}  |  Sin mapeo: {len(unmapped)}")
    print(f"  {'='*50}\n")


# ── STATUS ────────────────────────────────────────────────────────────────────

def cmd_status(conn) -> None:
    c = conn.cursor()
    c.execute("""
        SELECT silo, COUNT(*) AS docs,
               COUNT(DISTINCT meta_pdot) FILTER (WHERE meta_pdot IS NOT NULL) AS metas
        FROM corpus_mnt_mapping
        GROUP BY silo ORDER BY silo
    """)
    rows = c.fetchall()
    if not rows:
        print("  corpus_mnt_mapping vacía. Ejecutar sin --status primero.")
        return

    print(f"\n  {'Silo':10s} {'Docs':>6} {'Metas PDOT':>12}")
    print("  " + "-"*30)
    total = 0
    for r in rows:
        print(f"  {r['silo']:10s} {r['docs']:>6}  {r['metas']:>10}")
        total += r['docs']
    print("  " + "-"*30)
    print(f"  {'TOTAL':10s} {total:>6}")

    # Contar siglas sin mapeo
    c.execute("SELECT COUNT(DISTINCT norma_sigla) FROM normativa_corpus WHERE canton_id='MCR'")
    total_corpus = c.fetchone()
    total_corpus_n = list(total_corpus.values())[0] if isinstance(total_corpus, dict) else total_corpus[0]
    print(f"\n  Trazados: {total}/{total_corpus_n} siglas MCR ({total/total_corpus_n*100:.0f}%)")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 6.6A: tagging MNT_UUID en corpus MCR")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument("--status",  action="store_true")
    args = parser.parse_args()

    conn = get_connection()

    if args.status:
        cmd_status(conn)
        conn.close()
        return

    print("\n  Gate 6.6A — tag_mnt_uuid.py")
    print("  SIGLA → MNT_UUID → Meta → Silo → Variable ICPI\n")

    if not args.dry_run:
        create_table(conn)

    tag_all(conn, dry_run=args.dry_run)
    conn.close()


if __name__ == "__main__":
    main()
