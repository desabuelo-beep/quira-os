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

    roles = ["alcalde", "concejal", "tecnico"]

    print("Ingresa la contraseña para cada rol.")
    print("(Presiona Enter para usar 'quira2026' como valor por defecto)\n")

    hashes = {}
    for rol in roles:
        raw = input(f"  Contraseña para {rol}: ").strip()
        if not raw:
            raw = "quira2026"
            print(f"  → Usando 'quira2026'")
        hashes[rol] = _hash(raw)

    print("\n── Copia esto en .streamlit/secrets.toml ──\n")
    print("[auth]")
    for rol, h in hashes.items():
        print(f'{rol}_hash = "{h}"')

    print("\n── Y en Streamlit Cloud → Settings → Secrets ──")
    print("Pega exactamente el bloque [auth] de arriba.\n")


if __name__ == "__main__":
    main()
