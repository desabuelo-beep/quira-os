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

    text_alto  = "\n".join(lines_alto[:8])
    text_otros = "\n".join(lines_otros[:5])

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
        if len(lines) >= 10:
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
    Resumen compacto del diagnóstico oficial PDOT (version condensada para TPM limit).
    Fuente: documento diagnóstico técnico PDOT Montecristi 2023-2027 (300 págs).
    """
    return _section(
        "DIAGNÓSTICO PDOT — BRECHAS Y POTENCIALIDADES CLAVE",
        """BRECHAS CRÍTICAS (prioridad alta en matrices oficiales PDOT):
  · Agua/Saneamiento: 34.9% viviendas con red pública agua; 43.5% alcantarillado (INEC).
  · Vías: 53% centro urbano con tratamiento medio, 15.61% sin tratamiento.
  · Residuos: 47.9 ton/día generación sin reciclaje ni clasificación.
  · Conectividad/Salud: acceso inequitativo a tecnología y servicios médicos.
  · Empleo: falta especialización mano de obra; oferta no suple demanda.
  · Institucional: catastro predial desactualizado; déficit RRHH especializado.
  · Riesgos naturales: asentamientos en zonas deslizamiento/movimiento de masa (ENOS).

POTENCIALIDADES ESTRATÉGICAS:
  · Turismo: UNESCO ciudad creativa; artesanía paja toquilla; recursos naturales.
  · Empleo: 3er lugar en plazas de empleo en Manabí; polo inversión privada creciente.
  · Social: Patronato 56,158 beneficiarios; Clínica Diálisis; CBV; menor índice delitos vs Manta.
  · Ambiente: SNAP protegido, convenios reforestación, distintivo AFC agricultura familiar.
  · Economía solidaria: artesanías paja toquilla/mimbre/barro con potencial formalización.

VIVIENDA Y DEMOGRAFÍA: 34.6% población sin casa propia. Migración familiar en crecimiento.
GRUPOS PRIORITARIOS: Patronato (CBV 90%, USMC 4.4%, CMD 3%, Solidario 2.2%). Junta Cantonal.
ECONOMÍA: Cooperativas financieras como principal fuente crédito. Sin plan turismo formal."""
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
