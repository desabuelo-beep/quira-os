---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 3, 4]
  type: ARQUITECTONICA
---

# ADR-052 · La naturaleza del objeto no es un estado de la evidencia

**Estado:** PROPUESTO · 2026-08-20 — pendiente de aprobación de Javo (ADR-035 §5)
**No toca** la Constitución Ontológica. Declara la separación que ésta necesitaría **antes** de
poder incorporar la propuesta que lo originó, y la condición bajo la cual se promovería.
**Relacionado:** CAPA 0 (Principio Rector) · ADR-042 §6 (semántica de estados) · Regla de Oro 3.

---

## Contexto

Javo, mirando veinte años hacia adelante:

> *«Que tu escala de verificabilidad tenga un sexto estado. Hoy tienes cinco —independiente ·
> institucional · parcial · sin evidencia · contradicción—. Todos son estados **de la evidencia**.
> Falta uno que sea un estado **del objeto**: "no verificable por naturaleza" — decisiones cuyo
> valor no es documentable y cuya ausencia de evidencia no es un hallazgo de auditoría sino una
> propiedad legítima. Sin esa categoría, tu propio sistema empuja al municipio a dejar de hacer lo
> que no puede documentar. Con ella, distingues el vacío que acusa del vacío que no acusa.»*

La distinción es correcta y el problema que anticipa es real: **una economía política de la
documentabilidad**. Si el instrumento premia lo documentable, la institución racionalmente empieza
a producir documentación en lugar de gestión — Goodhart aplicado a la verificabilidad, y el
momento exacto en que la transparencia deja de ser un espejo y se vuelve teatro documental.

Pero al ir a escribirlo aparecieron tres obstáculos que lo convierten en algo más grande que una
línea.

### 1 · Sería una contradicción dentro del mismo párrafo

La CAPA 0 declara, dos renglones antes de la lista de estados:

> **«La AUSENCIA de evidencia es un RESULTADO de auditoría, nunca una autorización para inferir
> hechos.»**

Añadir un sexto ítem al paréntesis que afirme lo contrario para una clase de objetos deja el
principio contradiciéndose consigo mismo en el mismo párrafo — y esa contradicción es exactamente
lo que un impugnador buscaría primero.

### 2 · Los cinco actuales ya mezclan tres dimensiones

| Estado | Qué describe en realidad |
|---|---|
| independiente | **origen** de la evidencia |
| institucional | **origen** de la evidencia |
| parcial | **cobertura** de la evidencia |
| sin evidencia | **resultado de ausencia** |
| contradicción | **relación** entre evidencias |

No es una escala: son tres preguntas distintas en una lista. Añadir un sexto que describe **el
objeto** no agrega heterogeneidad a una escala limpia — la agrava en una que ya lo estaba.

### 3 · Nacería sin un solo caso que lo pruebe

En d07 **este estado probablemente no tiene ninguna aplicación**. La LOTAIP es transparencia
*activa*: todo lo que exige es publicar documentos, de modo que por construcción todo lo exigible
es documentable. Las 105 condiciones extraídas de la Guía son todas materializables.

Eso no invalida la propuesta: **la sitúa**. Su lugar natural son los dominios donde QUIRA mide
gestión y no publicación —d01 planificación, d03 mandato, d08 participación— y, sobre todo, la
capa que Javo señala como frontera real: **la intención detrás de la especificación**. Ahí sí
aparecen objetos como criterio, priorización, deliberación y decisión no formalizada.

---

## Decisión

### 1 · Se separan dos dimensiones que hoy viven en una sola lista

    A · NATURALEZA DE VERIFICABILIDAD DEL OBJETO
        ├─ verificable_documentalmente
        └─ no_verificable_documentalmente

    B · ESTADO DE LA EVIDENCIA          (sólo aplica si A = verificable)
        ├─ independiente
        ├─ institucional
        ├─ parcial
        ├─ sin_evidencia
        └─ contradiccion

**La propuesta de Javo deja de ser un sexto estado y pasa a ser una propiedad del objeto que
determina si la segunda dimensión es siquiera aplicable.** Con eso, el Principio Rector sigue
siendo absoluto **dentro del universo de objetos cuya materialización documental es normativamente
exigible**, que es donde siempre debió regir.

Para un objeto de naturaleza no documental no se dice *«buscamos y no encontramos»*. Se dice algo
anterior:

> **La ausencia de materialización documental no constituye hallazgo porque el objeto no tiene, por
> naturaleza normativa, una materialización documental exigible.**

### 2 · El nombre importa, y el evidente era incorrecto

No `no_verificable_por_naturaleza` a secas. La forma que se adopta es:

    naturaleza_verificable: no_documental
    fundamento: "no susceptible de verificación documental bajo este instrumento normativo"

La diferencia no es estilística (colega, 2026-08-20). *«Este objeto no es verificable»* es una
afirmación sobre la verificabilidad ontológica de una decisión humana, y **eso no le corresponde a
QUIRA**. *«No es susceptible de verificación documental bajo este instrumento»* es una afirmación
sobre el alcance del instrumento, que sí le corresponde y es defendible.

### 3 · Sólo el corpus normativo puede declararlo

La barrera sin la cual todo lo anterior se convierte en su contrario:

> **La clasificación `no_documental` proviene del corpus normativo congelado. Ni el motor de
> verificación ni el sujeto observado pueden producirla.**

    CORPUS NORMATIVO
          ↓
    ¿declara materialización esperada para este objeto?
          │
      ┌───┴────────────────┐
      SÍ                   NO
      ↓                     ↓
    objeto verificable    naturaleza_verificable: no_documental
      ↓
    evaluar estado de la evidencia

Si lo declarara **QUIRA**, el instrumento se autoexoneraría de todo lo que no sabe medir. Si lo
declarara **el sujeto observado**, sería la puerta trasera perfecta. Sólo el canon es defendible —
y es el mecanismo que la vara ya usa cuando marca `no_sustentado` porque la Guía no declara
periodicidad. No se inventa una categoría: se extiende una que ya opera bajo la misma regla de oro
(*lo que el corpus no dice, se marca; no se completa*).

### 4 · Tres proposiciones que no se pueden colapsar

    no encontré evidencia
        ≠  no existe evidencia esperable
        ≠  el objeto no admite verificación documental

La primera habla del **proceso de búsqueda**. La segunda, del **sujeto observado**. La tercera, de
la **relación entre el objeto y el instrumento**. Confundirlas produce los dos errores simétricos
que este ADR existe para impedir:

| Error | Forma | Qué destruye |
|---|---|---|
| **1** | no encontré → por tanto no existe | acusa al sujeto por un límite propio |
| **2** | no encontré → por tanto el objeto no era verificable | exonera al sujeto por un límite propio |

Ambos son ilegítimos, y el segundo es el que convertiría esta categoría en el cajón residual
perfecto. De ahí la regla que los cierra a los dos:

> **Ningún verificador puede convertir una propiedad de su propio límite epistemológico en una
> conclusión sobre el sujeto observado — ni acusatoria ni exculpatoria.**

### 5 · Qué protege esto, dicho sin rodeos

El objeto de QUIRA no es maximizar evidencia. Es:

> **maximizar la verificabilidad legítima de aquello que legítimamente debe poder verificarse.**

Sin esa precisión, el sistema empuja a la institución a documentar lo que antes simplemente hacía,
y el indicador termina gobernando al objeto que pretendía observar.

---

### 6 · La secuencia sólo se recorre en un sentido

    naturaleza → evidencia → resultado

**Nunca al revés.** QUIRA no puede observar un resultado de auditoría y deducir desde allí la
naturaleza del objeto: eso permitiría reclasificar un objeto *después* de haber fallado la
búsqueda, que es el error 2 en su forma más peligrosa. La prohibición es estructural —
`Naturaleza` es inmutable y `evaluar_ausencia` la recibe ya construida.

### 7 · La invariante, y su prueba de estrés

> **La ausencia de evidencia sólo puede evaluarse cuando existe una expectativa normativa previa de
> materialización documental.**
> *(colega, 2026-08-20)*

No se declara: se demuestra. `app/agents/procedencia.py` implementa la dimensión como función pura
—sin conexión a d07, a la matriz ni a ningún scoring— y **siete pruebas la someten a los cuatro
casos límite que el colega fijó**:

| | Caso | Naturaleza | Evidencia | Resultado exigido | |
|---|---|---|---|---|---|
| **1** | objeto inequívocamente documental | documental | existe / no existe | con_evidencia / sin_evidencia | ✅ |
| **2** | evidencia indirecta o trabajosa | documental | no hallada | **sin_evidencia**, no `no_documental` | ✅ |
| **3** | sin materialización esperada en el corpus | no_documental | no aplica | `sin_materializacion_documental_exigible` | ✅ |
| **4** | **el sujeto no publicó lo que debía** | documental | ninguna | **`sin_evidencia`, JAMÁS `no_documental`** | ✅ |

**El caso 4 es el que decide si la categoría sirve.** Si un incumplimiento pudiera terminar en
`no_documental`, la dimensión dejaría de proteger al observado y pasaría a exonerarlo. La defensa
no está en la buena voluntad de quien clasifica: está en el **orden**. La naturaleza se deriva de
si el corpus declara materialización esperada, y esa decisión se toma **antes** de mirar si hay
evidencia. Que no haya documento no puede entrar en ella.

Las otras tres pruebas cierran la barrera: ni el motor, ni el sujeto observado, ni el operador
pueden construir un objeto `no_documental` —lanza `NaturalezaUsurpada`—; ni siquiera el corpus
puede hacerlo sin declarar su fundamento; y los dos vocabularios se verifican **disjuntos**, para
que `no_documental` no pueda reaparecer nunca dentro de la lista de estados de evidencia.

## Consecuencias

### Lo que este ADR NO hace

- **No toca la Constitución Ontológica.** La CAPA 0 sigue como está.
- **No añade un sexto estado** a la lista de verificabilidad.
- **No toca SITA, ICPI ni ningún scoring.** Esto es ontología; los motores heredan, no al revés.
- **No se aplica a d07**, donde previsiblemente no tiene casos.

### Condición de promoción a la Constitución

Este ADR se promueve a la CAPA 0 cuando se cumplan **las dos**:

1. **Exista al menos un objeto real** clasificado `no_documental` con su fundamento en el corpus —
   no un ejemplo hipotético.
2. **Se haya reordenado la lista de cinco estados** en sus tres dimensiones (origen · cobertura ·
   resultado), porque incorporar la separación a una lista heterogénea heredaría el defecto.

Mientras tanto vive aquí, propuesto y sin efecto operativo. **Escribirlo hoy en la Constitución
sería declarar en el canon algo que todavía no podemos demostrar** — exactamente lo que esta misma
sesión estableció que no se hace.

### Por qué se escribe ahora si no se aplica todavía

Porque el problema que previene se construye antes de manifestarse. Cuando la economía de la
documentabilidad ya esté instalada, la categoría llega tarde: el incentivo perverso habrá operado
durante años sobre las instituciones observadas. Javo lo formuló como una obligación de diseño —
*dejar diseñada la salida antes de que el problema exista*— y en eso tiene razón.

---

## Trazabilidad

- **Origen:** Javo, 2026-08-20 · «el vacío que acusa ≠ el vacío que no acusa»
- **Separación de dimensiones y nombre correcto:** colega, 2026-08-20
- **Obstáculos detectados (contradicción del principio · heterogeneidad · ausencia de casos en
  d07):** revisión del director, 2026-08-20
- **Relacionado:** ADR-042 §6 y §6-bis · CAPA 0 Principio Rector · Regla de Oro 3

---
*ADR-052 · Dylus Lab © 2026 · el sistema debe poder declarar lo que no puede demostrar, sin
convertir su propia incapacidad en una conclusión sobre nadie.*
