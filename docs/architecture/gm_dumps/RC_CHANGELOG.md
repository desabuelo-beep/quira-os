# RC_CHANGELOG — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=14 · pobladas=14 · fórmulas=0
inputs(lee de): —
outputs(alimenta a): —

## FÓRMULAS
```
(sin fórmulas)
```

## ETIQUETAS / DATOS (tope 600)
```
A1	Fecha
B1	RC Version
C1	Componente
D1	Tipo
E1	Descripcion
F1	Archivos clave
G1	SAT Codes
H1	Dimensiones TGI
A2	2026-05-20
B2	P2
C2	Migracion Vault Obsidian
D2	data/arch
E2	Normalizacion 12 aliases → 5 IDs canonicos (D1-D5). 83 notas migradas, 219 reemplazos. vault_registry.json reconstruido con 252 notas, 227 con frontmatter.
F2	scripts/migrate_vault_dimensions.py | data/vault_registry.json | data/vault_schema.json
G2	SAT-IX, SAT-X-A, SAT-X-B, SAT-XI, SAT-XII
H2	D1_LEGALIDAD, D2_PLANIFICACION, D3_EJECUCION, D4_EQUIDAD, D5_CAPACIDAD
A3	2026-05-20
B3	P3
C3	Loop Semantico Vault → Claude
D3	code/arch
E3	Cierre loop semantico: SAT → obsidian_bridge → vault_registry → vault_enricher → legal_router → Claude Haiku. Provenance por respuesta. Max 4 notas/query.
F3	sentinel/vault_enricher.py | sentinel/legal_router.py (capa 2)
G3	SAT-IX, SAT-X-A, SAT-X-B, SAT-XI, SAT-XII
H3	D1_LEGALIDAD, D3_EJECUCION
A4	2026-05-20
B4	RC-7.2
C4	Longitudinal Engine — 4 sub-motores
D4	code
E4	Motor matematico puro: slopes OLS, momentum (vel+acel), discontinuidades z-score, estacionalidad Q4/Q1. Patrones institucionales: FREEZE, Q4_PUSH, REFORM_SHOCK, BURST, DIP, GRADUAL_DECLINE, RECOVERY, STRUCTURAL_FLAT. Clasificacion ejecutiva AVEP: PARALISIS_ESTRUCTURAL, MANIPULACION_TEMPORAL, EXPANSION_TARDIA (+7). Cierre normativo: patron → SAT → vault → legal_router → Claude Haiku.
F4	sentinel/longitudinal_engine.py | sentinel/administrative_patterns.py | sentinel/institutional_classifier.py | sentinel/normative_binding.py
G4	SAT-XI, SAT-X-A, SAT-X-B, SAT-XII
H4	D3_EJECUCION, D2_PLANIFICACION, D1_LEGALIDAD
A5	2026-05-20
B5	RC-7.3
C5	Calibration Layer — 5 mecanismos
D5	calibration
E5	confidence_decay: decae certeza por n_periodos < 3 o frecuencia mixta (x0.75). entity_baselines: gap vs Ti historico de cada entidad (GM v5.5). seasonal_normalization: Q1 G71-78 esperado 2.5% — PARALISIS → EXPANSION_TARDIA (conf x0.55). reform_whitelist: COPLAFIP Art.97 — reforma ≤ 10% Alcalde suprime SAT-X-B. evidence_weighting + SAT_suppression: SAT solo si conf ≥ 0.40 y ev_weight ≥ 0.50.
F5	sentinel/calibration_layer.py | data/rc72_calibration.json
G5	SAT-XI, SAT-X-B
H5	D3_EJECUCION, D1_LEGALIDAD
A6	2026-05-20
B6	PROTO
C6	Protocolo Canonico Sync 4 Fuentes
D6	arch
E6	REGLA CANONICA: toda entrega en quira-os se disemina automaticamente en Obsidian (nota arch YAML), Gold Master (esta hoja RC_CHANGELOG) y GitHub (commit+push). scripts/sync_protocol.py implementa el protocolo.
F6	scripts/sync_protocol.py
G6	N/A
H6	D5_CAPACIDAD
A7	2026-05-20
B7	RC-7.4
C7	RC-7.4 Data Bridge
D7	code
E7	Componente RC-7.4 Data Bridge vRC-7.4 entregado en QUIRA OS.
F7	sentinel/budget_record_loader.py | data/gm_snapshot.json | sentinel/__init__.py | components/sentinel.py
A8	2026-05-20
B8	RC-7.5
C8	RC-7.5 Visual Calibration Panel
D8	code
E8	Componente RC-7.5 Visual Calibration Panel vRC-7.5 entregado en QUIRA OS.
F8	sentinel/ui_components.py | sentinel/calibration_layer.py | components/sentinel.py
A9	2026-05-20
B9	1.0
C9	RC-D4-Engine
D9	motor
E9	Componente RC-D4-Engine v1.0 entregado en QUIRA OS.
F9	sentinel/d4_engine.py | sentinel/d4_patterns.py | sentinel/d4_calibration.py | sentinel/d4_loader.py | data/d4_calibration.json
A10	2026-05-20
B10	1.0
C10	RC-D4-Visual
D10	componente
E10	Componente RC-D4-Visual v1.0 entregado en QUIRA OS.
F10	sentinel/ui_components.py | sentinel/d4_calibration.py
A11	2026-05-20
B11	1.0
C11	RC-D4-Normative
D11	motor
E11	Componente RC-D4-Normative v1.0 entregado en QUIRA OS.
F11	sentinel/d4_normative.py | data/d4_normative.json
A12	2026-05-20
B12	1.0
C12	RC-D3D4-Cross-Engine
D12	motor
E12	Componente RC-D3D4-Cross-Engine v1.0 entregado en QUIRA OS.
F12	sentinel/d3d4_engine.py | sentinel/__init__.py | sentinel/ui_components.py | components/sentinel.py
A13	2026-05-20
B13	1.0
C13	RC-D3D4-Normative
D13	capa
E13	Componente RC-D3D4-Normative v1.0 entregado en QUIRA OS.
F13	sentinel/d3d4_normative.py | sentinel/__init__.py | sentinel/ui_components.py | components/sentinel.py | .github/workflows/claude-review.yml
A14	2026-05-20
B14	RC-CORE-1.0
C14	RC-CORE Registry + Provenance + Human Review
D14	sprint
E14	Componente RC-CORE Registry + Provenance + Human Review vRC-CORE-1.0 entregado en QUIRA OS.
F14	sentinel/rc_registry.py | sentinel/provenance_graph.py | sentinel/human_review.py
```