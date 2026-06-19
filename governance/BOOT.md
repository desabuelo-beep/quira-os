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

## 🎯 LA TESIS (lo que NUNCA se debe olvidar — Javo lo ha dicho muchas veces)
**QUIRA NO vende software a municipios. El GAD es SUJETO OBSERVADO, no cliente** (ADR-024).
QUIRA = **OBSERVATORIO NACIONAL DE INTEGRIDAD TERRITORIAL** (221 GADs). Montecristi = el MOLDE.
Cobertura nacional con **3 MOTORES = los 3 productos de Fase 1**: **Operaciones** (Dylus/QUIRA IA
barre Transparencia/SERCOP/CPCCS + extrae PDOT) · **Ciudadana** (la gente + cascada legal con firma
digital) · **Institucional/Gestión** (el GAD aporta dato ORO directo · GAD predictivo). Fase 2
(después, vistas de explotación): **Cooperación · Impact · Economic** (6 productos total · ADR-024).
Diferenciador: Plan CNE + NLP discurso RDC = demagogia expuesta. Ventana: **elecciones alcaldes
NOV-2026**. Negocio central = complementario (cooperación/certificación/estándar), no licencias.
Detalle completo: `HOJA_DE_RUTA_MAESTRA.md §0`.

## 📜 CONSTITUCIÓN ONTOLÓGICA → `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md`
**Define QUÉ ES QUIRA (capa 0 Doctrina + 4 macroejes + 12 dominios).** QUIRA mide la
CONGRUENCIA de la cadena PROMESA→PLAN→PRESUPUESTO→EJECUCIÓN→RESULTADO→TERRITORIO y
encuentra las BRECHAS. Los 12 dominios cambian; la Doctrina permanece. Esto, no los
dashboards, es lo que se define UNA vez. Sprint C: ontología antes que ingeniería.

## 🗺️ HOJA DE RUTA COMPLETA → `governance/HOJA_DE_RUTA_MAESTRA.md`
**Para la RUTA (qué sigue, sprints, productos, GeoTwin 3D, Ciudadana, CAF): leer ese archivo.**
BOOT.md §AHORA = detalle vivo del paso actual. Hoja de Ruta = el mapa completo que no se mueve.

## AHORA (estado vivo · historial → `governance/historico/BOOT_2026-06-17.md`)
**OLA 1 COMPLETA** — 3 hardcodes críticos al motor: d05 Holding 12.4% (h90) · d08 Participación 48.33% · d12 Género 2.83% (vectores). Patrón: tarjeta→detalle→firewall→commit. Último `fea4d28`.
**Firewall (ADR-027 · 3 capas):** deuda **Familia=47** (real) · canon Dylus/IA=37 · BAJO=58 · 9 cajones+calib · 3 mixtas resueltas.
▶ **Blitz→0:** `p11`9·`p8_metas`8·`p17_rdc`7·`p07`6·`p5_op`6·`p10_inv`4·`p4_geo`3·menores4. Mixto=Familia 100% pública (canon en capa Dylus). Pendiente ruling: TPS/AVEP/IGM/RC-M.
⚠ **CI:** BOOT.md límite 6KB. §AHORA LEAN — al cierre REEMPLAZAR (no apilar) + archivar a `historico/`.

## REGLA CANÓNICA — todo artefacto al grafo
`/graphify . --update` al cierre con artefactos nuevos (memoria histórica = base dialéctica autorregenerativa).

## ARQUITECTURA — RADAR NACIONAL (ADR-024 ratificado · detalle en el ADR)
GAD = sujeto observado, NO cliente. 4 capas: **A Núcleo** (Gold Master·QLEP·Graphify·GeoTwin·conectores·NLP·índices) · **B Operaciones** (capacidad interna Dylus) · **C Productos** (Institucional·Ciudadana·Impact·Economic·Cooperación · 5 UIs, 1 motor) · **D Portal** = `quiraintelligence.com` (radar vivo 221 GAD) · `quiraholding.streamlit.app` = laboratorio · Montecristi = Municipio 001.

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
