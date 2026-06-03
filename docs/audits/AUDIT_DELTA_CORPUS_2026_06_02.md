# Audit Delta Corpus — QUIRA Gov
**Fecha**: 2026-06-02  
**Ejecutado por**: Agente Gate 6.4  
**Corpus actual**: 43 docs · 8,351 chunks · 100% clasificados

---

## Resultado Principal

**DELTA NORMATIVA_WORD = CERO**

Los 43 documentos de `Normativa_Word/` tienen entrada en `manifest.py` y están
completamente ingresados en Supabase con el nuevo schema v2.0 (document_class +
authority_level + source_entity + canton_id).

No se requiere ingesta adicional de Normativa_Word.

---

## Estado del Corpus Normativo (Capas A y B)

| Capa | Docs | Chunks | Estado |
|---|---|---|---|
| A — NORMA | 36 | ~7,200 | COMPLETO |
| B — METODOLOGIA | 7 | ~1,150 | COMPLETO |
| C — INSTRUMENTO_TERRITORIAL (Normativa_Word) | 2 | ~612 | COMPLETO |
| D — EVIDENCIA_OBSERVACIONAL | 0 | 0 | PENDIENTE (Gate 6.5) |

---

## Verdadero Trabajo Pendiente — Gate 6.5 (Holding Municipal Montecristi)

Esta carpeta contiene la evidencia de ejecución real del GAD Montecristi y su
Holding. Es el activo más transformador del próximo sprint porque permite
responder: **La norma dijo X — ¿Montecristi lo hizo?**

### Capa C — Instrumento Territorial (~40 docs DOCX/PDF)

| Tipo | Entidades | Años | Docs estimados |
|---|---|---|---|
| POA (Plan Operativo Anual) | GAD + Aseo EP + Bomberos + Patronato | 2023-2026 | ~16 |
| PAC (Plan Anual de Contratación) | GAD + Aseo EP + Bomberos + Patronato | 2023-2026 | ~16 |
| PAI (Plan Anual de Inversión) | GAD | 2023, 2025, 2026 | 3 |
| Plan Plurianual de Inversiones | GAD | — | 1 |
| Plan Bicentenario | GAD | — | 1 |
| Resolución Orgánica 040-2025 | GAD | 2025 | 1 |

### Capa D — Evidencia Observacional (~16 docs DOCX/PDF)

| Tipo | Entidades | Años | Docs |
|---|---|---|---|
| Informe Rendición de Cuentas | GAD + Aseo EP + Bomberos + Patronato | 2023-2024 | 8 |
| Informe Presupuesto Participativo | GAD | 2024-2026 | 3 |
| Reporte ICM SIGAD | GAD | 2023-2024 | 2 |

### Datos Estructurados (→ holding_structured_data, NO normativa_corpus)

| Tipo | Período | Archivos |
|---|---|---|
| Cédulas presupuestarias GAD | 2023-2025 | 3 (.xls) |
| Presupuestos mensuales (Aseo EP, Bomberos, GAD, Patronato) | varios | ~12 (.xlsx) |
| Conjuntos datos LOTAIP Numeral 6 | 2025 completo + 2026 Ene-Abr | ~40 (.xlsx) |

### Imágenes (→ OCR antes de clasificar)

| Archivo | Contenido probable |
|---|---|
| pagina_01-17.png | Documento escaneado — identificar y clasificar tras OCR |

---

## Prioridad de Ingesta Gate 6.5

Ordenado por relevancia para los circuitos C01/C02/C03:

1. **Informes RC** (C01 + C03) — evidencia directa del circuito democrático
2. **Informes PP** (C01 + C02) — evidencia del ciclo participativo
3. **POAs** (C02 + C03) — planificación anual por dominio
4. **PACs** (C03) — contratación y ejecución
5. **Reporte ICM SIGAD** (transversal) — evaluación de gestión
6. **Cédulas y presupuestos** → tabla `holding_structured_data`
7. **Datos LOTAIP** → tabla `holding_structured_data`

---

## Gaps A≠C y A≠D Detectables Post Gate 6.5

Una vez ingestado el Holding, QUIRA podrá responder:

| Gap | Pregunta | Norma fundante |
|---|---|---|
| A≠C | COOTAD_266 obliga RC anual — ¿está en el POA? | COOTAD Art.266 |
| A≠C | LOPC_77 obliga silla vacía — ¿aparece en PAC? | LOPC Art.77 |
| A≠D | LOPC_65 obliga PP con presupuesto — ¿hay informe PP? | LOPC Art.65 |
| C≠D | POA planificó agua barrio X — ¿aparece en RC? | PDOT + COOTAD_266 |

---

*AUDIT_DELTA_CORPUS · QUIRA Gov · Dylus Lab · 2026-06-02*  
*"El Holding es donde el deber ser se encuentra con el ser."*
