# H36_QUIRA_BRIDGE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=56 · pobladas=53 · fórmulas=3
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H36_QUIRA_BRIDGE
A2	H36 — SIAP-ICPI BRIDGE — PUENTE HACIA SISTEMAS EXTERNOS
A3	Mapa de conectores para la futura implementación digital. Indica qué hojas se convertirán en tablas de la base de datos relacional.
A5	▌ MAPA DE TABLAS (58 hojas = 58 tablas BD)
A6	Hoja_Excel
B6	Tabla_BD
C6	Clave_Primaria
D6	Relaciones_FK
E6	Formato_Exportación
A7	H01_PARÁMETROS
B7	tb_parametros
C7	param_key
D7	—
E7	JSON config
A8	H04_S2_PLANIFICACIÓN_PDOT
B8	tb_metas
C8	id_meta
D8	—
E8	CSV
A9	H05_S3_COMPETENCIAS_COOTAD
B9	tb_competencias
C9	id_competencia
D9	id_meta→tb_metas
E9	CSV
A10	H07_S5_FINANCIERO_eSIGEF
B10	tb_financiero
C10	id_meta, año
D10	id_meta→tb_metas
E10	CSV
A11	H10_S8_PARTICIPACIÓN_CPCCS
B11	tb_cpccs
C11	id_compromiso
D11	—
E11	JSON
A12	H11_S9_AGENDA_GLOBAL_ODS
B12	tb_ods
C12	id_meta, id_ods
D12	id_meta→tb_metas
E12	CSV
A13	H12_MOTOR_ICPI_CANÓNICO
B13	tb_icpi_motor
C13	id_meta, año
D13	id_meta→tb_metas
E13	JSON
A14	H13_S6_VERIFICACIÓN
B14	tb_verificacion
C14	id_meta, año
D14	id_meta→tb_metas
E14	JSON
A15	H14_PONDERADORES
B15	tb_ponderadores
C15	id_meta
D15	id_meta→tb_metas
E15	CSV
A16	H15_ICPI_GLOBAL
B16	tb_icpi_global
C16	año
D16	—
E16	JSON
A17	H16_IFE
B17	tb_ife
C17	año
D17	—
E17	JSON
A18	H17_IED
B18	tb_ied
C18	id_direccion, año
D18	—
E18	JSON
A19	H18_ITAM
B19	tb_itam
C19	año
D19	—
E19	JSON
A20	H19_ICS_ISP
B20	tb_isp
C20	año
D20	—
E20	JSON
A21	H20_ICODS
B21	tb_icods
C21	año
D21	—
E21	JSON
A22	H20b_IGP_GOBERNANZA_PARTIC
B22	tb_igp
C22	año
D22	—
E22	JSON
A23	H20c_IEF_EFICIENCIA_FINANCIERA
B23	tb_ief
C23	año
D23	—
E23	JSON
A24	H21b_SAT-0_COHERENCIA_PAC
B24	tb_sat0
C24	año
D24	—
E24	JSON
A25	H21_SAT-I
B25	tb_sat1
C25	año
D25	—
E25	JSON
A26	H22_SAT-II
B26	tb_sat2
C26	año
D26	—
E26	JSON
A27	H23_SAT-III
B27	tb_sat3
C27	año
D27	—
E27	JSON
A28	H24_SAT-IV
B28	tb_sat4
C28	año
D28	—
E28	JSON
A29	H24b_SAT-V_ALERTA_CPCCS
B29	tb_sat5
C29	año
D29	—
E29	JSON
A30	H24c_SAT-VI_DESVÍO_PP
B30	tb_sat6
C30	año
D30	—
E30	JSON
A31	H25_MMP_MENSUAL
B31	tb_mmp_mensual
C31	id_meta, mes, año
D31	id_meta→tb_metas
E31	CSV
A32	H26_MMP_TRIMESTRAL
B32	tb_mmp_trimestral
C32	id_meta, trimestre, año
D32	id_meta→tb_metas
E32	CSV
A33	H27_MMP_ANUAL
B33	tb_mmp_anual
C33	id_meta, año
D33	id_meta→tb_metas
E33	CSV
A34	H28_RESUMEN_EJECUTIVO
B34	tb_resumen_ejecutivo
C34	año
D34	—
E34	JSON
A35	H29_TABLERO_ALCALDE
B35	tb_tablero_alcalde
C35	año
D35	—
E35	JSON
A36	H30_IED_POR_DIRECCIÓN
B36	tb_ied_detalle
C36	id_direccion, año
D36	id_direccion→tb_ied
E36	JSON
A37	H31_REPORTE_CPCCS
B37	tb_reporte_cpccs
C37	año
D37	—
E37	PDF/JSON
A38	H32_REPORTE_ODS_BILATERALES
B38	tb_reporte_ods
C38	año
D38	—
E38	PDF/JSON
A39	H33_TAC_QUIRA_CIUDADANA
B39	tb_tac
C39	año
D39	—
E39	JSON/HTML
A40	H34_CERTIFICADO_QUIRA
B40	tb_certificado
C40	año
D40	—
E40	PDF
A41	H34b_MFN_FIDELIDAD_NARRATIVA
B41	tb_mfn
C41	id_mfn
D41	id_ente→tb_entes
E41	JSON
A42	H35_DATASET_ACADEMIA
B42	tb_dataset_academia
C42	id_meta, año
D42	id_meta→tb_metas
E42	CSV/JSON
A43	H36_QUIRA_BRIDGE
B43	tb_bridge
C43	endpoint_id
D43	—
E43	JSON
A44	H36b_LOOKUP_ARRASTRE
B44	tb_arrastre
C44	id_registro
D44	id_ente→tb_entes
E44	JSON
A47	▌ API ENDPOINTS SUGERIDOS (próxima versión SIAP-ICPI 2.0)
A48	Endpoint
B48	Método
C48	Fuente
D48	Descripción
A49	/api/icpi/current
B49	GET
C49	H12!B33
D49	ICPI vigente del sistema
A50	/api/metas
B50	GET
C50	H04
D50	Lista de 25 metas PDOT
A51	/api/arrastre
B51	GET
C51	H36b
D51	Histórico entidades 2023-2025
A52	/api/sat/status
B52	GET
C52	H21b-H24c
D52	Estado de las 7 señales SAT
A53	/api/ied
B53	GET
C53	H17
D53	IED por dirección
A54	/api/mmp/mensual
B54	GET
C54	H25
D54	Avance mensual por meta
A55	/api/certificado
B55	GET
C55	H34
D55	Estado del Certificado QUIRA
A56	/api/ods
B56	GET
C56	H20
D56	ICODS y cobertura ODS
```