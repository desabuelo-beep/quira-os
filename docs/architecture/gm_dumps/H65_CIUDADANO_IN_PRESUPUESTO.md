# H65_CIUDADANO_IN_PRESUPUESTO — volcado determinista (fórmulas + etiquetas)
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
D1	H65_CIUDADANO_IN_PRESUPUESTO
A2	H65 — SANDBOX CIUDADANO — INGESTA: CÉDULA PRESUPUESTARIA eSIGEF EXTERNA
A3	Zona de volcado para datos presupuestarios de cualquier GAD externo. NUNCA mezclar con datos de Montecristi. Alimenta H68 (Motor Externo), NO H12 (Motor Canónico).
A5	▌ METADATOS DEL GAD EXTERNO
A6	GAD_Externo_Nombre
A7	GAD_Externo_RUC
A8	Año_Análisis
A9	Fecha_Carga
A10	Fuente
B10	eSIGEF — descarga directa ciudadano
A11	ADVERTENCIA
B11	⛔ DATOS EXTERNOS — No representan a Montecristi. No conectar a H12.
A13	▌ CÉDULA PRESUPUESTARIA EXTERNA (zona de volcado libre)
A14	Cod_Partida
B14	Descripción
C14	Programa
D14	Subprograma
E14	Presupuesto_Codificado
F14	Devengado
G14	Porcentaje_Ejecución
H14	Fecha
A16	(Pegar aquí los datos eSIGEF del GAD externo — zona libre de volcado)
```