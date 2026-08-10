"""
QUIRA — Gate del Sistema Visual  ·  `scripts/ci/check_sistema_visual.py`

Comprueba lo que la vista no delata a tiempo:

 1 · CONTRASTE. Cada color declarado alcanza el mínimo WCAG del uso que dice
     tener. El coral base sobre volcánico da 2,96:1 y no pasa ni el mínimo
     gráfico — es un error fácil de cometer y de no ver hasta que alguien no
     puede leer la pantalla. Ya pasó una vez: el gris #A9B8C1 de la landing
     daba 1,53:1 y estaba publicado.

 2 · UNA SOLA VERDAD. La landing define su paleta en CSS y el resto de la app
     la consume desde `utils/css_tokens.py`. Si los valores divergen, el sistema
     se bifurca en silencio. Aquí se comparan.

 3 · SIN COLOR DE "BIEN". Ningún token del sistema es verde. No es estética:
     QUIRA no certifica que la gestión esté bien, certifica qué se puede
     verificar — un verde en pantalla es un veredicto que la evidencia no
     sostiene.

 4 · LAS DOS ESCALAS. Verificabilidad tiene 5 niveles (CANON) y atención 3.
     Si alguien las funde en una, el gate lo dice.

Uso:  python scripts/ci/check_sistema_visual.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.css_tokens import C, contraste          # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
LANDING = RAIZ / "views" / "login_view.py"

fallas: list[str] = []
avisos: list[str] = []


def _t(titulo: str) -> None:
    print(f"\n{titulo}")


# ══════════════════════════════════════════════════════════════════════════════
# 1 · CONTRASTE — cada color contra el fondo donde el sistema dice usarlo
# ══════════════════════════════════════════════════════════════════════════════
# (token, hex, fondo, mínimo, para qué)
EXIGENCIAS = [
    ("ACENTO",   C.ACENTO,   C.VOLCAN,    4.5, "texto de acento sobre el fondo"),
    ("ACENTO",   C.ACENTO,   C.VOLCAN_UP, 4.5, "texto de acento sobre tarjeta"),
    ("V_TX",     C.V_TX,     C.VOLCAN,    7.0, "texto principal (AAA)"),
    ("V_TX2",    C.V_TX2,    C.VOLCAN,    4.5, "texto secundario"),
    ("V_TX3",    C.V_TX3,    C.VOLCAN_UP, 4.5, "metadatos sobre tarjeta"),
    ("OCRE",     C.OCRE,     C.VOLCAN_UP, 4.5, "atención sobre tarjeta"),
    ("CORAL_CL", C.CORAL_CL, C.VOLCAN,    3.0, "gráficos y bordes sobre oscuro"),
    ("PIZARRA",  C.PIZARRA,  C.PLANO,     4.5, "instrumental sobre plano"),
    ("TX",       C.TX,       C.PLANO,     7.0, "texto principal afuera (AAA)"),
    ("TX2",      C.TX2,      C.PLANO,     4.5, "texto secundario afuera"),
    # El coral pleno es de MARCA y GRÁFICO (logo, greca, bordes): 3:1. Da 4,05:1
    # sobre el plano, así que NO sirve para texto — para eso está CORAL_DP. La
    # landing lo usaba en 7 sitios de texto hasta que este gate lo delató.
    ("CORAL",    C.CORAL,    C.PLANO,     3.0, "marca y gráficos sobre plano"),
    ("CORAL_DP", C.CORAL_DP, C.PLANO,     4.5, "texto de acento sobre plano"),
    ("CORAL_DP", C.CORAL_DP, C.SUP,       4.5, "texto de acento sobre tarjeta"),
]

_t("[1/4] Contraste WCAG de cada token en su uso declarado")
for token, hx, fondo, minimo, uso in EXIGENCIAS:
    r = contraste(hx, fondo)
    ok = r >= minimo
    marca = "OK  " if ok else ">> "
    print(f"   {marca} {token:9} {hx} sobre {fondo}  {r:5.2f}:1  (min {minimo}) — {uso}")
    if not ok:
        fallas.append(f"{token} ({hx}) da {r:.2f}:1 sobre {fondo}; el uso «{uso}» "
                      f"exige {minimo}:1")

# El coral base NO debe alcanzar el umbral sobre volcánico: si un día lo alcanza
# es que alguien cambió el volcánico, y entonces todo lo demás hay que remedirlo.
if contraste(C.CORAL, C.VOLCAN) >= 3.0:
    avisos.append("CORAL ya pasa 3:1 sobre VOLCÁNICO — cambió un fondo; remedir todo.")


# ══════════════════════════════════════════════════════════════════════════════
# 2 · UNA SOLA VERDAD — la landing y los tokens no pueden divergir
# ══════════════════════════════════════════════════════════════════════════════
_t("[2/4] La paleta de la landing coincide con los tokens")
_VAR = re.compile(r"--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{6})")
css = LANDING.read_text(encoding="utf-8")
en_landing = {m.group(1): m.group(2).upper() for m in _VAR.finditer(css)}

ESPERADO = {"coral": C.CORAL, "coral-cl": C.CORAL_CL, "coral-dp": C.CORAL_DP,
            "plano": C.PLANO, "sup": C.SUP, "carril": C.CARRIL,
            "pizarra": C.PIZARRA, "tx": C.TX, "tx2": C.TX2, "tx3": C.TX3,
            "bd": C.BD}

for var, esperado in ESPERADO.items():
    real = en_landing.get(var)
    if real is None:
        avisos.append(f"la landing ya no declara --{var}")
        print(f"   ··  --{var:9} ausente en la landing")
    elif real != esperado.upper():
        fallas.append(f"--{var}: la landing dice {real} y css_tokens dice "
                      f"{esperado.upper()} — el sistema se bifurcó")
        print(f"   >>  --{var:9} landing {real} ≠ tokens {esperado.upper()}")
    else:
        print(f"   OK  --{var:9} {real}")

# El coral pleno no pinta texto: 4,05:1 sobre el plano. Se permite en `stroke`,
# `border`, `background` y en el fallback del logo — todo eso es gráfico.
# El look-behind excluye `border-color:`, `background-color:` y demás: esos son
# gráficos y el coral pleno sí les sirve.
_TEXTO_CORAL = re.compile(r"(?<![-\w])color:\s*(var\(--coral\)|#C1392B)(?![0-9A-Fa-f])", re.I)
usos_texto = [m.start() for m in _TEXTO_CORAL.finditer(css)
              if "Archivo,sans-serif" not in css[max(0, m.start() - 90):m.start()]]
if usos_texto:
    lineas = sorted({css[:p].count(chr(10)) + 1 for p in usos_texto})
    fallas.append(f"el coral pleno pinta texto en la landing (líneas {lineas}); "
                  f"da 4,05:1 y no alcanza AA — usar --coral-dp")
    print(f"   >>  coral pleno como color de texto en líneas {lineas}")
else:
    print("   OK  el coral pleno no pinta texto (solo marca, greca y bordes)")


# ══════════════════════════════════════════════════════════════════════════════
# 3 · NINGÚN VERDE EN EL SISTEMA
# ══════════════════════════════════════════════════════════════════════════════
_t("[3/4] Ningún token es verde (no hay color de «bien»)")


def _es_verde(hx: str) -> bool:
    """Verde = el canal G domina claramente sobre R y B."""
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", hx or ""):
        return False
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return g > r + 24 and g > b + 24


verdes = [(k, v) for k, v in vars(C).items()
          if not k.startswith("_") and isinstance(v, str) and _es_verde(v)]
if verdes:
    for k, v in verdes:
        fallas.append(f"{k} = {v} es un verde; el sistema no tiene color de «bien»")
        print(f"   >>  {k} = {v}")
else:
    print(f"   OK  {sum(1 for k, v in vars(C).items() if isinstance(v, str) and v.startswith('#'))} "
          f"tokens de color, ninguno verde")


# ══════════════════════════════════════════════════════════════════════════════
# 4 · LAS DOS ESCALAS SIGUEN SIENDO DOS
# ══════════════════════════════════════════════════════════════════════════════
_t("[4/4] Verificabilidad (5 niveles · CANON) y atención (3) no se funden")
CANON = ["independiente", "institucional", "parcial", "sin_evidencia", "contradiccion"]
niveles = [k for k, _ in C.niveles_verificabilidad()]
if niveles != CANON:
    fallas.append(f"la escala de verificabilidad es {niveles}; el canon dice {CANON}")
    print(f"   >>  {niveles}")
else:
    print(f"   OK  verificabilidad: {' · '.join(niveles)}")

# `sin_evidencia` no puede tener color: la ausencia se muestra como ausencia.
if C.verificabilidad("sin_evidencia")["c"] != "transparent":
    fallas.append("«sin evidencia» tiene color; la falta de evidencia se muestra "
                  "como falta de color, nunca como un suspenso")

# Un nivel desconocido debe caer en `sin_evidencia`, no inventar.
if C.verificabilidad("cualquier-cosa") is not C.verificabilidad("sin_evidencia"):
    fallas.append("un nivel desconocido no cae en «sin evidencia»")

atencion = {C.atencion(96), C.atencion(60), C.atencion(20), C.atencion(None)}
if len(atencion) != 3:
    fallas.append(f"la escala de atención devuelve {len(atencion)} colores; son 3")
else:
    print(f"   OK  atención: 3 niveles, y sin valor devuelve el instrumental")


# ══════════════════════════════════════════════════════════════════════════════
# 5 · NINGÚN VERDE DE «BIEN» EN LOS AMBIENTES
#
# Hasta 2026-08-08 este gate solo miraba `views/login_view.py`. Pasaba en verde
# mientras `quira_pages/env_civic.py` usaba #22C55E en cinco sitios — el verde de
# éxito que el sistema prohíbe expresamente, porque QUIRA mide VERIFICABILIDAD y
# no bondad: no hay color de «bien». El gate protegía la entrada y dejaba sin
# vigilar las pantallas donde la gente pasa el tiempo.
#
#   «Un gate verde no dice que el sistema esté conforme: dice que lo que ESE
#    gate inspecciona lo está.» (Colega · 2026-08-08)
#
# Se revisan los AMBIENTES, que son la frontera con el usuario. Las visualiza-
# ciones (mapas, series) quedan fuera a propósito: ahí una rampa de color puede
# ser legítima y este check produciría ruido en vez de señal.
# ══════════════════════════════════════════════════════════════════════════════
_t("5 · Verde de «bien» en los ambientes")

_HEX = re.compile(r"#([0-9a-fA-F]{6})\b")


def _es_verde_semaforo(h: str) -> bool:
    """Verde de éxito: el canal G domina claramente sobre los otros dos.

    Por composición y no por lista: una lista se queda corta en cuanto alguien
    escribe otro tono, que es exactamente cómo llegó #22C55E."""
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return g > r + 30 and g > b + 30


_ambientes = sorted(RAIZ.glob("quira_pages/env_*.py"))
_verdes = 0
for _amb in _ambientes:
    _txt = _amb.read_text(encoding="utf-8", errors="replace")
    _hall = {m.group(0) for m in _HEX.finditer(_txt) if _es_verde_semaforo(m.group(1))}
    if _hall:
        _verdes += len(_hall)
        fallas.append(f"{_amb.name} usa verde de «bien»: {', '.join(sorted(_hall))}")
if not _ambientes:
    fallas.append("no se encontró ningún ambiente que revisar — ¿cambió la ruta?")
elif not _verdes:
    print(f"   OK  {len(_ambientes)} ambientes, ningún verde de «bien»")


# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 62)
for a in avisos:
    print(f"  ·· aviso: {a}")
if fallas:
    print(f"  {len(fallas)} FALLA(S) — el sistema visual no se sostiene")
    for f in fallas:
        print(f"     - {f}")
    print("=" * 62)
    sys.exit(1)
print("  TODO OK — contraste verificado, una sola verdad, dos escalas")
print("=" * 62)
