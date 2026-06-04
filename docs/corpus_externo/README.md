# ADR Index — Architecture Decision Records

**DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones**

---

## ¿Qué es un ADR?

Un ADR (Architecture Decision Record) registra una decisión arquitectónica o de diseño con su contexto, las alternativas consideradas y la decisión adoptada. Es inmutable una vez aceptado — para revertirlo se crea un ADR nuevo que lo supera. El historial completo es la fuente de verdad sobre por qué el sistema es como es.

---

## Índice de decisiones

| ID | Título | Estado | Fecha |
|----|--------|--------|-------|
| [ADR-001](ADR-001_PDOT_fuente_canonica_territorial.md) | PDOT como fuente canónica territorial | Aceptado | 2026-05-31 |
| [ADR-002](ADR-002_COOTAD_vs_INEC_dominios_separados.md) | COOTAD vs INEC — dominios separados | Aceptado | 2026-05-31 |
| [ADR-003](ADR-003_proxy_requiere_proxy_de.md) | Proxy requiere `proxy_de` | Aceptado | 2026-05-31 |
| [ADR-004](ADR-004_ProyecT_workspace_oficial.md) | ProyecT como workspace oficial | Aceptado | 2026-05-31 |
| [ADR-005](ADR-005_Neo4j_cerebro_causal_no_vector.md) | Neo4j como cerebro causal (no vector) | Aceptado | 2026-05-31 |
| [ADR-006](ADR-006_Ti_G7G8_es_Piso1_no_impacto_territorial.md) | Ti G7/G8 es Piso 1, no impacto territorial | Aceptado | 2026-05-31 |
| [ADR-007](ADR-007_Gold_Master_unica_fuente_calculo.md) | Gold Master como única fuente de cálculo | Aceptado | 2026-05-31 |
| [ADR-008](ADR-008_C10_reflexion_institucional_es_Alpha.md) | C10 — reflexión institucional es Alpha | Aceptado | 2026-05-31 |
| [ADR-009](ADR-009_Red_Academica_valida_incertidumbres.md) | Red Académica valida incertidumbres | Aceptado | 2026-05-31 |

---

## Agregar un nuevo ADR

1. Crear el archivo con el ID siguiente: **`ADR-010_<nombre_descriptivo>.md`**
2. Usar la estructura estándar: `# Contexto` → `# Alternativas consideradas` → `# Decisión` → `# Consecuencias`
3. Agregar una fila a la tabla de este índice con estado `Aceptado` o `Propuesto` según corresponda

> El próximo ID disponible es **ADR-010**.
