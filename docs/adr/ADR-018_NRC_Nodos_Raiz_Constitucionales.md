---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-018 — Nodos Raíz Constitucionales (NRC)
## Categoría Formal de ACKs con Alcance Multi-Dominio

**Versión:** 1.0  
**Fecha:** 2026-06-02  
**Estado:** CONGELADO v1.0  
**Autores:** Dylus Lab · Colega asesor  
**Relacionado:** ACK_REGISTRY.md · ADR-016 (DCO) · ADR-017 (Circuitos) · FOUNDATION_LAYER_V1.md

---

## El problema que resuelve

El ACK Registry operacional (v0.2 · 11 ACKs) contiene dos tipos de átomos que se comportan de manera fundamentalmente diferente, pero el schema v0.1 no los distinguía:

```
ACK normal → funda un dominio

ACK raíz   → funda múltiples dominios simultáneamente
```

Ejemplo concreto:

```
CE_226 (Principio de Legalidad)

No describe Transparencia.
No describe Participación.
No describe Presupuesto.

Describe las condiciones bajo las cuales el Estado puede actuar en absoluto.
Por eso aparece en los 12 dominios simultáneamente.
```

```
CE_18 (Derecho a la información)

No pertenece a Dom07.
Dom07 es una manifestación institucional de CE_18.

La LOTAIP operacionaliza CE_18 en Dom07.
Pero CE_18 como derecho aplica también a Dom08 (participación informada),
Dom09 (rendición de cuentas), Dom02 (transparencia presupuestaria), etc.
```

Sin la distinción formal, QUIRA no puede responder correctamente:
```
"¿Qué ACK funda todo el sistema?"
"¿Qué ACK, si se derogara, rompería múltiples dominios independientes?"
"¿Por qué Dom07 aparece en C01 y C02?"
```

---

## La decisión

Introducir `es_nrc: boolean` como campo formal en el schema ACK con criterio de asignación conservador.

**Criterio canónico de NRC:**

> Si eliminar el ACK rompe la base normativa de 2 o más dominios independientes → candidato a NRC.

El criterio es deliberadamente conservador. No todo artículo transversal es NRC. La prueba es la ruptura de dominios *independientes* — no relacionados temáticamente entre sí.

```
LOTAIP_7: si se deroga → Dom07-A se debilita. Pero Dom08, Dom04, Dom12 siguen
           funcionando desde sus propias normas fundantes.
           → NO es NRC. Es ACK sectorial de alta importancia.

CE_18: si se deroga → Dom07 colapsa. Y Dom08 pierde su fundamento informacional
        (no puedes participar sin acceso a información). Y Dom09 pierde la base
        de la rendición de cuentas. Y Dom02 pierde la obligación de publicar
        presupuestos. Dominios independientes, todos afectados.
        → ES NRC.
```

---

## NRCs actuales (v1.0 del registry · 4 candidatos)

| NRC | Tipo | Dominios directamente afectados | Por qué es raíz |
|---|---|---|---|
| `CE_226` | principio | Dom01-Dom12 (todos) | Principio de Legalidad: sin él, ninguna actuación del GAD tiene fundamento constitucional |
| `CE_18` | derecho | Dom07, Dom08, Dom09, Dom02, Dom04 | Derecho a información: prerequisito de participación, rendición, planificación informada |
| `CE_95` | derecho | Dom08, Dom07-demanda, Dom09 | Participación protagónica: cierra el ciclo democrático cantonal |
| `CE_264` | competencia_exclusiva | Dom04, Dom10, Dom02, Dom03, Dom11 | Competencias GAD: sin ellas, ningún dominio municipal tiene mandato constitucional |

**Máximo esperado en corpus completo:** 6-8 NRCs.  
Más de 10 indicaría que el criterio se está aplicando incorrectamente.

---

## La nueva ontología

### Antes de ADR-018

```
ACK
  ↓ ancla a
DCO (dominio)
  ↓ sus nodos son
Circuito
  ↓ produce
Diagnóstico
```

### Después de ADR-018

```
NRC (Nodo Raíz Constitucional)
  ↓ habilita
ACK normal
  ↓ ancla a
DCO (dominio)
  ↓ sus nodos son
Circuito
  ↓ produce
Diagnóstico
```

El NRC no reemplaza al ACK — es una categoría de ACK con alcance universal. Un NRC puede participar en múltiples circuitos simultáneamente a través de los dominios que funda.

---

## Los dos flujos causales (válidos, propósitos distintos)

### Flujo de construcción (para desarrollar el sistema)

```
NRC (axioma constitucional)
  ↓
ACK normal (operacionalización normativa)
  ↓
DCO (dominio como sistema de razonamiento)
  ↓
Circuito (cadena causal multi-dominio)
  ↓
Diagnóstico (C01 = COLAPSADO / CHS = 0.0)
```

Sirve para: decidir qué ACK crear, qué DCO construir, qué circuito modelar.

### Flujo de explicación (para justificar una conclusión)

```
Diagnóstico (C01 = COLAPSADO · Portal LOTAIP 120 días sin actualizar)
  ↓
Circuito afectado (C01: Dom07 → Dom08 → Dom04)
  ↓
DCO del nodo ORIGEN (Dom07 · norma fundante: CE_18)
  ↓
ACK activado (LOTAIP_7 · instrumento de observación)
  ↓
NRC raíz (CE_226 · principio de legalidad de toda la cadena)
```

Sirve para: responder "¿por qué C01 está colapsado?", "¿qué norma funda esta conclusión?", "¿quién es el responsable legal?". Este flujo es el más importante políticamente — el alcalde pregunta "¿por qué?" y la trazabilidad descendente responde.

---

## Lo que QUIRA revela, no impone

El hallazgo más profundo de ADR-018 no es técnico:

```
QUIRA no impone una teoría de gobernanza.
QUIRA revela una estructura que emerge del ordenamiento jurídico.
```

CE_226 fue escrito en 2008 por la Asamblea Constituyente.  
CE_18 define derechos desde la misma fecha.  
La Asamblea diseñó que la legalidad (CE_226) y la información (CE_18) serían prerrequisitos de toda actuación pública.

Cuando Neo4j confirme empíricamente que CE_226 y CE_18 tienen la mayor betweenness centrality en el grafo de circuitos, QUIRA no estará haciendo una afirmación teórica. Estará mostrando una propiedad matemática de la Constitución ecuatoriana.

Esa diferencia importa para la legitimidad política del sistema:

```
Sin ADR-018: "El algoritmo dice que C01 está colapsado"
Con ADR-018: "La Constitución (CE_226 · CE_18) dice que el GAD debe informar.
              El GAD no informa (120 días). Por lo tanto C01 colapsa."
```

La causalidad no es estadística. Es normativa.

---

## Cambios al schema ACK

### Campo nuevo: `es_nrc`

```yaml
# Posición: después de fundante
es_nrc: true    # true = Nodo Raíz Constitucional · funda 2+ dominios independientes
                # false = ACK normal · alcance sectorial
                # (omitido = equivalente a false · retrocompatible)
```

**Reglas:**
- `es_nrc: true` SOLO se asigna después de validar el criterio conservador
- Un NRC es siempre `fundante: true` (la implicación inversa no aplica)
- `es_nrc` NO cambia el `tipo` — un principio, derecho o competencia sigue siendo su tipo
- Máximo 8 NRCs esperados en el corpus completo

### Consultas habilitadas

```bash
# ¿Cuántos NRCs existen?
python register_ack.py --stats
# → NRCs (Nodos Raiz): 4/11

# ¿Qué ACKs son NRC?
python register_ack.py --filter-nrc

# Traversal de CE_226 (NRC raíz)
python register_ack.py --traverse CE_226
```

---

## Relación con Foundation Layer v1.0

ADR-018 extiende el Pilar III (ACK_REGISTRY) sin modificarlo:

```
Pilar III actual:  ACK → DCO → Circuito
Pilar III + ADR-018:  NRC → ACK → DCO → Circuito
```

La regla de extensión de Foundation Layer v1.0 se mantiene intacta. ADR-018 cumple con ella: es un ADR formal que extiende un pilar existente (Pilar III) en lugar de inventar vocabulario nuevo.

---

## Próximos NRC candidatos (sin confirmar)

| Candidato | Razón | Estado |
|---|---|---|
| CE_85 | Principio de igualdad y no discriminación → Dom06, Dom12, Dom04 | Pendiente criterio |
| CE_238 | Definición y autonomía de los GADs → funda todo el sistema local | Pendiente QLEP |
| CE_340 | Sistema Nacional de Inclusión → Dom12, Dom09 | Pendiente QLEP |

Ninguno confirmado hasta aplicar el criterio formal.

---

## Estado de implementación (2026-06-02)

```
ADR-018:                  ✅ CONGELADO v1.0
Schema es_nrc:            ✅ Implementado en ack_registry.json v0.2
NRCs iniciales:           ✅ CE_226 (nuevo) · CE_18 · CE_95 · CE_264
register_ack.py:          ✅ --filter-nrc · --stats muestra NRCs
CE_226 chunk_refs:        ⏳ Pendiente --link-corpus CE_226 (corpus F0.1 disponible)
```

---

## Observación Empírica 2026-06-02 — NRCs como Comunidad Constitucional Computacionalmente Detectable

**Fuente**: `scripts/analytics/compute_centrality.py` — Community Detection Louvain (M5)

La Community Detection Louvain, ejecutada sobre el grafo constitucional con 37 nodos y 55 aristas, produjo el siguiente resultado sin ninguna instrucción sobre agrupamiento:

```
Comunidad 0: CE_1, CE_226, CE_95, CE_18, CE_264
```

Los 5 NRCs (4 funcionales + 1 constituyente) fueron agrupados en su propia comunidad separada de todos los dominios operacionales y ACKs sectoriales. Nadie programó ese agrupamiento — el algoritmo lo descubrió.

**Cohesión interna NRC Community 0:**
- 7 relaciones directas entre 5 nodos (CONSTITUYE + HABILITA)
- Densidad = 7/20 = 35% de todas las relaciones posibles
- Umbral Louvain típico para cluster significativo: ~10-15%

**Implicación para ADR-018**: La tesis original era **estructural** ("NRCs son nodos cuya eliminación rompe 2+ dominios independientes"). La observación O-02 es **empírica**: los NRCs son estructuralmente tan cohesivos entre sí que forman una comunidad computacionalmente distinguible sin guía humana.

Esto es más fuerte. La tesis de ADR-018 describe el CRITERIO para ser NRC. O-02 describe la PROPIEDAD EMERGENTE que ese criterio produce.

**Conclusión O-02**: Los NRC no son únicamente nodos raíz. Constituyen una comunidad constitucional computacionalmente detectable. La arquitectura normativa ecuatoriana, al menos en el subconjunto cargado, tiene una capa constitucional diferenciada que el grafo revela por sí mismo.

Ver: `docs/adr/ADR-019_Dominios_Legitimacion_Democratica.md` — Observación O-02.

---

*ADR-018 v1.0 · QUIRA Gov · Dylus Lab © 2026*  
*"QUIRA no impone una teoría de gobernanza — revela la que el ordenamiento jurídico ya diseñó."*  
*Propuesto: colega asesor + Javo · Formalizado: 2026-06-02*  
*Observación O-02 agregada: 2026-06-02 — Community detection confirmó cohesión constitucional*
