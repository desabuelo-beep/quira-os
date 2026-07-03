# METODOLOGÍA — Trazabilidad de Aportes y Compromisos Ciudadanos (d09)

> **PROPUESTA v0.3 · para revisión de Javo** (Regla 9: el cambio conceptual nace en el canon,
> no en Python). Sesión 2026-07-03 · asesor + Javo + Claude. Fundamenta la expansión de d09
> con la sección *Compromisos CPCCS + Aportes Ciudadanos*.

## 1 · El problema (por qué existe esta sección)
En la rendición de cuentas la ciudadanía plantea **demandas y aportes**, y el GAD **adquiere
compromisos** ante el CPCCS. Eso es **otra promesa pactada** — hermana del plan de campaña (CNE) —
y hoy nadie verifica si se cumplió. QUIRA la convierte en **trazabilidad auditable**: cada aporte se
sigue hasta su ejecución real (POA · PAC/SERCOP · presupuesto) y se **cuantifica, visualiza y explica**.

## 2 · Marco legal (verificado)
- **Aportes ciudadanos RDC = Advisory** — LOPC **Art. 89** (consultivo: orientan, no obligan).
- **Presupuesto Participativo = Vinculante** — COOTAD **Art. 238** (obliga). *(Se rutea a d08, no aquí.)*
- **Compromisos ante el CPCCS** — LOPC **Art. 88** (seguimiento de compromisos de la rendición).
- Consecuencia de registro: un aporte no atendido **no es ilegal** (es advisory) — el lenguaje es
  **de seguimiento**, nunca acusatorio (Regla 2). Pero la **brecha entre lo pedido y lo ejecutado
  queda a la vista**, con evidencia.

## 3 · Fuente de verdad (canon)
- **Aportes:** `H10c_RDC_APORTES` — **108 demandas verificadas** (43 en 2023 · 65 en 2024), cada una
  con actor, sector/lugar, eje PDOT, tipo y **link de verificación**. (2025 se estructura después.)
- **Compromisos CPCCS:** `H24b` (tablero SAT-V, hoy `B7=0`). El dato se **extrae de los informes RDC
  del corpus** (Supabase · `RC-GAD-2023/2024/2025`) — no existe estructurado en otra fuente (Javo 2026-07-03).
- **Ejecución (la evidencia — decisión Javo 2026-07-03: *ejecución real*, no auto-reporte):**
  - Proyectos POA `H05` (bloque «DETALLE PROYECTOS», col Descripción/Partida/Monto · ~257 · **2026**).
  - Procesos PAC/SERCOP `H05b` (descripción · monto · estado · ~32).
  - Presupuesto ejecutado eSIGEF `H07`.
  - **Ejecución multi-anual (2023-2026):** los PDFs oficiales de POA/PAC/Cédulas están en disco
    (`Holding_Municipal_Montecristi`) y son **texto limpio extraíble** — `pdfplumber.extract_tables`
    da `actividad · partida · monto · responsable` por año (verificado 2026-07-03).
  - ⚠️ **NO usar el corpus vectorizado para el cruce de POA:** la vectorización de esos PDFs quedó
    **corrupta** (OCR fallido — chunks de caracteres sueltos «n n n», «. . 4 7 0»). La fuente de
    ejecución es el **PDF re-extraído**, no `POA-GAD-20xx` del corpus. (Los informes RDC sí son texto sano.)

## 4 · El método de cruce (semiautomático · *evaluación experta trazable*)
Igual que el `IF_n` de fidelidad narrativa: **la máquina propone, el experto valida**. No es un JOIN
automático (el aporte es texto libre, sin ID común con la ejecución).
1. **Matching semántico** (embeddings locales, mismo modelo del corpus) aporte ↔ proyecto POA/PAC.
2. **Banda de decisión** (calibrada con el experimento de factibilidad):
   - `≥ 0.60` candidato **fuerte** → se propone el vínculo.
   - `0.50–0.60` **revisar** → validación experta obligatoria.
   - `< 0.50` **sin correlato** → se señala como demanda sin reflejo en la ejecución (información, no error).
3. **Validación experta** confirma/corrige el vínculo propuesto.
4. **Evidencia registrada:** proyecto POA + partida + monto + proceso SERCOP + estado + score + validador.

### Factibilidad probada (experimento 2026-07-03)
108 aportes × 289 ítems de ejecución (POA+PAC). Match plausible `≥0.5`: **87%**; los vínculos fuertes
son **correctos** (agua/vías/alcantarillado). **Subestimado**: se cruzó contra POA **2026** — un solo
año del periodo. Con el POA/PAC de **todos los años del periodo** (ventana §5) el correlato sube y se
clasifica por `Tiempo_Respuesta`. Los scores bajos aíslan honestamente las demandas de otra competencia
(p.ej. salud) o no atendidas.

## 5 · Estructura de la trazabilidad (hoja nueva en el Gold Master)
Por cada aporte: `Año_Aporte · Aporte · Sector · Eje_PDOT · Tipo │ Proyecto_POA · Año_Ejecución ·
Partida · Monto · Proceso_SERCOP · Estado │ Nivel_Atención · Tiempo_Respuesta · Score · Validado_por`.
- **Nivel_Atención:** `Atendido` · `Parcial` · `Sin correlato` · `Fuera de competencia`.
- **Tiempo_Respuesta** (aporte de Javo 2026-07-03 — **la ventana es el periodo de gobierno completo**,
  no solo el año siguiente):
  - ✅ `A tiempo` — atendido en el POA del **año siguiente** (lo legalmente esperable).
  - 🟡 `Tarde` — atendido **después, dentro del periodo 2023-2027** (cumplió, con demora).
  - 🔴 `Olvidado` — **no aparece en ningún POA del periodo**.
  El cruce se hace contra la **unión multi-anual** de POA/PAC/eSIGEF (todos los años del periodo);
  `Año_Ejecución` registra en qué año se materializó. Distingue *olvido* de *cumplimiento tardío*.
- Distinción crítica: **«sin correlato en el canon actual» ≠ «olvidado»** — hoy solo está el POA 2026;
  hasta poblar los años del periodo, los aportes sin match se marcan **«en formación»**, no «olvidado».

## 6 · Indicadores y visualización (elevar el nivel)
- **% de aportes con correlato de ejecución**, por **año · eje PDOT · tipo · territorio**.
- **Serie 2023 → 2024 → 2025** (cuando 2025 se estructure): ¿mejora la capacidad de respuesta?
- Formas gráficas nuevas (estilo Planificación): **mapa de calor aporte×eje**, **flujo demanda→ejecución**,
  **atención por parroquia/sector**, ranking de demandas recurrentes.

## 7 · Firewall y honestidad
- Lenguaje de **administración pública**: «en seguimiento», «correspondencia», «brecha» — nunca
  «incumplió/violó». Advisory ≠ obligación.
- Sin `H-series`/`ICPI`/scores crudos en UI. El score de matching es interno; en pantalla va el
  **vínculo validado** con su evidencia.
- Nada se afirma sin evidencia (Regla 3): un aporte «Atendido» **muestra** su proyecto/partida/contrato.

## 8 · Construcción (ejecutada) y el canon de la trazabilidad
**NO hay cirugía del Gold Master** (corrección v0.3 · Regla 1). El cruce aporte↔obra es una derivación
**semántica** (embeddings + validación experta), **no una fórmula que el Excel recalcule** —a diferencia
del IPE (`SUMAPRODUCTO` nativo, que el Excel sí calcula). Estampar su resultado en el Excel sería
**Python→Excel**, prohibido por la Regla 1 (Excel→Python→Supabase→UI, *nunca al revés*). El canon de la
trazabilidad de aportes NO es una hoja nueva, sino:
- **Inputs (ya en el Gold Master):** `H10c` (aportes verificados) + los POA oficiales (PDF/DOCX).
- **Decisiones ratificadas:** `data/aportes_validacion.json` (versionado en git · sello humano de Javo).
- **Método:** esta metodología.
- El cruce **DERIVA** de ahí: `extract_poa_pdf.py` + `enrich_aportes.py` → snapshot → UI.

**Pasos ejecutados (2026-07-03/04):** (1) extracción POA 2024-2026 (2025 desde DOCX) · (2) cruce de
ventana de periodo + validación experta ratificada → **49 atendido / 47 sin correlato** · (3) sección
«La voz ciudadana» en la lectura de d09, marco legal en bloque · (4) cierre en `PCD-D09` (tras el NLP).

---
*Metodología de Trazabilidad de Aportes · Dylus Lab © 2026 · PROPUESTA v0.3 (pendiente aval de Javo).*
