"""
QUIRA OS v0.1 — Tarjetas KPI y métricas
Dylus Lab © 2026
"""
import streamlit as st
from typing import Optional


def kpi_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "#38A169",
    icon: str = "",
    note: str = "",
    color: str = "#00D4FF",
    width_pct: int = 100,
) -> None:
    """
    KPI compacto para métricas principales del dashboard.
    delta_color: "#38A169" (positivo) | "#E53E3E" (negativo)
    """
    delta_html = ""
    if delta:
        delta_html = f'<div style="font-size:11px;color:{delta_color};margin-top:2px;font-weight:600">{delta}</div>'

    note_html = ""
    if note:
        note_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:5px">{note}</div>'

    st.html(f"""<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-top:2px solid {color};border-radius:12px;
                padding:14px 16px;width:{width_pct}%">
        <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.45);
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">
            {icon} {label}
        </div>
        <div style="font-size:1.7rem;font-weight:900;color:#FFFFFF;line-height:1">{value}</div>
        {delta_html}
        {note_html}
    </div>""")


def metric_row(*metrics: dict) -> None:
    """
    Renderiza una fila de KPIs. Cada métrica es un dict con keys:
    label, value, delta?, delta_color?, icon?, note?, color?
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            kpi_card(
                label       = m.get("label", ""),
                value       = m.get("value", "—"),
                delta       = m.get("delta"),
                delta_color = m.get("delta_color", "#38A169"),
                icon        = m.get("icon", ""),
                note        = m.get("note", ""),
                color       = m.get("color", "#00D4FF"),
            )


def progress_bar_card(
    label: str,
    value: Optional[float],
    max_value: float = 100,
    color: str = "#D69E2E",
    avep: str = "",
    emoji: str = "🟡",
    note: str = "",
    dashed: bool = False,
    show_tech: bool = False,
    tech_label: str = "",
) -> None:
    """
    Barra de progreso tipo P-01 Brechas Estructurales.
    dashed=True: barra rayada (índice en calibración).
    """
    pct = min((value or 0) / max_value * 100, 100) if value is not None else 0
    val_str = f"{value:.2f}" if value is not None else "calibrando"

    # Estilo de barra
    if dashed:
        bar_style = (
            "background:repeating-linear-gradient(45deg,"
            "rgba(124,92,252,.18),rgba(124,92,252,.18) 3px,"
            "transparent 3px,transparent 7px);"
            "border:1px dashed rgba(124,92,252,.35);border-radius:4px"
        )
        bar_inner = f'<div style="width:100%;height:100%;{bar_style}"></div>'
    else:
        bar_inner = f'<div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:4px"></div>'

    tech_html = ""
    if show_tech and tech_label:
        tech_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.25);margin-top:1px">↳ {tech_label}</div>'

    note_html = ""
    if note:
        note_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.35);margin-top:4px">{note}</div>'

    st.html(f"""<div style="margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
            <div>
                <span style="font-size:11px;font-weight:600;color:rgba(255,255,255,0.8)">{label}</span>
                {tech_html}
            </div>
            <span style="font-size:13px;font-weight:900;color:{color}">{val_str}</span>
        </div>
        <div style="height:6px;background:rgba(255,255,255,0.07);border-radius:4px;overflow:hidden">
            {bar_inner}
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:3px">
            <div style="font-size:9px;color:rgba(255,255,255,0.3)">{emoji} {avep}</div>
        </div>
        {note_html}
    </div>""")


def section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Encabezado de sección con línea inferior."""
    st.html(f"""<div style="border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:10px;margin-bottom:16px">
        <div style="font-size:1rem;font-weight:800;color:#E2E8F0;letter-spacing:-0.02em">
            {icon} {title}
        </div>
        {'<div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:3px">' + subtitle + '</div>' if subtitle else ''}
    </div>""")


def info_box(text: str, level: str = "info") -> None:
    """
    Caja de información/alerta contextual.
    level: 'info' | 'warning' | 'danger' | 'success'
    """
    colors = {
        "info":    ("#00D4FF", "rgba(0,212,255,0.08)"),
        "warning": ("#FFB700", "rgba(255,183,0,0.08)"),
        "danger":  ("#FF4D6D", "rgba(255,77,109,0.08)"),
        "success": ("#00E096", "rgba(0,224,150,0.08)"),
    }
    border_color, bg_color = colors.get(level, colors["info"])
    st.html(f"""<div style="background:{bg_color};border-left:3px solid {border_color};
                border-radius:0 8px 8px 0;padding:10px 14px;margin:8px 0;
                font-size:12px;color:rgba(255,255,255,0.75);line-height:1.5">
        {text}
    </div>""")
