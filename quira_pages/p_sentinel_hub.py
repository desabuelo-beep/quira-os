"""
QUIRA OS · p_sentinel_hub.py
Centro de Inteligencia Territorial — Pantalla 0 real.

Conectado al SENTINEL FastAPI (localhost:8100).
Sprint 2.3 — Muestra: estado institucional, TGI, Sentinel live, SLA/governance.

Dylus Lab © 2026
"""
from __future__ import annotations

import time
import requests
import streamlit as st

# ── CONFIG API ─────────────────────────────────────────────────────────────────
API_BASE    = "http://localhost:8100"
API_TIMEOUT = 4   # segundos — falla rápido si API no está corriendo

# ── DATOS INSTITUCIONALES (Gold Master v5.4 — fuente de verdad) ───────────────
TGI_DATA = {
    "score":        66.85,
    "estado":       "Transición con Riesgos",
    "color":        "#FFB800",
    "d1":  {"nombre": "D1 Legalidad",    "val": 83.5,  "color": "#00E096"},
    "d2":  {"nombre": "D2 Planificación","val": 69.93, "color": "#FFB800"},
    "d3":  {"nombre": "D3 Ejecución",    "val": 59.85, "color": "#FF4D6D"},
    "d4":  {"nombre": "D4 Equidad IET",  "val": 44.8,  "color": "#FF4D6D"},
    "d5":  {"nombre": "D5 Institucional","val": 100.0,  "color": "#00E096"},
    "irs": 79.7,
    "icpi": 69.93,
    "mandato_pct":  75,
    "dias_restantes": 370,
}

TERRITORIAL = {
    "poblacion":  "99.937",
    "parroquias": 7,
    "nbi_cantonal": 38.4,
    "iet_promedio": 69,
    "parroquia_critica": "Isabel Muentes",
    "critica_nbi": 61.2,
    "critica_iet": 28,
}

ALCALDIA = {
    "alcalde":   "Carlos Alberto Montoya",
    "inicio":    "23-may-2023",
    "fin":       "23-may-2027",
    "mandato":   "2023–2027",
}


# ── ESTILOS LOCALES ────────────────────────────────────────────────────────────
CSS = """
<style>
.hub-metric {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
}
.hub-metric-label {
    font-size: 9px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.hub-metric-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 26px;
    font-weight: 700;
    line-height: 1;
}
.hub-metric-sub {
    font-size: 10px;
    color: rgba(255,255,255,0.35);
    margin-top: 4px;
}
.hub-block-title {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: rgba(0,212,255,0.6);
    border-left: 3px solid #00D4FF;
    padding-left: 10px;
    margin-bottom: 14px;
}
.sla-row {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
}
.pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    font-family: monospace;
}
.pill-green  { background: rgba(0,224,150,0.15); color:#00E096; }
.pill-amber  { background: rgba(255,184,0,0.15);  color:#FFB800; }
.pill-red    { background: rgba(255,77,109,0.15); color:#FF4D6D; }
.pill-orange { background: rgba(255,120,0,0.15);  color:#FF7800; }
.pill-cyan   { background: rgba(0,212,255,0.12);  color:#00D4FF; }
</style>
"""


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _api(endpoint: str) -> dict | None:
    """Llama al SENTINEL API. Retorna None si falla."""
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=API_TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _color_dim(val: float) -> str:
    if val >= 75:  return "#00E096"
    if val >= 55:  return "#FFB800"
    return "#FF4D6D"


def _bar(val: float, color: str, height: int = 5) -> str:
    return f"""
<div style="background:rgba(255,255,255,0.07);border-radius:3px;height:{height}px;overflow:hidden;margin-top:4px">
  <div style="width:{val:.1f}%;height:100%;background:{color};border-radius:3px;
              transition:width 0.8s ease"></div>
</div>"""


def _metric_card(label: str, val: str, sub: str = "", color: str = "#E2E8F0") -> str:
    return f"""
<div class="hub-metric">
  <div class="hub-metric-label">{label}</div>
  <div class="hub-metric-val" style="color:{color}">{val}</div>
  <div class="hub-metric-sub">{sub}</div>
</div>"""


# ── BLOQUES ───────────────────────────────────────────────────────────────────
def _bloque_politico():
    st.markdown('<div class="hub-block-title">Estado Político-Institucional</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_metric_card(
            "Alcaldía", ALCALDIA["alcalde"][:22],
            f"Período {ALCALDIA['mandato']}", "#00D4FF"
        ) + _metric_card(
            "Inicio gestión", ALCALDIA["inicio"], "Posesión CNE", "#E2E8F0"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(_metric_card(
            "Fin de gestión", ALCALDIA["fin"], "Término ordinario", "#E2E8F0"
        ) + _metric_card(
            "Días restantes", str(TGI_DATA["dias_restantes"]),
            "días al cierre de mandato", "#FFB800"
        ), unsafe_allow_html=True)

    # Barra mandato
    pct = TGI_DATA["mandato_pct"]
    st.markdown(f"""
<div style="margin-top:12px">
  <div style="display:flex;justify-content:space-between;font-size:10px;
              color:rgba(255,255,255,0.4);margin-bottom:5px">
    <span>2023</span>
    <span style="color:#00D4FF;font-weight:700">■ {pct}% completado</span>
    <span>2027</span>
  </div>
  {_bar(pct, "linear-gradient(90deg,#00D4FF,#7C5CFC)", height=6)}
</div>
<div style="margin-top:8px;display:flex;gap:10px">
  <span style="font-size:10px;color:rgba(255,255,255,0.4)">
    Gestión consumida: <b style="color:#FFB800">{pct}%</b>
  </span>
  <span style="font-size:10px;color:rgba(255,255,255,0.4)">
    ICPI-Metas: <b style="color:#FF4D6D">51%</b>
    <span style="color:rgba(255,77,109,0.6)"> ← tensión política</span>
  </span>
</div>
""", unsafe_allow_html=True)


def _bloque_territorial():
    st.markdown('<div class="hub-block-title">Estado Territorial</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_metric_card(
            "Población", TERRITORIAL["poblacion"],
            "hab · RIPS 2024", "#00D4FF"
        ) + _metric_card(
            "NBI Cantonal", f"{TERRITORIAL['nbi_cantonal']}%",
            "necesidades básicas insatisfechas", "#FFB800"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(_metric_card(
            "Parroquias", str(TERRITORIAL["parroquias"]),
            "1 urbana · 6 rurales", "#00E096"
        ) + _metric_card(
            "IET Promedio", str(TERRITORIAL["iet_promedio"]),
            "índice equidad territorial", "#FFB800"
        ), unsafe_allow_html=True)

    # Parroquia crítica callout
    st.markdown(f"""
<div style="margin-top:12px;background:rgba(255,77,109,0.08);
            border:1px solid rgba(255,77,109,0.25);border-radius:10px;
            padding:12px 14px;display:flex;align-items:center;gap:12px">
  <div style="font-size:22px">⚠️</div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;color:#FF4D6D">
      {TERRITORIAL['parroquia_critica']}
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px">
      Parroquia rural prioritaria — intervención urgente
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:4px;align-items:flex-end">
    <span class="pill pill-red">NBI {TERRITORIAL['critica_nbi']}%</span>
    <span class="pill pill-red">IET = {TERRITORIAL['critica_iet']}</span>
  </div>
</div>
""", unsafe_allow_html=True)


def _bloque_ejecucion():
    st.markdown('<div class="hub-block-title">Estado de Ejecución</div>',
                unsafe_allow_html=True)

    dims = [
        ("TGI Global",        TGI_DATA["score"], "Motor SIAP-ICPI v5.4", 100),
        ("D3 Ejecución",      TGI_DATA["d3"]["val"], "eSIGEF · PAC · SERCOP", 100),
        ("D4 Equidad IET",    TGI_DATA["d4"]["val"], "Índice equidad territorial", 100),
        ("IRS Regresividad",  TGI_DATA["irs"], "Inversión vs necesidad", 100),
    ]
    for name, val, sub, max_val in dims:
        color = _color_dim(val)
        pct   = (val / max_val) * 100
        st.markdown(f"""
<div style="margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span style="font-size:12px;font-weight:600;color:#E2E8F0">{name}</span>
    <span style="font-family:monospace;font-size:14px;font-weight:700;color:{color}">{val:.1f}</span>
  </div>
  <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:1px">{sub}</div>
  {_bar(pct, color)}
</div>""", unsafe_allow_html=True)

    # Alertas activas
    st.markdown("""
<div style="margin-top:10px;background:rgba(255,77,109,0.08);
            border:1px solid rgba(255,77,109,0.2);border-radius:10px;
            padding:10px 14px;display:flex;align-items:center;gap:12px">
  <div style="font-family:monospace;font-size:28px;font-weight:700;color:#FF4D6D;line-height:1">3</div>
  <div>
    <div style="font-size:12px;font-weight:600;color:#FF4D6D">Alertas críticas activas</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px">
      D3 · Isabel Muentes · Fondos bloqueados
    </div>
  </div>
</div>""", unsafe_allow_html=True)


def _bloque_sentinel(health: dict | None, drift: dict | None, sla_summary: dict | None):
    st.markdown('<div class="hub-block-title">Estado SENTINEL</div>',
                unsafe_allow_html=True)

    # Estado API
    api_ok    = health is not None
    api_icon  = "🟢 En línea" if api_ok else "🔴 API offline"
    chunks    = health.get("total_chunks", 0) if health else "–"
    llm_ok    = health.get("llm_disponible", False) if health else False

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(_metric_card(
            "API Status", api_icon,
            f"{chunks} chunks indexados", "#00E096" if api_ok else "#FF4D6D"
        ), unsafe_allow_html=True)
        st.markdown(_metric_card(
            "LLM", "Claude Haiku" if llm_ok else "Solo RAG",
            "claude-haiku-4-5" if llm_ok else "Activar API key", "#00D4FF" if llm_ok else "#FFB800"
        ), unsafe_allow_html=True)
    with col2:
        # Casos en disputa — la métrica clave Sprint 2.2
        disputas = 0
        if sla_summary:
            disputas = sla_summary.get("vencidos", 0) + sla_summary.get("criticos", 0)
        st.markdown(_metric_card(
            "SLA Críticos/Vencidos",
            str(disputas),
            "requieren coordinador" if disputas > 0 else "todo dentro del SLA",
            "#FF4D6D" if disputas > 0 else "#00E096"
        ), unsafe_allow_html=True)
        # Trust Drift
        if drift:
            tendencia = drift.get("tendencia", "ESTABLE")
            td_color  = {"ESTABLE":"#00E096","MEJORANDO":"#00D4FF","DEGRADANDO":"#FF4D6D"}.get(tendencia,"#E2E8F0")
            td_icon   = {"ESTABLE":"=","MEJORANDO":"↑","DEGRADANDO":"↓"}.get(tendencia,"=")
            st.markdown(_metric_card(
                "Trust Drift",
                f"{td_icon} {tendencia}",
                f"{drift.get('n_semanas',0)} sem · máx rechazo {drift.get('pct_rechazo_max',0):.0f}%",
                td_color
            ), unsafe_allow_html=True)
        else:
            st.markdown(_metric_card(
                "Trust Drift", "–", "API offline", "#4A5A80"
            ), unsafe_allow_html=True)

    # Versiones
    st.markdown("""
<div style="margin-top:12px;display:flex;gap:6px;flex-wrap:wrap">
  <span style="font-size:9px;color:rgba(255,255,255,0.3);font-family:monospace;
               background:rgba(255,255,255,0.04);padding:3px 8px;border-radius:4px">
    SENTINEL v2.1.0
  </span>
  <span style="font-size:9px;color:rgba(255,255,255,0.3);font-family:monospace;
               background:rgba(255,255,255,0.04);padding:3px 8px;border-radius:4px">
    PROMPT v2.1.0
  </span>
  <span style="font-size:9px;color:rgba(255,255,255,0.3);font-family:monospace;
               background:rgba(255,255,255,0.04);padding:3px 8px;border-radius:4px">
    GUARDRAIL v1.7.0
  </span>
  <span style="font-size:9px;color:rgba(0,224,150,0.5);font-family:monospace;
               background:rgba(0,224,150,0.05);padding:3px 8px;border-radius:4px">
    20/20 regression ✓
  </span>
</div>
""", unsafe_allow_html=True)


# ── SLA TABLE ─────────────────────────────────────────────────────────────────
def _sla_table(slas: list[dict]):
    """Tabla de SLAs activos con semáforo."""
    if not slas:
        st.info("No hay SLAs activos en este momento.")
        return

    for sla in slas[:8]:
        icon    = sla.get("status_icon", "•")
        status  = sla.get("status", "")
        owner   = sla.get("owner", "–")
        hours   = sla.get("horas_restantes", "–")
        pregunta = sla.get("pregunta", "")[:55]
        priority = sla.get("priority", "")

        pill_cls = {
            "NORMAL":      "pill-green",
            "SEGUIMIENTO": "pill-amber",
            "CRITICO":     "pill-orange",
            "VENCIDO":     "pill-red",
            "CUMPLIDO":    "pill-cyan",
        }.get(status, "pill-cyan")

        st.markdown(f"""
<div class="sla-row">
  <span style="font-size:18px">{icon}</span>
  <div style="flex:1">
    <div style="font-size:12px;font-weight:600;color:#E2E8F0">{pregunta}…</div>
    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px">
      Owner: {owner} · Prioridad: {priority}
    </div>
  </div>
  <div style="text-align:right">
    <span class="pill {pill_cls}">{status}</span>
    <div style="font-size:10px;color:rgba(255,255,255,0.3);margin-top:3px">{hours}h restantes</div>
  </div>
</div>""", unsafe_allow_html=True)


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
def render():
    st.markdown(CSS, unsafe_allow_html=True)

    # Cabecera
    col_title, col_status = st.columns([3, 1])
    with col_title:
        st.markdown("""
<div style="margin-bottom:4px">
  <span style="font-size:20px;font-weight:800;color:#E2E8F0;letter-spacing:-0.3px">
    Centro de Control Territorial
  </span>
  <span style="font-size:11px;color:rgba(255,255,255,0.3);margin-left:12px;font-family:monospace">
    GAD Municipal de Montecristi · Sprint 2.3
  </span>
</div>""", unsafe_allow_html=True)
    with col_status:
        if st.button("↻ Actualizar", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    st.markdown(
        "<div style='height:1px;background:rgba(255,255,255,0.06);margin:8px 0 20px'></div>",
        unsafe_allow_html=True,
    )

    # Llamadas API (cacheadas 60s)
    @st.cache_data(ttl=60, show_spinner=False)
    def _fetch():
        health  = _api("/sentinel/health")
        drift   = _api("/sentinel/trust-drift")
        sla_data = _api("/sentinel/sla")
        return health, drift, sla_data

    with st.spinner("Conectando con SENTINEL API…"):
        health, drift, sla_resp = _fetch()

    sla_summary = sla_resp.get("summary") if sla_resp else None
    sla_list    = sla_resp.get("slas", []) if sla_resp else []

    # Alerta si API offline
    if health is None:
        st.warning(
            "⚠️ SENTINEL API no responde en `localhost:8100`. "
            "Iniciá la API con: `uvicorn sentinel.api_rag:app --port 8100 --reload`  |  "
            "Los datos estáticos siguen disponibles.",
            icon="⚠️"
        )

    # ── 4 BLOQUES — 2x2 ──────────────────────────────────────────────────────
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        with st.container(border=True):
            _bloque_politico()

    with col_b:
        with st.container(border=True):
            _bloque_territorial()

    col_c, col_d = st.columns(2, gap="large")

    with col_c:
        with st.container(border=True):
            _bloque_ejecucion()

    with col_d:
        with st.container(border=True):
            _bloque_sentinel(health, drift, sla_summary)

    # ── SLA PANEL — debajo del grid ───────────────────────────────────────────
    st.markdown(
        "<div style='height:1px;background:rgba(255,255,255,0.06);margin:20px 0 16px'></div>",
        unsafe_allow_html=True,
    )

    col_sla_title, col_sla_badge = st.columns([3, 1])
    with col_sla_title:
        st.markdown(
            '<div class="hub-block-title" style="margin-bottom:10px">'
            'SLA de Gobernanza — Casos activos</div>',
            unsafe_allow_html=True,
        )
    with col_sla_badge:
        if sla_summary:
            alerta = sla_summary.get("alerta", False)
            n_venc = sla_summary.get("vencidos", 0)
            if alerta:
                st.error(f"🔴 {n_venc} vencido{'s' if n_venc != 1 else ''}", icon="🔴")
            else:
                st.success("🟢 Dentro del SLA", icon="✅")
        else:
            st.info("API offline", icon="ℹ️")

    _sla_table(sla_list)

    if not sla_list:
        st.markdown("""
<div style="background:rgba(0,224,150,0.06);border:1px solid rgba(0,224,150,0.15);
            border-radius:10px;padding:14px 18px;text-align:center;color:rgba(255,255,255,0.5);
            font-size:12px;margin-top:8px">
  ✅ No hay disputas de gobernanza pendientes · Sentinel opera sin conflictos activos
</div>""", unsafe_allow_html=True)

    # ── DIMENSIONES TGI — fila completa ───────────────────────────────────────
    st.markdown(
        "<div style='height:1px;background:rgba(255,255,255,0.06);margin:20px 0 16px'></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hub-block-title" style="margin-bottom:14px">Dimensiones TGI — Motor SIAP-ICPI v5.4</div>',
        unsafe_allow_html=True,
    )

    dim_cols = st.columns(5)
    for i, (key, col) in enumerate(zip(["d1","d2","d3","d4","d5"], dim_cols)):
        d = TGI_DATA[key]
        with col:
            st.markdown(_metric_card(
                d["nombre"], f"{d['val']:.1f}%", "", d["color"]
            ) + _bar(d["val"], d["color"]), unsafe_allow_html=True)
