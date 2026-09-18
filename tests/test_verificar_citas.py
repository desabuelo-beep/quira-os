# -*- coding: utf-8 -*-
"""Ninguna cita normativa sin leer su fuente — pruebas del verificador.

Cada caso reproduce un error REAL encontrado el 2026-09-18 (PANORAMA §5-duoquinquagies y
§5-terquinquagies): la rendición de cuentas fundada en COOTAD 266 en vez de su cadena
rectora (falsación 43), un «LOD Art. 563» que no existe, una huella atribuida al artículo
equivocado. Índice sintético: las pruebas no tocan la base.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "normativa"))

import verificar_citas as vc  # noqa: E402

IDX = {
    "huella": {
        "aaaaaaaaaaaa": ["LOPC", "92", "Art. 92 Del nivel político"],
        "bbbbbbbbbbbb": ["COOTAD", "233", "Art. 233.- Plazo"],
        "cccccccccccc": ["CE", "264", "Art. 264.- Los gobiernos municipales"],
        "dddddddddddd": ["LOPAM", "84", "Art. 84.- Atribuciones de los GAD"],
    },
    "arts": {"LOPC": ["89", "90", "92", "95"], "COOTAD": ["215", "233", "266"], "CE": ["12", "264"],
             "LOPAM": ["14", "84"], "LODISC": ["47", "116"], "LOTAIP": ["19", "42"]},
}
RDC = {"id": "CNO-IX-001", "titulo": "Obligación de Rendición de Cuentas del GAD",
       "cadena": {("LOPC", "89"), ("LOPC", "90")}, "claves": {"rendicion", "cuentas"}}


def _v(texto, *, cnos=(), existencia=True, rector=False):
    return vc.verificar_texto(texto, IDX, list(cnos), existencia=existencia, rector=rector)


def test_huella_de_otro_articulo_es_hallazgo():
    h, _ = _v("la periodicidad está en LOPC 95 `aaaaaaaaaaaa`")
    assert len(h) == 1 and "LOPC 92" in h[0]


def test_continuacion_atribuye_al_ultimo_articulo():
    h, _ = _v("COOTAD 215 · 233 `bbbbbbbbbbbb` · 266")
    assert h == []


def test_numerales_no_son_articulos():
    h, _ = _v("CE 264 núm. 3 (vialidad) · 4 (agua) · 13 (incendios) `cccccccccccc`")
    assert h == []


def test_vineta_partida_en_dos_lineas_es_una_cita():
    h, _ = _v("- CE 264 núm. 3 (vialidad) · 7\n  (equipamientos) · 13 (incendios) `cccccccccccc`")
    assert h == []


def test_sigla_arrastrada_en_la_misma_linea():
    h, _ = _v("LOPAM 14 (exoneraciones) · 84 `dddddddddddd` (atribuciones)")
    assert h == []


def test_articulo_inexistente_con_alias_de_sigla():
    h, _ = _v("es infracción expresa (LOD Art. 563)")
    assert len(h) == 1 and "LODISC 563" in h[0]


def test_version_de_ley_no_es_articulo():
    h, _ = _v("bajo LOTAIP 2.0 la DPE centraliza el registro")
    assert h == []


def test_articulo_con_numeral_por_punto():
    h, _ = _v("competencia del CE 264.4 y del COOTAD 233")
    assert h == []


def test_falsacion_43_dispara_el_aviso_de_rector():
    _, avisos = _v("la rendición de cuentas es anual según COOTAD 266", cnos=[RDC], rector=True)
    assert len(avisos) == 1 and "COOTAD 266" in avisos[0] and "LOPC 89" in avisos[0]


def test_concordancia_declarada_no_avisa():
    _, avisos = _v("concordancia de la rendición de cuentas: COOTAD 266", cnos=[RDC], rector=True)
    assert avisos == []


def test_eslabon_de_la_cadena_no_avisa():
    _, avisos = _v("la rendición de cuentas la define LOPC 89", cnos=[RDC], rector=True)
    assert avisos == []


def test_flecha_de_renumeracion_atribuye_al_nuevo_articulo():
    h, _ = _v("COOTAD 215 → **233** (plazo `bbbbbbbbbbbb`)")
    assert h == []
