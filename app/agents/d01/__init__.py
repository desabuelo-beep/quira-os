"""
app/agents/d01/ — Pipeline de dominio · Planificación Estratégica (d01)
=====================================================================
Dylus Lab © 2026 · segundo dominio migrado al patrón de plataforma
(tras d07). Confirma que el molde es reutilizable: MISMA forma, distinta
sustancia.

DIFERENCIA CLAVE CON d07 (por eso el molde no se calca, se adapta):
  · d07 tuvo que RECONSTRUIR su métrica (el SITA no existía) → scoring.py
    era el corazón determinístico.
  · d01 YA tiene su métrica resuelta en el Gold Master (IPE, fórmula nativa
    H16b). Aquí motor.py solo la LEE (Regla 1/4). El corazón cognitivo se
    corre hacia articulacion.py (cruzar la cadena PDOT→POA→PAC).

PIPELINE:
    catalogo         → definición del dominio (cadena BRN CNO-I-001), YAML/grafo
    fuentes.*        → PDOT/POA/PAC/SERCOP/Budget Agents (Fase 4, IA — extraer)
    articulacion.*   → Alignment Agent (Fase 4, IA — cruzar RO-I-001/002)
    motor.leer_metricas → LEE IPE/cobertura del Gold Master (determinístico,
                       NO recalcula — implementado y funcional)
    persistencia.*   → estructurar/guardar (determinístico)

Grafo: scripts/cypher/003_d01_planificacion.cypher (cadena de 9 eslabones
jurídicos + 2 RO + fuentes + métricas marcadas INMUTABLE). La Fuente
'Presupuesto' está enlazada -MISMA_FUENTE_QUE-> CD-06 de d07: la cédula
presupuestaria se extrae UNA vez (en transparencia) y la consumen ambos
dominios.
"""
from . import articulacion, catalogo, fuentes, motor, persistencia

__all__ = ["articulacion", "catalogo", "fuentes", "motor", "persistencia"]
