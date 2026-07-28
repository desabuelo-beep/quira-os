---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 3, 4, 9]
  type: OBSERVACION
---

# OBS-019 · El metadato institucional leído como contenido sustantivo

**2026-07-29 · d08 Participación Ciudadana · Fase 2 · deriva de la calibración del Filtro Ontológico**

> **Patrón, no incidente.** Es la **tercera vez** que el mismo error rompe el cruce de
> demandas ciudadanas contra el POA. Se registra como observación de método —no como bug—
> porque la corrección puntual ya se aplicó tres veces y volvió a aparecer.

---

## 1 · El hallazgo

La fila del POA no contiene solo el proyecto. Contiene:

```
partida presupuestaria  ·  descripción del proyecto  ·  unidad administrativa responsable
```

El filtro clasificaba sobre la fila completa. `"Obras Públicas"` figuraba como rubro
compatible de **tres familias** (áreas verdes · vialidad · riesgos) — y en un GAD esa
dirección ejecuta parques, viales, muros **y arriendo de edificios**. Resultado observado:

| Demanda ciudadana | Proyecto emparejado | Veredicto emitido |
|---|---|---|
| `INUNDACIONES- MANANTIALES` | `Edificios, Locales, Parqueaderos, Casilleros Judiciales (Arrendamientos)` | **directa · riesgos** |

El sistema no clasificó por lo que se hace, sino por **quién lo ejecuta**.

### Las tres ocurrencias del mismo patrón

| # | Metadato confundido con contenido | Efecto |
|---|---|---|
| 1 | **Membrete** (`GOBIERNO AUTONOMO DESCENTRALIZADO…`) | el encabezado emparejaba con toda demanda |
| 2 | **Rubro de festejos** (`Feriado carnaval · Espectáculos`) | capturaba demandas de infraestructura |
| 3 | **Unidad ejecutora** (`Dirección de Obras Públicas`) | 22 correspondencias falsas con relación *fuerte* |

Las tres son la misma falla: **texto administrativo que acompaña al dato, tratado como el dato**.

## 2 · La regla que nace (REGLA 0 del Filtro Ontológico)

> **Quién ejecuta no acredita qué se hace.** El nombre de la unidad responsable es un
> atributo administrativo, no técnico. Se elimina del texto **antes** de clasificar.

Implementada en `scripts/d08/filtro_ontologico.py::_sin_unidad_ejecutora`. Vale para los
**222 GAD**: todos tienen Dirección de Obras Públicas, Planificación, Financiera, y todos
las arrastran en la columna de responsable de su POA.

**Invariante permanente:** ninguna whitelist de rubros puede nombrar una unidad
administrativa. Verificado por `scripts/d08/test_filtro_ontologico.py`.

## 3 · Defecto de trazabilidad que lo mantuvo oculto

El expediente guardaba el proyecto **recortado a 200 caracteres**, mientras el filtro
juzgaba **400**. El token que disparaba el veredicto quedaba fuera del registro: la
correspondencia era **inauditable**. Al inspeccionar el JSON, el falso positivo parecía
inexplicable porque la evidencia guardada no era la evidencia juzgada.

> **Regla derivada:** se persiste **exactamente** el texto que produjo el veredicto. Un
> expediente que no permite reconstruir el juicio no es expediente (Postulado I ·
> Trazabilidad Biográfica).

## 4 · Efecto medido de la corrección

| Corrida | Con correlato | Sin correlato | Gobierna |
|---|---|---|---|
| v1 · umbral 0.52, top-10 | 71 | 151 | el **umbral** |
| v2a · filtro, piso 0.42, top-30 | 153 | 70 | el **filtro** (contaminado) |
| **v2b · + REGLA 0** | **131** | **92** | el **filtro** (limpio) |

- El paso v1→v2a corrigió **falsos negativos** reales: `"áreas verdes"` sin correlato pasó de 11 a 2.
- El paso v2a→v2b eliminó **22 correspondencias falsas** que dependían de la unidad ejecutora.
- Correspondencias fuertes que aún dependen del nombre de la unidad: **0**.

## 5 · Hallazgo adjunto — la extracción depende del formato del acta

Al revisar los residuos apareció un defecto **de Fase 1, no del filtro**: **9 de 223 (4%)**
"demandas" son fragmentos narrativos del acta, no peticiones ciudadanas:

> *"Frente a esta solicitud, el alcalde expresó su compromiso con el sector…"*

**Las 9 provienen de audiencias públicas.** Ninguna de presupuesto participativo. La razón
es estructural: las actas de PP son **listas tabulares** (una fila = una demanda); las de
audiencia pública son **prosa corrida**, donde la petición viene envuelta en narración de
tercera persona.

No son todas ruido — *"Cesar Holguín manifestó la problemática de la pésima recolección de
basura"* **sí es una demanda**, mal delimitada. Requiere **desenvoltura**, no descarte.

> Esto confirma empíricamente la **Teoría de la Evidencia Pública Verificable**: la
> estructura del documento determina qué puede extraerse. No es un problema de algoritmo —
> es la calidad institucional del acta. Alimenta el ICEP del d07.

## 6 · Cuestión abierta para decisión de Javo

¿La **siembra de árboles** es instrumento *funcional* de mitigación de riesgo en quebradas?
Técnicamente la reforestación estabiliza taludes. El filtro hoy responde `nula` de forma
**conservadora**: no existe rubro técnico que lo acredite, y `sin_correlato` **no afirma que
no se atendió** (Principio de No-Inferencia). Antes respondía `funcional`, pero **por el bug
de REGLA 0** — no por conocimiento del dominio. Si Javo confirma la relación, se incorpora
el rubro; **no se infiere sin él**.

## 7 · Acciones

| # | Acción | Estado |
|---|---|---|
| 1 | REGLA 0 · eliminar unidad ejecutora antes de clasificar | ✅ aplicada |
| 2 | Persistir el texto íntegro juzgado | ✅ aplicada |
| 3 | Test de regresión con invariante estructural | ✅ `test_filtro_ontologico.py` (9 casos) |
| 4 | Desenvolver demandas narrativas de actas en prosa | ⏳ Fase 1 · pendiente |
| 5 | Segunda ronda de validación experta sobre la mezcla nueva | ⏳ pendiente de Javo |
| 6 | Decidir reforestación como rubro de mitigación de riesgo | ⏳ pendiente de Javo |

---
*OBS-019 · Dylus Lab © 2026 · deriva de la calibración del Filtro Ontológico v2.*
