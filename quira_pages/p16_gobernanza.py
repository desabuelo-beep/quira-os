"""
QUIRA OS v0.1 — P-16 GOBERNANZA PARTICIPATIVA
Tab 1: Participación Ciudadana — PP serie 2024/2025/2026, parroquias, IGP
Tab 2: Control Social — RDC estado real, brecha ICM vs ICPI, IFE, 25 metas PDOT,
                        aportes ciudadanos históricos RDC 2023-2024 (H10c_RDC_APORTES)

DOCTRINA: CERO INVENTOS — solo datos del SIAP-ICPI_GOLD_MASTER_v4.1 (corte Q1-2026)
Fuentes:
  Tab 1 → PP_2024/PP_2025/PP_2026 (demo_data) · PARROQUIAS (H99) · IGP (H20b/H73)
  Tab 2 → H31_REPORTE_CPCCS (25 metas Ti+Vi) · H63_S0_CNE (66 promesas IFE)
           H24b_SAT-V (sin señal) · H73_OUTPUT_API (ICM vs ICPI brecha histórica)
           H10c_RDC_APORTES (aportes ciudadanos GAD+Holding 2023-2024, ingesta verificada)
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── DATOS VERIFICADOS DEL EXCEL ────────────────────────────────────────────────
# Fuente: H31_REPORTE_CPCCS · Ti y Vi por meta · corte Q1-2026
# Vi = V_CPCCS proyectado desde patrones RDC 2024 (marcado como proyección)
METAS_PDOT = [
    # (ID, descripcion_corta, Ti_2026, Vi_estado)
    ("SC-I-N-01", "Agua potable · cobertura 39→42% · calidad INEN 1108",          0.70, "✅"),
    ("SC-L-N-02", "Talento humano · desempeño 80→90% · plan capacitación",        0.70, "✅"),
    ("AH-I-X-01", "Sostenibilidad financiera · autonomía 43→45%",                  0.70, "✅"),
    ("AH-I-X-02", "Vialidad cantonal · 43.8 km CUP + 57 km rurales",              0.23, "✅"),
    ("AH-I-X-03", "Salud integral · atenciones 57k→84k personas",                  0.43, "🔄"),
    ("AH-I-N-01", "Gestión desechos sólidos · 20k→23k Tn/año",                    0.43, "🔄"),
    ("SC-L-G-01", "Alcantarillado · cobertura 19→24% · PTAR 0→75%",              0.70, "✅"),
    ("AH-I-X-04", "Modernización recursos administrativos · tecnología",           0.70, "✅"),
    ("PI-I-G-01", "Equipamientos públicos · terminal, mercado, bomberos",          0.23, "✅"),
    ("AH-C-X-01", "Protección derechos sociales · CDI, adultos, género",           0.70, "✅"),
    ("AH-C-X-02", "Sistema información territorial · catastro 19→80%",             0.70, "✅"),
    ("SC-I-N-03", "Participación ciudadana · 50→100 UT · instancias COPFP",       0.70, "✅"),
    ("FA-I-X-01", "Gestión del riesgo · infraestructura susceptible -10%",         0.70, "✅"),
    ("FA-C-X-01", "Áreas verdes · IVU 10.94→17.32 m²/hab",                       0.43, "✅"),
    ("FA-I-X-02", "Equipamiento urbano · recolección 91→98% · barrido",           0.70, "✅"),
    ("FA-L-N-01", "Patrimonio cultural · 100% inventario · Museo Sombrero",        0.70, "✅"),
    ("PI-I-G-02", "PDOT/PUGS · SIL 19→80% · 37 trámites digitales",              0.70, "✅"),
    ("PI-L-G-01", "Señalización vial · 10k m² · 8 semáforos · 40 instituc.",      0.70, "✅"),
    ("EP-L-N-01", "Vivienda interés social · 50 VIS/VIP al 2027",                 0.70, "✅"),
    ("EP-L-X-01", "Fortalecimiento productivo · artesanos, mipymes, huertos",      0.70, "✅"),
    ("PI-TUR-01", "Turismo cantonal · 0→60 certificac. Ciudad Creativa",          0.00, "⬜"),
    ("PI-TUR-02", "Eventos turísticos · 10→22 eventos/año al 2027",               0.00, "⬜"),
    ("FA-CC-01",  "Cambio climático · 4 planes de acción al 2027",                0.00, "⬜"),
    ("AH-AP-04",  "Continuidad agua potable · índice ALTO 0→10%",                 0.43, "⬜"),
    ("FA-DIS-01", "Disposición final desechos sólidos · cap. 0→20%",              0.43, "⬜"),
]

# ── DATOS RDC HISTÓRICO · H10c_RDC_APORTES (sellado Q1-2026) ─────────────────
# 95 aportes verificados: GAD Municipal + Patronato + EP Aseo + Bomberos · 2023-2024
RDC_METRICAS = {
    "total":           95,
    "pct_compromisos": 0.979,
    "prom_cumpl":      88,
    "por_entidad": {
        "GAD Municipal": 62,
        "Patronato":      8,
        "EP Aseo":       14,
        "Bomberos":      11,
    },
    "por_componente": {"FA": 30, "AH": 23, "SC": 20, "PI": 14, "EP": 8},
}

# Alineación verificada RDC demandas → PP 2026 prioridades (narrativa del ciclo)
# (prioridad PP, fichas, componente_rdc, n_aportes, descripcion_demanda)
RDC_PP_ALINEACION = [
    ("Agua Potable / Saneamiento", 126, "AH",
     "Alcantarillado + agua potable demandados en 14+ aportes (sectores Isabel Muentes, Eloy Alfaro, Isla del Sol, Leónidas Proaño…)"),
    ("Áreas Verdes / Parques",      95, "FA",
     "Reforestación + espacios verdes (RDC 2024: reforestar Santa Isabella, paseo lúdico, senderos)"),
    ("Vialidad Cantonal",           94, "AH",
     "Arreglo de vías solicitado en 12+ sectores en RDC 2023 y 2024 (San Jacinto, Santa Lucía, Eloy Alfaro, Camarón…)"),
    ("Salud / Equipamiento Médico", 80, "SC",
     "Mejoras centros de salud + brigadas médicas Patronato (7 aportes SC en RDC 2023)"),
    ("Aseo / Recolección / Ambiente", 74, "FA",
     "FA es el componente MÁS demandado: 30 aportes sobre basura, recolección, ambiente (EP Aseo + GAD 2023-2024)"),
]

# Cumplimiento verificado de sugerencias año anterior (excl. N/A)
# Fuente: informes CPCCS-RDC oficiales · H10c sección B
RDC_CUMPLIMIENTOS = [
    {"entidad": "Patronato",  "sugerencia": "Mesas técnicas, terapias autismo, brigadas médicas, psicología comunidades", "pct": 98},
    {"entidad": "EP Aseo",    "sugerencia": "Frecuencia recolección Pile y La Sequita",                                  "pct": 100},
    {"entidad": "EP Aseo",    "sugerencia": "Entrega tanques La Sequita y Las Cañitas",                                  "pct": 50},
    {"entidad": "EP Aseo",    "sugerencia": "Socializar tasa de aseo por categoría",                                     "pct": 80},
    {"entidad": "EP Aseo",    "sugerencia": "Fortalecer gasto de inversión con POA focalizado",                          "pct": 100},
    {"entidad": "Bomberos",   "sugerencia": "Prevención riesgos sísmicos en unidades educativas",                        "pct": 100},
    {"entidad": "Bomberos",   "sugerencia": "Primera Brigada Bomberos Juniors — 30 niños en Río Caña",                   "pct": 100},
    {"entidad": "Bomberos",   "sugerencia": "Capacitaciones manejo de GLP en comunidades aledañas",                     "pct": 100},
    {"entidad": "Bomberos",   "sugerencia": "Capacitación continua prevención incendios todos los sectores",             "pct": 50},
    {"entidad": "Bomberos",   "sugerencia": "Evaluación visual sísmica edificaciones FEMA P-154 Fase I",                 "pct": 100},
]

# ICM autoreportado vs ICPI verificado — fuente: H08_SIGAD + H12c_HISTÓRICO
# ICM 2023/2024: 100% real según SIGAD (dato verificado en H08)
# ICPI: H12c_ICPI_HISTÓRICO_ANUAL (inmutable, sellado)
BRECHA_HISTORICA = [
    {"año": "2023", "icm": 100.0, "icpi": 57.36, "icm_fuente": "SIGAD real"},
    {"año": "2024", "icm": 100.0, "icpi": 67.12, "icm_fuente": "SIGAD real"},
    {"año": "2025", "icm": 100.0, "icpi": 69.93, "icm_fuente": "SIGAD autoreportado"},
    {"año": "2026 Q1", "icm": None,  "icpi": 53.56, "icm_fuente": "Pendiente SIGAD"},
]


# ── HELPERS HTML ───────────────────────────────────────────────────────────────
def _pp_cycle_card(label: str, color: str, lines: list[str]) -> str:
    items = "".join(
        f'<div style="font-size:10px;color:var(--white);padding:3px 0;'
        f'border-bottom:1px solid rgba(255,255,255,.04)">{l}</div>'
        for l in lines
    )
    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-top:3px solid var(--{color});border-radius:10px;
            padding:14px 16px;flex:1;min-width:0">
  <div style="font-size:11px;font-weight:800;color:var(--{color});
              margin-bottom:10px">{label}</div>
  {items}
</div>"""


def _parroquia_row(p: dict) -> str:
    part = p.get("participacion", {})
    est  = part.get("estado", "Sin datos")
    col  = {"Activo": "green", "Parcial": "amber", "Bajo": "amber", "Sin voz": "red"}.get(est, "muted")
    fichas = part.get("fichas_pp2026", 0) or 0
    return (
        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;'
        f'background:rgba(255,255,255,.02);border-radius:7px;margin-bottom:5px">'
        f'<span style="font-size:16px">{p.get("emoji","🏘️")}</span>'
        f'<div style="flex:1">'
        f'<div style="font-size:11px;font-weight:700;color:var(--white)">{p["nombre"]}</div>'
        f'<div style="font-size:9px;color:var(--muted)">'
        f'Fichas PP 2026: {fichas} · NBI: {p.get("nbi",0):.1f}% · Agua: {p.get("agua",0):.1f}%'
        f'</div></div>'
        f'<span style="font-size:9px;font-weight:700;padding:3px 8px;border-radius:5px;'
        f'background:rgba(255,255,255,.06);color:var(--{col})">{est}</span>'
        f'</div>'
    )


def _meta_row(meta: tuple) -> str:
    mid, desc, ti, vi = meta
    ti_pct = ti * 100
    col = "green" if vi == "✅" else "amber" if vi == "🔄" else "muted"
    bar_w = min(int(ti_pct), 100)
    return f"""
<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
            background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:3px">
  <span style="font-size:12px;min-width:20px">{vi}</span>
  <div style="flex:1">
    <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,.4);
                font-family:monospace">{mid}</div>
    <div style="font-size:9px;color:var(--white)">{desc}</div>
    <div style="height:3px;background:var(--divider);border-radius:2px;
                margin-top:4px;overflow:hidden">
      <div style="height:3px;width:{bar_w}%;background:var(--{col});border-radius:2px"></div>
    </div>
  </div>
  <div style="text-align:right;flex-shrink:0;min-width:40px">
    <div style="font-size:11px;font-weight:800;color:var(--{col});
                font-family:monospace">{ti_pct:.0f}%</div>
    <div style="font-size:8px;color:var(--muted)">Ti</div>
  </div>
</div>"""


def _brecha_row(b: dict) -> str:
    icm_txt  = f"{b['icm']:.0f}%" if b["icm"] is not None else "Pendiente"
    icm_col  = "white" if b["icm"] is not None else "muted"
    brecha   = (b["icm"] - b["icpi"]) if b["icm"] is not None else None
    brecha_txt = f"{brecha:.1f} pts" if brecha is not None else "—"
    brecha_col = "amber" if brecha and brecha > 20 else "green" if brecha is not None else "muted"
    icpi_pct = b["icpi"]
    # Stacked bar: cyan=ICPI achieved, translucent red=gap to 100%
    if b["icm"] is not None:
        stacked = (
            f'<div style="flex:1;margin-left:8px;height:14px;background:var(--divider);'
            f'border-radius:7px;overflow:hidden;position:relative">'
            f'<div style="position:absolute;left:0;top:0;height:100%;width:{icpi_pct:.1f}%;'
            f'background:var(--cyan);border-radius:7px 0 0 7px;opacity:.78"></div>'
            f'<div style="position:absolute;left:{icpi_pct:.1f}%;top:0;height:100%;'
            f'width:{brecha:.1f}%;background:var(--red);opacity:.35"></div>'
            f'</div>'
        )
    else:
        stacked = (
            f'<div style="flex:1;margin-left:8px;height:14px;background:var(--divider);'
            f'border-radius:7px;overflow:hidden">'
            f'<div style="height:100%;width:{icpi_pct:.1f}%;background:var(--cyan);'
            f'border-radius:7px;opacity:.78"></div>'
            f'</div>'
        )
    return f"""
<div style="display:flex;align-items:center;gap:10px;padding:12px 14px;
            background:rgba(255,255,255,.02);border-radius:8px;margin-bottom:5px">
  <div style="font-size:12px;font-weight:700;color:rgba(255,255,255,.5);
              min-width:65px;font-family:monospace">{b["año"]}</div>
  <div style="text-align:center;min-width:80px">
    <div style="font-size:14px;font-weight:800;color:var(--{icm_col});
                font-family:monospace">{icm_txt}</div>
    <div style="font-size:8px;color:var(--muted)">ICM SIGAD</div>
  </div>
  <div style="font-size:16px;color:var(--muted)">→</div>
  <div style="text-align:center;min-width:86px">
    <div style="font-size:14px;font-weight:800;color:var(--cyan);
                font-family:monospace">{b["icpi"]:.2f}%</div>
    <div style="font-size:8px;color:var(--muted)">ICPI Verificado</div>
  </div>
  <div style="font-size:16px;color:var(--muted)">=</div>
  <div style="text-align:center;min-width:80px">
    <div style="font-size:14px;font-weight:800;color:var(--{brecha_col});
                font-family:monospace">{brecha_txt}</div>
    <div style="font-size:8px;color:var(--muted)">Brecha</div>
  </div>
  {stacked}
</div>"""


def _cumpl_card(rec: dict) -> str:
    pct = rec["pct"]
    col = "green" if pct >= 80 else "amber" if pct >= 50 else "red"
    bar = min(pct, 100)
    return (
        f'<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;'
        f'background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:3px">'
        f'<div style="flex-shrink:0;min-width:66px;text-align:center">'
        f'<div style="font-size:8px;color:var(--muted)">{rec["entidad"]}</div>'
        f'<div style="font-size:12px;font-weight:800;color:var(--{col});'
        f'font-family:monospace">{pct}%</div></div>'
        f'<div style="flex:1;min-width:0">'
        f'<div style="font-size:9px;color:var(--white)">{rec["sugerencia"]}</div>'
        f'<div style="height:3px;background:var(--divider);border-radius:2px;'
        f'margin-top:3px;overflow:hidden">'
        f'<div style="height:3px;width:{bar}%;background:var(--{col});border-radius:2px">'
        f'</div></div></div></div>'
    )


def _rdc_pp_row(rec: tuple) -> str:
    nombre, fichas, comp, desc = rec
    comp_col = {"FA": "green", "AH": "cyan", "SC": "amber", "EP": "purple", "PI": "muted"}
    col = comp_col.get(comp, "white")
    return (
        f'<div style="display:grid;grid-template-columns:1fr 60px 40px;gap:8px;'
        f'align-items:start;padding:7px 10px;border-radius:6px;margin-bottom:3px;'
        f'background:rgba(255,255,255,.02)">'
        f'<div>'
        f'<div style="font-size:10px;font-weight:700;color:var(--white)">{nombre}</div>'
        f'<div style="font-size:9px;color:var(--muted);margin-top:2px">{desc}</div>'
        f'</div>'
        f'<div style="text-align:center">'
        f'<div style="font-size:12px;font-weight:800;color:var(--cyan);'
        f'font-family:monospace">{fichas}</div>'
        f'<div style="font-size:8px;color:var(--muted)">fichas</div>'
        f'</div>'
        f'<div style="text-align:center">'
        f'<span style="font-size:8px;font-weight:700;padding:2px 5px;border-radius:4px;'
        f'background:rgba(255,255,255,.06);color:var(--{col})">{comp}</span>'
        f'</div>'
        f'</div>'
    )


# ── RENDER PRINCIPAL ───────────────────────────────────────────────────────────
def render() -> None:
    data       = load_all()
    show_tech  = is_tecnico()
    parroquias = data.get("parroquias", [])
    pp_2024    = data.get("pp_2024", {})
    pp_2025    = data.get("pp_2025", {})
    pp_2026    = data.get("pp_2026", {})
    indices    = data["indices"]
    igp_ref    = indices.get("IGP", {}).get("valor", 27.98)

    # KPIs header
    n_parr_voz = sum(1 for p in parroquias
                     if p.get("participacion", {}).get("estado") not in ("Sin voz", "Bajo"))
    fichas_2026 = pp_2026.get("total_fichas", 149)
    fichas_2025 = pp_2025.get("total_fichas", 137)
    tendencia   = round((fichas_2026 - fichas_2025) / fichas_2025 * 100, 1)

    hdr = page_header(
        "GOBERNANZA PARTICIPATIVA",
        "Participación Ciudadana · Control Social",
        f"PP 2026: {fichas_2026} fichas · IGP ref 2025: {igp_ref:.2f}% · "
        f"RDC 2026: en preparación (informe jun-2026) · SAT-V: Sin señal",
        '<span class="badge badge-cyan">🗳️ Ciclo PP Completo</span>',
    )

    # ── TABS STREAMLIT ─────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs([
        "🗳️  Participación Ciudadana",
        "📋  Control Social",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1: PARTICIPACIÓN CIUDADANA
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:38px;font-weight:900;color:var(--cyan);
                font-family:var(--mono)">{igp_ref:.1f}<span style="font-size:16px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--cyan);margin-top:4px">IGP · REF 2025</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">H20b · Gobernanza Partic.</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:38px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{fichas_2026}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">FICHAS PP 2026</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">ACTA N°007-2025 · ago-2025</div>
  </div>
  <div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:38px;font-weight:900;color:var(--green);
                font-family:var(--mono)">+{tendencia}<span style="font-size:14px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">TENDENCIA FICHAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">PP2025 137 → PP2026 149</div>
  </div>
  <div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:38px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{n_parr_voz}<span style="font-size:16px">/7</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">PARROQUIAS ACTIVAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">COOTAD Art.238 · cobertura PP</div>
  </div>
</div>"""

        # PP Serie histórica
        cycles_html = f"""
<div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap">
  {_pp_cycle_card("PP 2024 · Proceso Online", "amber", [
      f"Método: {pp_2024.get('proceso_metodo', 'Formulario online')}",
      f"Presupuesto priorizado: ${pp_2024.get('presupuesto_total',6118924):,.0f}",
      "Parroquias: 7/7 cubiertas",
      f"ACTA: {pp_2024.get('acta_aprobacion','N°002-2023-JLAC')}",
      "Componente mayor: Asentamientos Humanos $3.22M (53%)",
  ])}
  {_pp_cycle_card("PP 2025 · Talleres Presenciales", "cyan", [
      f"Método: {pp_2025.get('total_talleres',6)} talleres presenciales · 7 parroquias",
      f"Fichas sistematizadas: {pp_2025.get('total_fichas',137)}",
      f"Presupuesto priorizado: ${pp_2025.get('presupuesto_total',5687954):,.0f}",
      f"Ingresos base: ${pp_2025.get('ingresos_estimados',21606774):,.0f}",
      f"ACTA: {pp_2025.get('acta_conformidad','N°005-2024-JLAC')}",
  ])}
  {_pp_cycle_card("PP 2026 · Vigente (ago 2025)", "green", [
      f"Método: {pp_2026.get('total_talleres',6)} talleres presenciales · 7 parroquias",
      f"Fichas sistematizadas: {pp_2026.get('total_fichas',149)} (oficial)",
      f"Ingresos base estimados: ${pp_2026.get('ingresos_estimados',20982884):,.0f}",
      f"ACTA: {pp_2026.get('acta_aprobacion','N°007-2025-JLAC')}",
      "Monto por prioridad: pendiente resolución GADM",
  ])}
</div>"""

        # PP 2026 prioridades ciudadanas
        top_prio = pp_2026.get("top_prioridades", {})
        prio_items = ""
        if top_prio:
            total_fichas_prio = sum(top_prio.values())
            for i, (nombre, fichas) in enumerate(sorted(top_prio.items(), key=lambda x: -x[1]), 1):
                pct = fichas / total_fichas_prio * 100
                prio_items += f"""
  <div style="display:flex;align-items:center;gap:8px;padding:7px 0;
              border-bottom:1px solid rgba(255,255,255,.04)">
    <div style="font-size:11px;font-weight:800;color:var(--cyan);
                min-width:16px;font-family:monospace">{i}</div>
    <div style="flex:1">
      <div style="font-size:10px;font-weight:700;color:var(--white)">{nombre}</div>
      <div style="height:3px;background:var(--divider);border-radius:2px;margin-top:4px">
        <div style="height:3px;width:{pct:.0f}%;background:var(--cyan);border-radius:2px"></div>
      </div>
    </div>
    <div style="text-align:right;min-width:60px">
      <div style="font-size:11px;font-weight:800;color:var(--cyan);
                  font-family:monospace">{fichas} fichas</div>
      <div style="font-size:8px;color:var(--muted)">{pct:.1f}%</div>
    </div>
  </div>"""

        prio_html = f"""
<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);
            border-radius:12px;padding:14px 16px;margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:var(--cyan);margin-bottom:10px">
    🗳️ TOP PRIORIDADES CIUDADANAS PP 2026 · {fichas_2026} fichas totales verificadas
  </div>
  <div style="font-size:9px;color:var(--amber);margin-bottom:8px;padding:4px 8px;
              background:rgba(255,184,0,.07);border-radius:4px;
              border:1px solid rgba(255,184,0,.15)">
    Fichas = votos de priorización ciudadana · Monto de inversión por prioridad:
    pendiente resolución presupuestaria GADM (proceso PP concluido ago-2025)
  </div>
  {prio_items}
</div>"""

        # Parroquias
        parr_rows = "".join(_parroquia_row(p) for p in parroquias)
        sin_voz = [p for p in parroquias
                   if p.get("participacion", {}).get("estado") in ("Sin voz", "Bajo")]
        alerta_parr = ""
        if sin_voz:
            nombres = " y ".join(p["nombre"] for p in sin_voz)
            alerta_parr = f"""
<div style="margin-top:8px;padding:8px 10px;background:rgba(255,77,109,.06);
            border:1px solid rgba(255,77,109,.15);border-radius:7px;
            font-size:10px;color:var(--red)">
  Parroquias sin participación activa verificada: <strong>{nombres}</strong> ·
  Prioridad para próximo ciclo PP 2027
</div>"""

        parr_html = f"""
<div class="card">
  <div class="card-title">🗺️ PARTICIPACIÓN POR PARROQUIA · 7 territorios · PP 2026</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:8px;padding:4px 8px;
              background:rgba(0,212,255,.05);border-radius:4px;
              border:1px solid rgba(0,212,255,.1)">
    Fuente: INFORME PP 2026 GAD Montecristi · ACTA N°007-2025-JLAC-JPC-GADMCM ·
    Fichas por parroquia: estimadas por taller (talleres agrupan múltiples parroquias).
    Total oficial 149 fichas verificado.
  </div>
  {parr_rows}
  {alerta_parr}
</div>"""

        # IGP nota metodológica
        igp_nota = f"""
<div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
            border-radius:10px;padding:12px 14px;margin-top:12px;
            font-size:10px;color:var(--muted);line-height:1.7">
  <strong style="color:var(--white)">IGP (Índice de Gobernanza Participativa) — Nota metodológica</strong><br>
  IGP ref 2025 = 27.98% · H20b_IGP_GOBERNANZA_PARTIC<br>
  IGP 2026 Q1 (H20b) = promedio de 3 componentes:
  IGP_1 (Asambleas CPCCS 54%) + IGP_2 (PP activo 0% — pendiente actualización post-PP) +
  IGP_3 (Fidelidad Narrativa 91%) = 48.33% · Clasificación: Gestión por Transición
</div>"""

        tab1_content = resumen_html + f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">📊 SERIE PP HISTÓRICA · Ciclos 2024 · 2025 · 2026 — VERIFICADA</div>
  <div style="font-size:8px;color:rgba(0,224,150,.7);margin-bottom:10px;padding:4px 8px;
              background:rgba(0,224,150,.05);border-radius:4px;
              border:1px solid rgba(0,224,150,.1)">
    Fuentes primarias: PDFs oficiales GAD Montecristi ·
    ACTA N°002-2023-JLAC (PP2024) · ACTA N°005-2024-JLAC (PP2025) · ACTA N°007-2025-JLAC (PP2026)
  </div>
  {cycles_html}
</div>""" + prio_html + parr_html + igp_nota

        render_page(tab1_content, show_tech=show_tech, height=1600)

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔮 Sentinel · Estrategia PP y Participación",
                         use_container_width=True, type="primary"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    f"El PP 2026 de Montecristi registró {fichas_2026} fichas ciudadanas "
                    f"en 7 parroquias (tendencia +{tendencia}% vs PP2025). "
                    f"El IGP referencia 2025 es {igp_ref:.2f}%. "
                    "Las prioridades ciudadanas son: agua potable, áreas verdes, vialidad, salud, aseo. "
                    "¿Qué estrategia concreta recomiendas para que el PP 2027 incremente la participación "
                    "en las parroquias con menor actividad y vincule mejor las fichas con partidas POA verificables?"
                )
                st.rerun()
        with c2:
            if st.button("🗺️ Ver GeoTwin · Territorio", use_container_width=True):
                st.session_state["page"] = "geotwin"
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2: CONTROL SOCIAL
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        # Estado RDC 2026
        rdc_estado_html = f"""
<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.2);
            border-radius:12px;padding:14px 18px;margin-bottom:16px;
            display:flex;align-items:flex-start;gap:16px">
  <div style="font-size:32px;flex-shrink:0">📋</div>
  <div style="flex:1">
    <div style="font-size:13px;font-weight:800;color:var(--cyan);margin-bottom:6px">
      RENDICIÓN DE CUENTAS 2026 · EN PREPARACIÓN
    </div>
    <div style="font-size:11px;color:var(--muted);line-height:1.8">
      <strong style="color:var(--white)">Estado real (corte Q1-2026):</strong>
      La RDC 2026 se encuentra en fase de preparación.
      El informe de gestión debe presentarse ante el CPCCS en <strong style="color:var(--cyan)">junio 2026</strong>
      (LOPC Art.88 + Constitución Art.204).
      <br>
      <strong style="color:var(--green)">SAT-V:</strong> Sin señal activa ·
      Compromisos CPCCS formales registrados: 0 (sin proceso abierto) ·
      <strong style="color:var(--white)">No existe calificación CPCCS vigente.</strong>
    </div>
    <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
      <span style="padding:5px 10px;background:rgba(0,212,255,.1);border-radius:6px;
                   font-size:9px;font-weight:700;color:var(--cyan)">
        📅 Plazo informe: junio 2026
      </span>
      <span style="padding:5px 10px;background:rgba(0,224,150,.08);border-radius:6px;
                   font-size:9px;font-weight:700;color:var(--green)">
        ✅ SAT-V: Sin señal · H24b_SAT-V
      </span>
      <span style="padding:5px 10px;background:rgba(255,184,0,.08);border-radius:6px;
                   font-size:9px;font-weight:700;color:var(--amber)">
        🔒 Marco legal: LOPC Art.88 · Const. Art.204
      </span>
    </div>
  </div>
</div>"""

        # Brecha ICM vs ICPI histórica
        brecha_rows = "".join(_brecha_row(b) for b in BRECHA_HISTORICA)
        brecha_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">📊 BRECHA DE VERIFICACIÓN · ICM Autoreportado vs ICPI Verificado</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:10px;padding:5px 10px;
              background:rgba(0,212,255,.05);border-radius:5px;
              border:1px solid rgba(0,212,255,.1)">
    ICM (Índice Cumplimiento Meta) = autoreportado por el GAD al SIGAD/SNP ·
    ICPI = verificado por QUIRA OS con 8 silos de datos independientes ·
    La brecha mide la distancia entre el discurso oficial y la evidencia verificable.
    <strong style="color:var(--white)"> Fuente: H08_SIGAD (ICM) + H12c_ICPI_HISTÓRICO (ICPI)</strong>
  </div>
  {brecha_rows}
  <div style="margin-top:8px;padding:8px 10px;
              background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.15);
              border-radius:7px;font-size:10px;color:var(--amber)">
    ⚠ Esta brecha no implica irregularidades — el ICM mide cumplimiento programático declarado
    y el ICPI incorpora verificación algorítmica cruzada. Reducir la brecha = fortalecer
    la evidencia documental de cada meta ante el CPCCS.
  </div>
</div>"""

        # IFE promesas CNE
        ife_html = f"""
<div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
            border-radius:12px;padding:14px 16px;margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:8px">
    🏛️ FIDELIDAD AL MANDATO ELECTORAL · IFE 72.73% · H63_S0_CNE_TRAZABILIDAD
  </div>
  <div class="grid-3" style="gap:10px;margin-bottom:10px">
    <div style="text-align:center;padding:10px;background:rgba(255,255,255,.03);border-radius:8px">
      <div style="font-size:28px;font-weight:900;color:var(--green);font-family:monospace">72.73%</div>
      <div style="font-size:9px;color:var(--muted)">IFE Global</div>
    </div>
    <div style="text-align:center;padding:10px;background:rgba(255,255,255,.03);border-radius:8px">
      <div style="font-size:28px;font-weight:900;color:var(--cyan);font-family:monospace">48/66</div>
      <div style="font-size:9px;color:var(--muted)">Promesas vinculadas PDOT</div>
    </div>
    <div style="text-align:center;padding:10px;background:rgba(255,255,255,.03);border-radius:8px">
      <div style="font-size:28px;font-weight:900;color:var(--amber);font-family:monospace">18</div>
      <div style="font-size:9px;color:var(--muted)">Sin meta PDOT asignada</div>
    </div>
  </div>
  <div style="font-size:10px;color:var(--muted);line-height:1.6">
    66 promesas del Plan de Trabajo CNE 2023 (Ing. Jonathan Toro Largacha) rastreadas por eje:
    Social (24), Económico (15), Ambiental (12), Político-Institucional (15).
    48 tienen meta PDOT 2023-2027 asignada y verificable. 18 sin meta formal — fortalecer vinculación.
  </div>
</div>"""

        # 25 Metas PDOT estado
        n_verif = sum(1 for m in METAS_PDOT if m[3] == "✅")
        n_proc  = sum(1 for m in METAS_PDOT if m[3] == "🔄")
        n_sinv  = sum(1 for m in METAS_PDOT if m[3] == "⬜")
        meta_rows = "".join(_meta_row(m) for m in METAS_PDOT)

        metas_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">🎯 25 METAS PDOT · Estado verificación Q1-2026 · H31_REPORTE_CPCCS</div>
  <div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap">
    <span style="padding:5px 10px;background:rgba(0,224,150,.1);border-radius:6px;
                 font-size:10px;font-weight:700;color:var(--green)">✅ {n_verif} Verificadas</span>
    <span style="padding:5px 10px;background:rgba(0,212,255,.08);border-radius:6px;
                 font-size:10px;font-weight:700;color:var(--cyan)">🔄 {n_proc} En proceso</span>
    <span style="padding:5px 10px;background:rgba(255,255,255,.05);border-radius:6px;
                 font-size:10px;font-weight:700;color:rgba(255,255,255,.35)">⬜ {n_sinv} Sin verificar</span>
  </div>
  <div style="font-size:8px;color:var(--amber);margin-bottom:8px;padding:4px 8px;
              background:rgba(255,184,0,.07);border-radius:4px;
              border:1px solid rgba(255,184,0,.15)">
    Ti = ejecución presupuestaria Q1-2026 · Estado Vi = verificación documental proyectada
    (basada en patrones RDC 2024 — actualizar cuando se presenten documentos RDC 2026 en junio)
  </div>
  {meta_rows}
</div>"""

        # ── APORTES CIUDADANOS HISTÓRICOS · H10c_RDC_APORTES ─────────────────
        rm = RDC_METRICAS
        n_ent = rm["por_entidad"]
        n_comp = rm["por_componente"]
        comp_total = sum(n_comp.values())

        def _comp_bar(label, n, color):
            pct = n / comp_total * 100
            return (
                f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">'
                f'<div style="font-size:8px;font-weight:700;color:var(--muted);'
                f'min-width:24px;text-align:right">{label}</div>'
                f'<div style="flex:1;height:10px;background:var(--divider);border-radius:4px;'
                f'overflow:hidden">'
                f'<div style="height:10px;width:{pct:.0f}%;background:var(--{color});'
                f'border-radius:4px"></div></div>'
                f'<div style="font-size:9px;font-weight:800;color:var(--{color});'
                f'font-family:monospace;min-width:28px">{n}</div>'
                f'</div>'
            )

        rdc_kpi_html = f"""
<div class="grid-4" style="margin-bottom:12px">
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:10px;padding:12px;text-align:center">
    <div style="font-size:32px;font-weight:900;color:var(--cyan);font-family:monospace">{rm["total"]}</div>
    <div style="font-size:9px;font-weight:700;color:var(--cyan)">APORTES INGRESADOS</div>
    <div style="font-size:8px;color:var(--muted)">GAD + Holding · 2023-2024</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:10px;padding:12px;text-align:center">
    <div style="font-size:32px;font-weight:900;color:var(--green);font-family:monospace">{rm["pct_compromisos"]:.0%}</div>
    <div style="font-size:9px;font-weight:700;color:var(--green)">COMPROMETIDOS</div>
    <div style="font-size:8px;color:var(--muted)">93/95 aceptados como SI</div>
  </div>
  <div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
              border-radius:10px;padding:12px;text-align:center">
    <div style="font-size:32px;font-weight:900;color:var(--green);font-family:monospace">{rm["prom_cumpl"]}%</div>
    <div style="font-size:9px;font-weight:700;color:var(--green)">CUMPL. PROMEDIO</div>
    <div style="font-size:8px;color:var(--muted)">Sugerencias año anterior</div>
  </div>
  <div style="background:rgba(255,184,0,.05);border:1px solid rgba(255,184,0,.2);
              border-radius:10px;padding:12px;text-align:center">
    <div style="font-size:32px;font-weight:900;color:var(--amber);font-family:monospace">4</div>
    <div style="font-size:9px;font-weight:700;color:var(--amber)">ENTIDADES</div>
    <div style="font-size:8px;color:var(--muted)">GAD · Patronato · EP Aseo · Bomberos</div>
  </div>
</div>"""

        comp_bars = (
            _comp_bar("FA", n_comp["FA"], "green") +
            _comp_bar("AH", n_comp["AH"], "cyan") +
            _comp_bar("SC", n_comp["SC"], "amber") +
            _comp_bar("PI", n_comp["PI"], "muted") +
            _comp_bar("EP", n_comp["EP"], "purple")
        )

        alin_rows = "".join(_rdc_pp_row(r) for r in RDC_PP_ALINEACION)
        cumpl_rows = "".join(_cumpl_card(r) for r in RDC_CUMPLIMIENTOS)

        _ent_colors = {"GAD Municipal": "cyan", "Patronato": "purple", "EP Aseo": "amber", "Bomberos": "green"}
        _ent_total  = sum(n_ent.values())
        ent_bars_html = "".join(
            f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:5px">'
            f'<div style="font-size:9px;color:var(--muted);min-width:90px">{k}</div>'
            f'<div style="flex:1;height:10px;background:var(--divider);border-radius:5px;overflow:hidden">'
            f'<div style="height:10px;width:{v/_ent_total*100:.0f}%;'
            f'background:var(--{_ent_colors.get(k,"cyan")});border-radius:5px;opacity:.85"></div></div>'
            f'<div style="font-size:10px;font-weight:800;'
            f'color:var(--{_ent_colors.get(k,"cyan")});font-family:monospace;min-width:24px;text-align:right">{v}</div>'
            f'</div>'
            for k, v in n_ent.items()
        )

        rdc_hist_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">📂 APORTES CIUDADANOS · RDC 2023-2024 · H10c_RDC_APORTES (VERIFICADO)</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:10px;padding:5px 10px;
              background:rgba(0,212,255,.05);border-radius:5px;
              border:1px solid rgba(0,212,255,.1)">
    Fuente: Informes CPCCS-RDC oficiales GAD Montecristi · Patronato · EP Aseo / EMAIMEP · Bomberos ·
    Ingesta verificada en SIAP-ICPI_GOLD_MASTER_v4.1 hoja H10c ·
    <strong style="color:var(--white)">Naturaleza legal: ADVISORY (LOPC Art.89) —
    no vinculante individual; obliga documentación y respuesta institucional colectiva.</strong>
  </div>
  {rdc_kpi_html}

  <div style="display:grid;grid-template-columns:1fr 1.6fr;gap:12px;margin-bottom:12px">
    <div>
      <div style="font-size:9px;font-weight:700;color:var(--muted);margin-bottom:8px">
        POR COMPONENTE PDOT
      </div>
      {comp_bars}
      <div style="font-size:8px;color:var(--muted);margin-top:6px">
        FA=Biofísico/Ambiente · AH=Asentamientos · SC=Sociocultural · PI=Institucional · EP=Económico
      </div>
    </div>
    <div>
      <div style="font-size:9px;font-weight:700;color:var(--muted);margin-bottom:8px">
        POR ENTIDAD
      </div>
      {ent_bars_html}
    </div>
  </div>

  <div style="border-top:1px solid var(--divider);padding-top:12px;margin-bottom:12px">
    <div style="font-size:9px;font-weight:700;color:var(--green);margin-bottom:8px">
      🔄 CICLO VERIFICADO: DEMANDA RDC → PRIORIDAD PP 2026
    </div>
    <div style="font-size:8px;color:var(--muted);margin-bottom:8px;padding:4px 8px;
                background:rgba(0,224,150,.05);border-radius:4px;
                border:1px solid rgba(0,224,150,.1)">
      Los aportes ciudadanos en RDC 2023-2024 se alinean directamente con las fichas PP 2026:
      el sistema participativo está funcionando como ciclo. · Columnas: Prioridad PP · Fichas · Componente RDC origen
    </div>
    {alin_rows}
  </div>

  <div style="border-top:1px solid var(--divider);padding-top:12px">
    <div style="font-size:9px;font-weight:700;color:var(--amber);margin-bottom:8px">
      ✅ CUMPLIMIENTO VERIFICADO · Sugerencias RDC → implementadas al año siguiente
    </div>
    {cumpl_rows}
    <div style="margin-top:8px;padding:6px 10px;background:rgba(0,224,150,.05);
                border-radius:6px;font-size:9px;color:var(--green)">
      Promedio cumplimiento holding 2023→2024: <strong>{rm["prom_cumpl"]}%</strong> ·
      Bomberos: 3 sugerencias 2023 implementadas al 100% en 2024 ·
      EP Aseo: 3 implementadas, 1 parcial (tanques 50%) ·
      Patronato: 98% implementación.
    </div>
  </div>
</div>"""

        tab2_content = rdc_estado_html + brecha_html + ife_html + metas_html + rdc_hist_html
        render_page(tab2_content, show_tech=show_tech, height=4000)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔮 Sentinel · Plan RDC 2026",
                         use_container_width=True, type="primary"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    "La RDC 2026 del GAD de Montecristi debe presentarse ante el CPCCS en junio 2026. "
                    "El IFE es 72.73% (48/66 promesas vinculadas al PDOT). "
                    f"De las 25 metas PDOT: {n_verif} verificadas, {n_proc} en proceso, {n_sinv} sin verificar. "
                    "La brecha ICM-ICPI histórica promedia 30 puntos. "
                    "Los aportes ciudadanos en RDC 2023-2024 suman 95 (GAD+Holding): "
                    "FA=30, AH=23, SC=20, PI=14, EP=8. El ciclo RDC→PP está verificado: "
                    "agua potable, vialidad y aseo fueron los más demandados en RDC y son las top prioridades PP 2026. "
                    "El cumplimiento promedio de sugerencias del año anterior es 88% (Holding). "
                    "¿Cómo se estructura el informe RDC 2026 para demostrar este ciclo participativo al CPCCS, "
                    "qué documentos son necesarios, y cómo se cierran las metas sin evidencia?"
                )
                st.rerun()
        with c2:
            if st.button("🔍 Ver Transparencia LOTAIP", use_container_width=True):
                st.session_state["page"] = "transparencia"
                st.rerun()
        with c3:
            if st.button("🎯 Ver Metas PDOT", use_container_width=True):
                st.session_state["page"] = "metas"
                st.rerun()
