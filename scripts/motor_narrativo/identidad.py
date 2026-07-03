# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — Etapa 0 · IDENTIDAD
Dylus Lab © 2026 · doctrina: MOTOR_NARRATIVO_QUIRA.md §2 (asesor 2026-07-04).

ANTES de descargar un video se registra QUIÉN habla y en qué contexto. Ese
registro es auditable y viaja con todo el pipeline (fundamento de la trazabilidad).

Registro: autoridad · institución · cargo · fecha · evento · período · enlace · hash.
El hash del audio lo completa la etapa 1 (adquirir.py).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
BASE = _ROOT / "data" / "motor_narrativo"


def _video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else re.sub(r"[^A-Za-z0-9_-]", "", url)[-11:]


def registrar(url: str, autoridad: str, institucion: str, cargo: str,
              evento: str, periodo: str, nivel: str = "municipal",
              fecha_evento: str | None = None) -> dict:
    """Crea (o actualiza) el registro de identidad de un discurso público.

    nivel: 'municipal' | 'nacional' | 'entidad' — determina la biblioteca de
           evidencia del cruce de 5 capas (MOTOR_NARRATIVO_QUIRA.md §4).
    """
    vid = _video_id(url)
    ident = {
        "video_id": vid,
        "url": url,
        "autoridad": autoridad,
        "institucion": institucion,
        "cargo": cargo,
        "nivel": nivel,
        "evento": evento,               # p.ej. "Rendición de Cuentas"
        "periodo": periodo,             # ejercicio que se rinde
        "fecha_evento": fecha_evento,
        "registrado_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audio_path": None,             # ← etapa 1
        "audio_sha256": None,           # ← etapa 1 (huella auditable)
        "duracion_seg": None,           # ← etapa 1
    }
    d = BASE / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "identidad.json").write_text(json.dumps(ident, ensure_ascii=False, indent=2), encoding="utf-8")
    return ident


def cargar(video_id: str) -> dict | None:
    p = BASE / video_id / "identidad.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


# ── Registro del piloto: RDC Montecristi 2024 y 2025 ─────────────────────────
PILOTO = {
    "2024": dict(url="https://www.youtube.com/watch?v=mqDT5jKXHW8",
                 autoridad="Alcalde de Montecristi", institucion="GAD Municipal de Montecristi",
                 cargo="Alcalde", evento="Rendición de Cuentas", periodo="2023", nivel="municipal"),
    "2025": dict(url="https://www.youtube.com/watch?v=Qexwg7EKmUo",
                 autoridad="Alcalde de Montecristi", institucion="GAD Municipal de Montecristi",
                 cargo="Alcalde", evento="Rendición de Cuentas", periodo="2024", nivel="municipal"),
}


if __name__ == "__main__":
    import sys
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    ident = registrar(**PILOTO[año])
    print(f"IDENTIDAD registrada · {año}: {ident['video_id']} · {ident['autoridad']} · "
          f"{ident['evento']} (rinde {ident['periodo']})")
    print(f"   {BASE / ident['video_id'] / 'identidad.json'}")
