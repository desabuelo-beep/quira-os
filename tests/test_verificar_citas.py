# -*- coding: utf-8 -*-
"""Ninguna cita normativa sin leer su fuente — pruebas del verificador.

Cada caso reproduce un error REAL (PANORAMA §5-duoquinquagies · §5-terquinquagies ·
§5-quinquinquagies). Los casos A–E son la demostración que pidió el colega antes de
aceptar el mecanismo:
  A · cita válida → pasa
  B · artículo real usado como rector equivocado (COOTAD 266 para la rendición) → bloquea
  C · artículo inexistente → bloquea
  D · artículo correcto fuera de la cadena → bloquea si no se declara; pasa si se declara
  E · paráfrasis → NO se finge verificada: la cita literal falsa bloquea; la paráfrasis
      queda contada como «contenido no verificado»
Índice sintético: las pruebas no tocan la base ni lanzan procesos.
"""
import io
import json
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
        "eeeeeeeeeeee": ["LOPC", "89", "Art. 89 Definición"],
        "ffffffffffff": ["COOTAD", "266", "Art. 266.- Rendición de Cuentas"],
        "999999999999": ["COOTAD", "249", "Art. 249.- Presupuesto para los grupos"],
    },
    "arts": {"LOPC": ["89", "90", "92", "95"], "COOTAD": ["215", "233", "249", "266"], "CE": ["12", "264"],
             "LOPAM": ["14", "84"], "LODISC": ["47", "116"], "LOTAIP": ["19", "42"]},
}
TEXTOS = {"999999999999": vc._comparable(
    "Art. 249.- Presupuesto para los grupos de atención prioritaria.- No se aprobará el presupuesto "
    "del gobierno autónomo descentralizado si en el mismo no se asigna, por lo menos, el diez por "
    "ciento (10%) de sus ingresos no tributarios para el financiamiento de la planificación y "
    "ejecución de programas sociales para la atención a grupos de atención prioritaria.")}
RDC = {"id": "CNO-IX-001", "titulo": "Obligación de Rendición de Cuentas del GAD",
       "cadena": {("LOPC", "89"), ("LOPC", "90")}, "claves": {"rendicion", "cuentas"}}


def _r(texto, *, cnos=(), textos=None):
    return vc.auditar(texto, idx=IDX, cnos=list(cnos), textos=textos)


def _v(texto, **kw):
    r = _r(texto, **kw)
    return r.hallazgos, [m for _, m in r.fuera_de_cadena]


# ── A · la cita válida pasa ────────────────────────────────────────────────────
def test_A_cita_valida_de_la_cadena_pasa():
    h, f = _v("la rendición de cuentas la define LOPC 89 `eeeeeeeeeeee`", cnos=[RDC])
    assert h == [] and f == []


def test_A_continuacion_atribuye_al_ultimo_articulo():
    assert _v("COOTAD 215 · 233 `bbbbbbbbbbbb` · 266")[0] == []


def test_A_numerales_no_son_articulos():
    assert _v("CE 264 núm. 3 (vialidad) · 4 (agua) · 13 (incendios) `cccccccccccc`")[0] == []


def test_A_vineta_partida_en_dos_lineas_es_una_cita():
    assert _v("- CE 264 núm. 3 (vialidad) · 7\n  (equipamientos) · 13 (incendios) `cccccccccccc`")[0] == []


def test_A_sigla_arrastrada_en_la_misma_linea():
    assert _v("LOPAM 14 (exoneraciones) · 84 `dddddddddddd` (atribuciones)")[0] == []


def test_A_version_de_ley_no_es_articulo():
    assert _v("bajo LOTAIP 2.0 la DPE centraliza el registro")[0] == []


def test_A_articulo_con_numeral_por_punto():
    assert _v("competencia del CE 264.4 y del COOTAD 233")[0] == []


def test_A_flecha_de_renumeracion_atribuye_al_nuevo_articulo():
    assert _v("COOTAD 215 → **233** (plazo `bbbbbbbbbbbb`)")[0] == []


# ── B · artículo real, rector equivocado (falsación 43) → bloquea ──────────────
def test_B_articulo_real_usado_como_rector_equivocado_bloquea():
    h, f = _v("la rendición de cuentas es anual según COOTAD 266 `ffffffffffff`", cnos=[RDC])
    assert h == []                                   # la huella es correcta y el artículo existe…
    assert len(f) == 1 and "COOTAD 266" in f[0]      # …pero no es el rector: bloquea
    assert "LOPC 89" in f[0]                         # y devuelve la cadena rectora


def test_B_huella_de_otro_articulo_es_hallazgo():
    h, _ = _v("la periodicidad está en LOPC 95 `aaaaaaaaaaaa`")
    assert len(h) == 1 and "LOPC 92" in h[0]


# ── C · artículo inexistente → bloquea ─────────────────────────────────────────
def test_C_articulo_inexistente_con_alias_de_sigla():
    h, _ = _v("es infracción expresa (LOD Art. 563)")
    assert len(h) == 1 and "LODISC 563" in h[0]


# ── D · artículo correcto fuera de la cadena → declarar o bloquear ─────────────
def test_D_eslabon_faltante_sin_declarar_bloquea():
    _, f = _v("la rendición de cuentas se hace una vez al año (LOPC 95)", cnos=[RDC])
    assert len(f) == 1 and "LOPC 95" in f[0]


def test_D_eslabon_faltante_declarado_pasa():
    _, f = _v("la rendición de cuentas se hace una vez al año (LOPC 95, eslabón faltante)", cnos=[RDC])
    assert f == []


def test_D_concordancia_declarada_pasa():
    _, f = _v("concordancia de la rendición de cuentas: COOTAD 266", cnos=[RDC])
    assert f == []


# ── E · paráfrasis: no se finge verificada ─────────────────────────────────────
def test_E_cita_literal_falsa_bloquea():
    r = _r("COOTAD 249 `999999999999` — «el diez por ciento de sus ingresos tributarios»", textos=TEXTOS)
    assert len(r.hallazgos) == 1 and "NO está en el artículo" in r.hallazgos[0]


def test_E_cita_literal_verdadera_se_cuenta_verificada():
    r = _r("COOTAD 249 `999999999999` — «No se aprobará el presupuesto del gobierno autónomo "
           "descentralizado si en el mismo no se asigna»", textos=TEXTOS)
    assert r.hallazgos == [] and r.literales == 1 and r.no_verificadas == 0


def test_E_parafrasis_falsa_no_se_finge_verificada():
    """La paráfrasis dice otra cosa que la ley. La máquina no puede saberlo, y no lo
    finge: no hay hallazgo, no hay «literal verificada», y queda contada como contenido
    no verificado para la validación humana."""
    r = _r("COOTAD 249 `999999999999` obliga a destinar el 10 % del presupuesto no salarial",
           textos=TEXTOS)
    assert r.hallazgos == [] and r.literales == 0 and r.no_verificadas == 1


def test_E_comillas_de_afirmacion_no_son_texto_de_ley():
    r = _r("COOTAD 249 `999999999999` — el catálogo decía “el 10 % del presupuesto no salarial”",
           textos=TEXTOS)
    assert r.hallazgos == [] and r.no_verificadas == 1


# ── El mecanismo: el hook y la línea base ──────────────────────────────────────
def test_el_hook_bloquea_el_caso_B(monkeypatch, capsys):
    """El código del hook está versionado aunque su activación sea local."""
    monkeypatch.setattr(vc, "cargar_indice", lambda *a, **k: IDX)
    monkeypatch.setattr(vc, "cargar_cnos", lambda: [RDC])
    monkeypatch.setattr(vc, "textos_de", lambda h: {})
    entrada = json.dumps({"tool_name": "Edit", "tool_input": {
        "file_path": "x.md", "new_string": "la rendición de cuentas es anual según COOTAD 266"}})
    monkeypatch.setattr(sys, "stdin", io.TextIOWrapper(io.BytesIO(entrada.encode("utf-8")), encoding="utf-8"))
    vc.modo_hook()
    salida = json.loads(capsys.readouterr().out)
    assert salida["decision"] == "block" and "COOTAD 266" in salida["reason"]


def test_la_clave_de_cadena_no_depende_del_corpus():
    """El gate corre la regla de cadena también sin corpus (CI): la clave debe ser la misma."""
    linea = "la rendición de cuentas es anual según CE 264.4"
    con = vc.auditar(linea, idx=IDX, cnos=[RDC]).fuera_de_cadena
    sin = vc.auditar(linea, idx=None, cnos=[RDC], siglas={"CE", "LOPC"}).fuera_de_cadena
    assert [c for c, _ in con] == [c for c, _ in sin]


def test_cita_retirada_o_ajena_no_es_cita_propia():
    """El registro tiene que poder nombrar una cita falsa para registrarla."""
    assert _v("se corrigió ~~LOD Art. 563~~ → LODISC 116")[0] == []
    assert _v("el catálogo decía “LOTAIP Art. 47”, que no existe")[0] == []
    assert len(_v("el catálogo decía LOTAIP Art. 47")[0]) == 1      # sin marca, sí se lee
