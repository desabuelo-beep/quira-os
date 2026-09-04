# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_007b0.py — GM-Ω-ICPI-007-B0 · la genealogía reescrita
════════════════════════════════════════════════════════════════════════════════
`007-B0` se reescribió UNA sola vez, cuando dejaron de aparecer documentos. Su
versión anterior concluía que «la regla escrita y los valores implementados
nunca coincidieron» — y era falso: la auditoría comparaba contra la definición
de la tesis mientras el motor implementa la de `Metodologia_SIAP_ICPI`.

⚠️ Estas pruebas vigilan las DOS mitades: que la reconstrucción se mantenga, y
que la versión superada siga visible. Un expediente que borra sus versiones
anteriores no es auditable — y este expediente audita, entre otras cosas, a
quien lo escribe.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_FICHA = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_FICHA_FORENSE.md"


def test_la_genealogia_clasifica_cada_afirmacion_por_certeza():
    """La regla que hace utilizable la reconstrucción: cada afirmación declara
    de qué tipo es.

        DEMOSTRADO · DECLARADO · INFERIDO · NO DETERMINABLE

    Sin esa clasificación, una razón declarada por el autor se lee igual que un
    hecho documentado, y la genealogía del ICPI quedaría escrita con un estándar
    epistemológico inferior al que QUIRA exige a los datos que analiza."""
    txt = _FICHA.read_text(encoding="utf-8")
    bloque = txt.split("## 007-B0 · GENEALOGÍA DEL CONSTRUCTO")[1].split(
        "### 📜 VERSIÓN ANTERIOR")[0]
    for grado in ("DEMOSTRADO", "DECLARADO", "INFERIDO", "NO DETERMINABLE"):
        assert grado in bloque, (
            f"desapareció el grado `{grado}` de la reconstrucción. Los cuatro "
            f"son necesarios: sin ellos, lo declarado por el autor se confunde "
            f"con lo demostrado por evidencia")
    assert "no autoriza a inventar su causa" in bloque, (
        "se perdió la regla de la reconstrucción: una transición documentada no "
        "autoriza a inventar su causa")


def test_la_version_superada_se_conserva():
    """Un expediente que borra sus versiones anteriores no es auditable.

    `007-B0` concluyó algo falso y se corrigió. La corrección sólo puede
    verificarse si se ve **contra qué** se corrigió — y lo mismo vale para
    `7-ter.3`, que declaraba a `E_i` «el único componente sin biografía»."""
    txt = _FICHA.read_text(encoding="utf-8")
    assert "VERSIÓN ANTERIOR — conservada por genealogía" in txt, (
        "se borró la versión superada de 007-B0. La corrección deja de ser "
        "auditable en cuanto desaparece aquello que corrigió")
    assert "SUPERADO" in txt, (
        "`7-ter.3` dejó de marcarse como superado: declaraba que E_i no tenía "
        "biografía, y sí la tiene")


def test_C_i_no_se_presenta_como_renombre_de_E_i():
    """La precisión que la evidencia obliga y que es fácil perder.

    `E_i` mide autonomía o modalidad institucional; `C_i`, calidad del proceso
    orgánico vía penalizaciones legales. La transición `5 → 6 factores` es una
    **incorporación de dimensión**, no una sustitución — y de eso depende que
    `011-C` pregunte lo correcto."""
    txt = _FICHA.read_text(encoding="utf-8")
    assert "no es un renombre de" in txt, (
        "desapareció la distinción entre C_i y E_i. Si se leen como el mismo "
        "factor renombrado, 011-C dejaría de preguntar por qué se AÑADIÓ una "
        "dimensión")
    assert "27-abr-2026" in txt, (
        "se perdió la fecha de entrada de C_i, que es lo que cierra la ventana "
        "genealógica a 24 días")


def test_el_fallback_de_Ci_no_se_califica_de_defecto():
    """`C_i` opera hoy con su fallback porque las 25 metas tienen `INF-01..04 =
    0`. Y eso es coherente con la presunción de inocencia que el propio motor
    declara: `H01!A187` prohíbe expresamente lo contrario —«NUNCA inventar
    infracciones»—.

    ⚠️ Llamarlo defecto sería exigirle al sistema que fabrique evidencia. Lo que
    `011` debe juzgar es otra cosa: si un heurístico de 2025 es el fallback
    adecuado para 2026."""
    txt = _FICHA.read_text(encoding="utf-8")
    assert "no es un defecto" in txt, (
        "el fallback de C_i se calificó como defecto. Usar el valor base ante "
        "ausencia de infracción es la conducta correcta bajo presunción de "
        "inocencia; lo discutible es la vigencia del heurístico, no el mecanismo")
    assert "NUNCA inventar infracciones" in txt


def test_el_dictamen_no_confunde_reconstruir_con_aprobar():
    """La frase de cierre, y la que impide que esta sección se cite como aval.

        Reconstruir la historia no significa aprobarla.

    007-B0 demuestra que las transformaciones ocurrieron. Si su validez
    metodológica se diera por buena aquí, `011` heredaría aprobado lo que
    todavía tiene que juzgar."""
    txt = _FICHA.read_text(encoding="utf-8")
    assert "Reconstruir la historia no significa aprobarla" in txt
    assert "NO como validación" in txt, (
        "007-B0 dejó de declarar que cierra como reconstrucción y no como "
        "validación metodológica")
