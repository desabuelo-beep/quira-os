"""
QUIRA — Gate de errores silenciados  ·  `scripts/ci/check_errores_silenciosos.py`

Un `except: pass` no es siempre un defecto: una migración ya aplicada debe
fallar en silencio, y un módulo opcional que no está instalado también. El
problema es dónde.

CRITERIO (colega · 2026-08-07). La pregunta no es «¿funciona?» sino:

    ¿puede este componente producir una afirmación falsa sobre la gestión
    pública, ocultar un fallo técnico, romper la trazabilidad o impedir
    reproducir el resultado?

Un fallo tragado durante la CAPTURA es el caso peligroso: si una petición falla
y nadie se entera, el vacío resultante se lee después como «no hay nada
publicado» — y eso es una afirmación sobre un municipio que la evidencia no
sostiene. Es exactamente lo que ADR-042 §6 convirtió en código.

Este gate NO exige cero silencios. Exige que en las zonas donde un silencio
puede volverse un dato, el error al menos se REGISTRE.

Uso:  python scripts/ci/check_errores_silenciosos.py
Dylus Lab © 2026
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# Zonas donde un error tragado puede convertirse en una afirmación o borrar una
# huella. Fuera de estas, el silencio se tolera.
ZONAS_CRITICAS = (
    "app/connectors", "app/fetchers", "app/agents", "app/observatorio",
    "sentinel/audit", "sentinel/alert_engine", "sentinel/integrity_engine",
    "models/auth", "utils/session", "utils/audit_log",
)

# Operaciones que, silenciadas, dejan al sistema creyendo que hizo algo.
RIESGOSAS = ("connect", "execute", "commit", "insert", "write", "post",
             "requests", "urlopen", "fetch")

_IGNORAR = ("__pycache__", ".venv", "graphify-out", "worktrees",
            "site-packages", ".claude")


def _archivos():
    for p in RAIZ.rglob("*.py"):
        rel = p.relative_to(RAIZ).as_posix()
        if any(x in rel for x in _IGNORAR):
            continue
        if any(rel.startswith(z) or z in rel for z in ZONAS_CRITICAS):
            yield p, rel


def main() -> int:
    hallazgos: list[str] = []
    revisados = 0

    for ruta, rel in _archivos():
        try:
            arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=rel)
        except Exception:  # noqa: BLE001
            continue
        revisados += 1
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.Try):
                continue
            hace_algo_riesgoso = any(
                any(r in (getattr(c.func, "attr", "") or
                          getattr(c.func, "id", "") or "").lower()
                    for r in RIESGOSAS)
                for c in ast.walk(nodo) if isinstance(c, ast.Call))
            if not hace_algo_riesgoso:
                continue
            for h in nodo.handlers:
                # Silencio total: el cuerpo es solo `pass`.
                if len(h.body) == 1 and isinstance(h.body[0], ast.Pass):
                    # Un ImportError silenciado es una dependencia opcional.
                    tipo = ast.unparse(h.type) if h.type else "bare"
                    if "ImportError" in tipo or "ModuleNotFound" in tipo:
                        continue
                    hallazgos.append(f"{rel}:{h.lineno} — silencia «{tipo}» "
                                     f"sobre una operación que puede fallar sin "
                                     f"dejar rastro")

    print("=" * 70)
    print(f"  ERRORES SILENCIADOS EN ZONA CRÍTICA · {revisados} archivos")
    print("=" * 70)
    if hallazgos:
        print(f"\n  {len(hallazgos)} HALLAZGO(S):\n")
        for h in hallazgos:
            print(f"     >> {h}")
        print("\n  No hace falta propagar el error — basta con REGISTRARLO.")
        print("  Un fallo de captura que no deja rastro se lee luego como")
        print("  «no hay evidencia», y eso afirma algo sobre un municipio.")
        print("=" * 70)
        return 1
    print("\n  TODO OK — en zona crítica, ningún fallo se pierde sin registro")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
