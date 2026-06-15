# H75_SAT_ENGINE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=14 · pobladas=14 · fórmulas=34
inputs(lee de): H00_ÍNDICE, H21_SAT-I, H21b_SAT-0_COHERENCIA_PAC, H22_SAT-II, H23_SAT-III, H24_SAT-IV, H24b_SAT-V_ALERTA_CPCCS, H24c_SAT-VI_DESVÍO_PP, H25_MMP_MENSUAL, H42_IET_EQUIDAD_TERRITORIAL
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API, SAT_Catalogo
MARCADORES: D9: =IFERROR(H25_MMP_MENSUAL!W38,"No disponible") · D10: =IFERROR(IF((1-H42_IET_EQUIDAD_TERRITORIAL!B8)>0.2,"⚠️ TERRITORIAL_INE

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
D2	='H21b_SAT-0_COHERENCIA_PAC'!B19
E2	=IF(ISNUMBER(SEARCH("✅",D2)),"INACTIVO","ACTIVO")
G2	=F2*IF(E2="ACTIVO",1,0)
D3	='H21_SAT-I'!B15
E3	=IF(ISNUMBER(SEARCH("✅",D3)),"INACTIVO","ACTIVO")
G3	=F3*IF(E3="ACTIVO",1,0)
D4	='H22_SAT-II'!B12
E4	=IF(ISNUMBER(SEARCH("✅",D4)),"INACTIVO","ACTIVO")
G4	=F4*IF(E4="ACTIVO",1,0)
D5	='H23_SAT-III'!B13
E5	=IF(ISNUMBER(SEARCH("✅",D5)),"INACTIVO","ACTIVO")
G5	=F5*IF(E5="ACTIVO",1,0)
D6	='H24_SAT-IV'!B13
E6	=IF(ISNUMBER(SEARCH("✅",D6)),"INACTIVO","ACTIVO")
G6	=F6*IF(E6="ACTIVO",1,0)
D7	='H24b_SAT-V_ALERTA_CPCCS'!B17
E7	=IF(ISNUMBER(SEARCH("✅",D7)),"INACTIVO","ACTIVO")
G7	=F7*IF(E7="ACTIVO",1,0)
D8	='H24c_SAT-VI_DESVÍO_PP'!B14
E8	=IF(ISNUMBER(SEARCH("✅",D8)),"INACTIVO","ACTIVO")
G8	=F8*IF(E8="ACTIVO",1,0)
D9	=IFERROR(H25_MMP_MENSUAL!W38,"No disponible")
E9	=IF(IFERROR(H25_MMP_MENSUAL!W38,1)<0.85,"ACTIVO","INACTIVO")
G9	=F9*IF(E9="ACTIVO",1,0)
D10	=IFERROR(IF((1-H42_IET_EQUIDAD_TERRITORIAL!B8)>0.2,"⚠️ TERRITORIAL_INEQUITY — desviación >"&TEXT((1-H42_IET_EQUIDAD_TERRITORIAL!B8),"0.0%"),"✅ Equidad territorial OK — desviación "&TEXT((1-H42_IET_EQUIDAD_TERRITORIAL!B8),"0.0%")),"No disponible")
E10	=IF(IFERROR((1-H42_IET_EQUIDAD_TERRITORIAL!B8),0)>0.2,"ACTIVO","INACTIVO")
G10	=F10*IF(E10="ACTIVO",1,0)
B11	=IF(B12>0.5,"CRITICO",IF(B12>0.3,"ALTO",IF(B12>0.15,"MEDIO","BAJO")))
B12	=SUM(G2:G10)
F12	=SUM(F2:F10)
G12	=B12
B13	=IF(B12>0.5,"CRITICO",IF(B12>0.3,"ALTO",IF(B12>0.15,"MEDIO","BAJO")))
B14	=COUNTIF(E2:E10,"ACTIVO")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	NOMBRE_ALERTA
C1	CONDICION_DESCRIPCION
D1	EVALUACION_RAW
E1	ESTADO
F1	PESO_SEVERIDAD
G1	CONTRIBUCION_RIESGO
A2	SAT-0
B2	Coherencia POA-PAC
C2	POA y PAC desalineados — contrataciones fuera del plan operativo
F2	0.2
A3	SAT-I
B3	Fragmentacion Selectiva
C3	Reformas presupuestarias > 5% del codificado base (monto, no fecha). H22 no verifica temporalidad Q2.
F3	0.25
A4	SAT-II
B4	Reforma Significativa Tardía
C4	Metas reformadas despues de Q2 — señal de planificacion reactiva
F4	0.15
A5	SAT-III
B5	Paralisis Presupuestaria
C5	Metas con rezago presupuestario critico — Ti < umbral en Q3/Q4
F5	0.2
A6	SAT-IV
B6	Alerta Fiscal COOTAD
C6	Inversion < 65% del presupuesto — incumplimiento Art.192 COOTAD
F6	0.1
A7	SAT-V
B7	Brecha Compromiso CPCCS
C7	Brecha de compromisos CPCCS > 30% (1 - Cumplidos/Total). No mide diferencial ICPI vs Vi_CPCCS.
F7	0.05
A8	SAT-VI
B8	Desvio Presupuesto Participativo
C8	PP registrado vs ejecutado > 20% desviacion — señal de desvio PP
F8	0.05
A9	SAT-VII
B9	Vi_Sináptico_Pulso
C9	Vi promedio de 25 metas < 0.85 — brecha entre avance real y plan mensual
F9	0
A10	SAT-VIII
B10	Equidad_Territorial
C10	Desviación IET > 20% — inversión urbana vs rural desequilibrada
F10	0
A11	---
C11	BAJO<0.15 | MEDIO<0.30 | ALTO<0.50 | CRITICO>=0.50
A12	RIESGO_TOTAL
C12	Riesgo ponderado 0.0-1.0 (SAT-VII y SAT-VIII informacionales con peso 0)
A13	CLASIF_RIESGO
C13	BAJO<0.15 | MEDIO<0.30 | ALTO<0.50 | CRITICO>=0.50
A14	SAT_ACTIVAS_COUNT
C14	Número de alertas SAT activas (incluyendo SAT-VII y SAT-VIII)
```