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

# ★ IDENTIFICADOR ESTABLE ≠ NOMBRE DE ARCHIVO (DOC-015 · P5, 2026-09-14) ───────────
# Sin `id:` declarado, este script fabricaba el identificador desde el nombre:
# `ADR-035` quedaba registrado como `CANON_ADR-ADR-035_Biblioteca_Reglas_Normativ`.
# 86 de 158 activos lo sufrían, y todo hijo que declaraba `parent: ADR-023` apuntaba
# a un id que el registro no tenía — cuatro aristas rotas que nadie vio en siete
# semanas porque el derivado no se regeneraba.
#
# El identificador canónico de un ADR, una OBS o un PCD es el que el propio
# documento DECLARA en su título (`# ADR-023 — …`) y el que usan todas las citas.
# Se lee de ahí, y sólo si el prefijo del archivo dice lo mismo: dos
# representaciones que coinciden, no una inferida de la otra (P5-G.2).
RE_PREFIJO_CANON = re.compile(r"^((?:ADR|OBS|PCD|DEC)-[A-Z]?\d+)(?=_|$)")
RE_TITULO = re.compile(r"^#\s+(.+)$", re.M)

# Canon vivo en disco que el CATALOGO no mira A PROPÓSITO (ver HUECO DE ALCANCE).
# Un `parent` que vive aquí no es un «padre inexistente»: es un padre fuera de
# catálogo. Confundirlos sería decir que falta lo que sólo no se inspeccionó.
ALCANCE_SIN_CATALOGAR = ("docs/architecture",)

FENCE = "`" * 3


def _sin_bloques_de_codigo(txt: str) -> str:
    """Borra el contenido de los bloques de código de un Markdown.

    Un `id:` o un `parent:` escrito DENTRO de un ejemplo no es una declaración del
    documento: es contenido citado. Leerlo como declaración es el error que la
    falsación 15 de `PANORAMA §5-septies` cometió con un `estado: NO_VIGENTE`
    ilustrativo — **hallar un término prueba la presencia del término, no la
    declaración que parece nombrar** (corolario de `DOC-035`)."""
    fuera, dentro = [], False
    for linea in txt.splitlines():
        if linea.lstrip().startswith(FENCE):
            dentro = not dentro
            fuera.append("")
            continue
        fuera.append("" if dentro else linea)
    return "\n".join(fuera)


def identificador(p: Path, declarado: str | None, kind: str) -> str:
    """El id con que el activo entra al registro, en orden de autoridad:

        1 · `id:` declarado en su cabecera
        2 · el identificador que su TÍTULO declara, si el archivo dice lo mismo
        3 · uno fabricado desde el nombre — y entonces nadie puede citarlo por id
    """
    if declarado:
        return declarado
    m = RE_PREFIJO_CANON.match(p.stem)
    if m and p.suffix == ".md":
        try:
            txt = _sin_bloques_de_codigo(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            txt = ""
        t = RE_TITULO.search(txt)
        if t and re.match(rf"{re.escape(m.group(1))}\b", t.group(1).strip()):
            return m.group(1)
    # Un paquete se llama por su carpeta: los seis `app/agents/d*/__init__.py`
    # compartían el id `DOMAIN_PIPELINE-__init__` — seis activos fundidos en uno,
    # y un id que nombra a seis no resuelve a ninguno.
    nombre = p.parent.name if p.name == "__init__.py" else p.stem
    return f"{kind.upper()}-{nombre[:32]}"

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

# ★ HUECO DE ALCANCE DECLARADO (2026-07-29) ────────────────────────────────────
# `docs/architecture/*.md` NO está en el CATALOGO de arriba. Son 49 documentos, y
# solo 2 declaran autoridad. Entre los 47 restantes hay canon vivo:
# PROTOCOLO_CURACION_DOMINIO (donde viven R-A..R-D) y METODOLOGIA_GOLD_MASTER
# (citada por CLAUDE.md como método canónico).
#
# Es decir: el "derivación 100% · 0 huérfanos" que este script venía reportando
# era cierto SOBRE LO QUE MIRA, y falso como afirmación general.
#
# NO se estampan los 47 bloques de golpe: atribuir un `parent` sin verificarlo
# sería INVENTAR AUTORIDAD, que es justo lo que la Carta Art. 1 prohíbe. Se aplica
# R-D (bifurcación algoritmo/instrumento) a nosotros mismos: la limitación es de
# ALCANCE, así que se MIDE y se DECLARA en vez de parchar a ciegas.
# Se usa el mecanismo que ya existe (EXTERNOS), no uno nuevo (Subsidiariedad).

# Activos externos al repo (se DECLARAN, no se mueven — Art. 3)
EXTERNOS = [
    ("ProyecT/SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx", "gold_master", "MOTOR ÚNICO de cálculo (Carta Art. 4.1) — se LEE, jamás se recalcula"),
    ("ProyecT/Holding_Municipal_Montecristi",       "fuente_evidencia", "documentos oficiales del GAD (PDOT, RDC, participación, POA/PAC)"),
    ("quira-harvester",                              "repo_hermano", "código de cosecha de evidencia — repo separado"),
    ("governance",                                   "gobernanza_legacy", "17 docs de gobernanza fuera del repo — PENDIENTE de fusión (Fase 2)"),
    ("docs/architecture",                            "canon_sin_catalogar", "49 .md · solo 2 declaran autoridad — HUECO DE ALCANCE del registry, contiene canon vivo (PROTOCOLO_CURACION_DOMINIO · METODOLOGIA_GOLD_MASTER). PENDIENTE de derivación verificada, no de estampado ciego"),
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
    if p.suffix == ".md":
        txt = _sin_bloques_de_codigo(txt)
    tiene = bool(RE_AUTHORITY.search(txt))
    mid = RE_ID.search(txt)
    mpar = RE_PARENT.search(txt)
    return (mid.group(1) if mid else None,
            mpar.group(2) if mpar else None,
            tiene)


def escanear() -> tuple[list[dict], list[dict]]:
    """Lo que el disco dice HOY. Lo usa `main` para escribir el registro y
    `check_health` para comprobar que el registro escrito sigue siendo cierto:
    una sola lectura de la realidad, no dos que puedan divergir."""
    activos, huerfanos = [], []
    for patron, kind, level, esperada in CATALOGO:
        for p in sorted(REPO.glob(patron)):
            if not p.is_file():
                continue
            rel = p.relative_to(REPO).as_posix()
            did, dparent, tiene = analizar(p)
            reg = {
                "id": identificador(p, did, kind), "kind": kind, "level": level,
                "path": rel,
                "hash": sha256(p),
                "authority_declared": tiene,
                "parent": dparent or esperada,
            }
            activos.append(reg)
            if not tiene:
                huerfanos.append(reg)
    return activos, huerfanos


def main() -> int:
    activos, huerfanos = escanear()

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

    # ★ El registro CERTIFICA lo que mira. Decir "derivación 100%" sin este matiz
    #   sería una afirmación no verificada — el error que el propio sistema combate.
    sin_cat = sum(1 for f in (REPO / "docs" / "architecture").glob("*.md")
                  if not re.search(r"^\s*(#|//)?\s*authority:",
                                   f.read_text(encoding="utf-8", errors="replace")[:400], re.M))
    if sin_cat:
        print(f"\n   ⚠️  ALCANCE: 0 huérfanos es cierto SOBRE LO CATALOGADO, no en general.")
        print(f"       docs/architecture/ tiene {sin_cat} .md sin autoridad declarada y NO entra")
        print(f"       al catálogo. Contiene canon vivo. Se declara como externo pendiente:")
        print(f"       derivación verificada, nunca estampado ciego (Carta Art. 1).")
    print("\n   Desglose por tipo:")
    from collections import Counter
    for k, n in sorted(Counter(a["kind"] for a in activos).items()):
        hu = sum(1 for a in activos if a["kind"] == k and not a["authority_declared"])
        print(f"     {k:18} {n:4}   (huérfanos: {hu})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
