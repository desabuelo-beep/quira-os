# H89_TRUST_SCORE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=32 · pobladas=27 · fórmulas=12
inputs(lee de): H00_ÍNDICE, H11_S9_AGENDA_GLOBAL_ODS, H25_MMP_MENSUAL, H34b_MFN_FIDELIDAD_NARRATIVA, H42_IET_EQUIDAD_TERRITORIAL
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API, H86_REPORT
MARCADORES: B30: =IFERROR(H42_IET_EQUIDAD_TERRITORIAL!B9,"Pendiente")

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
B8	=ROUND(0.35*C3+0.25*C4+0.25*C5+0.15*C6,1)
B9	=ROUND(C3*0.35+C4*0.25+C5*0.25+C6*0.15,1)
B24	=IF(B8>=95,"CERTIFICADO",IF(B8>=80,"OPERATIVO CON OBSERVACIONES",IF(B8>=60,"RIESGO MODERADO","INTERVENCIÓN REQUERIDA")))
C24	=IF(B8>=95,"CERTIFICADO",IF(B8>=80,"OPERATIVO CON OBSERVACIONES",IF(B8>=60,"RIESGO MODERADO","INTERVENCIÓN REQUERIDA")))
D24	=IFERROR("Score actual "&TEXT(B8,"0.0")&"/100 → umbral "&IF(B8>=95,"CERTIFICADO (≥95)",IF(B8>=80,"OPERATIVO (≥80)",IF(B8>=60,"RIESGO (≥60)","INTERVENCIÓN (<60)")))&" aplicado.","")
B27	=IFERROR(1-AVERAGE(H34b_MFN_FIDELIDAD_NARRATIVA!L11:L37),0)
B28	=IF(IFERROR(1-AVERAGE(H34b_MFN_FIDELIDAD_NARRATIVA!L11:L37),0)>0.15,"⚠️ PENALIZACIÓN -10pts — Brecha narrativa > 15%","✅ Sin penalización — Fidelidad narrativa dentro del umbral")
B29	=IFERROR(VALUE(B9)-IF(1-AVERAGE(H34b_MFN_FIDELIDAD_NARRATIVA!L11:L37)>0.15,10,0),VALUE(B9))
B30	=IFERROR(H42_IET_EQUIDAD_TERRITORIAL!B9,"Pendiente")
B31	=IFERROR(H25_MMP_MENSUAL!W38,0)
B32	=IFERROR(AVERAGE(H11_S9_AGENDA_GLOBAL_ODS!F14:F38),0)
```

## ETIQUETAS / DATOS (tope 600)
```
A2	DIMENSIÓN
B2	PESO_%
C2	SCORE_0-100
D2	FUENTE / DESCRIPCIÓN
A3	Integridad
B3	35%
C3	88
D3	H12!B33 intacto | brechas de ingesta 2026 detectadas | MODELO_VALIDO en validación
A4	Disponibilidad
B4	25%
C4	94
D4	Sistema OPERATIVO · 114 hojas · Backup activo · API online
A5	Trazabilidad
B5	25%
C5	86
D5	Trazabilidad parcial — datos simulados en H08/H10 · H81 cadena activa
A6	Cumplimiento
B6	15%
C6	92
D6	SoD correcto · DataValidation H06/H09/H13 · observaciones metodológicas activas
A8	⚡ TRUST SCORE TOTAL (PONDERADO)
A9	TRUST_SCORE
C9	/100
D9	Trust = 0.35×Integridad + 0.25×Disponibilidad + 0.25×Trazabilidad + 0.15×Cumplimiento
A10	CLASIFICACIÓN
B10	CERTIFICADO
D10	SIAP-ICPI READY — Predictive Sovereignty
A12	CERTIFICADO_POR
B12	DYLUS_LAB_CERTIFIER
A13	TIMESTAMP_CERTIF
B13	2026-05-01 19:42:26 UTC
A14	FIRMA_CERTIFICACION
B14	8F5EE0AC4AAD74F4C36DD1C6A7E86A7E...
A16	📊 ESCALA INSTITUCIONAL CONSERVADORA (SIAP-ICPI v1.0 Institutional Mode)
A17	RANGO_SCORE
B17	CLASIFICACIÓN
C17	NIVEL
D17	DESCRIPCIÓN
A18	95–100
B18	CERTIFICADO
C18	★★★
D18	Sistema opera con máxima integridad y trazabilidad. Apto para auditoría externa. SIAP-ICPI v1.0 Institutional Mode activo.
A19	80–94
B19	OPERATIVO CON OBSERVACIONES
C19	★★
D19	Sistema funcional con áreas de mejora identificadas. Monitoreo activo requerido. No apto para certificación plena.
A20	60–79
B20	RIESGO MODERADO
C20	★
D20	Debilidades estructurales detectadas. Revisión obligatoria antes de publicar resultados. Intervención técnica recomendada.
A21	< 60
B21	INTERVENCIÓN REQUERIDA
C21	⚠️
D21	Sistema no apto para operación institucional. Suspender publicación de resultados. Activar H87_RECOVERY_POLICY.
A23	⚡ ESTADO ACTUAL DEL SISTEMA
A24	ESTADO_ACTUAL
A26	📡 PULSOS SINÁPTICOS SIAP-ICPI — CONEXIONES EXTERNAS
A27	MFN_BRECHA_NARRATIVA
D27	Brecha discurso-dato de la Matriz de Fidelidad Narrativa. Si > 15%: penaliza Trust Score en 10 puntos.
A28	PENALIZACIÓN_MFN
D28	Activado si brecha MFN > 15%. Actualmente: fidelidad ~97% → sin penalización.
A29	TRUST_AJUSTADO_SIAP_ICPI
D29	Trust Score efectivo con penalización narrativa aplicada (si brecha>15% → -10pts).
A30	IET_STATUS
D30	Clasificación de Equidad Territorial (H42). Desviación >20% activa SAT-VIII en H75.
A31	Vi_SINÁPTICO_PROMEDIO
D31	Vi promedio sináptico de 25 metas (H25). Umbral crítico: 0.85. Vi < 0.85 activa SAT-VII en H75.
A32	ODS_ALINEACION_PROMEDIO
D32	Score promedio de alineación ODS de las 25 metas PDOT (H11). Alimenta elegibilidad de fondos internacionales en H69.
```