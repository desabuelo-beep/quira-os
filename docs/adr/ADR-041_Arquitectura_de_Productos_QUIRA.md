---
id: ADR-041
authority:
  parent: CONSTITUCION-001
  constitution_articles: [1, 2, 4, 5]
  type: ARQUITECTONICA
status: APROBADO — sellado por Javo (2026-08-07)
fecha: 2026-08-05
---

# ADR-041 · Arquitectura de productos de QUIRA · el Centro como núcleo

> **Decisión de Javo (2026-08-05).** QUIRA deja de organizarse por *tipo de usuario* y pasa a
> organizarse por **misión operativa**. Cambia el orden de construcción y se aclara qué es
> producto, qué es ambiente y qué es núcleo.

## 1 · Por qué se abre este ADR

La pantalla de acceso publica una arquitectura que ya no corresponde. Javo: *"es una versión
muy muy antigua y no representa nada de lo que tenemos ahora; tanto así que al observatorio
entramos por institucional"*. Corregir la pantalla sin corregir antes el canon habría
implementado en Python una arquitectura que el canon no declara — **Regla 9: ningún cambio
nace en Python**. De ahí este documento, y no un rediseño directo.

## 2 · Tres planos que no deben confundirse

Javo señaló que *"el observatorio nació como operaciones"*, y `NOMENCLATURA_CANONICA.md` dice
que **"OPS no es una plataforma pública; no aparece como tarjeta en la landing"**. La primera
versión de este ADR resolvió la tensión diciendo que *"el Observatorio es la cara pública de
lo que OPS ejecuta"*. **Javo lo corrigió, y con razón** (2026-08-05):

> *"QUIRA Operaciones es trabajo directo y único de Dylus Lab, por eso no lo tomamos; no es
> producto, sino la sección de mantenimiento del ecosistema. Eso es otra cosa."*

No son dos caras de lo mismo: son **funciones distintas**. El Observatorio **produce
conocimiento** —Javo monitorea los GAD con QUIRA IA—; Operaciones **mantiene la máquina** que
lo hace posible. Atarlos habría hecho creer que el panel del Observatorio es la consola de
mantenimiento, y no lo es.

| Plano | Qué es | Ejemplo | ¿Público? |
|---|---|---|---|
| **Producto** | genera o incorpora conocimiento | Observatorio · QUIRA Ciudadana | sí |
| **Mantenimiento** | sostiene el ecosistema | Operaciones — Dylus Lab, uso interno | **no, y no es producto** |
| **Motor** | calcula (ADR-023, inmutable) | Gold Master | no — se lee, nunca se expone |
| **Núcleo** | dónde converge y se lee el conocimiento | Centro de Inteligencia Territorial | sí, vía productos |

## 3 · Un solo motor, dos entradas

Segunda corrección, esta de la propia dirección técnica al releer el ADR con la explicación de
Javo delante: **el primer diagrama ponía los productos escribiendo directo al Centro, y eso se
salta el motor** — contra ADR-023, que es inmutable. La formulación de Javo pone el orden
correcto: *"tenemos un solo motor, que se alimenta con nuestro producto principal QUIRA
Observatorio… y por otro lado con otra entrada, QUIRA Ciudadana"*.

```
  QUIRA Observatorio ──┐
  (Dylus monitorea)    │
                       ├──→   MOTOR   ──→   CENTRO DE INTELIGENCIA TERRITORIAL
  QUIRA Ciudadana ─────┘   (Gold Master)                    │
  (control social)                                          │
                                        consumen ───────────┤
                                        · QUIRA Cooperación / Impact
                                        · Observatorio
                                        · QUIRA Economic
```

**Dos entradas de evidencia, un motor, un núcleo de lectura.** Los productos posteriores no
son otra fuente: **consumen** lo que las dos entradas construyeron. Eso evita el peor final
posible —varias bases de conocimiento contradiciéndose— y respeta la arquitectura de tres
niveles sin abrirle una puerta lateral.

## 4 · El orden no es de prioridad: es de DEPENDENCIA

| Fase | Productos | Misión |
|---|---|---|
| **1** | **Observatorio** · **QUIRA Ciudadana** | **construir la evidencia** |
| 2 | QUIRA Cooperación / Impact · Observatorio | ofrecer inteligencia a partir de esa evidencia |
| 3 | QUIRA Economic | inteligencia económica del territorio |

**El orden no es una preferencia: es una restricción.** Javo lo formula así: *"con estas dos
QUIRAs podríamos completar la información nacional que le dará vida a QUIRA Impact"*. Impact no
está en Fase 2 porque sea menos importante — **no puede existir antes**: su valor para
universidades, bilaterales y ONG es la cobertura nacional, y esa cobertura la producen las dos
entradas de Fase 1. Construirlo antes daría un producto sin nada que ofrecer.

**Cambia respecto del canon vigente** (`BOOT §LA TESIS` decía Fase 1 = Operaciones · Ciudadana
· Institucional; `NOMENCLATURA_CANONICA` daba `civic` como Fase 3):

- **Institucional baja a Fase 2.** No es degradación: es coherencia con la Tesis —*"el GAD es
  SUJETO OBSERVADO, no cliente"*—. Javo: *"dejamos posterior a QUIRA GAD o institucional, ya
  que no vendemos software a municipios"*. Lo que hoy existe en el ambiente `gov` es la
  herramienta con la que Dylus Lab construye el molde, no el producto para el GAD.
- **Ciudadana sube a Fase 1.** Es entrada de evidencia, no consumo: sin ella y sin el
  Observatorio, los productos de Fase 2 no tienen qué leer.
- **Operaciones desaparece de la lista de productos.** Nunca lo fue.

## 4-bis · El universo son 222 GAD, no 221 — y el 222 no es comparable

El canon decía **221 GAD** en cinco lugares (BOOT ×2, ADR-024 ×3). Javo aportó la fuente y se
corrigieron los cinco:

| | |
|---|---|
| **Cantón 222** | **Sevilla Don Bosco** — Morona Santiago, Región Amazónica |
| Origen | parroquia rural del cantón Morona, separada de Macas por el río Upano |
| Consulta popular | 5 de febrero de 2023 — mayoría a favor de la cantonización |
| **Ley de creación** | **8 de octubre de 2024** — Asamblea Nacional, por unanimidad |
| Primeras elecciones | 17 de agosto de 2025 (CNE) |
| Primer alcalde | Carlos Fabricio Narváez — credenciales el 5 de septiembre de 2025 |

> ⏳ **Deuda documental:** el hecho está verificado por fuente pública, pero la **Ley de
> creación publicada en Registro Oficial** aún no está en el corpus con su SHA256. Mientras no
> lo esté, el dato se cita por su fuente, no por su norma sellada (Regla 3).

### La consecuencia que no es aritmética

Sumar uno al universo es lo de menos. **Sevilla Don Bosco no tiene histórico comparable con
los otros 221**, y el radar nacional debe saberlo desde su diseño:

| Instrumento | Situación del GAD 222 |
|---|---|
| PDOT 2023-2027 | **no existe** — el cantón se creó después del ciclo |
| Rendición de cuentas 2023 · 2024 | **no aplica** — no había autoridad que rindiera |
| ICM 2023 · 2024 | **no aplica** — sin PDOT vigente que medir |
| Serie histórica de ejecución | arranca en 2026, primer ejercicio completo |

Es exactamente **R-H** —*no se comparan horizontes distintos*— aplicada a un sujeto nuevo. En
un ranking nacional, un GAD sin histórico aparecería con los peores indicadores por una razón
que no tiene que ver con su gestión: **todavía no ha tenido tiempo de generarlos**. Ponerlo en
la misma tabla sin marcar su condición produciría una afirmación falsa por construcción.

**El radar necesita, desde el diseño, un estado `sin ciclo comparable`** — igual que el
sistema ya distingue `inverificable` de `no atendido`. Se registra, se muestra, no se computa
en comparaciones ni en promedios nacionales.

## 4-ter · "No cliente" significa "no cliente de la OBSERVACIÓN"

Javo (2026-08-05) planteó el caso real: *"¿si el GAD Montecristi, que es la validación
empírica, una vez ve el producto nos pide software para su gestión?"* — y con razón: los
módulos de gestión existen, fueron la idea primera, y negarse cerraría una vertiente
escalable. *"También pienso como fundador y a nivel de economía."*

**No hay contradicción con la Tesis, pero la formulación era imprecisa.** Lo que la Tesis
protege no es la ausencia de ingresos: es que **el observado no pueda influir sobre la
observación**. La línea, explícita:

| ⛔ Nunca | ✅ Sí, y con soporte |
|---|---|
| Pagar por ser observado, por la evaluación o por lo que se publica | Licenciar herramientas para gestionar lo propio con la evidencia ya publicada |
| Contratar para que un hallazgo cambie, se matice o se retire | Licencia **independiente**, con soporte de Dylus Lab |
| Condicionar la cobertura de un municipio a que contrate | Contratar **no modifica una sola línea** de lo que el Observatorio publica sobre él |

Analogía que lo zanja: **nadie le paga al instituto de estadística para que le cambie el
censo, pero cualquiera puede contratar herramientas para trabajar con esos datos.** La
observación es pública e independiente; las herramientas de gestión son otro producto.
Separarlas explícitamente es lo que permite ofrecer ambas sin que una contamine a la otra.

> ⚠️ **Punto que sí toca decidir a Javo:** `BOOT §LA TESIS` dice *"negocio = complementario,
> **no licencias**"*. Esta vertiente lo contradice. Pero es **estrategia comercial, no
> doctrina epistemológica** —la doctrina es "sujeto observado", y queda intacta—, así que es
> decisión del fundador, no de la dirección técnica. Mientras no se resuelva, el BOOT y la
> landing dicen cosas distintas.

## 5 · Qué hace cada producto de Fase 1

### 5.1 · Observatorio — el producto principal · genera evidencia de forma proactiva

Panel de control desde el que se despachan agentes a los sistemas del Estado, con monitoreo
mensual y cobertura progresiva de GAD:

```
scheduler mensual → agentes → captura → CENTRO → validación humana → publicación
```

Fuentes: transparencia (LOTAIP) · SERCOP · CPCCS · SIGAD · portal institucional · PAC · POA ·
presupuesto · rendición de cuentas.

El eslabón **validación humana** no es opcional: ADR-035 fija que *la IA propone y el humano
valida*, y la Constitución Institucional Art. 3 que *la inteligencia artificial no constituye
fuente de verdad institucional*.

### 5.2 · QUIRA Ciudadana — la segunda entrada · el control social, operacionalizado

No es "la versión pública del Observatorio": es una **entrada distinta de evidencia**, y su
fundamento no es comercial sino constitucional — el control social que *"manda la Constitución
y la ley"* (Javo). Alcance nacional desde el primer día, porque el derecho lo es.

Dos funciones, y **su naturaleza jurídica no es la misma**:

| Función | Qué es | Estatuto |
|---|---|---|
| **Constructor de solicitudes** de acceso a información pública | operacionalizar la **vía 2** de R-F | ✅ ya canónico |
| **Aporte documental** ciudadano | documento cuya cadena de custodia QUIRA no controló | ⚠️ **§6** |

El constructor de solicitudes no necesita canon nuevo: **R-F ya establece que solicitar es
ejercer la norma, no contaminar el objeto**. QUIRA Ciudadana pone esa vía al alcance de
cualquiera, que es exactamente operacionalizar un derecho público.

## 6 · El problema que este ADR abre y no cierra

**Las vías canónicas de ingesta son tres** (R-F.1): transparencia activa, transparencia pasiva
y silos intersistémicos. **Un documento aportado por un ciudadano no es ninguna de las tres.**

Sin resolverlo, el aporte ciudadano contaminaría el Universo Documental Cerrado: entraría
evidencia sin cadena de custodia verificable junto a evidencia oficial, y todo el sistema
descansa en poder distinguirlas (Art. 1 y 2 de la Constitución Institucional).

**No se resuelve inventando una cuarta vía.** El canon ya tiene el instrumento: la escala de
verificabilidad de la Constitución Ontológica —*independiente · institucional · parcial · sin
evidencia · contradicción*—. Un documento ciudadano no entra ni rechazado ni equiparado: entra
**clasificado**.

| Caso | Verificabilidad propuesta |
|---|---|
| Respuesta oficial a una solicitud, con acuse institucional | **institucional** |
| Documento sin acuse, corroborable contra un silo del Estado | **parcial** hasta corroborar |
| Documento sin acuse ni corroboración posible | **sin evidencia** — se registra, no se computa |

> ⛔ **Queda como decisión abierta de Javo.** Esta clasificación es una propuesta de la
> dirección técnica, no una decisión tomada. Afecta a R-F, que es suyo.

## 7 · Consecuencias

| # | Qué se toca | Estado |
|---|---|---|
| 1 | `NOMENCLATURA_CANONICA.md` — fases de `civic` e `impact`; Observatorio como producto de `ops` | ✅ propagado (2026-08-07) |
| 2 | `BOOT §LA TESIS` — orden de fases | ✅ propagado (2026-08-07) |
| 3 | Pantalla de acceso — reconstrucción sobre esta arquitectura | ✅ hecha (2026-08-06) |
| 4 | R-F — estatuto del aporte ciudadano (§6) | ⛔ decisión de Javo |

### 7-bis · Lo ya implementado sin esperar el sello, y por qué

La pantalla de acceso se reconstruyó porque **publicaba una arquitectura que ya no existía**
—era el defecto que abrió este ADR— y dejarla así seguía mostrando al mundo un modelo
retirado. Se implementó lo que el ADR describe: una sola puerta, el Observatorio; Operaciones
fuera de la portada; el Centro como núcleo.

De ahí derivó, ya con el modelo delante, la infraestructura que le faltaba: **ADR-042**
—aprobado el 2026-08-07— separa el Observatorio (la función) de la Consola de Monitoreo (la
infraestructura que la ejecuta) y de Operaciones (mantenimiento técnico), y fija que la
integración pasa por la MATRIZ_CANONICA y no por el Gold Master.

**Lo que sigue esperando el sello es el canon escrito**, y con razón: mientras este ADR no se
selle, `BOOT §LA TESIS` mantiene el orden vigente —*Fase 1 = Operaciones · Ciudadana ·
Institucional*—, que **contradice** el §4 de este documento (Fase 1 = Observatorio +
Ciudadana; Operaciones no es producto). Esa contradicción es visible y deliberada: cambiar el
BOOT antes del sello sería dar por decidido lo que no lo está.

## 8 · Lo que este ADR NO decide, y conviene decirlo

**El costo de operación.** El monitoreo mensual con agentes sobre 222 GAD consume API, y hoy
no hay presupuesto para ello (Javo · 2026-08-05). **Definir la arquitectura no cuesta nada;
ejecutarla sí.** El Observatorio puede diseñarse y construirse su panel ahora, y arrancar el
despacho de agentes cuando haya créditos — municipio por municipio, empezando por el molde.

Confundir ambas cosas llevaría a no construir nada por falta de fondos, o a construir un
sistema que no se puede encender.

---
*ADR-041 · Dylus Lab © 2026 · decisión de Javo · deriva de CONSTITUCION-001 · propuesta, sin sellar.*
