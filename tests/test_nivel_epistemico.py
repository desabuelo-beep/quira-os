# -*- coding: utf-8 -*-
"""
tests/test_nivel_epistemico.py — el detector epistémico deja de depender de que
alguien se acuerde de correrlo
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-26 · decisión 3 del registro de autoridad).
`scripts/ci/check_epistemico.py` vigilaba desde agosto que el texto que lee el
ciudadano no llamara «auditoría» a QUIRA, no acusara y no diera órdenes al GAD.
Pero **detectaba sin bloquear y no estaba enganchado a nada**: dependía de que
alguien lo ejecutara a mano. Una defensa que hay que recordar activar es
exactamente la que falla el día que importa.

POR QUÉ NO SE ENGANCHÓ ANTES, y el hallazgo que lo desbloqueó. Sus cuatro
señales vivas se auditaron una por una con el protocolo del colega —patrón,
texto, negación, mención o afirmación, contradicción real, autoridad invocada,
qué haría el gate— y **las cuatro eran falsos positivos**:

    «La rendición de cuentas es obligatoria»   describe la ley, no prescribe
    «imposibilidad de auditoría»                predica del documento, no de QUIRA
    «Período Informe Fecha … Componentes»       es una cabecera de tabla

Activar el gate entonces habría bloqueado por 100 % de ruido. La causa de fondo
era que **los patrones no son homogéneos**: unos detectan violaciones inequívocas
del canon y otros hacen preguntas de juicio cuyo motivo termina literalmente en
«¿es ese el sentido?». De ahí la separación ERROR / SEÑAL.

SE IMPORTA, NO SE LANZA. Correrlo por `subprocess` cruzaría la frontera de
efectos de la deuda 4-ter sin declararla, y no hace falta: el script es puro.

Dylus Lab © 2026
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))


def _detector():
    ruta = RAIZ / "scripts" / "ci" / "check_epistemico.py"
    spec = importlib.util.spec_from_file_location("_check_epistemico", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _errores(mod, carpeta: Path) -> list[str]:
    fuera = []
    for archivo, items in mod.revisar(carpeta).items():
        for cat, linea, hit, motivo, _ctx, nivel in items:
            if nivel == mod.ERROR:
                fuera.append(f"{archivo}:{linea} [{cat}] «{hit}» — {motivo}")
    return fuera


# ── EL GATE ───────────────────────────────────────────────────────────────────
def test_el_texto_que_lee_el_ciudadano_no_viola_el_canon():
    """Lo que este gate impide que llegue al producto:

    · llamar **auditoría** a QUIRA — `CONSTITUCION-001` la define como
      infraestructura de conocimiento verificable (DEC-0012);
    · **lenguaje acusatorio** —«incumplió», «ilegal», «irregular»—, prohibido
      por la Regla de Oro 2;
    · que el sistema **ordene** al GAD: QUIRA informa y conecta, no actúa;
    · **certificar verdad** en vez de verificabilidad.

    Las SEÑALES —preguntas de juicio— no entran aquí: se imprimen al correr el
    script y las resuelve una persona."""
    mod = _detector()
    violaciones = _errores(mod, RAIZ / "app" / "viz" / "render")
    assert not violaciones, (
        "el texto que ve el ciudadano viola el canon:\n  " +
        "\n  ".join(violaciones))


def test_el_gate_se_comporta_como_debe_ante_casos_conocidos(tmp_path):
    """LA PRUEBA DE COMPORTAMIENTO, independiente del corpus real.

    Sin ella, `test_el_texto_que_lee_el_ciudadano_no_viola_el_canon` sólo dice
    que **hoy** `app/viz/render` está limpio: si mañana ese código se vaciara o
    se moviera, pasaría trivialmente sin detectar nada. Probar el corpus no es
    probar el detector.

    Los seis casos son los que se auditaron a mano el 2026-08-26 —tres
    violaciones reales y tres falsos positivos que costaron el gate—. Estaban
    verificados en un fixture temporal que se borró al terminar; aquí quedan
    fijados. *(Precisión del colega: «si sólo fueron pruebas manuales, yo
    registraría esa diferencia».)*"""
    mod = _detector()
    CASOS = [
        # (texto, ¿debe bloquear?, por qué)
        ("QUIRA es una auditoria de la gestion municipal del canton",
         True, "predica «auditoría» de QUIRA — CONSTITUCION-001 lo excluye"),
        ("El municipio incumplio la norma de transparencia del periodo",
         True, "lenguaje acusatorio — Regla de Oro 2"),
        ("El municipio debe corregir su plan operativo antes del cierre",
         True, "el sistema ordenando al GAD — QUIRA informa, no actúa"),
        ("cada afirmacion sin registro constituye una imposibilidad de auditoría",
         False, "«auditoría» predica del documento, no de QUIRA"),
        ("La rendición de cuentas es el acto anual y obligatorio de la autoridad",
         False, "describe un deber que fija la ley; no lo impone QUIRA"),
        ("Período Informe Fecha Lugar Asistentes Componentes",
         False, "cabecera de tabla: no afirma nada"),
    ]
    # ⚠️ Para los falsos positivos se exige CERO hallazgos de cualquier nivel, no
    # sólo cero ERROR. La primera versión miraba únicamente los ERROR y por eso no
    # detectó el ataque que retiraba `_OBLIGACION_AJENA`: esa supresión evita una
    # señal de nivel SEÑAL, invisible para un contador de errores. Un guard que
    # sólo vigila lo que bloquea deja sin proteger todo lo que hace legible el
    # informe — y un informe ilegible acaba desactivado igual que un gate que grita.
    fallos = []
    for texto, debe_bloquear, por_que in CASOS:
        f = tmp_path / "caso.py"
        f.write_text(f'X = {texto!r}\n', encoding="utf-8")
        if debe_bloquear:
            if not _errores(mod, tmp_path):
                fallos.append(f"NO bloqueó y debía: «{texto[:52]}…» — {por_que}")
        else:
            todos = sum(len(v) for v in mod.revisar(tmp_path).values())
            if todos:
                fallos.append(f"marcó y NO debía: «{texto[:52]}…» — {por_que}")
    assert not fallos, "el gate cambió de comportamiento:\n  " + "\n  ".join(fallos)


def test_el_gate_distingue_error_de_pregunta():
    """LA PRUEBA QUE HACE HONESTO AL GATE.

    Si todos los patrones fueran ERROR, bloquearía por dudas legítimas y alguien
    lo desactivaría — el destino de todo guard que grita. Si ninguno lo fuera,
    no defendería nada. Se comprueba que existen las dos clases y que el nivel
    está asignado donde corresponde."""
    mod = _detector()
    niveles = {}
    for _pat, cat, motivo, nivel in mod.SEÑALES:
        niveles.setdefault(nivel, []).append((cat, motivo))

    assert mod.ERROR in niveles and mod.SENAL in niveles, (
        "el detector perdió una de las dos clases: o bloquea por preguntas, o "
        "dejó de bloquear por violaciones")

    # Un motivo que pregunta no puede ser bloqueante.
    preguntas_que_bloquean = [m for c, m in niveles[mod.ERROR] if "?" in m]
    assert not preguntas_que_bloquean, (
        f"patrones marcados ERROR cuyo motivo es una pregunta: "
        f"{preguntas_que_bloquean}. Si hay que preguntar, no se puede bloquear.")

    # Y lo que la Regla 2 prohíbe expresamente tiene que ser ERROR. Son DOS los
    # patrones que hablan de incumplimiento —el acusatorio y «certifica el
    # incumplimiento»—, así que se comprueba el conjunto, no la cardinalidad:
    # esperar exactamente uno hacía fallar la prueba por contar, no por medir.
    acusatorio = {n for p, c, m, n in mod.SEÑALES if "incumpl" in p.pattern}
    assert acusatorio == {mod.ERROR}, (
        f"el lenguaje acusatorio dejó de ser bloqueante ({acusatorio}), y la "
        f"Regla de Oro 2 lo prohíbe sin matices")


def test_las_tres_supresiones_siguen_puestas():
    """Las tres causas de falso positivo que se auditaron. Si alguna se retira,
    el gate vuelve a gritar por ruido y acabará desactivado."""
    fuente = (RAIZ / "scripts" / "ci" / "check_epistemico.py").read_text(
        encoding="utf-8")
    for guarda, que_evita in (
            ("_OBLIGACION_AJENA", "describir un deber legal se tomaría por prescribirlo"),
            ("_TERMINO_SOBRE_OTRO", "«imposibilidad de auditoría» se leería como que QUIRA lo es"),
            ("_es_cabecera", "una cabecera de tabla se juzgaría como si afirmara algo")):
        assert guarda in fuente, f"se retiró {guarda}: {que_evita}"
