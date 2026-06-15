# H19_ICS_ISP — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=14 · pobladas=12 · fórmulas=10
inputs(lee de): H01_PARÁMETROS, H05_S3_OPERATIVO_POA, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=IFERROR(IF(ISNUMBER(B12),IF(B12>0,B12,0.584),0.584),0.584)
B7	=IF(B6>=0.9,"🔵 Salud Presupuestaria Excelente",IF(B6>=0.7,"🟢 Salud Presupuestaria por Mandato",IF(B6>=0.4,"🟡 Transición Crítica",IF(B6>=0.2,"🟠 Salud Presupuestaria Parcial","🔴 Atención Alta — Plan de mejora"))))
B8	=H07_S5_FINANCIERO_eSIGEF!B20
B9	=H07_S5_FINANCIERO_eSIGEF!B20
B10	=H01_PARÁMETROS!B33
B11	=IF(B9<B10,"⚠️ Inversión por debajo del umbral mínimo COOTAD — Revisar estructura de gasto","✅ Estructura de inversión dentro de parámetros")
B12	=IFERROR((B8+IFERROR(SUM(H05_S3_OPERATIVO_POA!D14:D38)/IFERROR(SUM(H07_S5_FINANCIERO_eSIGEF!D30:D200),1),0))/2,B6)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H19_ICS_ISP
A2	H19 — ISP — ÍNDICE DE SALUD PRESUPUESTARIA
A3	Mide la coherencia entre presupuesto codificado, devengado y metas programadas.
A5	▌ PANEL ISP
A6	ISP_Global_2025_Ref
C6	58.40% — Transición Crítica
A7	Clasificación_ISP
A8	Ti_Inversión_2026
C8	Vivo 2026 desde H07
A9	Pct_Inversion_Real
A10	Umbral_Inversion_Min_COOTAD
C10	65% mínimo COOTAD Art.192
A11	Alerta_SAT_IV
A12	ISP_2026_Real_eSIGEF
C12	Ti_Inversión 2026 Q1 real desde H07_eSIGEF · Datos 2023-2025 históricos inmutables
A14	▌ NOTA SAT-IV
B14	SAT = Sistema de Alertas Tempranas. SAT-IV activa cuando Ti_Inversión < Umbral COOTAD. El analista debe verificar mensualmente que el devengado Grupos 7+8 en eSIGEF mantiene el mínimo constitucional.
```