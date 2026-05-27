"""
QUIRA Intelligence — TOP: Trayectoria Operativa Proyectada
Motor Predictivo Institucional v1 · Dylus Lab © 2026

━━━ DOCTRINA (QUIRA_DOCTRINE_v1.3) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TOP NO es ejecución acumulada.
  TOP es coherencia temporal proyectada.
  El semáforo representa hacia dónde va la institución — no dónde está.

  QUIRA no mide el pasado. QUIRA vectoriza la trayectoria institucional.

━━━ FÓRMULA ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TOP = Ti_acumulado / W_Q

  Ti_acumulado: ejecución devengada acumulada al corte (%)
  W_Q: fracción histórica esperada del presupuesto anual a ese trimestre
       (curva estacional real del eSIGEF ecuatoriano)

  El resultado es la ejecución anual PROYECTADA si el ritmo actual se mantiene.

━━━ W_Q — PESOS ESTACIONALES HISTÓRICOS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Q1 (Ene-Mar): 0.13  ← letargo administrativo; liquidación año anterior,
                         reformas presupuestarias, carga de procesos a SERCOP.
                         Un GAD saludable devenga 12-15% de inversión en Q1.

  Q2 (Abr-Jun): 0.35  ← contratos activados, primera ola de obra pública.

  Q3 (Jul-Sep): 0.60  ← avance de obras, devengados parciales acumulados.

  Q4 (Oct-Dic): 1.00  ← explosión final; ~40% del presupuesto se devenga
                         en los últimos 45 días del año fiscal.

  Fuente: curva típica eSIGEF para GADs ecuatorianos de tamaño intermedio.
  Calibración Montecristi-específica: pendiente año 2 del Gold Master.
  En multiGAD: calibración por región, tipo de GAD y perfil histórico.

━━━ NOTA DOCTRINAL — CAP DE TOP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  TOP puede superar 100%. No significa "ejecutó más del 100%".
  Significa "ritmo superior al histórico esperado para este trimestre".

  REGLA DE DISPLAY: TOP > 100 → mostrar label narrativo, NO el número.
    "Sobre ritmo esperado"  →  cognitivamente correcto para el alcalde.
    "150%"                  →  políticamente confuso, numéricamente engañoso.

  El valor matemático interno siempre se preserva para QUIRA IA y cálculos.

━━━ UMBRALES CANONICOS (NOMENCLATURA_CANONICA.md Sección 7.2) ━━━━━━━━━━━━━━━

  TOP ≥ 75%  →  🟢  Sostenible         (Gobernanza por Mandato)
  TOP ≥ 55%  →  🟡  Atención           (Desaceleración leve)
  TOP ≥ 35%  →  🟠  Alerta Institucional (Intervención requerida)
  TOP <  35% →  🔴  Ruptura de Trayectoria (Riesgo Contraloría)

━━━ DISEÑO ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Funciones puras: deterministas, sin efectos secundarios.
  Sin imports de Streamlit. Sin estado global.
  Importable desde Vista Ejecutiva, QUIRA IA, tests y pipeline.
"""
from __future__ import annotations

# ── Constantes estacionales ───────────────────────────────────────────────────

WQ: dict[str, float] = {
    "Q1": 0.13,
    "Q2": 0.35,
    "Q3": 0.60,
    "Q4": 1.00,
}

# Mapeo de strings de corte canónico → quarter
_CORTE_A_QUARTER: dict[str, str] = {
    "Q1-2025": "Q1", "Q2-2025": "Q2", "Q3-2025": "Q3", "Q4-2025": "Q4",
    "Q1-2026": "Q1", "Q2-2026": "Q2", "Q3-2026": "Q3", "Q4-2026": "Q4",
    "Q1-2027": "Q1", "Q2-2027": "Q2", "Q3-2027": "Q3", "Q4-2027": "Q4",
}

# Clasificaciones en orden descendente (primera que aplica gana)
_CLASIFICACIONES: list[dict] = [
    {
        "min":              75.0,
        "categoria":        "sostenible",
        "label":            "Sostenible",
        "label_sobre_ritmo":"Sobre ritmo esperado",
        "color":            "#22C55E",
        "icono":            "🟢",
        "diagnostico": (
            "Trayectoria operativa coherente con el mandato fiscal. "
            "Garantiza cumplimiento del PDOT sin subejecución al cierre del año."
        ),
    },
    {
        "min":              55.0,
        "categoria":        "atencion",
        "label":            "Atención",
        "label_sobre_ritmo": None,
        "color":            "#F59E0B",
        "icono":            "🟡",
        "diagnostico": (
            "Desaceleración leve en trayectoria. Riesgo moderado de generar "
            "saldos de caja innecesarios al cierre fiscal. Monitorear Q siguiente."
        ),
    },
    {
        "min":              35.0,
        "categoria":        "alerta",
        "label":            "Alerta Institucional",
        "label_sobre_ritmo": None,
        "color":            "#F97316",
        "icono":            "🟠",
        "diagnostico": (
            "Desaceleración crítica. Requiere reforma presupuestaria de optimización "
            "inmediata o intervención directa en procesos de contratación pública."
        ),
    },
    {
        "min":              0.0,
        "categoria":        "ruptura",
        "label":            "Ruptura de Trayectoria",
        "label_sobre_ritmo": None,
        "color":            "#EF4444",
        "icono":            "🔴",
        "diagnostico": (
            "Parálisis operativa. Riesgo inminente de incumplimiento de metas del "
            "plan de trabajo y observaciones de Contraloría. Acción ejecutiva urgente."
        ),
    },
]


# ── Funciones públicas ────────────────────────────────────────────────────────

def quarter_desde_corte(corte: str) -> str:
    """
    Convierte un string de corte canónico al quarter activo.

    Args:
        corte: "Q1-2026", "Q2-2026", etc.

    Returns:
        "Q1" | "Q2" | "Q3" | "Q4"  (fallback: "Q1")
    """
    if corte in _CORTE_A_QUARTER:
        return _CORTE_A_QUARTER[corte]
    for q in ("Q1", "Q2", "Q3", "Q4"):
        if q in corte.upper():
            return q
    return "Q1"


def calcular_top(ti_acumulado: float, quarter: str) -> float:
    """
    Calcula la Trayectoria Operativa Proyectada.

    TOP = Ti_acumulado / W_Q

    Args:
        ti_acumulado: Ejecución devengada acumulada al corte (%, ej: 19.56)
        quarter:      Trimestre activo ("Q1" | "Q2" | "Q3" | "Q4")

    Returns:
        TOP proyectado (%). Puede superar 100 si el ritmo supera el histórico.

    Ejemplos (Q1-2026, W_Q1 = 0.13):
        calcular_top(19.56, "Q1") → 150.5   Patronato — sobre ritmo
        calcular_top(18.17, "Q1") → 139.8   EP Aseo   — sobre ritmo
        calcular_top( 1.05, "Q1") →   8.1   GAD inv.  — ruptura
    """
    wq = WQ.get(quarter, WQ["Q1"])
    if wq <= 0 or ti_acumulado < 0:
        return 0.0
    return round(ti_acumulado / wq, 1)


def calcular_top_desde_corte(ti_acumulado: float, corte: str) -> float:
    """
    Conveniencia: calcula TOP a partir del string de corte canónico.

    Args:
        ti_acumulado: Ejecución devengada acumulada al corte (%)
        corte:        String canónico ("Q1-2026", "Q2-2026", etc.)
    """
    return calcular_top(ti_acumulado, quarter_desde_corte(corte))


def clasificar_top(top: float) -> dict:
    """
    Clasifica un valor TOP y devuelve la ficha institucional completa.

    El resultado es consumido por Vista Ejecutiva (display) y QUIRA IA (narrativa).

    Returns dict con:
        top         (float)      — valor matemático interno (para IA y cálculos)
        categoria   (str)        — key doctrinal: sostenible|atencion|alerta|ruptura
        label       (str)        — etiqueta narrativa para UI
        color       (str)        — hex color semafórico
        icono       (str)        — indicador visual
        diagnostico (str)        — frase institucional para QUIRA IA
        top_display (str|None)   — string para UI (None si sobre ritmo con label)
        sobre_ritmo (bool)       — True si TOP > 100
    """
    sobre_ritmo = top > 100.0

    clasif = _CLASIFICACIONES[-1]  # default: ruptura
    for c in _CLASIFICACIONES:
        if top >= c["min"]:
            clasif = c
            break

    if sobre_ritmo and clasif.get("label_sobre_ritmo"):
        label_display = clasif["label_sobre_ritmo"]
        top_display   = None   # no mostrar el número — cognitivamente engañoso
    else:
        label_display = clasif["label"]
        top_display   = f"{min(top, 100.0):.0f}%"

    return {
        "top":         top,
        "categoria":   clasif["categoria"],
        "label":       label_display,
        "color":       clasif["color"],
        "icono":       clasif["icono"],
        "diagnostico": clasif["diagnostico"],
        "top_display": top_display,
        "sobre_ritmo": sobre_ritmo,
    }


def top_entidad(ti_pct: float, corte: str, nombre: str = "") -> dict:
    """
    Calcula + clasifica TOP para una entidad del Ecosistema Municipal.
    Retorna dict completo listo para renderizar en Vista Ejecutiva y QUIRA IA.

    Args:
        ti_pct:  Ti acumulado al corte (%)
        corte:   String canónico de corte ("Q1-2026")
        nombre:  Nombre de la entidad (para narrativa IA)

    Returns:
        Dict de clasificar_top() + {ti_pct, corte, quarter, entidad}
    """
    quarter = quarter_desde_corte(corte)
    top     = calcular_top(ti_pct, quarter)
    result  = clasificar_top(top)
    result.update({
        "ti_pct":  ti_pct,
        "corte":   corte,
        "quarter": quarter,
        "entidad": nombre,
    })
    return result


def narrativa_ia(entidad_dict: dict) -> str:
    """
    Genera un brief institucional ejecutivo para QUIRA IA.
    Lenguaje: autoritario, preciso, sin chatbot.

    Args:
        entidad_dict: resultado de top_entidad()

    Returns:
        String de brief institucional listo para mostrar en Zona 6 o QUIRA IA.
    """
    nombre  = entidad_dict.get("entidad", "La entidad")
    ti      = entidad_dict.get("ti_pct", 0.0)
    top     = entidad_dict.get("top", 0.0)
    cat     = entidad_dict.get("categoria", "ruptura")
    corte   = entidad_dict.get("corte", "Q1-2026")
    quarter = entidad_dict.get("quarter", "Q1")

    if cat == "sostenible":
        if entidad_dict.get("sobre_ritmo"):
            return (
                f"{nombre} mantiene trayectoria operativa sobre el ritmo histórico "
                f"esperado para {corte}. Ti acumulado {ti:.1f}% supera el promedio "
                f"del primer {quarter} en municipios ecuatorianos. "
                "No se observan riesgos inmediatos de ruptura de ejecución."
            )
        return (
            f"{nombre} mantiene trayectoria operativa sostenible para {corte}. "
            f"TOP proyectado {top:.0f}% garantiza cumplimiento del mandato fiscal "
            "sin riesgo de subejecución al cierre del año."
        )
    if cat == "atencion":
        return (
            f"{nombre} registra desaceleración leve en {corte}. "
            f"TOP proyectado {top:.0f}% — monitorear Q siguiente para evitar "
            "acumulación de saldos de caja innecesarios al cierre fiscal."
        )
    if cat == "alerta":
        return (
            f"{nombre} presenta alerta institucional en {corte}. "
            f"TOP proyectado {top:.0f}% requiere intervención en procesos "
            "de contratación pública o reforma presupuestaria de optimización."
        )
    # ruptura
    return (
        f"{nombre} registra ruptura de trayectoria en {corte}. "
        f"TOP proyectado {top:.1f}% — riesgo inminente de incumplimiento "
        "de metas del plan de trabajo. Se requiere acción ejecutiva urgente."
    )
