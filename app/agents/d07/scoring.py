"""
app/agents/d07/scoring.py — Motor de reglas SITA (etapa 3 del pipeline)
=========================================================================
Responsabilidad única: aplicar CTA/ETA/RP/CI y agregar SITA.

100% DETERMINÍSTICO — CERO llamadas a IA. Reglas literales del Instructivo
INST-TA-2024 (ver METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP.md §4b). No es un
"Agente": es matemática fija sobre evidencia ya dada. Deliberadamente NO se
llama "AgenteSITA" — ese nombre insinuaría IA donde no la hay.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field

_TRES_ESTRELLAS = {"csv", "tsv", "xml", "json", "ods"}  # Instructivo Tabla 1


@dataclass
class EvidenciaCD:
    existe: bool
    formato_archivo: str | None
    campos_completos: bool
    fecha_dato: _dt.date | None
    fecha_registro: _dt.date | None
    enlaces_vivos: bool = True
    vigencia_ok: bool = True
    validez_ok: bool = True
    url: str | None = None
    sha256: str | None = None


@dataclass
class ScoreCD:
    cd_id: str
    cta: float
    eta: int
    rp: int
    ci: int
    observaciones: list[str] = field(default_factory=list)

    @property
    def sita(self) -> float:
        return round((self.cta + self.eta + self.rp + self.ci) / 4, 4)


def evaluar_cd(cd_id: str, ev: EvidenciaCD,
               fecha_monitoreo: _dt.date | None = None) -> ScoreCD:
    """Instructivo Tabla 0 (CTA) · Tabla 1 (ETA) · Tabla 2 (RP) · Tabla 5 (CI)."""
    fecha_monitoreo = fecha_monitoreo or _dt.date.today()
    obs: list[str] = []

    if not ev.existe:
        obs.append("Sin información: el conjunto no está publicado en el portal.")
        return ScoreCD(cd_id, 0.0, 0, 0, 0, obs)

    mes_anterior = fecha_monitoreo.replace(day=1) - _dt.timedelta(days=1)
    actualizada = bool(ev.fecha_dato and ev.fecha_dato.year == mes_anterior.year
                       and ev.fecha_dato.month == mes_anterior.month)
    if ev.campos_completos and actualizada:
        cta = 1.0
    else:
        cta = 0.5
        if not ev.campos_completos:
            obs.append("Integridad parcial: hay campos obligatorios vacíos.")
        if not actualizada:
            obs.append("Desactualizada: la fecha del dato no es del mes anterior.")

    fmt = (ev.formato_archivo or "").lower().lstrip(".")
    eta = 1 if fmt in _TRES_ESTRELLAS else 0
    if not eta:
        obs.append(f"Datos no abiertos (formato '{fmt or '—'}' < 3★ requeridas).")

    rp = 1 if (ev.fecha_registro and ev.fecha_registro.day <= 15) else 0
    if not rp:
        obs.append("Registro fuera del plazo (posterior al día 15).")

    ci = 1 if (ev.enlaces_vivos and ev.vigencia_ok and ev.validez_ok) else 0
    if not ci:
        obs.append("Calidad: enlace roto, fuera de vigencia o valores incoherentes.")

    return ScoreCD(cd_id, cta, eta, rp, ci, obs)


def calcular_sita(scores: list[ScoreCD]) -> dict[str, float]:
    """SITA institucional = promedio de cada parámetro / 4 (Instructivo §Subíndice)."""
    if not scores:
        return {"CTA": 0.0, "ETA": 0.0, "RP": 0.0, "CI": 0.0, "SITA": 0.0}
    n = len(scores)
    cta = sum(s.cta for s in scores) / n
    eta = sum(s.eta for s in scores) / n
    rp = sum(s.rp for s in scores) / n
    ci = sum(s.ci for s in scores) / n
    return {"CTA": round(cta, 4), "ETA": round(eta, 4), "RP": round(rp, 4),
            "CI": round(ci, 4), "SITA": round((cta + eta + rp + ci) / 4, 4)}
