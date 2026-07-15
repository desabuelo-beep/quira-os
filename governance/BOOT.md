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
Negocio = complementario (cooperación/certificación), no licencias. **Detalle: `HOJA_DE_RUTA_MAESTRA.md §0` · ADR-024.**

## 📜 CONSTITUCIÓN → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` · 🗺️ RUTA → `governance/HOJA_DE_RUTA_MAESTRA.md`
Constitución = QUÉ ES QUIRA (CAPA 0 Doctrina + 4 macroejes + 12 dominios): mide la CONGRUENCIA de
PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO y halla las BRECHAS. Los dominios cambian;
la Doctrina permanece. Hoja de Ruta = el mapa que no se mueve. BOOT §AHORA = el paso actual.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
**CENTRO DE INTELIGENCIA TERRITORIAL · 2026-07-01.** QUIRA preventiva. Excel=Canon INVISIBLE.
✅ **P1/P2:** kernel `umi.py`+`qinv.py` · **QINV-001 nivel BI** · QINV-006 · d03=72.73.
🔧 **Backbone:** PDOT 25 metas · POA 257 proy $39.3M · Presup $45.98M · PAC $29.85M.
🔌 **MCD Planif · 7 cables ✅:** Excel·SERCOP·Relacional·Normativo·IA·Visual·Memoria.
🧭 **ADR-031 RATIF:** cajón=MCD · GoldMaster=MCM · MCIP 5 motores (Index §1.A).
🔑 **Planif✓ · RDC✓ · d02 v3✓** — 4 capacidades + SAT (Norma→Regla→Señal) + cadena inter-dominio.
📚 **ADR-035 BRN RATIF:** DOM Alertas **transmuta** en Biblioteca de Reglas (no se elimina). Ley→BRN→GoldMaster (único motor)→QUIRA. **IA propone, humano valida.**
🔶 **CI:** BOOT ≤6KB.

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: A Núcleo (motor·grafos·conectores·índices) · B Operaciones (Dylus) · C Productos (Institucional·Ciudadana·Impact·Economic·Cooperación · 1 motor) · D Portal `quiraintelligence.com` (radar 221 GAD). Montecristi = Municipio 001.

## REGLAS DE ORO → **las 9 viven en `CLAUDE.md`** (se lee siempre · no se duplican aquí)
Recordatorio de las 2 que más se olvidan: **el grafo es autoridad** (antes de definir: ¿existe? → DERIVA,
no redefinas · al cierre `/graphify . --update`) · **no congelar teoría antes que el grafo hable** (ADR-019).

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| **Arranque normal** | **SOLO este BOOT.md. No leas nada más hasta saber tu tarea.** |
| Arquitectura 3 niveles (inmutable) | `docs/adr/ADR-023` |
| Gate 6.6 / tagging / bridge Excel | `docs/architecture/BRIDGE_EXCEL_CORPUS.md` |
| Gate 7 (segundo municipio) | `docs/adr/GATE-007_Validacion_Externa_Municipio2.md` |
| Leer métricas del Gold Master | `app/connectors/gold_master.py` → NO recalcular |
| Reglas de construcción/UI/dominios | `docs/REFERENCE.md` |
| Ingesta corpus/Holding | `scripts/holding/manifest_holding.py` (docstring) |
| Tocar el grafo Neo4j | `docs/adr/ADR-017` + `ADR-018` |
| Clasificar documentos | `docs/adr/ADR-021` + `docs/architecture/CANONICAL_CHUNK_SCHEMA.md` |
| Hallazgos territoriales | `docs/observations/OBS-005/006/008/009` |
| Estado histórico completo (snapshot) | `governance/historico/QUIRA_STATE_2026-06-03.md` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB Free instancia `6c134c35` (user=DB=instance ID · patrón MATCH+MERGE) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
