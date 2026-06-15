# H97_VALIDACIONES — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=27 · pobladas=25 · fórmulas=17
inputs(lee de): H01_PARÁMETROS, H07b_Ti_INVERSIÓN_eSIGEF, H99_ENGINE_CORE
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
C5	=IF(COUNTIF(H99_ENGINE_CORE!$D$7:$D$13,">0")=7,"✅ Cumple","🔴 Faltan datos de población")
C6	=IF(AND(H01_PARÁMETROS!$B$15>0,H01_PARÁMETROS!$B$15<1),"✅ Cumple","🔴 ICPI fuera de rango")
C7	=IF(AND(H01_PARÁMETROS!$B$180>0,H01_PARÁMETROS!$B$180<=100),"✅ Cumple","🔴 Trust Score inválido")
C8	=IF(AND(H07b_Ti_INVERSIÓN_eSIGEF!$B$18>0,H07b_Ti_INVERSIÓN_eSIGEF!$B$18<=1),"✅ Cumple","🔴 Ti fuera de rango")
C9	=IF(AND(H99_ENGINE_CORE!$B$16>=0,H99_ENGINE_CORE!$B$16<=100),"✅ Cumple","🔴 IRS fuera de rango")
C10	=IF(ABS(H01_PARÁMETROS!$B$261+H01_PARÁMETROS!$B$265+H01_PARÁMETROS!$B$269+H01_PARÁMETROS!$B$273+H01_PARÁMETROS!$B$277-1)<0.001,"✅ Cumple","🔴 Pesos TGI no suman 100%")
C11	=IF(COUNTIF(H99_ENGINE_CORE!$E$7:$E$13,">0")=7,"✅ Cumple","⚠️ Alguna parroquia sin NBI")
C12	=IF(H99_ENGINE_CORE!$J$7>AVERAGE(H99_ENGINE_CORE!$J$8:$J$13),"✅ Regresividad confirmada","⚠️ Revisar IRS/IET")
C13	=IF(H99_ENGINE_CORE!$I$12=MAX(H99_ENGINE_CORE!$I$7:$I$13),"✅ Consistente","⚠️ Revisar CN — Isabel Muentes no es la más necesitada")
C14	=IF(COUNTIF(H99_ENGINE_CORE!$Y$7:$Y$13,"<50")=0,"✅ Ninguna en emergencia",COUNTIF(H99_ENGINE_CORE!$Y$7:$Y$13,"<50")&" parroquia(s) en Emergencia Territorial (<50)")
C15	=IF(H99_ENGINE_CORE!$B$52>=60,"✅ Meta alcanzada","⚠️ TGI rural avg de "&H99_ENGINE_CORE!$B$52&" — meta: 60")
C17	=IF(COUNTIF(H99_ENGINE_CORE!$G$7:$G$13,"<0")=0,"OK Cumple — sin valores negativos","FALLA "&COUNTIF(H99_ENGINE_CORE!$G$7:$G$13,"<0")&" parroquia(s) con Inv_PerCap < 0")
C18	=IF(COUNTIF(H99_ENGINE_CORE!$J$8:$J$13,">=100")=0,"OK Cumple - todas rurales IET<100","ALERTA "&COUNTIF(H99_ENGINE_CORE!$J$8:$J$13,">=100")&" rural(es) con IET>=100 - revisar")
C19	=IF(SUM(H99_ENGINE_CORE!$Z$8:$Z$13)>0,"OK Brecha rural = $"&TEXT(SUM(H99_ENGINE_CORE!$Z$8:$Z$13),"#,##0")&" — subinversion confirmada","FALLA Brecha negativa — revisar inversion parroquias rurales")
C20	=IF(H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100<75,"ALERTA CRITICA D3="&TEXT(H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100,"0.0")&"% — umbral optimo >=75%","OK D3="&TEXT(H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100,"0.0")&"% — umbral alcanzado")
C21	=IF(H99_ENGINE_CORE!$F$12<5,"ALERTA CRITICA Agua Isabel Muentes="&H99_ENGINE_CORE!$F$12&"% — PRIORIDAD MAXIMA","INFO Agua Isabel Muentes="&H99_ENGINE_CORE!$F$12&"% — revisar si supero el 5%")
C22	=IF(H99_ENGINE_CORE!$AA$12=MAX(H99_ENGINE_CORE!$AA$7:$AA$13),"OK Isabel Muentes prioridad maxima confirmada (Score: "&TEXT(H99_ENGINE_CORE!$AA$12,"0.000")&")","ALERTA Revisar — Isabel Muentes no es la parroquia de mayor prioridad")
```

## ETIQUETAS / DATOS (tope 600)
```
A1	H97 — VALIDACIONES Y AUDITORÍA INTERNA — SIAP-ICPI v5.4 TGI — GADM Montecristi 2026
A2	Hoja de auditoría interna. Cada regla usa fórmulas Excel vivas: ✅ Cumple · ⚠️ Alerta · 🔴 Falla. Actualizar la celda Responsable y Fecha después de cada revisión.
A4	ID
B4	Regla
C4	Resultado
D4	Evidencia (Hoja!Celda)
E4	Observación
F4	Responsable
G4	Fecha
A5	V-01
B5	¿Las 7 parroquias tienen población registrada?
D5	H99_ENGINE_CORE!D7:D13
E5	Columna D (Población_2022) debe ser >0 para las 7 parroquias
F5	Javo Delgado / Dylus Lab
G5	2026-05-16
A6	V-02
B6	¿ICPI_Real_2025 está en rango válido (0-1)?
D6	H01_PARÁMETROS!B15
E6	ICPI decimal debe estar entre 0 y 1. Valor actual: 0.6993
F6	Javo Delgado / Dylus Lab
G6	2026-05-16
A7	V-03
B7	¿Trust_Score_Metodológico está en rango válido (0-100)?
D7	H01_PARÁMETROS!B180
E7	Trust_Score en % — debe estar entre 0 y 100. Valor actual: 83.5
F7	Javo Delgado / Dylus Lab
G7	2026-05-16
A8	V-04
B8	¿Ti_Inversión_2025 ENTE-01 está en rango válido (0-1)?
D8	H07b_Ti_INVERSIÓN_eSIGEF!B18
E8	Ti es ratio decimal devengado/codificado. Valor actual: 0.5985
F8	Javo Delgado / Dylus Lab
G8	2026-05-16
A9	V-05
B9	¿IRS_Global está en rango esperado (0-100)?
D9	H99_ENGINE_CORE!B16
E9	IRS = índice de regresión territorial. Valor actual: 79.7 (Muy Regresivo)
F9	Javo Delgado / Dylus Lab
G9	2026-05-16
A10	V-06
B10	¿Suma de pesos TGI = 100%?
D10	H01_PARÁMETROS!B261+B265+B269+B273+B277
E10	D1(20%)+D2(20%)+D3(25%)+D4(25%)+D5(10%) = 100%. CRÍTICO para validez del score
F10	Javo Delgado / Dylus Lab
G10	2026-05-16
A11	V-07
B11	¿Todas las parroquias tienen NBI registrado?
D11	H99_ENGINE_CORE!E7:E13
E11	NBI_Pct necesario para Composite_Need y dimensión D4
F11	Javo Delgado / Dylus Lab
G11	2026-05-16
A12	V-08
B12	¿Montecristi urbana tiene IET mayor que promedio rural? (confirma regresividad)
D12	H99_ENGINE_CORE!J7 vs J8:J13
E12	P-01 Montecristi urbana debe tener IET > promedio rural. IET P-01: 193.75
F12	Javo Delgado / Dylus Lab
G12	2026-05-16
A13	V-09
B13	¿Isabel Muentes tiene el mayor Composite_Need del cantón?
D13	H99_ENGINE_CORE!I12 vs MAX(I7:I13)
E13	Isabel Muentes (P-06) debe tener CN máximo por NBI=61.2% y agua=1.02%. CN: 0.6193
F13	Javo Delgado / Dylus Lab
G13	2026-05-16
A14	V-10
B14	¿Ninguna parroquia en Emergencia Territorial TGI (<50)?
D14	H99_ENGINE_CORE!Y7:Y13
E14	Umbral emergencia TGI_5D < 50. Parroquias más críticas: Colorado 62.8, Isabel Muentes 64.6
F14	Javo Delgado / Dylus Lab
G14	2026-05-16
A15	V-11
B15	¿TGI_5D rural promedio ≥ 60 (meta 2027)?
D15	H99_ENGINE_CORE!B52
E15	Meta 2027: TGI rural ≥ 60 (Transición con Riesgos). Actual estimado: 66.85 ✅
F15	Javo Delgado / Dylus Lab
G15	2026-05-16
A16	— NUEVAS REGLAS v5.4 — INVERSIÓN · EQUIDAD · EJECUCIÓN · VALIDACIÓN MANUAL —
A17	V-12
B17	¿Hay inversiones per cápita negativas en alguna parroquia?
D17	H99_ENGINE_CORE!G7:G13
E17	Inv_PerCapita_Q1_2026 < 0 es error de datos. En inversion publica no existen valores negativos.
F17	Javo Delgado / Dylus Lab
G17	2026-05-16
A18	V-13
B18	Todas las parroquias rurales tienen IET < 100? (confirma regresividad)
D18	H99_ENGINE_CORE!J8:J13
E18	Rurales deben tener IET < 100 en GAD regresivo (IRS=79.7). Si alguna rural >= 100, revisar datos de inversion territorial.
F18	Javo Delgado / Dylus Lab
G18	2026-05-16
A19	V-14
B19	¿Brecha de equidad rural acumulada es positiva (> $0)?
D19	H99_ENGINE_CORE!Z8:Z13
E19	Brecha_Eq_USD positiva = parroquia subinvertida vs media cantonal. Total rural esperado: +$1,791,935.
F19	Javo Delgado / Dylus Lab
G19	2026-05-16
A20	V-15
B20	¿D3 Ejecucion presupuestaria esta por debajo del umbral critico 75%?
D20	H07b_Ti_INVERSIÓN_eSIGEF!B18
E20	Ti*100 = D3 Ejecucion. Umbral optimo >=75%. Actual: 59.85% = CATEGORIA EN RIESGO segun Tabla 200 PDOT.
F20	Javo Delgado / Dylus Lab
G20	2026-05-16
A21	V-16
B21	¿Cobertura de agua en Isabel Muentes (P-06) es critica (< 5%)?
D21	H99_ENGINE_CORE!F12
E21	Isabel Muentes (P-06, row 12): Cobertura_Agua_Pct. Valor esperado: 1.02%. NBI=61.2% — parroquia mas critica.
F21	Javo Delgado / Dylus Lab
G21	2026-05-16
A22	V-17
B22	¿Prioridad_Reequil de Isabel Muentes es la mas alta del canton?
D22	H99_ENGINE_CORE!AA12 vs MAX(AA7:AA13)
E22	Prioridad_Reequil: NBI*0.4 + (1-Agua)*0.3 + (1-TGI/100)*0.3. Isabel Muentes esperado: 0.648 (max).
F22	Javo Delgado / Dylus Lab
G22	2026-05-16
A23	V-18
B23	¿Metas sin presupuesto? (verificacion manual PDOT_KB)
C23	"MANUAL Ver PDOT_MONTECRISTI_KB.xlsx"
D23	PDOT_MONTECRISTI_KB.xlsx — columnas Meta/Presupuesto
E23	Verificar manualmente que cada meta del POA tiene presupuesto asignado. No automatizable desde Gold Master.
F23	Javo Delgado / Dylus Lab
G23	2026-05-16
A24	V-19
B24	¿Programas sin responsable institucional? (verificacion manual PDOT_KB)
C24	"MANUAL Ver propuesta_tgi/ en Obsidian KB"
D24	QUIRA_KB_Montecristi/01_PDOT/propuesta_tgi/
E24	Verificar que cada programa curado tiene unidad responsable en frontmatter. 10 programas curados Fase 2A.
F24	Javo Delgado / Dylus Lab
G24	2026-05-16
A26	▌ NOTA DE CORRECCIONES — Fórmulas propuestas externamente vs implementación real
A27	CORRECCIÓN 1 — T (D1_Legalidad): La propuesta sugería H01!B180*100, pero B180=83.5 YA está en porcentaje → multiplicar por 100 daría 8350 (error grave). Fórmula correcta: H01!B180 directo.
CORRECCIÓN 2 — W (D4_Equidad): La propuesta sugería =M (TGI_Score_Parroquia composite), pero M es un score derivado, NO IET_Local. Fórmula correcta: =MIN(100,J) donde J=IET_Local_Pct.
```