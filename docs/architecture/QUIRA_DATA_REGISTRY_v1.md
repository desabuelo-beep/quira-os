# QUIRA DATA REGISTRY v1.0

**Fecha:** 2026-06-09
**Origen:** Recomendación Colega asesor — cierre Operaciones pre-Sprint B
**Propósito:** Lista maestra de indicadores, fuentes y estado de cobertura. No gestiona dominios — gestiona Fuentes → Indicadores → Circuitos.
**Mantenimiento:** Actualizar cuando una fuente se conecte, un indicador cambie de estado o un circuito se active.

---

## Estado de cobertura por dominio

### Tipo D — Corpus Fundacional Verificable

| Dominio | Indicador / Artefacto | Fuente | Estado | Notas |
|---|---|---|---|---|
| D01 Marco Legal | Relaciones causales ACK Registry | Supabase C1 vectorizado | ✅ LIVE | Alimenta contexto normativo de todos los dominios |
| D05 PDOT | meta_pdot_2027 (agua, vialidad, residuos) | Supabase C1 vectorizado | ✅ LIVE | Computable → D10 metas territoriales |
| D05 PDOT | METAS_PDOT 25 metas institucionales | Supabase C1 vectorizado | ✅ LIVE | Alimenta D03 (M-01..M-10) + D08 + D09 |
| D05 PDOT | IFE_CNE tag (PLAN-GOB-MCR · PLAN-BICENT) | Supabase C1 vectorizado | ✅ LIVE | Alimenta D03 capa CNE (IFE-A) |

---

### Tipo A — Generadores

#### D02 — Cooperación / Motor de Elegibilidad Financiera

| Indicador | Fuente actual | Estado | Acción requerida |
|---|---|---|---|
| Portfolio fondos (ELEGIBLE/BLOQUEADO/LISTO) | `p18_cooperacion.py` hardcodeado | ⚠️ REDISEÑO | Skill `/fondos-radar` — reemplazar datos estáticos con snapshot dinámico |
| PSG threshold gate | D12 PSG output | ✅ LIVE (transitivo) | Mantener dependencia D12→D02 |
| ISP threshold gate | D10 / data.loader | ✅ LIVE (transitivo) | Mantener dependencia D10→D02 |
| ITAM threshold gate | D07 output | ✅ LIVE (transitivo) | Mantener dependencia D07→D02 |

#### D03 — Metas PDOT · Integridad del Mandato

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| IFE-A Fidelidad Electoral (72.73%) | H73_OUTPUT_API → Gold Master | ✅ LIVE | 48/66 promesas CNE → PDOT · auditado |
| IFE-E Fidelidad Ejecución | eSIGEF (POA→PAC→eSIGEF) | ⏳ PENDIENTE Q2-2026 | Diseñado · sin datos aún · completar cadena |
| M-01 Agua 34.9%→65% | QTMP AGUA_POTABLE + Gold Master | ✅ LIVE | Via D10 |
| M-02 Alcantarillado 43.5%→70% | Gold Master | ✅ LIVE | |
| M-03 Vialidad 53%→75% | Gold Master | ✅ LIVE | |
| M-04 Residuos 47.9→30 ton/día | Gold Master (EP Aseo) | ✅ LIVE | |
| M-05 UT activas 50→75 | D08 (CPCCS V=0) | ✅ LIVE | Via D08 |
| M-06 PSG 12.83%→30% | D12 (H73_OUTPUT_API) | ✅ LIVE | Via D12 |
| M-07 IET $40→$80/hab | D10 (parroquias) | ✅ LIVE | Via D10 |
| M-08 ITAM 56%→75% | D07 (LOTAIP audit) | ✅ LIVE | Via D07 |
| M-09 Plan Turismo 0→100% | Sin fuente activa | ❌ MISSING | Sin módulo dedicado |
| M-10 IFE-A 72.73%→100% | H73_OUTPUT_API | ✅ LIVE | Único indicador promesas→PDOT |

#### D04 — SAT / Alertas Institucionales

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| SAT-0 (metas sin PAC) | Gold Master H75_SAT_ENGINE | ✅ LIVE | 4 metas activas |
| SAT-IV (ISP bajo umbral) | Gold Master H24_SAT-IV | ✅ LIVE | ISP 14.58% < 65% |
| RIESGO_MATRIX (4 categorías) | Hardcodeado demo_data | ⚠️ HARDCODED | Pre-Sprint B: conectar a Gold Master snapshot |

#### D07 — Transparencia Institucional

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| C4 Cumplimiento Formal LOTAIP | QTMP TRANSPARENCIA (Neo4j) | ✅ LIVE | 21 artículos verificados |
| C5a Accesibilidad portal | Neo4j QTMP | ✅ LIVE | |
| C5b Accesibilidad descarga | Neo4j QTMP | ✅ LIVE | |
| C5t Oportunidad temporal | DPE API (transparencia.dpe.gob.ec) | ✅ LIVE | C5t=0 colapsa C8 |
| C5c Consistencia | Neo4j QTMP | ✅ LIVE | |
| C8 fórmula compuesta | C4 × C5a × C5b × C5t × C5c | ✅ LIVE | Multiplicativa · QNKC-P01 |
| IOC (Índice Observancia Contractual) | Gold Master H73_OUTPUT_API | ✅ LIVE | Vector D06 |
| Circuito C01 CHS | p07_transparencia._calcular_chs_c01() | ✅ LIVE | ORIGEN colapsa si falla |

#### D08 — Participación Ciudadana

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| IGP (Índice Gestión Participativa 27.98%) | Gold Master H73_OUTPUT_API | ✅ LIVE | Vector D06 |
| 6 mecanismos participación (%) | Gold Master + hardcoded | ⚠️ PARCIAL | PP 100% verificado · otros estáticos |
| Parroquias sin voz (2/7) | data.loader + parroquias | ✅ LIVE | Isabel Muentes · Aníbal San Andrés |
| CPCCS V=0 | H31_REPORTE_CPCCS | ✅ LIVE | Dato crítico 2026 |
| Aportes PP (95 aportes 2023-2026) | H10c_RDC_APORTES | ✅ LIVE | |

#### D10 — Territorio & Cobertura

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| Cobertura agua potable (34.9%) | QTMP AGUA_POTABLE (Neo4j) | ✅ LIVE | meta_pdot_2027: 42.38% |
| IET inversión per cápita | Gold Master H73_OUTPUT_API | ✅ LIVE | Vector D06 · 7 parroquias |
| Brecha per cápita (5.4×) | data.loader parroquias | ✅ LIVE | Isabel Muentes $40 vs cabecera $217 |
| GeoJSON parroquias | `data/parroquias_montecristi.geojson` | ✅ LIVE | Condicional si existe |
| ISP (14.58%) | Gold Master H73_OUTPUT_API | ✅ LIVE | Vector D06 · SAT-IV gate |

#### D12 — Género y Ambiente

| Indicador | Fuente actual | Estado | Acción requerida |
|---|---|---|---|
| PSG Presupuesto Sensible Género (12.83%) | Gold Master H73_OUTPUT_API | ✅ LIVE | Vector D06 · gate D02 |
| IGM-A Mujeres en cargos directivos | RRHH DAF (por solicitar) | ❌ MISSING | Solicitar reporte RRHH GAD Montecristi |
| IGM-B Brecha salarial género | Nómina DAF (por solicitar) | ❌ MISSING | Solicitar estructura salarial DAF |
| IGM-C Carga acarreo agua rurales | Encuesta PNUD/INEC | ❌ MISSING | Coordinar con PNUD Ecuador |
| IGM-D Luminarias Pin Morado (0%) | Binary · Gold Master | ✅ LIVE | Bloqueado: PSG < 30% |
| IGM-E Plan Género aprobado (0%) | Binary · acta Concejo | ✅ LIVE | No aprobado |
| IGM-F Representación política CNE | CNE/AME datos electorales | ❌ MISSING | Solicitar datos CNE post-2023 |
| ODS 5.1/5.2/5.4/5.5/5.a/5.c | INEC/SENPLADES (por solicitar) | ❌ MISSING (6/6) | Priorizar con PNUD en marco cooperación |
| Metas FA Ambiente (PDOT) | D05 PDOT corpus (Supabase) | ✅ LIVE | Via Tipo D |

---

### Tipo B — Sintetizador

#### D06 — Estado GAD

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| Score ICPI (via Gold Master) | Gold Master H73_OUTPUT_API | ✅ LIVE | NUNCA recalcular — solo leer |
| Histórico ICPI 2023-2025 | Gold Master H73_OUTPUT_API | ✅ LIVE | 57.36 → 67.12 → 69.93 |
| 6 vectores causales (ISP/IED/IGP/IOC/IET/PSG) | Feeds de dominios A | ✅ LIVE | Cada vector alimentado por su Generador |
| Brecha ICM/ICPI | p16_gobernanza.py BRECHA_HISTORICA | ✅ LIVE | 100% autoreporte vs 57-70% verificado |

---

### Tipo C — Protocolo

#### D09 — Rendición de Cuentas

| Indicador | Fuente actual | Estado | Notas |
|---|---|---|---|
| Checklist RDC (20 ítems) | Feeds de todos los Tipo A | 2/20 OK · 12 urgentes | Terminal — no genera datos propios |
| Resultado CPCCS V=0 | H31_REPORTE_CPCCS | ✅ LIVE | Árbitro externo · no modificable |
| Timeline estacional (Mayo-Sep) | Hardcoded | ✅ LIVE | Actualizar anualmente |

---

## Resumen de cobertura

| Estado | Descripción | Count |
|---|---|---|
| ✅ LIVE | Indicador operacional con fuente verificada | ~32 |
| ⏳ PENDIENTE | Diseñado, fuente identificada, sin datos aún | 1 (IFE-E) |
| ⚠️ HARDCODED | Funcional pero datos estáticos sin snapshot | 2 (RIESGO_MATRIX · D02 portfolio) |
| ❌ MISSING | Indicador definido, fuente externa no conectada | 10 (D12 IGM-A/B/C/F · ODS5 6/6 · M-09) |

---

## Prioridades de completitud pre-Sprint B

| Prioridad | Indicador | Acción | Responsable externo |
|---|---|---|---|
| 🔴 ALTA | IFE-E (D03) | Conectar trazabilidad POA→PAC→eSIGEF | Dirección Financiera GAD |
| 🔴 ALTA | D02 portfolio dinámico | Skill `/fondos-radar` (~15 días) | Claude + curation Javo |
| 🟠 MEDIA | IGM-A (D12) | Solicitar reporte RRHH a GAD | RRHH / DAF GAD Montecristi |
| 🟠 MEDIA | IGM-B (D12) | Solicitar estructura salarial | DAF GAD Montecristi |
| 🟡 BAJA | IGM-C (D12) | Coordinar encuesta PNUD/INEC | PNUD Ecuador |
| 🟡 BAJA | IGM-F (D12) | Solicitar datos electorales 2023 | CNE Ecuador |
| 🟡 BAJA | ODS 5.x (D12) | Priorizar en marco cooperación | PNUD / SENPLADES |
| ⬜ DIFERIR | M-09 Plan Turismo (D03) | Sin urgencia operacional | Planificación GAD |

---

## Circuitos y su estado de activación

| Circuito | Dominios | Estado | Pendiente |
|---|---|---|---|
| C01 | D07→D08→D04 | ✅ IMPLEMENTADO en código | Formalizar C02/C03 (ADR-017) |
| C-RDC | D07+D08+D02+D03+D04+D10+D12→D09→CPCCS | ✅ SPEC en ADR-026 | Ejecutar Cypher en Neo4j AuraDB |
| C02 | D07+D08→? | ⏳ SPEC PARCIAL ADR-017 | Completar especificación |
| C03 | ?→? | ⏳ SPEC PARCIAL ADR-017 | Completar especificación |

---

*QUIRA_DATA_REGISTRY_v1.0 · Dylus Lab © 2026*
*Derivado de Fase 0 Arqueología Funcional + ADR-026 v1.2 · 2026-06-09*
*Actualizar al conectar nuevas fuentes o cambiar estado de indicadores*
