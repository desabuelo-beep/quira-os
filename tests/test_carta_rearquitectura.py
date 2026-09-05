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


def test_el_inventario_se_cuenta_y_lleva_estampilla():
    """Un plan que no sabe su tamaño no es un plan — y un tamaño sin fecha ni
    commit es una **afirmación flotante**.

    ⚠️ EL EPISODIO QUE LO ENSEÑÓ. El colega objetó que el total `1321` no
    cuadraba con `1265` y dedujo un error de cardinalidad. Verificado: el
    total era correcto — la suma omitía `brn` (30), `governance` (23) y
    `marco_teorico` (3) = **56**, exactamente la diferencia detectada.

    Pero su conclusión valía igual **por otra razón**: si un lector experto
    suma mal la tabla, la tabla no era legible. Se corrigió la tabla, no el
    número, y se añadió la regla de conteo explícita.

    Y la estampilla resuelve la otra ambigüedad —«411 o 412»— sin discutirla:
    el número deja de ser una afirmación y pasa a ser una observación
    reproducible de un estado concreto del repositorio."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "rglob" in fuente, (
        "el inventario dejó de contarse del repositorio. Un tamaño escrito a "
        "mano se desactualiza en semanas y nadie se entera")
    txt = _CARTA.read_text(encoding="utf-8")
    for campo in ("INVENTARIO_ID", "COMMIT", "GENERATED_AT"):
        assert campo in txt, (
            f"desapareció `{campo}` de la estampilla. Sin ella, cada cifra "
            f"del inventario es una afirmación flotante que nadie puede "
            f"reproducir ni fechar")
    assert "afirmación flotante" in txt
    assert "Regla de conteo" in txt, (
        "se perdió la regla de conteo. Es lo que hace legible la tabla que un "
        "lector experto ya sumó mal una vez")
    assert "no suman" in txt, (
        "desapareció la marca de las filas contenidas en otras")
    assert "la tabla no era legible" in txt, (
        "se limpió la constancia del episodio. Conservarla es lo que explica "
        "por qué la regla de conteo existe")


def test_las_cuatro_bases_medulares_estan_en_el_eje_cero():
    """★ El vacío que Javo detectó y que obligó a rehacer la carta.

        «NO estamos tomando en consideración al corpus normativo de todo el
         marco legal que hemos vectorizado a Supabase, que es la otra base
         medular de QUIRA.»

    La `v1` inventarió el repositorio y llamó a eso «el ecosistema». Pero
    QUIRA se apoya en CUATRO bases, y el Excel es una de ellas:

        BM-01 NORMATIVA     ¿qué derecho vigente permite afirmar que algo existe?
        BM-02 METODOLÓGICA  ¿cómo se vuelve conocimiento calculable?
        BM-03 EVIDENCIAL    ¿qué documento demuestra el hecho?
        BM-04 ONTOLÓGICA    ¿qué cosas existen y cómo se relacionan?

    ⚠️ Y LA CONSECUENCIA QUE NO PUEDE PERDERSE: **la norma tiene precedencia
    sobre el diseño de QUIRA**. Si la metodología dice que un factor significa
    X y la norma vigente determina otra cosa, la metodología no puede
    ignorarlo. Esa es la línea entre `⚖️ NORMATIVO VIGENTE` y `🔧 DECISIÓN DE
    DISEÑO`, y sin ella las cinco categorías se derrumban."""
    txt = _CARTA.read_text(encoding="utf-8")
    for bid in ("BM-01", "BM-02", "BM-03", "BM-04"):
        assert bid in txt, (
            f"desapareció la base medular `{bid}`. Con menos de cuatro, el "
            f"refactor vuelve a tratar el repositorio como si fuera el "
            f"ecosistema entero")
    assert "PRECEDENCIA sobre el diseño de QUIRA" in txt, (
        "se perdió la precedencia normativa. Sin ella, una decisión de diseño "
        "puede sobrescribir lo que la ley determina, que es exactamente lo "
        "que QUIRA existe para detectar en otros")
    for pieza in ("**NORMA**", "**EVIDENCIA**", "**INFERENCIA QUIRA**"):
        assert pieza in txt, (
            f"desapareció {pieza} de la cadena. Mezclar norma con evidencia o "
            f"con inferencia es el error que produce afirmaciones que parecen "
            f"jurídicas y son metodológicas")


def test_el_corpus_normativo_declara_lo_que_le_falta():
    """★ Lo que midió `BM-01`, y que condiciona el refactor entero.

        · la tabla se llama `normativa_corpus` y contiene DOS universos:
          norma (~8.100) e instrumentos de gestión (~5.000) — BM-01 y BM-03
        · NO existe columna de vigencia: sólo `ingestado_at`, que es cuándo
          se cargó, no cuándo rige
        · `document_class` y `authority_level` vacías en ~81 % del corpus

    ⚠️ LO DE LA VIGENCIA ES LO MÁS GRAVE, y choca con la `Regla de Oro 3`
    —«sin norma verificada, no hay dato»—: hoy el corpus puede devolver un
    artículo derogado con la misma autoridad que uno vigente, y nada en el
    esquema lo impide.

    Esta prueba tolera que no haya conexión —el CI corre sin credenciales— y
    exige que, si no la hay, se declare el tercer estado en vez de estimar."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "`BM-01` · El corpus normativo, medido" in txt, (
        "desapareció la medición del corpus normativo")
    tiene_datos = "fragmentos vectorizados" in txt
    if not tiene_datos:
        assert "NO DETERMINABLE" in txt, (
            "sin conexión a Supabase, la carta debe DECLARAR el tercer estado "
            "en vez de estimar el tamaño del corpus")
        return
    assert "dos universos" in txt, (
        "se perdió que `normativa_corpus` mezcla norma con instrumentos de "
        "gestión. El nombre de la tabla induce a tratarlos igual, y la norma "
        "tiene precedencia mientras que la evidencia no")
    assert "NO EXISTE COLUMNA DE VIGENCIA" in txt or "vigencia presentes" in txt, (
        "la carta dejó de declarar el estado de la vigencia temporal del "
        "corpus. Sin ese dato, «sin norma verificada no hay dato» no se puede "
        "sostener: no se sabe si la norma sigue vigente")


def test_la_clasificacion_epistemologica_no_se_automatiza():
    """★ La corrección que impide crear una caja negra nueva.

    La `v1` decía «que la clasificación sea derivable». Es insuficiente: la
    máquina puede detectar referencias, dependencias y usos, pero **no puede
    decidir** que algo es «una decisión de diseño antigua» o que está
    «superado metodológicamente». Eso es epistemología, no búsqueda.

        classification_candidate  ← lo propone el script
        classification_status     ← lo ratifica la dirección

    ⚠️ Y `NO_DETERMINADO` NO ES UNA SEXTA CATEGORÍA: es un estado de
    evidencia. Sin esa separación el refactor deriva al silogismo falso «no
    está justificado → se puede quitar», que es exactamente lo que `DOC-027`
    prohíbe."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "classification_candidate" in txt and "classification_status" in txt, (
        "desapareció el par candidato/estado. Sin él, automatizar la "
        "clasificación convierte el refactor en una caja negra nueva")
    assert "La máquina propone, la dirección ratifica" in txt or \
           "la dirección ratifica" in txt
    assert "no es una sexta categoría" in txt.lower(), (
        "`NO_DETERMINADO` volvió a tratarse como categoría de tratamiento. Es "
        "un estado de EVIDENCIA: una pieza tiene categoría y estado a la vez")
    assert "nunca autoriza a eliminar" in txt.lower() or \
           "**nunca significa" in txt, (
        "se perdió la prohibición clave: NO_DETERMINADO significa «no lo "
        "hemos demostrado todavía», nunca «la razón no existe»")


def test_auditoria_es_la_prueba_patron_de_migracion_semantica():
    """★ El caso que deja de ser anécdota y se vuelve gate.

        auditoría CGE   ⚖️ referencia legal      INTOCABLE
        GM-Ω «audit.»   🔧 terminología de trabajo  revisar
        QUIRA «audita»  🔧 término incorrecto       sustituir
        auditable       🔬 propiedad                preservar
        auditabilidad   🔬 concepto                 evaluar

    El gate que obliga a construir:

        ninguna migración léxica puede alterar una referencia normativa
        vigente por el solo hecho de compartir una cadena de caracteres
        con un término que se desea reemplazar

    ⚠️ 609 ocurrencias en 233 archivos. Un reemplazo sin clasificar habría
    borrado artículos de ley, y estuvo a punto de ocurrir."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "prueba patrón de migración semántica" in txt, (
        "el caso `auditoría` volvió a ser un ejemplo narrativo. Debe ser el "
        "primer test de Q1: es el único que ya demostró el daño posible")
    assert "por el solo hecho de compartir una cadena de caracteres" in txt, (
        "desapareció el gate de migración léxica. Es la regla que separa un "
        "refactor gobernado de un search-and-replace")
    assert "609 ocurrencias" in txt and "233 archivos" in txt, (
        "se perdió la medición. Sin el tamaño, el riesgo parece teórico")


def test_el_corpus_historico_en_disco_entra_al_inventario():
    """★ El segundo vacío que Javo detectó, y lo planteó como paréntesis:

        «no sé si sea necesario […] hay una carpeta en local con gran parte
         de la historia, son 898 archivos, 147 carpetas»

    **Era necesario**, y por la misma razón que el corpus normativo: la carta
    inventariaba el repositorio y Supabase, y la historia del proyecto vive
    además en carpetas hermanas del disco.

    ⚠️ Y NO ES TEÓRICO — hay precedente en esta misma investigación:
    `metodologia.docx` estaba en una de esas carpetas y **reordenó `011-C3`
    entero**, obligando a corregir la fecha de `C_i` y explicando la
    superposición `E_i`↔`C_i` que `011-C2` había declarado inexplicada.

    Lo que apareció al medir: **83 versiones fechadas del Gold Master**, en
    una carpeta que se llama literalmente `historial_gold_master`. `011-C3`
    no las usó, y declaró `NO DETERMINABLE` la razón de cambios que esa serie
    puede al menos **fechar y describir**.

    La lección que esto fija: **un `NO DETERMINABLE` vale mientras no aparezca
    la fuente. Declararlo no clausura la búsqueda.**"""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "Inventario HISTÓRICO" in txt, (
        "desapareció el corpus histórico en disco. Sin él, el inventario "
        "vuelve a confundir «el repositorio» con «el ecosistema»")
    assert "historial_gold_master" in txt, (
        "se perdió la serie de versiones del motor. Es la fuente que puede "
        "reabrir preguntas que 011-C3 cerró por falta de evidencia")
    assert "puede reabrir `011-C3`" in txt, (
        "la carta dejó de advertir que hay conclusiones cerradas en riesgo. "
        "Ocultarlo haría que el dictamen se apoye en un NO DETERMINABLE que "
        "quizá ya no lo sea")
    assert "no explican el **por qué**" in txt, (
        "se perdió el límite de lo que la serie puede aportar: muestra QUÉ "
        "cambió y cuándo, no POR QUÉ. Sin ese matiz volvería la tentación de "
        "inferir la causa desde el resultado, que es DOC-009")
    assert "Tres sistemas de versionado" in txt, (
        "desapareció el hallazgo de los tres esquemas de versión sin "
        "reconciliar: el motor se llama v2.2, su archivo v5.5 y el canon v5.7")


def test_la_regla_maestra_ordena_las_cinco_fases():
    """`DOC-029` · lo que separa una limpieza de una rearquitectura gobernada.

        OBSERVAR → CLASIFICAR → JUSTIFICAR → DISEÑAR LA MIGRACIÓN → EJECUTAR

    ⚠️ «Clasificar antes de tocar» era correcto pero insuficiente: no decía
    nada sobre justificar ni sobre diseñar la migración. Y el episodio de
    `auditoría` mostró en vivo que QUIRA necesita ese mecanismo de protección
    **antes** de empezar a refactorizar QUIRA."""
    txt = _CARTA.read_text(encoding="utf-8")
    assert "REGLA MAESTRA DE REARQUITECTURA" in txt
    for fase in ("OBSERVA", "CLASIFICA", "JUSTIFICA", "DISEÑA LA MIGRACIÓN",
                 "EJECUTA"):
        assert fase in txt, (
            f"desapareció la fase `{fase}` de la regla maestra. Con menos de "
            f"cinco, el refactor puede saltar de observar a ejecutar")
    assert "rearquitectura gobernada" in txt


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
