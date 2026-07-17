# -*- coding: utf-8 -*-
"""
p_gobierno — la dimensión ¿QUÉ? del frame (ADR-037 · Javo 2026-07-16).

La institución y su mandato: quién gobierna, desde cuándo, hasta cuándo, con qué concejo y
bajo qué estructura. Es PÁGINA PROPIA —como Territorio e Inteligencia—, no un panel dentro
del Centro de Mando: el interior conserva el marco, el contenido es suyo.

TODO viene del canon y del corpus verificado vía `scripts/enrich_gobierno.py`; aquí solo se
lee (Regla 1). No se publican nombres de directores: las personas cambian, el orgánico
permanece — QUIRA observa estructuras, no personas (Javo + colega · 2026-07-16).
Dylus Lab © 2026
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

_MONO = "font-family:'JetBrains Mono',monospace"
_SNAP = Path(__file__).resolve().parent.parent / "data" / "gm_snapshot.json"


def _esc(s) -> str:
    return str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _cargar() -> dict:
    try:
        return (json.loads(_SNAP.read_text(encoding="utf-8")) or {}).get("gobierno") or {}
    except Exception:  # noqa: BLE001
        return {}


def _mandato(a: dict, m: dict) -> str:
    """El mandato y su cuenta regresiva. Las fechas salen del canon; sin ellas, no hay contador."""
    if not m.get("disponible"):
        return (f'<div style="font-size:12px;color:#7E8BA3">'
                f'{_esc(a.get("nombre"))} · {_esc(a.get("movimiento"))}</div>')
    rest = m.get("dias_restantes", 0)
    col = "#EF5350" if rest < 180 else ("#F9AB00" if rest < 365 else "#22C55E")
    tiles = "".join(
        f'<div style="flex:1 1 150px">'
        f'<div style="{_MONO};font-size:7.5px;font-weight:800;letter-spacing:.12em;'
        f'color:#5A6B7E">{k}</div>'
        f'<div style="{_MONO};font-size:30px;font-weight:200;color:{c};line-height:1.15">{v}</div>'
        f'<div style="font-size:9px;font-weight:300;color:#7E8BA3">{u}</div></div>'
        for k, v, u, c in (
            ("EN EL CARGO", f"{m['dias_transcurridos']:,}", "días transcurridos", "#00F0FF"),
            ("RESTAN", f"{rest:,}", "días de mandato", col),
            ("AVANCE", f"{m['avance_pct']:.0f}%", "del período", "#E0F7FA")))
    return (
        f'<div style="font-size:15px;font-weight:600;color:#E0F7FA">{_esc(a.get("nombre"))}</div>'
        f'<div style="font-size:10.5px;font-weight:300;color:#7E8BA3;margin:2px 0 16px">'
        f'{_esc(a.get("movimiento"))} · posesión {_esc(m["inicio"])} — hasta {_esc(m["fin"])}</div>'
        f'<div style="display:flex;gap:26px;flex-wrap:wrap;margin-bottom:14px">{tiles}</div>'
        f'<div style="height:3px;border-radius:2px;background:rgba(255,255,255,.06);overflow:hidden">'
        f'<span style="display:block;height:100%;width:{min(m["avance_pct"],100):.0f}%;'
        f'background:linear-gradient(90deg,#00F0FF,{col});border-radius:2px"></span></div>')


def _titulo(t: str, n: int | None = None) -> str:
    extra = (f'<span style="font-weight:300;color:#5A6B7E;margin-left:9px">{n}</span>'
             if n is not None else "")
    return (f'<div style="{_MONO};font-size:8px;font-weight:800;letter-spacing:.12em;'
            f'color:#00F0FF;margin:26px 0 10px;opacity:.85">{t}{extra}</div>')


def _flujo(gente: list) -> str:
    """Líneas de flujo (Javo): sin grillas ni filas rayadas — acento vertical, aire y contraste polar."""
    return '<div style="display:flex;flex-wrap:wrap;gap:9px">' + "".join(
        f'<div style="flex:1 1 236px;padding:8px 13px;border-left:2px solid rgba(0,240,255,.30);'
        f'background:linear-gradient(90deg,rgba(0,240,255,.05),transparent 82%);'
        f'border-radius:0 6px 6px 0">'
        f'<div style="font-size:11.5px;color:#E0F7FA;font-weight:500;line-height:1.3">'
        f'{_esc(x.get("nombre"))}</div>'
        f'<div style="{_MONO};font-size:8.5px;font-weight:300;color:#7E8BA3;'
        f'letter-spacing:.04em;margin-top:2px">{_esc(x.get("cargo"))}</div></div>'
        for x in gente) + '</div>'


def render() -> None:
    """Gobierno · ¿QUÉ? — la institución y su mandato."""
    g = _cargar()
    if not g:
        st.markdown('<div style="font-size:14px;color:#7E8BA3;padding:22px 0">'
                    '— evidencia institucional pendiente de carga —</div>', unsafe_allow_html=True)
        return
    a, m = g.get("alcalde") or {}, g.get("mandato") or {}

    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;'
        f'margin-bottom:18px;padding-bottom:11px;border-bottom:1px solid rgba(0,240,255,.14)">'
        f'<div><div style="font-size:19px;font-weight:700;color:#E8EDF4">El mandato en curso</div>'
        f'<div style="font-size:10px;font-weight:300;color:#7E8BA3;margin-top:2px">'
        f'La institución, su período y la estructura con que gobierna</div></div>'
        f'<span style="{_MONO};font-size:9px;color:#5A6B7E">GOBIERNO · ¿QUÉ?</span></div>'
        + _mandato(a, m), unsafe_allow_html=True)

    conc = (g.get("concejo") or {}).get("detalle") or []
    plan = (g.get("consejo_planificacion") or {}).get("detalle") or []
    if conc:
        st.markdown(_titulo("CONCEJO CANTONAL", len(conc)) + _flujo(conc), unsafe_allow_html=True)
    if plan:
        st.markdown(_titulo("CONSEJO CANTONAL DE PLANIFICACIÓN", len(plan)) + _flujo(plan),
                    unsafe_allow_html=True)

    org = g.get("organico") or {}
    niveles = org.get("niveles") or {}
    if niveles:
        cols = "".join(
            f'<div style="flex:1 1 214px;min-width:192px">'
            f'<div style="{_MONO};font-size:7.5px;font-weight:800;letter-spacing:.12em;'
            f'color:#00F0FF;opacity:.8;padding-bottom:7px;margin-bottom:9px;'
            f'border-bottom:1px solid rgba(0,240,255,.16);min-height:26px">{_esc(niv).upper()}</div>'
            + "".join(
                f'<div style="font-size:9.5px;font-weight:300;color:#A8B4C8;padding:4px 0 4px 10px;'
                f'margin-bottom:2px;border-left:1px solid rgba(224,247,250,.14);line-height:1.35">'
                f'{_esc(u)}</div>' for u in unidades)
            + '</div>' for niv, unidades in niveles.items())
        st.markdown(
            _titulo("ESTRUCTURA ORGÁNICA VIGENTE", org.get("n_unidades", 0))
            + f'<div style="display:flex;gap:22px;flex-wrap:wrap">{cols}</div>'
            f'<div style="font-size:8.5px;font-weight:300;color:#5A6B7E;margin-top:16px;'
            f'padding-top:10px;border-top:1px solid rgba(255,255,255,.05)">'
            f'{_esc(org.get("norma"))} — se publica la <span style="color:#7E8BA3">estructura</span>, '
            f'no la plantilla: las personas cambian, el orgánico permanece.</div>',
            unsafe_allow_html=True)
