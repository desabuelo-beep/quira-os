# H64_SELECTOR_PROTOCOLO_MODO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=31 · pobladas=27 · fórmulas=9
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): —
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=H01_PARÁMETROS!B220
B8	=H01_PARÁMETROS!B221
B9	=H01_PARÁMETROS!B222
B10	=H01_PARÁMETROS!B223
B11	=H01_PARÁMETROS!B224
B12	=H01_PARÁMETROS!B225
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H64_SELECTOR_PROTOCOLO_MODO
A2	H64 — SELECTOR DE PROTOCOLO — DOCUMENTACIÓN DEL MODO DE OPERACIÓN
A3	Hoja de documentación y control del Selector de Protocolo. El interruptor real está en H01_PARÁMETROS!B220 (MODO_OPERACION).
A5	▌ ESTADO ACTUAL DEL SELECTOR
A6	Campo
B6	Valor activo
A7	Modo_Activo
A8	Descripción_Modo
A9	Sandbox_Activo
A10	Cantón_Ciudadano
A11	RUC_Ciudadano
A12	Año_Análisis_Ciudadano
A14	▌ DIFERENCIAS ENTRE MODOS
A15	Aspecto
B15	MODO INSTITUCIONAL
C15	MODO CIUDADANO
A16	Fuente presupuestaria
B16	H07_S5 (eSIGEF Montecristi real)
C16	H65_CIUDADANO_IN_PRESUPUESTO (datos subidos)
A17	Fuente PAC
B17	H06_S4 (PAC Montecristi real)
C17	H66_CIUDADANO_IN_PAC (datos subidos)
A18	Fuente POA
B18	H05_S3 (POA Montecristi real)
C18	H67_CIUDADANO_IN_POA (datos subidos)
A19	Motor de congruencia
B19	H12 (ICPI canónico — inmutable)
C19	H68_MOTOR_CONGRUENCIA_EXTERNA (aislado)
A20	ICPI producido
B20	H12!B33 produce el ICPI dinámico del ciclo activo (fórmula B31/B32×100). Base histórica 2025: ICPI_Real_2025 = 69.93090617%. La fórmula es inmutable por Axioma de Invarianza; el resultado evoluciona con cada ciclo de ingesta.
C20	H68!B20 (valor externo, no sellado)
A21	Protección fórmula canónica (Axioma de Invarianza)
B21	✅ Absoluta
C21	✅ No afecta H12
A23	▌ INSTRUCCIÓN PARA EL ANALISTA QUIRA
A24	Para cambiar al Modo Ciudadano:
A25	  (1) Ir a H01_PARÁMETROS celda B220 y cambiar INSTITUCIONAL por CIUDADANO
A26	  (2) Completar B223 (Cantón), B224 (RUC), B225 (Año fiscal)
A27	  (3) Cargar datos en H65 (Presupuesto), H66 (PAC) y H67 (POA)
A28	  (4) Ejecutar H68 para obtener diagnóstico externo
A29	  ⛔ NUNCA modificar H03-H11 ni H12 con datos ciudadanos
A31	⚠️ ALERTA DE INTEGRIDAD: Cambiar el Selector NO modifica el cálculo del Motor H12. La FÓRMULA CANÓNICA H12!B33 = B31/B32×100 es inmutable por Axioma de Invarianza. El ICPI_Real_2025 = 69.93090617% es la referencia histórica sellada del ciclo 2025. El ciclo 2026 producirá su propio ICPI bajo la misma fórmula inmutable. El Modo Ciudadano opera en carril aislado sin interferir con H03–H62.
```