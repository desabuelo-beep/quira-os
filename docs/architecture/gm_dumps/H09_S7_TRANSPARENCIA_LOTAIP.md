# H09_S7_TRANSPARENCIA_LOTAIP — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=63 · pobladas=57 · fórmulas=8
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H18_ITAM, H76_AUDIT_TRAIL
refs no resueltas: #H00_ÍNDICE
MARCADORES: A3: Silo 7: Seguimiento al cumplimiento LOTAIP por meta PDOT. Fuente: DPE  · B8: Verificación trimestral DPE | Q1 (Ene-Mar 2026): cumplido ✓ | Q2-Q4: p · H34: 2026-Q2 (pendiente verificacion portal) · H35: 2026-Q2 (pendiente verificacion portal) · H36: 2026-Q2 (pendiente verificacion portal) · H37: 2026-Q2 (pendiente verificacion portal) · G39: Información social: calidad pendiente · H39: 2026-Q2 (pendiente verificacion portal) · H41: 2026-Q2 (pendiente verificacion portal) · H42: 2026-Q2 (pendiente verificacion portal) · H43: 2026-Q2 (pendiente verificacion portal) · G44: Indicador derivado: validación pendiente · H44: 2026-Q2 (pendiente verificacion portal) · G45: Inventario no publicado aún — pendiente · H45: 2026-Q2 (pendiente verificacion portal) · H47: 2026-Q2 (pendiente verificacion portal) · H48: 2026-Q2 (pendiente verificacion portal) · H49: 2026-Q2 (pendiente verificacion portal) · H50: 2026-Q2 (pendiente verificacion portal) · H51: 2026-Q2 (pendiente verificacion portal) · H52: 2026-Q2 (pendiente verificacion portal) · H53: 2026-Q2 (pendiente verificacion portal) · H54: 2026-Q2 (pendiente verificacion portal)

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE")
E1	=IFERROR("ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"%","—")
F1	=TODAY()
B6	=H01_PARÁMETROS!B13
D56	=AVERAGE(D30:D54)
E56	=AVERAGE(E30:E54)
F56	=AVERAGE(F30:F54)
B59	="V_LOTAIP promedio: "&TEXT(IFERROR(AVERAGE(G30:G54),0),"0.00")&" | Metas con V=1.0: "&COUNTIF(G30:G54,1)&" | Metas con V=0: "&COUNTIF(G30:G54,0)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H09_S7_TRANSPARENCIA_LOTAIP
A2	H09 — S7 LOTAIP/TRANSPARENCIA — Índice de Cumplimiento
A3	Silo 7: Seguimiento al cumplimiento LOTAIP por meta PDOT. Fuente: DPE 2025 (100/100) + 3 meses 2026 cargados. Calidad de contenido: pendiente de constatación.
A5	▌ PARÁMETROS S7
A6	Año_LOTAIP
A7	Fuente_2025
B7	DPE — Dirección Provincial de Empoderamiento | Resultado: 100/100
A8	Fuente_2026
B8	Verificación trimestral DPE | Q1 (Ene-Mar 2026): cumplido ✓ | Q2-Q4: pendiente
A9	Nota_Calidad
B9	★ Calidad de contenido no constatada. Score refleja DISPONIBILIDAD de información, no COMPLETITUD metodológica.
A10	SCORE_UMBRAL
B10	0.9
C10	≥0.90 = transparente (información accesible y publicada)
A11	Valor
B11	Criterio
A12	▌ ESCALA SCORE LOTAIP
B12	Documento en URL pública del GAD — accesible y verificable
A13	Score
B13	Significado
A14	0
B14	Sin URL pública — algorítmicamente no existe
A16	▌ REFERENCIA — LITERALES LOTAIP Art.7 APLICABLES A GAD MUNICIPALES
A17	Literal
B17	Contenido
C17	Aplicación para metas QUIRA
A18	a)
B18	Estructura orgánica y funcional, base legal de creación
C18	Metas institucionales/orgánico
A19	d)
B19	Servicios que ofrece, incluyendo normas, políticas y protocolos
C19	Metas de servicio directo al ciudadano
A20	f)
B20	Relación de los procedimientos, tiempos y trámites
C20	Metas de modernización/trámites digitales
A21	k)
B21	Los planes y programas en ejecución con presupuestos, objetivos y resultados
C21	LITERAL PRINCIPAL — todas las metas PDOT con POA
A22	l)
B22	Listado de contrataciones realizadas con personas naturales o jurídicas
C22	Metas con procesos de contratación pública
A23	n)
B23	Vigencia de las contrataciones suscritas
C23	Metas con contratos activos
A24	o)
B24	Presupuesto ejecutado — plazos, cantidades y pagos
C24	Metas con ejecución presupuestaria verificable
A26	⚠️ FALLA 13 — REGLA LITERAL_LOTAIP:
B26	El literal LOTAIP registrado en H09 DEBE corresponder al literal REAL bajo el cual el documento está publicado en el portal de transparencia del GAD (https://montecristi.gob.ec/transparencia). Asignar erróneamente el literal hace que V_LOTAIP=1 no sea verificable. REGLA: si el literal asignado no coincide con el publicado en el portal, V_LOTAIP=0.5 como máximo hasta verificación.
A28	▌ REGISTRO LOTAIP 2026 — 25 METAS
A29	ID_Meta
B29	Sistema_Meta
C29	Descripción_LOTAIP
D29	Score_2025
E29	Score_2026_Q1
F29	Score_LOTAIP_2026
G29	Observación
H29	Fecha_Verificación
A30	SC-I-N-01
B30	DAPS-01
C30	Agua potable — Cédula, contratos y ejecución publicados
D30	0.98
E30	0.95
F30	0.95
G30	DPE 100/100; partida 750101 pública
H30	2026-04-30
A31	SC-L-N-02
B31	RRHH-01
C31	Talento humano — nómina y contratos LOSNCP publicados
D31	0.95
E31	0.92
F31	0.92
G31	Nómina pública; contratos disponibles
H31	2026-04-30
A32	AH-I-X-01
B32	FIN-01
C32	Sostenibilidad financiera — presupuesto y cédula pública
D32	0.98
E32	0.97
F32	0.97
G32	Presupuesto 2026 publicado ✓
H32	2026-04-30
A33	AH-I-X-02
B33	DOP-01
C33	Vialidad — contratos de obra publicados
D33	0.95
E33	0.92
F33	0.92
G33	Partidas 750105/750116 disponibles
H33	2026-04-30
A34	AH-I-X-03
B34	PAT-01
C34	Salud — info Patronato parcialmente LOTAIP
D34	0.88
E34	0.85
F34	0.85
G34	Patronato: obligación LOTAIP parcial
H34	2026-Q2 (pendiente verificacion portal)
A35	AH-I-N-01
B35	EPAM-01
C35	Desechos sólidos — contratos EPAM publicados
D35	0.95
E35	0.93
F35	0.93
G35	EP Aseo: LOTAIP autónomo ✓
H35	2026-Q2 (pendiente verificacion portal)
A36	SC-L-G-01
B36	DAPS-01
C36	Alcantarillado — cédula y contratos públicos
D36	0.97
E36	0.94
F36	0.94
G36	Partidas 750103 publicadas
H36	2026-Q2 (pendiente verificacion portal)
A37	AH-I-X-04
B37	RRHH-01
C37	Modernización reg. — procesos LOSNCP publicados
D37	0.92
E37	0.9
F37	0.9
G37	Concurso méritos publicado
H37	2026-Q2 (pendiente verificacion portal)
A38	PI-I-G-01
B38	DOP-01
C38	Equipamientos públicos — contratos publicados
D38	0.94
E38	0.92
F38	0.92
G38	Obras publicadas en SERCOP
H38	2026-04-30
A39	AH-C-X-01
B39	PAT-01
C39	Derechos mujer — info PAT social disponible
D39	0.85
E39	0.83
F39	0.83
G39	Información social: calidad pendiente
H39	2026-Q2 (pendiente verificacion portal)
A40	AH-C-X-02
B40	ALC-01
C40	Sistema info municipal — actualización portal
D40	0.9
E40	0.88
F40	0.88
G40	Portal municipal: actualizado Q1 2026
H40	2026-04-30
A41	SC-I-N-03
B41	ALC-01
C41	Participación ciudadana — actas disponibles
D41	0.88
E41	0.86
F41	0.86
G41	Actas de sesión: parcialmente públicas
H41	2026-Q2 (pendiente verificacion portal)
A42	FA-I-X-01
B42	BOMB-01
C42	Gestión riesgo — informes BCBM publicados
D42	0.92
E42	0.91
F42	0.91
G42	Bomberos: LOTAIP autónomo ✓
H42	2026-Q2 (pendiente verificacion portal)
A43	FA-C-X-01
B43	EPAM-01
C43	Áreas verdes — contratos mantenimiento publicados
D43	0.94
E43	0.92
F43	0.92
G43	Partidas 730418/730419 disponibles
H43	2026-Q2 (pendiente verificacion portal)
A44	FA-I-X-02
B44	EPAM-01
C44	Índice equipamiento — datos disponibles portal
D44	0.85
E44	0.82
F44	0.82
G44	Indicador derivado: validación pendiente
H44	2026-Q2 (pendiente verificacion portal)
A45	FA-L-N-01
B45	ALC-01
C45	Inventario patrimonio — en elaboración
D45	0.78
E45	0.75
F45	0.78
G45	Inventario no publicado aún — pendiente
H45	2026-Q2 (pendiente verificacion portal)
A46	PI-I-G-02
B46	ALC-01
C46	Cumplimiento PDOT — informe DGA disponible
D46	0.9
E46	0.88
F46	0.9
G46	Informe PDOT Q1 disponible
H46	2026-04-30
A47	PI-L-G-01
B47	DOP-01
C47	Señalización vial — contratos publicados
D47	0.92
E47	0.91
F47	0.92
G47	Contratos SERCOP ✓
H47	2026-Q2 (pendiente verificacion portal)
A48	EP-L-N-01
B48	DOP-01
C48	Vivienda — info disponible parcialmente
D48	0.85
E48	0.84
F48	0.85
G48	Vivienda: gestión concurrente MIDUVI
H48	2026-Q2 (pendiente verificacion portal)
A49	EP-L-X-01
B49	ALC-01
C49	Fomento económico — datos no sistematizados aún
D49	0.78
E49	0.76
F49	0.78
G49	Económico: requiere sistematización portal
H49	2026-Q2 (pendiente verificacion portal)
A50	PI-TUR-01
B50	ALC-01
C50	Turismo — menos regulado LOTAIP
D50	0.75
E50	0.74
F50	0.76
G50	Turismo: obligación difusa en LOTAIP
H50	2026-Q2 (pendiente verificacion portal)
A51	PI-TUR-02
B51	ALC-01
C51	Eventos turísticos — programas parcialmente públicos
D51	0.75
E51	0.73
F51	0.76
G51	Eventos: publicidad parcial
H51	2026-Q2 (pendiente verificacion portal)
A52	FA-CC-01
B52	EPAM-01
C52	Cambio climático — plan PDOT publicado
D52	0.91
E52	0.9
F52	0.91
G52	Plan GestiónCC disponible en portal
H52	2026-Q2 (pendiente verificacion portal)
A53	AH-AP-04
B53	DAPS-01
C53	Continuidad agua — informe operación publicado
D53	0.97
E53	0.95
F53	0.96
G53	EMAPAM: LOTAIP autónomo ✓
H53	2026-Q2 (pendiente verificacion portal)
A54	FA-DIS-01
B54	EPAM-01
C54	Disposición final — contratos y operación públicos
D54	0.95
E54	0.93
F54	0.94
G54	Relleno sanitario: contratos SERCOP ✓
H54	2026-Q2 (pendiente verificacion portal)
A56	RESUMEN
G56	Transparentes(>=0.9): 15/25 | IOC_esperado: 40.0% | Fuente DPE 2025: 100/100
A57	⚠️ NOTA SIMULACIÓN LOTAIP 2026
B57	Valores V_LOTAIP simulados desde patrón 2024. V=1.0: metas con alta probabilidad de publicación directa en portal. V=0.5: metas con URL registrada pero acceso parcial. Responsable LOTAIP: Actualizar con verificación manual de URLs en montecristi.gob.ec
A59	RESUMEN:
A60	0.95
B60	Transparencia excelente — publicado y accesible
A61	0.9
B61	Cumplimiento LOTAIP — disponible en portal
A62	0.8
B62	Parcialmente accesible — calidad a verificar
A63	0.7
B63	Información incompleta — requiere actualización
```