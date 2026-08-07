# ACK Registry — Catálogo Maestro de Conocimiento Jurídico

**Versión:** 0.2 (implementado — carga inicial 10 ACKs)  
**Fecha:** 2026-06-01  
**Estado:** ACTIVO — carga inicial completa · chunk_refs pendientes · revisión experto pendiente  
**Autores:** Dylus Lab · Colega asesor  
**Relacionado:** QLEP v1.0 · ADR-016 (DCO) · ADR-017 (Circuitos)

---

## Principio de Alcance Nacional (INMUTABLE)

Los ACKs son normativa constitucional y orgánica aplicable a **todos los GADs municipales del Ecuador**. El campo `canton_id` **no existe por diseño de arquitectura**.

```
La normativa es NACIONAL         → ACK Registry
Los datos operacionales son CANTONALES → L0 (Excel Canónico)

El mismo CE_18 aplica a Quito, Guayaquil, Cuenca y Montecristi.
Lo que cambia canton a canton: ¿están cumpliendo con CE_18?
```

**Laboratorio:** GADMCM — Cantón Montecristi (modelado y validación)  
**Destino:** 222 municipios del Ecuador  

Esta separación no es accidental — es la razón por la que la arquitectura escala.  
Si se agrega `canton_id` a un ACK, se rompe este principio y el código lo rechazará.

### Tipos de GAD en Ecuador — implicaciones para el ACK Registry

Ecuador tiene cuatro tipos de GAD (CE Art.238):

| Tipo | Base CE | Ejemplo | Scope actual QUIRA |
|---|---|---|---|
| GAD Municipal | Art.264 | 220 cantones (Montecristi, Guayaquil, Cuenca...) | ✅ ACTIVO |
| Distrito Metropolitano | Art.266 | Quito (Distrito Metropolitano) | 🔵 Futuro |
| GAD Provincial | Art.263 | 24 provincias | 🔵 Futuro |
| GAD Parroquial Rural | Art.267 | 800+ parroquias rurales | 🔵 Futuro |

**Quito no es un GAD Municipal ordinario.** Es un Distrito Metropolitano (CE Art.258) que:
- Tiene todas las competencias del Art.264 (GAD Municipal)
- **ADEMÁS** tiene competencias ampliadas del Art.266 (exclusivas del Distrito)
- Usa "Concejo Metropolitano" en lugar de "Concejo Municipal"

**Implicación para ACK Registry:**
- `CE_264` es válido para Quito — aplica el mismo artículo
- Quito adicionalmente necesita `ACK CE_266` (no creado aún — scope futuro)
- `canton_id` sigue siendo arquitectónicamente imposible — la normativa aplica igual

```
El mismo CE_18 aplica a Quito Y a Montecristi.
Lo que cambia: Quito tiene CE_264 + CE_266 como normas fundantes,
               Montecristi solo tiene CE_264.
```

Esta distinción no rompe el Principio de Alcance Nacional — lo enriquece. El Kernel Nacional tiene dos variantes para competencias: GAD Municipal (la mayoría) y GAD Metropolitano (Quito). Ambas son nacionales; ninguna es cantonal.

---

## El problema que resuelve

Con el corpus normativo completo (7,740 chunks) y el DCO template (ADR-016), surge una brecha:

```
Corpus normativo           → 7,740 chunks semánticos (Cerebro 1)
ACKs producidos por QLEP   → YAML + Obsidian (existentes, sin catálogo)
DCO (ADR-016)              → referencia ACK IDs (CE_18, LOTAIP_7, etc.)
QTMP                       → referencia ACK IDs implícitamente
```

No existe ningún artefacto que sea **el catálogo formal de todos los ACKs existentes**. Cuando el DCO de Dom08 necesite saber si CE_95 ya está extraído, no hay dónde buscar excepto en los archivos YAML de QLEP.

El ACK Registry es ese catálogo.

---

## Analogía con el Excel Canónico

```
Excel Canónico  →  fuente de verdad de indicadores y fórmulas
ACK Registry    →  fuente de verdad de átomos jurídicos
```

El Excel Canónico no calcula desde cero cada vez — tiene una tabla de definiciones que todos los módulos consultan. El ACK Registry hace lo mismo para el conocimiento jurídico.

---

## La diferencia entre tamaño documental y tamaño estructural

(Señalado por el colega asesor — insight crítico)

| Tipo | Descripción | Resultado |
|---|---|---|
| **Documental** | +leyes, +chunks, +documentos | Mejor búsqueda semántica (Cerebro 1) |
| **Estructural** | +ACKs, +DCOs, +Circuitos | Mejor razonamiento institucional (Cerebro 2) |

```
Sistema con 10,000 normas y 0 circuitos = buscador sofisticado
Sistema con 500 normas y 50 circuitos   = motor de gobernanza
```

El corpus (Cerebro 1) da tamaño documental. Los ACKs + DCOs + Circuitos dan tamaño estructural. QUIRA crece en el segundo eje.

---

## Schema del ACK Registry

```yaml
ack_id: CE_18                    # formato: SIGLA_ARTICULO[_INCISO]
                                  # Ejemplos: CE_18 / LOTAIP_7 / LOTAIP_34_a / COOTAD_302

tipo: DERECHO                    # taxonomía cerrada (ver QLEP v1.0):
                                  # principio | competencia_exclusiva | competencia_concurrente
                                  # obligacion | derecho | prohibicion | procedimiento
                                  # plazo | sancion | distribucion | definicion

nombre: "Derecho de acceso a información pública"

norma:
  sigla: CE
  nombre_oficial: "Constitución del Ecuador"
  articulo: "18"
  inciso: null                   # null si aplica al artículo completo
  jerarquia: 0                   # 0=CE, 1=LO, 2=Reglamento, 3=Plan, 4=Local, 5=Pronunciamiento
  vigente: "2008-10-20"          # fecha de última reforma aplicable

dominios:                        # 1+ dominios que este ACK ancla
  - Dom07
  - Dom08

circuitos:                       # circuitos donde este ACK es nodo
  - C01

fundante: true                   # true = norma que CREA la obligación (no solo la desarrolla)
es_nrc: false                    # true = Nodo Raíz Constitucional (ver ADR-018)
                                  # Criterio: su remoción rompe 2+ dominios independientes
                                  # Máximo esperado: 6-8 NRCs en corpus completo
vigente: true                    # false = derogado o reformado sustancialmente

revisado_por_experto: false      # true = validado por jurista (no solo por Claude)

chunk_refs:                      # sha256 de chunks correspondientes en normativa_corpus
  - sha256: "abc123..."          # chunk principal del artículo
  - sha256: "def456..."          # chunk sub-artículo (chunk_seq > 0)

obsidian_nota: "CE_18.md"        # nombre de la nota Nivel 3 en Obsidian
qlep_yaml: null                  # ruta al YAML de QLEP si existe

meta:
  fecha_extraccion: "2026-06-01"
  extractor: "QLEP-v1.0"
  version: "1.0"
```

---

## Nodos Raíz Constitucionales (NRC) — ADR-018

*(Categoría formal introducida 2026-06-02 · v0.2 del registry)*

### La distinción

```
ACK normal → funda un dominio
ACK raíz   → funda múltiples dominios simultáneamente
```

Un ACK es NRC si su eliminación rompe la base normativa de 2 o más dominios **independientes**. El criterio es deliberadamente conservador. Máximo esperado: 6-8 NRCs en el corpus completo.

### NRCs actuales (registry v0.2 · 4 confirmados)

| ACK | Nombre | Por qué es raíz |
|---|---|---|
| `CE_226` | Principio de Legalidad | Axioma del sistema — toda actuación pública requiere habilitación. Sin él, ningún dominio tiene fundamento constitucional |
| `CE_18` | Derecho a información | Dom07 (primario) + Dom08 (participación informada) + Dom09 (rendición) + Dom02 (presupuesto) |
| `CE_95` | Participación protagónica | Dom08 (primario) + Dom07 lado demanda + Dom09 mecanismo control |
| `CE_264` | Competencias GAD Municipal | Dom04 (planificación) + Dom10 (agua) + Dom02 (presupuesto) + Dom03 (contratación) |

### La jerarquía extendida

```
NRC (axioma constitucional)
  ↓
ACK normal (operacionalización normativa)
  ↓
DCO (dominio como sistema de razonamiento)
  ↓
Circuito (cadena causal multi-dominio)
  ↓
Diagnóstico
```

### Consultas CLI

```bash
python scripts/normativa/register_ack.py --filter-nrc
python scripts/normativa/register_ack.py --stats   # muestra NRCs: 4/11
python scripts/normativa/register_ack.py --traverse CE_226
```

---

## Implementación — 3 opciones (decisión pendiente)

### Opción A — JSON en repositorio (RECOMENDADA para v0)
```
quira-os/data/ack_registry.json
```
- Versionado en git ✅
- Fácil de editar manualmente ✅
- Sin latencia de red ✅
- Sin búsqueda semántica ❌ (solo búsqueda por ID)
- Escalable hasta ~2,000 ACKs ✅

### Opción B — Tabla Supabase (para v1 productivo)
```sql
CREATE TABLE ack_registry (
  ack_id TEXT PRIMARY KEY,
  tipo TEXT NOT NULL,
  nombre TEXT NOT NULL,
  norma_sigla TEXT NOT NULL,
  norma_articulo TEXT NOT NULL,
  norma_jerarquia INTEGER NOT NULL,
  norma_vigente TEXT NOT NULL,
  dominios TEXT NOT NULL DEFAULT '[]',    -- JSON array
  circuitos TEXT NOT NULL DEFAULT '[]',   -- JSON array
  fundante BOOLEAN DEFAULT FALSE,
  vigente BOOLEAN DEFAULT TRUE,
  revisado_por_experto BOOLEAN DEFAULT FALSE,
  chunk_refs TEXT NOT NULL DEFAULT '[]',  -- JSON array de sha256
  obsidian_nota TEXT,
  qlep_yaml TEXT,
  fecha_extraccion TEXT NOT NULL,
  extractor TEXT NOT NULL DEFAULT 'QLEP-v1.0',
  version TEXT NOT NULL DEFAULT '1.0'
);

CREATE INDEX idx_ack_dominio ON ack_registry USING gin(dominios::jsonb);
CREATE INDEX idx_ack_circuito ON ack_registry USING gin(circuitos::jsonb);
CREATE INDEX idx_ack_tipo ON ack_registry (tipo);
CREATE INDEX idx_ack_sigla ON ack_registry (norma_sigla);
```

### Opción C — Híbrido (JSON como fuente, Supabase como runtime)
- JSON = fuente de verdad (git)
- Script de sync: `scripts/normativa/sync_ack_registry.py`
- Supabase = para queries rápidas desde Sentinel

**Recomendación:** Empezar con Opción A (JSON). Migrar a C cuando el registry tenga 50+ ACKs.

---

## Cómo se puebla el registry

El ACK Registry no se llena manualmente desde cero. Se alimenta desde tres fuentes:

### Fuente 1 — QLEP outputs
Cada vez que `/qlep` produce un ACK en YAML, el output incluye los campos necesarios para registrarlo. El comando de registro sería:
```bash
python scripts/normativa/register_ack.py --from-qlep data/acks/CE_18.yaml
```

### Fuente 2 — DCOs (ADR-016)
Cada DCO lista los `acks_clave` de su dominio. El registro inicial del dominio carga esos ACKs:
```bash
python scripts/normativa/register_ack.py --from-dco docs/adr/ADR-016_*.md
```

### Fuente 3 — QTMP chains
Los circuitos QTMP referencian ACKs implícitamente. Al formalizar un circuito (ADR-017), los ACKs relevantes se registran.

---

## Consultas clave que el registry habilita

```python
# ¿Qué ACKs anclan Dom07?
acks_dom07 = registry.filter(dominios__contains="Dom07", fundante=True)

# ¿Ce_18 está revisado por experto?
ce_18 = registry.get("CE_18")
print(ce_18.revisado_por_experto)  # False → necesita revisión jurista

# ¿Qué circuitos tiene CE_18?
print(ce_18.circuitos)  # ["C01"]

# ¿Qué chunks de corpus corresponden a LOTAIP_7?
lotaip_7 = registry.get("LOTAIP_7")
chunks = db.query(normativa_corpus).filter(sha256__in=lotaip_7.chunk_refs)
```

---

## El flujo correcto de razonamiento QUIRA (actualizado con registry)

```
Pregunta jurídico-institucional
           ↓
    Cerebro 1 (corpus)
    "¿Qué dice la norma?"
           ↓
    ACK Registry
    "¿Existe ya un ACK para este artículo?"
           ↓ Sí                    ↓ No
    Usar ACK existente        Producir ACK via /qlep
           ↓                       ↓
    DCO (ADR-016)             Registrar en registry
    "¿Cuál es la norma fundante?"
           ↓
    QTMP + Circuitos (Cerebro 2)
    "¿Quién debe hacer qué?"
           ↓
    Diagnóstico Territorial
```

---

## Prioridad de carga inicial

Los primeros ACKs a registrar (basados en DCO Dom07 y los circuitos activos):

| ACK ID | Dominio | Fundante | Estado |
|---|---|---|---|
| CE_18 | Dom07 | ✅ | ✅ CARGADO · confianza alta · chunk_refs pendiente |
| CE_61 | Dom07-B | ✅ | ✅ CARGADO · confianza media · pendiente jurista |
| CE_95 | Dom07-B | ✅ | ✅ CARGADO · confianza media-alta · pendiente jurista |
| CE_100 | Dom07-B | ✅ | ✅ CARGADO · confianza media · pendiente jurista |
| LOTAIP_7 | Dom07-A | — | ✅ CARGADO · confianza alta · chunk_refs pendiente |
| LOTAIP_34 | Dom07-A | — | ✅ CARGADO · confianza media-alta |
| LOTAIP_47 | Dom07-A | — | ✅ CARGADO · confianza media · pendiente jurista |
| LOPC_72 | Dom07-B | — | ✅ CARGADO · confianza media · pendiente jurista |
| CE_264 | Dom10/Dom04 | ✅ | ✅ CARGADO · confianza alta · sub-ACKs CE_264_1/264_4 pendientes |
| COOTAD_249 | Dom12 | ✅ | ✅ CARGADO · confianza alta · dato SIGEF verificado |

---

## Relación con el colega asesor — cita exacta

> "Todavía no existe una entidad formal que gobierne los ACKs. Necesitas algo así como un catálogo maestro de conocimiento jurídico. Ese registro se convierte en el árbitro entre corpus y gobernanza."

El ACK Registry es esa entidad. Junto con el DCO (ADR-016), resuelve el problema que el colega identificó: sin este catálogo, el corpus crece en tamaño documental pero no en tamaño estructural.

---

## Estado de implementación (2026-06-01 · post-carga-inicial)

```
data/ack_registry.json          ✅ OPERACIONAL — 10 ACKs · 8/10 chunk_refs
scripts/normativa/register_ack.py ✅ OPERACIONAL — CLI completo + encoding UTF-8
  --stats         OK — hito COMPLETADO visible
  --validate-all  OK — todos válidos · canton_id guardrail activo
  --traverse      OK — LOTAIP_7 → Dom07 → C01/C02 → Neo4j-ready ✅
  --link-corpus   OK — 8/10 operacional · LOTAIP_47/LOPC_72 corpus gaps documentados

Corpus gaps (no bloquean arquitectura):
  LOTAIP_47: Art.47 no en corpus F0.x — verificar artículo real
  LOPC_72:   LOPC no ingresada en F0.2 — re-ingestar

Opción A (JSON) IMPLEMENTADA para v0.
Migrar a Opción C (JSON + Supabase sync) cuando registry tenga 50+ ACKs.
```

## Próximos pasos

1. [x] Decidir Opción A vs C → RESUELTO: Opción A implementada
2. [x] Script `register_ack.py` → COMPLETADO: CLI completo con --stats/--get/--filter/--link-corpus/--traverse/--validate-all
3. [x] Carga inicial: 10 ACKs prioritarios → COMPLETADO en data/ack_registry.json
4. [x] chunk_refs: 8/10 completado · LOTAIP_47/LOPC_72 corpus gaps documentados
5. [x] **Primer hito operacional: COMPLETADO** — LOTAIP_7 → Dom07 → C01/C02 → traversal ✅
6. [ ] C01 → Neo4j: cargar Cypher de ADR-017 (prerequisito CHS live)
7. [ ] Dom08 DCO: usar ADR-016 template · norma fundante CE_95 · Triángulo P-02
8. [ ] Dom07 Layer 2: p07_transparencia.py con corpus + ACK Registry activo
9. [ ] Revisión jurista: CE_61 · CE_95 · CE_100 · LOPC_72 · LOTAIP_34 · LOTAIP_47
10. [ ] Sub-ACKs: CE_264_1 (planificación) + CE_264_4 (agua potable)
11. [ ] ACK CE_266: competencias adicionales Distrito Metropolitano Quito (futuro)
12. [ ] Integrar verificación en QLEP: antes de extraer, revisar si ACK ya existe

---

*ACK Registry v0.2 · QUIRA Gov · Dylus Lab © 2026*  
*Laboratorio: Montecristi · Destino: 222 municipios Ecuador*  
*Primer hito operacional: COMPLETADO 2026-06-01 — LOTAIP_7 → Dom07 → C01/C02*
