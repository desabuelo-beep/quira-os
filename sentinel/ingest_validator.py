"""
SENTINEL RAG · ingest_validator.py — Sprint 1.7
Pipeline de validación documental — la puerta de entrada al KB institucional.

Cada documento debe pasar por este pipeline antes de llegar a ChromaDB:

  Upload / Archivo
       ↓
  Extracción de texto  (ocr_quality.py)
       ↓
  Scoring de calidad   (ocr_quality.py)
       ↓
  Clasificación tipo   (document_classifier.py)
       ↓
  5 Guardrails         (este módulo)
       ↓
  Indexación           (ingest_kb.py) — SOLO si pasa

Guardrails:
  G1. Texto extraído ≥ 500 caracteres
  G2. Entidad institucional detectada
  G3. Fecha detectada
  G4. Tipo documental identificado (no DESCONOCIDO)
  G5. Score calidad textual ≥ 80%

Estados:
  APROBADO:              5/5 guardrails → listo para ChromaDB
  ADVERTENCIA:           4/5 guardrails → ingestar con flag de advertencia
  REQUIERE REVISIÓN:     2-3/5 guardrails → NO ingestar, revisión humana
  RECHAZADO:             0-1/5 guardrails → NO ingestar

"La basura entra, basura sale." — colega, 2026

Dylus Lab © 2026
"""
from __future__ import annotations
import re
import sys
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.ocr_quality import (
    extract_text_from_file, score_text_quality,
    DATE_PATTERNS, OcrQualityResult,
)
from sentinel.document_classifier import (
    classify_document, TipoDocumento, ClassificationResult,
)

# ── PATRONES DE ENTIDAD INSTITUCIONAL ─────────────────────────────────────────
ENTITY_PATTERNS = [
    r"gad\s+municipal",
    r"municipio\s+de\s+montecristi",
    r"gad\s+montecristi",
    r"gobierno\s+aut[oó]nomo\s+descentralizado",
    r"gobierno\s+local",
    r"alcald[iía]a",
    r"municipalidad",
    r"concejo\s+municipal",
    r"direcci[oó]n\s+de\s+planificaci[oó]n",
    r"direcci[oó]n\s+financiera",
    r"secretar[iía]a\s+general",
    r"ecuador",
    r"ministerio\s+de",
    r"secretar[iía]a\s+nacional",
    r"senplades",
    r"sercop",
    r"contralor[iía]a",
]

# ── ESTADOS ───────────────────────────────────────────────────────────────────
class ValidationState(str, Enum):
    APROBADO         = "APROBADO"
    ADVERTENCIA      = "ADVERTENCIA"
    REQUIERE_REVISION = "REQUIERE REVISIÓN HUMANA"
    RECHAZADO        = "RECHAZADO"


# ── DATACLASSES ───────────────────────────────────────────────────────────────
@dataclass
class GuardrailDoc:
    codigo:  str    # "G1" .. "G5"
    nombre:  str
    pasó:    bool
    detalle: str    # resultado específico (ej: "1,240 caracteres extraídos")


@dataclass
class ValidationResult:
    # Estado final
    estado:            ValidationState
    puede_ingestar:    bool

    # Guardrails
    guardrails:        list[GuardrailDoc]
    guardrails_pasados: int
    guardrails_total:  int

    # Clasificación
    tipo_documento:    str   # TipoDocumento.value
    dims_tgi:          list[str]
    confianza_tipo:    str

    # Calidad textual
    ocr_score:         float
    char_count:        int
    word_count:        int
    extraction_method: str

    # Metadata institucional detectada
    fecha_detectada:   str
    entidad_detectada: str
    filename:          str

    # Veredicto
    motivo_rechazo:    str
    accion_sugerida:   str
    nivel_riesgo:      str   # "🟢 Ninguno" | "🟡 Medio" | "🔴 Alto"

    # Para ChromaDB (solo si puede_ingestar)
    metadata_chroma:   dict = field(default_factory=dict)


# ── DETECCIÓN DE ENTIDAD ──────────────────────────────────────────────────────
def _detect_entity(text: str) -> str:
    """Detecta la entidad institucional en el texto."""
    text_lower = text.lower()

    # Montecristi primero (más específico)
    if "montecristi" in text_lower:
        if "gad" in text_lower or "municipio" in text_lower or "municipal" in text_lower:
            return "GAD Municipal de Montecristi"
        return "Montecristi (entidad no especificada)"

    # Patterns genéricos
    for pattern in ENTITY_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            # Extraer contexto alrededor del match (30 chars)
            start = max(0, match.start() - 5)
            end   = min(len(text), match.end() + 30)
            return text[start:end].strip().rstrip(",;:")

    return ""


def _detect_dates(text: str) -> list[str]:
    """Detecta fechas en el texto (máximo 5)."""
    text_lower = text.lower()
    found: list[str] = []
    for dp in DATE_PATTERNS:
        for m in re.finditer(dp, text_lower):
            date_str = m.group(0).strip()
            if date_str not in found:
                found.append(date_str)
    return found[:5]


# ── PIPELINE PRINCIPAL ────────────────────────────────────────────────────────
def validate_document(
    filepath: Path | str | None = None,
    text:     str = "",
    filename: str = "",
) -> ValidationResult:
    """
    Pipeline completo de validación documental.

    Acepta:
      - filepath: ruta a archivo (extrae texto automáticamente)
      - text: texto ya extraído (directo)
      - filename: nombre del archivo (para clasificación y metadata)

    Retorna ValidationResult con estado, guardrails y metadata para ChromaDB.
    """
    # ── 1. Extraer texto ──────────────────────────────────────────────────────
    extraction_method = "direct"

    if filepath is not None:
        fp = Path(filepath)
        filename = filename or fp.name
        if not text:
            text, extraction_method = extract_text_from_file(fp)
    else:
        fp = None

    # ── 2. Scoring de calidad OCR ─────────────────────────────────────────────
    ocr: OcrQualityResult = score_text_quality(text, filename)
    ocr.extraction_method = extraction_method

    # ── 3. Clasificación documental ───────────────────────────────────────────
    cls: ClassificationResult = classify_document(text, filename)

    # ── 4. Detección de metadata institucional ────────────────────────────────
    dates  = _detect_dates(text)
    entity = _detect_entity(text)

    # ── 5. Aplicar los 5 guardrails ───────────────────────────────────────────
    guardrails = [
        GuardrailDoc(
            "G1", "Texto extraído ≥ 500 caracteres",
            len(text) >= 500,
            f"{len(text):,} caracteres extraídos"
            if text else "Texto vacío — posible error de extracción",
        ),
        GuardrailDoc(
            "G2", "Entidad institucional detectada",
            bool(entity),
            f"Entidad: {entity[:80]}" if entity
            else "No se detectó referencia a entidad pública",
        ),
        GuardrailDoc(
            "G3", "Fecha detectada",
            bool(dates),
            f"Fecha: {dates[0]}" if dates
            else "No se detectó fecha — verificar si el documento está fechado",
        ),
        GuardrailDoc(
            "G4", "Tipo documental identificado",
            cls.tipo != TipoDocumento.DESCONOCIDO,
            f"Tipo: {cls.tipo.value} (confianza: {cls.confianza})"
            if cls.tipo != TipoDocumento.DESCONOCIDO
            else "Tipo DESCONOCIDO — el sistema no reconoce el formato",
        ),
        GuardrailDoc(
            "G5", "Score calidad textual ≥ 80%",
            ocr.score >= 80,
            f"Score: {ocr.score:.0f}%  {ocr.nivel}"
            + (f" — artefactos OCR: {ocr.artifacts_count}" if ocr.artifacts_count > 0 else ""),
        ),
    ]

    pasados = sum(1 for g in guardrails if g.pasó)

    # ── 6. Determinar estado ──────────────────────────────────────────────────
    if pasados == 5:
        estado        = ValidationState.APROBADO
        puede_ingestar = True
        nivel_riesgo  = "🟢 Ninguno"
    elif pasados == 4:
        estado        = ValidationState.ADVERTENCIA
        puede_ingestar = True
        nivel_riesgo  = "🟡 Medio"
    elif pasados >= 2:
        estado        = ValidationState.REQUIERE_REVISION
        puede_ingestar = False
        nivel_riesgo  = "🔴 Alto"
    else:
        estado        = ValidationState.RECHAZADO
        puede_ingestar = False
        nivel_riesgo  = "🔴 Alto"

    # ── 7. Motivo y acción ────────────────────────────────────────────────────
    failed = [g for g in guardrails if not g.pasó]

    if estado == ValidationState.APROBADO:
        motivo  = ""
        accion  = (
            f"Documento listo para indexación. "
            f"Tipo: {cls.tipo.value} · Dims TGI: {', '.join(cls.dims_tgi) or 'general'}"
        )
    elif estado == ValidationState.ADVERTENCIA:
        g_f = failed[0]
        motivo  = f"{g_f.codigo} falló: {g_f.detalle}"
        accion  = (
            "Ingestar con advertencia — revisar el guardrail fallido. "
            "El documento quedará marcado como 'requiere verificación'."
        )
    elif estado == ValidationState.REQUIERE_REVISION:
        motivos = " | ".join(f"{g.codigo}: {g.detalle}" for g in failed)
        motivo  = f"Guardrails fallidos: {motivos}"
        accion  = (
            "REQUIERE REVISIÓN HUMANA — no ingestar sin validación manual. "
            "Posibles causas: formato incompleto, sin metadatos, o extracción deficiente."
        )
    else:
        codes   = ", ".join(g.codigo for g in failed)
        motivo  = f"Rechazado ({pasados}/5 guardrails): falló {codes}"
        accion  = (
            "RECHAZAR — documento incompleto o ilegible. No ingestar. "
            "Verificar: (1) el documento no está vacío, "
            "(2) el OCR fue ejecutado si es escaneado, "
            "(3) el formato es compatible."
        )

    # ── 8. Metadata para ChromaDB ─────────────────────────────────────────────
    metadata_chroma = {}
    if puede_ingestar:
        metadata_chroma = {
            "tipo_nota":        cls.tipo.value.lower().replace("_", "-"),
            "fuente_tipo":      "vivo",      # POA/PAC/informes = "vivo"
            "dimension_tgi":    " | ".join(cls.dims_tgi) if cls.dims_tgi else "general",
            "fecha":            dates[0] if dates else datetime.now().strftime("%Y-%m-%d"),
            "entidad":          entity[:100] if entity else "GAD-MNT",
            "canton":           "Montecristi",
            "estado":           "activo",
            "ocr_score":        str(round(ocr.score, 1)),
            "char_count":       str(len(text)),
            "validation_state": estado.value,
            "filename":         filename,
            "index_version":    datetime.now().strftime("%Y-%m-%d-01"),
        }

    return ValidationResult(
        estado             = estado,
        puede_ingestar     = puede_ingestar,
        guardrails         = guardrails,
        guardrails_pasados = pasados,
        guardrails_total   = len(guardrails),
        tipo_documento     = cls.tipo.value,
        dims_tgi           = cls.dims_tgi,
        confianza_tipo     = cls.confianza,
        ocr_score          = ocr.score,
        char_count         = len(text),
        word_count         = ocr.word_count,
        extraction_method  = extraction_method,
        fecha_detectada    = dates[0] if dates else "",
        entidad_detectada  = entity,
        filename           = filename,
        motivo_rechazo     = motivo,
        accion_sugerida    = accion,
        nivel_riesgo       = nivel_riesgo,
        metadata_chroma    = metadata_chroma,
    )


# ── FORMATEO ──────────────────────────────────────────────────────────────────
_ESTADO_ICON = {
    ValidationState.APROBADO:         "🟢",
    ValidationState.ADVERTENCIA:      "🟡",
    ValidationState.REQUIERE_REVISION: "🟡",
    ValidationState.RECHAZADO:        "🔴",
}


def format_validation(r: ValidationResult) -> str:
    """Formatea ValidationResult para display en consola / log."""
    sep  = "═" * 64
    dash = "─" * 64
    icon = _ESTADO_ICON.get(r.estado, "❓")

    lines = [
        sep,
        "  SENTINEL · Validador Documental — Sprint 1.7",
        "  Dylus Lab © 2026",
        sep,
        f"  Archivo:  {r.filename or '(texto directo)'}",
        f"  Estado:   {icon} {r.estado.value}  ·  Riesgo: {r.nivel_riesgo}",
        f"  Guardrails pasados: {r.guardrails_pasados}/{r.guardrails_total}",
        dash,
        "  Guardrails:",
    ]

    for g in r.guardrails:
        ok = "✅" if g.pasó else "❌"
        lines.append(f"    {ok} {g.codigo}. {g.nombre}")
        lines.append(f"       → {g.detalle}")

    lines += [
        dash,
        f"  Tipo documental:  {r.tipo_documento}  (confianza: {r.confianza_tipo})",
        f"  Dims TGI:         {', '.join(r.dims_tgi) if r.dims_tgi else 'N/A'}",
        f"  Score calidad:    {r.ocr_score:.0f}%",
        f"  Caracteres:       {r.char_count:,}  ·  Palabras: {r.word_count:,}",
        f"  Extracción:       {r.extraction_method}",
        f"  Fecha detectada:  {r.fecha_detectada or 'no encontrada'}",
        f"  Entidad:          {r.entidad_detectada[:60] or 'no detectada'}",
        dash,
    ]

    if r.motivo_rechazo:
        lines.append(f"  ⚠️  {r.motivo_rechazo}")
        lines.append(dash)

    lines.append(f"  → {r.accion_sugerida}")
    lines.append(sep)

    return "\n".join(lines)


def to_dict(r: ValidationResult) -> dict:
    """JSON-serializable para API."""
    return {
        "timestamp":          datetime.now().isoformat(),
        "filename":           r.filename,
        "estado":             r.estado.value,
        "puede_ingestar":     r.puede_ingestar,
        "nivel_riesgo":       r.nivel_riesgo,
        "guardrails_pasados": r.guardrails_pasados,
        "guardrails_total":   r.guardrails_total,
        "guardrails": [
            {"codigo": g.codigo, "nombre": g.nombre, "pasó": g.pasó, "detalle": g.detalle}
            for g in r.guardrails
        ],
        "clasificacion": {
            "tipo":       r.tipo_documento,
            "confianza":  r.confianza_tipo,
            "dims_tgi":   r.dims_tgi,
        },
        "calidad": {
            "ocr_score":         r.ocr_score,
            "char_count":        r.char_count,
            "word_count":        r.word_count,
            "extraction_method": r.extraction_method,
        },
        "metadata_detectada": {
            "fecha":   r.fecha_detectada,
            "entidad": r.entidad_detectada,
        },
        "motivo_rechazo":  r.motivo_rechazo,
        "accion_sugerida": r.accion_sugerida,
        "metadata_chroma": r.metadata_chroma,
    }


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validador documental Sentinel — Sprint 1.7"
    )
    parser.add_argument(
        "target", nargs="?",
        help="Ruta al archivo a validar, o texto directo"
    )
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--save", action="store_true", help="Guardar reporte en reports/")
    args = parser.parse_args()

    target = args.target or ""
    p = Path(target) if target else None

    if p and p.exists():
        result = validate_document(filepath=p)
    elif target:
        result = validate_document(text=target, filename="texto_directo.txt")
    else:
        # Demo con texto institucional de ejemplo
        DEMO = """
        GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DE MONTECRISTI
        Plan Operativo Anual — Ejercicio Fiscal 2026
        Fecha: 15 de enero de 2026

        El presente Plan Operativo Anual ha sido elaborado en cumplimiento
        de la normativa establecida en el COOTAD y el COPFP, articulando
        las actividades operativas con las metas financieras y físicas
        del Gobierno Municipal de Montecristi para el período 2026.

        Las actividades programadas responden a los objetivos estratégicos
        del PDOT cantonal, con énfasis en la reducción de brechas de equidad
        territorial entre parroquias urbanas y rurales del cantón.
        """
        result = validate_document(text=DEMO, filename="POA_2026_demo.txt")
        print("  [Demo — usando texto institucional de ejemplo]\n")

    if args.json:
        print(json.dumps(to_dict(result), ensure_ascii=False, indent=2))
    else:
        print(format_validation(result))

    if args.save:
        report_dir = Path(__file__).parent / "reports"
        report_dir.mkdir(exist_ok=True)
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = report_dir / f"validation_{ts}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(to_dict(result), f, ensure_ascii=False, indent=2)
        print(f"\n  Guardado: {out}")
