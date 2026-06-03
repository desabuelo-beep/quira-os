# QUIRA OS — Guía Canónica (Dylus Lab)

> **ARRANQUE: lee SOLO `governance/BOOT.md`. Nada más hasta saber tu tarea.**
> BOOT.md = estado vivo + mapa lazy-load. Carga el detalle SOLO del área que tocas.
> NO leas archivos "por si acaso". Javo financia solo: **cada token cuenta.**

## QUÉ ES QUIRA (1 párrafo — evita reconstruir lo que ya existe)
QUIRA NO calcula métricas: las **demuestra documentalmente**. El **Gold Master**
(Excel SIAP-ICPI v5.5) ES el motor — calcula ICPI/TGI/SAT/MMP. QUIRA ingiere
evidencia, la traza (MNT_UUID) y la explica. **Si un número existe en el Excel,
NINGÚN script lo recalcula** — se lee vía `app/connectors/gold_master.py`.
Detalle: `docs/adr/ADR-023` (3 niveles, inmutable).

## REGLAS DE ORO (inviolables)
1. **Excel = Estado.** Gold Master es fuente de verdad. Excel→Python→Supabase→UI, nunca al revés.
2. **Bloomberg Firewall.** NUNCA en UI/API/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226). Lenguaje de gobernanza, no metodología interna.
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos o cifras.
4. **No recalcular el motor.** Métricas vienen del Excel (Regla 1 de ADR-023). Documento nuevo → QUIRA. Métrica nueva → Excel.
5. **No tocar congelados.** `governance/*` y `.github/workflows/*` no se modifican sin aprobación.
6. **Repo PRIVADO.** Credenciales solo en `.streamlit/secrets.toml` local. Nunca al repo.

## PROHIBICIONES
NUNCA: hardcodear sin snapshot · agregar dominio nuevo (D01-D12 inmutables) · agregar items al
sidebar Ejecutivo · exponer QTMP/ACK IDs en UI · lenguaje acusatorio (incumplió/violó/ilegal) ·
inventar artículos de ley · construir un motor de cálculo paralelo al Gold Master.

## ARQUITECTURA (1 línea — detalle en `docs/REFERENCE.md`)
Stack: Streamlit + Python + Claude Haiku + Neo4j + Supabase. 3 Cerebros: C1 Corpus (Supabase) · C2 Grafo (Neo4j) · C3 Razonamiento.
UI 3 capas: L1 Centro de Mando · L2 Dashboards dominio · L3 GeoTwin. Router: `env_gov.py` (puro).

## COMMITS
`[área]: descripción en español` + trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`

## CIERRE DE SESIÓN (obligatorio antes de "listo")
Actualiza `governance/BOOT.md` §AHORA (gate, último commit, siguiente paso). Si cambió arquitectura → ADR.
NO crees nuevos docs de estado — BOOT.md es la única fuente viva.

---
*CLAUDE.md v4.0 — mínimo, sin redundancia con BOOT · Dylus Lab © 2026*
*Mapa completo de archivos: tabla LAZY LOAD en `governance/BOOT.md`. Nada se perdió.*
