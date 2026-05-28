"""
QUIRA Intelligence — Centro de Mando  (Sprint 1.2 · Unificación Visual)
Teatro Operacional Único · GAD Montecristi

Arquitectura Sprint 1.2:
  · CERO widgets Streamlit visibles — Streamlit = runtime invisible
  · HTML Canvas full-viewport como único plano visual
  · Layout operacional: KPI band → [GeoTwin Rail | Domain Grid] → Bottom band
  · GeoTwin al left rail (inspiración Palantir Gotham / C4ISR)
  · Navigation por onclick → JS bridge → hidden st.button → st.rerun()
  · Sidebar oculto por CSS — no existe para el Ejecutivo

"QUIRA no es un conjunto de páginas. QUIRA es un teatro operacional vivo."
Dylus Lab © 2026
"""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as _cv1

from utils.cache_quira import cargar_gm_snapshot, cargar_snapshot
from utils.css_tokens import C
from utils.session import get_rol, is_tecnico, logout

# ── Rutas ─────────────────────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).parent.parent / "data"
_GEOJSON  = _DATA_DIR / "parroquias_montecristi.geojson"

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE TEMPERATURA
# ══════════════════════════════════════════════════════════════════════════════
_TEMP: dict[str, dict[str, str]] = {
    "critico": {"bg": "rgba(239,68,68,.10)",   "bd": "rgba(239,68,68,.35)",   "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.09)",  "bd": "rgba(249,115,22,.30)",  "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.05)",   "bd": "rgba(0,212,255,.16)",   "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.07)",   "bd": "rgba(34,197,94,.24)",   "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.10)",  "bd": "rgba(124,92,252,.32)",  "c": "#7C5CFC"},
}

# ══════════════════════════════════════════════════════════════════════════════
# CAPAS Y DOMINIOS INSTITUCIONALES
# mod = destino de navegación (gov_module key)
# ══════════════════════════════════════════════════════════════════════════════
_CAPAS: list[dict] = [
    {"id": "politica",    "label": "POLÍTICA",     "accent": "#00D4FF"},
    {"id": "ejecutiva",   "label": "EJECUTIVA",    "accent": "#F97316"},
    {"id": "rendicion",   "label": "RENDICIÓN",    "accent": "#7C5CFC"},
    {"id": "territorial", "label": "TERRITORIAL",  "accent": "#22C55E"},
]

_DOMAINS: list[dict] = [
    # ── CAPA POLÍTICA ─────────────────────────────────────────────────────────
    {"id":"d01","capa":"politica","nombre":"Salud Institucional",
     "metric":"17.4%","nota":"Índice cumplimiento · umbral 65%",
     "temp":"critico","grav":3,"act":"activo","mod":"situacion"},
    {"id":"d02","capa":"politica","nombre":"Fidelidad Política",
     "metric":"44/66","nota":"Compromisos CNE cumplidos",
     "temp":"normal","grav":1,"act":"pasivo","mod":"situacion"},
    {"id":"d03","capa":"politica","nombre":"Panel Estratégico",
     "metric":"6 vectores","nota":"Preparación · respuesta política",
     "temp":"alerta","grav":2,"act":"activo","mod":"concejo"},
    # ── CAPA EJECUTIVA ─────────────────────────────────────────────────────────
    {"id":"d04","capa":"ejecutiva","nombre":"Holding Municipal",
     "metric":"68.7%","nota":"Promedio 4 entidades",
     "temp":"alerta","grav":3,"act":"activo","mod":"municipal"},
    {"id":"d05","capa":"ejecutiva","nombre":"Eficiencia Operacional",
     "metric":"—","nota":"Rendimiento relativo por entidad",
     "temp":"normal","grav":1,"act":"monitoreo","mod":"analisis","tec":True},
    {"id":"d06","capa":"ejecutiva","nombre":"Equidad Territorial",
     "metric":"$40/hab","nota":"Rural vs $217 cabecera",
     "temp":"alerta","grav":2,"act":"activo","mod":"geotwin","tec":True},
    # ── CAPA RENDICIÓN ─────────────────────────────────────────────────────────
    {"id":"d07","capa":"rendicion","nombre":"Transparencia",
     "metric":"—","nota":"Gobierno abierto · CPCCS · LOTAIP",
     "temp":"normal","grav":1,"act":"pasivo","mod":"rdc"},
    {"id":"d08","capa":"rendicion","nombre":"Participación Ciudadana",
     "metric":"—","nota":"Presupuesto participativo · IGP",
     "temp":"normal","grav":1,"act":"pasivo","mod":"confianza"},
    {"id":"d09","capa":"rendicion","nombre":"Género y Equidad Social",
     "metric":"12.83%","nota":"Presupuesto género · umbral 30%",
     "temp":"critico","grav":2,"act":"activo","mod":"genero"},
    {"id":"d10","capa":"rendicion","nombre":"Ambiente y Sostenibilidad",
     "metric":"0%","nota":"Metas FA-CC · FA-DIS sin ejecución",
     "temp":"critico","grav":2,"act":"activo","mod":"genero"},
    # ── CAPA TERRITORIAL ───────────────────────────────────────────────────────
    {"id":"d11","capa":"territorial","nombre":"Cooperación Internacional",
     "metric":"$3.66M","nota":"Fondos condicionados · 3 fuentes activas",
     "temp":"funds","grav":3,"act":"activo","mod":"cooperacion"},
    {"id":"d12","capa":"territorial","nombre":"Agenda 2030",
     "metric":"—","nota":"ODS ↔ PDOT · alineación activa",
     "temp":"normal","grav":1,"act":"monitoreo","mod":"ods"},
    {"id":"d13","capa":"territorial","nombre":"Observabilidad Longitudinal",
     "metric":"1 punto","nota":"Sistema activo · histórico iniciado",
     "temp":"verde","grav":1,"act":"pasivo","mod":"control","tec":True},
]

# Mapa estado parroquia → estilos Folium
_MAP_ESTADO: dict[str, dict] = {
    "NORMAL":     {"c": "#0284C7", "fo": 0.55, "r": 20},
    "ALERTA":     {"c": "#EA580C", "fo": 0.60, "r": 17},
    "PRIORIDAD":  {"c": "#DC2626", "fo": 0.65, "r": 22},
    "EMERGENCIA": {"c": "#7F1D1D", "fo": 0.72, "r": 18},
}


# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def _load_data() -> dict[str, Any]:
    snap, _meta = cargar_snapshot()
    gm          = cargar_gm_snapshot()

    d: dict[str, Any] = {
        "icpi_pct": None, "icpi_clasif": "—",
        "n_alertas": 0,   "riesgo_clasif": "—",
        "hold_avg": 68.7, "has_snap": bool(snap),
    }

    if snap:
        icpi_d = snap.get("icpi", {})
        d["icpi_pct"]    = icpi_d.get("global_pct") or icpi_d.get("global")
        d["icpi_clasif"] = icpi_d.get("clasificacion", "—")
        sat_d = snap.get("sat", {})
        d["n_alertas"]     = sat_d.get("total_activas", 0)
        d["riesgo_clasif"] = sat_d.get("clasif_riesgo", "—").upper()

    if gm and d["icpi_pct"] is None:
        icpi_gm = gm.get("icpi", {})
        d["icpi_pct"]    = icpi_gm.get("global_pct") or icpi_gm.get("global")
        d["icpi_clasif"] = icpi_gm.get("clasificacion", "—")

    return d


# ══════════════════════════════════════════════════════════════════════════════
# GEOTWIN — genera HTML Folium y lo convierte a base64 iframe
# ══════════════════════════════════════════════════════════════════════════════

def _get_map_html() -> str | None:
    """Genera el mapa Folium como string HTML base64-encoded para iframe."""
    try:
        import folium
    except ImportError:
        return None

    if not _GEOJSON.exists():
        return None

    try:
        gj_data = json.loads(_GEOJSON.read_text(encoding="utf-8"))
    except Exception:
        return None

    m = folium.Map(
        location=[-1.065, -80.625],
        zoom_start=11,
        tiles=None,
        scrollWheelZoom=True,
        zoom_control=True,
        prefer_canvas=True,
        attributionControl=False,
    )
    folium.TileLayer(
        tiles="https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
        attr="© OpenStreetMap © CARTO",
        max_zoom=18,
        opacity=1.0,
    ).add_to(m)

    for feat in gj_data.get("features", []):
        props  = feat.get("properties", {})
        coords = feat["geometry"]["coordinates"]
        nombre = props.get("nombre", "")
        estado = props.get("estado", "NORMAL")
        tipo   = props.get("tipo", "")
        hab    = props.get("habitantes", 0)
        pc     = props.get("per_capita", 0)
        agua   = props.get("agua", 0)

        lat, lng = coords[1], coords[0]
        sty    = _MAP_ESTADO.get(estado, {"c": "#475569", "fo": 0.45, "r": 14})
        color  = sty["c"]
        radius = sty["r"]
        is_cab = "cabecera" in nombre.lower()
        if is_cab:
            radius = 30

        tooltip_body = f"""
<div style="font-family:Inter,system-ui,sans-serif;background:#0F172A;color:#E2E8F0;
            border:1px solid rgba(255,255,255,.12);border-radius:8px;
            padding:10px 14px;min-width:180px;box-shadow:0 4px 20px rgba(0,0,0,.45)">
  <div style="font-size:12px;font-weight:700;margin-bottom:4px">{nombre}</div>
  <div style="font-size:9px;color:{color};font-weight:700;letter-spacing:.08em;
              text-transform:uppercase;margin-bottom:8px">{estado} · {tipo}</div>
  <div style="font-size:10px;color:rgba(255,255,255,.50);line-height:1.65">
    {f'{hab:,} hab.' if hab else ''}
    {f'<br>Inversión: ${pc}/hab' if pc else ''}
    {f'<br>Agua: {agua}%' if agua else ''}
  </div>
</div>"""

        if estado in ("EMERGENCIA", "PRIORIDAD"):
            folium.CircleMarker(
                location=[lat, lng], radius=radius + 14,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.10, weight=0.5, interactive=False,
            ).add_to(m)

        folium.CircleMarker(
            location=[lat, lng], radius=radius,
            color=color, fill=True, fill_color=color,
            fill_opacity=sty["fo"], weight=2.0,
            tooltip=folium.Tooltip(tooltip_body, sticky=False, parse_html=True),
        ).add_to(m)

        nombre_corto = nombre.replace(" (cabecera)", "").replace("Parroquia ", "")
        lbl_mt = radius + 8 if not is_cab else radius + 6
        folium.Marker(
            location=[lat, lng],
            icon=folium.DivIcon(
                html=f"""<div style="font-family:Inter,system-ui;font-size:10px;
                    font-weight:700;color:#1e293b;white-space:nowrap;
                    text-align:center;margin-top:{lbl_mt}px;
                    text-shadow:0 0 3px #fff,0 0 3px #fff,1px 1px 4px rgba(255,255,255,.8)">
                    {nombre_corto}</div>""",
                icon_size=(160, 22), icon_anchor=(80, 0),
            ),
            tooltip=folium.Tooltip(tooltip_body, sticky=False, parse_html=True),
        ).add_to(m)

    try:
        html_str = m.get_root().render()
        # Inyectar CSS para fondo oscuro consistente con el canvas
        dark_bg = """<style>
html,body{background:#0a0f1e!important;margin:0;padding:0}
.leaflet-container{background:#0a0f1e!important}
</style>"""
        html_str = html_str.replace("</head>", dark_bg + "</head>", 1)
        b64 = base64.b64encode(html_str.encode("utf-8")).decode("ascii")
        return f"data:text/html;base64,{b64}"
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# HTML BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def _kpi_band(d: dict) -> str:
    """Banda Vital Superior — 4 KPIs con onclick al módulo correcto."""
    icpi_pct  = d.get("icpi_pct")
    n_alertas = d.get("n_alertas", 0)
    riesgo_cl = d.get("riesgo_clasif", "—")
    hold_avg  = d.get("hold_avg", 68.7)

    icpi_color  = C.sem(icpi_pct) if icpi_pct is not None else "#EF4444"
    alert_color = "#EF4444" if n_alertas > 0 else "#22C55E"
    hold_color  = C.sem(hold_avg)

    icpi_str  = f"{icpi_pct:.1f}%" if icpi_pct is not None else "17.4%"
    alert_str = str(n_alertas) if n_alertas >= 0 else "0"
    riesgo_str = riesgo_cl if riesgo_cl not in ("—", "") else "Sin alertas críticas"

    def _kpi(label: str, val: str, color: str, sub: str,
             dest: str, size: str = "lg") -> str:
        fs = "2.1rem" if size == "lg" else "1.55rem"
        pt = "18px 20px 14px" if size == "lg" else "14px 16px 11px"
        return f"""
<div onclick="qNav('{dest}')"
     style="background:rgba(8,13,24,.97);border:1px solid {color}28;
            border-top:2px solid {color};border-radius:10px;
            padding:{pt};cursor:pointer;flex:1;min-width:0;
            transition:border-color .18s,background .18s"
     onmouseover="this.style.background='rgba(0,212,255,.04)';this.style.borderColor='{color}55'"
     onmouseout="this.style.background='rgba(8,13,24,.97)';this.style.borderTopColor='{color}';this.style.borderLeftColor='{color}28';this.style.borderRightColor='{color}28';this.style.borderBottomColor='{color}28'">
  <div style="font-size:8px;font-weight:700;letter-spacing:.10em;
              text-transform:uppercase;color:rgba(255,255,255,.28);
              margin-bottom:10px">{label}</div>
  <div style="font-size:{fs};font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.04em;line-height:1;
              margin-bottom:8px">{val}</div>
  <div style="font-size:9px;color:rgba(255,255,255,.26);
              letter-spacing:.01em;line-height:1.4">{sub}</div>
</div>"""

    return f"""
<div style="display:flex;gap:10px;margin-bottom:12px">
  {_kpi("Cumplimiento Municipal", icpi_str, icpi_color,
        d.get("icpi_clasif","—") + " · umbral 65%", "situacion", "lg")}
  {_kpi("Fondos en Riesgo", "$3.66M", "#7C5CFC",
        "3 fuentes condicionadas · acción requerida", "cooperacion", "lg")}
  {_kpi("Alertas Activas", alert_str, alert_color, riesgo_str, "alertas", "sm")}
  {_kpi("Holding Municipal", f"{hold_avg:.1f}%", hold_color,
        "Promedio 4 entidades", "municipal", "sm")}
</div>"""


def _domain_card(dom: dict, accessible: bool) -> str:
    """Tarjeta de dominio HTML con onclick navigation."""
    t    = _TEMP.get(dom["temp"], _TEMP["normal"])
    grav = dom["grav"]
    act  = dom["act"]
    mod  = dom["mod"]

    pad     = {3: "14px 13px 12px", 2: "11px 12px 10px", 1: "9px 11px 8px"}[grav]
    nomb_fs = {3: "12px",           2: "11.5px",          1: "11px"}[grav]
    nota_fs = {3: "9px",            2: "8.5px",           1: "8px"}[grav]
    met_fs  = {3: "1.4rem",         2: "1.15rem",         1: ".95rem"}[grav]

    metric  = dom.get("metric", "—")
    met_html = (
        f'<div style="font-size:{met_fs};font-weight:900;color:{t["c"]};'
        f'font-family:"JetBrains Mono",monospace;letter-spacing:-.03em;'
        f'line-height:1;margin:6px 0 5px">{metric}</div>'
        if metric != "—" else '<div style="height:4px"></div>'
    )

    dot_anim = (
        f'animation:qcc-pulse 1.9s ease-in-out infinite' if act == "activo" else ""
    )
    dot_opacity = "1" if act in ("activo", "monitoreo") else "0.25"
    dot = (
        f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
        f'background:{t["c"]};flex-shrink:0;margin-top:3px;opacity:{dot_opacity};'
        f'{dot_anim}"></span>'
    )

    if not accessible:
        return f"""
<div style="background:{t['bg']};border:1px solid {t['bd']};border-radius:9px;
            padding:{pad};margin-bottom:8px;opacity:.35;cursor:not-allowed">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px">
    <div style="font-size:{nomb_fs};font-weight:700;color:#DDE4EE;line-height:1.2;flex:1">
      {dom['nombre']}</div>{dot}
  </div>
  {met_html}
  <div style="font-size:{nota_fs};color:rgba(255,255,255,.30);line-height:1.4">
    {dom['nota']}</div>
  <div style="font-size:8px;color:rgba(255,255,255,.16);margin-top:3px;
              letter-spacing:.04em;text-transform:uppercase">Sección técnica</div>
</div>"""

    return f"""
<div onclick="qNav('{mod}')"
     style="background:{t['bg']};border:1px solid {t['bd']};border-radius:9px;
            padding:{pad};margin-bottom:8px;cursor:pointer;
            transition:border-color .15s,background .15s,transform .12s"
     onmouseover="this.style.borderColor='{t['c']}';this.style.background='{t['bg'].replace('.10',',.16').replace('.09',',.14').replace('.07',',.12').replace('.05',',.10')}'"
     onmouseout="this.style.borderColor='{t['bd']}';this.style.background='{t['bg']}'">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px">
    <div style="font-size:{nomb_fs};font-weight:700;color:#DDE4EE;line-height:1.2;flex:1">
      {dom['nombre']}</div>{dot}
  </div>
  {met_html}
  <div style="font-size:{nota_fs};color:rgba(255,255,255,.32);line-height:1.4">
    {dom['nota']}</div>
</div>"""


def _domain_grid() -> str:
    """4 columnas de dominios (una por capa)."""
    cols_html = []
    is_tec = is_tecnico()

    for capa_cfg in _CAPAS:
        accent = capa_cfg["accent"]
        capa_doms = [d for d in _DOMAINS if d["capa"] == capa_cfg["id"]]
        cards = "".join(
            _domain_card(dom, accessible=not dom.get("tec", False) or is_tec)
            for dom in capa_doms
        )
        cols_html.append(f"""
<div style="flex:1;min-width:0">
  <div style="font-size:8px;font-weight:800;letter-spacing:.14em;
              text-transform:uppercase;color:{accent};
              border-bottom:1px solid {accent}28;
              padding-bottom:7px;margin-bottom:9px">{capa_cfg['label']}</div>
  {cards}
</div>""")

    return f"""
<div style="display:flex;gap:10px">
  {''.join(cols_html)}
</div>"""


def _bottom_band() -> str:
    """Banda inferior dinámica — sparklines + sistema + corte."""
    from config import GAD_NOMBRE, CORTE
    return f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-top:10px;padding:10px 14px;
            background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);
            border-radius:8px">
  <div style="display:flex;align-items:center;gap:16px">
    <div style="display:flex;align-items:center;gap:6px">
      <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;
                   display:inline-block;animation:qcc-pulse 2s ease-in-out infinite"></span>
      <span style="font-size:9px;color:rgba(255,255,255,.35);letter-spacing:.04em">
        Sistema operativo</span>
    </div>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:9px;color:rgba(255,255,255,.28);font-family:'JetBrains Mono',monospace">
      {GAD_NOMBRE}</span>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:9px;color:rgba(255,255,255,.25);letter-spacing:.04em">
      Corte {CORTE}</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <span style="font-size:8px;color:rgba(255,255,255,.18);letter-spacing:.06em;
                 text-transform:uppercase">QUIRA Intelligence</span>
    <span style="font-size:8px;color:rgba(255,255,255,.12)">·</span>
    <span style="font-size:8px;color:rgba(255,255,255,.14);font-family:'JetBrains Mono',monospace">
      Dylus Lab © 2026</span>
  </div>
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# CSS — Teatro Operacional
# ══════════════════════════════════════════════════════════════════════════════

_CANVAS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
  --navy:#0A1128; --navy-card:#0d1430; --cyan:#00D4FF;
  --green:#00E096; --amber:#FFB800; --red:#FF4D6D;
  --purple:#7C5CFC; --white:#E2E8F0; --muted:rgba(255,255,255,.30);
  --divider:rgba(255,255,255,.06);
}
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html,body {
  background:#0a0f1e;
  color:var(--white);
  font-family:'Inter',sans-serif;
  font-size:13px;
  overflow-x:hidden;
  scrollbar-width:none;
  -ms-overflow-style:none;
}
html::-webkit-scrollbar,body::-webkit-scrollbar { display:none; }
body { padding:12px 14px 16px; }

/* Animación pulso */
@keyframes qcc-pulse {
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:.25;transform:scale(.7)}
}
@keyframes fadeIn {
  from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none}
}

/* Layout principal */
.cc-middle {
  display:flex;
  gap:10px;
  min-height:420px;
}
.cc-left-rail {
  width:310px;
  min-width:280px;
  flex-shrink:0;
  display:flex;
  flex-direction:column;
  gap:8px;
}
.cc-right {
  flex:1;
  min-width:0;
  overflow:hidden;
}

/* GeoTwin iframe */
.geotwin-frame {
  width:100%;
  height:100%;
  min-height:360px;
  border:1px solid rgba(0,212,255,.12);
  border-radius:10px;
  background:#0a0f1e;
}

/* Rail header */
.rail-hdr {
  display:flex;
  align-items:center;
  gap:8px;
  padding:8px 10px;
  background:rgba(0,212,255,.04);
  border:1px solid rgba(0,212,255,.10);
  border-radius:8px;
}

/* Botón logout */
.btn-logout {
  display:inline-flex;
  align-items:center;
  gap:5px;
  padding:5px 12px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  border-radius:6px;
  font-size:9px;
  font-weight:600;
  color:rgba(255,255,255,.35);
  letter-spacing:.04em;
  cursor:pointer;
  text-transform:uppercase;
  transition:background .15s,color .15s;
}
.btn-logout:hover {
  background:rgba(239,68,68,.08);
  border-color:rgba(239,68,68,.25);
  color:#EF4444;
}

/* Mobile */
@media (max-width:768px) {
  .cc-middle { flex-direction:column; }
  .cc-left-rail { width:100%; min-width:0; }
  .geotwin-frame { min-height:260px; }
}
"""

_BRIDGE_JS = """
<script>
function qNav(dest) {
  window.parent.postMessage({type:'quira_nav', dest:dest}, '*');
}
function qLogout() {
  window.parent.postMessage({type:'quira_action', action:'logout'}, '*');
}

// Recibe mensajes del puente JS externo (por si el bridge usa este frame como relay)
window.addEventListener('message', function(e) {
  if (!e.data) return;
});
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# ENSAMBLADO DE CANVAS
# ══════════════════════════════════════════════════════════════════════════════

def _build_canvas(d: dict) -> str:
    """Ensambla el HTML del teatro operacional completo."""
    from config import GAD_NOMBRE, ALCALDE, CORTE

    map_src = _get_map_html()

    # Header del rail — identidad territorial
    rol = get_rol()
    header_html = f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-bottom:8px;padding:0 2px">
  <div style="display:flex;align-items:center;gap:8px">
    <span style="font-size:14px;font-weight:900;color:#00D4FF;letter-spacing:-.02em">
      ⬡ QUIRA</span>
    <span style="font-size:9px;color:rgba(255,255,255,.30);letter-spacing:.06em;
                 text-transform:uppercase">Intelligence</span>
    <span style="font-size:9px;font-weight:700;color:#00D4FF;
                 background:rgba(0,212,255,.10);border:1px solid rgba(0,212,255,.20);
                 border-radius:5px;padding:2px 8px;letter-spacing:.04em">{rol}</span>
  </div>
  <button class="btn-logout" onclick="qLogout()">⎋ Cerrar Sesión</button>
</div>"""

    # GeoTwin rail content
    if map_src:
        geotwin_html = f"""
<div style="font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
            color:rgba(0,212,255,.50);margin-bottom:6px;display:flex;
            align-items:center;gap:6px">
  <span style="width:2px;height:10px;background:#00D4FF;border-radius:1px;
               display:inline-block"></span>
  TERRITORIO MUNICIPAL
  <span style="color:rgba(255,255,255,.18);margin-left:auto;
               font-family:'JetBrains Mono',monospace;font-size:8px;font-weight:400">
    7 parroquias</span>
</div>
<iframe src="{map_src}"
        class="geotwin-frame"
        frameborder="0"
        scrolling="no"
        style="flex:1"
        title="GeoTwin Montecristi"></iframe>"""
    else:
        geotwin_html = """
<div style="flex:1;min-height:360px;display:flex;align-items:center;
            justify-content:center;background:rgba(255,255,255,.02);
            border:1px solid rgba(255,255,255,.06);border-radius:10px;
            flex-direction:column;gap:8px">
  <span style="font-size:20px;opacity:.25">🗺</span>
  <span style="font-size:11px;color:rgba(255,255,255,.22)">Mapa no disponible</span>
</div>"""

    # Meta-info bajo el mapa
    meta_html = f"""
<div style="padding:8px 10px;background:rgba(0,212,255,.03);
            border:1px solid rgba(0,212,255,.08);border-radius:8px">
  <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,.50);
              margin-bottom:4px">{GAD_NOMBRE}</div>
  <div style="font-size:8px;color:rgba(255,255,255,.28);line-height:1.6">
    {ALCALDE}<br>
    <span style="color:rgba(0,212,255,.45);font-family:'JetBrains Mono',monospace">
      Corte {CORTE}</span>
  </div>
</div>"""

    # Sección de capas — encabezado
    capas_hdr = """
<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
  <span style="width:2px;height:12px;background:#7C5CFC;border-radius:1px;
               display:inline-block"></span>
  <span style="font-size:8px;font-weight:800;letter-spacing:.14em;
               text-transform:uppercase;color:rgba(255,255,255,.35)">
    CAPAS OPERACIONALES</span>
  <span style="font-size:8px;color:rgba(255,255,255,.16);margin-left:auto;
               font-family:'JetBrains Mono',monospace">13 dominios · click para abrir</span>
</div>"""

    canvas = f"""
<div style="animation:fadeIn .22s ease">
  {header_html}
  {_kpi_band(d)}
  <div class="cc-middle">
    <div class="cc-left-rail">
      {geotwin_html}
      {meta_html}
    </div>
    <div class="cc-right">
      {capas_hdr}
      {_domain_grid()}
    </div>
  </div>
  {_bottom_band()}
</div>"""

    return (
        "<!DOCTYPE html><html lang='es'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{_CANVAS_CSS}</style>"
        "</head>"
        f"<body>{canvas}{_BRIDGE_JS}"
        # Auto-resize
        """<script>
(function(){
  function h(){
    var s=Math.max(
      document.body?document.body.scrollHeight:0,
      document.documentElement?document.documentElement.scrollHeight:0);
    if(s>0) window.parent.postMessage(
      {isStreamlitMessage:true,type:'streamlit:setFrameHeight',height:s},'*');
  }
  h(); document.addEventListener('DOMContentLoaded',h);
  window.addEventListener('load',h);
  setTimeout(h,150); setTimeout(h,600); setTimeout(h,1400);
})();
</script>"""
        "</body></html>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# JS BRIDGE — escucha postMessage del canvas y dispara botones ocultos
# ══════════════════════════════════════════════════════════════════════════════

_NAV_TARGETS = [
    "situacion", "cooperacion", "alertas", "municipal", "concejo",
    "analisis", "geotwin", "rdc", "confianza", "genero",
    "ods", "control",
]

_BRIDGE_SCRIPT = """
<script>
(function(){
  function dispatch(dest, action){
    var btns = window.parent.document.querySelectorAll(
      '[data-testid="stBaseButton-secondary"]');
    var token = action === 'logout' ? '__QLOGOUT__' : '__QNAV_' + dest + '__';
    for(var i=0;i<btns.length;i++){
      if(btns[i].innerText.trim() === token){ btns[i].click(); return; }
    }
  }
  window.addEventListener('message', function(e){
    if(!e.data) return;
    if(e.data.type === 'quira_nav')    dispatch(e.data.dest, 'nav');
    if(e.data.type === 'quira_action') dispatch(null, e.data.action);
  });

  // Ocultar todos los botones funcionales ocultos
  function hideHidden(){
    var btns = window.parent.document.querySelectorAll(
      '[data-testid="stBaseButton-secondary"]');
    for(var i=0;i<btns.length;i++){
      var t = btns[i].innerText.trim();
      if(t.startsWith('__Q') && t.endsWith('__')){
        var b = btns[i];
        b.style.cssText=[
          'width:0!important','height:0!important',
          'padding:0!important','margin:0!important',
          'border:none!important','overflow:hidden!important',
          'position:absolute!important','opacity:0!important',
          'pointer-events:none!important'
        ].join(';');
        if(b.parentElement)
          b.parentElement.style.cssText=
            'width:0!important;height:0!important;overflow:hidden!important';
      }
    }
  }
  setTimeout(hideHidden, 80);
  setTimeout(hideHidden, 350);
  setTimeout(hideHidden, 900);
})();
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Renderiza el Centro de Mando Unificado — teatro operacional único."""

    # ── Ocultar sidebar completamente para el Ejecutivo ───────────────────────
    st.markdown("""
<style>
/* Sprint 1.2: Sidebar invisible — Streamlit como runtime, no como UI */
[data-testid="stSidebar"] {
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
  overflow: hidden !important;
}
/* Expandir main al 100% del viewport sin sidebar */
.main .block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
  max-width: 100% !important;
  width: 100% !important;
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
  padding-top: 0.25rem !important;
}
/* Quitar el botón de colapsar sidebar */
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
  display: none !important;
}
/* Quitar padding top de Streamlit */
section[data-testid="stMainBlockContainer"] > div:first-child {
  padding-top: 4px !important;
}
</style>
""", unsafe_allow_html=True)

    # ── Datos ─────────────────────────────────────────────────────────────────
    data = _load_data()

    # ── Canvas HTML principal ─────────────────────────────────────────────────
    html = _build_canvas(data)
    _cv1.html(html, height=820, scrolling=False)

    # ── Bridge JS — escucha postMessage del canvas ────────────────────────────
    _cv1.html(_BRIDGE_SCRIPT, height=0)

    # ── Botones funcionales ocultos — dispatch real de navegación ─────────────
    # Cada destino tiene su token __QNAV_xxx__
    # El bridge JS encuentra el token y hace click
    _cols = st.columns(len(_NAV_TARGETS) + 1)
    for i, dest in enumerate(_NAV_TARGETS):
        with _cols[i]:
            if st.button(f"__QNAV_{dest}__", key=f"_qnav_{dest}",
                         use_container_width=True):
                if dest == "concejo":
                    # Panel Estratégico: cambiar modo dentro del flujo ejecutivo
                    st.session_state["ejecutivo_modo"] = "concejo"
                    st.session_state["gov_module"] = "inicio"
                else:
                    st.session_state["gov_module"] = dest
                    st.session_state["ejecutivo_modo"] = "vista"
                st.rerun()

    with _cols[-1]:
        if st.button("__QLOGOUT__", key="_qlogout", use_container_width=True):
            logout()
            st.rerun()
