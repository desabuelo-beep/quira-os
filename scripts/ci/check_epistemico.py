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

DOS NIVELES, y la distinción es lo que lo hace utilizable como gate (2026-08-26):

  ⛔ ERROR  viola el canon de forma inequívoca —lenguaje acusatorio, QUIRA como
           auditoría, el sistema ordenando al GAD—. Con `--estricto` DETIENE.
  ·  SEÑAL  es una pregunta de juicio: su motivo termina en «¿es ese el sentido?».
           Se imprime siempre y NUNCA bloquea.

Antes `--estricto` fallaba con CUALQUIER señal. Auditadas una a una, las cuatro vivas
eran falsos positivos: describir una obligación legal no es prescribirla, «imposibilidad
de auditoría» predica del documento y no de QUIRA, y una cabecera de tabla no afirma
nada. Engancharlo así habría bloqueado por 100 % de ruido — **un gate que bloquea por
falsos positivos es otra forma de autoridad fabricada por el código** (colega).

Capa: solo STRINGS LITERALES (lo que el usuario lee). Docstrings y comentarios son capa
interna y no se escanean — ahí explicar la regla exige nombrarla.

Uso:  python scripts/ci/check_epistemico.py [carpeta] [--estricto]
      (por defecto: app/viz/render — donde vive el texto de los cajones)
"""
from __future__ import annotations

import ast
import re
import sys
# La consola de Windows abre en cp1252 y este gate imprime flechas y viñetas.
# Sin esto revienta con UnicodeEncodeError DESPUÉS de calcular sus resultados:
# un gate que muere al informar es un gate que no informa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]

# ── ERROR vs SEÑAL · la distinción que hacía inviable el gate (2026-08-26) ────
# Auditando las cuatro señales vivas apareció que los patrones NO son homogéneos:
#
#   «incumplió», «ilegal»      → la Regla 2 lo PROHÍBE. Es un error, y es inequívoco.
#   «componentes», «por tanto» → el motivo termina literalmente en «¿es ese el
#                                sentido?». Es una PREGUNTA de juicio humano.
#
# Bloquear por igual ambas cosas convertiría el gate en ruido y lo haría desactivar
# —el destino de todo guard que grita— o, peor, detendría el trabajo por una duda
# legítima. `--estricto` falla SÓLO con ERROR; las señales siguen imprimiéndose.
ERROR, SENAL = "ERROR", "SEÑAL"

# (patrón, categoría, por qué importa, nivel).
SEÑALES: list[tuple[re.Pattern, str, str, str]] = [
    # ── 1 · INFERENCIA ────────────────────────────────────────────────────────
    (re.compile(r"\bdemuestra\b", re.I), "INFERENCIA", "¿está medido o se deduce?", SENAL),
    (re.compile(r"\bprueba que\b", re.I), "INFERENCIA", "afirma prueba, no medición", SENAL),
    (re.compile(r"\bconfirma\b", re.I), "INFERENCIA", "confirmar exige contraste previo", SENAL),
    (re.compile(r"\bpermite concluir\b", re.I), "INFERENCIA", "conclusión, no observación", SENAL),
    (re.compile(r"\b(el|la) (municipio|GAD|entidad) (sabe|puede|no puede|quiere)\b", re.I),
     "INFERENCIA", "atribuye capacidad o voluntad interna — nunca medida", SENAL),
    (re.compile(r"\brevela que\b", re.I), "INFERENCIA", "revelar = afirmar causa", SENAL),
    (re.compile(r"\bsignifica que\b", re.I), "INFERENCIA", "equivale a interpretar", SENAL),
    (re.compile(r"\bdebido a\b", re.I), "INFERENCIA", "atribución causal directa", SENAL),
    (re.compile(r"\bpor tanto\b", re.I), "INFERENCIA", "encadena deducción — revisar el salto", SENAL),
    # ── 2 · PRESCRIPCIÓN ──────────────────────────────────────────────────────
    (re.compile(r"\b(el|la) (municipio|GAD|entidad) deb[eí]", re.I), "PRESCRIPCION",
     "el sistema no ordena: informa y conecta", ERROR),
    (re.compile(r"\bhay que\b", re.I), "PRESCRIPCION", "instrucción directa", SENAL),
    (re.compile(r"\bes necesario que\b", re.I), "PRESCRIPCION", "instrucción encubierta", SENAL),
    (re.compile(r"\bse recomienda\b", re.I), "PRESCRIPCION", "la recomendación es del decisor", SENAL),
    (re.compile(r"\bdeberá\b", re.I), "PRESCRIPCION", "registro imperativo", SENAL),
    (re.compile(r"\bobligatori", re.I), "PRESCRIPCION", "¿lo obliga la ley, o lo propone el sistema?", SENAL),
    # ── 3 · ALCANCE ───────────────────────────────────────────────────────────
    (re.compile(r"\bla cadena (no se puede|no puede)\b", re.I), "ALCANCE",
     "la cadena existe; lo que falta son atributos para reconstruirla", SENAL),
    (re.compile(r"\bplan operativo \d{4}\s*[-–]\s*\d{4}", re.I), "ALCANCE",
     "el POA es ANUAL — un rango plurianual es el PDOT", SENAL),
    # ── 4 · TERMINOLOGÍA ──────────────────────────────────────────────────────
    (re.compile(r"\bauditor[ií]a\b", re.I), "TERMINOLOGIA",
     "QUIRA es infraestructura de conocimiento, no auditoría (CONSTITUCION-001)", ERROR),
    (re.compile(r"\bfiscaliza", re.I), "TERMINOLOGIA", "fiscalizar es competencia de otro órgano", ERROR),
    (re.compile(r"\bcertifica (que|el incumplimiento|la verdad)\b", re.I), "TERMINOLOGIA",
     "certifica VERIFICABILIDAD, nunca verdad ni incumplimiento", ERROR),
    (re.compile(r"\bcomponentes?\b", re.I), "TERMINOLOGIA",
     "en planificación designa los componentes del PDOT — ¿es ese el sentido?", SENAL),
    (re.compile(r"\b(incumpl|violó|ilegal|irregular)", re.I), "TERMINOLOGIA",
     "lenguaje acusatorio — prohibido (Regla 2)", ERROR),
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

# ── LAS TRES SUPRESIONES QUE FALTABAN (2026-08-26) ────────────────────────────
# Auditado señal por señal con el protocolo del colega —patrón · texto · negación ·
# mención o afirmación · contradicción real · autoridad invocada · qué haría el gate—
# las CUATRO señales vivas resultaron falsos positivos. Enganchar `--estricto` así
# habría bloqueado por 100 % de ruido: **un gate que bloquea por falsos positivos es
# otra forma de autoridad fabricada por el código** (colega, 2026-08-26).
#
# Las tres causas son distinciones que esta sesión ya había establecido en otro plano:

# 1 · DESCRIBIR UNA OBLIGACIÓN LEGAL NO ES PRESCRIBIR.
#     «La rendición de cuentas es el acto anual y obligatorio…» enuncia un deber que
#     fija la LOPC; no lo impone QUIRA. El propio motivo del patrón lo pregunta —«¿lo
#     obliga la ley, o lo propone el sistema?»— y aquí la respuesta es la ley. No se
#     veía porque `_ATRIBUIDO` sólo mira hacia atrás, y el órgano que obliga suele
#     aparecer DESPUÉS («…ante el Consejo de Participación Ciudadana»).
_OBLIGACION_AJENA = re.compile(
    r"\b(rendición de cuentas|transparencia activa|declaración patrimonial|"
    r"Consejo de Participación|CPCCS|LOTAIP|LOPC|COOTAD|COPFP|SERCOP|"
    r"la ley|la norma|el reglamento|la ordenanza)\b", re.I)

# 2 · MENCIÓN ≠ AFIRMACIÓN.  «constituye una imposibilidad de auditoría» predica del
#     DOCUMENTO, no de QUIRA. El término sólo debe marcar cuando se dice que QUIRA
#     *es* o *hace* auditoría — que es lo que CONSTITUCION-001 excluye.
_TERMINO_SOBRE_OTRO = re.compile(
    r"\b(imposibilidad|posibilidad|sujeto|objeto|informe|proceso|pista|traza|"
    r"capacidad|falta|ausencia)\s+de\s+$", re.I)

# 3 · UNA CABECERA DE TABLA NO ES PROSA.  «Período Informe Fecha Lugar Asistentes
#     Componentes» son los encabezados de una tabla: `_limpiar` retira el marcado y
#     deja las celdas pegadas, que parecen una frase y no lo son.
_SIN_VERBO = re.compile(
    r"\b(es|son|está|están|constituye|tiene|debe|puede|hay|fue|será|se\s+\w+)\b", re.I)


def _es_cabecera(prosa: str) -> bool:
    """Secuencia de rótulos sin un solo verbo conjugado: no es una afirmación."""
    palabras = prosa.split()
    if len(palabras) > 12 or _SIN_VERBO.search(prosa):
        return False
    capitalizadas = sum(1 for p in palabras if p[:1].isupper())
    return capitalizadas >= 3


def revisar(carpeta: Path) -> dict[str, list[tuple[str, int, str, str, str]]]:
    hallazgos: dict[str, list] = {}
    for py in sorted(carpeta.rglob("*.py")):
        if "__pycache__" in py.parts:
            continue
        for linea, texto in _literales(py):
            prosa = _limpiar(texto)
            if len(prosa.strip()) < 12:      # fragmentos de marcado, no prosa
                continue
            if _es_cabecera(prosa):          # rótulos de tabla: no afirman nada
                continue
            for patron, cat, motivo, nivel in SEÑALES:
                for m in patron.finditer(prosa):
                    previo = prosa[max(0, m.start() - 70):m.start()]
                    if _NEGACION.search(previo) or _ATRIBUIDO.search(previo):
                        continue      # negado o atribuido a un tercero: uso correcto
                    if cat == "PRESCRIPCION" and _OBLIGACION_AJENA.search(prosa):
                        continue      # describe un deber que fija la ley, no lo impone
                    if _TERMINO_SOBRE_OTRO.search(previo):
                        continue      # el término se predica de otro objeto, no de QUIRA
                    ctx = prosa[max(0, m.start() - 45):m.start() + 55].strip()
                    ctx = " ".join(ctx.split())
                    hallazgos.setdefault(py.name, []).append(
                        (cat, linea, m.group(0), motivo, ctx, nivel))
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
    # `relative_to` revienta si la carpeta está fuera del repo —p. ej. un fixture de
    # prueba en un temporal—, y lo hace DESPUÉS de haber recorrido todo: el mismo
    # defecto que el comentario de arriba señala para la consola de Windows. Un gate
    # que muere al informar es un gate que no informa (hallado 2026-08-26 al auditarlo).
    try:
        etiqueta = carpeta.relative_to(_RAIZ)
    except ValueError:
        etiqueta = carpeta
    print(f"  NIVEL EPISTEMOLÓGICO — {etiqueta}")
    print("  ¿cada afirmación dice exactamente lo que la evidencia sostiene?")
    print("=" * 78)
    if not hallazgos:
        print("\n  Sin señales léxicas. (Los seis puntos de juicio siguen siendo lectura humana.)\n")
        return 0
    for archivo, items in sorted(hallazgos.items(), key=lambda kv: -len(kv[1])):
        print(f"\n## {archivo}   señales={len(items)}")
        for cat, linea, hit, motivo, ctx, nivel in sorted(items):
            marca = "⛔" if nivel == ERROR else "· "
            print(f"  {marca} L{linea:<5} [{cat:<13}] «{hit}» — {motivo}")
            print(f"           … {ctx}")
    porcat: dict[str, int] = {}
    errores = 0
    for items in hallazgos.values():
        for cat, _l, _h, _m, _c, nivel in items:
            porcat[cat] = porcat.get(cat, 0) + 1
            errores += (nivel == ERROR)
    print("\n" + "=" * 78)
    print(f"  {total} hallazgos · {errores} ⛔ERROR · {total - errores} ·SEÑAL")
    print("  " + " · ".join(f"{k}={v}" for k, v in sorted(porcat.items())))
    print("  ⛔ERROR viola el canon y detiene con --estricto. ·SEÑAL es una pregunta")
    print("  de juicio: se imprime siempre y NUNCA bloquea (auditado 2026-08-26).")
    print("=" * 78)
    return 1 if (estricto and errores) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
