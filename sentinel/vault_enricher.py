"""
sentinel/vault_enricher.py
P3 — Cierre del Loop Semantico · QUIRA OS · 2026-05-20

Conecta obsidian_bridge → legal_router de forma 100% determinista.
Convierte notas, SATs, competencias, evidencias y dimensiones TGI
en contexto inferencial consumible por Claude Haiku.

Flujo:
    query
     |
     detect_sats_from_query()   -- codigos SAT implicados
     detect_dims_from_query()   -- dimensiones TGI implicadas
     |
     sat_context_for_legal_router()   -- contexto vault por SAT
     get_notas_dimension()            -- notas por dimension
     |
     build_vault_prompt_block()  -- bloque listo para system prompt
     + provenance_record         -- trazabilidad por respuesta

Reglas de diseno:
    - Max 4 notas del vault por query (control de tokens)
    - SAT-match tiene prioridad sobre dim-match
    - Determinismo total: misma query = mismo contexto siempre
    - Nunca reemplaza el routing legal estatico. Lo enriquece.
    - Provenance exportable a audit log y debug panel

Dylus Lab (c) 2026
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

# Ruta raiz del proyecto para imports
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    from data.obsidian_bridge import (
        get_registry,
        sat_context_for_legal_router,
        get_notas_dimension,
    )
    _BRIDGE_OK = True
except Exception:
    _BRIDGE_OK = False


# -- LIMITES ------------------------------------------------------------------
_MAX_NOTES_PER_QUERY = 4      # notas maximas del vault por query
_MAX_CONTEXT_CHARS   = 900    # caracteres maximos del bloque vault en prompt
_MAX_SATS_PER_QUERY  = 2      # SATs a expandir (evita explosion de tokens)
_MAX_DIMS_PER_QUERY  = 2      # dimensiones complementarias


# -- SAT DETECTION: keywords -> codigo SAT -----------------------------------
# Orden importa: el primero que hace match tiene prioridad
_SAT_TRIGGERS: list[tuple[list[str], str]] = [
    # SAT-IX: incumplimiento marco normativo COOTAD/COPFP/Constitucion
    ([
        "sat-ix", "sat ix",
        "legalidad", "marco normativo", "cootad", "copfp", "constitucion",
        "lotaip", "rendicion de cuentas", "rendicion", "cpccs",
        "participacion ciudadana", "concejo municipal", "competencias gad",
        "transparencia institucional", "control social",
    ], "SAT-IX"),

    # SAT-X-A: reforma oculta / contratacion irregular
    ([
        "sat-x-a", "sat x a", "reforma oculta",
        "contratacion", "sercop", "compraspublicas",
        "adjudicar", "adjudicacion", "fraccionamiento",
        "infima cuantia", "menor cuantia", "cotizacion", "licitacion",
        "emergencia contratacion", "daps", "proceso contractual",
        "losncp", "contrato",
    ], "SAT-X-A"),

    # SAT-X-B: reprogramacion presupuestaria
    ([
        "sat-x-b", "sat x b", "reprogramacion", "reprogramacion",
        "reforma presupuestaria", "modificacion presupuestaria",
        "reasignar", "reasignacion", "reforma poa", "reforma al poa",
        "modificar presupuesto", "cambiar presupuesto",
    ], "SAT-X-B"),

    # SAT-XI: paralisis de ejecucion presupuestaria
    ([
        "sat-xi", "sat xi", "paralisis",
        "ejecucion presupuestaria", "devengado", "esigef",
        "tasa ejecucion", "infraejecucion", "fondos bloqueados",
        "inversion bloqueada", "d3", "59.85", "bde",
        "grupos 7", "grupos 8", "grupos inversion",
    ], "SAT-XI"),

    # SAT-XII: regresividad e inequidad territorial
    ([
        "sat-xii", "sat xii", "irs", "regresividad", "regresivo",
        "equidad territorial", "iet", "brecha territorial",
        "isabel muentes", "inequidad", "per capita",
        "parroquia rural", "distribucion inequitativa", "nbi alto",
    ], "SAT-XII"),
]


# -- DIMENSION DETECTION: keywords -> ID canonico ----------------------------
_DIM_TRIGGERS: list[tuple[list[str], str]] = [
    ([
        "legalidad", "normativa", "cootad", "copfp", "constitucion",
        "legal", "decreto", "ordenanza", "lotaip", "cpccs",
        "juridico", "marco legal", "articulo", "ley ",
    ], "D1_LEGALIDAD"),
    ([
        "planificacion", "pdot", "poa", "pac", "meta", "icpi",
        "poi", "programacion", "congruencia", "pdyot",
        "plan operativo", "plan de desarrollo",
    ], "D2_PLANIFICACION"),
    ([
        "ejecucion", "devengado", "presupuesto", "d3",
        "esigef", "inversion", "fondos", "codificado",
        "ti 2025", "ti 2026", "tasa ejecucion", "grupos inversion",
    ], "D3_EJECUCION"),
    ([
        "equidad", "parroquia", "nbi", "irs", "iet", "brecha",
        "inequidad", "territorial", "rural", "per capita",
        "isabel muentes", "regresividad", "distribucion",
    ], "D4_EQUIDAD"),
    ([
        "institucional", "capacidad", "losep", "organico", "rdc",
        "icm", "transparencia", "d5", "talento humano",
        "estructura organica", "rendicion",
    ], "D5_CAPACIDAD"),
]


# -- HELPERS ------------------------------------------------------------------

def _norm(text: str) -> str:
    """Minusculas sin tildes."""
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


# -- API PUBLICA --------------------------------------------------------------

def detect_sats_from_query(query: str) -> list[str]:
    """
    Detecta codigos SAT implicados en la query.
    Retorna lista ordenada por prioridad, sin duplicados.
    Determinista: misma query = mismo resultado.
    """
    q = _norm(query)
    found: list[str] = []
    seen: set[str] = set()
    for triggers, sat_code in _SAT_TRIGGERS:
        if any(t in q for t in triggers):
            if sat_code not in seen:
                found.append(sat_code)
                seen.add(sat_code)
    return found


def detect_dims_from_query(query: str) -> list[str]:
    """
    Detecta dimensiones TGI canonicas implicadas en la query.
    Retorna lista de IDs canonicos sin duplicados.
    """
    q = _norm(query)
    found: list[str] = []
    seen: set[str] = set()
    for triggers, dim_id in _DIM_TRIGGERS:
        if any(t in q for t in triggers):
            if dim_id not in seen:
                found.append(dim_id)
                seen.add(dim_id)
    return found


def get_vault_normative_context(
    query:     str,
    max_notes: int = _MAX_NOTES_PER_QUERY,
) -> dict:
    """
    Obtiene contexto normativo del vault para una query.

    Prioridad:
        1. SAT codes detectados   -> sat_context_for_legal_router()
        2. Dimensiones detectadas -> get_notas_dimension()
        3. Sin match              -> retorna vacio (sin error)

    Returns:
        {
          "context_block": str,         # listo para system prompt
          "sat_codes":     list[str],   # SATs activados
          "dimensions":    list[str],   # dimensiones TGI activadas
          "provenance":    list[dict],  # trazabilidad nota x nota
          "has_context":   bool,
        }
    """
    _empty = {
        "context_block": "",
        "sat_codes":     [],
        "dimensions":    [],
        "provenance":    [],
        "has_context":   False,
    }

    if not _BRIDGE_OK:
        return _empty

    sat_codes  = detect_sats_from_query(query)
    dimensions = detect_dims_from_query(query)

    if not sat_codes and not dimensions:
        return {**_empty, "sat_codes": [], "dimensions": []}

    try:
        registry = get_registry()
    except Exception:
        return {**_empty, "sat_codes": sat_codes, "dimensions": dimensions}

    blocks:     list[str]  = []
    provenance: list[dict] = []
    notes_seen: set[str]   = set()

    # ---- 1. Contexto por SAT (maxima prioridad) ------------------------------
    notas_map: dict[str, dict] = {
        (n.get("name") or n["_path"]): n
        for n in registry.get("notas", [])
    }

    for sat_code in sat_codes[:_MAX_SATS_PER_QUERY]:
        ctx = sat_context_for_legal_router(sat_code, registry)
        if ctx:
            blocks.append(ctx)

        notas_ids = registry.get("sat_triggers", {}).get(sat_code.upper(), [])
        for nota_id in notas_ids[:max_notes]:
            if nota_id in notes_seen:
                continue
            nota = notas_map.get(nota_id)
            if nota:
                provenance.append({
                    "nota":        nota_id,
                    "sat_trigger": sat_code,
                    "dimension":   nota.get("dimension_tgi", []),
                    "competencia": str(nota.get("competencia", ""))[:80],
                    "evidencia":   str(nota.get("evidencia_requerida", ""))[:60],
                    "path":        nota.get("_path", ""),
                })
                notes_seen.add(nota_id)

    # ---- 2. Contexto por dimension (complementario) -------------------------
    for dim_id in dimensions[:_MAX_DIMS_PER_QUERY]:
        if len(notes_seen) >= max_notes:
            break

        dim_notas = get_notas_dimension(dim_id, registry)
        nuevas    = [n for n in dim_notas if n not in notes_seen]
        cupo      = max_notes - len(notes_seen)
        nuevas    = nuevas[:cupo]

        if not nuevas:
            continue

        dim_lines = [f"[Vault — {dim_id}]"]
        for nid in nuevas:
            nota = notas_map.get(nid)
            if not nota:
                continue
            comp = nota.get("competencia", "")
            desc = str(nota.get("description", ""))[:100]
            dim_lines.append(
                f"  . {nid}"
                + (f" | Competencia: {str(comp)[:70]}" if comp else "")
                + (f"\n    {desc}" if desc else "")
            )
            provenance.append({
                "nota":        nid,
                "sat_trigger": None,
                "dimension":   [dim_id],
                "competencia": str(comp)[:80],
                "evidencia":   str(nota.get("evidencia_requerida", ""))[:60],
                "path":        nota.get("_path", ""),
            })
            notes_seen.add(nid)
        blocks.append("\n".join(dim_lines))

    # ---- Ensamblar bloque final ---------------------------------------------
    if not blocks:
        return {
            "context_block": "",
            "sat_codes":     sat_codes,
            "dimensions":    dimensions,
            "provenance":    provenance,
            "has_context":   False,
        }

    context_block = "\n".join(blocks)
    if len(context_block) > _MAX_CONTEXT_CHARS:
        context_block = (
            context_block[:_MAX_CONTEXT_CHARS]
            + "\n  [...contexto vault truncado — ver vault_registry.json]"
        )

    return {
        "context_block": context_block,
        "sat_codes":     sat_codes,
        "dimensions":    dimensions,
        "provenance":    provenance,
        "has_context":   bool(context_block.strip()),
    }


def build_vault_prompt_block(query: str) -> str:
    """
    Genera el bloque de contexto vault listo para inyectar en el system prompt.
    Retorna "" si la query no activa ningun SAT ni dimension.
    """
    result = get_vault_normative_context(query)
    if not result["has_context"]:
        return ""

    header = (
        "CONOCIMIENTO NORMATIVO INSTITUCIONAL"
        " (Vault QUIRA KB — verificado · no inventar):"
    )
    footer = (
        "  Al citar: referencia la nota del vault como fuente institucional."
        " No inventes artículos fuera de este bloque."
    )
    return "\n".join([header, result["context_block"], footer])


def format_provenance(provenance: list[dict]) -> str:
    """
    Formatea provenance como texto auditable para logs y debug panel.
    """
    if not provenance:
        return "Sin contexto vault activado para esta query."
    lines = ["Provenance normativo (Vault QUIRA KB):"]
    for p in provenance:
        sat  = p.get("sat_trigger") or "dim-match"
        dims = "|".join(p.get("dimension", [])) or "?"
        ev   = p.get("evidencia", "")
        lines.append(
            f"  . {p['nota'][:55]}"
            f" | SAT:{sat}"
            f" | Dim:{dims}"
            + (f" | Ev:{ev[:40]}" if ev else "")
        )
    return "\n".join(lines)


def provenance_to_dict(vault_ctx: dict) -> dict:
    """
    Convierte el resultado de get_vault_normative_context()
    a un dict serializable para audit_log y session_state.
    """
    return {
        "sat_codes":  vault_ctx.get("sat_codes", []),
        "dimensions": vault_ctx.get("dimensions", []),
        "notas":      [
            {
                "nota":      p["nota"],
                "sat":       p.get("sat_trigger"),
                "dimension": p.get("dimension", []),
            }
            for p in vault_ctx.get("provenance", [])
        ],
        "has_context": vault_ctx.get("has_context", False),
    }
