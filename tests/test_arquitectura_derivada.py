# -*- coding: utf-8 -*-
"""
tests/test_arquitectura_derivada.py — CAPA 2 · lo declarado, lo derivable, lo que no
════════════════════════════════════════════════════════════════════════════════
El colega fijó el encargo con precisión: *«Continúa Capa 2. No repares todavía.
No decidas todavía. Mapea las relaciones»*, y prohibió expresamente el atajo:

> *«Una equivalencia no es una propiedad porque históricamente la conozcamos; es
> una propiedad cuando QUIRA puede señalar el artefacto que la establece.»*

Estas pruebas fijan las dos cosas que la Capa 2 aprendió el primer día:

 1 · el universo eran **53 ADR, no 41** — doce viven en `docs/corpus_externo/`,
     entre ellos `ADR-007_Gold_Master_unica_fuente_calculo`;
 2 · las cinco «citas rotas» que el módulo reportó eran **todas falsas**, y se
     cayeron al verificarlas antes de reportarlas.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import arquitectura as A                  # noqa: E402


# ── CRITERIOS ─────────────────────────────────────────────────────────────────
def test_el_universo_son_los_dos_directorios():
    """REGRESIÓN del falso positivo que abrió la Capa 2.

    Mirando sólo `docs/adr/` el inventario veía 41 ADR y reportaba cinco citas
    rotas. Los otros doce —`ADR-001..012`, incluido el del Gold Master— viven en
    `docs/corpus_externo/`. Universo incompleto en un 23%."""
    c = A.cobertura_arquitectonica()
    assert c["universo"]["hallados"] >= 53, (
        f"el universo volvió a recortarse: {c['universo']['hallados']} ADR")
    ids = {a["id"] for a in c["adr"]}
    assert {"ADR-005", "ADR-007", "ADR-011", "ADR-012"} <= ids, (
        "se perdieron los ADR fundacionales de corpus_externo/")


def test_ninguna_referencia_apunta_a_un_ADR_inexistente():
    """Las cuatro «rotas» se resuelven con el universo completo. La única que
    queda es `ADR-053 → ADR-054`, y su contexto dice *«obligaría a abrir un
    ADR-054»*: una mención hipotética, no una cita."""
    sueltas = A.referencias_no_resueltas()
    assert len(sueltas) <= 1, f"aparecieron referencias nuevas sin resolver: {sueltas}"
    for r in sueltas:
        assert r["contexto"], "una referencia sin resolver debe traer su contexto"
        assert "abrir un" in r["contexto"] or "futuro" in r["contexto"].lower(), (
            f"referencia sin resolver que NO es hipotética — hay que leerla: {r}")


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_el_modulo_no_puede_declarar_vigencia():
    """LA PROHIBICIÓN CENTRAL DE LA CAPA 2.

    Cuatro nombres de estado de tres épocas —ACEPTADO · ACTIVO · RATIFICADO ·
    APROBADO— y ningún artefacto declara que sean equivalentes. Mapear
    `RATIFICADO → vigente` sería fabricar la gobernanza que decimos auditar; es
    el mismo movimiento que produjo el «advisory» de d09."""
    c = A.cobertura_arquitectonica()
    assert "vigente" not in c, "el inventario empezó a computar vigencia"
    for fila in c["adr"]:
        assert "vigente" not in fila, f"{fila['id']} declara vigencia derivada"
        assert isinstance(fila["estado_declarado"], str), (
            "el estado debe conservarse literal, no normalizarse a una taxonomía")


def test_ataque_no_hay_imputacion_retroactiva():
    """Los ADR anteriores a ADR-035 no registran validador **porque la norma que
    lo exige no existía todavía**. Contarlos como defecto sería una imputación
    retroactiva: exactamente lo que este observatorio le prohíbe hacerle al
    sujeto observado."""
    c = A.cobertura_arquitectonica()
    anteriores = [a for a in c["adr"]
                  if a["anterior_a_la_autoridad"]
                  and a["validacion_humana"] == A.NO_DETERMINABLE]
    assert anteriores, "dejaron de distinguirse los anteriores a la autoridad"
    posteriores = c["sin_constancia_y_posteriores_a_la_autoridad"]
    for a in anteriores:
        assert a["id"] not in posteriores, (
            f"{a['id']} es anterior a la autoridad y se está señalando igual "
            f"que los posteriores")


def test_ataque_una_calificacion_de_evidencia_no_es_un_ADR_sin_validar():
    """`ADR-019` es `STRONGLY_SUPPORTED` **a propósito** — Regla de Oro 10: «no
    congelar teoría antes que el grafo hable». Contarlo entre los no validados
    sería acusar al canon de cumplir su propia regla."""
    for i in ("ADR-019", "ADR-022"):
        fila = next(a for a in A.todos() if a["id"] == i)
        assert fila["validacion_humana"] == A.NO_ES_DECISION, (
            f"{i} se está tratando como decisión de gobernanza")


def test_ataque_lo_pendiente_no_se_confunde_con_lo_no_constatado():
    """Tres estados distintos, no dos: `no` (el ADR dice que está pendiente),
    `no_determinable` (nadie registró nada) y `si`. Colapsar los dos primeros
    convertiría un trámite abierto y declarado en un vacío documental."""
    c = A.cobertura_arquitectonica()
    pendientes = c["por_validacion_humana"].get(A.NO, [])
    assert pendientes, "dejaron de verse los ADR que se declaran pendientes"
    for i in pendientes:
        fila = next(a for a in c["adr"] if a["id"] == i)
        assert "pendiente" in fila["estado_declarado"].lower()
        assert i not in c["sin_constancia_de_validacion"], (
            f"{i} declara estar pendiente: eso NO es falta de constancia")


def test_ADR_039_es_el_unico_posterior_a_la_autoridad_sin_constancia():
    """El hallazgo fino de la Capa 2, con trinquete. ADR-039 es del 17-jul —
    posterior a ADR-035— y su estado dice «ACEPTADO CONCEPTUALMENTE · (síntesis
    del colega…)»: nombra al colega, no a Javo. Puede ser un estado intermedio
    legítimo o un ADR a medio sellar; el inventario lo señala y **no lo decide**."""
    c = A.cobertura_arquitectonica()
    assert c["sin_constancia_y_posteriores_a_la_autoridad"] == ["ADR-039"], (
        f"cambió el conjunto: {c['sin_constancia_y_posteriores_a_la_autoridad']}")


def test_la_afirmacion_dice_lo_que_NO_puede_afirmar():
    """La frase debe declarar su propio límite. Un inventario que sólo cuenta lo
    que halló invita a leer como conforme lo que apenas es no medido."""
    f = A.cobertura_arquitectonica()["afirmacion_sostenible"]
    assert "No se afirma cuáles gobiernan hoy" in f
    assert "no consta ≠ no se validó" in f


# ── PROPIEDAD 6-7 · ROL OBSERVABLE Y TIPOS DE RELACIÓN (2026-08-31) ──────────
def test_el_descubrimiento_es_por_rol_no_por_territorio():
    """El colega, tras el hallazgo de los doce: *«¿cómo descubre QUIRA un ADR,
    independientemente de dónde esté almacenado?»*.

    El universo se barre del repositorio entero menos exclusiones declaradas, no
    de una lista de carpetas. Si mañana aparece un ADR en un tercer territorio,
    se ve solo — que es justo lo que no ocurrió con `corpus_externo/`."""
    t = A.territorios()
    assert len(t["territorios"]) >= 2, (
        "la arquitectura documental tiene más de un territorio físico y eso es "
        "una propiedad, no un accidente")
    assert sum(t["territorios"].values()) >= 53
    for e in t["excluidos"]:
        assert e["motivo"], f"exclusión sin motivo declarado: {e['archivo']}"


def test_ataque_el_inventario_no_se_cuenta_a_si_mismo():
    """`arquitectura.py` nombra decenas de ADR en sus comentarios. Si entrara en
    su propio corpus referente, inflaría la centralidad de lo que está midiendo
    — el mismo defecto que `arbol_limpio` tuvo en el registrador."""
    rutas = {r for r, _ in A._corpus_referente()}
    assert "app/agents/arquitectura.py" not in rutas
    r7 = A.rol_observable("ADR-007")
    for lista in r7["relaciones"].values():
        assert not any("arquitectura.py" in x for x in lista)


def test_ataque_el_corpus_referente_incluye_donde_viven_las_reglas():
    """REGRESIÓN de un universo incompleto detectado por su propio resultado.

    El corpus barría docs/, app/, scripts/, governance/ e identity/ — y dejaba
    fuera `CLAUDE.md`, donde viven las Reglas de Oro. Se notó porque «ningún
    script lo recalcula» dio 0 artefactos siendo de lo más citado del sistema."""
    rutas = {r for r, _ in A._corpus_referente()}
    assert "CLAUDE.md" in rutas, "volvió a quedar fuera el archivo de las reglas"


def test_ataque_centralidad_no_es_vigencia():
    """`ADR-035` es el más referido de todos. Eso NO lo declara vigente, y el
    módulo no puede insinuarlo: un ADR muy citado puede estar derogado y uno
    fundacional puede no citarse nunca — que es exactamente el caso de ADR-007."""
    top = A.centralidad()[0]
    assert top["id"] == "ADR-035", f"cambió el más central: {top['id']}"
    assert "vigente" not in top and "gobierna" not in top
    fuente = (RAIZ / "app" / "agents" / "arquitectura.py").read_text(encoding="utf-8")
    assert "Centralidad no es vigencia" in fuente


def test_el_principio_de_ADR_007_gobierna_aunque_su_ADR_no_se_cite():
    """EL HALLAZGO QUE LA PREGUNTA ORIGINAL NO PODÍA DAR.

    Se preguntó «¿ADR-007 gobierna?» — que le pide a la memoria humana lo que
    debe derivarse. Medido: su identificador aparece en 2 artefactos, ambos
    dentro de su propio territorio; y su principio —«Regla de Oro 1»— aparece en
    decenas. **El principio gobierna; el artefacto que lo fundó no se cita.**
    La regla viaja desacoplada de su decisión de origen."""
    import re

    r = A.rol_observable("ADR-007")
    assert r["lo_invocan_como_autoridad"] == 0, (
        "si alguien empezara a invocar ADR-007 como autoridad, hay que decirlo")
    con_regla = sum(1 for _, txt in A._corpus_referente()
                    if re.search(r"Regla 1/4|Regla de Oro 1", txt, re.I))
    assert con_regla >= 20, f"el principio aparece en {con_regla} artefactos"
    assert con_regla > r["artefactos_que_lo_refieren"] * 5, (
        "el principio debe estar mucho más presente que su identificador")


def test_ataque_mencion_no_es_autoridad():
    """*«mención ≠ referencia ≠ dependencia ≠ consumo ≠ autoridad»*. Un simple
    `referenciado=True` produjo cuatro falsos positivos hoy. Los tipos deben
    separarse: hay ADR mencionados que nadie invoca como fundamento."""
    solo_mencion = [r for r in A.centralidad()
                    if r["artefactos_que_lo_refieren"] > 0
                    and r["lo_invocan_como_autoridad"] == 0]
    assert solo_mencion, (
        "ningún ADR está sólo mencionado: los tipos de relación colapsaron")
    for r in solo_mencion[:3]:
        assert A.AUTORIDAD not in r["relaciones"]
