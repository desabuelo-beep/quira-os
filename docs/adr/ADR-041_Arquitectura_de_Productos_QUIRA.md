---
id: ADR-041
authority:
  parent: CONSTITUCION-001
  constitution_articles: [1, 2, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTA — pendiente de sello de Javo (ADR-035 §5)
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

## 2 · La distinción que resuelve la contradicción

Javo señala que *"el observatorio nació como operaciones, así que ese operaciones debe ser el
observatorio"*. Y `NOMENCLATURA_CANONICA.md` dice que **"OPS no es una plataforma pública; no
aparece como tarjeta en la landing"**. Ambas cosas son ciertas porque hablan de **planos
distintos** — la misma confusión producto/identidad que se corrigió hoy en el BOOT:

| Plano | Qué es | Ejemplo | ¿Público? |
|---|---|---|---|
| **Producto** | lo que el mundo ve y usa | Observatorio Nacional de Integridad Territorial | sí |
| **Ambiente** | dónde corre la maquinaria | `ops` — scheduler, agentes, colas, ETL, logs | **no** |
| **Núcleo** | dónde converge el conocimiento | Centro de Inteligencia Territorial | sí, vía productos |

**El Observatorio es la cara pública de lo que OPS ejecuta.** No se renombra `ops` a
"Observatorio": se declara que el Observatorio es el producto que OPS hace posible. La
maquinaria sigue sin aparecer en la landing.

## 3 · El Centro de Inteligencia Territorial es el NÚCLEO, no un producto

Todos los productos escriben y leen del mismo lugar. Esa es la consecuencia arquitectónica
más importante de esta decisión, y evita el peor final posible: cinco bases de conocimiento
que se contradicen entre sí.

```
   Observatorio ──┐                     ┌── QUIRA Institucional  (F2)
                  ▼                     ▼
            CENTRO DE INTELIGENCIA TERRITORIAL          ← núcleo único
                  ▲                     ▲
   QUIRA Ciudadana┘                     └── QUIRA Cooperación    (F2)
                                        └── QUIRA Economic       (F3)
```

## 4 · Las fases, reordenadas

| Fase | Productos | Misión |
|---|---|---|
| **1** | **Observatorio** · **QUIRA Ciudadana** | **construir la evidencia** |
| 2 | QUIRA Institucional · QUIRA Cooperación | ofrecer inteligencia al Estado y a la cooperación |
| 3 | QUIRA Economic | inteligencia económica del territorio |

**Cambia respecto del canon vigente** (`BOOT §LA TESIS` decía Fase 1 = Operaciones · Ciudadana
· Institucional; `NOMENCLATURA_CANONICA` daba `civic` como Fase 3):

- **Institucional baja a Fase 2.** No es una degradación: es coherencia con la Tesis —*"el GAD
  es SUJETO OBSERVADO, no cliente"*—. Lo que hoy existe en el ambiente `gov` es la herramienta
  con la que Dylus Lab construye el molde; el **producto para el GAD** llega después, cuando
  haya evidencia que ofrecerle.
- **Ciudadana sube a Fase 1.** Primero se construye la evidencia; sin ella los demás productos
  no tienen qué consumir.

## 5 · Qué hace cada producto de Fase 1

### 5.1 · Observatorio — genera evidencia de forma proactiva

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

### 5.2 · QUIRA Ciudadana — incorpora evidencia desde la sociedad

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
| 1 | `NOMENCLATURA_CANONICA.md` — fases de `civic` e `impact`; Observatorio como producto de `ops` | ⏳ tras el sello |
| 2 | `BOOT §LA TESIS` — orden de fases | ⏳ tras el sello |
| 3 | Pantalla de acceso — reconstrucción sobre esta arquitectura | ⏳ tras el sello |
| 4 | R-F — estatuto del aporte ciudadano (§6) | ⛔ decisión de Javo |

## 8 · Lo que este ADR NO decide, y conviene decirlo

**El costo de operación.** El monitoreo mensual con agentes sobre 221 GAD consume API, y hoy
no hay presupuesto para ello (Javo · 2026-08-05). **Definir la arquitectura no cuesta nada;
ejecutarla sí.** El Observatorio puede diseñarse y construirse su panel ahora, y arrancar el
despacho de agentes cuando haya créditos — municipio por municipio, empezando por el molde.

Confundir ambas cosas llevaría a no construir nada por falta de fondos, o a construir un
sistema que no se puede encender.

---
*ADR-041 · Dylus Lab © 2026 · decisión de Javo · deriva de CONSTITUCION-001 · propuesta, sin sellar.*
