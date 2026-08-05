# -*- coding: utf-8 -*-
"""
check_epistemico — ¿cada afirmación ocupa el nivel que le corresponde? (Dylus Lab © 2026)

Nace del cierre epistemológico de d01 (2026-08-05). De las diez comprobaciones que la
asesoría propuso, CUATRO son búsquedas léxicas —inferencia, prescripción, alcance y
terminología—. Hacerlas a mano obliga a repetirlas en cada dominio nuevo; hechas aquí,
las hereda todo el que venga. Es el mismo principio que ya rige `firewall_audit.py`
(frontera de lenguaje) y el test de regresión del filtro ontológico: **el hallazgo se
convierte en verificación permanente, no en una lectura que hay que recordar**.

Las otras seis (clasificación de proveniencia, hipótesis, consistencia con ambas
Constituciones, flujo y cierre doctrinal) exigen juicio y NO se automatizan: quedan como
lectura humana. Este script no las sustituye — les despeja el camino.

QUÉ MIDE, y contra qué canon:
  1 · INFERENCIA   — verbos que afirman más de lo medido ("demuestra", "sabe", "confirma").
                     Carta Art. 4.5 · Principio de No-Inferencia.
  2 · PRESCRIPCIÓN — el sistema tomando la decisión ("debe", "hay que", "obligatorio").
                     Frontera de Javo (2026-06-21 · qinv.py): "la ACCIÓN la cierra el
                     GOBIERNO, FUERA de QUIRA: QUIRA informa y conecta, no actúa".
  3 · ALCANCE      — decir "la cadena" cuando el objeto observado es UN instrumento.
  4 · TERMINOLOGÍA — palabras que el canon usa con un significado propio y que aquí
                     aparecen con otro ("auditoría", "observatorio", "componentes").

NO BLOQUEA: mide y reporta, como firewall_audit. Muchos aciertos son legítimos —"porque"
introduce explicaciones válidas— y el juicio de cuáles no lo son es humano. Con
`--estricto` devuelve código 1 si hay señales, para usarlo como gate donde se quiera.

Capa: solo STRINGS LITERALES (lo que el usuario lee). Docstrings y comentarios son capa
interna y no se escanean — ahí explicar la regla exige nombrarla.

Uso:  python scripts/ci/check_epistemico.py [carpeta] [--estricto]
      (por defecto: app/viz/render — donde vive el texto de los cajones)
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]

# (patrón, categoría, por qué importa). Case-insensitive salvo donde el canon distingue.
SEÑALES: list[tuple[re.Pattern, str, str]] = [
    # ── 1 · INFERENCIA ────────────────────────────────────────────────────────
    (re.compile(r"\bdemuestra\b", re.I), "INFERENCIA", "¿está medido o se deduce?"),
    (re.compile(r"\bprueba que\b", re.I), "INFERENCIA", "afirma prueba, no medición"),
    (re.compile(r"\bconfirma\b", re.I), "INFERENCIA", "confirmar exige contraste previo"),
    (re.compile(r"\bpermite concluir\b", re.I), "INFERENCIA", "conclusión, no observación"),
    (re.compile(r"\b(el|la) (municipio|GAD|entidad) (sabe|puede|no puede|quiere)\b", re.I),
     "INFERENCIA", "atribuye capacidad o voluntad interna — nunca medida"),
    (re.compile(r"\brevela que\b", re.I), "INFERENCIA", "revelar = afirmar causa"),
    (re.compile(r"\bsignifica que\b", re.I), "INFERENCIA", "equivale a interpretar"),
    (re.compile(r"\bdebido a\b", re.I), "INFERENCIA", "atribución causal directa"),
    (re.compile(r"\bpor tanto\b", re.I), "INFERENCIA", "encadena deducción — revisar el salto"),
    # ── 2 · PRESCRIPCIÓN ──────────────────────────────────────────────────────
    (re.compile(r"\b(el|la) (municipio|GAD|entidad) deb[eí]", re.I), "PRESCRIPCION",
     "el sistema no ordena: informa y conecta"),
    (re.compile(r"\bhay que\b", re.I), "PRESCRIPCION", "instrucción directa"),
    (re.compile(r"\bes necesario que\b", re.I), "PRESCRIPCION", "instrucción encubierta"),
    (re.compile(r"\bse recomienda\b", re.I), "PRESCRIPCION", "la recomendación es del decisor"),
    (re.compile(r"\bdeberá\b", re.I), "PRESCRIPCION", "registro imperativo"),
    (re.compile(r"\bobligatori", re.I), "PRESCRIPCION", "¿lo obliga la ley, o lo propone el sistema?"),
    # ── 3 · ALCANCE ───────────────────────────────────────────────────────────
    (re.compile(r"\bla cadena (no se puede|no puede)\b", re.I), "ALCANCE",
     "la cadena existe; lo que falta son atributos para reconstruirla"),
    (re.compile(r"\bplan operativo \d{4}\s*[-–]\s*\d{4}", re.I), "ALCANCE",
     "el POA es ANUAL — un rango plurianual es el PDOT"),
    # ── 4 · TERMINOLOGÍA ──────────────────────────────────────────────────────
    (re.compile(r"\bauditor[ií]a\b", re.I), "TERMINOLOGIA",
     "QUIRA es infraestructura de conocimiento, no auditoría (CONSTITUCION-001)"),
    (re.compile(r"\bfiscaliza", re.I), "TERMINOLOGIA", "fiscalizar es competencia de otro órgano"),
    (re.compile(r"\bcertifica (que|el incumplimiento|la verdad)\b", re.I), "TERMINOLOGIA",
     "certifica VERIFICABILIDAD, nunca verdad ni incumplimiento"),
    (re.compile(r"\bcomponentes?\b", re.I), "TERMINOLOGIA",
     "en planificación designa los componentes del PDOT — ¿es ese el sentido?"),
    (re.compile(r"\b(incumpl|violó|ilegal|irregular)", re.I), "TERMINOLOGIA",
     "lenguaje acusatorio — prohibido (Regla 2)"),
]


def _literales(ruta: Path) -> list[tuple[int, str]]:
    """Strings literales del módulo — la capa que el usuario lee. Excluye docstrings."""
    try:
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    except SyntaxError:
        return []
    docstrings = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            cuerpo = getattr(nodo, "body", [])
            if (cuerpo and isinstance(cuerpo[0], ast.Expr)
                    and isinstance(cuerpo[0].value, ast.Constant)
                    and isinstance(cuerpo[0].value.value, str)):
                docstrings.add(id(cuerpo[0].value))
    out = []
    for nodo in ast.walk(arbol):
        if (isinstance(nodo, ast.Constant) and isinstance(nodo.value, str)
                and id(nodo) not in docstrings):
            out.append((nodo.lineno, nodo.value))
    return out


def _limpiar(s: str) -> str:
    """Quita etiquetas y entidades HTML: se juzga la PROSA, no el marcado."""
    return re.sub(r"&[a-z]+;", " ", re.sub(r"<[^>]+>", " ", s))


# El canon se escribe muchas veces EN NEGATIVO, y ahí el término prohibido es justamente
# lo correcto: "QUIRA no certifica la verdad", "no es una irregularidad", "no se computa
# como incumplimiento". La primera versión marcaba las 14 y dejaba 1 señal real entre el
# ruido — un gate que grita siempre es un gate que nadie mira. Se suprime el acierto
# cuando viene negado o atribuido a un tercero (la ley obliga; el analista confirma).
_NEGACION = re.compile(
    r"(?:\bno\b|\bnunca\b|\bsin\b|\bjamás\b|\bni\b)\s+(?:\w+\s+){0,3}$", re.I)
_ATRIBUIDO = re.compile(
    r"\b(la ley|la norma|el marco|la Constitución|COOTAD|LOPC|COPFP|un analista|"
    r"el analista|la autoridad|el órgano|la ciudadanía|el humano)\b[^.]{0,60}$", re.I)


def revisar(carpeta: Path) -> dict[str, list[tuple[str, int, str, str, str]]]:
    hallazgos: dict[str, list] = {}
    for py in sorted(carpeta.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        for linea, texto in _literales(py):
            prosa = _limpiar(texto)
            if len(prosa.strip()) < 12:      # fragmentos de marcado, no prosa
                continue
            for patron, cat, motivo in SEÑALES:
                for m in patron.finditer(prosa):
                    previo = prosa[max(0, m.start() - 70):m.start()]
                    if _NEGACION.search(previo) or _ATRIBUIDO.search(previo):
                        continue      # negado o atribuido a un tercero: uso correcto
                    ctx = prosa[max(0, m.start() - 45):m.start() + 55].strip()
                    ctx = " ".join(ctx.split())
                    hallazgos.setdefault(py.name, []).append(
                        (cat, linea, m.group(0), motivo, ctx))
                    break
    return hallazgos


def main(argv: list[str]) -> int:
    estricto = "--estricto" in argv
    args = [a for a in argv if not a.startswith("--")]
    carpeta = _RAIZ / (args[0] if args else "app/viz/render")
    if not carpeta.exists():
        print(f"ERROR: no existe {carpeta}")
        return 1

    hallazgos = revisar(carpeta)
    total = sum(len(v) for v in hallazgos.values())
    print("=" * 78)
    print(f"  NIVEL EPISTEMOLÓGICO — {carpeta.relative_to(_RAIZ)}")
    print("  ¿cada afirmación dice exactamente lo que la evidencia sostiene?")
    print("=" * 78)
    if not hallazgos:
        print("\n  Sin señales léxicas. (Los seis puntos de juicio siguen siendo lectura humana.)\n")
        return 0
    for archivo, items in sorted(hallazgos.items(), key=lambda kv: -len(kv[1])):
        print(f"\n## {archivo}   señales={len(items)}")
        for cat, linea, hit, motivo, ctx in sorted(items):
            print(f"   L{linea:<5} [{cat:<13}] «{hit}» — {motivo}")
            print(f"           … {ctx}")
    porcat: dict[str, int] = {}
    for items in hallazgos.values():
        for cat, *_ in items:
            porcat[cat] = porcat.get(cat, 0) + 1
    print("\n" + "=" * 78)
    print(f"  {total} señales · " + " · ".join(f"{k}={v}" for k, v in sorted(porcat.items())))
    print("  NO son errores: son puntos donde el nivel de la afirmación debe verificarse.")
    print("=" * 78)
    return 1 if (estricto and total) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
