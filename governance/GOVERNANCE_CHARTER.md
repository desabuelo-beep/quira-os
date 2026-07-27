---
id: GOVERNANCE-001
kind: normative
level: 1
status: vigente
authority:
  parent: CONSTITUCION-001
  constitution_articles: [5, 9, 11, 20, 21]
  type: ARQUITECTONICA
owner: Dylus Lab
version: "1.0"
fecha: 2026-07-27
---

# CARTA DE GOBERNANZA DE QUIRA

**Nivel 1 · deriva de la Constitución Institucional (Art. 21) · v1.0 · 2026-07-27**

> **Órgano productor:** Gobernanza. Responde: **¿cómo se gobierna QUIRA?**
> No produce código. No define identidad (eso es la Constitución). No modela conocimiento
> (eso es el Canon). Consolida en UN documento lo que de otro modo serían cuatro
> (stack · autoridad · enmiendas · revisiones) — Regla de Oro 7, anti-inflación del canon.

---

## Artículo 1 · Principio de Derivación Institucional

> **Ningún componente, documento, especificación, modelo, agente, proceso o implementación
> podrá formar parte del ecosistema QUIRA sin declarar explícitamente la autoridad normativa
> de la cual deriva. Toda cadena de autoridad deberá ser reconstruible hasta la Constitución
> de QUIRA.**

Este principio es la **razón de ser de toda la arquitectura institucional**: el Registry, el
Authority Graph y la Matriz de Trazabilidad no requieren justificación propia — existen porque
implementan este artículo.

**Ubicación deliberada:** este principio se ubicó en la Carta y **no** en la Constitución porque
define *cómo se organiza* QUIRA, no *qué es* QUIRA. Solo si con el tiempo demuestra ser
constitutivo se promoverá por enmienda (Constitución Art. 20). Ver `decisions/DEC-0002.md`.

### Artefacto huérfano
Todo artefacto que no declare autoridad, o cuya cadena no sea reconstruible hasta la
Constitución, se considera **huérfano** y **no puede promoverse a `vigente`**.

### Bloque de autoridad obligatorio
Todo artefacto declara, en su encabezado:
```yaml
authority:
  parent: <id del artefacto que lo autoriza>
  constitution_articles: [<artículos que implementa>]
  type: CONSTITUCIONAL | NORMATIVA | ARQUITECTONICA | OPERATIVA | TECNICA
```

---

## Artículo 2 · Los Cuatro Órganos Permanentes

QUIRA no es un árbol de carpetas: es una institución. Cada órgano produce un tipo de artefacto
y **no invade** la competencia de otro.

| Órgano | Produce | Vive en | Nunca produce |
|---|---|---|---|
| **Constituyente** | Identidad | `identity/` | especificaciones técnicas |
| **Gobernanza** | Reglas, decisiones, autoridad | `governance/` | código |
| **Canónico** | Conocimiento normativo (Ontología, BRN, ADR, CNO, RO, Glosario) | `canon/`, `docs/` | infraestructura |
| **Operativo** | Funcionamiento (Core, ETL, APIs, agentes, grafos) | `app/`, `scripts/`, `data/` | **nunca modifica el Canon** |

### Cadena de autoridad
```
Constitución (identidad)
      ↓
Carta de Gobernanza (reglas)
      ↓
Canon (conocimiento normativo)
      ↓
Registry (certifica qué existe)
      ↓
Implementación (código, datos, agentes)
```
La cadena **nunca se invierte**: el Registry no gobierna a la Carta; el código no modifica el Canon.

---

## Artículo 3 · Naturaleza del Registry — describe, no gobierna

El Registry es el **Registro Civil de la institución**: no legisla y no ejecuta — **certifica
qué existe**. Su autoridad deriva de esta Carta (Art. 1), no de sí mismo.

Por eso vive en dominio propio (`registry/`), ni en `governance/` (no gobierna) ni entre el
código (no ejecuta):

| Artefacto | Naturaleza |
|---|---|
| `registry/registry.yaml` | fuente de verdad del catálogo de activos |
| `registry/authority_graph.json` | representación ejecutable del árbol de autoridad |
| `registry/traceability.json` | fuente de la matriz de trazabilidad |

**Authority Graph = un solo activo con múltiples representaciones** (Markdown legible → JSON →
Neo4j). No existen dos documentos para la misma realidad.

### Artefactos generados — nunca se editan a mano
`TRACEABILITY_MATRIX.md` e `INSTITUTIONAL_STATE.md` se **generan** desde el Registry.
Editarlos manualmente rompe la trazabilidad: una matriz escrita a mano termina mintiendo.

---

## Artículo 4 · Invariantes Operativos Inviolables

Estos invariantes son **gobernanza, no identidad** (por eso viven aquí y no en la Constitución),
pero su violación compromete la validez de todo el sistema. Detalle operativo: `CLAUDE.md`.

**4.1 · Motor Único (Regla de Oro 1 y 4).** El Gold Master (Excel SIAP-ICPI) es el **único motor
de cálculo**. QUIRA **lee** sus valores vía `app/connectors/gold_master.py`; **jamás los
recalcula** ni construye un motor paralelo. La fórmula canónica `H12!B33` (ICPI) es **INMUTABLE**.
Flujo: `Excel → Python → Supabase → UI`, nunca al revés. *(Implementa Constitución Art. 2 y 9.)*

**4.2 · Firewall de Lenguaje (Regla de Oro 2).** La jerga interna (ICPI · TGI · Ti · QTMP ·
H01-H99 · Gold Master · node IDs) **jamás cruza al producto**. Afuera: lenguaje de administración
pública. Adentro: lenguaje interno. Prohibido el lenguaje acusatorio (*incumplió · violó ·
ilegal*). *(Implementa Constitución Art. 8 — neutralidad institucional.)*

**4.3 · Evidencia verificada (Regla de Oro 3).** Sin norma verificada por SHA-256, no hay dato.
Prohibido alucinar artículos o cifras. *(Implementa Constitución Art. 1 y 2.)*

**4.4 · Sujeto observado.** El GAD es **sujeto observado, no cliente**. QUIRA es un Observatorio
Nacional de Integridad Territorial (222 GADs); Montecristi es el **molde** (Municipio 001), no el
cliente. *(Implementa Constitución Art. 4 y 8.)*

**4.5 · Verificabilidad, no sanción.** QUIRA distingue **tres cosas que jamás confunde**:
ausencia documental (lo único que certifica) · ausencia jurídica · incumplimiento (lo determina
la autoridad competente). *(Implementa Constitución Art. 8.)*

**4.6 · Origen del cambio (Reglas de Oro 8 y 9).** Ningún cambio conceptual nace en Python: nace
en el canon; Python solo implementa. La curación se hace dominio por dominio, cerrando con su
`PCD-DXX`.

**4.7 · Anti-inflación (Regla de Oro 7).** Un concepto que solo renombra **no entra**: debe
añadir capacidad, eliminar ambigüedad o reducir complejidad.

---

## Artículo 5 · Política de Enmiendas

| Nivel | Quién aprueba | Requisito |
|---|---|---|
| **Constitución** | Javo (fundador) | constatar que preserva identidad y principios (Const. Art. 20) |
| **Carta de Gobernanza** | Javo | registrar la decisión en `decisions/` |
| **Canon** (Ontología, BRN, ADR) | Javo ratifica; la IA propone (ADR-035 §5) | verificación SHA-256 contra corpus |
| **Implementación** | Director técnico | no puede alterar canon ni invariantes |

**Congelados (Regla de Oro 5):** `governance/*` y `.github/workflows/*` no se modifican sin
aprobación explícita de Javo.

---

## Artículo 6 · Política de Revisión y Verificación

La verificación de cumplimiento es **automática, no declarativa**. El gate real es
`scripts/ci/check_health.py` (ejecutado por `.github/workflows/quira-health.yml`), que se
**extiende** para validar el Registry — **no se crea un componente paralelo** (Art. 4.7).

Verificaciones del gate:
1. ¿El artefacto existe en disco?
2. ¿Está registrado en `registry.yaml`?
3. ¿Su `authority.parent` existe y es reconstruible hasta la Constitución?
4. ¿Su estado permite promoción?
5. ¿Su hash coincide con el archivo?

El gate **verifica estados, no interpreta filosofía**.

---

## Artículo 7 · Architecture Freeze v1.0

A partir de la ratificación de esta Carta se declara **Architecture Freeze v1.0**.

**Durante el freeze SOLO está permitido:**
- declarar autoridad de componentes existentes;
- completar trazabilidad;
- documentar decisiones institucionales;
- verificar cumplimiento.

**Queda prohibido:** crear documentos o conceptos nuevos, **salvo que sean consecuencia directa
de un documento ya autorizado**.

> El éxito de QUIRA deja de medirse por cuántos documentos nuevos produce, y pasa a medirse por
> su capacidad de **demostrar que toda la plataforma obedece la cadena de autoridad** definida
> por su Constitución, su Carta y su Canon.

**Levantamiento del freeze:** requiere que el `INSTITUTIONAL_STATE` reporte cadena de autoridad
completa y Registry íntegro.

---

*Carta de Gobernanza v1.0 · Dylus Lab © 2026 · deriva de CONSTITUCION-001.*
