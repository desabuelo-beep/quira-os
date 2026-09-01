# -*- coding: utf-8 -*-
"""
tests/test_recorrido_icpi.py — la cifra madre, recorrida hacia atrás
════════════════════════════════════════════════════════════════════════════════
Javo eligió la cifra: **el ICPI**. El colega fijó el método: no recalcular, no
corregir, no usar el propio artefacto como autoridad — sólo demostrar hasta
dónde puede reconstruirse.

EL RECORRIDO, medido:

    H12!B33  = B31/B32
      B31    = SUM(J6:J30)      Jᵢ = Pᵢ×Rᵢ×Vᵢ×Eᵢ×Tᵢ×Cᵢ
      B32    = SUM(K6:K30)      Kᵢ = Pᵢ×Rᵢ
        Pᵢ  ← H14_PONDERADORES!G      Rᵢ ← H14_PONDERADORES!F
        Vᵢ  ← VLOOKUP H13_VARIABLES_Vi
        Eᵢ  ← **literal, 25 de 25**
        Tᵢ  ← H07b!B20 ← H07_S5_FINANCIERO_eSIGEF!B23
              └─ Fuente declarada: «Cédula LOTAIP GAD Montecristi Abr-2026»
        Cᵢ  ← VLOOKUP H01_PARÁMETROS

EL HALLAZGO. `H04!B7` se llama **`Total_Metas_PDOT`** y vale **25**. Javo:

> *«para ICPI tomamos metas PDOT el total. Cuando empezamos la construcción
> empezamos con una **muestra de 25**, pero luego decidimos hacerlo completo,
> pero **nunca acoplamos el resto de metas**.»*

El parámetro etiquetado «total» es el tamaño de la muestra. Y BOOT ya tiene la
regla que lo nombra: **«etiqueta incorrecta = número falso»** (§6-sexies).

⚠️ EL MOTOR NO CALCULA MAL. Hace exactamente lo que dice hacer, y los
ponderadores suman 1.0000 sobre esas 25. Lo que no corresponde es el **alcance
declarado**: una cifra llamada `ICPI_GLOBAL_SISTEMA` calculada sobre un
subconjunto que se declara total. Es un problema de frontera, no de aritmética —
y esa distinción es la que esta sesión existe para no perder.

⛔ NO SE REPARA. El Gold Master es inmutable en su fórmula canónica y esto es una
decisión de gobernanza (Regla de Oro 1).

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


def _gm():
    try:
        import openpyxl
        from config import DATOS_DIR
        p = Path(DATOS_DIR) / "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"
        if not p.exists():
            return None
        return openpyxl.load_workbook(p, data_only=False, read_only=True)
    except Exception:                                    # noqa: BLE001
        return None


@pytest.mark.efecto_real
def test_la_formula_del_ICPI_es_la_declarada():
    """El punto de partida, literal y sin evaluar. `H12!B33` es la fuente única
    del ICPI y su fórmula es inmutable (Regla de Oro 1)."""
    wb = _gm()
    if wb is None:
        pytest.skip("Gold Master no accesible")
    ws = wb["H12_MOTOR_ICPI_CANÓNICO"]
    assert ws["B33"].value == "=B31/B32"
    assert ws["B31"].value == "=SUM(J6:J30)"
    assert ws["B32"].value == "=SUM(K6:K30)"
    wb.close()


@pytest.mark.efecto_real
def test_el_parametro_llamado_total_es_el_tamano_de_la_muestra():
    """EL HALLAZGO DEL RECORRIDO, fijado con trinquete.

    `Total_Metas_PDOT = 25` — y las 25 fueron una muestra inicial que nunca se
    amplió. El día que se acoplen las demás, este número subirá y la prueba
    fallará: **y ese fallo será el progreso**, no una regresión."""
    wb = _gm()
    if wb is None:
        pytest.skip("Gold Master no accesible")
    ws = wb["H04_S2_PLANIFICACIÓN_PDOT"]
    etiqueta = ws.cell(row=7, column=1).value
    assert etiqueta == "Total_Metas_PDOT", f"cambió la etiqueta: {etiqueta}"
    wb.close()

    wb2 = _gm()
    import openpyxl
    from config import DATOS_DIR
    v = openpyxl.load_workbook(Path(DATOS_DIR) / "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx",
                               data_only=True, read_only=True)
    total = v["H04_S2_PLANIFICACIÓN_PDOT"].cell(row=7, column=2).value
    v.close(); wb2.close()
    assert total == 25, (
        f"Total_Metas_PDOT pasó de 25 a {total}: si se acoplaron las metas que "
        f"faltaban, actualizar este hallazgo — dejó de ser una muestra")


@pytest.mark.efecto_real
def test_Ei_es_un_literal_sin_definicion_en_el_canon():
    """El segundo hallazgo, independiente del primero. `Eᵢ` participa en el
    numerador del ICPI y es un **valor escrito a mano en las 25 filas**: no tiene
    fórmula, no referencia ninguna hoja, y su única aparición en todo el libro es
    la cabecera de su propia columna.

    Mientras `H01_PARÁMETROS` declara: *«FUENTE ÚNICA de toda configuración.
    NINGUNA otra hoja tiene valores de configuración hardcodeados»*."""
    wb = _gm()
    if wb is None:
        pytest.skip("Gold Master no accesible")
    ws = wb["H12_MOTOR_ICPI_CANÓNICO"]
    literales = [r for r in range(6, 31)
                 if ws.cell(row=r, column=5).value is not None
                 and not str(ws.cell(row=r, column=5).value).startswith("=")]
    assert len(literales) == 25, (
        f"Eᵢ dejó de ser literal en las 25 filas ({len(literales)}): si ahora "
        f"deriva de alguna hoja, el hallazgo cambió")
    wb.close()


@pytest.mark.efecto_real
def test_el_eslabon_Ti_llega_a_un_documento_primario_declarado():
    """LO QUE SÍ SE RECONSTRUYE. De los seis insumos, `Tᵢ` es el único que
    retrocede hasta un documento nombrado: `H07_S5_FINANCIERO_eSIGEF` declara en
    su fila 11 la **Cédula LOTAIP GAD Montecristi Abr-2026**.

    No es trazabilidad completa —el documento se nombra en prosa, sin SHA ni
    ruta—, pero es más de lo que declaran los otros cinco insumos, que sólo
    apuntan a otras hojas del mismo libro."""
    wb = _gm()
    if wb is None:
        pytest.skip("Gold Master no accesible")
    ws = wb["H07_S5_FINANCIERO_eSIGEF"]
    assert ws.cell(row=11, column=1).value == "Fuente"
    doc = str(ws.cell(row=11, column=2).value)
    assert "Cédula" in doc and "2026" in doc, f"cambió la fuente declarada: {doc}"
    wb.close()
