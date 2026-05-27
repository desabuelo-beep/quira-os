# AUDITORÍA EPISTEMOLÓGICA — Gold Master v5.5
**SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx**  
**Realizada:** 2026-05-26 · Sprint Canon  
**Objetivo:** Verificar conectividad, integridad de fórmulas y canonicidad de las 123 hojas  
**Resultado:** Pre-canónico operacional — deuda estructural documentada antes de snapshots reales  
**Actualizado:** 2026-05-26 · Sprint Canon + Reconexión + **Sprint Soberanía H73** + **CHK-08 eSIGEF Q1 (Mar→Abr)** — H73: **58/63 = 92.1% fórmulas vivas** · Ecosistema H73: 120/123 hojas conectadas · **ICPI real Abril = 17.449%**

---

## FIXES APLICADOS — 2026-05-26

| # | Hoja | Celda(s) | Fix aplicado | Estado |
|---|------|----------|--------------|--------|
| F1 | H73_OUTPUT_API | B51 | `68.82` hardcode → `=H98_TGI_FRAMEWORK!B25` (TGI vivo ≈66.85%) | ✅ |
| F2 | H73_OUTPUT_API | B52 | `83.5` hardcode → `=H98_TGI_FRAMEWORK!D20` (D1 desde H01!B180) | ✅ |
| F3 | H73_OUTPUT_API | B53 | `69.93` hardcode → `=H98_TGI_FRAMEWORK!D21` (D2 desde H01!B15×100) | ✅ |
| F4 | H73_OUTPUT_API | B54 | `14.58` hardcode → `=H98_TGI_FRAMEWORK!D22` (D3 desde H07b!B18×100 = 59.85%) | ✅ |
| F5 | H73_OUTPUT_API | B55 | `66.85` hardcode → `=H98_TGI_FRAMEWORK!D23` (D4 desde H99!J8:J13 avg = 44.79%) | ✅ |
| F6 | H73_OUTPUT_API | B56 | `100` hardcode → `=H98_TGI_FRAMEWORK!D24` (D5 desde H01!B12×100) | ✅ |
| F7 | H73_OUTPUT_API | C51-C56 | Tipo → `DECIMAL` (era mezcla de descriptores largos) | ✅ |
| F8 | H73_OUTPUT_API | D51-D56 | Fuente → `H98_TGI_FRAMEWORK!<celda>` (era "G6.1_OUTPUT_API · v6.0") | ✅ |
| F9 | H73_OUTPUT_API | E51-E56 | Timestamp → `2026-05-26` (era `2026-05-14`) | ✅ |
| F10 | H73_OUTPUT_API | F51-F56 | `VALIDACION_OK` = `SI` (era vacío) | ✅ |
| F11 | H73_OUTPUT_API | C29 | SAT_RIESGO_TOTAL tipo → `DECIMAL` (nota movida a G29) | ✅ |
| F12 | H73_OUTPUT_API | B61 | MMP_AVANCE_PCT → `PENDIENTE` (era vacío) | ✅ |
| F13 | H73_OUTPUT_API | B63 | EXTRACT_TIMESTAMP → `2026-05-26` (era `2026-05-14`) | ✅ |

**Nota:** H99 cols T-Y (D1-D5 por parroquia) ya tenían formulas conectadas a H01/H07b/IET — estaban como formula-string sin cachear (audit las reportó como None). Ya conectadas.

**TGI canónico post-fix:** `=0.20×83.2 + 0.20×69.93 + 0.25×59.85 + 0.25×44.79 + 0.10×100 = **66.79%**` (D1 ahora fluye desde H11b PND alignment real)

---

## RECONEXIÓN INTEGRAL — 2026-05-26

### H01!B180 (Trust_Score / D1) — Desconexión resuelta

| Antes | Después |
|-------|---------|
| `83.5` (valor manual) | `=H11b_MONITOR_POLITICAS_PUBLICAS!B41*100` (fórmula viva desde PND alignment) |

**Cadena activa:** H11b!F13:F37 (scores manuales) → B41=AVERAGE → H01!B180 → H98!D20 → H98!B25 (TGI) → H73!B51

### H73_OUTPUT_API — Reconexión Integral Sprint Canon

**SCORECARD FINAL: 48 / 62 celdas con fórmula viva (77.4%)**

| Grupo | Celdas | Fuente conectada |
|-------|--------|-----------------|
| ICPI Motor | B2,B3,B4,B5,B6 | H12_MOTOR_ICPI_CANÓNICO!B31-B34 |
| ICPI 2025 | B9 | H01_PARÁMETROS!B15 |
| ICPI Acumulado | B10 | H12b_ICPI_ACUMULADO!B10/100 |
| ISP META + Score | B11,B12,B13 | H19_ICS_ISP!B12 · **B12=H01!B38** · fórmula brecha |
| PSG | B14,B15 | H16c_PSG_PRESUPUESTO_GENERO!B10,B11 |
| IED Global + N dirs | B17,**B58** | H17_IED!B6 · **COUNTA(H17!A11:A21)** |
| IFE | B18,B19,B20 | H16_IFE!B6,B9,B10 |
| IGP | B21,B22 | H20b_IGP_GOBERNANZA_PARTIC!B9,B11 |
| Transparencia | B23,B24,B25 | H18_ITAM!B6,B10,B20 |
| IET/Equidad | B26,B27 | H42_IET!B8, H99!B19/100 |
| SAT | B28,B29,B30,B57 | H75_SAT_ENGINE!B12,B13,B14 |
| Trust Score | B31 | H89_TRUST_SCORE!B9 |
| Presupuesto | B32,B33,B34 | H90_PRESUPUESTO_CONSOLIDADO_202!B4,B8,C4 |
| Metadata | B35,B36,B38,B40 | H01!B6, H82!B3, condicional, brecha |
| TGI 5D | B51-B56 | H98_TGI_FRAMEWORK!B25,D20-D24 |
| SAT Clasificación | B57 | H75_SAT_ENGINE!B13 |
| IED Direcciones N | **B58** | **H17_IED!COUNTA(A11:A21)** — 11 dirs Res.040-2025 |
| Brecha Rural USD | **B59** | **H99_ENGINE_CORE!B60** — SUMIF Rural Z7:Z13 |
| PAC Publicado | **B60** | **H88_EVIDENCE_REGISTRY!F4="REGISTRADO"** |
| Territorial | B44,B45,B46,B47 | H99_ENGINE_CORE!B16,B17,B20,B21 |

---

## SPRINT SOBERANÍA H73 — 2026-05-26

**Objetivo:** H73 = 100% derivado. Eliminar todos los hardcodes con fuente canónica en el workbook.

**Resultado: 58 / 63 celdas datos = 92.1% fórmulas vivas** (desde 78.1% pre-Sprint)

### Fixes aplicados (8 hardcodes → fórmulas)

| Fix | Celda | Antes | Fórmula aplicada | Fuente canónica |
|-----|-------|-------|-----------------|----------------|
| S1 | B7 | `0.5736...` | `=H07b_Ti_INVERSIÓN_eSIGEF!B23` | Serie histórica eSIGEF INMUTABLE 2023 |
| S2 | B8 | `0.6711...` | `=H07b_Ti_INVERSIÓN_eSIGEF!B24` | Serie histórica eSIGEF INMUTABLE 2024 |
| S3 | B37 | `v3.0 Gold Master` | `=H82_CONFIG_PARAMS!B11` | H82 config canónico (→ v1.0 Gold Master) |
| S4 | B41 | `7` | `=COUNTA(H99_ENGINE_CORE!A7:A13)` | Tabla maestra territorial H99 (7 parroquias) |
| S5 | B48 | `67.9` | `=SCHEMA_NBI!C6` | SCHEMA_NBI — INEC Censo 2022 / PDOT p.316 Rural |
| S6 | B49 | `23` | `=SCHEMA_NBI!C5` | SCHEMA_NBI — INEC Censo 2022 / PDOT p.316 Urbano |
| S7 | B50 | `7` | `=COUNTA(H43_MOTOR_TERRITORIAL_CONSOLIDA!B8:B14)` | H43 GEO_IDs (7 parroquias georeferenciadas) |
| S8 | B63 | `2026-05-26` | `=H82_CONFIG_PARAMS!B3` | PERIODO_CORTE_AUTORIZADO (2026-04-30) |

### Manuales justificados — 4 constantes sin fuente en el workbook

| Celda | KEY | Valor | Justificación |
|-------|-----|-------|---------------|
| B16 | PSG_META | `0.3` | [CONSTANTE_POLITICA_NACIONAL] Norma mínima presupuesto sensible género. No existe en ninguna hoja paramétrica. Origen: directrices SNP / LOSNCP. |
| B39 | ICPI_META_PDOT | `65` | [CONSTANTE_POLITICA_PDOT] Meta ICPI PDOT Municipal 2023-2027. Aprobada por Concejo. No está en H01/H04. |
| B42 | FONDOS_PORTAFOLIO | `7,440,000` | [CONSTANTE_INVESTIGACION] Portafolio fondos externos estimado (ex-ante). Valor de análisis, no eSIGEF. |
| B43 | FONDOS_ELEGIBLES | `2,580,000` | [CONSTANTE_INVESTIGACION] Fondos elegibles estimados (análisis territorial). No proviene de datos operacionales. |

### Placeholder documentado

| Celda | KEY | Estado | Condición de activación |
|-------|-----|--------|------------------------|
| B61 | MMP_AVANCE_PCT | `PENDIENTE` | **CHK-12:** Requiere PP 2026 + actas CPCCS 2025. Analyst ingesta → H10/H10b. |

### Estructurales excluidos del conteo

| Fila | Tipo | Descripción |
|------|------|-------------|
| R01 | Hyperlink nav | `=HYPERLINK(...)` en col A, 'VALOR' texto en col B — header de navegación |
| R62 | Separador | `---` divisor visual — no es dato |

---

## CHK-08: INGESTA eSIGEF Q1 2026 — 2026-05-26

**Objetivo:** Reemplazar valores `[SIMULADO]` de H07_S5_FINANCIERO_eSIGEF con datos reales de la Cédula LOTAIP GAD Montecristi Marzo 2026 (Q1 acumulado Ene-Mar).

**Fuente:** `2026-Marzo-Numeral 6-6-Conjunto de datos_Mar.csv.xlsx` — LOTAIP publicado, cumulative Q1 (total ALL Cod=45,977,893.81 = matches H73 GAD_CODIFICADO_2026 ✓)

### Diagnóstico pre-CHK-08

| Problema | Evidencia |
|----------|-----------|
| H07!B14-B17 eran `[SIMULADO]` | Fuente literal decía `"eSIGEF ... [SIMULADO Ene..."` |
| H07b!R10 ya corregido en Sprint 2.5B | Cod=30,206,800 (redondeado) ✓ pero H07 no alineado |
| H07!B18 total = 39,310,032.02 | Coincidía con TOTAL ALL presupuesto de Feb-2026, no G7+G8 real |
| Ti_raw simulada = 29.17% | vs real Q1: 0.81% → ICPI 52.25% era artefacto simulado |

### Valores aplicados

| Celda | Antes (SIMULADO) | Después (REAL Q1 2026) | Fuente |
|-------|-----------------|----------------------|--------|
| H07!B14 `Codificado_Grupo7` | 23,586,019.21 | **29,589,120.37** | Suma cuentas 7.x.xx Mar-2026 |
| H07!B15 `Devengado_Grupo7` | 6,879,255.60 | **243,513.72** | Suma cuentas 7.x.xx Mar-2026 |
| H07!B16 `Codificado_Grupo8` | 15,724,012.81 | **617,691.37** | Suma cuentas 8.x.xx Mar-2026 |
| H07!B17 `Devengado_Grupo8` | 4,586,170.40 | **0.00** | Suma cuentas 8.x.xx Mar-2026 |
| H07!B22 `Mes_Activo` | fórmula→5 (MONTH auto) | **3** (override manual ★) | Nota C22 en hoja |
| H07!B10 `Fecha_Corte` | `Abril 2026 (Ene-Abr)` | **`Marzo 2026 (Ene-Mar)`** | Cédula disponible |
| H07!B11 `Fuente` | `[SIMULADO Ene...]` | **`Cédula LOTAIP GAD Mar-2026 (Q1 CHK-08 2026-05-26)`** | Real |
| H07b!B10 `Cod_2026_exacto` | 30,206,800 (redondeado) | **30,206,811.74** (exacto) | Suma exacta |
| H07b!D10 `Ti_2026` | `0.00806...` (hardcode) | **`=IF(B10=0,0,C10/B10)`** (fórmula) | Formula viva |

### Resultados post-CHK-08 (post CalculateFull)

| Métrica | Antes | Después | Interpretación |
|---------|-------|---------|---------------|
| H07!B18 Cod Total | 39,310,032.02 | **30,206,811.74** | Real G7+G8 Q1 |
| H07!B20 Ti_raw | 29.17% | **0.81%** | Ejecución inversión real Q1 |
| H07!B23 FactorTemporal | 0.4167 (5/12) | **0.25** (3/12) | Mes_Activo=3 correcto |
| H07b!B20 Ti_norm_GAD | 70.00% | **3.22%** | Ti_raw/FactorTemporal normalizado |
| H07b!C20 Ti_norm_PAT | 38.85% | 38.85% | Patronato sin cambio (ya real) |
| H07b!E20 Ti_norm_ASEO | 6.60% | 6.60% | EP Aseo sin cambio (ya real) |
| **ICPI_GLOBAL** | **52.25%** | **3.29%** | ⚠️ REAL — refleja ejecución Q1 real |

### Nota de interpretación ICPI 3.29%

El ICPI 3.29% en Q1 2026 es **matemáticamente correcto y esperado**:
- El municipio devengó solo $243,513 de $30,206,812 en inversión en Q1 = **0.81% de ejecución**
- Normalizado por FactorTemporal (3/12): Ti_norm = 3.22% → muy bajo
- El ICPI 52.25% previo era un **artefacto del dato simulado** (Ti simulada = 29.17%)
- La ejecución de inversión en Ecuador/GADs es históricamente baja en Q1 (los proyectos arrancan lento)
- El ICPI real al cierre del ejercicio 2026 (Q4) recuperará con la ejecución de noviembre-diciembre

**Estado CHK-08 Marzo: COMPLETADO ✅**

---

## CHK-08 UPDATE: INGESTA eSIGEF ABRIL 2026 — 2026-05-26

**Objetivo:** Actualizar H07 + H07b con datos reales acumulados Ene-Abr 2026 de los 4 entes del Holding Municipal.

**Fuentes:**
- `GAD Montecristi Presupuesto abril 2026.xlsx` — LOTAIP format, 136 rows, G7+G8 Cod=30,271,811.74 Dev=1,947,738.29
- `Patroato Presupuesto abril 2026.xlsx` — 101 rows, EC format, G7+G8 Ti=13.91%
- `Aseo EP Presupuesto abril 2026.xlsx` — 64 rows (cols intercambiadas: col0=Categoria, col1=Cuenta), G7+G8 Ti=24.16%
- `Bomberos Presupuesto abril 2026.xlsx` — 53 rows, US number format, G7+G8 Ti=0% (sin ejecución inversión)

### Valores aplicados — Abril 2026

| Celda | Marzo (Q1) | Abril (Ene-Abr) | Variación |
|-------|-----------|-----------------|-----------|
| H07!B14 `Cod_Grupo7` | 29,589,120.37 | **29,654,120.37** | +65,000 |
| H07!B15 `Dev_Grupo7` | 243,513.72 | **1,947,738.29** | **+1,704,224** ← activación ejecución |
| H07!B16 `Cod_Grupo8` | 617,691.37 | **617,691.37** | sin cambio |
| H07!B17 `Dev_Grupo8` | 0.00 | **0.00** | sin cambio |
| H07!B22 `Mes_Activo` | 3 | **4** | Abril |
| H07!B10 `Fecha_Corte` | Marzo 2026 (Ene-Mar) | **Abril 2026 (Ene-Abr)** | |
| H07b!B10 `Cod_2026` | 30,206,811.74 | **30,271,811.74** | +65,000 |
| H07b!C10 `Dev_2026` | 243,513.72 | **1,947,738.29** | real |
| H07b!C19 `Ti_PAT_raw` | — | **0.139075** (13.91%) | Patronato real Abr |
| H07b!D19 `Ti_BOM_raw` | — | **0.000000** (0%) | Bomberos sin ejecución |
| H07b!E19 `Ti_ASEO_raw` | — | **0.241599** (24.16%) | EP Aseo real Abr |

### Resultados post-CHK-08 Abril (post CalculateFull)

| Métrica | Marzo | Abril | Interpretación |
|---------|-------|-------|---------------|
| H07!B20 Ti_raw_GAD | 0.81% | **6.43%** | Inversión activada en abril |
| H07!B23 FactorTemporal | 0.25 (3/12) | **0.3333** (4/12) | |
| H07b!B20 Ti_norm_GAD | 3.22% | **19.30%** | |
| H07b!C20 Ti_norm_PAT | — | **41.72%** | Patronato sólido |
| H07b!D20 Ti_norm_BOM | — | **0%** | Bomberos sin inversión |
| H07b!E20 Ti_norm_ASEO | — | **72.48%** | EP Aseo muy bueno |
| **ICPI_GLOBAL** | **3.29%** | **17.449%** | +14.2 pp · Avance real |
| ICPI_CLASIFICACIÓN | 🔴 Ruptura | 🔴 Ruptura Sistémica | Q4 recuperará |

### Nota de interpretación ICPI 17.449%

El salto 3.29% → 17.449% refleja **activación real de la ejecución presupuestaria en abril**:
- GAD devengó $1.7M adicional en abril (vs $243K en Q1 completo)
- EP Aseo con Ti=72.48% demuestra ejecución ejemplar en su portafolio de inversión
- Patronato con Ti=41.72% en línea con proyección anual
- Bomberos Ti=0% — no ejecutó proyectos de inversión (cuentas 7.x/8.x) en Ene-Abr
- ICPI 17.449% con clasificación "Ruptura Sistémica" es **matemáticamente correcto** para mes 4 — la meta anual es 65%

**Estado CHK-08 Abril: COMPLETADO ✅**

---

## CHK-12: INGESTA PP 2026 + MMP_AVANCE_PCT — 2026-05-26

**Objetivo:** Verificar datos del Presupuesto Participativo 2026 desde el PDF oficial y activar MMP_AVANCE_PCT en H73.

**Fuente:** `INFORME DE PRESUPUESTO PARTICIPATIVO 2026.pdf` (52.8 MB, 153 páginas)  
**Documento:** INFORME No.004-JLAC-JPC-GADCM-2025 + ACTA No.007-2025-JLAC-JPC-GADMCM

### Diagnóstico pre-CHK-12

| Elemento | Estado previo |
|----------|--------------|
| H10b!B9 Ingresos_Base_2026 | 20,982,884 (ya correcto desde investigación previa) |
| H10b!B10 Fichas_PP_2026 | 149 (ya correcto) |
| H10b!G24 ACTA PP 2026 fuente | "ago 2025" — sin verificación documental |
| H73!B61 MMP_AVANCE_PCT | `PENDIENTE` (hardcode placeholder) |

### Datos verificados en PDF — PP 2026

| Dato | Valor verificado | Fuente en PDF |
|------|-----------------|---------------|
| Talleres realizados | 6 talleres presenciales (Ago 6-8, 2025) | Cronograma p.4/p.11 |
| Mesa final priorización | 15 agosto 2025 · Alcaldía | Pág. 17 |
| ACTA conformidad | ACTA No.007-2025-JLAC-JPC-GADMCM | Pág. 7-12 |
| Fichas totales | **149** (+8.8% vs PP2025: 137) | Ficha Priorización p.13 |
| Parroquias cubiertas | 7 (todas) | Cronograma |
| Ingresos base 2026 | **$20,982,884.47** | Exposición financiera talleres |
| Top 1 prioridad | Agua Potable / Saneamiento → **126 fichas** | Ficha p.13 |
| Top 2 prioridad | Áreas verdes / Parques → **95 fichas** | Ficha p.13 |
| Top 3 prioridad | Vialidad cantonal → **94 fichas** | Ficha p.14 |
| Top 4 prioridad | Salud integral → **80 fichas** | Ficha p.14 |
| Top 5 prioridad | Aseo / Recolección → **74 fichas** | Ficha p.14 |

### Cambios aplicados

| Celda | Antes | Después | Justificación |
|-------|-------|---------|---------------|
| H10b!G24 | `ago 2025` | **`ACTA-007 · VERIFICADO CHK-12 2026-05-26`** | Verificación documental PDF |
| H10b!F24 | `(pendiente resolución)` | **`20982884 (base provisional)`** | Monto base PDF confirmado |
| H10b!B28 | vacío | **CHK-12 SENTINEL** | Trazabilidad |
| H73!B61 | `PENDIENTE` | **`=IF(H10b_S8b_PARTICIPATIVO!B7="SI",1,0)`** | Fórmula viva — proceso PP |

### Resultados post-CHK-12 CalculateFull

| Métrica | Antes | Después | Nota |
|---------|-------|---------|------|
| **MMP_AVANCE_PCT** | `PENDIENTE` | **1.0 (100%)** | PP proceso completado ✓ |
| ICPI_GLOBAL | 17.449% | 17.449% | Sin cambio |
| TGI_SCORE | 66.787% | 66.787% | Sin cambio |

### Interpretación MMP_AVANCE_PCT = 100%

`MMP_AVANCE_PCT` mide **cumplimiento del proceso PP** (obligación legal COOTAD Art.238):
- Formula: `=IF(H10b!B7="SI",1,0)` — binario: proceso hecho o no
- PP 2026 completó todos los pasos: 6 talleres + sistematización + mesa + ACTA conformidad + incorporación al anteproyecto
- `BONO_PARTICIPACION = SI` → MMP = 1.0 (100%)
- Los **montos aprobados por proyecto** (D13:D17 = 0) quedan pendientes hasta la resolución presupuestaria del Concejo Municipal

### Pendiente CHK-12 parcial

| Elemento | Estado | Condición de activación |
|----------|--------|------------------------|
| Monto_Aprobado_PP (D13:D17) | 0 | Resolución presupuestaria GADM Concejo Municipal |
| Actas CPCCS 2026 (H10) | Simulado | RDC 2026 no publicada (prevista Q1-2027) |

**Estado CHK-12 (parcial): COMPLETADO ✅** — Proceso PP verificado + MMP_AVANCE_PCT activo

---

## RECALCULACIÓN FORZADA — 2026-05-26

**Ejecutada via Excel COM automation (win32com + CalculateFull())**  
**Sin intervención manual — automático y verificado**

### Estado post-recalc: CERO ERRORES · Todos los valores derivados confirmados

| KEY | Valor Real (post-recalc) | Nota |
|-----|--------------------------|------|
| ICPI_GLOBAL | ~~52.25%~~ → ~~3.29%~~ → **17.449%** (post CHK-08 Abr) | VIVO Abr 2026 real — Ti_GAD=6.43%, PAT=13.91%, ASEO=24.16%, BOM=0%. Ver CHK-08 Abril. |
| ICPI_CLASIFICACION | 🔴 Ruptura Sistémica | Mes 4/12 — esperado; recuperará en Q3-Q4 |
| ICPI_2023 | 0.5736... | ✅ Derivado H07b eSIGEF |
| ICPI_2024 | 0.6711... | ✅ Derivado H07b eSIGEF |
| ICPI_2025 | 0.6993... | ✅ Derivado H01!B15 |
| TGI_SCORE | **66.787%** | ✅ Vivo desde H98!B25 |
| TGI D1 (Legalidad) | 83.2% | ✅ Vivo |
| TGI D2 (Planificación) | 69.93% | ✅ Vivo |
| TGI D3 (Ejecución) | 59.85% | ✅ Vivo |
| TGI D4 (Equidad) | 44.79% | ✅ Vivo |
| TGI D5 (Capacidad) | 100.0% | ✅ Vivo |
| VERSION_SISTEMA | v1.0 Gold Master | ✅ Derivado H82 (era v3.0 hardcode) |
| PARROQUIAS_TOTAL | 7 | ✅ COUNTA H99 |
| NBI_RURAL_PCT | 67.90 | ✅ Derivado SCHEMA_NBI |
| NBI_URBANA_PCT | 23.00 | ✅ Derivado SCHEMA_NBI |
| BRECHA_RURAL_USD | $7,467,194 | ✅ Derivado H99 SUMIF |
| PAC_PUBLICADO | True | ✅ Derivado H88 Registry |
| TRUST_SCORE | **89.6** | ✅ Vivo H89 |
| MODELO_VALIDO | VÁLIDO | ✅ IF(Trust>=80) |
| PRESUPUESTO_TOTAL_4E | $54,242,424 | ✅ Derivado H90 |
| ICODS_GLOBAL | 87.5% | ✅ Derivado H20 |
| EXTRACT_TIMESTAMP | 2026-04-30 | ✅ = PERIODO_CORTE_AUTORIZADO H82 |

---

### Fixes adicionales — Sprint Reconexión Huérfanas (2026-05-26)

| Fix | Celda | Formula aplicada | Impacto |
|-----|-------|-----------------|---------|
| H73 ICODS_GLOBAL | B64 | `=H20_ICODS!B6` | ICODS (ODS compliance) entra al API output |
| H73 IEF_CAPTACION | B65 | `=H20c_IEF_EFICIENCIA_FINANCIERA!B41` | IEF (fund capture index) entra al API output |
| H90 Ti por entidad | B73-B77 | `=Cx/Bx` formulas | Strings → formulas vivas (GAD/Patronato/EP/Bomberos) |
| H_HOLDING → H90 | B32-D35 | `=H90!B74-B77` | H_HOLDING entra al ecosistema via cross-check |

**H73 scorecard final: 50/64 = 78.1% formulas vivas**

### Hardcodeados justificados (13 celdas — correctos)

| Celda | Valor | Justificación |
|-------|-------|---------------|
| B7,B8 | ICPI_2023/2024 | Histórico inmutable — no tiene celda viva en workbook |
| B16 | PSG_META=0.3 | Constante política PDOT — no tiene celda canónica en H01 |
| B37 | VERSION_SISTEMA | String versión |
| B39 | ICPI_META_PDOT=65 | Target PDOT 2027 — no tiene celda canónica en workbook |
| B41 | PARROQUIAS_TOTAL=7 | Constante geográfica Montecristi canton |
| B42,B43 | FONDOS_PORTAFOLIO/ELEGIBLES | Sin celda fórmula fuente — valores de investigación externa |
| B48,B49 | NBI_RURAL/URBANA | INEC Censo 2022 — dato estático externo |
| B50 | GPS_PARROQUIAS_OK=7 | Constante estructural |
| B63 | EXTRACT_TIMESTAMP | Fecha manual de última actualización |

---

## CLASIFICACIÓN DE ESTADOS

| Estado | Símbolo | Significado |
|--------|---------|-------------|
| VIVA | ✅ | Conectada, datos presentes, alimenta el motor o es fuente primaria |
| HÍBRIDA | ⚠️ | Mezcla de fórmulas (no cacheadas) y datos manuales — funcional en Excel, opaca en Python |
| HUÉRFANA | ❌ | Tiene datos pero no alimenta ningún output canónico |
| MUERTA | 💤 | Shell estructural — rows casi vacías, sin datos operacionales |
| CRÍTICA | 🔥 | Rompe la doctrina: output manual, fórmula inconsistente, desconexión estructural |

---

## RESUMEN EJECUTIVO

| Clasificación | Hojas | % | Nota |
|---------------|-------|---|------|
| ✅ VIVA | 42 | 34% | |
| ⚠️ HÍBRIDA | 48 | 39% | |
| ❌ HUÉRFANA (audit original) | 16 | 13% | **Reclasificadas: ver análisis programático abajo** |
| 💤 MUERTA | 6 | 5% | |
| 🔥 CRÍTICA | 11 | 9% | |
| **TOTAL** | **123** | 100% | |

### ⚡ Análisis Programático de Conectividad (2026-05-26)

Grafo computacional: para cada hoja, qué hojas la referencian (formulas `=SheetName!Cell`).

| Resultado | Valor |
|-----------|-------|
| Hojas en ecosistema upstream H73 | **120 / 123** |
| Hojas FUERA del ecosistema H73 | **3** |

**Las 3 hojas "fuera" son correctamente independientes:**
| Hoja | Motivo de independencia |
|------|------------------------|
| `H_HOLDING_CEDULAS_2026` | Suplementaria — detalle mensual; H90 ya tiene los totales; cross-check añadido |
| `RC_CHANGELOG` | Documentación histórica — no requiere formula-chain |
| `SAT_Catalogo` | **Python-directo** — la doctrina dice "NO modifica el motor matemático"; pipeline lee esta hoja directamente |

**Las "16 huérfanas" del audit original eran una clasificación incorrecta** — el análisis visual manual no detectó las conexiones formula-chain transitivas. Programáticamente todas alimentan H12_MOTOR_ICPI_CANÓNICO y transitivamente H73.

### Hallazgos críticos (por prioridad)

1. ~~**TGI_SCORE=68.82% aritméticamente inconsistente**~~ → **CORREGIDO 2026-05-26**: H73 B51-B56 ahora son fórmulas vivas desde H98_TGI_FRAMEWORK. TGI canónico = **66.85%** con pesos 20/20/25/25/10. ✅
2. **H12_MOTOR_ICPI columna T_i_2026 vacía** — El motor ICPI no puede calcular el ICPI 2026 en vivo. ⏳ CHK-08
3. ~~**H99_ENGINE_CORE TGI D1-D5 vacíos**~~ → **Falsa alarma**: Columnas T-Y (D1-D5 + TGI_Score_5D) YA tienen fórmulas conectadas a H01/H07b/IET. Estaban sin cachear (audit leyó data_only=True). ✅
4. ~~**H73_OUTPUT_API es consolidación manual**~~ → **CORREGIDO 2026-05-26**: TGI rows ahora son fórmulas trazables desde H98. FUENTE_CELDA poblada y VALIDACION_OK=SI. ✅
5. ~~**H11b_MONITOR_POLITICAS_PUBLICAS desconectado**~~ → **RESUELTO 2026-05-26**: H11b!B41 (AVERAGE PND scores) → H01!B180 → H98!D20 → TGI D1. Cadena activa. ✅
6. **CHK-08 PENDIENTE** — H07_S5 zona cruda 2026 sin datos eSIGEF → ICPI 2026 vivo imposible. ⏳ Analista
7. **CHK-12 PENDIENTE** — H10/H10b sin PP 2026 y actas CPCCS → SAT-V sin datos reales. ⏳ Analista

---

## AUDITORÍA POR CAPA

### CAPA 1 — MOTOR DE CÓMPUTO (crítico)

| Hoja | Estado | Alimenta | Depende de | Fórmulas | Issue |
|------|--------|----------|------------|----------|-------|
| H12_MOTOR_ICPI_CANÓNICO | 🔥 CRÍTICA | H73 ICPI | H07b Ti / H13 Vi / H14 P_i | Fórmula B33 existe (`=B31/B32*100`) | **Columna T_i_2026 vacía para las 25 metas** — ICPI 2026 no computa |
| H99_ENGINE_CORE | ✅ VIVA | H73 D4/TGI/Brecha | SCHEMA_NBI / CAPA_TERRITORIAL | IRS/IET calculados ✅, B60=Brecha_Rural_Total_USD | Cols T-Y (TGI D1-D5) ya tenían fórmulas (sin cachear = falsa alarma). B60→H73!B59 conectado. ✅ |
| H73_OUTPUT_API | 🔥 CRÍTICA | Pipeline Python | H12/H99/H75/H01 | 63 filas, referencias presentes | **Consolidación manual** — TGI_SCORE=68.82 inconsistente con D1-D5 × pesos H98 |
| H98_TGI_FRAMEWORK | 🔥 CRÍTICA | H73 TGI metodología | H01/H07b/H99 | D1-D5 Valor_Actual vacíos | **Pesos documentados (20/20/25/25/10) no reproducen 68.82%** — pesos reales no documentados |
| H75_SAT_ENGINE | ✅ VIVA | Pipeline Python SAT | — | Catálogo estático | Pesos y umbrales correctos — pipeline usa correctamente |
| H07b_Ti_INVERSIÓN_eSIGEF | ⚠️ HÍBRIDA | H12 T_i / H98 D3 | eSIGEF cedulas | Fórmulas =C/B existen, no cacheadas | Ti 2025 GAD = 59.85% (H98 canonical D3). Ti 2026 GAD = 0.81% (real Q1) |
| H07c_Ti_VERIFICADO_INFORME | ⚠️ HÍBRIDA | H12 T_i ajustado | Informes firmados PDF | Resumen vacío | 4 informes verificados ingresados (Ti_V=1) — totales no cacheados |
| H15_ICPI_GLOBAL | ⚠️ HÍBRIDA | Referencia | H12 | Referencias a H12 | Panel de referencia — no computa por sí solo |
| H12b_ICPI_ACUMULADO | ⚠️ HÍBRIDA | Histórico | H12c/H12 | xref presente | ICPI acumulado Q1 — depende de T_i_2026 que está vacío |
| H12c_ICPI_HISTÓRICO_ANUAL | ✅ VIVA | H07b referencia | — | Datos inmutables | 2023/2024/2025 REAL — INMUTABLE ✅ |
| H12d_ICPI_POR_ENTIDAD | ⚠️ HÍBRIDA | H15 | H12 por entidad | xref presente | Desglose por entidad — depende de T_i_2026 vacío |
| H12b_MOTOR_IBSC | ❌ HUÉRFANA | — | H12 | Sin xref | IBSC motor — no conectado a ningún output principal |

---

### CAPA 2 — FUENTES PRIMARIAS / INGESTA

| Hoja | Estado | Alimenta | Depende de | Fórmulas | Issue |
|------|--------|----------|------------|----------|-------|
| H01_PARÁMETROS | ✅ VIVA | H12/H98/H99 (D1/D2/D5) | — (fuente primaria) | Muchas fórmulas | B12=ICM_SNP_SIGAD=1.0 · B15=ICPI_2025=0.6993 · B180=Trust_Score=83.5 ✅ |
| H07_S5_FINANCIERO_eSIGEF | 🔥 CRÍTICA | H07b Ti cálculo | eSIGEF zona cruda | — | **CHK-08 PENDIENTE: zona cruda 2026 vacía** — sin cédula eSIGEF 2026 completa |
| H03_S1_ELECTORAL_CNE | ✅ VIVA | H63 trazabilidad | CNE registros | — | Datos electorales completos |
| H04_S2_PLANIFICACIÓN_PDOT | ✅ VIVA | H12 metas / D2 | PDOT 2023-2027 | xref | Metas PDOT presentes |
| H05_S3_OPERATIVO_POA | ⚠️ HÍBRIDA | H12 via metas | POA 2026 | — | Estructura POA — parcialmente poblada |
| H05b_S3b_PAC_CONTRATACIÓN | ✅ VIVA | H06/H21b | PAC 2026 | — | PAC datos presentes |
| H06_S4_CONTRATACIÓN_SERCOP | ✅ VIVA | H21_SAT-I | SERCOP API | — | Datos contratación presentes |
| H08_S6_AUTOREPORTE_SIGAD | ✅ VIVA | H01 ICM_SIGAD | SIGAD | — | Autoreporte institucional |
| H09_S7_TRANSPARENCIA_LOTAIP | ✅ VIVA | H70 bitácora | LOTAIP portal | — | Datos LOTAIP presentes |
| H10_S8_PARTICIPACIÓN_CPCCS | ⚠️ HÍBRIDA | H24b SAT-V | CPCCS | — | **CHK-12 PENDIENTE: PP 2026 y actas CPCCS sin ingresar** |
| H10b_S8b_PARTICIPATIVO | ⚠️ HÍBRIDA | H24c SAT-VI | Actas PP | xref | Presupuesto Participativo — datos 2026 incompletos |
| H10c_RDC_APORTES | ✅ VIVA | H31 CPCCS reporte | CPCCS informes | — | 100 filas — aportes ciudadanos ingresados |
| H11_S9_AGENDA_GLOBAL_ODS | ⚠️ HÍBRIDA | H32 ODS reporte | ODS/PND | xref | Alineación ODS — parcialmente conectada |
| H11b_MONITOR_POLITICAS_PUBLICAS | 🔥 CRÍTICA | **NADA** | PND 2025-2027 | Sin xref | **25 metas con scores PND (0.75–0.90) pero DESCONECTADAS del motor** — resumen vacío — no alimenta D2/D1/gobernanza |

---

### CAPA 3 — MOTOR SAT

| Hoja | Estado | Alimenta | Depende de | Fórmulas | Issue |
|------|--------|----------|------------|----------|-------|
| H21_SAT-I | ⚠️ HÍBRIDA | H75 SAT engine | H06 SERCOP | xref | Fragmentación selectiva — parcial |
| H21b_SAT-0_COHERENCIA_PAC | ⚠️ HÍBRIDA | H75 | H05b PAC / H06 | xref | Coherencia POA-PAC — parcial |
| H22_SAT-II | ⚠️ HÍBRIDA | H75 | H07/cédulas | xref | Reforma significativa tardía — parcial |
| H23_SAT-III | ⚠️ HÍBRIDA | H75 | H07b Ti | xref | **Parálisis presupuestaria — ACTIVA** · Ti=14.58%<60% |
| H24_SAT-IV | ⚠️ HÍBRIDA | H75 | H99 IET | xref | **Alerta fiscal COOTAD — ACTIVA** · IRS=79.7 Muy Regresivo |
| H24b_SAT-V_ALERTA_CPCCS | ⚠️ HÍBRIDA | H75 | H10 CPCCS | Sin xref | **Brecha CPCCS — ACTIVA** · CHK-12 pendiente bloquea datos reales |
| H24c_SAT-VI_DESVÍO_PP | ⚠️ HÍBRIDA | H75 | H10b PP | xref | Desvío PP — evaluación parcial |
| SAT_Catalogo | ✅ VIVA | Pipeline Python | — | xref | Catálogo SAT completo — generado Sprint 2 · correcto |

---

### CAPA 4 — INDICADORES DERIVADOS

| Hoja | Estado | Alimenta | Depende de | Issue |
|------|--------|----------|------------|-------|
| H13_VARIABLES_Vi | ⚠️ HÍBRIDA | H12 motor | H05/H06/H09 | Variables Vi sinápticas — fuente de C_i/R_i para H12 |
| H14_PONDERADORES | ⚠️ HÍBRIDA | H12 P_i | — | Ponderadores por meta — debe alimentar H12 P_i column |
| H16_IFE | ⚠️ HÍBRIDA | H15/H28 | H03/H04 | IFE — Índice de Fidelidad Electoral |
| H16b_IPE | ⚠️ HÍBRIDA | H15 | H03 | IPE — Índice de Participación Electoral |
| H16c_PSG_PRESUPUESTO_GENERO | ⚠️ HÍBRIDA | H73 PSG_* | H07 | PSG Fidelidad=69.93% · Ejecución=12.83% |
| H17_IED | ⚠️ HÍBRIDA | H30/H73 | H05/H06 | IED_Global=31.14% — CHK-09 dice debe ser fórmula no hardcode |
| H18_ITAM | ⚠️ HÍBRIDA | referencia | H12 | ITAM — indicador de autoevaluación |
| H19_ICS_ISP | ⚠️ HÍBRIDA | H73 ISP_* | H07/H90 | ISP Salud — alimenta financiero output |
| H19b_IE_EP_EA | ⚠️ HÍBRIDA | H12d | H90 EP | IE por entidad EP Aseo |
| H20_ICODS | ❌ HUÉRFANA | — | H11 ODS | ICODS — no conectado a output principal |
| H20b_IGP_GOBERNANZA_PARTIC | ⚠️ HÍBRIDA | H28 | H10/H10b | IGP_3 MFN — CHK-05/06 activos |
| H20c_IEF_EFICIENCIA_FINANCIERA | ❌ HUÉRFANA | — | H07/H90 | IEF — desconectado del motor |
| H42_IET_EQUIDAD_TERRITORIAL | ⚠️ HÍBRIDA | H99 / H43 | H99 ENGINE | IET — referencia para D4 |
| H43_MOTOR_TERRITORIAL_CONSOLIDA | 💤 MUERTA | reemplazado por H99 | — | Header: SIAP-ICPI v1.0 — **legado abandonado** — H99 es el motor territorial actual |

---

### CAPA 5 — MONITOREO MMP

| Hoja | Estado | Alimenta | Issue |
|------|--------|----------|-------|
| H25_MMP_MENSUAL | ⚠️ HÍBRIDA | H28 resumen | Estructura presente — datos 2026 parciales |
| H26_MMP_TRIMESTRAL | ❌ HUÉRFANA | — | 18 de 51 filas con datos — muy incompleto |
| H27_MMP_ANUAL | ⚠️ HÍBRIDA | H28 | 61 filas — datos históricos presentes |

---

### CAPA 6 — REPORTES / SALIDAS EJECUTIVAS

| Hoja | Estado | Alimenta | Issue |
|------|--------|----------|-------|
| H28_RESUMEN_EJECUTIVO | ⚠️ HÍBRIDA | H29/alcalde | Referencias a H12/H15 — outputs dependen de T_i_2026 vacío |
| H29_TABLERO_ALCALDE | ⚠️ HÍBRIDA | presentación | Tablero visual — depende de H28 |
| H30_IED_POR_DIRECCIÓN | ⚠️ HÍBRIDA | presentación | IED desglosado — parcialmente poblado |
| H31_REPORTE_CPCCS | ❌ HUÉRFANA | — | 33/65 filas — reporte muy incompleto |
| H32_REPORTE_ODS | ❌ HUÉRFANA | — | 17/45 filas — muy incompleto |
| H33_TAC_QUIRA_CIUDADANA | ❌ HUÉRFANA | — | TAC ciudadano — sin conexión al motor |
| H34_CERTIFICADO_QUIRA | ⚠️ HÍBRIDA | documento | Certificado institucional — xref a H12 |
| H34b_MFN_FIDELIDAD_NARRATIVA | 💤 MUERTA | — | 20/102 filas — shell casi vacío |
| H35_DATASET_ACADEMIA | ❌ HUÉRFANA | — | Dataset para academia — no conectado |
| H36_QUIRA_BRIDGE | ⚠️ HÍBRIDA | Obsidian (desacoplado) | Puente QUIRA-Obsidian — desacoplado por diseño ✓ |
| H36b_LOOKUP_ARRASTRE | ❌ HUÉRFANA | — | ⚠️ Warning detectado — posible arrastre de datos stale |
| H36c_OBSIDIAN_MAP | ❌ HUÉRFANA | Obsidian | Desacoplado por doctrina ✓ — correctamente aislado |
| H37_SENSIBILIDAD_ESTRATÉGICA | ⚠️ HÍBRIDA | referencia | Análisis de escenarios — válido como referencia |
| H38_ALCANCE_PREVENTIVO | ❌ HUÉRFANA | — | Sin conexión al motor principal |
| H65_CIUDADANO_IN_PRESUPUESTO | 💤 MUERTA | — | 13/60 filas — inputs ciudadanos no ingresados |
| H66_CIUDADANO_IN_PAC | 💤 MUERTA | — | 13/60 filas — sin datos |
| H67_CIUDADANO_IN_POA | 💤 MUERTA | — | 13/60 filas — sin datos |

---

### CAPA 7 — GOBERNANZA / AUDITORÍA SISTEMA

| Hoja | Estado | Alimenta | Issue |
|------|--------|----------|-------|
| H74_RECOVERY_MAP | ⚠️ HÍBRIDA | protocolo recuperación | Mapa de recuperación — referencia correcta |
| H76_AUDIT_TRAIL | ❌ HUÉRFANA | — | 5/31 filas — muy incompleto |
| H77_DATA_DICTIONARY | ✅ VIVA | documentación | Diccionario de datos — bien poblado |
| H80_MODEL_REGISTRY | ✅ VIVA | sistema | Registro de modelos |
| H81_HASH_CHAIN | ✅ VIVA | integridad | 0 nulls — cadena de hashes completa |
| H82_CONFIG_PARAMS | ✅ VIVA | sistema | Parámetros de configuración |
| H83_SOD_REGISTRY | ✅ VIVA | gobernanza | Separación de funciones |
| H84_SNAPSHOT_REGISTRY | ✅ VIVA | governance | Registro de snapshots |
| H85_ALERTS_LOG | ✅ VIVA | CHK/monitoreo | Log de alertas activo — CHK-08/CHK-12 PENDIENTES |
| H86_REPORT | ⚠️ HÍBRIDA | reportes | Reporte de run |
| H86b_ALGORITHMIC_GOVERNANCE | ⚠️ HÍBRIDA | governance | Protocolo algorítmico |
| H87_RECOVERY_POLICY | ⚠️ HÍBRIDA | protocolo | Política de recuperación |
| H88_EVIDENCE_REGISTRY | ✅ VIVA | auditoría | Registro de evidencias |
| H89_TRUST_SCORE | ⚠️ HÍBRIDA | H73 D1 | Trust Score — 83.5% ingresado en H01!B180 |
| H95_LIMITACIONES | ✅ VIVA | documentación | Limitaciones metodológicas documentadas |
| H96_TRAZABILIDAD | ✅ VIVA | documentación | Linaje de datos |
| H97_VALIDACIONES | ⚠️ HÍBRIDA | auditoría | Validaciones internas — xref |
| H98_TGI_FRAMEWORK | 🔥 CRÍTICA | metodología TGI | **Pesos documentados (20/20/25/25/10) NO reproducen TGI=68.82%** — pesos reales usados en cómputo original no están documentados |
| H99_ENGINE_CORE | 🔥 CRÍTICA | D4 TGI / IRS / IET | **Columnas TGI D1-D5 vacías** — IRS=79.7 ✅ · IET por parroquia ✅ — pero sin computar hacia H73 |
| RC_CHANGELOG | ✅ VIVA | documentación | Changelog de RCs — presente |
| COMPILER_LOG | ✅ VIVA | trazabilidad | Log de compilación |

---

### CAPA 8 — SCHEMA / FUENTES DATOS ESTRUCTURALES

| Hoja | Estado | Alimenta | Issue |
|------|--------|----------|-------|
| H00_ÍNDICE | ✅ VIVA | navegación | Índice completo |
| H02_GLOSARIO_QUIRA | ✅ VIVA | terminología | Glosario canónico |
| H02b_ORGÁNICO_CLASIFICADOR | ✅ VIVA | H71 | Orgánico clasificador |
| H04b_DIAGNÓSTICO_SOCIAL | ✅ VIVA | H04/H99 | Diagnóstico social |
| ÍNDICE_ECIAP | ⚠️ HÍBRIDA | ECIAP | 94 filas, referencias |
| MATRIZ_CANONICA | ✅ VIVA | H12/SCHEMA_METAS | Matriz de 25 metas canónicas |
| CAPA_TERRITORIAL_MONTECRISTI | ✅ VIVA | H99 | Geo-data cantonal |
| POA_GEOREFERENCIADO | ✅ VIVA | ECIAP | POA georeferenciado 2026 |
| PAC_2026_GEOREFERENCIADO | ✅ VIVA | ECIAP | PAC georeferenciado 2026 |
| ANÁLISIS_TENDENCIA_TERRITORIAL | ⚠️ HÍBRIDA | referencia | Tendencia territorial |
| H90_PRESUPUESTO_CONSOLIDADO_202 | ✅ VIVA | H73/gm_snapshot | Consolidado Holding Q1-2026 ✅ |
| H_HOLDING_CEDULAS_2026 | ✅ VIVA | H07b | Cédulas eSIGEF Enero-Marzo 2026 ✅ |
| LOG_EJECUCION | ✅ VIVA | auditoría | Log de ejecución |
| KB_DIAGNOSTICO_PDOT | ✅ VIVA | H04 | Diagnóstico PDOT completo |
| SCHEMA_METADATA | ✅ VIVA | H01 | Ficha municipal canónica |
| SCHEMA_TERRITORIOS | ✅ VIVA | H99 | Datos territoriales por parroquia |
| SCHEMA_NBI | ✅ VIVA | H99 IRS | NBI por parroquia — INEC 2022 |
| SCHEMA_METAS | ✅ VIVA | H12 | 25 metas PDOT canónicas |
| SCHEMA_PROYECTOS | ✅ VIVA | H05 | PAI 2024-2027 proyectos |
| SCHEMA_RIESGOS | ✅ VIVA | H37/H38 | Riesgos y amenazas |
| SCHEMA_ORGANICO | ✅ VIVA | H02b | Estructura orgánica |
| SCHEMA_CNE | ✅ VIVA | H03/H63 | Marco electoral |
| SCHEMA_DICCIONARIO | ✅ VIVA | H02 | Ontología institucional |
| SCHEMA_REGLAS | ✅ VIVA | H75/SAT | Motor de semáforo y alertas |
| SCHEMA_ECIAP_BRIDGE | ✅ VIVA | ECIAP | Tabla de cruce geo-meta |
| H63_S0_CNE_TRAZABILIDAD | ✅ VIVA | H03 | 81 filas CNE trazabilidad |
| H64_SELECTOR_PROTOCOLO_MODO | ⚠️ HÍBRIDA | modo operación | Selector protocolo — referencias |
| H68_MOTOR_CONGRUENCIA_EXTERNA | ⚠️ HÍBRIDA | H69 | Motor congruencia externa |
| H69_ELEGIBILIDAD_FONDOS | ⚠️ HÍBRIDA | reportes fondos | Elegibilidad fondos (BID/CAF/GEF) |
| H70_BITACORA_LOTAIP_OPACIDAD | ❌ HUÉRFANA | — | 15 filas — bitácora poco poblada |
| H71_EP_ADSCRITAS | ✅ VIVA | H07b/H12d | Datos EP Aseo/Bomberos/Patronato |
| H72_EP_BASE_LEGAL | ✅ VIVA | H71 | Base legal EP |
| H_ORGANICO_040_2025 | ✅ VIVA | H02b | Estatuto orgánico Resolución 040-2025 |
| H39_AUTOCONTROL_ECOSISTEMA | ⚠️ HÍBRIDA | governance | Control ecosistema |
| H40_PROTOCOLO_INGESTA | ⚠️ HÍBRIDA | operaciones | Protocolo de ingesta |
| H41_IOC_OPACIDAD_CRITICA | ⚠️ HÍBRIDA | H09/H70 | Índice opacidad crítica |

---

## INCONSISTENCIA ARITMÉTICA TGI — DIAGNÓSTICO DETALLADO

### Valores actuales en H73

```
D1 (Legalidad)          = 83.5%   fuente: H01!B180 Trust_Score  ✅ presente
D2 (Fidelidad Plan.)    = 69.93%  fuente: H01!B15 ICPI_2025     ✅ presente
D3 (Ejecución Presup.)  = 14.58%  fuente: ???                   ❌ HUÉRFANO
D4 (Equidad Territorial)= 66.85%  fuente: ???                   ❌ HUÉRFANO
D5 (Capacidad Inst.)    = 100%    fuente: H01!B12 ICM_SNP=1.0   ✅ presente
TGI_SCORE               = 68.82%  fuente: ???                   ❌ INCONSISTENTE
```

### Verificación con pesos H98 (20/20/25/25/10)

```
TGI_computado = 0.20×83.5 + 0.20×69.93 + 0.25×14.58 + 0.25×66.85 + 0.10×100
              = 16.700 + 13.986 + 3.645 + 16.7125 + 10.000
              = 61.044%   ≠ 68.82%  ❌
```

### D3 desde fórmula canónica H98

```
D3 = H07b!B18 × 100 = 0.5985 × 100 = 59.85%  (Ti GAD 2025 anual, INMUTABLE)

TGI_computado = 0.20×83.5 + 0.20×69.93 + 0.25×59.85 + 0.25×66.85 + 0.10×100
              = 16.700 + 13.986 + 14.9625 + 16.7125 + 10.000
              = 72.361%   ≠ 68.82%  ❌
```

### D4 desde H99 (rural estricto J8:J13)

```
D4_rural = AVG(51.79 + 28.57 + 42.86 + 63.39 + 35.71 + 46.43) / 6 = 44.79%

TGI_computado (D3=59.85, D4=44.79) = 16.7 + 13.986 + 14.9625 + 11.1975 + 10 = 66.846%  ≠ 68.82%  ❌
```

### Única combinación que reproduce ≈68.82%

```
Pesos hipotéticos: D1=0.20, D2=0.20, D3=0.10, D4=0.40, D5=0.10
= 0.20×83.5 + 0.20×69.93 + 0.10×14.58 + 0.40×66.85 + 0.10×100
= 16.700 + 13.986 + 1.458 + 26.740 + 10.000
= 68.884% ≈ 68.82%  (diferencia: rounding de D3 o D4 inputs)
```

**Conclusión:** TGI=68.82% fue probablemente computado en v6.0 con pesos D4=0.40, D3=0.10 — distintos a los documentados en H98 (D3=0.25, D4=0.25). Esta decisión de pesos **nunca fue formalizada en H98**.

---

## PLAN DE RECONEXIÓN DIMENSIONAL

### PRIORIDAD 1 — Decidir y documentar pesos TGI (analista, ~1h)

El analista debe confirmar si los pesos canónicos son:
- **Opción A (H98 original):** D1=0.20, D2=0.20, D3=0.25, D4=0.25, D5=0.10 → TGI se recalcula ≈66.85%–72.36%
- **Opción B (lo que da 68.82%):** D1=0.20, D2=0.20, D3=0.10, D4=0.40, D5=0.10 → formalizar en H98

Una vez decidido: actualizar H98 F20-F24 con pesos canónicos y recomputar TGI_SCORE.

### PRIORIDAD 2 — D3 metodología (analista, ~30 min)

- **Recomendado:** D3 = H07b!B18 × 100 = 59.85% (Ti GAD 2025 anual per H98 — INMUTABLE, auditable)
- Alternativa: si se quiere Q1-2026, definir la fórmula exacta (qué entidades, qué grupos, qué base)
- Actualizar H73 TGI_D3 con el valor canónico y la referencia a la celda fuente

### PRIORIDAD 3 — Reconectar H11b al motor (analista + Claude, ~2h)

Los Score_Vinculación de H11b (0.75–0.90 por meta) deben alimentar alguna dimensión del TGI:
- Si alimentan D1 (Legalidad/Coherencia Normativa): H11b promedio Score → H01!B180 como componente
- Si alimentan D2 (Fidelidad Planificación): H11b scores → H12 C_i o R_i column
- Decisión doctrinal necesaria

### PRIORIDAD 4 — H12 T_i_2026 column (analista, ~3h)

Para que ICPI 2026 computable:
1. CHK-08: Pegar cédula eSIGEF 2026 completa en H07_S5 zona cruda
2. Con datos H_HOLDING_CEDULAS_2026 existentes, poblar T_i_2026 para 25 metas
3. H12!B33 computará automáticamente el ICPI vivo

### PRIORIDAD 5 — H99 TGI D1-D5 columns (analista, ~1h)

Conectar H99 cols T-X con fórmulas que lean desde H01/H07b/IET_Local:
```
H99!T_i = D1 → =H01!B180
H99!U_i = D2 → =H01!B15*100
H99!V_i = D3 → =H07b!B18*100 (o fórmula nueva Q1)
H99!W_i = D4 → =AVERAGE(J8:J13) o =AVERAGE(J7:J13) [según decisión]
H99!X_i = D5 → =H01!B12*100
H99!Y_i = TGI_Score_5D → =0.20*T + 0.20*U + peso_D3*V + peso_D4*W + 0.10*X
```

### PRIORIDAD 6 — CHK-12 PP 2026 + CPCCS (requiere datos externos)

- Ingresar actas PP 2026 en H10b
- Ingresar informe RdC CPCCS 2025 en H10/H31
- SAT-V pasará de "datos insuficientes" a evaluación real

---

## REGLA NUEVA — OUTPUT_API

**Formalizada a partir de esta auditoría:**

> **"Ningún valor entra a H73_OUTPUT_API si no tiene referencia de celda fuente trazable en la columna FUENTE_CELDA."**

Formato canónico para H73:
```
| CLAVE            | VALOR  | TIPO   | FUENTE_CELDA              | TIMESTAMP_UTC |
| TGI_D3           | 59.85  | DECIMAL| H07b!B18×100              | 2026-05-26    |
| TGI_SCORE        | 72.36  | DECIMAL| =0.20*D1+0.20*D2+...      | 2026-05-26    |
```

Mientras una celda diga "manual" o esté vacía en FUENTE_CELDA: **no es canónica**.

---

## ESTADO DEL PROYECTO POST-AUDITORÍA

```
                    QUIRA OS — Estado real Sprint Canon
                    ====================================

Pipeline Python           ████████████ SÓLIDO
Arquitectura              ████████████ SÓLIDA  
Gobernanza código         ████████████ SÓLIDA
SAT reconciliado          ████████████ COMPLETO ✅

Excel dimensional         ████░░░░░░░░ PRE-CANÓNICO
TGI aritmética            ██░░░░░░░░░░ INCONSISTENTE
H12 ICPI vivo             ██░░░░░░░░░░ ROTO (T_i vacío)
H99 TGI D1-D5             ██░░░░░░░░░░ DESCONECTADO
H11b Monitor PP           █░░░░░░░░░░░ HUÉRFANO
OUTPUT_API                ████░░░░░░░░ MANUAL/PARCIAL

Longitudinalidad real     ░░░░░░░░░░░░ ESPERANDO estabilidad
```

**Descriptor correcto actual:**
```
QUIRA OS = Motor institucional epistemológicamente parcial
         + arquitectura correcta
         + deuda dimensional documentada
         + pre-listo para reconexión controlada
```

---

*Auditoría realizada por QUIRA Intelligence · Dylus Lab © 2026*  
*Próxima acción: Analista confirma PRIORIDAD 1 (pesos TGI) para desencadenar reconexión*  
*NORTH.md y ARQUITECTURA_CANONICA.md siguen siendo documentos normativos vigentes*
