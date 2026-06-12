# -*- coding: utf-8 -*-
"""
audit_bloomberg_l2.py — Auditoría Bloomberg Firewall de los dashboards L2
=========================================================================
Cuenta términos PROHIBIDOS (Regla de Oro 2) dentro de STRINGS LITERALES
de cada página (lo que potencialmente se renderiza en UI) — no cuenta
comentarios ni nombres de variables. Base cuantificada para el plan de
refactorización L2 (mesa 2026-06-12).

Términos: ICPI · TGI · QTMP · H01-H99 · Gold Master · Dom01-Dom12 ·
C01-C99 (node) · CE_xxx · SAT · AVEP · MMP · Ti (omitido: ruido).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

# Páginas ruteadas desde env_gov (el mapa L2 del entorno GOV)
PAGINAS = [
    "p0_inicio", "m1_situacion", "m2_alertas", "m3_municipal", "m4_analisis",
    "m5_control", "p3_congruencias", "p4_geotwin", "p8_metas", "p07_transparencia",
    "p10_territorio", "p11_ods", "p13_simulador", "p16_confianza", "p17_rdc",
    "p18_cooperacion", "p19_genero", "p_vista_ejecutiva",
]

PATRONES = {
    "ICPI":        re.compile(r"\bICPI\b"),
    "TGI":         re.compile(r"\bTGI\b"),
    "QTMP":        re.compile(r"\bQTMP\b"),
    "H01-H99":     re.compile(r"\bH\d{2}\b"),
    "Gold Master": re.compile(r"Gold ?Master", re.I),
    "DomNN":       re.compile(r"\bDom\d{2}\b"),
    "CE_xxx":      re.compile(r"\bCE_\d+\b"),
    "SAT":         re.compile(r"\bSAT\b"),
    "AVEP":        re.compile(r"\bAVEP\b"),
    "MMP":         re.compile(r"\bMMP\b"),
    "node C01":    re.compile(r"\bC0\d\b"),
}


def strings_de(archivo: Path) -> list[str]:
    """Todas las constantes string del AST (lo renderizable)."""
    try:
        tree = ast.parse(archivo.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"__PARSE_ERROR__ {e}"]
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append(node.value)
    return out


def main() -> None:
    print(f"{'PÁGINA':<22} {'TOTAL':>6}  detalle")
    print("─" * 78)
    resultados = []
    for pag in PAGINAS:
        f = ROOT / "quira_pages" / f"{pag}.py"
        if not f.exists():
            print(f"{pag:<22} {'—':>6}  (no existe)")
            continue
        textos = strings_de(f)
        if textos and textos[0].startswith("__PARSE_ERROR__"):
            print(f"{pag:<22} {'ERR':>6}  {textos[0][:50]}")
            continue
        blob = "\n".join(textos)
        conteo = {k: len(p.findall(blob)) for k, p in PATRONES.items()}
        total = sum(conteo.values())
        detalle = " · ".join(f"{k}:{v}" for k, v in conteo.items() if v)
        resultados.append((total, pag, detalle, len(f.read_text(encoding='utf-8').splitlines())))
        print(f"{pag:<22} {total:>6}  {detalle[:50]}")

    print("─" * 78)
    print("\nRANKING DE SEVERIDAD (violaciones en strings renderizables):")
    for total, pag, detalle, lineas in sorted(resultados, reverse=True):
        sev = "🔴" if total >= 30 else ("🟠" if total >= 10 else ("🟡" if total > 0 else "🟢"))
        print(f"  {sev} {pag:<22} {total:>4} violaciones · {lineas} líneas")
    limpio = [p for t, p, _, _ in resultados if t == 0]
    print(f"\n  LIMPIOS: {', '.join(limpio) if limpio else 'ninguno'}")


if __name__ == "__main__":
    main()
