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
> **⚖️ PRINCIPIO RECTOR (elevado a la Constitución · Javo + asesor · 2026-07-07):** Toda afirmación pública posee un nivel de verificabilidad documental. La **ausencia de evidencia es un RESULTADO de auditoría, nunca una autorización para inferir hechos.** QUIRA no certifica verdad: certifica el **nivel de verificabilidad pública** (independiente·institucional·parcial·sin evidencia·contradicción). Las cadenas de QUIRA son **cadenas de integridad intersistémica**. Detalle: `CONSTITUCION_ONTOLOGICA_QUIRA.md` CAPA 0 · `docs/pcd/PCD-MN01 §21`.
1. **Excel = Estado.** Gold Master = **representación canónica de la evidencia procesada** (capa de integración), NO la verdad: la verdad vive en las **fuentes** —PDOT·POA·PAC·SERCOP·SIGAD·Presupuesto·Rendición— (ADR-029 §Precisión epistemológica). Excel→Python→Supabase→UI, nunca al revés. **La fórmula canónica (H12!B33 ICPI) es INMUTABLE** — jamás se modifica; correcciones SOLO en inputs/semáforo/presentación, sobre COPIA de trabajo, con evidencia, verificadas con dumps (openpyxl corrompe el canon). Metodología estampada: `docs/architecture/METODOLOGIA_GOLD_MASTER.md`.
2. **Bloomberg Firewall + doble registro de lenguaje.** NUNCA en UI/API/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs (Dom07·C01·CE_226). **Hacia AFUERA (público): lenguaje de administración pública. Hacia ADENTRO (Dylus Lab): el lenguaje interno** (jerga tipo "paja", node IDs, nombres de motor). Jamás la jerga interna cruza al producto (Javo · 2026-07-08).
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos o cifras.
4. **No recalcular el motor.** Métricas vienen del Excel (Regla 1 de ADR-023). Documento nuevo → QUIRA. Métrica nueva → Excel.
5. **No tocar congelados.** `governance/*` y `.github/workflows/*` no se modifican sin aprobación.
6. **Repo PRIVADO.** Credenciales solo en `.streamlit/secrets.toml` local. Nunca al repo.
7. **Anti-inflación del canon.** Ningún concepto entra si SOLO renombra: debe añadir capacidad, eliminar ambigüedad demostrable o reducir complejidad. Si solo cambia el nombre, no entra (asesor · 2026-06-30).
8. **Segunda ingeniería (del canon a la pantalla).** No es mantenimiento: se audita, cura y potencia **dominio por dominio**, del canon (Gold Master + corpus verificado) a la UI, por las **7 capas** (GM·metodológica·matemática·semántica·cableado·visual·narrativa). Cada dominio cierra con su `PCD-DXX`. Protocolo: `docs/architecture/PROTOCOLO_CURACION_DOMINIO.md` (asesor · 2026-07-02).
9. **Ningún cambio nace en Python.** Todo cambio conceptual (métrica, fórmula, definición) nace en el **canon**; Python solo deriva o implementa. El código refleja el canon, no es un segundo canon (asesor · 2026-07-02).

## PROHIBICIONES
NUNCA: hardcodear sin snapshot · agregar un dominio que NO pase el PROTOCOLO DE EXPANSIÓN ONTOLÓGICA
(6 condiciones · Constitución §Mutabilidad — la Doctrina inmutable, los dominios variables CON gate · d13 Ambiente = 1er ejercicio) · agregar items al
sidebar Ejecutivo · exponer QTMP/ACK IDs en UI · lenguaje acusatorio (incumplió/violó/ilegal) ·
inventar artículos de ley · **modificar la fórmula canónica del Gold Master (H12!B33)** · construir un motor de cálculo paralelo al Gold Master. *(Correcciones del motor: SOLO inputs/semáforo/presentación · sobre copia · con evidencia · ver `METODOLOGIA_GOLD_MASTER.md`.)*

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
