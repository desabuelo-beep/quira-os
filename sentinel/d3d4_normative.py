"""
sentinel/d3d4_normative.py
RC-D3D4-Normative — Capa Normativa del Motor de Inferencia Cruzada
QUIRA OS · Dylus Lab © 2026-05-20

Vincula los patrones cruzados D3xD4 con el marco juridico ecuatoriano.
Doctrina estricta: tension observable, NO acusacion. Hipotesis, NO veredicto.

La pregunta correcta no es: "¿se violo una norma?"
La pregunta correcta es: "¿que tensiones normativas emergen cuando D3 y D4 divergen?"

La divergencia temporal-territorial activa un nivel de tension normativa superior
al de cada motor por separado porque implica:
  - Recursos que aumentan (D3) pero no llegan equitativamente (D4): tension con equidad
  - Recursos que caen (D3) y la distribucion ya era inequitativa (D4): doble vulnerabilidad
  - Reforma presupuestaria (D3) que no corrige inequidad territorial (D4): coherencia PDOT

Tiers de tension (binding probabilistico cruzado):
  SEVERA    — cross_confidence confirmado + IRS critico + EED > 15
              "presenta una divergencia estructural significativa respecto a..."
  MODERADA  — patron cruzado moderado o EED significativo con D4 elevado
              "muestra patrones que ameritan revision a la luz de..."
  POTENCIAL — solo observacional o senales tempranas
              "genera indicadores de tension potencial en relacion con..."

PDOT siempre primero: la meta IRS <= 45 del PDOT 2023-2027 es el instrumento
mas fuerte porque es un autocompromiso municipal medible y directamente observable.
La divergencia D3xD4 respecto a esa meta no requiere interpretacion normativa externa.

NUNCA: "incumplio", "violo", "es responsable de", "decision ilegal"
SIEMPRE: observable → divergencia → tension normativa → la autoridad publica decide.

API principal:
  bind_cross_from_dict(cross_dict) -> D3D4NormativeBinding
  get_cross_normative_context(query, cross_dict) -> str  (para system prompt)
  summarize_d3d4_normative(binding) -> dict

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


# ── BASE NORMATIVA EMBEBIDA ────────────────────────────────────────────────────
# Articulos relevantes para divergencias D3xD4 (mas corta que D4-normative;
# el cruce es mas especifico y los articulos son un subconjunto orientado a
# coherencia presupuestaria-territorial, no solo equidad espacial).

_PDOT_IRS_META_2027: float = 45.0
_EED_SEVERO_UMBRAL:  float = 25.0   # EED > 25 pts → tension severa
_EED_MODERADO_UMBRAL: float = 12.0  # EED > 12 pts → tension moderada

_CROSS_NORM_DB: list[dict] = [
    # ── PDOT — instrumento prioritario (autocompromiso) ────────────────────────
    {
        "id": "PDOT-equidad-cruzada",
        "law": "PDOT",
        "article": "Meta D4 Equidad Territorial 2023-2027",
        "topic": "Objetivo IRS <= 45 — autocompromiso municipal en su propio plan de desarrollo",
        "cross_patterns": [
            "EXPANSION_CONCENTRADA", "EXPANSION_CON_EXCLUSION",
            "CRISIS_DOBLE", "EXCLUSION_PERIFERICA",
            "REDISTRIBUCION_REGRESIVA", "CONVERGENCIA_CRITICA",
            "MAQUILLAJE_TERRITORIAL",
        ],
        "tension_text": (
            "la divergencia entre desempeno presupuestario y distribucion territorial observada "
            "contrasta con el objetivo de equidad territorial que el propio municipio establecio "
            "en su PDOT 2023-2027 — la trayectoria actual es divergente respecto al autocompromiso institucional"
        ),
        "verificado": True,
        "nota": "Autocompromiso del GAD Montecristi. Meta IRS<=45 para 2027. "
                "Instrumento prioritario: no requiere interpretacion normativa externa — "
                "es el propio plan del municipio el que diverge del estado observado.",
    },
    # ── CRE — Constitucion de la Republica del Ecuador ─────────────────────────
    {
        "id": "CRE-238-cross",
        "law": "CRE",
        "article": "Art. 238",
        "topic": "Autonomia y principio de equidad interterritorial de los GADs",
        "cross_patterns": [
            "EXPANSION_CONCENTRADA", "CRISIS_DOBLE",
            "EXCLUSION_PERIFERICA", "CONVERGENCIA_CRITICA",
        ],
        "tension_text": (
            "la divergencia temporal-territorial observada — ejecucion presupuestaria y "
            "distribucion interparroquial — presenta indicadores de tension con el principio "
            "constitucional de equidad interterritorial que rige el ejercicio autonomo de los GADs"
        ),
        "verificado": True,
        "nota": "CRE Art. 238: los GADs se rigen por principios de equidad interterritorial. "
                "La divergencia D3xD4 es relevante cuando la ejecucion agregada mejora "
                "pero la distribucion territorial no converge.",
    },
    {
        "id": "CRE-264-4-cross",
        "law": "CRE",
        "article": "Art. 264(4)",
        "topic": "Competencia municipal en servicios de agua potable y saneamiento",
        "cross_patterns": ["VULNERABILIDAD_HIDRICA", "EXPANSION_CON_EXCLUSION"],
        "tension_text": (
            "la contraccion de ejecucion combinada con inequidad hidrica territorial genera "
            "tension en el ambito de competencia del GAD en agua potable establecida constitucionalmente"
        ),
        "verificado": True,
        "nota_competencia": (
            "Competencia concurrente: EMAPAM/SENAGUA/Juntas de Agua tambien intervienen. "
            "El binding hidrico aplica con calibracion de alcance competencial. "
            "No imputa responsabilidad exclusiva al GAD."
        ),
    },
    # ── COOTAD ────────────────────────────────────────────────────────────────
    {
        "id": "COOTAD-3-cross",
        "law": "COOTAD",
        "article": "Art. 3 (principios)",
        "topic": "Principio de equidad interterritorial en la gestion de los GADs",
        "cross_patterns": [
            "EXPANSION_CONCENTRADA", "CRISIS_DOBLE",
            "EXCLUSION_PERIFERICA", "REDISTRIBUCION_REGRESIVA",
        ],
        "tension_text": (
            "el patron de divergencia entre ejecucion presupuestaria y distribucion territorial "
            "muestra indicadores de tension con el principio de equidad interterritorial "
            "que el COOTAD establece como rector del ejercicio de potestades publicas de los GADs"
        ),
        "verificado": True,
        "nota": "COOTAD Art. 3 incluye explicitamente el principio de equidad interterritorial.",
    },
    # ── COPLAFIP — coherencia presupuestaria y planificacion ──────────────────
    {
        "id": "COPLAFIP-planificacion-cross",
        "law": "COPLAFIP",
        "article": "Coherencia presupuestaria-planificacion territorial",
        "topic": "Coherencia entre ejecucion presupuestaria y planificacion territorial de los GADs",
        "cross_patterns": [
            "MAQUILLAJE_TERRITORIAL", "REDISTRIBUCION_REGRESIVA",
            "EXPANSION_CONCENTRADA",
        ],
        "tension_text": (
            "la divergencia entre la trayectoria de ejecucion presupuestaria y la distribucion "
            "territorial observada genera indicadores de tension con el principio de coherencia "
            "entre planificacion y presupuesto establecido en el marco del COPLAFIP"
        ),
        "verificado": False,
        "nota": "Principio de coherencia presupuestaria-planificacion: verificar articulo exacto. "
                "Aplicar con lenguaje potencial hasta verificacion.",
    },
]

# Mapa rapido: cross_pattern → ids relevantes (precalculado)
_PATTERN_TO_NORM_IDS: dict[str, list[str]] = {}
for _art in _CROSS_NORM_DB:
    for _cp in _art.get("cross_patterns", []):
        _PATTERN_TO_NORM_IDS.setdefault(_cp, []).append(_art["id"])


# ── TIPOS ──────────────────────────────────────────────────────────────────────

@dataclass
class D3D4NormRef:
    """Una referencia normativa vinculada a un patron D3xD4."""
    law:          str     # "CRE" | "COOTAD" | "PDOT" | "COPLAFIP"
    article:      str     # "Art. 238" | "Meta D4 2023-2027" etc.
    topic:        str     # descripcion breve del principio
    tension_text: str     # lenguaje tension-aware generado
    tier:         str     # "severa" | "moderada" | "potencial"
    verificado:   bool    # True si el articulo fue verificado directamente


@dataclass
class D3D4NormativeBinding:
    """
    Resultado del binding normativo D3xD4 con prudencia institucional.

    Garantias del binding:
      - Nunca acusatorio — tension observable, no veredicto
      - Auditadle: refs identificadas, tiers explicitos, observacional flag heredado
      - PDOT como instrumento prioritario (autocompromiso > norma externa)
      - Hereda observational_only del motor D3xD4 (D3 insuficiente → tier max = potencial)
      - Nota de competencia concurrente en agua (CRE 264(4))
    """
    refs:                 List[D3D4NormRef]  # referencias normativas activas
    pdot_contradiction:   dict               # matriz de contradiccion PDOT
    overall_tier:         str                # "severa" | "moderada" | "potencial" | "sin_tension"
    tension_summary:      str                # texto compacto para Claude Haiku (<=450 chars)
    prompt_block:         str                # bloque para inyeccion en system prompt
    cross_pattern:        str                # patron D3xD4 que activo el binding
    observational_only:   bool               # heredado de D3D4CrossResult
    n_refs:               int


# ── MECANISMOS INTERNOS ────────────────────────────────────────────────────────

def _compute_cross_tier(
    cross_pattern:      str,
    irs:                float,
    eed:                float,
    cross_conf:         float,
    observational_only: bool,
) -> str:
    """
    Tier de tension normativa cruzada.

    Si observational_only=True: cap en 'potencial' (no confirmamos severa/moderada
    con evidencia D3 insuficiente).

    Logica:
      severa   — cross_conf >= 0.40 + IRS >= 70 + |EED| >= 25
      moderada — cross_conf >= 0.25 + (IRS >= 50 o |EED| >= 12)
      potencial — observacional o senales parciales
    """
    if observational_only:
        return "potencial"

    abs_eed = abs(eed)
    if cross_conf >= 0.40 and irs >= 70 and abs_eed >= _EED_SEVERO_UMBRAL:
        return "severa"
    if cross_conf >= 0.25 and (irs >= 50 or abs_eed >= _EED_MODERADO_UMBRAL):
        return "moderada"
    if cross_pattern not in ("SIN_CRUCE_CONFIRMADO",):
        return "potencial"
    return "sin_tension"


def _tier_verb(tier: str) -> str:
    """Verbo canonico para cada nivel de tension normativa cruzada."""
    return {
        "severa":    "presenta una divergencia estructural significativa respecto a",
        "moderada":  "muestra patrones que ameritan revision a la luz de",
        "potencial": "genera indicadores de tension potencial en relacion con",
    }.get(tier, "presenta indicadores en relacion con")


def _build_pdot_contradiction(
    cross_pattern: str,
    irs:           float,
    eed:           float,
    d3_class:      str,
) -> dict:
    """
    Matriz de contradiccion entre patron D3xD4 y metas PDOT.
    El PDOT es el instrumento mas fuerte (autocompromiso municipal).

    Dos dimensiones:
      1. Equidad territorial (IRS vs meta IRS <= 45)
      2. Coherencia temporal-territorial (EED vs objetivo EED ~ 0)
    """
    brecha_irs = round(irs - _PDOT_IRS_META_2027, 1)
    abs_eed    = round(abs(eed), 1)

    # Nivel brecha IRS
    if brecha_irs > 40:
        nivel_irs = "severa"
        texto_irs = (
            f"La distribucion territorial actual (IRS={irs:.1f}) registra una brecha de "
            f"{brecha_irs:+.1f} pts respecto a la meta PDOT 2027 (IRS <= {_PDOT_IRS_META_2027:.0f}) "
            f"que el propio municipio establecio en su plan de desarrollo."
        )
    elif brecha_irs > 10:
        nivel_irs = "moderada"
        texto_irs = (
            f"La distribucion territorial (IRS={irs:.1f}) supera la meta PDOT 2027 "
            f"(IRS <= {_PDOT_IRS_META_2027:.0f}) en {brecha_irs:.1f} pts."
        )
    elif brecha_irs > 0:
        nivel_irs, texto_irs = "potencial", f"IRS={irs:.1f} supera levemente la meta PDOT 2027."
    else:
        nivel_irs, texto_irs = "cumplido", f"IRS={irs:.1f} cumple la meta PDOT 2027."

    # Nivel coherencia temporal-territorial (EED)
    if abs_eed >= _EED_SEVERO_UMBRAL:
        nivel_eed = "severa"
        eed_dir   = "expansion concentrada" if eed > 0 else "rezago distributivo"
        texto_eed = (
            f"La divergencia temporal-territorial (EED={eed:+.1f} pts — {eed_dir}) "
            f"indica que el desempeno de ejecucion y la distribucion territorial operan "
            f"en sentidos opuestos, en tension con el autocompromiso de desarrollo equilibrado."
        )
    elif abs_eed >= _EED_MODERADO_UMBRAL:
        nivel_eed = "moderada"
        texto_eed = f"La divergencia EED={eed:+.1f} pts requiere revision de coherencia temporal-territorial."
    else:
        nivel_eed = "potencial"
        texto_eed = f"EED={eed:+.1f} pts: baja divergencia temporal-territorial."

    rows = [
        {
            "dimension":     "Equidad territorial (IRS)",
            "meta_pdot":     f"IRS <= {_PDOT_IRS_META_2027:.0f}",
            "estado_actual": f"IRS = {irs:.1f}",
            "brecha":        f"{brecha_irs:+.1f} pts",
            "nivel":         nivel_irs,
            "texto":         texto_irs,
        },
        {
            "dimension":     "Coherencia temporal-territorial (EED)",
            "meta_pdot":     "EED ~ 0 (equidad alineada)",
            "estado_actual": f"EED = {eed:+.1f} pts",
            "brecha":        f"{abs_eed:.1f} pts de divergencia",
            "nivel":         nivel_eed,
            "texto":         texto_eed,
        },
    ]

    overall_nivel = (
        "severa" if nivel_irs in ("severa",) and nivel_eed in ("severa", "moderada") else
        "moderada" if "moderada" in (nivel_irs, nivel_eed) else
        "potencial"
    )

    return {
        "cross_pattern": cross_pattern,
        "d3_class":      d3_class,
        "rows":          rows,
        "overall_nivel": overall_nivel,
        "brecha_irs":    brecha_irs,
        "brecha_eed":    abs_eed,
    }


def _find_cross_refs(
    cross_pattern: str,
    tier:          str,
) -> List[D3D4NormRef]:
    """
    Selecciona referencias normativas para el patron cruzado activo.
    PDOT siempre primero. Maximo 4 refs para conservar tokens Haiku.
    Articulos no verificados → downgrade de severa a moderada.
    """
    verb     = _tier_verb(tier)
    norm_ids = _PATTERN_TO_NORM_IDS.get(cross_pattern, [])
    id_set   = set(norm_ids)

    pdot_refs:  List[D3D4NormRef] = []
    other_refs: List[D3D4NormRef] = []

    for art in _CROSS_NORM_DB:
        if art["id"] not in id_set:
            continue

        effective_tier = tier
        if not art.get("verificado", False) and tier == "severa":
            effective_tier = "moderada"

        nota_comp   = art.get("nota_competencia", "")
        base_text   = art.get("tension_text", f"{verb} {art.get('topic','').lower()}")
        tension_txt = base_text
        if nota_comp:
            tension_txt = f"{base_text} — nota: {nota_comp[:100]}"

        ref = D3D4NormRef(
            law          = art["law"],
            article      = art["article"],
            topic        = art["topic"],
            tension_text = tension_txt[:350],
            tier         = effective_tier,
            verificado   = art.get("verificado", False),
        )

        if art["law"] == "PDOT":
            pdot_refs.append(ref)
        else:
            other_refs.append(ref)

    return (pdot_refs + other_refs)[:4]


def _build_tension_summary(
    refs:          List[D3D4NormRef],
    pdot:          dict,
    tier:          str,
    irs:           float,
    eed:           float,
    cross_pattern: str,
    observational: bool,
) -> str:
    """
    Texto compacto para Claude Haiku (<=450 chars).
    Observacional = prefijo explicito.
    """
    if tier == "sin_tension":
        return ""

    non_pdot = [f"{r.law} {r.article}" for r in refs if r.law != "PDOT"]
    laws_str = " · ".join(non_pdot[:3]) if non_pdot else ""
    verb     = _tier_verb(tier)

    pdot_line = ""
    if pdot["overall_nivel"] in ("severa", "moderada"):
        pdot_line = (
            f" PDOT 2027: brecha IRS {pdot['brecha_irs']:+.1f} pts + "
            f"divergencia EED {pdot['brecha_eed']:.1f} pts respecto a autocompromiso municipal."
        )

    obs_prefix = "[Observacional — D3 insuficiente] " if observational else ""
    cp_label   = cross_pattern.replace("_", " ").title()

    summary = (
        f"{obs_prefix}CRUCE D3xD4 — {cp_label}: "
        f"la divergencia temporal-territorial (IRS={irs:.1f}, EED={eed:+.1f}) "
        f"{verb} los principios de equidad institucional."
        + (f" Fundamento: {laws_str}." if laws_str else "")
        + pdot_line
        + " El sistema senala divergencia — la autoridad publica determina implicancias."
    )
    return summary[:450]


def _build_prompt_block(
    refs:          List[D3D4NormRef],
    pdot:          dict,
    tier:          str,
    cross_pattern: str,
    observational: bool,
    eed:           float,
) -> str:
    """
    Bloque para inyeccion en system prompt de Claude Haiku (<=650 chars).
    Estructura: tier + patron + refs + PDOT contradiction + instruccion.
    """
    if tier == "sin_tension":
        return ""

    obs_tag = " [OBSERVACIONAL]" if observational else ""
    lines   = [
        f"MARCO NORMATIVO D3xD4{obs_tag} — {cross_pattern} [{tier.upper()}]",
        f"  EED={eed:+.1f} pts | IRS={pdot['rows'][0]['estado_actual']}",
    ]

    for r in refs:
        verif_note = "" if r.verificado else " [verificar articulo exacto]"
        lines.append(f"  {r.law} {r.article}{verif_note}: {r.topic}")

    if pdot["overall_nivel"] in ("severa", "moderada"):
        rows_text = (
            f"IRS brecha {pdot['brecha_irs']:+.1f} pts | EED {pdot['brecha_eed']:.1f} pts"
        )
        lines.append(f"  PDOT 2023-2027 (autocompromiso): {rows_text}")

    lines.append(
        "INSTRUCCION D3xD4-NORM: Al responder sobre divergencia presupuestaria-territorial, "
        "usar lenguaje de hipotesis observable ('la evidencia sugiere...', "
        "'se observa tension con...'). "
        "PROHIBIDO: 'incumplio', 'violo', 'ilegal'. "
        "El sistema informa — la autoridad publica decide."
    )

    return "\n".join(lines)[:650]


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def bind_cross_from_dict(cross_dict: dict) -> D3D4NormativeBinding:
    """
    API principal: cross_dict de summarize_cross() -> D3D4NormativeBinding.

    El binding es probabilistico:
    - Selecciona articulos relevantes para el patron cruzado
    - Calcula el tier de tension (severa/moderada/potencial)
    - Hereda observational_only del motor D3xD4
    - Computa la matriz de contradiccion PDOT (dos dimensiones: IRS y EED)
    - Genera texto tension-aware institucional

    Args:
        cross_dict: output de summarize_cross() del motor d3d4_engine
    """
    cross_pattern = cross_dict.get("cross_pattern",      "SIN_CRUCE_CONFIRMADO")
    severity      = cross_dict.get("severity",           "OBSERVACIONAL")
    observational = bool(cross_dict.get("observational_only", True))
    eed           = float(cross_dict.get("eed_score",    0.0))
    cross_conf    = float(cross_dict.get("cross_confidence", 0.0))

    d4_s = cross_dict.get("d4_state", {})
    d3_s = cross_dict.get("d3_state", {})
    irs  = float(d4_s.get("irs",       0.0))
    d3_class = d3_s.get("avep_class", "SIN_PATRON_CLARO")

    # Patron nulo: sin binding
    if cross_pattern == "SIN_CRUCE_CONFIRMADO" and irs < 20:
        return D3D4NormativeBinding(
            refs                = [],
            pdot_contradiction  = {},
            overall_tier        = "sin_tension",
            tension_summary     = "",
            prompt_block        = "",
            cross_pattern       = cross_pattern,
            observational_only  = observational,
            n_refs              = 0,
        )

    tier = _compute_cross_tier(cross_pattern, irs, eed, cross_conf, observational)
    refs = _find_cross_refs(cross_pattern, tier)
    pdot = _build_pdot_contradiction(cross_pattern, irs, eed, d3_class)

    tension_summ = _build_tension_summary(
        refs, pdot, tier, irs, eed, cross_pattern, observational
    )
    prompt_block = _build_prompt_block(
        refs, pdot, tier, cross_pattern, observational, eed
    )

    return D3D4NormativeBinding(
        refs                = refs,
        pdot_contradiction  = pdot,
        overall_tier        = tier,
        tension_summary     = tension_summ,
        prompt_block        = prompt_block,
        cross_pattern       = cross_pattern,
        observational_only  = observational,
        n_refs              = len(refs),
    )


def get_cross_normative_context(
    query:      str,
    cross_dict: Optional[dict] = None,
) -> str:
    """
    Retorna bloque normativo D3xD4 para inyectar en Claude Haiku system prompt.
    Vacio si no hay cross_dict o si no hay tension normativa.
    """
    if cross_dict is None:
        return ""
    binding = bind_cross_from_dict(cross_dict)
    return binding.prompt_block


def summarize_d3d4_normative(binding: D3D4NormativeBinding) -> dict:
    """Serializa D3D4NormativeBinding a dict para session_state / debug."""
    return {
        "overall_tier":       binding.overall_tier,
        "cross_pattern":      binding.cross_pattern,
        "observational_only": binding.observational_only,
        "n_refs":             binding.n_refs,
        "tension_summary":    binding.tension_summary,
        "pdot_contradiction": binding.pdot_contradiction,
        "refs": [
            {
                "law":          r.law,
                "article":      r.article,
                "topic":        r.topic,
                "tension_text": r.tension_text[:200],
                "tier":         r.tier,
                "verificado":   r.verificado,
            }
            for r in binding.refs
        ],
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    from sentinel.d4_loader import run_d4_pipeline, invalidate_d4_cache
    from sentinel.d4_calibration import summarize_d4_calibrated
    from sentinel.d3d4_engine import analyze_cross, summarize_cross

    print("=" * 65)
    print("RC-D3D4-Normative — QUIRA OS")
    print("=" * 65)

    invalidate_d4_cache()
    d4_dict = summarize_d4_calibrated(run_d4_pipeline())
    d3_dict = {
        "calibrated_class":      "SIN_PATRON_CLARO",
        "avep_score":            52.0,
        "avep_riesgo":           "Transicion Critica",
        "calibrated_confidence": 0.07,
        "evidence_weight":       0.14,
        "sat_codes_calibrated":  [],
    }

    cross    = analyze_cross(d3_dict, d4_dict)
    cd       = summarize_cross(cross)
    binding  = bind_cross_from_dict(cd)

    print(f"\nPatron cruzado : {binding.cross_pattern}")
    print(f"Tier de tension: {binding.overall_tier.upper()}")
    print(f"Observacional  : {binding.observational_only}")
    print(f"Referencias    : {binding.n_refs}")

    print("\nReferencias normativas:")
    for r in binding.refs:
        v = "VERIFICADO" if r.verificado else "pendiente"
        print(f"  [{r.tier}] {r.law} {r.article} — {r.topic}")
        print(f"    {v}")

    print("\nMatriz PDOT contradiccion:")
    for row in binding.pdot_contradiction.get("rows", []):
        print(f"  {row['dimension']}")
        print(f"    Meta:    {row['meta_pdot']}")
        print(f"    Actual:  {row['estado_actual']}")
        print(f"    Brecha:  {row['brecha']}  [{row['nivel']}]")

    print("\n--- Tension Summary (para Haiku) ---")
    print(binding.tension_summary)

    print("\n--- Prompt Block ---")
    print(binding.prompt_block)
