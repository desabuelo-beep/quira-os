---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy loading: carga el detalle SOLO del área que vas a tocar. No leas todo "por si acaso".
> Mantener bajo 500 tokens · `## AHORA` al cierre · **¿dónde vive una verdad? → `QUIRA_MASTER_INDEX.md`** (Regla #6).

## QUÉ ES → `identity/CONSTITUCION_INSTITUCIONAL.md` (CONSTITUCION-001 · raíz `parent:null`)
> **QUIRA = plataforma de inteligencia pública · infraestructura de conocimiento verificable**
> (Plataforma · Método · Patrimonio Cognitivo) para gobiernos, ciudadanía, academia, cooperación.
> ⛔ **NO es "auditoría" ni "observatorio"** — función menor y producto (Javo 2026-08-05).
> Escala: SIAP-ICPI **mide** · QUADRUM **detecta** · **QUIRA EXPLICA la causalidad**.

**3 niveles** (ADR-023 — inmutable): **1 Motor** = Gold Master **v5.7_TGI** (calcula ICPI/TGI/SAT/MMP · leer vía
`app/connectors/gold_master.py` · NUNCA recalcular fuera del Excel) · **2 SO** = QUIRA (ingesta +
trazabilidad MNT_UUID + evidencia) · **3 UI** = Dashboards + GeoTwin (solo visualizan).
**MATRIZ_CANONICA** del Excel = ADN compartido: sin ella, dos mundos.

## 🎯 LA TESIS — no olvidar
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente.**
El **Observatorio de Integridad Territorial** es UN PRODUCTO, no la identidad: lleva QUIRA a los 222 GAD. Montecristi = el MOLDE.
**ADR-041 (sellado)**: F1 = **Observatorio · Ciudadana** (ENTRADAS de evidencia) · F2 = Institucional ·
Cooperación · Impact · F3 = Economic. **Operaciones NO es producto.** Licencia de gestión al GAD SÍ
(§4-ter): no es cliente de la OBSERVACIÓN. Ventana: **elecciones NOV-2026**.

## 📜 ONTOLÓGICA → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `HOJA_DE_RUTA_MAESTRA.md`
Define el OBJETO observado, **no a QUIRA** (CAPA 0 + 4 macroejes + 12 dominios): CONGRUENCIA
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO → BRECHAS. 3ª pieza: `GOVERNANCE_CHARTER.md`.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
🧭 **ADR-031** MCIP=**5 motores** (runtime: Matemático·Grafos) · **ADR-035/037** IA propone/humano valida · **ADR-038** BRN **traza, no alimenta**.
✅ **PCD: d01·d02·d03·d06·d09** · **d08 ENTRABLE** (Asamblea AUTÓNOMA · OBS-012..017).
🩺 **Curación por DOM (R.8) · `check_health.py`: NO adivinar.**
🏛️ **GOBERNANZA v1.0:** `identity/`→`governance/`→`marco_teorico/`→Canon→`registry/`.
🖥️ **d08 WEB** 191→162→**15%** · 66 inverificable · 96 sin-tema.
🩹 **9 GATES** (`scripts/ci/`) — correr TODOS antes de commitear.
🔧 **v5.7_TGI** (11-08) · promover = **recalcular y GUARDAR** (sin caché el conector lee vacío) · **IGP 48,33→27,00**.
⚖️ **ADR-045/046/047**: 1 superficie·3 custodias · techo = **el documento, no el portador** · **recálculo = Operaciones**.
🚒 **OBS-024** Bomberos: $1,75M sin meta · **OBS-025** `Ei`·`Ci_Manual`·`Competencia_GAD` = **3 manuales**. **Ei NO tocado.**
📋 **Metas PDOT: 66** (58 verif.) · **0 de Bomberos** · motor cablea **25**.
🔭 **ADR-042 CONSOLA** (`env_obs`≠`env_ops`) · integra **MATRIZ_CANONICA, NO el GM** · **humano acredita** · 1ª corrida=**calibración**. Ya tiene **mando** (`app/observatorio/despacho.py`).
🚦 **8 ESTADOS** (`app/observatorio/`): «no existe» ≠ «no pude obtener» ≠ «falló el capturador». **Solo 2 publicables**. Corpus **14.285** (+COESCOP).
🎨 **Identidad v1.1**: marca = **asset, NO se redibuja** · 1 acento → `login_view.py`.
🔌 **CABLEADO**: **GM→SILOS→DOM→QUIRA** · **S1·S6·S9 sin DOM** (`MATRIZ_CABLEADO_CANONICO.md`).
🧨 **OBS-023** brecha ICM↔ICPI **NO citable** · **`SAT-I`=S6 SIGAD**. ⛔ NO redefinir (R.1).
🚨 **OBS-022** SAT sin BRN → gate `check_sat_brn.py`. ⛔ `SAT-IX`(d08) ≠ `SAT-IX-001`.
🏛️ **R-C..R-H → `PROTOCOLO_CURACION_DOMINIO.md` §3.**
🔬 **d01 §05 → OBS-020**: POA 100% QUÉ · **1,1% DÓNDE** · 1 de 1027 ambas. `inverificable` ≠ `no atendido`.
⚖️ **3 CAPAS**: jurídica (**Guía LOTAIP=LEY**) · operativa (d07) · analítica (**no tramita**). 🧪 H-ARQ-01 HIPÓTESIS ⛔R-E.
🧠 **DESCUBRIMIENTO NORMATIVO**: 4º de los **5 MCIP**, no motor nuevo. **Laboratorio, NO runtime**. ⛔R-E.
⏭️ **JAVO: (1)** 2ª validación v4 (¿retirar `complementaria`?) **(2)** Haiku ~$60/18 meses **(3)** repintado Observatorio.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (§LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 222 GAD).

## REGLAS DE ORO → **las 9 viven en `CLAUDE.md`** (se lee siempre · no se duplican aquí)
Las 2 que más se olvidan: **antes de definir, consultar el Inventario de Conceptos** (¿existe? → DERIVA,
no redefinas · cierre `/graphify . --update`) · **no congelar teoría antes que el grafo hable** (ADR-019).

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque** | **SOLO este BOOT.md hasta saber la tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Construcción/UI/dom | `docs/REFERENCE.md` |
| Retomar d07 | `CATALOGO_CANONICO_CD_D07.md` + `app/agents/d07/` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
