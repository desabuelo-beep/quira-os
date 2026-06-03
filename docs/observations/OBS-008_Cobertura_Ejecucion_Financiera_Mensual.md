# OBS-008 — Cobertura Diferencial de Ejecución Financiera Mensual (LOTAIP)

**Estado**: CONFIRMED  
**Fecha**: 2026-06-03  
**Origen**: Ingesta Gate 6.5 Fase 4b — auto-descubrimiento `ingest_lotaip.py`  
**Candidato**: ADR-022 (evidencia adicional para el gap A≠D cuantificable)

> *"Las cédulas son el puente. Sin ellas puedes demostrar Participación→Rendición,
> pero no Planificación→Ejecución→Rendición." — Colega asesor, 2026-06-03*

---

## Hallazgo Principal

La cobertura de ejecución financiera mensual (LOTAIP Numeral 6-6) es
**heterogénea entre entidades del Holding MCR**. El GAD principal —
la entidad con mayor presupuesto — tiene la menor cobertura temporal.

---

## Cobertura LOTAIP 2025 por Entidad

| Entidad        | Meses disponibles | Meses faltantes | Cobertura |
|----------------|:-----------------:|:---------------:|:---------:|
| BOMBEROS_MCR   | 12/12             | ninguno         | ✅ 100%   |
| EP_ASEO_MCR    | 11/12             | Mar-2025        | 92%       |
| PATRONATO_MCR  | 9/12              | Ene, May, Dic   | 75%       |
| GAD_MCR        | 3/12              | Ene–Sep 2025    | **25%**   |

### Cobertura visual 2025 (✓ = disponible · · = ausente)

```
Entidad          Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic
BOMBEROS_MCR      ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓
EP_ASEO_MCR       ✓   ✓   ·   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓
PATRONATO_MCR     ·   ✓   ✓   ✓   ·   ✓   ✓   ✓   ✓   ✓   ✓   ·
GAD_MCR           ·   ·   ·   ·   ·   ·   ·   ·   ·   ✓   ✓   ✓
```

---

## Cobertura LOTAIP 2026 (datos hasta corte sesión)

| Entidad        | Meses disponibles |
|----------------|:-----------------:|
| BOMBEROS_MCR   | Ene–Mar 2026      |
| EP_ASEO_MCR    | Ene–Feb 2026      |
| GAD_MCR        | Ene–Mar 2026      |
| PATRONATO_MCR  | Ene–Feb, Abr 2026 |

---

## Interpretación

### El gap del GAD no es error técnico — es un hecho administrativo

Los primeros 9 meses de 2025 del GAD Montecristi no fueron publicados
en la plataforma LOTAIP. Esto puede indicar:
1. Retraso en la publicación de transparencia activa
2. Reformas presupuestarias en proceso que impidieron la publicación
3. Datos cargados con rezago hacia fin de año

**Implicación para QUIRA:** Al construir Q09 (POA vs Devengado) para el GAD,
solo se puede comparar Oct–Dic 2025 y Ene–Mar 2026 con los valores planificados.
El período Ene–Sep 2025 del GAD es una caja negra financiera observable
solo desde la RC 2025 (cuando esté disponible).

### Esto es evidencia directa del gap A≠D

```
Norma (COOTAD Art. 7 LOTAIP) exige publicación mensual
    ≠
Realidad: GAD publicó solo 3/12 meses en 2025
```

La norma ordena transparencia. La evidencia muestra incumplimiento
parcial de ese deber de publicación. Eso **no es hipótesis** — es
un gap A≠D medible con los datos ya en el corpus.

---

## Volumen ingresado

| Tipo                    | Archivos | Filas totales (aprox) |
|-------------------------|:--------:|:---------------------:|
| Cédulas mensuales 2025  | 35       | ~3,200                |
| Cédulas mensuales 2026  | 13       | ~1,300                |
| **Total LOTAIP**        | **48**   | **~4,500**            |

---

## Preguntas de investigación habilitadas

| Pregunta | Entidades con cobertura completa | Limitación |
|---|---|---|
| Q09 POA vs Devengado | Bomberos ✅, Aseo ✅ | GAD solo Oct-Dic · Patronato 9 meses |
| Q10 PAC vs Devengado | Bomberos ✅, Aseo ✅ | Misma limitación |
| Q11 Concentración Dic | Bomberos ✅, Aseo ✅ | Patronato: sin Dic 2025 |
| Q12 Gap A≠D LOTAIP    | Todos (parcial GAD) | Caja negra GAD Ene–Sep 2025 |

---

## Relación con ADR-022

OBS-007 definió los Dos Circuitos. OBS-008 provee la evidencia
financiera para validar el Circuito Financiero:

```
POA → PAC → [Cédula mensual = ejecución real] → RC
```

El hallazgo de cobertura diferencial sugiere que ADR-022 deberá
modelar la **asimetría de evidencia entre entidades** — no todas
tienen la misma densidad de datos para el mismo período.

---

## Siguiente paso recomendado

Gate 6.5 Fase 5: SIGAD (evaluación institucional) → completar el
circuito y habilitar Q12 con la dimensión de evaluación formal.

*OBS-008 · QUIRA Gov · Dylus Lab © 2026*
