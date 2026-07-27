---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2]
  type: NORMATIVA
---

# PCD-D02 · Presupuesto & Financiamiento (QINV-002)

**Estado:** CERRADO · 2026-07-16 · Javo + director técnico · aportes del colega
**Dominio:** la **capacidad financiera territorial** — la aptitud del cantón para captar, mover
y ejecutar recursos a tiempo, y para apalancar capital externo sin caer en subejecución.
**Visión (corrección de Javo · 2026-07-14):** no es "el presupuesto interno". Es la **salud
financiera como base para captar financiamiento internacional** (reembolsable y no reembolsable).
**Relacionado:** ADR-032 (objeto canónico compartido) · ADR-033 (proveniencia · dos verdades) ·
ADR-035 (BRN) · ADR-036 (universo operacional) · PCD-D01 · PCD-D03.

---

## Estado inicial

El dominio no existía. El Gold Master tenía la evidencia dispersa —salud presupuestaria,
ejecución eSIGEF, fondos externos, vinculación ODS— sin un expediente que la explicara ni una
tesis que la ordenara. La primera propuesta del director fue "presupuesto y ejecución interna":
**Javo la corrigió** — el dominio existe para responder si el municipio es **elegible y capaz de
absorber cooperación internacional**.

## Hallazgos (auditoría de las 7 capas)

| # | Hallazgo | Origen |
|---|---|---|
| 1 | **El índice de salud presupuestaria se leía de la columna equivocada**: el enricher tomaba el valor de ejecución (3.2%) en lugar del índice real (**58.4%**). Un error de columna que habría publicado una cifra falsa | director |
| 2 | **Fuga de firewall**: la línea de fuentes exponía siglas internas del motor hacia el público | director |
| 3 | **La visión estaba mal planteada**: se enfocaba en ejecución interna, no en capacidad de captación internacional | **Javo** |
| 4 | **El dominio nacía sin marco jurídico visible**, a diferencia de d01 | **Javo** |
| 5 | **Gráficas cortadas a media anchura**: los nodos eran de tamaño fijo y se agrupaban a la izquierda | **Javo** |
| 6 | **El código de meta no comunicaba**: `SC-I-N-01` sin decir qué es | **Javo** |
| 7 | **La tarjeta anunciaba `$3.66M`**, cifra que no cuadraba con los **$1.87M** realmente captados | director |

## Cambios y construcción

**Roster del canon (verificado contra el Excel antes de construir):** salud presupuestaria ·
ejecución (cédula eSIGEF) · fondos externos · vinculación ODS · alineación al Plan Nacional
(**consumida de d01**, no recalculada · ADR-032). Se descartó H16_IFE (es de d03) y H20b (es de
d08 · Participación).

**Las 4 capacidades** (marco propio del dominio): **Elegibilidad** (83% PND · 87.5% ODS) ·
**Movilización** ($1.87M en 4 convenios, todos no reembolsables) · **Absorción** (6.4% al corte
de abril) · **Sostenibilidad** (58.4%, bajo el 65% que fija el COOTAD Art. 192).

**La biografía del capital público** — la cadena causal por convenio: `ODS → Plan Nacional →
Meta del PDOT → Convenio → Capital → Contrato → Devengado → Resultado`, con el **estado de cada
eslabón** (✓ validado · ! en proceso · ✗ sin dato). **El último nodo va en rojo**: el municipio
no publica medición de resultados. *La ausencia se ve en el nodo; no se explica ni se rellena.*

**El salto predictivo (SAT · decisión de Javo 2026-07-15):** se elimina el DOM Alertas y cada
señal vive en su dominio. d02 toma las **3 financieras**, **leídas del motor** (Regla 1), cada
una contra su umbral legal:

| Señal | Norma | Estado |
|---|---|---|
| Reforma presupuestaria tardía | COPFP Art. 115 | ● sin señal |
| Parálisis presupuestaria | COPFP Art. 113 | ● sin señal |
| Alerta fiscal · estructura COOTAD | COOTAD Art. 192 | ● sin señal |

**3 vigiladas · 0 activas** — el presupuesto no dispara alertas, y eso *es* un dato.

**La cadena Norma → Regla → Indicador → Señal** (germen de la BRN · ADR-035): cada señal muestra
de qué **regla legal** nació. No inventamos las alertas: **las deriva la ley.**

## Aportes del colega (veredicto del director)

| Propuesta | Decisión |
|---|---|
| d02 es un *brief*, no un expediente: le falta **densidad de evidencia, no narrativa** | ✅ **Correcto** — motivó la v2 |
| Cronología forense · perfil del financiamiento · panel de riesgo | ✅ Tomados (el dato los sostenía) |
| **Afinidad proyectada BID/CAF/JICA** ("muy compatible", "alta afinidad") | ❌ **Rechazado** — inventar dato sin base (Regla 3). Qué fondo aplica lo resuelve **QUIRA Cooperación** (producto · ADR-024), no este cajón |
| Impacto inferido | ❌ Rechazado — la ausencia se declara, no se rellena |
| Escenarios de simulación (25%→45%→65%) | ❌ Rechazado — sería motor de cálculo paralelo (Regla 4) |
| Elasticidad hipotética "¿y si llegan $5M?" | ⚠️ Sustituida por el **SAT-III canónico** (dato real, no proyección) — a instancia de Javo |

## Validación

- **Firewall:** limpio en todas las verificaciones (sin ICPI·TGI·Ti·H-codes·siglas del motor).
- **Regla 1:** ningún índice se recalcula — todos se **leen** del Gold Master.
- **Regla 4:** las transiciones aguas abajo se **referencian** a su dominio; no se duplican.
- **Cifras contrastadas contra el snapshot:** $1.87M · 6.4% · 58.4% — la tarjeta corregida.

## Estado final

**Capacidad financiera territorial documentada** · 4 capacidades · perfil del financiamiento
(origen · sector · modalidad) · biografía del capital con 8 eslabones · **3 señales preventivas
con su norma** · cadena inter-dominio (d02 como eslabón, no isla) · marco legal desplegable ·
color propio (violeta) · **entrable y en línea**.

**Abierto:** el **resultado/impacto territorial no tiene medición publicada** (ausencia declarada
— es el hallazgo, no la deuda) · el registro no distingue aún **capital propio vs transferencia
vs cooperación** con el detalle que permitiría medir autonomía real.

---
*PCD-D02 · Dylus Lab © 2026 · "El dominio no pregunta cuánto gastó el municipio: pregunta si puede recibir el dinero del mundo y convertirlo en obra. Y responde con la cadena completa —del ODS al dólar— dejando en rojo el eslabón que nadie mide."*
