---
id: ADR-047
authority:
  parent: ADR-023
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTA — pendiente de sello de Javo (ADR-035 §5)
fecha: 2026-08-11
---

# ADR-047 · El ciclo cerrado de los motores canónicos

> **Qué decide.** Cómo la evidencia capturada llega hasta los motores deterministas, dónde se
> recalcula, quién autoriza esa escritura y cómo se prueba que el resultado es reproducible.
> **Qué NO decide.** Nada sobre las fórmulas. `H12!B33` sigue siendo inmutable.

## 1 · El hueco, y es reciente

La Consola de Operación (2026-08-10) despacha capturas reales. **Ninguna llega al motor.**
`app/connectors/gold_master.py` abre el Excel con `read_only=True`: solo lee. No existe ruta de
escritura hacia el Gold Master.

Consecuencia: se captura, se registra la corrida, se guarda la evidencia — y el ICPI no se mueve.
**Se construyó el mando y quedó el cable suelto.**

Javo lo formuló desde el otro extremo y llegó al mismo punto (2026-08-11):

> «La revisión del portal es de por sí una de las variables de la fórmula. Ese procedimiento es
> parte fundamental de la fórmula canónica y debe pasar por la fórmula primero para su cálculo,
> y luego se deriva donde se necesite.»

Tiene razón, y de ahí se sigue algo que estaba quedando oculto: **la innovación no es tener
conectores. Es que la observación documental del Estado se incorpora como variable metodológica
formal del cálculo canónico.** Capturar sin inyectar no es capturar: es archivar.

## 2 · Tres cosas que no deben confundirse

| | Qué es | Dónde vive |
|---|---|---|
| **Doctrina metodológica** | qué significa cada variable, qué evidencia la alimenta, qué la valida | canon · versionada |
| **Ejecución** | capturar, normalizar, validar, inyectar, ordenar recálculo, publicar, trazar | **código** |
| **Autoridad matemática** | la fórmula que produce la cifra | **motores canónicos, intocables** |

> **La lógica metodológica se formaliza en código; la autoridad del cálculo permanece en los
> motores canónicos.** El código orquesta y ejecuta. Los motores calculan. El humano valida donde
> el canon lo reserva. Ningún componente produce una segunda verdad.

Esto responde con precisión a *«toda la lógica matemática debe ser código»*: **la lógica de
proceso, sí; las fórmulas, no.** Portarlas sería construir el motor paralelo que CLAUDE.md
prohíbe expresamente, y destruiría justo lo que se quiere proteger — un único cálculo.

## 3 · Son DOS motores deterministas, no uno

Precisión de Javo (2026-08-11): *«no solo por el Gold Master, sino por todos los otros motores,
por la BRN y su corpus normativo»*. Es correcto, y el sistema ya los tiene:

| Motor | Qué determina | Soporte |
|---|---|---|
| **Gold Master** | cuánto vale — índices ICPI · TGI · IED · IGP · IOC · IET · PSG | Excel canónico `_TGI` |
| **BRN** | si la norma se cumple — CNO + RO compiladas, con SHA por eslabón | `docs/brn/*.yaml` + compilador + runtime |

**Y se encadenan.** `MATRIZ_CABLEADO_CANONICO` ya declara la secuencia por silo: cada fuente
*verifica* algo y *produce* una variable —`V_LOTAIP`, `V_SERCOP`, `V_eSIGEF`, `T_i`, `SAT-0`—.
Esa es la cadena real:

```
evidencia → BRN (¿cumple la norma?) → variable canónica V_* → Gold Master (¿cuánto vale?) → índice
```

La BRN no es documentación: es el motor que convierte un documento en un hecho normativo
evaluable. Que su resultado alimente al Gold Master es lo que hace que un índice tenga fundamento
jurídico y no solo aritmético.

## 4 · La frontera de escritura canónica

**Ningún proceso escribe una celda arbitraria.** Una cosa es que `d07` sea variable de entrada y
otra muy distinta permitir escritura libre sobre el motor.

Una escritura al Gold Master solo es legítima si cumple **las cuatro**:

1. **Variable declarada.** Está en el registro de variables canónicas escribibles, con su celda o
   rango de destino. Lo que no está declarado, no se escribe.
2. **Evidencia acreditada.** Con procedencia, huella SHA-256 y estado `validada` (ADR-042 §6).
   Una captura en `pendiente_validacion` no entra al motor.
3. **Validación humana donde el canon la reserva.** La automatización cubre la ejecución;
   **no puede automatizar una autoridad que el canon asigna a una persona.**
4. **Trazabilidad completa.** Queda registrado qué se escribió, en qué celda, desde qué evidencia,
   por orden de quién y con qué versión de procedimiento.

Todo lo demás sigue siendo lectura.

## 5 · Dónde ocurre el recálculo — y por qué no es un detalle

**`openpyxl` no recalcula fórmulas.** Es la librería con la que hoy se lee el Gold Master, y lo
hace con `data_only=True`: devuelve el valor que Excel cacheó la última vez que abrió el archivo.

Si se inyectara un input con esa librería, **el dato entraría y las fórmulas dependientes no se
recalcularían**. El archivo quedaría con el input nuevo y el ICPI viejo — y al leerlo después,
devolvería esa cifra desactualizada **sin señal alguna de que lo está**. Sería un error silencioso
sobre la cifra madre del sistema: exactamente la clase de defecto que este proyecto viene cazando,
en el peor sitio posible.

**Por tanto: el recálculo exige un entorno con motor de cálculo real** (Excel, o equivalente
verificado). En el despliegue público no lo hay.

> **El recálculo es un paso de Operaciones, no de la aplicación.**

| Paso | Dónde |
|---|---|
| Captura y registro | aplicación · Consola |
| Evaluación normativa (BRN) | aplicación |
| Validación humana | aplicación |
| **Inyección + recálculo** | **entorno autorizado con motor real** — ordenado desde la Consola |
| Publicación del snapshot | Operaciones |
| Lectura del resultado | aplicación |

**Queda prohibido leer como canónico un Gold Master con inputs nuevos y fórmulas sin recalcular.**
El conector debe detectarlo y negarse, no devolver la cifra vieja.

## 6 · Determinismo verificable, no declarado

Que el cálculo sea determinista no basta: **tiene que poder demostrarse**. Toda inyección registra:

- huella del motor **antes** y **después**;
- qué variables se escribieron y con qué valores;
- la evidencia de origen de cada una;
- el resultado de los índices afectados.

Con eso, repetir la misma inyección sobre el mismo motor debe producir la misma huella final. **Si
no la produce, el determinismo se rompió y el sistema debe decirlo** en vez de publicar.

## 7 · Un recálculo no sobrescribe lo publicado

Si un recálculo modifica una cifra ya publicada, **el snapshot anterior no se reemplaza**: se
versiona y la corrección se declara con su motivo. Enlaza con la exigencia de Javo (2026-08-10) de
no perder la serie mensual, y añade la razón de fondo: **un sistema que corrige en silencio no es
auditable**, y la auditabilidad es lo único que QUIRA vende.

## 8 · La Consola ordena; no calcula

El botón **no ejecuta un guion**: emite una **orden** que el despacho traduce al procedimiento
vigente. Así el conector de una fuente puede cambiar sin tocar la Consola, y añadir CNE, SERCOP o
Web GAD no altera la interfaz. `app/observatorio/despacho.py` ya opera así; este ADR lo fija como
regla y la extiende al tramo de inyección y recálculo.

## 9 · Consecuencias

| # | Qué | Estado |
|---|---|---|
| 1 | Registro de variables canónicas escribibles, con celda y condición | ⛔ pendiente |
| 2 | Ruta de escritura al Gold Master, en entorno con motor real | ⛔ pendiente |
| 3 | El conector se niega a leer un motor con fórmulas sin recalcular | ⛔ pendiente |
| 4 | Huella antes/después y prueba de reproducibilidad | ⛔ pendiente |
| 5 | Snapshots versionados por corte; ninguno se sobrescribe | ⛔ pendiente |
| 6 | Cadena BRN → variable → Gold Master, explícita por dominio | ⛔ pendiente |
| 7 | La Consola gana los mandos de inyección, recálculo y publicación | ⛔ pendiente |

## 10 · Lo que este ADR NO decide

- **Ninguna fórmula.** `H12!B33` permanece inmutable (Regla 1 · ADR-023).
- **Qué variables concretas son escribibles.** Eso es el punto 1 de consecuencias y exige revisar
  el motor hoja por hoja: declararlo aquí de memoria sería justo el error que este ADR previene.
- **Cuándo se automatiza cada tramo.** Las primeras corridas son manuales y con validación humana,
  por decisión expresa de Javo (2026-08-10). La automatización llega después, tramo por tramo, y
  solo donde el canon no reserve la decisión a una persona.

---
*ADR-047 · Dylus Lab © 2026 · deriva de ADR-023 · no altera ninguna fórmula.*
