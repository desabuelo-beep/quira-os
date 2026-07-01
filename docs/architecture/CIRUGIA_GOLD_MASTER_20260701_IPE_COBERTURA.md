# CIRUGÍA GOLD MASTER — 2026-07-01 · Cobertura de Metas POA (H16b)

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

---
*Cirugía Gold Master · Dylus Lab © 2026 · la fórmula canónica es INMUTABLE · correcciones solo en inputs/semáforo/presentación, sobre copia, con evidencia verificada.*
