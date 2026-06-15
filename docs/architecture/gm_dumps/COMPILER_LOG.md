# COMPILER_LOG — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=20 · pobladas=19 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE
MARCADORES: D11: PENDIENTE · H11: PENDIENTE · I11: Datos de candidatos y plan de gobierno pendientes de carga oficial CNE · I14: Ti_POA fuente: POA_GEO real. NBI rural estimado 67.9% para todos. CNE 

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ COMPILER_LOG — Log de Compilación SCHEMA PDOT → SIAP-ICPI v1.0
C1	Trazabilidad de fuentes y compilación · DYLUS LAB © 2026
A3	Log_ID
B3	Fase
C3	Hoja_Destino
D3	Registros
E3	Fuente_Principal
F3	Fuentes_Secundarias
G3	Fecha_Compilacion
H3	Estado
I3	Observacion
A4	LOG-001
B4	SCHEMA_METADATA
C4	SCHEMA_METADATA
D4	44
E4	PDOT 2023-2027 / H90_PRESUPUESTO / INEC
F4	SIAP-ICPI v1.0 H12!B33
G4	2026-05-08
H4	OK
I4	Todos los campos verificados contra fuentes primarias
A5	LOG-002
B5	SCHEMA_TERRITORIOS
C5	SCHEMA_TERRITORIOS
D5	73
E5	PDOT 2023-2027 p.63 / KB_TERRITORIOS
F5	pdot_checkpoint_v6.json territorios
G5	2026-05-08
H5	OK
I5	8 niveles jerárquicos. GEO_IDs asignados según KB
A6	LOG-003
B6	SCHEMA_NBI
C6	SCHEMA_NBI
D6	múltiple
E6	INEC Censo 2022 / PDOT p.316 / MSP
F6	KB_NBI / pdot_checkpoint_v6.json
G6	2026-05-08
H6	OK
I6	NBI urbano 23% y rural 67.9% verificados PDOT p.316
A7	LOG-004
B7	SCHEMA_METAS
C7	SCHEMA_METAS
D7	56
E7	KB_PROPUESTA_METAS / PDOT
F7	pdot_checkpoint_v6.json propuesta_metas
G7	2026-05-08
H7	OK
I7	56 metas canónicas del PDOT 2023-2027
A8	LOG-005
B8	SCHEMA_PROYECTOS
C8	SCHEMA_PROYECTOS
D8	145
E8	KB_PAI_PROYECTOS / PDOT
F8	pdot_checkpoint_v6.json pai
G8	2026-05-08
H8	OK
I8	145 proyectos PAI 2024-2027 con montos por año
A9	LOG-006
B9	SCHEMA_RIESGOS
C9	SCHEMA_RIESGOS
D9	40
E9	KB_RIESGOS / PDOT
F9	pdot_checkpoint_v6.json riesgos
G9	2026-05-08
H9	OK
I9	40 riesgos territoriales identificados
A10	LOG-007
B10	SCHEMA_ORGANICO
C10	SCHEMA_ORGANICO
D10	82
E10	COOTAD / PDOT / KB_MODELO_PROGRAMAS
F10	KB_ARTICULACIONES / pdot_checkpoint_v6.json
G10	2026-05-08
H10	OK
I10	4 entes + 14 competencias + 16 programas + 48 articulaciones
A11	LOG-008
B11	SCHEMA_CNE
C11	SCHEMA_CNE
D11	PENDIENTE
E11	CNE Ecuador (cne.gob.ec)
F11	PDOT 2023-2027 plan de gobierno
G11	2026-05-08
H11	PENDIENTE
I11	Datos de candidatos y plan de gobierno pendientes de carga oficial CNE
A12	LOG-009
B12	SCHEMA_DICCIONARIO
C12	SCHEMA_DICCIONARIO
D12	40
E12	COOTAD / COPLAFIP / SIAP-ICPI v1.0
F12	SENPLADES / OPS / PDOT 2023-2027
G12	2026-05-08
H12	OK
I12	40 términos ontológicos cubriendo marco legal, indicadores y tecnología
A13	LOG-010
B13	SCHEMA_REGLAS
C13	SCHEMA_REGLAS
D13	26
E13	SIAP-ICPI v1.0 / AVEP Scale
F13	PDOT 2023-2027 / OMS / SENPLADES
G13	2026-05-08
H13	OK
I13	Motor de clasificación y alertas completo
A14	LOG-011
B14	SCHEMA_ECIAP_BRIDGE
C14	SCHEMA_ECIAP_BRIDGE
D14	16
E14	POA_GEOREFERENCIADO (H_SIAP) / KB_NBI
F14	KB_RIESGOS / Usuario PDOT datos servicio
G14	2026-05-08
H14	PARCIAL
I14	Ti_POA fuente: POA_GEO real. NBI rural estimado 67.9% para todos. CNE pendiente
A15	LOG-012
B15	COMPILER_LOG
C15	COMPILER_LOG
D15	12
E15	SIAP-ICPI v1.0 / Script siap_schema_pdot.py
F15	Todos
G15	2026-05-08
H15	OK
I15	Log autogenerado — 12 hojas SCHEMA compiladas
A16	LOG-013
B16	DATOS_EXTERNOS
C16	SCHEMA_NBI + SCHEMA_TERRITORIOS
D16	N/A
E16	Usuario Javo Delgado (datos PDOT p.87, p.115, p.316)
F16	PDOT GAD Montecristi 2023-2027.pdf
G16	2026-05-08
H16	OK
I16	Dotación servicios parroquias, jerarquía asentamientos, proyecciones 2035, desechos sólidos, empleo, educación, salud — incorporados manualmente
A17	LOG-014
B17	CHECKPOINT_v6
C17	múltiple
D17	N/A
E17	pdot_checkpoint_v6.json
F17	pdot_supplement_ckpt.json
G17	2026-05-08
H17	OK
I17	763 indicadores diagnóstico, 56 metas, 145 PAI, 40 riesgos, 48 articulaciones cargados
A18	LOG-015
B18	INMUTABLES_VERIFICADOS
C18	H12_MOTOR_ICPI_CANÓNICO
D18	2
E18	SIAP-ICPI v1.0
F18	—
G18	2026-05-08
H18	OK
I18	B33=B31/B32*100 ✅ | B40=ABS(B38/B32*100-69.9309...) ✅
A19	LOG-016
B19	KB_INGESTA_NORMATIVA_OPERATIVA
C19	H36c_OBSIDIAN_MAP + 08_EJECUCION vault
D19	4 notas nuevas
E19	DOCX Obsidian: POA/PAC/Patronato/PPI GADM 2023-2024
F19	PATRONATO_RDC_2023.docx · POA_2024 · PAC_2023_2024 · PPI_PDOT.docx
G19	2026-05-20
H19	OK
I19	4 notas KB creadas: POA_2023_2024_GADM · PAC_2023_2024_GADM · PATRONATO_Operativo_2023_2024 · PPI_Inversiones_PDOT_2023_2027. Ti Patronato RDC 2023=47.99% marcado autodeclarado (no canónico Gold Master).
A20	LOG-017
B20	KB_ENRIQUECIMIENTO_RDC_ICM
C20	08_EJECUCION vault — RDC_Holding_2023_2024.md + ICM_SIGAD_2023_2024.md
D20	2
E20	DOCX (GAD_Monteristi_RDC_2023/2024 + Reporte_ICM_SIGAD_2023/2024)
F20	2026-05-20
G20	OK
H20	Notas thin enriquecidas con extraccion completa: RDC N17649/N22844 datos deliberacion+obras+ordenanzas; ICM 5metas/.82M→9metas/.94M
I20	SPRINT-2.5B
```