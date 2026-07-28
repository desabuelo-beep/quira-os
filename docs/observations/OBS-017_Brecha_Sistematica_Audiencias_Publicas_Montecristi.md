---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-017 · Brecha sistemática entre cumplimiento narrado y documental — Audiencias Públicas (MCR)

**Fecha:** 2026-07-24 · **Dominio:** d08 (Participación Ciudadana) · **Mecanismo:** Audiencia
Pública (CNO-VIII-004). **Primer hallazgo EMPÍRICO de d08** — medido sobre evidencia real, no
inferido. Hipótesis planteada por el asesor externo; verificada determinísticamente.

## Hipótesis (asesor · 2026-07-24)
> ¿Existe una brecha sistemática entre el **cumplimiento narrado** (el acta declara cumplir la
> ley) y el **cumplimiento documental** (el instrumento resolutivo que la ley exige)?

## Fuente oficial de la evidencia (Javo · 2026-07-24) — refuerza el hallazgo
Estos documentos NO son una carpeta suelta: son el **medio de verificación oficial que el propio
GAD declara** en su Informe de Rendición de Cuentas anual (CPCCS), sección **"Mecanismos de
Participación Ciudadana"**. Esa sección declara, por año:

| Mecanismo | ¿Cumplió? (dice el GAD) | Link de verificación (montecristi.gob.ec) |
|---|---|---|
| Asamblea Local | SÍ | `cloud.montecristi.gob.ec/…/EjFCAgyasTiWZ4e` |
| Audiencia Pública | SÍ | `…/yKbMxSdB49GxexE` → **las 28 actas de este hallazgo** |
| Cabildo Popular | SÍ | `…/4qgix3o9c4X94DT` |
| Consejo de Planificación Local | SÍ | `…/n6AeGJLpXpB2Kry` |
| Otros | NO | No aplica |

**NO existe otra evidencia** (confirmado por Javo). Por tanto el contraste es directo y potente:
el GAD **declara "SÍ cumplió"** la audiencia pública en su RDC, y el link que él mismo aporta como
prueba lleva a 28 actas que acreditan la REALIZACIÓN pero **no la formalización resolutiva** que
la ley exige. Es la brecha entre *lo declarado* (d09/RDC) y *lo verificable* (d08) — el núcleo de
lo que QUIRA demuestra. La sección Mecanismos del informe RDC es el **puente estructural d09↔d08**.

## Método (determinístico · sin IA · reproducible)
Sobre las **28 actas** de audiencia pública 2023-2025 (extraídas a texto por Javo, incluidas las
16 que estaban escaneadas), búsqueda de patrones:
- cita de la norma: `art[íi]culos? 73-75` / `Ley Orgánica de Participación` / `LOPC`
- resolución formal: `\bresuelve\b` / `Resolución (Legislativa) Nro` (el formato resolutivo que
  sí aparece, p. ej., en las resoluciones del Concejo o del Consejo de Planificación)
- presidencia: mención de `alcalde` · delegación: `delega` / `en representación del alcalde`

Script: `scratchpad/analisis_audiencias.py` (reproducible).

## Resultado
| Señal | Resultado |
|---|---|
| Actas que citan la LOPC (Arts. 73-75) | **28 / 28 (100%)** |
| Actas con RESOLUCIÓN formal | **0 / 28 (0%)** |
| **Patrón del hallazgo** (cita la norma, acta simple sin resolución) | **28 / 28 (100%)** |
| Alcalde presente/mencionado | 28 / 28 |
| Delegación explícita | 0 / 28 |

## Hallazgo — redacción canónica (precisión del asesor · 2026-07-24)
La formulación EXACTA que QUIRA emite, ni un grado más:

> **"En la evidencia documental oficial utilizada por el propio GAD para acreditar las
> Audiencias Públicas (28 actas analizadas, período 2023-2025), no consta un acto resolutivo
> identificable conforme al Art. 75 de la LOPC."**

### Las TRES cosas que QUIRA distingue (y no confunde jamás)
| Nivel | Qué es | ¿QUIRA lo afirma? |
|---|---|---|
| **Ausencia documental** | no consta el documento en la evidencia oficial disponible | **SÍ** — es lo único que QUIRA certifica aquí |
| **Ausencia jurídica** | el acto no existe en Derecho | **NO** — exige más que no hallar el documento |
| **Incumplimiento** | juicio de que se violó la norma, con consecuencia | **NO** — lo determina el CPCCS/Contraloría |

QUIRA se detiene en el primer nivel. Que las 28 actas inviten el Art. 75 y no contengan la
resolución es **ausencia documental verificada** — no "el GAD incumple". La consecuencia
normativa (COOTAD 312) existe en la Ley y se cita como contexto, pero **QUIRA no la aplica**.

El fenómeno, en lenguaje de administración pública: la audiencia se realiza y se documenta como
acta, pero **en la evidencia oficial no se acredita su formalización resolutiva** — el acto
consta en su fase deliberativa, no en la resolutiva que la ley prevé.

## Contraste que refuerza la verificabilidad (dentro del mismo dominio)
El Consejo de Planificación (CNO-VIII-003) **sí** produce su resolución (COPLAFIP 29 — consta en
la carpeta). Mismo GAD, misma exigencia de formalización resolutiva, cumplida en un mecanismo
(Consejo) y **sistemáticamente ausente en otro** (Audiencia). El contraste es objetivo, no
interpretativo.

## Estructura del hallazgo: 017A y 017B (asesor · 2026-07-27)

El hallazgo se desdobla en dos observaciones de naturaleza distinta:

### OBS-017A · Presidencia de las audiencias
> La documentación disponible **no permite acreditar de forma suficiente quién ejerció
> formalmente la presidencia** de cada audiencia. La actuación se infiere de la narración del
> acta, no de una fórmula de constitución del acto.

### OBS-017B · Habilitación de la autoridad actuante *(el más fuerte jurídicamente)*
> **No fue posible acreditar documentalmente la habilitación jurídica de la autoridad que
> presidió las audiencias públicas cuando la conducción no correspondió directamente al alcalde.
> El corpus documental analizado no incorpora actos administrativos de delegación, resoluciones
> u otros instrumentos que permitan reconstruir la cadena de legitimación institucional de quien
> dirigió dichas actuaciones.**

017B es más robusto que 017A porque **no depende de interpretar el lenguaje del acta**: depende
de verificar la existencia (o inexistencia) del acto habilitante. Cadena rota:

```
Audiencia Pública → ¿quién dirigió? → ¿con qué competencia?
                                   → ¿dónde está el acto administrativo? → NO CONSTA
```

### ★ PRECISIÓN DE JAVO — la ausencia de habilitación NO anula la evaluación
> *"Aunque no exista la delegación, con todo hay que medir y evaluar la cadena de la audiencia
> pública para determinar los hallazgos y el cumplimiento."*

**Corrige una lectura posible del hallazgo.** La falta del acto habilitante es **un hallazgo
puntual, no un anulador del mecanismo**: la audiencia se realizó, recogió demandas y generó
compromisos — todo eso es evidencia real que debe medirse. Poner el mecanismo en cero por una
brecha documental sería **castigar la evidencia en lugar de medirla**, y perdería información
sustantiva sobre la participación efectiva.

Por eso la cadena de la audiencia se evalúa **criterio por criterio, con estados independientes**
(RO-VIII-001): convocatoria · habilitación de la instancia · realización · presidencia acreditada
· habilitación del actuante · resolución de cierre · demandas recogidas · compromisos asumidos.
Cada uno reporta su propio estado; ninguno cancela a los demás.

## Sobre la delegación (COOTAD 60) — CORREGIDO 2026-07-27

**Corrección de una afirmación mal fundada.** Una versión anterior de este OBS afirmaba
*"delegación NO aplica: el alcalde está presente en las 28"*. Esa conclusión se infirió de que la
palabra «alcalde» aparecía en el texto — **que se mencione no significa que presida**. Javo
(15 años en gestión de GAD) advirtió que en la práctica muchas audiencias las dirigen delegados.

Re-verificación sobre las 28 actas:

| Señal | Resultado |
|---|---|
| Actas que registran una delegación explícita | **1 / 28** — y es delegación de TAREA (*"delego al Ing. Rómulo Santana para que inicie y lleve adelante…"*), no de presidencia |
| Actas donde el alcalde actúa directamente (bienvenida, interviene) | 23 / 28 |
| Expedientes que **acreditan formalmente la autoridad que presidió y su habilitación** | **0 / 28** |

> **Principio de No-Inferencia (Carta Art. 4.5).** «0/28» significa exactamente que *la
> documentación analizada no acredita formalmente la presidencia ni la habilitación*. **NO**
> significa «nadie presidió», ni «no presidió el alcalde», ni «presidió un delegado». La fuerza
> del hallazgo está en no inferir: QUIRA mide la capacidad del expediente para probar la
> legalidad del acto, no lo que ocurrió en la sala.

**Hallazgo corregido:** el problema no es que falte un acto de delegación puntual, sino que
**ninguna acta acredita quién presidió la audiencia ni bajo qué habilitación** (LOPC 73 exige que
la instancia esté *habilitada por la autoridad responsable*; COOTAD 60 regula la delegación). La
actuación del alcalde se infiere de la narración, no de una fórmula de constitución del acto.

**Consecuencia institucional (aporte de Javo):** si un delegado dirige la audiencia sin acto de
delegación que lo habilite, los acuerdos y compromisos asumidos allí **carecen de respaldo
institucional vinculante**. Se registra como verificabilidad, no como juicio de legalidad.

## Hallazgo cruzado d08 ↔ d07 (aporte de Javo · 2026-07-27)
Estos documentos se reportan como **instancias y mecanismos de participación EJECUTADOS** en los
informes de RDC que el GAD sube anualmente al portal del CPCCS — pero **no figuran en
transparencia activa** (d07). Es decir: la misma evidencia existe en el circuito de control
social (d09) y está ausente del circuito de transparencia (d07).

**Pendiente de verificación en d07** (no se afirma aún): confirmar si estos mecanismos deben
publicarse en transparencia activa y, de ser así, registrar la ausencia como hallazgo de ese
dominio. Se anota aquí para no perder la pista; la verificación corresponde a d07.

## Límites del método (honestidad)
- Es búsqueda de texto: detecta la resolución **en los documentos del medio de verificación
  oficial**. Como el GAD declara estos documentos como su prueba en la RDC y NO existe otra
  evidencia (Javo), el hallazgo es sólido: "no consta en la evidencia que el propio GAD designa
  como verificación". No es "falta buscar en otro lado".
- La presencia del alcalde se infiere de la mención; el acta no siempre formaliza quién preside.

## Valor para QUIRA
Este es el tipo de hallazgo que justifica el dominio: no un número del motor, sino una **brecha
verificable documentalmente** entre lo que la gestión declara (cumple la ley de participación) y
lo que la evidencia sostiene (no produce el instrumento resolutivo). Alimenta RO-VIII-001
(integridad normativa) del mecanismo audiencia con estado **acreditación PARCIAL** (el acto se
realiza; su formalización no consta), en las 28 del período.

---
*OBS-017 · Dylus Lab © 2026 · el primer hallazgo empírico de d08: la evidencia habla, QUIRA la escucha.*
