# -*- coding: utf-8 -*-
"""
scripts/ci/check_portabilidad.py — ¿corre QUIRA fuera de un escritorio?
═══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-19 · OBS-032 Fase 3). El primer recuento dio «54 rutas
absolutas» y se fijó un trinquete plano sobre esa cifra. El colega corrigió el
método, y tenía razón:

> *«"54 rutas absolutas" no equivale necesariamente a "54 defectos". Lo que sí es
> un defecto es que una frontera arquitectónica legítima esté replicada y no
> parametrizada.»*

Un número sin taxonomía es exactamente el error que este proyecto persigue en el
sujeto observado: contar apariciones y llamarlas hechos. Aquí se clasifica.

    derivada        la ruta sale de `QUIRA_DATOS` / `config.DATOS_DIR`     ✅ correcta
    repositorio     relativa a la raíz del repo                            ✅ correcta
    frontera_fija   apunta a `ProyecT/` con la ruta escrita a mano         ⚠️ la frontera es
                                                                             legítima; su
                                                                             replicación no
    personal        cualquier otra ruta al disco de una persona            ⛔ defecto

La distinción importa para saber **qué falta**: `frontera_fija` se resuelve
migrando a `config.DATOS_DIR` (mecánico, de a uno); `personal` es un dato que no
debería existir en ninguna forma.

Uso:  python scripts/ci/check_portabilidad.py [--detalle]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_B = chr(92)
# Cualquier ruta absoluta a un perfil de usuario, en Windows, macOS o Linux.
_ABSOLUTA = re.compile(
    r"[A-Za-z]:" + re.escape(_B) + r"+(?:Users|Proyectos)"
    r"|/Users/[A-Za-z]|/home/[A-Za-z]")

# La carpeta de documentos que vive fuera del repositorio a propósito.
_FRONTERA = "ProyecT"

# ── EL UNIVERSO SE DERIVA · D-004 (2026-09-01) ───────────────────────────────
# Aquí había cuatro carpetas enumeradas a mano. `sentinel/` —73 archivos con
# rutas absolutas reales— no estaba en la lista, y el gate llevaba meses
# reportando «0 rutas fijas · objetivo cumplido». Su patrón SÍ las detectaba:
# **fallaba el universo, no el detector.**
#
# Y este mismo archivo ya llevaba escrita la lección que le faltó aplicarse:
# *«un tope que no se midió es una suposición con apariencia de control»*. Midió
# el tope y no midió el universo.
#
# Ahora se barre todo el repositorio menos exclusiones DECLARADAS con motivo —
# excluir está permitido; excluir en silencio no—. Medido con el universo
# derivado: 9 hallazgos donde el gate veía 0.
_EXCLUIDOS = (
    ("config.py", "ES la puerta: aquí la frontera se declara UNA vez y se "
                  "recibe del entorno. Que la ruta viva aquí es el diseño, no "
                  "el defecto (gate REGLAS · 0 rutas fijas fuera de config)"),
    ("tests/", "las pruebas citan rutas para PROHIBIRLAS —una asercion que "
               "veta el prefijo de un perfil— y en docstrings que explican "
               "un hallazgo. Mencionar una ruta para vetarla no es depender "
               "de ella"),
    (".claude", "copias de trabajo y configuración del entorno"),
    (".agents", "herramientas de asistencia, no código de QUIRA"),
    ("node_modules", "dependencias externas"),
    ("__pycache__", "artefactos de compilación"),
    ("historial_gold_master", "archivo histórico, no código vivo"),
)

# TRINQUETE: puede bajar, nunca subir. Se separa por clase porque cada una se
# resuelve de forma distinta y mezclarlas oculta el progreso real.
#
# ⚠️ EL PRIMER TOPE FUE UNA ESTIMACIÓN, NO UNA MEDICIÓN, y salió mal: se fijó
# `personal: 2` y había 3. El propio guard lo detectó al primer intento — que es
# exactamente para lo que sirve, pero deja la lección: **un tope que no se midió
# es una suposición con apariencia de control.** Estos números salen de correr
# el guard, no de calcularlos de cabeza.
#
# 2026-08-19 · tras declarar `DATOS_DIR` y `VAULT_DIR` en `config.py` y migrar
# el conector canónico del Gold Master y los tres accesos a la bóveda.
# TRINQUETE EN CERO (2026-08-25). La frontera hacia `ProyecT/` ya no está
# escrita a mano en ningún punto: se recibe de `config.DATOS_DIR`, que a su vez
# la toma de `QUIRA_DATOS`. Este guard deja de medir una deuda y pasa a defender
# una propiedad: **QUIRA corre en cualquier máquina que declare dónde están sus
# datos.**
#
# El recorrido, por si alguien lo necesita: 54 → 50 → 25 → 3 → 0, en cuatro
# patrones distintos que hubo que descubrir uno a uno —`Path(r"…")`, cadena
# cruda, concatenación implícita multilínea, y constante sin imports previos—.
# Ninguno se forzó: cada lote pasó por `ast.parse` antes de escribirse, y los
# que no compilaban NO se tocaron.
# ⚠️ EL TOPE SUBE DE 0 A 3, Y NO ES UNA REGRESIÓN (2026-09-01 · D-004).
#
# El sistema NO se ató más a una máquina: **el instrumento dejó de ser ciego.**
# Las tres rutas de `sentinel/` existían desde antes y este gate no las miraba
# porque `AMBITOS` no incluía ese territorio. Al derivar el universo aparecieron.
#
#     un número que sube porque el universo creció
#     ≠ un número que sube porque el defecto creció
#
# Confundirlas haría lo peor posible: incentivar a no mirar, porque mirar
# «empeora la métrica». El trinquete se refunda sobre el piso medido, y desde
# aquí sólo puede bajar.
#
# QUÉ SON LAS TRES · `sentinel/` es **paquete legado declarado** —su propio
# `__init__` lo dice y `ARQUITECTURA_CANONICA.md §6.2` fija su absorción—, y las
# tres apuntan a la bóveda de conocimiento que `config.VAULT_DIR` ya declara.
# Bajan a 0 cuando sentinel se absorba o cuando esas tres reciban la ruta de
# `config`, lo que ocurra antes.
#
# De las 9 que el universo derivado encontró, 4 quedaron fuera por exclusión
# declarada —`config.py` es la puerta, `tests/` cita rutas para vetarlas—, 1 se
# reparó en el acto (`data/obsidian_bridge.py` duplicaba `VAULT_DIR`), y 1 más
# era de `sentinel/` en un archivo que no repite la constante.
TOPE = {"frontera_fija": 0, "personal": 3}


def clasificar(linea: str) -> str | None:
    if not _ABSOLUTA.search(linea) or linea.strip().startswith("#"):
        return None
    return "frontera_fija" if _FRONTERA in linea else "personal"


def recorrer() -> list[tuple[str, int, str, str]]:
    """Barre TODO el repositorio menos las exclusiones declaradas.

    Cada exclusión lleva su motivo: una exclusión sin justificar es
    indistinguible de un olvido, y fue un olvido —`sentinel/`— el que dejó
    a este gate reportando cero durante meses."""
    fuera = []
    for f in RAIZ.rglob("*.py"):
        rel = f.relative_to(RAIZ).as_posix()
        if any(pat in rel for pat, _ in _EXCLUIDOS):
            continue
        try:
            lineas = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, ln in enumerate(lineas, 1):
            clase = clasificar(ln)
            if clase:
                fuera.append((rel, i, clase, ln.strip()[:70]))
    return fuera


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--detalle", action="store_true")
    args = ap.parse_args()

    hallazgos = recorrer()
    por_clase = Counter(h[2] for h in hallazgos)

    print("PORTABILIDAD · ¿corre QUIRA fuera del escritorio donde nació?")
    print("=" * 74)
    print("una frontera arquitectónica legítima replicada 52 veces sigue "
          "siendo\nuna sola decisión — pero escrita 52 veces\n")

    falla = False
    for clase, tope in TOPE.items():
        n = por_clase.get(clase, 0)
        marca = "ok" if n <= tope else "XX"
        if n > tope:
            falla = True
        etiqueta = {"frontera_fija": "hacia ProyecT/, escrita a mano",
                    "personal": "al disco de una persona"}[clase]
        print(f"   [{marca}] {clase:14} {n:3} / {tope:3}   {etiqueta}")

    if args.detalle:
        print()
        for archivo, linea, clase, txt in sorted(hallazgos, key=lambda x: x[2]):
            print(f"   {clase:14} {archivo}:{linea}")
            print(f"                  {txt}")

    print()
    if falla:
        print("   ⛔ el sistema se ató MÁS a una máquina concreta desde la última")
        print("      medición. El trinquete sólo admite bajar (OBS-032).")
        return 1

    pendiente = sum(por_clase.values())
    print(f"   {pendiente} puntos por migrar a `config.DATOS_DIR` · objetivo 0")
    print("   ya migrados: config.py · app/connectors/gold_master.py "
          "(la puerta canónica al motor)")
    return 0


if __name__ == "__main__":
    sys.exit(main())