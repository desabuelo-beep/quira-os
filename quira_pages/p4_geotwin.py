"""
QUIRA OS v0.1 — P-04 GeoTwin · Territorio
Mapa Folium real (Leaflet) + tabla parroquias + Gov Twin
Dylus Lab © 2026
"""
import json
import math
from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

_GEOJSON_PATH = Path(__file__).parent.parent / "data" / "parroquias_montecristi.geojson"

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

def _tps_color(tps: float) -> str:
    if tps >= 60:
        return "#FF4D6D"
    if tps >= 40:
        return "#FF8C00"
    if tps >= 28:
        return "#FFB800"
    return "#00D4FF"


def _build_folium_map(parroquias: list) -> folium.Map:
    m = folium.Map(
        location=[-1.05, -80.62],
        zoom_start=10,
        tiles="CartoDB dark_matter",
        attr="© CartoDB © OpenStreetMap",
        prefer_canvas=True,
    )

    geojson_data = None
    if _GEOJSON_PATH.exists():
        geojson_data = json.loads(_GEOJSON_PATH.read_text(encoding="utf-8"))

    p_lookup = {p["nombre"]: p for p in parroquias}
    features = geojson_data["features"] if geojson_data else []

    for feat in features:
        props  = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        nombre  = props["nombre"]
        data    = p_lookup.get(nombre, props)

        tps     = data.get("tps", props.get("tps", 0))
        agua    = data.get("agua", props.get("agua", 0))
        hab     = data.get("habitantes", props.get("habitantes", 0))
        per_cap = data.get("per_capita", props.get("per_capita", 0))
        estado  = data.get("estado", props.get("estado", ""))
        emoji   = props.get("emoji", "📍")
        critica = props.get("critica", False)

        color  = _tps_color(tps)
        radius = max(8, min(22, int(math.log(max(hab, 100)) * 2.5)))

        badge_colors = {
            "EMERGENCIA": ("#FF4D6D", "#fff"),
            "PRIORIDAD":  ("#7C5CFC", "#fff"),
            "ALERTA":     ("#FFB800", "#000"),
            "NORMAL":     ("#00D4FF", "#000"),
            "OK":         ("#38A169", "#fff"),
        }
        bg, fg = badge_colors.get(estado, ("#333", "#fff"))
        agua_color = "#E53E3E" if agua < 20 else ("#D69E2E" if agua < 50 else "#38A169")

        popup_html = f"""
<div style="font-family:'Inter',sans-serif;background:#0D1B35;color:#E8EDF4;
            padding:14px 16px;border-radius:10px;min-width:210px;
            border:1px solid rgba(0,212,255,.25);box-shadow:0 4px 20px rgba(0,0,0,.6)">
  <div style="font-size:15px;font-weight:700;margin-bottom:8px">{emoji} {nombre}</div>
  <div style="display:inline-block;padding:2px 8px;border-radius:12px;
              font-size:10px;font-weight:700;background:{bg};color:{fg};margin-bottom:10px">
    {estado}
  </div>
  <table style="width:100%;font-size:11px;border-collapse:collapse">
    <tr><td style="color:#8892B0;padding:2px 0">TPS</td>
        <td style="color:{color};font-weight:700;text-align:right">{tps:.1f}</td></tr>
    <tr><td style="color:#8892B0;padding:2px 0">Agua potable</td>
        <td style="color:{agua_color};font-weight:700;text-align:right">{agua:.1f}%</td></tr>
    <tr><td style="color:#8892B0;padding:2px 0">Habitantes</td>
        <td style="text-align:right">{hab:,}</td></tr>
    <tr><td style="color:#8892B0;padding:2px 0">Inversión/hab</td>
        <td style="text-align:right">${per_cap}</td></tr>
  </table>
  {'<div style="margin-top:8px;font-size:10px;color:#FF4D6D;font-weight:600">⚠️ Zona Crítica — intervención urgente</div>' if critica else ''}
</div>"""

        tooltip = f"{emoji} {nombre} · TPS {tps:.0f} · Agua {agua:.0f}%"

        if critica:
            icon = folium.DivIcon(
                html=f"""
<div style="position:relative;width:44px;height:44px;margin-left:-22px;margin-top:-22px">
  <div style="position:absolute;top:50%;left:50%;
              width:{radius*2}px;height:{radius*2}px;
              margin-left:-{radius}px;margin-top:-{radius}px;
              border-radius:50%;background:{color};opacity:.9"></div>
  <div style="position:absolute;top:50%;left:50%;
              width:{radius*2+10}px;height:{radius*2+10}px;
              margin-left:-{radius+5}px;margin-top:-{radius+5}px;
              border-radius:50%;border:2px solid {color};opacity:.4"></div>
</div>""",
                icon_size=(44, 44),
            )
            folium.Marker(
                location=[lat, lon],
                icon=icon,
                tooltip=folium.Tooltip(tooltip, sticky=True),
                popup=folium.Popup(popup_html, max_width=240),
            ).add_to(m)
        else:
            folium.CircleMarker(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                weight=2,
                tooltip=folium.Tooltip(tooltip, sticky=True),
                popup=folium.Popup(popup_html, max_width=240),
            ).add_to(m)

        folium.Marker(
            location=[lat + 0.012, lon],
            icon=folium.DivIcon(
                html=f"""<div style="font-family:'Inter',sans-serif;font-size:10px;
                              font-weight:700;color:#E8EDF4;white-space:nowrap;
                              text-shadow:0 1px 3px #000,0 0 6px #000">{nombre}</div>""",
                icon_size=(120, 16),
                icon_anchor=(60, 0),
            ),
        ).add_to(m)

    folium.Rectangle(
        bounds=[[-1.25, -80.77], [-0.88, -80.38]],
        color="#1E3A5F",
        weight=1.5,
        fill=False,
        dash_array="6 4",
        tooltip="Cantón Montecristi — límite aproximado",
    ).add_to(m)

    return m


def _parroquia_row(p: dict) -> str:
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
    data       = load_all()
    parroquias = data.get("parroquias", [])
    show_tech  = is_tecnico()

    parroquias_sorted = sorted(parroquias, key=lambda x: x["tps"], reverse=True)

    hdr = page_header(
        "④ EQUIDAD TERRITORIAL · GOV TWIN",
        "Territorio + Gov Twin",
        "Nexo Holding Municipal ↔ Ciudadanía · Proyectos colaborativos",
    )
    render_page(hdr, show_tech=show_tech, height=110, extra_css=_GT_CSS)

    col_map, col_gov = st.columns([3, 2], gap="medium")

    with col_map:
        st.markdown(
            '<p style="font-size:13px;font-weight:700;color:#E8EDF4;margin-bottom:8px">'
            '🗺️ Mapa Territorial · 7 Parroquias</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:8px">
  <span style="font-size:11px;color:#8892B0"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#00D4FF;margin-right:4px"></span>Normal</span>
  <span style="font-size:11px;color:#8892B0"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#FFB800;margin-right:4px"></span>Alerta</span>
  <span style="font-size:11px;color:#8892B0"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#FF4D6D;margin-right:4px"></span>Emergencia</span>
  <span style="font-size:11px;color:#8892B0">· Radio = población · Clic = detalle</span>
</div>""",
            unsafe_allow_html=True,
        )

        folium_map = _build_folium_map(parroquias)
        st_folium(
            folium_map,
            width=None,
            height=420,
            returned_objects=[],
            use_container_width=True,
        )

        st.markdown(
            '<p style="font-size:9px;color:rgba(255,255,255,.2);margin-top:4px">'
            'CartoDB Dark Matter · Centroides IGM/INEC 2022 · EPSG:4326</p>',
            unsafe_allow_html=True,
        )

    with col_gov:
        st.markdown(
            '<p style="font-size:13px;font-weight:700;color:#E8EDF4;margin-bottom:8px">'
            '🤝 Gov Twin · Proyectos Colaborativos</p>',
            unsafe_allow_html=True,
        )
        gov_twin_html = """
<div style="font-size:12px;color:var(--muted);margin-bottom:12px;padding:8px;
            background:rgba(0,212,255,.04);border-radius:8px;border:1px solid rgba(0,212,255,.1)">
  <strong style="color:var(--cyan)">¿Qué es Gov Twin?</strong><br>
  La línea de encuentro entre el Holding Municipal y la ciudadanía.
  El municipio aporta recursos técnicos; el barrio aporta mano de obra y custodia.
  Juntos desbloquean fondos no reembolsables imposibles de obtener por separado.
</div>
<div class="gt-project">
  <div class="gt-project-title">
    💧 Sistema Agua · Isabel Muentes
    <span class="badge badge-red" style="float:right">URGENTE</span>
  </div>
  <div class="gt-contrib">
    <div class="gt-contrib-box"><strong>🏛️ Municipio aporta:</strong>Infraestructura hidráulica + diseño técnico</div>
    <div class="gt-contrib-box"><strong>👥 Comunidad aporta:</strong>Mano de obra + Junta de Agua + custodia</div>
  </div>
  <div class="gt-fund priority">🌐 PNUD Agua Rural · $2,400,000 · Score 81/100</div>
  <div style="font-size:11px;color:var(--amber);margin-top:4px">⚠️ Requiere Gobernanza ≥ 55% · Brecha: 1.44 pts</div>
</div>
<div class="gt-project">
  <div class="gt-project-title">🌳 Reforestación Laderas · Colorado</div>
  <div class="gt-contrib">
    <div class="gt-contrib-box"><strong>🏛️ Municipio aporta:</strong>Plantas nativas + técnico forestal</div>
    <div class="gt-contrib-box"><strong>👥 Comunidad aporta:</strong>Mano de obra + custodios del bosque</div>
  </div>
  <div class="gt-fund elegible">✅ Fondo Verde del Clima GEF · $180,000 · Elegible</div>
</div>
<div class="gt-project">
  <div class="gt-project-title">💜 Luminarias · Aníbal San Andrés</div>
  <div class="gt-contrib">
    <div class="gt-contrib-box"><strong>🏛️ Municipio aporta:</strong>Postes + instalación eléctrica</div>
    <div class="gt-contrib-box"><strong>👥 Comunidad aporta:</strong>Mantenimiento + veeduría</div>
  </div>
  <div class="gt-fund pending">⏳ BID Lab Gender Bond · $95,000 · PSG ≥ 30% req.</div>
</div>"""
        render_page(gov_twin_html, show_tech=False, height=560, extra_css=_GT_CSS)

    rows  = "".join(_parroquia_row(p) for p in parroquias_sorted)
    tabla = f"""
<div class="card">
  <div class="card-title">📊 Las 7 Parroquias · Inequidad territorial documentada · Q1-2026</div>
  <table class="tbl">
    <thead><tr>
      <th>Parroquia</th><th>TPS ↓</th><th>Agua %</th>
      <th>Habitantes</th><th>$/hab</th><th>Estado</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <div style="font-size:10px;color:var(--muted);margin-top:8px;padding-top:8px;
              border-top:1px solid rgba(255,255,255,.05)">
    📌 TPS = Tasa de Pobreza por Sistema · Cabecera $113/hab · Isabel Muentes $40/hab · Brecha 2.8×
  </div>
</div>"""

    tech = ""
    if show_tech:
        tech = """
<div style="margin-top:16px;font-size:9px;color:rgba(255,255,255,.2);
            border-top:1px solid rgba(255,255,255,.04);padding-top:8px">
  🔧 Fuente: SIAP-ICPI H24 · GeoTwin KB · INEC 2022 · IET Q1-2026 · Corte sellado Q1-2026
  · Mapa: Folium/Leaflet · CartoDB Dark Matter · GeoJSON centroides IGM
</div>"""

    render_page(tabla + tech, show_tech=show_tech, height=360, extra_css=_GT_CSS)

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("🎯 Ver Congruencia Territorial", use_container_width=True):
            st.session_state["page"] = "congruencias"
            st.rerun()
    with c2:
        if st.button("🔮 Priorizar territorio con Sentinel", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "¿Cuáles son las parroquias con mayor urgencia de inversión según NBI, "
                "cobertura de agua y estado de participación ciudadana? "
                "¿Qué prioriza el PDOT para el territorio?"
            )
            st.rerun()
