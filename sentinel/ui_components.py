"""
SENTINEL · ui_components.py
Componentes de UI generativa — Sentinel v2 / Sprint 1-7.
Alert · Nav · Evidence · KPI Mini · Scenario · Simulation · Trust · Legal · QUADRUM · RC-7.3.
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
