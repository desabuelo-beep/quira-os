# H20c_IEF_EFICIENCIA_FINANCIERA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=55 · pobladas=34 · fórmulas=18
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H07c_Ti_VERIFICADO_INFORME, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H27_MMP_ANUAL, H28_RESUMEN_EJECUTIVO, H29_TABLERO_ALCALDE, H31_REPORTE_CPCCS, H39_AUTOCONTROL_ECOSISTEMA, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B147
B7	=H01_PARÁMETROS!B148
B8	=H01_PARÁMETROS!B149
B9	=H01_PARÁMETROS!B150
B10	=H01_PARÁMETROS!B13
B36	=SUMIF(H07c_Ti_VERIFICADO_INFORME!D23:D50,"FONDO_CONCURSABLE",H07c_Ti_VERIFICADO_INFORME!G23:G50)
B37	=SUMIF(H07c_Ti_VERIFICADO_INFORME!D23:D50,"DONACION_ESPECIE",H07c_Ti_VERIFICADO_INFORME!G23:G50)
B38	=SUMIF(H07c_Ti_VERIFICADO_INFORME!D23:D50,"COOPERACION_DIRECTA",H07c_Ti_VERIFICADO_INFORME!G23:G50)
B39	=B36+B37+B38
B40	=H07_S5_FINANCIERO_eSIGEF!B18
B41	=IF(B40=0,0,B39/B40)
B42	=IF(B41>=H01_PARÁMETROS!B148,"🔵 Alta capacidad de captación",IF(B41>=H01_PARÁMETROS!B149,"🟢 Buena gestión de fondos externos",IF(B41>=H01_PARÁMETROS!B150,"🟡 Captación moderada","🟠 Oportunidad de mejora en gestión de fondos")))
C51	=B41
C52	=B41
C53	=B41
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H20c_IEF_EFICIENCIA_FINANCIERA
A2	H20c — IEF — ÍNDICE DE EFICIENCIA FINANCIERA
A3	Mide la capacidad del GAD para capturar fondos externos (concursables, donaciones, cooperación). IEF = Fondos Externos Captados / Presupuesto Codificado Total × 100.
A5	▌ PARÁMETROS IEF (de H01 Sección J)
A6	IEF_Activo
A7	Umbral_Alto
A8	Umbral_Bueno
A9	Umbral_Moderado
A10	Año_Activo
A12	▌ FONDOS EXTERNOS CAPTADOS 2026
A13	ID_Meta
B13	Nombre_Meta
C13	TIPO_FINANCIAMIENTO
D13	Monto_Externo_USD
E13	Fuente_Fondo
F13	Referencia_H07c
A14	SC-I-N-01
B14	Agua Potable Rural — convenio MIDUVI/BanEcuador
C14	FONDO_EXTERNO
D14	487500
A15	SC-L-G-01
B15	Alcantarillado rural — aporte sectorial SENAGUA
C15	FONDO_EXTERNO
D15	312000
A16	AH-I-X-02
B16	Vialidad — convenio MTOP rehabilitación
C16	FONDO_EXTERNO
D16	850000
A17	EP-L-N-01
B17	Vivienda social — MIDUVI bono entrega vivienda
C17	FONDO_EXTERNO
D17	225000
A35	▌ CÁLCULO IEF
A36	Fondos_Concursables_Total_USD
A37	Fondos_Donacion_Total_USD
A38	Fondos_Cooperacion_Total_USD
A39	Total_Fondos_Externos_USD
A40	Presupuesto_Codificado_Total_USD
A41	★ IEF_%
A42	Clasificación_IEF
A43	▌ NOTA METODOLÓGICA IEF
B43	El IEF premia la gestión proactiva de fondos externos:
B44	• Fondos concursables: ganados por concurso competitivo (no reembolsables)
B45	• Donaciones en especie: valorizadas a precio de mercado
B46	• Cooperación directa: asistencia técnica o financiera de organismos internacionales
B47	El IEF NO penaliza al GAD si no tiene fondos externos — simplemente muestra oportunidad de mejora. El IEF elevado indica gestión activa y diversificación de fuentes de financiamiento.
A49	▌ REFERENCIA CRUZADA — IEF EN OTROS MÓDULOS
A50	Módulo
B50	Campo
C50	Referencia a usar
A51	H28 Resumen Ejecutivo
B51	IEF_Global
A52	H29 Tablero Alcalde
B52	Pregunta IEF
A53	H27 MMP Anual
B53	IEF_Anual
A55	⚠️ NOTA ACTIVACIÓN:
B55	IEF mostrará 0.00% hasta que: (1) H01 §J tenga los umbrales J136-J139, y (2) H07c tenga registros de fondos externos con monto > 0. Cuando el analista ingrese los datos, B41 se actualizará automáticamente.
```