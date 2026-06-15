# H02b_ORGÁNICO_CLASIFICADOR — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=62 · pobladas=56 · fórmulas=19
inputs(lee de): H00_ÍNDICE, H01_PARÁMETROS
outputs(alimenta a): H00_ÍNDICE, H39_AUTOCONTROL_ECOSISTEMA

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
E1	="AXIOMA 2025: " & TEXT(H01_PARÁMETROS!$B$15, "0,00%") & " | LIVE 2026: " & TEXT(H01_PARÁMETROS!$B$19, "0,00%")
F1	=TODAY()
B11	=H01_PARÁMETROS!B11
B12	=COUNTA(A15:A34)
B38	=COUNTA(A15:A34)
D38	=COUNTA(A15:A34)
B39	=COUNTIF(C15:C34,"GOBERNANTE")
D39	=COUNTIF(C15:C34,"GOBERNANTE")
B40	=COUNTIF(C15:C34,"AGREGADOR_VALOR")
D40	=COUNTIF(C15:C34,"AGREGADOR_VALOR")
B41	=COUNTIF(C15:C34,"HABILITANTE_ASESORIA")
D41	=COUNTIF(C15:C34,"HABILITANTE_ASESORIA")
B42	=COUNTIF(C15:C34,"HABILITANTE_APOYO")
D42	=COUNTIF(C15:C34,"HABILITANTE_APOYO")
B43	=COUNTIF(C15:C34,"ENTIDAD_ADSCRITA")
D43	=COUNTIF(C15:C34,"ENTIDAD_ADSCRITA")
B44	=COUNTA(F15:F34)-COUNTIF(F15:F34,"—")
D44	=COUNTA(F15:F34)-COUNTIF(F15:F34,"—")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H02b_ORGÁNICO_CLASIFICADOR
A2	H02b — ORGÁNICO CLASIFICADOR — ADN DEL SISTEMA QUIRA
A3	Mapeo del nivel de autoridad y la naturaleza de la evidencia de cada unidad del GAD según la Resolución 040-2025-ALC-LJTL-GADMCM. Fuente del TIPO_PROCESO y EVIDENCIA_PREDOMINANTE para el motor H12. El financiamiento es por META (H04/H07c), no por dirección.
A4	★ DECISIÓN ARQUITECTÓNICA v1.0 (Javo Delgado Santana, 27-Abr-2026): TIPO_FINANCIAMIENTO es atributo de la META (H04 col O / H07c), NO de la dirección. INTANGIBLE_FLAG es atributo de la META (H13), NO de la dirección. Una misma unidad puede tener metas tangibles e intangibles y distintos tipos de financiamiento simultáneamente.
A6	▌ METADATOS DEL ESTATUTO
A7	Campo
B7	Valor
A8	Resolución
B8	No. 040-2025-ALC-LJTL-GADMCM
A9	Fecha aprobación
B9	2025-10-02 00:00:00
A10	Vigente desde
B10	2026-01-01 00:00:00
A11	Alcalde que firma
A12	Total unidades clasificadas
A13	▌ TABLA DE CLASIFICACIÓN ORGÁNICA (v1.0 — Estrictamente Orgánica)  |  ⚠️ COLUMNAS ELIMINADAS vs versión anterior: CLASE_PRODUCTO / INTANGIBLE_FLAG / TIPO_FIN_TÍPICO → ahora en H13 y H04 por META
A14	COD_UNIDAD
B14	NOMBRE_UNIDAD
C14	TIPO_PROCESO
D14	ROL_INSTITUCIONAL
E14	EVIDENCIA_PREDOMINANTE
F14	COD_H17
G14	Nota
A15	U-01
B15	Alcaldía / Despacho
C15	GOBERNANTE
D15	Dirección Política
E15	DOCUMENTO / RESOLUCIÓN
F15	—
G15	Dirección ejecutiva Art.60 COOTAD
A16	U-02
B16	Dirección de Planificación Estratégica e Institucional
C16	HABILITANTE_ASESORIA
D16	Asesoría Técnica
E16	DOCUMENTO / INDICADOR
F16	—
G16	PDOT/PUGS/POA — Res. 040-2025
A17	U-03
B17	Dirección de Proyectos Estratégicos
C17	HABILITANTE_ASESORIA
D17	Asesoría Técnica
E17	DOCUMENTO / ESIGEF
F17	—
G17	Captación y gestión fondos concursables
A18	U-04
B18	Procuraduría Síndica
C18	HABILITANTE_ASESORIA
D18	Asesoría Jurídica
E18	DOCUMENTO / DICTAMEN
F18	—
G18	Asesoría jurídica y patrocinio — Res. 040-2025
A19	U-05
B19	Dirección de Comunicación Social y RRPP
C19	HABILITANTE_ASESORIA
D19	Apoyo Comunicacional
E19	INDICADOR / DOCUMENTO
F19	—
G19	Productos comunicacionales — Res. 040-2025
A20	U-06
B20	Dirección de Participación Ciudadana y Control Social
C20	AGREGADOR_VALOR
D20	Servicio Ciudadano
E20	INDICADOR / ACTA ASAMBLEA
F20	—
G20	Asambleas / PP — Art.238 COOTAD
A21	U-07
B21	Dirección de Catastro y Gestión del Suelo
C21	AGREGADOR_VALOR
D21	Regulación
E21	INDICADOR / TRÁMITE
F21	—
G21	Permisos / legalización suelo — Res. 040-2025
A22	U-08
B22	Dirección de Obras Públicas y Fiscalización
C22	AGREGADOR_VALOR
D22	Infraestructura
E22	ESIGEF / SERCOP / ACTA OBRA
F22	DIR-OO.PP
G22	COOTAD Art.55 — infraestructura física
A23	U-09
B23	Dirección de Seguridad, Control Territorial y Comisarías
C23	AGREGADOR_VALOR
D23	Regulación / Servicio
E23	INDICADOR / ESIGEF
F23	—
G23	Espacio público / comisarías — Res. 040-2025
A24	U-10
B24	Dirección de Tránsito, Transporte y Matriculación Vehicular
C24	AGREGADOR_VALOR
D24	Regulación / Servicio
E24	INDICADOR / ESIGEF
F24	—
G24	Título competencia CNC — Res. 040-2025
A25	U-11
B25	Dirección de Gestión Ambiental y Riesgos
C25	AGREGADOR_VALOR
D25	Servicio / Control
E25	INDICADOR / DOCUMENTO
F25	DIR-AMB
G25	COOTAD Art.55 lit.k) — riesgos/ambiente
A26	U-12
B26	Dirección de Agua Potable y Alcantarillado Sanitario
C26	AGREGADOR_VALOR
D26	Infraestructura / Servicio
E26	ESIGEF / SERCOP
F26	DIR-AGUA
G26	ARCA / fondos MIDUVI — puede ser reembolsable o no
A27	U-13
B27	Dirección de Turismo, Cultura, Patrimonio y Fomento Productivo
C27	AGREGADOR_VALOR
D27	Servicio / Promoción
E27	INDICADOR / DOCUMENTO
F27	DIR-CUL
G27	Talleres / eventos / patrimonio — Res. 040-2025
A28	U-14
B28	Secretaría General y de Concejo
C28	HABILITANTE_APOYO
D28	Apoyo Institucional
E28	DOCUMENTO / ACTA
F28	SEC-GEN
G28	Gestión documental / actas de concejo
A29	U-15
B29	Dirección Administrativa
C29	HABILITANTE_APOYO
D29	Apoyo Operativo
E29	ESIGEF / INVENTARIO
F29	DIR-ADM
G29	Compras públicas / bienes / contratos
A30	U-16
B30	Dirección Financiera
C30	HABILITANTE_APOYO
D30	Apoyo Financiero
E30	ESIGEF / REPORTE
F30	—
G30	Presupuesto / tesorería / rentas
A31	U-17
B31	Dirección de Talento Humano
C31	HABILITANTE_APOYO
D31	Apoyo RRHH
E31	DOCUMENTO / NÓMINA
F31	—
G31	Capacitación / LOSEP Art.52
A32	U-18
B32	Dirección de Registro de la Propiedad y Mercantil
C32	HABILITANTE_APOYO
D32	Servicio Registral
E32	ESIGEF / INDICADOR
F32	—
G32	Ingresos propios / aranceles registrales
A33	U-19
B33	Patronato Municipal de Amparo Social
C33	ENTIDAD_ADSCRITA
D33	Servicio Especializado
E33	INDICADOR / INFORME SHA-256
F33	PATRONATO
G33	COOTAD Art.249 — servicio social especializado
A34	U-20
B34	EP Aseo Integral / Cuerpo de Bomberos (Adscritas)
C34	ENTIDAD_ADSCRITA
D34	Operación Específica
E34	ESIGEF / INDICADOR
F34	EP-ASEO
G34	LOEP / LOSC — servicios operativos especiales
A36	▌ TABLA DE VERIFICACIÓN H02b
A37	Verificación
B37	Fórmula
C37	Esperado
D37	Resultado
A38	Total unidades ingresadas
C38	20
A39	Unidades GOBERNANTE
C39	1
A40	Unidades AGREGADOR_VALOR
C40	8
A41	Unidades HABILITANTE_ASESORIA
C41	4
A42	Unidades HABILITANTE_APOYO
C42	5
A43	Unidades ENTIDAD_ADSCRITA
C43	2
A44	COD_H17 asignados (≠ — y no vacíos)
C44	7
A46	▌ PRINCIPIO ARQUITECTÓNICO — GESTIÓN DIALÉCTICA DEL FINANCIAMIENTO
A47	★ REGLA ABSOLUTA H02b v1.0:
A48	Esta hoja mapea AUTORIDAD ORGÁNICA y TIPO DE EVIDENCIA por unidad. NO define financiamiento. La gestión pública es dinámica:
A49	• Obras Públicas puede usar: presupuesto propio GAD + crédito BDE + donación embajada + fondo concursable BID. Todo en diferentes metas del mismo año.
A50	• Agua Potable puede usar: presupuesto propio + crédito CAF + cooperación MIDUVI no reembolsable.
A51	• Desarrollo Social puede usar: presupuesto corriente + cooperación PNUD + fondo concursable.
A53	Por eso TIPO_FINANCIAMIENTO está en:
A54	  → H04_S2_PLANIFICACIÓN_PDOT (col O): un valor por meta en la planificación anual
A55	  → H07c_Ti_VERIFICADO_INFORME: captura real por transacción de fondos externos
A57	INTANGIBLE_FLAG está en:
A58	  → H13_VARIABLES_Vi: un valor por meta (no por dirección)
A59	  Una dirección de infraestructura puede tener una meta intangible de 'estudio de riesgo'.
A61	Fuente: Resolución Administrativa No. 040-2025-ALC-LJTL-GADMCM — Estatuto Orgánico
A62	de Gestión Organizacional por Procesos del GAD Montecristi (vigente 01-ene-2026).
```