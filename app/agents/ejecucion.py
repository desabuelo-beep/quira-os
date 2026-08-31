"""
app/agents/ejecucion.py — el testimonio de que una prueba corrió, y cómo terminó
================================================================================
POR QUÉ EXISTE (2026-08-30 · escalones 5 y 6). La escalera prueba↔verificador
tenía dos peldaños abiertos, y el director los había declarado bloqueados con un
argumento equivocado:

> *«Cerrar el escalón 5 choca con la frontera de efectos, porque verificar que
> una prueba se ejecutó implica correrla.»*

**No implica correrla.** Ese razonamiento asume que para saber que algo ocurrió
hay que hacerlo ocurrir — exactamente la tentación que la Regla de Oro 4 prohíbe
frente al Gold Master. QUIRA no recalcula el ICPI para saber cuánto vale: lo
LEE de quien lo calculó. Aquí igual: **no se corre la prueba, se lee el registro
de quien la corrió.** El verificador de este escalón no es QUIRA — es pytest.

    declarado → existente → corresponde → CORRESPONDE AL ARTEFACTO → ejecutado → exitoso
                └────────── ya estaba ──────────────────┘            └── aquí ──┘

LO QUE ESTE ESCALÓN TIENE Y NINGÚN OTRO: **caduca.**

Que un hash corresponda a un artefacto es cierto para siempre. Que una prueba
haya pasado es cierto **sobre una versión del código y ninguna otra**. Por eso el
testimonio se ata al SHA del archivo que contiene la prueba: si el archivo cambió
después de la corrida, el registro ya no habla de la prueba que hay hoy, y la
respuesta vuelve a `None` — incomprobable, no falso. Es el primer mecanismo del
sistema que **se invalida solo al pasar el tiempo**, y esa es su virtud: un
testimonio que nunca caduca es un testimonio que dejó de mirar el objeto.

⚠️ LO QUE NO HACE, Y HAY QUE DECIRLO ANTES DE QUE ALGUIEN LO SUPONGA. Esto **no
es infalsificable**. Quien pueda escribir en el registro puede escribir «passed».
Lo que impide es la falsificación *barata y silenciosa*: el testimonio sólo vale
mientras el SHA del archivo coincida, así que alterar la prueba para volverla
trivial **caduca su propio testimonio** y obliga a regenerarlo dejando rastro. Es
la misma clase de garantía que QUIRA le exige a un GAD: no que sea imposible
mentir, sino que mentir deje constancia. Vender esto como imposibilidad sería el
tipo de afirmación que este observatorio existe para no hacer.

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# El artefacto de testimonio. Lo PRODUCE `scripts/ci/registrar_ejecucion.py`
# leyendo el JUnit XML de pytest; este módulo sólo lo lee. La separación es la
# de siempre: el motor produce, el agente lee (Regla de Oro 1).
REGISTRO = RAIZ / "docs" / "registry" / "registro_de_ejecucion.json"

PASO = "passed"
FALLO = "failed"
OMITIDA = "skipped"


@lru_cache(maxsize=None)
def _sha_archivo(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


@lru_cache(maxsize=1)
def leer_registro(ruta: Path | None = None) -> dict:
    """El testimonio tal como está. Un registro ausente no es un registro que
    diga «no corrió»: es la ausencia de testimonio, y se devuelve vacío.

    Cacheado porque la cadena de procedencia pregunta por cada afirmación que
    sostiene, y releer el JSON —y rehacer los SHA— en cada capa costaría más que
    la comprobación que justifica. Quien cambie el registro o los archivos
    durante una corrida debe llamar a `olvidar()`."""
    r = ruta or REGISTRO
    if not r.exists():
        return {}
    try:
        return json.loads(r.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Un registro ilegible tampoco afirma nada. No se infiere fallo de él.
        return {}


def olvidar() -> None:
    """Descarta lo memorizado. Necesario cuando el registro o un archivo de
    pruebas cambian dentro de la misma corrida — típicamente, un ataque."""
    leer_registro.cache_clear()
    _sha_archivo.cache_clear()


def _entradas(nombre: str, registro: dict) -> list[dict]:
    """Las entradas del registro que hablan de esta prueba.

    La procedencia declara el nombre de la función —`test_x`—; el registro guarda
    el nodeid completo —`tests/test_y.py::test_x`—. Se busca por sufijo, y se
    admiten varias: una misma función parametrizada corre varias veces."""
    salida = []
    for nodeid, dato in (registro.get("pruebas") or {}).items():
        cola = nodeid.split("::")[-1]
        if cola == nombre or cola.startswith(f"{nombre}["):
            salida.append({**dato, "nodeid": nodeid})
    return salida


def _vigente(dato: dict) -> bool:
    """¿El testimonio sigue hablando de la prueba que hay HOY?

    Si el archivo que contiene la prueba cambió desde la corrida, el registro
    describe otra versión del código. No se descarta por sospecha: se descarta
    porque **literalmente no habla del objeto que se está preguntando**."""
    archivo = RAIZ / dato.get("archivo", "")
    if not dato.get("archivo") or not archivo.exists():
        return False
    return _sha_archivo(archivo) == dato.get("archivo_sha256")


def se_ejecuto(nombre: str, registro: dict | None = None) -> bool | None:
    """¿Existe testimonio vigente de que esta prueba corrió? (escalón 5)

    `None` cuando no hay testimonio o cuando caducó. **No `False`**: nadie
    registró la corrida no es lo mismo que consta que no corrió, y colapsarlos
    repetiría afuera el error que el dominio persigue — *«no lo encontré» ≠ «no
    existe»* (Principio Rector · CAPA 0)."""
    reg = leer_registro() if registro is None else registro
    vivas = [d for d in _entradas(nombre, reg) if _vigente(d)]
    return True if vivas else None


def fue_exitosa(nombre: str, registro: dict | None = None) -> bool | None:
    """¿El testimonio vigente dice que pasó? (escalón 6)

    Tres respuestas, no dos:

        True   corrió y pasó — la interpretación está respaldada
        False  corrió y falló — hay constancia de que NO lo está
        None   no hay testimonio vigente — no se sabe, y no se supone

    Una prueba omitida (`skipped`) devuelve `None`, no `True`: saltarse una
    prueba deja el verificador exactamente igual de no respaldado que no
    haberla escrito, y contarla como éxito sería la vía más barata de acreditar
    cualquier cosa."""
    reg = leer_registro() if registro is None else registro
    vivas = [d for d in _entradas(nombre, reg) if _vigente(d)]
    if not vivas:
        return None
    resultados = {d.get("resultado") for d in vivas}
    if FALLO in resultados:
        # Basta una parametrización fallida: el verificador no está respaldado
        # para todos los casos que la prueba declara cubrir.
        return False
    if PASO in resultados:
        return True
    return None


def estado(nombre: str, registro: dict | None = None) -> str:
    """El escalón alcanzado, en una palabra. Para inventarios y para la UI
    interna — nunca para el producto (Regla de Oro 2)."""
    reg = leer_registro() if registro is None else registro
    exito = fue_exitosa(nombre, reg)
    if exito is True:
        return "exitosa"
    if exito is False:
        return "fallida"
    if _entradas(nombre, reg):
        return "testimonio_caducado"
    return "sin_testimonio"


def cobertura(registro: dict | None = None) -> dict:
    """Cuánto del sistema tiene testimonio vigente. El residuo, medido."""
    reg = leer_registro() if registro is None else registro
    pruebas = reg.get("pruebas") or {}
    vigentes = sum(1 for d in pruebas.values() if _vigente(d))
    return {
        "registradas": len(pruebas),
        "vigentes": vigentes,
        "caducadas": len(pruebas) - vigentes,
        "commit": reg.get("commit", ""),
        "arbol_limpio": reg.get("arbol_limpio"),
        # EL UNIVERSO, DECLARADO (2026-08-31 · Capa 0). Este inventario es el
        # más fácil de leer de más: dice cuántas pruebas tienen testimonio, no
        # cuántas existen. Si nadie registró una corrida, «0 vigentes» no
        # significa que nada funcione — significa que nadie miró.
        "universo": {
            "que": "pruebas con testimonio en el registro de ejecución",
            "donde": str(REGISTRO.relative_to(RAIZ)) if REGISTRO.is_relative_to(RAIZ) else str(REGISTRO),
            "como": "JUnit XML de pytest, anclado al SHA del archivo de cada prueba",
            "hallados": len(pruebas),
            "fuera_de_alcance": [
                "pruebas que existen y nunca se registraron: no aparecen aquí, "
                "y su ausencia NO es evidencia de que fallen",
                "el testimonio caduca al cambiar el archivo: 'caducadas' mide "
                "desactualización del registro, no defectos del código",
            ],
        },
    }
