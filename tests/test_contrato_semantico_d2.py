# -*- coding: utf-8 -*-
"""
tests/test_contrato_semantico_d2.py — el contrato que habilitó el sello de `D2`
════════════════════════════════════════════════════════════════════════════════
`ADR-055` fue sellado el 2026-09-06 adoptando la **lectura `A`**:

    el ICPI mide CONGRUENCIA ACREDITADA

Y con eso `V_i = 0` queda declarado como **un resultado de auditoría**, no como
una inferencia sobre el mundo: la unidad **no puede aportar congruencia
acreditada**, y eso **no afirma que el fenómeno no ocurriera**.

★ POR QUÉ ESTE TEST NO EXISTÍA ANTES

Mientras `D2` estaba `PROPUESTO`, un test no podía exigir ninguna de las dos
lecturas: habría convertido una propuesta en verdad matemática y la dirección
se habría encontrado con la decisión ya tomada por el custodio. Sólo cabía
verificar el estado de la implementación —`V=0 → J=0`—.

**El sello es lo que habilita este contrato.** Ahora sí hay una decisión
canónica que la implementación y la presentación deben respetar.

⚠️ Y LO QUE ESTE CONTRATO NO ACREDITA: que el ICPI sea una medida
sustantivamente válida de la gestión pública. La capa 3 de `011-C4` sigue
`NO DEMOSTRADA`. Declarar `A` elimina una ambigüedad semántica — nada más, y
nada menos.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_ADR = RAIZ / "docs" / "adr" / "ADR-055_D2_Semantica_de_la_Ausencia_de_Evidencia.md"

# Las superficies que le hablan a una persona. Son las que pueden afirmar de
# más: el motor calcula, la presentación es la que interpreta.
_SUPERFICIES = ("quira_pages", "app/viz", "data/gm_snapshot.json")


def _plano(txt: str) -> str:
    """Texto sin marcas de cita ni saltos.

    ⚠️ Hace falta porque el sello se escribe como bloque `> …` y el markdown
    parte las frases entre líneas. Un custodio que fallara por el formato del
    documento —y no por su contenido— enseña a ignorarlo."""
    return re.sub(r"\s+", " ", re.sub(r"^\s*>\s?", "", txt, flags=re.M))


def test_el_ADR_esta_sellado_con_la_lectura_A():
    """El contrato existe porque la decisión existe. Si `D2` volviera a
    `PROPUESTO`, este archivo entero dejaría de tener autoridad."""
    txt = _plano(_ADR.read_text(encoding="utf-8"))
    assert "sellado por Javo" in txt, (
        "D2 dejó de estar sellado. Sin decisión canónica, este contrato no "
        "puede exigir nada — volvería a fijar por su cuenta lo que la "
        "dirección no ha decidido")
    assert "LECTURA `A`: el ICPI mide CONGRUENCIA ACREDITADA" in txt, (
        "desapareció qué se adoptó exactamente. El contrato se apoya en esa "
        "frase")
    assert "no afirma que el fenómeno no ocurriera" in txt


def test_el_sello_declara_su_propio_limite():
    """★ La mitad que impide que el sello se lea como acreditación.

    Declarar `A` **no** declara que el ICPI mida válidamente la gestión
    pública. Si esa salvedad se pierde, un acto de precisión terminológica se
    convierte en un aval de validez — que es justo lo que las tres capas del
    dictamen existen para impedir."""
    txt = _plano(_ADR.read_text(encoding="utf-8"))
    assert "NO significa" in txt and "sustantivamente válida" in txt, (
        "el sello de D2 dejó de declarar su límite")
    assert "sigue `NO DEMOSTRADA`" in txt, (
        "desapareció la referencia a la capa 3 de 011-C4. Sin ella, sellar D2 "
        "parecería haber resuelto la validez del índice")


def test_ninguna_superficie_traduce_falta_de_evidencia_en_incumplimiento():
    """★★ EL CONTRATO. Lo que el sello de `D2` prohíbe decir.

    Bajo la lectura `A`, un `V_i = 0` significa **«no acreditado»**. Ninguna
    superficie puede traducirlo a **«no ejecutado»**, «no cumplió» o «no se
    hizo» — eso sería inferir un hecho del mundo desde una ausencia de
    evidencia, que el principio rector prohíbe expresamente:

        *«La ausencia de evidencia es un RESULTADO de auditoría, nunca
          autorización para inferir hechos.»*

    ⚠️ Se busca la CONJUNCIÓN en una misma frase —evidencia ausente **y**
    lenguaje de incumplimiento—, no cada término por separado. Un detector que
    marcara «sin evidencia» a secas caería en el falso positivo léxico que ya
    apareció dos veces en esta investigación (`col_E`, `«QUIRA adopta»`)."""
    _AUSENCIA = r"(sin evidencia|falta de evidencia|no verificad|V_?i?\s*=\s*0|no acreditad)"
    _INCUMPLE = r"(no se ejecut|no ejecut[óo]|incumpli|no cumpli[óo]|no se hizo|no se realiz|no ocurri)"
    rx = re.compile(
        rf"({_AUSENCIA}[^.\n]{{0,120}}{_INCUMPLE}|{_INCUMPLE}[^.\n]{{0,120}}{_AUSENCIA})",
        re.I)

    hallazgos, revisados = [], 0
    for ruta in _SUPERFICIES:
        base = RAIZ / ruta
        objetivos = [base] if base.is_file() else (
            list(base.rglob("*.py")) + list(base.rglob("*.json"))
            if base.exists() else [])
        revisados += len(objetivos)
        for p in objetivos:
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for m in rx.finditer(txt):
                frag = re.sub(r"\s+", " ", m.group(0))
                # Una frase que NIEGA la equivalencia es exactamente lo que
                # queremos que exista: no es una infracción, es el contrato.
                ctx = txt[max(0, m.start() - 140):m.end() + 80]
                if re.search(r"(\bno\b\s+(significa|implica|equivale|prueba)|≠|"
                             r"nunca|prohib)", ctx, re.I):
                    continue
                hallazgos.append(f"{p.relative_to(RAIZ).as_posix()} — «{frag[:150]}»")

    # ⚠️ Un contrato que no encuentra qué revisar pasa en verde sin haber
    # comprobado nada — es el defecto que `D-004` documentó en el propio CI:
    # un gate verde certificando un corpus que nunca miró.
    assert revisados >= 20, (
        f"el contrato sólo encontró {revisados} archivos de superficie. Si las "
        f"rutas cambiaron, este test pasa en verde sin verificar nada — "
        f"actualizar `_SUPERFICIES`")

    assert not hallazgos, (
        "una superficie traduce falta de evidencia en incumplimiento, y el "
        "sello de `ADR-055` (lectura `A`) lo prohíbe. `V_i = 0` significa NO "
        "ACREDITADO, no «no ejecutado»:\n  · " + "\n  · ".join(hallazgos[:6]))


def test_el_contrato_declara_que_verifica_presentacion_no_validez():
    """La barrera entre `ADR` y test, aplicada a este mismo archivo.

        ADR    declara la decisión
        TEST   comprueba que la implementación la respeta

    Este contrato verifica **cómo se presenta** un `V_i = 0`. No verifica —ni
    podría— que el ICPI mida bien la gestión pública. Confundir ambas cosas
    haría que una suite verde pareciera acreditar validez metodológica, y un
    recuento de pruebas sólo acredita el **estado del artefacto**."""
    yo = Path(__file__).read_text(encoding="utf-8")
    assert "no acredita" in yo.lower() and "sustantivamente válida" in yo, (
        "este contrato dejó de declarar qué no acredita. Sin esa línea, "
        "pasar el test se leería como haber demostrado la validez del índice")
