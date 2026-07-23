"""
app/agents/d07/ — Pipeline de dominio · Transparencia Activa (d07)
=====================================================================
Dylus Lab © 2026 · patrón de referencia para d01/d02/d03/d09 (mismo
esqueleto de 4 etapas; cada dominio aporta su propio catálogo + reglas
de scoring — NO se replica la lógica de negocio de d07, solo la forma).

PIPELINE (corregido 2026-07-22 tras objeción de Javo — la mayoría del
trabajo real de un DOM es IA, no determinístico; error de generalización
del director corregido):
    catalogo.cargar()                → fuente única (YAML)
    evidencia.*  → Portal Navigator + Evidence Collector + Evidence
                   Interpreter — TRES responsabilidades cognitivas reales
                   (Fase 4, IA — localizar, extraer, juzgar completitud/
                   simulación/vigencia)
    scoring.evaluar_cd/calcular_sita → Compliance Evaluator + SITA Engine
                   — únicas piezas determinísticas (Instructivo Tablas
                   0/1/2/5, aritmética fija sobre evidencia YA juzgada)
    reportes.redactar_observacion    → Report Generator — IA (narrativa
                   explicable, Regla de Oro 2)
    persistencia.*                   → estructurar/guardar — determinístico

Patrón para d01/d02/d03/d09 cuando les toque turno: cada DOM tendrá su
propia mezcla — en Planificación (SERCOP, PDOT, POA) y RDC (video/audio,
Motor Narrativo) la proporción de trabajo IA es aún mayor que en d07.
No se replica esta lista de módulos tal cual — se replica el PRINCIPIO
(separar lo que requiere juicio de lo que es aritmética fija una vez hay
evidencia limpia).

Neo4j (scripts/cypher/002_d07_transparencia.cypher) es un ÍNDICE DERIVADO
de este mismo catálogo, para navegación y consulta — nunca una segunda
fuente de verdad. Cambios de fondo nacen en el YAML, se regeneran hacia
Neo4j (Regla 9).
"""
from . import catalogo, evidencia, persistencia, reportes, scoring

__all__ = ["catalogo", "evidencia", "persistencia", "reportes", "scoring"]
