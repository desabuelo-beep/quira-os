# QUIRA · MAPA MAESTRO DE FRENTES

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/mapa_maestro.py`. El **estado** sale de las fuentes vivas (`deuda.py`, `doctrina.py`, `docs/pcd/`, `tests/`); la **secuencia y las dependencias** se declaran en el script, porque son un juicio de dirección y no un dato.

> ### Por qué existe
> Javo: *«hay varios frentes […] para que no nos pase nuevamente volver a hacer refactor porque no recordamos»*. No había un artefacto que dijera qué frentes hay, en qué orden y qué depende de qué: vivía en la cabeza del director y disperso en cinco documentos.
>
> Es la misma deuda que esta auditoría persigue en todo lo demás —conocimiento que existe en el diseño y no en algo verificable— con un agravante: **de éste dependía no repetir trabajo.**

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
  AHORA, en paralelo — nada de esto se bloquea entre sí
  ├── GM-Ω 008-R resolver las 40 ambiguas · 66↔25  ← desbloquea v2
  ├── GM-Ω 009   gaming: ¿se optimiza el índice sin mejorar la realidad?
  ├── GM-Ω 010   transferibilidad LATAM
  ├── T3-R R0    diagnóstico de los 13 dominios
  ├── T3-R R1    modelos A · B · C
  ├── 2ING d07   curación de Transparencia
  └── DEUDA      D-008 · D-009 · D-011 · D-012

           ↓ los tres primeros alimentan

  GM-Ω 011   DICTAMEN DE VALIDEZ DEL CONSTRUCTO
             ¿qué mide el ICPI · qué significa su álgebra ·
             conservar / corregir / potenciar / rediseñar?

           ↓ y sólo entonces

  ├── T3-R R2    residencia y ámbito de los índices
  ├── TF   T5    presentación dentro del dominio
  └── TF   T6    conservar / renombrar / deprecar / eliminar
```

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
| GM-Ω | `009` | ¿Se puede optimizar el índice sin mejorar la realidad? | ⬜ |  |
| GM-Ω | `010` | Transferibilidad LATAM · núcleo vs adaptador | ⬜ |  |
| GM-Ω | `011` | **Dictamen de validez del constructo + UNIDAD DE ANÁLISIS** | ⛔ | 008 · 009 · 010 · ⚠️ 008-R le añadió: ¿qué es `i`? |
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

**13 de 29 etapas cerradas.**

## Estado derivado de las fuentes vivas

| | |
|---|---:|
| Deudas declaradas | 12 |
| Deudas resueltas | 6 |
| Deudas abiertas | **6** |
| Reglas de doctrina con custodio | 19 |
| Pruebas que las fijan | 378 |
| Documentos GM-Ω | 8 |

### Deudas abiertas

| Deuda | Estado |
|---|---|
| `D-001` | ABIERTA |
| `D-008` | ABIERTA |
| `D-012` | ABIERTA |
| `D-011` | ABIERTA |
| `D-010` | ABIERTA |
| `D-009` | EN CURACIÓN · las 4 superficies del IGP curadas 2026-09-03. La cura NO fue cambiar 27,98 por 27,00: el motor e |

### Documentos de la auditoría

- [`GM-OMEGA_CONTRATO_INDICE_DOMINIO.md`](GM-OMEGA_CONTRATO_INDICE_DOMINIO.md)
- [`GM-OMEGA_ICPI_COBERTURA_008.md`](GM-OMEGA_ICPI_COBERTURA_008.md)
- [`GM-OMEGA_ICPI_FICHA_FORENSE.md`](GM-OMEGA_ICPI_FICHA_FORENSE.md)
- [`GM-OMEGA_ICPI_MATRIZ_004.md`](GM-OMEGA_ICPI_MATRIZ_004.md)
- [`GM-OMEGA_ICPI_RECONCILIACION_008R.md`](GM-OMEGA_ICPI_RECONCILIACION_008R.md)
- [`GM-OMEGA_ICPI_SENSIBILIDAD_007.md`](GM-OMEGA_ICPI_SENSIBILIDAD_007.md)
- [`GM-OMEGA_MAPA_MAESTRO.md`](GM-OMEGA_MAPA_MAESTRO.md)
- [`GM-OMEGA_TERMINOLOGIA_T1-T2.md`](GM-OMEGA_TERMINOLOGIA_T1-T2.md)

## Las tres reglas que sostienen este mapa

1. **Ningún frente se cierra sin custodio.** Una etapa marcada `✅` sin prueba que la fije acredita cero por no existir — es el defecto que `D-004` documentó en el propio CI.
2. **Un frente bloqueado no es un frente parado.** `011` está bloqueada por `008-010`, y esos tres pueden trabajarse hoy. La secuencia existe para ordenar, no para esperar.
3. **Este mapa se deriva.** El día que alguien lo edite a mano, dejará de reflejar el estado real sin que nada avise, y volveremos exactamente al punto que motivó escribirlo.

---
*QUIRA · Mapa Maestro · 13/29 etapas cerradas · 6 deudas abiertas · Dylus Lab © 2026*
