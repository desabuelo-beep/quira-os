---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2]
  type: NORMATIVA
---

# PCD-D09 · Rendición de Cuentas (QINV-009)

> **Expediente de Curación de Dominio** — segunda aplicación del `PROTOCOLO_CURACION_DOMINIO.md`
> (la primera fue [`PCD-D01`](PCD-D01_Planificacion.md)). Sesión 2026-07-02 · Director: Claude ·
> Fundador: Javo · Asesor externo. *"¿Por qué Rendición de Cuentas quedó exactamente así?"* — aquí está.

## Estado inicial
Cajón QINV-009 nacido por **réplica del molde** (Planificación): reusa `_css/_head/_intro/_narr/_div/
_tbl/_show` de `m_planificacion`. En su primera forma cubría **solo fidelidad narrativa** (2024). Ampliado
después a **serie de 3 años (2023-2025)** + **cumplimiento 2025** vía el enricher de DOCX. El Presupuesto
Participativo (H10b) había sido ruteado **fuera** de RDC hacia Participación (d08), su dueño por la pregunta
que responde. Faltaba la curación de las 7 capas de cabo a rabo.

## Hallazgos (auditoría de 7 capas)
1. **Gold Master:** el canon métrico está **completo y correcto** — `H34b` (fidelidad narrativa 2024,
   9 registros MFN, promedio `B21`), `H31` (marco + brecha compromisos CPCCS), `H24b` (SAT-V compromisos).
   **No hay artefacto** análogo al IPE 61% de d01: los números resisten la auditoría.
2. **Metodológica:** el backbone es la **triangulación** discurso ↔ evidencia física/financiera ↔ informe
   CPCCS. Metodología sólida; se conserva.
3. **Matemática (hallazgo insignia):** el `IF_n` por afirmación **no es** la fórmula-rúbrica de `H34b!A6`
   (`Ponderación × (1 − |N−E|/max)`) — los valores de la columna `L` igualan a `Valor_Narrativa` (`J`).
   Es decir, el `IF_n` es una **evaluación experta trazable** (juicio humano discurso↔evidencia), no un
   cómputo automático. Es lo correcto para fidelidad narrativa (exige criterio), y el cajón ya lo enmarca
   así ("se triangula… cada una recibe un índice"), sin afirmar cálculo automático. Sin cambio.
4. **Semántica:** `cpccs.fecha_rdc` era **redundante** — la serie ya porta la fecha de rendición por año.
   Regla #7 (anti-inflación): se elimina el campo que solo añade superficie.
5. **Cableado (hallazgo + corrección):** `enrich_rdc.py` leía `H31!B61` para `cpccs.fecha_rdc` y obtenía
   **texto de marco legal** ("LOPC Art.88 + Constitución Art.204") — dato **erróneo** que además **nunca se
   renderiza**. Se **eliminó** el campo y se **regeneró el snapshot** (ambos enrichers en orden: `enrich_rdc`
   escribe `rendicion` completo → `enrich_rdc_docx` fusiona `serie` + `cumplimiento_actual`).
6. **Visual:** compile OK · **Firewall limpio** (los 3 tokens H34b/H31/H10b viven solo en el docstring
   dev-facing, no en cadena emitida) · serie con barra de asistentes · tabla de claims discurso↔evidencia.
7. **Narrativa:** registro de administración pública · fidelidad **honestamente acotada al ejercicio 2024**
   (subtítulo `render()`: "Serie 2023-2025 · fidelidad narrativa del ejercicio 2024") · brecha de
   compromisos muestra "—" cuando no hay dato (no inventa un 0% falso).

## Cambios en el canon
- **Gold Master:** **ninguna cirugía** — el canon métrico de RDC ya era correcto (a diferencia de d01, no
  había proxy que corregir). H12!B33 intacta por construcción (no se tocó ninguna hoja).
- **Corpus (RESUELTO esta sesión):** ingestados los **3 informes RDC 2023-2025** (114 chunks) a Supabase
  `normativa_corpus` vía `scripts/ingest_rdc_corpus.py` — reutiliza el pipeline normativo `qlep-corpus`
  (mismo modelo local de embeddings, mismo insert idempotente por SHA256) + **modo documento**: ventana
  ≤450 palabras que **ignora el regex de artículos** (evita cortes espurios en un informe de prosa que cita
  leyes). Conteo: 2023=20 · 2024=38 · 2025=56 chunks. Coexisten con **25 chunks previos del Holding**
  (`tipo=EVIDENCIA_OBSERVACIONAL`, 2023/2024, `holding-v1.0`) que se **conservan** (decisión Javo 2026-07-02):
  son evidencia observacional temática de otro pipeline, distinguibles por `tipo_documento`. **Nota para el
  connector de recuperación de d09:** filtrar por `tipo_documento='informe_rendicion'` para el texto completo.
- **Snapshot (`rendicion`):** `cpccs` queda `{marco_legal, brecha_compromisos}` (se retira `fecha_rdc`).
  `fidelidad` (9 afirmaciones · global **91.0%** · 8 alta · 1 baja) · `serie` (2023/2024/2025) ·
  `cumplimiento_actual` (21 componentes 2025) intactos.
- **Motores:** `enrich_rdc.py` (fidelidad H34b + CPCCS H31, campo muerto retirado) · `enrich_rdc_docx.py`
  (serie 3 años + cumplimiento desde los informes DOCX verificados) · **`ingest_rdc_corpus.py`** (informes
  completos → corpus Supabase, modo documento, idempotente por SHA256 · nuevo esta sesión).
- **UI (`m_rdc.py`):** sin cambio de código en esta pasada — la corrección fue aguas arriba (canon→snapshot).

## Validación
- **Snapshot:** `cpccs` = `{marco_legal, brecha_compromisos}` (fecha_rdc retirado ✓) · `brecha_compromisos`
  = "" → cajón muestra "—" (honesto) · serie `[2023, 2024, 2025]` · 21 componentes · fidelidad 91.0%.
- **Enrichers:** ambos re-ejecutados en orden, salida esperada al dígito (201/261/322 asistentes ·
  7/8/21 componentes · N°17649/22844/28432).
- **Corpus (ingesta):** 114 chunks RC-GAD insertados (79.4s, modelo local sin API) y verificados por
  dry-run post-ingesta (0 nuevos · todos en DB). El bug del `%` de `LIKE` en el reporte por-sigla (el
  driver lo tomaba como marcador de parámetro) se cazó **después** de ingestar y se corrigió — no afectó la
  deduplicación, que va por SHA256.
- **Compile + Firewall:** `py_compile` OK · escaneo de tokens prohibidos = 3 hits, **todos en docstring**
  (no en UI). Sin ICPI/TGI/IF_n/H-series en pantalla.
- **Disciplina:** el campo `fecha_rdc` erróneo se cazó en la capa 5 **antes** de firmar el cierre — es
  justamente lo que la auditoría de 7 capas existe para atrapar.

## Estado final
Dominio **CERRADO de cabo a rabo** al nivel de lo que el canon hoy sostiene: cajón documental con **serie
2023-2025**, **cumplimiento 2025 (21 componentes)**, **fidelidad narrativa 2024 (91%, 9 afirmaciones,
8 alta / 1 baja)** y **circuito CPCCS** con marco legal verificado. Cableado saneado (campo muerto retirado),
firewall limpio, narrativa honesta que **acota la fidelidad al año auditado** y muestra "—" donde falta dato.

**Pendientes honestos (adquisición de dato / workstream aparte — NO cómputo pendiente):**
- **Fidelidad 2025:** requiere el **NLP sobre el video** de la rendición 2025 (el diferenciador). H34b hoy
  cubre 2024; 2025 se incorpora cuando el pipeline de video extraiga el discurso afirmación por afirmación.
- **Compromisos CPCCS (`H24b!B7` / `H31!B65`):** vacíos — los informes no publican la tabla de compromisos
  adquiridos/cumplidos. El canon lo maneja bien (devuelve "sin datos", no un 0% falso). Es **adquisición**.
- **Canon-pureza (Regla 8, recomendación):** la serie de 3 años hoy **deriva** del DOCX en cada corrida;
  podría **estamparse** en el Gold Master (dato de hecho de los informes) para que el canon —no el enricher—
  sea su fuente. Aceptable como está (deriva de informes verificados); mejora futura.

---
*PCD-D09 · Dylus Lab © 2026 · segundo expediente del Protocolo de Curación de Dominio.*
