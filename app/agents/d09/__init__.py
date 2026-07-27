"""
app/agents/d09/ — Pipeline de dominio · Rendición de Cuentas (d09)
=====================================================================
Dylus Lab © 2026 · quinto y último dominio BRN-conforme migrado al patrón
de plataforma (tras d07, d01, d02, d03). Visión (PCD-D09): triangulación
discurso oficial ↔ evidencia física/financiera ↔ informe CPCCS.

Fase 2 (auditoría, 2026-07-23) sin hallazgos nuevos: se buscó el mismo
patrón de bug de d02 (doble-conversión /100) en las 7 hojas de d09
(H24_SAT-IV, H24b_SAT-V, H24c_SAT-VI, H31, H34, H34b, H10c) — 0
coincidencias. Guardián ICPI intacto. Se corrigió una inconsistencia de
higiene documental en RO-IX-001.yaml (comentario "propuesta" desactualizado
tras la aprobación real de 2026-07-20).

DOMINIO MÁS HETEROGÉNEO MIGRADO: 1 ÍNDICE (fidelidad narrativa, evaluación
experta trazable, no cómputo automático) + 4 HECHOS documentales (brecha
CPCCS, serie 3 años, cumplimiento actual, trazabilidad de aportes
ciudadanos) — y DOS fuentes distintas: Excel en vivo (fidelidad/cpccs) vs
snapshot persistido desde DOCX/embeddings (serie/cumplimiento/aportes,
PCD-D09 lo documenta como aceptable así hoy).

BUG ENCONTRADO Y CORREGIDO (Fase 1, `scripts/enrich_rdc.py`): la Fase 1 de
descubrimiento inicial no detectó `scripts/enrich_aportes.py` (nombre no
calzaba con el patrón de búsqueda) — al ejecutar solo enrich_rdc.py+
enrich_rdc_docx.py para la evidencia reproducible, se descubrió que
enrich_rdc.py sobrescribía TODO `rendicion` en vez de fusionar, borrando
`aportes` (96 aportes ciudadanos cruzados con POA). Corregido a merge;
`aportes_ciudadanos` incorporado como 4º hecho del catálogo. Ver OBS-014.

`aportes_ciudadanos` se cataloga con su estado real de gobernanza:
OPERACIONAL desde 2026-07-03/04, pero su metodología formal
(`METODOLOGIA_TRAZABILIDAD_APORTES.md`) sigue v0.3 PENDIENTE DE AVAL de
Javo — no se presenta con el mismo peso que RO-IX-001 (ya ratificada).

PIPELINE:
    catalogo         → data/d09/catalogo_d09_v1.0.0.yaml
    fuentes.*        → única pieza IA real (Fase 4): contenido mínimo + NLP video 2025
    motor.leer_metricas → LEE fidelidad+cpccs (vivo) + serie+cumplimiento+aportes (persistido)
    persistencia.*   → estructurar/guardar (determinístico, evaluación ANUAL no mensual)

Grafo: scripts/cypher/006_d09_rendicion.cypher.
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [3, 9]
#   type: TECNICA
# ---
from . import catalogo, fuentes, motor, persistencia

__all__ = ["catalogo", "fuentes", "motor", "persistencia"]
