# -*- coding: utf-8 -*-
"""
Proveniencia epistemológica VISIBLE — QUIRA (ADR-033 · Javo · 2026-07-13).

Cada bloque del cajón declara su CAPA, para que el usuario distinga de un vistazo qué mira:
  🟢 documental     — hecho reconstruido de la fuente oficial.
  🔵 analítico      — índice REPRODUCIBLE calculado sobre la evidencia (Gold Master · etiqueta pública, sin código).
  🟣 interpretación — lectura del observatorio sobre la evidencia y los índices.

Autoridad DECRECIENTE: documental > analítico > interpretación. La analítica hereda la confianza de la evidencia
sobre la que se calcula. Compartido: todos los DOM etiquetan igual. (QUIRA IA conversacional = otra capa, aparte.)
"""
from __future__ import annotations

# (color, etiqueta pública, descripción) — NO exponer códigos canónicos (Firewall)
_PROV = {
    "doc": ("#2DD46F", "documental", "hecho reconstruido de la fuente oficial"),
    "ana": ("#5AA9E6", "analítico", "índice reproducible calculado sobre la evidencia"),
    "int": ("#A78BFA", "interpretación", "lectura del observatorio sobre evidencia e índices"),
}

PROV_CSS = """
.qc-prov{display:inline-flex;align-items:center;gap:5px;font-family:ui-monospace,monospace;font-size:8.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:2px 8px;border-radius:11px;border:1px solid;white-space:nowrap;vertical-align:middle;margin-left:2px}
.qc-prov i{width:7px;height:7px;border-radius:50%;display:inline-block;flex:none}
.qc-provl{display:flex;flex-wrap:wrap;gap:9px 18px;align-items:center;margin:4px 0 18px;padding:12px 16px;border:1px solid var(--bd);border-radius:10px;background:var(--sf)}
.qc-provl-t{width:100%;font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--tx2)}
.qc-provl-i{display:flex;align-items:center;gap:8px;font-size:11.5px;color:var(--tx2)}
"""


def prov(tipo: str) -> str:
    """Badge de proveniencia para el header de una sección (o cualquier bloque)."""
    c, lbl, _ = _PROV.get(tipo, _PROV["doc"])
    return (f'<span class="qc-prov" style="color:{c};border-color:{c}55;background:{c}14">'
            f'<i style="background:{c}"></i>{lbl}</span>')


def prov_leyenda() -> str:
    """Leyenda: cómo leer el dominio en sus tres niveles de verdad."""
    filas = "".join(
        f'<div class="qc-provl-i"><span class="qc-prov" style="color:{c};border-color:{c}55;background:{c}14">'
        f'<i style="background:{c}"></i>{lbl}</span><span>{desc}</span></div>'
        for c, lbl, desc in _PROV.values())
    return ('<div class="qc-provl"><div class="qc-provl-t">Cómo leer este dominio · tres niveles de verdad '
            f'(autoridad decreciente)</div>{filas}</div>')
