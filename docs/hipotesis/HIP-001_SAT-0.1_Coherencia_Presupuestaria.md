# HIP-001 — Hipótesis de Variable Causal: SAT-0.1 Coherencia Presupuestaria

**Estado**: HIPÓTESIS — pendiente validación. NO incorporar al Excel canónico hasta aprobar filtro.
**Fecha**: 2026-06-05
**Origen**: Terra Ciudadana v2.1 → refinamiento jurídico Colega (2026-06-05)
**Destino si aprueba**: Gold Master v6.0 (NO modificar v5.5 activo)

---

## Principio fundacional

Una reforma presupuestaria aprobada por el Concejo Municipal **NO constituye alerta**
por sí sola. Es una facultad legítima de gobierno (COOTAD · régimen financiero municipal).

**Lo que sí genera señal**: la ruptura de coherencia entre un compromiso público
verificable y los recursos disponibles para cumplirlo.

> Las alertas de QUIRA no son alarmas financieras.
> Son señales de coherencia entre compromisos públicos y su ejecución.

---

## Definición propuesta

```
SAT-0.1 — Señal de Coherencia Institucional (preventiva)

CONDICIÓN (requiere AMBAS):
  A. Variación significativa Presupuesto Inicial → Codificado (umbral a definir)
  B. La variación afecta al menos una de:
       [ ] Meta estratégica del PDOT activo
       [ ] Compromiso aprobado en Presupuesto Participativo
       [ ] Ítem declarado en Rendición de Cuentas (CPCCS)
       [ ] Obligación con base normativa verificada (COOTAD/COPFP/CRE)

RESULTADO: Señal de coherencia preventiva
TIPO: informacional/preventiva (no sancionatoria)
LENGUAJE PÚBLICO: "Variación presupuestaria que afecta compromiso institucional"
```

---

## Los tres casos (tipología Colega)

### Caso A — Sin señal (reforma legítima sin ruptura)
```
PI: $100.000 → PC: $20.000
Causa: proyecto terminó / emergencia climática / nueva prioridad territorial
Compromiso PP/PDOT/RDC: no afectado
→ NO genera SAT-0.1
```

### Caso B — Señal de coherencia (ruptura de participación)
```
Presupuesto Participativo: comunidad votó agua potable como prioridad
Reforma: elimina 80% del financiamiento del programa de agua
→ Participación ≠ Ejecución → SAT-0.1 activa
Narrativa pública: "Recurso comprometido en presupuesto participativo fue reformado"
```

### Caso C — Fricción Narrativa (ruptura de rendición)
```
Alcalde promete → POA incorpora → Presupuesto financia → Concejo reforma
→ Meta desaparece del presupuesto
→ Rendición de Cuentas mantiene narrativa original
→ SAT-0.1 + Fricción Narrativa activa
Detectado por: cruce eSIGEF (codificado) × PDOT metas × texto RDC (NLP)
```

---

## Cadena causal completa

```
Compromiso público verificable
(PP aprobado / meta PDOT / ítem RDC / obligación normativa)
        ↓
Presupuesto inicial refleja el compromiso
        ↓
Reforma presupuestaria reduce recursos significativamente
        ↓
QUIRA detecta: compromiso activo + recursos insuficientes
        ↓
SAT-0.1: Señal de coherencia preventiva
        ↓
Alcalde puede corregir antes de la ruptura
(no después de que el ciudadano lo reclame)
```

---

## Lo que el Excel debe medir (cuando se valide)

No: `Δ(PI - PC)` — demasiado bruto, miles de falsos positivos

Sí:
```
VARIACION_PC_SIGNIFICATIVA = (PI - PC) / PI > umbral_definido
META_ESTRATEGICA_AFECTADA  = cruce con PDOT activo
COMPROMISO_PP_AFECTADO     = cruce con actas PP aprobadas
ITEM_RDC_AFECTADO          = cruce con declaración RDC vigente
NORMA_AFECTADA             = cruce QLEP con artículo de competencia

SAT_0.1 = VARIACION_PC_SIGNIFICATIVA
          AND (META_ESTRATEGICA_AFECTADA
               OR COMPROMISO_PP_AFECTADO
               OR ITEM_RDC_AFECTADO
               OR NORMA_AFECTADA)
```

---

## Filtro de validación requerido (antes de Gold Master v6.0)

- [ ] **Base legal**: confirmar que la detección no penaliza la facultad legítima del Concejo
- [ ] **Casos reales**: 3-5 casos históricos de Montecristi donde habría sido relevante
- [ ] **Falsos positivos**: simular con datos reales cuántas reformas normales dispararían la señal
- [ ] **Umbral de variación**: definir el % mínimo de caída que activa la condición A
- [ ] **Relación con PP, PDOT, RDC**: mapear la cadena completa en Neo4j (QLEP)
- [ ] **Revisión jurídica**: validar lenguaje público con asesor municipal

**Aprobación requerida**: equipo Dylus Lab + validación con caso real Montecristi
**Destino si aprueba**: ADR + Gold Master v6.0 + SAT engine update

---

## Relación con otros componentes

- **Terra Ciudadana v2.1**: concepto original de "Fricción Narrativa" — Caso C
- **Sentinel**: SAT engine actual (SAT-0 a SAT-VIII) — SAT-0.1 sería nueva tipología
- **QLEP + Neo4j**: fuente de la cadena normativa para condición B
- **eSIGEF connector**: fuente de PI y PC para condición A
- **Gold Master v5.5**: NO modificar — este cálculo requiere v6.0

---

*HIP-001 · QUIRA Gov · Dylus Lab © 2026*
*Hipótesis documentada — NO es canon hasta completar filtro de validación*
