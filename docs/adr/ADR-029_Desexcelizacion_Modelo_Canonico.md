---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-029 · Desexcelización — el Gold Master es un Modelo Canónico, el Excel es un conector

**Estado:** RATIFICADO · 2026-06-21 (Javo + mesa) · decisión estratégica de escala
**Contexto de origen:** reconciliación de ruta — Javo: *"El Excel era para validar Montecristi; si escalamos a 221 municipios no es tener 2221 Excel sino un solo sistema."*
**Relacionado:** ADR-023 (3 niveles · Excel=motor) · ADR-024 (Radar Nacional · 221 GADs) · ADR-027 (3 capas soberanía) · `QUIRA_OS_INVENTARIO_CODIGO.md`

---

## Contexto

El Excel SIAP-ICPI fue el **laboratorio** para validar la metodología en Montecristi (el MOLDE).
Pensarlo como artefacto **permanente** es el error conceptual: **221 GADs ≠ 221 Exceles** — eso es
inmantenible. Igual que nadie vende el notebook donde entrenó un modelo: se vende el modelo, no el andamio.

## Decisión

**El Gold Master deja de ser, conceptualmente, "un Excel". Es un MODELO CANÓNICO.**
El Excel pasa a ser (a) su **representación actual** y (b) **un conector de entrada más**, junto a futuros
conectores: API ministerial · CSV/XML · SIGEF · SERCOP · CNE · INEC · SQL. Todos producen lo mismo:
**Datos Operacionales Canónicos.**

```
Excel ─┐
API   ─┤
CSV   ─┼─→  MOTOR ETL DETERMINISTA  ─→  MODELO CANÓNICO  ─→  Supabase · Neo4j · Snapshots ─→ productos QUIRA
SIGEF ─┤        (ingesta = QUIRA Operaciones)              (= el "Estado", Regla 1)
SERCOP─┘
```

### Ya estamos a medio camino (verificado · ADR-INVENTARIO)
El Excel **ya se lee 1 sola vez** (`scripts/_update_snapshot.py`) → se sella en snapshot; nadie más lo toca.
El sistema **ya trata al Excel como fuente sellada, no como base viva.** Desexcelizar = formalizar y
automatizar lo que la arquitectura ya insinúa: el Excel como plugin, no como cimiento.

### Lo que NO cambia (inviolable)
- **H12!B33 inmutable** · la metodología SIAP-ICPI · el Gold Master como **única autoridad de cálculo**.
- **Regla 1 (Excel=Estado)** se eleva a **"Modelo Canónico = Estado"**: Modelo→Python→Supabase→UI, nunca al revés.
- Solo cambia la **forma física** del modelo (pluggable): mañana puede vivir en Postgres/Supabase/DuckDB/Parquet.

## Operaciones vs Dylus — quién opera qué (refuerza ADR-024/027)

| | Opera | Responsabilidad | Lengua |
|---|---|---|---|
| **QUIRA Operaciones** | **el Estado** | recibe · valida · normaliza · versiona · sella · distribuye el dato (ingesta nacional) | administración pública (hacia afuera) |
| **Dylus Lab** | **QUIRA** | compilador · firewall · CID · ontologías · arquitectura · ciberseguridad · observabilidad · tuning | metodología canónica (hacia adentro) |

Analogía: **Windows opera el computador; Microsoft opera Windows.** Dylus no administra municipios — administra el sistema operativo que los observa.

## Consecuencias

- **Escalabilidad real:** 221 GADs = 221 **conectores** hacia **1 modelo canónico**, no 221 Exceles.
- El Excel deja de ser cuello de botella; se vuelve el primer conector (validación/migración).
- **Pertenece a la VÍA SISTEMA (S-4), no a la de producto.** NO se ejecuta ahora: primero el MOLDE
  Montecristi mostrable (Sprint D · CAF). La Desexcelización se construye cuando el producto lo permita.
- Disparador: tracción multi-cantón / barrido nacional (Sprint F). Antes, el Excel-conector basta.

## Precisión epistemológica (Javo · 2026-07-11) — el Modelo Canónico NO es "la verdad"

Refinamiento que corrige el malentendido recurrente *"el Gold Master es la verdad"*:

> **El Modelo Canónico es la _representación canónica de la evidencia procesada_ — la CAPA DE INTEGRACIÓN.
> NO es la verdad.** La verdad-verificable vive en las **fuentes**: PDOT · POA · PAC · SERCOP · SIGAD ·
> Presupuesto · Rendición. El Modelo integra, normaliza y representa esa evidencia. Cuando Regla 1 dice
> "Modelo Canónico = Estado", ese *Estado* es el estado de la **integración**, jamás un sustituto de la fuente.

Consecuencia metodológica (cambia bastante, no es cosmético):
- QUIRA no demuestra *"contra el Gold Master"*: demuestra **desde la fuente, a través de la integración**.
- El **motor Relacional (grafo)** es la capa que RE-ENLAZA la integración con las fuentes y las cruza entre
  sí: la *cadena de integridad intersistémica* (Constitución CAPA 0). Un eslabón roto en el grafo es **una
  fuente que no sostiene documentalmente a la siguiente**, nunca un error del Modelo ni una acusación.
- La **ausencia de evidencia en la fuente es un RESULTADO** de verificabilidad, no una autorización a inferir
  el hecho desde el Modelo. Coherente con el Principio Rector (CLAUDE.md · Constitución CAPA 0).

---
*ADR-029 · Desexcelización · Dylus Lab © 2026 · "El Excel fue el molde, no la estatua. El Gold Master es un modelo canónico; su forma física es reemplazable, su metodología no. Integra la evidencia — no la sustituye: la verdad vive en la fuente."*
