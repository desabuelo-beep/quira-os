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
- **Sprint A ✅ COMPLETO** (2026-06-04) · **ADR-026 v1.3 ✅ MODELO OPERATIVO** (2026-06-09)
- **FASE 0 — Arqueología funcional ✅ COMPLETA** (2026-06-09):
    9 excavaciones: D02 · D03 · D04 · D06 · D07 · D08 · D09 · D10 · D12
    Taxonomía 5 capas: Tipo D (corpus) · A (7 generadores) · B (sintetizador) · C (protocolo) · A² (consecuencia)
    → ADR-026 v1.3: `docs/adr/ADR-026_Topologia_Funcional_QUIRA.md`
    → MAPA_FUNCIONAL_QUIRA_v1: `docs/architecture/MAPA_FUNCIONAL_QUIRA_v1.md`
    → QUIRA_DATA_REGISTRY_v1: `docs/architecture/QUIRA_DATA_REGISTRY_v1.md`
- **FASE 1 Operaciones — EN CURSO D02** — último commit `1879d84` (2026-06-09):
    ✅ Bloomberg Firewall `2571e23`: p7_brecha · p10_inversion · p15_transparencia (deprecated) · m3_municipal · p_cadena
    ✅ D03 routing `205af2a`: mod=metas → p8_metas.py (IFE-A 72.73% ahora accesible)
    ✅ QUIRA_DATA_REGISTRY_v1 `2f8a98f`: ~32 LIVE · 10 MISSING · 2 HARDCODED · 1 PENDIENTE
    ✅ D02 Migración 002 `1879d84`: 5 tablas Supabase + 21 requisitos + 21 emisores ancla
       fondos_emisores · fondos_convocatorias · fondos_requisitos · fondos_conv_requisitos · fondos_elegibilidad
- **D02 MOTOR DE ELEGIBILIDAD — 4/4 PASOS COMPLETOS** (último commit pendiente):
    ✅ A.0 Schema 5 tablas Supabase (aplicado y verificado)
    ✅ A.1 Semilla: 21 requisitos (4 familias) + 21 emisores ancla + 5 convocatorias test
    ✅ B. `app/engines/fondos_matcher.py` — MCR-001: elegible=2·brecha=1·no_elegible=2·USD 1.3M
    ✅ C. `app/engines/fondos_simulator.py` — PSG→30%: ONU Mujeres USD 300K / ISP→65%: BDE USD 5M
    ✅ D.1 `quira_pages/p18_cooperacion.py` — rewrite COMPLETO como lector puro Supabase
       4 tabs: Disponible hoy · Bloqueado/Brechas · Simulador · Por emisor
       Bloomberg-safe: indicadores_display via demo_data (escala %) · nombre_publico para gates
    ⬜ D.2 skill /fondos-radar (Fetcher — ciclo 15 días, siguiente sesión)
    ⚠️  NOTA: Gold Master almacena ISP/PSG como fracción decimal (0.028 = 2.8% ≠ 14.58%)
       Renderer usa demo_data.INDICES para display (escala % correcta). Matcher usa Gold Master (correcto).
- **PENDIENTES BLOQUEANTES pre-Sprint B**:
    🟡 D02 Paso D.2: skill /fondos-radar (Fetcher auto-discovery, ciclo 15 días)
    🔴 IFE-E (D03): trazabilidad POA→PAC→eSIGEF → Dirección Financiera GAD
    🟠 D12 datos faltantes: IGM-A,B,C,F (RRHH · DAF · PNUD · CNE) — solicitar formalmente
    🟡 C-RDC en Neo4j: YAML spec lista en ADR-026 → ejecutar Cypher AuraDB
    🟡 C02 + C03: specs parciales ADR-017 → completar
    ⬜ Verificar UI Sprint A: `streamlit run app.py` (Tarea A3)
    ⬜ Graphify update: `/graphify . --update` (artefactos nuevos: ADR-026 v1.3 · MAPA · REGISTRY)
- **Histórico** `fb78876` (2026-06-08): `historico-construccion-quira.md` + `ultima-conversacion-director-claude.md`
- **Gate 6.6 ✅ · Corpus**: ~13,509 chunks · Neo4j: 38/58
- **Connector LISTO**: `app/connectors/gold_master.py` → H73_OUTPUT_API + fallback TGI
- **GATE-007 🧊 CONGELADO** — Manta = Municipio 002 · retomar post-Montecristi v1.0
- **Roadmap revisado**: A✅→[Operaciones ~90%]→B→C→D→E→F
    Siguiente: D02 `/fondos-radar` + C-RDC Neo4j → Sprint B (12 puertas por Tipo Funcional)
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED · ADR-023 ACTIVO · ADR-024 RATIFICADO · ADR-026 v1.3 RATIFICADO**

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
