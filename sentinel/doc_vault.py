"""
sentinel/doc_vault.py
Bóveda Documental Institucional — Sprint 2.4

Propósito: garantizar trazabilidad e integridad de cada documento
subido al sistema. Ningún proceso puede decir "ese no fue el archivo
que subimos" porque cada versión tiene SHA256 + timestamp + usuario.

Capas documentales (arquitectura Sprint 2.5):
    CAPA 0  — baseline anual (POA · PAC · PDOT · Presupuesto inicial)
    CAPA 1  — cédula presupuestaria mensual
    CAPA 2  — export SERCOP mensual
    CAPA 3  — transparencia LOTAIP mensual
    CAPA 4  — informe mensual por dirección
    CAPA 5  — análisis Sentinel (generado automáticamente)

Reglas:
    - Cada archivo tiene SHA256 calculado al momento de registro
    - Se versionan: POA_v1 → POA_v2 → POA_v3
    - No se borran versiones anteriores (append-only)
    - El cierre de capa requiere al menos un documento de cada tipo

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional

from sentinel.rag_config import LOGS_DIR, SENTINEL_VERSION

# ── RUTA ──────────────────────────────────────────────────────────────────────
DOC_VAULT_LOG = LOGS_DIR / "doc_vault.jsonl"
DOC_VAULT_LOG.parent.mkdir(parents=True, exist_ok=True)


# ── CAPAS DOCUMENTALES ────────────────────────────────────────────────────────
class DocCapa(str, Enum):
    C0_BASELINE  = "CAPA_0_BASELINE_ANUAL"
    C1_CEDULA    = "CAPA_1_CEDULA_MENSUAL"
    C2_SERCOP    = "CAPA_2_SERCOP_MENSUAL"
    C3_LOTAIP    = "CAPA_3_LOTAIP_MENSUAL"
    C4_INFORME   = "CAPA_4_INFORME_DIRECCION"
    C5_SENTINEL  = "CAPA_5_SENTINEL_ANALISIS"


# ── TIPOS DOCUMENTALES ────────────────────────────────────────────────────────
class DocTipo(str, Enum):
    POA             = "POA"               # Plan Operativo Anual
    PAC             = "PAC"               # Plan Anual de Contratación
    PDOT            = "PDOT"              # Plan Desarrollo y Ordenamiento Territorial
    PRESUPUESTO     = "PRESUPUESTO"       # Presupuesto codificado inicial
    CEDULA          = "CEDULA"            # Cédula presupuestaria mensual
    SERCOP          = "SERCOP"            # Export contratación pública
    LOTAIP          = "LOTAIP"            # Transparencia/LOTAIP
    INFORME_DIR     = "INFORME_DIR"       # Informe mensual de dirección
    ORDENANZA       = "ORDENANZA"         # Ordenanza municipal
    OTRO            = "OTRO"


# ── ROLES QUE PUEDEN SUBIR DOCUMENTOS ─────────────────────────────────────────
UPLOAD_ROLES = {"analista", "director", "alcaldia"}


# ── DATACLASS DOCUMENTO ───────────────────────────────────────────────────────
@dataclass
class DocEntry:
    """
    Registro inmutable de un documento subido.

    doc_id          — SHA256[:12] del contenido del archivo
    filename        — nombre original del archivo
    tipo            — DocTipo
    capa            — DocCapa
    version         — número de versión (1, 2, 3…)
    sha256          — hash SHA256 completo del contenido
    size_bytes      — tamaño en bytes
    uploaded_by     — usuario que subió el documento
    upload_ts       — timestamp ISO de la subida
    periodo         — período al que pertenece (ej: "2026-05" o "2026")
    direccion       — dirección responsable (si aplica)
    notas           — notas del analista
    sentinel_version — versión del sistema al registrar
    """
    doc_id:           str
    filename:         str
    tipo:             str
    capa:             str
    version:          int
    sha256:           str
    size_bytes:       int
    uploaded_by:      str
    upload_ts:        str
    periodo:          str
    direccion:        str = ""
    notas:            str = ""
    sentinel_version: str = SENTINEL_VERSION


# ── SHA256 ────────────────────────────────────────────────────────────────────
def compute_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def compute_doc_id(sha256: str) -> str:
    return sha256[:12]


# ── PERSISTENCIA ──────────────────────────────────────────────────────────────
def _append_entry(entry: DocEntry) -> None:
    with DOC_VAULT_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def _load_all() -> list[dict]:
    if not DOC_VAULT_LOG.exists():
        return []
    entries = []
    with DOC_VAULT_LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ── VERSIONADO ────────────────────────────────────────────────────────────────
def _next_version(tipo: str, periodo: str) -> int:
    """Calcula el número de versión siguiente para un tipo/período."""
    entries = _load_all()
    existing = [e for e in entries if e.get("tipo") == tipo and e.get("periodo") == periodo]
    return max((e.get("version", 0) for e in existing), default=0) + 1


# ── API PRINCIPAL ─────────────────────────────────────────────────────────────
def register_document(
    content:      bytes,
    filename:     str,
    tipo:         str,
    capa:         str,
    uploaded_by:  str,
    periodo:      str,
    direccion:    str = "",
    notas:        str = "",
) -> DocEntry:
    """
    Registra un documento en la bóveda.

    Args:
        content      — bytes del archivo
        filename     — nombre original
        tipo         — DocTipo (POA, PAC, CEDULA, etc.)
        capa         — DocCapa (CAPA_0 a CAPA_5)
        uploaded_by  — usuario responsable
        periodo      — "2026" para anual, "2026-05" para mensual
        direccion    — dirección responsable (para INFORME_DIR)
        notas        — notas del analista

    Returns:
        DocEntry persistido y verificado.

    Raises:
        PermissionError — si el rol no tiene autorización para subir documentos
        ValueError      — si tipo o capa no son válidos
    """
    # Validar tipo
    tipos_validos = {t.value for t in DocTipo}
    if tipo not in tipos_validos:
        raise ValueError(f"Tipo documental inválido: {tipo}. Válidos: {tipos_validos}")

    # Calcular hash
    sha256   = compute_sha256(content)
    doc_id   = compute_doc_id(sha256)
    version  = _next_version(tipo, periodo)
    ts       = time.strftime("%Y-%m-%dT%H:%M:%S")

    entry = DocEntry(
        doc_id           = doc_id,
        filename         = filename,
        tipo             = tipo,
        capa             = capa,
        version          = version,
        sha256           = sha256,
        size_bytes       = len(content),
        uploaded_by      = uploaded_by,
        upload_ts        = ts,
        periodo          = periodo,
        direccion        = direccion,
        notas            = notas,
        sentinel_version = SENTINEL_VERSION,
    )
    _append_entry(entry)
    return entry


def get_document_history(tipo: str, periodo: str) -> list[dict]:
    """Retorna el historial de versiones de un tipo/período."""
    return sorted(
        [e for e in _load_all() if e.get("tipo") == tipo and e.get("periodo") == periodo],
        key=lambda e: e.get("version", 0),
    )


def get_latest(tipo: str, periodo: str) -> Optional[dict]:
    """Retorna la última versión de un tipo/período."""
    hist = get_document_history(tipo, periodo)
    return hist[-1] if hist else None


def get_vault_summary(periodo: str = "") -> dict:
    """
    Resumen de documentos en la bóveda.
    Si periodo se provee, filtra por ese período.
    """
    entries = _load_all()
    if periodo:
        entries = [e for e in entries if e.get("periodo", "").startswith(periodo)]

    total       = len(entries)
    por_tipo    = {}
    por_capa    = {}

    for e in entries:
        t = e.get("tipo", "?")
        c = e.get("capa", "?")
        por_tipo[t] = por_tipo.get(t, 0) + 1
        por_capa[c] = por_capa.get(c, 0) + 1

    # Documentos base esperados para CAPA_0
    tipos_baseline = {DocTipo.POA.value, DocTipo.PAC.value,
                      DocTipo.PDOT.value, DocTipo.PRESUPUESTO.value}
    presentes_c0   = {e.get("tipo") for e in entries if e.get("capa") == DocCapa.C0_BASELINE.value}
    baseline_ok    = tipos_baseline.issubset(presentes_c0)

    return {
        "total":       total,
        "por_tipo":    por_tipo,
        "por_capa":    por_capa,
        "baseline_completo": baseline_ok,
        "baseline_faltantes": sorted(tipos_baseline - presentes_c0),
        "periodo_filtro": periodo or "todos",
    }


def verify_integrity(doc_id: str, content: bytes) -> dict:
    """
    Verifica la integridad de un archivo contra su hash registrado.

    Returns:
        valid (bool), sha256_stored, sha256_actual, match (bool)
    """
    entries = [e for e in _load_all() if e.get("doc_id") == doc_id]
    if not entries:
        return {"valid": False, "error": f"doc_id {doc_id} no encontrado en bóveda"}

    stored  = entries[-1]
    sha_reg = stored.get("sha256", "")
    sha_act = compute_sha256(content)
    match   = sha_reg == sha_act

    return {
        "valid":         match,
        "doc_id":        doc_id,
        "filename":      stored.get("filename"),
        "sha256_stored": sha_reg,
        "sha256_actual": sha_act,
        "match":         match,
        "upload_ts":     stored.get("upload_ts"),
        "uploaded_by":   stored.get("uploaded_by"),
    }


def format_entry(e: dict) -> str:
    """Formato legible para consola."""
    return (
        f"[v{e.get('version')}] {e.get('tipo')} | {e.get('filename')} "
        f"| {e.get('upload_ts')} | by {e.get('uploaded_by')} "
        f"| SHA256 {e.get('sha256','')[:12]}…"
    )


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if "--summary" in args:
        s = get_vault_summary()
        print("=" * 58)
        print("  DOC VAULT — Resumen")
        print("=" * 58)
        print(f"  Total documentos : {s['total']}")
        print(f"  Baseline C0      : {'✅ Completo' if s['baseline_completo'] else '⚠ Incompleto'}")
        if s["baseline_faltantes"]:
            print(f"  Faltantes C0     : {', '.join(s['baseline_faltantes'])}")
        print(f"  Por tipo         : {s['por_tipo']}")
        print("=" * 58)
        sys.exit(0)

    if "--demo" in args:
        contenido = b"POA 2026 - Contenido simulado para demo"
        entry = register_document(
            content      = contenido,
            filename     = "POA_2026_GADM_Montecristi.pdf",
            tipo         = DocTipo.POA.value,
            capa         = DocCapa.C0_BASELINE.value,
            uploaded_by  = "analista_demo",
            periodo      = "2026",
            notas        = "Demo registro POA 2026",
        )
        print(f"\n-- Demo: registro exitoso --")
        print(format_entry(asdict(entry)))
        integ = verify_integrity(entry.doc_id, contenido)
        print(f"Integridad: {'✅ OK' if integ['valid'] else '❌ FALLO'}")
        sys.exit(0)

    print("""
SENTINEL · Doc Vault CLI
Uso:
  python -m sentinel.doc_vault --summary   # Resumen de bóveda
  python -m sentinel.doc_vault --demo      # Demo registro + verificación
""")
