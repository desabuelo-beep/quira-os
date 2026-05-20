"""
sentinel/d4_normative.py
RC-D4 Normative Binding — QUIRA OS

Vincula patrones D4 calibrados con el marco juridico ecuatoriano.
Doctrina estricta: tension, NO acusacion. Inferencia, NO sentencia.

El sistema senala divergencias observables respecto a principios normativos.
La autoridad publica — nunca el sistema — determina implicancias juridicas.

Niveles de tension (binding probabilistico):
  SEVERA    — IRS critico + patrones multiples (overwhelm bypass activo)
              "presenta una divergencia estructural significativa respecto a..."
  MODERADA  — patron sistematico + IRS elevado
              "muestra patrones que ameritan revision a la luz de..."
  POTENCIAL — senales tempranas, analisis contextual necesario
              "genera indicadores de tension potencial en relacion con..."

NUNCA: "incumplio el Art. X" | "violo el principio Y" | "decision ilegal"
SIEMPRE: observable → divergencia → revision → la autoridad decide.

El PDOT es el instrumento mas fuerte: cuando el municipio fijo meta IRS<=45
y la distribucion actual es IRS=93, no hace falta norma externa — es el
propio plan institucional el que diverge del estado observado.

API principal: bind_d4_from_dict(cr_dict) -> D4NormativeBinding
Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# ── CARGA DE BASE NORMATIVA ────────────────────────────────────────────────────
_NORM_PATH = Path(__file__).parent.parent / "data" / "d4_normative.json"


def _load_norm_db() -> dict:
    try:
        if _NORM_PATH.exists():
            return json.loads(_NORM_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"articles": [], "pdot_targets": {}}


_NORM_DB = _load_norm_db()
_IRS_META_2027: float = float(
    _NORM_DB.get("pdot_targets", {}).get("irs_meta_2027", 45.0)
)


# ── TIPOS ──────────────────────────────────────────────────────────────────────

@dataclass
class D4NormRef:
    """Una referencia normativa vinculada a un patron D4."""
    law:          str     # "CRE" | "COOTAD" | "PDOT"
    article:      str     # "Art. 238" | "Art. 264(4)" | "Meta D4 2023-2027"
    topic:        str     # descripcion breve del principio
    tension_text: str     # lenguaje tension-aware generado
    tier:         str     # "severa" | "moderada" | "potencial"
    verificado:   bool    # True si el articulo fue verificado directamente


@dataclass
class D4NormativeBinding:
    """
    Resultado del binding normativo D4 con prudencia institucional.

    Garantias del binding:
      - Nunca acusatorio
      - Siempre auditadle (refs identificadas, tiers explicitos)
      - PDOT como instrumento prioritario (autocompromiso > norma externa)
      - Calibracion de competencia en agua (concurrente con SENAGUA/EMAPAM)
    """
    refs:             List[D4NormRef]   # referencias normativas activas
    pdot_alignment:   dict              # estado IRS vs meta PDOT 2027
    overall_tier:     str               # "severa" | "moderada" | "potencial" | "sin_tension"
    tension_summary:  str               # texto compacto para Claude Haiku (<=450 chars)
    prompt_block:     str               # bloque para inyeccion en system prompt
    n_refs:           int


# ── MECANISMOS INTERNOS ────────────────────────────────────────────────────────

def _compute_tier(irs: float, n_patterns: int, overwhelm: bool) -> str:
    """Determina el nivel de tension normativa."""
    if overwhelm or (irs >= 70 and n_patterns >= 3):
        return "severa"
    if irs >= 50 or n_patterns >= 2:
        return "moderada"
    if n_patterns >= 1 or irs >= 30:
        return "potencial"
    return "sin_tension"


def _tier_verb(tier: str) -> str:
    """Verbo canónico para cada nivel de tension."""
    return {
        "severa":    "presenta una divergencia estructural significativa respecto a",
        "moderada":  "muestra patrones que ameritan revision a la luz de",
        "potencial": "genera indicadores de tension potencial en relacion con",
    }.get(tier, "presenta indicadores en relacion con")


def _build_pdot_alignment(irs: float) -> dict:
    """
    Computa la alineacion IRS actual vs meta PDOT 2027.

    El PDOT es el instrumento analitico mas fuerte de D4-Normative:
    - Es el propio municipio quien establecio la meta
    - No requiere interpretacion de norma externa
    - La brecha es directamente observable y cuantificable
    """
    brecha = round(irs - _IRS_META_2027, 1)

    if brecha > 40:
        nivel = "severa"
        texto = (
            f"La distribucion actual (IRS={irs:.1f}) registra una brecha de "
            f"{brecha:+.1f} pts respecto a la meta PDOT 2027 (IRS <= {_IRS_META_2027:.0f}) "
            f"que el propio municipio establecio en su plan de desarrollo. "
            f"El autocompromiso institucional y la trayectoria observada divergen "
            f"estructuralmente."
        )
    elif brecha > 10:
        nivel = "moderada"
        texto = (
            f"La distribucion actual (IRS={irs:.1f}) supera la meta PDOT 2027 "
            f"(IRS <= {_IRS_META_2027:.0f}) en {brecha:.1f} pts. "
            f"Se requiere correccion de la tendencia para cumplir el "
            f"autocompromiso institucional."
        )
    elif brecha > 0:
        nivel = "potencial"
        texto = (
            f"La distribucion actual (IRS={irs:.1f}) supera levemente la meta "
            f"PDOT 2027 (IRS <= {_IRS_META_2027:.0f})."
        )
    else:
        nivel = "cumplido"
        texto = (
            f"La distribucion actual (IRS={irs:.1f}) cumple la meta PDOT 2027 "
            f"(IRS <= {_IRS_META_2027:.0f})."
        )

    return {
        "nivel":  nivel,
        "brecha": brecha,
        "meta":   _IRS_META_2027,
        "texto":  texto,
    }


def _find_relevant_articles(
    active_patterns: List[str],
    tier: str,
) -> List[D4NormRef]:
    """
    Selecciona articulos normativos relevantes para los patrones activos.
    Limita a 4 refs maximo para conservar tokens del contexto Haiku.
    PDOT siempre va primero — es el instrumento prioritario.
    """
    articles = _NORM_DB.get("articles", [])
    verb     = _tier_verb(tier)
    seen_ids: set = set()
    pdot_refs: List[D4NormRef] = []
    other_refs: List[D4NormRef] = []

    for art in articles:
        art_patterns = art.get("patterns", [])
        if not any(p in art_patterns for p in active_patterns):
            continue
        art_id = art.get("id", "")
        if art_id in seen_ids:
            continue
        seen_ids.add(art_id)

        # Para articulos no verificados: bajar el tier en el texto
        effective_tier = tier
        if not art.get("verificado", False) and tier == "severa":
            effective_tier = "moderada"  # no usar severa para articulos no verificados

        topic       = art.get("topic", "")
        base_text   = art.get("tension_text", f"{verb} {topic.lower()}")
        nota_comp   = art.get("nota_competencia", "")
        tension_txt = base_text
        if nota_comp:
            # Agregar nota de competencia concurrente (agua) al texto
            tension_txt = f"{base_text} — nota: {nota_comp[:100]}"

        ref = D4NormRef(
            law          = art.get("law", ""),
            article      = art.get("article", ""),
            topic        = topic,
            tension_text = tension_txt[:350],
            tier         = effective_tier,
            verificado   = art.get("verificado", False),
        )

        if art.get("law") == "PDOT":
            pdot_refs.append(ref)   # PDOT va primero
        else:
            other_refs.append(ref)

    # PDOT primero, luego el resto — max 4 en total
    all_refs = pdot_refs + other_refs
    return all_refs[:4]


def _build_tension_summary(
    refs:   List[D4NormRef],
    pdot:   dict,
    tier:   str,
    irs:    float,
    cr1:    float,
) -> str:
    """
    Texto compacto para Claude Haiku (<=450 chars).
    Prioriza el instrumento PDOT cuando la brecha es severa.
    """
    if tier == "sin_tension":
        return ""

    # Citar solo las leyes no-PDOT (el PDOT se menciona separado)
    non_pdot_laws = [
        f"{r.law} {r.article}"
        for r in refs
        if r.law != "PDOT"
    ]
    laws_str = " · ".join(non_pdot_laws[:3]) if non_pdot_laws else ""

    pdot_line = ""
    if pdot["nivel"] in ("severa", "moderada"):
        pdot_line = (
            f" PDOT 2027: brecha de {pdot['brecha']:+.1f} pts IRS "
            f"respecto al autocompromiso municipal."
        )

    verb = _tier_verb(tier)
    summary = (
        f"MARCO NORMATIVO D4: La distribucion territorial (IRS={irs:.1f}, "
        f"CR1={cr1:.0%}) {verb} los principios de equidad interterritorial."
        + (f" Fundamento: {laws_str}." if laws_str else "")
        + pdot_line
        + " El sistema senala divergencia — la autoridad publica determina implicancias."
    )
    return summary[:450]


def _build_prompt_block(
    refs:  List[D4NormRef],
    pdot:  dict,
    tier:  str,
) -> str:
    """
    Bloque completo para inyeccion en system prompt de Claude Haiku.
    Estructura: tier + refs + PDOT + instruccion de lenguaje.
    Max ~600 chars.
    """
    if tier == "sin_tension" and pdot["nivel"] == "cumplido":
        return ""

    lines = [
        f"MARCO NORMATIVO EQUIDAD TERRITORIAL D4 — Nivel: {tier.upper()}",
    ]

    for r in refs:
        verif_note = "" if r.verificado else " [verificar articulo exacto]"
        lines.append(f"  {r.law} {r.article}{verif_note}: {r.topic}")

    if pdot["nivel"] != "cumplido":
        lines.append(f"  PDOT 2023-2027 (autocompromiso): {pdot['texto'][:220]}")

    lines.append(
        "INSTRUCCION: Al responder sobre equidad o distribucion territorial, "
        "usar lenguaje de tension observable ('presenta divergencia respecto a...', "
        "'amerita revision a la luz de...'). "
        "PROHIBIDO: 'incumplio', 'violo', 'ilegal'. "
        "El sistema informa — la autoridad publica decide."
    )

    return "\n".join(lines)[:650]


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def bind_d4_from_dict(cr_dict: dict) -> D4NormativeBinding:
    """
    API principal: cr_dict de summarize_d4_calibrated() → D4NormativeBinding.

    El binding es probabilistico:
    - Selecciona articulos relevantes para los patrones activos
    - Calcula el tier de tension (severa/moderada/potencial)
    - Computa la brecha PDOT como instrumento prioritario
    - Genera texto tension-aware institucional
    """
    irs        = float(cr_dict.get("irs", 0))
    cr1        = float(cr_dict.get("cr1", 0))
    overwhelm  = irs >= 85.0
    patterns   = [p.get("nombre", "") for p in cr_dict.get("patterns_summary", [])]
    n_patterns = len(patterns)

    pdot = _build_pdot_alignment(irs)

    if n_patterns == 0 and irs < 20:
        return D4NormativeBinding(
            refs            = [],
            pdot_alignment  = pdot,
            overall_tier    = "sin_tension",
            tension_summary = "",
            prompt_block    = "",
            n_refs          = 0,
        )

    tier           = _compute_tier(irs, n_patterns, overwhelm)
    refs           = _find_relevant_articles(patterns, tier)
    tension_summ   = _build_tension_summary(refs, pdot, tier, irs, cr1)
    prompt_block   = _build_prompt_block(refs, pdot, tier)

    return D4NormativeBinding(
        refs            = refs,
        pdot_alignment  = pdot,
        overall_tier    = tier,
        tension_summary = tension_summ,
        prompt_block    = prompt_block,
        n_refs          = len(refs),
    )


def get_d4_normative_context(
    query:   str,
    cr_dict: Optional[dict] = None,
) -> str:
    """
    Retorna bloque normativo D4 para inyectar en Claude Haiku system prompt.
    Vacio si no hay tension normativa o cr_dict no disponible.
    Asume que query ya fue validada como territorialmente relevante.
    """
    if cr_dict is None:
        return ""

    binding = bind_d4_from_dict(cr_dict)
    return binding.prompt_block


def summarize_d4_normative(binding: D4NormativeBinding) -> dict:
    """Serializa D4NormativeBinding a dict para session_state / debug."""
    return {
        "overall_tier":    binding.overall_tier,
        "n_refs":          binding.n_refs,
        "tension_summary": binding.tension_summary,
        "pdot_alignment":  binding.pdot_alignment,
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
    import sys
    import io

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    from sentinel.d4_loader import run_d4_pipeline, invalidate_d4_cache
    from sentinel.d4_calibration import summarize_d4_calibrated

    print("=" * 65)
    print("RC-D4 Normative Binding — QUIRA OS")
    print("=" * 65)

    invalidate_d4_cache()
    cr  = run_d4_pipeline()
    if cr is None:
        print("ERROR: pipeline retorno None")
        sys.exit(1)

    d   = summarize_d4_calibrated(cr)
    binding = bind_d4_from_dict(d)

    print(f"\nTier de tension: {binding.overall_tier.upper()}")
    print(f"Referencias normativas: {binding.n_refs}")

    print("\nReferencias:")
    for r in binding.refs:
        verif = "VERIFICADO" if r.verificado else "pendiente verificacion"
        print(f"  [{r.tier}] {r.law} {r.article} — {r.topic}")
        print(f"    {verif}")

    print(f"\nPDOT Alignment:")
    pdot = binding.pdot_alignment
    print(f"  Meta 2027: IRS <= {pdot['meta']:.0f}")
    print(f"  IRS actual: {d['irs']:.1f}")
    print(f"  Brecha: {pdot['brecha']:+.1f} pts  [nivel: {pdot['nivel']}]")
    print(f"  {pdot['texto']}")

    print("\n--- Tension Summary (para Haiku) ---")
    print(binding.tension_summary)

    print("\n--- Prompt Block (inyeccion system) ---")
    print(binding.prompt_block)
