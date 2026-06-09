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
- **Sprint A ✅ COMPLETO** (2026-06-04) · **ADR-026 v1.2 ✅ MODELO OPERATIVO** (2026-06-09)
- **FASE 0 — Arqueología funcional ✅ COMPLETA** (2026-06-09):
    9 excavaciones: D02 · D03 · D04 · D06 · D07 · D08 · D09 · D10 · D12
    Hallazgo central: QUIRA tiene taxonomía funcional de 4 tipos (no 12 dominios iguales)
    → Tipo A (7 generadores) · Tipo B (D06 sintetizador) · Tipo C (D09 protocolo) · Tipo D (D01 D05 corpus)
    → D12 = membresía dual A+D (primer caso) · D02 = capa consecuencia financiera ($3.66M)
    → D03 = puente PDOT-Operaciones · IFE-A 72.73% único · mod=None (deuda activa)
    → Cadena epistemológica completa: Norma→Observación→Interpretación→Validación
    → ADR-026 v1.2: `docs/adr/ADR-026_Topologia_Funcional_QUIRA.md`
- **SECUENCIA OPERACIONES** (consecuencia de ADR-026):
    FASE 1 → QUIRA Operaciones (Bloomberg Firewall + deudas activas)
    FASE 2 → QUIRA Institucional (Sprint B — 12 puertas por Tipo Funcional)
- **Próximos pasos inmediatos** (FASE 1 Operaciones):
    1. ✅ Taxonomía Tipo A cerrada (D02+D03+D12 confirmados)
    2. **D02 REDISEÑO** (2026-06-09): `p18_cooperacion.py` portfolio bonds → retirado sin base Excel
       Nuevo concepto: inteligencia dinámica · reembolsable/no-reembolsable · GAD/ONG/OSC/Academia/Startup/coaliciones
       Skill pendiente: `/fondos-radar` (~15 días actualización) · render desde snapshot
    3. Bloomberg Firewall: corregir p9_sat · p7_brecha · p10_inversion · p15_transparencia
    4. Deprecar `p15_transparencia.py` (código muerto activo — riesgo Bloomberg)
    5. Wiring D03: `p8_metas.py` sin ruta sidebar (mod=None → agregar ruta en env_gov.py)
    6. D12 roadmap datos faltantes: IGM-A,B,C,F sin fuente Excel (RRHH · DAF · CNE · PNUD)
    7. Completar C02 + C03 (specs parciales ADR-017)
    8. Formalizar C-RDC en Neo4j (spec lista en ADR-026)
- **Pendiente verificar**: UI Sprint A con `streamlit run app.py` (Tarea A3 — sigue pendiente)
- **Histórico** `fb78876` (2026-06-08): `historico-construccion-quira.md` + `ultima-conversacion-director-claude.md`
- **Grafo**: pendiente `/graphify . --update` (fix Windows listo · usage reset a las 7:10pm Guayaquil)
    Nuevos artefactos: ADR-026 + sesión arqueología completa
- **Gate 6.6 ✅ · Corpus**: ~13,509 chunks · Neo4j: 38/58
- **Connector LISTO**: `app/connectors/gold_master.py` → H73_OUTPUT_API + fallback TGI
- **GATE-007 🧊 CONGELADO** — Manta = Municipio 002 · retomar post-Montecristi v1.0
- **Roadmap revisado**: A✅→[Operaciones]→B→C→D→E→F
    Operaciones: D02+D03+D12 excavación · Bloomberg · C-RDC Neo4j
    B: 12 Puertas diseñadas por Tipo Funcional (post-Operaciones)
- **ADR-019 STRONGLY_SUPPORTED · ADR-022 SUPPORTED · ADR-023 ACTIVO · ADR-024 RATIFICADO · ADR-026 RATIFICADO**

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
