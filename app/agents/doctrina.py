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
