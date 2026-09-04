# GM-Ω · EXPEDIENTE GENEALÓGICO DOCUMENTAL

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/genealogia_documental.py` barriendo `tesis historicas/documentos antiguos/`.

> ### Por qué existe
> Javo aportó la carpeta de documentos antiguos, y el primero que se abrió —`Metodologia_SIAP_ICPI.docx`, de abril, firmado **Ecosistema TERRA · Quadrum Gov Tech**— demostró que **abril contiene información que el corpus posterior no conserva**: la regla de `E_i` que esta auditoría había declarado `NOT_DETERMINABLE`.
>
> **Regla del barrido:** reconstruir la cadena entera **antes** de reescribir ningún diagnóstico. Corregir `007-B0` con el primer documento y volver a corregirlo con el segundo dejaría dos versiones de la misma historia en el expediente.

## ★ El hallazgo que abrió el barrido · `E_i` tiene DOS definiciones

| | Definición **A** | Definición **B** |
|---|---|---|
| Documento | `Metodologia_SIAP_ICPI.docx` (abril · TERRA/QUADRUM) | `metodologia.docx` (tesis) |
| Nombre | **Autonomía Orgánica** | **Fricción de Autonomía** |
| Qué mide | «el **control del director** sobre la ejecución de la meta» | fricción institucional por **delegación** |
| Escala | `1.0` autónomo · `0.9` compartido · `0.75` difuso | `1.0` directa · `0.90` convenio · `0.75` adscrita |
| Base | — | `COOTAD Art. 54` · `NCI 200-04` |

**Misma escala numérica, constructos distintos.** Y el motor declara la definición **A**, textualmente, en `H12!A4`:

```
Ei: 1.0=autónomo | 0.9=compartido | 0.75=difuso
```

### ⚠️ Qué corrige esto, y qué NO

| | |
|---|---|
| **CORRIGE** | `007-B0` concluyó que «la regla escrita y los valores implementados nunca coincidieron». Lo que ocurrió es que **la auditoría contrastó los valores contra la definición B mientras el motor implementa la A**. Los cinco casos de entidades adscritas con `E_i ≠ 0,75` no eran incoherencia: eran la respuesta correcta bajo la regla que el motor sí declara |
| **NO CORRIGE** | que la aplicación meta a meta siga sin verificarse. Comprobar que los 25 valores cumplen la definición A exige conocer el «control del director» por meta, y eso no consta en el libro |

**Estado nuevo de `E_i`** — cuatro capas que no deben colapsarse:

```
  REGLA                        VERIFICADA      · abril + H12!A4
  VALORES DEL MOTOR            VERIFICADOS     · 25 literales, estables
  APLICACIÓN META A META       PENDIENTE       · falta el insumo
  CORRESPONDENCIA VALOR↔REGLA  POR AUDITAR     · no se puede hoy
```

⚠️ **La definición B no se descarta.** No era basura: pasa a ser **evidencia de divergencia o evolución metodológica entre documentos**. Cuál rige lo dictamina `011`, no este expediente.

Y coincide con la corrección que Javo hizo el 2026-09-03 —*«castigar al GAD por derivar una obra a EP Aseo no es viable: es la misma institucionalidad»*—: **la definición A no penaliza el organigrama, mide el control del director.** Su criterio coincidía con la metodología original, no con la tesis.

## ★ Y el ICPI original tenía CINCO factores

`QUADRUM_ICPI_Calculadora.csv` conserva la construcción primitiva:

```
  PRODUCTO     = Pi × Vi × Ei × Ti × Ri      ← CINCO · sin C_i
  Pi           = PRESUPUESTO_ASIGNADO / PRESUPUESTO_TOTAL
  Ri           = 0.5 · 1 · 1.5               ← sin normalizar por 1,725
  DENOMINADOR  = Pi × Ri                     ← igual que hoy
```

Luego la evolución documentada es:

```
  ICPI_original = Pi · Vi · Ei · Ti · Ri            (abril · 5 factores)
  ICPI_actual   = Pi · Ri · Vi · Ei · Ti · Ci       (v5.7 · 6 factores)
```

**`C_i` no es parte del constructo original: es una incorporación posterior.** Eso reformula `011-C`, que ya no debe preguntar sólo si está bien multiplicar seis factores, sino:

> **¿Qué transformación metodológica ocurrió entre el ICPI original y el actual, qué constructo representa cada versión, y está justificada la incorporación de `C_i` y la arquitectura algebraica resultante?**

⚠️ Y `R_i` también cambió de representación —de `0.5·1·1.5` crudo a normalizado por el máximo teórico—. **Eso entra en la genealogía de `R_i`, no se trata automáticamente como error.**

## ★ La UNIDAD DE ANÁLISIS está declarada — y hay que leerla con cuidado

`ICPI.docx` (la tesis) la declara explícitamente:

> **Unidad de Análisis:** el **flujo informativo y programático** en la trayectoria `Plan de Trabajo → PDOT → POA → SIGAD` del GAD Municipal de Montecristi.

⚠️ **Pero eso NO responde todavía a `011-A`, y confundirlo sería el error de siempre.** Son dos cosas distintas:

| | |
|---|---|
| **Unidad de análisis de la INVESTIGACIÓN** | qué fenómeno se estudia → el flujo/trayectoria. **Declarada** |
| **Unidad `i` de la FÓRMULA** | qué objeto se indexa en `Σ` y recibe `P·R·V·E·T·C`. **Sigue sin declararse** |

Que la tesis diga «estudio el flujo» no dice si `i` es una meta, un agregado o una unidad programática. **Es material valioso para `011-A`, no su respuesta** — y tratarlo como respuesta sería colapsar el objeto de estudio con el objeto de cálculo.

## `C_i` · su origen conceptual

`memoriaa algo quira.docx` lo enlaza con la doctrina fundacional:

> **Responsabilidad Orgánica Vinculante (`C_i`)** → «✅ VIVO como… `H07c`: firma del Director activa `Ti_V`»

Coincide con `TERMINOLOGY_ORIGIN_v1.md`, que lo define como *«la obligación técnica y legal de que cada meta de inversión esté ineludiblemente anclada a una unidad administrativa específica […] el antídoto contra la burocracia diluida»*. `C_i` **sí tiene genealogía conceptual documentada** — lo que no tiene es presencia en el ICPI original de cinco factores.

## ⚠️ El barrido de los dos documentos grandes dio NEGATIVO

`historico construccion quira.docx` (358 KB · 6.194 párrafos) y `memoriaa algo quira.docx` (74 KB) son **historiales de construcción del software**, no documentos metodológicos: sprints, QLEP, Neo4j, GeoTwin, TERRA Ciudadana. Se buscaron en ellos:

| Buscado | Resultado |
|---|---|
| Primera aparición de la **fórmula de 6 factores** | ❌ nada |
| Primera aparición de la **fórmula de 5 factores** | ❌ nada |
| **Definición operacional de `i`** | ❌ nada |
| Incorporación de `C_i` al producto | ❌ sólo su concepto, ya conocido |
| Transición TERRA/QUADRUM → QUIRA | 🟡 menciones, sin decisión metodológica |

**Es un resultado, no un fracaso.** Lo que establece es que **el documento que explica la transición del ICPI de cinco a seis factores no está en este corpus**. Y la consecuencia es la que el asesor anticipó:

> Si los documentos históricos tampoco resuelven qué representa `i`, entonces **`011-A` tiene que decidirlo** — no descubrirlo. Y fabricar una definición retrospectiva para que la fórmula parezca más coherente de lo que era sería el peor desenlace posible.

## ★★★ EL ÚLTIMO HUECO, CERRADO · `C_i` entró el 27-ABR-2026

No estaba en ningún documento externo: **estaba en el propio Gold Master**, fechado y firmado. `H01!A94`:

> ★ **`Ci` DETERMINISTA v1.0 (Javo Delgado Santana, 27-Abr-2026)**: `Ci` arranca en 1.00. Deducciones legales Sección L calculan `Ci` final. `Ci_Base` columna E es FÓRMULA de Sección M — NO hardcodeado.

Y `H01!A172` declara el constructo completo:

> ★ **MOTOR DETERMINISTA `Ci`: abandona valoración heurística.** `Ci = MÁX(0.50, 1.00 − Σ penalizaciones)`. Marco legal: **LOSNCP + COPFP + CGE + CPCCS**. **Principio de inocencia: todo proceso nace `Ci=1.00`.**

| | |
|---|---|
| **Qué es** | `H01!A93` · «TABLA Ci — **Calidad de Proceso Orgánico por meta**» |
| **Fecha** | **27 de abril de 2026** |
| **Autor** | Javo Delgado Santana |
| **Fórmula** | `Ci = MÁX(0.50, 1.00 − Σ penalizaciones)` |
| **Marco legal** | LOSNCP · COPFP · CGE · CPCCS |
| **Principio** | **inocencia** — todo proceso nace en 1.00 |
| **Evolución declarada** | «abandona valoración heurística» → de `Ci_Manual_2025` a motor determinista |

### La ventana se cierra a 24 días

```
  3-abr-2026   ANEXO L QUADRUM v5.0   → 5 factores · SIN C_i
 27-abr-2026   Ci DETERMINISTA v1.0   → entra C_i · 6 factores
 10-may-2026   primer Gold Master conservado (ECIAP v1.1)
```

**`C_i` no fue una incorporación silenciosa ni sin fundamento.** Tiene fecha, autor, fórmula, marco legal y un principio explícito. Lo que no existía era un **artefacto que lo reuniera** — vivía dentro de una celda de parámetros del Excel, y por eso trece documentos externos no lo encontraron.

### ⚠️ Y un hallazgo colateral: `C_i` opera hoy con su FALLBACK

`H01!A187` y `A215`:

> «INF-01..04 **VACÍOS al inicio** — los ingresa el analista SIAP-ICPI con evidencia. NUNCA inventar infracciones.» […] «`Ci_Manual_2025` = **REAL-HEURÍSTICO**. `Ci_Calculado` usa `Ci_Manual_2025` como **fallback** cuando no hay infracciones → preserva `ICPI_Axioma=69.9309%`»

Es decir: **el motor determinista existe pero no tiene infracciones cargadas**, así que `C_i` devuelve hoy los valores heurísticos de la calibración retrospectiva 2025 (`1.00`×11 · `0.90`×9 · `0.75`×5).

⚠️ **Y eso está bien hecho, no es un defecto**: la alternativa —inventar infracciones para alimentar el motor— es exactamente lo que `A187` prohíbe. El fallback es la forma correcta de decir «no hay evidencia de infracción» sin fabricarla. Lo que `011` debe juzgar es si un valor heurístico de 2025 es el fallback adecuado para 2026.

## ★★★ LA GENEALOGÍA DE `E_i`, RECONSTRUIDA

El `ANEXO L MANUAL TÉCNICO QUADRUM v5.0` —**3 de abril de 2026**, hallado en `ProyecT/Terra archivo historico/`— documenta la fórmula y la función que la implementa:

```
ICPI = [Σ(Vi × Pi × Ei × Ti × Ri) / Σ(Pi × Ri)] × 100

def calcular_ICPI_dinamico(promesas_df):
    - Vi: float (0.0, 0.5, 1.0) - Verificación documental
    - Pi: float               - Peso presupuestario normalizado
    - Ei: int (1-5)           - ENTIDAD CUSTODIO RESPONSABLE   ⚠️
    - Ti: float (0.0-1.0)     - Avance temporal
    - Ri: float (0.5-1.5)     - Relevancia constitucional
```

> **En abril, `E_i` no era un coeficiente: era un IDENTIFICADOR de entidad custodio —un entero de 1 a 5— multiplicándose dentro del producto.**

Y eso es matemáticamente incoherente: una meta ejecutada por la entidad `5` valdría **cinco veces** más que una idéntica de la entidad `1`, sin ninguna razón metodológica. El identificador entra en el cálculo como si fuera una magnitud.

### La transición está documentada · su MOTIVO no

⚠️ **Una versión anterior de este expediente escribió «ahí está por qué `E_i` cambió: alguien vio que multiplicar por un ID no tenía sentido».** Eso es una **hipótesis causal**, no un hecho: ninguna fuente dice que se cambiara por esa razón. Es la explicación elegante que va más allá de la evidencia — el mismo error que `DOC-009` y `DOC-019` persiguen.

**La formulación correcta:**

> La transición de `E_i` desde identificador de entidad hacia coeficiente **está documentada**; la **motivación causal** de esa transformación permanece **NO DETERMINABLE** salvo evidencia explícita.

Y la secuencia observada es ésta:

| # | Estado de `E_i` | Fuente | Fecha |
|---|---|---|---|
| 1 | `int (1-5)` · **identificador** de entidad custodio | `ANEXO L QUADRUM v5.0` | **3-abr-2026** |
| 2 | «Autonomía Orgánica» · `1.0 / 0.9 / 0.75` — **control del director** | `Metodologia_SIAP_ICPI` | abril |
| 3 | coeficiente `1 · 0.9 · 0.5` en 20 promesas | calculadora QUADRUM | s/f |
| 4 | «Fricción de Autonomía» · `COOTAD 54 · NCI 200-04` | tesis | s/f |
| 5 | `1 / 0.90 / 0.75`, citando **«autónomo/compartido/difuso»** | `H12!A4` + 25 literales | v5.7 |

El motor actual cita el estado **2**. La tesis describe el **4**. Y esta auditoría comparó los valores contra el 4 cuando el motor implementa el 2 — de ahí que «no cuadraran».

⚠️ **Límite de lo afirmado**: el `ANEXO L` **especifica** esa función; que llegara a ejecutarse con `Ei` entero no está demostrado. Lo demostrado es qué decía la especificación de abril.

## ★★★ Y LA FÓRMULA ORIGINAL SÍ TENÍA EL `× 100`

```
abril    ICPI = [Σ(Vi × Pi × Ei × Ti × Ri) / Σ(Pi × Ri)] × 100
v5.7     H12!B33 = B31/B32                              ← sin ×100
```

⚠️ **Y aquí también hay que frenar.** Una versión anterior llamó a esto «la pérdida de un factor». **El cambio de escala está demostrado; su carácter, no.** Hay dos lecturas y la evidencia no elige entre ellas:

| | |
|---|---|
| **A · cambio semántico intencional** | el motor pasó a almacenar el ICPI como **proporción** (`0,274582`) y la presentación lo convierte. No hay pérdida matemática: hay cambio de representación interna |
| **B · pérdida accidental** | `B33` pretendía ser porcentaje y el `×100` se eliminó sin actualizar superficies ni documentación. Entonces sí es un defecto de representación |

**Formulación correcta:**

> El `×100` presente en la especificación histórica no está en la expresión canónica actual de `B33`. **El cambio de escala interna está demostrado; su carácter intencional o accidental permanece pendiente de determinación.**

Lo que `007-X` sí probó es que **existe una inconsistencia real de rotulado** —69 cabeceras imprimen «0,27 %»—, y eso es compatible con ambas lecturas: en A sería un rótulo mal actualizado; en B, la huella del factor perdido. La capa API compensa (`H73!ICPI_GLOBAL_PCT = B33*100`) y por eso la UI publica bien.

## ★★★ `011-A` RESUELTO EN SU GENEALOGÍA · `i` era una PROMESA

El `ANEXO_M_ICPI_DINAMICO_PROFESIONAL` —«Formalización del Algoritmo ICPI Dinámico», febrero— formaliza:

```
ICPI(t) = [Σᵢ (Vᵢ(t) × Pᵢ × Eᵢ × Tᵢ(t) × Rᵢ) / Σᵢ (Pᵢ × Rᵢ)] × 100

«Si Vᵢ(t) = 0 → Contribución_PROMESA_i = 0»
«la regla de anulación documental garantiza que ausencia de evidencia
 invalida PROMESA independientemente de otros factores»
```

**`i` indexaba PROMESAS del Plan de Trabajo del CNE**, no metas del PDOT. Y la calculadora QUADRUM lo confirma desde el dato: su columna se llama `PROMESA_CNE` y sus identificadores son `A-001`…`A-020`.

### Y el motivo lo declara Javo

> **«Comenzamos tomando el plan CNE como promesa original; luego replanteamos con PDOT pues era mandato.»**
> — Javo, 2026-09-04

### ⚠️⚠️ CORRECCIÓN JURÍDICA · un error de esta auditoría

Esta dirección escribió que **«el plan de campaña no obliga jurídicamente»**. **Es falso**, y además contradice un dominio ya curado de QUIRA. Javo:

> **«El plan CNE SÍ es vinculante legalmente, es ley, su cumplimiento también. El plan CNE se funde en el PDOT, así lo establece la normativa —COPFP, COOTAD, ley electoral—. Eso quedó definido en `d03 Gobernanza del Mandato Electoral`.»**

El error es doble: afirmé una tesis de derecho ecuatoriano sin fuente, y lo hice **contra el canon del propio sistema** — `d03` existe precisamente para sostener la exigibilidad del mandato electoral. Si el Plan CNE no obligara, `d03` no tendría objeto.

**La formulación correcta del cambio de unidad no es jurídica, es metodológica:**

> La unidad evolucionó de la promesa electoral individual hacia la meta del PDOT porque el equipo decidió que la evaluación del cumplimiento debía anclarse en el **instrumento de planificación territorial que OPERACIONALIZA el mandato de gobierno**. Ambos instrumentos son vinculantes; el PDOT es donde el mandato se vuelve medible.

Y eso es exactamente lo que Javo declaró —«pues era mandato»— sin necesidad de inventarle una causalidad jurídica adicional.

Y explica por qué la tesis define la unidad de análisis como la **trayectoria** `Plan de Trabajo → PDOT → POA → SIGAD`: **la promesa no desapareció, se convirtió en el eslabón anterior.**

### ⚠️ TRES UNIVERSOS QUE NO SON INTERCAMBIABLES

| Universo | Cantidad | Naturaleza |
|---|---:|---|
| Plan de Trabajo CNE | **77** · **76** tras exclusión (`ADR-036 §5`) | promesas electorales |
| PDOT 2023-2027 | **66** | metas documentales |
| Gold Master v1 | **25** | unidades operacionales |

> **La coincidencia numérica histórica entre «66 promesas CNE» y «66 metas PDOT» NO constituye evidencia de identidad entre ambos universos.**

Y no es una precaución teórica: `PCD-D03` ya lo probó —

> «**46 de las 66 promesas no salieron del Plan CNE.** Nadie las ingestó: aparecieron. Tres mencionaban **otros cantones** (Sucre, Jaramijó, Crucita)» — detectadas por Javo, antes que ningún análisis.

Las «66 promesas» del índice histórico eran **espurias**. El número 66 coincidiendo en dos universos distintos fue una trampa real, y ya cazó a alguien una vez.

### Estado de `011-A`, en tres partes

| | Estado | |
|---|---|---|
| **011-A1** · genealogía de la unidad | ✅ **CERRADO** | `promesa CNE → meta PDOT`, con motivo `DECLARADO` por Javo |
| **011-A2** · unidad vigente del cálculo | 🔄 **POR FORMALIZAR** | opera con metas PDOT; el canon no lo declara |
| **011-A3** · relación con la unidad documental | ⛔ **PENDIENTE** | pasa a `011-B` · hay al menos un `N:1` demostrado |

`011-A2` necesita que el canon diga algo como: *«unidad operacional vigente del ICPI: meta PDOT individual identificada por su ID canónico del Gold Master»* — un acto, no una investigación.

> ### `DOC-023` · un cambio de unidad no es una inconsistencia
> **La evolución de la unidad `i` no debe interpretarse automáticamente como inconsistencia metodológica.** Un cambio de unidad puede ser una revisión conceptual válida si existen: una **razón metodológica explícita**, una **nueva definición operacional** y una **trazabilidad** que permita reconstruir la genealogía.
>
> Aquí se cumplen las tres. Lo que faltaba era la tercera, y este expediente la construye.

⚠️ Y una precisión sobre el alcance del `ANEXO M`: **no demuestra que el ICPI «siempre fue sobre promesas»**. Demuestra que **en esa versión de febrero** `i` era una promesa. La diferencia parece pequeña y es exactamente la disciplina que permitió encontrar todo lo demás.

## ★★ POR QUÉ NO HAY DOCUMENTO · la evolución fue conversacional

Javo lo aclaró y resuelve el hueco que 13 documentos no llenaron:

> **«La fórmula del ICPI vino evolucionando desde ENERO, cuando comenzamos a trabajar con Claude. Antes era sólo yo trabajando, pero al trabajar con Claude desde el chat —antes de Code— me pudo ayudar a potenciar la fórmula; por eso ha venido cambiando, es decir, evolucionado.»**
> — Javo, 2026-09-04

**No falta un documento: nunca hubo uno.** La entrada de `C_i`, el paso de cinco a seis factores y la renormalización de `P_i` y `R_i` **no están documentados porque ocurrieron en diálogo**, iterando sobre la tesis. El barrido no fracasó — buscaba en el sitio equivocado.

Y la primera iteración tiene nombre: el chat **«profundo»**, donde se sentaron las bases del ecosistema que hoy es QUIRA, partiendo de la tesis.

### Lo que esto corrige de esta auditoría

| Se venía diciendo | Lo que es |
|---|---|
| «el hueco es abril → mayo» | **el hueco empieza en ENERO** — abril es sólo donde aparece el primer artefacto conservado |
| «falta el documento que explica `C_i`» | **no existe tal documento**; la justificación vive en una conversación |
| «la divergencia nació con la implementación» (`007-B0`) | nació de una **evolución iterativa** que el canon no registró |

### Y la deuda que sí queda, nombrada · `DOC-022`

> **Una decisión que sostiene el motor y vive sólo en una conversación es una decisión fuera del canon.**

No es un reproche al método: iterar con Claude fue lo que potenció la fórmula, y el motor resultante funciona y está validado empíricamente. **La deuda es otra**: lo que el sistema ejecuta debe poder explicarse **desde el sistema**, no desde la memoria de quien lo construyó. Sin eso, `011` tiene que volver a decidir lo que ya se decidió una vez.

### Qué haría falta del chat «profundo», y para qué exactamente

No hace falta todo: hay **cuatro decisiones** cuya justificación está sin recuperar, y cada una tiene un destino concreto en la auditoría.

| Buscar | Para | Si no aparece |
|---|---|---|
| Por qué entró `C_i` | `011-C` | se decide de nuevo, y se declara decisión nueva |
| Por qué 5 → 6 factores | `011-C` | ídem |
| Por qué se renormalizaron `P_i` y `R_i` | `011-C` · `007-A` ya probó que la de `R` es inocua | ídem |
| Qué es `i` | `011-A` | **`011-A` decide**, no descubre |

⚠️ Y una salvedad de método: lo que aparezca en el chat será **evidencia de la decisión**, no canon por sí mismo. Para entrar al canon tendrá que declararse como lo que es —una decisión de diseño, con su fecha y su motivo— igual que cualquier otra.

## Tabla de genealogía

⚠️ **Las fechas salen del CONTENIDO, no del sistema de ficheros.** Donde no hay fecha fiable se escribe `NO DETERMINABLE`, nunca el `mtime`.

| Elemento | Versión histórica | Evidencia | Cambio | Justificación | Estado |
|---|---|---|---|---|---|
| `P_i` | `PRESUPUESTO_ASIGNADO / TOTAL` | calculadora QUADRUM | → normalizado Σ=1 sobre 25 | **no hallada** | 🟡 cambio documentado, motivo no |
| `R_i` | `0.5 · 1 · 1.5` crudo | calculadora QUADRUM | → normalizado por máximo 1,725 | **no hallada** | 🟡 ídem |
| `V_i` | 3 niveles con núcleo financiero | `H13!B16-B21` | regla anterior `suma≥2` → actual | ✅ **documentada en el libro** | 🟢 con límite de reconstrucción |
| `E_i` | **A**: control del director (abril) · **B**: fricción por delegación (tesis) | `Metodologia_SIAP_ICPI` · `metodologia.docx` · `H12!A4` | dos definiciones coexistentes | **no hallada** | 🟡 regla verificada, aplicación pendiente |
| `T_i` | ratio por entidad | `H07b` | curva de pacing sustituyó a `mes/12` | **no hallada** · la nota quedó desfasada | 🟡 |
| `C_i` | **ausente** del ICPI original | calculadora QUADRUM (5 factores) | **incorporación posterior** | ❌ **NO HALLADA** | 🔴 el hueco principal |
| `i` | «flujo informativo/programático» (unidad de INVESTIGACIÓN) | `ICPI.docx` | — | — | 🔴 unidad de CÁLCULO sin declarar |
| Fórmula | `Pi·Vi·Ei·Ti·Ri` (5) | calculadora QUADRUM | → `Pi·Ri·Vi·Ei·Ti·Ci` (6) | ❌ **NO HALLADA** | 🔴 |
| AVEP | eje conceptual → 4 niveles | `TERMINOLOGY_ORIGIN_v1` | → 5 niveles + fórmula `IF` ×11 hojas | 🟡 el incidente sí (`H01!A28`) | 🟡 |
| Universo | «muestra estratégica» | tesis | → 25 rotuladas `Total_Metas_PDOT` | ✅ criterio: mayor monto (Javo) | 🟢 |

**Fecha interna más antigua localizada en el corpus: `2026-05-16`** (Gold Master v5.4). El material de abril existe —la metodología TERRA/QUADRUM— pero **entre abril y el 10 de mayo no hay ningún artefacto conservado**, y ahí es donde ocurrieron los cambios que esta tabla no puede justificar.

## Barrido documental

⚠️ **La columna «copiado» NO es la fecha del documento.** Todos los archivos se trasladaron a esta carpeta el mismo día, así que el sistema de ficheros dice `2026-09-04` para material que es de enero o de abril. **La fecha real vive en el contenido** —`Metodologia_SIAP_ICPI.docx` se identifica como TERRA/QUADRUM © 2026 y su copia en Drive está fechada el 25 de abril—. Ordenar la genealogía por `mtime` produciría una cronología falsa.

| Documento | Copiado | Caracteres | Temas con material |
|---|---|---:|---|
| `anexo 0.docx` | 2026-02-11 | 36708 | `TERRA/QUADRUM` |
| `ANEXO L MANUAL TECNICO QUADRUM FINAL v5.0.do` | 2026-04-03 | 83097 | `P_i · evolución`, `R_i · evolución`, `fórmula`, `TERRA/QUADRUM` |
| `Documento doctrinal.docx` | 2026-09-04 | 23912 | — |
| `historial conversacional de Quira.docx` | 2026-09-04 | 95189 | `universo 25/66`, `TERRA/QUADRUM` |
| `historico construccion quira.docx` | 2026-09-04 | 358314 | `E_i · regla`, `P_i · evolución`, `AVEP · origen`, `fórmula`, `TERRA/QUADRUM` |
| `ICPI (1).docx` | 2026-09-04 | 44342 | `AVEP · origen`, `universo 25/66`, `unidad `i`` |
| `ICPI.docx` | 2026-09-04 | 44342 | `AVEP · origen`, `universo 25/66`, `unidad `i`` |
| `memoriaa algo quira.docx` | 2026-09-04 | 73607 | `C_i · origen`, `P_i · evolución`, `AVEP · origen`, `universo 25/66` |
| `metodologia.docx` | 2026-09-04 | 77466 | `E_i · regla`, `P_i · evolución`, `AVEP · origen`, `universo 25/66` |
| `Metodologia_SIAP_ICPI.docx` | 2026-09-04 | 58662 | `E_i · regla`, `P_i · evolución`, `R_i · evolución`, `AVEP · origen`, `universo 25/66`, `fórmula`, `TERRA/QUADRUM` |
| `Metodología Integral SIAP-ICPI v2.4 (Maestra` | 2026-09-04 | 4326 | `fórmula`, `TERRA/QUADRUM` |
| `Metodología SIAP-ICPI v2.4 - Capítulo I.docx` | 2026-09-04 | 3482 | `AVEP · origen`, `TERRA/QUADRUM` |
| `QUADRUM_ICPI_Calculadora (1).csv` | 2026-09-04 | 2437 | `P_i · evolución` |
| `sprint 1.docx` | 2026-09-04 | 8479 | — |
| `Ultima conversacion Director Claude.docx` | 2026-09-04 | 31934 | `AVEP · origen` |

### `anexo 0.docx` · 2026-02-11

**TERRA/QUADRUM**

- …nvestigador Principal: Ronald Javier Delgado Santana Creador Metodología ICPI y Protocolo QUADRUM Febrero 2026 Versión 2.0 Documento Confidencial 0.1. INGENIERÍA FINANCIERA: La viabilidad financiera de QUADRUM se sustenta en modelos de apalancamiento de capital de cooperación. 0.1.1. Principio de Ad…
- …ón 2.0 Documento Confidencial 0.1. INGENIERÍA FINANCIERA: La viabilidad financiera de QUADRUM se sustenta en modelos de apalancamiento de capital de cooperación. 0.1.1. Principio de Adicionalidad (OCDE) El capital extranjero genera adicionalidad sin sustituir presupuesto municipal. 0.1.2. Ratio de A…
- …. Ratio de Apalancamiento 45:1 Ratio 45:1 alcanzable: Medellín sin blockchain logró 35:1, QUADRUM justifica +10 puntos BASE METODOLÓGICA DEL MODELO DE APALANCAMIENTO La viabilidad financiera del Proyecto QUADRUM no se sustenta en el gasto corriente del GAD, sino en la aplicación técnica de modelos d…

### `ANEXO L MANUAL TECNICO QUADRUM FINAL v5.0.docx` · 2026-04-03

**P_i · evolución**

- …entales APIs REST Públicas: SERCOP (compraspublicas.gob.ec), SNI (sni.gob.ec) Parseo LOTAIP: Extracción cédulas presupuestarias, fichas proyecto, POA No hay integración directa a eSIGEF/SIGAD internos, sino consulta de portales públicos + LOTAIP. L.4.2. Output JSON Estructurado Ejemplo de salida est…
- …mesa: str - Vi: float (0.0, 0.5, 1.0) - Verificación documental - Pi: float - Peso presupuestario normalizado - Ei: int (1-5) - Entidad custodio responsable - Ti: float (0.0-1.0) - Avance temporal - Ri: float (0.5-1.5) - Relevancia constitucional Returns: dict…

**R_i · evolución**

- …ad custodio responsable - Ti: float (0.0-1.0) - Avance temporal - Ri: float (0.5-1.5) - Relevancia constitucional Returns: dict: { 'icpi': float (0-100), 'timestamp': datetime, 'promesas_totales': int, 'promesas_verificadas': int, 'desglose_…

**fórmula**

- …n la tesis. L.6.1. Implementación de la Fórmula ICPI Fórmula matemática original (tesis): ICPI = [Σ(Vi × Pi × Ei × Ti × Ri) / Σ(Pi × Ri)] × 100 Código Python operacionalizado: def calcular_ICPI_dinamico(promesas_df): """ Calcula ICPI según fórmula validada tesis ULEAM Args: promesas_df (panda…
- …la Fórmula ICPI Fórmula matemática original (tesis): ICPI = [Σ(Vi × Pi × Ei × Ti × Ri) / Σ(Pi × Ri)] × 100 Código Python operacionalizado: def calcular_ICPI_dinamico(promesas_df): """ Calcula ICPI según fórmula validada tesis ULEAM Args: promesas_df (pandas.DataFrame): DataFrame con co…

**TERRA/QUADRUM**

- …ANEXO L MANUAL TÉCNICO QUADRUM De la Metodología a la Implementación Arquitectura Técnica de Verificación Cruzada y Detección Automática de Incoherencias ──────────────────────────────────────────────────────────── Investigador Principal: Ron…
- …nvestigador Principal: Ronald Javier Delgado Santana Creador Metodología ICPI y Protocolo QUADRUM Febrero 2026 ÍNDICE GENERAL PARTE I: FUNDAMENTOS METODOLÓGICOS L.1. Propósito y Alcance del Protocolo L.2. Del SIAP-ICPI a QUADRUM: Evolución de la Transparencia L.3. Arquitectura de los 13 Sistemas de …
- …I: FUNDAMENTOS METODOLÓGICOS L.1. Propósito y Alcance del Protocolo L.2. Del SIAP-ICPI a QUADRUM: Evolución de la Transparencia L.3. Arquitectura de los 13 Sistemas de Verificación Cruzada PARTE II: MÓDULOS TÉCNICOS AUTOMATIZADOS L.4. Módulo 1: Ingesta Automática de Datos (Scraping y APIs) L.5. Módu…

### `historial conversacional de Quira.docx` · 2026-09-04

**universo 25/66**

- …nito”. Lo más importante Esto desbloquea después: 1. Drilldown real Click entidad → abre universo operacional. 2. Navegación suave Sin rerender completo. 3. Estado persistente Entidad seleccionada, territorio, alerta, filtro temporal. 4. Sensación “OS” No “web app”. Y QUIRA ya está entrando exactame…

**TERRA/QUADRUM**

- …ocumentos_proyecto\ ← Manual técnico, ensayo, PDFs académicos _historico\ ← TODO Terra/ECIAP legacy quira-os\ ← git repo (intacto) quiraintelligence-web\ ← git repo (intacto) MAPA_ECOSISTEMA_QUIRA.md ← actualizado a v2.0 **Corregido:** - Typos BAses fundamentales, GAD Montecritis, Holding Muni…
- …siones antiguas del Gold Master → historial_gold_master\ (archivadas, no borradas) - Todo Terra/ECIAP → _historico\ **Creado:** - governance\QUIRA_STATE.md — el documento que el colega pidió primero **⚠️ Acción manual pendiente (no puedo hacerlo yo):** - Revocar API Key Gemini.txt en Tecnic_SOLO_CON…
- …— es contexto que no puedo perderme: Eso es exactamente lo que necesitaba leer. El boceto Terra Ciudadana es mucho más avanzado de lo que asumía. Voy a sintetizar todo antes de proponer qué documentos planificar. --- ## Lo que encontré en el boceto Terra Ciudadana ya tenía el 80% de QUIRA Ciudadana.…

### `historico construccion quira.docx` · 2026-09-04

**E_i · regla**

- …extractor: QLEP-v1.0 revisado_por_experto: false ACK_ID: CE_3_6 TIPO: principio NOMBRE: Descentralización y Fortalecimiento de Autonomías FUENTE: norma: Constitución de la República del Ecuador sigla: CE jerarquia: 0 articulo: "3" inciso: "6" fecha_vigencia: "2008 (vigente)" ACTOR_OBLIGADO: - Estado…
- …─────────────────────────────── ACK_ID: CE_238 CLASE: ACK_PRINCIPIO TIPO: principio NOMBRE: GADs — Autonomía Política, Administrativa y Financiera + Principios FUENTE: norma: Constitución de la República del Ecuador sigla: CE jerarquia: 0 articulo: "238" inciso: "" fecha_vigencia: "2008-10-20" ACTOR…

**P_i · evolución**

- …o con MIES/MSP/MIDUVI). EVIDENCIA: - POA con programas explícitos para cada subgrupo GAP - Presupuesto GAP ≥ 10% ingresos no tributarios (COOTAD 249) - LOTAIP Numeral 5 (catálogo servicios GAP) - LOTAIP Numeral 18 (convenios MIES/MSP/MIDUVI) - LOTAIP Numeral 22 (rendición de cuentas GAP) - Informe R…

**AVEP · origen**

- …QUIRA" es prominente e invita a interacción Lo que falla — los 5 críticos: D1 — "53.6% · Ruptura Sistémica" como primera impresión. El Q1-2026 acumulado es el primer número que ve el alcalde. El ICPI anual 2025 fue 69.93% (sobre umbral). El dato Q1 está bajo umbral por acumulación trimestral, no por…
- …Q1 está bajo umbral por acumulación trimestral, no por deterioro real. Un alcalde que ve "Ruptura Sistémica" en su primera pantalla va a ponerse defensivo o van a rechazar el sistema. Necesita contexto: "Q1-2026 acumulado · ICPI anual 2025: 69.93%". D2 — Aterrizaje directo en métricas sin contexto c…
- …afo: query "ADR-024 cuatro capas") - Auditoría UX hecha. Hallazgos: tagline frío · "53.6% Ruptura Sistémica" sin contexto asusta al alcalde · 12 dominios son tarjetas, deberían ser puertas. ═══════════════════════════════════════════════════════════ TAREA 2 — Preguntá a Javo antes de avanzar ═══════…

**fórmula**

- …* publicación * acceso * cumplimiento * calidad documental Normativa: * CE Art. 18 * LOTAIP * Reglamento * Manual DPE Pregunta: ¿La información pública cumple los estándares exigidos? Aquí viven: * C5a * C5b * C5t * C5d * C5c Dom07-B Transparencia Democrática Objeto: * participación * fiscalización …

**TERRA/QUADRUM**

- …fo. La memoria histórica es la base de QUIRA dialéctica. EditadoBOOT.md+5-0 Ahora ingiero TERRA CIUDADANA al grafo. Ejecutado un comando, ejecutado un agente Agente corriendo. Mientras, te digo lo que más importa del documento: QUIRA Ciudadana — visión actualizada vs. TERRA v2.1 Lo que mejoró respec…
- …tras, te digo lo que más importa del documento: QUIRA Ciudadana — visión actualizada vs. TERRA v2.1 Lo que mejoró respecto a TERRA: Dato clave: Ya tenemos app/connectors/dpe.py y app/connectors/sercop.py en el repo. La infraestructura de fetching automático de DPE y SERCOP ya existe en parte. Lo que…
- …documento: QUIRA Ciudadana — visión actualizada vs. TERRA v2.1 Lo que mejoró respecto a TERRA: Dato clave: Ya tenemos app/connectors/dpe.py y app/connectors/sercop.py en el repo. La infraestructura de fetching automático de DPE y SERCOP ya existe en parte. Lo que hay que consensuar en equipo antes d…

### `ICPI (1).docx` · 2026-09-04

**AVEP · origen**

- …ncia. Este paradigma, basado en la improvisación y la discrecionalidad técnica, socava la Gestión por Mandato y anula la soberanía del voto al desvincular el presupuesto de la planificación original. Desde la Ciencia Política, Desde la Ciencia Política, este trabajo proporciona herramientas metodoló…
- …ntrastar la evidencia documental reportada frente a la ejecución real para diferenciar la Gestión por Mandato de la Gestión por Ocurrencia. Calcular el Índice de Congruencia Programático e Institucional (ICPI) y determinar la Brecha de Integridad final respecto al reporte oficial. 1.4. Fundamentació…
- …ndición de cuentas. A continuación, se presenta la Matriz de Articulación Normativa de la Gestión por Mandato, la cual pormenoriza los instrumentos legales que obligan a la administración municipal a mantener la fidelidad absoluta entre lo prometido y lo ejecutado: 1.5. Hipótesis: Dada la naturaleza…

**universo 25/66**

- …validez semántica de la fuente original. 3.3. Delimitación de la Población y Diseño de la Muestra Estratégica Ponderada La determinación del componente empírico de esta investigación se articula mediante un abordaje dual de precisión técnica; en primera instancia, se define como Población de Estudio…
- …análisis de alta complejidad sobre la ejecución material y financiera, se implementa una Muestra Estratégica Ponderada de veinte (20) unidades de análisis; por consiguiente, esta selección no es azarosa, sino que responde a criterios de representatividad presupuestaria y competencias exclusivas del …

**unidad `i`**

- …rte del SIGAD y el mandato electoral (medida a través de la Variable de Verificación Vi). Unidad de Análisis: El flujo informativo y programático en la trayectoria: Plan de Trabajo → PDOT → POA → SIGAD del Gobierno Autónomo Descentralizado Municipal de Montecristi. CAPÍTULO II: MARCO TEÓRICO Y CONCE…

### `ICPI.docx` · 2026-09-04

**AVEP · origen**

- …ncia. Este paradigma, basado en la improvisación y la discrecionalidad técnica, socava la Gestión por Mandato y anula la soberanía del voto al desvincular el presupuesto de la planificación original. Desde la Ciencia Política, Desde la Ciencia Política, este trabajo proporciona herramientas metodoló…
- …ntrastar la evidencia documental reportada frente a la ejecución real para diferenciar la Gestión por Mandato de la Gestión por Ocurrencia. Calcular el Índice de Congruencia Programático e Institucional (ICPI) y determinar la Brecha de Integridad final respecto al reporte oficial. 1.4. Fundamentació…
- …ndición de cuentas. A continuación, se presenta la Matriz de Articulación Normativa de la Gestión por Mandato, la cual pormenoriza los instrumentos legales que obligan a la administración municipal a mantener la fidelidad absoluta entre lo prometido y lo ejecutado: 1.5. Hipótesis: Dada la naturaleza…

**universo 25/66**

- …validez semántica de la fuente original. 3.3. Delimitación de la Población y Diseño de la Muestra Estratégica Ponderada La determinación del componente empírico de esta investigación se articula mediante un abordaje dual de precisión técnica; en primera instancia, se define como Población de Estudio…
- …análisis de alta complejidad sobre la ejecución material y financiera, se implementa una Muestra Estratégica Ponderada de veinte (20) unidades de análisis; por consiguiente, esta selección no es azarosa, sino que responde a criterios de representatividad presupuestaria y competencias exclusivas del …

**unidad `i`**

- …rte del SIGAD y el mandato electoral (medida a través de la Variable de Verificación Vi). Unidad de Análisis: El flujo informativo y programático en la trayectoria: Plan de Trabajo → PDOT → POA → SIGAD del Gobierno Autónomo Descentralizado Municipal de Montecristi. CAPÍTULO II: MARCO TEÓRICO Y CONCE…

### `memoriaa algo quira.docx` · 2026-09-04

**C_i · origen**

- …IN — Cadena de Integridad Intersistémica ✅ VIVO como... Trazabilidad Intersistémica D1→D5 Responsabilidad Orgánica Vinculante (Ci) ✅ VIVO como... H07c: firma Director activa Ti_V Erosión del Compromiso ✅ VIVO como... Deterioro institucional en RC-M Brecha de Integridad Intersistémica ✅ VIVO como... …

**P_i · evolución**

- …Norma habilitante:** Art. 215-220 COOTAD — ciclo presupuestario y ejecución. Art. 113 COPFP — evaluación de la ejecución presupuestaria. **Alerta crítica:** 59.85% es preocupante. El umbral óptimo para GAD municipales ecuatorianos es ≥75%. Implica que más de 40% del presupuesto no se ejecutó, genera…
- …------|--------| | IED — Eficiencia Direccional | 33.99% | 🟡 Gestión por Ocurrencia | | IGP — Gobernanza Participativa | 27.98% | 🔴 Crítico | | ISP — Salud Presupuestal | 14.58% | 🔴 Crítico | | Coberturas agua CUP | 39.53% | 🔴 Déficit severo | | NBI cantonal | 30.84% | 🟡 Meta reducir | | Pobreza mul…

**AVEP · origen**

- …a tiene gemela en 01_PDOT/diagnostico/social/DIAG-Demografía.md Faltan en CORE: SAT, IED, AVEP, MMP, RC-M _Índice_CORE.md no los lista Crear 5 nuevas notas ✅ El trabajo del v5.5 NO se pierde El valor de las 123 hojas es 100% válido. Toda la lógica de fórmulas, scoring, alertas y metodología permanec…
- …osite IED "Índice de Evaluación Directiva" ✅ VIVO, mismo nombre G4.4_IED, LOSEP Art.76-82 Gestión por Mandato / Gestión por Ocurrencia ✅ VIVO AVEP 🟢/🟠 CININ — Cadena de Integridad Intersistémica ✅ VIVO como... Trazabilidad Intersistémica D1→D5 Responsabilidad Orgánica Vinculante (Ci) ✅ VIVO como... …
- …ismo nombre G4.4_IED, LOSEP Art.76-82 Gestión por Mandato / Gestión por Ocurrencia ✅ VIVO AVEP 🟢/🟠 CININ — Cadena de Integridad Intersistémica ✅ VIVO como... Trazabilidad Intersistémica D1→D5 Responsabilidad Orgánica Vinculante (Ci) ✅ VIVO como... H07c: firma Director activa Ti_V Erosión del Comprom…

**universo 25/66**

- …ADO — Los 4 niveles 🟢🟡🟠🔴, activadores, principio fundacional 08_MMP_MENSUAL.md ✅ CREADO — 25 metas × 12 meses, D2_Score, desambiguación ICPI 09_RCM_LONGITUDINAL.md ✅ CREADO — RC-M canónica, SAT-III reincidencia, Diff Engine _Índice_CORE.md ✅ ACTUALIZADO — +5 notas, advertencia colisión ICPI, v5.5 00…

### `metodologia.docx` · 2026-09-04

**E_i · regla**

- …trucción de vía urbana ejecutada directamente por la Dirección de Obras Públicas del GAD. E_i = 0,90: Proyecto de tratamiento de aguas residuales ejecutado mediante convenio entre el GAD y SENAGUA, con responsabilidades compartidas documentadas. E_i = 0,75: Operación del sistema de agua potable dele…
- …mediante convenio entre el GAD y SENAGUA, con responsabilidades compartidas documentadas. E_i = 0,75: Operación del sistema de agua potable delegado al Patronato Municipal de Agua Potable de Montecristi, entidad adscrita con personería jurídica y presupuesto propio. 3.4.6. Variable C_i: Imputabilida…

**P_i · evolución**

- …stratégica que corresponde a la meta i. Operacionaliza el mandato del artículo 54 del COPFP: las metas que consumen mayor proporción del presupuesto del PDOT tienen mayor peso en la evaluación de su cumplimiento. Fórmula: Propiedades: El valor de es estrictamente positivo y la suma de todos los es i…

**AVEP · origen**

- …iplicado por 100, expresa el ICPI como un porcentaje que oscila entre 0 y 100. 3.5.2. El Baremo de Interpretación AVEP Los resultados del ICPI se interpretan mediante la Escala AVEP (Alineación, Vinculación, Ejecución, Publicación), cuyos rangos y categorías se definen a continuación: 3.5.3. Ejercic…
- …el ICPI como un porcentaje que oscila entre 0 y 100. 3.5.2. El Baremo de Interpretación AVEP Los resultados del ICPI se interpretan mediante la Escala AVEP (Alineación, Vinculación, Ejecución, Publicación), cuyos rangos y categorías se definen a continuación: 3.5.3. Ejercicio Ilustrativo con Referen…
- …l Baremo de Interpretación AVEP Los resultados del ICPI se interpretan mediante la Escala AVEP (Alineación, Vinculación, Ejecución, Publicación), cuyos rangos y categorías se definen a continuación: 3.5.3. Ejercicio Ilustrativo con Referencia al GAD Montecristi Para demostrar el funcionamiento concr…

**universo 25/66**

- …evengados registrados en los sistemas oficiales del Estado para las metas incluidas en la muestra estratégica analizada. Por tanto, sus resultados no son estimaciones con margen de error; son hechos fácticos certificados por la evidencia transaccional oficial. Esta característica elimina la necesida…
- …lo de variables, en la que se calculan las seis variables del modelo para cada meta de la muestra estratégica. La cuarta es el cálculo de índices, en la que se obtienen el ICPI global, el IFE, los IED por dirección y las alertas MOM. La quinta es la generación de reportes, en la que el Módulo M8 pro…
- …e el Módulo M8 produce las visualizaciones y documentos de salida. 3.3. DEFINICIÓN DE LA MUESTRA ESTRATÉGICA DE METAS Antes de calcular el ICPI, es necesario definir sobre qué metas opera el modelo. El SIAP-ICPI no evalúa la totalidad de metas que puede contener un PDOT —algunos tienen más de doscie…

### `Metodologia_SIAP_ICPI.docx` · 2026-09-04

**E_i · regla**

- …ctos de calificación de cada componente, tal como están implementados en H13, son: 3.3.4. Eᵢ — Autonomía Orgánica Mide el grado de control que la dirección responsable tiene sobre la ejecución de la meta, considerando si depende de factores externos incontrolables. Se asigna manualmente por el anali…
- …ᵢ): variable que mide el control del director sobre la ejecución de la meta. Valores: 1.0 autónomo, 0.9 compartido, 0.75 difuso. Calidad del Proceso (Cᵢ): variable que evalúa la limpieza administrativa del expediente. Valores: 1.0 limpio, 0.9 regular, 0.75 ambiguo; reducción a 0.50 por SAT-V activo.…

**P_i · evolución**

- …ocurrió con integridad comprobable. 3.3. Desglose Operativo de las Seis Variables 3.3.1. Pᵢ — Peso Financiero Normalizado Representa la magnitud económica relativa de la meta i respecto al universo total de inversión del PDOT. Se calcula como: La condición de normalización exige que de manera exacta…

**R_i · evolución**

- …manera que una obra de infraestructura hídrica que beneficia a miles de familias. 3.3.2. Rᵢ — Relevancia Crítica o Peso de Competencia Clasifica las metas según la naturaleza jurídica de la competencia que les da origen, basándose en la jerarquía de competencias que establece el COOTAD. La escala ti…
- …rresponda. Si una meta tiene Rᵢ_raw = 1.5 y un Bono de Género, su Rᵢ_final = 1.5 × 1.15 = 1.725. 3.3.3. Vᵢ — Producto Lógico de Verificación Intersistémica Esta es la variable más crítica del sistema. Actúa como el filtro de integridad que determina si una meta tiene existencia verificable en los si…

**AVEP · origen**

- …Art. 204; LOPC Art. 12; COOTAD Art. 295. Clasificación: el IFE se clasifica en la escala AVEP canónica. Un IFE < 70% indica que la autoridad no convirtió la mayoría de sus compromisos electorales en planificación verificable. 4.3. IED — Índice de Eficiencia Directiva (H17 / H30) Qué mide: el ICPI ca…
- …e que estas metas sean prioritarias en la Ruta de Recuperación. CAPÍTULO VIII: LA ESCALA AVEP — CLASIFICACIÓN DE MADUREZ INSTITUCIONAL 8.1. Los Cinco Niveles de la Escala AVEP El ICPI no es solo un porcentaje. Es un diagnóstico del estado de madurez democrática e institucional. La Escala AVEP (Análi…
- …ESCALA AVEP — CLASIFICACIÓN DE MADUREZ INSTITUCIONAL 8.1. Los Cinco Niveles de la Escala AVEP El ICPI no es solo un porcentaje. Es un diagnóstico del estado de madurez democrática e institucional. La Escala AVEP (Análisis de Valor y Eficiencia Pública), implementada en H01 Sección B como la escala c…

**universo 25/66**

- …implementación para el período de mandato 2024-2027 del GAD Municipal de Montecristi, n = 25 metas). La estructura de la fórmula separa intencionalmente un numerador —que representa el "hecho verificado" de la gestión— de un denominador —que representa el "deber ser" estratégico de la gestión. El co…
- …ficación | Base estratégica inmutable aprobada mediante ordenanza municipal. Contiene las 25 metas plurianuales con sus presupuestos, competencias y metas de indicador. Ningún director puede modificar este silo unilateralmente. | H04 | COOTAD Art. 295; COPFP Arts. 41-42 S3 | POA — Operativo | Plan O…

**fórmula**

- …H12 sea la única cifra que alimenta los tableros de salida; y (c) la suma de ponderadores Σ(Pᵢ) sea exactamente igual a 1.0000. Es el mecanismo de defensa ante intentos de manipulación por parte de un operador del sistema. CAPÍTULO III: LA FÓRMULA SIAP-ICPI — EL MOTOR CANÓNICO 3.1. Naturaleza del Mo…
- …—sin importar cuánto dinero se haya declarado gastado (Tᵢ), cuán importante sea la meta (Pᵢ × Rᵢ), o cuán "limpio" sea su proceso (Cᵢ). El producto de cualquier número por cero es cero. Esta mecánica es el blindaje central del sistema contra el maquillaje estadístico: un gasto no íntegro es, para el…
- …la fórmula no es un promedio simple. Es un promedio ponderado y filtrado: El denominador Σ(Pᵢ × Rᵢ) establece el "deber ser" estratégico del GAD. Representa la suma del peso financiero multiplicado por la relevancia competencial de cada meta. Es el piso máximo teórico que alcanzaría el ICPI si todas…

**TERRA/QUADRUM**

- …METODOLOGÍA SIAP-ICPI Sistema de Integridad Algorítmica Preventiva — Ecosistema TERRA Quadrum Gov Tech © 2026 CAPÍTULO I: FUNDAMENTOS, NATURALEZA Y PROPÓSITO DEL SISTEMA 1.1. Naturaleza del Problema que Origina el Sistema La administración pública en los Gobiernos Autónomos Descentralizados del Ecua…
- …METODOLOGÍA SIAP-ICPI Sistema de Integridad Algorítmica Preventiva — Ecosistema TERRA Quadrum Gov Tech © 2026 CAPÍTULO I: FUNDAMENTOS, NATURALEZA Y PROPÓSITO DEL SISTEMA 1.1. Naturaleza del Problema que Origina el Sistema La administración pública en los Gobiernos Autónomos Descentralizados del Ecua…
- …S (SAT) — INTELIGENCIA PREVENTIVA 5.1. Naturaleza y Función del Sistema SAT El ecosistema TERRA no es un repositorio pasivo de datos. Actúa como un radar de vigilancia algorítmica continua. Las Señales de Atención Temprana (SAT) son activadores automáticos diseñados para detectar rupturas en la cade…

### `Metodología Integral SIAP-ICPI v2.4 (Maestra) (1).docx` · 2026-09-04

**fórmula**

- …normalizado que castiga la falta de evidencia en cualquier eslabón de la cadena: ICPI = [ Σ (Pi × Ri × Vi × Ei × Ti × Ci) / Σ (Pi × Ri) ] × 100 3.2. Definición de Variables Operativas CAPÍTULO IV: SISTEMA DE ÍNDICES DERIVADOS El SIAP-ICPI genera 12 índices especializados para diferentes tomadores de…
- …e evidencia en cualquier eslabón de la cadena: ICPI = [ Σ (Pi × Ri × Vi × Ei × Ti × Ci) / Σ (Pi × Ri) ] × 100 3.2. Definición de Variables Operativas CAPÍTULO IV: SISTEMA DE ÍNDICES DERIVADOS El SIAP-ICPI genera 12 índices especializados para diferentes tomadores de decisión (Ref: H15-H20b, H41, H42…

**TERRA/QUADRUM**

- …Integral SIAP-ICPI v2.4 Ecosistema de Integridad Algorítmica Preventiva Desarrollado por Quadrum GovTech | Autor: Ronald Javier Delgado Santana CAPÍTULO I: FUNDAMENTOS Y GOBERNANZA PREVENTIVA 1.1. Propósito y Alcance (Ref: H38) El Sistema de Integridad Algorítmica Preventiva (TERRA SIAP-ICPI) es una…
- …TIVA 1.1. Propósito y Alcance (Ref: H38) El Sistema de Integridad Algorítmica Preventiva (TERRA SIAP-ICPI) es una arquitectura de supervisión diseñada para certificar la congruencia entre la planificación estratégica (PDOT) y la ejecución transaccional en Gobiernos Autónomos Descentralizados (GAD). …

### `Metodología SIAP-ICPI v2.4 - Capítulo I.docx` · 2026-09-04

**AVEP · origen**

- …que mide si las promesas del Plan de Trabajo CNE fueron incorporadas formalmente al PDOT. AVEP | Escala de Gobernanza | Escala de 5 niveles (Ruptura, Ocurrencia, Transición, Mandato, Excelencia) para clasificar el desempeño institucional. MOM | Mutación del Objeto de Medición | Alteración de la unid…

**TERRA/QUADRUM**

- …aleza y Propósito del Sistema (Ref: H38) El Sistema de Integridad Algorítmica Preventiva (TERRA SIAP-ICPI) se define como una arquitectura tecnológica de supervisión no punitiva, diseñada para certificar la congruencia entre la planificación estratégica de un GAD y su ejecución transaccional efectiv…

### `QUADRUM_ICPI_Calculadora (1).csv` · 2026-09-04

**P_i · evolución**

- …CÓDIGO,PROMESA_CNE,PRESUPUESTO_ASIGNADO,PRESUPUESTO_TOTAL,Pi,Vi,Ei,Ti,Ri,PRODUCTO,DENOMINADOR,ICPI_INDIVIDUAL A-001,Construir sistema agua potable El Colorado,500000,6250000,=C2/D2,1,1,1,1.5,=E2*F2*G2*H2*I2,=E2*I2,=J2/K2*100 A-002,Asfaltar 5 km vías principal…

### `Ultima conversacion Director Claude.docx` · 2026-09-04

**AVEP · origen**

- …grafo: query "ADR-024 cuatro capas") Auditoría UX hecha. Hallazgos: tagline frío · "53.6% Ruptura Sistémica" sin contexto asusta al alcalde · 12 dominios son tarjetas, deberían ser puertas. ═══════════════════════════════════════════════════════════ TAREA 2 — Preguntá a Javo antes de avanzar ═══════…

## Lo que este expediente NO hace

- **No decide qué versión metodológica rige.** Registra que existen, con su documento y su fecha. El dictamen es de `011`.
- **No cierra el frente de `E_i`.** Cambia su estado; la correspondencia valor↔regla sigue por auditar.
- **No toca el Gold Master ni recalcula el 27,4582 %.** El baseline sigue congelado mientras se reconstruye la genealogía.
- **No descarta la definición B** ni ningún documento histórico: la divergencia entre versiones **es** el objeto de estudio.

---
*GM-Ω · Expediente genealógico · 15 documentos barridos · el Gold Master no se modificó · Dylus Lab © 2026*
