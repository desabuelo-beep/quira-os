"""
SENTINEL RAG · sentinel_setup.py
Script maestro de arranque — ejecuta Sprint 0 y Sprint 1 en orden correcto.
Ejecutar: python sentinel_setup.py
Dylus Lab © 2026
"""
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent

PASOS = [
    ("Sprint 0A", "Verificar dependencias RAG",        "verify_deps"),
    ("Sprint 0B", "Auditoría YAML del vault Obsidian", "audit"),
    ("Sprint 1A", "Ingestar vault en ChromaDB",        "ingest"),
    ("Sprint 1B", "Validar con 11 preguntas",          "test"),
]

def verify_deps() -> bool:
    print("  Verificando dependencias...")
    missing = []
    for pkg, import_name in [
        ("sentence-transformers", "sentence_transformers"),
        ("chromadb",              "chromadb"),
        ("fastapi",               "fastapi"),
        ("uvicorn",               "uvicorn"),
    ]:
        try:
            __import__(import_name)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} — FALTA")
            missing.append(pkg)

    if missing:
        print(f"\n  Instalar con:")
        print(f"  pip install -r requirements_rag.txt\n")
        return False
    return True

def run_audit() -> bool:
    from sentinel.audit_yaml import audit_vault, print_report, save_reports
    informe = audit_vault()
    print_report(informe)
    save_reports(informe)
    ok = informe["stats"].get("ok", 0)
    total = informe["total_notas"]
    print(f"  → {ok}/{total} notas listas para RAG")
    if ok / total < 0.5:
        print("  ⚠️  Menos del 50% listas — considera normalizar YAML primero")
        print("  (puedes continuar con la ingesta — el sistema maneja YAML parcial)")
    return True

def run_ingest() -> bool:
    from sentinel.ingest_kb import ingest
    stats = ingest(force=False)
    return stats.get("errores", 0) < stats.get("procesadas", 1)

def run_tests() -> bool:
    from sentinel.test_queries import run_tests
    report = run_tests(verbose=True)
    return report["porcentaje"] >= 60

def main():
    print("\n" + "█"*65)
    print("  SENTINEL RAG — SETUP SPRINT 0 + SPRINT 1")
    print("  Dylus Lab © 2026 · GAD Montecristi")
    print("█"*65)

    for (sprint, descripcion, paso) in PASOS:
        print(f"\n{'─'*65}")
        print(f"  {sprint}: {descripcion}")
        print(f"{'─'*65}")

        if paso == "verify_deps":
            ok = verify_deps()
        elif paso == "audit":
            ok = run_audit()
        elif paso == "ingest":
            ok = run_ingest()
        elif paso == "test":
            ok = run_tests()
        else:
            ok = False

        if not ok and paso == "verify_deps":
            print("\n  ❌ Instalá las dependencias antes de continuar.")
            print("  Comando: pip install -r requirements_rag.txt")
            sys.exit(1)

    print("\n" + "█"*65)
    print("  SETUP COMPLETO")
    print()
    print("  Próximos pasos:")
    print("  1. Revisar reporte CSV en sentinel/reports/")
    print("  2. Normalizar notas con YAML incompleto")
    print("  3. Reingestar: python -m sentinel.ingest_kb --force")
    print("  4. Para activar LLM: configurar ANTHROPIC_API_KEY en .env")
    print("  5. Levantar API: uvicorn sentinel.api_rag:app --port 8100")
    print("█"*65 + "\n")

if __name__ == "__main__":
    main()
