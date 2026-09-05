# QUIRA-NEXT · CARTA DE REARQUITECTURA

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/carta_rearquitectura.py`. El **inventario** se cuenta del repositorio; las **categorías y los ejes** se declaran, porque son un juicio de dirección.

> ### Qué es esto
> El plan del **refactor integral de fondo y forma de todo el ecosistema** — desde el Excel hacia adelante. **No ejecuta nada.** Ordena qué existe, en qué categoría cae cada pieza, y qué se puede decidir hoy.

⚠️ **El Gold Master sigue congelado hasta `011-C4`.** Planificar el refactor **no adelanta** el momento de intervenir el motor. Y el baseline **27,4582 %** no se mueve.

## Por qué existe esta carta

Javo, 2026-09-05:

> *«Lo histórico no es la verdad absoluta o una camisa de fuerza que se deba continuar […] esto merece una planificación integral para hacerlo bien, sin dañar lo que es válido.»*

### ⚠️ Y la prueba de que hacía falta la dio esta dirección en el acto

Ante el ejemplo *«quitar la palabra auditoría de la documentación»*, esta dirección **empezó a ejecutarlo** en vez de leerlo como lo que era: una muestra del NIVEL del refactor. Javo lo detuvo.

Lo medido antes de parar:

```
  «auditoría» →  609 ocurrencias  ·  233 archivos
```

Y **no son la misma palabra**:

| Uso | Ejemplo | Tratamiento |
|---|---|---|
| **auditoría CGE / Contraloría** | «observación formal de auditoría CGE», `NCI 406-01` | ⚖️ **norma citada — intocable** |
| **QUIRA descrita como auditoría** | «QUIRA audita la gobernanza» | 🔧 **sí cambia** — `BOOT` ya dice ⛔ «NO es auditoría ni observatorio» |
| **GM-Ω descrita como auditoría** | «esta auditoría cometió…» | 🔧 **sí cambia** — es un peritaje |
| **`auditable` / `auditabilidad`** | «cadena auditable» | 🔬 **se conserva** — es la propiedad que QUIRA certifica |

> Un reemplazo sin clasificación previa **habría borrado artículos de ley**. Eso es exactamente «dañar lo que es válido», y ocurrió en el primer minuto del primer ejemplo.

Y hay algo peor, que conviene decir: **`governance/BOOT.md` ya declara desde el 2026-08-05 que QUIRA «⛔ NO es auditoría ni observatorio»**. La regla existía; el vocabulario del repositorio no la siguió. Es el mismo patrón que `DOC-013` —el canon dice una cosa y la práctica deriva— y es la razón de fondo por la que este refactor es necesario.

## ★ 1 · Las cinco categorías · la regla que impide dañar lo válido

**Ninguna pieza del ecosistema se toca antes de clasificarla.** Y la clasificación no es opinable: cada categoría tiene una prueba distinta.

| | Categoría | Qué es | Qué se hace con ella |
|---|---|---|---|
| 🏛️ | **HISTÓRICO** | existió y ya no opera | se PRESERVA como trazabilidad — nunca se borra |
| ⚖️ | **NORMATIVO VIGENTE** | lo fija una norma en vigor | se ACATA mientras siga vigente — no es decisión de diseño |
| 🔬 | **EMPÍRICAMENTE ÚTIL** | funciona y hay evidencia de que funciona | se CONSERVA si supera validación — y hay que poder mostrar cuál |
| 🔧 | **DECISIÓN DE DISEÑO ANTIGUA** | se eligió, no se dedujo; y nadie escribió por qué | queda ABIERTA a rediseño — ni válida ni inválida por antigüedad |
| 📜 | **SUPERADO METODOLÓGICAMENTE** | fue correcto en su momento y el conocimiento actual lo desplazó | se conserva como ANTECEDENTE, no como regla |

### Ejemplos ya identificados por `GM-Ω`

**🏛️ HISTÓRICO** — el nombre `SIAP`, `QUADRUM`, `TERRA`; `ICPI_v1`; las versiones superadas de los expedientes

**⚖️ NORMATIVO VIGENTE** — `R_i`↔COOTAD 54-55 · `V_i`↔LOTAIP 7 · `T_i`↔COPFP 115-117 + Acuerdo 067 MEF · `P_i`↔COPFP 54 · las cuatro infracciones de `C_i`

**🔬 EMPÍRICAMENTE ÚTIL** — el producto lógico de `V_i` (un silo en cero anula la meta); la jerarquía de fuentes de `T_i`; los cuatro silos

**🔧 DECISIÓN DE DISEÑO ANTIGUA** — los pesos `0,10/0,15/0,05/0,50`; el piso `0,50`; la residencia de cada índice en su dominio; la escala AVEP

**📜 SUPERADO METODOLÓGICAMENTE** — `C_i` = imputabilidad orgánica frente a `C_i` = calidad de proceso; «Cumplimiento Institucional» como nombre del ICPI

### La corrección que esta tabla incorpora

Una versión anterior de `DOC-027` decía:

> ~~«Donde no hay razón documentada, no hay nada que respetar.»~~

El colega la corrigió, y con razón: **empujaba al extremo contrario** del sesgo conservador que venía a corregir. La formulación rigurosa es:

> Donde no existe justificación documental de una decisión de diseño, esa decisión **no adquiere autoridad metodológica por antigüedad**; su permanencia debe **evaluarse nuevamente** frente al fenómeno, la teoría, la evidencia, la norma y la arquitectura actual.

La diferencia es toda: una decisión antigua sin justificación **no es automáticamente incorrecta**. Tampoco automáticamente correcta. Queda **abierta**, que es un estado distinto de ambos.

## 2 · Sobre qué actúa · el tamaño real

Un plan que no sabe su tamaño no es un plan. Contado del repositorio:

| Grupo | Artefactos | Cuenta |
|---|---|---:|
| CANON | documentos `docs/**/*.md` | **412** |
| CANON |   ↳ de los cuales, `ADR` | *44* |
| CANON |   ↳ de los cuales, `PCD` de dominio | *7* |
| CANON | reglas de negocio `brn/*.yaml` | **30** |
| CANON | gobernanza | **23** |
| CANON | marco teórico | **3** |
| CÓDIGO | módulos de aplicación | **104** |
| CÓDIGO | páginas de interfaz | **61** |
| CÓDIGO | scripts | **175** |
| CÓDIGO | pruebas `tests/test_*.py` | **45** |
| DATOS | snapshots | **468** |
| | **TOTAL en el repositorio** | **1321** |

⚠️ Las filas en *cursiva* **no suman**: están contenidas en la línea de arriba. La primera versión de esta carta las sumaba —contando `ADR` y `PCD` dos veces, y dejando fuera las pruebas por el error opuesto— y publicó un total inflado. Se deja dicho porque es exactamente el defecto que este refactor viene a corregir, cometido en el documento que lo planifica.

Más, fuera del repositorio o no contable por archivo:

| | Cuenta |
|---|---:|
| hojas del Gold Master | 123 |
| dominios | 13 |
| índices | 12 |
| factores del ICPI | 6 |

> ### Esto no se refactoriza pieza por pieza a mano
>
> A un artefacto por sesión, el refactor tarda años. Lo que hace viable un cambio de esta escala es que **la clasificación sea derivable**: cada pieza declara su categoría y un gate lo verifica — el mismo patrón de `deuda.py` y `doctrina.py`.

## ★ 3 · La arquitectura propuesta · FONDO y FORMA

La expresión es de Javo —*«los dominios fondo y forma»*— y el colega la formalizó. Es el cambio conceptual más grande de la carta:

```
                        QUIRA
                          │
              ┌───────────┴───────────┐
            FONDO                   FORMA
     ¿QUÉ gestiona el GAD?    ¿CÓMO lo gestiona?
              │                       │
     dominios sectoriales    capacidades transversales
              │                       │
   salud · agua · vialidad    planificación · ejecución
   ambiente · riesgos ·       eficiencia · contratación
   desarrollo económico       transparencia · trazabilidad
                              coordinación · responsabilidad
              └───────────┬───────────┘
                          │
                    INTELIGENCIA
             gráfica → analítica → narrativa
                          │
                      EVIDENCIA
```

> **La misma gestión se observa a la vez desde el fondo y desde la forma.** Eso es lo que hoy no se puede hacer, y es la razón por la que indicadores transversales viven dentro de dominios sectoriales.

### El caso que lo ilustra · `IED`

Javo propuso *«establecer eficiencia directiva»*. **Ya existe**: el `IED` —Índice de Eficiencia por Dirección— desglosa metas del PDOT por dirección del Estatuto Orgánico (`H17`, `H30_IED_POR_DIRECCIÓN`). Lo que no tiene es sitio: su dominio, su rol y su pregunta están los tres `POR_DECLARAR`.

Y en el esquema FONDO/FORMA se ve por qué: **`IED` no pertenece a ningún dominio sectorial**. La pregunta «¿qué tan eficientemente funciona la dirección responsable?» aplica a Salud, a Obras Públicas y a Financiera por igual. Es **forma**, y hoy no hay dónde ponerla.

### Los tres niveles que esto habilita

| Nivel | Unidad | Pregunta |
|---|---|---|
| **sectorial** | una competencia | ¿qué resultados está gestionando? |
| **organizacional** | una dirección | ¿cómo funciona esa unidad? |
| **transversal** | el gobierno municipal | ¿es coherente, eficiente, trazable y coordinado el sistema completo? |

## ★ 4 · El ICPI · cuatro destinos posibles, ninguno decidido

⚠️ **No se decide aquí.** `011-C4` lo hace. Pero conviene tener los cuatro sobre la mesa para que el dictamen no se lea como binario:

| | Destino | Qué significaría |
|---|---|---|
| **A** | se **conserva** | la construcción supera `C4` y la teoría justifica sus dimensiones |
| **B** | se **refactoriza** | mismo fenómeno, otros factores, otra semántica, otra agregación, otra escala, otra residencia |
| **C** | se **descompone** | en vez de un número: congruencia programática · ejecución financiera · trazabilidad · responsabilidad institucional · eficiencia directiva · desempeño operativo. Y un **panel multidimensional** en lugar de un índice único |
| **D** | se **depreca** | `ICPI_v1` queda disponible para trazabilidad y deja de ser el indicador operativo principal |

**Ninguno de los cuatro es un fracaso.** `D` tampoco: sería evolución metodológica, y el `ICPI` histórico seguiría explicando de dónde vino el sistema.

### ⚠️ Y por qué el nombre va al final

Javo planteó renombrar el `ICPI`. La secuencia correcta **no empieza por el nombre**:

```
  1. ¿qué fenómeno sobrevive a C4?
  2. ¿cuál es su unidad?
  3. ¿cuál es su arquitectura?
  4. ¿cuál es su residencia?
  5. …y recién entonces: ¿cómo se llama?
```

> Empezar por el nombre sería hacer **branding de un concepto que todavía se está rediseñando**.

## 5 · Los diez ejes · se auditan simultáneamente

Un refactor que arregle la ontología sin tocar el frontend produce un sistema que **dice una cosa y muestra otra** — el defecto que `GM-Ω` lleva toda la investigación documentando dentro del propio instrumento.

| | Eje | Pregunta | Estado hoy |
|---|---|---|---|
| **A** | Ontología | ¿qué cosas existen en QUIRA? | Constitución §CAPA 0 · `T1`/`T2` cerrados |
| **B** | Taxonomía | ¿cómo se llaman y cómo se agrupan? | `T1`-`T6` · 43 nombres clasificados · `T6` espera al dictamen |
| **C** | Metodología | ¿qué significa cada indicador? | `011-C2` ✅ para los 6 factores · falta para los otros 11 índices |
| **D** | Datos | ¿qué fuente alimenta cada dato? | `004` matriz de procedencia · 150 celdas |
| **E** | Gold Master | ¿cómo se representa canónicamente? | ⚠️ CONGELADO hasta `011-C4` |
| **F** | Código | ¿la implementación coincide con la ontología? | `DOC-016`: la ontología gobierna a la implementación |
| **G** | Dominios | ¿cada indicador vive donde corresponde? | `R0`/`R1`/`R2` · 23 de 48 celdas `POR_DECLARAR` |
| **H** | Frontend | ¿la interfaz representa la arquitectura? | sin frente · Bloomberg Firewall vigente |
| **I** | Narrativa | ¿QUIRA explica bien lo que mide? | sin frente · es el salto de dashboard a inteligencia pública |
| **J** | Escalabilidad LATAM | ¿qué es Ecuador y qué es generalizable? | `010` · siguiente en la ruta |

## ★ 6 · Qué se puede hacer HOY y qué espera al dictamen

La dependencia con `011` es **más chica de lo que parece**. Sólo espera lo que presupone saber qué sobrevive:

```
  AHORA · no toca el motor, y alimenta al dictamen
  ├── 010        transferibilidad LATAM        ← siguiente en la ruta
  ├── R0         diagnóstico de los 13 dominios
  ├── R1         modelos A · B · C de arquitectura
  ├── EJE H/I    dashboards y narrativa por dominio
  ├── LIMPIEZA   clasificar los 411 documentos de canon
  └── 011-A2     declarar la unidad `i` en el canon

           ↓

  011-C4   DICTAMEN · ¿qué sobrevive del constructo?

           ↓ y sólo entonces

  ├── T6         renombrar / deprecar / eliminar
  ├── R2         residencia y ámbito de los índices
  ├── EJE E      intervenir el Gold Master
  └── v2         universo completo del PDOT (66)
```

| Frente | ¿Espera a `C4`? | Por qué |
|---|---|---|
| `010` LATAM | 🟢 no | separar lo ecuatoriano de lo generalizable **alimenta** el dictamen |
| `R0` · `R1` | 🟢 no | son diagnóstico |
| Dashboards · narrativa | 🟢 no | dependen de `R0`, no de `C4` |
| Limpieza documental | 🟢 no | clasificar no es cambiar |
| Renombrado (`T6`) | 🔴 **sí** | el nombre depende de qué resulte que mide |
| Residencia (`R2`) | 🔴 **sí** | mover un índice cuyo constructo está en dictamen es reorganizar la casa antes de saber qué se guarda |
| Gold Master | 🔴 **sí** | `Regla de Oro 1` |

## 7 · Las reglas de la migración

| # | Regla | De dónde sale |
|---|---|---|
| 1 | **Clasificar antes de tocar.** Ninguna pieza se modifica sin declarar en cuál de las cinco categorías cae | esta carta · §1 |
| 2 | **El basónimo no cambia.** El identificador estable sobrevive al renombrado, o se rompe la trazabilidad | `DOC-015` |
| 3 | **Nombre técnico ≠ nombre de presentación.** Tres capas, y la jerga no cruza al producto | `DOC-014` · `Regla de Oro 2` |
| 4 | **Anti-inflación.** Si un concepto sólo renombra, no entra: debe añadir capacidad, eliminar ambigüedad o reducir complejidad | `Regla de Oro 7` |
| 5 | **Ningún cambio nace en Python.** Nace en el canon; el código implementa | `Regla de Oro 9` · `DOC-016` |
| 6 | **Lo que se retira no se borra:** pasa a `HISTÓRICO` con su linaje | `DOC-013` |
| 7 | **Continuidad histórica ≠ continuidad metodológica.** Conservar `ICPI_v1` no obliga a que `ICPI_v2 = ICPI_v1`; conservar `d06` histórico no obliga a que `d06` futuro sea igual | el colega, 2026-09-05 |
| 8 | **Cada dominio cierra con su `PCD`.** El protocolo de curación no se salta | `Regla de Oro 8` |

## Lo que esta carta NO hace

- **No decide el destino del ICPI.** Cuatro opciones sobre la mesa, `011-C4` elige.
- **No renombra nada.** El nombre es el último paso, no el primero.
- **No toca el Gold Master.** Congelado hasta el dictamen.
- **No clasifica todavía** los 411 documentos ni las 123 hojas: establece **cómo** se clasifican. El barrido es trabajo de ejecución.

> ### El propósito, dicho en una línea
>
> `GM-Ω` no existe para legitimar el pasado ni para destruirlo, sino para **ponerlo en su lugar**: el pasado como **linaje**, la norma como **restricción**, la evidencia como **fundamento**, la teoría como **justificación** — y el diseño como **decisión presente**.

Lo que eso habilita es lo que hasta ahora no se podía hacer con seguridad: **diseñar el QUIRA que se necesita, no preservar el QUIRA que se construyó.**

---
*QUIRA-NEXT · Carta de Rearquitectura · 1321 artefactos inventariados · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
