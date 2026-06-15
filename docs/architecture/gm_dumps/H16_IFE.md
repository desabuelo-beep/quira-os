# H16_IFE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=16 · fórmulas=8
inputs(lee de): H03_S1_ELECTORAL_CNE, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H33_TAC_QUIRA_CIUDADANA, H39_AUTOCONTROL_ECOSISTEMA, H73_OUTPUT_API, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H03_S1_ELECTORAL_CNE!B9
B7	=IF(B6>=0.85,"✅ Fidelidad Electoral Alta",IF(B6>=0.6,"⚠️ Fidelidad Electoral Media","🔴 Fidelidad Electoral Baja"))
B8	="El GAD convirtió el "&TEXT(B6,"0%")&" de sus promesas electorales en metas estratégicas del PDOT."
B9	=H03_S1_ELECTORAL_CNE!B7
B10	=H03_S1_ELECTORAL_CNE!B8
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H16_IFE
A2	H16 — IFE — ÍNDICE DE FIDELIDAD ELECTORAL
A3	Mide qué % de las 66 promesas CNE se convirtió en metas PDOT verificables. NIVEL 3 — Solo referencia H03.
A5	▌ PANEL IFE
A6	IFE_Global
C6	← Fuente única: H03_S1_ELECTORAL_CNE
A7	Clasificación_IFE
A8	Interpretación
A9	Promesas_Totales_CNE
A10	Promesas_Vinculadas_PDOT
A11	Valor_2025_Referencia
B11	0.7283
A13	▌ NOTA METODOLÓGICA
B13	El IFE verifica el origen democrático de los compromisos. La base del ecosistema SIAP-ICPI es el PDOT (S2). El CNE es el origen político-democrático. Un IFE alto significa que las promesas electorales se tradujeron en planificación estratégica real.
A15	▌ ESCALA DE CLASIFICACIÓN IFE
A16	Umbral
B16	Nivel
A17	≥85%
B17	✅ Fidelidad Electoral Alta
A18	60–84%
B18	⚠️ Fidelidad Electoral Media
A19	<60%
B19	🔴 Fidelidad Electoral Baja
```