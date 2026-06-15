# H18_ITAM — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=20 · pobladas=17 · fórmulas=5
inputs(lee de): H09_S7_TRANSPARENCIA_LOTAIP, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H33_TAC_QUIRA_CIUDADANA, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=IF(B6>=0.9,"🔵 Excelencia en Gobernanza",IF(B6>=0.7,"🟢 Gestión por Mandato",IF(B6>=0.4,"🟡 Transición Crítica",IF(B6>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B8	=H09_S7_TRANSPARENCIA_LOTAIP!B7
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H18_ITAM
A2	H18 — ITAM — ÍNDICE DE TRANSPARENCIA ALGORÍTMICA MUNICIPAL
A3	Mide el cumplimiento de obligaciones de transparencia LOTAIP Art.7. Fuente: H09_S7_TRANSPARENCIA_LOTAIP.
A5	▌ PANEL ITAM
A6	ITAM_Global_2025_Ref
B6	0.8229
C6	56.00% — Transición Crítica
A7	Clasificación_ITAM
A8	URL_Base_GAD
A9	Metas_con_URL_Pública
B9	21
C9	de 25 metas totales
A10	Metas_sin_URL_Pública
B10	4
A11	ITAM_2026_Vivo (proyección desde 2025 si sin URLs)
B11	0.84
A13	▌ DESGLOSE OBLIGACIONES LOTAIP
A14	Artículo
B14	Obligación
C14	Estado_2025
A15	Art. 7
B15	Publicación información básica institucional
C15	✅ Cumplido
A16	Art. 19
B16	Actualización mensual de información
C16	✅ Publicado en website.montecristi.gob.ec
A17	Art. 29
B17	Rendición de cuentas anual CPCCS
C17	⚠️ Parcial
A19	▌ IOC (INVERSO TRANSPARENCIA)
A20	IOC_2025_Ref
B20	0.1771
C20	🔴 Opacidad Crítica — Ver plan de mejora LOTAIP
```