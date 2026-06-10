"""
app/fetchers/fondos_normalizer.py — Normalizador Semántico · QUIRA OS
======================================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

Responsabilidad única:
    Convertir FondoRaw (texto libre) → FondoCanonical (schema Supabase).

Por qué Haiku:
    El problema no es scraping — es semántica.
    "Call for Proposals" / "Funding Window" / "Facility" / "Challenge"
    todos significan cosas distintas según el emisor.
    Haiku convierte texto libre a schema canónico sin parser por organización.

Fallback:
    Si Haiku no está disponible (API key faltante), usa extracción
    heurística básica con regexes. Confidence = 0.4 en ese caso.

BLOOMBERG FIREWALL:
    El normalizador NUNCA incluye en su output:
    ICPI · TGI · Ti · QTMP · H73 · Gold Master · node IDs internos.
    Solo produce campos del schema público de fondos_convocatorias.

Pipeline de llamada:
    FondoRaw → normalize_raw_fund() → FondoCanonical
    FondoCanonical → validate_canonical() → (valid, errores)
"""
from __future__ import annotations

import json
import logging
import re
from datetime import date, datetime
from typing import Optional

from app.fetchers.base_adapter import FondoRaw, FondoCanonical

logger = logging.getLogger(__name__)

# ── Configuración Haiku ────────────────────────────────────────────────────────
HAIKU_MODEL   = "claude-haiku-4-5"
MAX_INPUT_CHARS = 8_000   # Máximo texto enviado a Haiku por fondo

# ── Vocabulario canónico ───────────────────────────────────────────────────────
TEMAS_VALIDOS = {
    "gobernanza", "genero", "agua", "democracia", "medioambiente",
    "infraestructura", "participacion", "transparencia", "derechos_humanos",
    "salud", "educacion", "economia", "otros",
    # Sprint B.2-cierre (G-15/G-20/G-23 + clima): 4 vacíos temáticos
    # detectados por las fichas — los fondos existen (CAF/BID/GEF/UE),
    # el radar no los veía.
    "movilidad", "empleo", "juventud", "residuos", "economia_circular",
    "clima", "resiliencia", "riesgo_desastres",
}
ELEGIBLES_VALIDOS = {
    "GAD", "ONG", "OSC", "academia", "empresa", "gobierno_central",
}
ESTADOS_VALIDOS = {"abierta", "cerrada", "recurrente", "borrador"}

# Emisores que ya existen en fondos_emisores (código → busca por código)
EMISORES_CONOCIDOS = {
    "PNUD", "BID", "AECID", "CAF", "BDE", "GEF", "FIDA", "USAID",
    "FORD", "ONU_MUJERES", "ACNUR", "UNICEF", "FAO", "OPS_OMS",
    "WB", "KFW", "SECO", "EMBASSY_USA", "EMBASSY_UE",
    "CAMARA_COMERCIO_GUAYAQUIL", "AME",
}


# ── Prompt de sistema para Haiku ──────────────────────────────────────────────

_SYSTEM_PROMPT = """
Eres un extractor de información sobre convocatorias de financiamiento para
municipios ecuatorianos (GADs). Tu tarea es extraer datos estructurados de
texto libre en formato JSON.

SCHEMA DE SALIDA (JSON estricto):
{
  "nombre": "Nombre oficial de la convocatoria (string, requerido)",
  "emisor_codigo": "Código del emisor (string, requerido, de la lista conocida)",
  "estado": "abierta|cerrada|recurrente (default: abierta)",
  "monto_min_usd": número o null,
  "monto_max_usd": número o null,
  "moneda": "USD (default)",
  "fecha_cierre": "YYYY-MM-DD o null",
  "fecha_inicio": "YYYY-MM-DD o null",
  "elegibles": ["GAD", "ONG", "OSC", "academia", "empresa", "gobierno_central"],
  "temas": ["gobernanza", "genero", "agua", "democracia", "medioambiente",
            "infraestructura", "participacion", "transparencia",
            "derechos_humanos", "salud", "educacion", "economia",
            "movilidad", "empleo", "juventud", "residuos",
            "economia_circular", "clima", "resiliencia",
            "riesgo_desastres", "otros"],
  "descripcion": "Descripción breve (max 300 chars)",
  "url": "URL directa a la convocatoria o null",
  "confidence": número 0.0-1.0,
  "razon_confidence": "Explicación de por qué ese confidence"
}

REGLAS:
1. emisor_codigo debe ser de: PNUD, BID, AECID, CAF, BDE, GEF, FIDA, USAID,
   FORD, ONU_MUJERES, ACNUR, UNICEF, FAO, OPS_OMS, WB, KFW, SECO,
   EMBASSY_USA, EMBASSY_UE, CAMARA_COMERCIO_GUAYAQUIL, AME.
   Si no reconoces el emisor, usa "OTROS" y baja el confidence.
2. Montos: convierte siempre a USD. Si es en otra moneda, convierte aproximado.
   Si dice "hasta USD 500.000" → monto_max_usd: 500000, monto_min_usd: null.
3. Fechas: convierte a formato YYYY-MM-DD. Si no hay fecha: null.
4. temas: usa solo los valores de la lista. Máximo 5 temas.
5. elegibles: si dice "municipios" o "GADs" → "GAD". Si dice "organizaciones
   de la sociedad civil" → "OSC". Si dice "universidades" → "academia".
6. confidence:
   - 0.9-1.0: todos los campos clave presentes y claros
   - 0.7-0.89: nombre+emisor+monto claros, fechas o elegibles dudosos
   - 0.5-0.69: información parcial o ambigua
   - 0.0-0.49: texto insuficiente (no insertar)
7. Si el texto no describe una convocatoria de financiamiento, confidence = 0.0.
8. Responde SOLO con el JSON. Sin texto adicional.
"""


# ── Función principal de normalización ────────────────────────────────────────

def normalize_raw_fund(
    raw: FondoRaw,
    use_haiku: bool = True,
) -> Optional[FondoCanonical]:
    """
    Convierte FondoRaw → FondoCanonical via Haiku (o heurística como fallback).

    Args:
        raw:       Objeto FondoRaw del adaptador
        use_haiku: True para usar Haiku, False para heurística básica

    Returns:
        FondoCanonical con confidence score, o None si el texto no es relevante.
        confidence < 0.5 → retorna None (no insertar).
    """
    # Truncar texto fuente al máximo para Haiku
    texto = (raw.texto_fuente or "")[:MAX_INPUT_CHARS]
    if not texto.strip():
        logger.warning(f"[Normalizer] texto_fuente vacío para fuente {raw.fuente_codigo}")
        return None

    # Enriquecer prompt con metadata pre-extraída del adaptador
    extras = []
    if raw.titulo_raw:       extras.append(f"Título: {raw.titulo_raw}")
    if raw.emisor_raw:       extras.append(f"Emisor: {raw.emisor_raw}")
    if raw.monto_raw:        extras.append(f"Monto: {raw.monto_raw}")
    if raw.fecha_cierre_raw: extras.append(f"Cierre: {raw.fecha_cierre_raw}")
    if raw.temas_raw:        extras.append(f"Temas: {', '.join(raw.temas_raw)}")
    if raw.elegibles_raw:    extras.append(f"Elegibles: {', '.join(raw.elegibles_raw)}")
    if raw.url:              extras.append(f"URL: {raw.url}")

    user_content = "\n".join(extras) + "\n\n---\n\n" + texto if extras else texto

    # ── Intentar con Haiku ────────────────────────────────────────────────────
    extracted = None
    if use_haiku:
        extracted = _call_haiku(user_content, raw.fuente_codigo)

    # ── Fallback heurístico ───────────────────────────────────────────────────
    if extracted is None:
        extracted = _heuristic_extract(raw)
        if extracted:
            extracted["confidence"] = min(extracted.get("confidence", 0.4), 0.4)
            logger.info(f"[Normalizer] Usando fallback heurístico para {raw.url}")

    if not extracted:
        return None

    confidence = float(extracted.get("confidence", 0.0))
    if confidence < 0.5:
        logger.info(
            f"[Normalizer] confidence={confidence:.2f} — descartando "
            f"{extracted.get('nombre', '?')[:60]}"
        )
        return None

    # ── Construir FondoCanonical ──────────────────────────────────────────────
    canonical = FondoCanonical(
        emisor_codigo  = _clean_emisor(extracted.get("emisor_codigo", ""), raw.fuente_codigo),
        nombre         = (extracted.get("nombre") or "")[:200],
        estado         = _clean_estado(extracted.get("estado", "abierta")),
        monto_min_usd  = _to_float(extracted.get("monto_min_usd")),
        monto_max_usd  = _to_float(extracted.get("monto_max_usd")),
        moneda         = extracted.get("moneda", "USD"),
        fecha_cierre   = _to_date(extracted.get("fecha_cierre")),
        fecha_inicio   = _to_date(extracted.get("fecha_inicio")),
        elegibles      = _clean_list(extracted.get("elegibles", []), ELEGIBLES_VALIDOS),
        temas          = _clean_list(extracted.get("temas", []), TEMAS_VALIDOS),
        descripcion    = (extracted.get("descripcion") or "")[:300] or None,
        url            = extracted.get("url") or raw.url,
        confidence     = confidence,
        fuente_codigo  = raw.fuente_codigo,
        raw_snippet    = texto[:400],
    )

    return canonical


def validate_canonical(canonical: FondoCanonical) -> tuple[bool, list[str]]:
    """
    Valida que un FondoCanonical tiene todos los campos mínimos para INSERT.
    Implementa el paso Staging → Validator del pipeline.

    Returns:
        (is_valid, lista_de_errores)
        is_valid = True solo si errores está vacío.
    """
    errores = []

    if not canonical.nombre or len(canonical.nombre) < 5:
        errores.append("nombre demasiado corto o vacío")
    if not canonical.emisor_codigo:
        errores.append("emisor_codigo requerido")
    if canonical.emisor_codigo not in EMISORES_CONOCIDOS and canonical.emisor_codigo != "OTROS":
        errores.append(f"emisor_codigo desconocido: {canonical.emisor_codigo}")
    if canonical.estado not in ESTADOS_VALIDOS:
        errores.append(f"estado inválido: {canonical.estado}")
    if canonical.monto_max_usd is not None and canonical.monto_max_usd <= 0:
        errores.append("monto_max_usd debe ser positivo")
    if (canonical.monto_min_usd and canonical.monto_max_usd and
            canonical.monto_min_usd > canonical.monto_max_usd):
        errores.append("monto_min_usd > monto_max_usd")
    if not canonical.url:
        # No es bloqueante pero sí un warning
        logger.warning(f"[Normalizer] Sin URL para {canonical.nombre[:60]}")

    canonical.errores_validacion = errores
    return (len(errores) == 0), errores


# ── Haiku caller ──────────────────────────────────────────────────────────────

def _load_anthropic_key() -> str:
    """Resuelve API key de Anthropic: env var → secrets.toml → vacío."""
    import os
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key
    # Fallback: .streamlit/secrets.toml — busca patrón sk-ant-... directamente
    try:
        import pathlib, re as _re
        secrets_path = pathlib.Path(".streamlit/secrets.toml")
        if secrets_path.exists():
            content = secrets_path.read_text(encoding="utf-8")
            # Buscar cualquier valor que sea una Anthropic API key
            match = _re.search(r'"(sk-ant-[A-Za-z0-9\-_]{20,})"', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return ""


def _call_haiku(user_content: str, fuente_codigo: str) -> Optional[dict]:
    """Llama a Claude Haiku y parsea el JSON de respuesta."""
    try:
        import anthropic
        api_key = _load_anthropic_key()
        client  = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

        msg = client.messages.create(
            model    = HAIKU_MODEL,
            max_tokens = 1024,
            system   = _SYSTEM_PROMPT,
            messages = [{"role": "user", "content": user_content}],
        )
        raw_text = msg.content[0].text.strip()

        # Limpiar posibles bloques de código markdown
        raw_text = re.sub(r"^```json\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$",     "", raw_text)

        data = json.loads(raw_text)
        return data

    except json.JSONDecodeError as e:
        logger.warning(f"[Normalizer][{fuente_codigo}] Haiku JSON parse error: {e}")
        return None
    except Exception as e:
        logger.warning(f"[Normalizer][{fuente_codigo}] Haiku error: {e}")
        return None


# ── Fallback heurístico ───────────────────────────────────────────────────────

def _heuristic_extract(raw: FondoRaw) -> Optional[dict]:
    """
    Extracción heurística básica sin LLM.
    Solo usa campos pre-extraídos del adaptador.
    Confidence máximo = 0.4 (siempre requiere revisión manual).
    """
    if not raw.titulo_raw:
        return None

    result = {
        "nombre":       raw.titulo_raw[:200],
        "emisor_codigo": raw.emisor_raw or raw.fuente_codigo,
        "estado":       "abierta",
        "elegibles":    raw.elegibles_raw or [],
        "temas":        raw.temas_raw or [],
        "url":          raw.url,
        "confidence":   0.4,
        "razon_confidence": "fallback heurístico sin Haiku",
    }

    # Intentar parsear monto_raw (usa _to_float para manejar notación europea)
    if raw.monto_raw:
        montos = re.findall(r"[\d.,]+", raw.monto_raw)
        nums   = [n for m in montos if (n := _to_float(m)) is not None]
        if len(nums) == 1:
            result["monto_max_usd"] = nums[0]
        elif len(nums) >= 2:
            result["monto_min_usd"] = min(nums[:2])
            result["monto_max_usd"] = max(nums[:2])

    return result


# ── Helpers de limpieza ────────────────────────────────────────────────────────

def _clean_emisor(codigo: str, fuente_fallback: str) -> str:
    c = (codigo or "").upper().strip().replace(" ", "_")
    return c if c in EMISORES_CONOCIDOS else fuente_fallback.upper()


def _clean_estado(estado: str) -> str:
    e = (estado or "abierta").lower().strip()
    return e if e in ESTADOS_VALIDOS else "abierta"


def _clean_list(items: list, validos: set) -> list:
    if not items:
        return []
    result = []
    for item in items:
        clean = (item or "").strip().lower().replace(" ", "_")
        # Intentar mapear variantes comunes
        if clean in ("municipio", "gad", "municipios", "gads"):
            clean = "GAD"
        elif clean in ("ong", "ngo"):
            clean = "ONG"
        elif clean in ("osc", "sociedad_civil"):
            clean = "OSC"
        else:
            # Capitalizar primer char para elegibles
            upper = clean.upper()
            if upper in validos:
                clean = upper
        if clean in validos:
            result.append(clean)
    return list(dict.fromkeys(result))  # deduplica preservando orden


def _to_float(val) -> Optional[float]:
    """
    Convierte a float manejando notación europea (5.000.000 = 5M)
    y americana (5,000,000 = 5M).
    """
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        s = str(val).strip()
        # Eliminar símbolos de moneda y espacios
        s = re.sub(r"[USD$€£¥\s]", "", s)
        if not s:
            return None

        dot_count   = s.count(".")
        comma_count = s.count(",")

        if dot_count == 0 and comma_count == 0:
            return float(s)
        elif dot_count > 1:
            # Notación europea: "5.000.000" o "5.000.000,50"
            s = s.replace(".", "").replace(",", ".")
        elif comma_count > 1:
            # Notación americana: "5,000,000" o "5,000,000.50"
            s = s.replace(",", "")
        elif dot_count == 1 and comma_count == 1:
            # Determinar cuál es el separador decimal (el último)
            if s.rindex(".") > s.rindex(","):
                s = s.replace(",", "")          # "5,000.50" → "5000.50"
            else:
                s = s.replace(".", "").replace(",", ".")  # "5.000,50" → "5000.50"
        elif comma_count == 1 and dot_count == 0:
            # "5000,50" → decimal europeo
            s = s.replace(",", ".")

        return float(s)
    except (TypeError, ValueError):
        return None


def _to_date(val) -> Optional[date]:
    if val is None:
        return None
    try:
        if isinstance(val, date):
            return val
        s = str(val).strip()
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
    except Exception:
        pass
    return None


# ── CLI de prueba ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

    # Test con texto de ejemplo
    test_raw = FondoRaw(
        fuente_codigo = "PNUD",
        url           = "https://undp.org/test",
        texto_fuente  = (
            "PNUD Ecuador abre convocatoria para proyectos de gobernanza local "
            "en municipios de la Costa. Monto: USD 50.000 - 200.000. "
            "Elegibles: GADs, ONG. Cierre: 30 de septiembre de 2026. "
            "Temas: gobernanza, participacion ciudadana, transparencia."
        ),
        titulo_raw    = "PNUD — Gobernanza Local Costa 2026",
        emisor_raw    = "PNUD",
    )

    use_haiku = "--no-haiku" not in sys.argv
    print(f"\nNormalizando con {'Haiku' if use_haiku else 'heurística'}...\n")

    result = normalize_raw_fund(test_raw, use_haiku=use_haiku)
    if result:
        print(f"nombre:       {result.nombre}")
        print(f"emisor:       {result.emisor_codigo}")
        print(f"monto:        {result.monto_min_usd} - {result.monto_max_usd}")
        print(f"fecha_cierre: {result.fecha_cierre}")
        print(f"elegibles:    {result.elegibles}")
        print(f"temas:        {result.temas}")
        print(f"confidence:   {result.confidence:.2f}")
        valid, errs = validate_canonical(result)
        print(f"valido:       {valid} {errs or ''}")
    else:
        print("Resultado: None (descartado por confidence bajo)")
