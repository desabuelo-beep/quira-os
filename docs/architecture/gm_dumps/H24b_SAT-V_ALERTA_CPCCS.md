# H24b_SAT-V_ALERTA_CPCCS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=22 · pobladas=17 · fórmulas=9
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H31_REPORTE_CPCCS, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE
MARCADORES: C9: =1 - (Cumplidos/Total). 0 si sin datos. · B19: =IF(B7=0,"Sin datos de compromisos CPCCS registrados. Ingresar datos d

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B9	=IF(B7=0,0,1-B8/B7)
C9	=1 - (Cumplidos/Total). 0 si sin datos.
B12	=IF(B7=0,0,IFERROR(B8/B7,0))
B13	=IFERROR(H01_PARÁMETROS!B60,"INACTIVO")
B17	=IF(B9>0.3,"⚠️ SAT-V ACTIVO — Brecha de compromisos CPCCS > 30%. Fortalecer seguimiento.",IF(B9>0.1,"🟡 SAT-V Monitoreo — Brecha de compromisos entre 10-30%. Revisar cumplimiento.","✅ Sin señal SAT-V"))
B19	=IF(B7=0,"Sin datos de compromisos CPCCS registrados. Ingresar datos de la última RDC en B7 y B8.",IF(B9>0.3,"Brecha entre compromisos adquiridos ante el CPCCS y la ejecución verificada supera el 30%. Fortalecer el seguimiento e implementar plan de cierre de compromisos. Ref: LOPC Art.88.","Nivel de cumplimiento de compromisos CPCCS dentro de parámetros aceptables. Sin señales de brecha significativa."))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H24b_SAT-V_ALERTA_CPCCS
A2	H24b — SAT-V — ALERTA DE BRECHA CPCCS
A3	Detecta diferencias entre compromisos adquiridos ante el CPCCS y la ejecución real. Fundamentación: LOPC Art.88. NOTA: lenguaje preventivo — NO usar la palabra Desacato.
A5	▌ PARÁMETROS SAT-V
A6	Fecha_RDC_CPCCS
C6	Fecha última RDC (ingresar manualmente)
A7	Compromisos_CPCCS
B7	0
C7	Total compromisos CPCCS (actualizar)
A8	Compromisos_Cumplidos
B8	0
C8	Compromisos cumplidos (actualizar)
A9	Brecha_Compromisos
A11	▌ MECANISMO COMBINADO SAT-V (Decisión canónica 26-Abr-2026)
A12	1. RATIO_AUTOMÁTICO
C12	IFERROR(Cumplidos/Compromisos, 0) — genera alerta visual si brecha > umbral
A13	SAT_V_FLAG_MANUAL
C13	Flag manual del analista (ACTIVO/INACTIVO) — activar solo ante resolución formal CPCCS de brecha verificada
A14	NOTA Ci=0.50
B14	Ci=0.50 se aplica SOLO cuando SAT_V_FLAG="ACTIVO" — no por el ratio automático solo. El ratio puede tener falsos positivos por datos CPCCS incompletos.
A16	▌ ESTADO SAT-V
A17	SAT_V_Estado
A19	▌ DIAGNÓSTICO PREVENTIVO SAT-V
A21	✔ CHECKPOINT H24b — 2 puntos
B21	1. Nombre hoja y celdas dicen "Alerta de Brecha CPCCS" — NO "Desacato"
B22	2. Diagnóstico dice "Fortalecer seguimiento" (preventivo)
```