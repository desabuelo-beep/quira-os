"""
app/agents/d07/evidencia.py — Etapas agénticas del pipeline d07
=========================================================================
Corrección (Javo + colega, 2026-07-22): esto NO es "una etapa de IA".
Son TRES responsabilidades cognitivas distintas, cada una con juicio real:

    1. Portal Navigator   — localizar la página/URL correcta del CD en el
                             portal (estructura cambia por GAD).
    2. Evidence Collector — descargar/leer el archivo real (PDF/CSV/HTML,
                             a veces escaneado, a veces enlace roto).
    3. Evidence Interpreter — juzgar lo recolectado: ¿está completo?
                             ¿es simulación o cumplimiento real? ¿el enlace
                             funciona? ¿hay inconsistencias internas?
                             (Instructivo Tabla 5 — vigencia/validez).

Solo el RESULTADO de las tres (el `EvidenciaCD` ya poblado) es determinístico
de ahí en adelante — eso lo consume `scoring.py`. Las tres siguen en un solo
módulo por ahora (no 3 archivos) porque ninguna tiene implementación real
todavía: separar en archivos vacíos no añade nada hasta que haya presupuesto
para ejecutarlas (Fase 4).
"""
from __future__ import annotations

from .scoring import EvidenciaCD


def levantar_evidencia_portal(cd_id: str, municipio: str, anio: int, mes: int) -> EvidenciaCD:
    raise NotImplementedError(
        "Fase 4 (Navigator + Collector + Interpreter) — en pausa por presupuesto de API. "
        "El scoring (scoring.evaluar_cd/calcular_sita) ya funciona con evidencia dada a mano."
    )
