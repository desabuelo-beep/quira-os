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
     [("COOTAD", "Art.272"), ("COOTAD", "Art.302")]),
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
        "COOTAD":     "COOTAD",
        "COPLAFIP":   "COPLAFIP",
        "COOTAD_2026": "COOTAD Reforma 2026",
    }
    label = law_labels.get(ref["law"], ref["law"])
    return f"{label} {ref['article']} — {ref['topic']}"


def build_legal_prompt_block(query: str) -> str:
    """
    Genera bloque normativo para inyectar al system prompt de Groq.
    Solo se activa cuando la query toca temas legales — mantiene el prompt ligero.
    """
    refs = find_legal_refs(query, max_refs=2)
    if not refs:
        return ""

    lines = ["MARCO NORMATIVO APLICABLE (citar si es relevante):"]
    for r in refs:
        law_label = {"COOTAD": "COOTAD", "COPLAFIP": "COPLAFIP",
                     "COOTAD_2026": "COOTAD Reforma 2026"}.get(r["law"], r["law"])
        lines.append(f"  {law_label} {r['article']}: {r['text'][:200]}...")
    lines.append("  Al citar: indica 'conforme [LEY] [Art.X]' — no inventes artículos.")
    return "\n".join(lines)
