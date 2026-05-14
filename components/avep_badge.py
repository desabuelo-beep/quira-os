"""
QUIRA OS v0.1 — Badge AVEP
Renderiza la banda canónica H01 en HTML para st.markdown
Dylus Lab © 2026
"""
import streamlit as st
from typing import Optional


def avep_badge_html(
    score: Optional[float],
    avep_label: str,
    emoji: str,
    color: str,
    show_score: bool = True,
    size: str = "md",   # "sm" | "md" | "lg"
) -> str:
    """
    Genera HTML para un badge AVEP inline.
    Usar con st.markdown(..., unsafe_allow_html=True).
    """
    sizes = {
        "sm": ("9px",  "5px 10px",  "10px"),
        "md": ("11px", "6px 14px",  "13px"),
        "lg": ("13px", "8px 18px",  "15px"),
    }
    label_fs, padding, score_fs = sizes.get(size, sizes["md"])

    score_span = ""
    if show_score and score is not None:
        score_span = f'<span style="font-size:{score_fs};font-weight:900;margin-right:5px">{score:.1f}</span>'

    return (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'background:rgba({_hex_to_rgb(color)},0.12);'
        f'border:1px solid rgba({_hex_to_rgb(color)},0.35);'
        f'border-radius:20px;padding:{padding};'
        f'font-size:{label_fs};font-weight:600;color:{color};'
        f'white-space:nowrap">'
        f'{emoji} {score_span}{avep_label}'
        f'</span>'
    )


def render_avep_scale(current_score: Optional[float] = None) -> None:
    """
    Renderiza la escala AVEP completa con el nivel actual resaltado.
    """
    from config import AVEP
    st.markdown("**Escala AVEP — Categorías de Gobernanza**")
    cols = st.columns(5)
    for i, band in enumerate(AVEP):
        with cols[i]:
            active = (
                current_score is not None
                and band["min"] <= current_score / 100 <= band["max"]
            )
            border = f"2px solid {band['color']}" if active else "1px solid rgba(255,255,255,0.08)"
            bg     = f"rgba({_hex_to_rgb(band['color'])},0.15)" if active else "rgba(255,255,255,0.03)"
            st.markdown(f"""
            <div style="background:{bg};border:{border};border-radius:10px;
                        padding:10px 8px;text-align:center">
                <div style="font-size:1.4rem">{band['emoji']}</div>
                <div style="font-size:0.65rem;font-weight:700;color:{band['color']};
                            margin-top:4px;line-height:1.3">{band['label']}</div>
                <div style="font-size:0.6rem;color:rgba(255,255,255,0.4);margin-top:3px">
                    {int(band['min']*100)}–{int(band['max']*100)}%
                </div>
                {'<div style="font-size:0.6rem;color:rgba(255,255,255,0.6);margin-top:4px">◄ ACTUAL</div>' if active else ''}
            </div>
            """, unsafe_allow_html=True)


def render_index_card(
    key: str,
    nombre: str,
    valor: Optional[float],
    avep: str,
    emoji: str,
    color: str,
    estado: str,
    nota: str,
    show_tech: bool = False,
) -> None:
    """Tarjeta compacta para un índice complementario."""
    valor_str = f"{valor:.2f}" if valor is not None else "—"
    tech_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px">↳ {key}</div>' if show_tech else ""

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                border-left:3px solid {color};border-radius:10px;padding:12px 14px;
                margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.85)">
                    {emoji} {nombre}
                </div>
                <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">{estado}</div>
                {tech_html}
            </div>
            <div style="text-align:right">
                <div style="font-size:1.4rem;font-weight:900;color:{color}">{valor_str}</div>
                <div style="font-size:8px;color:{color};opacity:0.8">{avep}</div>
            </div>
        </div>
        <div style="font-size:9px;color:rgba(255,255,255,0.35);margin-top:8px;
                    border-top:1px solid rgba(255,255,255,0.05);padding-top:6px">
            {nota}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── HELPER ────────────────────────────────────────────────────────────────────
def _hex_to_rgb(hex_color: str) -> str:
    """Convierte #RRGGBB a 'R,G,B' para uso en rgba()."""
    h = hex_color.lstrip("#")
    if len(h) == 6:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"{r},{g},{b}"
    return "255,255,255"
