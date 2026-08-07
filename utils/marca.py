"""
QUIRA — Acceso a la marca  ·  `utils/marca.py`

Único lugar del código que toca los activos de `assets/marca/`. La geometría de
la Q manteña NUNCA se reconstruye aquí ni en ningún otro módulo: se lee el
archivo y solo se ajusta su tamaño de render.

POR QUÉ ESTA REGLA EXISTE — el error se cometió dos veces:
  1ª · se redibujó la Q con paths propios → no era el logo de Javo.
  2ª · se usó un SVG de conversión automática con solo 2 paths → perdía los
       niveles interiores y se publicó una versión pobre.
Y una tercera cosa casi se publica: la vectorización traía un destello de cuatro
puntas —la firma que las herramientas de IA añaden a sus salidas— que estaba en
todas las variantes y se habría distribuido como parte de la marca.

Si el logo cambia, se cambia el ARCHIVO. Aquí nunca se dibuja.

VARIANTES
  coral      → sobre papel de plano (lo público)
  marfil     → sobre volcánico (el ambiente de trabajo)
  volcanico  → una tinta oscura, para impresión y sellos
  app        → ícono de aplicación con fondo
  favicon    → reducción con menos niveles interiores

Dylus Lab © 2026
"""
from __future__ import annotations

import re
from pathlib import Path

from utils.css_tokens import C

_MARCA = Path(__file__).resolve().parents[1] / "assets" / "marca"

# El logo NO es cuadrado: 150 × 160. Forzarlo a un cuadrado lo deforma, que fue
# otra de las formas en que se estropeó antes.
ASPECTO = 150 / 160

_VARIANTES = ("coral", "marfil", "volcanico", "app", "favicon")


def logo(variante: str = "coral", px: int = 96) -> str:
    """SVG de la marca en la variante y altura pedidas.

    Ante un archivo ausente o ilegible devuelve una Q tipográfica: la portada no
    se cae por un activo, pero tampoco se inventa la geometría."""
    v = variante if variante in _VARIANTES else "coral"
    try:
        svg = (_MARCA / f"quira_{v}.svg").read_text(encoding="utf-8")
        return re.sub(r"<svg ", f'<svg width="{round(px * ASPECTO)}" height="{px}" ',
                      svg, count=1)
    except Exception:  # noqa: BLE001
        color = C.V_TX if v == "marfil" else C.CORAL
        return (f'<div style="font:800 {px // 2}px Archivo,sans-serif;'
                f'color:{color};line-height:1">Q</div>')
