# -*- coding: utf-8 -*-
"""
scripts/test_brn_arquitectura.py — BRN v2 · Suite de Regresión Arquitectónica
═══════════════════════════════════════════════════════════════════════════════════
El salto de madurez que recomendó el colega (2026-07-18): en vez de re-discutir los fundamentos
por cada CNO nueva, un conjunto de pruebas que verifican que los INVARIANTES del modelo BRN se
mantienen. Si pasan, cada dominio nuevo (d04, d05…) valida la arquitectura automáticamente.

INVARIANTES VERIFICADOS (independientes del corpus · deterministas):
  1. Toda RO deriva de una CNO existente.
  2. Toda CNO tiene un SHA por eslabón (formato válido).
  3. Ninguna RO conoce el motor (sin campo `motor`, sin "Gold Master"/"Hxx" en su texto).
  4. El compilador no tiene lógica por dominio (sin `if dominio==` ni `d02/d03` embebidos).
  5. La firma del artefacto es estable (manifest.firma == recomputar(config)).
  6. config.json NO contiene metadatos jurídicos (ro/cno/sha/cadena).
  7. manifest.json conserva la trazabilidad (cadena_sha por cada RO compilada).

Uso:  python scripts/test_brn_arquitectura.py       (exit 0 = todo verde)
Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

from brn_ro_adapter import adaptar, umbral_en

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
BRN_DIR = REPO / "docs" / "brn"
CONFIG = REPO / "data" / "brn_config.json"
MANIFEST = REPO / "data" / "brn_manifest.json"
COMPILADOR = REPO / "scripts" / "brn_compilador.py"

_res: list[tuple[bool, str]] = []


def _check(cond: bool, ok: str, fail: str) -> None:
    _res.append((bool(cond), ok if cond else fail))


def _load(patron: str) -> list[dict]:
    return [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted(BRN_DIR.glob(patron))]


def main() -> int:
    cnos = {c["id"]: c for c in _load("CNO-*.yaml")}
    ros = _load("RO-*.yaml")

    # 1 · Toda RO deriva de una CNO existente
    huerfanas = [r["id"] for r in ros if str(r.get("deriva_de", "")).split()[0] not in cnos]
    _check(not huerfanas, f"1 · {len(ros)} RO derivan de una CNO existente",
           f"1 · RO sin CNO: {huerfanas}")

    # 2 · Toda CNO tiene un SHA (12+ hex) por eslabón
    sha_malos = []
    for c in cnos.values():
        for e in c.get("cadena", []):
            if not re.fullmatch(r"[0-9a-fA-F]{8,}…?", str(e.get("sha256", "")).rstrip("…") + ""):
                sha_malos.append(f'{c["id"]}/{e.get("norma")}-{e.get("articulo")}')
    _check(not sha_malos, f"2 · todos los eslabones de {len(cnos)} CNO tienen SHA válido",
           f"2 · SHA con formato inválido: {sha_malos}")

    # 3 · Ninguna RO conoce el motor
    fugas = []
    for r in ros:
        txt = yaml.safe_dump(r, allow_unicode=True)
        if r.get("motor") or "Gold Master" in txt or re.search(r"\bH\d{1,2}[a-z]?_", txt):
            fugas.append(r["id"])
    _check(not fugas, "3 · ninguna RO conoce el motor (canon desacoplado)",
           f"3 · RO que mencionan el motor: {fugas}")

    # 4 · El compilador no tiene lógica por dominio
    comp = COMPILADOR.read_text(encoding="utf-8")
    # se ignoran comentarios; se busca código con d0N literal o 'dominio =='
    codigo = "\n".join(l for l in comp.splitlines() if not l.strip().startswith("#"))
    ramas = re.findall(r'==\s*["\']d0\d|dominio\s*==|opera_en\s*==\s*["\']d0\d', codigo)
    _check(not ramas, "4 · el compilador no tiene ramas por dominio (grep=0)",
           f"4 · el compilador ramifica por dominio: {ramas}")

    # 5 · Firma estable: manifest.firma == recomputar(config)
    firma_ok = False
    if CONFIG.exists() and MANIFEST.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        base = {"artifact_schema": cfg.get("artifact_schema"), "parametros": cfg.get("parametros")}
        recompute = hashlib.sha256(
            json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        firma_ok = recompute == man.get("firma_sha256")
    _check(firma_ok, "5 · la firma del artefacto es estable (idempotente)",
           "5 · la firma NO coincide — el artefacto está desincronizado (recompila)")

    # 6 · config.json sin metadatos jurídicos
    cfg_txt = CONFIG.read_text(encoding="utf-8").lower() if CONFIG.exists() else ""
    juridico = [k for k in ("cadena_sha", '"cno"', '"ro"', "sha256") if k in cfg_txt]
    _check(not juridico, "6 · config.json sin metadatos jurídicos (solo ejecución)",
           f"6 · config.json filtra metadatos BRN: {juridico}")

    # 7 · manifest.json conserva la trazabilidad
    traza_ok = False
    if MANIFEST.exists():
        man = json.loads(MANIFEST.read_text(encoding="utf-8"))
        gen = man.get("generado_de", [])
        traza_ok = bool(gen) and all(g.get("cadena_sha") for g in gen)
    _check(traza_ok, "7 · manifest.json conserva la cadena de SHA (trazabilidad)",
           "7 · manifest.json sin trazabilidad completa")

    # ══ PRUEBAS SEMÁNTICAS (colega · 2026-07-18: distintas de las arquitectónicas) ══
    # No verifican la forma, sino el COMPORTAMIENTO: que la regla haga lo correcto.
    models = {m.id: m for m in (adaptar(r) for r in ros)}

    # 8 · Resolución de vigencia: el tramo correcto para cada fecha (§4b)
    ro_iv = models.get("RO-IV-001")
    sem_ok = ro_iv and umbral_en(ro_iv, "2026-07-01") == 65 and umbral_en(ro_iv, "2027-03-01") == 70
    _check(sem_ok, "8 · vigencia: RO-IV-001 resuelve 65 en 2026 y 70 en 2027 (tramo correcto)",
           "8 · vigencia MAL resuelta — el runtime tomaría el umbral equivocado")

    # 9 · Toda RO vigente tiene una métrica y al menos un umbral no nulo (medición real)
    sin_medicion = [m.id for m in models.values() if m.estado == "vigente"
                    and (not m.metrica or all(t.umbral is None for t in m.tramos))]
    _check(not sin_medicion, "9 · toda RO vigente tiene métrica y umbral (lógica de medición real)",
           f"9 · RO vigente sin medición: {sin_medicion}")

    # 10 · Esquema del config: schema versionado + cada fila con las claves de ejecución
    CLAVES = {"variable", "umbral", "desde", "hasta", "frecuencia", "opera_en"}
    fuera, schema = [], None
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        schema = cfg.get("artifact_schema")
        for i, fila in enumerate(cfg.get("parametros", [])):
            if set(fila) != CLAVES:
                fuera.append(f"fila{i}:{set(fila) ^ CLAVES}")
    _check(bool(schema) and not fuera,
           f"10 · config.json cumple el esquema de ejecución (artifact_schema {schema})",
           f"10 · config.json rompe el esquema: schema={schema} · {fuera}")

    # 11 · CONTRATO (colega · 2026-07-20): solo el ROAdapter puede leer el YAML de una RO.
    # Evita que dentro de seis meses alguien vuelva a hacer ro["metrica"]["nombre"] desde otro módulo.
    CLAVES_RO = ("metrica", "parametros", "vigencia_operativa", "deriva_de", "consume")
    infractores = []
    for py in sorted((REPO / "scripts").glob("brn_*.py")):
        if py.name == "brn_ro_adapter.py":
            continue
        cuerpo = "\n".join(l for l in py.read_text(encoding="utf-8").splitlines()
                           if not l.strip().startswith("#"))
        for k in CLAVES_RO:
            # solo cuenta si se lee sobre la RO cruda (variable `ro`), no sobre dicts propios
            if re.search(rf'\bro\b\s*(\.get\(["\']{k}["\']|\[["\']{k}["\']\])', cuerpo):
                infractores.append(f"{py.name}:{k}")
    _check(not infractores,
           "11 · contrato respetado: solo el ROAdapter lee el YAML de la RO",
           f"11 · lectura directa del YAML fuera del adaptador: {infractores}")

    # ── Reporte ───────────────────────────────────────────────────────────────
    print("BRN · Suite de Regresión Arquitectónica + Semántica")
    for ok, msg in _res:
        print(f"   {'✅' if ok else '❌'} {msg}")
    fallos = sum(1 for ok, _ in _res if not ok)
    print(f"\n{'TODO VERDE — la arquitectura BRN se mantiene' if not fallos else f'{fallos} INVARIANTE(S) ROTO(S)'}")
    return 0 if not fallos else 1


if __name__ == "__main__":
    raise SystemExit(main())
