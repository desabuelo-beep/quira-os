"""
QUIRA OS v0.1 — obsidian_bridge.py
Puente Obsidian → QUIRA Engine · Sprint Bridge-v1

Lee el vault Obsidian QUIRA_KB_Montecristi, parsea frontmatter YAML de todas
las notas y construye un registry estructurado que:
  · expone competencias normativas (legal_router dinámico)
  · indexa SAT triggers por código de alerta
  · agrupa notas por dimensión TGI
  · registra evidencias requeridas por nota
  · genera vault_registry.json como artefacto persistente

Filosofía: el vault es READ-ONLY para el engine. Nunca escribe en Obsidian.
El bridge actualiza vault_registry.json; el engine lo consume vía API.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Optional

try:
    import yaml
    _YAML_OK = True
except ImportError:
    _YAML_OK = False

# ── RUTAS ─────────────────────────────────────────────────────────────────────
_VAULT_DEFAULT = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi")
_REGISTRY_PATH = Path(__file__).parent / "vault_registry.json"
_SCHEMA_PATH   = Path(__file__).parent / "vault_schema.json"

# ── ALIAS MAP — cargado desde vault_schema.json ───────────────────────────────
def _load_alias_map() -> dict[str, str]:
    """Carga el mapa de aliases canónicos desde vault_schema.json."""
    try:
        schema = json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        return schema.get("alias_map", {})
    except Exception:
        return {}

_ALIAS_MAP: dict[str, str] = _load_alias_map()


def normalize_dimension(dim: str) -> str:
    """
    Normaliza un valor dimension_tgi al ID canónico v1.0.
    Ej: 'D1_Legalidad_Coherencia' → 'D1_LEGALIDAD'
    Valores ya canónicos (D1_LEGALIDAD, etc.) se devuelven sin cambio.
    """
    return _ALIAS_MAP.get(dim, dim)

# ── CAMPOS EXTRAÍDOS DEL FRONTMATTER ─────────────────────────────────────────
_CORE_FIELDS = [
    "name", "tipo", "tipo_nota", "description", "dimension_tgi",
    "competencia", "sat_trigger", "evidencia_requerida",
    "articulos", "normativa", "base_legal", "norma_habilitante",
    "tags", "etiquetas", "gold_master", "sentinel_sprint",
    "fecha", "fecha_actualizacion", "estado", "scope",
    "ley", "registro_oficial", "sancion",
]


# ── PARSER YAML FRONTMATTER ────────────────────────────────────────────────────
def _parse_frontmatter(path: Path) -> Optional[dict]:
    """
    Extrae el YAML frontmatter de un archivo .md.
    Retorna None si no hay frontmatter o si el parse falla.
    """
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    # Busca el cierre ---
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return None

    fm_text = content[3:end_idx].strip()
    if not fm_text:
        return None

    if _YAML_OK:
        try:
            fm = yaml.safe_load(fm_text)
            return fm if isinstance(fm, dict) else None
        except Exception:
            pass

    # Fallback: parser manual de key: value
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm if fm else None


def _extract_core(fm: dict, rel_path: str) -> dict:
    """Extrae solo los campos relevantes del frontmatter completo."""
    core = {"_path": rel_path}
    for field in _CORE_FIELDS:
        val = fm.get(field)
        if val is not None:
            core[field] = val

    # Normalizar sat_trigger a lista de strings
    st = core.get("sat_trigger")
    if st is None:
        core["sat_trigger"] = []
    elif isinstance(st, str):
        core["sat_trigger"] = [s.strip() for s in re.split(r"[,\s]+", st) if s.strip()]
    elif isinstance(st, list):
        core["sat_trigger"] = [str(s).strip() for s in st if s]
    else:
        core["sat_trigger"] = []

    # Normalizar dimension_tgi a lista de IDs canónicos
    dim = core.get("dimension_tgi")
    if dim is None:
        core["dimension_tgi"] = []
    elif isinstance(dim, str):
        core["dimension_tgi"] = [normalize_dimension(dim)]
    elif isinstance(dim, list):
        core["dimension_tgi"] = [normalize_dimension(str(d)) for d in dim]
    else:
        core["dimension_tgi"] = []

    # Normalizar tags
    tags = core.get("tags") or core.get("etiquetas")
    if isinstance(tags, list):
        core["tags"] = tags
    elif isinstance(tags, str):
        core["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
    else:
        core["tags"] = []

    return core


# ── BUILD REGISTRY ─────────────────────────────────────────────────────────────
def build_registry(vault_path: Path = _VAULT_DEFAULT) -> dict:
    """
    Escanea el vault y construye el registry completo.

    Returns:
        dict con claves: _meta, notas, sat_triggers, por_dimension,
                         competencias, evidencias
    """
    notas: list[dict] = []
    errores: list[str] = []
    total_files = 0

    for md_path in sorted(vault_path.rglob("*.md")):
        # Excluir archivos del sistema Obsidian
        parts = md_path.parts
        if any(p.startswith(".") for p in parts):
            continue

        total_files += 1
        fm = _parse_frontmatter(md_path)
        if fm is None:
            continue

        rel = str(md_path.relative_to(vault_path))
        core = _extract_core(fm, rel)
        notas.append(core)

    # ── Índice SAT triggers ──────────────────────────────────────────────────
    sat_index: dict[str, list[str]] = {}
    for n in notas:
        path = n.get("name") or n["_path"]
        for sat in n.get("sat_trigger", []):
            sat_clean = sat.upper().strip()
            if sat_clean:
                sat_index.setdefault(sat_clean, [])
                if path not in sat_index[sat_clean]:
                    sat_index[sat_clean].append(path)

    # ── Índice por dimensión TGI ─────────────────────────────────────────────
    dim_index: dict[str, list[str]] = {}
    for n in notas:
        path = n.get("name") or n["_path"]
        for dim in n.get("dimension_tgi", []):
            dim_index.setdefault(dim, [])
            if path not in dim_index[dim]:
                dim_index[dim].append(path)

    # ── Competencias (notas normativas con competencia declarada) ────────────
    competencias: list[dict] = [
        {
            "nota":          n.get("name") or n["_path"],
            "path":          n["_path"],
            "tipo":          n.get("tipo") or n.get("tipo_nota", ""),
            "competencia":   str(n.get("competencia", "")),
            "sat_triggers":  n.get("sat_trigger", []),
            "dimension_tgi": n.get("dimension_tgi", []),
            "articulos":     n.get("articulos") or n.get("norma_habilitante", ""),
        }
        for n in notas
        if n.get("competencia")
    ]

    # ── Evidencias requeridas ────────────────────────────────────────────────
    evidencias: dict[str, list[str]] = {}
    for n in notas:
        ev = n.get("evidencia_requerida")
        if ev:
            nota_id = n.get("name") or n["_path"]
            if isinstance(ev, list):
                evidencias[nota_id] = ev
            elif isinstance(ev, str):
                evidencias[nota_id] = [ev]

    registry = {
        "_meta": {
            "vault_path":        str(vault_path),
            "generado":          str(date.today()),
            "notas_escaneadas":  total_files,
            "notas_con_fm":      len(notas),
            "notas_con_sat":     sum(1 for n in notas if n.get("sat_trigger")),
            "notas_con_comp":    len(competencias),
            "sat_tipos":         sorted(sat_index.keys()),
            "dimensiones":       sorted(dim_index.keys()),
            "version":           "bridge_v1",
            "bridge_fuente":     "QUIRA_KB_Montecristi · frontmatter YAML",
        },
        "competencias":   competencias,
        "sat_triggers":   sat_index,
        "por_dimension":  dim_index,
        "evidencias":     evidencias,
        "notas":          notas,
    }
    return registry


# ── PERSISTENCIA ──────────────────────────────────────────────────────────────
def _json_default(obj):
    """Serializer JSON para tipos no estándar (date, datetime, Path)."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if isinstance(obj, Path):
        return str(obj)
    return str(obj)


def save_registry(registry: dict, path: Path = _REGISTRY_PATH) -> Path:
    """Serializa el registry a JSON."""
    path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2, default=_json_default),
        encoding="utf-8"
    )
    return path


def load_registry(path: Path = _REGISTRY_PATH) -> Optional[dict]:
    """Carga el registry desde JSON. Retorna None si no existe."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ── API PÚBLICA ───────────────────────────────────────────────────────────────
def get_registry(force_rebuild: bool = False) -> dict:
    """
    Retorna el registry del vault.
    Usa caché (vault_registry.json) salvo que force_rebuild=True.
    """
    if not force_rebuild:
        cached = load_registry()
        if cached:
            return cached
    reg = build_registry()
    save_registry(reg)
    return reg


def get_sat_notas(sat_codigo: str, registry: Optional[dict] = None) -> list[str]:
    """Retorna notas del vault que disparan un SAT dado (ej: 'SAT-X-A')."""
    reg = registry or get_registry()
    return reg.get("sat_triggers", {}).get(sat_codigo.upper(), [])


def get_notas_dimension(dimension: str, registry: Optional[dict] = None) -> list[str]:
    """Retorna notas vinculadas a una dimensión TGI (ej: 'D3_Ejecucion_Presupuestaria')."""
    reg = registry or get_registry()
    for key, notas in reg.get("por_dimension", {}).items():
        if dimension.lower() in key.lower():
            return notas
    return []


def get_competencia_nota(nombre: str, registry: Optional[dict] = None) -> Optional[dict]:
    """Busca una nota de competencia por nombre (case-insensitive)."""
    reg = registry or get_registry()
    for c in reg.get("competencias", []):
        if nombre.lower() in c.get("nota", "").lower():
            return c
    return None


def get_evidencias_requeridas(nombre_nota: str, registry: Optional[dict] = None) -> list[str]:
    """Retorna la lista de evidencias requeridas para una nota."""
    reg = registry or get_registry()
    return reg.get("evidencias", {}).get(nombre_nota, [])


def sat_context_for_legal_router(sat_codigo: str, registry: Optional[dict] = None) -> str:
    """
    Genera un bloque de texto contextual sobre las notas normativas
    asociadas a un SAT, para enriquecer las respuestas del legal_router.
    Formato compacto para inyección en prompts.
    """
    reg = registry or get_registry()
    notas_ids = get_sat_notas(sat_codigo, reg)
    if not notas_ids:
        return ""

    lines = [f"[Vault normativo — {sat_codigo}]"]
    notas_by_id = {
        (n.get("name") or n["_path"]): n
        for n in reg.get("notas", [])
    }

    for nota_id in notas_ids[:5]:  # Límite para control de tokens
        n = notas_by_id.get(nota_id)
        if not n:
            continue
        comp = n.get("competencia", "")
        arts = n.get("articulos") or n.get("norma_habilitante", "")
        ev = n.get("evidencia_requerida", "")
        desc = n.get("description", "")[:120]
        lines.append(
            f"  · {nota_id}"
            + (f" | Competencia: {str(comp)[:80]}" if comp else "")
            + (f" | Arts: {str(arts)[:60]}" if arts else "")
            + (f" | Evidencia: {str(ev)[:60]}" if ev else "")
            + (f"\n    {desc}" if desc else "")
        )

    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    force = "--rebuild" in sys.argv
    print("Construyendo vault registry...")
    reg = build_registry()
    meta = reg["_meta"]

    print(f"\n{'='*60}")
    print(f"  VAULT: {meta['vault_path']}")
    print(f"  Generado: {meta['generado']}")
    print(f"  Notas escaneadas:     {meta['notas_escaneadas']}")
    print(f"  Notas con frontmatter:{meta['notas_con_fm']}")
    print(f"  Notas con SAT:        {meta['notas_con_sat']}")
    print(f"  Notas con competencia:{meta['notas_con_comp']}")
    print(f"  SAT tipos indexados:  {meta['sat_tipos']}")
    print(f"  Dimensiones TGI:      {len(meta['dimensiones'])}")
    print(f"{'='*60}")

    out = save_registry(reg)
    print(f"\nRegistry guardado en: {out}")

    # Test de API
    if reg["sat_triggers"]:
        sat_test = list(reg["sat_triggers"].keys())[0]
        print(f"\nTest get_sat_notas('{sat_test}'):")
        for n in get_sat_notas(sat_test, reg)[:3]:
            print(f"  · {n}")

        print(f"\nTest sat_context_for_legal_router('{sat_test}'):")
        ctx = sat_context_for_legal_router(sat_test, reg)
        print(ctx[:400] + ("..." if len(ctx) > 400 else ""))
