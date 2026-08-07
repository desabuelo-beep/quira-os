---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-021 — Ontología del Corpus: 4 Capas + authority_level

**Estado**: ACTIVO  
**Fecha**: 2026-06-02  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Participantes**: Javo (fundador), Colega (asesor), Claude (director técnico)

> **Decisión arquitectónica más importante después de la creación del grafo constitucional.**  
> Este ADR define cómo QUIRA clasifica todo documento que ingresa al sistema, estableciendo  
> la base del **Motor de Trazabilidad Pública Municipal**.

---

## Contexto

Hasta Gate 5 (ADR-019), QUIRA construyó su corpus con documentos normativos (Capa A).  
El corpus tiene 43 docs / 8,351 chunks, todos del tipo "norma" o instrumentos de planificación nacional.

Con Gate 6, el corpus crece para incluir:
- Metodologías de planificación territorial (SNP, antes SENPLADES)
- Documentos de ejecución real del Holding Municipal Montecristi (POAs, PACs, presupuestos)
- Evidencia observacional (Rendiciones de Cuentas, Presupuesto Participativo, LOTAIP)

Sin una clasificación ontológica explícita, el sistema no puede distinguir entre:
- Lo que la ley **obliga** a hacer (COOTAD_266)
- Lo que el municipio **planificó** hacer (POA 2024)
- Lo que **realmente ejecutó** (Cédula presupuestaria Dic 2024)
- Lo que la **ciudadanía observó** (Informe RC 2024)

Mezclar esos pesos epistémicos destruye la capacidad analítica de QUIRA.

---

## La Decisión — 4 Capas Ontológicas

### Capa A — Norma (obliga)
**document_class**: `NORMA`  
**authority_level**: 70–100  
**canton_id**: PROHIBIDO (norma nacional aplica a todos los GADs)  

| authority_level | Tipo | Ejemplos |
|---|---|---|
| 100 | Constitución | CE Art.264, CE Art.95, CE Art.1 |
| 95 | Ley orgánica | COOTAD, LOPC, LOTAIP, LOSNCP, COA |
| 90 | Ley ordinaria | LOSEP, Código Democracia |
| 85 | Código / Decreto | COA Reglamento, COPFP |
| 80 | Reglamento ley orgánica | Reglamento LOSNCP, Reglamento LOSEP |
| 75 | Resolución / Ordenanza | Ordenanza municipal, Resolución CPCCS |
| 70 | Instrumento internacional | CEDAW, CDN Niños, Convención Americana, PIDESC |

### Capa B — Metodología (explica cómo cumplir)
**document_class**: `METODOLOGIA`  
**authority_level**: 50–69  
**canton_id**: PROHIBIDO (metodología nacional)  

| authority_level | Tipo | Ejemplos |
|---|---|---|
| 65 | Guía SNP / Acuerdo SNP | PDOT-ACUERDO-SNP-2023-0049-A, Guía LOTAIP |
| 60 | Lineamientos técnicos | Lineamientos monitoreo planes fortalecimiento |
| 55 | Clasificadores / estándares | Clasificador presupuestario 2026 |
| 50 | Plan nacional de referencia | Plan Nacional de Desarrollo 2025-2029, PAGCC-2024 |

### Capa C — Instrumento Territorial (el municipio planificó y ejecutó)
**document_class**: `INSTRUMENTO_TERRITORIAL`  
**authority_level**: 30–49  
**canton_id**: REQUERIDO (documento específico del GAD o ente)  

| authority_level | Tipo | Ejemplos MCR |
|---|---|---|
| 48 | PDOT cantonal | PDOT Montecristi 2023-2027 Bicentenario |
| 45 | Plan Plurianual inversiones | Plan Plurianual de Inversiones GAD MCR |
| 43 | PAI (Plan Anual de Inversión) | PAI 2023, 2025, 2026 |
| 40 | POA (Plan Operativo Anual) | POA GAD/Aseo/Bomberos/Patronato 2023-2026 |
| 38 | PAC (Plan Anual de Contratación) | PAC GAD/Aseo/Bomberos/Patronato 2023-2026 |
| 35 | Cédula presupuestaria | Cédula GAD 2023, 2024, 2025 |
| 32 | Presupuesto mensual aprobado | Presupuesto Bomberos/Aseo/Patronato mensual |
| 30 | Resolución orgánica interna | Resolución 040-2025 Orgánico GADMCM |

### Capa D — Evidencia Observacional (lo que la ciudadanía observó)
**document_class**: `EVIDENCIA_OBSERVACIONAL`  
**authority_level**: 10–29  
**canton_id**: REQUERIDO  

| authority_level | Tipo | Ejemplos MCR |
|---|---|---|
| 28 | Informe Rendición de Cuentas | RC GAD/Aseo/Bomberos/Patronato 2023-2024 |
| 25 | Informe Presupuesto Participativo | PP 2024, 2025, 2026 |
| 22 | Reporte ICM SIGAD | ICM SIGAD 2023, 2024 |
| 20 | Conjuntos de datos LOTAIP | Numeral 6 mensual 2025-2026 |
| 15 | Plan de gobierno (mandato electoral) | Plan CNE Alcalde Montecristi |
| 10 | Evidencia digital verificable (EDV) | Videos RC YouTube (ver EDV registry) |

---

## Motor de Trazabilidad Pública — Identidad Formal

QUIRA es un **Motor de Trazabilidad Pública Municipal**.

Responde la cadena causal completa de una intervención pública:

```
1. Qué DEBÍA ocurrir       → Capa A (Norma) authority 70-100
        ↓
2. Cómo DEBÍA hacerse      → Capa B (Metodología) authority 50-69
        ↓
3. Qué se PLANIFICÓ        → Capa C (POA/PAC/PDOT) authority 38-48
        ↓
4. Qué se EJECUTÓ          → Capa C (Cédula/presupuesto) authority 30-35
        ↓
5. Qué observó la CIUDAD   → Capa D (RC/PP/LOTAIP) authority 10-28
        ↓
6. DÓNDE ocurrió           → GeoTwin (Layer 3 UI — proyección espacial)
        ↓
7. Qué debería pasar AFTER → Circuitos Neo4j (retroalimentación democrática)
```

**Los tres gaps que QUIRA detecta automáticamente:**

| Gap | Pregunta | Ejemplo |
|---|---|---|
| A ≠ C | ¿La norma obliga pero el municipio no lo planificó? | LOPC_77 obliga silla vacía, ¿está en el POA? |
| C ≠ D | ¿El municipio lo planificó pero sin evidencia ciudadana? | POA incluye agua barrio X, ¿aparece en PP/RC? |
| A ≠ D | ¿La norma obliga pero sin evidencia de cumplimiento? | COOTAD_266 obliga RC anual, ¿existe informe RC? |

---

## Reglas de Aplicación

### 1. authority_level en conflicto → gana el mayor
Si un chunk de COOTAD (95) contradice un chunk de POA (40), el sistema prefiere COOTAD.  
Esto se implementa como filtro en las queries RAG: `WHERE authority_level >= umbral`.

### 2. canton_id en Capas C y D → obligatorio
- Capas A y B: `canton_id = NULL` (conocimiento nacional)
- Capas C y D: `canton_id = 'MCR'` para Montecristi (primer canton piloto)
- Esto permite escalar a 222 municipios sin contaminar el kernel nacional

### 3. Datos estructurados → tratamiento separado
Los archivos XLSX/CSV del Holding (presupuestos mensuales, conjuntos de datos LOTAIP) **no son chunks semánticos**.  
Tratamiento: tabla separada en Supabase (`holding_structured_data`) o integración con Gold Master.  
**No ingestar en `normativa_corpus` como texto plano.**

### 4. Imágenes → OCR antes de ingestar
Los archivos `pagina_01-17.png` en el Holding requieren OCR para extraer texto.  
Evaluar contenido antes de decidir capa y authority_level.

### 5. Documentos duplicados → versión más completa gana
Algunos documentos existen en .pdf y .docx. Usar .docx si disponible (mejor extracción).

---

## Inventario de Gate 6 (base para ejecución)

### Normativa_Word — Capa A y B (43 archivos totales)

**Delta vs corpus actual (verificar en Gate 6.1):**

| Documento | Capa | authority |
|---|---|---|
| Constitución del Ecuador.docx | A | 100 |
| COOTAD.docx | A | 95 |
| COOTAD PARA LA SOSTENIBILIDAD 2026.docx | A | 95 |
| LEY-ORGANICA-DE-PARTICIPACION-CIUDADANA.docx | A | 95 |
| LOTAIP.docx | A | 95 |
| losncp.docx | A | 95 |
| Codigo Organico Administrativo.docx | A | 95 |
| CODIGO_PLANIFICACION_FINAZAS_PÚBLICAS.docx | A | 95 |
| LEY_SPRGANICA_ERVICIO_PUBLICO LOSEP.docx | A | 90 |
| Codigo-de-la-Democracia.docx | A | 90 |
| CODIGO_ORGANICO_AMBIENTE-2qzoag.docx | A | 85 |
| REGLAMENTO AL CODIGO ORGANICO DEL AMBIENTE.docx | A | 80 |
| Reglamento-LOSNCP-20251030.docx | A | 80 |
| Reglamento-al-COPFP.docx | A | 80 |
| REGLAMENTO_LEY_SPRGANICA_ERVICIO_PUBLICO LOSEP.docx | A | 80 |
| LOTAIP - REGLAMENTO-24-01-2024.docx | A | 80 |
| resolución_no_cpccs-ple-sg-004-o-2026-0030.docx | A | 75 |
| RESOLUCIÓN ADMINISTRATIVA No. 040-2025-ALC...ORGANICO.docx | A | 75 |
| Ley Orgánica de la Contraloría General del Estado.docx | A | 95 |
| Normas de control INterno CGE.docx | A | 80 |
| LEY ORGANICA DE LAS PERSONAS ADULTAS MAYORES.docx | A | 90 |
| ley_organica_discapacidades.docx | A | 90 |
| ley_prevenir_y_erradicar_violencia_mujeres.docx | A | 90 |
| Ley Orgánica para Impulsar la Economía Mujeres.docx | A | 90 |
| ley_de_movilidad_humana_oficial.docx | A | 90 |
| codigo_ninezyadolescencia.docx | A | 90 |
| CODIFICACION_DEL_REGLAMENTO_DE_DEMOCRACIA_INTERNA.docx | A | 80 |
| convencion-americana-derechos-humanos.docx | A | 70 |
| cedaw-recomendacionespanama_26dic.docx | A | 70 |
| derechos CDN Niños.docx | A | 70 |
| Pacto PIDESC.docx | A | 70 |
| LOTAIP - guia-metodologica-mecanismos.docx | B | 65 |
| LOTAIP - guia-para-el-cumplimiento-entidades.docx | B | 65 |
| PDOT-ACUERDO-Nro.-SNP-SNP-2023-0049-A.docx | B | 65 |
| SNP-SNP-2023-0049-A-PDOT-2023.docx | B | 65 |
| Lineamientos-para-el-monitoreo-y-seguimiento.docx | B | 60 |
| clasificador_presupuestario_2026.docx | B | 55 |
| Plan Nacional de Desarrollo 2025-2029.docx | B | 50 |
| PAGCC-ECUADOR-2024.docx | B | 50 |
| PDOT MOntecristi 2023-2027 Bicentenario.docx | C | 48 |
| Plan CNE ALcalde Montecristi.docx | C | 15 |

### Holding_Municipal_Montecristi — Capa C y D (~90+ documentos)

**Entidades del Holding:**
- GAD Montecristi (municipio)
- EP Aseo (empresa pública saneamiento)
- Bomberos (cuerpo de bomberos)
- Patronato Municipal (servicios sociales)

**Documentos por categoría:**

| Categoría | Entidades | Años | Capa | authority |
|---|---|---|---|---|
| POA | GAD+Aseo+Bomberos+Patronato | 2023-2026 | C | 40 |
| PAC | GAD+Aseo+Bomberos+Patronato | 2023-2026 | C | 38 |
| PAI | GAD | 2023, 2025, 2026 | C | 43 |
| Cédulas presupuestarias | GAD | 2023-2025 | C | 35 |
| Presupuestos mensuales | todos | var | C | 32 |
| Plan Plurianual Inversiones | GAD | — | C | 45 |
| Plan Bicentenario | GAD | — | C | 48 |
| Informe RC | GAD+Aseo+Bomberos+Patronato | 2023-2024 | D | 28 |
| Informe PP (Presupuesto Participativo) | GAD | 2024-2026 | D | 25 |
| Reporte ICM SIGAD | GAD | 2023-2024 | D | 22 |
| Conjuntos datos LOTAIP Numeral 6 | GAD | 2025-2026 | D | 20 |

**Nota XLSX/CSV:** Los conjuntos de datos LOTAIP Numeral 6 (120+ archivos mensuales)  
son datos estructurados → tabla `holding_structured_data`, no `normativa_corpus`.

---

## Cambios de Schema Requeridos

### Supabase — tabla `normativa_corpus`
```sql
ALTER TABLE normativa_corpus 
  ADD COLUMN document_class TEXT CHECK (document_class IN 
    ('NORMA','METODOLOGIA','INSTRUMENTO_TERRITORIAL','EVIDENCIA_OBSERVACIONAL')),
  ADD COLUMN authority_level INTEGER CHECK (authority_level BETWEEN 10 AND 100),
  ADD COLUMN canton_id TEXT DEFAULT NULL;
```

### manifest.py — campos nuevos por documento
```python
{
  "sigla": "COOTAD",
  "document_class": "NORMA",        # NUEVO
  "authority_level": 95,            # NUEVO
  "canton_id": None,                # NUEVO — None para A/B, 'MCR' para C/D
  ...
}
```

### Documentos existentes (corpus actual 43 docs)
Todos son Capa A o C (PDOT MCR, Plan GOB MCR). Migración:
- 41 docs normativos → `document_class='NORMA'`, `authority_level` según tabla
- PDOT MCR → `document_class='INSTRUMENTO_TERRITORIAL'`, `authority_level=48`, `canton_id='MCR'`
- Plan GOB MCR → `document_class='INSTRUMENTO_TERRITORIAL'`, `authority_level=15`, `canton_id='MCR'`

---

## Estructura de Gate 6 (definitiva)

```
Gate 6.0  ✅  ADR-021 (este documento)
Gate 6.1  ⏳  Schema Supabase: ADD COLUMN document_class + authority_level + canton_id
Gate 6.2  ⏳  Migración corpus existente (43 docs → clasificar)
Gate 6.3  ⏳  Delta Normativa_Word: verificar qué falta vs corpus actual → ingestar
Gate 6.4  ⏳  Ingesta Holding_Municipal_Montecristi (Capas C+D, texto)
Gate 6.5  ⏳  Datos estructurados LOTAIP → tabla holding_structured_data
Gate 6.6  ⏳  Semantic Mining: densidad normativa por dominio, circuitos emergentes
Gate 6.7  ⏳  Re-evaluar ADR-019 con corpus completo + densidad Dom09 medida
```

---

## Nota sobre GeoTwin

GeoTwin **NO es uno de los 12 dominios canónicos**.  
GeoTwin es **Layer 3** de la arquitectura de presentación UI (ver CLAUDE.md).

```
Layer 2 → 12 Dominios (D01-D12)   → Inteligencia institucional
Layer 3 → GeoTwin (p4_geotwin.py) → Proyección espacial territorial
```

Dom10 (Territorio & Cobertura) ES un dominio — captura los datos de cobertura territorial.  
GeoTwin ES la herramienta que proyecta esos datos (y los de otros dominios) sobre el mapa de Montecristi.  
Son distintos y se necesitan mutuamente.

---

## Nota SNP (corrección permanente)

**SENPLADES ya no existe.** La entidad correcta es:  
**SNP — Secretaría Nacional de Planificación** (reemplazó a SENPLADES).  
Usar siempre SNP en documentos, código, comentarios y respuestas.

---

## Relacionado

- ADR-016: Template DCO
- ADR-017: Circuitos Constitucionales
- ADR-018: NRCs
- ADR-019: Dominios de Legitimación Democrática (pendiente Gate 6.7)
- ADR-020: Analítica Constitucional
- OBS-003: Cierre normativo del ciclo democrático (CONFIRMED)
- `governance/QUIRA_STATE.md` — estado vivo del proyecto

---

*ADR-021 ACTIVO · QUIRA Gov · Dylus Lab · 2026-06-02*  
*"QUIRA no es un dashboard. Es un motor de trazabilidad pública. Puede responder qué debía ocurrir,*  
*qué se planificó, qué se ejecutó, qué observó la ciudadanía, dónde ocurrió y qué debería pasar después."*  
*— Colega asesor, 2026-06-02*
