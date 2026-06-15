# H20b_IGP_GOBERNANZA_PARTIC — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=13 · pobladas=11 · fórmulas=8
inputs(lee de): H10_S8_PARTICIPACIÓN_CPCCS, H10b_S8b_PARTICIPATIVO, H12_MOTOR_ICPI_CANÓNICO, H34b_MFN_FIDELIDAD_NARRATIVA
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H73_OUTPUT_API, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE
MARCADORES: B9: =IF(AND(B6=0,B7=0,B8=0),"Sin datos 2026 — Ref. 2025: 27,98%",AVERAGE(B · B10: =IF(AND(B6=0,B7=0,B8=0),"⏳ Sin datos 2026 — Ref. 2025: 27,98% (Goberna

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=IFERROR(AVERAGE(H10_S8_PARTICIPACIÓN_CPCCS!E18:E42), 0)
B7	=IFERROR(AVERAGE(H10b_S8b_PARTICIPATIVO!F13:F17)/100, 0)
B8	=IFERROR(AVERAGE(H34b_MFN_FIDELIDAD_NARRATIVA!J11:J37), 0.28)
B9	=IF(AND(B6=0,B7=0,B8=0),"Sin datos 2026 — Ref. 2025: 27,98%",AVERAGE(B6:B8))
B10	=IF(AND(B6=0,B7=0,B8=0),"⏳ Sin datos 2026 — Ref. 2025: 27,98% (Gobernanza por Ocurrencia)",AVERAGE(B6:B8))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H20b_IGP_GOBERNANZA_PARTIC
A2	H20b — IGP — ÍNDICE DE GOBERNANZA PARTICIPATIVA
A3	Compuesto por: IGP_1 (Asamblea CPCCS) + IGP_2 (PP activo) + IGP_3 (Fidelidad Narrativa MFN). Valor 2025: 27.98%.
A5	▌ PANEL IGP — 3 COMPONENTES
A6	IGP_1_Asamblea_CPCCS
C6	Actualizar desde H10 cuando CPCCS 2026 esté disponible
A7	IGP_2_Presupuesto_Participativo
C7	Actualizar desde H10b cuando PP 2026 esté disponible
A8	IGP_3_Fidelidad_Narrativa_MFN
C8	✅ Conectado — AVERAGE(H34b!J11:J19) ≈ 91% | Fuente: Matriz Fidelidad Narrativa 9 registros MFN
A9	IGP_Global
A10	Clasificación_IGP
A11	Ref_2025_IGP
B11	0.2798
C11	🟠 Gobernanza por Ocurrencia 2025
A13	▌ NOTA METODOLÓGICA IGP
B13	El IGP 27.98% de 2025 refleja la ausencia de actividad formal de participación ciudadana registrada en CPCCS y presupuesto participativo. El componente IGP_3 (Fidelidad Narrativa MFN) requiere H34b, disponible en FASE 11. El bajo IGP indica una OPORTUNIDAD de mejora, no una falla estructural del GAD.
```