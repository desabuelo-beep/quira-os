---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-016 · Desalineación de nomenclatura SAT — canon BRN vs Gold Master

**Fecha:** 2026-07-24 · **Contexto:** al modelar las SAT de d08 (participación).
**Severidad:** media — afecta la trazabilidad canon↔motor de varios dominios. **NO se toca
el Gold Master.** Insumo de auditoría transversal (posterior).

## Cómo se destapó
Al construir d08 modelé **7 SAT (`SAT-VIII-001..007`, una por mecanismo)** siguiendo la
"Opción C". Javo corrigió: las SAT no son 1:1 con mecanismos, y de las señales del Gold
Master **solo una es de participación**. Al leer `SAT_Catalogo` (Gold Master) se confirmó.

## Cómo son las SAT en el Gold Master (la verdad del motor)
`SAT_Catalogo` define **9 señales de alerta temprana** (SAT-0 … SAT-VIII), cada una mapeada
a una **dimensión TGI (D1-D5)**, con base legal, métrica observable, umbral, peso y tipo:

| SAT (GM) | Alerta | Dim TGI | Dominio QUIRA |
|---|---|---|---|
| SAT-0 | Coherencia POA-PAC | D2 | d01/d02 |
| SAT-I | Fragmentación Selectiva | D3 | d03 |
| SAT-II | Reforma Significativa Tardía | D2 | d02 |
| SAT-III | Parálisis Presupuestaria | D3 | d02 |
| SAT-IV | Alerta Fiscal COOTAD | D3 | d02 |
| SAT-V | Brecha Compromiso CPCCS | D5 | d09 |
| **SAT-VI** | **Desvío Presupuesto Participativo** | **D4** | **d08** |
| SAT-VII | Vi Sináptico Pulso | D3 | informacional |
| SAT-VIII | Equidad Territorial | D4 | d10/d12 |

Las SAT se numeran por **orden de creación / dimensión TGI**, NO por dominio.

## El hallazgo
La nomenclatura que usé en el canon BRN es **`SAT-{romano-dominio}-001`**, que NO coincide con
la del Gold Master:
- **d08:** puse `SAT-VIII-001..007` → **colisión**: `SAT-VIII` en el GM es *Equidad Territorial*
  (otro dominio), no participación. La señal real de d08 es `SAT-VI`.
- **d09:** puse `SAT-IX-001` → el GM no tiene `SAT-IX`; la señal de CPCCS es `SAT-V`.
- **d02:** puse `SAT-IV-001` → coincide por casualidad con `SAT-IV` (Alerta Fiscal), pero el
  sufijo `-001` no existe en el GM.
- **d01/d03:** `SAT-I-001` / `SAT-III-001` → revisar contra SAT-0/SAT-I del GM.

Es decir: las RO del canon **consumen ids de SAT que no siempre existen con ese nombre en el
motor**. La cadena CNO→RO→SAT queda trazada contra una nomenclatura propia, no contra la real.

## Corrección aplicada a d08 (este OBS + commit asociado)
- Se retiran las 7 `SAT-VIII-00X` del canon (RO/CNO) y del grafo.
- La señal de participación es **`SAT-VI` (Desvío PP)** — hoy sin datos (`Hay_Datos_PP=NO`).
- `RO-VIII-003` (efectividad) consume `SAT-VI`; las SAT que falten se diseñan en fase 2.
- La verificabilidad documental por instancia (integridad, RO-VIII-001) **no es una SAT** —
  es el estado de la evidencia; se queda como criterios de evaluación.

## DOCTRINA DE 3 NIVELES SAT (consagrada · asesor 2026-07-24 + terreno Javo)
El asesor propuso separar "señal conceptual BRN" de "SAT operacional Excel". La doctrina es
correcta y se consagra AQUÍ para que d10/d11/… la hereden — pero con la ubicación precisa que
evita la colisión de nomenclatura (que el asesor no vio por no conocer el `SAT_Catalogo`):

- **Nivel 1 · BRN (conceptual):** las señales/riesgos que el dominio identifica y vigila viven
  como **CRITERIOS de la RO** (¿consta la ordenanza? ¿la resolución?), NO como nodos "SAT-…" con
  nomenclatura del motor. Así el BRN queda libre de decisiones de implementación (cuántas SAT,
  si se fusionan) SIN inventar ids que colisionen con el Gold Master.
- **Nivel 2 · Excel Gold Master (operacional):** las SAT reales (`SAT-0..VIII` por dimensión
  TGI), cada una con fórmula, fuente, variable, ponderación y salida. Solo entran las
  operacionalizadas. El BRN las **REFERENCIA por su id real del GM** (RO `consume: [SAT-VI]`),
  nunca las inventa.
- **Nivel 3 · QUIRA (evidencia):** QUIRA **no crea SAT**. Produce la evidencia documental que
  alimenta las variables del Excel; el Excel calcula la SAT; la SAT alimenta el IGP.

Flujo único: `evidencia (QUIRA) → variable (Excel) → SAT (Excel) → IGP (Excel)`. El BRN traza
la relación `RO ← consume ← SAT-real`, no una capa paralela de señales conceptuales numeradas.
Por eso d08 quedó con criterios en RO-VIII-001 (Nivel 1) + SAT-VI referenciada (Nivel 2) +
motor `evaluar_integridad` (Nivel 3): los tres niveles del asesor, sin resucitar las 7 SAT.

## Pendiente (auditoría transversal · NO ahora)
Revisar y realinear la nomenclatura SAT del canon (d01/d02/d03/d09) contra `SAT_Catalogo` del
Gold Master, decidiendo una convención única (id del GM vs alias por dominio con mapeo
explícito). Hasta entonces, cada RO debe declarar a qué SAT del GM corresponde su `consume`.

---
*OBS-016 · Dylus Lab © 2026 · el canon se traza contra el motor real, no contra una nomenclatura propia.*
