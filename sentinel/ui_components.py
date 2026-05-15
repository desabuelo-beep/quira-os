"""
SENTINEL · ui_components.py
5 componentes de UI generativa — Sentinel v2 / Opción C.
Contexto accionable post-chart: Alert · Nav · Evidence · KPI Mini · Scenario.
Doctrina: Sentinel genera intención → Streamlit renderiza experiencia institucional.
Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st

# ── PALETTE AVEP ───────────────────────────────────────────────────────────────
_SEV = {
    "critical": ("#E53E3E", "rgba(229,62,62,0.12)",  "rgba(229,62,62,0.35)",  "🚨"),
    "high":     ("#E67E22", "rgba(230,126,34,0.10)",  "rgba(230,126,34,0.30)",  "⚠️"),
    "medium":   ("#D69E2E", "rgba(214,158,46,0.08)",  "rgba(214,158,46,0.25)",  "⚡"),
    "info":     ("#00D4FF", "rgba(0,212,255,0.06)",   "rgba(0,212,255,0.20)",   "ℹ️"),
    "success":  ("#38A169", "rgba(56,161,105,0.08)",  "rgba(56,161,105,0.25)",  "✅"),
}

_CARD_BASE = (
    "border-radius:10px;padding:12px 16px;margin:8px 0 4px;"
    "font-family:'Inter',-apple-system,sans-serif;"
)


# ── 1. ALERT CARD ─────────────────────────────────────────────────────────────

def alert_card(
    severity: str,
    title:    str,
    message:  str,
    metric:   str = "",
    legal:    str = "",
) -> None:
    """
    Tarjeta de alerta contextual con severidad AVEP.
    severity: critical | high | medium | info | success
    """
    color, bg, border, emoji = _SEV.get(severity, _SEV["info"])
    metric_html = (
        f'<div style="font-size:11px;color:{color};font-weight:700;margin-top:6px">'
        f'{metric}</div>'
    ) if metric else ""
    legal_html = (
        f'<div style="font-size:9px;color:rgba(255,255,255,0.28);margin-top:4px">'
        f'⚖ {legal}</div>'
    ) if legal else ""

    st.markdown(f"""
<div style="{_CARD_BASE}background:{bg};border:1px solid {border};
            border-left:4px solid {color}">
    <div style="font-size:10px;font-weight:700;color:{color};letter-spacing:0.07em;
                text-transform:uppercase">{emoji}&nbsp;{title}</div>
    <div style="font-size:12px;color:#E2E8F0;margin-top:5px;line-height:1.5">
        {message}</div>
    {metric_html}{legal_html}
</div>""", unsafe_allow_html=True)


# ── 2. NAVIGATION CARD ────────────────────────────────────────────────────────

def nav_card(
    title:   str,
    buttons: list[dict],   # [{"label": str, "page_key": str, "icon": str}]
    query_hash: int = 0,
) -> None:
    """
    Tarjeta de acciones con botones de navegación a otras pantallas QUIRA.
    Cada botón setea session_state['page'] y hace rerun.
    """
    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(0,212,255,0.04);
            border:1px solid rgba(0,212,255,0.15)">
    <div style="font-size:10px;font-weight:700;color:rgba(0,212,255,0.7);
                letter-spacing:0.07em;text-transform:uppercase;margin-bottom:8px">
        🔗&nbsp;{title}</div>""", unsafe_allow_html=True)

    cols = st.columns(len(buttons))
    for i, btn in enumerate(buttons):
        with cols[i]:
            key = f"nav_sentinel_{btn['page_key']}_{query_hash}_{i}"
            if st.button(
                f"{btn.get('icon','👉')} {btn['label']}",
                key=key,
                use_container_width=True,
            ):
                st.session_state["page"] = btn["page_key"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ── 3. EVIDENCE CARD ──────────────────────────────────────────────────────────

def evidence_card(
    sources:    list[str],
    confidence: str = "Alta",
    cut:        str = "Q1-2026 · marzo 2026",
    note:       str = "",
) -> None:
    """
    Tarjeta de trazabilidad — responde '¿de dónde salió esto?'
    confidence: Alta | Media | Baja
    """
    conf_color = {
        "Alta":  "#38A169",
        "Media": "#D69E2E",
        "Baja":  "#E53E3E",
    }.get(confidence, "#D69E2E")

    src_html = "".join(
        f'<div style="font-size:10px;color:rgba(255,255,255,0.5);padding:1px 0">• {s}</div>'
        for s in sources
    )
    note_html = (
        f'<div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:5px;'
        f'font-style:italic">{note}</div>'
    ) if note else ""

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(255,255,255,0.025);
            border:1px solid rgba(255,255,255,0.07)">
    <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:6px">
        <span style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.4);
                     letter-spacing:0.07em;text-transform:uppercase">🛡 TRAZABILIDAD</span>
        <span style="font-size:10px;font-weight:700;color:{conf_color}">
            Confianza: {confidence}</span>
    </div>
    {src_html}
    <div style="font-size:9px;color:rgba(255,255,255,0.28);margin-top:5px">
        Corte: {cut}</div>
    {note_html}
</div>""", unsafe_allow_html=True)


# ── 4. KPI MINI GRID ──────────────────────────────────────────────────────────

def kpi_mini(
    title: str,
    items: list[dict],   # [{"label": str, "value": str, "delta": str?, "color": str?}]
) -> None:
    """
    Grid de KPIs compactos con color opcional.
    delta positivo → verde; negativo → rojo.
    """
    if title:
        st.markdown(
            f'<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);'
            f'letter-spacing:0.08em;text-transform:uppercase;margin-top:10px;'
            f'margin-bottom:4px">📊 {title}</div>',
            unsafe_allow_html=True,
        )
    n = min(len(items), 5)
    cols = st.columns(n)
    for i, item in enumerate(items):
        with cols[i % n]:
            delta_str = item.get("delta")
            st.metric(
                label=item.get("label", ""),
                value=item.get("value", ""),
                delta=delta_str,
            )


# ── 5. SCENARIO CARD ──────────────────────────────────────────────────────────

def scenario_card(
    description:  str,
    baseline:     float,
    projected:    float,
    action_label: str  = "Ver Simulador completo",
    query_hash:   int  = 0,
) -> None:
    """
    Tarjeta de escenario con delta ICGI-T y botón al Simulador.
    """
    delta  = projected - baseline
    dsign  = "+" if delta >= 0 else ""
    dcolor = "#38A169" if delta >= 0 else "#E53E3E"

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(124,92,252,0.08);
            border:1px solid rgba(124,92,252,0.25)">
    <div style="font-size:10px;font-weight:700;color:rgba(124,92,252,0.9);
                letter-spacing:0.07em;text-transform:uppercase;margin-bottom:6px">
        🧮&nbsp;ESCENARIO PROYECTADO</div>
    <div style="font-size:12px;color:#E2E8F0;line-height:1.5">{description}</div>
    <div style="display:flex;gap:24px;margin-top:8px">
        <div>
            <div style="font-size:9px;color:rgba(255,255,255,0.35)">Baseline</div>
            <div style="font-size:16px;font-weight:700;color:#E2E8F0">{baseline:.2f}</div>
        </div>
        <div>
            <div style="font-size:9px;color:rgba(255,255,255,0.35)">Proyectado</div>
            <div style="font-size:16px;font-weight:700;color:#00D4FF">{projected:.2f}</div>
        </div>
        <div>
            <div style="font-size:9px;color:rgba(255,255,255,0.35)">Delta ICGI-T</div>
            <div style="font-size:16px;font-weight:700;color:{dcolor}">{dsign}{delta:.2f}</div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

    if st.button(
        f"🧮 {action_label}",
        key=f"sc_sim_{query_hash}",
        use_container_width=False,
    ):
        st.session_state["page"] = "simulador"
        st.rerun()
