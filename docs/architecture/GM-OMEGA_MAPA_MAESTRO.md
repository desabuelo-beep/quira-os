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

## Los 6 frentes

| Frente | Qué pregunta responde | Depende de | ¿Puede avanzar ahora? |
|---|---|---|---|
| **GM-Ω** · Auditoría del motor ICPI | ¿el indicador mide lo que dice medir, y su matemática está fundamentada? | — | sí · es la vía crítica |
| **TF** · Terminology Freeze | ¿qué es cada nombre, quién lo define y en qué capa se lee? | — | sí · independiente de GM-Ω |
| **T3-R** · Refactor de arquitectura de dominios | ¿la estructura de dominios representa lo que QUIRA sabe hoy? | TF · T3 | R0 y R1 sí · R2 espera a 011 |
| **2ING** · Segunda ingeniería · curación dominio a dominio | ¿cada dominio está curado de la fuente a la UI, por las 7 capas? | — | sí · y alimenta a TF y a T3-R |
| **DEUDA** · Registro de deudas con ataque | ¿qué sabemos que está mal y aún no se ha corregido? | — | sí · cada una a su ritmo |
| **QNEXT** · Rearquitectura integral · fondo y forma | ¿cómo evoluciona el ecosistema entero sin dañar lo que es válido? | 011-C4 para EJECUTAR | Q0 ✅ · Q1 sí · Q3 espera al dictamen |

## ★ Para qué sirve todo esto — el encuadre, fijado el 2026-09-05

Javo:

> *«Lo histórico no es la verdad absoluta o una camisa de fuerza que se deba continuar.»*

**Tiene razón, y el canon ya lo decía.** `DOC-013`: QUIRA no conserva conceptos por herencia, sólo los que cumplen una función verificable. Lo que ocurrió es que `GM-Ω` reconstruyó tanta genealogía que empezó a producir un **sesgo conservador de hecho**, aunque de derecho el canon dijera lo contrario.

### La corrección de encuadre

```
  reconstruir la historia   →   NO obliga a repetirla
                            →   habilita a decidir SABIENDO qué se cambia
```

Y de ahí sale la regla operativa (`DOC-027`):

> ### Un `NO DETERMINABLE` genealógico es un GRADO DE LIBERTAD, no una laguna
>
> Donde no hay razón documentada, **no hay nada que respetar**.

Aplicado a lo que `011-C2` y `C3` acaban de producir, el balance se invierte: no son hallazgos para conservar, son **permisos para cambiar**.

| Hallazgo | Lo que habilita |
|---|---|
| Dos generaciones de `C_i` conviven y el instrumento no declara cuál rige | **hay que elegir una** — no elegir también es una decisión, y hoy está tomada por omisión |
| La razón de la sustitución, los pesos y el piso: `NO DETERMINABLE` | **tres decisiones libres**, sin contradecir a nadie |
| La residencia del ICPI en `d06` se apoya en «Cumplimiento Institucional», nombre que el canon **ya retiró** | **la residencia está abierta**, y hay instrumento: la prueba de exportabilidad |

### ⚠️ La única camisa de fuerza real, y no es histórica

Hay una parte del constructo que **no puede rediseñarse libremente**, y conviene no confundirla con herencia:

| | Naturaleza | ¿Se puede cambiar? |
|---|---|---|
| `R_i` ↔ COOTAD 54-55 · Constitución 12, 14 | **anclaje normativo** | 🔴 sólo si cambia la norma |
| `V_i` ↔ LOTAIP 7 · LOSNCP 22 · NCI 410-11 | **anclaje normativo** | 🔴 sólo si cambia la norma |
| `T_i` ↔ COPFP 115-117 · Acuerdo 067 MEF | **anclaje normativo** | 🔴 sólo si cambia la norma |
| `P_i` ↔ COPFP 54 | **anclaje normativo** | 🔴 ídem |
| pesos de deducción · piso `0,50` · qué constructo de `C_i` rige | **decisión de diseño** | ✅ **libre** |
| residencia de cada índice en su dominio | **decisión de diseño** | ✅ **libre** |
| nombres de presentación | **decisión de diseño** | ✅ libre, con basónimo (`DOC-015`) |

> **Herencia histórica ≠ anclaje normativo.** Lo primero se revisa; lo segundo se acata. Confundirlos en cualquiera de las dos direcciones es el error: congelar por costumbre lo que se puede mejorar, o rediseñar por gusto lo que la ley fija.

### Qué NO cambia este encuadre

- **El Gold Master sigue congelado** hasta `011-C4`. Ampliar el alcance de lo que se puede decidir **no adelanta el momento de intervenir**.
- **La genealogía no se descarta**: es lo que permite distinguir herencia de anclaje. Sin `C2`/`C3` no sabríamos cuál de las dos generaciones de `C_i` estamos eligiendo.
- **`DOC-011` sigue vigente**: un vacío se clasifica por su naturaleza. Que un `NO DETERMINABLE` habilite a decidir no autoriza a **inventar** la razón que faltaba y presentarla como hallazgo.

## El orden, y qué se puede hacer en paralelo

```
  LA RUTA AL DICTAMEN — acordada 2026-09-05, saneamiento ontológico primero

  011-C2  ✅ semántica de los factores      qué mide cada letra
     ↓
  011-C3  ✅ justificación                  por qué cambió · quién · cuándo
     ↓
  010        transferibilidad LATAM        qué parte del constructo es local
     ↓
  011-C4     DICTAMEN                      ¿es NECESARIA la multiplicatividad?

  EN PARALELO — nada de esto se bloquea entre sí
  ├── GM-Ω 008-R resolver las 40 ambiguas · 66↔25  ← desbloquea v2
  ├── GM-Ω 011-A2 declarar la unidad `i` en el canon
  ├── QNEXT BM-01 corpus normativo: vigencia · clase · norma↔instrumento
  ├── QNEXT Q1   matriz de clasificación · candidato → ratificado
  ├── T3-R R0    diagnóstico de los 13 dominios  ← desbloquea Q2
  ├── T3-R R1    modelos A · B · C de arquitectura de dominios
  ├── 2ING d07   curación de Transparencia
  └── DEUDA      D-008 · D-009 · D-011 · D-012 · D-013 · D-014

           ↓ y sólo tras el dictamen

  ├── T3-R R2    residencia y ámbito de los índices
  ├── TF   T5    presentación dentro del dominio
  ├── TF   T6    conservar / renombrar / deprecar / eliminar
  └── QNEXT Q3   ejecución del refactor integral · fondo y forma
```

⚠️ **El refactor integral (`QNEXT`) no es un frente que se abra después de `GM-Ω`: es el destino que le da sentido.** Su plan —la carta `Q0`— ya está, y `Q1` puede correr hoy porque **clasificar no es cambiar**. Lo que espera al dictamen es la EJECUCIÓN. Detalle: `QUIRA-NEXT_CARTA_REARQUITECTURA.md`.

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
| GM-Ω | `010` | Transferibilidad LATAM · arquitectura vs contingencia | ✅ | ★ 24 componentes: 7 núcleo · 10 adaptador · 2 sedimentación · 5 contingentes · el núcleo es METODOLÓGICO, no métrico — y la multiplicatividad está en `D`, no en `A` |
| GM-Ω | `007-B0` | Genealogía del constructo · unidad `i` · factores | ✅ | ★ reescrito con toda la evidencia · CERRADO como reconstrucción, NO como validación |
| GM-Ω | `011-A` | Unidad de análisis · ¿qué es `i`? | 🔄 | ★ genealogía RESUELTA: era PROMESA CNE → META PDOT «pues era mandato» (Javo) · falta DECLARARLA en el canon |
| GM-Ω | `011-B` | Regla de correspondencia PDOT → ICPI (1:1·N:1·1:N·N:N) | ⛔ | 011-A |
| GM-Ω | `011-C1` | Genealogía algebraica · P·R·V·T → +E → +C · escalas | ⬜ | ★ 007-B0 la dejó reconstruida |
| GM-Ω | `011-C2` | Genealogía semántica · qué significó cada factor | ✅ | ★ C_i mide LEGALIDAD del proceso, no entrega · E_i y C_i comparten escala sin ser la misma · 4 divergencias latentes |
| GM-Ω | `011-C3` | Justificación de cada transformación · qué·por qué·quién·cuándo | ✅ | ★ el 27-abr C_i no ENTRÓ: cambió de mecanismo (imputabilidad → calidad de proceso) · E_i↔C_i justificada · 3 de 9 NO DETERMINABLE porque la razón nunca se escribió |
| GM-Ω | `011-C4` | Dictamen · ¿merecen permanecer las decisiones de diseño? | ✅ | ★ NINGUNA decisión resultó incorrecta · toda la anulación viene hoy de `V_i` (6/25 metas · 12,8 % del peso) · tratar V=0 como «no acreditado» movería +4,03 pp · la acción es DECLARAR, no corregir |
| TF | `T1` | Inventario de nombres propios | ✅ |  |
| TF | `T2` | Clasificación ontológica + capa de presentación | ✅ |  |
| TF | `T3` | Contrato índice → dominio → rol → pregunta → capa | 🔄 | se llena con la curación de cada dominio |
| TF | `T4` | Rol de cada indicador | 🔄 | sin inventar: sólo con fuente |
| TF | `T5` | Presentación dentro de su dominio | ⛔ | T3 · T4 |
| TF | `T6` | Acción: conservar / renombrar / deprecar / eliminar | ⛔ | 011 · T5 |
| QNEXT | `Q0` | Carta de rearquitectura v2 · el plan del refactor integral | ✅ | ★ 4 bases medulares · 5 categorías · 10 ejes · 4 inventarios separados · DOC-029 regla maestra · NO ejecuta |
| QNEXT | `BM-01` | Corpus normativo · vigencia, clase y separación norma↔instrumento | ⬜ | 🔴 13.147 chunks SIN columna de vigencia · document_class vacía en 81 % · norma e instrumentos de gestión en la misma tabla |
| QNEXT | `BM-05` | Memoria histórica de diseño · 898 archivos + 71 versiones únicas del motor | ✅ | ★ inventariada · la serie fechó el cambio de `C_i` · pendiente el resto del corpus (121 .md · 80 .txt de fórmulas) |
| GM-Ω | `011-C3R` | Serie temporal del motor + Fase 3 documental · sensibilidad de las conclusiones de C3 | ✅ | ★ CERRADO · 25→29-abr en UN acto · `E-CRIT-04` declara el PORQUÉ del constructo · parámetros sin fundamento cuantitativo = 3 decisiones ABIERTAS para C4 |
| GM-Ω | `011-P6` | Grafo de correspondencia de versiones · identidad de artefactos | ⬜ | 3 esquemas sin reconciliar · NO bloquea a C4 · no cabe en 010: es identidad, no transferibilidad |
| QNEXT | `Q1` | Matriz de clasificación · candidato → ratificado | ⬜ | no espera al dictamen: clasificar no es cambiar · primer test = migración semántica de «auditoría» |
| QNEXT | `Q2` | Dashboards y narrativa por dominio · visual→analítica→explicación | ⛔ | R0 — no 011: depende de saber qué pregunta cada dominio |
| QNEXT | `ADR-D` | Declarar las 5 decisiones · ADR-054 a ADR-058 | 🔄 | ★ los 5 redactados con los 10 campos · PROPUESTOS, pendientes de sello de Javo (ADR-035 §5) |
| QNEXT | `Q3` | Ejecución del refactor · fondo y forma | ⛔ | ADR-D sellados · Q1 · R0/R1 |
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

**22 de 44 etapas cerradas.**

## Estado derivado de las fuentes vivas

| | |
|---|---:|
| Deudas declaradas | 14 |
| Deudas resueltas | 6 |
| Deudas abiertas | **8** |
| Reglas de doctrina con custodio | 31 |
| Pruebas que las fijan | 471 |
| Documentos GM-Ω | 15 |

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
- [`GM-OMEGA_ICPI_DICTAMEN_011C4.md`](GM-OMEGA_ICPI_DICTAMEN_011C4.md)
- [`GM-OMEGA_ICPI_FICHA_FORENSE.md`](GM-OMEGA_ICPI_FICHA_FORENSE.md)
- [`GM-OMEGA_ICPI_GAMING_009.md`](GM-OMEGA_ICPI_GAMING_009.md)
- [`GM-OMEGA_ICPI_JUSTIFICACION_011C3.md`](GM-OMEGA_ICPI_JUSTIFICACION_011C3.md)
- [`GM-OMEGA_ICPI_MATRIZ_004.md`](GM-OMEGA_ICPI_MATRIZ_004.md)
- [`GM-OMEGA_ICPI_RECONCILIACION_008R.md`](GM-OMEGA_ICPI_RECONCILIACION_008R.md)
- [`GM-OMEGA_ICPI_SEMANTICA_011C2.md`](GM-OMEGA_ICPI_SEMANTICA_011C2.md)
- [`GM-OMEGA_ICPI_SENSIBILIDAD_007.md`](GM-OMEGA_ICPI_SENSIBILIDAD_007.md)
- [`GM-OMEGA_ICPI_SERIE_MOTOR_011C3R.md`](GM-OMEGA_ICPI_SERIE_MOTOR_011C3R.md)
- [`GM-OMEGA_MAPA_MAESTRO.md`](GM-OMEGA_MAPA_MAESTRO.md)
- [`GM-OMEGA_TERMINOLOGIA_T1-T2.md`](GM-OMEGA_TERMINOLOGIA_T1-T2.md)
- [`GM-OMEGA_TRANSFERIBILIDAD_010.md`](GM-OMEGA_TRANSFERIBILIDAD_010.md)

## Las tres reglas que sostienen este mapa

1. **Ningún frente se cierra sin custodio.** Una etapa marcada `✅` sin prueba que la fije acredita cero por no existir — es el defecto que `D-004` documentó en el propio CI.
2. **Un frente bloqueado no es un frente parado.** `011` está bloqueada por `008-010`, y esos tres pueden trabajarse hoy. La secuencia existe para ordenar, no para esperar.
3. **Este mapa se deriva.** El día que alguien lo edite a mano, dejará de reflejar el estado real sin que nada avise, y volveremos exactamente al punto que motivó escribirlo.

---
*QUIRA · Mapa Maestro · 22/44 etapas cerradas · 8 deudas abiertas · Dylus Lab © 2026*
