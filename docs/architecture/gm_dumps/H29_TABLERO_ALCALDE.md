# H29_TABLERO_ALCALDE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=50 · pobladas=44 · fórmulas=56
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO, H17_IED, H20c_IEF_EFICIENCIA_FINANCIERA, H28_RESUMEN_EJECUTIVO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H12_MOTOR_ICPI_CANÓNICO!B33
B7	=IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=95,"🟢 Excelencia Institucional",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=85,"🔵 Buen Gobierno",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=70,"🟡 Gestión por Mandato",IF(H12_MOTOR_ICPI_CANÓNICO!B33*100>=50,"🟠 Transición Crítica","🔴 Ruptura Sistémica"))))
B8	="SIGAD: 100% vs ICPI Verificado: "&TEXT(H12_MOTOR_ICPI_CANÓNICO!B33,"0.0%")&" — Brecha de Verificación: "&TEXT(H12_MOTOR_ICPI_CANÓNICO!B36,"0.0")&"pp"
B9	=H12_MOTOR_ICPI_CANÓNICO!B37
B12	=INDEX(H17_IED!A11:A21,MATCH(MIN(H17_IED!B11:B21),H17_IED!B11:B21,0))
B13	=MIN(H17_IED!B11:B21)
B14	=IF(B13<0.4,"🔴 Nivel de Atención Alta — Requiere plan de acción",IF(B13<0.7,"🟡 Transición Crítica — En seguimiento","✅ En rango"))
A17	=H17_IED!A11
B17	=H17_IED!B11
C17	=IF(H17_IED!B11>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B11>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B11>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B11>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A18	=H17_IED!A12
B18	=H17_IED!B12
C18	=IF(H17_IED!B12>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B12>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B12>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B12>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A19	=H17_IED!A13
B19	=H17_IED!B13
C19	=IF(H17_IED!B13>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B13>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B13>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B13>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A20	=H17_IED!A14
B20	=H17_IED!B14
C20	=IF(H17_IED!B14>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B14>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B14>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B14>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A21	=H17_IED!A15
B21	=H17_IED!B15
C21	=IF(H17_IED!B15>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B15>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B15>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B15>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A22	=H17_IED!A16
B22	=H17_IED!B16
C22	=IF(H17_IED!B16>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B16>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B16>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B16>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A23	=H17_IED!A17
B23	=H17_IED!B17
C23	=IF(H17_IED!B17>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B17>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B17>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B17>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A24	=H17_IED!A18
B24	=H17_IED!B18
C24	=IF(H17_IED!B18>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B18>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B18>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B18>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A25	=H17_IED!A19
B25	=H17_IED!B19
C25	=IF(H17_IED!B19>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B19>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B19>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B19>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A26	=H17_IED!A20
B26	=H17_IED!B20
C26	=IF(H17_IED!B20>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B20>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B20>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B20>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
A27	=H17_IED!A21
B27	=H17_IED!B21
C27	=IF(H17_IED!B21>=0.9,"🔵 Excelencia en Gobernanza",IF(H17_IED!B21>=0.7,"🟢 Gestión por Mandato",IF(H17_IED!B21>=0.4,"🟡 Transición Crítica — En seguimiento",IF(H17_IED!B21>=0.2,"🟠 Gestión por Ocurrencia — Fortalecer procesos","🔴 Nivel de Atención Alta — Requiere plan de acción"))))
B30	=H28_RESUMEN_EJECUTIVO!B27
B31	=H28_RESUMEN_EJECUTIVO!B28
B32	=H28_RESUMEN_EJECUTIVO!B29
B33	=H28_RESUMEN_EJECUTIVO!B30
B34	=H28_RESUMEN_EJECUTIVO!B31
B35	=H28_RESUMEN_EJECUTIVO!B32
B36	=H28_RESUMEN_EJECUTIVO!B33
B41	=H12_MOTOR_ICPI_CANÓNICO!B33
B46	=H20c_IEF_EFICIENCIA_FINANCIERA!B41
B47	=H20c_IEF_EFICIENCIA_FINANCIERA!B42
B48	="$"&TEXT(H20c_IEF_EFICIENCIA_FINANCIERA!B39,"#,##0")
B49	="$"&TEXT(H20c_IEF_EFICIENCIA_FINANCIERA!B40,"#,##0")
B50	=IF(H20c_IEF_EFICIENCIA_FINANCIERA!B41>=0.1,"✅ Buena captación de fondos externos — diversificación activa",IF(H20c_IEF_EFICIENCIA_FINANCIERA!B41>=0.05,"🟡 Captación moderada — revisar oportunidades de fondos concursables","🟠 Oportunidad de mejora — explorar fondos externos disponibles"))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H29_TABLERO_ALCALDE
A2	H29 — TABLERO DEL ALCALDE — DECISIONES ESTRATÉGICAS
A3	Vista ejecutiva para toma de decisiones del Alcalde. Responde 5 preguntas clave.
A5	▌ PREGUNTA 1 — ¿CÓMO VAMOS?
A6	ICPI Verificado:
A7	Clasificación:
A8	vs SIGAD Oficial:
A9	Diagnóstico:
A11	▌ PREGUNTA 2 — ¿DÓNDE ENFOCAR ATENCIÓN?
A12	Dirección con menor IED:
A13	IED mínimo:
A14	Señal:
A16	Dirección
B16	IED_%
C16	Clasificación
A29	▌ PREGUNTA 3 — ¿QUÉ SEÑALES SAT ESTÁN ACTIVAS?
A30	SAT-0 (Coherencia POA-PAC):
A31	SAT-I (Fragmentación Selectiva):
A32	SAT-II (Reforma Tardía):
A33	SAT-III (Parálisis Presupuestaria):
A34	SAT-IV (Alerta Fiscal COOTAD):
A35	SAT-V (Brecha CPCCS):
A36	SAT-VI (Desvío PP):
A38	▌ PREGUNTA 4 — ¿CÓMO VA LA TENDENCIA?
A39	2023 (REAL-eSIGEF):
B39	0.5736130950255192
A40	2024 (REAL-eSIGEF):
B40	0.6711542988680421
A41	2025 (canónico):
A42	2026 (en curso):
B42	Motor H12 vivo
A43	Objetivo mandato 2027:
B43	≥70% 🟢 Gestión por Mandato
A45	▌ PREGUNTA 5 — ¿ESTAMOS CAPTANDO FONDOS EXTERNOS?
A46	IEF_2026:
C46	Eficiencia Financiera
A47	Clasificación IEF:
A48	Fondos externos captados:
A49	Presupuesto propio codificado:
A50	Señal:
```