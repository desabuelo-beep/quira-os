# -*- coding: utf-8 -*-
"""
scripts/gm_omega/matriz_procedencia_icpi.py — GM-Ω-ICPI-004/005

Genera la matriz de procedencia 25 × 6 del ICPI: para cada meta y cada variable,
de qué celda sale, con qué fórmula, de qué período y en qué estado de
trazabilidad queda.

POR QUÉ SE DERIVA Y NO SE ESCRIBE. El colega exigió la trazabilidad celda a
celda —«poder contestar, para cualquier meta, por qué tiene exactamente ese
número»— y la primera pasada comprimió las 150 celdas en 6 patrones. Comprimir
era legítimo mientras el patrón fuera idéntico, pero deja sin respuesta la
pregunta concreta.

Y escribirla a mano habría reproducido el defecto que esta misma auditoría
persigue: una tabla copiada del Excel se queda atrás el día que el Excel cambia
—el patrón del «48,33 %»—. Este script la vuelve a derivar cada vez.

    LECTURA PURA. No escribe en el Gold Master. Regla de Oro 1 y 4:
    el Excel es el estado, aquí sólo se le pregunta.

Uso:  python scripts/gm_omega/matriz_procedencia_icpi.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_MATRIZ_004.md"

# Columnas del motor, con el nombre que la TESIS les da (no el del Excel: el
# nombre canónico es el del constructo, y GM-Ω-ICPI-001 lo reconstruyó).
_VARIABLES = {
    2: ("P_i", "Coeficiente de Peso Presupuestario"),
    3: ("R_i", "Coeficiente de Relevancia Normativa"),
    4: ("V_i", "Inmutabilidad Documental"),
    5: ("E_i", "Coeficiente de Fricción de Autonomía"),
    6: ("T_i", "Materialización Temporal"),
    9: ("C_i", "Trazabilidad Orgánica"),
}

# Clasificación provisional acordada con el colega (2026-09-03). NO son
# veredictos: son estados de la auditoría mientras GM-Ω-ICPI-011 no dictamine.
_ESTADO = {
    "P_i": ("provenance provisionally verified", "referencia directa a H14!G"),
    "R_i": ("provenance provisionally verified", "fórmula + norma citada por meta"),
    "V_i": ("TEMPORAL SEMANTIC GAP", "la columna leída se llama `Vi_2025`"),
    "E_i": ("UNTRACEABLE · provenance gap", "literal sin fórmula ni fuente en el libro"),
    "T_i": ("provenance verified · sensitivity pending", "ratio por ENTIDAD ejecutora"),
    "C_i": ("provenance provisionally verified", "VLOOKUP a TBL_CALIBRACION_Ci"),
}

# Qué entidad ejecutora representa cada columna de `Ti_norm_2026` (H07b fila 20).
_ENTIDAD_TI = {"B": "ENTE-01 GAD central", "C": "ENTE-02 Patronato",
               "D": "ENTE-03 Bomberos", "E": "ENTE-04 EP Aseo"}


def _entidad_de(formula: str) -> str:
    """De `=H07b_Ti_INVERSIÓN_eSIGEF!B20` a la entidad que ese ratio mide."""
    m = re.search(r"!([A-Z]+)\d+", str(formula))
    return _ENTIDAD_TI.get(m.group(1), "—") if m else "—"


def construir() -> list[dict]:
    import openpyxl

    import config
    if not getattr(config, "GOLD_MASTER_RESUELTO", False):
        return []

    # Dos lecturas del mismo libro: fórmulas y valores. Sin ellas no se puede
    # responder a la vez «de dónde sale» y «cuánto vale».
    wf = openpyxl.load_workbook(config.SIAP_PATH, data_only=False, read_only=True)
    wv = openpyxl.load_workbook(config.SIAP_PATH, data_only=True, read_only=True)
    hf, hv = wf["H12_MOTOR_ICPI_CANÓNICO"], wv["H12_MOTOR_ICPI_CANÓNICO"]

    filas = []
    for r in range(6, 31):                       # las 25 metas del motor
        meta = hv.cell(row=r, column=1).value
        for col, (var, nombre) in _VARIABLES.items():
            formula = hf.cell(row=r, column=col).value
            valor = hv.cell(row=r, column=col).value
            es_literal = not (isinstance(formula, str) and formula.startswith("="))
            estado, por_que = _ESTADO[var]
            filas.append({
                "meta": str(meta), "var": var, "nombre": nombre,
                "celda": f"H12!{hf.cell(row=r, column=col).coordinate}",
                "valor": valor,
                "origen": "LITERAL (sin origen declarado)" if es_literal else str(formula),
                "entidad": _entidad_de(formula) if var == "T_i" else "—",
                "estado": estado, "por_que": por_que,
            })
    wf.close(); wv.close()
    return filas


def main() -> int:
    filas = construir()
    if not filas:
        print("[no determinable] Gold Master no resuelto — no se genera la matriz.")
        return 2                                  # ni verde ni rojo: no pude mirar

    metas = sorted({f["meta"] for f in filas})
    print(f"matriz de procedencia: {len(filas)} celdas · {len(metas)} metas × "
          f"{len(_VARIABLES)} variables")

    out = ["# GM-Ω · ICPI — MATRIZ DE PROCEDENCIA  `004/005`", "",
           "**DERIVADO — no editar a mano.** Lo regenera "
           "`scripts/gm_omega/matriz_procedencia_icpi.py` leyendo el Gold Master "
           "vigente. Escribirlo a mano lo dejaría atrás el día que el Excel "
           "cambie, que es el patrón que esta auditoría persigue.", "",
           f"`{len(filas)}` celdas · {len(metas)} metas × {len(_VARIABLES)} variables · "
           "baseline congelado **27,4582 %** (regla GM-Ω-ICPI-000)", "",
           "## Estado de trazabilidad por variable", "",
           "| Var | Constructo (tesis) | Estado provisional | Por qué |",
           "|---|---|---|---|"]
    for var, nombre in [(v, n) for v, n in _VARIABLES.values()]:
        estado, por_que = _ESTADO[var]
        out.append(f"| `{var}` | {nombre} | **{estado}** | {por_que} |")

    out += ["", "⚠️ Estos NO son veredictos: son estados de la auditoría mientras "
            "`GM-Ω-ICPI-011` no dictamine.", "", "## Las 150 celdas", ""]
    for meta in metas:
        out += [f"### `{meta}`", "",
                "| Var | Celda | Valor | Origen | Entidad |", "|---|---|---|---|---|"]
        for f in [x for x in filas if x["meta"] == meta]:
            v = f["valor"]
            v = f"{v:.6f}" if isinstance(v, float) else str(v)
            out.append(f"| `{f['var']}` | `{f['celda']}` | {v} | "
                       f"`{f['origen'][:72]}` | {f['entidad']} |")
        out.append("")

    _SALIDA.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")

    literales = [f for f in filas if f["origen"].startswith("LITERAL")]
    print(f"celdas sin origen declarado: {len(literales)} "
          f"({', '.join(sorted({f['var'] for f in literales}))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
