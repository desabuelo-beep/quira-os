# HIP-001 — SAT-0.1 Coherencia Presupuestaria

**Estado**: PROPUESTA
**Fecha de apertura**: 2026-06-05
**Origen**: Terra Ciudadana v2.1 (concepto "desfinanciamiento silencioso") →
           debate equipo Dylus Lab → refinamiento jurídico Colega → ADR-025

---

## Problema observado

Un GAD incorpora en su POA una meta con financiamiento. El Concejo Municipal
aprueba posteriormente una reforma presupuestaria que reduce significativamente
esos recursos. Al final del período, la meta no se cumple.

El alcalde declara en rendición de cuentas que "se trabajó en esa área",
pero los datos de ejecución muestran recursos insuficientes desde meses antes.

El ciudadano no supo que la meta era inviable hasta que fue demasiado tarde.

QUIRA tampoco lo detectó, porque registró la reforma presupuestaria como
un acto administrativo normal — que lo es — sin cruzarla con el compromiso
que esa partida respaldaba.

## Base normativa

| Norma | Artículo | Relevancia |
|---|---|---|
| COOTAD | Art. 227, 229 | Proceso presupuestario municipal · reformas |
| COPFP | Art. 54, 115 | Coherencia POA-presupuesto · reformas significativas |
| COOTAD | Art. 302 | Rendición de cuentas ante CPCCS |
| LOPC | Art. 64-77 | Presupuesto participativo como compromiso ciudadano |
| COOTAD | Art. 238, 247 | Equidad territorial en asignación de recursos |

*Validación pendiente: confirmar base específica con corpus QLEP*

## Cadena causal

```
Compromiso público verificable
(meta PDOT / compromiso PP / ítem RDC / obligación normativa)
        ↓
Presupuesto inicial refleja ese compromiso
        ↓
Reforma presupuestaria reduce recursos en >X% (umbral a definir)
        ↓
RUPTURA: compromiso activo + recursos insuficientes para cumplirlo
        ↓
Si no se detecta preventivamente:
  → Meta no cumplida al cierre del período
  → Fricción Narrativa en rendición de cuentas
  → Ciudadano sin respuesta hasta que ya fue demasiado tarde
```

**Eje de ruptura**: Presupuesto ↔ Participación (Caso B) | Presupuesto ↔ Rendición (Caso C)

## Riesgo de falsos positivos

Una reforma presupuestaria es un acto administrativo LEGÍTIMO.
Por eso SAT-0.1 NO puede activarse solo por Δ PI → PC.

Casos que NO deben generar alerta:
- Proyecto terminó antes de lo previsto → recursos reasignados legítimamente
- Emergencia climática → repriorización urgente y documentada
- Nueva necesidad territorial detectada → POA reformulado con justificación
- Desfase temporal entre codificación y devengado (diferencia estacional)

**Condición mínima para activar**: la partida reducida debe estar vinculada
a un compromiso público verificable (PP / meta PDOT / ítem RDC / norma).
Sin ese vínculo → no hay alerta, solo dato de contexto.

Estimación de falsos positivos si se usa solo Δ PI-PC > 20%: **MUY ALTA**
(la mayoría de reformas presupuestarias no afectan compromisos específicos)

Estimación de falsos positivos con la condición completa: **BAJA** (hipótesis)

## Impacto esperado si se canoniza

**Para el alcalde**: saber con anticipación que un compromiso ya no tiene
financiamiento, para poder corregir o comunicar proactivamente.

**Para el ciudadano**: ver en QUIRA Ciudadana si una obra comprometida
en presupuesto participativo fue desfinanciada.

**Para el analista / academia**: detectar patrones sistemáticos de
desfinanciamiento de compromisos participativos en múltiples GAD.

**Para la CAF / BID**: evidencia de gobernanza preventiva vs. reactiva.

## Definición propuesta (sujeta a validación)

```
SAT-0.1 — Señal de Coherencia Presupuestaria (preventiva)

CONDICIÓN (requiere A Y al menos una de B):
  A. Variación PI → PC > umbral (% a definir con casos reales)
  B. La partida reducida está vinculada a:
       [ ] Meta estratégica del PDOT activo
       [ ] Compromiso aprobado en Presupuesto Participativo
       [ ] Ítem declarado en Rendición de Cuentas vigente
       [ ] Obligación con base normativa verificada (QLEP)

RESULTADO: Señal de coherencia preventiva (no sancionatoria)
TIPO: informacional/preventiva · no es hallazgo · no es sanción
LENGUAJE PÚBLICO: "Compromiso institucional con recursos reducidos"
FUENTES: eSIGEF (PI y PC) × PDOT × actas PP × declaración RDC
```

## Validación requerida para avanzar de PROPUESTA a VALIDACIÓN

- [ ] Confirmar base normativa específica con corpus QLEP
- [ ] Identificar 3-5 casos históricos reales de Montecristi (2020-2025)
      donde esta hipótesis hubiera sido relevante
- [ ] Definir el umbral de variación PI→PC (requiere análisis de datos reales)
- [ ] Simular con datos reales cuántas reformas presupuestarias de Montecristi
      habrían activado SAT-0.1 correctamente vs. como falso positivo
- [ ] Mapear la cadena completa en Neo4j (compromiso → partida → reforma → resultado)
- [ ] Revisión jurídica: confirmar que la detección no penaliza la facultad
      legítima del Concejo Municipal

## Log de decisiones de equipo

| Fecha | Estado anterior | Estado nuevo | Decisión | Quién |
|---|---|---|---|---|
| 2026-06-05 | — | PROPUESTA | Hipótesis abierta desde Terra Ciudadana | Colega |
| 2026-06-05 | PROPUESTA | PROPUESTA | Refinamiento jurídico: NO es alerta financiera sino de coherencia | Colega + Claude |
| 2026-06-05 | PROPUESTA | PROPUESTA | Formato estandarizado ADR-025 aplicado | Claude |

---

*HIP-001 · QUIRA Gov · Dylus Lab © 2026*
*Referencia: ADR-025 — Principio de Alertas QUIRA: Coherencia Institucional*
*Destino si canonizada: Gold Master v6.0 + Sentinel engine*
