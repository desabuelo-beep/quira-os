# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_serie_motor.py — GM-Ω-ICPI-011-C3R · serie temporal
════════════════════════════════════════════════════════════════════════════════
`011-C3` declaró `NO DETERMINABLE` la razón de tres transformaciones de `C_i`.
Después Javo señaló —como paréntesis, dudando si era necesario— una carpeta con
la historia del proyecto. Al medirla aparecieron **83 versiones fechadas del
Gold Master** que `C3` no había examinado.

★ LO QUE LA SERIE DEMOSTRÓ

    25-abr-2026   última versión SIN el mecanismo determinista   58 hojas
    27-abr-2026   fecha declarada en H01!A94
    29-abr-2026   primera versión CON el mecanismo               72 hojas

    Y entran JUNTOS: mecanismo · pesos 0,05/0,10/0,15 · piso 0,50 ·
    fallback Ci_Manual_2025 · Sección L · Sección M

`C_i` **no derivó: fue refactorizado en un solo acto de diseño**, y la fecha que
el autor declaró cae dentro de la ventana — corroborada por evidencia
independiente.

⚠️ Y EL LÍMITE QUE NO SE CRUZA. La serie demuestra CUÁNDO y QUÉ. No demuestra
POR QUÉ. Que cuatro cosas entren juntas hace **plausible** una decisión
deliberada; plausible no es demostrado, y confundirlos sería `DOC-009`.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SERIE_MOTOR_011C3R.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "serie_temporal_motor.py"


def test_la_serie_es_lectura_pura():
    """Ochenta y dos libros abiertos, ninguno modificado. Y no se toca el Gold
    Master vigente: la serie son copias históricas en disco."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "C3R intenta escribir en un libro"
    assert "data_only=False, read_only=True" in fuente, (
        "los libros dejaron de abrirse en modo lectura")
    txt = _DOC.read_text(encoding="utf-8")
    assert "27,4582 %" in txt, "se perdió la constancia del baseline congelado"


def test_la_reapertura_no_invalida_ni_confirma_por_defecto():
    """★ `DOC-031` · la formulación que evita los dos extremos.

    Decir «`C3` no usó la serie, luego `C3` está incompleto» sería demasiado
    fuerte y prejuzgaría. La formulación forense es que `C3` se ejecutó sobre
    el corpus **disponible**, y después apareció un corpus externo relevante
    que no formó parte de su universo de revisión — así que se abre una
    **verificación de sensibilidad documental**.

    ⚠️ EL RESULTADO PODÍA SER CUALQUIERA: sin cambio, parcial o reabierto. Fue
    el intermedio, y eso hay que decirlo tal cual: `C3` **no se invalidó, se
    precisó**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "verificación de sensibilidad documental" in txt, (
        "desapareció la formulación forense de la reapertura. Sin ella, "
        "revisar una conclusión cerrada se lee como desautorizarla")
    assert "No prejuzga el resultado" in txt, (
        "se perdió que la verificación podía terminar sin cambio. Una "
        "reapertura que da por hecho que encontrará algo no es una "
        "verificación: es una búsqueda de confirmación")
    assert "no se invalidan" in txt and "se **precisan**" in txt, (
        "el expediente dejó de declarar qué le pasó a C3. Ni invalidado ni "
        "confirmado: precisado, que es el tercer resultado")


def test_el_corte_queda_fechado_y_corrobora_la_declaracion():
    """★ El hallazgo. La ventana del cambio se acota a cuatro días, y la fecha
    que el autor declaró en `H01!A94` **cae dentro**.

    Eso convierte una declaración del autor en un hecho corroborado por
    evidencia independiente — que es exactamente lo que `DOC-024` pedía y que
    en `011-C2` no se pudo hacer."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "última versión **sin** el mecanismo determinista" in txt
    assert "primera versión **con** el mecanismo determinista" in txt
    assert "cae dentro de la ventana" in txt, (
        "se perdió la corroboración. Es lo que eleva `H01!A94` de declaración "
        "del autor a hecho verificado contra una fuente independiente")
    assert "2026-04-27" in txt, (
        "desapareció la fecha declarada contra la que se contrasta")


def test_el_cambio_fue_un_acto_unico_y_eso_no_prueba_su_causa():
    """★ Lo que la serie demuestra, y lo que sigue sin demostrar.

    Mecanismo, pesos, piso, fallback y las dos secciones de `H01` entran en la
    **misma versión**. No hay pesos intermedios que se ajustaran después, ni un
    piso añadido más tarde: **descarta la calibración iterativa**. Y el libro
    pasa de 58 a 72 hojas — una refactorización mayor, no un ajuste.

    ⚠️ PERO LA CAUSA SIGUE SIN CONSTAR. Que cuatro cosas entren juntas hace
    plausible una decisión deliberada y única. Plausible no es demostrado. El
    resultado exacto es:

        SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA

    Si esa segunda mitad se pierde, la serie se leerá como si explicara el
    porqué — y eso es inferir la intención desde el resultado, `DOC-009`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no derivó: fue REFACTORIZADO en un solo acto de diseño" in txt, (
        "desapareció el hallazgo central de C3R")
    # ⚠️ «Descarta la calibración iterativa» era MÁS FUERTE de lo que la serie
    # permite: pudo haber ajustes fuera de los artefactos preservados, o una
    # calibración desarrollada antes y materializada de golpe.
    assert "no evidencia una calibración iterativa" in txt, (
        "se perdió la formulación acotada. «Descartar» afirma sobre lo que no "
        "se conservó; lo defendible es que la serie PRESERVADA no lo evidencia")
    assert "sin soporte documental" in txt, (
        "desapareció el grado exacto de la inferencia sobre la calibración")
    assert "consistente con una modificación estructural sustantiva" in txt, (
        "volvió «las 14 hojas demuestran una refactorización mayor». Un "
        "aumento de hojas es CONSISTENTE con un cambio estructural; por sí "
        "solo no lo demuestra")
    assert "«Entraron juntos» ≠ «sabemos por qué entraron juntos»" in txt, (
        "se perdió la salvedad de DOC-009. La simultaneidad sugiere una "
        "decisión deliberada; no la prueba")
    for grado in ("✅ DEMOSTRADO", "🟡 INFERENCIA RAZONABLE", "🔴 NO DEMOSTRADO"):
        assert grado in txt, (
            f"desapareció el grado `{grado}`. Sin los tres separados, una "
            f"inferencia razonable se lee como un hecho demostrado")


def test_la_fase3_encuentra_la_razon_del_constructo_y_no_la_de_los_pesos():
    """★ El resultado de la Fase 3, y el matiz que lo hace utilizable.

    `GOLDMASTER_REFACTOR_MASTER_v2.0.md` no menciona `C_i`: **lo corrige**. Lo
    cataloga como `E-CRIT-04` —error crítico— y prescribe el reemplazo, con la
    razón escrita:

        «Ci evalúa la CALIDAD DEL EXPEDIENTE ADMINISTRATIVO vía infracciones
         normativas verificadas — nunca el estatus jurídico de ninguna
         entidad.»

    Eso mueve `P5a` de `NO DETERMINABLE` a `DECLARADO`. Y encaja con el canon:
    evaluar el estatus jurídico de una entidad sería lenguaje acusatorio, que
    la `Regla de Oro 2` prohíbe.

    ⚠️ PERO NO CUBRE TODO. El documento **enuncia** los pesos y el piso; no los
    justifica. `P5b` y `P5c` siguen `NO DETERMINABLE`, y presentar la Fase 3
    como si hubiera cerrado el porqué entero sería exagerar el hallazgo."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "E-CRIT-04" in txt, (
        "desapareció el hallazgo de la Fase 3: la definición anterior de C_i "
        "se catalogó como error crítico, no se abandonó sin más")
    assert "nunca el estatus jurídico de ninguna entidad" in txt, (
        "se perdió la razón declarada del cambio de constructo")
    assert "**DECLARADO**" in txt and "no `DEMOSTRADO`" in txt, (
        "el grado se perdió. Una razón escrita por el autor en un artefacto "
        "de trabajo es DECLARADO — DOC-024 sigue aplicando")
    assert "los enuncia, no los justifica" in txt, (
        "desapareció el límite de la Fase 3. Los pesos y el piso siguen sin "
        "justificación, y presentar el hallazgo como si cerrara el porqué "
        "entero sería exagerarlo")


def test_cerrar_C3R_no_agota_la_genealogia():
    """★ La salvaguarda que impide que `BM-05` se vuelva un pozo sin fondo.

    Cerrar `C3-R` **no** significa que la genealogía histórica de QUIRA esté
    agotada: significa que la evidencia examinada basta para actualizar las
    conclusiones **específicas** de `C3` sin ampliar la búsqueda de forma
    indefinida.

    ⚠️ Y la ausencia de justificación de los parámetros permanece como
    HALLAZGO, no como pendiente: «los parámetros fueron establecidos
    documentalmente, pero su fundamento cuantitativo no ha sido determinado».
    Para `011-C4` eso vale más que la historia completa — un parámetro sin
    fundamento cuantitativo es una decisión de diseño **abierta** (`DOC-027`),
    y hay tres."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no implica que la genealogía histórica completa" in txt, (
        "desapareció la salvaguarda. Sin ella, «C3-R cerrado» se lee como "
        "«ya no hay nada que buscar en BM-05», que es falso")
    assert "pozo sin fondo" in txt, (
        "se perdió la razón de la salvaguarda: perseguir indefinidamente una "
        "frase que quizá nunca se escribió no es método")
    assert "su **fundamento cuantitativo no ha sido determinado**" in txt, (
        "la ausencia dejó de declararse como hallazgo. Un pendiente se "
        "arrastra; un hallazgo entra al dictamen")
    assert "C3-R` — CERRADO" in txt


def test_las_cinco_preguntas_no_se_colapsan_en_una():
    """★ La arquitectura epistemológica que `C3-R` deja montada.

        Historia                  ¿qué mecanismo existía?          DEMOSTRADO
        Evolución                 ¿cuándo fue sustituido?          DEMOSTRADO
        Decisión                  ¿qué razón declaró el autor?     DECLARADO
        Justificación metodológica ¿es válida esa solución?         → 011-C4
        Parámetros                ¿por qué 0,15/0,10/0,05 y 0,50?  NO DETERMINABLE

    ⚠️ Tratarlas como una sola —«la razón del cambio»— fue lo que hizo que
    `011-C3` cerrara con un `NO DETERMINABLE` demasiado grueso. Hoy hay
    respuestas de **calidad distinta** para cada una, y colapsarlas destruiría
    justamente esa precisión."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Cinco preguntas distintas, cinco calidades de respuesta" in txt, (
        "desapareció la separación de las cinco preguntas")
    for p in ("**Historia**", "**Evolución**", "**Decisión**",
              "**Justificación metodológica**", "**Parámetros**"):
        assert p in txt, (
            f"se perdió la pregunta {p}. Con menos de cinco, alguna se "
            f"responde con la calidad de evidencia de otra")


def test_la_definicion_anterior_se_conserva_como_antecedente():
    """La precisión sobre qué le pasó al `C_i` original.

    «No se abandonó, se catalogó como error crítico» es impreciso: **sí fue
    abandonada como mecanismo operativo**. Lo que sobrevive es su condición de
    antecedente histórico.

    Es exactamente la categoría `📜 SUPERADO METODOLÓGICAMENTE` de la carta —
    y la distinción importa porque `BM-05` conserva antecedentes, no reglas
    vigentes."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "conservada como antecedente histórico" in txt, (
        "se perdió qué le pasó a la definición original: sobrevive como "
        "antecedente, no como mecanismo")
    assert "mecanismo operativo fue declarado un defecto crítico y " \
           "sustituido" in txt, (
        "desapareció que el mecanismo SÍ fue abandonado. Decir que «no se "
        "abandonó» sugeriría que ambas definiciones siguen operando")


def test_la_palabra_refactorizacion_declara_su_fuente():
    """Disciplina de procedencia aplicada a un adjetivo.

    «Refactorización» se usa porque **existe un documento que se declara a sí
    mismo proceso de refactorización** y prescribe los cambios. El incremento
    de 58 a 72 hojas es sólo **consistente** con ella.

    ⚠️ Si la fuente de la clasificación fuera el conteo de hojas, sería
    inferir la naturaleza de un cambio desde su tamaño — y eso es el mismo
    error de forma que `DOC-009`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "La fuente de esa clasificación es ese documento, no el " \
           "incremento de hojas" in txt, (
        "desapareció la procedencia de la palabra «refactorización». Un "
        "adjetivo sin fuente es una inferencia disfrazada de descripción")


def test_P6_tiene_expediente_propio_y_no_cabe_en_010():
    """`P6` es **identidad de artefactos**; `010` es **transferibilidad
    LATAM**. Meterla ahí mezclaría dos problemas sin relación.

    Y si se cierra, se cierra con un grafo de correspondencia cuya taxonomía
    —`1:1` · `PROBABLE` · `RAMIFICACIÓN` · `DUPLICADO` · `NO DETERMINABLE`—
    es la de `011-B`, que aparece por tercera vez en esta investigación."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no cabe en `010`" in txt, (
        "P6 volvió a mezclarse con la transferibilidad LATAM")
    assert "grafo de correspondencia de versiones" in txt
    assert "**No bloquea a `C4`**" in txt, (
        "se perdió que P6 no es bloqueante. Una cuestión abierta que no "
        "bloquea nada debe decirlo, o se convierte en excusa para no avanzar")


def test_P5_y_P6_no_se_mezclan():
    """Son problemas distintos: `P5` es **causalidad histórica** —por qué se
    sustituyó—; `P6` es **identidad y versionado** —cómo se corresponden las
    nomenclaturas—.

    `P6` podría resolverse por completo mañana y `P5b`/`P5c` seguir abiertas.
    No sería una contradicción, y confundirlas haría parecer que resolver el
    versionado explica la decisión de diseño."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "son problemas distintos y no deben mezclarse" in txt, (
        "P5 y P6 volvieron a tratarse como una sola cuestión abierta")
    assert "causalidad histórica" in txt and "identidad y versionado" in txt


def test_versiones_unicas_no_es_estados_del_motor():
    """La salvaguarda de cardinalidad.

    «71 artefactos únicos por contenido» **no** es «71 estados históricos del
    motor». Un hash distinto puede deberse a un cambio en el motor, en los
    datos, en otra hoja, o a algo cosmético.

    ⚠️ Sin esta distinción, alguien podría objetar con razón que el estudio
    confunde *archivo distinto* con *versión metodológica distinta* — y por
    eso el análisis trabaja con transiciones de variables relevantes, no con
    diferencias binarias del libro."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "artefactos históricos únicos por contenido" in txt, (
        "se perdió la terminología precisa. «Versiones» sugiere estados "
        "metodológicos distintos, y un hash distinto no lo prueba")
    assert "evidencia estructural suficiente del motor" in txt, (
        "desapareció la calificación de los 68 libros: no son «los que "
        "tienen H12», son los que traen evidencia suficiente para LAS "
        "PREGUNTAS EXAMINADAS")
    assert "confundiría *archivo distinto* con *diseño distinto*" in txt, (
        "se limpió la salvaguarda que explica por qué la terminología importa")


def test_el_ruido_de_lectura_no_se_cuenta_como_transicion():
    """La disciplina que hace fiable la serie.

    Algunos libros se guardaron con valores en vez de fórmulas, y entonces el
    conteo de factores lee `0` sin que el motor haya cambiado. Una transición
    que va y vuelve el mismo día, con todas las demás propiedades intactas,
    **es un artefacto de lectura**.

    ⚠️ Contarla sería FABRICAR GENEALOGÍA — inventar un cambio de diseño que
    nunca ocurrió, en un expediente cuyo objeto es reconstruir cambios
    reales."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "ruido de lectura" in txt, (
        "desapareció el filtro de artefactos de lectura")
    assert "fabricar genealogía" in txt, (
        "se perdió por qué importa: un falso positivo aquí no es un error de "
        "conteo, es un cambio de diseño inventado")


def test_las_copias_se_deduplican_por_contenido():
    """82 archivos, 71 versiones únicas. Deduplicar por SHA-256 evita leer el
    mismo libro varias veces y —lo que importa— **evita contar una copia como
    una transición**: el mismo contenido con otro nombre y otra fecha de
    archivo parecería un cambio y no lo es."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "sha256" in fuente.lower(), (
        "la deduplicación por contenido desapareció")
    txt = _DOC.read_text(encoding="utf-8")
    assert "únicos por contenido" in txt
    assert "copias exactas" in txt, (
        "se perdió la constancia de cuántos archivos eran duplicados")
