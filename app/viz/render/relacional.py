# -*- coding: utf-8 -*-
"""
Motor Relacional — cadena de integridad intersistémica (Javo · 2026-07-11).

"Encender el Relacional": la cadena del cajón deja de ser decorativa y se vuelve un RECORRIDO con
estado REAL de integración entre las FUENTES —donde vive la verdad (ADR-029 §Precisión epistemológica)—.

  · Nodos  = sistemas fuente (PDOT · POA · Presupuesto · PAC · SERCOP · Rendición…).
  · Aristas = la integración que QUIRA VERIFICÓ entre una fuente y la siguiente.
  · Un eslabón delgado = una fuente que aún no sostiene documentalmente a la siguiente
    (nunca una acusación · Constitución CAPA 0). La ausencia es un RESULTADO, no una inferencia.

Compartido: RDC, Planificación, IFE… renderizan su cadena aquí y hablan el mismo idioma.
Regla 1: el estado de cada arista se LEE del snapshot (motor→snapshot→render), no se consulta en vivo.
"""
from __future__ import annotations

import html as _h

# estado de la arista = gramática semántica (consistente con hallazgos/evidencia)
_EDGE = {
    "verificado": ("#1E8E3E", "sostiene"),
    "parcial":    ("#F9AB00", "sostiene en parte"),
    "roto":       ("#D93025", "no sostiene"),
    "pendiente":  ("#9AA0A6", "sin evidencia aún"),
}

REL_CSS = """
.rl-hd{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--tx2);margin:14px 0 9px}
.rl-chain{display:flex;align-items:stretch;flex-wrap:nowrap;overflow-x:auto;gap:0;padding-bottom:6px}
.rl-n{flex:0 0 auto;min-width:94px;border:1px solid var(--bd);border-radius:7px;padding:9px 10px;background:var(--sf);text-align:center}
.rl-sys{font-family:ui-monospace,monospace;font-size:10.5px;font-weight:700;color:var(--tx);letter-spacing:.04em}
.rl-lb{font-size:9px;color:var(--tx2);margin-top:3px;line-height:1.2}
.rl-e{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;min-width:54px;padding:0 5px}
.rl-line{width:100%;height:2px;border-radius:2px;opacity:.85}
.rl-arw{font-size:13px;line-height:1;margin-top:2px}
.rl-pct{font-family:ui-monospace,monospace;font-size:10px;font-weight:700;margin-top:1px}
.rl-lg{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px;font-size:9.5px;color:var(--tx2)}
.rl-lg span{display:inline-flex;align-items:center;gap:5px}
.rl-lg i{width:9px;height:9px;border-radius:2px;display:inline-block}
"""


def _esc(s) -> str:
    return _h.escape(str(s or ""))


def cadena_integridad(nodos: list, titulo: str = "", leyenda: bool = True) -> str:
    """nodos = [{"sys","label","edge"?}]. La arista de cada nodo apunta al SIGUIENTE:
    edge = {"estado": verificado|parcial|roto|pendiente, "pct"?: n, "nota"?: str}."""
    nodos = [n for n in (nodos or []) if n]
    if len(nodos) < 2:
        return ""
    usados = set()
    seg = ""
    for i, n in enumerate(nodos):
        seg += (f'<div class="rl-n"><div class="rl-sys">{_esc(n.get("sys"))}</div>'
                f'<div class="rl-lb">{_esc(n.get("label", ""))}</div></div>')
        e = n.get("edge")
        if e and i < len(nodos) - 1:
            est = e.get("estado", "pendiente")
            col, _v = _EDGE.get(est, _EDGE["pendiente"])
            usados.add(est)
            pct = e.get("pct")
            val = f'<span class="rl-pct" style="color:{col}">{round(pct)}%</span>' if pct is not None else ""
            seg += (f'<div class="rl-e" title="{_esc(e.get("nota", ""))}">'
                    f'<div class="rl-line" style="background:{col}"></div>'
                    f'<div class="rl-arw" style="color:{col}">&#9656;</div>{val}</div>')
    lg = ""
    if leyenda and usados:
        items = "".join(f'<span><i style="background:{_EDGE[k][0]}"></i>{_esc(_EDGE[k][1])}</span>'
                        for k in ("verificado", "parcial", "roto", "pendiente") if k in usados)
        lg = f'<div class="rl-lg">{items}</div>'
    hd = f'<div class="rl-hd">{_esc(titulo)}</div>' if titulo else ""
    return f'{hd}<div class="rl-chain">{seg}</div>{lg}'
