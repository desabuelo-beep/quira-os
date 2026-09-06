# GM-Ω · ICPI — DICTAMEN  `011-C4`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/dictamen_c4.py`.

> ### Las tres etiquetas
> Toda cifra distinta del baseline es **MATEMÁTICAMENTE REPRODUCIBLE** · **METODOLÓGICAMENTE CONTRAFACTUAL** · **NO AUTORIZADA PARA PUBLICACIÓN** (`DOC-010`). El único ICPI publicable sigue siendo **27,4582 %**.

⚠️ **`C4` no modifica nada.** No recalibra, no renombra, no mueve dominios. Emite un juicio metodológico sobre decisiones de diseño enumeradas.

## Las dos reglas que ordenan el dictamen

> ### La historia explica. La transferibilidad clasifica. La metodología justifica. La evidencia decide.

| Error | Estado |
|---|---|
| «es antiguo, por tanto debe conservarse» | 🔴 prohibido · `DOC-013` |
| «es contingente, por tanto debe eliminarse» | 🔴 prohibido · `DOC-027` |

Y la segunda, que gobierna `C4-4`:

> ### La ausencia de evidencia puede LIMITAR lo que el sistema puede afirmar; no demuestra por sí misma la ausencia del fenómeno.

⚠️ Y lo que `C4` **no** es: un juicio sobre si QUIRA está «bien» o «mal». Las cinco decisiones `D` de `010` llegan aquí como **decisiones sometidas a prueba, no como cargos contra el diseño**. `D` significa «no puede recibir presunción de necesidad» — no «incorrecto».

## La estructura del dictamen

| # | Sección | Pregunta |
|---|---|---|
| `C4-1` | **Fenómeno** | ¿qué pretende medir realmente el ICPI? |
| `C4-2` | **Unidad** | ¿qué representa cada `i`, y cómo se relacionan unidad documental, operacional y estadística? |
| `C4-3` | **Arquitectura algebraica** | ¿la multiplicación representa la relación entre dimensiones, o introduce una restricción no demostrada? |
| `C4-4` | **Evidencia** | ¿`V_i` mide verificabilidad, ausencia de evidencia, calidad documental — o algo más? |
| `C4-5` | **Parametrización** | ¿hay fundamento suficiente para `0,15/0,10/0,05` y `0,50`? |
| `C4-6` | **Interpretación** | ¿qué afirmaciones permite el resultado, y cuáles no? |
| `C4-7` | **AVEP** | ¿el baremo clasifica el fenómeno medido, o traduce el resultado para comunicación institucional? |

El orden no es arbitrario: **no se puede juzgar el álgebra antes de saber qué fenómeno se mide, ni la escala antes de saber qué clasifica**.

## `C4-1` · Fenómeno

> ¿Qué pretende medir realmente el ICPI?

Lo que las etapas anteriores establecieron:

| Fuente | Qué dice |
|---|---|
| `GM-Ω-001` | **Índice de Congruencia Programática e Intersistémica** |
| Constitución §CAPA 0.5 | «Cumplimiento Institucional (ICPI)» — ⚠️ nombre que el propio canon retiró |
| `data/gm_snapshot.json` | «Índice Compuesto de Progreso Institucional», «mide velocidad de ejecución» — 🔴 `D-011` |

> ### Tres nombres distintos para el mismo número, y dos de ellos afirman cosas que el motor no hace

El ICPI **no mide cumplimiento** ni **velocidad**: mide si la cadena `programa → norma → verificación → ejecución → tiempo → trazabilidad` **se sostiene entera**. Es una propiedad de la cadena, no un grado de avance.

| Dictamen | |
|---|---|
| El fenómeno está **definido** en el constructo | ✅ **DEMOSTRADO** (`001`) |
| La **capa de publicación** lo describe mal | 🔴 **DEMOSTRADO** · `D-011`, abierta |
| El nombre `ICPI` corresponde al fenómeno | 🟡 **parcial** · «congruencia» sí; el acrónimo circula con tres expansiones |

## `C4-2` · Unidad

> ¿Qué representa cada `i`?

| Etapa | Resultado |
|---|---|
| `007-B0` · `011-A` | la unidad **cambió**: `i` = promesa del Plan CNE → `i` = meta del PDOT |
| `DOC-023` | el cambio **no es deriva**: hay razón declarada, definición operacional y genealogía |
| `008` | el universo medido son **25 de 66** metas |
| `008-R` | la correspondencia documental↔operacional **no está reconciliada** |
| `011-A2` | la unidad vigente **no está declarada en el canon** |

> ### El dictamen no puede cerrar `C4-2`, y eso es un hallazgo
>
> Mientras `011-A2` no declare la unidad en el canon y `011-B` no establezca la regla de correspondencia, **el ICPI se calcula sobre una unidad que el sistema no define formalmente**. El motor funciona; la definición vive en la práctica y no en el canon.

| Dictamen | |
|---|---|
| La unidad operacional está **implementada y es consistente** | ✅ **DEMOSTRADO** · 25 identificadores estables |
| La unidad está **declarada en el canon** | 🔴 **no** · `011-A2` |
| La correspondencia con las 66 documentales | ⬜ **NO DETERMINABLE** · `011-B` |

⚠️ **Esto no invalida el índice**: lo acota. El ICPI es válido **sobre su universo operacional declarado**, y `ADR-036` lo congela para `v1`. Lo que no puede hacerse es presentarlo como si midiera el PDOT completo.

## ★ `C4-3` · Arquitectura algebraica

> ¿La multiplicación **representa** la relación entre dimensiones, o **introduce una restricción no demostrada**?

Lo primero es medir qué hace hoy:

| | |
|---|---:|
| metas del universo | 25 |
| metas **sin ningún factor en cero** | 19 |
| metas **anuladas** por al menos un factor | 6 |

| Factor | Metas en cero | Peso `P·R` que arrastran |
|---|---:|---:|
| `V_i` | 6 | 12.80 % |
| `E_i` | 0 | 0.00 % |
| `T_i` | 0 | 0.00 % |
| `C_i` | 0 | 0.00 % |

> ### La anulación multiplicativa opera hoy por **un solo factor**: `V_i`
>
> Ningún `E_i`, `T_i` ni `C_i` vale cero. Las **6 metas anuladas** lo están **exclusivamente por falta de evidencia documental**, y arrastran el **12.80 %** del peso del denominador.

Eso reformula `D1`: la pregunta sobre la multiplicatividad **no es abstracta**. En el estado actual, *toda* la anulación proviene de `V_i`, así que `D1` y `D2` **son la misma pregunta en la práctica** — aunque sigan siendo distintas en teoría.

| Dictamen | |
|---|---|
| La multiplicatividad **produce anulación total** ante un solo factor en cero | ✅ **DEMOSTRADO** · es su definición |
| Hoy esa anulación afecta a **6 de 25** metas | ✅ **DEMOSTRADO** |
| Existe razón **teórica, normativa o empírica** que la funde | ⬜ **NO DETERMINABLE** · `C3-R` cerró: los parámetros están documentados, su fundamento no |
| La multiplicatividad es **necesaria** al constructo | 🔴 **NO DEMOSTRADO** |
| La multiplicatividad es **incorrecta** | 🔴 **NO DEMOSTRADO** |

> ### Veredicto de `D1` · **DECISIÓN DE DISEÑO NO FUNDAMENTADA, CONSERVABLE BAJO DECLARACIÓN EXPLÍCITA**
>
> No se demuestra necesaria ni incorrecta. Puede conservarse **si el sistema declara que es una elección metodológica** y no una propiedad derivada del fenómeno. Lo que no puede hacerse es seguir presentándola como si estuviera fundada.

Y hay un argumento **a favor** que sí es defendible, y conviene decirlo: una cadena de congruencia en la que **cualquier eslabón roto invalida el conjunto** es una lectura coherente del fenómeno. `007-D` midió que es la decisión más consecuente del motor (**51,26 pp**). Que sea coherente no la vuelve necesaria — hay agregaciones alternativas que también lo serían.

## ★★ `C4-4` · Evidencia — la sección decisiva

> ¿`V_i` mide verificabilidad, ausencia de evidencia, calidad documental — o algo más?

### Las tres proposiciones que no pueden confundirse

| # | Proposición | Naturaleza |
|---|---|---|
| 1 | «el fenómeno **no ocurrió**» | afirmación sobre el **mundo** |
| 2 | «**no hay evidencia suficiente** para acreditarlo» | afirmación sobre el **estado del conocimiento** |
| 3 | «la unidad **no puede contribuir** al índice mientras carezca de evidencia» | **regla metodológica** |

> ### La proposición 3 puede ser perfectamente defendible. Lo que NO puede es presentarse como **consecuencia lógica** de la 2.
>
> Y ése es exactamente el punto que `C4` debe resolver.

### Qué hace el motor hoy

`V_i = 0` en **6 de 25 metas**, y el producto las anula: `J_i = 0`. Contribuyen `0` al numerador **y siguen pesando en el denominador** — el 12.80 %.

El contrafactual que separa la proposición 2 de la 3:

| Tratamiento de `V=0` | ICPI | Δ |
|---|---:|---:|
| **vigente** · anula la meta, que sigue en el denominador | **27.4582 %** | — |
| «no acreditado» · la meta **sale del universo medido** | 31.4883 % | +4.03 pp |
| «se presume cumplida» · `V=1` | 31.8909 % | +4.43 pp |

⚠️ **La tercera fila no es una alternativa defendible** —presumir cumplimiento sin evidencia contradice el principio rector—; se mide sólo para **acotar el rango** del efecto.

> ### El hallazgo
>
> Tratar `V=0` como «no acreditado» en vez de «no cumplido» mueve el índice **+4.03 pp**. No es un matiz interpretativo: **es una decisión con efecto material medible** sobre el resultado publicado.

### El choque con el canon, dicho sin rodeos

| Principio rector | *«La ausencia de evidencia es un RESULTADO de auditoría, nunca autorización para inferir hechos.»* |
|---|---|

Si `V=0` anula la meta, el índice **resta** por no poder acreditar. Caben dos lecturas, y el sistema no declara cuál sostiene:

| Lectura | Qué implicaría |
|---|---|
| **A** · el ICPI mide *congruencia acreditada* | anular es correcto: lo no acreditado **no cuenta como congruente**, y eso es un resultado, no una inferencia |
| **B** · el ICPI mide *congruencia real* | anular es una **inferencia**: se trata la falta de evidencia como falta de cumplimiento |

> ### Veredicto de `D2` · **LA REGLA ES DEFENDIBLE BAJO LA LECTURA `A`, Y HOY EL SISTEMA NO DECLARA CUÁL SOSTIENE**
>
> Bajo `A` no hay contradicción con el principio rector: el índice mide lo acreditable y lo declara. Bajo `B` sí la hay. **La diferencia no está en la fórmula: está en lo que el sistema afirma que el número significa** — y eso es `C4-6`.

⚠️ Y el índice mide entonces **dos cosas a la vez**: la gestión y la capacidad de documentarla. Puede ser intencional y legítimo en un índice de *congruencia intersistémica* —donde la trazabilidad **es** parte del fenómeno—, pero **debe declararse como elección metodológica**, no asumirse.

### La formulación endurecida de `V_i = 0`

> `V_i = 0` **no significa que el fenómeno no ocurrió**. Significa que, bajo la arquitectura actual, **la unidad no puede aportar congruencia acreditada al índice**.

Y el salto `27,4582 % → 31,4883 %` **no vale porque `31,4883` sea mejor** —no lo es ni pretende serlo—. Vale porque demuestra que **una decisión semántica sobre el estado de la evidencia tiene efecto material sobre el resultado**. Eso convierte a `D2` en una cuestión de **diseño epistemológico**, no en un detalle de fórmula.

### La pregunta que `D2` deja preparada — y que `C4` NO responde

Si la trazabilidad forma parte del fenómeno observado, entonces `V_i` **no es un defecto accidental del índice**: puede ser una dimensión sustantiva. Pero entonces:

> ¿Debe `V_i` estar **embebida multiplicativamente** dentro de un único ICPI, o debe existir **además** como una medida explícita e independiente de **acreditabilidad**?

⚠️ **Esa pregunta pertenece a la arquitectura futura y no se responde retrospectivamente aquí.** Resolverla dentro de `C4` sería rediseñar desde un peritaje, que es precisamente lo que la `Regla Maestra` (`DOC-029`) prohíbe.

## `C4-5` · Parametrización

> ¿Hay fundamento suficiente para `0,15 / 0,10 / 0,05` y `0,50`?

`C3-R` ya cerró la genealogía: **no hay que rehacerla**. Los parámetros están documentados; su fundamento cuantitativo no está determinado. `C4` sólo pregunta si hay justificación **metodológica** para conservarlos.

| Decisión | Estado | Efecto hoy |
|---|---|---|
| `D3` ponderación `0,15/0,10/0,05` | ⬜ sin fundamento cuantitativo | 🔵 **ninguno** · no hay infracciones registradas |
| `D4` piso `C_i ≥ 0,50` | ⬜ sin fundamento cuantitativo | 🔵 **ninguno** · el piso no se alcanza |

> ### Veredicto de `D3` y `D4` · **LATENTES · CONSERVABLES CON REVISIÓN OBLIGATORIA ANTES DE SU PRIMERA ACTIVACIÓN**
>
> Hoy no mueven el índice: ninguna infracción está registrada. Se activan **el día que se registre la primera** — y ése es exactamente el día en que tienen que estar bien. Conservarlos sin revisar sería aplazar la decisión hasta el momento en que ya no se pueda tomar con calma.

Y `D4` merece una línea propia, porque **no es un parámetro técnico**:

> El piso afirma que **incluso acumulando infracciones existe un mínimo de contribución institucional que debe preservarse**. Eso es una tesis sustantiva sobre la relación entre infracción y desempeño, y requiere fundamento propio.

## ★ `C4-6` · Interpretación

> ¿Qué afirmaciones permite el resultado — y cuáles no?

La sección que convierte al dictamen en algo operativo. Lo que **27,4582 %** autoriza a decir:

| ✅ Se puede afirmar | 🔴 NO se puede afirmar |
|---|---|
| «la congruencia **acreditada** de las 25 metas del universo operacional es 27,4582 %» | «el GAD cumple el 27 % de su PDOT» |
| «al corte de abril, con `T_i` parcial» | «el desempeño anual es del 27 %» |
| «`n` metas carecen de evidencia en al menos un silo» | «`n` metas **no se ejecutaron**» |
| «el índice mide la cadena completa» | «el índice mide velocidad de ejecución» (`D-011`) |

> ### La columna derecha no es hipotética
>
> `D-011` documenta que la capa de publicación ya describe el ICPI como «progreso institucional» que «mide velocidad de ejecución». Esa afirmación **no la sostiene el motor**.

## `C4-7` · AVEP

> ¿El baremo **clasifica el fenómeno medido**, o **traduce el resultado para comunicación institucional**?

⚠️ **No se pregunta qué escala es correcta.** No se puede validar una escala antes de declarar el fenómeno que pretende clasificar (`DOC-012`).

| Lo que consta | |
|---|---|
| `AVEP` es un **baremo propio**, no una norma externa | `007-X-bis` |
| Conviven **dos escalas divergentes** — 4 niveles con umbrales 75/60/50 y 5 con 90/70/40/20 | 🔴 `D-012` |
| Para el mismo baseline, el motor dice «🟠 Gestión por Ocurrencia» y el canon «🔴 Nivel de Atención Alta» | 🔴 `D-012` |
| Qué fenómeno clasifica —integridad, cumplimiento, desempeño, evidencia o riesgo— | ⬜ **NO DECLARADO** |

> ### Veredicto de `D5` · **NO EVALUABLE HASTA QUE SE DECLARE SU OBJETO**
>
> No es que la escala esté mal: es que **no se puede juzgar**. Y mientras dos versiones convivan sin que ninguna superficie declare cuál rige, el mismo número admite dos lecturas institucionales distintas.

## ★ DICTAMEN CONSOLIDADO

| | Decisión | Veredicto |
|---|---|---|
| `D1` | multiplicatividad | **no fundamentada · conservable bajo declaración explícita** |
| `D2` | `V_i` multiplicativo | **defendible bajo la lectura «congruencia acreditada» · el sistema debe declarar cuál sostiene** |
| `D3` | pesos `0,15/0,10/0,05` | **latente · revisión obligatoria antes de su primera activación** |
| `D4` | piso `0,50` | **latente · y afirma una tesis sustantiva que requiere fundamento propio** |
| `D5` | `AVEP` | **no evaluable hasta declarar su objeto** |

### Lo que el dictamen NO dice

- **No dice que el ICPI esté mal.** Ninguna decisión resultó incorrecta.
- **No autoriza a eliminar nada.** `D` era incertidumbre, no condena.
- **No recalibra.** El Gold Master sigue intacto y el baseline congelado.

### ⚠️ Y la corrección de la frase de cierre

Una versión anterior decía:

> ~~«El constructo **funciona y es internamente coherente**.»~~

Es **más amplia que lo demostrado**. `D1`-`D5` muestran justamente que **operatividad matemática ≠ coherencia sustantiva demostrada**. La formulación canónica es:

> **La implementación actual del constructo es matemáticamente operativa y sus reglas producen un resultado reproducible; su coherencia sustantiva depende de decisiones metodológicas que `C4` ha identificado y cuya necesidad no está completamente fundamentada.**

### ★ Las tres capas, que no pueden colapsarse

| # | Capa | Estado |
|---|---|---|
| 1 | **Operatividad computacional** — la fórmula corre y produce `27,4582 %` de forma reproducible | ✅ **DEMOSTRADA** |
| 2 | **Consistencia formal** — las reglas se ejecutan juntas sin conflicto | 🟡 **PARCIAL** · hay decisiones semánticas sin declarar |
| 3 | **Validez sustantiva** — el índice mide el fenómeno que dice medir | ⬜ **NO DEMOSTRADA POR `C4`** |

> La tercera capa es la que impide que «el motor funciona» se convierta inadvertidamente en «el índice es válido». **Las tres pueden ser ciertas a la vez sin contradicción.**

### ⚠️ Y qué hace realmente `C4` con las decisiones `D`

> **`C4` no las valida ni autoriza a conservarlas: cambia su ESTATUS EPISTEMOLÓGICO.** Pasan de ser reglas aplicadas sin declarar a ser decisiones identificadas, acotadas y con condición de revisión.

Lo que le falta al constructo no son correcciones: es **declarar sus propias elecciones como elecciones**. Cinco decisiones sostienen el índice y ninguna está declarada como decisión — se presentan como si fueran propiedades del fenómeno.

### Dictamen global

> **No existe evidencia suficiente para declarar que las decisiones `D` sean incorrectas. Tampoco existe evidencia suficiente para tratarlas como propiedades necesarias del fenómeno.**

Ése es el punto medio que `GM-Ω` tenía que alcanzar: ni conservadurismo ni revisionismo.

### La acción que el dictamen autoriza · **cinco `ADR`, no cuatro**

Son cinco decisiones y **no tienen el mismo tipo epistemológico**, así que cada una necesita su propia declaración:

| `ADR` | Decisión | Función de la declaración |
|---|---|---|
| `ADR-D1` | multiplicatividad | declarar la elección algebraica y sus alternativas |
| `ADR-D2` | `V_i` multiplicativo | declarar el significado de la ausencia / no acreditación |
| `ADR-D3` | pesos `C_i` | declarar el estado de fundamentación y la condición de activación |
| `ADR-D4` | piso `C_i ≥ 0,50` | declarar la tesis sustantiva implícita y su revisión obligatoria |
| `ADR-D5` | `AVEP` | declarar el objeto **antes** de usar el baremo |

Y cada `ADR` debe contener **los diez campos**, o se convierte en una justificación retrospectiva:

```
   1. decisión vigente
   2. fenómeno que pretende representar
   3. unidad afectada
   4. evidencia que la sostiene
   5. alternativas consideradas
   6. qué está DEMOSTRADO
   7. qué es INFERENCIA
   8. qué permanece NO DETERMINABLE
   9. consecuencias de mantenerla
  10. condición objetiva para revisarla
```

⚠️ **Los `ADR` primero; la implementación después.** El motor no se toca hasta que sus decisiones estén declaradas.

| Después de los cinco `ADR` | |
|---|---|
| **Corregir la capa de publicación** | `D-011`, ya abierta |
| **Declarar el objeto de `AVEP`** | desbloquea `D5` y `D-012` |
| **Ontología FONDO / FORMA** | `REARQUITECTURA` |

## ★ La frontera · dónde termina `GM-Ω` y empieza la construcción

```
  C3            genealogía DEMOSTRADA
  010           dependencia y contexto CLASIFICADOS provisionalmente
  C4            suficiencia metodológica NO DEMOSTRADA
  Gold Master   CONGELADO
  baseline      27,4582 % CONGELADO
  REARQUITECTURA    autorizado para DISEÑO · no para ejecución todavía
```

Y el orden de la construcción, que invierte el hábito de empezar por la fórmula:

```
  1. qué queremos CONOCER
  2. qué EVIDENCIA hace falta para conocerlo
  3. cómo INFERIMOS
  4. …y sólo al final, qué FÓRMULA merece entrar al Gold Master
```

> ### La regla que protege de los dos entusiasmos
>
> **No se rediseña un indicador porque tenga un problema matemático. Se rediseña cuando la relación entre fenómeno, unidad, evidencia, inferencia y resultado deja de estar suficientemente justificada.**

Y las tres cosas que hoy son ciertas **a la vez**, sin contradicción:

| | |
|---|---|
| el motor funciona | ✅ |
| el índice produce un resultado reproducible | ✅ |
| **no se ha demostrado que ese resultado represente adecuadamente el fenómeno que se quiere medir** | ⬜ |

### El cambio de pregunta

| Etapa | Pregunta |
|---|---|
| `GM-Ω` | ¿qué construimos, y cómo llegó a ser lo que es? |
| **`REARQUITECTURA`** | **¿qué debe ser QUIRA para responder correctamente a aquello que queremos conocer sobre la gestión pública?** |

> **La historia ya hizo su trabajo. Ahora no debemos pedirle que diseñe el futuro de QUIRA.**

---
*GM-Ω-ICPI-011-C4 · dictamen sobre 5 decisiones de diseño · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
