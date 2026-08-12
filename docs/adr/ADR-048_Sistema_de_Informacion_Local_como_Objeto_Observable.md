---
id: ADR-048
authority:
  parent: ADR-041
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTO — pendiente de sello (ADR-035 §5)
fecha: 2026-08-12
---

# ADR-048 · El Sistema de Información Local como objeto observable

> **Qué decide.** Que el SIL —la capacidad del GAD para producir, custodiar, integrar y respaldar
> información oficial local— es un **objeto observable de QUIRA**, con cadena normativa propia; y
> cómo se separa de la gestión, de la transparencia y del cálculo canónico.
>
> **Qué NO decide.** No crea un dominio. No crea un índice. No crea una fórmula. No modifica
> `H12!B33` ni ninguna variable del motor. No convierte a QUIRA en productor de estadística.

## 1 · El hallazgo que obliga a escribir esto

Durante la curación del Gold Master (agosto 2026) se acumularon hallazgos que se venían leyendo
como defectos del instrumento. Puestos juntos, no lo son:

| Hallazgo | Lo que se creyó | Lo que es |
|---|---|---|
| El POA 2026 pierde la columna de meta (OBS-027) | falla de planificación | pérdida de capacidad informacional |
| La cédula del Numeral 6 trae menos estructura que la que reemplazó (OBS-028) | cambio de formato | ídem |
| El PDOT no tiene llave primaria (OBS-026) | descuido de redacción | ausencia de identidad de los objetos |
| La ordenanza vigente: 242 páginas, **241 caracteres** de texto | problema de OCR | la norma no es procesable |
| El Patronato publica su conjunto de datos en Word | detalle administrativo | el dato abierto no es dato |
| `V_SERCOP ≡ V_eSIGEF` en 25/25 filas | coincidencia | el verificador no verifica |
| Bomberos ejecuta $1,75 M sin meta asignada (OBS-024) | desalineación | el vínculo no es reconstruible |

> **Ninguno es un hallazgo sobre la gestión del cantón. Todos lo son sobre su sistema de
> información.** QUIRA llevaba semanas midiendo el SIL sin haberlo nombrado.

De ahí se sigue algo que el motor no puede resolver: **un GAD que ejecuta bien y no puede
demostrarlo puntúa igual que uno que no ejecuta.** El índice canónico mide congruencia de gestión;
no tiene forma de expresar si el municipio *puede saber* lo que afirma. Son dos preguntas
distintas y hoy se responden con una sola cifra.

## 2 · La cadena normativa — verificada, no inferida

El SIL no es una figura que QUIRA proponga. Existe, es obligatorio y tiene norma técnica propia.

**Norma Técnica para la Creación, Consolidación y Fortalecimiento de los Sistemas de Información
Local** · Acuerdo **SNPD-056-2015**, R.O. 556 de 31-VII-2015 · reformado por Acuerdo
**SNPD-006-2018**, R.O. 194 de 06-III-2018.

| | sha256 | carácter |
|---|---|---|
| Texto 2015 **consolidado** con la reforma | `02aa4f4531a34509deb517bf81a22bd2…` | **norma vigente** |
| Acuerdo reformatorio 2018 | `2d1440cca495586feda51932b342d010…` | sustituye Arts. 4·5a·9·11·13·14·15 |

> **Precisión que costó una discusión y vale conservarla.** El acuerdo de 2018 **no contiene
> cláusula derogatoria alguna**: reforma por sustitución de artículos y adapta la norma a la nueva
> estructura del Sistema Nacional de Planificación. Los artículos que sostienen todo lo que sigue
> —**2, 6 y 8**— **no fueron tocados y existen sólo en el texto de 2015**. Archivar ese texto como
> derogado equivale a perder la obligatoriedad del SIL y el mandato de respaldo documental.
> *Cambió el aparato institucional, no el mandato.*

### Los tres artículos que anclan esta decisión

**Art. 2 — Ámbito de aplicación** *(íntegro de 2015)*
> «Esta Norma se implementará de manera **obligatoria** en los Gobiernos Autónomos
> Descentralizados, provinciales, metropolitanos y municipales, entidades que deberán **crear,
> institucionalizar y fortalecer** sus Sistemas de Información Local.»

**Art. 8 — De la información a ser administrada por los GAD** *(íntegro de 2015)*
> «Toda información contenida en el Sistema de Información Local deberá contar con los respectivos
> **respaldos documentales y metodológicos**.» *(y podrá alimentarse de la generada en sus
> **empresas públicas**)*

**Art. 6 — De la vinculación con la Planificación y el Ordenamiento Territorial** *(íntegro de 2015)*
> La información incorporada al SIL «será utilizada principalmente como insumo para los procesos de
> actualización, formulación, articulación, **seguimiento y evaluación** de los planes de desarrollo
> y ordenamiento territorial».

**Art. 4 — Definición** *(sustituido por SNPD-006-2018)*
> «conjunto organizado y sistemático de elementos —dependencias técnicas y administrativas; talento
> humano; medios técnicos; procedimientos; productos informativos— que permiten la interacción de
> los GAD con la ciudadanía en el territorio, **en el marco de la rendición de cuentas y control
> social**; para acceder, recoger, almacenar, transformar y difundir datos en información
> relevante…»

> **El Art. 8 no describe una aspiración de QUIRA: pide literalmente lo que la capa derivada de
> `cruce_poa_cedula.py` construye.** La arquitectura de procedencia no es una capa tecnológica
> añadida sobre la norma — es una forma contemporánea de cumplirla.

## 3 · Cuatro planos que no deben confundirse

**El SIL no es un dominio de QUIRA.** Un dominio es algo que QUIRA cura; el SIL es algo que QUIRA
observa. Meterlo como dominio introduciría el objeto observado dentro del observador.

| Plano | Qué es | Quién lo sostiene |
|---|---|---|
| **SIL** | capacidad del GAD de producir, custodiar, integrar y respaldar información oficial local | **el GAD** — obligación normativa propia |
| **QUIRA Observatorio** | observa esa capacidad y la evidencia que produce | QUIRA · F1 |
| **QUIRA Institucional** | puede fortalecer esa capacidad, u operar como infraestructura del SIL | QUIRA · F2 |
| **Motor canónico** | mide congruencia de la gestión | Gold Master · intocable |

> **Capacidad informacional ≠ gestión ≠ transparencia ≠ ejecución ≠ resultados.** Un GAD puede
> tener mucha información y mala calidad; poca información y excelente trazabilidad; muchos
> documentos y ningún sistema; buen SIL y baja ejecución. Colapsar esos casos en una cifra
> destruye justamente lo que hace falta saber.

## 4 · El cortafuegos — y es la parte que puede romper la tesis

ADR-041 §4-ter admite licencia de gestión al GAD y sostiene que ello «no lo hace cliente de la
observación». Esa cláusula se escribió pensando en **gestión**. No previó el caso que este ADR
abre: que **la evidencia misma nazca de una herramienta de QUIRA**.

> **Si QUIRA Institucional opera como SIL de un GAD, el Observatorio pasaría a medir datos que
> QUIRA produjo.** Un observatorio que califica la capacidad informacional de un municipio cuyo
> sistema de información provee no puede tratar esa medición como evidencia independiente.

**Decisión.** La custodia se declara siempre, y el techo lo fija la procedencia (ADR-046: *el techo
lo pone el documento, no el portador*):

| Origen de la evidencia | Techo de verificabilidad |
|---|---|
| Fuente oficial publicada por el GAD, capturada por el Observatorio | hasta `independiente` |
| Producida o intermediada por infraestructura de QUIRA Institucional | **máximo `institucional`** |
| No declarada | **inadmisible** — no se publica |

No es una restricción cosmética: **una evidencia cuya procedencia no puede declararse no entra.**

## 5 · Evidencia mínima de un SIL — las dimensiones, sin fórmula

Derivadas del Art. 8 (respaldo documental **y metodológico**) y de lo hallado en la curación:

| Dimensión | Pregunta |
|---|---|
| Existencia | ¿existe el dato? |
| Procedencia | ¿de qué documento, hoja, fila y período sale? |
| Método | ¿se sabe cómo fue producido? |
| Temporalidad | ¿a qué corte corresponde? |
| Territorialización | ¿está localizado? |
| Actualización | ¿se sostiene en el tiempo? |
| Interoperabilidad | ¿puede cruzarse con otras fuentes? |
| Reconciliabilidad | ¿puede vincularse con los demás instrumentos? |

> **No se define índice, ponderador ni fórmula.** Hacerlo hoy repetiría exactamente el error de
> `Ei` (OBS-025): una variable que entra al cálculo sin cadena normativa que la sostenga. Primero
> la doctrina y la evidencia; la métrica, si llega, llega después y con su propio ADR.

## 6 · Estados epistemológicos — la regla que este ADR eleva a canon

Un `0/1` no distingue «no ocurrió» de «no encontré». Esa confusión ya produjo daño verificable:
el derivador declaró `sin_registro_presupuestario` en una meta con **$187.200 devengados** en otra
de sus partidas.

**Decisión.** Toda reconciliación conserva estado tipado, y ninguno se colapsa antes de que una
variable canónica decida qué es computable:

| Estado | Qué afirma |
|---|---|
| `devengado_certificado` | hay ejecución acreditada |
| `codificado_sin_devengado` | hay asignación sin ejecución |
| `partida_no_hallada_en_cedula` | no aparece en la fuente consultada |
| `ejecución_no_atribuible` | hay ejecución en la línea; el monto no es atribuible a esta meta |
| `sin_partida_declarada` | **la fuente** no ancla partida |
| `no_reconciliado` | **nuestro procedimiento** no la alcanzó |
| `reconciliacion_ambigua` | dos objetos comparten enunciado; no se elige por conveniencia |

> **`no_reconciliado` habla de nosotros; `sin_partida_declarada` habla de la fuente.** Colapsarlos
> convierte un límite del observador en un defecto del observado. **Ausencia de evidencia ≠
> evidencia de ausencia**, y el derivador no está exento (Regla de Oro 3).

## 7 · Capa derivada inmutable

**Ninguna reconciliación modifica una fuente.** Toda derivación nace como capa aparte y conserva
archivo, hoja, fila, partida, período y método. Si mañana una partida cambia por reforma, o una
cédula mensual difiere de la de diciembre, debe poder reconstruirse **por qué** el derivador dijo
lo que dijo. Implementación de referencia: `data/pdot/cruce_poa_cedula.json`.

## 8 · Relación con el sistema estadístico nacional

La propia norma resuelve esto, y no hace falta opinar. Dispone que la calidad de la información
local se valore **según los lineamientos metodológicos del INEC** —Código de Buenas Prácticas
Estadísticas; Norma Técnica para la Producción de Estadística Básica—.

> **El SIL no compite con el INEC: se mide con la vara del INEC.**

**Decisión.** QUIRA **no produce estadística oficial** ni la sustituye. El GAD produce información
oficial **dentro del ámbito de sus competencias** y territorializada; la capa nacional sigue siendo
la referencia estadística. La formulación admisible:

> El GAD municipal debe disponer de capacidad institucional para producir, integrar, territorializar,
> validar y respaldar información oficial local en el ámbito de sus competencias, interoperando con
> los sistemas nacionales y **sin sustituir** las competencias estadísticas de los órganos rectores.

⛔ **No admisible en canon ni en producto:** «el GAD debe crear información oficial para todo y
todos» · «la provincia es una línea imaginaria». Provincia y país son circunscripciones reales con
competencias propias. Lo defendible es que **el cantón es la escala donde el territorio deja de ser
abstracción**.

## 9 · Prueba metodológica — por qué esto no es una hipótesis

La cadena `meta → partida → devengado` se sometió deliberadamente a los casos **fuera** de las 25
metas donde ya se conocían los defectos de H13:

| | dentro del motor | fuera |
|---|---|---|
| Metas | 23 | **43** |
| Derivables | 18 · 78 % | **28 · 65 %** |
| `no_reconciliado` | 5 | 15 |
| Atribución unívoca | 2 | **7** |

La cadena no se degrada fuera de su muestra de origen, y las 25 del motor resultaron ser —en
atribución— las **peores** del conjunto. Los 15 `no_reconciliado` se conservaron como tales: **no
se rellenó ninguno para mejorar la cobertura.**

> **No se persigue un porcentaje.** El contraste contra H13 no mide corrección: mide coincidencia
> con una asignación manual cuyos ceros no sobreviven al contraste con la cédula (5 de 6). H13 es
> paciente, no juez.

## 10 · Invariantes

1. El SIL es **objeto observado**, nunca dominio ni módulo de QUIRA.
2. Ninguna derivación modifica una fuente. La capa derivada es aparte y trazable.
3. Ningún estado se colapsa a binario antes de que una variable canónica lo decida.
4. `no_reconciliado` **jamás** se publica como incumplimiento.
5. Evidencia intermediada por QUIRA Institucional: techo `institucional`, custodia declarada.
6. Este ADR **no crea métrica**. Cualquier índice de capacidad informacional exige ADR propio con
   cadena normativa verificada, so pena de repetir `Ei`.
7. Sin norma verificada con SHA, no hay dato (Regla de Oro 3) — **incluida la norma del SIL**.

## 11 · Trazabilidad

| Fuente | sha256 | Carácter |
|---|---|---|
| Acuerdo SNPD-056-2015 consolidado (Arts. 2·6·8) | `02aa4f4531a34509…` | norma vigente |
| Acuerdo SNPD-006-2018 (reforma Arts. 4·5a·9·11·13·14·15) | `2d1440cca4955866…` | reformatorio |
| Ordenanza 07-2024-CM-GADMCM (Word procesable) | `285d54244305d61d…` | oficial · sancionada 05-XI-2024 |
| Ordenanza 07-2024-CM-GADMCM (PDF firmado) | `662756aac591b247…` | oficial · escaneado, 241 car. |
| Acuerdo Ministerial SNP-SNP-2023-0049-A · guía PDOT | `f3b8ed699e64` (corpus) | actualización al inicio del período |

## 12 · Consecuencias abiertas

- **Ingesta al corpus** de la ordenanza en Word y de las dos normas del SIL — decisión de Javo
  (costo de *embeddings*).
- **OBS pendiente** sobre la no independencia de `V_SERCOP` y `V_eSIGEF` (25/25 idénticos).
- **Revisión jurista** de la clasificación de competencias, ya en `ACK_REGISTRY` desde julio.
- La ordenanza escaneada **valida la propuesta de OCR del colega del GAD** con un caso concreto:
  la norma que da vigencia al plan no era legible por máquina.

---
*ADR-048 · Dylus Lab © 2026 · hallazgo de Javo · corrección de alcance del colega · cadena normativa verificada documento por documento.*
