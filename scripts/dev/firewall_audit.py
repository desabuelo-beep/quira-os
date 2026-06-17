#!/usr/bin/env python3
"""
Firewall Audit — barrido determinista de la frontera de lenguaje (Regla 2 · Bloomberg).
Mide la "deuda de frontera": terminos canonicos/internos que aparecen en STRINGS VISIBLES
al usuario. NO corrige — solo MIDE (ley de la mesa: no estimar, medir).

Clasificacion de capa (donde el grep ciego fallaba):
  - docstrings (modulo/func/clase) y comentarios  -> capa INTERNA (permitido · no se escanea)
  - string literals + partes literales de f-strings -> candidato VISIBLE (se escanea)

Riesgo:
  - ALTO  = termino embebido en texto/HTML visible ("IGP 27.98% fuente: H73 ...")
  - BAJO  = el string ES la clave bare (ej. .get("IGP")) -> probable acceso a dato interno

Importante: NO marca terminos PUBLICOS legitimos (SIGEF/eSIGEF/SERCOP/CPCCS/LOTAIP/COOTAD/
PDOT/POA/PAC/ODS/NBI/CNE/RDC) — esos SON lenguaje de gobernanza correcto.

Uso:  python scripts/dev/firewall_audit.py [carpeta]     (default: quira_pages)
"""
from __future__ import annotations
import ast
import json
import re
import sys
from pathlib import Path

# Corpus PROHIBIDO en capa publica -> alternativa de gobernanza. Case-sensitive a proposito
# (la prosa en minusculas no debe disparar: "participacion" != IGP, "satelite" != SAT).
PROHIBITED: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bGold[ _]Master\b"),            "motor / sistema canonico"),
    (re.compile(r"\bSIAP-?ICPI\b"),                "—"),
    (re.compile(r"\bOUTPUT_API\b"),                "—"),
    (re.compile(r"\bv[56]\.\d\b"),                 "QUIRA Intelligence v1.0"),
    (re.compile(r"\bH\d{2}[a-z]?\b"),              "Fuente publica (SIGEF/SERCOP/CPCCS)"),
    (re.compile(r"\bICPI\b"),                      "Cumplimiento institucional"),
    (re.compile(r"\bTGI\b"),                       "Gobernanza territorial"),
    (re.compile(r"\bIGP\b"),                       "Participacion ciudadana"),
    (re.compile(r"\bPSG\b"),                       "Presupuesto con enfoque de genero"),
    (re.compile(r"\bISP\b"),                       "Salud presupuestaria"),
    (re.compile(r"\bIED\b"),                       "Eficiencia directiva"),
    (re.compile(r"\bIOC\b"),                       "Opacidad informativa"),
    (re.compile(r"\bIET\b"),                       "Equidad territorial"),
    (re.compile(r"\b(?:IFE|ITAM|IPE|IEFR|MMP)\b"), "—"),
    (re.compile(r"\bQTMP\b"),                      "—"),
    (re.compile(r"\bQNKC\b"),                      "—"),
    (re.compile(r"\bSAT-?(?:I{1,3}|\d+)?\b"),      "Alerta de reincidencia"),
    (re.compile(r"\bSupabase\b"),                  "registros institucionales"),
    (re.compile(r"\bNeo4j\b"),                     "—"),
    (re.compile(r"\bdemo_data\b"),                 "—"),
    (re.compile(r"\bgm_snapshot\b"),               "—"),
    (re.compile(r"\bdata\.loader\b"),              "—"),
]

_BARE = re.compile(r"^[A-Za-z0-9_\-\.]+$")


def _docstring_ids(tree: ast.AST) -> set[int]:
    """ids de los nodos Constant que son docstrings (capa interna · no se escanean)."""
    out: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                out.add(id(body[0].value))
    return out


def scan_file(path: Path) -> list[dict]:
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [{"line": exc.lineno or 0, "terms": "SYNTAX-ERROR", "alt": "—",
                 "risk": "ERROR", "snippet": str(exc)}]
    docs = _docstring_ids(tree)
    hits: list[dict] = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Constant) and isinstance(node.value, str)):
            continue
        if id(node) in docs:
            continue
        s = node.value
        found: list[tuple[str, str]] = []
        for rx, alt in PROHIBITED:
            m = rx.search(s)
            if m:
                found.append((m.group(0), alt))
        if not found:
            continue
        terms = ", ".join(dict.fromkeys(t for t, _ in found))
        alt   = found[0][1]
        bare  = len(s.strip()) <= 14 and _BARE.match(s.strip()) is not None
        risk  = "BAJO" if bare else "ALTO"
        snip  = s if len(s) <= 72 else s[:69] + "..."
        hits.append({"line": node.lineno, "terms": terms, "alt": alt,
                     "risk": risk, "snippet": snip.replace("\n", " ").strip()})
    return hits


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # consola Windows = cp1252
    except Exception:
        pass
    root  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("quira_pages")
    files = sorted(root.glob("*.py"))
    report: dict[str, list[dict]] = {}
    tot_alto = tot_bajo = 0
    for f in files:
        hits = scan_file(f)
        if hits:
            report[f.name] = hits
            tot_alto += sum(1 for h in hits if h["risk"] == "ALTO")
            tot_bajo += sum(1 for h in hits if h["risk"] == "BAJO")

    print(f"# FIREWALL DEBT REPORT — {root}/")
    print(f"# {len(files)} archivos · {len(report)} con hits · "
          f"VISIBLES(ALTO)={tot_alto} · clave-interna(BAJO)={tot_bajo}\n")
    ranked = sorted(report.items(),
                    key=lambda kv: -sum(1 for h in kv[1] if h["risk"] == "ALTO"))
    for fname, hits in ranked:
        alto = sum(1 for h in hits if h["risk"] == "ALTO")
        if alto == 0:
            continue  # en la consola priorizamos lo VISIBLE; el BAJO queda en el JSON
        print(f"## {fname}   ALTO={alto}")
        for h in sorted(hits, key=lambda x: (x["risk"] != "ALTO", x["line"])):
            if h["risk"] != "ALTO":
                continue
            print(f"   L{h['line']:<4} [{h['terms']:<18}] {h['snippet']}")
        print()

    only_bajo = [f for f, hs in report.items() if all(h["risk"] != "ALTO" for h in hs)]
    if only_bajo:
        print(f"# Solo clave-interna (BAJO · sin fugas visibles): {', '.join(sorted(only_bajo))}")
    Path("firewall_debt.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n# JSON completo -> firewall_debt.json")


if __name__ == "__main__":
    main()
