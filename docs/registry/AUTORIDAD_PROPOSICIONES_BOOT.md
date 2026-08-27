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
| el código ejecuta #1 en el producto | eso demuestra **tratamiento**, no decisión originaria |

> ⛔ **DOS DE LOS TRES COROLARIOS ORIGINALES ERAN FALSOS.** Se retiran con constancia, porque el
> modo en que fallaron enseña más que el principio que ilustraban:
>
> | corolario retirado | por qué era falso |
> |---|---|
> | *«ADR-041/043 no transfieren autoridad a F1/F2/F3»* | `ADR-041 §4` **sí declara** la agrupación en fases (§F) |
> | *«que el Inventario esté vigente no hace vigente la regla»* | la regla **está escrita dentro del propio Inventario**, línea 33 (§6) |
>
> El principio general de ambos era correcto —autoridad sobre X no se transfiere a Y—, **pero
> ninguno de los dos casos lo demostraba**. Y los dos fallaron por la misma causa: se afirmó qué
> contenía un artefacto **sin haberlo leído entero**.
>
> Ilustrar una regla verdadera con un caso falso no sólo la deja sin apoyo: **la hace parecer
> demostrada**. Es una forma más de fabricar autoridad, y la cometió el registro escrito para
> impedirlo.

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
| 2 | SIAP → QUADRUM → QUIRA | genealogía | ⏳ **evidencia conservada**, rango sin decidir | `docs/registry/GENEALOGIA_QUIRA.md` |
| 3 | «define el OBJETO, no a QUIRA» | meta-regla ontológica | ✅ **RESUELTO** — la Constitución la cubre | ver §2 y §3 |
| 4 | Seccionales 29-NOV-2026 | estado estratégico temporal | §AHORA | testimonio Javo 2026-08-25 |
| 5 | «no congelar teoría antes que el grafo hable» | regla metodológica | **B — el caso GENUINO** | ver §5 |
| 6 | «Inventario de Conceptos → DERIVA» | regla de procedimiento | ✅ **RESUELTO** — regla propia del artefacto | ver §6 |
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

## §2 y §3 · EVIDENCIA PREPARADA (2026-08-26) — no decidida

> Javo pidió **preparar la evidencia**, no resolver. Lo que sigue es lo que se comprobó, con sus
> rutas. **Ninguna de las dos queda decidida aquí.**

### ⚠️ Primer hallazgo: la decisión 7 agrupaba dos casos de naturaleza distinta

Se unieron porque ambas preguntan *«dónde vive esta memoria»*. Al reunir la evidencia resulta que
**no comparten respuesta**:

| | #3 meta-regla ontológica | #2 genealogía |
|---|---|---|
| ¿autoridad viva que la cubra? | ✅ **sí** | ⛔ **no** |
| qué queda por hacer | corregir un puntero | decidir dónde vive |
| quién puede resolverlo | ya está resuelto en el canon | **sólo Javo** |

Agruparlas fue razonable con la información de entonces; mantenerlas juntas ahora haría que una
resolviera a la otra por arrastre — exactamente lo que el colega advirtió para #5.

### §3 · «define el OBJETO, no a QUIRA» — CUBIERTA por autoridad existente

`identity/CONSTITUCION_INSTITUCIONAL.md`, §*Relación con la Constitución Ontológica*:

> *«La Ontológica define el **objeto observado** (el GAD, sus 4 macroejes y 13 dominios); esta
> define el **sujeto observador** (QUIRA y su gobernanza del conocimiento). Ambas son L0.»*

Cubre la proposición **y dice más** que BOOT: no sólo que la Ontológica no define a QUIRA, sino
qué define cada una de las dos. **Cuarto caso** resuelto por autoridad preexistente.

**Defecto colateral medido — BOOT dice «12 dominios», el total vigente es 13.** Y no es error de
nadie: la Ontológica lo explica en su L292 —*«13 DOMINIOS (12 originales + d13 Ambiente vía
Mutabilidad)»*—. Ambos números son correctos en su contexto; BOOT declara **el original donde
debería declarar el vigente**. Otro caso de referencia que sobrevivió al cambio de lo referido.

### §2 · genealogía SIAP → QUADRUM → QUIRA — rastro sólido, hogar inexistente

Lo que Javo declaró (2026-08-25) tiene respaldo documental, y más del que él recordaba:

| evidencia | qué prueba |
|---|---|
| `docs/corpus_externo/Metodologia SIAP-ICPI Final.md` | *«SIAP-ICPI v2.0 · Sistema de Integridad Algorítmica y Planificación Intersistémica · **QUADRUM GovTech** · Ronald Javier Delgado Santana · Abril 2026»* — **el documento fundacional, firmado con el nombre antiguo** |
| `QTMP` = **Q**uadrum **T**erritorial **M**eta-**P**attern | QUADRUM **no desapareció: vive fosilizado en vocabulario canónico actual** (`CLAUDE.md` Regla 2 lo protege del firewall) |
| `H36_QUADRUM_BRIDGE` | una hoja del Gold Master lleva el nombre antiguo |
| `docs/ciudadana/TERRA_*_origen.md` | ~230 KB de especificaciones de la etapa **TERRA** |

**Pero ninguno es un registro de genealogía, y ninguno tiene frontmatter de autoridad.** Existe el
rastro; no existe la declaración. Es memoria dispersa en artefactos cuyo propósito era otro.

⚠️ **Y la memoria se está perdiendo mientras tanto**: Javo escribió *«Quadrum (no sé, se construyó
algo con ese nombre antiguo)»* — el fundador ya no recuerda con certeza qué fue, y el documento que
lo prueba lleva su propia firma. **Ésa es la razón para que la decisión no espere indefinidamente**,
y es un dato, no una opinión.

**Candidatos de hogar, sin recomendar ninguno:** `marco_teorico/MARCO_TEORICO_QUIRA.md`
(`MARCO-TEORICO-001`, vigente) · `governance/historico/` (existe y se usa) · un registro nuevo.
Elegir es gobernanza.

## §5 · El caso GENUINO — test A+B+C+D, y no lo resuelve la autoridad existente

Tras tres casos consecutivos resueltos por autoridad preexistente, éste **no**. Y eso importa:
si los cuatro se hubieran resuelto igual, habría que sospechar que se están forzando las
equivalencias.

| | pregunta | resultado |
|---|---|---|
| **A** | ¿existe hoy una formulación viva? | ⚠️ **sólo aplicada a un caso**, no como regla |
| **B** | ¿tiene autoridad declarada? | ✅ `ADR-019` es ARQUITECTONICA |
| **C** | ¿esa autoridad cubre la **regla metodológica**? | ⛔ **NO** |
| **D** | ¿la evidencia histórica demuestra una **decisión** de rango? | ⛔ demuestra **uso**, no decisión |

### Lo único vivo que existe: una aplicación, no la norma

`ADR-019` §Decisión Provisional, punto 5:

> *«**No renombrar Dom08 ni Dom09** — los nombres canónicos permanecen **hasta que el grafo
> hable**.»*

Usa la fórmula, y **eso confirma con cita textual lo que este registro ya sostenía**: ADR-019 es el
**caso de aplicación** de la regla, no su fuente. Aplica la regla a Dom08/Dom09 mientras el propio
ADR sigue en `STRONGLY_SUPPORTED`; no la establece como norma general del sistema.

*(Nota: la búsqueda anterior de «congelar» en ADR-019 dio 0 y de ahí se concluyó que no la
contenía. La contenía —con otra formulación—. Otro falso vacío, el sexto de la sesión.)*

### La equivalencia que NO se aceptó, y por qué se declara

`governance/GOVERNANCE_CHARTER.md:148` dice: *«el Authority Graph evoluciona por necesidad real,
**no por completitud teórica**»*. Suena a la misma regla y **no lo es**: habla del **grafo de
autoridad documental** y de no inflarlo para subir una métrica. #5 habla de **diferir la teoría
hasta que la evidencia estructural la sostenga**. Parientes, no equivalentes.

⚠️ **Aceptarla habría producido un cuarto «resuelto por autoridad existente» falso** — y con él, una
confirmación falsa de la hipótesis que la sesión venía verificando. La presión para encontrar el
patrón otra vez es exactamente lo que hace peligrosa la cuarta comprobación.

### Qué queda, entonces

| consta | no consta |
|---|---|
| fue Regla de Oro #4 (`BOOT_2026-06-17`) y #6 (`QUIRA_STATE_2026-06-03`) | que su salida de las nueve fuera una **decisión** |
| `ADR-019` la aplica hoy a un caso concreto, con autoridad | que exista una **formulación general vigente** con autoridad |
| se sigue invocando en BOOT | que alguien le haya otorgado o retirado rango |

**Es el único de los cinco casos que requiere una decisión real de gobernanza**, y sigue siendo la
que este registro no toma: ¿se **restaura** (hay precedente) o se **eleva** a ADR propio (rango
distinto)? Restaurar y crear no son la misma decisión.

## §6 · RESUELTO el 2026-08-26 · la regla estaba dentro del propio artefacto

Test A+B+C del colega, y los tres dan positivo:

| | | |
|---|---|---|
| **A** | ¿existe el artefacto? | ✅ `marco_teorico/INVENTARIO_CONCEPTOS_FUNDACIONALES.md` |
| **B** | ¿tiene autoridad real? | ✅ `INVENTARIO-CONCEPTOS-001` · `status: vigente` · ← `MARCO-TEORICO-001` |
| **C** | ¿establece la regla de consultarlo? | ✅ **sí, en su línea 33** |

> *«**Regla:** antes de "crear" un concepto, **se consulta este inventario**. Si ya existe, se
> **declara y opera**, no se reinventa.»*

**No hacía falta convertirla en Regla de Oro ni elevarla a ADR.** La regla es **propia del artefacto
que la ejecuta**, y ese artefacto tiene autoridad vigente. Lo único que fallaba era el puntero:
BOOT la presentaba como una de «las 9 que viven en `CLAUDE.md`», y no está entre ellas.

### El defecto que apareció al verificar: citas por número a una lista renumerada

La regla se citaba a sí misma como *«Regla de Oro 6: deriva, no redefinas»*. Pero:

    Regla de Oro 6 HOY  =  «Repo PRIVADO. Credenciales solo en secrets.toml»

Dos artefactos vigentes —`INVENTARIO_CONCEPTOS_FUNDACIONALES` y `DESCUBRIMIENTO_NORMATIVO_ADR031`—
citaban ese número. La lista se renumeró y las citas quedaron apuntando a otra regla. Corregidas
para que apunten a la autoridad real, dejando constancia de qué decían.

⚠️ **Tercer caso del mismo patrón**, y ya no parece casualidad:

    Constitución       dos numeraciones (Art. 0-30 · Art. 1-21) → `constitution_articles` dudosos
    ADR-041            frontmatter «APROBADO» · pie «sin sellar»
    Reglas de Oro      citas por número a una lista que se renumeró

**Las referencias por número sobreviven a los cambios de la lista que numeran.** Es la misma
familia que el resto de la sesión: el vínculo *parece* válido porque el identificador existe.

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
3. ~~¿`check_epistemico` pasa de detector a gate de CI?~~ ✅ **Sí, y el trabajo no fue
   engancharlo sino hacerlo enganchable.** `--estricto` ya existía; lo que faltaba era que
   no bloqueara por ruido. Auditadas sus 4 señales una a una: **las 4 eran falsos
   positivos**. Se separó ⛔ERROR (viola el canon · bloquea) de ·SEÑAL (pregunta de juicio ·
   nunca bloquea), y el gate vive ahora en `tests/test_nivel_epistemico.py` — importado, no
   lanzado, para no cruzar la frontera de efectos de 4-ter.
4. ¿#5 se **restaura** como Regla de Oro, o se eleva a ADR propio?
5. ~~¿#6 se convierte en regla, o basta con que BOOT apunte al artefacto vigente?~~
   ✅ **Ninguna de las dos: la regla YA está escrita dentro del artefacto** (`INVENTARIO_CONCEPTOS_
   FUNDACIONALES.md:33`). No hizo falta crear Regla de Oro ni ADR. BOOT ahora apunta a su hogar.
6. ~~¿La taxonomía F1/F2/F3 se lleva a ADR-041/043, o BOOT deja de atribuírsela?~~
   ✅ **Ninguna de las dos: ADR-041 §4 ya la declara** y ADR-043 §7 remite a él. La atribución de
   BOOT era correcta; el error era mío. Sólo se precisó la cita a «ADR-041 §4».
7. **DESAGREGADA** al reunir la evidencia — eran dos casos distintos:
   · **#3** ✅ cubierta por `CONSTITUCION_INSTITUCIONAL` §Relación con la Ontológica. Corregido de
     paso: BOOT decía «12 dominios», el vigente es 13 (12 + d13 vía Mutabilidad). Las tres
     autoridades ya coinciden.
   · **#2** ⏳ **sigue abierta.** La evidencia se conservó en `docs/registry/GENEALOGIA_QUIRA.md`
     —porque el fundador ya no la recuerda y la fuente se erosiona— pero **conservar no es
     decidir**: dónde vive canónicamente y con qué rango lo decide Javo.

### Trazabilidad de los cierres — el contador no basta

*(colega: «un estado agregado sin trazabilidad vuelve a introducir el problema que intentamos
eliminar»; el número tiene que poder reconstruirse)*

| decisión | caso | resuelta por | qué autoridad la cubría | acción derivada |
|---|---|---|---|---|
| 1 y 2 | #1 identidad | **DEC-0012** (2026-08-26) | `CONSTITUCION-001` Preámbulo · Art. 8 · Art. 14 · Cierre | corregidos `GOVERNANCE_CHARTER §4.4` y `HOJA_DE_RUTA §0`; Constitución **sin enmendar** |
| 6 | F1/F2/F3 | lectura de ADR-041 (2026-08-26) | **ADR-041 §4**, sellado 2026-08-07, y `ADR-043 §7` que remite a él | BOOT precisa la cita a «§4»; se retiró una **acusación falsa** del propio registro |
| 5 | #6 Inventario | lectura del artefacto (2026-08-26) | `INVENTARIO-CONCEPTOS-001` — **la regla está en su línea 33** | BOOT apunta al hogar real; corregidas 2 citas a una «Regla 6» renumerada |
| 3 | `check_epistemico` | auditoría señal por señal (2026-08-26) | ninguna nueva — el modo `--estricto` ya existía | **gate SELECTIVO**: bloquea sólo ⛔ERROR; ·SEÑAL queda como revisión humana |

> ⚠️ **La decisión 3 NO es «el detector pasó a ser gate».** La formulación precisa, y conviene que
> sobreviva a esta sesión: *se convirtió un detector epistemológico en un **gate selectivo**, que
> bloquea únicamente lo clasificado `ERROR` y conserva `SEÑAL` como materia de revisión humana.*
> Sin ese matiz, dentro de unos meses alguien leerá «gate» y supondrá que toda señal epistémica
> detiene el trabajo. El motivo de esa arquitectura está medido: **el primer conjunto de señales
> tenía 100 % de falsos positivos.** *(precisión del colega, 2026-08-26)*

    ABIERTAS: 2   ← #4 (=#5) y #7-parte-#2 · reconstruible, no declarado

| decisión | qué agrupa | por qué es UNA |
|---|---|---|
| ~~**3**~~ | ~~`check_epistemico` a gate~~ ✅ cerrada 2026-08-26 | — |
| **4** | **#5** «no congelar teoría» — restaurar o elevar | una sola proposición |
| **7** | **#2** genealogía SIAP→QUADRUM→QUIRA **y #3** meta-regla ontológica | ambas preguntan *dónde vive esta memoria*; se decide el criterio una vez y se aplica a las dos |

⚠️ **El contador se reconstruye desde esta tabla, no se declara.** Al cerrar #6 y F1/F2/F3 se
escribió en prosa «quedan #5, #3, #2/#7 y el gate» — cuatro elementos para un contador de tres,
porque **#3 se enumeró dos veces**: suelto y dentro de #2/#7. El número era correcto; la
enumeración no. *(colega, 2026-08-26: «todo número de estado debe poder reconstruirse desde sus
elementos, no sólo coincidir con ellos»)*

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
