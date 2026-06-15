# H12b_ICPI_ACUMULADO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=23 · pobladas=21 · fórmulas=10
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
D7	=B7/69.9309*100
E7	=IF(B7>=90,"🔵",IF(B7>=70,"🟢",IF(B7>=40,"🟡",IF(B7>=20,"🟠","🔴"))))
F7	=H12_MOTOR_ICPI_CANÓNICO!B31/H12_MOTOR_ICPI_CANÓNICO!B32
B20	=H12_MOTOR_ICPI_CANÓNICO!B38/H12_MOTOR_ICPI_CANÓNICO!B32*100
B21	=H12_MOTOR_ICPI_CANÓNICO!B33
B22	=B20-B21
B23	=IFERROR(AVERAGEIF(B7:B18,">0"),0)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H12b_ICPI_ACUMULADO
A2	H12b — ICPI ACUMULADO (AVANCE MENSUAL HACIA ICPI_ANUAL)
A3	▌ NOTA: Meses históricos = valores congelados (simulación/cédula real). ICPI vivo actual siempre en H12_MOTOR_ICPI_CANÓNICO!B33. Actualizar H07!B14:B17 con nueva cédula eSIGEF para recalcular todo el ecosistema.
A5	▌ CRONOGRAMA MENSUAL DE AVANCE ICPI
A6	Mes
B6	ICPI_Acumulado_%
C6	Variación_Mensual
D6	Avance_vs_Meta_Anual
E6	Estado
F6	Ti_Ponderado_Efectivo
G6	Nota
A7	ENE-2026
B7	4.4654
C7	4.4654
G7	[SIMULACIÓN] Ti_GAD=0.0500 estimado (arranque enero). El valor en col B es simulado. Actualizar con cedula enero 2026.
A8	FEB-2026
B8	11.1130991002
C8	6.647699
D8	15.8915
E8	🟠
F8	0.14
G8	[SIMULACIÓN] Ti_GAD=0.1400 basado en patrón histórico eSIGEF Ecuador. Actualizar con cedula oficial cuando esté disponible.
A9	MAR-2026
B9	18.314734259
C9	7.201635
D9	26.1898
E9	🟠
F9	0.2375
G9	✅ REAL Q1 — cedula eSIGEF verificada
A10	ABR-2026
B10	23.6697963001
C10	5.355062
D10	33.8474
E10	🟡
F10	0.31
G10	[SIMULACIÓN] Ti_GAD=0.3100 basado en patrón histórico eSIGEF Ecuador. Actualizar con cedula oficial cuando esté disponible.
A11	2026-05-01 00:00:00
B11	29.948145
F11	0.395
G11	[PROYECCIÓN] Ti_GAD=0.3950 proyección lineal histórica
A12	2026-06-01 00:00:00
B12	35.11855
F12	0.465
G12	[PROYECCIÓN] Ti_GAD=0.4650 proyección lineal histórica
A13	2026-07-01 00:00:00
B13	41.027584
F13	0.545
G13	[PROYECCIÓN] Ti_GAD=0.5450 proyección lineal histórica
A14	AGO-2026
B14	46.936618
F14	0.625
G14	[PROYECCIÓN] Ti_GAD=0.6250 proyección lineal histórica
A15	2026-09-01 00:00:00
B15	52.476337
F15	0.7
G15	[PROYECCIÓN] Ti_GAD=0.7000 proyección lineal histórica
A16	2026-10-01 00:00:00
B16	56.908112
F16	0.76
G16	[PROYECCIÓN] Ti_GAD=0.7600 proyección lineal histórica
A17	2026-11-01 00:00:00
B17	62.078517
F17	0.83
G17	[PROYECCIÓN] Ti_GAD=0.8300 proyección lineal histórica
A18	DIC-2026
B18	65.771663
F18	0.88
G18	[PROYECCIÓN] Ti_GAD=0.8800 proyección lineal histórica
A20	ICPI_ANUAL_META
G20	Meta ICPI_2026 ≥ ICPI_Real_2025 = 69.9309% (referencia histórica)
A21	ICPI_ACTUAL
A22	Brecha_Faltante
A23	Promedio_ICPI_Mensual_No0
```