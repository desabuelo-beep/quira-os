"""
app/agents/acoplamiento.py — CAPA 2 · P6/P7 · qué artefactos toca de verdad el código
================================================================================
POR QUÉ NO ES UN GRAFO DE IMPORTS (colega, 2026-08-31):

> *«No construyamos un "grafo de imports". Construyamos un grafo de acoplamiento
> observable. Los imports pueden ser una de sus fuentes, pero no la definición
> del grafo.»*

Y tiene razón por una consecuencia concreta en este sistema: los acoplamientos
que más importan **no son imports**. `d09` carga su enricher con
`importlib.util.spec_from_file_location`; `d07` abre YAML del BRN; los motores
leen `gm_snapshot.json` y el Gold Master. Un análisis de `import` no vería nada
de eso, y sí vería `pathlib` — que no es una dependencia arquitectónica.

    LA PREGUNTA NO ES «¿está mal?» SINO **«¿está declarado?»**

Cuatro respuestas, no dos, porque colapsarlas convertiría una divergencia en una
acusación:

    declarado_y_observable   el código lo usa y la arquitectura lo declara
    no_declarado             el código lo usa y nadie lo documentó
    declarado_sin_evidencia  la documentación lo declara y no se observa uso
    no_determinable          la ruta no se resuelve estáticamente

⚠️ EL ÚLTIMO ES EL IMPORTANTE. **No detectar una lectura no significa que no
exista una lectura.** Si el código construye la ruta con una variable, un
f-string o una función auxiliar, el analizador no puede resolverla — y eso debe
APARECER como `no_determinable`, no desaparecer del grafo. Un acoplamiento
invisible es peor que uno no declarado: el segundo se ve.

QUÉ NO DECIDE ESTE MÓDULO. Un acoplamiento no declarado todavía no es una
infracción. Puede ser deuda de arquitectura, dependencia legítima omitida,
arquitectura antigua que sobrevivió en código, implementación accidental o falso
positivo del análisis. Eso se decide después, con evidencia y gobernanza — aquí
sólo se observa.

Dylus Lab © 2026
"""
from __future__ import annotations

import ast
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

DECLARADO = "declarado_y_observable"
NO_DECLARADO = "no_declarado"
SIN_EVIDENCIA = "declarado_sin_evidencia"
NO_DETERMINABLE = "no_determinable"

LECTURA = "lectura"
ESCRITURA = "escritura"
CARGA_DE_MODULO = "carga_de_modulo"

# Operaciones que acoplan el código a un artefacto externo. Se detectan por AST
# —no por texto— porque el nombre de una función en un comentario no es una
# llamada, y esa distinción ya costó cuatro falsos positivos hoy.
#
# ⚠️ CADA OPERACIÓN DECLARA **DÓNDE LLEVA LA RUTA**, y esto fue un defecto real
# de la primera versión: asumí que la ruta era «el primer argumento string» y el
# grafo se llenó de basura — contenidos de archivos como artefactos, el modo
# `"a"` de `open`, el `encoding` `cp850`, el nombre de módulo de
# `spec_from_file_location`. Todo eran strings, ninguno era una ruta.
#
#   arg0 / arg1   la ruta viaja como argumento en esa posición
#   receptor      `Path(x).read_text()` — la ruta está en el objeto, no en args
#
# `yaml.safe_load(f)` y `json.load(f)` quedan FUERA a propósito: reciben un
# descriptor ya abierto, así que no aportan destino. El acoplamiento real lo
# produjo el `open` que los alimenta, y contarlos duplicaría la arista o, peor,
# le inventaría un destino falso.
_OPERACIONES = {
    "open": (LECTURA, "arg0"),
    "read_text": (LECTURA, "receptor"), "read_bytes": (LECTURA, "receptor"),
    "write_text": (ESCRITURA, "receptor"), "write_bytes": (ESCRITURA, "receptor"),
    "load_workbook": (LECTURA, "arg0"),
    "read_csv": (LECTURA, "arg0"), "read_excel": (LECTURA, "arg0"),
    "read_json": (LECTURA, "arg0"), "Document": (LECTURA, "arg0"),
    "spec_from_file_location": (CARGA_DE_MODULO, "arg1"),
}

_EXCLUIDOS = (
    (".claude", "copias de trabajo y configuración del entorno, no del sistema"),
    ("node_modules", "dependencias externas"),
    ("__pycache__", "artefactos de compilación"),
    (".agents", "herramientas de asistencia, no código de QUIRA"),
    ("app/agents/acoplamiento.py", "este módulo se excluye a sí mismo: nombra "
                                   "operaciones de acoplamiento en su tabla y se "
                                   "contaría como acoplado a todo lo que mide"),
)


def _literal(nodo: ast.AST, constantes: dict[str, str]) -> tuple[str, bool]:
    """Intenta resolver una ruta estáticamente. Devuelve `(valor, resuelto)`.

    Resuelve literales y constantes de módulo con valor literal. **No inventa**:
    una ruta armada con variables, f-strings o llamadas devuelve `resuelto=False`
    y el acoplamiento entra al grafo como `no_determinable` — visible, sin valor."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        return nodo.value, True
    if isinstance(nodo, ast.Name) and nodo.id in constantes:
        return constantes[nodo.id], True
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Div):
        # `RAIZ / "docs" / "brn"` — LA FORMA DOMINANTE EN QUIRA, y sin resolverla
        # el grafo era ciego al 98% del sistema. No es un defecto del código: el
        # sistema tiene trinquete en **0 rutas fijas** (gate REGLAS · BOOT), así
        # que las rutas se componen a partir de una raíz. Un analizador que sólo
        # entiende literales mide bien un sistema mal construido, y mal uno bien
        # construido.
        izq, ok_i = _literal(nodo.left, constantes)
        der, ok_d = _literal(nodo.right, constantes)
        if ok_i and ok_d:
            return (f"{izq}/{der}".lstrip("/") if izq else der), True
        return "", False
    if isinstance(nodo, ast.JoinedStr):
        return "", False
    if isinstance(nodo, ast.Call):
        nombre = (nodo.func.attr if isinstance(nodo.func, ast.Attribute)
                  else getattr(nodo.func, "id", ""))
        if nombre == "join":
            # `os.path.join(a, "..", "data", "x.json")`: se unen los tramos y se
            # admite la derrota si alguno no resuelve — media ruta es una ruta
            # falsa, y una ruta falsa es peor que un `no_determinable`.
            tramos = []
            for arg in nodo.args:
                v, ok = _literal(arg, constantes)
                if not ok:
                    return "", False
                tramos.append(v)
            return "/".join(tramos), True
        if nombre in ("Path", "str"):
            return _literal(nodo.args[0], constantes) if nodo.args else ("", False)
        return "", False
    if isinstance(nodo, ast.Attribute):
        return "", False
    return "", False


def _constantes_de(arbol: ast.Module) -> dict[str, str]:
    """Constantes de módulo con valor literal — el caso común de `EXCEL = "..."`."""
    out: dict[str, str] = {}
    for n in arbol.body:
        if not (isinstance(n, ast.Assign) and len(n.targets) == 1):
            continue
        t = n.targets[0]
        if not isinstance(t, ast.Name):
            continue
        # Raíces del repositorio: `RAIZ = Path(__file__).resolve().parents[2]`.
        # Se DERIVAN del patrón, no se listan por nombre — llamarla `RAIZ`,
        # `_ROOT` o `REPO` da igual; lo que la identifica es cómo se calcula.
        if _es_raiz_de_repo(n.value):
            out[t.id] = ""
            continue
        v, ok = _literal(n.value, out)
        if ok and v:
            out[t.id] = v
    return out


def _es_raiz_de_repo(nodo: ast.AST) -> bool:
    """`Path(__file__).resolve().parents[N]` — la raíz, se llame como se llame."""
    txt = ast.dump(nodo)
    return "__file__" in txt and "parents" in txt


@lru_cache(maxsize=1)
def grafo() -> list[dict]:
    """Los acoplamientos observables del repositorio, uno por llamada."""
    aristas: list[dict] = []
    for f in sorted(RAIZ.rglob("*.py")):
        rel = f.relative_to(RAIZ).as_posix()
        if any(p in rel for p, _ in _EXCLUIDOS):
            continue
        try:
            arbol = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        constantes = _constantes_de(arbol)
        for n in ast.walk(arbol):
            if not isinstance(n, ast.Call):
                continue
            nombre = (n.func.attr if isinstance(n.func, ast.Attribute)
                      else getattr(n.func, "id", ""))
            if nombre not in _OPERACIONES:
                continue
            tipo, donde = _OPERACIONES[nombre]
            # `open(ruta, "rb")` y `ruta.open("rb")` son la MISMA operación con
            # la ruta en sitios opuestos. Sin distinguirlas, el grafo registraba
            # los modos de apertura —«a», «r», «rb», «w»— como si fueran
            # artefactos del sistema.
            if nombre == "open" and isinstance(n.func, ast.Attribute):
                donde = "receptor"

            # La ruta se busca DONDE la operación la lleva, no en el primer
            # string que aparezca. Ese atajo llenó el grafo de contenidos de
            # archivo y modos de apertura.
            if donde == "receptor":
                fuente = n.func.value if isinstance(n.func, ast.Attribute) else None
            else:
                i = int(donde[-1])
                fuente = n.args[i] if len(n.args) > i else None
            destino, resuelto = _literal(fuente, constantes) if fuente is not None else ("", False)
            aristas.append({
                "desde": rel, "operacion": nombre, "tipo": tipo,
                "hacia": destino if resuelto else "",
                "resuelto": bool(resuelto and destino),
                "linea": n.lineno,
            })
    return aristas


@lru_cache(maxsize=1)
def _declarado_en_documentacion() -> set[str]:
    """Rutas de artefacto que la documentación nombra en alguna parte."""
    textos = []
    for patron in ("*.md", "docs/**/*.md", "governance/*.md", "identity/*.md"):
        for f in RAIZ.glob(patron):
            if ".claude" in f.as_posix():
                continue
            textos.append(f.read_text(encoding="utf-8", errors="replace"))
    todo = "\n".join(textos)
    return {a["hacia"] for a in grafo()
            if a["resuelto"] and a["hacia"] and a["hacia"] in todo}


def artefactos() -> list[dict]:
    """Cada artefacto tocado, con su estado respecto de la arquitectura."""
    declarados = _declarado_en_documentacion()
    por_destino: dict[str, dict] = {}
    for a in grafo():
        if not a["resuelto"]:
            continue
        d = por_destino.setdefault(a["hacia"], {
            "artefacto": a["hacia"], "tocado_por": set(), "operaciones": set()})
        d["tocado_por"].add(a["desde"])
        d["operaciones"].add(a["tipo"])
    salida = []
    for k, d in sorted(por_destino.items()):
        salida.append({
            "artefacto": k,
            "estado": DECLARADO if k in declarados else NO_DECLARADO,
            "tocado_por": sorted(d["tocado_por"]),
            "operaciones": sorted(d["operaciones"]),
        })
    return salida


def cobertura_de_acoplamiento() -> dict:
    """El grafo con su universo y sus límites (Capa 0 lo exige)."""
    g = grafo()
    sin_resolver = [a for a in g if not a["resuelto"]]
    arts = artefactos()
    no_declarados = [a for a in arts if a["estado"] == NO_DECLARADO]
    return {
        "aristas": len(g),
        "artefactos": arts,
        "no_declarados": [a["artefacto"] for a in no_declarados],
        "no_determinables": len(sin_resolver),
        "modulos_con_ruta_no_resoluble": sorted({a["desde"] for a in sin_resolver}),
        "universo": {
            "que": "operaciones de acoplamiento a artefactos externos "
                   "(lectura · escritura · carga de módulo)",
            "donde": "todos los `*.py` del repositorio",
            "como": "análisis del AST — no de texto: el nombre de una función en "
                    "un comentario no es una llamada",
            "hallados": len(g),
            "mecanismo": {
                "tipo": "derivado",
                "operacion": "rglob",
                "por_que": "se recorre el repositorio y se analiza cada árbol "
                           "sintáctico; ninguna lista enumera los módulos",
            },
            "exclusiones": [
                {"patron": p, "motivo": m,
                 "autoridad": "decisión de alcance de este módulo, revisable"}
                for p, m in _EXCLUIDOS],
            "fuera_de_alcance": [
                f"{len(sin_resolver)} llamadas cuya ruta NO se resuelve "
                f"estáticamente —variables, f-strings, funciones auxiliares—: "
                f"están en el grafo como no_determinable, porque no detectar una "
                f"lectura no significa que no exista",
                "acoplamientos por red o base de datos: no son artefactos de ruta",
                "operaciones fuera de la tabla `_OPERACIONES`: si el sistema "
                "empieza a leer de otra forma, este grafo no la verá",
                "que la documentación nombre una ruta no dice que la declare "
                "como arquitectura — sólo que la menciona",
            ],
        },
        "afirmacion_sostenible": _afirmar(g, arts, no_declarados, sin_resolver),
    }


def _afirmar(g, arts, no_declarados, sin_resolver) -> str:
    return (
        f"Se observan {len(g)} operaciones de acoplamiento sobre "
        f"{len(arts)} artefactos con ruta resoluble; {len(no_declarados)} de esos "
        f"artefactos no aparecen nombrados en la documentación. "
        f"⚠️ Otras {len(sin_resolver)} operaciones construyen su ruta de forma no "
        f"resoluble estáticamente: **no se sabe qué tocan**, y eso no es lo mismo "
        f"que no tocar nada — es el límite del método, no una ausencia de "
        f"acoplamiento. No se afirma que lo no declarado esté mal: puede ser "
        f"deuda, arquitectura antigua o falso positivo, y decidirlo exige "
        f"gobernanza, no análisis."
    )
