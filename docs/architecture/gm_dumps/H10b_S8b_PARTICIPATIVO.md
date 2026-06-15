# H10b_S8b_PARTICIPATIVO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=203 · pobladas=40 · fórmulas=13
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H20b_IGP_GOBERNANZA_PARTIC, H73_OUTPUT_API, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE
MARCADORES: G13: Fichas verificadas: 126 (1ra prioridad) - Monto pendiente resolucion G · F24: 20982884 (base provisional ingresos — resolución GADM pendiente) · G24: ACTA No.007-2025-JLAC-JPC-GADMCM · VERIFICADO CHK-12 2026-05-26 — Info · G201: =IF(D201=0,"Sin montos PP 2026 - fichas verificadas: 149 - pendiente r

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B13
F13	=IF(D13=0,0,E13/D13)
F14	=IF(D14=0,0,E14/D14)
F15	=IF(D15=0,0,E15/D15)
F16	=IF(D16=0,0,E16/D16)
F17	=IF(D17=0,0,E17/D17)
D201	=SUM(D13:D200)
E201	=SUM(E13:E200)
F201	=IF(D201=0,0,E201/D201)
G201	=IF(D201=0,"Sin montos PP 2026 - fichas verificadas: 149 - pendiente resolucion GADM",IF(F201<0.8,"SAT-VI ACTIVO - Ejecucion PP < 80%","SAT-VI: Ejecucion PP aceptable"))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H10b_S8b_PARTICIPATIVO
A2	H10b — S8b PRESUPUESTO PARTICIPATIVO — CONTROL DEMOCRÁTICO 2026
A3	Silo 8b: Seguimiento al Presupuesto Participativo. Alimenta SAT-VI (Desvío PP) y el BONO_PARTICIPACION (H01!B40).
A5	PARAMETROS PP - SERIE 2024-2026 (DATOS VERIFICADOS)
A6	Año
A7	BONO_PARTICIPACION
B7	SI
A8	Marco_Legal
B8	COOTAD Art.238 / LOPC Art.93
A9	Ingresos_Base_2026
B9	20982884
A10	Fichas_PP_2026
B10	149
A11	REGISTRO PP 2026 - PRIORIDADES VERIFICADAS (ACTA No.007-2025-JLAC-JPC-GADMCM)
A12	ID_Proyecto_PP
B12	Descripción
C12	ID_Meta_PDOT
D12	Monto_Aprobado_PP
E12	Monto_Ejecutado
F12	Cumplimiento_PP_%
G12	Alerta_SAT_VI
A13	PP-GAD-2026-P01
B13	Agua Potable / Saneamiento rural
C13	AH-AP-01
D13	0
E13	0
G13	Fichas verificadas: 126 (1ra prioridad) - Monto pendiente resolucion GADM
A14	PP-GAD-2026-P02
B14	Areas verdes / Parques / Recreacion
C14	FA-C-X-01
D14	0
E14	0
G14	Fichas verificadas: 95 (2da prioridad)
A15	PP-GAD-2026-P03
B15	Vialidad cantonal / Red interna
C15	AH-V-X-01
D15	0
E15	0
G15	Fichas verificadas: 94 (3ra prioridad)
A16	PP-GAD-2026-P04
B16	Salud / Equipamiento medico parroquial
C16	SC-S-G-01
D16	0
E16	0
G16	Fichas verificadas: 80 (4ta prioridad)
A17	PP-GAD-2026-P05
B17	Aseo / Recoleccion / Gestion ambiental
C17	FA-R-X-01
D17	0
E17	0
G17	Fichas verificadas: 74 (5ta prioridad)
A20	SERIE HISTORICA PP - VERIFICADA (FUENTES OFICIALES GAD MONTECRISTI)
A21	Año PP
B21	Metodo proceso
C21	Talleres
D21	Fichas
E21	Parroquias
F21	Presupuesto PP (USD)
G21	ACTA / Fuente
A22	PP 2024
B22	Formulario online (Google Forms) - convocatoria publica GAD web
C22	N/A (online)
D22	N/A (online)
E22	7
F22	6118924
G22	ACTA No.002-2023-JLAC-JPC-GADMCM - INFORME No.003-JLAC-JPC-GADCM-2023
A23	PP 2025
B23	6 talleres presenciales - 7 parroquias - 6 mesas de trabajo
C23	6
D23	137
E23	7
F23	5687954
G23	ACTA No.005-2024-JLAC-JPC-GADMCM - MEMORANDO No.255 (30-oct-2024)
A24	PP 2026
B24	6 talleres presenciales - 7 parroquias - 6 mesas de trabajo
C24	6
D24	149
E24	7
F24	20982884 (base provisional ingresos — resolución GADM pendiente)
G24	ACTA No.007-2025-JLAC-JPC-GADMCM · VERIFICADO CHK-12 2026-05-26 — Informe PP 2026 PDF 153 pág. · 6 talleres Ago 6-8-2025 · Mesa final Ago 15 2025 · Montos pendientes resolución presupuestaria GADM
A26	Tendencia fichas:
B26	PP2025: 137 fichas -> PP2026: 149 fichas (+8.8%) - Cobertura: 7/7 parroquias en todos los ciclos (COOTAD Art.238 cumplido)
A27	Ingresos base:
B27	PP2025: $21,606,774 (propios 56.4% + transferencias 43.6%) - PP2026: $20,982,884 estimado provisional
A28	CHK-12_SENTINEL
B28	CHK-12 COMPLETADO 2026-05-26 · PDF INFORME PP 2026 verificado · Proceso PP 2026 COMPLETO (6 talleres + ACTA-007) · 149 fichas = +8.8% vs PP2025 · Ingresos base 0,982,884 · MMP_AVANCE_PCT activado en H73!B61
A29	COMPONENTES PRESUPUESTO PP 2025 - VERIFICADO (Fuente: PDF p.116)
A30	Componente
B30	Monto USD
C30	%
D30	Area tematica
A31	Fisico Ambiental
B31	1249758
C31	22%
D31	Ambiente, ecosistemas
A32	Territorial AAHH
B32	1886695
C32	33%
D32	Agua, alcantarillado, vialidad
A33	Social Cultural
B33	1331666
C33	23%
D33	Educacion, salud, deporte
A34	Economico Productivo
B34	603279
C34	11%
D34	Produccion, comercio
A35	Politico Institucional
B35	616554
C35	11%
D35	Gestion, participacion
A38	COMPONENTES PRESUPUESTO PP 2024 - VERIFICADO (Fuente: PDF p.3)
A39	Componente
B39	Monto USD
C39	%
D39	Area tematica
A40	Biofsico
B40	161920
C40	3%
D40	Medio ambiente
A41	Economico Productivo
B41	60760
C41	1%
D41	Produccion
A42	Sociocultural
B42	468750
C42	8%
D42	Educacion, salud, cultura
A43	Asentamientos Humanos
B43	3220532
C43	53%
D43	Infraestructura territorial
A44	Politico Institucional
B44	2206962
C44	36%
D44	Gestion institucional
A201	TOTAL PP 2026
B201	—
C201	—
A203	NOTA SAT-VI:
B203	El SAT-VI (Desvío PP) se activa cuando el Cumplimiento_PP_% cae por debajo del umbral definido en H01. El BONO_PARTICIPACION se aplica en H14 cuando la participación ciudadana en el PP cumple criterios. Las filas 13-200 están disponibles para registrar proyectos individuales del PP 2026.
```