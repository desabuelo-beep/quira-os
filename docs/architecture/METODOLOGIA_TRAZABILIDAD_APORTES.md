# METODOLOGÍA — Trazabilidad de Aportes y Compromisos Ciudadanos (d09)

> **PROPUESTA v0.1 · para revisión de Javo** (Regla 9: el cambio conceptual nace en el canon,
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
- **Compromisos CPCCS:** `H24b` (tablero SAT-V, hoy `B7=0` — adquisición de dato pendiente).
- **Ejecución (la evidencia — decisión Javo 2026-07-03: *ejecución real*, no auto-reporte):**
  - Proyectos POA `H05` (bloque «DETALLE PROYECTOS», col Descripción/Partida/Monto · ~257).
  - Procesos PAC/SERCOP `H05b` (descripción · monto · estado · ~32).
  - Presupuesto ejecutado eSIGEF `H07`.

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
son **correctos** (agua/vías/alcantarillado). **Subestimado**: se cruzó contra POA **2026** por ser lo
único en el canon; con el POA/PAC de los años correctos mejora. Los scores bajos aíslan honestamente
las demandas de otra competencia (p.ej. salud) o no atendidas.

## 5 · Estructura de la trazabilidad (hoja nueva en el Gold Master)
Por cada aporte: `Año · Aporte · Sector · Eje_PDOT · Tipo │ Proyecto_POA · Partida · Monto ·
Proceso_SERCOP · Estado │ Nivel_Atención · Score · Validado_por`.
- **Nivel_Atención:** `Atendido` · `Parcial` · `Sin correlato (canon actual)` · `Fuera de competencia`.
- Distinción crítica: **«sin correlato en el canon actual» ≠ «no atendido»** (puede faltar el año de
  ejecución). Hasta tener los años completos, esos aportes se marcan **«en formación»**.

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

## 8 · Plan de construcción (7 capas · PCD)
1. Canon: crear hoja de trazabilidad (cirugía Gold Master · sobre copia · B33 intacta).
2. Poblar: cruce semiautomático + validación (arranque 2023-2024 con H10c).
3. Cableado: enricher `enrich_aportes.py` → snapshot.
4. Matemática: indicadores de atención + serie.
5. Visual + Narrativa: sección nueva en la lectura de d09.
6. Cierre: actualizar `PCD-D09`.

---
*Metodología de Trazabilidad de Aportes · Dylus Lab © 2026 · PROPUESTA v0.1 (pendiente aval de Javo).*
