"""
QUIRA OS v0.1 — Datos sellados Q1-2026
Fuente: SIAP-ICPI_GOLD_MASTER_v4.1_QUIRA_20260514.xlsx · Corte Q1-2026
Sincronizado con H73_OUTPUT_API (50 métricas) + H99_ENGINE_CORE (7 parroquias)
Auditado y corregido 2026-05-15 contra Gold Master v4.1 · Dylus Lab © 2026

⚠ INTEGRIDAD — FUENTES POR CAMPO:
  - INDICES (IFE-A, ISP, PSG, IED, IGP, IOC, IET, ICODS): H73_OUTPUT_API · verificado
  - ICGIT_Q1_2026 score/historico: H73_OUTPUT_API · verificado
  - PARROQUIAS nbi: H99_ENGINE_CORE col NBI_Pct · INEC Censo 2022
  - PARROQUIAS agua: H99_ENGINE_CORE col Cobertura_Agua_Pct · PDOT diagnóstico INEC 2022
  - PARROQUIAS habitantes: H99_ENGINE_CORE col Población_2022 · INEC Censo 2022
  - PARROQUIAS inversion/per_capita: H99_ENGINE_CORE col Inv_Total_Q1/Inv_PerCapita_Q1_2026
    (eSIGEF corte 2026-04-30)
  - PARROQUIAS tps: Tasa de Pobreza por Servicios · fuente INEC/PDOT diagnóstico oficial
    (campo separado de H99 · pendiente vinculación directa H99)
  - PARROQUIAS participacion.estado/actas/fichas_pp2026: "INFORME PP 2026 GAD Montecristi.pdf"
    (6 talleres ago-2025, 149 fichas, 7/7 parroquias, ACTA N°007-2025-JLAC-JPC-GADMCM)
  - PP_2024: "GAD Montecristi Informe Presupuesto Participativo 2024.pdf" (40 pp)
  - PP_2025: "GAD Montecristi Informe Presupuesto Participativo 2025.pdf" (124 pp)
  - PARROQUIAS participacion.presupuesto: sin asignación oficial per-parroquia en PDF → 0
  - IGM-A,B,C,F en p19_genero: sin dato oficial → 'Sin dato oficial'
  - ODS5_TARGETS avance en p19_genero: sin medición oficial → N/D

⚠ CORRECCIONES APLICADAS 2026-05-15 (auditoría vs Gold Master v4.1):
  - Aníbal San Andrés: nbi 61.7→52.1%, agua 28.9→67.01%, hab 3100→5200, inv 190K→301.6K
  - Colorado: nbi 58.4→58.7%, agua 34.7→38.82%, hab 2230→3800, inv 210K→121.6K, pc 94→32
  - La Pila: nbi 52.8→55.9%, agua 51.2→50%, hab 4100→4600, inv 380K→239.2K, pc 93→52
  - Eloy Alfaro: nbi 45.1→49.8%, agua 62.1→100%, hab 12800→6300, inv 980K→447.3K, pc 77→71
  - Leónidas Plaza: nbi 41.3→54.3%, agua 68.4→100%, hab 8200→4100, inv 720K→196.8K, pc 88→48
  - Montecristi: nbi 38.2→38.4%, agua 78.3→95%, hab 28400→39800, inv 3.2M→8.6M, pc 113→217
  - Isabel Muentes: hab 3488→5700, inv 140K→228K (nbi/agua/pc sin cambio)
  - ICODS: 87.50→91.42% (Excelencia Gobernanza · H20_ICODS Ref_2025)
  - IET nota actualizada con per_cápita correcto ($40 vs $217 cabecera)
"""

# ── ICGI-T GLOBAL ─────────────────────────────────────────────────────────────
ICGIT_Q1_2026 = {
    "score":          53.56,
    "avep":           "Transición Crítica",
    "avep_emoji":     "🟡",
    "corte":          "Q1-2026 · solo marzo",
    "ti_raw":         23.75,           # % inversión ejecutada Q1 · H73_ICPI_ACUMULADO_Q1≈23.67%
    "ti_norm":        70.0,            # % ritmo normalizado para mayo (proyección interna)
    "proyeccion":     65.77,           # PROYECCIÓN cierre 2026 — no es dato oficial
    "meta_mandato":   70.0,            # umbral AVEP "Gestión por Mandato" (H01_PARÁMETROS)
    "meta_pdot_2027": 65.0,            # meta ICGI-T PDOT 2027 · H73 ICPI_META_PDOT=65
    "historico": {
        "2023": 57.36,                 # H73_ICPI_2023 · verificado
        "2024": 67.12,                 # H73_ICPI_2024 · verificado
        "2025": 69.93,                 # H73_ICPI_2025 · verificado
        "2026_q1": 53.56,              # H73_ICPI_GLOBAL_PCT · verificado
        "2026_proj": 65.77,            # PROYECCIÓN — no es dato oficial H73
    },
    "presupuesto_total": 26_689_147,   # pendiente validación vs H73 GAD_CODIFICADO_2026=45.97M
    "inversion_ejecutada": 7_820_000,  # pendiente validación vs H73 GAD_DEVENGADO_Q1=5.15M
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
        "nota":   "Isabel Muentes $40/hab vs cabecera $217/hab · brecha 5.4x · H99 Q1-2026",
    },
    "ICODS": {
        "nombre": "Cumplimiento ODS",
        "valor":  91.42,               # H20_ICODS Ref_2025=0.9142 · auditado 2026-05-15
        "avep":   "Excelencia en Gobernanza",
        "emoji":  "🔵",
        "color":  "#3182CE",
        "estado": "Referencia 2025",
        "nota":   "25 metas PDOT vinculadas · 14 ODS cubiertos · H20_ICODS",
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
        # H99 P-06 · auditado 2026-05-15 · todos los campos nbi/agua/hab/inv/pc son H99 exactos
        "nombre": "Isabel Muentes",
        "tps": 77.94,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 61.2,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 1.02,                  # H99_ENGINE_CORE Cobertura_Agua_Pct
        "inversion": 228_000,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 5_700,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 40,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 228000/5700
        "estado": "EMERGENCIA",
        "color": "#E53E3E",
        "emoji": "🚨",
        # PP 2026: Taller 3 (07-ago-2025) · Antigua Escuela Sucre · ACTA N°003-2025
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        # H99 P-02 · auditado 2026-05-15 · corrección crítica: nbi 61.7→52.1, agua 28.9→67.01
        "nombre": "Aníbal San Andrés",
        "tps": 62.34,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 52.1,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 67.01,                 # H99_ENGINE_CORE Cobertura_Agua_Pct
        "inversion": 301_600,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 5_200,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 58,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 301600/5200
        "estado": "ALERTA",
        "color": "#E67E22",
        "emoji": "🟠",
        # PP 2026: Taller 2 (06-ago-2025) · Auditorium GAD · ACTA N°002-2025
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        # H99 P-03 · auditado 2026-05-15 · corrección: agua 34.7→38.82, hab 2230→3800, inv/pc
        "nombre": "Colorado",
        "tps": 58.67,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 58.7,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 38.82,                 # H99_ENGINE_CORE Cobertura_Agua_Pct
        "inversion": 121_600,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 3_800,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 32,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 121600/3800
        "estado": "ALERTA",
        "color": "#E67E22",
        "emoji": "🟠",
        # PP 2026: Taller 5 (08-ago-2025) · Auditorio GAD · ACTA N°005-2025 · 18 fichas (Colorado+El Arroyo+Los Corrales)
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 18},
    },
    {
        # H99 P-07 · auditado 2026-05-15 · corrección: nbi 52.8→55.9, hab 4100→4600, inv/pc
        "nombre": "La Pila",
        "tps": 41.23,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 55.9,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 50.0,                  # H99_ENGINE_CORE Cobertura_Agua_Pct
        "inversion": 239_200,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 4_600,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 52,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 239200/4600
        "estado": "ALERTA",            # actualizado: NBI 55.9% supera umbral 50% crítico
        "color": "#E67E22",
        "emoji": "🟠",
        # PP 2026: Taller 4 (07-ago-2025) · GAD La Pila · ACTA N°004-2025 · 10 fichas (La Pila+Cda Virgen del Pilar+Las Lagunas+Aguas Nuevas)
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 10},
    },
    {
        # H99 P-05 "Gral. Alfaro" · auditado 2026-05-15 · corrección: agua 62.1→100, hab 12800→6300
        "nombre": "Eloy Alfaro",
        "tps": 31.18,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 49.8,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 100.0,                 # H99_ENGINE_CORE Cobertura_Agua_Pct (cobertura total)
        "inversion": 447_300,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 6_300,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 71,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 447300/6300
        "estado": "NORMAL",
        "color": "#D69E2E",
        "emoji": "🟡",
        # PP 2026: Taller 3 (07-ago-2025) · Antigua Escuela Sucre · ACTA N°003-2025
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 14},
    },
    {
        # H99 P-04 "Leónidas Proaño" · auditado 2026-05-15 · corrección crítica: nbi 41.3→54.3
        # Nombre oficial parroquia: Leónidas Plaza Gutiérrez (H99 usa "Proaño" — error tipográfico)
        "nombre": "Leónidas Plaza",
        "tps": 28.76,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 54.3,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 100.0,                 # H99_ENGINE_CORE Cobertura_Agua_Pct (cobertura total)
        "inversion": 196_800,          # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 4_100,           # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 48,              # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 196800/4100
        "estado": "ALERTA",            # actualizado: NBI 54.3% supera umbral 50% crítico
        "color": "#E67E22",
        "emoji": "🟠",
        # PP 2026: Taller 6 (08-ago-2025) · CDC Leónidas Proaño · ACTA N°006-2025 · 25 fichas
        "participacion": {"mesas": 1, "presupuesto": 0, "actas": 1, "estado": "Activo", "fichas_pp2026": 25},
    },
    {
        # H99 P-01 · auditado 2026-05-15 · corrección: agua 78.3→95, hab 28400→39800, inv/pc
        "nombre": "Montecristi (cabecera)",
        "tps": 22.45,                  # INEC/PDOT diagnóstico oficial · pendiente H99
        "nbi": 38.4,                   # H99_ENGINE_CORE NBI_Pct · INEC Censo 2022
        "agua": 95.0,                  # H99_ENGINE_CORE Cobertura_Agua_Pct
        "inversion": 8_636_600,        # H99_ENGINE_CORE Inv_Total_Q1 · eSIGEF 2026-04-30
        "habitantes": 39_800,          # H99_ENGINE_CORE Población_2022 · INEC Censo 2022
        "per_capita": 217,             # H99_ENGINE_CORE Inv_PerCapita_Q1_2026 = 8636600/39800
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
