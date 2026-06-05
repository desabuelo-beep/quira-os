"""
QUIRA OS v0.1 — P-19 Género y Equidad + Ambiente
Tab 1 💜 Género: PSG 12.83% · ODS 5 · Gender Bond · Pin Morado · Plan género · Panel IGM 6 sub-ind.
Tab 2 🌿 Ambiente: 6 metas FA PDOT · alineación PP 2026 · RDC aportes FA (30 = más demandado)
FUENTE ÚNICA DE DATOS: SIAP-ICPI_GOLD_MASTER_v4.1 (H73_OUTPUT_API + H99_ENGINE_CORE + H10c_RDC)
Indicadores sin fuente Excel marcados con valor=None → "Sin dato oficial"
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico, is_ejecutivo
from quira_pages.html_engine import render_page, page_header

# ── PANEL IGM · 6 SUB-INDICADORES DE GÉNERO ──────────────────────────────────
# valor=None  → dato NO disponible en Excel · se muestra como "Sin dato oficial"
# valor=float → dato derivable del Gold Master (IGM-D y IGM-E son estados binarios)
INDICADORES_GENERO = [
    {
        "codigo": "IGM-A",
        "nombre": "Mujeres en cargos directivos GAD",
        "icon":   "👩‍💼",
        "valor":  None,          # NO en Excel · pendiente certificación RRHH
        "meta":   40.0,
        "unidad": "%",
        "estado": "ALERTA",
        "color":  "amber",
        "nota":   "Meta PDOT 40% para 2027 · ODS 5.5 · Pendiente certificación oficial RRHH",
    },
    {
        "codigo": "IGM-B",
        "nombre": "Brecha salarial mujeres/hombres (GAD)",
        "icon":   "💰",
        "valor":  None,          # NO en Excel · pendiente análisis nómina oficial
        "meta":   0.0,
        "unidad": "% diferencia",
        "estado": "PARCIAL",
        "color":  "amber",
        "nota":   "ODS 8.5 · Meta: paridad salarial certificada · Pendiente análisis nómina DAF",
    },
    {
        "codigo": "IGM-C",
        "nombre": "Carga acarreo agua · mujeres rurales",
        "icon":   "💧",
        "valor":  None,          # NO en Excel · pendiente encuesta PNUD / INEC
        "meta":   0.0,
        "unidad": "% del acarreo",
        "estado": "CRÍTICO",
        "color":  "red",
        "nota":   "Isabel Muentes + Colorado · cobertura agua 1.02% · Pendiente encuesta PNUD/INEC",
    },
    {
        "codigo": "IGM-D",
        "nombre": "Luminarias seguridad · Pin Morado activo",
        "icon":   "💡",
        "valor":  0.0,           # FUENTE: PSG=12.83%<30% (H73_OUTPUT_API) → proyecto BLOQUEADO
        "meta":   100.0,
        "unidad": "% avance",
        "estado": "BLOQUEADO",
        "color":  "red",
        "nota":   "Aníbal San Andrés · Gov Twin aprobado · BLOQUEADO: PSG 12.83% < umbral 30% · Fuente: H73",
    },
    {
        "codigo": "IGM-E",
        "nombre": "Plan Género municipal aprobado",
        "icon":   "📋",
        "valor":  0.0,           # BINARIO: plan no aprobado = 0% (estado documentado en PDOT)
        "meta":   100.0,
        "unidad": "% aprobación",
        "estado": "PENDIENTE",
        "color":  "red",
        "nota":   "Requisito ONU Mujeres · Patronato debe designar coordinadora género · Estado: no aprobado",
    },
    {
        "codigo": "IGM-F",
        "nombre": "ODS 5.5 · Representación política femenina",
        "icon":   "🏛️",
        "valor":  None,          # NO en Excel · requiere fuente CNE/AME oficial
        "meta":   50.0,
        "unidad": "%",
        "estado": "PARCIAL",
        "color":  "amber",
        "nota":   "Concejo Municipal Q1-2026 · Meta paridad 2027 · Pendiente certificación CNE/AME",
    },
]

# ODS 5 sub-metas · avance=None: sin medición oficial en Excel
# Estado cualitativo derivado del PDOT / PSG / contexto GAD
ODS5_TARGETS = [
    {"id": "5.1", "desc": "Fin a discriminación legal de género",    "avance": None, "estado": "PARCIAL"},
    {"id": "5.2", "desc": "Violencia doméstica · protocolos activos","avance": None, "estado": "ALERTA"},
    {"id": "5.4", "desc": "Reconocimiento cuidados no remunerados",  "avance": None, "estado": "CRÍTICO"},
    {"id": "5.5", "desc": "Liderazgo político y económico femenino", "avance": None, "estado": "PARCIAL"},
    {"id": "5.a", "desc": "Igualdad derechos económicos / catastro", "avance": None, "estado": "PARCIAL"},
    {"id": "5.c", "desc": "Políticas y legislación género · PSG",    "avance": None, "estado": "CRÍTICO"},
]


def _igm_card(ind: dict) -> str:
    """Renderiza tarjeta IGM. valor=None → sin dato oficial (no inventado)."""
    col   = ind["color"]
    valor = ind["valor"]  # puede ser None
    estado_map = {
        "CRÍTICO":   '<span class="badge badge-red">🔴 CRÍTICO</span>',
        "BLOQUEADO": '<span class="badge badge-red">🔴 BLOQUEADO</span>',
        "ALERTA":    '<span class="badge badge-amber">🟠 ALERTA</span>',
        "PARCIAL":   '<span class="badge badge-amber">🟡 PARCIAL</span>',
        "PENDIENTE": '<span class="badge badge-red">⬜ PENDIENTE</span>',
        "OK":        '<span class="badge badge-green">✅ OK</span>',
    }
    badge = estado_map.get(ind["estado"], "")

    # Bloque valor: si hay dato → número; si no → etiqueta "Sin dato oficial"
    if valor is not None:
        valor_html = (
            f'<div style="font-size:18px;font-weight:900;color:var(--{col});'
            f'font-family:var(--mono)">{valor:.1f}'
            f'<span style="font-size:10px">{ind["unidad"]}</span></div>'
        )
        meta_html = (
            f'<div style="font-size:9px;color:var(--muted)">Meta: {ind["meta"]:.0f}{ind["unidad"]}</div>'
            if ind["meta"] > 0
            else '<div style="font-size:9px;color:var(--red)">Meta: 0 (eliminar)</div>'
        )
        # Barra de progreso solo si hay valor numérico
        invert_bar = ind["meta"] == 0.0
        bar_color  = col if not invert_bar else ("red" if valor > 30 else "amber")
        pct_bar    = min(valor / ind["meta"] * 100, 100) if ind["meta"] > 0 else 100
        bar_html   = (
            f'<div style="height:4px;background:var(--divider);border-radius:2px;'
            f'overflow:hidden;margin-bottom:5px">'
            f'<div style="height:4px;width:{pct_bar:.0f}%;background:var(--{bar_color});'
            f'border-radius:2px"></div></div>'
        ) if ind["meta"] > 0 else ""
    else:
        # Sin dato oficial → no inventar
        valor_html = (
            '<div style="font-size:12px;font-weight:700;color:rgba(255,255,255,.35);'
            'font-family:var(--mono);padding:2px 7px;background:rgba(255,255,255,.05);'
            'border-radius:5px;border:1px solid rgba(255,255,255,.1)">Sin dato oficial</div>'
        )
        meta_html = (
            f'<div style="font-size:9px;color:var(--muted)">Meta: {ind["meta"]:.0f}{ind["unidad"]}</div>'
            if ind["meta"] > 0 else ""
        )
        bar_html = ""

    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-left:3px solid var(--{col});border-radius:9px;
            padding:11px 13px;margin-bottom:7px">
  <div style="display:flex;justify-content:space-between;align-items:center;
              margin-bottom:5px;gap:8px;flex-wrap:wrap">
    <div style="display:flex;align-items:center;gap:6px;flex:1">
      <span style="font-size:14px">{ind["icon"]}</span>
      <div>
        <div style="font-size:9px;color:var(--muted);font-weight:700;letter-spacing:.06em">{ind["codigo"]}</div>
        <div style="font-size:11px;font-weight:700;color:var(--white)">{ind["nombre"]}</div>
      </div>
      {badge}
    </div>
    <div style="text-align:right;flex-shrink:0">
      {valor_html}
      {meta_html}
    </div>
  </div>
  {bar_html}
  <div style="font-size:9px;color:var(--muted)">{ind["nota"]}</div>
</div>"""


# ── PROGRAMAS POA CON PERSPECTIVA DE GÉNERO ───────────────────────────────────
PROGRAMAS_GENERO = [
    {
        "programa": "Patronato Municipal · Grupos vulnerables",
        "monto": 380_000, "pct_genero": 100, "vinculo_psg": True,
        "estado": "OK",
        "nota": "Programas mujer-jefe-hogar, adulto mayor, discapacidad",
    },
    {
        "programa": "Luminarias seguridad Aníbal San Andrés",
        "monto": 95_000, "pct_genero": 80, "vinculo_psg": True,
        "estado": "BLOQUEADO",
        "nota": "Gov Twin activo · requiere PSG ≥30% para Gender Bond",
    },
    {
        "programa": "Formación liderazgo femenino parroquial",
        "monto": 18_000, "pct_genero": 100, "vinculo_psg": True,
        "estado": "PARCIAL",
        "nota": "2 de 7 parroquias · Isabel Muentes y Aníbal SA sin cobertura",
    },
    {
        "programa": "Infraestructura agua Isabel Muentes",
        "monto": 228_000, "pct_genero": 60, "vinculo_psg": True,  # H99 Inv_Total_Q1
        "estado": "CRÍTICO",
        "nota": "Mujeres rurales = 68% de la carga de acarreo de agua",
    },
    {
        "programa": "Espacios seguros niñez y adolescencia",
        "monto": 45_000, "pct_genero": 70, "vinculo_psg": True,
        "estado": "PARCIAL",
        "nota": "Centro cabecera operativo · parroquias rurales sin cobertura",
    },
    {
        "programa": "Vialidad Av. Eloy Alfaro (tramo 3)",
        "monto": 210_000, "pct_genero": 20, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Vinculable a género si incluye iluminación y accesibilidad",
    },
    {
        "programa": "Residuos sólidos EP Aseo",
        "monto": 480_000, "pct_genero": 15, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Potencial: empleo femenino + separación en origen domiciliario",
    },
    {
        "programa": "Digitalización trámites DTIC",
        "monto": 85_000, "pct_genero": 10, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Potencial: trámites accesibles desde hogar para cuidadoras",
    },
]

# ── METAS FA (BIOFÍSICO-AMBIENTE) · H31_REPORTE_CPCCS · corte Q1-2026 ─────────
# (codigo, nombre, desc_meta, Ti_2026, Vi_estado, color)
FA_METAS = [
    ("FA-I-X-01", "Gestión del Riesgo",
     "Infraestructura susceptible reducida -10% · Plan cantonal riesgo",
     0.70, "✅", "green"),
    ("FA-C-X-01", "Áreas Verdes · IVU",
     "Índice Verde Urbano 10.94→17.32 m²/hab · parques y espacios públicos",
     0.43, "✅", "amber"),
    ("FA-I-X-02", "Equipamiento Urbano / Aseo",
     "Recolección residuos 91→98% · barrido · EMAIMEP · EP Aseo",
     0.70, "✅", "green"),
    ("FA-L-N-01", "Patrimonio Cultural-Ambiental",
     "100% inventario · Museo Sombrero · cerro Montecristi protegido",
     0.70, "✅", "green"),
    ("FA-DIS-01", "Disposición Final Desechos",
     "Capacidad disposición final 0→20% · relleno sanitario cantonal",
     0.43, "⬜", "amber"),
    ("FA-CC-01",  "Cambio Climático",
     "4 planes de acción al 2027 · Q1-2026: 0 iniciados · SAT ambiental activa",
     0.00, "⬜", "red"),
]

_total_poa = 26_689_147
_total_genero_actual = sum(
    p["monto"] * (p["pct_genero"] / 100) for p in PROGRAMAS_GENERO if p["vinculo_psg"]
)
_psg_actual  = 12.83
_psg_meta    = 30.0
_psg_brecha  = _psg_meta - _psg_actual

# Proyección si se reclasifican los programas potenciales
_total_genero_potencial = sum(
    p["monto"] * (p["pct_genero"] / 100) for p in PROGRAMAS_GENERO
)
_psg_potencial = (_total_genero_potencial / _total_poa) * 100


def _prog_row(p: dict) -> str:
    col = {"OK": "green", "PARCIAL": "amber", "BLOQUEADO": "red", "CRÍTICO": "red", "NORMAL": "muted"}.get(p["estado"], "muted")
    badge = {
        "OK":       '<span class="badge badge-green">OK</span>',
        "PARCIAL":  '<span class="badge badge-amber">PARCIAL</span>',
        "BLOQUEADO":'<span class="badge badge-red">BLOQUEADO</span>',
        "CRÍTICO":  '<span class="badge badge-red">CRÍTICO</span>',
        "NORMAL":   '<span class="badge badge-cyan">POTENCIAL</span>',
    }.get(p["estado"], "")
    aporte = p["monto"] * (p["pct_genero"] / 100)
    pct_bar = min(p["pct_genero"], 100)
    psg_ico = "💜" if p["vinculo_psg"] else "⬜"
    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:9px;
              padding:11px 13px;margin-bottom:7px">
    <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:5px;gap:8px">
      <div style="display:flex;align-items:center;gap:6px;flex:1;flex-wrap:wrap">
        <span style="font-size:12px">{psg_ico}</span>
        <span style="font-size:11px;font-weight:700;color:var(--white)">{p["programa"]}</span>
        {badge}
      </div>
      <div style="text-align:right;flex-shrink:0">
        <div style="font-size:13px;font-weight:800;color:var(--{'purple' if p['vinculo_psg'] else 'muted'});
                    font-family:var(--mono)">${aporte:,.0f}</div>
        <div style="font-size:8px;color:var(--muted)">{p["pct_genero"]}% género</div>
      </div>
    </div>
    <div style="height:4px;background:var(--divider);border-radius:2px;
                overflow:hidden;margin-bottom:5px">
      <div style="height:4px;width:{pct_bar:.0f}%;
                  background:{'#7C5CFC' if p['vinculo_psg'] else '#444'};
                  border-radius:2px"></div>
    </div>
    <div style="font-size:9px;color:var(--muted)">{p["nota"]}</div>
  </div>"""


def _fa_card(m: tuple) -> str:
    cod, nombre, desc, ti, vi, col = m
    ti_pct = ti * 100
    bar_w  = min(int(ti_pct), 100)
    vi_badge = {
        "✅": '<span style="font-size:9px;font-weight:700;color:var(--green)">✅ Verificada</span>',
        "⬜": '<span style="font-size:9px;font-weight:700;color:rgba(255,255,255,.35)">⬜ Sin verificar</span>',
        "🔄": '<span style="font-size:9px;font-weight:700;color:var(--cyan)">🔄 En proceso</span>',
    }.get(vi, "")
    return (
        f'<div style="background:var(--navy-card);border:1px solid var(--divider);'
        f'border-left:3px solid var(--{col});border-radius:9px;'
        f'padding:11px 13px;margin-bottom:7px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'margin-bottom:5px;gap:8px">'
        f'<div style="flex:1">'
        f'<div style="font-size:9px;color:var(--muted);font-weight:700;'
        f'letter-spacing:.06em;font-family:monospace">{cod}</div>'
        f'<div style="font-size:11px;font-weight:700;color:var(--white)">{nombre}</div>'
        f'</div>'
        f'<div style="text-align:right;flex-shrink:0">'
        f'<div style="font-size:18px;font-weight:900;color:var(--{col});'
        f'font-family:monospace">{ti_pct:.0f}<span style="font-size:10px">% Ti</span></div>'
        f'{vi_badge}</div></div>'
        f'<div style="height:4px;background:var(--divider);border-radius:2px;'
        f'overflow:hidden;margin-bottom:6px">'
        f'<div style="height:4px;width:{bar_w}%;background:var(--{col});border-radius:2px">'
        f'</div></div>'
        f'<div style="font-size:9px;color:var(--muted)">{desc}</div>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 — EJECUTIVO · DOM12 · PROTECCIÓN SOCIAL & GRUPOS PRIORITARIOS
# ADR-013: GAP_10PCT → Dom12 — cadena causal confirmada en Neo4j
# Bloomberg Model: cero nomenclatura interna en esta sección.
# ══════════════════════════════════════════════════════════════════════════════

# Colores canónicos QUIRA
_VERDE   = "#22C55E"
_ALERTA  = "#F97316"
_CRITICO = "#EF4444"
_MUTED   = "rgba(255,255,255,0.45)"


def _render_return_band() -> None:
    """Banda superior de retorno al Centro de Mando — persiste en drill-down Ejecutivo."""
    if is_ejecutivo():
        col1, _col2 = st.columns([1, 7])
        with col1:
            if st.button("← Centro de Mando", key="back_to_cc_d12"):
                st.session_state["gov_module"] = "inicio"
                st.rerun()


def _semaforo_color(semaforo: str) -> str:
    m = {"VERDE": _VERDE, "AMARILLO": _ALERTA, "ROJO": _CRITICO}
    return m.get(semaforo, _MUTED)


def _semaforo_label(semaforo: str) -> str:
    m = {"VERDE": "EN RUTA", "AMARILLO": "BAJO OBJETIVO", "ROJO": "BRECHA CRÍTICA",
         "PENDIENTE": "EN MODELADO"}
    return m.get(semaforo, semaforo)


def _render_dom12_ejecutivo(chain: dict) -> None:
    """
    Layer 2 canónico — Dom12 Protección Social & Grupos Prioritarios.
    Solo lenguaje de gobernanza. Sin nomenclatura interna. Ejecutivo.

    Estructura:
      1. Semáforo y KPI principal
      2. Narrativa causal
      3. Indicadores clave (3 máx.)
      4. Visualización: barra progreso + serie histórica
      5. Pie de página con fuente pública
    """
    # Colores
    sem   = chain.get("semaforo", "ROJO")
    color = _semaforo_color(sem)
    label = _semaforo_label(sem)
    valor = chain.get("valor_principal", 50.0)
    ind_label = chain.get("indicador_label", "Ejecución presupuestaria Patronato Municipal")
    fuente    = chain.get("fuente", "Sistema Integrado de Gestión Financiera · 2025")
    corte     = chain.get("fecha_corte", "noviembre 2025")
    narrativa = chain.get("narrativa", "")
    estado    = chain.get("estado_dato", "confirmado")
    asignacion    = chain.get("asignacion_pct", 20.84)
    sem_asignacion= chain.get("asignacion_semaforo", "VERDE")
    serie         = chain.get("serie_historica", {2023: 35.03, 2024: 53.77, 2025: 50.0})
    fuente_neo4j  = chain.get("fuente_neo4j", False)

    # ── Cabecera de dominio ────────────────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:11px;color:{_MUTED};letter-spacing:2px;"
        f"text-transform:uppercase;margin-bottom:4px'>D12 · PROTECCIÓN SOCIAL</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:20px;font-weight:700;color:white;margin-bottom:16px'>"
        "Protección Social &amp; Grupos de Atención Prioritaria</div>",
        unsafe_allow_html=True,
    )

    # ── Sección 1: Semáforo y KPI principal ───────────────────────────────────
    badge_asterisco = " *" if estado != "confirmado" else ""
    st.markdown(
        f"""<div style="background:{color}18;border:1px solid {color}44;
                     border-left:4px solid {color};border-radius:10px;
                     padding:16px 20px;margin-bottom:16px">
  <div style="font-size:2.8rem;font-weight:900;color:{color};
              font-family:monospace;line-height:1">{valor:.1f}%{badge_asterisco}</div>
  <div style="font-size:0.75rem;font-weight:700;color:{color};
              letter-spacing:1px;margin-top:6px">{label}</div>
  <div style="font-size:0.8rem;color:rgba(255,255,255,0.7);margin-top:6px">
    {ind_label}
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    if estado != "confirmado":
        st.caption(f"* Pendiente confirmación oficial · {fuente}")

    # ── Sección 2: Narrativa causal ───────────────────────────────────────────
    if narrativa:
        st.markdown(
            f"""<div style="background:rgba(255,255,255,0.04);border-radius:10px;
                         padding:14px 18px;margin-bottom:16px;
                         border:1px solid rgba(255,255,255,0.08);
                         font-size:0.88rem;color:rgba(255,255,255,0.82);
                         line-height:1.7">{narrativa}</div>""",
            unsafe_allow_html=True,
        )

    # ── Sección 3: Indicadores clave (3 máx.) ────────────────────────────────
    col_a, col_b, col_c = st.columns(3)

    col_ejecucion_color = _semaforo_color(sem)
    col_asig_color      = _semaforo_color(sem_asignacion)

    with col_a:
        st.markdown(
            f"""<div style="background:{col_ejecucion_color}15;border:1px solid {col_ejecucion_color}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{col_ejecucion_color};
              font-family:monospace">{valor:.1f}%</div>
  <div style="font-size:0.68rem;color:{col_ejecucion_color};font-weight:700;margin-top:4px">
    BRECHA CRÍTICA
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Ejecución presupuestaria<br>Patronato Municipal
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""<div style="background:{col_asig_color}15;border:1px solid {col_asig_color}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{col_asig_color};
              font-family:monospace">{asignacion:.1f}%</div>
  <div style="font-size:0.68rem;color:{col_asig_color};font-weight:700;margin-top:4px">
    CUMPLE LA NORMA
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Asignación presupuestaria<br>para grupos prioritarios
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    with col_c:
        umbral = chain.get("umbral_verde", 85.0)
        brecha = umbral - valor
        st.markdown(
            f"""<div style="background:{_CRITICO}15;border:1px solid {_CRITICO}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{_CRITICO};
              font-family:monospace">{brecha:.0f} pts</div>
  <div style="font-size:0.68rem;color:{_CRITICO};font-weight:700;margin-top:4px">
    DISTANCIA AL UMBRAL
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Umbral de referencia<br>{umbral:.0f}% · SIGEF
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Sección 4: Visualización ──────────────────────────────────────────────
    # Barra de progreso
    progress_pct = min(valor / 100.0, 1.0)
    umbral_pct   = min(umbral / 100.0, 1.0)

    st.markdown(
        f"""<div style="margin-bottom:16px">
  <div style="font-size:0.75rem;color:{_MUTED};margin-bottom:6px;
              font-weight:600;letter-spacing:1px">EJECUCIÓN PRESUPUESTARIA VS UMBRAL</div>
  <div style="position:relative;height:10px;background:rgba(255,255,255,0.1);
              border-radius:6px;overflow:hidden;margin-bottom:4px">
    <div style="position:absolute;height:100%;width:{valor:.1f}%;
                background:{color};border-radius:6px;
                transition:width 0.5s ease"></div>
    <div style="position:absolute;height:100%;left:{umbral:.0f}%;
                width:2px;background:{_VERDE};opacity:0.7"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:0.7rem;
              color:{_MUTED}">
    <span>0%</span>
    <span style="color:{_VERDE}">▲ Umbral {umbral:.0f}%</span>
    <span>100%</span>
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    # Serie histórica
    if serie:
        años = sorted(serie.keys())
        vals = [serie[a] for a in años]
        bars = ""
        max_v = max(vals) if vals else 100
        for año, v in zip(años, vals):
            h = (v / max_v) * 60  # altura relativa en px
            c = _semaforo_color("VERDE" if v >= umbral else "ROJO")
            bars += (
                f"<div style='display:flex;flex-direction:column;align-items:center;gap:4px'>"
                f"<div style='font-size:0.75rem;color:{c};font-weight:700'>{v:.0f}%</div>"
                f"<div style='width:40px;height:{h:.0f}px;background:{c};border-radius:4px 4px 0 0'></div>"
                f"<div style='font-size:0.68rem;color:{_MUTED}'>{año}</div>"
                f"</div>"
            )
        st.markdown(
            f"""<div style="margin-bottom:20px">
  <div style="font-size:0.75rem;color:{_MUTED};margin-bottom:10px;
              font-weight:600;letter-spacing:1px">SERIE HISTÓRICA · EJECUCIÓN PATRONATO</div>
  <div style="display:flex;gap:24px;align-items:flex-end;height:80px">{bars}</div>
</div>""",
            unsafe_allow_html=True,
        )

    # ── Sección 5: Pie de página ──────────────────────────────────────────────
    fuente_label = (
        f"{'🔴 Datos en vivo · Neo4j' if fuente_neo4j else '📋 Datos consolidados'}"
        f" · Fuente: {fuente} · Corte: {corte}"
    )
    st.caption(fuente_label)


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 TÉCNICO — Vista enriquecida para Directivo / Técnico / Administrador
# (contenido existente — violaciones de lenguaje pendientes de corrección)
# ══════════════════════════════════════════════════════════════════════════════

def _render_dom12_tecnico() -> None:
    """Vista técnica existente — Directivo / Técnico / Administrador."""
    data      = load_all()
    show_tech = is_tecnico()
    indices   = data["indices"]
    psg_val   = indices.get("PSG", {}).get("valor", _psg_actual)

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(124,92,252,.1);border:1px solid rgba(124,92,252,.35);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--purple);
                font-family:var(--mono)">{psg_val:.2f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--purple);margin-top:4px">PSG ACTUAL</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Ruptura Sistémica</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{_psg_meta:.0f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">META PDOT 2027</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Desbloquea Gender Bond</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{_psg_brecha:.2f}<span style="font-size:18px">pts</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">BRECHA PSG</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Vs meta mínima 30%</div>
  </div>
  <div style="background:rgba(124,92,252,.08);border:1px solid rgba(124,92,252,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--purple);
                font-family:var(--mono)">${(_total_genero_potencial/1000):.0f}K</div>
    <div style="font-size:10px;font-weight:700;color:var(--purple);margin-top:4px">POA RECLASIFICABLE</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">PSG potencial {_psg_potencial:.1f}%</div>
  </div>
</div>"""

    # ── Panel IGM ─────────────────────────────────────────────────────────────
    igm_criticos  = sum(1 for i in INDICADORES_GENERO if i["estado"] in ("CRÍTICO", "BLOQUEADO"))
    igm_parciales = sum(1 for i in INDICADORES_GENERO if i["estado"] in ("ALERTA", "PARCIAL"))
    igm_ok        = sum(1 for i in INDICADORES_GENERO if i["estado"] == "OK")

    # Contar indicadores con y sin dato oficial
    igm_sin_dato = sum(1 for i in INDICADORES_GENERO if i["valor"] is None)

    igm_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">💜 PANEL IGM · INDICADORES DE GÉNERO MUNICIPAL · {len(INDICADORES_GENERO)} dimensiones</div>
  <div style="font-size:8px;color:var(--amber);margin-bottom:10px;
              padding:5px 10px;background:rgba(255,184,0,.07);border-radius:5px;
              border:1px solid rgba(255,184,0,.2);line-height:1.6">
    ⚠ <strong>Integridad de datos:</strong>
    {igm_sin_dato} de {len(INDICADORES_GENERO)} indicadores muestran "Sin dato oficial"
    — valores no disponibles en el Gold Master (H73/H99).
    IGM-D e IGM-E son estados binarios derivados del PSG 12.83% (fuente: H73_OUTPUT_API).
    Pendiente: certificación RRHH (IGM-A), análisis nómina DAF (IGM-B),
    encuesta PNUD/INEC (IGM-C), fuente CNE/AME (IGM-F).
  </div>
  <div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap">
    <div style="padding:6px 12px;background:rgba(255,77,109,.1);border-radius:7px;
                font-size:10px;color:var(--red);font-weight:700">
      🔴 {igm_criticos} crítico/bloqueado
    </div>
    <div style="padding:6px 12px;background:rgba(255,184,0,.08);border-radius:7px;
                font-size:10px;color:var(--amber);font-weight:700">
      🟠 {igm_parciales} alerta/parcial
    </div>
    <div style="padding:6px 12px;background:rgba(0,224,150,.07);border-radius:7px;
                font-size:10px;color:var(--green);font-weight:700">
      ✅ {igm_ok} OK
    </div>
    <div style="padding:6px 12px;background:rgba(255,255,255,.04);border-radius:7px;
                font-size:10px;color:rgba(255,255,255,.4);font-weight:700">
      📋 {igm_sin_dato} sin dato oficial
    </div>
  </div>
  <div class="grid-2" style="gap:10px">
    <div>{"".join(_igm_card(i) for i in INDICADORES_GENERO[:3])}</div>
    <div>{"".join(_igm_card(i) for i in INDICADORES_GENERO[3:])}</div>
  </div>
</div>"""

    # ── ODS 5 Sub-targets ─────────────────────────────────────────────────────
    def _ods5_row(t: dict) -> str:
        """avance=None → sin porcentaje oficial, muestra badge de estado."""
        col_map  = {"CRÍTICO": "red", "ALERTA": "amber", "PARCIAL": "amber", "OK": "green"}
        badge_map = {
            "CRÍTICO": '<span style="font-size:8px;font-weight:700;color:var(--red)">🔴 CRÍTICO</span>',
            "ALERTA":  '<span style="font-size:8px;font-weight:700;color:var(--amber)">🟠 ALERTA</span>',
            "PARCIAL": '<span style="font-size:8px;font-weight:700;color:var(--amber)">🟡 PARCIAL</span>',
            "OK":      '<span style="font-size:8px;font-weight:700;color:var(--green)">✅ OK</span>',
        }
        c       = col_map.get(t["estado"], "muted")
        avance  = t.get("avance")
        if avance is not None:
            derecha_html = f"""
    <div style="min-width:90px">
      <div style="height:5px;background:var(--divider);border-radius:3px;overflow:hidden;margin-bottom:2px">
        <div style="height:5px;width:{avance}%;background:var(--{c});border-radius:3px"></div>
      </div>
      <div style="font-size:8px;color:var(--{c});text-align:right">{avance}%</div>
    </div>"""
        else:
            # Sin dato oficial → mostrar badge cualitativo
            derecha_html = f"""
    <div style="min-width:90px;text-align:right">
      {badge_map.get(t["estado"], "")}
      <div style="font-size:7px;color:var(--muted);margin-top:1px">sin medición</div>
    </div>"""
        return f"""
<div style="display:flex;align-items:center;gap:10px;padding:6px 8px;
            background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:3px">
  <span style="font-size:10px;font-weight:800;color:var(--purple);
               min-width:28px;font-family:var(--mono)">{t["id"]}</span>
  <div style="flex:1;font-size:9px;color:var(--white)">{t["desc"]}</div>
  {derecha_html}
</div>"""

    ods5_html = f"""
<div style="background:rgba(124,92,252,.05);border:1px solid rgba(124,92,252,.2);
            border-radius:12px;padding:14px 16px;margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:4px">
    🌐 ODS 5 · SUB-METAS MONTECRISTI · Estado Q1-2026
  </div>
  <div style="font-size:8px;color:var(--amber);margin-bottom:8px;
              padding:4px 8px;background:rgba(255,184,0,.07);border-radius:4px;
              border:1px solid rgba(255,184,0,.2)">
    ⚠ Avance % pendiente de medición oficial SNP/ONU Mujeres · Estado cualitativo derivado del PDOT
  </div>
  {"".join(_ods5_row(t) for t in ODS5_TARGETS)}
  <div style="margin-top:8px;font-size:9px;color:var(--muted)">
    PSG 12.83% afecta directamente ODS 5.c · Luminarias (IGM-D) afecta ODS 5.2 · Plan género (IGM-E) afecta 5.1 y 5.5
  </div>
</div>"""

    gender_bond_html = f"""
<div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.3);
            border-radius:12px;padding:14px 16px;margin-bottom:16px;
            display:flex;align-items:flex-start;gap:14px">
  <div style="font-size:32px;flex-shrink:0">💜</div>
  <div style="flex:1">
    <div style="font-size:12px;font-weight:700;color:var(--purple);margin-bottom:6px">
      BID Lab GENDER BOND · $95,000 · BLOQUEADO · Vence Q3-2026
    </div>
    <div style="font-size:11px;color:var(--muted);line-height:1.7;margin-bottom:8px">
      El Gender Bond financia luminarias de seguridad en Aníbal San Andrés
      (Pin Morado activo · Gov Twin aprobado). Está <strong style="color:var(--red)">bloqueado</strong>
      porque el BID Lab exige PSG ≥ 30%. Con PSG actual 12.83%, la brecha es
      <strong style="color:var(--purple)">{_psg_brecha:.2f} puntos</strong>.
      Si no se alcanza antes de Q3-2026, el fondo <strong style="color:var(--red)">vence</strong>
      y debe recompetir en la siguiente convocatoria (2027).
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <div style="padding:6px 12px;background:rgba(124,92,252,.12);border-radius:7px;
                  font-size:10px;color:var(--purple)">
        Reclasificar 3 programas POA → PSG sube a ~{_psg_potencial:.1f}%
      </div>
      <div style="padding:6px 12px;background:rgba(0,212,255,.08);border-radius:7px;
                  font-size:10px;color:var(--cyan)">
        Acción legal bajo COOTAD Art. 55 lit. c · no requiere reforma presupuestaria
      </div>
    </div>
  </div>
</div>"""

    plan_reclasificacion_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">💜 PLAN RECLASIFICACIÓN POA · PSG {psg_val:.2f}% → {_psg_potencial:.1f}%</div>
  <div style="font-size:10px;color:var(--muted);margin-bottom:10px;
              padding:6px 10px;background:rgba(124,92,252,.05);
              border-radius:6px;border:1px solid rgba(124,92,252,.15)">
    La reclasificación de partidas presupuestarias con perspectiva de género
    no requiere reforma presupuestaria — solo un informe técnico DAF + resolución Alcaldía.
    El PDOT ya vincula estos programas con ODS 5. Plazo estimado: 15 días hábiles.
  </div>
  {"".join(_prog_row(p) for p in PROGRAMAS_GENERO)}
  <div style="margin-top:10px;padding:8px 10px;
              background:rgba(124,92,252,.05);border:1px solid rgba(124,92,252,.15);
              border-radius:7px;font-size:10px;color:var(--purple)">
    💜 PSG actual: {psg_val:.2f}% ·
    Con reclasificación potencial: {_psg_potencial:.1f}% ·
    Meta Gender Bond: ≥30% · Meta ONU Mujeres: ≥25%
  </div>
</div>"""

    hoja_ruta_html = """
<div class="grid-2">
  <div style="background:rgba(124,92,252,.06);border:1px solid rgba(124,92,252,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:8px">
      💜 HOJA DE RUTA PSG · 30 DÍAS
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 1-5:</strong> Informe técnico DAF · identificar partidas reclasificables
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 6-10:</strong> Resolución Alcaldía · reforma interna POA
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 11-15:</strong> Registro eSIGEF · PSG recalculado ≥20%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 16-30:</strong> Ampliar programas género · PSG ≥30% · Gender Bond
      </div>
    </div>
  </div>
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:8px">
      ✅ BENEFICIOS DE ALCANZAR PSG ≥ 30%
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        💜 Gender Bond BID Lab $95K · luminarias Aníbal San Andrés desbloqueadas
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        🌐 ONU Mujeres Municipio Igualitario $65K · elegibilidad activa
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        📈 ODS 5 pasa de CRÍTICO a PARCIAL · ICODS sube a ~90%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        🏆 Sello igualdad ONU Mujeres · diferenciador político para 2027
      </div>
    </div>
  </div>
</div>"""

    hdr = page_header(
        "GÉNERO · EQUIDAD · AMBIENTE",
        "PSG · ODS 5 · Gender Bond · Metas FA",
        f"PSG {psg_val:.2f}% · Brecha {_psg_brecha:.2f} pts · Gender Bond $95K · "
        f"6 metas FA PDOT · Cambio climático sin iniciar",
        '<span class="badge badge-red">💜 PSG Ruptura Sistémica</span>',
    )

    tab1, tab2 = st.tabs(["💜  Género", "🌿  Ambiente"])

    # ══════════════════════════════════════════════════════════════════════
    # TAB 1: GÉNERO Y EQUIDAD
    # ══════════════════════════════════════════════════════════════════════
    with tab1:
        render_page(
            hdr + resumen_html + igm_html + ods5_html + gender_bond_html
            + plan_reclasificacion_html + hoja_ruta_html,
            show_tech=show_tech, height=2100,
        )
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔮 Sentinel · Plan reclasificación PSG",
                         use_container_width=True, type="primary"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    f"El PSG de Montecristi es {psg_val:.2f}%. El Gender Bond BID Lab $95K "
                    "y ONU Mujeres $65K están bloqueados por este indicador. "
                    f"La reclasificación de partidas en el POA podría elevar el PSG a ~{_psg_potencial:.1f}%. "
                    "¿Cuál es el procedimiento legal exacto bajo COOTAD y el reglamento SINFÍN "
                    "para reclasificar partidas presupuestarias con perspectiva de género, "
                    "quién firma la resolución y cuánto tiempo toma el registro en eSIGEF?"
                )
                st.rerun()
        with c2:
            if st.button("💸 Ver Cooperación Internacional", use_container_width=True):
                st.session_state["page"] = "cooperacion"
                st.rerun()
        with c3:
            if st.button("🌐 Ver Agenda 2030 · ODS", use_container_width=True,
                         key="btn_ods_tab1"):
                st.session_state["page"] = "ods"
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # TAB 2: AMBIENTE
    # ══════════════════════════════════════════════════════════════════════
    with tab2:
        fa_ini    = sum(1 for m in FA_METAS if m[3] > 0)
        fa_no_ini = sum(1 for m in FA_METAS if m[3] == 0)

        amb_kpi_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:14px;text-align:center">
    <div style="font-size:34px;font-weight:900;color:var(--green);font-family:monospace">{fa_ini}<span style="font-size:14px">/{len(FA_METAS)}</span></div>
    <div style="font-size:9px;font-weight:700;color:var(--green)">METAS FA INICIADAS</div>
    <div style="font-size:8px;color:var(--muted)">Ti > 0% · H31_REPORTE_CPCCS</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:14px;text-align:center">
    <div style="font-size:34px;font-weight:900;color:var(--red);font-family:monospace">{fa_no_ini}</div>
    <div style="font-size:9px;font-weight:700;color:var(--red)">SIN INICIAR</div>
    <div style="font-size:8px;color:var(--muted)">CC + DIS · riesgo RDC 2026</div>
  </div>
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:12px;padding:14px;text-align:center">
    <div style="font-size:34px;font-weight:900;color:var(--cyan);font-family:monospace">74</div>
    <div style="font-size:9px;font-weight:700;color:var(--cyan)">FICHAS PP 2026</div>
    <div style="font-size:8px;color:var(--muted)">Aseo / Recolección / Ambiente</div>
  </div>
  <div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
              border-radius:12px;padding:14px;text-align:center">
    <div style="font-size:34px;font-weight:900;color:var(--green);font-family:monospace">30</div>
    <div style="font-size:9px;font-weight:700;color:var(--green)">APORTES RDC FA</div>
    <div style="font-size:8px;color:var(--muted)">Componente más demandado · H10c</div>
  </div>
</div>"""

        fa_cards = "".join(_fa_card(m) for m in FA_METAS)
        fa_metas_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">🌿 6 METAS BIOFÍSICO-AMBIENTE · Plan 2023-2027 · Estado ene–mar 2026</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:10px;padding:5px 10px;
              background:rgba(0,212,255,.05);border-radius:5px;
              border:1px solid rgba(0,212,255,.1)">
    Fuente: H31_REPORTE_CPCCS · Ti = ejecución presupuestaria Q1-2026 ·
    Vi = verificación documental proyectada · Meta PDOT 2027
  </div>
  <div class="grid-2" style="gap:10px">
    <div>{fa_cards[:len(fa_cards)//2 + 200]}</div>
    <div>{"".join(_fa_card(m) for m in FA_METAS[3:])}</div>
  </div>
</div>"""

        fa_metas_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">🌿 6 METAS BIOFÍSICO-AMBIENTE · Plan 2023-2027 · Estado ene–mar 2026</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:10px;padding:5px 10px;
              background:rgba(0,212,255,.05);border-radius:5px;border:1px solid rgba(0,212,255,.1)">
    Fuente: H31_REPORTE_CPCCS · Ti = ejecución presupuestaria Q1-2026 ·
    Vi ✅ verificada / ⬜ sin verificar · Meta global al 2027
  </div>
  {"".join(_fa_card(m) for m in FA_METAS)}
  <div style="margin-top:8px;padding:8px 10px;background:rgba(255,77,109,.06);
              border:1px solid rgba(255,77,109,.15);border-radius:7px;
              font-size:10px;color:var(--red)">
    ⚠ <strong>Riesgo RDC 2026:</strong> FA-CC-01 (Cambio Climático) y FA-DIS-01 (Disposición Final)
    muestran Ti=0% en Q1-2026. Sin acciones documentadas antes de junio,
    estas metas aparecerán como incumplidas en el informe CPCCS.
  </div>
</div>"""

        alin_html = f"""
<div style="background:rgba(0,224,150,.04);border:1px solid rgba(0,224,150,.15);
            border-radius:12px;padding:14px 16px;margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:10px">
    🔄 CICLO VERIFICADO: RDC DEMANDAS AMBIENTE → PP 2026 PRIORIDADES
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
    <div>
      <div style="font-size:9px;font-weight:700;color:var(--muted);margin-bottom:8px">
        APORTES RDC 2023-2024 · COMPONENTE FA (30 registros · H10c)
      </div>
      {"".join(
        f'<div style="font-size:9px;color:var(--white);padding:5px 8px;'
        f'background:rgba(255,255,255,.02);border-radius:5px;margin-bottom:3px">'
        f'{"🔴" if "Pepa de Huso" in t or "ladrillera" in t or "Climát" in t else "🟡"} {t}</div>'
        for t in [
            "Culminar ducto cajón aguas residuales (Pepa de Huso)",
            "Recolección basura periódica en múltiples sectores",
            "Reforestar barrio Santa Isabella",
            "Reubicación ladrilleras en la Y",
            "Control chancheras y empresas por mal olor",
            "Coordinar obras destrucción cerro carretera Toalla",
            "Visitas periódicas a empresas (control ambiental)",
        ]
      )}
    </div>
    <div>
      <div style="font-size:9px;font-weight:700;color:var(--muted);margin-bottom:8px">
        PP 2026 · TOP PRIORIDADES AMBIENTE
      </div>
      <div style="padding:10px;background:rgba(0,212,255,.06);border-radius:8px;
                  border:1px solid rgba(0,212,255,.15);margin-bottom:6px">
        <div style="font-size:10px;font-weight:700;color:var(--cyan)">#1 Agua Potable / Saneamiento</div>
        <div style="font-size:28px;font-weight:900;color:var(--cyan);font-family:monospace">126 fichas</div>
        <div style="font-size:8px;color:var(--muted)">Incluye alcantarillado y aguas servidas</div>
      </div>
      <div style="padding:10px;background:rgba(0,224,150,.06);border-radius:8px;
                  border:1px solid rgba(0,224,150,.15)">
        <div style="font-size:10px;font-weight:700;color:var(--green)">#5 Aseo / Recolección / Ambiente</div>
        <div style="font-size:28px;font-weight:900;color:var(--green);font-family:monospace">74 fichas</div>
        <div style="font-size:8px;color:var(--muted)">EP Aseo · EMAIMEP · gestión residuos</div>
      </div>
    </div>
  </div>
  <div style="margin-top:10px;padding:6px 10px;background:rgba(0,224,150,.05);
              border-radius:6px;font-size:9px;color:var(--green)">
    FA fue el componente más demandado en RDC (30/95 aportes = 31.6%) →
    Agua+Aseo son prioridades #1 y #5 en PP 2026 → el ciclo participativo está funcionando.
  </div>
</div>"""

        tab2_content = amb_kpi_html + fa_metas_html + alin_html
        render_page(tab2_content, show_tech=show_tech, height=1500)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔮 Sentinel · Estrategia FA metas críticas",
                         use_container_width=True, type="primary"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    "En el componente biofísico-ambiental del PDOT 2023-2027 de Montecristi, "
                    "FA-CC-01 (Cambio Climático: 4 planes al 2027) y FA-DIS-01 (Disposición final "
                    "desechos: 0→20%) muestran Ti=0% en Q1-2026. El componente FA fue el más "
                    "demandado en RDC 2023-2024 con 30 aportes ciudadanos. "
                    "¿Qué acciones concretas puede tomar el GAD en Q2-2026 para iniciar estos dos "
                    "planes antes del informe RDC de junio, qué competencias institucionales "
                    "intervienen y qué presupuesto mínimo requiere cada uno?"
                )
                st.rerun()
        with c2:
            if st.button("🗳️ Ver Gobernanza Participativa", use_container_width=True):
                st.session_state["page"] = "gobernanza"
                st.rerun()
        with c3:
            if st.button("🌐 Ver Agenda 2030 · ODS", use_container_width=True,
                         key="btn_ods_tab2"):
                st.session_state["page"] = "ods"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT CANÓNICO — Layer 2 Dom12
# ADR-013 · Sprint 3 Panel Estratégico
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Layer 2 — Protección Social & Grupos Prioritarios
    Dominio D12 · Sprint 3 Panel Estratégico

    Ejecutivo → vista canónica QTMP (narrativa causal + semáforo + fuente pública)
    Directivo / Técnico / Administrador → vista enriquecida técnica
    """
    from app.connectors.neo4j_qtmp import get_qtmp_chain

    # Banda de retorno siempre arriba
    _render_return_band()

    if is_ejecutivo():
        chain = get_qtmp_chain("GAP_10PCT")
        if chain:
            _render_dom12_ejecutivo(chain)
        else:
            st.error("Datos del dominio no disponibles. Intente nuevamente.")
    else:
        _render_dom12_tecnico()
