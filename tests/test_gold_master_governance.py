"""
Tests: Gobernanza Gold Master — QUIRA Intelligence (Sprint 3 · P4)

Cobertura:
  - ResultadoValidacion (dataclass)
  - validar_gold_master()
  - obtener_changelog_gm()
  - respaldar_gold_master()
  - obtener_estado_gm()
  - Helpers internos (_calcular_sha256, _resolver_ruta_gm)

Doctrina: un sistema con memoria necesita gobernanza de cambios.
El Gold Master es infraestructura epistemológica — no solo un Excel.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.services.gold_master_governance import (
    CLAVES_OUTPUT_API_REQUERIDAS,
    HOJAS_REQUERIDAS_V6,
    ResultadoValidacion,
    _calcular_sha256,
    _resolver_ruta_gm,
    obtener_changelog_gm,
    obtener_estado_gm,
    respaldar_gold_master,
    validar_gold_master,
)


# ══════════════════════════════════════════════════════════════════════════════
# Fixtures compartidas
# ══════════════════════════════════════════════════════════════════════════════

def _crear_excel_mock(hojas: list[str], filas_api: list[tuple] | None = None) -> MagicMock:
    """Crea un workbook openpyxl simulado con hojas y datos de G6.1."""
    wb_mock = MagicMock()
    wb_mock.sheetnames = hojas

    # Fila por defecto de G1.1_CONFIG
    fila_version  = ("VERSION_GOLD_MASTER", "v6.0", "Versión canónica")
    fila_fecha    = ("FECHA_CORTE", "2026-05-18", "Fecha de corte")

    # Filas por defecto de G6.1_OUTPUT_API
    filas_default = filas_api or [
        ("ICPI_GLOBAL",        0.6685, "ICPI ratio"),
        ("ICPI_GLOBAL_PCT",    66.85,  "ICPI pct"),
        ("ICPI_CLASIFICACION", "Transición Crítica", "Nivel AVEP"),
        ("PSG_EJECUCION",      0.5985, "Ejecución GAD"),
        ("PSG_FIDELIDAD",      0.6993, "Fidelidad D2"),
        ("SAT_RIESGO_TOTAL",   0.70,   "Score SAT"),
        ("SAT_CLASIF_RIESGO",  "ALTO", "Clasificación"),
        ("SAT_ACTIVAS_COUNT",  2,      "Alertas activas"),
        ("TGI_SCORE",          66.85,  "TGI Score"),
        ("TGI_D1",             83.5,   "D1"),
        ("TGI_D2",             69.93,  "D2"),
        ("TGI_D3",             59.85,  "D3"),
        ("TGI_D4",             66.85,  "D4"),
        ("TGI_D5",             100.0,  "D5"),
    ]

    def _ws_mock_g61():
        ws = MagicMock()
        ws.iter_rows.return_value = iter(filas_default)
        return ws

    def _ws_mock_g11():
        ws = MagicMock()
        ws.iter_rows.return_value = iter([fila_version, fila_fecha])
        return ws

    def _ws_mock_generico():
        ws = MagicMock()
        ws.iter_rows.return_value = iter([])
        return ws

    def _getitem(nombre):
        if nombre == "G6.1_OUTPUT_API":
            return _ws_mock_g61()
        if nombre == "G1.1_CONFIG":
            return _ws_mock_g11()
        return _ws_mock_generico()

    wb_mock.__getitem__ = MagicMock(side_effect=_getitem)
    wb_mock.close = MagicMock()
    return wb_mock


# ══════════════════════════════════════════════════════════════════════════════
# Clase 1: ResultadoValidacion
# ══════════════════════════════════════════════════════════════════════════════

class TestResultadoValidacion:
    """Verifica comportamiento del dataclass ResultadoValidacion."""

    def test_instancia_ok(self):
        r = ResultadoValidacion("estructura", "hoja_existe", "OK", "Hoja G3.1 presente")
        assert r.estado == "OK"
        assert not r.es_error()
        assert not r.es_alerta()

    def test_instancia_error(self):
        r = ResultadoValidacion("estructura", "hoja_ausente", "ERROR", "Hoja G3.1 faltante")
        assert r.es_error()
        assert not r.es_alerta()

    def test_instancia_alerta(self):
        r = ResultadoValidacion("contrato_api", "clave_nula", "ALERTA", "Clave presente pero None")
        assert r.es_alerta()
        assert not r.es_error()

    def test_campos_opcionales_por_defecto(self):
        r = ResultadoValidacion("version", "version_ok", "OK", "v6.0")
        assert r.valor is None
        assert r.esperado is None

    def test_campos_completos(self):
        r = ResultadoValidacion(
            "integridad", "rango_icpi", "OK",
            "ICPI en rango", valor=66.85, esperado="[0,100]"
        )
        assert r.valor == 66.85
        assert r.esperado == "[0,100]"

    def test_categoria_contrato_api(self):
        r = ResultadoValidacion("contrato_api", "clave_x", "OK", "OK")
        assert r.categoria == "contrato_api"


# ══════════════════════════════════════════════════════════════════════════════
# Clase 2: validar_gold_master
# ══════════════════════════════════════════════════════════════════════════════

class TestValidarGoldMaster:
    """Tests para la función de validación canónica."""

    def test_archivo_inexistente_retorna_error(self, tmp_path):
        ruta_falsa = tmp_path / "no_existe.xlsx"
        resultados = validar_gold_master(str(ruta_falsa))
        assert len(resultados) == 1
        assert resultados[0].es_error()
        assert resultados[0].regla == "archivo_existe"

    def test_archivo_inexistente_termina_temprano(self, tmp_path):
        """Sin archivo no debe verificar hojas ni API."""
        ruta_falsa = tmp_path / "no_existe.xlsx"
        resultados = validar_gold_master(str(ruta_falsa))
        reglas = [r.regla for r in resultados]
        assert "hoja_requerida:G3.1_D1_LEGALIDAD" not in reglas

    @patch("app.services.gold_master_governance.openpyxl")
    def test_todas_hojas_presentes_dan_ok(self, mock_openpyxl, tmp_path):
        """Cuando todas las hojas requeridas están, no debe haber ERROR de estructura."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        errores_estructura = [
            r for r in resultados
            if r.categoria == "estructura" and r.es_error()
            and r.regla.startswith("hoja_requerida")
        ]
        assert len(errores_estructura) == 0

    @patch("app.services.gold_master_governance.openpyxl")
    def test_hoja_faltante_da_error(self, mock_openpyxl, tmp_path):
        """Falta de hoja requerida debe generar ERROR."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        hojas_incompletas = [h for h in HOJAS_REQUERIDAS_V6 if h != "G3.3_D3_EJECUCION_GAD"]
        wb_mock = _crear_excel_mock(hojas_incompletas)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        reglas_error = [r.regla for r in resultados if r.es_error()]
        assert "hoja_requerida:G3.3_D3_EJECUCION_GAD" in reglas_error

    @patch("app.services.gold_master_governance.openpyxl")
    def test_claves_api_presentes_dan_ok(self, mock_openpyxl, tmp_path):
        """Con todas las claves de contrato API, no debe haber ERRORs de contrato."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        errores_api = [
            r for r in resultados
            if r.categoria == "contrato_api" and r.es_error()
        ]
        assert len(errores_api) == 0

    @patch("app.services.gold_master_governance.openpyxl")
    def test_clave_api_faltante_da_error(self, mock_openpyxl, tmp_path):
        """Clave ausente en G6.1 debe generar ERROR de contrato."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        # Filas sin TGI_SCORE
        filas = [(c, None, "") for c in CLAVES_OUTPUT_API_REQUERIDAS if c != "TGI_SCORE"]
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6, filas_api=filas)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        reglas_error = [r.regla for r in resultados if r.es_error()]
        assert "clave_api:TGI_SCORE" in reglas_error

    @patch("app.services.gold_master_governance.openpyxl")
    def test_clave_api_con_valor_none_da_alerta(self, mock_openpyxl, tmp_path):
        """Clave presente pero con valor None debe generar ALERTA, no ERROR."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        filas = [("TGI_SCORE", None, "pendiente")] + [
            (c, 10.0, "") for c in CLAVES_OUTPUT_API_REQUERIDAS if c != "TGI_SCORE"
        ]
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6, filas_api=filas)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        r_tgi = next((r for r in resultados if r.regla == "clave_api:TGI_SCORE"), None)
        assert r_tgi is not None
        assert r_tgi.es_alerta()

    @patch("app.services.gold_master_governance.openpyxl")
    def test_rango_metrica_fuera_de_rango_da_error(self, mock_openpyxl, tmp_path):
        """ICPI_GLOBAL fuera de [0,1] debe generar ERROR de integridad."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        filas = [("ICPI_GLOBAL", 150.0, "fuera de rango")] + [
            (c, 0.5, "") for c in CLAVES_OUTPUT_API_REQUERIDAS if c != "ICPI_GLOBAL"
        ]
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6, filas_api=filas)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        r_rango = next(
            (r for r in resultados if r.regla == "rango_metrica:ICPI_GLOBAL"), None
        )
        assert r_rango is not None
        assert r_rango.es_error()

    @patch("app.services.gold_master_governance.openpyxl")
    def test_rango_metrica_correcto_da_ok(self, mock_openpyxl, tmp_path):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        r_icpi = next(
            (r for r in resultados if r.regla == "rango_metrica:ICPI_GLOBAL"), None
        )
        assert r_icpi is not None
        assert r_icpi.estado == "OK"

    @patch("app.services.gold_master_governance.openpyxl")
    def test_version_v6_da_ok(self, mock_openpyxl, tmp_path):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        r_ver = next((r for r in resultados if r.regla == "version_declarada"), None)
        assert r_ver is not None
        assert r_ver.estado == "OK"

    @patch("app.services.gold_master_governance.openpyxl")
    def test_version_no_v6_da_alerta(self, mock_openpyxl, tmp_path):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        # Simular G1.1 con versión v5.5
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        ws_g11 = MagicMock()
        ws_g11.iter_rows.return_value = iter([
            ("VERSION_GOLD_MASTER", "v5.5", "Versión antigua")
        ])
        wb_mock.__getitem__.side_effect = lambda n: (
            ws_g11 if n == "G1.1_CONFIG"
            else _crear_excel_mock(HOJAS_REQUERIDAS_V6)[n]
        )
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        r_ver = next((r for r in resultados if r.regla == "version_declarada"), None)
        assert r_ver is not None
        assert r_ver.es_alerta()

    @patch("app.services.gold_master_governance.openpyxl")
    def test_resultado_incluye_multiple_categorias(self, mock_openpyxl, tmp_path):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_openpyxl.load_workbook.return_value = wb_mock

        resultados = validar_gold_master(str(ruta))
        categorias = {r.categoria for r in resultados}
        assert "estructura" in categorias
        assert "contrato_api" in categorias
        assert "integridad" in categorias
        assert "version" in categorias

    @patch("app.services.gold_master_governance.openpyxl")
    def test_apertura_fallida_retorna_error(self, mock_openpyxl, tmp_path):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"dummy")
        mock_openpyxl.load_workbook.side_effect = Exception("Archivo corrupto")

        resultados = validar_gold_master(str(ruta))
        reglas = [r.regla for r in resultados]
        assert "apertura_workbook" in reglas
        assert resultados[-1].es_error()


# ══════════════════════════════════════════════════════════════════════════════
# Clase 3: obtener_changelog_gm
# ══════════════════════════════════════════════════════════════════════════════

class TestObtenerChangelogGm:
    """Tests del historial de versiones del Gold Master."""

    def test_changelog_inexistente_retorna_error(self, tmp_path):
        ruta_falsa = tmp_path / "no_existe.json"
        resultado = obtener_changelog_gm(str(ruta_falsa))
        assert resultado["error"] is not None
        assert resultado["versiones"] == []
        assert resultado["total_versiones"] == 0

    def test_changelog_existente_retorna_versiones(self, tmp_path):
        datos = {
            "versiones": [
                {"version": "v6.0", "fecha": "2026-05-25", "estado": "ACTIVO"},
                {"version": "v5.5", "fecha": "2026-05-18", "estado": "CONGELADO"},
            ]
        }
        ruta = tmp_path / "changelog.json"
        ruta.write_text(json.dumps(datos), encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert resultado["error"] is None
        assert resultado["total_versiones"] == 2

    def test_changelog_detecta_version_activa(self, tmp_path):
        datos = {
            "versiones": [
                {"version": "v6.0", "estado": "ACTIVO"},
                {"version": "v5.5", "estado": "CONGELADO"},
            ]
        }
        ruta = tmp_path / "changelog.json"
        ruta.write_text(json.dumps(datos), encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert resultado["version_activa"] == "v6.0"

    def test_changelog_sin_version_activa(self, tmp_path):
        datos = {"versiones": [{"version": "v5.5", "estado": "CONGELADO"}]}
        ruta = tmp_path / "changelog.json"
        ruta.write_text(json.dumps(datos), encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert resultado["version_activa"] is None

    def test_changelog_json_malformado_retorna_error(self, tmp_path):
        ruta = tmp_path / "mal.json"
        ruta.write_text("{esto no es json válido", encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert resultado["error"] is not None

    def test_changelog_vacio_retorna_lista_vacia(self, tmp_path):
        datos = {"versiones": []}
        ruta = tmp_path / "changelog.json"
        ruta.write_text(json.dumps(datos), encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert resultado["versiones"] == []
        assert resultado["total_versiones"] == 0
        assert resultado["error"] is None

    def test_changelog_retorna_estructura_completa(self, tmp_path):
        datos = {"versiones": [{"version": "v6.0", "estado": "ACTIVO"}]}
        ruta = tmp_path / "changelog.json"
        ruta.write_text(json.dumps(datos), encoding="utf-8")

        resultado = obtener_changelog_gm(str(ruta))
        assert "versiones" in resultado
        assert "version_activa" in resultado
        assert "total_versiones" in resultado
        assert "error" in resultado


# ══════════════════════════════════════════════════════════════════════════════
# Clase 4: respaldar_gold_master
# ══════════════════════════════════════════════════════════════════════════════

class TestRespaldarGoldMaster:
    """Tests del sistema de respaldo firmado SHA-256."""

    def test_archivo_inexistente_retorna_error(self, tmp_path):
        ruta_falsa = tmp_path / "no_existe.xlsx"
        resultado = respaldar_gold_master(str(ruta_falsa), str(tmp_path))
        assert resultado["estado"] == "error"
        assert resultado["error"] is not None

    def test_respaldo_exitoso_crea_archivo(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"contenido de prueba del gold master")
        destino = tmp_path / "backups"

        resultado = respaldar_gold_master(str(origen), str(destino))

        assert resultado["estado"] == "ok"
        assert resultado["ruta_respaldo"] is not None
        assert Path(resultado["ruta_respaldo"]).exists()

    def test_respaldo_genera_sha256(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        contenido = b"datos epistemologicos del gold master"
        origen.write_bytes(contenido)

        resultado = respaldar_gold_master(str(origen), str(tmp_path))

        assert resultado["sha256"] is not None
        assert len(resultado["sha256"]) == 64  # SHA-256 = 64 hex chars

    def test_sha256_es_correcto(self, tmp_path):
        import hashlib
        origen = tmp_path / "gm_test.xlsx"
        contenido = b"verificacion sha256 gold master quira"
        origen.write_bytes(contenido)
        sha_esperado = hashlib.sha256(contenido).hexdigest()

        resultado = respaldar_gold_master(str(origen), str(tmp_path))
        assert resultado["sha256"] == sha_esperado

    def test_respaldo_crea_archivo_firma_json(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos de prueba")
        destino = tmp_path / "backups"

        resultado = respaldar_gold_master(str(origen), str(destino))

        ruta_respaldo = Path(resultado["ruta_respaldo"])
        ruta_firma = ruta_respaldo.with_suffix(".sha256.json")
        assert ruta_firma.exists()

    def test_respaldo_firma_contiene_campos_requeridos(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos")
        destino = tmp_path / "backups"

        resultado = respaldar_gold_master(str(origen), str(destino))
        ruta_firma = Path(resultado["ruta_respaldo"]).with_suffix(".sha256.json")
        firma = json.loads(ruta_firma.read_text(encoding="utf-8"))

        assert "sha256" in firma
        assert "tamano_bytes" in firma
        assert "fecha_respaldo" in firma
        assert "ruta_origen" in firma
        assert "integridad" in firma

    def test_respaldo_retorna_tamano(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        contenido = b"A" * 1024  # 1KB
        origen.write_bytes(contenido)

        resultado = respaldar_gold_master(str(origen), str(tmp_path))
        assert resultado["tamano_bytes"] == 1024

    def test_respaldo_crea_carpeta_destino_si_no_existe(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos")
        destino_nuevo = tmp_path / "nueva_carpeta" / "backups"
        assert not destino_nuevo.exists()

        resultado = respaldar_gold_master(str(origen), str(destino_nuevo))
        assert resultado["estado"] == "ok"
        assert destino_nuevo.exists()

    def test_respaldo_nombre_incluye_fecha(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos")

        resultado = respaldar_gold_master(str(origen), str(tmp_path))
        nombre = Path(resultado["ruta_respaldo"]).name
        assert nombre.startswith("GM_BACKUP_")

    def test_respaldo_retorna_fecha_iso(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos")

        resultado = respaldar_gold_master(str(origen), str(tmp_path))
        assert resultado["fecha_respaldo"] is not None
        # Debe ser parseable como ISO datetime
        from datetime import datetime
        datetime.fromisoformat(resultado["fecha_respaldo"])  # no lanza excepción

    def test_respaldo_estructura_completa_retorno(self, tmp_path):
        origen = tmp_path / "gm_test.xlsx"
        origen.write_bytes(b"datos")

        resultado = respaldar_gold_master(str(origen), str(tmp_path))
        assert "estado" in resultado
        assert "ruta_respaldo" in resultado
        assert "sha256" in resultado
        assert "tamano_bytes" in resultado
        assert "fecha_respaldo" in resultado
        assert "error" in resultado


# ══════════════════════════════════════════════════════════════════════════════
# Clase 5: obtener_estado_gm
# ══════════════════════════════════════════════════════════════════════════════

class TestObtenerEstadoGm:
    """Tests del diagnóstico completo del Gold Master."""

    def test_archivo_inexistente_retorna_no_disponible(self, tmp_path):
        ruta_falsa = tmp_path / "no_existe.xlsx"
        estado = obtener_estado_gm(str(ruta_falsa))
        assert estado["disponible"] is False
        assert estado["error"] is not None

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_disponible_con_archivo(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"A" * 1024)
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_opx.load_workbook.return_value = wb_mock
        mock_validar.return_value = []
        mock_changelog.return_value = {"versiones": [], "version_activa": "v6.0",
                                        "total_versiones": 1, "error": None}

        estado = obtener_estado_gm(str(ruta))
        assert estado["disponible"] is True
        assert estado["error"] is None

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_retorna_nombre_archivo(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        ruta = tmp_path / "TGI_GOLD_MASTER_v6.0_test.xlsx"
        ruta.write_bytes(b"datos")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_opx.load_workbook.return_value = wb_mock
        mock_validar.return_value = []
        mock_changelog.return_value = {"versiones": [], "version_activa": None,
                                        "total_versiones": 0, "error": None}

        estado = obtener_estado_gm(str(ruta))
        assert estado["nombre_archivo"] == "TGI_GOLD_MASTER_v6.0_test.xlsx"

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_retorna_total_hojas(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"datos")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_opx.load_workbook.return_value = wb_mock
        mock_validar.return_value = []
        mock_changelog.return_value = {"versiones": [], "version_activa": None,
                                        "total_versiones": 0, "error": None}

        estado = obtener_estado_gm(str(ruta))
        assert estado["total_hojas"] == len(HOJAS_REQUERIDAS_V6)

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_retorna_sha256(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"contenido fijo para sha256")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_opx.load_workbook.return_value = wb_mock
        mock_validar.return_value = []
        mock_changelog.return_value = {"versiones": [], "version_activa": None,
                                        "total_versiones": 0, "error": None}

        estado = obtener_estado_gm(str(ruta))
        assert estado["sha256"] is not None
        assert len(estado["sha256"]) == 64

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_cuenta_errores_validacion(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"datos")
        wb_mock = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_opx.load_workbook.return_value = wb_mock
        mock_validar.return_value = [
            ResultadoValidacion("estructura", "r1", "ERROR", "falla"),
            ResultadoValidacion("estructura", "r2", "ALERTA", "aviso"),
            ResultadoValidacion("estructura", "r3", "OK", "bien"),
        ]
        mock_changelog.return_value = {"versiones": [], "version_activa": None,
                                        "total_versiones": 0, "error": None}

        estado = obtener_estado_gm(str(ruta))
        assert estado["n_errores_val"] == 1
        assert estado["n_alertas_val"] == 1

    @patch("app.services.gold_master_governance.validar_gold_master")
    @patch("app.services.gold_master_governance.obtener_changelog_gm")
    @patch("app.services.gold_master_governance.openpyxl")
    def test_estado_estructura_completa(
        self, mock_opx, mock_changelog, mock_validar, tmp_path
    ):
        """Verifica que todos los campos del contrato de retorno estén presentes."""
        ruta = tmp_path / "gm.xlsx"
        ruta.write_bytes(b"datos")
        mock_opx.load_workbook.return_value = _crear_excel_mock(HOJAS_REQUERIDAS_V6)
        mock_validar.return_value = []
        mock_changelog.return_value = {"versiones": [], "version_activa": None,
                                        "total_versiones": 0, "error": None}

        estado = obtener_estado_gm(str(ruta))
        campos = [
            "disponible", "nombre_archivo", "version", "fecha_corte",
            "total_hojas", "metricas_clave", "sha256", "tamano_mb",
            "n_errores_val", "n_alertas_val", "changelog", "error"
        ]
        for campo in campos:
            assert campo in estado, f"Campo ausente: {campo}"


# ══════════════════════════════════════════════════════════════════════════════
# Clase 6: Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

class TestHelpers:
    """Tests para funciones internas del módulo."""

    def test_calcular_sha256_correcto(self, tmp_path):
        import hashlib
        archivo = tmp_path / "test.bin"
        contenido = b"quira intelligence gold master hash"
        archivo.write_bytes(contenido)
        esperado = hashlib.sha256(contenido).hexdigest()
        assert _calcular_sha256(archivo) == esperado

    def test_calcular_sha256_longitud(self, tmp_path):
        archivo = tmp_path / "test.bin"
        archivo.write_bytes(b"datos")
        resultado = _calcular_sha256(archivo)
        assert len(resultado) == 64

    def test_calcular_sha256_archivo_vacio(self, tmp_path):
        import hashlib
        archivo = tmp_path / "vacio.bin"
        archivo.write_bytes(b"")
        esperado = hashlib.sha256(b"").hexdigest()
        assert _calcular_sha256(archivo) == esperado

    def test_calcular_sha256_determinista(self, tmp_path):
        archivo = tmp_path / "test.bin"
        archivo.write_bytes(b"mismo contenido siempre")
        sha1 = _calcular_sha256(archivo)
        sha2 = _calcular_sha256(archivo)
        assert sha1 == sha2

    def test_resolver_ruta_con_argumento_explicito(self, tmp_path):
        ruta_esperada = tmp_path / "gm.xlsx"
        resultado = _resolver_ruta_gm(str(ruta_esperada))
        assert resultado == ruta_esperada

    def test_resolver_ruta_con_path_object(self, tmp_path):
        ruta_path = tmp_path / "gm.xlsx"
        resultado = _resolver_ruta_gm(ruta_path)
        assert resultado == ruta_path

    def test_resolver_ruta_ninguna_usa_fallback(self):
        """Sin argumento debe intentar resolver desde config o conector."""
        # No lanza excepción — puede retornar None si no hay config ni conector
        resultado = _resolver_ruta_gm(None)
        # resultado puede ser None o Path válido
        assert resultado is None or isinstance(resultado, Path)


# ══════════════════════════════════════════════════════════════════════════════
# Clase 7: Constantes del módulo
# ══════════════════════════════════════════════════════════════════════════════

class TestConstantesModulo:
    """Verifica la integridad de las constantes canónicas."""

    def test_hojas_requeridas_no_vacio(self):
        assert len(HOJAS_REQUERIDAS_V6) > 0

    def test_hojas_requeridas_contiene_g61_output_api(self):
        assert "G6.1_OUTPUT_API" in HOJAS_REQUERIDAS_V6

    def test_hojas_requeridas_contiene_todas_g3x(self):
        hojas_d1_d5 = [h for h in HOJAS_REQUERIDAS_V6 if h.startswith("G3.")]
        assert len(hojas_d1_d5) >= 5  # G3.1 a G3.7

    def test_claves_output_api_no_vacio(self):
        assert len(CLAVES_OUTPUT_API_REQUERIDAS) > 0

    def test_claves_output_api_contiene_tgi_d1_d5(self):
        for d in ["TGI_D1", "TGI_D2", "TGI_D3", "TGI_D4", "TGI_D5"]:
            assert d in CLAVES_OUTPUT_API_REQUERIDAS

    def test_claves_output_api_contiene_sat_requeridos(self):
        assert "SAT_CLASIF_RIESGO" in CLAVES_OUTPUT_API_REQUERIDAS
        assert "SAT_ACTIVAS_COUNT" in CLAVES_OUTPUT_API_REQUERIDAS

    def test_claves_output_api_contiene_icpi_tgi(self):
        assert "ICPI_GLOBAL" in CLAVES_OUTPUT_API_REQUERIDAS
        assert "TGI_SCORE" in CLAVES_OUTPUT_API_REQUERIDAS
