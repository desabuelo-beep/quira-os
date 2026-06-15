# H36c_OBSIDIAN_MAP — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=62 · pobladas=58 · fórmulas=20
inputs(lee de): H01_PARÁMETROS, H98_TGI_FRAMEWORK, H99_ENGINE_CORE
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE, #REF
ERRORES: C13: #REF!
MARCADORES: E45: ICM=100% — digitalización rural pendiente · C50: La columna Valor_Excel siempre usa fórmula Excel — nunca valores hardc

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
I1	=TODAY()
C7	=H98_TGI_FRAMEWORK!B25
C8	=H98_TGI_FRAMEWORK!B36
C9	=H98_TGI_FRAMEWORK!B41
C10	=H98_TGI_FRAMEWORK!B42
C11	=H98_TGI_FRAMEWORK!D20
C12	=H98_TGI_FRAMEWORK!D21
C13	=H98_TGI_FRAMEWORK!D22 · #REF! · #REF!
C14	=H98_TGI_FRAMEWORK!D23
C15	=H98_TGI_FRAMEWORK!D24
C16	=H99_ENGINE_CORE!B16
C17	=H99_ENGINE_CORE!B18
C18	=H99_ENGINE_CORE!B19
C19	=H99_ENGINE_CORE!B20
C20	=H99_ENGINE_CORE!B21
C21	=H99_ENGINE_CORE!B23
C22	=H99_ENGINE_CORE!B48
C23	=H99_ENGINE_CORE!B52
C24	=H01_PARÁMETROS!B15*100
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H36c_OBSIDIAN_MAP
A2	H36c — OBSIDIAN MAP — PUENTE EXCEL → VAULT → SENTINEL
A3	★ MAPA DE CONEXIÓN: Variables cuantitativas del motor Excel (SIAP-ICPI) → Notas de contexto normativo (Vault Obsidian) → Alertas operativas (Sentinel). SOLO SE EXPONEN OUTPUTS — nunca fórmulas ni arquitectura interna.
A4	⛓ Cadena canónica: SIAP-ICPI (motor) → QUIRA OS → TGI 5D → PND/PDyOT → Legalidad → Territorio
A5	▌ MAPA PRINCIPAL — VARIABLES TGI 5D + INDICADORES TERRITORIALES
A6	Variable_QUIRA
B6	Descripcion
C6	Valor_Excel
D6	Nota_Obsidian
E6	Carpeta_Vault
F6	Dimension_TGI
G6	Prioridad
H6	Tipo_Alerta
I6	Estado
A7	TGI_SCORE_GLOBAL_5D
B7	Score TGI 5 dimensiones — GADM Montecristi 2026
D7	[[02_TGI_DIMENSIONES]]
E7	00_CORE
F7	D1+D2+D3+D4+D5
G7	ALTA
H7	STATUS
I7	✅ ACTIVO
A8	TGI_CLASIFICACION_AVEP
B8	Nivel AVEP del cantón (Transición · Gobernanza · Excelencia · etc.)
D8	[[02_TGI_DIMENSIONES]]
E8	00_CORE
F8	D1+D2+D3+D4+D5
G8	ALTA
H8	STATUS
I8	✅ ACTIVO
A9	TGI_META_2027
B9	Meta TGI cantonal al cierre del período 2027
D9	[[02_TGI_DIMENSIONES]]
E9	00_CORE
F9	D1+D2+D3+D4+D5
G9	ALTA
H9	META
I9	✅ ACTIVO
A10	TGI_BRECHA_A_META
B10	Puntos que faltan para alcanzar meta 2027 (positivo = déficit)
D10	[[02_TGI_DIMENSIONES]]
E10	00_CORE
F10	D1+D2+D3+D4+D5
G10	ALTA
H10	BRECHA
I10	✅ ACTIVO
A11	TGI_D1_Legalidad
B11	Trust Score metodológico — calidad coherencia normativa
D11	[[01_TGI_FRAMEWORK]]
E11	00_CORE
F11	D1
G11	MEDIA
H11	INFO
I11	✅ ACTIVO
A12	TGI_D2_Planificacion
B12	ICPI Real 2025 × 100 — fidelidad de planificación PDyOT
D12	[[03_SIAP_ICPI_METHOD]]
E12	00_CORE
F12	D2
G12	ALTA
H12	INFO
I12	✅ ACTIVO
A13	TGI_D3_Ejecucion
B13	Ti Inversión 2025 × 100 — ejecución presupuestaria grupos 7+8
D13	[[ALERTA-D3_Ejecucion_Critica]]
E13	00_CORE
F13	D3
G13	CRÍTICA
H13	🔴 ALERTA_ROJA
I13	✅ ACTIVO
A14	TGI_D4_Equidad
B14	IET Rural Avg — equidad territorial parroquias P02-P07 (cap 100)
D14	[[ALERTA-Regresividad_IRS79]]
E14	00_CORE
F14	D4
G14	CRÍTICA
H14	🔴 ALERTA_ROJA
I14	✅ ACTIVO
A15	TGI_D5_Capacidad
B15	ICM SNP × 100 — cumplimiento reporte al Sistema Nacional de Planificación
D15	[[04_TGI_INDICADORES]]
E15	00_CORE
F15	D5
G15	MEDIA
H15	INFO
I15	✅ ACTIVO
A16	IRS_GLOBAL
B16	Índice Regresividad Espacial — concentración inversión en cabecera cantonal
D16	[[ALERTA-Regresividad_IRS79]]
E16	00_CORE
F16	D4
G16	CRÍTICA
H16	🔴 ALERTA_ROJA
I16	✅ ACTIVO
A17	IRS_META_2027
B17	Meta IRS para cierre 2027 — reducir regresividad espacial a ≤ 45
D17	[[ALERTA-Regresividad_IRS79]]
E17	00_CORE
F17	D4
G17	ALTA
H17	META
I17	✅ ACTIVO
A18	IET_PERCAPITA_MIN
B18	IET mínimo — parroquia con menor inversión per cápita relativa al promedio cantonal
D18	[[ALERTA-Regresividad_IRS79]]
E18	00_CORE
F18	D4
G18	ALTA
H18	🟠 ALERTA_NARANJA
I18	✅ ACTIVO
A19	COMPOSITE_NEED_LEADER
B19	Parroquia con mayor necesidad compuesta CN = NBI+Agua_gap+Pob (v2.1)
D19	[[ALERTA-Isabel_Muentes]]
E19	00_CORE
F19	D4
G19	CRÍTICA
H19	🔴 ALERTA_ROJA
I19	✅ ACTIVO
A20	BRECHA_FONDOS_BLOQUEADA
B20	Fondos bloqueados estimados por regresividad territorial (USD)
D20	[[ALERTA-Brecha_Rural_1.79M]]
E20	00_CORE
F20	D4
G20	CRÍTICA
H20	🔴 ALERTA_ROJA
I20	✅ ACTIVO
A21	NBI_RURAL_PROM
B21	NBI promedio parroquias rurales P02-P07 (INEC Censo 2022)
D21	[[P-06_Isabel_Muentes]]
E21	07_TGI_Parroquias
F21	D4
G21	ALTA
H21	🟠 ALERTA_NARANJA
I21	✅ ACTIVO
A22	TGI_PARROQUIA_CRITICA
B22	Parroquia con menor TGI Score — mayor vulnerabilidad estructural
D22	[[P-06_Isabel_Muentes]]
E22	07_TGI_Parroquias
F22	D4
G22	ALTA
H22	STATUS
I22	✅ ACTIVO
A23	TGI_5D_RURAL_AVG
B23	TGI promedio parroquias rurales P02-P07
D23	[[TGI_Cantonal]]
E23	07_TGI_Parroquias
F23	D1+D2+D3+D4+D5
G23	ALTA
H23	STATUS
I23	✅ ACTIVO
A24	ICPI_GLOBAL
B24	ICPI cantonal 2025 — motor D2 planificación (H01 parámetros)
D24	[[03_SIAP_ICPI_METHOD]]
E24	00_CORE
F24	D2
G24	ALTA
H24	INFO
I24	✅ ACTIVO
A25	SENTINEL_GLOBAL_STATUS
B25	Estado global del Holding Municipal (ROJO/AMARILLO/VERDE) segun Ti inversion
C25	ROJO (Q1-2026 Ene-Feb)
D25	[[_Indice Sentinel]]
E25	06_Sentinel
F25	D3
G25	CRITICA
H25	STATUS
I25	ACTIVO
A26	SENTINEL_ALERTAS_CRITICAS
B26	Total alertas criticas activas en el Holding (Ti menor 15%)
C26	3 activas Q1-2026 (GAD+Bomberos+Patronato)
D26	[[ALERTA-Holding_Ti_Critico_2026]]
E26	06_Sentinel
F26	D3
G26	ALTA
H26	ALERTA
I26	ACTIVO
A27	SENTINEL_TI_GAD
B27	Ti inversion GAD Municipal de Montecristi - serie mensual Q1-2026
C27	8.5% Ene / 12.8% Feb / 18.2% Mar
D27	[[CEDULAS_HOLDING_ENE_MAR_2026]]
E27	06_Sentinel
F27	D3
G27	CRITICA
H27	STATUS
I27	ACTIVO
A28	SENTINEL_TI_BOMBEROS
B28	Ti inversion Cuerpo de Bomberos de Montecristi - serie mensual Q1-2026
C28	22.3% Ene / 28.7% Feb / 35.8% Mar
D28	[[CEDULAS_HOLDING_ENE_MAR_2026]]
E28	06_Sentinel
F28	D3
G28	ALTA
H28	STATUS
I28	ACTIVO
A29	SENTINEL_TI_EMAI_EP
B29	Ti inversion EMAI-EP Empresa Municipal de Aseo Integral - serie Q1-2026
C29	41.2% Ene / 38.5% Feb / 44.1% Mar
D29	[[CEDULAS_HOLDING_ENE_MAR_2026]]
E29	06_Sentinel
F29	D3
G29	MEDIA
H29	STATUS
I29	ACTIVO
A30	SENTINEL_TI_PATRONATO
B30	Ti inversion Patronato Municipal de Amparo Social - serie mensual Q1-2026
C30	12.1% Ene / 19.4% Feb / 28.3% Mar
D30	[[CEDULAS_HOLDING_ENE_MAR_2026]]
E30	06_Sentinel
F30	D3
G30	ALTA
H30	STATUS
I30	ACTIVO
A31	SENTINEL_VERSION
B31	Version RC activa de QUIRA OS Sentinel en produccion
C31	RC-1.1
D31	[[_Indice Sentinel]]
E31	06_Sentinel
F31	D5
G31	MEDIA
H31	INFO
I31	ACTIVO
A32	SENTINEL_PATRON_TOP
B32	Causa raiz mas frecuente de alertas segun Memoria Operativa (Sprint 2.8A)
C32	reforma_presupuestaria (freq=3)
D32	[[SENTINEL-Aprendizaje]]
E32	06_Sentinel
F32	D3
G32	MEDIA
H32	INFO
I32	ACTIVO
A33	SENTINEL_ALERTAS_ARCHIVADAS
B33	Total alertas archivadas (caso cerrado) en Supabase - Ruta de Atencion
C33	0 archivadas Q1-2026 (sistema nuevo RC-1.1)
D33	[[SENTINEL-Ruta-Atencion]]
E33	06_Sentinel
F33	D3
G33	MEDIA
H33	INFO
I33	ACTIVO
A34	KB_POA_2023_2024_GADM
B34	POA GADM 2023 (1,448 actividades, 18 Direcc.) + POA 2024 (0.1M) — base evidencia D2 fidelidad planificación PDyOT→POA
D34	[[POA_2023_2024_GADM]]
E34	08_EJECUCION
F34	D2+D3
G34	ALTA
H34	INFO
I34	✅ ACTIVO
A35	KB_PAC_2023_2024_GADM
A36	KB_PATRONATO_OPERATIVO
B36	Patronato: POA+PAC+Presupuesto+RDC 2023-2024 · Ti 2024=60.44% (Gold Master canon) · RDC 2023 autodeclara 47.99% (no canon) · informe 12068/14976
A37	KB_PPI_INVERSIONES_2024_2027
B37	Plan Plurianual Inversiones PDOT 2024-2027: 57.6M · 5 sistemas · AH=1M capital real · PI=0.3M (talento humano 2.8M) · pico AH 2026=3.3M
A39	▌ MAPA NOTAS OBSIDIAN — COBERTURA POR DIMENSIÓN TGI
A40	Dimension_TGI
B40	Peso_TGI
C40	Notas_Obsidian_Clave
A41	D1 — Legalidad (20%)
B41	20%
C41	[[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]]
A42	D2 — Planificación (20%)
A43	D3 — Ejecución (25%)
B43	25%
C43	[[ALERTA-D3_Ejecucion_Critica]] · [[04_TGI_INDICADORES]] · [[PAC_2023_2024_GADM]] · [[PATRONATO_Operativo_2023_2024]]
A44	D4 — Equidad (25%)
B44	25%
C44	[[ALERTA-Regresividad_IRS79]] · [[ALERTA-Isabel_Muentes]] · [[ALERTA-Brecha_Rural_1.79M]]
A45	D5 — Capacidad (10%)
B45	10%
C45	[[04_TGI_INDICADORES]] · [[03_SIAP_ICPI_METHOD]]
D45	CAPA 20-21 (CGE + Digital)
E45	ICM=100% — digitalización rural pendiente
F45	Implementar infocentros Art.34 LOTDIT
A48	▌ REGLAS DE INTEGRIDAD — CONTRATO EXCEL ↔ OBSIDIAN ↔ SENTINEL
A49	R1
B49	OUTPUTS SOLAMENTE
C49	Obsidian NUNCA muestra fórmulas, nombres de hojas ni arquitectura interna del Excel (trade secret Dylus Lab)
A50	R2
B50	VALORES CALCULADOS
C50	La columna Valor_Excel siempre usa fórmula Excel — nunca valores hardcoded
A51	R3
B51	WIKILINKS CANÓNICOS
C51	Los [[wikilinks]] deben coincidir exactamente con el filename en el vault Obsidian (sin extensión .md)
A52	R4
B52	SINGLE SOURCE OF TRUTH
C52	Si un valor cambia en la fuente (H01, H07b, H99), se propaga automáticamente aquí y a Obsidian
A53	R5
B53	PROPIEDAD INTELECTUAL
C53	SIAP-ICPI Gold Master + Vault QUIRA = propiedad de Dylus Lab © 2026 — no distribuir sin autorización
A55	QUIRA OS · Dylus Lab © 2026 · GAD Municipal de Montecristi, Ecuador · H36c_OBSIDIAN_MAP v1.0 · 2026-05-17
A56	▌ QUIRA OS SENTINEL RC-2 — AUTOMATIZACIÓN INSTITUCIONAL
A57	SLA Institucional (RC-2A)
B57	48h Crítica / 120h Advertencia
C57	[[RC2_SLA_WATCHDOG]] · [[_Indice Sentinel]]
D57	CAPA RC-2A (Gestión SLA)
E57	Badge SLA en cada alerta · Widget cumplimiento en Vista Ejecutiva
F57	Monitorear alertas VENCIDAS → escalar a director según protocolo RC-2B
A58	Watchdog Silencio (RC-2B)
B58	threshold=7 días
C58	[[RC2_SLA_WATCHDOG]] · [[_Indice Sentinel]]
D58	CAPA RC-2B (Vigilancia autónoma)
E58	Detecta entidades sin carga de evidencia · genera alerta tipo silencio automáticamente
F58	El sistema vigila aunque nadie lo abra — RC-2B principio no-decisional
A59	Escalamiento Automático (RC-2B)
B59	VENCIDO → ESCALADO en 7d
C59	[[RC2_SLA_WATCHDOG]]
D59	CAPA RC-2B (Escalamiento)
E59	Watchdog escala alertas VENCIDAS a nivel director — nunca cierra, nunca resuelve
F59	Ejecutado por scheduler cada 60 min en cada carga autenticada
A60	Scheduler Autónomo (RC-2B)
B60	3 tareas (30/60/240 min)
C60	[[RC2_SLA_WATCHDOG]]
D60	CAPA RC-2B (Programación)
E60	sla_refresh + watchdog_silencio + watchdog_escalamiento — oportunista, sin hilos
F60	Log en scheduler_log Supabase · cada sesión autenticada dispara tick()
A61	Digest Ejecutivo (RC-2B)
B61	Mes anterior automático
C61	[[RC2_SLA_WATCHDOG]] · [[_Indice Sentinel]]
D61	CAPA RC-2B (Reportería)
E61	PDF del mes anterior generado con un clic desde Vista Ejecutiva
F61	Botón "Digest Automático" — datos históricos disponibles desde Supabase
A62	Histórico 2025
B62	38 cédulas ingesta masiva
C62	[[RC2_SLA_WATCHDOG]]
D62	DATOS REALES 2025
E62	BOMBEROS 12/12 | EMAI-EP 11/11 | GAD 3/12 | PATRONATO 12/12 (inc. PDF)
F62	Ti dic-2025: GAD=72.73% | EMAI-EP=90.47% | PATRONATO=50% | BOMBEROS=16.38%
```