---
id: ADR-053
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: ARQUITECTONICA
status: PROPUESTA — pendiente de sello de Javo (ADR-035 §5)
fecha: 2026-08-26
---

# ADR-053 · Cuál es el camino productivo de un dominio

> **Propone la dirección técnica; decide Javo.** La IA no fija arquitectura (ADR-035 §5).

## 1 · Por qué se abre, y por qué no se abrió antes

Javo (2026-08-26): *«adelante con la integración de los cinco dominios»*, y después el encuadre que
cambió el umbral: *«estamos en construcción y al final es parte de la misma etapa de consolidación
de la versión final»*.

Antes de conectar nada se midió qué significa integrar. **El resultado desplazó el encargo tres
veces**, y esa es la razón de que esto sea un ADR y no un commit:

| se creía | se midió |
|---|---|
| cinco dominios sin defensa, expuestos | cinco paquetes que **nadie importa** — no expuestos, inertes |
| falta conectarlos | el **pipeline productivo es otro** y está documentado |
| `d09` duplica lógica | su motor **delega** en el enricher; era un falso positivo |
| el `MASTER_INDEX` ampara el cambio | **routea, no decide** — lo dice él mismo |

## 2 · La arquitectura que hay, medida

```
    Gold Master
        │
    scripts/enrich_*.py  ──────►  snapshot  ──────►  UI          ← productivo HOY
        ▲
        │ envuelve
    app/agents/dXX/motor.py                                       ← la forma, sin consumidor
    app/agents/dXX/{catalogo,fuentes,persistencia}
```

- **`d09/motor.py` DELEGA**: `_ENRICHER_PATH = Path("scripts/enrich_rdc.py")`, *«envolviendo
  `build_block()` — mismo patrón que d01/d02/d03»*. **No hay dos caminos a la misma verdad.**
- **`PCD-D09`** documenta el camino vigente: *«la corrección fue aguas arriba (canon→snapshot)»*.
- **Ningún PCD** declara la integración como pendiente. Los seis dominios se cerraron sin ella.
- **`persistencia.guardar` es `NotImplementedError` en los SEIS**, incluido `d07`, que **sí** está
  integrado — vía su orquestador. Luego la persistencia no es lo que impide integrar.
- Sólo `d07` tiene orquestador y etapas. Los cinco tienen otro molde. **No son la misma clase de
  artefacto**, y el ADR debe decir si deben serlo.

## 3 · Por qué esto no lo ampara el canon existente

Se siguió el routeo del `MASTER_INDEX` hasta sus tres rectores de arquitectura:

    QUIRA_OS_ARCHITECTURE_v1   «app/agents/dXX» 0 · «enrich_» 0
    ARQUITECTURA_CANONICA      «app/agents/dXX» 0 · «enrich_» 0
    ADR-031 §6                 «app/agents/dXX» 0 · «enrich_» 0

**Ninguno menciona la relación entre paquetes y enrichers.** Sólo el `MASTER_INDEX` la nombra, y su
propósito declarado lo excluye como autoridad: *«NO explica, NO define, NO interpreta — **ROUTEA a
la autoridad**»*. Su propia tabla remite: *«Una decisión de arquitectura → `docs/adr/ADR-NNN`»*, y
su regla final: *«si una verdad no tiene rector claro → es deuda de gobernanza»*.

> **Es exactamente esa deuda.** Implementar sin decidir sería que Python fije la arquitectura —
> Regla de Oro 9.

## 4 · La decisión que se propone

**Que `app/agents/dXX/` sea el camino productivo canónico de un dominio, envolviendo a los
`scripts/enrich_*` en vez de sustituirlos**, con migración progresiva y por equivalencia demostrada.

Los enrichers **no se retiran**: siguen siendo el motor de lectura del Gold Master. Lo que cambia es
quién los invoca y qué contrato cumple esa invocación.

    HOY      UI → snapshot ← script
    OBJETIVO UI → paquete → script → Gold Master
                     └─ identidad · procedencia · verificador · persistencia

**Motivo:** mantener una capa construida y desconectada es deuda, y en una versión final es peor que
el refactor — se publicaría una arquitectura documentada distinta de la que ejecuta.

## 5 · Criterios de entrada — qué debe demostrar un dominio para migrar

Ninguno es nuevo: **los cinco salieron de defectos reales encontrados en d07** durante agosto.

| # | criterio | de dónde salió |
|---|---|---|
| 1 | **identidad huellada** — todo lo que va a la fuente entra en `sujeto.huella()` | el RUC no estaba huellado (deuda 2-ter) |
| 2 | **procedencia en el artefacto**, escrita por el generador y sin reloj | estamparla después re-ejecutaba la cadena (deuda #2) |
| 3 | **verificador con prueba que lo respalde**, comprobado por AST | `materializacion.evaluar` no tenía ninguna (deuda #1) |
| 4 | **no cruzar la frontera de efectos** sin declararlo | una prueba lanzó una corrida real (deuda 4-ter) |
| 5 | **equivalencia demostrada** antes de retirar nada | — |

⚠️ **Migrar sin el criterio 1 introduce el agujero que se acaba de cerrar.** El inventario lo dirá
solo —`cobertura_de_defensa` pasa a `no_protegido` en cuanto aparezca un importador— pero es mejor
no crearlo.

## 6 · Orden propuesto — `d01` como piloto

`d01` es el de menor radio: su métrica ya está resuelta en el Gold Master (IPE nativo `H16b`), su
motor sólo lee, y es el único de los cinco con un importador (aunque sea `_template`).

    d01 (piloto) → d02 → d03 → d09 → d08

`d09` va tarde a propósito: es el más heterogéneo —dos fuentes, una de ellas snapshot persistido— y
conviene llegar con el patrón ya probado. `d08` último: su `fuentes.extraer_aportes_de_acta` está
sin implementar y depende de adquisición que no existe.

### Por qué `d02` es el segundo y no `d03` — corregido antes del sello

La primera versión de este ADR ponía `d03` segundo, por ser el de menor radio. **Medido contra el
`META_CATALOGO_AGENTES`, ese orden no producía nada:**

    d01 ↔ d03   comparten   sólo el «Orquestador d07» — la plantilla, no una fuente
    d01 ↔ d02   comparten   7 fuentes reales: Budget Agent · eSIGEF · SERCOP Agent ·
                            Portal Navigator · Cobertura Material · Trazabilidad
                            Biográfica · Cadena de Adquisición

`d03` **no comparte ninguna fuente con nadie**: su único vínculo con los demás dominios es la
plantilla del orquestador. Migrarlo segundo cumpliría la condición del §6-bis —«dos dominios
migrados»— **de forma puramente formal: los dos primeros no tendrían nada que preguntarse**, y la
primera interacción real se aplazaría hasta el tercero.

`d01 ↔ d02` comparten además **la cédula presupuestaria**, que es exactamente el caso que Javo
planteó al proponer la consulta inter-dominio. El eje real es `d01 ↔ d02 ↔ d07`.

> **Un orden de migración no se elige sólo por facilidad, sino por qué permite observar.** Poner
> primero lo más fácil habría retrasado la única evidencia que puede fijar el contrato del §6-bis.

## 6-bis · Consulta entre dominios — un agente pregunta, no re-deriva

*(Incorporado por decisión de Javo, 2026-08-26. La propuesta es suya.)*

### La mitad que ya existe

Javo planteó que cada dominio fuera **un agente único** con capacidades internas, en vez de un
conjunto de scripts. **`d07` ya lo es**, y el `META_CATALOGO_AGENTES` lo declara:

> *«Orquestador d07 — ✅ `orquestador.py` · **patrón replicable a todo DOM** · **plantilla para
> d01/d02/d03/d08/d09**»*

    ejecutar(anio, meses, guardar) → corrida con run_id, gates y hallazgos

Un punto de entrada que orquesta captura → descarga → análisis → scoring y devuelve un contrato
único. **Eso no se decide aquí: ya está construido y declarado replicable.** El §4 de este ADR sólo
lo convierte en el camino productivo.

### La mitad que NO existe, y es el aporte

    consultas dominio → dominio, medidas en el código:   NINGUNA
    memoria compartida (`MISMA_FUENTE_QUE`, Neo4j):      3 archivos en scripts/

Hoy hay **reuso de fuente**, no **consulta entre agentes**. Y el catálogo muestra por qué importa:

> *Budget Agent — reutilizable: «**YA compartido**» — lo usan: **d01 + d02 + d07 + d09**»*
> *eSIGEF (Fuente) — «**d02 = d01 Presupuesto = d07 CD-06** (misma cédula)»*

**Cuatro dominios miran la misma cédula presupuestaria y cada uno deriva su propia lectura.** Es la
puerta a cuatro verdades sobre el mismo documento — exactamente lo que el sistema entero existe para
impedir. Que `d02` **pregunte** a `d07` en lugar de re-derivar la cierra.

### Qué se pregunta — y esto va antes que cualquier condición técnica

*(Precisión del colega, 2026-08-26, sobre la primera redacción de este §6-bis.)*

    ✅  «d07 tiene evidencia para sostener X respecto de este sujeto»
    ⛔  «d07 dice que X es verdadero, por tanto d02 puede asumirlo»

La primera conserva la genealogía. **La segunda crea el atajo epistemológico que QUIRA existe para
impedir**: convertiría a un dominio en fuente de verdad para otro, y ningún producto QUIRA es fuente
independiente de verdad (`ADR-043 §3`, regla 3).

La primera redacción de este apartado fijaba las dos condiciones técnicas —procedencia y no ascenso
de grado— **pero no decía sobre qué se pregunta**. Un implementador podía cumplir ambas y seguir
preguntando por la verdad. Se corrige antes del sello, que es cuando todavía se puede.

> **QUIRA no es una colección de agentes conversando entre sí: es un sistema de dominios que
> comparten evidencia gobernada.** *(formulación del colega)*

### Se propone: un contrato de consulta, con dos condiciones innegociables

**1 · La respuesta lleva su procedencia. No es un booleano.**

Si `d07` responde *«publicada y auditable»*, `d02` heredaría una afirmación cuya cadena no
construyó, y afirmaría sobre el sujeto con evidencia que no puede acreditar. Es la **deuda #2
llevada al plano inter-dominio**: la procedencia debe viajar con el artefacto hasta donde el
artefacto se consuma — y aquí se consume en otro dominio.

    ⛔ d07.responde(...) → True
    ✅ d07.responde(...) → Sostenida(peso, procedencia, sujeto, faltan)

**2 · Cruzar la frontera NO puede subir el grado.**

Si `d07` sostiene un `hallazgo_de_verificabilidad` y `d02` lo consume como `hecho_verificable`, el
grado subió sin evidencia nueva. `test_ninguna_transformacion_puede_subir_el_grado` ya lo prohíbe
**dentro** de un dominio; el cruce no puede ser la forma de saltárselo. El peso que entra es, como
máximo, el que salió.

⚠️ **Sin estas dos condiciones, la consulta inter-dominio empeoraría el sistema**: propagaría
afirmaciones sin cadena y permitiría que un grado ascendiera al cambiar de dominio. Con ellas,
elimina un riesgo que hoy existe y nadie estaba mirando.

### Por qué va en este ADR y no en uno aparte

Son **la misma decisión en dos planos**: el §4 dice *quién ejecuta*; esto dice *cómo se hablan*.
Separarlas obligaría a abrir un ADR-054 dentro de un mes para algo que pertenece aquí — y el
`MASTER_INDEX` advierte contra multiplicar rectores: *«si una verdad no tiene rector claro → es
deuda de gobernanza, **no señal de construir un doc más**»*.

**Condición de implementación:** el contrato de consulta **no se construye hasta que haya dos
dominios migrados** que puedan hablarse de verdad. Antes de eso sería una interfaz sin interlocutor
— y esta sesión ya midió lo que cuesta construir capas que nadie invoca.

## 7 · Lo que este ADR NO decide

- **Si se completa la Fase 5** (`persistencia.guardar`, pendiente en los seis). Es ortogonal: `d07`
  está integrado sin ella.
- **Si los cinco deben adoptar el molde de `d07`** (orquestador + etapas) o conservar el suyo.
- **Qué pasa con los `scripts/enrich_*` a largo plazo.** Aquí se decide que no se retiran; su
  destino final es otra decisión.
- **La forma exacta del contrato de consulta** (§6-bis): se fija su obligación —procedencia y no
  ascenso de grado— pero no su firma ni su transporte. Se diseña con dos dominios migrados delante,
  no antes.
- **El calendario.** Depende de la ventana de noviembre, y ahí manda la prioridad de Javo:
  *«no hay problema si no alcanzamos; lo imperante es dejar QUIRA impoluta e inexpugnable»*.

---
*ADR-053 · Dylus Lab © 2026 · propuesto por la dirección técnica sobre la medición del 2026-08-26 ·
deriva de GOVERNANCE-001 · **sin sellar**.*
