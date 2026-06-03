# OBS-009 — Divergencia entre Evaluación Externa (SIGAD) y Transparencia Real (LOTAIP)

**Estado**: CONFIRMED — divergencia medida con datos de fuentes independientes  
**Fecha**: 2026-06-03  
**Origen**: Gate 6.5 Fases 4b + 5 · Cruce SIGAD vs LOTAIP vs RC  
**Candidato**: ADR-022 (condición cumplida — circuito completo observado empíricamente)

> *"SIGAD introduce un evaluador externo. Eso permite contrastar lo que el GAD
> dijo vs lo que el SNP registró." — Colega asesor, 2026-06-03*

---

## Hallazgo Central

El GAD Montecristi reporta **ICM = 1.00** (100% de cumplimiento) al sistema
nacional de planificación (SIGAD) en 2023 y 2024.

Simultáneamente, el mismo GAD publicó solo **3/12 meses** de ejecución
financiera mensual requerida por LOTAIP durante 2025, y envió los informes
SIGAD con **16–17 meses de retraso**.

```
SIGAD dice:   ICM = 1.00   → cumplimiento total de metas PDOT
LOTAIP dice:  3/12 meses   → 75% de brecha en transparencia financiera
Envío SIGAD:  +16 meses    → el propio reporte de cumplimiento llegó tarde
```

**Eso no es una contradicción aparente — es el gap A≠D observado empíricamente.**

---

## Evidencia por fuente

### Fuente 1: SIGAD (evaluador externo — SNP)

| Año  | ICM   | Metas | Proyectos | Monto ejecutado    | Fecha envío | Demora |
|------|:-----:|:-----:|:---------:|-------------------:|:-----------:|:------:|
| 2023 | 1.00  | 5     | 13        | $1,824,689.36      | 16/05/2024  | 16 m   |
| 2024 | 1.00  | 9     | 18        | $3,939,101.48      | 30/05/2025  | 17 m   |

**Lectura:** El GAD declara cumplimiento total en ambos años.
Los montos en ejecución = montos ingresados (ratio = 1.0).

### Fuente 2: LOTAIP (transparencia activa — autogestión)

| Entidad        | 2025: meses LOTAIP publicados | Cobertura |
|----------------|:-----------------------------:|:---------:|
| GAD_MCR        | 3/12 (Oct–Dic)                | **25%**   |
| BOMBEROS_MCR   | 12/12                         | 100%      |
| EP_ASEO_MCR    | 11/12                         | 92%       |
| PATRONATO_MCR  | 9/12                          | 75%       |

**Lectura:** El GAD es el único ente del Holding con brecha severa de publicación.
Las empresas subsidiarias (Bomberos, Aseo) cumplen sin problemas.

### Fuente 3: RC (autoevaluación — propio GAD)

Los informes de Rendición de Cuentas 2023 y 2024 están en corpus
(RC-GAD-2023, RC-GAD-2024). El análisis semántico de esos documentos
comparado con los indicadores SIGAD es el siguiente paso analítico.

---

## El patrón

```
Norma (COOTAD + LOTAIP + COPFP)
   ↓ exige
Planificación PDOT → POA → PAC
   ↓ ejecutado
$1,824,689 (2023) / $3,939,101 (2024)
   ↓ reportado a
SIGAD: ICM = 1.00 ✓  (pero 16-17 meses tarde)
   ↓ validado por
RC propia: positiva (autoreporte)
   ↓ verificable en
LOTAIP mensual: GAD publicó 3/12 meses en 2025

Gap observable:
   A (deber ser)  →  transparencia mensual obligatoria
   D (lo que ocurrió)  →  publicación parcial + reportes tardíos
```

---

## Caveat metodológico (recomendado por colega asesor)

La observación de 3/12 meses LOTAIP debe distinguir entre:

1. **Los archivos no existen** — el GAD nunca produjo los datos
2. **Los archivos existen pero no están en el Holding** — pendiente verificación
3. **Los archivos están en otro repositorio** — SIGAD, Ministerio de Finanzas, etc.

**Estado actual de OBS-009:** La divergencia entre ICM=1.00 y LOTAIP=25% es
real e independiente de la causa. Pero la **atribución causal** requiere
verificar si los 9 meses faltantes del GAD existen en algún repositorio público.

**Impacto en ADR-022:** La divergencia es suficiente como evidencia base.
La causa modifica la interpretación pero no invalida el hallazgo.

---

## Comparación: SIGAD Score vs Transparency Score

| Entidad       | SIGAD ICM | LOTAIP 2025 | Divergencia |
|---------------|:---------:|:-----------:|:-----------:|
| GAD_MCR       | 1.00      | 25%         | **75 pts**  |
| BOMBEROS_MCR  | n/d       | 100%        | —           |
| EP_ASEO_MCR   | n/d       | 92%         | —           |
| PATRONATO_MCR | n/d       | 75%         | —           |

El GAD es el único ente con evaluación SIGAD disponible y, paradójicamente,
el que muestra mayor brecha entre evaluación externa (100%) y comportamiento
real de transparencia (25%).

---

## Relación con OBS anteriores

| OBS     | Contenido                              | Relación con OBS-009              |
|---------|----------------------------------------|-----------------------------------|
| OBS-005 | Ciclo PP→RC confirmado                 | OBS-009 agrega dimensión evaluación externa |
| OBS-007 | Dos circuitos trazabilidad             | Circuito B (financiero) ahora medible |
| OBS-008 | Cobertura diferencial LOTAIP           | OBS-009 explica la significancia del gap |

---

## Condición para ADR-022

El circuito completo ahora está observado empíricamente en Montecristi:

```
Norma (COOTAD) ✅
    ↓
PP (participación ciudadana) ✅
    ↓
POA (planificación) ✅
    ↓
PAC (contratación) ✅
    ↓
Cédula mensual (ejecución real) ✅  ←  Fases 4/4b
    ↓
RC (rendición de cuentas) ✅
    ↓
SIGAD (evaluación externa SNP) ✅  ←  Fase 5
```

**OBS-009 es la evidencia fundacional de ADR-022.**
ADR-022 está abierto con estado SUPPORTED (2026-06-03).
Para CONFIRMED: replicar en segundo municipio + cobertura LOTAIP >50%.

---

*OBS-009 · QUIRA Gov · Dylus Lab © 2026*
