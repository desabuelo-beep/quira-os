"""
SENTINEL · ui_components.py
Componentes de UI generativa — Sentinel v2 / Sprint 1-8.
Alert · Nav · Evidence · KPI Mini · Scenario · Simulation · Trust · Legal · QUADRUM · RC-7.3 · RC-D4.
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
        🧮&nbsp;PROYECCIÓN CBST v0.1 — BETA</div>
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

    # Nota de impacto cantonal — solo cuando el delta ICGI-T es pequeño
    nota_cantonal = result.get("nota_impacto_cantonal", "")
    if nota_cantonal:
        st.markdown(
            f'<div style="font-size:10px;color:rgba(214,158,46,0.85);'
            f'background:rgba(214,158,46,0.07);border-left:3px solid rgba(214,158,46,0.4);'
            f'border-radius:0 6px 6px 0;padding:6px 10px;margin:4px 0 8px">'
            f'⚡ {nota_cantonal}</div>',
            unsafe_allow_html=True,
        )

    cols = st.columns(3)
    with cols[0]:
        if st.button("🧮 Ver Simulador", key=f"sim_go_{query_hash}",
                     use_container_width=True):
            st.session_state["page"] = "simulador"
            st.rerun()
    with cols[1]:
        if st.button("🗺️ Territorio Digital", key=f"sim_geo_{query_hash}",
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
        "COOTAD":      ("COOTAD",           "#00D4FF"),
        "COPLAFIP":    ("COPLAFIP",         "#7C5CFC"),
        "COOTAD_2026": ("COOTAD 2026",      "#38A169"),
        "CRE":         ("Constitución CRE", "#E67E22"),  # naranja = norma suprema
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


# ── 10. COHERENCIA CARD (Fase 3) ──────────────────────────────────────────────

def coherencia_card(result: dict) -> None:
    """
    Tarjeta de Coherencia Institucional — Fase 3.
    result: dict de coherencia_engine.evaluate()
    Muestra 4 dimensiones + Confianza de Implementación.
    """
    ci        = result.get("confianza_implementacion", 0)
    ci_label  = result.get("confianza_label", "")
    dims      = result.get("dimensiones", [])
    recoms    = result.get("recomendaciones", [])

    ci_color = (
        "#38A169" if ci >= 80 else
        "#00D4FF" if ci >= 65 else
        "#D69E2E" if ci >= 50 else
        "#E53E3E"
    )

    _NIVEL_COLOR = {
        "Alta":         "#38A169",
        "Media":        "#D69E2E",
        "Baja":         "#E67E22",
        "Insuficiente": "#E53E3E",
    }

    def _bar(score: int, nivel: str) -> str:
        color = _NIVEL_COLOR.get(nivel, "#E2E8F0")
        return (
            f'<div style="height:6px;background:rgba(255,255,255,0.06);'
            f'border-radius:3px;overflow:hidden;margin-top:4px">'
            f'<div style="height:6px;width:{min(score,100)}%;background:{color};'
            f'border-radius:3px"></div></div>'
        )

    dims_html = ""
    for d in dims:
        color = _NIVEL_COLOR.get(d["nivel"], "#E2E8F0")
        dims_html += (
            f'<div style="flex:1;padding:8px 6px;background:rgba(255,255,255,0.02);'
            f'border-radius:6px;margin:2px;border-top:2px solid {color}">'
            f'<div style="font-size:8px;font-weight:700;color:{color};'
            f'text-transform:uppercase;letter-spacing:0.05em">{d["dimension"]}</div>'
            f'<div style="font-size:18px;font-weight:700;color:{color};margin:3px 0">'
            f'{d["score"]}</div>'
            f'<div style="font-size:8px;color:rgba(255,255,255,0.4)">{d["nivel"]}</div>'
            f'{_bar(d["score"], d["nivel"])}'
            f'</div>'
        )

    recoms_html = "".join(
        f'<div style="font-size:10px;color:rgba(255,255,255,0.65);'
        f'padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04)">{r}</div>'
        for r in recoms
    )

    st.markdown(f"""
<div style="{_CARD_BASE}background:rgba(0,180,120,0.05);border:1px solid rgba(0,180,120,0.20)">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
    <div>
      <div style="font-size:10px;font-weight:700;color:rgba(56,161,105,0.9);
                  letter-spacing:0.07em;text-transform:uppercase">
        ◆ COHERENCIA INSTITUCIONAL</div>
      <div style="font-size:9px;color:rgba(255,255,255,0.35);margin-top:2px">
        Confianza de Implementación</div>
    </div>
    <div style="text-align:right;min-width:64px">
      <div style="font-size:28px;font-weight:900;color:{ci_color};line-height:1">{ci}%</div>
      <div style="font-size:8px;color:{ci_color};max-width:120px;text-align:right;margin-top:2px">
        {ci_label.split(' — ')[0]}</div>
    </div>
  </div>
  <div style="display:flex;gap:4px;margin-bottom:10px">{dims_html}</div>
  <div style="font-size:8px;color:rgba(255,255,255,0.25);margin-bottom:6px">{ci_label}</div>
  <div style="border-top:1px solid rgba(255,255,255,0.06);padding-top:7px">
    <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);margin-bottom:4px">
      PARA ELEVAR AL DECISOR</div>
    {recoms_html}
  </div>
</div>""", unsafe_allow_html=True)


# ── 11. CALIBRATION CARD — RC-7.3 (Sprint 7) ──────────────────────────────────

# AVEP risk → color + bg
_AVEP_PALETTE = {
    "Ruptura Institucional":  ("#E53E3E", "rgba(229,62,62,0.10)",  "rgba(229,62,62,0.30)"),
    "Ocurrencia Preocupante": ("#E67E22", "rgba(230,126,34,0.09)", "rgba(230,126,34,0.28)"),
    "Transición Crítica":     ("#D69E2E", "rgba(214,158,46,0.08)", "rgba(214,158,46,0.25)"),
    "Mandato Cumplido":       ("#00D4FF", "rgba(0,212,255,0.06)",  "rgba(0,212,255,0.20)"),
    "Excelencia Institucional":("#38A169","rgba(56,161,105,0.07)", "rgba(56,161,105,0.22)"),
}

_CLASS_DISPLAY = {
    "PARALISIS_ESTRUCTURAL":       "Parálisis Estructural",
    "CONTRACCION_CRITICA":         "Contracción Crítica",
    "Q4_CONCENTRACION_TERMINAL":   "Concentración Q4 Terminal",
    "REFORMA_SHOCK":               "Reforma Shock",
    "EXPANSION_TARDIA":            "Expansión Tardía",
    "RECUPERACION_ACTIVA":         "Recuperación Activa",
    "EXPANSION_PRESUPUESTARIA":    "Expansión Presupuestaria",
    "EJECUCION_ESTABLE":           "Ejecución Estable",
    "LIDER_EJECUCION":             "Líder de Ejecución",
    "SIN_PATRON_CLARO":            "Sin Patrón Claro",
}


def calibration_card(cr: dict, query_hash: int = 0) -> None:
    """
    Tarjeta RC-7.3 — Diagnóstico Calibrado de Ejecución Presupuestaria.

    Muestra: clase institucional calibrada · AVEP score · confianza raw→calibrada
    · peso evidencial · SATs activos · reglas de calibración aplicadas.

    Args:
        cr:         dict devuelto por summarize_calibrated(CalibratedResult)
        query_hash: int para llaves únicas de widgets Streamlit
    """
    if not cr:
        return

    # ── Extraer campos ──────────────────────────────────────────────────────────
    cal_class    = cr.get("calibrated_class", "SIN_PATRON_CLARO")
    orig_class   = cr.get("original_class", "")
    raw_conf     = float(cr.get("raw_confidence", 0))
    cal_conf     = float(cr.get("calibrated_confidence", 0))
    ev_weight    = float(cr.get("evidence_weight", 0))
    seasonal_f   = float(cr.get("seasonal_factor", 1.0))
    baseline_gap = float(cr.get("baseline_gap", 0))
    reform_wl    = bool(cr.get("reform_whitelisted", False))
    sats         = cr.get("sat_codes_calibrated", [])
    rules        = cr.get("calibration_applied", [])
    avep_riesgo  = cr.get("avep_riesgo", "Transición Crítica")
    avep_score   = float(cr.get("avep_score", 50))
    narrative    = cr.get("narrative", "")

    class_label  = _CLASS_DISPLAY.get(cal_class, cal_class.replace("_", " ").title())
    reclassified = orig_class and orig_class != cal_class
    color, bg, border = _AVEP_PALETTE.get(avep_riesgo, _AVEP_PALETTE["Transición Crítica"])

    # ── Barra doble: confianza raw (pálida) → calibrada (sólida) ───────────────
    raw_w = int(min(raw_conf * 100, 100))
    cal_w = int((cal_conf / raw_conf * 100) if raw_conf > 0 else 0)

    bar_html = (
        f'<div style="background:rgba(255,255,255,0.07);border-radius:4px;'
        f'height:6px;overflow:hidden;margin:5px 0 3px">'
        f'<div style="height:6px;width:{raw_w}%;'
        f'background:rgba(255,255,255,0.18);border-radius:4px;position:relative">'
        f'<div style="height:6px;width:{cal_w}%;background:{color};border-radius:4px">'
        f'</div></div></div>'
    )

    # ── Chips: reglas de calibración ────────────────────────────────────────────
    chip_style = (
        f"display:inline-block;font-size:8px;font-weight:600;padding:2px 7px;"
        f"border-radius:10px;margin:2px 2px;background:rgba(255,255,255,0.06);"
        f"border:1px solid rgba(255,255,255,0.12);color:rgba(255,255,255,0.55)"
    )
    chips_html = "".join(
        f'<span style="{chip_style}">{r.split(":")[0].strip()}</span>'
        for r in rules
    ) if rules else (
        f'<span style="{chip_style}">sin ajustes adicionales</span>'
    )

    # ── SATs ────────────────────────────────────────────────────────────────────
    sat_colors = {
        "SAT-IX":  "#E53E3E",
        "SAT-X-A": "#E67E22",
        "SAT-X-B": "#D69E2E",
        "SAT-XI":  "#D69E2E",
        "SAT-XII": "#00D4FF",
    }
    if sats:
        sats_html = " ".join(
            f'<span style="font-size:9px;font-weight:700;color:{sat_colors.get(s,"#E2E8F0")};'
            f'background:rgba(255,255,255,0.05);border:1px solid '
            f'{sat_colors.get(s,"rgba(255,255,255,0.15)")};border-radius:4px;'
            f'padding:2px 6px">{s}</span>'
            for s in sats
        )
    else:
        sats_html = (
            '<span style="font-size:9px;color:rgba(255,255,255,0.30)">'
            'ninguno activo · umbral: conf≥40% · ev≥50%</span>'
        )

    # ── Reclasificación badge ───────────────────────────────────────────────────
    reclassified_html = ""
    if reclassified:
        orig_label = _CLASS_DISPLAY.get(orig_class, orig_class.replace("_", " ").title())
        reclassified_html = (
            f'<div style="font-size:9px;color:#D69E2E;margin-top:3px">'
            f'⚡ Reclasificado: {orig_label} → {class_label}</div>'
        )

    # ── Render tarjeta principal ────────────────────────────────────────────────
    st.markdown(f"""
<div style="{_CARD_BASE}background:{bg};border:1px solid {border};border-left:4px solid {color}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div style="flex:1;min-width:0">
      <div style="font-size:9px;font-weight:700;color:{color};letter-spacing:0.07em;
                  text-transform:uppercase">📊 RC-7.3 · DIAGNÓSTICO CALIBRADO</div>
      <div style="font-size:14px;font-weight:700;color:#E2E8F0;margin-top:3px;
                  line-height:1.2">{class_label}</div>
      {reclassified_html}
    </div>
    <div style="text-align:right;min-width:60px;padding-left:10px">
      <div style="font-size:22px;font-weight:900;color:{color};line-height:1">{avep_score:.0f}</div>
      <div style="font-size:8px;color:{color};white-space:nowrap">{avep_riesgo}</div>
    </div>
  </div>
  <div style="font-size:11px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:8px">
    {narrative[:300] if narrative else ""}</div>
  <div style="font-size:9px;color:rgba(255,255,255,0.40)">
    Confianza epistémica:&nbsp;
    <span style="color:rgba(255,255,255,0.60)">{raw_conf:.0%}</span>
    &nbsp;→&nbsp;
    <span style="color:{color};font-weight:700">{cal_conf:.0%}</span>
    &nbsp;·&nbsp;Peso evidencial:&nbsp;
    <span style="color:rgba(255,255,255,0.60)">{ev_weight:.0%}</span>
  </div>
  {bar_html}
  <div style="margin-top:4px">{chips_html}</div>
  <div style="border-top:1px solid rgba(255,255,255,0.06);margin-top:8px;padding-top:6px;
              display:flex;align-items:center;gap:8px;flex-wrap:wrap">
    <span style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);
                 text-transform:uppercase;letter-spacing:0.06em">SATs&nbsp;</span>
    {sats_html}
  </div>
</div>""", unsafe_allow_html=True)

    # ── Detalle expandible: reglas completas ────────────────────────────────────
    if rules:
        with st.expander(f"🔬 Calibración aplicada ({len(rules)} regla{'s' if len(rules)>1 else ''})",
                         expanded=False):
            for rule in rules:
                st.markdown(
                    f'<div style="font-size:10px;color:rgba(255,255,255,0.6);'
                    f'padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04)">'
                    f'· {rule}</div>',
                    unsafe_allow_html=True,
                )
            extras = []
            if seasonal_f != 1.0:
                extras.append(f"Factor estacional: {seasonal_f:.2f}")
            if abs(baseline_gap) > 0.01:
                sign = "+" if baseline_gap > 0 else ""
                extras.append(f"Brecha vs baseline entidad: {sign}{baseline_gap:.0%}")
            if reform_wl:
                extras.append("Reforma dentro del umbral COPLAFIP Art.97 (Alcalde) — SAT-X-B suprimido")
            for extra in extras:
                st.markdown(
                    f'<div style="font-size:9px;color:rgba(255,255,255,0.40);padding:2px 0">'
                    f'  {extra}</div>',
                    unsafe_allow_html=True,
                )


# ── 12. D4 CARD — RC-D4 Equidad Territorial (Sprint 8) ───────────────────────

# AVEP D4 → (text_color, bg, border)
_D4_AVEP_PALETTE = {
    "Ruptura Territorial":    ("#E53E3E", "rgba(229,62,62,0.10)",  "rgba(229,62,62,0.35)"),
    "Inequidad Estructural":  ("#E67E22", "rgba(230,126,34,0.09)", "rgba(230,126,34,0.30)"),
    "Sesgo Distributivo":     ("#D69E2E", "rgba(214,158,46,0.08)", "rgba(214,158,46,0.25)"),
    "Distribución Aceptable": ("#48BB78", "rgba(72,187,120,0.07)", "rgba(72,187,120,0.22)"),
    "Equidad Territorial":    ("#38A169", "rgba(56,161,105,0.07)", "rgba(56,161,105,0.22)"),
}

_D4_IRS_META_2027 = 45.0   # objetivo institucional: IRS ≤ 45


def d4_card(cr: dict, query_hash: int = 0) -> None:
    """
    Componente 12 — Panel de Equidad Territorial RC-D4.

    Muestra: AVEP D4 · IRS gauge con meta-2027 · tabla parroquial (need vs actual)
    · señal triple territorial · SAT-D4 chips · prudencia espacial aplicada.

    Args:
        cr:         dict de summarize_d4_calibrated(CalibratedD4Result)
        query_hash: int para llaves únicas de widgets Streamlit
    """
    if not cr:
        return

    # ── Extraer campos ─────────────────────────────────────────────────────────
    avep_riesgo  = cr.get("avep_d4_riesgo", "Distribución Aceptable")
    avep_score   = float(cr.get("avep_d4_score", 60))
    irs          = float(cr.get("irs", 0))
    gini         = float(cr.get("gini", 0))
    cr1          = float(cr.get("cr1", 0))
    cr2          = float(cr.get("cr2", 0))
    cap_ratio    = float(cr.get("capital_ratio", 0))
    n_crit       = int(cr.get("n_critical_underfunded", 0))
    narrative    = cr.get("narrative", "")
    raw_conf     = float(cr.get("raw_confidence", 0))
    cal_conf     = float(cr.get("calibrated_confidence", 0))
    adj          = cr.get("adjustments_applied", [])
    patterns     = cr.get("patterns_summary", [])
    parishes     = cr.get("parish_analyses_summary", [])
    sat_codes    = cr.get("sat_codes_calibrated", [])

    color, bg, border = _D4_AVEP_PALETTE.get(avep_riesgo, _D4_AVEP_PALETTE["Sesgo Distributivo"])
    overwhelm    = irs >= 85.0

    # ── Triple señal territorial (hiperconcentración institucionalizada) ────────
    triple_signal = irs >= 70 and cr1 >= 0.65 and cap_ratio >= 3.0
    triple_html   = ""
    if triple_signal:
        triple_html = (
            '<div style="background:rgba(229,62,62,0.15);border:1px solid rgba(229,62,62,0.35);'
            'border-radius:4px;padding:4px 8px;margin-top:5px;font-size:9px;'
            'color:#FC8181;font-weight:700;letter-spacing:0.04em">'
            '&#9888; ASIMETRÍA TERRITORIAL TRIPLE: IRS crítico · CR1 extremo · captura capital'
            '</div>'
        )

    overwhelm_html = ""
    if overwhelm:
        overwhelm_html = (
            '<div style="background:rgba(229,62,62,0.20);border-left:3px solid #E53E3E;'
            'border-radius:0 4px 4px 0;padding:3px 8px;margin-top:4px;font-size:9px;'
            'color:#FC8181;font-weight:700">'
            '&#9889; EVIDENCIA ABRUMADORA (IRS ≥ 85) — calibración máxima: descuentos omitidos'
            '</div>'
        )

    # ── IRS gauge HTML ─────────────────────────────────────────────────────────
    irs_frac   = min(1.0, irs / 100.0)
    meta_frac  = _D4_IRS_META_2027 / 100.0
    gauge_color = (
        "#E53E3E" if irs >= 80 else
        "#E67E22" if irs >= 60 else
        "#D69E2E" if irs >= 40 else
        "#48BB78" if irs >= 20 else
        "#38A169"
    )
    brecha_meta = irs - _D4_IRS_META_2027
    gauge_html = (
        f'<div style="margin:8px 0 4px 0">'
        f'<div style="display:flex;justify-content:space-between;'
        f'font-size:9px;color:rgba(255,255,255,0.30);margin-bottom:3px">'
        f'<span>0 — Equidad plena</span>'
        f'<span style="color:#63B3ED">Meta 2027: {_D4_IRS_META_2027:.0f}</span>'
        f'<span>100 — Máx. regresivo</span></div>'
        f'<div style="background:rgba(255,255,255,0.07);border-radius:4px;'
        f'height:8px;position:relative;overflow:visible">'
        f'<div style="height:8px;width:{irs_frac*100:.1f}%;background:{gauge_color};'
        f'border-radius:4px;transition:width 0.3s"></div>'
        f'<div style="position:absolute;top:-4px;left:{meta_frac*100:.1f}%;'
        f'width:2px;height:16px;background:#63B3ED;border-radius:1px" '
        f'title="Meta IRS 2027"></div>'
        f'</div>'
        f'<div style="font-size:9px;color:rgba(255,255,255,0.35);'
        f'text-align:right;margin-top:3px">'
        f'Brecha a meta 2027: <span style="color:{gauge_color};font-weight:700">'
        f'{brecha_meta:+.1f} puntos IRS</span></div>'
        f'</div>'
    )

    # ── SAT-D4 chips ───────────────────────────────────────────────────────────
    _SAT_D4_COLORS = {
        "SAT-D4-A": "#E53E3E",
        "SAT-D4-B": "#E67E22",
        "SAT-D4-C": "#D69E2E",
        "SAT-D4-D": "#00D4FF",
        "SAT-D4-E": "#7C5CFC",
    }
    if sat_codes:
        sats_html = " ".join(
            f'<span style="font-size:9px;font-weight:700;'
            f'color:{_SAT_D4_COLORS.get(s,"#E2E8F0")};'
            f'background:rgba(255,255,255,0.05);'
            f'border:1px solid {_SAT_D4_COLORS.get(s,"rgba(255,255,255,0.15)")};'
            f'border-radius:4px;padding:2px 6px">{s}</span>'
            for s in sat_codes
        )
    else:
        sats_html = (
            '<span style="font-size:9px;color:rgba(255,255,255,0.30)">'
            'ninguno activo</span>'
        )

    # ── Render tarjeta principal ───────────────────────────────────────────────
    st.markdown(f"""
<div style="{_CARD_BASE}background:{bg};border:1px solid {border};border-left:4px solid {color}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
    <div style="flex:1;min-width:0">
      <div style="font-size:9px;font-weight:700;color:{color};letter-spacing:0.07em;
                  text-transform:uppercase">&#127760; RC-D4 &middot; EQUIDAD TERRITORIAL</div>
      <div style="font-size:13px;font-weight:700;color:#E2E8F0;margin-top:3px;line-height:1.2">
        {avep_riesgo}</div>
      <div style="font-size:10px;color:rgba(255,255,255,0.55);margin-top:4px;line-height:1.5">
        {narrative[:220] if narrative else ""}</div>
      {triple_html}
      {overwhelm_html}
    </div>
    <div style="text-align:right;min-width:64px;padding-left:10px">
      <div style="font-size:28px;font-weight:900;color:{color};line-height:1">
        {irs:.0f}</div>
      <div style="font-size:8px;color:rgba(255,255,255,0.35);margin-top:1px">IRS</div>
      <div style="font-size:16px;font-weight:700;color:{color};margin-top:4px;line-height:1">
        {avep_score:.0f}</div>
      <div style="font-size:8px;color:rgba(255,255,255,0.35)">AVEP</div>
    </div>
  </div>

  {gauge_html}

  <div style="display:flex;gap:8px;margin:8px 0 6px 0;flex-wrap:wrap">
    <div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:5px 10px;flex:1;min-width:60px">
      <div style="font-size:8px;color:rgba(255,255,255,0.30);text-transform:uppercase">Gini inv.</div>
      <div style="font-size:16px;font-weight:700;color:{color}">{gini:.3f}</div>
    </div>
    <div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:5px 10px;flex:1;min-width:60px">
      <div style="font-size:8px;color:rgba(255,255,255,0.30);text-transform:uppercase">CR1</div>
      <div style="font-size:16px;font-weight:700;color:{color}">{cr1:.0%}</div>
    </div>
    <div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:5px 10px;flex:1;min-width:60px">
      <div style="font-size:8px;color:rgba(255,255,255,0.30);text-transform:uppercase">Cap.&times;</div>
      <div style="font-size:16px;font-weight:700;color:{color}">{cap_ratio:.1f}x</div>
    </div>
    <div style="background:rgba(255,255,255,0.04);border-radius:6px;padding:5px 10px;flex:1;min-width:60px">
      <div style="font-size:8px;color:rgba(255,255,255,0.30);text-transform:uppercase">Rezago&nbsp;cr.</div>
      <div style="font-size:16px;font-weight:700;color:{color}">{n_crit}</div>
    </div>
  </div>

  <div style="border-top:1px solid rgba(255,255,255,0.06);margin-top:6px;padding-top:5px;
              display:flex;align-items:center;gap:8px;flex-wrap:wrap">
    <span style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);
                 text-transform:uppercase;letter-spacing:0.06em">SAT-D4&nbsp;</span>
    {sats_html}
  </div>
</div>""", unsafe_allow_html=True)

    # ── Tabla parroquial — el "oro institucional" ──────────────────────────────
    if parishes:
        def _gap_color(gap: float) -> str:
            if gap < -0.60: return "#FC8181"    # rojo claro — rezago crítico
            if gap < -0.30: return "#F6AD55"    # naranja
            if gap < 0.0:   return "#F6E05E"    # ámbar
            return "#68D391"                    # verde — sobre baseline

        rows_html = ""
        for p in parishes:
            tipo_icon = "&#127970;" if p["tipo"] == "Urbana" else "&#127807;"
            gc = _gap_color(p["gap"])
            inv_vs_exp = "&#9650;" if p["over"] else "&#9660;"   # ▲ ▼
            rows_html += (
                f'<tr style="border-bottom:1px solid rgba(255,255,255,0.04)">'
                f'<td style="padding:4px 6px;font-size:10px;color:rgba(255,255,255,0.80)">'
                f'{tipo_icon} {p["nombre"]}</td>'
                f'<td style="padding:4px 6px;font-size:10px;color:rgba(255,255,255,0.45);'
                f'text-align:right">{p["cn"]:.0f}</td>'
                f'<td style="padding:4px 6px;font-size:10px;color:rgba(255,255,255,0.70);'
                f'text-align:right">${p["inv"]}</td>'
                f'<td style="padding:4px 6px;font-size:10px;color:rgba(255,255,255,0.45);'
                f'text-align:right">${p["exp"]}</td>'
                f'<td style="padding:4px 6px;font-size:10px;font-weight:700;color:{gc};'
                f'text-align:right">{inv_vs_exp} {p["gap"]:+.0%}</td>'
                f'</tr>'
            )

        st.markdown(
            f'<div style="{_CARD_BASE}background:rgba(0,0,0,0.20);'
            f'border:1px solid rgba(255,255,255,0.07);padding:8px 0 4px 0">'
            f'<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
            f'letter-spacing:0.07em;text-transform:uppercase;padding:0 10px 5px 10px">'
            f'PARROQUIAS — necesidad compuesta vs inversión real</div>'
            f'<table style="width:100%;border-collapse:collapse">'
            f'<thead><tr style="background:rgba(255,255,255,0.04)">'
            f'<th style="padding:3px 6px;font-size:9px;color:rgba(255,255,255,0.30);'
            f'font-weight:600;text-align:left">Parroquia</th>'
            f'<th style="padding:3px 6px;font-size:9px;color:rgba(255,255,255,0.30);'
            f'font-weight:600;text-align:right">CN</th>'
            f'<th style="padding:3px 6px;font-size:9px;color:rgba(255,255,255,0.30);'
            f'font-weight:600;text-align:right">Real $/hab</th>'
            f'<th style="padding:3px 6px;font-size:9px;color:rgba(255,255,255,0.30);'
            f'font-weight:600;text-align:right">Equit. $/hab</th>'
            f'<th style="padding:3px 6px;font-size:9px;color:rgba(255,255,255,0.30);'
            f'font-weight:600;text-align:right">Brecha</th>'
            f'</tr></thead>'
            f'<tbody>{rows_html}</tbody>'
            f'</table>'
            f'<div style="font-size:8px;color:rgba(255,255,255,0.20);padding:4px 10px">'
            f'CN = Composite Need (0.5×NBI + 0.3×déficit agua + 0.2×pop_share) &middot; '
            f'Equit. = baseline de distribución proporcional a necesidad</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Detalle expandible: calibración espacial + marco normativo ────────────
    exp_label = (
        f"🌍 Análisis D4 — prudencia espacial"
        + (f" · {len(adj)} ajuste{'s' if len(adj)>1 else ''}" if adj else "")
    )
    with st.expander(exp_label, expanded=False):
        # ── Patrones detectados ────────────────────────────────────────────────
        if patterns:
            st.markdown(
                '<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
                'margin-bottom:3px">PATRONES ACTIVOS</div>',
                unsafe_allow_html=True,
            )
            for p in patterns:
                risk_color = {"CRITICO": "#E53E3E", "ALTO": "#E67E22",
                              "MEDIO": "#D69E2E", "BAJO": "#48BB78"}.get(p.get("risk",""), "#E2E8F0")
                st.markdown(
                    f'<div style="font-size:10px;color:rgba(255,255,255,0.6);padding:2px 0">'
                    f'<span style="color:{risk_color};font-weight:700">[{p.get("risk","")}]</span>'
                    f' {p.get("nombre","").replace("_"," ")} &middot; '
                    f'{p.get("sat_hint","")} &middot; conf={p.get("confianza",0):.0%}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # ── Calibración espacial ───────────────────────────────────────────────
        if adj:
            st.markdown(
                '<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
                'margin-top:8px;margin-bottom:3px">PRUDENCIA ESPACIAL</div>',
                unsafe_allow_html=True,
            )
            for a in adj:
                st.markdown(
                    f'<div style="font-size:10px;color:rgba(255,255,255,0.55);'
                    f'padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04)">'
                    f'· {a}</div>',
                    unsafe_allow_html=True,
                )

        st.caption(
            f"Confianza: {raw_conf:.0%} → {cal_conf:.0%}  "
            f"| CR2: {cr2:.0%}  "
            f"| Bypass: {'ACTIVO (IRS≥85)' if overwhelm else 'inactivo'}"
        )

        # ── Marco normativo (D4-Normative) ────────────────────────────────────
        try:
            from sentinel.d4_normative import bind_d4_from_dict
            _norm = bind_d4_from_dict(cr)
            if _norm.overall_tier != "sin_tension":
                _tier_color = {
                    "severa":    "#E53E3E",
                    "moderada":  "#E67E22",
                    "potencial": "#D69E2E",
                }.get(_norm.overall_tier, "#E2E8F0")
                st.markdown(
                    f'<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
                    f'margin-top:10px;margin-bottom:3px">MARCO NORMATIVO D4</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div style="font-size:9px;font-weight:700;color:{_tier_color};'
                    f'margin-bottom:4px">Nivel de tension: {_norm.overall_tier.upper()}</div>',
                    unsafe_allow_html=True,
                )
                for ref in _norm.refs:
                    verif_badge = (
                        '<span style="color:#48BB78;font-size:8px"> verificado</span>'
                        if ref.verificado else
                        '<span style="color:#D69E2E;font-size:8px"> pendiente verificacion</span>'
                    )
                    st.markdown(
                        f'<div style="border-left:2px solid {_tier_color};padding:3px 8px;'
                        f'margin:3px 0;background:rgba(255,255,255,0.02);border-radius:0 4px 4px 0">'
                        f'<div style="font-size:9px;font-weight:700;color:{_tier_color}">'
                        f'{ref.law} {ref.article}{verif_badge}</div>'
                        f'<div style="font-size:9px;color:rgba(255,255,255,0.45);margin-top:1px">'
                        f'{ref.topic}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                # PDOT alignment — instrumento prioritario
                pdot = _norm.pdot_alignment
                if pdot["nivel"] != "cumplido":
                    pdot_color = {"severa": "#E53E3E", "moderada": "#E67E22",
                                  "potencial": "#D69E2E"}.get(pdot["nivel"], "#E2E8F0")
                    st.markdown(
                        f'<div style="margin-top:5px;background:rgba(255,255,255,0.03);'
                        f'border:1px solid rgba(255,255,255,0.08);border-radius:4px;'
                        f'padding:5px 8px;font-size:9px">'
                        f'<span style="color:{pdot_color};font-weight:700">PDOT 2023-2027</span>'
                        f'<span style="color:rgba(255,255,255,0.35)"> brecha: </span>'
                        f'<span style="color:{pdot_color};font-weight:700">'
                        f'{pdot["brecha"]:+.1f} pts IRS</span>'
                        f'<span style="color:rgba(255,255,255,0.40)"> vs meta <= '
                        f'{pdot["meta"]:.0f}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    '<div style="font-size:8px;color:rgba(255,255,255,0.25);margin-top:5px;'
                    'font-style:italic">'
                    'El sistema senala divergencias observables. '
                    'La autoridad publica determina implicancias juridicas.'
                    '</div>',
                    unsafe_allow_html=True,
                )
        except ImportError:
            pass  # d4_normative aun no disponible


# ── 13. D3xD4 CROSS-INFERENCE CARD ───────────────────────────────────────────

# Colores por severidad D3xD4
_D3D4_SEV_COLORS: dict[str, tuple] = {
    "CRITICO":      ("#E53E3E", "rgba(229,62,62,0.12)",  "rgba(229,62,62,0.40)"),
    "ALTO":         ("#E67E22", "rgba(230,126,34,0.10)", "rgba(230,126,34,0.35)"),
    "MEDIO":        ("#D69E2E", "rgba(214,158,46,0.08)", "rgba(214,158,46,0.28)"),
    "OBSERVACIONAL":("#00D4FF", "rgba(0,212,255,0.06)",  "rgba(0,212,255,0.22)"),
}

# Colores por clase EED
_EED_CLASS_COLORS: dict[str, str] = {
    "expansion_concentrada": "#E53E3E",
    "rezago_distributivo":   "#E67E22",
    "alineado":              "#38A169",
}

# Etiquetas de patron cruzado en espanol
_CROSS_LABELS: dict[str, str] = {
    "EXPANSION_CONCENTRADA":     "Expansion Concentrada",
    "EXPANSION_CON_EXCLUSION":   "Expansion con Exclusion",
    "CRISIS_DOBLE":              "Crisis Doble",
    "EXCLUSION_PERIFERICA":      "Exclusion Periferica",
    "VULNERABILIDAD_HIDRICA":    "Vulnerabilidad Hidrica",
    "MAQUILLAJE_TERRITORIAL":    "Maquillaje Territorial",
    "REDISTRIBUCION_REGRESIVA":  "Redistribucion Regresiva",
    "CONVERGENCIA_CRITICA":      "Convergencia Critica",
    "SIN_CRUCE_CONFIRMADO":      "Sin Cruce Confirmado",
}


def d3d4_card(
    cross_dict:  dict,
    query_hash:  int = 0,
) -> None:
    """
    Componente 13 — Tarjeta de inferencia cruzada D3xD4.
    cross_dict: output de summarize_cross() — sentinel.d3d4_engine

    Muestra:
      - Header: patron cruzado + severidad + badge observacional
      - EED gauge (barometro temporal-territorial)
      - Dos columnas: estado D3 | estado D4
      - Narrativa del patron
      - Expander: evidencias auditables
    """
    if not cross_dict:
        return

    cross_pattern = cross_dict.get("cross_pattern",      "SIN_CRUCE_CONFIRMADO")
    severity      = cross_dict.get("severity",           "OBSERVACIONAL")
    observational = cross_dict.get("observational_only", True)
    eed_score     = float(cross_dict.get("eed_score",    0.0))
    eed_class     = cross_dict.get("eed_class",          "alineado")
    narrative     = cross_dict.get("narrative",          "")
    sat_codes     = cross_dict.get("sat_codes",          [])
    d3_s          = cross_dict.get("d3_state",           {})
    d4_s          = cross_dict.get("d4_state",           {})
    cross_conf    = float(cross_dict.get("cross_confidence", 0.0))
    evidence      = cross_dict.get("evidence",           [])

    color, bg, border = _D3D4_SEV_COLORS.get(severity, _D3D4_SEV_COLORS["OBSERVACIONAL"])
    label         = _CROSS_LABELS.get(cross_pattern, cross_pattern.replace("_", " "))
    eed_color     = _EED_CLASS_COLORS.get(eed_class, "#E2E8F0")

    # Badge observacional
    obs_badge = ""
    if observational:
        obs_badge = (
            '<span style="background:rgba(0,212,255,0.15);color:#00D4FF;'
            'border:1px solid rgba(0,212,255,0.40);border-radius:4px;'
            'font-size:8px;font-weight:700;padding:1px 5px;margin-left:6px;'
            'letter-spacing:0.05em">OBSERVACIONAL</span>'
        )

    # SAT chips D3D4
    sat_html = ""
    if sat_codes:
        chips = "".join(
            f'<span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);'
            f'border-radius:4px;font-size:8px;font-weight:700;color:{color};padding:1px 6px;'
            f'margin-right:4px">{s}</span>'
            for s in sat_codes
        )
        sat_html = f'<div style="margin-top:5px">{chips}</div>'

    # EED gauge bar — centro = 0, escala -80 a +80
    eed_clamped = max(-80, min(80, eed_score))
    eed_pct_center = 50.0
    eed_pct_fill   = eed_clamped / 1.6   # -80→-50, 0→0, +80→+50 offset from center
    if eed_score >= 0:
        bar_left  = eed_pct_center
        bar_width = abs(eed_pct_fill)
        bar_color = "#E53E3E" if eed_class == "expansion_concentrada" else "#D69E2E"
    else:
        bar_left  = eed_pct_center + eed_pct_fill
        bar_width = abs(eed_pct_fill)
        bar_color = "#E67E22"

    eed_gauge_html = f"""
<div style="margin:8px 0 6px 0">
  <div style="display:flex;justify-content:space-between;margin-bottom:2px">
    <span style="font-size:8px;color:rgba(255,255,255,0.35)">Rezago Distributivo</span>
    <span style="font-size:9px;font-weight:700;color:{eed_color}">
      EED {eed_score:+.1f} pts</span>
    <span style="font-size:8px;color:rgba(255,255,255,0.35)">Expansion Concentrada</span>
  </div>
  <div style="background:rgba(255,255,255,0.08);border-radius:4px;height:6px;position:relative;overflow:hidden">
    <div style="position:absolute;top:0;left:49.5%;width:1px;height:100%;
                background:rgba(255,255,255,0.25)"></div>
    <div style="position:absolute;top:0;left:{bar_left:.1f}%;width:{bar_width:.1f}%;
                height:100%;background:{bar_color};border-radius:4px;
                transition:width 0.4s ease"></div>
  </div>
</div>"""

    # ── Header card ──────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="{_CARD_BASE}background:{bg};border:1px solid {border};border-left:4px solid {color}">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
    <div style="flex:1;min-width:0">
      <div style="font-size:9px;font-weight:700;color:{color};letter-spacing:0.07em;
                  text-transform:uppercase">&#128202; D3&times;D4 &middot; INFERENCIA CRUZADA
        {obs_badge}
      </div>
      <div style="font-size:13px;font-weight:700;color:#E2E8F0;margin-top:3px;line-height:1.2">
        {label}</div>
      {sat_html}
    </div>
    <div style="text-align:right;min-width:72px;padding-left:10px">
      <div style="font-size:10px;font-weight:700;color:{color};letter-spacing:0.04em">
        {severity}</div>
      <div style="font-size:11px;font-weight:700;color:{eed_color};margin-top:2px">
        {eed_score:+.1f}</div>
      <div style="font-size:8px;color:rgba(255,255,255,0.35)">EED pts</div>
      <div style="font-size:9px;color:rgba(255,255,255,0.40);margin-top:2px">
        conf {cross_conf:.0%}</div>
    </div>
  </div>
  {eed_gauge_html}
</div>""", unsafe_allow_html=True)

    # ── Dos columnas: D3 state | D4 state ────────────────────────────────────
    col_d3, col_d4 = st.columns(2)

    d3_conf   = float(d3_s.get("confidence",  0.0))
    d3_class  = d3_s.get("avep_class",  "SIN_PATRON_CLARO")
    d3_score  = float(d3_s.get("avep_score",  52.0))
    d3_riesgo = d3_s.get("avep_riesgo", "Transicion Critica")
    d3_ew     = float(d3_s.get("evidence_wt", 0.0))
    d3_sats   = d3_s.get("sat_codes",   [])

    d4_conf   = float(d4_s.get("confidence",   0.0))
    d4_pat    = d4_s.get("principal_pattern", "SIN_PATRON")
    d4_irs    = float(d4_s.get("irs",           0.0))
    d4_score  = float(d4_s.get("avep_d4_score", 100.0))
    d4_riesgo = d4_s.get("avep_d4_riesgo",     "Equidad Territorial")
    d4_ncrit  = int(d4_s.get("n_critical",     0))

    # Colores confianza
    _conf_color = lambda c: (
        "#E53E3E" if c < 0.25 else
        "#E67E22" if c < 0.50 else
        "#D69E2E" if c < 0.75 else
        "#38A169"
    )

    with col_d3:
        d3_cc = _conf_color(d3_conf)
        d3_has = d3_s.get("confidence", None) is not None and d3_conf > 0
        d3_insuf_note = (
            '<div style="font-size:8px;color:#00D4FF;margin-top:3px">'
            '&#9432; Datos insuficientes — periodo(s) incompleto(s)</div>'
        ) if (not d3_has or d3_conf < 0.20) else ""
        st.markdown(f"""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.10);
            border-radius:8px;padding:10px 12px">
  <div style="font-size:8px;font-weight:700;color:rgba(255,255,255,0.35);
              text-transform:uppercase;letter-spacing:0.06em">D3 Temporal</div>
  <div style="font-size:11px;font-weight:700;color:#E2E8F0;margin-top:4px;line-height:1.3">
    {d3_class.replace("_"," ")}</div>
  <div style="font-size:10px;color:rgba(255,255,255,0.50);margin-top:2px">{d3_riesgo}</div>
  <div style="display:flex;gap:8px;margin-top:6px">
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">AVEP-D3</div>
      <div style="font-size:14px;font-weight:700;color:#E2E8F0">{d3_score:.0f}</div>
    </div>
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">conf</div>
      <div style="font-size:14px;font-weight:700;color:{d3_cc}">{d3_conf:.0%}</div>
    </div>
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">ew</div>
      <div style="font-size:12px;font-weight:600;color:rgba(255,255,255,0.55)">{d3_ew:.0%}</div>
    </div>
  </div>
  {d3_insuf_note}
</div>""", unsafe_allow_html=True)

    with col_d4:
        d4_cc = _conf_color(d4_conf)
        irs_color = (
            "#E53E3E" if d4_irs >= 70 else
            "#E67E22" if d4_irs >= 50 else
            "#D69E2E" if d4_irs >= 30 else
            "#38A169"
        )
        st.markdown(f"""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.10);
            border-radius:8px;padding:10px 12px">
  <div style="font-size:8px;font-weight:700;color:rgba(255,255,255,0.35);
              text-transform:uppercase;letter-spacing:0.06em">D4 Territorial</div>
  <div style="font-size:11px;font-weight:700;color:#E2E8F0;margin-top:4px;line-height:1.3">
    {d4_pat.replace("_"," ")}</div>
  <div style="font-size:10px;color:rgba(255,255,255,0.50);margin-top:2px">{d4_riesgo}</div>
  <div style="display:flex;gap:8px;margin-top:6px">
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">IRS</div>
      <div style="font-size:14px;font-weight:700;color:{irs_color}">{d4_irs:.1f}</div>
    </div>
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">AVEP-D4</div>
      <div style="font-size:14px;font-weight:700;color:#E2E8F0">{d4_score:.0f}</div>
    </div>
    <div>
      <div style="font-size:8px;color:rgba(255,255,255,0.30)">conf</div>
      <div style="font-size:14px;font-weight:700;color:{d4_cc}">{d4_conf:.0%}</div>
    </div>
  </div>
  <div style="font-size:8px;color:rgba(255,255,255,0.35);margin-top:3px">
    Rezago critico: {d4_ncrit} parroquia(s)</div>
</div>""", unsafe_allow_html=True)

    # ── Narrativa ─────────────────────────────────────────────────────────────
    if narrative:
        st.markdown(
            f'<div style="font-size:10px;color:rgba(255,255,255,0.60);'
            f'padding:7px 10px;margin:5px 0 2px;'
            f'background:rgba(255,255,255,0.02);border-radius:6px;line-height:1.5">'
            f'{narrative[:400]}</div>',
            unsafe_allow_html=True,
        )

    # ── Expander: evidencias auditables ───────────────────────────────────────
    with st.expander(
        f"Evidencias D3xD4 · EED={eed_score:+.1f} · conf_cruce={cross_conf:.0%}",
        expanded=False,
    ):
        if evidence:
            st.markdown(
                '<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
                'margin-bottom:4px">CADENA DE EVIDENCIA (auditable)</div>',
                unsafe_allow_html=True,
            )
            for ev in evidence:
                st.markdown(
                    f'<div style="font-size:10px;color:rgba(255,255,255,0.55);'
                    f'padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.04)">'
                    f'· {ev}</div>',
                    unsafe_allow_html=True,
                )
        # ── Marco normativo cruzado D3xD4 ────────────────────────────────────
        try:
            from sentinel.d3d4_normative import bind_cross_from_dict, summarize_d3d4_normative
            _cnorm = bind_cross_from_dict(cross_dict)
            if _cnorm.overall_tier != "sin_tension":
                _tier_colors = {
                    "severa":    "#E53E3E",
                    "moderada":  "#E67E22",
                    "potencial": "#D69E2E",
                }
                _tc = _tier_colors.get(_cnorm.overall_tier, "#D69E2E")

                st.markdown(
                    f'<div style="font-size:9px;font-weight:700;color:{_tc};'
                    f'margin-top:10px;margin-bottom:4px;letter-spacing:0.06em">'
                    f'MARCO NORMATIVO D3xD4 — {_cnorm.overall_tier.upper()}'
                    + (' [OBSERVACIONAL]' if _cnorm.observational_only else '') +
                    '</div>',
                    unsafe_allow_html=True,
                )

                # Referencias normativas
                for r in _cnorm.refs:
                    _rv_color = "#48BB78" if r.verificado else "rgba(255,255,255,0.35)"
                    _rv_badge = "✓" if r.verificado else "?"
                    _ref_tc   = _tier_colors.get(r.tier, "#D69E2E")
                    st.markdown(
                        f'<div style="border-left:3px solid {_ref_tc};padding:4px 8px;'
                        f'margin:3px 0;background:rgba(255,255,255,0.02);border-radius:0 4px 4px 0">'
                        f'<span style="font-size:8px;font-weight:700;color:{_ref_tc}">'
                        f'{r.law} {r.article}</span>'
                        f'<span style="font-size:7px;color:{_rv_color};margin-left:5px">{_rv_badge}</span>'
                        f'<div style="font-size:9px;color:rgba(255,255,255,0.55);margin-top:1px">'
                        f'{r.topic}</div></div>',
                        unsafe_allow_html=True,
                    )

                # Matriz PDOT contradicción
                _pdot_c = _cnorm.pdot_contradiction
                if _pdot_c.get("rows"):
                    st.markdown(
                        '<div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.30);'
                        'margin-top:8px;margin-bottom:3px">MATRIZ PDOT — CONTRADICCION</div>',
                        unsafe_allow_html=True,
                    )
                    for _row in _pdot_c["rows"]:
                        _row_color = _tier_colors.get(_row["nivel"], "rgba(255,255,255,0.35)")
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;'
                            f'padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.05)">'
                            f'<span style="font-size:8px;color:rgba(255,255,255,0.40)">'
                            f'{_row["dimension"]}</span>'
                            f'<span style="font-size:8px;font-weight:700;color:{_row_color}">'
                            f'{_row["brecha"]}</span></div>',
                            unsafe_allow_html=True,
                        )

        except ImportError:
            pass  # d3d4_normative aun no disponible

        st.markdown(
            '<div style="font-size:8px;color:rgba(255,255,255,0.22);margin-top:6px;'
            'font-style:italic">'
            'El cruce D3xD4 produce hipotesis institucionales — no veredictos. '
            'La autoridad publica determina implicancias y acciones correctivas.'
            '</div>',
            unsafe_allow_html=True,
        )


# ── 14. INFERENCE REVIEW CARD (RC-CORE) ───────────────────────────────────────

def inference_review_card(flag_dict: dict) -> None:
    """
    Tarjeta de aviso institucional: el sistema detectó que una inferencia
    requiere validación humana antes de elevar tensión normativa.

    Argumentos:
        flag_dict — dict serializado de InferenceReviewFlag (de get_active_flags())

    Doctrina: este card no toma decisiones — informa que la complejidad
    de la evidencia supera el umbral de autonomía del sistema.
    La autoridad institucional es quien valida.
    """
    if not flag_dict:
        return

    cross_pattern = flag_dict.get("cross_pattern", "DESCONOCIDO")
    cross_conf    = float(flag_dict.get("cross_conf", 0.0))
    irs           = float(flag_dict.get("irs", 0.0))
    eed           = float(flag_dict.get("eed", 0.0))
    obs           = bool(flag_dict.get("observational", True))
    reason        = flag_dict.get("reason", "")
    flag_id       = flag_dict.get("flag_id", "")
    contracts     = flag_dict.get("rc_contracts", [])
    ts            = flag_dict.get("timestamp", "")
    rule          = int(flag_dict.get("trigger_rule", 1))
    ack           = bool(flag_dict.get("acknowledged", False))

    # Color según si ya fue reconocido
    _bg     = "rgba(56,161,105,0.08)"  if ack else "rgba(230,126,34,0.10)"
    _border = "rgba(56,161,105,0.35)"  if ack else "rgba(230,126,34,0.40)"
    _color  = "#38A169"                if ack else "#E67E22"
    _icon   = "✅"                     if ack else "⚠️"
    _title  = "Revisión Institucional Completada" if ack else "Revisión Institucional Requerida"

    obs_tag = " · OBSERVACIONAL" if obs else " · CONFIRMADO"
    rule_labels = {
        1: "Patrón D3×D4 crítico confirmado",
        2: "Evidencia D4 abrumadora con SATs críticos",
        3: "Divergencia temporal-territorial severa (EED)",
    }
    rule_label = rule_labels.get(rule, f"Regla {rule}")

    st.markdown(
        f'<div style="background:{_bg};border:1px solid {_border};'
        f'border-left:4px solid {_color};border-radius:10px;'
        f'padding:14px 16px;margin:10px 0 6px;'
        f'font-family:Inter,-apple-system,sans-serif">'
        # Header
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
        f'<span style="font-size:10px;font-weight:700;color:{_color};letter-spacing:.06em">'
        f'{_icon} {_title.upper()}</span>'
        f'<span style="font-size:8px;color:rgba(255,255,255,0.40)">'
        f'FLAG {flag_id} · {ts[:16]}</span></div>'
        # Patrón + regla
        f'<div style="font-size:12px;font-weight:600;color:rgba(255,255,255,0.85);margin-bottom:4px">'
        f'{cross_pattern}{obs_tag}</div>'
        f'<div style="font-size:9px;color:rgba(255,255,255,0.50);margin-bottom:8px">'
        f'Regla activada: {rule_label}</div>'
        # Métricas
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px">'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">CROSS CONF</div>'
        f'<div style="font-size:13px;font-weight:700;color:{_color}">{cross_conf:.2%}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">IRS</div>'
        f'<div style="font-size:13px;font-weight:700;color:#E53E3E">{irs:.1f}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">EED</div>'
        f'<div style="font-size:13px;font-weight:700;color:#00D4FF">{eed:+.1f}</div></div>'
        f'</div>'
        # Reason
        f'<div style="font-size:9px;color:rgba(255,255,255,0.55);margin-bottom:8px;'
        f'padding:6px 8px;background:rgba(0,0,0,0.15);border-radius:6px;line-height:1.5">'
        f'{reason[:200]}{"..." if len(reason) > 200 else ""}</div>'
        # Contratos
        f'<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px">'
        + "".join(
            f'<span style="background:rgba(0,0,0,0.25);border-radius:4px;'
            f'padding:2px 6px;font-size:7.5px;color:rgba(255,255,255,0.50)">'
            f'{c}</span>'
            for c in contracts
        )
        + f'</div>'
        # Doctrina
        f'<div style="font-size:8px;color:rgba(255,255,255,0.28);'
        f'border-top:1px solid rgba(255,255,255,0.08);padding-top:6px;font-style:italic">'
        f'El sistema informa — la autoridad publica valida y decide sobre las implicancias institucionales.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Botón de reconocimiento (fuera del HTML para interactividad Streamlit)
    if not ack:
        _btn_key = f"ack_{flag_id}_{id(flag_dict)}"
        if st.button(
            f"Reconocer flag {flag_id}",
            key=_btn_key,
            help="Confirmar que este aviso fue recibido y revisado por el equipo institucional.",
        ):
            try:
                from sentinel.human_review import acknowledge_flag
                acknowledge_flag(flag_id)
                st.rerun()
            except Exception:
                pass


# ── 15. RC-D1 LEGALIDAD CARD ──────────────────────────────────────────────────

def d1_card(d1_dict: dict) -> None:
    """
    Tarjeta RC-D1 Legalidad — coherencia normativa institucional.

    Argumentos:
        d1_dict — output de summarize_d1() (sentinel.d1_engine)

    Doctrina: D1 informa hipótesis de coherencia — no emite veredictos.
    "El sistema informa — la autoridad pública decide."
    """
    if not d1_dict:
        return

    entity_id    = d1_dict.get("entity_id", "")
    status       = d1_dict.get("status_global", "OBSERVADO")
    confidence   = float(d1_dict.get("confidence", 0.0))
    obs          = bool(d1_dict.get("observational", True))
    needs_review = bool(d1_dict.get("needs_review", False))
    d3_pattern   = d1_dict.get("d3_pattern", "")
    d4_pattern   = d1_dict.get("d4_pattern", "")
    sat_codes    = d1_dict.get("sat_codes", [])
    n_risks      = int(d1_dict.get("n_risks", 0))
    top_action   = d1_dict.get("top_action", "")
    top_approver = d1_dict.get("top_approver", "")
    counterfactual = d1_dict.get("top_counterfactual", "")
    norm_refs    = d1_dict.get("top_norm_refs", [])
    gaps         = d1_dict.get("top_evidence_gaps", [])
    proc_overdue = d1_dict.get("proc_overdue", [])
    narrative    = d1_dict.get("narrative", "")

    # Paleta por status D1
    _STATUS_PALETTE = {
        "LEGAL":                   ("#38A169", "rgba(56,161,105,0.08)",  "rgba(56,161,105,0.35)",  "✅"),
        "OBSERVADO":               ("#00D4FF", "rgba(0,212,255,0.06)",   "rgba(0,212,255,0.20)",   "ℹ️"),
        "RIESGO_DE_EVIDENCIA":     ("#D69E2E", "rgba(214,158,46,0.08)",  "rgba(214,158,46,0.30)",  "⚡"),
        "RIESGO_DE_PROCEDIMIENTO": ("#E67E22", "rgba(230,126,34,0.10)",  "rgba(230,126,34,0.35)",  "⚠️"),
        "RIESGO_DE_COMPETENCIA":   ("#E53E3E", "rgba(229,62,62,0.12)",   "rgba(229,62,62,0.40)",   "🚨"),
        "REQUIERE_REVIEW":         ("#9B59B6", "rgba(155,89,182,0.12)",  "rgba(155,89,182,0.40)",  "🔍"),
    }
    _color, _bg, _border, _icon = _STATUS_PALETTE.get(
        status, ("#00D4FF", "rgba(0,212,255,0.06)", "rgba(0,212,255,0.20)", "ℹ️")
    )

    obs_tag = " [OBSERVACIONAL]" if obs else ""
    rev_tag = " · REQUIERE REVISIÓN HUMANA" if needs_review else ""

    st.markdown(
        f'<div style="background:{_bg};border:1px solid {_border};'
        f'border-left:4px solid {_color};border-radius:10px;'
        f'padding:14px 16px;margin:10px 0 6px;'
        f'font-family:Inter,-apple-system,sans-serif">'
        # Header
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
        f'<span style="font-size:10px;font-weight:700;color:{_color};letter-spacing:.06em">'
        f'{_icon} RC-D1 LEGALIDAD — {entity_id}</span>'
        f'<span style="font-size:8px;color:rgba(255,255,255,0.40)">'
        f'conf={confidence:.0%}{obs_tag}</span></div>'
        # Status
        f'<div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.90);margin-bottom:2px">'
        f'{status}{rev_tag}</div>'
        # Patrones activadores
        f'<div style="font-size:9px;color:rgba(255,255,255,0.45);margin-bottom:8px">'
        f'D3: {d3_pattern} · D4: {d4_pattern}</div>'
        # KPIs
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px">'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">RIESGOS</div>'
        f'<div style="font-size:14px;font-weight:700;color:{_color}">{n_risks}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">PROC. VENCIDOS</div>'
        f'<div style="font-size:14px;font-weight:700;color:#E53E3E">{len(proc_overdue)}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.40)">SAT D1</div>'
        f'<div style="font-size:10px;font-weight:700;color:#00D4FF">'
        f'{", ".join(sat_codes[:2]) if sat_codes else "—"}</div></div>'
        f'</div>'
        + (
            # Acción principal + aprobador
            f'<div style="font-size:9px;color:rgba(255,255,255,0.60);margin-bottom:6px;'
            f'padding:6px 8px;background:rgba(0,0,0,0.15);border-radius:6px;line-height:1.5">'
            f'<span style="color:rgba(255,255,255,0.35)">Acción: </span>{top_action} · '
            f'<span style="color:rgba(255,255,255,0.35)">Aprobador req.: </span>{top_approver[:40]}'
            f'</div>'
            if top_action else ""
        )
        + (
            # Normas aplicables
            f'<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px">'
            + "".join(
                f'<span style="background:rgba(0,0,0,0.25);border-radius:4px;'
                f'padding:2px 6px;font-size:7.5px;color:rgba(255,255,255,0.50)">'
                f'{n}</span>'
                for n in norm_refs[:4]
            )
            + f'</div>'
            if norm_refs else ""
        )
        + (
            # Brechas de evidencia
            f'<div style="font-size:8px;color:rgba(255,255,255,0.40);margin-bottom:6px;'
            f'padding:5px 8px;background:rgba(0,0,0,0.12);border-radius:6px">'
            f'<span style="color:rgba(255,255,255,0.30)">Brechas:</span> '
            + " · ".join(g[:60] for g in gaps[:2])
            + ("..." if len(gaps) > 2 else "")
            + f'</div>'
            if gaps else ""
        )
        + (
            # Ventanas procedimentales vencidas
            f'<div style="font-size:8px;color:#E53E3E;margin-bottom:6px;'
            f'padding:5px 8px;background:rgba(229,62,62,0.08);border-radius:6px">'
            f'⏰ Plazo vencido: {", ".join(proc_overdue[:3])}</div>'
            if proc_overdue else ""
        )
        + (
            # Counterfactual
            f'<div style="font-size:8px;color:rgba(56,161,105,0.85);margin-bottom:6px;'
            f'padding:5px 8px;background:rgba(56,161,105,0.06);border-radius:6px;line-height:1.5">'
            f'<span style="color:rgba(56,161,105,0.60)">Ruta LEGAL: </span>'
            f'{counterfactual[:150]}{"..." if len(counterfactual) > 150 else ""}</div>'
            if counterfactual and status not in ("LEGAL", "OBSERVADO") else ""
        )
        + f'<div style="font-size:8px;color:rgba(255,255,255,0.28);'
        f'border-top:1px solid rgba(255,255,255,0.08);padding-top:6px;font-style:italic">'
        f'D1 produce hipótesis de coherencia normativa — no veredictos. '
        f'El sistema informa — la autoridad pública decide.'
        f'</div></div>',
        unsafe_allow_html=True,
    )


# ── 16. RC-D1.3 COHERENCIA ESTRATÉGICA CARD ──────────────────────────────────

def d1_coherence_card(d13_dict: dict) -> None:
    """
    Tarjeta RC-D1.3 Normative Coherence — coherencia estratégica PDOT ↔ ejecución.

    Argumentos:
        d13_dict — output de summarize_coherence() (sentinel.d1_coherence)

    Núcleo: detecta si el municipio ejecuta lo que dijo que era prioritario.
    "El sistema informa — la autoridad pública decide."
    """
    if not d13_dict:
        return
    status       = d13_dict.get("status", "EVIDENCIA_INSUFICIENTE")
    confidence   = float(d13_dict.get("confidence", 0.0))
    obs          = bool(d13_dict.get("observational", True))
    irs_actual   = float(d13_dict.get("irs_actual", 0.0))
    irs_meta     = float(d13_dict.get("irs_meta", 45.0))
    irs_delta    = float(d13_dict.get("irs_delta", 0.0))
    comp_gap     = float(d13_dict.get("composite_gap", 0.0))
    t_gap        = float(d13_dict.get("territorial_gap", 0.0))
    e_gap        = float(d13_dict.get("execution_gap", 0.0))
    n_commit     = int(d13_dict.get("n_commitments", 0))
    sat_code     = d13_dict.get("sat_code", "")
    hypothesis   = d13_dict.get("hypothesis", "")
    counterfactual = d13_dict.get("counterfactual", "")
    entity_id    = d13_dict.get("entity_id", "")
    d3_pattern   = d13_dict.get("d3_pattern", "")
    d4_pattern   = d13_dict.get("d4_pattern", "")

    _STATUS_PALETTE = {
        "ALINEADO":               ("#38A169", "rgba(56,161,105,0.08)",  "rgba(56,161,105,0.35)",  "✅"),
        "EVIDENCIA_INSUFICIENTE": ("#718096", "rgba(113,128,150,0.08)", "rgba(113,128,150,0.30)", "📋"),
        "DESVIACION_MENOR":       ("#D69E2E", "rgba(214,158,46,0.08)",  "rgba(214,158,46,0.30)",  "⚡"),
        "DESVIACION_ESTRATEGICA": ("#E67E22", "rgba(230,126,34,0.10)",  "rgba(230,126,34,0.35)",  "⚠️"),
        "CONTRADICCION_CRITICA":  ("#E53E3E", "rgba(229,62,62,0.12)",   "rgba(229,62,62,0.40)",   "🚨"),
    }
    _color, _bg, _border, _icon = _STATUS_PALETTE.get(
        status, ("#718096", "rgba(113,128,150,0.08)", "rgba(113,128,150,0.30)", "📋")
    )
    obs_tag   = " [OBS]" if obs else ""
    delta_str = f"{irs_delta:+.1f}" if irs_delta != 0 else "0.0"
    delta_col = "#E53E3E" if irs_delta > 0 else "#38A169"

    st.markdown(
        f'<div style="background:{_bg};border:1px solid {_border};'
        f'border-left:4px solid {_color};border-radius:10px;'
        f'padding:14px 16px;margin:10px 0 6px;'
        f'font-family:Inter,-apple-system,sans-serif">'
        # Header
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">'
        f'<span style="font-size:10px;font-weight:700;color:{_color};letter-spacing:.06em">'
        f'{_icon} RC-D1.3 COHERENCIA PDOT — {entity_id}</span>'
        f'<span style="font-size:8px;color:rgba(255,255,255,0.40)">conf={confidence:.0%}{obs_tag}</span>'
        f'</div>'
        # Status
        f'<div style="font-size:13px;font-weight:700;color:rgba(255,255,255,0.90);margin-bottom:2px">'
        f'{status}</div>'
        f'<div style="font-size:9px;color:rgba(255,255,255,0.45);margin-bottom:10px">'
        f'D3: {d3_pattern} · D4: {d4_pattern}</div>'
        # KPIs: IRS actual / meta / delta
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:10px">'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:7.5px;color:rgba(255,255,255,0.40)">IRS ACTUAL</div>'
        f'<div style="font-size:14px;font-weight:700;color:#E53E3E">{irs_actual:.1f}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:7.5px;color:rgba(255,255,255,0.40)">META PDOT 2027</div>'
        f'<div style="font-size:14px;font-weight:700;color:#38A169">≤{irs_meta:.0f}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:7.5px;color:rgba(255,255,255,0.40)">DELTA</div>'
        f'<div style="font-size:14px;font-weight:700;color:{delta_col}">{delta_str}</div></div>'
        f'<div style="background:rgba(0,0,0,0.20);border-radius:6px;padding:6px;text-align:center">'
        f'<div style="font-size:7.5px;color:rgba(255,255,255,0.40)">GAP COMP.</div>'
        f'<div style="font-size:14px;font-weight:700;color:{_color}">{comp_gap:.0%}</div></div>'
        f'</div>'
        # Barra de brechas
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:8px">'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.45)">'
        f'Brecha territorial: <span style="color:{_color};font-weight:600">{t_gap:.0%}</span></div>'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.45)">'
        f'Brecha ejecución: <span style="color:{_color};font-weight:600">{e_gap:.0%}</span></div>'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.45)">'
        f'Compromisos PDOT activos: <span style="color:#00D4FF;font-weight:600">{n_commit}</span></div>'
        f'<div style="font-size:8px;color:rgba(255,255,255,0.45)">'
        f'SAT D1.3: <span style="color:#E67E22;font-weight:600">{sat_code if sat_code else "—"}</span></div>'
        f'</div>'
        + (
            # Hipótesis institucional (el corazón de D1.3)
            f'<div style="font-size:9px;color:rgba(255,255,255,0.75);margin-bottom:8px;'
            f'padding:8px 10px;background:rgba(0,0,0,0.18);border-radius:6px;'
            f'border-left:3px solid {_color};line-height:1.6">'
            f'<span style="font-size:7.5px;color:rgba(255,255,255,0.35);display:block;margin-bottom:3px">'
            f'HIPOTESIS INSTITUCIONAL</span>'
            f'{hypothesis[:250]}{"..." if len(hypothesis) > 250 else ""}</div>'
            if hypothesis and status not in ("ALINEADO", "EVIDENCIA_INSUFICIENTE") else ""
        )
        + (
            # Ruta de alineamiento
            f'<div style="font-size:8px;color:rgba(56,161,105,0.85);margin-bottom:6px;'
            f'padding:6px 8px;background:rgba(56,161,105,0.06);border-radius:6px;line-height:1.5">'
            f'<span style="color:rgba(56,161,105,0.60)">Ruta PDOT: </span>'
            f'{counterfactual[:180]}{"..." if len(counterfactual) > 180 else ""}</div>'
            if counterfactual and status not in ("ALINEADO", "EVIDENCIA_INSUFICIENTE") else ""
        )
        + f'<div style="font-size:8px;color:rgba(255,255,255,0.28);'
        f'border-top:1px solid rgba(255,255,255,0.08);padding-top:6px;font-style:italic">'
        f'D1.3 detecta contradicciones institucionales entre compromisos PDOT y comportamiento material. '
        f'No acusa — produce hipótesis auditadas. El sistema informa — la autoridad decide.'
        f'</div></div>',
        unsafe_allow_html=True,
    )
