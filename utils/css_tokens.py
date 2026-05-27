"""
QUIRA Intelligence — Design Tokens Canónicos
Sprint D.4/D.5 · Hardening Visual + Design System Extraction

Fuente única de verdad para colores, tipografía, spacing y animaciones.
Cualquier componente Python o React debe importar desde aquí — nunca hardcodear.

Usar en HTML builders:
    from utils.css_tokens import C, T, S, A

Usar en React (exportar como JSON o TypeScript):
    python -c "from utils.css_tokens import export_json; print(export_json())"

Dylus Lab © 2026
"""
from __future__ import annotations
import json


# ══════════════════════════════════════════════════════════════════════════════
# C — COLOR TOKENS
# ══════════════════════════════════════════════════════════════════════════════

class C:
    """Paleta canónica QUIRA. Todas las instancias de color en el sistema."""

    # Identidad
    ACCENT    = "#00D4FF"    # Cyan — identidad QUIRA, links, ecosistema, IA
    BG        = "#050A12"    # Negro institucional — background global

    # Semáforo institucional
    RUPTURA   = "#EF4444"    # Rojo — TOP ruptura, SAT-III, alertas críticas
    ALERTA    = "#F97316"    # Naranja — SAT activas, cierre Q2
    AMBER     = "#F59E0B"    # Ámbar — concejo, compromisos urgentes, SAT-IV
    SOSTENIB  = "#22C55E"    # Verde — TOP sobre ritmo, D5, SISTEMA VIVO

    # Especiales
    PURPLE    = "#7C5CFC"    # Púrpura — fondos bloqueados, reencuadre político
    PURPLE_L  = "#C084FC"    # Púrpura claro — argumentario, destacados suaves
    AMBER_TGI = "#FFB700"    # Ámbar TGI — transición (no usar para SAT)

    # Texto
    TEXT      = "#E2E8F0"    # Texto principal — blanco frío
    TEXT_SEC  = "rgba(255,255,255,.35)"   # Texto secundario
    TEXT_MUTED = "rgba(255,255,255,.18)"  # Metadata, labels
    TEXT_DIM  = "rgba(255,255,255,.12)"   # Ultra sutil, fuentes, footers

    # Superficies
    SURFACE   = "rgba(255,255,255,.025)"  # Cards, zonas
    SURFACE_Z5 = "rgba(0,212,255,.02)"   # Ecosistema (tint cyan)
    SURFACE_Z6 = "rgba(255,255,255,.02)" # IA (neutro)

    # Bordes
    BORDER    = "rgba(255,255,255,.07)"   # Borde base
    BORDER_Z1 = "rgba(255,255,255,.09)"   # Z1 dominante (levemente más visible)
    BORDER_Z5 = "rgba(0,212,255,.12)"     # Ecosistema
    BORDER_Z6 = "rgba(255,255,255,.06)"   # IA

    # Separadores
    DIVIDER   = "rgba(255,255,255,.05)"   # Líneas internas de separación

    @classmethod
    def sem(cls, valor: float) -> str:
        """
        Semáforo TGI estándar (0–100).
        Función canónica — único lugar donde vive esta lógica.
        """
        if valor >= 70: return cls.SOSTENIB
        if valor >= 50: return cls.AMBER_TGI
        if valor >= 30: return cls.ALERTA
        return cls.RUPTURA

    @classmethod
    def top_color(cls, categoria: str) -> str:
        """Mapa canónico categoría TOP → color."""
        _MAP = {
            "ruptura":   cls.RUPTURA,
            "alerta":    cls.ALERTA,
            "sostenible": cls.SOSTENIB,
        }
        return _MAP.get(categoria, cls.RUPTURA)

    @classmethod
    def sat_color(cls, clasif: str) -> str:
        """Mapa canónico clasificación SAT → color."""
        _MAP = {
            "BAJO":    cls.SOSTENIB,
            "MEDIO":   cls.AMBER,
            "ALTO":    cls.ALERTA,
            "CRÍTICO": cls.RUPTURA,
        }
        return _MAP.get(clasif, cls.ALERTA)

    @classmethod
    def alpha(cls, hex_color: str, opacity: float) -> str:
        """
        Convierte hex + opacidad a string CSS para background inline.
        Ej: C.alpha(C.RUPTURA, 0.1) → 'rgba(239,68,68,.10)'
        Solo funciona con los 6 colores base definidos.
        """
        _HEX_TO_RGB = {
            "#00D4FF": (0, 212, 255),
            "#EF4444": (239, 68, 68),
            "#F97316": (249, 115, 22),
            "#F59E0B": (245, 158, 11),
            "#22C55E": (34, 197, 94),
            "#7C5CFC": (124, 92, 252),
            "#C084FC": (192, 132, 252),
            "#FFB700": (255, 183, 0),
        }
        rgb = _HEX_TO_RGB.get(hex_color)
        if not rgb:
            return hex_color
        r, g, b = rgb
        return f"rgba({r},{g},{b},{opacity:.2f})"


# ══════════════════════════════════════════════════════════════════════════════
# T — TYPOGRAPHY TOKENS
# ══════════════════════════════════════════════════════════════════════════════

class T:
    """Tokens tipográficos. Shorthand: font-property/line-height."""

    FAMILY_SANS  = "Inter, sans-serif"
    FAMILY_MONO  = "'JetBrains Mono', monospace"

    # Métricas dominantes (TOP, TGI grandes)
    METRIC_XL = "font:900 3rem/1 Inter,sans-serif;letter-spacing:-.04em"
    METRIC_LG = "font:900 2.8rem/1 Inter,sans-serif;letter-spacing:-.05em"
    METRIC_MD = "font:900 1.6rem/1 Inter,sans-serif;letter-spacing:-.03em"
    METRIC_SM = "font:900 1.5rem/1.1 Inter,sans-serif"
    METRIC_XS = "font:900 1.2rem/1 Inter,sans-serif"

    # Texto ejecutivo
    BODY_LG   = "font:400 13px/1.7 Inter,sans-serif"
    BODY_MD   = "font:400 11px/1.7 Inter,sans-serif"
    BODY_SM   = "font:400 10px/1.55 Inter,sans-serif"
    BODY_XS   = "font:400 9px/1.4 Inter,sans-serif"

    # Labels institucionales
    LABEL_LG  = "font:700 11px/1.2 Inter,sans-serif"
    LABEL_MD  = "font:700 9px/1 Inter,sans-serif"
    LABEL_SM  = "font:700 8px/1 Inter,sans-serif"
    LABEL_XS  = "font:700 7px/1 Inter,sans-serif"

    # Caps institucionales
    CAPS_LG = "font:800 10px/1 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase"
    CAPS_MD = "font:700 9px/1 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase"
    CAPS_SM = "font:700 8px/1 Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase"
    CAPS_XS = "font:700 7px/1 Inter,sans-serif;letter-spacing:.07em;text-transform:uppercase"

    # Mono (metadatos, fuentes, código)
    MONO_SM = "font:400 9px/1 'JetBrains Mono',monospace;letter-spacing:.04em"
    MONO_XS = "font:400 8px/1 'JetBrains Mono',monospace;letter-spacing:.04em"


# ══════════════════════════════════════════════════════════════════════════════
# S — SPACING TOKENS
# ══════════════════════════════════════════════════════════════════════════════

class S:
    """Tokens de spacing. Todos en px. Múltiplos de 2."""

    GAP_GRID   = 14    # Gap entre zonas principales
    GAP_CARD   = 12    # Gap entre entity cards
    GAP_INNER  = 10    # Gap interno en zona
    GAP_TIGHT  = 8     # Gap reducido
    GAP_MICRO  = 6     # Gap mínimo entre elementos inline

    PAD_ZONE   = 20    # Padding zona estándar
    PAD_COMPACT = 14   # Padding zona compacta (Z34)
    PAD_CARD   = 14    # Padding entity card vertical
    PAD_CARD_H = 12    # Padding entity card horizontal
    PAD_HEADER = 11    # Padding header vertical
    PAD_HEADER_H = 18  # Padding header horizontal
    PAD_CHIP_V = 5     # Padding chip vertical (KPI header)
    PAD_CHIP_H = 12    # Padding chip horizontal

    RADIUS_ZONE = 14   # Border-radius zona
    RADIUS_CARD = 12   # Border-radius card
    RADIUS_CHIP = 8    # Border-radius chip/badge pequeño
    RADIUS_BADGE = 4   # Border-radius badge inline


# ══════════════════════════════════════════════════════════════════════════════
# A — ANIMATION TOKENS
# ══════════════════════════════════════════════════════════════════════════════

class A:
    """Tokens de animación. Sprint C.3 — Observabilidad Viva."""

    # Duraciones
    LIVE_DOT      = "1.8s"    # Heartbeat SISTEMA VIVO
    RUPTURA_GLOW  = "2.8s"    # TOP ruptura box
    BRIEFING_GLOW = "3.2s"    # Briefing strip border

    # Timings distintos intencionalmente — ritmos orgánicos, no sincronizados
    EASING = "ease-in-out"

    # Clases CSS
    CLASS_RUPTURA  = "ve-ruptura-pulse"
    CLASS_LIVE_DOT = "ve-live-dot"
    CLASS_BRIEFING = "ve-briefing-live"

    # Umbrales de opacidad para ve-live-beat
    DOT_OPACITY_MAX = 1.0
    DOT_OPACITY_MIN = 0.28
    DOT_SCALE_MIN   = 0.58


# ══════════════════════════════════════════════════════════════════════════════
# EXPORT PARA REACT/TYPESCRIPT
# ══════════════════════════════════════════════════════════════════════════════

def export_json() -> str:
    """
    Exporta todos los tokens como JSON.
    Usar para generar design-tokens.json o tokens.ts en React.

    Usage:
        python -c "from utils.css_tokens import export_json; print(export_json())"
    """
    tokens = {
        "colors": {
            k: v for k, v in vars(C).items()
            if not k.startswith("_") and isinstance(v, str)
        },
        "spacing": {
            k: v for k, v in vars(S).items()
            if not k.startswith("_") and isinstance(v, int)
        },
        "animation": {
            "durations": {
                "liveDot":     A.LIVE_DOT,
                "rupturaGlow": A.RUPTURA_GLOW,
                "briefingGlow": A.BRIEFING_GLOW,
            },
            "easing": A.EASING,
            "classes": {
                "ruptura":  A.CLASS_RUPTURA,
                "liveDot":  A.CLASS_LIVE_DOT,
                "briefing": A.CLASS_BRIEFING,
            }
        }
    }
    return json.dumps(tokens, indent=2, ensure_ascii=False)
