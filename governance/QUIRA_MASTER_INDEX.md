# QUIRA MASTER INDEX — Constitución Operacional (el DNS del conocimiento)

**2026-06-21 · el índice de índices · mesa (colega + académico + Javo)**

> **Propósito único:** responder *"¿dónde vive la verdad de X?"* en **<5 segundos.** NO explica, NO define,
> NO interpreta — **ROUTEA a la autoridad.** Es el primer paso de la Regla de Oro #6 (el grafo es autoridad).
>
> **Cómo usar:** ¿vas a definir/tocar algo? Busca su **RECTOR** aquí → lee ESE doc → si lo que ibas a
> escribir ya está → **DERIVA, no redefines** (Regla #6). Esto mata para siempre el *"creo que ya existía"*.

## 1 · Tabla de Autoridad — una verdad, un rector

| ¿Dónde vive la verdad de…? | RECTOR (autoridad única) | Gobierna · NO toca |
|---|---|---|
| **Qué ES un cajón/dominio** (concepto · pregunta estratégica · exclusiones · indicador madre) | `docs/sprint-c/DICCIONARIO_CONCEPTUAL_QUIRA.md` (13 ADN · 11 campos · SELLADO) | el contenido conceptual · NO la forma |
| **Qué CALCULA el sistema** (ICPI·TGI·índices · causalidad matemática) | **Gold Master Model** (Excel SIAP-ICPI · vía `app/connectors/gold_master.py`) | el número · NUNCA recalcular fuera (Regla 1) |
| **Cómo se VE la UI** (card · dashboard · forma) | `docs/adr/ADR-030` | la forma · lee el contenido del Diccionario |
| **Qué SIGNIFICA el dato** (causalidad relacional · circuitos · 4 congruencias · DCO) | Neo4j + `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` + ADR-016/017/019/021 | la doctrina · NO promedia |
| **Cómo está CABLEADO el código** (estructura · dependencias · contratos) | CodeGraph + `graphify-out/graph.json` + `docs/architecture/QUIRA_OS_DEPENDENCY_ATLAS_v1.md` | el plano + invariantes |
| **La ARQUITECTURA** (7 capas · motores · flujo del dato) | `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md` | el mapa del metro |
| **La RUTA** (sprints · fases · productos · CAF) | `governance/HOJA_DE_RUTA_MAESTRA.md` | el plan que no se mueve |
| **El paso de HOY** (estado vivo) | `governance/BOOT.md §AHORA` | el detalle vivo · se reemplaza, no se apila |
| **Lenguaje público vs interno** (firewall) | `ADR-027` + `scripts/dev/firewall_dictionary.json` + `firewall_audit.py` | la frontera de exposición |
| **Qué conservar/purgar al construir un cajón** | `docs/sprint-c/AUDITORIA_CANONICA_CAJONES_v1.md` + `PLANO_DE_CAJONES_v1.md` | la cosecha · deriva del Diccionario |
| **Una decisión de arquitectura** | `docs/adr/ADR-NNN` (cronológico) | el porqué de cada decisión |
| **Principios · invariantes · reglas de oro** | `CLAUDE.md` + `BOOT.md §Reglas de Oro` + Atlas §invariantes | los axiomas inviolables |
| **Compilador · CID · desexcelización** | `ADR-028` (Compilador+CID) · `ADR-029` (Modelo Canónico) | la Vía Sistema (Dylus) |

## 2 · Las 3 columnas del ecosistema (quién hace qué · ADR-024/027/029)

```
QUIRA OPERATIONS  (motor de verdad)  ── ingesta · normaliza · calcula · valida · sella
   │  Gold Master Model + N conectores (SERCOP·CPCCS·CNE·eSIGEF·INEC·PDOT·Excel·API·CSV…)
   │  NUNCA interpreta · NUNCA comunica · solo produce verdad
   ▼
QUIRA PRODUCTS  (capas de salida)  ── Institucional · Ciudadana · Cooperación · Impact · Economic
   │  LEEN Operations · aplican firewall · JAMÁS recalculan ni duplican lógica
   ▼
DYLUS LAB  (laboratorio evolutivo)  ── canon · arquitectura · lenguaje · compilador · CID · firewall · seguridad
      hace EVOLUCIONAR el sistema · NO toca el producto en producción
```
**Encima de las 3 · la CONSTITUCIÓN** (principios · invariantes · dominios · contratos · reglas de oro) — todo
deriva de ahí. *(No es un doc nuevo: vive en `CLAUDE.md` + `BOOT §Reglas` + Atlas §invariantes + Constitución Ontológica — este Index los rutea, no los duplica.)*

## 3 · La regla del Index

- Es el **primer stop** de cualquier sesión que vaya a crear/definir (Regla de Oro #6).
- **Si nace un rector nuevo** (doc con autoridad), **regístralo aquí el mismo día** — o se pierde (la amnesia que ya nos costó).
- Si una verdad **no tiene rector claro** → es **deuda de gobernanza**, no señal de construir un doc más.

---
*QUIRA Master Index · Dylus Lab © 2026 · "Una verdad, un rector. Antes de escribir, pregunta dónde vive. El que redefine, se detiene."*
