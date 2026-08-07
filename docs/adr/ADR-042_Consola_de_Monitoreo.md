---
id: ADR-042
authority:
  parent: ADR-041
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: PROPUESTA — pendiente de sello de Javo (ADR-035 §5)
fecha: 2026-08-06
---

# ADR-042 · La Consola de Monitoreo · capa de adquisición del Observatorio

> **Decisión de Javo (2026-08-06)**, sobre revisión del colega y evaluación crítica del
> director. Se cierra la arquitectura conceptual ANTES de seguir construyendo: ningún
> cambio nace en Python (Regla 9). Este documento define el modelo; el código lo
> implementa después.

## 1 · Por qué se abre este ADR

El Observatorio recibió primero un «Panel del Observatorio»: un tablero de lectura con
cifras contadas de los registros. Estaba mal encuadrado, y la corrección de Javo lo dice
sin rodeos — lo que hace falta no es una pantalla para mirar sino **la mesa desde la que
se opera la vigilancia mensual y progresiva de los 222 GAD**.

Al intentar emplazarla aparecieron tres confusiones que este ADR resuelve:

1. **Observatorio ≠ Operaciones.** El director alojó la consola dentro del ambiente de
   mantenimiento técnico razonando que evitaba duplicar. Degradaba el producto principal
   a herramienta de soporte.
2. **La consola no es un dominio, ni un dominio la contiene.** Son capas distintas.
3. **No todo converge en el Gold Master.** El diagrama propuesto hacía desembocar toda la
   captura en el motor de cálculo, lo que contradice ADR-023.

## 2 · La cadena completa

```
FUENTES PÚBLICAS                          QUIRA CIUDADANA
(CNE · Transparencia · CPCCS ·            (evidencia aportada
 SERCOP · Web GAD · otras)                 desde el territorio)
        └───────────────┬───────────────────────┘
                        ↓
                  OBSERVATORIO
        la capacidad institucional de vigilancia
                        ↓
              CONSOLA DE MONITOREO
     coordina corridas de captura, proceso y validación
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
  CORPUS + GRAFO                  insumos numéricos
  evidencia documental                    ↓
        └────── MATRIZ_CANONICA ────→ GOLD MASTER
                  (el contrato)       (calcula métricas)
                        ↓
                 MOTORES DE QUIRA
                        ↓
              DOM d01 · d02 · … · d12
          unidades de conocimiento por dominio
                        ↓
        CENTRO DE INTELIGENCIA TERRITORIAL
              donde se consulta y se relaciona
```

## 3 · Qué es cada cosa — y qué NO es

| Capa | Es | No es |
|---|---|---|
| **Observatorio** | la **función** institucional de vigilancia y adquisición de evidencia | una pantalla, ni un tablero |
| **Consola de Monitoreo** | la **infraestructura operativa** que ejecuta esa función | un producto que se le enseña a un alcalde |
| **Corpus + Grafo** | el **universo de evidencia** documental, con su huella | una base de métricas |
| **Gold Master** | el **núcleo de cálculo** de métricas | un repositorio de documentos |
| **MATRIZ_CANONICA** | el **contrato de integración** entre ambos universos | una tabla auxiliar |
| **DOM** | la **unidad de conocimiento** por dominio | un informe, ni un resultado suelto |
| **Centro** | la **capa de consulta** y articulación | el sitio donde se opera |

### 3-bis · El punto de integración es la MATRIZ, no el Gold Master

ADR-023 lo fija literalmente: **«Excel = motor · Corpus = evidencia verificable del
motor»**, y la MATRIZ_CANONICA es *«el contrato semántico entre el Motor y QUIRA — la
tabla de correspondencia entre el universo Excel y el universo documental»*.

Son **dos universos**. Un documento capturado del portal de transparencia **no entra al
Gold Master**: entra al corpus con su huella. Lo que llega al motor son los insumos
numéricos ya previstos en la matriz.

Decir «todo se integra en el Gold Master» invitaría a meter documentos en un libro de
cálculo de 123 hojas, y a que el motor deje de ser el motor.

## 4 · Las seis preguntas que la consola debe responder

Son el requisito funcional, tomado de la formulación de Javo — *«todo lo que un humano
debería tener para poder realizar este trabajo de manera automatizada pero con rigor
técnico y científico»*:

1. **¿Qué fuentes se monitorean?** — con su capturador, su cadencia y su estado real.
2. **¿Qué corrida se está ejecutando?** — municipio, dominio, fuente, período,
   procedimiento, modelo, versión y estado.
3. **¿Qué evidencia se obtuvo?** — documentos, huellas, marcas de tiempo, ausencias, y
   qué cambió respecto de la captura anterior.
4. **¿Qué validación ocurrió?** — qué propuso la máquina, qué observó la supervisión
   metodológica y qué acreditó la persona.
5. **¿Qué pasó con la corrida?** — con la semántica de estados del §6.
6. **¿Cuánto costó?** — costo de la corrida y acumulado del mes.

La sexta no es administrativa: en una infraestructura que debe escalar de un municipio a
222 con financiamiento propio, **el costo es parte de la trazabilidad operativa**. Una
corrida que no se puede pagar no se puede repetir, y un método que no se puede repetir no
es un método.

## 5 · Quién hace qué — y por qué el orden importa

```
fuente → HAIKU → OPUS → HUMANO → evidencia acreditada
```

| Actor | Función | Límite |
|---|---|---|
| **Haiku** | ejecuta: extrae, clasifica y normaliza según el procedimiento | opera sobre volumen; no decide qué es verdad |
| **Opus** | supervisa el **procedimiento**: muestras, inconsistencias, desviaciones metodológicas | **no es una segunda fuente de verdad** |
| **Humano** | **acredita**: decide qué hallazgo queda validado y publicable | es la única autoridad de validación |

La precisión sobre Opus importa y es del colega: decir «Opus corrige a Haiku» lo
convertiría en una segunda máquina de verdad, que es exactamente lo que prohíbe el
Art. 3 de la Constitución Institucional —*la inteligencia artificial no constituye fuente
de verdad institucional*— y lo que fija ADR-035. Opus revisa **cómo se hizo el trabajo**,
no **qué dice el territorio**.

### 5-bis · La primera corrida de 2025 es de CALIBRACIÓN, no de producción

Se registra como **corrida de calibración metodológica**. Su finalidad no es producir
cifras publicables sino **demostrar que el procedimiento funciona**, detectar sus errores
y medir su comportamiento antes de automatizarlo a escala.

Consecuencia práctica: lo que salga de esa corrida **no se publica como hallazgo** hasta
que el procedimiento quede acreditado. Confundir una calibración con producción sería
publicar cifras cuyo método todavía se estaba probando.

## 6 · Semántica de estados — la distinción que sostiene la tesis

**«No existe evidencia» ≠ «no pude obtener evidencia» ≠ «el capturador falló».**

Es la regla más importante de este ADR. Si un portal cambia su HTML y el conector deja de
funcionar, QUIRA **no puede convertir ese fallo técnico en una afirmación sobre la gestión
pública**. Sería exactamente el tipo de aseveración que este sistema existe para no hacer.

| Estado | Qué afirma | ¿Dice algo del sujeto observado? |
|---|---|---|
| `capturada` | el artefacto se obtuvo de la fuente | no todavía |
| `procesada` | se extrajo y estructuró su contenido | no todavía |
| `pendiente_validacion` | la máquina propuso; falta acreditación humana | **no** — nada se publica aquí |
| `validada` | una persona la acreditó contra la fuente | **sí** |
| `evidencia_ausente` | la fuente respondió y **no hay nada publicado** | **sí**, y es un hallazgo |
| `fuente_no_disponible` | la fuente no respondió | **no** — habla de la fuente |
| `capturador_degradado` | la fuente respondió pero el formato cambió | **no** — habla de nuestro instrumento |
| `error_tecnico` | falló algo nuestro | **no** — habla de nosotros |

Los cuatro últimos estados **no son juicios sobre la gestión**. Solo `evidencia_ausente`
lo es, y aun así se enuncia como lo que es —ausencia de publicación registrada—, nunca
como incumplimiento: calificar jurídicamente no le corresponde a QUIRA.

Esta tabla es la aplicación operativa del Principio Rector: *la ausencia de evidencia es
un RESULTADO de auditoría, nunca autorización para inferir hechos*.

## 7 · La relación fuente↔dominio es de muchos a muchos

**No** existe correspondencia rígida `SERCOP → d02`. Una fuente aporta evidencia a varios
dominios; un dominio necesita evidencia de varias fuentes. El mandato electoral, por
ejemplo, solo puede contrastarse cruzando el plan de trabajo del CNE con la planificación
y con lo efectivamente contratado.

Es lo que distingue una infraestructura de conocimiento de un conjunto de raspadores con
destino fijo. La consola declara **de dónde puede venir** la evidencia; cada dominio
decide cuál admite.

## 8 · Reglas que este ADR fija

1. **Ningún DOM depende de la consola para ser inteligible.** Un dominio se entiende por
   sí mismo; la consola explica de dónde salieron sus datos, no qué significan.
2. **Ninguna consola se convierte en un DOM.** Opera, no interpreta.
3. **Ningún DOM es fuente de verdad de otro DOM.** El contrato de integración es la
   MATRIZ_CANONICA.
4. **La cobertura pertenece al dominio; la corrida, a la consola.** Son dos vistas del
   mismo dato: el dominio pregunta *«¿qué cobertura tiene mi evidencia?»* y la consola
   *«¿qué corrida la produjo y qué ocurrió durante ella?»*.
5. **La consola no publica.** Produce evidencia acreditable; publicar es decisión humana.

## 9 · Consecuencias

- El Observatorio es un **ambiente propio** (`quira_pages/env_obs.py`), separado del de
  mantenimiento técnico.
- La Consola de Monitoreo es su pantalla de trabajo
  (`quira_pages/p_monitoreo_fuentes.py`).
- La semántica de estados del §6 debe existir **en código** antes de la primera corrida:
  sin ella, un fallo de capturador podría llegar a un informe como si fuera un hallazgo.
- El costo por corrida debe registrarse desde la primera, no añadirse después.
- QUIRA Ciudadana **no es un segundo observatorio**: es la otra vía de adquisición hacia
  el mismo sistema de conocimiento (ADR-041 §3).

## 10 · Lo que este ADR NO decide

- **Qué dominios se curan primero.** Sigue siendo el Protocolo de Curación.
- **El estatuto del aporte ciudadano** como evidencia — queda abierto en ADR-041 §6.
- **La ingesta del Instructivo de Monitoreo**, que es precondición de la primera corrida:
  `app/agents/d07/scoring.py` implementa sus reglas y el documento no está en el corpus.
  Sin él, cada puntaje citaría una norma sin verificar (Regla 3).

---
*ADR-042 · Dylus Lab © 2026 · propuesto por el director sobre revisión del colega,
consolidado por Javo (2026-08-06)*
