# GM — REGISTRO INTEGRAL del Gold Master (SIAP-ICPI v5.5 TGI)

> **Fuente única, vectorizada hoja por hoja.** Para que NUNCA MÁS se dude "si hay o no hay, si está o no está".
> Auditoría **100 % determinista** (openpyxl · solo lectura · NUNCA se modificó el Excel · NUNCA se recalculó el motor).
> **El árbitro es SIEMPRE la celda.** Cada cifra de este documento sale de un volcado citado (`hoja!celda`), no de la memoria.

**Generado:** 2026-06-15 · **Excel vivo:** `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` (123 hojas · 991 KB · mtime 2026-05-30) · **timestamp del motor:** 2026-05-26 (H73).
**Herramientas (todas en `scripts/dev/`, reusables):**
- `gm_full_audit.py` → 123 volcados de fórmulas + grafo de dependencias → `gm_dumps/<hoja>.md`, `gm_dumps/_INDEX.md`, `gm_dumps/_ANALYSIS.md`.
- `gm_probe.py` → valores cacheados de auto-chequeos → `gm_dumps/_PROBE_VALUES.md`.
- `gm_freeze_diff.py` → vivo vs FREEZE → `gm_dumps/_FREEZE_DIFF.md`.
- (previos) `gm_surface_map.py`, `gm_h73_dump.py`, `gm_sheet_dump.py`.

---

## 0 · RESUMEN DE HALLAZGOS MAYORES (pegar de vuelta al chat origen)

1. **El motor está limpio de errores de fórmula.** En las 123 hojas hay **3 tokens de error**: `H01!A28 #NAME?` es **falso positivo** (texto que explica que `=AVEP()` no existe); `H36c!C13 #REF!` (mapa Obsidian, fuera del cálculo) y `H71!B8 #REF!` (radar EP, enmascarado por `IFERROR→0`) son **reales pero periféricos**. **La cadena canónica H12/H07b/H98/H99/H73 NO tiene `#REF!`/`#DIV/0!`.**
2. **ICPI 2026 = 17.45 % 🔴 Ruptura Sistémica, confirmado en la celda.** `H12!B33 = 0.17448914236369514` (= `B31 0.119102 / B32 0.682576`); `B34 = 🔴 Ruptura`. La fórmula canónica `=B31/B32*100` está **INTACTA** (auto-chequeo `H85!CHK-11 ✅ INTACTO`).
3. **Causa #1 del bajo ICPI — metas con `Ti=0` que multiplican por cero (numerador colapsa, denominador no).** En el propio motor: `H12!F18=0` (meta `FA-I-X-01`, **BOMBEROS Ti=0.0000**) y `H12!F26:F29=0` (4 metas **`GAD_SIN_ESIGEF`** Ti=0.0000). **5 de 25 metas** aportan 0 al numerador.
4. **El dato de Bomberos SÍ EXISTE en otra fuente.** `H90!D7 = 19.43 %` (cod `B7 1,485,033.40` / dev `C7 288,599.28` · "Cédula oficial SERCOP Q1-2026"). El motor lo lee desde eSIGEF (vacío para Bomberos) ⇒ 0. **Es problema de RUTEO de fuente, no de falta de dato.**
5. **Discrepancia eSIGEF vs SERCOP en las 4 entidades** (§5): la normalización temporal `Ti_norm` del motor diverge de H90 — Patronato `H12 41.72 %` vs `H90 19.56 %`; EP Aseo `H12 72.48 %` vs `H90 18.17 %`; Bomberos `0` vs `19.43 %`.
6. **`Motor Ci`: íntegro hoy, con 1 alerta.** `H39` confirma `TBL_CALIBRACION_Ci` = 25 metas (`D25 ✅`), `Ci_mín ≥ 0.50` (`D26 ✅`), **0 hilos rotos** (`D27 ✅`) — el "⚠️ HILO ROTO" es un guard latente, NO está disparado. Pero `H39!D28 = ERROR (#22 desviación Ci 1pp)` ⇒ `H39!B30 = "ERRORES: 1 check fallido"`.
7. **Fragilidad estructural S-04:** los 25 `Pi` de `H12!C6:C30` están **hardcodeados** (no son fórmulas vivas a `H14`). Coinciden hoy, pero si se edita `H14` sin replicar, el ICPI se desincroniza (`H39!A38`).
8. **`VALIDACION_OK = NO` única:** `H73!MMP_AVANCE_PCT` (fila `--- | NO`) — la única clave del contrato sin validar (proviene del template v6.0).
9. **Huecos de ingesta marcados por el propio motor:** `H85!CHK-08 ★PENDIENTE pegar cédula eSIGEF 2026 en H07!A46+` (zona cruda `H07_S5` vacía) y `H85!CHK-12 ⚠️ PENDIENTE PP+CPCCS 2026`. Estado global `H85!D33 = 🟡 12 OK / 1 WARN / 0 ERR`.
10. **Inconsistencia INTERNA de la brecha rural (viva):** `H73!B59 = 1,371,051` y `H99!B60 = 1,371,051`, pero `H97!V-14` computa `7,467,194` (sobre `Z8:Z13`) — y la nota esperaba `1,791,935`. **Tres cifras para el mismo concepto.**
11. **DIFF vivo vs FREEZE: 79/123 hojas difieren, pero ~70 solo por el sello de fecha `F1` (`05-29→05-26`).** Deltas sustantivos reales: (a) **`H06` SERCOP +9,057 celdas** en vivo (carga de contratos post-freeze); (b) **reclasificación territorial** Rural↔Urbana en `H99/CAPA_TERRITORIAL/SCHEMA_TERRITORIOS/H43` + brecha rural `7,467,194 (freeze) → 1,371,051 (vivo)`; (c) `H10` CPCCS 28 celdas (RDC).
12. **TGI = 66.79 se ve "sano" porque su D2 usa el ICPI ANUAL 2025 (69.93 %), no el parcial 2026 (17.45 %)** (`H73 TGI_D2`). Dos lentes temporales coexistiendo — el corazón del diagnóstico de Javo.

**Conclusión:** el Gold Master está ~97 % poblado y la lógica canónica es sólida e intacta. El "17.45 % Ruptura" NO es un bug de fórmula: es (a) `Ti=0` en 5 metas por ruteo de fuente (Bomberos/GAD_SIN_ESIGEF), (b) `FactorTemporal` lineal sobre gasto back-loaded, y (c) el semáforo AVEP anual aplicado a un corte parcial. Todo corregible en **inputs/semáforo/presentación sobre copia** — **NUNCA en `B33`**.

---

## 1 · ÁRBOL DE DEPENDENCIAS — ICPI y TGI (derivado de fórmulas reales)

> Convención: se omiten dos aristas ubicuas y no-sustantivas — `H00_ÍNDICE` (hipervínculos de navegación) y el banner decorativo `="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)` presente en casi toda cabecera. El grafo crudo completo está en `gm_dumps/_INDEX.md` y cada `gm_dumps/<hoja>.md`.

### 1.1 Cadena ICPI (motor canónico)
```
H73_OUTPUT_API  (capa de publicación · 60 fórmulas · lo que LEE el conector)
        ▲
        │  ICPI_GLOBAL = H12_MOTOR_ICPI_CANÓNICO!B33 (live)
        │
H12_MOTOR_ICPI_CANÓNICO!B33  =  B31 / B32 × 100   ← ★ FUENTE ÚNICA · INMUTABLE ★
   (matriz 25 metas × 6 factores · 233 fórmulas)
        ├── Pi  ponderador     ← H14_PONDERADORES   (⚠️ S-04: copiado/hardcodeado en H12!C6:C30)
        ├── Ri  relevancia      ← H14_PONDERADORES
        ├── Vi  variable/avance ← H13_VARIABLES_Vi
        ├── Ei  exigibilidad    (1.0 autónomo / 0.9 compartido / 0.75 difuso · en H12!E)
        ├── Ti  ejecución       ← H07b_Ti_INVERSIÓN_eSIGEF!B20 (Ti_norm)  ◀── CAUSA del 17.45%
        │         └── H07b ← H07_S5_FINANCIERO_eSIGEF (zona cruda · VACÍA 2026) + H_HOLDING_CEDULAS_2026 + H36b
        └── Ci  calibración     ← H01_PARÁMETROS §M (A189:G213 · VLOOKUP, fallback "⚠️ HILO ROTO")
   también lee: H08_S6_AUTOREPORTE_SIGAD, H25_MMP_MENSUAL
```
**Consumidores del ICPI (B33):** H15_ICPI_GLOBAL, H28_RESUMEN_EJECUTIVO, H73, H12b/c/d, y ~50 cabeceras (banner). El consumidor de cálculo real es H15 (recomputa/valida) y H73 (publica).

### 1.2 Cadena TGI (marco territorial)
```
H73_OUTPUT_API  ← TGI_SCORE = H98_TGI_FRAMEWORK!B25 = 66.79
        ▲
H98_TGI_FRAMEWORK   (D1..D5 en D20:D24 · pesos 20/20/25/25/10 · H97!V-06)
        ├── D1 Legalidad        = 83.20   (H98!D20)
        ├── D2 Ejecución(anual)  = 69.93   (H98!D21 = ICPI ANUAL 2025, ¡no el 2026 parcial!)
        ├── D3 Ejecución(Ti)     = 59.85   (H98!D22 = Ti_2025×100)
        ├── D4 Equidad           = 44.79   (H98!D23 = IET)
        ├── D5                    = 100.0  (H98!D24)
        ├── H01_PARÁMETROS  (pesos/umbrales)
        ├── H07b_Ti_INVERSIÓN_eSIGEF
        └── H99_ENGINE_CORE  (parroquial: NBI, IRS, Composite_Need, IET · 7 parroquias)
                 └── H99 ← H01, H07b   →  H98, H73, H97_VALIDACIONES, H36c_OBSIDIAN_MAP
```

### 1.3 Sub-cadena de índices compuestos → H73 (24 entradas vivas a H73)
`H16_IFE · H16c_PSG · H17_IED · H18_ITAM · H19_ICS_ISP · H20_ICODS · H20b_IGP · H20c_IEF · H42_IET · H43_MOTOR_TERRITORIAL · H75_SAT_ENGINE · H89_TRUST_SCORE · H90_PRESUPUESTO · H98_TGI · H99_ENGINE · H12 · H12b · H07b · H10b · H82_CONFIG · H88_EVIDENCE · SCHEMA_NBI · H00 · H01`. Cada uno con su sub-árbol (ver fichas §7).

### 1.4 Motor SAT (riesgo) y MMP (metas)
```
H75_SAT_ENGINE (RIESGO_TOTAL B12=0.2 · MEDIO · 2 activas)
   ← H21_SAT-I, H21b_SAT-0, H22_SAT-II, H23_SAT-III, H24_SAT-IV, H24b_SAT-V, H24c_SAT-VI, H25_MMP, H42_IET   → H73, SAT_Catalogo
H27_MMP_ANUAL ← H26_MMP_TRIMESTRAL ← H25_MMP_MENSUAL ← (H07c, H04, H01)
```

---

## 2 · CONTRATO H73_OUTPUT_API (65 claves · lo que LEE el conector)

`H73` es **capa de publicación VIVA** (60 fórmulas que jalan de 24 hojas), no un snapshot pegado. La columna `FUENTE_CELDA` es **documental** (texto), la columna `VALOR` es **fórmula viva**. Volcado íntegro con valores y `VALIDACION_OK`: [`GM_H73_DUMP.md`](GM_H73_DUMP.md). Estado por bloque:

| Bloque | Claves | Estado | Nota auditada |
|---|---|---|---|
| ICPI | ICPI_GLOBAL=0.17449 · _PCT=17.45 · _CLASIFICACION=🔴 Ruptura · _NUM=0.11910 · _DEN=0.68258 · _2023/24/25 · _ACUMULADO_Q1=0.2367 | ✅ SI | coherente con `H12!B31/B32/B33/B34` |
| Índices | ISP=0.0322 · PSG=0.0283 · IED=0.1652 · IFE=0.7273 · IGP · IOC=0.1771 · ITAM=0.8229 · IET=0.9273 · ICODS=0.875 · IEF=0.0619 | ✅ SI | fracción decimal (normalizar ↔ % en UI) |
| SAT | SAT_ACTIVAS=2 · SAT_RIESGO_TOTAL=0.2 · SAT_CLASIFICACION=MEDIO · SAT_CLASIF_RIESGO=MEDIO | ✅ SI | reconciliado 2026-05-26 (nota en celda) |
| Presupuesto | PRESUPUESTO_TOTAL_4E=54,242,424.28 · GAD_CODIFICADO=45,977,893.81 · GAD_DEVENGADO_Q1=5,147,258.86 | ✅ SI | = `H90!B8/B4/C4` |
| TGI | TGI_SCORE=66.79 · D1=83.2 · D2=69.93 · D3=59.85 · D4=44.79 · D5=100 | ✅ SI | = `H98!B25/D20:D24` |
| Territorio | NBI_RURAL=67.90 · NBI_URBANA=23.00 · IRS=79.7 · **BRECHA_RURAL_USD=1,371,051** · BRECHA_RURAL... | ✅ SI | ⚠️ ver §5: inconsistente con `H97!V-14`=7,467,194 |
| Trust/Meta | TRUST_SCORE=89.6 · MODELO_VALIDO=VÁLIDO · ICPI_META_PDOT=65 · PERIODO=2026-04-30 | ✅ SI | |
| **MMP** | **MMP_AVANCE_PCT=1** + fila `--- | --- | NO` | **🔴 NO** | **única `VALIDACION_OK=NO` del contrato** · "pendiente" · viene de G6.1 v6.0 |

---

## 3 · INVENTARIO DE HUECOS / ERRORES (deliverable #4)

### 3.1 Errores de fórmula (3 tokens · todos verificados)
| Celda | Token | Veredicto | Detalle |
|---|---|---|---|
| `H01_PARÁMETROS!A28` | `#NAME?` | ⚪ **FALSO POSITIVO** | Texto-documentación: *"AVEP NO es función… =AVEP() dará #¿NOMBRE? (#NAME?)"*. No es fórmula rota. |
| `H36c_OBSIDIAN_MAP!C13` | `#REF!` | 🟠 **REAL, periférico** | Fila `TGI_D3_Ejecucion`: `=H98_TGI_FRAMEWORK!D22` con `#REF!` colgando. Hoja de export Obsidian (G1) · fuera del cálculo ICPI. |
| `H71_EP_ADSCRITAS!B8` | `#REF!` | 🟠 **REAL, enmascarado** | `=IFERROR(COUNTIF(#REF!,"✅ OPERATIVA")/…,0)` → devuelve **0** silencioso. El "75 %" visible es nota de texto (`C8`), no la celda. H71 no alimenta a nadie (referencial). |

### 3.2 Metas con `Ti=0` que colapsan el numerador (CAUSA estructural del 17.45 %)
Verificado en `H12!F` (columna Ti) y `H12!H` (fuente), volcado en `_PROBE_VALUES.md`:
| Meta (H12!A) | Fila | Ti (F) | Fuente (H) |
|---|---|---|---|
| `FA-I-X-01` (Bomberos) | 18 | **0** | `eSIGEF-Q1-2026 BOMBEROS Ti=0.0000` |
| `PI-TUR-01` | 26 | **0** | `GAD_SIN_ESIGEF Ti=0.0000` |
| `PI-TUR-02` | 27 | **0** | `GAD_SIN_ESIGEF Ti=0.0000` |
| `FA-CC-01` | 28 | **0** | `GAD_SIN_ESIGEF Ti=0.0000` |
| `AH-AP-04` | 29 | **0** | `GAD_SIN_ESIGEF Ti=0.0000` |

→ 5/25 metas con término de numerador = 0 (multiplicativo), pero sus `Pi·Ri` siguen en el denominador (`B32`). Es el "hueco de realidad" de la tesis que no subió al Excel.

### 3.3 Pendientes / guards / fragilidades marcados por el propio motor
| Origen | Estado vivo | Significado |
|---|---|---|
| `H85!CHK-08` (`G26`) | ★ PENDIENTE | "pegar cédula eSIGEF 2026 en `H07!A46+`" — zona cruda `H07_S5` filas 46+ **vacía** |
| `H85!CHK-12` (`D30`) | ⚠️ PENDIENTE | ingesta PP 2026 + actas CPCCS 2026 (E30 = `0 / 1`) |
| `H85!D33` | 🟡 12 OK / 1 WARN / 0 ERR | estado global de los 13 CHK de sincronía |
| `H39!D28` (#22) | ❌ ERROR | "desviación Ci 1pp revisar" → `H39!B30 = ERRORES: 1` |
| `H39!D27` (#21) | ✅ 0 hilos rotos | `Motor Ci` conectado HOY (guard "⚠️ HILO ROTO" **no** disparado) |
| `H39!D25/D26` | ✅ | `TBL_CALIBRACION_Ci` íntegra (25 metas) · `Ci_mín ≥ 0.50` |
| `H39!A38` (S-04) | ⚠️ riesgo | `Pi` de `H12!C6:C30` **hardcodeados** (no fórmulas vivas a `H14`) |
| `H73!MMP_AVANCE_PCT` | 🔴 `VALIDACION_OK=NO` | única clave no validada del contrato |
| `H01 §M TBL_CALIBRACION_Ci` | poblada (25) | el "Motor Ci pendiente" histórico **ya está construido** (A189:A213) — contrario a notas viejas |

### 3.4 Hojas incompletas (4 · del surface dump, confirmadas)
| Hoja | pobl/filas | Naturaleza |
|---|---|---|
| `H65_CIUDADANO_IN_PRESUPUESTO` | 13/60 | entradas ciudadanas (QUIRA Ciudadana) — esqueleto |
| `H66_CIUDADANO_IN_PAC` | 13/60 | idem |
| `H67_CIUDADANO_IN_POA` | 13/60 | idem · alimentan `H68_MOTOR_CONGRUENCIA_EXTERNA` (que no sale a nadie) |
| `H34b_MFN_FIDELIDAD_NARRATIVA` | 21/202 | matriz de fidelidad narrativa (filas reservadas) |

---

## 4 · DISCREPANCIAS ENTRE FUENTES (deliverable #5)

### 4.1 Ti de las 4 entidades — eSIGEF (motor) vs SERCOP (H90)
Todas las cifras citadas: `H07b` (raw/norm), `H12!F` (lo que usa el motor), `H90!D` (SERCOP certificado).
| Entidad | eSIGEF raw 2026 | `Ti_norm` (motor H12!F) | **SERCOP `H90!D`** | Lectura |
|---|---|---|---|---|
| GAD | 6.43 % (`H07b!B19`) | 19.30 % (`F` GAD = `H07b!B20`) | **11.20 %** (`D4`) | norm > SERCOP (FactorTemporal infla) · denom. distinto (7+8 vs total) |
| Patronato | 13.91 % (`H07b!C19`) | 41.72 % (`F10/F15`) | **19.56 %** (`D5`) | **norm DUPLICA a SERCOP** |
| EP Aseo | ~24.1 % | 72.48 % (`F11/F20/F30`) | **18.17 %** (`D6`) | **norm CUADRUPLICA a SERCOP** |
| Bomberos | ausente → 0 | **0** (`F18`) | **19.43 %** (`D7`) | motor en 0 por fuente vacía |

> Doble causa: (1) **ruteo** — el motor lee Ti de eSIGEF (H07_S5/H07b), que NO tiene a Bomberos; (2) **normalización** — `Ti_norm = MIN(1, raw / (mes/12))` con mes≈4 multiplica ×3 el raw, inflando entes con algo de ejecución y dejando en 0 al que tiene fuente vacía. H90 (SERCOP) tiene los 4 con "Cédula oficial SERCOP Q1-2026". **Decisión pendiente de Javo: fuente canónica eSIGEF vs SERCOP** (sobre copia, INPUT, jamás `B33`).

### 4.2 Brecha rural — 3 cifras para el mismo concepto
| Origen | Valor | Fórmula |
|---|---|---|
| `H73!B59` (BRECHA_RURAL_USD) | **1,371,051** | `H99!B60 - SUMIF(...Z7:Z13)` |
| `H99!B60` | **1,371,051** | idem (vivo) |
| `H97!V-14` (C19) | **7,467,194** | `SUM(Z8:Z13)` "subinversión confirmada" |
| `H97!V-14` nota esperada (E19) | 1,791,935 | "Total rural esperado" |
→ Inconsistencia **interna del archivo vivo**, originada por la reclasificación territorial parcial (§6): se actualizó `B60`/`B59` pero la columna `Z` que lee `V-14` quedó con el cálculo anterior.

### 4.3 Lente temporal del ICPI (no es discrepancia, es diseño)
`ICPI 2026 = 17.45 %` (parcial Q1, `H12!B33`) vs `ICPI 2025 = 69.93 %` (anual, `H07b!B25`). El TGI usa el **anual** (`H98!D21=69.93`) ⇒ TGI 66.79 "sano". El semáforo AVEP (`H01!A29`: <0.20=🔴) se calibró para valor **anual** → aplicado al parcial da "Ruptura" falsa.

---

## 5 · DIFF Canónico VIVO vs FREEZE (deliverable #6)

`vivo` (2026-05-30) vs `FREEZE_20260526`. Ambos **123 hojas, ninguna exclusiva**. **79 hojas con diferencias**, pero la inmensa mayoría es **cosmética** (sello `F1`/`I1` `2026-05-29 → 2026-05-26` y sufijos de fecha en IDs de `H76`). Detalle: [`_FREEZE_DIFF.md`](gm_dumps/_FREEZE_DIFF.md).

**Deltas SUSTANTIVOS (los únicos que importan):**
| Hoja | Cambio vivo (vs freeze) | Lectura |
|---|---|---|
| `H06_S4_CONTRATACIÓN_SERCOP` | **+9,057 celdas** solo en vivo (`A65+`) | carga masiva de contratos SERCOP post-freeze |
| `H99_ENGINE_CORE` | `C8:C12 Urbana←Rural` · `A23 NBI_PARROQUIAS_PROM←NBI_RURAL_PROM` · `B57 67.2←66.79` · `B60 1,371,051←7,467,194` · `F23/F52` "7 parroquias (1 rural+6 urb)"←"6 rurales" | **reclasificación territorial** de 5 parroquias |
| `CAPA_TERRITORIAL_MONTECRISTI` | `D4:D9 Urbana←Rural` | misma reclasificación |
| `SCHEMA_TERRITORIOS` | `C3:C7 Urbana←Rural` · `F3:F4` "urbana"←"rural" | misma reclasificación |
| `H43_MOTOR_TERRITORIAL_CONSOLIDA` | `D8:D13 Urbana←Rural` · `B8 GEO_MNT_0007←GEO_MNT_P06` | misma reclasificación + cambio de id |
| `H73_OUTPUT_API` | `B59 1,371,051←7,467,194` | refleja la nueva brecha rural |
| `H10_S8_PARTICIPACIÓN_CPCCS` | 28 celdas (`D18/D19` RDC, `B47/B49` notas) | actualización CPCCS/RDC |

> El vivo introdujo una **reclasificación Rural→Urbana** coordinada en 4 hojas territoriales + recargó SERCOP. Esa reclasificación es la que dejó la **brecha rural inconsistente** (§4.2): bajó de 7.47 M (freeze) a 1.37 M en `H99!B60`/`H73!B59`, pero `H97!V-14` (col `Z`) sigue en 7.47 M.

---

## 6 · FICHAS POR HOJA (123 · agrupadas G1–G7) — deliverable #1

> `Estado` = pobladas/filas (del value-pass). `Lee de` / `Alimenta` = aristas **clave** de fórmula (omitidos `H00` navegación y banner `ROUND(H12!B33)`; grafo crudo completo en `gm_dumps/_INDEX.md`). `f=` nº de fórmulas.

### G1 · Configuración / Paramétrico / Diccionarios
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| H00_ÍNDICE | 148/158 | Índice + hipervínculos de navegación | (todas) | (todas) | navegación · f=124 |
| H01_PARÁMETROS | 259/284 | **Parámetros maestros**: AVEP (A29), pesos TGI, ISP_META, §M `TBL_CALIBRACION_Ci` (A189:G213), §O adscritas | H11b | H12, H99, ~todas | **raíz de Ci/umbrales** · A28 #NAME? falso-pos · f=89 |
| H02_GLOSARIO_QUIRA | 94/96 | Glosario términos | — | — | doc · f=5 |
| H02b_ORGÁNICO_CLASIFICADOR | 56/62 | Clasificador orgánico (direcciones) | H01 | H39 | insumo IED · f=19 |
| H36b_LOOKUP_ARRASTRE | 41/44 | Lookup histórico (arrastre 2023-25) | — | H39 | base histórica Ti · f=8 |
| H36c_OBSIDIAN_MAP | 58/62 | Mapa de celdas→Obsidian KB | H98, H99 | — | export · **C13 #REF! real** · f=20 |
| H40_PROTOCOLO_INGESTA | 25/35 | Protocolo de ingesta documental | — | — | doc/control · f=3 |
| H64_SELECTOR_PROTOCOLO_MODO | 27/31 | Selector de modo de protocolo | H01 | — | control · f=9 |
| H77_DATA_DICTIONARY | 19/19 | Diccionario de datos | — | — | doc · f=1 |
| H80_MODEL_REGISTRY | 9/10 | Registro de versiones del modelo | — | — | gobernanza · f=1 |
| H82_CONFIG_PARAMS | 23/24 | Config (PERIODO_CORTE, VERSION) | — | **H73** | publica meta-datos · f=1 |
| MATRIZ_CANONICA | 83/83 | **ADN compartido** Excel↔QUIRA | — | — | puente ontológico · f=1 |
| ÍNDICE_ECIAP | 95/97 | Índice ECIAP | — | — | doc · f=92 |
| SCHEMA_METADATA | 46/47 | Metadatos de esquema | — | — | doc · f=1 |
| SCHEMA_DICCIONARIO | 42/43 | Diccionario de esquema | — | — | doc · f=1 |
| SCHEMA_REGLAS | 35/39 | Reglas de validación | — | — | doc · f=1 |
| SCHEMA_ECIAP_BRIDGE | 18/19 | Puente ECIAP | — | — | doc · f=1 |
| RC_CHANGELOG | 14/14 | Changelog RC | — | — | gobernanza · f=0 |
| COMPILER_LOG | 19/20 | Log de compilación | — | — | gobernanza · f=1 |

### G2 · Fuentes (S0–S9 + datos territoriales)
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| H03_S1_ELECTORAL_CNE | 82/86 | S1 Plan de campaña / CNE | H01 | H16_IFE, H63 | base IFE · f=12 |
| H04_S2_PLANIFICACIÓN_PDOT | 40/43 | S2 PDOT (metas/programas) | H01 | H05,H06,H08,H10,H11,H12d,H15,H17,H25,H31,H32,H39,H71 | **hub de planificación** · f=10 |
| H04b_DIAGNÓSTICO_SOCIAL | 38/44 | Diagnóstico social | H12b_IBSC | H12b_IBSC, H16c_PSG | insumo PSG · f=52 |
| H05_S3_OPERATIVO_POA | 37/42 | S3 POA | H04 | H05b, H19, H21b, H28 | base ISP/PAC · f=121 |
| H05b_S3b_PAC_CONTRATACIÓN | 44/49 | S3b PAC | H05 | H21b | coherencia PAC · f=84 |
| H06_S4_CONTRATACIÓN_SERCOP | 830/837 | S4 SERCOP (contratos) | H04 | H21b | **+9,057 vs freeze** · f=58 |
| H07_S5_FINANCIERO_eSIGEF | 37/88 | **S5 eSIGEF** — zona cruda de pegado (A46+) | H07b | H07b,H16b,H16c,H19,H20c,H22,H23,H24,H26,H27,H33,H42,H85 | **zona cruda 2026 VACÍA** · f=14 |
| H07b_Ti_INVERSIÓN_eSIGEF | 27/30 | **Ti serie 2023-26 + Ti_norm (B20)** | H07_S5 | **H12, H98, H99**, H37, H73, H85, H97 | **fuente del Ti del ICPI** · f=14 |
| H07c_Ti_VERIFICADO_INFORME | 32/61 | Ti verificado por informe | H01 | H20c, H21b, H25, H27, H39 | conciliación Ti · f=12 |
| H08_S6_AUTOREPORTE_SIGAD | 39/44 | S6 SIGAD autorreporte | H04 | **H12**, H15, H21 | insumo motor · f=33 |
| H09_S7_TRANSPARENCIA_LOTAIP | 57/63 | S7 LOTAIP transparencia | H01 | H18_ITAM, H76 | base ITAM/IOC · f=8 |
| H10_S8_PARTICIPACIÓN_CPCCS | 45/51 | S8 CPCCS participación | H04 | H20b, H31, H33, H85 | base IGP · 28 celdas vs freeze · f=29 |
| H10b_S8b_PARTICIPATIVO | 40/203 | S8b Presupuesto participativo | H01 | H20b, **H73**, H85 | base IGP · f=13 |
| H10c_RDC_APORTES | 132/134 | Aportes RDC (rendición) | — | — (índice) | datos RDC · f=0 |
| H11_S9_AGENDA_GLOBAL_ODS | 39/44 | S9 ODS/Agenda 2030 | H04 | H20_ICODS, H32, H69, H89 | base ICODS · f=32 |
| H11b_MONITOR_POLITICAS_PUBLICAS | 41/47 | Monitor de políticas | H04 | H01, H20, H69 | insumo ODS/fondos · f=35 |
| H63_S0_CNE_TRAZABILIDAD | 81/83 | S0 trazabilidad CNE | H03 | H85 | trazabilidad · f=13 |
| H90_PRESUPUESTO_CONSOLIDADO_202 | 74/80 | **Presupuesto 4 entes (SERCOP Q1)** | — | **H73**, H_HOLDING | **fuente Bomberos 19.43%** · f=6 |
| H_HOLDING_CEDULAS_2026 | 30/35 | Cédulas mensuales 2026 | H90 | — | serie mensual · f=12 |
| H_ORGANICO_040_2025 | 120/125 | Orgánico Res.040-2025 | — | — | base IED (11 direcc.) · f=0 |
| KB_DIAGNOSTICO_PDOT | 1571/1578 | KB estructurado del PDOT | — | — | corpus territorial · f=1 |
| POA_GEOREFERENCIADO | 2090/2701 | POA georreferenciado | H01 | — | datos GeoTwin · f=2 |
| PAC_2026_GEOREFERENCIADO | 216/217 | PAC 2026 georreferenciado | H01 | — | datos GeoTwin · f=2 |
| CAPA_TERRITORIAL_MONTECRISTI | 23/24 | Capa territorial | H01 | — | **D4:D9 reclasif. vs freeze** · f=2 |
| SCHEMA_TERRITORIOS | 76/76 | 7 parroquias (urbano/rural) | — | — | **reclasif. vs freeze** · f=0 |
| SCHEMA_NBI | 83/90 | NBI por territorio | — | **H73** | base D4/Composite_Need · f=1 |
| SCHEMA_METAS | 59/60 | Metas estructuradas | — | — | datos · f=1 |
| SCHEMA_PROYECTOS | 147/148 | Proyectos | — | — | datos · f=1 |
| SCHEMA_ORGANICO | 91/95 | Orgánico estructurado | — | — | datos · f=1 |
| SCHEMA_CNE | 19/22 | CNE estructurado | — | — | datos · f=1 |
| SCHEMA_RIESGOS | 42/43 | Catálogo de riesgos | — | — | datos SAT · f=1 |
| H65_CIUDADANO_IN_PRESUPUESTO | 13/60 | Entrada ciudadana presupuesto | H01 | H68 | 🟡 INCOMPLETA · f=7 |
| H66_CIUDADANO_IN_PAC | 13/60 | Entrada ciudadana PAC | H01 | H68 | 🟡 INCOMPLETA · f=7 |
| H67_CIUDADANO_IN_POA | 13/60 | Entrada ciudadana POA | H01 | H68 | 🟡 INCOMPLETA · f=7 |

### G3 · Motor ICPI + Dimensiones TGI
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| **H12_MOTOR_ICPI_CANÓNICO** | 40/40 | **Motor ICPI** (25 metas × 6 factores · B33) | H07b(Ti), H13(Vi), H14(Pi/Ri), H01(Ci), H08, H25 | H15, H73, H12b/c/d, +consumidores | ★ **B33 INMUTABLE** · 5 metas Ti=0 · Pi hardcoded · f=233 |
| H12b_ICPI_ACUMULADO | 21/23 | ICPI acumulado Q1 (0.2367) | H12 | **H73** | lente acumulada · f=10 |
| H12b_MOTOR_IBSC | 39/43 | Motor IBSC (bienestar social) | H04b, H14 | H04b | índice paralelo · f=154 |
| H12c_ICPI_HISTÓRICO_ANUAL | 16/19 | ICPI anual 2023-25 | H01, H12 | — | serie histórica · f=16 |
| H12d_ICPI_POR_ENTIDAD | 19/24 | ICPI por entidad | H04 | H17, H19b, H28 | desglose · f=47 |
| H13_VARIABLES_Vi | 73/81 | **Vi** (variable/avance por meta) | — | **H12** | factor Vi · f=28 |
| H14_PONDERADORES | 33/36 | **Pi/Ri** ponderadores | — | **H12**, H12b, H35, H37, H39 | factor Pi/Ri · ⚠️ S-04 · f=31 |
| H15_ICPI_GLOBAL | 47/53 | ICPI global (valida/expande B33) | H04, H08, H12 | H39 | consumidor real de B33 · f=165 |
| **H98_TGI_FRAMEWORK** | 50/60 | **Marco TGI** (D1-D5 · B25=66.79) | H01, H07b, H99 | **H73**, H36c | motor TGI · D2=ICPI anual · f=18 |
| **H99_ENGINE_CORE** | 55/63 | Núcleo parroquial (NBI/IRS/IET/CN · 7 parroquias) | H01, H07b | **H98, H73**, H97, H36c | motor territorial · reclasif. vs freeze · f=107 |

### G4 · Índices compuestos
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| H16_IFE | 16/19 | Índice Fidelidad Electoral (72.73%) | H03 | H28, H33, H39, **H73**, H85 | → H73 IFE · f=8 |
| H16b_IPE | 11/13 | Índice Planif. Estratégica | H07_S5 | H28 | f=9 |
| H16c_PSG_PRESUPUESTO_GENERO | 15/19 | PSG presupuesto género (2.83%) | H01, H04b, H07_S5 | H28, **H73** | → H73 PSG · f=8 |
| H17_IED | 22/25 | Índice Ejecución por Dirección (16.5%) | H04, H12d | H28, H29, H30, **H73**, H85 | → H73 IED · f=51 |
| H18_ITAM | 17/20 | Transparencia/Acceso (82.29%) + IOC | H09 | H28, H33, **H73** | → H73 ITAM/IOC · f=5 |
| H19_ICS_ISP | 12/14 | Inversión Salud Presup. (3.22%) | H01, H05, H07_S5 | H28, **H73** | → H73 ISP · f=10 |
| H19b_IE_EP_EA | 10/12 | Ejecución EP/EA | H12d | H85 | adscritas · f=12 |
| H20_ICODS | 20/22 | Cumplimiento ODS (0.875) | H11, H11b | H28, H32, **H73** | → H73 ICODS (d13) · f=7 |
| H20b_IGP_GOBERNANZA_PARTIC | 11/13 | Gobernanza participativa | H10, H10b, H34b | H28, **H73**, H85 | → H73 IGP · f=8 |
| H20c_IEF_EFICIENCIA_FINANCIERA | 34/55 | Eficiencia financiera (6.19%) | H01, H07_S5, H07c | H27, H28, H29, H31, H39, **H73** | → H73 IEF · f=18 |
| H30_IED_POR_DIRECCIÓN | 30/35 | IED desglosado por dirección | H17 | — | detalle IED · f=49 |
| H41_IOC_OPACIDAD_CRITICA | 23/27 | Opacidad crítica | H01 | — | IOC detalle · f=4 |
| H42_IET_EQUIDAD_TERRITORIAL | 31/37 | Equidad territorial (Gini 0.927) | H07_S5 | **H73**, H75, H89 | → H73 IET · f=12 |
| H43_MOTOR_TERRITORIAL_CONSOLIDA | 34/37 | Consolida territorial (GPS 7 parroquias) | — | **H73** | reclasif. vs freeze · f=0 |
| H68_MOTOR_CONGRUENCIA_EXTERNA | 19/23 | Congruencia ciudadana externa | H65, H66, H67 | — | 🟡 inputs incompletos · sin salida · f=20 |
| ANÁLISIS_TENDENCIA_TERRITORIAL | 25/27 | Tendencia territorial | H01 | — | análisis · f=2 |

### G5 · SAT (alertas) + MMP (metas)
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| H21_SAT-I | 25/31 | Fragmentación selectiva | H01, H08, H25 | H28, **H75** | f=18 |
| H21b_SAT-0_COHERENCIA_PAC | 25/32 | Coherencia POA-PAC | H05, H05b, H06, H07c | H28, **H75** | f=14 |
| H22_SAT-II | 17/28 | Reforma significativa tardía | H01, H07_S5 | H28, **H75** | f=10 |
| H23_SAT-III | 15/19 | Parálisis presupuestaria | H01, H07_S5 | H28, **H75** | f=14 |
| H24_SAT-IV | 15/20 | Alerta fiscal COOTAD | H01, H07_S5 | H28, **H75** | f=10 |
| H24b_SAT-V_ALERTA_CPCCS | 17/22 | Brecha compromiso CPCCS | H01 | H28, H31, **H75** | f=9 |
| H24c_SAT-VI_DESVÍO_PP | 18/23 | Desvío presupuesto participativo | H01 | H28, **H75** | f=9 |
| H75_SAT_ENGINE | 14/14 | **Motor SAT** (RIESGO_TOTAL 0.2 · MEDIO) | H21..H24c, H25, H42 | **H73**, SAT_Catalogo | agrega SAT · f=34 |
| SAT_Catalogo | 26/31 | Catálogo SAT (v6.0) | H73, H75 | — | doc SAT · f=5 |
| H25_MMP_MENSUAL | 39/41 | Metas MMP mensual | H01, H04, H07c | **H12**, H21, H26, H75, H89 | insumo motor · f=237 |
| H26_MMP_TRIMESTRAL | 43/51 | MMP trimestral | H01, H07_S5, H25 | H27 | f=328 |
| H27_MMP_ANUAL | 61/68 | MMP anual | H07_S5, H07c, H20c, H26 | — | f=164 |

### G6 · Salidas / Reportes / API
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| **H73_OUTPUT_API** | 65/65 | **Contrato de salida (65 claves)** | 24 hojas (índices) | SAT_Catalogo | **lo que LEE el conector** · MMP_AVANCE NO · f=60 |
| H28_RESUMEN_EJECUTIVO | 40/42 | Resumen ejecutivo (agrega 20 hojas) | H12, H16..H24c | H29, H31 | hub de reporte · f=40 |
| H29_TABLERO_ALCALDE | 44/50 | Tablero del alcalde | H12, H17, H20c, H28 | — | dashboard · f=56 |
| H31_REPORTE_CPCCS | 58/65 | Reporte CPCCS | H04,H10,H12,H20c,H24b,H28 | — | reporte · f=148 |
| H32_REPORTE_ODS_BILATERALES | 42/45 | Reporte ODS bilaterales | H04, H11, H12, H20 | — | reporte · f=113 |
| H33_TAC_QUIRA_CIUDADANA | 18/21 | TAC ciudadana | H01,H07_S5,H10,H12,H16,H18 | — | reporte · f=14 |
| H34_CERTIFICADO_QUIRA | 21/24 | Certificado QUIRA | H01, H12 | — | salida · f=14 |
| H34b_MFN_FIDELIDAD_NARRATIVA | 21/202 | Fidelidad narrativa (MFN) | H12 | H20b, H39, H85, H89 | 🟡 INCOMPLETA · f=17 |
| H35_DATASET_ACADEMIA | 45/48 | Dataset académico | H01, H12, H14 | — | export · f=278 |
| H36_QUIRA_BRIDGE | 53/56 | Puente QUIRA (export) | H12 | — | export · f=3 |
| H37_SENSIBILIDAD_ESTRATÉGICA | 30/38 | Sensibilidad (what-if Pi/Ti) | H07b, H12, H14 | — | análisis · f=24 |
| H38_ALCANCE_PREVENTIVO | 19/23 | Alcance preventivo | H12 | — | reporte · f=3 |
| H69_ELEGIBILIDAD_FONDOS | 24/28 | Elegibilidad de fondos (portafolio $7.44M) | H01, H11, H11b, H12 | H85 | D02 cooperación · f=24 |
| H71_EP_ADSCRITAS | 27/32 | Radar EP/adscritas (Presunción Operativa) | H01, H04 | — | referencial · **B8 #REF!→0** · f=37 |
| H72_EP_BASE_LEGAL | 23/26 | Base legal EP | H12 | — | doc legal · f=25 |
| H86_REPORT | 69/78 | Reporte general | H89 | — | reporte · f=2 |
| H86b_ALGORITHMIC_GOVERNANCE_PRO | 41/50 | Gobernanza algorítmica | — | — | doc · f=1 |

### G7 · Gobernanza / Auditoría / Recovery
| Hoja | Estado | Propósito | Lee de (clave) | Alimenta (clave) | Rol / ⚠️ |
|---|---|---|---|---|---|
| H39_AUTOCONTROL_ECOSISTEMA | 36/39 | **Auto-control (24 checks)** | H01,H02b,H04,H07c,H12,H14,H15,H16,H20c,H34b,H36b | — | **D28 ERROR (Ci 1pp) · B30 ERRORES:1** · f=27 |
| H97_VALIDACIONES | 25/27 | **Validaciones internas (V-01..V-19)** | H01, H07b, H99 | — | V-14 brecha rural inconsist. · f=17 |
| H85_ALERTS_LOG | 49/54 | **Alertas + 13 CHK sincronía** | H01,H07_S5,H07b,H10,H12,H16,H17,H19b,H20b,H34b,H63,H69 | — | **D33 12OK/1WARN/0ERR** · CHK-08/12 pend · f=30 |
| H89_TRUST_SCORE | 27/32 | Trust score (89.6) | H11, H25, H34b, H42 | **H73**, H86 | → H73 TRUST · f=12 |
| H88_EVIDENCE_REGISTRY | 10/10 | Registro de evidencia (PAC publicado) | — | **H73** | → H73 PAC_PUBLICADO · f=1 |
| H74_RECOVERY_MAP | 25/25 | Mapa de recuperación | H12 | — | resiliencia · f=31 |
| H76_AUDIT_TRAIL | 30/31 | Pista de auditoría (IDs por meta) | H09 | — | 50 IDs c/fecha vs freeze · f=230 |
| H81_HASH_CHAIN | 21/21 | Cadena de hash | — | — | integridad · f=1 |
| H83_SOD_REGISTRY | 7/8 | Segregación de funciones | — | — | gobernanza · f=1 |
| H84_SNAPSHOT_REGISTRY | 8/9 | Registro de snapshots | — | — | gobernanza · f=1 |
| H87_RECOVERY_POLICY | 15/16 | Política de recuperación | — | — | doc · f=1 |
| H70_BITACORA_LOTAIP_OPACIDAD | 15/18 | Bitácora LOTAIP/opacidad | H12 | — | referencial · f=14 |
| H95_LIMITACIONES | 15/16 | Limitaciones declaradas | — | — | doc honesto · f=0 |
| H96_TRAZABILIDAD | 22/23 | Trazabilidad | — | — | doc · f=0 |
| LOG_EJECUCION | 36/38 | Log de ejecución | H01 | — | gobernanza · f=2 |

---

## 7 · ARTEFACTOS DURABLES (todos en `docs/architecture/`)
- [`gm_dumps/_INDEX.md`](gm_dumps/_INDEX.md) — índice de las 123 hojas (llenado · #fórmulas · #in/out · #err/marc).
- [`gm_dumps/_ANALYSIS.md`](gm_dumps/_ANALYSIS.md) — análisis compacto (errores/marcadores globales + dependencias + ficha por hoja).
- [`gm_dumps/_PROBE_VALUES.md`](gm_dumps/_PROBE_VALUES.md) — valores cacheados de motor/validaciones.
- [`gm_dumps/_FREEZE_DIFF.md`](gm_dumps/_FREEZE_DIFF.md) — diff vivo vs FREEZE.
- [`gm_dumps/<hoja>.md`](gm_dumps/) — **123 volcados de fórmulas** (1 por hoja).
- Previos: [`GM_H73_DUMP.md`](GM_H73_DUMP.md) · [`GM_SURFACE_DUMP.md`](GM_SURFACE_DUMP.md) · [`GM_SHEET_H12_MOTOR_ICPI.md`](GM_SHEET_H12_MOTOR_ICPI.md) · [`GM_SHEET_H07B.md`](GM_SHEET_H07B.md) · [`GM_SHEET_H90.md`](GM_SHEET_H90.md) · [`METODOLOGIA_GOLD_MASTER.md`](METODOLOGIA_GOLD_MASTER.md).

*Registro Integral del Gold Master · Dylus Lab © 2026 · 100 % determinista · la fórmula canónica `H12!B33` es INMUTABLE · este documento NO modificó el Excel.*
