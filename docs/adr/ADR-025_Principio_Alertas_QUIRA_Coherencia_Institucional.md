---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-025 — Principio de Alertas QUIRA: Coherencia Institucional

**Estado**: RATIFICADO — 2026-06-05 · Consenso equipo Dylus Lab (Javo + Claude + Colega)
**Fecha**: 2026-06-05
**Proyecto**: QUIRA Gov · Dylus Lab
**Origen**: Debate SAT-0.1 → síntesis Colega → ratificación equipo

---

## El principio

> **QUIRA no alerta sobre actos administrativos legítimos.**
>
> **QUIRA alerta sobre rupturas verificables de coherencia entre compromisos públicos
> y las condiciones reales para cumplirlos.**

---

## Por qué existe este ADR

Durante la discusión de SAT-0.1 (HIP-001) emergió una pregunta más profunda:

> ¿Cuándo debe QUIRA generar una alerta?

La respuesta incorrecta: "cuando detecta un movimiento financiero significativo."

La respuesta correcta: "cuando detecta que un compromiso público ya no tiene las condiciones para cumplirse."

Esa distinción convierte QUIRA en infraestructura de inteligencia institucional —
no en un sistema de control financiero ni en una herramienta que castiga decisiones de gobierno.

---

## Los 5 ejes de coherencia que QUIRA observa

Todo SAT presente y futuro debe poder mapearse a la ruptura entre al menos dos de estos ejes:

```
1. PLANIFICACIÓN    PDOT · POA · PAC · metas estratégicas
       ↕
2. PRESUPUESTO      Codificado · Devengado · Pagado (eSIGEF)
       ↕
3. PARTICIPACIÓN    Compromisos PP · mecanismos LOPC · demandas territoriales
       ↕
4. RENDICIÓN        Declaraciones CPCCS · narrativa pública alcalde · informes
       ↕
5. EJECUCIÓN        Contratos SERCOP · obra física · indicadores de resultado
```

Una alerta QUIRA es la detección verificable de que dos o más de estos ejes
se han separado de manera significativa.

---

## La regla de validación para cualquier SAT nuevo

Antes de incorporar cualquier nueva alerta al sistema canónico (Sentinel o Gold Master),
debe responder afirmativamente a las tres preguntas siguientes:

**Pregunta 1 — ¿Es un acto administrativo legítimo o una ruptura de coherencia?**
- Si el evento es una decisión legal de gobierno (reforma presupuestaria, cambio de prioridad,
  reprogramación) → NO es alerta por sí solo.
- Si el evento genera una distancia verificable entre un compromiso público y las condiciones
  reales → SÍ puede ser alerta.

**Pregunta 2 — ¿Se puede verificar documentalmente?**
- La ruptura debe poder trazarse con fuentes verificables: eSIGEF, SERCOP, LOTAIP, actas PP,
  informes CPCCS, texto de RDC.
- Sin evidencia documental → hipótesis de investigación, no alerta canónica.

**Pregunta 3 — ¿Tiene base normativa?**
- La coherencia esperada debe estar fundamentada en una norma (COOTAD, COPFP, CRE, LOPC, LOSNCP).
- Sin norma → la expectativa no es institucional, es interpretativa.

---

## Cómo aplica por dominio

| Dominio | Coherencia que observa QUIRA |
|---|---|
| D01 Plan de Gobierno | PDOT aprobado ↔ ejecución real de metas |
| D02 Cooperación | Fondos comprometidos ↔ condiciones de desembolso cumplidas |
| D03 Ejecución Anual | POA aprobado ↔ codificado disponible ↔ devengado real |
| D04 Señales | Cualquier ruptura de los 5 ejes en tiempo real |
| D05 Holding | Presupuesto entidad ↔ ejecución ↔ servicio prestado |
| D06 Estado GAD | Compromisos globales ↔ indicadores ICPI/TGI resultantes |
| D07 Transparencia | Obligación LOTAIP ↔ publicación verificada |
| D08 Participación | Compromiso PP/LOPC ↔ incorporación en planificación/presupuesto |
| D09 Rendición | Narrativa declarada RDC ↔ ejecución verificada → Fricción Narrativa |
| D10 Territorio | Inversión planificada por parroquia ↔ cobertura real de servicios |
| D12 Protección Social | Obligación CRE Art. 35 ↔ inversión ejecutada |

---

## Los tres tipos de ruptura (tipología canónica)

### Tipo 1 — Ruptura de planificación
Lo aprobado en el plan no tiene recursos o ejecución.
Ejemplo: meta PDOT sin codificado en POA.

### Tipo 2 — Ruptura de participación
Lo decidido con la ciudadanía no se refleja en la asignación presupuestaria.
Ejemplo: obra votada en PP eliminada por reforma presupuestaria.

### Tipo 3 — Fricción Narrativa
Lo declarado públicamente no coincide con la ejecución verificable.
Ejemplo: alcalde declara "construimos 5 km de vías rurales" → eSIGEF muestra $0 devengado.
*(Concepto originado en TERRA Ciudadana v2.1)*

---

## Lo que NO es una alerta QUIRA

- Una reforma presupuestaria del Concejo (acto legal de gobierno)
- Una reprogramación de metas justificada por emergencia
- Un cambio de prioridad aprobado en sesión ordinaria
- Un desvío de gasto corriente dentro de los límites normativos

Estos eventos son DATOS de contexto que QUIRA registra.
Solo se convierten en señal si generan una ruptura verificable de coherencia.

---

## Implicancia para el Gold Master

Este principio gobierna el crecimiento del Excel canónico:

- **Antes de ADR-025**: nuevas variables entraban orgánicamente cuando surgía una necesidad.
- **Desde ADR-025**: toda nueva variable del Gold Master debe poder mapearse a una ruptura
  de coherencia entre los 5 ejes. Si no puede, es hipótesis de investigación (carpeta `docs/hipotesis/`).

Esto aplica retroactivamente a la evaluación de HIP-001 (SAT-0.1).

---

## Relación con otros ADRs

- **ADR-023** (3 niveles de cálculo): este ADR no modifica los niveles. Define qué MERECE ser calculado.
- **ADR-024** (Radar Nacional): la coherencia institucional es lo que QUIRA observa en los 221 GAD.
- **HIP-001** (SAT-0.1): primera hipótesis evaluada bajo este principio.

---

*ADR-025 · QUIRA Gov · Dylus Lab © 2026*
*Principio rector del sistema de alertas — inmutable hasta nueva decisión formal de equipo*
