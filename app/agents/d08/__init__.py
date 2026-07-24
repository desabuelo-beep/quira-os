"""
app/agents/d08/ — Pipeline de dominio · Participación Ciudadana (d08)
=====================================================================
Dylus Lab © 2026 · sexto dominio migrado al patrón de plataforma. El más rico
institucionalmente: familia CNO-VIII de 8 CNO jerárquicas (marco → Sistema →
Asamblea → Consejo → mecanismos) + 3 dimensiones (aporte de Javo, 15 años GAD):

    1. INTEGRIDAD NORMATIVA  (RO-VIII-001) → ¿existe/se instaló/documentó/aprobó?  [operable hoy]
    2. VITALIDAD DEMOCRÁTICA (RO-VIII-002) → ¿cuántos/qué diversidad? (LOPC 57)    [diseño · índice en Excel]
    3. EFECTIVIDAD/INCIDENCIA (RO-VIII-003) → ¿lo pedido se ejecutó?               [diseño · motor propio pendiente]

DISTINCIONES DOCTRINALES (Javo · 2026-07-23/24):
  · La Asamblea Ciudadana es ÓRGANO ciudadano autónomo (no mecanismo, no GAD):
    QUIRA verifica que el GAD la reconozca/articule (COOTAD 306), no su interior.
  · Frontera d08/d09: aportes de participación (actas de instancias) ≠ aportes de
    RDC/control social (H10c). NO se reusa enrich_aportes.py.
  · El IGP (indicador madre) se LEE, se deriva del dominio, y se RECONSTRUIRÁ en el
    Gold Master (fase 2) — hoy está mal compuesto (OBS-015: mezcla d09, IGP_PP=0).

PIPELINE:
    catalogo        → data/d08/catalogo_d08_v1.0.0.yaml (Nivel 4: evidencia clasificada)
    motor.leer_igp_diagnostico → LEE el IGP (diagnóstico, no canónico aún)
    motor.evaluar_integridad   → 1ª dimensión (determinístico)
    fuentes.*       → extracción de aportes de actas (Fase 4, IA · motor propio de d08)
    persistencia.*  → estructurar/guardar (anual)

Grafo: scripts/cypher/007_d08_participacion.cypher (pendiente).
"""
from . import catalogo, fuentes, motor, persistencia

__all__ = ["catalogo", "fuentes", "motor", "persistencia"]
