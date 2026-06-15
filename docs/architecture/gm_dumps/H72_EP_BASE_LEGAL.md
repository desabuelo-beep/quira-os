# H72_EP_BASE_LEGAL — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=26 · pobladas=23 · fórmulas=25
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): —
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=IFERROR(VLOOKUP(A7,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C7	=IFERROR(VLOOKUP(A7,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B8	=IFERROR(VLOOKUP(A8,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C8	=IFERROR(VLOOKUP(A8,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B9	=IFERROR(VLOOKUP(A9,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C9	=IFERROR(VLOOKUP(A9,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B10	=IFERROR(VLOOKUP(A10,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C10	=IFERROR(VLOOKUP(A10,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B11	=IFERROR(VLOOKUP(A11,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C11	=IFERROR(VLOOKUP(A11,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B12	=IFERROR(VLOOKUP(A12,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C12	=IFERROR(VLOOKUP(A12,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B13	=IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C13	=IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B14	=IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
C14	=IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"")
B18	=IF(B17="","",IFERROR(VLOOKUP(B17,H72_EP_BASE_LEGAL!A7:F14,2,FALSE),"⚠️ ID no encontrado"))
B19	=IF(B17="","",IFERROR(VLOOKUP(B17,H72_EP_BASE_LEGAL!A7:F14,3,FALSE),"⚠️ ID no encontrado"))
B20	=IF(B17="","",IFERROR(VLOOKUP(B17,H72_EP_BASE_LEGAL!A7:F14,4,FALSE),"⚠️ ID no encontrado"))
B21	=IF(B17="","",IFERROR(VLOOKUP(B17,H72_EP_BASE_LEGAL!A7:F14,5,FALSE),"⚠️ ID no encontrado"))
B22	=IF(B17="","",IFERROR(VLOOKUP(B17,H72_EP_BASE_LEGAL!A7:F14,6,FALSE),"⚠️ ID no encontrado"))
B23	=IF(B17="","",IFERROR(VLOOKUP(B17,TBL_RADAR_EP[],7,FALSE),"⚠️ No encontrado en H71"))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H72_EP_BASE_LEGAL
A2	H72 — CONSULTOR JURÍDICO AUTOMÁTICO — BASE LEGAL EP
A3	Diccionario normativo por tipo de entidad. Cuando H71 detecta una vulnerabilidad o alerta, H72 provee el contexto legal exacto, el artículo específico y la recomendación de acción preventiva. Fuente: TBL_ENTIDADES_ADSCRITAS (H01 Sección O).
A5	▌ TABLA BASE LEGAL — TBL_BASE_LEGAL_EP
A6	ID_Entidad
B6	Nombre_Entidad
C6	Ley_Marco
D6	Articulo_PEI
E6	Articulo_Gasto
F6	Recomendacion_Preventiva
A7	EP-01
D7	Art. 44 (Plan Estratégico Institucional obligatorio)
E7	COPFP Art. 115 (alineación PDOT)
F7	Elaborar PEI 2025-2027 con vinculación explícita a metas PDOT. Presentar antes de auditoría Contraloría.
A8	EP-02
D8	Art. 44 (Plan Estratégico Institucional obligatorio)
E8	COPFP Art. 115 (alineación PDOT)
F8	Elaborar PEI 2025-2027 con vinculación explícita a metas PDOT. Presentar antes de auditoría Contraloría.
A9	AD-01
D9	Art. 234 (plan de trabajo adscrita)
E9	COPFP Art. 10 (coherencia planificación)
F9	Elaborar Plan de Trabajo 2026 alineado al PDOT. Aprobación en Concejo antes del 31-Mar-2026.
A10	CB-01
D10	Art. 274 (planificación institucional)
E10	COPFP Art. 115
F10	Elaborar Plan Operativo Anual 2026 con vinculación PDOT. Coordinar con Dirección de Gestión de Riesgos GAD.
A11	NEW-01
D11	(completar cuando se registre en H01 Sección O)
E11	(completar)
F11	(completar)
A12	NEW-02
D12	(completar)
E12	(completar)
F12	(completar)
A13	NEW-03
D13	(completar)
E13	(completar)
F13	(completar)
A14	NEW-04
D14	(completar)
E14	(completar)
F14	(completar)
A16	▌ PANEL DE CONSULTA RÁPIDA
A17	Ingresa ID de entidad:
B17	EP-01
C17	← Cambiar por: EP-01, EP-02, AD-01, CB-01, NEW-XX
A18	Nombre_Entidad
A19	Ley_Marco
A20	Artículo PEI
A21	Artículo Gasto
A22	Recomendación
A23	Estado en H71
A25	▌ NOTA DE USO
A26	Esta hoja es un consultor jurídico pasivo. Nunca genera alertas por sí misma — responde consultas desde H71. Cuando un Gerente de EP o el equipo DYLUS LAB quiera entender el riesgo de una entidad específica, ingresa el ID en B17 y obtiene el contexto legal completo en segundos. Las recomendaciones usan lenguaje preventivo (Principio D7) — nunca términos punitivos.
```