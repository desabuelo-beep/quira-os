# H13_VARIABLES_Vi — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=81 · pobladas=73 · fórmulas=28
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H12_MOTOR_ICPI_CANÓNICO
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B20	=SI(O(V_eSIGEF=0,V_SERCOP=0),0,SI(O(V_LOTAIP=1,V_CPCCS=1),1,0.5))
H25	=IF(F25<>"","Vi_2025_Ref","⚠️ VACÍO")
H26	=IF(F26<>"","Vi_2025_Ref","⚠️ VACÍO")
H28	=IF(F28<>"","Vi_2025_Ref","⚠️ VACÍO")
H29	=IF(F29<>"","Vi_2025_Ref","⚠️ VACÍO")
H30	=IF(F30<>"","Vi_2025_Ref","⚠️ VACÍO")
H31	=IF(F31<>"","Vi_2025_Ref","⚠️ VACÍO")
H32	=IF(F32<>"","Vi_2025_Ref","⚠️ VACÍO")
H33	=IF(F33<>"","Vi_2025_Ref","⚠️ VACÍO")
H34	=IF(F34<>"","Vi_2025_Ref","⚠️ VACÍO")
H35	=IF(F35<>"","Vi_2025_Ref","⚠️ VACÍO")
H36	=IF(F36<>"","Vi_2025_Ref","⚠️ VACÍO")
H37	=IF(F37<>"","Vi_2025_Ref","⚠️ VACÍO")
H38	=IF(F38<>"","Vi_2025_Ref","⚠️ VACÍO")
H39	=IF(F39<>"","Vi_2025_Ref","⚠️ VACÍO")
H40	=IF(F40<>"","Vi_2025_Ref","⚠️ VACÍO")
H41	=IF(F41<>"","Vi_2025_Ref","⚠️ VACÍO")
H42	=IF(F42<>"","Vi_2025_Ref","⚠️ VACÍO")
H43	=IF(F43<>"","Vi_2025_Ref","⚠️ VACÍO")
H44	=IF(F44<>"","Vi_2025_Ref","⚠️ VACÍO")
H45	=IF(F45<>"","Vi_2025_Ref","⚠️ VACÍO")
H46	=IF(F46<>"","Vi_2025_Ref","⚠️ VACÍO")
H47	=IF(F47<>"","Vi_2025_Ref","⚠️ VACÍO")
H48	=IF(F48<>"","Vi_2025_Ref","⚠️ VACÍO")
H49	=IF(F49<>"","Vi_2025_Ref","⚠️ VACÍO")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H13_VARIABLES_Vi
A2	H13 — VARIABLES Vi — VERIFICACIÓN INTERSISTÉMICA
A3	Los 4 verificadores activos de Vi. V_POA (S3) NO entra — es verificador de programación, no de ejecución.
A4	REGLA MAESTRA: V_eSIGEF y V_SERCOP son verificadores NÚCLEO obligatorios (ejecución financiera). V_LOTAIP y V_CPCCS son verificadores de TRANSPARENCIA/RENDICIÓN.
A6	▌ DOCUMENTACIÓN DE VERIFICADORES
A7	Silo
B7	V_Componente
C7	Criterio V=1.0
D7	Criterio V=0.5
E7	Criterio V=0.0
F7	Fuente
G7	Base Legal
A8	S4 — SERCOP
B8	V_SERCOP
C8	Proceso adjudicado publicado en portal SERCOP
D8	Proceso registrado en SERCOP pero no adjudicado (en trámite)
E8	Sin proceso SERCOP registrado
F8	H06_S4_CONTRATACIÓN_SERCOP
G8	LOSNCP Art.22 + Art.73
A9	S5 — eSIGEF
B9	V_eSIGEF
C9	Devengado certificado > 0 en sistema MEF
D9	Codificado > 0 pero sin devengado registrado
E9	Sin registro presupuestario en eSIGEF
F9	H07_S5_FINANCIERO_eSIGEF
G9	COPFP Arts.115-117 + Acuerdo 067 MEF
A10	S7 — LOTAIP
B10	V_LOTAIP
C10	Documento en URL pública del GAD — accesible y verificable
D10	URL registrada pero no accesible o incompleta
E10	Sin URL pública — algorítmicamente no existe
F10	H09_S7_TRANSPARENCIA_LOTAIP
G10	LOTAIP Art.7 + Constitución Art.18
A11	S8 — CPCCS
B11	V_CPCCS
C11	Mencionada en rendición con evidencia documental citada ante CPCCS
D11	Mencionada en rendición sin evidencia documental específica
E11	No mencionada en acto de rendición de cuentas
F11	H10_S8_PARTICIPACIÓN_CPCCS
G11	LOPC Art.88 + Constitución Art.204
A13	▌ NOTA METODOLÓGICA
B13	V_POA (S3) NO entra en el producto lógico Vi — S3 es verificador de programación, no de ejecución. Los 4 verificadores activos de Vi son: V_SERCOP + V_eSIGEF + V_LOTAIP + V_CPCCS.
A15	▌ FÓRMULA DEL PRODUCTO LÓGICO Vi
A16	LÓGICA Vi CORRECTA (3 niveles):
B16	1. Vi = 0.0 → si V_eSIGEF=0 O V_SERCOP=0 (sin ejección financiera verificada = sin puntuación)
B17	2. Vi = 0.5 → si V_eSIGEF=1 Y V_SERCOP=1 Y V_LOTAIP=0 Y V_CPCCS=0 (ejecución financiera confirmada pero sin evidencia pública)
B18	3. Vi = 1.0 → si V_eSIGEF=1 Y V_SERCOP=1 Y (V_LOTAIP=1 O V_CPCCS=1) (ejecución financiera + al menos un verificador de transparencia)
A20	Fórmula Excel (español):
A21	⚠️ POR QUÉ NO la fórmula anterior:
B21	La fórmula original SI(suma≥2,0.5) era incorrecta: producía Vi=0.5 para metas con SERCOP=0/eSIGEF=0 pero LOTAIP=1/CPCCS=1. Los valores Vi_2025 canónicos prueban que AH-I-X-02 (SERCOP=0/eSIGEF=0/LOTAIP=1/CPCCS=1) tiene Vi=0.0. REGLA: sin núcleo financiero = sin score.
A23	▌ VALORES Vi DE REFERENCIA 2025 (para verificar ICPI_Real_2025 (resultado de la fórmula canónica H12!B33))
A24	Meta
B24	V_SERCOP
C24	V_eSIGEF
D24	V_LOTAIP
E24	V_CPCCS
F24	Vi_2025
G24	Nota_AH-I-X-02 / Casos especiales
H24	Vi_Fuente
A25	SC-I-N-01
B25	1
C25	1
D25	1
E25	1
F25	1
A26	SC-L-N-02
B26	1
C26	1
D26	1
E26	1
F26	1
A27	AH-I-X-01
B27	1
C27	1
D27	1
E27	1
F27	1
H27	Vi_Fuente
A28	AH-I-X-02
B28	0
C28	0
D28	1
E28	1
F28	0
G28	⬜ Vi=0.0 aunque LOTAIP=1/CPCCS=1. SERCOP=0/eSIGEF=0 activa la regla NÚC LEO FINANCIERO.
A29	AH-I-X-03
B29	1
C29	1
D29	1
E29	1
F29	1
A30	AH-I-N-01
B30	1
C30	1
D30	0
E30	0
F30	0.5
G30	Vi=0.5 — núcleo eSIGEF+SERCOP OK pero sin transparencia pública LOTAIP/CPCCS
A31	SC-L-G-01
B31	1
C31	1
D31	1
E31	0
F31	1
A32	AH-I-X-04
B32	1
C32	1
D32	1
E32	0
F32	1
A33	PI-I-G-01
B33	1
C33	1
D33	1
E33	1
F33	1
A34	AH-C-X-01
B34	1
C34	1
D34	1
E34	1
F34	1
A35	AH-C-X-02
B35	1
C35	1
D35	1
E35	1
F35	1
A36	SC-I-N-03
B36	1
C36	1
D36	0
E36	1
F36	1
A37	FA-I-X-01
B37	1
C37	1
D37	1
E37	1
F37	1
A38	FA-C-X-01
B38	1
C38	1
D38	1
E38	1
F38	1
A39	FA-I-X-02
B39	1
C39	1
D39	1
E39	0
F39	1
A40	FA-L-N-01
B40	1
C40	1
D40	1
E40	1
F40	1
A41	PI-I-G-02
B41	1
C41	1
D41	1
E41	1
F41	1
A42	PI-L-G-01
B42	1
C42	1
D42	0
E42	1
F42	1
A43	EP-L-N-01
B43	1
C43	1
D43	1
E43	1
F43	1
A44	EP-L-X-01
B44	1
C44	1
D44	1
E44	1
F44	1
A45	PI-TUR-01
B45	0
C45	0
D45	1
E45	1
F45	0
G45	Vi=0.0 — sin SERCOP ni eSIGEF (meta de fondos concursables). Brecha real documentada.
A46	PI-TUR-02
B46	0
C46	0
D46	1
E46	1
F46	0
A47	FA-CC-01
B47	0
C47	0
D47	1
E47	1
F47	0
A48	AH-AP-04
B48	0
C48	0
D48	1
E48	1
F48	0
A49	FA-DIS-01
B49	0
C49	0
D49	1
E49	1
F49	0
A51	▌ ATRIBUTOS POR META — CLASE_PRODUCTO e INTANGIBLE_FLAG
A52	★ DECISIÓN ARQUITECTÓNICA v1.0:
B52	CLASE_PRODUCTO e INTANGIBLE_FLAG son atributos de la META ESPECÍFICA, NO de la dirección. Se registran aquí (H13). La misma dirección puede tener metas tangibles e intangibles simultáneamente. Fuente: esta hoja (H13) — NOT H02b.
A54	ID_Meta
B54	CLASE_PRODUCTO
C54	INTANGIBLE_FLAG
D54	Nota_Evidencia
A55	SC-I-N-01
B55	OBRA
C55	FALSO
D55	Infraestructura agua potable — devengado eSIGEF directo
A56	SC-L-N-02
B56	SERVICIO
C56	VERDADERO
D56	Capacitación/gestión RRHH — informe SHA-256 / Ti_V
A57	AH-I-X-01
B57	SERVICIO
C57	VERDADERO
D57	Gestión financiera/coactivas — no genera obra física
A58	AH-I-X-02
B58	OBRA
C58	FALSO
D58	Vialidad cantonal — devengado eSIGEF directo
A59	AH-I-X-03
B59	SERVICIO
C59	VERDADERO
D59	Salud integral — atenciones Patronato / informe SHA-256
A60	AH-I-N-01
B60	OBRA
C60	FALSO
D60	Desechos sólidos — relleno sanitario, eSIGEF directo
A61	SC-L-G-01
B61	OBRA
C61	FALSO
D61	Alcantarillado — obra física, devengado eSIGEF
A62	AH-I-X-04
B62	BIEN
C62	FALSO
D62	Modernización — adquisición equipos/tecnología, eSIGEF
A63	PI-I-G-01
B63	OBRA
C63	FALSO
D63	Equipamientos públicos — obra física, eSIGEF directo
A64	AH-C-X-01
B64	SERVICIO
C64	VERDADERO
D64	Protección social — atenciones / convenio MIES
A65	AH-C-X-02
B65	SERVICIO
C65	VERDADERO
D65	Catastro / trámites digitales — sistema, no obra
A66	SC-I-N-03
B66	SERVICIO
C66	VERDADERO
D66	Participación ciudadana — talleres, instancias
A67	FA-I-X-01
B67	NORMATIVO
C67	VERDADERO
D67	Gestión riesgo — planes de acción / informes
A68	FA-C-X-01
B68	OBRA
C68	FALSO
D68	Áreas verdes / manglar — obra física, eSIGEF
A69	FA-I-X-02
B69	SERVICIO
C69	FALSO
D69	Equipamiento urbano — barrido/recolección, eSIGEF EP Aseo
A70	FA-L-N-01
B70	SERVICIO
C70	VERDADERO
D70	Cultura / patrimonio — eventos, inventario, no obra
A71	PI-I-G-02
B71	NORMATIVO
C71	VERDADERO
D71	PDOT/PUGS — instrumentos de planificación
A72	PI-L-G-01
B72	OBRA
C72	FALSO
D72	Señalización vial — obra física, eSIGEF directo
A73	EP-L-N-01
B73	OBRA
C73	FALSO
D73	Vivienda VIS/VIP — obra física cofinanciada MIDUVI
A74	EP-L-X-01
B74	SERVICIO
C74	VERDADERO
D74	Fortalecimiento productivo — capacitación, asistencia técnica
A75	PI-TUR-01
B75	SERVICIO
C75	VERDADERO
D75	Turismo / certificación — no genera obra ni eSIGEF propio
A76	PI-TUR-02
B76	SERVICIO
C76	VERDADERO
D76	Eventos turísticos — intangible, informe SHA-256
A77	FA-CC-01
B77	NORMATIVO
C77	VERDADERO
D77	Planes cambio climático — instrumento normativo
A78	AH-AP-04
B78	SERVICIO
C78	VERDADERO
D78	Continuidad agua — índice de servicio, no obra
A79	FA-DIS-01
B79	OBRA
C79	FALSO
D79	Disposición final — capacidad operativa relleno, eSIGEF
A81	NOTA DE USO:
B81	INTANGIBLE_FLAG alimenta la lógica Ti_V en H12. Si INTANGIBLE_FLAG=VERDADERO y Ti_V=0, H12 aplica el factor H01!J134 (INTANGIBLE_SIN_TiV=0.85) al Ci_Adaptativo. CLASE_PRODUCTO alimenta paneles MMP (H25/H26/H27) y el análisis por tipo de producto en H17_IED.
```