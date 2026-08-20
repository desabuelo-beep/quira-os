# QUIRA OS — Guía Canónica (Dylus Lab)

> **ARRANQUE: lee SOLO `governance/BOOT.md`. Nada más hasta saber tu tarea.**
> NO leas archivos "por si acaso". Javo financia solo: **cada token cuenta.**

## QUÉ ES QUIRA
QUIRA NO calcula métricas: las **demuestra documentalmente**. El **Gold Master** (Excel SIAP-ICPI v5.5)
ES el motor — calcula ICPI/TGI/SAT/MMP. QUIRA ingiere evidencia, la traza (MNT_UUID) y la explica.
**Si un número existe en el Excel, NINGÚN script lo recalcula** — se lee vía `app/connectors/gold_master.py`.
Detalle: `docs/adr/ADR-023` (3 niveles, inmutable).

## REGLAS DE ORO (inviolables)
> **⚖️ PRINCIPIO RECTOR:** toda afirmación pública tiene un nivel de verificabilidad documental. La **ausencia
> de evidencia es un RESULTADO de auditoría, nunca autorización para inferir hechos.** QUIRA no certifica
> verdad: certifica **verificabilidad** (independiente·institucional·parcial·sin evidencia·contradicción).
> Detalle: `CONSTITUCION_ONTOLOGICA_QUIRA.md` CAPA 0 · `docs/pcd/PCD-MN01 §21`.
1. **Excel = Estado.** Gold Master = representación canónica de la evidencia procesada, NO la verdad: la verdad vive en las **fuentes** (PDOT·POA·PAC·SERCOP·SIGAD·Presupuesto·Rendición · ADR-029). Excel→Python→Supabase→UI, nunca al revés. **La fórmula canónica (H12!B33 ICPI) es INMUTABLE**; correcciones SOLO en inputs/semáforo/presentación, sobre COPIA, con evidencia. Método: `docs/architecture/METODOLOGIA_GOLD_MASTER.md`.
2. **Bloomberg Firewall + doble registro.** NUNCA en UI/API/público: ICPI·TGI·Ti·QTMP·H01-H99·Gold Master·node IDs. **AFUERA: lenguaje de administración pública. ADENTRO: lenguaje interno.** La jerga jamás cruza al producto.
3. **Sin norma verificada (SHA256), no hay dato.** Prohibido alucinar artículos o cifras.
4. **No recalcular el motor.** Documento nuevo → QUIRA. Métrica nueva → Excel.
5. **No tocar congelados.** `governance/*` y `.github/workflows/*` no se modifican sin aprobación.
6. **Repo PRIVADO.** Credenciales solo en `.streamlit/secrets.toml` local.
7. **Anti-inflación del canon.** Si un concepto SOLO renombra, no entra: debe añadir capacidad, eliminar ambigüedad o reducir complejidad.
8. **Segunda ingeniería.** Se cura **dominio por dominio**, del canon a la UI, por las 7 capas; cada uno cierra con su `PCD-DXX`. Protocolo: `docs/architecture/PROTOCOLO_CURACION_DOMINIO.md`.
9. **Ningún cambio nace en Python.** Todo cambio conceptual nace en el **canon**; Python solo implementa.

## PROHIBICIONES
NUNCA: hardcodear sin snapshot · agregar un dominio que no pase el **Protocolo de Expansión Ontológica**
(6 condiciones · Constitución §Mutabilidad) · agregar items al sidebar Ejecutivo · exponer QTMP/ACK IDs en UI ·
lenguaje acusatorio (incumplió/violó/ilegal) · inventar artículos de ley · **modificar la fórmula canónica
(H12!B33)** · construir un motor de cálculo paralelo al Gold Master.

## ARQUITECTURA (detalle en `docs/REFERENCE.md`)
Streamlit + Python + Claude Haiku + Neo4j + Supabase. 3 Cerebros: C1 Corpus · C2 Grafo · C3 Razonamiento.
UI 3 capas: L1 Centro de Mando · L2 Dashboards dominio · L3 GeoTwin. Router: `env_gov.py` (puro).

## COMMITS
`[área]: descripción en español` + trailer `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`

## CIERRE DE SESIÓN (obligatorio antes de "listo")
1. Actualiza `governance/BOOT.md` §AHORA (gate, último commit, siguiente paso). Si cambió arquitectura → ADR.
2. **Corre `python scripts/ci/check_health.py`** ANTES de commitear gobernanza. Es el gate real (BOOT ≤6000 b,
   CLAUDE.md ≤4000 b). **No adivines el tamaño ni inventes guards**: el check te da el número exacto.
NO crees nuevos docs de estado — BOOT.md es la única fuente viva.

---
*CLAUDE.md v4.1 — mínimo, sin redundancia con BOOT · Dylus Lab © 2026*
*Mapa completo de archivos: tabla LAZY LOAD en `governance/BOOT.md`. Nada se perdió.*
