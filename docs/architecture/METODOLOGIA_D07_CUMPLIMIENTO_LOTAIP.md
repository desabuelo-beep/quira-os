# Metodología d07 — Verificación de Cumplimiento LOTAIP (rediseño Gold Master)

> **Estado:** APROBADO (Capa 2 Metodológica del Protocolo de Curación) · propuesto 2026-07-21 · **ratificado por Javo 2026-08-07**
>
> **Al sellarse, la cadena normativa quedó completa en el corpus** (2026-08-07). Las tres
> piezas vigentes de la DPE están ingeridas con su huella y ninguna anula a otra:
> Guía Metodológica (Res. 019, 241 fragmentos) · Instructivo de Parámetros Técnicos
> (Res. 015, 47) · Instructivo de Monitoreo (42). `app/agents/d07/scoring.py` implementa
> las reglas del tercero, así que hasta ahora cada puntaje habría citado una norma que el
> sistema no tenía verificada (Regla 3). Ese bloqueo está levantado.
> **Nace en el canon, no en el Excel** (Regla 9). Este documento define el modelo; el Excel lo implementa después, sobre copia, con evidencia (Regla de Oro 1).

## 0 · Por qué se rediseña (diagnóstico que lo motivó)

El d07 actual del Gold Master **no tiene un motor de cumplimiento LOTAIP**. Rastreo del 2026-07-21:

| Cifra publicada | Qué es en realidad |
|---|---|
| **82.29%** (viaja a UI) | `1 − IOC`. El IOC (17.71%) es una métrica del **motor ICPI** (metas Pi alto × Vi bajo = inversión sin evidencia, `H37!E17`), base de ADR-022. **No mide transparencia LOTAIP.** |
| **56%** (glosario/índice) | Valor **pegado a mano**, sin fórmula ni fuente trazable. |
| **~88%** (promedio H09) | Scores por meta **simulados** ("desde patrón 2024", nota H09!A57). |

Conclusión: ninguna cifra deriva de una verificación real de la ley. Se reconstruye entero.

## 1 · Doctrina (Javo, 2026-07-21) + Jerarquía normativa (colega, 2026-07-22)

```
Constitución
   ↓
Ley (LOTAIP)                          → define las obligaciones jurídicas
   ↓
Reglamento (RLOTAIP)                  → las desarrolla
   ↓
Guía Metodológica de Mecanismos 2024  → operativiza QUÉ debe publicarse (conjuntos de datos CD-XX)
   ↓
Instructivo de Monitoreo 2024         → define CÓMO se evalúa (criterios, escala, formatos) ← hallado 2026-07-22
   ↓
Formatos oficiales DPE (Formato N)    → la plantilla concreta de cada CD
   ↓
Videos de capacitación DPE            → refuerzo operativo (nota: falta el del Presupuesto — §5b)
   ↓
Portal Nacional de Transparencia      → la evidencia real
   ↓
QUIRA                                 → verifica evidencia contra toda esta cadena
```

> **Distinción clave (colega, 2026-07-22):** la **Guía** dice *qué* debe publicarse; el **Instructivo de Monitoreo 2024** dice *cómo la DPE lo evalúa* (escala, dimensiones, formatos). No son lo mismo — el Instructivo es la capa que faltaba, y es la que convierte a QUIRA en reproductor del estándar oficial en vez de evaluador con criterios propios.

1. **QUIRA no hereda la calificación de la DPE.** La DPE evaluó Montecristi 100/100, pero su matriz operativa está incompleta (numeral 6 sin cédula de ingresos, literal D ausente, numerales 5-22 fusionados — verificado, OBS-011). Una calificación sobre una matriz sesgada es un falso positivo estructural.
2. **El cumplimiento se valida contra la norma, no contra el evaluador.** Fuentes: **LOTAIP + Reglamento + Guía Metodológica 2024** (canon vigente, ya en el corpus con SHA). QUIRA no compara Portal↔matriz-DPE; compara **Portal↔Guía↔Reglamento↔Ley**.
3. **La verificación es sobre lo realmente publicado en el Portal Nacional de Transparencia** — evidencia directa, no reporte de terceros.
4. **Principio de reproducibilidad (colega, 2026-07-22):** todo valor de ITAM debe ser reconstruible desde evidencia + reglas explícitas — `Valor = Norma + Portal + Regla explícita`, nunca un texto pegado ni una calificación heredada. Si un valor no puede regenerarse desde datos y fórmula, no es un indicador válido. Es la misma condición que ya falló en 56%/82.29%/88% (§0).

## 2 · Unidad de medición (RATIFICADA + corrección Javo 2026-07-21)

**La unidad NO es el numeral suelto de la ley — es el CONJUNTO DE DATOS de la Guía Metodológica 2024**, tal como el portal lo estructura. Tres planos, cada uno con su rol:

| Plano | Rol | Ejemplo |
|---|---|---|
| **Ley (LOTAIP Art. 19 · 24 numerales + Art. 24)** | Define el **universo** de obligaciones (qué debe existir) | num. 5 = servicios/horarios · num. 22 = formularios/formatos |
| **Guía Metodológica 2024** | **Operativiza**: agrupa y despliega los numerales en **conjuntos de datos** verificables (la estructura real del portal) | **la guía une 5 + 22 en un solo conjunto de datos** (servicios + sus formularios) |
| **Portal Nacional de Transparencia** | Donde se **verifica** — sigue la estructura de la guía | un dataset publicado por conjunto |

> **Lección arquitectónica (Javo):** modelar la matriz desde la numeración cruda de la ley e ignorar cómo la guía la operativiza es un **error metodológico y arquitectónico grave** — la matriz no coincidiría con lo que realmente se verifica en el portal. La ley manda; la guía la traduce en unidades verificables; se mide contra la guía, trazando cada conjunto a su(s) numeral(es) de ley.

Esto además corrige el error de fondo del H09 actual, que medía "por meta PDOT" (mezclaba planificación d01 con transparencia d07).

**Nomenclatura (colega, 2026-07-22):** cada conjunto de datos recibe un ID `CD-XX` con columna de trazabilidad a su(s) numeral(es) de ley:

| Conjunto | Ley | Nombre operativo |
|---|---|---|
| CD-05 | Art.19 num. 5 + num. 22 | Servicios y acceso ciudadano |
| CD-06 | Art.19 num. 6 | Presupuesto |
| CD-08 | Art.19 num. 8 | Contratación |
| … | … | (se completa en la fase de evidencia, §3) |

## 3 · Universo de obligaciones — el catálogo lo fija la Guía, no yo (Regla 3)

El **catálogo operativo** (cuántos conjuntos de datos, qué agrupa cada uno) es autoridad de la **Guía 2024 + el portal real**, no de una lista inferida de la ley. Se levanta al implementar (fase de evidencia), leyendo la guía/portal — no se inventa aquí.

Lo confirmado hasta ahora del corpus (`GUIA-LOTAIP-MEC`), estructura de la guía:
- **Sección Art. 19** — obligaciones generales de transparencia activa, un "Conjunto de datos" por bloque, **con agrupamientos** (confirmado: **CD-05 = num. 5 + num. 22**; hay que mapear el resto contra el portal).
- **Sección Art. 20-30** — obligaciones específicas por tipo de entidad (Art. 20 Min. Finanzas, 28 Partidos, 29 Empresas Públicas, 30 IESS…).
- **Sección Art. 24 GAD** — procesos legislativos/planificación (ordenanzas, PDOT/PUGS) + actas de sesiones + procesos de contratación.

Cada fila del nuevo H09 = **un conjunto de datos de la guía** (`CD-XX`), con columna de trazabilidad al/los numeral(es) de ley que operativiza. **CD-06** (presupuesto: ingresos + gastos) es el caso de prueba (§7).

**Pendiente de la fase de evidencia:** extraer de la guía/portal el catálogo exacto de conjuntos de datos aplicables a un GAD municipal (con sus agrupamientos y sus campos = criterio de completitud).

## 4 · Criterio de score — es el ESTÁNDAR OFICIAL DPE, no una invención (Instructivo 2024)

Hallazgo del 2026-07-22: el modelo de 4 dimensiones **no hay que diseñarlo — ya existe** en el Instructivo de Monitoreo 2024 de la DPE. QUIRA lo reproduce fielmente y lo aplica con verificación independiente. Dimensiones oficiales, con su tabla en el Instructivo:

| Dimensión (nuestra) | Nombre oficial DPE | Escala oficial | Tabla Instructivo |
|---|---|---|---|
| **A. Existencia / Integridad** | Información completa y actualizada | **1.0 / 0.5 / 0.0** | Tabla 0 |
| **B. Datos abiertos** | Estructura de datos abiertos ("tres estrellas") | 1 / 0 | Tabla 1 |
| **C. Actualización** | Registro dentro del plazo | 1 / 0 | Tabla 2 |
| **D. Cualitativas** | Estado de verificables · Vigencia · Validez | SI / NO | Tabla 5 |

**La escala `1.0 / 0.5 / 0.0` que habíamos propuesto es literalmente la de la DPE** (Tabla 0: completa=1.0 · incompleta/desactualizada=0.5 · sin información=0.0). Coincidencia total — se adopta la oficial.

**Existencia como gate** (colega): si no hay publicación, el score es 0 (nada que evaluar en las demás dimensiones).

**Función de agregación — RESUELTA por el estándar oficial (Instructivo 2024, §Subíndice de Transparencia Activa):**

```
SITA [%] = (CTA + ETA + RP + CI) / 4
```
| Sigla | Parámetro oficial | Tabla |
|---|---|---|
| **CTA** | Condiciones de transparencia activa (completa/incompleta/sin info) | Tabla 0 |
| **ETA** | Estructura de datos abiertos (tres estrellas) | Tabla 1 |
| **RP** | Registro dentro del plazo | Tabla 2 |
| **CI** | Calidad de la información (cualitativa: verificables·vigencia·validez) | Tabla 5 |

**SITA = promedio simple de los 4 parámetros** (cada uno promediado sobre los conjuntos, expresado en %). No es ponderado, no es multiplicación. Queda descartada tanto la multiplicación (`1×1×0×1=0`) como cualquier ponderación 40/30/30 hipotética: **QUIRA reproduce el SITA oficial tal cual**. La única decisión abierta (§10) es si además QUIRA publica un índice *complementario* que exponga las omisiones del propio estándar (como el numeral 6).

El score es de **verificabilidad documental**, no de calidad de gestión (Principio Rector). La dimensión Integridad reusa el eje `completitud` del modelo de manifestaciones PDOT.

## 4b · Algoritmo SITA oficial reconstruido (Instructivo 2024, §6-8)

**El flujo completo (colega, 2026-07-22): la fórmula `(CTA+ETA+RP+CI)/4` es solo la última línea, no el algoritmo.** El motor real es:

```
Artículo LOTAIP (Art.19/24)
      ↓
Formato oficial DPE (Anexo 1 del Instructivo)     ← específico por CD, viene del Catálogo CD-XX (Producto C)
      ↓
Campos obligatorios del formato                    ← específico por CD (conjunto de datos + metadatos + diccionario)
      ↓
Reglas de completitud/vigencia/validez (§ abajo)   ← genéricas, se aplican igual a cualquier CD
      ↓
CTA · ETA · RP · CI  (score por CD, cada uno 0/0.5/1 o SI/NO)
      ↓
SITA = (CTA+ETA+RP+CI)/4   (promedio sobre todos los CD evaluados)
```

Las reglas de scoring (esta sección) son **genéricas y ya están cerradas**. Lo que falta para
ejecutarlas sobre un CD concreto es su insumo específico — "Formato oficial" y "Campos
obligatorios" — que es exactamente lo que construye el Catálogo Canónico CD-XX (Producto C,
siguiente pieza). Por eso el colega ordena: primero este algoritmo, después el Catálogo.

Cada parámetro se calcula así (reglas literales de la DPE — van directo al Gold Master):

### CTA — Condiciones de transparencia activa → `1.0 / 0.5 / 0.0` (Tabla 1)
Combina dos verificaciones:
- **Actualizada:** en el archivo *metadatos*, el campo `fecha` corresponde al **mes anterior** a la fecha de monitoreo.
- **Completa:** en *conjunto de datos* + *metadatos* + *diccionario de datos*, **ningún campo vacío**. Un campo sin dato solo es válido si dice `INFORMACIÓN NO DISPONIBLE` o `NO APLICA` **y** el diccionario trae la nota aclaratoria.
- Resultado: completa+actualizada = **1.0** · publicada pero incompleta o desactualizada = **0.5** · no publicada/inaccesible = **0.0**.

### ETA — Estructura de datos abiertos → `1 / 0` (Tabla 2, escala Berners-Lee, tope 3★)
- 1★ = no estructurado (PDF, HTML, ZIP, DOC, PPT, JPG) · 2★ = estructurado (XLS, XLSX) · **3★ = estructurado no propietario (CSV, TSV, XML, JSON, ODS)**.
- La DPE evalúa **hasta 3★**: alcanza 3★ = **1**, no = **0**. (Aquí el CSV del numeral 6 sí puntúa en ETA — el problema del num. 6 es de CTA/completitud, no de formato.)

### RP — Registro dentro del plazo → `1 / 0` (Tabla 3)
- Registrado en el Portal hasta el **15 de cada mes** (o siguiente día laborable) con la info del cierre del **mes inmediato anterior** = **1** · fuera de plazo = **0**. (Art. 12 Reglamento.)

### CI — Calidad de la información (cualitativa) → `SI / NO` (Tabla 6)
Tres sub-ámbitos:
- **Estado de verificables:** los enlaces de los formatos de datos abiertos son de libre acceso, funcionan y corresponden a la información difundida.
- **Vigencia:** para formatos con fecha de inicio/plazo (num. 16 y 18 del Art. 19; formatos 1,2,4,5 del Art. 21) la información está dentro del plazo de vigencia.
- **Validez:** para formatos con valores dependientes (num. 3 Remuneraciones: "Total ingresos adicionales" = suma de componentes) los valores son coherentes. Si el formato tiene >3 filas, se validan **3 filas al azar**.

### Agregación
```
SITA [%] = (CTA + ETA + RP + CI) / 4
```
Cada parámetro se promedia sobre los conjuntos/numerales evaluados y se expresa en %. El SITA es el promedio de esos cuatro promedios. QUIRA lo reproduce exactamente y responde: *"si la DPE aplicara correctamente su propio Instructivo, este sería el resultado."*

## 5 · Regla anti-sesgo DPE

La calificación DPE (p. ej. "100/100") **no entra al cálculo del score**. Puede **registrarse como dato de contraste** (columna aparte) para exponer la divergencia QUIRA-vs-DPE — que es en sí un hallazgo (igual que OBS-009 SIGAD vs LOTAIP). Nunca como fuente de la puntuación.

**Matiz importante (Instructivo 2024):** QUIRA sí adopta el *estándar de evaluación* de la DPE (el Instructivo: dimensiones, escala, formatos) — eso es reproducir el canon oficial, no heredar sesgo. Lo que NO adopta es la *calificación resultante* de la DPE sobre un GAD, ni las omisiones del estándar operativo (como el numeral 6 sin ingresos). Distinción: se reproduce **cómo se mide** (Instructivo), se verifica **de forma independiente** el resultado, y se señala cuando el propio estándar operativo contradice a la norma superior (Ley/Reglamento).

## 5b · Observación metodológica — video de capacitación ausente (Presupuesto)

La DPE publica videos de capacitación para prácticamente todos los formatos (1.1, 1.2, 1.3, 4, 5-22, 10, 16, 17, 18, 19, 20, 21, 23, 24). **Falta precisamente el del formato de Presupuesto Institucional** — el mismo formato donde se identificó la mayor inconsistencia del estándar (ausencia de la cédula de ingresos, §7 / OBS-011). No se afirma intencionalidad; se **documenta como observación** para analizar durante la reconstrucción del estándar (Fase 1). Es un dato, no una conclusión (Principio Rector).

## 6 · Agregación → ITAM + separación del IOC(motor)

- **ITAM (d07)** = promedio de los scores de cumplimiento LOTAIP. Fórmula viva desde el nuevo H09. Es lo que d07 reporta y lo que viaja a H73 → UI como "transparencia".
- **IOC (motor)** = se queda intacto en su eje (Pi×Vi, `H37`, ADR-022). Solo se **re-etiqueta**: deja de llamarse "opacidad LOTAIP" (H41!A3 hoy lo define mal); su nombre correcto es opacidad de inversión / riesgo reputacional. **ADR-022 no se toca en su fondo** — solo su glosa que confundía ambos ejes.
- Se **elimina** la identidad falsa `ITAM = 1 − IOC`. Son dos ejes distintos.

## 6b · CD-06 no es una fila — es árbol + entidad (colega, 2026-07-22)

El texto literal del Art. 19.6 (verificado en el corpus 2026-07-22, ver OBS-011) ya especifica la
estructura interna: *"...especificando **ingresos, gastos, financiamiento** y **resultados
operativos**... así como **liquidación** del presupuesto..."*. CD-06 tiene dos dimensiones de
modelado, no una:

**Árbol (sub-componentes internos de contenido):**
```
CD-06 — Presupuesto Institucional
   ├── Ingresos            ← el sub-componente ausente (OBS-011)
   ├── Gastos
   ├── Financiamiento
   ├── Resultados operativos
   └── Liquidación del presupuesto
```

**Entidad (modelo de objeto, colega 2026-07-22 — mismo esquema para cualquier CD):**
```
CD-06 {
    Dominio:        d07 (+ observa d02 Presupuesto, ver DOMINIOS_QUIRA cruzado)
    Fuente:         LOTAIP Art.19.6 + RLOTAIP Art.11/12 + GUIA-LOTAIP-MEC + INST-TA-2024
    Componentes:    [Ingresos, Gastos, Financiamiento, Resultados_operativos, Liquidación]
    Reglas:         CTA/ETA/RP/CI (§4b) — una instancia por componente
    Evidencia:      {url, sha256, fecha_verificación} — por componente
    Score:          SITA agregado de los componentes
    Observaciones:  libre (ej. OBS-011, ausencia de video §5b)
}
```
Cada elemento de `Componentes` es a su vez una instancia con sus propios `Reglas`/`Evidencia`/
`Score` — es un objeto recursivo, no una fila plana. El Gold Master implementa este esquema como
tabla relacional (CD → Componentes 1:N), no como columnas fijas por CD.

Cada sub-componente del árbol recibe su propio CTA/ETA/RP/CI (§4b); el score de CD-06 (campo
"Score SITA" de la entidad) es la agregación de sus sub-componentes. **El Gold Master trabajará
con entidades, no con jerarquías visuales** — el árbol explica el contenido; la entidad es lo que
se implementa (fila/registro). Este mismo patrón (numeral de ley → árbol de sub-componentes +
entidad de metadatos) se aplica a cada CD en el Catálogo (Producto C) — no es exclusivo de CD-06.

## 7 · Caso de prueba — CD-06 Presupuesto (Montecristi)

| Dimensión | Verificación | Valor |
|---|---|---|
| A. Existencia | Cédula presupuestaria publicada en el portal | **1** |
| B. **Integridad documental** | **Solo egresos; falta cédula de ingresos** (CSV oficial: 75 registros, 100% cuentas "5"/"8") — la Guía exige ingresos+gastos | **0.5 (parcial)** |
| C. Actualización | Publicación mensual | **1** |
| D. Accesibilidad | Enlace/CSV abre correctamente | **1** |
| **Score CD-06** | Existencia=1 (gate pasa) → agregación de B/C/D (§4, fórmula pendiente de validación) | **parcial, no 0 ni 1** |

Con **nota de contexto OBS-011**: la incompletitud tiene causa intersistémica (el Portal Nacional no tiene campo para ingresos — falla reconocida por la DPE, correo 2026-07-09), documentada sin lenguaje acusatorio (Regla de Oro 2).

## 8 · Impacto en el Gold Master (implementación posterior, sobre copia)

| Hoja | Cambio |
|---|---|
| **H09_S7** | Reconstruida: 25 metas PDOT → matriz de **conjuntos de datos de la Guía 2024** (`CD-XX`, con agrupamientos reales, ej. CD-05). Columnas: CD · Numeral(es) de ley · Existencia · Integridad · Actualización · Accesibilidad · Score · Evidencia(URL/SHA) · Score_DPE(contraste). Fin de la simulación. |
| **H18_ITAM** | ITAM = fórmula viva `=AVERAGE(scores H09)`. Se elimina el hardcode 0.8229 y la nota huérfana 56%. B59 (fórmula rota sobre columna de texto) se elimina. |
| **H41_IOC** | Re-etiquetado: IOC = opacidad de inversión (motor), no "opacidad LOTAIP". Se corrige A3. |
| **H73_OUTPUT_API** | `ITAM_2025_REF` pasa a apuntar al ITAM real; se rompe `ITAM = 1−IOC`. |
| **H09!B7 / H18!B8** | "DPE — Dirección Provincial de Empoderamiento" → **Defensoría del Pueblo del Ecuador**. |

## 9 · Qué NO cambia (blindaje)

- **H12!B33 (fórmula canónica del ICPI)** — INMUTABLE. Este rediseño no la toca.
- **IOC del motor (Pi×Vi)** y **ADR-022** en su fondo — el índice de opacidad de inversión sigue válido; solo se separa del nombre "transparencia".
- **El corpus normativo v1.0** — la norma que sirve de base ya está congelada, sin cambios.

## 9b · Temporalidad — la evaluación es MENSUAL, no anual (Javo, 2026-07-22)

La unidad de evaluación **no es "el año" — es `(CD × mes)`**. La LOTAIP exige publicación
mensual (Art. 19; el registro se hace hasta el 15 de cada mes — es el parámetro RP del SITA). Por
tanto:

- **SITA mensual por CD** es el dato base. Cada mes de 2025 y 2026 es una foto independiente.
- **Acumulado anual** = agregación de los 12 SITA mensuales (no una evaluación anual única).
- **Comparativos**: mes vs mes · año vs año (2025 vs 2026) · CD vs CD.
- **Patrones**: qué CD incumple de forma **recurrente** (no un mes aislado) — señal más fuerte que
  un fallo puntual.
- **Hallazgos**: rupturas en la serie (un CD que dejó de publicarse, uno que mejoró tras una
  observación, estacionalidad).

**Implicación de datos (ya reflejada en el esqueleto):** la persistencia guarda por
`(dominio, municipio, cd, año, mes)` — ver `app/agents/d07/persistencia.construir_resultado`
(campo `periodo = "AAAA-MM"`). El grafo modelará `(:Evaluacion {cd, periodo, sita})`, no un score
único por CD. El barrido de Fase 4 recorre **CD × mes** del portal, no CD una sola vez.

**Estado del motor (Opción D del colega, aplicada al Gold Master 2026-07-22):** mientras no haya
evidencia real, H18 conserva el ITAM heredado marcado `Estado_Motor_SITA = LEGACY` (H18!B22) — no
muestra 0% ni falso "pendiente", conserva trazabilidad histórica y permite comparar antes/después.
Pasa a `VERIFICADO` (fórmula viva sobre la serie mensual de H09) cuando Haiku produzca el primer
piloto. La reconstrucción de H09 se pospone a ese momento (evita rehacerla dos veces).

## 10 · Dependencias aguas abajo a revisar (Capa 5-7)

- **Fondos (FICHA-01):** la brecha AECID (≥65) se calculó con 56%. Al reconstruir el ITAM sobre evidencia real, la brecha se recalcula con dato verificable (no con el 82.29% que la borraba falsamente).
- **ADR-022:** revisar la redacción "divergencia SIGAD vs ITAM(82.29%)" — comparaba contra 1−IOC, no contra transparencia.
- **UI d07 / narrativa:** el dashboard debe mostrar cumplimiento por obligación, con la nota del numeral 6.

---
*Metodología d07 · Dylus Lab © 2026 · "La transparencia se mide contra la ley, no contra quien la califica."*
