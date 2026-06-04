# ADR-008 — C10 (Reflexión Institucional) es Alpha, no Beta

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  
**Origen**: Propuesta Director de Arquitectura — sesión 2026-05-31

## Contexto

Al descubrir las limitaciones del indicador `Ti_G7+G8` (ADR-006), surgió la pregunta: ¿QUIRA debería esperar a Beta para registrar y comunicar sus propias limitaciones metodológicas?

La tentación era: "si no podemos medirlo bien, no lo mostremos hasta Beta." El riesgo: un sistema que oculta sus limitaciones en lugar de declararlas pierde credibilidad epistemológica.

## Decisión

**C10 — Reflexión Institucional es la décima capa de la cadena causal QNKC-002, y pertenece a Alpha 1.0, no a Beta.**

```
Alpha 0.8: QUIRA mide
Alpha 0.9: QUIRA explica
Alpha 1.0: QUIRA reconoce explícitamente lo que aún no puede explicar
```

C10 no es una capa técnica de ingeniería — es una capa epistémica. QUIRA activa C10 cuando:
- Un C9 tiene datos insuficientes para concluir
- Un indicador tiene limitaciones metodológicas documentadas
- Una hipótesis causal no está validada externamente

C10 registra el hallazgo, lo etiqueta (`BETA-DOM12-001`, etc.) y lo pone en el Beta Backlog — sin ocultar la limitación, sin pretender tener lo que no tiene.

## Consecuencias

- El Beta Backlog (QUIRA_BETA_BACKLOG.md) es el OUTPUT de C10 — no un bug tracker
- Principio 6 (Autocuración Metodológica): QUIRA no elimina limitaciones — las convierte en tareas trazables
- La Red Académica valida los ítems C10, no los resultados confirmados
- Un sistema que dice "no lo sé" es más confiable que uno que siempre dice que sí sabe

## Fundamento teórico

Autopoiesis (Luhmann): C10 da a QUIRA la capacidad de observar sus propias observaciones — sistema autopoiético. Ver QUIRA_CAUSAL_MODEL_v1.0.md Adenda Sec. XIV.
