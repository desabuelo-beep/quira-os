# -*- coding: utf-8 -*-
"""
app/observatorio/despacho.py — el mando de la Consola de Operación
═══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (Javo · 2026-08-10): la consola tenía 710 líneas y **cero
botones**. Mostraba lo que la máquina había hecho y no ofrecía forma de pedirle
que hiciera nada. Para capturar cualquier cosa había que decírselo al director,
y eso deja el sistema apagado en cuanto el director no está.

  «No siempre vamos a trabajar con Claude direccionando el sistema. QUIRA debe
   hacer todo sola, y el operario del observatorio controlar.»

Este módulo es la frontera entre esa orden y su ejecución. Traduce
«monitorear transparencia de Montecristi, marzo de 2025» al procedimiento
concreto, lo lanza, lo registra y devuelve un estado. **Nunca lanza una
excepción muda**: si algo no puede ejecutarse, dice por qué (ADR-042 §6).

QUÉ NO HACE, a propósito:
  · No captura. Eso es de los conectores y los scripts, que ya existen.
  · No decide si el resultado es publicable. Eso es del circuito de validación.
  · No inventa procedimientos: si una fuente no tiene uno declarado aquí, la
    consola no ofrece el botón. Un botón que no ejecuta nada es peor que su
    ausencia, porque promete una capacidad inexistente.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from app.observatorio.corrida import Corrida, registrar
from app.observatorio.estados import Estado

_RAIZ = Path(__file__).resolve().parents[2]
_DIR = _RAIZ / "data" / "observatorio"
_LOCK = _DIR / "en_curso.json"

# Una corrida que lleva más de esto sin cerrar se considera colgada. No la mata
# —puede seguir viva y escribiendo— pero deja de bloquear el botón: si no,
# un proceso muerto dejaría la fuente inoperable para siempre.
_MINUTOS_VENCIMIENTO = 90


# ══════════════════════════════════════════════════════════════════════════════
# CATÁLOGO DE PROCEDIMIENTOS
#
# Cada fuente operable declara QUÉ se ejecuta. `version` cambia cuando cambia el
# método, y viaja a la corrida: sin eso, dos capturas del mismo mes hechas con
# procedimientos distintos serían indistinguibles en el registro.
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Procedimiento:
    id: str
    version: str
    guion: str                                   # ruta relativa al repositorio
    args: "Callable[[Contexto], list[str]]"      # cada guion tiene SU interfaz
    descripcion: str
    requiere_api: bool = False                   # True = necesita presupuesto de modelo


@dataclass(frozen=True)
class Contexto:
    """Lo que un procedimiento necesita saber del encargo. `ruc` va aparte del
    código de municipio porque los guiones identifican entidades por RUC, no por
    el código interno — y confundirlos fue lo que casi rompe este módulo."""
    municipio: str
    ruc: str
    periodo: str
    anio: int


# Cada guion declara sus PROPIOS argumentos. La primera versión de este catálogo
# asumía una convención común —`--municipio` y `--periodo` para todos— y era
# falsa: `rc_scout.py` usa `--download --ruc` y `fetch_rdc_cpccs.py` usa
# `--ruc --year`. Con la convención inventada, cada botón habría lanzado un
# proceso que muere por argumento desconocido, y la corrida habría quedado
# registrada como lanzada. Verificado contra el `argparse` de cada guion.
_PROCEDIMIENTOS: dict[str, Procedimiento] = {
    "transparencia": Procedimiento(
        id="captura_dpe_mensual",
        version="v1",
        guion="scripts/rc_scout.py",
        args=lambda c: ["--download", "--ruc", c.ruc],
        descripcion="Descarga del portal de la Defensoría lo que el municipio publicó.",
    ),
    "cpccs": Procedimiento(
        id="captura_cpccs_anual",
        version="v1",
        guion="scripts/fetch_rdc_cpccs.py",
        args=lambda c: ["--ruc", c.ruc, "--year", str(c.anio)],
        descripcion="Descarga el informe de rendición y su circuito de cumplimiento.",
    ),
}

# Declarados y NO ejecutables. Se listan para que la consola pueda decir por qué
# no hay botón, en vez de callar la fuente (ADR-046 §2.4: la ausencia se muestra).
_SIN_PROCEDIMIENTO: dict[str, str] = {
    "sercop":  "El conector existe, pero no hay procedimiento de captura declarado.",
    "cne":     "Sin conector. Es el origen de la cadena y sigue siendo el hueco mayor.",
    "web_gad": "Sin conector. Cada municipio publica en su propio formato.",
}


# ══════════════════════════════════════════════════════════════════════════════
# ÓRDENES Y RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class Orden:
    fuente: str
    municipio: str
    periodo: str
    modo: str = "calibracion"   # «calibracion» no publica nunca (corrida.es_publicable)


@dataclass
class Despacho:
    """Resultado de intentar despachar una orden. Siempre se devuelve uno."""
    aceptada: bool
    motivo: str
    corrida_id: str | None = None
    procedimiento: str | None = None
    incidencias: list[str] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════════════
# ESTADO DE LO QUE ESTÁ CORRIENDO
# ══════════════════════════════════════════════════════════════════════════════

def _clave(fuente: str, municipio: str) -> str:
    return f"{fuente}:{municipio}"


def _leer_lock() -> dict:
    try:
        return json.loads(_LOCK.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError):
        # Un lock ilegible no puede bloquear la operación entera: se reporta
        # como vacío y la incidencia se registra en la corrida siguiente.
        return {}


def _escribir_lock(datos: dict) -> None:
    _DIR.mkdir(parents=True, exist_ok=True)
    _LOCK.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def _vencida(inicio_iso: str) -> bool:
    try:
        ini = datetime.fromisoformat(inicio_iso)
    except ValueError:
        return True
    delta = datetime.now(timezone.utc) - ini
    return delta.total_seconds() > _MINUTOS_VENCIMIENTO * 60


def en_curso() -> dict[str, dict]:
    """Corridas vivas, ya descontadas las vencidas."""
    lock = _leer_lock()
    vivas = {k: v for k, v in lock.items() if not _vencida(v.get("inicio", ""))}
    if len(vivas) != len(lock):
        _escribir_lock(vivas)
    return vivas


def liberar(fuente: str, municipio: str) -> None:
    """Quita el bloqueo de una fuente. Es lo que hace «reintentar» cuando una
    corrida quedó colgada: no mata el proceso —puede seguir vivo— pero permite
    ordenar otra."""
    lock = _leer_lock()
    lock.pop(_clave(fuente, municipio), None)
    _escribir_lock(lock)


# ══════════════════════════════════════════════════════════════════════════════
# DESPACHO
# ══════════════════════════════════════════════════════════════════════════════

def puede_ejecutarse(fuente: str) -> tuple[bool, str]:
    """¿Hay procedimiento para esta fuente, y puede correrse hoy?"""
    p = _PROCEDIMIENTOS.get(fuente)
    if p is None:
        return False, _SIN_PROCEDIMIENTO.get(
            fuente, "No hay procedimiento declarado para esta fuente.")
    if p.requiere_api:
        return False, ("El procedimiento requiere presupuesto de modelo. "
                       "Queda declarado y a la espera.")
    if not (_RAIZ / p.guion).exists():
        return False, f"El procedimiento declara `{p.guion}`, que no existe en el repositorio."
    return True, p.descripcion


def ruc_de(municipio: str) -> str | None:
    """RUC de un municipio según el registro canónico. Sin RUC no hay orden: los
    guiones identifican entidades por RUC y adivinarlo produciría una captura
    sobre el municipio equivocado."""
    try:
        reg = json.loads((_RAIZ / "data" / "municipality_registry.json")
                         .read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for ruc, codigo in (reg.get("lookup", {}).get("por_ruc") or {}).items():
        if str(codigo) == str(municipio):
            return ruc
    return None


def _armar(p: Procedimiento, orden: Orden, ruc: str) -> list[str]:
    anio = int(str(orden.periodo)[:4]) if str(orden.periodo)[:4].isdigit() \
        else datetime.now(timezone.utc).year
    ctx = Contexto(municipio=orden.municipio, ruc=ruc, periodo=orden.periodo, anio=anio)
    return [sys.executable, str(_RAIZ / p.guion), *p.args(ctx)]


def despachar(orden: Orden) -> Despacho:
    """Lanza el procedimiento de una fuente y registra la corrida.

    El proceso corre APARTE (`Popen`) y no bloquea la interfaz: una captura de
    doce meses tarda minutos, y Streamlit congelaría la pantalla entera
    mientras tanto. La consola sigue el avance leyendo el registro."""
    ok, motivo = puede_ejecutarse(orden.fuente)
    if not ok:
        return Despacho(False, motivo)

    vivas = en_curso()
    clave = _clave(orden.fuente, orden.municipio)
    if clave in vivas:
        desde = vivas[clave].get("inicio", "?")
        return Despacho(False, f"Ya hay una corrida en curso para esta fuente (desde {desde}).")

    ruc = ruc_de(orden.municipio)
    if not ruc:
        return Despacho(False, f"El municipio {orden.municipio} no tiene RUC en el registro "
                               f"canónico. Sin RUC el guion no sabe a quién consultar.")

    p = _PROCEDIMIENTOS[orden.fuente]
    c = Corrida(
        municipio=orden.municipio, fuente=orden.fuente, periodo=orden.periodo,
        procedimiento=p.id, version_procedimiento=p.version, tipo=orden.modo,
    )

    incidencias: list[str] = []
    try:
        _DIR.mkdir(parents=True, exist_ok=True)
        salida = _DIR / f"log_{c.id}.txt"
        with open(salida, "w", encoding="utf-8") as fh:
            proc = subprocess.Popen(
                _armar(p, orden, ruc), cwd=str(_RAIZ), stdout=fh,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
    except Exception as e:  # noqa: BLE001
        # El fallo al LANZAR es distinto del fallo al capturar: aquí la fuente
        # no tiene la culpa, y decirlo evita atribuir al municipio una ausencia
        # que es nuestra (ADR-046 §1).
        c.estado = Estado.ERROR_TECNICO.value
        c.incidencias = [f"no se pudo lanzar el procedimiento: {type(e).__name__}: {e}"]
        registrar(c)
        return Despacho(False, f"No se pudo lanzar el procedimiento: {e}",
                        corrida_id=c.id, incidencias=c.incidencias)

    vivas[clave] = {"pid": proc.pid, "inicio": c.inicio,
                    "corrida": c.id, "procedimiento": p.id, "periodo": orden.periodo}
    _escribir_lock(vivas)
    registrar(c)
    return Despacho(True, f"Corrida lanzada · {p.id} {p.version}",
                    corrida_id=c.id, procedimiento=p.id, incidencias=incidencias)


def log_de(corrida_id: str, ultimas: int = 40) -> str:
    """Últimas líneas del log de una corrida. Vacío si aún no escribió nada."""
    f = _DIR / f"log_{corrida_id}.txt"
    try:
        return "\n".join(f.read_text(encoding="utf-8", errors="replace").splitlines()[-ultimas:])
    except (FileNotFoundError, OSError):
        return ""
