"""
app/agents/doctrina.py — cada regla operativa, con su verificador al lado
================================================================================
POR QUÉ EXISTE (2026-09-02). Javo:

> *«BOOT está crónicamente al límite. Ese es un problema para cada iteración, y
> vamos a seguir meses trabajando en QUIRA. Debemos resolverlo.»*

Y tiene razón: `governance/BOOT.md` lleva **doce revisiones pegado al techo** de
6000 bytes. En una sola sesión hubo que recortarlo cuatro veces, y cada recorte
borró información viva para pagar los bytes de la nueva. Eso no es administrar
un presupuesto: es perder memoria para poder seguir escribiendo.

EL DIAGNÓSTICO, medido antes de tocar. `check_health` declara BOOT como «única
fuente de **estado vivo**», y §AHORA es el 48% del archivo. Pero de sus 26
líneas **sólo 7 son estado**: las otras 19 son doctrina permanente —ADR-049 a
053, la escalera, los 8 estados, la procedencia, las fronteras—. El archivo dejó
de ser lo que su presupuesto dice que es, y por eso el presupuesto ahoga.

    §AHORA mezcla dos naturalezas con un solo presupuesto:
      · ESTADO    cambia cada sesión, se sustituye
      · DOCTRINA  permanente, sólo se acumula — un ADR nuevo, una línea más

POR QUÉ NINGUNA LÍNEA PODÍA SALIR, que es la causa real. Nadie podía saber qué
líneas son la ÚNICA defensa de una regla y cuáles son un recordatorio de algo ya
garantizado por un gate. Quitar la equivocada desprotege el sistema, así que no
se quitaba ninguna. El archivo sólo podía crecer.

    Una regla escrita en un documento de arranque es una nota que hay que
    recordar. Una regla con verificador es una regla que se aplica sola.

LO QUE ESTE REGISTRO HACE, y es el patrón que `deuda.py` ya demostró: declarar
el vínculo. Cada regla nombra el ataque que la sostiene, y una prueba comprueba
que ese ataque existe de verdad. Entonces —y sólo entonces— la regla puede salir
de BOOT sin desproteger nada: no se borra, cambia de custodio.

⚠️ EL VÍNCULO NO SE DERIVA, SE DECLARA. Se intentó derivarlo buscando términos
en `tests/` y salieron 18 de 19 «cubiertas» — falso: que un archivo mencione la
palabra «naturaleza» no prueba que verifique ADR-052. Es el mismo error léxico
que esta sesión lleva doce casos desmontando. Cada entrada de aquí se estableció
leyendo el verificador, no buscándolo.

    REGLA CON VERIFICADOR VIVO  →  puede salir de BOOT
    REGLA SIN VERIFICADOR       →  se queda: ahí BOOT ES la defensa

Y las que no tienen verificador quedan visibles, que es lo valioso: son el mapa
de qué doctrina todavía depende de que alguien la recuerde.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
BOOT = RAIZ / "governance" / "BOOT.md"

# Dónde vive la custodia de la regla.
GATE = "un_gate_o_ataque_la_sostiene"       # se aplica sola; BOOT no la necesita
SOLO_BOOT = "solo_la_recuerda_el_arranque"  # nadie la verifica: BOOT ES la defensa

# ⚠️ EL TERCER ESTADO, que la Capa 0 obligó a nombrar en cuanto nació el módulo.
# Sin él, una regla ausente de este registro se leería como «no tiene gate», y lo
# que significa es «nadie ha ido a mirar». Es la misma distinción que el sistema
# le exige al GAD —«no existe» ≠ «no pude obtener»— aplicada a su propia doctrina.
# Se usa el término canónico de la casa —`no_determinable`— y no uno nuevo:
# inventar vocabulario para decir lo que el canon ya dice es justo lo que la
# Regla de Oro 7 prohíbe.
VINCULO_NO_DETERMINADO = "no_determinable_si_algo_la_sostiene"

_DOCTRINA = (
    dict(id="DOC-001", custodia=GATE,
         regla="TEST ≠ OPERACIÓN · una prueba no actúa sobre el mundo sin "
               "declararlo",
         fuente="Javo 2026-08-25 · deuda 4-ter · tests/conftest.py",
         verificador="test_una_prueba_no_declarada_no_puede_lanzar_un_subproceso",
         por_que_ahi="`subprocess` es el único punto por el que sale el trabajo "
                     "real; cerrarlo cierra la descarga, la regeneración y la red"),
    dict(id="DOC-002", custodia=GATE,
         regla="8 ESTADOS · «no existe» ≠ «no pude obtener» ≠ «no lo intenté»",
         fuente="ADR-042 §6",
         verificador="test_d_una_captura_que_fallo_no_es_una_ausencia",
         por_que_ahi="si un 404 o un corte de fuente se registrara como ausencia, "
                     "QUIRA imputaría al GAD una limitación del observador"),
    dict(id="DOC-003", custodia=GATE,
         regla="Quién carga el YAML de su RO queda registrado con trinquete: "
               "si otro dominio empieza a hacerlo, tiene que constar",
         fuente="ADR-038 · CLAUDE.md regla 9",
         verificador="test_d07_es_el_unico_que_carga_el_yaml_de_su_regla",
         por_que_ahi="trinquete hacia arriba: si otro dominio empieza a cargarla "
                     "queda constancia, y si d07 dejara de hacerlo se entera alguien"),
    dict(id="DOC-004", custodia=GATE,
         regla="ADR-042 · env_obs ≠ env_ops · Observatorio ≠ Centro · "
               "Operaciones NO es producto",
         fuente="ADR-042 · ADR-041 §4",
         verificador="test_las_cuatro_fronteras_declaradas_se_observan_en_el_codigo",
         por_que_ahi="las cuatro fronteras se comprueban CONTRA EL CÓDIGO, no "
                     "contra su enunciado: `env_obs` no menciona el Centro"),
    dict(id="DOC-005", custodia=GATE,
         regla="PROCEDENCIA · d02 y d03 declaran sobre quién leen y NO llevan "
               "reloj (estamparla después re-ejecuta la cadena)",
         fuente="ADR-051 · sesión de procedencia 2026-08-25",
         verificador="test_d02_declara_sobre_quien_lee_y_sin_reloj",
         por_que_ahi="un reloj dentro del declarante hace que el mecanismo de "
                     "observación modifique el objeto observado"),
    dict(id="DOC-007", custodia=GATE,
         regla="Un documento puede ser EVIDENCIA para un dominio sin ser su "
               "documento PRIMIGENIO. d08 no ilustra su vitalidad con la "
               "asistencia a las jornadas de rendición: esa acta es de d09",
         fuente="Javo 2026-09-03 · frontera formalizada por el colega",
         verificador="test_d08_no_ilustra_su_vitalidad_con_evidencia_de_d09",
         por_que_ahi="el mismo gráfico —201·261·322— salía en los dos cajones, y "
                     "el pie afirmaba «el único registro disponible» cuando 31 "
                     "actas propias declaran registro anexo: lo que falta es su "
                     "digitalización, no el registro"),
    dict(id="DOC-008", custodia=GATE,
         regla="AFILIACIÓN NO IMPLICA E_i REDUCIDO · pertenecer a una entidad "
               "adscrita (EP municipal, patronato) NO determina por sí solo un "
               "coeficiente menor. Es la mitad estrecha y demostrable del "
               "principio: QUIRA penaliza la pérdida VERIFICABLE de integridad, "
               "no la arquitectura administrativa legítima",
         alcance_del_verificador="⚠️ ACOTADO POR EL COLEGA. Que existan adscritas "
               "con E_i=1,00 demuestra que la adscripción no implica "
               "penalización automática; NO demuestra que «la arquitectura "
               "legítima nunca es penalizada» —eso exigiría conocer la regla de "
               "asignación vigente, que está NOT_DETERMINABLE—. El test prueba "
               "una propiedad más estrecha y perfectamente defendible, que es "
               "mejor que intentar demostrar más de lo que mide",
         fuente="Javo 2026-09-03 —«es la misma institucionalidad, NO otro nivel "
                "de gobierno»— · formalizado por el colega",
         verificador="test_ser_entidad_adscrita_no_determina_E_i",
         por_que_ahi="si delegar debilitara la trazabilidad, `V_i` ya lo mediría "
                     "sobre el rastro REAL; penalizar por el organigrama sería "
                     "usar estructura institucional como proxy de desempeño, e "
                     "imputar por presunción donde el sistema exige evidencia"),
    dict(id="DOC-009", custodia=GATE,
         regla="No inferir la REGLA GENERADORA de un dato a partir del patrón "
               "observado en sus resultados. `datos → patrón → hipótesis` NO "
               "equivale a `regla → datos`. Cuando una explicación encaja, "
               "primero se pregunta qué evidencia demuestra que ESA era la "
               "regla; si no existe, permanece hipótesis",
         fuente="el colega, 2026-09-03 · GM-Ω, tras cazar al director "
                "infiriendo el criterio de E_i desde sus valores",
         verificador="test_ninguna_regla_generadora_se_infiere_del_patron_de_sus_resultados",
         por_que_ahi="con 25 casos y tres valores posibles, cualquier hipótesis "
                     "encuentra algunos que la respaldan: encajar no es derivar"),
    dict(id="DOC-020", custodia=GATE,
         regla="La CORRESPONDENCIA entre una unidad documental y una unidad "
               "operacional es un DATO EXPLÍCITO del modelo, declarado y "
               "auditable — nunca una inferencia del motor. Ningún algoritmo de "
               "similitud textual, numérica o semántica puede establecer una "
               "correspondencia canónica: produce CANDIDATOS que una persona "
               "confirma. Y de ahí la regla de hierro: **no se recalcula el "
               "ICPI «para ver qué pasa» hasta que 011-A defina qué es `i`**",
         fuente="el colega, 2026-09-03 · precisión final sobre el contrato v2",
         verificador="test_el_catalogo_de_correspondencias_es_insumo_no_canon",
         por_que_ahi="008-R escribió un algoritmo que empareja por cifras y "
                     "acertó en un caso comprobable. El riesgo es justamente "
                     "ése: que un método que funciona a veces se convierta en "
                     "autoridad. Si el motor puede «descubrir» que dos metas "
                     "corresponden, la trazabilidad deja de ser un dato y pasa "
                     "a ser una hipótesis con formato de tabla. Y recalcular "
                     "antes de saber qué representa `i` daría un número "
                     "matemáticamente impecable y epistemológicamente inútil"),
    dict(id="DOC-019", custodia=GATE,
         regla="Un caso demostrado NO autoriza la regla general. «Existe al "
               "menos un X» y «todos son X» son afirmaciones distintas, y sólo "
               "la primera la sostiene una evidencia puntual. Antes de "
               "generalizar hay que comprobar que los propios datos no lo "
               "desmientan",
         fuente="el colega, 2026-09-03 · GM-Ω-008-R, al frenar la conclusión "
                "«el motor agregó las 66 en 25»",
         verificador="test_el_hallazgo_N1_no_se_generaliza_a_regla",
         por_que_ahi="008-R encontró un caso inequívoco de correspondencia N:1 "
                     "—una unidad del motor con las cifras de tres metas del "
                     "PDOT— y esta dirección concluyó que el motor agregaba las "
                     "66 en 25. Los propios números del informe lo desmentían: "
                     "19 de las 25 no tienen componentes atribuidas. ⚠️ Y NO ES "
                     "DOC-009, aunque se le parezca: son errores DISTINTOS y "
                     "confundirlos diluye los dos. DOC-009 evita «los "
                     "resultados muestran este patrón → ésa fue la regla que "
                     "los generó»; DOC-019 evita «encontré un caso con esta "
                     "propiedad → todos la tienen». Uno va del efecto a la "
                     "causa; el otro, de lo particular a lo universal. Aquí el "
                     "error fue el segundo: **existencia de N:1 ≠ "
                     "universalidad de N:1** — convertir una evidencia local en "
                     "una ontología global"),
    dict(id="DOC-018", custodia=GATE,
         regla="La justificación del UNIVERSO OPERACIONAL no implica la "
               "justificación de su MECANISMO DE SELECCIÓN. Decidir con "
               "autoridad que se mide sobre un subconjunto no demuestra que ese "
               "subconjunto sea representativo: son dos afirmaciones distintas "
               "y sólo la primera la da un ADR",
         fuente="el colega, 2026-09-03 · GM-Ω-ICPI-008, al precisar el veredicto "
                "de cobertura",
         verificador="test_el_criterio_de_seleccion_se_declara_con_su_autoridad",
         por_que_ahi="`ADR-036` ratificó usar 25 metas como universo operacional "
                     "v1 y eso quedó bien justificado; durante meses pareció "
                     "que con ello estaba justificada también la muestra. No lo "
                     "estaba: el criterio —mayor monto económico— sólo se supo "
                     "cuando Javo lo declaró. Es la misma trampa de `E_i`: "
                     "conocer el valor no es conocer la regla que lo produjo, y "
                     "aquí la regla llegó de su fuente legítima —quien la "
                     "aplicó— y no de mirar el resultado"),
    dict(id="DOC-017", custodia=GATE,
         regla="La CONSECUENCIA PRÁCTICA de un ADR ratificado necesita custodio. "
               "Un ADR que ordena algo —«toda publicación debe declarar su "
               "alcance»— y no deja prueba que lo verifique es una decisión que "
               "existe en el papel y no en el producto. Ratificar no es ejecutar",
         fuente="GM-Ω-ICPI-008, 2026-09-03 · el ADR-036 §1 obliga a declarar el "
                "universo operacional en d01/d03 y aparece en 0 superficies",
         verificador="test_el_alcance_del_ICPI_se_declara_donde_el_ADR_lo_exige",
         por_que_ahi="es «un gate que no corre acredita cero» (D-004) aplicado a "
                     "las decisiones de arquitectura. El ADR-036 convirtió una "
                     "debilidad en una decisión transparente y defendible — pero "
                     "sólo dentro del propio ADR: el usuario que lee el ICPI en "
                     "una superficie sigue recibiendo un índice que se presenta "
                     "como global sobre un universo del que nadie le informa. Es "
                     "el patrón del «48,33 %» invertido: allí una cifra retirada "
                     "seguía publicándose; aquí una declaración obligatoria "
                     "nunca llegó a publicarse"),
    dict(id="DOC-016", custodia=GATE,
         regla="No se cambia la ONTOLOGÍA de un indicador para hacerla coincidir "
               "con su IMPLEMENTACIÓN; se corrige la implementación para "
               "hacerla coincidir con la ontología validada. Descubrir que la "
               "fórmula hace A no autoriza a rebautizar A como si siempre "
               "hubiera sido el propósito",
         fuente="el colega, 2026-09-03 · principio rector de T3-T6, tras frenar "
                "una disyuntiva prematura entre «congruencia» e «integridad»",
         verificador="test_la_ontologia_gobierna_a_la_implementacion_no_al_reves",
         por_que_ahi="el título de la tesis —«Sistema de INTEGRIDAD Algorítmica "
                     "Preventiva: Modelo de CONGRUENCIA Intersistémica»— "
                     "contiene ambas palabras como dos NIVELES, no como "
                     "alternativas. La disyuntiva que esta auditoría llegó a "
                     "plantear era falsa, y de haberla resuelto «eligiendo "
                     "nombre» habríamos adaptado la ontología al álgebra que "
                     "todavía no está fundamentada"),
    dict(id="DOC-015", custodia=GATE,
         regla="IDENTIFICADOR ESTABLE ≠ NOMBRE CANÓNICO. El identificador de un "
               "objeto —`ICPI`— NO cambia nunca: lo usan el código, el Gold "
               "Master y toda referencia previa. El nombre desarrollado SÍ puede "
               "evolucionar, con su versión, su vigencia y su nombre histórico "
               "conservado. Migrar un nombre no debe costar trazabilidad, y con "
               "esta separación no la cuesta",
         fuente="Javo, 2026-09-03 —«si debería considerar la migración, pero "
                "sin perder la trazabilidad que se ha creado a partir del "
                "nombre histórico»—",
         verificador="test_el_identificador_es_estable_y_el_nombre_puede_migrar",
         por_que_ahi="es el mecanismo del basónimo en nomenclatura científica: "
                     "una especie se renombra, el nombre original queda "
                     "registrado y ninguna cita anterior se rompe. Sin esta "
                     "separación, «renombrar» y «conservar la genealogía» "
                     "parecen excluyentes y obligan a elegir. Con ella, el "
                     "orden correcto es posible: PRIMERO se decide qué mide el "
                     "constructo (011), DESPUÉS cómo se llama — nunca al revés, "
                     "que sería poner etiqueta nueva a contenido no auditado"),
    dict(id="DOC-014", custodia=GATE,
         regla="NOMBRE TÉCNICO ≠ NOMBRE DE PRESENTACIÓN. Un indicador se publica "
               "en TRES capas —pregunta pública · ficha metodológica · "
               "trazabilidad forense— y ninguna sustituye a las otras. El "
               "Bloomberg Firewall no significa «prohibir siglas»: significa "
               "que el lenguaje interno no se filtre ACCIDENTALMENTE como "
               "lenguaje de producto. Y la primera capa nunca publica un "
               "porcentaje sin decir qué pregunta responde",
         fuente="el colega, 2026-09-03, corregido por Javo: los índices SÍ "
                "aparecen en el dominio que los representa — la decisión no es "
                "cuáles publicar, sino en qué capa de lectura",
         verificador="test_todo_indicador_publicable_declara_su_capa_de_lectura",
         por_que_ahi="una portada de siglas y porcentajes flotantes induce a "
                     "leerlos como notas comparables, y DOC-012 ya dice por qué "
                     "eso es falso. Pero esconder el nombre técnico rompería la "
                     "otra mitad de QUIRA: que toda afirmación pueda regresar a "
                     "su evidencia y su metodología. Tres capas resuelven ambas"),
    dict(id="DOC-013", custodia=GATE,
         regla="QUIRA no conserva conceptos por HERENCIA; conserva únicamente "
               "conceptos que cumplen una FUNCIÓN VERIFICABLE en su "
               "arquitectura. Que un nombre se haya propagado por el "
               "repositorio no demuestra que deba existir: demuestra que se "
               "propagó. Y todo nombre debe poder responder «¿qué tipo de "
               "objeto QUIRA soy?» — fuente · evidencia · variable · indicador "
               "· estado · producto · capa · función · artefacto",
         fuente="Javo, 2026-09-03 —«si no aporta a QUIRA solo infla»— elevado "
                "por el colega de criterio de canon a higiene ontológica",
         verificador="test_todo_nombre_propio_declara_su_categoria_ontologica",
         por_que_ahi="es la Regla de Oro 7 (anti-inflación del canon) aplicada "
                     "al VOCABULARIO, y con una salvaguarda que la separa de "
                     "destruir evidencia: un concepto puede morir como "
                     "componente activo SIN desaparecer de la historia de "
                     "QUIRA. AVEP es el caso que la produjo — se propagó a 67 "
                     "archivos sin responder a ninguna categoría"),
    dict(id="DOC-012", custodia=GATE,
         regla="Un PORCENTAJE no tiene significado semántico por sí mismo. El "
               "significado de sus rangos depende del constructo que mide, de la "
               "teoría de interpretación y de la procedencia de sus umbrales. "
               "95 % en desempeño humano ≠ 95 % en congruencia intersistémica ≠ "
               "95 % en transparencia: el número puede ser el mismo, la "
               "afirmación no",
         fuente="el colega, 2026-09-03 · GM-Ω-ICPI-007-X-bis, sobre el aporte de "
                "Javo de que AVEP es baremo propio y existe además una escala "
                "obligatoria LOSEP",
         verificador="test_ninguna_escala_ajena_se_adopta_por_compartir_la_unidad",
         por_que_ahi="la escala LOSEP del Ministerio del Trabajo (95/90/80/70) "
                     "es obligatoria y está a mano, y adoptarla para el ICPI "
                     "sería confundir dos constructos porque ambos producen "
                     "porcentajes. El diseño original YA tenía la distinción "
                     "resuelta —el módulo F-EDS traducía el índice a insumos "
                     "LOSEP como puente explícito—, y perderla sería deshacer "
                     "trabajo bien hecho. Contrastar no es adoptar"),
    dict(id="DOC-011", custodia=GATE,
         regla="Un vacío de trazabilidad se clasifica por su NATURALEZA, no por "
               "su tamaño. «No puedo reconstruirlo del todo» —hay genealogía y "
               "un límite explícito— NO es «no hay nada que reconstruir» —no "
               "existe evidencia preservada de la regla generadora—. Exigen "
               "auditorías distintas y admiten conclusiones distintas",
         fuente="el colega, 2026-09-03 · GM-Ω-ICPI-007, al contrastar V_i "
                "contra E_i",
         verificador="test_V_y_E_no_comparten_la_naturaleza_de_su_vacio",
         por_que_ahi="`V` tiene regla vigente, regla histórica, motivo del "
                     "cambio y 25 de 25 valores reproducibles: su vacío es un "
                     "LÍMITE DE RECONSTRUCCIÓN, y eso es sano para una "
                     "auditoría. `E` tiene valores y ninguna regla que los "
                     "produzca: su vacío es AUSENCIA DE REGLA GENERADORA. "
                     "Tratarlos igual llevaría a sospechar de todo el motor por "
                     "lo que falla en una variable — o, al revés, a dar por "
                     "buena una ausencia porque otras variables sí documentan"),
    dict(id="DOC-010", custodia=GATE,
         regla="Un contrafactual no sale del laboratorio. Toda cifra producida "
               "por un escenario de auditoría lleva sus TRES etiquetas "
               "—MATEMÁTICAMENTE REPRODUCIBLE · METODOLÓGICAMENTE CONTRAFACTUAL "
               "· NO AUTORIZADO PARA PUBLICACIÓN— y ninguna puede aparecer en "
               "una superficie del producto mientras el dictamen no la adopte",
         fuente="el colega, 2026-09-03 · GM-Ω-ICPI-007, al abrir 16 escenarios "
                "sobre la cifra madre",
         verificador="test_ningun_contrafactual_se_filtro_a_las_superficies",
         por_que_ahi="el riesgo no es hipotético: es el «48,33 %», un número de "
                     "trabajo que sobrevivió a su contexto y siguió publicándose "
                     "22 días. Una auditoría que genera cifras nuevas multiplica "
                     "ese riesgo, y el custodio busca los valores REALES leídos "
                     "del documento derivado, no una lista escrita a mano"),
    dict(id="DOC-006", custodia=GATE,
         regla="Lo PENDIENTE declarado no se confunde con lo NO CONSTATADO — "
               "tres estados, no dos",
         fuente="Constitución Ontológica CAPA 0 · regla de DETERMINABILIDAD",
         verificador="test_ataque_lo_pendiente_no_se_confunde_con_lo_no_constatado",
         por_que_ahi="colapsarlos convertiría un trámite abierto y declarado en "
                     "un vacío documental"),
)

# Cifras de BOOT que NO son doctrina ni decisión: son DERIVADOS de una fuente
# viva, escritos a mano. Es el patrón que produjo el «48,33 %» — una nota
# metodológica que siguió publicando el método retirado durante 22 días porque
# su cifra estaba escrita, no derivada.
#
# ⚠️ NO SE GENERAN: BOOT lo escribe una persona y debe seguir leyéndose como
# prosa. Lo que se hace es DETECTAR LA DIVERGENCIA — si BOOT afirma un número
# que su fuente contradice, la prueba falla y alguien lo corrige. Generar BOOT
# lo volvería ilegible; verificarlo lo mantiene verdadero.
_DERIVADOS = (
    dict(en_boot=r"gates?\s*\+\s*suite EN CI|(\d+)\s*gates",
         que="cuántos gates hay en scripts/ci/",
         fuente="len(list((RAIZ/'scripts'/'ci').glob('check_*.py')))"),
    dict(en_boot=r"\*\*(\d+) en sentinel\*\*",
         que="rutas personales que el gate de portabilidad todavía ve",
         fuente="scripts/ci/check_portabilidad.py · TOPE['personal']"),
)


def doctrina() -> list[dict]:
    """El registro, con cada verificador localizado en disco.

    Se comprueba que la prueba EXISTE, no que esté bien escrita: nombrar un
    verificador inexistente sería acreditar sin nada detrás — el mismo defecto
    que el escalón 2 de la escalera cerró para la evidencia."""
    donde: dict[str, str] = {}
    for f in (RAIZ / "tests").glob("test_*.py"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        for d in _DOCTRINA:
            if f"def {d['verificador']}(" in txt:
                donde[d["id"]] = f.relative_to(RAIZ).as_posix()
    return [{**d, "verificador_en": donde.get(d["id"], "")} for d in _DOCTRINA]


def puede_salir_de_boot(regla_id: str) -> dict:
    """¿Esta regla sigue necesitando estar en el arranque?

    La respuesta NO es una opinión sobre su importancia: es si algo la sostiene
    cuando nadie la recuerda."""
    d = next((x for x in doctrina() if x["id"] == regla_id), None)
    if d is None:
        return {"puede": False, "por_que": f"{regla_id} no está en el registro"}
    if not d["verificador_en"]:
        return {"puede": False,
                "por_que": f"declara «{d['verificador']}» y esa prueba no existe "
                           f"en disco: la regla quedaría sin custodio"}
    return {"puede": True,
            "por_que": f"la sostiene {d['verificador']} en {d['verificador_en']}"}


def cobertura_de_doctrina() -> dict:
    """Qué doctrina se aplica sola y cuál depende de que alguien la recuerde."""
    filas = doctrina()
    con_gate = [d["id"] for d in filas if d["verificador_en"]]
    huerfanas = [d["id"] for d in filas if not d["verificador_en"]]
    return {
        "reglas": filas,
        "con_verificador": con_gate,
        "sin_verificador": huerfanas,
        "universo": {
            "que": "doctrina operativa que vivía en §AHORA de BOOT.md",
            "donde": "app/agents/doctrina.py, contrastado con tests/",
            "como": "DECLARACIÓN CON JUICIO, no barrido. El vínculo regla→"
                    "verificador se estableció LEYENDO cada prueba: derivarlo "
                    "por búsqueda de términos dio 18 de 19 «cubiertas» y era "
                    "falso (C0 · el mismo error léxico de toda la sesión)",
            "hallados": len(filas),
            "mecanismo": {
                "tipo": "explicitamente_limitado",
                "operacion": "declaración",
                "por_que": "migrar una regla exige leer su verificador y "
                           "responder por el vínculo; hacerlo en bloque sería "
                           "fabricar la cobertura que se quiere demostrar",
            },
            "exclusiones": [
                {"patron": "doctrina de §AHORA sin vínculo establecido",
                 "motivo": "migrarla exigiría leer su verificador y responder "
                           "por el vínculo; declararla cubierta sin haberlo "
                           "leído fabricaría la cobertura que se quiere "
                           "demostrar. Su estado es "
                           f"«{VINCULO_NO_DETERMINADO}», no «sin gate»",
                 "autoridad": "criterio de esta sesión, 2026-09-02 · el intento "
                              "de derivar el vínculo por búsqueda dio 18 de 19 "
                              "«cubiertas» y era falso"},
            ],
            "fuera_de_alcance": [
                "§AHORA conserva doctrina sin migrar: NO está desprotegida, "
                "sigue en BOOT, que es donde debe estar mientras nadie la "
                "verifique. Su ausencia aquí significa «todavía no se estableció "
                "el vínculo», nunca «no tiene regla»",
                "que un verificador exista no prueba que verifique BIEN la "
                "regla: eso exige leerlo, y este módulo no puede leer por nadie",
            ],
        },
        "afirmacion_sostenible": (
            f"{len(con_gate)} reglas de doctrina tienen un verificador que existe "
            f"en disco y por eso pueden salir del arranque sin quedar "
            f"desprotegidas: cambian de custodio, no desaparecen. "
            + (f"{len(huerfanas)} lo declaran y no lo tienen: "
               f"{', '.join(huerfanas)}. " if huerfanas else "")
            + "Lo que este registro NO dice es que la doctrina restante de BOOT "
              "esté sin gate — dice que el vínculo no se ha establecido, y "
              "establecerlo exige leer, no buscar."
        ),
    }


def cifras_de_boot_divergentes() -> list[dict]:
    """Cifras escritas en BOOT que su fuente viva contradice.

    EL PATRÓN QUE ESTO PERSIGUE tiene nombre desde el 2026-09-02: *derivado
    narrativo desacoplado de la fuente canónica*. Se descubrió con el «48,33 %»
    de `p16_gobernanza`, que siguió publicando durante 22 días una cifra y un
    método que Javo había retirado. BOOT tiene la misma forma: prosa con números
    escritos a mano.

    En esta misma sesión hubo que corregirle dos —«0 rutas fijas» cuando eran 3,
    «12 GATES» cuando sólo corría 1— y se corrigieron porque alguien miró, no
    porque algo avisara."""
    if not BOOT.exists():
        return [{"estado": "no_determinable", "por_que": "no existe BOOT.md"}]
    txt = BOOT.read_text(encoding="utf-8", errors="replace")
    fuera = []

    gates = len(list((RAIZ / "scripts" / "ci").glob("check_*.py")))
    m = re.search(r"\*\*(\d+) gates", txt)
    if m and int(m.group(1)) != gates:
        fuera.append({"en_boot": f"{m.group(1)} gates", "real": f"{gates} gates",
                      "fuente": "scripts/ci/check_*.py"})

    gate = (RAIZ / "scripts" / "ci" / "check_portabilidad.py")
    if gate.exists():
        t = re.search(r'"personal":\s*(\d+)', gate.read_text(encoding="utf-8"))
        b = re.search(r"\*\*(\d+) en sentinel\*\*", txt)
        if t and b and t.group(1) != b.group(1):
            fuera.append({"en_boot": f"{b.group(1)} en sentinel",
                          "real": f"{t.group(1)}",
                          "fuente": "check_portabilidad.py · TOPE['personal']"})
    return fuera
