# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico de QUIRA — el OBJETO CANÓNICO.
Dylus Lab © 2026 · doctrina: docs/architecture/SISTEMA_VISUALIZACION_CANONICO.md.

TODOS los renderers (matplotlib/svg/plotly) consumen `NarrativeEvidence`, NUNCA el motor.
canon → datos → presentación (Regla 1). El motor no sabe que existe Matplotlib.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

# ── GRAMÁTICA DE COLOR · eje de EVIDENCIA (distinto del semáforo de cumplimiento del Excel) ──
# Decisión del director (2026-07-08): escala nueva porque mide otro eje (verificabilidad,
# no cumplimiento). El gris = ausencia, NO "malo" (principio rector · no acusatorio).
GRAMATICA = {
    "independiente":         {"color": "#1E8E3E", "nombre": "verde", "label": "Verificado"},
    "institucional":         {"color": "#1A73E8", "nombre": "azul",  "label": "Declarado institucionalmente"},
    "parcial":               {"color": "#F9AB00", "nombre": "ámbar", "label": "Evidencia parcial"},
    "sin_evidencia_publica": {"color": "#9AA0A6", "nombre": "gris",  "label": "Sin evidencia pública"},
    "contradiccion":         {"color": "#D93025", "nombre": "rojo",  "label": "Contradicción documental"},
}
_GRIS = GRAMATICA["sin_evidencia_publica"]

# ── veredicto del motor (clase) → (estado legible · fuente · tipo Familia A) ──
_CLASE = {
    "coherente":             ("Verificado",            "POA (planificación)",   "gestión"),
    "en_contratacion":       ("En contratación",       "PAC / SERCOP",          "gestión"),
    "verif_ejecucion":       ("Ejecución verificada",  "Cédula presupuestaria", "gestión"),
    "verif_cobertura":       ("Cobertura verificada",  "Literal D (patronato)", "gestión"),
    "discrepa_ejecucion":    ("Contradicción",         "Cédula presupuestaria", "gestión"),
    "sin_evidencia_publica": ("Sin evidencia pública", "",                      "gestión"),
    "sin_correlato":         ("Sin correlato",         "",                      "gestión"),
    "proceso":               ("Proceso de rendición",  "",                      "proceso"),
}


@dataclass
class NarrativeEvidence:
    """Un renglón = una afirmación de la autoridad, con su nivel de verificabilidad pública.
    Este es el Modelo de Datos Canónico que consume toda la capa de visualización."""
    id: str
    afirmacion: str
    estado: str
    nivel_evidencia: str
    fuente: str = ""
    regla: str = ""
    explicacion: str = ""
    periodo: str = ""
    entidad: str = "GAD Montecristi"
    tipo: str = "gestión"
    confianza: float = 0.0

    @property
    def color(self) -> str:
        return GRAMATICA.get(self.nivel_evidencia, _GRIS)["color"]

    @property
    def etiqueta(self) -> str:
        return GRAMATICA.get(self.nivel_evidencia, _GRIS)["label"]

    def as_dict(self) -> dict:
        d = asdict(self)
        d["color"], d["etiqueta"] = self.color, self.etiqueta
        return d


def estado_fuente_tipo(clase: str) -> tuple[str, str, str]:
    """Deriva (estado legible, fuente, tipo) del veredicto del motor. En gobernanza."""
    return _CLASE.get(clase, ("Sin correlato", "", "gestión"))
