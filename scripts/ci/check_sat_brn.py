# -*- coding: utf-8 -*-
"""
scripts/ci/check_sat_brn.py — ¿toda SAT del motor tiene cadena BRN que la funde?
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 9]
  type: TECNICA

POR QUÉ EXISTE (OBS-022 · hallazgo de Javo · 2026-07-29)

ADR-038 §1b: *"una CNO todavía es Derecho; una SAT ya es control"*, y los umbrales
**son lógica, así que viven en la RO**, no en `SAT_Catalogo`. Pero al medirlo:

    SAT en el Gold Master ......... 9
    SAT declaradas en alguna RO ... 1     ← 89% huérfanas

Ninguna RO tenía bloque `produce:`. El concepto existía en el ADR desde julio y
**nunca se implementó**, así que umbral y peso de 8 señales viven solo en el Excel:
si mañana cambia la norma que las funda, nada obliga a revisarlas.

Javo lo detectó preguntando por SAT-IX: *"¿por las SAT no debería pasar la BRN?"*.

QUÉ HACE
Reporta la deuda; **no rompe el gate**. Romperlo hoy bloquearía todo el trabajo por
una deuda heredada de 4 dominios ya cerrados. Cuando la deuda llegue a cero,
`--estricto` puede activarse en CI para impedir recurrencia.

Uso:
  python scripts/ci/check_sat_brn.py             → reporta la deuda
  python scripts/ci/check_sat_brn.py --estricto  → falla si hay SAT huérfanas
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
BRN = REPO / "docs" / "brn"

# Las 9 señales del Gold Master (SAT_Catalogo · verificado 2026-07-29).
# Se declaran aquí y no se leen del Excel: este gate debe correr sin abrir el motor.
SAT_MOTOR = {
    "SAT-0":    ("Coherencia POA-PAC",            "D2", "d01/d02"),
    "SAT-I":    ("Fragmentacion Selectiva",       "D3", "d03"),
    "SAT-II":   ("Reforma Significativa Tardia",  "D2", "d02"),
    "SAT-III":  ("Paralisis Presupuestaria",      "D3", "d02"),
    "SAT-IV":   ("Alerta Fiscal COOTAD",          "D3", "d02"),
    "SAT-V":    ("Brecha Compromiso CPCCS",       "D5", "d09"),
    "SAT-VI":   ("Desvio Presupuesto Participativo", "D4", "d08"),
    "SAT-VII":  ("Vi Sinaptico Pulso",            "D3", "informacional"),
    "SAT-VIII": ("Equidad Territorial",           "D4", "d10/d12"),
    "SAT-IX":   ("Brecha de Atencion Ciudadana",  "D4", "d08"),
}


def sat_declaradas() -> dict[str, str]:
    """SAT que alguna RO declara en su bloque `produce:` → {id_sat: archivo_ro}."""
    import yaml
    out: dict[str, str] = {}
    for f in sorted(BRN.glob("RO-*.yaml")):
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except Exception as e:                                  # YAML roto = hallazgo
            print(f"  ⚠️ {f.name}: YAML ilegible ({e})")
            continue
        for item in d.get("produce") or []:
            if isinstance(item, dict) and item.get("id"):
                out[item["id"]] = f.stem
    return out


def main() -> int:
    decl = sat_declaradas()
    huerfanas = [s for s in SAT_MOTOR if s not in decl]

    print("=== SAT ↔ CADENA BRN · ¿cada señal tiene RO que la funde? ===\n")
    print(f"  {'SAT':10} {'DIMENSIÓN':10} {'DOM':16} DECLARADA EN")
    for sat, (nombre, dim, dom) in SAT_MOTOR.items():
        ro = decl.get(sat)
        print(f"  {sat:10} {dim:10} {dom:16} {ro if ro else '❌ NINGUNA RO'}")

    total = len(SAT_MOTOR)
    print(f"\n  con cadena BRN : {total - len(huerfanas)} / {total}")
    print(f"  HUÉRFANAS      : {len(huerfanas)}  ({len(huerfanas) / total:.0%})")

    if huerfanas:
        print("\n  DEUDA (OBS-022) — el umbral y el peso viven solo en el Excel:")
        print(f"    {', '.join(huerfanas)}")
        print("\n  Se salda añadiendo el bloque `produce:` a la RO de cada dominio,")
        print("  con umbral, peso, justificación y frontera interpretativa —")
        print("  como se hizo con SAT-IX en RO-VIII-003.")
        print("\n  NO se reabren los PCD cerrados (Regla 8): la deuda se anexa al PCD.")

    estricto = "--estricto" in sys.argv
    if huerfanas and estricto:
        print("\n  FALLO (--estricto): hay SAT sin cadena BRN.")
        return 1
    print("\n  OK — reporte informativo. Use --estricto en CI cuando la deuda llegue a 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
