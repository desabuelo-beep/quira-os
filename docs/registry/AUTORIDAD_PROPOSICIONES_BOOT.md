---
authority:
  parent: GOVERNANCE-001
  type: REGISTRO
estado: ABIERTO — inventario cerrado, decisiones pendientes
fecha: 2026-08-25
---

# Autoridad de las proposiciones de BOOT — inventario, no poda

> **Este registro NO decide nada.** Reúne la evidencia para que la decisión de gobernanza tenga
> sobre qué decidirse. Ninguna de sus filas autoriza a mover una línea de `governance/BOOT.md`.

## La regla que gobierna la lectura de este registro

> **Que exista evidencia de que una proposición tuvo rango NO significa que vuelva a estar
> vigente.** *(colega, 2026-08-25)*

Es la misma distinción que el dominio le exige al sujeto observado, aplicada a nosotros: **la
evidencia informa la decisión; no la sustituye.** Un registro que la olvidara reintroduciría por la
puerta de atrás justo lo que existe para impedir — canon aparecido sin que nadie lo decidiera.

De ahí tres corolarios que este registro **no** puede saltarse:

| se ha comprobado que… | …y aun así |
|---|---|
| #5 fue Regla de Oro #4 | eso es **genealogía de autoridad**, no una decisión de restauración |
| `INVENTARIO-CONCEPTOS-001` está vigente | eso **no hace vigente** la regla «consultarlo antes de definir» |
| el código ejecuta #1 en el producto | eso demuestra **tratamiento**, no decisión originaria |

> ⛔ **Aquí figuraba un tercer corolario que resultó FALSO**, y se retira dejando constancia:
> *«ADR-041/043 tienen autoridad sobre los productos → no la transfieren a la agrupación F1/F2/F3»*.
> El principio es correcto, **pero el ejemplo no**: `ADR-041 §4` **sí declara** la agrupación en
> fases. Ver §F. Ilustrar una regla verdadera con un caso falso la vuelve inservible — y peor, la
> hace parecer demostrada.

## Dónde encaja este registro

    BOOT           «esto es lo que el operador debe saber»
    ESTE REGISTRO  «esto creemos que BOOT dice · qué evidencia lo respalda · quién debe decidirlo»
    ADR / CONSTITUCIÓN  «esto ya fue decidido»

El ciclo que esa separación rompe, y que esta sesión persiguió entera:

    BOOT → atribución → falsa autoridad → compresión → canon aparente
         → construcción sobre una premisa que nadie decidió

El flujo correcto queda:

    fuente primaria → proposición → registro de autoridad → decisión de Javo → canon → BOOT lo refleja

*(Sin `constitution_articles`: la propia Constitución declara dos numeraciones incompatibles
—Art. 0-30 y Art. 1-21, siendo la B la oficial y la otra derogada— y no verifiqué cuál cubre este
registro. No se citan artículos que no se comprobaron.)*

## Por qué existe

Depurando `§AHORA` apareció algo que no era un problema de tamaño. El colega lo formuló así:

> *«La compresión anterior no sólo había eliminado información; en algunos puntos había comprimido
> la relación entre una proposición y su autoridad hasta hacer parecer que una autoridad decía algo
> que nunca dijo.»*

Y el principio que ordena todo lo demás:

> **BOOT no debe decidir qué es canon. BOOT sólo debe reflejar el canon que ya ha sido decidido.**

## El procedimiento, que no debe saltarse

    proposición → evidencia → hogar → autoridad → cobertura → estado → decisión → recién entonces poda

Con tres estados posibles, y sólo tres:

| | |
|---|---|
| **A** | recuperable con autoridad válida — BOOT puede apuntar a ella |
| **B** | existe pero carece de autoridad suficiente — no se poda; requiere gobernanza |
| **C** | no existe como norma viva — **no se inventa autoridad**; queda candidata |

## El inventario

| # | proposición | naturaleza | estado | evidencia verificada |
|---|---|---|---|---|
| 1 | «NO es auditoría ni observatorio» | identidad + guard conceptual | ✅ **RESUELTO** DEC-0012 | ver §1 |
| 2 | SIAP → QUADRUM → QUIRA | genealogía | memoria histórica | testimonio Javo 2026-08-25 |
| 3 | «define el OBJETO, no a QUIRA» | meta-regla ontológica | **C** | sólo en BOOT |
| 4 | Seccionales 29-NOV-2026 | estado estratégico temporal | §AHORA | testimonio Javo 2026-08-25 |
| 5 | «no congelar teoría antes que el grafo hable» | regla metodológica | **B — tuvo rango** | ver §5 |
| 6 | «Inventario de Conceptos → DERIVA» | regla de procedimiento | **B** | ver §6 |
| F | F1/F2/F3 | taxonomía de fases | ✅ **RESUELTO** — ADR-041 §4 ya la declara | ver §F |

## §1 · RESUELTO el 2026-08-26 · DEC-0012

> **La Constitución ya lo decía.** No hizo falta enmendarla ni crear canon: hizo falta **leerla**.
>
> | fuente | qué ya establecía |
> |---|---|
> | Preámbulo | «QUIRA es una plataforma de inteligencia pública… **infraestructura de conocimiento verificable**» |
> | Art. 8 | su función es «**exclusivamente** organizar, preservar e interpretar evidencia» |
> | Art. 14 | «Interfaces: … **observación** …» — la observación **ya figuraba como interfaz** |
> | Cierre | «Su identidad **no reside en sus interfaces**» |
>
> Los dos artefactos de `governance/` no necesitaban una decisión nueva: **contradecían a su propio
> padre en el árbol de autoridad**, y el Art. 20 exige que todo derivado sea compatible. Corregirlos
> no alteró canon — lo restituyó. Los artículos de la Constitución **siguen intactos**.
>
> Lección para las seis restantes: **antes de preguntar qué autoridad hace falta, comprobar si la
> autoridad existente ya lo cubre.** Este caso parecía necesitar rango constitucional nuevo y sólo
> necesitaba lectura.

*El diagnóstico original se conserva abajo porque explica por qué se propagaba.*

**No era que faltara una frase en la Constitución. Era que dos capas se contradecían.**

    governance/GOVERNANCE_CHARTER.md:176    «QUIRA ES un Observatorio Nacional…»
    governance/HOJA_DE_RUTA_MAESTRA.md:23   «QUIRA ES un OBSERVATORIO NACIONAL…»  (Javo · 2026-06-12)
    governance/BOOT.md                      «⛔ NO es auditoría ni observatorio»   (Javo · 2026-08-05)

La corrección de agosto **nunca bajó a los artefactos de junio**. Javo (2026-08-25):

> *«Es para que Claude, cuando construye, no siga degradando a QUIRA a una simple auditoría o al
> observatorio, como ha propagado en muchos documentos.»*

Tenía razón, y la causa es material: un constructor que lee `governance/` encuentra **escrito** que
QUIRA es un observatorio. No lo inventa — lo lee.

**Pero la proposición NO es canon inexistente: ya se ejecuta.**

    views/login_view.py:555          «QUIRA es una infraestructura de conocimiento verificable
                                      para la gestión pública territorial»   ← el landing
    app/viz/render/plan_render.py:836  la atribuye a CONSTITUCION-001
    scripts/ci/check_epistemico.py:79  detector: «no auditoría (CONSTITUCION-001)»

El código **ya la trata como norma constitucional**; ~~lo que falta es que el texto de la
Constitución la contenga~~.

> ⛔ **ESA ÚLTIMA FRASE ERA FALSA, y se conserva tachada a propósito.** El texto constitucional
> **sí la contenía** —Preámbulo, Art. 8, Art. 14, Cierre— y nadie lo había comprobado: se dio por
> hecho que faltaba porque la búsqueda de una formulación literal no la encontró. Es, una vez más,
> **coincidencia textual ≠ contenido**, esta vez en sentido inverso: no un falso positivo, sino un
> falso vacío. Verificar que algo falta exige el mismo rigor que verificar que está.

Dato que sigue vigente: `check_epistemico.py` **detecta pero no bloquea, y no está enganchado a
CI** — hoy depende de que alguien lo corra a mano.

⚠️ **Y aquí aplica la misma regla que a §5, por simetría: que el código la ejecute no la convierte
en canon.** Es evidencia de que se la trata como tal —fuerte, porque está en el producto que ve el
ciudadano—, no de que alguien la decidiera con la autoridad para hacerlo. Que `plan_render.py:836`
la atribuya a `CONSTITUCION-001` es una **atribución hecha desde el código**, exactamente el mismo
género de vínculo no verificado que este registro documenta en BOOT. La diferencia con #5 es de
grado, no de naturaleza: allí la evidencia es histórica, aquí es operante.

## §5 · Tuvo rango — y eso es evidencia, no vigencia

Consta que lo tuvo:

    governance/historico/BOOT_2026-06-17.md        Regla de Oro #4
    governance/historico/QUIRA_STATE_2026-06-03.md Regla #6

Dejó de figurar cuando `CLAUDE.md` reescribió las nueve. **Eso no la devuelve al canon**: no hay
constancia de que su salida fuera una decisión, ni de que fuera un descuido. Ambas lecturas caben
en la evidencia, y elegir entre ellas es gobernanza, no lectura.

Lo que sí cambia respecto a una proposición nueva: **restaurar y crear no son la misma decisión**
ni requieren la misma deliberación. El precedente informa; no resuelve.

**ADR-019 no es su fuente: es su caso de aplicación.** El texto original decía *«ADR-019 a propósito
en SUPPORTED»*; el ADR sigue hoy en `STRONGLY_SUPPORTED`, mantenido sin confirmar como demostración
viva de la regla. Al comprimirse, el paréntesis pasó a leerse como atribución de autoría.

## §6 · Artefacto autorizado ≠ regla que ordena usarlo

`marco_teorico/INVENTARIO_CONCEPTOS_FUNDACIONALES.md` — `INVENTARIO-CONCEPTOS-001`, `status:
vigente`, autoridad `MARCO-TEORICO-001`, 13.651 b. **BOOT lo referencia 0 veces.**

La regla «consultarlo antes de definir» no está ni en él ni en `CLAUDE.md`. Son **dos objetos
normativos distintos**: el artefacto tiene autoridad; la regla que obliga a consultarlo, no.

Restricción medida para esa decisión: **`CLAUDE.md` está en 3944 / 4000 bytes.** La vía «meterla
entre las Reglas de Oro» está cerrada hoy sin podar `CLAUDE.md` primero.

## §F · RESUELTO el 2026-08-26 · ~~«aquí BOOT fabrica canon»~~ — **la acusación era mía y era falsa**

> ⛔ **ESTE APARTADO CONTENÍA UNA ACUSACIÓN FALSA CONTRA BOOT. Se conserva corregido, no borrado.**

Decía que BOOT «presta el sello de un ADR que no la contiene». **Es al revés: BOOT cita
correctamente.** Buscando `F1`, `F2`, `F3` como cadenas no las encontré en ADR-041, y de ese vacío
concluí fabricación de canon. Al **leer el ADR completo**, la taxonomía está en su **§4**, con otra
nomenclatura:

| BOOT abrevia | ADR-041 §4 declara |
|---|---|
| F1 = Observatorio · Ciudadana (ENTRADAS de evidencia) | **Fase 1** = Observatorio · QUIRA Ciudadana — «construir la evidencia» |
| F2 = Institucional · Cooperación · Impact | **Fase 2** = Cooperación / Impact · Institucional |
| F3 = Economic | **Fase 3** = QUIRA Economic |
| Operaciones NO es producto | «Operaciones desaparece de la lista de productos. Nunca lo fue» |

Y **ADR-043 §7 lo ratifica sin ambigüedad**: *«El orden de fases lo fija ADR-041 §4.»* La autoridad
existe, está sellada (Javo · 2026-08-07) y deriva de `CONSTITUCION-001`.

**No había desalineación siquiera: sólo una abreviatura.** «F1» por «Fase 1».

### Por qué este error importa más que los otros

Es la **quinta vez** en la sesión que se confunde coincidencia textual con presencia semántica —y
la primera en que el resultado fue **acusar a un artefacto de fabricar autoridad**. El registro
escrito para impedir que se invente canon estuvo a punto de provocar que se «corrigiera» una cita
que era correcta.

    buscar la etiqueta   → no aparece → concluir que no existe   ⛔
    leer la proposición  → aparece con otro nombre → verificar   ✅

Es exactamente la regla que el colega formuló antes de esta ronda, y que evitó el daño:

> *«No busques "F1/F2/F3"; busca la proposición semántica que F1/F2/F3 pretende representar.»*

**Única mejora pendiente, y es menor:** BOOT cita «ADR-041 (sellado)» sin apuntar al §4. Añadir la
sección haría la cita verificable en un paso en vez de dos. No es un defecto de autoridad.

## Lo que esta ronda enseñó, y conviene no repetir

| error | cómo se manifestó |
|---|---|
| identificador ≠ contenido | 4 proposiciones «tenían destino»; el destino sólo tenía la etiqueta |
| coincidencia textual ≠ recuperación | «elecciones» apareció… hablando del 17-ago-2025, otro contexto |
| búsqueda literal → falso negativo | dije que ADR-023 no decía «recalcular»; sí lo dice |
| **inferir una negación** | de «era el Diplomado CAF» concluí que las elecciones no existían, y **borré un dato correcto**. La ausencia de confirmación no autoriza a concluir la negación |

Ese último es el más grave, porque es el error que QUIRA persigue afuera, cometido adentro y sobre
el testimonio del propio fundador.

## Decisiones pendientes — ninguna la toma este registro

1. ~~¿La corrección de agosto (#1) baja a `GOVERNANCE_CHARTER` y `HOJA_DE_RUTA_MAESTRA`?~~
   ✅ **DEC-0012** (2026-08-26). Javo autorizó tocar lo aprobado para subsanar.
2. ~~¿#1 se escribe en la Constitución que el código ya cita?~~ ✅ **No hizo falta: ya estaba**
   (Preámbulo · Art. 8 · Art. 14 · Cierre). La Constitución no se enmendó.
3. ¿`check_epistemico` pasa de detector a gate de CI? — **sigue abierta**
4. ¿#5 se **restaura** como Regla de Oro, o se eleva a ADR propio?
5. ¿#6 se convierte en regla, o basta con que BOOT apunte al artefacto vigente?
6. ~~¿La taxonomía F1/F2/F3 se lleva a ADR-041/043, o BOOT deja de atribuírsela?~~
   ✅ **Ninguna de las dos: ADR-041 §4 ya la declara** y ADR-043 §7 remite a él. La atribución de
   BOOT era correcta; el error era mío. Sólo se precisó la cita a «ADR-041 §4».
7. ¿Dónde vive la genealogía (#2) y la meta-regla ontológica (#3)?

### Trazabilidad de los cierres — el contador no basta

*(colega: «un estado agregado sin trazabilidad vuelve a introducir el problema que intentamos
eliminar»; el número tiene que poder reconstruirse)*

| decisión | caso | resuelta por | qué autoridad la cubría | acción derivada |
|---|---|---|---|---|
| 1 y 2 | #1 identidad | **DEC-0012** (2026-08-26) | `CONSTITUCION-001` Preámbulo · Art. 8 · Art. 14 · Cierre | corregidos `GOVERNANCE_CHARTER §4.4` y `HOJA_DE_RUTA §0`; Constitución **sin enmendar** |
| 6 | F1/F2/F3 | lectura de ADR-041 (2026-08-26) | **ADR-041 §4**, sellado 2026-08-07, y `ADR-043 §7` que remite a él | BOOT precisa la cita a «§4»; se retiró una **acusación falsa** del propio registro |

    ABIERTAS: 4     (3 · check_epistemico como gate · 4 · #5 · 5 · #6 · 7 · genealogía y meta-regla)

**Hasta que se resuelvan, `§AHORA` no debe podarse más.** Con 564 bytes de margen el espacio dejó
de ser el problema; la integridad de autoridad no. La siguiente modificación de BOOT debería venir
**después** de una decisión de gobernanza, nunca antes.

## Fuera de alcance — un frente distinto, anotado para que no contamine éste

Al escribir este registro apareció que la Constitución Institucional declara **dos numeraciones
incompatibles** (Art. 0-30 y Art. 1-21, oficial la B, derogada la otra). Hay **105 artefactos** con
`constitution_articles` en su cabecera.

    105 artefactos → constitution_articles → ¿numeración A o B?
                  → ¿artículo vigente? → ¿referencia realmente aplicable?

Podría ser una **clase completa de falsos vínculos de autoridad** — la misma familia de todo lo
hallado aquí: referencias que parecen válidas porque el identificador existe. **No se ha medido.**

⛔ No pertenece a este registro y no debe mezclarse con las siete decisiones de arriba: aquéllas son
proposiciones individuales; esto sería una auditoría transversal del árbol. Se anota para que no se
pierda, no para resolverse aquí.

---
*Registro de autoridad · Dylus Lab © 2026 · reúne evidencia, no decide canon.*
