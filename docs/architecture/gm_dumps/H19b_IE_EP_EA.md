# H19b_IE_EP_EA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=12 · pobladas=10 · fórmulas=12
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO, H12d_ICPI_POR_ENTIDAD
outputs(alimenta a): H00_ÍNDICE, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
E7	=H12_MOTOR_ICPI_CANÓNICO!B33/100
F7	=H12_MOTOR_ICPI_CANÓNICO!B33/100
G7	=IF(D7>C7,IF(E7>D7,"⬆️⬆️ Aceleración","⬆️➡️ Mejora"),"➡️⬇️ Regresión")
F8	=IFERROR(H12d_ICPI_POR_ENTIDAD!E10/100,0)
G8	=IF(D8>C8,"⬆️➡️ Mejora","➡️⬇️ Regresión")
F9	=IFERROR(H12d_ICPI_POR_ENTIDAD!E9/100,0)
G9	=IF(D9>C9,IF(E9<D9,"⬆️⬇️ Volatilidad","⬆️➡️ Mejora"),"➡️⬇️ Regresión")
F10	=IFERROR(H12d_ICPI_POR_ENTIDAD!E8/100,0)
G10	=IF(D10>C10,IF(E10>D10,"⬆️⬆️ Aceleración","⬆️➡️ Mejora"),"➡️⬇️ Regresión")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H19b_IE_EP_EA
A2	H19b — IE EP/EA — ÍNDICE DE EFICIENCIA POR ENTIDAD
A3	IED desglosado por las 4 entidades del ecosistema. Datos históricos 2023-2025 inmutables (H36b). 2026 dinámico desde H12.
A5	▌ IED POR ENTIDAD — SERIE HISTÓRICA
A6	Entidad
B6	Cod_Entidad
C6	IED_2023
D6	IED_2024
E6	IED_2025
F6	IED_2026
G6	Tendencia
A7	GAD Central
B7	ENTE-01
C7	0.5736130950255192
D7	0.6711542988680421
A8	Patronato Municipal
B8	ENTE-02
C8	0.3503
D8	0.5377
E8	0.5377
A9	Cuerpo de Bomberos
B9	ENTE-03
C9	0.0077
D9	0.678
E9	0.1638
A10	EP Aseo Integral (EPAM)
B10	ENTE-04
C10	0
D10	0.6759
E10	0.9047
A12	NOTA:
B12	Todos los datos históricos 2023-2025 provienen de H36b_LOOKUP_ARRASTRE y son inmutables. Los valores 2026 se actualizan dinámicamente cuando el analista pueble H07 con eSIGEF 2026. ENTE-01 IED_2025 = ICPI_Global (GAD Central es el ente principal del ecosistema).
```