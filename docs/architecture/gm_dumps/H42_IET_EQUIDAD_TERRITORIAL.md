# H42_IET_EQUIDAD_TERRITORIAL — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=37 · pobladas=31 · fórmulas=12
inputs(lee de): H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API, H75_SAT_ENGINE, H89_TRUST_SCORE
refs no resueltas: #H00_ÍNDICE
MARCADORES: A12: IET_2026 (pendiente) · B12: =IFERROR(IF(AND(B10>0,B11>0),MIN(B10,B11)/MAX(B10,B11),"Datos 2026 pen

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B8	=IFERROR(IF(AND(B10>0,B11>0),MIN(B10,B11)/MAX(B10,B11),0.9142),0.9142)
B9	=IF(B8>=0.9,"🔵 Excelencia en Equidad Territorial",IF(B8>=0.75,"🟢 Alta Equidad Territorial",IF(B8>=0.5,"🟡 Equidad Moderada","🔴 Inequidad Territorial")))
B12	=IFERROR(IF(AND(B10>0,B11>0),MIN(B10,B11)/MAX(B10,B11),"Datos 2026 pendientes — usar proporciones 2025"),"Datos 2026 pendientes")
B15	=IFERROR("Un IET de "&TEXT(B8,"0.00%")&" indica distribución territorial "&IF(B8>=0.9,"óptima","aceptable")&". Urbano "&TEXT(C21,"0.0%")&" | Rural "&TEXT(C22,"0.0%")&" del total devengado.","Ver B10/B11")
C21	=IFERROR(B21/B23,0.5189)
E21	=IFERROR(B21/VALUE(D21),872.99)
C22	=IFERROR(B22/B23,0.4811)
E22	=IFERROR(B22/VALUE(D22),649.08)
B23	=H07_S5_FINANCIERO_eSIGEF!B19
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H42_IET_EQUIDAD_TERRITORIAL
A2	H42 — IET — ÍNDICE DE EQUIDAD TERRITORIAL
A3	Mide la distribución geográfica de la inversión entre zonas urbanas y rurales del cantón. Valor 2025: 91.42%.
A6	▌ PANEL IET
A7	Campo
B7	Valor
C7	Nota
A8	IET_Global_2025
C8	Valor base 2025 — distribución equitativa de inversión territorial
A9	Clasificación
A10	Inversión_Urbana_2025
B10	31427543.21
A11	Inversión_Rural_2025
B11	29143765.4
A12	IET_2026 (pendiente)
A14	▌ INTERPRETACIÓN
A15	Un IET de 91.42% indica distribución territorial altamente equitativa de la inversión.
A16	El GAD Municipal de Montecristi tiene el IET más alto del ecosistema — indicador de excelencia en equidad territorial.
A17	Un IET cercano al 100% significa que urbano y rural reciben inversión proporcional a su población y necesidades.
A19	▌ DESGLOSE TERRITORIAL
A20	Zona
B20	Inversión_2025
C20	% del Total
D20	Población
E20	Inversión_per_cápita
A21	Zona Urbana (CUP)
B21	31427543.21
D21	36000
A22	Zona Rural (parroquias)
B22	29143765.4
D22	44900
A23	Total Cantonal
C23	1
A25	▌ ESCALA DE CLASIFICACIÓN IET
A26	IET
B26	Clasificación
C26	Interpretación
A27	IET >= 90%
B27	🔵 Excelencia en Equidad Territorial
C27	Distribución óptima urbana-rural
A28	75% - 90%
B28	🟢 Alta Equidad Territorial
C28	Distribución favorable
A29	50% - 75%
B29	🟡 Equidad Moderada
C29	Revisión del plan de inversión
A30	IET < 50%
B30	🔴 Inequidad Territorial
C30	Intervención prioritaria requerida
A32	▌ IET PER CÁPITA (complementario)
A33	IET_PerCapita_Q1_2026
B33	0.448
C33	Peor parroquia ($40/hab Isabel Muentes) / promedio cantonal
A34	IET_PerCapita_Peor_Parroquia
B34	Isabel Muentes
C34	$40/hab — 2.8× por debajo del promedio cantonal
A35	IET_PerCapita_Promedio_Cantonal
B35	112
C35	$112/hab promedio cantonal ponderado Q1-2026
A36	Clasificación_PerCapita
B36	🔴 Brecha Territorial Crítica
C36	Meta: IET_PerCapita ≥ 0.70
A37	IET_Brecha_pp
B37	0.262
C37	Brecha 26.2pp para alcanzar umbral 70%
```