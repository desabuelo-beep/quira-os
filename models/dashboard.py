"""
QUIRA OS — Model: Dashboard
Responsabilidad única: extraer y calcular los datos del tablero ejecutivo.
Sin Streamlit. Sin HTML. Solo números y estructuras.
Dylus Lab © 2026
"""
from __future__ import annotations
from dataclasses import dataclass, field
from data.loader import load_all


@dataclass(frozen=True)
class DashboardData:
    # ICGI-T principal
    score:       float
    color:       str
    avep_label:  str
    avep_emoji:  str
    color_rgb:   str

    # Inversión
    ppto_total:  float   # en pesos
    inv_ejec:    float
    ti_raw:      float
    ti_norm:     float
    proj:        float
    inv_m:       float   # millones
    ppto_m:      float

    # Histórico
    h2023: float
    h2024: float
    h2025: float
    h2026: float
    h2027: float

    # Gauge arc (SVG)
    arc:       float
    arc_score: float
    arc_meta:  float

    # Brechas
    isp_v: float
    ied_v: float
    psg_v: float

    # SAT
    sats: list = field(default_factory=list)


def _hex_to_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,183,0"


def load() -> DashboardData:
    """Carga y calcula todos los datos que necesita el Dashboard."""
    data    = load_all()
    icgit   = data["icgit"]
    indices = data["indices"]

    score  = icgit["score"]
    color  = icgit.get("color", "#FFB800")

    ppto  = icgit.get("presupuesto_total",   26_689_147)
    inv   = icgit.get("inversion_ejecutada",  7_820_000)
    ti_r  = icgit.get("ti_raw",  23.75)
    ti_n  = icgit.get("ti_norm", 70.0)
    proj  = icgit.get("proyeccion", 65.77)

    hist  = icgit.get("historico", {})

    arc       = 276.5   # π × r=88
    arc_score = arc * (1.0 - score / 100.0)
    arc_meta  = arc * (1.0 - 70.0  / 100.0)

    return DashboardData(
        score      = score,
        color      = color,
        avep_label = icgit.get("avep",       "Transición Crítica"),
        avep_emoji = icgit.get("avep_emoji", "🟠"),
        color_rgb  = _hex_to_rgb(color),
        ppto_total = ppto,
        inv_ejec   = inv,
        ti_raw     = ti_r,
        ti_norm    = ti_n,
        proj       = proj,
        inv_m      = inv  / 1_000_000,
        ppto_m     = ppto / 1_000_000,
        h2023      = hist.get("2023",      57.36),
        h2024      = hist.get("2024",      67.11),
        h2025      = hist.get("2025",      69.93),
        h2026      = hist.get("2026_q1",   53.56),
        h2027      = hist.get("2026_proj", 65.77),
        arc        = arc,
        arc_score  = arc_score,
        arc_meta   = arc_meta,
        isp_v      = indices.get("ISP", {}).get("valor") or 14.58,
        ied_v      = indices.get("IED", {}).get("valor") or 33.99,
        psg_v      = indices.get("PSG", {}).get("valor") or 12.83,
        sats       = data.get("sats", []),
    )
