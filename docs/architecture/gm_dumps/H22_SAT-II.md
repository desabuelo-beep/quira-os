# H22_SAT-II — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=28 · pobladas=17 · fórmulas=10
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B51
B7	=IFERROR(H07_S5_FINANCIERO_eSIGEF!B18,0)
B9	=IF(B7=0,0,B8/B7)
C9	=Total_Reformas / Presupuesto_Base
B12	=IF(B9>B6,"⚠️ SAT-II ACTIVO — Reforma significativa detectada. Revisar cronograma de ejecución.","✅ Sin señal SAT-II")
B14	=IF(B9>B6,"Reforma presupuestaria superior al "&TEXT(B6,"0%")&" del total codificado. Revisar el cronograma de ejecución para mantener la alineación con el POA y las metas del PDOT. Ref: COPFP Art.115.","Reformas dentro del umbral aceptable. Sin señales de impacto significativo en la programación anual.")
B25	=SUM(C18:C24)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H22_SAT-II
A2	H22 — SAT-II — REFORMA TARDÍA
A3	Detecta reformas presupuestarias significativas que alteran más del 5% del presupuesto total. Fundamentación: COPFP Art.115.
A5	▌ PARÁMETROS SAT-II
A6	SAT_II_Umbral_Reforma
C6	Umbral reforma significativa (H01!B51=5%)
A7	Presupuesto_Codificado_Base
C7	Presupuesto codificado base (H07!B18)
A8	Total_Reformas_2026
B8	0
C8	Ingresar suma de reformas presupuestarias 2026 (actualizar manualmente)
A9	Pct_Reforma
A11	▌ ESTADO SAT-II
A12	SAT-II_Estado
A14	▌ DIAGNÓSTICO PREVENTIVO SAT-II
A16	▌ HISTORIAL DE REFORMAS 2026
A17	Nº Reforma
B17	Fecha
C17	Monto_USD
D17	Tipo
E17	Justificación
F17	Aprobado_por
A18	⬜ REF-001
C18	0
D18	[Incremento/Disminución]
E18	[Justificación preventiva]
A25	SUMA TOTAL REFORMAS
A27	✔ CHECKPOINT H22 — 2 puntos
B27	1. Umbral referencia H01!B51 (5%) — sin hardcoding
B28	2. Diagnóstico usa "Revisar cronograma" (preventivo) — NO "irregularidad"
```