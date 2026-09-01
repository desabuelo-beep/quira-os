# -*- coding: utf-8 -*-
"""
tests/test_datos_procedencia.py — CAPA 3 · procedencia de los ARTEFACTOS
════════════════════════════════════════════════════════════════════════════════
`procedencia.py` modela la procedencia de una **afirmación**. C3 pregunta por la
de los **artefactos**: los 2.213 archivos de `data/`. Son cosas distintas y
sólo la primera estaba cubierta.

EL HALLAZGO, y no es una acusación:

    1360000430001    31 artefactos · 2026-05-25 → 2026-06-16
    1360001010001   158 artefactos · 2026-08-18 → 2026-09-01
                    NO se solapan — sucesión limpia

La identidad del sujeto **tiene versiones**. Los artefactos anteriores al cambio
llevan el RUC previo y son correctos para su época; lo que falta es que declaren
bajo qué versión se produjeron.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import datos as D                         # noqa: E402


def test_las_identidades_del_sujeto_se_suceden_y_no_conviven():
    """LA PROPIEDAD GRAVE, con trinquete.

    Que un artefacto lleve una identidad anterior es normal: la del perfil
    cambió y su propia nota lo registra («no estaba huellado», cerrado el
    2026-08-26). Lo que sería grave es que **dos identidades estuvieran activas
    a la vez** sobre el mismo sujeto — eso ya no sería historia, sería
    ambigüedad viva."""
    c = D.cobertura_de_datos()
    assert not c["identidades_que_conviven"], (
        f"dos identidades del sujeto activas a la vez: "
        f"{c['identidades_que_conviven']}")
    assert len(c["identidades_del_sujeto"]) >= 2, (
        "dejó de verse la sucesión de identidades: el hallazgo se perdió")


def test_el_ruc_vigente_es_el_ultimo_de_la_sucesion():
    """La identidad más reciente en los artefactos debe ser la que el perfil
    declara. Si divergieran, el sistema estaría produciendo evidencia bajo una
    identidad que su propio canon no reconoce."""
    from app.agents import sujeto as S
    import json

    perfil = json.loads((S._SUJETOS / f"{S.POR_DEFECTO}.json").read_text(encoding="utf-8"))
    canonico = str(perfil["identidad_en_fuentes"]["ruc"])
    ultima = D.identidades_del_sujeto()[-1]["identidad"]
    assert ultima == canonico, (
        f"los artefactos más recientes usan {ultima} y el perfil declara "
        f"{canonico}")


# ── ATAQUES AL DETECTOR ───────────────────────────────────────────────────────
def test_ataque_un_ensayo_no_es_un_artefacto_sin_procedencia():
    """REGRESIÓN del octavo falso positivo, evitado por poco.

    185 archivos viven en un directorio llamado **`provenance/ensayos`** y no
    llevaban ninguna de las marcas que el detector buscaba. Parecía «artefactos
    de procedencia sin procedencia». Declaran `dry_run: true`: **son ensayos que
    declaran serlo**, material de ingeniería, no evidencia de observación."""
    c = D.cobertura_de_datos()
    assert c["por_estado"].get(D.ENSAYO, 0) >= 180, (
        "los ensayos dejaron de reconocerse y volverán a contarse como huérfanos")
    ensayos = [a for a in D.artefactos_json() if a["estado"] == D.ENSAYO]
    assert all("ensayo" in a["artefacto"] or "provenance" in a["artefacto"]
               for a in ensayos[:20])


def test_ataque_el_detector_busca_por_patron_y_a_profundidad():
    """El primer detector usaba una LISTA de marcas y sólo el primer nivel: dio
    **221 falsos positivos**. `ack_registry.json` lleva `meta` sin guion bajo y
    `cadena_estado.json` guarda sus sellos dentro de las etapas. Con patrón y
    profundidad quedan 13 — y aun así se llaman «sin marca hallada», no «sin
    procedencia»: el detector no es autoridad sobre lo que no ve."""
    c = D.cobertura_de_datos()
    assert c["por_estado"].get(D.SIN_MARCA, 999) < 40, (
        f"volvieron los falsos positivos: {c['por_estado'].get(D.SIN_MARCA)}")
    fuente = (RAIZ / "app" / "agents" / "datos.py").read_text(encoding="utf-8")
    assert "prof + 1" in fuente, "el detector dejó de mirar en profundidad"
    assert D.SIN_MARCA == "sin_marca_hallada", (
        "el estado se renombró a algo que afirma más de lo medido")


def test_el_universo_declara_que_no_mide_la_mayor_parte_del_volumen():
    """`data/` tiene 943 CSV, 774 binarios, 16 PDF y 13 hojas de cálculo. Este
    detector sólo lee JSON. Decir «85 con procedencia» sin decir eso invitaría a
    leer como medido lo que ni siquiera se miró."""
    limites = " ".join(D.cobertura_de_datos()["universo"]["fuera_de_alcance"]).lower()
    assert "csv" in limites and "no está medida" in limites
    assert "mayor parte del volumen" in D.cobertura_de_datos()["afirmacion_sostenible"]
