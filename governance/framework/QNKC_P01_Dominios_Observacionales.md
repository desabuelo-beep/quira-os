# QNKC-P01 — Principio de Dualidad Epistémica en Dominios Observacionales

**Estado:** Congelado — v1.1  
**Fecha:** 2026-06-01  
**Tipo:** Principio Arquitectónico del Framework QNKC  
**Autores:** Dylus Lab + colega arquitectónico externo  
**Clasif.:** Interno · QUIRA Operaciones

> *"No son dos documentos. Son dos lecturas del mismo documento."*

---

## Enunciado del Principio

En dominios cuyo Servicio Público (C3) consiste en la producción o publicación de información institucional verificable, las capas C4 (Proceso) y C5 (Evidencia) pueden originarse en el mismo artefacto documental.

**El artefacto físico es uno. La perspectiva epistémica es doble:**

| Perspectiva | Capa QNKC | Pregunta que responde |
|-------------|----------|-----------------------|
| El GAD ejecutó el proceso | C4 | ¿El municipio cumplió su obligación de publicar / informar / convocar? |
| Un tercero puede verificarlo | C5 | ¿Un ciudadano o ente de control puede confirmar ese cumplimiento de forma independiente? |

C5 no es redundante respecto de C4.  
C5 es C4 visto desde fuera del municipio.  
Sin C5, el cumplimiento es autodeclarado.  
Con C5, el cumplimiento es verificable.

La anomalía no es que el dominio *observa*. La anomalía es que **el mismo artefacto cumple simultáneamente función operativa y función probatoria** — dependiendo de quién lo lee.

---

## Familia de Dominios Observacionales

Un dominio es **observacional** cuando su C3 (Servicio Público) es la producción de información, no la entrega de un servicio físico o una transferencia de recursos.

| Dom | Nombre | Artefacto C4 | Artefacto C5 | Proceso antes del artefacto | Grado de dualidad |
|-----|--------|-------------|-------------|----------------------------|-------------------|
| Dom07 | Transparencia | Publicación LOTAIP | Publicación verificable por ciudadano | Mínimo — publicar es el servicio completo | **ALTO** |
| Dom09 | Rendición de Cuentas | Informe de rendición | Informe verificable / acto público documentado | Rico — preparar, validar, presentar, responder, documentar | **MEDIO** |
| Dom08 | Participación Ciudadana | Acta / memoria de participación | Acta verificable por tercero | Medio — convocatoria, deliberación, decisión, registro | **MEDIO** |

**Dom09 antes que Dom08 en la tabla:** el proceso de rendición de cuentas (preparar, validar, presentar públicamente, responder preguntas, documentar compromisos) es más complejo y rico que el proceso participativo antes del acta. El acta de rendición no agota el proceso; el acta de participación tampoco, pero en menor medida.

**El grado de dualidad determina el diseño de Layer 2:**

- **ALTO (Dom07):** la distancia entre C4 y C5 es mínima. Publicar el enlace es casi suficiente como C4. C5 requiere verificar que el enlace responde, que el contenido es del período vigente, que es comprensible. La pantalla tiene dos columnas claramente separadas.
- **MEDIO (Dom09, Dom08):** el proceso antes del artefacto es rico y C5 no lo captura todo. Layer 2 debe mostrar el proceso Y el artefacto, no solo el artefacto. El semáforo de C5 pesa menos que en Dom07.

---

## El Peso Relativo de C4 y C5 Varía por Grado

La dualidad no es binaria — es un gradiente. A mayor grado de dualidad:
- C4 y C5 pesan igual (Dom07: publicar es el proceso y la evidencia son la misma cosa)
- El artefacto casi agota el proceso

A menor grado:
- C4 pesa más que C5 (Dom09: el proceso de rendición tiene valor institucional propio más allá del informe)
- C5 es la huella verificable de un proceso que va más allá del artefacto

Esta variación debe reflejarse en los pesos del indicador C8 para cada dominio.

---

## Contraejemplos — Dominios No Observacionales

| Dom | Nombre | C4 | C5 | Por qué no hay dualidad |
|-----|--------|----|----|------------------------|
| Dom10 | Territorio & Cobertura | Contrato EP Agua / POA de inversión | SIGEF + medición INEC | Proceso y evidencia son artefactos distintos — el contrato no prueba la cobertura |
| Dom12 | Protección Social | Ejecución presupuestaria Patronato | SIGEF / informe CGE | El dinero ejecutado y su reporte son producidos por actores diferentes |

En los no observacionales: C4 es interno al GAD y C5 viene de un tercero externo que mide el resultado de forma independiente. El proceso y la prueba del proceso son objetos separados.

---

## Consecuencias de Diseño

### Para el QTMP YAML

En dominios observacionales, el bloque EVIDENCIAS debe declarar la dualidad explícitamente:

```yaml
EVIDENCIAS:
  - id: EVD_[DOM]_01_MCR
    tipo: documental_verificable
    nombre: "[Nombre del artefacto]"
    perspectiva_interna: "El GAD ejecutó: [descripción C4]"
    perspectiva_externa: "Un tercero puede verificar: [descripción C5]"
    artefacto_compartido: true
    nota_epistemica: "QNKC-P01"
```

### Para Layer 2

El diseño de la pantalla debe exponer ambas perspectivas sin confundirlas:

- **Columna de proceso (C4):** ¿El municipio lo hizo? — barra de cumplimiento formal
- **Columna de verificabilidad (C5):** ¿Se puede confirmar desde afuera? — semáforo de accesibilidad real

En Dom07: mostrar "21/21 artículos publicados" no es suficiente. Hay que mostrar si el enlace funciona, si el contenido es del período vigente, si es descargable y comprensible. Eso es C5.

### Para el indicador C8

En dominios observacionales, C8 es el producto de las dos perspectivas:

```
C8 = cumplimiento_formal_C4 × verificabilidad_efectiva_C5
```

**Por qué multiplicación y no suma o promedio:**  
Si cualquiera de las dos dimensiones es cero, C8 debe ser cero. El GAD que no publica tiene C8=0. El GAD que publica 21/21 artículos con enlaces rotos o PDFs ilegibles tiene verificabilidad≈0 y por tanto C8≈0. Ambas son fallas de transparencia de igual gravedad. La multiplicación captura esto; la suma o el promedio lo enmascaran.

**Ejemplo concreto:**

```
cumplimiento_formal  = 21/21 artículos publicados = 100%
verificabilidad      = 7/21 accesibles y actualizados = 35%

C8 = 100% × 35% = 35%
```

El sistema lee 35%, no 100%. El semáforo es ROJO, no VERDE.  
Ese es exactamente el comportamiento que QUIRA debe tener: **no premiar simulaciones de transparencia.**

**Pesos variables por dominio:**  
El peso relativo de `cumplimiento_formal` vs. `verificabilidad_efectiva` en C8 puede ajustarse por el grado de dualidad. En Dom07 (ALTO) ambos pesos son iguales. En Dom09 y Dom08 (MEDIO), `cumplimiento_formal` puede pesar más porque el proceso antes del artefacto tiene valor institucional propio.

**Descomposición de `verificabilidad_efectiva` en tres dimensiones (OBS-QNKC-01):**

`verificabilidad_efectiva` no es un valor binario. Se descompone en:

```
verificabilidad_efectiva = C5a × C5b × C5c
```

| Dimensión | Nombre | Pregunta |
|-----------|--------|---------|
| C5a | Existencia | ¿El documento existe y es accesible? |
| C5b | Actualidad | ¿El contenido es del período vigente y está completo? |
| C5c | Inteligibilidad | ¿Un ciudadano común puede entenderlo y usarlo? |

La multiplicación es la misma lógica que C8: un cero en cualquier dimensión colapsa la verificabilidad total. Un PDF publicado (C5a=1), actualizado (C5b=1) pero técnicamente incomprensible para el ciudadano (C5c≈0) tiene `verificabilidad_efectiva ≈ 0` y por tanto `C8 ≈ 0`. El sistema no puede premiar transparencia inaccesible.

Esta descomposición está registrada como OBS-QNKC-01 en `QNKC_PRINCIPIOS_INDEX.md`.

---

## QUIRA como Radar Externo

Este principio establece una distinción fundamental entre QUIRA y el sistema de autoreporte del propio GAD:

| Sistema | Qué verifica | Perspectiva |
|---------|-------------|-------------|
| Portal LOTAIP del GAD | El municipio dice que publicó | Interna — C4 autodeclarado |
| QUIRA Gov | Un tercero puede confirmar que lo que publicó es accesible, actual y comprensible | Externa — C5 verificado |

QUIRA no acepta el autoreporte como evidencia de cumplimiento. QUIRA verifica de forma independiente. Esa es la diferencia entre un sistema de gestión y un sistema de inteligencia institucional.

En términos de diseño: **QUIRA siempre opera desde la perspectiva C5**, aunque reciba como insumo datos de C4. El trabajo del Layer 2 en dominios observacionales es traducir los datos C4 del GAD a resultados C5 verificables externamente.

---

## Implicación para el Resultado C9

El grado de dualidad determina la longitud de la cadena hasta C9. A mayor proceso antes del artefacto, más pasos entre C5 y C9:

**Dom07 — cadena corta:**
```
publicación → verificabilidad → escrutinio ciudadano
```
C9 es casi directo desde C5. Si la información es verificable, el escrutinio puede ocurrir.

**Dom09 — cadena media:**
```
informe → revisión → observación → corrección
```
El informe presentado no implica rendición efectiva. C9 requiere trazar si el proceso generó correcciones reales, no solo el acto de presentar.

**Dom08 — cadena media:**
```
participación → decisión → cambio
```
El acta publicada no implica incidencia real. C9 requiere trazar si la participación modificó una decisión de inversión concreta. Sin esa trazabilidad, Dom08 mide ceremonias, no gobernanza.

**Consecuencia para Layer 2:** Dom07 puede calcular C9 desde los datos de publicación. Dom09 y Dom08 necesitan trazabilidad adicional que el artefacto por sí solo no provee — el diseño de sus Layer 2 debe incluir un mecanismo para registrar ese eslabón adicional.

**Consecuencia para C8 por dominio:**

La fórmula base `C8 = cumplimiento_formal × verificabilidad_efectiva` aplica directamente a Dom07. Para Dom09 y Dom08, donde la cadena hasta C9 es más larga, C8 puede requerir un factor adicional:

```
Dom09: C8 = proceso_documentado × verificabilidad × corrección_efectiva
Dom08: C8 = proceso_documentado × verificabilidad × incidencia_real
```

El tercer factor captura si el proceso observacional cerró el ciclo — si la rendición generó correcciones, si la participación generó cambios. Sin ese factor, C8 en Dom09 y Dom08 también puede premiar ceremonias bien documentadas.

---

## Implicación para el Semáforo

> **Verde en un dominio observacional no significa que el servicio fue prestado.**  
> **Verde significa que la información sobre el servicio es pública, actual y verificable.**

El Verde en Dom07 no dice "el municipio es transparente."  
Dice "el municipio ha hecho verificable su transparencia."  
La diferencia es epistemológicamente crítica y debe preservarse en la narrativa de C10.

---

## Núcleo del Framework — Conexión al Meta-Principio

QNKC-P01 no es una excepción de Dom07. Es la segunda instancia de un meta-principio que ya opera en el sistema desde la decisión de colocar LOTAIP en C4:

> **Meta-principio QNKC: Existencia documental ≠ Cumplimiento institucional**

Las dos instancias conocidas:

| Principio | Enunciado operacional | Consecuencia de diseño |
|-----------|----------------------|----------------------|
| OBLIGACIÓN SUSTANTIVA ≠ VENTANA DE OBSERVACIÓN | LOTAIP no crea la obligación de prestar el servicio — solo crea el mecanismo de verificación de que se prestó | LOTAIP vive en C4, no en C2. Dom07 no absorbe Dom02, Dom05, Dom10. |
| QNKC-P01 Dualidad Epistémica | El mismo artefacto documental tiene función operativa (C4) y función probatoria (C5) según quién lo lee | C8 = cumplimiento × verificabilidad. Un enlace roto = C8 cercano a cero aunque el municipio "haya publicado". |

Ambos principios resuelven el mismo problema: **evitar que la existencia de un documento sea confundida con la existencia del cumplimiento.**

El primer principio lo resuelve en el eje de las *capas* (dónde vive la norma en la cadena C1-C9).  
El segundo lo resuelve en el eje de la *lectura* (quién lee el artefacto y con qué propósito).

Son ortogonales — se necesitan ambos para blindar el sistema contra el compliance de fachada.

**Posición en la jerarquía del framework:** QNKC-P01 opera al mismo nivel que "OBLIGACIÓN SUSTANTIVA ≠ VENTANA DE OBSERVACIÓN" — no como regla de un dominio específico, sino como principio transversal que aplica a cualquier dominio donde el producto principal sea información institucional.

---

## Origen y Validación

- Identificado durante construcción de `data/qtmp/qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` (2026-06-01)
- Validado y refinado por colega arquitectónico externo (2026-06-01)
- Aplicable a Dom07, Dom08, Dom09 — y a cualquier dominio futuro cuyo C3 sea producción de información institucional

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"El artefacto es uno. El ángulo epistémico es doble."*
