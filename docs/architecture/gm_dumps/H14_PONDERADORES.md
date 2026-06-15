# H14_PONDERADORES — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=36 · pobladas=33 · fórmulas=31
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H12_MOTOR_ICPI_CANÓNICO, H12b_MOTOR_IBSC, H35_DATASET_ACADEMIA, H37_SENSIBILIDAD_ESTRATÉGICA, H39_AUTOCONTROL_ECOSISTEMA
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
F7	=(D7*E7)/1.725
F8	=(D8*E8)/1.725
F9	=(D9*E9)/1.725
F10	=(D10*E10)/1.725
F11	=(D11*E11)/1.725
F12	=(D12*E12)/1.725
F13	=(D13*E13)/1.725
F14	=(D14*E14)/1.725
F15	=(D15*E15)/1.725
F16	=(D16*E16)/1.725
F17	=(D17*E17)/1.725
F18	=(D18*E18)/1.725
F19	=(D19*E19)/1.725
F20	=(D20*E20)/1.725
F21	=(D21*E21)/1.725
F22	=(D22*E22)/1.725
F23	=(D23*E23)/1.725
F24	=(D24*E24)/1.725
F25	=(D25*E25)/1.725
F26	=(D26*E26)/1.725
F27	=(D27*E27)/1.725
F28	=(D28*E28)/1.725
F29	=(D29*E29)/1.725
F30	=(D30*E30)/1.725
F31	=(D31*E31)/1.725
G33	=SUM(G7:G31)
H33	=IF(ABS(SUM(G7:G31)-1)<0.0001,"✅ Σ Pi = 1,0000","❌ ERROR: Σ Pi ≠ 1 — verificar")
K33	=IF(ABS(SUM(G7:G31)-1)<0.0001,"✅ Σ Pi OK","❌ Σ Pi ≠ 1")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H14_PONDERADORES
A2	H14 — PONDERADORES Pi y Ri — JUSTIFICACIÓN METODOLÓGICA
A3	P_i = Peso financiero normalizado. Suma = 1.0000 exacto. R_i incorpora bono discriminación positiva de H01.
A4	ESCALA R_i_raw: 1.5=Exclusiva Crítica (agua/alcantarillado/desechos) | 1.0=Exclusiva Importante (vialidad/salud/educación) | 0.5=Complementaria/Concurrente
A6	ID_Meta
B6	Descripción
C6	Competencia_GAD
D6	R_i_raw
E6	Bono_Equidad
F6	R_i_final
G6	P_i
H6	Justificación R_i
I6	Justificación P_i
J6	VERIFICACIÓN_R
K6	VERIFICACIÓN_P
A7	SC-I-N-01
B7	Agua potable
C7	Exclusiva_Crítica
D7	1.5
E7	1
G7	0.2736043382767234
H7	COOTAD Art.55d — agua potable competencia exclusiva municipal. R_raw=1.5 por ser servicio vital
I7	Pi = presupuesto agua/inversión total — meta de mayor peso financiero del PDOT
K7	<openpyxl.worksheet.formula.ArrayFormula object at 0x0000025C33BAFD90>
A8	SC-L-N-02
B8	Talento humano
C8	Exclusiva_Importante
D8	1
E8	1
G8	0.3078567637341166
H8	COOTAD Art.57 — gestión RRHH competencia propia. R_raw=1.0 por ser gestión institucional
I8	Pi = presupuesto talento humano — segundo mayor componente del presupuesto municipal
A9	AH-I-X-01
B9	Sostenibilidad financiera
C9	Exclusiva_Importante
D9	1
E9	1
G9	0.1178634256863337
H9	COOTAD Art.57 — gestión financiera exclusiva del GAD. R_raw=1.0
I9	Pi = componente coactivas/recaudación — peso presupuestario intermedio
A10	AH-I-X-02
B10	Vialidad cantonal
C10	Exclusiva_Crítica
D10	1.5
E10	1
G10	0.06368520194497646
H10	COOTAD Art.55f — vialidad cantonal competencia exclusiva. R_raw=1.5
I10	Pi = vialidad urbana y rural — presupuesto significativo pero menor que agua y RRHH
A11	AH-I-X-03
B11	Salud integral
C11	Concurrente_Crítica
D11	0.5
E11	1
G11	0.03431449043672
H11	COOTAD Art.135 — salud concurrente con Ministerio de Salud. R_raw=0.5
I11	Pi = Patronato Municipal — gasto social moderado vs inversión directa
A12	AH-I-N-01
B12	Gestión desechos sólidos
C12	Exclusiva_Crítica
D12	1.5
E12	1.15
G12	0.0335450946873591
H12	COOTAD Art.55d — manejo residuos sólidos exclusivo. R_raw=1.5 × Bono_ODS13=1.15 → R_final=1.0 (tope)
I12	Pi = desechos sólidos — EP Aseo Integral; presupuesto moderado pero impacto ambiental crítico
A13	SC-L-G-01
B13	Alcantarillado sanitario
C13	Exclusiva_Crítica
D13	1.5
E13	1
G13	0.00740731528645508
H13	COOTAD Art.55d — alcantarillado competencia exclusiva. R_raw=1.5
I13	Pi = alcantarillado — bajo Pi histórico por rezago en ejecución vs impacto crítico
A14	AH-I-X-04
B14	Modernización administrativa
C14	Exclusiva_Importante
D14	1
E14	1
G14	0.02196201959256068
H14	COOTAD Art.57 — modernización institucional exclusiva. R_raw=1.0
I14	Pi = tecnología e infraestructura — gasto moderado en modernización
A15	PI-I-G-01
B15	Equipamientos públicos
C15	Exclusiva_Importante
D15	1
E15	1
G15	0.0150994994949404
H15	COOTAD Art.55k — infraestructura física exclusiva. R_raw=1.0
I15	Pi = terminal/mercado/centro salud — presupuesto planificado moderado
A16	AH-C-X-01
B16	Protección derechos sociales
C16	Concurrente_Crítica
D16	0.5
E16	1.15
G16	0.0102376183399494
H16	COOTAD Art.249 — Patronato, concurrente con MIES. Bono_ODS5=1.15 (equidad género)
I16	Pi = protección social — gasto social Patronato en servicios CDI y adultos mayores
A17	AH-C-X-02
B17	Sistema información territorial
C17	Exclusiva_Importante
D17	1
E17	1
G17	0.01061385811124415
H17	COOTAD Art.139 — catastro y planificación territorial exclusiva. R_raw=1.0
I17	Pi = catastro urbano-rural — presupuesto moderado con retorno en recaudación
A18	SC-I-N-03
B18	Participación ciudadana
C18	Exclusiva_Importante
D18	1
E18	1
G18	0.00080439479785343
H18	COOTAD Art.302-304 — participación ciudadana obligatoria. R_raw=1.0
I18	Pi = asamblea cantonal y presupuesto participativo — bajo Pi por gasto directo limitado
A19	FA-I-X-01
B19	Gestión del riesgo
C19	Exclusiva_Importante
D19	1
E19	1.15
G19	0.00554151601131804
H19	COOTAD Art.55k + SNGRE — gestión riesgos local. Bono_ODS13=1.15 (acción climática)
I19	Pi = gestión riesgo — presupuesto bajo pero con transferencias SNGRE
A20	FA-C-X-01
B20	Áreas verdes y parques
C20	Exclusiva_Importante
D20	1
E20	1.15
G20	0.00414155407161664
H20	COOTAD Art.55k — espacios públicos exclusivos. Bono_ODS13=1.15 (ambiente)
I20	Pi = áreas verdes/manglar — gasto directo moderado en mantenimiento
A21	FA-I-X-02
B21	Índice equipamiento urbano
C21	Exclusiva_Importante
D21	1
E21	1
G21	0.02917733009898571
H21	COOTAD Art.55d — servicio de barrido/recolección exclusivo EP Aseo. R_raw=1.0
I21	Pi = barrido vial y recolección — presupuesto EP Aseo significativo
A22	FA-L-N-01
B22	Inventario patrimonial
C22	Exclusiva_Importante
D22	1
E22	1
G22	0.00290753428716785
H22	COOTAD Art.144 — preservación patrimonio local exclusiva. R_raw=1.0
I22	Pi = cultura/museo — gasto directo bajo en eventos y catalogación
A23	PI-I-G-02
B23	Cumplimiento PDOT/PUGS
C23	Exclusiva_Importante
D23	1
E23	1
G23	0.00275892832726854
H23	COOTAD Art.466 — PDOT/PUGS obligatorio exclusivo del GAD. R_raw=1.0
I23	Pi = planificación territorial — presupuesto técnico moderado SIL/PUGS
A24	PI-L-G-01
B24	Señalización vial
C24	Exclusiva_Importante
D24	1
E24	1
G24	0.00158020703943795
H24	COOTAD Art.55f — señalización vial exclusiva municipal. R_raw=1.0
I24	Pi = señalización/semáforos — gasto presupuestado bajo
A25	EP-L-N-01
B25	Vivienda de interés social
C25	Exclusiva_Importante
D25	1
E25	1
G25	0.00188994861859689
H25	COOTAD Art.55k — vivienda concurrente con MIDUVI. R_raw=1.0
I25	Pi = VIS/VIP — presupuesto bajo GAD; cofinanciamiento MIDUVI no contabiliza en Pi
A26	EP-L-X-01
B26	Fortalecimiento productivo
C26	Concurrente
D26	0.5
E26	1
G26	0.00134375346782239
H26	COOTAD Art.135 — fomento productivo concurrente con MIPRO. R_raw=0.5
I26	Pi = emprendimiento/artesanos — bajo gasto directo municipal
A27	PI-TUR-01
B27	Turismo cantonal
C27	Concurrente
D27	0.5
E27	1
G27	0.01866615919601866
H27	COOTAD Art.135 — turismo concurrente con MINTUR. R_raw=0.5
I27	Pi = Ciudad Creativa/certificación — gasto presupuestado moderado con transferencias
A28	PI-TUR-02
B28	Eventos turísticos
C28	Concurrente
D28	0.5
E28	1
G28	0.006999809698507
H28	COOTAD Art.135 — eventos turísticos concurrentes. R_raw=0.5
I28	Pi = eventos anuales — presupuesto operativo bajo
A29	FA-CC-01
B29	Cambio climático
C29	Exclusiva_Importante
D29	1
E29	1.15
G29	0.00466653979900466
H29	COOTAD Art.55k — planes ambientales locales exclusivos. Bono_ODS13=1.15
I29	Pi = planes cambio climático — gasto técnico bajo (normativo)
A30	AH-AP-04
B30	Continuidad agua potable
C30	Exclusiva_Crítica
D30	1.5
E30	1
G30	0.01458293687188958
H30	COOTAD Art.55d — continuidad servicio agua exclusivo. R_raw=1.5
I30	Pi = índice continuidad servicio — asignación presupuestaria O&M agua
A31	FA-DIS-01
B31	Disposición final desechos
C31	Exclusiva_Crítica
D31	1.5
E31	1.15
G31	0.00874976212313375
H31	COOTAD Art.55d — disposición final residuos exclusivo. R_raw=1.5 × Bono_ODS13=1.15 → R_final=1.0 (tope)
I31	Pi = relleno sanitario — EP Aseo; presupuesto operativo bajo vs impacto crítico
A33	TOTALES / VERIFICACIÓN
A34	NOTA BUG-01:
B34	Los 25 valores Pi YA están normalizados (suma = 1.0000). BUG-01 (Pi=0.9463) fue corregido. Fórmula normalización: Pi_corr_i = Pi_raw_i / SUMA(todos_Pi_raw). Aplicar antes de emitir Certificado SIAP-ICPI para nuevos GADs.
A36	FALLA 11 — VERIFICACIÓN ALINEACIóN:
B36	Las columnas H (Justificación R_i) e I (Justificación P_i) están EXACTAMENTE en la misma fila que su ID_Meta en columna A. Verificar manualmente scrolleando columnas H e I que cada justificación corresponde al ID de la misma fila.
```