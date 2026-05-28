# D.2 — Mapeo Ontológico Institucional
## QUIRA OS — ADN del Grafo Futuro

> **Propósito:** Documento de planificación D-Sprint. Alimenta navegación, IA (Sentinel), Graphify, Obsidian links y causalidad institucional.
> **Estado:** D.2 COMPLETADO — 2026-05-28
> **Doctrina:** "El Excel es el Estado." Toda data canónica proviene de `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx`.

---

## ESTRUCTURA DEL MAPEO

Cada entrada sigue el esquema canónico:
`módulo → dominio → hojas Excel → índices → entidades → territorialidad → relaciones → acción`

---

## LOS 13 MACRO-DOMINIOS (D.1 validado + D.2 ajuste: Género y Ambiente separados)

> **Ajuste D.2:** Dom 9 se divide en dos dominios distintos — Género/Equidad Social y Ambiente/Sostenibilidad. Total: 13 dominios. La separación es correcta: tienen indicadores, entidades, fondos y acciones completamente distintos.

| # | Dominio | Capa | Módulos que lo alimentan |
|---|---------|------|--------------------------|
| 1 | **Salud Institucional** | Política | p_vista_ejecutiva, p6_pulso, p7_brecha, p1_dashboard |
| 2 | **Fidelidad Política** | Política | p3_congruencias, p8_metas, p16_gobernanza (ctrl social) |
| 3 | **Planificación y Ejecución** | Política | p8_metas, p12_cadena, p_cadena_institucional, p5_operacion |
| 4 | **Holding Municipal** | Ejecutiva | p2_holding, p5_operacion (ingesta), m3_municipal |
| 5 | **Análisis de Eficiencia** | Ejecutiva | p14_eficiencia, p7_brecha, p1_dashboard, p13_simulador |
| 6 | **Equidad Territorial** | Ejecutiva | p4_geotwin, p10_inversion, p13_simulador (IRS) |
| 7 | **Transparencia y Gobierno Abierto** | Rendición | p15_transparencia, p_cadena_institucional (LOTAIP tab) |
| 8 | **Participación Ciudadana** | Rendición | p16_gobernanza, p17_rdc, p_cadena_institucional (PP+RDC) |
| 9 | **Género y Equidad Social** | Rendición | p19_genero (Tab Género) |
| 10 | **Ambiente y Sostenibilidad** | Rendición | p19_genero (Tab Ambiente) — nuevo módulo p20_ambiente en D.4 |
| 11 | **Cooperación Internacional** | Territorial | p18_cooperacion, p11_ods |
| 12 | **Agenda 2030** | Territorial | p11_ods |
| 13 | **Observabilidad Longitudinal** | Territorial | m2_alertas, p9_sat, p_alertas, p_historico, p_seguimiento |

---

## MAPEO COMPLETO POR MÓDULO

---

### 01 · p_vista_ejecutiva.py
**Nombre UI:** Vista Ejecutiva (Bloomberg-style)
**Rol:** Vista principal Ejecutivo/Alcaldía. 6 zonas de scorecard.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 1 — Salud Institucional |
| **Hojas Excel** | H73_OUTPUT_API · H07_S5_FINANCIERO_eSIGEF · H90_PRESUPUESTO_CONSOLIDADO |
| **Índices** | ICPI global · D1-D5 (TGI 5D) · TOP predictor · AVEP escala · ISP · IED · ITAM |
| **Entidades** | GAD Central · Holding (4 adscritas) |
| **Territorialidad** | Cantón Montecristi — vista consolidada |
| **Relaciones** | → m1_situacion (Situación) · → m2_alertas (Alertas) · → p2_holding (Holding) · → p4_geotwin (Territorio) · → Sentinel IA |
| **Acción** | Diagnóstico ejecutivo en 1 pantalla → decisión política o derivar al Técnico |

---

### 02 · p_concejo.py (Panel Estratégico)
**Nombre UI:** Panel Estratégico (Concejo Municipal)
**Rol:** Vista del Concejo. Contexto institucional reducido.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 1 — Salud Institucional |
| **Hojas Excel** | H73_OUTPUT_API · H82_CONFIG_PARAMS |
| **Índices** | ICPI · scores concejo · resumen ejecutivo |
| **Entidades** | GAD Central · Concejo Municipal |
| **Territorialidad** | Cantón |
| **Relaciones** | → p_vista_ejecutiva · → m1_situacion |
| **Acción** | Contexto para sesiones de Concejo y deliberación política |

---

### 03 · m1_situacion.py → p6_pulso.py + p7_brecha.py
**Nombre UI:** Situación Institucional (container)
**Rol:** Pulso ejecutivo + 6 vectores de brecha causal.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 1 — Salud Institucional |
| **Hojas Excel** | H73_OUTPUT_API · H07_S5_FINANCIERO_eSIGEF |
| **Índices** | ISP=14.58% · IED=33.99% · IGP=48.33% · IOC=17.71% · IET=92.73%* · PSG=12.83% · ICGI-T timeline 2023-Q1 2026 |
| **Entidades** | GAD Central |
| **Territorialidad** | Cantón + desglose por direcciones |
| **Relaciones** | → p9_sat · → p14_eficiencia · → p13_simulador |
| **Acción** | Identificar vectores causales de baja calificación → priorizar intervenciones |

> *IET pendiente recalibración: solo 1 parroquia rural (La Pila), no 6.

---

### 04 · m2_alertas.py → p9_sat.py + Longitudinal Engine
**Nombre UI:** Alertas (container)
**Rol:** Señales activas + evolución temporal (Tabla RC-M).

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 12 — Observabilidad Longitudinal |
| **Hojas Excel** | H73_OUTPUT_API · Supabase (snapshots) |
| **Índices** | ICPI por período · D3 ejecución · RC-M tabla · tendencia ICPI · ISP/ITAM/PSG alertas |
| **Entidades** | GAD Central · Holding |
| **Territorialidad** | Cantón |
| **Relaciones** | → longitudinal_engine.py · → p_alertas · → p_historico |
| **Acción** | Activar alerta si Ti < 60% por ≥3 períodos (SAT-III REINCIDENTE doctrina RC-M) |

---

### 05 · m3_municipal.py → p2_holding + p16_gobernanza + p15_transparencia + p10_inversion
**Nombre UI:** Municipal (container)
**Rol:** Holding + participación ciudadana + transparencia + inversión territorial.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 4 (Holding) + Dom 7 (Transparencia) + Dom 8 (Participación) + Dom 6 (Territorial) |
| **Hojas Excel** | H71_EP_ADSCRITAS · H90_PRESUPUESTO_CONSOLIDADO · H10c_RDC_APORTES · H99_ENGINE_CORE |
| **Índices** | HPT-M scores · ITAM · IOC · PP fichas · IFE · RDC ciclo |
| **Entidades** | GAD + EP Aseo + Bomberos + Patronato + Ciudadanía |
| **Territorialidad** | Cantón + 7 parroquias |
| **Relaciones** | → 4 módulos atómicos internos |
| **Acción** | Hub para toma de decisiones del holding y rendición a la ciudadanía |

---

### 06 · p2_holding.py (HPT-M)
**Nombre UI:** Holding Municipal
**Rol:** Scorecard de las 4 entidades adscritas + GAD.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 4 — Holding Municipal |
| **Hojas Excel** | H71_EP_ADSCRITAS · H90_PRESUPUESTO_CONSOLIDADO |
| **Índices** | Bomberos 82.7% ✅ · Patronato 74.1% ✅ · GAD 61.2% ⚠ · EP Aseo 58.4% ⚠ |
| **Entidades** | Cuerpo de Bomberos · Patronato Municipal · EP Aseo (EMAI) · GAD Central |
| **Territorialidad** | Cantón |
| **Relaciones** | → p14_eficiencia (eficiencia GAD) · → p5_operacion (ingesta) · → p_alertas (alertas entidades) |
| **Acción** | Identificar entidad que arrastra el holding → intervención directiva |

---

### 07 · p3_congruencias.py
**Nombre UI:** Fidelidad Política (antes "Congruencias")
**Rol:** 4 congruencias del grupo municipal + IFE electoral.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 2 — Fidelidad Política |
| **Hojas Excel** | H16 · H24 · H63_S0_CNE |
| **Índices** | IFE-A=72.73% (48/66 promesas CNE) · Congruencia Política 58.4% · Operativa 47.2% · Territorial 44.8% · Ecosistémica 61.1% |
| **Entidades** | Alcaldía (Ing. Jonathan Toro) · Concejo · CNE · 4 Nodos HPT-M |
| **Territorialidad** | Cantón + 7 parroquias (congruencia territorial) |
| **Relaciones** | → p8_metas (metas PDOT) · → p4_geotwin (territorio) · → p2_holding (ecosistémica) · → Sentinel IA |
| **Acción** | ¿Estamos gobernando lo que prometimos? → Alinear POA con compromisos CNE faltantes |

---

### 08 · p4_geotwin.py
**Nombre UI:** Equidad Territorial / GeoTwin
**Rol:** Mapa Folium de 7 parroquias + Gov Twin proyectos colaborativos.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 6 — Equidad Territorial |
| **Hojas Excel** | H24 · H99_ENGINE_CORE |
| **Índices** | TPS por parroquia · agua % · $/hab · IRS=79.7 (Muy Regresivo) · Composite_Need |
| **Entidades** | 7 parroquias · GAD · PNUD · GEF · Comunidades |
| **Territorialidad** | 7 parroquias: Montecristi (cabecera) · La Pila (única rural) · Colorado · Isabel Muentes · Gral. Alfaro · Leónidas Proaño · Aníbal San Andrés |
| **Relaciones** | → p10_inversion ($/hab) · → p13_simulador (IRS sensibilidad) · → p18_cooperacion (Gov Twin fondos) · → p3_congruencias (congruencia territorial) |
| **Acción** | Priorizar inversión territorial según TPS+NBI → desbloquear PNUD $2.4M + GEF $180K |

---

### 09 · p5_operacion.py (P-17 Ingesta + P-18 Validador + P-19 HITL)
**Nombre UI:** Operación Técnica · Backoffice
**Rol:** Protocolo mensual de ingesta con validación humana HITL.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 4 (operativo interno) + Dom 12 (observabilidad) |
| **Hojas Excel** | H05 POA · H05b PAC · H07 eSIGEF · Informes PDF firmados |
| **Índices** | Brechas C1/C2/C3/C4 · SHA-256 trazabilidad · estado ingesta por unidad |
| **Entidades** | 7 unidades: DAPS · DOP · FIN · RRHH · Bomberos · EMAI-EP · Patronato |
| **Territorialidad** | Cantón (todas las direcciones) |
| **Relaciones** | → p12_cadena (SAT-0 detección) · → p_alertas (alertas activas) · → motor ICPI (recálculo) |
| **Acción** | Cargar mes → validar → HITL aprueba → motor recalcula → QUIRA se actualiza |

---

### 10 · p6_pulso.py
**Nombre UI:** Pulso Ejecutivo
**Rol:** Vista de indicadores de pulso en tiempo cuasi-real.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 1 — Salud Institucional |
| **Hojas Excel** | H73_OUTPUT_API |
| **Índices** | ISP · IED · ITAM · IOC · IGP · IET · PSG (6 vectores + contexto) |
| **Entidades** | GAD Central |
| **Territorialidad** | Cantón |
| **Relaciones** | → p7_brecha · → p_vista_ejecutiva |
| **Acción** | Alarma rápida de desviación → escalar a decisión ejecutiva |

---

### 11 · p7_brecha.py
**Nombre UI:** Brecha Institucional (6 vectores causales)
**Rol:** Análisis causal de la brecha entre ICGI-T actual y meta.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 1 — Salud Institucional + Dom 5 — Análisis de Eficiencia |
| **Hojas Excel** | H73_OUTPUT_API |
| **Índices** | ISP -8.2pts · IED -6.8pts · IGP -4.1pts · IOC -3.1pts · IET -2.8pts · PSG -2.4pts · ICGI-T 2023=57.36% → 2025=69.93% → Q1-2026=53.56% |
| **Entidades** | GAD Central |
| **Territorialidad** | Cantón |
| **Relaciones** | → p13_simulador (simular mejora vectores) · → p14_eficiencia (IED) · → p10_inversion (IET) · → p19_genero (PSG) |
| **Acción** | Identificar vector de mayor impacto para intervención focalizada |

---

### 12 · p8_metas.py
**Nombre UI:** Metas del Plan (10 Metas PDOT 2023-2027)
**Rol:** Trazabilidad promesa → meta → POA → ejecución.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 3 — Planificación y Ejecución |
| **Hojas Excel** | H31_REPORTE_CPCCS · H73_OUTPUT_API · H99_ENGINE_CORE |
| **Índices** | M-01 Agua 34.9% · M-02 Alcantarillado 43.5% · M-03 Vialidad 53% · M-06 PSG 12.83% · M-07 Inversión $40/hab · M-10 IFE-A 72.73% · 4 sin PAC |
| **Entidades** | GAD · DAPS · DOP · DAF · Patronato |
| **Territorialidad** | Cantón + Isabel Muentes (M-01/M-07 crítico) |
| **Relaciones** | → p12_cadena (PAC sin contrato) · → p3_congruencias (IFE) · → p7_brecha (impacto en ICGI-T) · → p_cadena_institucional (Tab PDOT) |
| **Acción** | Regularizar 4 metas sin PAC → ICPI D3 mejora → Contraloría riesgo eliminado |

---

### 13 · p9_sat.py
**Nombre UI:** Señales Activas (Alertas SAT)
**Rol:** Panel de alertas por categoría de riesgo.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 12 — Observabilidad Longitudinal |
| **Hojas Excel** | H73_OUTPUT_API · H07_S5_FINANCIERO_eSIGEF |
| **Índices** | Riesgo Fiscal CRÍTICO (ISP 14.58% < COOTAD 65%) · Contractual CRÍTICO (24 proc sin SHA-256) · Transparencia ALERTA · Participativo ALERTA |
| **Entidades** | GAD · DAF · Contraloría · DPE |
| **Territorialidad** | Cantón |
| **Relaciones** | → m2_alertas (container) · → p12_cadena (SAT-0) · → p_alertas (alert_engine) |
| **Acción** | Escalar alertas críticas a Alcaldía → Contraloría notificación preventiva |

---

### 14 · p10_inversion.py
**Nombre UI:** Inversión por Habitante
**Rol:** Inequidad territorial documentada: $/habitante por parroquia.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 6 — Equidad Territorial |
| **Hojas Excel** | H99_ENGINE_CORE |
| **Índices** | Isabel Muentes $40/hab (EMERGENCIA) · Colorado $94 · La Pila $93 · Montecristi $217 · Brecha 5.4× · Meta rural $80/hab |
| **Entidades** | GAD · 7 parroquias |
| **Territorialidad** | 7 parroquias (La Pila = única rural) |
| **Relaciones** | → p4_geotwin (mapa) · → p13_simulador (IRS) · → p18_cooperacion (PNUD eligibility) · → p7_brecha (IET vector) |
| **Acción** | Redistribuir inversión → Isabel Muentes de $40 → $80/hab → elegibilidad PNUD $2.4M |

---

### 15 · p11_ods.py
**Nombre UI:** Agenda 2030 / ODS
**Rol:** ICODS + 14 ODS vinculados + fondos de elegibilidad.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 11 — Agenda 2030 |
| **Hojas Excel** | H73_OUTPUT_API |
| **Índices** | ICODS=87.5% · ODS 5 CRÍTICO (PSG 12.83%) · ODS 6 CRÍTICO (agua 34.9%) · 4 scores derivados H73 |
| **Entidades** | GAD · ONU Mujeres · GEF · PNUD · BID Lab |
| **Territorialidad** | Cantón + Isabel Muentes (ODS 6) |
| **Relaciones** | → p18_cooperacion (fondos por ODS) · → p19_genero (ODS 5) · → p10_inversion (ODS 10) |
| **Acción** | Mejorar ODS 5+6 → desbloquear $160K fondos ONU + reducir riesgo RDC |

---

### 16 · p12_cadena.py
**Nombre UI:** Cadena POA-PAC (interno técnico)
**Rol:** SAT-0: 4 metas PDOT sin contrato PAC + 24 procesos sin SHA-256.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 3 — Planificación y Ejecución |
| **Hojas Excel** | H05b PAC · H07_S5_FINANCIERO_eSIGEF · SERCOP OCDS |
| **Índices** | 4 metas sin PAC (POA-06-12 $380K agua · POA-03-07 $210K vialidad · POA-09-04 $95K luminarias · POA-11-02 $145K La Pila) · 24 procesos sin SHA-256 en 5 direcciones |
| **Entidades** | DOBS · DAPS · DAF · DPM · Otras · SERCOP |
| **Territorialidad** | Cantón + Isabel Muentes + La Pila |
| **Relaciones** | → p8_metas (metas afectadas) · → p5_operacion (validador cruzado) · → p_alertas (SAT-0) · → p_cadena_institucional (Tab POA-PAC) |
| **Acción** | Regularizar 4 contratos PAC → SHA-256 → eliminar SAT-0 → ICPI D4 mejora |

---

### 17 · p13_simulador.py
**Nombre UI:** Simulador / Laboratorio de Escenarios
**Rol:** Simulación ICGI-T (6 sliders) + sensibilidad IRS.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 5 — Análisis de Eficiencia + Dom 6 — Equidad Territorial |
| **Hojas Excel** | H73_OUTPUT_API · H99_ENGINE_CORE |
| **Índices** | ISP/IED/IGP/IOC/IET/PSG sliders · BASE=53.56% · META=70% · IRS=79.7 (★ oficial) · 6 escenarios IRS |
| **Entidades** | GAD Central (todos los ejes) |
| **Territorialidad** | Cantón (global) + parroquias (IRS) |
| **Relaciones** | → p7_brecha (vectores a mejorar) · → p19_genero (PSG) · → p10_inversion (IRS/IET) |
| **Acción** | Simular combinación óptima de mejoras → hoja de ruta de 3-6 meses |

---

### 18 · p14_eficiencia.py
**Nombre UI:** Eficiencia Institucional (IED)
**Rol:** IED=33.99% + ranking de 12 direcciones.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 5 — Análisis de Eficiencia |
| **Hojas Excel** | H73_OUTPUT_API |
| **Índices** | IED=33.99% · DJUR=68.4% (top) · DTUR=22.4% · DTIC=18.3% (peor) · 4 direcciones con alertas (DAF, DPM, DAPS, DOBS) |
| **Entidades** | 12 Direcciones GAD: DJUR · DSOC · DAF · DPM · DAPS · DOBS · DTUR · DTIC · y otras |
| **Territorialidad** | Cantón (Sede GAD) |
| **Relaciones** | → p7_brecha (IED vector) · → p12_cadena (DAF/DPM/DAPS/DOBS alerta) · → p_alertas (alertas por dir.) |
| **Acción** | Intervenir DTIC y DTUR primero → IED sube → ICPI D2 mejora |

---

### 19 · p15_transparencia.py
**Nombre UI:** Transparencia y Gobierno Abierto
**Rol:** ITAM=56% + 21 artículos LOTAIP.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 7 — Transparencia y Gobierno Abierto |
| **Hojas Excel** | H73_OUTPUT_API · DPE API |
| **Índices** | ITAM=56% · IOC=17.71% · 12 OK / 5 PARCIAL / 4 NO (Art. 7h, 7n, 7p, 7r) |
| **Entidades** | GAD · DPE · Ciudadanía |
| **Territorialidad** | Cantón (portal web) |
| **Relaciones** | → p17_rdc (CPCCS IOC) · → p_cadena_institucional (Tab LOTAIP) · → m3_municipal |
| **Acción** | Publicar 4 artículos faltantes → ITAM +19% → cumplimiento DPE → CPCCS nota mejora |

---

### 20 · p16_gobernanza.py (Tab 1: PP + Tab 2: Control Social/RDC)
**Nombre UI:** Gobernanza Participativa
**Rol:** PP 2026 + Control Social IFE.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 8 — Participación Ciudadana |
| **Hojas Excel** | H10_S8_PARTICIPACIÓN_CPCCS · H10c_RDC_APORTES · H63_S0_CNE |
| **Índices** | PP 2026: 149 fichas (ACTA N°007-2025) · IGP=48.33% Q1-2026 · IFE-A=72.73% (48/66) · IFE-E: 4 metas sin PAC · ICM vs ICPI brecha histórica · 95 aportes RDC 2023-2024 |
| **Entidades** | Ciudadanía · CPCCS · Concejo · Alcaldía |
| **Territorialidad** | 7 parroquias (PP por parroquia) |
| **Relaciones** | → p17_rdc (RDC preparación) · → p8_metas (promesas CNE) · → p_cadena_institucional (Tabs PP+RDC) |
| **Acción** | IFE: formalizar 18 promesas sin PDOT · PP: vincular fichas a POA · RDC: preparar junio 2026 |

---

### 21 · p17_rdc.py
**Nombre UI:** Rendición de Cuentas (RDC)
**Rol:** Checklist RDC + 4 fases de preparación.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 8 — Participación Ciudadana |
| **Hojas Excel** | H10c_RDC_APORTES · H31_REPORTE_CPCCS |
| **Índices** | 2/20 OK · 11 urgentes · CPCCS V=0 (meta ≥70) · IFE-A=72.73% actualizado · 4 fases (May-Jun → Sep) |
| **Entidades** | GAD · CPCCS · Ciudadanía · 7 parroquias |
| **Territorialidad** | Cantón |
| **Relaciones** | → p15_transparencia (ITAM para RDC) · → p16_gobernanza (ciclo PP→RDC) · → p_cadena_institucional (Tab RDC) |
| **Acción** | Completar 11 urgentes antes de junio → CPCCS V sube ≥70 → RDC aprobado |

---

### 22 · p18_cooperacion.py
**Nombre UI:** Cooperación Internacional
**Rol:** 6 fondos activos con elegibilidad y llaves maestras.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 10 — Cooperación Internacional |
| **Hojas Excel** | H73_OUTPUT_API (índices de elegibilidad) |
| **Índices** | GEF $180K (LISTO) · PNUD $2.4M (ELEGIBLE — brecha 1.44 pts) · CAF $1.2M (EN GESTIÓN) · BDE $3.5M (BLOQUEADO — ISP < 65%) · Gender Bond $95K (BLOQUEADO — PSG < 30%) · ONU Mujeres $65K (BLOQUEADO) |
| **Entidades** | GEF/MAATE · PNUD Ecuador · BID Lab · CAF · ONU Mujeres · BDE |
| **Territorialidad** | Colorado (GEF) · Isabel Muentes (PNUD) · Aníbal San Andrés (Gender Bond) · Cantón (BDE/CAF) |
| **Relaciones** | → p11_ods (ODS vinculados) · → p19_genero (PSG llave) · → p4_geotwin (Gov Twin) · → p7_brecha (ISP llave) |
| **Acción** | 2 llaves maestras: ISP 14.58%→65% (BDE $3.5M) + PSG 12.83%→30% (Gender Bond $160K) |

---

### 23 · p19_genero.py (Tab 1: Género + Tab 2: Ambiente)
**Nombre UI:** Género, Equidad y Ambiente
**Rol:** PSG=12.83% + 6 indicadores IGM + 6 metas FA ambiente.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 9 — Género y Ambiente |
| **Hojas Excel** | H73_OUTPUT_API · H99_ENGINE_CORE · H31_REPORTE_CPCCS |
| **Índices** | PSG=12.83% (RUPTURA) · 6 IGM (4 sin dato oficial · 2 binarios) · ODS 5.1/5.2/5.4/5.5/5.a/5.c · FA-CC-01 Ti=0% (riesgo RDC) · FA-DIS-01 Ti=0% · PP 74 fichas ambiente |
| **Entidades** | GAD · Patronato · ONU Mujeres · BID Lab · MAATE · EP Aseo |
| **Territorialidad** | Aníbal San Andrés (luminarias) · Isabel Muentes (agua/acarreo) · Colorado (reforestación) |
| **Relaciones** | → p18_cooperacion (Gender Bond desbloqueado por PSG) · → p11_ods (ODS 5) · → p16_gobernanza (PP fichas ambiente) |
| **Acción** | Reclasificar POA en 15 días → PSG 12.83%→~20% → Gender Bond $95K desbloqueado |

---

### 24 · m4_analisis.py (container técnico)
**Nombre UI:** Análisis (container — Técnico/Admin)
**Rol:** Agrega tablero + eficiencia + metas + cadena + operación.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 5 — Análisis + Dom 3 — Planificación |
| **Hojas Excel** | Múltiples (delegado a módulos atómicos) |
| **Índices** | Todos los del Técnico consolidados |
| **Entidades** | GAD · todas las Direcciones |
| **Territorialidad** | Cantón |
| **Relaciones** | Contiene: p1_dashboard · p14_eficiencia · p8_metas · p12_cadena · p5_operacion |
| **Acción** | Centro de análisis técnico de dirección |

---

### 25 · p_cadena_institucional.py
**Nombre UI:** Cadena Institucional (Vista Técnica del Analista)
**Rol:** Orquesta 7 eslabones con capa HITL. Vista técnica unificada.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 3 — Planificación y Ejecución (todos los eslabones) |
| **Hojas Excel** | H63_S0_CNE · H31_REPORTE_CPCCS · H05b PAC · G71-78 eSIGEF · H90 · H10_PARTICIPACIÓN · H10c_RDC |
| **Índices** | 7 semáforos: CNE=SEGUIMIENTO · PDOT=TRANSICIÓN · POA-PAC=RUPTURA · Presupuesto=RUPTURA · PP=EN PROCESO · RDC=PENDIENTE · LOTAIP=PARCIAL |
| **Entidades** | Todas (CNE → ciudadanía) |
| **Territorialidad** | Cantón |
| **Relaciones** | Importa: p16_gobernanza · p8_metas · p12_cadena · p17_rdc · p15_transparencia · p_cadena_institucional HITL widgets |
| **Acción** | Vista de analista para validar coherencia de la cadena completa antes de informes oficiales |

---

### 26 · p_congruencia.py
**Nombre UI:** Congruencia Institucional (Sistema QUIRA)
**Rol:** Estado de las 3 capas del sistema (Fuente Operativa / Memoria Institucional / Motor Analítico).

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 12 — Observabilidad Longitudinal (meta-nivel) |
| **Hojas Excel** | Supabase · data/gm_snapshot.json |
| **Índices** | 3 pilares: Fuente Operativa (docs cargados) · Memoria Institucional (vault) · Motor Analítico (KPIs, períodos, reglas) · Integridad Semántica (Motor vs Memoria) |
| **Entidades** | Sistema QUIRA (meta) |
| **Territorialidad** | Sistema (no territorial) |
| **Relaciones** | → p_sentinel_hub · → p_historico · → p_ingesta |
| **Acción** | Verificar estado del sistema QUIRA antes de generar informes → detectar incoherencias entre capas |

---

### 27 · m5_control.py (container técnico)
**Nombre UI:** Control (container — Técnico/Admin)
**Rol:** 9 tabs operativos del técnico.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 12 (control) + Dom 3 (operativo) |
| **Hojas Excel** | Múltiples (delegado a módulos) |
| **Índices** | Pipeline estado · alertas activas · historial snapshots · reportes · gestión |
| **Entidades** | Equipo QUIRA (interno) |
| **Territorialidad** | Sistema |
| **Relaciones** | Contiene: p_sentinel_hub · p_carga · p_ingesta · p_historico · p_alertas · p_seguimiento · p_reportes · p_gestion · Sentinel IA |
| **Acción** | Hub operativo del técnico — todo lo que no es analytics va aquí |

---

### 28 · p_alertas.py (alert_engine)
**Nombre UI:** Monitor de Alertas
**Rol:** Alert engine basado en ejecución + cobertura. SLA + HITL resolución.

| Campo | Valor |
|-------|-------|
| **Dominio** | Dom 12 — Observabilidad Longitudinal |
| **Hojas Excel** | H07_S5_FINANCIERO_eSIGEF · H73_OUTPUT_API |
| **Índices** | Alertas "ejecucion" + "cobertura" · SLA tracking · antecedentes comparables · export XLSX para LOTAIP/RDC |
| **Entidades** | Todas las entidades del Holding |
| **Territorialidad** | Cantón |
| **Relaciones** | → p9_sat · → m2_alertas · → p5_operacion (HITL) |
| **Acción** | Resolver alertas con contexto histórico → SHA-256 → cierre documentado |

---

### 29 · env_ops.py (ambiente interno Dylus Lab)
**Nombre UI:** ⚙ Ops (INTERNO — nunca visible al municipio)
**Rol:** Pipeline · Snapshots · Reliability · Gold Master · Configuración.

| Campo | Valor |
|-------|-------|
| **Dominio** | Sistema (meta-nivel — no en 12 dominios) |
| **Hojas Excel** | Gold Master completo · H82_CONFIG_PARAMS · H73_OUTPUT_API |
| **Índices** | Reliability scores: Gold Master 99% · DPE API 95% · SERCOP 95% · CPCCS 80% · Evidencia social 45% |
| **Entidades** | Equipo Dylus Lab |
| **Territorialidad** | Sistema |
| **Relaciones** | → p_sentinel_hub · → p_carga · → p_ingesta · → p_historico |
| **Acción** | Gestión del sistema, versionado Gold Master, health check del pipeline |

---

### 30 · env_civic.py + env_impact.py (placeholders futuros)
**Estado:** PRÓXIMAMENTE — condición: GOV estable + 6 meses datos longitudinales

| Módulo | Dominio Futuro | Propósito |
|--------|---------------|-----------|
| env_civic.py | Participación ciudadana ampliada | Vista pública · evidencia ciudadana con reliability_score propio |
| env_impact.py | Cooperación (reportes) | Policy briefs · dashboards BID/PNUD/CAF · outputs multilaterales |

---

## GRAFO DE RELACIONES (para Graphify)

```
[Dom 1 — Salud Institucional]
  p_vista_ejecutiva ──→ p7_brecha
  p_vista_ejecutiva ──→ p9_sat
  p6_pulso ──→ p7_brecha
  p7_brecha ──→ p13_simulador
  p7_brecha ──→ p14_eficiencia
  p7_brecha ──→ p10_inversion
  p7_brecha ──→ p19_genero (PSG)

[Dom 2 — Fidelidad Política]
  p3_congruencias ──→ p8_metas
  p3_congruencias ──→ p16_gobernanza
  p16_gobernanza ──→ p17_rdc

[Dom 3 — Planificación y Ejecución]
  p8_metas ──→ p12_cadena (SAT-0)
  p12_cadena ──→ p5_operacion
  p_cadena_institucional ORQUESTA {p16_gobernanza, p8_metas, p12_cadena, p17_rdc, p15_transparencia}

[Dom 4 — Holding Municipal]
  p2_holding ──→ p14_eficiencia
  p2_holding ──→ p5_operacion
  p5_operacion ──→ alert_engine (p_alertas)

[Dom 5 — Análisis de Eficiencia]
  p14_eficiencia ──→ p12_cadena
  p13_simulador ──→ p19_genero
  p13_simulador ──→ p10_inversion

[Dom 6 — Equidad Territorial]
  p4_geotwin ──→ p10_inversion
  p10_inversion ──→ p18_cooperacion
  p4_geotwin ──→ p3_congruencias (congruencia territorial)

[Dom 7 — Transparencia]
  p15_transparencia ──→ p17_rdc

[Dom 8 — Participación Ciudadana]
  p16_gobernanza ──→ p17_rdc
  p17_rdc ──→ p15_transparencia

[Dom 9 — Género y Ambiente]
  p19_genero ──→ p18_cooperacion (PSG llave → Gender Bond)
  p19_genero ──→ p11_ods (ODS 5)

[Dom 10 — Cooperación Internacional]
  p18_cooperacion ──→ p11_ods
  p18_cooperacion ──→ p4_geotwin (Gov Twin)

[Dom 11 — Agenda 2030]
  p11_ods ──→ p18_cooperacion (fondos)

[Dom 12 — Observabilidad Longitudinal]
  m2_alertas ──→ longitudinal_engine
  p_alertas ──→ p9_sat
  p_congruencia VERIFICA {Fuente, Memoria, Motor}
  env_ops GESTIONA {pipeline, snapshots, gold_master}
```

---

## CAUSALIDADES CRÍTICAS (para IA / Sentinel)

| Causa | Efecto | Módulos afectados |
|-------|--------|-------------------|
| ISP 14.58% < 65% | BDE $3.5M BLOQUEADO → ICPI D1 bajo | p7_brecha · p18_cooperacion · p14_eficiencia |
| PSG 12.83% < 30% | Gender Bond $95K + ONU Mujeres $65K BLOQUEADOS | p19_genero → p18_cooperacion |
| ICGI-T ≥ 55% | PNUD $2.4M desbloqueado (brecha 1.44 pts) | p10_inversion → p18_cooperacion |
| 4 metas sin PAC | SAT-0 activa → riesgo Contraloría | p12_cadena → p_alertas |
| 24 proc sin SHA-256 | Riesgo contractual CRÍTICO | p12_cadena → p9_sat |
| Ti < 60% × 3 períodos | Reincidencia (doctrina RC-M) | m2_alertas longitudinal |
| IED DTIC 18.3% | ICPI D2 baja → brecha eficiencia | p14_eficiencia → p7_brecha |
| FA-CC-01 Ti=0% | RDC 2026 sin evidencia CC → CPCCS nota baja | p19_genero (Ambiente) → p17_rdc |
| PSG reclasif. POA | PSG 12.83% → ~20% en 15 días (sin reforma) | p19_genero → p18_cooperacion |

---

## HOJAS EXCEL × MÓDULOS (índice invertido)

| Hoja Gold Master | Módulos que la consumen |
|-----------------|------------------------|
| H73_OUTPUT_API | p_vista_ejecutiva · p6_pulso · p7_brecha · p9_sat · p11_ods · p14_eficiencia · p15_transparencia · p18_cooperacion · p19_genero · p13_simulador |
| H07_S5_FINANCIERO_eSIGEF | p_vista_ejecutiva · m2_alertas · p_cadena_institucional · p_alertas |
| H90_PRESUPUESTO_CONSOLIDADO | p2_holding · p_cadena_institucional |
| H71_EP_ADSCRITAS | p2_holding |
| H99_ENGINE_CORE | p8_metas · p10_inversion · p13_simulador · p19_genero |
| H31_REPORTE_CPCCS | p8_metas · p19_genero · p_cadena_institucional |
| H63_S0_CNE | p3_congruencias · p16_gobernanza · p_cadena_institucional |
| H10_S8_PARTICIPACIÓN_CPCCS | p16_gobernanza · p_cadena_institucional |
| H10c_RDC_APORTES | p16_gobernanza · p17_rdc · p19_genero (FA ciclo) |
| H16/H24 | p3_congruencias · p4_geotwin |
| H82_CONFIG_PARAMS | env_ops |
| G71-78 eSIGEF | p_cadena_institucional (presupuesto tab) |
| H05/H05b PAC | p5_operacion · p12_cadena |

---

## ENTIDADES × DOMINIOS (índice institucional)

| Entidad | Dominios relevantes | Módulos primarios |
|---------|--------------------|--------------------|
| GAD Central (Alcaldía) | Dom 1, 2, 3, 5, 7 | p_vista_ejecutiva · p3_congruencias · p8_metas |
| EP Aseo (EMAI) | Dom 4 | p2_holding · p5_operacion |
| Bomberos | Dom 4 | p2_holding |
| Patronato Municipal | Dom 4, 9 | p2_holding · p19_genero |
| Ciudadanía | Dom 8, 7 | p16_gobernanza · p17_rdc · p15_transparencia |
| CPCCS | Dom 8 | p17_rdc |
| CNE | Dom 2 | p3_congruencias · p16_gobernanza |
| PNUD | Dom 10, 6 | p18_cooperacion · p4_geotwin |
| GEF/MAATE | Dom 9, 10 | p18_cooperacion · p19_genero |
| BID Lab | Dom 9, 10 | p18_cooperacion · p19_genero |
| BDE | Dom 10 | p18_cooperacion |
| Contraloría | Dom 3 | p12_cadena (SAT-0) |
| DPE | Dom 7 | p15_transparencia |
| SERCOP | Dom 3 | p12_cadena |

---

## TERRITORIALIDAD × MÓDULOS

| Territorio | Módulos clave | Indicadores críticos |
|-----------|--------------|---------------------|
| Isabel Muentes | p4_geotwin · p10_inversion · p12_cadena · p19_genero | $40/hab · agua 1.02% · TPS 77.94 · EMERGENCIA |
| La Pila (rural) | p4_geotwin · p10_inversion | $93/hab · única rural · IRS objetivo |
| Colorado | p4_geotwin · p18_cooperacion · p19_genero | reforestación GEF $180K |
| Aníbal San Andrés | p4_geotwin · p19_genero · p18_cooperacion | Pin Morado · Gender Bond $95K |
| Montecristi (cabecera) | p4_geotwin | $217/hab · brecha 5.4× vs Isabel Muentes |
| Gral. Alfaro · Leónidas Proaño | p4_geotwin · p10_inversion | Rango normal |
| Cantón (global) | Todos | ICPI=17.45% · TGI=66.79% |

---

## NOTA DE ARQUITECTURA (para D.3)

### Regla de navegación D-Sprint:
- **CAPA 1** (pantalla principal) = 12 tarjetas dominio → cada dominio abre CAPA 2
- **CAPA 2** (dashboards profundos) = módulos existentes refactorizados por dominio
- **CAPA 3** = Control (operativo técnico, no en pantalla principal)

### Módulos a refactorizar (D.4):
Los módulos actuales son reutilizables. Lo que cambia es:
- **Agrupación:** cada módulo cae en 1 dominio canónico
- **Navegación:** las tarjetas CAPA 1 son las puertas de entrada
- **Naming UI:** NUNCA usar siglas internas (SAT, TGI, etc.) en etiquetas visibles

### Módulos nuevos necesarios (D.3):
- `p_dominio_card.py` (componente de tarjeta CAPA 1) — nuevo
- Actualizar `env_gov.py` para routing por dominio — refactor

---

*D.2 completado — Dylus Lab © 2026-05-28*
