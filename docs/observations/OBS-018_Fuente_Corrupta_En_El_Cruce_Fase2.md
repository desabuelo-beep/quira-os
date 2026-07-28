---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3]
  type: OPERATIVA
---

# OBS-018 · Fuente corrupta en el primer cruce de Fase 2 — el canon ya lo advertía

**Fecha:** 2026-07-27 · **Dominio:** d08 · **Severidad:** alta (resultado inválido, detectado
antes de publicar) · **Naturaleza:** error de dirección técnica, corregido.

## Qué pasó

El primer cruce de Fase 2 (demanda ciudadana → POA) usó como fuente de ejecución el **corpus
vectorizado** (`POA-GAD-2025`, 1434 chunks). Produjo números presentables —40 hipótesis, 94
pendientes, 89 sin correlato— que eran **completamente inválidos**.

El texto contra el que "coincidían" las demandas era ilegible:

```
"bsta idl s iae d r li eao s INDICADOR OPERATIVO mai P nno ftr rea cne ei"
```

El mismo chunk corrupto (`sha 72b5a3aa68bd`) aparecía como match de cuatro demandas distintas.
Una similitud de 0.727 contra texto basura **es ruido, no señal**.

## El canon ya lo advertía — y no se consultó

`docs/architecture/METODOLOGIA_TRAZABILIDAD_APORTES.md` §3 dice literalmente:

> ⚠️ **NO usar el corpus vectorizado para el cruce de POA:** la vectorización de esos PDFs quedó
> **corrupta** (OCR fallido — chunks de caracteres sueltos «n n n», «. . 4 7 0»). La fuente de
> ejecución es el **PDF re-extraído**, no `POA-GAD-20xx` del corpus.

**Es el tercer caso del mismo patrón en una sola sesión:** la información existía en el canon y no
se consultó antes de actuar (los otros dos: los postulados de la tesis y los conceptos del marco
epistémico — ver `marco_teorico/INVENTARIO_CONCEPTOS_FUNDACIONALES.md`).

## Segundo error, encadenado
Al corregir la fuente (XLSX oficial del GAD, texto limpio sin OCR), el cruce seguía inválido: los
matches eran **membretes y filas de encabezado** (*"GOBIERNO AUTONOMO DESCENTRALIZADO DEL CANTON
MONTECRISTI"*, *"NO. DE ACTIVIDAD · PARTIDA · MONTO"*). El extractor tomaba cualquier fila con
texto. La solución también existía ya: `scripts/extract_poa_pdf.py::_HDR_TOKENS`.

## Corrección aplicada
1. Fuente: **XLSX oficial del GAD** (`POA 2023-2026/GAD Montecristi/*.xlsx`) — estructurado, sin
   OCR. 1027 filas sustantivas de 4 años.
2. Filtro de encabezados reusando los tokens del extractor existente (Regla 7: no reinventar).
3. El resultado final tiene **señal real con ruido conocido**, correctamente etiquetado como
   `hipotesis` — nunca como hecho.

## Lección — regla operativa que se adopta
> **Antes de elegir una fuente de datos, consultar si el canon ya se pronunció sobre su calidad.**
> El corpus no es uniformemente confiable: los informes RDC son texto sano; los PDF de POA
> quedaron corruptos. Esa distinción **está documentada** y debe leerse antes, no descubrirse
> después.

Se suma a la regla del Inventario de Conceptos: *antes de crear, consultar*. Aquí: *antes de
consumir una fuente, consultar su estado documentado*.

## Por qué esto no llegó a ser un daño
El error se detectó **antes de publicar cualquier resultado**, al inspeccionar la evidencia
concreta en lugar de aceptar los números agregados. Es exactamente lo que el Principio de
No-Inferencia y el Horizonte de Verdad existen para forzar: **mirar la evidencia, no la métrica**.

---
*OBS-018 · Dylus Lab © 2026 · el canon advirtió; la dirección técnica no lo consultó a tiempo.*
