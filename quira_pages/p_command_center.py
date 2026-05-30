"""
QUIRA Intelligence — Centro de Mando  (Sprint D.3.2 · Full-Screen Fill)
Teatro Operacional · GAD Montecristi · Holding Municipal

D.3.2 — Layout full-screen:
  · body height:100% + flexbox vertical → 4 filas llenan toda la pantalla
  · Cada card con número duro + texto de enganche específico
  · Flecha → en cada card activa para señal de click
  · Dom 03 sin pending — muestra "56 metas" como número real
  · Dom 05 nota con breakdown de las 4 entidades y sus %
  · Dom 06 nota con brecha exacta en puntos

"QUIRA entiende relaciones institucionales."
Dylus Lab © 2026
"""
from __future__ import annotations

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
    "critico": {"bg": "rgba(239,68,68,.11)",    "bd": "rgba(239,68,68,.42)",   "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.10)",   "bd": "rgba(249,115,22,.38)",  "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.06)",    "bd": "rgba(0,212,255,.20)",   "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.08)",    "bd": "rgba(34,197,94,.30)",   "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.11)",   "bd": "rgba(124,92,252,.40)",  "c": "#7C5CFC"},
    "dim":     {"bg": "rgba(255,255,255,.025)", "bd": "rgba(255,255,255,.08)", "c": "#64748B"},
}

# ══════════════════════════════════════════════════════════════════════════════
# SVG 3D — Cantón Montecristi (volumen sólido isométrico)
# ══════════════════════════════════════════════════════════════════════════════
_CANTON_3D_SVG = """
<svg viewBox="0 0 220 106" xmlns="http://www.w3.org/2000/svg"
     style="width:100%;height:100%;display:block;overflow:visible">
  <defs>
    <linearGradient id="g3_top" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#1a56cc"/>
      <stop offset="100%" stop-color="#0b329e"/>
    </linearGradient>
    <linearGradient id="g3_side" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#081e5a"/>
      <stop offset="100%" stop-color="#040c26"/>
    </linearGradient>
    <filter id="g3_glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  <!-- Back/shadow face — offset (+10,+13) from top face -->
  <polygon
    points="40,65 56,39 78,23 106,17 132,23 154,19 174,33 184,53 178,77 160,91 130,98 88,95 62,87 44,72"
    fill="url(#g3_side)" stroke="rgba(0,60,160,.30)" stroke-width=".6"/>
  <!-- Top face — approximate Montecristi canton silhouette -->
  <polygon
    points="30,52 46,26 68,10 96,4 122,10 144,6 164,20 174,40 168,64 150,78 120,85 78,82 52,74 34,59"
    fill="url(#g3_top)" stroke="rgba(20,140,255,.55)" stroke-width="1.1"/>
  <!-- Edge glow -->
  <polygon
    points="30,52 46,26 68,10 96,4 122,10 144,6 164,20 174,40 168,64 150,78 120,85 78,82 52,74 34,59"
    fill="none" stroke="rgba(0,212,255,.88)" stroke-width="1.8"
    filter="url(#g3_glow)"/>
  <!-- Montecristi cabecera -->
  <circle cx="102" cy="46" r="5.5" fill="#00D4FF" opacity=".92"/>
  <circle cx="102" cy="46" r="11" fill="none" stroke="#00D4FF" stroke-width="1" opacity=".28"/>
  <text x="102" y="42.5" text-anchor="middle" font-size="5.5" fill="#fff"
        font-family="Inter,sans-serif" font-weight="900">MCR</text>
  <!-- Parroquia dots -->
  <circle cx="48" cy="52" r="3" fill="rgba(0,212,255,.65)"/>
  <text x="48" y="46" text-anchor="middle" font-size="4.8" fill="rgba(255,255,255,.52)" font-family="Inter,sans-serif">Crucita</text>
  <circle cx="74" cy="36" r="2.6" fill="rgba(0,212,255,.55)"/>
  <text x="74" y="30.5" text-anchor="middle" font-size="4.8" fill="rgba(255,255,255,.48)" font-family="Inter,sans-serif">La Pila</text>
  <circle cx="144" cy="36" r="3.2" fill="rgba(239,68,68,.80)"/>
  <text x="144" y="30" text-anchor="middle" font-size="4.8" fill="rgba(255,255,255,.55)" font-family="Inter,sans-serif">Chirijos</text>
  <circle cx="152" cy="58" r="2.6" fill="rgba(0,212,255,.55)"/>
  <circle cx="120" cy="68" r="2.8" fill="rgba(249,115,22,.68)"/>
  <circle cx="62" cy="66" r="2.4" fill="rgba(0,212,255,.50)"/>
  <!-- Footer label -->
  <text x="110" y="102" text-anchor="middle" font-size="6.5"
        fill="rgba(0,212,255,.52)" font-family="Inter,sans-serif"
        font-weight="700" letter-spacing=".09em">CANTÓN MONTECRISTI · 7 PARROQUIAS</text>
</svg>
"""

# ══════════════════════════════════════════════════════════════════════════════
# 12 DOMINIOS — número duro + texto de enganche específico Montecristi
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_12: list[dict] = [
    # ── Fila 1 ────────────────────────────────────────────────────────────────
    {
        "id": "d01", "num": "01",
        "nombre": "Planificación Estratégica",
        "metric": "17 ODS activos",
        "nota": "4 ejes estratégicos · 56 metas PDOT 2023–2027 · avance por parroquia",
        "temp": "verde", "mod": "ods",
    },
    {
        "id": "d02", "num": "02",
        "nombre": "Presupuesto & Financiamiento",
        "metric": "$3.66M",
        "nota": "BID $1.2M · CAF $0.9M · PNUD $1.56M · desembolso condicionado",
        "temp": "funds", "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03",
        "nombre": "Seguimiento de Metas",
        "metric": "56 metas",
        "nota": "Q1-2026 en actualización · 3 metas con rezago identificado",
        "temp": "alerta", "mod": "situacion",
    },
    # ── Fila 2 ────────────────────────────────────────────────────────────────
    {
        "id": "d04", "num": "04",
        "nombre": "Alertas Institucionales",
        "metric_key": "n_alertas",
        "metric_suffix": " activas",
        "nota": "7 tipos de señal preventiva · protocolos de intervención activos",
        "temp": "critico", "mod": "alertas", "glow": True,
    },
    {
        "id": "d05", "num": "05",
        "nombre": "Holding Municipal",
        "metric_key": "hold_avg",
        "metric_suffix": "%",
        "nota": "EP Aseo 82% · Bomberos 71% · Patronato 68% · GAD 54%",
        "temp": "alerta", "mod": "municipal",
    },
    {
        "id": "d06", "num": "06",
        "nombre": "Salud Institucional",
        "metric_key": "icpi_pct",
        "metric_suffix": "%",
        "nota": "Brecha activa · 11.4 puntos bajo umbral · 41 métricas en seguimiento",
        "temp": "critico", "mod": "situacion", "glow": True, "featured": True,
    },
    # ── Fila 3 ────────────────────────────────────────────────────────────────
    {
        "id": "d07", "num": "07",
        "nombre": "Transparencia",
        "metric": "21 art. LOTAIP",
        "nota": "Publicación activa 2025 · CPCCS verificado · sin opacidad registrada",
        "temp": "normal", "mod": "municipal",
    },
    {
        "id": "d08", "num": "08",
        "nombre": "Participación Ciudadana",
        "metric": "27.98%",
        "nota": "6 mecanismos activos · presupuesto participativo habilitado",
        "temp": "alerta", "mod": "confianza",
    },
    {
        "id": "d09", "num": "09",
        "nombre": "Rendición de Cuentas",
        "metric": "Agosto 2026",
        "nota": "CPCCS · 20 ítems requeridos · preparación Q2 en curso",
        "temp": "alerta", "mod": "rdc",
    },
    # ── Fila 4 ────────────────────────────────────────────────────────────────
    {
        "id": "d10", "num": "10",
        "nombre": "Territorio & Cobertura",
        "metric": "$40/hab rural",
        "nota": "vs $217 cabecera · brecha 5.4× · 3 parroquias en nivel crítico",
        "temp": "critico", "mod": "geotwin", "has_map": True,
    },
    {
        "id": "d11", "num": "11",
        "nombre": "Ecosistema Productivo Territorial",
        "metric": "—",
        "nota": "Empleo · industria · turismo · ZEDE · en construcción",
        "temp": "dim", "mod": None, "disabled": True,
    },
    {
        "id": "d12", "num": "12",
        "nombre": "Protección Social & Grupos Prioritarios",
        "metric": "12.83%",
        "nota": "vs umbral 30% · brecha $2.1M · Art. 35 CRE · Patronato activo",
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
# KPI BAND
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
    icpi_sub   = (d.get("icpi_clasif", "—") + " · umbral 65%")

    def _tile(label: str, val: str, color: str, sub: str,
              dest: str, size: str = "lg") -> str:
        fs = "2.4rem" if size == "lg" else "1.8rem"
        return f"""
<div onclick="qNav('{dest}')"
     class="kpi-tile" style="border-top-color:{color}">
  <div class="kpi-label">{label}</div>
  <div class="kpi-val" style="color:{color};font-size:{fs}">{val}</div>
  <div class="kpi-sub">{sub}</div>
  <div class="kpi-arrow" style="color:{color}">→</div>
</div>"""

    return f"""
<div class="kpi-band">
  {_tile("Cumplimiento Institucional", icpi_str, icpi_color, icpi_sub, "situacion", "lg")}
  {_tile("Fondos en Riesgo", "$3.66M", "#7C5CFC",
         "BID · CAF · PNUD · desembolso condicionado", "cooperacion", "lg")}
  {_tile("Alertas Activas", alert_str, alert_color, riesgo_str, "alertas", "sm")}
  {_tile("Holding Municipal", f"{hold_avg:.1f}%", hold_color,
         "Promedio 4 entidades · EP Aseo líder", "municipal", "sm")}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# CARD VIZ — mini visualización por dominio
# ══════════════════════════════════════════════════════════════════════════════

def _card_viz(dom_id: str, data: dict) -> str:
    """Retorna HTML de mini-visualización para el espacio interno del cajón."""
    icpi_pct  = data.get("icpi_pct", 17.4) or 17.4
    hold_avg  = data.get("hold_avg", 68.7)
    n_alertas = data.get("n_alertas", 0)

    if dom_id == "d01":
        return """<div class="card-viz card-viz-pills">
          <span class="viz-pill vp-green">● Eje Social</span>
          <span class="viz-pill vp-green">● Eje Económico</span>
          <span class="viz-pill vp-green">● Eje Ambiental</span>
          <span class="viz-pill vp-green">● Eje Institucional</span>
        </div>"""

    if dom_id == "d02":
        return """<div class="card-viz card-viz-bars">
          <div class="vb-row"><span class="vb-lbl">BID</span>
            <div class="vb-track"><div class="vb-fill" style="width:32.8%;background:#7C5CFC"></div></div>
            <span class="vb-val">$1.2M</span></div>
          <div class="vb-row"><span class="vb-lbl">CAF</span>
            <div class="vb-track"><div class="vb-fill" style="width:24.6%;background:#7C5CFC"></div></div>
            <span class="vb-val">$0.9M</span></div>
          <div class="vb-row"><span class="vb-lbl">PNUD</span>
            <div class="vb-track"><div class="vb-fill" style="width:42.6%;background:#9B72FF"></div></div>
            <span class="vb-val">$1.56M</span></div>
        </div>"""

    if dom_id == "d03":
        return """<div class="card-viz card-viz-pills">
          <span class="viz-pill vp-green">✓ 53 en ruta</span>
          <span class="viz-pill vp-orange">⚑ 3 rezago</span>
          <span class="viz-pill vp-dim">PDOT 2023–2027</span>
          <span class="viz-pill vp-dim">Q1-2026 activo</span>
        </div>"""

    if dom_id == "d04":
        return f"""<div class="card-viz card-viz-signals">
          <div class="sig-type sig-red">SAT</div>
          <div class="sig-type sig-red">TOP</div>
          <div class="sig-type sig-orange">MMP</div>
          <div class="sig-type sig-orange">RDC</div>
          <div class="sig-type sig-orange">FIN</div>
          <div class="sig-type sig-amber">CTIC</div>
          <div class="sig-type sig-amber">PAR</div>
        </div>"""

    if dom_id == "d05":
        entities = [
            ("EP Aseo",   82, "#22C55E"),
            ("Bomberos",  71, "#FFB700"),
            ("Patronato", 68, "#FFB700"),
            ("GAD",       54, "#F97316"),
        ]
        rows = "".join(
            f'<div class="vb-row"><span class="vb-lbl">{n}</span>'
            f'<div class="vb-track"><div class="vb-fill" style="width:{v}%;background:{c}"></div></div>'
            f'<span class="vb-val">{v}%</span></div>'
            for n, v, c in entities
        )
        return f'<div class="card-viz card-viz-bars">{rows}</div>'

    if dom_id == "d06":
        pct      = float(icpi_pct)
        fill_pct = min(pct, 100)
        brecha   = max(0.0, 65.0 - pct)
        return f"""<div class="card-viz card-viz-progress">
          <div class="vp-row-top">
            <span class="vp-row-top-val" style="color:#EF4444">{pct:.1f}%</span>
            <span class="vp-row-top-sub">umbral: 65%</span>
          </div>
          <div class="vp-track">
            <div class="vp-fill" style="width:{fill_pct:.1f}%;background:#EF4444"></div>
            <div class="vp-umbral" style="left:65%"></div>
          </div>
          <div class="vp-gap">Brecha activa: {brecha:.1f} puntos</div>
        </div>"""

    if dom_id == "d07":
        return """<div class="card-viz card-viz-pills">
          <span class="viz-pill vp-cyan">LOTAIP ✓</span>
          <span class="viz-pill vp-cyan">CPCCS ✓</span>
          <span class="viz-pill vp-cyan">SAIP ✓</span>
          <span class="viz-pill vp-cyan">OCP ✓</span>
          <span class="viz-pill vp-dim">21 artículos</span>
        </div>"""

    if dom_id == "d08":
        return """<div class="card-viz card-viz-pills">
          <span class="viz-pill vp-orange">Presup. Participativo</span>
          <span class="viz-pill vp-orange">Cabildos</span>
          <span class="viz-pill vp-orange">Consultas</span>
          <span class="viz-pill vp-dim">Veedurías</span>
          <span class="viz-pill vp-dim">Asambleas</span>
          <span class="viz-pill vp-dim">Silla Vacía</span>
        </div>"""

    if dom_id == "d09":
        return """<div class="card-viz card-viz-timeline">
          <div class="vt-step vt-done">
            <span class="vt-tag">✓</span>
            <span>Q1</span>
            <span class="vt-sub">CERRADO</span>
          </div>
          <div class="vt-line"></div>
          <div class="vt-step vt-active">
            <span class="vt-tag">●</span>
            <span>Q2</span>
            <span class="vt-sub">EN CURSO</span>
          </div>
          <div class="vt-line"></div>
          <div class="vt-step vt-future">
            <span class="vt-tag">○</span>
            <span>AGO</span>
            <span class="vt-sub">CPCCS</span>
          </div>
        </div>"""

    if dom_id == "d10":
        return f'<div class="card-viz card-viz-map">{_CANTON_3D_SVG}</div>'

    if dom_id == "d12":
        pct    = 12.83
        umbral = 30.0
        brecha = umbral - pct
        return f"""<div class="card-viz card-viz-progress">
          <div class="vp-row-top">
            <span class="vp-row-top-val" style="color:#EF4444">{pct}%</span>
            <span class="vp-row-top-sub">umbral: {umbral:.0f}%</span>
          </div>
          <div class="vp-track">
            <div class="vp-fill" style="width:{pct:.2f}%;background:#EF4444"></div>
            <div class="vp-umbral" style="left:{umbral:.0f}%"></div>
          </div>
          <div class="vp-gap">Brecha: {brecha:.2f} puntos · Art. 35 CRE</div>
        </div>"""

    return ""


# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN CARD — número duro + nota de enganche + flecha
# ══════════════════════════════════════════════════════════════════════════════

def _resolve_metric(dom: dict, data: dict) -> str:
    key = dom.get("metric_key")
    if key:
        val = data.get(key)
        if val is not None:
            suffix = dom.get("metric_suffix", "")
            return f"{val:.1f}{suffix}" if isinstance(val, float) else f"{val}{suffix}"
    return dom.get("metric", "—")


def _domain_card(dom: dict, data: dict) -> str:
    t        = _TEMP.get(dom["temp"], _TEMP["normal"])
    mod      = dom.get("mod")
    disabled = dom.get("disabled", False)
    glow     = dom.get("glow", False)
    featured = dom.get("featured", False)

    metric = _resolve_metric(dom, data)

    num_html = (
        f'<span class="card-num" style="color:{t["c"]};'
        f'background:{t["c"]}18;border-color:{t["c"]}32">{dom["num"]}</span>'
    )

    # Card deshabilitada (Dom 11)
    if disabled:
        return f"""
<div class="domain-card" style="background:{t["bg"]};border-color:{t["bd"]};
     opacity:.32;cursor:not-allowed;">
  <div class="card-top">
    {num_html}
    <div class="card-name" style="color:#8899AA">{dom["nombre"]}</div>
  </div>
  <div class="card-metric" style="color:{t["c"]};font-size:1.4rem">{metric}</div>
  <div class="card-nota" style="color:rgba(255,255,255,.38)">{dom["nota"]}</div>
  <div class="card-footer" style="color:rgba(255,255,255,.18)">En construcción</div>
</div>"""

    glow_anim = (
        "animation:qcc-glow-strong 2s ease-in-out infinite;" if featured
        else "animation:qcc-glow 2.3s ease-in-out infinite;" if glow
        else ""
    )

    viz_html = _card_viz(dom["id"], data)

    return f"""
<div class="domain-card" onclick="qNav('{mod}')"
     style="background:{t["bg"]};border-color:{t["bd"]};{glow_anim}"
     onmouseover="this.classList.add('hovered')"
     onmouseout="this.classList.remove('hovered')">
  <div class="card-top">
    {num_html}
    <div class="card-name">{dom["nombre"]}</div>
    <span class="card-dot" style="background:{t["c"]}"></span>
  </div>
  <div class="card-metric" style="color:{t["c"]}">{metric}</div>
  <div class="card-nota">{dom["nota"]}</div>
  {viz_html}
  <div class="card-footer" style="color:{t["c"]}80">→ Ver detalle</div>
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# GRID — flex column, filas con flex:1 para llenar pantalla completa
# ══════════════════════════════════════════════════════════════════════════════

def _domain_grid(data: dict) -> str:
    rows_html = []
    for row_start in range(0, 12, 3):
        row_doms = _DOMAINS_12[row_start: row_start + 3]
        cards = "".join(_domain_card(dom, data) for dom in row_doms)
        rows_html.append(f'<div class="dom-row">{cards}</div>')
    return f'<div class="dom-grid">{"".join(rows_html)}</div>'


# ══════════════════════════════════════════════════════════════════════════════
# CSS — layout full-height con flexbox vertical
# ══════════════════════════════════════════════════════════════════════════════

_CANVAS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }

/* ── Layout vertical full-height ── */
html { height:100%; }
body {
  height:100%;
  background:#080D18;
  color:#E8EDF5;
  font-family:'Inter',system-ui,sans-serif;
  font-size:13px;
  overflow:hidden;
  display:flex;
  flex-direction:column;
  padding:12px 14px 10px;
}

/* Wrapper central */
.canvas-wrap {
  display:flex;
  flex-direction:column;
  flex:1;
  min-height:0;
  gap:0;
}

/* ── Animaciones ── */
@keyframes qcc-pulse {
  0%,100%{opacity:1;transform:scale(1)}
  50%{opacity:.18;transform:scale(.62)}
}
@keyframes fadeIn {
  from{opacity:0;transform:translateY(4px)} to{opacity:1;transform:none}
}
@keyframes qcc-glow {
  0%,100%{box-shadow:0 0 8px rgba(239,68,68,.30),inset 0 0 0 1px rgba(239,68,68,.18)}
  50%{box-shadow:0 0 22px rgba(239,68,68,.56),inset 0 0 0 1px rgba(239,68,68,.34)}
}
@keyframes qcc-glow-strong {
  0%,100%{box-shadow:0 0 14px rgba(239,68,68,.44),0 0 35px rgba(239,68,68,.14),inset 0 0 0 1px rgba(239,68,68,.28)}
  50%{box-shadow:0 0 28px rgba(239,68,68,.72),0 0 55px rgba(239,68,68,.20),inset 0 0 0 1px rgba(239,68,68,.50)}
}

/* ── HEADER ── */
.cc-header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 2px;
  margin-bottom:11px;
  flex-shrink:0;
}
.cc-brand {
  display:flex;
  align-items:center;
  gap:11px;
}
.cc-logo {
  font-size:17px;
  font-weight:900;
  color:#00D4FF;
  letter-spacing:-.02em;
  line-height:1;
}
.cc-divider {
  width:1px;
  height:18px;
  background:rgba(255,255,255,.10);
}
.cc-title { font-size:12px; font-weight:700; color:#E8EDF5; letter-spacing:.01em; }
.cc-sub { font-size:9px; color:rgba(255,255,255,.50); margin-top:1px; letter-spacing:.03em; }
.cc-controls { display:flex; align-items:center; gap:8px; }

.badge-online {
  display:flex;align-items:center;gap:5px;
  padding:4px 10px;
  background:rgba(34,197,94,.06);
  border:1px solid rgba(34,197,94,.18);
  border-radius:6px;
}
.badge-online-dot {
  width:5px;height:5px;border-radius:50%;background:#22C55E;
  display:inline-block;animation:qcc-pulse 2.2s ease-in-out infinite;
}
.badge-online span { font-size:8.5px;color:rgba(255,255,255,.62);letter-spacing:.05em;font-weight:600; }

.badge-rol {
  font-size:9px;font-weight:700;color:#00D4FF;
  background:rgba(0,212,255,.10);border:1px solid rgba(0,212,255,.22);
  border-radius:6px;padding:3px 10px;letter-spacing:.04em;
}

.btn-cc {
  display:inline-flex;align-items:center;gap:5px;
  padding:5px 12px;border-radius:6px;
  font-size:9px;font-weight:600;
  letter-spacing:.04em;cursor:pointer;
  text-transform:uppercase;transition:all .15s;
}
.btn-ai {
  background:rgba(0,212,255,.07);
  border:1px solid rgba(0,212,255,.22);
  color:rgba(0,212,255,.75);
}
.btn-ai:hover { background:rgba(0,212,255,.14);border-color:rgba(0,212,255,.45);color:#00D4FF; }
.btn-logout {
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.10);
  color:rgba(255,255,255,.45);
}
.btn-logout:hover { background:rgba(239,68,68,.10);border-color:rgba(239,68,68,.28);color:#EF4444; }

/* ── KPI BAND ── */
.kpi-band {
  display:flex;
  gap:10px;
  margin-bottom:11px;
  flex-shrink:0;
}
.kpi-tile {
  flex:1;min-width:0;
  background:rgba(8,13,24,.98);
  border:1px solid rgba(255,255,255,.06);
  border-top-width:2.5px;
  border-radius:10px;
  padding:12px 16px 10px;
  cursor:pointer;
  transition:background .18s;
  position:relative;
}
.kpi-tile:hover { background:rgba(0,212,255,.04); }
.kpi-label {
  font-size:8.5px;font-weight:700;letter-spacing:.10em;
  text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:8px;
}
.kpi-val {
  font-weight:900;font-family:'JetBrains Mono',monospace;
  letter-spacing:-.04em;line-height:1;margin-bottom:6px;
}
.kpi-sub { font-size:9.5px;color:rgba(255,255,255,.50);line-height:1.4; }
.kpi-arrow {
  position:absolute;bottom:10px;right:13px;
  font-size:11px;opacity:.45;transition:opacity .15s;
}
.kpi-tile:hover .kpi-arrow { opacity:1; }

/* ── DOM HEADER LABEL ── */
.dom-label {
  display:flex;align-items:center;gap:8px;
  margin-bottom:8px;flex-shrink:0;
}
.dom-label-bar { width:2px;height:12px;background:#7C5CFC;border-radius:2px; }
.dom-label-text {
  font-size:9px;font-weight:800;letter-spacing:.14em;
  text-transform:uppercase;color:rgba(255,255,255,.50);
}
.dom-label-right {
  margin-left:auto;font-size:8.5px;
  color:rgba(255,255,255,.20);
  font-family:'JetBrains Mono',monospace;
}

/* ── DOMAIN GRID — full height ── */
.dom-grid {
  display:flex;
  flex-direction:column;
  flex:1;
  min-height:0;
  gap:8px;
}
.dom-row {
  display:grid;
  grid-template-columns:1fr 1fr 1fr;
  gap:8px;
  flex:1;
  min-height:0;
}

/* ── DOMAIN CARD ── */
.domain-card {
  border:1px solid;
  border-radius:10px;
  padding:12px 14px 10px;
  display:flex;
  flex-direction:column;
  cursor:pointer;
  transition:border-color .15s,background .15s;
  min-height:0;
  overflow:hidden;
}
.domain-card:hover { filter:brightness(1.12); }
.domain-card.hovered { filter:brightness(1.12); }

.card-top {
  display:flex;align-items:flex-start;gap:6px;margin-bottom:6px;
}
.card-num {
  font-size:8px;font-weight:800;
  border:1px solid;border-radius:4px;
  padding:2px 6px;flex-shrink:0;letter-spacing:.03em;
}
.card-name {
  font-size:13px;font-weight:700;color:#E8EDF5;
  line-height:1.25;flex:1;
}
.card-dot {
  width:5px;height:5px;border-radius:50%;flex-shrink:0;margin-top:4px;
  animation:qcc-pulse 2.1s ease-in-out infinite;
}
.card-metric {
  font-size:1.45rem;font-weight:900;
  font-family:'JetBrains Mono',monospace;
  letter-spacing:-.03em;line-height:1;
  margin:6px 0 5px;
  flex-shrink:0;
}
.card-nota {
  font-size:10px;color:rgba(255,255,255,.60);
  line-height:1.45;flex-shrink:0;
}
.card-footer {
  font-size:9px;font-weight:600;letter-spacing:.04em;
  margin-top:6px;flex-shrink:0;
  text-transform:uppercase;
}

/* ── CARD VIZ — mini visualizaciones dentro de cada cajón ── */
.card-viz {
  flex:1;min-height:0;
  display:flex;flex-direction:column;
  justify-content:center;
  margin:5px 0 3px;
  overflow:hidden;
}

/* Pills */
.card-viz-pills {
  flex-direction:row;flex-wrap:wrap;
  gap:4px;align-content:flex-start;
  padding-top:2px;
}
.viz-pill {
  font-size:8.5px;font-weight:700;letter-spacing:.04em;
  border-radius:4px;padding:3px 8px;white-space:nowrap;
}
.vp-green  { background:rgba(34,197,94,.12);color:#22C55E;border:1px solid rgba(34,197,94,.28); }
.vp-orange { background:rgba(249,115,22,.12);color:#F97316;border:1px solid rgba(249,115,22,.28); }
.vp-amber  { background:rgba(255,183,0,.12);color:#FFB700;border:1px solid rgba(255,183,0,.28); }
.vp-cyan   { background:rgba(0,212,255,.10);color:#00D4FF;border:1px solid rgba(0,212,255,.25); }
.vp-red    { background:rgba(239,68,68,.12);color:#EF4444;border:1px solid rgba(239,68,68,.28); }
.vp-dim    { background:rgba(255,255,255,.05);color:rgba(255,255,255,.38);border:1px solid rgba(255,255,255,.10); }

/* Bar rows */
.card-viz-bars { gap:5px;justify-content:center; }
.vb-row { display:flex;align-items:center;gap:6px; }
.vb-lbl { font-size:8px;color:rgba(255,255,255,.48);width:52px;flex-shrink:0;letter-spacing:.01em; }
.vb-track { flex:1;height:5px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden; }
.vb-fill  { height:100%;border-radius:3px; }
.vb-val   { font-size:8px;color:rgba(255,255,255,.55);width:36px;text-align:right;
             flex-shrink:0;font-family:'JetBrains Mono',monospace;font-weight:600; }

/* Progress bar (single metric vs umbral) */
.card-viz-progress { gap:5px;justify-content:center; }
.vp-row-top { display:flex;justify-content:space-between;align-items:baseline;margin-bottom:3px; }
.vp-row-top-val { font-size:11px;font-weight:900;font-family:'JetBrains Mono',monospace;letter-spacing:-.02em; }
.vp-row-top-sub { font-size:8px;color:rgba(255,255,255,.35); }
.vp-track { position:relative;height:7px;background:rgba(255,255,255,.07);border-radius:4px;overflow:visible; }
.vp-fill  { position:absolute;top:0;left:0;height:100%;border-radius:4px; }
.vp-umbral { position:absolute;top:-4px;bottom:-4px;width:2px;background:rgba(255,255,255,.42);border-radius:2px; }
.vp-gap { font-size:8px;color:rgba(255,255,255,.32);margin-top:4px; }

/* Signal type grid (Dom 04) */
.card-viz-signals { flex-direction:row;flex-wrap:wrap;gap:4px;align-content:flex-start;padding-top:2px; }
.sig-type { font-size:8px;font-weight:800;letter-spacing:.07em;
  border-radius:4px;padding:3px 8px; }
.sig-red    { background:rgba(239,68,68,.15);color:#EF4444;border:1px solid rgba(239,68,68,.30); }
.sig-orange { background:rgba(249,115,22,.12);color:#F97316;border:1px solid rgba(249,115,22,.28); }
.sig-amber  { background:rgba(255,183,0,.12);color:#FFB700;border:1px solid rgba(255,183,0,.25); }

/* Timeline (Dom 09) */
.card-viz-timeline { flex-direction:row;align-items:center;justify-content:center; }
.vt-step { display:flex;flex-direction:column;align-items:center;gap:3px;
  font-size:9px;font-weight:800;min-width:44px;text-align:center; }
.vt-done   { color:#22C55E; }
.vt-active { color:#F97316; }
.vt-future { color:rgba(255,255,255,.28); }
.vt-tag  { font-size:10px; }
.vt-sub  { font-size:7px;font-weight:600;letter-spacing:.04em;opacity:.70; }
.vt-line { flex:1;height:1.5px;background:rgba(255,255,255,.12);margin:0 2px; }

/* Map (Dom 10) */
.card-viz-map { padding-top:2px; }

/* ── FOOTER ── */
.cc-footer {
  display:flex;align-items:center;justify-content:space-between;
  padding:7px 2px 0;
  border-top:1px solid rgba(255,255,255,.05);
  margin-top:8px;flex-shrink:0;
}
.cc-footer-left {
  display:flex;align-items:center;gap:12px;
  font-size:9px;color:rgba(255,255,255,.38);
}
.cc-footer-dot {
  width:5px;height:5px;border-radius:50%;background:#22C55E;
  display:inline-block;animation:qcc-pulse 2.5s ease-in-out infinite;
}
.cc-footer-right {
  font-size:8.5px;color:rgba(255,255,255,.18);
  font-family:'JetBrains Mono',monospace;
}
"""

_BRIDGE_JS = """
<script>
function qNav(d){if(d)window.parent.postMessage({type:'quira_nav',dest:d},'*');}
function qLogout(){window.parent.postMessage({type:'quira_action',action:'logout'},'*');}
</script>
"""

_NAV_TARGETS = [
    "situacion", "cooperacion", "alertas", "municipal",
    "analisis", "geotwin", "rdc", "confianza", "genero",
    "ods", "control",
]

_BRIDGE_SCRIPT = """
<script>
(function(){
  function dispatch(dest,action){
    var btns=window.parent.document.querySelectorAll('[data-testid="stBaseButton-secondary"]');
    var token=action==='logout'?'__QLOGOUT__':'__QNAV_'+dest+'__';
    for(var i=0;i<btns.length;i++){
      if(btns[i].innerText.trim()===token){btns[i].click();return;}
    }
  }
  window.addEventListener('message',function(e){
    if(!e.data)return;
    if(e.data.type==='quira_nav')dispatch(e.data.dest,'nav');
    if(e.data.type==='quira_action'&&e.data.action==='logout')dispatch(null,'logout');
  });
})();
</script>
"""


# ══════════════════════════════════════════════════════════════════════════════
# BUILD CANVAS
# ══════════════════════════════════════════════════════════════════════════════

def _build_canvas(d: dict) -> str:
    from config import GAD_NOMBRE, ALCALDE, CORTE
    rol = get_rol()

    header = f"""
<div class="cc-header">
  <div class="cc-brand">
    <span class="cc-logo">⬡ QUIRA</span>
    <div class="cc-divider"></div>
    <div>
      <div class="cc-title">Centro de Mando</div>
      <div class="cc-sub">{GAD_NOMBRE} · Corte {CORTE}</div>
    </div>
  </div>
  <div class="cc-controls">
    <div class="badge-online">
      <span class="badge-online-dot"></span>
      <span>EN LÍNEA</span>
    </div>
    <span class="badge-rol">{rol}</span>
    <button class="btn-cc btn-ai" onclick="void(0)">◎ Preguntar a QUIRA</button>
    <button class="btn-cc btn-logout" onclick="qLogout()">⎋ Salir</button>
  </div>
</div>"""

    dom_label = f"""
<div class="dom-label">
  <span class="dom-label-bar"></span>
  <span class="dom-label-text">Dominios Operacionales</span>
  <span class="dom-label-right">Holding Municipal · Montecristi · 12 dominios · click para abrir</span>
</div>"""

    footer = f"""
<div class="cc-footer">
  <div class="cc-footer-left">
    <span class="cc-footer-dot"></span>
    <span>Sistema operativo</span>
    <span>·</span>
    <span style="font-family:'JetBrains Mono',monospace">{GAD_NOMBRE}</span>
    <span>·</span>
    <span>Corte {CORTE}</span>
  </div>
  <span class="cc-footer-right">Dylus Lab © 2026 · Gold Master v5.5_TGI</span>
</div>"""

    canvas = f"""
<div class="canvas-wrap" style="animation:fadeIn .20s ease">
  {header}
  {_kpi_band(d)}
  {dom_label}
  {_domain_grid(d)}
  {footer}
</div>"""

    return (
        "<!DOCTYPE html><html lang='es'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{_CANVAS_CSS}</style>"
        "</head>"
        f"<body>{canvas}{_BRIDGE_JS}</body></html>"
    )


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Centro de Mando — full-screen fill · Sprint D.3.2."""

    st.markdown("""
<style>
/* Sidebar invisible */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
  display:none!important;width:0!important;min-width:0!important;overflow:hidden!important;
}
/* Main 100% */
.main .block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
  max-width:100%!important;width:100%!important;
  padding:0.2rem 0.4rem 0!important;
}
section[data-testid="stMainBlockContainer"]>div:first-child { padding-top:2px!important; }
/* iframe sin márgenes */
iframe[title] { display:block!important; margin:0!important; padding:0!important; }
/* QNAV bridge buttons — funcionales pero invisibles */
div[data-testid="stHorizontalBlock"] {
  display:none!important;height:0!important;min-height:0!important;
  overflow:hidden!important;position:absolute!important;pointer-events:none!important;
}
</style>
""", unsafe_allow_html=True)

    data = _load_data()
    html = _build_canvas(data)
    _cv1.html(html, height=920, scrolling=False)
    _cv1.html(_BRIDGE_SCRIPT, height=0)

    # Botones ocultos — dispatch navegación (invisible via CSS)
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
