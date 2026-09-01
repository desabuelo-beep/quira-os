# -*- coding: utf-8 -*-
"""
tests/test_meta_integridad.py — CAPA 0 · la capacidad de QUIRA de auditarse
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-31). El colega la puso antes que todas las demás capas:

> *«Antes de auditar QUIRA, auditamos la capacidad de QUIRA para auditarse a sí
> mismo. […] Esta capa es crítica: porque si falla, todo lo demás queda
> contaminado.»*

Y falla. En un solo día salieron tres diagnósticos falsos —«7 de 8 enrichers»,
«d08 tiene 3/3 SHA», «d02 no carga su RO»— y los tres eran el mismo error:

    afirmar sobre un universo que no se declaró.

De ahí salió la regla. Pero la regla **no se había aplicado a los inventarios
que la produjeron**: sólo `canon.py` declaraba universo, y aun él lo hacía por
fila y no sobre sí mismo. Un mecanismo de meta-integridad que se exceptúa a sí
mismo no es una regla, es una costumbre.

LO QUE ESTA CAPA FIJA:

    Ningún inventario puede afirmar sin declarar su universo,
    cómo lo descubrió, y qué queda fuera de su alcance.

Y se comprueba sobre la lista DERIVADA de inventarios — no sobre una escrita a
mano, que tendría exactamente el defecto que persigue.

Dylus Lab © 2026
"""
from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_CAMPOS = ("que", "donde", "como", "hallados", "fuera_de_alcance",
           "mecanismo", "exclusiones")


def inventarios() -> list[tuple[str, object]]:
    """Los inventarios del sistema, DERIVADOS por introspección.

    Un inventario es una función pública de `app/agents/*.py` cuyo nombre
    empieza por `cobertura` y que no exige argumentos. Escribir la lista a mano
    haría que este mismo módulo afirmara sobre un universo no declarado — el
    defecto que existe para impedir."""
    salida = []
    for f in sorted((RAIZ / "app" / "agents").glob("*.py")):
        if f.name.startswith("_"):
            continue
        mod = importlib.import_module(f"app.agents.{f.stem}")
        for nombre, fn in vars(mod).items():
            if not nombre.startswith("cobertura") or not callable(fn):
                continue
            firma = inspect.signature(fn)
            if all(p.default is not inspect.Parameter.empty
                   for p in firma.parameters.values()):
                salida.append((f"{f.stem}.{nombre}", fn))
    return salida


def test_hay_inventarios_que_auditar():
    """Si la introspección deja de encontrarlos, las demás pruebas pasarían en
    vacío — el peor modo de fallo de una suite: verde por no mirar nada."""
    assert len(inventarios()) >= 3, (
        f"se esperaban al menos apropiacion, ejecucion y canon: {inventarios()}")


@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_todo_inventario_declara_su_universo(nombre):
    """LA REGLA DE LA CAPA 0, aplicada a todos por igual.

    No basta con decir qué encontró: hay que decir **dónde buscó, cómo, y qué
    no puede ver**. Sin eso, un resultado no es comprobable — nadie sabe sobre
    qué se hizo la afirmación, que es exactamente lo que pasó tres veces."""
    fn = dict(inventarios())[nombre]
    u = fn().get("universo")
    assert u, f"{nombre} afirma sin declarar sobre qué universo lo hace"
    for campo in _CAMPOS:
        assert campo in u, f"{nombre}: al universo le falta «{campo}»"
    assert u["fuera_de_alcance"], (
        f"{nombre} declara no tener límites. Ningún inventario de este sistema "
        f"lo consiguió todavía; declarar cero es no haberlos buscado")


@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_el_universo_declarado_coincide_con_lo_hallado(nombre):
    """El universo no puede ser prosa decorativa: `hallados` debe cuadrar con lo
    que el inventario efectivamente devuelve. Un universo que nadie contrasta se
    vuelve un adorno que envejece."""
    fn = dict(inventarios())[nombre]
    d = fn()
    u = d["universo"]
    assert isinstance(u["hallados"], int) and u["hallados"] >= 0
    filas = d.get("dominios")
    if filas is not None:
        assert u["hallados"] == len(filas), (
            f"{nombre}: declara {u['hallados']} y devuelve {len(filas)} filas")


def test_ningun_inventario_confunde_no_hallado_con_inexistente():
    """El error de fondo: cada inventario debe distinguir «no lo encontré» de
    «no existe» — el Principio Rector aplicado hacia adentro.

    ⚠️ ESTA PRUEBA YA FALLÓ UNA VEZ, Y POR SU PROPIO DEFECTO. Buscaba una lista
    literal de marcas —`no_comprobable`, `no_integrado`…— y `arquitectura.py`
    nació usando `no_determinable`: la delató como incumplidora cumpliendo. Un
    universo de marcas escrito a mano es el mismo error que perseguimos, una
    capa más arriba.

    Ahora se mide la **propiedad**: que el módulo declare al menos una constante
    pública cuyo valor nombre un estado de indeterminación. Se deriva del
    módulo, no de una lista que alguien deba mantener."""
    import importlib
    for nombre, _ in inventarios():
        mod_nombre = nombre.split(".")[0]
        mod = importlib.import_module(f"app.agents.{mod_nombre}")
        fuente = (RAIZ / "app" / "agents" / f"{mod_nombre}.py").read_text(encoding="utf-8")
        assert "fuera_de_alcance" in fuente, f"{mod_nombre} no declara sus límites"

        constantes = [v for k, v in vars(mod).items()
                      if k.isupper() and isinstance(v, str)]
        indeterminacion = [v for v in constantes
                           if any(m in v for m in ("no_determinable", "no_comprobable",
                                                   "no_integrado", "sin_", "no_la_",
                                                   "no_es_", "no_acreditado"))]
        assert indeterminacion, (
            f"{mod_nombre} no declara ningún estado de indeterminación: sin él, "
            f"«no hallado» y «no existe» salen iguales — {constantes[:8]}")


def test_la_regla_alcanza_a_los_inventarios_futuros():
    """El trinquete de la capa. Un inventario nuevo queda sujeto a la regla por
    el solo hecho de llamarse `cobertura*` en `app/agents/` — nadie tiene que
    acordarse de añadirlo a una lista. Es la diferencia entre una regla y una
    costumbre, y es lo que faltaba: la regla nació de tres errores y no se había
    aplicado a los inventarios que la produjeron."""
    nombres = [n for n, _ in inventarios()]
    assert {"apropiacion.cobertura_de_la_plataforma",
            "ejecucion.cobertura",
            "canon.cobertura_canonica"} <= set(nombres), (
        f"la introspección dejó de alcanzar a alguno de los tres: {nombres}")


# ── EXHAUSTIVIDAD DERIVADA ≠ SELECCIÓN DELIBERADA (2026-08-31) ───────────────
@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_un_universo_exhaustivo_debe_derivarse_no_enumerarse(nombre):
    """LA REGLA QUE CIERRA LA CAPA 0, con el matiz que la salva de ser absurda.

    El director propuso prohibir toda lista escrita a mano. El colega lo corrigió:

    > *«Una lista manual no siempre es un defecto. Una exclusión explícita como
    > `ADR-FORMAT.md` puede y debe ser manual: representa una decisión de
    > alcance. Lo peligroso es que una lista manual pretenda exhaustividad.»*

    Así que no se prohíbe enumerar: se prohíbe **enumerar y llamarlo universo**.
    Quien declare `tipo: derivado` debe nombrar la operación que lo descubre, y
    esa operación tiene que existir de verdad en su código — la declaración no
    se cree, se comprueba."""
    fn = dict(inventarios())[nombre]
    mod_nombre = nombre.split(".")[0]
    m = fn()["universo"]["mecanismo"]
    assert m["tipo"] in ("derivado", "explicitamente_limitado"), m
    assert m.get("por_que"), f"{nombre}: mecanismo sin justificar"

    if m["tipo"] == "derivado":
        fuente = (RAIZ / "app" / "agents" / f"{mod_nombre}.py").read_text(encoding="utf-8")
        assert m["operacion"] in fuente, (
            f"{nombre} declara descubrir por «{m['operacion']}» y esa operación "
            f"no aparece en su código: la declaración no se cree, se comprueba")


@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_toda_exclusion_declara_motivo_y_autoridad(nombre):
    """La contracara: excluir está permitido, **excluir en silencio no**. Una
    exclusión sin motivo es indistinguible de un olvido, y fue precisamente un
    olvido —`corpus_externo/`— el que costó el 23% del universo."""
    fn = dict(inventarios())[nombre]
    for e in fn()["universo"]["exclusiones"]:
        assert e.get("motivo"), f"{nombre}: exclusión sin motivo → {e}"
        assert e.get("autoridad"), (
            f"{nombre}: exclusión sin autoridad — quién decidió dejarlo fuera "
            f"es parte de la decisión → {e}")


def test_la_leccion_se_enuncia_sin_extrapolar():
    """El colega corrigió también el LENGUAJE del hallazgo, y esa corrección es
    parte de la disciplina:

    > *«No diría todavía "los universos derivados nunca fallan". La propia
    > disciplina que estamos construyendo exige no extrapolar más allá de lo
    > atacado.»*

    Lo demostrado es acotado: **en los inventarios auditados hasta ahora**, cada
    universo fijado a mano que pretendía exhaustividad resultó incompleto —los
    enrichers, los CNO de d08, el universo de d02, los territorios de ADR, el
    corpus referente—; los derivados no han producido todavía ese fallo. Que no
    lo hayan producido no es que no puedan."""
    for nombre, fn in inventarios():
        u = fn()["universo"]
        assert u["fuera_de_alcance"], (
            f"{nombre} afirma no tener límites — ninguno lo ha conseguido aún")
        # Y el límite no puede enunciarse como una garantía: un inventario que
        # promete infalibilidad deja de invitar a que lo ataquen, que es lo
        # único que hasta ahora ha encontrado algo.
        texto = " ".join(str(x) for x in u["fuera_de_alcance"]).lower()
        for absoluto in ("nunca falla", "siempre completo", "garantiza",
                         "exhaustivo y definitivo"):
            assert absoluto not in texto, (
                f"{nombre} promete «{absoluto}» en sus límites: eso es lo "
                f"contrario de declarar un límite")


# ── UN MECANISMO DE COBERTURA NO ES AUTORIDAD SOBRE SU PROPIA COBERTURA ──────
def test_un_gate_no_puede_acreditar_su_propia_cobertura():
    r"""LA REGLA QUE C2 OBLIGÓ A AÑADIR A C0 (colega, 2026-08-31):

    > *«Un mecanismo de cobertura no puede ser autoridad sobre su propia
    > cobertura. […] 0 hallazgos ≠ 0 problemas si el universo no está
    > demostrado.»*

    `check_portabilidad.py` reporta **0 rutas fijas · objetivo cumplido** desde
    hace meses. Su patrón `_ABSOLUTA` incluye `Proyectos` y detectaría
    perfectamente `C:\Proyectos\QUIRA\...` — **falla el universo, no el
    detector**: `AMBITOS` no incluye `sentinel/`, donde hay tres.

    Y `AMBITOS` no lleva motivo declarado, a diferencia de `_FRONTERA` y
    `_ABSOLUTA`, que sí lo llevan justo encima. Por eso **no se puede determinar
    si la exclusión fue decisión u omisión** — y esa indeterminación es el
    hallazgo, no las rutas.

    ⚠️ Esta prueba FIJA el estado, no lo repara. Ampliar `AMBITOS` movería un
    trinquete de 0 a 3 y eso es gobernanza. El día que se decida —incluir
    sentinel, o declarar por qué queda fuera— habrá que invertirla, y que haya
    que tocarla es la señal."""
    gate = (RAIZ / "scripts" / "ci" / "check_portabilidad.py").read_text(encoding="utf-8")

    # El detector sí sabe reconocer la ruta: lo que no la alcanza es el universo.
    assert "Proyectos" in gate, "el patrón dejó de cubrir rutas de perfil"
    assert "sentinel" not in gate, (
        "sentinel entró al gate: el hallazgo cambió y hay que reescribir esto")

    # El universo se enumera a mano y sin justificar, que es lo que C0 prohíbe
    # a los inventarios y todavía no exige a los gates de CI.
    i = gate.find("AMBITOS = ")
    contexto_previo = gate[max(0, i - 220):i]
    assert "#" not in contexto_previo.split("\n")[-2], (
        "AMBITOS ya declara motivo: entonces la exclusión es deliberada y el "
        "hallazgo pasa de «indeterminable» a «decidido»")


# ── UN LÍMITE DECLARADO TAMBIÉN DEBE RESPETARSE AL INTERPRETAR ───────────────
def test_un_instrumento_no_deja_leer_su_silencio_como_ausencia():
    """LA SEGUNDA REGLA DE C0, y es distinta de la primera (colega, 2026-08-31):

    > *«Un límite declarado por el instrumento también debe respetarse al
    > interpretar sus resultados. […] El universo puede estar correctamente
    > declarado y aun así el analista puede interpretar como exhaustivo algo que
    > el propio instrumento reconoce que no puede resolver.»*

    En la primera regla el universo estaba **mal declarado**. Aquí estaba
    **bien** declarado —«501 de 597 rutas no se resuelven»— y el analista lo
    ignoró al leer: concluyó que 422 binarios no tenían registro cuando su
    productor componía la ruta. Ningún inventario había fallado; falló la
    lectura.

    Por eso el guardián no vive en la prosa del docstring, donde nadie lo
    consulta: **el instrumento se niega a sostener una ausencia** mientras le
    queden rutas sin resolver."""
    from app.agents import acoplamiento as K

    r = K.puede_afirmarse_ausencia("lotaip/artefactos")
    assert r["veredicto"] == K.NO_DETERMINABLE, (
        "el grafo volvió a sostener una ausencia que no puede demostrar")
    assert r["por_que"] and r["donde_mirar"], (
        "una negativa sin decir dónde mirar no es accionable")

    # Y sigue pudiendo afirmar lo positivo: un uso observado es un uso observado.
    assert K.puede_afirmarse_ausencia("data/gm_snapshot.json")["veredicto"] == "usado"
