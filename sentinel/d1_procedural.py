"""
sentinel/d1_procedural.py
RC-D1.2 — Procedural Integrity (Integridad Procedimental)
Dylus Lab © 2026-05-20

FUNCIÓN:
  Verifica si una acción presupuestaria detectada respeta las ventanas temporales
  y los encadenamientos de aprobación establecidos por norma vault-verified.

  No evalúa si la acción fue "buena" — solo si fue procesada dentro del plazo
  correcto y por el canal correcto.

VENTANAS TEMPORALES VERIFICADAS:
  - Liquidación presupuestaria: antes del 31 de enero (COOTAD Art. 265)
  - Plan Anual de Contratación: publicado antes del 15 de enero (LOSNCP)
  - Clausura presupuestaria: 31 de diciembre (COOTAD Art. 263)
  - Presupuesto Participativo: primer semestre del año (COOTAD Art. 238)

DOCTRINA:
  D1.2 informa — no sanciona. Produce hipótesis de riesgo procedimental.
  "El sistema informa — la autoridad pública decide."

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ── VENTANAS TEMPORALES VAULT-VERIFIED ────────────────────────────────────────

_TIME_WINDOWS: Dict[str, Dict[str, Dict]] = {

    "GAD": {
        "liquidacion_presupuesto": {
            "deadline_month": 1,
            "deadline_day":   31,
            "description":    "Liquidación presupuestaria antes del 31 de enero",
            "norm":           "COOTAD Art. 265",
            "check_months":   [1, 2],   # Solo verificar en ene-feb (después es histórico)
            "sat_code":       "SAT-D1-B",
        },
        "contratacion_publica": {
            "deadline_month": 1,
            "deadline_day":   15,
            "description":    "PAC publicado antes del 15 de enero en portal SERCOP",
            "norm":           "LOSNCP Art. 22",
            "check_months":   [1, 2, 3],
            "sat_code":       "SAT-D1-C",
        },
        "presupuesto_participativo": {
            "deadline_month": 6,
            "deadline_day":   30,
            "description":    "PP concluido antes del 30 de junio (primer semestre)",
            "norm":           "COOTAD Art. 238",
            "check_months":   [5, 6, 7, 8],
            "sat_code":       "SAT-D1-C",
        },
        "reforma_presupuestaria": {
            "deadline_month": 10,
            "deadline_day":   31,
            "description":    "Reformas presupuestarias ordinarias antes del 31 de octubre",
            "norm":           "COPLAFIP Art. 97",
            "check_months":   [10, 11, 12],
            "sat_code":       "SAT-D1-A",
        },
    },

    "EMAI-EP": {
        "liquidacion_presupuesto": {
            "deadline_month": 1,
            "deadline_day":   31,
            "description":    "Liquidación EMAI-EP formulada antes del 31 de enero",
            "norm":           "COOTAD Art. 265",
            "check_months":   [1, 2],
            "sat_code":       "SAT-D1-B",
        },
        "contratacion_publica": {
            "deadline_month": 1,
            "deadline_day":   15,
            "description":    "PAC EMAI-EP publicado antes del 15 de enero",
            "norm":           "LOSNCP Art. 22",
            "check_months":   [1, 2, 3],
            "sat_code":       "SAT-D1-C",
        },
        "reforma_presupuestaria": {
            "deadline_month": 10,
            "deadline_day":   31,
            "description":    "Reforma EMAI-EP aprobada por Directorio antes del 31 de octubre",
            "norm":           "COOTAD Art. 267",
            "check_months":   [10, 11, 12],
            "sat_code":       "SAT-D1-A",
        },
    },

    "BOMBEROS": {
        "liquidacion_presupuesto": {
            "deadline_month": 1,
            "deadline_day":   31,
            "description":    "Liquidación Bomberos antes del 31 de enero",
            "norm":           "COOTAD Art. 265",
            "check_months":   [1, 2],
            "sat_code":       "SAT-D1-B",
        },
        "reforma_presupuestaria": {
            "deadline_month": 10,
            "deadline_day":   31,
            "description":    "Reforma Bomberos aprobada por Directorio antes del 31 de octubre",
            "norm":           "COOTAD Art. 267",
            "check_months":   [10, 11, 12],
            "sat_code":       "SAT-D1-A",
        },
    },

    "PATRONATO": {
        "liquidacion_presupuesto": {
            "deadline_month": 1,
            "deadline_day":   31,
            "description":    "Liquidación Patronato antes del 31 de enero",
            "norm":           "COOTAD Art. 265",
            "check_months":   [1, 2],
            "sat_code":       "SAT-D1-B",
        },
        "reforma_presupuestaria": {
            "deadline_month": 10,
            "deadline_day":   31,
            "description":    "Reforma Patronato aprobada por Directorio antes del 31 de octubre",
            "norm":           "COOTAD Art. 267",
            "check_months":   [10, 11, 12],
            "sat_code":       "SAT-D1-A",
        },
    },
}


# ── DATACLASS ─────────────────────────────────────────────────────────────────

@dataclass
class D1ProceduralResult:
    """
    Resultado de una verificación de ventana temporal RC-D1.2.

    is_overdue      — True si la ventana temporal ya venció y no hay confirmación
    is_active       — True si el mes actual está dentro del rango de verificación
    deadline_label  — descripción legible del plazo
    norm_ref        — artículo vault-verified aplicable
    sat_code        — código SAT si is_overdue (vacío si en plazo)
    narrative       — texto tension-aware (<200 chars)
    """
    entity_id:      str
    action_type:    str
    is_overdue:     bool
    is_active:      bool
    deadline_label: str
    norm_ref:       str
    sat_code:       str
    narrative:      str
    confidence:     float = 0.50


# ── MOTOR PROCEDIMENTAL ───────────────────────────────────────────────────────

def check_procedural(
    entity_id:      str,
    action_type:    str,
    current_month:  int,
    current_year:   int,
    has_cedula_data: bool = False,
) -> Optional[D1ProceduralResult]:
    """
    Verifica si la acción está dentro de su ventana temporal vault-verified.

    Retorna None si no hay ventana temporal para esta combinación entidad/acción.
    Solo activa verificación en los meses relevantes (check_months).

    Doctrina: solo informa la hipótesis — no sanciona.
    """
    entity_windows = _TIME_WINDOWS.get(entity_id, {})
    window = entity_windows.get(action_type)

    if not window:
        return None

    check_months = window.get("check_months", [])
    is_active    = current_month in check_months

    if not is_active:
        return None

    dl_month    = window["deadline_month"]
    dl_day      = window["deadline_day"]
    description = window["description"]
    norm        = window["norm"]
    sat         = window["sat_code"]

    # Determinar si el plazo ya venció en el contexto del mes actual
    # Para plazos de enero: si estamos en febrero → ya venció
    # Para plazos de octubre: si estamos en noviembre/dic → ya venció
    is_overdue = current_month > dl_month

    # Baja confianza si no hay cédula
    conf = 0.45 if has_cedula_data else 0.20

    narrative = _build_proc_narrative(
        entity_id, action_type, is_overdue, description, norm, dl_month, dl_day, conf
    )

    return D1ProceduralResult(
        entity_id      = entity_id,
        action_type    = action_type,
        is_overdue     = is_overdue,
        is_active      = True,
        deadline_label = description,
        norm_ref       = norm,
        sat_code       = sat if is_overdue else "",
        narrative      = narrative,
        confidence     = conf,
    )


def _build_proc_narrative(
    entity_id:   str,
    action_type: str,
    is_overdue:  bool,
    description: str,
    norm:        str,
    month:       int,
    day:         int,
    conf:        float,
) -> str:
    _MONTH_NAMES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
    }
    deadline = f"{day} de {_MONTH_NAMES.get(month, str(month))}"
    status   = "presenta indicadores de vencimiento de plazo" if is_overdue else "se encuentra dentro del plazo"
    return (
        f"[D1.2:{entity_id}] {action_type} — {status} ({description}; "
        f"plazo: {deadline} — {norm}; conf={conf:.0%})."
    )[:200]


# ── CONSULTA DIRECTA ──────────────────────────────────────────────────────────

def get_time_windows(entity_id: str) -> Dict[str, str]:
    """Devuelve las ventanas temporales registradas para una entidad."""
    windows = _TIME_WINDOWS.get(entity_id, {})
    return {
        action: w.get("description", "") + f" [{w.get('norm', '')}]"
        for action, w in windows.items()
    }


def list_entities_with_windows() -> List[str]:
    """Entidades con ventanas temporales registradas en RC-D1.2."""
    return list(_TIME_WINDOWS.keys())


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D1.2 Procedural Integrity — QUIRA OS")
    print("=" * 65)

    print("\n── Ventanas temporales registradas ──")
    for ent in list_entities_with_windows():
        print(f"\n  {ent}:")
        for action, desc in get_time_windows(ent).items():
            print(f"    {action}: {desc}")

    print("\n── Test: GAD liquidación — febrero (mes 2, fuera de plazo) ──")
    r1 = check_procedural("GAD", "liquidacion_presupuesto", current_month=2, current_year=2026, has_cedula_data=True)
    if r1:
        print(f"  is_overdue  : {r1.is_overdue}")
        print(f"  is_active   : {r1.is_active}")
        print(f"  SAT         : {r1.sat_code}")
        print(f"  Narrative   : {r1.narrative}")

    print("\n── Test: GAD PAC — enero (mes 1, en plazo) ──")
    r2 = check_procedural("GAD", "contratacion_publica", current_month=1, current_year=2026, has_cedula_data=True)
    if r2:
        print(f"  is_overdue  : {r2.is_overdue}")
        print(f"  is_active   : {r2.is_active}")
        print(f"  Narrative   : {r2.narrative}")
    else:
        print("  (fuera de rango de verificacion)")

    print("\n── Test: EMAI-EP reforma — mes 5 (fuera de rango) ──")
    r3 = check_procedural("EMAI-EP", "reforma_presupuestaria", current_month=5, current_year=2026)
    print(f"  Resultado: {r3}  (debe ser None — mes 5 fuera de check_months)")

    print("\n── Test: GAD PP — junio (en plazo) ──")
    r4 = check_procedural("GAD", "presupuesto_participativo", current_month=6, current_year=2026, has_cedula_data=True)
    if r4:
        print(f"  is_overdue  : {r4.is_overdue}  (debe ser False en junio)")
        print(f"  Narrative   : {r4.narrative}")
