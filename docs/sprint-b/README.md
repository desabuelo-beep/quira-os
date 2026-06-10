# SPRINT B — Validación de QUIRA Operaciones · Montecristi v1.0
**QUIRA OS · Dylus Lab · 2026**

---

## Objetivo canónico

> **Montecristi debe convertirse en el primer territorio completamente explicable por QUIRA.**

Sprint B NO construye funcionalidades. Valida la hipótesis:

> ¿QUIRA Operaciones puede explicar Montecristi como sistema completo —
> sin fuentes externas nuevas, sin oficios pendientes, sin procesamiento manual
> fuera del ecosistema?

Si la respuesta es sí: Institucional = empaquetado · Ciudadana = traducción ·
Impact/Economic/Cooperación = vistas. El motor es el activo; las UIs son derivados (ADR-024).

---

## Estructura del sprint

```
B.1  DIAGNÓSTICO     → correr 5 casos · llenar 25 celdas · registrar gaps · NO reparar
B.2  CIERRE          → reparar SOLO gaps críticos priorizados por evidencia
B.3  RE-VALIDACIÓN   → segunda pasada + 5 Fichas de Explicabilidad finales
```

**Regla anti-madriguera (inviolable en B.1):** si un caso falla una pregunta,
se registra el gap y se continúa. El diagnóstico se completa ENTERO antes de reparar.
Sin esta regla, Sprint B se convierte en 5 mini-proyectos secuenciales.

---

## Matriz de validación — 5 casos × 5 preguntas

| Pregunta | Fuente primaria | Motor |
|---|---|---|
| ¿Qué pasa? | PDOT / Corpus | GeoTwin |
| ¿Por qué pasa? | Motor de indicadores | ADR-026 |
| ¿Dónde pasa? | PDOT territorializado | PD-GEO-01 |
| ¿Cuánto cuesta no resolverlo? | Circuito rendición + D02 | Neo4j |
| ¿Qué recursos existen? | fondos_radar | Matcher |

| # | Caso | Pronóstico | Estado | Ficha |
|---|---|---|---|---|
| 1 | Transparencia | 🟢 | ✅ completada | `FICHA-01_transparencia.md` |
| 2 | Agua potable | 🟢 | ⬜ | — |
| 3 | Violencia de género | 🟡 | ⬜ | — |
| 4 | Movilidad | 🔴 | ⬜ | — |
| 5 | Desempleo juvenil | 🔴 | ⬜ | — |

El pronóstico desigual es deliberado: dos verdes validan el motor,
dos rojos mapean la **frontera actual del sistema** — el entregable más
importante antes de escalar.

---

## Plantilla — Ficha de Explicabilidad QUIRA

Cada caso produce una ficha con esta estructura exacta:

```markdown
# FICHA DE EXPLICABILIDAD QUIRA — [Caso]

## Caso
[Nombre del caso en lenguaje de gobernanza]

## ¿Qué pasa?
[Respuesta del sistema]

## ¿Por qué pasa?
[Respuesta del sistema]

## ¿Dónde pasa?
[Respuesta territorial — o convención institucional si aplica]

## ¿Cuánto cuesta no resolverlo?
[Impacto financiero o institucional]

## ¿Qué recursos existen?
[Fondos, cooperación, instrumentos]

## Evidencia
- Fuente 1 · Fuente 2 · Fuente 3

## Nivel de confianza
Alto / Medio / Bajo — por pregunta

## Gaps detectados
| Tipo | Descripción | Dónde debería vivir | Esfuerzo |
|---|---|---|---|
| Dato / Nodo / Indicador / Conector | ... | ... | ... |

## Acción propuesta
[Próximo paso — se ejecuta en B.2, no ahora]
```

---

## Reglas de redacción de fichas

1. **Bloomberg Firewall desde el origen.** El cuerpo de la ficha (las 5 respuestas)
   se escribe 100% en lenguaje de gobernanza — sin códigos internos de metodología,
   sin identificadores de nodos, sin referencias al motor de cálculo.
2. **Pie técnico separado.** La trazabilidad interna (tablas, evaluaciones, conectores)
   va en el pie "Referencia interna" — igual que los oficios D12. El material demo
   para UEB/CAF es la ficha SIN pie.
3. **Sin dato verificable, no hay afirmación.** Cada cifra debe poder rastrearse a
   una fuente del sistema (Supabase, Neo4j, corpus, conector). Prohibido estimar.
4. **"¿Dónde pasa?" admite convención institucional.** Para casos de capacidad
   institucional (PD-GEN-01: 20%), la respuesta canónica es "sede institucional /
   impacto cantonal uniforme" — no se fuerza una capa territorial que no existe.

---

## Doble uso de las fichas

```
Validación interna  →  ¿el motor explica el territorio?
Material demo       →  UEB · CAF · caso Montecristi · académico · comercial
```

Sprint B produce **evidencia**. La evidencia después sirve para vender,
enseñar, defender y mejorar QUIRA.

---

*Sprint B · QUIRA OS · Dylus Lab © 2026 — definición consensuada Javo + Colega + Director Técnico*
