# -*- coding: utf-8 -*-
"""
tests/test_rearq_matriz_ontologica.py — REARQ · `Q-M0`
════════════════════════════════════════════════════════════════════════════════
El primer artefacto de la Rearquitectura. **No es una fórmula nueva**: es una
ficha por indicador con veinte campos, y su función es obligar a separar lo que
un indicador CALCULA de lo que se AFIRMA con él.

★ EL HALLAZGO ES EL PORCENTAJE

    240 celdas · 70 declaradas (29 %) · 170 POR DECLARAR (71 %)

No es una matriz incompleta: es una matriz **honesta**. Rellenar de memoria
produciría un documento completo y falso — el defecto que `GM-Ω` pasó toda la
investigación desmontando.

★ Y LA COLUMNA 19 ES LA QUE MÁS OBLIGA

    ¿qué afirmación NO permite hacer este indicador?

Existe porque el caso ya ocurrió: el ICPI mide congruencia acreditada de 25
metas al corte de abril, y la capa de publicación lo describe como que «mide
velocidad de ejecución» (`D-011`).

⚠️ NO EMPIEZA POR EL ICPI, y es deliberado: entra como uno más, en orden
alfabético, para no diseñar la arquitectura nueva alrededor de su forma
histórica.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "REARQ_Q-M0_MATRIZ_ONTOLOGICA.md"
_SCRIPT = RAIZ / "scripts" / "rearq" / "matriz_ontologica.py"


def test_la_matriz_no_toca_nada():
    """`Q-M0` es diseño conceptual. La Rearquitectura está autorizada
    **exclusivamente** para eso: no decide destinos, los registra."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "Q-M0 intenta escribir en el Gold Master"
    txt = _DOC.read_text(encoding="utf-8")
    assert "exclusivamente para diseño conceptual" in txt, (
        "desapareció el límite de autorización de la Rearquitectura")
    assert "no decide destinos" in txt.lower(), (
        "el campo 20 dejó de declararse evaluación inicial. Un destino "
        "registrado que se lea como decidido cierra por omisión lo que "
        "`Q-M1` debe abrir")


def test_el_ICPI_entra_como_uno_mas():
    """★ La disciplina que evita rediseñar alrededor de lo conocido.

    El ICPI es el indicador más trabajado, y por eso mismo **no puede abrir la
    matriz**: si la arquitectura nueva se piensa desde su forma, heredará su
    forma. Entra en orden alfabético, tercero, entre `ICODS` e `IED`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "No empieza por el ICPI, y es deliberado" in txt, (
        "se perdió la razón del orden. Sin ella, el próximo que edite la "
        "matriz pondrá el ICPI primero «porque es el importante»")
    fichas = re.findall(r"^### `([A-Z]{3,5})`$", txt, re.M)
    assert fichas, "no se encontraron fichas en la matriz"
    assert fichas == sorted(fichas), (
        f"las fichas dejaron de ir en orden alfabético: {fichas[:4]}…")
    assert fichas[0] != "ICPI", (
        "el ICPI volvió a abrir la matriz. El orden alfabético es lo que lo "
        "mantiene como un indicador entre los demás")


def test_lo_no_establecido_se_cuenta_y_no_se_rellena():
    """★ El hallazgo de `Q-M0`.

    170 de 240 celdas están `POR DECLARAR`, y **contarlas es más útil que
    rellenarlas de memoria**. Una matriz completa y falsa sería exactamente el
    defecto que esta matriz existe para evitar.

    ⚠️ Si un día el porcentaje baja, tiene que ser porque alguien declaró esas
    celdas con su fuente — no porque el generador dejó de contarlas."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "POR DECLARAR" in txt
    # ⚠️ Y el matiz que la corrección de Javo obligó a añadir: el vacío es
    # hallazgo SÓLO después de haber leído el instrumento. Antes de eso era
    # simplemente no haber mirado.
    assert "el porcentaje que queda **sí** es el hallazgo" in txt, (
        "la matriz dejó de declarar que su vacío es el resultado. Sin esa "
        "línea, un 62 % en blanco se lee como trabajo a medias")
    assert "después de leer el instrumento" in txt, (
        "se perdió la condición que hace válido el hallazgo: sólo cuenta como "
        "vacío lo que sigue vacío DESPUÉS de leer el Gold Master")
    assert "de memoria produciría un documento completo y falso" in txt
    # El recuento debe seguir derivándose, no escribirse a mano.
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "sum(len(f) for f in _FICHAS.values())" in fuente, (
        "el recuento de celdas declaradas dejó de derivarse de las fichas")


def test_el_campo_19_existe_y_declara_por_que():
    """★★ La columna que impide que la presentación infle la medición.

        dato → evidencia → inferencia → afirmación

    No son sinónimos — es lo que `D2` dejó demostrado. Y el campo existe
    porque el caso **ya ocurrió**: `data/gm_snapshot.json` describe el ICPI
    como que «mide velocidad de ejecución», y el motor no mide eso (`D-011`).

    ⚠️ El dato incómodo que la matriz publica: la mayoría de los indicadores
    **no tiene declarado qué NO permite afirmar**. Ése es el hueco por donde
    una medición limitada se convierte en un titular."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Qué afirmación NO PERMITE hacer" in txt, (
        "desapareció el campo 19, que es el mecanismo central de Q-M0")
    assert "dato  →  evidencia  →  inferencia  →  afirmación" in txt, (
        "se perdió la cadena que hace legible el campo 19")
    assert "El campo 19 existe porque eso ya pasó" in txt, (
        "desapareció el caso que lo justifica. Una regla sin su incidente se "
        "borra en la siguiente limpieza")
    assert "no tienen declarado qué afirmación NO permiten hacer" in txt, (
        "la matriz dejó de contar cuántos indicadores carecen del campo 19")


def test_los_hallazgos_estructurales_no_se_pierden():
    """Lo que la matriz deja ver de un vistazo, y que ninguna ficha suelta
    mostraría:

        IFE / IEF   dos siglas casi idénticas para materia contigua
        IED         no pertenece a ningún dominio sectorial — prueba el eje FORMA
        IBSC        hereda ENTERA la multiplicatividad del ICPI
        TGI         evalúa al evaluador; H95 dice que no está verificado fuera
        IPE         el más maduro — el patrón a replicar

    ⚠️ Y el patrón de fondo: los indicadores con pregunta declarada son los
    que pasaron por curación de dominio. **La matriz no descubre indicadores
    malos: descubre indicadores no curados.**"""
    txt = _DOC.read_text(encoding="utf-8")
    for clave in ("no son duplicados", "no pertenece a ningún dominio "
                  "sectorial", "hereda entera la multiplicatividad",
                  "evalúa al evaluador", "el más maduro"):
        assert clave.lower() in txt.lower(), (
            f"se perdió el hallazgo «{clave}». Son los que justifican que la "
            f"matriz exista como vista de conjunto y no como fichas sueltas")
    assert "descubre indicadores no curados" in txt, (
        "desapareció el patrón de fondo. Sin él, las celdas vacías parecen "
        "descuido y son la huella de qué dominios no se curaron")


def test_la_matriz_lee_el_instrumento_antes_de_declarar_vacio():
    """★★ La corrección que Javo hizo en una línea: *«pero todos están en el
    Excel canónico»*.

    La `v1` publicó **71 % `POR DECLARAR`** sin haber abierto las hojas de los
    índices. Cada una trae su título completo, una descripción con su fuente y,
    en varios casos, la fórmula escrita en texto.

    ⚠️ ES EL MISMO PATRÓN QUE ESTA INVESTIGACIÓN CAZÓ TRES VECES EN OTROS
    —`E_i` declarado `UNTRACEABLE` cuando la tesis lo definía, «no existe
    artefacto índice→dominio» cuando la Constitución lo declaraba, `011-C3`
    cerrando `NO DETERMINABLE` lo que 83 versiones podían fechar— y esta vez
    lo cometió quien lo venía señalando.

        El tercer estado obliga en las dos direcciones: «no pude obtener» no
        es «no existe», y **no haber mirado no autoriza a declarar vacío**."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "def leer_hojas_indice" in fuente, (
        "la matriz dejó de leer las hojas de los índices. Sin eso vuelve a "
        "declarar POR DECLARAR lo que el instrumento ya dice")
    txt = _DOC.read_text(encoding="utf-8")
    assert "Pero todos están en el Excel canónico" in txt, (
        "se perdió la corrección de Javo. Conservarla es lo que explica por "
        "qué el generador lee las hojas")
    assert "no haber mirado no autoriza a declarar vacío" in txt, (
        "desapareció la formulación de la lección. El tercer estado obliga en "
        "las dos direcciones")
    assert "derivadas del Gold Master" in txt, (
        "el recuento dejó de separar lo declarado por GM-Ω de lo derivado del "
        "instrumento. Mezclarlos oculta cuánto aporta cada fuente")


def test_el_caso_IFE_queda_como_hallazgo_falso_corregido():
    """★ El caso concreto que prueba la corrección.

    La `v1` anunció que `IFE` e `IEF` eran «materia contigua» con riesgo de
    duplicación. **Falso**: `IFE` es Fidelidad Electoral (`H03_S1_ELECTORAL_
    CNE`) e `IEF` es Eficiencia Financiera (`H20c`). No tienen relación.

    El parecido de las siglas produjo un hallazgo inventado, y sólo abrir la
    hoja lo desmintió.

    ⚠️ Y el hallazgo REAL es otro: si esta dirección las confundió teniendo el
    Excel delante, cualquier lector puede hacerlo. Eso va a `T6` como caso de
    nombres que no distinguen."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Índice de Fidelidad Electoral" in txt, (
        "se perdió qué es realmente IFE. Sin ese dato vuelve la falsa "
        "duplicación con IEF")
    assert "El riesgo real no era la duplicación: es la confusión" in txt, (
        "desapareció el hallazgo verdadero. Corregir un error sin quedarse "
        "con lo que sí enseñó desperdicia el error")
    assert "cómo se fabricó un hallazgo falso" in txt, (
        "se limpió la constancia. Un expediente que borra sus errores deja de "
        "ser auditable — y este audita, entre otras cosas, a quien lo escribe")


def test_el_orden_de_los_campos_es_el_metodo():
    """Primero el fenómeno, al final la fórmula.

    Invertirlo sería empezar por la matemática — el hábito que `GM-Ω` vino a
    corregir y que `011-C4` dejó como orden de trabajo:

        FENÓMENO → EVIDENCIA → INFERENCIA → MODELO → FÓRMULA → …"""
    from scripts.rearq.matriz_ontologica import _CAMPOS

    nombres = [n for _num, n in _CAMPOS]
    i_fenomeno = next(i for i, n in enumerate(nombres) if "Fenómeno" in n)
    i_formula = next(i for i, n in enumerate(nombres) if "Fórmula" in n)
    assert i_fenomeno < i_formula, (
        "la fórmula adelantó al fenómeno en el orden de campos. El orden es "
        "el método: preguntar por la matemática antes que por el objeto es "
        "lo que produjo cinco decisiones sin declarar")
    txt = _DOC.read_text(encoding="utf-8")
    assert "El orden de los campos es el método" in txt
