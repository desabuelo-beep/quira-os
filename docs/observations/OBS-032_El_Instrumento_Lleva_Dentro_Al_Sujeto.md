---
id: OBS-032
authority:
  parent: ADR-051
  constitution_articles: [1, 3, 5, 20]
  type: OBSERVACION
fecha: 2026-08-19
dominio: método · arquitectura
estado: VERIFICADA
---

# OBS-032 · La cadena de d07 no mide municipios: mide Montecristi

> El colega fijó el criterio rector que hacía falta:
>
> > *«No debemos construir d07 para Montecristi. Debemos utilizar Montecristi para construir el
> > patrón que permita ejecutar d07 sobre 222 GAD.»*
>
> La medición dice que hoy es al revés: **la identidad del sujeto observado está incrustada en el
> instrumento, en 11 puntos de código efectivo.**

## Lo medido

| Dónde | Qué lleva dentro |
|---|---|
| `capturar_lotaip_dpe.py:59` | `ENTIDADES = {937: "GAD Montecristi"}` — el identificador del sujeto en la fuente |
| `descargar_lotaip.py:137` | `ev["entidades"]["937"]` — la misma clave, repetida a mano |
| `analizar_contenido_lotaip.py:87` | `DOMINIO_GAD = "montecristi.gob.ec"` |
| `verificar_enlaces_lotaip.py:67,224` | el dominio otra vez, como criterio de procedencia institucional |
| `capturar_lotaip_dpe.py:42` · `descargar_lotaip.py:51` · `etapas.py:80,89` | rutas `dpe_montecristi.json` |
| `orquestador.py:76` | `MUNICIPIO = "montecristi"` |

Nada de esto es un error de ejecución: la cadena funciona y sus resultados son correctos. **Es un
error de escala.** Aplicarla al GAD 002 exigiría editar siete archivos y acordarse de los once
puntos; multiplicado por 222, no es un pipeline sino un procedimiento manual con apariencia de
software.

## Por qué apareció ahora y no antes

Porque hasta hoy la pregunta era «¿el resultado es correcto?», y lo era. La pregunta nueva
—«¿quién produjo este conocimiento y con qué capacidad?» (ADR-051 §2c-2d)— arrastra una tercera
que estaba tapada: **¿sobre qué sujeto?** Un instrumento que sólo sabe medir un sujeto no es un
instrumento: es una medición.

Es el mismo fenómeno de OBS-030 y OBS-031, un nivel más arriba. Allí el observador se equivocaba
sobre la fuente y sobre sí mismo; aquí el observador **no puede distinguirse de su primer caso**.

## Y al medir apareció algo mayor: el instrumento tampoco sale de un escritorio

Buscando la identidad del sujeto se encontró otra atadura, más fuerte y más silenciosa:

    54 puntos · 49 archivos · rutas absolutas al disco de una persona
    C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\...

Alcanza a `app/connectors/gold_master.py` —el conector canónico— y a los motores de **d01** y
**d08**. En una máquina distinta, la mayoría de esos programas no arranca.

**Una parte NO es un defecto y hay que decirlo:** `ProyecT/` está fuera del repositorio a
propósito —el repo es privado y los documentos fuente no se suben—, así que la frontera entre
código y datos es deliberada. El defecto es otro: esa frontera está **escrita a mano 54 veces** en
vez de declararse una sola. Cuando la carpeta cambie de sitio, o el sistema corra en un servidor,
habrá que encontrar los 54.

No se corrige hoy: son programas de varios dominios, con sus propias pruebas, y tocarlos de paso
al final de una jornada es exactamente cómo se rompe lo que funciona. Queda **medido, declarado y
con trinquete** — puede bajar, no subir.

## La regla que queda

> **Ninguna identidad del sujeto observado —código en la fuente, dominio web, nombre, territorio—
> puede vivir en el instrumento. El instrumento recibe un sujeto; no lo contiene.**

Corolario operativo: si aplicar la cadena a otro GAD exige editar código, la capacidad todavía no
existe como capacidad — existe como caso resuelto.

## Consecuencias

- Se crea el **perfil de sujeto observado** (`data/sujetos/`) como fuente única de identidad, y
  `app/agents/sujeto.py` como su única puerta de lectura — transversal, no de d07.
- Una prueba vigila que el acoplamiento **no crezca**: el número medido queda fijado, y todo punto
  nuevo hace fallar la suite. No se exige llegar a cero de golpe; se prohíbe empeorar.
- Montecristi conserva su lugar: **laboratorio de apropiación**, no destinatario del diseño.

---
*OBS-032 · Dylus Lab © 2026 · un instrumento que sólo sabe medir un sujeto es una medición.*
