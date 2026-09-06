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
    assert "exigiría un segundo caso" in txt and "DOC-019" in txt, (
        "se perdió por qué la transferibilidad no está demostrada: un caso no "
        "autoriza la regla general")
    assert "habría sido un `010` mal hecho" in txt, (
        "desapareció la advertencia contra la ansiedad de universalidad. Si "
        "el resultado esperado es «todo viaja», el análisis está sesgado "
        "antes de empezar")
