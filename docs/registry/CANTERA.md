# Registro de cantera tecnológica

> **Sin entrada aquí, el componente no existe para QUIRA** (ADR-050 §5).
> Grados: **R0** referencia · **R1** patrón sin código · **R2** componente refactorizado ·
> **R3** capacidad QUIRA nativa.

| Proyecto | Licencia | Versión / commit | Evaluado | Capacidad de interés | Grado | Vive en | Prueba superada |
|---|---|---|---|---|---|---|---|
| EcuDataMCP | MIT | — | pendiente | adquisición fuentes públicas EC · SERCOP/OCDS | — | — | — |
| Cali Monitor | — | — | pendiente | monitoreo contractual · cache/cron | — | — | — |
| diagram-design | MIT | — | pendiente | densidad deliberada · acento reservado | — | — | — |
| mono-charts | — | — | pendiente | microvisualización sobria | — | — | — |
| CodeWiki | MIT | — | suspendido | documentación estructural | — | — | ver ADR-050 §6.2 |

## Nada absorbido todavía

Ninguna capacidad ha superado la prueba contra caso real. **Esta tabla es la agenda de
evaluación, no un inventario de dependencias.**

---

## Cantera OCR · matriz de licencias verificada (2026-08-18)

> **Por qué esta matriz existe.** Javo (2026-08-18): *«lo que más me preocupa son las cuestiones
> de licencia cuando tomemos cosas de otros, por el tema del motor canónico, que es nuestra
> receta secreta»*. La preocupación es correcta y la respuesta no puede darse de memoria: cada
> licencia se verificó contra el repositorio de origen.
>
> **LA REGLA, corregida el mismo día (colega · 2026-08-18).** La primera versión de esta tabla
> preguntaba «¿qué licencia tiene PaddleOCR?» y respondió «modelos no declarados» porque el
> README del repositorio no lo dice. **Estaba mal, y el error es instructivo:** el modelo
> `PaddleOCR-VL` declara `license: apache-2.0` en su propia ficha. La declaración vive en el
> ARTEFACTO, no en el proyecto.
>
> Por eso el registro se hace **por artefacto**, nunca por proyecto:
>
>     no existe «la licencia de PaddleOCR» — existe la licencia de cada pieza que QUIRA incorpora
>
> Un pipeline OCR arrastra código, pesos de detección, pesos de reconocimiento, modelo de
> layout, runtime, datos lingüísticos y dependencias transitivas. Cada uno con procedencia y
> licencia propias.

| Artefacto | Función | Licencia | Verificado en | Uso propietario | Riesgo |
|---|---|---|---|---|---|
| **tesseract** (código) | motor OCR | Apache 2.0 | `LICENSE` del repo | sí, permisiva | 🟢 |
| **tessdata** (modelos) | datos entrenados, incl. español | **Apache 2.0** | repo `tessdata` — «all data… licensed under Apache-2.0» | sí | 🟢 |
| **leptonica** (dependencia) | procesamiento de imagen que Tesseract requiere | **BSD-2-Clause** | `leptonica-license.txt` | sí, permisiva | 🟢 |
| **OCRmyPDF** | orquestación PDF→OCR, capa de texto | **MPL-2.0** | doc. del repo | sí — copyleft **de archivo** | 🟡 |
| **PaddleOCR** (código) | OCR + estructura documental | Apache 2.0 | `pyproject.toml` | sí | 🟢 |
| **PaddleOCR-VL** (modelo) | parsing documental | **Apache 2.0** | ficha del modelo · `license: apache-2.0` | sí | 🟢 |
| **PP-OCRv5** (pesos) | detección/reconocimiento del pipeline clásico | **por verificar artefacto por artefacto** | — | — | 🟡 |
| **docTR** (código) | OCR por aprendizaje profundo | Apache 2.0 | repo | sí | 🟢 |
| **docTR** (pesos) | modelos de detección/reconocimiento | **sin declaración separada localizada** | — | — | 🟡 |

### Lo que esta matriz permite afirmar

1. **Ninguna obliga a liberar el Gold Master ni el canon.** Apache 2.0 y BSD son permisivas;
   MPL-2.0 es copyleft **de archivo** y su propia documentación declara que *«permite la
   integración con otro código, incluido comercial y de código cerrado»*.
2. **Tesseract tiene la cadena completa verificada de extremo a extremo** —código Apache 2.0,
   modelos Apache 2.0, y su dependencia obligatoria Leptonica BSD-2-Clause—. Es el **baseline
   jurídico**: no necesariamente el mejor, sí el piso limpio contra el que medir a los demás.
3. **PaddleOCR deja de estar bloqueado**, pero sólo para los artefactos con licencia localizada.
   `PaddleOCR-VL` está verificado; los pesos del pipeline clásico `PP-OCRv5` **siguen pendientes**
   y no se usan hasta fijarlos.
4. **Invocar por subproceso reduce el riesgo** aún más que enlazar como librería: no hay obra
   derivada, sólo ejecución de un programa independiente. Es como ya usamos `curl`. Pero
   **⚠️ no convierte automáticamente MPL-2.0 en «verde»** (corrección del colega): OCRmyPDF
   exige publicar las modificaciones hechas sobre SUS archivos, y arrastra componentes con
   licencias distintas (MIT, CC-BY-SA para documentación). Es **candidato viable con
   condiciones**, no aprobado. Y para lo que QUIRA necesita —extracción estructural— encaja
   mejor como orquestador que como motor: no conviene confundir esas dos funciones.
5. **Ningún «sí» de esta tabla es un dictamen jurídico.** Significa «compatible según la licencia
   identificada»; las obligaciones concretas y el árbol transitivo se revisan antes de R3.
6. **Que el proyecto sea Apache 2.0 no cubre cada peso que se descargue.** Vale para
   `PaddleOCR-VL`, verificado; **no se extrapola** a `PP-OCRv5` ni a los pesos de docTR. Cada
   artefacto se fija por su cuenta, con versión o hash.

### La cadena de derechos · cinco preguntas antes de incorporar nada

No basta preguntar «¿la licencia permite software propietario?». El registro debe responder:

```
1. ¿QUÉ incorporamos?            artefacto concreto, no proyecto
2. ¿DE DÓNDE proviene?           repositorio, commit o hash fijado
3. ¿BAJO QUÉ LICENCIA?           la del artefacto, verificada en su origen
4. ¿QUÉ ARRASTRA?                dependencias transitivas y pesos
5. ¿QUÉ HACEMOS con él?          usar · invocar · modificar · redistribuir
```

Las cinco contestadas → recién entonces se evalúa el grado.

### Frontera de propiedad · y el contrato pobre

```
        TERCEROS                          QUIRA
   ┌────────────────┐  contrato   ┌──────────────────────┐
   │ motor OCR      │  propio     │ normalización        │
   │ EXTRAE         │ ─────────►  │ trazabilidad · SHA   │
   │                │             │ evidencia · canon    │
   └────────────────┘             │ Gold Master · CNO/RO │
                                  └──────────────────────┘
```

**El tercero EXTRAE. QUIRA interpreta conforme al canon.** Y hay una segunda pregunta que la
licencia no cubre y que importa igual (colega · 2026-08-18): **¿qué información nuestra le
estamos entregando al componente externo?** Una dependencia MIT perfectamente permisiva sigue
siendo un error estratégico si le pasamos el canon.

Por eso el adaptador OCR de QUIRA tendrá un **contrato deliberadamente pobre**:

| recibe | devuelve | NUNCA recibe |
|---|---|---|
| imagen · página · documento | texto · *bounding boxes* · confianza · orden de lectura · regiones · metadatos técnicos | CNO · RO · Gold Master · SITA · ICPI · ponderaciones · criterios de cumplimiento |

Así, cambiar de motor —Tesseract, PaddleOCR, docTR, ONNX o uno propio— **no mueve la frontera
de propiedad**. Es la misma disciplina de ADR-051 aplicada a las dependencias: el instrumento
no sabe qué está mirando.

### Grados, precisados para artefactos externos (2026-08-18)

| Grado | Qué significa |
|---|---|
| **R0** | se observa el proyecto |
| **R1** | se estudia arquitectura o interfaz · sin código |
| **R2** | **candidato técnico**: puede someterse a benchmark, **todavía NO entra en QUIRA** |
| **R3** | **incorporable**: las ocho condiciones en verde a la vez |

```
R3 =  benchmark técnico ✅   licencia del código ✅   licencia de pesos ✅
      dependencias ✅        procedencia/versión ✅   cadena de derechos ✅
      contrato del adaptador ✅                       aislamiento del canon ✅
```

> **R3 no significa «funciona». Significa «funciona y podemos demostrar que tenemos derecho a
> usar exactamente lo que estamos usando, exactamente de la manera en que lo usamos».**

### Estado y siguiente paso

| Etapa | Estado |
|---|---|
| A · cantera y cadena de derechos por artefacto | ✅ hecho (esta tabla) |
| A2 · **inventario visual del corpus** | ⏭️ **bloquea B** — ver abajo |
| B · benchmark contra caso real | ⏭️ tras el inventario |
| C · adaptador propio con contrato pobre | ⏭️ tras el benchmark |
| D · decisión de grado y registro | ⏭️ sólo con prueba superada |

#### ⚠️ El OCR NO es el bloqueo del dominio (2026-08-18 · corrección de alcance)

Se dijo que el OCR bloqueaba «123 documentos del numeral 17». Al abrir los 13 ZIP de ese numeral
aparecieron **260 archivos: 120 jpg, 100 jpeg, 39 png y 1 mp4 — ningún PDF, XLS ni DOC**. Son
fotografías de eventos, no registros de asistencia.

**Un OCR perfecto no resolvería ese numeral**: el problema es de universo documental, no de
legibilidad. El OCR hace falta para **24 documentos** —15 del numeral 15 y 9 del 18, escaneos
reales de contratos colectivos y convenios—, y esos son los que deben formar la muestra.

#### ⚠️ Corrección · la primera muestra no era representativa (2026-08-18)

El banco preparó 20 archivos y se describieron como *«registros de asistencia con tablas, firmas
y sellos»*. **Javo los abrió y son fotografías**: 20 JPG, todas nítidas, sin tablas, formularios,
matrices, multipágina, rotación ni degradación.

El error fue de método y es el mismo que se venía corrigiendo todo el día: **el nombre del campo
normativo se tomó por descripción del contenido.** La guía llama al enlace «registro de asistencia»
y se dedujo qué habría dentro sin abrir un solo archivo.

    corpus OCR: 123 documentos identificados
    muestra preliminar: 20 JPG · NO representativos
    estratificación: pendiente de inventario visual

**No se escribe «20/123»** para que nadie lea dentro de unas semanas que el banco ya tiene una
muestra defendible. Y la estratificación no se inventa: primero se miran los 123 y **después** se
definen las categorías que el corpus realmente contiene — no las que un OCR suele encontrar.

*Que esto se detectara antes de instalar un motor es exactamente para lo que el harness se
escribió primero.*

| Artefacto | Grado hoy |
|---|---|
| tesseract · tessdata · leptonica | **R2** — candidato en evaluación · cadena de derechos limpia. **NO es «el motor recomendado»**: R2 significa que puede entrar al banco, no que haya ganado |
| PaddleOCR + PaddleOCR-VL | **R2** — licencias localizadas; `PP-OCRv5` pendiente |
| OCRmyPDF | **R1/R2** — MPL-2.0, evaluar si se invoca o se prescinde |
| docTR | **R1** — pesos sin declaración localizada |

**No se instala nada todavía.** ADR-050 §4: *«la prueba contra caso real es obligatoria y precede
a la decisión»*.

---
*Registro de ADR-050 · Dylus Lab © 2026*
