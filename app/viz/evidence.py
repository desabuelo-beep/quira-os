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

# ── CAPA 0 · RELEVANCIA ONTOLÓGICA (Javo + asesor · 2026-07-10 · PCD-MN01 §22) ──
# Antes de verificar, QUIRA decide si la afirmación MERECE análisis. No elimina: CLASIFICA.
# Se analizan A/B/C (valor público verificable); la D (protocolaria) se archiva y se cuenta
# (transparencia metodológica: no se esconde, se explica por qué no entra). Expedientes = solo A.
RELEVANCIA = {
    "estrategica":    {"nivel": "A", "label": "Estratégica",    "sub": "obra · sistema · inversión",     "orden": 0, "analiza": True,  "seguimiento": False, "color": "#1E8E3E"},
    "programatica":   {"nivel": "B", "label": "Programática",   "sub": "gestión · servicio recurrente",  "orden": 1, "analiza": True,  "seguimiento": False, "color": "#1A73E8"},
    "administrativa": {"nivel": "C", "label": "Administrativa", "sub": "acto de gestión menor",          "orden": 2, "analiza": True,  "seguimiento": False, "color": "#6BA6C9"},
    "prospectiva":    {"nivel": "E", "label": "Prospectiva",    "sub": "compromiso a futuro · seguimiento", "orden": 3, "analiza": False, "seguimiento": True,  "color": "#8B7BD8"},
    "protocolaria":   {"nivel": "D", "label": "Protocolaria",   "sub": "sin contenido de gestión",       "orden": 4, "analiza": False, "seguimiento": False, "color": "#9AA0A6"},
}


def analiza_relevancia(rel: str) -> bool:
    """¿La afirmación entra al análisis de verificabilidad de HOY? (A/B/C sí · E/D no)."""
    return RELEVANCIA.get(rel, RELEVANCIA["estrategica"])["analiza"]


def es_seguimiento(rel: str) -> bool:
    """¿Es compromiso a futuro que se rastrea entre años (no verificable aún, no ruido)?"""
    return RELEVANCIA.get(rel, RELEVANCIA["estrategica"]).get("seguimiento", False)

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
    relevancia: str = "estrategica"   # Capa 0 · ontológica (A/B/C analiza · D archiva)
    eje: str = ""                     # tema (agua|vías|salud|…) para el corte longitudinal

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
