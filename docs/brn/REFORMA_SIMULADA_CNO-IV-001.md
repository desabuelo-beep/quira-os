# Reforma Simulada · CNO-IV-001 — prueba de gobernanza (sin tocar el motor)

> **Qué es.** El ejercicio que el colega pidió **antes** de escribir una línea de integración con
> Python (2026-07-18): ejecutar **documentalmente** un caso de cambio y verificar que la propagación
> ocurre **exactamente como el canon la describe**. No se toca código, no se toca el Gold Master.
> Si aparece una duda, se corrige el canon; si no aparece ninguna, la arquitectura soporta un cambio real.
> **Precondición cumplida:** CNO-IV-001 v1.0 y RO-IV-001 v1.0 están `vigentes` (ratificadas 2026-07-18).

**Referencias:** `BRN_CICLO_VIDA_Y_MOLDE` (§4 versionado · §5 propagación · §5b liberación) ·
`BRN_PLANO_MAESTRO` · ADR-038 §108 (por qué el desacople) · ADR-039 (compilación).

---

## Caso A — cambia el UMBRAL (65 → 70), la cadena NO cambia
**Disparo real:** al terminar el régimen transitorio, deja de aplicar el piso del 65% (Disposición
Transitoria Primera) y entra la regla plena del 70% (Art. 198.1). El 70% **ya vive en el Corpus** —
no hay texto nuevo. Es el caso más común y el que prueba la separación CNO/RO (ADR-038 §108).

| Paso (ciclo de liberación §5b) | Qué ocurre | ¿Cambia? | Verificación |
|---|---|---|---|
| **Corpus** | el 70% ya está en 198.1 (SHA `66255f1d`) | **NO** | la cadena ya lo contenía |
| **CNO-IV-001** | la cadena jurídica es idéntica | **NO** → sigue `v1.0 vigente` | ✅ **prueba la separación**: un umbral no toca el Derecho |
| **RO-IV-001** | `v1.0` (65) → `v1.1` (70); v1.0 pasa a `obsoleta` | **SÍ** (solo el dígito M · §4) | nace `propuesta` → validación humana → `vigente` |
| **Compilación** | recompila RO v1.1 → **artefacto firmado** nuevo (build+SHA) | **SÍ** | determinista·reproducible·idempotente (ADR-039) |
| **Gold Master** | recibe umbral 70 por config compilada; **no consulta** la BRN | **SÍ** (H24: 65→70) | Regla 1 intacta — el motor no se edita, se reconfigura |
| **SAT-IV-001** | recomputa con 70; su definición no cambia | **NO** (sigue → RO-IV-001) | la SAT no conoce el número; lo hereda de la RO |
| **DOM d02** | muestra 70 como umbral | **NO** (código) | lee el umbral de la config, no lo hardcodea |

**Intervenciones humanas: una** (validar RO v1.1). **Código tocado: cero.** **Gold Master editado a
mano: no** (se reconfigura por compilación). → **La arquitectura soporta el cambio de umbral.** ✅

## Caso B — cambia la CADENA (reforma agrega un artículo), la lógica puede o no cambiar
**Disparo simulado (artículo ficticio):** una reforma futura agrega el `Art. 198.7 — excepción por
emergencia` a la cadena de la regla.

| Paso | Qué ocurre | ¿Cambia? | Verificación |
|---|---|---|---|
| **Corpus** | ingresa el texto del 198.7 con su **SHA** nuevo | **SÍ** | sin SHA no entra (Regla 3) |
| **CNO-IV-001** | se agrega el eslabón; `v1.0` → `v2.0`; v1.0 archivada | **SÍ** (dígito N · nueva cadena) | el MDN señala la CNO afectada automáticamente |
| **RO-IV-001** | si el 198.7 **no** cambia variable/umbral → la RO **re-apunta** al SHA, no versiona; si introduce una excepción operativa → `v1.1` | **depende** | decisión de la **validación humana**, no de la IA |
| **Compilación → Gold Master → SAT → DOM** | igual que el Caso A **solo si** la RO cambió | condicional | si la RO no cambió, el motor no se recompila |

**Prueba clave:** agregar Derecho a la cadena **no obliga** a recompilar el motor. Solo se propaga
aguas abajo si la **lógica** (la RO) cambió. → **La arquitectura separa correctamente los dos ejes.** ✅

---

## Resultado del ejercicio
- **Ninguna duda estructural apareció.** Los dos ejes de cambio (umbral vs. cadena) se propagan por
  caminos distintos, con **una sola** intervención humana y **sin editar el motor a mano**.
- **Se confirma la separación CNO/RO** (ADR-038 §108): el Caso A no tocó la CNO; el Caso B no obligó
  a tocar la RO. La lógica de negocio no se dispersa.
- **Se confirma la Regla 1**: en ambos casos el Gold Master se **reconfigura por compilación**, nunca
  se edita ni consulta la BRN en runtime.
- **Se confirma el ciclo de liberación §5b**: el artefacto firmado es la única bisagra hacia el motor.

**Conclusión.** La BRN v2 soporta un cambio normativo real. Concluye la fase de **diseño**; procede la
de **implementación incremental** — empezando por el compilador RO→Gold Master (ADR-039), cuando Javo
lo disponga. Cualquier cambio de fondo, de aquí en más, se justifica en un ADR.

---
*Reforma Simulada · CNO-IV-001 · Dylus Lab © 2026 · "Probamos la gobernanza antes que el motor: la arquitectura movió un umbral y agregó un artículo sin tocar una línea de código ni el Gold Master. Está lista para ejecutar, no solo para leerse."*
