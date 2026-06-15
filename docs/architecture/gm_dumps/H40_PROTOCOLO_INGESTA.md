# H40_PROTOCOLO_INGESTA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=35 · pobladas=25 · fórmulas=3
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE
MARCADORES: A24: Nunca hardcodear valores en H12 u otras hojas de cálculo

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H40_PROTOCOLO_INGESTA
A2	H40 — PROTOCOLO DE INGESTA — GUÍA PARA ACTUALIZACIÓN DE DATOS
A3	Instrucciones paso a paso para ingresar nuevos datos al sistema sin alterar la fórmula canónica H12!B33 = B31/B32*100 (Axioma de Invarianza = la fórmula, no un número).
A5	§1 ANTES DE INGESTAR
A6	Verificar H39 — estado debe ser ✅ SISTEMA ÍNTEGRO
A7	Hacer copia de seguridad del archivo antes de cualquier cambio
A8	Identificar el tipo de dato: ARRASTRE nuevo / actualización de silo / parámetros
A10	§2 INGRESAR DATOS eSIGEF
A11	Verificar formato numérico: si viene como '1.234,56' → convertir a 1234.56 (importante: Excel puede interpretar como texto)
A12	Actualizar H07 (silo S5) con los nuevos devengados
A13	El ICPI en H12!B33 se actualiza automáticamente
A14	Verificar que H39!D7 siga mostrando ✅ AXIOMA VERIFICADO
A16	§3 AGREGAR NUEVO ARRASTRE a H36b
A17	El nuevo ARRASTRE debe tener ID correlativo (ARRASTRE-018, ARRASTRE-019, etc.)
A18	Nunca modificar ARRASTREs existentes con estado REAL o REAL-VERIFICADO
A19	Los ARRASTREs SIMULADO pueden actualizarse cuando llegan datos reales
A20	Marcar como ⚫ SUPERSEDED si el registro es reemplazado por uno más actual
A22	§4 ACTUALIZAR PARÁMETROS EN H01
A23	Cualquier cambio de configuración solo va en H01_PARÁMETROS
A24	Nunca hardcodear valores en H12 u otras hojas de cálculo
A25	Después de cambios en H01, siempre verificar H39 para confirmar integridad
A27	§5 VERIFICACIÓN FINAL
A28	H39!B30 debe mostrar ✅ SISTEMA ÍNTEGRO — Gold Master v1.0 listo para uso
A29	H12!B33 debe mantener el valor esperado del período activo
A30	Guardar el archivo con nombre versionado: SIAP-ICPI_v1.0_GoldMaster_YYYYMMDD.xlsx
```