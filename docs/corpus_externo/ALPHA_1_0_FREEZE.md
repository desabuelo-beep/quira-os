# ALPHA_1_0_FREEZE — Congelamiento Formal de Alpha 1.0
## Registro de Estado Verificable al Cierre de Fase

**Estado**: CONGELADO  
**Fecha de cierre**: 2026-05-31  
**Versión de congelamiento**: Alpha 1.0  
**Custodio**: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO

> Este documento sigue la práctica de congelamiento formal de Palantir:
> registra qué EXISTE verificablemente, qué fue EXCLUIDO deliberadamente,
> y qué significa Alpha 1.0 para el proyecto.
> No es un resumen. Es un contrato.

---

## I. DECLARACIÓN ALPHA 1.0

**Alpha 1.0 se declara completo a las [hora] del 2026-05-31.**

La consulta bautismal (ADR-010) fue ejecutada y respondida de forma
completa, trazable y reproducible. El grafo Neo4j demostró que puede
razonar sobre el territorio de Montecristi, no solo almacenar datos.

### Consulta Bautismal — Pregunta

```
¿Por qué Montecristi mantiene brechas en Dom12
si cumple formalmente COOTAD Art. 249?
```

### Respuesta Verificada — Paradoja Causal Confirmada

```
COOTAD_249 (Norma C1)
    ↓ [MATERIALIZA_VIA]
SP_G10P_MCR (C3 — Servicio Público Grupos Prioritarios Montecristi)
    ↓ [HABILITA]
RES_G10P_01_MCR (C9 — Asignación GAD: 20.84% codificado → VERDE)
    ↓ [HABILITA] ← pero NO garantiza ejecución
IND_G10P_04_MCR (C8 — Ti_Patronato: serie 35%→54%→50%)
    ↓ [EXPLICA] {g73_programas: 29.7%}
RES_G10P_04_MCR (C9 — Ti_Patronato_2025 = 50% → ROJO persistente año 3)

PARADOJA CAUSAL:
  El GAD cumple FORMALMENTE COOTAD_249 (2.08× el mínimo legal)
  PERO el Patronato ejecuta solo el 50% de su presupuesto de inversión.
  La norma se cumple en PAPEL pero no en TERRITORIO.
  El incumplimiento es de EJECUCIÓN INSTITUCIONAL (Patronato),
  no de ASIGNACIÓN FORMAL (GAD central).
  $2,048,280 sin ejecutar no llegaron a grupos prioritarios en 2025.
```

### Verificación de Condiciones ADR-010

```
✓ CONDICIÓN 1 — Los 3 QTMPs cargados en Neo4j
  ✓ GAP_10PCT: 1C3 + 6C4 + 7C5 + 5C6 + 4C7 + 5C8 + 5C9
  ✓ AGUA_POTABLE: 1C3 + 5C4 + 5C8 + 5C9
  ✓ EQUIDAD: 7 parroquias + 1C3 + 6C8 + 2C9 cantonal + 7C9 parroquial
  ✓ TOTAL: 79 nodos en el grafo

✓ CONDICIÓN 2 — La cadena causal aparece completa en el grafo
  ✓ Path verificado: 4 relaciones, 5 nodos
  ✓ Largo de cadena: COOTAD_249 → SP → RES_01 → IND_04 → RES_04

✓ CONDICIÓN 3 — La consulta es reproducible
  ✓ Script público: quira-os/scripts/neo4j_bautismal_query.py
  ✓ Cualquier observador externo puede replicar con: bolt://localhost:7687

✓ CONDICIÓN 4 — Cada nodo tiene fuente_documental o norma_base
  ✓ RES_G10P_04_MCR: Gold Master SIAP-ICPI v5.5_TGI — H07b_Ti_INVERSIÓN
  ✓ RES_AGPT_01_MCR: INEC Censo de Población y Vivienda 2022
  ✓ RES_AGPT_02_MCR: Dirección de Agua Potable GADMCM / PDOT Bicentenario
  ✓ RES_EQUD_01_MCR: SNP / INEC
  ✓ RES_EQUD_04_MCR: INEC Censo 2022 / PDOT Bicentenario págs. 316 y 375
```

---

## II. QUÉ EXISTE — VERIFICABLE

### Capa 1 — Gobernanza documental

| Artefacto | Ruta | Estado |
|---|---|---|
| ALPHA_0_9_FREEZE | `governance\ALPHA_0_9_FREEZE.md` | CONGELADO |
| ALPHA_1_0_FREEZE (este) | `governance\ALPHA_1_0_FREEZE.md` | CONGELADO |
| Data Governance v1.0 | `governance\QUIRA_DATA_GOVERNANCE_v1.0.md` | CONGELADO |
| Territorial Semantics v1.0 | `governance\QUIRA_TERRITORIAL_SEMANTICS_v1.0.md` | CONGELADO |
| Causal Model v1.0 + C10 + Adenda | `governance\QUIRA_CAUSAL_MODEL_v1.0.md` | CONGELADO |
| ADRs (10 decisiones) | `governance\decisions\ADR-001 a ADR-010` | CONGELADOS |
| QUIRA_STATE v1.2 | `governance\QUIRA_STATE.md` | ACTUALIZADO |
| Beta Backlog | `governance\QUIRA_BETA_BACKLOG.md` | VIVO |

### Capa 2 — Infraestructura grafo causal

| Componente | Valor | Estado |
|---|---|---|
| Neo4j DBMS | quira-alpha · v5.26.8 · bolt://localhost:7687 | ACTIVO |
| Nodos totales | 79 | CARGADOS |
| Nodos C9 confirmados | 5 | VERIFICADOS |
| Circuito GAP_10PCT | SP + 6C4 + 7C5 + 5C6 + 4C7 + 5C8 + 5C9 | CARGADO |
| Circuito AGUA_POTABLE | SP + 5C4 + 5C8 + 5C9 | CARGADO |
| Circuito EQUIDAD | 7 parroquias + SP + 6C8 + 9C9 | CARGADO |
| Corpus normativo | 6 ACK atoms (COOTAD_249, CE_12, CE_264, CE_274, COOTAD_228, CE_35) | CARGADO |

### Capa 3 — Scripts de carga y consulta

| Script | Ruta | Función |
|---|---|---|
| `neo4j_load_qtmp.py` | `quira-os\scripts\` | Carga idempotente de 3 QTMPs — MERGE |
| `neo4j_bautismal_query.py` | `quira-os\scripts\` | Consulta bautismal ADR-010 + declaración |

### Capa 4 — Datos confirmados en el grafo

| Nodo | Valor | Semáforo | Fuente |
|---|---|---|---|
| RES_G10P_01_MCR | 20.84% asignación | VERDE | SIGEF cédulas GAD + Patronato 2025 |
| RES_G10P_04_MCR | 50.0% Ti_Patronato | ROJO | Gold Master v5.5_TGI H07b |
| IND_G10P_04_MCR | Serie 35%→54%→50% | ROJO | Gold Master v5.5_TGI |
| RES_AGPT_01_MCR | 34.9% cobertura agua | ROJO | INEC Censo 2022 |
| RES_AGPT_02_MCR | 0% continuidad 24/7 | ROJO | PDOT Bicentenario 2023 |
| RES_EQUD_01_MCR | 79.7 IRS cantonal | AMARILLO | SNP / INEC |
| RES_EQUD_04_MCR | 32pp brecha NBI | ROJO | INEC Censo 2022 |

### Capa 5 — Gold Master (sin cambios desde Alpha 0.9)

| Artefacto | Valor | Estado |
|---|---|---|
| SIAP-ICPI v5.5_TGI | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | ACTIVO |
| H73 métricas | 58/63 = 92.1% | SPRINT SOBERANÍA COMPLETADO |
| Snapshot longitudinal #1 | ICPI=17.45%, TGI=66.79% | 2026-05-26 Supabase |

---

## III. QUÉ FUE EXCLUIDO DELIBERADAMENTE

| Exclusión | Razón | Registro |
|---|---|---|
| Cédula Patronato dic-2025 | Dato externo SIGEF pendiente — no bloquea Alpha | pendiente GADMCM |
| Integración UI/Streamlit con Neo4j | No es condición ADR-010 | Sprint 3 |
| Nuevos circuitos o dominios | 3 circuitos son suficientes para la consulta bautismal | Beta |
| Validación Red Académica H1-H8 | Hipótesis marcadas como `hipotesis` — pendiente FLACSO/IAEN | Beta |
| Piso 2 — índices impacto territorial | Piso 1 (Ti) es suficiente para Alpha | `BETA-DOM12-001` |
| PDOT atomizado (QLEP) | Sprint Beta dedicado | `BETA-DOM04-001` |

**Principio de exclusión**: Ningún ítem excluido invalida Alpha 1.0.
Son profundizaciones del grafo, no correcciones.

---

## IV. PARADOJA CAUSAL — HALLAZGO FUNDACIONAL ALPHA 1.0

```
HALLAZGO FUNDACIONAL — Alpha 1.0:

  La Ley dice: "asigna el 10% al Patronato" → GAD Montecristi asignó 20.84%
  La Institución hace: Patronato ejecuta solo el 50% de ese presupuesto
  El Territorio recibe: G73 programas = 29.7% (fracción que llega a servicios)
  El Resultado es: brecha Dom12 persistente, año 3 consecutivo en ROJO

  QUIRA formalizó lo que ningún sistema fiscal ecuatoriano captura:
  el cumplimiento legal no garantiza el impacto territorial.
  Esa brecha — entre el papel y el territorio — es exactamente lo que
  QUIRA existe para hacer visible y trazable.
```

Este hallazgo es reproducible, trazable y refutable. Es el primer resultado
científicamente honesto del sistema.

---

## V. CONTEXTO TERRITORIAL ALPHA 1.0

Los 3 circuitos revelan un patrón sistémico en Montecristi:

```
Dom12 — Protección Social:  Ti_Patronato = 50%  → ROJO (año 3)
Agua Potable:               Cobertura = 34.9%   → ROJO (40% sin acceso red)
Agua Potable:               Continuidad 24/7 = 0% → ROJO (ninguna zona continua)
Equidad Territorial:        IRS = 79.7           → AMARILLO
Equidad NBI brecha:         32pp urbano/rural    → ROJO
```

No son indicadores aislados. Son síntomas del mismo problema estructural:
recursos asignados que no se ejecutan, brechas que no se cierran,
territorio que no recibe lo que la ley manda.

---

## VI. CONDICIONES DE ENTRADA A BETA

Beta comienza cuando:

```
NO es condición para Beta iniciar:
  - Cédula Patronato dic-2025 (puede seguir pendiente)
  - Validación académica H1-H8

ES condición para Beta:
  ✓ Alpha 1.0 declarado (este documento)
  ✓ Al menos un artefacto Beta acordado formalmente con equipo
  ✓ Red Académica contactada (FLACSO o IAEN preferido)
```

---

## VII. DECLARACIÓN DE CIERRE

> Alpha 1.0 cierra habiendo demostrado lo que un grafo causal puede hacer
> que ningún Excel o dashboard puede: responder el *por qué*.
>
> COOTAD_249 cumplido en papel. Patronato en ROJO. Territorio sin servicio.
> La paradoja no era un error de datos — era un error de razonamiento institucional
> que ahora tiene nombre, cadena, fuente y número.
>
> Ese es el umbral que separa "colección de documentos" de
> "infraestructura de razonamiento territorial."
>
> QUIRA cruzó ese umbral hoy.

---

*ALPHA_1_0_FREEZE v1.0 — Congelado 2026-05-31*  
*Este documento no se modifica. Solo BETA FREEZE lo sucede.*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
