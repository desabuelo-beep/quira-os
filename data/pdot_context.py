"""
QUIRA OS v0.1 — PDOT Context Loader para Sentinel
Lee PDOT_MONTECRISTI_KB.xlsx y genera un bloque de contexto semántico
compacto (~4-5k tokens) para inyectar en el system prompt de Sentinel.

Hojas usadas (por valor prospectivo):
  KB_PRIORIZACION      → potencialidades + problemas ponderados por sistema
  KB_RIESGOS           → amenazas territoriales con nivel y área
  KB_NBI               → necesidades básicas insatisfechas por territorio
  KB_SERVICIOS_PARROQUIAS → cobertura agua/saneamiento/electricidad
  KB_PROPUESTA_METAS   → compromisos PDOT 2023-2027
  KB_ARTICULACIONES    → alianzas institucionales activas
  KB_MODELO_PROGRAMAS  → objetivos de desarrollo por sistema

Estrategia: texto plano estructurado, no JSON — Claude razona mejor con
lenguaje natural compacto que con estructuras anidadas.

Dylus Lab © 2026
"""
import streamlit as st
import pandas as pd
from typing import Optional
from config import get_pdot_path


@st.cache_data(ttl=7200, show_spinner=False)
def build_pdot_context() -> str:
    """
    Genera el bloque de contexto PDOT para Sentinel.
    Retorna string vacío si el Excel no está disponible.
    """
    try:
        pdot_path = get_pdot_path()
        sheets = pd.read_excel(pdot_path, sheet_name=None, header=None)
    except Exception:
        return ""

    blocks = []

    # ── 1. IDENTIDAD TERRITORIAL ─────────────────────────────────────────────
    blocks.append(_section(
        "TERRITORIO: CANTON MONTECRISTI — CONTEXTO PDOT 2023-2027",
        "GAD Municipal de Montecristi, provincia de Manabí, Ecuador. "
        "Período de planificación: 2023-2027 (Plan Bicentenario). "
        "El PDOT estructura el territorio en 5 sistemas: Físico Ambiental, "
        "Asentamientos Humanos, Sociocultural, Económico Productivo y "
        "Político Institucional. El cantón tiene como cabecera Montecristi "
        "y 7 parroquias rurales, con alta diversidad de condiciones sociales."
    ))

    # ── 2. PRIORIDADES Y PROBLEMAS (KB_PRIORIZACION) ─────────────────────────
    df_prio = _get_sheet(sheets, "KB_PRIORIZACION")
    if df_prio is not None:
        blocks.append(_build_priorizacion(df_prio))

    # ── 3. RIESGOS TERRITORIALES (KB_RIESGOS) ────────────────────────────────
    df_risk = _get_sheet(sheets, "KB_RIESGOS")
    if df_risk is not None:
        blocks.append(_build_riesgos(df_risk))

    # ── 4. NBI POR TERRITORIO (KB_NBI) ───────────────────────────────────────
    df_nbi = _get_sheet(sheets, "KB_NBI")
    if df_nbi is not None:
        blocks.append(_build_nbi(df_nbi))

    # ── 5. COBERTURA DE SERVICIOS (KB_SERVICIOS_PARROQUIAS) ──────────────────
    df_serv = _get_sheet(sheets, "KB_SERVICIOS_PARROQUIAS")
    if df_serv is not None:
        blocks.append(_build_servicios(df_serv))

    # ── 6. METAS PDOT 2023-2027 (KB_PROPUESTA_METAS) ────────────────────────
    df_metas = _get_sheet(sheets, "KB_PROPUESTA_METAS")
    if df_metas is not None:
        blocks.append(_build_metas(df_metas))

    # ── 7. PROGRAMAS (KB_MODELO_PROGRAMAS) ───────────────────────────────────
    df_prog = _get_sheet(sheets, "KB_MODELO_PROGRAMAS")
    if df_prog is not None:
        blocks.append(_build_programas(df_prog))

    # ── 8. ARTICULACIONES (KB_ARTICULACIONES) ────────────────────────────────
    df_art = _get_sheet(sheets, "KB_ARTICULACIONES")
    if df_art is not None:
        blocks.append(_build_articulaciones(df_art))

    # ── 9. DIAGNÓSTICO OFICIAL (fuente: documento Word diagnóstico PDOT) ─────
    blocks.append(_build_diagnostico_docx())

    return "\n\n".join(b for b in blocks if b)


# ── BUILDERS POR HOJA ─────────────────────────────────────────────────────────

def _build_priorizacion(df: pd.DataFrame) -> str:
    """
    KB_PRIORIZACION: potencialidades y problemas por sistema PDOT.
    Columnas: Sistema_PDOT, Tematica, Potencialidad, Problema, Nivel_Priorizacion
    """
    cols = {
        "sistema":  1,   # Sistema_PDOT
        "tematica": 3,   # Tematica
        "pot":      5,   # Potencialidad
        "prob":     6,   # Problema
        "nivel":    12,  # Nivel_Priorizacion
    }
    lines_alto = []
    lines_otros = []

    for _, row in df.iterrows():
        sistema = _val(row, cols["sistema"])
        tematica = _val(row, cols["tematica"])
        pot   = _val(row, cols["pot"])
        prob  = _val(row, cols["prob"])
        nivel = _val(row, cols["nivel"])

        if not sistema or sistema in ("Municipio_ID", "Sistema_PDOT"):
            continue

        line = f"  [{sistema} | {tematica}] POTENCIALIDAD: {_trunc(pot, 120)} | PROBLEMA: {_trunc(prob, 120)} [{nivel}]"
        if nivel == "Alto":
            lines_alto.append(line)
        else:
            lines_otros.append(line)

    text_alto  = "\n".join(lines_alto[:15])
    text_otros = "\n".join(lines_otros[:10])

    return _section(
        "PRIORIDADES PDOT — POTENCIALIDADES Y PROBLEMAS TERRITORIALES",
        f"PRIORIDAD ALTA (urgencia + alcance + capacidad institucional):\n{text_alto}\n\n"
        f"PRIORIDAD MEDIA:\n{text_otros}"
    )


def _build_riesgos(df: pd.DataFrame) -> str:
    """
    KB_RIESGOS: amenazas territoriales.
    Columnas: Riesgo_ID, Tipo_Amenaza, Nivel, Territorio, Area_Afectada_ha, Medida_Mitigacion
    """
    cols = {"tipo": 2, "nivel": 3, "territorio": 4, "area": 6, "medida": 7}
    lines = []

    for _, row in df.iterrows():
        tipo  = _val(row, cols["tipo"])
        nivel = _val(row, cols["nivel"])
        terr  = _val(row, cols["territorio"])
        area  = _val(row, cols["area"])
        medida = _val(row, cols["medida"])

        if not tipo or tipo in ("Tipo_Amenaza",):
            continue

        area_str = f" ({area} ha)" if area else ""
        medida_str = f" → Medida: {_trunc(medida, 80)}" if medida else ""
        lines.append(f"  - {_trunc(tipo, 90)}{area_str} | Nivel: {nivel or 'no clasificado'} | Zona: {_trunc(terr, 70)}{medida_str}")

    return _section(
        "RIESGOS TERRITORIALES IDENTIFICADOS EN EL PDOT",
        "\n".join(lines[:25])
    )


def _build_nbi(df: pd.DataFrame) -> str:
    """
    KB_NBI: NBI por territorio y año.
    Columnas: Geo_ID, Territorio, Año, NBI_Total_%, NBI_Agua_%
    """
    cols = {"territorio": 2, "anio": 3, "nbi": 4, "componente": 5}
    registros = {}

    for _, row in df.iterrows():
        terr = _val(row, cols["territorio"])
        anio = _val(row, cols["anio"])
        nbi  = _val(row, cols["nbi"])
        comp = _val(row, cols["componente"])

        if not terr or terr in ("Territorio",):
            continue
        # Ignorar las filas de 'SOCIOCULTURAL' (son headers de bloque)
        if comp and len(str(comp)) > 15:
            continue

        key = terr
        if key not in registros:
            registros[key] = {}
        try:
            registros[key][str(anio)] = float(nbi)
        except (ValueError, TypeError):
            pass

    lines = []
    for terr, datos in list(registros.items())[:15]:
        years = sorted(datos.items())
        vals = " | ".join(f"{y}: {v:.1f}%" for y, v in years)
        lines.append(f"  {terr}: {vals}")

    return _section(
        "NBI (NECESIDADES BÁSICAS INSATISFECHAS) POR TERRITORIO",
        "Fuente: PDOT 2023-2027 — Referencia 2022-2023.\n" + "\n".join(lines)
    )


def _build_servicios(df: pd.DataFrame) -> str:
    """
    KB_SERVICIOS_PARROQUIAS: cobertura de servicios.
    Columnas: Parroquia, Agua_%, Saneamiento_%, Pluvial_%, Electricidad_%
    """
    # Buscar la fila header real
    header_row = None
    for i, row in df.iterrows():
        if any(str(v).strip().lower() in ("parroquia", "agua_%", "agua") for v in row if v):
            header_row = i
            break

    if header_row is None:
        return ""

    lines = []
    for _, row in df.iloc[header_row + 1:].iterrows():
        vals = [v for v in row if pd.notna(v)]
        if len(vals) >= 4:
            try:
                parroquia = str(vals[0])[:40]
                agua      = f"{float(vals[1]):.1f}%" if vals[1] else "?"
                sanea     = f"{float(vals[2]):.1f}%" if vals[2] else "?"
                elec      = f"{float(vals[4]):.1f}%" if len(vals) > 4 and vals[4] else "?"
                lines.append(f"  {parroquia}: agua={agua} | saneamiento={sanea} | electricidad={elec}")
            except (ValueError, IndexError):
                continue

    return _section(
        "COBERTURA DE SERVICIOS BÁSICOS POR PARROQUIA",
        "⚠ Nota PDOT: datos agua/saneamiento corresponden a CUPS (urbanizaciones), "
        "no toda el área parroquial.\n" + "\n".join(lines[:10])
    )


def _build_metas(df: pd.DataFrame) -> str:
    """
    KB_PROPUESTA_METAS: compromisos PDOT 2023-2027.
    Columnas: Meta_ID, Sistema, Subsistema, Sector, Nombre_Indicador
    """
    cols = {"sistema": 2, "sector": 4, "nombre": 5}
    por_sistema: dict[str, list] = {}

    for _, row in df.iterrows():
        sistema = _val(row, cols["sistema"])
        sector  = _val(row, cols["sector"])
        nombre  = _val(row, cols["nombre"])

        if not sistema or sistema in ("Sistema", "Municipio_ID"):
            continue

        if sistema not in por_sistema:
            por_sistema[sistema] = []
        if len(por_sistema[sistema]) < 4:
            por_sistema[sistema].append(f"{sector}: {_trunc(nombre, 90)}")

    text = ""
    for sistema, items in por_sistema.items():
        text += f"\n  [{sistema}]\n" + "\n".join(f"    · {i}" for i in items)

    return _section(
        "METAS PDOT 2023-2027 (COMPROMISOS DE GESTIÓN)",
        text
    )


def _build_programas(df: pd.DataFrame) -> str:
    """
    KB_MODELO_PROGRAMAS: programas y objetivos de desarrollo.
    Columnas: Sistema, Objetivo_Desarrollo, Objetivo_Gestion, Programa
    """
    cols = {"sistema": 2, "obj_des": 3, "obj_ges": 4, "programa": 5}
    vistos = set()
    lines = []

    for _, row in df.iterrows():
        sistema   = _val(row, cols["sistema"])
        obj_des   = _val(row, cols["obj_des"])
        programa  = _val(row, cols["programa"])

        if not sistema or sistema in ("Sistema", "Municipio_ID"):
            continue

        key = (sistema, programa)
        if key in vistos or not programa:
            continue
        vistos.add(key)

        lines.append(f"  [{sistema}] {_trunc(obj_des, 80)} → Programa: {_trunc(programa, 60)}")
        if len(lines) >= 18:
            break

    return _section(
        "PROGRAMAS Y OBJETIVOS DE DESARROLLO PDOT",
        "\n".join(lines)
    )


def _build_articulaciones(df: pd.DataFrame) -> str:
    """
    KB_ARTICULACIONES: alianzas y convenios institucionales.
    Columnas: Art_ID, Iniciativa, Institucion, Objetivo, Forma_Gestion
    """
    cols = {"iniciativa": 2, "institucion": 3, "forma": 5}
    creditos = []
    convenios = []
    alianzas = []

    for _, row in df.iterrows():
        inic   = _val(row, cols["iniciativa"])
        inst   = _val(row, cols["institucion"])
        forma  = _val(row, cols["forma"])

        if not inic or inic in ("Iniciativa",):
            continue

        line = f"  {_trunc(inic, 70)} ({_trunc(inst, 50)}) [{forma}]"
        if forma == "credito":
            creditos.append(line)
        elif forma == "convenio":
            convenios.append(line)
        else:
            alianzas.append(line)

    text = ""
    if creditos:
        text += "CRÉDITOS/FINANCIAMIENTO:\n" + "\n".join(creditos[:5])
    if convenios:
        text += "\n\nCONVENIOS INSTITUCIONALES:\n" + "\n".join(convenios[:8])
    if alianzas:
        text += "\n\nALIANZAS:\n" + "\n".join(alianzas[:5])

    return _section(
        "ARTICULACIONES INSTITUCIONALES Y COOPERACIÓN",
        text
    )


# ── UTILIDADES ────────────────────────────────────────────────────────────────

def _section(title: str, content: str) -> str:
    sep = "─" * 70
    return f"## {title}\n{sep}\n{content}"


def _get_sheet(sheets: dict, name: str) -> Optional[pd.DataFrame]:
    """Retorna el DataFrame de la hoja o None."""
    if name in sheets:
        return sheets[name]
    return None


def _val(row, idx: int) -> str:
    """Obtiene valor de una fila por índice, devuelve string limpio."""
    try:
        v = row.iloc[idx]
        if pd.isna(v):
            return ""
        return str(v).strip()
    except (IndexError, TypeError):
        return ""


def _trunc(text: str, n: int) -> str:
    """Trunca un string a n caracteres."""
    if not text:
        return ""
    return text[:n] + ("…" if len(text) > n else "")


def _build_diagnostico_docx() -> str:
    """
    Contexto estático extraído del documento diagnóstico oficial PDOT Montecristi 2023-2027.
    Fuente: 'diagnostico pdot para claude ingesta excel 2.docx' (Dylus Lab ProyecT).
    Incluye matrices de sistematización y tablas de priorización por los 5 sistemas PDOT.
    """
    return _section(
        "DIAGNÓSTICO OFICIAL PDOT — MATRICES DE POTENCIALIDADES, PROBLEMAS Y PRIORIZACIÓN",
        """Fuente: Documento de diagnóstico técnico oficial PDOT Montecristi 2023-2027.
Metodología de priorización: C1=Apoyo sectorial, C2=Urgencia, C3=Ámbito territorial, C4=Capacidad institucional.
Niveles: Alto (≥9 pts), Medio (5-8), Bajo (<5).

━━ SISTEMA FÍSICO AMBIENTAL ━━
  [ALTO · 9pts]  Ecosistema — Contaminación de cuencas hídricas por descargas domésticas e industriales. Potencialidad: convenios de reforestación con fauna silvestre.
  [ALTO · 10pts] Amenazas Naturales — Asentamientos en zonas de deslizamientos y movimientos de masa (eventos ENOS, sismos). Capacidad de respuesta ante eventos menores con sitios evacuación.
  [ALTO · 10pts] Calidad Ambiental/Residuos — Déficit de espacio para tratamiento residuos sólidos (producción: 47.9 ton/día sin reciclaje). EP Aseo tiene competencia de recolección.
  [MEDIO · 8pts] Contaminación — Aguas servidas en quebradas/esteros + emisiones GEI por cambio de uso de suelo agrícola y silvicultura.
  [MEDIO · 7pts] Patrimonio Hídrico — Pérdida de hábitats por expansión urbana, agricultura intensiva. Patrimonio en SNAP con protección marítima.
  [MEDIO · 6pts] Recursos Mineros — Falta facilidades para material pétreo obra pública. Minería ilegal en ecosistemas frágiles.
  Desafío LP: infraestructura resiliente ante cambio climático; sistemas de monitoreo continuo.

━━ SISTEMA ASENTAMIENTOS HUMANOS ━━
  [ALTO · 12pts] Agua y Saneamiento — Solo 34.9% viviendas con red pública de agua; 43.5% con alcantarillado (INEC). Estudios de ampliación existen en PUGS 2023.
  [ALTO · 10pts] Red de Vías — Centro urbano: 53% vías con tratamiento medio, 15.61% sin tratamiento. Mal estado vías: principal malestar ciudadano. PUGS proyecta vías interconexión.
  [MEDIO · 7pts] Transporte — Sin Plan Inteligente de Movilidad urbana; transporte público ineficiente; accidentes por falta de señaléticas y agentes de control.
  [MEDIO · 7pts] Vivienda — 34.6% de la población sin casa propia (arrendada/prestada). PUGS proyecta suelo para vivienda social.
  [MEDIO · 6pts] Equipamiento — No cumple cobertura estándar de equipamientos por habitante. PUGS 2023 destina suelos para equipamientos futuros.
  Desafío LP: conectividad rural prioritaria; plan de movilidad integral.

━━ SISTEMA SOCIOCULTURAL ━━
  [ALTO · 10pts] Educación/Salud/Conectividad — Acceso inequitativo a tecnología y salud; carencia de programas deportivos y educacionales comunitarios.
  [ALTO · 9pts]  Grupos Prioritarios — Falta programas de protección social. Patronato: 56,158 beneficiarios (CBV 90.23%, USMC 4.45%, CMD 3%, Montecristi Solidario 2.24%).
  [ALTO · 9pts]  Pobreza y NBI — Necesidad urgente de políticas para áreas rurales. Montecristi: menor índice de delitos vs. Manta y Portoviejo.
  [MEDIO · 8pts] Seguridad — Escasa vigilancia policial; déficit luminarias en espacios públicos; falta oportunidades laborales estables.
  [MEDIO · 5pts] Patrimonio Cultural — Artesanos paja toquilla no formalizados; no acceden a financiamiento. Reconocimiento UNESCO ciudad creativa.
  [MEDIO · 5pts] Demografía/Migración — Ausencia de políticas para familias migrantes que llegan buscando nuevas oportunidades.
  Potencialidades sociales: Clínica Municipal Diálisis, CBV, Junta Cantonal Protección Derechos.

━━ SISTEMA ECONÓMICO PRODUCTIVO ━━
  [ALTO · 10pts] Concentración de Riqueza — Carencia de asesoramiento técnico/empresarial; emprendedores sin estrategias efectivas.
  [ALTO · 9pts]  Tecnología Limpia — Ausencia de normativa que promueva tecnologías limpias; 47.9 ton/día residuos sin tratamiento.
  [MEDIO · 8pts] Empleo — Falta especialización de mano de obra local; oferta no suple demanda. Montecristi: 3er lugar plazas empleo en Manabí.
  [MEDIO · 8pts] Economía Solidaria — Artesanías paja toquilla, mimbre, barro: productividad local sin formalización completa.
  [MEDIO · 6pts] Turismo — Sin agencias turísticas, centros comunitarios, ni transporte turístico. Recursos: arquitectura, naturaleza, artesanía.
  [MEDIO · 5pts] Servicios Financieros — Dificultades acceso crédito por falta de garantías; cooperativas como fuente principal.
  [BAJO · 4pts]  Modelos de Consumo — Actividades industriales/turísticas concentradas en ciudad; desequilibrio campo-ciudad.
  Potencialidades económicas: inversión privada creciente, distintivo AFC agricultura familiar, programa FAO alimentación.

━━ SISTEMA POLÍTICO INSTITUCIONAL ━━
  [ALTO · 10pts] Seguimiento Institucional — Carencia de evaluación en procesos de fortalecimiento; catastro predial desactualizado; déficit RRHH especializado.
  [MEDIO · 8pts] Gobernanza del Riesgo — Falta recursos para proyectos de gestión del riesgo; albergues temporales en escuelas durante desastres.
  [MEDIO · 8pts] Actores Territoriales — Relación baja con GAD's provinciales/cantonales y Gobierno Central; buena relación con academia y ONG internacionales.
  [MEDIO · 7pts] Participación Ciudadana — Falta incentivos y programas que fomenten participación activa; comités barriales/comunitarios no consolidados.
  [MEDIO · 6pts] Capacidades Institucionales — Déficit equipos, maquinarias, RRHH especializado; imagen institucional en construcción.
  [MEDIO · 6pts] Transversalización Igualdad — Oportunidad de fortalecer imagen con comunicación abierta y participativa.
  Potencialidades institucionales: convenios ONG internacionales, buena relación academia-GAD.

━━ POTENCIALIDADES ESTRATÉGICAS DEL CANTÓN ━━
  · Turismo y cultura: UNESCO ciudad creativa, artesanía paja toquilla (tratamiento MP a venta), recursos naturales.
  · Economía: 3er lugar en plazas de empleo en Manabí; polo creciente de inversión privada local y extranjera.
  · Social: Patronato de Amparo Social con 56,158 beneficiarios; clínica diálisis; CBV Centro Diario Buen Vivir.
  · Ambiente: Sistema Nacional Áreas Protegidas, protección marina, convenios reforestación, distintivo AFC.
  · Seguridad: índice de delitos más bajo comparado con Manta y Portoviejo.
  · Institucional: alianzas ONG internacionales y academia; programa FAO 'Alimentando la Ciudad'.

━━ DESAFÍOS ESTRATÉGICOS DE LARGO PLAZO (PDOT oficial) ━━
  · Cobertura universal agua potable/saneamiento (brecha actual: 65.1% sin red pública agua).
  · Plan de Movilidad Inteligente: reducir accidentes, mejorar conectividad rural.
  · Infraestructura salud resiliente ante ENOS y cambio climático.
  · Formalizar artesanos paja toquilla + plan turismo sostenible con agencias e intermediación.
  · Fortalecer relación con Gobierno Central y GADs provinciales (actualmente baja).
  · Reducir NBI en parroquias rurales (agua, vivienda, salud, educación).
  · Normativa de tecnologías limpias + sistema de reciclaje para 47.9 ton/día residuos."""
    )


# ── FUNCIÓN DE DIAGNÓSTICO ────────────────────────────────────────────────────
def pdot_context_stats() -> dict:
    """Retorna estadísticas del contexto para debug en modo técnico."""
    ctx = build_pdot_context()
    return {
        "disponible": bool(ctx),
        "tokens_aprox": len(ctx) // 4,
        "chars": len(ctx),
        "bloques": ctx.count("## "),
    }
