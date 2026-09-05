# -*- coding: utf-8 -*-
"""
tests/test_carta_rearquitectura.py — QUIRA-NEXT · el plan del refactor integral
════════════════════════════════════════════════════════════════════════════════
Javo pidió un refactor **integral de fondo y forma de todo el ecosistema**, y
antes de cualquier ejecución pidió lo correcto:

    «esto merece una planificación integral para hacerlo bien,
     sin dañar lo que es válido»

⚠️ Y LA PRUEBA DE QUE HACÍA FALTA LA DIO ESTA DIRECCIÓN EN EL ACTO. Ante el
ejemplo «quitar la palabra auditoría de la documentación», empezó a ejecutarlo
en vez de leerlo como una muestra del NIVEL del refactor. Medido antes de
parar: **609 ocurrencias en 233 archivos**, y no son la misma palabra —
`auditoría CGE` es norma citada, `auditoría` como nombre de GM-Ω sí cambia,
`auditable` es la propiedad que QUIRA certifica. Un reemplazo sin clasificar
habría borrado artículos de ley.

Estas pruebas vigilan que el plan conserve lo que lo hace utilizable:
las cinco categorías, la separación entre lo que se acata y lo que se decide,
el inventario contado y no estimado, y que el nombre vaya al final.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_CARTA = RAIZ / "docs" / "architecture" / "QUIRA-NEXT_CARTA_REARQUITECTURA.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "carta_rearquitectura.py"


def test_la_carta_planifica_pero_no_ejecuta():
    """El límite que la hace segura. Un plan que además empieza a ejecutar es
    lo que Javo tuvo que detener, y el Gold Master sigue congelado hasta
    `011-C4`: ampliar QUÉ se puede decidir no adelanta CUÁNDO se interviene."""
    assert _SCRIPT.exists(), "desapareció el generador de la carta"
    txt = _CARTA.read_text(encoding="utf-8")
    assert "No ejecuta nada" in txt, (
        "la carta dejó de declarar que no ejecuta. Sin esa línea se convierte "
        "en una orden de trabajo sobre 1300 artefactos")
    assert "no adelanta" in txt and "27,4582 %" in txt, (
        "se perdió que planificar el refactor no descongela el motor")


def test_las_cinco_categorias_son_la_regla_que_protege_lo_valido():
    """★ El núcleo de la carta.

        🏛️ HISTÓRICO                 se preserva como trazabilidad
        ⚖️ NORMATIVO VIGENTE          se acata mientras siga vigente
        🔬 EMPÍRICAMENTE ÚTIL         se conserva si supera validación
        🔧 DECISIÓN DE DISEÑO ANTIGUA queda abierta a rediseño
        📜 SUPERADO METODOLÓGICAMENTE antecedente, no regla

    ⚠️ NINGUNA PIEZA SE TOCA ANTES DE CLASIFICARLA. Es lo único que hace
    compatible «refactor integral» con «sin dañar lo que es válido» — y el
    caso `auditoría` demuestra que sin la regla se rompe en el primer minuto."""
    txt = _CARTA.read_text(encoding="utf-8")
    for cat in ("HISTÓRICO", "NORMATIVO VIGENTE", "EMPÍRICAMENTE ÚTIL",
                "DECISIÓN DE DISEÑO ANTIGUA", "SUPERADO METODOLÓGICAMENTE"):
        assert cat in txt, (
            f"desapareció la categoría `{cat}`. Las cinco son necesarias: con "
            f"cuatro, alguna pieza queda sin sitio y se decide por defecto")
    assert "Ninguna pieza del ecosistema se toca antes de clasificarla" in txt


def test_la_carta_separa_lo_que_se_acata_de_lo_que_se_decide():
    """★ `DOC-027` y `DOC-028` · la distinción que evita los dos extremos.

    Un refactor puede fallar en dos direcciones opuestas, y las dos son malas:

        congelar por costumbre lo que se puede mejorar
        rediseñar por gusto lo que la norma fija

    `R_i`↔COOTAD, `V_i`↔LOTAIP, `T_i`↔COPFP/Acuerdo 067 y `P_i`↔COPFP 54 **no
    son herencia**: son obligación vigente. Los pesos, el piso, la residencia
    de los índices y los nombres **sí** son diseño.

    ⚠️ Y LA CORRECCIÓN QUE COSTÓ UNA VUELTA: la primera redacción de `DOC-027`
    decía «donde no hay razón documentada no hay nada que respetar». Convertía
    un sesgo conservador en uno destructivo. Sin justificación, una decisión
    antigua no es automáticamente incorrecta NI correcta: queda ABIERTA."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "no adquiere autoridad metodológica por antigüedad" in txt, (
        "se perdió la formulación rigurosa de DOC-027. La versión anterior "
        "—«no hay nada que respetar»— autorizaba a barrer lo que no estuviera "
        "justificado, que es el extremo opuesto del problema que corrige")
    assert "Tampoco automáticamente correcta" in txt, (
        "desapareció el tercer estado. Una decisión sin justificación no es "
        "válida ni inválida: está abierta, y eso es distinto de ambas")
    for anclaje in ("COOTAD", "LOTAIP", "Acuerdo 067"):
        assert anclaje in txt, (
            f"desapareció el anclaje normativo `{anclaje}`. Sin la lista, el "
            f"refactor no sabe qué NO puede tocar por criterio propio")
    assert "Continuidad histórica ≠ continuidad metodológica" in txt, (
        "se perdió DOC-028. Sin ella, conservar la trazabilidad y rediseñar "
        "parecen incompatibles, y hay que elegir — y no hay que elegir")


def test_el_inventario_se_cuenta_y_no_se_estima():
    """Un plan que no sabe su tamaño no es un plan.

    ⚠️ Y AQUÍ LA CARTA COMETIÓ EL ERROR QUE VIENE A CORREGIR: su primera
    versión sumó `ADR` y `PCD` —que viven dentro de `docs/`— contándolos dos
    veces, y dejó fuera las pruebas por el error opuesto. Publicó un total
    inflado en el documento cuyo objeto es no falsear datos.

    Esta prueba vigila que el inventario siga derivándose del repositorio y
    que la constancia del error no se limpie."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "rglob" in fuente, (
        "el inventario dejó de contarse del repositorio. Un tamaño escrito a "
        "mano se desactualiza en semanas y nadie se entera")
    txt = _CARTA.read_text(encoding="utf-8")
    assert "no suman" in txt, (
        "desapareció la marca de las filas contenidas en otras. Sin ella "
        "vuelve el doble conteo")
    assert "cometido en el documento que lo planifica" in txt, (
        "se limpió la constancia del error de suma. Conservarla es lo que "
        "hace creíble al resto de la carta")


def test_el_nombre_va_al_final_de_la_secuencia():
    """Javo planteó renombrar el `ICPI`. La secuencia correcta no empieza ahí:

        fenómeno → unidad → arquitectura → residencia → …y luego el nombre

    ⚠️ Empezar por el nombre sería hacer branding de un concepto que todavía
    se está rediseñando. Y los cuatro destinos del ICPI —conservar,
    refactorizar, descomponer, deprecar— siguen abiertos: cerrarlos aquí sería
    que el plan del refactor dictamine lo que `011-C4` debe decidir."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "branding de un concepto que" in txt, (
        "se perdió la razón por la que el nombre va al final")
    for destino in ("se **conserva**", "se **refactoriza**",
                    "se **descompone**", "se **depreca**"):
        assert destino in txt, (
            f"desapareció el destino «{destino}» del ICPI. Con menos de "
            f"cuatro, el dictamen de C4 se lee como binario y no lo es")
    assert "Ninguno de los cuatro es un fracaso" in txt, (
        "desapareció la línea que permite considerar la deprecación sin que "
        "parezca una derrota. Si deprecar se lee como fracaso, C4 queda "
        "sesgado a conservar")


def test_fondo_y_forma_explica_donde_vive_lo_transversal():
    """★ El cambio conceptual mayor, de una expresión de Javo.

        FONDO   ¿QUÉ gestiona el GAD?   dominios sectoriales
        FORMA   ¿CÓMO lo gestiona?      capacidades transversales

    El caso que lo prueba es el `IED`: **ya existe** —desglosa metas del PDOT
    por dirección del Estatuto Orgánico— y su dominio, su rol y su pregunta
    están los tres `POR_DECLARAR`. En el esquema se ve por qué: «¿qué tan
    eficientemente funciona la dirección responsable?» aplica a Salud, a Obras
    Públicas y a Financiera por igual. Es **forma**, y hoy no hay dónde
    ponerla."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "FONDO" in txt and "FORMA" in txt
    assert "`IED`" in txt and "POR_DECLARAR" in txt, (
        "desapareció el caso que hace concreto el esquema. Sin un ejemplo "
        "medido, FONDO/FORMA es una figura bonita sin consecuencia")
    assert "no pertenece a ningún dominio sectorial" in txt, (
        "se perdió la conclusión operativa: hay indicadores transversales "
        "viviendo dentro de dominios sectoriales porque no existe el otro eje")
