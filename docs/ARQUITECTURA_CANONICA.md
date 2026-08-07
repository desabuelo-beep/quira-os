# QUIRA Intelligence — Arquitectura Canónica de 6 Capas
**CANON OFICIAL — No modificar sin validación del equipo Dylus Lab**
*Formalizado: 2026-05-26 · Sprint 3 Semana 3 · Actualizado: 2026-05-26 · Decisión Doctrinal Dos Mundos*

> **📚 Stack de Descripción de QUIRA · NIVEL 2 — Arquitectura (Infraestructura / Despliegue).**
> Responde *"¿cómo funciona técnicamente QUIRA?"* — los **6 tiers tecnológicos** (Excel·Pipeline·Supabase·Streamlit·Obsidian·GitHub) + las reglas de flujo del dato. **Subordinado al Nivel 1** (rector) → `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md`.
> Estas **"6 capas" ≠ las "7 capas de soberanía"** del Nivel 1 **≠ las "7 capas del MCD"** del Nivel 3 (`docs/adr/ADR-031 §6`): **son niveles distintos del mismo sistema, NO un conflicto de conteo.** Mapa rector: `governance/QUIRA_MASTER_INDEX.md §1.A`.

> Este documento responde a la pregunta: **¿cómo fluye la información entre las seis capas que componen QUIRA Intelligence?**
> Antes de agregar un componente nuevo, pregunta: ¿en qué capa vive? ¿Respeta las reglas de comunicación de esta arquitectura?
> Si la respuesta no es clara: es futuro, no PMV.

---

## 0. Principio Central

QUIRA Intelligence no es una aplicación. Es una **infraestructura de memoria institucional longitudinal**.

Sus seis capas son complementarias, cada una con una responsabilidad exclusiva. La integridad del sistema depende de que cada capa haga solo lo que le corresponde.

```
GOLD MASTER  →  PIPELINE  →  SUPABASE  →  STREAMLIT
     ↑                              ↑
 GITHUB (versioning)          OBSIDIAN (doctrina)
```

**Regla absoluta:** el flujo de datos es unidireccional hacia adelante. Ninguna capa downstream modifica datos de una capa upstream.

---

## 0.B Doctrina de Producto — Los Dos Mundos

> **⚠️ Doctrina de negocio SUPERADA — banner de deferencia (Regla #6: NO se reescribe §0.B; se conserva como histórico).**
> El modelo *"SaaS · el municipio compra · GAD = cliente"* de esta sección **quedó superado**. **Rector vigente: `docs/adr/ADR-024` + `governance/BOOT.md §LA TESIS`.**
> Doctrina vigente (Javo): **GAD = sujeto observado** (no cliente) · vender software a GADs es **válido pero NO el negocio central** ·
> **familia QUIRA = 6 productos** (Operaciones · Ciudadana · Institucional · Impact · Cooperación · Economic). El texto de §0.B abajo es **registro histórico**, no doctrina activa.

*Decisión doctrinal establecida 2026-05-26. Permanente e irrevocable sin revisión formal.*

QUIRA Intelligence opera en **dos mundos separados con propósitos, audiencias y reglas completamente distintas**. Esta separación no es de implementación — es de doctrina.

### El Primer Mundo: Observatorio (Núcleo Soberano)

```
MUNICIPIO
  └── Operador proporciona Excel mensual
        └── Gold Master (actualización manual)
              └── Pipeline → Snapshot → Supabase
                    └── Dashboard GOV (funcionarios autorizados)
```

**Principios:**
- La fuente de verdad es el Excel del municipio, cargado por el operador. **No hay scraping automático.**
- Razón: los portales ecuatorianos (SRI, SERCOP, eSIGEF) son inestables, los PDFs corruptos, las URLs cambian sin aviso. La confiabilidad epistemológica exige control humano de la ingesta.
- El municipio compra: operación institucional automatizada — Gold Master + snapshot mensual + monitoreo + SAT + dashboards + alertas + trazabilidad + QUIRA IA + operación mensual.
- Cada GAD municipal es una instancia independiente con su propio Gold Master (modelo SaaS).

**Lo que nunca ocurre en este mundo:**
- El pipeline no escribe en el Gold Master.
- Streamlit no accede al Excel directamente en producción.
- Los datos de ICPI, TGI, SAT, formulas del Gold Master no se exponen al mundo Ciudadano.

---

### El Segundo Mundo: QUIRA Ciudadano (Exploración Pública)

```
CIUDADANÍA / ACADEMIA / ONGs
  └── Acceso público sin autenticación
        └── Datos traducidos / curados / pedagógicos
              └── NUNCA comparte estado con el núcleo soberano
```

**Principios:**
- Transparencia activa y rendición de cuentas para toda la ciudadanía.
- Los datos que muestra son los que el municipio decide publicar — nunca cálculos crudos del Gold Master.
- El mundo Ciudadano **nunca modifica snapshots, métricas, Gold Master ni Supabase** de producción.
- Los términos técnicos se traducen al lenguaje ciudadano (ver `docs/QUIRA_CIV_CITIZEN_JOURNEY_v1.md`).
- Canal LOTAIP: el ciudadano puede solicitar información formal — QUIRA facilita el proceso, no extrae datos automáticamente.

**Lo que nunca ocurre en este mundo:**
- Formularios que escriban en el núcleo de datos.
- Exposición de H73, ICPI crudo, formulas del Gold Master, logs del pipeline.
- Autenticación compartida con el mundo Institucional.

---

### Tabla de Mundos

| Dimensión | Observatorio | QUIRA Ciudadano |
|---|---|---|
| Nombre público | Observatorio | QUIRA Ciudadano |
| Código interno | `GOV` | `CIV` |
| Audiencia | Funcionarios, Alcaldía, Analistas, Equipo QUIRA | Ciudadanía, Academia, ONGs, Cooperación |
| Acceso | Restringido (autenticación por roles) | Público (sin autenticación) |
| Datos | Gold Master → Pipeline → Supabase → Dashboard | Curados, traducidos, pedagógicos |
| Escritura | Pipeline → Supabase (vía Ops) | Nunca |
| Estado compartido | Solo entre GOV y OPS | Ninguno con GOV/OPS |
| QUIRA IA | Técnica: SAT, alertas, trazabilidad | Pedagógica: explicaciones ciudadanas |
| Fase de desarrollo | Fase 1–2 (activa) | Fase 3 (futura) |

---

### Tabla de Branding Canónico

| Código Interno | Nombre Público | Audiencia Principal | Estado |
|---|---|---|---|
| `GOV` | Observatorio | Funcionarios municipales, Alcaldía | PMV operativo |
| `CIV` | QUIRA Ciudadano | Ciudadanía, Academia, ONGs | Fase 3 (futuro) |
| `IMPACT` | QUIRA Cooperación | Cooperación internacional, Investigadores | Placeholder |
| `OPS` | Operaciones (interno) | Equipo Dylus Lab | PMV operativo |

> **Regla:** el código interno (GOV/CIV/IMPACT/OPS) es para el código y la arquitectura. El nombre público (Institucional/Ciudadano/Cooperación) es lo que el usuario ve. Nunca mezclar en la UI.

---

## 1. Las Seis Capas — Tabla de Responsabilidades

| # | Capa | Tecnología | Responsabilidad | Reemplazable |
|---|---|---|---|---|
| L1 | **Gold Master** | Excel (.xlsx) | Verdad epistemológica — fuente de todos los números canónicos | No (doctrina permanente) |
| L2 | **Pipeline Python** | Python 3.11+ | Lógica operacional — orquesta, calcula, persiste | Sí (arquitectura reemplazable) |
| L3 | **Supabase** | PostgreSQL + pgvector | Memoria longitudinal — historial de snapshots auditables | Sí (cualquier BD persistente) |
| L4 | **Streamlit** | Python UI | Experiencia institucional — visualización, alertas, análisis | Sí (cualquier UI framework) |
| L5 | **Obsidian** | Markdown vault | Cerebro doctrinal-cognitivo — base del futuro QUIRA IA | Sí (cualquier knowledge base) |
| L6 | **GitHub** | Git + Streamlit Cloud | Versionado + despliegue continuo | Sí (cualquier VCS/CD) |

---

## 2. Flujo Canónico Detallado

### L1 → L2: Gold Master alimenta el Pipeline

```
TGI_GOLD_MASTER_v6.0_20260525.xlsx
  └── G6.1_OUTPUT_API  (51 métricas estructuradas)
        ↓
  app/connectors/gold_master.py
        ↓
  Snapshot pipeline recibe datos canónicos (reliability=0.99)
```

**Reglas:**
- El pipeline **lee** el Gold Master. **Nunca escribe**.
- La lectura ocurre a través de `app/connectors/gold_master.py` exclusivamente.
- Si el Gold Master no está accesible (Streamlit Cloud), el pipeline usa `data/gm_snapshot.json` como fallback.
- `gm_snapshot.json` se actualiza **manualmente** cada vez que se sube una nueva versión del Gold Master.

**Archivos:**
```
app/connectors/gold_master.py         ← único punto de acceso al Excel
data/gm_snapshot.json                 ← fallback para entornos sin acceso local
data/doctrinal/gm_changelog.json      ← registro de versiones del Gold Master
data/doctrinal/gm_schema.json         ← esquema canónico de G6.1_OUTPUT_API
```

---

### L2: Pipeline — Orquestador Central

El pipeline es el corazón operacional. Integra todas las fuentes y produce un snapshot completo.

```
                    ┌─────────────────────────────────┐
                    │     snapshot_pipeline.py         │
                    │                                 │
  gold_master.py ──►│  1. Datos canónicos (GM)         │
  dpe.py         ──►│  2. Ejecución presupuestaria      │
  sercop.py      ──►│  3. Contratación pública          │
  cpccs.py       ──►│  4. Control social / RdC          │
                    │                                 │
                    │  5. sat_evaluator.py → SAT        │
                    │  6. snapshot_diff.py → Diff       │
                    │  7. reliability_tracker.py → Fib  │
                    │  8. gold_master_governance.py → Gov│
                    │                                 │
                    │  → SNAPSHOT canónico v6.0         │
                    └────────────────┬────────────────┘
                                     ↓
                              Supabase + JSON local
```

**Reglas:**
- El pipeline produce **un único snapshot canónico** por ejecución.
- Cada snapshot incluye: TGI · D1-D5 · ICPI · SAT · Diff vs período anterior · Reliability.
- El pipeline no modifica el Gold Master, no escribe en Obsidian, no interactúa con GitHub.
- El pipeline es ejecutado por el equipo QUIRA (Operator/Admin). No por el municipio.

**Módulos del pipeline:**

| Módulo | Función |
|---|---|
| `app/connectors/dpe.py` | DPE API — ejecución presupuestaria eSIGEF |
| `app/connectors/sercop.py` | SERCOP OCDS — contratos públicos |
| `app/connectors/cpccs.py` | CPCCS — control social, RdC |
| `app/connectors/gold_master.py` | Gold Master Excel — datos canónicos |
| `app/services/sat_evaluator.py` | Evaluación SAT con triple ancla legal+operativa+doctrinal |
| `app/services/snapshot_diff.py` | Comparación entre períodos: MEJORA/DETERIORO/RUPTURA... |
| `app/services/longitudinal_engine.py` | RC-M: tabla y tendencias longitudinales |
| `app/services/reliability_tracker.py` | Fiabilidad por fuente: dashboard · historial · salud |
| `app/services/gold_master_governance.py` | Gobernanza GM: validación · changelog · respaldo SHA-256 |
| `app/pipelines/snapshot_pipeline.py` | Orquestador: 11 pasos, integra todo lo anterior |

---

### L2 → L3: Pipeline persiste en Supabase

```
snapshot_pipeline.py
      ↓
Supabase / PostgreSQL + pgvector
  ├── tabla: snapshots         ← snapshot canónico por municipio/período
  ├── tabla: sat_alerts        ← alertas SAT históricas
  ├── tabla: reliability_log   ← historial de fiabilidad por fuente
  └── tabla: diff_log          ← registro de diffs entre períodos
```

**Reglas:**
- Supabase es **escritura desde el pipeline, lectura desde Streamlit**.
- Streamlit **nunca escribe** en Supabase directamente (toda escritura pasa por el pipeline).
- Los datos en Supabase son la **memoria longitudinal auditada** — no se borran, solo se agregan.
- Cada snapshot tiene: `municipio_code`, `periodo`, `fecha_snapshot`, `hash` de integridad.

---

### L3 → L4: Supabase alimenta Streamlit

```
Supabase
  ↓
Streamlit App (quira-os)
  ├── 🏛 GOV — análisis institucional (Viewer · Analyst)
  │     ├── Estado Municipal — ICPI · TGI · SAT activas
  │     ├── RC-M Longitudinal — tendencia · deterioro · recuperación
  │     ├── Alertas SAT — triple ancla legal+operativa+doctrinal
  │     ├── Comparación de Períodos — Diff Engine
  │     ├── Ejecución Presupuestaria — D3 Ti · devengado · holding
  │     └── Trazabilidad — fuentes · reliability · cadena evidencial
  │
  ├── 🌎 QUIRA Ciudadano (CIV) — exploración pública, transparencia activa (Fase 3)
  │
  ├── 📑 QUIRA Cooperación (IMPACT) — academia, ONGs, cooperación internacional (Fase 3)
  │
  └── ⚙ Ops — infraestructura interna (Operator · Admin)
        ├── Pipeline — ejecución · estado · logs
        ├── Snapshots — historial · comparación
        ├── Reliability — dashboard fiabilidad por fuente
        ├── Gold Master — validación · changelog · respaldo
        └── Config — entornos · municipios · parámetros
```

**Reglas:**
- Streamlit **solo lee** de Supabase y `gm_snapshot.json`.
- Streamlit **nunca accede al Excel directamente en producción** (Streamlit Cloud no tiene acceso local).
- El sidebar tiene **máximo 7 módulos**. Toda nueva vista es un tab dentro del módulo correspondiente.
- Los 4 ambientes (GOV/Civic/Impact/Ops) son las únicas contenedores posibles para nuevas features.

---

### L5: Obsidian — Cerebro Doctrinal (Desacoplado)

```
QUIRA_KB_Montecristi (vault Obsidian)
  ├── 00_CORE — doctrina TGI, QUIRA, SAT
  ├── 01_MUNICIPIO — perfil Montecristi, historia
  ├── 02_NORMATIVA — COPFP, COOTAD, LOSNCP...
  ├── 03_PDOT — Plan Desarrollo Ordenamiento Territorial
  ├── 04_PRESUPUESTO — eSIGEF, D3, D4
  ├── 05_CONTRATACION — SERCOP, PAC, contratos
  ├── 06_CONTROL — CPCCS, RdC, accountability
  ├── 07_HOLDING — EP Aseo, Bomberos, Patronato
  └── 08_ALERTAS — SAT histórico, notas doctrinales
```

**Estado actual:** 39+ notas creadas, estructura 00-08 operativa, PDOT completamente fragmentado.

**Reglas:**
- Obsidian **nunca se conecta al runtime operacional** (pipeline, Supabase, Streamlit).
- Obsidian es el insumo futuro para QUIRA IA (Fase 2 — embeddings + RAG).
- El vault se mantiene actualizado **manualmente** por el equipo QUIRA después de cada ciclo mensual.
- No usar Obsidian como fuente de datos operacionales. Solo como base doctrinal cognitiva.

**Rol en la hoja de ruta:**

```
AHORA (Fases 1-2):
  Obsidian ← actualización manual → Equipo QUIRA

FUTURO (Fase 2+):
  Obsidian → embeddings/pgvector → Retriever → QUIRA IA
               └── GOV: "¿Qué dice el Art. 113 COPFP sobre D3?"
               └── Civic: explicaciones simplificadas para ciudadanía
               └── Impact: contexto normativo en reportes cooperación
```

---

### L6: GitHub — Versionado y Despliegue

```
GitHub (desabuelo-beep/quira-os)
  ↓ (Streamlit Cloud integración continua)
Streamlit Cloud
  └── quira-os app productiva
```

**Reglas:**
- Todo código vive en GitHub. No hay código productivo fuera del repositorio.
- Streamlit Cloud se despliega automáticamente desde `main` (integración continua).
- El Gold Master Excel **no vive en GitHub** (archivo binario grande, con datos institucionales).
- `data/gm_snapshot.json` sí vive en GitHub — es el puente entre Gold Master y Streamlit Cloud.
- Los documentos doctrinales (`docs/`) viven en GitHub como parte del repositorio.

---

## 3. Reglas de Comunicación Inter-capa

| Comunicación | Permitida | Dirección | Mecanismo |
|---|---|---|---|
| Gold Master → Pipeline | ✅ SÍ | L1 → L2 | `gold_master.py` (lectura) |
| Pipeline → Gold Master | ❌ NO | — | Prohibido absolutamente |
| Pipeline → Supabase | ✅ SÍ | L2 → L3 | SDK Supabase (escritura) |
| Supabase → Pipeline | ✅ SÍ | L3 → L2 | SDK Supabase (lectura histórica) |
| Supabase → Streamlit | ✅ SÍ | L3 → L4 | SDK Supabase (lectura) |
| Streamlit → Supabase | ❌ NO | — | Toda escritura pasa por Pipeline |
| Pipeline → Obsidian | ❌ NO | — | Obsidian está desacoplado del runtime |
| Obsidian → Pipeline | ❌ NO | — | Obsidian solo alimenta IA (Fase 2+) |
| GitHub → Streamlit Cloud | ✅ SÍ | L6 → L4 | CD automático desde `main` |
| Streamlit → Gold Master (local) | ⚠️ DEV ONLY | L4 → L1 | Solo en desarrollo local, nunca en Cloud |

---

## 4. Inventario de Módulos por Capa

### Capa L1 — Gold Master
```
C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\
  TGI_GOLD_MASTER_v6.0_20260525.xlsx  ← ACTIVO (34 hojas, G1.x-G7.x)
  SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx  ← CONGELADO (referencia)
```

### Capa L2 — Pipeline Python
```
app/
  connectors/
    gold_master.py          ← L1→L2: lectura Gold Master
    dpe.py                  ← DPE API ejecución presupuestaria
    sercop.py               ← SERCOP OCDS contratación
    cpccs.py                ← CPCCS control social
  services/
    sat_evaluator.py        ← evaluación SAT triple ancla
    snapshot_diff.py        ← diff entre períodos (6 clasificaciones)
    longitudinal_engine.py  ← RC-M, tendencias, historial
    reliability_tracker.py  ← fiabilidad por fuente
    gold_master_governance.py ← gobernanza GM (validación · changelog · respaldo)
  pipelines/
    snapshot_pipeline.py    ← orquestador principal (11 pasos)
scripts/
  run_pipeline.py           ← entry-point CLI
  registry.py               ← CRUD municipios
data/
  gm_snapshot.json          ← fallback Gold Master para Cloud
  doctrinal/
    gm_changelog.json       ← registro de versiones GM
    gm_schema.json          ← esquema canónico G6.1_OUTPUT_API
  snapshots/130801/         ← longitudinalidad por municipio
models/
  auth.py                   ← roles: Viewer · Analyst · Operator · Admin
utils/
  session.py                ← helpers de sesión y roles
  snapshot_io.py            ← lectura/escritura de snapshots locales
  logger.py                 ← logging centralizado
```

### Capa L3 — Supabase
```
Tablas (PostgreSQL):
  snapshots               ← snapshot canónico por municipio/período
  sat_alerts              ← alertas SAT con triple ancla
  reliability_log         ← fiabilidad por fuente en el tiempo
  (pgvector — Fase 2)     ← embeddings documentales para RAG
```

### Capa L4 — Streamlit
```
app.py                    ← selector 4 ambientes, branding QUIRA Intelligence
quira_pages/
  env_gov.py              ← 🏛 GOV: Estado · RC-M · SAT · Comparación · Ejecución · Trazabilidad
  env_civic.py            ← 🌎 Civic: placeholder (futuro)
  env_impact.py           ← 📑 Impact: placeholder (futuro)
  env_ops.py              ← ⚙ Ops: Pipeline · Snapshots · Reliability · GM · Config
config.py                 ← configuración centralizada
```

### Capa L5 — Obsidian
```
QUIRA_KB_Montecristi/ (vault local)
  39+ notas en estructura 00-08
  PDOT completamente fragmentado en notas atómicas
  Catálogo SAT con triple ancla (legal · operativa · doctrinal)
```

### Capa L6 — GitHub
```
github.com/desabuelo-beep/quira-os  ← repositorio principal
  → Streamlit Cloud (deploy desde main)
  docs/                             ← documentos doctrinales
  tests/                            ← 327 tests acumulados
```

---

## 5. Ciclo Mensual — Integración de Capas

El ciclo mensual es el pulso operacional de QUIRA Intelligence. Integra las 6 capas de forma secuenciada:

```
SEMANA 1: Actualización de fuentes
  DPE API + SERCOP + CPCCS → datos crudos del mes

SEMANA 2: Ciclo Gold Master (L1)
  1. Actualizar hojas G3.x con datos del mes
  2. Recalcular G4.x ICPI/TGI
  3. Revisar G5.x SAT activas
  4. Confirmar G6.1_OUTPUT_API (contrato API)
  5. Registrar nueva versión en gm_changelog.json
  6. Hacer respaldo SHA-256 (gold_master_governance.py)

SEMANA 2-3: Pipeline (L2)
  run_pipeline.py → snapshot canónico
  → SAT evaluado · Diff calculado · Reliability actualizado

SEMANA 3: Persistencia (L3)
  Snapshot → Supabase
  Actualizar gm_snapshot.json → GitHub

SEMANA 4: Análisis y Reporte (L4 + L5)
  Streamlit: RC-M actualizado · alertas revisadas
  Obsidian: notas del período agregadas al vault
  Reporte mensual: exportación PDF/docx para cooperación
```

Para el detalle completo del ciclo: ver `docs/MONTHLY_CYCLE.md`.

---

## 6. Deprecaciones Formales

### 6.1 Roles Municipales → Roles de Sistema → Roles en Español

**Migración completa (2026-05-26):** los roles ahora usan nombres en español en toda la UI y en la lógica de acceso de `ENVIRONMENTS`.

| DEPRECATED (modelo municipal) | INTERMEDIATE (inglés, v5.x) | ACTIVO (español, v6.x) | Key (`auth.py`) |
|---|---|---|---|
| `Alcalde` | `Viewer` | `Visualizador` | `viewer` |
| `Concejal` | `Analyst` | `Analista` | `analyst` |
| `Técnico` | `Operator` | `Operador` | `operator` |
| `Admin` | `Admin` | `Administrador` | `admin` |

**Reglas críticas (aprendidas en producción):**
- El campo `rol` en `_USER_META` (models/auth.py) DEBE coincidir con los nombres en `ENVIRONMENTS["roles"]` (app.py).
- Si se cambia uno sin el otro, `_accessible()` devuelve conjunto vacío → ningún ambiente carga → pantalla en blanco.
- Los nombres de display en el dropdown (`👁 Visualizador`, `📊 Analista`...) son independientes del `key` (`viewer`, `analyst`...) — el key nunca cambia.
- `session_state["rol"]` almacena el nombre en español (p.ej. `"Analista"`) — nunca el key inglés.

Los roles deprecated no deben reaparecer en código nuevo. Las referencias antiguas están marcadas con `# DEPRECATED` en `models/auth.py` y `utils/session.py`.

### 6.2 Branding: "Sentinel" → "QUIRA"

El término "Sentinel" es conceptualmente redundante: **QUIRA Intelligence ya es la infraestructura de inteligencia**. No necesita un módulo "centinela" separado — el SAT cumple esa función con doctrina y base legal.

| DEPRECATED | ACTIVO | Ubicación |
|---|---|---|
| `Sentinel IA` | `QUIRA` | `snapshot_pipeline.py` |
| `sentinel_score` | `quira_score` | `longitudinal_engine.py` |
| `SENTINEL_*` | `QUIRA_*` | referencias genéricas |

**Prioridad de deprecación:** baja — no rompe nada, pero debe resolverse antes de Fase 2.

### 6.3 Arquitectura H01-H99 → G1.x-G7.x

| DEPRECATED | ACTIVO |
|---|---|
| `H73_OUTPUT_API` | `G6.1_OUTPUT_API` |
| `SIAP-ICPI_*` nomenclatura | `TGI_GOLD_MASTER_*` nomenclatura |
| Hojas H01-H99 (v5.5) | Hojas G1.x-G7.x (v6.0) |

El conector `gold_master.py` mantiene compatibilidad con H73 como fallback (v5.5). Se eliminará en v7.0.

---

## 7. Anti-patrones — Lo que NO debe ocurrir

### ❌ Streamlit leyendo el Excel directamente en producción
```python
# PROHIBIDO EN PRODUCCIÓN
import openpyxl
wb = openpyxl.load_workbook("TGI_GOLD_MASTER_v6.0_20260525.xlsx")
```
**Por qué:** Streamlit Cloud no tiene acceso al sistema de archivos local.
**Solución:** Usar `data/gm_snapshot.json` + Supabase.

### ❌ Pipeline modificando el Gold Master
```python
# ABSOLUTAMENTE PROHIBIDO
ws["B2"] = nuevo_valor  # el pipeline NUNCA escribe en el Gold Master
wb.save(ruta_gold_master)
```
**Por qué:** El Gold Master es la fuente de verdad. Modificarlo desde código rompe la cadena de custodia.
**Solución:** Actualizarlo manualmente, registrar la versión en `gm_changelog.json`.

### ❌ Streamlit escribiendo en Supabase directamente
```python
# PROHIBIDO — toda escritura pasa por el pipeline
supabase.table("snapshots").insert({"data": "..."}).execute()
```
**Por qué:** La escritura debe pasar por el pipeline que valida, firma y garantiza integridad.
**Solución:** Streamlit invoca el pipeline (o espera que Ops lo ejecute manualmente).

### ❌ Obsidian conectado al runtime
```python
# PROHIBIDO — Obsidian está desacoplado
obsidian_note = requests.get("http://obsidian-api/notas/sat-i")
```
**Por qué:** Obsidian es el cerebro cognitivo futuro (Fase 2+), no una fuente de datos operacionales.
**Solución:** Los datos doctrinales viven en el Gold Master y en `data/doctrinal/`.

### ❌ QUIRA Ciudadano accediendo al núcleo soberano
```python
# PROHIBIDO — env_civic.py nunca debe hacer esto
from app.connectors.gold_master import read_api_sheet
df = read_api_sheet()  # datos crudos del Gold Master
supabase.table("snapshots").select("*").execute()  # snapshots internos
```
**Por qué:** QUIRA Ciudadano es el mundo público. Los datos del Gold Master (ICPI crudo, TGI, fórmulas, H73) son el núcleo soberano. Exponerlos directamente desde el mundo Ciudadano viola la doctrina de los Dos Mundos y compromete la integridad institucional.
**Solución:** env_civic.py usa únicamente datos curados/traducidos preparados por el operador para exposición pública. En Fase 3: una vista de presentación (ej. `data/civic_snapshot.json`) separada del snapshot operacional.

### ❌ Quinto ambiente o ítem de sidebar extra
```python
# PROHIBIDO — máximo 7 módulos en el sidebar
PAGES["mi_nueva_seccion"] = {"url": "nueva_feature"}
```
**Por qué:** La regla arquitectural es: 4 ambientes (GOV/Civic/Impact/Ops), máximo 7 módulos en sidebar. Toda nueva feature vive como tab dentro del módulo existente.
**Solución:** Agregar como tab en el módulo correspondiente.

### ❌ Datos calculados en Python hardcodeados en el Gold Master
```python
# PROHIBIDO — el Gold Master calcula, Python no dicta
ws["B15"] = icpi_calculado_por_python  # rompería la trazabilidad
```
**Por qué:** Las fórmulas del Gold Master garantizan reproducibilidad. Si Python calcula y escribe, se pierde la cadena epistemológica.
**Solución:** Python lee el resultado ya calculado por el Gold Master (G6.1_OUTPUT_API).

---

## 8. Métricas de Salud de la Arquitectura

Para verificar que la arquitectura está integrada correctamente en cada ciclo:

| Indicador | Fuente | Umbral |
|---|---|---|
| `gm_snapshot.json` actualizado | L1→L2 bridge | < 7 días del último cierre GM |
| Tests en verde | L2 pipeline | 327+ tests, 0 failures |
| SHA-256 Gold Master verificado | `gold_master_governance.py` | Coincide con `.sha256.json` |
| Snapshot en Supabase | L2→L3 | 1 snapshot/mes mínimo |
| Reliability Gold Master | `reliability_tracker.py` | ≥ 0.99 |
| Reliability DPE API | `reliability_tracker.py` | ≥ 0.90 |
| Vault Obsidian actualizado | L5 | < 30 días del último ciclo |
| GitHub sincronizado con Cloud | L6 | Deploy automático activo |

---

## 9. Hoja de Ruta — Tres Fases de Producto

La hoja de ruta está organizada en tres fases que siguen la lógica de consolidación antes de expansión.

### Fase 1 — Estabilización (Sprint 3 · Activa)

**Objetivo:** QUIRA Institucional 100% operativo en producción.

| Ítem | Estado | Descripción |
|---|---|---|
| Login 4 roles (español) | ✅ Completo | Visualizador · Analista · Operador · Administrador |
| Landing 3 plataformas | ✅ Completo | Institucional · Ciudadano · Cooperación |
| 4 ambientes desplegados | ✅ Completo | GOV · Civic · Impact · Ops (todos en git/Cloud) |
| Snapshot activo | ✅ Completo | ICPI · TGI · SAT · longitudinalidad en Supabase |
| Requirements.txt Cloud | ✅ Completo | Todos los paquetes críticos validados |
| Ciclo mensual documentado | ⚠️ En progreso | Scripts operacionales a confirmar en git |

---

### Fase 2 — Consolidación GOV (Sprint 4)

**Objetivo:** Observatorio con experiencia completa, narrativa institucional y herramientas del ciclo mensual.

| Ítem | Descripción |
|---|---|
| RC-M Longitudinal completo | Historial multi-período, tendencias, deterioro/recuperación |
| SAT automático con triple ancla | Evaluación con base legal + operativa + doctrinal |
| Ciclo mensual ejecutable desde Ops | Scripts run_snapshot, informe mensual desde UI |
| Narrativa institucional GOV | Textos, interpretaciones, alertas con contexto normativo |
| Exportación de reportes | PDF/DOCX para el municipio desde GOV |
| QUIRA IA Institucional | Respuestas técnicas sobre SAT, COPFP, COOTAD |
| Expansión SaaS | Segundo GAD: Manta o Jipijapa (Gold Master independiente) |

---

### Fase 3 — QUIRA Ciudadano (Sprint 5+)

**Objetivo:** Vista pública con transparencia activa, accesible sin autenticación.

| Ítem | Descripción |
|---|---|
| Panel transparencia ciudadana | Indicadores traducidos al lenguaje ciudadano |
| QUIRA IA Pedagógica | Explicaciones simples, sin jerga técnica |
| Canal LOTAIP | Facilitador de solicitudes de información pública |
| Módulo Academia/ONGs | Datos longitudinales para investigación (con QUIRA Cooperación) |
| Acceso público | Sin autenticación, sin exposición del núcleo |

---

### Estado por Capa (actualizado Fase 1)

| Capa | Estado | Próxima evolución |
|---|---|---|
| L1 Gold Master | ✅ v5.5_TGI (canónico activo) | v6.0 migración · v7.0 nuevos municipios |
| L2 Pipeline | ✅ 11 pasos + 5 servicios activos | Scheduler automático mensual (Fase 2) |
| L3 Supabase | ✅ esquema canónico + snapshots activos | pgvector para embeddings (Fase 3) |
| L4 Streamlit | ✅ 4 ambientes, landing nueva, roles español | GOV completo (Fase 2) · Civic público (Fase 3) |
| L5 Obsidian | ⚠️ vault activo, desacoplado | Embeddings + RAG (Fase 3 Sep-Dic 2026) |
| L6 GitHub | ✅ repositorio activo, CD operativo | Flujo CI/CD formal (Fase 2) |

---

## 10. Reglas Doctrinales Permanentes de Producto

*Establecidas 2026-05-26. No negociables. Requieren aprobación formal del equipo Dylus Lab para cualquier excepción.*

### Regla 1 — Un Solo Dominio
```
quiraintelligence.streamlit.app
```
No hay subdominios, no hay aplicaciones separadas. Los cuatro ambientes (GOV/Civic/Impact/Ops) conviven en la misma app bajo el mismo dominio.

### Regla 2 — Un Solo Núcleo Matemático
El Gold Master Excel es la única fuente de verdad para todos los números. No hay cálculos paralelos en Python que contradigan o reemplacen los del Gold Master. Python lee, Excel calcula.

### Regla 3 — QUIRA Ciudadano Nunca Toca el Núcleo
QUIRA Ciudadano (`env_civic.py`) no puede:
- Leer directamente de Supabase con las credenciales del pipeline.
- Exponer datos de ICPI, TGI, SAT crudos.
- Disparar ejecuciones del pipeline.
- Modificar cualquier dato que pertenezca al mundo Institucional.

Si necesita datos del municipio, pasa por una capa de presentación curada (curada por el operador/admin).

### Regla 4 — Operaciones es Infraestructura Crítica
El ambiente Ops (`env_ops.py`) es el panel de control del equipo Dylus Lab. Accesible solo para roles `Operador` y `Administrador`. Cualquier acción que modifique el estado del sistema (ejecutar pipeline, cargar snapshot, cambiar parámetros) solo puede ocurrir desde Ops.

### Regla 5 — El Operador Proporciona el Excel
No hay scraping automático de portales públicos ecuatorianos (SRI, SERCOP, eSIGEF, portales GAD). El operador (equipo Dylus Lab) consolida los datos en el Gold Master mensualmente. Esta es una decisión de confiabilidad epistemológica, no de capacidad técnica.

### Regla 6 — Cada GAD es una Instancia Independiente
El modelo de negocio es SaaS: cada municipio (GAD) tiene su propio Gold Master, sus propios snapshots, su propia configuración. No hay datos compartidos entre municipios. La arquitectura escala horizontalmente por replicación, no por base de datos compartida.

### Regla 7 — Arquitectura Congelada en PMV
La arquitectura de 6 capas (Gold Master → Pipeline → Supabase → Streamlit + Obsidian + GitHub) está congelada para el PMV. Ninguna capa nueva, ningún servicio externo adicional sin revisión formal. Nuevas features = tabs dentro de ambientes existentes.

---

*NORTH.md es el documento de visión estratégica. SPRINT3.md es el plan de ejecución. Este documento es el contrato arquitectónico permanente entre las seis capas y la doctrina de los Dos Mundos.*

*Dylus Lab © 2026 — QUIRA Intelligence*
