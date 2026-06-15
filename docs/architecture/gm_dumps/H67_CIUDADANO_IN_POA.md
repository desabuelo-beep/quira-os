# H67_CIUDADANO_IN_POA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=60 · pobladas=13 · fórmulas=7
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H68_MOTOR_CONGRUENCIA_EXTERNA
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B223
B7	=H01_PARÁMETROS!B224
B8	=H01_PARÁMETROS!B225
B9	=TODAY()
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H67_CIUDADANO_IN_POA
A2	H67 — SANDBOX CIUDADANO — INGESTA: POA / PLANIFICACIÓN OPERATIVA EXTERNA
A3	Zona de volcado para el POA del GAD externo. Alimenta H68. NO conecta con H05 ni H12.
A5	▌ METADATOS DEL GAD EXTERNO
A6	GAD_Externo_Nombre
A7	GAD_Externo_RUC
A8	Año_Análisis
A9	Fecha_Carga
A10	Fuente
B10	POA Institucional — descarga ciudadano
A11	ADVERTENCIA
B11	⛔ DATOS EXTERNOS — No representan a Montecristi. No conectar a H12.
A13	▌ POA EXTERNO (zona de volcado libre)
A14	ID_Meta_Local
B14	Descripción_Meta
C14	Eje_PDOT_Local
D14	Presupuesto_Asignado
E14	Unidad_Responsable
F14	Indicador
G14	Meta_Física
H14	Avance_%
I14	Estado
A16	(Pegar aquí los datos POA del GAD externo — zona libre de volcado)
```