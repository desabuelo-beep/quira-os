"""
app/agents/d03/ — Pipeline de dominio · Gobernanza del Mandato (d03)
=====================================================================
Dylus Lab © 2026 · cuarto dominio migrado al patrón de plataforma
(tras d07, d01, d02). Visión (PCD-D03): la palabra empeñada — qué
proporción de lo prometido ante el CNE se convirtió en meta del plan.

Fase 2 (auditoría, colega 2026-07-23) sin hallazgos nuevos: se buscó el
mismo patrón de bug de d02 (doble-conversión /100) en H03/H16 — 0
coincidencias. Guardián ICPI intacto, centinela H85!D21 = "✅ CORRECTO",
Clasificación_IFE ya es fórmula viva (no texto estampado, corregido en
el PCD original).

DOS MÉTRICAS (no una): Incorporación (HECHO documental, se cuenta) vs
Calidad/IFE (ÍNDICE del motor, se lee) — nunca se confunden entre sí
(fue precisamente la confusión que motivó la curación del canon
original). `motor.py` envuelve `scripts/enrich_mandato.py` (enricher
real, ya en producción, ya corrige el bug histórico del rótulo).

PIPELINE:
    catalogo         → data/d03/catalogo_d03_v1.0.0.yaml
    fuentes.*        → única pieza IA real (Fase 4): contraste documental CNE
    motor.leer_metricas → LEE incorporación+calidad+centinela (determinístico, funcional hoy)
    persistencia.*   → estructurar/guardar (determinístico, evaluación ANUAL no mensual)

Grafo: scripts/cypher/005_d03_gobernanza.cypher.
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [3, 9]
#   type: TECNICA
# ---
from . import catalogo, fuentes, motor, persistencia

__all__ = ["catalogo", "fuentes", "motor", "persistencia"]
