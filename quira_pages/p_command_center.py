"""
QUIRA Intelligence — Centro de Mando  (D.3a Skeleton · Sprint D)
Pantalla Principal · Sala de Mando Institucional · GAD Montecristi

Arquitectura D.2b:
  · BANDA VITAL      → 4 indicadores de pulso  (thin strip, lectura 0–3s)
  · MAPA VIVO        → corazón gravitacional   (ancla territorial, full-width)
  · CINTURÓN         → 13 dominios como capas  (temperatura · gravedad · actividad)

"QUIRA no gobierna números, gobierna territorio."
El mapa decide. Los índices explican.

Estética objetivo: Bloomberg Terminal institucional + sala situacional civil.
Más silencioso. Más elegante. Más territorial.

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
# D.3a: estados derivados del Gold Master (hardcoded).
# D.3b+: estados en vivo desde el motor de cálculo.
#
# temp:  temperatura visual ("critico" | "alerta" | "normal" | "verde" | "funds")
# grav:  gravedad visual  (1=leve · 2=medio · 3=dominante)
# act:   actividad        ("activo" | "monitoreo" | "pasivo")
# mod:   módulo GOV destino de navegación
# tec:   True = solo visible para Técnico/Administrador
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS: list[dict] = [
    # ── CAPA POLÍTICA ─────────────────────────────────────────────────────────
    {
        "id": "d01", "capa": "politica",
        "nombre": "Salud Institucional",
        "nota": "Índice de cumplimiento en zona crítica",
        "temp": "critico", "grav": 3, "act": "activo",
        "mod": "situacion",
    },
    {
        "id": "d02", "capa": "politica",
        "nombre": "Fidelidad Política",
        "nota": "48 de 66 compromisos CNE activos",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "situacion",
    },
    {
        "id": "d03", "capa": "politica",
        "nombre": "Planificación y Ejecución",
        "nota": "4 metas sin vínculo presupuestario",
        "temp": "alerta", "grav": 2, "act": "monitoreo",
        "mod": "situacion",
    },
    # ── CAPA EJECUTIVA ─────────────────────────────────────────────────────────
    {
        "id": "d04", "capa": "ejecutiva",
        "nombre": "Holding Municipal",
        "nota": "EP Aseo 58.4% · GAD 61.2% · vigilancia",
        "temp": "alerta", "grav": 2, "act": "activo",
        "mod": "municipal",
    },
    {
        "id": "d05", "capa": "ejecutiva",
        "nombre": "Eficiencia Operacional",
        "nota": "Rendimiento relativo por entidad",
        "temp": "normal", "grav": 1, "act": "monitoreo",
        "mod": "analisis", "tec": True,
    },
    {
        "id": "d06", "capa": "ejecutiva",
        "nombre": "Equidad Territorial",
        "nota": "$40/hab sector rural vs $217 cabecera",
        "temp": "alerta", "grav": 2, "act": "activo",
        "mod": "geotwin", "tec": True,
    },
    # ── CAPA RENDICIÓN ─────────────────────────────────────────────────────────
    {
        "id": "d07", "capa": "rendicion",
        "nombre": "Transparencia",
        "nota": "Gobierno abierto · CPCCS · LOTAIP",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "rdc",
    },
    {
        "id": "d08", "capa": "rendicion",
        "nombre": "Participación Ciudadana",
        "nota": "IGP · presupuesto participativo",
        "temp": "normal", "grav": 1, "act": "pasivo",
        "mod": "confianza",
    },
    {
        "id": "d09", "capa": "rendicion",
        "nombre": "Género y Equidad Social",
        "nota": "Presupuesto género: 12.83% — alerta activa",
        "temp": "critico", "grav": 2, "act": "activo",
        "mod": "genero",
    },
    {
        "id": "d10", "capa": "rendicion",
        "nombre": "Ambiente y Sostenibilidad",
        "nota": "Metas FA-CC y FA-DIS: 0% ejecución",
        "temp": "critico", "grav": 2, "act": "activo",
        "mod": "genero",
    },
    # ── CAPA TERRITORIAL ───────────────────────────────────────────────────────
    {
        "id": "d11", "capa": "territorial",
        "nombre": "Cooperación Internacional",
        "nota": "$3.66M condicionados · 3 fuentes activas",
        "temp": "funds", "grav": 3, "act": "activo",
        "mod": "cooperacion",
    },
    {
        "id": "d12", "capa": "territorial",
        "nombre": "Agenda 2030",
        "nota": "ODS ↔ PDOT · alineación activa",
        "temp": "normal", "grav": 1, "act": "monitoreo",
        "mod": "ods",
    },
    {
        "id": "d13", "capa": "territorial",
        "nombre": "Observabilidad Longitudinal",
        "nota": "Sistema activo · 1 punto histórico registrado",
        "temp": "verde", "grav": 1, "act": "pasivo",
        "mod": "control", "tec": True,
    },
]

# ── Estilos de estado del mapa (geojson) ──────────────────────────────────────
_MAP_ESTADO: dict[str, dict] = {
    "NORMAL":     {"c": "#00D4FF", "fo": 0.22, "r": 20},
    "ALERTA":     {"c": "#F97316", "fo": 0.32, "r": 17},
    "PRIORIDAD":  {"c": "#EF4444", "fo": 0.42, "r": 22},
    "EMERGENCIA": {"c": "#DC2626", "fo": 0.48, "r": 17},
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
# BANDA VITAL — 4 chips de pulso institucional
# ══════════════════════════════════════════════════════════════════════════════

def _render_banda_vital(d: dict) -> None:
    """Banda superior fina — estado del municipio en 0–3 segundos."""
    icpi_pct   = d.get("icpi_pct")
    n_alertas  = d.get("n_alertas", 0)
    riesgo_cl  = d.get("riesgo_clasif", "—")
    icpi_clasif = d.get("icpi_clasif", "—")

    icpi_color  = C.sem(icpi_pct) if icpi_pct is not None else "#64748B"
    alert_color = "#EF4444" if n_alertas > 0 else "#22C55E"
    riesgo_color = {
        "BAJO": "#22C55E", "MEDIO": "#F59E0B",
        "ALTO": "#F97316", "CRÍTICO": "#EF4444",
    }.get(riesgo_cl, "#64748B")

    icpi_str  = f"{icpi_pct:.2f}%" if icpi_pct is not None else "—"
    hold_avg  = 68.7   # D.3a: HPT-M promedio Gold Master (Bomberos+Patronato+GAD+EP Aseo)
    hold_color = C.sem(hold_avg)

    def _chip(label: str, value: str, color: str, sub: str = "") -> str:
        sub_html = (
            f'<div style="font-size:9px;color:rgba(255,255,255,.28);margin-top:2px;'
            f'letter-spacing:.02em">{sub}</div>'
            if sub else ""
        )
        return f"""
<div style="flex:1;border-right:1px solid rgba(255,255,255,.05);
            padding:11px 20px;min-width:0">
  <div style="font-size:8px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
              color:rgba(255,255,255,.32);margin-bottom:4px">{label}</div>
  <div style="font-size:1.5rem;font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;
              letter-spacing:-.03em;line-height:1">{value}</div>
  {sub_html}
</div>"""

    c1 = _chip("Cumplimiento Municipal", icpi_str,        icpi_color,  icpi_clasif)
    c2 = _chip("Alertas Activas",        str(n_alertas),  alert_color, riesgo_cl)
    c3 = _chip("Holding Municipal",      f"{hold_avg:.1f}%", hold_color, "Promedio 4 entidades")
    c4 = _chip("Fondos en Riesgo",       "$3.66M",        "#7C5CFC",   "3 fuentes condicionadas")

    st.markdown(f"""
<div style="display:flex;background:rgba(8,13,24,.96);
            border:1px solid rgba(255,255,255,.07);border-radius:10px;
            overflow:hidden;margin-bottom:14px">
  {c1}{c2}{c3}{c4}
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAPA VIVO — corazón gravitacional de la pantalla
# ══════════════════════════════════════════════════════════════════════════════

def _build_folium_map() -> Any | None:
    """Construye el mapa Folium: CartoDB Dark Matter + círculos de estado."""
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

    # Base: CartoDB Dark Matter — mínimo, elegante
    folium.TileLayer(
        tiles="https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="© OpenStreetMap © CARTO",
        max_zoom=18,
        opacity=0.88,
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

        sty   = _MAP_ESTADO.get(estado, {"c": "#64748B", "fo": 0.20, "r": 14})
        color = sty["c"]
        radius = sty["r"]
        is_cab = "cabecera" in nombre.lower()
        if is_cab:
            radius = 38

        # Tooltip elegante
        tooltip_body = f"""
<div style="font-family:Inter,system-ui,sans-serif;background:#080D18;color:#E2E8F0;
            border:1px solid rgba(255,255,255,.12);border-radius:8px;
            padding:10px 14px;min-width:175px;box-shadow:0 4px 20px rgba(0,0,0,.6);
            pointer-events:none">
  <div style="font-size:12px;font-weight:700;margin-bottom:5px">{nombre}</div>
  <div style="font-size:9px;color:{color};font-weight:700;letter-spacing:.08em;
              text-transform:uppercase;margin-bottom:8px">{estado} · {tipo}</div>
  <div style="font-size:10px;color:rgba(255,255,255,.45);line-height:1.65">
    {f'{hab:,} habitantes' if hab else ''}
    {f'<br>Inversión: ${pc}/hab' if pc else ''}
    {f'<br>Cobertura agua: {agua}%' if agua else ''}
  </div>
</div>"""

        # Anillo exterior (glow) para estados críticos
        if estado in ("EMERGENCIA", "PRIORIDAD"):
            folium.CircleMarker(
                location=[coords[1], coords[0]],
                radius=radius + 12,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.06,
                weight=0.4,
                interactive=False,
            ).add_to(m)

        # Círculo principal
        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=sty["fo"],
            weight=1.5,
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

    # Encabezado de sección — fino, no compite con el mapa
    st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
  <div style="width:2px;height:14px;background:#00D4FF;border-radius:1px"></div>
  <span style="font-size:9px;font-weight:700;letter-spacing:.12em;
               text-transform:uppercase;color:rgba(255,255,255,.38)">
    TERRITORIO MUNICIPAL
  </span>
  <span style="font-size:9px;color:rgba(255,255,255,.18);margin-left:auto;
               font-family:'JetBrains Mono',monospace">
    Cantón Montecristi · Manabí
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

    # Estilos del iframe (borde elegante)
    st.markdown("""
<style>
iframe[title="streamlit_folium.st_folium"] {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.06) !important;
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
    """HTML de tarjeta de dominio con temperatura · gravedad · actividad."""
    t    = _TEMP.get(dom["temp"], _TEMP["normal"])
    grav = dom["grav"]
    act  = dom["act"]

    # Espaciado según gravedad
    pad = {3: "17px 16px", 2: "13px 14px", 1: "10px 12px"}[grav]
    fs  = {3: "12.5px",    2: "11.5px",    1: "11px"      }[grav]
    fn  = {3: "9.5px",     2: "9px",       1: "9px"       }[grav]

    # Dot de actividad
    if act == "activo":
        dot = (
            f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            f'background:{t["c"]};flex-shrink:0;margin-top:2px;'
            f'animation:qcc-pulse 1.9s ease-in-out infinite"></span>'
        )
    elif act == "monitoreo":
        dot = (
            f'<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            f'background:{t["c"]};flex-shrink:0;margin-top:2px;opacity:.65"></span>'
        )
    else:
        dot = (
            '<span style="display:inline-block;width:5px;height:5px;border-radius:50%;'
            'background:rgba(255,255,255,.2);flex-shrink:0;margin-top:2px"></span>'
        )

    lock = (
        '<div style="font-size:8px;color:rgba(255,255,255,.18);margin-top:4px;'
        'letter-spacing:.05em;text-transform:uppercase">Sección técnica</div>'
        if not accessible else ""
    )

    dim = "opacity:.52;" if not accessible else ""

    return f"""
<div style="background:{t['bg']};border:1px solid {t['bd']};border-radius:9px;
            padding:{pad};margin-bottom:6px;{dim}">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px">
    <div style="font-size:{fs};font-weight:700;color:#DDE4EE;line-height:1.25;flex:1">
      {dom['nombre']}
    </div>
    {dot}
  </div>
  <div style="font-size:{fn};color:rgba(255,255,255,.40);margin-top:5px;line-height:1.45">
    {dom['nota']}
  </div>
  {lock}
</div>"""


def _render_cinturon() -> None:
    """Cinturón cognitivo — 4 capas × 13 dominios como capas del territorio."""
    # CSS global de animaciones
    st.markdown("""
<style>
@keyframes qcc-pulse {
  0%, 100% { opacity: 1;   transform: scale(1);    }
  50%       { opacity: .30; transform: scale(.72);  }
}
</style>
""", unsafe_allow_html=True)

    # Encabezado de sección
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

                st.markdown(_domain_card_html(dom, accessible), unsafe_allow_html=True)

                # Botón de navegación — solo para dominios accesibles
                if accessible:
                    if st.button(
                        "→",
                        key=f"qcc_nav_{dom['id']}",
                        help=f"Ir a: {dom['nombre']}",
                        use_container_width=True,
                    ):
                        st.session_state["gov_module"] = dom["mod"]
                        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Renderiza el Centro de Mando D.3a."""
    # ── CSS base ─────────────────────────────────────────────────────────────
    st.markdown("""
<style>
/* Reduce padding superior en main block */
section[data-testid="stMainBlockContainer"] > div:first-child {
    padding-top: 14px;
}
/* Botones de navegación de dominio — sutiles, no compiten */
div[data-testid="stButton"] > button {
    height: 22px !important;
    min-height: 22px !important;
    padding: 0 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,.28) !important;
    background: transparent !important;
    border: none !important;
    border-radius: 4px !important;
    transition: color .15s, background .15s;
    margin-bottom: 2px;
}
div[data-testid="stButton"] > button:hover {
    color: rgba(255,255,255,.7) !important;
    background: rgba(255,255,255,.04) !important;
}
</style>
""", unsafe_allow_html=True)

    # ── Datos ─────────────────────────────────────────────────────────────────
    data = _load_data()

    # ── 1 · Banda Vital ───────────────────────────────────────────────────────
    _render_banda_vital(data)

    # ── 2 · Mapa Vivo — corazón gravitacional ────────────────────────────────
    _render_mapa()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── 3 · Cinturón de Capas ─────────────────────────────────────────────────
    _render_cinturon()

    # ── Footer institucional ──────────────────────────────────────────────────
    st.markdown("""
<div style="font-size:8px;color:rgba(255,255,255,.1);margin-top:22px;
            border-top:1px solid rgba(255,255,255,.04);padding-top:10px;
            font-family:'JetBrains Mono',monospace;letter-spacing:.03em;
            display:flex;justify-content:space-between">
  <span>QUIRA Intelligence · Centro de Mando · D.3a</span>
  <span>GAD Montecristi · Manabí · Ecuador</span>
</div>
""", unsafe_allow_html=True)
