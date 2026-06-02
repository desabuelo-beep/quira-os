# ACK Registry — Catálogo Maestro de Conocimiento Jurídico

**Versión:** 0.1 (diseño — NO implementado)  
**Fecha:** 2026-06-01  
**Estado:** DISEÑO PENDIENTE IMPLEMENTACIÓN  
**Autores:** Dylus Lab · Colega asesor  
**Relacionado:** QLEP v1.0 · ADR-016 (DCO) · ADR-017 (Circuitos)

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
| CE_18 | Dom07 | ✅ | Pendiente |
| CE_61 | Dom07-B | ✅ | Pendiente |
| CE_95 | Dom07-B | ✅ | Pendiente |
| CE_100 | Dom07-B | ✅ | Pendiente |
| LOTAIP_7 | Dom07-A | — | Pendiente |
| LOTAIP_34 | Dom07-A | — | Pendiente |
| LOTAIP_47 | Dom07-A | — | Pendiente |
| LOPC_72 | Dom07-B | — | Pendiente |
| CE_264 | Dom10 | ✅ | Pendiente |
| COOTAD_249 | Dom12 | ✅ | Pendiente |

---

## Relación con el colega asesor — cita exacta

> "Todavía no existe una entidad formal que gobierne los ACKs. Necesitas algo así como un catálogo maestro de conocimiento jurídico. Ese registro se convierte en el árbitro entre corpus y gobernanza."

El ACK Registry es esa entidad. Junto con el DCO (ADR-016), resuelve el problema que el colega identificó: sin este catálogo, el corpus crece en tamaño documental pero no en tamaño estructural.

---

## Próximos pasos

1. [ ] Decidir Opción A vs C para implementación
2. [ ] Script `register_ack.py` (lectura de YAML QLEP → registry)
3. [ ] Carga inicial: CE_18 + 9 ACKs prioritarios de Dom07 y circuitos activos
4. [ ] Integrar verificación en QLEP: antes de extraer un ACK, revisar si ya existe en registry
5. [ ] Campo `chunk_refs` — cruzar sha256 del registry con normativa_corpus para validar cobertura

---

*ACK Registry Design v0.1 · QUIRA Gov · Dylus Lab © 2026*  
*Siguiente: implementación scripts/normativa/register_ack.py*
