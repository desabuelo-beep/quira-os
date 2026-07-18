# Reforma Simulada · CNO-IV-001 — prueba de gobernanza (sin tocar el motor)

> **Qué es.** El ejercicio que el colega pidió **antes** de escribir una línea de integración con
> Python (2026-07-18): ejecutar **documentalmente** un caso de cambio y verificar que la propagación
> ocurre **exactamente como el canon la describe**. No se toca código, no se toca el Gold Master.
> Si aparece una duda, se corrige el canon; si no aparece ninguna, la arquitectura soporta un cambio real.
> **Precondición cumplida:** CNO-IV-001 v1.0 y RO-IV-001 v1.0 están `vigentes` (ratificadas 2026-07-18).

**Referencias:** `BRN_CICLO_VIDA_Y_MOLDE` (§4 versionado · §4b vigencia operativa · §5 propagación ·
§5b liberación) · `BRN_PLANO_MAESTRO` · ADR-038 §108 · ADR-039 (compilación).

---

## Distinción previa — vigencia operativa ≠ reforma (colega · 2026-07-18)
El paso **65 → 70** de esta regla **NO es una reforma**: la propia norma lo prevé (Disposición
Transitoria Primera → Art. 198.1). Es una **transición temporal** y se modela como **tramos de
vigencia operativa** dentro de la misma RO v1.0 (molde §4b) — **no versiona, no recompila por sí sola**:
el motor toma el umbral del tramo vigente a la fecha (65 en 2026, 70 desde 2027). Por eso los casos de
prueba de abajo usan **reformas reales**, no esa transición.

## Caso A — el legislador REFORMA el umbral (70 → 75) · reforma real
**Disparo:** una ley reformatoria futura sustituye el 70% del Art. 198.1 por **75%**. Es **texto nuevo**.

| Paso (ciclo de liberación §5b) | Qué ocurre | ¿Cambia? | Verificación |
|---|---|---|---|
| **Corpus** | ingresa el texto reformado (75%) con **SHA nuevo** | **SÍ** | sin SHA no entra (Regla 3) |
| **CNO-IV-001** | el eslabón `regla` apunta al SHA nuevo; `v1.0 → v2.0`; v1.0 archivada | **SÍ** | el MDN señala la CNO afectada |
| **RO-IV-001** | hereda CNO v2.0 → `v2.0`, umbral 75; v1.0 pasa a `obsoleta` | **SÍ** (N sube · §4) | nace `propuesta` → validación humana → `vigente` |
| **Compilación** | recompila RO v2.0 → **artefacto firmado** nuevo (build+SHA) | **SÍ** | determinista·reproducible·idempotente (ADR-039) |
| **Gold Master** | recibe umbral 75 por config compilada; **no consulta** la BRN | **SÍ** (H24: 70→75) | Regla 1 intacta — se reconfigura, no se edita |
| **SAT-IV-001** | recomputa con 75; su definición no cambia | **NO** (sigue → RO-IV-001) | la SAT no conoce el número; lo hereda |
| **DOM d02** | muestra 75 | **NO** (código) | lee el umbral de la config, no lo hardcodea |

**Intervenciones humanas: una** (validar RO v2.0). **Código tocado: cero.** **Gold Master editado a
mano: no.** → **La arquitectura soporta una reforma de umbral.** ✅

## Caso B — el legislador agrega una EXCEPCIÓN (nuevo artículo) · reforma de cadena
**Disparo simulado (artículo ficticio):** una reforma agrega el `Art. 198.7 — excepción por
emergencia declarada` a la cadena de la regla.

| Paso | Qué ocurre | ¿Cambia? | Verificación |
|---|---|---|---|
| **Corpus** | ingresa el texto del 198.7 con su **SHA** | **SÍ** | Regla 3 |
| **CNO-IV-001** | se agrega el eslabón; `v2.0 → v3.0`; anterior archivada | **SÍ** (nueva cadena) | el MDN marca la CNO |
| **RO-IV-001** | si el 198.7 introduce una excepción operativa (p. ej. "el umbral no aplica en emergencia") → nueva **lógica** → nueva RO; si es solo declarativo → la RO **re-apunta** al SHA sin versionar | **depende** | lo decide la **validación humana**, no la IA (Neutralidad Operativa) |
| **Compilación → Gold Master → SAT → DOM** | igual que el Caso A **solo si** la RO cambió | condicional | si la RO no cambió, el motor **no** se recompila |

**Prueba clave:** agregar Derecho a la cadena **no obliga** a recompilar el motor. Solo se propaga
aguas abajo si la **lógica** cambió. → **La arquitectura separa correctamente los dos ejes.** ✅

---

## Resultado del ejercicio
- **Ninguna duda estructural apareció.** Los dos ejes de cambio (umbral vs. cadena) se propagan por
  caminos distintos, con **una sola** intervención humana y **sin editar el motor a mano**.
- **Se distingue vigencia de reforma** (§4b): la transición 65→70 no versiona (la prevé la norma);
  solo una reforma del **texto** (70→75, o un nuevo artículo) versiona y recompila.
- **Se confirma la separación CNO/RO** (ADR-038 §108): un cambio de umbral por reforma sube la CNO y
  la RO; un artículo declarativo puede subir solo la CNO. La lógica de negocio no se dispersa.
- **Se confirma la Regla 1**: el Gold Master se **reconfigura por compilación**, nunca se edita ni
  consulta la BRN en runtime. Y el **ciclo de liberación §5b**: el artefacto firmado es la única bisagra.

**Conclusión.** La BRN v2 soporta un cambio normativo real y distingue una transición temporal de una
reforma. Concluye la fase de **diseño**; procede la de **implementación incremental** — empezando por
el compilador RO→Gold Master (ADR-039), cuando Javo lo disponga. Cualquier cambio de fondo se justifica
en un ADR. Esto es lo que permite **operativizar progresivamente los 222 cantones** sobre el mismo molde.

---
*Reforma Simulada · CNO-IV-001 · Dylus Lab © 2026 · "Probamos la gobernanza antes que el motor: la arquitectura reformó un umbral y agregó un artículo sin tocar una línea de código ni el Gold Master, y supo distinguir una transición prevista de una reforma real. Está lista para ejecutar."*
