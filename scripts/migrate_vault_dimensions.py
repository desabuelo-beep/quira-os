"""
scripts/migrate_vault_dimensions.py
P2 — Normalizacion Semantica dimension_tgi · QUIRA OS · 2026-05-20

Migra todos los valores dimension_tgi del vault al schema canonico v1.0.
Opera sobre los archivos .md directamente. Crea backup antes de modificar.

Caracteristicas:
  - Backup completo en data/vault_backup_p2/ antes de cualquier cambio
  - Reemplazos ordenados por longitud (longest-first) para evitar colisiones
  - Log detallado de cada cambio con archivo, alias antiguo y canonico
  - Verificacion post-migracion: sin aliases residuales
  - Dry-run disponible con --dry-run

Uso:
  python scripts/migrate_vault_dimensions.py          # migracion real
  python scripts/migrate_vault_dimensions.py --dry-run # solo reporta, no escribe
  python scripts/migrate_vault_dimensions.py --verify  # solo verifica estado actual

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# ── RUTAS ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
try:
    from config import VAULT_DIR as _VAULT_BASE
except Exception:                                        # noqa: BLE001
    import os as _os
    _VAULT_BASE = Path(_os.environ.get("QUIRA_VAULT", "."))
VAULT      = _VAULT_BASE
SCHEMA_PATH = BASE_DIR / "data" / "vault_schema.json"
BACKUP_DIR = BASE_DIR / "data" / "vault_backup_p2"
LOG_PATH   = BASE_DIR / "data" / "migration_p2_log.json"

# ── CARGAR SCHEMA ─────────────────────────────────────────────────────────────
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
ALIAS_MAP: dict[str, str] = schema["alias_map"]
CANONICAL_IDS = set(schema["dimensiones"].keys())

# Ordenar aliases por longitud DESC para evitar reemplazos parciales
# (D1_Legalidad_Coherencia antes que D1_Legalidad)
SORTED_ALIASES = sorted(
    [(alias, canon) for alias, canon in ALIAS_MAP.items() if alias != canon],
    key=lambda x: len(x[0]),
    reverse=True,
)


# ── VERIFICADOR: cuenta aliases residuales ────────────────────────────────────
def verify_vault() -> dict:
    """
    Escanea el vault y reporta aliases residuales.
    Retorna {alias: count} de valores no-canonicos encontrados.
    """
    residuales: dict[str, int] = defaultdict(int)
    files_with_issues: dict[str, list] = defaultdict(list)

    for md_path in sorted(VAULT.rglob("*.md")):
        if any(p.startswith(".") for p in md_path.parts):
            continue
        try:
            content = md_path.read_text(encoding="utf-8", errors="replace")
            if not content.startswith("---"):
                continue
            end = content.find("---", 3)
            if end == -1:
                continue
            fm = content[3:end]
            if "dimension_tgi" not in fm:
                continue
            for alias, _ in SORTED_ALIASES:
                # Buscar el alias como valor en el frontmatter
                pattern = r'(?<![A-Za-z0-9_])' + re.escape(alias) + r'(?![A-Za-z0-9_])'
                if re.search(pattern, fm):
                    residuales[alias] += 1
                    files_with_issues[alias].append(str(md_path.relative_to(VAULT)))
        except Exception:
            pass

    return {"residuales": dict(residuales), "files": dict(files_with_issues)}


# ── BACKUP ───────────────────────────────────────────────────────────────────
def backup_vault() -> int:
    """Crea backup de todos los .md con dimension_tgi. Retorna numero de archivos."""
    backed_up = 0
    for md_path in sorted(VAULT.rglob("*.md")):
        if any(p.startswith(".") for p in md_path.parts):
            continue
        try:
            content = md_path.read_text(encoding="utf-8", errors="replace")
            if "dimension_tgi" not in content[:2000]:
                continue
            rel = md_path.relative_to(VAULT)
            bak = BACKUP_DIR / rel
            bak.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_path, bak)
            backed_up += 1
        except Exception as e:
            print(f"  WARN backup {md_path.name}: {e}")
    return backed_up


# ── MIGRACIÓN DE UN ARCHIVO ───────────────────────────────────────────────────
def migrate_file(md_path: Path, dry_run: bool = False) -> list[dict]:
    """
    Migra dimension_tgi de un archivo al schema canonico.
    Retorna lista de cambios aplicados (vacia si no hubo cambios).
    """
    try:
        content = md_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    if not content.startswith("---"):
        return []

    end_idx = content.find("---", 3)
    if end_idx == -1:
        return []

    frontmatter = content[3:end_idx]
    if "dimension_tgi" not in frontmatter:
        return []

    new_fm = frontmatter
    applied: list[dict] = []

    for alias, canonical in SORTED_ALIASES:
        # Patron: alias completo, no como parte de otra palabra
        pattern = r'(?<![A-Za-z0-9_])' + re.escape(alias) + r'(?![A-Za-z0-9_])'
        matches = re.findall(pattern, new_fm)
        if matches:
            new_fm = re.sub(pattern, canonical, new_fm)
            applied.append({
                "alias":    alias,
                "canonical": canonical,
                "count":    len(matches),
            })

    if applied and not dry_run:
        new_content = "---" + new_fm + content[end_idx:]
        md_path.write_text(new_content, encoding="utf-8")

    return applied


# ── MIGRACIÓN COMPLETA ────────────────────────────────────────────────────────
def run_migration(dry_run: bool = False) -> dict:
    """
    Ejecuta la migracion completa del vault.
    Retorna estadisticas y log de cambios.
    """
    print(f"\n{'='*65}")
    print(f"  MIGRACION P2 -- dimension_tgi -> schema canonico v1.0")
    if dry_run:
        print("  MODO: DRY-RUN (no se modifican archivos)")
    print(f"{'='*65}\n")

    # 1. Verificar estado ANTES
    print("1. Estado pre-migracion:")
    pre = verify_vault()
    if not pre["residuales"]:
        print("   [OK] Vault ya esta limpio. No hay aliases residuales.")
        return {"status": "already_clean", "pre": pre, "changes": []}
    for alias, count in sorted(pre["residuales"].items()):
        print(f"   WARN {alias}: {count} ocurrencias")
    print()

    # 2. Backup
    if not dry_run:
        print("2. Creando backup...")
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        n_bak = backup_vault()
        print(f"   Archivos respaldados: {n_bak} -> {BACKUP_DIR}")
        print()

    # 3. Migrar
    print(f"3. {'Simulando' if dry_run else 'Ejecutando'} migracion...")
    all_changes: list[dict] = []
    files_modified = 0
    total_replacements = 0

    for md_path in sorted(VAULT.rglob("*.md")):
        if any(p.startswith(".") for p in md_path.parts):
            continue
        changes = migrate_file(md_path, dry_run=dry_run)
        if changes:
            rel = str(md_path.relative_to(VAULT))
            files_modified += 1
            for c in changes:
                total_replacements += c["count"]
                all_changes.append({
                    "file":     rel,
                    "alias":    c["alias"],
                    "canonical": c["canonical"],
                    "count":    c["count"],
                })
            action = "  [DRY]" if dry_run else "  [ok]"
            print(f"{action} {rel}")
            for c in changes:
                print(f"       {c['alias']} -> {c['canonical']} ({c['count']}x)")

    print(f"\n   Archivos {'que se modificarian' if dry_run else 'modificados'}: {files_modified}")
    print(f"   Reemplazos totales:   {total_replacements}")

    # 4. Verificar estado DESPUÉS
    if not dry_run:
        print("\n4. Verificando estado post-migracion...")
        post = verify_vault()
        if not post["residuales"]:
            print("   [OK] VAULT LIMPIO ? sin aliases residuales")
        else:
            print("   WARN ALIASES RESIDUALES (revisar manualmente):")
            for alias, count in post["residuales"].items():
                print(f"      {alias}: {count} en {post['files'].get(alias, [])}")
    else:
        post = {}

    # 5. Guardar log
    log = {
        "timestamp":      datetime.now().isoformat(),
        "dry_run":        dry_run,
        "schema_version": schema["SCHEMA_VAULT_VERSION"],
        "stats": {
            "files_modified":    files_modified,
            "total_replacements": total_replacements,
        },
        "pre_migration":  pre,
        "post_migration": post,
        "changes":        all_changes,
    }

    if not dry_run:
        LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n   Log guardado: {LOG_PATH}")

    print(f"\n{'='*65}")
    print(f"  {'DRY-RUN COMPLETO' if dry_run else 'MIGRACI?N COMPLETADA'}")
    print(f"{'='*65}\n")
    return log


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if "--verify" in args:
        print("\nVerificando estado actual del vault...")
        result = verify_vault()
        if not result["residuales"]:
            print("[OK] Vault limpio ? todos los dimension_tgi son canonicos.")
        else:
            print("WARN Aliases no-canonicos encontrados:")
            for alias, count in sorted(result["residuales"].items()):
                print(f"  {alias}: {count}x")
                for f in result["files"].get(alias, [])[:3]:
                    print(f"    -> {f}")
        sys.exit(0)

    dry_run = "--dry-run" in args
    run_migration(dry_run=dry_run)
