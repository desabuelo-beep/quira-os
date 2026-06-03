# Schema Canónico del Chunk — QUIRA Corpus Semántico Gobernado
## Dylus Lab · Motor de Trazabilidad Pública Municipal

**Versión**: 1.1  
**Fecha**: 2026-06-02  
**Estado**: EJECUTADO — Gate 6.1b aplicado en Supabase  
**Referencia**: ADR-021 (Ontología Corpus 4 Capas)

> Este documento es la especificación técnica del schema canónico del corpus.  
> El principio rector: **un schema diseñado una vez, no migrado cinco veces**.  
> El colega asesor: *"La decisión más importante es diseñar el schema completo antes  
> de ejecutar — dentro de 6 meses van a querer que el sistema sepa automáticamente  
> qué tiene más autoridad."*

---

## 1. Schema Actual (normativa_corpus — 17 columnas, 8,351 chunks)

```sql
CREATE TABLE normativa_corpus (
    id               BIGSERIAL PRIMARY KEY,
    norma_sigla      TEXT NOT NULL,          -- "COOTAD", "LOPC", etc.
    norma_nombre     TEXT NOT NULL,          -- nombre completo
    jerarquia        INTEGER,                -- 0-5 (escala propia QUIRA)
    milestone_qlep   TEXT,                   -- "F0.1".."F0.8"
    tipo_documento   TEXT,                   -- "ley_organica", "guia", etc.
    articulo_num     TEXT,                   -- "Art. 266", nullable
    articulo_raw     TEXT,                   -- título del artículo, nullable
    chunk_seq        INTEGER,                -- secuencia dentro del documento
    contenido        TEXT NOT NULL,          -- texto del chunk
    palabras         INTEGER,                -- conteo de palabras
    dominios_quira   TEXT,                   -- "Dom07,Dom08" (CSV)
    sha256           TEXT UNIQUE NOT NULL,   -- hash del contenido
    embedding        VECTOR(384),            -- paraphrase-multilingual-MiniLM-L12-v2
    archivo_nombre   TEXT,                   -- nombre del archivo fuente
    archivo_sha256   TEXT,                   -- hash del archivo completo
    ingestado_at     TEXT,                   -- ISO timestamp
    ingestado_por    TEXT                    -- "qlep-corpus-v1.0"
);
```

---

## 2. Schema Canónico v2.0 (diseño Gate 6.1b — 8 columnas nuevas)

### 2.1 Columnas nuevas — Clasificación Ontológica

```sql
-- Capa del corpus (ADR-021)
document_class    TEXT CHECK (document_class IN (
                    'NORMA',                    -- Capa A: obliga
                    'METODOLOGIA',              -- Capa B: explica cómo cumplir
                    'INSTRUMENTO_TERRITORIAL',  -- Capa C: planifica y ejecuta
                    'EVIDENCIA_OBSERVACIONAL'   -- Capa D: ciudadanía observó
                  )),

-- Autoridad epistemológica (10-100)
authority_level   INTEGER CHECK (authority_level BETWEEN 10 AND 100),

-- Entidad que produjo el documento
source_entity     TEXT,    -- ver catálogo §2.3

-- GAD-específico (NULL para normas nacionales)
canton_id         TEXT DEFAULT NULL,   -- 'MCR', 'GYE', 'UIO', etc.

-- Circuitos constitucionales que aplican
circuit_refs      TEXT[],   -- ['C01', 'C02', 'Circuito_RC_001']

-- Tipo de evidencia (solo Capa D)
evidence_type     TEXT CHECK (evidence_type IN (
                    'RC_INFORME',       -- Informe Rendición de Cuentas
                    'PP_INFORME',       -- Informe Presupuesto Participativo
                    'EDV',             -- Evidencia Digital Verificable (videos)
                    'SIGAD_ICM',       -- Reporte ICM SIGAD
                    'LOTAIP_DATOS',    -- Conjunto datos LOTAIP
                    NULL               -- para Capas A, B, C
                  )),

-- Vigencia temporal
valid_from        DATE,    -- fecha de entrada en vigor
valid_to          DATE,    -- NULL si sigue vigente

-- Metadatos flexibles (overflow para futuras extensiones)
metadata_json     JSONB DEFAULT '{}'
```

### 2.2 ALTER TABLE completo (ejecutar Gate 6.1b)

```sql
-- Paso 1: agregar columnas (nullable — no rompe rows existentes)
ALTER TABLE normativa_corpus
    ADD COLUMN IF NOT EXISTS document_class   TEXT,
    ADD COLUMN IF NOT EXISTS authority_level  INTEGER,
    ADD COLUMN IF NOT EXISTS source_entity    TEXT,
    ADD COLUMN IF NOT EXISTS canton_id        TEXT DEFAULT NULL,
    ADD COLUMN IF NOT EXISTS circuit_refs     TEXT[],
    ADD COLUMN IF NOT EXISTS evidence_type    TEXT,
    ADD COLUMN IF NOT EXISTS valid_from       DATE,
    ADD COLUMN IF NOT EXISTS valid_to         DATE,
    ADD COLUMN IF NOT EXISTS metadata_json    JSONB DEFAULT '{}';

-- Paso 2: agregar constraints CHECK
ALTER TABLE normativa_corpus
    ADD CONSTRAINT chk_document_class CHECK (
        document_class IN ('NORMA','METODOLOGIA',
                           'INSTRUMENTO_TERRITORIAL','EVIDENCIA_OBSERVACIONAL')
    ),
    ADD CONSTRAINT chk_authority_level CHECK (authority_level BETWEEN 10 AND 100),
    ADD CONSTRAINT chk_evidence_type CHECK (
        evidence_type IN ('RC_INFORME','PP_INFORME','EDV','SIGAD_ICM','LOTAIP_DATOS')
        OR evidence_type IS NULL
    );

-- Paso 3: índices de consulta
CREATE INDEX IF NOT EXISTS idx_corpus_document_class  ON normativa_corpus(document_class);
CREATE INDEX IF NOT EXISTS idx_corpus_authority_level ON normativa_corpus(authority_level);
CREATE INDEX IF NOT EXISTS idx_corpus_canton_id       ON normativa_corpus(canton_id);
CREATE INDEX IF NOT EXISTS idx_corpus_circuit_refs    ON normativa_corpus USING GIN(circuit_refs);
```

### 2.3 Catálogo source_entity

| Código | Entidad | Nivel |
|---|---|---|
| `CONST_EC` | Constitución del Ecuador | Nacional |
| `ASAMBLEA_NAC` | Asamblea Nacional | Nacional |
| `EJ_EJECUTIVO` | Ejecutivo Nacional | Nacional |
| `SNP` | Secretaría Nacional de Planificación | Nacional |
| `CPCCS` | Consejo de Participación Ciudadana y Control Social | Nacional |
| `CGE` | Contraloría General del Estado | Nacional |
| `CNE` | Consejo Nacional Electoral | Nacional |
| `SERCOP` | Servicio Nacional de Contratación Pública | Nacional |
| `MDT` | Ministerio de Trabajo | Nacional |
| `MEF` | Ministerio de Economía y Finanzas | Nacional |
| `ONU` | Organización de las Naciones Unidas | Internacional |
| `OEA` | Organización de Estados Americanos | Internacional |
| `GAD_MCR` | GAD Municipal de Montecristi | Cantonal |
| `EP_ASEO_MCR` | EP de Aseo del Cantón Montecristi | Cantonal |
| `BOMBEROS_MCR` | Cuerpo de Bomberos Montecristi | Cantonal |
| `PATRONATO_MCR` | Patronato Municipal Montecristi | Cantonal |

---

## 3. Reglas de Resolución de Conflictos

### 3.1 Cuando dos chunks responden la misma consulta

```python
# Pseudocódigo del resolver
def resolver_autoridad(chunks: list) -> list:
    """Ordena chunks por autoridad epistemológica."""
    return sorted(chunks, key=lambda c: c.authority_level, reverse=True)
    # Resultado: COOTAD (95) antes que POA (40) antes que RC (28)
```

### 3.2 Regla canon: authority_level gana en conflicto

Si chunk A (authority=95) dice "el GAD DEBE hacer X"  
y chunk B (authority=35) dice "el GAD no planificó X para 2024":  
→ No es contradicción. Es un **GAP detectado** (tipo A≠C).

Los tres gaps que QUIRA detecta:

| Gap | Señal | Pregunta |
|---|---|---|
| `A≠C` | Norma obliga pero no aparece en POA/PAC | ¿El municipio no planificó lo que la ley manda? |
| `C≠D` | POA planificó pero no hay evidencia ciudadana | ¿Lo ejecutó sin que nadie lo observara? |
| `A≠D` | Norma obliga pero no hay evidencia de cumplimiento | ¿Nunca se cumplió? |

---

## 4. Cambios a manifest.py (Gates 6.3 y 6.4)

### 4.1 Nuevos campos por entrada del MANIFEST

```python
# Campos adicionales para cada documento del MANIFEST
{
    # -- existentes (no cambiar) --
    "archivo":         "COOTAD.docx",
    "sigla":          "COOTAD",
    "nombre":         "Código Orgánico...",
    "jerarquia":      1,
    "milestone":      "F0.3",
    "tipo":           "ley_organica",
    "dominios":       ["Dom01",...],
    "vigente":        True,

    # -- NUEVOS (Gate 6.1b) --
    "document_class":  "NORMA",              # A/B/C/D
    "authority_level": 95,                   # 10-100
    "source_entity":   "ASAMBLEA_NAC",       # catálogo §2.3
    "canton_id":       None,                 # None para normas nacionales
    "circuit_refs":    ["C01","C02"],         # circuitos aplicables
    "evidence_type":   None,                 # solo Capa D
    "valid_from":      "2010-10-19",         # fecha promulgación
    "valid_to":        None,                 # None = vigente
}
```

### 4.2 Migración de 43 documentos existentes (tabla de mapping)

| Sigla | document_class | authority | source_entity | canton_id | circuit_refs |
|---|---|---|---|---|---|
| CE | NORMA | 100 | CONST_EC | NULL | C01,C02,C03 |
| LOTAIP | NORMA | 95 | ASAMBLEA_NAC | NULL | C01 |
| RLOTAIP | NORMA | 80 | EJ_EJECUTIVO | NULL | C01 |
| GUIA-LOTAIP-MEC | METODOLOGIA | 55 | SNP | NULL | C01 |
| GUIA-LOTAIP-ENT | METODOLOGIA | 55 | SNP | NULL | C01 |
| LOPC | NORMA | 95 | ASAMBLEA_NAC | NULL | C01,C02 |
| COD | NORMA | 95 | ASAMBLEA_NAC | NULL | C01 |
| RCOD | NORMA | 80 | CNE | NULL | C01 |
| COOTAD | NORMA | 95 | ASAMBLEA_NAC | NULL | C01,C02,C03 |
| COOTAD-2026 | NORMA | 95 | ASAMBLEA_NAC | NULL | C01,C02 |
| COPLAFIP | NORMA | 95 | ASAMBLEA_NAC | NULL | C02,C03 |
| RCOPLAFIP | NORMA | 80 | EJ_EJECUTIVO | NULL | C02,C03 |
| PND-2025 | METODOLOGIA | 50 | SNP | NULL | [] |
| ACUERDO-PDOT-2023 | METODOLOGIA | 65 | SNP | NULL | [] |
| LINEAMIENTOS-PDOT-2023 | METODOLOGIA | 65 | SNP | NULL | [] |
| LINEAMIENTOS-PFI | METODOLOGIA | 60 | SNP | NULL | [] |
| LOTUGS | NORMA | 95 | ASAMBLEA_NAC | NULL | [] |
| LOC-CGE | NORMA | 95 | ASAMBLEA_NAC | NULL | C01,C03 |
| NCI-CGE | NORMA | 80 | CGE | NULL | C01,C03 |
| CONA | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |
| LODISC | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |
| LOPAM | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |
| LMH | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |
| LPEVM | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |
| CEDAW | NORMA | 70 | ONU | NULL | [] |
| CADH | NORMA | 70 | OEA | NULL | [] |
| CDN | NORMA | 70 | ONU | NULL | [] |
| PIDESC | NORMA | 70 | ONU | NULL | [] |
| LOSNCP | NORMA | 95 | ASAMBLEA_NAC | NULL | C03 |
| RLOSNCP | NORMA | 80 | EJ_EJECUTIVO | NULL | C03 |
| LOSEP | NORMA | 95 | ASAMBLEA_NAC | NULL | [] |
| RLOSEP | NORMA | 80 | EJ_EJECUTIVO | NULL | [] |
| COA | NORMA | 95 | ASAMBLEA_NAC | NULL | [] |
| COA-AMB | NORMA | 95 | ASAMBLEA_NAC | NULL | [] |
| RCOA-AMB | NORMA | 80 | EJ_EJECUTIVO | NULL | [] |
| LOTD | NORMA | 95 | ASAMBLEA_NAC | NULL | [] |
| CLASP-2026 | NORMA | 65 | MEF | NULL | C02,C03 |
| RES-ORG-GADMCM-2025 | NORMA | 75 | GAD_MCR | MCR | [] |
| RES-CPCCS-RC-2026 | NORMA | 75 | CPCCS | NULL | C01 |
| PDOT-MONTECRISTI | INSTRUMENTO_TERRITORIAL | 48 | GAD_MCR | MCR | C01,C02,C03 |
| PLAN-GOB-MCR | INSTRUMENTO_TERRITORIAL | 15 | GAD_MCR | MCR | C01,C02 |
| PAGCC-2024 | METODOLOGIA | 50 | EJ_EJECUTIVO | NULL | C01,C02 |
| LOIEME | NORMA | 92 | ASAMBLEA_NAC | NULL | [] |

---

## 5. Tabla holding_structured_data (nueva — Gate 6.5)

Para los archivos XLSX/CSV del Holding (conjuntos de datos LOTAIP Numeral 6 + presupuestos tabulares). **NO van a normativa_corpus** — son datos estructurados.

```sql
CREATE TABLE holding_structured_data (
    id             BIGSERIAL PRIMARY KEY,
    source_entity  TEXT NOT NULL,       -- 'GAD_MCR', 'EP_ASEO_MCR', etc.
    canton_id      TEXT NOT NULL,       -- 'MCR'
    document_class TEXT NOT NULL,       -- 'INSTRUMENTO_TERRITORIAL' o 'EVIDENCIA_OBSERVACIONAL'
    authority_level INTEGER,
    evidence_type  TEXT,                -- 'LOTAIP_DATOS', 'RC_INFORME', etc.
    periodo        TEXT,                -- '2025-01', '2025-Q1', '2025', etc.
    archivo_nombre TEXT,
    archivo_sha256 TEXT,
    datos_json     JSONB,               -- contenido estructurado
    ingestado_at   TEXT,
    ingestado_por  TEXT
);
```

---

## 6. Tabla evidencia_digital_verificable (ya existe — ajustar)

El archivo `data/evidencia_digital_verificable.json` ya existe para EDVs (videos RC/PP).  
Cuando sea necesario escalar, migrar a tabla Supabase:

```sql
CREATE TABLE evidencia_digital_verificable (
    id              BIGSERIAL PRIMARY KEY,
    edv_id          TEXT UNIQUE,        -- 'EDV_RC_2025_MCR', etc.
    source_entity   TEXT,               -- 'GAD_MCR'
    canton_id       TEXT,               -- 'MCR'
    evidence_type   TEXT DEFAULT 'EDV',
    authority_level INTEGER DEFAULT 10,
    url             TEXT,               -- YouTube, plataforma oficial
    titulo          TEXT,
    evento_fecha    DATE,
    periodo_gestion TEXT,               -- '2025' (año de gestión rendido)
    cpccs_url       TEXT,               -- informe CPCCS relacionado
    cpccs_calificacion TEXT,
    chunk_ref_sha256 TEXT,              -- vincula a normativa_corpus.sha256
    metadata_json   JSONB DEFAULT '{}'
);
```

---

## 7. Compatibilidad hacia atrás

### Reglas para el pipeline de ingesta existente

1. **`ingest.py` no se rompe**: todas las columnas nuevas son nullable. La inserción existente sigue funcionando con `ON CONFLICT (sha256) DO NOTHING`.

2. **Migración de datos existentes**: script `scripts/normativa/migrate_schema_v2.py` (a crear en Gate 6.1b) — actualiza las 43 entradas con los valores de la tabla §4.2.

3. **`manifest.py`**: los nuevos campos se agregan como opcionales con defaults None. Los documentos existentes no fallan si no tienen los nuevos campos — el pipeline los llenará con NULL.

---

## 7b. La Bifurcación Resuelta — ¿documents o chunks?

**Pregunta del colega**: ¿document_class y authority_level viven en chunks o en documents?

**Respuesta**: **Ambos — Star Schema intencional.**

```
documents (dimension table)
    1 fila por documento
    Fuente de verdad para document_class, authority_level
    Reclasificar = 1 UPDATE aquí
         ↓ FK
normativa_corpus (fact table)
    1 fila por chunk
    Copia denormalizada: document_class, authority_level
    Performance: pgvector WHERE sin JOIN
    circuit_refs: SOLO aquí (chunk-level — distintos artículos tocan distintos circuitos)
```

**Por qué denormalizar en chunks también:**
El índice pgvector (IVFFlat) hace búsqueda vectorial + WHERE en una sola tabla. Sin denormalización, cada query necesitaría un JOIN que destruye la performance de búsqueda semántica.

**Cuándo actualizar la copia en chunks:**
```sql
-- Reclasificar un documento:
UPDATE documents SET document_class='METODOLOGIA', authority_level=60
WHERE norma_sigla='GUIA-X';

-- Propagar a chunks (script o trigger):
UPDATE normativa_corpus nc
SET document_class='METODOLOGIA', authority_level=60
FROM documents d
WHERE nc.document_id = d.document_id
AND d.norma_sigla='GUIA-X';
```

**circuit_refs es SOLO chunk-level:**
```
COOTAD Art.266  → circuit_refs=['C01','C02','C03']  ← RC + presupuesto + planificación
COOTAD Art.302  → circuit_refs=['C01','C03']         ← participación + planificación
```
Diferentes artículos del mismo documento tocan diferentes circuitos. Por eso NO se desnormaliza desde documents — es propiedad del artículo, no del documento.

---

## 8. Decisiones tomadas (no re-litigar)

| Decisión | Alternativa descartada | Razón |
|---|---|---|
| `circuit_refs` como TEXT[] en corpus | Solo en ACK Registry | El corpus debe poder responder "qué chunks sirven al Circuito C01" sin join |
| `authority_level` 10-100 continuo | Escala 0-5 de jerarquia | El 0-5 actual es demasiado grueso; necesitamos distinguir ley orgánica (95) de resolución (75) de ordenanza (75) |
| `canton_id` nullable (no NOT NULL) | Requerir siempre | Las normas nacionales (Capa A) no pertenecen a ningún cantón |
| `holding_structured_data` separado | Todo en normativa_corpus | Los XLSX no son texto semántico — mezclarlos destruye la relevancia del índice vectorial |
| Schema único (no tablas por capa) | Tabla_normas + tabla_instrumentos | La búsqueda semántica necesita cruzar capas en una sola query |

---

## 9. Secuencia de Ejecución Gate 6.1 (recordatorio)

```
Gate 6.1a ✅  Este documento — schema canónico diseñado
Gate 6.1b ⏳  ALTER TABLE en Supabase + constraints + índices
Gate 6.2  ⏳  Script migrate_schema_v2.py — poblar nuevas columnas en 43 docs
Gate 6.3  ⏳  Actualizar manifest.py con nuevos campos
Gate 6.4  ⏳  Ingestar Normativa_Word pendiente (Capa A/B delta)
Gate 6.5  ⏳  Ingestar Holding MCR (Capa C/D texto) + holding_structured_data
Gate 6.6  ⏳  Semantic Mining por dominio + circuitos emergentes
Gate 6.7  ⏳  Re-evaluar ADR-019 con corpus completo
```

---

*CANONICAL_CHUNK_SCHEMA v1.0 · QUIRA Gov · Dylus Lab · 2026-06-02*  
*"Una migración dolorosa futura evitada por un buen diseño hoy."*
