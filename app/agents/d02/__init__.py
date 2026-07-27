"""
app/agents/d02/ — Pipeline de dominio · Presupuesto & Financiamiento (d02)
=====================================================================
Dylus Lab © 2026 · tercer dominio migrado al patrón de plataforma
(tras d07, d01). Visión (Javo, PCD-D02): la salud financiera del
municipio COMO BASE para captar financiamiento internacional — no
"presupuesto interno".

DIFERENCIA CON d01/d07: casi TODO d02 ya vive resuelto en el Gold Master.
`motor.py` envuelve `scripts/enrich_presupuesto.py` (enricher real, ya en
producción, ya corrige el bug histórico del PCD: ISP leído de la columna
correcta). No se reimplementó nada — se conectó al patrón.

4 capacidades (todas LEÍDAS, Regla 1): Sostenibilidad (ISP 58.4%,
umbral COOTAD 65%) · Absorción (Ti 6.4%) · Movilización ($1.87M/4
convenios) · Elegibilidad (PND 83% / ICODS 87.5%, consumido de d01).

3 señales SAT (H22/H23/H24, LEÍDAS): solo "Alerta fiscal" tiene cadena
normativa verificada hoy — `CNO-IV-001` (auditoría 2026-07-23, mismo 65%
que la Disposición Transitoria COOTAD-2026). Las otras 2 (reforma tardía,
parálisis) siguen con norma pendiente — el propio enricher las dejó así
a propósito tras la auditoría del 2026-07-18 (cita errada, Regla 3).

PIPELINE:
    catalogo         → data/d02/catalogo_d02_v1.0.0.yaml
    fuentes.*        → única pieza IA real (Fase 4): verificar medición de resultados
    motor.leer_metricas → LEE las 4 capacidades + 3 señales (determinístico, funcional hoy)
    persistencia.*   → estructurar/guardar (determinístico)

Grafo: scripts/cypher/004_d02_presupuesto.cypher.
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [3, 9]
#   type: TECNICA
# ---
from . import catalogo, fuentes, motor, persistencia

__all__ = ["catalogo", "fuentes", "motor", "persistencia"]
