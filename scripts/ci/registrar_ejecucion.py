#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scripts/ci/registrar_ejecucion.py — produce el testimonio de una corrida
================================================================================
La otra mitad de `app/agents/ejecucion.py`, y están separadas a propósito: **este
script PRODUCE, el agente LEE**. Es la misma división que gobierna todo QUIRA —el
Gold Master calcula, el motor de dominio lee (Regla de Oro 1/4)— aplicada esta
vez a un hecho sobre nosotros mismos.

QUÉ REGISTRA. Para cada prueba: el nodeid, cómo terminó, y el SHA del archivo que
la contiene **en el momento de correrla**. Ese SHA es el ancla temporal: sin él,
un testimonio viejo seguiría acreditando una prueba que ya se reescribió.

SIN RELOJ, y por la misma razón que `procedencia.de_generacion`: un derivado debe
poder reconstruirse byte a byte desde su evidencia. Meter la hora de la corrida
haría que el archivo cambiara en cada ejecución aunque nada más cambiara, y el
ruido en el historial acabaría escondiendo los cambios que sí importan. El
*cuándo* lo dice el commit; el *sobre qué* lo dice el SHA.

USO
    python scripts/ci/registrar_ejecucion.py            corre la suite y registra
    python scripts/ci/registrar_ejecucion.py ruta.xml   registra un JUnit ya hecho

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "docs" / "registry" / "registro_de_ejecucion.json"


def _sha(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def _ubicacion(caso: ET.Element) -> tuple[str, str]:
    """Dónde vive la prueba: `(archivo, clase)`, relativo a la raíz y con «/».

    ⚠️ LA CLASE NO ES DECORATIVA, y costó descubrirlo. La primera versión armaba
    el nodeid como `archivo::nombre` y **cinco testimonios desaparecieron**: dos
    pruebas con el mismo nombre en clases distintas del mismo archivo colapsaban
    en una sola clave y la segunda pisaba a la primera. Si una hubiera fallado y
    la otra pasado, el registro habría acreditado con la que pasó — un testimonio
    borrando a otro, que es exactamente el falso positivo que este escalón
    existe para impedir. El nodeid se arma como lo arma pytest, entero.

    Se prefiere el atributo `file` que pytest emite; si faltara, se deriva del
    `classname` (`tests.test_x.TestY` → `tests/test_x.py` + `TestY`). No se
    inventa una ruta que no exista: un caso sin archivo localizable se descarta,
    porque su testimonio no podría anclarse a nada y acreditaría sin caducar."""
    partes = [p for p in (caso.get("classname") or "").split(".") if p]
    bruto = (caso.get("file") or "").replace("\\", "/")
    if bruto and (RAIZ / bruto).exists():
        # La clase es lo que sobra del classname tras el módulo del archivo.
        tallo = Path(bruto).stem
        resto = partes[partes.index(tallo) + 1:] if tallo in partes else []
        return bruto, ".".join(resto)
    while partes:
        cand = "/".join(partes) + ".py"
        if (RAIZ / cand).exists():
            return cand, ".".join(
                [p for p in (caso.get("classname") or "").split(".")][len(partes):])
        partes = partes[:-1]
    return "", ""


def _resultado(caso: ET.Element) -> str:
    if caso.find("failure") is not None or caso.find("error") is not None:
        return "failed"
    if caso.find("skipped") is not None:
        return "skipped"
    return "passed"


def leer_junit(xml: Path) -> dict[str, dict]:
    raiz = ET.parse(xml).getroot()
    shas: dict[str, str] = {}
    pruebas: dict[str, dict] = {}
    perdidos = 0
    for caso in raiz.iter("testcase"):
        archivo, clase = _ubicacion(caso)
        if not archivo:
            perdidos += 1
            continue
        if archivo not in shas:
            shas[archivo] = _sha(RAIZ / archivo)
        nodeid = "::".join(x for x in (archivo, clase, caso.get("name")) if x)
        pruebas[nodeid] = {"resultado": _resultado(caso), "archivo": archivo,
                           "archivo_sha256": shas[archivo]}
    if perdidos:
        # No se calla: un caso sin ancla es un testimonio que no existirá, y
        # quien lea el registro debe saber que no está completo.
        print(f"  ⚠️ {perdidos} casos sin archivo localizable: quedan sin testimonio")
    return dict(sorted(pruebas.items()))


def _arbol_limpio(salida: Path) -> bool:
    """Si queda algo sin commitear **aparte del propio registro**.

    El registro no puede contarse a sí mismo: escribirlo ensucia el árbol, así
    que incluirlo haría que el campo fuera `false` para siempre — un dato que
    nunca puede ser verdadero no informa de nada, sólo aparenta rigor."""
    propio = salida.relative_to(RAIZ).as_posix()
    lineas = [ln for ln in _git("status", "--porcelain").splitlines()
              if ln.strip() and propio not in ln.replace("\\", "/")]
    return not lineas


def registrar(xml: Path, salida: Path = SALIDA) -> dict:
    pruebas = leer_junit(xml)
    registro = {
        "_lease": "testimonio de una corrida de pytest. NO lo produce QUIRA "
                  "sobre sí misma: lo produce el ejecutor, y QUIRA lo lee. "
                  "Caduca cuando el archivo de la prueba cambia.",
        "commit": _git("rev-parse", "--short", "HEAD"),
        "arbol_limpio": _arbol_limpio(salida),
        "pruebas": pruebas,
    }
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(registro, ensure_ascii=False, indent=1) + "\n",
                      encoding="utf-8")
    return registro


def main(argv: list[str]) -> int:
    # La consola de Windows no siempre habla UTF-8 y el resumen lleva
    # simbolos: sin esto el script muere DESPUES de escribir el registro,
    # dando por fallida una corrida que si se guardo.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:                                    # noqa: BLE001
        pass

    if len(argv) > 1:
        xml = Path(argv[1])
        if not xml.exists():
            print(f"  no existe el JUnit indicado: {xml}")
            return 2
        codigo = 0
    else:
        tmp = Path(tempfile.mkdtemp()) / "junit.xml"
        codigo = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q", "-p", "no:randomly",
             f"--junitxml={tmp}"], cwd=RAIZ).returncode
        xml = tmp
        if not xml.exists():
            print("  pytest no produjo el reporte: no hay testimonio que registrar")
            return 2

    reg = registrar(xml)
    p = reg["pruebas"]
    cuenta = {r: sum(1 for d in p.values() if d["resultado"] == r)
              for r in ("passed", "failed", "skipped")}
    print(f"  registro escrito · {len(p)} pruebas · {cuenta} · "
          f"commit {reg['commit'] or '?'} · "
          f"arbol {'limpio' if reg['arbol_limpio'] else 'con cambios'}")
    if cuenta["failed"]:
        print("  ⚠️ hay pruebas fallidas: el testimonio lo registra, no lo oculta")
    return codigo


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
