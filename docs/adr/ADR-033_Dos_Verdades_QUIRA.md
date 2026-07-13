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

## Regla nueva — PROVENIENCIA EXPLÍCITA
Toda respuesta de QUIRA **declara de qué capa proviene**:
- **Documental:** *"Según el PAC 2025 existe el proceso X."* → hecho reconstruido de la fuente.
- **Analítica:** *"El índice de cumplimiento de la gestión, calculado sobre los documentos oficiales, es 53.56%."*
  → conclusión matemática derivada de múltiples fuentes.

Ambas son verdad, pero de **capas epistemológicas diferentes**, y el usuario debe saber cuál está viendo.
**Bloomberg Firewall:** se muestra el **valor + etiqueta pública**; el código interno (ICPI/TGI/SAT) jamás.

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

## Consecuencia práctica (el trabajo que sigue)
Los DOM deben presentar **las dos mitades**: la trazabilidad documental (biografía) **Y** la evaluación
analítica (los índices, bajo etiqueta pública). Hasta hoy se construyó la documental; **incorporar los
índices al DOM es la otra mitad de QUIRA** — con proveniencia explícita (documental vs analítica).

---
*ADR-033 · Dos verdades de QUIRA · Dylus Lab © 2026 · "Los documentos contienen la evidencia; el Gold Master contiene el conocimiento. QUIRA dice qué ocurrió, y mide qué tan bien se gobernó."*
