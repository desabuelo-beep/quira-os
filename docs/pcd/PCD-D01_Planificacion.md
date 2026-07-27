---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2]
  type: NORMATIVA
---

# PCD-D01 · Planificación Estratégica (QINV-001)

> **Expediente de Curación de Dominio** — primer aplicación del `PROTOCOLO_CURACION_DOMINIO.md`.
> Sesiones 2026-07-01 / 07-02 · Director: Claude · Fundador: Javo · Asesor externo.
> *"¿Por qué Planificación quedó exactamente así?"* — aquí está la respuesta, de cabo a rabo.

## Estado inicial
Cajón QINV-001 a "nivel BI": UI de expediente **forense** (2 pestañas Datos/Análisis), encabezado de
investigación + pregunta + estado. En el Gold Master, el IPE era un **proxy** (`B9 = Devengado × 0.84`,
circular). Sin cobertura de metas calculada. Coherencia relegada a 4 pastillas ilegibles. Registro casual
("aterriza", "el dinero se mueve donde el plan manda"). Sin marco legal por eslabón.

## Hallazgos (auditoría de 7 capas)
1. **Gold Master:** IPE proxy ×0.84 (no real) · POA→Meta aproximado (257 proyectos con objetivo-texto, no `ID_Meta`).
2. **Metodológica:** el veredicto era un % de "fidelidad" (dimensión TGI interna, sensible al Firewall, sobresimplificaba) → se reemplazó por criterio cualitativo + señal de coherencia.
3. **Matemática (el caso insignia):** el proxy no representaba "% del gasto vinculado a metas". El match EXACTO daba **61% — artefacto** (el POA agrega `71` a 2 díg, el eSIGEF ejecuta `710xxx` a 6). Match **jerárquico** → IPE real **95.6%**. *Investigar antes de estampar evitó un número falso.*
4. **Semántica:** MCIP → "Motores Analíticos QUIRA" · "cobertura POA" ≠ "Presupuesto Municipal" (POA es programación, no instrumento financiero) · ruteo de 5 hojas (H11b/H16b→d01 · H19→d02 · H37/H38 transversales).
5. **Cableado:** el IPE vivía como **valor stampeado desde Python** en H16b → se movió a **fórmula nativa** en el Excel. Enricher preserva `base_normativa` en re-runs.
6. **Visual:** cromo forense → **flujo documental** único · dona → barra (más análisis) · cards de color · fuentes ↑ · cronograma con marcador de corte (plan ≠ ejecución) · 4 motores SAT (grafo bipartito, scatter, cadena de evidencia, estado limpio) honestos "en formación".
7. **Narrativa:** registro elevado a administración pública ("se formula en concordancia con", "obras de mayor cuantía inician") · marco legal **verificado** por eslabón · síntesis ejecutiva por eslabón.

## Cambios en el canon
- **Gold Master (H16b, aditivo · B33 INTACTA · guardián pasa · 0 errores nuevos · 3 cirugías):**
  `B12` Cobertura_Metas_POA=96% (fórmula) · `B15` IPE_Ejecutado (=B16/B7) · `B16` Inversión_Vinculada = **`SUMAPRODUCTO` nativo** (devengado inversión de H07 con partida en el POA de H05, exacto o prefijo de grupo) · `B17` no-PDOT. Detalle: `CIRUGIA_GOLD_MASTER_20260701_IPE_COBERTURA.md` §3-8.
- **Corpus:** marco legal por eslabón (artículos verificados sha256) vía `base_normativa.por_eslabon`.
- **Snapshot (`planificacion`):** +`cobertura_metas_poa` +`ipe_ejecutado` +`ipe_por_objetivo` +`base_normativa.por_eslabon`.
- **Motores:** `enrich_planificacion.py` (cobertura, IPE, bridge por objetivo, preservación normativa) · `normativa_planificacion.py` (marco por eslabón).
- **UI (`m_planificacion.py`):** reescritura documental completa + 4 motores SAT + síntesis + ley inline.
- **Anclaje:** ruteo de 5 hojas en `MAPA_ANCLAJE_MOTOR.md`.

## Validación
- **Gold Master (Excel COM · 3 cirugías):** `H12!B33` = 0.27458226534062735 idéntica siempre · guardián `B40` = ICPI 69.9309% pasa · 5=5 errores (0 nuevos).
- **Excel ↔ Python:** la fórmula nativa reproduce el bridge al centavo — vinculada **$1,861,533.08**, IPE **95.57%**.
- **UI:** compile + render headless OK (53 bloques, 7 gráficas) · **Firewall limpio** (sin ICPI/TGI/H-series/IPE en pantalla).
- **Disciplina:** el 61% artefacto se cazó ANTES de estampar (capa 3).

## Estado final
Dominio **CERRADO de cabo a rabo**: IPE-ejecutado **95.6%** como fórmula **nativa y auditable** en el Gold
Master (el auditor lo sigue celda a celda) · cobertura 96% · ruteo anclado · cajón documental con marco legal
verificado + 4 motores SAT + síntesis ejecutiva · registro de administración pública. **Nivel objetivo (12)**
= fiel a la fuente (el POA no etiqueta por las 25 metas). El **25-metas es adquisición de dato** (POA con
meta-tag de origen · verificado inexistente en corpus), no un cómputo pendiente.

**Commits:** `cc05531` (cobertura+UI+ruteo) → `78a629a` (anclaje) → `d0fc250` (IPE-ejec) → `b9866a8` (forma+ley)
→ `f40a87f` (marco legal) → `cb24266` (síntesis) → `0926662` (motores SAT) → `c80c7be` (pinceladas) →
`6bc4d62` (IPE nativo audit-grade).

---
*PCD-D01 · Dylus Lab © 2026 · el molde del Protocolo de Curación de Dominio.*
