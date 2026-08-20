"""
app/agents/d07/reglas.py — la única puerta por la que d07 conoce la norma
=========================================================================
POR QUÉ EXISTE (2026-08-18). Javo detuvo el dominio con un reparo de raíz:

> *«No olvide la BRN, CNO, etc., y lo que aterriza la norma al DOM: eso es la
> base, por eso estábamos trabajando mal.»*

Tenía razón. d07 leía la Guía Metodológica desde Python y derivaba allí sus
criterios: la periodicidad la deducía un script, el plazo del día 15 estaba
escrito a mano en `scoring.py`, las fórmulas de ausencia eran una constante de
módulo. Ninguno era inventado —todos salían de la norma— pero **ninguno era
verificable**: no tenían cadena, ni SHA, ni consecuencia declarada. Un criterio
que sólo existe dentro de una función no es norma; es interpretación del
programador con apariencia de norma (ADR-051 §2).

QUÉ HACE ESTE MÓDULO. Es el **único** punto de d07 que sabe que existe una
Regla Operativa, y ni siquiera lee su YAML: eso sólo lo hace el `ROAdapter`
(contrato BRN, invariante 11). De aquí para adentro, el dominio pregunta
«¿cada cuánto debe publicarse CD-06?» y recibe una respuesta — sin saber de qué
artículo salió ni tener que interpretarlo.

    RO YAML → [ ROAdapter ] → ROModel → [ este módulo ] → agentes de d07

LO QUE NO HACE, y es la línea que no debe cruzarse:
  · No interpreta Derecho. Si la RO no declara un parámetro, aquí no se inventa:
    se devuelve `None` y el agente debe tratarlo como `no_determinable`.
  · No define umbrales propios ni valores por defecto «razonables». Un default
    silencioso es un criterio escondido, que es de lo que veníamos.
  · No mide ni califica. Sólo entrega lo que el canon declaró.

ESTADO DE LAS RO. `RO-VII-001` y `RO-VII-002` están en `propuesta` (sólo Javo
promueve a `vigente`, ADR-035 §5). El módulo las carga igual y **expone su
estado**, para que una corrida pueda decidir si publica un resultado calculado
con reglas aún no promovidas. Decidirlo es del orquestador; declararlo, de aquí.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
_BRN = RAIZ / "docs" / "brn"
_SCRIPTS = RAIZ / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from brn_ro_adapter import ROModel, adaptar      # noqa: E402  (único lector del YAML)

# Las RO que gobiernan este dominio. Si mañana d07 necesita otra regla, se declara
# aquí y se modela en `docs/brn/` — no se añade un criterio en el código.
RO_CUMPLIMIENTO = "RO-VII-001"      # SITA · la vara del órgano rector
RO_COBERTURA = "RO-VII-002"         # cobertura material · observación de QUIRA
RO_DOCUMENTAL = "RO-VII-003"        # universo documental del art. 24 (obligación de GAD)
RO_PASIVA = "RO-VII-004"            # atención de solicitudes de acceso (transparencia pasiva)
RO_DIFUSION = "RO-VII-005"          # difusión y capacitación · hoy no observable


class ReglaNoDisponible(RuntimeError):
    """Se pide un parámetro a una RO que no existe o no se pudo cargar.

    Es un error, no un valor por defecto: d07 no puede medir sin su regla, y
    seguir con un supuesto sería reproducir el problema que este módulo corrige."""


@lru_cache(maxsize=8)
def cargar(ro_id: str) -> ROModel:
    import yaml
    p = _BRN / f"{ro_id}.yaml"
    if not p.exists():
        raise ReglaNoDisponible(f"no existe {p.relative_to(RAIZ)}")
    return adaptar(yaml.safe_load(p.read_text(encoding="utf-8")))


def estado_reglas() -> dict[str, str]:
    """Estado de las RO del dominio. El orquestador lo registra en la corrida:
    un resultado calculado con reglas en `propuesta` no es lo mismo que uno
    calculado con reglas vigentes, y esa diferencia debe quedar visible."""
    return {rid: cargar(rid).estado
            for rid in (RO_CUMPLIMIENTO, RO_COBERTURA, RO_DOCUMENTAL,
                        RO_PASIVA, RO_DIFUSION)}


def _param(ro_id: str, clave: str, defecto=None):
    return (cargar(ro_id).parametros or {}).get(clave, defecto)


# ── RO-VII-001 · cumplimiento de publicación ────────────────────────────────────
def periodicidad(cd_id: str) -> str | list[str] | None:
    """Cadencia del CONTENIDO para un conjunto. `None` = la guía no la declara, y
    entonces el conjunto NO se evalúa en temporalidad. Antes esto lo deducía un
    script leyendo el docx; ahora lo dice la RO, conjunto por conjunto."""
    return (_param(RO_CUMPLIMIENTO, "periodicidad_contenido") or {}).get(cd_id)


def cadencia_aplicable(cd_id: str) -> tuple[str | None, str]:
    """Resuelve la cadencia con la que se mide, y por qué.

    Cuando la norma admite dos —«semestral o anual, según varíen los
    contenidos»— la RO declara con cuál se mide (`cadencia_condicionada`). El
    dominio no elige: aplica lo declarado."""
    p = periodicidad(cd_id)
    if p is None:
        return None, "la guía no declara periodicidad de contenidos para este conjunto"
    if p == "por_subnumeral":
        return None, "la periodicidad se declara por sub-numeral, no para el conjunto"
    if isinstance(p, str):
        return p, "cadencia única declarada por la guía"
    modo = _param(RO_CUMPLIMIENTO, "cadencia_condicionada", "menos_exigente")
    orden = {"mensual": 12, "trimestral": 4, "semestral": 2, "anual": 1}
    elegida = (min(p, key=lambda x: orden.get(x, 99)) if modo == "menos_exigente"
               else max(p, key=lambda x: orden.get(x, 0)))
    return elegida, (f"la guía admite «{' o '.join(p)}»; la regla operativa manda "
                     f"medir con la {modo.replace('_', ' ')}")


def periodos_por_anio(cadencia: str) -> int | None:
    return {"mensual": 12, "trimestral": 4, "semestral": 2, "anual": 1}.get(cadencia)


def dia_limite_registro() -> int | None:
    """Día del mes hasta el que puede registrarse. Estaba escrito a mano en
    `scoring.py`; ahora viene de la RO, que además cita su fundamento y explica
    por qué NO es el día 10 de la resolución de 2015."""
    return (_param(RO_CUMPLIMIENTO, "plazo_registro") or {}).get("dia_limite")


def formatos_datos_abiertos() -> set[str]:
    return set(_param(RO_CUMPLIMIENTO, "formatos_datos_abiertos") or ())


def formulas_ausencia() -> list[str]:
    """Las fórmulas que la norma ADMITE para declarar ausencia. La RO prohíbe
    expresamente traducir otras por equivalencia semántica: `no disponible` no
    es `INFORMACIÓN NO DISPONIBLE`, y convertir una en otra reintroduce la
    interpretación que el canon quiere fuera."""
    return list(_param(RO_CUMPLIMIENTO, "formulas_ausencia_admitidas") or ())


def muestreo_cualitativo() -> dict:
    """Muestreo que fija el propio órgano rector para los parámetros
    cualitativos. Importa declararlo: el resultado no es censo, es muestra
    normada, y quien lea el dato debe saberlo."""
    return dict(_param(RO_CUMPLIMIENTO, "muestreo_cualitativo") or {})


def periodos_no_publicados_califican_cero() -> bool:
    """Un período exigido y no publicado, ¿entra al promedio con cero?

    Lo declara el método de la RO. Cuando esto vivía en el bucle del
    orquestador, omitirlo dio `SITA 0,97` en un año con dos conjuntos sin una
    sola publicación: el criterio estaba mal y nadie podía verlo."""
    m = cargar(RO_CUMPLIMIENTO).metodo or {}
    return m.get("periodos_no_publicados") == "califican_cero"


# ── RO-VII-002 · cobertura material ─────────────────────────────────────────────
def dimensiones(cd_id: str) -> list[str]:
    """Dimensiones que la obligación enumera para el conjunto. Vacío = la norma
    no enumera ninguna, y entonces no hay cobertura material que medir."""
    d = (_param(RO_COBERTURA, "dimensiones") or {}).get(cd_id) or {}
    return list(d.get("lista") or ())


def instrumento_de_verificacion(cd_id: str) -> str | None:
    """Instrumento al que la obligación remite para comprobar sus dimensiones.
    `None` = no remite a ninguno, y sin él la ausencia NO se declara: queda
    `no_determinable`. Es la asimetría que evitó cinco hallazgos falsos."""
    d = (_param(RO_COBERTURA, "dimensiones") or {}).get(cd_id) or {}
    return d.get("instrumento_de_verificacion")


def grupos_clasificador() -> dict[str, tuple[str, ...]]:
    c = _param(RO_COBERTURA, "clasificador_presupuestario") or {}
    return {k: tuple(v) for k, v in (c.get("grupos") or {}).items()}


def clasificador_habilitado(obligacion_literal: str | None) -> bool:
    """El clasificador SÓLO se usa donde la propia obligación lo invoca. La RO
    declara la condición; aquí se comprueba contra el texto, sin extrapolar a
    otros conjuntos."""
    c = _param(RO_COBERTURA, "clasificador_presupuestario") or {}
    cond = c.get("habilitado_cuando") or ""
    if not cond or not obligacion_literal:
        return False
    # La condición nombra el instrumento entre comillas angulares; se busca ese
    # término en el enunciado, que es lo verificable sin interpretar.
    import re
    m = re.search(r"«(.+?)»", cond)
    clave = (m.group(1) if m else cond).lower()
    return clave.split()[0][:12] in obligacion_literal.lower()


def caso_sin_dimensiones_determinables() -> dict:
    """Qué hacer cuando NINGUNA dimensión es determinable (el caso 0/0).

    Lo declara la RO precisamente para que el módulo no lo decida en tiempo de
    ejecución: contarlo como 0 imputaría una carencia no probada; como 100,
    acreditaría una cobertura no verificada."""
    return dict(_param(RO_COBERTURA, "caso_sin_dimensiones_determinables") or {})


# ── RO-VII-003 · universo documental del art. 24 ────────────────────────────────
def clases_de_acto() -> list[dict]:
    """Clases de acto que la norma distingue, con el patrón que las reconoce.

    Vivían en `documentos.py` como constante de módulo, y eran criterio normativo
    puro: que un acta no sea una resolución lo decide la ley. Se migraron al
    cerrar `CNO-VII-002` — antes no había cadena a la que anclarlas."""
    return list(_param(RO_DOCUMENTAL, "clases_de_acto") or ())


def clase_exigida(seccion: str) -> dict:
    """Qué clase de acto admite cada sección del literal, y cuál NO la sustituye.

    La sección 2 exige el acta porque su campo dice «Enlace para ver y descargar
    **el acta**»: el fundamento es el campo, no una lectura del analista."""
    return dict((_param(RO_DOCUMENTAL, "clase_exigida_por_seccion") or {}).get(seccion) or {})


def tipos_de_sesion_admitidos() -> list[str]:
    return list(_param(RO_DOCUMENTAL, "tipos_de_sesion_admitidos") or ())


def serie_correlativa() -> dict:
    """Patrón y mínimo para evaluar la continuidad de la numeración de sesiones.
    Un salto señala una sesión sin documentación publicada — verificable sin
    interpretar nada."""
    return dict(_param(RO_DOCUMENTAL, "serie_correlativa") or {})


def documento_no_procesable() -> dict:
    """Qué hacer con un escaneo sin texto. Lo declara la norma operativa para que
    el módulo no lo resuelva por su cuenta: no se transcribe lo que no se leyó.

    Vive en `metodo`, no en `parametros`: es una regla de tratamiento de la
    evidencia, no un valor de configuración."""
    return dict((cargar(RO_DOCUMENTAL).metodo or {}).get("documento_no_procesable") or {})


# ── RO-VII-004 · transparencia pasiva (solicitudes de acceso) ───────────────────
def plazo_respuesta_solicitud() -> dict:
    """Plazo del art. 34: diez días, prorrogable cinco. La prórroga NO es
    discrecional —exige causa justificada E informada al solicitante—, así que
    una prórroga no comunicada no extiende el término."""
    return dict(_param(RO_PASIVA, "plazo_respuesta") or {})


def contenido_minimo_solicitud() -> list[str]:
    """Lo que la solicitud debe contener (art. 32). Se consulta porque una
    petición incompleta no activa el plazo: imputarle el retraso al sujeto
    obligado sería atribuirle un defecto ajeno."""
    return list(_param(RO_PASIVA, "contenido_minimo_solicitud") or ())


def silencio_administrativo() -> dict:
    """Qué significa no contestar. El art. 36 no deja margen: el silencio
    equivale a denegación y habilita la gestión oficiosa y la acción
    constitucional. QUIRA registra el hecho; no ejerce ninguna de las dos vías."""
    return dict(_param(RO_PASIVA, "silencio_administrativo") or {})


def caso_sin_solicitudes() -> dict:
    """Sin solicitudes presentadas NO hay incumplimiento: hay ausencia de
    ejercicio del derecho. Confundirlos convertiría el silencio ciudadano en
    falta del sujeto obligado."""
    return dict((cargar(RO_PASIVA).metodo or {}).get("caso_sin_solicitudes") or {})


# ── RO-VII-005 · difusión y capacitación ────────────────────────────────────────
def frecuencia_minima_difusion() -> dict:
    """«Por lo menos tres veces al año» (Reglamento art. 10). La obligación más
    fácil de verificar del dominio, y la que ningún monitoreo estaba mirando."""
    return dict(_param(RO_DIFUSION, "frecuencia_minima") or {})


def destinatarios_difusion() -> list[dict]:
    """Los dos destinatarios que la norma distingue. Capacitar sólo hacia adentro
    no satisface la obligación: el Reglamento nombra expresamente a las personas
    a las que la entidad sirve."""
    return list(_param(RO_DIFUSION, "destinatarios") or ())


def observabilidad_difusion() -> dict:
    """⚠️ Estado por defecto: `no_observable`. Ningún numeral del art. 19 recoge
    esta actividad, así que el portal no la acredita ni la desmiente. Devolver
    cero imputaría un incumplimiento por una ceguera propia — la lección de
    OBS-030 aplicada por adelantado."""
    return dict((cargar(RO_DIFUSION).metodo or {}).get("observabilidad") or {})


def condiciones_de_escalamiento() -> list[str]:
    """Las condiciones que deben cumplirse TODAS para hablar de posible
    incumplimiento. Ningún agente puede saltar del hecho verificable a la
    calificación jurídica sin ellas (ADR-051 §4)."""
    import yaml
    p = _BRN / f"{RO_COBERTURA}.yaml"
    if not p.exists():
        return []
    # `niveles` no forma parte del contrato del ROAdapter todavía; se lee del
    # canon con el mismo criterio y se declara aquí para que quede visible que
    # es una lectura de nivel, no un criterio propio del dominio.
    doc = yaml.safe_load(p.read_text(encoding="utf-8"))
    for n in doc.get("niveles") or []:
        if n.get("id") == "posible_incumplimiento":
            return list(n.get("requiere_todas") or ())
    return []
