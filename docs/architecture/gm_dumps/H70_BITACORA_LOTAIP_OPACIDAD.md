# H70_BITACORA_LOTAIP_OPACIDAD — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=18 · pobladas=15 · fórmulas=14
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): —
refs no resueltas: #H00_ÍNDICE
MARCADORES: A11: Alertas_Pendientes · B11: =COUNTIF(G:G,"❌ Pendiente subsanación")

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=COUNTA(A15:A200)-1
C6	=IF(B6=0,"✅ Sin alertas activas",IF(B6<=3,"⚠️ "&B6&" alerta(s) — atención requerida","❌ "&B6&" alertas — RIESGO INSTITUCIONAL ALTO"))
B7	=COUNTIF(F15:F200,"CRÍTICA")
B8	=COUNTIF(F15:F200,"MODERADA")
B9	=COUNTIF(F15:F200,"INFORMATIVA")
B10	=COUNTIF(G15:G200,"✅ Resuelta")
B11	=COUNTIF(G:G,"❌ Pendiente subsanación")
B15	=TODAY()
I15	=TODAY()+30
B16	=TODAY()
I16	=TODAY()+15
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H70_BITACORA_LOTAIP_OPACIDAD
A2	H70 — BITÁCORA DE ALERTAS LOTAIP Y OPACIDAD INSTITUCIONAL
A3	Registro centralizado de hallazgos de opacidad: LOTAIP incumplida, fondos sin respaldo documental, procedimientos sin registro público. Alimenta H38 (SAT) y H37 (Escenarios). Inmutable una vez registrado.
A5	▌ PANEL DE ALERTAS LOTAIP
A6	Total_Alertas_Registradas
A7	Alertas_Críticas
A8	Alertas_Moderadas
A9	Alertas_Informativas
A10	Alertas_Resueltas
A11	Alertas_Pendientes
A13	▌ MARCO LEGAL DE REFERENCIA
B13	LOTAIP Art. 7: Publicación obligatoria de 84 literales. CPCCS: control social. CGE: control interno. LOSNCP: contratación pública. COPFP: planificación.
A14	ID_Alerta
B14	Fecha_Detección
C14	Tipo_Opacidad
D14	Descripción_Hallazgo
E14	Norma_Vulnerada
F14	Severidad
G14	Estado_Resolución
H14	Responsable_GAD
I14	Fecha_Límite_Subsanación
J14	Impacto_ICPI
A15	ALERTA-001
C15	LOTAIP — Literal k)
D15	Registro de actas del Concejo Municipal no publicado en portal web institucional para el período enero-marzo 2026
E15	LOTAIP Art. 7 lit. k)
F15	MODERADA
G15	⏳ En proceso
H15	Secretaría Municipal
J15	INF-02 si persiste 90 días
A16	ALERTA-002
C16	PAC — proceso sin publicar
D16	Proceso de contratación para adquisición de materiales de construcción no publicado en SERCOP dentro del plazo LOSNCP
E16	LOSNCP Art. 23
F16	CRÍTICA
G16	⚠️ Subsanación en proceso — LOTAIP verificación Q2-2026
H16	Dirección de Contratación Pública
J16	INF-01 aplicable si no subsana
A18	⛔ REGLA DE INMUTABILIDAD: Una vez registrada, ninguna alerta puede eliminarse de esta bitácora. Solo puede cambiar Estado_Resolución a ✅ Resuelta con evidencia.
```