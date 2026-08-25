# -*- coding: utf-8 -*-
"""
tests/test_ensayo_vs_observacion.py — un ensayo no se guarda donde la observación
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-25). Cerrando la portabilidad aparecieron dos archivos
de procedencia sin rastrear. Al contarlos, el directorio del sujeto observado
decía esto:

    85 corridas en seco  ·  4 reales

El 95 % de la carpeta de procedencia de 130801 **no observó nada**. Todas se
llamaban igual —`provenance_130801_<fecha>.json`— y vivían en el mismo sitio;
la única diferencia era un campo `dry_run` dentro del archivo. Quien barriera
el directorio con un glob obtenía 89 registros que *parecen* procedencia del
sujeto.

Es exactamente el error que este dominio persigue afuera —**«el nombre del
enlace no es evidencia»**, anotado tres veces contra el GAD— cometido aquí
contra nosotros mismos. Y es el más grave de los dos sentidos posibles: no
inventa un incumplimiento del sujeto, pero **fabrica actividad propia**.

LO QUE ESTAS PRUEBAS DEFIENDEN:

    Un artefacto que no observó al sujeto no puede ser indistinguible, por su
    ubicación ni por su nombre, de uno que sí lo observó.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

SNAPSHOTS = RAIZ / "data" / "snapshots"


def _procedencias_declaradas() -> list[Path]:
    """Lo que un consumidor razonable leería como procedencia del sujeto: los
    JSON que están en `provenance/`, sin entrar a los subdirectorios."""
    return [f for d in SNAPSHOTS.glob("*/provenance")
            for f in d.glob("*.json") if d.is_dir()]


def test_ningun_ensayo_se_hace_pasar_por_observacion():
    """El caso que originó la prueba. Si un `dry_run` reaparece en el
    directorio principal, algo volvió a mezclar ensayo con observación."""
    intrusos = []
    for f in _procedencias_declaradas():
        try:
            if json.loads(f.read_text(encoding="utf-8")).get("dry_run") is True:
                intrusos.append(f.relative_to(RAIZ))
        except (json.JSONDecodeError, OSError):
            continue                       # ilegible es otro problema, no éste
    assert not intrusos, (
        f"{len(intrusos)} corridas en seco guardadas como si fueran procedencia "
        f"del sujeto: {intrusos[:5]}. Un `dry_run` no dice nada del sujeto — "
        f"dice que ejercitamos el instrumento.")


def test_el_nombre_del_archivo_tambien_lo_declara():
    """La ubicación no basta: un archivo se copia, se adjunta, se comparte
    suelto. Debe decir qué es **por sí mismo**, igual que se le exige a la
    procedencia de los artefactos del sujeto (deuda #2 del registro d07)."""
    for d in SNAPSHOTS.glob("*/provenance/ensayos"):
        mal = [f.name for f in d.glob("*.json") if not f.name.startswith("ensayo_")]
        assert not mal, (
            f"ensayos que no se declaran ensayos en su propio nombre: {mal[:5]}")


def test_el_emisor_separa_por_estructura_no_por_confianza():
    """La defensa no puede depender de que alguien recuerde mirar el campo.
    Se comprueba en el emisor: misma corrida, dos destinos distintos."""
    from app.pipelines import snapshot_pipeline as sp

    fuente = Path(sp.__file__).read_text(encoding="utf-8")
    cuerpo = fuente[fuente.index("def _step_emit_provenance"):]
    cuerpo = cuerpo[:cuerpo.index("# ── CÁLCULOS INTERNOS")]

    assert 'prov_dir = prov_dir / "ensayos"' in cuerpo, (
        "el emisor volvió a escribir ensayo y observación en el mismo directorio")
    assert 'prefijo = "ensayo" if dry_run else "provenance"' in cuerpo, (
        "el emisor volvió a darles el mismo nombre")


def test_las_observaciones_reales_siguen_donde_estaban():
    """El contrapeso: separar no puede convertirse en esconder. Lo que sí
    observó al sujeto tiene que seguir siendo legible donde siempre estuvo."""
    reales = _procedencias_declaradas()
    assert reales, ("no quedó ninguna procedencia real: la separación borró o "
                    "movió lo que debía conservar")
    for f in reales:
        d = json.loads(f.read_text(encoding="utf-8"))
        assert d.get("dry_run") is False
        assert d.get("municipio_code"), "una procedencia sin sujeto no es procedencia"
