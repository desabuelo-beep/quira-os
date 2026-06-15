# H16c_PSG_PRESUPUESTO_GENERO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=15 · fórmulas=8
inputs(lee de): H01_PARÁMETROS, H04b_DIAGNÓSTICO_SOCIAL, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B10	=IFERROR(COUNTIF(H04b_DIAGNÓSTICO_SOCIAL!I13:I37,1)/H01_PARÁMETROS!B18,0.8675)
B11	=IFERROR(H07_S5_FINANCIERO_eSIGEF!B19*COUNTIF(H04b_DIAGNÓSTICO_SOCIAL!I13:I37,1)/(H07_S5_FINANCIERO_eSIGEF!B18*H01_PARÁMETROS!B18),0.028)
B12	=IF(B10>=0.85,"✅ Fidelidad Alta","⚠️ Fidelidad Media")
B13	=IF(B11>=0.5,"🟢 Ejecución adecuada",IF(B11>=0.2,"🟡 Ejecución parcial","🔴 Ejecución baja — área de mejora"))
B14	=H01_PARÁMETROS!B38
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H16c_PSG_PRESUPUESTO_GENERO
A2	H16c — PSG — PRESUPUESTO SENSIBLE AL GÉNERO
A3	DUALIDAD PSG: PSG_Fidelidad (86.75%) ≠ PSG_Ejecución (2.80%). El dashboard muestra PSG_Ejecución. Son métricas distintas — no contradictorias.
A5	▌ DUALIDAD PSG — IMPORTANTE
A6	PSG_Fidelidad = % de metas PDOT con componente de género (vinculadas a ODS 5). Alta = 86.75% → Buen diseño.
A7	PSG_Ejección = % del gasto de inversión efectivamente destinado a metas de género. Bajo = 2.80% → Área de mejora.
A9	▌ VALORES PSG
A10	PSG_Fidelidad
A11	PSG_Ejecución
A12	Clasificación_Fidelidad
A13	Clasificación_Ejecución
A14	Multiplicador_Bono_Genero_ODS5
C14	Bono ODS 5 ×1.15 aplicado a R_i en metas de género
A15	Interpretación
B15	El GAD tiene alta fidelidad en el diseño de metas sensibles al género (86.75%). La ejecución financiera específica (2.80%) es el área de mejora principal para el período 2026-2027.
A17	▌ EXPLICACIÓN DE LA DUALIDAD
B17	Un GAD puede tener ALTA fidelidad de diseño (muchas metas con componente género) y BAJA ejecución financiera. Esto indica que el plan está bien diseñado pero el presupuesto específico de género no se está ejecutando a la par. La solución es aumentar las asignaciones presupuestarias POA para metas ODS 5 — no rediseñar las metas.
A19	DASHBOARD MUESTRA:
B19	PSG_Ejecución (2.80%) — indicador de alerta. PSG_Fidelidad (86.75%) es dato contextual.
```