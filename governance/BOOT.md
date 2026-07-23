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
✅ **P1/P2:** kernel `umi.py`+`qinv.py` · **QINV-001 nivel BI** · QINV-006 · d03=72.73.
🔌 **MCD Planif · 7 cables ✅:** Excel·SERCOP·Relacional·Normativo·IA·Visual·Memoria.
🧭 **ADR-031 RATIF:** cajón=MCD · GoldMaster=MCM · MCIP 5 motores (Index §1.A).
🔑 **AUDIT 18-jul:** COOTAD-2026 70%/piso65% dic-2026 · d03 COPLAFIP41-42.
✅ **4 DOM cerrados con PCD: d01·d02·d03·d09** (molde d01: dictamen + qc-ev + fundamento jurídico).
📚 **ADR-038 BRN v2 RATIF:** nodo = REGLA, no artículo. 4 niveles **Corpus→CNO(Derecho)→RO(lógica)→SAT**. BRN = CAPA (no cajón) que CONSOLIDA (no interpreta). **Corpus v1.0 CONGELADO** (43 docs·9158 chunks·grafo cerrado·`parser-v1.0`; v1.1=refs cruzadas). **BRN v2.1**: d01+d02+d03+d09 CONFORMES·5 RO·suite 12✓·diff=0.
🩺 **Canon curado por el DOM (Regla 8), ICPI intacto · centinela ✅. Gate real = `python scripts/ci/check_health.py` (BOOT≤6000·CLAUDE≤4000): NO adivinar.**
📚 **ADR-035/037 (RATIF):** Ley→BRN→GoldMaster(único motor)→QUIRA · IA propone, humano valida. Frame: Gobierno(página propia)·Territorio·Inteligencia·Norma(BRN).
🏛️ **d02+d03 migrados (2026-07-23):** motor.py envuelve `enrich_presupuesto.py`/`enrich_mandato.py` (ya prod). d02: 4 capacidades+3 SAT — **bug ICPI÷100 doble en 13 celdas, corregido** (OBS-013). d03: 2 métricas (incorporación=hecho 98.7%·calidad=índice 79.3%), Fase2 auditoría sin hallazgos, drift YAML↔Neo4j=0 (`EVIDENCIA_d03`). Antes: 26/34 SHA BRN obsoletos+CE Art.241 perdido → corregidos (OBS-012, Corpus v1.0.1). d07/d01/d02/d03 IMPORTAN `_template`. Neo4j 145 nodos. Falta d09. **Fase4/Haiku=pausa**.

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
| Retomar d07 Transparencia | `docs/architecture/CATALOGO_CANONICO_CD_D07.md` + `METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP.md` + `app/agents/d07/` |
| Estado histórico completo (snapshot) | `governance/historico/QUIRA_STATE_2026-06-03.md` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB Free instancia `8dc8519a` (user=DB=instance ID · patrón MATCH+MERGE) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
