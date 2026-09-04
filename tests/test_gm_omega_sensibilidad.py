# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_sensibilidad.py — GM-Ω-ICPI-007 · el laboratorio no se escapa
════════════════════════════════════════════════════════════════════════════════
Un experimento de sensibilidad produce números interesantes que NO son el ICPI.
El riesgo clásico de las auditorías es que uno de ellos sobreviva a su contexto:

    alguien ejecuta una simulación, obtiene una cifra atractiva, y seis meses
    después esa cifra aparece publicada como «el ICPI».

Eso no es una hipótesis: es el patrón del «48,33 %», que vivió 22 días en
`p16_gobernanza` después de que Javo retirara el método que lo producía. Estas
pruebas existen para que los 16 escenarios de `007` no puedan repetirlo.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SENSIBILIDAD_007.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "sensibilidad_icpi.py"
_FICHA = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_FICHA_FORENSE.md"

# El baseline congelado por la regla GM-Ω-ICPI-000, en las dos escalas en que
# el motor lo guarda: `H12!B33` lo tiene en 0-1 y la capa API lo publica ×100.
_BASELINE_PCT = "27,4582"
_SUPERFICIES = ("quira_pages", "components", "views")


def _escenarios() -> list[tuple[str, float]]:
    """Los ICPI contrafactuales, leídos del documento derivado. No se escriben
    aquí: si un escenario cambia de valor, esta prueba lo persigue igual."""
    if not _DOC.exists():
        return []
    filas = re.findall(r"\|\s*`([A-DX]\d\w?)`\s*\|[^|]+\|\s*([\d.]+)\s*%",
                       _DOC.read_text(encoding="utf-8"))
    return [(cid, float(v)) for cid, v in filas]


# ═════════════════════════════════════════════════════════════════════════════
# EL LABORATORIO OBSERVA — NO TOCA
# ═════════════════════════════════════════════════════════════════════════════
def test_el_generador_no_escribe_en_el_gold_master():
    """Regla de Oro 1 y 4. Se mide la PROPIEDAD —que toda apertura sea de sólo
    lectura— y no la promesa escrita en el encabezado."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert fuente.count("load_workbook") == fuente.count("read_only=True"), (
        "hay una apertura del Gold Master que no es de sólo lectura")
    assert ".save(" not in fuente, "el laboratorio intenta escribir en el Excel"


def test_sin_gold_master_no_se_inventan_escenarios():
    """El tercer estado. Sin motor no hay contrafactuales: hay un 2. Una tabla
    de escenarios vacía parecería una auditoría sin hallazgos."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "GOLD_MASTER_RESUELTO" in fuente
    assert "return 2" in fuente, (
        "desapareció el código «no determinable»: sin él, no poder mirar se "
        "confundiría con haber mirado y no encontrar nada")


def test_el_laboratorio_reproduce_el_baseline_antes_de_mover_nada(gold_master):
    """La condición que hace interpretable todo lo demás.

    Si el laboratorio no reproduce `H12!B33` EXACTAMENTE, entonces los deltas de
    los escenarios miden la diferencia entre mi reimplementación y el motor —no
    el efecto de la decisión metodológica—, y cada conclusión de `007` sería un
    artefacto. Por eso el script se detiene con exit 1 en vez de seguir."""
    from scripts.gm_omega.sensibilidad_icpi import (_BASELINE, _K_ACTUAL,
                                                    _S_ACTUAL, evaluar,
                                                    leer_motor)
    d = leer_motor()
    assert d, "el Gold Master está presente pero `leer_motor` no devolvió nada"
    icpi = evaluar(d["metas"], _K_ACTUAL, _S_ACTUAL)["icpi"]
    assert abs(icpi - _BASELINE) < 1e-9, (
        f"el laboratorio da {icpi * 100:.6f} % y el motor {_BASELINE * 100:.6f} %. "
        f"Ningún escenario de 007 es interpretable hasta que esto cuadre")


def test_el_baseline_sigue_congelado_donde_dice_la_regla_000():
    """El número oficial no se mueve porque un contrafactual sea más favorable."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "_BASELINE = 0.27458226534062735" in fuente, (
        "cambió el baseline del laboratorio. La regla GM-Ω-ICPI-000 lo congela "
        "hasta el dictamen 011: si el motor cambió, eso es un hallazgo que se "
        "documenta, no una constante que se actualiza en silencio")
    assert _BASELINE_PCT in _DOC.read_text(encoding="utf-8")


# ═════════════════════════════════════════════════════════════════════════════
# LAS TRES ETIQUETAS Y LA FRONTERA DEL LABORATORIO
# ═════════════════════════════════════════════════════════════════════════════
def test_las_tres_etiquetas_estan_declaradas():
    """La regla que el colega impuso para todo 007. Sin ellas, un lector futuro
    no puede distinguir un contrafactual de una medición."""
    txt = _DOC.read_text(encoding="utf-8")
    for etiqueta in ("MATEMÁTICAMENTE REPRODUCIBLE",
                     "METODOLÓGICAMENTE CONTRAFACTUAL",
                     "NO AUTORIZADO PARA PUBLICACIÓN"):
        assert etiqueta in txt, f"desapareció la etiqueta «{etiqueta}»"


def test_ningun_contrafactual_se_filtro_a_las_superficies():
    """⚠️ EL CUSTODIO CENTRAL DE 007, y el que fija el patrón del «48,33 %».

    Ninguna cifra producida por un escenario puede aparecer en el producto. Se
    buscan los valores REALES leídos del documento —no una lista escrita a
    mano—, así que el día que un escenario cambie de valor, la prueba persigue
    el valor nuevo sin que nadie la actualice.

    Si esta prueba falla, la lectura NO es «hay que ajustar el test»: es que un
    número de laboratorio llegó a una superficie pública."""
    esc = _escenarios()
    if not esc:
        pytest.skip("aún no se generó el documento de 007 — nada que vigilar")

    archivos = [p for c in _SUPERFICIES if (RAIZ / c).exists()
                for p in (RAIZ / c).rglob("*.py") if "_deprecated" not in p.parts]
    assert archivos, "no se encontró ninguna superficie: la prueba no mira nada"

    # El baseline SÍ puede aparecer: es el número oficial.
    base = float(_BASELINE_PCT.replace(",", "."))
    fugas = []
    for cid, valor in esc:
        if abs(valor - base) < 0.001:
            continue
        for patron in (f"{valor:.4f}", f"{valor:.2f}"):
            for var in (patron, patron.replace(".", ",")):
                for py in archivos:
                    if var in py.read_text(encoding="utf-8", errors="replace"):
                        fugas.append(f"{cid}={var} en {py.relative_to(RAIZ)}")
    assert not fugas, (
        "un contrafactual de 007 aparece en una superficie del producto:\n  "
        + "\n  ".join(sorted(set(fugas)))
        + "\n\nEstos números son METODOLÓGICAMENTE CONTRAFACTUALES y NO ESTÁN "
          "AUTORIZADOS PARA PUBLICACIÓN. El único ICPI publicable es "
          f"{_BASELINE_PCT} % hasta que GM-Ω-ICPI-011 dictamine.")


# ═════════════════════════════════════════════════════════════════════════════
# DOC-009 · E_i NO ENTRA
# ═════════════════════════════════════════════════════════════════════════════
def test_ningun_escenario_de_007_manipula_E_i():
    """DOC-009 aplicado a la propia auditoría.

    `E_i` tiene su regla generadora `NOT_DETERMINABLE` (`007-B0`): los valores
    nacieron con la primera versión conservada del motor y nunca cambiaron,
    mientras la tesis —anterior a todas— describe otra regla. Construir un
    escenario «E_i corregido» exigiría decidir cuál es la regla correcta, y esa
    decisión sólo puede salir de una fuente, nunca del efecto que produce.

    ⚠️ SE MIDE LO QUE SE PUEDE MEDIR, no más: que ningún escenario declarado
    sustituya `E`, y que el documento conserve la declaración de por qué. Esto
    NO demuestra que `E_i` sea correcto —no lo es ni deja de serlo aquí—:
    demuestra que 007 no lo tocó."""
    fuente = _SCRIPT.read_text(encoding="utf-8")

    # La propiedad, nítida y falsable: `E` se ASIGNA una sola vez en todo el
    # script —cuando `leer_motor` lo lee del Gold Master— y en ningún otro sitio.
    # Cualquier escenario que quisiera sustituirlo tendría que asignarlo.
    #
    # ⚠️ La primera versión de esta prueba troceaba el código con una expresión
    # regular y sólo alcanzaba 10 de los 16 escenarios: habría dado verde con un
    # `E_i` manipulado en los otros seis. Medir una propiedad del archivo entero
    # no deja ese hueco.
    asignaciones = re.findall(r'"E"\s*:', fuente)
    assert len(asignaciones) == 1, (
        f'`E` se asigna {len(asignaciones)} veces y debe asignarse UNA —la '
        f'lectura del motor en `leer_motor`—. Si un escenario lo sustituye, '
        f'estaría decidiendo cuál es la regla de E_i, y esa decisión sólo puede '
        f'salir de una fuente: nunca del efecto que produce')
    assert re.search(r'"E":\s*h12v\.cell', fuente), (
        "la única asignación de E ya no es la lectura directa del Gold Master")

    txt = _DOC.read_text(encoding="utf-8")
    assert "NOT_DETERMINABLE" in txt and "DOC-009" in txt, (
        "el documento dejó de declarar por qué E_i queda fuera. Sin esa "
        "constancia, su ausencia se lee como olvido y no como decisión")


def test_la_regla_anterior_de_V_no_se_da_por_reconstruida():
    """DOC-009 aplicado a `V`, que es donde estuvo la tentación real.

    `H13!B21` conserva un fragmento de la regla anterior —«SI(suma≥2,0.5)»— y es
    tentador tratarlo como la regla. No lo es: no dice qué producía con los
    cuatro verificadores en 1, y las dos lecturas posibles difieren en más de
    diez puntos y en DOS categorías AVEP. El documento debe conservar ambas y
    declarar la forma exacta como no determinable."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "`B2a`" in txt and "`B2b`" in txt, (
        "desapareció una de las dos lecturas de la regla anterior de V. "
        "Quedarse con una sola convertiría una reconstrucción en un hecho")
    bloque = txt.split("## 007-B")[1].split("## 007-C")[0]
    assert "NOT_DETERMINABLE" in bloque, (
        "la forma exacta de la regla anterior de V dejó de declararse no "
        "determinable")


def test_la_coherencia_de_V_se_verifica_contra_la_regla_no_se_afirma():
    """La contrapartida positiva: `V` sí es reconstruible, y eso también hay que
    demostrarlo en vez de afirmarlo. El escenario `B1` aplica la regla
    documentada a los cuatro verificadores; si coincide con `B0`, los valores
    implementados la obedecen.

    ⚠️ Que `E_i` esté sin biografía no autoriza a sospechar del resto del motor:
    la mayoría de sus variables documenta sus cambios, y decirlo es tan parte de
    la auditoría como señalar la que no."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "H13!B16-B20" in txt or "H13!B20" in txt, (
        "el documento dejó de citar dónde vive la regla de V")
    m = re.search(r"De las \*\*(\d+) metas comparables\*\*, \*\*(\d+) coinciden",
                  txt)
    assert m, "desapareció la comprobación de coherencia regla↔valor de V"
    comparables, coinciden = int(m.group(1)), int(m.group(2))
    assert comparables == 25, (
        f"sólo {comparables} de 25 metas se pudieron contrastar contra la regla "
        f"de V: si bajó, algo dejó de leerse en H13 y el resto del bloque B "
        f"mide menos de lo que dice medir")
    assert coinciden == comparables, (
        f"{comparables - coinciden} metas tienen un V_i que la regla documentada "
        f"no produce. Si esto salta, V acaba de perder la biografía que lo "
        f"distinguía de E_i, y hay que auditarlo como se auditó aquél")


def test_la_robustez_de_categoria_declara_de_donde_salen_sus_umbrales():
    """007-X mide si la CATEGORÍA aguanta los contrafactuales. Esa medición tiene
    un supuesto: que los umbrales `0,9 / 0,7 / 0,4 / 0,2` significan algo.

    Javo aportó el contexto —la escala AVEP es invención de Dylus Lab, ajustada
    después a la normativa— y auditarla dio esto: la norma sostiene el
    CONSTRUCTO (`COPFP Art. 41`) pero **no los CORTES**, que son una decisión
    metodológica propia. Es legítimo —los umbrales de un índice compuesto casi
    nunca salen de una norma— y por eso mismo debe estar **declarado**: hoy la
    escala se presenta con la autoridad de un umbral legal, y de ella depende la
    emisión de un Certificado (`H01!C59`, AVEP ≥ 70 %).

    ⚠️ SE VERIFICA QUE EL SUPUESTO ESTÉ DICHO, no que la escala sea correcta.
    Una medición de robustez que no declara contra qué mide la robustez afirma
    de más."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "007-X-bis" in txt, (
        "desapareció la auditoría de procedencia de la escala AVEP: sin ella, "
        "007-X mide la estabilidad de una categoría cuyos cortes nadie justificó")
    bloque = txt.split("007-X-bis")[1].split("## Concentración")[0]
    assert "CONSTRUCTO" in bloque and "CORTES" in bloque, (
        "se perdió la distinción entre lo que la norma sí sostiene (por qué "
        "medir congruencia) y lo que no (dónde cortar en 70 o en 40)")
    assert "dice que la escala esté mal" in bloque.lower(), (
        "desapareció la salvedad. Sin ella, «los cortes no tienen norma» se lee "
        "como «los cortes están mal», y son cosas distintas")


def test_las_escalas_AVEP_de_QUIRA_no_divergen_en_silencio():
    """⚠️ ATAQUE DE D-012 · dos baremos incompatibles, y nadie declaraba cuál rige.

        canon 07_AVEP_LENGUAJE.md   4 niveles · 75/60/50 · ICPI + SAT + Ti
        config.AVEP + Gold Master   5 niveles · 90/70/40/20 · sólo ICPI

    Para 27,4582 % el motor dice «Gestión por Ocurrencia» y el canon dice «Nivel
    de Atención Alta». No divergió una cifra: divergió **el significado de la
    cifra**, que es el patrón del «48,33 %» un piso más arriba.

    ⚠️ SE MIDE LA DIVERGENCIA, NO SE JUZGA CUÁL ES CORRECTA — eso es de `011`.
    Mientras la deuda siga abierta esta prueba verifica que el defecto está donde
    decimos; el día que se unifiquen, saltará y se cierra D-012."""
    from scripts.gm_omega.sensibilidad_icpi import escalas_avep
    e = escalas_avep()
    if len(e["fuentes"]) < 2:
        pytest.skip("no se pudieron leer las dos fuentes de la escala")
    assert e["coinciden"] is False, (
        "las escalas AVEP del canon y del motor ya coinciden: si alguien las "
        "unificó, hay que CERRAR D-012 declarando cuál rige y con qué "
        "procedencia, e invertir esta prueba para que vigile que no vuelvan a "
        "separarse")


def test_ninguna_escala_ajena_se_adopta_por_compartir_la_unidad():
    """DOC-012 · un porcentaje no tiene significado semántico por sí mismo.

    Existe una escala obligatoria de desempeño público (LOSEP · Ministerio del
    Trabajo: 95/90/80/70) y está a mano. Adoptarla para el ICPI sería confundir
    dos constructos porque ambos producen porcentajes: mide **talento humano**,
    no congruencia programática e intersistémica.

    Y el diseño original YA tenía la distinción resuelta — el módulo `F-EDS`
    traducía el índice a insumos LOSEP como **puente explícito hacia otro
    constructo**. Perderla sería deshacer trabajo bien hecho.

    ⚠️ SE VERIFICA QUE LA DISTINCIÓN SIGA ESCRITA y que los umbrales de la LOSEP
    NO estén en la escala del motor. No prohíbe contrastar: contrastar no es
    adoptar."""
    from scripts.gm_omega.sensibilidad_icpi import escalas_avep
    motor = dict(escalas_avep()["fuentes"]).get("config.AVEP", [])
    umbrales = {round(u, 2) for u, _ in motor}
    losep = {0.95, 0.90, 0.80, 0.70}
    assert not losep.issubset(umbrales), (
        "la escala del motor adoptó los cortes de la LOSEP (95/90/80/70). Esa "
        "escala mide desempeño del talento humano, no congruencia programática: "
        "compartir la unidad no hace equivalentes los constructos")

    txt = _DOC.read_text(encoding="utf-8")
    assert "F-EDS" in txt, (
        "desapareció la constancia de que el diseño original ya separaba ambos "
        "constructos con un módulo puente. Sin ella, adoptar la escala LOSEP "
        "parecería una simplificación razonable en vez de una regresión")


def test_V_y_E_no_comparten_la_naturaleza_de_su_vacio():
    """DOC-011 · el resultado que más lejos llega de todo 007, y no es un número.

    `V` y `E` están ambas incompletas y **no tienen el mismo problema**:

        V   regla vigente + regla histórica + motivo del cambio +
            25 de 25 valores reproducibles     → LÍMITE DE RECONSTRUCCIÓN
        E   valores, y ninguna regla que los produzca
                                               → AUSENCIA DE REGLA GENERADORA

    El primero es una situación sana para una auditoría: se puede decir con
    precisión qué se sabe, qué no y por qué. El segundo no admite esa frase.

    ⚠️ SE VERIFICA QUE LA DISTINCIÓN SIGA DECLARADA, no que sea correcta —eso lo
    juzga 011—. Colapsarla llevaría a uno de dos errores simétricos: sospechar
    de todo el motor por lo que falla en una variable, o dar por buena una
    ausencia porque las demás sí documentan."""
    txt = _DOC.read_text(encoding="utf-8")
    bloque = txt.split("## 007-B")[1].split("## 007-C")[0]
    for marca in ("límite de reconstrucción", "ausencia de regla generadora"):
        assert marca in bloque.lower(), (
            f"desapareció «{marca}» del contraste V↔E. Sin los dos nombres, los "
            f"dos vacíos vuelven a leerse como el mismo problema")
    assert "25 de 25" in bloque, (
        "desapareció la contrapartida positiva: que V sí reproduce su regla en "
        "las 25 metas es la mitad que sostiene la distinción")


def test_el_vocabulario_publicado_del_ICPI_corresponde_al_motor():
    """⚠️ ATAQUE DE D-011 · fija el estado, no lo aprueba.

    El snapshot que consume la UI describe el ICPI con palabras que el motor no
    sostiene. Mientras la deuda siga abierta, esta prueba **verifica que el
    defecto está donde decimos** —si se moviera sin que nadie lo registre,
    saltaría—; el día que se cure, saltará también, y entonces se cierra D-011 y
    esta prueba se invierte.

    Es el patrón del «48,33 %» en la cifra madre: no una cifra equivocada, sino
    una NARRATIVA sobre la cifra que se soltó de su fuente."""
    import json
    snap = RAIZ / "data" / "gm_snapshot.json"
    if not snap.exists():
        pytest.skip("no hay snapshot publicado en el repositorio")
    icpi = json.loads(snap.read_text(encoding="utf-8")).get("icpi", {})

    clasif = str(icpi.get("clasificacion", ""))
    jerga = [t for t in ("umbral anual", "Corte parcial", "lectura preliminar")
             if t in clasif]
    nombre_ajeno = "Compuesto de Progreso Institucional" in json.dumps(
        icpi, ensure_ascii=False)

    assert jerga or nombre_ajeno, (
        "D-011 ya no se reproduce: el snapshot dejó de publicar la frase interna "
        "de `H12!B34` y/o el nombre que la tesis no respalda. Si alguien lo "
        "curó, hay que CERRAR D-011 en `app/agents/deuda.py` y convertir esta "
        "prueba en su contraria —que la clasificación publicada sea una "
        "categoría de gobernanza, o diga en lenguaje público que aún no la hay—")


def test_la_jerarquia_de_sensibilidad_esta_declarada():
    """El resultado central de 007, y el que reordena 011: el ICPI es robusto a
    baja sensibilidad a las ponderaciones ENSAYADAS y alta a la arquitectura de
    agregación. Si el documento deja de decirlo, `011` se sentaría a discutir los
    ponderadores —que casi no mueven el índice— creyendo que discute lo
    importante.

    ⚠️ Y se vigila la FORMULACIÓN, no sólo el orden. La primera versión decía que
    el índice era «frágil a su forma matemática», y eso contrabandeaba un juicio:
    sugería que multiplicar es un defecto. `007-D` no demuestra que multiplicar
    esté mal — demuestra que multiplicar es **determinante**. Sólo la segunda
    afirmación está medida, y la palabra «ensayadas» acota el alcance a las
    cuatro alternativas que se probaron."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "## La jerarquía de sensibilidad" in txt
    assert "ENSAYADAS" in txt, (
        "la conclusión perdió el acotamiento: se probaron cuatro alternativas de "
        "peso, no todas las posibles, y afirmar sin ese límite es afirmar de más")
    assert "no demuestra que multiplicar" in txt.lower() or (
        "**no demuestra que multiplicar esté mal**" in txt), (
        "desapareció la salvedad de que 007-D mide determinación, no defecto")
    orden = [f for f in ("007-D", "007-B", "007-A", "007-C")
             if f"`{f}`" in txt.split("## La jerarquía")[1].split("## 007-X")[0]]
    assert orden[0] == "007-D", (
        f"la familia más sensible pasó a ser {orden[0]} y era 007-D (la "
        f"estructura algebraica). Es un cambio de conclusión, no de formato: "
        f"hay que releer el dictamen antes de aceptarlo")
