# H07_S5_FINANCIERO_eSIGEF — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=88 · pobladas=37 · fórmulas=14
inputs(lee de): H07b_Ti_INVERSIÓN_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H07b_Ti_INVERSIÓN_eSIGEF, H16b_IPE, H16c_PSG_PRESUPUESTO_GENERO, H19_ICS_ISP, H20c_IEF_EFICIENCIA_FINANCIERA, H22_SAT-II, H23_SAT-III, H24_SAT-IV, H26_MMP_TRIMESTRAL, H27_MMP_ANUAL, H33_TAC_QUIRA_CIUDADANA, H42_IET_EQUIDAD_TERRITORIAL, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B18	=B14+B16
B19	=B15+B17
B20	=IF(B18>0,B19/B18,0)
B21	=IF(B20>=0.9,"🔵 Excelencia",IF(B20>=0.7,"🟢 Por Mandato",IF(B20>=0.5,"🟡 En Progreso",IF(B20>=0.25,"🟠 Bajo","🔴 Atención"))))
B23	=IFERROR(B22/12,0.3333)
B25	=H07b_Ti_INVERSIÓN_eSIGEF!B16
B26	=H07b_Ti_INVERSIÓN_eSIGEF!B17
B28	=B20
N46	=IF(A46="","",SUBSTITUTE(SUBSTITUTE(A46,".",""),",","."))
S46	=IF(Q46=0,0,R46/Q46)
T46	=IF(R46>0,1,IF(Q46>0,0.5,0))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H07_S5_FINANCIERO_eSIGEF
A2	H07 — S5 FINANCIERO eSIGEF — EJECUCIÓN PRESUPUESTARIA 2026 (Ti VIVO)
A3	Silo 5: Fuente del Ti (ejecución de inversión). Ti = Devengado_Grupos_7+8 / Codificado_Grupos_7+8. SOLO Grupos 7+8 — excluye Grupo 5 corriente. Alimenta H12 (motor).
A4	★ Este silo alimenta directamente la columna Ti del motor H12. Cuando Ti se actualiza aquí, el ICPI cambia automáticamente. ★
A6	▌ PARÁMETROS S5
A7	Año_eSIGEF
B7	2026
A8	Entidad
B8	GAD Municipal de Montecristi
A9	RUC
B9	0160000390001
A10	Fecha_Corte
B10	Abril 2026 (Ene-Abr)
A11	Fuente
B11	Cédula LOTAIP GAD Montecristi Abr-2026 (Acum Ene-Abr) — CHK-08 update Abril 2026-05-26
A13	▌ RESUMEN Ti POR GRUPOS (2026)
A14	Codificado_Grupo7_Bienes
B14	29654120.37
C14	Cédula LOTAIP GAD Abr-2026 · cuentas 7.x.xx (G7 inversión) · CHK-08 Abril 2026-05-26
A15	Devengado_Grupo7_Bienes
B15	1947738.29
C15	Cédula LOTAIP GAD Abr-2026 · G7 devengado Ene-Abr · CHK-08 Abril 2026-05-26
A16	Codificado_Grupo8_Obras
B16	617691.37
C16	Cédula LOTAIP GAD Abr-2026 · cuentas 8.x.xx (G8 capital) · sin cambio
A17	Devengado_Grupo8_Obras
B17	0
C17	Cédula LOTAIP GAD Abr-2026 · G8 dev=0 (sin ejecución capital Ene-Abr) · CHK-08
A18	Codificado_Total_Inversión_7+8
A19	Devengado_Total_Inversión_7+8
A20	Ti_Global_2026
A21	Clasificación_Ti
A22	Mes_Activo (auto)
B22	4
C22	★ MANUAL: actualizar con el mes de la cédula que se ingesta. Marzo 2026 → 3. Cédula eSIGEF real → usar mes de corte real.
A23	FactorTemporal (mes/12)
A24	Año
B24	Ti_Inversión
C24	Fuente
A25	2023
C25	H36b (ARRASTRE-010) — ★ INMUTABLE
A26	2024
C26	H36b (ARRASTRE-011) — ★ INMUTABLE
A27	2025
B27	[Q4-2026 — actualizar al cierre del ejercicio presupuestario]
C27	H36b en construcción
A28	2026
C28	Año activo — en tiempo real
A30	▌ REGISTRO eSIGEF 2026 — DETALLE POR PARTIDA
A31	Codigo_Partida
B31	Descripcion_Partida
C31	Grupo
D31	Codificado_2026
E31	Devengado_2026
F31	Ti_Partida
G31	ID_Meta_PDOT
H31	V_eSIGEF
A32	[Zona cruda eSIGEF — pegar cédula oficial cuando esté disponible]
A34	ESCALA V_eSIGEF:
B34	1.0 = Devengado > 0 certificado en eSIGEF | 0.5 = Codificado > 0 pero sin devengado | 0.0 = Sin registro presupuestario
A36	⚠️ NOTA CRÍTICA — Formato numérico eSIGEF:
B36	Si la cédula eSIGEF viene en formato europeo (1.234,56): primero reemplazar el punto '.' con nada (eliminar separador de miles), luego reemplazar la coma ',' con punto decimal. Ejemplo: $1.686.370,33 → 1686370.33. Fórmula normalización: =SUSTITUIR(SUSTITUIR(A[n],".",""),",",".")
A40	▌ ARQUITECTURA DE INGESTA PASIVA — H07
A41	Zona Cruda (columnas A–M)
B41	Área de pegado libre. El funcionario pega la cédula eSIGEF exportada (CSV o Excel) con todas sus columnas y formatos originales del gobierno, incluyendo el formato europeo con comas. PROHIBIDO exigir limpieza manual previa.
A42	Zona Inteligente SIAP-ICPI (columnas N–T)
B42	Fórmulas que extraen de la Zona Cruda: Cod_Partida_SIAP, Grupo_SIAP (7 u 8), ID_Meta_PDOT, Codificado_2026, Devengado_2026, Ti_Calculado (=SI(R=0,0,S/R)), V_eSIGEF (=SI(S>0,1.0,0)).
A44	ZONA CRUDA → PEGAR CÉDULA eSIGEF AQUÍ (filas 46+, columnas A–M)
N44	ZONA INTELIGENTE SIAP-ICPI → COLUMNAS N–T
A45	Codigo_Partida
B45	Descripcion
C45	Grupo
D45	Codificado_2026
E45	Devengado_2026
F45	Ti_Partida
G45	Fuente
N45	Cod_Partida_SIAP
O45	Grupo_SIAP
P45	ID_Meta_Enlazado
Q45	Codificado_Extraído
R45	Devengado_Extraído
S45	Ti_Calculado
T45	V_eSIGEF
```