"""
QUIRA Intelligence — Centro de Mando  (Sprint D.3 · 12 Dominios Canónicos)
Teatro Operacional · GAD Montecristi · Holding Municipal

Arquitectura D.3:
  · 12 dominios canónicos en grilla 4×3 — sin capas improvisadas
  · GeoTwin = card 10 con SVG estático (no Folium en canvas)
  · Glow pulsante en cards críticas: 04 / 06 / 12
  · Card 11 dimmed — Ecosistema Productivo en construcción
  · KPI band corregida: "Cumplimiento Institucional"
  · Left rail eliminado — domain grid ocupa 100% del ancho
  · QUIRA AI = botón invocable en status bar (no panel fijo)
  · No scroll · HTML Canvas full-viewport · postMessage bridge

"QUIRA entiende relaciones institucionales."
Dylus Lab © 2026
"""
from __future__ import annotations

import json
from typing import Any

import streamlit as st
import streamlit.components.v1 as _cv1

from utils.cache_quira import cargar_gm_snapshot, cargar_snapshot
from utils.css_tokens import C
from utils.session import get_rol, logout


# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE TEMPERATURA
# ══════════════════════════════════════════════════════════════════════════════
_TEMP: dict[str, dict[str, str]] = {
    "critico": {"bg": "rgba(239,68,68,.10)",   "bd": "rgba(239,68,68,.35)",   "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.09)",  "bd": "rgba(249,115,22,.30)",  "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.05)",   "bd": "rgba(0,212,255,.16)",   "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.07)",   "bd": "rgba(34,197,94,.24)",   "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.10)",  "bd": "rgba(124,92,252,.32)",  "c": "#7C5CFC"},
    "dim":     {"bg": "rgba(255,255,255,.02)", "bd": "rgba(255,255,255,.07)", "c": "#64748B"},
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG ESTÁTICO — Cantón Montecristi (7 parroquias)
# Thumbnail inline para la card Dom 10 — no Folium, no dependencias externas
# ══════════════════════════════════════════════════════════════════════════════
_CANTON_SVG = """
<svg viewBox="0 0 200 160" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:80px;display:block;margin:4px 0">
  <defs>
    <radialGradient id="bg_grd" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0f2040" stop-opacity="1"/>
      <stop offset="100%" stop-color="#060d1a" stop-opacity="1"/>
    </radialGradient>
  </defs>
  <!-- Fondo -->
  <rect width="200" height="160" fill="url(#bg_grd)" rx="6"/>
  <!-- Silueta simplificada cantón -->
  <polygon points="30,120 50,95 45,70 65,55 90,50 120,48 145,55 160,75 155,100 140,120 110,130 80,132 55,128"
           fill="rgba(0,140,255,.12)" stroke="rgba(0,140,255,.35)" stroke-width="1.2"/>
  <!-- Parroquias — puntos con color por estado -->
  <!-- Montecristi cabecera — ALERTA -->
  <circle cx="95" cy="88" r="7" fill="#F97316" fill-opacity=".75"/>
  <circle cx="95" cy="88" r="11" fill="none" stroke="#F97316" stroke-width="1" stroke-opacity=".35"/>
  <!-- Crucita — NORMAL -->
  <circle cx="50" cy="80" r="4" fill="#00D4FF" fill-opacity=".65"/>
  <!-- La Pila — NORMAL -->
  <circle cx="70" cy="65" r="3.5" fill="#00D4FF" fill-opacity=".60"/>
  <!-- Chirijos — PRIORIDAD -->
  <circle cx="125" cy="70" r="4.5" fill="#EF4444" fill-opacity=".70"/>
  <!-- Noboa — NORMAL -->
  <circle cx="140" cy="95" r="3.5" fill="#00D4FF" fill-opacity=".55"/>
  <!-- San Sebastián — ALERTA -->
  <circle cx="108" cy="110" r="4" fill="#F97316" fill-opacity=".65"/>
  <!-- Leonidas Plaza — NORMAL -->
  <circle cx="60" cy="108" r="3" fill="#00D4FF" fill-opacity=".55"/>
  <!-- Labels -->
  <text x="95" y="82" text-anchor="middle" font-size="7" fill="#E2E8F0"
        font-family="Inter,system-ui,sans-serif" font-weight="700">MCR</text>
  <text x="50" y="74" text-anchor="middle" font-size="5.5" fill="rgba(255,255,255,.55)"
        font-family="Inter,system-ui,sans-serif">Crucita</text>
  <text x="125" y="64" text-anchor="middle" font-size="5.5" fill="rgba(255,255,255,.55)"
        font-family="Inter,system-ui,sans-serif">Chirijos</text>
  <!-- Título -->
  <text x="100" y="150" text-anchor="middle" font-size="7.5" fill="rgba(0,212,255,.55)"
        font-family="Inter,system-ui,sans-serif" font-weight="600" letter-spacing=".05em">
    CANTÓN MONTECRISTI · 7 PARROQUIAS</text>
</svg>
"""

# ══════════════════════════════════════════════════════════════════════════════
# 12 DOMINIOS CANÓNICOS
# Arquitectura: architecture_quira_v1.md v2.0 (CONGELADO 2026-05-29)
# Regla: ningún nombre interno en labels públicos (ICPI, TGI, SAT, Ti, H73...)
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_12: list[dict] = [
    # ── Fila 1 ────────────────────────────────────────────────────────────────
    {
        "id": "d01", "num": "01",
        "nombre": "Planificación Estratégica",
        "metric": "17 ODS activos",
        "nota": "PDOT 2023–2027 · en seguimiento",
        "temp": "verde",
        "mod": "ods",
    },
    {
        "id": "d02", "num": "02",
        "nombre": "Presupuesto & Financiamiento",
        "metric": "$3.66M",
        "nota": "Fondos condicionados · 3 fuentes activas",
        "temp": "funds",
        "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03",
        "nombre": "Seguimiento de Metas",
        "metric": "en carga…",
        "nota": "56 metas canónicas PDOT",
        "temp": "alerta",
        "mod": "situacion",
        "pending": True,
    },
    # ── Fila 2 ────────────────────────────────────────────────────────────────
    {
        "id": "d04", "num": "04",
        "nombre": "Alertas Institucionales",
        "metric_key": "n_alertas",
        "metric_suffix": " activas",
        "nota": "Intervención inmediata requerida",
        "temp": "critico",
        "mod": "alertas",
        "glow": True,
    },
    {
        "id": "d05", "num": "05",
        "nombre": "Holding Municipal",
        "metric_key": "hold_avg",
        "metric_suffix": "%",
        "nota": "EP Aseo · Bomberos · Patronato · GAD",
        "temp": "alerta",
        "mod": "municipal",
    },
    {
        "id": "d06", "num": "06",
        "nombre": "Salud Institucional",
        "metric_key": "icpi_pct",
        "metric_suffix": "%",
        "nota": "Brecha de ejecución · umbral 65%",
        "temp": "critico",
        "mod": "situacion",
        "glow": True,
        "featured": True,
    },
    # ── Fila 3 ────────────────────────────────────────────────────────────────
    {
        "id": "d07", "num": "07",
        "nombre": "Transparencia",
        "metric": "21 art. LOTAIP",
        "nota": "Gobierno abierto · publicación activa",
        "temp": "normal",
        "mod": "municipal",
    },
    {
        "id": "d08", "num": "08",
        "nombre": "Participación Ciudadana",
        "metric": "27.98%",
        "nota": "Gestión participativa · 6 mecanismos",
        "temp": "alerta",
        "mod": "confianza",
    },
    {
        "id": "d09", "num": "09",
        "nombre": "Rendición de Cuentas",
        "metric": "Agosto 2026",
        "nota": "Preparación en curso · CPCCS",
        "temp": "alerta",
        "mod": "rdc",
    },
    # ── Fila 4 ────────────────────────────────────────────────────────────────
    {
        "id": "d10", "num": "10",
        "nombre": "Territorio & Cobertura",
        "metric": "$40/hab rural",
        "nota": "7 parroquias · brecha territorial activa",
        "temp": "critico",
        "mod": "geotwin",
        "has_map": True,
    },
    {
        "id": "d11", "num": "11",
        "nombre": "Ecosistema Productivo Territorial",
        "metric": "—",
        "nota": "Datos en construcción",
        "temp": "dim",
        "mod": None,
        "disabled": True,
    },
    {
        "id": "d12", "num": "12",
        "nombre": "Protección Social & Grupos Prioritarios",
        "metric": "12.83%",
        "nota": "Presupuesto social · umbral 30% · Art. 35",
        "temp": "critico",
        "mod": "genero",
        "glow": True,
    },
]


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
# KPI BAND — 4 tiles superiores (fuente canónica de métricas)
# ══════════════════════════════════════════════════════════════════════════════

def _kpi_band(d: dict) -> str:
    """Banda de 4 KPI tiles con onclick → módulo."""
    icpi_pct  = d.get("icpi_pct")
    n_alertas = d.get("n_alertas", 0)
    riesgo_cl = d.get("riesgo_clasif", "—")
    hold_avg  = d.get("hold_avg", 68.7)

    icpi_color  = C.sem(icpi_pct) if icpi_pct is not None else "#EF4444"
    alert_color = "#EF4444" if n_alertas > 0 else "#22C55E"
    hold_color  = C.sem(hold_avg)

    icpi_str   = f"{icpi_pct:.1f}%" if icpi_pct is not None else "17.4%"
    alert_str  = str(n_alertas) if n_alertas >= 0 else "0"
    riesgo_str = riesgo_cl if riesgo_cl not in ("—", "") else "Sin alertas críticas"

    def _tile(label: str, val: str, color: str, sub: str,
              dest: str, size: str = "lg") -> str:
        fs = "2.0rem" if size == "lg" else "1.5rem"
        pt = "16px 18px 12px" if size == "lg" else "13px 15px 10px"
        return f"""
<div onclick="qNav('{dest}')"
     style="background:rgba(8,13,24,.97);border:1px solid {color}28;
            border-top:2px solid {color};border-radius:10px;
            padding:{pt};cursor:pointer;flex:1;min-width:0;
            transition:border-color .18s,background .18s"
     onmouseover="this.style.background='rgba(0,212,255,.04)'"
     onmouseout="this.style.background='rgba(8,13,24,.97)'">
  <div style="font-size:7.5px;font-weight:700;letter-spacing:.10em;
              text-transform:uppercase;color:rgba(255,255,255,.28);
              margin-bottom:9px">{label}</div>
  <div style="font-size:{fs};font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.04em;line-height:1;
              margin-bottom:7px">{val}</div>
  <div style="font-size:8.5px;color:rgba(255,255,255,.28);
              letter-spacing:.01em;line-height:1.4">{sub}</div>
</div>"""

    return f"""
<div style="display:flex;gap:10px;margin-bottom:12px">
  {_tile("Cumplimiento Institucional", icpi_str, icpi_color,
         d.get("icpi_clasif","—") + " · umbral 65%", "situacion", "lg")}
  {_tile("Fondos en Riesgo", "$3.66M", "#7C5CFC",
         "3 fuentes condicionadas · acción requerida", "cooperacion", "lg")}
  {_tile("Alertas Activas", alert_str, alert_color, riesgo_str, "alertas", "sm")}
  {_tile("Holding Municipal", f"{hold_avg:.1f}%", hold_color,
         "Promedio entidades · click para detalle", "municipal", "sm")}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN CARD — una tarjeta por dominio
# ══════════════════════════════════════════════════════════════════════════════

def _resolve_metric(dom: dict, data: dict) -> str:
    """Resuelve el valor de métrica: fijo o desde snapshot."""
    key = dom.get("metric_key")
    if key:
        val = data.get(key)
        if val is not None:
            suffix = dom.get("metric_suffix", "")
            if isinstance(val, float):
                return f"{val:.1f}{suffix}"
            return f"{val}{suffix}"
    return dom.get("metric", "—")


def _domain_card(dom: dict, data: dict) -> str:
    """Genera el HTML de una tarjeta de dominio."""
    t        = _TEMP.get(dom["temp"], _TEMP["normal"])
    mod      = dom.get("mod")
    disabled = dom.get("disabled", False)
    has_map  = dom.get("has_map", False)
    glow     = dom.get("glow", False)
    featured = dom.get("featured", False)
    pending  = dom.get("pending", False)

    metric = _resolve_metric(dom, data)

    num_badge = (
        f'<span style="font-size:7px;font-weight:800;color:{t["c"]};'
        f'background:{t["c"]}1A;border:1px solid {t["c"]}33;'
        f'border-radius:4px;padding:1px 5px;flex-shrink:0;'
        f'letter-spacing:.04em">{dom["num"]}</span>'
    )

    nombre_html = (
        f'<div style="font-size:11.5px;font-weight:700;color:#DDE4EE;'
        f'line-height:1.25;flex:1">{dom["nombre"]}</div>'
    )

    # Métrica — solo si existe y no es placeholder
    if metric != "—" and not pending:
        met_html = (
            f'<div style="font-size:1.25rem;font-weight:900;color:{t["c"]};'
            f'font-family:"JetBrains Mono",monospace;letter-spacing:-.03em;'
            f'line-height:1;margin:6px 0 5px">{metric}</div>'
        )
    else:
        met_html = '<div style="height:6px"></div>'

    nota_html = (
        f'<div style="font-size:8.5px;color:rgba(255,255,255,.32);'
        f'line-height:1.45;margin-top:2px">{dom["nota"]}</div>'
    )

    # SVG mapa para Dom 10
    map_html = _CANTON_SVG if has_map else ""

    # Dot de estado
    dot = (
        f'<span style="width:5px;height:5px;border-radius:50%;'
        f'background:{t["c"]};display:inline-block;flex-shrink:0;'
        f'margin-top:3px;opacity:{"1" if not disabled else "0.3"};'
        f'{"animation:qcc-pulse 2s ease-in-out infinite" if not disabled else ""}"></span>'
    )

    # Card deshabilitada (Dom 11)
    if disabled:
        return f"""
<div style="background:{t["bg"]};border:1px solid {t["bd"]};
            border-radius:9px;padding:11px 12px 10px;
            opacity:.38;cursor:not-allowed;min-height:80px">
  <div style="display:flex;align-items:flex-start;
              justify-content:space-between;gap:5px;margin-bottom:5px">
    {num_badge}{nombre_html}{dot}
  </div>
  {nota_html}
  <div style="font-size:7.5px;color:rgba(255,255,255,.18);margin-top:5px;
              text-transform:uppercase;letter-spacing:.06em">En construcción</div>
</div>"""

    # Glow keyframe via style attr (cards 04, 06, 12)
    glow_style = (
        'animation:qcc-glow 2.2s ease-in-out infinite;'
        if glow else ""
    )
    strong_glow = (
        'animation:qcc-glow-strong 2s ease-in-out infinite;'
        if featured else ""
    )

    return f"""
<div onclick="qNav('{mod}')"
     style="background:{t["bg"]};border:1px solid {t["bd"]};
            border-radius:9px;padding:11px 12px 10px;
            cursor:pointer;min-height:80px;
            transition:border-color .15s,background .15s;
            {glow_style}{strong_glow}"
     onmouseover="this.style.borderColor='{t["c"]}80';this.style.background='{t["bg"].replace("rgba(","rgba(").replace(".10",",.18").replace(".09",",.16").replace(".07",",.13").replace(".05",",.11").replace(".02",",.07")}'"
     onmouseout="this.style.borderColor='{t["bd"]}';this.style.background='{t["bg"]}'">
  <div style="display:flex;align-items:flex-start;
              justify-content:space-between;gap:5px;margin-bottom:5px">
    {num_badge}{nombre_html}{dot}
  </div>
  {map_html}
  {met_html}
  {nota_html}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN GRID — grilla 4×3 (4 filas · 3 columnas)
# ══════════════════════════════════════════════════════════════════════════════

def _domain_grid(data: dict) -> str:
    """Genera la grilla 4×3 de los 12 dominios canónicos."""
    # Agrupar en filas de 3
    rows_html = []
    for row_start in range(0, 12, 3):
        row_doms = _DOMAINS_12[row_start: row_start + 3]
        cards = "".join(_domain_card(dom, data) for dom in row_doms)
        rows_html.append(f"""
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;
            margin-bottom:9px">
  {cards}
</div>""")

    return "".join(rows_html)


# ══════════════════════════════════════════════════════════════════════════════
# BOTTOM BAND
# ══════════════════════════════════════════════════════════════════════════════

def _bottom_band() -> str:
    from config import GAD_NOMBRE, CORTE
    return f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-top:10px;padding:9px 13px;
            background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.05);
            border-radius:8px">
  <div style="display:flex;align-items:center;gap:14px">
    <div style="display:flex;align-items:center;gap:5px">
      <span style="width:6px;height:6px;border-radius:50%;background:#22C55E;
                   display:inline-block;animation:qcc-pulse 2s ease-in-out infinite"></span>
      <span style="font-size:8.5px;color:rgba(255,255,255,.35);letter-spacing:.04em">
        Sistema operativo</span>
    </div>
    <span style="font-size:8.5px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.30);
                 font-family:'JetBrains Mono',monospace">{GAD_NOMBRE}</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.26);letter-spacing:.04em">
      Corte {CORTE}</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <span style="font-size:7.5px;color:rgba(255,255,255,.18);letter-spacing:.06em;
                 text-transform:uppercase">QUIRA Intelligence</span>
    <span style="font-size:7.5px;color:rgba(255,255,255,.12)">·</span>
    <span style="font-size:7.5px;color:rgba(255,255,255,.15);
                 font-family:'JetBrains Mono',monospace">Dylus Lab © 2026</span>
  </div>
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# CSS — Teatro Operacional D.3
# ══════════════════════════════════════════════════════════════════════════════

_CANVAS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
  --navy:#0A1128; --cyan:#00D4FF;
  --green:#00E096; --amber:#FFB800; --red:#FF4D6D;
  --purple:#7C5CFC; --white:#E2E8F0; --muted:rgba(255,255,255,.30);
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
body { padding:12px 14px 14px; }

/* Animaciones */
@keyframes qcc-pulse {
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:.25;transform:scale(.7)}
}
@keyframes fadeIn {
  from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none}
}
@keyframes qcc-glow {
  0%,100%{box-shadow:0 0 6px rgba(239,68,68,.30)}
  50%{box-shadow:0 0 16px rgba(239,68,68,.60),0 0 6px rgba(239,68,68,.25)}
}
@keyframes qcc-glow-strong {
  0%,100%{box-shadow:0 0 10px rgba(239,68,68,.40),0 0 20px rgba(239,68,68,.15)}
  50%{box-shadow:0 0 22px rgba(239,68,68,.75),0 0 40px rgba(239,68,68,.20)}
}

/* Botón logout */
.btn-logout {
  display:inline-flex;align-items:center;gap:5px;
  padding:4px 11px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);
  border-radius:6px;
  font-size:8.5px;font-weight:600;
  color:rgba(255,255,255,.32);
  letter-spacing:.04em;cursor:pointer;
  text-transform:uppercase;
  transition:background .15s,color .15s;
}
.btn-logout:hover {
  background:rgba(239,68,68,.08);
  border-color:rgba(239,68,68,.22);
  color:#EF4444;
}

/* Botón QUIRA AI */
.btn-quira-ai {
  display:inline-flex;align-items:center;gap:5px;
  padding:4px 11px;
  background:rgba(0,212,255,.06);
  border:1px solid rgba(0,212,255,.18);
  border-radius:6px;
  font-size:8.5px;font-weight:600;
  color:rgba(0,212,255,.65);
  letter-spacing:.04em;cursor:pointer;
  transition:background .15s,color .15s;
}
.btn-quira-ai:hover {
  background:rgba(0,212,255,.12);
  color:#00D4FF;
}

/* Mobile */
@media (max-width:768px) {
  body { padding:8px 10px 10px; }
}
"""

_BRIDGE_JS = """
<script>
function qNav(dest) {
  if(!dest) return;
  window.parent.postMessage({type:'quira_nav', dest:dest}, '*');
}
function qLogout() {
  window.parent.postMessage({type:'quira_action', action:'logout'}, '*');
}
function qQuiraAI() {
  window.parent.postMessage({type:'quira_action', action:'quira_ai'}, '*');
}
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# ENSAMBLADO DE CANVAS
# ══════════════════════════════════════════════════════════════════════════════

def _build_canvas(d: dict) -> str:
    """Ensambla el HTML del teatro operacional completo — D.3."""
    from config import GAD_NOMBRE, ALCALDE, CORTE

    rol = get_rol()

    # ── Header ────────────────────────────────────────────────────────────────
    header_html = f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-bottom:10px;padding:0 2px">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="font-size:15px;font-weight:900;color:#00D4FF;letter-spacing:-.02em">
      ⬡ QUIRA</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.28);letter-spacing:.06em;
                 text-transform:uppercase">Intelligence</span>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.35);font-weight:600;
                 letter-spacing:.04em">Centro de Mando</span>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:8.5px;color:rgba(255,255,255,.28);
                 font-family:'JetBrains Mono',monospace">{GAD_NOMBRE}</span>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <button class="btn-quira-ai" onclick="qQuiraAI()">
      ◎ Preguntar a QUIRA ▼</button>
    <span style="font-size:8.5px;font-weight:700;color:#00D4FF;
                 background:rgba(0,212,255,.10);border:1px solid rgba(0,212,255,.20);
                 border-radius:5px;padding:2px 8px;letter-spacing:.04em">{rol}</span>
    <button class="btn-logout" onclick="qLogout()">⎋ Salir</button>
  </div>
</div>"""

    # ── Status bar ────────────────────────────────────────────────────────────
    status_bar = f"""
<div style="display:flex;align-items:center;gap:14px;
            padding:5px 12px;margin-bottom:12px;
            background:rgba(255,255,255,.015);
            border:1px solid rgba(255,255,255,.04);border-radius:7px">
  <div style="display:flex;align-items:center;gap:5px">
    <span style="width:5px;height:5px;border-radius:50%;background:#22C55E;
                 display:inline-block;animation:qcc-pulse 2s ease-in-out infinite"></span>
    <span style="font-size:8px;color:rgba(255,255,255,.32);letter-spacing:.04em">
      EN LÍNEA</span>
  </div>
  <span style="font-size:8px;color:rgba(255,255,255,.15)">·</span>
  <span style="font-size:8px;color:rgba(255,255,255,.25);
               font-family:'JetBrains Mono',monospace">Corte {CORTE}</span>
  <span style="font-size:8px;color:rgba(255,255,255,.15)">·</span>
  <span style="font-size:8px;color:rgba(255,255,255,.22);letter-spacing:.04em">
    {ALCALDE}</span>
  <div style="margin-left:auto;font-size:7.5px;color:rgba(255,255,255,.18);
              letter-spacing:.06em;text-transform:uppercase">
    12 dominios · click para explorar</div>
</div>"""

    # ── Sección label dominios ─────────────────────────────────────────────────
    dom_header = """
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
  <span style="width:2px;height:10px;background:#7C5CFC;border-radius:1px;
               display:inline-block"></span>
  <span style="font-size:7.5px;font-weight:800;letter-spacing:.14em;
               text-transform:uppercase;color:rgba(255,255,255,.32)">
    DOMINIOS OPERACIONALES</span>
  <span style="font-size:7.5px;color:rgba(255,255,255,.14);margin-left:auto;
               font-family:'JetBrains Mono',monospace">
    Holding Municipal Montecristi · Q1-2026</span>
</div>"""

    canvas = f"""
<div style="animation:fadeIn .22s ease">
  {header_html}
  {_kpi_band(d)}
  {status_bar}
  {dom_header}
  {_domain_grid(d)}
  {_bottom_band()}
</div>"""

    return (
        "<!DOCTYPE html><html lang='es'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{_CANVAS_CSS}</style>"
        "</head>"
        f"<body>{canvas}{_BRIDGE_JS}"
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
  setTimeout(h,120); setTimeout(h,500); setTimeout(h,1200);
})();
</script>"""
        "</body></html>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# JS BRIDGE — escucha postMessage del canvas y dispara botones ocultos
# ══════════════════════════════════════════════════════════════════════════════

_NAV_TARGETS = [
    "situacion", "cooperacion", "alertas", "municipal",
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
    if(e.data.type === 'quira_action') {
      if(e.data.action === 'logout') dispatch(null, 'logout');
    }
  });

  // Ocultar botones funcionales del DOM visible
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
    """Renderiza el Centro de Mando — 12 dominios canónicos · Sprint D.3."""

    # CSS Streamlit: sidebar invisible, main 100%
    st.markdown("""
<style>
[data-testid="stSidebar"] {
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
  overflow: hidden !important;
}
.main .block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
  max-width: 100% !important;
  width: 100% !important;
  padding-left: 0.5rem !important;
  padding-right: 0.5rem !important;
  padding-top: 0.25rem !important;
}
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
  display: none !important;
}
section[data-testid="stMainBlockContainer"] > div:first-child {
  padding-top: 4px !important;
}
</style>
""", unsafe_allow_html=True)

    # Datos
    data = _load_data()

    # Canvas HTML
    html = _build_canvas(data)
    _cv1.html(html, height=860, scrolling=False)

    # Bridge JS
    _cv1.html(_BRIDGE_SCRIPT, height=0)

    # Botones funcionales ocultos — dispatch de navegación
    _cols = st.columns(len(_NAV_TARGETS) + 1)
    for i, dest in enumerate(_NAV_TARGETS):
        with _cols[i]:
            if st.button(f"__QNAV_{dest}__", key=f"_qnav_{dest}",
                         use_container_width=True):
                st.session_state["gov_module"] = dest
                st.session_state["ejecutivo_modo"] = "vista"
                st.rerun()

    with _cols[-1]:
        if st.button("__QLOGOUT__", key="_qlogout", use_container_width=True):
            logout()
            st.rerun()
