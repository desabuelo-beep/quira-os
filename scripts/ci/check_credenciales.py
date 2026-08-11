"""
QUIRA — Gate de credenciales embebidas  ·  `scripts/ci/check_credenciales.py`

Busca credenciales escritas en archivos RASTREADOS POR GIT. No es hipotético:
el 2026-08-06 se encontró la contraseña de la base de datos en texto plano en
dos motores de producción, como «fallback directo (solo dev)».

POR QUÉ UNA CREDENCIAL EN EL CÓDIGO NO ES UN ATAJO DE DESARROLLO
  · viaja a cada clon del repositorio;
  · queda en el historial de versiones aunque después se borre — quitarla del
    archivo NO la quita de los commits anteriores;
  · convierte cualquier filtración del código en una filtración de la base.

Ya había pasado antes con `models/auth.py`, que guardaba la contraseña de
acceso en un `_FALLBACK_HASHES`. Este gate existe para que no haya una tercera.

Uso:  python scripts/ci/check_credenciales.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import subprocess
import sys
# La consola de Windows abre en cp1252 y este gate imprime flechas y viñetas.
# Sin esto revienta con UnicodeEncodeError DESPUÉS de calcular sus resultados:
# un gate que muere al informar es un gate que no informa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# Un valor es PLACEHOLDER si contiene alguna de estas marcas. Todo lo demás
# que encaje en un patrón de credencial se considera real.
_PLACEHOLDER = re.compile(
    r"\[PASSWORD\]|\[YOUR|xxx|<[^>]+>|CHANGEME|placeholder|REEMPLAZA|"
    # `TU-KEY`, `TU_PROYECTO`, `SU-CLAVE`… — con guion medio o bajo. El guion
    # medio faltaba y los tres ejemplos de la documentación salían como
    # hallazgos reales.
    r"\b(?:TU|SU|MI|YOUR|MY)[-_](?:KEY|CLAVE|PROYECTO|PROJECT|PASSWORD|TOKEN|"
    r"USUARIO|USER|API)|"
    r"example\.com|ejemplo|\bxxxx\b|\.\.\.|\$\{|\bREDACTADO\b", re.I)

# (nombre, patrón). Buscan el VALOR pegado, no la mención del concepto.
_PATRONES = [
    ("URI de PostgreSQL con contraseña",
     re.compile(r"postgres(?:ql)?://[A-Za-z0-9._%-]+:[^\s\"'@]{6,}@")),
    ("clave de API de Anthropic",     re.compile(r"sk-ant-[A-Za-z0-9_-]{12,}")),
    ("clave de API de OpenAI",        re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("token de GitHub",               re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("clave de servicio de Supabase", re.compile(r"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}")),
    ("URI de Neo4j con contraseña",   re.compile(r"neo4j(?:\+s)?://[A-Za-z0-9._%-]+:[^\s\"'@]{6,}@")),
]

EXT = {".py", ".toml", ".json", ".yaml", ".yml", ".md", ".txt", ".env",
       ".ini", ".cfg", ".sh", ".ps1", ".js", ".ts"}


def _rastreados() -> list[Path]:
    """Solo lo que git rastrea: lo ignorado (secrets.toml) no es el problema."""
    salida = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True,
                            text=True, encoding="utf-8", errors="ignore")
    return [RAIZ / linea for linea in salida.stdout.splitlines()
            if linea and Path(linea).suffix.lower() in EXT]


def main() -> int:
    hallazgos: list[str] = []
    revisados = 0

    for ruta in _rastreados():
        try:
            texto = ruta.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        revisados += 1
        for numero, linea in enumerate(texto.splitlines(), 1):
            if _PLACEHOLDER.search(linea):
                continue
            for nombre, patron in _PATRONES:
                if patron.search(linea):
                    rel = ruta.relative_to(RAIZ).as_posix()
                    # No se imprime la línea: sería filtrarla otra vez.
                    hallazgos.append(f"{rel}:{numero} — {nombre}")
                    break

    print("=" * 66)
    print(f"  CREDENCIALES EMBEBIDAS · {revisados} archivos rastreados")
    print("=" * 66)
    if hallazgos:
        print(f"\n  {len(hallazgos)} HALLAZGO(S) — no se muestra el valor:\n")
        for h in hallazgos:
            print(f"     >> {h}")
        print("\n  Retirar del archivo NO basta: la credencial queda en el")
        print("  historial de git. Hay que ROTARLA en el proveedor.")
        print("=" * 66)
        return 1
    print("\n  TODO OK — ninguna credencial en archivos rastreados")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
