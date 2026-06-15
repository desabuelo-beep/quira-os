# H23_SAT-III — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=15 · fórmulas=14
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H75_SAT_ENGINE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B53
B7	=H01_PARÁMETROS!B52
B8	=COUNTIF(H07_S5_FINANCIERO_eSIGEF!C7:C31,"<"&B6)
B9	=IFERROR(AVERAGE(H07_S5_FINANCIERO_eSIGEF!C7:C31),0)
B10	=IF(ISNUMBER(B9),"✅ Ti_Promedio es número","❌ ERROR: Ti_Promedio devuelve texto — verificar referencia H07")
B13	=IF(B8>=B7,"⚠️ SAT-III ACTIVO — "&B8&" metas con riesgo de sub-ejecución","✅ Sin señal SAT-III")
B15	=IF(B8>=B7,"Se detectan "&B8&" metas con ejecución financiera inferior al "&TEXT(B6,"0%")&" del codificado. Revisar cronograma y eliminar bloqueos operativos para fortalecer el avance. Ref: COPFP Arts.115-117.","Ejecución financiera dentro de rangos aceptables. Sin señales de parálisis presupuestaria.")
A19	=IFERROR(H12_MOTOR_ICPI_CANÓNICO!A6,"")
C19	=H01_PARÁMETROS!B53
D19	=IF(B19<H01_PARÁMETROS!B53,"⚠️ Riesgo de sub-ejecución","✅ Ejecución dentro de rango")
E19	=IF(B19<H01_PARÁMETROS!B53,"Meta con baja ejecución financiera. Revisar cronograma y eliminar bloqueos operativos para fortalecer el avance.","Sin señal SAT-III.")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H23_SAT-III
A2	H23 — SAT-III — PARÁLISIS PRESUPUESTARIA
A3	Detecta metas con devengado inferior al 10% del codificado. Indica riesgo de sub-ejecución. Fundamentación: COPFP Arts.115-117.
A5	▌ PARÁMETROS SAT-III
A6	SAT_III_Umbral_Deveng
C6	Devengado mínimo (H01!B53=10%)
A7	SAT_III_Umbral_Cumpl
C7	Nº metas en riesgo para alerta (H01!B52=5)
A8	Metas_Con_Paralisis
C8	Metas con Ti < umbral (conteo dinámico desde H07)
A9	Ti_Promedio_Global
C9	★ FALLA 16 PREVENIDA: fórmula numérica IFERROR(AVERAGE(H07!C7:C31),0) — NUNCA referencia a texto
A10	Validación_Ti_Es_Número
C10	Guardia FALLA 16 — verificación ESNUMERO()
A12	▌ ESTADO SAT-III
A13	SAT-III_Estado
A15	▌ DIAGNÓSTICO PREVENTIVO SAT-III
A17	▌ TABLA DE METAS EN RIESGO SAT-III
A18	ID_Meta
B18	Ti_Actual
C18	Umbral_Deveng
D18	Estado_SAT_III
E18	Diagnóstico_Preventivo
```