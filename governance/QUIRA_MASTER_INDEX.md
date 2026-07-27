---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: ARQUITECTONICA
---

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
| **Qué ES por DENTRO un cajón** (MCD · MCM vs MCD · 5 Motores Analíticos QUIRA · capas tipadas) | `docs/adr/ADR-031` | el modelo, no el dashboard · deriva del ADN · no recalcula el MCM |
| **Qué CALCULA el sistema** (ICPI·TGI·índices · causalidad matemática) | **Gold Master Model** (Excel SIAP-ICPI · vía `app/connectors/gold_master.py`) | el número · NUNCA recalcular fuera (Regla 1) |
| **Cómo se VE la UI** (card · dashboard · forma) | `docs/adr/ADR-030` | la forma · lee el contenido del Diccionario |
| **Qué SIGNIFICA el dato** (causalidad relacional · circuitos · 4 congruencias · DCO) | Neo4j + `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` + ADR-016/017/019/021 | la doctrina · NO promedia |
| **Cómo está CABLEADO el código** (estructura · dependencias · contratos) | CodeGraph + `graphify-out/graph.json` + `docs/architecture/QUIRA_OS_DEPENDENCY_ATLAS_v1.md` | el plano + invariantes |
| **La ARQUITECTURA del sistema · Soberanía** (Nivel 1 del Stack §1.A · 7 capas · motores) | `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md` | el mapa del metro · ontología del SO |
| **La RUTA** (sprints · fases · productos · CAF) | `governance/HOJA_DE_RUTA_MAESTRA.md` | el plan que no se mueve |
| **El paso de HOY** (estado vivo) | `governance/BOOT.md §AHORA` | el detalle vivo · se reemplaza, no se apila |
| **Lenguaje público vs interno** (firewall) | `ADR-027` + `scripts/dev/firewall_dictionary.json` + `firewall_audit.py` | la frontera de exposición |
| **Qué conservar/purgar al construir un cajón** | `docs/sprint-c/AUDITORIA_CANONICA_CAJONES_v1.md` + `PLANO_DE_CAJONES_v1.md` | la cosecha · deriva del Diccionario |
| **Una decisión de arquitectura** | `docs/adr/ADR-NNN` (cronológico) | el porqué de cada decisión |
| **Principios · invariantes · reglas de oro** | `CLAUDE.md` + `BOOT.md §Reglas de Oro` + Atlas §invariantes | los axiomas inviolables |
| **Compilador · CID · desexcelización** | `ADR-028` (Compilador+CID) · `ADR-029` (Modelo Canónico) | la Vía Sistema (Dylus) |
| **Qué ES un CD / evaluación en d07** (unidad de medición, no numeral de ley) | `docs/architecture/CATALOGO_CANONICO_CD_D07.md` v1.0.0 (SSoT) | el catálogo · deriva Excel/Neo4j/JSON, nunca al revés |
| **Cómo se califica LOTAIP** (algoritmo SITA, CTA/ETA/RP/CI) | `docs/architecture/METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP.md` | estándar oficial DPE reconstruido, no inventado |
| **Memoria operacional entre dominios** (grafo compartido, no solo circuitos) | Neo4j AuraDB `8dc8519a` + `scripts/cypher/00N_*.cypher` | evidencia reutilizada (`MISMA_FUENTE_QUE`), nunca re-extraída |
| **Quién razona vs quién solo calcula** (organigrama de agentes IA) | `docs/architecture/META_CATALOGO_AGENTES.md` | IA=juicio/API · Determinístico=lectura fija, gratis |
| **Cómo se implementa el pipeline de un DOM** (código) | `app/agents/d0X/` — importa `app/agents/_template/` (genérico), nunca lo duplica | la forma; NUNCA recalcula el Gold Master |
| **Qué ES la cadena de d01** (eslabones BRN, RO, fuentes, métricas) | `data/d01/catalogo_d01_v1.0.0.yaml` (SSoT) | Neo4j deriva de aquí, nunca al revés |
| **Qué ES d02** (4 capacidades, 3 señales SAT, cadena BRN) | `data/d02/catalogo_d02_v1.0.0.yaml` (SSoT) — motor real: `scripts/enrich_presupuesto.py` | Neo4j deriva de aquí; el enricher YA existía, no se reimplementó |
| **Qué ES d03** (2 métricas: incorporación=hecho, calidad=índice, cadena BRN) | `data/d03/catalogo_d03_v1.0.0.yaml` (SSoT) — motor real: `scripts/enrich_mandato.py` | Neo4j deriva de aquí; evaluación ANUAL (no mensual) |
| **Qué ES d09** (1 índice fidelidad narrativa + 4 hechos documentales incl. aportes ciudadanos, cadena BRN 10 eslabones) | `data/d09/catalogo_d09_v1.0.0.yaml` (SSoT) — motores: `scripts/enrich_rdc.py` (vivo) + `scripts/enrich_rdc_docx.py`/`enrich_aportes.py` (persistidos) | Neo4j deriva de aquí; último dominio BRN-conforme, evaluación ANUAL |
| **Qué ES d08** (jerarquía institucional: marco→Sistema→Asamblea(órgano autónomo)→Consejo→4 mecanismos · 3 dimensiones integridad/vitalidad/efectividad · familia BRN CNO-VIII de 8 CNO) | `data/d08/catalogo_d08_v1.0.0.yaml` (SSoT) | Neo4j deriva de aquí; IGP se LEE (diagnóstico, OBS-015); SAT real = SAT-VI, no 1:1 con mecanismos (OBS-016) |

## 1.A · Stack de Descripción de QUIRA (Marco Fundacional + 3 niveles anidados — aquí se responde "¿6 o 7 capas?")

> **Por qué existe:** tres docs describen "capas" con conteos distintos (6/7/7). **No es conflicto:** son
> **NIVELES** distintos del mismo sistema (anidados, no rivales), **enmarcados por un Marco Fundacional que los condiciona a
> todos** (la Constitución no es un peldaño: **funda**, como la de un país no pertenece a ningún poder). Dentro del stack, el
> nivel de arriba restringe al de abajo; ninguno recalcula la verdad del otro. *(Ratificado por Javo · 2026-06-30 · deriva del canon — Regla #6, no lo redefine.)*

| Rol en el stack | Responde | Rector | Conteo propio |
|---|---|---|---|
| **Marco Fundacional** (Doctrina · ontología del OBJETO) | ¿Qué ES la integridad territorial que QUIRA observa? | `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` (BOOT §32: "capa 0") | 4 macroejes · 12 dominios |
| **Nivel 1 · Ontología del Sistema** (Soberanía) | ¿Qué ES QUIRA como SO · qué verdades gobierna? | `docs/architecture/QUIRA_OS_ARCHITECTURE_v1.md` ⭐**rector del stack** | 7 capas de soberanía |
| **Nivel 2 · Arquitectura** (infra / despliegue) | ¿Cómo funciona técnicamente? | `docs/ARQUITECTURA_CANONICA.md` | 6 capas (tiers) |
| **Nivel 3 · Ingeniería** (construir un dominio) | ¿Cómo construyo un MCD? | `docs/adr/ADR-031 §6` (Matriz del MCD) | 7 capas del MCD |

**Reglas del stack:** (1) el archivo `…OS_ARCHITECTURE…` es el Nivel **1** (ontología/soberanía) pese a su nombre histórico
— el rótulo "Arquitectura" (Nivel 2) vive en `ARQUITECTURA_CANONICA`; (2) no se renombra archivo sellado (Regla #5);
(3) *"¿6 o 7 capas?"* → ninguna y las tres: **son niveles distintos**, cada uno con su conteo legítimo; (4) el **Marco
Fundacional** (Constitución) condiciona a los 3 niveles — no es un peldaño ni compite con ellos.

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
