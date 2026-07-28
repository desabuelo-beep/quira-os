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

## QUÉ ES
> **"El Gold Master ya sabe medir la gestión pública; QUIRA está aprendiendo a demostrar
> documentalmente por qué cada métrica del Gold Master es verdadera o falsa."**
> Objetivo: **sistema de auditoría explicable del modelo ICPI.** No agrega datos: agrega significado.

**3 niveles** (ADR-023 — inmutable): **1 Motor** = Gold Master v5.5 (calcula ICPI/TGI/SAT/MMP · leer vía
`app/connectors/gold_master.py` · NUNCA recalcular fuera del Excel) · **2 SO** = QUIRA (ingesta +
trazabilidad MNT_UUID + evidencia) · **3 UI** = Dashboards + GeoTwin (solo visualizan).
**MATRIZ_CANONICA** del Excel = ADN compartido: sin ella, dos mundos.

## 🎯 LA TESIS (lo que NUNCA se debe olvidar)
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente.**
QUIRA = **OBSERVATORIO NACIONAL DE INTEGRIDAD TERRITORIAL** (221 GADs). Montecristi = el MOLDE.
Fase 1 = 3 motores/productos: **Operaciones · Ciudadana · Institucional**. Fase 2: Cooperación ·
Impact · Economic. Diferenciador: Plan CNE + NLP discurso RDC. Ventana: **elecciones NOV-2026**.
Negocio = complementario, no licencias. **Detalle: `HOJA_DE_RUTA_MAESTRA.md §0` · ADR-024.**

## 📜 CONSTITUCIÓN → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `governance/HOJA_DE_RUTA_MAESTRA.md`
Constitución = QUÉ ES QUIRA (CAPA 0 Doctrina + 4 macroejes + 12 dominios): mide la CONGRUENCIA de
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO y halla las BRECHAS. BOOT §AHORA = el paso actual.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
🧭 **ADR-031 RATIF:** cajón=MCD · GoldMaster=MCM · MCIP 5 motores (Index §1.A).
✅ **4 DOM cerrados con PCD: d01·d02·d03·d09.**
📚 **ADR-038 BRN v2:** nodo = REGLA, no artículo. **Corpus→CNO→RO→SAT** · **v1.0 CONGELADO** · **BRN v2.1** d01-03+08-09 CONFORMES·diff=0.
🩺 **Canon curado por DOM (R.8), ICPI intacto. Gate = `check_health.py`: NO adivinar tamaños.**
📚 **ADR-035/037:** Ley→BRN→GoldMaster(único motor)→QUIRA · IA propone, humano valida.
🏛️ **d02·d03·d09·d08 migrados** (OBS-012/013/014). **d08**: **Asamblea ciudadana AUTÓNOMA (no GAD)** · CNO-VIII(8) · **OBS-015/016/017** · frontera d08≠d09.
🏛️ **GOBERNANZA v1.0:** `identity/`Constitución → `governance/`Carta → `marco_teorico/`(Postulados+Inventario+**Mapa Gobernanza**) → Canon → `registry/`. ⚠️ Derivación 100% **solo en lo catalogado**: `docs/architecture/` = 47 .md sin autoridad, FUERA del registry.
🔬 **d08 · MRSPP v3** (5 niveles; embedding PROPONE, modelo DECIDE): 68·27·**0**·25 · 103 nulas. **OBS-019** REGLA 0: quién ejecuta ≠ qué se hace. T1 ya estaba en canon.
🏛️ **REGLAS Protocolo §3** — **R-C** el dueño del instrumento lo califica (OBS-020 → **d01**) · **R-D** ¿limitación del ALGORITMO o del INSTRUMENTO? si del instrumento **se mide, no se parcha** · **R-E (LEY)** Montecristi = ÚNICO universo activo hasta cerrarlo · **R-F** pedir depende del CONOCIMIENTO del universo: mal publicado→pedir · **conocido inexistente→NO** (lo construiría → evid. de REACCIÓN) · **no conocido→SÍ vía Observatorio**, la respuesta ES evidencia.
🔬 POA localiza el **1%** → **CVI** = 2ª dim. del IOC (`IOC=f(ICEP,CVI)`). `instrumental=0` ES el hallazgo. **Universo doc. de Montecristi: CERRADO** (el PP puntúa prioridad, NO costo).
⏭️ **EXCEL d08** → `ESPECIFICACION_GOLD_MASTER_D08.md`. GM leído: H73 **SÍ** publica IGP (f.21-22) — hueco era el conector, **corregido**. ⛔ **NO restaurar `H24c!B7=H10b!B9`**: son Ingresos_Base = cifra falsa. **Nada bloqueado**: IGP_3(d09) · `IGP_2=0` **medido** · **SAT-IX** 46,2% · CVI en IOC.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo · B Operaciones · C Productos (los 6 de §LA TESIS · 1 motor) · D Portal `quiraintelligence.com` (radar 221 GAD).

## REGLAS DE ORO → **las 9 viven en `CLAUDE.md`** (se lee siempre · no se duplican aquí)
Las 2 que más se olvidan: **antes de definir, consultar el Inventario de Conceptos** (¿existe? → DERIVA,
no redefinas · cierre `/graphify . --update`) · **no congelar teoría antes que el grafo hable** (ADR-019).

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque normal** | **SOLO este BOOT.md. No leas nada más hasta saber tu tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Gate 7 (segundo municipio) | `docs/adr/GATE-007_Validacion_Externa_Municipio2.md` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Reglas de construcción/UI/dominios | `docs/REFERENCE.md` |
| Ingesta corpus/Holding | `scripts/holding/manifest_holding.py` (docstring) |
| Tocar el grafo Neo4j | `docs/adr/ADR-017` + `ADR-018` |
| Clasificar documentos | `docs/adr/ADR-021` + `docs/architecture/CANONICAL_CHUNK_SCHEMA.md` |
| Retomar d07 Transparencia | `docs/architecture/CATALOGO_CANONICO_CD_D07.md` + `app/agents/d07/` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB `8dc8519a` (user=DB=instance ID · MATCH+MERGE) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
