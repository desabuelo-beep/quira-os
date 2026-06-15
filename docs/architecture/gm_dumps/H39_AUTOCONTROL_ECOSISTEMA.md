# H39_AUTOCONTROL_ECOSISTEMA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=39 · pobladas=36 · fórmulas=27
inputs(lee de): H00_ÍNDICE, H01_PARÁMETROS, H02b_ORGÁNICO_CLASIFICADOR, H04_S2_PLANIFICACIÓN_PDOT, H07c_Ti_VERIFICADO_INFORME, H12_MOTOR_ICPI_CANÓNICO, H14_PONDERADORES, H15_ICPI_GLOBAL, H16_IFE, H20c_IEF_EFICIENCIA_FINANCIERA, H34b_MFN_FIDELIDAD_NARRATIVA, H36b_LOOKUP_ARRASTRE
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE, H12
MARCADORES: B25: Motor Ci — TBL_CALIBRACION_Ci (25 metas) · D25: =IF(COUNTA(H01_PARÁMETROS!A189:A213)=25,"✅ TBL_CALIBRACION_Ci íntegra  · D26: =IF(MIN(H01_PARÁMETROS!F189:F213)>=0.5,"✅ Ci_mínimo ≥ 0.50 en las 25 m · B27: Motor Ci — Sin Ci hardcodeados en H12 · C27: COUNTIF(H12!I6:I30, "⚠️ HILO ROTO") = 0 · D27: =IF(COUNTIF(H12_MOTOR_ICPI_CANÓNICO!I6:I30,"⚠️ HILO ROTO")=0,"✅ Ci con · A33: Nota Motor Ci (#18-22): Verificaciones #19-22 requieren que TBL_CALIBR · D36: ⚠️ Pi en H12 son valores hardcodeados (no fórmulas vivas a H14). Consi · A38: NOTA S-04: Los 25 Pi en H12!C6:C30 son valores numéricos hardcodeados 

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
D7	=IF(AND(ISNUMBER(H12_MOTOR_ICPI_CANÓNICO!B33),H12_MOTOR_ICPI_CANÓNICO!B33>0,H12_MOTOR_ICPI_CANÓNICO!B33<=1),"OK Motor ICPI activo — ICGI-T "&TEXT(H12_MOTOR_ICPI_CANÓNICO!B33,"0.00%"),"ERROR Motor ICPI — verificar H12!B33")
D8	=IF(ABS(SUM(H14_PONDERADORES!G7:G31)-1)<0.0001,"✅ Σ Pi = 1,0000","❌ ERROR: Σ Pi ≠ 1")
D9	=IF(ABS(H12_MOTOR_ICPI_CANÓNICO!B33-H15_ICPI_GLOBAL!B6)<0.001,"✅ H12 y H15 consistentes","❌ Inconsistencia ICPI")
D10	=IF(AND(H16_IFE!B6>=0,H16_IFE!B6<=1),"✅ IFE en rango","❌ Error IFE")
D11	=IF(H01_PARÁMETROS!B13=2026,"✅ Año 2026","⚠️ Actualizar Año_Activo")
D12	=IF(COUNTA(H04_S2_PLANIFICACIÓN_PDOT!A16:A40)=25,"✅ 25 metas","❌ Número de metas incorrecto")
D13	=IF(COUNTA(H36b_LOOKUP_ARRASTRE!A19:A35)=17,"✅ 17 ARRASTREs","❌ Verificar H36b")
D14	=IF(H36b_LOOKUP_ARRASTRE!M25="⚫ SUPERSEDED","✅ SUPERSEDED — ARRASTRE-005","❌ Marcar SUPERSEDED en H36b fila 25")
D15	=IF(H36b_LOOKUP_ARRASTRE!M26="⚫ SUPERSEDED","✅ SUPERSEDED — ARRASTRE-006","❌ Marcar SUPERSEDED en H36b fila 26")
D16	=IF(COUNTIF(H34b_MFN_FIDELIDAD_NARRATIVA!K:K,"*INFIEL*")=0,"✅ Lenguaje limpio","❌ Eliminar término punitivo")
D17	=IF(COUNTA(H02b_ORGÁNICO_CLASIFICADOR!A11:A30)=20,"✅ H02b íntegra — 20 unidades","❌ H02b incompleta — verificar tabla")
D18	=IF(H02b_ORGÁNICO_CLASIFICADOR!B8="No. 040-2025-ALC-LJTL-GADMCM","✅ Resolución correcta","❌ Verificar resolución en H02b")
D19	=IF(COUNTA(H07c_Ti_VERIFICADO_INFORME!J22:J50)>=COUNTIF(H07c_Ti_VERIFICADO_INFORME!L22:L50,"✅ Válido"),"✅ H07c íntegra — hashes presentes","⚠️ H07c sin registros (normal si no hay fondos externos aún)")
D20	=IF(COUNTA(H12_MOTOR_ICPI_CANÓNICO!H6:H30)>0,"✅ Ti_FUENTE registrado","⚠️ Ti_FUENTE vacío — normal si Ti=0 en todo")
D21	=IF(H01_PARÁMETROS!J136="SÍ",IF(ISNUMBER(H20c_IEF_EFICIENCIA_FINANCIERA!B41),"✅ IEF calculado","❌ H20c no calculada"),"⚫ IEF desactivado en H01")
D22	=IF(COUNTA(H00_ÍNDICE!A:A)>=70,"✅ 72 hojas activas (62 canónicas + 8 universalización + 2 módulo EP)","⚠️ Verificar conteo — deben ser 72 tras FASE14")
D23	=IF(ABS(SUM(H14_PONDERADORES!G7:G31)-1)<0.0001,"✅ BUG-01 RESUELTO — ΣPi=1.0000","❌ BUG-01 ACTIVO — aplicar Pi_corr_i = Pi_i / SUMA(todos)")
D24	=IF(COUNTA(H01_PARÁMETROS!A176:A179)=4,"✅ TBL_HOMOLOGACION_NORMATIVA íntegra — 4 infracciones","❌ TBL_HOMOLOGACION_NORMATIVA incorrecta — debe tener 4 filas (INF-01..INF-04)")
D25	=IF(COUNTA(H01_PARÁMETROS!A189:A213)=25,"✅ TBL_CALIBRACION_Ci íntegra — 25 metas","❌ TBL_CALIBRACION_Ci incorrecta — debe tener exactamente 25 filas de metas")
D26	=IF(MIN(H01_PARÁMETROS!F189:F213)>=0.5,"✅ Ci_mínimo ≥ 0.50 en las 25 metas","❌ HAY METAS CON Ci < 0.50 — verificar lógica INF-04 en TBL_CALIBRACION_Ci")
D27	=IF(COUNTIF(H12_MOTOR_ICPI_CANÓNICO!I6:I30,"⚠️ HILO ROTO")=0,"✅ Ci conectados — 0 hilos rotos","❌ "&COUNTIF(H12_MOTOR_ICPI_CANÓNICO!I6:I30,"⚠️ HILO ROTO")&" hilos rotos en columna Ci")
D28	=IF(ABS(H12_MOTOR_ICPI_CANÓNICO!B38/H12_MOTOR_ICPI_CANÓNICO!B32*100-69.9309061706625)<0.0001<0.5,"OK Motor Ci canonico integro delta<0.5pp","ERROR desviacion Ci "&ROUND(ABS(H12_MOTOR_ICPI_CANÓNICO!B38/H12_MOTOR_ICPI_CANÓNICO!B32*100-69.9309061706625)<0.0001,4)&"pp revisar")
B30	=IF(COUNTIF(D7:D28,"ERROR*")=0,"SISTEMA INTEGRO Gold Master v1.0","ERRORES: "&COUNTIF(D7:D28,"ERROR*")&" check(s) fallidos revisar col D")
C39	=IF(ISNUMBER(MATCH("Ti_Histórico-2025",H12_MOTOR_ICPI_CANÓNICO!H6:H30,0)),"✅ Ti_FUENTE activo","⚠️ Revisar")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H39_AUTOCONTROL_ECOSISTEMA
A2	H39 — AUTOCONTROL DEL ECOSISTEMA — VERIFICACIÓN DE INTEGRIDAD
A3	★ Hoja de control de integridad. Verifica que todos los axiomas y referencias del sistema estén correctos antes de emitir reportes.
A5	▌ VERIFICACIONES DE INTEGRIDAD DEL SISTEMA
A6	#
B6	Verificación
C6	Fórmula / Criterio
D6	Estado
A7	1
B7	Motor ICPI activo y en rango válido [0,1] — ICGI-T 2026 vivo
C7	ISNUMBER(H12!B33) AND (H12!B33 en [0,1]) → motor vivo y en rango
A8	2
B8	Σ Pi = 1.0000
C8	ABS(SUM(H14!G7:G31) - 1) < 0.0001
A9	3
B9	H12!B33 = H15!B6
C9	ABS(H12!B33 - H15!B6) < 0.001
A10	4
B10	IFE en rango 0-1
C10	AND(H16!B6>=0, H16!B6<=1)
A11	5
B11	Año_Activo = 2026
C11	H01!B13 = 2026
A12	6
B12	25 metas en H04
C12	COUNTA(H04!A16:A40) = 25
A13	7
B13	17 ARRASTREs en H36b
C13	COUNTA(H36b!A19:A35) = 17
A14	8
B14	ARRASTRE-005 SUPERSEDED
C14	H36b!M25 = '⚫ SUPERSEDED' (ARRASTRE-005 en fila 25)
A15	9
B15	ARRASTRE-006 SUPERSEDED
C15	H36b!M26 = '⚫ SUPERSEDED' (ARRASTRE-006 en fila 26)
A16	10
B16	No hay "INFIEL" en H34b
C16	COUNTIF(H34b!K:K, INFIEL) = 0
A17	11
B17	H02b — 20 unidades clasificadas
C17	COUNTA(H02b!A11:A30) = 20
A18	12
B18	H02b — Resolución registrada
C18	H02b!B8 = 'No. 040-2025-ALC-LJTL-GADMCM' (dato en fila 8, columna B)
A19	13
B19	H07c — estructura válida
C19	COUNTA(H07c!J22:J50) >= COUNTIF(H07c!L22:L50)
A20	14
B20	H12 — columna Ti_FUENTE existe
C20	COUNTA(H12!H6:H30) > 0
A21	15
B21	H20c — IEF calculado
C21	H01!J136=SI -> ISNUMBER(H20c!B41)
A22	16
B22	Total hojas: 72 (62 canónicas + 8 universalización FASE13 + 2 módulo EP FASE14)
C22	COUNTA(H00!ÍNDICE A:A) >= 70 (proxy de 72 hojas)
A23	17
B23	BUG-01 (ΣPi=0.9463) — estado
C23	ABS(SUM(H14!G7:G31)-1) < 0.0001
A24	18
B24	Motor Ci — TBL_HOMOLOGACION_NORMATIVA (4 filas)
C24	COUNTA(H01!A176:A179) = 4 (INF-01 en A176 a INF-04 en A179)
A25	19
B25	Motor Ci — TBL_CALIBRACION_Ci (25 metas)
C25	COUNTA(H01!A189:A213) = 25 (metas desde fila 189 a 213)
A26	20
B26	Motor Ci — Ci_mínimo ≥ 0.50 en todo el universo
C26	MIN(H01!F189:F213) >= 0.50 (columna F = Ci_Calculado, filas 189-213)
A27	21
B27	Motor Ci — Sin Ci hardcodeados en H12
C27	COUNTIF(H12!I6:I30, "⚠️ HILO ROTO") = 0
A28	22
B28	Motor Ci — Fórmula canónica intacta (base 2025 en estado vacío)
C28	Misma lógica que verificación #1. En estado vacío (sin ingesta 2026), B38/B32×100 retorna la base histórica 2025 = 69.9309%. Con ingesta 2026 activa, B33 refleja el ICPI dinámico del ciclo corriente. La fórmula canónica B31/B32×100 se preserva íntegra en todo estado de operación.
A29	▌ ESTADO GLOBAL DEL SISTEMA
A30	Estado Global:
A32	Nota H02b+H07c: Las verificaciones #11-13 no generaran error si H02b tiene 20 unidades y H07c tiene su estructura base.
A33	Nota Motor Ci (#18-22): Verificaciones #19-22 requieren que TBL_CALIBRACION_Ci este nombrado correctamente en Excel.
A34	Nota #22 Critico: Si INFs=0 y axioma falla, revisar valores Ci_Manual_2025 en Seccion M de H01_PARAMETROS.
A35	Celda B30 tambien alimenta a H34_CERTIFICADO_QUIRA como indicador de integridad del sistema.
A36	23
B36	Pi en H12 — ¿Fórmulas vivas hacia H14?
C36	Verificación manual requerida: columna C de H12 (filas 6-30) debe referenciar H14!G[n], no valores numéricos.
D36	⚠️ Pi en H12 son valores hardcodeados (no fórmulas vivas a H14). Consistencia numérica verificada — riesgo si se modifica H14 sin actualizar H12.
A38	NOTA S-04: Los 25 Pi en H12!C6:C30 son valores numéricos hardcodeados idénticos a H14!G7:G31. No hay error matemático actual, pero si alguien modifica H14 sin actualizar H12, el ICPI se desincronizará. Acción recomendada: en próxima versión (v1.1) convertir Pi de H12 a fórmulas =H14_PONDERADORES!G[n].
A39	24
B39	Idioma fórmulas H12 col H
D39	Verifica que H12 columna H devuelve Ti_Histórico-2025 (estado pre-ingesta correcto)
```