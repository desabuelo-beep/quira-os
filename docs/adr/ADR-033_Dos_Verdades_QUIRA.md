---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-033 · Las dos verdades de QUIRA — Motor de Evidencia + Motor de Evaluación

**Estado:** RATIFICADO · 2026-07-13 (Javo + colega + director técnico)
**Contexto de origen:** cierre de la fase documental. Javo precisa: *"la trazabilidad es superpotente, pero
es solo la mitad de QUIRA; el Excel tiene también el análisis y los resultados de la gestión — ahí también
hay verdad."* El colega lo formaliza como **dos motores epistemológicos**.
**Relacionado:** ADR-023 (Gold Master = motor de cálculo) · ADR-029 §Precisión (la verdad documental vive
en la fuente) · ADR-031 (5 motores tipados · Matemático) · ADR-032 (Motor de Biografía) · Constitución CAPA 0.

---

## Contexto

Toda la fase reciente construyó **trazabilidad** (la biografía documental: promesa → POA → PAC → contrato).
Pero el Excel Canónico contiene **~11 índices principales + secundarios** (ICPI, IPE, IEF, SAT-0/II/III/IV…)
que son la **razón de ser** del Excel: miden el **desempeño real** de la gestión, no solo su trazabilidad.
Esos índices son **también verdad** — no documental, sino **analítica**.

## Decisión — QUIRA integra DOS dimensiones de verdad

### I · Verdad documental (Motor de Evidencia)
Responde **"¿qué ocurrió realmente?"**. Reconstruye desde las fuentes (PDOT·POA·PAC·SERCOP·SIGAD·Presupuesto·
Rendición). Producto: **trazabilidad**. Es forense: no interpreta, reconstruye. **Vive en las FUENTES** (ADR-029 §Precisión).

### II · Verdad analítica (Motor de Evaluación)
Responde **"¿qué tan bien gobernó la institución?"**. **Calcula · integra · normaliza · compara** sobre esa
misma evidencia. Producto: un **índice**. No inventa datos ni interpreta políticamente: son **funciones
matemáticas reproducibles sobre documentos oficiales**. **Vive en el Gold Master** (los algoritmos, no los documentos).

> Los documentos contienen la **evidencia**. El Gold Master contiene el **conocimiento**. No es un repositorio: es un laboratorio.

**Precisión (colega · 2026-07-13) — el índice NO es un hecho nuevo:** el ICPI no "existe" en el documento del
GAD — es una **inferencia cuantitativa reproducible**. Existe porque se definió un **algoritmo transparente**
sobre documentos oficiales; su **legitimidad es la reproducibilidad** (cualquiera repite el cálculo y obtiene
lo mismo), no la primacía. El Gold Master **no crea realidad administrativa**: integra, normaliza, compara,
calcula, sintetiza. Con máxima precisión: los documentos contienen la **evidencia primaria**; el Gold Master,
la **representación canónica + los resultados analíticos derivados**. *(Por eso "verdad analítica" es un atajo:
rigurosamente es una inferencia reproducible, no un hecho.)*

### III · Interpretación — la TERCERA capa epistemológica (Javo + colega · corregido)
Responde **"¿qué significa esto?"**: lenguaje explicativo, comparaciones, narrativa. **Estatus epistemológico
MENOR:** una interpretación **NO tiene el mismo peso** que un documento (evidencia) ni que un índice (inferencia);
se declara como tal (anti-alucinación · Principio Rector).

**⚠️ Precisión de Javo (2026-07-13) — la interpretación NO es QUIRA IA (el colega las fundió):**
- La **interpretación CURADA** vive en la **capa DOM** (L2 dashboards): ahí se evidencia y explica todo —gráfica,
  analítica, conceptualmente— en **lenguaje de administración pública** (sin exponer lo canónico), y **queda definido**.
  Es parte del producto entregado.
- **QUIRA IA es OTRA capa — la CONVERSACIONAL** (arquitectónica · aún por construir): el usuario **conversa** sobre
  todo lo que hay en QUIRA, **anclado a evidencia + índices, sin alucinar**. No "es la interpretación": es el **acceso
  conversacional** a las tres capas. *(Igual: **GeoTwin → GEO IA** es otra capa por construir.)*

> **Tres capas EPISTEMOLÓGICAS (autoridad decreciente): evidencia > inferencia analítica > interpretación.**
> NO confundir con las capas ARQUITECTÓNICAS (ADR-023 Motor·SO·UI · UI: L1 Mando · L2 DOM · L3 GeoTwin→GEO IA ·
> **+ QUIRA IA conversacional** · aún por construir). Son **ejes ortogonales**: *qué autoridad tiene una afirmación*
> ≠ *en qué capa del sistema vive*.

**Nomenclatura (Javo · Regla 7 anti-inflación):** lo que QUIRA administra NO se llama "cadena de confianza"
(propuesta del colega, rechazada). El término canónico —ya en la Constitución CAPA 0— es **cadena de integridad
intersistémica**. El nivel de confianza por proveniencia es una **dimensión** de esa cadena, no un concepto nuevo.

### Reconciliación con ADR-029 §Precisión — NO hay contradicción
- La verdad **documental** NO vive en el Gold Master (vive en la fuente) → ADR-029, correcto.
- La verdad **analítica** SÍ vive en el Gold Master (los índices) → ADR-033, se completa.

Son **dos capas epistemológicas distintas**. El Gold Master **integra** la evidencia documental (capa de
integración) **y produce** la verdad analítica (capa de evaluación). La corrección anterior seguía siendo
correcta — solo hablaba de la mitad documental.

### El rol del Gold Master: **Motor Analítico Canónico**
El Gold Master **no "apoya"** la trazabilidad — **constituye la capa analítica de QUIRA**. Sin él, QUIRA es
un excelente sistema de auditoría documental. Con él, es **además** un sistema de **evaluación objetiva del
desempeño gubernamental**. *(Se conserva el nombre "Gold Master" como artefacto — Regla 7, anti-churn;
"Motor Analítico Canónico" es su ROL epistemológico, no un renombre.)*

## Regla — PROVENIENCIA EXPLÍCITA (3 tipos · colega 2026-07-13)
Toda afirmación de QUIRA se clasifica **automáticamente** en una de tres, con autoridad decreciente:

| Tipo | Procedencia | Ejemplo |
|---|---|---|
| **Evidencia** | documento oficial | *"El PAC registra 109 procesos."* |
| **Resultado analítico** | Gold Master | *"El índice de congruencia es 53,56%."* |
| **Interpretación** | DOM (curada) / QUIRA IA (conversacional) | *"La planificación muestra alta coherencia, pero ejecución desigual."* |

El usuario debe saber siempre cuál ve — un **hecho reconstruido**, una **inferencia matemática**, o una
**explicación de la IA**. **Bloomberg Firewall:** valor + etiqueta pública; el código interno (ICPI/TGI/SAT) jamás.
Además, la analítica **hereda la confianza de la evidencia** sobre la que se calcula (capa dependiente · ver ADR-032:
ejec. per-meta *thin* ⇒ índice per-meta limitado; a nivel de dominio, firme).

## Por qué es ciencia — el ejemplo del IPE
Al corregir el IPE **no se cambió la realidad ni un documento — se cambió un CÁLCULO**. La evidencia siguió
igual; la verdad analítica **mejoró**. Eso es exactamente lo que debe hacer un índice científico: perfeccionar
la medición sin tocar el hecho.

## Arquitectura (actualizada)
```
FUENTES OFICIALES → Motor de Evidencia → verdad DOCUMENTAL
                                              │
                                              ▼
                                        Gold Master → Motor de Evaluación → verdad ANALÍTICA
                                                                                  │
                          Neo4j (consume AMBAS verdades) ◄────────────────────────┘
                                              │
                                              ▼
                                          QUIRA IA
```

## Definición oficial de QUIRA (nueva)
> **QUIRA es un sistema de inteligencia pública que integra dos formas complementarias de verdad: la verdad
> documental, reconstruida desde las fuentes oficiales (qué ocurrió), y la verdad analítica, obtenida mediante
> indicadores matemáticos reproducibles calculados sobre esa misma evidencia (qué tan bien gobernó la
> institución).** La primera explica qué ocurrió; la segunda mide qué tan bien se gobernó. La combinación
> distingue a QUIRA de un repositorio documental o de un tablero de indicadores aislado.

**Formulación canónica (colega · resiste revisión académica/tesis):**
> **QUIRA no sustituye la verdad documental por una verdad analítica; transforma evidencia oficial en
> conocimiento reproducible mediante reglas explícitas, preservando siempre la trazabilidad entre ambos niveles.**

## Consecuencia práctica (el trabajo que sigue)
Los DOM deben presentar **las dos mitades**: la trazabilidad documental (biografía) **Y** la evaluación
analítica (los índices, bajo etiqueta pública). Hasta hoy se construyó la documental; **incorporar los
índices al DOM es la otra mitad de QUIRA** — con proveniencia explícita (documental vs analítica).

## Corolario de presentación — PRIMACÍA NARRATIVA (Javo + colega · 2026-07-13)
Las tres capas **no se mezclan visualmente**. El DOM es un **espacio narrativo de conocimiento**, no un
tablero: primero **explica** (documental) → **interpreta** (analítica) → **comunica** una conclusión
(interpretación). La **evidencia** —tablas, tableros, gráficos, documentos, el detalle de las metas— es
**desplegable BAJO DEMANDA** (patrón normativa ya en el cajón: `<details>` · *clic → se abre*), **nunca el
protagonista**. Regla: *el usuario primero comprende, después verifica; ninguna tabla reemplaza el relato del
dominio.* NO es un renombre (Regla 7): es el **corolario de UI** de las tres capas — y lo que separa a QUIRA de
un Power BI. Reencuadra el trabajo de cada DOM: la pregunta deja de ser *"¿qué hoja del Excel falta mostrar?"*
y pasa a ser *"¿qué idea falta explicar?"* — con la evidencia detrás de un *"Ver …"*. *(Principio en maduración;
se cita como corolario de ADR-033, no abre ADR nuevo.)*

---
*ADR-033 · Dos verdades de QUIRA · Dylus Lab © 2026 · "Los documentos contienen la evidencia; el Gold Master contiene el conocimiento. QUIRA dice qué ocurrió, y mide qué tan bien se gobernó."*
