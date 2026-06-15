# H69_ELEGIBILIDAD_FONDOS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=28 · pobladas=24 · fórmulas=24
inputs(lee de): H01_PARÁMETROS, H11_S9_AGENDA_GLOBAL_ODS, H11b_MONITOR_POLITICAS_PUBLICAS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE
MARCADORES: E28: =IF(ISNUMBER(SEARCH("✅",B28)),"CERTIFICADO","PENDIENTE")

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H12_MOTOR_ICPI_CANÓNICO!B33/100
C6	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=0.6,"✅ Sobre umbral mínimo 60%","❌ Bajo umbral mínimo — ICPI="&TEXT(H12_MOTOR_ICPI_CANÓNICO!B33/100,"0.00%"))
B7	=H01_PARÁMETROS!B6
B8	=H01_PARÁMETROS!B13
D12	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=C12,"✅ ELEGIBLE","❌ No elegible")
D13	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=C13,"✅ ELEGIBLE","❌ No elegible")
D14	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=C14,"✅ ELEGIBLE","❌ No elegible")
D15	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=C15,"✅ ELEGIBLE","❌ No elegible")
D16	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100>=C16,"✅ CERTIFICADO","❌ No certificable")
B19	=COUNTIF(D12:D16,"✅*")
C19	=B19&" de 5 fondos elegibles con ICPI="&TEXT(H12_MOTOR_ICPI_CANÓNICO!B33/100,"0.00%")&" (2026)"
B20	=COUNTIF(D12:D16,"❌*")
B21	=IF(H12_MOTOR_ICPI_CANÓNICO!B33/100<0.7,"ICPI debe subir "&TEXT(ROUND(0.7-H12_MOTOR_ICPI_CANÓNICO!B33/100,4),"0.0000")&"pp para umbral 70%","✅ Sobre umbral 70% — siguiente: 75%")
B25	=IFERROR(AVERAGE(H11_S9_AGENDA_GLOBAL_ODS!F14:F38),0)
E25	=IF(B25>=0.75,"✅ ELEGIBLE ODS","❌ Insuficiente")
B26	=IFERROR(AVERAGE(H11b_MONITOR_POLITICAS_PUBLICAS!F13:F37),0)
E26	=IF(B26>=0.75,"✅ ELEGIBLE PND","❌ Insuficiente")
B27	=IFERROR(COUNTIF(H11_S9_AGENDA_GLOBAL_ODS!F14:F38,">=0.9"),0)
E27	=IF(B27>=20,"✅ UMBRAL FONDOS OK","⚠️ Reforzar")
B28	=IF(AND(IFERROR(AVERAGE(H11_S9_AGENDA_GLOBAL_ODS!F14:F38),0)>=0.75,IFERROR(AVERAGE(H11b_MONITOR_POLITICAS_PUBLICAS!F13:F37),0)>=0.75),"✅ CERTIFICADO — Fondos internacionales ODS/PND","❌ No elegible — Reforzar alineación")
E28	=IF(ISNUMBER(SEARCH("✅",B28)),"CERTIFICADO","PENDIENTE")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H69_ELEGIBILIDAD_FONDOS
A2	H69 — MOTOR DE ELEGIBILIDAD DE FONDOS (ICPI como umbral de acceso)
A3	Determina si el GAD cumple el umbral ICPI para acceder a fondos concursables, asistencia técnica y financiamiento no reembolsable. Umbral base: 60%.
A5	▌ ICPI DEL GAD
A6	ICPI_Actual
A7	GAD_Nombre
A8	Año_Análisis
A10	▌ TABLA DE UMBRALES DE ELEGIBILIDAD
A11	Fondo / Programa
B11	Entidad Financiadora
C11	Umbral_ICPI_Mínimo
D11	Elegibilidad_GAD
E11	Tipo_Apoyo
F11	Notas
A12	Fondo Nacional de Preinversión (FNP)
B12	SENPLADES / SETEPLAN
C12	0.6
E12	Financiamiento reembolsable preinversión
F12	Requiere PDOT actualizado y presupuesto participativo
A13	Programa de Fortalecimiento Municipal (PFM)
B13	BDE — Banco de Desarrollo del Ecuador
C13	0.65
E13	Asistencia técnica no reembolsable
F13	Evaluación anual. Requiere estados financieros al día.
A14	Fondo de Inversión para Gobiernos Locales (FIGL)
B14	Ministerio de Finanzas — COPFP
C14	0.7
E14	Transferencias extraordinarias
F14	ICPI mínimo 70% para segunda ronda de financiamiento
A15	Cooperación Descentralizada (bilateral/multilateral)
B15	GIZ / BID / Banco Mundial
C15	0.75
E15	Cooperación internacional no reembolsable
F15	Requiere carta compromiso Alcaldía + H63 completa
A16	Certificación DYLUS LAB Gold (max transparencia)
B16	DYLUS LAB — SIAP-ICPI
C16	0.85
E16	Sello de transparencia algorítmica
F16	Requiere H39!B30=✅ y H63 completa (66/66 promesas validadas)
A18	▌ RESUMEN DE POSICIÓN
A19	Fondos_Elegibles
A20	Fondos_No_Elegibles
A21	Brecha_Para_Siguiente_Umbral
A23	🌐 CONEXIÓN SIAP-ICPI — CERTIFICACIÓN ODS/PND FONDOS INTERNACIONALES
A24	INDICADOR
B24	VALOR
C24	DESCRIPCIÓN
D24	UMBRAL
E24	ELEGIBILIDAD
F24	FUENTE
A25	Score_ODS_Promedio
C25	Alineación promedio PDOT-ODS (25 metas)
D25	0.75
F25	H11_S9_AGENDA_GLOBAL_ODS!F14:F38
A26	Score_PND_Promedio
C26	Alineación promedio PDOT-PND 2025-2029 (25 metas)
D26	0.75
F26	H11b_MONITOR_POLITICAS_PUBLICAS!F13:F37
A27	Metas_Alta_Alineacion_ODS
C27	Metas con Score_ODS ≥ 90% (alineación alta)
D27	20
F27	H11!F14:F38
A28	Elegibilidad_Internacional_SIAP_ICPI
C28	Certificación combinada ODS+PND para acceso a fondos internacionales BID/BM/GIZ
D28	ODS≥75% + PND≥75%
F28	H11 + H11b
```