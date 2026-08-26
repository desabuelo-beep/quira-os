---
authority:
  parent: GOVERNANCE-001
  type: REGISTRO
estado: ABIERTO — inventario cerrado, decisiones pendientes
fecha: 2026-08-25
---

# Autoridad de las proposiciones de BOOT — inventario, no poda

> **Este registro NO decide nada.** Reúne la evidencia para que la decisión de gobernanza tenga
> sobre qué decidirse. Ninguna de sus filas autoriza a mover una línea de `governance/BOOT.md`.

*(Sin `constitution_articles`: la propia Constitución declara dos numeraciones incompatibles
—Art. 0-30 y Art. 1-21, siendo la B la oficial y la otra derogada— y no verifiqué cuál cubre este
registro. No se citan artículos que no se comprobaron.)*

## Por qué existe

Depurando `§AHORA` apareció algo que no era un problema de tamaño. El colega lo formuló así:

> *«La compresión anterior no sólo había eliminado información; en algunos puntos había comprimido
> la relación entre una proposición y su autoridad hasta hacer parecer que una autoridad decía algo
> que nunca dijo.»*

Y el principio que ordena todo lo demás:

> **BOOT no debe decidir qué es canon. BOOT sólo debe reflejar el canon que ya ha sido decidido.**

## El procedimiento, que no debe saltarse

    proposición → evidencia → hogar → autoridad → cobertura → estado → decisión → recién entonces poda

Con tres estados posibles, y sólo tres:

| | |
|---|---|
| **A** | recuperable con autoridad válida — BOOT puede apuntar a ella |
| **B** | existe pero carece de autoridad suficiente — no se poda; requiere gobernanza |
| **C** | no existe como norma viva — **no se inventa autoridad**; queda candidata |

## El inventario

| # | proposición | naturaleza | estado | evidencia verificada |
|---|---|---|---|---|
| 1 | «NO es auditoría ni observatorio» | identidad + guard conceptual | **conflicto activo** | ver §1 |
| 2 | SIAP → QUADRUM → QUIRA | genealogía | memoria histórica | testimonio Javo 2026-08-25 |
| 3 | «define el OBJETO, no a QUIRA» | meta-regla ontológica | **C** | sólo en BOOT |
| 4 | Seccionales 29-NOV-2026 | estado estratégico temporal | §AHORA | testimonio Javo 2026-08-25 |
| 5 | «no congelar teoría antes que el grafo hable» | regla metodológica | **B — degradada** | ver §5 |
| 6 | «Inventario de Conceptos → DERIVA» | regla de procedimiento | **B** | ver §6 |
| F | F1/F2/F3 | taxonomía de fases | **C** | ver §F |

## §1 · El caso más delicado: divergencia entre capas de autoridad

**No es que falte una frase en la Constitución. Es que dos capas se contradicen.**

    governance/GOVERNANCE_CHARTER.md:176    «QUIRA ES un Observatorio Nacional…»
    governance/HOJA_DE_RUTA_MAESTRA.md:23   «QUIRA ES un OBSERVATORIO NACIONAL…»  (Javo · 2026-06-12)
    governance/BOOT.md                      «⛔ NO es auditoría ni observatorio»   (Javo · 2026-08-05)

La corrección de agosto **nunca bajó a los artefactos de junio**. Javo (2026-08-25):

> *«Es para que Claude, cuando construye, no siga degradando a QUIRA a una simple auditoría o al
> observatorio, como ha propagado en muchos documentos.»*

Tenía razón, y la causa es material: un constructor que lee `governance/` encuentra **escrito** que
QUIRA es un observatorio. No lo inventa — lo lee.

**Pero la proposición NO es canon inexistente: ya se ejecuta.**

    views/login_view.py:555          «QUIRA es una infraestructura de conocimiento verificable
                                      para la gestión pública territorial»   ← el landing
    app/viz/render/plan_render.py:836  la atribuye a CONSTITUCION-001
    scripts/ci/check_epistemico.py:79  detector: «no auditoría (CONSTITUCION-001)»

El código **ya la trata como norma constitucional**; lo que falta es que el texto de la Constitución
la contenga. Dato para la decisión: `check_epistemico.py` **detecta pero no bloquea, y no está
enganchado a CI** — hoy depende de que alguien lo corra a mano.

## §5 · No es huérfana: es canon perdido en una reescritura

Tuvo rango, y consta:

    governance/historico/BOOT_2026-06-17.md        Regla de Oro #4
    governance/historico/QUIRA_STATE_2026-06-03.md Regla #6

Desapareció cuando `CLAUDE.md` reescribió las nueve. **Restaurar canon perdido y crear canon nuevo
no son la misma decisión** ni requieren la misma autoridad.

**ADR-019 no es su fuente: es su caso de aplicación.** El texto original decía *«ADR-019 a propósito
en SUPPORTED»*; el ADR sigue hoy en `STRONGLY_SUPPORTED`, mantenido sin confirmar como demostración
viva de la regla. Al comprimirse, el paréntesis pasó a leerse como atribución de autoría.

## §6 · Artefacto autorizado ≠ regla que ordena usarlo

`marco_teorico/INVENTARIO_CONCEPTOS_FUNDACIONALES.md` — `INVENTARIO-CONCEPTOS-001`, `status:
vigente`, autoridad `MARCO-TEORICO-001`, 13.651 b. **BOOT lo referencia 0 veces.**

La regla «consultarlo antes de definir» no está ni en él ni en `CLAUDE.md`. Son **dos objetos
normativos distintos**: el artefacto tiene autoridad; la regla que obliga a consultarlo, no.

Restricción medida para esa decisión: **`CLAUDE.md` está en 3944 / 4000 bytes.** La vía «meterla
entre las Reglas de Oro» está cerrada hoy sin podar `CLAUDE.md` primero.

## §F · Aquí BOOT fabrica canon

BOOT dice *«**ADR-041 (sellado)**: F1 = Observatorio · Ciudadana · F2 = … · F3 = Economic»*.

    docs/adr/ADR-041   APROBADO, sellado por Javo, parent CONSTITUCION-001  →  F1/F2/F3: 0
    docs/adr/ADR-043   APROBADO, sellado por Javo, parent ADR-041           →  F1/F2/F3: 0

Los **productos** tienen canon sellado. Su **agrupación en tres fases** sólo existe en
`docs/QUIRA_DOCTRINE_v1.md`, que **no tiene frontmatter de autoridad**. BOOT le presta el sello de
un ADR que no la contiene.

⛔ Que los productos estén aprobados **no arrastra** la taxonomía de fases.

## Lo que esta ronda enseñó, y conviene no repetir

| error | cómo se manifestó |
|---|---|
| identificador ≠ contenido | 4 proposiciones «tenían destino»; el destino sólo tenía la etiqueta |
| coincidencia textual ≠ recuperación | «elecciones» apareció… hablando del 17-ago-2025, otro contexto |
| búsqueda literal → falso negativo | dije que ADR-023 no decía «recalcular»; sí lo dice |
| **inferir una negación** | de «era el Diplomado CAF» concluí que las elecciones no existían, y **borré un dato correcto**. La ausencia de confirmación no autoriza a concluir la negación |

Ese último es el más grave, porque es el error que QUIRA persigue afuera, cometido adentro y sobre
el testimonio del propio fundador.

## Decisiones pendientes — ninguna la toma este registro

1. ¿La corrección de agosto (#1) baja a `GOVERNANCE_CHARTER` y `HOJA_DE_RUTA_MAESTRA`? Son
   **congelados** (Regla 5): requiere aprobación explícita.
2. ¿#1 se escribe en la Constitución que el código ya cita?
3. ¿`check_epistemico` pasa de detector a gate de CI?
4. ¿#5 se **restaura** como Regla de Oro, o se eleva a ADR propio?
5. ¿#6 se convierte en regla, o basta con que BOOT apunte al artefacto vigente?
6. ¿La taxonomía F1/F2/F3 se lleva a ADR-041/043, o BOOT deja de atribuírsela?
7. ¿Dónde vive la genealogía (#2) y la meta-regla ontológica (#3)?

**Hasta que se resuelvan, `§AHORA` no debe podarse más.** Con 564 bytes de margen el espacio dejó
de ser el problema; la integridad de autoridad no.

---
*Registro de autoridad · Dylus Lab © 2026 · reúne evidencia, no decide canon.*
