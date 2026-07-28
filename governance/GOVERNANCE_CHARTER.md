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

### 1.2 · Principio de Subsidiariedad Normativa

> **Ninguna regla podrá existir en un nivel superior cuando pueda residir completamente en un
> nivel inferior.**

Principio hermano del de Derivación: aquel ordena la autoridad **hacia arriba** (todo declara de
qué deriva); este ordena las reglas **hacia abajo** (nada sube más de lo necesario). Juntos
resumen la filosofía anti-inflación (Art. 4.7) y **cierran de antemano las discusiones futuras**
sobre dónde ubicar una norma: en el nivel más bajo que la contenga por completo.

Aplicaciones ya realizadas: el Principio de Derivación quedó en la Carta y no en la Constitución
(DEC-0002); la Doctrina de Gobernanza quedó como artículo y no como documento (Art. 7); los
invariantes operativos quedaron en la Carta y no como artículos constitucionales.

**Criterio operativo permanente** (asesor · 2026-07-27) — protege a QUIRA de su principal riesgo
futuro: *crecer más rápido en arquitectura que en evidencia*:

> Toda ampliación del marco institucional deberá justificarse demostrando que **aumenta la
> capacidad de explicar, verificar o gobernar un proceso real**; no por mejorar la simetría
> conceptual del sistema.

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
Implementación (código, datos, agentes)

      ⟂  Registry — VISTA GENERADA, transversal a toda la cadena
```
La cadena **nunca se invierte**: el código no modifica el Canon; el Canon no reescribe la Carta.

**El Registry NO es una capa de la cadena** (precisión del asesor · 2026-07-27): no está *entre*
el Canon y la Implementación — es una **fotografía transversal** que las retrata a todas. Situarlo
dentro de la cadena induciría a pensar, en el futuro, que tiene autoridad propia. No la tiene: la
recibe de esta Carta (Art. 1) y **la certifica, no la crea**.

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

### 3.1 · El cumplimiento es un indicador, no un fin

> **El porcentaje de cumplimiento del Principio de Derivación es un indicador operativo,
> nunca un fin institucional.**

La autoridad **no existe para que el Registry marque 100%**: el Registry existe porque la
autoridad existe. Invertir esa relación degradaría la cultura del proyecto — se optimizaría la
métrica en lugar de la sustancia, declarando autoridades vacías para "subir el número".

En consecuencia:
- El Authority Graph **evoluciona por necesidad real**, no por completitud teórica: no se añaden
  tipos de relación ni nodos para que el grafo "se vea completo".
- Un 100% con autoridades mal declaradas vale **menos** que un 95% con cadena sustantiva.
- Ninguna decisión institucional se toma *porque* una métrica lo indique (ver Art. 8).

---

## Artículo 4 · Invariantes Operativos Inviolables

Estos invariantes son **gobernanza, no identidad** (por eso viven aquí y no en la Constitución),
pero su violación compromete la validez de todo el sistema. Detalle operativo: `CLAUDE.md`.

> **Frontera (asesor · 2026-07-27):** esta Carta enuncia **principios**, no implementaciones.
> No nombra archivos, celdas ni lenguajes: debe sobrevivir aunque mañana Python se sustituya
> por otra tecnología. Las referencias concretas (rutas, conectores, celdas del motor) viven en
> `CLAUDE.md` y en el ADR correspondiente.

**4.1 · Motor Único (Regla de Oro 1 y 4).** Existe **un único mecanismo autorizado de cálculo**.
QUIRA **lee** sus valores; **jamás los recalcula** ni construye un motor paralelo. La fórmula
canónica del índice de cumplimiento institucional es **INMUTABLE**. El flujo va del motor hacia
la plataforma y de ahí a la interfaz, **nunca al revés**. *(Constitución Art. 2 y 9.)*

**4.2 · Firewall de Lenguaje (Regla de Oro 2).** La nomenclatura interna del sistema **jamás
cruza al producto**. Afuera: lenguaje de administración pública. Adentro: lenguaje interno.
Prohibido el lenguaje acusatorio. *(Constitución Art. 8 — neutralidad institucional.)*

**4.3 · Evidencia verificada (Regla de Oro 3).** Sin norma verificada criptográficamente, no hay
dato. Prohibido afirmar artículos o cifras sin respaldo. *(Constitución Art. 1 y 2.)*

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

El ciclo de vida de un cambio tiene **dos actos, no uno**: quién lo **propone** y quién lo
**aprueba**. Separarlos es lo que hace auditable la evolución del sistema.

| Nivel | Quién **propone** | Quién **aprueba** | Requisito |
|---|---|---|---|
| **Constitución** | Dirección + asesoría externa | Javo (fundador) | constatar que preserva identidad y principios (Const. Art. 20) |
| **Carta de Gobernanza** | Dirección | Javo | registrar la decisión en `decisions/` |
| **Canon** (Ontología, BRN, ADR) | IA + Dirección (ADR-035 §5) | Javo ratifica | verificación criptográfica contra corpus |
| **Registry / artefactos generados** | *(nadie: se generan)* | *(automático)* | no se editan a mano — Art. 3 |
| **Implementación** | Dirección técnica | Dirección técnica | no puede alterar canon ni invariantes |

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

## Artículo 7 · Doctrina de Gobernanza — criterios de ubicación

> *"Evita que dentro de dos años el equipo vuelva a discutir dónde debe vivir una regla."*
> Es la **jurisprudencia** del ecosistema: no define reglas ni arquitectura, define **criterios**.
> Vive como artículo (no como documento aparte) para respetar el Freeze y la Regla 7. Si crece
> lo suficiente, se extrae a `governance/DOCTRINA_DE_GOBERNANZA.md` por enmienda.

### 7.1 · ¿Dónde vive una regla?

| Pregunta que responde | Va en | Órgano |
|---|---|---|
| ¿Qué **nunca puede cambiar** sin dejar de ser QUIRA? | Constitución | Constituyente |
| ¿Cómo se **gobierna** QUIRA? (autoridad, enmiendas, invariantes) | Carta | Gobernanza |
| ¿Cómo **modela** QUIRA el conocimiento normativo? | Canon (Ontología, BRN, ADR, Glosario) | Canónico |
| ¿Cómo **funciona**? | Implementación (`app/`, `scripts/`, `data/`) | Operativo |
| ¿**Qué existe** y con qué autoridad? | Registry | *(certifica, no gobierna)* |

**Prueba decisiva:** si el artefacto puede cambiar sin que QUIRA deje de ser QUIRA, **no es
constitucional**. La mayoría de las reglas son de Gobernanza o Canon, no de Constitución.

### 7.2 · ¿Cuándo nace cada artefacto?

| Artefacto | Responde | Ejemplo real |
|---|---|---|
| **DEC** (decisión institucional) | ¿Qué **decisión adoptó QUIRA** como institución? | *"Se adopta la numeración constitucional B"* (DEC-0001) |
| **ADR** (decisión de arquitectura) | ¿Por qué se tomó una decisión **técnica**? | *"Elegimos Neo4j frente a otra base de grafos"* |
| **OBS** (observación) | ¿Qué **hallazgo** produjo la evidencia? | *"28/28 audiencias sin resolución Art. 75"* (OBS-017) |
| **PCD** (expediente de curación) | ¿Cómo quedó **curado un dominio**, capa por capa? | PCD-D09 |
| **Enmienda constitucional** | ¿Cambia la **identidad** de QUIRA? | *(ninguna aún)* |

**No se mezclan.** Un DEC no es un ADR: uno decide institucionalmente, el otro técnicamente.
Un OBS no decide nada: reporta lo que la evidencia mostró.

### 7.3 · Relación con el Master Index
`governance/QUIRA_MASTER_INDEX.md` responde *"¿dónde vive la verdad de X?"* para lo que **ya
existe** (rutea a rectores). Este artículo responde *"¿dónde debe vivir X?"* para lo que **va a
nacer** (criterio de creación). Se complementan; no se duplican.

---

## Artículo 8 · Architecture Freeze v1.0

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

### Levantamiento del Freeze — lo decide un órgano, no una métrica

> El Freeze se levanta cuando el **Órgano de Gobernanza certifica** que la cadena de autoridad
> es **suficiente para continuar**, apoyándose en las métricas del `INSTITUTIONAL_STATE` — no
> por el mero hecho de que una métrica alcance determinado valor.

Puede coincidir con el 100%, con el 98% o con el 95%: **la autoridad reside en el órgano, no en
el número** (Art. 3.1). El levantamiento se formaliza mediante un DEC en `decisions/`.

Esto evita el vicio de "gobernar por indicador": una cadena al 100% con autoridades declaradas
mecánicamente no habilita nada; una cadena al 95% con autoridad sustantiva sí puede hacerlo, si
el órgano así lo certifica.

---

*Carta de Gobernanza v1.0 · Dylus Lab © 2026 · deriva de CONSTITUCION-001.*
