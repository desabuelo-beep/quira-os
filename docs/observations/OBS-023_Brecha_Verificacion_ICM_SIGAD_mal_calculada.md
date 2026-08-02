---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 4, 9]
  type: OBSERVACION
---

# OBS-023 · La Brecha de Verificación ICM↔ICPI está mal calculada e interpretada

**2026-07-29 · hallazgo abierto por Javo · silo S6 (SIGAD) · afecta el núcleo de la tesis**

> **Lo que Javo dijo:** *"SAT-I mide o analiza el tema de ICM de SIGAD… pero creo **no la
> aterrizamos bien metodológica y legalmente**, habría que revisar."* Tenía razón en las dos
> cosas: el mapeo estaba mal **y** el cálculo también.

---

## 1 · Primer error: SAT-I no es de contratación, es de SIGAD

La matriz de cableado la había ubicado en **d03 Contratación** por su nombre *"Fragmentación
Selectiva"*. El catálogo dice otra cosa:

| Campo | Valor real (`SAT_Catalogo` fila 7) |
|---|---|
| Base legal | **COPFP Art. 54** — *"las entidades deben reportar avances de **todas** las metas del plan operativo en el SIGAD"* |
| Métrica | `ICM_Global >= 80% AND pct_metas_reportadas <= 10%` |
| Doctrina | *"calificación alta con universo de metas mínimo es señal de fragmentación"* |

**`SAT-I` pertenece al silo S6 (SIGAD)**, que es uno de los tres **sin DOM que lo cure**
(MATRIZ_CABLEADO_CANONICO). No a d03. Corregido.

### Qué mide realmente

No fragmentación de contratos: **fragmentación del reporte**. El GAD obtiene calificación alta
en SIGAD **reportando solo una fracción de sus metas**.

## 2 · ⛔ DESCALCE DE HORIZONTES — la comparación que yo había hecho es INVÁLIDA

> **Dato decisivo de Javo (2026-07-30):** *"el PDOT 2023-2027 de Montecristi fue aprobado vía
> **ordenanza el 5 de noviembre de 2024**. Es decir que esos años 2023 y 2024 fueron trabajados
> con el **PDOT 2019-2023**."*

La primera versión de esta observación decía:

| ~~Año~~ | ~~Metas al SIGAD~~ | ~~Metas del PDOT en el motor~~ | ~~Cobertura~~ |
|---|---:|---:|---:|
| ~~2023~~ | ~~5~~ | ~~25~~ | ~~20%~~ |
| ~~2024~~ | ~~9~~ | ~~25~~ | ~~36%~~ |

**Está mal.** Las 5 y 9 metas pertenecen al **PDOT 2019-2023**; las 25 del motor son del **PDOT
2023-2027**. Dividir unas entre otras compara **universos programáticos distintos**:

```
ICM 2023 ─┐
          ├──► PDOT 2019-2023      (plan anterior)
ICM 2024 ─┘

ICPI ─────────► PDOT 2023-2027      (plan vigente, ordenanza 05-nov-2024)
```

**Cualquier "brecha" calculada así sería un artefacto del descalce de horizontes**, no evidencia
sobre el GAD. Habría sido una crítica metodológica fatal ante una revisión académica.

### Lo que SÍ permiten los informes 2023-2024

| ✅ Sirven para | ❌ NO sirven para |
|---|---|
| caracterizar el patrón histórico del autorreporte | afirmar *"Montecristi tuvo X de congruencia"* |
| entender cómo el SIGAD calcula el ICM | fundar la brecha ICM↔ICPI |
| construir el ETL y calibrar el parser de **d06** | comparación longitudinal con el ICPI actual |

## 2-bis · Naturaleza del ICM: se calcula sobre el PDOT VIGENTE de cada año

> **Precisión de Javo (2026-07-30), para que quede claro:** *"no es que haya otros ICM para medir
> el nuevo PDOT. Los ICM se miden **anualmente con el instrumento PDOT vigente para cada año**.
> No existe un ICM 2023 o 2024 en base al PDOT 2023-2027: **los únicos y oficiales son los que
> tenemos**, aunque corran con el PDOT 2019-2023."*

Eso corrige la Fase C que la asesoría formuló como *"cuando exista el ICM del PDOT 2023-2027"*.
**No hay ICM retroactivo — no puede haberlo.** La secuencia real:

| Año | PDOT vigente | ICM | Comparable con el ICPI |
|---|---|---|---|
| 2023 | 2019-2023 | ✅ existe · **oficial y único** | ❌ otro plan |
| 2024 | 2019-2023 *(hasta 05-nov)* | ✅ existe · **oficial y único** | ❌ otro plan |
| **2025** | **2023-2027** | ⏳ **aún no publicado** | ✅ **el primero comparable** |

**La Fase C no espera un dato imposible: espera el ICM 2025**, primer ejercicio completo bajo el
plan vigente. Por el patrón de envío observado (informe 2023 → mayo 2024; informe 2024 → mayo
2025), sería exigible hacia **mayo de 2026**.

### Estructura temporal de d06

| Fase | Período | Estatus del dato | Uso admisible |
|---|---|---|---|
| **A · Caracterización** | 2023-2024 · PDOT 2019-2023 | ✅ **hecho documentado** | estudiar el SIGAD · calibrar el parser · **NO comparar** |
| **B · Escenario** | 2025-2026 · sin informe publicado | ⚠️ **proyección, NO dato** | simulación etiquetada (HCI-01) |
| **C · Auditoría empírica** | **al publicarse el ICM 2025** | ⏳ ~mayo 2026 | **única comparación ICM↔ICPI válida** |

## 2-ter · ⛔ Lo que NO se hace: redefinir SAT-I

La asesoría propuso *"convertir SAT-I en una SAT de elegibilidad metodológica"* que responda
*"¿existe comparabilidad temporal?"*. **La idea es buena; la ubicación es incorrecta.**

`SAT-I` está definida en el Gold Master, que es **la autoridad** (Regla 1):

```
ICM_Global >= 80% AND pct_metas_reportadas <= 10%
```

Eso mide **fragmentación del reporte**, no elegibilidad. Redefinirla desde QUIRA sería construir
un segundo canon — exactamente lo que R-B prohíbe.

**Lo correcto es una PRECONDICIÓN aguas arriba**, que no toca la SAT:

```
   ¿ICM y ICPI pertenecen al MISMO horizonte PDOT?
            │
    ┌───────┴────────┐
   NO               SÍ
    │                │
    ▼                ▼
"no comparable    se evalúa SAT-I
 por descalce"    tal como la define
 → no se calcula   el Gold Master
```

La SAT conserva su definición canónica. Lo que se añade es un **guard de comparabilidad** que
decide *si procede evaluarla*, no *qué mide*. Es la misma lógica que `Hay_Datos_PP` en `H24c`:
una guardia que bloquea el cálculo sin alterar la fórmula.

### La proyección, redactada como corresponde

Javo aporta conocimiento de campo: *"cuando se revisan los portales oficiales, los ICM de los GAD
siempre autorreportan por encima del 90%"*. Es observación válida — **pero no es un dato de
Montecristi 2025**. La formulación admisible:

| ❌ Inadmisible | ✅ Admisible |
|---|---|
| *"el ICM 2025 fue del 95%"* | *"para efectos de simulación se proyecta un ICM > 90%, siguiendo el patrón histórico observado en portales oficiales de GAD, hasta disponer del informe oficial"* |

> **Este hallazgo FORTALECE la tesis en vez de debilitarla.** En lugar de comparar dos indicadores
> construidos sobre planes distintos —crítica fatal—, el argumento pasa a ser: *2023-2024 modelan
> el funcionamiento del SIGAD; 2025-2026 son el primer ciclo auditable del nuevo PDOT; la
> confrontación ICM↔ICPI se certifica cuando existan los reportes del mismo horizonte.*

> ⚠️ **Nada de esto afirma incumplimiento.** Determinar si el reporte al SIGAD infringe el COPFP 54
> corresponde al ente rector, no a QUIRA (Carta Art. 4.5).

## 3 · Segundo error, más grave: el cálculo de la brecha

La **Brecha de Verificación** (`ICM autoreportado − ICPI verificable`) es el hallazgo central de
QUIRA: *lo que el GAD dice de sí mismo frente a lo que puede demostrarse*. Está mal en dos hojas
a la vez, **con signos opuestos**:

| Celda | Fórmula | Valor | Problema |
|---|---|---:|---|
| `H08!B7` ICM_Global_SIGAD_2026 | *(input)* | **0,01** | la nota de `B13` dice *"ICM autoreportado (**100%**)"* — **contradice el input** |
| `H08!B10` Brecha_Verificacion | `B7 − ICPI` | **−0,2646** | **negativa**: diría que el GAD se autorreporta POR DEBAJO de lo verificable |
| `H12!B35` ICM_SIGAD_Oficial | `H08!B7 × 100` | **1** | ¿1% o 100%? la escala es ambigua |
| `H12!B36` Brecha_Verificacion | `B35 − B33` | **+0,7254** | **positiva** — signo contrario a `H08!B10` |
| `H12!B37` Interpretación | `IF(B36>30,"🔴 Alta",IF(B36>15,"🟡 Media","✅ mínima"))` | ✅ ***"mínima"*** | **el bug** |

### El bug de escala

`B36` está en **fracción** (0,7254 = 72,54%). `B37` la compara contra **30 y 15 como puntos
porcentuales**. Como `0,7254 > 30` es falso, el motor concluye:

> ✅ *"Brecha de Verificación **mínima** — Consistencia entre ICM autoreportado y verificación"*

**Cuando la brecha real es de ~72,5 puntos.** El indicador más potente de la tesis está
reportando lo contrario de lo que muestra.

### Y las dos hojas no coinciden

`H08!B10 = −0,2646` frente a `H12!B36 = +0,7254`. **La misma magnitud con signo opuesto**, porque
`H08` usa `B7 = 0,01` crudo y `H12` lo multiplica por 100. Una de las dos escalas está mal, y
mientras no se resuelva **ninguna de las dos cifras es citable**.

## 4 · Lo que NO se corrige aquí, y por qué

**No se toca el motor.** Falta el dato que resuelve la ambigüedad: **cuál es el ICM real
reportado por el GAD**. Está en los informes SIGAD, pero extraerlo con rigor es trabajo del silo
S6 — que **no tiene DOM**. Poner un número supuesto sería inventar cifra pública.

| Corrección | Naturaleza | Quién |
|---|---|---|
| `H12!B37` — comparar contra la misma escala que `B36` | **presentación** (Regla 1 lo permite) | dirección técnica, tras fijar la escala |
| `H08!B7` — cargar el ICM real de los informes | **input** | requiere extracción S6 |
| `H08!B10` vs `H12!B36` — unificar signo y escala | **metodológica** | **Javo** |

## 5 · Por qué esto importa más que un bug

La brecha ICM↔ICPI **es la tesis**: el GAD se autorreporta alto y solo una fracción es
verificable. Es el mismo patrón que OBS-020 encontró en el POA y OBS-021 en las demandas.

**Doble impedimento para citarla hoy:**

1. **Escala** — `B36` y `B37` operan en unidades distintas (§3).
2. **Horizonte** — no existe ICM oficial calculado sobre el PDOT 2023-2027 (§2).

Publicar una brecha mal calculada **y** construida sobre planes distintos sería exactamente el
error que este sistema existe para evitar.

## 6 · Acciones

| # | Acción | Estado |
|---|---|---|
| 1 | Corregir el mapeo: `SAT-I` → **S6 SIGAD**, no d03 | ✅ |
| 2 | ⛔ **RETIRADA** la comparación 5/25 · 9/25 — descalce de horizontes PDOT (Javo) | ✅ corregida |
| 3 | Detectar el bug de escala en `B36`/`B37` y el signo opuesto | ✅ |
| 4 | Extraer el ICM real de los informes SIGAD 2023-2024 **como calibración, no como dato de congruencia** | ⏳ **requiere S6** |
| 4b | Etiquetar 2025-2026 como **proyección de escenario**, nunca como hecho | ⏳ |
| 5 | Unificar escala y signo entre `H08` y `H12` | ⏳ **Javo** |
| 6 | Corregir `H12!B37` una vez fijada la escala | ⏳ |
| 7 | Crear el DOM que cure S6 (SIGAD) | ⏳ — hoy **ningún dominio lo audita** |

> **La acción 7 es la de fondo.** Tres silos del motor no tienen dominio (S1 electoral · **S6
> SIGAD** · S9 ODS), y S6 es el que mide la distancia entre discurso y evidencia. Sin él, el
> hallazgo más potente de QUIRA queda sin custodio.

---
*OBS-023 · Dylus Lab © 2026 · hallazgo de Javo · silo S6 · relacionada con OBS-020 y OBS-021.*
