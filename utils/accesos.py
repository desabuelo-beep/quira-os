"""
QUIRA OS — Lectura de la bitácora de accesos
=========================================================================
POR QUÉ EXISTE (2026-08-18). Javo, tras publicar el landing en LinkedIn:

    «Están ingresando a QUIRA y no sé qué, ni quiénes, ni cómo.»

Resultó que la bitácora **ya existía y llevaba dos meses registrando** —343
eventos, incluidos tres intentos fallidos de contraseña—. El problema no era
falta de registro: era que sólo podía leerse abriendo el archivo a mano, así que
nadie lo leía. Un control que nadie mira no es un control.

Este módulo convierte `logs/audit.log` en algo consultable. No añade telemetría
ni instala analítica de terceros: **lee lo que el sistema ya escribe.**

POR QUÉ NO SE USA ANALÍTICA EXTERNA. Se evaluó incrustar Google Analytics y se
descartó por tres razones. Técnica: `st.components.v1.html` monta un iframe
aislado y la etiqueta no vería la aplicación padre — mediría el iframe y
entregaría un dato falso con apariencia de dato, que es justo lo que QUIRA
existe para combatir. De coherencia: un sistema que audita transparencia pública
no puede rastrear a quien lo visita con herramientas de un tercero. Y de
control: esos datos vivirían fuera de Dylus Lab.

LO QUE **NO** SE REGISTRA, y es deliberado: ni IP, ni huella de navegador, ni
identificador persistente de visitante. Sólo la procedencia declarada del enlace
y la actividad de las sesiones autenticadas.

Dylus Lab © 2026
"""
from __future__ import annotations

import datetime as _dt
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

_LOG = Path("logs") / "audit.log"

# Un pico de fallos en poco tiempo es la señal que distingue a alguien que teclea
# mal de alguien que prueba contraseñas. El umbral es de vigilancia, no una regla
# de bloqueo: el bloqueo real lo aplica la sesión a los 3 intentos.
VENTANA_ALERTA_MIN = 30
FALLOS_PARA_ALERTA = 3


@dataclass
class Resumen:
    total: int = 0
    por_evento: dict[str, int] = field(default_factory=dict)
    desde: str = ""
    hasta: str = ""
    accesos_ok: int = 0
    fallos: int = 0
    bloqueos: int = 0
    landings: int = 0
    origenes: dict[str, int] = field(default_factory=dict)
    modulos: dict[str, int] = field(default_factory=dict)
    usuarios: dict[str, int] = field(default_factory=dict)
    alertas: list[dict] = field(default_factory=list)
    ultimos: list[dict] = field(default_factory=list)


def _eventos(ruta: Path | None = None) -> list[dict]:
    p = ruta or _LOG
    if not p.exists():
        return []
    fuera = []
    for linea in p.read_text(encoding="utf-8", errors="replace").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        try:
            fuera.append(json.loads(linea))
        except json.JSONDecodeError:
            # Una línea corrupta no invalida la bitácora, pero tampoco se
            # descarta en silencio: se cuenta como evento ilegible.
            fuera.append({"event": "ILEGIBLE", "ts": ""})
    return fuera


def _fecha(ts: str) -> _dt.datetime | None:
    try:
        return _dt.datetime.fromisoformat(str(ts).rstrip("Z"))
    except (ValueError, TypeError):
        return None


def detectar_alertas(eventos: list[dict]) -> list[dict]:
    """Fallos concentrados en una ventana corta.

    Tres contraseñas erradas en dos meses son un despiste; tres en media hora
    son otra cosa. La bitácora ya distinguía ambos casos — faltaba mirarla."""
    fallos = sorted(
        (e for e in eventos if e.get("event") in ("LOGIN_FAIL", "LOCKOUT")),
        key=lambda e: str(e.get("ts", "")))
    alertas, ventana = [], []
    for e in fallos:
        f = _fecha(e.get("ts", ""))
        if not f:
            continue
        ventana = [x for x in ventana
                   if (f - x[0]).total_seconds() <= VENTANA_ALERTA_MIN * 60]
        ventana.append((f, e))
        if len(ventana) >= FALLOS_PARA_ALERTA:
            alertas.append({
                "desde": ventana[0][0].isoformat(timespec="minutes"),
                "hasta": f.isoformat(timespec="minutes"),
                "fallos": len(ventana),
                "usuarios": sorted({str(x[1].get("usuario", "—")) for x in ventana}),
            })
            ventana = []          # se cierra el episodio y se abre uno nuevo
    return alertas


def resumir(ruta: Path | None = None, ultimos_n: int = 25) -> Resumen:
    ev = _eventos(ruta)
    r = Resumen(total=len(ev))
    if not ev:
        return r

    r.por_evento = dict(Counter(e.get("event", "?") for e in ev).most_common())
    fechas = sorted(str(e.get("ts", "")) for e in ev if e.get("ts"))
    r.desde, r.hasta = (fechas[0][:16], fechas[-1][:16]) if fechas else ("", "")

    r.accesos_ok = r.por_evento.get("LOGIN_OK", 0)
    r.fallos = r.por_evento.get("LOGIN_FAIL", 0)
    r.bloqueos = r.por_evento.get("LOCKOUT", 0)
    r.landings = r.por_evento.get("LANDING", 0)

    r.origenes = dict(Counter(e.get("origen", "—") for e in ev
                              if e.get("event") == "LANDING").most_common())
    r.modulos = dict(Counter(e.get("page", "—") for e in ev
                             if e.get("event") == "PAGE_VIEW").most_common(10))
    r.usuarios = dict(Counter(e.get("usuario", "—") for e in ev
                              if e.get("event") == "LOGIN_OK").most_common())
    r.alertas = detectar_alertas(ev)
    r.ultimos = sorted(ev, key=lambda e: str(e.get("ts", "")),
                       reverse=True)[:ultimos_n]
    return r


def integridad(ruta: Path | None = None) -> dict:
    """Estado de la propia bitácora.

    Si el registro deja de escribirse, un acceso no autorizado no dejaría huella
    — que es exactamente lo que alguien necesitaría para no ser visto. Por eso el
    estado del instrumento se muestra junto a los datos, y no aparte."""
    p = ruta or _LOG
    if not p.exists():
        return {"estado": "SIN BITÁCORA", "detalle":
                "no existe logs/audit.log — ningún acceso está quedando registrado"}
    ev = _eventos(p)
    ilegibles = sum(1 for e in ev if e.get("event") == "ILEGIBLE")
    ultimo = max((str(e.get("ts", "")) for e in ev), default="")
    dias = None
    f = _fecha(ultimo)
    if f:
        dias = (_dt.datetime.utcnow() - f).days
    return {
        "estado": "ILEGIBLE PARCIAL" if ilegibles else "OK",
        "eventos": len(ev),
        "lineas_ilegibles": ilegibles,
        "ultimo_evento": ultimo[:16],
        "dias_sin_actividad": dias,
        "bytes": p.stat().st_size,
    }
