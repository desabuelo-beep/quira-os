"""
QUIRA Intelligence — Centro de Mando  (D.3b · Sprint D)
Pantalla Principal · Sala de Mando Institucional · GAD Montecristi

Arquitectura D.2b:
  · BANDA VITAL      → 4 tarjetas de pulso  (clickeables · tamaño por relevancia)
  · MAPA VIVO        → corazón gravitacional (CartoDB Voyager · etiquetas visibles)
  · CINTURÓN         → 13 dominios como capas (métrica · temperatura · actividad)

"QUIRA no gobierna números, gobierna territorio."
El mapa decide. Los índices explican.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from utils.cache_quira import cargar_gm_snapshot, cargar_snapshot
from utils.css_tokens import C
from utils.session import get_rol, is_tecnico

# ── Rutas ─────────────────────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).parent.parent / "data"
_GEOJSON  = _DATA_DIR / "parroquias_montecristi.geojson"


# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE TEMPERATURA  (dominio → background · border · color principal)
# ══════════════════════════════════════════════════════════════════════════════
_TEMP: dict[str, dict[str, str]] = {
    "critico": {"bg": "rgba(239,68,68,.09)",   "bd": "rgba(239,68,68,.32)",   "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.08)",  "bd": "rgba(249,115,22,.28)",  "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.04)",   "bd": "rgba(0,212,255,.14)",   "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.06)",   "bd": "rgba(34,197,94,.22)",   "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.09)",  "bd": "rgba(124,92,252,.30)",  "c": "#7C5CFC"},
}

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CAPAS
# ══════════════════════════════════════════════════════════════════════════════
_CAPAS: list[dict] = [
    {"id": "politica",    "label": "POLÍTICA",     "accent": "#00D4FF"},
    {"id": "ejecutiva",   "label": "EJECUTIVA",    "accent": "#F97316"},
    {"id": "rendicion",   "label": "RENDICIÓN",    "accent": "#7C5CFC"},
    {"id": "territorial", "label": "TERRITORIAL",  "accent": "#22C55E"},
]

# ══════════════════════════════════════════════════════════════════════════════
# 13 DOMINIOS INSTITUCIONALES
# metric: valor headline visible en la tarjeta
# temp:   temperatura visual ("critico"|"alerta"|"normal"|"verde"|"funds")
# grav:   gravedad visual  (1=leve · 2=medio · 3=dominante)
# act:    actividad        ("activo"|"monitoreo"|"pasivo")
# mod:    módulo GOV destino de navegación
# tec:    True = solo visible completo para Técnico/Administrador
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS: list[dict] = [
    # ── CAPA POLÍTICA ─────────────────────────────────────────────────────────
    {
        "id": "d01", "capa": "politica",
        "nombre": "Salud Institucional",
        "metric": "17.4%",
        "nota": "Índice cumplimiento · umbral 65%",
        "temp": "critico", "grav": 3, "act": "activo",
        "mod": "situacion",
    },
    {
        "id": "d02", "capa": "politica",
        "nombre": "Fidelidad Política",
        "metric": "44 / 66",
        "nota": "Compromisos CNE cumplidos",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "situacion",
    },
    {
        "id": "d03", "capa": "politica",
        "nombre": "Planificación y Ejecución",
        "metric": "4 metas",
        "nota": "Sin vínculo presupuestario",
        "temp": "alerta", "grav": 2, "act": "monitoreo",
        "mod": "situacion",
    },
    # ── CAPA EJECUTIVA ─────────────────────────────────────────────────────────
    {
        "id": "d04", "capa": "ejecutiva",
        "nombre": "Holding Municipal",
        "metric": "68.7%",
        "nota": "Promedio 4 entidades",
        "temp": "alerta", "grav": 2, "act": "activo",
        "mod": "municipal",
    },
    {
        "id": "d05", "capa": "ejecutiva",
        "nombre": "Eficiencia Operacional",
        "metric": "—",
        "nota": "Rendimiento relativo por entidad",
        "temp": "normal", "grav": 1, "act": "monitoreo",
        "mod": "analisis", "tec": True,
    },
    {
        "id": "d06", "capa": "ejecutiva",
        "nombre": "Equidad Territorial",
        "metric": "$40/hab",
        "nota": "Rural vs $217 cabecera",
        "temp": "alerta", "grav": 2, "act": "activo",
        "mod": "geotwin", "tec": True,
    },
    # ── CAPA RENDICIÓN ─────────────────────────────────────────────────────────
    {
        "id": "d07", "capa": "rendicion",
        "nombre": "Transparencia",
        "metric": "—",
        "nota": "Gobierno abierto · CPCCS · LOTAIP",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "rdc",
    },
    {
        "id": "d08", "capa": "rendicion",
        "nombre": "Participación Ciudadana",
        "metric": "—",
        "nota": "Presupuesto participativo · IGP",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "confianza",
    },
    {
        "id": "d09", "capa": "rendicion",
        "nombre": "Género y Equidad Social",
        "metric": "12.83%",
        "nota": "Presupuesto género · umbral 30%",
        "temp": "critico", "grav": 2, "act": "activo",
        "mod": "genero",
    },
    {
        "id": "d10", "capa": "rendicion",
        "nombre": "Ambiente y Sostenibilidad",
        "metric": "0%",
        "nota": "Metas FA-CC · FA-DIS sin ejecución",
        "temp": "critico", "grav": 2, "act": "activo",
        "mod": "genero",
    },
    # ── CAPA TERRITORIAL ───────────────────────────────────────────────────────
    {
        "id": "d11", "capa": "territorial",
        "nombre": "Cooperación Internacional",
        "metric": "$3.66M",
        "nota": "Fondos condicionados · 3 fuentes activas",
        "temp": "funds", "grav": 3, "act": "activo",
        "mod": "cooperacion",
    },
    {
        "id": "d12", "capa": "territorial",
        "nombre": "Agenda 2030",
        "metric": "—",
        "nota": "ODS ↔ PDOT · alineación activa",
        "temp": "normal", "grav": 1, "act": "monitoreo",
        "mod": "ods",
    },
    {
        "id": "d13", "capa": "territorial",
        "nombre": "Observabilidad Longitudinal",
        "metric": "1 punto",
        "nota": "Sistema activo · histórico iniciado",
        "temp": "verde", "grav": 1, "act": "pasivo",
        "mod": "control", "tec": True,
    },
]

# ── Estilos de estado del mapa — ajustados para CartoDB Voyager (fondo claro)
_MAP_ESTADO: dict[str, dict] = {
    "NORMAL":     {"c": "#0284C7", "fo": 0.55, "r": 20},   # azul — visible sobre beige
    "ALERTA":     {"c": "#EA580C", "fo": 0.60, "r": 17},   # naranja
    "PRIORIDAD":  {"c": "#DC2626", "fo": 0.65, "r": 22},   # rojo
    "EMERGENCIA": {"c": "#7F1D1D", "fo": 0.72, "r": 18},   # rojo oscuro
}


# ══════════════════════════════════════════════════════════════════════════════
# CARGA DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def _load_data() -> dict[str, Any]:
    """Carga snapshot activo + Gold Master JSON. Retorna dict unificado."""
    snap, _meta = cargar_snapshot()
    gm          = cargar_gm_snapshot()

    d: dict[str, Any] = {
        "icpi_pct":      None,
        "icpi_clasif":   "—",
        "n_alertas":     0,
        "riesgo_clasif": "—",
        "alertas_act":   [],
        "has_snap":      bool(snap),
    }

    if snap:
        icpi_d = snap.get("icpi", {})
        d["icpi_pct"]    = icpi_d.get("global_pct") or icpi_d.get("global")
        d["icpi_clasif"] = icpi_d.get("clasificacion", "—")

        sat_d = snap.get("sat", {})
        d["n_alertas"]     = sat_d.get("total_activas", 0)
        d["riesgo_clasif"] = sat_d.get("clasif_riesgo", "—").upper()
        d["alertas_act"]   = sat_d.get("alertas_activas", [])

    if gm and d["icpi_pct"] is None:
        icpi_gm = gm.get("icpi", {})
        d["icpi_pct"]    = icpi_gm.get("global_pct") or icpi_gm.get("global")
        d["icpi_clasif"] = icpi_gm.get("clasificacion", "—")

    return d


# ══════════════════════════════════════════════════════════════════════════════
# BANDA VITAL — 4 tarjetas clickeables de pulso institucional
# Tamaño diferenciado por relevancia: c1+c2 grandes · c3+c4 medianas
# ══════════════════════════════════════════════════════════════════════════════

def _bv_card_html(label: str, value: str, color: str, sub: str) -> str:
    """HTML de tarjeta Banda Vital — visual completa, sin botón."""
    return f"""
<div style="background:rgba(8,13,24,.97);border:1px solid {color}30;
            border-top:2px solid {color};border-radius:10px;
            padding:18px 20px 12px;margin-bottom:6px">
  <div style="font-size:8px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
              color:rgba(255,255,255,.30);margin-bottom:10px">{label}</div>
  <div style="font-size:2.1rem;font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.04em;line-height:1;margin-bottom:8px">{value}</div>
  <div style="font-size:9px;color:rgba(255,255,255,.28);
              letter-spacing:.01em;line-height:1.4">{sub}</div>
</div>"""


def _bv_card_sm_html(label: str, value: str, color: str, sub: str) -> str:
    """HTML de tarjeta Banda Vital pequeña."""
    return f"""
<div style="background:rgba(8,13,24,.97);border:1px solid {color}28;
            border-top:2px solid {color};border-radius:10px;
            padding:15px 16px 10px;margin-bottom:6px">
  <div style="font-size:8px;font-weight:700;letter-spacing:.10em;text-transform:uppercase;
              color:rgba(255,255,255,.28);margin-bottom:8px">{label}</div>
  <div style="font-size:1.6rem;font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.03em;line-height:1;margin-bottom:6px">{value}</div>
  <div style="font-size:9px;color:rgba(255,255,255,.26);
              letter-spacing:.01em;line-height:1.35">{sub}</div>
</div>"""


def _render_banda_vital(d: dict) -> None:
    """Banda superior — 4 tarjetas de pulso con navegación integrada."""
    icpi_pct    = d.get("icpi_pct")
    n_alertas   = d.get("n_alertas", 0)
    riesgo_cl   = d.get("riesgo_clasif", "—")
    icpi_clasif = d.get("icpi_clasif", "—")

    icpi_color  = C.sem(icpi_pct) if icpi_pct is not None else "#EF4444"
    alert_color = "#EF4444" if n_alertas > 0 else "#22C55E"

    icpi_str   = f"{icpi_pct:.1f}%" if icpi_pct is not None else "17.4%"
    hold_avg   = 68.7
    hold_color = C.sem(hold_avg)

    # Columnas: 2 grandes · 2 medianas (ratio refleja relevancia)
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 1.5, 1.5], gap="small")

    with c1:
        st.markdown(_bv_card_html(
            "Cumplimiento Municipal", icpi_str, icpi_color,
            f"{icpi_clasif} · umbral institucional 65%",
        ), unsafe_allow_html=True)
        if st.button("Ver situación institucional →", key="bv_icpi",
                     use_container_width=True):
            st.session_state["gov_module"] = "situacion"
            st.rerun()

    with c2:
        st.markdown(_bv_card_html(
            "Fondos en Riesgo", "$3.66M", "#7C5CFC",
            "3 fuentes condicionadas · acción requerida",
        ), unsafe_allow_html=True)
        if st.button("Ver cooperación →", key="bv_fondos",
                     use_container_width=True):
            st.session_state["gov_module"] = "cooperacion"
            st.rerun()

    with c3:
        sub_alerta = riesgo_cl if riesgo_cl not in ("—", "") else "Sin alertas críticas"
        st.markdown(_bv_card_sm_html(
            "Alertas Activas", str(n_alertas), alert_color, sub_alerta,
        ), unsafe_allow_html=True)
        if st.button("Ver alertas →", key="bv_alertas",
                     use_container_width=True):
            st.session_state["gov_module"] = "control"
            st.rerun()

    with c4:
        st.markdown(_bv_card_sm_html(
            "Holding Municipal", f"{hold_avg:.1f}%", hold_color,
            "Promedio 4 entidades",
        ), unsafe_allow_html=True)
        if st.button("Ver holding →", key="bv_holding",
                     use_container_width=True):
            st.session_state["gov_module"] = "municipal"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MAPA VIVO — corazón gravitacional de la pantalla
# CartoDB Voyager: fondo claro · profesional · legible
# ══════════════════════════════════════════════════════════════════════════════

def _build_folium_map() -> Any | None:
    """Construye el mapa Folium: CartoDB Voyager + círculos + etiquetas de parroquia."""
    try:
        import folium
        from streamlit_folium import st_folium as _sf  # noqa: F401  importability check
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

    # CartoDB Voyager — profesional, legible, sin fondo negro
    folium.TileLayer(
        tiles="https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
        attr="© OpenStreetMap © CARTO",
        max_zoom=18,
        opacity=1.0,
    ).add_to(m)

    for feat in gj_data.get("features", []):
        props  = feat.get("properties", {})
        coords = feat["geometry"]["coordinates"]   # [lng, lat]
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

        # Tooltip elegante (dark card que contrasta sobre fondo claro)
        tooltip_body = f"""
<div style="font-family:Inter,system-ui,sans-serif;background:#0F172A;color:#E2E8F0;
            border:1px solid rgba(255,255,255,.12);border-radius:8px;
            padding:10px 14px;min-width:180px;box-shadow:0 4px 20px rgba(0,0,0,.45);
            pointer-events:none">
  <div style="font-size:12px;font-weight:700;margin-bottom:4px">{nombre}</div>
  <div style="font-size:9px;color:{color};font-weight:700;letter-spacing:.08em;
              text-transform:uppercase;margin-bottom:8px">{estado} · {tipo}</div>
  <div style="font-size:10px;color:rgba(255,255,255,.50);line-height:1.65">
    {f'{hab:,} habitantes' if hab else ''}
    {f'<br>Inversión: ${pc}/hab' if pc else ''}
    {f'<br>Cobertura agua: {agua}%' if agua else ''}
  </div>
</div>"""

        # Anillo exterior (glow) para estados críticos
        if estado in ("EMERGENCIA", "PRIORIDAD"):
            folium.CircleMarker(
                location=[lat, lng],
                radius=radius + 14,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.10,
                weight=0.5,
                interactive=False,
            ).add_to(m)

        # Círculo principal
        folium.CircleMarker(
            location=[lat, lng],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=sty["fo"],
            weight=2.0,
            tooltip=folium.Tooltip(tooltip_body, sticky=False, parse_html=True),
        ).add_to(m)

        # Etiqueta de nombre — texto oscuro visible sobre mapa claro
        nombre_corto = (
            nombre
            .replace(" (cabecera)", "")
            .replace("Parroquia ", "")
        )
        # margin-top posiciona la etiqueta debajo del círculo
        lbl_mt = radius + 8 if not is_cab else radius + 6
        folium.Marker(
            location=[lat, lng],
            icon=folium.DivIcon(
                html=f"""<div style="
                    font-family: Inter, system-ui, sans-serif;
                    font-size: 10px;
                    font-weight: 700;
                    color: #1e293b;
                    white-space: nowrap;
                    text-align: center;
                    margin-top: {lbl_mt}px;
                    text-shadow:
                        0 0 3px #fff, 0 0 3px #fff,
                        0 0 3px #fff, 1px 1px 4px rgba(255,255,255,.8);
                ">{nombre_corto}</div>""",
                icon_size=(160, 22),
                icon_anchor=(80, 0),
            ),
            tooltip=folium.Tooltip(tooltip_body, sticky=False, parse_html=True),
        ).add_to(m)

    return m


def _render_mapa() -> None:
    """Sección del mapa — corazón gravitacional de QUIRA."""
    try:
        from streamlit_folium import st_folium
    except ImportError:
        st.info("Instala streamlit-folium para ver el mapa territorial.")
        return

    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
  <div style="width:2px;height:14px;background:#00D4FF;border-radius:1px"></div>
  <span style="font-size:9px;font-weight:700;letter-spacing:.12em;
               text-transform:uppercase;color:rgba(255,255,255,.38)">
    TERRITORIO MUNICIPAL
  </span>
  <span style="font-size:9px;color:rgba(255,255,255,.18);margin-left:auto;
               font-family:'JetBrains Mono',monospace">
    Cantón Montecristi · Manabí · 7 parroquias
  </span>
</div>
""", unsafe_allow_html=True)

    m = _build_folium_map()

    if m is None:
        st.markdown("""
<div style="height:420px;display:flex;align-items:center;justify-content:center;
            background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.07);
            border-radius:12px;color:rgba(255,255,255,.25);font-size:12px;
            flex-direction:column;gap:8px">
  <span style="font-size:20px;opacity:.4">🗺</span>
  <span>Mapa territorial no disponible</span>
</div>
""", unsafe_allow_html=True)
        return

    st.markdown("""
<style>
iframe[title="streamlit_folium.st_folium"] {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.08) !important;
}
</style>
""", unsafe_allow_html=True)

    map_data = st_folium(
        m,
        use_container_width=True,
        height=460,
        returned_objects=["last_object_clicked"],
        key="qcc_mapa_vivo",
    )

    # Click en parroquia → navegar a módulo territorial
    if map_data and map_data.get("last_object_clicked"):
        target = "geotwin" if is_tecnico() else "situacion"
        st.session_state["gov_module"] = target
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# CINTURÓN DE CAPAS — 13 dominios como capas del territorio
# ══════════════════════════════════════════════════════════════════════════════

def _domain_card_html(dom: dict, accessible: bool) -> str:
    """HTML de tarjeta de dominio con métrica headline · temperatura · actividad."""
    t    = _TEMP.get(dom["temp"], _TEMP["normal"])
    grav = dom["grav"]
    act  = dom["act"]

    # Padding y tipografía por gravedad
    pad     = {3: "16px 15px 13px", 2: "12px 13px 10px", 1: "10px 12px 9px"}[grav]
    nomb_fs = {3: "12px",           2: "11.5px",          1: "11px"         }[grav]
    nota_fs = {3: "9px",            2: "9px",              1: "8.5px"        }[grav]

    # Métrica headline
    metric  = dom.get("metric", "—")
    met_fs  = {3: "1.55rem", 2: "1.2rem", 1: "1rem"}[grav]
    if metric and metric != "—":
        met_html = (
            f'<div style="font-size:{met_fs};font-weight:900;color:{t["c"]};'
            f'font-family:"JetBrains Mono",monospace;letter-spacing:-.03em;'
            f'line-height:1;margin:7px 0 5px">{metric}</div>'
        )
    else:
        met_html = '<div style="height:6px"></div>'

    # Dot de actividad
    if act == "activo":
        dot = (
            f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            f'background:{t["c"]};flex-shrink:0;margin-top:3px;'
            f'animation:qcc-pulse 1.9s ease-in-out infinite"></span>'
        )
    elif act == "monitoreo":
        dot = (
            f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            f'background:{t["c"]};flex-shrink:0;margin-top:3px;opacity:.55"></span>'
        )
    else:
        dot = (
            '<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            'background:rgba(255,255,255,.16);flex-shrink:0;margin-top:3px"></span>'
        )

    lock = (
        '<div style="font-size:8px;color:rgba(255,255,255,.18);margin-top:4px;'
        'letter-spacing:.04em;text-transform:uppercase">Sección técnica</div>'
        if not accessible else ""
    )

    dim = "opacity:.42;" if not accessible else ""

    return f"""
<div style="background:{t['bg']};border:1px solid {t['bd']};border-radius:9px;
            padding:{pad};margin-bottom:0;{dim}">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px">
    <div style="font-size:{nomb_fs};font-weight:700;color:#DDE4EE;
                line-height:1.2;flex:1">{dom['nombre']}</div>
    {dot}
  </div>
  {met_html}
  <div style="font-size:{nota_fs};color:rgba(255,255,255,.36);
              line-height:1.40">{dom['nota']}</div>
  {lock}
</div>"""


def _render_cinturon() -> None:
    """Cinturón cognitivo — 4 capas × 13 dominios como capas del territorio."""
    # CSS de animaciones
    st.markdown("""
<style>
@keyframes qcc-pulse {
  0%, 100% { opacity: 1;   transform: scale(1);   }
  50%       { opacity: .25; transform: scale(.68); }
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">
  <div style="width:2px;height:14px;background:#7C5CFC;border-radius:1px"></div>
  <span style="font-size:9px;font-weight:700;letter-spacing:.12em;
               text-transform:uppercase;color:rgba(255,255,255,.38)">CAPAS OPERATIVAS</span>
  <span style="font-size:9px;color:rgba(255,255,255,.18);margin-left:auto;
               font-family:'JetBrains Mono',monospace">13 dominios · 4 capas institucionales</span>
</div>
""", unsafe_allow_html=True)

    cols = st.columns(4, gap="small")

    for col_obj, capa_cfg in zip(cols, _CAPAS):
        with col_obj:
            accent = capa_cfg["accent"]
            # Cabecera de capa
            st.markdown(f"""
<div style="font-size:8px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;
            color:{accent};border-bottom:1px solid {accent}28;
            padding-bottom:7px;margin-bottom:9px">{capa_cfg['label']}</div>
""", unsafe_allow_html=True)

            capa_domains = [d for d in _DOMAINS if d["capa"] == capa_cfg["id"]]

            for dom in capa_domains:
                tec_only   = dom.get("tec", False)
                accessible = not tec_only or is_tecnico()

                # Tarjeta visual HTML
                st.markdown(_domain_card_html(dom, accessible), unsafe_allow_html=True)

                # Botón de navegación — conectado visualmente a la tarjeta
                if accessible:
                    btn_label = f"Ver {dom['nombre']} →"
                    if st.button(
                        btn_label,
                        key=f"qcc_nav_{dom['id']}",
                        use_container_width=True,
                    ):
                        st.session_state["gov_module"] = dom["mod"]
                        st.rerun()
                else:
                    # Espacio equivalente al botón para mantener alineación
                    st.markdown('<div style="height:34px"></div>',
                                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Renderiza el Centro de Mando."""
    # ── CSS global ────────────────────────────────────────────────────────────
    st.markdown("""
<style>
/* Padding superior reducido */
section[data-testid="stMainBlockContainer"] > div:first-child {
    padding-top: 14px;
}
/* Botones de navegación — uniformes, discretos */
div[data-testid="stButton"] > button {
    height: 28px !important;
    min-height: 28px !important;
    padding: 0 12px !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,.33) !important;
    background: rgba(255,255,255,.025) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    border-radius: 6px !important;
    letter-spacing: .02em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: color .15s, background .15s, border-color .15s;
    margin-top: 4px;
    margin-bottom: 6px;
}
div[data-testid="stButton"] > button:hover {
    color: rgba(255,255,255,.78) !important;
    background: rgba(255,255,255,.055) !important;
    border-color: rgba(255,255,255,.14) !important;
}
div[data-testid="stButton"] > button:focus {
    box-shadow: none !important;
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

    # ── Datos ─────────────────────────────────────────────────────────────────
    data = _load_data()

    # ── 1 · Banda Vital ───────────────────────────────────────────────────────
    _render_banda_vital(data)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── 2 · Mapa Vivo — corazón gravitacional ────────────────────────────────
    _render_mapa()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── 3 · Cinturón de Capas ─────────────────────────────────────────────────
    _render_cinturon()

    # ── Footer institucional ──────────────────────────────────────────────────
    st.markdown("""
<div style="font-size:8px;color:rgba(255,255,255,.10);margin-top:22px;
            border-top:1px solid rgba(255,255,255,.04);padding-top:10px;
            font-family:'JetBrains Mono',monospace;letter-spacing:.03em;
            display:flex;justify-content:space-between">
  <span>QUIRA Intelligence · Centro de Mando · D.3b</span>
  <span>GAD Montecristi · Manabí · Ecuador</span>
</div>
""", unsafe_allow_html=True)
