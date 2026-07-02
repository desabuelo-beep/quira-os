# CIRUGÍA GOLD MASTER — 2026-07-01 · Cobertura de Metas POA + IPE-ejecutado (H16b)

**Sobre COPIA · openpyxl (input) + Excel nativo COM recalc (malla) · `H12!B33` JAMÁS tocada · aditivo.**

> Cierre "en papel" del nudo POA→Meta ↔ IPE + primera cirugía aditiva sobre el canon v5.5.
> Metodología: `METODOLOGIA_GOLD_MASTER.md` · precedente: `CIRUGIA_GOLD_MASTER_D2A.md`.

## 1 · Ruteo de 5 hojas al cajón Planificación (RATIFICADO por Javo · 2026-07-01)
Regla: una hoja pertenece a la **pregunta que responde**, no a su nombre. Un solo dueño por hoja.

| Hoja | Qué hace (del dump) | Ruta |
|---|---|---|
| H11b_MONITOR_POLITICAS_PUBLICAS | Alinea 25 metas PDOT ↔ PND 2025-2029 (score/meta) | **Planificación (d01)** — evidencia propia; leída por d02/d13 |
| H16b_IPE | % del gasto de inversión vinculado a metas PDOT | **Planificación (d01)** — medidor del link POA→Meta |
| H19_ICS_ISP | Salud presupuestaria vs COOTAD Art.192 65% · SAT-IV | **Presupuesto (d02)** — frontera; d01 lee la señal |
| H37_SENSIBILIDAD_ESTRATÉGICA | Escenarios sobre ICPI (Pi/Ri/Ti) | **Instrumento transversal** (Motor Analítico QUIRA) · ⚠️ Firewall: no se renderiza |
| H38_ALCANCE_PREVENTIVO | Matriz SAT-0…VI → acción preventiva | **Instrumento transversal** (motor preventivo · d04) |

Pendiente: anclar en `MAPA_ANCLAJE_MOTOR.md` / `QUIRA_MASTER_INDEX.md` (coordinar — otro Claude edita canon compartido).

## 2 · Hallazgo POA→Meta ↔ IPE
- H05 (POA) ya está keyed 1:1 a las 25 metas (col A=ID_Meta). El link a nivel **PLAN es exacto**: **24/25 metas costeadas** (solo `AH-I-X-03` en $0 — Obj.1.3 grupos vulnerables/Patronato).
- IPE = "% del **gasto ejecutado** vinculado a metas". Denominador = devengado eSIGEF (H07!B19 = $1,947,738). El proxy ×0.84 era circular.
- **Escalas no comparables:** plan 25 metas = $39,310,032 ≠ devengado $1.95M ≠ codificado ~$30.3M. Un IPE-% planificado ingenuo da **2,018%** (basura). El IPE-% real necesita etiquetar el devengado por meta = **camino A**.
- Decisión (Javo): **cobertura ahora + camino A luego.**

## 3 · La cirugía (celda a celda · H16b_IPE)
Aditivo — solo celdas antes vacías (fila 12). NO se tocó B6:B11 ni H12.
```
A12 = "Cobertura_Metas_POA_2026"
B12 = =IFERROR(COUNTIF(H05_S3_OPERATIVO_POA!E14:E38,">0")/COUNT(H05_S3_OPERATIVO_POA!E14:E38),0)
C12 = nota: cobertura PLANIFICADA (no IPE-$); IPE-$ ejecutado pendiente camino A
```
Valor calculado (Excel nativo): **B12 = 0.96 (24/25 = 96%)**.

## 4 · Verificación (3 compuertas · Excel nativo determinista)
- ✅ `H12!B33` = 0.27458226534062735 — **idéntica** antes/después (canon intacto).
- ✅ `H12!B40` = "✅ AXIOMA VERIFICADO: ICPI = 69.9309%" — guardián del motor **pasa**.
- ✅ `H16b!B9` (proxy IPE) = 0.84 — **intacto**.
- ✅ Errores de fórmula: **5 en FREEZE = 5 en WORK · 0 nuevos** (los 5 preexistentes del D2A, fuera del motor ICPI).

## 5 · Trazabilidad de archivos (`…\ProyecT\`)
- FREEZE (rollback): `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260701_PRE_IPE.xlsx`
- WORK (cirugía):    `SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260701_IPE.xlsx`
- VIVO (promovido):  `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · SHA256 `60009C8722877ED4A6B86024E7D4DE38BA7BD9B1D789536641E63796DBE12219` · mtime 2026-07-01 03:10

## 6 · Siguientes pasos
1. **Camino A** — etiquetar devengado eSIGEF (H07) por meta → IPE-$ ejecutado real (cirugía mayor).
2. **Wiring snapshot/UI** — el enricher lee `Cobertura_Metas_POA` (H16b!B12) → surface en el cajón + la brecha de `AH-I-X-03`.
3. **UI del cajón** — los 6 cambios (flujo único, sin encabezado forense, ley inline, sin IA, sin memoria, fuentes grandes), con cierre **factual corto**.
4. **Anclar el ruteo** de §1 en el índice canónico (coordinar).

## 7 · Cirugía 2 — IPE-EJECUTADO real (H16b · 2026-07-01 · camino A nivel objetivo)

**Por qué se investigó antes de estampar:** el match EXACTO partida→objetivo daba IPE=61% —artefacto: el POA
planifica personal-de-inversión al nivel agregado `71` (2 díg) y el eSIGEF lo ejecuta en detalle `710xxx`
(6 díg). Con **match jerárquico** (respeta el clasificador presupuestario) se recupera el 89% del "no
vinculado"; el no-PDOT real es solo **$86,205 (4.4%)** — una obra, seguros, agrícolas.

**IPE-ejecutado real = 95.6%** (devengado inversión vinculado $1,861,533 / total $1,947,738).

**Cirugía (aditivo · H16b fila 14-17 antes vacías · proxy B6:B11 y cobertura B12 intactos):**
```
A15/B15  IPE_Ejecutado_2026_Real       = =IFERROR(B16/B7,0)  → 0.9557 (95.6%)   [fórmula]
A16/B16  Inversion_Vinculada_Real_USD  = 1,861,533.08   [valor QUIRA · evidencia: bridge jerárquico]
A17/B17  Inversion_No_PDOT_USD         = =IFERROR(B7-B16,0)  → 86,205.21          [fórmula]
```
Solo B16 es valor estampado; B15/B17 son fórmulas vivas. Reemplaza narrativamente el proxy B9 (×0.84).

**Verificación (WORK vs FREEZE · Excel COM):** ✅ `H12!B33` = 0.27458226534062735 idéntica · ✅ `H12!B40`
guardián pasa (ICPI 69.9309%) · ✅ 5=5 errores, **0 nuevos**.

**Archivos (`…\ProyecT\`):** FREEZE `…FREEZE_20260701_PRE_IPEEJEC.xlsx` · WORK `…WORK_20260701_IPEEJEC.xlsx` ·
VIVO `…v5.5_TGI.xlsx` SHA256 `9528BA299DAD3A257C98C3B3E6048A386E48A398E1C917C20BCF7BF6A0E41551` · mtime 09:02.

**Cableado:** enricher lee H16b!B15/B16/B7/B17 → `ipe_ejecutado` + computa `ipe_por_objetivo` (desglose · suma
= vinculado exacto) → snapshot → cajón sección **"EL GASTO VINCULADO AL PLAN"** (lenguaje gobernanza · sin "IPE").

**Nivel 25-metas:** pendiente — 0/257 proyectos POA traen `ID_Meta` (traen objetivo-texto). Requiere
meta-tagging de origen o heurística documentada con flag. No se fabrica (Regla 3).

## 8 · Cierre AUDIT-GRADE — IPE-ejecutado NATIVO en el Excel (2026-07-02)

**Riesgo cerrado (Javo: "¿y si nos auditan el Excel?"):** el IPE-ejecutado 95.6% vivía como **valor stampeado
desde Python** en `H16b!B16` —sin derivación dentro del Gold Master—. Ante una auditoría de la hoja, el número
no se podía rastrear. **Un dominio no está cerrado si el motor tiene un eslabón calculado fuera del Excel.**

**Solución:** `B16` (vinculada) pasa de valor a **FÓRMULA VIVA**, calculada por Excel:
```
B16 = SUMPRODUCT( inversión(7/8 en H07) · devengado(H07!E) · en_POA(COUNTIF H05 exacto + prefijo de grupo) )
```
Referencias: `H07_S5_FINANCIERO_eSIGEF` (devengado por partida, rangos A/E 46:180) + `H05_S3_OPERATIVO_POA`
(partidas del POA, E47:320). `B15` (IPE)=`=B16/B7` · `B17` (no-PDOT)=`=B7-B16`. Traceable celda a celda.

**Verificación (Excel COM ↔ Python · la prueba de fuego):** la fórmula del Excel reproduce EXACTO el bridge:
- `B16` = **$1,861,533.08** (idéntico) · `B15` = **95.57%** · `B17` = $86,205.21.
- ✅ `H12!B33` = 0.27458226534062735 idéntica · ✅ guardián `B40` pasa · ✅ 5=5 errores, 0 nuevos.

**Nivel objetivo = fiel a la fuente (verificado en H05):** el POA etiqueta los 257 proyectos por **OBJETIVO
(12)**, no por las 25 metas (col "Meta" = texto de objetivo). Solo el 36% del presupuesto mapea a una meta vía
Dirección; el 64% está en direcciones administrativas (Procuraduría, Comunicación, TI, Seguridad…) sin meta de
desarrollo. El IPE nativo a nivel objetivo/plan es lo auditable; el 25-metas exigiría meta-tag por proyecto en
la fuente (el municipio), no un mapeo derivado que un auditor objetaría.

**Archivos:** FREEZE `…FREEZE_20260702_PRE_IPENATIVE.xlsx` · WORK `…WORK_20260702_IPENATIVE.xlsx` · VIVO SHA256
`C8FE5F74367634144908FD4C7F89C5125E92FE14FD31B91395597A077649599E` · mtime 2026-07-02 05:09. Enricher/snapshot/UI
sin cambio (mismo valor cacheado). **Dominio Planificación cerrado de cabo a rabo.**

---
*Cirugía Gold Master · Dylus Lab © 2026 · la fórmula canónica es INMUTABLE · correcciones solo en inputs/semáforo/presentación, sobre copia, con evidencia verificada.*
