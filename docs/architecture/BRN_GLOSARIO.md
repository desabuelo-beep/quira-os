# BRN v2 · Glosario Canónico

> **Qué es.** Definiciones **canónicas** de los términos técnicos de la BRN v2, para que todo lector
> use la misma palabra para el mismo concepto (propuesta del colega · 2026-07-18). Es **interno**
> (docs/) — varios de estos términos son jerga del Bloomberg Firewall (Regla 2) y **jamás cruzan a
> la UI/producto**. Fuente de cada definición: el ADR que la decidió.

| Término | Definición canónica | Fuente |
|---|---|---|
| **Corpus** | El texto jurídico oficial íntegro, con su huella **SHA256** por chunk (Supabase · pgvector). No solo leyes: todo lo que genera obligación operativa (reglamentos, reformas, resoluciones, metodologías). Es donde **vive la verdad**; todo lo demás la referencia. | ADR-038 §4 · ADR-005 |
| **CNO** · Cadena Normativa Operativa | El **nodo de la BRN**: una **regla** con toda su cadena jurídica (fundamentos, reforma, disposición, derogaciones), cada eslabón con su SHA. Es **puro Derecho** — no contiene variable ni umbral. Consultarla obliga a recorrer la cadena entera. | ADR-038 §1 |
| **RO** · Regla Operativa | La **única representación operativa autorizada** de una regla: variable · umbral · periodo · consecuencia. Deriva de una CNO. **Operacionaliza, no interpreta** (Neutralidad Operativa). No es "la verdad": es su representación. | ADR-038 §1b · ADR-039 |
| **MDN** · Modelo de Dependencias Normativas | El **grafo** de la BRN: CNO, RO, SAT y DOM son nodos; sus dependencias, aristas. Da **trazabilidad bidireccional** y convierte una reforma en un mapa de impacto. Implementación recomendada Neo4j; el canon habla del **modelo**, no de la base. | ADR-038 §9 |
| **SAT** · (señal analítica del motor) | El control que **mide** si una regla se cumple. En v2 **no conoce la ley**: lleva solo el **ID de su RO**. La computa el Gold Master. *(Jerga interna · nunca en UI.)* | ADR-038 §2 |
| **DOM** · Dominio | La unidad funcional que **explica** un área de gestión al usuario (d01 Planificación, d02 Presupuesto…). Consume RO/SAT; no conoce Derecho directamente. *(Interno; en UI se usa lenguaje de administración pública.)* | Constitución Ontológica |
| **Gold Master** | El **único motor** de cálculo (Excel SIAP-ICPI v5.5). Calcula ICPI/TGI/SAT. Su fórmula canónica (`H12!B33`) es **inmutable**. Recibe configuración **compilada**; **nunca consulta la BRN en runtime**. *(Jerga interna.)* | ADR-023 · ADR-031 |
| **Compilador** | El **proceso** (no un software) que transforma una RO vigente en un **artefacto de configuración** consumible por el Gold Master. **No decide, materializa**; es determinista, reproducible e idempotente. | ADR-039 |
| **Configuración** | Los **parámetros de entrada** del motor (umbral, periodicidad). Mandan la RO. Distinta del Estado: la configuración entra por **compilación**, no por runtime. | ADR-039 |
| **Estado** | El **resultado** del cálculo (ICPI, Ti, SAT…). Manda **Excel siempre** (Regla 1): `Excel → Python → Supabase → UI`. La Regla 1 protege el estado, no la configuración. | ADR-039 · Regla 1 |
| **Vigencia operativa** | Tramos temporales (`desde·hasta·umbral`) dentro de **una misma RO**, cuando la **norma ya prevé** un cambio de parámetro por calendario (ej. piso 65% en 2026 → 70% en 2027). Es una **transición, no una reforma**: **no versiona** la RO. Distingue el paso del tiempo de un cambio real del texto. | Molde §4b |

## Estados del ciclo de vida (referencia rápida)
- **CNO:** `propuesta` → `vigente` → `en_reforma` → `derogada`
- **RO:** `propuesta` → `vigente` → `obsoleta` / `retirada`
- Solo **Javo** promueve a `vigente` (ADR-035 §5). Detalle: `BRN_CICLO_VIDA_Y_MOLDE.md`.

---
*BRN v2 · Glosario Canónico · Dylus Lab © 2026 · "Una palabra, un concepto — para que a los 40 ADR nadie discuta qué significa CNO."*
