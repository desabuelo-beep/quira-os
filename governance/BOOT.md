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
> ⛔ **NO es "auditoría" ni "observatorio"** — función menor y producto (Javo 2026-08-05).
> Escala: SIAP-ICPI **mide** · QUADRUM **detecta** · **QUIRA EXPLICA la causalidad**.

## 🎯 LA TESIS — no olvidar
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente.**
El **Observatorio de Integridad Territorial** es UN PRODUCTO, no la identidad: lleva QUIRA a los 222 GAD. Montecristi = el MOLDE.
**ADR-041 §4 (sellado)**: F1 = **Observatorio · Ciudadana** (ENTRADAS de evidencia) · F2 = Institucional ·
Cooperación · Impact · F3 = Economic. **Operaciones NO es producto.** Licencia de gestión al GAD SÍ
(§4-ter): no es cliente de la OBSERVACIÓN. ⛔ NO se presenta hasta operar varios GAD.

## 📜 ONTOLÓGICA → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `HOJA_DE_RUTA_MAESTRA.md`
Define el OBJETO, **no a QUIRA** (CAPA 0 · 4 macroejes · **13 dom.** = 12 + d13 Mutabilidad): CONGRUENCIA
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO → BRECHAS. 3ª pieza: `GOVERNANCE_CHARTER.md`.

## AHORA (estado vivo · historial → `governance/historico/`)
🧭 **ADR-031** MCIP=5 motores · **035/037** IA propone/humano valida · **038** BRN **traza, no alimenta**.
✅ **PCD: d01·d02·d03·d06·d09** · d08 ENTRABLE · **d07 en curación**.
🩹 **12 GATES** · Curación por DOM (R.8) · **estados, NO bool** · 529 pruebas.
📑 ⛔ `.docx` gana al `.pdf`.
⚖️ **d07 BRN VIGENTE** (Javo 26-08): `CNO-VII-001..004` **46/46 SHA** + `RO-VII-001..005`. ⛔ el DOM **consume RO, NO lee la ley**.
📡 **SITA 2025 0,4448** (era 0,4646) · **0 actas** · num.6 sin ingresos.
🧹 **CORPUS**: 8 chunks de preámbulo fingían artículo (LOTAIP 19 = Pacto).
🧪 **§6-bis**: falta evidencia→**degrada** · identidad contradictoria→**BLOQUEA** · el SHA prueba el archivo, NO la atribución.
🚦 **8 ESTADOS**: «no existe»≠«no pude obtener»≠«falló».
🎨 **ADR-049** *la gráfica no sabe más que el motor* · ⛏️ **050 CANTERA**: hereda capacidades, NO productos.
🔧 **v5.7_TGI** · promover = **recalcular y GUARDAR**.
📋 **Metas 66/cablea 25** · PDOT **05-11-2024**→**≥2025**.
🔭 **ADR-042** (`env_obs`≠`env_ops`) · **MATRIZ_CANONICA, NO el GM**.
🤖 **ADR-051 §12**: 5 dim. (capacidad·**sujeto**·ejecución·evidencia·validación) · sin sujeto NO hay afirmación.
🔌 **ÚNICA puerta**: `reglas.py`→norma (gate **REGLAS**) · `config.DATOS_DIR`→datos: **0 rutas fijas**.
🔐 **PANEL ACCESOS**: bitácora 2 meses sin leerse · alerta por concentración.
📐 **MATRIZ (Javo)**: portal = **materialización de obligaciones** · ⛔ ausencia≠incumplimiento · 7 cond. ✅.
🪞 **ADR-052** (⛔ NO toca CAPA 0): **naturaleza ≠ estado de la evidencia** · `no_documental` sólo lo declara el CORPUS · ⛔ no publicar ≠ no exigible.
🧬 **§6-sexies**: **segmento ≠ condición ≠ exigencia** · *etiqueta incorrecta = número falso*.
➡️ **SIGUIENTE**: Capa 2 a los 24 numerales (⏸ valid. jurídica de 105) · luego los 636.
🧾 **SCORING vs Instr.**: SITA·CTA·ETA·RP ✅ · **CI mal** (Anexo 1: 1×1). ⛔ NO tocar SITA.
⛔ **EL NOMBRE NO ES EVIDENCIA** — 3× GAD · **1× nosotros**: 85 ensayos.
🧷 **PROCEDENCIA nace en el GENERADOR**, sin reloj · ⛔ estamparla luego re-ejecuta la cadena.
🚧 **TEST ≠ OPERACIÓN**: `conftest` corta subprocess/red · efecto real se declara (2).
🧱 **ADR-053**: el DOM es **agente gobernado** · **d01+d02 migrados y atacados** · d01≡d02 misma evidencia GM.
🗳️ **SECCIONALES 29-NOV-2026** (alcaldes·prefectos·juntas): ventana para que la gente verifique su alcaldía · ⛔ **la fecha NO manda**: primero impoluto.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (§LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 222 GAD).

## REGLAS DE ORO → **las 10 viven en `CLAUDE.md`** (se lee siempre)
⚠️ **NO está entre las 10**: **antes de definir** → `marco_teorico/INVENTARIO_CONCEPTOS_FUNDACIONALES.md`
(**deriva, no redefinas** · cierre `/graphify . --update`). La #10 se restauró el 26-08.

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque** | **SOLO este BOOT.md hasta saber la tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Construcción/UI/dom | `docs/REFERENCE.md` |
| SIL · capacidad informacional | `docs/adr/ADR-048` (SNPD-056-2015 Arts.2·6·8) |
| Autoridad de una proposición de BOOT | `docs/registry/AUTORIDAD_PROPOSICIONES_BOOT.md` (REGISTRO · decisiones abiertas) |
| De dónde viene un nombre antiguo | `marco_teorico/GENEALOGIA_QUIRA.md` (SIAP·QUADRUM·TERRA) |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
