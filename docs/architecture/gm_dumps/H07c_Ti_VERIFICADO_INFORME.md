# H07c_Ti_VERIFICADO_INFORME — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=61 · pobladas=32 · fórmulas=12
inputs(lee de): H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H20c_IEF_EFICIENCIA_FINANCIERA, H21b_SAT-0_COHERENCIA_PAC, H25_MMP_MENSUAL, H27_MMP_ANUAL, H39_AUTOCONTROL_ECOSISTEMA
refs no resueltas: #H00_ÍNDICE
MARCADORES: L23: ⬜ PENDIENTE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B13
B7	=H01_PARÁMETROS!J124
B8	=H01_PARÁMETROS!J129
B9	=COUNTA(A12:A50)
B53	=COUNTA(A23:A50)
B54	=COUNTIF(J23:J50,"<>")
B55	=IFERROR(AVERAGEIF(F23:F50,"<>0",F23:F50),0)
B56	=SUM(G23:G50)
B57	=SUMIF(D23:D50,"FONDO_CONCURSABLE",G23:G50)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H07c_Ti_VERIFICADO_INFORME
A2	H07c — Ti_VERIFICADO — SILO DE EVIDENCIA VERIFICADA NO-eSIGEF
A3	Registra informes de ejecución firmados electrónicamente (PDF SHA-256) para metas intangibles y fondos concursables. Activa la jerarquía Ti_V en H12 cuando eSIGEF no aplica.
A5	▌ PARÁMETROS H07c
A6	Año_Activo
A7	Ti_V_Hash_Requerido
A8	Ci_Fondo_Concursable_Modificador
A9	Total_Registros
A11	▌ INSTRUCCIÓN DE USO
A12	CUÁNDO USAR H07c:
B12	1. Meta con INTANGIBLE_FLAG=VERDADERO en H02b → no hay cédula eSIGEF individual
B13	2. Meta financiada con FONDO_CONCURSABLE → el fondo externo no aparece en eSIGEF del GAD
B14	3. Meta NORMATIVO (ordenanza, plan) → el 'producto' es el documento firmado
A16	FLUJO DEL ANALISTA:
B16	a) Obtener informe de ejecución en PDF
B17	b) Firma electrónica del Director responsable (Firma Digital BC o equivalente)
B18	c) Calcular SHA-256 del PDF firmado (herramienta online o PowerShell)
B19	d) Ingresar todos los campos de esta hoja. H12 detectará automáticamente Ti_V > 0 + Hash ≠ '' y lo usará en lugar de Ti=0
A21	▌ REGISTRO DE INFORMES VERIFICADOS 2026
A22	ID_Registro
B22	ID_Meta
C22	NOMBRE_META_RESUMIDA
D22	TIPO_FINANCIAMIENTO
E22	CLASE_PRODUCTO
F22	Ti_V
G22	Monto_Ejecutado_USD
H22	Fecha_Informe
I22	Firmante_Cargo
J22	Hash_SHA256
K22	Nombre_Archivo_PDF
L22	Estado_Validación
M22	Nota
A23	[Simulado Q1-2026 — actualizar con Ti_V verificado]
B23	[Simulado Q1-2026 — actualizar con Ti_V verificado]
C23	[Se completan cuando el analista ingresa los informes firmados]
L23	⬜ PENDIENTE
A24	IEF-001
B24	SC-I-N-01
C24	Agua Potable Rural — convenio MIDUVI/BanEcuador
D24	COOPERACION_DIRECTA
E24	CONVENIO_SECTORIAL
F24	1
G24	487500
H24	abr-2026
I24	Director de Agua y Saneamiento
J24	SIM-SHA256-SC-I-N-01-MIDUVI-2026
K24	Convenio_MIDUVI_BanEcuador_Agua_Potable_2026.pdf
L24	✅ VÁLIDO
M24	Fondo externo MIDUVI/BanEcuador — ingresado para cálculo IEF
A25	IEF-002
B25	SC-L-G-01
C25	Alcantarillado rural — aporte sectorial SENAGUA
D25	COOPERACION_DIRECTA
E25	CONVENIO_SECTORIAL
F25	1
G25	312000
H25	abr-2026
I25	Director de Agua y Saneamiento
J25	SIM-SHA256-SC-L-G-01-SENAGUA-2026
K25	Aporte_Sectorial_SENAGUA_Alcantarillado_2026.pdf
L25	✅ VÁLIDO
M25	Aporte sectorial SENAGUA — ingresado para cálculo IEF
A26	IEF-003
B26	AH-I-X-02
C26	Vialidad — convenio MTOP rehabilitación
D26	COOPERACION_DIRECTA
E26	CONVENIO_SECTORIAL
F26	1
G26	850000
H26	abr-2026
I26	Director de Obras Públicas
J26	SIM-SHA256-AH-I-X-02-MTOP-2026
K26	Convenio_MTOP_Vialidad_Rehabilitacion_2026.pdf
L26	✅ VÁLIDO
M26	Convenio MTOP rehabilitación vial — ingresado para cálculo IEF
A27	IEF-004
B27	EP-L-N-01
C27	Vivienda social — MIDUVI bono entrega vivienda
D27	FONDO_CONCURSABLE
E27	BONO_SECTORIAL
F27	1
G27	225000
H27	abr-2026
I27	Director Económico
J27	SIM-SHA256-EP-L-N-01-MIDUVI-VIS-2026
K27	MIDUVI_Bono_VIS_VIP_Entrega_2026.pdf
L27	✅ VÁLIDO
M27	Bono MIDUVI VIS/VIP — concursable — ingresado para cálculo IEF
A51	▌ RESUMEN H07c
A52	Verificación
B52	Fórmula
C52	Resultado
A53	Total informes ingresados
A54	Informes válidos (con hash SHA-256)
A55	Ti_V promedio (informes válidos)
A56	Monto total verificado USD
A57	Fondos concursables verificados
A59	NOTA AL PIE:
B59	H07c es un silo de solo-ingreso. Los valores Ti_V son referenciados por H12 vía BUSCARV(ID_Meta, H07c!B23:J50, 5, 0). La columna Hash (J) debe estar llena para que H12 active Ti_V — sin hash, H12 ignora Ti_V y baja a Ti_Histórico.
B61	Metas candidatas para H07c (FONDO_CONCURSABLE o INTANGIBLE): EP-L-N-01 | EP-L-X-01 | FA-CC-01 | FA-DIS-01
```