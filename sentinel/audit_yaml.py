"""
SENTINEL RAG · audit_yaml.py
Sprint 0 — Auditoría de gobernanza del vault Obsidian.
Detecta: notas sin YAML, campos faltantes, nombres de campo inconsistentes,
notas vacías, y genera reporte CSV + resumen consola.
Ejecutar: python -m sentinel.audit_yaml
Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import re
import csv
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Asegurar encoding UTF-8 en Windows
sys.stdout.reconfigure(encoding="utf-8")

# Importar config — con fallback si se corre standalone
try:
    from sentinel.rag_config import (
        VAULT_DIR, REPORTS_DIR, YAML_CAMPOS_REQUERIDOS, YAML_ALIASES
    )
except ImportError:
    VAULT_DIR   = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi")
    REPORTS_DIR = Path(__file__).parent / "reports"
    YAML_CAMPOS_REQUERIDOS = [
        "tipo_nota", "nombre", "territorio", "dimension_tgi",
        "tags", "fecha", "estado", "fuente_canonica",
    ]
    YAML_ALIASES = {
        "tipo_nota":       ["tipo", "type"],
        "nombre":          ["name", "titulo", "title"],
        "tags":            ["etiquetas", "keywords"],
        "fecha":           ["fecha_creacion", "date", "fecha_actualizacion"],
        "fuente_canonica": ["gold_master", "fuente", "source"],
        "estado":          ["status"],
    }

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ── TIPOS CONOCIDOS (para validar tipo_nota) ───────────────────────────────────
TIPOS_VALIDOS = {
    "dashboard", "core", "meta-sistema", "pdot", "fondo", "fuente-financiamiento",
    "actor", "normativa", "brecha", "ejecucion", "parroquia", "parroquia-tgi",
    "sentinel", "alerta-tgi", "alerta", "indicador", "plantilla", "indice",
    "programa", "proyecto", "diagnostico", "marco-plurianual-pdot",
}


def _extract_frontmatter(text: str) -> tuple[dict, str]:
    """
    Extrae el bloque YAML frontmatter de una nota Obsidian.
    Retorna (dict_yaml, contenido_sin_yaml).
    Maneja YAML con comentarios (#) y bloques malformados.
    """
    if not text.strip().startswith("---"):
        return {}, text

    # Encontrar cierre del bloque ---
    lines = text.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, text

    yaml_block = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])

    # Parsear manualmente — evita dependencia de PyYAML para casos edge
    data = {}
    current_key = None
    current_list = None

    for raw_line in yaml_block.split("\n"):
        # Eliminar comentarios inline tipo # === SECCIÓN ===
        line = re.sub(r"\s*#.*$", "", raw_line).rstrip()
        if not line:
            continue

        # Lista item
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip("- ").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(item)
            elif current_key:
                data[current_key] = [item]
                current_list = data[current_key]
            continue

        # Key: value
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip().lower()
            val = parts[1].strip().strip('"').strip("'") if len(parts) > 1 else ""

            if val == "" and not line.strip().endswith(":"):
                # probablemente es un objeto anidado — tratamos como string vacío
                pass

            current_key = key
            current_list = None

            if val:
                data[key] = val
            else:
                data[key] = None  # se llenará con lista si siguen items

    return data, body


def _resolve_field(yaml: dict, campo: str) -> tuple[str | None, str]:
    """
    Busca el campo en el dict YAML, incluyendo aliases.
    Retorna (valor_encontrado_o_None, nombre_campo_encontrado).
    """
    # Nombre canónico directo
    if campo in yaml and yaml[campo] is not None:
        return str(yaml[campo]), campo

    # Buscar en aliases
    aliases = YAML_ALIASES.get(campo, [])
    for alias in aliases:
        if alias in yaml and yaml[alias] is not None:
            return str(yaml[alias]), alias

    return None, ""


def _word_count(text: str) -> int:
    return len(text.split())


def audit_vault() -> dict:
    """
    Escanea todas las notas .md del vault y retorna el informe completo.
    """
    md_files = list(VAULT_DIR.rglob("*.md"))
    total = len(md_files)

    results = []
    stats = defaultdict(int)
    tipo_distribution = defaultdict(int)
    folder_stats = defaultdict(lambda: {"total": 0, "ok": 0, "warn": 0, "error": 0})

    for md_path in sorted(md_files):
        rel = md_path.relative_to(VAULT_DIR)
        folder = str(rel.parent)
        content = ""

        try:
            content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            content = ""
            results.append({
                "archivo": str(rel),
                "carpeta": folder,
                "estado": "ERROR",
                "palabras": 0,
                "tiene_yaml": False,
                "campos_ok": [],
                "campos_faltantes": YAML_CAMPOS_REQUERIDOS.copy(),
                "campos_alias": [],
                "tipo_nota": "",
                "tipo_valido": False,
                "problemas": [f"No se pudo leer: {e}"],
            })
            stats["error"] += 1
            folder_stats[folder]["total"] += 1
            folder_stats[folder]["error"] += 1
            continue

        yaml_data, body = _extract_frontmatter(content)
        tiene_yaml = bool(yaml_data)
        palabras = _word_count(content)

        problemas = []
        campos_ok = []
        campos_faltantes = []
        campos_alias = []   # campos encontrados via alias (necesitan renombrar)

        # Nota vacía
        if palabras < 10:
            problemas.append("Nota vacía o casi vacía")

        # Verificar cada campo requerido
        for campo in YAML_CAMPOS_REQUERIDOS:
            valor, found_as = _resolve_field(yaml_data, campo)

            if valor is not None:
                campos_ok.append(campo)
                if found_as and found_as != campo:
                    campos_alias.append(f"{found_as}→{campo}")
            else:
                campos_faltantes.append(campo)

        # Validar tipo_nota
        tipo_raw, _ = _resolve_field(yaml_data, "tipo_nota")
        tipo_valido = False
        if tipo_raw:
            tipo_clean = tipo_raw.lower().strip()
            tipo_distribution[tipo_clean] += 1
            tipo_valido = tipo_clean in TIPOS_VALIDOS
            if not tipo_valido:
                problemas.append(f"tipo_nota desconocido: '{tipo_clean}'")
        else:
            tipo_distribution["(sin tipo)"] += 1

        # Clasificar estado general
        n_faltantes = len(campos_faltantes)
        if n_faltantes == 0 and not problemas:
            estado = "OK"
            stats["ok"] += 1
            folder_stats[folder]["ok"] += 1
        elif n_faltantes <= 2:
            estado = "WARN"
            stats["warn"] += 1
            folder_stats[folder]["warn"] += 1
            if campos_faltantes:
                problemas.append(f"Faltan: {', '.join(campos_faltantes)}")
        else:
            estado = "ERROR"
            stats["error"] += 1
            folder_stats[folder]["error"] += 1
            if campos_faltantes:
                problemas.append(f"Faltan {n_faltantes} campos: {', '.join(campos_faltantes)}")

        if campos_alias:
            problemas.append(f"Aliases no canónicos: {', '.join(campos_alias)}")

        folder_stats[folder]["total"] += 1

        results.append({
            "archivo":          str(rel),
            "carpeta":          folder,
            "estado":           estado,
            "palabras":         palabras,
            "tiene_yaml":       tiene_yaml,
            "campos_ok":        campos_ok,
            "campos_faltantes": campos_faltantes,
            "campos_alias":     campos_alias,
            "tipo_nota":        tipo_raw or "",
            "tipo_valido":      tipo_valido,
            "problemas":        problemas,
        })

    stats["total"] = total
    stats["sin_yaml"] = sum(1 for r in results if not r["tiene_yaml"])

    return {
        "timestamp":    datetime.now().isoformat(),
        "vault":        str(VAULT_DIR),
        "total_notas":  total,
        "stats":        dict(stats),
        "por_carpeta":  dict(folder_stats),
        "tipos":        dict(tipo_distribution),
        "notas":        results,
    }


def print_report(informe: dict) -> None:
    """Imprime resumen legible en consola."""
    s = informe["stats"]
    total = informe["total_notas"]

    print("\n" + "═" * 65)
    print("  SENTINEL · AUDITORÍA YAML DEL VAULT")
    print("  Dylus Lab © 2026")
    print("═" * 65)
    print(f"  Vault:   {informe['vault']}")
    print(f"  Fecha:   {informe['timestamp'][:19]}")
    print("─" * 65)
    print(f"  Total notas escaneadas:    {total:>4}")
    print(f"  ✅ OK (listos para RAG):   {s.get('ok', 0):>4}  ({s.get('ok', 0)/total*100:.0f}%)")
    print(f"  ⚠️  WARN (1-2 campos):      {s.get('warn', 0):>4}  ({s.get('warn', 0)/total*100:.0f}%)")
    print(f"  ❌ ERROR (3+ campos):      {s.get('error', 0):>4}  ({s.get('error', 0)/total*100:.0f}%)")
    print(f"  Sin YAML:                  {s.get('sin_yaml', 0):>4}")
    print("─" * 65)

    print("\n  Por carpeta:")
    for carpeta, cst in sorted(informe["por_carpeta"].items()):
        barra_ok   = "█" * cst["ok"]
        barra_warn = "▒" * cst["warn"]
        barra_err  = "░" * cst["error"]
        print(f"  {carpeta:<40} {cst['total']:>3} notas  {barra_ok}{barra_warn}{barra_err}")

    print("\n  Distribución tipo_nota:")
    for tipo, count in sorted(informe["tipos"].items(), key=lambda x: -x[1]):
        print(f"  {tipo:<35} {count:>3}")

    # Notas problemáticas prioritarias
    errores = [n for n in informe["notas"] if n["estado"] == "ERROR"]
    if errores:
        print(f"\n  ❌ Las {min(len(errores), 15)} notas más críticas:")
        for n in errores[:15]:
            print(f"  · {n['archivo']}")
            for p in n["problemas"][:2]:
                print(f"      → {p}")

    warns = [n for n in informe["notas"] if n["estado"] == "WARN"]
    if warns:
        print(f"\n  ⚠️  {len(warns)} notas con advertencias (ver CSV para detalle)")

    print("\n" + "═" * 65)


def save_reports(informe: dict) -> None:
    """Guarda CSV + JSON en sentinel/reports/."""
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    # CSV — para revisar en Excel
    csv_path = REPORTS_DIR / f"audit_yaml_{ts}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "archivo", "carpeta", "estado", "palabras", "tiene_yaml",
            "tipo_nota", "tipo_valido",
            "campos_ok_count", "campos_faltantes_count",
            "campos_faltantes", "campos_alias", "problemas"
        ])
        writer.writeheader()
        for n in informe["notas"]:
            writer.writerow({
                "archivo":              n["archivo"],
                "carpeta":              n["carpeta"],
                "estado":               n["estado"],
                "palabras":             n["palabras"],
                "tiene_yaml":           n["tiene_yaml"],
                "tipo_nota":            n["tipo_nota"],
                "tipo_valido":          n["tipo_valido"],
                "campos_ok_count":      len(n["campos_ok"]),
                "campos_faltantes_count": len(n["campos_faltantes"]),
                "campos_faltantes":     " | ".join(n["campos_faltantes"]),
                "campos_alias":         " | ".join(n["campos_alias"]),
                "problemas":            " | ".join(n["problemas"]),
            })

    # JSON — para consumo programático
    json_path = REPORTS_DIR / f"audit_yaml_{ts}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(informe, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n  Reportes guardados:")
    print(f"  CSV  → {csv_path}")
    print(f"  JSON → {json_path}\n")


if __name__ == "__main__":
    print("  Escaneando vault...")
    informe = audit_vault()
    print_report(informe)
    save_reports(informe)
