"""
QUIRA — Monitoreo de Fuentes  ·  `quira_pages/p_monitoreo_fuentes.py`

La consola desde la que se OPERA la captura de evidencia pública: se despacha,
se vigila y se valida. No es un tablero para mirar.

────────────────────────────────────────────────────────────────────────────────
QUÉ CAMBIÓ Y POR QUÉ (Javo · 2026-08-06, corrigiendo al director)
────────────────────────────────────────────────────────────────────────────────
La primera versión era un «Panel del Observatorio»: cifras contadas de los
registros, para leer. Estaba mal encuadrado. Lo que hace falta es el sitio desde
donde se envían los agentes, los guiones y los ciclos que recorren los silos
públicos, extraen, procesan, y con los motores actualizan cada dominio — de
forma automática y mensual.

La distinción que SÍ se conserva, y es la razón de que esta pantalla no viva
dentro del Centro:
  · El CENTRO responde «¿qué dice la evidencia sobre la gestión?». Su lector
    quiere entender el territorio.
  · Esta consola responde «¿de dónde salió, cuándo, y está completa?». Su
    usuario opera la máquina.
Mezclarlas obligaría al Centro a explicarle a una autoridad por qué falló una
captura. Lo que SÍ pertenece a cada dominio es la cobertura de SUS datos —qué
periodo abarcan y cuándo se actualizaron—, y ahí es donde debe verse.

────────────────────────────────────────────────────────────────────────────────
LOS SILOS — y la relación con los dominios NO es uno a uno
────────────────────────────────────────────────────────────────────────────────
La consola vigila las fuentes públicas que alimentan a TODOS los dominios, no a
uno. Y la correspondencia es de muchos a muchos: una fuente aporta evidencia a
varios dominios, y un dominio necesita evidencia de varias fuentes. Escribirlo
como «SERCOP → d02» sería tratar el sistema como un conjunto de raspadores con
destino fijo; lo que lo hace una infraestructura de conocimiento es justamente
que las fuentes se cruzan.

Un silo sin capturador se muestra pendiente, nunca como si estuviera listo.

────────────────────────────────────────────────────────────────────────────────
DÓNDE DESEMBOCA LA EVIDENCIA — dos universos, un contrato
────────────────────────────────────────────────────────────────────────────────
No todo converge en el Gold Master. ADR-023 es explícito: «Excel = motor ·
Corpus = evidencia verificable del motor», y la MATRIZ_CANONICA es el contrato
semántico entre ambos — «la tabla de correspondencia entre el universo Excel y
el universo documental».

  · La evidencia DOCUMENTAL capturada vive en el corpus y en el grafo.
  · Las MÉTRICAS las calcula el Gold Master, y solo él.
  · La MATRIZ_CANONICA es lo que impide que sean dos mundos.

Importa para esta consola porque decide dónde deja lo que captura: un documento
del portal no «entra al Gold Master», entra al corpus con su huella; lo que
llega al motor son los insumos numéricos que ya estaban previstos en la matriz.

────────────────────────────────────────────────────────────────────────────────
DOCTRINA
────────────────────────────────────────────────────────────────────────────────
 1 · Ninguna cifra escrita a mano: todo se cuenta al abrir.
 2 · Cada número con su denominador. «227 documentos» es publicidad;
     «227 de 252» informa.
 3 · Lo que falta se declara. Un registro ilegible sale como «sin dato», con
     borde punteado, no como un cero.
 4 · La ausencia se muestra como ausencia, nunca como un suspenso en rojo.
 5 · Frontera de lenguaje (Regla 2), aunque el público sea el propio equipo.
 6 · No se recalcula nada (Reglas 1 y 4): se lee, se cuenta y se despacha.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo

_RAIZ = Path(__file__).resolve().parents[1]
_DATA = _RAIZ / "data"
_PCD = _RAIZ / "docs" / "pcd"
_CENSO = _DATA / "scouting" / "gad_municipales_all.json"
_SCAN = _DATA / "scouting" / "manabi_scan.json"

# Universo de observación (ADR-041 §4-bis). No es 221: la Ley del 8-oct-2024
# creó el cantón 222, Sevilla Don Bosco, cuyo GAD no tiene todavía un ciclo
# completo de gestión — se cuenta en el universo y se declara aparte.
_GAD_PAIS = 222

# La secuencia es progresiva por diseño (Javo): se valida el cantón piloto
# —2025 completo y lo que va de 2026— antes de ampliar el barrido.
_CANTON_PILOTO = "MONTECRISTI"
_MESES = ("E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D")


# ══════════════════════════════════════════════════════════════════════════════
# LOS SILOS DE INFORMACIÓN PÚBLICA
# ══════════════════════════════════════════════════════════════════════════════
# `conector` apunta al módulo que sabe hablar con la fuente. Si no existe, el
# silo se muestra como pendiente: declarar la falta es el trabajo, fingir que
# está listo sería lo contrario de lo que hace este sistema.
#
# `aporta_a` NO es «pertenece a». Es la lista de dominios a los que esa fuente
# puede aportar evidencia, y varias fuentes concurren sobre el mismo dominio —
# el mandato electoral solo se puede contrastar cruzando CNE con planificación y
# con lo efectivamente contratado, por ejemplo. Cada dominio decide qué evidencia
# admite; la consola solo dice de dónde puede venir.
_SILOS: list[dict[str, Any]] = [
    {
        "id": "transparencia",
        "nombre": "Portal de Transparencia",
        "entidad": "Defensoría del Pueblo",
        "que": "Cumplimiento mensual de la obligación de publicar. La "
               "obligación es del municipio y la Defensoría registra si la "
               "cumple: se lee ese registro sin pedirle nada al GAD.",
        "conector": "app/connectors/dpe.py",
        "herramienta": "scripts/rc_scout.py",
        "dominios": ["d07 Transparencia", "d02 Presupuesto", "d09 Rendición"],
        "cadencia": "mensual",
    },
    {
        "id": "sercop",
        "nombre": "Contratación Pública",
        "entidad": "SERCOP",
        "que": "Procesos de contratación y plan anual. Permite contrastar lo "
               "planificado contra lo efectivamente contratado.",
        "conector": "app/connectors/sercop.py",
        "herramienta": None,
        "dominios": ["d02 Presupuesto", "d05 Holding", "d01 Planificación"],
        "cadencia": "mensual",
    },
    {
        "id": "cpccs",
        "nombre": "Rendición de Cuentas",
        "entidad": "CPCCS",
        "que": "Informes anuales de rendición y su circuito de cumplimiento "
               "ante el consejo de participación.",
        "conector": "app/connectors/cpccs.py",
        "herramienta": "scripts/fetch_rdc_cpccs.py",
        "dominios": ["d09 Rendición de Cuentas", "d08 Participación"],
        "cadencia": "anual",
    },
    {
        "id": "cne",
        "nombre": "Plan de trabajo electoral",
        "entidad": "CNE",
        "que": "El compromiso con el que la autoridad fue electa. Es el "
               "origen de la cadena: sin él no hay contra qué contrastar la "
               "planificación.",
        "conector": None,
        "herramienta": None,
        "dominios": ["d03 Mandato electoral", "d01 Planificación"],
        "cadencia": "por período",
    },
    {
        "id": "web_gad",
        "nombre": "Portal institucional del GAD",
        "entidad": "cada municipio",
        "que": "Ordenanzas, resoluciones y publicaciones propias que no pasan "
               "por ningún registro central.",
        "conector": None,
        "herramienta": None,
        "dominios": ["d07 Transparencia", "d08 Participación", "otros"],
        "cadencia": "continua",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# LECTURA
# ══════════════════════════════════════════════════════════════════════════════

def _nombre_corto(entidad: dict) -> str:
    """Nombre legible de una entidad del portal. Los oficiales vienen en
    mayúsculas y con la razón social completa; en una rejilla no caben."""
    n = (entidad.get("name") or "").strip()
    alto = n.upper()
    if "GOBIERNO AUTÓNOMO" in alto:
        return "GAD Municipal (matriz)"
    for pista, corto in (("ASEO", "Empresa de Aseo"),
                         ("PATRONATO", "Patronato de Amparo Social"),
                         ("HÁBITAT", "Hábitat y Vivienda"),
                         ("HABITAT", "Hábitat y Vivienda"),
                         ("AGUA", "Agua Potable"),
                         ("BOMBER", "Cuerpo de Bomberos")):
        if pista in alto:
            return corto
    return (entidad.get("name_short") or n)[:34].title()


def _leer(nombre: str) -> tuple[dict | None, str]:
    """(contenido, problema). Un registro ausente no rompe la consola: se
    reporta como lo que es, un dato que no está."""
    try:
        return json.loads((_DATA / nombre).read_text(encoding="utf-8")), ""
    except FileNotFoundError:
        return None, f"`data/{nombre}` no está en el repositorio"
    except json.JSONDecodeError as e:
        return None, f"`data/{nombre}` no es JSON válido (línea {e.lineno})"
    except Exception as e:  # noqa: BLE001
        return None, f"`data/{nombre}`: {type(e).__name__}"


def _corridas() -> tuple[list[dict], str]:
    """Historial de tareas programadas y cola de validación humana.

    Sale de la base, no de un archivo: es el estado vivo de la operación. Si la
    base no responde, se dice — con `connect_timeout` corto, para que una base
    caída no congele la pantalla."""
    try:
        from sentinel.db_config import get_connection
        con = get_connection()
        filas = con.execute(
            "SELECT task_name, last_run, status, result_msg, runs_total "
            "FROM scheduler_log ORDER BY last_run DESC"
        ).fetchall()
        pendientes = con.execute(
            "SELECT COUNT(*) AS n FROM validation_runs").fetchone()
        con.close()
        return [dict(f) for f in filas], str((pendientes or {}).get("n", 0))
    except Exception as e:  # noqa: BLE001
        return [], f"error:{type(e).__name__}"


def _estado_silo(silo: dict) -> tuple[bool, str]:
    """(operable, motivo). Un silo es operable si su conector existe en disco."""
    ruta = silo.get("conector")
    if not ruta:
        return False, "sin conector — no se puede despachar todavía"
    if not (_RAIZ / ruta).exists():
        return False, f"el conector declarado no está en disco ({ruta})"
    return True, ruta


def _cifras() -> dict[str, Any]:
    """Todo lo que la consola muestra, con la marca de qué pudo leerse."""
    d: dict[str, Any] = {"faltantes": []}

    mun, err = _leer("municipality_registry.json")
    if err:
        d["faltantes"].append(err)
    else:
        lista = mun.get("municipios") or []
        d["mun_total"] = len(lista)
        d["mun_provincias"] = sorted({m.get("provincia", "—") for m in lista})
        d["mun_dpe"] = sum(1 for m in lista if m.get("dpe_id_verificado") is True)
        d["mun_sin_dpe"] = sorted(m.get("canton", "—") for m in lista
                                  if not m.get("dpe_id_verificado"))

    try:
        censo = json.loads(_CENSO.read_text(encoding="utf-8"))
        d["censo_total"] = len(censo)
        d["censo_provincias"] = sorted({(g.get("provincia") or "—") for g in censo})
    except FileNotFoundError:
        d["faltantes"].append("el censo del portal no se ha corrido")
    except Exception as e:  # noqa: BLE001
        d["faltantes"].append(f"censo del portal: {type(e).__name__}")

    try:
        scan = json.loads(_SCAN.read_text(encoding="utf-8"))
        d["scan_total"] = len(scan)
        piloto = [x for x in scan
                  if _CANTON_PILOTO in f"{x.get('name','')}{x.get('name_short','')}".upper()]
        piloto.sort(key=lambda x: (0 if "GOBIERNO AUTÓNOMO" in (x.get("name") or "").upper()
                                   else 1, x.get("name") or ""))
        d["piloto"] = [{
            "nombre": _nombre_corto(x),
            "es_matriz": "GOBIERNO AUTÓNOMO" in (x.get("name") or "").upper(),
            "m2025": sorted(x.get("months_2025") or []),
            "m2026": sorted(x.get("months_2026") or []),
            "ruc": x.get("ruc"),
            "id": x.get("id"),
        } for x in piloto]
    except FileNotFoundError:
        d["faltantes"].append("el barrido mensual no se ha corrido")
    except Exception as e:  # noqa: BLE001
        d["faltantes"].append(f"barrido mensual: {type(e).__name__}")

    snap, err = _leer("gm_snapshot.json")
    if err:
        d["faltantes"].append(err)
    else:
        gad = snap.get("gad") or {}
        d["corte"] = (snap.get("_meta") or {}).get("fecha_corte")
        d["gad_nombre"] = gad.get("nombre")
        d["gad_ruc"] = gad.get("ruc")

    try:
        d["pcd"] = sorted(p.stem for p in _PCD.glob("PCD-*.md"))
    except Exception:  # noqa: BLE001
        d["pcd"] = []

    # ¿Todas las fuentes identifican al piloto con el mismo RUC? El registro ya
    # está corregido (Javo · 2026-08-06). Si el snapshot conserva otro, se
    # DECLARA: es el espejo del motor y se corrige en su origen, sobre copia y
    # con evidencia (Regla 1), nunca escribiendo hacia atrás desde una pantalla.
    try:
        reg = next(m for m in (mun or {}).get("municipios", [])
                   if _CANTON_PILOTO in (m.get("canton") or "").upper())
        portal = next((e for e in d.get("piloto") or [] if e["es_matriz"]), None)
        if portal:
            discrepan = {n: r for n, r in (("el registro", reg.get("ruc")),
                                           ("el motor", d.get("gad_ruc")))
                         if r and r != portal["ruc"]}
            if discrepan:
                d["contradiccion_ruc"] = {
                    "canton": reg.get("canton"), "discrepan": discrepan,
                    "portal": portal["ruc"], "id_portal": portal["id"],
                }
    except (StopIteration, AttributeError, TypeError):
        pass

    return d


# ══════════════════════════════════════════════════════════════════════════════
# PIEZAS
# ══════════════════════════════════════════════════════════════════════════════

def _mono() -> str:
    return "font-family:'JetBrains Mono',monospace"


def _resumen_estados():
    """Los ocho estados de captura (ADR-042 §6). La semántica vive en
    `app/observatorio/estados.py`, no aquí: esta pantalla la muestra, no la
    define."""
    from app.observatorio import resumen
    return resumen()


def _color_estado(clave: str) -> str:
    from app.observatorio import color
    return color(clave)


def _dato(valor: str, de: str, etiqueta: str, nota: str = "",
          color: str | None = None) -> str:
    """Una cifra con su denominador visible."""
    col = color or C.V_TX
    den = (f'<span style="{_mono()};font-size:13px;color:{C.V_TX3};'
           f'font-weight:500"> / {de}</span>') if de else ""
    pie = (f'<div style="font-size:9.5px;color:{C.V_TX3};margin-top:5px;'
           f'line-height:1.45">{nota}</div>') if nota else ""
    return (f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
            f'border-radius:10px;padding:13px 14px;height:100%">'
            f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;text-transform:uppercase;color:{C.V_TX3};'
            f'margin-bottom:7px">{etiqueta}</div>'
            f'<div><span style="{_mono()};font-size:26px;font-weight:900;'
            f'color:{col};letter-spacing:-.02em">{valor}</span>{den}</div>'
            f'{pie}</div>')


def _franja(titulo: str, derecha: str = "") -> str:
    return (f'<div style="display:flex;justify-content:space-between;'
            f'align-items:baseline;margin:22px 2px 9px">'
            f'<span style="font-size:10.5px;font-weight:800;letter-spacing:.1em;'
            f'color:{C.ACENTO}">▎{titulo}</span>'
            f'<span style="{_mono()};font-size:9.5px;color:{C.V_TX3}">'
            f'{derecha}</span></div>')


def _sin_dato(motivo: str) -> str:
    """Un hueco declarado. Se ve distinto de un cero — porque lo es."""
    return (f'<div style="background:transparent;border:1px dashed '
            f'{C.V_BD_FUERTE};border-radius:10px;padding:13px 14px;height:100%">'
            f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;text-transform:uppercase;color:{C.V_TX3};'
            f'margin-bottom:7px">Sin dato</div>'
            f'<div style="font-size:11px;color:{C.V_TX2};line-height:1.5">'
            f'{motivo}</div></div>')


def _rejilla_meses(publicados: list[int], hasta: int = 12) -> str:
    """Doce (o cuatro) casillas: publicado = acento, ausente = contorno vacío.

    Que un mes no esté publicado es un hecho verificable; llamarlo
    incumplimiento sería un juicio que a QUIRA no le toca emitir."""
    pub = set(publicados or [])
    casillas = []
    for m in range(1, hasta + 1):
        hay = m in pub
        casillas.append(
            f'<span title="mes {m}: '
            f'{"publicado" if hay else "sin publicación registrada"}" '
            f'style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:17px;height:17px;border-radius:3px;font-size:7.5px;'
            f'{_mono()};font-weight:700;'
            + (f'background:{C.alpha(C.ACENTO,.85)};color:{C.VOLCAN};'
               f'border:1px solid {C.ACENTO}'
               if hay else
               f'background:transparent;color:{C.V_TX3};'
               f'border:1px dashed {C.V_BD_FUERTE}')
            + f'">{_MESES[m-1]}</span>')
    return f'<span style="display:inline-flex;gap:3px">{"".join(casillas)}</span>'


def _fila_piloto(e: dict) -> str:
    """Una entidad con sus dos años."""
    n25, n26 = len(e["m2025"]), len(e["m2026"])
    etiqueta = (f'<b style="color:{C.V_TX}">{e["nombre"]}</b>'
                if e["es_matriz"] else
                f'<span style="color:{C.V_TX2}">{e["nombre"]}</span>')
    return (f'<div style="display:flex;align-items:center;gap:14px;padding:8px 0;'
            f'border-bottom:1px solid {C.V_BD}">'
            f'<div style="flex:0 0 190px;font-size:11px">{etiqueta}</div>'
            f'<div style="flex:0 0 auto">{_rejilla_meses(e["m2025"], 12)}</div>'
            f'<div style="{_mono()};font-size:10px;flex:0 0 44px;'
            f'color:{C.V_TX if n25 == 12 else C.OCRE}">{n25}/12</div>'
            f'<div style="flex:0 0 auto;opacity:.9">{_rejilla_meses(e["m2026"], 4)}</div>'
            f'<div style="{_mono()};font-size:10px;color:{C.V_TX3}">{n26}/4</div>'
            f'</div>')


def _tarjeta_silo(silo: dict, operable: bool, motivo: str) -> str:
    """Un silo con lo que alimenta y con qué se captura."""
    color = C.ACENTO if operable else C.V_TX3
    doms = "".join(
        f'<span style="display:inline-block;background:{C.alpha(color,.10)};'
        f'border:1px solid {C.alpha(color,.28)};border-radius:5px;'
        f'padding:3px 8px;margin:0 5px 5px 0;font-size:9.5px;color:{C.V_TX2}">'
        f'{x}</span>' for x in silo["dominios"])
    pie = (f'<span style="{_mono()};font-size:9px;color:{C.V_TX3}">{motivo}</span>'
           if operable else
           f'<span style="{_mono()};font-size:9px;color:{C.OCRE}">{motivo}</span>')
    return (f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
            f'border-left:3px solid {color};border-radius:10px;padding:13px 15px;'
            f'height:100%;display:flex;flex-direction:column">'
            f'<div style="display:flex;align-items:baseline;gap:8px">'
            f'<span style="font-size:12.5px;font-weight:800;color:{C.V_TX}">'
            f'{silo["nombre"]}</span>'
            f'<span style="{_mono()};font-size:8.5px;color:{C.V_TX3}">'
            f'{silo["entidad"]} · {silo["cadencia"]}</span></div>'
            f'<div style="font-size:10.5px;color:{C.V_TX2};line-height:1.55;'
            f'margin:7px 0 9px;flex:1">{silo["que"]}</div>'
            f'<div>{doms}</div><div style="margin-top:4px">{pie}</div></div>')


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Monitoreo de Fuentes — la consola de captura."""
    d = _cifras()

    st.markdown(f"""<style>
.stApp {{ background:{C.VOLCAN}!important; }}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display:none!important; }}
.main .block-container, [data-testid="stMainBlockContainer"] {{
  max-width:100%!important; padding:.7rem 1.2rem 1rem!important; }}
html, body, .stApp, .stApp * {{ font-family:'Inter',system-ui,sans-serif; }}
div[data-testid="stVerticalBlock"] {{ gap:.5rem!important; }}
</style>""", unsafe_allow_html=True)

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px">'
        f'<div style="line-height:0">{logo("marfil", 27)}</div>'
        f'<div style="border-left:1px solid {C.V_BD_FUERTE};padding-left:13px">'
        f'<div style="font-size:14px;font-weight:800;color:{C.V_TX}">'
        f'Consola de Monitoreo</div>'
        f'<div style="font-size:10.5px;color:{C.V_TX2}">Monitoreo, captura y '
        f'validación de fuentes públicas</div></div></div>',
        unsafe_allow_html=True)

    if d["faltantes"]:
        st.markdown(
            f'<div style="margin-top:12px;border:1px dashed {C.alpha(C.OCRE,.5)};'
            f'border-radius:9px;padding:10px 13px;font-size:11px;color:{C.V_TX2};'
            f'line-height:1.6"><b style="color:{C.OCRE}">No legible:</b> '
            f'{" · ".join(d["faltantes"])}. Las secciones afectadas dicen '
            f'«sin dato», no cero.</div>', unsafe_allow_html=True)

    # ── 1 · LOS SILOS ────────────────────────────────────────────────────────
    operables = [(s, *_estado_silo(s)) for s in _SILOS]
    n_ok = sum(1 for _, ok, _ in operables if ok)
    st.markdown(_franja("SILOS DE INFORMACIÓN PÚBLICA",
                        f"{n_ok} de {len(_SILOS)} con capturador · una fuente "
                        f"aporta a varios dominios y un dominio bebe de varias"),
                unsafe_allow_html=True)
    fila1 = st.columns(3, gap="small")
    fila2 = st.columns(3, gap="small")
    for col, (silo, ok, motivo) in zip(list(fila1) + list(fila2), operables):
        with col:
            st.markdown(_tarjeta_silo(silo, ok, motivo), unsafe_allow_html=True)

    # ── 2 · COBERTURA ────────────────────────────────────────────────────────
    st.markdown(_franja("COBERTURA TERRITORIAL",
                        f"universo · {_GAD_PAIS} GAD municipales"),
                unsafe_allow_html=True)
    c = st.columns(4, gap="small")
    with c[0]:
        st.markdown(_dato("1", str(_GAD_PAIS), "Con evidencia procesada",
                          f"{d.get('gad_nombre', '—')} · corte "
                          f"{d.get('corte', '—')}", C.ACENTO),
                    unsafe_allow_html=True)
    with c[1]:
        if "censo_total" in d:
            st.markdown(_dato(str(d["censo_total"]), str(_GAD_PAIS),
                              "Censados en el portal",
                              f"{' · '.join(d['censo_provincias'])}. La cobertura "
                              f"es <b>progresiva por diseño</b>: se valida el "
                              f"piloto, se estabiliza el método y recién entonces "
                              f"se amplía."),
                        unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato("El censo del portal no se ha corrido."),
                        unsafe_allow_html=True)
    with c[2]:
        if "mun_total" in d:
            n, sin = d["mun_dpe"], d["mun_sin_dpe"]
            nota = ("Con el identificador del portal se consulta su cumplimiento "
                    "mensual sin pedirle nada al municipio.")
            if sin:
                nota += f" <b style='color:{C.OCRE}'>Sin enlazar: {', '.join(sin)}</b>."
            st.markdown(_dato(str(n), str(d["mun_total"]),
                              "Consultables en el portal", nota,
                              C.ACENTO if n else C.OCRE),
                        unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato("Depende del registro de municipios."),
                        unsafe_allow_html=True)
    with c[3]:
        st.markdown(_dato(str(len([p for p in d.get("pcd", [])
                                   if not p.startswith("PCD-MN")])), "12",
                          "Dominios curados",
                          "Un dominio curado tiene sus siete capas revisadas, "
                          "del canon a la pantalla.", C.ACENTO),
                    unsafe_allow_html=True)

    cr = d.get("contradiccion_ruc")
    if cr:
        st.markdown(
            f'<div style="margin-top:9px;border-left:3px solid {C.OCRE};'
            f'background:{C.alpha(C.OCRE,.07)};border-radius:0 8px 8px 0;'
            f'padding:11px 14px;font-size:11px;color:{C.V_TX2};line-height:1.65">'
            f'<b style="color:{C.OCRE}">Contradicción entre fuentes · '
            f'{cr["canton"]}.</b> El portal publica al municipio con el RUC '
            f'<span style="{_mono()}">{cr["portal"]}</span> (entidad '
            f'<span style="{_mono()}">{cr["id_portal"]}</span>), y ese es el '
            f'válido. Sigue discrepando '
            + " · ".join(f'<b>{n}</b> (<span style="{_mono()}">{r}</span>)'
                         for n, r in cr["discrepan"].items())
            + f'. <b>Se declara y no se arregla aquí</b>: el snapshot es el '
            f'espejo del motor y sus valores se corrigen en el origen, sobre '
            f'copia y con evidencia.</div>', unsafe_allow_html=True)

    # ── 3 · LA PRIMERA PRÁCTICA ──────────────────────────────────────────────
    st.markdown(_franja("PRIMERA PRÁCTICA · CUMPLIMIENTO MES A MES",
                        "se valida el piloto antes de escalar"),
                unsafe_allow_html=True)
    piloto = d.get("piloto") or []
    if piloto:
        matriz = next((e for e in piloto if e["es_matriz"]), None)
        cab = (f'<div style="display:flex;align-items:center;gap:14px;'
               f'padding-bottom:7px">'
               f'<div style="flex:0 0 190px;{_mono()};font-size:7.5px;'
               f'font-weight:800;letter-spacing:.13em;color:{C.V_TX3}">ENTIDAD</div>'
               f'<div style="flex:0 0 auto;{_mono()};font-size:7.5px;'
               f'font-weight:800;letter-spacing:.13em;color:{C.V_TX3};'
               f'width:243px">EJERCICIO 2025</div>'
               f'<div style="flex:0 0 44px"></div>'
               f'<div style="flex:0 0 auto;{_mono()};font-size:7.5px;'
               f'font-weight:800;letter-spacing:.13em;color:{C.V_TX3}">2026</div>'
               f'</div>')
        st.markdown(
            f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
            f'border-radius:10px;padding:14px 16px">{cab}'
            f'{"".join(_fila_piloto(e) for e in piloto)}</div>',
            unsafe_allow_html=True)

        if matriz and len(matriz["m2025"]) < 12:
            adscritas = [e for e in piloto if not e["es_matriz"]]
            mejores = [e for e in adscritas
                       if len(e["m2025"]) > len(matriz["m2025"])]
            st.markdown(
                f'<div style="margin-top:10px;border-left:3px solid {C.OCRE};'
                f'background:{C.alpha(C.OCRE,.07)};border-radius:0 8px 8px 0;'
                f'padding:11px 14px;font-size:11px;color:{C.V_TX2};'
                f'line-height:1.65"><b style="color:{C.OCRE}">Lo que muestra el '
                f'piloto.</b> El portal acredita <b>{len(matriz["m2025"])} de 12 '
                f'meses</b> de 2025 para la entidad matriz, frente a '
                f'{len(mejores)} de {len(adscritas)} adscritas con más meses '
                f'acreditados. La diferencia es interna al mismo cantón y bajo la '
                f'misma obligación, así que no se explica por capacidad del '
                f'territorio. <b>Qué la explica, esta consola no lo dice</b> — eso '
                f'se resuelve en el dominio, con el documento delante.</div>',
                unsafe_allow_html=True)
    else:
        st.markdown(_sin_dato("El barrido mensual no se ha corrido para el "
                              "cantón piloto."), unsafe_allow_html=True)

    # ── 4 · CORRIDAS Y VALIDACIÓN ────────────────────────────────────────────
    st.markdown(_franja("CORRIDAS Y VALIDACIÓN HUMANA",
                        "la máquina propone · la persona acredita"),
                unsafe_allow_html=True)
    filas, pendientes = _corridas()
    cc = st.columns([2.2, 1], gap="small")
    with cc[0]:
        if filas:
            cuerpo = "".join(
                f'<div style="display:flex;gap:12px;padding:7px 0;'
                f'border-bottom:1px solid {C.V_BD};font-size:11px">'
                f'<span style="flex:0 0 130px;color:{C.V_TX}">'
                f'{f.get("task_name", "—")}</span>'
                f'<span style="{_mono()};flex:0 0 130px;color:{C.V_TX3}">'
                f'{str(f.get("last_run", "—"))[:16]}</span>'
                f'<span style="flex:1;color:{C.V_TX2}">'
                f'{f.get("result_msg", "") or "—"}</span>'
                f'<span style="{_mono()};color:{C.V_TX3}">'
                f'×{f.get("runs_total", "—")}</span></div>' for f in filas)
            st.markdown(
                f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
                f'border-radius:10px;padding:13px 15px">'
                f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
                f'letter-spacing:.13em;color:{C.V_TX3};margin-bottom:6px">'
                f'TAREAS PROGRAMADAS</div>{cuerpo}</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato(
                "No hay tareas programadas registradas"
                + (f" — {pendientes.split(':')[1]} al consultar la base."
                   if pendientes.startswith("error:") else ".")),
                unsafe_allow_html=True)
    with cc[1]:
        if pendientes.startswith("error:"):
            st.markdown(_sin_dato("La cola de validación no pudo consultarse."),
                        unsafe_allow_html=True)
        else:
            st.markdown(_dato(pendientes, "", "En cola de validación",
                              "Ninguna cifra se publica sin que una persona la "
                              "acredite contra la fuente. En cero significa que "
                              "el circuito todavía no ha corrido.",
                              C.V_TX3 if pendientes == "0" else C.OCRE),
                        unsafe_allow_html=True)

    # ── 5 · SEMÁNTICA DE ESTADOS ─────────────────────────────────────────────
    st.markdown(_franja("SEMÁNTICA DE LA CAPTURA",
                        "ADR-042 §6 · qué puede y qué no puede afirmarse"),
                unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:{C.alpha(C.ACENTO,.07)};border:1px solid '
        f'{C.alpha(C.ACENTO,.28)};border-radius:10px;padding:11px 14px;'
        f'font-size:11px;color:{C.V_TX2};line-height:1.6;margin-bottom:9px">'
        f'<b style="color:{C.ACENTO}">«No existe evidencia» no es lo mismo que '
        f'«no pude obtener evidencia» ni que «el capturador falló».</b> Si un '
        f'portal cambia su formato y el conector deja de entenderlo, eso habla '
        f'de nuestro instrumento — no del municipio. Solo dos de los ocho '
        f'estados pueden llegar a un producto publicado, y el sistema lo '
        f'verifica solo.</div>',
        unsafe_allow_html=True)
    filas_e = "".join(
        f'<div style="display:flex;align-items:center;gap:12px;padding:7px 0;'
        f'border-bottom:1px solid {C.V_BD};font-size:11px">'
        f'<span style="width:11px;height:11px;border-radius:3px;flex:0 0 auto;'
        f'background:{_color_estado(clave)}"></span>'
        f'<span style="flex:0 0 175px;color:{C.V_TX}">{s.etiqueta}</span>'
        f'<span style="flex:0 0 150px;{_mono()};font-size:9.5px;'
        f'color:{C.V_TX3}">habla de {s.habla_de}</span>'
        f'<span style="flex:0 0 96px;{_mono()};font-size:9px;'
        f'color:{C.ACENTO if s.publicable else C.V_TX3}">'
        f'{"PUBLICABLE" if s.publicable else "no publicable"}</span>'
        f'<span style="flex:1;color:{C.V_TX2};font-size:10.5px">'
        f'{s.explicacion}</span></div>'
        for clave, s in _resumen_estados())
    st.markdown(
        f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
        f'border-radius:10px;padding:13px 15px">{filas_e}</div>',
        unsafe_allow_html=True)

    st.markdown(
        f'<div style="margin-top:20px;padding-top:10px;border-top:1px solid '
        f'{C.V_BD};font-size:9.5px;color:{C.V_TX3};line-height:1.6">'
        f'Todas las cifras se cuentan de los registros al abrir esta página; '
        f'ninguna está escrita a mano. Donde un registro no se pudo leer, la '
        f'sección dice «sin dato» — la ausencia de evidencia es un resultado de '
        f'auditoría, no un valor.<br>Dylus Lab © 2026</div>',
        unsafe_allow_html=True)
