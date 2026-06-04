# ADR-010 — Alpha termina con una consulta causal reproducible

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones · Director de Arquitectura  

## Contexto

Alpha 0.9 está congelado. Sprint 2 acaba de ser autorizado con objetivo único: "Primer grafo causal funcional." Sin embargo, existe riesgo de que dentro de 6 meses alguien intente redefinir qué significaba completar Alpha — agregar más métricas, más circuitos, más documentación — antes de declarar Alpha 1.0.

Este ADR existe para que eso no ocurra.

## Decisión

**Alpha 1.0 se declara completo cuando Neo4j puede responder la siguiente consulta de forma completa, trazable y reproducible:**

```
CONSULTA BAUTISMAL:
¿Por qué Montecristi mantiene brechas en Dom12
si cumple formalmente COOTAD Art. 249?
```

**Respuesta esperada (cadena causal verificable):**

```
COOTAD_249 (Norma C1)
        ↓ FUNDA
Competencia_GAP_Patronato (C2)
        ↓ HABILITA
Asignacion_GAD (C3 — 20.84% cod → VERDE)
        ↓ HABILITA
Ti_Patronato_2025 (C8 — 50% → ROJO)
        ↓ EXPLICA (con evidencia: G73=29.7%)
Brecha_Dom12_Montecristi (C9 — ROJO)
```

Cada nodo debe ser trazable a una fuente documental verificable (cédula SIGEF o norma).

## Condiciones de aceptación

```
✓ Los 3 QTMPs (GAP_10PCT, AGUA_POTABLE, EQUIDAD) cargados en Neo4j
✓ La cadena causal aparece completa en el grafo
✓ La consulta es reproducible por cualquier observador externo
✓ Cada nodo tiene campo fuente_documental o norma_base

No es condición:
✗ UI/Streamlit integrado
✗ Nuevas métricas o dominios
✗ Validación académica H1-H8
✗ Cédula Patronato dic-2025
✗ Más de 3 circuitos
```

## Por qué este ADR es necesario

Alpha no termina cuando el grafo "funciona técnicamente." Un grafo vacío con Neo4j corriendo no es Alpha 1.0. Alpha termina cuando el grafo **responde correctamente** a una pregunta real sobre el territorio de Montecristi.

Esa distinción — entre sistema funcionando y sistema razonando — es el umbral que separa "colección de documentos" de "infraestructura de razonamiento territorial."

## Consecuencias

- Si alguien propone agregar algo antes de ejecutar la consulta bautismal → rechazar, referir a este ADR
- Si el grafo responde la consulta → declarar Alpha 1.0, documentar en ALPHA_1_0_FREEZE.md
- Si el grafo no responde correctamente → corregir el schema de carga, no agregar nuevos circuitos

## Ver también

ALPHA_0_9_FREEZE.md Sec. IV (condiciones de entrada Alpha 1.0), ADR-005 (Neo4j como cerebro causal)

---

*ADR-010 — Registrado 2026-05-31 por indicación del Director de Arquitectura*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
