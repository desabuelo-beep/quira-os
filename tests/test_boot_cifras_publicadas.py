# -*- coding: utf-8 -*-
"""
tests/test_boot_cifras_publicadas.py — ataque de `D-015`
════════════════════════════════════════════════════════════════════════════════
★ POR QUÉ EXISTE

`BOOT.md` es contexto operativo: se lee en cada arranque y **sus cifras se
propagan a todo lo que se escriba después**. Una cifra stale ahí no envejece en
silencio — contamina lecturas futuras.

Publicaba `SITA 2025 0,4448`, un valor que **no aparece en ningún otro lugar del
repositorio**. Ni en las corridas selladas de `d07`, ni en `PCD-D07`, ni en las
pruebas. Un número huérfano en el archivo que más se lee.

    Una cifra publicada en el arranque debe poder señalar su fuente.

Es la Regla de Oro 3 —«sin norma verificada, no hay dato»— aplicada a nuestro
propio estado: si el sujeto observado debe acreditar lo que publica, el
observador no puede publicar sin acreditar.

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


def _sita_de_las_corridas() -> set[str]:
    """Los `SITA` que las corridas selladas de `d07` acreditan, normalizados a
    cuatro decimales con coma — que es como `BOOT` los escribe."""
    out: set[str] = set()

    def hurga(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "SITA" and isinstance(v, (int, float)):
                    out.add(f"{v:.4f}".replace(".", ","))
                hurga(v)
        elif isinstance(o, list):
            for x in o:
                hurga(x)

    if _CORRIDAS.is_dir():
        for f in _CORRIDAS.glob("*.json"):
            hurga(json.loads(f.read_text(encoding="utf-8")))
    return out


def test_BOOT_no_publica_una_cifra_de_SITA_sin_respaldo():
    """★ ATAQUE DE `D-015` · REGLA PROTEGIDA: **toda cifra del arranque debe
    poder señalar su fuente.**

    `BOOT` publicaba `SITA 2025 0,4448`. Ese número no existe en las corridas
    selladas, ni en `PCD-D07`, ni en ninguna prueba: apareció en el archivo más
    leído del proyecto y nadie podía decir de dónde salía.

    ⚠️ Esta prueba **no valida el cálculo** — la fórmula `SITA` está verificada
    contra el Instructivo DPE 2024 y `BOOT` ordena ⛔ no tocarla. Valida la
    **procedencia de lo publicado**, que es una deuda distinta (`D-015`).

    Y no exige que `BOOT` publique todas las cifras: exige que **las que
    publique sean acreditables**. Callar un valor no reconciliado es correcto;
    publicarlo con apariencia de dato firme, no."""
    linea = ""
    for ln in _BOOT.read_text(encoding="utf-8").splitlines():
        if "SITA" in ln and re.search(r"0,\d{3,4}", ln):
            linea = ln
            break
    if not linea:
        return  # BOOT no publica ninguna cifra de SITA: correcto y suficiente

    acreditadas = _sita_de_las_corridas()
    pcd = _PCD07.read_text(encoding="utf-8") if _PCD07.is_file() else ""
    huerfanas = []
    for cifra in re.findall(r"0,\d{3,4}", linea):
        # una corrida sellada la acredita, o el expediente la afirma
        en_corrida = any(a.startswith(cifra) or cifra.startswith(a.rstrip("0"))
                         for a in acreditadas)
        if not en_corrida and cifra not in pcd:
            huerfanas.append(cifra)

    assert not huerfanas, (
        "`BOOT` publica cifras de SITA que ninguna corrida sellada de `d07` ni "
        "`PCD-D07` acreditan: " + " · ".join(huerfanas)
        + f"\nacreditadas por corridas: {sorted(acreditadas) or '—'}"
        + "\n⚠️ NO se corrige inventando el respaldo ni eligiendo una cifra "
          "cercana: se publica la que la fuente sostiene, o no se publica "
          "ninguna (D-015)")


def test_la_deuda_D015_sigue_registrada_mientras_2025_no_se_reconcilie():
    """★ REGLA PROTEGIDA: **el hueco no se cierra al dejar de mirarlo.**

    Quitar `0,4448` de `BOOT` corrige lo publicado y **no resuelve** por qué
    hay dos corridas `COMPLETED` del mismo año, mismos doce meses y mismo
    `vara_sha` con `0,9719` y `0,4630`.

    ⚠️ Si esta prueba estorbara algún día, la salida no es borrarla: es cerrar
    `D-015` determinando qué corrida es la vigente para 2025."""
    from app.agents import deuda as _d

    reg = {x["id"]: x for x in _d._DEUDAS}
    assert "D-015" in reg, (
        "desapareció `D-015`. El valor de `SITA 2025` sigue sin reconciliar "
        "mientras existan dos corridas selladas discrepantes")
    txt = json.dumps(reg["D-015"], ensure_ascii=False)
    assert "0,9719" in txt and "0,4630" in txt, (
        "la deuda dejó de nombrar las dos corridas discrepantes, que son la "
        "evidencia concreta de que el valor no está determinado")
    assert "NO DETERMINABLE" in txt, (
        "se perdió el tercer estado. Sin él, `D-015` se leería como «falta "
        "calcularlo» cuando lo que falta es decidir cuál es la fuente")
