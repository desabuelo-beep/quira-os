# GM-Ω · ICPI — RECONCILIACIÓN META A META  `008-R`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/reconciliacion_metas.py`. El catálogo de trabajo queda en `data/pdot/catalogo_reconciliacion_66.json`.

> ### La regla de 008-R
> **No reconciliar por parecido textual solamente.** Primero identidad literal; después correspondencia semántica controlada; y todo caso dudoso queda `AMBIGUA` — **nunca forzado a una coincidencia**. Un catálogo con ambigüedades declaradas es utilizable; uno con coincidencias inventadas, no.

## 1 · La cadena de procedencia, reconstruida

```
Portal GAD · Transparencia (LOTAIP) · sección PDOT
  └── PDF publicado                    ← ORIGINAL OFICIAL
        └── Word · conversión propia   ← derivado fiel del PDF
              └── Excel · tabulación   ← insumo de trabajo · 66 metas
```

| Artefacto | SHA256 | Papel |
|---|---|---|
| `PDOT GAD Montecristi 2023-2027.pdf` | `3810ad062903138f…` | original publicado en el portal |
| `PLAN PLURIANUAL DE INVERSIONES GAD Montecristi` | `02996b6d2c4ee108…` | conversión propia del PDF |
| `Plan Plurianual PDOT 2023-2027 GAD Montecristi` | `09a2aaccca4bc90d…` | tabulación de trabajo · fuente de las 66 |

⚠️ **Esta cadena costó TRES rectificaciones**, y la lección vale más que el dato. Se fue preguntando por atributos sueltos —«¿es oficial?»— en vez de reconstruir la cadena entera, y cada respuesta parcial produjo una etiqueta que hubo que volver a corregir: primero se aceptó «no oficial», luego se cambió a «OFICIAL» aplicándolo al archivo equivocado, y sólo a la tercera apareció que lo publicado es el PDF, el Word es su conversión y el Excel una tabulación.

> **Un artefacto no se clasifica por un atributo: se clasifica por su cadena.**

## 2 · Escalón 7 · ¿la tabulación corresponde a lo publicado?

De las **66 metas** del Excel, **41** se localizan en el texto del documento publicado (Word (conversión del PDF del portal)).

🔴 **La correspondencia es baja.** Antes de usar esta tabulación como universo documental hay que explicar la diferencia.

## 3 · ★ EL HALLAZGO · el motor AGREGA, no selecciona

La reconciliación por palabras daba **7 de 66** y parecía un problema de calidad de datos. No lo era. Al mirar un caso concreto apareció otra cosa:

```
Gold Master · SC-I-N-01
  «Agua potable: cobertura 39.25%→42.38%; calidad 100% INEN 1108;
   infraestructura BUENA 22.74%→41.64%»

PDOT · TRES metas distintas
  «Aumentar del 39.25% al 42.38% la cobertura de agua potable…»
  «Mejorar el índice de la calidad del agua al 100%…»
  «Mejorar el índice de calidad de la infraestructura BUENO de
   22.74% al 41.64%…»
```

> **El Gold Master no seleccionó 25 metas de 66: agregó las 66 en 25.**

Y las **cifras lo prueban**: viajan intactas del PDOT a la celda del motor. Cambiando la señal de emparejamiento de palabras a cifras, las reconciliadas pasaron de **7 a 25** y las no encontradas de **46 a 1**.

### Qué invalida esto

| Se venía diciendo | Lo que es |
|---|---|
| `25 ⊂ 66` · subconjunto | **`25 = agregación de 66`** · mapeo N:1 |
| `66 − 25 = 41` metas excluidas | **la resta no describe nada** |
| «cobertura del 37,88 %» | **una meta operacional puede cubrir varias documentales** |
| «41 metas fuera del universo» | **no hay partición que hacer** |

**La pregunta de 008-R estaba mal planteada** —y no por quien la formuló: la suposición de subconjunto la compartíamos todos, incluido `ADR-036`, que dice «las 25 existen todas en el PDOT». Sigue siendo cierto, pero con un matiz que cambia su alcance: existen **como agregación de sus metas**, no como selección literal de 25 de ellas.

⚠️ Y esto **no contradice el criterio que Javo declaró** —mayor monto económico—: se agregaron las metas de los proyectos de mayor peso. Lo que cambia es la aritmética con la que se describía el resultado.

## 4 · La reconciliación 66 ↔ 25, con la señal correcta

| Estado | Metas |
|---|---:|
| ✅ RECONCILIADA | 25 |
| ⚠️ AMBIGUA | 40 |
| ⬜ NO_RECONCILIADA (fuera del universo v1) | 1 |
| **Total** | **66** |

De las reconciliadas, **0 por identidad literal** y **25 por correspondencia semántica controlada** — estas últimas con su score declarado, para que puedan revisarse una a una.

⚠️ **19 IDs del motor no encontraron su meta en el PDOT**: `SC-L-N-02`, `AH-I-X-01`, `AH-I-X-02`, `AH-I-X-03`, `AH-I-N-01`, `AH-I-X-04`, `PI-I-G-01`, `AH-C-X-01`, `AH-C-X-02`, `SC-I-N-03`, `FA-I-X-01`, `FA-C-X-01`, `FA-I-X-02`, `PI-I-G-02`, `PI-L-G-01`, `EP-L-X-01`, `FA-CC-01`, `AH-AP-04`, `FA-DIS-01`

Bajo el modelo de **agregación** esto se lee distinto: no significa que falten en el PDOT, sino que **este cruce no consiguió atribuirles sus metas de origen**. Una meta operacional cuyas componentes no se identifican es precisamente lo que v2 no puede heredar sin resolver.

### Reparto por sistema

| Sistema | Sin reconciliar | Total | % |
|---|---:|---:|---:|
| 1. FIS AM | 1 | 9 | 11 % |
| 2. ASEN | 0 | 26 | 0 % |
| 3.SOC | 0 | 13 | 0 % |
| 4. EC | 0 | 5 | 0 % |
| 5. INST | 0 | 13 | 0 % |

## 5 · Por qué el catálogo de exclusiones tiene 50

- Entradas en `metas_fuera_del_motor.json`: **50**
- De ellas presentes en las 66 del Plan Plurianual: **10**
- Entradas duplicadas por texto: **1**

⚠️ **40 entradas del catálogo de exclusiones NO están en las 66.** El catálogo describe un universo distinto del Plan Plurianual — probablemente otra versión del PDOT, o un conteo que incluye proyectos y actividades además de metas.

**Ésa es la explicación del `50` que 008 no podía dar**, y confirma que la resta `66−25=41` no describía a esas 50. Los dos catálogos nunca fueron complementarios.

## Lo que 008-R entrega, y lo que deja abierto

**El objetivo original NO se alcanzó, y ésa es la conclusión.** Se buscaba la partición `66 → 25 + 41`. No existe: el motor **agrega**, no selecciona, así que no hay 41 metas excluidas que identificar. La pregunta era irresoluble tal como estaba planteada, y demostrarlo vale más que la tabla que se esperaba.

**Lo que sí entrega:**

- La **cadena de procedencia** con SHA256 de los tres artefactos, y el escalón 7 medido meta a meta.
- **La naturaleza real de la relación**: `25 = agregación de 66`, probada con las cifras que viajan del PDOT a la celda del motor.
- **La explicación del `50`**: sólo 10 de esas 50 entradas pertenecen a las 66. Los dos catálogos nunca fueron complementarios.
- El catálogo `catalogo_reconciliacion_66.json` con **25 correspondencias** y **40 ambigüedades declaradas** — base de trabajo para v2.

**Lo que deja abierto, a propósito:**

- **40 metas AMBIGUAS.** No se fuerzan: cada una necesita ojo humano contra el documento. Un catálogo con ambigüedades declaradas es utilizable; uno con coincidencias inventadas, no — y afinar más el algoritmo habría empezado a producir las segundas.
- **19 metas operacionales sin componentes atribuidas.** Es lo que v2 no puede heredar sin resolver.
- **El escalón 7 no está cerrado**: 41 de 66 se localizan literalmente en el documento publicado. El resto exige revisar esas metas concretas — la conversión PDF→Word altera saltos y guiones, y la comparación es literal.

### La consecuencia para v2, que es lo que 008-R venía a preparar

**El Gold Master no conserva el texto de las metas del PDOT, sólo un resumen agregado.** Por eso ninguna reconciliación posterior puede ser automática, y por eso ésta llegó hasta donde llegó.

Para v2, cada meta operacional debe guardar **el texto íntegro de cada meta documental que agrega, con su localización** (sistema · fila · SHA del documento). No es un requisito de comodidad: sin él, el universo ampliado nacería con la misma deuda de trazabilidad que esta auditoría acaba de medir — y en un sistema cuyo objeto **es** la trazabilidad.

- **No se amplía 25 → 66.** Sigue siendo `ADR-036 §4`: versión nueva, recalibración y ADR propio, después de `011`.

---
*GM-Ω-ICPI-008-R · 66 metas documentales · 25 reconciliadas · 40 ambiguas · el Gold Master no se modificó · Dylus Lab © 2026*
