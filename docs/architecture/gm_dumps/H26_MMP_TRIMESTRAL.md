# H26_MMP_TRIMESTRAL — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=51 · pobladas=43 · fórmulas=328
inputs(lee de): H01_PARÁMETROS, H07_S5_FINANCIERO_eSIGEF, H12_MOTOR_ICPI_CANÓNICO, H25_MMP_MENSUAL
outputs(alimenta a): H00_ÍNDICE, H27_MMP_ANUAL
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
A11	=H25_MMP_MENSUAL!A11
B11	=H25_MMP_MENSUAL!B11
C11	=H25_MMP_MENSUAL!C11
D11	=H25_MMP_MENSUAL!D11
E11	=H25_MMP_MENSUAL!F11
F11	=SUM(H25_MMP_MENSUAL!G11:I11)
G11	=SUM(H25_MMP_MENSUAL!J11:L11)
H11	=SUM(H25_MMP_MENSUAL!M11:O11)
I11	=SUM(H25_MMP_MENSUAL!P11:R11)
J11	=IF(E11=0,0,SUM(F11:I11)/E11)
K11	=IF(J11>=0.9,"🔵 Excelencia en Gobernanza",IF(J11>=0.7,"🟢 Gestión por Mandato",IF(J11>=0.4,"🟡 Transición Crítica",IF(J11>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L11	=IF(E11=0,"⬜ Sin meta",IF(H11/IF(E11=0,1,E11)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A12	=H25_MMP_MENSUAL!A12
B12	=H25_MMP_MENSUAL!B12
C12	=H25_MMP_MENSUAL!C12
D12	=H25_MMP_MENSUAL!D12
E12	=H25_MMP_MENSUAL!F12
F12	=SUM(H25_MMP_MENSUAL!G12:I12)
G12	=SUM(H25_MMP_MENSUAL!J12:L12)
H12	=SUM(H25_MMP_MENSUAL!M12:O12)
I12	=SUM(H25_MMP_MENSUAL!P12:R12)
J12	=IF(E12=0,0,SUM(F12:I12)/E12)
K12	=IF(J12>=0.9,"🔵 Excelencia en Gobernanza",IF(J12>=0.7,"🟢 Gestión por Mandato",IF(J12>=0.4,"🟡 Transición Crítica",IF(J12>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L12	=IF(E12=0,"⬜ Sin meta",IF(H12/IF(E12=0,1,E12)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A13	=H25_MMP_MENSUAL!A13
B13	=H25_MMP_MENSUAL!B13
C13	=H25_MMP_MENSUAL!C13
D13	=H25_MMP_MENSUAL!D13
E13	=H25_MMP_MENSUAL!F13
F13	=SUM(H25_MMP_MENSUAL!G13:I13)
G13	=SUM(H25_MMP_MENSUAL!J13:L13)
H13	=SUM(H25_MMP_MENSUAL!M13:O13)
I13	=SUM(H25_MMP_MENSUAL!P13:R13)
J13	=IF(E13=0,0,SUM(F13:I13)/E13)
K13	=IF(J13>=0.9,"🔵 Excelencia en Gobernanza",IF(J13>=0.7,"🟢 Gestión por Mandato",IF(J13>=0.4,"🟡 Transición Crítica",IF(J13>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L13	=IF(E13=0,"⬜ Sin meta",IF(H13/IF(E13=0,1,E13)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A14	=H25_MMP_MENSUAL!A14
B14	=H25_MMP_MENSUAL!B14
C14	=H25_MMP_MENSUAL!C14
D14	=H25_MMP_MENSUAL!D14
E14	=H25_MMP_MENSUAL!F14
F14	=SUM(H25_MMP_MENSUAL!G14:I14)
G14	=SUM(H25_MMP_MENSUAL!J14:L14)
H14	=SUM(H25_MMP_MENSUAL!M14:O14)
I14	=SUM(H25_MMP_MENSUAL!P14:R14)
J14	=IF(E14=0,0,SUM(F14:I14)/E14)
K14	=IF(J14>=0.9,"🔵 Excelencia en Gobernanza",IF(J14>=0.7,"🟢 Gestión por Mandato",IF(J14>=0.4,"🟡 Transición Crítica",IF(J14>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L14	=IF(E14=0,"⬜ Sin meta",IF(H14/IF(E14=0,1,E14)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A15	=H25_MMP_MENSUAL!A15
B15	=H25_MMP_MENSUAL!B15
C15	=H25_MMP_MENSUAL!C15
D15	=H25_MMP_MENSUAL!D15
E15	=H25_MMP_MENSUAL!F15
F15	=SUM(H25_MMP_MENSUAL!G15:I15)
G15	=SUM(H25_MMP_MENSUAL!J15:L15)
H15	=SUM(H25_MMP_MENSUAL!M15:O15)
I15	=SUM(H25_MMP_MENSUAL!P15:R15)
J15	=IF(E15=0,0,SUM(F15:I15)/E15)
K15	=IF(J15>=0.9,"🔵 Excelencia en Gobernanza",IF(J15>=0.7,"🟢 Gestión por Mandato",IF(J15>=0.4,"🟡 Transición Crítica",IF(J15>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L15	=IF(E15=0,"⬜ Sin meta",IF(H15/IF(E15=0,1,E15)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A16	=H25_MMP_MENSUAL!A16
B16	=H25_MMP_MENSUAL!B16
C16	=H25_MMP_MENSUAL!C16
D16	=H25_MMP_MENSUAL!D16
E16	=H25_MMP_MENSUAL!F16
F16	=SUM(H25_MMP_MENSUAL!G16:I16)
G16	=SUM(H25_MMP_MENSUAL!J16:L16)
H16	=SUM(H25_MMP_MENSUAL!M16:O16)
I16	=SUM(H25_MMP_MENSUAL!P16:R16)
J16	=IF(E16=0,0,SUM(F16:I16)/E16)
K16	=IF(J16>=0.9,"🔵 Excelencia en Gobernanza",IF(J16>=0.7,"🟢 Gestión por Mandato",IF(J16>=0.4,"🟡 Transición Crítica",IF(J16>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L16	=IF(E16=0,"⬜ Sin meta",IF(H16/IF(E16=0,1,E16)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A17	=H25_MMP_MENSUAL!A17
B17	=H25_MMP_MENSUAL!B17
C17	=H25_MMP_MENSUAL!C17
D17	=H25_MMP_MENSUAL!D17
E17	=H25_MMP_MENSUAL!F17
F17	=SUM(H25_MMP_MENSUAL!G17:I17)
G17	=SUM(H25_MMP_MENSUAL!J17:L17)
H17	=SUM(H25_MMP_MENSUAL!M17:O17)
I17	=SUM(H25_MMP_MENSUAL!P17:R17)
J17	=IF(E17=0,0,SUM(F17:I17)/E17)
K17	=IF(J17>=0.9,"🔵 Excelencia en Gobernanza",IF(J17>=0.7,"🟢 Gestión por Mandato",IF(J17>=0.4,"🟡 Transición Crítica",IF(J17>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L17	=IF(E17=0,"⬜ Sin meta",IF(H17/IF(E17=0,1,E17)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A18	=H25_MMP_MENSUAL!A18
B18	=H25_MMP_MENSUAL!B18
C18	=H25_MMP_MENSUAL!C18
D18	=H25_MMP_MENSUAL!D18
E18	=H25_MMP_MENSUAL!F18
F18	=SUM(H25_MMP_MENSUAL!G18:I18)
G18	=SUM(H25_MMP_MENSUAL!J18:L18)
H18	=SUM(H25_MMP_MENSUAL!M18:O18)
I18	=SUM(H25_MMP_MENSUAL!P18:R18)
J18	=IF(E18=0,0,SUM(F18:I18)/E18)
K18	=IF(J18>=0.9,"🔵 Excelencia en Gobernanza",IF(J18>=0.7,"🟢 Gestión por Mandato",IF(J18>=0.4,"🟡 Transición Crítica",IF(J18>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L18	=IF(E18=0,"⬜ Sin meta",IF(H18/IF(E18=0,1,E18)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A19	=H25_MMP_MENSUAL!A19
B19	=H25_MMP_MENSUAL!B19
C19	=H25_MMP_MENSUAL!C19
D19	=H25_MMP_MENSUAL!D19
E19	=H25_MMP_MENSUAL!F19
F19	=SUM(H25_MMP_MENSUAL!G19:I19)
G19	=SUM(H25_MMP_MENSUAL!J19:L19)
H19	=SUM(H25_MMP_MENSUAL!M19:O19)
I19	=SUM(H25_MMP_MENSUAL!P19:R19)
J19	=IF(E19=0,0,SUM(F19:I19)/E19)
K19	=IF(J19>=0.9,"🔵 Excelencia en Gobernanza",IF(J19>=0.7,"🟢 Gestión por Mandato",IF(J19>=0.4,"🟡 Transición Crítica",IF(J19>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L19	=IF(E19=0,"⬜ Sin meta",IF(H19/IF(E19=0,1,E19)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A20	=H25_MMP_MENSUAL!A20
B20	=H25_MMP_MENSUAL!B20
C20	=H25_MMP_MENSUAL!C20
D20	=H25_MMP_MENSUAL!D20
E20	=H25_MMP_MENSUAL!F20
F20	=SUM(H25_MMP_MENSUAL!G20:I20)
G20	=SUM(H25_MMP_MENSUAL!J20:L20)
H20	=SUM(H25_MMP_MENSUAL!M20:O20)
I20	=SUM(H25_MMP_MENSUAL!P20:R20)
J20	=IF(E20=0,0,SUM(F20:I20)/E20)
K20	=IF(J20>=0.9,"🔵 Excelencia en Gobernanza",IF(J20>=0.7,"🟢 Gestión por Mandato",IF(J20>=0.4,"🟡 Transición Crítica",IF(J20>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L20	=IF(E20=0,"⬜ Sin meta",IF(H20/IF(E20=0,1,E20)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A21	=H25_MMP_MENSUAL!A21
B21	=H25_MMP_MENSUAL!B21
C21	=H25_MMP_MENSUAL!C21
D21	=H25_MMP_MENSUAL!D21
E21	=H25_MMP_MENSUAL!F21
F21	=SUM(H25_MMP_MENSUAL!G21:I21)
G21	=SUM(H25_MMP_MENSUAL!J21:L21)
H21	=SUM(H25_MMP_MENSUAL!M21:O21)
I21	=SUM(H25_MMP_MENSUAL!P21:R21)
J21	=IF(E21=0,0,SUM(F21:I21)/E21)
K21	=IF(J21>=0.9,"🔵 Excelencia en Gobernanza",IF(J21>=0.7,"🟢 Gestión por Mandato",IF(J21>=0.4,"🟡 Transición Crítica",IF(J21>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L21	=IF(E21=0,"⬜ Sin meta",IF(H21/IF(E21=0,1,E21)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A22	=H25_MMP_MENSUAL!A22
B22	=H25_MMP_MENSUAL!B22
C22	=H25_MMP_MENSUAL!C22
D22	=H25_MMP_MENSUAL!D22
E22	=H25_MMP_MENSUAL!F22
F22	=SUM(H25_MMP_MENSUAL!G22:I22)
G22	=SUM(H25_MMP_MENSUAL!J22:L22)
H22	=SUM(H25_MMP_MENSUAL!M22:O22)
I22	=SUM(H25_MMP_MENSUAL!P22:R22)
J22	=IF(E22=0,0,SUM(F22:I22)/E22)
K22	=IF(J22>=0.9,"🔵 Excelencia en Gobernanza",IF(J22>=0.7,"🟢 Gestión por Mandato",IF(J22>=0.4,"🟡 Transición Crítica",IF(J22>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L22	=IF(E22=0,"⬜ Sin meta",IF(H22/IF(E22=0,1,E22)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A23	=H25_MMP_MENSUAL!A23
B23	=H25_MMP_MENSUAL!B23
C23	=H25_MMP_MENSUAL!C23
D23	=H25_MMP_MENSUAL!D23
E23	=H25_MMP_MENSUAL!F23
F23	=SUM(H25_MMP_MENSUAL!G23:I23)
G23	=SUM(H25_MMP_MENSUAL!J23:L23)
H23	=SUM(H25_MMP_MENSUAL!M23:O23)
I23	=SUM(H25_MMP_MENSUAL!P23:R23)
J23	=IF(E23=0,0,SUM(F23:I23)/E23)
K23	=IF(J23>=0.9,"🔵 Excelencia en Gobernanza",IF(J23>=0.7,"🟢 Gestión por Mandato",IF(J23>=0.4,"🟡 Transición Crítica",IF(J23>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L23	=IF(E23=0,"⬜ Sin meta",IF(H23/IF(E23=0,1,E23)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A24	=H25_MMP_MENSUAL!A24
B24	=H25_MMP_MENSUAL!B24
C24	=H25_MMP_MENSUAL!C24
D24	=H25_MMP_MENSUAL!D24
E24	=H25_MMP_MENSUAL!F24
F24	=SUM(H25_MMP_MENSUAL!G24:I24)
G24	=SUM(H25_MMP_MENSUAL!J24:L24)
H24	=SUM(H25_MMP_MENSUAL!M24:O24)
I24	=SUM(H25_MMP_MENSUAL!P24:R24)
J24	=IF(E24=0,0,SUM(F24:I24)/E24)
K24	=IF(J24>=0.9,"🔵 Excelencia en Gobernanza",IF(J24>=0.7,"🟢 Gestión por Mandato",IF(J24>=0.4,"🟡 Transición Crítica",IF(J24>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L24	=IF(E24=0,"⬜ Sin meta",IF(H24/IF(E24=0,1,E24)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A25	=H25_MMP_MENSUAL!A25
B25	=H25_MMP_MENSUAL!B25
C25	=H25_MMP_MENSUAL!C25
D25	=H25_MMP_MENSUAL!D25
E25	=H25_MMP_MENSUAL!F25
F25	=SUM(H25_MMP_MENSUAL!G25:I25)
G25	=SUM(H25_MMP_MENSUAL!J25:L25)
H25	=SUM(H25_MMP_MENSUAL!M25:O25)
I25	=SUM(H25_MMP_MENSUAL!P25:R25)
J25	=IF(E25=0,0,SUM(F25:I25)/E25)
K25	=IF(J25>=0.9,"🔵 Excelencia en Gobernanza",IF(J25>=0.7,"🟢 Gestión por Mandato",IF(J25>=0.4,"🟡 Transición Crítica",IF(J25>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L25	=IF(E25=0,"⬜ Sin meta",IF(H25/IF(E25=0,1,E25)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A26	=H25_MMP_MENSUAL!A26
B26	=H25_MMP_MENSUAL!B26
C26	=H25_MMP_MENSUAL!C26
D26	=H25_MMP_MENSUAL!D26
E26	=H25_MMP_MENSUAL!F26
F26	=SUM(H25_MMP_MENSUAL!G26:I26)
G26	=SUM(H25_MMP_MENSUAL!J26:L26)
H26	=SUM(H25_MMP_MENSUAL!M26:O26)
I26	=SUM(H25_MMP_MENSUAL!P26:R26)
J26	=IF(E26=0,0,SUM(F26:I26)/E26)
K26	=IF(J26>=0.9,"🔵 Excelencia en Gobernanza",IF(J26>=0.7,"🟢 Gestión por Mandato",IF(J26>=0.4,"🟡 Transición Crítica",IF(J26>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L26	=IF(E26=0,"⬜ Sin meta",IF(H26/IF(E26=0,1,E26)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A27	=H25_MMP_MENSUAL!A27
B27	=H25_MMP_MENSUAL!B27
C27	=H25_MMP_MENSUAL!C27
D27	=H25_MMP_MENSUAL!D27
E27	=H25_MMP_MENSUAL!F27
F27	=SUM(H25_MMP_MENSUAL!G27:I27)
G27	=SUM(H25_MMP_MENSUAL!J27:L27)
H27	=SUM(H25_MMP_MENSUAL!M27:O27)
I27	=SUM(H25_MMP_MENSUAL!P27:R27)
J27	=IF(E27=0,0,SUM(F27:I27)/E27)
K27	=IF(J27>=0.9,"🔵 Excelencia en Gobernanza",IF(J27>=0.7,"🟢 Gestión por Mandato",IF(J27>=0.4,"🟡 Transición Crítica",IF(J27>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L27	=IF(E27=0,"⬜ Sin meta",IF(H27/IF(E27=0,1,E27)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A28	=H25_MMP_MENSUAL!A28
B28	=H25_MMP_MENSUAL!B28
C28	=H25_MMP_MENSUAL!C28
D28	=H25_MMP_MENSUAL!D28
E28	=H25_MMP_MENSUAL!F28
F28	=SUM(H25_MMP_MENSUAL!G28:I28)
G28	=SUM(H25_MMP_MENSUAL!J28:L28)
H28	=SUM(H25_MMP_MENSUAL!M28:O28)
I28	=SUM(H25_MMP_MENSUAL!P28:R28)
J28	=IF(E28=0,0,SUM(F28:I28)/E28)
K28	=IF(J28>=0.9,"🔵 Excelencia en Gobernanza",IF(J28>=0.7,"🟢 Gestión por Mandato",IF(J28>=0.4,"🟡 Transición Crítica",IF(J28>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L28	=IF(E28=0,"⬜ Sin meta",IF(H28/IF(E28=0,1,E28)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A29	=H25_MMP_MENSUAL!A29
B29	=H25_MMP_MENSUAL!B29
C29	=H25_MMP_MENSUAL!C29
D29	=H25_MMP_MENSUAL!D29
E29	=H25_MMP_MENSUAL!F29
F29	=SUM(H25_MMP_MENSUAL!G29:I29)
G29	=SUM(H25_MMP_MENSUAL!J29:L29)
H29	=SUM(H25_MMP_MENSUAL!M29:O29)
I29	=SUM(H25_MMP_MENSUAL!P29:R29)
J29	=IF(E29=0,0,SUM(F29:I29)/E29)
K29	=IF(J29>=0.9,"🔵 Excelencia en Gobernanza",IF(J29>=0.7,"🟢 Gestión por Mandato",IF(J29>=0.4,"🟡 Transición Crítica",IF(J29>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L29	=IF(E29=0,"⬜ Sin meta",IF(H29/IF(E29=0,1,E29)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A30	=H25_MMP_MENSUAL!A30
B30	=H25_MMP_MENSUAL!B30
C30	=H25_MMP_MENSUAL!C30
D30	=H25_MMP_MENSUAL!D30
E30	=H25_MMP_MENSUAL!F30
F30	=SUM(H25_MMP_MENSUAL!G30:I30)
G30	=SUM(H25_MMP_MENSUAL!J30:L30)
H30	=SUM(H25_MMP_MENSUAL!M30:O30)
I30	=SUM(H25_MMP_MENSUAL!P30:R30)
J30	=IF(E30=0,0,SUM(F30:I30)/E30)
K30	=IF(J30>=0.9,"🔵 Excelencia en Gobernanza",IF(J30>=0.7,"🟢 Gestión por Mandato",IF(J30>=0.4,"🟡 Transición Crítica",IF(J30>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L30	=IF(E30=0,"⬜ Sin meta",IF(H30/IF(E30=0,1,E30)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A31	=H25_MMP_MENSUAL!A31
B31	=H25_MMP_MENSUAL!B31
C31	=H25_MMP_MENSUAL!C31
D31	=H25_MMP_MENSUAL!D31
E31	=H25_MMP_MENSUAL!F31
F31	=SUM(H25_MMP_MENSUAL!G31:I31)
G31	=SUM(H25_MMP_MENSUAL!J31:L31)
H31	=SUM(H25_MMP_MENSUAL!M31:O31)
I31	=SUM(H25_MMP_MENSUAL!P31:R31)
J31	=IF(E31=0,0,SUM(F31:I31)/E31)
K31	=IF(J31>=0.9,"🔵 Excelencia en Gobernanza",IF(J31>=0.7,"🟢 Gestión por Mandato",IF(J31>=0.4,"🟡 Transición Crítica",IF(J31>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L31	=IF(E31=0,"⬜ Sin meta",IF(H31/IF(E31=0,1,E31)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A32	=H25_MMP_MENSUAL!A32
B32	=H25_MMP_MENSUAL!B32
C32	=H25_MMP_MENSUAL!C32
D32	=H25_MMP_MENSUAL!D32
E32	=H25_MMP_MENSUAL!F32
F32	=SUM(H25_MMP_MENSUAL!G32:I32)
G32	=SUM(H25_MMP_MENSUAL!J32:L32)
H32	=SUM(H25_MMP_MENSUAL!M32:O32)
I32	=SUM(H25_MMP_MENSUAL!P32:R32)
J32	=IF(E32=0,0,SUM(F32:I32)/E32)
K32	=IF(J32>=0.9,"🔵 Excelencia en Gobernanza",IF(J32>=0.7,"🟢 Gestión por Mandato",IF(J32>=0.4,"🟡 Transición Crítica",IF(J32>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L32	=IF(E32=0,"⬜ Sin meta",IF(H32/IF(E32=0,1,E32)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A33	=H25_MMP_MENSUAL!A33
B33	=H25_MMP_MENSUAL!B33
C33	=H25_MMP_MENSUAL!C33
D33	=H25_MMP_MENSUAL!D33
E33	=H25_MMP_MENSUAL!F33
F33	=SUM(H25_MMP_MENSUAL!G33:I33)
G33	=SUM(H25_MMP_MENSUAL!J33:L33)
H33	=SUM(H25_MMP_MENSUAL!M33:O33)
I33	=SUM(H25_MMP_MENSUAL!P33:R33)
J33	=IF(E33=0,0,SUM(F33:I33)/E33)
K33	=IF(J33>=0.9,"🔵 Excelencia en Gobernanza",IF(J33>=0.7,"🟢 Gestión por Mandato",IF(J33>=0.4,"🟡 Transición Crítica",IF(J33>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L33	=IF(E33=0,"⬜ Sin meta",IF(H33/IF(E33=0,1,E33)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A34	=H25_MMP_MENSUAL!A34
B34	=H25_MMP_MENSUAL!B34
C34	=H25_MMP_MENSUAL!C34
D34	=H25_MMP_MENSUAL!D34
E34	=H25_MMP_MENSUAL!F34
F34	=SUM(H25_MMP_MENSUAL!G34:I34)
G34	=SUM(H25_MMP_MENSUAL!J34:L34)
H34	=SUM(H25_MMP_MENSUAL!M34:O34)
I34	=SUM(H25_MMP_MENSUAL!P34:R34)
J34	=IF(E34=0,0,SUM(F34:I34)/E34)
K34	=IF(J34>=0.9,"🔵 Excelencia en Gobernanza",IF(J34>=0.7,"🟢 Gestión por Mandato",IF(J34>=0.4,"🟡 Transición Crítica",IF(J34>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L34	=IF(E34=0,"⬜ Sin meta",IF(H34/IF(E34=0,1,E34)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
A35	=H25_MMP_MENSUAL!A35
B35	=H25_MMP_MENSUAL!B35
C35	=H25_MMP_MENSUAL!C35
D35	=H25_MMP_MENSUAL!D35
E35	=H25_MMP_MENSUAL!F35
F35	=SUM(H25_MMP_MENSUAL!G35:I35)
G35	=SUM(H25_MMP_MENSUAL!J35:L35)
H35	=SUM(H25_MMP_MENSUAL!M35:O35)
I35	=SUM(H25_MMP_MENSUAL!P35:R35)
J35	=IF(E35=0,0,SUM(F35:I35)/E35)
K35	=IF(J35>=0.9,"🔵 Excelencia en Gobernanza",IF(J35>=0.7,"🟢 Gestión por Mandato",IF(J35>=0.4,"🟡 Transición Crítica",IF(J35>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
L35	=IF(E35=0,"⬜ Sin meta",IF(H35/IF(E35=0,1,E35)<H01_PARÁMETROS!$B$54,"⚠️ Brecha Q3 — Considerar repriorización o fondos externos","✅ En rango"))
B39	=COUNTIF(L11:L35,"✅ En rango")/25
C39	=25-COUNTIF(L11:L35,"✅ En rango")
D39	=IFERROR(SUMIF(H25_MMP_MENSUAL!D11:D35,"FONDO_CONCURSABLE",H25_MMP_MENSUAL!G11:I35)/H07_S5_FINANCIERO_eSIGEF!B18,0)
B40	=COUNTIF(L11:L35,"✅ En rango")/25
C40	=25-COUNTIF(L11:L35,"✅ En rango")
D40	=IFERROR(SUMIF(H25_MMP_MENSUAL!D11:D35,"FONDO_CONCURSABLE",H25_MMP_MENSUAL!J11:L35)/H07_S5_FINANCIERO_eSIGEF!B18,0)
B41	=COUNTIF(L11:L35,"✅ En rango")/25
C41	=25-COUNTIF(L11:L35,"✅ En rango")
D41	=IFERROR(SUMIF(H25_MMP_MENSUAL!D11:D35,"FONDO_CONCURSABLE",H25_MMP_MENSUAL!M11:O35)/H07_S5_FINANCIERO_eSIGEF!B18,0)
B42	=COUNTIF(L11:L35,"✅ En rango")/25
C42	=25-COUNTIF(L11:L35,"✅ En rango")
D42	=IFERROR(SUMIF(H25_MMP_MENSUAL!D11:D35,"FONDO_CONCURSABLE",H25_MMP_MENSUAL!P11:R35)/H07_S5_FINANCIERO_eSIGEF!B18,0)
B46	=COUNTIF(C11:C35,"OBRA")
C46	=IFERROR(AVERAGEIF(C11:C35,"OBRA",J11:J35),0)
D46	=IF(C46>=0.9,"🔵 Excelencia en Gobernanza",IF(C46>=0.7,"🟢 Gestión por Mandato",IF(C46>=0.4,"🟡 Transición Crítica",IF(C46>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B47	=COUNTIF(C11:C35,"SERVICIO")
C47	=IFERROR(AVERAGEIF(C11:C35,"SERVICIO",J11:J35),0)
D47	=IF(C47>=0.9,"🔵 Excelencia en Gobernanza",IF(C47>=0.7,"🟢 Gestión por Mandato",IF(C47>=0.4,"🟡 Transición Crítica",IF(C47>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B48	=COUNTIF(C11:C35,"NORMATIVO")
C48	=IFERROR(AVERAGEIF(C11:C35,"NORMATIVO",J11:J35),0)
D48	=IF(C48>=0.9,"🔵 Excelencia en Gobernanza",IF(C48>=0.7,"🟢 Gestión por Mandato",IF(C48>=0.4,"🟡 Transición Crítica",IF(C48>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B49	=COUNTIF(C11:C35,"BIEN")
C49	=IFERROR(AVERAGEIF(C11:C35,"BIEN",J11:J35),0)
D49	=IF(C49>=0.9,"🔵 Excelencia en Gobernanza",IF(C49>=0.7,"🟢 Gestión por Mandato",IF(C49>=0.4,"🟡 Transición Crítica",IF(C49>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B51	=SUM(B46:B49)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H26_MMP_TRIMESTRAL
A2	H26 — MMP TRIMESTRAL — MONITOR DE PROGRESO Q1-Q4 2026
A3	Consolidación trimestral del avance de metas. Base para reportes al alcalde y CPCCS.
A5	◌ RESUMEN TRIMESTRAL
A10	ID_Meta
B10	Descripción
C10	CLASE_PRODUCTO
D10	TIPO_FIN
E10	Meta_Anual ($)
F10	Q1_Ene-Mar
G10	Q2_Abr-Jun
H10	Q3_Jul-Sep
I10	Q4_Oct-Dic
J10	Ti_Anual
K10	Clasificación
L10	Alerta_Q3
A37	▌ SEMÁFORO TRIMESTRAL — RESUMEN EJECUTIVO
A38	Trimestre
B38	% Metas en Rango
C38	N° Metas con Alerta
D38	IEF_Trimestral
A39	Q1 (Ene-Mar)
A40	Q2 (Abr-Jun)
A41	Q3 (Jul-Sep)
A42	Q4 (Oct-Dic)
A44	▌ PANEL ICPI EMERGENTE POR CLASE_PRODUCTO
A45	CLASE_PRODUCTO
B45	N° Metas
C45	Ti_Promedio
D45	Clasificación_Promedio
A46	OBRA
A47	SERVICIO
A48	NORMATIVO
A49	BIEN
A51	Total verificado:
```