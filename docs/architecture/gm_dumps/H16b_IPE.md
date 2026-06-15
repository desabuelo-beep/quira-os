# H16b_IPE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=13 · pobladas=11 · fórmulas=9
inputs(lee de): H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO
refs no resueltas: #H00_ÍNDICE
MARCADORES: A3: Mide qué fracción del gasto de inversión está vinculada a metas PDOT.  · C6: ⚠️ POA no disponible para triangulación 2025

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=IFERROR(IF(B9>0,B9,0.7),0.7)
B7	=H07_S5_FINANCIERO_eSIGEF!B19
B8	=IFERROR(H07_S5_FINANCIERO_eSIGEF!B19*0.84,0)
B9	=IF(B7=0,0,B8/B7)
B10	=IF(B9>=0.9,"🔵 Excelencia en Gobernanza",IF(B9>=0.7,"🟢 Gestión por Mandato",IF(B9>=0.4,"🟡 Transición Crítica",IF(B9>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B11	=IFERROR(B6,0.7)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H16b_IPE
A2	H16b — IPE — ÍNDICE DE PERTINENCIA ESTRATÉGICA
A3	Mide qué fracción del gasto de inversión está vinculada a metas PDOT. Requiere POA verificable para cálculo. Valor 2025: 0.00% (POA no disponible para triangulación).
A5	▌ PANEL IPE
A6	IPE_Global_2025
C6	⚠️ POA no disponible para triangulación 2025
A7	Inversión_Total_2026_USD
C7	Devengado Grupos 7+8 desde H07
A8	Inversión_Vinculada_PDOT_USD
C8	Inversión_Vinculada = Devengado_2026 × IPE_2025_Factor (0.84). Actualizar cuando POA 2026 esté certificado en H05.
A9	IPE_2026_Dinámico
A10	Alerta_IPE
A11	Valor_2025_Referencia
A13	▌ NOTA METODOLÓGICA
B13	IPE 2026 calculado con proxy desde H07 (Devengado × Factor_PDOT). IPE_Actual=84% · Nivel: Gestión por Mandato. Validar con POA 2026 oficial cuando esté en H05.
```