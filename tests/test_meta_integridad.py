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
import re
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

    ⚠️ SUBSANADO 2026-09-02 · D-004, y esta prueba se invirtió: era la señal
    pactada. La versión anterior decía «`sentinel` NO puede aparecer en el gate»
    y hoy exige lo contrario. Lo que NO cambió es la regla de C0 — sólo cambió
    quién la cumple.

    El gate ya no enumera carpetas: **deriva su universo** de `RAIZ.rglob` y
    resta `_EXCLUIDOS`, donde cada exclusión lleva su motivo escrito al lado.
    Excluir sigue permitido; excluir en silencio, no — porque el silencio es
    justo lo que impide distinguir la decisión de la omisión.

    El trinquete pasó de 0 a 3 y eso NO es una regresión: el sistema no se ató
    más a una máquina, el instrumento dejó de ser ciego."""
    gate = (RAIZ / "scripts" / "ci" / "check_portabilidad.py").read_text(encoding="utf-8")

    # El detector sí sabía reconocer la ruta: lo que no la alcanzaba era el universo.
    assert "Proyectos" in gate, "el patrón dejó de cubrir rutas de perfil"

    # 1 · El universo se deriva, no se enumera.
    assert "AMBITOS = (" not in gate, "volvió la lista de carpetas escrita a mano"
    assert "RAIZ.rglob" in gate, "el gate dejó de derivar su universo"

    # 2 · Y toda exclusión lleva motivo: sin él no se puede saber si fue decisión.
    assert "_EXCLUIDOS" in gate, "desapareció el registro de exclusiones"
    exclusiones = re.findall(r'\("([^"]+)",\s*"([^"]*)"', gate)
    assert exclusiones, "no se pudo leer ninguna exclusión: cambió su forma"
    mudas = [p for p, motivo in exclusiones if len(motivo.strip()) < 20]
    assert not mudas, f"exclusiones sin motivo declarado: {mudas}"


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


# ── TERCERA REGLA · UNIDAD ───────────────────────────────────────────────────
def test_una_metrica_no_combina_unidades_distintas():
    """LA TERCERA REGLA DE C0 (colega, 2026-09-01), que completa la familia:

        1 · ALCANCE          no afirmar sobre lo que no fue incluido
        2 · DETERMINABILIDAD no convertir un límite del instrumento en ausencia
        3 · UNIDAD           no combinar numerador y denominador de unidades
                             distintas

    Nació de un número mío. Reporté «204 documentos sin trazabilidad»: la resta
    era **correcta dentro de una unidad que nunca declaré** —240 nombres únicos
    menos 36—, y presentarla como documentos la volvía falsa. Sustituirla por
    222 (258 − 36) habría sido igual de incorrecto: mezcla archivos con nombres.

    Ahora los tres contadores viven separados y sólo se restan los homogéneos."""
    from app.agents import datos as D

    e = D.evidencia_primaria()
    if e.get("estado") == "no_determinable":
        import pytest
        pytest.skip(e["por_que"])
    assert e["unidad_de_trazabilidad"] == "nombres de archivo únicos"
    assert (e["nombres_con_trazabilidad"] + e["nombres_no_determinables"]
            == e["nombres_unicos"]), "la resta cruza unidades"
    assert e["archivos_fisicos"] >= e["documentos"] >= e["nombres_unicos"], (
        "los tres contadores dejaron de ser consistentes entre sí")
    assert (e["archivos_fisicos"] - len(e["excluidos_por_clasificacion"])
            == e["documentos"]), "los excluidos no explican la diferencia"


def test_lo_excluido_se_clasifica_no_se_enumera():
    """*«La prueba debe comprobar la clasificación, no simplemente una lista de
    nombres prohibidos»* — colega. Un `if name == "desktop.ini"` sería la misma
    lista escrita a mano que esta sesión lleva diez casos desmontando.

    Se excluye por **atributo del sistema de archivos** (OCULTO ∧ SISTEMA), que
    es una propiedad del objeto y no de su nombre. Verificado: identifica
    exactamente los mismos 9, y capturaría uno futuro con otro nombre."""
    from app.agents import datos as D

    fuente = (RAIZ / "app" / "agents" / "datos.py").read_text(encoding="utf-8")
    assert "st_file_attributes" in fuente, (
        "la exclusión volvió a decidirse por el nombre del archivo")
    e = D.evidencia_primaria()
    if e.get("estado") == "no_determinable":
        import pytest
        pytest.skip(e["por_que"])
    for x in e["excluidos_por_clasificacion"]:
        assert x["clase"] and x["motivo"], f"exclusión sin clasificar: {x}"


# ── EL MISMO PATRÓN, UN NIVEL ARRIBA · D-007 ─────────────────────────────────
def test_ataque_un_gate_que_no_se_ejecuta_no_acredita_nada():
    """D-007 · EL HALLAZGO QUE APARECIÓ AL CERRAR D-004, y es el séptimo caso del
    mismo patrón en dos días.

    D-004 era un gate con el universo mal declarado: veía 0 porque no miraba
    `sentinel/`. Al repararlo salió la pregunta obvia —*¿y los demás gates?*— y
    la respuesta es peor que el defecto original:

        12 gates en `scripts/ci/` · **1 se ejecuta en CI**
        33 archivos de prueba · **`pytest` no es un paso de ningún workflow**

    Un gate ciego al menos corre y puede acertar por accidente. Un gate que no
    se ejecuta acredita cero hallazgos **por no existir**, y su verde es el
    silencio de nadie preguntando. Es la forma extrema de la regla de C0: no ya
    un mecanismo que es autoridad sobre su propia cobertura, sino uno cuya
    cobertura es cero y nadie lo sabe.

    ⚠️ ESTA PRUEBA FIJA EL ESTADO, NO LO REPARA, y esta vez por una razón que no
    es sólo de método: `.github/workflows/*` está **congelado** (Regla de Oro 5)
    y engancharlo es decisión de Javo, no mía. Enganchar 11 gates de golpe sobre
    un repositorio que nunca los corrió tampoco es una mejora: es un CI rojo de
    origen desconocido. El orden correcto es correr cada uno a mano, ver qué
    dice, y engancharlo cuando esté en verde.

    El día que se enganche, esta prueba falla — y ese fallo es la señal."""
    gates = sorted(p.name for p in (RAIZ / "scripts" / "ci").glob("check_*.py"))
    pasos: list[str] = []
    for w in (RAIZ / ".github" / "workflows").glob("*.y*ml"):
        pasos += re.findall(r"^\s*run:\s*(.+)$",
                            w.read_text(encoding="utf-8", errors="replace"), re.M)

    ejecutados = {g for g in gates if any(g in c for c in pasos)}
    assert len(gates) >= 12, "el inventario de gates se derivó mal"
    assert ejecutados == {"check_health.py"}, (
        f"cambió qué gates corren en CI: ahora {sorted(ejecutados)}. Si CRECIÓ, "
        f"D-007 avanzó y hay que actualizar esta prueba y el registro de deuda")

    # `pytest` aparece en `claude.yml`, pero como permiso de herramienta del bot
    # —`Bash(python -m pytest *)`—, no como paso de CI. Medir la palabra habría
    # dado un falso positivo; se mide el paso `run:`, que es lo que se ejecuta.
    assert not [c for c in pasos if "pytest" in c], (
        "la suite entró a CI: D-007 avanzó y esta prueba debe invertirse")


def test_ataque_el_gate_visual_vigila_la_puerta_no_las_habitaciones():
    """D-008 · LA REINCIDENCIA, y es lo que la hace grave.

    `check_sistema_visual` ya cayó en esto el 2026-08-08: cubría sólo
    `views/login_view.py` y pasaba en verde mientras `env_civic.py` usaba
    #22C55E en cinco sitios. Su propio comentario guarda la lección —*«el gate
    protegía la entrada y dejaba sin vigilar las pantallas donde la gente pasa
    el tiempo»*— y la reparación fue ampliarlo a los 5 ambientes.

    Pero los ambientes **son otra vez la entrada**: `env_gov`, `env_ops` y
    `qinv` enrutan a 25 páginas vivas que sí usan verde de «bien». La lección se
    aplicó al caso, no al patrón.

    ⚠️ NO SON 26 INFRACCIONES, y la diferencia es la de siempre en esta capa:
    `app/viz/` está excluido CON motivo escrito —una rampa de color puede ser
    legítima en un mapa— y `p11_ods` usa los verdes oficiales de Naciones
    Unidas, que son identidad ajena y no un juicio de bondad. Un barrido que no
    distinga eso rompería lo correcto junto con lo incorrecto.

    Esta prueba fija el estado. El día que el gate mire las páginas, falla."""
    gate = (RAIZ / "scripts" / "ci" / "check_sistema_visual.py").read_text(encoding="utf-8")
    assert 'glob("quira_pages/env_*.py")' in gate, (
        "cambió cómo el gate arma su universo: si CRECIÓ, D-008 avanzó")

    def _verde_de_bien(h: str) -> bool:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return g > r + 30 and g > b + 30          # el mismo criterio del gate

    def _codigo(p) -> str:
        """Sin comentarios, con la misma poda que el gate — y por la misma razón.

        El gate la añadió el 2026-08-10 tras dispararse con su propia
        documentación: al retirar #22C55E de `umi.py` y explicar en un
        comentario cuál era el color retirado, volvió a encontrarlo. Esta
        prueba repitió el caso hoy, con el comentario que escribí en
        `env_obs.py` al aplicarle la paleta. Un `#` de Python no llega al
        navegador."""
        import io
        import tokenize
        try:
            toks = tokenize.generate_tokens(io.StringIO(
                p.read_text(encoding="utf-8", errors="replace")).readline)
            return "\n".join(t.string for t in toks if t.type != tokenize.COMMENT)
        except Exception:                                   # noqa: BLE001
            return p.read_text(encoding="utf-8", errors="replace")

    vigilados = {p.name for p in (RAIZ / "quira_pages").glob("env_*.py")} | {"umi.py"}
    hex_ = re.compile(r"#([0-9a-fA-F]{6})\b")
    fuera = [p.name for p in (RAIZ / "quira_pages").glob("*.py")
             if p.name not in vigilados
             and any(_verde_de_bien(h) for h in hex_.findall(_codigo(p)))]

    # Los ambientes vigilados están limpios — y esa limpieza es justamente lo
    # que hace creíble un verde que no cubre donde está el problema.
    for p in (RAIZ / "quira_pages").glob("env_*.py"):
        assert not any(_verde_de_bien(h) for h in hex_.findall(_codigo(p))), (
            f"volvió el verde a un ambiente vigilado: {p.name}")

    assert len(fuera) >= 15, (
        f"quedan {len(fuera)} páginas con verde fuera del universo del gate. Si "
        f"BAJÓ, D-008 avanzó y hay que actualizar el registro: {sorted(fuera)}")
