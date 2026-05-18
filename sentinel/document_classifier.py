"""
SENTINEL RAG · document_classifier.py — Sprint 1.7
Clasificación documental institucional — identifica el tipo de documento
antes de indexarlo en ChromaDB.

Tipos soportados:
  POA              Plan Operativo Anual
  PAC              Plan Anual de Contratación
  PRESUPUESTO      Cédula / Proforma Presupuestaria
  INFORME_MENSUAL  Informes de avance y cumplimiento
  CONVENIO         Convenios interinstitucionales
  REFORMA          Reformas y traspasos presupuestarios
  NORMATIVA        Ordenanzas, resoluciones, decretos
  PDOT             Plan de Desarrollo y Ordenamiento Territorial
  RENDICION        Rendición de Cuentas
  DESCONOCIDO      No identificado — requiere revisión humana

Método: scoring por keywords primarias (peso=3) + secundarias (peso=1) + filename hints (peso=2).
Umbral de confianza ALTA: score >= 9 (≈ 3 matches primarias).

Extensible: agregar tipos en TIPO_KEYWORDS sin modificar el motor.

Dylus Lab © 2026
"""
from __future__ import annotations
import re
import sys
from dataclasses import dataclass
from enum import Enum

sys.stdout.reconfigure(encoding="utf-8")

# ── TIPOS DOCUMENTALES ────────────────────────────────────────────────────────
class TipoDocumento(str, Enum):
    POA         = "POA"
    PAC         = "PAC"
    PRESUPUESTO = "PRESUPUESTO"
    INFORME     = "INFORME_MENSUAL"
    CONVENIO    = "CONVENIO"
    REFORMA     = "REFORMA_PRESUPUESTARIA"
    NORMATIVA   = "NORMATIVA"
    PDOT        = "PDOT"
    RENDICION   = "RENDICION_CUENTAS"
    DESCONOCIDO = "DESCONOCIDO"

# Dimensiones TGI que predominan en cada tipo
TIPO_A_DIM_TGI: dict[TipoDocumento, list[str]] = {
    TipoDocumento.POA:         ["D2", "D3"],
    TipoDocumento.PAC:         ["D1", "D3"],
    TipoDocumento.PRESUPUESTO: ["D2", "D3"],
    TipoDocumento.INFORME:     ["D2", "D3"],
    TipoDocumento.CONVENIO:    ["D2", "D3"],
    TipoDocumento.REFORMA:     ["D2", "D3"],
    TipoDocumento.NORMATIVA:   ["D1"],
    TipoDocumento.PDOT:        ["D2", "D4"],
    TipoDocumento.RENDICION:   ["D1", "D5"],
    TipoDocumento.DESCONOCIDO: [],
}

# ── KEYWORDS POR TIPO ─────────────────────────────────────────────────────────
# primary: peso=3 — muy específico del tipo
# secondary: peso=1 — genérico pero relevante
# filename: peso=2 — hinting por nombre de archivo
TIPO_KEYWORDS: dict[TipoDocumento, dict[str, list[str]]] = {

    TipoDocumento.POA: {
        "primary": [
            "plan operativo anual", "poa ", "p.o.a",
            "actividad operativa", "meta física", "meta financiera",
            "programación de actividades", "plan de trabajo anual",
        ],
        "secondary": [
            "actividades", "metas", "cronograma de actividades",
            "presupuesto asignado", "responsable de actividad",
            "indicadores de cumplimiento", "trimestre",
        ],
        "filename": ["poa", "plan_operativo", "operativo_anual", "plan-operativo"],
    },

    TipoDocumento.PAC: {
        "primary": [
            "plan anual de contratación", "pac ", "p.a.c",
            "proceso de contratación", "sercop", "portal de compras",
            "catálogo electrónico", "subasta inversa",
        ],
        "secondary": [
            "contratación pública", "compra pública",
            "proceso", "licitación", "concurso público",
            "menor cuantía", "ínfima cuantía",
        ],
        "filename": ["pac", "plan_anual_contratacion", "contratacion", "pac_"],
    },

    TipoDocumento.PRESUPUESTO: {
        "primary": [
            "cédula presupuestaria", "proforma presupuestaria",
            "esigef", "devengado", "codificado",
            "comprometido", "pagado", "partida presupuestaria",
        ],
        "secondary": [
            "asignación inicial", "reformas presupuestarias",
            "grupo de gasto", "subgrupo", "ítem",
            "ingresos", "gastos corrientes", "gastos de inversión",
        ],
        "filename": ["presupuesto", "cedula", "proforma", "esigef", "cedula_presupuestaria"],
    },

    TipoDocumento.INFORME: {
        "primary": [
            "informe mensual", "informe de avance",
            "avance de cumplimiento", "reporte mensual de gestión",
            "informe trimestral", "porcentaje de cumplimiento",
        ],
        "secondary": [
            "observaciones", "período reportado",
            "meta programada", "meta ejecutada",
            "desviación", "semáforo",
        ],
        "filename": ["informe", "avance", "reporte", "mensual", "trimestral"],
    },

    TipoDocumento.CONVENIO: {
        "primary": [
            "convenio de cooperación", "convenio interinstitucional",
            "convenio marco", "convenio específico",
            "contraparte", "cooperante", "monto del convenio",
            "acuerdo de cooperación",
        ],
        "secondary": [
            "vigencia", "cláusula", "objeto del convenio",
            "obligaciones de las partes", "plazo de ejecución",
            "desembolsos", "contrapartida",
        ],
        "filename": ["convenio", "cooperacion", "acuerdo", "mou", "agreement"],
    },

    TipoDocumento.REFORMA: {
        "primary": [
            "reforma presupuestaria", "traspaso de crédito",
            "modificación presupuestaria", "incremento presupuestario",
            "reducción presupuestaria",
        ],
        "secondary": [
            "reforma", "traspaso", "reasignación",
            "justificación de la reforma", "partida origen",
            "partida destino",
        ],
        "filename": ["reforma", "traspaso", "modificacion", "reforma_presupuestaria"],
    },

    TipoDocumento.NORMATIVA: {
        "primary": [
            "ordenanza municipal", "resolución administrativa",
            "decreto alcaldicio", "reglamento interno",
            "ordenanza que reglamenta", "el concejo municipal",
        ],
        "secondary": [
            "considerando", "resuelve", "artículo primero",
            "disposición general", "disposición transitoria",
            "vigencia", "promulgación", "registro oficial",
        ],
        "filename": ["ordenanza", "resolucion", "decreto", "reglamento", "normativa"],
    },

    TipoDocumento.PDOT: {
        "primary": [
            "plan de desarrollo y ordenamiento territorial",
            "pdot", "objetivos estratégicos del pdot",
            "modelo de gestión territorial", "diagnóstico territorial",
            "propuesta de desarrollo",
        ],
        "secondary": [
            "visión territorial", "indicadores de gestión",
            "competencias", "programas y proyectos",
            "articulación territorial",
        ],
        "filename": ["pdot", "plan_desarrollo", "ordenamiento", "desarrollo_territorial"],
    },

    TipoDocumento.RENDICION: {
        "primary": [
            "rendición de cuentas", "informe de gestión anual",
            "participación ciudadana", "informe al concejo",
            "logros de gestión",
        ],
        "secondary": [
            "ciudadanía", "obras realizadas", "inversión ejecutada",
            "resultados del período", "evaluación de gestión",
        ],
        "filename": ["rendicion", "cuentas", "gestion_anual", "informe_anual"],
    },
}

# Umbral mínimo de score para no ser DESCONOCIDO
SCORE_MIN_CONOCIDO  = 4    # al menos 1 match primario + algo
SCORE_ALTA_CONFIANZA = 9   # 3 matches primarios = alta confianza


# ── RESULTADO ─────────────────────────────────────────────────────────────────
@dataclass
class ClassificationResult:
    tipo:              TipoDocumento
    score:             float        # 0-100 normalizado
    score_raw:         int          # puntos brutos
    matches_primary:   int
    matches_secondary: int
    filename_hint:     str          # tipo sugerido por el nombre del archivo
    confianza:         str          # "Alta" | "Media" | "Baja" | "Ninguna"
    dims_tgi:          list[str]    # dimensiones TGI que este tipo afecta
    keywords_found:    list[str]    # keywords que matchearon


# ── MOTOR DE CLASIFICACIÓN ────────────────────────────────────────────────────
def classify_document(text: str, filename: str = "") -> ClassificationResult:
    """
    Clasifica el tipo de documento usando keyword scoring.

    Retorna ClassificationResult con el tipo más probable.
    Si el score es muy bajo → TipoDocumento.DESCONOCIDO
    """
    text_lower    = text.lower()
    filename_lower = Path_stem_lower(filename)

    scores: dict[TipoDocumento, dict] = {}

    for tipo, kw in TIPO_KEYWORDS.items():
        primary_hits   = []
        secondary_hits = []
        filename_hits  = []

        for kw_p in kw.get("primary", []):
            if kw_p.lower() in text_lower:
                primary_hits.append(kw_p)

        for kw_s in kw.get("secondary", []):
            if kw_s.lower() in text_lower:
                secondary_hits.append(kw_s)

        for kw_f in kw.get("filename", []):
            if kw_f.lower() in filename_lower:
                filename_hits.append(kw_f)

        raw_score = (
            len(primary_hits)   * 3 +
            len(secondary_hits) * 1 +
            len(filename_hits)  * 2
        )

        scores[tipo] = {
            "raw":       raw_score,
            "primary":   primary_hits,
            "secondary": secondary_hits,
            "filename":  filename_hits,
        }

    # Tipo ganador
    best_tipo = max(scores.keys(), key=lambda t: scores[t]["raw"])
    best      = scores[best_tipo]
    best_raw  = best["raw"]

    # Hinting por filename independiente
    filename_hint = _hint_from_filename(filename_lower)

    # Determinar confianza
    if best_raw == 0 or best_raw < SCORE_MIN_CONOCIDO:
        tipo_final = TipoDocumento.DESCONOCIDO
        confianza  = "Ninguna"
        score_norm = 0.0
    else:
        tipo_final = best_tipo
        if best_raw >= SCORE_ALTA_CONFIANZA:
            confianza = "Alta"
        elif best_raw >= SCORE_MIN_CONOCIDO + 3:
            confianza = "Media"
        else:
            confianza = "Baja"
        # Normalizar a 0-100 (asumiendo max raw ≈ 30)
        score_norm = round(min(best_raw / 30 * 100, 100.0), 1)

    keywords_found = best["primary"] + best["secondary"] + best["filename"]

    return ClassificationResult(
        tipo             = tipo_final,
        score            = score_norm,
        score_raw        = best_raw,
        matches_primary  = len(best["primary"]),
        matches_secondary= len(best["secondary"]),
        filename_hint    = filename_hint,
        confianza        = confianza,
        dims_tgi         = TIPO_A_DIM_TGI.get(tipo_final, []),
        keywords_found   = keywords_found[:8],  # máximo 8 para display
    )


def _hint_from_filename(name: str) -> str:
    """Sugiere tipo a partir del nombre del archivo."""
    hints = {
        "poa": "POA",
        "pac": "PAC",
        "presupuesto": "PRESUPUESTO",
        "cedula": "PRESUPUESTO",
        "convenio": "CONVENIO",
        "ordenanza": "NORMATIVA",
        "informe": "INFORME_MENSUAL",
        "reforma": "REFORMA_PRESUPUESTARIA",
        "pdot": "PDOT",
        "rendicion": "RENDICION_CUENTAS",
    }
    for key, tipo_str in hints.items():
        if key in name:
            return tipo_str
    return ""


def Path_stem_lower(filename: str) -> str:
    """Extrae stem del filename en lowercase para matching."""
    if not filename:
        return ""
    from pathlib import Path
    try:
        return Path(filename).stem.lower().replace("-", "_").replace(" ", "_")
    except Exception:
        return filename.lower()


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python -m sentinel.document_classifier <archivo_o_texto>")
        sys.exit(1)

    from pathlib import Path
    from sentinel.ocr_quality import extract_text_from_file, score_text_quality

    target = sys.argv[1]
    path   = Path(target)
    filename = path.name if path.exists() else target[:50]

    if path.exists():
        text, _ = extract_text_from_file(path)
    else:
        text = target

    result = classify_document(text, filename)

    print(f"\n  Tipo detectado:    {result.tipo.value}")
    print(f"  Confianza:         {result.confianza}")
    print(f"  Score:             {result.score:.0f}%  (raw={result.score_raw})")
    print(f"  Dims TGI:          {result.dims_tgi or 'N/A'}")
    print(f"  Filename hint:     {result.filename_hint or 'ninguno'}")
    print(f"  Matches primarios: {result.matches_primary}")
    print(f"  Matches secundarios:{result.matches_secondary}")
    print(f"  Keywords halladas: {result.keywords_found}")
