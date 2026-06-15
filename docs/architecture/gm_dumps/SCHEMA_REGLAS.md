# SCHEMA_REGLAS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=39 · pobladas=35 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ SCHEMA_REGLAS — Reglas de Alerta y Clasificación SIAP-ICPI v1.0
C1	Motor de semáforo y clasificación automática · DYLUS LAB
A3	▌ CLASIFICACIÓN ICPI (Índice de Cumplimiento Planificación Institucional)
A4	Regla_ID
B4	Nombre_Clasificacion
C4	Umbral_Min
D4	Umbral_Max
E4	Color_Hex
F4	Emoji
G4	Accion_Recomendada
A5	ICPI-R01
B5	Ecosistema Pleno
C5	90.00
D5	100.00
E5	#1E40AF
F5	🔵
G5	Mantener ritmo, comunicar logros, replicar modelo
A6	ICPI-R02
B6	Gestión Sólida
C6	70.00
D6	89.99
E6	#15803D
F6	🟢
G6	Reforzar metas rezagadas, optimizar ejecución presupuestaria
A7	ICPI-R03
B7	Transición Crítica
C7	50.00
D7	69.99
E7	#D97706
F7	🟡
G7	Plan de recuperación inmediato, revisión POA, alertar concejo
A8	ICPI-R04
B8	Gestión Precaria
C8	30.00
D8	49.99
E8	#C2410C
F8	🟠
G8	Intervención urgente, auditoría interna, comunicación transparente
A9	ICPI-R05
B9	Colapso Institucional
C9	0.00
D9	29.99
E9	#DC2626
F9	🔴
G9	Declaratoria de emergencia institucional, veeduría externa
A10	ICPI-REF
B10	Axioma 2025 (referencia histórica)
C10	69.93
D10	69.93
E10	#7C3AED
F10	⭐
G10	Valor de referencia canonizado SIAP-ICPI v1.0 — NO MODIFICAR
A12	▌ REGLAS DE EJECUCIÓN PRESUPUESTARIA (Ti)
A13	Regla_ID
B13	Nombre_Alerta
C13	Umbral_Ti_Min_%
D13	Umbral_Ti_Max_%
E13	Semaforo
F13	Emoji
G13	Accion
A14	TI-R01
B14	Ejecución Óptima
C14	80.00
D14	100.00
E14	VERDE
F14	🟢
G14	Continuar, registrar buenas prácticas
A15	TI-R02
B15	Ejecución Adecuada
C15	60.00
D15	79.99
E15	AMARILLO
F15	🟡
G15	Monitorear, identificar cuellos de botella
A16	TI-R03
B16	Ejecución en Riesgo
C16	30.00
D16	59.99
E16	NARANJA
F16	🟠
G16	Reprogramar actividades, acelerar procesos PAC
A17	TI-R04
B17	Ejecución Crítica
C17	0.00
D17	29.99
E17	ROJO
F17	🔴
G17	Revisión urgente: ¿fondos bloqueados?, ¿procesos desiertos?
A18	TI-Q1
B18	Q1 2026 GAD Municipal
C18	11.20
D18	11.20
E18	NARANJA
F18	⚠️
G18	Bajo para Q1 — revisar cronograma PAC
A19	TI-Q1b
B19	Q1 2026 Patronato
C19	19.56
D19	19.56
E19	AMARILLO
F19	🟡
G19	Aceptable para Q1
A20	TI-Q1c
B20	Q1 2026 EP Aseo
C20	18.17
D20	18.17
E20	AMARILLO
F20	🟡
G20	Aceptable para Q1
A21	TI-Q1d
B21	Q1 2026 Bomberos
C21	19.43
D21	19.43
E21	AMARILLO
F21	🟡
G21	Aceptable para Q1
A23	▌ REGLAS NBI — COBERTURA DE SERVICIOS
A24	Regla_ID
B24	Indicador
C24	Umbral_Critico
D24	Umbral_Deficiente
E24	Umbral_Adecuado
F24	Fuente
A25	NBI-R01
B25	NBI Total territorio
C25	≥60% = CRÍTICO (🔴)
D25	40-59% = ALTO (🟠)
E25	<40% = MANEJABLE (🟡)
F25	INEC/SENPLADES
A26	NBI-R02
B26	Cobertura Agua Potable
C26	<50% = BRECHA CRÍTICA
D26	50-79% = DÉFICIT
E26	≥80% = ADECUADO
F26	OMS/PDOT
A27	NBI-R03
B27	Cobertura Alcantarillado
C27	<30% = BRECHA CRÍTICA
D27	30-69% = DÉFICIT
E27	≥70% = ADECUADO
F27	OMS/PDOT
A28	NBI-R04
B28	Recolección Desechos
C28	NO = ALERTA
D28	SI con <2 días = BÁSICO
E28	SI con ≥3 días = ADECUADO
F28	PDOT/OMS
A29	NBI-R05
B29	Equipamiento m2/hab
C29	<3 m2 = CRÍTICO
D29	3-9 m2 = BÁSICO
E29	≥9 m2 = ESTÁNDAR OMS
F29	OMS referencia 9m2/hab
A30	NBI-R06
B30	Madres adolescentes 15-19
C30	>25% = ALERTA
D30	15-25% = MODERADO
E30	<15% = DENTRO_META
F30	OPS/PDOT
A32	▌ REGLAS MPP — MONITOREO DE METAS Y PROYECTOS
A33	Regla_ID
B33	Tipo_Alerta
C33	Condicion
D33	Accion_MPP
E33	Responsable
F33	Plazo_Respuesta
G33	Modulo_SIAP
A34	MPP-R01
B34	Meta en Riesgo
C34	Avance <70% del cronograma previsto a mes corriente
D34	Emitir alerta amarilla. Solicitar informe de causas
E34	Director de área
F34	5 días hábiles
G34	H25_MONITORING_MPP_MES
A35	MPP-R02
B35	Meta Crítica
C35	Avance <50% del cronograma previsto
D35	Emitir alerta roja. Convocar mesa técnica de seguimiento
E35	Alcalde / Concejo
F35	48 horas
G35	H25_MONITORING_MPP_MES
A36	MPP-R03
B36	Meta Cumplida
C36	Avance ≥100%
D36	Registrar como logro. Validar con fuente Ruta B
E36	Unidad responsable
F36	Mes siguiente
G36	H26_MONITORING_MPP_TRI
A37	MPP-R04
B37	Proyecto Desierto
C37	PAC proceso declarado desierto 2+ veces
D37	Alerta crítica PAC. Revisar especificaciones técnicas
E37	Director Financiero
F37	Inmediato
G37	H27_MONITORING_MPP_ANUAL
A38	MPP-R05
B38	Brecha Territorial
C38	Ti de territorio rural <50% del Ti urbano
D38	Alerta equidad territorial. Reasignar inversión
E38	Planificación
F38	Trimestral
G38	H26_MONITORING_MPP_TRI
A39	MPP-R06
B39	Vencimiento PDOT
C39	Meta sin avance documentado por >3 meses
D39	Revisión extraordinaria. Posible reprogramación
E39	Unidad + Planificación
F39	10 días hábiles
G39	H25_MONITORING_MPP_MES
```