# -*- coding: utf-8 -*-
"""
scripts/gm_omega/contrato_indice_dominio.py — GM-Ω · TERMINOLOGY FREEZE `T3-T5`

El contrato arquitectónico que le falta a QUIRA:

    ÍNDICE → DOMINIO → ROL → PREGUNTA QUE RESPONDE → CAPA DE PRESENTACIÓN

    POR QUÉ EXISTE. Javo afirmó que cada índice pertenece al dominio que lo
    representa, y tenía razón: la `CONSTITUCION_ONTOLOGICA_QUIRA.md` §CAPA 0.5
    lo declara para los 13 dominios, con su capacidad estatal y su indicador.

    ⚠️ ESTA AUDITORÍA LLEGÓ A AFIRMAR QUE ESE ARTEFACTO NO EXISTÍA. Era falso:
    no lo busqué en la Constitución. El mismo error que le hizo a `E_i`
    —declararlo `UNTRACEABLE` antes de agotar la búsqueda—, y la misma lección:
    **una ausencia sólo se declara después de mirar donde debía estar.**

    Lo que SÍ falta, y es más preciso, es una forma **consumible por máquina** y
    unos campos que la Constitución no tiene: el ROL del indicador, la PREGUNTA
    RECTORA de cada dominio y la CAPA DE PRESENTACIÓN. Sin ellos no se puede
    verificar que un índice no se publique fuera de su dominio, ni detectar que
    un dominio perdió su indicador.

    ⚠️ LAS CELDAS NO SE RELLENAN POR INFERENCIA. Sólo se declara lo que tiene
    AUTORIDAD DOCUMENTAL —un PCD cerrado, un ADR, una decisión registrada—. Todo
    lo demás queda `POR_DECLARAR` y se cuenta. Un contrato a medio llenar que
    dice cuánto le falta es infinitamente más útil que uno completo por
    suposición: eso sería `DOC-009` a escala de arquitectura.

    NO TOCA Gold Master · NO renombra índices · NO modifica frontend.

Uso:  python scripts/gm_omega/contrato_indice_dominio.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_CONTRATO_INDICE_DOMINIO.md"

_PENDIENTE = "POR_DECLARAR"

# ── T4 · ROL DEL INDICADOR ───────────────────────────────────────────────────
_ROLES = {
    "PRIMARIO": "responde la pregunta central de su dominio",
    "COMPUESTO": "agrega otros indicadores",
    "AUXILIAR": "alimenta a otro indicador, no se lee solo",
    "DIAGNÓSTICO": "sirve al análisis interno, no a la lectura pública",
    _PENDIENTE: "⚠️ la arquitectura no lo ha declarado",
}

# ── LOS DOMINIOS ─────────────────────────────────────────────────────────────
# La pregunta de cada dominio SÓLO se declara donde hay PCD cerrado que la
# sostenga. Los demás quedan pendientes: inventarles una pregunta sería
# escribir el canon desde un script, que es lo contrario de lo que QUIRA hace.
#
# ⚠️ CORRECCIÓN DE UN ERROR DE ESTA AUDITORÍA. La versión anterior de este
# script declaró que «no existe un artefacto que declare qué índice pertenece a
# qué dominio». **Es falso**: la `CONSTITUCION_ONTOLOGICA_QUIRA.md` §CAPA 0.5
# lo declara para los 13, con su capacidad estatal y su indicador real. No lo
# busqué ahí. Es exactamente el error que esta misma auditoría le hizo a `E_i`
# —clasificarlo `UNTRACEABLE` antes de agotar la búsqueda— y la lección se
# repite: **una ausencia sólo se declara después de mirar donde debía estar**.
#
# (dominio, capacidad estatal · macroeje, indicador según la Constitución,
#  estado de construcción, pregunta rectora)
_DOMINIOS = {
    "d01": ("Planificación Estratégica", "trayectoria · 1 Dirección",
            "Avance físico metas PDOT", "CONSTRUIDO · PCD-D01",
            "¿Lo planificado se formula en concordancia con el mandato, y el "
            "gasto aterriza donde el plan manda?"),
    "d02": ("Presupuesto y Financiamiento", "movilización · 1 Dirección",
            "Elegibilidad / fondos en riesgo", "PCD-D02", _PENDIENTE),
    "d03": ("Gobernanza del Mandato", "fidelidad democrática · 1 Dirección",
            "Consistencia IFE-A", "PCD-D03", _PENDIENTE),
    "d04": ("Alertas Institucionales", "anticipación · 2 Capacidad",
            "Cola del SAT", "SELLADO · sin construir", _PENDIENTE),
    "d05": ("Holding e Integración Municipal", "articulación · 2 Capacidad",
            "Promedio de entidades", "SELLADO · sin construir", _PENDIENTE),
    "d06": ("Salud Institucional", "sostenibilidad interna · 2 Capacidad",
            "⚠️ «Cumplimiento Institucional (ICPI)»", "PCD-D06 · sintetizador",
            _PENDIENTE),
    "d07": ("Transparencia", "verificabilidad · 3 Democracia",
            "LOTAIP 21/21", "EN CURACIÓN", _PENDIENTE),
    "d08": ("Participación Ciudadana", "inteligencia colectiva · 3 Democracia",
            "Gobernanza participativa (IGP)", "ENTRABLE", _PENDIENTE),
    "d09": ("Rendición de Cuentas", "responsabilidad pública · 3 Democracia",
            "Estado del circuito de rendición", "CONSTRUIDO · PCD-D09",
            "¿Lo que el GAD rindió ante el CPCCS se corresponde con lo que "
            "hizo, y la ciudadanía pudo incidir?"),
    "d10": ("Cobertura de Servicios e Infraestructura", "acceso colectivo · 4 Territorio",
            "Cobertura agua/saneamiento · NBI", "SELLADO · sin construir", _PENDIENTE),
    "d11": ("Desarrollo Económico Territorial", "dinamización · 4 Territorio",
            "PEA / cadenas de valor", "SELLADO · sin construir", _PENDIENTE),
    "d12": ("Inclusión, Equidad y Género", "inclusión y equidad · 4 Territorio",
            "Presupuesto con enfoque de género (PSG)", "SELLADO · sin construir",
            _PENDIENTE),
    "d13": ("Sostenibilidad y Resiliencia Ambiental", "resiliencia · 4 Territorio",
            "ICODS · biofísico/riesgo", "SELLADO · primer ejercicio de mutabilidad",
            _PENDIENTE),
}

# ── EL CONTRATO ──────────────────────────────────────────────────────────────
# (índice, dominio, rol, pregunta que responde, autoridad de la asignación)
#
# ⚠️ Se declara ÚNICAMENTE lo que un documento sostiene. `IPE → d01` consta en
# `PCD-D01` («IPE nativo en Excel», cerrado de cabo a rabo); `IGP → d08` consta
# en `D-010` y en la curación de d08. El resto NO se infiere de dónde aparece
# el nombre: que un índice se mencione en una página no prueba que ese sea su
# dominio canónico.
_CONTRATO = [
    ("ICPI", "d06", "PRIMARIO", _PENDIENTE,
     "Constitución §CAPA 0.5 (d06 → «Cumplimiento Institucional (ICPI)») + "
     "PCD-D06 «Ancla en ICPI» — ⚠️ residencia canónica EN REVISIÓN, ver §T3-R"),
    ("IPE", "d01", "PRIMARIO",
     "¿Qué proporción del gasto ejecutado está vinculada a metas del PDOT?",
     "PCD-D01 · cerrado · fórmula nativa en H16b"),
    ("IGP", "d08", "PRIMARIO", _PENDIENTE,
     "Constitución §CAPA 0.5 (d08 → «Gobernanza participativa (IGP)») · ⚠️ alcance en disputa: mide 2 de 7 mecanismos (D-010)"),
    ("ITAM", "d07", _PENDIENTE, _PENDIENTE, "PCD-D07 · asignación por confirmar"),
    ("IED", _PENDIENTE, _PENDIENTE, _PENDIENTE, "06_IED_DIRECTIVO.md"),
    ("IFE", _PENDIENTE, _PENDIENTE, _PENDIENTE, "H16"),
    ("ICODS", "d13", "PRIMARIO", _PENDIENTE,
     "Constitución §CAPA 0.5 (d13 → «ICODS · biofísico/riesgo»)"),
    ("IEF", _PENDIENTE, _PENDIENTE, _PENDIENTE, "H20c"),
    ("PSG", "d12", "PRIMARIO", _PENDIENTE,
     "Constitución §CAPA 0.5 (d12 → «Presupuesto con enfoque de género (PSG)»)"),
    ("IBSC", _PENDIENTE, _PENDIENTE, _PENDIENTE, "H12b"),
    ("TGI", _PENDIENTE, "COMPUESTO", _PENDIENTE,
     "01_TGI_FRAMEWORK.md · 5 dimensiones · probablemente transversal"),
    ("MMP", _PENDIENTE, _PENDIENTE, _PENDIENTE, "08_MMP_MENSUAL.md"),
]


def _capas() -> dict[str, str]:
    """La capa de presentación ya declarada en el inventario de `T1-T2`.

    ⚠️ Se llamaba `VISIBILIDAD` y el nombre era engañoso: sugería una decisión
    de publicar o esconder, cuando los índices YA pertenecen al producto. Lo que
    se decide es la capa de lectura."""
    from scripts.gm_omega.terminologia_quira import _INVENTARIO
    return {n: v for n, c, _a, v, _x in _INVENTARIO if c == "INDICADOR"}


def main() -> int:
    capas = _capas()
    filas = [{"idx": i, "dom": d, "rol": r, "preg": p, "aut": a,
              "capa": capas.get(i, _PENDIENTE)}
             for i, d, r, p, a in _CONTRATO]

    total = len(filas) * 4          # dominio · rol · pregunta · capa
    faltan = sum(1 for f in filas for k in ("dom", "rol", "preg", "capa")
                 if f[k] == _PENDIENTE)
    dom_sin_preg = sum(1 for _, (_n, _c, _i, _e, q) in _DOMINIOS.items() if q == _PENDIENTE)

    print(f"contrato: {len(filas)} índices × 4 campos = {total} celdas · "
          f"{faltan} POR_DECLARAR ({faltan / total * 100:.0f} %)")
    print(f"dominios sin pregunta declarada: {dom_sin_preg} de {len(_DOMINIOS)}")

    _escribir(filas, total, faltan, dom_sin_preg)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(filas, total, faltan, dom_sin_preg) -> None:
    o: list[str] = []
    A = o.append

    A("# GM-Ω · CONTRATO ÍNDICE → DOMINIO  `T3-T5`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/contrato_indice_dominio.py`. Para declarar una celda, "
      "se edita `_CONTRATO` en el script **citando la autoridad**, no aquí.")
    A("")
    A("> ### Qué es esto")
    A("> El artefacto que le falta a QUIRA para poder decir, de forma "
      "**verificable**:")
    A(">")
    A("> **«Este indicador pertenece aquí, responde esta pregunta y se presenta "
      "de esta manera.»**")
    A(">")
    A("> Cuando exista completo, el frontend deja de ser una discusión estética "
      "y pasa a ser una **proyección de la arquitectura canónica**.")
    A("")
    A("> ### ⚠️ Las celdas NO se rellenan por inferencia")
    A("> Sólo se declara lo que tiene **autoridad documental**: un PCD cerrado, "
      "un ADR, una decisión registrada. Que un índice aparezca en una página no "
      "prueba que ése sea su dominio canónico. Todo lo demás queda "
      f"`{_PENDIENTE}` **y se cuenta**.")
    A(">")
    A("> Un contrato a medio llenar que dice cuánto le falta es más útil que uno "
      "completo por suposición — eso sería `DOC-009` a escala de arquitectura.")
    A("")
    A(f"## Estado: **{faltan} de {total} celdas** por declarar "
      f"({faltan / total * 100:.0f} %)")
    A("")
    A("| Índice | Dominio | Rol | Pregunta que responde | Capa | Autoridad |")
    A("|---|---|---|---|---|---|")
    for f in filas:
        def _c(v):
            return f"**{_PENDIENTE}**" if v == _PENDIENTE else v
        A(f"| `{f['idx']}` | {_c(f['dom'])} | {_c(f['rol'])} | {_c(f['preg'])} | "
          f"{_c(f['capa'])} | {f['aut']} |")
    A("")

    A("## Los dominios y su pregunta")
    A("")
    A("Javo lo señaló: **los dominios también responden a algo propio.** "
      "`m_rdc.py` lo dice en un comentario —«su dueño por la pregunta que "
      "responde»— pero **ningún campo la declara**. Es la misma forma que el "
      "mapeo índice→dominio: existe en el diseño, no como artefacto.")
    A("")
    A("| Dom | Nombre | Capacidad del Estado · macroeje | Indicador (Constitución) | Construcción | Pregunta rectora |")
    A("|---|---|---|---|---|---|")
    for cid, (nombre, cap, ind, estado, preg) in _DOMINIOS.items():
        p = f"**{_PENDIENTE}**" if preg == _PENDIENTE else preg
        A(f"| `{cid}` | {nombre} | {cap} | {ind} | {estado} | {p} |")
    A("")
    A(f"**{dom_sin_preg} de {len(_DOMINIOS)} dominios** no tienen pregunta "
      "declarada. Sólo se escribieron las de `d01` y `d09`, que tienen PCD "
      "cerrado y de cuyo expediente se pueden sostener. **Inventar las demás "
      "sería escribir el canon desde un script**, que es exactamente lo "
      "contrario de cómo QUIRA construye.")
    A("")

    A("## Los roles (`T4`)")
    A("")
    A("| Rol | Qué significa |")
    A("|---|---|")
    for rol, desc in _ROLES.items():
        A(f"| **{rol}** | {desc} |")
    A("")

    A("## ⚠️ El caso `ICPI` merece párrafo propio")
    A("")
    A("**Sí tenía dominio declarado, y estaba donde Javo recordaba**: `PCD-D06 "
      "Salud Institucional` lo fija como su ancla —*«Ancla en ICPI — "
      "cumplimiento sostenible de gobierno»*—. Lo que faltaba no era la "
      "decisión: era el **artefacto que la hiciera legible sin abrir el "
      "expediente de un dominio**. Eso es exactamente lo que este contrato es.")
    A("")
    A("Y el hallazgo interesante es que **la asignación no cierra la pregunta**, "
      "la afina: `d06` está cerrado **como sintetizador** —un dominio que agrega "
      "lo que otros producen—, así que alojar allí un indicador **transversal** "
      "no es una contradicción sino la forma natural de hacerlo. Las dos cosas "
      "pueden ser ciertas a la vez:")
    A("")
    A("> `ICPI` = **indicador nuclear transversal del Gold Master**, con "
      "residencia canónica en `d06` por ser el dominio sintetizador.")
    A("")
    A("⚠️ Se deja como **denominación provisional**, no como decisión. Para "
      "declararlo transversal hace falta responder algo que todavía no está "
      "escrito: **¿la pregunta que responde el ICPI pertenece a un dominio, o "
      "evalúa la relación ENTRE dominios?** Consumir datos de varios silos no "
      "basta —un indicador puede leer de todas partes y aun así responder una "
      "pregunta local—. La celda `pregunta` sigue `POR_DECLARAR` a propósito.")
    A("")

    A("## ★ El título de la tesis disuelve el falso dilema")
    A("")
    A("Javo aportó el título completo del documento fundacional:")
    A("")
    A("> **Arquitectura del Sistema de Integridad Algorítmica Preventiva "
      "(SIAP): Modelo de Congruencia Intersistémica** para la Trazabilidad y "
      "Alineación POA-PDOT en los GAD del Ecuador.")
    A("")
    A("Ese título **contiene las dos palabras**, y no como sinónimos: como "
      "**dos niveles de una misma arquitectura**.")
    A("")
    A("```")
    A("   SIAP   Sistema de INTEGRIDAD Algorítmica Preventiva   ← el propósito")
    A("     └── ICPI   Modelo de CONGRUENCIA Intersistémica     ← lo que mide")
    A("```")
    A("")
    A("Esto **corrige un planteamiento anterior de esta auditoría**. Se había "
      "formulado como disyuntiva —«si el constructo es congruencia hay que "
      "quitar la multiplicatividad; si es integridad conjunta, el nombre se "
      "queda corto»— y era demasiado rápido. La multiplicatividad puede ser "
      "**perfectamente coherente con un constructo de congruencia** si la "
      "teoría establece que la congruencia efectiva **exige simultáneamente** "
      "determinadas condiciones. Integridad y congruencia no compiten por el "
      "nombre: una es el sistema, la otra es el modelo.")
    A("")
    A("Lo que `011` debe juzgar, entonces, **no es qué palabra encaja mejor**, "
      "sino la **semántica de la multiplicación**:")
    A("")
    A("> ¿Qué relación teórica existe entre `P`, `R`, `V`, `E`, `T` y `C`, y qué "
      "significa que uno de ellos sea cero? Si `V=0` —«no pude verificar "
      "documentalmente»— anula toda la contribución de una meta, el índice no "
      "está diciendo «esta meta no es congruente»: está diciendo «la "
      "congruencia **certificable** de esta unidad es nula porque falta una "
      "condición necesaria». Puede ser defendible. Hay que demostrarlo.")
    A("")
    A("Y `SIAP` resultó tener **dos expansiones** en las tesis —«Sistema de "
      "Integridad Algorítmica Preventiva» y «Sistema Integral de Auditoría y "
      "Planificación»—: la misma deriva semántica de `AVEP`, en la sigla que da "
      "nombre al propio Gold Master.")
    A("")

    A("## ★ T3-R · La transversalidad del ICPI es una DECISIÓN NUEVA")
    A("")
    A("Javo lo precisó y corrige cómo se venía contando: **nunca se concibió el "
      "ICPI como transversal.** Tenía su dominio —`d06`— igual que los demás "
      "índices. Lo que ahora se plantea es **incorporar** esa transversalidad.")
    A("")
    A("La diferencia no es de matiz. Presentarlo como si «siempre hubiera sido "
      "transversal y no nos habíamos dado cuenta» sería reescribir la historia "
      "para que encaje con una idea nueva — el mismo pecado que `DOC-016` "
      "prohíbe, aplicado a la arquitectura en vez de al nombre. **Es una "
      "evolución del canon, y como tal se registra.**")
    A("")
    A("### El canon YA autoriza este refactor")
    A("")
    A("No hace falta forzar nada: la Constitución lo previó.")
    A("")
    A("> **DECLARACIÓN DE MUTABILIDAD** — «Los 12 cajones constituyen la "
      "organización operativa VIGENTE […] La estructura de dominios es modular "
      "[…] **Lo permanente es la Capa 0; los dominios son variables.**»")
    A("")
    A("Y `CAPA 0.5` da el criterio que decide: cada dominio es la manifestación "
      "de **una capacidad del Estado**. Ahí está el argumento, y no es una "
      "opinión:")
    A("")
    A("| | |")
    A("|---|---|")
    A("| `d06` es la capacidad de | **sostenibilidad interna** — «cumplir "
      "funciones consistentemente» |")
    A("| El ICPI mide | **congruencia entre el mandato y su materialización a "
      "través de los silos** |")
    A("")
    A("**No son lo mismo.** Y el propio canon lo delata: la Constitución nombra "
      "el indicador de `d06` como «**Cumplimiento** Institucional (ICPI)», "
      "cuando `GM-Ω-ICPI-001` reconstruyó que el ICPI **no mide cumplimiento** "
      "—mide congruencia— y la Regla de Oro lo prohíbe expresamente.")
    A("")
    A("> La residencia del ICPI en `d06` se apoya en una denominación que el "
      "propio canon ya retiró.")
    A("")
    A("Eso **no invalida `d06`**: cuando se selló, «Cumplimiento Institucional» "
      "era la lectura vigente. Es una divergencia **entre dos documentos del "
      "canon**, y resolverla es justamente lo que GM-Ω existe para hacer.")
    A("")
    A("### Pero la transversalidad todavía no está probada")
    A("")
    A("⚠️ **Que el ICPI consuma datos de varios silos NO prueba que sea "
      "transversal.** Un indicador puede leer de todas partes y responder una "
      "pregunta local; inferir la arquitectura del patrón de consumo sería "
      "`DOC-009` otra vez. La prueba tiene que venir del **constructo**:")
    A("")
    A("> Si para responder su pregunta es **necesario relacionar "
      "sistemáticamente dimensiones que pertenecen a distintos dominios**, "
      "entonces la transversalidad es una propiedad del constructo y no una "
      "conveniencia de diseño.")
    A("")
    A("Y el canon ya tiene el instrumento para juzgarlo: **la prueba de "
      "exportabilidad** (Constitución §CAPA 0.5) —*«¿sobreviven las capacidades "
      "si desaparecen los dominios?»*—. Aplicada al ICPI: ¿sobrevive el ICPI si "
      "desaparece `d06`? Si la respuesta es sí, no era su dominio.")
    A("")
    A("### Residencia ≠ ámbito, y ahí está la salida")
    A("")
    A("El contrato actual sólo sabe decir `índice → dominio`, y esa relación es "
      "demasiado pobre. Hacen falta dos campos donde hay uno:")
    A("")
    A("```")
    A("   RESIDENCIA CANÓNICA   dónde se gestiona y quién responde por él")
    A("   ÁMBITO DE COBERTURA   qué dominios atraviesa")
    A("```")
    A("")
    A("Con esa distinción, **sacar el ICPI de `d06` deja de ser un dilema**. No "
      "es «o pertenece a `d06` o desaparece de `d06`»: `d06` puede conservarlo "
      "como **indicador relacionado** —lo necesita para explicar la salud "
      "institucional— sin ser su propietario exclusivo. Nada se esconde; cambia "
      "quién responde por él.")
    A("")
    A("### Secuencia propuesta — y no empieza moviendo nada")
    A("")
    A("| | | |")
    A("|---|---|---|")
    A("| **R0** | Diagnóstico | qué dominios hay, cuáles construidos, qué "
      "pregunta rectora, qué índices residen, cuáles se solapan |")
    A("| **R1** | Modelos | `A` todo índice dentro de un dominio · `B` dominios "
      "+ transversales · `C` dominios + capa transversal + Centro |")
    A("| **R2** | Decisión | ¿sale el ICPI de `d06`? ¿qué otros son "
      "transversales? ¿`d06` conserva referencia? |")
    A("")
    A("⚠️ **`T3-R` es diagnóstico, no ejecución.** No mueve el ICPI, no toca el "
      "Gold Master, no desmonta dominios. Primero se demuestra **qué "
      "arquitectura hace falta**; sólo entonces se cambia. Y `011` sigue por "
      "delante: mover un indicador cuyo constructo aún está en dictamen sería "
      "reorganizar la casa antes de saber qué se guarda.")
    A("")

    A("## ⚠️ Ningún dominio está cerrado hasta pasar este refactor")
    A("")
    A("**Primero, una distinción que esta auditoría tenía al revés.** Javo la "
      "precisó: **sellado ≠ terminado, y sellado ≠ construido.**")
    A("")
    A("| Estado | Qué significa |")
    A("|---|---|")
    A("| **SELLADO** | su concepción quedó fijada bajo el canon de entonces · "
      "**no está construido** |")
    A("| **ABIERTO / CONSTRUIDO** | es sobre el que se ha trabajado y tiene "
      "producto |")
    A("| **CERRADO (PCD)** | su expediente de curación se completó — cosa "
      "distinta de las dos anteriores |")
    A("")
    A("Se venía leyendo «cerrado» como «terminado e intocable», y eso llevó a "
      "recomendar no tocar `d01`, `d06` y `d09`. **Era demasiado fuerte.**")
    A("")
    A("Regla de Javo, entonces, con su consecuencia: esos tres tienen PCD "
      "cerrado bajo un canon **anterior** al Terminology Freeze — antes de que "
      "existieran `DOC-013`, `DOC-014` y este contrato. Su cierre es válido "
      "**para lo que entonces se auditó**, y no acredita lo que entonces no se "
      "preguntaba.")
    A("")
    A("Es el mismo principio que gobierna todo GM-Ω: **un mecanismo de "
      "cobertura no es autoridad sobre su propia cobertura**. Un PCD cerrado "
      "acredita las siete capas que revisó, no las preguntas que aún no se "
      "hacían. Por eso el estado correcto de esos tres no es «cerrado» ni "
      "«abierto», sino **cerrado bajo canon anterior** — y su reapertura es "
      "barata: sólo necesitan declarar su pregunta rectora y la residencia de "
      "sus índices, que es lo que este contrato pide.")
    A("")

    A("## Lo que este contrato NO hace")
    A("")
    A("- **No renombra `ICPI`.** La migración del nombre, si `011` la decide, "
      "no cuesta trazabilidad: el **identificador** (`ICPI`) permanece estable y "
      "es lo que usan el código, el Gold Master y toda referencia previa; el "
      "**nombre desarrollado** puede evolucionar con su versión, su vigencia y "
      "su nombre histórico conservado (`DOC-015`). Pero el orden no se invierte: "
      "**primero se decide qué mide el constructo, después cómo se llama.**")
    A("- **No asigna dominios por inferencia.** Diez de doce índices esperan una "
      "decisión de arquitectura o de curación.")
    A("- **No toca el Gold Master, ni el frontend, ni AVEP.**")
    A("")
    A("---")
    A(f"*GM-Ω · Contrato T3-T5 · {faltan}/{total} celdas por declarar · "
      "ningún código de producto modificado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
