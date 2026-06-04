# QUIRA Causal Model v1.0
**Modelo Causal — Epistemología de Causalidad Institucional Territorial**

**Versión**: 1.0 — CONGELADO  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Fecha**: 2026-05-31  
**Estado**: Alpha 0.9 — documento fundacional pre-Neo4j  
**Caso fundante**: Paradoja COOTAD_249 — Patronato Montecristi 2025

---

## PRINCIPIO FUNDACIONAL

> QUIRA no monitorea lo que ocurre. QUIRA explica por qué ocurre.

Un dashboard muestra que el Patronato ejecutó el 50% de su presupuesto.  
QUIRA explica que el 20.84% del presupuesto GAD está asignado (COOTAD_249 cumplido), pero el Patronato convierte solo el 50% de esa asignación en gasto real, y que esa brecha de ejecución — no la norma — es la causa de que los grupos prioritarios de Montecristi no reciban los servicios que les corresponden legalmente.

La diferencia entre ambas afirmaciones es la diferencia entre un dashboard y un sistema de inteligencia causal.

---

## I. LA DISTINCIÓN QUIRA: CORRELACIÓN VS. CAUSALIDAD INSTITUCIONAL

```
Correlación observada:
  Cuando Ti_Patronato < 70%, el NBI Dom12 no mejora.

Causalidad institucional QUIRA:
  COOTAD_249 obliga al GAD a asignar ≥ 10% del presupuesto no-salarial
  al Patronato. El GAD cumple (20.84%). Pero el Patronato ejecuta solo el
  50% de lo asignado → los recursos jurídicamente destinados a grupos
  prioritarios no se convierten en servicios → el NBI Dom12 no mejora.

  La causa no es la norma. La causa es la capacidad institucional del
  Patronato para ejecutar su propio presupuesto.
```

**La causalidad institucional QUIRA requiere tres elementos:**

1. **Una norma** que establece la obligación (ACK — QLEP corpus)
2. **Una cadena de transmisión** que conecta norma → resultado (QNKC-002)
3. **Un nodo de ruptura** que identifica dónde la cadena falla (C9 ↔ semáforo)

Sin norma fundante, no hay causalidad institucional verificable — solo correlación estadística.

---

## II. QNKC-002: LA CADENA DE 9 CAPAS

La cadena QNKC-002 es la unidad estructural fundamental de QUIRA.  
Cada circuito temático (QTMP) materializa exactamente una instancia de esta cadena para un territorio y período.

```
C1  NORMA / ACK          ← Átomo Canónico de Conocimiento (QLEP)
     ↓ FUNDA
C2  COMPETENCIA          ← Habilitación o mandato institucional
     ↓ GENERA
C3  SERVICIO PÚBLICO     ← Prestación hacia el ciudadano
     ↓ IMPLEMENTADO_VIA
C4  PROCESO              ← Proceso administrativo / operativo
     ↓ PRODUCE
C5  EVIDENCIA            ← Documento, registro, acto administrativo
     ↓ SUJETA_A
C6  CONTROL              ← Mecanismo de fiscalización (CGE, DPE, CPCCS)
     ↓ VERIFICADO_POR
C7  OBSERVABILIDAD       ← Sistema o portal donde el dato es visible
     ↓ ALIMENTA
C8  INDICADOR            ← Métrica con fórmula, fuente y umbrales
     ↓ MIDE
C9  RESULTADO TERRITORIAL ← Valor observado o calculado para un cantón/período
```

**Principio de completitud de cadena:**

Un C9 sin C1 (norma fundante) es una métrica huérfana — no es QUIRA.  
Un C1 sin C9 es una norma no monitoreada — no es QUIRA.  
La cadena debe ser completa en ambas direcciones.

**El grafo Neo4j materializa cada eslabón como un nodo y cada `↓` como una relación tipada.**

---

## III. TAXONOMÍA DE RELACIONES CAUSALES

```
(:Atom)-[:FUNDA]->(:C2Competencia)
  El átomo normativo (ACK) es la fuente jurídica de la competencia.

(:C2Competencia)-[:GENERA]->(:C3ServicioPublico)
  La competencia habilitada produce una obligación de servicio.

(:C3ServicioPublico)-[:IMPLEMENTADO_VIA]->(:C4Proceso)
  El servicio se materializa en procesos administrativos concretos.

(:C4Proceso)-[:PRODUCE]->(:C5Evidencia)
  El proceso debe generar evidencia verificable de cumplimiento.

(:C5Evidencia)-[:SUJETA_A]->(:C6Control)
  La evidencia es auditada por organismos de control.

(:C6Control)-[:VERIFICADO_POR]->(:C7Observabilidad)
  El control es ejercitable porque el dato es observable públicamente.

(:C7Observabilidad)-[:ALIMENTA]->(:C8Indicador)
  El portal o sistema observable provee los datos al indicador.

(:C8Indicador)-[:MIDE]->(:C9ResultadoTerritorial)
  El indicador, aplicado a un territorio y período, produce un resultado.

(:C9ResultadoTerritorial)-[:ANCLADO_EN]->(:Canton)
  El resultado es siempre territorial — no existe sin territorio.
```

**Relaciones de causalidad horizontal (entre cadenas distintas):**

```
(:C8Indicador)-[:HABILITA]->(:C8Indicador)
  El cumplimiento de un indicador es condición habilitante de otro.
  Ejemplo: Dom02 (ejecución presupuestaria) → Dom12 (inversión GAP efectiva).

(:C8Indicador)-[:CONSTRIÑE]->(:C8Indicador)
  El incumplimiento de un indicador limita el alcance de otro.
  Ejemplo: Dom05 (talento humano débil) → constriñe Dom03 (contratación).

(:C9ResultadoTerritorial)-[:EXPLICA]->(:C9ResultadoTerritorial)
  Un resultado territorial es causa directa de otro.
  Ejemplo: Ti_Patronato=50%(Dom12) → NBI_Dom12_no_mejora.

(:C9ResultadoTerritorial)-[:PREDICE]->(:C9ResultadoTerritorial)
  Relación predictiva basada en historial confirmado.
  Ejemplo: Ti_Patronato<70% por 3 años → predice NBI Dom12 > 30%.
```

---

## IV. LOS 12 DOMINIOS COMO NODOS DE CAUSALIDAD VERTICAL

Cada dominio representa una dimensión de la acción institucional del GAD.  
Los dominios no son categorías de datos — son nodos de causalidad en el grafo.

```
Dom01  Legalidad e Institucionalidad       (condición base del sistema)
Dom02  Presupuesto, Inversión y Financiamiento  (habilita todos los demás)
Dom03  Contratación Pública                (materializa la inversión)
Dom04  Planificación Territorial           (PDOT como Constitución Territorial)
Dom05  Talento Humano y Gestión Interna    (constriñe o amplifica todos)
Dom06  Agua, Saneamiento y Servicios Básicos   (indicador de bienestar basal)
Dom07  Transparencia e Información Pública (habilita control ciudadano)
Dom08  Participación Ciudadana             (fuente de mandato democrático)
Dom09  Ambiente y Gestión de Riesgos       (condición de sostenibilidad)
Dom10  Vialidad y Movilidad Urbana         (conecta territorio y servicios)
Dom11  Ecosistema Productivo Territorial   (capacidad generativa del cantón)
Dom12  Protección Social y Grupos Prioritarios  (resultado humano final)
```

**Jerarquía causal de dominios (dirección de dependencia):**

```
Dom01 (legalidad) y Dom04 (planificación) → condiciones estructurales basales
  ↓ habilitan
Dom02 (presupuesto) → condición habilitadora de todos los demás
  ↓ materializado por
Dom03 (contratación) y Dom05 (talento humano)
  ↓ producen resultados en
Dom06, Dom07, Dom08, Dom09, Dom10, Dom11 → resultados de proceso/gestión
  ↓ acumulan en
Dom12 (protección social) → resultado humano final / indicador de impacto territorial
```

**REGLA DE DIRECCIÓN CAUSAL:**
No toda relación entre dominios es simétrica.  
Dom02 constriñe Dom12 (sin presupuesto no hay servicio social).  
Dom12 no constriñe Dom02 (el resultado social no determina el presupuesto).  
El grafo Neo4j debe codificar la dirección correctamente.

---

## V. CIRCUITOS HORIZONTALES — CONEXIONES ENTRE DOMINIOS

Los circuitos horizontales (H) son relaciones causales documentadas entre dos o más dominios que QUIRA activa cuando ambos tienen datos confirmados.

### Circuitos activos en Montecristi Alpha 0.9

```
H1  COOTAD_249 ↔ COOTAD_215
    Dom02 → Dom12
    La ejecución presupuestaria GAD (Dom02, Ti=59.85%) determina el margen
    disponible para el Patronato. Si el GAD no ejecuta bien, el Patronato
    no recibe transferencias a tiempo → Dom12 sufre.
    Estado: activo — datos parcialmente disponibles.

H2  LOD_58 ↔ COOTAD_137
    Dom12 → Dom06 (accesibilidad + infraestructura)
    La accesibilidad universal (rampas, aceras) en zonas urbanas facilita
    el acceso de personas con discapacidad a servicios básicos.
    Estado: pendiente — requiere PUGS Montecristi + LOD_58 cumplimiento.

H3  LOTAIP ↔ COOTAD_249
    Dom07 → Dom12
    La transparencia de datos Patronato (portal LOTAIP) habilita el control
    ciudadano (Dom08) que a su vez presiona el cumplimiento Dom12.
    Estado: pendiente — requiere auditoría LOTAIP portal Montecristi.

H4  LOD_47 ↔ COOTAD_198
    Dom12 → Dom05
    El 4% de inclusión laboral de personas con discapacidad (LOD_47)
    dentro del GADMCM (Dom05) es a la vez un indicador Dom12 y una
    obligación de talento humano Dom05. Los dominios se cruzan.
    Estado: pendiente — requiere nómina SIGEF + CONADIS registro.

H5  COOTAD_264 ↔ CE_32
    Dom04 → Dom06
    El PDOT debe planificar agua potable y saneamiento. Si Dom04 no
    planifica Dom06, la inversión en servicios básicos es improvisada.
    Estado: activo en GAP_AGUA_POTABLE.yaml — datos disponibles.

H6  LOSNCP_21 ↔ COOTAD_249
    Dom03 → Dom12
    Si el Patronato no contrata (LOSNCP — Dom03), no puede ejecutar
    programas GAP aunque tenga el presupuesto asignado. La subjecución
    Dom12 puede ser causada por debilidad en contratación Dom03.
    Estado: hipótesis — requiere PAC Patronato 2025 para validar.

H7  COOTAD_249 ↔ COOTAD_228
    Dom12 → Dom11 (inversión GAP vs. inversión productiva)
    La inversión en grupos prioritarios (Dom12) puede competir por
    recursos con la inversión productiva territorial (Dom11).
    Tensión de asignación presupuestaria en cantones pequeños.
    Estado: pendiente — requiere análisis estructura presupuestaria.

H8  COOTAD_304 ↔ COOTAD_249
    Dom08 → Dom12
    Si el proceso participativo (Dom08, rendición de cuentas + consultas)
    prioriza las demandas de grupos prioritarios, el GAD tiene mandato
    democrático para aumentar la asignación Dom12 sobre el mínimo legal.
    Estado: pendiente — requiere sistematización proceso participativo 2025.
```

---

## VI. EL CASO FUNDANTE: PARADOJA COOTAD_249

El caso fundante de QUIRA Causal Model es la paradoja descubierta en Montecristi (2026-05-31):

```
HECHO 1 (confirmado): El GAD asigna 20.84% del presupuesto no-salarial al Patronato.
         → COOTAD_249 cumplido formalmente. Semáforo: 🟢 VERDE.

HECHO 2 (confirmado): El Patronato ejecuta solo el 50% de lo asignado.
         → Ti_Patronato_2025 = 50%. Serie: 2023=35%, 2024=54%, 2025=50%.
         → Semáforo: 🔴 ROJO (3 años consecutivos).

PARADOJA: El GAD cumple la norma. El impacto no ocurre.
           ¿Quién es responsable? ¿Cuál es la causa?

EXPLICACIÓN CAUSAL QUIRA:
  La causa de la brecha Dom12 no es el incumplimiento de COOTAD_249
  (asignación formal). La causa es la incapacidad del Patronato de
  convertir el presupuesto asignado en gasto real.

  Posibles sub-causas (hipótesis — requieren datos adicionales):
    a) Debilidad en contratación pública (H6: Dom03 → Dom12)
    b) Estructura de personal pesada (G71 personal inversión = 67.60% Ti)
       frente a ejecución de programas (G73 bienes servicios = 29.73% Ti)
    c) Falta de planificación POA alineada con PDOT Dom12
    d) Capacidad técnica institucional insuficiente (Dom05 → Dom12)

  El montante no ejecutado ($2,048,280 ≈ 50% de $4.1M) no desaparece:
  ingresa como G97 (pasivo circulante) al siguiente ejercicio, acumulando
  rezago presupuestario que se vuelve estructuralmente difícil de ejecutar.
```

**La paradoja COOTAD_249 es la demostración empírica del valor de QUIRA:**  
ningún dashboard que muestre solo el cumplimiento formal de la norma capturaría este fallo.  
Solo la cadena QNKC-002 completa revela dónde está la ruptura.

---

## VII. REGLAS DE INFERENCIA CAUSAL CANÓNICA

```
Regla C1 — Dirección de causalidad:
  La causalidad fluye de norma → resultado, nunca al revés.
  Un C9 rojo no "causa" que el ACK sea malo. Causa que el C3 (servicio)
  no se presta, que el C4 (proceso) no funciona, o que el C6 (control)
  no detectó el fallo. La norma no es responsable del resultado.

Regla C2 — Confirmación antes de causalidad:
  Solo los nodos C9 con estado_dato: confirmado pueden activar inferencias
  causales en Neo4j. Los nodos pendiente_validacion o proxy pueden
  informar hipótesis pero no alimentar conclusiones causales formales.

Regla C3 — Nodo de ruptura explícito:
  Toda cadena causal debe identificar el nodo donde la transmisión falla.
  No es suficiente decir "el circuito no funciona". QUIRA debe responder:
  ¿En qué capa (C3, C4, C5, C6, C7) se rompe la cadena?

Regla C4 — Evidencia de ruptura:
  La identificación del nodo de ruptura debe estar respaldada por un C9
  con valor rojo o por la ausencia de evidencia (C5) verificable.
  La hipótesis de ruptura sin dato es una señal, no una conclusión.

Regla C5 — Causalidad horizontal vs. vertical:
  Vertical (QNKC-002): norma → resultado dentro de un mismo circuito.
  Horizontal (H1-H8): resultado de un dominio → impacto en otro dominio.
  Las causas horizontales son hipótesis hasta confirmarse con dos C9
  confirmados en dominios diferentes con correlación negativa documentada.

Regla C6 — La paradoja formal/real:
  Cuando un C9 de proceso (asignación formal) es VERDE y un C9 de
  resultado (impacto real) es ROJO para el mismo circuito, QUIRA activa
  la cadena H correspondiente para buscar el nodo de ruptura intermedio.
  Esta es la regla que captura paradojas tipo COOTAD_249.

Regla C7 — PDOT como referencia normativa territorial:
  El diagnóstico PDOT establece el estado inicial del territorio.
  Las metas PDOT son los objetivos contra los cuales QUIRA mide el avance.
  Si un C9 viola el diagnóstico PDOT (empeora la condición documentada),
  QUIRA activa alerta de regresión territorial.
  Ver: QUIRA Territorial Semantics v1.0 — Sección VII.
```

---

## VIII. ANTI-PATRONES CAUSALES

| Anti-patrón | Descripción | Corrección |
|---|---|---|
| **Causalidad inversa** | "La norma no funciona" cuando el problema es la implementación | Identificar nodo de ruptura en C3-C7, no en C1 |
| **Correlación como causalidad** | "Dom02 bajo → Dom12 bajo" sin cadena QNKC verificada | Documentar la cadena H explícita con hipótesis y estado |
| **C9 pendiente activa inferencia** | Usar resultado proxy para concluir ruptura causal | Solo C9 confirmado activa inferencia causal formal |
| **Paradoja ignorada** | Asignación formal VERDE + impacto real ROJO sin investigar ruptura | Activar búsqueda de nodo ruptura en cadena H |
| **Causalidad sin ACK** | Afirmar que X causa Y sin norma fundante verificable | Todo efecto institucional requiere un ACK en la base |
| **Ruptura sin evidencia** | Identificar "el proceso falla" sin un C5 ausente o un C9 rojo | Señalar como hipótesis hasta contar con dato confirmado |
| **Determinismo normativo** | Asumir que si la norma existe, el resultado ocurre | QUIRA mide la brecha norma→resultado — el determinismo es el error a combatir |
| **Unicausalidad** | Atribuir un C9 rojo a una sola causa | Dom12 rojo puede venir de Dom02, Dom03 y Dom05 simultáneamente |

---

## IX. TIPOLOGÍA DE CONCLUSIONES CAUSALES

QUIRA produce conclusiones causales de tres tipos, cada uno con diferente estatus epistemológico:

```
CONCLUSIÓN CONFIRMADA:
  "El Patronato ejecuta el 50% de su presupuesto de inversión (Ti=50%, ROJO)."
  → C9 con estado_dato: confirmado + Gold Master verificado.
  → Puede publicarse como hallazgo QUIRA sin restricciones.

CONCLUSIÓN HIPÓTESIS:
  "La baja Ti del Patronato puede deberse a debilidad en contratación (Dom03)."
  → Basada en dos C9 confirmados en dominios diferentes + cadena H documentada.
  → Se publica como "hipótesis QUIRA — verificación pendiente PAC Patronato 2025".

CONCLUSIÓN SEÑAL:
  "El rezago G97 del Patronato puede acumularse año a año si Ti < 70% persiste."
  → Proyección metodológica basada en serie histórica confirmada + regla QUIRA.
  → Se publica como "señal QUIRA — monitoreo trimestral necesario".
```

**El estatus de cada conclusión debe ser visible en la UI y en los informes.  
Mezclar los tres tipos sin distinción es un error de gobernanza epistémica.**

---

## X. NODO NEO4J — TIPOLOGÍA DE RELACIONES CAUSALES

```cypher
// Relaciones verticales (QNKC-002)
(:Atom)-[:FUNDA]->(c2:C2Competencia)
(c2)-[:GENERA]->(c3:C3ServicioPublico)
(c3)-[:IMPLEMENTADO_VIA]->(c4:C4Proceso)
(c4)-[:PRODUCE]->(c5:C5Evidencia)
(c5)-[:SUJETA_A]->(c6:C6Control)
(c6)-[:VERIFICADO_POR]->(c7:C7Observabilidad)
(c7)-[:ALIMENTA]->(c8:C8Indicador)
(c8)-[:MIDE]->(c9:C9ResultadoTerritorial)
(c9)-[:ANCLADO_EN]->(ct:Canton)

// Relaciones horizontales (H1-H8)
(c9a:C9ResultadoTerritorial)-[:HABILITA {circuito:'H5', confianza:'alta'}]->(c9b:C9ResultadoTerritorial)
(c9a:C9ResultadoTerritorial)-[:CONSTRIÑE {circuito:'H6', estado:'hipotesis'}]->(c9b:C9ResultadoTerritorial)
(c9a:C9ResultadoTerritorial)-[:EXPLICA {evidencia:'confirmada'}]->(c9b:C9ResultadoTerritorial)
(c9a:C9ResultadoTerritorial)-[:PREDICE {base:'serie_historica_3_anios'}]->(c9b:C9ResultadoTerritorial)

// Propiedades mínimas de C9ResultadoTerritorial para inferencia
{
  id: 'RES_G10P_04_MCR',
  valor: 50.0,
  estado_dato: 'confirmado',     // REQUERIDO para activar inferencia
  naturaleza_valor: 'calculado',
  semaforo: 'ROJO',
  periodo: '2025',
  canton_id: 'ECU-13-MONTECRISTI'
}
```

---

## XI. FLUJO DE ACTIVACIÓN CAUSAL — DE DATO A CONCLUSIÓN

```
C9 ingresado (estado_dato: confirmado)
    ↓
¿semáforo = ROJO?
    SÍ → activar búsqueda de ruptura en cadena QNKC-002
         → ¿cuál capa (C3/C4/C5/C6/C7) tiene evidencia de falla?
         → documentar nodo de ruptura + hipótesis
         → si ruptura identificada con otro C9 confirmado → CONCLUSIÓN_HIPOTESIS
         → si ruptura identificada con C9 confirmado en otro dominio → activar H
    NO → registrar como dato de contexto
         → verificar tendencia histórica (serie_historica)
         → si tendencia negativa por ≥ 2 períodos → SEÑAL_QUIRA

¿Existe paradoja formal/real?
  (C9_proceso = VERDE y C9_impacto = ROJO para mismo circuito)
    SÍ → activar Regla C6 → buscar nodo ruptura intermedio
         → documentar paradoja en Neo4j con relación :PARADOJA
    NO → seguir flujo estándar

¿C9 actualiza dato anterior?
    SÍ → verificar escalamiento (Gobernanza v1.0 Sección I)
         → si nuevo valor < umbral anterior → alerta de regresión
    NO → ingesta estándar
```

---

## XII. RELACIÓN CON OTROS DOCUMENTOS FUNDACIONALES

| Documento | Relación con Causal Model |
|---|---|
| QUIRA Data Governance v1.0 | Define `estado_dato` y `naturaleza_valor` — los prerequisitos de toda inferencia causal |
| QUIRA Territorial Semantics v1.0 | Define el `nivel_territorial` de cada C9 — sin territorio correcto, la cadena causal no se ancla |
| QTMP schema v1.1 | Implementación técnica del QNKC-002 en YAML — el formato que construye el grafo |
| QLEP SKILL.md | Fuente de los ACKs (C1) que fundan cada cadena causal — sin ACK, no hay C1, no hay cadena |
| SIAP-ICPI Gold Master | Fuente de los C9 confirmados que activan inferencias — sin Gold Master, no hay causalidad confirmada |
| PDOT Montecristi (futuro: atomizado) | Fuente de las metas de progreso territorial contra las cuales se mide cada C9 |

---

## XIII. HOJA DE RUTA CAUSAL — DESDE ALPHA 0.9

```
Alpha 0.9 (HOY — 2026-05-31):
  ✅ Causal Model definido (este documento)
  ✅ 3 circuitos QTMP con cadenas QNKC-002 completas:
     GAP_10PCT (Dom12) | AGUA_POTABLE (Dom06) | EQUIDAD (multi-dominio)
  ✅ 1 C9 confirmado con conclusión causal: Ti_Patronato=50% → Dom12 brecha
  ✅ Paradoja COOTAD_249 documentada formalmente

Alpha Neo4j (siguiente fase):
  → Cargar 3 circuitos en Neo4j
  → Ejecutar primera consulta causal pública
  → Verificar que las relaciones H1-H8 se codifican correctamente

Alpha Red Académica:
  → Validar causalidad H1-H8 con metodología externa (UEB/ESPAM/FLACSO)
  → INEC DPA 2022 microdatos → confirmar C9 parroquiales (Territorial v1.0 Sec. V)
  → PDOT atomizado → reemplazar metas de referencia por propuestas PDOT verificadas

Beta Multi-cantón:
  → Replicar QNKC-002 en segundo cantón de Manabí
  → Comparar ruptura causal entre cantones
  → Hub-and-Spoke: un mismo ACK (COOTAD_249) → múltiples cadenas territoriales
```

---

## REGLA DE ORO CAUSAL

> **QUIRA no produce rankings de desempeño. QUIRA produce explicaciones de causalidad institucional.**  
> Un C9 rojo sin nodo de ruptura identificado es una métrica. Con nodo de ruptura: es conocimiento accionable.  
> La diferencia entre una métrica y conocimiento accionable es el valor de QUIRA para el GAD.

---

## ADENDA v1.0.1 — 2026-05-31
*Cierre epistémico Alpha 0.9 — no modifica secciones anteriores*

---

### XIV. C10 — REFLEXIÓN INSTITUCIONAL

La cadena QNKC-002 tiene nueve capas: C1 (norma) → C9 (resultado territorial).  
C10 es la meta-capa que cierra el ciclo: **¿qué aprendió el modelo sobre sí mismo?**

```
C10 — Reflexión Institucional
  Trigger: hallazgo que revela una limitación del modelo (no del territorio)
  Input:   C9 confirmado + paradoja o anomalía metodológica documentada
  Output:  Nueva hipótesis sobre una variable no medida
           O nueva capa en la cadena causal existente
           O corrección de un supuesto previo
  Destino: Beta backlog (si requiere construcción)
           O corrección directa (si invalida dato Alpha anterior)
```

**Ejemplo fundante (2026-05-31):**

```
C9: Ti_Patronato_2025 = 50%  →  🔴 ROJO  (confirmado)
C10: "Ti no distingue ejecución programática de ejecución de personal.
      En servicios sociales intensivos en capital humano (diálisis, psicología,
      atención gerontológica), puede existir Ti financiero bajo con cobertura
      real alta. La cadena necesita una segunda capa: índices de impacto social."
↓
Resultado C10: nueva variable identificada → postergada a Beta.
Impacto en Alpha: ninguno. Ti_50% sigue siendo correcto en su capa (Piso 1).
```

**C10 NO invalida C1-C9.** Agrega profundidad, no corrección.  
Cuando C10 revela un error factual en datos anteriores → activar regla de escalamiento  
(Data Governance v1.0, Sección I — escalamiento irreversible).

**C10 y la Red Académica:**  
C10 es el punto de interfaz institucional entre QUIRA y la Red Académica (UEB/ESPAM/FLACSO/IAEN).  
Los hallazgos C10 son exactamente el tipo de preguntas que una alianza académica puede responder:  
- metodología de índices de impacto social
- validación de hipótesis causales H1-H8
- procesamiento de microdatos INEC DPA para C9 parroquiales  

Sin Red Académica, C10 produce preguntas sin respuesta.  
Con Red Académica, C10 produce mejoras metodológicas trazables que vuelven a C1-C9.

---

### XV. LOS TRES ESTADOS DE MADUREZ — TRAYECTORIA EPISTÉMICA

```
Alpha 0.8    QUIRA mide.
Alpha 0.9    QUIRA explica.
Alpha 1.0    QUIRA reconoce explícitamente lo que aún no puede explicar.
```

C10 no es funcionalidad de Beta. Es el mecanismo que permite declarar Alpha 1.0 sin fingir omnisciencia.  
Un sistema que mide sin explicar es un dashboard.  
Un sistema que explica sin reconocer sus límites es ideología.  
Un sistema que reconoce sus límites y los formaliza es infraestructura de conocimiento.

**La Red Académica (UEB/ESPAM/FLACSO/IAEN) no valida resultados — valida incertidumbres.**  
Lo que QUIRA lleva a la academia son los hallazgos C10: preguntas abiertas con estructura metodológica precisa.  
Lo que la academia devuelve es `estado_metodologico: validado_academico | refutado | requiere_investigacion`.  
Eso la convierte en co-investigadora del ciclo de aprendizaje, no en auditora de los datos.

---

### XVI. PRINCIPIO 6 — AUTOCURACIÓN METODOLÓGICA

> QUIRA no busca eliminar las limitaciones del modelo.  
> Busca identificarlas, registrarlas y convertirlas en mejoras trazables.  
> Todo hallazgo metodológico se convierte en una tarea futura del ecosistema.  
> Ningún hallazgo invalida el trabajo anterior si la evidencia original sigue siendo correcta.

**El ciclo:**

```
construir (C1-C9)
     ↓
observar (C9 en territorio real)
     ↓
detectar limitación (anomalía o paradoja)
     ↓
documentar (C10 — Reflexión Institucional)
     ↓
mejorar (Beta backlog → nueva construcción)
     ↓
construir (C1-C9 mejorado)
```

Este ciclo no termina. Esa es la respuesta correcta.  
Un sistema que ya no descubre sus propias limitaciones no está completo — está muerto.

**Señal de madurez Alpha:** QUIRA encontró su primera paradoja real (COOTAD_249) antes de llegar a Neo4j. Eso no indica desorden. Indica que la arquitectura ya es capaz de revelar contradicciones reales del territorio. Alpha funciona.

---

*QUIRA Causal Model v1.0 — CONGELADO 2026-05-31*  
*Versión siguiente: v1.1 tras primer ciclo de consultas causales Neo4j reales*  
*Custodio: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO*
