# ADR-012 — Regla de Expansión Canónica de Dominios QUIRA

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones · Director de Arquitectura  
**Motivado por**: Análisis Director de Arquitectura (colega) — riesgo de fragmentación ontológica en BETA

---

## Contexto

Alpha 1.0 demostró que QUIRA puede razonar sobre el territorio.
La pregunta Alpha era: "¿QUIRA funciona?" — Respuesta: sí.

La pregunta Beta es: "¿QUIRA puede explicar Montecristi completo?"

Para responderla se necesitan 12 dominios causalmente cerrados.
El riesgo identificado:

> 12 dominios = 12 oportunidades de romper la ontología.

Sin un gate formal de entrada, cada dominio puede ingresar al grafo
con cadenas incompletas, datos sin fuente verificable, o resultados sin C9 territorial.
Eso crea contradicciones internas que invalidan la capacidad de QUIRA
de describir Montecristi sin inconsistencias metodológicas.

El riesgo no es construir lento. Es construir incorrecto y tener que deshacer.

---

## Decisión

**Ningún dominio entra al grafo sin cumplir los cinco niveles — en ese orden:**

```
Nivel 1 — Norma identificada
  → ACK atom registrado en Supabase (QLEP)
  → C1 (norma raíz) y C2 (actor obligado) definidos
  → Sin norma: no hay obligación verificable → el dominio no existe para QUIRA

Nivel 2 — Pregunta bautismal definida
  → Consulta Cypher canónica que el dominio debe ser capaz de responder
  → Equivalente a la consulta ADR-010 que cerró Alpha 1.0
  → La pregunta debe ser formulable antes de cargar datos

Nivel 3 — Cadena causal completa
  → C3 (servicio) → C4 (proceso) → C5 (evidencia) → C6 (control) → C7 (observabilidad) → C8 (indicador)
  → Registrada en QTMP schema (YAML) antes de cargar al grafo
  → Cada nodo con fuente_documental o estado epistémico explícito

Nivel 4 — C9 verificable
  → Resultado territorial con valor numérico y fuente pública identificada
  → Estado: confirmado / pendiente_validacion / proxy_documentado
  → Sin C9: la cadena no llega al territorio → el dominio no está cerrado

Nivel 5 — C10 registrado
  → Reflexión institucional documentada en QUIRA_BETA_BACKLOG.md
  → Incertidumbres formalizadas (hipótesis H marcadas)
  → Lo que se descubrió que no sabíamos — convertido en estructura, no en deuda oculta
```

**Si un dominio no cumple los cinco niveles:**

```
→ No entra al grafo
→ Sus datos se registran en ProyecT\ (capturados, no descartados)
→ El gap entre nivel alcanzado y Nivel 5 se registra como entrada C10
→ Entra en el siguiente sprint cuando complete los niveles faltantes
```

---

## Criterio de cierre de BETA

BETA cierra cuando los 12 dominios de Montecristi cumplen los cinco niveles.
No antes.

**Sprint de validación (Sprint 9):**
> "¿Puede QUIRA describir Montecristi completo sin contradicciones metodológicas?"

Operacionalización:
- Un técnico externo recorre los 12 dominios sin intervención del equipo
- Cada semáforo tiene fuente verificable
- Ninguna cadena tiene nodos sin estado epistémico definido
- Si la respuesta es SÍ → GAMMA se abre
- Si la respuesta es NO → Sprint 9b: resolver antes de escalar

---

## Consecuencias

- El ritmo de construcción está gobernado por la profundidad de la cadena, no por la disponibilidad de datos. Tener datos no es suficiente para cargar un dominio.
- GAMMA (segundo cantón) no se abre hasta que Sprint 9 valide Montecristi completo.
- CAF, academia, expansión y ciudadana son posteriores al cierre de BETA.
- Los dominios que no cumplan un nivel en su sprint entran al BETA_BACKLOG como C10 — no se descartan, se formalizan como incertidumbre.
- La velocidad del sistema no se mide en dominios cargados sino en cadenas verificables cerradas.

---

## Principio director

> Montecristi no es un piloto.
> Es el laboratorio donde QUIRA aprende qué es un municipio.
> Cuando QUIRA pueda representar correctamente un municipio completo,
> los otros cantones son escala.
> Montecristi es descubrimiento.

---

## Ver también

ADR-008 (C10 como Alpha), ADR-009 (Red Académica valida incertidumbres),
ADR-010 (criterio de cierre Alpha — pregunta bautismal),
QUIRA_BETA_BACKLOG.md, QUIRA_CAUSAL_MODEL_v1.0.md

---

*ADR-012 — Registrado 2026-05-31*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
