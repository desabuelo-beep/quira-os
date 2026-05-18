"""
SENTINEL RAG · explain.py  — Sprint 1.5
Capa de trazabilidad auditable: explica POR QUÉ Sentinel recuperó lo que recuperó.
Prerequisito obligatorio antes de conectar el LLM.

Reglas institucionales (colega 3):
  1. Nada responde sin fuente → retorna INSUFICIENTE si no hay chunks.
  2. Nada recomienda sin confianza → advierte si cobertura baja.
  3. Nada oculta sus vacíos → muestra qué dimensiones NO están cubiertas.

Uso:
  python -m sentinel.explain "¿Por qué D3 está en rojo?"
  o importar: from sentinel.explain import explain_retrieval

Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import json
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.query_rag import retrieve, ChunkResult
from sentinel.rag_config import RAG_TOP_K

# ── DIMENSIONES TGI ────────────────────────────────────────────────────────────
DIMENSIONES = {
    "D1": "Legalidad",
    "D2": "Planificación (ICPI)",
    "D3": "Ejecución Presupuestaria",
    "D4": "Equidad Territorial (IET)",
    "D5": "Capacidad Institucional",
}

# Qué tipos de nota cubren qué dimensiones
TIPO_A_DIMENSION: dict[str, list[str]] = {
    "normativa":            ["D1"],
    "normativa-cootad":     ["D1"],
    "normativa-constitucional": ["D1"],
    "normativa-losncp":     ["D1", "D3"],
    "normativa-losep":      ["D1", "D5"],
    "normativa-ley-loipevm":["D1", "D4"],
    "normativa-reforma-cootad": ["D1", "D3"],
    "normativa-cpfp":       ["D1", "D2"],
    "alerta-tgi":           ["D3"],
    "alerta-territorial":   ["D4"],
    "alerta-metodologica":  ["D2"],
    "alerta":               ["D2", "D3"],
    "contexto-operativo":   ["D2", "D3"],
    "plan-trabajo-cne":     ["D2"],
    "marco-plurianual-pdot":["D2"],
    "propuesta-pai":        ["D2", "D3"],
    "icm-sigad":            ["D2", "D5"],
    "rendicion-cuentas":    ["D1", "D5"],
    "trayectoria-historica":["D2", "D3"],
    "parroquia-tgi":        ["D4"],
    "parroquia":            ["D4"],
    "fondo":                ["D2", "D3"],
    "fuente-financiamiento":["D2", "D3"],
    "normativa-interna":    ["D5"],
    "programa_pdot":        ["D2", "D3"],
    "diagnostico":          ["D2", "D4"],
    "diagnostico-pugs":     ["D3", "D4"],
    "modelo-gestion":       ["D2", "D5"],
    "meta-sistema":         ["D1","D2","D3","D4","D5"],
    "meta-framework":       ["D1","D2","D3","D4","D5"],
    "sentinel-logica":      ["D1","D2","D3","D4","D5"],
    "catalogo":             ["D2"],
    "dashboard-cantonal":   ["D1","D2","D3","D4","D5"],
}

# Umbrales de confianza
UMBRAL_ALTA  = 0.65
UMBRAL_MEDIA = 0.40
UMBRAL_MIN   = 0.25  # por debajo → INSUFICIENTE

# Cobertura dimensional mínima para responder con confianza
MIN_DIMENSIONES_CUBIERTAS = 2


# ── ESTRUCTURAS DE DATOS ──────────────────────────────────────────────────────
@dataclass
class DimensionCoverage:
    dim_id:   str          # "D1" .. "D5"
    nombre:   str          # "Legalidad", etc.
    cubierta: bool
    score:    float        # mejor score de chunks que cubren esta dim
    fuentes:  list[str]    # notas que la cubren


@dataclass
class ExplainResult:
    pregunta:         str
    chunks:           list[ChunkResult]

    # Métricas de recuperación
    score_promedio:   float
    score_maximo:     float
    score_minimo:     float
    notas_distintas:  int
    tipos_distintos:  int
    territorios:      list[str]

    # Cobertura dimensional
    cobertura_dims:   dict[str, DimensionCoverage]  # "D1" → DimensionCoverage
    dims_cubiertas:   list[str]    # ["D1", "D3"]
    dims_faltantes:   list[str]    # ["D4", "D5"]

    # Veredicto
    confianza_pct:    float        # 0-100
    nivel_confianza:  str          # "🟢 Alta" | "🟡 Media" | "🔴 Baja"
    puede_responder:  bool
    puede_recomendar: bool
    razon_veredicto:  str

    # Las 3 reglas institucionales
    regla_fuente:     bool         # Tiene fuente para citar
    regla_confianza:  bool         # Confianza suficiente
    regla_cobertura:  bool         # Cobertura dimensional OK

    # Vacíos detectados
    vacios:           list[str]    # descripciones de lo que falta

    # Recomendación Sentinel
    accion_sentinel:  str          # qué debe hacer Sentinel con esta pregunta


# ── LÓGICA DE COBERTURA ───────────────────────────────────────────────────────
def _inferir_dimensiones_chunk(chunk: ChunkResult) -> list[str]:
    """
    Infiere qué dimensiones TGI cubre un chunk, usando:
    1. metadata dimension_tgi (más preciso)
    2. tipo_nota (fallback)
    3. keywords en el texto (último recurso)
    """
    dims: set[str] = set()

    # 1. Campo dimension_tgi del metadata
    if chunk.dimension:
        for part in chunk.dimension.split("|"):
            part = part.strip()
            if part in DIMENSIONES:
                dims.add(part)

    # 2. Tipo de nota
    tipo = chunk.tipo_nota.lower().strip()
    for tipo_key, tipo_dims in TIPO_A_DIMENSION.items():
        if tipo == tipo_key or tipo.startswith(tipo_key):
            dims.update(tipo_dims)
            break

    # 3. Keywords en texto (fallback)
    texto = chunk.text.lower()
    kw_map = {
        "D1": ["cootad", "constitución", "normativa", "legalidad", "ordenanza",
               "resolución", "decreto", "ley ", "reglamento", "legal"],
        "D2": ["icpi", "poa", "pdot", "planificación", "meta", "indicador",
               "pac", "poi", "programación", "snp", "copfp"],
        "D3": ["ejecución", "presupuesto", "esigef", "devengado", "contratación",
               "sercop", "d3", "59.85", "144k", "inversión real"],
        "D4": ["iet", "irs", "equidad", "parroquia", "rural", "nbi",
               "isabel muentes", "regresividad", "territorial", "d4"],
        "D5": ["institucional", "estatuto", "orgánico", "capacidad", "rdc",
               "rendición", "talento humano", "losep", "d5"],
    }
    for dim, keywords in kw_map.items():
        if any(kw in texto for kw in keywords):
            dims.add(dim)

    return list(dims)


def _calcular_cobertura(chunks: list[ChunkResult]) -> dict[str, DimensionCoverage]:
    """Calcula cobertura dimensional de todos los chunks."""
    # Inicializar todas las dimensiones como no cubiertas
    cobertura: dict[str, DimensionCoverage] = {}
    for dim_id, nombre in DIMENSIONES.items():
        cobertura[dim_id] = DimensionCoverage(
            dim_id=dim_id, nombre=nombre,
            cubierta=False, score=0.0, fuentes=[]
        )

    for chunk in chunks:
        dims = _inferir_dimensiones_chunk(chunk)
        for dim in dims:
            if dim in cobertura:
                cobertura[dim].cubierta = True
                cobertura[dim].score = max(cobertura[dim].score, chunk.score)
                if chunk.nota not in cobertura[dim].fuentes:
                    cobertura[dim].fuentes.append(chunk.nota)

    return cobertura


def _calcular_territorios(chunks: list[ChunkResult]) -> list[str]:
    """Extrae territorios cubiertos por los chunks."""
    territorios: set[str] = set()
    for c in chunks:
        texto = c.text.lower()
        if "isabel muentes" in texto:
            territorios.add("Isabel Muentes")
        if "noboa" in texto:
            territorios.add("Noboa")
        if "chirijos" in texto:
            territorios.add("Chirijos")
        if "la pila" in texto:
            territorios.add("La Pila")
        if "san sebastián" in texto or "san sebastian" in texto:
            territorios.add("San Sebastián")
        if "colorado" in texto:
            territorios.add("Colorado")
        if "leonidas" in texto:
            territorios.add("Leonidas Proaño")
        if "cantonal" in texto or "montecristi" in texto:
            territorios.add("Cantonal")
    return sorted(territorios) if territorios else ["Cantonal"]


def _confianza_global(
    chunks: list[ChunkResult],
    dims_cubiertas: list[str],
    dims_faltantes: list[str],
) -> float:
    """
    Score de confianza compuesto (0-100):
      60% → score promedio de similitud
      25% → cobertura dimensional
      15% → diversidad de fuentes
    """
    if not chunks:
        return 0.0

    score_avg  = sum(c.score for c in chunks) / len(chunks)
    cob_ratio  = len(dims_cubiertas) / len(DIMENSIONES)
    src_ratio  = min(len({c.nota for c in chunks}) / max(len(chunks), 1), 1.0)

    raw = (score_avg * 0.60) + (cob_ratio * 0.25) + (src_ratio * 0.15)
    return round(raw * 100, 1)


# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────────────────────
def explain_retrieval(pregunta: str, k: int = RAG_TOP_K) -> ExplainResult:
    """
    Recupera chunks y explica con trazabilidad completa por qué cada uno fue elegido.
    Aplica las 3 reglas institucionales y emite veredicto auditado.
    """
    chunks = retrieve(pregunta, k=k)

    # Sin resultados → veredicto inmediato
    if not chunks:
        empty_cov = {
            dim: DimensionCoverage(dim, nombre, False, 0.0, [])
            for dim, nombre in DIMENSIONES.items()
        }
        return ExplainResult(
            pregunta=pregunta, chunks=[],
            score_promedio=0, score_maximo=0, score_minimo=0,
            notas_distintas=0, tipos_distintos=0, territorios=[],
            cobertura_dims=empty_cov,
            dims_cubiertas=[], dims_faltantes=list(DIMENSIONES.keys()),
            confianza_pct=0, nivel_confianza="🔴 Sin resultados",
            puede_responder=False, puede_recomendar=False,
            razon_veredicto="ChromaDB no devolvió chunks — vault puede estar vacío o pregunta sin match",
            regla_fuente=False, regla_confianza=False, regla_cobertura=False,
            vacios=["No hay información en el Knowledge Base para esta pregunta"],
            accion_sentinel='RECHAZAR: "No encontré información suficiente en el Knowledge Base."',
        )

    # Métricas básicas
    scores         = [c.score for c in chunks]
    notas          = {c.nota for c in chunks}
    tipos          = {c.tipo_nota for c in chunks}
    score_prom     = round(sum(scores) / len(scores), 3)
    territorios    = _calcular_territorios(chunks)

    # Cobertura dimensional
    cobertura      = _calcular_cobertura(chunks)
    dims_cubiertas = [d for d, cov in cobertura.items() if cov.cubierta]
    dims_faltantes = [d for d, cov in cobertura.items() if not cov.cubierta]

    # Confianza compuesta
    conf_pct = _calcular_confianza_global(chunks, dims_cubiertas, dims_faltantes)

    if conf_pct >= UMBRAL_ALTA * 100:
        nivel = "🟢 Alta"
    elif conf_pct >= UMBRAL_MEDIA * 100:
        nivel = "🟡 Media"
    else:
        nivel = "🔴 Baja"

    # ── Las 3 reglas institucionales ──────────────────────────────────────────
    regla_fuente    = len(notas) >= 1 and score_prom >= UMBRAL_MIN
    regla_confianza = conf_pct >= UMBRAL_MEDIA * 100
    regla_cobertura = len(dims_cubiertas) >= MIN_DIMENSIONES_CUBIERTAS

    puede_responder  = regla_fuente and regla_confianza
    puede_recomendar = puede_responder and regla_cobertura

    # Vacíos detectados
    vacios = []
    if dims_faltantes:
        for d in dims_faltantes:
            vacios.append(f"{d} ({DIMENSIONES[d]}): sin cobertura en chunks recuperados")
    if score_prom < UMBRAL_MEDIA:
        vacios.append(f"Score promedio bajo ({score_prom:.2f}) — puede haber terminología no indexada")
    if len(notas) == 1:
        vacios.append("Todos los chunks vienen de una sola nota — respuesta puede ser parcial")

    # Razón del veredicto
    razon_partes = []
    if not regla_fuente:
        razon_partes.append("sin fuente confiable")
    if not regla_confianza:
        razon_partes.append(f"confianza insuficiente ({conf_pct:.0f}%)")
    if not regla_cobertura:
        dims_f_str = ", ".join(f"{d}={DIMENSIONES[d]}" for d in dims_faltantes)
        razon_partes.append(f"dimensiones sin cubrir: {dims_f_str}")

    razon = " | ".join(razon_partes) if razon_partes else "Criterios cumplidos"

    # Acción recomendada para Sentinel
    if not puede_responder:
        accion = 'RECHAZAR: "Información insuficiente para emitir criterio con trazabilidad."'
    elif not puede_recomendar:
        accion = 'RESPONDER CON ADVERTENCIA: citar fuentes, aclarar dimensiones sin cobertura.'
    else:
        accion = 'RESPONDER Y RECOMENDAR: confianza alta, cobertura suficiente, citar todas las fuentes.'

    return ExplainResult(
        pregunta        = pregunta,
        chunks          = chunks,
        score_promedio  = score_prom,
        score_maximo    = round(max(scores), 3),
        score_minimo    = round(min(scores), 3),
        notas_distintas = len(notas),
        tipos_distintos = len(tipos),
        territorios     = territorios,
        cobertura_dims  = cobertura,
        dims_cubiertas  = dims_cubiertas,
        dims_faltantes  = dims_faltantes,
        confianza_pct   = conf_pct,
        nivel_confianza = nivel,
        puede_responder  = puede_responder,
        puede_recomendar = puede_recomendar,
        razon_veredicto = razon,
        regla_fuente    = regla_fuente,
        regla_confianza = regla_confianza,
        regla_cobertura = regla_cobertura,
        vacios          = vacios,
        accion_sentinel = accion,
    )


# Alias para el nombre de función usado internamente
def _calcular_confianza_global(chunks, dims_cubiertas, dims_faltantes):
    return _confianza_global(chunks, dims_cubiertas, dims_faltantes)


# ── FORMATO DE SALIDA ─────────────────────────────────────────────────────────
def format_explain(r: ExplainResult) -> str:
    """Formatea ExplainResult como texto auditable para consola / log / Streamlit."""
    sep  = "═" * 64
    dash = "─" * 64
    lines = [
        sep,
        "  SENTINEL · explain_retrieval() — Capa de Trazabilidad",
        "  Dylus Lab © 2026",
        sep,
        f"  Pregunta: {r.pregunta}",
        dash,
    ]

    # Chunks recuperados
    lines.append(f"  Chunks recuperados ({len(r.chunks)}/{RAG_TOP_K}):")
    for i, c in enumerate(r.chunks, 1):
        dims = _inferir_dimensiones_chunk(c)
        dims_str = " ".join(dims) if dims else "?"
        lines.append(
            f"    {i}. {c.nota:<40} score={c.score}  [{dims_str}]"
        )
        lines.append(
            f"       '{c.section}'  tipo={c.tipo_nota}"
        )

    lines.append(dash)

    # Cobertura dimensional
    lines.append("  Cobertura por Dimensión TGI:")
    for dim_id, cov in r.cobertura_dims.items():
        if cov.cubierta:
            fuentes_str = " · ".join(cov.fuentes[:3])
            icon = "✅"
            lines.append(f"    {icon} {dim_id} {cov.nombre:<30} score={cov.score:.3f}")
            lines.append(f"       fuentes: {fuentes_str}")
        else:
            lines.append(f"    ❌ {dim_id} {cov.nombre:<30} SIN COBERTURA")

    lines.append(dash)

    # Territorio
    terr_str = " · ".join(r.territorios)
    lines.append(f"  Territorio cubierto: {terr_str}")
    lines.append(dash)

    # Métricas
    lines.append(f"  Métricas de recuperación:")
    lines.append(f"    Score promedio:    {r.score_promedio}  (max={r.score_maximo}, min={r.score_minimo})")
    lines.append(f"    Notas distintas:   {r.notas_distintas}")
    lines.append(f"    Tipos distintos:   {r.tipos_distintos}")
    lines.append(f"    Dims cubiertas:    {len(r.dims_cubiertas)}/5  ({' '.join(r.dims_cubiertas)})")
    lines.append(f"    Confianza global:  {r.confianza_pct:.0f}%  {r.nivel_confianza}")
    lines.append(dash)

    # Las 3 reglas
    lines.append("  Las 3 Reglas Institucionales:")
    lines.append(f"    {'✅' if r.regla_fuente    else '❌'} Regla 1 — Tiene fuente para citar")
    lines.append(f"    {'✅' if r.regla_confianza else '❌'} Regla 2 — Confianza suficiente ({r.confianza_pct:.0f}%)")
    lines.append(f"    {'✅' if r.regla_cobertura else '⚠️'} Regla 3 — Cobertura dimensional ({len(r.dims_cubiertas)}/5 dims)")
    lines.append(dash)

    # Vacíos
    if r.vacios:
        lines.append("  Vacíos detectados:")
        for v in r.vacios:
            lines.append(f"    ⚠️  {v}")
        lines.append(dash)

    # Veredicto
    verdict_icon = "🟢" if r.puede_recomendar else ("🟡" if r.puede_responder else "🔴")
    lines.append(f"  Veredicto: {verdict_icon}")
    if r.razon_veredicto != "Criterios cumplidos":
        lines.append(f"    {r.razon_veredicto}")
    lines.append(f"  → {r.accion_sentinel}")
    lines.append(sep)

    return "\n".join(lines)


def to_dict(r: ExplainResult) -> dict:
    """Convierte ExplainResult a dict serializable (para API / logs)."""
    return {
        "pregunta":         r.pregunta,
        "timestamp":        datetime.now().isoformat(),
        "metricas": {
            "score_promedio":  r.score_promedio,
            "score_maximo":    r.score_maximo,
            "score_minimo":    r.score_minimo,
            "notas_distintas": r.notas_distintas,
            "tipos_distintos": r.tipos_distintos,
            "confianza_pct":   r.confianza_pct,
            "nivel":           r.nivel_confianza,
        },
        "cobertura_dims": {
            dim: {
                "cubierta": cov.cubierta,
                "score":    cov.score,
                "fuentes":  cov.fuentes,
            }
            for dim, cov in r.cobertura_dims.items()
        },
        "territorios":      r.territorios,
        "dims_cubiertas":   r.dims_cubiertas,
        "dims_faltantes":   r.dims_faltantes,
        "reglas": {
            "fuente":    r.regla_fuente,
            "confianza": r.regla_confianza,
            "cobertura": r.regla_cobertura,
        },
        "puede_responder":  r.puede_responder,
        "puede_recomendar": r.puede_recomendar,
        "vacios":           r.vacios,
        "accion_sentinel":  r.accion_sentinel,
        "chunks": [
            {
                "nota":      c.nota,
                "section":   c.section,
                "tipo":      c.tipo_nota,
                "score":     c.score,
                "dims":      _inferir_dimensiones_chunk(c),
                "preview":   c.text[:200],
            }
            for c in r.chunks
        ],
    }


# ── INTEGRACIÓN EN api_rag.py (endpoint adicional) ───────────────────────────
def get_explain_endpoint_handler():
    """
    Retorna el handler FastAPI para /sentinel/explain.
    Llamar desde api_rag.py:
        from sentinel.explain import get_explain_endpoint_handler
        app.add_api_route("/sentinel/explain", get_explain_endpoint_handler(), methods=["POST"])
    """
    def handler(req):  # req: QueryRequest
        r = explain_retrieval(req.pregunta, k=req.k)
        return to_dict(r)
    return handler


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="explain_retrieval() — trazabilidad auditable Sentinel RAG"
    )
    parser.add_argument(
        "pregunta", nargs="?",
        default="¿Qué riesgos legales enfrenta Montecristi si D3 sigue bajo 60%?",
        help="Pregunta a analizar"
    )
    parser.add_argument("--json", action="store_true", help="Salida en JSON")
    parser.add_argument("--save", action="store_true", help="Guardar JSON en reports/")
    args = parser.parse_args()

    print(f"\n  Analizando: '{args.pregunta}'\n")
    result = explain_retrieval(args.pregunta)

    if args.json:
        print(json.dumps(to_dict(result), ensure_ascii=False, indent=2))
    else:
        print(format_explain(result))

    if args.save:
        report_dir = Path(__file__).parent / "reports"
        report_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        p  = report_dir / f"explain_{ts}.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(to_dict(result), f, ensure_ascii=False, indent=2)
        print(f"\n  Guardado: {p}")
