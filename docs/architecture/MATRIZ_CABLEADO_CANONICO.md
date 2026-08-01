---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 4, 8]
  type: OPERATIVA
---

# MATRIZ DE CABLEADO CANÓNICO · Gold Master ↔ Silos ↔ DOM

**2026-07-29 · verificado celda a celda contra `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` (123 hojas)**

> **Por qué existe** *(Javo · 2026-07-29):* *"en el Excel se hace el análisis real del SERCOP, pero
> no aparece ya en los DOM… con los DOM desnaturalizamos el Excel."* La percepción era correcta y
> el diagnóstico también — pero la solución **no es reestructurar los DOM**.

---

## 0 · Lo que se encontró antes de construir nada

**El puente ya existe en el Gold Master.** No había que crearlo:

| Hoja | Qué es | Estado |
|---|---|---|
| **`H36_QUIRA_BRIDGE`** | *"Mapa de conectores"* · `Hoja_Excel │ Tabla_BD │ Clave_Primaria │ Relaciones_FK` · 56 filas | ✅ **existe, 95% sano** (2 de 38 referencias desajustadas) |
| **`H77_DATA_DICTIONARY`** | diccionario de datos con restricciones críticas | ⚠️ nombres truncados + 1 hoja inexistente |
| **`H13_VARIABLES_Vi`** | matriz `Meta × 4 verificadores` | ✅ **es el cruce intersistémico** |

Es la **quinta vez** que el canon ya contenía la respuesta. El Inventario funcionó para conceptos;
faltaba aplicar la misma disciplina al **motor**.

## 1 · S3 (POA) SÍ es silo de verificación — el Excel lo dice literal

Javo lo afirmó y `H13!B13` lo confirma palabra por palabra:

> *"V_POA (S3) **NO entra en el producto lógico Vi** — **S3 es verificador de programación, no de
> ejecución**. Los 4 verificadores activos de Vi son: V_SERCOP + V_eSIGEF + V_LOTAIP + V_CPCCS."*

**Ambas cosas son ciertas y no se contradicen:**

| | S3 · POA | S4/S5/S7/S8 |
|---|---|---|
| **Es silo verificador** | ✅ sí | ✅ sí |
| **Qué verifica** | **incorporación programática**: ¿el mandato se anualizó como programa/proyecto? | **ejecución**: contratación · devengo · publicidad · rendición |
| **Entra en `Vi`** | ❌ no | ✅ sí |

El error fue mío: dije *"el POA no verifica nada"*. Verifica **otra dimensión**.

### Y la fórmula que Javo escribió de memoria es exacta

`H13!B20`, carácter por carácter:

```
=SI(O(V_eSIGEF=0,V_SERCOP=0),0,SI(O(V_LOTAIP=1,V_CPCCS=1),1,0.5))
```

Con su justificación en `B21`: *"sin núcleo financiero = sin score"*. Vi = 0 si falta eSIGEF **o**
SERCOP; 1 si además hay LOTAIP **o** CPCCS; 0,5 si hay ejecución sin publicidad.

## 2 · La matriz verificada

| Silo | Hoja Gold Master | DOM | Verifica | Produce |
|---|---|---|---|---|
| **S1** | `H03_S1_ELECTORAL_CNE` | *d00 — no existe aún* | legitimidad de origen | `H16_IFE` |
| **S2** | `H04_S2_PLANIFICACIÓN_PDOT` | **d01** | alineación plurianual · 25 metas | `P_i` · `R_i` (`H14`) |
| **S3** | `H05_S3_OPERATIVO_POA` | **d01** | **incorporación programática** | `V_POA` · `SAT-0` |
| **S3b** | `H05b_S3b_PAC_CONTRATACIÓN` | **d03** | programación de compras | `SAT-0` coherencia POA-PAC |
| **S4** | `H06_S4_CONTRATACIÓN_SERCOP` | **d03** | legalidad y adjudicación | **`V_SERCOP`** ★ 850 filas |

| **S5** | `H07_S5_FINANCIERO_eSIGEF` | **d02** | ejecución presupuestaria | **`V_eSIGEF`** · `T_i` |
| **S6** | `H08_S6_AUTOREPORTE_SIGAD` | *d06 — no existe aún* | autoreporte vs evidencia | brecha `ICM − ICPI` · **`SAT-I`** ★ |
| **S7** | `H09_S7_TRANSPARENCIA_LOTAIP` | **d07** | publicidad activa | **`V_LOTAIP`** · `H18_ITAM` |
| **S8** | `H10_S8_PARTICIPACIÓN_CPCCS` | **d09** | rendición · imputabilidad | **`V_CPCCS`** · `C_i` |
| **S8b** | `H10b_S8b_PARTICIPATIVO` | **d08** | presupuesto participativo | `IGP_2` · `SAT-VI` |
| **S9** | `H11_S9_AGENDA_GLOBAL_ODS` | *d05 — no existe aún* | vinculación ODS | `H20_ICODS` |

> ⚠️ **Corrección 2026-07-29 (Javo · OBS-023):** `SAT-I` *"Fragmentación Selectiva"* estaba
> mapeada aquí a **d03** por su nombre. **Es de S6 (SIGAD)**: su base legal es COPFP Art. 54
> (reportar *todas* las metas al SIGAD) y su métrica es `ICM_Global >= 80% AND
> pct_metas_reportadas <= 10%`. No mide fragmentación de contratos: mide **fragmentación del
> reporte** — calificación alta sobre un universo mínimo de metas.

> ⚠️ **Precisión sobre la propuesta original:** `d00`, `d05` y `d06` **no existen** en
> `app/agents/`. Hoy hay seis: d01·d02·d03·d07·d08·d09. **Tres silos del motor no tienen dominio
> que los cure** — S1 electoral, S6 SIGAD y S9 ODS. Eso es un hallazgo, no un error de la matriz.

## 3 · Respuesta a *"¿es de cablear todo sin excepción?"*

**Sí — y en una sola dirección**, que es la que las Reglas 1 y 9 ya imponen:

```
   GOLD MASTER (motor · fórmula canónica H12!B33)
         │
         ▼
   SILOS S1..S9  (verificadores · H13)
         │
         ▼
   DOM  (curación documental · PCD)
         │
         ▼
   QUIRA  (ingesta · trazabilidad · UI)
```

**Nunca al revés.** Si un DOM deja de corresponder con su silo, ocurre exactamente lo que Javo
percibió: la implementación documental se desvía del modelo matemático.

**Regla que se deriva — R-G:** *todo DOM declara explícitamente qué silo alimenta, qué variable
del ICPI produce y qué hojas del Gold Master consume.* Sin esa declaración, un dominio no puede
cerrarse con PCD.

## 4 · Desajustes detectados (a subsanar en el Excel)

| Hoja | Fila | Dice | Real |
|---|---:|---|---|
| `H36_QUIRA_BRIDGE` | 9 | `H05_S3_COMPETENCIAS_COOTAD` | `H05_S3_OPERATIVO_POA` |
| `H36_QUIRA_BRIDGE` | 14 | `H13_S6_VERIFICACIÓN` | `H13_VARIABLES_Vi` *(y S6 es SIGAD, no Vi)* |
| `H77_DATA_DICTIONARY` | 15 | `QUIRA_OS_SYNC` | **la hoja no existe** |

El bridge está **95% sano** (36 de 38 referencias correctas). Son correcciones de nomenclatura,
no de estructura — **no tocan ninguna fórmula**.

## 5 · Conclusión: no se reestructuran los DOM

| Opción | Costo | Veredicto |
|---|---|---|
| Reestructurar DOM a S1..S9 | rompe 4 PCD cerrados · re-curación completa | ❌ |
| **Cablear los DOM existentes a sus silos** | 1 documento + 3 correcciones de nomenclatura | ✅ |

Los DOM **sí mapean** a los silos. Lo que faltaba era **hacer el mapeo explícito y verificable**,
que es esta matriz. La preocupación de Javo era correcta; la solución es una fracción del costo
que temía.

**Lo que sigue faltando de verdad:** la **vista por meta** (`Meta × V_SERCOP × V_eSIGEF ×
V_LOTAIP × V_CPCCS`) en QUIRA. Existe en `H13` y no se expone. Ahí es donde SERCOP "desaparece"
para el usuario — no en los DOM.

---
*Matriz de Cableado Canónico · Dylus Lab © 2026 · verificada contra el Gold Master v5.5.*
