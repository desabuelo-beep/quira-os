# -*- coding: utf-8 -*-
"""
Sintetizador de Hallazgos COMPARTIDO — QUIRA (Javo + asesor · 2026-07-11).
Un solo idioma para TODOS los DOM: mismo tipo de hallazgo, mismas primitivas, mismo render.

NO es un 6º motor (ADR-031 · anti-inflación Regla 7): es la utilidad de SÍNTESIS que consume la
salida de los motores tipados —Matemático (números del Gold Master) · Prospectivo (proyección) ·
Descubrimiento (patrones, promovidos al canon)—. Cada DOM COMPONE sus hallazgos con estas primitivas
y los renderiza aquí; jamás inventa formato propio. Así Planificación, RDC, IFE, etc. hablan igual.
"""
from __future__ import annotations

import html as _h

# gramática de color del hallazgo (eje semántico · consistente entre DOM)
_TAG = {"up": "#1E8E3E", "down": "#D93025", "warn": "#F9AB00", "info": "#1A73E8", "prosp": "#8B7BD8"}


def _esc(s) -> str:
    return _h.escape(str(s or ""))


# ── tipo estándar de hallazgo: (tag, título, detalle) · tag ∈ up|down|warn|info|prosp ──
def hallazgo(tag: str, titulo: str, detalle: str) -> tuple:
    return (tag, titulo, detalle)


# ── primitivas reutilizables (el "idioma" común) ──
def h_tendencia(titulo: str, y0, v0: float, y1, v1: float, sube_es_bueno: bool = True, u: str = "%") -> tuple:
    """Hallazgo de TENDENCIA entre dos períodos. El DOM decide si subir es bueno."""
    d = round((v1 or 0) - (v0 or 0))
    if d == 0:
        return ("info", titulo, f"Se mantiene estable en {round(v1 or 0)}{u} entre {y0} y {y1}: sin variación en el período.")
    sube = d > 0
    tag = "up" if (sube == sube_es_bueno) else "warn"
    verbo = "asciende" if sube else "desciende"
    return (tag, titulo, f"{verbo} del {round(v0)}{u} ({y0}) al {round(v1)}{u} ({y1}) —{abs(d)} puntos porcentuales—.")


def h_serie(titulo: str, puntos: list, u: str = "%") -> tuple:
    """Hallazgo NARRATIVO de una serie temporal (Etapa 2 del asesor · describe COMPORTAMIENTO, no valores).
    `puntos` = [(etiqueta, valor), …] ordenados. Devuelve 'ciclo de expansión → caída → estabilización'."""
    pts = [(l, v) for l, v in (puntos or []) if v is not None]
    if len(pts) < 2:
        return ("info", titulo, "Serie insuficiente para describir el comportamiento.")
    nombre = {"exp": "expansión", "cae": "contracción", "est": "estabilidad"}
    tramos = []
    for i in range(1, len(pts)):
        d = pts[i][1] - pts[i - 1][1]
        k = "exp" if d > 3 else ("cae" if d < -3 else "est")
        tramos.append((k, pts[i][0], d))
    # comprime tramos consecutivos del mismo tipo
    frases, i = [], 0
    while i < len(tramos):
        k = tramos[i][0]
        j = i
        while j + 1 < len(tramos) and tramos[j + 1][0] == k:
            j += 1
        frases.append(f"{nombre[k]} hasta {tramos[j][1]}")
        i = j + 1
    ult = tramos[-1][0]
    tag = {"exp": "up", "cae": "warn", "est": "info"}[ult]
    v0, vN, y0, yN = pts[0][1], pts[-1][1], pts[0][0], pts[-1][0]
    return (tag, titulo, f"La serie describe un ciclo de {', luego '.join(frases)} "
                         f"(de {round(v0)}{u} en {y0} a {round(vN)}{u} en {yN}).")


def h_proyeccion(titulo: str, valor_proy: float, ancla: str = "", u: str = "%") -> tuple:
    """Hallazgo PROSPECTIVO (motor Prospectivo · lee la proyección del Gold Master, p.ej. H12c)."""
    det = f"La proyección del canon sitúa el próximo ejercicio en torno al {round(valor_proy)}{u}"
    det += f" ({ancla})." if ancla else "."
    return ("prosp", titulo, det + " No es un pronóstico: es la tendencia proyectada sobre la serie verificada.")


# ── render ÚNICO (mismo formato de hallazgos en todos los DOM) ──
def render_hallazgos(hallazgos: list) -> str:
    if not hallazgos:
        return ""
    rows = ""
    for i, (tag, tit, det) in enumerate(hallazgos, 1):
        c = _TAG.get(tag, "#1A73E8")
        rows += (f'<div class="qc-hz" style="border-left-color:{c}"><div class="hz-n" style="color:{c};border-color:{c}">{i:02d}</div>'
                 f'<div class="hz-b"><div class="hz-t">{_esc(tit)}</div><div class="hz-d">{_esc(det)}</div></div></div>')
    return f'<div class="qc-hzs">{rows}</div>'
