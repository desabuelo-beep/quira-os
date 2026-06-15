# H24_SAT-IV — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=20 · pobladas=15 · fórmulas=10
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE, H01
MARCADORES: B13: =IF(B6="NO","⚫ SAT-IV en espera (reforma COOTAD pendiente evaluación)"

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B40
B7	=H01_PARÁMETROS!B38
B8	=H01_PARÁMETROS!B39
B9	=IFERROR(H07_S5_FINANCIERO_eSIGEF!B20,0)
B10	=IF(1-B9<B7,"⚠️ Inversión por debajo del umbral mínimo COOTAD","✅ Estructura fiscal conforme")
B13	=IF(B6="NO","⚫ SAT-IV en espera (reforma COOTAD pendiente evaluación)",IF(LEFT(B10,2)="⚠️","⚠️ SAT-IV ACTIVO — Revisar estructura de gasto GAD con Dirección Financiera","✅ Sin señal SAT-IV"))
B17	=IF(B6="NO","SAT-IV en modo espera. Activar en H01!B40 cuando la reforma COOTAD artículos 198-199 sea vigente para este GAD.",IF(LEFT(B10,2)="⚠️","Estructura fiscal con inversión por debajo del mínimo COOTAD. Revisar composición del gasto con Dirección Financiera para fortalecer la inversión pública local.","Estructura fiscal dentro de los parámetros COOTAD. Sin señales de alerta fiscal."))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H24_SAT-IV
A2	H24 — SAT-IV — ALERTA FISCAL COOTAD
A3	Activa si el gasto corriente supera el 35% del presupuesto total o si la inversión baja del 65%. Marco: COOTAD Arts.198-199 (reforma 23-feb-2026).
A5	▌ PARÁMETROS SAT-IV
A6	SAT_IV_Activa
C6	Control en H01!B40 — cambiar a SÍ si reforma COOTAD feb-2026 confirmada
A7	Pct_Inversion_Minimo
C7	Inversión mínima requerida COOTAD (H01!B38=65%)
A8	Pct_Corriente_Maximo
C8	Gasto corriente máximo COOTAD (H01!B39=35%)
A9	Ti_Global_2026
C9	Ejecución global Ti (H07!B20)
A10	Alerta_Corriente
A12	▌ ESTADO SAT-IV
A13	SAT_IV_Estado
A15	▌ NOTA REFORMA COOTAD
B15	SAT-IV_Activa se controla desde H01!B40. Si la reforma COOTAD de feb-2026 es confirmada, cambiar H01!B40 a "SÍ". Actualmente en "NO". Marco: COOTAD Arts.198-199 (reforma 23-feb-2026).
A17	▌ DIAGNÓSTICO PREVENTIVO SAT-IV
A19	✔ CHECKPOINT H24 — 2 puntos
B19	1. SAT_IV_Activa lee de H01!B40 — control centralizado
B20	2. Umbrales Pct_Inversion y Pct_Corriente leen de H01!B38 y H01!B39
```