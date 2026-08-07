---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-026 — Topología Funcional de QUIRA

**Versión:** 1.2
**Fecha:** 2026-06-08 (v1.0) → 2026-06-09 (v1.2)
**Estado:** MODELO OPERATIVO — taxonomía cerrada · Fase 0 Arqueología Funcional completada
**Origen:** Fase 0 · Arqueología funcional · 9 excavaciones de dominio (D02, D03, D04, D06, D07, D08, D09, D10, D12)
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

Dominios excavados: **D02, D03, D04, D06, D07, D08, D09, D10, D12** (9/12 dominios constitucionales).
Dominios no operacionales (no excavar): D11 (`disabled: True` en command center).
Dominios Tipo D verificados: D01 (Marco Legal), D05 (PDOT) — confirmados por Javo Fundador, no son módulos operacionales sino corpus vectorizado.

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

**Dominios confirmados (7 de 7):** D02 · D03 · D04 · D07 · D08 · D10 · D12
*(taxonomía Tipo A cerrada — Fase 0 completa)*

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
| Capa de consecuencia financiera | D02 | Convierte outputs de otros Tipo A en elegibilidad de fondos · arquitectura: snapshot dinámico vía skill (ver corrección post-excavación abajo) |
| Puente PDOT-Operaciones | D03 | Dos capas independientes: CNE (IFE-A 72.73% · 48/66 promesas) + PDOT (IFE-E pendiente Q2-2026 · trazabilidad POA→PAC→eSIGEF) · sin ruta sidebar |
| Generador con membresía dual A+D | D12 | PSG = output Tipo A (Gold Master H73) · PDOT género = input Tipo D · 4/6 IGM incompletos |

**Nota sobre D12 — primer caso de membresía dual:** un dominio puede tener outputs operacionales (Tipo A) alimentados por marcos normativos (Tipo D). La dirección del flujo determina el tipo funcional; la presencia de norma no lo contradice. El PDOT de género es referencia (Tipo D); PSG es medición (Tipo A). Esta coexistencia es arquitectónicamente válida y esperada en dominios de inclusión social.

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

### Tipo D — Corpus Fundacional Verificable

Dominios que **no producen métricas operacionales ni sintetizan indicadores**. Definen qué significa "cumplir" — son el estándar de referencia contra el cual los Generadores observan y el Sintetizador interpreta. Viven principalmente en **Supabase C1 Corpus** como embeddings vectorizados con sus relaciones causales, y alimentan el sistema desde la capa de conocimiento.

**La diferencia con un repositorio documental:** un PDF archivado no es Tipo D. Tipo D tiene **comportamiento computable** — sus contenidos alimentan decisiones en tiempo de ejecución. Por ejemplo: `PDOT → meta_pdot_2027 → D10` ya es comportamiento computable, no solo referencia. La palabra clave es **Verificable**: el corpus puede ser consultado, citado y usado para validar afirmaciones operacionales del sistema.

*Precisión conceptual: Colega asesor, sesión 2026-06-08.*

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

## Visión sinóptica — La cadena completa

*Formulación del Colega asesor, confirmada tras las 9 excavaciones. Esta tabla es la síntesis más precisa de QUIRA en una sola vista.*

| Capa funcional | Tipo | Dominios | Función |
|---|---|---|---|
| NORMA | D | D01 · D05 | Definen qué significa "cumplir" |
| OBSERVACIÓN | A | D02 · D03 · D04 · D07 · D08 · D10 · D12 | Observan la realidad contra la norma |
| INTERPRETACIÓN | B | D06 | Interpretan la realidad en su conjunto |
| VALIDACIÓN | C | D09 | La someten a validación externa (CPCCS) |
| CONSECUENCIA | A² | D02 | Traducen el estado institucional en dinero disponible / bloqueado |

*Nota D02: doble naturaleza confirmada en código — Observación (genera datos de elegibilidad) y Consecuencia (traduce estado institucional en consecuencia financiera cuantificada). No rompe la taxonomía — agrega una dimensión. Documentado como: `Generador con función de consecuencia financiera`. Aporte: Colega asesor, 2026-06-09.*

> Esta estructura evita el error clásico de GovTech: `Norma = Indicador`. El PDOT no es un indicador. La Constitución no es un indicador. LOTAIP no es un indicador. Son marcos de referencia. Por eso Tipo D existe como categoría separada — y por eso QUIRA puede afirmar que "verifica" y no solo que "mide".

---

## Hallazgos no anticipados por el diseño original

Las excavaciones revelaron seis hallazgos que no estaban formalizados antes de este ADR.

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

### Hallazgo 4 — D02 como capa de consecuencia financiera *(con corrección de implementación)*

**⚠️ CORRECCIÓN POST-EXCAVACIÓN (2026-06-09 · Javo Fundador):**
El portfolio hardcodeado de `p18_cooperacion.py` (6 fondos con thresholds fijos: BID Gender Bond, BDE, CAF, etc.) no tiene base sustancial en el Gold Master. Fue construido en una etapa temprana sin fundamento verificado. **El concepto de "bonds" queda retirado.**

**Arquitectura correcta de D02:**

```
INTELIGENCIA DE FINANCIAMIENTO DINÁMICO
──────────────────────────────────────────────────────────────────────
Eje 1: Tipo de financiamiento
   · Reembolsable   → crédito/préstamo (BDE, CAF crédito, banca multilateral)
   · No reembolsable → cooperación/donación (GEF, PNUD, ONU Mujeres, fondos climáticos)

Eje 2: Tipo de entidad elegible
   · GAD · ONG · OSC · Academia · Startup
   · Coaliciones: GAD+ONG · GAD+Academia · Multisectorial · todas las combinaciones

Eje 3: Condición de elegibilidad
   · Derivada de indicadores reales de dominios Tipo A (PSG, ISP, ITAM, ICPI rango, etc.)
   · ELEGIBLE / CONDICIONADO / BLOQUEADO / REQUIERE-COALICIÓN

Skill de actualización: `/fondos-radar` (~15 días)
   → mapea fuentes de fondos disponibles (BID, CAF, GEF, PNUD, MAATE, BDE, etc.)
   → evalúa elegibilidad GAD contra snapshot de indicadores
   → genera JSON estructurado → D02 renderiza desde snapshot
   → NUNCA hardcoded — siempre desde el último snapshot con timestamp
```

Este rediseño hace D02 más robusto porque:
1. Elimina Bloomberg violations actuales (ISP/PSG/ITAM como códigos hardcodeados en UI)
2. Escala a los 222 GADs del Radar Nacional (cada uno con su snapshot de elegibilidad)
3. Cubre el ecosistema completo de financiamiento (no solo 6 fondos encontrados en un momento)
4. La dimensión de coaliciones — GAD puede no calificar solo pero sí con una ONG aliada

La cuantificación del costo de incoherencia sigue siendo válida y poderosa:
> "PSG 12.83% no es abstractamente crítico — es un monto bloqueado de financiamiento cuantificable."
El método de cálculo cambia (dinámico vía skill) pero el insight arquitectónico permanece.

### Hallazgo 4a — D02 como capa de consecuencia financiera (insight permanente)

`p18_cooperacion.py` convierte estados de dominio en consecuencia económica cuantificada. Cada fondo tiene umbrales cruzados sobre outputs de otros Tipo A:

```
D12 PSG = 12.83% < 30% → BID Gender Bond BLOQUEADO ($95K) + ONU Mujeres BLOQUEADO ($65K)
D10 ISP = 14.58% < 65% → BDE Crédito Reactivación BLOQUEADO ($3.5M)
D07 ITAM = 56% < 65% → CAF Ciudades Sostenibles EN GESTIÓN ($1.2M)
──────────────────────────────────────────────────────────────────
Total bloqueado verificado: $3.66M — exactamente el datum del command center
```

Esta es la primera demostración empírica del COSTO DE LA INCOHERENCIA INSTITUCIONAL en QUIRA: un dominio "en rojo" no es abstractamente malo. Es $3.66M sin poder moverse.

**Regla canónica derivada:** D02 debe mostrar las "llaves maestras" — las 2-3 acciones mínimas que desbloquean el mayor volumen financiero. No es un portafolio de oportunidades. Es un diagnóstico de elegibilidad con prescripción accionable.

### Hallazgo 5 — D03 como puente formal PDOT→Operaciones

`p8_metas.py` implementa el contrato de rendición de cuentas: cada METAS_PDOT mapea una obligación del Plan de Desarrollo (Tipo D) a su medición actual (Tipo A). 10 metas al cierre de la excavación:

```
M-06: PSG 12.83% → 30% · fuente: D12 · estado: CRÍTICO · bloquea: Gender Bond $95K
M-07: IET $40/hab → $80/hab · fuente: D10 · estado: CRÍTICO
M-08: ITAM 56% → 75% · fuente: D07 · estado: NORMAL
M-05: UT activas 50 → 75 · fuente: D08 · estado: ALERTA
M-01: Agua 34.9% → 65% · fuente: D10 · estado: CRÍTICO
M-10: IFE-A 72.73% → 100% · ÚNICO EN D03 · trazabilidad promesas electorales
```

D03 tiene `mod=None` en el command center — existe como página (`p8_metas.py`) sin ruta de sidebar. Esto es deuda activa: el contrato de rendición de cuentas más importante del sistema no tiene acceso público directo.

**Regla canónica derivada:** IFE-A (Índice de Fidelidad Electoral) es un indicador sin par en el sistema — mide cuántas promesas del alcalde tienen respaldo en metas PDOT formales. 72.73% al cierre de excavación, 18 promesas sin respaldo. Debe preservarse y no mezclarse con indicadores de ejecución.

### Hallazgo 6 — D12 confirma membresía dual, revela brecha en Gold Master

D12 genera PSG = 12.83% (Tipo A, vivo en H73_OUTPUT_API) pero sus 4/6 sub-indicadores IGM tienen `valor=None`:

```python
IGM-A: Mujeres en cargos directivos   → valor=None (pendiente certificación RRHH)
IGM-B: Brecha salarial                → valor=None (pendiente nómina DAF)
IGM-C: Carga acarreo agua rurales     → valor=None (pendiente encuesta PNUD/INEC)
IGM-F: Representación política CNE    → valor=None (pendiente datos CNE/AME)
```

El patrón `valor=None` está documentado como diseño deliberado: "Indicadores sin fuente Excel marcados con valor=None → Sin dato oficial". No es un bug. Es un contrato: QUIRA no inventa datos. Pero sí revela que D12 es el dominio con mayor brecha entre lo que el sistema debería medir y lo que el Gold Master actualmente cubre.

**Regla canónica derivada:** antes de Sprint B, D12 debe tener un roadmap explícito de qué fuentes externas (RRHH, DAF, CNE/AME, PNUD/INEC) se necesitan para cubrir IGM-A, B, C y F. Sin eso, D12 muestra una puerta con luz prendida pero sin datos detrás.

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
| A — Consecuencia financiera | D02 | Portafolio elegibilidad + llaves maestras + $X bloqueado | Continuo (por dominio fuente) |
| A — Puente PDOT | D03 | Dashboard metas M-01→M-10 + IFE-A + brechas | Trimestral + Gold Master |
| A — Dual A+D | D12 | PSG semáforo + IGM panel (con gaps explícitos) + Ambiente FA | Trimestral + Gold Master |
| B — Sintetizador | D06 | Score ICPI + 6 vectores causales + histórico | Trimestral (Gold Master) |
| C — Protocolo | D09 | Checklist preparación RDC + timeline estacional | Anual (Mayo-Sep) |
| D — Corpus | D01 · D05 | No puerta operacional — entrada Supabase C1 corpus | N/A |

---

## Cierre de taxonomía — todos los dominios clasificados

Fase 0 completa. Los 12 dominios constitucionales están clasificados:

| Dominio | Tipo | Evidencia | Estado |
|---|---|---|---|
| D01 — Marco Legal | D | Vectorizado Supabase C1 · ACK Registry · relaciones causales | ✅ RESUELTO |
| D02 — Cooperación | A | `p18_cooperacion.py` · $3.66M bloqueado · umbral PSG/ISP/ITAM | ✅ CONFIRMADO |
| D03 — Metas PDOT | A | `p8_metas.py` · M-01→M-10 · IFE-A 72.73% · mod=None | ✅ CONFIRMADO |
| D04 — SAT/Alertas | A | `p9_sat.py` · `p_alertas.py` · 3 capas · SLA temporal | ✅ CONFIRMADO |
| D05 — PDOT | D | Vectorizado Supabase C1 · meta_pdot_2027 computable · GeoTwin | ✅ RESUELTO |
| D06 — Estado GAD | B | `p6_pulso.py` · `p7_brecha.py` · 6 vectores causales | ✅ CONFIRMADO |
| D07 — Transparencia | A | `p07_transparencia.py` · C8 · QTMP TRANSPARENCIA · ORIGEN C01 | ✅ CONFIRMADO |
| D08 — Participación | A | `p16_confianza.py` · `p16_gobernanza.py` · IGP · 6 mecanismos | ✅ CONFIRMADO |
| D09 — Rendición | C | `p17_rdc.py` · 20-item checklist · 4 fases · CPCCS árbitro | ✅ CONFIRMADO |
| D10 — Territorio | A | `p10_territorio.py` · QTMP AGUA_POTABLE · IET · GeoTwin | ✅ CONFIRMADO |
| D11 — (DESHABILITADO) | — | `disabled: True` en command center | NO EXCAVAR |
| D12 — Género/Ambiente | A+D | `p19_genero.py` · PSG H73 (A) · PDOT género/FA (D) · IGM 4/6 None | ✅ CONFIRMADO |

---

## Relación con ADRs previos

| ADR | Relación con ADR-026 |
|---|---|
| ADR-016 (DCO) | Define el dominio constitucional como unidad. ADR-026 clasifica cada DCO en uno de 3 tipos funcionales. |
| ADR-017 (Circuitos) | Diseñó C01, C02, C03 desde la teoría. ADR-026 confirma C01 en código y formaliza C-RDC como circuito nuevo descubierto en arqueología. |
| ADR-022 (Principio Divergencia A-D) | Principio de separación datos/presentación. ADR-026 añade: los datos A son Generadores, los datos D son síntesis del Sintetizador. |
| ADR-023 (3 Niveles) | Los 3 niveles son Motor/SO/UI. ADR-026 opera en el nivel SO — describe cómo los dominios se relacionan entre sí dentro de QUIRA. |
| ADR-024 (Radar Nacional) | QUIRA como radar de 222 GADs. ADR-026 describe la arquitectura interna que hace posible ese radar: Generadores → Sintetizador → Protocolo. |
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
| Taxonomía 4 tipos | ✅ CERRADA — 9 excavaciones · D02/D03/D12 confirman · D11 deshabilitado |
| Tipo A — 7 generadores clasificados | ✅ COMPLETO — D02 D03 D04 D07 D08 D10 D12 |
| Tipo B — Sintetizador | ✅ ÚNICO — D06 |
| Tipo C — Protocolo | ✅ ÚNICO — D09 |
| Tipo D — Corpus Fundacional Verificable | ✅ DOS — D01 D05 · confirmado Javo Fundador |
| Membresía dual A+D documentada | ✅ PRIMER CASO — D12 (PSG output + PDOT género input) |
| C01 confirmado en código | ✅ CONFIRMADO — `p07_transparencia.py` líneas 82-113, 118-139 |
| C-RDC formalizado | ✅ NUEVO — spec completa en este ADR |
| ICM/ICPI como propuesta de valor | ✅ CONFIRMADO — `p16_gobernanza.py` líneas 100-104 |
| Fórmula C8 como innovación epistemológica | ✅ CONFIRMADO — `p07_transparencia.py` líneas 506-566 |
| D02 corrección arquitectónica | ✅ CORREGIDO — portfolio hardcodeado retirado · nuevo concepto: inteligencia dinámica financiamiento + skill `/fondos-radar` · entidades: GAD/ONG/OSC/Academia/Startup/coaliciones |
| D03 puente PDOT-Operaciones | ✅ NUEVO HALLAZGO — IFE-A único · mod=None (deuda activa) |
| Visión sinóptica Norma→Obs→Interp→Valid | ✅ FORMALIZADA — tabla 4 capas · aporte Colega asesor |
| Deprecación `p15_transparencia.py` | ⏳ PENDIENTE — acción pre-Sprint B |
| Bloomberg Firewall completo (todos dominios) | ⏳ PENDIENTE — acción pre-Sprint B |
| D03 routing (mod=None) | ⏳ PENDIENTE — p8_metas.py sin entrada sidebar |
| D12 roadmap datos faltantes (IGM-A,B,C,F) | ⏳ PENDIENTE — fuentes RRHH/DAF/CNE/PNUD |
| Diseño de puertas por Tipo Funcional | ⏳ PENDIENTE — Sprint B FASE 2 (post-Operaciones) |

---

*ADR-026 v1.2 · QUIRA Gov · Dylus Lab © 2026*
*v1.0 → v1.1: Tipo D Corpus Fundacional añadido (D01 Marco Legal + D05 PDOT) — confirmación Javo Fundador 2026-06-08*
*v1.1 → v1.2: Taxonomía cerrada · D02 D03 D12 confirmados como Tipo A · D12 membresía dual documentada · Visión sinóptica 4 capas formalizada · Estado: MODELO OPERATIVO — 2026-06-09*
*Siguiente: Bloomberg Firewall → p15 deprecación → D03 routing → D12 datos faltantes → Sprint B FASE 2*
