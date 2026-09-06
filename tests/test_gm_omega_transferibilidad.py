# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_transferibilidad.py — GM-Ω-ICPI-010
════════════════════════════════════════════════════════════════════════════════
`010` no pregunta «¿puede QUIRA aplicarse en otro país?» — eso se responde con
un sí vacío. Pregunta:

    ¿Qué elementos constituyen ARQUITECTURA GENERALIZABLE de inteligencia
    pública y cuáles son SOLUCIONES CONTINGENTES derivadas de la historia
    normativa, institucional, documental y metodológica del Ecuador?

    QUIRA no debe exportar Ecuador. Debe exportar su ARQUITECTURA y adaptar
    su CORPUS.

★ LA REGLA QUE EVITA REPETIR `DOC-009` EN VERSIÓN AUTOMATIZADA

    La PRESENCIA de una norma ecuatoriana no demuestra contingencia:
    demuestra acoplamiento, que hay que identificar.
    La AUSENCIA de cita normativa no demuestra universalidad.

    La máquina detecta dependencia; la dirección determina significado.

Sin ella, el script haría *detectar → clasificar → convertir la detección en
ontología*. Y un documento puede citar la Constitución sólo para ilustrar un
principio generalizable.

★ EL RESULTADO QUE IMPORTA PARA `C4`: la multiplicatividad quedó en `D`
—decisión contingente—, no en `A`. **No puede defenderse como necesaria por
ser transferible.**

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_TRANSFERIBILIDAD_010.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "transferibilidad_latam.py"


def test_010_no_toca_nada():
    """Lectura pura. `010` clasifica; no mueve componentes ni renombra."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "010 intenta escribir en el Gold Master"
    txt = _DOC.read_text(encoding="utf-8")
    assert "27,4582 %" in txt, "se perdió la constancia del baseline congelado"


def test_la_deteccion_no_se_convierte_en_ontologia():
    """★ La regla que ordena `010`, y la que impide el error automatizado.

    Un script puede contar cuántas veces aparece `COOTAD`. No puede concluir
    de ahí que un componente sea intransferible: la cita puede estar
    ilustrando un principio generalizable.

    ⚠️ Y AL REVÉS TAMBIÉN: no citar norma no vuelve universal a nada. Ambas
    direcciones del error son igual de fáciles de cometer, y las dos
    producirían una clasificación que parece medida y es inventada."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "La máquina detecta dependencia; la dirección determina " \
           "significado" in txt, (
        "desapareció la regla. Sin ella, `010` convierte un conteo de "
        "menciones en una ontología de transferibilidad")
    assert "**NO** demuestra que un componente sea contingente" in txt, (
        "se perdió la mitad que impide leer una cita normativa como prueba de "
        "que algo no viaja")
    assert "**NO** demuestra que un componente sea universal" in txt, (
        "se perdió la otra mitad: la ausencia de cita no acredita nada")
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "la categoría la fija la dirección" in fuente, (
        "el script dejó de declarar que la clasificación es un juicio "
        "declarado y no una derivación automática")


def test_las_cuatro_categorias_evitan_la_falsa_dicotomia():
    """★ La cuarta categoría, que añadió el colega.

        🟢 A núcleo          no tendría que cambiar
        🔵 B adaptador       sólo cambiar el corpus normativo
        🟠 C sedimentación   cambiar ontología, unidad, fuente y lógica
        🟣 D contingente     depende de si la decisión era necesaria

    ⚠️ SIN `D`, TODA DECISIÓN PROPIA SE COLARÍA COMO NÚCLEO por el mero hecho
    de no citar una norma. «Elegimos esta fórmula porque parecía adecuada» no
    es Ecuador, pero tampoco es arquitectura universal — y esa zona es
    justamente la que `011-C4` debe juzgar."""
    txt = _DOC.read_text(encoding="utf-8")
    for cat in ("NÚCLEO ARQUITECTÓNICO", "ADAPTADOR NORMATIVO",
                "SEDIMENTACIÓN HISTÓRICA",
                "DECISIÓN DE DISEÑO CONTINGENTE"):
        assert cat in txt, (
            f"desapareció la categoría `{cat}`. Con menos de cuatro, algún "
            f"componente cae en la equivocada por descarte")
    assert "evita una falsa dicotomía" in txt, (
        "se perdió por qué existe la categoría D")
    assert "¿qué tendría que cambiar para desplegarlo en otro país?" in txt, (
        "desapareció el test que decide la categoría. Sin criterio explícito, "
        "la clasificación es opinión")


def test_funcion_y_instancia_no_se_confunden():
    """★ El corazón de `010`.

        SERCOP  es la instancia · «portal nacional de contratación» la función
        eSIGEF  es la instancia · «sistema de ejecución presupuestaria» la función

    Lo que hace transferible a un adaptador es que su **función** existe en
    cualquier Estado aunque la **institución** que la encarna sea ecuatoriana.
    Confundirlas llevaría a declarar intransferible todo el motor por nombrar
    a `SERCOP`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Función ≠ instancia" in txt, (
        "desapareció la distinción central de 010")
    for inst in ("`SERCOP`", "`eSIGEF`", "`CPCCS`"):
        assert inst in txt, f"se perdió la instancia {inst} de la tabla"
    assert "portal nacional de contratación pública" in txt, (
        "las instancias dejaron de declarar su función generalizable, que es "
        "lo único que permite sustituirlas")


def test_el_acoplamiento_normativo_no_se_presenta_como_defecto():
    """La lectura que hay que evitar: «cuanta menos norma, más universal».

    Un motor que no citara norma no sería más transferible — sería **menos
    auditable**. La `Regla de Oro 3` («sin norma verificada, no hay dato»)
    exige el acoplamiento.

    Lo que `010` separa no es «con norma» de «sin norma», sino **norma como
    parámetro** —sustituible— de **norma como supuesto estructural**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no es un defecto" in txt, (
        "el acoplamiento normativo volvió a leerse como una atadura. Es lo "
        "que hace verificable al sistema")
    assert "menos auditable" in txt, (
        "se perdió el argumento: quitar las citas no universaliza, "
        "desacredita")


def test_la_multiplicatividad_no_se_defiende_por_transferibilidad():
    """★ El hallazgo que `010` entrega a `011-C4`.

    El motor de congruencia multiplicativa quedó clasificado en `D`
    —**decisión de diseño contingente**—, no en `A`.

    ⚠️ CONSECUENCIA DIRECTA: no puede defenderse como necesaria alegando que
    es transferible. Su transferibilidad **depende** de que la decisión fuera
    necesaria, que es exactamente lo que `C4` tiene que juzgar. Argumentar al
    revés sería circular."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no se puede defender como necesaria por ser transferible" in txt, (
        "desapareció la consecuencia para C4. Sin ella, la multiplicatividad "
        "podría defenderse con un argumento circular")
    assert "Motor de congruencia multiplicativa" in txt


def test_D_no_significa_incorrecto_ni_eliminable():
    """★ La corrección más importante antes de entrar a `C4`.

    Las cuatro categorías **no son del mismo tipo**: `A`, `B` y `C` son
    clasificaciones **estructurales**; `D` es **una incertidumbre sobre la
    necesidad del diseño**.

        D = incorrecto                                     🔴 falso
        D = debe eliminarse                                🔴 falso
        D = no puede recibir presunción de necesidad       ✅

    ⚠️ Es `DOC-027` aplicado a la arquitectura: **no validado no es
    invalidado**. Si `C4` leyera `D` como condena, el dictamen estaría escrito
    antes de empezar — y sería el error simétrico del que quisimos evitar al
    corregir el sesgo conservador."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "NO son categorías del mismo tipo" in txt, (
        "desapareció la distinción de naturaleza entre A/B/C y D. Sin ella, "
        "D se lee como una clasificación estructural más")
    assert "no puede recibir presunción de necesidad arquitectónica" in txt, (
        "se perdió la lectura correcta de D. Es la única de las tres que la "
        "evidencia sostiene")
    assert "no validado **no es** invalidado" in txt, (
        "desapareció el vínculo con DOC-027, que es lo que impide que C4 "
        "trate D como una lista de cosas a eliminar")


def test_las_cinco_decisiones_D_llegan_a_C4_con_su_pregunta():
    """★ Lo que convierte a `C4` en un peritaje y no en una opinión.

        D1  multiplicatividad      ¿razón teórica, normativa o empírica?
        D2  V_i multiplicativo     ¿la falta de evidencia debe ANULAR?
        D3  pesos 0,15/0,10/0,05   ¿justificación para conservarlos?
        D4  piso 0,50              ¿qué propiedad del fenómeno lo funda?
        D5  AVEP                   ¿qué fenómeno pretende representar?

    ⚠️ `D2` es la más grave y toca la raíz del canon: si `V=0` produce `J=0`,
    el índice mide a la vez la **gestión** y la **capacidad de demostrarla**.
    Puede ser legítimo, pero choca con el principio rector —«la ausencia de
    evidencia es un RESULTADO, nunca autorización para inferir hechos»— y `C4`
    debe resolver si anular la meta es un resultado o una inferencia.

    Y `D5` no pregunta qué escala es correcta: pregunta **qué fenómeno
    clasifica**. No se valida una escala antes de declarar su objeto
    (`DOC-012`)."""
    txt = _DOC.read_text(encoding="utf-8")
    for d in ("`D1`", "`D2`", "`D3`", "`D4`", "`D5`"):
        assert d in txt, (
            f"desapareció la decisión {d}. Las cinco deben llegar a C4 "
            f"enumeradas, o el dictamen vuelve a ser «¿está bien el ICPI?»")
    assert "«no tengo evidencia»  ≠  «el fenómeno no ocurrió»" in txt, (
        "se perdió la tensión de D2, que es la más grave: el índice puede "
        "estar midiendo la gestión y la capacidad de demostrarla a la vez")
    assert "No se puede validar una escala antes de declarar el fenómeno" in txt, (
        "D5 volvió a preguntar por la escala antes que por su objeto")
    assert "No basta con «así funciona el modelo»" in txt, (
        "desapareció el listón de D1")


def test_la_cadena_bloquea_los_dos_errores_simetricos():
    """La regla de cierre de toda la investigación:

        La historia explica. La transferibilidad clasifica.
        La metodología justifica. La evidencia decide.

    Y las tres últimas etapas preguntan cosas distintas: `C3` de dónde vino,
    `010` a qué pertenece, `C4` si merece permanecer.

    ⚠️ Eso bloquea los dos errores a la vez: «es antiguo, luego se conserva»
    (`DOC-013`) y «es contingente, luego se elimina» (`DOC-027`)."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "La historia explica. La transferibilidad clasifica." in txt, (
        "desapareció la regla que ordena la cadena entera")
    assert "es antiguo, por tanto debe conservarse" in txt and \
           "es contingente, por tanto debe eliminarse" in txt, (
        "se perdieron los dos errores simétricos. Nombrarlos es lo que "
        "impide cometerlos")


def test_010_no_declara_transferible_lo_que_no_probo():
    """La honestidad del cierre.

    Que el núcleo identificado sea **metodológico y no métrico** es
    *compatible* con la hipótesis de que lo exportable no es el ICPI sino la
    arquitectura. **No la demuestra**: haría falta un segundo caso, y hoy no
    existe (`DOC-019`: un caso no autoriza la regla general).

    ⚠️ Un `010` que devolviera «todo es núcleo» habría sido un `010` mal
    hecho. La etapa no se hizo para demostrar que QUIRA es universal."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no confirma ni refuta la hipótesis: la hace formulable" in txt, (
        "010 dejó de declarar el límite de su propio hallazgo")
    # ⚠️ La diferencia entre «en el caso analizado los A son metodológicos» y
    # «el núcleo transferible de QUIRA es metodológico». La segunda convierte
    # el resultado de una clasificación INTERNA en evidencia EXTERNA.
    assert "candidatos a núcleo arquitectónico" in txt, (
        "se perdió la palabra «candidatos». Sin ella, una clasificación "
        "declarada se lee como transferibilidad demostrada")
    assert "permanece pendiente de validación externa" in txt, (
        "desapareció el límite de la conclusión: la generalización efectiva "
        "no está probada y no puede estarlo con un solo caso")
    assert "hipótesis arquitectónica emergente" in txt, (
        "se perdió la hipótesis de que QUIRA admita múltiples modelos "
        "métricos. Registrarla sin convertirla en doctrina es lo correcto")
    assert "exigiría un segundo caso" in txt and "DOC-019" in txt, (
        "se perdió por qué la transferibilidad no está demostrada: un caso no "
        "autoriza la regla general")
    assert "habría sido un `010` mal hecho" in txt, (
        "desapareció la advertencia contra la ansiedad de universalidad. Si "
        "el resultado esperado es «todo viaja», el análisis está sesgado "
        "antes de empezar")
