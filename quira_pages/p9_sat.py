"""
QUIRA OS v0.1 — P-09 Alertas SAT Preventivas
Sistema de Alertas Tempranas · SIAP-ICPI · Fiel al DEMO.html P-09
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all, get_sat_counts
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── MATRIZ DE RIESGO INSTITUCIONAL ────────────────────────────────────────────
RIESGO_MATRIX = [
    {
        "categoria": "Riesgo Fiscal",
        "nivel": "CRÍTICO",
        "color": "red",
        "items": [
            "ISP 14.58% bajo umbral COOTAD 65% · bloquea perfil BDE",
            "Presupuesto total $26.7M · ejecutado Q1 solo $7.8M (29.3%)",
        ],
    },
    {
        "categoria": "Riesgo Contractual",
        "nivel": "CRÍTICO",
        "color": "red",
        "items": [
            "4 metas PDOT sin contrato PAC activo · SAT-0",
            "24 procesos sin evidencia SHA-256 · Gasto Ciego C4",
        ],
    },
    {
        "categoria": "Riesgo de Transparencia",
        "nivel": "ALERTA",
        "color": "amber",
        "items": [
            "Patrón fragmentación selectiva DAPS-01 · LOSNCP",
            "IOC 17.71% · LOTAIP parcialmente actualizado",
        ],
    },
    {
        "categoria": "Riesgo Participativo",
        "nivel": "ALERTA",
        "color": "amber",
        "items": [
            "IGP 27.98% · CPCCS V=0 en RDC 2026",
            "2 parroquias sin voz: Isabel Muentes · Aníbal San Andrés",
        ],
    },
]


def _sat_card(sat: dict) -> str:
    """Tarjeta HTML para una SAT."""
    col   = "red" if sat["nivel"] == "CRÍTICO" else "amber"
    badge = (
        '<span class="badge badge-red">🔴 CRÍTICO</span>'
        if sat["nivel"] == "CRÍTICO"
        else '<span class="badge badge-amber">🟠 ALERTA</span>'
    )
    estado_badge = (
        '<span style="font-size:9px;font-weight:700;color:var(--red);'
        'background:rgba(255,77,109,.1);border-radius:4px;padding:2px 7px">ACTIVA</span>'
        if sat["estado"] == "ACTIVA"
        else
        '<span style="font-size:9px;font-weight:700;color:var(--amber);'
        'background:rgba(255,184,0,.1);border-radius:4px;padding:2px 7px">PREVENTIVA</span>'
    )

    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-top:3px solid var(--{col});border-radius:12px;
            padding:16px;margin-bottom:12px">
  <!-- Cabecera -->
  <div style="display:flex;justify-content:space-between;align-items:flex-start;
              margin-bottom:10px">
    <div style="display:flex;align-items:center;gap:10px">
      <div style="font-size:22px;font-weight:900;color:var(--{col});
                  font-family:var(--mono);letter-spacing:-.02em">{sat["id"]}</div>
      <div>
        <div style="font-size:13px;font-weight:700;color:var(--white)">{sat["nombre"]}</div>
        <div style="display:flex;gap:6px;margin-top:3px">{badge} {estado_badge}</div>
      </div>
    </div>
    <div style="text-align:right">
      <div style="font-size:18px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">{sat["impacto"].split("·")[0].strip()}</div>
      <div style="font-size:9px;color:var(--muted)">impacto ICGI-T</div>
    </div>
  </div>

  <!-- Descripción -->
  <div style="font-size:11px;color:var(--muted);padding:8px 10px;
              background:rgba(255,255,255,.03);border-radius:7px;margin-bottom:8px">
    {sat["descripcion"]}
  </div>

  <!-- Impacto full -->
  <div style="font-size:10px;color:var(--{col});padding:6px 10px;
              background:rgba(255,77,109,.05) if col=='red' else rgba(255,184,0,.05);
              border-left:2px solid var(--{col});margin-bottom:8px">
    ⚡ Impacto: {sat["impacto"]}
  </div>

  <!-- Acción recomendada -->
  <div style="display:flex;align-items:flex-start;gap:8px;padding:8px 10px;
              background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);
              border-radius:7px">
    <span style="color:var(--cyan);font-size:11px">▶</span>
    <span style="font-size:11px;color:var(--cyan);font-weight:600">{sat["accion"]}</span>
  </div>
</div>"""


def _riesgo_card(r: dict) -> str:
    col = r["color"]
    items_html = "".join(
        f'<div style="font-size:10px;color:var(--white);padding:4px 8px;'
        f'background:rgba(255,255,255,.03);border-radius:5px;margin-bottom:4px">'
        f'{"🔴" if col=="red" else "🟠"} {item}</div>'
        for item in r["items"]
    )
    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-left:3px solid var(--{col});border-radius:10px;padding:12px">
  <div style="font-size:10px;font-weight:700;color:var(--{col});
              text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px">
    {r["categoria"]} · {r["nivel"]}
  </div>
  {items_html}
</div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    sat_list  = data["sat"]
    counts    = get_sat_counts(data)

    n_crit  = counts["criticos"]
    n_alert = counts["alertas"]
    n_total = counts["total"]

    # ── RESUMEN HEADER ────────────────────────────────────────────────────────
    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{n_crit}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">SATs CRÍTICAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Acción inmediata requerida</div>
  </div>
  <div style="background:rgba(255,184,0,.08);border:1px solid rgba(255,184,0,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{n_alert}</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">SATs ALERTA</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Preventivas · monitoreo activo</div>
  </div>
  <div style="background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--white);
                font-family:var(--mono)">{n_total}</div>
    <div style="font-size:10px;font-weight:700;color:var(--muted);margin-top:4px">TOTAL SATs</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Sistema de alertas Q1-2026</div>
  </div>
  <div style="background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">−16.4</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">PTS ICGI-T</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Impacto acumulado SATs</div>
  </div>
</div>"""

    # ── ALERTA CONTRALORÍA ────────────────────────────────────────────────────
    alerta_ctrl = """
<div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.35);
            border-radius:12px;padding:14px 16px;margin-bottom:16px;
            display:flex;align-items:flex-start;gap:12px">
  <div style="font-size:28px">⚠️</div>
  <div>
    <div style="font-size:12px;font-weight:700;color:var(--red);margin-bottom:4px">
      RIESGO CONTRALORÍA GENERAL DEL ESTADO · Sin acción en Q2-2026
    </div>
    <div style="font-size:11px;color:var(--muted);line-height:1.6">
      Las SATs críticas activas (SAT-0 y SAT-IV) generan riesgo de observación formal
      por parte de la Contraloría. La falta de evidencias SHA-256 en 24 procesos
      y el ISP 14.58% bajo umbral COOTAD 65% pueden derivar en
      <strong style="color:var(--white)">glosas contables y bloqueo de crédito BDE</strong>
      si no se regulariza antes del cierre del primer semestre 2026.
    </div>
  </div>
</div>"""

    # ── TARJETAS SAT ──────────────────────────────────────────────────────────
    sat_cards = f"""
<div class="card">
  <div class="card-title">🚨 SATs ACTIVAS · Detalle y Acciones</div>
  {"".join(_sat_card(s) for s in sat_list)}
</div>"""

    # ── MATRIZ RIESGO ─────────────────────────────────────────────────────────
    riesgo_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">📊 MATRIZ DE RIESGO INSTITUCIONAL · Q1-2026</div>
  <div class="grid-2" style="gap:12px">
    {"".join(_riesgo_card(r) for r in RIESGO_MATRIX)}
  </div>
  <div style="margin-top:12px;font-size:10px;color:var(--muted);
              padding:8px 10px;background:rgba(0,212,255,.04);
              border:1px solid rgba(0,212,255,.1);border-radius:7px;line-height:1.6">
    💡 <strong style="color:var(--cyan)">Lógica SAT:</strong>
    El sistema detecta patrones de desviación antes de que se conviertan en crisis.
    Una SAT PREVENTIVA activa significa que el algoritmo identificó señales de riesgo
    en los datos de POA·PAC·eSIGEF — no espera a que el problema sea visible.
  </div>
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑤ ALERTAS SAT",
        "Sistema de Alertas Tempranas",
        f"{n_crit} SATs Críticas · {n_alert} SATs Alerta · Impacto acumulado −16.4 pts ICGI-T · Q1-2026",
        f'<span class="badge badge-red">🚨 {n_crit} CRÍTICAS ACTIVAS</span>',
    )

    html = hdr + resumen_html + alerta_ctrl + sat_cards + riesgo_html

    render_page(html, show_tech=show_tech, height=2200)

    # ── CTAs Streamlit ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · ¿Cómo desactivar las SATs?",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El GAD de Montecristi tiene 2 SATs críticas activas: "
                "SAT-0 (4 metas sin contrato PAC, 24 procesos sin evidencia SHA-256) "
                "y SAT-IV (ISP 14.58% bajo umbral COOTAD 65%). "
                "¿Cuál es el protocolo de desactivación más rápido para cada una "
                "y qué área administrativa debe liderar cada acción?"
            )
            st.rerun()
    with c2:
        if st.button("📉 Ver Causas de la Brecha", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c3:
        if st.button("🎯 Ver Metas PDOT", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
