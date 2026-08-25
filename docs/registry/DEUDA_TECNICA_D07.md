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

## 4 · Portabilidad — 25 puntos de frontera replicada (eran 54)

`personal 0 / 0` · `frontera_fija 25 / 25` (`scripts/ci/check_portabilidad.py`).

**Avance del 2026-08-20: 50 → 25.** Migración por lotes a `config.DATOS_DIR`, en dos patrones
distintos: `Path(r"…ProyecT…")` (7 archivos) y cadena cruda `r"…ProyecT…"` conservando el tipo
`str` (17 archivos). Suite verde en cada lote.

**Los 25 restantes no se forzaron.** La inserción automática del import rompía la sintaxis en esos
archivos, `ast.parse` los rechazó y **no se escribieron** — fallar seguro antes que dejar 25
archivos con sintaxis inválida. Quedan para revisión manual, con el trinquete ya bajado a 25 para
que el avance no se pierda.

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
