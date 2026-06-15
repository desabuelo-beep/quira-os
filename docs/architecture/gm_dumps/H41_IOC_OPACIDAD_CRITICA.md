# H41_IOC_OPACIDAD_CRITICA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=27 · pobladas=23 · fórmulas=4
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B10	=H01_PARÁMETROS!B18
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H41_IOC_OPACIDAD_CRITICA
A2	H41 — IOC — ÍNDICE DE OPACIDAD CRÍTICA
A3	Mide el porcentaje de información pública con acceso restringido o no publicada según LOTAIP. Valor 2025: 17.71%.
A4	NOTA: El IOC mide opacidad — un valor BAJO de IOC es bueno. IOC=17.71% significa que el 82.29% de la información requerida es accesible.
A6	▌ PANEL IOC
A7	Campo
B7	Valor
C7	Nota
A8	IOC_Global_2025
B8	0.1771
C8	17.71% metas sin URL verificada — Fuente: H18_ITAM!B20
A9	Clasificación
B9	Opacidad Moderada - plan de mejora activo
A10	Información_Requerida_Total
C10	25 metas con obligaciones LOTAIP
A11	Información_No_Accesible
B11	4
C11	Calculado dinámicamente desde H01
A12	Información_Accesible
B12	21
C12	Metas con información accesible
A13	IOC_2026 (dinámico)
B13	0.1771
C13	Dinámico desde H09 LOTAIP
A15	▌ INTERPRETACIÓN PREVENTIVA
A16	Un IOC de 17.71% indica que 4-5 metas requieren mayor publicidad en el portal institucional.
A17	La mejora de IOC fortalece la transparencia y el ITAM simultáneamente.
A18	Meta 2027: IOC < 10% (reducir opacidad mediante publicación sistemática en LOTAIP).
A20	▌ ESCALA DE CLASIFICACIÓN IOC
B20	Opacidad Moderada - plan de mejora activo
A21	IOC
B21	Clasificación
C21	Interpretación
A22	IOC < 10%
B22	🟢 Transparencia Excelente
C22	Información ampliamente accesible
A23	10% - 20%
B23	🟡 Opacidad Moderada
C23	Recomendada revisión trimestral
A24	20% - 40%
B24	🔴 Opacidad Detectada
C24	Área de mejora prioritaria
A25	IOC > 40%
B25	⚫ Opacidad Crítica
C25	Intervención urgente requerida
A27	Fuente_IOC_Autorizada
B27	H18_ITAM!B20 = IOC_2025_Ref
C27	NUNCA calcular desde H01 defaults - usar H18
```