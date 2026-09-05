# QUIRA · MAPA MAESTRO DE FRENTES

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/mapa_maestro.py`. El **estado** sale de las fuentes vivas (`deuda.py`, `doctrina.py`, `docs/pcd/`, `tests/`); la **secuencia y las dependencias** se declaran en el script, porque son un juicio de dirección y no un dato.

> ### Por qué existe
> Javo: *«hay varios frentes […] para que no nos pase nuevamente volver a hacer refactor porque no recordamos»*. No había un artefacto que dijera qué frentes hay, en qué orden y qué depende de qué: vivía en la cabeza del director y disperso en cinco documentos.
>
> Es la misma deuda que esta auditoría persigue en todo lo demás —conocimiento que existe en el diseño y no en algo verificable— con un agravante: **de éste dependía no repetir trabajo.**

## Qué está corrigiendo este refactor · RESTAURAR vs. CREAR

Javo: *«tenemos la tesis, y todo el constructo metodológico allí claro […] eso es lo que estamos corrigiendo con este refactor»*. Es cierto en lo esencial, **y hay un matiz operativo**: no todo lo que el refactor toca estaba en la tesis.

### 🔵 RESTAURAR — la tesis tenía la respuesta y la implementación la perdió

| | La tesis decía | El motor hizo |
|---|---|---|
| `P_i` | antídoto anti-gaming, explicado | correcto — la auditoría lo dudó y la tesis la corrigió |
| `E_i` | regla con `COOTAD 54 · NCI 200-04` | valores que no la siguen |
| AVEP | «Baremo de **Interpretación**» | fórmula `IF` copiada en 11 hojas |
| universo | «muestra **estratégica**» | rotulado `Total_Metas_PDOT` |
| nombre | `SIAP` integridad ⊃ `ICPI` congruencia | se perdió la jerarquía |
| `V_i` | regla de tres niveles con núcleo | documentada, **no implementada** |

### 🟠 CREAR — la tesis NO tiene la respuesta, y hay que decidirla

| | Por qué no está en la tesis |
|---|---|
| Criterio de selección de las 25 | lo declaró Javo en 2026-09-03, no el documento |
| **Qué es `i`** (`011-A`) | la tesis habla de metas; no resuelve la unidad documental que contiene tres |
| Umbrales de AVEP | ni la tesis ni ninguna norma los fundamenta |
| Transferibilidad LATAM (`010`) | no era pregunta de una tesis sobre Montecristi |
| Capas de presentación (`DOC-014`) | no existía el producto cuando se escribió |
| Arquitectura de dominios (`T3-R`) | posterior a la tesis |

⚠️ **La distinción es operativa, no filosófica.** Buscar en la tesis una respuesta que no está lleva a inventarla; decidir por cuenta propia algo que la tesis ya resolvió rompe la genealogía. Esta auditoría cometió los dos errores —dudó de `P_i`, que la tesis explicaba; y declaró `UNTRACEABLE` a `E_i`, cuya regla la tesis define—.

> **Antes de decidir cualquier punto del refactor: ¿esto lo resuelve la tesis?** Si sí, se restaura y se cita. Si no, se decide **y se declara que es una decisión nueva**, no un hallazgo.

## Los cinco frentes

| Frente | Qué pregunta responde | Depende de | ¿Puede avanzar ahora? |
|---|---|---|---|
| **GM-Ω** · Auditoría del motor ICPI | ¿el indicador mide lo que dice medir, y su matemática está fundamentada? | — | sí · es la vía crítica |
| **TF** · Terminology Freeze | ¿qué es cada nombre, quién lo define y en qué capa se lee? | — | sí · independiente de GM-Ω |
| **T3-R** · Refactor de arquitectura de dominios | ¿la estructura de dominios representa lo que QUIRA sabe hoy? | TF · T3 | R0 y R1 sí · R2 espera a 011 |
| **2ING** · Segunda ingeniería · curación dominio a dominio | ¿cada dominio está curado de la fuente a la UI, por las 7 capas? | — | sí · y alimenta a TF y a T3-R |
| **DEUDA** · Registro de deudas con ataque | ¿qué sabemos que está mal y aún no se ha corregido? | — | sí · cada una a su ritmo |

## El orden, y qué se puede hacer en paralelo

```
  LA RUTA AL DICTAMEN — acordada 2026-09-05, saneamiento ontológico primero

  011-C2  ✅ semántica de los factores      qué mide cada letra
     ↓
  011-C3     justificación                 por qué cambió · quién · cuándo
     ↓
  010        transferibilidad LATAM        qué parte del constructo es local
     ↓
  011-C4     DICTAMEN                      ¿es NECESARIA la multiplicatividad?

  EN PARALELO — nada de esto se bloquea entre sí
  ├── GM-Ω 008-R resolver las 40 ambiguas · 66↔25  ← desbloquea v2
  ├── GM-Ω 011-A2 declarar la unidad `i` en el canon
  ├── T3-R R0    diagnóstico de los 13 dominios
  ├── T3-R R1    modelos A · B · C de arquitectura de dominios
  ├── 2ING d07   curación de Transparencia
  └── DEUDA      D-008 · D-009 · D-011 · D-012 · D-013 · D-014

           ↓ y sólo tras el dictamen

  ├── T3-R R2    residencia y ámbito de los índices
  ├── TF   T5    presentación dentro del dominio
  └── TF   T6    conservar / renombrar / deprecar / eliminar
```

⚠️ **Por qué `010` va DESPUÉS de `C3` y no antes.** Esta dirección proponía adelantarla —la transferibilidad también alimenta al dictamen—. El criterio que prevaleció es el del colega y es mejor: **mientras no se sepa qué significan `E_i` y `C_i`, todo análisis se hace sobre variables cuya ontología seguimos reconstruyendo**. `011-C2` lo demostró en el acto: la semántica que se daba por buena era falsa.

⚠️ **`011-A2` y `011-B` siguen abiertas y la ruta acordada las pospone.** No es un olvido: `A` tiene su genealogía resuelta y sólo falta declararla en el canon, y `B` —la correspondencia documental ↔ operacional— depende de `008-R`. Ninguna bloquea a `C3`. Pero **`C4` sigue necesitándolas**, así que no desaparecen del camino.

⚠️ **`R0` y `R1` NO dependen de `011`** —esta dirección lo tuvo mal y se corrigió—: son diagnóstico y **lo alimentan**. Sólo `R2` espera, porque mover un indicador cuyo constructo está en dictamen sería reorganizar la casa antes de saber qué se guarda.

Y **`T6` espera a `011` por la misma razón**: deprecar `AVEP` o migrar el nombre del `ICPI` son decisiones que dependen de qué resulte que mide el constructo.

## Estado por etapa

✅ cerrada · 🔄 en curso · ⬜ abierta, sin bloqueo · ⛔ bloqueada

| Frente | Etapa | Título | Estado | Nota |
|---|---|---|:-:|---|
| GM-Ω | `001` | Identidad y árbol matemático | ✅ |  |
| GM-Ω | `002` | El veto de la obra sobre la norma | ✅ |  |
| GM-Ω | `003` | Reconstrucción de la fórmula | ✅ |  |
| GM-Ω | `004` | Matriz de procedencia · 150 celdas | ✅ |  |
| GM-Ω | `005` | Temporalidad y determinabilidad | ✅ |  |
| GM-Ω | `006` | Semántica del cero | ✅ |  |
| GM-Ω | `007` | Sensibilidad A·B·C·D·X + X-bis | ✅ |  |
| GM-Ω | `008` | Cobertura real del universo medido | ✅ | veredicto: JUSTIFICADA EN v1 · criterio = mayor monto (Javo) |
| GM-Ω | `008-R` | Reconciliación meta a meta 66 ↔ 25 | 🔄 | PARCIAL · caso N:1 demostrado · correspondencia exhaustiva sin reconciliar |
| GM-Ω | `v2` | Universo completo del PDOT (66) — decisión de Javo | ⛔ | 011 · 008-R · exige ADR propio y recalibración (ADR-036 §4) |
| GM-Ω | `009` | ¿Se puede optimizar el índice sin mejorar la realidad? | ✅ | ★ superficie de incentivo DINÁMICA: la ventaja material domina mientras hay margen y puede invertirse al cierre |
| GM-Ω | `010` | Transferibilidad LATAM · núcleo vs adaptador | ⬜ |  |
| GM-Ω | `007-B0` | Genealogía del constructo · unidad `i` · factores | ✅ | ★ reescrito con toda la evidencia · CERRADO como reconstrucción, NO como validación |
| GM-Ω | `011-A` | Unidad de análisis · ¿qué es `i`? | 🔄 | ★ genealogía RESUELTA: era PROMESA CNE → META PDOT «pues era mandato» (Javo) · falta DECLARARLA en el canon |
| GM-Ω | `011-B` | Regla de correspondencia PDOT → ICPI (1:1·N:1·1:N·N:N) | ⛔ | 011-A |
| GM-Ω | `011-C1` | Genealogía algebraica · P·R·V·T → +E → +C · escalas | ⬜ | ★ 007-B0 la dejó reconstruida |
| GM-Ω | `011-C2` | Genealogía semántica · qué significó cada factor | ✅ | ★ C_i mide LEGALIDAD del proceso, no entrega · E_i y C_i comparten escala sin ser la misma · 4 divergencias latentes |
| GM-Ω | `011-C3` | Justificación de cada transformación · qué·por qué·quién·cuándo | ⬜ | 9 preguntas heredadas de C2 · sin fuente documental → NO DETERMINABLE, no explicación inventada |
| GM-Ω | `011-C4` | ¿Es la multiplicatividad NECESARIA al constructo, o una arquitectura elegida y conservada? | ⛔ | ⚠️ faltan A · B · C1 · C3 · 010 — y C2 la reformuló: la pregunta ya no es sólo si el producto es correcto, sino sobre cuántas dimensiones REALMENTE independientes opera |
| TF | `T1` | Inventario de nombres propios | ✅ |  |
| TF | `T2` | Clasificación ontológica + capa de presentación | ✅ |  |
| TF | `T3` | Contrato índice → dominio → rol → pregunta → capa | 🔄 | se llena con la curación de cada dominio |
| TF | `T4` | Rol de cada indicador | 🔄 | sin inventar: sólo con fuente |
| TF | `T5` | Presentación dentro de su dominio | ⛔ | T3 · T4 |
| TF | `T6` | Acción: conservar / renombrar / deprecar / eliminar | ⛔ | 011 · T5 |
| T3-R | `R0` | Diagnóstico de los 13 dominios | ⬜ |  |
| T3-R | `R1` | Modelos A · B · C de arquitectura | ⬜ |  |
| T3-R | `R2` | Decisión: residencia y ámbito de los índices | ⛔ | 011 |
| 2ING | `d01` | Planificación | ✅ | ⚠️ PCD bajo canon anterior |
| 2ING | `d06` | Salud Institucional | ✅ | ⚠️ PCD bajo canon anterior |
| 2ING | `d09` | Rendición de Cuentas | ✅ | ⚠️ PCD bajo canon anterior |
| 2ING | `d07` | Transparencia | 🔄 |  |
| 2ING | `d08` | Participación Ciudadana | ⬜ | entrable |
| 2ING | `d02·d03` | Presupuesto · Gobernanza del Mandato | ⬜ |  |
| 2ING | `d04·d05·d10-d13` | Sellados · sin construir | ⬜ |  |

**16 de 35 etapas cerradas.**

## Estado derivado de las fuentes vivas

| | |
|---|---:|
| Deudas declaradas | 14 |
| Deudas resueltas | 6 |
| Deudas abiertas | **8** |
| Reglas de doctrina con custodio | 25 |
| Pruebas que las fijan | 403 |
| Documentos GM-Ω | 11 |

### Deudas abiertas

| Deuda | Estado |
|---|---|
| `D-001` | ABIERTA |
| `D-008` | ABIERTA |
| `D-014` | ABIERTA |
| `D-013` | ABIERTA |
| `D-012` | ABIERTA |
| `D-011` | ABIERTA |
| `D-010` | ABIERTA |
| `D-009` | EN CURACIÓN · las 4 superficies del IGP curadas 2026-09-03. La cura NO fue cambiar 27,98 por 27,00: el motor e |

### Documentos de la auditoría

- [`GM-OMEGA_CONTRATO_INDICE_DOMINIO.md`](GM-OMEGA_CONTRATO_INDICE_DOMINIO.md)
- [`GM-OMEGA_GENEALOGIA_DOCUMENTAL.md`](GM-OMEGA_GENEALOGIA_DOCUMENTAL.md)
- [`GM-OMEGA_ICPI_COBERTURA_008.md`](GM-OMEGA_ICPI_COBERTURA_008.md)
- [`GM-OMEGA_ICPI_FICHA_FORENSE.md`](GM-OMEGA_ICPI_FICHA_FORENSE.md)
- [`GM-OMEGA_ICPI_GAMING_009.md`](GM-OMEGA_ICPI_GAMING_009.md)
- [`GM-OMEGA_ICPI_MATRIZ_004.md`](GM-OMEGA_ICPI_MATRIZ_004.md)
- [`GM-OMEGA_ICPI_RECONCILIACION_008R.md`](GM-OMEGA_ICPI_RECONCILIACION_008R.md)
- [`GM-OMEGA_ICPI_SEMANTICA_011C2.md`](GM-OMEGA_ICPI_SEMANTICA_011C2.md)
- [`GM-OMEGA_ICPI_SENSIBILIDAD_007.md`](GM-OMEGA_ICPI_SENSIBILIDAD_007.md)
- [`GM-OMEGA_MAPA_MAESTRO.md`](GM-OMEGA_MAPA_MAESTRO.md)
- [`GM-OMEGA_TERMINOLOGIA_T1-T2.md`](GM-OMEGA_TERMINOLOGIA_T1-T2.md)

## Las tres reglas que sostienen este mapa

1. **Ningún frente se cierra sin custodio.** Una etapa marcada `✅` sin prueba que la fije acredita cero por no existir — es el defecto que `D-004` documentó en el propio CI.
2. **Un frente bloqueado no es un frente parado.** `011` está bloqueada por `008-010`, y esos tres pueden trabajarse hoy. La secuencia existe para ordenar, no para esperar.
3. **Este mapa se deriva.** El día que alguien lo edite a mano, dejará de reflejar el estado real sin que nada avise, y volveremos exactamente al punto que motivó escribirlo.

---
*QUIRA · Mapa Maestro · 16/35 etapas cerradas · 8 deudas abiertas · Dylus Lab © 2026*
