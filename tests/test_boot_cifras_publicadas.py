# -*- coding: utf-8 -*-
"""
tests/test_boot_cifras_publicadas.py — ataques de `D-015`
════════════════════════════════════════════════════════════════════════════════
★ POR QUÉ EXISTE

`BOOT.md` es contexto operativo: se lee en cada arranque y **sus cifras se
propagan a todo lo que se escriba después**. Publicaba `SITA 2025 0,4448`, un
valor que ningún artefacto examinado respalda.

Al buscar el valor correcto apareció algo mayor: **dos corridas selladas del
mismo año, los mismos doce meses y el mismo `vara_sha`, con `0,9719` y
`0,4630`**. La forense mostró que la diferencia no era metodológica sino de
**universo de entrada** — y que la corrida alta había excluido justo los tres
conjuntos que el portal no publica.

    El universo de una medición son los conjuntos EXIGIBLES,
    nunca los conjuntos ENCONTRADOS.

Medir sólo lo que existe produce un municipio casi perfecto. Es exactamente lo
que `ADR-046` advierte: así «el sistema premiaría la opacidad».

⚠️ Estas pruebas protegen REGLAS, no el estado actual: siguen siendo válidas
aunque mañana cambien todos los valores.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_BOOT = RAIZ / "governance" / "BOOT.md"
_PCD07 = RAIZ / "docs" / "pcd" / "PCD-D07_Transparencia.md"
_CORRIDAS = RAIZ / "data" / "d07" / "corridas"
_CATALOGO = RAIZ / "data" / "d07"


def _universo_canonico() -> set[str]:
    """Los conjuntos de datos exigibles, **derivados del catálogo** que se
    declara `fuente_verdad`, nunca de un número escrito en una prueba."""
    cats = sorted(_CATALOGO.glob("catalogo_cd_d07_v*.yaml"))
    if not cats:
        return set()
    return set(re.findall(r"\bCD-[A-Z0-9]+",
                          cats[-1].read_text(encoding="utf-8")))


def _corridas() -> dict[str, dict]:
    if not _CORRIDAS.is_dir():
        return {}
    return {f.stem: json.loads(f.read_text(encoding="utf-8"))
            for f in sorted(_CORRIDAS.glob("*.json"))}


def test_una_corrida_no_excluye_del_universo_lo_no_publicado():
    """★ ATAQUE DE `D-015` · REGLA PROTEGIDA: **el universo son los conjuntos
    exigibles, no los encontrados.**

    `RUN-D07-2026-08-18-0001` midió 21 de 24 conjuntos y no produjo **ni una
    fila en cero** — `SITA 0,9719`. Los tres que faltaban eran precisamente
    `CD-01`, `CD-07` y `CD-10`, los que el portal no publica.

    ⚠️ Una corrida así no es una medición alternativa: es una medición **mal
    encuadrada**, y su cifra recompensa al sujeto por no publicar. La doctrina
    del proyecto es la contraria — la ausencia de evidencia es un **resultado**
    de la observación, no una exclusión de su universo.

    Esta prueba no prohíbe que existan corridas parciales: prohíbe que existan
    **sin estar reconocidas**. Una corrida incompleta que nadie declaró es una
    cifra suelta esperando a ser citada como si fuera el índice del año."""
    universo = _universo_canonico()
    assert universo, (
        "no se pudo derivar el universo canónico del catálogo de `d07`. Sin "
        "esa referencia, ninguna corrida puede declararse completa")

    from app.agents import deuda as _d
    d015 = json.dumps(
        next((x for x in _d._DEUDAS if x["id"] == "D-015"), {}),
        ensure_ascii=False)

    parciales = []
    for nombre, c in _corridas().items():
        usados = {r["cd"] for r in c.get("resultados", [])}
        faltan = universo - usados
        if faltan and c.get("run_id", "") not in d015 and nombre not in d015:
            parciales.append(f"{nombre} omite {sorted(faltan)}")

    assert not parciales, (
        "hay corridas selladas cuyo universo es menor que el catálogo y que "
        "NO están reconocidas en `D-015`:\n  " + "\n  ".join(parciales)
        + "\n⚠️ Una corrida parcial no se corrige borrándola ni completando el "
          "universo a posteriori: se declara parcial, para que su cifra no se "
          "cite como el índice del período")


def test_BOOT_no_publica_una_cifra_de_SITA_sin_respaldo():
    """★ REGLA PROTEGIDA: **toda cifra del arranque debe poder señalar su
    fuente.**

    Es la `Regla de Oro 3` —«sin norma verificada, no hay dato»— aplicada a
    nosotros: si el sujeto observado debe acreditar lo que publica, el
    observador no puede publicar sin acreditar.

    ⚠️ No valida el cálculo: la fórmula `SITA` está verificada contra el
    Instructivo DPE 2024 y `BOOT` ordena ⛔ no tocarla. Valida la
    **procedencia de lo publicado**, que es otra cosa.

    Y no exige que `BOOT` publique todas las cifras. Exige que las que publique
    sean acreditables: **callar un valor no reconciliado es correcto;
    publicarlo con apariencia de dato firme, no.**

    ⚠️⚠️ SU PRIMERA VERSIÓN ACREDITABA CONTRA UN UNIVERSO DEMASIADO ESTRECHO
    —sólo corridas selladas y `PCD-D07`— y dio un **falso positivo** contra
    `0,4448`, que es el valor vigente: su respaldo estaba en la genealogía del
    repositorio (`76ca5de`), no en un artefacto de datos. Casi se retira de
    `BOOT` la única cifra correcta.

    Es `DOC-035` cometida por el propio verificador escrito para impedirla: **el
    alcance de la búsqueda es parte del resultado, también cuando quien busca es
    una prueba.** Por eso el registro de deuda —donde la genealogía queda
    escrita— entra ahora en el universo de acreditación."""
    linea = ""
    for ln in _BOOT.read_text(encoding="utf-8").splitlines():
        if "SITA" in ln and re.search(r"0,\d{3,4}", ln):
            linea = ln
            break
    if not linea:
        return  # BOOT no publica ninguna cifra de SITA: correcto y suficiente

    acreditadas: set[str] = set()

    def hurga(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "SITA" and isinstance(v, (int, float)):
                    acreditadas.add(f"{v:.4f}".replace(".", ","))
                hurga(v)
        elif isinstance(o, list):
            for x in o:
                hurga(x)

    for c in _corridas().values():
        hurga(c)

    # El universo de acreditación, declarado: artefactos de datos, expediente
    # y registro de deuda —donde vive la genealogía de una cifra cuyo origen
    # es un cambio de método y no una corrida conservada—.
    from app.agents import deuda as _d
    prosa = json.dumps([x for x in _d._DEUDAS], ensure_ascii=False)
    if _PCD07.is_file():
        prosa += _PCD07.read_text(encoding="utf-8")

    sin_respaldo = []
    for cifra in re.findall(r"0,\d{3,4}", linea):
        en_corrida = any(a.startswith(cifra) or cifra.startswith(a.rstrip("0"))
                         for a in acreditadas)
        if not en_corrida and cifra not in prosa:
            sin_respaldo.append(cifra)

    assert not sin_respaldo, (
        "`BOOT` publica cifras de SITA sin respaldo en ninguna corrida "
        "sellada, ni en `PCD-D07`, ni en el registro de deuda: "
        + " · ".join(sin_respaldo)
        + f"\nacreditadas por corridas: {sorted(acreditadas) or '—'}"
        + "\n⚠️ NO se corrige inventando el respaldo ni eligiendo una cifra "
          "cercana. Y antes de declarar una cifra sin respaldo, **revise la "
          "genealogía del repositorio** (`git log -S`): un valor puede venir "
          "de un cambio de método documentado en un commit y no de un "
          "artefacto de datos")


def test_un_sello_de_canon_no_acredita_el_universo_de_entrada():
    """★ REGLA PROTEGIDA: **mismo `vara_sha` no significa mismo estado de
    entrada.**

    Las dos corridas de 2025 comparten vara y catálogo, y difieren en más de
    medio punto. El sello acredita **la regla aplicada**, jamás el universo
    sobre el que se aplicó.

    ⚠️ Sin esta distinción, dos resultados con el mismo sello parecen
    contradecirse y se resuelve escogiendo el más cómodo. Con ella, la pregunta
    correcta deja de ser *«¿cuál cifra es la buena?»* —que invita a escoger— y
    pasa a ser *«¿qué diferencia de entrada produjo dos resultados bajo la
    misma vara?»*, que obliga a reconstruir.

    Es la misma familia que `no_procesable ≠ ausente` y `no_observable ≠
    incumplimiento`: **la trazabilidad de una parte no acredita el todo.**"""
    from app.agents import deuda as _d

    reg = {x["id"]: x for x in _d._DEUDAS}
    assert "D-015" in reg, (
        "desapareció `D-015`. Mientras el residuo de 2025 no se cierre, la "
        "deuda sostiene la regla")
    txt = json.dumps(reg["D-015"], ensure_ascii=False)
    assert "mismo `vara_sha` no significa" in txt, (
        "se perdió la regla que la forense dejó: un sello de canon acredita la "
        "regla aplicada, no el universo de entrada")
    # ⚠️ La genealogía completa debe quedar escrita, no sólo su conclusión.
    # Sin las cuatro cifras y su orden, la próxima lectura vuelve a encontrar
    # números sueltos y a sospechar del correcto — que es lo que pasó.
    for cifra in ("0,9719", "0,4630", "0,4646", "0,4448"):
        assert cifra in txt, (
            f"`D-015` dejó de registrar `{cifra}`. La genealogía se sostiene "
            "con las cuatro y su orden, no con la conclusión sola")
    assert "76ca5de" in txt, (
        "desapareció el commit que acredita el valor vigente. Sin esa "
        "referencia, `0,4448` vuelve a parecer una cifra sin origen")
    assert "VIGENTE" in txt, (
        "`D-015` dejó de declarar cuál es el valor vigente de 2025, que es "
        "precisamente lo que la genealogía estableció")
