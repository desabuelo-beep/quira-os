---
authority:
  parent: ADR-051
  constitution_articles: [1, 3, 5]
  type: REGISTRO
estado: ABIERTO
fecha: 2026-08-19
---

# Deuda técnica de d07 — medida, no estimada

> **Orden de trabajo (Javo, 2026-08-19):** *«Todo lo pendiente una vez salgamos de terminar DOM
> Transparencia con todo lo que implica. Pasamos a trabajar las deudas técnicas.»*
>
> Este registro existe para que ese «después» tenga contenido exacto y no haya que reconstruirlo
> de memoria. Cada entrada trae **su medición, su prueba y su condición de cierre** — ninguna es
> una impresión.

## 1 · El vínculo prueba↔verificador · `declarado ≠ existente ≠ ejecutado ≠ exitoso`

**Qué falta.** La cadena de procedencia comprueba que la prueba citada **exista**; no que
**corresponda** al verificador que dice respaldar. Hoy cualquier prueba real acredita cualquier
verificador.

```
prueba_declarada → ¿existe? → sí → aceptada          ← hasta aquí llegamos
                 → ¿corresponde al verificador?      ← falta
                 → ¿ejecutó realmente?               ← falta
                 → ¿tuvo resultado exitoso?          ← falta
```

**Por qué importa.** Es exactamente el error que este dominio persigue en el GAD: *tomar la
existencia de algo como evidencia de su validez.* Cometerlo contra nosotros mismos invalidaría la
autoridad para señalarlo afuera.

**Dónde está fijado.** `tests/test_procedencia_adversarial.py::test_05_la_prueba_deberia_estar_vinculada_al_verificador_que_respalda`
— en verde y explícita, documentando el hueco.

**Condición de cierre.** Cuando el vínculo sea comprobable, se invierte la aserción de esa prueba:
pasa de registrar la ausencia de la regla a defenderla.

## 2 · Artefactos que no declaran su sujeto

**Medido el 2026-08-19** sobre los nueve puntos de transición de la cadena:

| Punto | Defensa | Estado |
|---|---|---|
| perfil del sujeto | huella + gate `SUJETO` | ✅ |
| sello de la cadena | gate `SUJETO` (etiqueta + huella) | ✅ |
| captura de la fuente | lleva `entidades{937}`, sin huella | ⚠️ parcial |
| **índice de descargas** | — | ⛔ |
| **análisis de contenido** | — | ⛔ |
| **inventario documental** | — | ⛔ |
| **contenido de contenedores** | — | ⛔ |
| corridas persistidas | `Corrida.municipio`, sin huella | ⚠️ parcial |
| autoconocimiento | derivado del sello | ✅ |

**El riesgo real.** Hoy la cadena los protege *indirectamente*: alterar la identidad invalida el
sello y el gate detiene la corrida. Pero un artefacto leído **fuera** de la cadena —copiado,
compartido, ingerido por otro dominio— no dice de quién es. Con 222 GAD produciendo archivos con
los mismos nombres, la ambigüedad deja de ser teórica.

> **La procedencia debe viajar con el artefacto hasta el límite en que el artefacto pueda ser
> consumido independientemente de la cadena que lo produjo.**
> *(formulación del colega, 2026-08-19)*

**Dónde está fijado.** `test_11_los_artefactos_derivados_no_declaran_su_sujeto` — trinquete en 4:
pueden bajar, no subir.

### CERRADA del todo el 2026-08-26 — y no re-ejecutando

Quedaba **uno**: `descargas_indice.json`, cuya etapa se selló antes de que la cadena exigiera
sujeto. El colega marcó el riesgo antes de tocarlo:

> *«Que una prueba pueda regenerar el archivo no demuestra que la etapa deba volver a ejecutarse
> ahora. La ejecución es evidencia de mecanismo; la autorización para modificar un artefacto
> histórico es otra cuestión.»*

Tenía razón: re-ejecutar habría **sustituido evidencia histórica** por evidencia nueva para
conseguir el estado que queríamos ver. Había tres salidas y dos eran malas:

    re-ejecutar      → sustituir la evidencia de agosto
    escribir 130801  → fabricar procedencia con lo que el operador sabe
    DERIVARLO        → leer lo que la evidencia ya contiene   ← ésta

**Las 936 URLs son `transparencia.dpe.gob.ec/…/1360001010001/…`, y ése es el RUC del sujeto.**
936 de 936, sin ningún otro RUC en el artefacto. El sujeto no se declaró: **se derivó**, con su
comprobación reproducible escrita dentro del propio `_meta`. Y el sello de la etapa **sigue
diciendo `sujeto: None`**, que es la verdad: la cadena no lo acreditó, lo acredita el contenido.

`procedencia.por_derivacion()` exige `fundamento` y `comprobacion`; sin ambos lanza
`NaturalezaUsurpada`, porque derivar sin comprobación es declarar con otro nombre.

## 2-ter · CERRADO el 2026-08-26 · el RUC no estaba huellado

**Apareció al acreditar lo anterior**, buscando en la evidencia lo que el sello no decía.

`huella()` promete en su propia docstring *«se huella todo aquello con lo que se va a la fuente»*.
No era cierto:

    huellado      dpe_entidad_id · dpe_entidad_nombre · dominio_web · dominios_asociados
    NO huellado   el RUC — y es con lo que QUIRA va realmente a la Defensoría

Cambiar el RUC no alteraba la huella. **Es el mismo ataque que motivó la huella** —`dpe_entidad_id`
937→999, 2026-08-19— en un campo que se olvidó: QUIRA habría descargado de otra entidad con todos
los gates en verde.

Cerrado declarando el RUC en `identidad_en_fuentes`. La huella cambió
(`e187a12a…` → `fe11fb1e…`) y **eso es lo correcto**: la identidad no cambió, se completó su
declaración. Las 4 etapas afectadas se re-huellaron **con fundamento escrito en el sello**
(`rehuellado`), conservando la huella anterior y declarando que no se re-ejecutó nada.

**Dónde está fijado.** `test_09b_TODO_lo_que_va_a_la_fuente_esta_huellado`, que **deriva** los
campos del perfil en vez de fijarlos a mano: una lista escrita repetiría el olvido en cuanto se
añada el siguiente identificador.

## 3 · Cinco dominios sin la defensa, y sin atacar

```
  d01    no_protegido           d07    protegido_y_atacado (13 ataques)
  d02    no_protegido
  d03    no_protegido
  d08    no_protegido
  d09    no_protegido
```

**La afirmación que QUIRA puede sostener**, y la que no:

> ✅ *«QUIRA ha demostrado un mecanismo de integridad de sujeto en d07; los demás dominios
> permanecen sin evidencia de haber pasado por ese mecanismo.»*
>
> ⛔ *«QUIRA tiene un mecanismo transversal de integridad de sujeto.»*

**«Sin atacar» no es «seguro».** Los otros cinco no resistieron nada: no tienen sello de cadena,
ni gate de sujeto, ni huella. Un ataque equivalente no encontraría defensa que romper. Es el mismo
error que el sistema acaba de descubrir a nivel de sujeto, ahora a nivel de plataforma —
**confundir ausencia de contradicción con evidencia de validez**— y por eso el estado se deriva y
se publica en vez de suponerse.

**Dónde está fijado.** `apropiacion.cobertura_de_la_plataforma()`, derivado del código de cada
dominio y de las pruebas adversariales que lo nombran. Nadie declara «protegido».

## 3-bis · CERRADO el 2026-08-19 · la reanudación se saltaba el trabajo

**Encontrado al acreditar la etapa `enlaces`**, que es exactamente para lo que servía acreditarla.

`verificar_enlaces_lotaip.py` reanuda desde su salida anterior y copiaba cualquier registro cuyo
estado no fuera `no_verificable`. Eso incluía **`no_intentado_por_corte_de_fuente`** — un estado
que no dice nada del enlace: dice que nuestro instrumento se detuvo aquella vez.

    corrida del 17-ago   135 enlaces cortados por un fallo transitorio de SERCOP
    corridas siguientes  copian el «no intentado» → NUNCA se reintentan
    y con ellos          417 «accesibles» se arrastran sin reverificar

La corrida de acreditación lo delató por el reloj: **10 segundos para 576 enlaces**, con 8
intentos registrados en el transporte. Una etapa que se declaraba `ejecutada` sin haber ejecutado
— `declarado ≠ ejecutado`, cometido por nosotros mismos mientras lo perseguíamos en el GAD.

**La regla que queda:** *se reutiliza lo que dice algo del enlace; se reintenta lo que dice algo
de nuestro instrumento.* Y `forzar=True` ahora llega hasta el script (`--rehacer`), no se queda en
saltarse el «al día».

Fijado en `test_un_corte_de_fuente_no_condena_al_enlace_para_siempre` y
`test_forzar_una_etapa_fuerza_su_trabajo_no_solo_su_estado`.

**Nota sobre los 135.** Son de `compraspublicas.gob.ec` (SERCOP), no del GAD: enlaces a procesos
de contratación que el sujeto obligado publica. Su inaccesibilidad, si se confirma, **no es un
hallazgo sobre Montecristi** sino sobre la disponibilidad de una fuente de tercero (ADR-042 §6:
`fuente_no_disponible` no dice nada del sujeto).

## 4 · Portabilidad — CERRADA el 2026-08-25 (eran 54 puntos)

`personal 0 / 0` · `frontera_fija 0 / 0` (`scripts/ci/check_portabilidad.py`).

**La frontera hacia `ProyecT/` ya no está escrita a mano en ningún punto.** Se recibe de
`config.DATOS_DIR`, que la toma de `QUIRA_DATOS`. El guard deja de medir una deuda y pasa a
defender una propiedad: **QUIRA corre en cualquier máquina que declare dónde están sus datos.**

    54 → 50 → 25 → 3 → 0

Cuatro patrones distintos, descubiertos uno a uno porque cada lote revelaba el siguiente:

| Patrón | Archivos | Por qué falló el anterior |
|---|---|---|
| `Path(r"…ProyecT…")` | 7 | — |
| cadena cruda `r"…"` conservando `str` | 17 | no llevaba `Path()` |
| **concatenación implícita multilínea** | 20 | la sustitución dejaba `str(…)` seguido de una cadena → error de sintaxis |
| constante sin imports previos | 2 | el bloque de imports no existía; el import va tras el docstring |

Y un tercer punto que no era código: un **docstring documentaba la ruta absoluta** como si fuera la
fuente de verdad. Corregido a `$QUIRA_DATOS/…`.

**Ningún lote se forzó.** Cada uno pasó por `ast.parse` antes de escribirse; los archivos que no
compilaban **no se tocaron**. Fallar seguro antes que terminar rápido — y por eso el recorrido tomó
cuatro pasadas en vez de una.

Verificado tras cada lote: 488 pruebas verdes · 742 archivos sin error de sintaxis · el conector
canónico del Gold Master y los manifiestos importando y resolviendo.

## 4-bis · CERRADO el 2026-08-25 · 85 ensayos guardados como procedencia del sujeto

**Encontrado al cerrar la portabilidad**, no buscándolo: dos JSON sin rastrear en
`data/snapshots/130801/provenance/`. Al contar la carpeta entera:

    85 corridas en seco  ·  4 reales

El 95 % de la procedencia del sujeto observado **no observó nada**. Todas se llamaban igual
—`provenance_130801_<fecha>.json`—, vivían en el mismo directorio, y la única diferencia era un
campo `dry_run` dentro del archivo.

**Por qué cuenta como defecto y no como desorden.** Es el mismo error que este dominio persigue
afuera —*el nombre del artefacto no es evidencia de lo que promete*, anotado tres veces contra el
GAD— cometido aquí contra nosotros mismos. Y en el sentido más grave de los dos: no inventa un
incumplimiento del sujeto, pero **fabrica actividad propia**. Cualquier consumidor futuro —otro
dominio, la cantera, un auditor con un `glob`— habría leído 89 observaciones donde había 4.

**La distinción ya estaba declarada** en el dato (`dry_run` existía desde siempre). Lo que faltaba
era que la **estructura la respetara**: nada nace en Python (Regla 9), esto sólo obliga al disco a
decir lo que el campo ya decía.

| | antes | ahora |
|---|---|---|
| destino | mismo directorio | `provenance/` · `provenance/ensayos/` |
| nombre | `provenance_…` ambos | `provenance_…` · `ensayo_…` |
| distinguible | leyendo el interior | por ubicación **y** por nombre |

Los 85 se separaron con `git mv` —reversible y auditable en el historial—; las 4 observaciones
reales siguen donde estaban, lo cual **también se prueba**: separar no puede volverse esconder.

**Dónde está fijado.** `tests/test_ensayo_vs_observacion.py`, cuatro pruebas. Verificadas contra
regresión inyectada: al devolver un `dry_run` al directorio principal, fallan. Un guard que no se
intentó romper no es un guard (OBS-031).

**De paso:** el log del emisor anunciaba «PASO 9» siendo el 11. *Etiqueta incorrecta = número
falso* (§6-sexies) aplica también a los pasos.

## 2-bis · CERRADA el 2026-08-25 · los artefactos ya declaran su sujeto

Cierra la deuda #2, y **no en 4/4** — que es la parte que importa:

| artefacto | sujeto |
|---|---|
| `contenido.json` · `enlaces.json` · `inventario_documental.json` · `contenido_contenedores.json` | 130801 Montecristi, acreditado por la cadena |
| `descargas_indice.json` | ⛔ **su etapa no acreditó sujeto** |

La etapa `descarga` se selló el 2026-08-19, antes de que la cadena exigiera sujeto. Sabemos que es
de Montecristi; **la cadena no lo acreditó**. Escribirlo «porque lo sabemos» habría convertido un
artefacto sin procedencia en uno que aparenta tenerla. Declara su hueco y se cierra cuando la etapa
vuelva a correr.

Lo que se defiende ahora es más fuerte que «tienen sujeto»: **ninguno guarda silencio** — o lo
declara, o declara por qué no puede.

### El error que costó la sesión, y vale más que el arreglo

El primer intento estampó la procedencia desde `_sellar()`, **después** de que el generador
escribiera el archivo. Parecía inofensivo:

    estampo contenido.json   →  su SHA cambia
    la etapa que lo consume  →  «mi insumo cambió»  →  se re-ejecuta
    re-ejecutarse            →  reanalizar 936 archivos, salir a la red

Tres etapas quedaron desalineadas y la suite se colgó re-analizando el corpus.

> **El acto de registrar la procedencia alteró aquello cuya identidad registraba.**
> Un observador que modifica lo observado.

Es el mismo género de error que este dominio persigue afuera, cometido por el módulo cuyo propósito
es impedirlo. **El sitio correcto es el generador**: ahí el archivo nace con su procedencia dentro y
el SHA que la cadena mide después ya la incluye. Nadie tiene que acordarse de estampar.

Y un segundo hallazgo, cazado por `test_quira_reconstruye_sus_derivados_sin_ayuda`: la procedencia
llevaba **marca de tiempo**, lo que volvía el derivado irreproducible para siempre. El *cuándo*
pertenece al sello; el *de quién*, al artefacto. La prueba de autonomía detectó que se había escrito
a mano algo que el sistema no sabía regenerar — exactamente para lo que existe.

**Dónde queda fijado.** `test_11b` (nace en el generador, no se estampa después), `test_11c` (sin
reloj, reproducible), ambas verificadas contra regresión inyectada.

**Daño a los datos: ninguno.** Comprobado: 422/5/3/6/1/139 estados de enlaces idénticos, y
936/936/422/935 registros intactos.

## 4-ter · CERRADA el 2026-08-25 · una prueba ya no puede actuar sobre el mundo

**Lo reveló la cuelga anterior, y no lo causó.** `test_08b` llamaba a `orquestador.ejecutar()`, que
al ver la cadena desalineada **re-ejecutaba etapas**: analizar 936 archivos, y `verificar_enlaces`
llegó a intentar salida de red.

Javo le dio el encuadre que lo convierte en prioridad, y no en higiene:

> *«Una prueba que puede salir a la red, descargar, regenerar o modificar artefactos deja de ser una
> observación controlada y puede contaminar aquello que pretende verificar.»*

Y la simetría con el fallo de procedencia, que es lo que los hace la misma familia:

| | |
|---|---|
| procedencia | el mecanismo de observación modificó **el objeto observado** |
| `test_08b` | el mecanismo de observación podía modificar **el mundo que observa** |

> **El observador no puede alterar en silencio aquello cuya integridad pretende demostrar.**

### El inventario, antes de tocar un solo test

|  |  |
|---|---|
| red (directa, en-proceso) | **0** — ninguna prueba la llama |
| subprocess | 1 |
| escrituras | 57 en 4 archivos |
| generador / orquestador | 8 y 8, en 2 archivos |
| `conftest.py` | **no existía** — ningún punto de aislamiento |

El hallazgo que fijó el diseño: **la red no se alcanza en-proceso, se hereda.**

    test → orquestador.ejecutar() → preparar_evidencia()
         → ejecutar_etapa() → subprocess → script → curl

Por eso bloquear sockets no habría servido de nada —el hijo tiene su propio proceso— y el único
estrangulamiento real es el `spawn` (`app/agents/d07/etapas.py:337`). Los sockets se cierran igual,
como defensa en profundidad.

### Qué quedó

`tests/conftest.py`, fixture `autouse`: **prohibido por defecto, permitido si se declara.**

    @pytest.mark.efecto_real("por qué lo necesita")

Con la frontera cerrada, **2 de 494** pruebas la cruzaban. Una se **eliminó** —lanzaba un subproceso
para correr un script puro; ahora lo importa—; la otra se **declaró**, porque reconstruir un derivado
es literalmente lo que demuestra. Regla: *si el efecto se puede eliminar, se elimina; sólo se declara
el que es inherente.* Trinquete en 2 declarantes, contados **con AST** —la primera versión contaba 3,
porque sumaba una línea de ejemplo dentro de un docstring: *etiqueta incorrecta = número falso*,
esta vez contra el propio guard.

Y `test_08b` **no falló**: hoy no cruza la frontera porque la cadena está alineada. Eso confirma el
diagnóstico —era la suerte— y ahora, si se desalinea, se detiene en 4 segundos con causa legible en
vez de colgarse.

### El guard también se ataca

Tres regresiones inyectadas, las tres detectadas:

| ataque | resultado |
|---|---|
| quitar el `autouse` | 4 pruebas en rojo |
| ensanchar el `except` de `ejecutar_etapa` a `Exception` | 1 en rojo |
| una prueba se da permiso sin justificarlo | 1 en rojo |

El segundo es el que más importa: era la forma de anular la defensa **sin tocarla** — la excepción
se convertía en un plácido «etapa fallida» y nada se ponía rojo.

**500 pruebas · check_health TODO OK.**

## 4-quater · CERRADO el 2026-08-26 · el guard moría al informar

`check_epistemico.py` llamaba a `relative_to(_RAIZ)` para imprimir su cabecera. Si la carpeta
auditada estaba **fuera del repositorio** —un fixture en un temporal, por ejemplo—, lanzaba
`ValueError` **después de haber recorrido todo el corpus**: calculaba el resultado y moría al
mostrarlo.

El propio archivo lleva desde su primera versión el comentario que lo condena, escrito para otro
fallo idéntico —la consola de Windows en cp1252—:

> *«un gate que muere al informar es un gate que no informa»*

**El mismo defecto, dos veces, en el mismo archivo.** Se anota como deuda del guard y no como parte
de la decisión de gobernanza que lo convirtió en gate: son cosas distintas, y mezclarlas habría
hecho parecer que el gate se activó con un defecto abierto.

## 5 · Lo que sigue abierto del dominio, no de la técnica

- **Los 636 artefactos** — clasificados como `material_de_ingenieria` en su propio `_meta`. Se
  usan ya para fixtures y casos límite; **no** son observación atribuible hasta que la cadena que
  los produce esté acreditada (ADR-051 §10).
- **`Ordenanzas.zip`** >500 MB — captura declarada incompleta.
- **OCR** — 10 escaneos únicos, ningún motor instalado.
- **Prueba A de origen** — `fuente → captura → descarga → SHA`, escrita y desactivada
  (`QUIRA_PRUEBA_DE_ORIGEN=1`).
- **Promoción a `vigente`** de las 9 piezas de d07 — decisión de Javo (ADR-035 §5).

---
*Registro de deuda d07 · Dylus Lab © 2026 · lo que falta, con su medición y su condición de cierre.*
