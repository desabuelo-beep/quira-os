# -*- coding: utf-8 -*-
"""
tests/test_puente_compilado.py — D-003 · por qué nadie cruza el puente
════════════════════════════════════════════════════════════════════════════════
D-003 decía: *«las 13 RO están compiladas en `snapshot['brn_cno']` — el puente
existe, firmado y al día, y ningún motor lo cruza»*. Iba a construir el lector
para que lo cruzaran. **La medición previa lo impidió**, y el colega la había
exigido antes de escribir código:

> *«No modificar. No recalcular. No reparar todavía. Primero medir.»*

Y antes fijó la frontera que este módulo NO debe romper:

> *«el puente no debe hacer que el Gold Master consulte la BRN para decidir sus
> valores. La BRN explica y traza la dependencia; no gobierna el motor.»*

LO QUE LA MEDICIÓN ENCONTRÓ — tres cosas, y ninguna era la esperada:

 1 · **El catálogo se declara `propuesta` por un LITERAL.** `brn_cno.py:165`
     escribe `"estado_catalogo": "propuesta · pendiente de validación humana"`
     fijo, mientras la línea 147 sí deriva el estado de cada CNO. Aunque Javo
     selle todo el canon, el compilado seguirá diciendo pendiente: **un campo
     que nunca puede ser verdadero no informa** — el mismo defecto que tuvo
     `arbol_limpio` al contarse a sí mismo.

 2 · **El compilado está desactualizado.** Su fecha es 2026-08-19 y las 9 piezas
     de d07 —`CNO-VII-001..004` y `RO-VII-001..005`— se promovieron a `vigente`
     el 26-ago. El compilado las tiene como `propuesta`. Nueve de nueve,
     coincidencia exacta con un evento conocido.

 3 · Por tanto **cruzar el puente hoy sería consumir un catálogo obsoleto que
     además se auto-declara no validado.** No cruzarlo no era negligencia.

EL ORDEN CORRECTO, que la medición reveló: recompilar → resolver el literal del
estado → *sólo entonces* el lector. Construir el lector primero habría acoplado
nueve motores a un artefacto caducado.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_SNAP = RAIZ / "data" / "gm_snapshot.json"


def _brn():
    if not _SNAP.exists():
        return None
    d = json.loads(_SNAP.read_text(encoding="utf-8"))
    return d.get("brn_cno")


def test_el_puente_lleva_la_cadena_normativa_completa():
    """LO QUE EL PUENTE SÍ TIENE, y es más de lo que D-003 suponía: cada CNO
    viaja con su cadena de eslabones —`rol`, `norma`, `articulo`, `sumilla`— y
    con `cadena_integra`. La trazabilidad norma→regla está compilada."""
    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    c0 = brn["cno"][0]
    assert c0.get("cadena"), "la cadena normativa dejó de viajar compilada"
    esl = c0["cadena"][0]
    assert {"rol", "norma", "articulo"} <= set(esl), f"eslabón incompleto: {esl}"
    assert brn["cadenas_integras"] == brn["total_cno"]


def test_el_estado_del_catalogo_se_deriva_y_no_se_escribe():
    """HALLAZGO 1 · CERRADO, y la prueba se invirtió — la señal acordada.

    Decía que `estado_catalogo` era un literal que ninguna validación podía
    mover. Ahora el catálogo **deriva** lo que de verdad hay dentro y declara
    aparte lo que sólo un humano puede afirmar:

        estado_piezas_cno / estado_piezas_ro   derivados del canon
        integridad_compilacion                 16/16
        canon_sha256                           huella de la entrada
        validacion_humana_del_catalogo         «no_consta» — no se inventa

    Javo pidió que heredara el estado de sus piezas; el colega advirtió que
    validar las piezas no valida el acto de compilarlas. **Las dos cosas eran
    ciertas**: lo derivable se deriva y lo que exige un acto humano se declara
    pendiente, sin colapsar una afirmación en la otra (ADR-035 §5)."""
    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    assert "estado_catalogo" not in brn, (
        "volvió el campo único que colapsaba piezas y acto de compilación")
    assert brn["estado_piezas_cno"] and brn["estado_piezas_ro"]
    sello = brn["validacion_humana_del_catalogo"]
    assert isinstance(sello, dict), (
        "el sello volvió a ser una cadena suelta: debe registrar QUIÉN y CUÁNDO")
    fuente = (RAIZ / "scripts" / "brn_cno.py").read_text(encoding="utf-8")
    assert '"estado_catalogo": "propuesta' not in fuente, (
        "el literal volvió al compilador")

def test_el_compilado_refleja_el_canon_en_disco():
    """HALLAZGO 2 · CERRADO. El compilado del 19-ago tenía como `propuesta` las
    nueve piezas de d07 que Javo promovió el 26-ago. Recompilado, cero piezas
    difieren."""
    import glob

    import yaml

    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    comp = {c["id"]: c["estado"] for c in brn["cno"]}
    comp.update({r["id"]: r["estado"] for c in brn["cno"] for r in c["deriva_ro"]})
    difieren = []
    for f in glob.glob(str(RAIZ / "docs" / "brn" / "*.yaml")):
        d = yaml.safe_load(Path(f).read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("id") in comp and comp[d["id"]] != d.get("estado"):
            difieren.append(d["id"])
    assert not difieren, f"el compilado volvió a desfasarse del canon: {difieren}"


def test_un_compilado_desfasado_ya_no_puede_pasar_inadvertido():
    """LA MEJORA QUE HACE EL HALLAZGO IMPOSIBLE DE OCULTAR, propuesta por el
    colega: el catálogo guarda la **huella del canon de entrada**.

    Antes, un compilado viejo sólo se detectaba comparando pieza por pieza y
    sabiendo qué se había promovido. Ahora basta rehacer el hash de
    `docs/brn/`: si no coincide con `canon_sha256`, el compilado describe otro
    canon. Es el escalón 7 aplicado al compilador — **el derivado señala el
    origen del que salió**, igual que el nombre del `.bin` señala su URL.

    ⚠️ Que el hash difiera NO significa que el compilado esté mal: significa que
    describe una entrada distinta de la actual. La distinción de siempre.

    ⚠️ Y LA CUENTA SE PIDE, NO SE REPITE (2026-09-02). Esta prueba rehacía el
    hash con su propio `read_bytes()`, así que había TRES implementaciones de la
    misma huella: compilador, lector y prueba. Cuando se normalizaron los
    finales de línea —el SHA dependía del sistema de archivos y el sello de Javo
    no viajaba fuera de su máquina— dos se corrigieron y ésta se quedó atrás,
    acusando de desfase a un catálogo que estaba al día.

    Una prueba que reimplementa lo que verifica comprueba su propia copia."""
    from app.agents import brn_lector as L

    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    assert brn.get("canon_sha256"), "el catálogo dejó de declarar su entrada"
    actual = L.canon_sha_actual()
    assert brn["canon_sha256"] == actual, (
        f"el compilado describe un canon distinto del que hay en disco: "
        f"declara {brn['canon_sha256']}, el canon actual es {actual} "
        f"— recompilar con `python scripts/brn_cno.py`")

def test_ningun_motor_cruza_el_puente_todavia():
    """HALLAZGO 3. Y no cruzarlo **no era negligencia**: hacerlo hoy sería
    consumir un catálogo caducado que además se declara no validado.

    Los únicos que tocan `brn_cno` son su productor y los inventarios de
    auditoría — que lo leen para medirlo, no para calcular con él."""
    # ⚠️ SE LEE CON `pathlib`, NO CON `grep` POR SUBPROCESO. El primer intento
    # llamó a `subprocess.run(["grep"...])` y la frontera de efectos lo detuvo
    # —el mecanismo de la deuda 4-ter funcionando contra quien lo escribió—. La
    # salida correcta no era declarar `efecto_real`: era no necesitarlo.
    motores = [f for d in ("d01", "d02", "d03", "d07", "d08", "d09")
               for f in (RAIZ / "app" / "agents" / d).rglob("*.py")
               if "__pycache__" not in f.parts]
    consumidores = [f.relative_to(RAIZ).as_posix() for f in motores
                    if "brn_cno" in f.read_text(encoding="utf-8", errors="replace")]
    assert not consumidores, (
        f"un motor empezó a consumir el compilado: {consumidores} — comprobar "
        f"antes que el catálogo esté recompilado y validado")


def test_la_frontera_de_la_BRN_sigue_declarada():
    """LA REGLA QUE EL PUENTE NO PUEDE ROMPER, y que el colega fijó antes de
    dejar construir nada: la BRN **explica y traza**; no gobierna al motor. El
    flujo canónico sigue siendo `Excel → Python`, y el Gold Master permanece
    autónomo (Reglas de Oro 1 y 4)."""
    doctrina = _brn()
    if doctrina is None:
        pytest.skip("no está el snapshot")
    assert "REGLA" in doctrina["_doctrina"] and "ADR-035" in doctrina["_doctrina"]
    assert "MDN" in doctrina["_modelo"], (
        "el modelo de dependencias normativas dejó de declararse")


# ── EL SELLO HUMANO DEL CATÁLOGO · ADR-035 §5 (2026-09-01) ───────────────────
def test_el_catalogo_lleva_sello_humano_con_nombre_y_fecha():
    """Javo: *«selle el catálogo director, con mi nombre y fecha»*.

    El colega puso la condición que lo hace válido: el sello acredita el **acto
    de compilación** y su correspondencia con el canon — no convierte las piezas
    en vigentes ni a la BRN en autoridad sobre el Gold Master."""
    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    s = brn["validacion_humana_del_catalogo"]
    assert s["estado"] == "validado"
    assert s["validado_por"] == "Javo"
    # 2026-09-02: RENOVACIÓN del sello del 01-sep sobre un canon IDÉNTICO. No
    # cambió el canon —el último commit en `docs/brn/` es anterior al sello—:
    # cambió la forma de medirlo, porque la huella dependía del sistema de
    # archivos y no viajaba. El sello lo dice en `renovacion_de`, y esa
    # constancia es lo que impide leer esto como una validación nueva.
    assert s["fecha_validacion"] == "2026-09-02", (
        "la fecha debe ser la del sello real, no la de una compilación anterior")
    assert s.get("renovacion_de"), (
        "una renovación de sello sin constancia de qué renueva es un sello "
        "nuevo disfrazado: debe decir cuál caducó y por qué")
    assert "NO convierte" in s.get("alcance", ""), (
        "el sello dejó de declarar su límite")


def test_el_compilador_no_puede_firmar_su_propio_sello():
    """LA PROPIEDAD QUE HACE QUE EL SELLO VALGA ALGO.

    Si el compilador escribiera el sello, **cada recompilación lo renovaría
    sola** — y un sello que se firma solo no acredita nada: sería el literal que
    vino a sustituir, con otro disfraz. Vive en `docs/registry/` como acto de
    gobernanza, y el compilador sólo lo LEE."""
    fuente = (RAIZ / "scripts" / "brn_cno.py").read_text(encoding="utf-8")
    assert "_leer_sello" in fuente
    assert "sello_catalogo_brn.json" in fuente
    # No debe haber ninguna escritura hacia el artefacto de sello.
    for linea in fuente.splitlines():
        if "sello" in linea.lower() and ("write_text" in linea or "json.dump" in linea):
            raise AssertionError(f"el compilador escribe el sello: {linea.strip()}")


def test_el_sello_caduca_si_cambia_el_canon_que_valido():
    """EL SELLO ESTÁ ATADO AL CANON QUE VALIDÓ — mecanismo del escalón 5.

    Si el canon de entrada cambia, el sello describe **otra compilación** y el
    catálogo vuelve a `no_consta`, conservando quién y cuándo firmó el anterior.
    Un testimonio que no caduca es un testimonio que dejó de mirar el objeto.

    Se comprueba sin tocar disco: se invoca el lector con un canon distinto."""
    import importlib.util as iu

    ruta = RAIZ / "scripts" / "brn_cno.py"
    spec = iu.spec_from_file_location("_brn_mod", ruta)
    mod = iu.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:                                    # noqa: BLE001
        pytest.skip("el compilador no es importable en aislamiento")

    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    vigente = mod._leer_sello(brn["canon_sha256"])
    assert vigente["estado"] == "validado"

    caducado = mod._leer_sello("0000000000000000")
    assert caducado["estado"] == "no_consta", (
        "el sello sigue valiendo para un canon que no validó")
    assert caducado.get("sello_caducado_de") == "Javo", (
        "al caducar debe conservarse quién firmó el sello anterior")


# ══════════════════════════════════════════════════════════════════════════════
# UNA SOLA FUNCIÓN DEFINE LA IDENTIDAD CRIPTOGRÁFICA DEL CANON
# ══════════════════════════════════════════════════════════════════════════════
def test_la_identidad_del_canon_tiene_una_sola_implementacion():
    """DOCTRINA QUE EL COLEGA FIJÓ TRAS EL CASO CRLF (2026-09-02):

    > *«Una sola función debe definir la identidad criptográfica del canon. Si
    > compilador y lector la calculan por separado, el sistema puede declarar
    > "el sello no corresponde" cuando la divergencia está en el código que
    > calcula la identidad.»*

    Y no era hipotético. Había TRES implementaciones —compilador, lector y una
    prueba—. Al normalizar los finales de línea se corrigieron dos, y la tercera
    acusó de desfase a un catálogo que estaba al día. El sistema dijo la verdad
    sobre lo que medía; lo que medía estaba mal en un sitio de tres.

    EL UNIVERSO SE DERIVA: se barren los `.py` del repositorio buscando el
    patrón —un `sha256` alimentado con los YAML de `docs/brn/`— en vez de
    comprobar una lista de archivos conocidos, que es justo el defecto que
    D-004 cerró."""
    import re

    _FUERA = {".venv", "venv", "node_modules", "__pycache__", "historico",
              "worktrees", "_deprecated"}
    # El patrón: un hash alimentado con el contenido de los YAML del canon.
    PATRON = re.compile(
        r"hashlib\.sha256\(\)[\s\S]{0,400}?glob\(\s*[\"']\*\.yaml"
        r"|glob\(\s*[\"']\*\.yaml[\s\S]{0,300}?\.update\(",
        re.M)

    implementan = []
    for f in RAIZ.rglob("*.py"):
        if set(f.parts) & _FUERA:
            continue
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if PATRON.search(txt):
            implementan.append(f.relative_to(RAIZ).as_posix())

    assert implementan == ["app/agents/brn_lector.py"], (
        f"la identidad del canon se calcula en más de un sitio: {implementan}. "
        f"El día que dos divergan, el sistema acusará al sello de no "
        f"corresponder cuando lo que no corresponde es el código que mide")


def test_el_compilador_pide_la_identidad_en_vez_de_calcularla():
    """La otra mitad: que el compilador NO tenga la suya. Sin esto, la prueba
    de arriba pasaría el día que el compilador dejara de calcular el hash… y
    también el día que dejara de escribirlo."""
    fuente = (RAIZ / "scripts" / "brn_cno.py").read_text(encoding="utf-8")
    assert "from app.agents.brn_lector import canon_sha_actual" in fuente
    assert "canon_sha = canon_sha_actual()" in fuente

    # Y las dos cuentas dan lo mismo sobre el canon de hoy.
    import json

    from app.agents import brn_lector as L
    brn = json.loads((RAIZ / "data" / "gm_snapshot.json").read_text(
        encoding="utf-8"))["brn_cno"]
    assert brn["canon_sha256"] == L.canon_sha_actual()


def test_la_huella_del_canon_no_depende_del_sistema_de_archivos(tmp_path, monkeypatch):
    """EL ATAQUE QUE FIJA EL CASO CRLF, y es el que impide que vuelva.

    Los 30 YAML llevan CRLF en Windows y LF en el runner. Con `read_bytes()`
    crudo el mismo canon daba 59be1b69b8e033c9 aquí y f9fa18c6f3b8bb9b allá:
    una identidad semánticamente idéntica y criptográficamente distinta según
    la máquina. Incompatible con una infraestructura verificable portable —
    Regla de Oro 3: sin norma verificada no hay dato, y QUIRA va a 222 GAD.

    ⚠️ SE USA LA FUNCIÓN REAL SOBRE DOS COPIAS, y no un hash propio. La primera
    versión de esta prueba calculaba la huella por su cuenta para comparar — y
    el ataque de arriba la cazó en el acto: **era la cuarta implementación**,
    escrita mientras se redactaba la regla que las prohíbe. Un hash propio aquí
    habría probado que hashear crudo depende de CRLF (obvio) en vez de que
    `canon_sha_actual` no depende (la propiedad que importa)."""
    from app.agents import brn_lector as L

    origen = sorted((RAIZ / "docs" / "brn").glob("*.yaml"))
    assert origen, "no hay canon que medir"

    def _copiar(destino, con_crlf: bool):
        destino.mkdir(parents=True, exist_ok=True)
        for f in origen:
            b = f.read_bytes().replace(b"\r\n", b"\n")
            if con_crlf:
                b = b.replace(b"\n", b"\r\n")
            (destino / f.name).write_bytes(b)
        return destino

    lf = _copiar(tmp_path / "lf", con_crlf=False)
    crlf = _copiar(tmp_path / "crlf", con_crlf=True)

    monkeypatch.setattr(L, "_BRN_DIR", lf)
    huella_lf = L.canon_sha_actual()
    monkeypatch.setattr(L, "_BRN_DIR", crlf)
    huella_crlf = L.canon_sha_actual()

    assert huella_lf == huella_crlf, (
        f"la huella del canon volvió a depender de los finales de línea "
        f"(LF {huella_lf} ≠ CRLF {huella_crlf}): el sello dejaría de valer al "
        f"cruzar de sistema operativo, y con él la verificación de los 222 GAD")
