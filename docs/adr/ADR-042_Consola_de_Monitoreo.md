---
id: ADR-042
authority:
  parent: ADR-041
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: APROBADO — sellado por Javo (2026-08-07)
fecha: 2026-08-06
---

# ADR-042 · La Consola de Monitoreo · capa de adquisición del Observatorio

> **Decisión de Javo (2026-08-06)**, sobre revisión del colega y evaluación crítica del
> director. Se cierra la arquitectura conceptual ANTES de seguir construyendo: ningún
> cambio nace en Python (Regla 9). Este documento define el modelo; el código lo
> implementa después.

## 1 · Por qué se abre este ADR

El Observatorio recibió primero un «Panel del Observatorio»: un tablero de lectura con
cifras contadas de los registros. Estaba mal encuadrado, y la corrección de Javo lo dice
sin rodeos — lo que hace falta no es una pantalla para mirar sino **la mesa desde la que
se opera la vigilancia mensual y progresiva de los 222 GAD**.

Al intentar emplazarla aparecieron tres confusiones que este ADR resuelve:

1. **Observatorio ≠ Operaciones.** El director alojó la consola dentro del ambiente de
   mantenimiento técnico razonando que evitaba duplicar. Degradaba el producto principal
   a herramienta de soporte.
2. **La consola no es un dominio, ni un dominio la contiene.** Son capas distintas.
3. **No todo converge en el Gold Master.** El diagrama propuesto hacía desembocar toda la
   captura en el motor de cálculo, lo que contradice ADR-023.

## 2 · La cadena completa

```
FUENTES PÚBLICAS                          QUIRA CIUDADANA
(CNE · Transparencia · CPCCS ·            (evidencia aportada
 SERCOP · Web GAD · otras)                 desde el territorio)
        └───────────────┬───────────────────────┘
                        ↓
                  OBSERVATORIO
        la capacidad institucional de vigilancia
                        ↓
              CONSOLA DE MONITOREO
     coordina corridas de captura, proceso y validación
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
  CORPUS + GRAFO                  insumos numéricos
  evidencia documental                    ↓
        └────── MATRIZ_CANONICA ────→ GOLD MASTER
                  (el contrato)       (calcula métricas)
                        ↓
                 MOTORES DE QUIRA
                        ↓
              DOM d01 · d02 · … · d12
          unidades de conocimiento por dominio
                        ↓
        CENTRO DE INTELIGENCIA TERRITORIAL
              donde se consulta y se relaciona
                        ↓
                    QUIRA IA
        conversa y explica en lenguaje natural
        ┌───────────────┴───────────────┐
        ↓                               ↓
  usuario del Observatorio      usuario de Ciudadana
```

## 3 · Qué es cada cosa — y qué NO es

| Capa | Es | No es |
|---|---|---|
| **Observatorio** | la **función** institucional de vigilancia y adquisición de evidencia | una pantalla, ni un tablero |
| **Consola de Monitoreo** | la **infraestructura operativa** que ejecuta esa función | un producto que se le enseña a un alcalde |
| **Corpus + Grafo** | el **universo de evidencia** documental, con su huella | una base de métricas |
| **Gold Master** | el **núcleo de cálculo** de métricas | un repositorio de documentos |
| **MATRIZ_CANONICA** | el **contrato de integración** entre ambos universos | una tabla auxiliar |
| **DOM** | la **unidad de conocimiento** por dominio | un informe, ni un resultado suelto |
| **Centro** | la **capa de consulta** y articulación | el sitio donde se opera |
| **QUIRA IA** | la **capa conversacional**: explica en lenguaje natural | una fuente de cifras |

### 3-bis · El punto de integración es la MATRIZ, no el Gold Master

ADR-023 lo fija literalmente: **«Excel = motor · Corpus = evidencia verificable del
motor»**, y la MATRIZ_CANONICA es *«el contrato semántico entre el Motor y QUIRA — la
tabla de correspondencia entre el universo Excel y el universo documental»*.

Son **dos universos**. Un documento capturado del portal de transparencia **no entra al
Gold Master**: entra al corpus con su huella. Lo que llega al motor son los insumos
numéricos ya previstos en la matriz.

Decir «todo se integra en el Gold Master» invitaría a meter documentos en un libro de
cálculo de 123 hojas, y a que el motor deje de ser el motor.

### 3-ter · La cadena cierra en QUIRA IA, y explica sin calcular

El recorrido no termina en el Centro. Termina cuando una persona —del Observatorio o de
Ciudadana— **pregunta y entiende**.

> **Precisión de Javo (2026-08-06):** esto **no es nuevo**. QUIRA IA está planificada
> desde hace tiempo como una de las capas finales, junto con GeoTwin, y su organigrama de
> agentes ya está escrito en `docs/architecture/META_CATALOGO_AGENTES.md` —28 piezas con
> su tipo, estado y dependencias—, con la ruta en `governance/HOJA_DE_RUTA_MAESTRA.md`.
> Se incorpora a este ADR porque **faltaba en la cadena**, no porque se acabe de decidir.
>
> El problema real que esto revela no es de planificación sino de **integración**: las
> piezas están consensuadas y avanzadas, pero al trabajarlas por separado cada una vuelve
> a parecer un descubrimiento. Antes de proponer algo, se consulta la Hoja de Ruta y el
> Meta-Catálogo — ahí suele estar ya.

QUIRA IA conversa en **lenguaje de administración pública y desarrollo territorial** sobre
el cantón que se monitorea, y bebe de cuatro sitios: el corpus normativo, el corpus
metodológico, los análisis y los resultados de los dominios. Responde lo que se le
pregunte sobre ese territorio.

**Y no calcula.** Esta es la frontera, y es la misma que la portada declara públicamente:
*la cifra no la produce la inteligencia artificial*. QUIRA IA **lee, relaciona, cita y
explica**; los números salen del motor y la evidencia del corpus. Si la capa
conversacional produjera una cifra propia, se convertiría en una segunda fuente de verdad
—lo que prohíbe el Art. 3 de la Constitución Institucional— y todo el trabajo de
reproducibilidad quedaría anulado en la última pantalla.

De ahí tres obligaciones para esta capa:

1. **Cita siempre.** Cada afirmación remite a la norma o al documento que la sostiene.
2. **Declara el nivel de verificabilidad** de lo que dice (los cinco niveles del canon), y
   dice «no hay evidencia» cuando no la hay, en vez de completar el hueco.
3. **No emite juicio jurídico.** Explica qué muestra la evidencia; calificar un
   incumplimiento no le corresponde a QUIRA.

Es la cuarta lente del frame (ADR-037 · *Inteligencia: ¿por qué?*), hoy en preparación.

## 4 · Las seis preguntas que la consola debe responder

Son el requisito funcional, tomado de la formulación de Javo — *«todo lo que un humano
debería tener para poder realizar este trabajo de manera automatizada pero con rigor
técnico y científico»*:

1. **¿Qué fuentes se monitorean?** — con su capturador, su cadencia y su estado real.
2. **¿Qué corrida se está ejecutando?** — municipio, dominio, fuente, período,
   procedimiento, modelo, versión y estado.
3. **¿Qué evidencia se obtuvo?** — documentos, huellas, marcas de tiempo, ausencias, y
   qué cambió respecto de la captura anterior.
4. **¿Qué validación ocurrió?** — qué propuso la máquina, qué observó la supervisión
   metodológica y qué acreditó la persona.
5. **¿Qué pasó con la corrida?** — con la semántica de estados del §6.
6. **¿Cuánto costó?** — costo de la corrida y acumulado del mes.

La sexta no es administrativa: en una infraestructura que debe escalar de un municipio a
222 con financiamiento propio, **el costo es parte de la trazabilidad operativa**. Una
corrida que no se puede pagar no se puede repetir, y un método que no se puede repetir no
es un método.

## 5 · Quién hace qué — y por qué el orden importa

```
fuente → HAIKU → OPUS → HUMANO → evidencia acreditada
```

| Actor | Función | Límite |
|---|---|---|
| **Haiku** | ejecuta: extrae, clasifica y normaliza según el procedimiento | opera sobre volumen; no decide qué es verdad |
| **Opus** | supervisa el **procedimiento**: muestras, inconsistencias, desviaciones metodológicas | **no es una segunda fuente de verdad** |
| **Humano** | **acredita**: decide qué hallazgo queda validado y publicable | es la única autoridad de validación |

La precisión sobre Opus importa y es del colega: decir «Opus corrige a Haiku» lo
convertiría en una segunda máquina de verdad, que es exactamente lo que prohíbe el
Art. 3 de la Constitución Institucional —*la inteligencia artificial no constituye fuente
de verdad institucional*— y lo que fija ADR-035. Opus revisa **cómo se hizo el trabajo**,
no **qué dice el territorio**.

### 5-bis · La primera corrida de 2025 es de CALIBRACIÓN, no de producción

Se registra como **corrida de calibración metodológica**. Su finalidad no es producir
cifras publicables sino **demostrar que el procedimiento funciona**, detectar sus errores
y medir su comportamiento antes de automatizarlo a escala.

Consecuencia práctica: lo que salga de esa corrida **no se publica como hallazgo** hasta
que el procedimiento quede acreditado. Confundir una calibración con producción sería
publicar cifras cuyo método todavía se estaba probando.

## 6 · Semántica de estados — la distinción que sostiene la tesis

**«No existe evidencia» ≠ «no pude obtener evidencia» ≠ «el capturador falló».**

Es la regla más importante de este ADR. Si un portal cambia su HTML y el conector deja de
funcionar, QUIRA **no puede convertir ese fallo técnico en una afirmación sobre la gestión
pública**. Sería exactamente el tipo de aseveración que este sistema existe para no hacer.

| Estado | Qué afirma | ¿Dice algo del sujeto observado? |
|---|---|---|
| `capturada` | el artefacto se obtuvo de la fuente | no todavía |
| `procesada` | se extrajo y estructuró su contenido | no todavía |
| `pendiente_validacion` | la máquina propuso; falta acreditación humana | **no** — nada se publica aquí |
| `validada` | una persona la acreditó contra la fuente | **sí** |
| `evidencia_ausente` | la fuente respondió y **no hay nada publicado** | **sí**, y es un hallazgo |
| `fuente_no_disponible` | la fuente no respondió | **no** — habla de la fuente |
| `capturador_degradado` | la fuente respondió pero el formato cambió | **no** — habla de nuestro instrumento |
| `error_tecnico` | falló algo nuestro | **no** — habla de nosotros |

Los cuatro últimos estados **no son juicios sobre la gestión**. Solo `evidencia_ausente`
lo es, y aun así se enuncia como lo que es —ausencia de publicación registrada—, nunca
como incumplimiento: calificar jurídicamente no le corresponde a QUIRA.

Esta tabla es la aplicación operativa del Principio Rector: *la ausencia de evidencia es
un RESULTADO de auditoría, nunca autorización para inferir hechos*.

### 6-bis · Regla de atribución de evidencia — falsar el mecanismo antes de culpar al objeto

La tabla anterior clasifica los estados. Esta regla dice **qué hacer antes de asignarlos**:

> **Antes de atribuir un fallo al objeto observado, debe falsarse el mecanismo que produjo la
> afirmación sobre ese objeto.**
> *(formulación del colega, 2026-08-19 · adoptada)*

Vive aquí, en el nivel normativo, y no dentro de una observación concreta: se aplica igual al Gold
Master, al CNE, al CPCCS, al SERCOP, al portal de un GAD y a cualquier verificador futuro, sin
necesidad de redactar doctrina nueva cada vez. Las observaciones que la originaron son su
**evidencia histórica**, no su enunciado:

| | Lo que el mecanismo afirmó | Lo que se probó al falsarlo |
|---|---|---|
| **OBS-030** | «el portal de la Defensoría está caído» durante seis días | funcionaba; el defecto era una VPN en el observador |
| **OBS-031** | «al Gold Master le faltan 14 claves» durante tres meses | 30/30 reglas OK; el defecto estaba en el aparato de prueba |

Es la misma epistemología en dos niveles: en el primero se equivocaba el instrumento de captura,
en el segundo el instrumento de verificación. En ambos, **la culpa viajaba hacia afuera** — hacia
el sujeto observado o hacia el artefacto canónico— y en ambos el error era propio.

**Por qué es una regla de atribución y no una práctica de QA.** Un fallo mal atribuido no produce
un error técnico: produce una **afirmación falsa sobre un tercero**, y en este sistema esos
terceros son instituciones públicas. La Regla de Oro 1 (*Excel = Estado*) queda protegida por el
mismo mecanismo: ante nueve pruebas en rojo, el camino natural era «corrijamos el Excel», y se
habría modificado un artefacto sano para satisfacer una prueba obsoleta.

**Corolario de grado epistemológico** (colega, 2026-08-19):

> **Una afirmación de fallo no puede tener mayor grado epistemológico que el mecanismo que la
> produjo.**

Ante `Gold Master 30/30 OK` y `pruebas FAIL`, la lectura correcta no es «el Excel es sospechoso»
sino:

    la afirmación «el Excel falla»       → sospechosa
    el verificador que la produjo        → bajo revisión

Y es generalizable a toda la cadena. Cuando QUIRA afirma **«el GAD no publicó X»**, debe poder
responder, capa por capa:

    ¿qué fuente?              ¿qué captura?          ¿qué estado de adquisición?
    ¿qué evidencia?           ¿qué verificador?      ¿qué prueba de ese verificador?
    ¿sobre qué sujeto?

**Si alguna capa no puede responder, la afirmación se degrada** —al estado que la evidencia sí
sostiene— en lugar de fabricar certeza. Es la contrapartida exacta del Principio Rector: así como
la ausencia de evidencia no autoriza a inferir hechos sobre el sujeto, la ausencia de procedencia
no autoriza a inferir solidez sobre la propia afirmación.

Esta regla ya opera en código: una capacidad con sello de ejecución pero **sin sujeto declarado**
no se eleva a «ejecutada» — baja a «capacidad», y lo dice.

**No basta con que exista evidencia: debe existir evidencia que responda la cadena
pertinente.** La regla es ejecutable, no una recomendación — vive en
`app/agents/procedencia.py` y toda afirmación de un DOM pasa por ella:

| Peso | Qué afirma | Capas que exige |
|---|---|---|
| `hecho_verificable` | algo **del sujeto observado** | las siete |
| `hallazgo_de_verificabilidad` | algo de **nuestra capacidad de verificar** | fuente · captura · estado · sujeto |
| `no_determinable` | nada | — |

La capa `prueba_del_verificador` **se comprueba, no se cree**: citar una prueba inexistente
acreditaría un criterio sin nada que lo respalde. Y cuando una afirmación se degrada, el registro
dice **desde qué peso y qué capas lo impidieron** — «se degradó» sin causa es media respuesta, y
la mitad que falta es la accionable.

**LA REGLA, en su formulación final** (colega, 2026-08-19):

> **QUIRA no completa una afirmación cuando la cadena de evidencia está incompleta: la degrada
> hasta el máximo grado que la evidencia permite sostener. Ninguna transformación de evidencia
> puede aumentar el grado epistemológico ni perder el sujeto de la afirmación.**

**Deuda declarada y medida — el vínculo prueba↔verificador.** La escala completa es
`declarado ≠ existente ≠ ejecutado ≠ exitoso`, y hoy sólo se cubren los dos primeros escalones:
la cadena comprueba que la prueba **exista**, no que **corresponda** al verificador que dice
respaldar. Hoy cualquier prueba real acredita cualquier verificador. Queda fijado en
`test_05_la_prueba_deberia_estar_vinculada_al_verificador_que_respalda`, que documenta el hueco
en verde: el día que el vínculo sea comprobable, se invierte la aserción y pasa a defender la
regla en vez de registrar su ausencia. Es la misma epistemología que se le exige al GAD, aplicada
a nosotros.

### La asimetría: cuándo se degrada y cuándo se bloquea

Los ataques del 2026-08-19 separaron dos cosas que la escala «bueno/malo» confundía:

    FALTA DE EVIDENCIA          →  DEGRADACIÓN   la afirmación pesa menos
    CONTRADICCIÓN DE IDENTIDAD  →  BLOQUEO       la afirmación no se emite

Falta de fuerza epistemológica no es lo mismo que atribución incorrecta. Ante una cadena
incompleta todavía queda conocimiento parcialmente sostenible —«no fue posible acreditarlo» es un
resultado de auditoría legítimo—. Ante evidencia de otro sujeto no hay nada que sostener: **el
sistema no tiene derecho a transformar evidencia de A en conocimiento sobre B.**

Y la distinción que lo hizo visible:

> **Integridad del artefacto ≠ integridad de la atribución.** El SHA demuestra que el archivo no
> cambió; no demuestra que ese archivo corresponda al sujeto que QUIRA dice estar observando.

**Los dos ataques que lo probaron.** Ambos dejaban todos los gates en verde y la corrida
`COMPLETED`:

| | Ataque | Antes | Ahora |
|---|---|---|---|
| 8 | alterar el sujeto del sello | mide 130801 y afirma sobre 130802 | `BLOCKED` |
| 9 | cambiar `dpe_entidad_id` sin tocar el nombre | mide con evidencia de la entidad 937 declarando observar la 999 | `BLOCKED` |

El segundo entró por donde el primer arreglo no miraba: el gate comparaba una **etiqueta legible**
y el nombre no cambia al cambiar el identificador en la fuente. De ahí `sujeto.huella()`: *una
etiqueta identifica para leer; una huella identifica para verificar.*

**La invariante de identidad epistemológica**, hermana del invariante estructural que impide
construir una afirmación ejecutada sin sujeto:

    sujeto_sello = sujeto_activo = sujeto_de_la_afirmación

**Corolario operativo.** Una prueba que falla siempre no protege nada: un rojo permanente es
funcionalmente idéntico a no tener prueba, con el agravante de que aparenta cobertura.

## 7 · La relación fuente↔dominio es de muchos a muchos

**No** existe correspondencia rígida `SERCOP → d02`. Una fuente aporta evidencia a varios
dominios; un dominio necesita evidencia de varias fuentes. El mandato electoral, por
ejemplo, solo puede contrastarse cruzando el plan de trabajo del CNE con la planificación
y con lo efectivamente contratado.

Es lo que distingue una infraestructura de conocimiento de un conjunto de raspadores con
destino fijo. La consola declara **de dónde puede venir** la evidencia; cada dominio
decide cuál admite.

## 8 · Reglas que este ADR fija

1. **Ningún DOM depende de la consola para ser inteligible.** Un dominio se entiende por
   sí mismo; la consola explica de dónde salieron sus datos, no qué significan.
2. **Ninguna consola se convierte en un DOM.** Opera, no interpreta.
3. **Ningún DOM es fuente de verdad de otro DOM.** El contrato de integración es la
   MATRIZ_CANONICA.
4. **La cobertura pertenece al dominio; la corrida, a la consola.** Son dos vistas del
   mismo dato: el dominio pregunta *«¿qué cobertura tiene mi evidencia?»* y la consola
   *«¿qué corrida la produjo y qué ocurrió durante ella?»*.
5. **La consola no publica.** Produce evidencia acreditable; publicar es decisión humana.

## 9 · Consecuencias

- El Observatorio es un **ambiente propio** (`quira_pages/env_obs.py`), separado del de
  mantenimiento técnico.
- La Consola de Monitoreo es su pantalla de trabajo
  (`quira_pages/p_monitoreo_fuentes.py`).
- La semántica de estados del §6 debe existir **en código** antes de la primera corrida:
  sin ella, un fallo de capturador podría llegar a un informe como si fuera un hallazgo.
- El costo por corrida debe registrarse desde la primera, no añadirse después.
- QUIRA Ciudadana **no es un segundo observatorio**: es la otra vía de adquisición hacia
  el mismo sistema de conocimiento (ADR-041 §3).

## 10 · Lo que este ADR NO decide

- **Qué dominios se curan primero.** Sigue siendo el Protocolo de Curación.
- **El estatuto del aporte ciudadano** como evidencia — queda abierto en ADR-041 §6.
- **La interfaz de QUIRA IA**, más allá de la frontera fijada en §3-ter. El organigrama
  de agentes ya existe y no se rehace aquí: `docs/architecture/META_CATALOGO_AGENTES.md`.

- **Cuándo se reactiva la Fase 4.** Los agentes están en pausa por presupuesto, y la vía
  sin costo de API ya está registrada (idea de Javo, 2026-07-24): inferencia local con
  `llama-cpp-python` y modelos GGUF. Este ADR no decide si se adopta.

---
*ADR-042 · Dylus Lab © 2026 · propuesto por el director sobre revisión del colega,
consolidado por Javo (2026-08-06)*
