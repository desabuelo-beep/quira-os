"""
sentinel/learning_engine.py
Aprendizaje Institucional Trazable — Sprint 2.8A

Flujo: Humano resuelve → Sistema clasifica → Detecta recurrencia → Asiste futuras revisiones.

Sin ML. Sin cajas negras. Reglas deterministas auditables para sector público.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Optional

from sentinel.db_config import get_connection

# ── CATÁLOGO DE CATEGORÍAS ─────────────────────────────────────────────────────
# keyword sets → categoría canónica
CATEGORIAS: dict[str, dict] = {
    "reforma_presupuestaria": {
        "label":    "Reforma Presupuestaria",
        "keywords": [
            "reforma", "codificado", "presupuesto", "partida", "reasignac",
            "modificac", "ampliación", "reducción",
        ],
    },
    "retraso_documental": {
        "label":    "Retraso Documental",
        "keywords": [
            "documen", "cédula", "planilla", "entrega", "retraso", "demora",
            "pendiente entrega", "falta documento", "sin informar",
        ],
    },
    "proceso_contractual": {
        "label":    "Proceso Contractual",
        "keywords": [
            "contrat", "licitac", "concurso", "adjudicac", "sercop",
            "proceso compra", "adquisic", "proveedor",
        ],
    },
    "certificacion_presupuestaria": {
        "label":    "Certificación Presupuestaria",
        "keywords": [
            "certificac", "disponibilidad", "compromiso", "reserva",
            "certificado presupuestario",
        ],
    },
    "decision_directiva": {
        "label":    "Decisión Directiva",
        "keywords": [
            "directiv", "alcald", "resolucion directiv", "sesion", "acuerdo",
            "directorio", "acta", "disposición superior",
        ],
    },
    "ingesta_completada": {
        "label":    "Ingesta Completada",
        "keywords": [
            "ingesta", "cargado", "subido", "actualizado", "registrado",
            "cédula cargada", "planilla cargada",
        ],
    },
    "automatico": {
        "label":    "Resolución Automática",
        "keywords": [
            "automático", "automatico", "sistema", "recalcul", "correg",
            "auto-resolv",
        ],
    },
}

_OTRO = "otro"
_OTRO_LABEL = "Otro / No Clasificado"


# ── CLASIFICACIÓN DE TEXTO LIBRE ──────────────────────────────────────────────
def _classify_resolucion(text: str) -> str:
    """
    Asigna una categoría al texto de resolución humana.
    Reglas deterministas por frecuencia de keywords.
    Retorna el id de categoría o 'otro'.
    """
    if not text or not text.strip():
        return _OTRO
    low = text.lower()
    scores: dict[str, int] = {}
    for cat_id, meta in CATEGORIAS.items():
        hits = sum(1 for kw in meta["keywords"] if kw in low)
        if hits:
            scores[cat_id] = hits
    if not scores:
        return _OTRO
    return max(scores, key=lambda k: scores[k])


# ── EXTRACCIÓN Y PERSISTENCIA DE PATRONES ─────────────────────────────────────
def run_pattern_extraction() -> dict:
    """
    Lee todas las alertas resueltas con resolución, las clasifica
    y actualiza resolution_patterns (UPSERT).

    Retorna: {"procesadas": int, "categorias_actualizadas": int}
    """
    conn = get_connection()
    c    = conn.cursor()

    rows = c.execute("""
        SELECT entidad, tipo, resuelta_en, detected_at, resolucion
        FROM   alerts_history
        WHERE  estado = 'resuelta'
          AND  resolucion IS NOT NULL
          AND  resolucion != ''
    """).fetchall()

    if not rows:
        conn.close()
        return {"procesadas": 0, "categorias_actualizadas": 0}

    # Agrupar por categoría
    buckets: dict[str, list[dict]] = {}
    for r in rows:
        cat = _classify_resolucion(r.get("resolucion", ""))
        buckets.setdefault(cat, []).append(r)

    now_iso = datetime.now(timezone.utc).isoformat()

    cats_updated = 0
    for cat_id, items in buckets.items():
        label = CATEGORIAS.get(cat_id, {}).get("label", _OTRO_LABEL)

        frecuencia  = len(items)
        entidades   = list({i["entidad"] for i in items if i.get("entidad")})
        ejemplos    = [i["resolucion"][:120] for i in items[:3]]

        # Tiempo promedio de resolución (días)
        dias_list = []
        for i in items:
            try:
                det = datetime.fromisoformat(i["detected_at"])
                res = datetime.fromisoformat(i["resuelta_en"])
                dias_list.append((res - det).days)
            except Exception:
                pass
        tiempo_prom = round(sum(dias_list) / len(dias_list), 1) if dias_list else 0.0

        fechas = [i["resuelta_en"] for i in items if i.get("resuelta_en")]
        primera_vez = min(fechas) if fechas else now_iso
        ultima_vez  = max(fechas) if fechas else now_iso

        if conn.mode == "supabase":
            upsert = """
                INSERT INTO resolution_patterns
                    (categoria, label_display, frecuencia, tiempo_promedio_dias,
                     entidades_afectadas, ejemplos, primera_vez, ultima_vez, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (categoria) DO UPDATE SET
                    label_display         = EXCLUDED.label_display,
                    frecuencia            = EXCLUDED.frecuencia,
                    tiempo_promedio_dias  = EXCLUDED.tiempo_promedio_dias,
                    entidades_afectadas   = EXCLUDED.entidades_afectadas,
                    ejemplos              = EXCLUDED.ejemplos,
                    primera_vez           = EXCLUDED.primera_vez,
                    ultima_vez            = EXCLUDED.ultima_vez,
                    updated_at            = EXCLUDED.updated_at
            """
        else:
            upsert = """
                INSERT INTO resolution_patterns
                    (categoria, label_display, frecuencia, tiempo_promedio_dias,
                     entidades_afectadas, ejemplos, primera_vez, ultima_vez, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (categoria) DO UPDATE SET
                    label_display         = excluded.label_display,
                    frecuencia            = excluded.frecuencia,
                    tiempo_promedio_dias  = excluded.tiempo_promedio_dias,
                    entidades_afectadas   = excluded.entidades_afectadas,
                    ejemplos              = excluded.ejemplos,
                    primera_vez           = excluded.primera_vez,
                    ultima_vez            = excluded.ultima_vez,
                    updated_at            = excluded.updated_at
            """

        c.execute(upsert, (
            cat_id,
            label,
            frecuencia,
            tiempo_prom,
            json.dumps(entidades, ensure_ascii=False),
            json.dumps(ejemplos,  ensure_ascii=False),
            primera_vez,
            ultima_vez,
            now_iso,
        ))
        cats_updated += 1

    conn.commit()
    conn.close()
    return {"procesadas": len(rows), "categorias_actualizadas": cats_updated}


# ── CONSULTAS ─────────────────────────────────────────────────────────────────
def get_pattern_ranking() -> list[dict]:
    """
    Retorna patrones ordenados por frecuencia desc.
    Parsea entidades_afectadas y ejemplos desde JSON.
    """
    conn  = get_connection()
    rows  = conn.cursor().execute("""
        SELECT categoria, label_display, frecuencia, tiempo_promedio_dias,
               entidades_afectadas, ejemplos, primera_vez, ultima_vez, updated_at
        FROM   resolution_patterns
        ORDER  BY frecuencia DESC
    """).fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        try:
            d["entidades_afectadas"] = json.loads(d["entidades_afectadas"] or "[]")
        except Exception:
            d["entidades_afectadas"] = []
        try:
            d["ejemplos"] = json.loads(d["ejemplos"] or "[]")
        except Exception:
            d["ejemplos"] = []
        result.append(d)
    return result


# ── MATCHING DETERMINÍSTICO — Sprint 2.8B ─────────────────────────────────────

_RECOMENDACIONES: dict[str, str] = {
    "reforma_presupuestaria":
        "Verificar existencia de reforma presupuestaria vigente antes de escalar.",
    "retraso_documental":
        "Solicitar y confirmar entrega de documentación pendiente a la unidad responsable.",
    "proceso_contractual":
        "Revisar estado del proceso en el SERCOP y coordinar con la unidad de compras públicas.",
    "certificacion_presupuestaria":
        "Verificar disponibilidad presupuestaria y obtener certificación antes de comprometer recursos.",
    "decision_directiva":
        "Escalar a nivel directivo o de alcaldía para decisión formal en sesión ordinaria o extraordinaria.",
    "ingesta_completada":
        "Confirmar que la información fue registrada correctamente en el sistema antes de cerrar.",
    "automatico":
        "Verificar si el sistema corrigió automáticamente el indicador o si requiere intervención manual.",
    _OTRO:
        "Revisar antecedentes y coordinar con la unidad correspondiente para determinar la acción apropiada.",
}


def _same_trimester(y1: int, m1: int, y2: int, m2: int) -> bool:
    return (y1, (m1 - 1) // 3) == (y2, (m2 - 1) // 3)


def _recomendacion_operativa(cat_id: str, n_casos: int) -> str:
    base = _RECOMENDACIONES.get(cat_id, _RECOMENDACIONES[_OTRO])
    if n_casos >= 3:
        base += f" (Patrón recurrente: {n_casos} casos similares en la memoria institucional.)"
    return base


def get_context_for_alert(alerta: dict) -> Optional[dict]:
    """
    Sprint 2.8B — Contexto Institucional Activo.

    Matching determinístico multi-criterio sobre alertas resueltas con justificación.
    Pesos:
        mismo tipo      → +3  (alto)
        misma entidad   → +2  (medio)
        misma severidad → +2  (medio)
        mismo trimestre → +1  (bajo)

    Retorna None si no hay antecedentes disponibles.
    """
    tipo      = alerta.get("tipo", "")
    entidad   = alerta.get("entidad", "")
    severidad = alerta.get("severidad", "")
    year      = int(alerta.get("period_year",  0) or 0)
    month     = int(alerta.get("period_month", 0) or 0)

    conn = get_connection()
    rows = conn.cursor().execute("""
        SELECT entidad, tipo, severidad, period_year, period_month,
               detected_at, resuelta_en, resolucion
        FROM   alerts_history
        WHERE  estado     = 'resuelta'
          AND  resolucion IS NOT NULL
          AND  resolucion != ''
        ORDER  BY resuelta_en DESC
        LIMIT  100
    """).fetchall()
    conn.close()

    if not rows:
        return None

    # Pre-computa frecuencia por entidad+tipo para flag de reincidencia
    freq: dict[str, int] = {}
    for r in rows:
        k = f"{r['entidad']}|{r['tipo']}"
        freq[k] = freq.get(k, 0) + 1

    scored = []
    for r in rows:
        score = 0
        if r["tipo"]      == tipo:      score += 3
        if r["entidad"]   == entidad:   score += 2
        if r["severidad"] == severidad: score += 2
        if _same_trimester(
            int(r.get("period_year",  0) or 0),
            int(r.get("period_month", 0) or 0),
            year, month,
        ):                              score += 1

        if score < 1:
            continue

        dias = None
        try:
            det  = datetime.fromisoformat(r["detected_at"])
            res  = datetime.fromisoformat(r["resuelta_en"])
            dias = max(0, (res - det).days)
        except Exception:
            pass

        cat = _classify_resolucion(r.get("resolucion", ""))
        scored.append({
            "score":           score,
            "entidad":         r["entidad"],
            "periodo":         f"{int(r.get('period_month', 0) or 0):02d}/{r.get('period_year', '')}",
            "categoria":       CATEGORIAS.get(cat, {}).get("label", _OTRO_LABEL),
            "categoria_id":    cat,
            "resolucion":      (r.get("resolucion") or "")[:200],
            "dias_resolucion": dias,
            "reincidio":       freq.get(f"{r['entidad']}|{r['tipo']}", 0) >= 2,
        })

    if not scored:
        return None

    scored.sort(key=lambda x: x["score"], reverse=True)
    casos = scored[:5]

    # Categoría más frecuente entre los casos → recomendación
    cats_freq: dict[str, int] = {}
    for c in casos:
        cid = c["categoria_id"]
        cats_freq[cid] = cats_freq.get(cid, 0) + 1
    top_cat = max(cats_freq, key=lambda k: cats_freq[k]) if cats_freq else _OTRO

    return {
        "n_total":                len(casos),
        "casos_similares":        casos,
        "recomendacion_operativa": _recomendacion_operativa(top_cat, len(casos)),
    }


# ── BORRADORES INSTITUCIONALES — Sprint 2.8C ──────────────────────────────────

_TIPO_LABEL_MAP = {"ejecucion": "ejecución presupuestaria", "cobertura": "cobertura documental"}

_BORRADORES: dict[str, str] = {
    "reforma_presupuestaria": (
        "Se registra que el indicador de {tipo_label} correspondiente a {entidad_label} "
        "en el período {periodo} presenta afectación derivada de proceso de reforma "
        "presupuestaria institucional en trámite. Se verificará el cumplimiento del "
        "indicador una vez aprobada y ejecutada la reforma correspondiente, actualizando "
        "el seguimiento en el período inmediato siguiente."
    ),
    "retraso_documental": (
        "Se constata retraso en la entrega de documentación habilitante requerida para "
        "el indicador de {tipo_label} de {entidad_label} en el período {periodo}. "
        "La unidad responsable ha sido notificada formalmente para la regularización "
        "inmediata. Se realizará seguimiento en los próximos días hábiles."
    ),
    "proceso_contractual": (
        "El indicador de {tipo_label} de {entidad_label} en el período {periodo} "
        "presenta afectación por proceso contractual en etapa de selección y adjudicación. "
        "El proceso se encuentra registrado en el SERCOP conforme a la normativa vigente. "
        "Se espera regularización una vez completado el proceso de contratación pública."
    ),
    "certificacion_presupuestaria": (
        "Se registra que la ejecución del indicador de {tipo_label} de {entidad_label} "
        "en el período {periodo} está condicionada a la obtención de certificación "
        "presupuestaria. La unidad financiera ha iniciado los trámites correspondientes. "
        "El indicador será actualizado una vez obtenida la certificación."
    ),
    "decision_directiva": (
        "El estado del indicador de {tipo_label} de {entidad_label} en el período {periodo} "
        "está sujeto a resolución directiva. El caso fue presentado ante la dirección "
        "institucional para decisión formal. Se procederá conforme a lo resuelto en "
        "sesión ordinaria o extraordinaria según corresponda."
    ),
    "ingesta_completada": (
        "Se confirma que la información correspondiente al indicador de {tipo_label} de "
        "{entidad_label} en el período {periodo} ha sido registrada y validada en el "
        "sistema institucional. El indicador queda actualizado con los datos del período."
    ),
    "automatico": (
        "El sistema detectó y corrigió la inconsistencia en el indicador de {tipo_label} "
        "de {entidad_label} en el período {periodo}. Se verificó la integridad de los "
        "datos y se confirma la regularización automática del indicador."
    ),
    _OTRO: (
        "Se registra la revisión y gestión institucional del indicador de {tipo_label} "
        "de {entidad_label} en el período {periodo}. La alerta ha sido atendida "
        "conforme a los procedimientos internos aplicables."
    ),
}

from sentinel.alert_engine import ENTITY_LABELS as _ENTITY_LABELS   # noqa: E402


def build_resolution_suggestion(
    alerta: dict,
    ctx: Optional[dict] = None,
) -> Optional[dict]:
    """
    Sprint 2.8C — Continuidad Institucional Asistida.

    Construye un borrador de resolución institucional basado en antecedentes
    comparables. La decisión final siempre es humana.

    Retorna None si no hay suficientes antecedentes para sugerir.
    """
    if ctx is None:
        ctx = get_context_for_alert(alerta)
    if not ctx or ctx["n_total"] == 0:
        return None

    casos = ctx["casos_similares"]

    # Categoría más frecuente → confianza
    cats_freq: dict[str, int] = {}
    for c in casos:
        cid = c["categoria_id"]
        cats_freq[cid] = cats_freq.get(cid, 0) + 1
    top_cat   = max(cats_freq, key=lambda k: cats_freq[k]) if cats_freq else _OTRO
    confianza = round(cats_freq.get(top_cat, 1) / max(1, len(casos)), 2)

    # No sugerir si la categoría dominante es "otro" y confianza es baja
    if top_cat == _OTRO and confianza < 0.5:
        return None

    # Contextualizar el borrador
    tipo   = alerta.get("tipo", "")
    entidad = alerta.get("entidad", "")
    year   = alerta.get("period_year", "")
    month  = alerta.get("period_month", "")

    tipo_label   = _TIPO_LABEL_MAP.get(tipo, tipo)
    entidad_label = _ENTITY_LABELS.get(entidad, entidad)
    periodo      = f"{int(month or 0):02d}/{year}" if month and year else "–"

    template = _BORRADORES.get(top_cat, _BORRADORES[_OTRO])
    borrador = template.format(
        tipo_label=tipo_label,
        entidad_label=entidad_label,
        periodo=periodo,
    )

    label = CATEGORIAS.get(top_cat, {}).get("label", _OTRO_LABEL)
    return {
        "categoria_probable":  top_cat,
        "label_probable":      label,
        "confianza":           confianza,
        "confianza_pct":       round(confianza * 100),
        "sugerencia_operativa": ctx["recomendacion_operativa"],
        "borrador_resolucion": borrador,
    }


# ── ESTADÍSTICAS RÁPIDAS ──────────────────────────────────────────────────────
def get_learning_stats() -> dict:
    """Métricas de resumen para la cabecera de la página."""
    conn = get_connection()
    c    = conn.cursor()

    total_resueltas = (c.execute(
        "SELECT COUNT(*) as n FROM alerts_history WHERE estado='resuelta'"
    ).fetchone() or {}).get("n", 0)

    con_resolucion = (c.execute(
        "SELECT COUNT(*) as n FROM alerts_history WHERE estado='resuelta' AND resolucion IS NOT NULL AND resolucion != ''"
    ).fetchone() or {}).get("n", 0)

    n_patrones = (c.execute(
        "SELECT COUNT(*) as n FROM resolution_patterns"
    ).fetchone() or {}).get("n", 0)

    ultima_extraccion = (c.execute(
        "SELECT MAX(updated_at) as ts FROM resolution_patterns"
    ).fetchone() or {}).get("ts")

    conn.close()
    return {
        "total_resueltas":  total_resueltas,
        "con_resolucion":   con_resolucion,
        "sin_resolucion":   total_resueltas - con_resolucion,
        "n_patrones":       n_patrones,
        "ultima_extraccion": ultima_extraccion,
        "cobertura_pct":    round(con_resolucion / total_resueltas * 100, 1)
                            if total_resueltas else 0.0,
    }
