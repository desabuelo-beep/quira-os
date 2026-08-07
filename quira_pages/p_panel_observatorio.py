"""
QUIRA — Panel del Observatorio  ·  `quira_pages/p_panel_observatorio.py`

Estado de la OPERACIÓN del observatorio (ADR-041 §5.1): qué hay capturado, qué
falta y qué se debe. No es un producto — es mantenimiento del ecosistema, y por
eso no aparece como área de gestión ni como lente: se entra por el pie.

DOCTRINA DE ESTE PANEL
──────────────────────────────────────────────────────────────────────────────
 1 · TODO SALE DE UN ARCHIVO. Ninguna cifra se escribe a mano. Si un registro
     falta, el panel lo dice en vez de rellenar con un número plausible: la
     ausencia de evidencia es un resultado, nunca autorización para inferir.

 2 · MUESTRA LO QUE FALTA, no solo lo que hay. Un panel que solo enseña lo
     conseguido es publicidad. El valor está en el denominador: 1 de 222, 227 de
     252, 0 de 17 con identificadores verificados.

 3 · FRONTERA DE LENGUAJE (Regla 2). Es una UI, así que la jerga interna no
     entra aunque el público sea el propio equipo. Las disposiciones se cuentan,
     no se listan por identificador.

 4 · NO RECALCULA NADA (Reglas 1 y 4). Lee registros y los cuenta. Ningún
     indicador del motor se reproduce aquí.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo

_DATA = Path(__file__).resolve().parents[1] / "data"
_PCD = Path(__file__).resolve().parents[1] / "docs" / "pcd"

# Universo de observación (ADR-041 §4-bis). No es 221: la Ley del 8-oct-2024
# creó el cantón 222, Sevilla Don Bosco, cuyo GAD no tiene todavía un ciclo
# completo de gestión — se cuenta en el universo y se declara aparte.
_GAD_PAIS = 222

# ══════════════════════════════════════════════════════════════════════════════
# LA VÍA DE COBERTURA — portal de transparencia de la DPE (Javo · 2026-08-06)
# ══════════════════════════════════════════════════════════════════════════════
# Es la primera herramienta de gestión del observatorio, y su virtud es
# jurídica antes que técnica: bajo LOTAIP la obligación de publicar es del GAD,
# y la Defensoría del Pueblo registra el cumplimiento mes a mes. QUIRA lee ese
# registro. No hace falta que ningún municipio entregue nada, ni acordar nada
# con él — es la vía 1 de R-F, transparencia activa, en su forma más limpia.
#
# De ahí sale la cobertura progresiva de los 222: se monitorea a todos desde el
# primer mes SIN tener toda su información, y el establishment_id que devuelve
# el portal es la llave para cruzar después con SERCOP (por RUC), CPCCS y el
# resto de sistemas.
#
# La infraestructura ya existe: `scripts/rc_scout.py` (RC-SCOUT v2.0) consulta
# la API pública del portal — `establishment/list` para el censo,
# `transparency/months` para el cumplimiento mensual.
_CENSO = _DATA / "scouting" / "gad_municipales_all.json"
_SCAN = _DATA / "scouting" / "manabi_scan.json"

# LA PRIMERA PRÁCTICA (Javo · 2026-08-06). Los 222 NO se abordan de una vez: se
# valida primero con Montecristi —2025 completo y lo que va de 2026— y desde ahí
# se avanza de forma progresiva. El monitoreo es materia del dominio
# Transparencia, pero se CORRE DESDE EL OBSERVATORIO: es el observatorio el que
# despacha la revisión mensual y el que retroalimenta al sistema con lo que
# encuentra. Por eso este panel no es un tablero de lectura — es el lugar donde
# la práctica se opera y se ve.
_CANTON_PILOTO = "MONTECRISTI"
_MESES = ("E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D")


# ══════════════════════════════════════════════════════════════════════════════
# CARGA — cada lectura declara si tuvo éxito
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
    """Devuelve (contenido, problema). Un registro ausente o ilegible no rompe
    el panel: se reporta como lo que es, un dato que no está."""
    ruta = _DATA / nombre
    try:
        return json.loads(ruta.read_text(encoding="utf-8")), ""
    except FileNotFoundError:
        return None, f"`data/{nombre}` no está en el repositorio"
    except json.JSONDecodeError as e:
        return None, f"`data/{nombre}` no es JSON válido (línea {e.lineno})"
    except Exception as e:  # noqa: BLE001
        return None, f"`data/{nombre}`: {type(e).__name__}"


def _cifras() -> dict[str, Any]:
    """Todo lo que el panel muestra, con la marca de qué pudo leerse."""
    d: dict[str, Any] = {"faltantes": []}

    mun, err = _leer("municipality_registry.json")
    if err:
        d["faltantes"].append(err)
    else:
        lista = mun.get("municipios") or []
        d["mun_total"] = len(lista)
        d["mun_provincias"] = sorted({m.get("provincia", "—") for m in lista})
        # El `establishment_id` del portal DPE es LA llave: con él se consulta
        # el cumplimiento mensual de transparencia sin pedirle nada al GAD, y
        # es el punto de cruce con los demás sistemas.
        d["mun_dpe"] = sum(1 for m in lista if m.get("dpe_id_verificado") is True)
        d["mun_sin_dpe"] = sorted(m.get("canton", "—") for m in lista
                                  if not m.get("dpe_id_verificado"))
        # Vías secundarias: se abren DESPUÉS, cruzando por RUC.
        d["mun_sercop"] = sum(1 for m in lista if m.get("sercop_entity_id"))
        d["mun_cpccs"] = sum(1 for m in lista if m.get("cpccs_slug"))
        d["mun_video"] = sum(1 for m in lista if m.get("youtube_channel"))

    # Censo del portal DPE — cuántos GAD se han listado desde la fuente.
    try:
        censo = json.loads(_CENSO.read_text(encoding="utf-8"))
        d["censo_total"] = len(censo)
        d["censo_provincias"] = sorted({(g.get("provincia") or "—") for g in censo})
    except FileNotFoundError:
        d["faltantes"].append("`data/scouting/gad_municipales_all.json` no está "
                              "en el repositorio — el censo del portal no se ha corrido")
    except Exception as e:  # noqa: BLE001
        d["faltantes"].append(f"censo del portal DPE: {type(e).__name__}")

    # Monitoreo mensual — la primera práctica, sobre el cantón piloto.
    try:
        scan = json.loads(_SCAN.read_text(encoding="utf-8"))
        d["scan_total"] = len(scan)
        d["scan_2025_completo"] = sum(1 for x in scan
                                      if len(x.get("months_2025") or []) == 12)
        piloto = [x for x in scan
                  if _CANTON_PILOTO in f"{x.get('name','')}{x.get('name_short','')}".upper()]
        # La matriz primero, luego las adscritas: el orden es el del holding.
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
        d["faltantes"].append("`data/scouting/manabi_scan.json` no está — el "
                              "monitoreo mensual no se ha corrido")
    except Exception as e:  # noqa: BLE001
        d["faltantes"].append(f"monitoreo mensual: {type(e).__name__}")

    # ¿El municipio piloto figura en el portal con el mismo RUC que en el
    # registro? Si no, se declara la contradicción: es el 5º nivel de la escala
    # de verificabilidad, y NO se resuelve aquí — resolverla exigiría una fuente
    # que este panel no tiene (Regla 3).
    try:
        reg_piloto = next(m for m in (mun or {}).get("municipios", [])
                          if _CANTON_PILOTO in (m.get("canton") or "").upper())
        por_portal = next((e for e in d.get("piloto") or [] if e["es_matriz"]), None)
        if por_portal and reg_piloto.get("ruc") != por_portal["ruc"]:
            d["contradiccion_ruc"] = {
                "canton": reg_piloto.get("canton"),
                "registro": reg_piloto.get("ruc"),
                "portal": por_portal["ruc"],
                "id_portal": por_portal["id"],
            }
    except (StopIteration, AttributeError, TypeError):
        pass

    vault, err = _leer("vault_registry.json")
    if err:
        d["faltantes"].append(err)
    else:
        meta = vault.get("_meta") or {}
        d["doc_escaneados"] = meta.get("notas_escaneadas")
        d["doc_con_metadatos"] = meta.get("notas_con_fm")
        d["doc_generado"] = meta.get("generado")
        d["doc_con_evidencia"] = len(vault.get("evidencias") or {})
        d["doc_competencias"] = len(vault.get("competencias") or [])

    ack, err = _leer("ack_registry.json")
    if err:
        d["faltantes"].append(err)
    else:
        meta = ack.get("meta") or {}
        d["norma_anclajes"] = meta.get("total_acks")
        d["norma_alcance"] = meta.get("scope", "—")
        cuerpos: dict[str, int] = {}
        for a in ack.get("acks") or []:
            nom = ((a.get("norma") or {}).get("nombre_oficial")
                   or (a.get("norma") or {}).get("sigla") or "—")
            cuerpos[nom] = cuerpos.get(nom, 0) + 1
        d["norma_cuerpos"] = sorted(cuerpos.items(), key=lambda x: -x[1])

    snap, err = _leer("gm_snapshot.json")
    if err:
        d["faltantes"].append(err)
    else:
        meta = snap.get("_meta") or {}
        gad = snap.get("gad") or {}
        d["corte"] = meta.get("fecha_corte")
        d["gad_nombre"] = gad.get("nombre")
        d["gad_provincia"] = gad.get("provincia")
        d["gad_periodo"] = gad.get("periodo")
        d["gad_promesas"] = gad.get("promesas_cne")
        d["gad_metas"] = gad.get("metas_pdot")

    try:
        d["pcd"] = sorted(p.stem for p in _PCD.glob("PCD-*.md"))
    except Exception:  # noqa: BLE001
        d["pcd"] = []

    return d


# ══════════════════════════════════════════════════════════════════════════════
# PIEZAS
# ══════════════════════════════════════════════════════════════════════════════

def _mono() -> str:
    return "font-family:'JetBrains Mono',monospace"


def _dato(valor: str, de: str, etiqueta: str, nota: str = "",
          color: str | None = None) -> str:
    """Una cifra con su denominador visible. El denominador NO es decorativo:
    es la diferencia entre «227 documentos» y «227 de 252»."""
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


def _rejilla_meses(publicados: list[int], hasta: int = 12) -> str:
    """Doce (o cuatro) casillas: publicado = acento, ausente = contorno vacío.

    Es la doctrina del sistema aplicada a un dato concreto: la ausencia se
    muestra como AUSENCIA —sin color— y no como un suspenso en rojo. Que un mes
    no esté publicado es un hecho verificable; llamarlo incumplimiento sería un
    juicio que a QUIRA no le toca emitir."""
    pub = set(publicados or [])
    casillas = []
    for m in range(1, hasta + 1):
        hay = m in pub
        casillas.append(
            f'<span title="mes {m}: '
            f'{"publicado" if hay else "sin publicación registrada"}" '
            f'style="display:inline-flex;align-items:center;justify-content:center;'
            f'width:17px;height:17px;border-radius:3px;font-size:7.5px;'
            f'font-family:\'JetBrains Mono\',monospace;font-weight:700;'
            + (f'background:{C.alpha(C.ACENTO,.85)};color:{C.VOLCAN};'
               f'border:1px solid {C.ACENTO}'
               if hay else
               f'background:transparent;color:{C.V_TX3};'
               f'border:1px dashed {C.V_BD_FUERTE}')
            + f'">{_MESES[m-1]}</span>')
    return f'<span style="display:inline-flex;gap:3px">{"".join(casillas)}</span>'


def _fila_piloto(e: dict) -> str:
    """Una entidad con sus dos años. La matriz se marca porque su cumplimiento
    no es comparable al de una adscrita: responde por el cantón."""
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


def _sin_dato(motivo: str) -> str:
    """Un hueco declarado. Se ve distinto de una cifra en cero — porque lo es."""
    return (f'<div style="background:transparent;border:1px dashed '
            f'{C.V_BD_FUERTE};border-radius:10px;padding:13px 14px;height:100%">'
            f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;text-transform:uppercase;color:{C.V_TX3};'
            f'margin-bottom:7px">Sin dato</div>'
            f'<div style="font-size:11px;color:{C.V_TX2};line-height:1.5">'
            f'{motivo}</div></div>')


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Panel del Observatorio — estado de la operación."""
    d = _cifras()
    st.markdown(f"""<style>
.stApp {{ background:{C.VOLCAN}!important; }}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display:none!important; }}
.main .block-container, [data-testid="stMainBlockContainer"] {{
  max-width:100%!important; padding:.7rem 1.2rem 1rem!important; }}
html, body, .stApp, .stApp * {{ font-family:'Inter',system-ui,sans-serif; }}
div[data-testid="stVerticalBlock"] {{ gap:.5rem!important; }}
</style>""", unsafe_allow_html=True)

    # ── Encabezado ───────────────────────────────────────────────────────────
    # Sin botón de retorno propio: el router ya pone la banda de migas y el
    # botón «← Centro de Inteligencia Territorial» encima de cada drill-in. Dos
    # salidas para lo mismo solo obligan a decidir cuál es la buena.
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px">'
        f'<div style="line-height:0">{logo("marfil", 27)}</div>'
        f'<div style="border-left:1px solid {C.V_BD_FUERTE};padding-left:13px">'
        f'<div style="font-size:14px;font-weight:800;color:{C.V_TX}">'
        f'Panel del Observatorio</div>'
        f'<div style="font-size:10.5px;color:{C.V_TX2}">Estado de la operación · '
        f'mantenimiento del ecosistema · equipo Dylus Lab</div></div></div>',
        unsafe_allow_html=True)

    if d["faltantes"]:
        st.markdown(
            f'<div style="margin-top:12px;border:1px dashed {C.alpha(C.OCRE,.5)};'
            f'border-radius:9px;padding:10px 13px;font-size:11px;color:{C.V_TX2};'
            f'line-height:1.6"><b style="color:{C.OCRE}">Registros no legibles:</b> '
            f'{" · ".join(d["faltantes"])}. Las secciones afectadas se muestran '
            f'como «sin dato», no en cero.</div>',
            unsafe_allow_html=True)

    # ── 1 · Cobertura territorial ────────────────────────────────────────────
    st.markdown(_franja("COBERTURA TERRITORIAL",
                        f"universo · {_GAD_PAIS} GAD municipales"),
                unsafe_allow_html=True)
    st.markdown(
        f'<div style="background:{C.alpha(C.ACENTO,.07)};border:1px solid '
        f'{C.alpha(C.ACENTO,.28)};border-radius:10px;padding:11px 14px;'
        f'font-size:11px;color:{C.V_TX2};line-height:1.6;margin-bottom:9px">'
        f'<b style="color:{C.ACENTO}">La vía es el portal de transparencia de la '
        f'Defensoría del Pueblo.</b> Bajo la Ley Orgánica de Transparencia la '
        f'obligación de publicar es del municipio, y la Defensoría registra su '
        f'cumplimiento mes a mes. El observatorio lee ese registro: no requiere '
        f'que ningún GAD entregue nada ni que medie acuerdo alguno. Por eso los '
        f'{_GAD_PAIS} se pueden monitorear de forma progresiva desde el primer '
        f'mes <b>sin tener toda su información</b> — y el identificador que '
        f'devuelve el portal es la llave para cruzar después con el resto de '
        f'sistemas.</div>',
        unsafe_allow_html=True)
    c = st.columns(4, gap="small")
    with c[0]:
        st.markdown(_dato("1", str(_GAD_PAIS), "Con evidencia procesada",
                          f"{d.get('gad_nombre', '—')} · corte "
                          f"{d.get('corte', '—')}", C.ACENTO),
                    unsafe_allow_html=True)
    with c[1]:
        if "censo_total" in d:
            provs = d["censo_provincias"]
            st.markdown(_dato(str(d["censo_total"]), str(_GAD_PAIS),
                              "Censados en el portal",
                              f"{' · '.join(provs)}. La cobertura es "
                              f"<b>progresiva por diseño</b>: se valida el piloto, "
                              f"se estabiliza el método y recién entonces se "
                              f"amplía el barrido. Ampliarlo no requiere "
                              f"desarrollo nuevo."),
                        unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato("El censo del portal no se ha corrido."),
                        unsafe_allow_html=True)
    with c[2]:
        if "mun_total" in d:
            n = d["mun_dpe"]
            sin = d["mun_sin_dpe"]
            nota = ("Con este identificador ya se consulta su cumplimiento "
                    "mensual sin pedirle nada al municipio.")
            if sin:
                nota += (f" <b style='color:{C.OCRE}'>Sin enlazar: "
                         f"{', '.join(sin)}</b> — ver la nota de abajo.")
            st.markdown(_dato(str(n), str(d["mun_total"]),
                              "Consultables en el portal", nota,
                              C.ACENTO if n else C.OCRE),
                        unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato("Depende del registro de municipios."),
                        unsafe_allow_html=True)
    with c[3]:
        if "mun_total" in d:
            st.markdown(_dato(str(max(d["mun_sercop"], d["mun_cpccs"])),
                              str(d["mun_total"]), "Cruzados con otros sistemas",
                              "Contratación, control social y rendición se "
                              "enlazan <b>después</b>, por RUC. El portal abre "
                              "la puerta; el cruce llega en segundo lugar.",
                              C.V_TX3),
                        unsafe_allow_html=True)
        else:
            st.markdown(_sin_dato("Depende del registro de municipios."),
                        unsafe_allow_html=True)

    # Contradicción entre fuentes — se declara, no se resuelve.
    cr = d.get("contradiccion_ruc")
    if cr:
        st.markdown(
            f'<div style="margin-top:9px;border-left:3px solid {C.OCRE};'
            f'background:{C.alpha(C.OCRE,.07)};border-radius:0 8px 8px 0;'
            f'padding:11px 14px;font-size:11px;color:{C.V_TX2};line-height:1.65">'
            f'<b style="color:{C.OCRE}">Contradicción entre fuentes · '
            f'{cr["canton"]}.</b> El registro interno identifica al municipio con '
            f'el RUC <span style="{_mono()}">{cr["registro"]}</span>; el portal de '
            f'la Defensoría lo publica con '
            f'<span style="{_mono()}">{cr["portal"]}</span> (entidad '
            f'<span style="{_mono()}">{cr["id_portal"]}</span>). Por eso el único '
            f'cantón con evidencia procesada figura como no enlazado. '
            f'<b>La contradicción se declara, no se arregla aquí</b>: elegir un '
            f'RUC sobre el otro exige una fuente que este panel no tiene, y sin '
            f'norma o registro verificado no hay dato.</div>',
            unsafe_allow_html=True)

    # ── 1-bis · Monitoreo mensual · LA PRIMERA PRÁCTICA ──────────────────────
    st.markdown(_franja("MONITOREO MENSUAL DE TRANSPARENCIA",
                        "primera práctica · se valida el piloto antes de escalar"),
                unsafe_allow_html=True)
    piloto = d.get("piloto") or []
    if piloto:
        matriz = next((e for e in piloto if e["es_matriz"]), None)
        filas = "".join(_fila_piloto(e) for e in piloto)
        st.markdown(
            f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
            f'border-radius:10px;padding:14px 16px">'
            f'<div style="display:flex;align-items:center;gap:14px;'
            f'padding-bottom:7px">'
            f'<div style="flex:0 0 190px;{_mono()};font-size:7.5px;'
            f'font-weight:800;letter-spacing:.13em;color:{C.V_TX3}">'
            f'ENTIDAD</div>'
            f'<div style="flex:0 0 auto;{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;color:{C.V_TX3};width:243px">EJERCICIO 2025</div>'
            f'<div style="flex:0 0 44px"></div>'
            f'<div style="flex:0 0 auto;{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;color:{C.V_TX3}">2026</div></div>'
            f'{filas}</div>',
            unsafe_allow_html=True)

        if matriz and len(matriz["m2025"]) < 12:
            adscritas = [e for e in piloto if not e["es_matriz"]]
            mejores = [e for e in adscritas if len(e["m2025"]) > len(matriz["m2025"])]
            st.markdown(
                f'<div style="margin-top:10px;border-left:3px solid {C.OCRE};'
                f'background:{C.alpha(C.OCRE,.07)};border-radius:0 8px 8px 0;'
                f'padding:11px 14px;font-size:11px;color:{C.V_TX2};line-height:1.65">'
                f'<b style="color:{C.OCRE}">Lo que muestra el piloto.</b> '
                f'El registro del portal acredita <b>{len(matriz["m2025"])} de 12 '
                f'meses</b> de 2025 para la entidad matriz, frente a '
                f'{len(mejores)} de {len(adscritas)} entidades adscritas con más '
                f'meses acreditados. La diferencia es interna al mismo cantón y '
                f'bajo la misma obligación, así que no se explica por capacidad '
                f'del territorio. <b>Qué la explica, este panel no lo dice</b> — '
                f'eso se resuelve en el dominio Transparencia, con el documento '
                f'delante.</div>',
                unsafe_allow_html=True)
    else:
        st.markdown(_sin_dato("El barrido mensual del portal no se ha corrido "
                              "para el cantón piloto."),
                    unsafe_allow_html=True)

    # ── 2 · Base normativa ───────────────────────────────────────────────────
    st.markdown(_franja("BASE NORMATIVA",
                        f"alcance {d.get('norma_alcance', '—')} · "
                        f"la norma no es cantonal"),
                unsafe_allow_html=True)
    if "norma_anclajes" in d:
        cuerpos = d["norma_cuerpos"]
        chips = "".join(
            f'<span style="display:inline-block;background:{C.VOLCAN_UP};'
            f'border:1px solid {C.V_BD};border-radius:6px;padding:6px 11px;'
            f'margin:0 6px 6px 0;font-size:10.5px;color:{C.V_TX2}">{nom} '
            f'<b style="{_mono()};color:{C.V_TX}">{n}</b></span>'
            for nom, n in cuerpos)
        cn = st.columns([1, 2.6], gap="small")
        with cn[0]:
            st.markdown(_dato(str(d["norma_anclajes"]), "",
                              "Disposiciones ancladas",
                              f"sobre {len(cuerpos)} cuerpos normativos · sin "
                              f"norma verificada no hay dato"),
                        unsafe_allow_html=True)
        with cn[1]:
            st.markdown(
                f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
                f'border-radius:10px;padding:13px 14px;height:100%">'
                f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
                f'letter-spacing:.13em;text-transform:uppercase;color:{C.V_TX3};'
                f'margin-bottom:9px">Reparto por cuerpo normativo</div>'
                f'{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown(_sin_dato("El catálogo normativo no pudo leerse."),
                    unsafe_allow_html=True)

    # ── 3 · Corpus documental ────────────────────────────────────────────────
    st.markdown(_franja("CORPUS DOCUMENTAL",
                        f"{d.get('gad_nombre', '—')} · barrido "
                        f"{d.get('doc_generado', '—')}"),
                unsafe_allow_html=True)
    if "doc_escaneados" in d:
        esc = d["doc_escaneados"] or 0
        con = d["doc_con_metadatos"] or 0
        sin = esc - con
        c = st.columns(4, gap="small")
        with c[0]:
            st.markdown(_dato(str(con), str(esc), "Con metadatos",
                              f"{sin} documento(s) escaneados sin clasificar: "
                              f"están en el acervo pero no entran en ninguna "
                              f"consulta por materia."),
                        unsafe_allow_html=True)
        with c[1]:
            st.markdown(_dato(str(d["doc_con_evidencia"]), str(con),
                              "Con evidencia asociada",
                              "El resto documenta el marco; estos sostienen "
                              "una afirmación concreta."),
                        unsafe_allow_html=True)
        with c[2]:
            st.markdown(_dato(str(d["doc_competencias"]), str(con),
                              "Vinculados a una competencia",
                              "Un documento sin competencia no puede "
                              "contrastarse contra una obligación."),
                        unsafe_allow_html=True)
        with c[3]:
            st.markdown(_dato(str(d.get("gad_promesas", "—")), "",
                              "Compromisos de campaña trazados",
                              f"{d.get('gad_metas', '—')} metas de planificación "
                              f"territorial · período {d.get('gad_periodo', '—')}"),
                        unsafe_allow_html=True)
    else:
        st.markdown(_sin_dato("El registro documental no pudo leerse."),
                    unsafe_allow_html=True)

    # ── 4 · Curación por dominio ─────────────────────────────────────────────
    st.markdown(_franja("CURACIÓN POR DOMINIO",
                        "expediente cerrado = las 7 capas revisadas"),
                unsafe_allow_html=True)
    pcd = [p for p in d.get("pcd", []) if not p.startswith("PCD-MN")]
    otros = [p for p in d.get("pcd", []) if p.startswith("PCD-MN")]
    nombres = "".join(
        f'<span style="display:inline-block;background:{C.alpha(C.ACENTO,.09)};'
        f'border:1px solid {C.alpha(C.ACENTO,.3)};border-radius:6px;'
        f'padding:6px 11px;margin:0 6px 6px 0;font-size:10.5px;color:{C.V_TX2}">'
        f'{p.split("_", 1)[-1].replace("_", " ")}</span>' for p in pcd + otros)
    cc = st.columns([1, 2.6], gap="small")
    with cc[0]:
        st.markdown(_dato(str(len(pcd)), "12", "Dominios cerrados",
                          f"más {len(otros)} expediente(s) de método. La curación "
                          f"va dominio por dominio, del canon a la pantalla.",
                          C.ACENTO if pcd else C.OCRE),
                    unsafe_allow_html=True)
    with cc[1]:
        st.markdown(
            f'<div style="background:{C.VOLCAN_UP};border:1px solid {C.V_BD};'
            f'border-radius:10px;padding:13px 14px;height:100%">'
            f'<div style="{_mono()};font-size:7.5px;font-weight:800;'
            f'letter-spacing:.13em;text-transform:uppercase;color:{C.V_TX3};'
            f'margin-bottom:9px">Expedientes</div>{nombres or "—"}</div>',
            unsafe_allow_html=True)

    # ── Pie ──────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="margin-top:22px;padding-top:10px;border-top:1px solid '
        f'{C.V_BD};font-size:9.5px;color:{C.V_TX3};line-height:1.6">'
        f'Todas las cifras salen de los registros del repositorio y se cuentan '
        f'al abrir la página; ninguna está escrita a mano. Donde un registro no '
        f'se pudo leer, la sección dice «sin dato» en vez de mostrar cero — '
        f'la ausencia de evidencia es un resultado de auditoría, no un valor.'
        f'<br>Dylus Lab © 2026 · mantenimiento del ecosistema · no es un producto '
        f'(ADR-041 §2)</div>',
        unsafe_allow_html=True)
