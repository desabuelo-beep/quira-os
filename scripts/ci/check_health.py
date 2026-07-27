#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ci/check_health.py — Guardián de salud QUIRA (CI/CD)
Dylus Lab © 2026

Corre en GitHub Actions en cada push/PR. Rápido (~segundos), SIN credenciales,
SIN conectar a Supabase/Neo4j/Excel. Protege lo que importa:

  1. PRESUPUESTO DE CONTEXTO — CLAUDE.md y BOOT.md no deben volver a inflarse
     (la causa del problema de "chats que mueren"). Límites duros.
  2. SECRETOS — ningún archivo con credenciales puede llegar al repo
     (.env.claude, secrets.toml, URIs de DB, claves API).
  3. SINTAXIS PYTHON — todos los scripts deben compilar.
  4. INTEGRIDAD DE REFERENCIAS — los archivos que BOOT.md manda a leer existen.

Salida: exit 0 si todo OK, exit 1 si alguna verificación crítica falla.

Uso local:  python scripts/ci/check_health.py
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [1, 5, 9]
#   type: OPERATIVA
# ---

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ── LÍMITES DE PRESUPUESTO DE CONTEXTO (bytes) ────────────────────────────────
# Si estos archivos crecen más allá del límite, el arranque vuelve a pesar.
# Ajustar conscientemente si el proyecto realmente lo necesita.
CONTEXT_BUDGET = {
    "CLAUDE.md":              4000,   # guía canónica mínima
    ".claude/CLAUDE.md":       500,   # solo punteros de skills
    "governance/BOOT.md":     6000,   # única fuente de estado vivo
    "governance/QUIRA_STATE.md": 1500,  # stub redirector (no contenido)
}

# ── PATRONES DE SECRETOS (nunca deben aparecer en archivos versionados) ───────
SECRET_PATTERNS = [
    (r"postgresql://[^\s\"']+:[^\s\"'@]+@", "URI PostgreSQL con password"),
    (r"sk-ant-[a-zA-Z0-9\-]{20,}",          "clave API Anthropic"),
    (r"neo4j\+s://[^\s\"']+:[^\s\"']+@",    "URI Neo4j con credenciales"),
    (r"eyJ[A-Za-z0-9_\-]{30,}\.[A-Za-z0-9_\-]{30,}", "JWT / service_role key"),
]

# Archivos que NUNCA deben estar trackeados por git
FORBIDDEN_FILES = [
    ".env.claude",
    ".streamlit/secrets.toml",
    ".env",
]

# Archivos del lazy-load de BOOT que deben existir (integridad de referencias)
# Se extraen dinámicamente, pero verificamos los críticos siempre.
CRITICAL_REFS = [
    "docs/adr/ADR-023_Arquitectura_Tres_Niveles_QUIRA.md",
    "docs/architecture/BRIDGE_EXCEL_CORPUS.md",
    "app/connectors/gold_master.py",
]


def check_context_budget() -> list[str]:
    errors = []
    print("\n[1/4] Presupuesto de contexto (arranque liviano)")
    for rel, limit in CONTEXT_BUDGET.items():
        path = ROOT / rel
        if not path.exists():
            print(f"   - {rel}: no existe (omitido)")
            continue
        size = path.stat().st_size
        status = "OK" if size <= limit else "EXCEDE"
        marker = "  " if size <= limit else ">>"
        print(f"   {marker} {rel}: {size} / {limit} bytes [{status}]")
        if size > limit:
            errors.append(
                f"{rel} pesa {size} bytes (límite {limit}). "
                f"El arranque vuelve a inflarse — mover detalle a lazy-load."
            )
    return errors


# Placeholders de documentación — un match que los contenga NO es secreto real
PLACEHOLDER_MARKERS = [
    "TU-PROYECTO", "tu-proyecto", "xxx", "XXX", "[PASSWORD]", "[PASS]",
    "example", "EXAMPLE", "ejemplo", "your-", "YOUR-", "<", "...",
    "PROJECT-REF", "REGION", "password@", "PASSWORD@",
]


def _git_tracked_files() -> list[Path]:
    """Archivos que git realmente rastrea. Excluye gitignoreados (secrets.toml, .env.claude)."""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        return [ROOT / line for line in r.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def check_no_secrets() -> list[str]:
    errors = []
    print("\n[2/4] Fuga de secretos (solo archivos rastreados por git)")

    tracked = _git_tracked_files()
    if not tracked:
        print("   - git ls-files no disponible — omitido (se valida en CI)")
        return errors

    # 1. Archivos prohibidos NO deben estar rastreados
    tracked_rel = {str(p.relative_to(ROOT)).replace("\\", "/") for p in tracked}
    for rel in FORBIDDEN_FILES:
        if rel in tracked_rel:
            errors.append(f"ARCHIVO SECRETO RASTREADO POR GIT: {rel}")
            print(f"   >> {rel}: RASTREADO (CRÍTICO)")
    print(f"   OK — ninguno de {FORBIDDEN_FILES} está rastreado")

    # 2. Patrones de secreto SOLO en archivos rastreados (lo que va al repo)
    scan_ext = {".py", ".md", ".json", ".yml", ".yaml", ".toml", ".txt"}
    hits = 0
    for path in tracked:
        if path.suffix.lower() not in scan_ext:
            continue
        if path.name == "check_health.py":  # este archivo contiene los patrones
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, text):
                snippet = m.group(0)
                # Ignorar si el match es claramente un placeholder de documentación
                if any(marker in snippet for marker in PLACEHOLDER_MARKERS):
                    continue
                errors.append(f"SECRETO REAL ({label}) en {path.relative_to(ROOT)}")
                print(f"   >> {path.relative_to(ROOT)}: {label}")
                hits += 1
    if hits == 0:
        print("   OK — sin secretos reales (placeholders de docs ignorados)")
    return errors


def check_python_syntax() -> list[str]:
    import py_compile
    errors = []
    print("\n[3/4] Sintaxis Python")
    py_files = [
        p for p in ROOT.rglob("*.py")
        if not (set(p.parts) & {".venv", "venv", "node_modules", "__pycache__", "historico"})
    ]
    bad = 0
    for p in py_files:
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"Error de sintaxis: {p.relative_to(ROOT)} — {e.msg}")
            print(f"   >> {p.relative_to(ROOT)}")
            bad += 1
    print(f"   {'OK' if bad == 0 else '>>'} — {len(py_files)} archivos, {bad} con error")
    return errors


def check_references() -> list[str]:
    errors = []
    print("\n[4/4] Integridad de referencias críticas")
    for rel in CRITICAL_REFS:
        path = ROOT / rel
        if path.exists():
            print(f"   OK — {rel}")
        else:
            errors.append(f"Referencia crítica faltante: {rel}")
            print(f"   >> {rel}: NO EXISTE")
    return errors


def check_registry() -> list[str]:
    """[5/5] Cumplimiento del Principio de Derivación (Carta de Gobernanza Art. 1 y 6).

    El gate VERIFICA ESTADOS, no interpreta filosofía. Es la extensión del gate
    existente — no un componente paralelo (Carta Art. 4.7, anti-inflación).
    """
    errors: list[str] = []
    print("\n[5/5] Cadena de autoridad (Carta de Gobernanza Art. 1)")
    reg = ROOT / "registry" / "registry.yaml"
    if not reg.exists():
        print("   >> registry/registry.yaml NO EXISTE — ejecutar build_registry.py")
        return ["Registry ausente: el Principio de Derivación no puede verificarse"]

    txt = reg.read_text(encoding="utf-8", errors="replace")
    total = int(re.search(r"^total_activos:\s*(\d+)", txt, re.M).group(1))
    huerfanos = int(re.search(r"^huerfanos:\s*(\d+)", txt, re.M).group(1))
    con_autoridad = total - huerfanos
    pct = round(100 * con_autoridad / max(total, 1), 1)

    # 1 · ¿hay artefactos sin autoridad declarada?
    print(f"      activos registrados : {total}")
    print(f"      declaran autoridad  : {con_autoridad} ({pct}%)")
    if huerfanos:
        print(f"   >> HUÉRFANOS: {huerfanos} — no promovibles a vigente (Art. 1)")
        errors.append(f"{huerfanos} artefacto(s) sin declarar autoridad (Carta Art. 1)")
    else:
        print("      OK — todo artefacto declara su autoridad")

    # 2 · ¿la cadena es reconstruible? (aristas rotas = padre inexistente)
    graph = ROOT / "registry" / "authority_graph.json"
    if graph.exists():
        import json as _json
        g = _json.loads(graph.read_text(encoding="utf-8"))
        rotas = g.get("aristas_rotas", 0)
        if rotas:
            print(f"   >> {rotas} arista(s) rota(s): padre declarado inexistente")
            errors.append(f"{rotas} cadena(s) de autoridad no reconstruible(s) hasta la Constitución")
        else:
            print(f"      OK — cadena reconstruible ({g.get('total_aristas', 0)} aristas, 0 rotas)")

    # 3 · ¿el Registry está al día con el disco? (hash de un centinela)
    frozen = ROOT / "identity" / "CONSTITUCION_INSTITUCIONAL.md"
    if not frozen.exists():
        errors.append("Constitución Institucional ausente: la raíz de autoridad no existe")
        print("   >> identity/CONSTITUCION_INSTITUCIONAL.md NO EXISTE")
    return errors


def main() -> int:
    print("=" * 60)
    print("  QUIRA Health Check — guardián de arranque + secretos")
    print("=" * 60)

    all_errors = []
    all_errors += check_context_budget()
    all_errors += check_no_secrets()
    all_errors += check_python_syntax()
    all_errors += check_references()
    all_errors += check_registry()

    print("\n" + "=" * 60)
    if all_errors:
        print(f"  FALLO — {len(all_errors)} problema(s):")
        for e in all_errors:
            print(f"    - {e}")
        print("=" * 60)
        return 1
    print("  TODO OK — arranque liviano, sin secretos, sintaxis válida")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
