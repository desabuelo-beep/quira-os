---
id: ADR-050
authority:
  parent: ADR-023
  constitution_articles: [1, 3, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTO — pendiente de sello (ADR-035 §5)
fecha: 2026-08-17
---

# ADR-050 · Cantera tecnológica — cómo QUIRA absorbe capacidades ajenas

> **Qué decide.** Cómo se evalúa, extrae, refactoriza y registra una capacidad proveniente de
> software externo, y qué procedencia debe conservar.
>
> **Qué NO decide.** No aprueba ningún repositorio. No autoriza dependencias. No sustituye ninguna
> decisión arquitectónica vigente.

## 1 · Por qué ahora

Javo (2026-08-17): *«usar EcuDataMCP como cantera tecnológica, evaluar qué componentes son
reutilizables, extraer lo que nos sirve, refactorizarlo bajo la arquitectura y estándares de QUIRA,
y hacer que QUIRA sea el producto y propietario conceptual de esa capacidad»*.

La estrategia es correcta y evita meses de reinventar infraestructura. Pero **sin política previa,
el primer commit que traiga código externo ya nos deja sin registro de dónde vino** — y eso es
incoherente con todo lo demás:

> Llevamos semanas exigiendo que **cada cifra pueda decir de dónde salió**. Sería insostenible que
> el código no pueda hacer lo mismo. **La procedencia del componente es tan exigible como la
> procedencia del dato.**

## 2 · La regla rectora

> **QUIRA no hereda productos. Hereda capacidades.**
> *(formulación del colega, 2026-08-13 — adoptada)*

Y su corolario, que fija la dirección de la subordinación:

> **La cantera sirve a QUIRA. QUIRA no se adapta a la cantera.**

Un proyecto externo entra sólo si **se somete** a la arquitectura, la nomenclatura, los gates y las
reglas epistemológicas vigentes. Si para incorporarlo hay que relajar una regla de QUIRA, **no
entra** — por bueno que sea.

### La trampa específica de esta estrategia

> **Tener la capacidad técnica de producir algo no es autorización epistemológica para producirlo.**

Una biblioteca que ofrece veintinueve tipos de diagrama no nos da veintinueve hallazgos: nos da
veintinueve tentaciones de dibujar relaciones que ningún motor estableció. Lo mismo con conectores
que devuelven campos que no sabemos interpretar. **La capacidad amplía lo posible; el canon decide
lo admisible**, y ADR-049 §VIS-INV-001 sigue mandando.

## 3 · Los cuatro grados de absorción

Ningún repositorio «se adopta». Cada capacidad recibe un grado, y el grado se declara:

| Grado | Qué significa | Qué se conserva del origen |
|---|---|---|
| **R0 · Referencia** | se estudia el proyecto; no se toma nada | cita en el registro |
| **R1 · Patrón** | se extrae una idea arquitectónica o visual, **sin código** | cita y descripción del patrón |
| **R2 · Componente** | se reutiliza código compatible con su licencia, refactorizado | licencia, versión, *commit*, atribución |
| **R3 · Capacidad QUIRA** | vive bajo arquitectura, nomenclatura, pruebas y reglas propias | genealogía en el registro |

> **R2 no es el final del camino, es una etapa.** Una capacidad que se queda en R2
> indefinidamente es una dependencia disfrazada.

⚠️ **Sobre licencias.** MIT permite reutilizar, modificar y redistribuir, **conservando el aviso de
copyright y la licencia**. Un *fork* no convierte código ajeno en propio. Lo que sí pertenece a
Dylus Lab es **la arquitectura construida alrededor y las modificaciones originales**, sujetas a la
licencia de origen.

## 4 · El procedimiento

```
fuente externa → identificación → licencia → versión/commit → capacidad candidata
      → PRUEBA CONTRA CASO REAL → decisión (R0-R3) → refactorización
      → validación con gates → registro de procedencia → componente QUIRA
```

**La prueba contra caso real es obligatoria y precede a la decisión.** No se adopta lo que «parece
funcionar»: se adopta lo que superó una batería contra evidencia que ya tenemos validada.

Para adquisición, esa batería existe y es concreta — los procesos SERCOP ya capturados y
reconciliados contra el PAC:

| Prueba | Criterio |
|---|---|
| Recupera el proceso conocido | identidad `ocid` exacta |
| Comprador · proveedor · estado | coinciden con lo capturado |
| Monto · fecha · partida | coinciden |
| Reproducibilidad | dos corridas, mismo resultado |
| Procedencia | conserva de dónde salió cada campo |
| Tiempo de respuesta | mejor o igual que la ruta actual |

**Si falla ahí, no se adopta.** Y si un componente externo no conserva procedencia, sólo puede
llegar a R1: la idea sirve, la implementación no.

## 5 · Registro de procedencia

Todo lo absorbido se anota en `docs/registry/CANTERA.md`, con: proyecto · licencia · versión o
*commit* · fecha de evaluación · capacidad extraída · grado · dónde vive en QUIRA · qué prueba
superó.

> **Sin entrada en el registro, el componente no existe para QUIRA.** Es la misma regla que
> VIS-INT-001 aplica a los elementos visuales, un nivel más abajo.

## 6 · Evaluación de los cinco candidatos actuales

Clasificación inicial. **Ninguno está aprobado**; ésta es la agenda de evaluación.

| Candidato | Capacidad de interés | Grado propuesto | Prioridad |
|---|---|---|---|
| **EcuDataMCP** | adquisición de fuentes públicas ecuatorianas · SERCOP/OCDS | **por evaluar** → R1 o R2 | 🟢 alta |
| **Cali Monitor** | monitoreo contractual · patrones de actualización | R0 · banco de pruebas | 🔵 baja |
| **diagram-design** | densidad deliberada · acento reservado | **R1 · sólo patrón** | 🔵 baja |
| **mono-charts** | microvisualización sobria | **R0 · referencia estética** | 🔵 baja |
| **CodeWiki** | documentación estructural del propio código | **R0** — ver §6.1 | ⚪ suspendido |

### 6.1 · Por qué `diagram-design` no es cantera principal

El colega lo propuso como cantera primaria de la capa visual. **La evaluación es la contraria**, y
por una razón que no es de gusto:

> **Ya tenemos gramática visual, y es más restrictiva que cualquier biblioteca de diagramas.**
> VIS-INV-001, 002 y 003, el gate de procedencia y el de coherencia arista↔nodo no existen en
> ningún repositorio de diagramas — porque ningún repositorio de diagramas tiene el problema de no
> poder afirmar de más.

Siete rondas de corrección costó que el objeto canónico no mintiera. Adoptar un sistema visual
coherente **por sí mismo** no añade capacidad: añade un vocabulario que compite con el nuestro. De
ahí se toma **un principio** —densidad deliberada, acento reservado a uno o dos elementos—, que es
justamente lo que a QUIRA le falta y no tiene nada que ver con tipologías.

### 6.2 · Por qué `CodeWiki` queda suspendido

Antes de traer un sistema con CLI, servidor, múltiples analizadores y orquestación de agentes, hay
que responder: **¿qué hace que CodeGraph —ya configurado en este proyecto— no haga?** Índice de
símbolos, aristas, trazas e impacto ya están cubiertos. Sin esa respuesta, el costo de absorción no
tiene contrapartida.

### 6.3 · La pregunta que decide sobre `EcuDataMCP`

Una sola, y es barata:

> **¿Consulta el mismo host que a nosotros nos corta, o encontró otra ruta de adquisición?**

Si encontró otra ruta, es prioritario: resolvería el cuello de botella real. Si encapsula la misma
fuente, no resuelve nada urgente y baja de prioridad. **No se evalúan sus 28 herramientas: se
evalúa si nos da lo que hoy no tenemos.**

## 7 · Invariantes

1. **La cantera sirve a QUIRA**; si incorporarlo exige relajar una regla propia, no entra.
2. Ninguna capacidad se adopta **sin prueba contra evidencia ya validada**.
3. Todo lo absorbido lleva **grado declarado** (R0-R3) y entrada en el registro.
4. **La procedencia del componente es tan exigible como la del dato.**
5. Un *fork* **no** transfiere titularidad; la licencia de origen se conserva.
6. **Capacidad ≠ autorización.** Poder dibujar o consultar algo no lo vuelve admisible.
7. La cantera está **subordinada al trabajo principal**: nunca desplaza la curación en curso.

---
*ADR-050 · Dylus Lab © 2026 · estrategia de Javo · taxonomía R0-R3 del colega · evaluación técnica del director.*
