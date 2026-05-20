"""
SENTINEL · legal_router.py
Motor de Referencia Normativa — Sprint Legal v1.
Fuentes: COOTAD · COPLAFIP · Ley Reformatoria 2026.
Sin RAG, sin vector DB — keyword routing determinístico, 100% trazable.
Doctrina: cada recomendación debe poder defenderse frente a Contraloría, Concejo y ciudadanía.
Dylus Lab © 2026
"""
from __future__ import annotations
import json
import unicodedata
from pathlib import Path
import streamlit as st

_CHUNKS_PATH = Path(__file__).parent.parent / "knowledge_base" / "legal" / "legal_chunks.json"

# ── ROUTING MAP — keywords → artículos relevantes ──────────────────────────────
# Cada entrada: lista de términos de trigger → lista de (law, article)
_ROUTES: list[tuple[list[str], list[tuple[str, str]]]] = [
    # Agua y servicios básicos
    (["agua", "potable", "alcantarillado", "saneamiento", "hidric"],
     [("COOTAD", "Art.55"), ("COPLAFIP", "Art.97")]),

    # Presupuesto participativo
    (["presupuesto participativo", "pp 2026", "priorización", "fichas", "talleres participativos"],
     [("COOTAD", "Art.238"), ("COOTAD", "Art.302"), ("COOTAD", "Art.303")]),

    # Inversión, transferencias y distribución
    (["inversion", "transferencias", "recursos", "per capita", "distribución fondos"],
     [("COOTAD", "Art.272"), ("COPLAFIP", "Art.98"), ("COPLAFIP", "Art.118")]),

    # POA y programación operativa
    (["poa", "plan operativo", "programacion anual", "programación"],
     [("COPLAFIP", "Art.28"), ("COPLAFIP", "Art.97"), ("COPLAFIP", "Art.98")]),

    # PAC y contratación pública
    (["pac", "contratacion", "contratación", "sercop", "adquisiciones"],
     [("COPLAFIP", "Art.100"), ("COOTAD", "Art.432")]),

    # Ejecución presupuestaria y reforma
    (["ejecucion presupuestaria", "devengado", "reforma presupuestaria", "reasignacion"],
     [("COPLAFIP", "Art.100"), ("COPLAFIP", "Art.101"), ("COOTAD", "Art.432")]),

    # PDOT y planificación territorial
    (["pdot", "planificacion territorial", "ordenamiento", "plan de desarrollo"],
     [("COOTAD", "Art.302"), ("COPLAFIP", "Art.118"), ("COPLAFIP", "Art.4")]),

    # Gobernanza y participación
    (["gobernanza", "participacion ciudadana", "asambleas", "cpccs"],
     [("COOTAD", "Art.303"), ("COOTAD", "Art.304"), ("COOTAD", "Art.305")]),

    # Competencias del Concejo y alcalde
    (["concejo", "alcalde", "sesion", "resolucion", "normativa municipal"],
     [("COOTAD", "Art.57"), ("COOTAD", "Art.305")]),

    # Finanzas y sostenibilidad fiscal
    (["finanzas", "sostenibilidad fiscal", "isp", "salud presupuestaria", "deuda"],
     [("COPLAFIP", "Art.5"), ("COOTAD_2026", "Art.192"), ("COPLAFIP", "Art.119")]),

    # Reforma COOTAD 2026
    (["reforma 2026", "eficiencia gasto", "sostenibilidad gad", "ley reformatoria"],
     [("COOTAD_2026", "Art.1"), ("COOTAD_2026", "Art.2"), ("COOTAD_2026", "Art.3")]),

    # NBI y equidad territorial
    (["nbi", "brecha territorial", "equidad", "inequidad", "iet"],
     [("COOTAD", "Art.272"), ("COOTAD", "Art.302"), ("CRE", "Art.340")]),

    # ── Constitución de la República del Ecuador (CRE) ─────────────────────────

    # Agua — fundamento constitucional (Art. 12 CRE)
    (["agua", "potable", "hidric", "derecho al agua", "patrimonio hidrico"],
     [("CRE", "Art.12"), ("COOTAD", "Art.55")]),

    # Ambiente, sostenibilidad y Buen Vivir
    (["ambiente sano", "buen vivir", "sumak kawsay", "ecosistema", "sostenibilidad ambiental"],
     [("CRE", "Art.14"), ("CRE", "Art.275")]),

    # Participación ciudadana — base constitucional del PP
    (["participacion ciudadana", "presupuesto participativo", "asambleas", "democracia participativa"],
     [("CRE", "Art.95"), ("COOTAD", "Art.303")]),

    # Competencias municipales — base constitucional del COOTAD
    (["competencias", "gobierno municipal", "gad municipal", "constitucion"],
     [("CRE", "Art.264"), ("COOTAD", "Art.55"), ("COOTAD", "Art.57")]),

    # Competencias parroquiales rurales
    (["parroquia rural", "gobierno parroquial", "jap", "competencias parroquial"],
     [("CRE", "Art.267"), ("COOTAD", "Art.302")]),

    # Régimen del Buen Vivir y planificación
    (["buen vivir", "sumak kawsay", "regimen desarrollo", "desarrollo cantonal"],
     [("CRE", "Art.275"), ("COPLAFIP", "Art.4")]),

    # Equidad social, NBI y pobreza
    (["inclusion social", "erradicacion pobreza", "proteccion integral", "sistema equidad"],
     [("CRE", "Art.340"), ("CRE", "Art.341"), ("COOTAD", "Art.272")]),

    # Salud como derecho vinculado a servicios básicos
    (["salud", "sistema salud", "derecho salud"],
     [("CRE", "Art.32")]),
]


# ── HELPERS ────────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


@st.cache_data(show_spinner=False)
def _load_chunks() -> list[dict]:
    if _CHUNKS_PATH.exists():
        with open(_CHUNKS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def _find_chunk(chunks: list[dict], law: str, article: str) -> dict | None:
    for c in chunks:
        if c["law"] == law and c["article"] == article:
            return c
    return None


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def find_legal_refs(query: str, max_refs: int = 3) -> list[dict]:
    """
    Retorna los artículos legales más relevantes para la query dada.
    Usa keyword routing determinístico — sin embeddings, sin LLM.

    Returns:
        list de dicts: [{law, article, topic, text, keywords}]
    """
    chunks = _load_chunks()
    q      = _norm(query)
    seen   = set()
    refs   = []

    for triggers, targets in _ROUTES:
        if any(t in q for t in triggers):
            for law, article in targets:
                key = f"{law}:{article}"
                if key not in seen:
                    chunk = _find_chunk(chunks, law, article)
                    if chunk:
                        refs.append(chunk)
                        seen.add(key)
                    if len(refs) >= max_refs:
                        break
        if len(refs) >= max_refs:
            break

    return refs[:max_refs]


def has_legal_refs(query: str) -> bool:
    """True si la query activa alguna referencia legal."""
    q = _norm(query)
    return any(any(t in q for t in triggers) for triggers, _ in _ROUTES)


def format_legal_citation(ref: dict) -> str:
    """Formatea una referencia como cita inline para Sentinel."""
    law_labels = {
        "COOTAD":      "COOTAD",
        "COPLAFIP":    "COPLAFIP",
        "COOTAD_2026": "COOTAD Reforma 2026",
        "CRE":         "Constitución (CRE)",
    }
    label = law_labels.get(ref["law"], ref["law"])
    return f"{label} {ref['article']} — {ref['topic']}"


def build_legal_prompt_block(query: str) -> str:
    """
    Genera bloque normativo enriquecido para inyectar al system prompt de Claude.

    Dos capas (P3 — Loop Semantico):
      1. Marco normativo estatico (COOTAD/COPLAFIP/CRE) -- keyword determinístico
      2. Contexto vault Obsidian (notas institucionales verificadas) -- P3 bridge

    Solo activa cuando la query toca temas legales o institucionales.
    """
    refs = find_legal_refs(query, max_refs=2)

    # ---- Capa 1: Marco legal estatico (base inmutable) ----------------------
    static_lines: list[str] = []
    if refs:
        static_lines.append("MARCO NORMATIVO APLICABLE (citar si es relevante):")
        for r in refs:
            law_label = {
                "COOTAD":      "COOTAD",
                "COPLAFIP":    "COPLAFIP",
                "COOTAD_2026": "COOTAD Reforma 2026",
                "CRE":         "Constitucion (CRE)",
            }.get(r["law"], r["law"])
            static_lines.append(
                f"  {law_label} {r['article']}: {r['text'][:200]}..."
            )
        static_lines.append(
            "  Al citar: indica 'conforme [LEY] [Art.X]' -- no inventes articulos."
        )

        reason = get_reason_path(query, refs)
        if reason:
            static_lines.append("")
            static_lines.append("RUTA PROCEDIMENTAL APLICABLE:")
            static_lines.append(f"  {reason}")

    # ---- Capa 2: Contexto vault (P3 enriquecimiento) ------------------------
    vault_block = ""
    try:
        from sentinel.vault_enricher import build_vault_prompt_block
        vault_block = build_vault_prompt_block(query)
    except Exception:
        pass  # vault no disponible -- continua sin el

    # ---- Ensamblar bloque final ---------------------------------------------
    parts: list[str] = []
    if static_lines:
        parts.append("\n".join(static_lines))
    if vault_block:
        parts.append(vault_block)

    return "\n\n".join(parts) if parts else ""


# ── INTENTS — clasificación por propósito institucional ───────────────────────

_INTENT_LABELS: dict[str, str] = {
    "agua_potable":       "Prestación de servicio de agua y saneamiento",
    "presupuesto":        "Planificación y aprobación presupuestaria",
    "reforma_poa":        "Reforma al POA/PAC y modificaciones presupuestarias",
    "competencias":       "Competencias constitucionales y legales del GAD",
    "contratacion":       "Contratación pública y procesos SERCOP",
    "participacion":      "Participación ciudadana y presupuesto participativo",
    "gobernanza":         "Gobernanza institucional y eficiencia GAD",
    "equidad_territorial":"Equidad territorial e inversión redistributiva",
    "planificacion":      "Planificación territorial y PDOT",
    "finanzas":           "Sostenibilidad fiscal y finanzas municipales",
    "derechos":           "Derechos constitucionales y garantías",
}

# Rutas procedimentales por intent — lo que Sentinel razona, no solo cita
_REASON_PATHS: dict[str, str] = {
    "reforma_poa": (
        "La reforma presupuestaria es viable. Requiere: (1) informe técnico de la Dirección "
        "de Planificación que justifique la reasignación; (2) consistencia con metas PDOT vigentes; "
        "(3) reforma al POA aprobada por el Alcalde; (4) si supera el 10% del presupuesto, "
        "requiere resolución del Concejo Municipal. Riesgo: Medio."
    ),
    "contratacion": (
        "La contratación debe seguir el régimen SERCOP: (1) verificar umbral (ínfima cuantía / "
        "menor cuantía / cotización / licitación); (2) inclusión en PAC vigente o reforma PAC; "
        "(3) certificación presupuestaria previa; (4) proceso en COMPRASPÚBLICAS. Riesgo: Bajo si "
        "el proceso se documenta correctamente desde inicio."
    ),
    "agua_potable": (
        "La inversión en agua es competencia exclusiva del GAD Municipal (CRE Art.264 + COOTAD "
        "Art.55). El derecho constitucional al agua (CRE Art.12) genera obligación de provisión. "
        "Puede financiarse con recursos propios, transferencias del Estado, o cooperación. "
        "Requiere inclusión en POA/PAC y proceso de contratación. Riesgo: Bajo."
    ),
    "participacion": (
        "El presupuesto participativo es obligatorio (COOTAD Art.238). Requiere: (1) convocatoria "
        "pública documentada; (2) talleres en las 7 parroquias con acta oficial; (3) fichas de "
        "priorización ciudadana; (4) incorporación al POA. Omitirlo genera observación de Contraloría."
    ),
    "equidad_territorial": (
        "La distribución equitativa de inversión es mandato constitucional (CRE Art.340) y legal "
        "(COOTAD Art.272). Las parroquias con mayor NBI tienen derecho preferente de inversión. "
        "El GAD debe documentar el criterio de distribución para la RDC y ante Contraloría."
    ),
}


def find_refs_by_intent(intent: str, max_refs: int = 3) -> list[dict]:
    """Retorna artículos clasificados bajo un intent específico."""
    chunks = _load_chunks()
    return [c for c in chunks if c.get("intent") == intent][:max_refs]


def get_intents_from_refs(refs: list[dict]) -> list[str]:
    """Extrae los intents únicos presentes en una lista de referencias."""
    seen, result = set(), []
    for r in refs:
        i = r.get("intent", "general")
        if i not in seen:
            seen.add(i)
            result.append(i)
    return result


def get_reason_path(query: str, refs: list[dict] | None = None) -> str:
    """
    Retorna la ruta procedimental aplicable según los intents de la query.
    Permite que Sentinel razone sobre viabilidad, no solo cite artículos.

    Returns: string con la ruta procedimental, o "" si no aplica.
    """
    q = _norm(query)

    # Detectar si es pregunta de viabilidad
    viabilidad_triggers = [
        "puedo", "podemos", "es posible", "esta permitido", "permite",
        "viable", "reasignar", "modificar", "reformar", "cambiar el poa",
        "cambiar presupuesto", "contratar", "adjudicar", "priorizar",
    ]
    if not any(t in q for t in viabilidad_triggers):
        return ""

    # Detección directa de intent por keywords de la query (prioridad sobre refs)
    _QUERY_INTENTS: list[tuple[list[str], str]] = [
        (["poa", "presupuesto", "reasignar", "reformar presupuesto", "modificar presupuesto"], "reforma_poa"),
        (["contratar", "contratacion", "licitacion", "adjudicar", "pac"], "contratacion"),
        (["participativo", "pp 2026", "talleres", "fichas", "asamblea"], "participacion"),
        (["agua", "potable", "hidric", "saneamiento"], "agua_potable"),
        (["equidad", "iet", "nbi", "brecha", "inequidad"], "equidad_territorial"),
    ]
    for kws, intent in _QUERY_INTENTS:
        if any(k in q for k in kws):
            path = _REASON_PATHS.get(intent, "")
            if path:
                return path

    # Fallback: intent desde los refs
    active_refs = refs or find_legal_refs(query, max_refs=3)
    intents     = get_intents_from_refs(active_refs)
    for intent in intents:
        path = _REASON_PATHS.get(intent, "")
        if path:
            return path

    return ""
