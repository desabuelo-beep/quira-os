"""
QUIRA OS v0.1 — P-04 GeoTwin · Territorio
Fiel al DEMO.html P-04 · st.components.v1.html() render
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# Extra CSS for GeoTwin-specific classes not in DEMO_CSS
_GT_CSS = """
.gt-legend { display:flex; gap:12px; flex-wrap:wrap; margin-top:10px; }
.gt-leg-item { display:flex; align-items:center; gap:5px; font-size:11px; color:var(--muted); }
.gt-leg-dot { width:10px; height:10px; border-radius:50%; }
.gt-project { background:var(--navy-light); border:1px solid var(--divider);
  border-radius:10px; padding:14px; margin-bottom:10px; }
.gt-project-title { font-size:13px; font-weight:700; color:var(--white); margin-bottom:8px; }
.gt-contrib { display:flex; gap:10px; margin-bottom:8px; }
.gt-contrib-box { flex:1; background:var(--navy-card); border-radius:8px;
  padding:8px; font-size:11px; color:var(--muted); }
.gt-contrib-box strong { display:block; font-size:10px; margin-bottom:3px; }
.gt-fund { font-size:12px; font-weight:600; }
.gt-fund.elegible { color:var(--green); }
.gt-fund.pending { color:var(--amber); }
.gt-fund.priority { color:var(--cyan); }
"""


def _parroquia_row(p: dict) -> str:
    """HTML row for parroquia table."""
    agua_color = "#E53E3E" if p["agua"] < 20 else ("#D69E2E" if p["agua"] < 50 else "#38A169")
    estado_badge = {
        "EMERGENCIA": '<span class="badge badge-red">EMERGENCIA</span>',
        "PRIORIDAD":  '<span style="display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:600;background:rgba(124,92,252,.15);color:#7C5CFC;border:1px solid rgba(124,92,252,.3)">PRIORIDAD</span>',
        "ALERTA":     '<span class="badge badge-amber">ALERTA</span>',
        "NORMAL":     '<span class="badge badge-cyan">NORMAL</span>',
        "OK":         '<span class="badge badge-green">OK</span>',
    }.get(p["estado"], "")

    return (
        f'<tr>'
        f'<td>{p["emoji"]} {p["nombre"]}</td>'
        f'<td class="td-num" style="color:var(--red)">{p["tps"]:.2f}</td>'
        f'<td class="td-num" style="color:{agua_color}">{p["agua"]:.1f}%</td>'
        f'<td class="td-num">{p["habitantes"]:,}</td>'
        f'<td class="td-num">${p["per_capita"]}</td>'
        f'<td>{estado_badge}</td>'
        f'</tr>'
    )


def render() -> None:
    data      = load_all()
    parroquias = data.get("parroquias", [])
    show_tech = is_tecnico()

    # Sort by TPS descending (most vulnerable first)
    parroquias_sorted = sorted(parroquias, key=lambda x: x["tps"], reverse=True)

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr = page_header(
        "④ EQUIDAD TERRITORIAL · GOV TWIN",
        "Territorio + Gov Twin",
        "Nexo Holding Municipal ↔ Ciudadanía · Proyectos colaborativos",
    )

    # ── SVG MAP ───────────────────────────────────────────────────────────────
    svg_map = """
<div class="gt-map">
  <svg viewBox="0 0 400 260" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
    <rect width="400" height="260" fill="#111830"/>
    <text x="200" y="130" text-anchor="middle" fill="#1E2D50" font-size="40"
          font-weight="800" font-family="Inter">MANABÍ</text>
    <path d="M60,40 L340,40 L360,130 L300,220 L100,220 L40,130 Z"
          fill="none" stroke="#1E2D50" stroke-width="2" stroke-dasharray="6,4"/>

    <!-- Montecristi cabecera -->
    <circle cx="200" cy="120" r="14" fill="#00D4FF" opacity=".9"/>
    <text x="200" y="125" text-anchor="middle" fill="#0A1128" font-size="9" font-weight="800">MCT</text>
    <text x="200" y="144" text-anchor="middle" fill="#F0F4FF" font-size="8">Montecristi</text>
    <text x="200" y="154" text-anchor="middle" fill="#8892B0" font-size="7">TPS: 22.4</text>

    <!-- Eloy Alfaro -->
    <circle cx="140" cy="90" r="10" fill="#FFB800" opacity=".85"/>
    <text x="140" y="94" text-anchor="middle" fill="#0A1128" font-size="8" font-weight="700">EA</text>
    <text x="140" y="108" text-anchor="middle" fill="#F0F4FF" font-size="7">E. Alfaro</text>
    <text x="140" y="117" text-anchor="middle" fill="#FFB800" font-size="7">TPS: 31.2</text>

    <!-- Leónidas Plaza -->
    <circle cx="270" cy="85" r="10" fill="#FFB800" opacity=".85"/>
    <text x="270" y="89" text-anchor="middle" fill="#0A1128" font-size="8" font-weight="700">LP</text>
    <text x="270" y="103" text-anchor="middle" fill="#F0F4FF" font-size="7">L. Plaza</text>
    <text x="270" y="112" text-anchor="middle" fill="#FFB800" font-size="7">TPS: 28.8</text>

    <!-- La Pila -->
    <circle cx="155" cy="160" r="9" fill="#FF4D6D" opacity=".85"/>
    <text x="155" y="164" text-anchor="middle" fill="#F0F4FF" font-size="8" font-weight="700">LP</text>
    <text x="155" y="178" text-anchor="middle" fill="#F0F4FF" font-size="7">La Pila</text>
    <text x="155" y="187" text-anchor="middle" fill="#FF4D6D" font-size="7">TPS: 41.2</text>

    <!-- Colorado -->
    <circle cx="290" cy="170" r="9" fill="#FF4D6D" opacity=".85"/>
    <text x="290" y="174" text-anchor="middle" fill="#F0F4FF" font-size="8" font-weight="700">CO</text>
    <text x="290" y="188" text-anchor="middle" fill="#F0F4FF" font-size="7">Colorado</text>
    <text x="290" y="197" text-anchor="middle" fill="#FF4D6D" font-size="7">TPS: 58.7</text>

    <!-- Aníbal San Andrés -->
    <circle cx="100" cy="170" r="9" fill="#7C5CFC" opacity=".9"/>
    <text x="100" y="174" text-anchor="middle" fill="#F0F4FF" font-size="8" font-weight="700">ASA</text>
    <text x="100" y="188" text-anchor="middle" fill="#F0F4FF" font-size="7">A. San Andrés</text>
    <text x="100" y="197" text-anchor="middle" fill="#7C5CFC" font-size="7">💜 TPS: 62.3</text>

    <!-- Isabel Muentes (CRÍTICA — con pulso animado) -->
    <circle cx="340" cy="190" r="12" fill="#FF4D6D" opacity="1"/>
    <circle cx="340" cy="190" r="16" fill="none" stroke="#FF4D6D" stroke-width="2" opacity=".5">
      <animate attributeName="r" values="16;22;16" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".5;0;.5" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="340" y="194" text-anchor="middle" fill="#F0F4FF" font-size="8" font-weight="800">IM!</text>
    <text x="340" y="210" text-anchor="middle" fill="#FF4D6D" font-size="7" font-weight="700">Isabel Muentes</text>
    <text x="340" y="219" text-anchor="middle" fill="#FF4D6D" font-size="7">💧 1.02% agua</text>

    <text x="370" y="30" text-anchor="middle" fill="#1E2D50" font-size="12">N↑</text>
  </svg>
</div>
<div class="gt-legend">
  <div class="gt-leg-item"><div class="gt-leg-dot" style="background:var(--cyan)"></div>Cabecera</div>
  <div class="gt-leg-item"><div class="gt-leg-dot" style="background:var(--amber)"></div>Alerta media</div>
  <div class="gt-leg-item"><div class="gt-leg-dot" style="background:var(--red)"></div>Prioridad alta</div>
  <div class="gt-leg-item"><div class="gt-leg-dot" style="background:var(--purple)"></div>Pin Morado 💜</div>
</div>
<div style="display:inline-block;margin-top:12px;padding:8px 12px;
            background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
            border-radius:8px;font-size:12px;color:var(--cyan)">
  💬 Analizar prioridad territorial
</div>"""

    # ── GOV TWIN PROJECTS ─────────────────────────────────────────────────────
    gt_projects = """
<div style="font-size:12px;color:var(--muted);margin-bottom:12px;padding:8px;
            background:rgba(0,212,255,.04);border-radius:8px;border:1px solid rgba(0,212,255,.1)">
  <strong style="color:var(--cyan)">¿Qué es Gov Twin?</strong><br>
  La línea de encuentro entre el Holding Municipal y la ciudadanía. El municipio aporta recursos
  técnicos; el barrio aporta mano de obra y custodia. Juntos desbloquean fondos no reembolsables
  imposibles de obtener por separado.
</div>

<div class="gt-project">
  <div class="gt-project-title">
    💧 Sistema Agua · Isabel Muentes
    <span class="badge badge-red" style="float:right">URGENTE</span>
  </div>
  <div class="gt-contrib">
    <div class="gt-contrib-box">
      <strong>🏛️ Municipio aporta:</strong>Infraestructura hidráulica + diseño técnico + fiscalización
    </div>
    <div class="gt-contrib-box">
      <strong>👥 Comunidad aporta:</strong>Mano de obra local + Junta de Agua + custodia
    </div>
  </div>
  <div class="gt-fund priority">🌐 PNUD Agua Rural · $2,400,000 · Score 81/100</div>
  <div style="font-size:11px;color:var(--amber);margin-top:4px">
    ⚠️ Requiere Gobernanza ≥ 55% · Brecha actual: 1.44 pts
  </div>
</div>

<div class="gt-project">
  <div class="gt-project-title">🌳 Reforestación Laderas · Colorado</div>
  <div class="gt-contrib">
    <div class="gt-contrib-box">
      <strong>🏛️ Municipio aporta:</strong>Plantas nativas + técnico forestal + transporte
    </div>
    <div class="gt-contrib-box">
      <strong>👥 Comunidad aporta:</strong>Mano de obra + custodios del bosque
    </div>
  </div>
  <div class="gt-fund elegible">✅ Fondo Verde del Clima GEF · $180,000 · Elegible</div>
  <div style="font-size:11px;color:var(--muted);margin-top:4px">
    Pin Verde activo · dMRV preparado
  </div>
</div>

<div class="gt-project">
  <div class="gt-project-title">💜 Luminarias Seguridad · Aníbal San Andrés</div>
  <div class="gt-contrib">
    <div class="gt-contrib-box">
      <strong>🏛️ Municipio aporta:</strong>Postes + instalación eléctrica + diseño
    </div>
    <div class="gt-contrib-box">
      <strong>👥 Comunidad aporta:</strong>Mantenimiento + veeduría + Pin Morado activo
    </div>
  </div>
  <div class="gt-fund pending">⏳ BID Lab Gender Bond · $95,000 · Requiere PSG ≥ 30%</div>
  <div style="font-size:11px;color:var(--amber);margin-top:4px">
    PSG actual: 12.83% · Brecha: 17.17 pts
  </div>
</div>

<div style="display:inline-block;padding:8px 12px;
            background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
            border-radius:8px;font-size:12px;color:var(--cyan)">
  💬 Explicar Gov Twin
</div>"""

    # ── 2-COL GRID ────────────────────────────────────────────────────────────
    grid = f"""
<div class="grid-2" style="align-items:start;gap:20px;margin-bottom:16px">
  <div>
    <div class="section-hdr">
      <h3>Mapa Territorial · 7 Parroquias</h3>
      <span class="badge badge-amber">Q1-2026</span>
    </div>
    {svg_map}
  </div>
  <div>
    <div class="section-hdr">
      <h3>Gov Twin · Proyectos Colaborativos</h3>
      <span class="badge badge-cyan">Proyectos Colaborativos</span>
    </div>
    {gt_projects}
  </div>
</div>"""

    # ── PARROQUIAS TABLE ──────────────────────────────────────────────────────
    rows = "".join(_parroquia_row(p) for p in parroquias_sorted)
    tabla = f"""
<div class="card">
  <div class="card-title">📊 Las 7 Parroquias · Inequidad territorial documentada · Q1-2026</div>
  <table class="tbl">
    <thead>
      <tr>
        <th>Parroquia</th>
        <th>TPS ↓</th>
        <th>Agua %</th>
        <th>Habitantes</th>
        <th>$/hab</th>
        <th>Estado</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <div style="font-size:10px;color:var(--muted);margin-top:8px;padding-top:8px;
              border-top:1px solid rgba(255,255,255,.05)">
    📌 TPS = Tasa de Pobreza por Sistema (mayor TPS = mayor vulnerabilidad)
    · Montecristi cabecera: $113/hab · Isabel Muentes: $40/hab
    · Brecha: 2.8×
  </div>
</div>"""

    # ── TECH NOTE ─────────────────────────────────────────────────────────────
    tech = ""
    if show_tech:
        tech = """
<div style="margin-top:16px;font-size:9px;color:rgba(255,255,255,.2);
            border-top:1px solid rgba(255,255,255,.04);padding-top:8px">
  🔧 Fuente: SIAP-ICPI H24 · GeoTwin KB · INEC 2022 · IET Q1-2026 · Corte sellado Q1-2026
</div>"""

    # ── ASSEMBLE & RENDER ─────────────────────────────────────────────────────
    html = hdr + grid + tabla + tech
    render_page(html, show_tech=show_tech, height=1400, extra_css=_GT_CSS)

    # Native CTA
    st.html("<div style='height:8px'></div>")
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("🎯 Ver Congruencia Territorial", use_container_width=True):
            st.session_state["page"] = "congruencias"
            st.rerun()
    with c2:
        if st.button("🔮 Priorizar territorio con Sentinel", use_container_width=True):
            st.session_state["page"] = "sentinel"
            st.rerun()
