# -*- coding: utf-8 -*-
"""
scripts/governance/build_registry.py — Constructor del Registry Constitucional
═══════════════════════════════════════════════════════════════════════════════
Implementa el Art. 1 de la Carta de Gobernanza (Principio de Derivación) y su Art. 3
(el Registry describe, no gobierna: es el Registro Civil de la institución).

ESCANEA la realidad del disco y CERTIFICA qué existe. NO inventa: si un artefacto no
está en disco, no entra al Registry. Detecta artefactos HUÉRFANOS (sin bloque
`authority:`), que por Art. 1 no pueden promoverse a `vigente`.

Uso:  python scripts/governance/build_registry.py
Salida: registry/registry.yaml
Dylus Lab © 2026
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [9]
#   type: OPERATIVA
# ---
from __future__ import annotations

import hashlib
import os
import re
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
EXTERNO = REPO.parent                     # C:\...\Dylus Lab
# El bloque de autoridad aparece como clave YAML (`authority:`), como front-matter en .md,
# o COMENTADO en .py/.cypher (`# authority:` / `// authority:`). El detector debe reconocer
# las tres formas: si no, el Registry miente y marca huérfano lo que sí declaró.
RE_AUTHORITY = re.compile(r"^\s*(#|//)?\s*authority:", re.M)
RE_ID = re.compile(r"^id:\s*(\S+)", re.M)
RE_PARENT = re.compile(r"^\s*(#|//)?\s*parent:\s*(\S+)", re.M)

# Qué se cataloga como ACTIVO INSTITUCIONAL (no cada .py: eso sería ruido)
CATALOGO = [
    # (glob, kind, level, autoridad_esperada)
    ("identity/*.md",                  "identity",   0, None),
    ("governance/*.md",                "normative",  1, "CONSTITUCION-001"),
    ("governance/decisions/*.md",      "decision",   1, "GOVERNANCE-001"),
    ("governance/policies/*.md",       "policy",     1, "GOVERNANCE-001"),
    ("docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md", "identity", 0, None),
    ("marco_teorico/*.md",             "marco_teorico", 1, "CONSTITUCION-001"),
    ("docs/brn/CNO-*.yaml",            "canon_cno",  2, "GOVERNANCE-001"),
    ("docs/brn/RO-*.yaml",             "canon_ro",   2, "GOVERNANCE-001"),
    ("docs/adr/ADR-*.md",              "canon_adr",  2, "GOVERNANCE-001"),
    ("docs/pcd/PCD-*.md",              "canon_pcd",  2, "GOVERNANCE-001"),
    ("docs/observations/OBS-*.md",      "observation", 2, "GOVERNANCE-001"),
    ("data/d*/catalogo_*.yaml",        "domain_catalog", 3, None),
    ("app/agents/d*/__init__.py",      "domain_pipeline", 3, None),
    ("app/connectors/gold_master.py",  "connector",  3, None),
    ("scripts/ci/check_health.py",     "gate",       3, "GOVERNANCE-001"),
    ("scripts/cypher/*.cypher",        "graph",      3, None),
]

# Activos externos al repo (se DECLARAN, no se mueven — Art. 3)
EXTERNOS = [
    ("ProyecT/SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx", "gold_master", "MOTOR ÚNICO de cálculo (Carta Art. 4.1) — se LEE, jamás se recalcula"),
    ("ProyecT/Holding_Municipal_Montecristi",       "fuente_evidencia", "documentos oficiales del GAD (PDOT, RDC, participación, POA/PAC)"),
    ("quira-harvester",                              "repo_hermano", "código de cosecha de evidencia — repo separado"),
    ("governance",                                   "gobernanza_legacy", "17 docs de gobernanza fuera del repo — PENDIENTE de fusión (Fase 2)"),
    ("documentos_proyecto",                          "insumo", "Manual Técnico v5.0, doctrinal, PDOT, Plan CNE"),
    ("metodologia_beta_Dctos",                       "insumo", "SIAP-ICPI maestras, TERRA, tesis"),
    ("_historico",                                   "archivo", "23 items legacy"),
    ("quiraintelligence-web",                        "producto", "portal público (index.html, vercel)"),
]


def sha256(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    except Exception:
        return ""


def analizar(p: Path) -> tuple[str | None, str | None, bool]:
    """Devuelve (id declarado, parent declarado, tiene_bloque_authority)."""
    try:
        txt = p.read_text(encoding="utf-8", errors="replace")[:4000]
    except Exception:
        return None, None, False
    tiene = bool(RE_AUTHORITY.search(txt))
    mid = RE_ID.search(txt)
    mpar = RE_PARENT.search(txt)
    return (mid.group(1) if mid else None,
            mpar.group(2) if mpar else None,
            tiene)


def main() -> int:
    activos, huerfanos = [], []
    for patron, kind, level, esperada in CATALOGO:
        for p in sorted(REPO.glob(patron)):
            if not p.is_file():
                continue
            rel = p.relative_to(REPO).as_posix()
            did, dparent, tiene = analizar(p)
            aid = did or f"{kind.upper()}-{p.stem[:32]}"
            reg = {
                "id": aid, "kind": kind, "level": level, "path": rel,
                "hash": sha256(p),
                "authority_declared": tiene,
                "parent": dparent or esperada,
            }
            activos.append(reg)
            if not tiene:
                huerfanos.append(reg)

    # externos
    ext = []
    for ruta, kind, nota in EXTERNOS:
        p = EXTERNO / ruta
        ext.append({"path": f"../{ruta}", "kind": kind, "existe": p.exists(), "nota": nota})

    # escribir YAML a mano (sin dependencia extra, formato estable)
    out = [
        "# ═══════════════════════════════════════════════════════════════════",
        "# REGISTRY CONSTITUCIONAL DE QUIRA — el Registro Civil de la institución",
        "# GENERADO por scripts/governance/build_registry.py · NO editar a mano.",
        "# Autoridad: Carta de Gobernanza Art. 1 (Derivación) y Art. 3 (describe, no gobierna).",
        "# ═══════════════════════════════════════════════════════════════════",
        f"generado: {date.today().isoformat()}",
        f"total_activos: {len(activos)}",
        f"huerfanos: {len(huerfanos)}   # sin bloque authority: → no pueden promoverse a vigente (Art. 1)",
        "",
        "componentes:",
    ]
    for a in activos:
        out += [
            f"  - id: {a['id']}",
            f"    kind: {a['kind']}",
            f"    level: {a['level']}",
            f"    path: {a['path']}",
            f"    hash: {a['hash']}",
            f"    authority_declared: {str(a['authority_declared']).lower()}",
            f"    parent: {a['parent'] or 'null'}",
        ]
    out += ["", "# Activos EXTERNOS al repo — se declaran, no se mueven (Carta Art. 3)", "externos:"]
    for e in ext:
        out += [
            f"  - path: {e['path']}",
            f"    kind: {e['kind']}",
            f"    existe: {str(e['existe']).lower()}",
            f"    nota: \"{e['nota']}\"",
        ]

    dest = REPO / "registry" / "registry.yaml"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(f"OK — Registry generado: {dest.relative_to(REPO)}")
    print(f"   activos catalogados : {len(activos)}")
    print(f"   con autoridad       : {len(activos) - len(huerfanos)}")
    print(f"   HUÉRFANOS           : {len(huerfanos)}  (Art. 1: no promovibles a vigente)")
    print(f"   externos declarados : {len(ext)}  ({sum(1 for e in ext if e['existe'])} existen en disco)")
    print("\n   Desglose por tipo:")
    from collections import Counter
    for k, n in sorted(Counter(a["kind"] for a in activos).items()):
        hu = sum(1 for a in activos if a["kind"] == k and not a["authority_declared"])
        print(f"     {k:18} {n:4}   (huérfanos: {hu})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
