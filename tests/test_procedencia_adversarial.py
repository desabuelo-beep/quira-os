# -*- coding: utf-8 -*-
"""
tests/test_procedencia_adversarial.py — atacar la cadena, no confirmarla
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-19). El colega, tras ver `procedencia.py` funcionando:

> *«El siguiente paso debería ser cerrar el mecanismo con pruebas adversariales,
> no añadir más arquitectura. Si esos casos quedan fijados, `procedencia.py`
> deja de ser "código nuevo que parece funcionar" y pasa a ser una pieza
> canónica demostrada.»*

Tiene razón, y hay evidencia de por qué: en dos turnos consecutivos el mismo
defecto —acreditar algo por declarado en vez de por comprobado— entró primero
por el sujeto y después por la prueba del verificador. Un mecanismo que sólo se
prueba con sus casos felices no protege de eso.

Cada prueba de este archivo intenta **romper** la cadena de un modo distinto. La
regla que todas defienden:

> **QUIRA no completa una afirmación cuando la cadena de evidencia está
> incompleta: la degrada hasta el máximo grado que la evidencia permite
> sostener. Ninguna transformación puede aumentar el grado ni perder el sujeto.**

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import apropiacion as A                  # noqa: E402
from app.agents import procedencia as P                  # noqa: E402

# El par verificador↔prueba del fixture estaba CRUZADO —«componentes.verificar_
# cobertura» respaldado por la prueba de `_periodos_del_anio`— y nadie lo notaba
# porque la cadena sólo comprobaba que la prueba EXISTIERA. Al cerrar la deuda #1
# (2026-08-26) el propio fixture pasó a degradar. Ahora es un par real y vinculado.
_VERIFICADOR_REAL = "orquestador._periodos_del_anio"
_PRUEBA_REAL = "test_cadencia_trimestral_no_exige_doce_periodos"

COMPLETA = dict(
    fuente="Portal Nacional de Transparencia · Defensoría del Pueblo",
    captura="2026-08-19T10:00",
    estado_adquisicion="descargado",
    evidencia="e4585f7c44d7216b",
    verificador=_VERIFICADOR_REAL,
    prueba_del_verificador=_PRUEBA_REAL,
    sujeto="130801 Montecristi",
)


# ── 7 · el caso feliz, primero: si esto no pasa, lo demás no significa nada ─────
def test_07_con_las_siete_capas_conserva_el_grado_maximo():
    s = P.sostener("el conjunto no acredita la dimensión exigida",
                   P.Procedencia(**COMPLETA))
    assert s.peso == P.HECHO_VERIFICABLE
    assert s.habla_del_sujeto is True
    assert not s.degradada_desde and not s.faltan


# ── 1 · el sujeto no puede desaparecer al transformar ───────────────────────────
def test_01_el_sujeto_no_sobrevive_a_su_propia_desaparicion():
    """Si el sujeto se pierde en una transformación, la afirmación no puede
    seguir siendo `ejecutada` ni `validada`. Es el defecto real que tuvo
    `grados()`: el sello lo traía y la etiqueta lo perdía."""
    with pytest.raises(A.AfirmacionSinSujeto):
        A.Afirmacion("x", A.VALIDADO, "fundamento", "d07", "")
    with pytest.raises(A.AfirmacionSinSujeto):
        A.Afirmacion("x", A.EJECUCION, "fundamento", "d07", "")

    # Y en la cadena: sin sujeto no se sostiene ni el peso intermedio.
    sin = P.Procedencia(**{**COMPLETA, "sujeto": ""})
    s = P.sostener("x", sin)
    assert s.peso == P.NO_DETERMINABLE
    assert "sujeto" in s.faltan


# ── 2 · sin evidencia conservada no se habla del sujeto ─────────────────────────
def test_02_sin_evidencia_no_se_afirma_sobre_el_sujeto():
    """Se capturó, se supo en qué estado terminó, pero no quedó artefacto. Se
    puede decir que no fue posible acreditarlo; no lo que el GAD hizo."""
    s = P.sostener("x", P.Procedencia(**{**COMPLETA, "evidencia": ""}))
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert s.faltan == ["evidencia"]


# ── 3 · sin verificador, la evidencia no se interpretó ──────────────────────────
def test_03_sin_verificador_la_evidencia_no_dice_nada_por_si_sola():
    """Un archivo descargado no es un hallazgo. Alguien —un componente— tuvo que
    interpretarlo, y ese componente debe poder nombrarse."""
    s = P.sostener("x", P.Procedencia(**{**COMPLETA, "verificador": ""}))
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert "verificador" in s.faltan


# ── 4 · la prueba declarada debe EXISTIR ────────────────────────────────────────
def test_04_una_prueba_inexistente_no_respalda_nada():
    """`declarado ≠ existente`. Citar una prueba que no está es el equivalente
    exacto de citar un artículo de ley inexistente (Regla de Oro 3)."""
    s = P.sostener("x", P.Procedencia(
        **{**COMPLETA, "prueba_del_verificador": "test_inventado_que_no_existe"}))
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert s.faltan == ["prueba_del_verificador"]


# ── 6 · fuente sin captura: no se observó, se supuso ────────────────────────────
def test_06_una_fuente_que_nunca_se_consulto_no_sostiene_observacion():
    """Saber de dónde vendría el dato no es haberlo ido a buscar. Sin captura no
    hay observación: hay expectativa."""
    s = P.sostener("x", P.Procedencia(**{**COMPLETA, "captura": ""}))
    assert s.peso == P.NO_DETERMINABLE, (
        "sin captura no puede afirmarse ni siquiera un hallazgo de verificabilidad")
    assert "captura" in s.faltan


# ── la degradación nunca puede ir hacia arriba ──────────────────────────────────
def test_ninguna_transformacion_puede_subir_el_grado():
    """El sistema puede bajar el peso de una afirmación; jamás subirlo. Pedir
    `no_determinable` sobre una cadena completa no la degrada —el peso sostenible
    es el que es— pero tampoco debe reportarse como ascenso."""
    s = P.sostener("x", P.Procedencia(**COMPLETA), P.NO_DETERMINABLE)
    assert s.peso == P.HECHO_VERIFICABLE
    assert s.degradada_desde == "", "no existe la degradación hacia arriba"

    # Y una cadena pobre no mejora por pretender menos.
    pobre = P.Procedencia(fuente="DPE", sujeto="130801")
    for pretendido in (P.HECHO_VERIFICABLE, P.HALLAZGO_DE_VERIFICABILIDAD,
                       P.NO_DETERMINABLE):
        assert P.sostener("x", pobre, pretendido).peso == P.NO_DETERMINABLE


# ── 5 · el vínculo prueba↔verificador · DEUDA DECLARADA ─────────────────────────
def test_05_la_prueba_debe_respaldar_al_verificador_que_dice_acreditar():
    """✅ HUECO CERRADO el 2026-08-26. La aserción se invirtió, como estaba
    previsto en su condición de cierre.

    El colega lo anticipó el 2026-08-19:

    > *«No basta que el identificador de la prueba exista; la prueba debe estar
    > vinculada al mecanismo que dice respaldar. De lo contrario, mañana podría
    > aparecer una prueba cualquiera: el archivo existe, pero no demuestra que
    > el verificador sea correcto.»*

    Y no era hipotético. En producción, `materializacion.py` declaraba
    `materializacion.evaluar` respaldado por una prueba que comprueba los
    NOMBRES de los estados y **nunca llama a `evaluar()`** — y ninguna otra lo
    ejercitaba. Se escribió la prueba que faltaba y se corrigió la referencia.

    La correspondencia se **deriva** del AST de la función de prueba: si no
    nombra al verificador, no puede estar respaldándolo.

    ⚠️ Se cierra el escalón 3 de 4. `declarado ≠ existente ≠ CORRESPONDE ≠
    ejecutado ≠ exitoso`: que la prueba nombre al verificador no demuestra que
    lo ejecute con casos significativos. Lo que falta queda dicho, no supuesto."""
    ajena = P.Procedencia(**{**COMPLETA,
                            "verificador": "un.modulo.que.nada.tiene.que.ver"})
    s = P.sostener("x", ajena)
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD, (
        "una prueba que no nombra al verificador no puede acreditarlo")
    assert "prueba_del_verificador" in s.faltan

    # Y el caso legítimo sigue sosteniéndose: no se cerró la puerta a todos.
    assert P.sostener("x", P.Procedencia(**COMPLETA)).peso == P.HECHO_VERIFICABLE



# ── 8 · cambiar el sujeto después del sello ─────────────────────────────────────
def test_08_medir_con_evidencia_de_otro_sujeto_DETIENE_la_corrida():
    """EL AGUJERO QUE ESTA PRUEBA ENCONTRÓ, y es el más grave de los ocho.

    Antes de escribirla, alterar el sujeto del sello dejaba **todo en verde**:

        pendientes()  → ninguna
        gates         → ninguno en rojo
        corrida       → COMPLETED
        informe       → «reproducible sobre 130802 OtroMunicipio»

    …mientras medía a 130801. El sistema habría atribuido a un municipio lo
    observado en otro, con todos los archivos en su sitio y sin un solo error.

    No se degrada: se DETIENE. Una medición con evidencia de otro sujeto no es
    un resultado más débil — es una afirmación falsa sobre un tercero, y eso no
    se publica atenuado."""
    import json
    from app.agents.d07 import etapas as E
    from app.agents.d07.orquestador import ejecutar

    ruta = E._SELLO_CADENA
    if not ruta.exists():
        pytest.skip("no hay sello de cadena en este entorno")
    respaldo = ruta.read_bytes()
    try:
        d = json.loads(respaldo)
        clave = next((k for k, v in d.items() if v.get("sujeto")), None)
        if not clave:
            pytest.skip("ningún sello registra sujeto todavía")
        d[clave]["sujeto"] = "999999 MunicipioAjeno"
        ruta.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                        encoding="utf-8")

        assert clave in E.pendientes(), (
            "la evidencia de otro sujeto no puede considerarse al día")

        c = ejecutar(2025, list(range(1, 13)))
        gate = next((g for g in c.gates if g.nombre == "SUJETO"), None)
        assert gate is not None and not gate.ok, "el gate SUJETO no detuvo nada"
        assert c.estado == "BLOCKED"
        assert not c.resultados, "no puede publicarse un resultado en este estado"
    finally:
        ruta.write_bytes(respaldo)


def test_08b_sin_discordancia_el_gate_no_estorba():
    """Un gate que detiene siempre es tan inútil como uno que nunca detiene."""
    from app.agents.d07.orquestador import ejecutar
    c = ejecutar(2025, list(range(1, 13)))
    gate = next((g for g in c.gates if g.nombre == "SUJETO"), None)
    assert gate is not None and gate.ok
    assert c.estado == "COMPLETED"


# ══════════════════════════════════════════════════════════════════════════════
# FAMILIA B · ataques END-TO-END sobre la identidad del sujeto
# ══════════════════════════════════════════════════════════════════════════════
# El colega, tras el caso 8 (2026-08-19):
#
# > *«¿Dónde más puede cambiar la identidad del sujeto entre una capa y la
# > siguiente sin que el sistema lo detecte? No hace falta adivinar la
# > respuesta. Hay que atacarlo.»*
#
# Se atacó. Apareció una segunda puerta, y por eso estas pruebas existen.

def test_09_cambiar_la_identidad_en_la_fuente_DETIENE_la_corrida():
    """SEGUNDO AGUJERO, y entró justo por donde el gate no miraba.

    El gate `SUJETO` comparaba una etiqueta legible —«130801 Montecristi»—.
    Cambiar `dpe_entidad_id` de 937 a 999 **no altera esa etiqueta**: el código
    territorial y el nombre siguen iguales. Resultado del ataque, antes del
    cierre:

        entidad activa  999
        evidencia       de la entidad 937
        pendientes()    ninguna
        gates en rojo   ninguno
        corrida         COMPLETED · SITA 0,4646

    QUIRA habría medido a un GAD con la evidencia de otro, y el número tenía
    buena cara. La lección: **una etiqueta identifica para leer; una huella
    identifica para verificar.**"""
    import json
    from app.agents import sujeto as S
    from app.agents.d07 import etapas as E
    from app.agents.d07.orquestador import ejecutar

    perfil = S._SUJETOS / f"{S.POR_DEFECTO}.json"
    if not perfil.exists():
        pytest.skip("sin perfil de sujeto en este entorno")
    respaldo = perfil.read_bytes()
    try:
        d = json.loads(respaldo)
        d["identidad_en_fuentes"]["dpe_entidad_id"] = 999
        perfil.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                          encoding="utf-8")
        S.cargar.cache_clear()

        assert E.pendientes(), "la evidencia de otra entidad no está al día"
        c = ejecutar(2025, list(range(1, 13)))
        gate = next((g for g in c.gates if g.nombre == "SUJETO"), None)
        assert gate is not None and not gate.ok
        assert c.estado == "BLOCKED" and not c.resultados
    finally:
        perfil.write_bytes(respaldo)
        S.cargar.cache_clear()


def test_09b_TODO_lo_que_va_a_la_fuente_esta_huellado():
    """EL AGUJERO QUE QUEDABA DEL ATAQUE DE 2026-08-19, hallado el 2026-08-26.

    `huella()` promete en su propia docstring: *«se huella todo aquello con lo
    que se va a la fuente»*. No era cierto. Se huellaban `dpe_entidad_id`,
    `dominio_web` y los dominios asociados — **pero no el RUC**, y el RUC es
    con lo que QUIRA va realmente a la Defensoría: las 936 URLs de descarga son
    `transparencia.dpe.gob.ec/…/1360001010001/…`.

    Cambiarlo no alteraba la huella. Es **el mismo ataque que motivó la huella**
    —`dpe_entidad_id` 937→999— en un campo que se olvidó. Se descubrió al
    acreditar `descargas_indice.json`, buscando en la evidencia lo que el sello
    no decía.

    La prueba no fija una lista de campos: **deriva** los que el artefacto usa
    para ir a la fuente y exige que ninguno sea invisible a la huella. Fijar la
    lista a mano repetiría el olvido en cuanto se añada el siguiente."""
    import json

    from app.agents import sujeto as S

    perfil = S._SUJETOS / f"{S.POR_DEFECTO}.json"
    respaldo = perfil.read_bytes()
    base = S.huella()
    identidad = json.loads(respaldo.decode("utf-8"))["identidad_en_fuentes"]

    invisibles = []
    try:
        for campo, valor in identidad.items():
            d = json.loads(respaldo.decode("utf-8"))
            d["identidad_en_fuentes"][campo] = (
                "___alterado___" if not isinstance(valor, list) else ["___alterado___"])
            perfil.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                              encoding="utf-8")
            S.cargar.cache_clear()
            if S.huella() == base:
                invisibles.append(campo)
    finally:
        perfil.write_bytes(respaldo)
        S.cargar.cache_clear()

    assert not invisibles, (
        f"campos de la identidad que la huella NO ve: {invisibles}. Cambiarlos "
        f"dejaría a QUIRA midiendo a otra entidad con todos los gates en verde "
        f"— exactamente el ataque de 2026-08-19.")
    assert S.huella() == base, "la huella no volvió a su valor tras restaurar"


def test_10_la_huella_cubre_toda_la_identidad_en_fuentes():
    """La huella debe cambiar ante CUALQUIER alteración de la identidad, no sólo
    ante el identificador. El dominio web también decide qué se considera
    publicación propia del sujeto: si cambia, la evidencia anterior ya no
    corresponde."""
    import json
    from app.agents import sujeto as S

    perfil = S._SUJETOS / f"{S.POR_DEFECTO}.json"
    if not perfil.exists():
        pytest.skip("sin perfil de sujeto en este entorno")
    respaldo = perfil.read_bytes()
    original = S.huella()
    try:
        for campo, valor in (("dpe_entidad_id", 999),
                             ("dominio_web", "otro-gad.gob.ec"),
                             ("dominios_asociados", ["x.gob.ec"])):
            d = json.loads(respaldo)
            d["identidad_en_fuentes"][campo] = valor
            perfil.write_text(json.dumps(d, ensure_ascii=False, indent=1),
                              encoding="utf-8")
            S.cargar.cache_clear()
            assert S.huella() != original, (
                f"alterar «{campo}» no cambió la huella: la identidad quedaría "
                f"sin proteger por ese lado")
    finally:
        perfil.write_bytes(respaldo)
        S.cargar.cache_clear()
    assert S.huella() == original, "la huella debe ser estable si nada cambió"


def test_11_los_artefactos_derivados_no_declaran_su_sujeto():
    """⚠️ HUECO MEDIDO Y DECLARADO — la prueba fija el estado, no lo aprueba.

    Respuesta a la pregunta del colega —*«¿dónde más puede cambiar la identidad
    del sujeto entre una capa y la siguiente?»*— tras auditar los nueve puntos
    de transición de la cadena:

        [ok] perfil del sujeto        huella + gate SUJETO
        [ok] sello de la cadena       gate SUJETO (etiqueta + huella)
        [~~] captura de la fuente     lleva entidades{937}, sin huella
        [XX] índice de descargas      no declara sujeto
        [XX] análisis de contenido    no declara sujeto
        [XX] inventario documental    no declara sujeto
        [XX] contenido contenedores   no declara sujeto
        [~~] corridas persistidas     Corrida.municipio, sin huella
        [ok] autoconocimiento         derivado del sello

    Hoy la cadena los protege **indirectamente**: alterar la identidad invalida
    el sello y el gate `SUJETO` detiene la corrida. Pero un artefacto leído
    FUERA de la cadena —copiado, compartido, ingerido por otro dominio— no dice
    de quién es. Con 222 GAD produciendo los mismos nombres de archivo, esa
    ambigüedad deja de ser teórica.

    ✅ CERRADO el 2026-08-25. Los cuatro llevan ahora su procedencia dentro, y
    la estampa `_sellar()` —no un script aparte— en el mismo acto en que sella
    la cadena, de modo que sujeto sellado y sujeto estampado no pueden diverger.

    Pero NO se cerró en 4/4, y esa es la parte que importa:

        [ok] contenido.json                el sello acredita 130801
        [ok] inventario_documental.json    el sello acredita 130801
        [ok] contenido_contenedores.json   el sello acredita 130801
        [!!] descargas_indice.json         SU ETAPA NO ACREDITÓ SUJETO

    La etapa `descarga` se selló el 2026-08-19, antes de que la cadena exigiera
    declarar sujeto. Yo sé que es de Montecristi; **la cadena no lo acreditó**.
    Escribir «130801» ahí porque lo sé habría convertido un artefacto sin
    procedencia en uno que aparenta tenerla — el error exacto que este archivo
    entero persigue. Así que el artefacto declara su propio hueco, y se cierra
    cuando la etapa se vuelva a correr bajo el mecanismo de sujeto.

    Lo que ahora se defiende es más fuerte que «tienen sujeto»:

        **ningún artefacto guarda SILENCIO sobre su sujeto** — o lo declara, o
        declara por qué no puede."""
    import json
    rutas = ["data/lotaip/descargas_indice.json",
             "data/lotaip/contenido.json",
             "data/lotaip/inventario_documental.json",
             "data/lotaip/contenido_contenedores.json"]
    mudos, sin_acreditar = [], []
    for r in rutas:
        p = RAIZ / r
        if not p.exists():
            continue
        proc = json.loads(p.read_text(encoding="utf-8")).get("_meta", {}).get(
            "procedencia")
        if not proc:
            mudos.append(r)
        elif not proc.get("sujeto"):
            sin_acreditar.append((r, proc.get("estado")))

    assert not mudos, (
        f"artefactos que no dicen nada de su sujeto: {mudos}. Un archivo sale "
        f"de la cadena en cuanto alguien lo copia; ahí la protección indirecta "
        f"del gate SUJETO ya no lo alcanza.")

    # Trinquete sobre lo que la cadena NO acreditó: puede bajar, nunca subir.
    assert len(sin_acreditar) <= 1, (
        f"más etapas dejaron de acreditar sujeto: {sin_acreditar}")


def test_11b_la_procedencia_nace_en_el_generador_no_se_estampa_despues():
    """EL ERROR QUE ESTA PRUEBA IMPIDE REPETIR (2026-08-25).

    El primer intento estampó la procedencia desde `_sellar()`, después de que
    el generador escribiera el archivo. Parecía inofensivo. No lo era:

        estampo contenido.json   →  su SHA cambia
        la etapa que lo consume  →  «mi insumo cambió» →  se re-ejecuta
        re-ejecutarse            →  reanalizar 936 archivos, salir a la red

    Tres etapas quedaron desalineadas y la suite se colgó. **El acto de
    registrar la procedencia alteró aquello cuya identidad registraba.**

    El sitio correcto es el generador: ahí el archivo nace con su procedencia
    dentro, y el SHA que la cadena mide después ya la incluye. Nadie tiene que
    acordarse de estampar, y nada se mueve bajo los pies de la cadena."""
    import json

    fuente = (RAIZ / "app/agents/d07/etapas.py").read_text(encoding="utf-8")
    cuerpo = fuente[fuente.index("def _sellar("):]
    cuerpo = cuerpo[:cuerpo.index("\ndef ")]
    llamadas = [ln for ln in cuerpo.splitlines()
                if "_estampar_procedencia(" in ln and not ln.strip().startswith("#")]
    assert not llamadas, (
        f"el sellador volvió a escribir dentro de los artefactos: {llamadas}. "
        f"Eso cambia el SHA que él mismo acaba de medir y desalinea la cadena.")

    # Y que los generadores sí la escriban, que es la otra mitad del contrato.
    sin_declarar = []
    for script, etapa in (("descargar_lotaip.py", "descarga"),
                          ("analizar_contenido_lotaip.py", "contenido"),
                          ("verificar_enlaces_lotaip.py", "enlaces"),
                          ("inventario_documental.py", "inventario"),
                          ("inventario_contenido.py", "contenedores")):
        t = (RAIZ / "scripts" / "normativa" / script).read_text(encoding="utf-8")
        if f'_procedencia("{etapa}")' not in t:
            sin_declarar.append(script)
    assert not sin_declarar, (
        f"generadores que producen un artefacto mudo sobre su sujeto: "
        f"{sin_declarar}")


def test_11c_la_procedencia_del_artefacto_es_reproducible():
    """SIN RELOJ DENTRO, y es deliberado.

    Un derivado debe reconstruirse byte a byte desde su evidencia
    —`test_quira_reconstruye_sus_derivados_sin_ayuda`—. Una marca de tiempo
    dentro del artefacto lo volvería irreproducible para siempre: cada corrida
    daría un archivo distinto sin que nada hubiera cambiado.

    El **cuándo** pertenece al sello de la cadena; el **de quién**, al
    artefacto. Meter el reloj aquí ya costó un fallo real."""
    import json

    from app.agents import procedencia as P

    a = P.de_generacion("contenido", "130801 Montecristi", "abc123")
    b = P.de_generacion("contenido", "130801 Montecristi", "abc123")
    assert a == b, "dos llamadas iguales dieron resultados distintos"

    prohibidas = {"sellado", "generado", "fecha", "timestamp", "cuando"}
    for art in ("data/lotaip/contenido.json", "data/lotaip/enlaces.json",
                "data/lotaip/inventario_documental.json",
                "data/lotaip/contenido_contenedores.json"):
        p = RAIZ / art
        if not p.exists():
            continue
        proc = json.loads(p.read_text(encoding="utf-8")).get(
            "_meta", {}).get("procedencia", {})
        intrusas = prohibidas & set(proc)
        assert not intrusas, (
            f"{art} guarda un reloj en su procedencia ({intrusas}): deja de "
            f"poder reconstruirse byte a byte")


def test_12_sin_atacar_no_puede_leerse_como_seguro():
    """El colega lo puso en rojo (2026-08-19):

    > *«"Sin atacar" no puede convertirse en "seguro" por defecto. Eso debería
    > entrar directamente en el autoconocimiento de QUIRA.»*

    Es el mismo error que el sistema acaba de descubrir a nivel de sujeto,
    ahora a nivel de plataforma: confundir ausencia de contradicción con
    evidencia de validez. Un dominio sin defensas no las resistió — no las
    tiene."""
    from app.agents import apropiacion as A
    c = A.cobertura_de_la_plataforma()
    estados = {f["dominio"]: f["estado"] for f in c["dominios"]}

    assert estados.get("d07") == A.PROTEGIDO_Y_ATACADO

    # ⚠️ CUARTA VEZ QUE ESTE TEST SE ROMPE POR LO MISMO, y la causa raíz no era
    # ninguna de las tres correcciones anteriores: **reimplementaba la detección
    # de ataques con nombres de archivo**, en paralelo al inventario. Cada vez que
    # el inventario mejoró —contar propiedad, no nombre— esta copia se quedó atrás:
    #
    #   1ª  «sólo d07 puede estar atacado»          ← el estado de agosto como propiedad
    #   2ª  buscaba `test_<dom>_adversarial.py`     ← el nombre del archivo
    #   3ª  añadía búsqueda genérica en esos mismos archivos
    #   4ª  d03 trae sus ataques en `test_d03_agente.py` y no lo veía
    #
    # Se deja de reimplementar: se comprueba la PROPIEDAD sobre el dato que el
    # inventario ya deriva. Dos formas de contar lo mismo divergen siempre — es
    # el mismo principio que impide dos caminos a la misma verdad (2026-08-30).
    for fila in c["dominios"]:
        if fila["estado"] != A.PROTEGIDO_Y_ATACADO:
            continue
        assert fila.get("ataques_ejecutados", 0) > 0, (
            f"{fila['dominio']} figura como atacado con 0 ataques ejecutados: "
            f"«sin atacar» se estaría leyendo como «seguro»")
        assert fila.get("defensas"), (
            f"{fila['dominio']} figura como atacado sin defensa alguna que "
            f"pudiera resistir el ataque")

    # La afirmación publicable nombra el alcance, nunca la plataforma entera.
    #
    # ⚠️ Antes se comprobaba la frase literal «los demás dominios permanecen sin
    # evidencia». Eso ataba la prueba a una REDACCIÓN, no a una propiedad: al
    # mejorar la afirmación —para que dijera además que esos dominios ni siquiera
    # están integrados— la prueba falló sin que nada se hubiera roto. Se comprueba
    # la propiedad (2026-08-26).
    afirmacion = c["afirmacion_sostenible"]
    assert "d07" in afirmacion, "la afirmación debe nombrar dónde está demostrado"
    for dom, est in estados.items():
        if est != A.PROTEGIDO_Y_ATACADO:
            assert dom in afirmacion, (
                f"{dom} no figura en la afirmación: un dominio sin el mecanismo "
                f"demostrado no puede quedar fuera del relato, o la afirmación "
                f"se leería como si cubriera la plataforma entera")


def test_12b_no_integrado_no_es_lo_mismo_que_desprotegido():
    """LA DISTINCIÓN QUE LA DEUDA #3 NO HACÍA (2026-08-26).

    El registro decía «cinco dominios sin la defensa», y era cierto: se comprobó
    por PROPIEDAD —ninguno compara identidad, ninguno detiene por sujeto, ninguno
    huella— y no por los nombres de d07, que es como se había medido antes.

    Pero al medir la integración apareció lo que la etiqueta ocultaba: **ningún
    módulo importa esos cinco paquetes.** `no_protegido` se lee como «existe y
    está expuesto»; la verdad era «existe y no está conectado».

    La distinción corta en dos direcciones, y por eso no es cosmética: el riesgo
    de hoy es menor del que el registro sugería, y el de mañana es idéntico.
    Confundirlas lleva o a alarmarse de más, o —peor— a integrarlos sin exigirles
    la defensa.

    Lo que esta prueba defiende es que el estado **se deriva**: el día que
    alguien importe uno de esos paquetes, el inventario debe decir «expuesto»
    sin que nadie tenga que acordarse de cambiarlo."""
    from app.agents import apropiacion as A

    for f in A.cobertura_de_la_plataforma()["dominios"]:
        if f["estado"] in (A.NO_INTEGRADO, A.NO_PROTEGIDO):
            assert "importadores" in f, (
                f"{f['dominio']} no declara cuántos módulos lo importan: sin ese "
                f"dato, «no protegido» y «no integrado» son indistinguibles")
            esperado = A.NO_INTEGRADO if f["importadores"] == 0 else A.NO_PROTEGIDO
            assert f["estado"] == esperado, (
                f"{f['dominio']}: estado «{f['estado']}» con "
                f"{f['importadores']} importadores — el estado no se está "
                f"derivando de la integración real")
