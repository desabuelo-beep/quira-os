---
id: ADR-044
authority:
  parent: ADR-043
  constitution_articles: [1, 2, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTA — pendiente de sello de Javo (ADR-035 §5)
fecha: 2026-08-07
supersedes:
  - ADR-024 §Capa C
---

# ADR-044 · Rectificación de la taxonomía de productos heredada

> **Supersede `ADR-024 §Capa C`.** No lo edita: lo corrige desde aquí, dejando visible qué se
> dijo, qué resultó equivocado y por qué. La forma importa tanto como el fondo.

## 1 · Qué dice ADR-024 y qué de eso no se sostiene

`ADR-024 §Capa C — PRODUCTOS (interfaces sobre el mismo motor)` lista cinco:

```
- QUIRA Institucional → alcaldes y directivos (la médula del sistema)
- QUIRA Ciudadana     → ciudadanía, academia, OSC
- QUIRA Impact        → BID, CAF, PNUD, Banco Mundial
- QUIRA Economic      → inversión y desarrollo económico local
- QUIRA Cooperación   → elegibilidad y financiamiento internacional
```

Dos cosas quedaron mal, y ninguna fue un descuido de redacción: faltaba el criterio para
distinguir un producto de otro, y ese criterio no existió hasta ADR-043.

### 1.1 · Impact y Cooperación tienen el mismo destinatario

La lista asigna a **Impact** «BID, CAF, PNUD, Banco Mundial» y a **Cooperación**
«elegibilidad y financiamiento internacional». **Son el mismo público y la misma función
descritos dos veces.** Si dos productos comparten usuario y salida, ADR-043 §3 es explícito:
son una vista, no dos productos.

Y el error se propagó al código, donde vivió hasta el 2026-08-07: la clave del ambiente era
`impact` y su nombre público «Cooperación».

**Lo que sí los separa** —y no estaba escrito— es el contrato de salida:

| | QUIRA Cooperación | QUIRA Impact |
|---|---|---|
| Pregunta | ¿qué puede financiarse y con qué instrumento? | ¿qué pueden investigar y reproducir terceros? |
| Usuario | bilaterales · multilaterales · banca de desarrollo | academia · observatorios · investigadores |
| Entrega | elegibilidad, alineación, expediente, seguimiento | datos, series, metodología, trazabilidad |
| Naturaleza | **aplicación** a una decisión | **apertura** a la verificación |

Consumen la misma evidencia y el mismo motor. Lo que cambia es qué entregan y a quién —que
es, según ADR-043, lo único que constituye a un producto.

### 1.2 · QUIRA Ciudadana no es un producto de la Capa C

ADR-024 la lista como interfaz sobre el motor, junto a las demás. **ADR-041 §4 la reclasificó
como ENTRADA de evidencia**, y ADR-043 §2 lo formalizó: Observatorio y Ciudadana no explotan
el conocimiento, lo **producen**. Ponerlas en la misma columna que Cooperación o Impact
confunde quién alimenta el sistema con quién lo consume.

## 2 · Qué de ADR-024 sigue plenamente vigente

Esta rectificación es **quirúrgica**. Lo demás de aquel ADR se mantiene, y buena parte
sostiene todo lo que vino después:

- **La inversión de arquitectura**: el radar nacional es el producto, no la vitrina de un
  municipio. Es la decisión que dio origen a la escala de 222 GAD.
- **Capa B — Operaciones es una CAPACIDAD, no un producto.** Se confirma en ADR-041 §2 y
  ADR-042. Aquel ADR ya lo tenía bien, y quien lo desoyó fue el director en 2026-08-06 al
  alojar el Observatorio dentro de Operaciones.
- **Capa D — el portal como producto principal**, con el despliegue actual como laboratorio
  de validación.
- **QUIRA Institucional como producto para el GAD.** Sigue siendo correcto, con la precisión
  de ADR-043: el GAD puede ser usuario de una herramienta de gestión, **nunca sujeto que
  condicione la observación**.

## 3 · La taxonomía vigente

Manda ADR-043 §2 y §4:

| Categoría | Elementos |
|---|---|
| **Adquisición de evidencia** | Observatorio · QUIRA Ciudadana |
| **Núcleo** | Corpus + Grafo · MATRIZ_CANONICA · Gold Master · DOM · Centro |
| **Productos** | Institucional · Cooperación · **Impact** · Economic |
| **Capas transversales** | QUIRA IA · GeoTwin |
| **Mantenimiento** | Operaciones — no es producto |

## 4 · Por qué se rectifica con un ADR y no editando el anterior

**Un ADR sellado registra una decisión tomada con el vocabulario y la información de su
momento.** Cambiarle las palabras no corrige el error: borra la evidencia de que se cometió,
y con ella la posibilidad de entender por qué se decidió así.

La lección es reciente y costó cuatro reversiones. El 2026-08-07 un reemplazo automático de
«QUIRA Institucional» por «Observatorio» alcanzó a ADR-024, ADR-026 y al propio ADR-041 —que
acababa de sellarse—, y produjo afirmaciones falsas: que el Observatorio era a la vez entrada
de Fase 1 y consumidor de Fase 2, y que el GAD «opera el Observatorio como herramienta
diaria», lo que invierte la Tesis. **Ninguna de esas contradicciones estaba en los ADR: las
introdujo la edición.**

De ahí la regla que este ADR deja fijada:

> **Un ADR sellado no se edita. Se supersede.** La corrección vive en un documento nuevo que
> declara qué parte queda superada y por qué. La trazabilidad documental vale más que la
> pulcritud del texto viejo.

Aplica también al histórico, a los planes de sesión y a las capturas de pantalla: todo eso es
registro de lo que se dijo o se vio entonces.

## 5 · Consecuencias

| # | Qué | Estado |
|---|---|---|
| 1 | `ADR-024 §Capa C` queda superado por este documento | ✅ al sellar |
| 2 | Clave `impact` → `coop`, con `impact` reservado | ✅ hecho (2026-08-07) |
| 3 | `NOMENCLATURA_CANONICA §2` con la tabla vigente | ✅ hecho (2026-08-07) |
| 4 | Portada publicando la familia sin fases | ✅ hecho (2026-08-07) |
| 5 | Ambiente propio para `QUIRA Impact` | ⛔ no existe — no hay producto que servir todavía |

## 6 · Lo que este ADR NO decide

- **Cuándo se construye Impact.** Fija qué es y qué no; no su calendario.
- **Si Economic sobrevive.** ADR-043 lo dejó como línea futura por no pasar el gate de
  sostenibilidad, y ahí sigue.
- **El modelo de licencia de QUIRA Institucional**, que depende de una decisión comercial.

---
*ADR-044 · Dylus Lab © 2026 · rectifica ADR-024 §Capa C · deriva de ADR-043.*
