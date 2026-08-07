"""
QUIRA — Sistema Visual Canónico  ·  v1.1 "Papel de plano"  ·  2026-08-06

Fuente única de color, tipografía, spacing y animación. Ningún módulo escribe
un hex a mano: si un color no está aquí, no existe.

────────────────────────────────────────────────────────────────────────────────
DOS REGISTROS — no son dos temas, son dos contextos con función distinta
────────────────────────────────────────────────────────────────────────────────
  · PLANO (claro)      → landing, informes, fichas, QUIRA Ciudadana. Lo público.
    Un fondo oscuro es literalmente opaco y la tesis del proyecto es que la
    información pública debe poder verse.
  · VOLCÁNICO (oscuro) → Centro de Inteligencia, cajones, panel del Observatorio.
    Ambiente de trabajo prolongado. Precedente exacto: la terminal de Bloomberg
    es negra, el sitio de Bloomberg es blanco.

────────────────────────────────────────────────────────────────────────────────
UN SOLO ACENTO — el coral Spondylus
────────────────────────────────────────────────────────────────────────────────
El jade salió del sistema: rojo + verde es un SEMÁFORO, y un semáforo dicta
«bueno / malo». QUIRA certifica verificabilidad, no verdad. Una marca con un
color es además más reconocible que con dos.

⚠ El coral base NO se usa sobre fondo oscuro: da 2,96:1 y no alcanza ni el
mínimo gráfico de 3:1. Adentro se usa `ACENTO` (#E08B7A, AA sobre volcánico y
sobre tarjeta). Medido, no estimado — ver `CONTRASTES` al pie.

────────────────────────────────────────────────────────────────────────────────
DOS ESCALAS QUE NO SE MEZCLAN — confundirlas sería el error más caro
────────────────────────────────────────────────────────────────────────────────
 1 · VERIFICABILIDAD (`verificabilidad()`) — CANON. Qué tan sostenida está una
     afirmación por la evidencia: independiente · institucional · parcial · sin
     evidencia · contradicción. NO dice nada sobre si la gestión es buena.
     Referencia: `CONSTITUCION_ONTOLOGICA_QUIRA.md` CAPA 0 · `PCD-MN01 §21`.

 2 · ATENCIÓN (`atencion()`) — qué tan lejos está un indicador de su umbral.
     La calcula el Gold Master (Regla 1: el semáforo es corregible en
     presentación, la fórmula no). Aquí solo se pinta.

Una afirmación puede ser de verificabilidad *independiente* y de atención
*crítica* a la vez: son ejes distintos. Pintarlas con la misma rampa haría
ilegible esa diferencia, que es justo lo que QUIRA vende.

Uso:
    from utils.css_tokens import C, T, S, A
    C.ACENTO · C.verificabilidad("parcial") · C.css_vars("volcanico")

Dylus Lab © 2026
"""
from __future__ import annotations
import json


# ══════════════════════════════════════════════════════════════════════════════
# C — COLOR
# ══════════════════════════════════════════════════════════════════════════════

class C:
    """Paleta canónica QUIRA v1.1. Todo color del sistema sale de aquí."""

    # ── IDENTIDAD ────────────────────────────────────────────────────────────
    CORAL      = "#C1392B"   # Spondylus. El color de la concha que da nombre al
                             # proyecto. Sobre PLANO. Nunca sobre volcánico.
    CORAL_CL   = "#D4715F"   # Coral claro — gráficos y bordes sobre oscuro (4,81:1)
    CORAL_DP   = "#8E2419"   # Coral profundo — hover y presionado sobre plano

    # ── REGISTRO PLANO (afuera · lo público) ─────────────────────────────────
    PLANO      = "#D9E0E5"   # Papel de levantamiento — fondo
    SUP        = "#F3F6F7"   # Superficie elevada (tarjeta, ficha)
    CARRIL     = "#C2CDD4"   # Carril, riel, pista de fondo
    PIZARRA    = "#4E6674"   # Instrumental sobre plano (4,53:1 · AA)
    TX         = "#18232B"   # Texto principal
    TX2        = "#52616B"   # Texto secundario
    TX3        = "#8296A2"   # Metadatos
    BD         = "#B9C6CD"   # Borde

    # ── REGISTRO VOLCÁNICO (adentro · el trabajo) ────────────────────────────
    # El volcánico es el mismo #18232B que afuera es el texto: la tinta de fuera
    # es el fondo de dentro. No es coincidencia, es el mismo sistema dado vuelta.
    VOLCAN     = "#18232B"   # Fondo
    VOLCAN_UP  = "#212F3A"   # Superficie elevada. Separación 1,17:1 — deliberado:
                             # la tarjeta se distingue por BORDE, no por fondo.
    ACENTO     = "#E08B7A"   # Acento de texto adentro (6,20:1 fondo · 5,31:1 tarjeta)
    V_TX       = "#E6EDF1"   # Texto principal (13,51:1 · AAA)
    V_TX2      = "#A9BAC5"   # Texto secundario (8,00:1 · AAA)
    V_TX3      = "#8FA5B2"   # Metadatos (6,23:1 · AA en ambos fondos)
    V_BD       = "rgba(255,255,255,.09)"   # Borde base
    V_BD_FUERTE= "rgba(255,255,255,.17)"   # Borde de énfasis

    # ── ATENCIÓN — sin verde, y la razón importa ─────────────────────────────
    # No hay color de "bien". La ausencia de señal es ausencia de señal, no un
    # aprobado: QUIRA no certifica que la gestión esté bien, certifica qué se
    # puede verificar. Un verde en pantalla sería un veredicto que la evidencia
    # no sostiene — el mismo error que se corrigió en la portada de d08.
    SIN_SENAL  = "#8FA5B2"   # Dentro de umbral. Instrumental, no celebratorio.
    OCRE       = "#C89B3C"   # Requiere atención (6,25:1 · AA)
    CRITICO    = "#E08B7A"   # Fuera de umbral. Es el acento: lo que pide tu ojo.

    # ── COMPATIBILIDAD ───────────────────────────────────────────────────────
    # Nombres del sistema anterior, remapeados. No usar en código nuevo.
    ACCENT     = ACENTO
    BG         = VOLCAN
    RUPTURA    = CRITICO
    ALERTA     = OCRE
    AMBER      = OCRE
    AMBER_TGI  = OCRE
    SOSTENIB   = SIN_SENAL
    TEXT       = V_TX
    TEXT_SEC   = V_TX2
    TEXT_MUTED = V_TX3
    TEXT_DIM   = "rgba(255,255,255,.12)"
    SURFACE    = VOLCAN_UP
    BORDER     = V_BD
    DIVIDER    = "rgba(255,255,255,.06)"

    # ── ESCALA 1 · VERIFICABILIDAD (CANON) ───────────────────────────────────
    # Rampa del Spondylus a la ausencia: la INTENSIDAD dice cuánto sostiene el
    # documento; la falta de color dice falta de evidencia — nunca un suspenso.
    #
    # `contradiccion` NO pertenece a la rampa. No es "menos evidencia": es
    # evidencia en conflicto, que es un hallazgo distinto en naturaleza, no en
    # grado. Por eso lleva marca propia (trama) y no una intensidad menor.
    _VERIF: dict[str, dict[str, str]] = {
        "independiente": {"c": ACENTO,    "op": "1",    "trama": "",
                          "label": "Verificación independiente"},
        "institucional": {"c": ACENTO,    "op": ".72",  "trama": "",
                          "label": "Fuente institucional"},
        "parcial":       {"c": ACENTO,    "op": ".45",  "trama": "",
                          "label": "Evidencia parcial"},
        "sin_evidencia": {"c": "transparent", "op": "1", "trama": "punteado",
                          "label": "Sin evidencia localizada"},
        "contradiccion": {"c": OCRE,      "op": "1",    "trama": "diagonal",
                          "label": "Contradicción entre fuentes"},
    }

    @classmethod
    def verificabilidad(cls, nivel: str) -> dict[str, str]:
        """Tratamiento visual de un nivel de verificabilidad (CANON · 5 niveles).

        Devuelve color, opacidad, trama y etiqueta pública. Un nivel desconocido
        cae en `sin_evidencia`: ante la duda, la ausencia de evidencia es un
        RESULTADO de auditoría, nunca autorización para inferir."""
        return cls._VERIF.get(str(nivel or "").lower(), cls._VERIF["sin_evidencia"])

    @classmethod
    def niveles_verificabilidad(cls) -> list[tuple[str, dict[str, str]]]:
        """Los 5 niveles en orden canónico — para leyendas y catálogos."""
        return list(cls._VERIF.items())

    # ── ESCALA 2 · ATENCIÓN (la calcula el motor) ────────────────────────────
    @classmethod
    def atencion(cls, valor: float | None, umbral: float = 70.0,
                 alerta: float = 50.0) -> str:
        """Color de atención para un indicador 0–100 que el motor ya clasificó.

        Tres niveles, no cuatro, y ninguno dice "bien" (ver SIN_SENAL). Sin
        valor devuelve el instrumental: no saber no es estar mal."""
        if valor is None:
            return cls.SIN_SENAL
        if valor >= umbral:
            return cls.SIN_SENAL
        if valor >= alerta:
            return cls.OCRE
        return cls.CRITICO

    @classmethod
    def sem(cls, valor: float | None) -> str:
        """Alias histórico de `atencion()`. Se conserva porque el Centro de Mando
        y su v1 lo llaman; el comportamiento cambió a propósito — ya no devuelve
        verde, porque no hay color de "bien" en el sistema."""
        return cls.atencion(valor)

    @classmethod
    def sat_color(cls, clasif: str) -> str:
        """Clasificación SAT → color de atención."""
        _MAP = {"BAJO": cls.SIN_SENAL, "MEDIO": cls.OCRE,
                "ALTO": cls.OCRE, "CRÍTICO": cls.CRITICO}
        return _MAP.get(str(clasif or "").upper(), cls.SIN_SENAL)

    @classmethod
    def top_color(cls, categoria: str) -> str:
        """Categoría TOP → color de atención."""
        _MAP = {"ruptura": cls.CRITICO, "alerta": cls.OCRE,
                "sostenible": cls.SIN_SENAL}
        return _MAP.get(str(categoria or "").lower(), cls.SIN_SENAL)

    # ── UTILIDADES ───────────────────────────────────────────────────────────
    @staticmethod
    def alpha(hex_color: str, opacity: float) -> str:
        """hex + opacidad → rgba(). Convierte cualquier hex de 3 o 6 dígitos.

        La versión anterior solo conocía 8 colores y devolvía el hex CRUDO para
        el resto: pedir 10% de opacidad entregaba el color pleno, en silencio."""
        h = str(hex_color or "").strip().lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        if len(h) != 6:
            return hex_color
        try:
            r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return hex_color
        return f"rgba({r},{g},{b},{opacity:.3f})"

    @classmethod
    def css_vars(cls, registro: str = "volcanico") -> str:
        """Bloque `:root{…}` con las variables del registro pedido.

        Que el CSS beba de aquí es lo que impide que el sistema se bifurque en
        dos verdades — que es exactamente lo que pasó hasta hoy: este módulo
        existía y solo 3 archivos lo importaban."""
        if registro == "plano":
            pares = [("coral", cls.CORAL), ("coral-cl", cls.CORAL_CL),
                     ("coral-dp", cls.CORAL_DP), ("plano", cls.PLANO),
                     ("sup", cls.SUP), ("carril", cls.CARRIL),
                     ("pizarra", cls.PIZARRA), ("tx", cls.TX),
                     ("tx2", cls.TX2), ("tx3", cls.TX3), ("bd", cls.BD)]
        else:
            pares = [("bg", cls.VOLCAN), ("sup", cls.VOLCAN_UP),
                     ("acento", cls.ACENTO), ("acento-gr", cls.CORAL_CL),
                     ("tx", cls.V_TX), ("tx2", cls.V_TX2), ("tx3", cls.V_TX3),
                     ("bd", cls.V_BD), ("bd-f", cls.V_BD_FUERTE),
                     ("sin-senal", cls.SIN_SENAL), ("ocre", cls.OCRE),
                     ("critico", cls.CRITICO)]
        cuerpo = "".join(f"--q-{k}:{v};" for k, v in pares)
        return f":root{{{cuerpo}}}"


# ══════════════════════════════════════════════════════════════════════════════
# T — TIPOGRAFÍA
# ══════════════════════════════════════════════════════════════════════════════

class T:
    """Tokens tipográficos. Shorthand: font-property/line-height."""

    FAMILY_SANS  = "Inter, sans-serif"
    FAMILY_MONO  = "'JetBrains Mono', monospace"
    FAMILY_MARCA = "Archivo, Inter, sans-serif"   # solo el nombre QUIRA

    # Métricas dominantes
    METRIC_XL = "font:900 3rem/1 Inter,sans-serif;letter-spacing:-.04em"
    METRIC_LG = "font:900 2.8rem/1 Inter,sans-serif;letter-spacing:-.05em"
    METRIC_MD = "font:900 1.6rem/1 Inter,sans-serif;letter-spacing:-.03em"
    METRIC_SM = "font:900 1.5rem/1.1 Inter,sans-serif"
    METRIC_XS = "font:900 1.2rem/1 Inter,sans-serif"

    # Texto
    BODY_LG   = "font:400 13px/1.7 Inter,sans-serif"
    BODY_MD   = "font:400 11px/1.7 Inter,sans-serif"
    BODY_SM   = "font:400 10px/1.55 Inter,sans-serif"
    BODY_XS   = "font:400 9px/1.4 Inter,sans-serif"

    # Labels
    LABEL_LG  = "font:700 11px/1.2 Inter,sans-serif"
    LABEL_MD  = "font:700 9px/1 Inter,sans-serif"
    LABEL_SM  = "font:700 8px/1 Inter,sans-serif"
    LABEL_XS  = "font:700 7px/1 Inter,sans-serif"

    # Caps institucionales
    CAPS_LG = "font:800 10px/1 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase"
    CAPS_MD = "font:700 9px/1 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase"
    CAPS_SM = "font:700 8px/1 Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase"
    CAPS_XS = "font:700 7px/1 Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase"

    # Mono — metadatos, folios, trazabilidad
    MONO_SM = "font:400 9px/1 'JetBrains Mono',monospace;letter-spacing:.04em"
    MONO_XS = "font:400 8px/1 'JetBrains Mono',monospace;letter-spacing:.04em"


# ══════════════════════════════════════════════════════════════════════════════
# S — SPACING
# ══════════════════════════════════════════════════════════════════════════════

class S:
    """Tokens de spacing. Todos en px. Múltiplos de 2."""

    GAP_GRID   = 14
    GAP_CARD   = 12
    GAP_INNER  = 10
    GAP_TIGHT  = 8
    GAP_MICRO  = 6

    PAD_ZONE     = 20
    PAD_COMPACT  = 14
    PAD_CARD     = 14
    PAD_CARD_H   = 12
    PAD_HEADER   = 11
    PAD_HEADER_H = 18
    PAD_CHIP_V   = 5
    PAD_CHIP_H   = 12

    RADIUS_ZONE  = 14
    RADIUS_CARD  = 12
    RADIUS_CHIP  = 8
    RADIUS_BADGE = 4


# ══════════════════════════════════════════════════════════════════════════════
# A — ANIMACIÓN
# ══════════════════════════════════════════════════════════════════════════════

class A:
    """Tokens de animación. Sobrio por doctrina: nada parpadea para alarmar."""

    LIVE_DOT      = "1.8s"
    ATENCION_GLOW = "2.8s"
    BRIEFING_GLOW = "3.2s"
    EASING        = "ease-in-out"

    CLASS_ATENCION = "q-atencion-pulse"
    CLASS_LIVE_DOT = "q-live-dot"
    CLASS_BRIEFING = "q-briefing-live"

    DOT_OPACITY_MAX = 1.0
    DOT_OPACITY_MIN = 0.28
    DOT_SCALE_MIN   = 0.58

    # Compatibilidad con el nombre anterior
    RUPTURA_GLOW  = ATENCION_GLOW
    CLASS_RUPTURA = CLASS_ATENCION


# ══════════════════════════════════════════════════════════════════════════════
# CONTRASTES VERIFICADOS — medidos con `_contraste()`, no estimados
# ══════════════════════════════════════════════════════════════════════════════
# Sobre VOLCÁNICO #18232B          Sobre TARJETA #212F3A
#   CORAL    #C1392B   2,96  ✗       CORAL    #C1392B   2,54  ✗   ← nunca adentro
#   CORAL_CL #D4715F   4,81  AA      CORAL_CL #D4715F   4,13  gráfico
#   ACENTO   #E08B7A   6,20  AA      ACENTO   #E08B7A   5,31  AA
#   V_TX     #E6EDF1  13,51  AAA     V_TX     #E6EDF1  11,58  AAA
#   V_TX2    #A9BAC5   8,00  AAA     V_TX2    #A9BAC5   6,86  AA
#   V_TX3    #8FA5B2   6,23  AA      V_TX3    #8FA5B2   5,35  AA
#   OCRE     #C89B3C   6,25  AA      OCRE     #C89B3C   5,36  AA

def _luminancia(hx: str) -> float:
    """Luminancia relativa WCAG de un hex."""
    h = hx.lstrip("#")
    def _lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a: str, b: str) -> float:
    """Razón de contraste WCAG entre dos hex. Para verificar, no para adivinar."""
    la, lb = _luminancia(a), _luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def export_json() -> str:
    """Tokens como JSON — para generar design-tokens.json o tokens.ts.

        python -c "from utils.css_tokens import export_json; print(export_json())"
    """
    return json.dumps({
        "colors":  {k: v for k, v in vars(C).items()
                    if not k.startswith("_") and isinstance(v, str)},
        "spacing": {k: v for k, v in vars(S).items()
                    if not k.startswith("_") and isinstance(v, int)},
        "animation": {
            "durations": {"liveDot": A.LIVE_DOT, "atencionGlow": A.ATENCION_GLOW,
                          "briefingGlow": A.BRIEFING_GLOW},
            "easing": A.EASING,
            "classes": {"atencion": A.CLASS_ATENCION, "liveDot": A.CLASS_LIVE_DOT,
                        "briefing": A.CLASS_BRIEFING},
        },
    }, indent=2, ensure_ascii=False)
