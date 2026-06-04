# MAPA DEL ECOSISTEMA QUIRA
## Dylus Lab — Índice de Navegación Canónico

**Versión**: 2.1  
**Fecha**: 2026-05-31 (Alpha 1.0 declarado — Neo4j operativo — consulta bautismal ejecutada)  
**Custodio**: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO  
**Propósito**: Punto de entrada único para toda sesión de trabajo. Resuelve el problema de "contexto cero" al inicio de cada sesión.

> **Regla de uso**: Leer este documento PRIMERO antes de explorar cualquier carpeta. Evita volver a leer documentos ya procesados y evita confundir versiones antiguas con las canónicas.

---

## PROTOCOLO DE ARRANQUE DE SESIÓN

**Orden canónico de lectura para Claude al inicio de cada sesión:**

| Orden | Archivo | Propósito |
|---|---|---|
| 1 | Este archivo (`MAPA_ECOSISTEMA_QUIRA.md`) | Orientación completa del ecosistema |
| 2 | `governance\QUIRA_STATE.md` | Estado actual del proyecto — qué está abierto, qué está cerrado |
| 3 | `governance\QUIRA_DATA_GOVERNANCE_v1.0.md` | Principios de datos, autoridad documental, guardrails |
| 4 | `governance\QUIRA_CAUSAL_MODEL_v1.0.md` | Modelo causal QNKC-002, cadena C1-C10, hipótesis H1-H8 |
| 5 | `governance\QUIRA_TERRITORIAL_SEMANTICS_v1.0.md` | Semántica territorial, parroquias, NBI, demografía |

**Lectura condicional (solo si la tarea lo requiere):**

| Condición | Leer |
|---|---|
| Trabajo con Gold Master / indicadores | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` |
| Trabajo con QTMP o circuitos | `quira-os\data\qtmp\qtmp_schema.yaml` + circuito |
| Cargar Neo4j (reinstalar/reiniciar) | `quira-os\scripts\neo4j_load_qtmp.py` |
| Ejecutar consulta bautismal | `quira-os\scripts\neo4j_bautismal_query.py` |
| Trabajo con PDOT o metas territoriales | `ProyecT\Documentos_Montecristi\PDOT_MONTECRISTI_KB.xlsx` |
| Auditoría metodológica Dom12 | `governance\NOTA_METODOLOGICA_DOM12_INDICES_COMPLEMENTARIOS.md` |
| Cédulas presupuestarias Holding | `ProyecT\Holding_Municipal_Montecristi\Presupuestos 2023-2026\` |
| Cédulas SIGEF 2025-2026 | `ProyecT\Cedulas_SIGEF_2026\` |
| Deudas metodológicas Beta | `governance\QUIRA_BETA_BACKLOG.md` |

---

## FUENTES DE VERDAD CANÓNICAS

### Jerarquía de autoridad (de mayor a menor)

```
1. Constitución del Ecuador / COOTAD / COPLAFIP    → norma superior
2. SIGEF (cédulas presupuestarias oficiales)        → dato de ejecución oficial
3. Gold Master (SIAP-ICPI_GOLD_MASTER_v5.5_TGI)    → cálculo canónico interno
4. QTMP (circuitos yaml)                            → observación QUIRA estructurada
5. Vault Obsidian / PMV Streamlit                   → derivados del Gold Master
```

**Principio de autoridad**: Si hay conflicto entre un dato del PMV y el Gold Master, el Gold Master gana siempre. Si hay conflicto entre el Gold Master y una cédula SIGEF, la cédula SIGEF gana.

### Archivos canónicos activos

| Artefacto | Ruta canónica | Estado |
|---|---|---|
| **Gold Master (canónico activo)** | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | ACTIVO — aquí se trabaja y actualiza |
| Gold Master (snapshot freeze) | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260526.xlsx` | SOLO LECTURA |
| Historial Gold Master (15 versiones) | `ProyecT\historial_gold_master\` | REFERENCIA — no usar |
| PDOT Montecristi KB (canónico app) | `quira-os\data\PDOT_MONTECRISTI_KB.xlsx` | ACTIVO (app) |
| PDOT Montecristi KB (fuente) | `ProyecT\Documentos_Montecristi\PDOT_MONTECRISTI_KB.xlsx` | REFERENCIA |
| Schema QTMP | `quira-os\data\qtmp\qtmp_schema.yaml` | v1.1 ACTIVO |
| Circuito GAP_10PCT | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_GAP_10PCT.yaml` | ACTIVO |
| Circuito AGUA_POTABLE | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_AGUA_POTABLE.yaml` | ACTIVO |
| Circuito EQUIDAD | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_EQUIDAD.yaml` | ACTIVO |
| Governance: estado | `governance\QUIRA_STATE.md` | ACTIVO — actualizar al cerrar sprint |
| Governance: datos | `governance\QUIRA_DATA_GOVERNANCE_v1.0.md` | v1.0 CONGELADO |
| Governance: semántica | `governance\QUIRA_TERRITORIAL_SEMANTICS_v1.0.md` | v1.0 CONGELADO |
| Governance: modelo causal | `governance\QUIRA_CAUSAL_MODEL_v1.0.md` | v1.0 + Adenda CONGELADO |
| Beta Backlog | `governance\QUIRA_BETA_BACKLOG.md` | VIVO — agregar C10 según surjan |

---

## MAPA COMPLETO DE ARCHIVOS

### Estructura `C:\Users\DELL\Desktop\Javo\Dylus Lab\`

```
Dylus Lab\
│
├── MAPA_ECOSISTEMA_QUIRA.md               ← ESTE ARCHIVO — leer primero
│
├── governance\                            ← CAPA EPISTEMOLÓGICA (7 documentos)
│   ├── QUIRA_STATE.md                     ← Estado actual del proyecto
│   ├── QUIRA_DATA_GOVERNANCE_v1.0.md      ← Principios de datos — CONGELADO
│   ├── QUIRA_TERRITORIAL_SEMANTICS_v1.0.md← Semántica territorial — CONGELADO
│   ├── QUIRA_CAUSAL_MODEL_v1.0.md         ← Modelo causal + C10 — CONGELADO
│   ├── NOTA_METODOLOGICA_DOM12_*.md       ← Piso1 vs Piso2 — CONGELADO
│   ├── QUIRA_BETA_BACKLOG.md              ← Deudas C10 — VIVO
│   └── QUIRA_ECOSYSTEM_2026_2030.md       ← Visión estratégica
│
├── ProyecT\                               ← ÁREA DE TRABAJO ACTIVA
│   │
│   ├── SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx        ← GOLD MASTER — abrir aquí
│   ├── SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260526.xlsx  ← Snapshot (no editar)
│   │
│   ├── Holding_Municipal_Montecristi\     ← Documentos del Holding
│   │   ├── PAC 2023-2026\                 — Plan Anual de Contratación
│   │   ├── POA 2023-2026\                 — Plan Operativo Anual
│   │   ├── Presupuestos 2023-2026\        ← Cédulas presupuestarias históricas
│   │   ├── Rendiciones de cuentas 2023-2024\
│   │   ├── Presupuesto participativo 2024-2026\
│   │   ├── Oficiales\                     — Documentos legales
│   │   ├── Oficiales_2026\
│   │   └── [PAI, POA, ICM SIGAD — PDFs]
│   │
│   ├── Cedulas_SIGEF_2026\                ← Cédulas 2025-2026 (SIGEF directo)
│   │   ├── GAD Montecristi Presupuesto 2025 (diciembre).xlsx
│   │   ├── GAD MUNICIPAL DE MONTECRISTI PRESUPUESTO MARZO 2026.xlsx
│   │   ├── PATRONATO MUNICIPAL ... MARZO 2026.xlsx
│   │   ├── CUERPO DE BOMBEROS ... MARZO 2026.xlsx
│   │   └── EMPRESA MUNICIPAL DE ASEO ... MARZO 2026.xlsx
│   │
│   ├── Documentos_Montecristi\            ← PDOT, Resoluciones, Planes oficiales
│   │   ├── PDOT_MONTECRISTI_KB.xlsx       — PDOT estructurado (fuente)
│   │   ├── PDOT_MONTECRISTI_KB_v6.3.xlsx
│   │   ├── PDOT MOntecristi 2023-2027 Bicentenario.docx
│   │   ├── PDOT_GAD_Montecristi_2023_2027.pdf
│   │   ├── Plan Plurianual PDOT 2023-2027 GAD Montecristi.xlsx
│   │   ├── Resolucion_040_2025_Organico_Estructural.docx
│   │   ├── Resolucion_040_2025_Organico_Estructural.pdf
│   │   ├── Plan CNE ALcalde Montecristi.docx
│   │   └── diagnostico pdot para claude ingesta excel 2.docx
│   │
│   ├── Normativa_PDF\                     ← Cuerpo normativo en PDF
│   ├── Normativa_Word\                    ← Cuerpo normativo en Word
│   ├── logos\                             ← Logos QUIRA (png)
│   └── historial_gold_master\             ← 15 versiones anteriores (v4.1→v5.5)
│                                            NO usar — solo referencia histórica
│
├── metodologia_beta\                      ← FUENTE BETA — No leer en Alpha
│   ├── Metodologia SIAP-ICPI Final.md     — Índices complementarios Piso 2
│   ├── SIAP-ICPI_VERSION_CON_METODOLOGIA.xlsx
│   ├── Instrumento SIAP-ICPI TESIS.xlsx
│   ├── TESIS DE LICENCIATURA EN CIENCIAS POLÍTICAS menos punitiva.docx
│   └── [otros insumos metodológicos tesis]
│
├── documentos_proyecto\                   ← Documentos técnicos y académicos
│   ├── Manual_Tecnico_QUIRA_v5.0.docx
│   ├── Informe_Patronato_Reestructuracion_2018.docx
│   ├── Para_ensayo_academico_negocio.docx
│   ├── Plan_Bicentenario_Montecristi.pdf
│   ├── Plan_CNE_Alcalde_Montecristi_2023.pdf
│   └── flujogramas\                       — SVG/HTML de arquitectura QUIRA
│
├── _historico\                            ← TODO LO QUE NO ES QUIRA
│   ├── TERRA_ECIAP\                       — Proyecto anterior completo
│   │   ├── Refactorizacion_TERRA\         — ETL scripts Terra
│   │   ├── Varios_Actuales_terra\         — Excel Terra (múltiples versiones)
│   │   └── [otros archivos Terra]
│   ├── ETL_scripts_legacy\                — Scripts de procesamiento viejos
│   │   └── Gold_Master_varios\            — Scripts ECIAP
│   ├── ARCHIVO_VIEJOS\                    — Archivos archivados previamente
│   ├── pantalla pmv tearra institucional\ — Capturas Terra PMV
│   ├── Prompt\                            — Prompts anteriores
│   └── Para_API_keys_REVISAR\            ← ⚠️ REVISAR: GNOMIKA-LAB-ECIAP-API-KEY.txt
│                                           Revocar o mover a gestor seguro
│
├── Tecnic_SOLO_CONTIENE_API_KEY_GEMINI\  ← ⚠️ REVISAR: API Key Gemini.txt
│                                           Revocar o mover a gestor seguro
│
├── quira-os\                              ← GIT REPO — App Streamlit + QTMPs
│   ├── scripts\                           ← Scripts Neo4j Sprint 2
│   │   ├── neo4j_load_qtmp.py             ← Carga 3 QTMPs → Neo4j (MERGE idempotente)
│   │   └── neo4j_bautismal_query.py       ← Consulta bautismal ADR-010
│   └── data\
│       ├── PDOT_MONTECRISTI_KB.xlsx       ← PDOT canónico para la app
│       ├── qtmp\                          ← Circuitos QTMP (5 archivos)
│       └── vault_backup_p2\              ← 80+ notas Obsidian
│
├── quiraintelligence-web\                 ← GIT REPO — Sitio quiraintelligence.com
└── quira-harvester\                       ← GIT REPO — Harvester (revisar propósito)
```

---

## INVENTARIO DE DATOS — CÉDULAS PRESUPUESTARIAS

### Cédulas disponibles (al 2026-05-31)

| Entidad | Período | Archivo | Ubicación |
|---|---|---|---|
| GAD Montecristi | Anual 2025 (dic) | `GAD Montecristi Presupuesto 2025 (diciembre).xlsx` | `Cedulas_SIGEF_2026\` |
| GAD Montecristi | Mar 2026 | `GAD MUNICIPAL DE MONTECRISTI PRESUPUESTO MARZO 2026.xlsx` | `Cedulas_SIGEF_2026\` |
| Patronato Municipal | Mar 2026 | `PATRONATO MUNICIPAL ... MARZO 2026.xlsx` | `Cedulas_SIGEF_2026\` |
| Cuerpo de Bomberos | Mar 2026 | `CUERPO DE BOMBEROS ... MARZO 2026.xlsx` | `Cedulas_SIGEF_2026\` |
| EMAI (Aseo/Agua) | Mar 2026 | `EMPRESA MUNICIPAL DE ASEO ... MARZO 2026.xlsx` | `Cedulas_SIGEF_2026\` |
| Holding 2023-2025 | Histórico anual | Ver subcarpetas por año | `Holding_Municipal_Montecristi\Presupuestos 2023-2026\` |

### Dato pendiente prioritario

```
PENDIENTE: Cédula Patronato Diciembre 2025 (mes 12)
Efecto: Confirmar RES_G10P_01_MCR (actualmente pendiente_validacion con valor 20.84%)
Fuente: SIGEF → solicitar a Dirección Financiera GADMCM
```

### Indicadores calculados (Gold Master v5.5)

| Indicador | Valor | Estado |
|---|---|---|
| Ti_Patronato_2025 | 50.00% | confirmado (11 meses) |
| Ratio_COOTAD_249 (cod) | 20.84% | pendiente_validacion |
| Ratio_COOTAD_249 (dev) | 14.19% | pendiente_validacion |
| TGI Holding | 66.79% | confirmado |
| ICPI real (Abr) | 17.45% | confirmado |

---

## QUÉ IGNORAR

| Carpeta / Archivo | Razón |
|---|---|
| `_historico\TERRA_ECIAP\` | Proyecto TERRA anterior — no es QUIRA |
| `_historico\ETL_scripts_legacy\` | Scripts ETL viejos — obsoletos |
| `ProyecT\historial_gold_master\` | Versiones v4.1-v5.4 — solo referencia |
| `C:\Desa\` | Proyecto TERRA antiguo — ignorar completamente |
| `metodologia_beta\` | Fuente Beta — no tocar durante Alpha |

---

## SISTEMAS EXTERNOS

### Neo4j (NUEVO — Alpha 1.0)

| Componente | Valor | Estado |
|---|---|---|
| DBMS | quira-alpha · v5.26.8 | ACTIVO |
| URI | bolt://localhost:7687 | Local |
| Nodos totales | 79 | Cargados 2026-05-31 |
| Circuitos | GAP_10PCT · AGUA_POTABLE · EQUIDAD | 3 cargados |
| Consulta bautismal | ADR-010 — EJECUTADA | Alpha 1.0 declarado |

> **Nota**: Neo4j Desktop debe estar corriendo localmente para que los scripts funcionen.
> DBMS: `quira-alpha` · Password: en poder del equipo · `bolt://localhost:7687`

### GitHub

| Repositorio | Contenido | Estado |
|---|---|---|
| `quira-os` (privado) | App Streamlit + QTMPs + scripts Neo4j | Rama main — activo |
| `quiraintelligence-web` (privado) | Sitio quiraintelligence.com | Activo |
| `quira-harvester` (privado) | Harvester de datos | Revisar propósito |

### Supabase

| Schema / Tabla | Contenido | Estado |
|---|---|---|
| `ack_atoms` | Átomos normativos QLEP | Activo |
| Métricas H73 | 41 métricas + cadena provenance | CHK-08 completado |
| Snapshot longitudinal | ICPI=17.45%, TGI=66.79% | Snapshot #1 establecido 2026-05-26 |

### Obsidian

| Vault | Backup |
|---|---|
| QUIRA_KB_Montecristi (39+ notas) | `quira-os\data\vault_backup_p2\` |

---

## ALERTA DE SEGURIDAD

> ⚠️ **Hay API keys en texto plano que deben ser revocadas o movidas a un gestor seguro:**
>
> | Archivo | Ubicación |
> |---|---|
> | `API Key Gemini.txt` | `Tecnic_SOLO_CONTIENE_API_KEY_GEMINI\` |
> | `GNOMIKA-LAB-ECIAP-API-KEY.txt` | `_historico\Para_API_keys_REVISAR\` |
>
> Acción requerida: revocar en la consola del proveedor y eliminar los archivos.

---

## PENDIENTES DE LIMPIEZA MENOR

| Item | Acción |
|---|---|
| `ProyecT\` — carpeta puede quedar con desktop.ini residual | Ignorar — solo artefacto Windows |
| `quira-harvester\` — propósito no verificado | Revisar con colega |
| `ProyecT\Documentos_Montecristi\Plan CNE ALcalde Montecristi.docx` | Puede estar duplicado con copia en Holding |

---

## HOJA DE RUTA — ESTADO

| Sprint | Entregable | Estado |
|---|---|---|
| Sprint Soberanía | H73 = 58/63 = 92.1% | COMPLETADO |
| Alpha 0.9 governance | 3 doc fundacionales + MAPA + STATE | COMPLETADO 2026-05-31 |
| Reorganización ecosistema | Carpetas limpias, audit-ready | COMPLETADO 2026-05-31 |
| **Sprint 2 — Neo4j** | **3 QTMPs cargados + consulta bautismal** | **COMPLETADO 2026-05-31** |
| **Alpha 1.0** | **Paradoja COOTAD_249 confirmada en grafo** | **DECLARADO 2026-05-31** |
| Beta | Índices Piso 2 · PDOT atomizado · Red Académica | SIGUIENTE |

---

*MAPA_ECOSISTEMA_QUIRA v2.1 — Alpha 1.0 declarado 2026-05-31*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
