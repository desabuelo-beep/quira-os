---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 4]
  type: OPERATIVA
---

# TEORÍA DE LA EVIDENCIA PÚBLICA VERIFICABLE

**Doctrina rectora del DOM Transparencia (d07) · 2026-07-27 · deriva de OBS-018**

> **NO es una capa nueva** (Subsidiariedad · Carta Art. 1.2). Es la **elevación** del documento
> `ESCALERA_DE_FUENTES.md` — no un documento paralelo — y se apoya en artefactos que **ya
> existen**: el IOC del Gold Master (`H41_IOC_OPACIDAD_CRITICA`) y la clasificación documental del
> catálogo d08.

> **Por qué existe:** para que dentro de seis meses nadie diga *"hay que mejorar el OCR"*. **El
> problema nunca fue el OCR.**

---

## 1 · Qué es una evidencia pública — y cuál es el objeto real de auditoría

**QUIRA no audita documentos. Audita la capacidad institucional del Estado para producir evidencia
pública verificable y reutilizable.**

| Un sistema tradicional ve | QUIRA ve |
|---|---|
| PDF escaneado → *"fallo del OCR"* | PDF escaneado → **baja calidad de la evidencia pública** |

El DOM Transparencia (d07) **cambia de naturaleza**: no responde *"¿pude leer el documento?"* sino
**"¿el Estado publicó evidencia susceptible de verificación automática?"**. Eso no es un problema
de algoritmo: es un problema de **calidad institucional del dato** que el GAD entrega al ciudadano.

## 2 · Qué significa que sea verificable

Una evidencia es verificable cuando permite **reconstruir el dato sin intervención humana**:
estructura legible por máquina, origen trazable, contenido reutilizable. La Guía Metodológica
Integral de la **LOTAIP 2024 exige datos abiertos y reutilizables** — ese es el estándar contra
el que se contrasta.

## 3 · Qué es la opacidad técnica — el silencio inducido

> **El PDF ilegible no es ausencia: es un silencio INDUCIDO.** La institución habla, pero en un
> formato que impide reconstruir el dato. Es otra forma de silencio administrativo.

Conecta directamente con el concepto propio **"el silencio como dato"** (Marco Teórico): así como
la ausencia documental se tipifica en vez de ocultarse, **la ilegibilidad se mide en vez de
"arreglarse"**.

### La perversión que esto elimina
```
AUDITORÍA TRADICIONAL          QUIRA
documento ilegible             documento ilegible
   ↓                              ↓
el auditor limpia el dato      NO se limpia
   ↓                              ↓
el problema desaparece         se convierte en evidencia → el IOC aumenta
```

## 4 · La frontera jurídica — lo que QUIRA certifica y lo que no

> ⚠️ **Advertencia de la asesoría, adoptada:** NO se afirma automáticamente que *PDF ilegible =
> incumplimiento LOTAIP*. Jurídicamente pueden existir excepciones.

| ❌ QUIRA **no** dice | ✅ QUIRA certifica |
|---|---|
| *"el GAD viola la LOTAIP 2024"* | *"la evidencia publicada **no cumple condiciones de reutilización automática**"* |

Lo primero lo determina la Defensoría del Pueblo o la Contraloría. Lo segundo es **observable**.
Mantiene intacto el Horizonte de Verdad (Marco Teórico) y el Principio de No-Inferencia.

---

## 5 · El problema estratégico

QUIRA debe escalar a **222 GAD de Ecuador** y potencialmente **+6.000 gobiernos locales de LAC**.
Toda su evidencia llega en PDF, Word y Excel — mayoritariamente PDF, con calidad heterogénea.
Si cada dominio depende de resolver extracción caso por caso, el proyecto se consume en ingeniería
de documentos y nunca llega a producir inteligencia pública.

## La decisión: no competir en extracción

**QUIRA no compite en OCR.** Los modelos de extracción son *commodity* y están dominados por
actores con recursos incomparables. Invertir ahí es perder por definición.

**QUIRA compite en algo que nadie mide:** *¿qué proporción de la evidencia pública de un GAD es
verificable automáticamente?* Esa pregunta:
- se responde **sin costo adicional** (se sabe al intentar extraer);
- es **comparable entre los 222 GAD** con la misma regla;
- es un **indicador real de madurez digital y de opacidad técnica**;
- **nadie más la está midiendo**.

> **La falencia se convierte en el dato.** Si un GAD publica únicamente PDF escaneado sin capa de
> texto, eso no es un problema técnico de QUIRA: es **opacidad técnica del GAD**, y es medible.
> Es el concepto *"el silencio como dato"* (Marco Teórico) aplicado al formato del documento.

## Los patrones reales de opacidad técnica *(aporte de Javo · 15 años en GAD)*

La ingesta **no es un problema técnico secundario: es el cuello de botella estructural nº 1 de la
gobernanza pública en Ecuador**, y el obstáculo real del DOM Transparencia al escalar a 222 GAD.

La **Guía Metodológica Integral de la LOTAIP 2024 exige datos abiertos y reutilizables**. Frente a
eso, la práctica municipal produce patrones identificables:

| Patrón | En qué consiste | Por qué importa |
|---|---|---|
| **Excel Cáscara** | el GAD sube la matriz Excel que exige el Numeral 10 (Planes y Programas), pero dentro **solo hay un enlace** a un PDF en Drive o en su servidor | cumple la forma, no el fondo |
| **PDF Trampa** | el enlace lleva a un documento **impreso y escaneado a 150 DPI** | ilegible para máquina — no es dato abierto |
| **Silos de información** | CPCCS en PDF propio · SERCOP en PDF · portal del GAD con **accesos rotos** — cada sistema encerrado en sí mismo | fragmentación intersistémica (Postulado II) |

### El tercer patrón — opacidad de ESTRUCTURA, no de formato *(Javo · 2026-07-29 · OBS-020)*

Los dos patrones anteriores son de **formato**: el documento no se puede leer. Existe un
tercero, de naturaleza distinta y **más grave porque el documento sí se lee**:

| Patrón | Naturaleza | En qué consiste |
|---|---|---|
| **Ficha POA Agregada** | **estructura del contenido** | el POA es un XLSX limpio, nivel A del ICEP — y aun así **no permite verificar nada**: mezcla `partida · programa · actividad · unidad` en una fila y **omite el territorio** |

Medido en Montecristi (`scripts/d08/diagnostico_ficha_poa.py`, 1.027 filas, dos métodos
independientes que convergen): **~1% de las filas declara dónde se ejecuta el gasto**;
70% no declara componentes operativos.

> **Lo demostrado, sin atribuir intención:** la ficha observada **no contiene la información
> suficiente para reconstruir territorialmente la ejecución mediante evidencia documental
> verificable**. Por qué fue diseñada así es una pregunta distinta — exigiría contrastar el
> diseño normativo del instrumento con su implementación, y hoy no hay evidencia para eso.

**Consecuencia para la escalera de fuentes:** un documento puede estar en el **peldaño 1
(óptimo)** y ser igualmente inauditable. La calidad del *formato* no garantiza la
**habilitación del contenido** — son dos dimensiones distintas del ICEP, y ninguna mejora
de ingesta, OCR o modelo resuelve la segunda.

> **Precisión terminológica (Javo · 2026-07-27):** se dice **silos de información**, no
> "archipiélago de formatos". El archipiélago describe la *forma*; el silo describe la
> **conducta institucional**: cada sistema opera encerrado, sin obligación de dialogar. Es la
> causa, no el síntoma.

### "Excel Cáscara" — no es un formato, es una estrategia institucional

El concepto acuñado por Javo describe un **patrón de simulación**, no un descuido técnico:

```
Legalmente:   ✔ Excel publicado (cumple el Numeral 10)
Materialmente: Excel → link → PDF → imagen → ilegible
```

**Formalmente cumplen. Materialmente no.** Cumplen en apariencia pero **bloquean la fiscalización
automática**. Por eso merece un tratamiento propio en el IOC: no es lo mismo no publicar que
publicar una cáscara.

> **Consecuencia normativa:** si la LOTAIP 2024 exige datos **abiertos y reutilizables**, publicar
> un PDF ilegible **no es cumplir: es simular cumplimiento**. Eso convierte la opacidad técnica en
> un **hallazgo normativo verificable**, no en una queja de ingeniería.

**Dónde se audita:** el **DOM Transparencia (d07)** tiene ese trabajo — recorre el portal, sigue
los enlaces y registra el estado. d08 y los demás dominios *consumen* la evidencia; d07 *califica
cómo fue publicada*.

## La escalera de ingesta — buscar siempre el peldaño más alto disponible

| Nivel | Fuente encontrada | Acción del motor | Impacto en el ecosistema |
|---|---|---|---|
| **1 · Óptimo** | `.xlsx` / `.csv` nativo | extracción automática, ingesta directa al canon | **verificabilidad alta (100%)** |
| **2 · Aceptable** | `.pdf` con capa de texto | extracción determinística de texto | verificabilidad directa |
| **3 · Fricción** | `.pdf` escaneado (imagen) | OCR local ligero (Tesseract, gratis) **+ alerta de fricción** | **evidencia con fricción** — se declara |
| **4 · Opacidad** | enlace roto · archivo corrupto · escaneo ilegible | registra **ausencia de habilitación documental** | **castiga el IOC** (`H41`) |

El sistema **NUNCA falla ni se detiene**: marca `ESTADO_EXTRACCION: OPACIDAD_TECNICA_DOCUMENTAL`
y continúa. El fallo es el dato.

### Regla operativa (nace de OBS-018 · **acotada por R-F el 2026-07-29**)
> **Antes de recurrir a OCR o a un corpus derivado, verificar si existe la fuente en un peldaño
> superior.** El GAD casi siempre tiene el XLSX aunque publique el PDF.

> ⚠️ **RÉGIMEN DE SOLICITUD (R-F).** Solicitar es legítimo — **lo que decide es el estado de
> conocimiento del universo documental del GAD**, no el acto de pedir:
>
> | Universo | Situación | ¿Solicitar? |
> |---|---|---|
> | **conocido** | el documento existe, mal publicado | ✅ sí — recupera preexistente |
> | **conocido** | el dato **no existe** *(Montecristi: el PP no fija costo por prioridad)* | ⛔ no — lo **induciría** |
> | **no conocido** | GAD sin documento hallable en web ni transparencia | ✅ **sí, obligatorio** — la solicitud **determina** cuál de los dos casos es |
>
> **Canal:** siempre vía **Observatorio QUIRA / QUIRA Ciudadana**, por derecho de acceso a la
> información pública — nunca QUIRA pidiéndole insumos al auditado. Detalle en
> `PROTOCOLO_CURACION_DOMINIO.md` **R-F**.

En el cruce de d08 se usó un corpus vectorizado (nivel 4, corrupto) cuando el XLSX oficial
(nivel 1, limpio) estaba disponible. El canon ya advertía la corrupción y no se consultó. Esa es
exactamente la pérdida de tiempo que esta escalera evita.

### Regla de honestidad
El fallo de extracción **nunca se oculta ni se rellena con inferencias**: se registra con su nivel
y alimenta el indicador de opacidad. Un documento que no se pudo procesar es evidencia sobre el
GAD, no un hueco en QUIRA (Horizonte de Verdad · Principio de No-Inferencia).

## 6 · ICEP — Índice de Calidad de Evidencia Pública

> **NO es una capa nueva: es una DIMENSIÓN del IOC** (asesoría · Subsidiariedad). Permite comparar
> **municipios completos**, no documentos sueltos — que es lo que hace falta para 222 GAD.

| Nivel | Calidad de la evidencia | Estado del dato en QUIRA | Impacto en el IOC |
|---|---|---|---|
| **A** | datos abiertos · `.xlsx` / `.csv` nativos | excelente · verificable | **0% opacidad** |
| **B** | `.pdf` con capa de texto | buena · extraíble | baja fricción |
| **C** | `.pdf` escaneado (requiere OCR) | evidencia con fricción | fricción técnica |
| **D** | imagen ilegible · `.jpg` · escaneo pobre | **opacidad técnica** | penalización |
| **E** | enlace roto · archivo inexistente | **ausencia documental** | castigo crítico |

**Pendiente de decisión de Javo (Regla 1):** la fórmula que integra el ICEP al IOC **se sella en
el Gold Master**, no en QUIRA. Aquí solo se produce el dato de nivel por documento.

## 6-bis · CVI — Capacidad Verificativa del Instrumento

> **NO es una capa nueva** (Subsidiariedad · Carta Art. 1.2): es la **segunda dimensión del
> IOC**, hermana del ICEP. Vive aquí, junto a él, porque miden la misma cosa por dos caras.

El ICEP responde *"¿pude leer el documento?"*. **OBS-020 demostró que eso no basta**: el POA
de Montecristi es XLSX nativo —**nivel A, la mejor calificación posible del ICEP**— y aun
así no permite verificar dónde se ejecutó el gasto. Un instrumento puede ser perfectamente
legible y **completamente inauditable**.

| | Pregunta | Naturaleza de la opacidad |
|---|---|---|
| **ICEP** | ¿el documento se puede **leer**? | de **formato** |
| **CVI** | lo que se lee, ¿permite **demostrar** algo? | de **estructura de contenido** |

> **El CVI no mide cumplimiento ni ejecución. Mide cuánto permite demostrar un instrumento.**

**Definición formal de la arquitectura** *(precisión de la asesoría · 2026-07-29):*

> **ICEP** evalúa la **legibilidad documental**.
> **CVI** evalúa la **verificabilidad estructural**.
> **IOC** integra ambas dimensiones: `IOC = f(ICEP, CVI)`.

Las tres categorías no se solapan y ninguna es una SAT: **ICEP → formato · CVI → estructura ·
IOC → opacidad · SAT → alertas.** Mantener esa separación es lo que impide inflar el marco.

### Por qué es un meta-indicador y no una métrica de dominio

Se aplica con la **misma regla** a todo instrumento documental del Estado, y cada dominio lo
instrumenta para el suyo (§0 de OBS-020: *quien es dueño del instrumento lo califica*):

| Instrumento | Dominio | Qué mide el CVI |
|---|---|---|
| **POA** | d01 Planificación | % de fichas con territorio y componentes declarados |
| **PAC** | d03 Contratación | % de contrataciones vinculables a un proyecto del POA |
| **Presupuesto** | d02 Presupuesto | % de cédulas con desglose de inversión territorial |
| **Rendición de Cuentas** | d09 | % de afirmaciones respaldadas por código de contratación o cédula |
| **Portal / LOTAIP** | d07 Transparencia | *(lo cubre el ICEP — es la cara de formato)* |

**Primera medición registrada:** POA Montecristi 2023-2026 → **territorio 1,1%** ·
**componentes 29,8%** (`scripts/d08/diagnostico_ficha_poa.py`, dos métodos convergentes).

### Frontera — lo que el CVI NO dice

| ❌ No afirma | ✅ Certifica |
|---|---|
| *"el GAD planifica mal"* · *"el instrumento fue diseñado para no ser auditado"* | *"el instrumento **no habilita** la verificación documental de X"* |

Atribuir intención de diseño exigiría contrastar el diseño normativo del instrumento con su
implementación, o comparar varios municipios. **Hoy es hipótesis, no hallazgo.**

**Pendiente de decisión de Javo (Regla 1):** cómo el CVI se integra al IOC **se sella en el
Gold Master**, no en QUIRA. Aquí solo se produce el dato por instrumento.

> **Por qué esto puede pesar más que el propio MRSPP:** el MRSPP mejora cómo QUIRA clasifica
> una correspondencia. El CVI abre una pregunta que **nadie está haciendo en Ecuador**:
> *¿cuánto permiten demostrar los instrumentos con que el Estado planifica?* Y si el patrón
> se repite en un segundo GAD, deja de ser un hallazgo sobre Montecristi para convertirse en
> evidencia sobre **el diseño nacional del instrumento** (Gate 7).

## 7 · Por qué esto sirve a la familia QUIRA

Javo lo planteó: la información rescatada no es un fin en sí misma — debe permitir **modelar el
desarrollo y la mejora de la calidad de vida** a partir de las intervenciones del GAD. El nivel de
evidencia condiciona qué producto puede construirse encima:

| Nivel de evidencia | Qué habilita |
|---|---|
| **A-B** (verificable) | análisis causal · modelado de intervenciones · **QUIRA Impact** |
| **C** (con fricción) | verificación con reserva · trazabilidad parcial |
| **D-E** (opaco) | solo **QUIRA Ciudadana**: exigir apertura — no se puede modelar sobre lo ilegible |

**Sin evidencia de nivel A-B no hay modelación posible.** Por eso elevar el ICEP de un territorio
es condición previa para el resto de la familia QUIRA, no un detalle técnico.

## Conexión con artefactos existentes *(no se crea nada nuevo)*

| Ya existe | Se usa para |
|---|---|
| `IOC` — Índice de Opacidad Cantonal (`H41_IOC_OPACIDAD_CRITICA`, Gold Master) | recibir la proporción de evidencia no procesable como componente de opacidad técnica |
| `clasificacion_documental` (catálogo d08) | vocabulario ya definido: `procesable · ocr_certificado · parcial · no_localizada` |
| `extract_poa_pdf.py` · `enrich_*_docx.py` | extractores por nivel, ya operativos |

**Pendiente de decisión de Javo (Regla 1):** si la proporción de evidencia no procesable debe
incorporarse como componente del IOC, esa fórmula **se sella en el Gold Master**, no en QUIRA.
Aquí solo se produce el dato.

## Por qué esto es ventaja competitiva y no un parche

Un competidor puede comprar mejor OCR. **No puede comprar la serie histórica de qué tan
verificable ha sido la información pública de 222 cantones a lo largo de los años** — eso es
patrimonio cognitivo acumulado (Constitución Art. 19 · *longitudinalidad*).

La extracción es un medio. **La medición de la extractibilidad es el activo.**

---
*Escalera de Fuentes · Dylus Lab © 2026 · deriva de OBS-018 · alimenta el IOC.*
