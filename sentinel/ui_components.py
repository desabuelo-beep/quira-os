"""
SENTINEL · ui_components.py
Componentes de UI generativa — Sentinel v2 / Sprint 1-6.
Alert · Nav · Evidence · KPI Mini · Scenario · Simulation · Trust · Legal · QUADRUM.
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


# ── 6. SIMULATION CARD (Sprint 4) ─────────────────────────────────────────────

def simulation_card(result: dict, query_hash: int = 0) -> None:
    """
    Tarjeta completa de resultado de simulación paramétrica (CBST v0.1).
    result: dict devuelto por simulate_policy.simulate_policy()
    """
    b      = result["baseline"]
    p      = result["proyectado"]
    conf   = result["confidence"]
    c_lab  = result["confidence_label"]
    delta  = result["delta_pct"]
    nombre = result["territorio"]
    plabel = result["policy_label"]

    # Colores confianza
    c_color = (
        "#38A169" if conf >= 78 else
        "#D69E2E" if conf >= 65 else
        "#E53E3E"
    )

    def _row(label: str, base: float, proj: float, unit: str = "%",
             positive_is_good: bool = True) -> str:
        d = proj - base
        sign = "+" if d >= 0 else ""
        color = "#38A169" if (d >= 0) == positive_is_good else "#E53E3E"
        return (
            f'<tr>'
            f'<td style="padding:4px 8px;font-size:11px;color:rgba(255,255,255,0.6)">{label}</td>'
            f'<td style="padding:4px 8px;font-size:11px;color:#E2E8F0;text-align:right">{base:.2f}{unit}</td>'
            f'<td style="padding:4px 8px;font-size:11px;color:#00D4FF;text-align:right">{proj:.2f}{unit}</td>'
            f'<td style="padding:4px 8px;font-size:11px;font-weight:700;color:{color};text-align:right">'
            f'{sign}{d:.2f}{unit}</td>'
            f'</tr>'
        )

    rows = ""
    if p["agua_delta"] != 0:
        rows += _row("Cobertura Agua", b["agua"], p["agua"], "%", True)
    if p["nbi_delta"] != 0:
        rows += _row("NBI", b["nbi"], p["nbi"], "%", False)
    if p["tps_delta"] != 0:
        rows += _row("TPS (Pobreza Svc)", b["tps"], p["tps"], "%", False)
    rows += _row("ICGI-T Cantonal", b["icgit"], p["icgit"], "pts", True)

    inv_add = result["inversion_adicional"]
    inv_fmt = f"${inv_add:,}"

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(124,92,252,0.09);
            border:1px solid rgba(124,92,252,0.30)">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div>
      <div style="font-size:10px;font-weight:700;color:rgba(124,92,252,0.9);
                  letter-spacing:0.07em;text-transform:uppercase">
        🧮&nbsp;SIMULACIÓN CBST v0.1 — BETA</div>
      <div style="font-size:12px;font-weight:600;color:#E2E8F0;margin-top:3px">
        {plabel} · <b>{nombre}</b> · +{delta}%</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px">
        Inversión adicional: <b>{inv_fmt}</b>
        ({result['per_capita_nuevo']} $/hab vs {b['per_capita']} $/hab actual)</div>
    </div>
    <div style="text-align:right;min-width:70px">
      <div style="font-size:9px;color:rgba(255,255,255,0.35)">Confianza</div>
      <div style="font-size:20px;font-weight:700;color:{c_color}">{conf}%</div>
      <div style="font-size:9px;color:{c_color}">{c_lab}</div>
    </div>
  </div>
  <table style="width:100%;border-collapse:collapse">
    <thead>
      <tr>
        <th style="padding:3px 8px;font-size:9px;color:rgba(255,255,255,0.35);
                   text-align:left;font-weight:400">Indicador</th>
        <th style="padding:3px 8px;font-size:9px;color:rgba(255,255,255,0.35);
                   text-align:right;font-weight:400">Actual</th>
        <th style="padding:3px 8px;font-size:9px;color:rgba(255,255,255,0.35);
                   text-align:right;font-weight:400">Proyectado</th>
        <th style="padding:3px 8px;font-size:9px;color:rgba(255,255,255,0.35);
                   text-align:right;font-weight:400">Delta</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <div style="font-size:8px;color:rgba(255,255,255,0.22);margin-top:8px">
    ⚠ {result['nota']}</div>
</div>""", unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        if st.button("🧮 Ver Simulador", key=f"sim_go_{query_hash}",
                     use_container_width=True):
            st.session_state["page"] = "simulador"
            st.rerun()
    with cols[1]:
        if st.button("🗺️ GeoTwin", key=f"sim_geo_{query_hash}",
                     use_container_width=True):
            st.session_state["page"] = "geotwin"
            st.rerun()
    with cols[2]:
        if st.button("🔗 Cadena POA", key=f"sim_poa_{query_hash}",
                     use_container_width=True):
            st.session_state["page"] = "cadena"
            st.rerun()


# ── 7. TRUST BADGE (Sprint 5) ─────────────────────────────────────────────────

def trust_badge(trust_result: dict, legal_refs: list | None = None) -> None:
    """
    Badge compacto de Governance Confidence Index — aparece en cada respuesta.
    trust_result: dict de trust_engine.calculate_trust()
    legal_refs:   lista de chunks de legal_router.find_legal_refs()
    """
    score  = trust_result.get("score", 0)
    label  = trust_result.get("label", "")
    desg   = trust_result.get("desglose", {})
    nota   = trust_result.get("nota", "")
    from sentinel.trust_engine import trust_label_color
    color  = trust_label_color(score)

    desg_html = " · ".join(
        f'<span style="color:rgba(255,255,255,0.5)">{k}</span> '
        f'<span style="color:{color};font-weight:600">{v}%</span>'
        for k, v in desg.items()
    )

    legal_html = ""
    if legal_refs:
        law_labels = {"COOTAD": "COOTAD", "COPLAFIP": "COPLAFIP",
                      "COOTAD_2026": "COOTAD 2026"}
        citas = " · ".join(
            f"{law_labels.get(r['law'], r['law'])} {r['article']}"
            for r in legal_refs[:2]
        )
        legal_html = (
            f'<div style="font-size:9px;color:#38A169;margin-top:4px">'
            f'⚖ Sustento normativo: {citas}</div>'
        )

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.08);
            display:flex;justify-content:space-between;align-items:center;padding:8px 14px">
  <div>
    <span style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);
                 letter-spacing:0.07em;text-transform:uppercase">
      🛡 CONFIANZA INSTITUCIONAL</span>
    <div style="font-size:9px;margin-top:3px">{desg_html}</div>
    {legal_html}
    <div style="font-size:8px;color:rgba(255,255,255,0.22);margin-top:3px">{nota}</div>
  </div>
  <div style="text-align:right;min-width:56px;padding-left:12px">
    <div style="font-size:22px;font-weight:700;color:{color}">{score}%</div>
    <div style="font-size:9px;color:{color}">{label}</div>
  </div>
</div>""", unsafe_allow_html=True)


# ── 8. LEGAL CARD (Sprint Legal) ──────────────────────────────────────────────

def legal_card(refs: list[dict]) -> None:
    """
    Tarjeta de referencias normativas — muestra artículos relevantes de COOTAD/COPLAFIP.
    refs: lista de chunks de legal_router.find_legal_refs()
    """
    if not refs:
        return

    law_labels = {
        "COOTAD":     ("COOTAD",       "#00D4FF"),
        "COPLAFIP":   ("COPLAFIP",     "#7C5CFC"),
        "COOTAD_2026":("COOTAD 2026",  "#38A169"),
    }

    rows_html = ""
    for r in refs:
        label, color = law_labels.get(r["law"], (r["law"], "#E2E8F0"))
        txt = r["text"][:220] + "…" if len(r["text"]) > 220 else r["text"]
        rows_html += (
            f'<div style="border-left:3px solid {color};padding:6px 10px;margin:5px 0;'
            f'background:rgba(255,255,255,0.03);border-radius:0 6px 6px 0">'
            f'<div style="font-size:9px;font-weight:700;color:{color}">'
            f'{label} {r["article"]} — {r["topic"]}</div>'
            f'<div style="font-size:10px;color:rgba(255,255,255,0.6);margin-top:3px;line-height:1.4">'
            f'{txt}</div></div>'
        )

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(0,0,0,0.15);border:1px solid rgba(0,212,255,0.12)">
  <div style="font-size:10px;font-weight:700;color:rgba(0,212,255,0.7);
              letter-spacing:0.07em;text-transform:uppercase;margin-bottom:6px">
    ⚖&nbsp;MARCO NORMATIVO APLICABLE</div>
  {rows_html}
</div>""", unsafe_allow_html=True)


# ── 9. QUADRUM CARD (Sprint 6) ────────────────────────────────────────────────

def quadrum_card(quadrum_result: dict) -> None:
    """
    Tarjeta QUADRUM — evaluación de coherencia institucional entre las 4 capas.
    quadrum_result: dict de quadrum_engine.evaluate()
    """
    coherencia = quadrum_result.get("coherencia", 0)
    coh_label  = quadrum_result.get("coherencia_label", "")
    capas      = quadrum_result.get("capas", [])
    recoms     = quadrum_result.get("recomendaciones", [])
    criticos   = quadrum_result.get("criticos", 0)

    coh_color = (
        "#38A169" if coherencia >= 80 else
        "#D69E2E" if coherencia >= 65 else
        "#E53E3E"
    )

    estado_color = {"OK": "#38A169", "ALERTA": "#D69E2E",
                    "CRÍTICO": "#E53E3E", "PENDIENTE": "#7C5CFC"}

    capas_html = ""
    for c in capas:
        ec = estado_color.get(c["estado"], "#E2E8F0")
        capas_html += (
            f'<div style="flex:1;text-align:center;padding:6px 4px;'
            f'background:rgba(255,255,255,0.03);border-radius:6px;margin:2px">'
            f'<div style="font-size:8px;font-weight:700;color:{ec};text-transform:uppercase">'
            f'{c["capa"]}</div>'
            f'<div style="font-size:16px;font-weight:700;color:{ec}">{c["score"]}</div>'
            f'<div style="font-size:8px;color:rgba(255,255,255,0.4)">{c["pregunta"][:22]}</div>'
            f'</div>'
        )

    recoms_html = "".join(
        f'<div style="font-size:10px;color:rgba(255,255,255,0.6);padding:2px 0">{r}</div>'
        for r in recoms
    )

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(124,92,252,0.06);border:1px solid rgba(124,92,252,0.20)">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
    <div style="font-size:10px;font-weight:700;color:rgba(124,92,252,0.9);
                letter-spacing:0.07em;text-transform:uppercase">
      ◆ QUADRUM · Coherencia Institucional</div>
    <div style="text-align:right">
      <div style="font-size:20px;font-weight:700;color:{coh_color}">{coherencia}%</div>
      <div style="font-size:8px;color:{coh_color}">{coh_label}</div>
    </div>
  </div>
  <div style="display:flex;gap:4px;margin-bottom:8px">{capas_html}</div>
  <div style="border-top:1px solid rgba(255,255,255,0.06);padding-top:7px;margin-top:4px">
    <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);margin-bottom:4px">
      RECOMENDACIONES EJECUTIVAS</div>
    {recoms_html}
  </div>
</div>""", unsafe_allow_html=True)
