# H71_EP_ADSCRITAS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=32 · pobladas=27 · fórmulas=37
inputs(lee de): H01_PARÁMETROS, H04_S2_PLANIFICACIÓN_PDOT, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): —
refs no resueltas: #H00_ÍNDICE, #REF
ERRORES: B8: #REF!
MARCADORES: A3: Módulo EP: Evalúa las entidades satélite del GAD bajo el principio de  · A32: Las EPs en 🔴 DESVINCULACIÓN TOTAL informan a H01!TBL_CALIBRACION_Ci pa

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=SUMPRODUCT((LEN(TBL_ENTIDADES_ADSCRITAS[ID_Entidad])>0)*(LEFT(TBL_ENTIDADES_ADSCRITAS[ID_Entidad],3)<>"NEW"))
B7	=H01_PARÁMETROS!B13
B8	=IFERROR(COUNTIF(#REF!,"✅ OPERATIVA")/SUMPRODUCT((LEFT(TBL_ENTIDADES_ADSCRITAS[ID_Entidad],3)<>"NEW")*1),0)
B13	=IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F13	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!M15:M39,"ENTE-04"),0)
G13	=IF(AND(C13="❌ NO",D13=0),"🔴 DESVINCULACIÓN TOTAL",IF(C13="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI","✅ OPERATIVA"))
H13	=IF(G13="🔴 DESVINCULACIÓN TOTAL","⚠️ RIESGO: "&IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?")&" "&IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"Ley?")&" — Contraloría puede observar gasto sin alineación PDOT",IF(G13="🟡 VULNERABILIDAD NORMATIVA — Sin PEI","ℹ️ Formalizar PEI antes de rendición de cuentas. "&IFERROR(VLOOKUP(A13,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?"),""))
B14	=IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
G14	=IF(AND(C14="❌ NO",D14=0),"🔴 DESVINCULACIÓN TOTAL",IF(C14="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI","✅ OPERATIVA"))
H14	=IF(G14="🔴 DESVINCULACIÓN TOTAL","⚠️ RIESGO: "&IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?")&" "&IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"Ley?")&" — Contraloría puede observar gasto sin alineación PDOT",IF(G14="🟡 VULNERABILIDAD NORMATIVA — Sin PEI","ℹ️ Formalizar PEI antes de rendición de cuentas. "&IFERROR(VLOOKUP(A14,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?"),""))
B15	=IFERROR(VLOOKUP(A15,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F15	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!M15:M39,"ENTE-02"),0)
G15	=IF(AND(C15="❌ NO",D15=0),"🔴 DESVINCULACIÓN TOTAL",IF(C15="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI","✅ OPERATIVA"))
H15	=IF(G15="🔴 DESVINCULACIÓN TOTAL","⚠️ RIESGO: "&IFERROR(VLOOKUP(A15,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?")&" "&IFERROR(VLOOKUP(A15,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"Ley?")&" — Contraloría puede observar gasto sin alineación PDOT",IF(G15="🟡 VULNERABILIDAD NORMATIVA — Sin PEI","ℹ️ Formalizar PEI antes de rendición de cuentas. "&IFERROR(VLOOKUP(A15,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?"),""))
B16	=IFERROR(VLOOKUP(A16,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F16	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!M15:M39,"ENTE-03"),0)
G16	=IF(AND(C16="❌ NO",D16=0),"🔴 DESVINCULACIÓN TOTAL",IF(C16="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI","✅ OPERATIVA"))
H16	=IF(G16="🔴 DESVINCULACIÓN TOTAL","⚠️ RIESGO: "&IFERROR(VLOOKUP(A16,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?")&" "&IFERROR(VLOOKUP(A16,TBL_ENTIDADES_ADSCRITAS[],4,FALSE),"Ley?")&" — Contraloría puede observar gasto sin alineación PDOT",IF(G16="🟡 VULNERABILIDAD NORMATIVA — Sin PEI","ℹ️ Formalizar PEI antes de rendición de cuentas. "&IFERROR(VLOOKUP(A16,TBL_ENTIDADES_ADSCRITAS[],5,FALSE),"Art.?"),""))
B17	=IFERROR(VLOOKUP(A17,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F17	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!G:G,A17),0)
G17	=IF(A17="NEW-01","⬜ Sin registrar",IF(AND(C17="❌ NO",D17=0),"🔴 DESVINCULACIÓN TOTAL",IF(C17="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI",IF(C17="✅ SÍ","✅ OPERATIVA","⬜ Sin registrar"))))
B18	=IFERROR(VLOOKUP(A18,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F18	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!G:G,A18),0)
G18	=IF(VLOOKUP(A18,TBL_ENTIDADES_ADSCRITAS[],2,FALSE)="(espacio abierto)","⬜ Sin registrar",IF(AND(C18="❌ NO",D18=0),"🔴 DESVINCULACIÓN TOTAL",IF(C18="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI",IF(C18="✅ SÍ","✅ OPERATIVA","⬜ Sin registrar"))))
B19	=IFERROR(VLOOKUP(A19,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F19	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!G:G,A19),0)
G19	=IF(VLOOKUP(A19,TBL_ENTIDADES_ADSCRITAS[],2,FALSE)="(espacio abierto)","⬜ Sin registrar",IF(AND(C19="❌ NO",D19=0),"🔴 DESVINCULACIÓN TOTAL",IF(C19="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI",IF(C19="✅ SÍ","✅ OPERATIVA","⬜ Sin registrar"))))
B20	=IFERROR(VLOOKUP(A20,TBL_ENTIDADES_ADSCRITAS[],2,FALSE),"")
F20	=IFERROR(COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!G:G,A20),0)
G20	=IF(VLOOKUP(A20,TBL_ENTIDADES_ADSCRITAS[],2,FALSE)="(espacio abierto)","⬜ Sin registrar",IF(AND(C20="❌ NO",D20=0),"🔴 DESVINCULACIÓN TOTAL",IF(C20="❌ NO","🟡 VULNERABILIDAD NORMATIVA — Sin PEI",IF(C20="✅ SÍ","✅ OPERATIVA","⬜ Sin registrar"))))
B23	=COUNTIF(G13:G20,"✅ OPERATIVA")
B24	=COUNTIF(G13:G20,"🟡*")
B25	=COUNTIF(G13:G20,"🔴*")
B26	=IF(B25>0,"🔴 ALERTA — "&B25&" entidad(es) en Desvinculación Total",IF(B24>0,"🟡 ATENCIÓN — "&B24&" entidad(es) sin PEI pero operativa(s)","✅ Todas las EPs operativas"))
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H71_EP_ADSCRITAS
A2	H71 — RADAR DE ENTIDADES ADSCRITAS Y EMPRESAS PÚABLICAS
A3	Módulo EP: Evalúa las entidades satélite del GAD bajo el principio de Presunción Operativa. No penaliza la falta formal si existe impacto territorial real. Doble condición activa solo en Desvinculación Total. Fuente: TBL_ENTIDADES_ADSCRITAS (H01 Sección O).
A5	▌ PARÁMETROS H71
A6	Total_Entidades
C6	Entidades reales registradas (excluye slots NEW-xx sin RUC activo). Actual: 4
I6	Ti_G7+G8_%
A7	Año_Evaluación
A8	Umbral_Impacto_Territorial
C8	% entidades con ✅ OPERATIVA / total entidades activas. Actual: 3/4 = 75%
A9	Fuente_Ley_EP
B9	"LOEP (EP Aseo, EP Hábitat) · COESCOP (Cuerpo de Bomberos) · LOSEP (Patronato) · COOTAD Art.343 (procesos desconcentrados)"
C9	Marco legal diferenciado por naturaleza jurídica de cada entidad
A11	▌ TABLA DE EVALUACIÓN EP — TBL_RADAR_EP
A12	ID_Entidad
B12	Nombre_Entidad
C12	Tiene_PEI
D12	Impacto_Territorial_%
E12	Monto_Ejecutado_USD
F12	Metas_PDOT_Vinculadas
G12	Estado_EP
H12	Alerta_Normativa
A13	EP-01
C13	✅ SÍ
D13	0.85
E13	245000
I13	0.177379
A14	EP-02
C14	❌ NO
D14	0.45
E14	98000
F14	0
A15	AD-01
C15	✅ SÍ
D15	0.92
E15	312000
I15	0.097128
A16	CB-01
C16	✅ SÍ
D16	0.78
E16	178000
I16	0
A17	NEW-01
D17	0
E17	0
H17	(slot disponible — completar B17 y H01 Sección O)
A18	NEW-02
D18	0
E18	0
H18	(slot disponible)
A19	NEW-03
D19	0
E19	0
H19	(slot disponible)
A20	NEW-04
D20	0
E20	0
H20	(slot disponible)
A22	▌ RESUMEN RADAR EP
A23	EPs en ✅ OPERATIVA
A24	EPs en 🟡 VULNERABILIDAD
A25	EPs en 🔴 DESVINCULACIÓN
A26	Estado_Global_EP
A28	▌ NOTA METODOLÓGICA — PRINCIPIO DE PRESUNCIÓN OPERATIVA
A29	SIAP-ICPI respeta el trabajo real de las EPs en el territorio. La ausencia de PEI es una vulnerabilidad formal, no una falla operativa. Solo la combinación de sin-PEI + impacto-cero activa la deducción Ci. Las entidades 🟡 reciben asesoría preventiva — no penalización. Principio D7: lenguaje 100% preventivo.
A31	▌ IMPACTO EN ICPI — LECTURA REFERENCIAL (solo informativo)
A32	Las EPs en 🔴 DESVINCULACIÓN TOTAL informan a H01!TBL_CALIBRACION_Ci para consideración en la próxima actualización del Ci_Manual. Esta hoja NO modifica directamente ningún valor de H12 ni H01 Secciones A-M. Cualquier ajuste a Ci requiere decisión explícita del equipo DYLUS LAB + recalibración formal del axioma.
```