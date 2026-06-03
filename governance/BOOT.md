# QUIRA · BOOT

> **Único archivo de arranque.** Léelo y NADA más hasta saber en qué vas a trabajar.
> Lazy loading: carga el detalle SOLO del área que vas a tocar. No leas todo "por si acaso".
> Mantener bajo 500 tokens. Actualizar `## AHORA` al cierre de cada sesión.

## QUÉ ES
> **"El Gold Master ya sabe medir la gestión pública; QUIRA está aprendiendo a
> demostrar documentalmente por qué cada métrica del Gold Master es verdadera o falsa."**
>
> Gate 6.6 no agrega datos. Agrega significado.
> Objetivo: **sistema de auditoría explicable del modelo ICPI.**

**3 niveles** (ADR-023 — inmutable):
- **Nivel 1 Motor**: Gold Master SIAP-ICPI v5.5 — calcula ICPI/TGI/SAT/MMP. Leer via `app/connectors/gold_master.py`. NUNCA recalcular fuera del Excel.
- **Nivel 2 SO**: QUIRA — ingesta + trazabilidad (MNT_UUID) + evidencia documental
- **Nivel 3 UI**: Dashboards + GeoTwin — solo visualizan, no calculan

**MATRIZ_CANONICA** del Excel = ADN compartido. Sin ella: dos mundos. Con ella: un sistema.

## AHORA (actualizar al cierre)
- **Sprint**: Gate 6.5 — Ingesta Holding MCR (Capas C+D)
- **Último commit**: `6be6888` — ADR-023 completo · identidad definitiva · cierre sesión
- **Excel Canon (120 hojas)**: 9 Silos S1-S9 · Motor ICPI H12 · ICPI-2025=69.93% · TGI=66.79%
- **Fórmula**: ICPI = Σ(Pi×Ri×Vi×Ei×Ti×Ci)/Σ(Pi×Ri) · Vi=producto lógico 4 verificadores
- **Connector**: `app/connectors/gold_master.py` → H73_OUTPUT_API — ÚNICA FUENTE DE VERDAD
- **Gate 6.5 (hecho)**: corpus = evidencia para silos S5/S7/S8
- **Gate 6.6 (siguiente — EL MAS IMPORTANTE)**:
    1. `tag_mnt_uuid.py` → SIGLA corpus → MNT_UUID (MATRIZ_CANONICA) → Silo → Variable
    2. `update_silos.py --silo s5` → Ti real LOTAIP → H07 (Excel recalcula ICPI)
    3. `verify_cpccs.py` → V_CPCCS real desde RC → H10
- **Ver**: `docs/architecture/BRIDGE_EXCEL_CORPUS.md` — cadena completa + mapa SIGLA→MNT→Silo
- **ADR-022 corregido**: cadena Norma→Instrumento→Ejecución→Evidencia→Motor ICPI
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED**
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
