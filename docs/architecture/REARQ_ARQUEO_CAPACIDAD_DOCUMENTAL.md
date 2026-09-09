---
id: REARQ-ARQUEO-001
authority:
  parent: REARQUITECTURA_QUIRA
  constitution_articles: [1, 2, 3, 9]
  type: ARQUEO
status: CONGELADO — preservación activa
fecha: 2026-09-09
---

# REARQ · Arqueo de la capacidad documental de Transparencia

> ## Principio de esta parte del expediente
>
> **La capacidad documental de Transparencia no se considera una capacidad perdida ni
> inexistente. Su existencia está demostrada por artefactos normativos, metodológicos,
> computacionales y documentales preservados. La cuestión abierta de `REARQ` no es su
> existencia, sino su residencia arquitectónica, grado de completitud, escalabilidad y
> eventual reutilización transversal.**

Este documento existe porque la Rearquitectura estuvo a punto de tratar como vacío algo que
llevaba semanas construido. Se registra el arqueo para que **no vuelva a ocurrir**.

## 1 · La secuencia obligatoria

```
ARQUEO → PRESERVACIÓN → RECONCILIACIÓN → DISEÑO REARQ → MIGRACIÓN
```

**Nunca al revés.** No se alinea un artefacto histórico con un diseño que todavía no existe.
Primero se establece qué hay, luego se protege, luego se reconcilia con el canon, y sólo
entonces se diseña. La migración es lo último.

## 2 · Artefactos protegidos · NO SE TOCAN

Hasta completar `RECONCILIACIÓN`, estos artefactos no se modifican «para alinearlos» con
`REARQ`. Se leen, se citan y se preservan.

| Artefacto | Naturaleza |
|---|---|
| `docs/pcd/PCD-D07_Transparencia.md` | expediente de curación · `EN CURACIÓN` |
| `docs/architecture/gm_dumps/H09_S7_TRANSPARENCIA_LOTAIP.md` | silo del motor |
| `docs/architecture/gm_dumps/H70_BITACORA_LOTAIP_OPACIDAD.md` | bitácora de opacidad |
| `docs/architecture/gm_dumps/H41_IOC_OPACIDAD_CRITICA.md` | índice de opacidad |
| `scripts/holding/ingest_lotaip.py` | ingestor |
| `quira_pages/p07_transparencia.py` | superficie del dominio |
| `docs/observations/OBS-009_Divergencia_SIGAD_LOTAIP_GAD_MCR.md` | observación `S6`↔`S7` |
| `data/lotaip/**` | **1.748** archivos · de ellos **936** en `descargas/` |
| `data/vault_backup_p2/02_NORMATIVA/11_LOTAIP` · `12_REGLAMENTO_LOTAIP` · `13_GUIAS_LOTAIP` | fuente del criterio |

## 3 · Lo que queda DEMOSTRADO por el arqueo

**1 · Existe el expediente específico**, y es el mayor del proyecto: 26.388 bytes, 440 líneas,
declarado `EN CURACIÓN` a propósito.

**2 · Existe evidencia documental real, no una especificación.** Inventario del 2026-08-18 con
**417/417 enlaces inspeccionados y cero fallos de red**:

```
417   enlaces publicados accesibles
        391  archivos individuales
         26  contenedores  →  935 artefactos dentro
──────────────────────────────────────────────
1.326  objetos físicos observados     el balance cuadra
```

Naturaleza determinada **por firma del archivo, no por su extensión**: 267 PDF · 123 imágenes ·
26 contenedores · 1 sin identificar. Trazabilidad por `SHA-256`. Identificación de escaneados:
**10 PDF únicos**, no las cifras infladas que produjeron los conteos anteriores.

**3 · Existe la norma técnica como fuente del criterio, con su SHA.** El *Instructivo para
evaluar el nivel de cumplimiento de los parámetros técnicos de la transparencia activa* (DPE
2024). La matriz del Anexo 1 vive en `matriz_calificacion.json` **con el SHA del Instructivo**, y
los parámetros llegan al motor desde la RO, nunca desde el código (`Regla de Oro 9`).

**4 · Existe el motor de evaluación**, auditado parámetro por parámetro contra el Instructivo:

| | Resultado |
|---|---|
| `SITA = (CTA+ETA+RP+CI)/4` | idéntico ✅ |
| `CTA` · `ETA` · `RP` | idénticos ✅ |
| `CI` | ⛔ el motor exigía los 3 parámetros a los 24 numerales; el Anexo 1 los asigna numeral por numeral → **corregido** |

Resultados: `SITA 2025 · 0,4646` · `SITA 2026 (ene-may) · 0,8382`. Base: 4 CNO · 46/46 SHA · 5 RO
· 936 archivos de evidencia con SHA · 36 pruebas de regresión.

**5 · Existe la separación metodológica** entre construir el canon de evaluación, ejecutar la
captura periódica, procesar evidencia y evaluar cumplimiento. Fijada por Javo el 2026-08-19:

> *«Claude no es QUIRA. Estamos construyendo un ecosistema que deberá reportar más adelante 222
> municipios, sin Claude, solo QUIRA.»*

> **Construcción del canon ≠ capacidad operativa.** La primera corre una vez, bajo criterio
> humano, y su producto se sella con SHA — *un sistema que reejecuta la extracción de su propia
> vara puede cambiarse el patrón con el que mide*. La segunda corre cada mes, en 222 municipios,
> sin nadie mirando.

**6 · Existe la opacidad como resultado analítico**, no como juicio político. El `IOC` ya está en
el motor (`H41`, 17,71 %). Y el ranking futuro es **compatible con la arquitectura**, bajo tres
reglas ya escritas:

| Norma | Qué establece |
|---|---|
| `ADR-024` | el Radar Nacional **es el producto principal** — 222 GAD · semáforo · ranking |
| `ADR-041` | exige el estado **`sin ciclo comparable`**: un GAD sin histórico *«aparecería con los peores indicadores por una razón que no tiene que ver con su gestión»*. Se registra, se muestra, **no se computa** |
| `ADR-043` | prohíbe el ranking **ideológico** y el juicio político — no el ranking de evidencia |

**7 · La ausencia de evidencia está tratada metodológicamente.** Un archivo que no puede
procesarse **no se convierte artificialmente en incumplimiento**:

- `Ordenanzas.zip` supera 500 MB → `cortado_por_tope_de_tamano` = *«captura incompleta del
  observador, jamás ausencia del sujeto obligado»*
- Numeral 10: 8 enlaces devuelven 404; se falsó el instrumento primero; los 7 restantes quedan
  **sin verificar**, no «inaccesibles»
- `RO-VII-005` nace `no_observable` — requiere otra fuente, no otro cálculo
- `RO-VII-004` sin solicitudes: *«no hay incumplimiento: hay ausencia de ejercicio del derecho»*

Este punto 7 es doctrina general de QUIRA, no un detalle de d07.

## 4 · La pregunta `REARQ` correcta

El problema **ya no es** «QUIRA no tiene capa de adquisición documental». La tiene, para LOTAIP.
La pregunta es otra:

> **¿La capacidad documental construida para Transparencia es sólo un componente de su dominio,
> o es el primer caso implementado de una capacidad transversal que otros dominios deben
> reutilizar?**

Porque un mismo documento institucional puede producir **múltiples evidencias para múltiples
dominios**:

```
Portal LOTAIP → documento → captura → SHA → extracción → verificación → evidencia canónica
                                                                            │
        ┌───────────────┬───────────────┬──────────────┬────────────────────┤
   Transparencia   Participación   Rendición de    Planificación      Gobernanza
   cumplimiento      actas y        cuentas         instrumentos       mandato
   y opacidad      mecanismos      informes        de planificación
```

La evidencia documental **no debería capturarse cinco veces porque cinco dominios la necesitan.**

## 5 · La distinción que se conserva

| | |
|---|---|
| **DOMINIO DE TRANSPARENCIA** | evalúa transparencia · sectorial · producto |
| **CAPACIDAD DOCUMENTAL REUTILIZABLE** | captura, verifica y sella evidencia · posible infraestructura transversal |

> Que ambas estén **hoy implementadas juntas no demuestra que deban permanecer juntas. Tampoco
> demuestra que deban separarse.** Ese es exactamente el tipo de cuestión que `REARQ` resuelve, y
> no se decide en este arqueo.

## 6 · Clasificación · lo que NO es

**No es `RECONSTRUIR`.** Ese destino queda descartado por la evidencia de este arqueo.

Que hoy exista OCR manual para 10 artefactos **no significa que la arquitectura documental esté
ausente**: significa que su **automatización y escalabilidad** están incompletas. Es una
diferencia de grado de madurez, no de existencia.

Destinos que siguen abiertos, sin elegir ninguno:

| Destino | Sobre qué recaería |
|---|---|
| `CONSERVAR` | el canon de evaluación, la trazabilidad, el tratamiento de la ausencia |
| `MEJORAR` | OCR y procesamiento · escalabilidad a 222 GAD |
| `DESCOMPONER` | separar capacidad transversal de lógica específica de Transparencia |
| `TRASLADAR` | llevar componentes de captura/sellado a infraestructura común |

## 7 · Correcciones que este arqueo registra

**Se retira el hallazgo «existe una capacidad de sistema sin dominio asignado».** Es falso. La
capacidad tiene dominio, expediente, norma con SHA, código, 1.748 descargas y 936 archivos de
evidencia.

**Se corrige además una cifra de este mismo arqueo.** La primera redacción atribuyó los 1.748
archivos a `data/lotaip/descargas/`. El reparto real es **1.748 en `data/lotaip/`, de los cuales
936 están en `descargas/`** — y 936 es justamente la cifra de evidencia con SHA que `PCD-D07`
declara. Es el mismo error que ese expediente cazó cuatro veces: **una cifra parcial con
apariencia de total**.

**Causa del error, y la regla que deja:**

> ### `DOC-035` · El alcance de una búsqueda es parte de su resultado
>
> La búsqueda que produjo el falso vacío **excluyó rutas** (`worktrees`) y **buscó por el número
> del dominio** en vez de por el nombre del trabajo. Ninguna de las dos cosas se declaró al
> reportar el resultado.
>
> **Una búsqueda acotada no autoriza a declarar ausencia.** Quien informa un vacío debe declarar
> qué rutas incluyó, qué términos usó y qué excluyó — igual que `d07` declara
> `cortado_por_tope_de_tamano` en lugar de afirmar que el archivo no existe.
>
> Es `DOC-034` aplicado al observador: **no haber mirado bien no es haber mirado.**

**Numeración · verificado, no resuelto.** La hipótesis de renumeración por la baja de `d04` es
**falsa**: el código conserva `QINV-001..013` sin renumerar — `QINV-006` es Salud Institucional
(`m1_situacion.py`) y `QINV-007` es Transparencia (`p07_transparencia.py`). La dirección se
refiere al dominio de Transparencia como `DOM06`. **La discrepancia se registra y no se resuelve
aquí** (`DOC-033`: el nombre no demuestra la correspondencia).

**Lo que sí queda en pie:** `d06 Salud Institucional` conserva su silo `S6` (`H08` autorreporte
SIGAD) abierto, sin `ICM` y con `SAT-I` apagada (`app/services/sat_evaluator.py:297`, verificado
el 2026-09-08). Es **otro** hueco, distinto del de Transparencia, y `OBS-009` documenta
precisamente la divergencia entre ambos silos.

---
*REARQ · Arqueo `001` · Dylus Lab © 2026 · el Gold Master no se modificó · baseline 27,4582 %
congelado · preservación activa sobre 9 clases de artefacto.*
