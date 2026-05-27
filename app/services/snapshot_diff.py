"""
app/services/snapshot_diff.py — QUIRA OS · Sprint 3 P2
Snapshot Diff Engine: detecta deterioro, mejora, reincidencia y ruptura
entre dos snapshots consecutivos.

Clasificaciones canónicas:
  MEJORA        — ICPI aumentó ≥ 1pp respecto al período anterior
  DETERIORO     — ICPI cayó ≥ 1pp respecto al período anterior
  ESTABLE       — variación < 1pp
  RUPTURA       — caída > 10pp en un solo período (señal de crisis)
  RECUPERACION  — ICPI supera 65% habiendo estado < 60% en período anterior
  REINCIDENCIA  — D3 Ti < 60% por ≥ 3 períodos consecutivos (→ SAT-III)

Doctrina: RC-M convierte observaciones puntuales en trayectoria institucional.
La reincidencia distingue ineficiencia puntual de patrón estructural crónico.

Fuente canónica: docs/SPRINT3.md · NORTH.md · Gold Master TGI v6.0 G5.3_SAT_LONGITUDINAL
Dylus Lab © 2026
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ── Umbrales doctrinales ───────────────────────────────────────────────────────
_UMBRAL_MEJORA      =  1.0   # pp mínimos para clasificar como MEJORA
_UMBRAL_RUPTURA     = 10.0   # pp de caída para clasificar como RUPTURA
_UMBRAL_RECUPERACION = 65.0  # % ICPI para considerar recuperación
_UMBRAL_CRISIS_ICPI  = 60.0  # % ICPI que activa riesgo de reincidencia
_UMBRAL_D3_SAT_III   = 60.0  # % D3 Ti que activa SAT-III si persiste
_PERIODOS_REINCIDENCIA = 3   # períodos consecutivos para SAT-III REINCIDENTE


# ══════════════════════════════════════════════════════════════════════════════
# Dataclasses de resultado
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class FieldDiff:
    """Diferencia de un campo entre dos snapshots."""
    campo:     str
    valor_a:   Any
    valor_b:   Any
    delta:     float | None   # valor_b - valor_a (solo si numérico)
    direccion: str            # "MEJORA" | "DETERIORO" | "ESTABLE" | "SIN_DATOS"


@dataclass
class DiffResult:
    """Resultado del análisis de diferencia entre dos snapshots.

    Attributes:
        clasificacion:      Clasificación canónica del período.
        icpi_delta_pp:      Cambio en ICPI en puntos porcentuales (positivo = mejora).
        d3_ti_delta_pp:     Cambio en D3 Ti en puntos porcentuales.
        campos_cambiados:   Lista de FieldDiff con todos los campos que cambiaron.
        alertas_nuevas:     Códigos SAT que se activaron en snap_b pero no en snap_a.
        alertas_mitigadas:  Códigos SAT que estaban activos en snap_a y no en snap_b.
        sat_iii_reincidente:True si D3 Ti < 60% por ≥ 3 períodos consecutivos.
        riesgo_a:           Clasificación de riesgo del período anterior.
        riesgo_b:           Clasificación de riesgo del período actual.
        periodo_a:          Identificador del período anterior (fecha_corte).
        periodo_b:          Identificador del período actual (fecha_corte).
        notas:              Lista de notas doctrinales generadas.
    """
    clasificacion:      str
    icpi_delta_pp:      float | None
    d3_ti_delta_pp:     float | None
    campos_cambiados:   list[FieldDiff]  = field(default_factory=list)
    alertas_nuevas:     list[str]        = field(default_factory=list)
    alertas_mitigadas:  list[str]        = field(default_factory=list)
    sat_iii_reincidente: bool            = False
    riesgo_a:           str | None       = None
    riesgo_b:           str | None       = None
    periodo_a:          str | None       = None
    periodo_b:          str | None       = None
    notas:              list[str]        = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

def _get(snap: dict, path: str, default=None) -> Any:
    """Acceso seguro a campo anidado por notación de punto.

    Ejemplo: _get(snap, "icpi.score") → snap["icpi"]["score"]
    """
    keys = path.split(".")
    cur  = snap
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k, default)
        if cur is None:
            return default
    return cur


def _pct(ratio: float | None) -> float | None:
    """Convierte ratio (0-1) a porcentaje (0-100). None → None."""
    if ratio is None:
        return None
    # Si ya viene como porcentaje (> 1.5), no convertir
    if abs(ratio) > 1.5:
        return float(ratio)
    return float(ratio) * 100.0


def _sat_activas(snap: dict) -> set[str]:
    """Extrae códigos SAT activas de un snapshot."""
    activas: set[str] = set()

    # Fuente 1: sat.activas (lista de strings o dicts)
    sat_list = _get(snap, "sat.activas", [])
    if isinstance(sat_list, list):
        for item in sat_list:
            if isinstance(item, str):
                activas.add(item.strip().upper())
            elif isinstance(item, dict):
                code = item.get("codigo") or item.get("code") or item.get("sat")
                if code:
                    activas.add(str(code).strip().upper())

    # Fuente 2: sat.alertas (estructura alternativa)
    alertas = _get(snap, "sat.alertas", [])
    if isinstance(alertas, list):
        for item in alertas:
            if isinstance(item, dict):
                code = item.get("codigo") or item.get("sat_codigo")
                estado = str(item.get("estado", "")).upper()
                if code and estado == "ACTIVA":
                    activas.add(str(code).strip().upper())

    return activas


def _field_diff(campo: str, val_a: Any, val_b: Any) -> FieldDiff | None:
    """Crea FieldDiff si el valor cambió."""
    if val_a == val_b:
        return None

    delta     = None
    direccion = "SIN_DATOS"

    if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
        delta = float(val_b) - float(val_a)
        if abs(delta) < 0.001:
            return None  # cambio insignificante
        direccion = "MEJORA" if delta > 0 else "DETERIORO"
    elif val_a is None and val_b is not None:
        direccion = "NUEVO"
    elif val_a is not None and val_b is None:
        direccion = "PERDIDO"
    else:
        direccion = "CAMBIADO"

    return FieldDiff(
        campo=campo,
        valor_a=val_a,
        valor_b=val_b,
        delta=delta,
        direccion=direccion,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Motor principal
# ══════════════════════════════════════════════════════════════════════════════

def compare_snapshots(
    snap_a: dict,
    snap_b: dict,
    historial_d3: list[float] | None = None,
) -> DiffResult:
    """Compara dos snapshots y produce un DiffResult canónico.

    Args:
        snap_a:       Snapshot anterior (período N-1).
        snap_b:       Snapshot actual  (período N).
        historial_d3: Lista de valores D3 Ti (%) de períodos previos,
                      en orden cronológico, para detectar SAT-III reincidente.
                      Si None, se evalúa solo con los dos snapshots disponibles.

    Returns:
        DiffResult con clasificación, deltas, alertas y notas doctrinales.
    """
    # ── 1. Extraer métricas clave ──────────────────────────────────────────
    icpi_a = _pct(_get(snap_a, "icpi.score"))
    icpi_b = _pct(_get(snap_b, "icpi.score"))

    d3_a = _pct(_get(snap_a, "tgi.dimensiones.d3"))
    d3_b = _pct(_get(snap_b, "tgi.dimensiones.d3"))

    periodo_a = _get(snap_a, "_meta.fecha_corte") or _get(snap_a, "fecha_corte")
    periodo_b = _get(snap_b, "_meta.fecha_corte") or _get(snap_b, "fecha_corte")

    riesgo_a = _get(snap_a, "sat.riesgo_ponderado") or _get(snap_a, "sat.clasif_riesgo")
    riesgo_b = _get(snap_b, "sat.riesgo_ponderado") or _get(snap_b, "sat.clasif_riesgo")

    # ── 2. Calcular deltas ─────────────────────────────────────────────────
    icpi_delta = None
    if icpi_a is not None and icpi_b is not None:
        icpi_delta = round(icpi_b - icpi_a, 4)

    d3_delta = None
    if d3_a is not None and d3_b is not None:
        d3_delta = round(d3_b - d3_a, 4)

    # ── 3. Clasificación canónica ──────────────────────────────────────────
    clasificacion = _clasificar(icpi_a, icpi_b, icpi_delta)

    # ── 4. Alertas nuevas / mitigadas ─────────────────────────────────────
    sats_a = _sat_activas(snap_a)
    sats_b = _sat_activas(snap_b)
    alertas_nuevas    = sorted(sats_b - sats_a)
    alertas_mitigadas = sorted(sats_a - sats_b)

    # ── 5. SAT-III Reincidencia ────────────────────────────────────────────
    sat_iii = _detectar_sat_iii(d3_a, d3_b, historial_d3)

    # ── 6. Campos cambiados ────────────────────────────────────────────────
    campos = _diff_campos(snap_a, snap_b)

    # ── 7. Notas doctrinales ───────────────────────────────────────────────
    notas = _generar_notas(
        clasificacion, icpi_delta, d3_b, icpi_b, sat_iii,
        alertas_nuevas, alertas_mitigadas,
    )

    logger.info(
        f"[DiffEngine] {periodo_a} → {periodo_b} | "
        f"ICPI: {icpi_a}% → {icpi_b}% (Δ{icpi_delta:+.2f}pp) | "
        f"D3: {d3_a}% → {d3_b}% | "
        f"Clasificacion: {clasificacion} | "
        f"SAT-III: {sat_iii}"
        if icpi_delta is not None else
        f"[DiffEngine] {periodo_a} → {periodo_b} | Sin delta ICPI (datos insuficientes)"
    )

    return DiffResult(
        clasificacion=clasificacion,
        icpi_delta_pp=icpi_delta,
        d3_ti_delta_pp=d3_delta,
        campos_cambiados=campos,
        alertas_nuevas=alertas_nuevas,
        alertas_mitigadas=alertas_mitigadas,
        sat_iii_reincidente=sat_iii,
        riesgo_a=str(riesgo_a) if riesgo_a else None,
        riesgo_b=str(riesgo_b) if riesgo_b else None,
        periodo_a=str(periodo_a) if periodo_a else None,
        periodo_b=str(periodo_b) if periodo_b else None,
        notas=notas,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Funciones auxiliares
# ══════════════════════════════════════════════════════════════════════════════

def _clasificar(
    icpi_a: float | None,
    icpi_b: float | None,
    delta:  float | None,
) -> str:
    """Determina la clasificación canónica del período."""
    if delta is None:
        return "INSUFICIENTE_DATOS"

    # RUPTURA: caída brusca en un solo período
    if delta <= -_UMBRAL_RUPTURA:
        return "RUPTURA"

    # RECUPERACION: estaba en crisis, ahora supera umbral
    if (icpi_a is not None and icpi_a < _UMBRAL_CRISIS_ICPI
            and icpi_b is not None and icpi_b >= _UMBRAL_RECUPERACION):
        return "RECUPERACION"

    # MEJORA / DETERIORO / ESTABLE
    if delta >= _UMBRAL_MEJORA:
        return "MEJORA"
    if delta <= -_UMBRAL_MEJORA:
        return "DETERIORO"
    return "ESTABLE"


def _detectar_sat_iii(
    d3_a: float | None,
    d3_b: float | None,
    historial_d3: list[float] | None,
) -> bool:
    """Detecta SAT-III REINCIDENTE.

    Regla: D3 Ti < 60% por ≥ 3 períodos consecutivos.
    Si historial_d3 no está disponible, evalúa solo snap_a y snap_b.
    """
    umbral = _UMBRAL_D3_SAT_III

    # Con historial completo
    if historial_d3 is not None:
        todos = list(historial_d3)
        if d3_b is not None:
            todos.append(d3_b)
        if len(todos) < _PERIODOS_REINCIDENCIA:
            return False
        # Verificar los últimos N períodos consecutivos
        ultimos = todos[-_PERIODOS_REINCIDENCIA:]
        return all(
            v is not None and v < umbral
            for v in ultimos
        )

    # Sin historial — evaluación limitada con 2 snapshots
    if d3_a is not None and d3_b is not None:
        # Solo podemos detectar 2 períodos; no alcanza para SAT-III
        # pero anotamos el riesgo
        return False

    return False


def _diff_campos(snap_a: dict, snap_b: dict) -> list[FieldDiff]:
    """Genera lista de FieldDiff para campos clave."""
    campos_a_revisar = [
        ("icpi.score",               "ICPI Global (ratio)"),
        ("tgi.score",                "TGI Score cantonal"),
        ("tgi.dimensiones.d1",       "D1 Legalidad"),
        ("tgi.dimensiones.d2",       "D2 Planificacion"),
        ("tgi.dimensiones.d3",       "D3 Ejecucion Ti"),
        ("tgi.dimensiones.d4",       "D4 Equidad"),
        ("tgi.dimensiones.d5",       "D5 Capacidad"),
        ("sat.riesgo_ponderado",     "SAT Riesgo"),
        ("sat.total_activas",        "SAT Total Activas"),
        ("financiero.ejecucion_pct", "Ejecucion Presupuestaria (%)"),
    ]

    diffs = []
    for path, _ in campos_a_revisar:
        val_a = _get(snap_a, path)
        val_b = _get(snap_b, path)
        diff = _field_diff(path, val_a, val_b)
        if diff:
            diffs.append(diff)

    return diffs


def _generar_notas(
    clasificacion: str,
    icpi_delta: float | None,
    d3_b: float | None,
    icpi_b: float | None,
    sat_iii: bool,
    alertas_nuevas: list[str],
    alertas_mitigadas: list[str],
) -> list[str]:
    """Genera notas doctrinales contextuales."""
    notas = []

    if clasificacion == "RUPTURA":
        notas.append(
            f"RUPTURA INSTITUCIONAL: ICPI cayo {abs(icpi_delta or 0):.1f}pp en un solo periodo. "
            "Requiere analisis inmediato de causas. Protocolo SAT-VI."
        )
    elif clasificacion == "RECUPERACION":
        notas.append(
            "RECUPERACION: ICPI supero el umbral 65% luego de haber estado en zona critica. "
            "Seguimiento estricto para confirmar sostenibilidad."
        )
    elif clasificacion == "MEJORA":
        notas.append(
            f"MEJORA: ICPI aumento {icpi_delta or 0:.1f}pp. "
            "Confirmar con proximo periodo para descartar variacion puntual."
        )
    elif clasificacion == "DETERIORO":
        notas.append(
            f"DETERIORO: ICPI bajo {abs(icpi_delta or 0):.1f}pp. "
            "Identificar dimension responsable y activar protocolo correctivo."
        )

    if sat_iii:
        notas.append(
            "SAT-III REINCIDENTE: D3 Ti < 60% por 3 periodos consecutivos. "
            "Base legal: COPFP Art. 113. Requiere intervencion estructural, "
            "no solo operativa."
        )

    if d3_b is not None and d3_b < 40.0:
        notas.append(
            f"D3 Ti = {d3_b:.1f}% — zona critica severa (< 40%). "
            "Riesgo de devolucion de recursos y perdida de elegibilidad a fondos externos."
        )

    if alertas_nuevas:
        notas.append(f"Alertas SAT nuevas en este periodo: {', '.join(alertas_nuevas)}")

    if alertas_mitigadas:
        notas.append(f"Alertas SAT mitigadas en este periodo: {', '.join(alertas_mitigadas)}")

    if icpi_b is not None and icpi_b < 50.0:
        notas.append(
            f"ICPI = {icpi_b:.1f}% < 50%: nivel 'Ruptura Sistémica'. "
            "Riesgo de intervención por órganos de control (Contraloría, CPCCS)."
        )

    return notas


# ══════════════════════════════════════════════════════════════════════════════
# API de alto nivel — detección de reincidencia longitudinal
# ══════════════════════════════════════════════════════════════════════════════

def detect_reincidence_from_history(
    snapshots: list[dict],
) -> dict:
    """Analiza una lista de snapshots y detecta reincidencia D3.

    Args:
        snapshots: Lista ordenada cronológicamente de snapshots.

    Returns:
        dict con:
            sat_iii_activa:    bool — SAT-III reincidente activa
            periodos_d3_bajo:  int  — períodos consecutivos con D3 < 60%
            valores_d3:        list[float] — historial D3 Ti (%)
            clasificacion_seq: list[str]  — clasificación de cada período
    """
    if not snapshots:
        return {
            "sat_iii_activa": False,
            "periodos_d3_bajo": 0,
            "valores_d3": [],
            "clasificacion_seq": [],
        }

    valores_d3: list[float | None] = []
    for snap in snapshots:
        d3 = _pct(_get(snap, "tgi.dimensiones.d3"))
        valores_d3.append(d3)

    # Contar rachas consecutivas al final
    consecutivos = 0
    for v in reversed(valores_d3):
        if v is not None and v < _UMBRAL_D3_SAT_III:
            consecutivos += 1
        else:
            break

    sat_iii = consecutivos >= _PERIODOS_REINCIDENCIA

    # Clasificaciones par a par
    clasif_seq = []
    for i in range(1, len(snapshots)):
        diff = compare_snapshots(snapshots[i - 1], snapshots[i])
        clasif_seq.append(diff.clasificacion)

    return {
        "sat_iii_activa": sat_iii,
        "periodos_d3_bajo": consecutivos,
        "valores_d3": [v for v in valores_d3 if v is not None],
        "clasificacion_seq": clasif_seq,
    }
