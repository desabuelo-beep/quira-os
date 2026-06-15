# H34b_MFN_FIDELIDAD_NARRATIVA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=202 · pobladas=21 · fórmulas=17
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H20b_IGP_GOBERNANZA_PARTIC, H39_AUTOCONTROL_ECOSISTEMA, H85_ALERTS_LOG, H89_TRUST_SCORE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
M11	=IF(J11>=0.85,"✅ Fidelidad Alta",IF(J11>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M12	=IF(J12>=0.85,"✅ Fidelidad Alta",IF(J12>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M13	=IF(J13>=0.85,"✅ Fidelidad Alta",IF(J13>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M14	=IF(J14>=0.85,"✅ Fidelidad Alta",IF(J14>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M15	=IF(J15>=0.85,"✅ Fidelidad Alta",IF(J15>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M16	=IF(J16>=0.85,"✅ Fidelidad Alta",IF(J16>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M17	=IF(J17>=0.85,"✅ Fidelidad Alta",IF(J17>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M18	=IF(J18>=0.85,"✅ Fidelidad Alta",IF(J18>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
M19	=IF(J19>=0.85,"✅ Fidelidad Alta",IF(J19>=0.6,"⚠️ Fidelidad Media","🔴 Fidelidad Baja"))
B21	=IFERROR(ROUND(AVERAGE(J11:J19),4),0)
C21	=TEXT(B21,"0.00%")&" — Promedio IF_n 9 registros MFN"
B43	=B21
L43	=TEXT(B21,"0.00%")&" — IGP_3 alimenta H20b"
J202	=AVERAGE(J11:J201)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H34b_MFN_FIDELIDAD_NARRATIVA
A2	H34b — MFN — MATRIZ DE FIDELIDAD NARRATIVA
A3	Triangula las afirmaciones oficiales de rendición de cuentas con la evidencia documental verificable.
A4	ESCALA IF_n: ≥0.85 = Fidelidad Alta | ≥0.60 = Fidelidad Media | <0.60 = Fidelidad Baja
A5	▌ METODOLOGÍA DE SCORING
A6	IF_n = Ponderación × (1 - |Narrativa - Evidencia| / max(Narrativa, Evidencia)). Rango: 0.00 (sin evidencia) a 1.00 (fidelidad perfecta).
A7	▌ FUENTES DE DATOS
A8	RDC 2024 Patronato · PAC 2024 Patronato · Presupuesto 2024 Patronato · RDC 2023 · PAC 2023 · eSIGEF · PDOT · LOTAIP · Actas CPCCS
A10	ID_MFN
B10	ID_Ente
C10	Entidad
D10	Eje_PDOT_Vinculado
E10	Meta_PDOT_POA
F10	Categoría_Gestión
G10	Timestamp_Video
H10	Discurso_Alcalde_NLP (Narrativa Oficial)
I10	Evidencia_Técnica_CPCCS (Hecho Verificado)
J10	Valor_Narrativa
K10	Valor_Evidencia
L10	IF_n
M10	Clasificación_Fidelidad
A11	MFN-001
B11	ENTE-01
C11	GAD Montecristi
D11	2. Asentamientos Humanos
E11	Aumentar del 39.25% al 42.38% la cobertura de agua potable
F11	Infraestructura / Financiamiento
G11	[01:36:17]
H11	"El proyecto de captación de agua ya tiene el crédito aprobado por la CAF por 28 millones de dólares"
I11	Oficio de solicitud 1028-2024 para ampliación de financiamiento por 28 millones. Aprobación préstamo CAF Res. P.E. 1478/2024.
J11	1
K11	28000000
L11	1.00
A12	MFN-002
B12	ENTE-01
C12	GAD Montecristi
D12	2. Asentamientos Humanos
E12	Sistema Vial: conectividad a escala cantonal
F12	Vialidad / Equipamiento
G12	[01:47:32]
H12	"Vamos a tener un segundo kit de compactación: motoniveladora, rodillo y también dos retroexcavadoras"
I12	Etapa precontractual para adquisición de maquinaria pesada (Motoniveladora, Rodillo y 2 Retroexcavadora) a la espera de anticipo.
J12	1
K12	4
L12	1.00
A13	MFN-003
B13	ENTE-01
C13	GAD Montecristi
D13	4. Económico Productivo
E13	Incrementar establecimientos con certificación Ciudad Creativa
F13	Cultura / Promoción
G13	[01:10:45]
H13	"Hoy somos parte de la red de ciudades creativas de la UNESCO... ¿Cuánto le gastó a Montecristi? Cero centavos"
I13	Adhesión a la Red de Ciudades Creativas UNESCO. Ejecución PDOT lograda mediante planes de acción y alianzas, sin costo directo reportado en PAC para este fin.
J13	1
K13	1
L13	1.00
A14	MFN-004
B14	ENTE-02
C14	Patronato Municipal
D14	3. Sociocultural
E14	Incrementar la población atendida en salud preventiva
F14	Inversión / Ejecución Financiera
G14	[01:07:05]
H14	"En total, con relación al Patronato... una inversión de 900,200 dólares"
I14	Balance General eSIGEF: Gasto de Inversión Ejecutado por $1,022,627.73.
J14	0.88
K14	1022627.73
L14	0.88
A15	MFN-005
B15	ENTE-02
C15	Patronato Municipal
D15	3. Sociocultural
E15	Incrementar el 10% anualmente de la población atendida
F15	Servicios Médicos / Cobertura
G15	[01:07:05]
H15	"En la cual se han hecho 130,038 atenciones"
I15	Meta POA 5000: Brigadas médicas, visitas domiciliarias. Totales Cumplidos: 414,743.00.
J15	0.31
K15	414743
L15	0.31
A16	MFN-006
B16	ENTE-03
C16	Cuerpo de Bomberos
D16	1. Físico Ambiental
E16	Protección frente a riesgos y desastres
F16	Eficiencia Operativa / Emergencias
G16	[01:39:55]
H16	"1,683 emergencias atendidas... 13% de crecimiento en atenciones"
I16	Meta 1468.00: Número factible de emergencias atendidas. Totales Cumplidos: 1683.00 (114.65% de la gestión).
J16	1
K16	1683
L16	1.00
A17	MFN-007
B17	ENTE-03
C17	Cuerpo de Bomberos
D17	5. Institucional
E17	Incrementar el porcentaje de proyectos ejecutados
F17	Infraestructura Operativa
G17	[01:40:13]
H17	"Ya está el proyecto, ya está el presupuesto y estamos a pocos meses de empezar la construcción del Cuartel Leónidas Proaño"
I17	Meta POA GAD: Estudio de suelo en los predios previstos para la construcción del cuartel de bomberos de Leonidas Proaño.
J17	1
K17	1
L17	1.00
A18	MFN-008
B18	ENTE-04
C18	Aseo Integral EP
D18	1. Físico Ambiental
E18	Aumentar a 17.32 m²/hab el IVU y Saneamiento
F18	Equipamiento / Saneamiento
G18	[01:28:25]
H18	"Teníamos solamente uno, ahora tenemos seis recolectores de basura que garantizan la cobertura"
I18	Meta 11: Fortalecer el servicio de recolección. Se realizó la adquisición de 6 vehículos recolectores de desechos sólidos.
J18	1
K18	6
L18	1.00
A19	MFN-009
B19	ENTE-04
C19	Aseo Integral EP
D19	1. Físico Ambiental
E19	Recuperación de ecosistemas degradados
F19	Saneamiento Estratégico
G19	[01:28:54]
H19	"Logramos la viabilidad para una celda emergente y el cierre técnico del botadero de basura"
I19	Meta 31: Operativizar el cierre técnico. Estudio para el cierre del actual botadero y obtención de viabilidad de la celda emergente.
J19	1
K19	1
L19	1.00
A21	IGP_3_Fidelidad_MFN_Global:
M21	Escala 0-1 → alimenta H20b
N21	→ H20b IGP_3
A43	IGP_3_Fidelidad_MFN_Global:
K43	Escala 0-1 → alimenta H20b
```