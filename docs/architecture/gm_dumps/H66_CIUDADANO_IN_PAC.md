# H66_CIUDADANO_IN_PAC — volcado determinista (fórmulas + etiquetas)
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
D1	H66_CIUDADANO_IN_PAC
A2	H66 — SANDBOX CIUDADANO — INGESTA: PLAN ANUAL DE CONTRATACIÓN EXTERNO
A3	Zona de volcado para el PAC del GAD externo. Alimenta H68. NO conecta con H06 ni H12.
A5	▌ METADATOS DEL GAD EXTERNO
A6	GAD_Externo_Nombre
A7	GAD_Externo_RUC
A8	Año_Análisis
A9	Fecha_Carga
A10	Fuente
B10	SERCOP — descarga PAC ciudadano
A11	ADVERTENCIA
B11	⛔ DATOS EXTERNOS — No representan a Montecristi. No conectar a H12.
A13	▌ PAC EXTERNO (zona de volcado libre)
A14	Cod_CPC
B14	Descripción_Proceso
C14	Tipo_Contratación
D14	Presupuesto_Referencial
E14	Fecha_Publicación_Prevista
F14	Estado_PAC
G14	Vinculación_Meta_PDOT
A16	(Pegar aquí los datos PAC del GAD externo — zona libre de volcado)
```