# QUIRA · Laboratorio de Hipótesis

> El conocimiento no se canoniza por ocurrencia. Se canoniza por validación.

Esta carpeta es la capa intermedia entre la intuición y la verdad canónica de QUIRA.

## El ciclo de vida del conocimiento en QUIRA

```
Observación o intuición
        ↓
    HIPÓTESIS (HIP-XXX)
        ↓
    Validación contra ADR-025
    (¿detecta ruptura de coherencia verificable?)
        ↓
    Revisión de casos reales + falsos positivos
        ↓
    Decisión de equipo Dylus Lab
        ↓
    Canonizada → Gold Master v6+ / Sentinel / QLEP
    Rechazada  → Permanece aquí como antecedente
```

## Por qué existe esta capa

Hasta ADR-025, el Excel canónico crecía orgánicamente.
Desde ADR-025, el Excel es un **repositorio de métricas validadas**.

Esta carpeta protege el núcleo: ninguna métrica entra al Gold Master
sin pasar por el filtro epistemológico de QUIRA.

## Lo que el Grafo recuerda aquí

El grafo (Graphify) indexa esta carpeta como **Laboratorio**:
- Qué fue aprobado y por qué
- Qué fue rechazado y por qué
- Qué está pendiente y desde cuándo
- Quién lo propuso y en qué contexto

Eso evita que dentro de 18 meses alguien repropose una hipótesis
ya discutida sin saber su historial.

## Estados posibles

| Estado | Significado |
|---|---|
| `PROPUESTA` | Idea inicial, sin validación |
| `OBSERVACIÓN` | Bajo análisis de equipo |
| `VALIDACIÓN` | Probando contra casos reales |
| `APROBADA` | Supera el filtro ADR-025, pendiente implementación |
| `RECHAZADA` | No supera el filtro — queda como antecedente |
| `CANONIZADA` | Incorporada al Gold Master / Sentinel / QLEP |

Solo `CANONIZADA` puede tocar el Excel canónico.

## Hipótesis activas

| ID | Título | Estado | Fecha |
|---|---|---|---|
| HIP-001 | SAT-0.1 Coherencia Presupuestaria | PROPUESTA | 2026-06-05 |

## Referencia normativa

ADR-025 — Principio de Alertas QUIRA: Coherencia Institucional
