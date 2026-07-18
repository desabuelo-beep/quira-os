# -*- coding: utf-8 -*-
"""
scripts/brn_compilador.py — BRN v2 · Compilación de Reglas Operativas (ADR-039)
═══════════════════════════════════════════════════════════════════════════════════
Materializa cada RO **vigente** en un ARTEFACTO consumible por el Gold Master. Es la "bisagra"
del ciclo de liberación (molde §5b): de aquí hacia el motor manda la Regla 1.

DOS PLANOS SEPARADOS (colega · 2026-07-18) — desacoplan el motor de la BRN:
  · data/brn_config.json   → SOLO EJECUCIÓN. Lo único que el Gold Master lee: variable, umbral,
    desde, hasta, frecuencia, ancla del motor. NO conoce RO, CNO ni SHA.
  · data/brn_manifest.json → TRAZABILIDAD. RO·CNO·SHA de la cadena·build·firma·fecha·compilador.
    Es lo que audita la BRN. El motor nunca lo mira.

PROPIEDADES (ADR-039):
  · PROCESO, no motor: no decide, no interpreta, no calcula — MATERIALIZA una RO ya validada.
  · DETERMINISTA·REPRODUCIBLE·IDEMPOTENTE: la firma es el SHA256 del config; recompilar sin
    cambios = misma firma, mismo artifact_id.
  · El compilador ENTREGA TODOS LOS TRAMOS de vigencia; NUNCA pregunta "¿qué tramo toca hoy?".
    Resolver la vigencia a una fecha es tarea del RUNTIME (molde §4b), no de la compilación.

LÍMITES DUROS (ADR-039 §4 · Regla 1): NO toca la fórmula canónica (H12!B33); NO escribe el Gold
Master vivo — genera artefactos; aplicarlos al motor es aparte, sobre COPIA con evidencia.
Solo compila RO `vigente` cuya CNO también esté `vigente` (ADR-035 §5).

SALIDA:  data/brn_config.json · data/brn_manifest.json   (firmados · NO editar a mano)
Uso:     python scripts/brn_compilador.py [--verificar]
Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
BRN_DIR = REPO / "docs" / "brn"
CONFIG = REPO / "data" / "brn_config.json"
MANIFEST = REPO / "data" / "brn_manifest.json"
COMPILADOR_VERSION = "1.0"
ARTIFACT_SCHEMA = "1.0"          # versión del FORMATO del artefacto (independiente del compilador)


def _cargar(patron: str) -> list[dict]:
    out = []
    for p in sorted(BRN_DIR.glob(patron)):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("id"):
            out.append(d)
    return out


def _firma(contenido: dict) -> str:
    """SHA256 del config en orden canónico. Idempotente: mismo config = misma firma."""
    payload = json.dumps(contenido, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parametros_de(ro: dict) -> list[dict]:
    """Traduce una RO en filas de EJECUCIÓN — un tramo de vigencia = una fila (molde §4b).
    Lee la estructura de tres planos (métrica·parámetros·método): del config solo salen métrica y
    parámetros; el método es algoritmo conceptual, no ejecución. Entrega TODOS los tramos; el
    runtime elige el de la fecha. El compilador no decide y NO conoce el motor (la RO tampoco)."""
    m = ro.get("metrica") or {}
    p = ro.get("parametros") or {}
    tramos = p.get("vigencia_operativa") or [{"desde": None, "hasta": None, "umbral": p.get("umbral")}]
    filas = []
    for t in tramos:
        filas.append({
            "variable": m.get("nombre"),
            "umbral": t.get("umbral"),
            "desde": t.get("desde"),
            "hasta": t.get("hasta"),
            "frecuencia": p.get("frecuencia"),
            "opera_en": ro.get("opera_en"),
        })
    return filas


def main() -> int:
    solo_verificar = "--verificar" in sys.argv
    cnos = {c["id"]: c for c in _cargar("CNO-*.yaml")}
    ros = _cargar("RO-*.yaml")

    parametros, traza, saltadas = [], [], []
    for ro in ros:
        cno_id = str(ro.get("deriva_de", "")).split()[0]
        cno = cnos.get(cno_id, {})
        if ro.get("estado") != "vigente":
            saltadas.append(f'{ro["id"]} (RO {ro.get("estado")})'); continue
        if cno.get("estado") != "vigente":
            saltadas.append(f'{ro["id"]} (CNO {cno.get("estado", "ausente")})'); continue
        parametros.extend(_parametros_de(ro))
        traza.append({
            "ro": ro["id"], "ro_version": ro.get("version"),
            "cno": cno_id, "cno_version": cno.get("version"),
            "consume": ro.get("consume", []),
            "cadena_sha": [e.get("sha256") for e in cno.get("cadena", []) if e.get("sha256")],
        })

    # ── PLANO 1 · config de EJECUCIÓN (lo único que el motor lee) ──────────────
    config = {"artifact_schema": ARTIFACT_SCHEMA, "parametros": parametros}
    firma = _firma(config)
    artifact_id = f"BRN-BUILD-{firma[:8]}"        # derivado de la firma → idempotente y auditable
    config = {"artifact_schema": ARTIFACT_SCHEMA, "artifact_id": artifact_id, "parametros": parametros}

    firma_previa = None
    if MANIFEST.exists():
        try:
            firma_previa = json.loads(MANIFEST.read_text(encoding="utf-8")).get("firma_sha256")
        except Exception:
            pass

    print(f"BRN · Compilador {COMPILADOR_VERSION} (schema {ARTIFACT_SCHEMA}) — "
          f"{len(traza)} RO vigente(s), {len(parametros)} fila(s) de ejecución")
    for c in traza:
        print(f'   ✓ {c["ro"]} v{c["ro_version"]} ← {c["cno"]} v{c["cno_version"]} → {", ".join(c["consume"]) or "—"}')
    if saltadas:
        print(f'   ⏭ no compiladas (no vigentes): {", ".join(saltadas)}')
    print(f"   {artifact_id}", "(sin cambios · idempotente)" if firma == firma_previa else "(NUEVA firma)")

    if solo_verificar:
        ok = firma == firma_previa
        print("VERIFICACIÓN:", "OK — artefacto al día" if ok else "DIVERGE — falta recompilar")
        return 0 if ok else 1

    # ── PLANO 2 · manifest de TRAZABILIDAD (lo que audita la BRN; el motor no lo mira) ──
    ahora = datetime.now(timezone.utc)
    manifest = {
        "artifact_schema": ARTIFACT_SCHEMA, "artifact_id": artifact_id,
        "compilador_version": COMPILADOR_VERSION,
        "build": ahora.strftime("%Y.%m.%d"), "build_utc": ahora.isoformat(timespec="seconds"),
        "firma_sha256": firma,                    # firma del config (identidad idempotente)
        "_nota": "config.json = ejecución (motor) · manifest.json = trazabilidad (BRN). "
                 "El compilador entrega todos los tramos; el runtime resuelve la vigencia (§4b).",
        "generado_de": traza,
    }
    CONFIG.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — {CONFIG.relative_to(REPO)} + {MANIFEST.relative_to(REPO)} ({artifact_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
