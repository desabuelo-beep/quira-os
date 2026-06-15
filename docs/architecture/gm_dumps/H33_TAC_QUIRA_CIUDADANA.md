# H33_TAC_QUIRA_CIUDADANA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=21 · pobladas=18 · fórmulas=14
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H10_S8_PARTICIPACIÓN_CPCCS, H12_MOTOR_ICPI_CANÓNICO, H16_IFE, H18_ITAM
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=95,"🟢 La gestión municipal opera con excelencia institucional",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=85,"🔵 Buen gobierno — Metas superando el 85%",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=70,"🟡 Gestión sólida — en camino a las metas",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=50,"🟠 En transición — avance parcial, con oportunidades de mejora","🔴 Atención ciudadana — requiere plan de acción municipal"))))
B8	=TEXT(H16_IFE!B6,"0%")&" de las promesas electorales verificadas"
B9	="Ti 2026: "&TEXT(H07_S5_FINANCIERO_eSIGEF!B20,"0%")&" del presupuesto de inversión ejecutado"
B10	=IF(H18_ITAM!B6>=0.7,"✅ Sí, disponible en el portal municipal","⚠️ En proceso de actualización")
B11	=IF(H10_S8_PARTICIPACIÓN_CPCCS!B7>0,"✅ Sí — "&TEXT(H10_S8_PARTICIPACIÓN_CPCCS!B7,"dd/mm/yyyy"),"🔄 Programada")
B14	=H01_PARÁMETROS!B6
B15	=H01_PARÁMETROS!B11
B16	=H01_PARÁMETROS!B10
B17	=H01_PARÁMETROS!B13
B18	=H01_PARÁMETROS!B19&" metas estratégicas 2023-2027"
B19	=TODAY()
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H33_TAC_QUIRA_CIUDADANA
A2	H33 — TAC — TABLERO DE ACCOUNTABILITY CIUDADANA
A3	Interfaz pública simplificada para ciudadanía. SIAP-ICPI Ciudadana. Lenguaje ciudadano, no técnico.
A5	▌ PARA EL CIUDADANO — PREGUNTAS FRECUENTES SOBRE LA GESTIÓN MUNICIPAL
A6	Pregunta ciudadana
B6	Respuesta
A7	¿Cómo va la gestión de Montecristi?
A8	¿Qué porcentaje de las promesas electorales se cumplieron?
A9	¿Cómo va la inversión pública?
A10	¿Está publicada la información pública?
A11	¿Se realizó rendición de cuentas?
A13	▌ INFORMACIÓN ADICIONAL PARA LA CIUDADANÍA
A14	Municipio:
A15	Alcalde:
A16	Período de gobierno:
A17	Año activo:
A18	Metas del plan de gobierno:
A19	Fecha de actualización:
A21	ℹ️ NOTA: Este tablero se actualiza automáticamente con cada ingreso de datos al sistema SIAP-ICPI v1.0. Para mayor información, consultar el portal de transparencia del GAD Municipal de Montecristi.
```