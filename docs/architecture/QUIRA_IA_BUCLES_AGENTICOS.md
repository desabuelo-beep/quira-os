# QUIRA IA · Bucles Agénticos — nota para retomar

**2026-06-17 · captura de decisión (Javo + mesa) · NO implementar aún — post-convergencia**
**Relacionado:** ADR-027 (3 capas de soberanía · QUIRA IA = capa transversal) · skill `claude-api`

> Pregunta de Javo: *"los creadores de Claude Code dicen que no promptean sino que usan bucles, ¿qué es y se puede en QUIRA? ¿gastamos más?"*

## Qué es un bucle agéntico
Claude Code **sí usa prompts** — el prompt deja de ser el centro; el sistema es un **ciclo**:
`percibir → razonar → actuar (herramienta) → observar resultado → corregir → repetir` hasta cumplir el objetivo.
El propio trabajo de la mesa (`Firewall Audit → Debt → Blitz → Re-medir`) ya es ese patrón, con el humano cerrando el ciclo.

## El costo — la verdad (corrige el "crece exponencial" de la mesa)
- **Prompt caching:** el contexto repetido (system + herramientas + historial) se cobra a **~10%** (90% de descuento). La "bola de nieve" se aplana: solo los tokens NUEVOS por vuelta pagan completo.
- **Frenos:** `task_budget` (el modelo se autolimita a un presupuesto de tokens), `effort` (low/medium/high), **Batches API (-50%)** para lotes nocturnos.
- **Modelo escudo = Haiku 4.5** (`claude-haiku-4-5`, **$1/$5 por 1M**) — NO el viejo "Claude 3 Haiku". Bucle acotado de 10 vueltas + caché = **centavos**. *(Sonnet 4.6 = $3/$15 · Opus 4.8 = $5/$25.)*

## Arquitectura (la del colega — encaja con la Regla de Oro)
```
Excel → Motor determinista → VERDAD oficial → Agente en bucle → Explicación / Diagnóstico
```
**El motor produce la verdad; el agente produce inteligencia SOBRE la verdad — jamás inventa el dato** (Regla 1: Excel = Estado, no recalcular).

| Capa | Bucles | Uso |
|---|---|---|
| Producción pública (portal · Centro de Mando) | ❌ NO | motor lee snapshot · $0 tokens · auditable · estable |
| QUIRA IA Analista | 🔁 acotados (5-10 · `task_budget`) | *"¿por qué cayó el cumplimiento?"* |
| Dylus Lab | 🔁 largos (20-100) | investigación · auditoría causal · hipótesis |

## Disciplina
**Es el siguiente capítulo de QUIRA IA, NO ahora.** Regla de la mesa: no abrir frentes nuevos hasta cerrar la convergencia (Firewall Blitz + ola 1). Cuando toque: **Haiku 4.5 + prompt caching + task_budget**, sobre el Gold Master validado, en las capas Analista/Dylus — **nunca en la pública**.

---
*Nota de captura · Dylus Lab © 2026 · el motor produce la verdad, el agente la explica.*
