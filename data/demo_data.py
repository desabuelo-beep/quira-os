"""
QUIRA OS v0.1 — Datos sellados Q1-2026
Fuente: SIAP-ICPI_GOLD_MASTER_v4.1_QUIRA_20260514.xlsx · Corte Q1-2026
Sincronizado con H73_OUTPUT_API (50 métricas) + H99_ENGINE_CORE (7 parroquias)
Verificado con quira_extract.py v1.1 · Dylus Lab © 2026

⚠ INTEGRIDAD:
  - INDICES: todos los valores provienen de H73_OUTPUT_API (verificado quira_extract.py)
  - PARROQUIAS nbi/agua/composite_need: derivados de H99_ENGINE_CORE
  - PARROQUIAS tps: Tasa de Pobreza por Servicios · fuente INEC/PDOT diagnóstico oficial
    (no extraída por quira_extract.py · pendiente vinculación directa H99)
  - PARROQUIAS inversion/per_capita/habitantes: POA-PAC GAD + INEC proyecciones
  - PARROQUIAS participacion.estado/actas/fichas_pp2026: verificados en "INFORME PP 2026 GAD Montecristi.pdf"
    (6 talleres ago-2025, 149 fichas, 7/7 parroquias con acta, ACTA N°007-2025-JLAC-JPC-GADMCM)
  - PP_2024: "GAD Montecristi Informe Presupuesto Participativo 2024.pdf" (40 pp) · FY2024 · proceso online jul-2023
    (presupuesto $6.1M, 7/7 parroquias, ACTA N°002-2023-JLAC-JPC-GADMCM)
  - PP_2025: "GAD Montecristi Informe Presupuesto Participativo 2025.pdf" (124 pp) · FY2025 · talleres ago-2024
    (137 fichas, 6 talleres, $5.7M priorización, ingresos $21.6M, ACTA N°005-2024-JLAC)
  - PARROQUIAS participacion.presupuesto: sin asignación oficial per-parroquia en PDF → valor 0
  - IGM-A,B,C,F en p19_genero: sin dato oficial → mostrados como 'Sin dato oficial'
  - ODS5_TARGETS avance en p19_genero: sin medición oficial → mostrados como N/D
"""

# ── ICGI-T GLOBAL ─────────────────────────────────────────────────────────────
ICGIT_Q1_2026 = {
    "score":          53.56,
    "avep":           "Transición Crítica",
    "avep_emoji":     "🟡",
    "corte":          "Q1-2026 · solo marzo",
    "ti_raw":         23.75,        # % inversión ejecutada Q1
    "ti_norm":        70.0,         # % ritmo normalizado (ok para mayo)
    "proyeccion":     65.77,        # proyección cierre 2026
    "meta_mandato":   70.0,         # ≥70% Gestión por Mandato
    "historico": {
        "2023": 57.36,
        "2024": 67.12,
        "2025": 69.93,
        "2026_q1": 53.56,
        "2026_proj": 65.77,
    },
    "presupuesto_total": 26_689_147,
    "inversion_ejecutada": 7_820_000,
}

# ── 10 ÍNDICES COMPLEMENTARIOS ────────────────────────────────────────────────
INDICES = {
    "IFE-A": {
        "nombre": "Fidelidad Electoral",
        "valor":  72.73,
        "avep":   "Gestión por Mandato",
        "emoji":  "🟢",
        "color":  "#38A169",
        "estado": "REAL auditado",
        "nota":   "48 de 66 promesas vinculadas al PDOT",
    },
    "IFE-E": {
        "nombre": "Fidelidad Ejecución",
        "valor":  None,
        "avep":   "En construcción",
        "emoji":  "⏳",
        "color":  "#7C5CFC",
        "estado": "Q2-2026",
        "nota":   "Mide trazabilidad POA→PAC→eSIGEF",
    },
    "ISP": {
        "nombre": "Salud Presupuestaria",
        "valor":  14.58,
        "avep":   "Ruptura Sistémica",
        "emoji":  "🔴",
        "color":  "#E53E3E",
        "estado": "REAL Q1-2026",
        "nota":   "−8.2 pts ICGI-T · SAT-IV activa",
    },
    "IED": {
        "nombre": "Eficiencia Direcciones",
        "valor":  33.99,
        "avep":   "Gestión por Ocurrencia",
        "emoji":  "🟠",
        "color":  "#E67E22",
        "estado": "En calibración",
        "nota":   "12 direcciones evaluadas · IED Q2-2026",
    },
    "IGP": {
        "nombre": "Gobernanza Participativa",
        "valor":  27.98,
        "avep":   "Gestión por Ocurrencia",
        "emoji":  "🟠",
        "color":  "#7C5CFC",
        "estado": "Referencia 2025",
        "nota":   "CPCCS V=0 en RDC 2026 · 50 UT activas vs meta 75",
    },
    "PSG": {
        "nombre": "Presupuesto Género",
        "valor":  12.83,
        "avep":   "Ruptura Sistémica",
        "emoji":  "🔴",
        "color":  "#E53E3E",
        "estado": "REAL Q1-2026",
        "nota":   "Bloquea acceso Gender Bond · ONU Mujeres",
    },
    "ITAM": {
        "nombre": "Transparencia Municipal",
        "valor":  56.00,
        "avep":   "Transición Crítica",
        "emoji":  "🟡",
        "color":  "#D69E2E",
        "estado": "Referencia 2025",
        "nota":   "LOTAIP parcial · portal desactualizado",
    },
    "IOC": {
        "nombre": "Opacidad Crítica",
        "valor":  17.71,
        "avep":   "Ruptura Sistémica",
        "emoji":  "🔴",
        "color":  "#E53E3E",
        "estado": "Referencia 2025",
        "nota":   "Índice invertido — mayor es peor",
    },
    "IET": {
        "nombre": "Equidad Territorial",
        "valor":  44.80,
        "avep":   "Transición Crítica",
        "emoji":  "🟡",
        "color":  "#D69E2E",
        "estado": "REAL Q1-2026",
        "nota":   "Isabel Muentes $40/hab vs cabecera $113/hab",
    },
    "ICODS": {
        "nombre": "Cumplimiento ODS",
        "valor":  87.50,
        "avep":   "Gestión por Mandato",
        "emoji":  "🟢",
        "color":  "#38A169",
        "estado": "Referencia 2025",
        "nota":   "14 ODS vinculados con metas PDOT",
    },
}

# ── 4 CONGRUENCIAS ────────────────────────────────────────────────────────────
CONGRUENCIAS = {
    "politica": {
        "nombre": "Congruencia Política",
        "pregunta": "¿Estamos gobernando lo que prometimos?",
        "score": 72.73,
        "avep": "Gestión por Mandato",
        "emoji": "🟢",
        "color": "#00D4FF",
        "fuente": "IFE-A · 48/66 promesas CNE vinculadas al PDOT",
    },
    "operativa": {
        "nombre": "Congruencia Operativa",
        "pregunta": "¿Lo planificado se está ejecutando?",
        "score": 47.20,
        "avep": "Transición Crítica",
        "emoji": "🟡",
        "color": "#FF4D6D",
        "fuente": "POA→PAC→SERCOP→eSIGEF · 4 cortes detectados",
    },
    "territorial": {
        "nombre": "Congruencia Territorial",
        "pregunta": "¿La inversión llega donde más se necesita?",
        "score": 44.80,
        "avep": "Transición Crítica",
        "emoji": "🟡",
        "color": "#FF4D6D",
        "fuente": "GeoTwin · 7 parroquias · PDOT_KB",
    },
    "ecosistemica": {
        "nombre": "Congruencia Ecosistémica",
        "pregunta": "¿Todo el holding municipal está alineado?",
        "score": 68.90,
        "avep": "Transición Crítica",
        "emoji": "🟡",
        "color": "#FFB700",
        "fuente": "HPT-M · 4 entidades · Bomberos/Patronato/EP Aseo",
    },
}

# ── SAT ACTIVAS ───────────────────────────────────────────────────────────────
SAT_ACTIVAS = [
    {
        "id": "SAT-0",
        "nombre": "Coherencia POA-PAC",
        "estado": "ACTIVA",
        "nivel": "CRÍTICO",
        "color": "#E53E3E",
        "emoji": "🔴",
        "descripcion": "24 procesos sin evidencia SHA-256 · Gasto Ciego C4",
        "impacto": "−6.8 pts ICGI-T · riesgo observación Contraloría",
        "accion": "Publicar evidencias PAC en portal SERCOP · plazo 48h",
    },
    {
        "id": "SAT-IV",
        "nombre": "Alerta Fiscal COOTAD",
        "estado": "ACTIVA",
        "nivel": "CRÍTICO",
        "color": "#E53E3E",
        "emoji": "🔴",
        "descripcion": "ISP 14.58% bajo umbral mínimo COOTAD 65%",
        "impacto": "−8.2 pts ICGI-T · bloquea perfil BDE",
        "accion": "Activar coactivas · actualizar catastro predial",
    },
    {
        "id": "SAT-I",
        "nombre": "Fragmentación Selectiva",
        "estado": "PREVENTIVA",
        "nivel": "ALERTA",
        "color": "#E67E22",
        "emoji": "🟠",
        "descripcion": "Patrón de partición de contratos detectado",
        "impacto": "−3.1 pts ICGI-T potencial · riesgo LOSNCP",
        "accion": "Auditar procesos de contratación DAPS-01",
    },
    {
        "id": "SAT-V",
        "nombre": "Brecha CPCCS",
        "estado": "PREVENTIVA",
        "nivel": "ALERTA",
        "color": "#D69E2E",
        "emoji": "🟡",
        "descripcion": "IGP 27.98% · PP 2026 completado 7/7 parroquias · Asambleas locales: solo 2/7",
        "impacto": "−2.4 pts IGP · déficit en asambleas parroquiales formales COOTAD Art.304",
        "accion": "Formalizar asambleas locales pendientes · Aníbal San Andrés e Isabel Muentes",
    },
]

# ── HOLDING MUNICIPAL (HPT-M) ─────────────────────────────────────────────────
HOLDING = {
    "icgit_global": 53.56,
    "entidades": [
        {
            "id": "GAD",
            "nombre": "GAD Central",
            "tipo": "Alcaldía · Concejo · 12 Direcciones",
            "score": 61.20,
            "nodo": "Nodo 1",
            "avep": "Transición Crítica",
            "emoji": "🟡",
            "color": "#D69E2E",
            "alerta": False,
        },
        {
            "id": "BOMB",
            "nombre": "Cuerpo de Bomberos",
            "tipo": "Entidad adscrita · servicio emergencias",
            "score": 82.70,
            "nodo": "Nodo 2",
            "avep": "Gestión por Mandato",
            "emoji": "🟢",
            "color": "#38A169",
            "alerta": False,
        },
        {
            "id": "PAT",
            "nombre": "Patronato Municipal",
            "tipo": "Desarrollo social · grupos vulnerables",
            "score": 74.10,
            "nodo": "Nodo 2",
            "avep": "Gestión por Mandato",
            "emoji": "🟢",
            "color": "#38A169",
            "alerta": False,
        },
        {
            "id": "EP_ASEO",
            "nombre": "EP Aseo Municipal",
            "tipo": "Empresa pública · residuos sólidos",
            "score": 58.40,
            "nodo": "Nodo 2",
            "avep": "Transición Crítica",
            "emoji": "🟡",
            "color": "#D69E2E",
            "alerta": True,
        },
    ],
}

# ── 7 PARROQUIAS (GeoTwin) ────────────────────────────────────────────────────
PARROQUIAS = [
    {
        "nombre": "Isabel Muentes",
        "tps": 77.94,
        "nbi": 61.2,
        "agua": 1.02,
        "inversion": 140_000,
        "habitantes": 3_488,
        "per_capita": 40,
        "estado": "EMERGENCIA",
        "color": "#E53E3E",
        "emoji": "🚨",
        # PP 2026: Taller 3 (07-ago-2025) · Antigua Escuela Sucre · ACTA N°003-2025
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        "nombre": "Aníbal San Andrés",
        "tps": 62.34,
        "nbi": 61.7,
        "agua": 28.9,
        "inversion": 190_000,
        "habitantes": 3_100,
        "per_capita": 61,
        "estado": "PRIORIDAD",
        "color": "#7C5CFC",
        "emoji": "💜",
        # PP 2026: Taller 2 (06-ago-2025) · Auditorium GAD · ACTA N°002-2025
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        "nombre": "Colorado",
        "tps": 58.67,
        "nbi": 58.4,
        "agua": 34.7,
        "inversion": 210_000,
        "habitantes": 2_230,
        "per_capita": 94,
        "estado": "ALERTA",
        "color": "#E67E22",
        "emoji": "🟠",
        # PP 2026: Taller 5 (08-ago-2025) · Auditorio GAD · ACTA N°005-2025 · 18 fichas (Colorado+El Arroyo+Los Corrales)
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 18},
    },
    {
        "nombre": "La Pila",
        "tps": 41.23,
        "nbi": 52.8,
        "agua": 51.2,
        "inversion": 380_000,
        "habitantes": 4_100,
        "per_capita": 93,
        "estado": "NORMAL",
        "color": "#D69E2E",
        "emoji": "🟡",
        # PP 2026: Taller 4 (07-ago-2025) · GAD La Pila · ACTA N°004-2025 · 10 fichas (La Pila+Cda Virgen del Pilar+Las Lagunas+Aguas Nuevas)
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 10},
    },
    {
        "nombre": "Eloy Alfaro",
        "tps": 31.18,
        "nbi": 45.1,
        "agua": 62.1,
        "inversion": 980_000,
        "habitantes": 12_800,
        "per_capita": 77,
        "estado": "NORMAL",
        "color": "#D69E2E",
        "emoji": "🟡",
        # PP 2026: Taller 3 (07-ago-2025) · Antigua Escuela Sucre · ACTA N°003-2025 · (combinado con Isabel Muentes, ~14 fichas c/u)
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        "nombre": "Leónidas Plaza",
        "tps": 28.76,
        "nbi": 41.3,
        "agua": 68.4,
        "inversion": 720_000,
        "habitantes": 8_200,
        "per_capita": 88,
        "estado": "NORMAL",
        "color": "#D69E2E",
        "emoji": "🟡",
        # PP 2026: Taller 6 (08-ago-2025) · CDC Leónidas Proaño · ACTA N°006-2025 · 25 fichas
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 25},
    },
    {
        "nombre": "Montecristi (cabecera)",
        "tps": 22.45,
        "nbi": 38.2,
        "agua": 78.3,
        "inversion": 3_200_000,
        "habitantes": 28_400,
        "per_capita": 113,
        "estado": "OK",
        "color": "#38A169",
        "emoji": "🏛️",
        # PP 2026: Taller 1 (06-ago-2025, AM, 31 fichas) + Taller 2 (06-ago-2025, PM, 28 fichas) · ACTAS N°001-002-2025
        "participacion": {"mesas": 2, "presupuesto": 0, "actas": 2, "estado": "Activo", "fichas_pp2026": 59},
    },
]

# ── PRESUPUESTO PARTICIPATIVO · SERIE HISTÓRICA ──────────────────────────────
# Fuentes primarias verificadas (PDFs oficiales GAD Montecristi):
#   PP_2024: "GAD Montecristi Informe Presupuesto Participativo 2024.pdf" (40 pp)
#            INFORME N°003-JLAC-JPC-GADCM-2023 · proceso online jul-2023 · FY2024
#   PP_2025: "GAD Montecristi Informe Presupuesto Participativo 2025.pdf" (124 pp)
#            MEMORANDO N°255-JLAC-JPC-GADMCM-2024 · talleres ago-2024 · FY2025
#   PP_2026: "INFORME DE PRESUPUESTO PARTICIPATIVO 2026 GAD MOntecristi.pdf" (153 pp)
#            ACTA N°007-2025-JLAC-JPC-GADMCM · talleres ago-2025 · FY2026

PP_2024 = {
    "fiscal_year":          2024,
    "proceso_fecha":        "2023-07-18/20",
    "proceso_metodo":       "Formulario online · convocatoria pública GAD web",
    "acta_aprobacion":      "ACTA N°002-2023-JLAC-JPC-GADMCM",
    "fecha_aprobacion":     "2023-06-21",
    "informe":              "INFORME N°003-JLAC-JPC-GADCM-2023",
    "parroquias_cubiertas": 7,
    "total_talleres":       None,      # proceso online, sin talleres presenciales
    "total_fichas":         None,      # online; respuestas individuales sin ficha estándar
    "ingresos_estimados":   None,      # sin dato oficial en PDF disponible
    "presupuesto_total":    6_118_924, # USD · suma componentes verificada en PDF p.3
    "base_legal":           "COOTAD Art. 238 · LOPC Art. 67-71",
    "presupuesto_componentes": {
        "Biofísico":                161_920,
        "Económico Productivo":      60_760,
        "Sociocultural":            468_750,
        "Asentamientos Humanos":  3_220_532,
        "Político Institucional": 2_206_962,
    },
}

PP_2025 = {
    "fiscal_year":          2025,
    "proceso_fecha":        "2024-08-08/13",
    "proceso_metodo":       "6 talleres presenciales · 7 parroquias · 6 mesas de trabajo",
    "acta_conformidad":     "ACTA N°005-2024-JLAC-JPC-GADMCM",
    "fecha_aprobacion":     "2024-08-15",
    "memorando":            "MEMORANDO N°255-JLAC-JPC-GADMCM-2024 · 30-oct-2024",
    "parroquias_cubiertas": 7,
    "total_talleres":       6,
    "total_fichas":         137,       # verificado: T1=16+T2=14+T3=31+T4=19+T5=24+T6=33
    "ingresos_estimados":   21_606_774, # USD ingresos provisionales 2025 (fuente: PDF p.19)
    "ingresos_propios":     12_188_220, # 56.41% del total
    "transferencias":        9_418_574, # 43.59% del total
    "presupuesto_total":     5_687_954, # USD total priorización sistematizada (fuente: PDF p.116)
    "base_legal":           "COOTAD Art. 238, 302, 303, 305 · LOPC Art. 67-71",
    "talleres_fichas": {
        "T1_Eloy_Alfaro_rural":  16,   # ACTA N°001-2024-JLAC · Los Bajos comunas (08-ago-2024 9am)
        "T2_La_Pila":            14,   # ACTA N°002-2024-JLAC · La Pila (08-ago-2024 3pm)
        "T3_Montecristi_Anibal": 31,   # ACTA N°003-2024-JLAC · Montecristi+Aníbal San Andrés (12-ago-2024 9am)
        "T4_Colorado_Arroyo":    19,   # ACTA N°004-2024-JLAC · Colorado+El Arroyo+Los Corrales (12-ago-2024 3pm)
        "T5_Isabel_Muentes":     24,   # ACTA N°001-2024-AGMC · Isabel Muentes (13-ago-2024 10am)
        "T6_Leonidas_Proano":    33,   # ACTA N°002-2024-AGMC · Leónidas Proaño (13-ago-2024 4pm)
    },
    "presupuesto_componentes": {
        "Físico Ambiental":      1_249_758,  # 22%
        "Territorial AAHH":     1_886_695,  # 33%
        "Social Cultural":       1_331_666,  # 23%
        "Económico Productivo":    603_279,  # 11%
        "Político Institucional":  616_554,  # 11%
    },
}

# ── PRESUPUESTO PARTICIPATIVO 2026 (fuente: Informe PP GAD Montecristi) ──────
# Verificado en "INFORME DE PRESUPUESTO PARTICIPATIVO 2026 GAD MOntecristi.pdf"
PP_2026 = {
    "total_fichas":       149,          # fichas sistematizadas (fuente: PDF p.5)
    "total_talleres":     6,            # 6-8 agosto 2025
    "ingresos_estimados": 20_982_884,   # USD estimación provisional (fuente: PDF p.2+actas)
    "ingresos_propios":    9_738_444,   # USD ingresos propios de gestión
    "acta_aprobacion":    "ACTA N°007-2025-JLAC-JPC-GADMCM",
    "fecha_aprobacion":   "2025-08-15",
    "parroquias_cubiertas": 7,          # 7/7 con acta oficial
    "alcalde":            "Jonathan Toro Largacha",
    "base_legal":         "COOTAD Art. 238, 302, 303, 305 · LOPC Art. 67-71",
    "top_prioridades": {
        "Agua Potable":         126,
        "Áreas verdes/parques": 95,
        "Vialidad":             94,
        "Salud":                80,
        "Aseo/Recolección":     74,
    },
    "fichas_pp2026_nota": (
        "fichas_pp2026 en PARROQUIAS son estimadas por taller (talleres agrupan múltiples parroquias). "
        "Total oficial verificado: 149. Suma parcelas estimadas: 154 (+5 error estimación)."
    ),
}

# ── MÉTRICAS TERRITORIALES (H99_ENGINE_CORE · v4.0) ──────────────────────────
# Fuente: SIAP-ICPI_GOLD_MASTER_v4.0 · H99_ENGINE_CORE + H73_OUTPUT_API

IRS_GLOBAL = 79.7
# Índice de Regresividad Social — Composite_Need v2.1
# 79.7% = Muy Regresivo: inversión NO llega donde más se necesita
# Fórmula oficial: -CORREL(Composite_Need, Inv_PerCápita) × 100
# Composite_Need = 0.50×(NBI/100) + 0.30×(1-Agua/100) + 0.20×(Pop/total)
# Fuente: Tester SIAP-ICPI análisis de sensibilidad v2.1 · Gold Master v4.1

IRS_CLASIFICACION = "🔴 Muy Regresivo"
# Umbrales: <30 Equitativo · 30-50 Moderado · 50-70 Regresivo · >70 Muy Regresivo
# Rango sensibilidad (tester): 71.8–82.1 según pesos · todos "Muy Regresivo"

# Sensitivity scenarios (Tester v2.1)
IRS_SENSIBILIDAD = [
    {"label": "Base Anterior",       "w_agua": 45, "w_nbi": 30, "w_pop": 25, "irs": 78.4},
    {"label": "Alto énfasis NBI",    "w_agua": 35, "w_nbi": 50, "w_pop": 15, "irs": 82.1},
    {"label": "Alto énfasis Agua",   "w_agua": 60, "w_nbi": 25, "w_pop": 15, "irs": 76.9},
    {"label": "★ Recomendado v2.1",  "w_agua": 50, "w_nbi": 30, "w_pop": 20, "irs": 79.7},
    {"label": "Bajo énfasis NBI",    "w_agua": 50, "w_nbi": 20, "w_pop": 30, "irs": 74.3},
    {"label": "Muy bajo NBI",        "w_agua": 55, "w_nbi": 15, "w_pop": 30, "irs": 71.8},
]

TRUST_SCORE = 89.6
# Trust Score del sistema ICPI — confianza en los datos y el modelo

BRECHA_FONDOS_BLOQ = 3_660_000
# USD de fondos internacionales bloqueados por métricas ICPI insuficientes
# BDE $3.5M (ISP<65%) + Gender Bond $95K + ONU Mujeres $65K (PSG<30%)

NBI_RURAL_PCT = 67.9
# % promedio de NBI en parroquias rurales del cantón Montecristi

NBI_URBANA_PCT = 23.0
# % NBI en cabecera cantonal (Montecristi urbano)

GPS_PARROQUIAS_OK = 7
# Parroquias con coordenadas GPS cargadas en CAPA_TERRITORIAL

# ── PARROQUIAS TERRITORIALES — datos H99 (coordenadas + Composite_Need) ───────
# NOTA: Población en H99 difiere de PARROQUIAS arriba (fuente PDOT vs INEC 2022)
# Isabel Muentes: H99=5,700 hab (INEC) vs PARROQUIAS=3,488 (beneficiarios proyecto agua)
# Usar H99 para análisis territorial, PARROQUIAS para inversión per cápita operativa
PARROQUIAS_GEO = {
    "Montecristi":        {"lat": -1.0450, "lon": -80.6578, "composite_need": 0.3310, "nbi_pct": 38.4},
    "Aníbal San Andrés":  {"lat": -1.0238, "lon": -80.5891, "composite_need": 0.3521, "nbi_pct": 52.1},
    "Colorado":           {"lat": -1.1253, "lon": -80.5612, "composite_need": 0.4614, "nbi_pct": 58.7},
    "Leónidas Proaño":    {"lat": -1.0978, "lon": -80.6021, "composite_need": 0.2591, "nbi_pct": 54.3},
    "Gral. Alfaro":       {"lat": -0.9876, "lon": -80.5234, "composite_need": 0.2468, "nbi_pct": 49.8},
    "Isabel Muentes":     {"lat": -0.9712, "lon": -80.6487, "composite_need": 0.5928, "nbi_pct": 61.2},
    "La Pila":            {"lat": -1.0689, "lon": -80.6923, "composite_need": 0.4181, "nbi_pct": 55.9},
}
