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
