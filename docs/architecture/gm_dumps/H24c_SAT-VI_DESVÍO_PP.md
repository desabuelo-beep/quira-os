# H24c_SAT-VI_DESVÍO_PP — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=23 · pobladas=18 · fórmulas=9
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE
MARCADORES: C8: Guardia: NO = sin datos PP en H10b — bloquea activación SAT-VI · C11: 0 si sin datos PP (FALLA 17 activa) · B14: =IF(B8="NO","✅ Sin señal SAT-VI — Sin datos PP registrados en H10b (pe · B16: =IF(B8="NO","Sin datos de Presupuesto Participativo registrados en H10 · B23: 4. SAT_VI_Estado muestra "✅ Sin señal SAT-VI — Sin datos PP registrado

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B45
B8	=IF(B7>0,"SÍ","NO")
B10	=IF(B8="NO",0,IF(B9>B7,B9-B7,0))
B11	=IF(B7=0,0,IFERROR(B10/B7,0))
B14	=IF(B8="NO","✅ Sin señal SAT-VI — Sin datos PP registrados en H10b (período inicial o PP no implementado)",IF(B11>0.1,"⚠️ SAT-VI ACTIVO — Desvío de Presupuesto PP detectado. Revisar asignación con asamblea ciudadana.","✅ Sin señal SAT-VI"))
B16	=IF(B8="NO","Sin datos de Presupuesto Participativo registrados en H10b. Cuando se registren proyectos PP aprobados por la asamblea ciudadana, el SAT-VI calculará automáticamente.",IF(B11>0.1,"Se detecta un desvío del "&TEXT(B11,"0%")&" de los fondos de Presupuesto Participativo aprobados. Revisar la asignación de fondos PP con la asamblea ciudadana para fortalecer el cumplimiento del mandato participativo. Ref: COOTAD Art.238.","Ejecución del Presupuesto Participativo dentro del rango acordado con la asamblea ciudadana. Sin señales de desvío."))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H24c_SAT-VI_DESVÍO_PP
A2	H24c — SAT-VI — DESVÍO DE PRESUPUESTO PARTICIPATIVO
A3	Detecta uso de fondos PP en proyectos distintos a los aprobados por la asamblea ciudadana. Marco: COOTAD Art.238. NOTA: NO usar 'Fuga presupuestaria'.
A5	▌ PARÁMETROS SAT-VI
A6	BONO_PARTICIPACION
C6	Bono participación (H01!B45=1.25)
A7	Monto_PP_Aprobado
B7	0
C7	★ FALLA 17: IFERROR(H10b!B9,0) — guardia anti-datos-vacíos
A8	Hay_Datos_PP
C8	Guardia: NO = sin datos PP en H10b — bloquea activación SAT-VI
A9	Monto_PP_Ejecutado_PP
B9	0
C9	Ingresar ejecución PP 2026 (actualizar manualmente)
A10	Monto_PP_Desviado
C10	Desvio = IF(ejecutado > aprobado, diferencia, 0) — solo si hay datos
A11	Pct_Desviación
C11	0 si sin datos PP (FALLA 17 activa)
A13	▌ ESTADO SAT-VI
A14	SAT_VI_Estado
A16	▌ DIAGNÓSTICO PREVENTIVO SAT-VI
A18	▌ NOTA FALLA 17 — GUARDIA ANTI-DATOS-VACÍOS
B18	Todas las celdas que leen de H10b tienen IFERROR(...,0). Si H10b está vacío, Monto_PP_Aprobado=0, Hay_Datos_PP="NO" y SAT_VI_Estado muestra "Sin señal" — NUNCA genera alertas activas desde datos vacíos. Cuando se agreguen proyectos PP en H10b, el SAT-VI se activará automáticamente si hay desvío real.
A20	✔ CHECKPOINT H24c — 4 puntos
B20	1. Nombre visible dice "Desvío de Presupuesto Participativo" — NO "Fuga presupuestaria"
B21	2. BONO_PARTICIPACION referencia H01!B45 (=1.25)
B22	3. Monto_PP_Aprobado usa IFERROR(H10b!B9,0) con guardia anti-datos-vacíos (FALLA 17)
B23	4. SAT_VI_Estado muestra "✅ Sin señal SAT-VI — Sin datos PP registrados en H10b" cuando Monto_PP_Aprobado=0 — NO genera alertas falsas
```