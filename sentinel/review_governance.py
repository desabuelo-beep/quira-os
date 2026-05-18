"""
SENTINEL RAG · review_governance.py
Sprint 2.2 — Review Governance Layer.

Resuelve conflictos entre analistas que evalúan distinto la misma recomendación.
Mide Trust Drift semanal para detectar degradación de alineación institucional.

Modelo de revisión:
  NIVEL 1  →  Analista       (revisión inicial)
  NIVEL 2  →  Coordinador    (escalación por disputa)
  NIVEL 3  →  Institucional  (cierre definitivo)

Estados de caso:
  PENDIENTE   →  revisión recibida, sin conflicto detectado
  EN_DISPUTA  →  dos o más revisiones con estados incompatibles
  ESCALADO    →  promovido a Coordinador / Institucional
  CERRADO     →  resolución definitiva emitida

Trust Drift: % semanal APROBAR / OBSERVAR / RECHAZAR.
Si RECHAZAR ≥ 15% en cualquier semana → ALERTA_DRIFT.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import time
import hashlib
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from typing import Optional
from collections import defaultdict

from sentinel.rag_config import LOGS_DIR, SENTINEL_VERSION

# ── RUTAS ─────────────────────────────────────────────────────────────────────
CASES_LOG      = LOGS_DIR / "governance_cases.jsonl"
CASES_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
TRUST_DRIFT_RECHAZO_ALERT  = 15.0   # % de rechazo que dispara ALERTA_DRIFT
TRUST_DRIFT_DEGRADACION_PP = 5.0    # pp de aumento RECHAZAR para DEGRADANDO
TRUST_DRIFT_MEJORA_PP      = 5.0    # pp de aumento APROBAR para MEJORANDO


# ── ENUMS ─────────────────────────────────────────────────────────────────────
class NivelRevision(str, Enum):
    ANALISTA      = "ANALISTA"
    COORDINADOR   = "COORDINADOR"
    INSTITUCIONAL = "INSTITUCIONAL"


class CaseStatus(str, Enum):
    PENDIENTE  = "PENDIENTE"
    EN_DISPUTA = "EN_DISPUTA"
    ESCALADO   = "ESCALADO"
    CERRADO    = "CERRADO"


# ── DATACLASSES ───────────────────────────────────────────────────────────────
@dataclass
class Escalacion:
    """Registro de una escalación dentro de un caso."""
    ts:             str
    de_nivel:       str
    a_nivel:        str
    responsable:    str
    motivo:         str


@dataclass
class GovernanceCase:
    """
    Caso de gobernanza — agrupa revisiones en conflicto sobre una decisión.

    Campos:
        case_id       — SHA8 de decision_ts (estable, reproducible)
        decision_ts   — Timestamp de la decisión original en decisions.jsonl
        pregunta      — Pregunta original (trazabilidad)
        estado        — CaseStatus actual
        nivel_actual  — Nivel de revisión activo
        reviews       — Lista de dicts de HumanReview involucradas
        escalaciones  — Historial de escalaciones
        resolucion    — Texto de cierre (solo estado CERRADO)
        resolver      — Identificador del responsable de cierre
        closed_ts     — Timestamp de cierre (solo CERRADO)
        created_ts    — Timestamp de apertura del caso
        sentinel_version — Versión activa al crear el caso
    """
    case_id:          str
    decision_ts:      str
    pregunta:         str
    estado:           CaseStatus
    nivel_actual:     NivelRevision
    reviews:          list[dict] = field(default_factory=list)
    escalaciones:     list[dict] = field(default_factory=list)
    resolucion:       str        = ""
    resolver:         str        = ""
    closed_ts:        str        = ""
    created_ts:       str        = ""
    sentinel_version: str        = SENTINEL_VERSION


@dataclass
class TrustDriftWeek:
    """Métricas de confianza para una semana ISO."""
    semana:         str     # "2026-W20"
    total:          int
    n_aprobar:      int
    n_observar:     int
    n_rechazar:     int
    pct_aprobar:    float
    pct_observar:   float
    pct_rechazar:   float
    alerta:         bool    # True si pct_rechazar >= TRUST_DRIFT_RECHAZO_ALERT


@dataclass
class TrustDriftReport:
    """Reporte completo de Trust Drift."""
    semanas:        list[TrustDriftWeek]
    tendencia:      str    # ESTABLE | DEGRADANDO | MEJORANDO
    alerta_activa:  bool
    semana_alerta:  str    # semana con mayor rechazo
    pct_rechazo_max: float
    n_semanas:      int


# ── UTILIDADES ────────────────────────────────────────────────────────────────
def _case_id_from_ts(decision_ts: str) -> str:
    """Genera un case_id estable a partir del decision_ts."""
    return hashlib.sha256(decision_ts.encode()).hexdigest()[:8]


def _detect_conflict(reviews: list[dict]) -> bool:
    """
    Detecta conflicto entre revisiones.
    Conflicto: hay al menos dos revisiones con estados distintos.
    """
    estados = {r.get("status", "") for r in reviews}
    return len(estados) > 1


def _conflict_severity(reviews: list[dict]) -> CaseStatus:
    """
    Determina el estado inicial del caso según la severidad del conflicto.
    RECHAZAR en conflicto con APROBAR → EN_DISPUTA.
    Cualquier otro conflicto → PENDIENTE.
    """
    estados = {r.get("status", "") for r in reviews}
    if "RECHAZAR" in estados and "APROBAR" in estados:
        return CaseStatus.EN_DISPUTA
    if len(estados) > 1:
        return CaseStatus.PENDIENTE
    # Consenso RECHAZAR / APROBAR / OBSERVAR → cerrar automáticamente
    return CaseStatus.CERRADO


# ── PERSISTENCIA ──────────────────────────────────────────────────────────────
def _append_case(case: GovernanceCase) -> None:
    """Persiste snapshot del caso en JSONL (latest-wins)."""
    entry = asdict(case)
    entry["estado"]        = case.estado.value
    entry["nivel_actual"]  = case.nivel_actual.value

    with CASES_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _load_all_cases() -> dict[str, dict]:
    """
    Carga todos los casos del log (latest-wins por case_id).
    Retorna dict keyed por case_id.
    """
    if not CASES_LOG.exists():
        return {}

    cases: dict[str, dict] = {}
    with CASES_LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                cases[entry["case_id"]] = entry
            except (json.JSONDecodeError, KeyError):
                continue
    return cases


# ── API PRINCIPAL ─────────────────────────────────────────────────────────────
def open_case(
    decision_ts: str,
    pregunta:    str,
    reviews:     list[dict],
) -> GovernanceCase:
    """
    Abre (o reabre) un caso de gobernanza para una decisión con revisiones en conflicto.

    Si ya existe un caso para este decision_ts, lo actualiza con las revisiones nuevas.
    Determina automáticamente el estado: EN_DISPUTA | PENDIENTE | CERRADO.
    """
    case_id   = _case_id_from_ts(decision_ts)
    now_ts    = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Verificar si ya existe el caso
    existing = _load_all_cases().get(case_id)

    if existing:
        # Mantener historial de escalaciones y estado CERRADO
        if existing.get("estado") == "CERRADO":
            # No reabrir casos cerrados automáticamente
            return _dict_to_case(existing)
        estado_str    = existing.get("estado", "PENDIENTE")
        escalaciones  = existing.get("escalaciones", [])
        nivel_str     = existing.get("nivel_actual", "ANALISTA")
        created_ts    = existing.get("created_ts", now_ts)
    else:
        escalaciones  = []
        created_ts    = now_ts
        nivel_str     = "ANALISTA"
        estado_str    = None

    # Determinar estado según conflicto
    if _detect_conflict(reviews):
        nuevo_estado = _conflict_severity(reviews)
    else:
        nuevo_estado = CaseStatus.CERRADO  # consenso → cerrar

    if estado_str and nuevo_estado == CaseStatus.CERRADO and estado_str != "CERRADO":
        # Si ya estaba abierto, no cerrar automáticamente por nuevo consenso
        nuevo_estado = CaseStatus(estado_str)

    case = GovernanceCase(
        case_id          = case_id,
        decision_ts      = decision_ts,
        pregunta         = pregunta,
        estado           = nuevo_estado,
        nivel_actual     = NivelRevision(nivel_str),
        reviews          = reviews,
        escalaciones     = escalaciones,
        resolucion       = "",
        resolver         = "",
        closed_ts        = "",
        created_ts       = created_ts,
        sentinel_version = SENTINEL_VERSION,
    )

    _append_case(case)
    return case


def escalate(
    decision_ts:  str,
    responsable:  str,
    motivo:       str,
    nivel_destino: NivelRevision | str | None = None,
) -> dict:
    """
    Escala un caso al siguiente nivel de revisión.

    Si nivel_destino es None, avanza automáticamente:
        ANALISTA → COORDINADOR → INSTITUCIONAL
    """
    cases    = _load_all_cases()
    case_id  = _case_id_from_ts(decision_ts)

    if case_id not in cases:
        raise KeyError(f"No existe caso para decision_ts='{decision_ts}'")

    raw = cases[case_id]
    case = _dict_to_case(raw)

    if case.estado == CaseStatus.CERRADO:
        raise ValueError("El caso ya está CERRADO — no puede escalarse.")

    # Determinar nivel destino
    if isinstance(nivel_destino, str):
        nivel_destino = NivelRevision(nivel_destino.upper())

    secuencia = [NivelRevision.ANALISTA, NivelRevision.COORDINADOR, NivelRevision.INSTITUCIONAL]
    if nivel_destino is None:
        idx = secuencia.index(case.nivel_actual)
        if idx + 1 >= len(secuencia):
            raise ValueError("El caso ya está en el nivel máximo (INSTITUCIONAL).")
        nivel_destino = secuencia[idx + 1]

    now_ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    esc = Escalacion(
        ts           = now_ts,
        de_nivel     = case.nivel_actual.value,
        a_nivel      = nivel_destino.value,
        responsable  = responsable,
        motivo       = motivo,
    )

    case.escalaciones.append(asdict(esc))
    case.nivel_actual = nivel_destino
    case.estado       = CaseStatus.ESCALADO

    _append_case(case)

    return {
        "case_id":       case.case_id,
        "decision_ts":   case.decision_ts,
        "estado":        case.estado.value,
        "nivel_actual":  case.nivel_actual.value,
        "escalacion":    asdict(esc),
        "mensaje":       f"Caso escalado a {nivel_destino.value} por {responsable}.",
    }


def close_case(
    decision_ts: str,
    resolver:    str,
    resolucion:  str,
    comment:     str = "",
) -> dict:
    """
    Cierra definitivamente un caso con una resolución institucional.
    Solo el nivel actual puede cerrar (validación en API).
    """
    cases   = _load_all_cases()
    case_id = _case_id_from_ts(decision_ts)

    if case_id not in cases:
        raise KeyError(f"No existe caso para decision_ts='{decision_ts}'")

    raw  = cases[case_id]
    case = _dict_to_case(raw)

    if case.estado == CaseStatus.CERRADO:
        raise ValueError("El caso ya está CERRADO.")

    if not resolucion.strip():
        raise ValueError("La resolución de cierre no puede estar vacía.")

    now_ts         = time.strftime("%Y-%m-%dT%H:%M:%S")
    case.estado    = CaseStatus.CERRADO
    case.resolucion = f"{resolucion.strip()} — {comment.strip()}" if comment.strip() else resolucion.strip()
    case.resolver  = resolver
    case.closed_ts = now_ts

    _append_case(case)

    return {
        "case_id":      case.case_id,
        "decision_ts":  case.decision_ts,
        "estado":       CaseStatus.CERRADO.value,
        "resolver":     resolver,
        "resolucion":   case.resolucion,
        "closed_ts":    now_ts,
        "mensaje":      f"Caso cerrado por {resolver}.",
    }


def get_cases(estado: str | None = None) -> list[dict]:
    """
    Retorna todos los casos, opcionalmente filtrados por estado.
    Más recientes (por created_ts) primero.
    """
    cases = _load_all_cases()
    result = list(cases.values())

    if estado:
        result = [c for c in result if c.get("estado") == estado.upper()]

    result.sort(key=lambda c: c.get("created_ts", ""), reverse=True)
    return result


def get_case(decision_ts: str) -> Optional[dict]:
    """Retorna el caso para una decisión dada, o None si no existe."""
    cases   = _load_all_cases()
    case_id = _case_id_from_ts(decision_ts)
    return cases.get(case_id)


# ── TRUST DRIFT ───────────────────────────────────────────────────────────────
def calculate_trust_drift(n_weeks: int = 8) -> TrustDriftReport:
    """
    Calcula el Trust Drift semanal de las revisiones humanas.

    Agrupa por semana ISO (YYYY-Www) y calcula distribución porcentual.
    Detecta degradación (RECHAZAR ≥ 15%) y tendencia (ESTABLE/DEGRADANDO/MEJORANDO).
    """
    from sentinel.human_review import read_reviews

    reviews = read_reviews(n=500)

    # Agrupar por semana ISO
    by_week: dict[str, list[str]] = defaultdict(list)
    for r in reviews:
        ts     = r.get("review_ts", "")
        status = r.get("status", "")
        if not ts or not status:
            continue
        try:
            import datetime
            dt   = datetime.datetime.fromisoformat(ts)
            week = f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"
            by_week[week].append(status)
        except Exception:
            continue

    # Ordenar semanas y tomar las últimas n_weeks
    semanas_ord = sorted(by_week.keys())[-n_weeks:]
    semanas_data: list[TrustDriftWeek] = []

    for semana in semanas_ord:
        statuses  = by_week[semana]
        total     = len(statuses)
        n_apr     = statuses.count("APROBAR")
        n_obs     = statuses.count("OBSERVAR")
        n_rec     = statuses.count("RECHAZAR")

        pct_apr   = round(100 * n_apr / total, 1) if total else 0.0
        pct_obs   = round(100 * n_obs / total, 1) if total else 0.0
        pct_rec   = round(100 * n_rec / total, 1) if total else 0.0
        alerta    = pct_rec >= TRUST_DRIFT_RECHAZO_ALERT

        semanas_data.append(TrustDriftWeek(
            semana      = semana,
            total       = total,
            n_aprobar   = n_apr,
            n_observar  = n_obs,
            n_rechazar  = n_rec,
            pct_aprobar = pct_apr,
            pct_observar= pct_obs,
            pct_rechazar= pct_rec,
            alerta      = alerta,
        ))

    # Tendencia: comparar primera vs última semana
    tendencia    = "ESTABLE"
    alerta_activa = any(s.alerta for s in semanas_data)
    semana_alerta = ""
    pct_max       = 0.0

    if semanas_data:
        primera  = semanas_data[0]
        ultima   = semanas_data[-1]
        max_week = max(semanas_data, key=lambda s: s.pct_rechazar)
        semana_alerta = max_week.semana
        pct_max       = max_week.pct_rechazar

        delta_rechazo = ultima.pct_rechazar - primera.pct_rechazar
        delta_aprobar = ultima.pct_aprobar  - primera.pct_aprobar

        if delta_rechazo >= TRUST_DRIFT_DEGRADACION_PP:
            tendencia = "DEGRADANDO"
        elif delta_aprobar >= TRUST_DRIFT_MEJORA_PP:
            tendencia = "MEJORANDO"
        else:
            tendencia = "ESTABLE"

    return TrustDriftReport(
        semanas         = semanas_data,
        tendencia       = tendencia,
        alerta_activa   = alerta_activa,
        semana_alerta   = semana_alerta,
        pct_rechazo_max = pct_max,
        n_semanas       = len(semanas_data),
    )


# ── HELPERS DE CONVERSIÓN ─────────────────────────────────────────────────────
def _dict_to_case(raw: dict) -> GovernanceCase:
    """Convierte un dict de JSONL a GovernanceCase."""
    return GovernanceCase(
        case_id          = raw.get("case_id", ""),
        decision_ts      = raw.get("decision_ts", ""),
        pregunta         = raw.get("pregunta", ""),
        estado           = CaseStatus(raw.get("estado", "PENDIENTE")),
        nivel_actual     = NivelRevision(raw.get("nivel_actual", "ANALISTA")),
        reviews          = raw.get("reviews", []),
        escalaciones     = raw.get("escalaciones", []),
        resolucion       = raw.get("resolucion", ""),
        resolver         = raw.get("resolver", ""),
        closed_ts        = raw.get("closed_ts", ""),
        created_ts       = raw.get("created_ts", ""),
        sentinel_version = raw.get("sentinel_version", SENTINEL_VERSION),
    )


def to_dict(report: TrustDriftReport) -> dict:
    """Serializa TrustDriftReport a dict JSON-compatible."""
    return {
        "semanas":          [asdict(s) for s in report.semanas],
        "tendencia":        report.tendencia,
        "alerta_activa":    report.alerta_activa,
        "semana_alerta":    report.semana_alerta,
        "pct_rechazo_max":  report.pct_rechazo_max,
        "n_semanas":        report.n_semanas,
        "umbral_alerta_pct": TRUST_DRIFT_RECHAZO_ALERT,
    }


# ── FORMATO CONSOLA ───────────────────────────────────────────────────────────
def format_drift(report: TrustDriftReport) -> str:
    """Formato legible del Trust Drift para consola."""
    icon_tend = {"ESTABLE": "=", "DEGRADANDO": "v", "MEJORANDO": "^"}.get(report.tendencia, "?")
    lines = [
        "=" * 62,
        "  SENTINEL · Trust Drift Report",
        "=" * 62,
        f"  Tendencia : {icon_tend} {report.tendencia}",
        f"  Semanas   : {report.n_semanas}",
        f"  ALERTA    : {'SI — drift detectado' if report.alerta_activa else 'no'}",
        "-" * 62,
        f"  {'Semana':<12} {'Total':>6} {'APR%':>7} {'OBS%':>7} {'REC%':>7} {'Alerta':>8}",
        "-" * 62,
    ]
    for s in report.semanas:
        alerta_str = "ALERTA" if s.alerta else ""
        lines.append(
            f"  {s.semana:<12} {s.total:>6} {s.pct_aprobar:>6.1f}% {s.pct_observar:>6.1f}% "
            f"{s.pct_rechazar:>6.1f}% {alerta_str:>8}"
        )
    lines.append("=" * 62)
    return "\n".join(lines)


def format_case(case: GovernanceCase | dict) -> str:
    """Formato legible de un caso de gobernanza."""
    if isinstance(case, dict):
        case = _dict_to_case(case)

    estado_icon = {
        CaseStatus.PENDIENTE:  "⏳",
        CaseStatus.EN_DISPUTA: "⚡",
        CaseStatus.ESCALADO:   "↑",
        CaseStatus.CERRADO:    "✓",
    }.get(case.estado, "•")

    lines = [
        "-" * 60,
        f"  Caso {case.case_id}  {estado_icon} {case.estado.value}",
        "-" * 60,
        f"  Nivel     : {case.nivel_actual.value}",
        f"  Decision  : {case.decision_ts}",
        f"  Pregunta  : {case.pregunta[:70]}...",
        f"  Reviews   : {len(case.reviews)} — {', '.join(r.get('status','?') for r in case.reviews)}",
        f"  Escaladas : {len(case.escalaciones)}",
    ]
    if case.resolucion:
        lines.append(f"  Resolucion: {case.resolucion[:80]}")
    if case.resolver:
        lines.append(f"  Resuelto  : {case.resolver} ({case.closed_ts})")
    lines.append("-" * 60)
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if "--drift" in args:
        report = calculate_trust_drift()
        print(format_drift(report))
        sys.exit(0)

    if "--cases" in args:
        estado = None
        if "--estado" in args:
            idx    = args.index("--estado")
            estado = args[idx + 1] if idx + 1 < len(args) else None
        cases = get_cases(estado)
        if not cases:
            print(f"No hay casos{' en estado ' + estado if estado else ''}.")
        else:
            print(f"\nCasos de gobernanza ({len(cases)}):\n")
            for c in cases[:10]:
                print(format_case(c))
        sys.exit(0)

    if "--demo" in args:
        print("\n-- Demo: open_case + escalate + close --\n")

        # Simular dos revisiones en conflicto
        reviews_demo = [
            {"status": "APROBAR",  "reviewer": "Analista-A", "comment": ""},
            {"status": "RECHAZAR", "reviewer": "Analista-B",
             "comment": "El chunk de D3 no refleja la ejecucion real Q1 2026."},
        ]
        ts_demo = "2026-05-17T10:00:00"

        case = open_case(ts_demo, "Por que D3 esta en rojo?", reviews_demo)
        print(format_case(case))

        result = escalate(ts_demo, "Coordinador-GAD", "Conflicto severo APROBAR vs RECHAZAR")
        print(f"Escalado: {result['nivel_actual']} — {result['mensaje']}")

        result2 = close_case(ts_demo, "Dir-Planificacion",
                             "Se valida posicion de Analista-B: datos Q1 2026 desactualizados en vault.",
                             "Pendiente reingestar POA Q1.")
        print(f"Cerrado : {result2['mensaje']}")

        drift = calculate_trust_drift()
        print(format_drift(drift))
        sys.exit(0)

    print("""
SENTINEL · Review Governance CLI
Uso:
  python -m sentinel.review_governance --drift              # Trust Drift semanal
  python -m sentinel.review_governance --cases              # Todos los casos
  python -m sentinel.review_governance --cases --estado EN_DISPUTA
  python -m sentinel.review_governance --demo               # Demo completo
""")
