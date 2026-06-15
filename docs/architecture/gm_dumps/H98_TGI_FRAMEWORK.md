# H98_TGI_FRAMEWORK — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=60 · pobladas=50 · fórmulas=18
inputs(lee de): H01_PARÁMETROS, H07b_Ti_INVERSIÓN_eSIGEF, H99_ENGINE_CORE
outputs(alimenta a): H00_ÍNDICE, H36c_OBSIDIAN_MAP, H73_OUTPUT_API

## FÓRMULAS
```
D20	=H01_PARÁMETROS!B180
E20	=C20*D20
D21	=H01_PARÁMETROS!B15*100
E21	=C21*D21
D22	=H07b_Ti_INVERSIÓN_eSIGEF!B18*100
E22	=C22*D22
D23	=MIN(100,AVERAGE(H99_ENGINE_CORE!J8:J13))
E23	=C23*D23
D24	=H01_PARÁMETROS!B12*100
E24	=C24*D24
B25	=C20*D20+C21*D21+C22*D22+C23*D23+C24*D24
B35	=B25
B36	=SI(B35>=85,"🔵 Excelencia Territorial",SI(B35>=75,"🟢 Gobernanza Inteligente",SI(B35>=65,"🟡 Transición con Riesgos",SI(B35>=50,"🟠 Inequidad Estructural","🔴 Emergencia Territorial"))))
B37	=H99_ENGINE_CORE!B16
B38	=H01_PARÁMETROS!B15*100
B39	=H99_ENGINE_CORE!B23
B40	=H99_ENGINE_CORE!B20
B42	=B41-B35
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️  QUIRA Gov · Powered by Dylus Lab · Territorial Governance Intelligence
E1	H98_TGI_FRAMEWORK
A2	H98 — TGI FRAMEWORK CANÓNICO v1.0 — QUIRA Gov · GADM Montecristi 2026
A3	Gobernar con evidencia · Decidir con territorio · No medir solo cuánto se gastó — medir si transformó el territorio
A5	▌ 1. DEFINICIÓN CANÓNICA TGI
A6	TGI
B6	Territorial Governance Intelligence — sistema que transforma información fragmentada del Estado (normativa, planificación, ejecución presupuestaria y realidad territorial) en señales accionables de gobernanza basada en evidencia, alineando mandato político, inversión pública y transformación real del territorio.
A7	Categoría
B7	Nueva categoría de inteligencia pública — no es BI, no es GovTech genérico → es Territorial Governance Intelligence
A8	Diferencia clave
B8	TGI pregunta: ¿La inversión ejecutada llegó donde el territorio más lo necesitaba? No solo ¿Cuánto se gastó?
A10	▌ 2. LAS 5 CAPAS TGI — ARQUITECTURA OFICIAL
A11	Capa
B11	Qué mide
C11	Pregunta clave
D11	Donde vive (Excel)
E11	Estado
A12	1. Normativa
B12	Coherencia legal del acto de gobierno
C12	¿La decisión es legalmente válida?
D12	H01_PARÁMETROS · SCHEMA_REGLAS · H_ORGANICO
E12	✅ Sólida
A13	2. Planificación
B13	Fidelidad entre lo planificado y lo ejecutado
C13	¿Lo que se hace estaba en el PDOT?
D13	H04_PDOT · SCHEMA_METAS · H03_CNE
E13	✅ Sólida
A14	3. Ejecución
B14	Grado de ejecución real vs planificación financiera
C14	¿Lo planificado se ejecutó en tiempo y forma?
D14	H07_eSIGEF · H05_POA · H12_ICPI · H12b_ACUMULADO
E14	🔄 En progreso
A15	4. Territorial
B15	Distribución equitativa de la inversión en el territorio
C15	¿La inversión llegó donde más se necesitaba?
D15	H99_ENGINE_CORE · SCHEMA_ECIAP · SCHEMA_NBI
E15	🔄 Consolidando
A16	5. Inteligencia
B16	Patrones, alertas y recomendaciones de acción
C16	¿Qué debe hacer el alcalde mañana?
D16	Sentinel-TGI · H98 (esta hoja) · H37_SENSIBILIDAD
E16	🔄 Construyendo
A18	▌ 3. TGI SCORE — ÍNDICE MAESTRO CANTONAL v1.0
A19	Componente
B19	Variable
C19	Peso
D19	Valor_Actual
E19	Contribucion
F19	Fuente_Excel
A20	D1 — Legalidad y Coherencia
B20	Trust_Score_Metodológico = calidad metodológica del proceso normativo
C20	0.2
F20	H01_PARÁMETROS!B180 (% directo · valor actual: 83.5)
A21	D2 — Fidelidad de Planificación
B21	ICPI_Real_2025 × 100 = ejecución ponderada metas PDOT (decimal → %)
C21	0.2
F21	H01_PARÁMETROS!B15 (×100 · valor actual: 69.93)
A22	D3 — Ejecución Presupuestaria
B22	Ti_Inversión_2025 × 100 = devengado/codificado ENTE-01 grupos 7+8
C22	0.25
F22	H07b_Ti_INVERSIÓN_eSIGEF!B18 (×100 · valor actual: 59.85)
A23	D4 — Equidad Territorial
B23	IET_Rural_Avg = AVERAGE IET_Local_Pct parroquias rurales P02-P07 · cap 100
C23	0.25
F23	H99_ENGINE_CORE!J8:J13 → MIN(100, AVERAGE) · calculado dinámicamente
A24	D5 — Capacidad Institucional
B24	ICM_SNP_SIGAD × 100 = cumplimiento reporte al Sistema Nacional de Planificación
C24	0.1
F24	H01_PARÁMETROS!B12 (×100 · valor actual: 100.0)
A25	TGI_SCORE_GLOBAL_5D
C25	← TGI cantonal Montecristi 2026 (5 dimensiones)
A26	▌ 4. CLASIFICACIÓN TGI
A27	Rango
B27	Nivel
C27	Símbolo
D27	Implicación para el GADM
E27	Acceso a Cooperación
A28	85 – 100
B28	Excelencia Territorial
C28	🔵
D28	Gobernanza ejemplar — inversión equitativa y eficiente
E28	Acceso pleno BID/CAF/GCF/UE — referente nacional
A29	75 – 84
B29	Gobernanza Inteligente
C29	🟢
D29	Alta calidad — brechas territoriales marginales
E29	CAF · GIZ · USAID · BEI — elegibilidad total
A30	65 – 74
B30	Transición con Riesgos
C30	🟡
D30	Gestión correcta pero desequilibrios identificados
E30	CAF · BEI directos — GIZ/USAID con condiciones
A31	50 – 64
B31	Inequidad Estructural
C31	🟠
D31	Inversión no llega al territorio correcto — alerta
E31	Solo CAF/BEI proyectos existentes
A32	< 50
B32	Emergencia Territorial
C32	🔴
D32	Crisis de gobernanza — intervención urgente requerida
E32	Acceso bloqueado — plan de recuperación obligatorio
A34	▌ 5. POSICIÓN ACTUAL — GADM MONTECRISTI 2026
A35	TGI_Score_Actual
A36	TGI_Clasificacion
A37	IRS_Global (regresividad)
C37	← Meta 2027: ≤ 45
A38	ICPI_Real_2025
A39	NBI_Rural_Prom
A40	Parroquia_Más_Vulnerable
A41	TGI_Meta_2027
B41	60
A42	TGI_Brecha_a_Meta
C42	← positivo = puntos que faltan para la meta
A44	▌ 6. HOJA DE RUTA TGI 2026 → 2027
A45	Período
B45	Objetivo
C45	Acción Concreta
D45	Responsable
E45	KPI/Resultado
A46	Q2-2026
B46	Reducir brecha IRS rural
C46	Rebalancear inversión: +20% hacia parroquias rurales con CN > 0.40
D46	Dirs. Obras Públicas + Planificación
E46	IRS → 65
A47	Q3-2026
B47	ICPI → 73%
C47	Ejecutar 2-3 metas adicionales en ejecución parcial
D47	Todas las direcciones
E47	ICPI > 70% → acceso FIGL 2da ronda
A48	Q4-2026
B48	Cerrar PDOT metas críticas
C48	Isabel Muentes: agua + saneamiento + vialidad
D48	DAPS + Obras Públicas
E48	Cobertura agua Isabel Muentes > 50%
A49	Q1-2027
B49	TGI = 55
C49	Consolidar equidad territorial — nueva inversión por necesidad
D49	Alcaldía + Planificación
E49	Elegibilidad GIZ + USAID plena
A50	Q4-2027
B50	TGI = 60
C50	Cierre PDyOT — TGI Transición con Riesgos certificado
D50	Todo el GADM
E50	Benchmark municipal Ecuador
A52	QUIRA Gov v5.0 · Territorial Governance Intelligence (TGI) Framework · Dylus Lab © 2026
A53	Gobernar con evidencia · Decidir con territorio · El negocio no está en dashboards — está en datos territoriales confiables
A58	▌ NOTA METODOLÓGICA — DIFERENCIACIÓN PARROQUIAL TGI 5D
B59	D1 (Legalidad), D2 (Planificación), D3 (Ejecución) y D5 (Capacidad) son métricas CANTONALES — mismas para todas las parroquias. D4 (Equidad = MIN(100, IET_Local)) es el ÚNICO diferenciador territorial real. Esto es correcto: la gestión institucional se evalúa a nivel cantonal; la equidad territorial se evalúa a nivel parroquial. El TGI_Score_5D por parroquia refleja cómo la política cantonal se materializa o no en cada territorio.
A60	Columnas H99
B60	T=D1_Legalidad · U=D2_Planificación · V=D3_Ejecución · W=D4_Equidad(var) · X=D5_Capacidad · Y=TGI_Score_5D
```