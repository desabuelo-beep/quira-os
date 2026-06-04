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
- **Sprint**: Sprint A — Identidad Institucional (ficha viva Montecristi · pantalla base)
    Auditoría UX hecha (2026-06-04): login + dashboard revisados con Playwright
    Hallazgos críticos: tagline frío · "53.6% Ruptura Sistémica" sin contexto · dominios=tarjetas no puertas
- **Grafo QUIRA v2**: `graphify-out/graph.json` ✅ — 1938 nodos · 3238 aristas · MCP activo
    Incluye: ADRs 001-023 · governance · código Python · Gold Master schema · Vault Obsidian 00_CORE + TGI parroquias
    Gold Master TGI = 5to nodo más conectado (degree 26) — hub metodológico confirmado
    Próxima actualización: `/graphify . --update` al cerrar Sprint A
- **Último commit**: `106359a` — CI health-check · tag `boot-estable-v1` creado
- **Gate 6.6 ✅ COMPLETO**: 51/51 siglas MCR · 0 huérfanos · ICPI=69.93% explicable
- **Corpus**: ~13,509 chunks · 65 tablas LOTAIP · Neo4j: 38/58
- **Connector LISTO**: `app/connectors/gold_master.py` → H73_OUTPUT_API
- **GATE-007 🧊 CONGELADO** — no cancelado · Manta elegida · retomar post-Montecristi v1.0
- **DECISIÓN ESTRATÉGICA (2026-06-03)**: QUIRA = familia de productos
    - QUIRA Institucional (70% sistema, 20% producto) → PRIORIDAD: invertir relación
    - QUIRA Operaciones → módulo técnico municipal (UI sobre pipeline) → sprint E
    - QUIRA Ciudadana → post Institucional+Operaciones · hereda ambos
    - QUIRA Impact / Cooperación / Economic → motor financiero post-Montecristi v1.0
- **Roadmap activo**: A→B→C→D→E→F (Montecristi v1.0) → Gate 7
    A: Contexto Cantonal · B: 12 Dominios (puertas) · C: Dashboard+IA analista
    D: GeoTwin conectado · E: QUIRA Operaciones · F: v1.0 completo
- **UI norte**: institucional · premium · territorial · ecuatoriana (NO SaaS genérico)
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED · ADR-023 ACTIVO**

## REGLA CANÓNICA NUEVA (2026-06-03)
**Todo artefacto construido entra al grafo.** Docs, decisiones, specs, planes, versiones históricas.
La memoria histórica es la base de QUIRA dialéctica / autorregenerativa.
Comando: `/graphify . --update` al cierre de cada sesión con nuevos artefactos.

## ARQUITECTURA DE 4 CAPAS (ADR-024 — RATIFICADO 2026-06-04)
**Pregunta central a ratificar: ¿QUIRA es software municipal o radar nacional?**
Los 3 convergemos en: RADAR NACIONAL independiente. (GAD = sujeto observado, no cliente)
- **Capa A NÚCLEO**: Gold Master · QLEP · Graphify · GeoTwin · conectores · NLP · índices (ya construido)
- **Capa B OPERACIONES**: CAPACIDAD interna Dylus Lab (NO producto). Hoy = Javo+Claude+Colega
- **Capa C PRODUCTOS**: Institucional · Ciudadana · Impact · Economic · Cooperación (5 UIs, 1 motor)
- **Capa D PORTAL** = **PRODUCTO PRINCIPAL**: quiraintelligence.com = radar vivo 221 GAD
    quiraholding.streamlit.app = LABORATORIO donde validamos el motor (no es el producto final)
- **Montecristi = Municipio 001** (laboratorio). NO cambia sprints; SÍ cambia interpretación.
- ADR-024 RATIFICADO. Capa D disponible post-Montecristi v1.0.

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
