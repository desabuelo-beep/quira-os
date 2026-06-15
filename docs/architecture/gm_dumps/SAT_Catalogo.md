# SAT_Catalogo — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=31 · pobladas=26 · fórmulas=5
inputs(lee de): H73_OUTPUT_API, H75_SAT_ENGINE
outputs(alimenta a): —
MARCADORES: E8: Las reformas presupuestarias deben justificarse y registrarse en eSIGE · N11: Pipeline CPCCS en Sprint 1 captura score_total y n_informe_cpccs. Comp

## FÓRMULAS
```
C19	=H75_SAT_ENGINE!B12
C20	=H75_SAT_ENGINE!B13
C21	=H75_SAT_ENGINE!B14
C22	=H73_OUTPUT_API!B2
C23	=H73_OUTPUT_API!B4
```

## ETIQUETAS / DATOS (tope 600)
```
A1	SAT_Catalogo — QUIRA OS Sprint 2 | Puente Q1-Pipeline → Motor SAT Gold Master
A2	Generado: 2026-05-25  |  Gold Master: SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518  |  Motor SAT: H75_SAT_ENGINE  |  Quira Layer: Q1  |  Dylus Lab © 2026
A3	DOCTRINA: Esta hoja NO modifica el motor matemático. Define el triple ancla (Legal + Operativa + Doctrinal QUIRA) y mapea cada SAT al campo del pipeline Q1 que la alimenta.
A5	CODIGO SAT
B5	NOMBRE ALERTA
C5	DIM
TGI
D5	BASE LEGAL
(Artículo)
E5	BASE LEGAL
(Descripción)
F5	BASE OPERATIVA
(Métrica Observable)
G5	BASE DOCTRINAL QUIRA
H5	FUENTE
PIPELINE
I5	CAMPO JSON
(Snapshot Q1)
J5	UMBRAL
ACTIVACIÓN
K5	PESO
SEV.
L5	TIPO
M5	REFERENCIA
GOLD MASTER
N5	NOTAS OPERATIVAS
A6	SAT-0
B6	Coherencia POA-PAC
C6	D2
D6	LOSNCP Art. 22
E6	Obliga a que el PAC refleje los procesos de contratación previstos en el POA institucional.
F6	pac_publicado = false  O  brecha POA-PAC > 20%
G6	D2-Planificación: ausencia de coherencia entre planificación operativa y contratación.
H6	sercop
I6	contratacion.pac_publicado / contratacion.brecha_poa_pac
J6	pac_publicado = False  O  brecha > 20%
K6	0.2
L6	PREVENTIVA
M6	H75_SAT_ENGINE + H21b_SAT-0
N6	Si pac_publicado=False → alerta directa. Si True → evaluar brecha monto POA vs monto PAC.
A7	SAT-I
B7	Fragmentacion Selectiva
C7	D3
D7	COPFP Art. 54
E7	Las entidades deben reportar avances de todas las metas del plan operativo en el SIGAD.
F7	ICM_Global >= 80% AND pct_metas_reportadas <= 10%
G7	D3-Ejecución: calificación alta con universo de metas mínimo es señal de fragmentación.
H7	dpe
I7	financiero.icm_global / financiero.pct_metas_reportadas
J7	ICM >= 0.80 AND cobertura_metas <= 0.10
K7	0.25
L7	CRITICA
M7	H75_SAT_ENGINE + H21_SAT-I
N7	Requiere ingesta SIGAD (H08). Pipeline DPE provee datos financieros; SIGAD requiere ingesta manual o CSV.
A8	SAT-II
B8	Reforma Significativa Tardia
C8	D2
D8	COPFP Art. 115 / Acuerdo MEF 067
E8	Las reformas presupuestarias deben justificarse y registrarse en eSIGEF. Reformas tardías indican falta de planificación.
F8	reformas_post_q2 = True AND monto_reforma / codificado_base > 5%
G8	D2-Planificación: reformas tardías evidencian planificación reactiva, no prospectiva.
H8	dpe
I8	financiero.reformas_presupuestarias / financiero.fecha_reforma
J8	monto_reforma > 5% codificado base Y fecha > 30-Jun
K8	0.15
L8	ALERTA
M8	H75_SAT_ENGINE + H22_SAT-II
N8	Pipeline DPE captura cédulas presupuestarias. Comparar codificado inicial vs reformado + fecha.
A9	SAT-III
B9	Paralisis Presupuestaria
C9	D3
D9	COPFP Art. 113
E9	Obliga a la evaluación periódica de la ejecución presupuestaria. Entidades deben alcanzar metas de ejecución por período.
F9	Ti_ejecucion < 60% antes del Q4  O  < 80% en cierre anual
G9	D3-Ejecución: ejecución menor al umbral por persistencia longitudinal = riesgo SAT-D3 crítico.
H9	dpe
I9	financiero.ejecucion_porcentaje / financiero.ti_devengado
J9	ejecucion_pct < 0.60 (Q3/Q4)  O  < 0.80 (cierre)
K9	0.2
L9	CRITICA
M9	H75_SAT_ENGINE + H23_SAT-III
N9	Caso Montecristi: ejecucion_observada = 59.85% es SAT-III activa (< 60%). CRITICO por persistencia.
A10	SAT-IV
B10	Alerta Fiscal COOTAD
C10	D3
D10	COOTAD Art. 192
E10	Los GAD deben destinar al menos el 65% del presupuesto de ingresos propios a inversión pública.
F10	inversion_pct < 65% del presupuesto codificado
G10	D3-Ejecución + D1-Legalidad: incumplimiento directo de mandato legal con magnitud medible.
H10	dpe
I10	financiero.inversion_porcentaje / financiero.gasto_corriente_pct
J10	inversion_pct < 0.65
K10	0.1
L10	LEGAL
M10	H75_SAT_ENGINE + H24_SAT-IV + H16_IFE
N10	Gold Master ISP_SALUD_PRESUP = 14.58% vs meta 65%. Brecha actual = 50.42%. ALERTA ACTIVA.
A11	SAT-V
B11	Brecha Compromiso CPCCS
C11	D5
D11	COOTAD Art. 302
E11	Los GAD deben realizar rendición de cuentas anual y cumplir los compromisos declarados ante la ciudadanía.
F11	1 - (compromisos_cumplidos / compromisos_total) > 30%
G11	D5-Capacidad Institucional: brecha compromiso-cumplimiento erosiona la credibilidad del GAD.
H11	cpccs
I11	accountability.rdc.componente_a.score / accountability.rdc.score_total
J11	brecha_compromisos > 0.30  O  score_total < 50
K11	0.05
L11	ALERTA
M11	H75_SAT_ENGINE + H24b_SAT-V_ALERTA_CPCCS + H10_S8_PARTICIPACIÓN_CPCCS
N11	Pipeline CPCCS en Sprint 1 captura score_total y n_informe_cpccs. Componente B (redes) es evidencia independiente.
A12	SAT-VI
B12	Desvio Presupuesto Participativo
C12	D4
D12	COOTAD Art. 238 / Reglamento PP
E12	El presupuesto participativo debe ejecutarse según lo acordado con la ciudadanía. Desvíos requieren justificación.
F12	abs(pp_ejecutado - pp_registrado) / pp_registrado > 20%
G12	D4-Equidad Territorial: PP es el mecanismo principal de inversión territorial equitativa.
H12	dpe
I12	financiero.pp_registrado / financiero.pp_ejecutado
J12	desvio_pct > 0.20
K12	0.05
L12	ALERTA
M12	H75_SAT_ENGINE + H24c_SAT-VI_DESVÍO_PP + H20b_IGP_GOBERNANZA_PARTIC
N12	Requiere campo PP en cédulas DPE. Actualmente pipeline captura ejecución total; PP requiere filtro por partida.
A13	SAT-VII
B13	Vi Sinaptico Pulso
C13	D3
D13	COPFP Art. 54 (referencial)
E13	Marco referencial: entidades deben reportar avances mensualmente en el SIGAD.
F13	promedio(Vi_metas_PDOT) < 0.85
G13	D3-Ejecución: pulso sináptico mide la vitalidad operativa del plan. Peso=0 → informacional.
H13	dpe
I13	financiero.vi_promedio_metas
J13	vi_promedio < 0.85 (INFORMACIONAL — peso=0)
K13	0
L13	INFORMACIONAL
M13	H75_SAT_ENGINE (peso=0, informacional)
N13	No contribuye al riesgo ponderado. Dashboard puede mostrarlo como indicador de pulso.
A14	SAT-VIII
B14	Equidad Territorial
C14	D4
D14	COOTAD Art. 249 (referencial)
E14	Marco referencial: los GAD deben garantizar equidad en la inversión territorial.
F14	IET_desviacion > 20% (urbano vs rural)
G14	D4-Equidad Territorial: IET mide el equilibrio de inversión en el territorio. Peso=0 → informacional.
H14	dpe
I14	territorial.iet_desviacion / territorial.inversion_urbana / territorial.inversion_rural
J14	iet_desviacion > 0.20 (INFORMACIONAL — peso=0)
K14	0
L14	INFORMACIONAL
M14	H75_SAT_ENGINE (peso=0, informacional) + H42_IET_EQUIDAD_TERRITORIAL
N14	Requiere datos geolocalizados de inversión. Phase 2+ cuando tengamos Q2 semántico.
A17	RESUMEN RIESGO SAT — Valores Live desde H75_SAT_ENGINE (Gold Master)
A18	MÉTRICA
B18	DESCRIPCIÓN
C18	VALOR GOLD MASTER
D18	FUENTE CELDA
A19	RIESGO_TOTAL
B19	Riesgo ponderado global SAT (0.0-1.0)
D19	H75_SAT_ENGINE!B12
A20	CLASIF_RIESGO
B20	Clasificación: BAJO/MEDIO/ALTO/CRITICO
D20	H75_SAT_ENGINE!B13
A21	SAT_ACTIVAS_COUNT
B21	N° de alertas SAT activas
D21	H75_SAT_ENGINE!B14
A22	ICPI_GLOBAL
B22	ICPI Global (H73 Output API) — 2026
D22	H73_OUTPUT_API!B2
A23	ICPI_CLASIFICACION
B23	Clasificación ICPI institucional
D23	H73_OUTPUT_API!B4
A26	LEYENDA — TIPOS DE ALERTA
A27	CRITICA
B27	Activa inmediatamente. Peso alto. Impacta directamente el RIESGO_TOTAL.
A28	LEGAL
B28	Incumplimiento normativo directo con artículo específico. Requiere acción inmediata.
A29	PREVENTIVA
B29	Señal temprana antes de incumplimiento. Permite acción correctiva proactiva.
A30	ALERTA
B30	Tendencia de riesgo. Monitoreo requerido. Puede escalar a CRITICA.
A31	INFORMACIONAL
B31	Peso=0 en riesgo ponderado. Enriquece el dashboard. No bloquea.
```