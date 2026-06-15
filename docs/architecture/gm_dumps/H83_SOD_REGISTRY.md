# H83_SOD_REGISTRY — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=8 · pobladas=7 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
A2	OPERADOR
B2	ROL
C2	FUNCIÓN
D2	AUTORIZACIÓN
E2	SOD_OK
F2	DESCRIPCIÓN
A3	SIAP_ENGINE
B3	MODIFICACION
C3	Escritura en hojas de datos
D3	RBAC_LEVEL_2
E3	TRUE
F3	Motor engine — modifica hojas de cálculo
A4	DYLUS_LAB_CERTIFIER
B4	CERTIFICACION
C4	Firma de reportes y audit trail
D4	RBAC_LEVEL_3
E4	TRUE
F4	DYLUS LAB certifier — no puede modificar
A5	ADMIN_TRUSTEE
B5	ADMINISTRACION
C5	Gestión de configuración del sistema
D5	RBAC_LEVEL_4
E5	TRUE
F5	Superadministrador — acceso total
A6	READONLY_AUDITOR
B6	LECTURA
C6	Solo lectura de reportes y H86/H89
D6	RBAC_LEVEL_1
E6	TRUE
F6	Auditor externo — sin escritura
A8	VALIDACIÓN SoD ACTUAL
B8	Modificacion (SIAP_ENGINE) ≠ Certificacion (DYLUS_LAB_CERTIFIER)
C8	VÁLIDA
```