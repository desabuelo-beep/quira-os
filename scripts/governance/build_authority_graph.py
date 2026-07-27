# -*- coding: utf-8 -*-
"""
scripts/governance/build_authority_graph.py — Authority Graph + Estado Institucional
═══════════════════════════════════════════════════════════════════════════════════
Genera DESDE el Registry (nunca a mano · Carta de Gobernanza Art. 3):
  · registry/authority_graph.json   — representación ejecutable del árbol de autoridad
  · registry/INSTITUTIONAL_STATE.md — el estado vivo de la institución

"Un activo con múltiples representaciones": Markdown legible → JSON → Neo4j.
El JSON es cargable al grafo para que QUIRA IA responda "¿qué depende del Art. 9?".

Uso:  python scripts/governance/build_authority_graph.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
REG = REPO / "registry" / "registry.yaml"


def parse_registry() -> tuple[list[dict], list[dict], dict]:
    """Parser mínimo del registry generado (formato estable, sin dependencias)."""
    txt = REG.read_text(encoding="utf-8")
    meta = {}
    for k in ("generado", "total_activos", "huerfanos"):
        m = re.search(rf"^{k}:\s*(\S+)", txt, re.M)
        if m:
            meta[k] = m.group(1)
    comps, exts, cur, en = [], [], None, None
    for line in txt.splitlines():
        if line.startswith("componentes:"):
            en = "c"; continue
        if line.startswith("externos:"):
            en = "e"; continue
        if line.strip().startswith("- "):
            cur = {}
            (comps if en == "c" else exts).append(cur)
            line = line.replace("- ", "", 1)
        if cur is not None and ":" in line:
            k, _, v = line.strip().partition(":")
            cur[k.strip()] = v.strip().strip('"')
    return comps, exts, meta


def main() -> int:
    comps, exts, meta = parse_registry()

    # ── nodos y aristas ──
    nodes, edges = [], []
    ids = {c["id"] for c in comps}
    for c in comps:
        nodes.append({
            "id": c["id"], "kind": c["kind"], "level": int(c.get("level", 3)),
            "path": c["path"], "declared": c.get("authority_declared") == "true",
        })
        par = c.get("parent")
        if par and par != "null":
            edges.append({"from": c["id"], "to": par, "type": "DERIVA_DE",
                          "resuelto": par in ids})

    rotas = [e for e in edges if not e["resuelto"]]
    huerfanos = [n for n in nodes if not n["declared"]]
    cumplimiento = round(100 * (len(nodes) - len(huerfanos)) / max(len(nodes), 1), 1)

    graph = {
        "_fuente": "GENERADO por scripts/governance/build_authority_graph.py — no editar",
        "_autoridad": "Carta de Gobernanza Art. 1 (Derivación) y Art. 3 (representaciones)",
        "generado": date.today().isoformat(),
        "raiz": "CONSTITUCION-001",
        "total_nodos": len(nodes), "total_aristas": len(edges),
        "aristas_rotas": len(rotas), "huerfanos": len(huerfanos),
        "cumplimiento_derivacion_pct": cumplimiento,
        "nodes": nodes, "edges": edges,
    }
    (REPO / "registry" / "authority_graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")

    # ── Estado Institucional (GENERADO — el panel de control del Estado de QUIRA) ──
    por_kind = Counter(n["kind"] for n in nodes)
    hu_kind = Counter(n["kind"] for n in huerfanos)
    dominios = sorted({re.search(r"d\d\d", n["path"]).group(0)
                       for n in nodes if n["kind"] == "domain_catalog"
                       and re.search(r"d\d\d", n["path"])})

    L = [
        "<!-- GENERADO por scripts/governance/build_authority_graph.py · NO EDITAR A MANO.",
        "     Editarlo a mano rompe la trazabilidad (Carta de Gobernanza Art. 3). -->",
        "",
        "# ESTADO INSTITUCIONAL DE QUIRA",
        "",
        f"**Generado:** {date.today().isoformat()} · **Fuente:** `registry/registry.yaml`",
        "",
        "> No es documentación: es **gobernanza viva**. Describe el estado de la institución,",
        "> no de los archivos. Se regenera; nunca se redacta.",
        "",
        "## Cadena de autoridad",
        "",
        "| Capa | Artefacto | Estado |",
        "|---|---|---|",
        "| L0 · Identidad | Constitución Institucional | " + ("✅ vigente" if any(n["id"] == "CONSTITUCION-001" for n in nodes) else "❌ ausente") + " |",
        "| L0 · Identidad | Constitución Ontológica | " + ("✅ presente" if any("ONTOLOGICA" in n["path"].upper() for n in nodes) else "❌ ausente") + " |",
        "| L1 · Gobernanza | Carta de Gobernanza | " + ("✅ vigente" if any(n["id"] == "GOVERNANCE-001" for n in nodes) else "❌ ausente") + " |",
        f"| L1 · Gobernanza | Decisiones institucionales | {por_kind.get('decision', 0)} registradas |",
        f"| L2 · Canon | CNO · RO · ADR · PCD | {por_kind.get('canon_cno',0)} · {por_kind.get('canon_ro',0)} · {por_kind.get('canon_adr',0)} · {por_kind.get('canon_pcd',0)} |",
        f"| L2 · Canon | Observaciones | {por_kind.get('observation', 0)} |",
        f"| L3 · Implementación | Dominios con catálogo | {', '.join(dominios) or '—'} |",
        f"| Registry | Integridad | {'✅ íntegro' if not rotas else f'⚠️ {len(rotas)} aristas rotas'} |",
        "",
        "## Cumplimiento del Principio de Derivación (Carta Art. 1)",
        "",
        f"**{cumplimiento}%** — {len(nodes) - len(huerfanos)} de {len(nodes)} activos declaran su autoridad.",
        "",
        f"⚠️ **{len(huerfanos)} artefactos HUÉRFANOS** — sin bloque `authority:`, no pueden",
        "promoverse a `vigente` (Carta Art. 1). Desglose:",
        "",
        "| Tipo | Total | Huérfanos |",
        "|---|---|---|",
    ]
    for k in sorted(por_kind):
        L.append(f"| {k} | {por_kind[k]} | {hu_kind.get(k, 0)} |")

    L += [
        "",
        "## Activos externos declarados (Carta Art. 3 — se declaran, no se mueven)",
        "",
        "| Ruta | Tipo | En disco |",
        "|---|---|---|",
    ]
    for e in exts:
        L.append(f"| `{e.get('path','')}` | {e.get('kind','')} | {'✅' if e.get('existe')=='true' else '❌'} |")

    L += [
        "",
        "## Architecture Freeze v1.0",
        "",
        f"**ACTIVO.** Solo se permite: declarar autoridad · completar trazabilidad · documentar",
        "decisiones · verificar cumplimiento. Prohibido crear conceptos nuevos (Carta Art. 7).",
        "",
        f"**Condición de levantamiento:** cumplimiento de derivación = 100% (hoy **{cumplimiento}%**)",
        f"y Registry íntegro (hoy {'✅' if not rotas else '⚠️'}).",
        "",
        "---",
        "*Estado Institucional · GENERADO · Dylus Lab © 2026*",
    ]
    (REPO / "registry" / "INSTITUTIONAL_STATE.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"OK — authority_graph.json  ({len(nodes)} nodos · {len(edges)} aristas · {len(rotas)} rotas)")
    print(f"OK — INSTITUTIONAL_STATE.md")
    print(f"   Cumplimiento del Principio de Derivación: {cumplimiento}%")
    print(f"   Huérfanos: {len(huerfanos)} · Aristas rotas: {len(rotas)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
