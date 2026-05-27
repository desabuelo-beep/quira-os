# Gold Master v6.0 — Esquema de Diseño Canónico
**Estado: DISEÑO — Pendiente validación antes de construcción**
**Fecha: 2026-05-25 · Dylus Lab**

> v5.5 queda CONGELADO como referencia histórica.
> v6.0 es un libro nuevo de Excel con terminología TGI desde cero.
> Todo el contenido matemático del v5.5 migra. Solo cambia la organización y nomenclatura.

---

## Terminología Canónica v6.0

| Término Anterior (v5.x) | Término Canónico v6.0 | Notas |
|---|---|---|
| SIAP-ICPI Gold Master | Gold Master TGI v6.0 | Nombre oficial |
| SIAP Engine | Motor TGI | Nombre del motor Excel |
| H01_ICPI_MOTOR | G4.1_ICPI_GLOBAL | ICPI = Índice Compuesto de Progreso Institucional |
| ICPI_Global (69.93% / D2) | D2_Score | Eliminar colisión de nombres |
| ICPI (53.56% / composite) | ICPI_GLOBAL (mantener) | El composite real |
| H07b_EJECUCION_PRESUP | G3.3_D3_EJECUCION_GAD | Ejecución presupuestaria |
| H11b_MONITOR_POLITICAS | G4.3_MMP | Monitor de Progreso Mensual |
| H12_ICPI_ACUMULADO | G4.5_RC_M | Tabla RC-M longitudinal |
| H38_SAT_PROTOCOLOS | G5.4_PROTOCOLO_ACCION | Protocolo preventivo SAT |
| H73_OUTPUT_API | G6.1_OUTPUT_API | API para conector Python |
| H80-H89 (integridad) | → Supabase/Python | No en Excel |

---

## G1 — CONFIGURACIÓN (5 hojas)

| Hoja | Nombre | Contenido |
|---|---|---|
| G1.1 | CONFIG | Versión, municipio (130801), fecha_corte, pesos D1-D5, umbrales |
| G1.2 | MUNICIPIO_PROFILE | Perfil GADM Montecristi: área, población, 7 parroquias, 4 entidades holding |
| G1.3 | HOLDING_ENTIDADES | Registro: GAD central · EMAI · Bomberos · Patronato — códigos, responsables |
| G1.4 | PESOS_PONDERACIONES | Pesos TGI por dimensión, sub-indicador y variante histórica |
| G1.5 | CHANGELOG | Historial versiones Gold Master: v5.0 → v5.5 → v6.0 con hashes |

**Fuente principal:** Data doctrinal Dylus Lab. Reliability: 1.00

---

## G2 — FUENTES Y CONFIABILIDAD (4 hojas)

| Hoja | Nombre | Contenido |
|---|---|---|
| G2.1 | FUENTES_INSTITUCIONALES | Catálogo: DPE, SERCOP, CPCCS, SIGAD, eSIGEF, CNE, INEC, PDOT |
| G2.2 | RELIABILITY_SCORE | Score por fuente: Gold Master=0.99, DPE=0.95, SERCOP=0.95, CPCCS=0.80, Social=0.45 |
| G2.3 | INGESTA_CALENDARIO | Calendario: qué fuente, cuándo llega, cuándo se procesa, responsable |
| G2.4 | TRAZABILIDAD | Cadena: dato bruto → campo → fórmula → score → output API |

**Conecta con:** `app/services/reliability_tracker.py` (Sprint 3 P3)

---

## G3 — DIMENSIONES TGI D1-D5 (8 hojas)

| Hoja | Nombre | Migra de | Contenido |
|---|---|---|---|
| G3.1 | D1_LEGALIDAD | H03_*, H04_* | Score D1, Trust Score institucional, componentes PDOT-POA-PAC-LOTAIP |
| G3.2 | D2_PLANIFICACION | H11b_MONITOR | Score D2, 25 metas PDOT, D2_Score (antes mal llamado ICPI) |
| G3.3 | D3_EJECUCION_GAD | H07b_*, H08_* | Ejecución presupuestaria GAD central, Ti por período |
| G3.4 | D3_HOLDING | H17_*, H18_*, H19_* | Ti por entidad: EMAI / Bomberos / Patronato |
| G3.5 | D3_CONSOLIDADO | H21_* | D3 consolidado holding municipal, ponderado por presupuesto |
| G3.6 | D4_EQUIDAD | H99_* | IET por parroquia, IRS=79.7, Brecha_USD=$1.79M |
| G3.7 | D5_CAPACIDAD | H28_*, H29_* | IED 11 direcciones, ICM-SNP, estructura orgánica |
| G3.8 | D3_HISTORICO | H12b_*, H63_* | Serie temporal D3 por período (base RC-M) |

**Regla clave:** H07c_INGESTA_MENSUAL → se convierte en el FLUJO DIGITAL de ingesta.
El Director sube el informe firmado → SHA-256 → activa Ti_V en G3.3.

---

## G4 — ÍNDICES COMPUESTOS (5 hojas)

| Hoja | Nombre | Migra de | Contenido |
|---|---|---|---|
| G4.1 | ICPI_GLOBAL | H01_ICPI_MOTOR | ICPI=53.56% — composite de D1×0.20 + D2×0.20 + D3×0.25 + D4×0.25 + D5×0.10 |
| G4.2 | TGI_SCORE | H99_*, motor | TGI Score cantonal 5D ponderado |
| G4.3 | MMP | H25_MMP | Monitor Progreso Mensual: 25 metas × 12 meses |
| G4.4 | IED | H28_IED | Índice Eficiencia Directiva: 11 direcciones, LOSEP Art.76-82 |
| G4.5 | RC_M | H12b_*, H63_* | Tabla RC-M: Período | ICPI | D3_Ti | SAT-IV | Riesgo |

**Nota ICPI:** El ICPI_GLOBAL (53.56%) es el composite sistémico. El D2_Score (ex-ICPI) es solo el sub-índice de planificación. Nunca más se llamarán igual.

---

## G5 — SAT Y ALERTAS (5 hojas)

| Hoja | Nombre | Migra de | Contenido |
|---|---|---|---|
| G5.1 | SAT_CATALOGO | SAT_Catalogo | Catálogo SAT-0 a SAT-VIII: triple ancla legal+operativa+doctrinal |
| G5.2 | SAT_ACTIVAS | H38_*, H40_* | Alertas activas período actual: clasificación + estado + prioridad |
| G5.3 | SAT_LONGITUDINAL | H12b_* | Evolución temporal de alertas: activación, mitigación, reincidencia |
| G5.4 | PROTOCOLO_ACCION | H38_PROTOCOLOS | Protocolo preventivo por nivel SAT: qué hacer antes de que escale |
| G5.5 | AVEP_LENGUAJE | H40_* | Sistema AVEP: 🟢 Gestión por Mandato / 🟡 Transición / 🟠 Ocurrencia / 🔴 Atención Alta |

**AVEP es el lenguaje de comunicación al Alcalde. No es punitivo. Es predictivo.**

---

## G6 — OUTPUTS Y API (5 hojas)

| Hoja | Nombre | Migra de | Contenido |
|---|---|---|---|
| G6.1 | OUTPUT_API | H73_OUTPUT_API | 51+ métricas leídas por `app/connectors/gold_master.py` |
| G6.2 | SNAPSHOT_SCHEMA | (nuevo) | Esquema canónico del snapshot JSON Supabase |
| G6.3 | REPORTE_EJECUTIVO | H29_*, H30_* | 1 página: 5 preguntas del Alcalde respondidas con datos |
| G6.4 | REPORTE_DIRECTIVO | H29_*, H40_* | Reporte técnico: IED por dirección, SAT activas, tendencia |
| G6.5 | DASHBOARD_DATA | (nuevo) | Datos procesados listos para Streamlit — evita re-cálculo en Python |

**Regla conector Python:** `gold_master.py` lee exclusivamente G6.1_OUTPUT_API. Esta hoja nunca tiene fórmulas complejas — solo valores calculados de las otras hojas.

---

## G7 — GOBERNANZA (2 hojas)

| Hoja | Nombre | Migra de | Contenido |
|---|---|---|---|
| G7.1 | GOBERNANZA_SOD | H83_SOD_REGISTRY | Segregación de funciones: quién puede leer/editar/validar |
| G7.2 | POLITICA_INTEGRIDAD | H87_RECOVERY | Política de integridad: backup, recuperación, versionado |

**Las hojas H80-H89 del v5.5 (hash chain, model registry, snapshot registry, alerts log, evidence registry, trust score operativo) migran a Supabase y Python — no al Excel.**

---

## Hoja H07c digitalizada — Flujo de Ingesta Mensual

La hoja H07c del v5.5 tenía el concepto del flujo de ingesta. En v6.0:
- NO existe como hoja de Excel
- Se convierte en la **pantalla de ingesta por dirección** en el frontend (Ambiente Técnico)
- El director sube su informe firmado → sistema genera SHA-256 → activa Ti_V en G3.3
- Esa activación es el "corazón del IED en acción"

---

## Resumen del Esquema

| Grupo | Hojas | Función |
|---|---|---|
| G1 Configuración | 5 | Parámetros globales y estructura |
| G2 Fuentes | 4 | Trazabilidad y confiabilidad |
| G3 Dimensiones | 8 | D1-D5 con sus sub-motores |
| G4 Índices | 5 | ICPI, TGI, MMP, IED, RC-M |
| G5 SAT | 5 | Alertas, protocolos, AVEP |
| G6 Outputs | 5 | API, reportes, dashboard data |
| G7 Gobernanza | 2 | SOD, integridad |
| **TOTAL** | **34** | |

---

## Proceso de Construcción v6.0

```
1. Validar este esquema con el equipo
2. Crear libro nuevo: SIAP-TGI_GOLD_MASTER_v6.0_[fecha].xlsx
3. Construir G1 primero (parámetros guían todo lo demás)
4. Construir G3 (dimensiones son el motor real)
5. Construir G4 (índices dependen de G3)
6. Construir G5 (SAT depende de G3-G4)
7. Construir G6.1 OUTPUT_API (conecta con Python)
8. Construir G2, G6.2-6.5, G7
9. Actualizar conector Python: gold_master.py → leer G6.1
10. Freezar v5.5 → archivar en data/doctrinal/historical/
```

---

## Archivos Python a actualizar post-v6.0

- `app/connectors/gold_master.py` → cambiar nombre hoja H73 → G6.1_OUTPUT_API
- `app/services/gold_master_governance.py` (Sprint 3 P4) → apuntar a v6.0
- `data/doctrinal/gm_schema.json` → actualizar con esquema G6.1 v6.0
- `config.py` → actualizar GOLD_MASTER_PATH y GOLD_MASTER_VERSION

---

*Documento de diseño — no ejecutar hasta validación del equipo.*
*Gold Master v5.5 permanece operativo durante construcción del v6.0.*
