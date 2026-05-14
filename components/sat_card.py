"""
QUIRA OS v0.1 — Tarjetas SAT (Sistema de Alertas Tempranas)
Dylus Lab © 2026
"""
import streamlit as st


def sat_card(
    sat_id: str,
    nombre: str,
    estado: str,
    nivel: str,
    color: str,
    emoji: str,
    descripcion: str,
    impacto: str,
    accion: str,
    compact: bool = False,
) -> None:
    """
    Tarjeta SAT completa.
    compact=True: versión feed para sidebar o resumen.
    """
    if compact:
        _sat_compact(sat_id, nombre, nivel, color, emoji, impacto)
    else:
        _sat_full(sat_id, nombre, estado, nivel, color, emoji, descripcion, impacto, accion)


def _sat_full(
    sat_id, nombre, estado, nivel, color, emoji, descripcion, impacto, accion
) -> None:
    estado_badge = (
        f'<span style="background:rgba({_rgb(color)},0.15);border:1px solid rgba({_rgb(color)},0.3);'
        f'border-radius:20px;padding:2px 10px;font-size:9px;font-weight:700;color:{color}">'
        f'{estado}</span>'
    )
    st.html(f"""<div style="background:rgba(255,255,255,0.03);
                border:1px solid rgba({_rgb(color)},0.25);
                border-left:4px solid {color};
                border-radius:12px;padding:16px 18px;margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
            <div style="display:flex;align-items:center;gap:8px">
                <span style="font-size:1.2rem">{emoji}</span>
                <div>
                    <div style="font-size:13px;font-weight:800;color:#E2E8F0">{nombre}</div>
                    <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.4);
                                letter-spacing:0.05em;margin-top:1px">{sat_id} · {nivel}</div>
                </div>
            </div>
            {estado_badge}
        </div>
        <div style="font-size:11px;color:rgba(255,255,255,0.65);margin-bottom:10px;line-height:1.5">
            {descripcion}
        </div>
        <div style="background:rgba({_rgb(color)},0.07);border-radius:8px;padding:10px 12px;margin-bottom:10px">
            <div style="font-size:9px;font-weight:700;color:{color};letter-spacing:0.06em;margin-bottom:4px">
                IMPACTO CUANTIFICADO
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.75)">{impacto}</div>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.06);padding-top:10px">
            <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.4);
                        letter-spacing:0.06em;margin-bottom:4px">ACCIÓN RECOMENDADA</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.65)">→ {accion}</div>
        </div>
    </div>""")


def _sat_compact(sat_id, nombre, nivel, color, emoji, impacto) -> None:
    st.html(f"""<div style="background:rgba({_rgb(color)},0.06);
                border-left:3px solid {color};
                border-radius:0 8px 8px 0;
                padding:8px 12px;margin-bottom:6px">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-size:11px;font-weight:700;color:#E2E8F0">{emoji} {nombre}</div>
            <div style="font-size:9px;color:{color};font-weight:600">{nivel}</div>
        </div>
        <div style="font-size:9px;color:rgba(255,255,255,0.45);margin-top:3px">{impacto}</div>
    </div>""")


def sat_feed_header(n_criticos: int, n_alertas: int) -> None:
    """Header del feed SAT con contadores."""
    total = n_criticos + n_alertas
    if n_criticos > 0:
        color_header = "#E53E3E"
        emoji_header = "🔴"
    elif n_alertas > 0:
        color_header = "#E67E22"
        emoji_header = "🟠"
    else:
        color_header = "#38A169"
        emoji_header = "🟢"

    st.html(f"""<div style="background:rgba({_rgb(color_header)},0.08);
                border:1px solid rgba({_rgb(color_header)},0.25);
                border-radius:10px;padding:10px 14px;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;align-items:center">
            <div style="font-size:12px;font-weight:800;color:{color_header}">
                {emoji_header} ALERTAS SAT ACTIVAS
            </div>
            <div style="display:flex;gap:8px">
                <span style="font-size:9px;background:rgba(229,62,62,0.2);
                             border-radius:20px;padding:2px 8px;color:#FC8181;font-weight:700">
                    🔴 {n_criticos} Crítico{'s' if n_criticos != 1 else ''}
                </span>
                <span style="font-size:9px;background:rgba(230,126,34,0.2);
                             border-radius:20px;padding:2px 8px;color:#F6AD55;font-weight:700">
                    🟠 {n_alertas} Alerta{'s' if n_alertas != 1 else ''}
                </span>
            </div>
        </div>
    </div>""")


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,255,255"
