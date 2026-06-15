# H21b_SAT-0_COHERENCIA_PAC — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=32 · pobladas=25 · fórmulas=14
inputs(lee de): H01_PARÁMETROS, H05_S3_OPERATIVO_POA, H05b_S3b_PAC_CONTRATACIÓN, H06_S4_CONTRATACIÓN_SERCOP, H07c_Ti_VERIFICADO_INFORME, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE
MARCADORES: B14: =IFERROR(IF(ABS(H05b_S3b_PAC_CONTRATACIÓN!B19-H05_S3_OPERATIVO_POA!B19 · B15: =IFERROR(IF(H06_S4_CONTRATACIÓN_SERCOP!B12>H01_PARÁMETROS!B51,"⚠️ Down · B16: =IFERROR(IF(H05b_S3b_PAC_CONTRATACIÓN!B10<H01_PARÁMETROS!B56,"⚠️ Proce · B17: =IFERROR(IF(COUNTA(H07c_Ti_VERIFICADO_INFORME!A24:A50)=0,"⏳ Sin proces · B23: =IFERROR(IF(COUNTIF(H07c_Ti_VERIFICADO_INFORME!J23:J50,"")=0,"✅ Todos 

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B55
B7	=H01_PARÁMETROS!B56
B8	=H01_PARÁMETROS!B63
B9	=H01_PARÁMETROS!B57
B14	=IFERROR(IF(ABS(H05b_S3b_PAC_CONTRATACIÓN!B19-H05_S3_OPERATIVO_POA!B19)/IF(H05_S3_OPERATIVO_POA!B19=0,1,H05_S3_OPERATIVO_POA!B19)>H01_PARÁMETROS!B55,"⚠️ Brecha POA-PAC activa","✅ Dentro del umbral"),"⏳ Sin datos")
B15	=IFERROR(IF(H06_S4_CONTRATACIÓN_SERCOP!B12>H01_PARÁMETROS!B51,"⚠️ Downcoding detectado","✅ Sin downcoding"),"⏳ Sin datos SERCOP")
B16	=IFERROR(IF(H05b_S3b_PAC_CONTRATACIÓN!B10<H01_PARÁMETROS!B56,"⚠️ Procesos bajo monto mínimo","✅ Montos sobre umbral"),"⏳ Sin datos PAC")
B17	=IFERROR(IF(COUNTA(H07c_Ti_VERIFICADO_INFORME!A24:A50)=0,"⏳ Sin procesos PAC registrados en H07c",IF(COUNTIFS(H07c_Ti_VERIFICADO_INFORME!A24:A50,"<>",H07c_Ti_VERIFICADO_INFORME!J24:J50,"")>0,"🔴 GASTO CIEGO — "&COUNTIFS(H07c_Ti_VERIFICADO_INFORME!A24:A50,"<>",H07c_Ti_VERIFICADO_INFORME!J24:J50,"")&" proceso(s) sin evidencia SHA-256 en H07c","✅ Evidencia en plazo — "&COUNTA(H07c_Ti_VERIFICADO_INFORME!A24:A50)&" proceso(s) verificados")),"⏳ Sin datos H07c")
B19	=IF(OR(LEFT(B14,2)="⚠️",LEFT(B15,2)="⚠️",LEFT(B16,2)="⚠️",COUNTIFS(H07c_Ti_VERIFICADO_INFORME!A24:A50,"<>",H07c_Ti_VERIFICADO_INFORME!J24:J50,"")>0),"⚠️ SAT-0 ACTIVO — Revisar coherencia POA-PAC","✅ Sin señal SAT-0")
B21	=IF(B19="✅ Sin señal SAT-0","Sin señales de incoherencia POA-PAC en el período analizado.","Detectada brecha entre programación operativa y plan de contratación. Revisar alineación POA-PAC para fortalecer la ejecución del plan anual.")
B23	=IFERROR(IF(COUNTIF(H07c_Ti_VERIFICADO_INFORME!J23:J50,"")=0,"✅ Todos los procesos PAC tienen evidencia en plazo","🔴 "&COUNTIF(H07c_Ti_VERIFICADO_INFORME!J23:J50,"")&" proceso(s) sin evidencia SHA-256 — riesgo observación Contraloría"),"⏳ Sin datos H07c")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H21b_SAT-0_COHERENCIA_PAC
A2	H21b — SAT-0 — COHERENCIA POA-PAC
A3	Señal preventiva que detecta brechas entre la programación operativa (POA) y el plan de contrataciones (PAC). Marco: LOSNCP Art.22.
A5	▌ PARÁMETROS SAT-0 (de H01)
A6	SAT0_C3_Umbral_Brecha
C6	Umbral brecha POA-PAC (H01!B55=20%)
A7	SAT0_Monto_Minimo
C7	Monto mínimo proceso analizable (H01!B56=$10,000)
A8	SAT0_Fecha_Corte
C8	Fecha de corte (H01!B63 — PND_Resolución)
A9	SAT0_Umbral_Downcoding
C9	Umbral downcoding (H01!B57)
A10	SAT0_Umbral_Dias_Evidencia
B10	7
C10	Días máx. entre publicación PAC y evidencia SHA-256 (Reloj Coerción C4)
A12	▌ ESTADO SAT-0
A13	Componente
B13	Estado
C13	Descripción / Fórmula
A14	C1 — Brecha POA-PAC
C14	Brecha > umbral B49 entre montos POA (H05) y PAC (H05b)
A15	C2 — Downcoding
C15	Cambio tipo contratación hacia menor jerarquía (H06 vs H01!B51)
A16	C3 — Monto mínimo
C16	Procesos bajo $10k excluidos del análisis (H01!B50)
A17	C4 — Reloj Coerción (Gasto Ciego)
C17	Compara publicación PAC vs evidencia SHA-256 en H07c. Umbral: B10 días.
A19	SAT-0_Global
A21	▌ DIAGNÓSTICO PREVENTIVO SAT-0
A23	▌ RESUMEN RELOJ DE COERCIÓN C4
A25	▌ MARCO LEGAL
B25	LOSNCP Art.22 — Obligatoriedad del PAC y coherencia con el POA institucional.
B26	Acuerdo MEF 067 — Registros presupuestarios y devengados en eSIGEF.
B27	Contraloría General del Estado — Normas de Control Interno 402-01 Responsabilidad del control.
A29	✔ CHECKPOINT H21b
B29	1. Todos los umbrales referencian H01 (B49, B50, B51, B63) — SIN hardcoding
B30	2. Diagnóstico usa lenguaje preventivo: "Revisar alineación" — NO "incumplimiento"
B31	3. Reloj de Coerción C4 presente como componente en fila 17
B32	4. SAT-0_Global (B19) incluye condición IZQUIERDA(B17,2)="�" para activar con C4
```