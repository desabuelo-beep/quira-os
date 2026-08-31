# -*- coding: utf-8 -*-
"""
tests/test_canon_derivado.py — el estado de lo construido, sin depender de memoria
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30). En una sola sesión el director propuso tres veces
reconstruir cosas que ya existían: la matriz jurídica de d09 (vigente, 10/10
SHA), los artículos que iba a buscar en Supabase (estaban en `docs/brn/`), y una
degradación a «advisory» contra un CNO que ya modela d09 como obligación de
hacer. Javo lo nombró antes de que se viera el tercero:

> *«hay que hacer algo para navegar toda la documentación y no perder contexto
> de todo lo que tenemos construido»*

La respuesta no fue otro documento —envejecen en silencio— sino **derivar el
estado y poder atacarlo**, que es lo que estas pruebas hacen.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import canon as C                        # noqa: E402


# ── CRITERIOS ─────────────────────────────────────────────────────────────────
def test_el_inventario_deriva_el_dominio_del_canon_y_no_del_numeral():
    """`CNO-IV` es de **d02**, no de d04. El romano no es el número del dominio,
    así que el mapeo se lee de `opera_en` en la RO. Suponerlo sería inferir el
    dueño de una cadena normativa — justo lo que el sistema no se permite."""
    fam = C._familia_a_dominio()
    assert fam.get("IV") == "d02", f"el mapeo romano→dominio se rompió: {fam}"
    assert fam.get("IX") == "d09"
    assert fam.get("I") == "d01"


def test_los_sha_coinciden_con_la_matriz_de_cobertura():
    """VALIDACIÓN CRUZADA contra fuente independiente: `BRN_MATRIZ_COBERTURA.md`
    se escribió a mano, mucho antes que este módulo. Si el inventario derivado y
    la matriz escrita divergen, uno de los dos miente y hay que saberlo."""
    matriz = (RAIZ / "docs" / "architecture" / "BRN_MATRIZ_COBERTURA.md")
    if not matriz.exists():
        import pytest
        pytest.skip("no está la matriz de cobertura")
    texto = matriz.read_text(encoding="utf-8", errors="replace")

    for dom, esperado in (("d09", "10/10"), ("d02", "6/6"), ("d03", "9/9")):
        e = C.estado_canonico(dom)
        derivado = f"{e['sha_sellados']}/{e['sha_totales']}"
        assert derivado == esperado, (
            f"{dom}: el inventario deriva {derivado} y la matriz dice {esperado}")
        assert esperado in texto, f"la matriz ya no declara {esperado} para {dom}"


def test_d07_es_el_unico_que_carga_su_regla_operativa():
    """El estado medido hoy, con trinquete hacia arriba: si otro dominio empieza
    a cargarla, esta prueba lo obliga a constar; si d07 dejara de hacerlo, se
    entera alguien. No juzga si la implementa bien — dice si la tiene delante."""
    c = C.cobertura_canonica()
    cargan = [f["dominio"] for f in c["dominios"]
              if f["vinculo_con_el_motor"] == C.CARGA]
    assert "d07" in cargan
    assert set(c["con_ro_vigente_sin_cargarla"]) >= {"d09"}, (
        "d09 tiene RO-IX-001 vigente; si dejara de aparecer aquí sería porque "
        "empezó a cargarla — y eso hay que celebrarlo, no esconderlo")


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_un_cno_sin_RO_no_puede_desaparecer_del_inventario():
    """REGRESIÓN de un falso negativo REAL de este mismo módulo.

    La primera versión navegaba `dominio ← RO ← CNO`. Los siete `CNO-VIII-00x`
    que **ninguna RO reclama** eran por eso invisibles, y d08 reportaba 3/3 SHA
    cuando tiene 29/29. Un canon huérfano es un tramo ANTES del problema de d09:
    allí la regla existe y el motor no la carga; aquí la cadena se modeló y
    nunca llegó a ser regla. Invisibilizarlo es la peor de las dos."""
    e = C.estado_canonico("d08")
    assert len(e["cno_huerfanos"]) >= 7, (
        "volvieron a perderse los CNO que ninguna RO deriva")
    assert e["sha_totales"] >= 29, (
        f"d08 reporta {e['sha_totales']} eslabones: se está contando sólo lo "
        f"que alguna RO alcanza")


def test_ataque_citar_la_regla_no_cuenta_como_cargarla():
    """`d09/fuentes.py` nombra RO-IX-001 en un docstring. Eso no es obedecerla.

    Es la misma lección que costó cuatro correcciones en la escalera de
    apropiación: **la mención no es el uso**. Si el inventario aceptara la cita,
    d09 aparecería conforme y el hallazgo de hoy no existiría."""
    e = C.estado_canonico("d09")
    assert e["vinculo_con_el_motor"] == C.CITA
    assert e["modulos_que_la_nombran"], "d09 sí nombra su RO en alguna parte"
    assert C.CARGA != e["vinculo_con_el_motor"]


def test_ataque_el_inventario_no_recuenta_los_ataques_por_su_cuenta():
    """No reimplementa lo que `apropiacion` ya deriva. Dos formas de contar lo
    mismo divergen siempre —`test_12` se rompió cuatro veces por eso— y un
    inventario que contradice a otro es peor que no tener ninguno."""
    from app.agents import apropiacion as A

    fuente = (RAIZ / "app" / "agents" / "canon.py").read_text(encoding="utf-8")
    assert "def test_" not in fuente and "adversarial" not in fuente, (
        "canon.py está deduciendo ataques por su cuenta en vez de consumirlos")

    oficial = {f["dominio"]: f.get("ataques_ejecutados", 0)
               for f in A.cobertura_de_la_plataforma()["dominios"]}
    for fila in C.cobertura_canonica()["dominios"]:
        if fila["dominio"] in oficial:
            assert fila["ataques_ejecutados"] == oficial[fila["dominio"]]


def test_ataque_un_dominio_sin_RO_no_se_reporta_como_incumplidor():
    """Sin RO vigente no hay regla que cargar, y eso **no es un incumplimiento**:
    es una etapa anterior. Colapsarlos acusaría de desobedecer a quien todavía
    no tiene qué obedecer — el mismo error que el dominio persigue afuera."""
    c = C.cobertura_canonica()
    for fila in c["dominios"]:
        if not fila["ro_vigentes"]:
            assert fila["dominio"] not in c["con_ro_vigente_sin_cargarla"]


def test_la_afirmacion_se_compone_del_estado_medido():
    """No hay frase escrita a mano: si cambia el estado, cambia la frase. Un
    texto fijo sobreviviría a la corrección del defecto que describe."""
    c = C.cobertura_canonica()
    frase = c["afirmacion_sostenible"]
    for d in c["con_ro_vigente_sin_cargarla"]:
        assert d in frase, f"{d} no aparece en la afirmación que lo describe"
    assert "d07" in frase


def test_el_inventario_responde_lo_que_hoy_nadie_podia_consultar():
    """La prueba de propósito. Estas cuatro preguntas son exactamente las que se
    respondieron mal hoy por no poder consultarlas."""
    e = C.estado_canonico("d09")
    assert e["cno_vigentes"] == ["CNO-IX-001"]      # ¿existe el canon jurídico?
    assert e["sha_sellados"] == 10                  # ¿está sellado?
    assert e["ro_vigentes"] == ["RO-IX-001"]        # ¿hay regla operativa?
    assert e["vinculo_con_el_motor"] != C.CARGA     # ¿el motor la obedece?
