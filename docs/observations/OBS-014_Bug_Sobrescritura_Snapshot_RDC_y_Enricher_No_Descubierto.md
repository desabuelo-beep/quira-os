# OBS-014 · Bug de sobrescritura en `enrich_rdc.py` + enricher no descubierto en Fase 1 (d09)

**Fecha:** 2026-07-23 · **Contexto:** migración de d09 (Rendición de Cuentas) al patrón DOM_TEMPLATE.
**Severidad:** media — dato destructible en re-ejecución, sin afectar el Excel ni el ICPI.

## Qué pasó

1. **Fase 1 (Descubrimiento)** buscó enrichers de d09 con el patrón `rdc|rendicion|accountab` sobre
   `scripts/*.py` y encontró 4 archivos: `enrich_rdc.py`, `enrich_rdc_docx.py`, `fetch_rdc_cpccs.py`,
   `ingest_rdc_corpus.py`. **No encontró `scripts/enrich_aportes.py`** — su nombre no calza con el
   patrón de búsqueda, y el propio `enrich_rdc.py` (docstring) ya no lo menciona (fue añadido después
   del cierre de PCD-D09, 2026-07-02/03/04, y nunca se registró en el Master Index).

2. Al generar el paquete de evidencia reproducible (`EVIDENCIA_d09`) se ejecutaron `enrich_rdc.py` y
   `enrich_rdc_docx.py` en el orden documentado por PCD-D09. **Esto borró el bloque
   `rendicion.aportes`** (96 aportes ciudadanos cruzados contra POA, 44 validados) que un tercer
   script — `enrich_aportes.py` — había escrito en una sesión anterior (2026-07-03/04).

3. **Causa raíz:** `enrich_rdc.py::main()` hacía `snap["rendicion"] = block` — una sobrescritura
   ciega de TODO el sub-objeto `rendicion`, en vez de fusionar. `enrich_rdc_docx.py` y
   `enrich_aportes.py` sí fusionan correctamente (`rend = snap.get("rendicion") or {}`,
   `snap.setdefault("rendicion", {})["aportes"] = block`). Solo `enrich_rdc.py` era destructivo.

## Cómo se detectó y contuvo

- El diff de `git diff --stat data/gm_snapshot.json` mostró **1295 líneas eliminadas, 0 insertadas**
  tras correr un solo enricher — desproporcionado para un re-cálculo de fidelidad/cpccs. Se detuvo
  la operación de inmediato y se restauró el snapshot con `git restore` (el archivo no estaba
  comiteado) antes de investigar.
- Investigación: `grep -rn '"aportes"' scripts/` reveló `enrich_aportes.py` y confirmó, en su propio
  docstring, la intención correcta ("Escribe snap['rendicion']['aportes'] (merge, preserva
  fidelidad/cpccs/serie)") — es decir, el autor de `enrich_aportes.py` ya sabía que `enrich_rdc.py`
  debía preservar lo ajeno; el bug estaba únicamente en `enrich_rdc.py`.

## Corrección

`scripts/enrich_rdc.py::main()`: `snap["rendicion"] = block` → 
```python
rend = snap.get("rendicion") or {}
rend.update(block)
snap["rendicion"] = rend
```
Verificado: correr `enrich_rdc.py` solo, ahora, preserva `aportes` (96) y `serie` (3) intactos
(`git diff --stat data/gm_snapshot.json` → sin cambios tras el fix).

## Alcance de la corrección de catálogo

`data/d09/catalogo_d09_v1.0.0.yaml` se completó con un 4º hecho documental (`aportes_ciudadanos`),
`app/agents/d09/motor.py` lo expone, y `scripts/cypher/006_d09_rendicion.cypher` genera su nodo
`Metrica` + `Fuente H10c_aportes`. Se cataloga con su **estado real de gobernanza**: operacional
desde 2026-07-03/04, pero la metodología formal (`METODOLOGIA_TRAZABILIDAD_APORTES.md`) sigue
**v0.3 pendiente de aval de Javo** — no se presenta con el mismo peso que RO-IX-001 (ya ratificada
el 2026-07-20). Fundamento legal ya cubierto por la cadena existente: LOPC Art.89 (eslabón 3 de
CNO-IX-001), consultivo/advisory — distinto del Presupuesto Participativo (vinculante, COOTAD
Art.238), que se rutea a d08 y no aparece aquí.

## Lección para el patrón DOM_TEMPLATE

La Fase 1 (Descubrimiento) debe buscar enrichers por **contenido** (`grep "rendicion\|aportes\|serie"
scripts/*.py` — qué clave del snapshot escriben) y no solo por **nombre de archivo**. Cuando un
dominio tiene más de un enricher, verificar explícitamente que cada uno **fusiona** en vez de
sobrescribir antes de darlo por completo — el mismo tipo de auditoría de cableado que ya encontró el
campo muerto `cpccs.fecha_rdc` en PCD-D09 (capa 5).

---
*OBS-014 · Dylus Lab © 2026 · disciplina: el diff desproporcionado se detuvo antes de comitear, no después.*
