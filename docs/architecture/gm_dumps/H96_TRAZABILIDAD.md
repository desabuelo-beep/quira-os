# H96_TRAZABILIDAD — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=23 · pobladas=22 · fórmulas=0
inputs(lee de): —
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
(sin fórmulas)
```

## ETIQUETAS / DATOS (tope 600)
```
A1	H96 — TRAZABILIDAD DE DATOS · SIAP-ICPI v5.3 TGI · GADM Montecristi 2026
A2	Linaje completo de cada variable del modelo TGI. Requerido por cooperantes (BID, GIZ, USAID) y para publicación científica. Cada fila es una variable trazable hasta su fuente primaria.
A4	Variable_TGI
B4	Descripción
C4	Fuente_Primaria
D4	Hoja_Excel
E4	Celda_Referencia
F4	Tipo_Dato
G4	Fecha_Actualización
H4	Responsable
A5	D1_Legalidad (Trust_Score)
B5	Calidad metodológica del proceso normativo — Trust Score SIAP-ICPI
C5	SIAP-ICPI v1.0 — Metodología Dylus Lab
D5	H01_PARÁMETROS
E5	B180
F5	Constante manual
G5	2026-05-14
H5	Javo Delgado
A6	D2_Planificacion (ICPI)
B6	ICPI_Real_2025 × 100 — Índice Compuesto Proyectos Inversión
C6	eSIGEF GAD Montecristi + SIGAD SNP — cierre 2025
D6	H01_PARÁMETROS
E6	B15
F6	Resultado motor H12
G6	2026-05-14
H6	Javo Delgado
A7	D3_Ejecucion (Ti)
B7	Ti_Inversión_2025 × 100 — devengado/codificado grupos 7+8
C7	eSIGEF — Sistema de Gestión Financiera Pública Ecuador
D7	H07b_Ti_INVERSIÓN_eSIGEF
E7	B18
F7	Constante verificada
G7	2026-05-14
H7	Javo Delgado
A8	D4_Equidad (IET_Local)
B8	MIN(100, IET_Local_Pct) — Índice de Equidad Territorial por parroquia
C8	H99_ENGINE_CORE — calculado de Inv_PerCapita/Cantonal_Avg
D8	H99_ENGINE_CORE
E8	J7:J13
F8	Calculado de constantes
G8	2026-05-14
H8	Javo Delgado
A9	D5_Capacidad (ICM_SNP)
B9	ICM_SNP_SIGAD × 100 — cumplimiento reporte Sistema Nacional Planificación
C9	SNP — Secretaría Nacional de Planificación Ecuador
D9	H01_PARÁMETROS
E9	B12
F9	Constante manual
G9	2026-05-14
H9	Javo Delgado
A10	Población_2022
B10	Población por parroquia del cantón Montecristi
C10	INEC — Censo de Población y Vivienda 2022
D10	H99_ENGINE_CORE
E10	D7:D13
F10	Constante censal
G10	2022
H10	INEC / Javo Delgado
A11	NBI_Pct
B11	Necesidades Básicas Insatisfechas por parroquia
C11	INEC — Censo 2022 — NBI multidimensional
D11	H99_ENGINE_CORE
E11	E7:E13
F11	Constante censal
G11	2022
H11	INEC / Javo Delgado
A12	Cobertura_Agua_Pct
B12	Cobertura de agua potable por red pública (% hogares)
C12	INEC — Censo 2022 / PDOT Montecristi 2023-2027
D12	H99_ENGINE_CORE
E12	F7:F13
F12	Constante mixta
G12	2022-2023
H12	GADM / Javo Delgado
A13	Inv_PerCapita_Q1_2026
B13	Inversión per cápita ejecutada Q1 2026 (grupos 7+8 / habitante)
C13	eSIGEF Q1 2026 — devengado grupos 7+8 / INEC 2022
D13	H99_ENGINE_CORE
E13	G7:G13
F13	Calculado
G13	2026-04-30
H13	Javo Delgado
A14	Inv_Total_Q1
B14	Inversión total ejecutada por parroquia Q1-2026 (USD)
C14	eSIGEF Q1 2026 — asignación territorial estimada
D14	H99_ENGINE_CORE
E14	H7:H13
F14	Constante estimada
G14	2026-04-30
H14	Javo Delgado
A15	Composite_Need
B15	Necesidad compuesta territorial: 0.45×NBI + 0.30×(1-Agua) + 0.25×PobPct
C15	Metodología QUIRA Gov / Dylus Lab — fórmula canónica v2.1
D15	H99_ENGINE_CORE
E15	I7:I13
F15	Calculado de constantes
G15	2026-05-14
H15	Javo Delgado
A16	IET_Local_Pct
B16	Índice Equidad Territorial: (Inv_PerCapita/Cantonal_Avg)×100
C16	Calculado de eSIGEF + INEC — metodología QUIRA
D16	H99_ENGINE_CORE
E16	J7:J13
F16	Calculado de constantes
G16	2026-05-14
H16	Javo Delgado
A17	IRS_Global
B17	Índice de Regresión Territorial: -CORREL(NBI, Inv_PerCapita)×100
C17	Calculado de H99 — metodología QUIRA/Dylus
D17	H99_ENGINE_CORE
E17	B16
F17	Calculado de constantes
G17	2026-05-14
H17	Javo Delgado
A18	ICPI_Real_2025
B18	Índice Compuesto Proyectos Inversión 2025 — motor H12 canónico
C18	eSIGEF + SIGAD + informes Ti_V firmados digitalmente
D18	H12_MOTOR_ICPI_CANÓNICO
E18	B33
F18	Motor SIAP-ICPI
G18	2025-12-31
H18	Javo Delgado
A19	TGI_Score_Parroquia (col M)
B19	TGI per-parroquia 3 componentes: equidad+proximidad+desarrollo (v5.x)
C19	Calculado de H99: IET_Local, Desviacion_Ideal, NBI
D19	H99_ENGINE_CORE
E19	M7:M13
F19	Fórmula
G19	2026-05-16
H19	Claude+Javo Delgado
A20	TGI_Score_5D (col Y)
B20	TGI 5 dimensiones: D1-D5 ponderadas 0.20+0.20+0.25+0.25+0.10
C20	Calculado de H01, H07b, H99 — modelo TGI v5.x
D20	H99_ENGINE_CORE
E20	Y7:Y13
F20	Fórmula
G20	2026-05-16
H20	Claude+Javo Delgado
A21	Brecha_Equidad_Abs_USD
B21	Déficit en USD vs media cantonal por parroquia
C21	Cálculo H99
D21	H99_ENGINE_CORE
E21	Z7:Z13
F21	Fórmula
G21	2026-05-16
H21	QUIRA Gov
A22	Prioridad_Reequilibrio
B22	Score urgencia 0-1 (NBI×0.40 + ΔAgua×0.30 + ΔTGI×0.30)
C22	Cálculo H99
D22	H99_ENGINE_CORE
E22	AA7:AA13
F22	Fórmula
G22	2026-05-16
H22	QUIRA Gov
A23	Clasif_Equidad
B23	Semáforo 4 niveles por IET_Local (Sobre media/Media/Alta/Crítica)
C23	Cálculo H99
D23	H99_ENGINE_CORE
E23	AB7:AB13
F23	Fórmula
G23	2026-05-16
H23	QUIRA Gov
```