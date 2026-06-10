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
B.1   DIAGNÓSTICO    → correr 6 casos · llenar 30 celdas · registrar gaps · NO reparar
B.1A  AUDITORÍA PDOT → barrido temático del corpus (¿gap de datos o de extracción?)
                       → B1A_AUDITORIA_PDOT.md · ejecutada 2026-06-09
B.2   CIERRE         → reparar SOLO gaps críticos priorizados por evidencia
B.3   RE-VALIDACIÓN  → segunda pasada + 6 Fichas de Explicabilidad finales
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
| 2 | Agua potable y alcantarillado (saneamiento básico) | 🟢 | ✅ completada | `FICHA-02_agua_alcantarillado.md` |
| 3 | Violencia de género | 🟡 | ✅ 4/5 + frontera | `FICHA-03_violencia_genero.md` |
| 4 | Movilidad | 🟡 *(era 🔴 — B.1A: 211 chunks, 49 parroquiales)* | ⬜ | — |
| 5 | Desempleo juvenil | 🔴 *(B.1A: demografía sí, tasa no)* | ⬜ | — |
| 6 | Residuos sólidos (recolección · transporte · disposición final) | 🟢 *(era 🟡 — B.1A: 158 chunks, tonelajes)* | ⬜ | — |

**Caso 02 — por qué agua + alcantarillado juntos:** son el mismo sistema (ciclo del
agua). Cobertura de agua alta puede ocultar alcantarillado deficiente → contaminación,
enfermedad, deterioro de fuentes. Así evalúan ODS 6, BDE, CAF, BID y así diagnostica
el PDOT. Transparencia valida la capa institucional; este caso valida la capa
territorial completa (GeoTwin + PDOT + capacidad + fondos + circuito simultáneamente).

**Caso 06 — por qué residuos sólidos separado:** es otra cadena física
(recolección → transporte → disposición final), otro diagnóstico PDOT y otra línea
de financiamiento. Fusionarlo con agua diluiría ambas fichas. Competencia municipal
exclusiva igual que saneamiento — juntos completan el bloque de servicios básicos.

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

## Rol de las fichas en el horizonte UEB/CAF (re-encuadre 2026-06-09)

**Decisión estratégica de Javo:** UEB/CAF no recibe una demo. Recibe **QUIRA
operando sobre X cantones reales**, donde los testers/estudiantes **operativizan
una ingesta completa como experiencia**.

Consecuencia para Sprint B: las fichas dejan de ser "material demo" y se
convierten en **control de calidad del motor antes de replicar**. No se replica
a X cantones un motor no validado — la replicación multiplica defectos.

```
Sprint B   →  validar el motor (Montecristi explicable 6/6 casos)
Sprint C   →  industrializar la ingesta (pipeline operable por no-ingenieros)
Sprint D   →  replicar a X cantones — testers UEB/CAF como operadores de ingesta
```

El diplomado CAF como fuerza de ingesta distribuida: N estudiantes × 1 cantón
cada uno = el radar nacional crece mientras ellos aprenden. La experiencia
educativa ES la expansión del sistema.

---

*Sprint B · QUIRA OS · Dylus Lab © 2026 — definición consensuada Javo + Colega + Director Técnico*
