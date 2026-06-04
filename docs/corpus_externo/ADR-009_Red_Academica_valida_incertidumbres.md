# ADR-009 — La Red Académica valida incertidumbres (C10), no resultados

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

QUIRA tiene hipótesis causales (H1-H8) marcadas como `estado: hipotesis`. Tiene ítems en el Beta Backlog que requieren validación metodológica externa. La pregunta era: ¿cuándo y para qué involucramos a la Red Académica (FLACSO, IAEN, UEB, ESPAM)?

Dos visiones posibles:
1. "La academia valida los resultados" — QUIRA presenta sus indicadores y la academia los certifica
2. "La academia valida las incertidumbres" — QUIRA presenta sus limitaciones y la academia las resuelve

## Decisión

**La Red Académica (FLACSO / IAEN preferidos para causalidad; UEB / ESPAM para microdatos) valida las INCERTIDUMBRES registradas en C10, no los resultados ya confirmados.**

Los resultados confirmados se validan con SIGEF (cédulas oficiales) y documentos primarios — eso no requiere academia.

Lo que requiere Red Académica:
- Validación de cadenas causales H1-H8 (`estado: hipotesis` → `estado: validado_academico`)
- Calibración metodológica de índices Piso 2 (BETA-DOM12-001)
- Procesamiento microdatos INEC DPA 2022 parroquiales (BETA-TERRITORIO-001)
- Revisión estándar de confirmación de hipótesis (BETA-METODO-001)

Lo que NO requiere Red Académica:
- `Ti_Patronato = 50%` — es aritmética sobre cédulas SIGEF
- `Ratio_COOTAD_249 = 20.84%` — es aritmética sobre cédulas SIGEF
- Los datos confirmados del Gold Master

## Consecuencias

- La publicación potencial es: artículo metodológico QUIRA/SIAP-ICPI (BETA-METODO-001)
- Los ítems Beta con `estado_metodologico: pendiente_academia` esperan la Red Académica
- El estado `validado_academico` en el Beta Backlog requiere revisión formal de al menos un par académico
- QUIRA no necesita esperar la academia para operar en Alpha — opera con hipótesis declaradas

## Ver también

QUIRA_BETA_BACKLOG.md, ADR-008 (C10), QUIRA_CAUSAL_MODEL_v1.0.md Sec. XIV
