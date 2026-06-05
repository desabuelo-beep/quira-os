---
name: "Motor QUIRA — Arquitectura Lógica y Epistemología"
description: "Nota madre de la Capa MOTOR. Define la arquitectura lógica del SIAP Engine (CAPA 3 de la ontología QUIRA): sus silos epistémicos, su lógica de integración, su naturaleza dialéctica entre lo físico institucional y lo digital aplicativo. No expone implementación — expone comprensión."
tipo: motor-arquitectura
capa: "CAPA 3 — SIAP Engine"
version: "SIAP-ICPI_GOLD_MASTER_v5.4"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
fecha: "2026-05-17"
tags: [motor, arquitectura, silos, dialectica, epistemologia, quira, tgi, core, siap-engine, capa3]
---

# Motor QUIRA — Arquitectura Lógica *(CAPA 3 — SIAP Engine)*

> El SIAP Engine no es una hoja de cálculo. Es el **motor cuantitativo propietario** que implementa el TGI Framework: toma la realidad bruta de un municipio ecuatoriano —sus leyes, su planificación, su dinero, su geografía, su capacidad— y la convierte en scores verificables. Esta capa documenta su lógica, no su implementación.

→ [[QUIRA_OS_Ontologia]] — visión sistémica completa (CAPA 0 → CAPA 5)

---

## Posición en la Ontología QUIRA

```
CAPA 0 — Dylus Lab          (IP / ownership)
CAPA 1 — QUIRA OS           (ecosistema)
CAPA 2 — TGI Framework      (metodología D1–D5)
CAPA 3 — SIAP Engine  ◄──── (este nodo) motor propietario
CAPA 4 — Knowledge Layer    (Obsidian KB)
CAPA 5 — Action Layer       (Sentinel · PMV)
```

**Distinción crítica:** El SIAP Engine EJECUTA el TGI Framework. No lo define. La metodología existe independientemente de la implementación — puede ser auditada académicamente, presentada a cooperación internacional, y publicada como framework sin revelar el motor.

---

## La Pregunta Fundacional

El Motor existe para responder una sola pregunta — definida por Dylus Lab en el TGI Framework:

> **¿Está este municipio gobernando bien su territorio, con equidad, con legalidad y con eficiencia, en relación a lo que se comprometió y a lo que la ley le exige?**

El TGI Score es la respuesta cuantificada. Las 5 dimensiones son las cinco formas de mirar esa misma pregunta.

---

## Los Cinco Silos Epistémicos

El Motor organiza el conocimiento municipal en cinco silos. Cada silo representa una dimensión de la gobernanza — no una hoja de cálculo, sino una **pregunta sobre la realidad territorial**:

| Silo | Dimensión | La pregunta que responde |
|------|-----------|------------------------|
| **S1 · Normatividad** | D1 — Legalidad | ¿Está el GAD actuando dentro del marco legal que le corresponde? |
| **S2 · Planificación** | D2 — Fidelidad | ¿Lo que programó para este año es coherente con lo que prometió? |
| **S3 · Ejecución Fiscal** | D3 — Presupuesto | ¿Está convirtiendo recursos en obra real a ritmo suficiente? |
| **S4 · Territorio** | D4 — Equidad | ¿La inversión llega donde más se necesita, o se concentra? |
| **S5 · Institucionalidad** | D5 — Capacidad | ¿Tiene la institución la fortaleza para sostener lo anterior? |

→ Desarrollo completo en [[MOTOR_01_Silos_Epistemicos]]

---

## La Lógica de Integración — TGI 5D

Los cinco silos no son independientes. El Motor los integra en una sola síntesis ponderada:

```
TGI = S1×0.20 + S2×0.20 + S3×0.25 + S4×0.25 + S5×0.10
```

La ponderación no es arbitraria:
- **S3 y S4 (25% cada uno)** — tienen el mayor peso porque capturan los dos problemas crónicos de la gobernanza municipal ecuatoriana: sub-ejecución presupuestaria y regresividad territorial
- **S1 y S2 (20% cada uno)** — la legalidad y la planificación son condición necesaria pero no suficiente
- **S5 (10%)** — la capacidad institucional es el piso mínimo; sin ella los otros cuatro silos colapsan

→ [[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]]

---

## El Ciclo Dialéctico — Física e Digital

El Motor es dialéctico porque no es estático. Existe en un ciclo continuo:

```
MUNDO FÍSICO                    MUNDO DIGITAL
(instituciones, territorio)     (motor, datos, algoritmos)

    Realidad bruta          →       INGESTA (Fuentes)
    (eSIGEF, SIGAD,                 ↓
     SERCOP, INEC, CNE,        PROCESAMIENTO (Motor)
     PDOT, POA, RdC)               ↓
                             OUTPUTS (TGI, alertas)
    Decisiones              ←       ↓
    (priorización,           INTELIGENCIA (QUIRA Gov)
     contratación,               ↓
     rendición de cuentas)  RETORNO al territorio
```

El Motor va al territorio (lee sus datos), ve la realidad (la transforma en scores), y se recrea en él (produce inteligencia que regresa como acción institucional).

→ Desarrollo completo en [[MOTOR_03_Dialectica]]

---

## Las Fuentes — De Dónde Viene el Conocimiento

Cada silo tiene fuentes institucionales específicas — organismos del Estado que producen los datos que el Motor consume:

| Silo | Fuentes principales |
|------|-------------------|
| S1 Normatividad | Registro Oficial, CPCCS, CGE |
| S2 Planificación | SIGAD (SNP/SETEPLAN), POA institucional, CNE |
| S3 Ejecución | eSIGEF (Ministerio Finanzas), SERCOP, PAC |
| S4 Territorio | INEC (Censo, NBI), SIGAD inversiones, PDyOT |
| S5 Institucionalidad | SNP (ICM), CPCCS (RdC), GAD (estructura orgánica) |

→ Desarrollo completo en [[MOTOR_02_Fuentes_Institucionales]]

---

## La Manifestación — Outputs del Motor hacia las Capas Superiores

El SIAP Engine produce outputs verificables que las capas superiores consumen. No los define — los alimenta:

| Output del Motor | Capa que lo consume | Forma de consumo |
|-----------------|--------------------|--------------------|
| TGI=66.85, D1-D5 scores | CAPA 4 — Obsidian | Interpretación contextual |
| Alertas D3=59.85%, IRS=79.7 | CAPA 4 — Obsidian | Nodos Sentinel activos |
| TGI + drill-down parroquial | CAPA 1 — QUIRA Gov (Dashboard) | Visualización ejecutiva |
| Señales accionables | CAPA 5 — Sentinel / PMV | Decisiones institucionales |
| Score de gobernanza | CAPA 1 — QUIRA Funds/Audit | Elegibilidad y trazabilidad |

**La cadena de valor del Motor:**
```
SIAP Engine calcula   →  Knowledge Layer interpreta  →  Action Layer actúa
(outputs numéricos)      (contexto + trazabilidad)       (decisiones + alertas)
```

→ Desarrollo completo en [[MOTOR_04_Ecosistema_Digital]] · [[QUIRA_OS_Ontologia]]

---

## Cadena Canónica de esta Capa

```
[[MOTOR_00_Arquitectura_Logica]]  ←  (este nodo) visión sistémica
    ↓
[[MOTOR_01_Silos_Epistemicos]]    ←  qué pregunta responde cada silo
    ↓
[[MOTOR_02_Fuentes_Institucionales]] ← de dónde vienen los datos
    ↓
[[MOTOR_03_Dialectica]]            ←  el ciclo físico ↔ digital
    ↓
[[MOTOR_04_Ecosistema_Digital]]    ←  hacia dónde escala
```

Todos conectan hacia: [[03_SIAP_ICPI_METHOD]] (metodología) · [[01_TGI_FRAMEWORK]] (framework) · [[02_TGI_DIMENSIONES]] (outputs actuales)

---

*Motor QUIRA · Arquitectura Lógica · SIAP-ICPI_GOLD_MASTER_v5.4 · Dylus Lab © 2026*
