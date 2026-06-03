# QUIRA OS — Guía Canónica (Dylus Lab)

> **ARRANQUE: lee SOLO `governance/BOOT.md` primero. Nada más hasta saber tu tarea.**
> Este archivo es reglas esenciales. El detalle vive en archivos que se cargan bajo demanda
> (lazy loading) — NO los leas "por si acaso". Javo financia solo: **cada token cuenta.**

---

## PROTOCOLO DE ARRANQUE
1. Lee `governance/BOOT.md` (~400 tokens — estado + lazy-load map).
2. Identifica tu tarea. Carga SOLO el archivo de referencia que aplica (ver tabla en BOOT).
3. NO invoques `/quira-orient` ni leas QUIRA_STATE completo salvo que necesites el estado total.

## REGLAS DE ORO (inviolables — detalle en `docs/REFERENCE.md`)
1. **Excel = Estado.** Gold Master es fuente de verdad. Excel→Python→Supabase→UI, nunca al revés.
2. **Bloomberg Firewall.** NUNCA en UI/API/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226). Lenguaje de gobernanza pública, no metodología interna.
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos o cifras.
4. **No congelar teoría antes que el grafo hable.** ADR-019 a propósito en STRONGLY_SUPPORTED.
5. **No tocar congelados.** `governance/*` y `.github/workflows/*` no se modifican sin aprobación.
6. **Repo PRIVADO.** Credenciales solo en `.streamlit/secrets.toml` local. Nunca al repo.

## PROHIBICIONES (detalle completo en `docs/REFERENCE.md`)
NUNCA: hardcodear sin snapshot · agregar dominio nuevo (D01-D12 inmutables) · agregar items al
sidebar Ejecutivo · exponer QTMP/ACK IDs en UI · lenguaje acusatorio (incumplió/violó/ilegal) ·
inventar artículos de ley.

## ARQUITECTURA (1 línea — detalle en `docs/REFERENCE.md`)
Stack: Streamlit + Python + Claude Haiku + Neo4j + Supabase.
3 Cerebros: C1 Corpus (Supabase) · C2 Grafo (Neo4j) · C3 Razonamiento (futuro).
UI 3 capas: L1 Centro de Mando · L2 Dashboards dominio · L3 GeoTwin. Router: `env_gov.py` (puro).

## DÓNDE ESTÁ TODO (lazy load)
| Necesitas | Archivo |
|---|---|
| Estado vivo del proyecto | `governance/QUIRA_STATE.md` (§0 TL;DR primero) |
| 12 dominios · UI · patrones · Bloomberg detalle · skill routing | `docs/REFERENCE.md` |
| ADRs (decisiones congeladas) | `docs/adr/ADR-016..021` |
| Ontología corpus / schema | `docs/architecture/CANONICAL_CHUNK_SCHEMA.md` · `ADR-021` |
| Hallazgos territoriales | `docs/observations/OBS-003..007` |

## COMMITS
`[área]: descripción en español` + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## CIERRE DE SESIÓN (obligatorio antes de "listo")
Actualiza `governance/BOOT.md` §AHORA (gate, último commit, siguiente paso). Si cambió arquitectura → ADR. Eso evita que el próximo Claude empiece de cero.

---
*CLAUDE.md v3.0 — adelgazado para lazy loading · Dylus Lab © 2026*
*Historial completo: git + docs/REFERENCE.md + docs/adr/. Nada se perdió, solo se movió.*
