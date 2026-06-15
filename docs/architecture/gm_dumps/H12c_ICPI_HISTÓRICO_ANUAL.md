# H12c_ICPI_HISTÓRICO_ANUAL — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=16 · fórmulas=16
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
E7	=IF(B7>=90,"🔵 Excelencia en Gobernanza",IF(B7>=70,"🟢 Gestión por Mandato",IF(B7>=40,"🟡 Transición Crítica",IF(B7>=20,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
D8	=B8-B7
E8	=IF(B8>=90,"🔵 Excelencia en Gobernanza",IF(B8>=70,"🟢 Gestión por Mandato",IF(B8>=40,"🟡 Transición Crítica",IF(B8>=20,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B9	=H01_PARÁMETROS!B15*100
D9	=B9-B8
B10	=H12_MOTOR_ICPI_CANÓNICO!B33
D10	=B10-B9
E10	=IF(B10>=90,"🔵 Excelencia",IF(B10>=70,"🟢 Gestión por Mandato",IF(B10>=40,"🟡 Transición Crítica",IF(B10>=20,"🟠 Por Ocurrencia","🔴 Ruptura"))))
B13	=AVERAGE(B7:B9)
B14	=MAX(B7:B9)
B15	=MIN(B7:B9)
B16	=IFERROR((B9/B7)^(1/2)-1,0)
B17	=B9*(1+B16)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H12c_ICPI_HISTÓRICO_ANUAL
A2	H12c — SERIE HISTÓRICA 2023-2026 — ⚠️ 2023/2024 = proxies Ti_Inversión | 2025 = ICPI Canónico ★ ICPI_Real_2025 (resultado canónico)
A3	Años 2023-2025: valores verificados del corpus SIAP-ICPI. Año 2026: calculado dinámicamente por H12.
A5	▌ SERIE HISTÓRICA ICPI ANUAL
A6	Año
B6	Valor_%
C6	Tipo de dato — Fuente y Advertencia
D6	Variación_yoy_pp
E6	Nivel_AVEP
F6	Fuente
G6	Nota
A7	2023
B7	68.04
C7	⚠️ Ti_Inversión_eSIGEF_2023 (proxy) — ICPI canónico 2023 simulado de recálculo completo. NO confundir con ICPI.
D7	0
F7	H07b Ti_INVERSIÓN_eSIGEF — Ti_2023
G7	Primer año de serie SIAP-ICPI v1.0 disponible
A8	2024
B8	79.61
C8	⚠️ Ti_Inversión_eSIGEF_2024 (proxy) — ICPI canónico 2024 simulado de recálculo completo. NO confundir con ICPI.
F8	H07b Ti_INVERSIÓN_eSIGEF — Ti_2024
G8	Salto +11.57pp — mayor ejecución eSIGEF
A9	2025
C9	✅ ICPI_Real_2025 = 69.9309% — primer resultado auditado bajo metodología SIAP-ICPI completa (calibración retroactiva Ci 2025).
E9	🟡 Transición Crítica
F9	H01_PARÁMETROS!B15 — ICPI_Real_2025
G9	CAÍDA -9.68pp vs 2024 — ICPI_Real_2025 VERIFICADO (●3)
A10	2026
C10	Ti_Inversión_eSIGEF_2026 (parcial datos reales) — ICPI canónico 2026 en cálculo activo.
F10	H12_MOTOR_ICPI_CANÓNICO!B33 — Dinámico
G10	⏳ En curso 2026 — actualizar mensualmente con Ti_m de eSIGEF
A12	ESTADÍSTICOS HISTÓRICOS
A13	ICPI Promedio 2023-2025
A14	Máximo histórico (2024)
A15	Mínimo histórico (2023)
A16	Tendencia CAGR 2023-2025
A17	ICPI_2026_Proyectado si tendencia CAGR
A19	⚠️ NOTA METODOLÓGICA SERIES 2023-2024: Los valores 2023 (68.04%) y 2024 (79.61%) son proxies de Ti_Inversión_eSIGEF (Grupos 7+8), NO ICPI canónicos. El ICPI requiere Pi×Ri×Vi×Ei×Ti×Ci por meta — esos multiplicadores no están disponibles para años anteriores a 2025. El ICPI_2025 = 69.9309% es el único valor certificado bajo metodología SIAP-ICPI completa. Los valores 2023/2024 deben presentarse como indicadores proxy, no como ICPI. Válido para contexto de tendencia, no para comparación exacta con el axioma.
B19	La caída 2025 vs 2024 (-9.68pp) refleja el recalibrado metodológico SIAP-ICPI v1.0: los verificadores S7 (LOTAIP) y S8 (CPCCS) se activaron en 2025. En 2024 no existían estos verificadores, por lo que el ICPI_2024 es una retrociálculo proxy. La serie 2023-2024 es indicativa; el ICPI 2025 es el primer valor auditado bajo metodología SIAP-ICPI completa.
```