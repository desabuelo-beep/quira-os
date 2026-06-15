# H21_SAT-I — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=31 · pobladas=25 · fórmulas=18
inputs(lee de): H01_PARÁMETROS, H08_S6_AUTOREPORTE_SIGAD, H12_MOTOR_ICPI_CANÓNICO, H25_MMP_MENSUAL
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE, H01, H08

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B49
B7	=H01_PARÁMETROS!B50
B8	=H08_S6_AUTOREPORTE_SIGAD!B7
B9	=IFERROR(H08_S6_AUTOREPORTE_SIGAD!B8/H01_PARÁMETROS!B18,0)
C9	=H08!B8 / H01!B18 (Total_Metas_PDOT=25). CORRECIÓN S-02: B18=25 metas, NO B15=ICPI_Axioma
B13	=IF(H08_S6_AUTOREPORTE_SIGAD!B7>=H01_PARÁMETROS!B49,"⚠️ Alta calificación detectada","✅ Normal")
B14	=IF(IFERROR(H08_S6_AUTOREPORTE_SIGAD!B8/H01_PARÁMETROS!B18,0)<=H01_PARÁMETROS!B50,"⚠️ Cobertura parcial","✅ Cobertura adecuada")
B15	=IF(AND(H08_S6_AUTOREPORTE_SIGAD!B7>=H01_PARÁMETROS!B49,IFERROR(H08_S6_AUTOREPORTE_SIGAD!B8/H01_PARÁMETROS!B18,0)<=H01_PARÁMETROS!B50),"⚠️ SAT-I ACTIVO","✅ Sin señal SAT-I")
B17	=IF(AND(H08_S6_AUTOREPORTE_SIGAD!B7>=H01_PARÁMETROS!B49,IFERROR(H08_S6_AUTOREPORTE_SIGAD!B8/H01_PARÁMETROS!B18,0)<=H01_PARÁMETROS!B50),"Alta calificación con cobertura parcial de metas. Ampliar el universo de reporte para fortalecer la trazabilidad de la gestión. Ref: COPFP Art.54.","Alta calificación sobre universo completo de metas. Sin señales de fragmentación selectiva.")
B20	=H08_S6_AUTOREPORTE_SIGAD!B7
B21	=H08_S6_AUTOREPORTE_SIGAD!B8
B22	=H01_PARÁMETROS!B18
B23	=IFERROR(B21/B22,0)
B30	=IFERROR(H25_MMP_MENSUAL!W38,0)
B31	=COUNTIF(H25_MMP_MENSUAL!W11:W35,"<0.85")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H21_SAT-I
A2	H21 — SAT-I — FRAGMENTACIÓN SELECTIVA
A3	Detecta alta calificación SIGAD con cobertura parcial de metas. Condición: ICM ≥ 80% Y metas reportadas/total ≤ 10%. Fundamentación: COPFP Art.54.
A5	▌ PARÁMETROS SAT-I
A6	SAT_I_Umbral_ICM
C6	ICM mínimo para activar fragmentación (H01!B49=80%)
A7	SAT_I_Umbral_Universo
C7	Porcentaje máximo cobertura parcial (H01!B50=10%)
A8	ICM_Global_SIGAD
C8	Leído dinámicamente de H08!B7
A9	Pct_Metas_Reportadas
A11	▌ ESTADO SAT-I
A12	Condición
B12	Evaluación
C12	Descripción
A13	Cond_1: ICM >= Umbral_ICM
C13	Comparación numérica directa H08!B7 vs H01!B43 — FALLA 15 prevenida
A14	Cond_2: Pct_Metas <= Umbral_Universo
C14	Comparación numérica directa. CORRECIÓN S-02: B18=25 metas totales PDOT
A15	SAT-I_Estado
C15	★ FALLA 15: comparación NUMÉRICA DIRECTA — NO compara texto de B13/B14
A17	▌ DIAGNÓSTICO PREVENTIVO SAT-I
A19	▌ VALORES ACTUALES
A20	ICM_SIGAD actual
A21	H08!B8 (metas reportadas)
A22	Total metas PDOT (H01!B18)
A23	Pct_Universo calculado
A25	✔ CHECKPOINT H21 — 3 puntos
B25	1. Diagnóstico dice "Ampliar el universo de reporte" (preventivo) — NO "posible omisión selectiva"
B26	2. Umbrales referencian H01!B43 y H01!B44
B27	3. Fórmulas B15 y B17 usan comparaciones NUMÉRICAS DIRECTAS vs H08/H01 — FALLA 15 prevenida
A29	⚡ PULSO Vi_SINÁPTICO SIAP-ICPI — CONEXIÓN H25
A30	Vi_Sin_Promedio
C30	Vi promedio sináptico de las 25 metas (umbral crítico 0.85)
A31	Metas_Vi_Baja
C31	Metas con Vi < 0.85 → dispara alerta SAT-VII en H75
```