# -*- coding: utf-8 -*-
"""
tag_domains.py — Gate 6.6B: Tagging Dom01-D12 en corpus_mnt_mapping
QUIRA Gov · Dylus Lab © 2026

Agrega el dominio canónico a cada sigla ya trazada con MNT_UUID.

12 DOMINIOS CANÓNICOS INMUTABLES (docs/REFERENCE.md):
  D01 Planificación Estratégica
  D02 Presupuesto & Financiamiento
  D03 Seguimiento de Metas
  D04 Alertas Institucionales
  D05 Holding Municipal
  D06 Salud Institucional
  D07 Transparencia
  D08 Participación Ciudadana
  D09 Rendición de Cuentas
  D10 Territorio & Cobertura
  D11 Ecosistema Productivo Territorial (DISABLED)
  D12 Protección Social & Grupos Prioritarios

Cuando exista: Documento → MNT_UUID → Meta → Dominio → Silo → Variable ICPI
La trazabilidad estará completa (ADR-023 Sprint Ontología Territorial).

Uso:
  python -X utf8 scripts/analysis/tag_domains.py
  python -X utf8 scripts/analysis/tag_domains.py --status
  python -X utf8 scripts/analysis/tag_domains.py --dry-run
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

# ── MAPEO SIGLA → DOMINIO(S) ──────────────────────────────────────────────────
# Dominio primario = el que la UI muestra. Secundario = contexto adicional.
# Fuente: docs/REFERENCE.md tabla 12 DOMINIOS CANÓNICOS + mapeo meta PDOT.

# Meta PDOT → Dominio primario
META_DOMINIO = {
    "SC-I-N-01":  "D10",  # Agua potable → Territorio & Cobertura
    "SC-L-N-02":  "D06",  # Talento humano → Salud Institucional
    "AH-I-X-01":  "D02",  # Sostenibilidad financiera → Presupuesto
    "AH-I-X-02":  "D10",  # Vialidad → Territorio & Cobertura
    "AH-I-X-03":  "D12",  # Salud/Patronato → Protección Social
    "AH-I-N-01":  "D10",  # Desechos sólidos → Territorio & Cobertura
    "SC-L-G-01":  "D10",  # Alcantarillado → Territorio & Cobertura
    "AH-I-X-04":  "D06",  # Modernización → Salud Institucional
    "PI-I-G-01":  "D10",  # Equipamientos → Territorio & Cobertura
    "AH-C-X-01":  "D12",  # Derechos sociales → Protección Social
    "AH-C-X-02":  "D01",  # Sistema info territorial → Planificación
    "SC-I-N-03":  "D08",  # Participación ciudadana → Participación
    "FA-I-X-01":  "D04",  # Gestión del riesgo → Alertas Institucionales
    "FA-C-X-01":  "D10",  # Áreas verdes → Territorio & Cobertura
    "FA-I-X-02":  "D10",  # Equipamiento urbano → Territorio & Cobertura
    "FA-L-N-01":  "D09",  # Patrimonio cultural → Rendición/Cultura
    "PI-I-G-02":  "D01",  # PDOT/PUGS → Planificación Estratégica
    "PI-L-G-01":  "D10",  # Señalización vial → Territorio & Cobertura
    "EP-L-N-01":  "D12",  # Vivienda → Protección Social
    "EP-L-X-01":  "D05",  # Productivo → Holding Municipal
    "PI-TUR-01":  "D10",  # Turismo → Territorio & Cobertura
    "PI-TUR-02":  "D10",  # Eventos turísticos → Territorio & Cobertura
    "FA-CC-01":   "D10",  # Cambio climático → Territorio & Cobertura
    "AH-AP-04":   "D10",  # Agua potable continuidad → Territorio
    "FA-DIS-01":  "D10",  # Disposición final → Territorio & Cobertura
}

# Silo/tipo de documento → Dominio cuando no hay meta específica
SILO_DOMINIO = {
    "S1":      "D08",  # CNE promesas → Participación Ciudadana
    "S2":      "D01",  # PDOT/PAI → Planificación Estratégica
    "S3":      "D03",  # POA → Seguimiento de Metas
    "S3b":     "D02",  # PAC → Presupuesto & Financiamiento
    "S3b+S4":  "D02",  # PAC+SERCOP → Presupuesto & Financiamiento
    "S4":      "D02",  # SERCOP → Presupuesto & Financiamiento
    "S5":      "D07",  # Cédulas → Transparencia
    "S6":      "D03",  # SIGAD → Seguimiento de Metas
    "S8":      "D09",  # RC/RDC → Rendición de Cuentas
    "S8b":     "D08",  # PP → Participación Ciudadana
}

# Entidad → Dominio para documentos del Holding sin meta específica
ENTITY_DOMINIO = {
    "GAD_MCR":       None,        # GAD: usar silo_dominio
    "BOMBEROS_MCR":  "D04",       # Bomberos → Alertas Institucionales
    "EP_ASEO_MCR":   "D10",       # EP Aseo → Territorio & Cobertura
    "PATRONATO_MCR": "D12",       # Patronato → Protección Social
}

DOMINIO_NOMBRES = {
    "D01": "Planificación Estratégica",
    "D02": "Presupuesto & Financiamiento",
    "D03": "Seguimiento de Metas",
    "D04": "Alertas Institucionales",
    "D05": "Holding Municipal",
    "D06": "Salud Institucional",
    "D07": "Transparencia",
    "D08": "Participación Ciudadana",
    "D09": "Rendición de Cuentas",
    "D10": "Territorio & Cobertura",
    "D11": "Ecosistema Productivo (DISABLED)",
    "D12": "Protección Social & Grupos Prioritarios",
}


def resolve_dominio(row: dict) -> str | None:
    """Resuelve el dominio canónico para un registro de corpus_mnt_mapping."""
    meta = row.get("meta_pdot")
    silo = row.get("silo", "")
    entity = row.get("source_entity", "")

    # 1. Meta PDOT específica → dominio preciso
    if meta and meta in META_DOMINIO:
        return META_DOMINIO[meta]

    # 2. Entidad no-GAD → dominio de entidad
    ent_dom = ENTITY_DOMINIO.get(entity)
    if ent_dom:
        return ent_dom

    # 3. Silo → dominio por tipo de instrumento
    for silo_key in [silo, silo.split("+")[0]]:
        if silo_key in SILO_DOMINIO:
            return SILO_DOMINIO[silo_key]

    return None


def cmd_tag(conn, dry_run: bool = False) -> None:
    """Agrega campo dominio a corpus_mnt_mapping."""

    # Agregar columna si no existe
    if not dry_run:
        try:
            conn.execute("ALTER TABLE corpus_mnt_mapping ADD COLUMN IF NOT EXISTS dominio TEXT")
            conn.commit()
        except Exception:
            pass

    c = conn.cursor()
    c.execute("""
        SELECT id, document_sigla, meta_pdot, silo, source_entity, dominio
        FROM corpus_mnt_mapping
        ORDER BY document_sigla
    """)
    rows = c.fetchall()

    updated = already = unknown = 0
    print(f"\n  Gate 6.6B — Dom01-D12 tagging")
    print(f"  {len(rows)} registros en corpus_mnt_mapping\n")

    for row in rows:
        dominio = resolve_dominio(row)
        actual = row.get("dominio")

        if dominio == actual:
            already += 1
            continue

        nombre = DOMINIO_NOMBRES.get(dominio, "?") if dominio else "SIN DOMINIO"

        if dry_run:
            print(f"  [DRY] {row['document_sigla']:42s} → {dominio or '???':4s}  {nombre}")
        else:
            conn.execute("""
                UPDATE corpus_mnt_mapping SET dominio = %s WHERE id = %s
            """, (dominio, row["id"]))
            conn.commit()
            print(f"  [OK]  {row['document_sigla']:42s} → {dominio or '???':4s}  {nombre}")

        if dominio:
            updated += 1
        else:
            unknown += 1
            if not dry_run:
                print(f"  [WARN] sin dominio: {row['document_sigla']}")

    print(f"\n  {'='*55}")
    print(f"  Actualizados: {updated}  |  Ya tenían: {already}  |  Sin dominio: {unknown}")
    print(f"  {'='*55}\n")


def cmd_status(conn) -> None:
    """Resumen de dominios asignados."""
    c = conn.cursor()
    c.execute("""
        SELECT dominio, COUNT(*) as docs
        FROM corpus_mnt_mapping
        GROUP BY dominio ORDER BY dominio
    """)
    rows = c.fetchall()

    print(f"\n  {'Dominio':6s} {'Nombre':40s} {'Docs':>5}")
    print(f"  {'-'*55}")
    for r in rows:
        dom = r["dominio"] or "NULL"
        nombre = DOMINIO_NOMBRES.get(dom, "SIN ASIGNAR")
        print(f"  {dom:6s} {nombre:40s} {r['docs']:>5}")

    c.execute("SELECT COUNT(*) as total FROM corpus_mnt_mapping")
    total = c.fetchone()
    total_n = list(total.values())[0]
    c.execute("SELECT COUNT(*) as con FROM corpus_mnt_mapping WHERE dominio IS NOT NULL")
    con = c.fetchone()
    con_n = list(con.values())[0]
    print(f"\n  Con dominio: {con_n}/{total_n} ({con_n/total_n*100:.0f}%)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gate 6.6B: Dom01-D12 tagging")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument("--status",  action="store_true")
    args = parser.parse_args()

    conn = get_connection()
    if args.status:
        cmd_status(conn)
    else:
        cmd_tag(conn, dry_run=args.dry_run)
    conn.close()


if __name__ == "__main__":
    main()
