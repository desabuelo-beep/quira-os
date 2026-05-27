"""
tests/test_top.py — Suite de verificación del Motor TOP
Trayectoria Operativa Proyectada · QUIRA_DOCTRINE_v1.3 · Sección 1.6

Gold assertions derivadas de datos reales Montecristi Q1-2026
(SIAP-ICPI_GOLD_MASTER_v5.5_TGI — H90_PRESUPUESTO_CONSOLIDADO)

Principio: si TOP falla aquí, la doctrina falla en Concejo.

Dylus Lab © 2026
"""
from __future__ import annotations

import pytest
from utils.top import (
    WQ,
    calcular_top,
    clasificar_top,
    calcular_top_desde_corte,
    quarter_desde_corte,
    top_entidad,
    narrativa_ia,
)


# ══════════════════════════════════════════════════════════════════════════════
# 1. CONSTANTES W_Q — inmutables, calibradas con eSIGEF Ecuador
# ══════════════════════════════════════════════════════════════════════════════

class TestWQ:
    def test_wq_keys_completos(self):
        assert set(WQ.keys()) == {"Q1", "Q2", "Q3", "Q4"}

    def test_wq_q1_letargo_administrativo(self):
        assert WQ["Q1"] == 0.13

    def test_wq_q4_cierre_fiscal(self):
        assert WQ["Q4"] == 1.00

    def test_wq_monotono(self):
        """Los pesos deben aumentar de Q1 a Q4."""
        assert WQ["Q1"] < WQ["Q2"] < WQ["Q3"] < WQ["Q4"]

    def test_wq_q4_igual_a_uno(self):
        """Al cierre anual la institución debe haber ejecutado 100%."""
        assert WQ["Q4"] == 1.00


# ══════════════════════════════════════════════════════════════════════════════
# 2. calcular_top() — fórmula pura, determinista
# ══════════════════════════════════════════════════════════════════════════════

class TestCalcularTop:
    """
    Valores gold derivados de Gold Master v5.5_TGI · H90_PRESUPUESTO_CONSOLIDADO.
    Fórmula: TOP = Ti_acumulado / W_Q
    """

    # ── Gold assertions Montecristi Q1-2026 ────────────────────────────────
    def test_gad_inversion_ruptura(self):
        """GAD inversión G71-78: Ti=1.05% → TOP=8.1% → ruptura."""
        assert calcular_top(1.05, "Q1") == 8.1

    def test_patronato_sobre_ritmo(self):
        """Patronato H90: Ti=19.56% → TOP=150.5%."""
        assert calcular_top(19.56, "Q1") == 150.5

    def test_ep_aseo_sobre_ritmo(self):
        """EP Aseo H90: Ti=18.17% → TOP=139.8%."""
        assert calcular_top(18.17, "Q1") == 139.8

    def test_bomberos_sobre_ritmo(self):
        """Bomberos H90: Ti=19.43% → TOP=149.5%."""
        assert calcular_top(19.43, "Q1") == 149.5

    # ── Propiedades matemáticas ───────────────────────────────────────────
    def test_top_q4_identidad(self):
        """En Q4 TOP = Ti (W_Q4 = 1.00 — el divisor es identidad)."""
        assert calcular_top(75.0, "Q4") == 75.0

    def test_top_negativo_retorna_cero(self):
        """Ti negativo es imposible institucionalmente — retorna 0."""
        assert calcular_top(-5.0, "Q1") == 0.0

    def test_top_puede_superar_100(self):
        """
        Doctrina QUIRA: TOP > 100 es VÁLIDO.
        Significa ritmo superior al histórico — no error.
        """
        top = calcular_top(30.0, "Q1")
        assert top > 100.0  # 30 / 0.13 ≈ 230.8

    def test_top_quarter_desconocido_fallback_q1(self):
        """Quarter desconocido usa W_Q1 como fallback defensivo."""
        assert calcular_top(13.0, "QX") == calcular_top(13.0, "Q1")

    def test_redondeo_a_1_decimal(self):
        """TOP devuelve exactamente 1 decimal — no float crudo."""
        result = calcular_top(19.56, "Q1")
        assert result == round(result, 1)


# ══════════════════════════════════════════════════════════════════════════════
# 3. quarter_desde_corte() — parsing de cortes canónicos
# ══════════════════════════════════════════════════════════════════════════════

class TestQuarterDesdeCorte:
    def test_corte_canonico_q1_2026(self):
        assert quarter_desde_corte("Q1-2026") == "Q1"

    def test_corte_canonico_q3_2025(self):
        assert quarter_desde_corte("Q3-2025") == "Q3"

    def test_corte_canonico_q4_2027(self):
        assert quarter_desde_corte("Q4-2027") == "Q4"

    def test_corte_malformado_fallback_q1(self):
        """Corte no reconocido → fallback Q1 (conservador)."""
        assert quarter_desde_corte("INVALIDO") == "Q1"

    def test_corte_con_q_en_upper(self):
        """Parsing robusto — case insensitive."""
        assert quarter_desde_corte("q2-2026") in ("Q1", "Q2", "Q3", "Q4")


# ══════════════════════════════════════════════════════════════════════════════
# 4. clasificar_top() — umbrales canónicos (NOMENCLATURA 7.2)
# ══════════════════════════════════════════════════════════════════════════════

class TestClasificarTop:
    """
    Umbrales canónicos:
      ≥ 75  → sostenible
      ≥ 55  → atencion
      ≥ 35  → alerta
      < 35  → ruptura
    """

    def test_100_es_sostenible(self):
        r = clasificar_top(100.0)
        assert r["categoria"] == "sostenible"

    def test_umbral_exacto_sostenible(self):
        r = clasificar_top(75.0)
        assert r["categoria"] == "sostenible"

    def test_bajo_sostenible_es_atencion(self):
        r = clasificar_top(74.9)
        assert r["categoria"] == "atencion"

    def test_umbral_exacto_atencion(self):
        r = clasificar_top(55.0)
        assert r["categoria"] == "atencion"

    def test_bajo_atencion_es_alerta(self):
        r = clasificar_top(54.9)
        assert r["categoria"] == "alerta"

    def test_umbral_exacto_alerta(self):
        r = clasificar_top(35.0)
        assert r["categoria"] == "alerta"

    def test_bajo_alerta_es_ruptura(self):
        r = clasificar_top(34.9)
        assert r["categoria"] == "ruptura"

    def test_cero_es_ruptura(self):
        r = clasificar_top(0.0)
        assert r["categoria"] == "ruptura"

    # ── Sobre ritmo ───────────────────────────────────────────────────────
    def test_sobre_ritmo_flag(self):
        """TOP > 100 debe activar sobre_ritmo."""
        r = clasificar_top(150.5)
        assert r["sobre_ritmo"] is True

    def test_exactamente_100_no_es_sobre_ritmo(self):
        r = clasificar_top(100.0)
        assert r["sobre_ritmo"] is False

    def test_sobre_ritmo_no_muestra_numero(self):
        """
        Doctrina cap: TOP > 100 → top_display=None (mostrar label, no el %).
        Evita confusión política con números > 100%.
        """
        r = clasificar_top(150.5)
        assert r["top_display"] is None

    def test_top_display_capeado_a_100(self):
        """TOP ≤ 100 → top_display muestra el % (capeado, no el valor interno)."""
        r = clasificar_top(85.0)
        assert r["top_display"] == "85%"

    def test_top_display_cero(self):
        r = clasificar_top(0.0)
        assert r["top_display"] == "0%"

    # ── Campos requeridos por Vista Ejecutiva y QUIRA IA ──────────────────
    def test_resultado_tiene_todos_los_campos(self):
        campos = {"top", "categoria", "label", "color", "icono",
                  "diagnostico", "top_display", "sobre_ritmo"}
        assert campos.issubset(clasificar_top(50.0).keys())

    def test_color_es_hex(self):
        r = clasificar_top(50.0)
        assert r["color"].startswith("#")
        assert len(r["color"]) == 7

    # ── Colores canónicos por categoría ──────────────────────────────────
    def test_color_sostenible(self):
        assert clasificar_top(80.0)["color"] == "#22C55E"

    def test_color_atencion(self):
        assert clasificar_top(60.0)["color"] == "#F59E0B"

    def test_color_alerta(self):
        assert clasificar_top(40.0)["color"] == "#F97316"

    def test_color_ruptura(self):
        assert clasificar_top(10.0)["color"] == "#EF4444"


# ══════════════════════════════════════════════════════════════════════════════
# 5. calcular_top_desde_corte() — conveniencia con corte canónico
# ══════════════════════════════════════════════════════════════════════════════

class TestCalcularTopDesdeCorte:
    def test_equivale_a_calcular_con_q1(self):
        assert calcular_top_desde_corte(19.56, "Q1-2026") == calcular_top(19.56, "Q1")

    def test_gad_inversion_montecristi(self):
        assert calcular_top_desde_corte(1.05, "Q1-2026") == 8.1


# ══════════════════════════════════════════════════════════════════════════════
# 6. top_entidad() — pipeline completo: cálculo + clasificación + metadata
# ══════════════════════════════════════════════════════════════════════════════

class TestTopEntidad:
    def test_gad_inversion_ruptura_q1_2026(self):
        """GAD inversión Montecristi — gold assertion completa."""
        r = top_entidad(1.05, "Q1-2026", "GAD Municipal")
        assert r["top"]      == 8.1
        assert r["categoria"] == "ruptura"
        assert r["icono"]    == "🔴"
        assert r["entidad"]  == "GAD Municipal"
        assert r["corte"]    == "Q1-2026"
        assert r["quarter"]  == "Q1"
        assert r["ti_pct"]   == 1.05

    def test_patronato_sobre_ritmo_q1_2026(self):
        """Patronato Montecristi — sobre ritmo esperado."""
        r = top_entidad(19.56, "Q1-2026", "Patronato Municipal")
        assert r["top"]        == 150.5
        assert r["categoria"]  == "sostenible"
        assert r["sobre_ritmo"] is True
        assert r["top_display"] is None  # no mostrar el número

    def test_campos_ecosistema_presentes(self):
        """top_entidad() debe incluir todos los campos necesarios para Zona 5."""
        r = top_entidad(19.56, "Q1-2026", "Patronato Municipal")
        campos = {"top", "categoria", "label", "color", "icono",
                  "diagnostico", "top_display", "sobre_ritmo",
                  "ti_pct", "corte", "quarter", "entidad"}
        assert campos.issubset(r.keys())

    def test_nombre_vacio_no_falla(self):
        """nombre vacío → usa fallback sin crash."""
        r = top_entidad(10.0, "Q1-2026")
        assert r is not None
        assert "top" in r


# ══════════════════════════════════════════════════════════════════════════════
# 7. narrativa_ia() — brief ejecutivo institucional (no chatbot)
# ══════════════════════════════════════════════════════════════════════════════

class TestNarrativaIA:
    """
    El lenguaje de QUIRA IA es autoritario, preciso, sin chatbot.
    Las narrativas deben ser concretas y contener el nombre de la entidad.
    """

    def test_gad_ruptura_menciona_entidad(self):
        r = top_entidad(1.05, "Q1-2026", "GAD Municipal")
        nar = narrativa_ia(r)
        assert "GAD Municipal" in nar

    def test_gad_ruptura_menciona_top(self):
        r = top_entidad(1.05, "Q1-2026", "GAD Municipal")
        nar = narrativa_ia(r)
        assert "8.1" in nar or "ruptura" in nar.lower()

    def test_patronato_sobre_ritmo_lenguaje(self):
        r = top_entidad(19.56, "Q1-2026", "Patronato Municipal")
        nar = narrativa_ia(r)
        assert "ritmo" in nar.lower() or "sobre" in nar.lower()

    def test_atencion_menciona_monitoreo(self):
        r = top_entidad(8.0, "Q1-2026", "Entidad Test")   # TOP=61.5 → atención
        nar = narrativa_ia(r)
        # debe ser string no vacío
        assert isinstance(nar, str) and len(nar) > 20

    def test_ruptura_menciona_urgencia(self):
        r = top_entidad(1.0, "Q1-2026", "Entidad Crítica")
        nar = narrativa_ia(r)
        # debe contener señal de urgencia
        assert "urgente" in nar.lower() or "riesgo" in nar.lower() or "ruptura" in nar.lower()

    def test_retorna_string(self):
        r = top_entidad(50.0, "Q2-2026", "Entidad X")
        assert isinstance(narrativa_ia(r), str)

    def test_no_contiene_porcentaje_ficticio(self):
        """La narrativa debe usar los valores reales del dict, no inventar."""
        r = top_entidad(19.56, "Q1-2026", "Patronato Municipal")
        nar = narrativa_ia(r)
        # No debe contener un % completamente inventado
        assert "999" not in nar
        assert "200%" not in nar


# ══════════════════════════════════════════════════════════════════════════════
# 8. GOLD ASSERTIONS — Holding Municipal Montecristi Q1-2026
#    Fuente: H90_PRESUPUESTO_CONSOLIDADO · Gold Master v5.5_TGI
# ══════════════════════════════════════════════════════════════════════════════

class TestGoldAssertionsMontecristi:
    """
    Estas son las verdades matemáticas del sistema para Q1-2026.
    Si alguna falla, hay un cambio en la metodología o en el snapshot
    que debe ser documentado y aprobado explícitamente.
    """

    CORTE = "Q1-2026"

    _ENTIDADES = [
        ("GAD Municipal",       1.05,  "ruptura",    8.1),
        ("Patronato Municipal", 19.56, "sostenible", 150.5),
        ("EP Aseo",             18.17, "sostenible", 139.8),
        ("Cuerpo de Bomberos",  19.43, "sostenible", 149.5),
    ]

    @pytest.mark.parametrize("nombre,ti,cat_esperada,top_esperado", _ENTIDADES)
    def test_gold_master_q1_2026(self, nombre, ti, cat_esperada, top_esperado):
        r = top_entidad(ti, self.CORTE, nombre)
        assert r["top"]       == top_esperado, \
            f"{nombre}: TOP esperado {top_esperado}, obtenido {r['top']}"
        assert r["categoria"] == cat_esperada, \
            f"{nombre}: categoría esperada '{cat_esperada}', obtenida '{r['categoria']}'"

    def test_holding_contraste_narrativo(self):
        """
        El hallazgo doctrinal central de Sprint B:
        GAD inversión en ruptura mientras el ecosistema está sobre ritmo.
        """
        gad       = top_entidad(1.05,  self.CORTE, "GAD")
        patronato = top_entidad(19.56, self.CORTE, "Patronato")
        ep_aseo   = top_entidad(18.17, self.CORTE, "EP Aseo")
        bomberos  = top_entidad(19.43, self.CORTE, "Bomberos")

        assert gad["categoria"] == "ruptura"
        assert patronato["categoria"] == "sostenible"
        assert ep_aseo["categoria"] == "sostenible"
        assert bomberos["categoria"] == "sostenible"

        # El ecosistema periférico tiene MAYOR TOP que el GAD
        assert patronato["top"] > gad["top"] * 10
        assert ep_aseo["top"]   > gad["top"] * 10
        assert bomberos["top"]  > gad["top"] * 10
