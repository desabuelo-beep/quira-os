"""
QUIRA Intelligence — Centro de Mando v2 NATIVO  (Sprint C · 2026-06-11)
Teatro Operacional · GAD Montecristi · Holding Municipal

POR QUÉ v2 (lección registrada en BOOT):
  El v1 renderizaba los cajones dentro de components.html (iframe) y
  navegaba con un puente postMessage → click de botones ocultos del parent.
  En Streamlit Cloud el iframe corre SANDBOX cross-origin: el puente jamás
  puede tocar la ventana principal → los cajones NUNCA navegaron en deploy.
  v2 = TODO nativo: st.container + st.button reales. Cero iframes para
  navegación. Lo que se ve es el DOM de Streamlit — no puede fallar.

SPECS DE CONTENIDO (Javo · 2026-06-11):
  Cada cajón = (a) CONCEPTO: qué ES este dominio en lenguaje humano,
  (b) número duro representativo, (c) GANCHO que invita a entrar.
  "Su info no me dice nada, es solo un número frío" → resuelto aquí.

Navegación: st.session_state["gov_module"] = mod → env_gov rutea.
Dylus Lab © 2026
"""
from __future__ import annotations

from typing import Any

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo
from utils.session import get_rol, logout

UI_VERSION = "UI v2.1 · registro volcánico · 2026-08-06"

# ══════════════════════════════════════════════════════════════════════════════
# ESCALA DE ATENCIÓN — v1.1 (2026-08-06)
# ══════════════════════════════════════════════════════════════════════════════
# El sistema visual tiene TRES atenciones y ninguna dice "bien": no hay color de
# aprobado porque QUIRA no certifica que la gestión esté bien, certifica qué se
# puede verificar. La ausencia de señal es ausencia de señal.
#
# Las claves de abajo son DATOS de los 13 dominios y por eso se conservan; lo
# que cambia es a qué traducen. Las traducciones que importan:
#   · "verde" y "normal" → ambos SIN SEÑAL. Un verde en portada era un veredicto
#     que la evidencia no sostiene — el mismo error corregido en d08.
#   · "funds" era púrpura por ser financiamiento: mezclaba CATEGORÍA con ESTADO
#     en el mismo canal. d02 está condicionado al 58%, así que su atención es
#     ocre; que sea el dominio de recursos se lee en su nombre, no en su color.
_ATENCION_DE: dict[str, str] = {
    "critico": C.CRITICO,
    "alerta":  C.OCRE,
    "funds":   C.OCRE,
    "normal":  C.SIN_SENAL,
    "verde":   C.SIN_SENAL,
    "dim":     C.V_TX3,
}


def _temp(clave: str) -> dict[str, str]:
    """Fondo, borde y color de una atención. Un tinte del 7% y un borde del 30%:
    la tarjeta se distingue por su borde, no por su fondo (la separación entre
    volcánico y superficie es de 1,17:1, deliberadamente baja)."""
    c = _ATENCION_DE.get(clave, C.SIN_SENAL)
    return {"bg": C.alpha(c, .07), "bd": C.alpha(c, .30), "c": c}


_TEMP: dict[str, dict[str, str]] = {k: _temp(k) for k in _ATENCION_DE}

# ══════════════════════════════════════════════════════════════════════════════
# 13 DOMINIOS — CONCEPTO (campo-4 ADN) + número duro + PREGUNTA (campo-6 ADN)
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_V2: list[dict[str, Any]] = [
    {
        "id": "d01", "num": "01", "nombre": "Planificación Estratégica",
        "concepto": "Instrumento rector que verifica la consistencia entre la planificación "
                    "territorial, la programación operativa, la asignación presupuestaria y la "
                    "ejecución pública.",
        "estado": "EN RUTA", "metric": "96%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicios 2025 y 2026",
        "radiografia_macro": [("METAS", "25"), ("COBERTURA", "96%"), ("ALINEACIÓN PND", "83%")],
        "gancho": "¿El cantón mantiene el rumbo hacia sus metas plurianuales, o se desvió en el camino?",
        "temp": "verde", "mod": "ods",
    },
    {
        "id": "d02", "num": "02", "nombre": "Presupuesto & Financiamiento",
        "concepto": "La capacidad del cantón de captar, mover y ejecutar recursos a "
                    "tiempo — y de apalancar capital externo sin caer en subejecución.",
        "estado": "CONDICIONADO", "metric": "58%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicio 2026 · corte Abril",
        "radiografia_macro": [("CAPTADO", "$1.87M"), ("EJECUCIÓN", "6.4%"), ("SALUD PRESUP.", "58%")],
        "gancho": "¿Con qué eficiencia y oportunidad se ejecutan los recursos frente al riesgo de subejecución?",
        "temp": "funds", "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03", "nombre": "Gobernanza del Mandato Electoral",
        "concepto": "La correspondencia entre lo que se prometió en campaña y lo que "
                    "el plan de gobierno realmente ejecuta — la palabra empeñada, medida.",
        "estado": "EN RUTA", "metric": "79.3%",
        "folio_estado": "EN LÍNEA", "periodo": "Período 2023 – 2027",
        "radiografia_macro": [("PROMESAS", "76"), ("VINCULADAS", "75"), ("FIDELIDAD", "79.3%")],
        "gancho": "¿La gestión mantiene la correspondencia con los compromisos que la ciudadanía validó en las urnas?",
        "temp": "alerta", "mod": "metas",
    },
    # d04 "Alertas Institucionales" SE RETIRA de las áreas de gestión (ADR-035 · Javo 2026-07-15):
    # no se elimina — TRANSMUTA en la Biblioteca de Reglas Normativas, y cada señal (SAT) vive en
    # el dominio que le corresponde (d02 ya publica las 3 financieras con su norma). La BRN no es
    # un dominio: no observa una capacidad del Estado, es la FUENTE de la lógica normativa. Por eso
    # ocupa la 4ª dimensión del frame (ADR-037), no una tarjeta aquí.
    {
        "id": "d05", "num": "05", "nombre": "Holding e Integración Municipal",
        "concepto": "El desempeño coordinado de las entidades adscritas del municipio "
                    "(empresas públicas, Bomberos, Patronato) — quién articula y quién "
                    "arrastra al conjunto.",
        "estado": "BAJO OBJETIVO", "metric_key": "hold_avg", "metric_suffix": "%",
        "gancho": "¿Las entidades operan articuladas, o hay piezas que arrastran al conjunto?",
        "temp": "alerta", "mod": "municipal",
    },
    {
        "id": "d06", "num": "06", "nombre": "Salud Institucional",
        "concepto": "El estado de fondo del aparato público: su capacidad de sostener "
                    "el cumplimiento de sus funciones en el tiempo, no solo cumplir hoy.",
        "estado": "BAJO UMBRAL", "metric_key": "icpi_pct", "metric_suffix": "%",
        "gancho": "¿El gobierno cumple sus funciones de forma sostenible, o hay un deterioro estructural?",
        "temp": "critico", "mod": "situacion",
    },
    {
        "id": "d07", "num": "07", "nombre": "Transparencia",
        "concepto": "La relación entre la obligación legal de publicar y la capacidad "
                    "real de sostener una gestión auditable por la ciudadanía.",
        "estado": "OBSERVADO", "metric": "21/21",
        "gancho": "¿La información pública es verificable, o hay opacidad que impide auditar la gestión?",
        "temp": "normal", "mod": "transparencia",
    },
    {
        "id": "d08", "num": "08", "nombre": "Participación Ciudadana",
        "concepto": "La incidencia real de la ciudadanía en las decisiones públicas — "
                    "no cuántos talleres hubo, sino cuánto cambiaron lo que se decidió.",
        # La métrica de portada NO es el índice del motor (48,33%): su composición no se
        # puede explicar todavía y el cajón la deja fuera por eso mismo (Regla 3). Se
        # publica lo que sí se sostiene documento a documento — la correspondencia
        # acreditada sobre lo que la ley hace exigible: 29 de 191.
        "estado": "OBSERVADO", "metric": "15%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicios 2023 - 2026",
        "radiografia_macro": [("EXIGIBLES", "191"), ("SIN ACREDITAR", "162"), ("ACREDITADO", "15%")],
        "gancho": "¿La ciudadanía incide de verdad en las decisiones, o la participación es solo formal?",
        # "alerta", no "crítico": la causa dominante de la brecha es que el instrumento no
        # localiza el gasto, no la gestión. Un rojo en portada sería un veredicto que la
        # evidencia no sostiene (Regla 2 · el cajón lo desarrolla en sus dos causas).
        "temp": "alerta", "mod": "confianza",
    },
    {
        "id": "d09", "num": "09", "nombre": "Rendición de Cuentas",
        "concepto": "Espacio de fiscalización y control social que contrasta la asignación de "
                    "recursos aprobada contra la ejecución real devengada en territorio, "
                    "garantizando el cumplimiento normativo de la rendición.",
        "estado": "CONSOLIDADO", "metric": "72.7%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicios 2023 - 2025",
        "radiografia_macro": [("VERIFICABLE", "55%"), ("SIN RESPALDO", "16%"), ("EFICACIA", "72.7%")],
        "gancho": "¿Qué parte del discurso se comprueba con registros independientes y qué queda sin respaldo público?",
        "temp": "normal", "mod": "rdc",
    },
    {
        "id": "d10", "num": "10", "nombre": "Cobertura de Servicios e Infraestructura",
        "concepto": "El acceso real a los servicios básicos visto desde el territorio: "
                    "dónde llegan las redes y dónde está el déficit estructural.",
        "estado": "BRECHA CRÍTICA", "metric": "34.9%",
        "gancho": "¿Dónde está el déficit real de servicios y a quién golpea la brecha urbano-rural?",
        "temp": "critico", "mod": "territorio",
    },
    {
        "id": "d11", "num": "11", "nombre": "Desarrollo Económico Territorial",
        "concepto": "La vitalidad económica del territorio: su capacidad de sostener "
                    "producción, empleo y cadenas de valor.",
        "estado": "EN CONSTRUCCIÓN", "metric": "—",
        "gancho": "Módulo en estructuración — empleo, industria y turismo.",
        "temp": "dim", "mod": None, "disabled": True,
    },
    {
        "id": "d12", "num": "12", "nombre": "Inclusión, Equidad y Género",
        "concepto": "La capacidad del municipio de cerrar las brechas de los grupos de "
                    "atención prioritaria, sobre todo donde la vulnerabilidad se "
                    "concentra en el territorio.",
        "estado": "CRÍTICO", "metric_key": "psg_pct", "metric_suffix": "%",
        "gancho": "¿El presupuesto de equidad es real, y dónde se concentra la brecha territorial?",
        "temp": "critico", "mod": "genero",
    },
    {
        "id": "d13", "num": "13", "nombre": "Sostenibilidad y Resiliencia Ambiental",
        "concepto": "La integridad ecológica del territorio: el equilibrio entre las "
                    "presiones sobre el ambiente y la capacidad del municipio de "
                    "conservar sus recursos y adaptarse al riesgo climático.",
        "estado": "EN CONSTRUCCIÓN", "metric": "—",
        "gancho": "¿Qué tan efectiva es la gestión pública para mitigar la "
                  "vulnerabilidad ambiental y conservar los recursos vitales del territorio?",
        "temp": "dim", "mod": None, "disabled": True,
    },
]

# Solo los DOM CURADOS son entrables; el resto queda BLOQUEADO (Javo 2026-07-14).
# d03 REABIERTO (2026-07-16): el canon fue curado y promovido — 76 promesas reales del Plan
# CNE, cero contaminación (antes: 66 con 3 de otros cantones). Las vinculaciones están
# validadas por Javo y corroboradas contra las 25 metas del universo operacional (ADR-036).
# d08 ABIERTO (2026-08-05): cajón construido sobre las tres dimensiones del catálogo d08
# v1.0.0 — integridad (7 instancias), vitalidad (declarada y reservada) y efectividad
# (223 demandas contra 1027 registros del plan operativo, con el desglose de dos causas).
_ENTRABLES = {"d01", "d02", "d03", "d08", "d09"}
for _dm in _DOMAINS_V2:
    _dm["disabled"] = _dm["id"] not in _ENTRABLES

# Las 4 DIMENSIONES del sistema (lentes · NO contenido · NUNCA duplican los 13).
# Ciclo: ¿Qué? (Gobierno) · ¿Dónde? (Territorio) · ¿Por qué? (Inteligencia) · ¿Con quién? (Convergencia).
# La ACCIÓN (¿y ahora qué?) la cierra el GOBIERNO, FUERA de QUIRA: QUIRA informa y
# conecta, no actúa (frontera · Javo 2026-06-21). El 4to = match entre QUIRAs.
# Frame universal a las 6 QUIRAs; el contenido es propio de cada una.
# ADR-037 (RATIFICADO · Javo 2026-07-16): Convergencia NO se elimina — se ABSORBE en Territorio,
# que es donde las QUIRAs se encuentran de verdad (el mapa). Su lugar lo toma la BRN: "¿bajo qué
# norma?" es la pregunta que sostiene a las otras tres (sin norma verificada no hay dato · Regla 3).
# El frame sigue siendo universal a las 6 QUIRAs. La frontera se conserva: QUIRA informa y conecta,
# no actúa.
_DIMS = [
    # "El color se gana al estar viva" (Javo · 2026-07-16) es la regla, y con un
    # solo acento se cumple mejor que con un color por lente: la que está viva
    # lleva el acento, las que no, el instrumental. Nada más las distingue porque
    # nada más hay que distinguir todavía.
    {"key": "dim_gob",    "icon": "🏛", "nombre": "Gobierno", "col": C.ACENTO,
     "desc": "¿Qué? · la institución, el mandato y sus investigaciones", "dest": "gobierno"},
    # Territorio e Inteligencia: SIN acceso hasta trabajarlas (Javo · 2026-07-17).
    {"key": "dim_terr",   "icon": "🗺", "nombre": "Territorio", "col": C.V_TX3,
     "desc": "¿Dónde? · el cantón en el mapa · el encuentro entre las QUIRAs", "dest": None, "proximamente": True},
    {"key": "dim_intel",  "icon": "◎", "nombre": "Inteligencia", "col": C.V_TX3,
     "desc": "¿Por qué? · QUIRA IA: lee, explica y anticipa", "dest": None, "proximamente": True},
    {"key": "dim_brn", "icon": "📖", "nombre": "Norma", "col": C.V_TX3,
     "desc": "¿Bajo qué norma? · la ley que sostiene cada verificación", "dest": None, "proximamente": True},
]


# Ícono alusivo por cajón — reemplaza la numeración: ningún cajón manda sobre
# otro. Con el color por dominio retirado, el ícono y el nombre son lo que los
# distingue entre sí; el color quedó libre para decir el estado.
_ICON: dict[str, str] = {
    "d01": "🧭", "d02": "💰", "d03": "📜", "d04": "🚨", "d05": "🏢",
    "d06": "🩺", "d07": "🔍", "d08": "🗳", "d09": "📣", "d10": "🗺",
    "d11": "📈", "d12": "🤝", "d13": "🌿",
}


def _esc_h(s) -> str:
    """Escape mínimo para el HTML inline de esta página."""
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _cargar_gobierno() -> dict:
    """Bloque `gobierno` del snapshot (ADR-037 · dimensión ¿QUÉ?): alcalde, mandato, concejo,
    consejo de planificación y estructura orgánica. Todo viene del canon y del corpus
    verificado vía `scripts/enrich_gobierno.py`; aquí solo se lee (Regla 1)."""
    try:
        import json
        from pathlib import Path
        p = Path(__file__).resolve().parent.parent / "data" / "gm_snapshot.json"
        return (json.loads(p.read_text(encoding="utf-8")) or {}).get("gobierno") or {}
    except Exception:  # noqa: BLE001
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# DATOS — reusa la carga del v1 (misma fuente, misma doctrina)
# ══════════════════════════════════════════════════════════════════════════════

def _data() -> dict[str, Any]:
    from quira_pages.p_command_center import _load_data
    d = _load_data()
    icpi = d.get("icpi_pct")
    n_al = int(d.get("n_alertas", 0) or 0)
    hold = d.get("hold_avg", 0.0)
    d["icpi_str"]    = f"{icpi:.1f}%" if icpi is not None else "—"
    _parcial = any(t in str(d.get("icpi_clasif", "")).lower() for t in ("parcial", "preliminar"))
    # Sin valor NO es crítico. Antes, un indicador ausente se pintaba de rojo
    # como si estuviera fuera de umbral; la falta de dato es un resultado de
    # auditoría, no un veredicto sobre la gestión (Principio Rector).
    d["icpi_color"]  = C.OCRE if _parcial else C.atencion(icpi)
    d["icpi_sub"]    = d.get('icpi_clasif', '—')
    d["alert_str"]   = str(n_al)
    d["alert_color"] = C.CRITICO if n_al > 0 else C.SIN_SENAL
    d["riesgo_str"]  = (d.get("riesgo_clasif") or "Sin alertas críticas")
    if d["riesgo_str"] in ("—", ""):
        d["riesgo_str"] = "Sin alertas críticas"
    d["hold_str"]    = f"{hold:.1f}%"
    d["hold_color"]  = C.sem(hold)
    return d


def _metric_of(dom: dict, d: dict) -> str:
    k = dom.get("metric_key")
    if k:
        v = d.get(k)
        if v is not None:
            suf = dom.get("metric_suffix", "")
            return f"{v:.1f}{suf}" if isinstance(v, float) else f"{v}{suf}"
    return dom.get("metric", "—")


def _nav(mod: str) -> None:
    st.session_state["gov_module"] = mod
    st.session_state["ejecutivo_modo"] = "vista"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# CSS GLOBAL — estética sobre componentes NATIVOS (st-key-* targeting)
# ══════════════════════════════════════════════════════════════════════════════

def _css() -> str:
    per_card = []
    for dom in _DOMAINS_V2:
        t = _TEMP[dom["temp"]]
        op = "opacity:.45;" if dom.get("disabled") else ""
        per_card.append(
            f'.st-key-card_{dom["id"]} > div[data-testid="stVerticalBlockBorderWrapper"] '
            f'{{ background:{t["bg"]}!important; border:1px solid {t["bd"]}!important; '
            f'border-left:3px solid {t["c"]}!important; border-radius:12px!important; '
            f'min-height:220px!important; transition:border-color .12s ease; {op} }}'
        )
        if True:  # ícono-entrada estilizado para las 13 (todas son investigaciones)
            # ÍCONO-entrada (Javo · 2026-06-21): el ícono alusivo ES el disparador
            # nativo de entrada — reemplaza la numeración y el botón-caja. Robusto
            # (no overlay, no enlace). Hover = el cajón se ilumina e invita a entrar.
            per_card.append(
                f'.st-key-card_{dom["id"]}:hover > div[data-testid="stVerticalBlockBorderWrapper"] '
                f'{{ border-color:{t["c"]}!important; }}'
                f'.st-key-nav_{dom["id"]} button {{ background:{t["c"]}1c!important; '
                f'border:1px solid {t["c"]}45!important; border-radius:9px!important; '
                f'font-size:17px!important; line-height:1!important; padding:0!important; '
                f'min-height:38px!important; height:38px!important; width:100%!important; '
                f'box-shadow:none!important; }}'
                f'.st-key-nav_{dom["id"]} button:hover {{ background:{t["c"]}33!important; '
                f'border-color:{t["c"]}!important; transform:translateY(-1px); }}'
            )
    for k in _DIMS:
        per_card.append(
            f'.st-key-{k["key"]} > div[data-testid="stVerticalBlockBorderWrapper"] '
            f'{{ background:{C.VOLCAN_UP}!important; '
            f'border:1px solid {C.V_BD}!important; '
            f'border-radius:12px!important; }}'
            f'.st-key-go_{k["key"]} button {{ background:transparent!important; '
            f'border:none!important; color:{C.V_TX2}!important; font-size:11px!important; '
            f'min-height:26px!important; padding:0 6px!important; }}'
            f'.st-key-go_{k["key"]} button:hover {{ color:{C.ACENTO}!important; }}'
        )
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Sidebar fuera + main full-width + fondo */
[data-testid="stSidebar"], [data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {{
  display:none!important; width:0!important; min-width:0!important;
}}
.stApp {{ background:{C.VOLCAN}!important; }}
.main .block-container, [data-testid="stMainBlockContainer"], div.block-container {{
  max-width:100%!important; padding:0.6rem 1.1rem 0.8rem!important;
}}
html, body, .stApp, .stApp * {{ font-family:'Inter',system-ui,sans-serif; }}

/* Header buttons */
.st-key-btn_salir button {{
  background:transparent!important; border:1px solid {C.V_BD_FUERTE}!important;
  color:{C.V_TX2}!important; font-size:12px!important; border-radius:9px!important;
}}
.st-key-btn_salir button:hover {{ color:{C.V_TX}!important;
  border-color:{C.alpha(C.ACENTO, .55)}!important; }}

/* Acceso al panel de operación: presente pero discreto — no compite con los
   13 dominios porque no es uno de ellos. */
.st-key-btn_panel_obs button {{
  background:transparent!important; border:1px solid {C.V_BD}!important;
  color:{C.V_TX3}!important; font-size:10px!important; border-radius:8px!important;
  min-height:28px!important; letter-spacing:.05em!important;
}}
.st-key-btn_panel_obs button:hover {{ color:{C.V_TX2}!important;
  border-color:{C.V_BD_FUERTE}!important; }}

/* Compactar gaps verticales */
div[data-testid="stVerticalBlock"] {{ gap:.45rem!important; }}

{''.join(per_card)}
</style>"""


# ══════════════════════════════════════════════════════════════════════════════
# TARJETA DE DOMINIO — función pura
# ══════════════════════════════════════════════════════════════════════════════

def cuerpo_tarjeta(dom: dict, color: str) -> str:
    """HTML del cuerpo de una tarjeta de dominio: alcance · estado · radiografía.

    Pura y sin Streamlit a propósito, para que la maqueta de revisión pueda
    construir exactamente lo que ve el usuario en vez de una copia del markup
    que envejecería aparte.

    Estructura tipo FOLIO / MEMORANDO (Javo · 2026-07-14): alcance, estado y
    radiografía de 3 indicadores macro. El detalle se descubre AL ENTRAR — la
    tarjeta no es un índice.

    Rejilla de 3 filas fijas (Javo · 2026-07-16): el alcance fluía libre y su
    largo variable empujaba ESTADO y RADIOGRAFÍA a alturas distintas en cada
    tarjeta. Con alto fijo en el alcance y la radiografía anclada al fondo, las
    tres franjas caen SIEMPRE en la misma línea, sea cual sea el texto."""
    mono = "font-family:'JetBrains Mono',monospace"
    rm   = dom.get("radiografia_macro", [])
    est  = dom.get("folio_estado", "")
    per  = dom.get("periodo", "")

    box = ""
    if rm:
        sep = f'<span style="color:{color};opacity:.55;margin:0 6px">→</span>'
        cells = sep.join(
            f'<span style="white-space:nowrap"><span style="font-size:7.5px;font-weight:800;'
            f'letter-spacing:.05em;color:{C.V_TX3}">{_esc_h(lab)}</span> '
            f'<span style="{mono};font-size:13px;font-weight:900;color:{color}">'
            f'{_esc_h(val)}</span></span>'
            for lab, val in rm)
        box = (f'<div style="{mono};font-size:7.5px;font-weight:800;letter-spacing:.1em;'
               f'text-transform:uppercase;color:{C.V_TX3};margin-top:11px;margin-bottom:5px">'
               f'Radiografía documental · métricas de consistencia</div>'
               f'<div style="border:1px solid {C.alpha(color, .27)};border-radius:6px;'
               f'padding:9px 8px;text-align:center;'
               f'background:{C.alpha(color, .05)}">{cells}</div>')

    estado_html = ""
    if est or per:
        _p = f' · {_esc_h(per)}' if per else ""
        estado_html = (f'<div style="{mono};font-size:8.5px;color:{C.V_TX3};'
                       f'margin-top:10px;letter-spacing:.02em">'
                       f'<span style="color:{color};font-weight:800">ESTADO:</span> '
                       f'<b style="color:{C.V_TX2}">{_esc_h(est)}</b>{_p}</div>')

    return (f'<div style="padding:2px 2px 0;display:flex;flex-direction:column;'
            f'min-height:196px">'
            f'<div style="height:3px;background:{color};border-radius:2px;opacity:.7;'
            f'margin-bottom:10px"></div>'
            f'<div style="{mono};font-size:8px;font-weight:800;letter-spacing:.08em;'
            f'color:{color};margin-bottom:3px">[ ALCANCE ]</div>'
            f'<div style="font-size:11px;color:{C.V_TX2};line-height:1.5;height:66px;'
            f'overflow:hidden">{_esc_h(dom["concepto"])}</div>'
            f'<div style="margin-top:auto">{estado_html}{box}</div>'
            f'</div>')


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Centro de Mando v2 — nativo, sin iframes de navegación."""
    st.markdown(_css(), unsafe_allow_html=True)
    d = _data()
    rol = get_rol() or "ejecutivo"

    # ── Header ────────────────────────────────────────────────────────────────
    # ADR-037: fuera el chip de rol ("Ejecutivo") y el botón "Preguntar a QUIRA" — si la
    # dimensión Inteligencia ES QUIRA IA, un botón aparte la duplica. El corte se lee del
    # canon (no se escribe a mano: envejece en silencio).
    _gob = _cargar_gobierno()
    _man = _gob.get("mandato") or {}
    _corte = _gob.get("corte") or "Corte Q1-2026"
    h1, h2, h3 = st.columns([6.4, 1.5, 0.9])
    with h1:
        # La MARCA, no un glifo. Antes decía "⬡ QUIRA" con un hexágono tipográfico
        # que no es el logo de nada; la Q manteña se lee del activo (`utils/marca`).
        st.markdown(
            '<div style="display:flex;align-items:center;gap:13px">'
            f'<div style="line-height:0">{logo("marfil", 30)}</div>'
            f'<span style="font:600 17px/1 Archivo,Inter,sans-serif;letter-spacing:.19em;'
            f'color:{C.V_TX}">QUIRA</span>'
            f'<div style="border-left:1px solid {C.V_BD_FUERTE};padding-left:14px">'
            f'<div style="font-size:14px;font-weight:800;color:{C.V_TX}">'
            f'Centro de Inteligencia Territorial</div>'
            f'<div style="font-size:10.5px;color:{C.V_TX2}">GAD Municipal de Montecristi · '
            f'{_esc_h(_corte)}</div></div></div>',
            unsafe_allow_html=True,
        )
    with h2:
        # Instrumental, no verde: que el sistema esté en línea es un hecho de
        # operación, no un aprobado sobre la gestión. El sistema no tiene color
        # de "bien" y este chip era el último que lo usaba.
        st.markdown(
            '<div style="text-align:right;padding-top:8px">'
            f'<span style="font:700 10px/1 \'JetBrains Mono\',monospace;color:{C.V_TX3};'
            f'border:1px solid {C.V_BD_FUERTE};border-radius:12px;letter-spacing:.08em;'
            f'padding:4px 10px;display:inline-block">● EN LÍNEA</span></div>',
            unsafe_allow_html=True,
        )
    with h3:
        if st.button("⎋ Salir", key="btn_salir", use_container_width=True):
            logout()
            st.rerun()

    # ── Subtítulo de la franja superior (ADR-037: como ÁREAS DE GESTIÓN lo tiene abajo) ──
    st.markdown(
        '<div style="display:flex;justify-content:space-between;margin:8px 2px 2px">'
        f'<span style="font-size:10.5px;font-weight:800;letter-spacing:.1em;'
        f'color:{C.ACENTO}">▎LECTURA DEL SISTEMA</span>'
        f'<span style="font-size:9.5px;color:{C.V_TX3};font-family:\'JetBrains Mono\',monospace">'
        f'qué · dónde · por qué · bajo qué norma</span></div>',
        unsafe_allow_html=True,
    )

    # ── Banda de 4 DIMENSIONES (lentes del sistema · no duplican los 13) ──────
    # Simetría (Javo): alto fijo en la descripción + pie anclado → las 4 franjas caen siempre
    # en la misma línea, sea cual sea el texto.
    # Las 4 lentes NO llevan métrica (Javo · 2026-07-16): solo nombre y conceptualización. Son
    # RECTANGULARES —más bajas que los dominios— para que se distingan de ellos a simple vista.
    # Y el ÍCONO es el acceso, igual que en las áreas de gestión: mismo gesto en todo el sistema.
    dcols = st.columns(4, gap="small")
    for col, dim in zip(dcols, _DIMS):
        with col:
            with st.container(border=True, key=dim["key"]):
                ic, nm = st.columns([0.17, 0.83], gap="small")
                with ic:
                    if dim.get("proximamente"):
                        st.markdown(f'<div style="font-size:18px;text-align:center;opacity:.4;'
                                    f'padding-top:6px" title="En preparación">{dim["icon"]}</div>',
                                    unsafe_allow_html=True)
                    elif st.button(dim["icon"], key=f"go_{dim['key']}",
                                   help=f"Entrar · {dim['nombre']}"):
                        _nav(dim["dest"])
                with nm:
                    c = dim.get("col", C.ACENTO)
                    prox = (f'<span style="font-size:8.5px;color:{C.V_TX3};margin-left:6px">'
                            f'— próximamente —</span>') if dim.get("proximamente") else ""
                    st.markdown(
                        f'<div style="padding-top:2px">'
                        f'<div style="font-size:14px;font-weight:800;color:{c}">'
                        f'{dim["nombre"]}{prox}</div>'
                        f'<div style="height:2px;width:34px;background:{c};opacity:.55;'
                        f'border-radius:1px;margin:4px 0 3px"></div>'
                        f'<div style="font-size:9.5px;color:{C.V_TX2};line-height:1.4;'
                        f'height:26px;overflow:hidden">{dim["desc"]}</div></div>',
                        unsafe_allow_html=True,
                    )

    st.markdown(
        '<div style="display:flex;justify-content:space-between;margin:4px 2px 0">'
        f'<span style="font-size:10.5px;font-weight:800;letter-spacing:.1em;'
        f'color:{C.ACENTO}">▎ÁREAS DE GESTIÓN</span>'
        f'<span style="font-size:9.5px;color:{C.V_TX3};font-family:\'JetBrains Mono\','
        f'monospace">Montecristi · clic en el ícono para entrar</span></div>',
        unsafe_allow_html=True,
    )

    # ── Grid · 12 cajones · dimensiones iguales · ÍCONO = entrada ─────────────
    # UN COLOR POR DOMINIO — retirado (2026-08-06).
    # Había 13 colores, uno por dominio (Javo · 2026-07-14, para diferenciarlos a
    # simple vista). Dos razones para retirarlo, y la segunda pesa más que la
    # estética:
    #   1 · Contradice el acento único de la identidad v1.1 — trece acentos es
    #       ninguno, y el conjunto leía como un arcoíris genérico.
    #   2 · Ocupaba el canal del color con una CATEGORÍA, y entonces el color no
    #       podía decir nada sobre el estado. Ahora el color significa ATENCIÓN:
    #       mirar la pantalla y ver dónde está el problema, que es para lo que
    #       sirve un tablero.
    # Los dominios se distinguen por ícono y por nombre, que ya los tenían.
    for fila in range(0, len(_DOMAINS_V2), 3):
        cols = st.columns(3, gap="small")
        for col, dom in zip(cols, _DOMAINS_V2[fila:fila + 3]):
            with col:
                with st.container(border=True, key=f"card_{dom['id']}"):
                    t = _TEMP[dom["temp"]]
                    color = t["c"]
                    estado = dom.get("estado", "")
                    metric = _metric_of(dom, d)
                    icono = _ICON.get(dom["id"], "◉")
                    # título: ÍCONO-entrada (disparador) + nombre
                    ic, nm = st.columns([0.17, 0.83], gap="small")
                    with ic:
                        # Las 13 abren su investigación sobre el kernel (qinv · UMI)
                        if dom.get("disabled"):
                            st.markdown('<div style="font-size:18px;text-align:center;opacity:.4;'
                                        'padding-top:6px" title="En preparación">🔒</div>',
                                        unsafe_allow_html=True)
                        elif st.button(icono, key=f"nav_{dom['id']}",
                                       help=f"Entrar · {dom['nombre']}"):
                            _nav(f"qinv_{dom['id']}")
                    with nm:
                        st.markdown(
                            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:7.5px;'
                            f'font-weight:800;letter-spacing:.14em;color:{color};padding-top:6px">DOMINIO</div>'
                            f'<div style="font-size:13px;font-weight:800;color:{C.V_TX};'
                            f'line-height:1.15;margin-top:1px">{dom["nombre"]}</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(cuerpo_tarjeta(dom, color), unsafe_allow_html=True)
                    if dom.get("disabled"):
                        st.markdown(
                            f'<div style="font-size:9.5px;color:{C.V_TX3};text-align:center;'
                            f'padding:2px 0">— en construcción —</div>',
                            unsafe_allow_html=True,
                        )

    # ── Footer + stamp de versión ─────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;margin-top:6px;'
        f'padding-top:8px;border-top:1px solid {C.V_BD}">'
        f'<span style="font-size:9.5px;color:{C.V_TX3}">● Sistema operativo · '
        f'GAD Municipal de Montecristi · Corte Q1-2026</span>'
        f'<span style="font-size:9.5px;color:{C.V_TX3}">Dylus Lab © 2026 · '
        f'QUIRA · <span style="font-family:\'JetBrains Mono\',monospace;'
        f'opacity:.75">{UI_VERSION}</span></span></div>',
        unsafe_allow_html=True,
    )

    # ── Panel del Observatorio — acceso discreto ──────────────────────────────
    # Va en el pie y no como área de gestión ni como lente: Operaciones es
    # mantenimiento del ecosistema, NO producto (ADR-041 §2). Ponerlo entre los
    # 13 dominios lo convertiría en uno, que es justo lo que el ADR niega.
    _, col_panel, _ = st.columns([3.4, 1.2, 3.4])
    with col_panel:
        if st.button("◷ Estado de la operación", key="btn_panel_obs",
                     use_container_width=True,
                     help="Panel del Observatorio — qué hay capturado, qué falta "
                          "y qué se debe. Uso interno del equipo."):
            _nav("panel_obs")
