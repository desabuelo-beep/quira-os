"""
QUIRA Intelligence — Centro de Mando  (Sprint D.3.1 · Visual Upgrade)
Teatro Operacional · GAD Montecristi · Holding Municipal

Mejoras D.3.1:
  · Botones QNAV ocultos via CSS Streamlit (no flicker)
  · Contraste tipográfico: labels al 65%, notas al 58%
  · Fuentes más grandes: nombres 13px, notas 10px, métricas 1.4rem
  · Status bar redundante eliminado
  · Dom 10 SVG contenido a 64px fijo — filas uniformes
  · Grilla con align-items:stretch para altura uniforme por fila
  · Notas específicas Montecristi, no genéricas

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
    "critico": {"bg": "rgba(239,68,68,.11)",   "bd": "rgba(239,68,68,.40)",   "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.10)",  "bd": "rgba(249,115,22,.35)",  "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.06)",   "bd": "rgba(0,212,255,.18)",   "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.08)",   "bd": "rgba(34,197,94,.28)",   "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.11)",  "bd": "rgba(124,92,252,.38)",  "c": "#7C5CFC"},
    "dim":     {"bg": "rgba(255,255,255,.025)","bd": "rgba(255,255,255,.08)", "c": "#64748B"},
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG ESTÁTICO — Cantón Montecristi · 7 parroquias
# Contenido a 64px fijo — no desborda la card
# ══════════════════════════════════════════════════════════════════════════════
_CANTON_SVG = """
<svg viewBox="0 0 240 100" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:64px;display:block;margin:5px 0 4px;flex-shrink:0">
  <defs>
    <radialGradient id="bg_g" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#0f2040"/>
      <stop offset="100%" stop-color="#060c18"/>
    </radialGradient>
  </defs>
  <rect width="240" height="100" fill="url(#bg_g)" rx="5"/>
  <!-- Silueta cantón -->
  <polygon points="30,80 52,60 48,42 72,30 100,26 135,25 162,33 178,52 172,72 155,84 122,90 88,92 60,86"
           fill="rgba(0,130,255,.10)" stroke="rgba(0,150,255,.30)" stroke-width="1.2"/>
  <!-- Montecristi cabecera -->
  <circle cx="108" cy="56" r="8" fill="#F97316" fill-opacity=".80"/>
  <circle cx="108" cy="56" r="13" fill="none" stroke="#F97316" stroke-width="1" stroke-opacity=".30"/>
  <text x="108" y="51" text-anchor="middle" font-size="7" fill="#fff"
        font-family="Inter,sans-serif" font-weight="800">MCR</text>
  <!-- Crucita -->
  <circle cx="50" cy="55" r="4.5" fill="#00D4FF" fill-opacity=".70"/>
  <text x="50" y="50" text-anchor="middle" font-size="5.5" fill="rgba(255,255,255,.65)"
        font-family="Inter,sans-serif">Crucita</text>
  <!-- La Pila -->
  <circle cx="78" cy="40" r="3.5" fill="#00D4FF" fill-opacity=".60"/>
  <text x="78" y="35" text-anchor="middle" font-size="5" fill="rgba(255,255,255,.55)"
        font-family="Inter,sans-serif">La Pila</text>
  <!-- Chirijos -->
  <circle cx="148" cy="45" r="5" fill="#EF4444" fill-opacity=".75"/>
  <text x="148" y="40" text-anchor="middle" font-size="5.5" fill="rgba(255,255,255,.65)"
        font-family="Inter,sans-serif">Chirijos</text>
  <!-- Noboa -->
  <circle cx="160" cy="65" r="3.5" fill="#00D4FF" fill-opacity=".60"/>
  <!-- San Sebastián -->
  <circle cx="122" cy="76" r="4" fill="#F97316" fill-opacity=".68"/>
  <!-- Leonidas Plaza -->
  <circle cx="62" cy="72" r="3" fill="#00D4FF" fill-opacity=".55"/>
  <!-- Leyenda -->
  <text x="120" y="97" text-anchor="middle" font-size="7" fill="rgba(0,212,255,.50)"
        font-family="Inter,sans-serif" font-weight="600" letter-spacing=".06em">
    CANTÓN MONTECRISTI · 7 PARROQUIAS</text>
</svg>
"""

# ══════════════════════════════════════════════════════════════════════════════
# 12 DOMINIOS CANÓNICOS
# architecture_quira_v1.md v2.0 · CONGELADO 2026-05-29
# Notas específicas a Montecristi — no genéricas
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_12: list[dict] = [
    # ── Fila 1 ────────────────────────────────────────────────────────────────
    {
        "id": "d01", "num": "01",
        "nombre": "Planificación Estratégica",
        "metric": "17 ODS activos",
        "nota": "PDOT 2023–2027 · 4 ejes · 56 metas canónicas",
        "temp": "verde", "mod": "ods",
    },
    {
        "id": "d02", "num": "02",
        "nombre": "Presupuesto & Financiamiento",
        "metric": "$3.66M",
        "nota": "BID · CAF · PNUD · fondos condicionados activos",
        "temp": "funds", "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03",
        "nombre": "Seguimiento de Metas",
        "metric": "56 metas",
        "nota": "4 áreas estratégicas · trayectoria en cálculo",
        "temp": "alerta", "mod": "situacion", "pending": True,
    },
    # ── Fila 2 ────────────────────────────────────────────────────────────────
    {
        "id": "d04", "num": "04",
        "nombre": "Alertas Institucionales",
        "metric_key": "n_alertas",
        "metric_suffix": " activas",
        "nota": "Monitoreo preventivo · 7 tipos de señal",
        "temp": "critico", "mod": "alertas", "glow": True,
    },
    {
        "id": "d05", "num": "05",
        "nombre": "Holding Municipal",
        "metric_key": "hold_avg",
        "metric_suffix": "%",
        "nota": "EP Aseo · Bomberos · Patronato · GAD",
        "temp": "alerta", "mod": "municipal",
    },
    {
        "id": "d06", "num": "06",
        "nombre": "Salud Institucional",
        "metric_key": "icpi_pct",
        "metric_suffix": "%",
        "nota": "Brecha activa · umbral institucional 65%",
        "temp": "critico", "mod": "situacion", "glow": True, "featured": True,
    },
    # ── Fila 3 ────────────────────────────────────────────────────────────────
    {
        "id": "d07", "num": "07",
        "nombre": "Transparencia",
        "metric": "21 art. LOTAIP",
        "nota": "Publicación activa · CPCCS · gobierno abierto",
        "temp": "normal", "mod": "municipal",
    },
    {
        "id": "d08", "num": "08",
        "nombre": "Participación Ciudadana",
        "metric": "27.98%",
        "nota": "Presupuesto participativo · 6 mecanismos activos",
        "temp": "alerta", "mod": "confianza",
    },
    {
        "id": "d09", "num": "09",
        "nombre": "Rendición de Cuentas",
        "metric": "Agosto 2026",
        "nota": "CPCCS · 20 ítems · preparación Q2 en curso",
        "temp": "alerta", "mod": "rdc",
    },
    # ── Fila 4 ────────────────────────────────────────────────────────────────
    {
        "id": "d10", "num": "10",
        "nombre": "Territorio & Cobertura",
        "metric": "$40/hab rural",
        "nota": "vs $217 cabecera · brecha 5.4× · 7 parroquias",
        "temp": "critico", "mod": "geotwin", "has_map": True,
    },
    {
        "id": "d11", "num": "11",
        "nombre": "Ecosistema Productivo Territorial",
        "metric": "—",
        "nota": "Empleo · industria · turismo · en construcción",
        "temp": "dim", "mod": None, "disabled": True,
    },
    {
        "id": "d12", "num": "12",
        "nombre": "Protección Social & Grupos Prioritarios",
        "metric": "12.83%",
        "nota": "Presupuesto social · umbral 30% · Art. 35 CRE",
        "temp": "critico", "mod": "genero", "glow": True,
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
# KPI BAND — 4 tiles superiores
# ══════════════════════════════════════════════════════════════════════════════

def _kpi_band(d: dict) -> str:
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
        fs = "2.2rem" if size == "lg" else "1.65rem"
        pt = "15px 18px 13px" if size == "lg" else "12px 15px 10px"
        return f"""
<div onclick="qNav('{dest}')"
     style="background:rgba(8,13,24,.98);border:1px solid {color}30;
            border-top:2.5px solid {color};border-radius:10px;
            padding:{pt};cursor:pointer;flex:1;min-width:0;
            transition:border-color .18s,background .18s"
     onmouseover="this.style.background='rgba(0,212,255,.05)'"
     onmouseout="this.style.background='rgba(8,13,24,.98)'">
  <div style="font-size:9px;font-weight:700;letter-spacing:.10em;
              text-transform:uppercase;color:rgba(255,255,255,.55);
              margin-bottom:9px">{label}</div>
  <div style="font-size:{fs};font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.04em;line-height:1;
              margin-bottom:7px">{val}</div>
  <div style="font-size:9.5px;color:rgba(255,255,255,.50);
              letter-spacing:.01em;line-height:1.4">{sub}</div>
</div>"""

    icpi_sub = (d.get("icpi_clasif", "—") + " · umbral 65%") if d.get("icpi_clasif") else "umbral 65%"

    return f"""
<div style="display:flex;gap:10px;margin-bottom:14px">
  {_tile("Cumplimiento Institucional", icpi_str, icpi_color, icpi_sub, "situacion", "lg")}
  {_tile("Fondos en Riesgo", "$3.66M", "#7C5CFC",
         "BID · CAF · PNUD condicionados", "cooperacion", "lg")}
  {_tile("Alertas Activas", alert_str, alert_color, riesgo_str, "alertas", "sm")}
  {_tile("Holding Municipal", f"{hold_avg:.1f}%", hold_color,
         "Promedio 4 entidades holding", "municipal", "sm")}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN CARD
# ══════════════════════════════════════════════════════════════════════════════

def _resolve_metric(dom: dict, data: dict) -> str:
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
    t        = _TEMP.get(dom["temp"], _TEMP["normal"])
    mod      = dom.get("mod")
    disabled = dom.get("disabled", False)
    has_map  = dom.get("has_map", False)
    glow     = dom.get("glow", False)
    featured = dom.get("featured", False)
    pending  = dom.get("pending", False)

    metric = _resolve_metric(dom, data)

    # Badge numérico
    num_badge = (
        f'<span style="font-size:8px;font-weight:800;color:{t["c"]};'
        f'background:{t["c"]}1A;border:1px solid {t["c"]}35;'
        f'border-radius:4px;padding:2px 6px;flex-shrink:0;'
        f'letter-spacing:.03em">{dom["num"]}</span>'
    )

    # Nombre
    nombre_html = (
        f'<div style="font-size:13px;font-weight:700;color:#E8EDF5;'
        f'line-height:1.25;flex:1">{dom["nombre"]}</div>'
    )

    # Métrica
    if metric != "—" and not pending:
        met_html = (
            f'<div style="font-size:1.40rem;font-weight:900;color:{t["c"]};'
            f'font-family:"JetBrains Mono",monospace;letter-spacing:-.03em;'
            f'line-height:1;margin:7px 0 5px">{metric}</div>'
        )
    else:
        met_html = '<div style="height:5px"></div>'

    # Nota
    nota_html = (
        f'<div style="font-size:10px;color:rgba(255,255,255,.58);'
        f'line-height:1.45;margin-top:2px">{dom["nota"]}</div>'
    )

    # SVG mapa (solo Dom 10)
    map_html = _CANTON_SVG if has_map else ""

    # Dot estado
    dot = (
        f'<span style="width:5px;height:5px;border-radius:50%;'
        f'background:{t["c"]};display:inline-block;flex-shrink:0;'
        f'margin-top:4px;'
        f'{"animation:qcc-pulse 2s ease-in-out infinite" if not disabled else "opacity:.25"}"></span>'
    )

    # Card deshabilitada (Dom 11)
    if disabled:
        return f"""
<div style="background:{t["bg"]};border:1px solid {t["bd"]};
            border-radius:10px;padding:13px 14px 12px;
            opacity:.35;cursor:not-allowed;">
  <div style="display:flex;align-items:flex-start;
              justify-content:space-between;gap:6px;margin-bottom:6px">
    {num_badge}{nombre_html}{dot}
  </div>
  {nota_html}
  <div style="font-size:8.5px;color:rgba(255,255,255,.22);margin-top:6px;
              text-transform:uppercase;letter-spacing:.06em">En construcción</div>
</div>"""

    # Glow para cards críticas
    glow_style = "animation:qcc-glow 2.2s ease-in-out infinite;" if glow else ""
    strong_glow = "animation:qcc-glow-strong 2s ease-in-out infinite;" if featured else ""

    # hover: intensifica bg y borde
    bg_hover = t["bg"].replace(".11", ",.20").replace(".10", ",.18").replace(".08", ",.15").replace(".06", ",.13").replace(".025", ",.06")

    return f"""
<div onclick="qNav('{mod}')"
     style="background:{t["bg"]};border:1px solid {t["bd"]};
            border-radius:10px;padding:13px 14px 12px;
            cursor:pointer;
            transition:border-color .15s,background .15s;
            {glow_style}{strong_glow}"
     onmouseover="this.style.borderColor='{t["c"]}90';this.style.background='{bg_hover}'"
     onmouseout="this.style.borderColor='{t["bd"]}';this.style.background='{t["bg"]}'">
  <div style="display:flex;align-items:flex-start;
              justify-content:space-between;gap:6px;margin-bottom:6px">
    {num_badge}{nombre_html}{dot}
  </div>
  {map_html}
  {met_html}
  {nota_html}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN GRID — 4 filas × 3 columnas · altura uniforme por fila
# ══════════════════════════════════════════════════════════════════════════════

def _domain_grid(data: dict) -> str:
    rows_html = []
    for row_start in range(0, 12, 3):
        row_doms = _DOMAINS_12[row_start: row_start + 3]
        cards = "".join(_domain_card(dom, data) for dom in row_doms)
        rows_html.append(f"""
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;
            grid-auto-rows:1fr;align-items:stretch;
            gap:9px;margin-bottom:9px">
  {cards}
</div>""")
    return "".join(rows_html)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER — banda inferior mínima
# ══════════════════════════════════════════════════════════════════════════════

def _footer() -> str:
    from config import GAD_NOMBRE, CORTE
    return f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-top:8px;padding:7px 12px;
            border-top:1px solid rgba(255,255,255,.05)">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="width:5px;height:5px;border-radius:50%;background:#22C55E;
                 display:inline-block;animation:qcc-pulse 2s ease-in-out infinite"></span>
    <span style="font-size:9px;color:rgba(255,255,255,.42);letter-spacing:.03em">
      Sistema operativo</span>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:9px;color:rgba(255,255,255,.38);
                 font-family:'JetBrains Mono',monospace">{GAD_NOMBRE}</span>
    <span style="font-size:9px;color:rgba(255,255,255,.18)">·</span>
    <span style="font-size:9px;color:rgba(255,255,255,.35)">Corte {CORTE}</span>
  </div>
  <span style="font-size:8.5px;color:rgba(255,255,255,.18);
               font-family:'JetBrains Mono',monospace">Dylus Lab © 2026</span>
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# CSS — Teatro Operacional D.3.1
# ══════════════════════════════════════════════════════════════════════════════

_CANVAS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html,body {
  background:#080D18;
  color:#E8EDF5;
  font-family:'Inter',system-ui,sans-serif;
  font-size:13px;
  overflow:hidden;
  scrollbar-width:none;
}
html::-webkit-scrollbar { display:none; }
body { padding:14px 16px 12px; }

/* Animaciones */
@keyframes qcc-pulse {
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:.2;transform:scale(.65)}
}
@keyframes fadeIn {
  from{opacity:0;transform:translateY(5px)}
  to{opacity:1;transform:none}
}
@keyframes qcc-glow {
  0%,100%{box-shadow:0 0 8px rgba(239,68,68,.32),inset 0 0 0 1px rgba(239,68,68,.20)}
  50%{box-shadow:0 0 20px rgba(239,68,68,.58),inset 0 0 0 1px rgba(239,68,68,.35)}
}
@keyframes qcc-glow-strong {
  0%,100%{box-shadow:0 0 12px rgba(239,68,68,.45),0 0 30px rgba(239,68,68,.15),inset 0 0 0 1px rgba(239,68,68,.30)}
  50%{box-shadow:0 0 25px rgba(239,68,68,.75),0 0 50px rgba(239,68,68,.22),inset 0 0 0 1px rgba(239,68,68,.50)}
}

/* Botón logout */
.btn-action {
  display:inline-flex;align-items:center;gap:5px;
  padding:5px 12px;
  border-radius:6px;
  font-size:9px;font-weight:600;
  letter-spacing:.04em;cursor:pointer;
  text-transform:uppercase;
  transition:background .15s,color .15s,border-color .15s;
}
.btn-logout {
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.10);
  color:rgba(255,255,255,.45);
}
.btn-logout:hover {
  background:rgba(239,68,68,.10);
  border-color:rgba(239,68,68,.28);
  color:#EF4444;
}
.btn-ai {
  background:rgba(0,212,255,.07);
  border:1px solid rgba(0,212,255,.22);
  color:rgba(0,212,255,.75);
}
.btn-ai:hover {
  background:rgba(0,212,255,.14);
  border-color:rgba(0,212,255,.45);
  color:#00D4FF;
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
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# CANVAS COMPLETO
# ══════════════════════════════════════════════════════════════════════════════

def _build_canvas(d: dict) -> str:
    from config import GAD_NOMBRE, ALCALDE, CORTE

    rol = get_rol()

    # ── Header ────────────────────────────────────────────────────────────────
    header_html = f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            margin-bottom:12px;padding:0 2px">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:16px;font-weight:900;color:#00D4FF;
                 letter-spacing:-.02em;line-height:1">⬡ QUIRA</span>
    <span style="width:1px;height:16px;background:rgba(255,255,255,.10);
                 display:inline-block"></span>
    <div>
      <div style="font-size:11px;font-weight:700;color:#E8EDF5;letter-spacing:.02em">
        Centro de Mando</div>
      <div style="font-size:9px;color:rgba(255,255,255,.50);letter-spacing:.04em;
                  margin-top:1px">{GAD_NOMBRE} · Corte {CORTE}</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <div style="display:flex;align-items:center;gap:5px;
                padding:4px 10px;background:rgba(34,197,94,.06);
                border:1px solid rgba(34,197,94,.18);border-radius:6px">
      <span style="width:5px;height:5px;border-radius:50%;background:#22C55E;
                   display:inline-block;animation:qcc-pulse 2.2s ease-in-out infinite"></span>
      <span style="font-size:8.5px;color:rgba(255,255,255,.60);
                   letter-spacing:.05em;font-weight:600">EN LÍNEA</span>
    </div>
    <span style="font-size:9px;font-weight:700;color:#00D4FF;
                 background:rgba(0,212,255,.10);border:1px solid rgba(0,212,255,.22);
                 border-radius:6px;padding:3px 10px;letter-spacing:.04em">{rol}</span>
    <button class="btn-action btn-ai" onclick="void(0)">◎ Preguntar a QUIRA</button>
    <button class="btn-action btn-logout" onclick="qLogout()">⎋ Salir</button>
  </div>
</div>"""

    # ── Divisor + label dominios ───────────────────────────────────────────────
    dom_header = """
<div style="display:flex;align-items:center;gap:8px;margin-bottom:9px">
  <span style="width:2px;height:12px;background:#7C5CFC;border-radius:2px;
               display:inline-block"></span>
  <span style="font-size:9px;font-weight:800;letter-spacing:.14em;
               text-transform:uppercase;color:rgba(255,255,255,.50)">
    DOMINIOS OPERACIONALES</span>
  <span style="font-size:8.5px;color:rgba(255,255,255,.18);margin-left:auto;
               font-family:'JetBrains Mono',monospace">
    Holding Municipal · Montecristi · 12 dominios · click para abrir</span>
</div>"""

    canvas = f"""
<div style="animation:fadeIn .20s ease">
  {header_html}
  {_kpi_band(d)}
  {dom_header}
  {_domain_grid(d)}
  {_footer()}
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
  h();
  document.addEventListener('DOMContentLoaded',h);
  window.addEventListener('load',h);
  setTimeout(h,100); setTimeout(h,450); setTimeout(h,1100);
})();
</script>"""
        "</body></html>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# JS BRIDGE — postMessage → botones ocultos Streamlit
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
    if(e.data.type === 'quira_action' && e.data.action === 'logout')
      dispatch(null, 'logout');
  });
})();
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Centro de Mando — 12 dominios canónicos · Sprint D.3.1."""

    # ── CSS Streamlit: sidebar invisible + botones QNAV ocultos ──────────────
    st.markdown("""
<style>
/* Sidebar invisible */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
  overflow: hidden !important;
}
/* Main 100% */
.main .block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
  max-width: 100% !important;
  width: 100% !important;
  padding-left: 0.4rem !important;
  padding-right: 0.4rem !important;
  padding-top: 0.2rem !important;
}
section[data-testid="stMainBlockContainer"] > div:first-child {
  padding-top: 3px !important;
}
/* QNAV bridge buttons — funcionales pero completamente invisibles */
div[data-testid="stHorizontalBlock"] {
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
  overflow: hidden !important;
  position: absolute !important;
  pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

    # ── Datos ─────────────────────────────────────────────────────────────────
    data = _load_data()

    # ── Canvas HTML ───────────────────────────────────────────────────────────
    html = _build_canvas(data)
    _cv1.html(html, height=870, scrolling=False)

    # ── Bridge JS (iframe height=0) ───────────────────────────────────────────
    _cv1.html(_BRIDGE_SCRIPT, height=0)

    # ── Botones ocultos — dispatch de navegación ──────────────────────────────
    # stHorizontalBlock está oculto por CSS — son funcionales, no visibles
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
