# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy loading: carga el detalle SOLO del área que vas a tocar. No leas todo "por si acaso".
> Mantener bajo 500 tokens. Actualizar `## AHORA` al cierre de cada sesión.

## QUÉ ES
QUIRA = Motor de Trazabilidad Pública Municipal (Dylus Lab). KOS, no dashboard.
Laboratorio: GAD Montecristi (MCR). Destino: 221 municipios.
3 Cerebros: **C1** Corpus normativo (Supabase pgvector) · **C2** Grafo causal (Neo4j) · **C3** Razonamiento (futuro).

## AHORA (actualizar al cierre)
- **Sprint**: Gate 6.5 — Ingesta Holding MCR (Capas C+D)
- **Último commit**: pendiente
- **Hecho**: Gate 6.5 F1-F5 ✅ · OBS-008/009 ✅ · ADR-022 SUPPORTED ✅ · **metrics_mcr anclado al Gold Master ✅**
- **Excel Canon (SIAP-ICPI v5.5)**: ICPI-2025=69.93% · TGI=66.79% · D3=59.85%(gap) · D4=44.79%(crítico)
- **Connector**: `app/connectors/gold_master.py` → H73_OUTPUT_API — USAR SIEMPRE
- **Deuda Gate 6.6**: `dominios_quira=""` en Holding → tagging Dom01-Dom12 + bridge H36_QUIRA_BRIDGE
- **Siguiente**: Gate 6.6 — tagging dominios + circuitos en Capas C/D · segundo municipio para ADR-022→CONFIRMED
- **Corpus**: ~13,509 chunks · 65+ tablas · Neo4j: 38/58 · ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED
- **No tocar**: ADR-019 sigue STRONGLY_SUPPORTED · ADR-022 candidato (espera Fase 3 PAC)

## REGLAS DE ORO (inviolables — el resto en CLAUDE.md)
1. **Excel = Estado.** Gold Master es fuente de verdad. Excel→Python→Supabase→UI, nunca al revés.
2. **Bloomberg Firewall.** NUNCA en UI/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226).
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos/cifras.
4. **No congelar teoría antes que el grafo hable.** ADR-019 a propósito en SUPPORTED.
5. **Commits**: `[area]: desc en español` + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## LAZY LOAD — lee SOLO lo que aplica a tu tarea
| Si vas a... | Lee primero |
|---|---|
| Entender estado completo | `governance/QUIRA_STATE.md` (§0 TL;DR primero) |
| Reglas de construcción/UI/dominios | `CLAUDE.md` + `docs/REFERENCE.md` |
| Ingesta corpus/Holding | `scripts/holding/manifest_holding.py` (docstring) |
| Tocar el grafo Neo4j | `docs/adr/ADR-017` + `ADR-018` |
| Clasificar documentos | `docs/adr/ADR-021` + `docs/architecture/CANONICAL_CHUNK_SCHEMA.md` |
| Hallazgos territoriales | `docs/observations/OBS-005/006/007` |
| Métricas del grafo | `data/centrality_results.json` + `ADR-019/020` |

## INFRA (credenciales en `.streamlit/secrets.toml` local, NUNCA al repo)
Neo4j AuraDB Free instancia `6c134c35` (user=DB=instance ID · patrón MATCH+MERGE) · Supabase `normativa_corpus` · repo PRIVADO.

## EQUIPO
Javo (fundador, decide) · Claude (director técnico, ejecuta) · Colega (asesor externo, revisa).
Flujo: "revise, mejore, supere, ejecute". Javo financia solo → **cada token cuenta**.
