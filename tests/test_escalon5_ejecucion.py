# -*- coding: utf-8 -*-
"""
tests/test_escalon5_ejecucion.py — la prueba citada tiene que haber corrido
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30). Los dos últimos peldaños de la escalera estaban
abiertos, y el director los había declarado bloqueados con un argumento que era
falso:

> *«Verificar que una prueba se ejecutó implica correrla, y eso choca con la
> frontera de efectos.»*

No implica correrla. Implica **leer el registro de quien la corrió** — la Regla
de Oro 4 aplicada a un hecho sobre nosotros mismos. Javo lo dijo antes de que el
director lo viera: *«hay que ir cerrando todo, no dejar cosas pendientes».*

    declarado → existente → corresponde → CORRESPONDE AL ARTEFACTO → EJECUTADO → EXITOSO
                └───────────── ya estaba ───────────────┘            └── aquí ───┘

LO QUE ESTE ESCALÓN TIENE Y NINGÚN OTRO: **caduca.** Que un hash corresponda a un
artefacto es cierto para siempre; que una prueba pasara es cierto sobre una
versión del código y ninguna otra. Media docena de estas pruebas existen sólo
para fijar esa caducidad, porque un testimonio que no caduca es un testimonio que
dejó de mirar el objeto.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import ejecucion as E                     # noqa: E402
from app.agents import procedencia as P                   # noqa: E402
from app.agents import sujeto as S                        # noqa: E402

_YO = "tests/test_escalon5_ejecucion.py"


def _registro(resultado: str = "passed", *, archivo: str = _YO,
              sha: str | None = None, prueba: str = "test_fantasma") -> dict:
    """Un testimonio sintético. El SHA real por defecto: así el testimonio está
    vigente y las pruebas de caducidad pueden romperlo a propósito."""
    real = E._sha_archivo(RAIZ / archivo) if (RAIZ / archivo).exists() else "0" * 16
    return {"pruebas": {f"{archivo}::{prueba}": {
        "resultado": resultado, "archivo": archivo,
        "archivo_sha256": sha if sha is not None else real}}}


def _procedencia(prueba: str) -> P.Procedencia:
    return P.Procedencia(
        fuente="Gold Master", captura="2026-08-30",
        estado_adquisicion="leido_del_motor", evidencia="abc",
        verificador="app.agents.ejecucion.fue_exitosa",
        prueba_del_verificador=prueba,
        sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}")


# ── ESCALÓN 5 · ¿corrió? ──────────────────────────────────────────────────────
def test_un_testimonio_vigente_acredita_que_corrio_y_que_paso():
    reg = _registro("passed")
    assert E.se_ejecuto("test_fantasma", reg) is True
    assert E.fue_exitosa("test_fantasma", reg) is True
    assert E.estado("test_fantasma", reg) == "exitosa"


def test_sin_testimonio_no_se_afirma_ni_se_niega():
    """EL RESIDUO, medido y no escondido — igual que en el escalón 4.

    `None`, no `False`: que nadie registrara la corrida **no prueba que la prueba
    no corriera**. Colapsarlos repetiría adentro el error que este dominio
    persigue afuera — *«no lo encontré» ≠ «no existe»*."""
    assert E.se_ejecuto("test_que_nadie_registro", {}) is None
    assert E.fue_exitosa("test_que_nadie_registro", {}) is None
    assert E.estado("test_que_nadie_registro", {}) == "sin_testimonio"


# ── ESCALÓN 6 · ¿pasó? ────────────────────────────────────────────────────────
def test_un_testimonio_de_fallo_DEGRADA_la_afirmacion():
    """La única forma de que este escalón diga `False`, y es fuerte: hay
    constancia de que la prueba citada como respaldo **no respalda nada**."""
    reg = _registro("failed", prueba="test_un_testimonio_vigente_acredita_que_corrio_y_que_paso")
    assert E.fue_exitosa(
        "test_un_testimonio_vigente_acredita_que_corrio_y_que_paso", reg) is False


def test_una_prueba_omitida_no_cuenta_como_exito():
    """`skipped` → `None`. Saltarse una prueba deja el verificador exactamente
    igual de no respaldado que no haberla escrito; contarla como éxito sería la
    vía más barata de acreditar cualquier cosa, y hay 1 omitida en esta suite."""
    reg = _registro("skipped")
    assert E.se_ejecuto("test_fantasma", reg) is True
    assert E.fue_exitosa("test_fantasma", reg) is None


# ── LA CADUCIDAD ──────────────────────────────────────────────────────────────
def test_ataque_un_testimonio_de_otra_version_del_codigo_CADUCA():
    """El ataque central. Alguien escribe «passed» en el registro, pero el
    archivo cambió desde entonces: el testimonio **ya no habla de la prueba que
    hay hoy**. No se descarta por sospecha — se descarta porque literalmente no
    describe el objeto por el que se pregunta."""
    reg = _registro("passed", sha="ffffffffffffffff")
    assert E.se_ejecuto("test_fantasma", reg) is None
    assert E.fue_exitosa("test_fantasma", reg) is None
    assert E.estado("test_fantasma", reg) == "testimonio_caducado"


def test_ataque_caducado_devuelve_None_y_no_False():
    """Y caduca hacia `None`, **nunca hacia `False`**: un testimonio viejo no es
    evidencia de que la prueba falle. Si caducar acusara, cada edición de un
    archivo de pruebas degradaría todas las afirmaciones que dependen de él —
    convertiría el mantenimiento normal del código en una imputación."""
    reg = _registro("passed", sha="ffffffffffffffff")
    assert E.fue_exitosa("test_fantasma", reg) is not False


def test_ataque_un_archivo_que_ya_no_existe_no_acredita():
    reg = _registro("passed", archivo="tests/borrado_hace_meses.py")
    assert E.se_ejecuto("test_fantasma", reg) is None


# ── ATAQUES A LA IDENTIFICACIÓN DE LA PRUEBA ──────────────────────────────────
def test_ataque_un_nombre_parecido_no_hereda_el_testimonio():
    """`test_x` no puede acreditarse con el testimonio de `test_x_bis`. Se compara
    la cola del nodeid completa, no por prefijo."""
    reg = _registro("passed", prueba="test_fantasma_bis")
    assert E.se_ejecuto("test_fantasma", reg) is None


def test_una_prueba_parametrizada_si_hereda_su_testimonio():
    """Pero `test_x[caso]` **sí** es `test_x`: la misma función corriendo varias
    veces. Si no se admitiera, toda prueba parametrizada quedaría sin testimonio
    y el escalón se volvería inútil justo donde más casos cubre."""
    reg = _registro("passed", prueba="test_fantasma[130801]")
    assert E.se_ejecuto("test_fantasma", reg) is True


def test_ataque_basta_una_parametrizacion_fallida_para_no_acreditar():
    reg = {"pruebas": {}}
    real = E._sha_archivo(RAIZ / _YO)
    for caso, res in (("[130801]", "passed"), ("[130802]", "failed")):
        reg["pruebas"][f"{_YO}::test_fantasma{caso}"] = {
            "resultado": res, "archivo": _YO, "archivo_sha256": real}
    assert E.fue_exitosa("test_fantasma", reg) is False, (
        "el verificador no está respaldado para todos los casos que la prueba "
        "declara cubrir")


def test_ataque_un_testimonio_no_puede_borrar_a_otro():
    """REGRESIÓN de un defecto real, cazado al generar el primer registro.

    La primera versión armaba el nodeid como `archivo::nombre` y **cinco
    testimonios desaparecieron**: dos pruebas homónimas en clases distintas del
    mismo archivo colapsaban en una clave y la segunda pisaba a la primera. Si
    una hubiera fallado y la otra pasado, el registro habría acreditado con la
    que pasó.

    Con la clase en el nodeid ya no se pisan, y ante dos homónimas se responde
    por la peor: la procedencia cita un nombre de función, no un nodeid, así que
    QUIRA **no puede saber a cuál de las dos se refería**. Elegir la que pasó
    sería resolver la ambigüedad a favor propio."""
    real = E._sha_archivo(RAIZ / _YO)
    reg = {"pruebas": {
        f"{_YO}::TestUno::test_homonima": {
            "resultado": "passed", "archivo": _YO, "archivo_sha256": real},
        f"{_YO}::TestDos::test_homonima": {
            "resultado": "failed", "archivo": _YO, "archivo_sha256": real}}}
    assert len(E._entradas("test_homonima", reg)) == 2, "un testimonio se perdió"
    assert E.fue_exitosa("test_homonima", reg) is False


# ── LO QUE UN REGISTRO ROTO NO PUEDE HACER ────────────────────────────────────
def test_ataque_un_registro_ilegible_no_afirma_ni_acusa():
    """Un JSON corrupto devuelve testimonio vacío — no un veredicto. Si un
    archivo malformado degradara, bastaría con romperlo para tumbar la
    acreditación de todo el sistema."""
    roto = RAIZ / "docs" / "registry" / "_registro_roto_de_prueba.json"
    roto.write_text("{ esto no es json", encoding="utf-8")
    try:
        E.olvidar()
        assert E.leer_registro(roto) == {}
    finally:
        roto.unlink(missing_ok=True)
        E.olvidar()


def test_ataque_un_registro_ausente_no_degrada_la_cadena():
    """El trinquete al revés: mientras el residuo exista, la falta de testimonio
    **no puede** bajar el peso de una afirmación. El día que se exija, será una
    decisión declarada — no un efecto colateral."""
    p = _procedencia("test_una_prueba_omitida_no_cuenta_como_exito")
    assert P.prueba_respaldo_vigente(
        P.Procedencia(**{**p.__dict__, "prueba_del_verificador": "test_inexistente_xyz"})
    ) is None


# ── LA CADENA COMPLETA ────────────────────────────────────────────────────────
def test_la_cadena_degrada_cuando_consta_que_la_prueba_falla(monkeypatch):
    """La integración: `procedencia` deja de acreditar la capa 6 cuando hay
    constancia de fallo. Citar como respaldo algo que consta que falla es peor
    que no citar nada — aparenta acreditación donde hay constancia de lo
    contrario."""
    p = _procedencia("test_una_prueba_omitida_no_cuenta_como_exito")
    assert P.sostener("x", p).peso == P.HECHO_VERIFICABLE

    monkeypatch.setattr(E, "fue_exitosa", lambda nombre, registro=None: False)
    s = P.sostener("x", p)
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert "prueba_del_verificador" in s.faltan


def test_verificar_la_ejecucion_no_ejecuta_nada():
    """LA PROPIEDAD QUE DESMIENTE LA OBJECIÓN ORIGINAL, y por eso está aquí.

    El módulo que responde «¿esta prueba corrió?» no importa `subprocess` ni
    `socket`: no cruza la frontera de efectos porque **no reproduce el hecho para
    conocerlo, lee el artefacto de quien lo produjo**. Es la misma razón por la
    que ningún motor de dominio recalcula el Gold Master."""
    fuente = (RAIZ / "app" / "agents" / "ejecucion.py").read_text(encoding="utf-8")
    for efecto in ("import subprocess", "import socket", "os.system", "Popen"):
        assert efecto not in fuente, (
            f"«{efecto}» en el lector del testimonio: estaría produciendo el "
            f"hecho que sólo debe leer")


def test_ningun_dominio_migrado_se_apoya_en_una_prueba_que_consta_que_falla():
    """TRINQUETE: puede subir, nunca bajar — el gemelo del escalón 4.

    Deliberadamente exige `is not False`, no `is True`. Que el testimonio esté
    al día es higiene y se mide en `cobertura()`; que un dominio se acredite con
    una prueba **de la que consta que falla** es otra cosa, y es la que no puede
    pasar. Exigir `True` aquí haría fallar la suite cada vez que alguien editara
    un archivo de pruebas antes de regenerar el registro: convertiría el
    mantenimiento normal en una alarma, y las alarmas que suenan siempre dejan
    de mirarse."""
    from app.agents.d01 import motor as D1
    from app.agents.d02 import motor as D2
    from app.agents.d03 import motor as D3

    if not D1._GM_DEFAULT.exists():
        import pytest
        pytest.skip("Gold Master no accesible")

    E.olvidar()
    for nombre, sostenida in (("d01", D1.sostener_ipe()),
                              ("d02", D2.sostener_isp()),
                              ("d03", D3.sostener_incorporacion())):
        pr = sostenida.procedencia
        assert P.prueba_respaldo_vigente(pr) is not False, (
            f"{nombre} cita como respaldo «{pr.prueba_del_verificador}», y hay "
            f"constancia de que esa prueba corrió y no pasó")


def test_el_registro_real_habla_de_esta_suite():
    """El testimonio que hay en el repositorio tiene que ser de ESTE código, no
    de uno cualquiera. Si nadie lo ha generado todavía, se dice — no se supone."""
    E.olvidar()
    c = E.cobertura()
    if not c["registradas"]:
        import pytest
        pytest.skip("aún no se ha registrado ninguna corrida")
    assert c["vigentes"] > 0, (
        "hay testimonio pero ninguna entrada vigente: el registro quedó atrás "
        "del código — correr `scripts/ci/registrar_ejecucion.py`")
