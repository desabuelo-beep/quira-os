---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy load: carga SOLO el área que vas a tocar. No leas "por si acaso".
> `## AHORA` al cierre · **¿dónde vive una verdad? → `QUIRA_MASTER_INDEX.md`** (Regla #6).

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
🩹 **12 GATES** — correr TODOS · **Curación por DOM (R.8)** · `check_health.py`: NO adivinar.
🧬 **INVARIANTES** (`normativa/invariantes.py`): la extracción declara qué la hace correcta · **estados, NO bool** · corpus **69/69**.
📑 **PAC del holding**: 586 ítems · 4 entidades · `data/pdot/pac_holding.json` · ⛔ **el `.docx` gana al `.pdf`**.
🎨 **ADR-049 visual**: *la gráfica nunca sabe más que el motor* · **la ausencia se dibuja** · VIS-INV-001/002/003.
⛏️ **ADR-050 CANTERA**: **QUIRA hereda capacidades, NO productos** · R0-R3 · **nada se adopta sin prueba contra caso real** · registro `docs/registry/CANTERA.md`.
🔧 **v5.7_TGI** · promover = **recalcular y GUARDAR** (sin caché el conector lee vacío) · **IGP 48,33→27,00**.
⚖️ **ADR-045/046/047**: 1 superficie·3 custodias · techo = **el documento, no el portador** · recálculo = Operaciones.
🏛️ **ADR-048 SIL** (SELLADO): **objeto observado, NO dominio** · ⛔ sin fórmula (no repetir `Ei`).
🔍 **OBS-029**: `V_SERCOP` 0,5 en **42/66** (PAC=puente) · ⛔ captura SERCOP solo **mar-ago 2025** → `1,0`/`0,0` NO derivables · `V_CPCCS` **0/66 citadas en RDC**.
🚒 **OBS-024** Bomberos $1,75M sin meta · **OBS-025/028** **5 factores manuales** (`Ei`·`Ci_Manual`·`Competencia_GAD`·`V_eSIGEF`≡`V_SERCOP`). **Ei NO tocado.**
📋 **Metas 66** · cablea **25** · **OBS-028** meta→partida→devengado · PDOT vige **05-11-2024** → **≥2025** · **5/6 ceros `V_eSIGEF` desmentidos**.
🔭 **ADR-042 CONSOLA** (`env_obs`≠`env_ops`) · **MATRIZ_CANONICA, NO el GM** · **humano acredita** · mando `despacho.py` · ⏭️ **1ª corrida LOTAIP**.
🚦 **8 ESTADOS**: «no existe»≠«no pude obtener»≠«falló». **Solo 2 publicables**.
🔌 **CABLEADO**: **GM→SILOS→DOM→QUIRA** · **S1·S6·S9 sin DOM**.
🧨 **OBS-023** brecha ICM↔ICPI **NO citable** · **`SAT-I`=S6 SIGAD** ⛔NO redefinir (R.1).
🚨 **OBS-022** SAT sin BRN → `check_sat_brn.py`. ⛔`SAT-IX`(d08)≠`SAT-IX-001`.
🔬 **OBS-020**: POA 100% QUÉ · **1,1% DÓNDE**.
⏭️ **JAVO: (1)** ingesta corpus (ordenanza Word + 2 normas SIL) **(2)** Haiku ~$60/18m **(3)** repintado Observatorio.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (§LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 222 GAD).

## REGLAS DE ORO → **las 9 viven en `CLAUDE.md`** (se lee siempre)
Las 2 más olvidadas: **antes de definir, consultar el Inventario de Conceptos** (¿existe? → DERIVA,
no redefinas · cierre `/graphify . --update`) · **no congelar teoría antes que el grafo hable** (ADR-019).

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque** | **SOLO este BOOT.md hasta saber la tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Construcción/UI/dom | `docs/REFERENCE.md` |
| SIL · capacidad informacional | `docs/adr/ADR-048` (SNPD-056-2015 Arts.2·6·8) |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
