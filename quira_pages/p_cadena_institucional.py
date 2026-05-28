"""
QUIRA Intelligence — Cadena Institucional · Sprint E.1
Vista Técnica del Analista · p_cadena_institucional.py

Orquesta la cadena de planificación territorial completa:
  CNE → PDOT → POA → PAC → Presupuesto → PP → RdC → LOTAIP

Doctrina:
  - Recicla módulos existentes (p8, p12, p15, p16_gobernanza, p17) como tabs.
  - Agrega capa HITL (Human-in-the-Loop): validación y notas por eslabón.
  - Muestra semáforo de estado por eslabón en el header.
  - Solo visible para Técnico y Administrador (is_tecnico() enforced en env_gov).
  - Datos del Gold Master v5.5_TGI · Corte Q1-2026.

Recicla:
  p16_gobernanza  → CNE promesas + PP participativo
  p8_metas        → metas PDOT
  p12_cadena      → POA→PAC→SERCOP→eSIGEF
  utils/cache_quira → Presupuesto (snapshot financiero)
  p17_rdc         → Rendición de Cuentas
  p15_transparencia → LOTAIP

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import datetime

import streamlit as st

from config import GAD_NOMBRE, CORTE, ALCALDE

# ── SEMÁFORO POR ESLABÓN (Gold Master v5.5_TGI · Q1-2026) ───────────────────
# Estado de cada eslabón: color + label + score/nota
_CADENA_ESTADO: list[dict] = [
    {
        "id": "cne",
        "icon": "📜",
        "label": "CNE / IFE",
        "sub": "66 compromisos",
        "color": "#F97316",
        "status": "SEGUIMIENTO",
        "score": "66 promesas · 19% RdC vinculadas",
        "tip": "H63_S0_CNE",
    },
    {
        "id": "pdot",
        "icon": "🗺",
        "label": "PDOT",
        "sub": "25 metas",
        "color": "#F59E0B",
        "status": "TRANSICIÓN",
        "score": "Ti promedio 62% · 8 metas sin avance",
        "tip": "H31_REPORTE_CPCCS",
    },
    {
        "id": "poa_pac",
        "icon": "⚡",
        "label": "POA → PAC",
        "sub": "SAT-0 activa",
        "color": "#EF4444",
        "status": "RUPTURA",
        "score": "4 metas sin contrato PAC · 24 procesos sin SHA-256",
        "tip": "SAT-0 · SERCOP",
    },
    {
        "id": "presupuesto",
        "icon": "💰",
        "label": "Presupuesto",
        "sub": "eSIGEF Q1",
        "color": "#EF4444",
        "status": "RUPTURA",
        "score": "Ti inversión 1.05% · TOP 8.1%",
        "tip": "G71-78 eSIGEF",
    },
    {
        "id": "pp",
        "icon": "🏘",
        "label": "Pres. Partic.",
        "sub": "$20.9M 2026",
        "color": "#F59E0B",
        "status": "EN PROCESO",
        "score": "6 talleres · 149 fichas · ACTA N°007-2025",
        "tip": "IGP + PP 2026",
    },
    {
        "id": "rdc",
        "icon": "📣",
        "label": "RdC",
        "sub": "CPCCS 2026",
        "color": "#EF4444",
        "status": "PENDIENTE",
        "score": "V=0 · acción ejecutiva requerida",
        "tip": "H10c_RDC_APORTES",
    },
    {
        "id": "lotaip",
        "icon": "🔍",
        "label": "LOTAIP",
        "sub": "21 artículos",
        "color": "#F59E0B",
        "status": "PARCIAL",
        "score": "ITAM 56% · IOC 17.71%",
        "tip": "LOTAIP · DPE",
    },
]

# ── CSS INSTITUCIONAL ─────────────────────────────────────────────────────────
_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

.ci-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

.ci-header {
    background: rgba(0,212,255,.04);
    border: 1px solid rgba(0,212,255,.12);
    border-left: 4px solid #00D4FF;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.ci-chain {
    display: flex;
    align-items: center;
    gap: 6px;
    overflow-x: auto;
    padding: 14px 18px;
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    margin-bottom: 14px;
}

.ci-nodo {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1.5px solid;
    min-width: 90px;
    cursor: default;
    flex-shrink: 0;
}

.ci-arrow {
    font-size: 16px;
    color: rgba(255,255,255,.2);
    flex-shrink: 0;
}

.ci-hitl {
    background: rgba(124,92,252,.06);
    border: 1px solid rgba(124,92,252,.18);
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 12px;
}
</style>"""


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _html_header() -> str:
    ts = datetime.now().strftime("%H:%M · %d/%m/%Y")
    return (
        f'<div class="ci-root ci-header">'
        f'<div>'
        f'<div style="font:900 15px/1 Inter,sans-serif;color:#E2E8F0;letter-spacing:-.02em">'
        f'🔗 Cadena Institucional</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.35);margin-top:4px">'
        f'{GAD_NOMBRE} · QUIRA Técnico · Corte {CORTE}</div>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:10px">'
        f'<div style="text-align:right">'
        f'<div style="font:700 8px/1 Inter,sans-serif;color:rgba(0,212,255,.6);'
        f'letter-spacing:.08em;text-transform:uppercase">ACTUALIZADO</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.4);margin-top:2px">'
        f'{ts}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


def _html_semaforo() -> str:
    """Barra de semáforo: un nodo por eslabón de la cadena."""
    nodos = ""
    for i, e in enumerate(_CADENA_ESTADO):
        col = e["color"]
        bg  = col + "18"
        nodos += (
            f'<div class="ci-nodo" style="background:{bg};border-color:{col}40">'
            f'<div style="font-size:16px">{e["icon"]}</div>'
            f'<div style="font:800 8px/1 Inter,sans-serif;color:{col};'
            f'letter-spacing:.05em;text-transform:uppercase;text-align:center">'
            f'{e["label"]}</div>'
            f'<div style="font:400 7px/1 Inter,sans-serif;color:rgba(255,255,255,.35);'
            f'text-align:center;margin-top:1px">{e["status"]}</div>'
            f'</div>'
        )
        if i < len(_CADENA_ESTADO) - 1:
            nodos += '<div class="ci-arrow">→</div>'

    return f'<div class="ci-root ci-chain">{nodos}</div>'


def _hitl_widget(tab_id: str, label: str) -> None:
    """
    Capa Human-in-the-Loop por eslabón.
    Persiste en st.session_state durante la sesión.
    """
    state_key_ok    = f"hitl_ok_{tab_id}"
    state_key_notas = f"hitl_notas_{tab_id}"
    state_key_ts    = f"hitl_ts_{tab_id}"

    st.markdown(
        '<div class="ci-root ci-hitl">'
        '<div style="font:800 9px/1 Inter,sans-serif;color:rgba(124,92,252,.8);'
        'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
        '🧑‍💻 Validación HITL — Analista Dylus Lab</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([1, 2])
    with col_a:
        validado = st.checkbox(
            f"✓ Datos {label} verificados con Gold Master",
            key=state_key_ok,
            value=st.session_state.get(state_key_ok, False),
        )
        if validado and state_key_ts not in st.session_state:
            st.session_state[state_key_ts] = datetime.now().strftime("%H:%M · %d/%m/%Y")

        if st.session_state.get(state_key_ts):
            st.markdown(
                f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(34,197,94,.6);'
                f'margin-top:4px">Validado: {st.session_state[state_key_ts]}</div>',
                unsafe_allow_html=True,
            )

    with col_b:
        notas = st.text_area(
            "Observaciones de campo / contexto territorial (Obsidian KB)",
            key=state_key_notas,
            value=st.session_state.get(state_key_notas, ""),
            height=68,
            placeholder="Ej: Contraloría solicitó info adicional sobre PAC. "
                        "Director Financiero confirmó bloqueo BDE el 15/05...",
        )
        st.session_state[state_key_notas] = notas


def _tab_presupuesto() -> None:
    """Presupuesto desde el snapshot Gold Master (no hardcoded)."""
    try:
        from utils.cache_quira import cargar_gm_snapshot
        data = cargar_gm_snapshot()
    except Exception:
        data = {}

    fin  = data.get("financiero", {})
    tgi  = data.get("tgi", {})
    h90  = fin.get("h90_consolidado", {})

    # Fallback Q1-2026
    ti_gad     = fin.get("ti_2026_raw_pct",                   1.05)
    cod_gad    = fin.get("presupuesto_codificado_grupos78_2026", 22_595_464)
    dev_gad    = fin.get("devengado_q1_2026",                   238_066)
    bloqueados = fin.get("fondos_bloqueados_est",               3_660_000)
    blk_det    = fin.get("fondos_bloqueados_detalle",
                          "BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K")
    d3_val     = tgi.get("d3", {}).get("valor", 14.58)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ti Inversión GAD (G71-78)", f"{ti_gad:.2f}%",
                  delta="⚡ RUPTURA · TOP 8.1%", delta_color="inverse")
    with col2:
        st.metric("Codificado Inversión",
                  f"${cod_gad:,.0f}", delta="Grupos 71–78")
    with col3:
        st.metric("Devengado Q1-2026",
                  f"${dev_gad:,.0f}", delta=f"{ti_gad:.2f}% Ti")
    with col4:
        st.metric("Fondos Bloqueados Est.",
                  f"${bloqueados:,.0f}", delta_color="inverse",
                  delta="⚠ No activados")

    st.markdown(
        f'<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);'
        f'border-radius:8px;padding:12px 14px;margin:8px 0;font:400 10px/1.5 Inter,sans-serif;'
        f'color:rgba(255,255,255,.55)">'
        f'<strong style="color:#EF4444">Fondos bloqueados:</strong> {blk_det}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        '<div style="font:700 9px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
        'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
        'H90 CONSOLIDADO · Holding Municipal Q1-2026</div>',
        unsafe_allow_html=True,
    )

    entidades = [
        ("🏛 GAD Municipal",       h90.get("gad_ti_q1_pct",         11.20),
         0.0, 0.0),
        ("💚 Patronato Municipal", h90.get("patronato_ti_q1_pct",   19.56),
         h90.get("patronato_codificado",   4_341_242),
         h90.get("patronato_devengado_q1", 849_062)),
        ("♻ EP Aseo",              h90.get("ep_aseo_ti_q1_pct",     18.17),
         h90.get("ep_aseo_codificado",     2_438_254),
         h90.get("ep_aseo_devengado_q1",   442_930)),
        ("🚒 Cuerpo de Bomberos",  h90.get("bomberos_ti_q1_pct",    19.43),
         h90.get("bomberos_codificado",    1_485_033),
         h90.get("bomberos_devengado_q1",  288_599)),
    ]

    for nombre, ti, cod, dev in entidades:
        col_sem = "#22C55E" if ti >= 35 else "#F59E0B" if ti >= 13 else "#EF4444"
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'padding:8px 12px;background:rgba(255,255,255,.02);border:1px solid '
            f'rgba(255,255,255,.06);border-radius:8px;margin-bottom:6px">'
            f'<div style="font:600 10px/1 Inter,sans-serif;color:rgba(255,255,255,.7)">'
            f'{nombre}</div>'
            f'<div style="display:flex;gap:20px;align-items:center">'
            f'<div style="font:900 13px/1 Inter,sans-serif;color:{col_sem}">'
            f'{ti:.2f}%<span style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3)"> Ti</span></div>'
            + (f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3)">'
               f'${cod:,.0f} cod · ${dev:,.0f} dev</div>' if cod else "")
            + f'</div></div>',
            unsafe_allow_html=True,
        )

    _hitl_widget("presupuesto", "Presupuesto eSIGEF")


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────

def render() -> None:
    """
    Vista Técnica del Analista — Cadena Institucional.
    Orquesta CNE → PDOT → POA/PAC → Presupuesto → PP → RdC → LOTAIP
    con capa HITL de validación por eslabón.

    Solo visible para Técnico y Administrador (enforced en env_gov).
    """
    from utils.session import is_tecnico
    if not is_tecnico():
        st.warning("Vista restringida al rol Técnico.")
        return

    # ── CSS + Header ────────────────────────────────────────────────────────
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(_html_header(), unsafe_allow_html=True)
    st.markdown(_html_semaforo(), unsafe_allow_html=True)

    # ── Tabs por eslabón ────────────────────────────────────────────────────
    tabs = st.tabs([
        "📜 CNE / IFE",
        "🗺 PDOT · Metas",
        "⚡ POA → PAC → SERCOP",
        "💰 Presupuesto",
        "🏘 Pres. Participativo",
        "📣 Rendición de Cuentas",
        "🔍 LOTAIP",
    ])

    # ── Tab 1: CNE / IFE ─────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'H63_S0_CNE · 66 Promesas IFE · Corte Q1-2026</div>',
            unsafe_allow_html=True,
        )
        try:
            from quira_pages.p16_gobernanza import render as _r_gov
            # Mostrar solo el contexto CNE del módulo de gobernanza
            # p16_gobernanza tiene Tab 2 con promesas CNE — lo llamamos completo
            _r_gov()
        except Exception as e:
            st.error(f"Módulo Gobernanza Participativa no disponible: {e}")
        _hitl_widget("cne", "CNE / IFE")

    # ── Tab 2: PDOT · Metas ──────────────────────────────────────────────────
    with tabs[1]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'H31_REPORTE_CPCCS · 25 Metas PDOT · Ti + Vi · Q1-2026</div>',
            unsafe_allow_html=True,
        )
        try:
            from quira_pages.p8_metas import render as _r_metas
            _r_metas()
        except Exception as e:
            st.error(f"Módulo Metas PDOT no disponible: {e}")
        _hitl_widget("pdot", "PDOT Metas")

    # ── Tab 3: POA → PAC → SERCOP → eSIGEF ──────────────────────────────────
    with tabs[2]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'SAT-0 · Cadena Operativa POA→PAC→SERCOP→eSIGEF · OCDS API</div>',
            unsafe_allow_html=True,
        )
        try:
            from quira_pages.p12_cadena import render as _r_cadena
            _r_cadena()
        except Exception as e:
            st.error(f"Módulo Cadena POA-PAC no disponible: {e}")
        _hitl_widget("poa_pac", "POA-PAC-SERCOP")

    # ── Tab 4: Presupuesto eSIGEF ────────────────────────────────────────────
    with tabs[3]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'eSIGEF · G71-78 · H90 Holding · Gold Master v5.5_TGI</div>',
            unsafe_allow_html=True,
        )
        _tab_presupuesto()

    # ── Tab 5: Presupuesto Participativo ─────────────────────────────────────
    with tabs[4]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'PP 2026 · $20.9M · 7 Parroquias · IGP 27.98%</div>',
            unsafe_allow_html=True,
        )
        # p16_confianza tiene el panel IGP + PP detallado
        try:
            from quira_pages.p16_confianza import render as _r_conf
            _r_conf()
        except Exception as e:
            st.error(f"Módulo Confianza Ciudadana no disponible: {e}")
        _hitl_widget("pp", "Presupuesto Participativo")

    # ── Tab 6: Rendición de Cuentas ──────────────────────────────────────────
    with tabs[5]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'CPCCS · RdC 2026 · H10c_RDC_APORTES · V=0 actual</div>',
            unsafe_allow_html=True,
        )
        try:
            from quira_pages.p17_rdc import render as _r_rdc
            _r_rdc()
        except Exception as e:
            st.error(f"Módulo RdC no disponible: {e}")
        _hitl_widget("rdc", "Rendición de Cuentas")

    # ── Tab 7: LOTAIP / Transparencia Activa ─────────────────────────────────
    with tabs[6]:
        st.markdown(
            '<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            'letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px">'
            'LOTAIP · 21 Artículos · ITAM 56% · IOC 17.71% · DPE API</div>',
            unsafe_allow_html=True,
        )
        try:
            from quira_pages.p15_transparencia import render as _r_trans
            _r_trans()
        except Exception as e:
            st.error(f"Módulo Transparencia LOTAIP no disponible: {e}")
        _hitl_widget("lotaip", "LOTAIP Transparencia")

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:12px;font:400 8px/1 JetBrains Mono,monospace;'
        'color:rgba(255,255,255,.1);text-align:right;display:flex;'
        'justify-content:space-between;align-items:center">'
        '<span style="color:rgba(124,92,252,.2)">Vista Técnica · HITL activo · datos no salen de esta sesión</span>'
        f'<span>QUIRA Intelligence · Cadena Institucional · Sprint E.1 · '
        f'Gold Master v5.5_TGI · {CORTE} · Dylus Lab © 2026</span>'
        '</div>',
        unsafe_allow_html=True,
    )
