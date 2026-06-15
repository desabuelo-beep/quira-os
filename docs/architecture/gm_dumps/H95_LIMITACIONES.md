# H95_LIMITACIONES — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=16 · pobladas=15 · fórmulas=0
inputs(lee de): —
outputs(alimenta a): H00_ÍNDICE
MARCADORES: C13: D1 (Trust_Score=83.5) es una evaluación metodológica interna (Dylus La · E13: v5.3: someter Trust_Score a revisión externa por par académico o consu

## FÓRMULAS
```
(sin fórmulas)
```

## ETIQUETAS / DATOS (tope 600)
```
A1	H95 — LIMITACIONES METODOLÓGICAS · SIAP-ICPI v5.3 TGI · GADM Montecristi 2026
A2	Registro transparente de limitaciones del modelo. Requerido para credibilidad ante cooperantes, pares académicos y auditoría gubernamental. Una limitación declarada es una fortaleza metodológica.
A4	ID
B4	Categoría
C4	Limitación
D4	Impacto / Riesgo
E4	Plan de Mejora (v5.x+)
A5	L-01
B5	Granularidad
C5	D1 (Legalidad), D2 (Planificación), D3 (Ejecución) y D5 (Capacidad) son métricas CANTONALES — el mismo valor para todas las parroquias. Solo D4 (Equidad=IET_Local) varía por parroquia.
D5	El TGI_Score_5D por parroquia refleja únicamente la inequidad de inversión (D4×25%). Las otras 4 dimensiones no diferencian el desempeño intraparroquial.
E5	v5.3: desagregar D3 (Ejecución) por parroquia usando eSIGEF georeferenciado cuando esté disponible
A6	L-02
B6	Granularidad
C6	Inv_Total_Q1 por parroquia es una estimación territorial basada en códigos de proyecto y localización. eSIGEF no tiene georreferenciación nativa a nivel parroquial.
D6	Error de asignación estimado en ±15-20% para proyectos multi-parroquiales o cantonales.
E6	v5.4: cruzar con SERCOP (código CPC + localización geográfica) para mejorar asignación
A7	L-03
B7	Granularidad
C7	Cobertura_Agua_Pct (col F) usa dato censal 2022 para algunos sectores y datos administrativos GADM para otros. Metodología de homologación no está 100% documentada.
D7	Posible subvaloración de cobertura en sectores con inversión post-censal (CAF/BEI 2024-2026).
E7	v5.3: actualizar con encuesta rápida DAPS 2026 para parroquias con proyectos activos
A8	L-04
B8	Temporalidad
C8	D3 (Ti_Ejecución) usa dato de cierre 2025 (59.85%), no el avance Q1-2026 (1.05%). El Ti_2026 Q1 es artificialmente bajo (solo 2 meses de ejecución anual).
D8	D3 subestima la velocidad real de ejecución 2026 si se compara con año completo 2025.
E8	v5.3: añadir selector de año en H01 para elegir entre Ti_2025 (anual) y Ti_2026 (parcial)
A9	L-05
B9	Temporalidad
C9	Población_2022 (Censo INEC) puede tener desfase para parroquias con migración alta (ej. La Pila, Isabel Muentes). Proyecciones intercensales no aplicadas.
D9	IET_Local podría estar subestimado en parroquias con emigración post-2022 (denominador de población más alto que el real).
E9	v5.4: aplicar proyecciones INEC 2024-2026 cuando estén disponibles
A10	L-06
B10	Temporalidad
C10	TGI_Score_5D es un snapshot de Q1-2026. No captura aceleración de ejecución en Q2-Q4 (donde históricamente se concentra el 70-80% del gasto municipal).
D10	El TGI calculado en mayo subestima el desempeño anual real. Comparación interanual directa no es válida sin normalizar el período.
E10	v5.3: agregar factor de ajuste estacional basado en tendencia 2023-2025
A11	L-07
B11	Metodológica
C11	Los pesos de las 5 dimensiones (20/20/25/25/10) son definidos por criterio experto (Dylus Lab), no por análisis de componentes principales (PCA) o regresión sobre resultados.
D11	Sensibilidad: cambio de ±5pp en cualquier peso cambia el TGI_Score en ±0.5-1.5 puntos. Rango de incertidumbre estimado: ±3 puntos sobre el score final.
E11	v5.4: calibrar pesos con análisis de sensibilidad Monte Carlo sobre datos históricos 2023-2025
A12	L-08
B12	Metodológica
C12	IRS_Global = -CORREL(NBI, Inv_PerCapita) usando solo 7 parroquias. La correlación de Pearson con n=7 tiene intervalos de confianza amplios (±0.35).
D12	IRS puede variar significativamente con pequeños cambios en la inversión de Montecristi urbana. No es estadísticamente robusto con n=7.
E12	v5.4: complementar con ranking de Spearman y calcular IC 95% para IRS
A13	L-09
B13	Metodológica
C13	D1 (Trust_Score=83.5) es una evaluación metodológica interna (Dylus Lab), no verificada externamente por Contraloría o auditor independiente.
D13	Riesgo de sesgo de confirmación en la autoevaluación metodológica. No es comparable con evaluaciones externas estándar.
E13	v5.3: someter Trust_Score a revisión externa por par académico o consultor independiente
A14	L-10
B14	Metodológica
C14	Composite_Need v2.1 usa pesos 0.45/0.30/0.25 (NBI/Agua/Pob). No incluye variables de acceso vial, educación o salud.
D14	CN puede subestimar la necesidad real de parroquias con buena agua pero mal acceso vial o bajo logro educativo.
E14	v5.4: ampliar CN a 5 variables cuando haya datos actualizados post-2022
A15	L-11
B15	Fuentes
C15	eSIGEF no desagrega automáticamente inversión por parroquia. La asignación territorial es manual/semestimada por el equipo técnico GADM.
D15	Margen de error en H7:H13 (Inv_Total_Q1) estimado en ±10-20% para proyectos con beneficio difuso (vialidad cantonal, gestión de riesgos).
E15	v5.3: desarrollar protocolo de asignación territorial con código de proyecto SERCOP+mapa
A16	L-12
B16	Fuentes
C16	ICPI_Real_2025 = 69.93% incluye intangibles (metas normativas, planes) con Ti_Verificado de informe. No hay auditoría externa de los informes usados.
D16	Riesgo de sobrevaloración de ICPI si informes de ejecución no reflejan el producto real. Sin contraverificación física para metas intangibles.
E16	v5.3: implementar muestra de verificación campo para 20% de metas intangibles por año
```