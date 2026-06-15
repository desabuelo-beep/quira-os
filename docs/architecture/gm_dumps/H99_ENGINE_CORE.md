# H99_ENGINE_CORE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=63 · pobladas=55 · fórmulas=107
inputs(lee de): H00_ÍNDICE, H01_PARÁMETROS, H07b_Ti_INVERSIÓN_eSIGEF
outputs(alimenta a): H00_ÍNDICE, H36c_OBSIDIAN_MAP, H73_OUTPUT_API, H97_VALIDACIONES, H98_TGI_FRAMEWORK
MARCADORES: C47: DECIMAL · negativo = falta por subir

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
K7	=IFERROR(ROUND(SUM($H$7:$H$13)*I7/SUM($I$7:$I$13),0),0)
L7	=IFERROR(IF(K7=0,0,ROUND((H7-K7)/K7*100,2)),0)
M7	=Y7
N7	=RANK(Y7,Y$7:Y$13,0)
T7	=H01_PARÁMETROS!$B$180
U7	=H01_PARÁMETROS!$B$15*100
V7	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W7	=J7
X7	=H01_PARÁMETROS!$B$12*100
Y7	=0.2*T7+0.2*U7+0.25*V7+0.25*W7+0.1*X7
Z7	=IF(K7<>"",K7-H7,"")
AA7	=IFERROR(ROUND(E7/100*0.4+(1-F7/100)*0.3+(1-Y7/100)*0.3,4),0)
AB7	=IF(J7>=75,"🟢 Equidad Alta",IF(J7>=50,"🟡 Equidad Moderada",IF(J7>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K8	=IFERROR(ROUND(SUM($H$7:$H$13)*I8/SUM($I$7:$I$13),0),0)
L8	=IFERROR(IF(K8=0,0,ROUND((H8-K8)/K8*100,2)),0)
M8	=Y8
N8	=RANK(Y8,Y$7:Y$13,0)
T8	=H01_PARÁMETROS!$B$180
U8	=H01_PARÁMETROS!$B$15*100
V8	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W8	=J8
X8	=H01_PARÁMETROS!$B$12*100
Y8	=0.2*T8+0.2*U8+0.25*V8+0.25*W8+0.1*X8
Z8	=IF(K8<>"",K8-H8,"")
AA8	=IFERROR(ROUND(E8/100*0.4+(1-F8/100)*0.3+(1-Y8/100)*0.3,4),0)
AB8	=IF(J8>=75,"🟢 Equidad Alta",IF(J8>=50,"🟡 Equidad Moderada",IF(J8>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K9	=IFERROR(ROUND(SUM($H$7:$H$13)*I9/SUM($I$7:$I$13),0),0)
L9	=IFERROR(IF(K9=0,0,ROUND((H9-K9)/K9*100,2)),0)
M9	=Y9
N9	=RANK(Y9,Y$7:Y$13,0)
T9	=H01_PARÁMETROS!$B$180
U9	=H01_PARÁMETROS!$B$15*100
V9	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W9	=J9
X9	=H01_PARÁMETROS!$B$12*100
Y9	=0.2*T9+0.2*U9+0.25*V9+0.25*W9+0.1*X9
Z9	=IF(K9<>"",K9-H9,"")
AA9	=IFERROR(ROUND(E9/100*0.4+(1-F9/100)*0.3+(1-Y9/100)*0.3,4),0)
AB9	=IF(J9>=75,"🟢 Equidad Alta",IF(J9>=50,"🟡 Equidad Moderada",IF(J9>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K10	=IFERROR(ROUND(SUM($H$7:$H$13)*I10/SUM($I$7:$I$13),0),0)
L10	=IFERROR(IF(K10=0,0,ROUND((H10-K10)/K10*100,2)),0)
M10	=Y10
N10	=RANK(Y10,Y$7:Y$13,0)
T10	=H01_PARÁMETROS!$B$180
U10	=H01_PARÁMETROS!$B$15*100
V10	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W10	=J10
X10	=H01_PARÁMETROS!$B$12*100
Y10	=0.2*T10+0.2*U10+0.25*V10+0.25*W10+0.1*X10
Z10	=IF(K10<>"",K10-H10,"")
AA10	=IFERROR(ROUND(E10/100*0.4+(1-F10/100)*0.3+(1-Y10/100)*0.3,4),0)
AB10	=IF(J10>=75,"🟢 Equidad Alta",IF(J10>=50,"🟡 Equidad Moderada",IF(J10>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K11	=IFERROR(ROUND(SUM($H$7:$H$13)*I11/SUM($I$7:$I$13),0),0)
L11	=IFERROR(IF(K11=0,0,ROUND((H11-K11)/K11*100,2)),0)
M11	=Y11
N11	=RANK(Y11,Y$7:Y$13,0)
T11	=H01_PARÁMETROS!$B$180
U11	=H01_PARÁMETROS!$B$15*100
V11	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W11	=J11
X11	=H01_PARÁMETROS!$B$12*100
Y11	=0.2*T11+0.2*U11+0.25*V11+0.25*W11+0.1*X11
Z11	=IF(K11<>"",K11-H11,"")
AA11	=IFERROR(ROUND(E11/100*0.4+(1-F11/100)*0.3+(1-Y11/100)*0.3,4),0)
AB11	=IF(J11>=75,"🟢 Equidad Alta",IF(J11>=50,"🟡 Equidad Moderada",IF(J11>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K12	=IFERROR(ROUND(SUM($H$7:$H$13)*I12/SUM($I$7:$I$13),0),0)
L12	=IFERROR(IF(K12=0,0,ROUND((H12-K12)/K12*100,2)),0)
M12	=Y12
N12	=RANK(Y12,Y$7:Y$13,0)
T12	=H01_PARÁMETROS!$B$180
U12	=H01_PARÁMETROS!$B$15*100
V12	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W12	=J12
X12	=H01_PARÁMETROS!$B$12*100
Y12	=0.2*T12+0.2*U12+0.25*V12+0.25*W12+0.1*X12
Z12	=IF(K12<>"",K12-H12,"")
AA12	=IFERROR(ROUND(E12/100*0.4+(1-F12/100)*0.3+(1-Y12/100)*0.3,4),0)
AB12	=IF(J12>=75,"🟢 Equidad Alta",IF(J12>=50,"🟡 Equidad Moderada",IF(J12>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
K13	=IFERROR(ROUND(SUM($H$7:$H$13)*I13/SUM($I$7:$I$13),0),0)
L13	=IFERROR(IF(K13=0,0,ROUND((H13-K13)/K13*100,2)),0)
M13	=Y13
N13	=RANK(Y13,Y$7:Y$13,0)
T13	=H01_PARÁMETROS!$B$180
U13	=H01_PARÁMETROS!$B$15*100
V13	=H07b_Ti_INVERSIÓN_eSIGEF!$B$18*100
W13	=J13
X13	=H01_PARÁMETROS!$B$12*100
Y13	=0.2*T13+0.2*U13+0.25*V13+0.25*W13+0.1*X13
Z13	=IF(K13<>"",K13-H13,"")
AA13	=IFERROR(ROUND(E13/100*0.4+(1-F13/100)*0.3+(1-Y13/100)*0.3,4),0)
AB13	=IF(J13>=75,"🟢 Equidad Alta",IF(J13>=50,"🟡 Equidad Moderada",IF(J13>=25,"🟠 Inequidad","🔴 Inequidad Crítica")))
B44	=0.2*H01_PARÁMETROS!B180+0.2*H01_PARÁMETROS!B15*100+0.25*H07b_Ti_INVERSIÓN_eSIGEF!B18*100+0.25*MIN(100,AVERAGE(J8:J13))+0.1*H01_PARÁMETROS!B12*100
B45	=SI(B44>=85,"🔵 Excelencia Territorial",SI(B44>=75,"🟢 Gobernanza Inteligente",SI(B44>=65,"🟡 Transición con Riesgos",SI(B44>=50,"🟠 Inequidad Estructural","🔴 Emergencia Territorial"))))
B47	=B46-B44
B48	=INDEX($B$7:$B$13,MATCH(MIN($Y$7:$Y$13),$Y$7:$Y$13,0))
B51	=ROUND(AVERAGE($Y$7:$Y$13),2)
B52	=ROUND(AVERAGE($Y$8:$Y$13),2)
B53	=INDEX($B$7:$B$13,MATCH(MIN($Y$7:$Y$13),$Y$7:$Y$13,0))
B54	=INDEX($B$7:$B$13,MATCH(MAX($Y$7:$Y$13),$Y$7:$Y$13,0))
B55	=ROUND(MIN($Y$7:$Y$13),2)
B56	=ROUND(MAX($Y$7:$Y$13),2)
B57	=IFERROR(ROUND(AVERAGEIF($C$7:$C$13,"Rural",$Y$7:$Y$13),2),0)
B60	=ROUND(SUMIF($C$7:$C$13,"Rural",$Z$7:$Z$13),0)
B61	=INDEX($B$7:$B$13,MATCH(MAX($Z$7:$Z$13),$Z$7:$Z$13,0))
B62	=INDEX($B$8:$B$13,MATCH(MAX($AA$8:$AA$13),$AA$8:$AA$13,0))
B63	=COUNTIF($AB$8:$AB$13,"🔴 Crítica")
```

## ETIQUETAS / DATOS (tope 600)
```
A2	H99 — ENGINE_CORE — Motor Territorial Integrado QUIRA v4.0
A3	IRS · IET · Composite_Need · Brecha Fondos · 7 Parroquias Montecristi
A5	▌ TABLA MAESTRA TERRITORIAL (7 PARROQUIAS)
A6	ID_Parroquia
B6	Nombre
C6	Tipo
D6	Población_2022
E6	NBI_Pct
F6	Cobertura_Agua_Pct
G6	Inv_PerCapita_Q1_2026
H6	Inv_Total_Q1
I6	Composite_Need
J6	IET_Local_Pct
K6	Inv_Ideal_USD
L6	Desviacion_vs_Ideal_Pct
M6	TGI_Score_Parroquia
N6	TGI_Ranking
T6	TGI_D1_Legalidad
U6	TGI_D2_Planificacion
V6	TGI_D3_Ejecucion
W6	TGI_D4_Equidad
X6	TGI_D5_Capacidad
Y6	TGI_Score_5D
Z6	Brecha_Eq_USD
AA6	Prioridad_Reequil
AB6	Clasif_Equidad
A7	P-01
B7	Montecristi
C7	Urbana
D7	39800
E7	38.4
F7	95
G7	217
H7	8636600
I7	0.3215
J7	193.75
A8	P-02
B8	Aníbal San Andrés
C8	Urbana
D8	5200
E8	52.1
F8	67.01
G8	58
H8	301600
I8	0.3744
J8	51.79
A9	P-03
B9	Colorado
C9	Urbana
D9	3800
E9	58.7
F9	38.82
G9	32
H9	121600
I9	0.488
J9	28.57
A10	P-04
B10	Leónidas Proaño
C10	Urbana
D10	4100
E10	54.3
F10	100
G10	48
H10	196800
I10	0.2833
J10	42.86
A11	P-05
B11	Gral. Alfaro
C11	Urbana
D11	6300
E11	49.8
F11	100
G11	71
H11	447300
I11	0.2671
J11	63.39
A12	P-06
B12	Isabel Muentes
C12	Urbana
D12	5700
E12	61.2
F12	1.02
G12	40
H12	228000
I12	0.6193
J12	35.71
A13	P-07
B13	La Pila
C13	Rural
D13	4600
E13	55.9
F13	50
G13	52
H13	239200
I13	0.4427
J13	46.43
A15	▌ MÉTRICAS AGREGADAS — SÍNTESIS TERRITORIAL CANTONAL
A16	IRS_GLOBAL
B16	79.7
C16	DECIMAL
F16	-CORREL(Composite_Need,Inv_PC)x100 · w_NBI=50% w_Agua=30% w_Pop=20% · Tester v2.1
J16	🔴 Muy Regresivo — inversión concentrada en cabecera cantonal
A17	IRS_CLASIFICACION
B17	Muy Regresivo · Composite_Need v2.1
C17	STRING
F17	IRS > 70 = sistema regresivo crítico
J17	Requiere rebalanceo urgente hacia parroquias rurales
A18	IRS_META_2027
B18	45
C18	DECIMAL
F18	Meta PDOT 2027 — reducción a nivel aceptable
J18	Requiere incremento mínimo 80% inversión rural
A19	IET_PERCAPITA_MIN
B19	44.8
C19	DECIMAL
F19	IET_PerCápita peor parroquia / cantonal_avg — QUIRA OS v3.0
J19	Isabel Muentes: $40 / $112 cantonal ≈ 35.7% real; 44.80% ajustado QUIRA OS
A20	COMPOSITE_NEED_LEADER
B20	Isabel Muentes
C20	STRING
F20	Parroquia con Composite_Need más alto del cantón
J20	NBI 61.2% + Agua 1.02% + peso poblacional → necesidad más alta
A21	BRECHA_FONDOS_BLOQUEADA
B21	3660000
C21	DECIMAL
F21	BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K
J21	Fondos bloqueados por ICPI < umbral de elegibilidad
A22	CANTONAL_AVG_INV
B22	112
C22	DECIMAL
F22	Promedio ponderado inversión per cápita Q1-2026
J22	Urbana $217 distorsiona media — rural promedio $50
A23	NBI_PARROQUIAS_PROM
B23	55.7
C23	DECIMAL
F23	Promedio NBI 7 parroquias (1 rural + 6 urbanas) — INEC Censo 2022
J23	Rango: 49.8% (Gral. Alfaro) → 61.2% (Isabel Muentes)
A25	▌ METODOLOGÍA — FÓRMULAS Y FUENTES
A26	IRS_FORMULA
B26	IRS = -CORREL(NBI_pct, Inv_PerCapita) × 100
F26	Índice Regresividad Social. Correlación negativa: NBI alto → inversión baja = sistema regresivo. Rango [0,100]. IRS>70 = Muy Regresivo. Fuente: H99_ENGINE_CORE datos Q1-2026.
A27	COMPOSITE_NEED_FORMULA
B27	CN = 0.45·(NBI/100) + 0.30·(1-Agua/100) + 0.25·(Pob/Σpob)
F27	Necesidad compuesta por parroquia. Pesos: NBI 45% (pobreza estructural), Déficit hídrico 30% (urgencia servicios), Peso poblacional 25% (escala).
A28	IET_LOCAL_FORMULA
B28	IET_Local = (Inv_PerCapita / Cantonal_Avg) × 100
F28	Equidad territorial local. Cantonal_Avg = $112/hab Q1-2026. IET<50% → parroquia con inequidad severa → fondos bloqueados activados.
A29	FONDOS_BLOQUEADOS_EST
B29	FB_est = Pob × (55 - IET_Local)/55 × $500
F29	Estimación bloqueados por parroquia si IET_Local < 55%. $500/hab = proxy costo mínimo proyecto infraestructura rural.
A30	FUENTES_DATOS
B30	INEC Censo 2022 · PDOT Montecristi 2023-2027 · eSIGEF Q1-2026 · H42_IET · H43_MOTOR_TERRITORIAL
F30	NBI: Censo 2022 (INEC). Cobertura agua: PDOT pp.115,316. Inversión: eSIGEF corte 2026-04-30. GPS: Coordinador GAD Montecristi (aprox.). Fondos: H69_ELEGIBILIDAD_FONDOS.
A32	QUIRA OS v4.0 · Dylus Lab © 2026 · GAD Municipal de Montecristi, Ecuador · H99_ENGINE_CORE generado 2026-05-14
A34	▌ ANÁLISIS SENSIBILIDAD IRS · Composite_Need Weights (Tester v2.1)
A35	Escenario
B35	w_Agua_gap (%)
C35	w_NBI (%)
D35	w_Población (%)
E35	IRS_Global
F35	Interpretación
G35	Recomendación
A36	Base Anterior
B36	45
C36	30
D36	25
E36	78.4
F36	Muy Regresivo
G36	Referencia v4.0
A37	Alto énfasis NBI
B37	35
C37	50
D37	15
E37	82.1
F37	Extremadamente Regresivo
G37	Muestra peor realidad
A38	Alto énfasis Agua
B38	60
C38	25
D38	15
E38	76.9
F38	Muy Regresivo
G38	Buen equilibrio
A39	★ Recomendado v2.1
B39	50
C39	30
D39	20
E39	79.7
F39	Muy Regresivo
G39	OFICIAL QUIRA OS v4.1
A40	Bajo énfasis NBI
B40	50
C40	20
D40	30
E40	74.3
F40	Regresivo Fuerte
G40	Subestima problema
A41	Muy bajo NBI
B41	55
C41	15
D41	30
E41	71.8
F41	Regresivo Moderado
G41	Demasiado optimista
A43	▌ TGI — TERRITORIAL GOVERNANCE INTELLIGENCE
A44	TGI_SCORE_CANTONAL_5D
C44	DECIMAL · 0-100
F44	Legalidad(20%) + Planificación(20%) + Ejecución(25%) + Equidad(25%) + Capacidad(10%)
A45	TGI_CLASIFICACION
C45	STRING
A46	TGI_META_2027
B46	60
C46	DECIMAL
F46	Meta: alcanzar nivel Transicion con Riesgos al cierre del PDOT 2027
A47	TGI_BRECHA_A_META
C47	DECIMAL · negativo = falta por subir
A48	TGI_PARROQUIA_CRITICA
C48	STRING · parroquia con menor TGI_Score
F48	La parroquia con menor TGI = mayor urgencia de reequilibrio territorial
A50	▌ TGI 5D — RESÚMENES CANTONALES
A51	TGI_5D_Cantonal_Completo
F51	Promedio TGI_Score_5D 7 parroquias — incluye Montecristi urbana
A52	TGI_5D_Rural_Avg
F52	Promedio TGI_Score_5D 7 parroquias (1 rural + 6 urbanas) (excluye P-01 urbana)
A53	TGI_5D_Parroquia_Critica
F53	Parroquia con menor TGI_Score_5D = máxima urgencia territorial
A54	TGI_5D_Parroquia_Mejor
F54	Parroquia con mayor TGI_Score_5D
A55	TGI_5D_Score_Min
F55	Valor mínimo TGI_Score_5D entre las 7 parroquias
A56	TGI_5D_Score_Max
F56	Valor máximo TGI_Score_5D entre las 7 parroquias
A57	TGI_5D_Rural_AvgIF
F57	AVERAGEIF usando col C (Tipo)=Rural — método más robusto que AVERAGE(Y8:Y13). Equivalente porque las 6 rurales son P-02 a P-07 (filas 8-13).
A59	▌ BRECHAS DE EQUIDAD — REEQUILIBRIO
A60	Brecha_Rural_Total_USD
F60	Déficit acumulado USD parroquias rurales vs media cantonal
A61	Parroquia_Brecha_Max
F61	Parroquia con mayor déficit absoluto en USD
A62	Parroquia_Prioridad_1
F62	Parroquia rural de máxima prioridad de reequilibrio
A63	Parroquias_Criticas_N
F63	Nº parroquias rurales en categoría Crítica (IET<50)
```