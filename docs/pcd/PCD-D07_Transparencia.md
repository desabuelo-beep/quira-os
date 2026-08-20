---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 9]
  type: NORMATIVA
---

# PCD-D07 · Transparencia y Acceso a la Información (QINV-007)

> **Expediente de Curación de Dominio** — aplicación del `PROTOCOLO_CURACION_DOMINIO.md`.
> Sesión 2026-08-17/18 · Director: Claude · Fundador: Javo · Asesor externo.
> *«¿Por qué Transparencia quedó exactamente así?»* — aquí está, incluidos los errores.

> ## ⚠️ ESTADO: EN CURACIÓN — reabierto el 2026-08-18
>
> Este expediente se declaró **CERRADO** y hubo que reabrirlo el mismo día. Javo:
>
> > *«No se ha completado el trabajo en este DOM hasta que no se haga el análisis completo de
> > todo el universo documental. Este DOM debe quedar impoluto e inexpugnable para que pueda
> > nutrir a todo el sistema de QUIRA.»*
>
> Tenía razón. El cierre decía «CERRADO **al nivel de lo que el canon hoy sostiene**», y esa
> salvedad era una coartada: el canon sostiene los 417 documentos accesibles, no los 246 que se
> habían abierto. **El 41% del universo documental estaba sin leer.**
>
> Un dominio que abastece al resto del sistema no puede cerrarse con la mayor parte de su
> evidencia sin abrir. Queda `EN CURACIÓN` hasta completar el inventario.

## Estado inicial

El dominio tenía catálogo canónico (`CD-01`…`CD-24`), un motor determinístico de scoring con la
fórmula del Instructivo (`SITA = (CTA+ETA+RP+CI)/4`) y un contrato de evidencia (`EvidenciaCD`).
Lo que **no** tenía era con qué llenar ese contrato: `evidencia.py` estaba sin implementar, en
pausa por presupuesto de API, porque el pipeline suponía tres agentes cognitivos —Portal
Navigator, Evidence Collector, Evidence Interpreter—.

Y no tenía la vara. El catálogo enumeraba los conjuntos de datos pero no su periodicidad, ni sus
campos exigidos, ni la regla de ausencia. **Sin vara no hay medición** (Regla 3).

## Hallazgos

### 1 · El error de método, y es el hallazgo insignia

El dominio se construyó **leyendo la Guía Metodológica directamente desde Python**. La
periodicidad la deducía un script del `.docx`; el plazo del día 15 estaba a mano en `scoring.py`;
las fórmulas de ausencia eran una constante de módulo. Ninguno inventado —todos salían de la
norma— pero **ninguno verificable**: sin cadena, sin SHA, sin consecuencia declarada.

Javo lo detuvo tres veces, cada una con un caso concreto, y la tercera dio con la raíz:

> *«No olvide la BRN, CNO, etc., y lo que aterriza la norma al DOM: eso es la base, por eso
> estábamos trabajando mal.»*

El glosario BRN define el DOM como la unidad que **«consume RO/SAT; no conoce Derecho
directamente»**. d07 hacía exactamente lo contrario, y por eso todo resultado sonaba arbitrario
por más pruebas que se le pusieran: **el criterio lo ponía el programador**.

### 2 · Errores de medición que la disciplina cazó

| Error | Consecuencia | Cómo se detectó |
|---|---|---|
| contar meses con *alguna* publicación | «12/12 meses» en un año con numerales sin publicar | Javo: *«en solo 3 de 12 meses sube su Presupuesto»* |
| cadencia uniforme de 12 meses | fabricaba faltas en numerales trimestrales | lectura de la Guía: seis cadencias distintas |
| omitir períodos no publicados del promedio | `SITA 0,97` con dos conjuntos sin publicar nada | incredulidad ante el número |
| truncar nombres al descargar | 29 archivos se sobrescribieron entre sí | 917 archivos en disco para 936 descargados |
| «HTML ⇒ no es el documento» | «0 de 430 enlaces accesibles» — falso | el número era increíble |
| buscar el término del componente | 5 componentes «ausentes» que sí estaban con otro nombre | inspección de las cabeceras |
| tomar el nombre del campo por su contenido | la muestra OCR resultó ser fotografías, no actas | Javo abrió los archivos |

**Ninguno lo detectó el sistema.** Todos los encontró una persona leyendo salidas, y ese es el
hallazgo que originó ADR-051.

### 3 · Hallazgos sobre el sujeto observado

- **Numeral 6 · Presupuesto:** la obligación exige *«especificando **ingresos**, gastos,
  financiamiento y resultados operativos»*. Los 8 períodos publicados traen **cero filas de
  ingreso** (clasificador: sin códigos de los grupos 1 y 2). Publicación formal impecable —14
  campos de 14, formato abierto, en plazo— y dimensión ausente.
- **Art. 24 · actas:** la guía exige *«Enlace para ver y descargar **el acta**»*. Sobre 254
  documentos abiertos: 199 resoluciones administrativas, 52 certificados de resolución de sesión,
  **cero actas**. El propio documento delata la ausencia — entre sus resoluciones figura «Aprobar
  el Acta de Sesión Ordinaria Nro. 099».
- **Numeral 10 · Planes y programas:** cero archivos en todo 2025.
- **Numeral 14:** tabla desalineada; la columna «Apellidos y Nombres» contiene el cargo. **No hay
  un solo nombre de responsable publicado.**
- **Enlaces:** 123 documentos llegan como imagen escaneada (no procesables) y 5 exigen sesión
  iniciada en la nube del GAD — el Reglamento art. 11 prohíbe requisitos que limiten el acceso.
- **Punto de inflexión:** 2025 oscila entre 11 y 17 numerales por mes; enero de 2026 salta a 25/25
  y se mantiene. Cambio de régimen, no mejora gradual.
- **Numeral 17 · audiencias y reuniones (hallazgo del 18-ago, al abrir los ZIP):** la guía exige
  *«Enlace para descargar el **registro de asistencia** de las personas que participaron»*. Los 13
  archivos comprimidos contienen **260 archivos: 120 `.jpg`, 100 `.jpeg`, 39 `.png` y 1 `.mp4`**.
  **Ni un solo PDF, XLS o DOC.** Son fotografías de eventos, organizadas en carpetas por fecha
  («Anexos Reuniones/2025/ABRIL/1 DE ABRIL»), y algunas conservan nombres de archivo de redes
  sociales. Un registro de asistencia es una lista con nombres y firmas; esto es otra cosa.

  **Consecuencia para el OCR:** ninguna. Aunque un motor leyera perfectamente cada imagen,
  seguirían siendo fotos de un evento. El problema no es que no se puedan leer — es que **no son
  el documento que la norma exige**. Es el mismo hallazgo del art. 24 en otro numeral.

### 4 · Naturaleza observacional · lo que el canon ya sabía

El ACK `lotaip_f02.yaml`, de mayo, lo tenía modelado y nadie lo había leído:

> *«LOTAIP no crea obligaciones sustantivas. Crea **ventanas observacionales** sobre obligaciones
> que ya existen en CE/COOTAD.»*

`19_6 → financiera (d02)` · `19_8 → contratación (d01)` · `19_10 → planificación (d01)` ·
`19_12 → accountability (d09)`. **Que el GAD no publique el POA no es sólo una falta de d07: es
d01 quedándose ciego.** Eso explica la insistencia de Javo en que este dominio abastece al resto.

### 5 · Incidencia de corpus, subsanada

Al construir la cadena se halló que el chunk `beb5bb18162f` llevaba `articulo_num=19` de LOTAIP
siendo un considerando que cita el Pacto Internacional. Fundar la cadena ahí habría repetido el
error de ADR-040. Se corrigieron **8 chunks** de preámbulo (LOTAIP y RLOTAIP) a `articulo_num:
null`, con respaldo y reversión, tras comprobar que ninguna CNO citaba esos SHA. **No** se tocaron
`COOTAD 443` ni `RCOA-AMB 77`: contienen su propio encabezado y estaban bien.

## Cambios en el canon

| Artefacto | Qué aporta |
|---|---|
| `CNO-VII-001` | transparencia activa · art. 19 · 12 eslabones |
| `CNO-VII-002` | obligación específica de GAD · art. 24 · 12 eslabones |
| `CNO-VII-003` | transparencia pasiva · capítulo VI · 16 eslabones |
| `CNO-VII-004` | difusión y capacitación · Reglamento art. 10 · 6 eslabones |
| `RO-VII-001` | SITA: periodicidad por conjunto, plazo, formatos, ausencia, muestreo |
| `RO-VII-002` | cobertura material: dimensiones, clasificador, tres estados |
| `RO-VII-003` | universo documental: clases de acto, tipos de sesión, serie correlativa |
| `RO-VII-004` | solicitudes: plazo 10+5, silencio = denegación, gratuidad |
| `RO-VII-005` | difusión: tres veces al año · hoy `no_observable` |
| `catalogo_cd_d07_v1.1.0` | el catálogo enriquecido con la vara |
| `ADR-051` | autonomía de producción y evolución de plataforma |
| `ROModel 2.1` | el adaptador expone `parametros` — sin esto el DOM no podía consumir la RO |

**46 eslabones, 46 SHA verificados contra el corpus.** Todo en `propuesta`: sólo Javo promueve.

## Validación

```
CNO/RO               16 cadenas · 16 íntegras · 13 RO
pruebas d07          36/36 · ocho invariantes de autonomía
suite BRN            10 ✅ · check 3 ajeno (d08) · check 12 justificado por ADR-051
gate de salud        TODO OK
```

**La prueba que más pesa:** `SITA 2025 = 0,4646` antes y después de migrar cadencia, plazo,
formatos, fórmulas de ausencia, dimensiones, clasificador y clases de acto desde el código hacia
las Reglas Operativas. Cuatro migraciones sucesivas, el resultado no se movió una milésima.

> **Cambió la procedencia del criterio, no el resultado.** Es la diferencia entre «tocamos el
> código hasta que salió un número que nos gustó» y «sacamos el criterio del código, lo
> declaramos en el canon y comprobamos que el mismo criterio produce lo mismo».

## Estado · EN CURACIÓN

**Lo que sí está cerrado.** La capa normativa: cadena completa y verificada (4 CNO · 46/46 SHA),
reglas operativas que gobiernan cada criterio (5 RO), agente que las consume por una única puerta
(`reglas.py`), orquestador con gates que detienen, 936 archivos de evidencia con SHA y 36 pruebas
de regresión.

`SITA 2025 · 0,4646` — 2 conjuntos sin publicar nada, 14 incumpliendo periodicidad.
`SITA 2026 (ene-may) · 0,8382` — 1 sin publicar; **pero 4 numerales sólo declaran ausencia**.

**Lo que NO está cerrado, y por eso el expediente sigue abierto.**

### Universo físico · inventario del 2026-08-18 (417/417 · cero fallos de red)

Las magnitudes **no se suman entre sí**. Un contenedor no es «un documento más sus 35
documentos»: es una capa distinta, y confundirlas fue lo que produjo la cifra falsa de «417
documentos».

```
417   enlaces publicados accesibles      ← inspeccionados 417/417
        391  archivos individuales
         26  contenedores  →  935 artefactos dentro
──────────────────────────────────────────────────────────
1.326  objetos físicos observados          balance cuadra
```

| Naturaleza material (por firma del archivo, no por su extensión) | |
|---|---|
| documento PDF | 267 |
| imagen | 123 |
| contenedor | 26 |
| sin identificar | 1 |

**Dentro de los contenedores:** 671 PDF · 122 jpg · 101 jpeg · 39 png · 1 xls · 1 mp4.

> ### ⚠️ ATRIBUCIÓN · esto NO es todavía una observación de QUIRA
>
> Javo (2026-08-18), corrigiendo la redacción de este expediente:
>
> > *«Si Claude lo dice, por ser Claude. Pero Claude no es QUIRA. Claude puede hacer eso, QUIRA
> > creo que no. Nunca olvidar que estamos construyendo las capacidades de QUIRA; no es un
> > trabajo que toda la vida la hará Claude, eso no es real. Estamos construyendo un ecosistema
> > que deberá reportar más adelante 222 municipios, sin Claude, solo QUIRA.»*
>
> Tenía razón y el reparo es de arquitectura, no de estilo. La formulación correcta es:
>
> **Durante el desarrollo, un proceso auxiliar ejecutado fuera del pipeline inspeccionó 671 PDF
> y obtuvo texto extraíble en los 671.** Es evidencia de validación del método — **no una
> capacidad atribuible a QUIRA**, porque hoy ningún componente del sistema puede reproducirla.
>
> La auditoría lo confirma: de 31 scripts en `scripts/normativa/`, **sólo uno es invocable desde
> la aplicación**. Los treinta restantes —incluidas captura, descarga, verificación de enlaces,
> análisis de contenido e inventario— sólo existen si alguien los ejecuta a mano.
>
>     hoy:  Claude corre scripts → deja JSON en data/ → el orquestador los lee
>     sin Claude: el orquestador no tiene qué leer
>
> Y el propio gate `EVIDENCIA` del orquestador lo decía sin que nadie lo notara: *«no hay índice
> de descargas — **ejecute la captura primero**»*. El hueco estaba documentado y se dejó abierto
> el mismo día que se firmaba ADR-051, titulado «QUIRA ejecuta sin Claude».

### Publicación ≠ artefacto físico

Se conservan los dos niveles, porque responden a preguntas distintas y ninguna sustituye a la
otra *(criterio del colega, 2026-08-18)*:

| nivel | qué cuenta |
|---|---|
| **publicación** | cada aparición del documento en el portal (enlace × período) |
| **artefacto** | el objeto físico único, identificado por su SHA-256 |

Sin esa distinción se dijo *«15 escaneos del numeral 15»* cuando es **un único archivo, mismo
SHA, publicado quince meses seguidos**. Se contaron referencias y se llamaron documentos. **11
documentos idénticos aparecen bajo más de un enlace** en el universo.

Deduplicar y quedarse sólo con el artefacto perdería la historia de publicación; contar
publicaciones y llamarlas documentos infla el universo. Con ambos niveles se puede afirmar a la
vez «se publicó 15 veces» y «es un solo archivo».

### El corpus real de OCR

```
10  PDF escaneados únicos     9 del numeral 18 · 1 del numeral 15
```

No 24 ni 123. Las **123 imágenes del numeral 17 no entran**: su problema es de universo
documental —son fotografías donde la norma exige un registro de asistencia— y ningún OCR lo
resolvería.

### Frontera de observación declarada

`Ordenanzas.zip` (numeral 1.2) **supera los 500 MB** y no se ha capturado íntegro. El servidor no
declara `Content-Length` —Nextcloud lo genera al vuelo—. Queda registrado como
`cortado_por_tope_de_tamano`: **captura incompleta del observador, jamás ausencia del sujeto
obligado**.

### Tres reglas que este expediente incorpora al proyecto

**1 · Sobre la evidencia observada** *(colega, 2026-08-18)*

> **La existencia de un enlace no acredita la existencia ni la naturaleza del documento exigido.
> La evidencia debe ser inspeccionada materialmente antes de ser considerada evidencia del
> cumplimiento.**

Ocurrió tres veces en el mismo dominio: el campo decía «acta» y había un certificado de
resoluciones; decía «registro de asistencia» y había fotografías de un evento; el banco de pruebas
tomó una muestra OCR basándose en el nombre del numeral y resultó no ser un problema de OCR.
**QUIRA observa el documento, no le cree al nombre del campo.**

**2 · Sobre el perímetro del observador** *(colega, 2026-08-18)*

> **Un instrumento de observación no puede interpretar como ausencia aquello que quedó fuera de
> su perímetro efectivo de captura.**

**3 · Sobre los límites operativos**

> **Todo límite operativo que pueda reducir el universo observado debe producir un estado
> explícito de captura incompleta; nunca una ausencia silenciosa.**

Las dos últimas nacen de un hecho incómodo: **el inventario auditó al observador antes que al
observado.** Primero un filtro sensible a mayúsculas ocultó 121 enlaces. Después los topes del
propio inventario —`--max-filesize 80 MB`, `--max-time 60 s`— devolvieron **94 artefactos internos
donde había 935**. Ninguna de las dos cifras era falsa en sentido técnico: ambas eran ciertas
respecto de un universo recortado por el instrumento.

> Sin estas reglas, QUIRA habría acusado al sujeto observado por una ausencia que produjo el
> observador. Es el mismo error de OBS-030, esta vez sin VPN de por medio.

Por eso el inventario ahora emite **estados de captura tipados** —`cortado_por_tope_de_tamano`,
`cortado_por_tiempo`, `respuesta_no_200`— y un **balance de conservación** que debe cuadrar. Y por
eso las magnitudes no se suman entre sí:

    enlaces publicados  ≠  contenedores  ≠  artefactos internos  ≠  archivos individuales

Decir «417 documentos» distorsionaba: 26 de esos enlaces son contenedores con **935 artefactos
dentro**, de los cuales **672 llevan texto** (671 PDF y 1 XLS) que nadie había abierto.

### La capacidad pasó del repositorio al sistema · 2026-08-19

Javo cerró la discusión con una frase que obliga a revisar todo lo anterior:

> *«Claude no es QUIRA. Estamos construyendo un ecosistema que deberá reportar más adelante
> 222 municipios, sin Claude, solo QUIRA.»*

La auditoría le dio la razón: de **31 programas** en `scripts/normativa/`, **uno solo** era
invocable desde la aplicación. Todo lo demás existía en el repositorio y no en el sistema. El
gate `EVIDENCIA` lo confesaba en su propio texto —*«ejecute la captura primero»*— el mismo día
en que se firmaba el ADR-051, titulado «QUIRA ejecuta sin Claude».

Lo que cambió:

| Antes | Ahora |
|---|---|
| el orquestador **pedía** que alguien corriera la captura | `etapas.py`: el agente **la ejecuta** |
| la evidencia se daba por buena si el archivo existía | caduca por calendario (fuente) o por **cambio de contenido** del insumo |
| «existe en disco» = «está al día» | el sello registra **con qué insumos** se produjo cada salida (SHA) |
| 31 programas sin clasificar | los 32 declarados: etapa · canon · biblioteca · corpus · otro dominio · superado |
| la revisión documental sólo la lanzaba una persona | `analizar_documentos()` con su control en la consola |

Y la distinción que el canon necesitaba fijar, porque automatizarlo todo habría sido la respuesta
fácil y equivocada:

> **Construcción del canon ≠ capacidad operativa.** La primera corre una vez, bajo criterio
> humano, y su producto se sella con SHA — un sistema que reejecuta la extracción de su propia
> vara puede cambiarse el patrón con el que mide. La segunda corre cada mes, en 222 municipios,
> sin nadie mirando. Una prueba verifica que **ningún programa quede sin clasificar**.

### El instrumento se delató a sí mismo · Numeral 10

La primera revisión documental lanzada **desde el agente** produjo un archivo que decía
`completo: true` con **7 de 15 documentos jamás intentados**: la fuente dejó de responder, el
guardarraíl cortó, y el resultado era indistinguible de un análisis entero. «Completo» tiene dos
enemigos —el tope que pide quien invoca y el corte automático por fuente caída— y sólo se miraba
el primero. Es la cuarta vez que este dominio produce una cifra parcial con apariencia de total:
«390 artefactos» era una resta, «24 escaneos» eran referencias, «94 documentos» era un tope de
tamaño. Corregido y fijado en prueba.

Sobre el sujeto observado, y con OBS-030 aplicado antes de afirmar nada: de los **8 enlaces
intentados** del Numeral 10 (2026, enero a mayo), los 8 devolvieron **404** en
`cloud.montecristi.gob.ec`. Se falsó el instrumento primero: el script sí resuelve el visor de
Nextcloud a `/download`, y dos enlaces se comprobaron por vía independiente con el mismo
resultado. El servidor del GAD responde —devuelve 25.886 bytes de HTML—; **lo que no existe es
el recurso compartido**. Los 7 restantes quedan **sin verificar**, no «inaccesibles».

### Qué ES el universo documental · corrección de Javo, 2026-08-20

El director propuso analizar los 636 artefactos «por numeral o por artefacto», y ofreció declarar
como dato que **los artefactos sin obligación asociada revelarían que el GAD publica lo que la
norma no le pide**. Javo lo corrigió de raíz:

> *«Si todo lo que sube el GAD obedece específicamente a lo que exige la LOTAIP, su reglamento y
> los documentos metodológicos que tenemos en el corpus, no se puede separar los artefactos de los
> numerales: están transversalizados por la normativa legal vigente y sus procedimientos técnicos,
> que también son ley. Los GAD responden en ese portal única y exclusivamente al cumplimiento de
> esta normativa, y con ello al derecho constitucional a la información pública.»*
>
> **«El universo de información de transparencia activa del GAD no debe interpretarse como una
> colección arbitraria de archivos, sino como una materialización documental de obligaciones
> normativas y procedimentales.»**

Tenía razón, y el error era doble. El primero, de método: «por numeral» y «por artefacto» son
técnicas de recorrido, no la estructura del fenómeno. El segundo, más grave y del tipo que este
dominio existe para impedir: **presumir en vez de determinar**. Un artefacto que no se asocia a
una obligación puede significar cuatro cosas distintas —que no hallamos la relación normativa, que
existe una obligación transversal, que es materialización complementaria, o que efectivamente no
es exigido— y sólo la cuarta es «el GAD publica lo que nadie le pide». Presentarla como la única
lectura habría sido inventar un hallazgo.

**La unidad analítica** (formulación del colega, adoptada):

> El universo documental de transparencia activa de un GAD no constituye una colección arbitraria
> de archivos, sino la materialización documental de obligaciones jurídicas, normativas y
> procedimentales que concretan el deber de transparencia activa y el derecho de acceso a la
> información pública. **La unidad analítica no es el archivo aislado ni el numeral aislado, sino
> la relación verificable entre obligación, objeto de información, materialización documental,
> evidencia y afirmación sobre el sujeto.**

    ordenamiento normativo → obligación → objeto exigible → materialización
        → publicación → accesibilidad → actualidad → evidencia → verificación
        → afirmación sobre el sujeto

Y su consecuencia inmediata, que impide repetir con los documentos el error que se acaba de
corregir con los enlaces:

> **La ausencia de un artefacto no constituye por sí misma incumplimiento: constituye ausencia de
> evidencia respecto de una obligación cuya materialización esperada debe haber sido previamente
> determinada por el corpus normativo y procedimental aplicable.**

Lo que QUIRA no decide es **qué información debería existir** — eso lo fija el ordenamiento. QUIRA
determina, a partir del corpus, qué debía materializarse, cómo debía publicarse, y qué puede
afirmarse sobre lo que efectivamente encuentra.

### Auditoría del scoring contra el Instructivo · 2026-08-20

Javo ordenó la verificación que faltaba:

> *«Sincerar todo en base a la norma y las metodologías para no inventarnos nada. Este DOM debe
> quedar impoluto e inexpugnable como base para los demás.»*

Se confrontó `scoring.py` contra el **Instructivo para evaluar el nivel de cumplimiento de los
parámetros técnicos de la transparencia activa** (DPE 2024), parámetro por parámetro.

| | Instructivo | Motor | |
|---|---|---|---|
| **SITA** | `(CTA+ETA+RP+CI)/4`, «promedio de los valores promedio de cada parámetro» (§Subíndice, párr. 268) | idéntico | ✅ |
| **CTA** | 1,0 completa y actualizada · **0,5 incompleta O desactualizada** · 0,0 sin información (Tabla 1) | idéntico | ✅ |
| **ETA** | 1 tres estrellas · 0 sin información (Tabla 2) | idéntico | ✅ |
| **RP** | 1 dentro del plazo · 0 fuera (Tabla 3) | idéntico | ✅ |
| **CI** | tres parámetros **asignados numeral por numeral** (Anexo 1) | los exigía **todos a todos** | ⛔ |

**El defecto.** El Anexo 1 del Instructivo trae una matriz de calificación que declara, para cada
numeral, qué parámetros cualitativos se evalúan:

    estado_de_verificables      20 de 24 numerales — NO al 2, 3, 4 ni 6
    vigencia_de_la_informacion  sólo a los numerales 16 y 18
    validez_de_la_informacion   sólo a los numerales 3 y 6

El motor exigía los tres a los 24. Un conjunto al que la norma no le pide vigencia perdía calidad
por no tenerla: **un castigo inventado por el instrumento**, exactamente lo que este dominio
existe para no hacer.

**Impacto medido.** Sobre la evidencia de 2025 el SITA no se movió —los `CI = 0` de Montecristi
vienen de verificables caídos, que sí le aplican—, pero la corrección impide el castigo injusto en
cualquier corrida futura y en los otros 221 GAD. La matriz se extrajo a `matriz_calificacion.json`
con el SHA del Instructivo, y los parámetros llegan al motor **desde la RO**, nunca desde el
código (Regla de Oro 9).

**Y una confirmación independiente.** El Anexo 1 lista los **numerales 5 y 22 como filas
separadas**, con sus propias descripciones. La misma Defensoría los evalúa por separado — lo que
respalda por otra vía la corrección que Javo hizo ese mismo día sobre la vara.

### Pendientes — adquisición de dato, no cómputo pendiente

- **Inventario documental completo:** falta abrir el universo restante y descomprimir los 27 ZIP.
  Es la condición para volver a cerrar el dominio.
- **OCR:** afecta a **10 artefactos físicos únicos**. La cifra de «24 documentos» contaba
  apariciones: el contrato colectivo del numeral 15 es **un solo archivo, mismo SHA, publicado
  quince meses seguidos**. **No** resuelve el numeral 17, cuyo problema es de
  universo documental y no de legibilidad. La cadena de derechos está verificada por artefacto
  (`CANTERA.md`); la muestra del banco debe rehacerse desde los escaneos reales.
- **Difusión y capacitación:** `RO-VII-005` nace `no_observable` — ningún numeral del art. 19
  recoge la actividad. Requiere otra fuente, no otro cálculo.
- **Transparencia pasiva:** `RO-VII-004` sólo se activa cuando alguien presenta una solicitud. Sin
  ellas no hay incumplimiento: hay ausencia de ejercicio del derecho.
- **Doble publicación:** el Reglamento art. 11 exige que la información sea *«visible desde el
  portal principal del sitio web institucional»*. Sólo se observó la DPE.
- **Promoción a `vigente`:** las nueve piezas están en `propuesta`. Es decisión de Javo
  (ADR-035 §5), no del director — y no procede mientras el expediente siga en curación.

---
*PCD-D07 · Dylus Lab © 2026 · el expediente donde el dominio aprendió que no debía interpretar Derecho.*
