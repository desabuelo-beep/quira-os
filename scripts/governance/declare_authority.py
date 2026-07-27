# -*- coding: utf-8 -*-
"""
scripts/governance/declare_authority.py — Declaración masiva de autoridad
═══════════════════════════════════════════════════════════════════════════════
Implementa el Art. 1 de la Carta (Principio de Derivación) sobre los artefactos
HUÉRFANOS existentes. NO inventa autoridad: la DERIVA de lo que el artefacto ya
declara semánticamente (`fundamenta_en`, `deriva_de`) y solo cae a un padre por
defecto cuando el artefacto no expresa ninguno.

IDEMPOTENTE: si el bloque `authority:` ya existe, no lo toca.
Formato: YAML → clave top-level. Markdown → front-matter.

Uso:  python scripts/governance/declare_authority.py [--dry-run]
Dylus Lab © 2026
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [9]
#   type: OPERATIVA
# ---
from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
DRY = "--dry-run" in sys.argv

RE_TIENE_AUTH = re.compile(r"^authority:", re.M)
RE_FUNDAMENTA = re.compile(r"^fundamenta_en:\s*(\S+)", re.M)
RE_DERIVA = re.compile(r"^deriva_de:\s*(\S+)", re.M)
RE_ID = re.compile(r"^id:\s*(\S+)", re.M)
RE_OPERA = re.compile(r"^opera_en:\s*(\S+)", re.M)

# (glob, tipo_autoridad, padre_por_defecto, arts_constitucionales)
GRUPOS = [
    ("docs/brn/CNO-*.yaml", "NORMATIVA",   "GOVERNANCE-001", "[1, 2, 9]"),   # cadena jurídica verificada
    ("docs/brn/RO-*.yaml",  "NORMATIVA",   "GOVERNANCE-001", "[1, 9]"),      # lógica operacional
    ("docs/adr/ADR-*.md",   "ARQUITECTONICA", "GOVERNANCE-001", "[5, 20]"),
    ("docs/pcd/PCD-*.md",   "NORMATIVA",   "GOVERNANCE-001", "[1, 2]"),
    ("docs/observations/OBS-*.md", "OPERATIVA", "GOVERNANCE-001", "[1, 2, 8]"),  # hallazgos de evidencia
    ("scripts/governance/*.py", "OPERATIVA", "GOVERNANCE-001", "[9]"),
    ("data/d*/catalogo_*.yaml", "TECNICA",  "GOVERNANCE-001", "[1, 9]"),
    ("app/agents/d*/__init__.py", "TECNICA", "GOVERNANCE-001", "[3, 9]"),
    ("app/connectors/gold_master.py", "TECNICA", "GOVERNANCE-001", "[2]"),
]


def padre_real(txt: str, default: str) -> str:
    """Deriva el padre de lo que el artefacto YA declara. No inventa."""
    m = RE_FUNDAMENTA.search(txt)            # micro-CNO → su marco
    if m:
        return m.group(1)
    m = RE_DERIVA.search(txt)                # RO → su CNO ("CNO-VIII-000 v1.0" → id)
    if m:
        return m.group(1).split()[0]
    return default


def bloque_yaml(parent: str, tipo: str, arts: str) -> str:
    return (f"authority:\n"
            f"  parent: {parent}\n"
            f"  constitution_articles: {arts}\n"
            f"  type: {tipo}\n")


def procesar(p: Path, tipo: str, default: str, arts: str) -> str | None:
    txt = p.read_text(encoding="utf-8", errors="replace")
    if RE_TIENE_AUTH.search(txt):
        return None                                   # idempotente
    parent = padre_real(txt, default)
    if p.suffix == ".yaml":
        # se inserta tras la línea `id:` si existe, si no al inicio del cuerpo
        m = RE_ID.search(txt)
        blk = bloque_yaml(parent, tipo, arts)
        if m:
            fin = txt.index("\n", m.end()) + 1
            nuevo = txt[:fin] + blk + txt[fin:]
        else:
            nuevo = blk + txt
    else:
        # markdown / python → front-matter o encabezado comentado
        if p.suffix == ".py":
            # CRÍTICO: el bloque va DESPUÉS del docstring del módulo — anteponerlo
            # dejaría el docstring sin ser lo primero y rompería __doc__.
            blk = ('# ---\n# authority:\n'
                   f'#   parent: {parent}\n'
                   f'#   constitution_articles: {arts}\n'
                   f'#   type: {tipo}\n# ---\n')
            m_doc = re.match(r'\s*(#[^\n]*\n)*\s*("""|\'\'\')', txt)
            if m_doc:
                q = m_doc.group(2)
                fin = txt.index(q, m_doc.end()) + 3          # cierre del docstring
                fin = txt.index("\n", fin) + 1
                nuevo = txt[:fin] + blk + txt[fin:]
            else:
                nuevo = blk + txt
        else:
            nuevo = "---\n" + bloque_yaml(parent, tipo, arts) + "---\n\n" + txt
    if not DRY:
        p.write_text(nuevo, encoding="utf-8")
    return parent


def main() -> int:
    tot, hechos = 0, 0
    resumen: dict[str, int] = {}
    for patron, tipo, default, arts in GRUPOS:
        for p in sorted(REPO.glob(patron)):
            if not p.is_file():
                continue
            tot += 1
            par = procesar(p, tipo, default, arts)
            if par:
                hechos += 1
                resumen[patron] = resumen.get(patron, 0) + 1
    print(f"{'[DRY-RUN] ' if DRY else ''}Autoridad declarada en {hechos}/{tot} artefactos")
    for k, v in resumen.items():
        print(f"   {k:34} {v}")
    if hechos == 0:
        print("   (todos ya declaraban autoridad — idempotente)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
