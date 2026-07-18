# -*- coding: utf-8 -*-
"""
scripts/brn_compilador.py — BRN v2 · Compilación de Reglas Operativas (ADR-039)
═══════════════════════════════════════════════════════════════════════════════════
Materializa cada RO **vigente** en un ARTEFACTO DE CONFIGURACIÓN firmado, consumible por el
Gold Master. Es la "bisagra" del ciclo de liberación (molde §5b): de aquí hacia el motor manda
la Regla 1; de aquí hacia atrás manda la BRN.

QUÉ ES (ADR-039):
  · La compilación es un PROCESO, no un motor. NO decide, NO interpreta, NO calcula: MATERIALIZA
    una RO ya validada en un formato que el Gold Master puede leer.
  · DETERMINISTA · REPRODUCIBLE · IDEMPOTENTE: la misma RO produce siempre el mismo artefacto
    (misma firma SHA256); recompilar sin cambios no altera nada.

LÍMITES DUROS (ADR-039 §4 · Regla 1):
  · NO toca la fórmula canónica (H12!B33). Solo produce la TABLA DE PARÁMETROS (umbrales,
    periodicidades) — inputs, nunca la lógica de cálculo.
  · NO escribe el Gold Master vivo: GENERA un artefacto; su aplicación al motor es aparte, sobre
    COPIA, con evidencia (metodología del Gold Master). Este script se detiene en el artefacto.
  · Solo compila RO `vigente` cuya CNO también esté `vigente` (ADR-035 §5). Una RO `propuesta`
    NUNCA llega al motor.

SALIDA:  data/brn_artefacto_config.json  (firmado · NO editar a mano)
Uso:     python scripts/brn_compilador.py [--verificar]   (--verificar: no escribe, solo compara firma)
Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
BRN_DIR = REPO / "docs" / "brn"
ARTEFACTO = REPO / "data" / "brn_artefacto_config.json"
COMPILADOR_VERSION = "1.0"


def _cargar(patron: str) -> list[dict]:
    out = []
    for p in sorted(BRN_DIR.glob(patron)):
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and d.get("id"):
            out.append(d)
    return out


def _firma(contenido: dict) -> str:
    """SHA256 del contenido en orden canónico (sin la firma). Garantiza idempotencia:
    la misma RO produce siempre la misma firma."""
    payload = json.dumps(contenido, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parametros_de(ro: dict) -> list[dict]:
    """Traduce una RO en filas de parámetros — un tramo de vigencia = una fila (molde §4b).
    El compilador NO elige el umbral de hoy: entrega TODOS los tramos y el motor toma el que
    corresponde a la fecha de cálculo. Así una transición prevista no obliga a recompilar."""
    filas = []
    tramos = ro.get("vigencia_operativa") or [{"desde": None, "hasta": None, "umbral": ro.get("umbral")}]
    for t in tramos:
        filas.append({
            "variable": ro.get("variable"),
            "umbral": t.get("umbral"),
            "vigente_desde": t.get("desde"),
            "vigente_hasta": t.get("hasta"),
            "frecuencia": (ro.get("periodo") or {}).get("frecuencia"),
            "ro": ro["id"], "ro_version": ro.get("version"),
            "opera_en": ro.get("opera_en"),
        })
    return filas


def main() -> int:
    solo_verificar = "--verificar" in sys.argv
    cnos = {c["id"]: c for c in _cargar("CNO-*.yaml")}
    ros = _cargar("RO-*.yaml")

    compiladas, saltadas = [], []
    parametros = []
    for ro in ros:
        cno_id = str(ro.get("deriva_de", "")).split()[0]
        cno = cnos.get(cno_id, {})
        # el compilador NO decide: solo materializa lo YA validado (ADR-039)
        if ro.get("estado") != "vigente":
            saltadas.append(f'{ro["id"]} (RO {ro.get("estado")})')
            continue
        if cno.get("estado") != "vigente":
            saltadas.append(f'{ro["id"]} (CNO {cno.get("estado", "ausente")})')
            continue
        parametros.extend(_parametros_de(ro))
        compiladas.append({
            "ro": ro["id"], "ro_version": ro.get("version"),
            "cno": cno_id, "cno_version": cno.get("version"),
            "consumida_por": ro.get("consumida_por", []),
            # traza jurídica: los SHA de la cadena que funda estos parámetros (ADR-039 §5)
            "cadena_sha": [e.get("sha256") for e in cno.get("cadena", []) if e.get("sha256")],
        })

    # contenido determinista (sin build ni firma → idempotente ante recompilación)
    contenido = {
        "_tipo": "artefacto_configuracion_compilado",
        "_advertencia": "GENERADO POR COMPILACIÓN · NO editar a mano · NO es el Gold Master · "
                        "aplicar al motor es aparte, sobre COPIA con evidencia (Regla 1)",
        "compilador_version": COMPILADOR_VERSION,
        "generado_de": compiladas,
        "parametros_tabla": parametros,
    }
    firma = _firma(contenido)

    # ¿idempotente? comparar contra el artefacto previo
    firma_previa = None
    if ARTEFACTO.exists():
        try:
            firma_previa = json.loads(ARTEFACTO.read_text(encoding="utf-8")).get("firma_sha256")
        except Exception:
            pass

    print(f"BRN · Compilador {COMPILADOR_VERSION} — {len(compiladas)} RO vigente(s) compilada(s), "
          f"{len(parametros)} fila(s) de parámetros")
    for c in compiladas:
        print(f'   ✓ {c["ro"]} v{c["ro_version"]} ← {c["cno"]} v{c["cno_version"]} → {", ".join(c["consumida_por"]) or "—"}')
    if saltadas:
        print(f'   ⏭ no compiladas (no vigentes): {", ".join(saltadas)}')
    print(f"   firma: {firma[:16]}…", "(sin cambios · idempotente)" if firma == firma_previa else "(NUEVA)")

    if solo_verificar:
        ok = firma == firma_previa
        print("VERIFICACIÓN:", "OK — artefacto al día" if ok else "DIVERGE — falta recompilar")
        return 0 if ok else 1

    salida = {**contenido, "build": datetime.now(timezone.utc).strftime("%Y.%m.%d"),
              "build_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "firma_sha256": firma}
    ARTEFACTO.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — artefacto firmado escrito: {ARTEFACTO.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
