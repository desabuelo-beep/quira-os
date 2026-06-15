# H77_DATA_DICTIONARY — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=19 · fórmulas=1
inputs(lee de): —
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE
MARCADORES: C17: Bitacora append-only de eventos por alerta. Registra los 7 estados ins

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	📖 SIAP-ICPI v1.0 — DICCIONARIO DE DATOS
D1	H77_DATA_DICTIONARY
A2	📖 H77 — DICCIONARIO DE DATOS / DATA DICTIONARY
A3	MÓDULO / HOJA
B3	TIPO
C3	DEFINICIÓN
D3	RESTRICCIONES
E3	VERSIÓN
A4	H12d_ICPI_POR_ENTIDAD
B4	HUB_SOBERANO
C4	Módulo exclusivo para Entidades Adscritas y Empresas Públicas con personería jurídica propia. Se excluyen direcciones municipales internas por corresponder a la lógica de Eficiencia Directiva de H30_IED y no al Hub de entidades autónomas. Entidades activas: Aseo EP (EPAM-01), Bomberos (BOMB-01), Patronato (PAT-01). Reservas escalables: RESERVA-X, RESERVA-Y, RESERVA-Z.
D4	Cod_Unidad en B debe coincidir con H04!K15:K39. Sin metas asignadas → ICPI_Parcial=0. H12!B33 INTOCABLE.
E4	v1.3 — 2026
A5	H12_MOTOR_ICPI_CANÓNICO
B5	MOTOR_CANÓNICO
C5	Motor central de cálculo del ICPI. Fórmula canónica: ICPI = Σ(Pi·Ri·Vi·Ei·Ti·Ci) / Σ(Pi·Ri) × 100, implementada en B33=B31/B32*100. Axioma de Invarianza: la fórmula es inmutable. El valor es dinámico por ciclo.
D5	B33 = B31/B32*100 — NUNCA modificar. Columnas B=Pi×Ri, J=numerador parcial, K=denominador parcial, D=Vi.
E5	v2.1
A6	H30_IED_POR_DIRECCIÓN
B6	EFICIENCIA_DIRECTIVA
C6	Índice de Eficiencia Directiva (IED) por dirección municipal interna. Complemento de H12d: mientras H12d mide entidades autónomas, H30 mide el desempeño de las unidades administrativas internas del GAD.
D6	No confundir con H12d. Direcciones sin personería jurídica propia.
E6	v1.0
A7	H81_HASH_CHAIN
B7	TRAZABILIDAD
C7	Cadena de hash inmutable (append-only). Hash_n = SHA256(Evento_n + Hash_{n-1}). Registra todos los eventos de gobernanza del sistema SIAP-ICPI.
D7	NUNCA modificar hashes anteriores. Solo añadir al final.
E7	v2.1
A8	H89_TRUST_SCORE
B8	CERTIFICACIÓN
C8	Métrica ejecutiva Trust Score 0-100. Escala Institucional Conservadora (SIAP-ICPI v1.0 Institutional Mode): CERTIFICADO (95-100) / OPERATIVO CON OBSERVACIONES (80-94) / RIESGO MODERADO (60-79) / INTERVENCIÓN REQUERIDA (<60). Trust = 0.35×Integridad + 0.25×Disponibilidad + 0.25×Trazabilidad + 0.15×Cumplimiento.
D8	Trust Score ≥ 95 requerido para estado CERTIFICADO.
E8	v1.2 GTU
A9	H73_OUTPUT_API
B9	CAPA_SALIDA_API
C9	Capa de salida API del sistema SIAP-ICPI. Expone ICPI_LIVE, ESTADO_SISTEMA, HASH_MODELO, CIRCUIT_BREAKER, TRUST_SCORE_REF. ESTADO_SISTEMA = OPERATIVO_CERTIFICADO si Trust≥95, OPERATIVO si válido, DEGRADADO si inactivo.
D9	CIRCUIT_BREAKER activo si ΔICPI>0.0001 o periodo≠2026-04-30.
E9	v2.1
A10	H18_ITAM
B10	TRANSPARENCIA
C10	Índice de Transparencia Algorítmica Municipal. ITAM=0.8229, IOC=0.1771
D10	IOC_2025_Ref = 0.1771 — FUENTE ÚNICA para H41
E10	v3.0 — 2026
A11	H41_IOC_OPACIDAD
B11	OPACIDAD
C11	Índice de Opacidad Crítica. IOC = H18!B20. NUNCA calcular desde H01
D11	Refiere H18_ITAM!B20. No calcular internamente
E11	v3.0 — 2026
A12	H42_IET
B12	EQUIDAD_TERRITORIAL
C12	IET_Gini=92.73% equidad territorial. IET_PerCapita=44.80%
D12	Dos métricas: Gini (inversión total) y PerCápita (parroquia peor)
E12	v3.0 — 2026
A13	H73_OUTPUT_API
B13	CAPA_SALIDA
C13	API de salida SIAP-ICPI. 43 métricas actualizadas Q1-2026
D13	EXTRACT_TIMESTAMP actualizado manualmente cada corte
E13	v3.0 — 2026
A14	H90_PRESUPUESTO_CONSOL
B14	FINANCIERO
C14	Presupuesto consolidado 4 entidades. Total 2026 = $54.2M
D14	INMUTABLE para datos 2023-2024. Corte Q1-2026 verificado.
E14	v3.0 — 2026
A15	QUIRA_OS_SYNC
B15	TRAZABILIDAD_PMV
C15	Mapa explícito Excel ↔ QUIRA OS PMV. 15 métricas mapeadas.
D15	2 métricas en revisión: IOC (resuelto v3.0), IET (dual métrica v3.0)
E15	v3.0 — 2026
A16	H01 Sección I vs M
B16	ACLARACIÓN
C16	Sección I = Ci_Base (calidad orgánica base por meta). Sección M = Infracciones INF-01..04 que MODIFICAN Ci. NO son duplicados — Sección M ajusta el Ci de Sección I.
D16	Leer: Ci_final = MAX(0.50, 1.00 - Σ(INF_i × deducción_i))
E16	v4.0 — 2026
A17	alert_timeline
B17	TRAZABILIDAD_SENTINEL
C17	Bitacora append-only de eventos por alerta. Registra los 7 estados institucionales: pendiente en_revision derivada resuelta observada validada archivada. Actor + timestamp + nota inmutable
D17	INSERT solo - NUNCA UPDATE. Integridad auditada. Sin borrado de historia.
E17	RC-1.1 - 2026
A18	resolution_patterns
B18	MEMORIA_OPERATIVA
C18	Patrones de resolucion aprendidos por Sentinel. Multi-criteria matching: tipo+3 entidad+2 severidad+2 trimestre+1. Alimenta Borrador Institucional y Antecedentes Comparables
D18	INSERT solo - agregar patrones nuevos al final. Sin borrado de historia.
E18	RC-1.1 - 2026
A19	alerts_history
B19	ALERTAS_HOLDING
C19	Historial Ti inversion 4 entidades Holding Municipal de Montecristi. Genera alertas semaforo QUIRA OS RC-1: Verde>=35% Amarillo 15-34.9% Rojo<15%
D19	Umbrales congelados RC-1.1. Unique constraint: (anio mes entidad tipo). ON CONFLICT DO UPDATE para re-ingesta idempotente.
E19	RC-1.1 - 2026
```