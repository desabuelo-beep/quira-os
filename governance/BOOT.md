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
- **Último commit**: `f27d611` — Fase 2 POA completa (+3,274c) · chunker tabla umbral ≥5
- **Hecho**: Gates 6.1-6.4 ✅ · Fase 1 (RC+PP) ✅ · Gate 6.5A mining ✅ · **Fase 2 (POA, +3,274c) ✅**
- **Siguiente**: Gate 6.5 Fase 3 (PAC) → `python scripts/holding/ingest_holding.py --fase 3`
- **Corpus**: ~12,017 chunks · Neo4j: 38 nodos/58 aristas
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
