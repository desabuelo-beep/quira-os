#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ci/check_health.py — Guardián de salud QUIRA (CI/CD)
Dylus Lab © 2026

Corre en GitHub Actions en cada push/PR. Rápido (~segundos), SIN credenciales,
SIN conectar a Neo4j ni al Excel. Supabase: sólo el paso 6, en LECTURA, y sólo donde
hay credenciales locales; en CI no las hay y ese tramo es «no determinable».
Protege lo que importa:

  1. PRESUPUESTO DE CONTEXTO — CLAUDE.md y BOOT.md no deben volver a inflarse
     (la causa del problema de "chats que mueren"). Límites duros.
  2. SECRETOS — ningún archivo con credenciales puede llegar al repo
     (.env.claude, secrets.toml, URIs de DB, claves API).
  3. SINTAXIS PYTHON — todos los scripts deben compilar.
  4. INTEGRIDAD DE REFERENCIAS — los archivos que BOOT.md manda a leer existen.

Salida: exit 0 si todo OK, exit 1 si alguna verificación crítica falla.

Uso local:  python scripts/ci/check_health.py

CIRCUITO: OBLIGATORIO — protege: arranque legible, secretos, sintaxis, referencias y una cadena de autoridad al día con el disco (Carta de Gobernanza Art. 1) · integridad
"""
# ---
# authority:
#   parent: GOVERNANCE-001
#   constitution_articles: [1, 5, 9]
#   type: OPERATIVA
# ---

from __future__ import annotations

import re
import sys
# La consola de Windows abre en cp1252 y este gate imprime flechas y viñetas.
# Sin esto revienta con UnicodeEncodeError DESPUÉS de calcular sus resultados:
# un gate que muere al informar es un gate que no informa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ── LÍMITES DE PRESUPUESTO DE CONTEXTO (bytes) ────────────────────────────────
#
# ⚠️ RECALIBRADO 2026-09-09, y el motivo queda escrito porque
# `test_el_tope_de_boot_sigue_siendo_una_decision_y_no_un_estorbo` obliga a
# pasar por aquí — hizo exactamente su trabajo.
#
# ⛔ CORRECCIÓN DE UNA ATRIBUCIÓN FALSA: se dijo que estos topes «nacieron para
# ahorrar tokens». NO es cierto, y la propia prueba lo desmiente: *«el tope NO
# existe para ahorrar tokens — existe para FORZAR SÍNTESIS. Un BOOT de 20.000
# bytes nadie lo lee bien, y entonces deja de proteger.»* Ese razonamiento
# sigue vigente y no se deroga.
#
# POR QUÉ SE SUBE IGUALMENTE, y no es «no encontré qué recortar»:
# la dirección ordenó que el arranque incluya `QUIRA_MASTER_INDEX` —«¿dónde
# vive la verdad?»— tras medir que su omisión costó una sesión reconstruyendo
# con `grep` lo que ya era canon. Esa instrucción NO es doctrina migrable a
# `doctrina.py`: es la instrucción de arranque, y tiene que estar donde se
# arranca. Con 6000 la presión ya no producía síntesis sino CRIPTOGRAFÍA
# —`SITA 26(1-5) 0,8382 vig · 25→D-015`—, que es la otra forma de dejar de
# proteger.
#
#     el techo protege la LEGIBILIDAD del arranque, en sus dos extremos:
#     ni tan largo que no se lea, ni tan comprimido que no se entienda.
#
# 7000 conserva la presión de síntesis. Lo que no quepa se ROUTEA desde el
# índice; no se borra ni se cifra.
CONTEXT_BUDGET = {
    "CLAUDE.md":              4500,   # guía canónica + ruta al índice
    ".claude/CLAUDE.md":       500,   # solo punteros de skills
    "governance/BOOT.md":     7000,   # estado vivo · legible, no comprimido
    "governance/QUIRA_STATE.md": 1500,  # stub redirector (no contenido)
}

# ── PATRONES DE SECRETOS (nunca deben aparecer en archivos versionados) ───────
SECRET_PATTERNS = [
    (r"postgresql://[^\s\"']+:[^\s\"'@]+@", "URI PostgreSQL con password"),
    (r"sk-ant-[a-zA-Z0-9\-]{20,}",          "clave API Anthropic"),
    (r"neo4j\+s://[^\s\"']+:[^\s\"']+@",    "URI Neo4j con credenciales"),
    (r"eyJ[A-Za-z0-9_\-]{30,}\.[A-Za-z0-9_\-]{30,}", "JWT / service_role key"),
]

# Archivos que NUNCA deben estar trackeados por git
FORBIDDEN_FILES = [
    ".env.claude",
    ".streamlit/secrets.toml",
    ".env",
]

# Archivos del lazy-load de BOOT que deben existir (integridad de referencias)
# Se extraen dinámicamente, pero verificamos los críticos siempre.
CRITICAL_REFS = [
    "docs/adr/ADR-023_Arquitectura_Tres_Niveles_QUIRA.md",
    "docs/architecture/BRIDGE_EXCEL_CORPUS.md",
    "app/connectors/gold_master.py",
]


def check_context_budget() -> list[str]:
    errors = []
    print("\n[1/4] Presupuesto de contexto (arranque liviano)")
    for rel, limit in CONTEXT_BUDGET.items():
        path = ROOT / rel
        if not path.exists():
            print(f"   - {rel}: no existe (omitido)")
            continue
        size = path.stat().st_size
        status = "OK" if size <= limit else "EXCEDE"
        marker = "  " if size <= limit else ">>"
        print(f"   {marker} {rel}: {size} / {limit} bytes [{status}]")
        if size > limit:
            errors.append(
                f"{rel} pesa {size} bytes (límite {limit}). "
                f"El arranque vuelve a inflarse — mover detalle a lazy-load."
            )
    return errors


# Placeholders de documentación — un match que los contenga NO es secreto real
PLACEHOLDER_MARKERS = [
    "TU-PROYECTO", "tu-proyecto", "xxx", "XXX", "[PASSWORD]", "[PASS]",
    "example", "EXAMPLE", "ejemplo", "your-", "YOUR-", "<", "...",
    "PROJECT-REF", "REGION", "password@", "PASSWORD@",
]


def _git_tracked_files() -> list[Path]:
    """Archivos que git realmente rastrea. Excluye gitignoreados (secrets.toml, .env.claude)."""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        return [ROOT / line for line in r.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def check_no_secrets() -> list[str]:
    errors = []
    print("\n[2/4] Fuga de secretos (solo archivos rastreados por git)")

    tracked = _git_tracked_files()
    if not tracked:
        print("   - git ls-files no disponible — omitido (se valida en CI)")
        return errors

    # 1. Archivos prohibidos NO deben estar rastreados
    tracked_rel = {str(p.relative_to(ROOT)).replace("\\", "/") for p in tracked}
    for rel in FORBIDDEN_FILES:
        if rel in tracked_rel:
            errors.append(f"ARCHIVO SECRETO RASTREADO POR GIT: {rel}")
            print(f"   >> {rel}: RASTREADO (CRÍTICO)")
    print(f"   OK — ninguno de {FORBIDDEN_FILES} está rastreado")

    # 2. Patrones de secreto SOLO en archivos rastreados (lo que va al repo)
    scan_ext = {".py", ".md", ".json", ".yml", ".yaml", ".toml", ".txt"}
    hits = 0
    for path in tracked:
        if path.suffix.lower() not in scan_ext:
            continue
        if path.name == "check_health.py":  # este archivo contiene los patrones
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pattern, label in SECRET_PATTERNS:
            for m in re.finditer(pattern, text):
                snippet = m.group(0)
                # Ignorar si el match es claramente un placeholder de documentación
                if any(marker in snippet for marker in PLACEHOLDER_MARKERS):
                    continue
                errors.append(f"SECRETO REAL ({label}) en {path.relative_to(ROOT)}")
                print(f"   >> {path.relative_to(ROOT)}: {label}")
                hits += 1
    if hits == 0:
        print("   OK — sin secretos reales (placeholders de docs ignorados)")
    return errors


def _version_de_ci() -> tuple[int, int] | None:
    """La versión de Python que CI usa, LEÍDA del workflow — no copiada aquí.

    Si se escribiera a mano, sería una copia que se queda atrás en cuanto el
    workflow cambie: el patrón que produjo el «48,33 %». Se deriva."""
    wf = ROOT / ".github" / "workflows" / "quira-health.yml"
    if not wf.exists():
        return None
    m = re.search(r'python-version:\s*"?(\d+)\.(\d+)"?',
                  wf.read_text(encoding="utf-8", errors="replace"))
    return (int(m.group(1)), int(m.group(2))) if m else None


def check_python_syntax() -> list[str]:
    """Compila con la versión de CI, no con la del intérprete que corre.

    ⚠️ NACIÓ DE UN FALLO REAL (2026-09-02). El primer CI tras enganchar los
    gates falló con tres `SyntaxError` que en local NO existían: `login_view`,
    `p_gestion` y `p_alertas` usaban un backslash dentro de la expresión de una
    f-string. PEP 701 lo permite desde 3.12; el runner usa 3.11 y lo rechaza.

        local (3.13)  →  verde
        CI    (3.11)  →  rojo, y una de las tres es la pantalla de acceso

    El gate decía la verdad sobre el Python que lo ejecutaba, y esa verdad no
    era la que importaba. `compile(..., _feature_version=N)` permite comprobar
    la versión de destino desde cualquier intérprete moderno.

    Si `_feature_version` no está disponible —es API privada de CPython— NO se
    finge la comprobación: se cae a la versión del intérprete y se DICE, porque
    un chequeo degradado en silencio es peor que uno ausente."""
    errors = []
    destino = _version_de_ci()
    print("\n[3/4] Sintaxis Python")

    modo = f"contra Python {destino[0]}.{destino[1]} (el de CI)" if destino else \
           f"contra {sys.version_info.major}.{sys.version_info.minor} (local)"
    py_files = [
        p for p in ROOT.rglob("*.py")
        if not (set(p.parts) & {".venv", "venv", "node_modules", "__pycache__", "historico"})
    ]
    bad = 0
    degradado = False
    for p in py_files:
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except Exception:                                    # noqa: BLE001
            continue
        try:
            if destino:
                compile(src, str(p), "exec", _feature_version=destino[1])
            else:
                compile(src, str(p), "exec")
        except TypeError:            # `_feature_version` no existe en este intérprete
            degradado = True
            destino = None
            try:
                compile(src, str(p), "exec")
            except SyntaxError as e:
                errors.append(f"Error de sintaxis: {p.relative_to(ROOT)} — {e.msg} (L{e.lineno})")
                print(f"   >> {p.relative_to(ROOT)}")
                bad += 1
        except SyntaxError as e:
            errors.append(f"Error de sintaxis: {p.relative_to(ROOT)} — {e.msg} (L{e.lineno})")
            print(f"   >> {p.relative_to(ROOT)}")
            bad += 1

    if degradado:
        print("   [--] no se pudo fijar la versión de destino: se comprobó contra "
              "el intérprete local, y eso NO acredita el runtime de CI")
    print(f"   {'OK' if bad == 0 else '>>'} — {len(py_files)} archivos, {bad} con "
          f"error · {modo}")
    return errors


def check_references() -> list[str]:
    errors = []
    print("\n[4/4] Integridad de referencias críticas")
    for rel in CRITICAL_REFS:
        path = ROOT / rel
        if path.exists():
            print(f"   OK — {rel}")
        else:
            errors.append(f"Referencia crítica faltante: {rel}")
            print(f"   >> {rel}: NO EXISTE")
    return errors


def check_registry() -> list[str]:
    """[5/5] Cumplimiento del Principio de Derivación (Carta de Gobernanza Art. 1 y 6).

    El gate VERIFICA ESTADOS, no interpreta filosofía. Es la extensión del gate
    existente — no un componente paralelo (Carta Art. 4.7, anti-inflación).
    """
    errors: list[str] = []
    print("\n[5/5] Cadena de autoridad (Carta de Gobernanza Art. 1)")
    reg = ROOT / "registry" / "registry.yaml"
    if not reg.exists():
        print("   >> registry/registry.yaml NO EXISTE — ejecutar build_registry.py")
        return ["Registry ausente: el Principio de Derivación no puede verificarse"]

    txt = reg.read_text(encoding="utf-8", errors="replace")
    total = int(re.search(r"^total_activos:\s*(\d+)", txt, re.M).group(1))
    huerfanos = int(re.search(r"^huerfanos:\s*(\d+)", txt, re.M).group(1))
    con_autoridad = total - huerfanos
    pct = round(100 * con_autoridad / max(total, 1), 1)

    # 1 · ¿hay artefactos sin autoridad declarada?
    print(f"      activos registrados : {total}")
    print(f"      declaran autoridad  : {con_autoridad} ({pct}%)")
    if huerfanos:
        print(f"   >> HUÉRFANOS: {huerfanos} — no promovibles a vigente (Art. 1)")
        errors.append(f"{huerfanos} artefacto(s) sin declarar autoridad (Carta Art. 1)")
    else:
        print("      OK — todo artefacto declara su autoridad")

    # 2 · ¿la cadena es reconstruible? (aristas rotas = padre inexistente)
    graph = ROOT / "registry" / "authority_graph.json"
    if graph.exists():
        import json as _json
        g = _json.loads(graph.read_text(encoding="utf-8"))
        rotas = g.get("aristas_rotas", 0)
        fuera = g.get("aristas_fuera_de_catalogo", 0)
        if rotas:
            print(f"   >> {rotas} arista(s) rota(s): padre declarado inexistente")
            errors.append(f"{rotas} cadena(s) de autoridad no reconstruible(s) hasta la Constitución")
        else:
            print(f"      OK — cadena reconstruible ({g.get('total_aristas', 0)} aristas, 0 rotas)")
        if fuera:
            # No es un fallo: el padre EXISTE, en el hueco de alcance que el
            # registro declara. Pero el verde no lo cubre, y se dice.
            print(f"      ⚠️  {fuera} arista(s) hacia canon fuera de catálogo — "
                  "el verde NO las cubre")

    # 3 · ¿el Registry está al día con el disco?
    #
    # ⛔ Este paso se llamaba «¿el Registry está al día con el disco? (hash de un
    # centinela)» y sólo comprobaba que la Constitución EXISTIERA. El rótulo
    # prometía frescura; el mecanismo verificaba existencia. Resultado medido
    # (2026-09-14): registro de 2026-08-12, grafo de 2026-07-27, 29 activos fuera
    # —toda la familia normativa de Transparencia entre ellos— y cinco aristas
    # rotas invisibles, mientras este gate imprimía «100 %».
    # Ahora se relee el disco con el MISMO escáner que escribe el registro.
    frozen = ROOT / "identity" / "CONSTITUCION_INSTITUCIONAL.md"
    if not frozen.exists():
        errors.append("Constitución Institucional ausente: la raíz de autoridad no existe")
        print("   >> identity/CONSTITUCION_INSTITUCIONAL.md NO EXISTE")
    errors += _registro_al_dia(txt, graph)
    return errors


def _registro_al_dia(registro_txt: str, graph: Path) -> list[str]:
    """Compara lo que el registro AFIRMA con lo que el disco dice HOY.

    Falla por lo que el gate certifica —qué activos existen y de quién cuelgan—.
    Un hash desactualizado sin cambio de cadena se informa y no bloquea: la
    cadena de autoridad no depende del contenido, y exigir regenerar el registro
    por cada edición de prosa convertiría el gate en ruido."""
    sys.path.insert(0, str(ROOT / "scripts" / "governance"))
    try:
        import build_registry  # stdlib-only: corre antes de instalar dependencias
    except Exception as exc:  # noqa: BLE001
        return [f"no se pudo releer el disco para verificar el registro: {exc}"]

    activos, _ = build_registry.escanear()
    disco = {(a["id"], a["path"], a["parent"] or "null", str(a["authority_declared"]).lower())
             for a in activos}
    hashes_disco = {a["path"]: a["hash"] for a in activos}

    registrado, hashes_reg, cur = set(), {}, {}
    for linea in registro_txt.split("\nexternos:")[0].splitlines():
        s = linea.strip()
        if s.startswith("- id:"):
            cur = {"id": s.split(":", 1)[1].strip()}
        elif ":" in s and cur:
            k, _, v = s.partition(":")
            cur[k.strip()] = v.strip()
            if k.strip() == "parent":
                registrado.add((cur["id"], cur.get("path", ""), cur["parent"],
                                cur.get("authority_declared", "")))
                hashes_reg[cur.get("path", "")] = cur.get("hash", "")

    errores = []
    nuevos, retirados = disco - registrado, registrado - disco
    if nuevos or retirados:
        print(f"   >> REGISTRO DESACTUALIZADO: {len(nuevos)} activo(s) en disco no registrados · "
              f"{len(retirados)} registrado(s) que ya no son así")
        for ident, ruta, *_ in sorted(nuevos)[:8]:
            print(f"        + {ident}  ({ruta})")
        errores.append("registry.yaml no refleja el disco — ejecutar "
                       "scripts/governance/build_registry.py y build_authority_graph.py")
    else:
        cambiados = sum(1 for r, h in hashes_disco.items() if hashes_reg.get(r) not in ("", h))
        print(f"      OK — registro al día con el disco ({len(disco)} activos)"
              + (f" · {cambiados} con contenido editado desde la generación" if cambiados else ""))

    if graph.exists():
        import json as _json
        nodos = {n["id"] for n in _json.loads(graph.read_text(encoding="utf-8")).get("nodes", [])}
        ids_reg = {r[0] for r in registrado}
        if nodos != ids_reg:
            print(f"   >> GRAFO DESACTUALIZADO: {len(nodos)} nodos frente a {len(ids_reg)} activos registrados")
            errores.append("authority_graph.json no refleja el registro — ejecutar "
                           "scripts/governance/build_authority_graph.py")
    return errores


def check_citas() -> list[str]:
    """[6/6] Citas normativas contra el corpus.

    Nace de la falsación 43 (PANORAMA §5-duoquinquagies/terquinquagies): se citaban
    artículos de memoria —textos que la ley no dice, números que no existen—. Sin
    corpus (CI) el estado es «no determinable» y no bloquea; en local, una huella mal
    atribuida o un artículo inexistente bloquea el cierre."""
    print("\n[6/6] Citas normativas: integridad documental (no autoridad normativa)")
    sys.path.insert(0, str(ROOT / "scripts" / "normativa"))
    try:
        import verificar_citas as vc
        g = vc.auditar_gate()
    except Exception as exc:  # noqa: BLE001
        print(f"   2 — no determinable: {exc.__class__.__name__}")
        return []
    errores = list(g["hallazgos"]) + list(g["fuera_nuevas"])
    print(f"      universo: {g['archivos']} archivos")
    if g["corpus"]:
        print(f"      huella · existencia · literal: {len(g['hallazgos'])} hallazgo(s) · "
              f"{g['literales']} cita(s) literal(es) verificada(s) contra el artículo")
        print(f"      ⚠️  {g['no_verificadas']} cita(s) con huella SIN texto literal: se verifica "
              "que el artículo es el citado, NO su contenido (validación humana)")
    else:
        print("      huella · existencia · literal: 2 — no determinable (sin corpus)")
    if g["cadena"]:
        print(f"      cadena rectora (disparador léxico · sin cobertura universal): "
              f"{len(g['fuera_nuevas'])} fuera de cadena sin declarar · {g['fuera_en_base']} en la "
              "línea base (inventario histórico, no aprobación)")
    else:
        print("      cadena rectora: 2 — no determinable (sin la BRN legible)")
    if errores:
        print(f"   >> {len(errores)} cita(s) bloquean el cierre")
        for e in errores[:10]:
            print(f"        {e[:220]}")
    return errores


def main() -> int:
    print("=" * 60)
    print("  QUIRA Health Check — guardián de arranque + secretos")
    print("=" * 60)

    all_errors = []
    all_errors += check_context_budget()
    all_errors += check_no_secrets()
    all_errors += check_python_syntax()
    all_errors += check_references()
    all_errors += check_registry()
    all_errors += check_citas()

    print("\n" + "=" * 60)
    if all_errors:
        print(f"  FALLO — {len(all_errors)} problema(s):")
        for e in all_errors:
            print(f"    - {e}")
        print("=" * 60)
        return 1
    print("  TODO OK — arranque liviano, sin secretos, sintaxis válida")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
