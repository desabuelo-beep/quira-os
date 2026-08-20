---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 3, 5, 9, 20]
  type: ARQUITECTONICA
---

# ADR-051 · Autonomía de producción y evolución de plataforma — QUIRA ejecuta sola, o no ejecuta

**Estado:** PROPUESTO · 2026-08-18 — pendiente de aprobación formal de Javo (ADR-035 §5)
**Contexto de origen:** la incorporación de **d07 Transparencia** rompió el `Infrastructure diff = 0`
que la línea base `brn-v2.1` exige (check 12 de la suite BRN). La regla es explícita: *«si cambia
`scripts/`, se abre un ADR de evolución de plataforma, NO se parchea ad hoc»*. Este es ese ADR.
**Relacionado:** ADR-023 (Regla 1/4) · ADR-031 (los SAT se leen, no se generan) · ADR-035 (BRN ·
sólo Javo promueve a vigente) · ADR-038 (CNO/RO/MDN) · ADR-039 (compilador) · Reglas de Oro 1, 3, 7, 9.

---

## Contexto

### Lo que pasó con d07, dicho sin adornos

d07 se construyó **leyendo la Guía Metodológica directamente desde Python**. La periodicidad de cada
numeral la derivaba un script; el plazo del día 15 estaba escrito a mano en `scoring.py`; las
fórmulas de ausencia admitidas eran una constante de módulo; el umbral de cobertura material lo
decidía una función. Todo salía de la norma —ninguno de esos criterios era inventado— pero **ninguno
era verificable**: no tenían cadena, ni SHA, ni consecuencia declarada.

Javo lo detuvo tres veces, cada vez con un caso concreto:

> *«Mal tu contador Director: en solo 3 de 12 meses del 2025 el GAD sube su Presupuesto.»*
> *«En el mismo presupuesto la norma establece ingreso y egresos. El GAD solo reporta egresos.»*
> *«No olvide la BRN, CNO, etc., y lo que aterriza la norma al DOM: eso es la base, por eso
> estábamos trabajando mal.»*

La tercera es la que importa. El glosario BRN define el DOM como la unidad que **«consume RO/SAT; no
conoce Derecho directamente»**. d07 hacía exactamente lo contrario. El resultado fue medible: una
corrida daba `SITA 0,97` con dos conjuntos que no publicaron nada en todo el año, porque el bucle
omitía los períodos ausentes. El criterio estaba mal y **nadie podía verlo**, porque vivía dentro de
una función.

### Por qué la línea base tuvo que romperse

Para medir transparencia hacía falta lo que no existía: capturar una API pública, descargar 936
archivos con integridad, abrir los PDF que los conjuntos de datos enlazan, comprobar que los enlaces
entregan el documento y verificar que el contenido acredita las dimensiones que la norma enumera.
Nada de eso estaba en la plataforma, y ninguna CNO/RO podía producirlo por sí sola.

Es evolución real, no un parche. Y por eso se documenta en vez de tolerarse en silencio.

---

## Decisión

### 1 · Se declara la evolución de plataforma `brn-v2.2`

Las capacidades que d07 incorporó a `scripts/` y `app/agents/d07/` pasan a formar parte de la
plataforma, con una condición: **son servicios de adquisición y verificación de evidencia, y no
contienen criterio normativo alguno.**

| Capacidad | Qué hace | Qué NO decide |
|---|---|---|
| **captura** | consulta la fuente estructurada del órgano rector | qué debe publicarse |
| **adquisición** | descarga con SHA256, reanudable, anti-colisión | si lo descargado cumple |
| **lectura de evidencia** | codificación, delimitador, columnas útiles | si los campos son los exigidos |
| **verificación de enlaces** | resuelve, clasifica procedencia institucional | si un enlace roto es incumplimiento |
| **apertura documental** | extrae texto, clase de acto, correlativo | qué clase de acto exige la norma |
| **orquestación** | encadena etapas y aplica gates | el contenido de los gates |

La frontera es la misma que separa un microscopio de un diagnóstico: **el instrumento no sabe qué
está mirando.** Los parámetros —periodicidad, plazo, formatos, fórmulas de ausencia, dimensiones
materiales— vienen de la RO.

#### 1b · El contrato interno sube a `ROModel 2.1`

Al reescribir d07 apareció el límite que hacía imposible cumplir esta decisión: **`ROModel` no
exponía `parametros`**. Entregaba métrica, tramos de umbral y método — suficiente para una regla de
umbral (d02) o de congruencia (d03), pero no para una que declara periodicidad por conjunto, plazo
de registro, formatos admitidos, fórmulas literales de ausencia y dimensiones materiales.

Sin ese campo, el dominio no tenía de dónde consumirlos **y volvía a derivarlos en Python**. Se
extiende el adaptador —único componente autorizado a conocer el YAML— con un campo al final y con
default: ningún consumidor anterior cambia. Es exactamente el escenario que el propio contrato
previó: *«si cambian las claves, solo cambia este archivo»*.

### 2 · Regla de Autonomía de Producción

Formulación del colega (2026-08-18), adoptada como invariante transversal:

> **1.** Toda función invocable desde UI o comando debe poder ejecutarse **sin Claude**.
> **2.** Ningún criterio normativo puede existir únicamente en un prompt, un script ad hoc o la
> interpretación del operador.
> **3.** El DOM consume CNO/RO/SAT; **no interpreta Derecho**.
> **4.** Los gates son ejecutables por máquina.
> **5.** Un fallo detiene o desvía la cadena según una consecuencia **previamente declarada**.
> **6.** La intervención humana se reserva a lo que el canon marque como validación, promoción,
> excepción o resolución de conflicto.
> **7.** Claude asiste al desarrollo y a la auditoría, pero **no es dependencia de runtime**.

**El punto 2 es el diagnóstico exacto de lo que ocurrió con d07**, y por eso encabeza las
consecuencias verificables de este ADR.

### 2b · Regla de Autonomía Instrumental (añadida el mismo día, tras auditar el propio ADR)

Javo, horas después de firmarse este ADR:

> *«Claude no es QUIRA. Claude puede hacer eso, QUIRA creo que no. Estamos construyendo un
> ecosistema que deberá reportar más adelante 222 municipios, sin Claude, solo QUIRA.»*

La auditoría le dio la razón y dejó al descubierto que **este ADR se estaba incumpliendo desde su
primera línea**: de 31 scripts en `scripts/normativa/`, sólo uno es invocable desde la aplicación.
Captura, descarga, verificación de enlaces, análisis de contenido e inventario existen únicamente
si una persona los ejecuta a mano.

> **Toda capacidad utilizada para producir una observación atribuida a QUIRA debe existir como
> capacidad reproducible, instrumentada y verificable DENTRO de QUIRA. Los resultados obtenidos
> mediante herramientas externas de asistencia, desarrollo o supervisión constituyen evidencia de
> I+D y validación del método, pero no pueden atribuirse a QUIRA como observaciones operativas
> hasta que la capacidad correspondiente haya sido incorporada al pipeline y pueda ejecutarse con
> independencia de esa herramienta.**
> *(formulación del colega, 2026-08-18 · adoptada)*

**Cuatro identidades que no son la misma cosa**, y confundirlas fue el error:

    repositorio  ≠  sistema
    script       ≠  capacidad productiva
    prueba       ≠  observación operativa
    Claude       ≠  QUIRA

Un resultado no se convierte en observación de QUIRA por haberse producido dentro del repositorio
de QUIRA.

**Dónde queda Claude.** No desaparece ni se restringe: **cambia de lugar**. Javo lo fijó al día
siguiente, corrigiendo una lectura demasiado estrecha de esta regla:

> *«Claude no es QUIRA, es parte del equipo de Dylus Lab; puede supervisar todo el trabajo de
> QUIRA de manera independiente. Claude ayuda a construir y evolucionar QUIRA.»*

Es decir: **«QUIRA debe poder operar sin Claude» no significa «Claude no debe volver a usarse».**
Significa que Claude no puede ser una **dependencia operacional invisible**. La arquitectura
correcta separa dos planos que hasta hoy estaban mezclados:

    I+D y evolución        Claude · Javo · el colega · el equipo
            │              diseña, audita, halla errores, escribe reglas y pruebas
            ▼
    reglas · código · pruebas · canon
            │
            ▼
    QUIRA                  ejecuta, produce, conserva procedencia
            │
            ▼
    222 municipios

Claude arriba tiene todo el margen —y esta misma sesión es prueba de su valor: descubrió que el
instrumento recortaba el universo, que se contaban referencias como documentos, que un
`_meta.completo = true` podía mentir—. Lo que no puede es aparecer **abajo**, en el plano de
producción, sin que nadie lo note.

**La prueba de la regla es de escala.** Para un dominio se tolera «Claude + humano + script +
revisión». Para 222 GAD no existe la operación «Claude analiza documentos» multiplicada por 222.
O la capacidad vive en el pipeline, o el ecosistema no existe.

### 2b-bis · Las dos mitades de la misma frase

El colega, cerrando la falsa dicotomía (2026-08-19):

> **La capacidad de Claude no constituye evidencia de capacidad operacional de QUIRA.**
>
> **Una capacidad de QUIRA puede haber sido construida con asistencia de Claude sin que esa
> asistencia forme parte de la operación de producción.**

Las dos frases juntas, y no una sola de ellas. La primera impide atribuir al sistema lo que hizo
la herramienta; la segunda impide el error opuesto —descalificar una capacidad legítima por haber
nacido con ayuda—. Todo el software del mundo se construye con herramientas; lo que importa es si
la herramienta sigue haciendo falta **para operar**.

### 2c · Regla de Atribución de Producción

> **Todo resultado producido durante una intervención asistida debe declarar su procedencia: si es
> resultado de I+D, si fue producido por QUIRA, o si fue validado como reproducible por QUIRA. Las
> tres son legítimas; confundirlas no.**
> *(formulación del colega, 2026-08-19 · adoptada)*

Sin esta regla, el hallazgo verdadero y el hallazgo atribuible se mezclan. Los 636 artefactos
únicos identificados hoy **son un hecho**; que QUIRA los haya identificado **todavía no lo es**. La
diferencia no es retórica: la primera afirmación sostiene una decisión de ingeniería, la segunda
sostiene una publicación institucional ante 222 municipios.

### 2d · Escalera de apropiación · capacidad ≠ ejecución ≠ validación

Tres preguntas distintas que se venían respondiendo como si fueran una:

| Grado | La pregunta | Cómo se acredita |
|---|---|---|
| **capacidad** | ¿QUIRA tiene el código para hacerlo? | el programa existe y está declarado |
| **ejecución** | ¿QUIRA lo invoca y lo corre de verdad? | hay registro de una corrida hecha **por el agente** |
| **validación** | ¿hay prueba reproducible de que lo hace bien desde cero? | una prueba nombrada lo ejercita y pasa |

**Y la escalera no basta por sí sola: le falta el sujeto.** El colega lo señaló al día
siguiente, y es la corrección que impide la ilusión más peligrosa de todas:

> *«La escalera responde "¿qué sabe hacer QUIRA?" pero no "¿sobre quién puede hacerlo?". Hoy
> tenían: QUIRA sabe hacer X + X está configurado para Montecristi. La afirmación completa era
> "esta instancia de I+D sabe hacer X sobre Montecristi".»*

La unidad mínima de una afirmación sostenible es, entonces:

    capacidad + sujeto + ejecución + evidencia + validación = afirmación reproducible

Por eso el sello de cada ejecución registra **sobre quién** se hizo, y el informe del sistema dice
«reproducible sobre 130801 Montecristi», nunca «reproducible» a secas. Una capacidad demostrada
sobre un solo sujeto no es una capacidad nacional, y la cifra tiene que decirlo sola.

**Consecuencia sobre cómo se habla de los 222.** No se puede afirmar *«QUIRA está preparada para
222 municipios»*. Lo que la evidencia sostiene es: *«QUIRA se diseña bajo una arquitectura
parametrizable para su aplicación progresiva a 222 GAD»*. La primera afirma capacidad operacional
nacional; la segunda, una propiedad arquitectónica demostrable. Sólo la segunda es cierta hoy.

**No se salta ningún grado, y ninguno se declara: se deriva de la evidencia.** El grado de una
capacidad lo calcula el sistema mirando qué puede demostrar —igual que la Regla de Oro 3 exige SHA
para admitir un dato—. Una capacidad que se dice «validada» sin prueba que la ejercite es
exactamente el tipo de afirmación que este observatorio existe para no hacer.

Haber ejecutado `analizar_documentos()` sobre el Numeral 10 acredita **ejecución** de esa etapa. No
acredita que QUIRA pueda analizar todo d07 desde cero: eso es **validación**, y requiere su propia
prueba.

### 3 · La cadena obligatoria

```
FUENTE JURÍDICA → CORPUS → CNO → RO → DOM → AGENTE → EVIDENCIA → HALLAZGO
```

Y nunca:

```
FUENTE JURÍDICA → PYTHON → «criterio del programador» → resultado
```

### 4 · Tres niveles semánticos, y la prohibición de saltarlos

Ningún agente puede producir `posible_incumplimiento` sin satisfacer las seis condiciones que
declara la RO. Del nivel 1 al 3 **no se salta**:

| Nivel | Qué afirma | Quién lo produce |
|---|---|---|
| **hecho verificable** | lo que la evidencia muestra | el agente |
| **hallazgo de verificabilidad** | lo que no fue posible verificar | el agente |
| **posible incumplimiento** | calificación normativa | el motor normativo, con las seis condiciones |

### 5 · La IA se justifica, no se presupone

d07 demostró que **no toda autonomía necesita IA**. El meta-catálogo daba tres agentes de d07 por
cognitivos —Portal Navigator, Evidence Collector, Evidence Interpreter— y en pausa por presupuesto de
API. Resultaron determinísticos, porque la fuente canónica (`OBS-QNKC-02`) es una API estructurada y
no un portal que haya que navegar. **Costo cero, y el dominio puede correr sin presupuesto.**

Regla: si la decisión está completamente determinada por CNO + RO + reglas de evidencia, **meter un
modelo en medio es un defecto arquitectónico**, no una virtud: añade costo, latencia y una superficie
de interpretación que el canon no autorizó.

### 6 · Lo que este ADR **no** decide

- **No promueve nada a `vigente`.** `CNO-VII-001`, `RO-VII-001` y `RO-VII-002` siguen `propuesta`.
- **No crea un SAT de transparencia.** `SAT_Catalogo` no lo tiene y la BRN no genera señales del
  motor (ADR-031 · Regla 1).
- **No crea canon paralelo.** Nada de MVM ni matrices alternativas: se enriquece la BRN existente.

---

### 7 · Las cinco pruebas de apropiación (colega, 2026-08-19)

Antes de atribuir a QUIRA el análisis del universo documental, el dominio debe superar cinco
pruebas. Su estado es medido, no declarado:

| | Prueba | Qué demuestra | Estado |
|---|---|---|---|
| **A** | `fuente → captura → descarga → SHA` | QUIRA **obtiene** sola | escrita y desactivada (`QUIRA_PRUEBA_DE_ORIGEN=1`) |
| **B** | `ZIP → hijos → SHA → padre/hijo` | abrir no desprende al hijo de su procedencia | ✅ verde |
| **C** | publicación ≠ objeto físico, sin perder apariciones | deduplicar no borra la historia | ✅ verde |
| **D** | timeout · 404 · tope · no alcanzado | un fallo de captura **no es una ausencia** | ✅ verde |
| **E** | borrar los derivados y reconstruir | QUIRA **procesa** sola, y de forma reproducible | ✅ verde |

**A es la que falta**, y es la mitad de la cadena que sigue dependiendo de que alguien haya traído
los archivos alguna vez. No se activa en la suite ordinaria porque golpear el portal del GAD en
cada `pytest` sería usar al sujeto observado como banco de ensayo.

### 8 · Consecuencia inmediata: los 636 artefactos esperan

La recomendación del colega se adopta:

> *«Yo NO abriría todavía los 636 para hacer el análisis normativo completo. No porque no sea
> necesario, sino porque acabamos de descubrir una deuda arquitectónica más importante.»*

Abrirlos ahora produciría un resultado correcto y **no atribuible**: sería I+D, no observación de
QUIRA (§2c). El orden es al revés — primero la apropiación, después el universo—, y entonces la
afirmación que se podrá publicar es de otra naturaleza:

> QUIRA inspeccionó materialmente 636 artefactos físicos únicos, conservando sus 935 apariciones
> de publicación, y confrontó cada uno contra la exigencia normativa correspondiente.

Eso ya no lo dice Claude. Lo dice el sistema, y se puede repetir 222 veces.

### 9 · Autonomía no es ausencia de decisión humana

Ajuste convergente (director y colega, 2026-08-19). La Prueba A hablaba de adquisición «sin
intervención humana», y esa formulación era incorrecta:

    decisión humana / calendario     ← QUÉ observar, CUÁNDO, bajo qué política
              ↓
            QUIRA                    ← CÓMO: adquiere · procesa · valida · conserva procedencia
              ↓
      estado de evidencia → reporte

La persona decide **cuándo y bajo qué política**. No decide cómo descargar un ZIP, cómo calcular
un SHA, cómo abrir un PDF ni cómo clasificar un tiempo agotado. Un sistema que se despierta y
empieza a golpear portales públicos porque puede no es más autónomo: es menos gobernable, y sobre
222 sujetos observados eso es un problema, no una virtud.

Lo que la Prueba A debe demostrar, entonces, es que **una sola orden basta** — no que no haya
orden.

### 10 · Material de ingeniería ≠ observación de QUIRA

Precisión del colega sobre la decisión de no abrir los 636 todavía:

> *«No es simplemente "no los abramos porque Claude lo haría". Es: no confundamos conocimiento
> producido durante I+D con conocimiento producido por el sistema que estamos construyendo.»*

Los 636 artefactos **sí deben usarse ya**, y con intensidad, como material de ingeniería:
clasificadores, fixtures, casos límite, pruebas de padre/hijo, casos de ZIP, de PDF, de captura
incompleta. Lo que no pueden ser todavía es **el resultado oficial de observación**.

    I+D → construcción de capacidad → validación → observación QUIRA → hallazgo

Usar el material para construir la capacidad es correcto. Publicarlo como si la capacidad ya
existiera es lo que la §2c prohíbe.

### 11 · Criterio rector · Montecristi es el laboratorio, no el destinatario

> *«No debemos construir d07 para Montecristi. Debemos utilizar Montecristi para construir el
> patrón que permita ejecutar d07 sobre 222 GAD.»* — colega, 2026-08-19

La medición del mismo día mostró que se estaba haciendo lo contrario: **la identidad del sujeto
observado vivía en once puntos de código** (OBS-032). Se corrigieron seis —el identificador en la
API de la Defensoría, el dominio web y su uso como criterio de procedencia, el nombre del
municipio— trasladándolos a `data/sujetos/` con `app/agents/sujeto.py` como única puerta. Quedan
cinco, todos rutas de archivo, y una prueba impide que el número suba.

**El «1 de 7 validada» no es un mal resultado: es el resultado que queremos ver.** Significa que
QUIRA empezó a producir un mapa explícito de sus propias capacidades en vez de suponerlas. La
cadena estará operacionalmente apropiada cuando las siete lo estén; y sólo entonces empieza la
prueba interesante —el mismo patrón contra 222 portales distintos, con sus Nextcloud, sus ZIP, sus
enlaces muertos y sus cambios mensuales.

### 12 · Las cinco dimensiones, y la frase que las une

El colega, cerrando la línea (2026-08-19), corrigió una simplificación de §2d: **el sujeto no es
un cuarto nivel de madurez, es una dimensión de alcance**, y el grado de apropiación es una
*función derivada* de las dimensiones, no una dimensión más.

| Dimensión | Pregunta | Cómo se acredita |
|---|---|---|
| **Capacidad** | ¿puede hacerlo? | el código existe y está declarado |
| **Sujeto** | ¿sobre quién puede afirmarlo? | perfil declarado en `data/sujetos/` |
| **Ejecución** | ¿lo hizo realmente? | sello de una corrida propia |
| **Evidencia** | ¿qué prueba sellada conserva? | insumos y salidas con SHA |
| **Validación** | ¿puede reproducirse? | una prueba nombrada que existe y pasa |

Esa distinción resolvió un defecto concreto: mientras el grado fue un dato independiente, el
sistema **pudo perder el sujeto al construir la etiqueta**, y lo hizo el mismo día en que se
añadió. Ahora es estructuralmente imposible: una afirmación `ejecutada` o `reproducible` sin
sujeto no se construye —lanza `AfirmacionSinSujeto`— y una ejecución sellada sin sujeto **se
degrada** a `capacidad` en vez de suponer el ámbito.

> **Ninguna capacidad puede afirmarse sin sujeto; ninguna ejecución sin sello; ninguna evidencia
> sin procedencia; ninguna validación sin prueba; y ningún fallo puede atribuirse al objeto
> observado mientras el mecanismo que produjo esa atribución permanezca sin falsar.**
> *(síntesis del colega, 2026-08-19 · adoptada — une OBS-030, OBS-031, OBS-032, ADR-042 §6-bis y
> este ADR sin añadir doctrina nueva)*

### 13 · El perímetro propio es un artefacto, no una pantalla

`app/agents/apropiacion.py::sellar_autoconocimiento` deriva y persiste
`data/quira/autoconocimiento.json` con SHA del estado, fecha de derivación, fuentes declaradas y
esta leyenda:

    NO DECLARADO MANUALMENTE · DERIVADO POR QUIRA

El SHA se calcula sobre el contenido sin la fecha: dos derivaciones del mismo estado dan el mismo
hash, de modo que se distingue **«el sistema cambió»** de **«el reloj avanzó»**. Es la misma
exigencia de procedencia que QUIRA le impone al sujeto observado, aplicada a sí misma en vez de
eximirse de ella.

## Consecuencias

### Verificables (se convierten en invariantes de la suite)

1. **Ningún módulo de dominio contiene un criterio normativo literal.** Periodicidad, plazos,
   formatos, fórmulas de ausencia y dimensiones materiales se leen de la RO vía el adaptador.
2. **Ningún agente emite `posible_incumplimiento`** sin las seis condiciones satisfechas.
3. **Toda corrida produce identidad**: `run_id`, SHA del canon utilizado, gates y estado.
4. **Un gate fallido produce `BLOCKED` con causa**, y no un resultado degradado.
5. **Cada corrección manual descubierta en una corrida** termina como regla, gate o prueba antes de
   considerar autónomo el dominio.

### Deuda saldada el mismo día

- **d07 consume la RO.** `app/agents/d07/reglas.py` es la única puerta por la que el dominio conoce
  la norma, y ni siquiera lee el YAML: eso sólo lo hace el `ROAdapter`. Migrados: la periodicidad por
  conjunto y la regla de cadencia condicionada (salían de un script que leía el `.docx`), el plazo del
  día 15 (estaba a mano en `scoring.py`), los formatos de datos abiertos, las fórmulas de ausencia,
  el muestreo cualitativo, el criterio de período no publicado, las dimensiones materiales y los
  grupos del clasificador presupuestario (eran constante de módulo).
- **El orquestador tiene gate `REGLAS`**: sin Regla Operativa disponible, la corrida se detiene en
  vez de improvisar; y si las reglas están en `propuesta`, el resultado lo declara.
- **Ocho invariantes nuevos en la suite** (`tests/test_d07_autonomia.py`, 26 pruebas) hacen
  verificable esta decisión: si alguien reintroduce el clasificador en el módulo, o pone un valor por
  defecto donde falta la RO, la prueba falla.

- **`CNO-VII-002` + `RO-VII-003` cierran el art. 24** el mismo día. Con ellas se migró lo último
  que quedaba: las clases de acto (acta ≠ resolución), los tipos de sesión admitidos, el patrón de
  la serie correlativa y el tratamiento del documento no procesable. **`documentos.py` ya no
  declara ningún criterio normativo.**

### Lo que queda en el código, y por qué es correcto

- **`campos.py` conserva sus umbrales de similitud.** Son heurística de lectura —como el
  delimitador o la codificación—, no criterio normativo: la ley dice qué campos exige, no con
  cuánto parecido léxico se reconoce un encabezado. Queda declarado en el módulo para que la
  frontera sea visible y nadie los confunda con exigencia legal.
- **`scoring.py` conserva los valores del Instructivo como respaldo**, para que el motor siga
  siendo usable de forma aislada. En una corrida real mandan los de la RO, que el orquestador pasa.

### Deuda que sigue abierta

- **`CNO-VII-003/004`** — transparencia pasiva (SAIP) y deber de difusión y capacitación.
- **El OCR** sigue sin instalarse y bloquea 123 documentos del numeral 17. Vía local, sin API.
- **Promoción a `vigente`** — las cinco piezas de d07 están en `propuesta`; sólo Javo las promueve.
- **El meta-catálogo de agentes está desactualizado**, y eso ya produjo un juicio equivocado: marcaba
  `NLP Video RDC Agent` como pendiente cuando la capacidad está desplegada y d09 cerrado. Un mapa que
  miente sobre lo que existe es peor que no tenerlo.
- **Faltan `CNO-VII-002/003/004`** (art. 24 · transparencia pasiva · difusión y capacitación).
- **El OCR sigue sin instalarse** y bloquea la lectura de 123 documentos del numeral 17. La vía es
  local (Tesseract), sin costo de API.

### Riesgo asumido

La plataforma crece, y con ella la superficie que hay que mantener conforme. Se acepta porque la
alternativa es peor: sin estas capacidades, d07 no puede abastecer a los demás dominios — y `d07` es,
según el propio ACK `lotaip_f02`, la **ventana observacional** por la que d01, d02 y d09 ven su
propia materia. Javo lo dijo antes de que el canon lo confirmara:

> *«De este DOM depende toda la información que entra a todo el sistema de QUIRA. Si este DOM no
> cumple las condiciones necesarias, QUIRA no podrá desarrollar su labor.»*

---

## Trazabilidad

| Elemento | Referencia |
|---|---|
| Invariante roto que origina el ADR | suite BRN · check 12 · `Infrastructure diff = 0` vs `brn-v2.1` |
| Cadena normativa de d07 | `CNO-VII-001` · 12 eslabones · 12/12 SHA verificados |
| Parámetros extraídos del código | `RO-VII-001` (periodicidad, plazo, formatos, ausencia, muestreo) |
| Cobertura material | `RO-VII-002` (dimensiones, clasificador, tres estados) |
| Subsanación de corpus | 8 chunks · respaldo en `data/backups/corpus_articulo_num_20260818.json` |
| Naturaleza observacional | ACK `lotaip_f02.yaml` · campo `OBSERVA_CAPA` · `observa_capas` en la CNO |

---
*ADR-051 · Dylus Lab © 2026 · «QUIRA ejecuta sola dentro de límites declarados — eso es autonomía; hacerlo sin ellos sería otra cosa.»*
