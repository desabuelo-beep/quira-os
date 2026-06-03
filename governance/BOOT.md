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
- **Sprint**: Gate 6.6 — Bridge Corpus → Motor ICPI
- **Último commit**: `106359a` — CI health-check (guardián arranque liviano + anti-secretos)
- **Gate 6.5 ✅ COMPLETO**: 13,509 chunks · 65 tablas · OBS-008/009 · ADR-022/023
- **Corpus**: ~13,509 chunks texto · 65+ tablas LOTAIP/cédulas · Neo4j: 38/58
- **Gold Master leído completo** (120 hojas): ICPI-2025=69.93% · TGI=66.79% · D3=59.85%(gap) · D4=44.79%(crítico)
- **Connector LISTO**: `app/connectors/gold_master.py` → H73_OUTPUT_API
- **Gate 6.6 ✅ COMPLETO** (Sprint Ontología Territorial):
    - 6.6A: `corpus_mnt_mapping` · 51/51 siglas MCR → MNT_UUID · 0 huérfanos
    - 6.6B: Dom01-D12 · 51/51 (100%) · D10=9 · D04=9 · D12=9 · D03=8
    - 6.6C: `explainability_report.py` — "¿Por qué ICPI=69.93%?" → respuesta automática
- **Siguiente**: **GATE-007** — Municipio #2 (Javo elige: Portoviejo/Manta/Jipijapa/Santa Ana/Chone)
    Ver `docs/adr/GATE-007_Validacion_Externa_Municipio2.md`
    Objetivo: replicar el pipeline. Si funciona: QUIRA = solución para 221 GAD del Ecuador.
- **Ver**: `docs/architecture/BRIDGE_EXCEL_CORPUS.md` · `docs/adr/ADR-023`
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED · ADR-023 ACTIVO**

## REGLAS DE ORO (inviolables — el resto en CLAUDE.md)
1. **Excel = Estado.** Gold Master es fuente de verdad. Excel→Python→Supabase→UI, nunca al revés.
2. **Bloomberg Firewall.** NUNCA en UI/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226).
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos/cifras.
4. **No congelar teoría antes que el grafo hable.** ADR-019 a propósito en SUPPORTED.
5. **Commits**: `[area]: desc en español` + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

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
