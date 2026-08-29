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

    d01 (piloto) → d03 → d02 → d09 → d08

`d09` va tarde a propósito: es el más heterogéneo —dos fuentes, una de ellas snapshot persistido— y
conviene llegar con el patrón ya probado. `d08` último: su `fuentes.extraer_aportes_de_acta` está
sin implementar y depende de adquisición que no existe.

## 7 · Lo que este ADR NO decide

- **Si se completa la Fase 5** (`persistencia.guardar`, pendiente en los seis). Es ortogonal: `d07`
  está integrado sin ella.
- **Si los cinco deben adoptar el molde de `d07`** (orquestador + etapas) o conservar el suyo.
- **Qué pasa con los `scripts/enrich_*` a largo plazo.** Aquí se decide que no se retiran; su
  destino final es otra decisión.
- **El calendario.** Depende de la ventana de noviembre, y ahí manda la prioridad de Javo:
  *«no hay problema si no alcanzamos; lo imperante es dejar QUIRA impoluta e inexpugnable»*.

---
*ADR-053 · Dylus Lab © 2026 · propuesto por la dirección técnica sobre la medición del 2026-08-26 ·
deriva de GOVERNANCE-001 · **sin sellar**.*
