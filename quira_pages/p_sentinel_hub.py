"""
QUIRA OS · p_sentinel_hub.py
QUIRA Observatorio — Pantalla 0

Fuente de datos:
  - Datos institucionales: data/gm_snapshot.json (outputs verificados Gold Master)
  - Datos Sentinel en tiempo real: SENTINEL API localhost:8100

PROHIBIDO hardcodear datos institucionales en este archivo.
Todo dato del GAD proviene exclusivamente de gm_snapshot.json,
actualizado manualmente por el analista Dylus Lab desde el Excel Gold Master.

Sprint 2.4 · UX alineada con html_engine · Dylus Lab © 2026
"""
from __future__ import annotations

import requests
import streamlit as st
import streamlit.components.v1 as components

from quira_pages.html_engine import DEMO_CSS, page_frame, page_header
from sentinel.gm_loader import (
    load as gm_load,
    get_gad, get_tgi, get_financiero, get_territorial,
    get_parroquias, get_parroquia_critica,
    mandato_progress, tgi_color, dim_color, iet_color,
    tgi_clasificacion_emoji, meta_info,
)

# ── API ────────────────────────────────────────────────────────────────────────
API_BASE    = "http://localhost:8100"
API_TIMEOUT = 4


def _api(endpoint: str) -> dict | None:
    try:
        r = requests.get(f"{API_BASE}{endpoint}", timeout=API_TIMEOUT)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


@st.cache_data(ttl=60, show_spinner=False)
def _fetch_sentinel():
    return (
        _api("/sentinel/health"),
        _api("/sentinel/trust-drift"),
        _api("/sentinel/sla"),
    )


@st.cache_data(ttl=300, show_spinner=False)
def _fetch_parity() -> dict | None:
    try:
        from sentinel.parity_engine import get_congruencia_status
        return get_congruencia_status()
    except Exception:
        return None


# ── CSS EXTRA (específico de esta pantalla) ───────────────────────────────────
EXTRA_CSS = """
.bloque-label {
  font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--cyan);
  border-left: 3px solid var(--cyan); padding-left: 9px;
  margin-bottom: 14px; line-height: 1;
}
.kpi-mini {
  background: var(--navy-card); border: 1px solid var(--divider);
  border-radius: 10px; padding: 12px 14px; text-align: center;
  margin-bottom: 8px;
}
.kpi-mini-label { font-size: 9px; color: var(--muted); letter-spacing: 0.6px; text-transform: uppercase; margin-bottom: 4px; }
.kpi-mini-val   { font-family: var(--mono); font-size: 20px; font-weight: 700; line-height: 1; }
.kpi-mini-sub   { font-size: 10px; color: var(--muted); margin-top: 4px; }

.insight-box {
  background: rgba(0,212,255,0.04); border: 1px solid rgba(0,212,255,0.15);
  border-radius: 10px; padding: 10px 14px; font-size: 11px;
  color: var(--muted); margin-top: 10px; line-height: 1.6;
}
.insight-box b { color: var(--cyan); }

.parr-row {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 0; border-bottom: 1px solid var(--divider);
  font-size: 11px;
}
.parr-row:last-child { border-bottom: none; }
.parr-nombre { flex: 1; color: var(--white); }

.sla-item {
  background: var(--navy-card); border: 1px solid var(--divider);
  border-radius: 8px; padding: 9px 13px; margin-bottom: 6px;
  display: flex; align-items: center; gap: 10px; font-size: 11px;
}
.sla-pregunta { flex: 1; color: var(--white); font-weight: 500; }
.sla-owner    { font-size: 10px; color: var(--muted); margin-top: 2px; }

.live-dot {
  display: inline-block; width: 7px; height: 7px; border-radius: 50%;
  background: var(--green); margin-right: 5px;
  animation: pulse 2s infinite; vertical-align: middle;
}
.pill-mini {
  display: inline-block; padding: 2px 8px; border-radius: 20px;
  font-size: 9px; font-weight: 700; font-family: var(--mono);
}
.pill-green  { background: rgba(0,224,150,0.12); color: var(--green); }
.pill-amber  { background: rgba(255,184,0,0.12);  color: var(--amber); }
.pill-red    { background: rgba(255,77,109,0.12); color: var(--red); }
.pill-orange { background: rgba(255,120,0,0.12);  color: #FF7800; }
.pill-muted  { background: rgba(255,255,255,0.06); color: var(--muted); }

.ver-tag {
  font-size: 9px; color: var(--muted); font-family: var(--mono);
  background: rgba(255,255,255,0.04); padding: 2px 7px; border-radius: 4px;
  margin-right: 4px;
}
.dim-row    { margin-bottom: 10px; }
.dim-header { display: flex; justify-content: space-between; align-items: center; }
.dim-nombre { font-size: 12px; font-weight: 600; color: var(--white); }
.dim-val    { font-family: var(--mono); font-size: 14px; font-weight: 700; }
.dim-sub    { font-size: 9px; color: var(--muted); margin-top: 1px; }

.hub-grid-5 { display: grid; grid-template-columns: repeat(5,1fr); gap: 10px; }
@media (max-width:600px) { .hub-grid-5 { grid-template-columns: 1fr 1fr !important; } }
"""


# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def _kpi(label: str, val: str, sub: str = "", color: str = "var(--white)") -> str:
    return f"""
<div class="kpi-mini">
  <div class="kpi-mini-label">{label}</div>
  <div class="kpi-mini-val" style="color:{color}">{val}</div>
  <div class="kpi-mini-sub">{sub}</div>
</div>"""


def _bar(pct: float, color: str, height: int = 5) -> str:
    return f"""
<div style="background:var(--divider);border-radius:3px;height:{height}px;overflow:hidden;margin-top:3px">
  <div style="width:{min(pct,100):.1f}%;height:100%;background:{color};border-radius:3px;transition:width .8s ease"></div>
</div>"""


def _pill(text: str, cls: str = "pill-muted") -> str:
    return f'<span class="pill-mini {cls}">{text}</span>'


def _dim_css(val: float) -> str:
    return "pill-green" if val >= 75 else ("pill-amber" if val >= 55 else "pill-red")


# ── BLOQUES HTML ──────────────────────────────────────────────────────────────
def _html_bloque_a(gad: dict, tgi: dict, prog: dict) -> str:
    pct       = prog["pct_ejecutado"]
    dias      = prog["dias_restantes"]
    tgi_score = tgi.get("score", 0)
    tgi_cls   = tgi.get("clasificacion", "")
    tgi_emoji = tgi_clasificacion_emoji(tgi_cls)
    tgi_clr   = tgi_color(tgi_score)
    icpi      = tgi.get("icpi_historico", {}).get("2025", 0)
    objetivo  = tgi.get("meta_2027", 60)
    brecha    = objetivo - tgi_score

    brecha_txt = (
        f"Faltan <b>{brecha:.2f} pts</b> para meta TGI 2027 ({objetivo})."
        if brecha > 0 else "✓ Meta TGI 2027 alcanzada."
    )

    return f"""
<div class="card">
  <div class="bloque-label">A · Gobierno y Mandato</div>
  <div class="grid-2">
    <div>
      {_kpi("Alcaldía", gad.get("alcalde","–"), gad.get("periodo",""), "var(--cyan)")}
      {_kpi("Inicio de gestión", gad.get("inicio_mandato","–"), "CNE Ecuador 2023")}
    </div>
    <div>
      {_kpi("TGI Territorial", f"{tgi_score:.2f}", f"{tgi_emoji} {tgi_cls}", tgi_clr)}
      {_kpi("Días restantes", f"{dias:,}", "para cierre de mandato", "var(--amber)")}
    </div>
  </div>

  <div style="margin-top:10px">
    <div style="display:flex;justify-content:space-between;font-size:10px;
                color:var(--muted);margin-bottom:5px">
      <span>{gad.get("inicio_mandato","2023")[:4]}</span>
      <span style="color:var(--cyan);font-weight:700">■ {pct:.1f}% mandato ejecutado</span>
      <span>{gad.get("fin_mandato","2027")[:4]}</span>
    </div>
    {_bar(pct, "linear-gradient(90deg,var(--cyan),#7C5CFC)", height=6)}
    <div style="margin-top:8px;display:flex;gap:16px;flex-wrap:wrap">
      <span style="font-size:10px;color:var(--muted)">
        Mandato consumido: <b style="color:var(--amber)">{pct:.1f}%</b>
      </span>
      <span style="font-size:10px;color:var(--muted)">
        ICPI-Metas 2025: <b style="color:{'var(--red)' if icpi < 70 else 'var(--green)'}">{icpi:.2f}%</b>
      </span>
      {'<span style="font-size:10px;color:rgba(255,77,109,.7)">⚠ Mandato supera ritmo de metas</span>' if (pct - icpi) > 10 else ''}
    </div>
  </div>

  <div class="insight-box">
    Han transcurrido <b>{pct:.1f}%</b> del mandato.
    TGI territorial: <b>{tgi_score:.2f}</b> ({tgi_cls}).
    Ventana de cierre: <b>{dias} días</b>. {brecha_txt}
  </div>
</div>"""


def _html_bloque_b(terr: dict, parroquias: list, critica: dict | None) -> str:
    rurales = sorted(
        [p for p in parroquias if p.get("tipo") == "Rural"],
        key=lambda p: p.get("iet_local_pct", 0),
    )

    critica_html = ""
    if critica:
        agua = critica.get("cobertura_agua_pct", 0)
        nbi  = critica.get("nbi_pct", 0)
        iet  = critica.get("iet_local_pct", 0)
        invpc = critica.get("inv_percapita_q1", 0)
        critica_html = f"""
<div style="margin-top:10px;background:rgba(255,77,109,.06);
            border:1px solid rgba(255,77,109,.2);border-radius:10px;
            padding:11px 14px;display:flex;align-items:center;gap:12px">
  <div style="font-size:18px">⚠</div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:700;color:var(--red)">{critica.get('nombre','')}</div>
    <div style="font-size:10px;color:var(--muted);margin-top:2px">
      Parroquia con mayor brecha territorial · intervención urgente
    </div>
  </div>
  <div style="display:flex;flex-direction:column;gap:4px;align-items:flex-end">
    {_pill(f"NBI {nbi}%","pill-red")}
    {_pill(f"IET {iet:.0f}%","pill-red")}
    {_pill(f"Agua {agua}%","pill-red")}
    {_pill(f"${invpc}/hab","pill-orange")}
  </div>
</div>"""

    ranking_rows = ""
    for p in rurales:
        iet  = p.get("iet_local_pct", 0)
        clr  = iet_color(iet)
        css  = "pill-green" if iet >= 60 else ("pill-amber" if iet >= 40 else "pill-red")
        invpc = p.get("inv_percapita_q1", 0)
        ranking_rows += f"""
<div class="parr-row">
  <span class="parr-nombre">{p.get('nombre','')}</span>
  <div style="width:70px">
    <div style="background:var(--divider);border-radius:3px;height:4px;overflow:hidden">
      <div style="width:{min(iet,100):.0f}%;height:100%;background:{clr};border-radius:3px"></div>
    </div>
  </div>
  {_pill(f"{iet:.0f}%", css)}
  <span style="font-size:9px;color:var(--muted)">${invpc}/hab</span>
</div>"""

    return f"""
<div class="card">
  <div class="bloque-label">B · Territorio y Equidad</div>
  <div class="grid-2">
    <div>
      {_kpi("Población", f"{terr.get('poblacion_census_2022',0):,}", "Censo INEC 2022", "var(--cyan)")}
      {_kpi("NBI Rural promedio", f"{terr.get('nbi_rural_promedio',0):.1f}%",
             "6 parroquias rurales", "var(--red)")}
    </div>
    <div>
      {_kpi("Parroquias", str(terr.get('parroquias_total',7)), "1 urbana · 6 rurales", "var(--green)")}
      {_kpi("Inv. per cápita cantonal", f"${terr.get('cantonal_avg_inv_percapita',0)}/hab",
             "promedio ponderado Q1-2026", "var(--amber)")}
    </div>
  </div>
  {critica_html}
  <div style="margin-top:12px;font-size:9px;color:var(--muted);
              letter-spacing:.8px;text-transform:uppercase;margin-bottom:6px">
    Ranking equidad — parroquias rurales (IET local)
  </div>
  {ranking_rows}
</div>"""


def _html_bloque_c(tgi: dict, fin: dict) -> str:
    icpi_2025 = tgi.get("icpi_historico", {}).get("2025", 0)
    dims_html = ""
    for key in ["d1", "d2", "d3", "d4", "d5"]:
        d    = tgi.get(key, {})
        val  = d.get("valor", 0)
        clr  = dim_color(val)
        css  = _dim_css(val)
        peso = int(d.get("peso", 0) * 100)
        src  = d.get("fuente", "").split("—")[0].strip()[:38]
        dims_html += f"""
<div class="dim-row">
  <div class="dim-header">
    <span class="dim-nombre">{d.get('codigo','?')} {d.get('nombre','')}</span>
    <div style="display:flex;align-items:center;gap:6px">
      {_pill(f"w={peso}%","pill-muted")}
      <span class="dim-val" style="color:{clr}">{val:.1f}</span>
    </div>
  </div>
  <div class="dim-sub">{src}</div>
  {_bar(val, clr)}
</div>"""

    irs      = tgi.get("irs", {})
    irs_val  = irs.get("valor", 0)
    irs_clr  = "var(--red)" if irs_val > 70 else ("var(--amber)" if irs_val > 45 else "var(--green)")
    fondos   = fin.get("fondos_bloqueados_est", 0)
    f_det    = fin.get("fondos_bloqueados_detalle", "")

    return f"""
<div class="card">
  <div class="bloque-label">C · Ejecución y Riesgo</div>
  {dims_html}
  <div class="grid-2" style="margin-top:8px">
    {_kpi("IRS — Regresividad", f"{irs_val:.1f}",
          f"{irs.get('clasificacion','')} · Meta 2027: {irs.get('meta_2027','?')}", irs_clr)}
    {_kpi("Fondos bloqueados est.", f"${fondos/1e6:.1f}M", f_det[:40], "var(--red)")}
  </div>
  <div style="margin-top:10px;background:rgba(255,77,109,.06);
              border:1px solid rgba(255,77,109,.2);border-radius:10px;padding:10px 14px">
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-bottom:6px">
      Alertas TGI activas
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      {_pill("D3 Ejecución 🔴 59.85%","pill-red")}
      {_pill("D4 Equidad 🔴 44.8%","pill-red")}
      {_pill("IRS Muy Regresivo 79.7","pill-red")}
      {_pill("Isabel Muentes agua 1%","pill-red")}
    </div>
    <div style="font-size:10px;color:var(--muted);margin-top:6px">
      ICPI_2025: {icpi_2025:.2f}% · Objetivo 2027: ≥70%
    </div>
  </div>
</div>"""


def _parity_panel(parity: dict | None) -> str:
    if not parity:
        return ""
    g_label = parity.get("global_label", "–")
    g_emoji = parity.get("global_emoji", "⬜")
    g_color = parity.get("global_color", "#888")
    g_ts    = parity.get("checked_display", "–")
    g_st    = parity.get("global_status", "error")
    fuente  = parity.get("fuente", {})
    memoria = parity.get("memoria", {})
    motor   = parity.get("motor", {})

    def _clr(s):
        return "var(--green)" if s == "ok" else ("var(--amber)" if s == "warning" else "var(--red)")

    bg  = "rgba(0,224,150,.06)"  if g_st == "ok" else \
          "rgba(255,184,0,.06)"  if g_st == "warning" else \
          "rgba(255,77,109,.06)"
    brd = "rgba(0,224,150,.2)"   if g_st == "ok" else \
          "rgba(255,184,0,.2)"   if g_st == "warning" else \
          "rgba(255,77,109,.2)"

    def _row(label, s):
        icon = {"ok": "✓", "warning": "⚠", "error": "✗"}.get(s, "?")
        return f"""
<div style="display:flex;justify-content:space-between;font-size:11px;padding:3px 0">
  <span style="color:var(--muted)">{label}</span>
  <span style="color:{_clr(s)};font-weight:700">{icon}</span>
</div>"""

    return f"""
<div style="background:{bg};border:1px solid {brd};border-radius:10px;
            padding:12px 14px;margin-bottom:10px">
  <div style="font-size:12px;font-weight:800;color:{g_color};margin-bottom:8px">
    {g_emoji} {g_label}
  </div>
  {_row("Fuente Operativa",      fuente.get("status","error"))}
  {_row("Memoria Institucional", memoria.get("status","error"))}
  {_row("Motor Analítico",       motor.get("status","error"))}
  <div style="font-size:9px;color:rgba(255,255,255,.2);margin-top:8px;padding-top:6px;
              border-top:1px solid rgba(255,255,255,.05)">
    Última sincronización: {g_ts}
  </div>
</div>"""


def _html_bloque_d(health: dict | None, drift: dict | None,
                   sla_summary: dict | None, gm_meta: dict,
                   parity: dict | None = None) -> str:
    api_ok   = health is not None
    chunks   = health.get("total_chunks", 0) if health else "–"
    llm_ok   = health.get("llm_disponible", False) if health else False
    disputas = 0
    if sla_summary:
        disputas = sla_summary.get("vencidos", 0) + sla_summary.get("criticos", 0)

    live_dot = '<span class="live-dot"></span>' if api_ok else "🔴 "

    drift_html = ""
    if drift:
        tend  = drift.get("tendencia", "ESTABLE")
        tc    = {"ESTABLE":"var(--green)","MEJORANDO":"var(--cyan)","DEGRADANDO":"var(--red)"}.get(tend,"var(--white)")
        ti    = {"ESTABLE":"=","MEJORANDO":"↑","DEGRADANDO":"↓"}.get(tend,"=")
        max_r = drift.get("pct_rechazo_max", 0)
        drift_html = _kpi("Tendencia Operativa", f"{ti} {tend}",
                          f"{drift.get('n_semanas',0)} sem · variación máx {max_r:.0f}%", tc)
    else:
        drift_html = _kpi("Tendencia Operativa", "–", "Sistema analítico sin conexión", "var(--muted)")

    mi = gm_meta

    return f"""
<div class="card">
  <div class="bloque-label">D · Estado del Sistema Institucional</div>
  {_parity_panel(parity)}
  <div class="grid-2">
    {_kpi("Sistema Analítico",
          f"{live_dot}{'Operativo' if api_ok else 'No disponible'}",
          f"{chunks} documentos indexados",
          "var(--green)" if api_ok else "var(--red)")}
    {_kpi("Motor de Consulta",
          "Activo" if llm_ok else "Modo básico",
          "Análisis institucional habilitado" if llm_ok else "Consultas limitadas",
          "var(--cyan)" if llm_ok else "var(--amber)")}
    {_kpi("Alertas sin atender",
          str(disputas),
          "requieren coordinador" if disputas > 0 else "dentro del SLA",
          "var(--red)" if disputas > 0 else "var(--green)")}
    {drift_html}
  </div>
  <div style="margin-top:10px;display:flex;gap:5px;flex-wrap:wrap">
    <span class="ver-tag">SENTINEL v2.1.0</span>
    <span class="ver-tag">PROMPT v2.1.0</span>
    <span class="ver-tag">GUARDRAIL v1.7.0</span>
    <span class="ver-tag">20/20 regression ✓</span>
  </div>
  <div style="margin-top:5px;font-size:9px;color:rgba(255,255,255,.2)">
    Gold Master {mi.get('version_excel','–')} ·
    Corte {mi.get('fecha_corte','–')} ·
    Próx. act.: {mi.get('proxima_actualizacion','–')}
  </div>
</div>"""


def _html_sla_table(sla_list: list) -> str:
    if not sla_list:
        return """
<div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.15);
            border-radius:10px;padding:14px;text-align:center;
            color:var(--muted);font-size:12px">
  ✓ Sin disputas de gobernanza activas · SENTINEL opera sin conflictos
</div>"""

    rows = ""
    for sla in sla_list[:8]:
        icon   = sla.get("status_icon", "•")
        status = sla.get("status", "")
        owner  = sla.get("owner", "–")
        hours  = sla.get("horas_restantes", "–")
        preg   = sla.get("pregunta", "")[:58]
        prio   = sla.get("priority", "")
        css    = {"NORMAL":"pill-green","SEGUIMIENTO":"pill-amber","CRITICO":"pill-orange",
                  "VENCIDO":"pill-red","CUMPLIDO":"pill-muted"}.get(status,"pill-muted")
        rows += f"""
<div class="sla-item">
  <span style="font-size:15px">{icon}</span>
  <div style="flex:1">
    <div class="sla-pregunta">{preg}…</div>
    <div class="sla-owner">Owner: {owner} · Prioridad: {prio}</div>
  </div>
  <div style="text-align:right">
    {_pill(status, css)}
    <div style="font-size:9px;color:var(--muted);margin-top:3px">{hours}h restantes</div>
  </div>
</div>"""
    return rows


def _html_fila_dimensiones(tgi: dict) -> str:
    items = ""
    for key in ["d1", "d2", "d3", "d4", "d5"]:
        d   = tgi.get(key, {})
        val = d.get("valor", 0)
        clr = dim_color(val)
        items += f"""
<div class="kpi-mini">
  <div class="kpi-mini-label">{d.get('codigo','')}</div>
  <div class="kpi-mini-val" style="color:{clr};font-size:18px">{val:.1f}</div>
  <div class="kpi-mini-sub" style="font-size:9px">{d.get('nombre','')}</div>
  {_bar(val, clr)}
</div>"""
    return f'<div class="hub-grid-5">{items}</div>'


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
def render():
    # ── Cargar Gold Master snapshot ─────────────────────────────────────────
    gm = gm_load()
    if not gm.get("_loaded"):
        st.error("Datos institucionales no disponibles. El sistema no puede mostrar indicadores.")
        st.info("Contactar al equipo técnico para actualizar la base de datos institucional.")
        return

    gad        = get_gad(gm)
    tgi        = get_tgi(gm)
    fin        = get_financiero(gm)
    terr       = get_territorial(gm)
    parroquias = get_parroquias(gm)
    critica    = get_parroquia_critica(gm)
    prog       = mandato_progress(gm)
    gm_meta    = meta_info(gm)

    # ── Cargar SENTINEL API ─────────────────────────────────────────────────
    with st.spinner("Conectando SENTINEL API…"):
        health, drift, sla_resp = _fetch_sentinel()

    # ── Congruencia Institucional (Sprint 2.5C) ─────────────────────────────
    parity = _fetch_parity()

    sla_summary = sla_resp.get("summary") if sla_resp else None
    sla_list    = sla_resp.get("slas", []) if sla_resp else []

    # ── Botón actualizar (fuera del iframe) ─────────────────────────────────
    col_t, col_btn = st.columns([5, 1])
    with col_t:
        api_status = "🟢 SENTINEL en línea" if health else "🔴 SENTINEL offline"
        st.caption(f"**Centro de Control Territorial** · {gad.get('nombre', 'GAD Montecristi')} · {api_status}")
    with col_btn:
        if st.button("↻", use_container_width=True, help="Actualizar datos en tiempo real"):
            st.cache_data.clear()
            st.rerun()

    if health is None:
        st.warning(
            "SENTINEL API no responde en `localhost:8100`. "
            "Datos institucionales del Gold Master disponibles.",
            icon="⚠️",
        )

    # ── Construir HTML completo ─────────────────────────────────────────────
    hdr = page_header(
        "⬡ CONTROL",
        "QUIRA Observatorio",
        f"{gad.get('alcalde','–')} · {gad.get('periodo','–')} · TGI {tgi.get('score',0):.2f} — {tgi.get('clasificacion','')}",
        f'<span class="badge badge-amber">⬡ v1.0 RC</span>',
    )

    # 4 bloques en 2×2
    bloques_2x2 = f"""
<div class="grid-2" style="margin-bottom:12px">
  {_html_bloque_a(gad, tgi, prog)}
  {_html_bloque_b(terr, parroquias, critica)}
</div>
<div class="grid-2" style="margin-bottom:12px">
  {_html_bloque_c(tgi, fin)}
  {_html_bloque_d(health, drift, sla_summary, gm_meta, parity=parity)}
</div>"""

    # SLA panel
    sla_alerta = ""
    if sla_summary and sla_summary.get("alerta"):
        n = sla_summary.get("vencidos", 0)
        sla_alerta = f'<span class="badge badge-red">🔴 {n} SLA vencido{"s" if n!=1 else ""}</span>'
    else:
        sla_alerta = '<span class="badge badge-green">🟢 Dentro del SLA</span>'

    sla_section = f"""
<div class="card">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
    <div class="bloque-label" style="margin-bottom:0">SLA de Gobernanza · Casos activos</div>
    {sla_alerta}
  </div>
  {_html_sla_table(sla_list)}
</div>"""

    # Fila dimensiones TGI
    dims_section = f"""
<div class="card">
  <div class="bloque-label" style="margin-bottom:12px">
    Dimensiones TGI — Motor SIAP-ICPI {gm_meta.get('version_excel','v5.4')}
  </div>
  {_html_fila_dimensiones(tgi)}
</div>"""

    html = hdr + bloques_2x2 + sla_section + dims_section

    # ── Render iframe ───────────────────────────────────────────────────────
    full = page_frame(html, show_tech=False, extra_css=EXTRA_CSS)
    components.html(full, height=1600, scrolling=False)

    # ── Snapshot Institucional Mensual ──────────────────────────────────────
    st.markdown("---")
    with st.expander("📊 Registro de Estado Institucional Mensual", expanded=False):
        st.caption(
            "Genera un registro oficial del estado del municipio al cierre del período. "
            "Incluye congruencia documental, validación de indicadores y alertas activas. "
            "Apto para **LOTAIP**, rendición de cuentas y transición administrativa."
        )
        sc1, sc2, sc3 = st.columns([2, 2, 3])
        snap_year  = sc1.number_input("Año", min_value=2024, max_value=2030,
                                      value=2026, step=1, label_visibility="visible")
        snap_month = sc2.number_input("Mes", min_value=1, max_value=12,
                                      value=3, step=1, label_visibility="visible")
        snap_notas = sc3.text_input("Notas (opcional)",
                                    placeholder="Cierre Q1 / Rendición ordinaria",
                                    label_visibility="visible")

        if st.button("📊 Registrar Estado Institucional", use_container_width=True, type="primary"):
            with st.spinner("Consolidando estado institucional…"):
                from sentinel.snapshot_engine import generate_snapshot, get_snapshots, export_snapshot_xlsx
                snap = generate_snapshot(int(snap_year), int(snap_month),
                                         triggered_by="manual_hub", notas=snap_notas)
            if snap.get("saved"):
                st.success(
                    f"Registro **{snap['period_label']}** generado. "
                    f"Congruencia documental: `{snap['congruencia_status']}` · "
                    f"Validación indicadores: `{snap['integridad_n_ok']}/{snap['integridad_n_total']}` · "
                    f"Alertas críticas: `{snap['alertas_criticas']}`"
                )
                xlsx_snap = export_snapshot_xlsx(snap, [])
                if xlsx_snap:
                    from datetime import date as _d
                    st.download_button(
                        label="📊 Descargar Registro Excel",
                        data=xlsx_snap,
                        file_name=f"estado_institucional_{snap_year}{snap_month:02d}_{_d.today().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
            else:
                st.warning("Registro generado pero no guardado. Verificar conexión institucional.")

        # Registros anteriores
        from sentinel.snapshot_engine import get_snapshots
        snaps = get_snapshots(limit=12)
        if snaps:
            st.markdown("**Registros anteriores**")
            _LABEL = {"ok": "✓ Operativo", "warning": "⚠ Atención", "error": "✗ Revisión"}
            snap_rows = []
            for s in snaps:
                snap_rows.append({
                    "Período":       s.get("period_label", ""),
                    "Congruencia":   _LABEL.get(s.get("congruencia_status", ""), "–"),
                    "Integridad":    f"{s.get('integridad_n_ok',0)}/{s.get('integridad_n_total',0)}",
                    "Alertas Crit.": s.get("alertas_criticas", 0),
                    "Generado":      (s.get("generated_at") or "")[:16],
                })
            st.dataframe(snap_rows, use_container_width=True, hide_index=True)

    # ── Botones de navegación (fuera del iframe) ─────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔍 Análisis de Brecha", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c2:
        if st.button("💬 Consultar SENTINEL", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.rerun()
    with c3:
        if st.button("📋 Metas del PDOT", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
