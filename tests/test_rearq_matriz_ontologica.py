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
    # ⚠️ Y la conclusión se enuncia con cuidado: «no descubre indicadores
    # malos, descubre no curados» presuponía que ninguno tiene problemas
    # metodológicos — y `011-C4` demostró que algunos sí.
    assert "no presume que un indicador sea bueno o malo" in txt, (
        "desapareció el patrón de fondo, o volvió en su forma excesiva. La "
        "matriz identifica el estado de curación y evidencia disponible para "
        "evaluar; no absuelve por adelantado")


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


def test_IBSC_distingue_dependencia_de_forma_compartida():
    """★ El hallazgo que hubo que **demostrar** antes de afirmarlo.

    La `v1` dijo que `IBSC` «hereda entera la multiplicatividad del ICPI» y
    que «si `D1` se rediseña, `IBSC` cambia». El colega exigió demostrar la
    dependencia causal, y al verificarla resultó **falsa en una mitad y real
    en la otra**:

        154 fórmulas en H12b_MOTOR_IBSC · referencias a H12_MOTOR: NINGUNA
        → H14_PONDERADORES ×50 · H04b_DIAGNÓSTICO_SOCIAL ×25

    Es decir: **comparte insumos** (`P_i`/`R_i` de `H14`) — dependencia real
    de datos — y **comparte forma algebraica** — coincidencia de diseño, no
    herencia.

    ⚠️ La consecuencia precisa es la contraria a la que se había escrito: si
    `D1` se rediseña, `IBSC` **no cambia solo**. Si cambian los ponderadores
    de `H14`, **sí**. Confundir ambas cosas habría hecho que un rediseño del
    ICPI arrastrara a `IBSC` sin que nadie lo notara — o que no lo arrastrara
    creyendo que sí."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no referencian `H12` ni una sola vez" in txt, (
        "se perdió la evidencia. Sin ella vuelve la afirmación de herencia, "
        "que es falsa")
    assert "coincidencia" in txt and "no herencia" in txt, (
        "desapareció la distinción entre dependencia de datos y forma "
        "compartida — que es exactamente lo que el colega pidió demostrar")
    assert "no cambia solo" in txt, (
        "se perdió la consecuencia precisa del acoplamiento asimétrico")


def test_los_hallazgos_se_clasifican_en_tres_categorias():
    """★ Sin esta separación, `Q-M0` convertiría todo hallazgo en
    «refactorizar» — y la mayoría no lo son:

        A  problema del INSTRUMENTO   la fórmula existe, el fenómeno no
        B  problema de ARQUITECTURA   el indicador está bien; falta su sitio
        C  problema de PRESENTACIÓN   ni matemático ni conceptual: nombres

    ⚠️ Un hallazgo `B` **no dice que el indicador esté mal**: dice que la
    ontología heredada no tiene todavía el lugar que le corresponde. Y uno `C`
    no exige tocar una sola fórmula."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Tres categorías de hallazgo" in txt, (
        "desapareció la clasificación. Sin ella, «IED no tiene dominio» se "
        "lee como «IED está mal»")
    for cat in ("problema del instrumento", "problema de arquitectura",
                "problema de presentación"):
        assert cat in txt, f"falta la categoría «{cat}»"
    assert "no dice que el indicador esté mal" in txt


def test_las_cinco_reglas_se_congelan_antes_de_Q_M1():
    """Las reglas que impiden que `Q-M1` herede los errores de `Q-M0`.

        1  no inferir ontología por nombre          IFE ≠ IEF
        2  no inferir ausencia por no haber mirado  71 % → 62 %
        3  no confundir dependencia con forma       IBSC no referencia H12
        4  existir no justifica ser necesario       Q-M1 parte de preguntas
        5  cada indicador necesita CONTRATO DE AFIRMACIÓN

    ⚠️ La quinta puede ser para QUIRA lo que el Gold Master fue para la
    trazabilidad: separa la afirmación **computacional** («calcula 27,4582 %»)
    de la **epistemológica** («QUIRA puede afirmar X») y de la
    **interpretación** («la gestión está en tal estado»)."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "cinco reglas que se congelan antes de `Q-M1`" in txt
    assert "CONTRATO DE AFIRMACIÓN" in txt, (
        "desapareció la quinta regla, que es la que convierte los campos 18 y "
        "19 en una barrera epistemológica y no en documentación")
    assert "afirmación COMPUTACIONAL" in txt and \
           "afirmación EPISTEMOLÓGICA" in txt and "INTERPRETACIÓN" in txt, (
        "se perdieron los tres niveles que el contrato separa")


def test_Q_M1_parte_de_las_preguntas_y_no_de_los_indices():
    """★ El cambio de fase, y la pregunta que lo abre:

        «Si mañana borráramos mentalmente los doce índices históricos de
         QUIRA, ¿qué preguntas fundamentales sobre la gestión pública
         seguiríamos necesitando responder?»

    La cadena va `PREGUNTA → FENÓMENO → … → AFIRMACIÓN PERMITIDA → PRODUCTO`
    y **nunca al revés** — `INDICADOR → buscarle una razón de existir` es
    exactamente cómo se llegó a doce índices con 62 % de campos sin declarar.

    ⚠️ Y `Q-M1` no dirá «este sirve y este no»: un indicador podrá
    conservarse, dividirse, fusionarse, trasladarse, volverse componente,
    volverse capa interpretativa, volverse variable, o sólo documentarse
    mejor."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "borráramos mentalmente los doce índices" in txt, (
        "desapareció la pregunta que abre Q-M1. Sin ella, Q-M1 vuelve a ser "
        "una revisión de los doce índices")
    assert "Nunca al revés" in txt
    assert "no dirá «este índice sirve y este no»" in txt.replace(
        "no dirá **«este índice sirve y este no»**",
        "no dirá «este índice sirve y este no»") or \
        "no dirá **«este índice sirve y este no»**" in txt, (
        "Q-M1 dejó de declarar que no emite veredictos de utilidad")
    # ⚠️ Y se enuncia como HIPÓTESIS, no como diagnóstico cerrado. La versión
    # anterior afirmaba «QUIRA no tiene falta de indicadores, tiene un problema
    # de correspondencia»: es una hipótesis estratégica buena y todavía no
    # demostrada. `Q-M1` es quien determina si es el problema CENTRAL.
    assert "problemas de **correspondencia**" in txt, (
        "se perdió la hipótesis de fondo: que el problema está en la "
        "correspondencia entre preguntas, fenómenos, evidencia y unidades")
    assert "`Q-M1` determinará si esa falta de correspondencia constituye" \
           in txt, (
        "la hipótesis volvió a enunciarse como diagnóstico cerrado. Q-M0 "
        "aporta evidencia; no demuestra que sea el problema central")


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
