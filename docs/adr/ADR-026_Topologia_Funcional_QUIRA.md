# ADR-026 — Topología Funcional de QUIRA

**Versión:** 1.0
**Fecha:** 2026-06-08
**Estado:** RATIFICADO — consenso equipo Dylus Lab (Javo + Claude + Colega)
**Origen:** Fase 0 · Arqueología funcional · 6 excavaciones de dominio (D04, D06, D07, D08, D09, D10)
**Autores:** Dylus Lab · Colega asesor · Claude Director Técnico
**Relacionado:** ADR-017 (Circuitos Constitucionales) · ADR-023 (3 Niveles) · ADR-024 (Radar Nacional) · ADR-025 (Principio Alertas)

---

## El problema que resuelve

QUIRA tiene 12 dominios constitucionales visibles en la UI (`_DOMAINS_12` en `p_command_center.py`). Durante el diseño de Sprint B surgió la pregunta:

> ¿Cómo convertir 12 cajones en 12 puertas navegables?

La pregunta era incorrecta. Asumía que los 12 dominios son arquitectónicamente equivalentes — que cada uno tiene el mismo tipo de dato, la misma relación con los demás, y que una "puerta" se diseña igual para todos.

Las excavaciones demostraron que eso es falso.

Los 12 dominios son equivalentes como **responsabilidades constitucionales** (taxonomía correcta para la UI). No son equivalentes como **unidades funcionales** (taxonomía necesaria para la arquitectura).

Sin este ADR, Sprint B construiría 12 puertas idénticas para 12 tipos de dominio distintos — algunas serían monitores en tiempo real, otras checklists anuales, otras síntesis de síntesis. El resultado sería arquitectónicamente incoherente aunque visualmente uniforme.

---

## Origen de la evidencia

Este ADR no es un documento de diseño. Es un documento de descubrimiento.

Entre las 19:00 y las 21:00 del 8 de junio de 2026, se realizaron excavaciones arqueológicas sobre 6 dominios del codebase de QUIRA OS. Se leyó el código fuente completo de cada dominio y se respondieron 6 preguntas sistemáticas por excavación:

1. ¿Qué problema resuelve?
2. ¿Qué métricas genera?
3. ¿Cuál es la narrativa pública?
4. ¿Cómo sobrevive?
5. ¿Cuándo muere?
6. ¿Qué es la "puerta"?

Dominios excavados: **D04, D06, D07, D08, D09, D10**.

Los hallazgos de cada excavación están registrados en el historial de sesión 2026-06-08 (contexto vivo, no duplicado aquí).

---

## Los dos planos de QUIRA

QUIRA opera simultáneamente en dos taxonomías que coexisten sin conflicto:

```
PLANO UI — Taxonomía constitucional pública
────────────────────────────────────────────────────────────────
12 puertas · 12 competencias municipales · 12 artículos CE/COOTAD
Audiencia: alcalde, director, ciudadano
Pregunta: ¿el municipio cumple su función constitucional X?
Diseñada para: navegación, narrativa, comunicación pública

PLANO FUNCIONAL — Taxonomía epistemológica interna
────────────────────────────────────────────────────────────────
3 tipos funcionales · N circuitos constitucionales · 1 puerta de protocolo
Audiencia: arquitecto, desarrollador, analista
Pregunta: ¿qué rol cumple este dominio en la cadena causal del sistema?
Diseñada para: construcción, debugging, diseño de circuitos
```

Ninguno reemplaza al otro. Son dos vistas del mismo sistema.

Este ADR formaliza el **Plano Funcional** descubierto en el código.

---

## Taxonomía Funcional — 3 Tipos

### Tipo A — Generadores

Dominios que **producen evidencia propia** sobre el cumplimiento de una función constitucional. Tienen fuentes de datos primarias externas al sistema QUIRA (INEC, Gold Master, Neo4j QTMP, documentos físicos), operan en tiempo real o casi-real, y pueden existir independientemente de otros dominios.

**Dominios confirmados:** D04 · D07 · D08 · D10
**Dominios probables:** D02 · D03 · D12 *(pendiente excavación)*

Características comunes:
- Conectan a fuentes externas verificables (SIGEF, INEC, CPCCS, SERCOP, Gold Master)
- Sus métricas son observables por ciudadanos sin credenciales del sistema
- Un fallo en ellos puede propagarse hacia otros dominios
- Cada uno implementa o puede implementar `get_qtmp_chain()` o `load_all()` con fuentes primarias

**Sub-tipos identificados dentro de Tipo A:**

| Sub-tipo | Dominio | Descripción |
|---|---|---|
| Motor autónomo | D04 | Genera señales de alerta propias · 3 capas · SLA temporal |
| Sensor constitucional | D10 | Lee fuente primaria única (QTMP AGUA_POTABLE + Gold Master) · no propaga |
| Nodo origen causal | D07 | Es ORIGEN del Circuito C01 · colapsa circuito si falla · dimensión temporal C5t |
| Nodo de unión | D08 | Mayor conectividad del sistema · C01 INTER · IGP→D06 · D08→D09 · verificador ICM/ICPI |

---

### Tipo B — Sintetizador

Dominio que **no produce evidencia propia**. Interpreta y sintetiza señales generadas por los Tipo A. No puede existir sin sus dominios fuente.

**Único dominio confirmado:** D06

Características:
- Lee explícitamente de otros dominios (vectores: IGP de D08, IOC de D07, IET de D10, ISP de D04/D02, PSG de D19)
- Sus 6 vectores causales son exactamente los outputs de los Generadores
- Si todos sus fuentes están en verde, D06 está en verde. No tiene datos propios que verificar.
- Es la cara pública del ICPI — pero el ICPI lo calcula el Gold Master, no D06

```
D07 → IOC (-3.1)  ┐
D08 → IGP (-4.1)  │
D10 → IET (-2.8)  ├──► D06 (ICPI síntesis)
D02 → ISP (-8.2)  │
D02 → IED (-6.8)  │
D19 → PSG (-2.4)  ┘
```

D06 no es el producto de QUIRA. Es la **consecuencia** del correcto funcionamiento de los Generadores.

---

### Tipo C — Puerta de Protocolo

Dominio que **no produce ni sintetiza evidencia**. Agrega el estado de todos los demás dominios para validarlos ante un árbitro externo en un ciclo temporal específico.

**Único dominio confirmado:** D09

Características:
- Su checklist de 20 ítems referencia exclusivamente métricas de otros dominios (D07, D08, D02, D03, D04, D10, D19)
- No genera ningún indicador propio — produce `pct_ok` (composite de otros)
- Escala temporal: **anual** (a diferencia de los Tipo A que son tiempo real)
- Su resultado final (V=0 o V≥70) lo determina el CPCCS como árbitro externo, no el sistema
- Sus CTAs apuntan hacia atrás (a D08 y D07), no hacia adelante — es un terminal

```
D07 (Transparencia)  ──┐
D08 (Participación)  ──┤
D02/D03 (Fiscal)     ──┼──► D09 (Checklist RDC) ──► CPCCS (V=0 / V≥70)
D04 (Planificación)  ──┤
D10 (Territorio)     ──┤
D19 (Género)         ──┘
```

**D09 no es un dominio entre iguales. Es el protocolo de cierre anual del sistema.**

---

### Tipo D — Corpus Fundacional

Dominios que **no producen métricas operacionales ni sintetizan indicadores**. Proveen el marco normativo y territorial dentro del cual todos los demás tipos adquieren significado. Viven principalmente en **Supabase C1 Corpus** como embeddings vectorizados con sus relaciones causales, y alimentan el sistema desde la capa de conocimiento.

**Dominios confirmados:** D01 (Marco Legal) · D05 (PDOT)
*Confirmación: Javo Fundador, sesión 2026-06-08*

Características:
- Vectorizados en Supabase C1 con relaciones causales explícitas (no son indicadores — son contexto semántico)
- No aparecen como vectores en D06 (no contribuyen al ICPI — contribuyen a su interpretación)
- Alimentan a los Generadores como referencias normativas y de meta: `meta_pdot_2027` (D10), `METAS_PDOT` (D08), checklist PDOT (D09)
- El PDOT fue cargado específicamente para territorializar en GeoTwin (Layer 3)
- El Marco Legal establece las relaciones causales entre artículos constitucionales que el ACK Registry implementa

```
CAPA 0 — CORPUS FUNDACIONAL (Supabase C1 · vectorizado)
  D01 Marco Legal  → relaciones causales ACK Registry · contexto normativo
  D05 PDOT         → metas territoriales (→ D08, D09, D10) · GeoTwin (→ p4_geotwin.py)

       ↓  alimenta como referencia  ↓

CAPA 1 — GENERADORES Tipo A  (D04 D07 D08 D10 D02 D03 D12)
CAPA 2 — SINTETIZADOR Tipo B  (D06)
CAPA 3 — PROTOCOLO Tipo C    (D09)
```

**Por qué D01 y D05 no son Generadores:** un Generador produce evidencia verificable sobre el cumplimiento de una función constitucional hoy. El Marco Legal y el PDOT no se "cumplen" en tiempo real — definen el contrato que los Generadores deben demostrar que se está cumpliendo. Son la referencia, no la medición.

**Por qué D01 y D05 no están en los vectores de D06:** D06 sintetiza el estado operacional del sistema. D01/D05 son el estándar contra el que ese estado se mide. Incluirlos como vectores equivaldría a incluir la constitución como variable dentro de un indicador de cumplimiento constitucional.

---

## Hallazgos no anticipados por el diseño original

Las excavaciones revelaron tres hallazgos que no estaban formalizados antes de este ADR.

### Hallazgo 1 — La brecha ICM/ICPI es la propuesta de valor central

En `p16_gobernanza.py` (D08) está codificado el dato más importante de QUIRA:

```python
BRECHA_HISTORICA = [
    {"año": "2023", "icm": 100.0, "icpi": 57.36},
    {"año": "2024", "icm": 100.0, "icpi": 67.12},
    {"año": "2025", "icm": 100.0, "icpi": 69.93},
]
```

Tres años consecutivos: el municipio reporta 100% de cumplimiento al SIGAD. QUIRA verifica entre 57% y 70%. La brecha promedio es de 30 puntos.

Este dato no es una anomalía técnica. Es la demostración empírica del valor de QUIRA: la distancia entre lo que una institución declara y lo que la evidencia verifica. Vive en D08, el dominio de Participación Ciudadana — el único actor externo que puede confirmar o contradecir el autoreporte institucional.

**Regla canónica derivada:** La propuesta de valor de QUIRA no es producir mejores indicadores. Es hacer visible la brecha entre el autoreporte y la evidencia verificable. Sin esa brecha, QUIRA es un dashboard más.

### Hallazgo 2 — La fórmula C8 es filosofía institucional, no matemática

D07 implementa en `p07_transparencia.py`:

```
C8 = C4 × (C5a × C5b_acc × C5t × C5c)
```

La fórmula es **multiplicativa**. Un cero en cualquier dimensión colapsa el resultado a cero. En particular: si C5t = 0 (publicó fuera del plazo legal), C8 = 0 independientemente de que publicó todo.

*"La transparencia tardía no es transparencia oportuna."*

Esto no es una elección técnica — es una **tesis de gobernanza**: la oportunidad forma parte constitutiva del derecho a la información. No un atributo deseable sino un requisito definitorio. Esta lógica multiplicativa distingue a QUIRA de cualquier sistema que promedia indicadores.

**Regla canónica derivada:** Las fórmulas de QUIRA deben ser multiplicativas donde la oportunidad o la integridad sean condición necesaria, no acumulativas donde la excelencia en una dimensión puede compensar el fallo en otra.

### Hallazgo 3 — Deuda arquitectónica activa en D07

`p07_transparencia.py` (canónico, Sprint 4, QTMP circuit) y `p15_transparencia.py` (legacy, Sprint 1, `load_all()`) coexisten en el codebase. El router `env_gov.py` apunta a `p07_transparencia.py`. `p15_transparencia.py` es código muerto activo — existe, se importa, podría activarse accidentalmente, y sus Bloomberg violations (ITAM, IOC como códigos públicos) son un riesgo latente.

**Acción requerida:** Deprecar formalmente `p15_transparencia.py` antes de Sprint B. No eliminar — mover a `governance/historico/` o marcarlo con `# DEPRECATED — ver p07_transparencia.py`.

---

## Circuitos funcionales confirmados

Este ADR confirma dos circuitos en el código (uno ya formalizado en ADR-017, uno nuevo):

### C01 — Confirmado en código (ADR-017 diseñó, excavación verificó)

```
D07 (ORIGEN · CE Art.18) ──► D08 (INTER · CE Art.95) ──► D04 (DEST · CE Art.264.1)
```

**Estado ADR-017:** CONGELADO v1.0
**Estado en código:** Implementado en `p07_transparencia.py` via `_C01_NODES` y `_calcular_chs_c01()`
**Regla de colapso:** Dom07 ORIGEN falla → CHS_C01 = 0.0 (implementada y activa)

### C-RDC — Circuito de Rendición Anual (nuevo, emergente)

```
D07 + D08 + D02/D03 + D04 + D10 + D19
              ↓
            D09 (protocolo de convergencia)
              ↓
           CPCCS (árbitro externo)
              ↓
         V=0 / V≥70 (resultado)
```

Este circuito es cualitativamente diferente de C01:
- Escala temporal: anual (no tiempo real)
- Árbitro: externo (CPCCS, no el sistema)
- Dirección: convergente (todos apuntan a D09, nadie recibe de D09)
- Activación: estacional (Mayo-Septiembre, no por degradación de nodo)

**Estado:** Implementado en `p17_rdc.py` · No formalizado en ADR previo · **Formalizado aquí por primera vez**

**Spec formal C-RDC:**

```yaml
circuit_id: C-RDC
nombre_corto: "Convergencia Anual — Rendición de Cuentas"
descripcion: >
  Circuito de validación externa anual. Todos los dominios Tipo A deben
  alcanzar sus umbrales para que el municipio pueda presentar una RDC
  válida ante el CPCCS. D09 es el punto de convergencia — no genera
  datos sino que verifica su completitud.
escala_temporal: ANUAL
arbitro_externo: CPCCS
activacion: Estacional · Mayo (preparación) → Agosto (ejecución) → Septiembre (calificación)

nodos_convergentes:
  - Dom07 · umbral: IOC < 10% · 21 arts LOTAIP completos · Art.7r publicado
  - Dom08 · umbral: 7/7 asambleas · actas digitalizadas · PP rendido por parroquia
  - Dom02/Dom03 · umbral: ISP regularizado ≥ 25% · ejecución Q2 documentada
  - Dom04 · umbral: 4 metas SAT-0 regularizadas · avance PDOT con indicadores
  - Dom10 · umbral: informe cobertura agua actualizado
  - Dom19 · umbral: PSG ≥ 20% documentado

nodo_protocolo: Dom09
  tipo: CONVERGENCIA (no ORIGEN ni INTERMEDIARIO ni DESTINO)
  output: checklist pct_ok + evidencias → CPCCS
  resultado_externo: V=0 (no validado) / V≥70 (validado)

diferencia_con_C01:
  C01: causal (un dominio causa el fallo del siguiente)
  C-RDC: convergente (todos deben funcionar para que el protocolo pase)
```

---

## Implicaciones para la secuencia de construcción

La conclusión más importante de este ADR, consensuada entre Javo (fundador), Claude (director técnico) y Colega (asesor), es:

> **QUIRA Operaciones debe completarse antes de QUIRA Institucional.**

Sin los Generadores funcionando (Tipo A), el Sintetizador (Tipo B) produce números sin evidencia. Sin evidencia, la capa Institucional (puertas, narrativa, experiencia alcalde) es presentación sin sustancia.

```
SECUENCIA INCORRECTA (anterior):
Sprint B → Institucional (puertas)
Sprint C → Operaciones (motores)

SECUENCIA CORRECTA (post-ADR-026):
FASE 1 → QUIRA Operaciones
         · Completar Generadores (D02, D03, D12 pendientes de excavación)
         · Cerrar Bloomberg Firewall en todos los dominios
         · Formalizar C-RDC en Neo4j
         · Completar C02 y C03 (ADR-017 specs parciales)
         ↓
         ADR-026 CERRADO + Bloomberg Firewall CERRADO
         ↓
FASE 2 → QUIRA Institucional
         · Sprint B: 12 puertas diseñadas con taxonomía funcional correcta
         · Cada puerta tiene diseño específico a su Tipo (A/B/C)
         · Narrativa pública basada en evidencia real de los Generadores
```

### Diseño de puertas por Tipo Funcional

Una vez completada FASE 1, las puertas de Sprint B deben diseñarse así:

| Tipo | Dominio | Tipo de puerta | Actualización |
|---|---|---|---|
| A — Motor | D04 | Monitor de señales activas + lifecycle | Tiempo real |
| A — Sensor | D10 | KPI constitucional + barra de progreso PDOT | Semestral / datos vivos |
| A — Origen causal | D07 | Semáforo C8 + dualidad C4/C5 + estado C01 | Mensual (publicación LOTAIP) |
| A — Nodo unión | D08 | 6 mecanismos + parroquias + ICM/ICPI gap | Trimestral + RDC |
| B — Sintetizador | D06 | Score ICPI + 6 vectores causales + histórico | Trimestral (Gold Master) |
| C — Protocolo | D09 | Checklist preparación RDC + timeline estacional | Anual (Mayo-Sep) |

---

## Pendientes para cerrar la taxonomía

Los siguientes dominios no fueron excavados en esta sesión. Son necesarios para confirmar si existen Generadores adicionales y si hay sub-tipos nuevos:

| Dominio | Hipótesis pre-excavación | Prioridad |
|---|---|---|
| D02 — Presupuesto Municipal | Generador fiscal (ISP, IED → D06) | Alta |
| D03 — Contratación Pública | Generador contractual (LOSNCP, SERCOP → D06) | Alta |
| D12 — Inclusión Social | Sensor social (probable Tipo A) | Media |
| D01 — Marco Legal | **✅ RESUELTO** — Tipo D Corpus Fundacional · vectorizado Supabase C1 · ACK Registry | N/A |
| D05 — PDOT | **✅ RESUELTO** — Tipo D Corpus Fundacional · vectorizado Supabase C1 · feeds GeoTwin + D08/D09/D10 | N/A |
| D11 — (DESHABILITADO) | `disabled: True` en command center — no excavar | N/A |

---

## Relación con ADRs previos

| ADR | Relación con ADR-026 |
|---|---|
| ADR-016 (DCO) | Define el dominio constitucional como unidad. ADR-026 clasifica cada DCO en uno de 3 tipos funcionales. |
| ADR-017 (Circuitos) | Diseñó C01, C02, C03 desde la teoría. ADR-026 confirma C01 en código y formaliza C-RDC como circuito nuevo descubierto en arqueología. |
| ADR-022 (Principio Divergencia A-D) | Principio de separación datos/presentación. ADR-026 añade: los datos A son Generadores, los datos D son síntesis del Sintetizador. |
| ADR-023 (3 Niveles) | Los 3 niveles son Motor/SO/UI. ADR-026 opera en el nivel SO — describe cómo los dominios se relacionan entre sí dentro de QUIRA. |
| ADR-024 (Radar Nacional) | QUIRA como radar de 221 GADs. ADR-026 describe la arquitectura interna que hace posible ese radar: Generadores → Sintetizador → Protocolo. |
| ADR-025 (Principio Alertas) | Las alertas detectan rupturas de coherencia. ADR-026 especifica: las rupturas ocurren cuando un Generador falla o cuando la brecha ICM/ICPI supera umbrales. |

---

## Regla canónica derivada de este ADR

> **Antes de diseñar la puerta de un dominio, identifica su Tipo Funcional.**
>
> Una puerta Tipo A es un monitor (¿qué evidencia existe hoy?).
> Una puerta Tipo B es un diagnóstico (¿qué dice la síntesis de la evidencia?).
> Una puerta Tipo C es un preparador (¿qué falta para que el protocolo pase?).
> Un dominio Tipo D no tiene puerta operacional — tiene entrada de corpus (Supabase ingest).
>
> Diseñar una puerta Tipo C como si fuera Tipo A produce un checklist que parece un monitor.
> Diseñar una puerta Tipo B como si fuera Tipo A produce un dashboard que pretende generar datos que no tiene.
> Intentar construir una puerta operacional para un Tipo D produce una pantalla que muestra un PDF — porque el PDOT y el Marco Legal no son indicadores, son el estándar.

---

## Estado

| Componente | Estado |
|---|---|
| Taxonomía 4 tipos | ✅ RATIFICADA — 3 tipos por excavación + Tipo D por confirmación Javo Fundador 2026-06-08 |
| C01 confirmado en código | ✅ CONFIRMADO — `p07_transparencia.py` líneas 82-113, 118-139 |
| C-RDC formalizado | ✅ NUEVO — spec completa en este ADR |
| ICM/ICPI como propuesta de valor | ✅ CONFIRMADO — `p16_gobernanza.py` líneas 100-104 |
| Fórmula C8 como innovación epistemológica | ✅ CONFIRMADO — `p07_transparencia.py` líneas 506-566 |
| Excavaciones D02, D03, D12 pendientes | ⏳ PENDIENTE — necesarias para cerrar taxonomía |
| Deprecación `p15_transparencia.py` | ⏳ PENDIENTE — acción pre-Sprint B |
| Bloomberg Firewall completo (todos dominios) | ⏳ PENDIENTE — acción pre-Sprint B |
| Diseño de puertas por Tipo Funcional | ⏳ PENDIENTE — Sprint B FASE 2 |

---

*ADR-026 v1.1 · QUIRA Gov · Dylus Lab © 2026*
*v1.0 → v1.1: Tipo D Corpus Fundacional añadido (D01 Marco Legal + D05 PDOT) — confirmación Javo Fundador 2026-06-08*
*Siguiente: Excavaciones D02 + D03 + D12 → cierre taxonomía Tipo A → Bloomberg Firewall → Sprint B FASE 2*
