"""
QUIRA OS — Utilidad: Generar hashes de contraseñas para producción
Uso:
    python scripts/generar_hashes.py
    → Te pide una contraseña y te da el hash para pegar en secrets.toml
Dylus Lab © 2026
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.auth import _hash


def main():
    print("\n╔════════════════════════════════════════╗")
    print("║  QUIRA OS — Generador de hashes auth  ║")
    print("╚════════════════════════════════════════╝\n")

    # Roles canónicos (docs/NOMENCLATURA_CANONICA.md). Los anteriores —alcalde ·
    # concejal— quedaron eliminados en la v3 de auth y aquí seguían vivos.
    roles = ["ejecutivo", "tecnico", "operador", "administrador"]

    print("Ingresa la contraseña para cada rol.")
    # Sin valor por defecto, a propósito: una contraseña por defecto termina en
    # producción. Este script la ofrecía, y esa clave acabó publicada en dos
    # documentos y en el código (corregido 2026-08-05).
    print("Usa una DISTINTA por rol — si comparten clave, quien tiene una las tiene todas.\n")

    hashes = {}
    for rol in roles:
        raw = input(f"  Contraseña para {rol}: ").strip()
        if not raw:
            print("  ⚠️  Vacío no admitido — escribe una contraseña.")
            continue
        hashes[rol] = _hash(raw)

    print("\n── Copia esto en .streamlit/secrets.toml ──\n")
    print("[auth]")
    for rol, h in hashes.items():
        print(f'{rol}_hash = "{h}"')

    print("\n── Y en Streamlit Cloud → Settings → Secrets ──")
    print("Pega exactamente el bloque [auth] de arriba.\n")


if __name__ == "__main__":
    main()
