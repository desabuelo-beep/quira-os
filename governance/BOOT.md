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
🧭 **ADR-031** MCIP=5 motores · **035/037** IA propone/humano valida · **038** BRN **traza, no alimenta**.
✅ **PCD: d01·d02·d03·d06·d09** · d08 ENTRABLE · **d07 en curación**.
🩹 **12 GATES** · Curación por DOM (R.8) · **estados, NO bool** · corpus 69/69.
📑 **PAC** 586 · **SERCOP 265+75** · ⛔ `.docx` gana al `.pdf`.
⚖️ **d07 EN LA BRN**: `CNO-VII-001..004` **46/46 SHA** + `RO-VII-001..005` **propuesta**. ⛔ el DOM **consume RO, NO lee la ley** — el error de raíz.
📡 **MEDICIÓN**: **SITA 2025 0,4448** (era 0,4646: se contaba bueno lo no mirado) · **0 actas** · num.6 **sin ingresos 8/8** · 11 enlaces caídos.
🧹 **CORPUS**: 8 chunks de preámbulo fingían artículo (LOTAIP 19 = Pacto).
🧪 **ADR-042 §6-bis**: falta evidencia→**degrada** · identidad contradictoria→**BLOQUEA** · el SHA prueba el archivo, NO la atribución.
🎨 **ADR-049**: *la gráfica nunca sabe más que el motor*.
⛏️ **ADR-050 CANTERA**: hereda capacidades, NO productos · nada sin prueba.
🔧 **v5.7_TGI** · promover = **recalcular y GUARDAR** · **IGP 48,33→27,00**.
⚖️ **ADR-045/046/047**: 1 superficie·3 custodias · techo = **el documento**.
🖥️ **OBS-032**: `QUIRA_DATOS`/`QUIRA_VAULT` = frontera 1 vez · **0 rutas personales** · 50 por migrar.
🏛️ **ADR-048 SIL**: **objeto observado, NO dominio** · ⛔ sin fórmula.
🚒 **OBS-024/025/028**: Bomberos $1,75M sin meta · 5 factores manuales · ⛔**Ei**.
📋 **Metas 66/cablea 25** · PDOT **05-11-2024** → **≥2025**.
🔭 **ADR-042 CONSOLA** (`env_obs`≠`env_ops`) · **MATRIZ_CANONICA, NO el GM**.
🚦 **8 ESTADOS**: «no existe»≠«no pude obtener»≠«falló». Solo 2 publicables.
🤖 **ADR-051 §12**: 5 dimensiones (capacidad·**sujeto**·ejecución·evidencia·validación) · sin sujeto **NO se construye** la afirmación · perímetro propio SELLADO.
🔌 **`reglas.py` = ÚNICA puerta a la norma**: cadencia·plazo·formatos del canon · gate **REGLAS** · **472 pruebas**.
🔐 **PANEL ACCESOS** (→Ops): bitácora 2 meses sin leerse · alerta por fallos concentrados.
📐 **MATRIZ (Javo)**: el portal NO es colección de archivos sino **materialización de obligaciones** · unidad *obligación↔evidencia* · ⛔ **ausencia ≠ incumplimiento** · 26: 7·17·2.
⛔ **EL NOMBRE DEL ENLACE NO ES EVIDENCIA** — 3×: «acta»→certificado · «asistencia»→fotos.

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
