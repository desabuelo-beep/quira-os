# H68_MOTOR_CONGRUENCIA_EXTERNA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=23 · pobladas=19 · fórmulas=20
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO, H65_CIUDADANO_IN_PRESUPUESTO, H66_CIUDADANO_IN_PAC, H67_CIUDADANO_IN_POA
outputs(alimenta a): —
refs no resueltas: #H00_ÍNDICE, H01
MARCADORES: C12: =IF(B12>0,"✅ Datos cargados","⚠️ Sin datos — cargar H65") · C13: =IF(B13>0,"✅ Datos cargados","⚠️ Sin datos — cargar H66") · C14: =IF(B14>0,"✅ Datos cargados","⚠️ Sin datos — cargar H67") · C20: =IF(H01_PARÁMETROS!B222=FALSE,"⛔ Sandbox inactivo",IF(B15=0,"⚠️ Sin da

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B222
C6	=IF(H01_PARÁMETROS!B222=TRUE,"✅ Motor externo habilitado","⛔ Motor en espera — cambiar H01!B220 a CIUDADANO")
B7	=H01_PARÁMETROS!B223
B8	=H01_PARÁMETROS!B225
B12	=COUNTA(H65_CIUDADANO_IN_PRESUPUESTO!A17:A500)
C12	=IF(B12>0,"✅ Datos cargados","⚠️ Sin datos — cargar H65")
B13	=COUNTA(H66_CIUDADANO_IN_PAC!A17:A500)
C13	=IF(B13>0,"✅ Datos cargados","⚠️ Sin datos — cargar H66")
B14	=COUNTA(H67_CIUDADANO_IN_POA!A17:A500)
C14	=IF(B14>0,"✅ Datos cargados","⚠️ Sin datos — cargar H67")
B15	=IF(B12>0,SUM(H65_CIUDADANO_IN_PRESUPUESTO!E17:E500),0)
C15	=IF(B15>0,"✅ Presupuesto registrado","⚠️ Verificar columna E de H65")
B16	=IF(B12>0,SUM(H65_CIUDADANO_IN_PRESUPUESTO!F17:F500),0)
B17	=IF(B15>0,B16/B15,0)
C17	=IF(B17>=0.7,"✅ Ejecución ≥ 70%",IF(B17>=0.5,"⚠️ Ejecución moderada","❌ Ejecución baja < 50%"))
B20	=IF(H01_PARÁMETROS!B222=TRUE,IF(B15>0,(B16/B15)*0.7+0.3*IF(B14>0,COUNTIF(H67_CIUDADANO_IN_POA!H17:H500,">0.5")/MAX(B14,1),0),0),0)
C20	=IF(H01_PARÁMETROS!B222=FALSE,"⛔ Sandbox inactivo",IF(B15=0,"⚠️ Sin datos suficientes para calcular ICPI",IF(B20>=0.7,"✅ Congruencia alta",IF(B20>=0.5,"⚠️ Congruencia moderada","❌ Congruencia baja"))))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H68_MOTOR_CONGRUENCIA_EXTERNA
A2	H68 — MOTOR DE CONGRUENCIA EXTERNA (MODO CIUDADANO)
A3	Calcula el ICPI externo del GAD ciudadano usando los datos cargados en H65-H67. El resultado NO modifica H12!B33 ni el Axioma canónico de Montecristi.
A5	▌ VERIFICACIÓN DE MODO
A6	Sandbox_Activo
A7	GAD_Externo
A8	Año_Análisis
A10	▌ DIAGNÓSTICO DE CONGRUENCIA PRESUPUESTO-POA-PAC
A11	Indicador
B11	Valor calculado
C11	Estado
A12	Filas_Presupuesto_Cargadas
A13	Filas_PAC_Cargadas
A14	Filas_POA_Cargadas
A15	Presupuesto_Total_Externo ($)
A16	Devengado_Total_Externo ($)
A17	Ejecución_Global_%
A19	▌ ICPI EXTERNO ESTIMADO (diagnóstico ciudadano)
A20	ICPI_Externo_Estimado
A21	Nota metodológica
B21	Fórmula simplificada: ICPI_ext = 0.70×(Devengado/Codificado) + 0.30×(POA_metas_avance>50%). Para análisis completo el ciudadano debe solicitar acceso a SIAP-ICPI Institucional al GAD.
A23	⛔ FIREWALL CANÓNICO
B23	La FÓRMULA CANÓNICA de H12!B33 (B31/B32×100) permanece sellada e inamovible por Axioma de Invarianza. El resultado del ciclo 2025 fue ICPI_Real_2025 = 69.9309%. El ciclo corriente produce su propio ICPI dinámico bajo la misma fórmula. Este motor opera en carril aislado: modificar H01!B220=CIUDADANO no altera ninguna celda de H03 a H62.
```