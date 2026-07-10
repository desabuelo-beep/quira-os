"""
QUIRA OS v0.1 — P-17 Rendición de Cuentas
RDC 2026 · CPCCS · Checklist preparación · Timeline · Circuito C-RDC
Dylus Lab © 2026

Wired: app/connectors/neo4j_crdc.py → Circuito convergente vivo (6 nodos)
       Neo4j AuraDB si está activo, fallback embebido si está pausado.
Bloomberg: solo lenguaje de gobernanza en UI. Nodo IDs / circuito ID: internos.
"""
import logging

import streamlit as st

from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

logger = logging.getLogger(__name__)

# ── CONECTOR C-RDC ─────────────────────────────────────────────────────────────
try:
    from app.connectors.neo4j_crdc import get_crdc_state
    _CRDC_AVAILABLE = True
except ImportError:
    _CRDC_AVAILABLE = False
    logger.warning("neo4j_crdc no disponible — bloque C-RDC omitido en p17")

# ── CHECKLIST RDC 2026 ────────────────────────────────────────────────────────
CHECKLIST_RDC = [
    # (categoría, item, ok, urgente)
    ("Normativa",     "Resolución de convocatoria publicada 30 días antes",          False, True),
    ("Normativa",     "Informe de gestión aprobado por Alcaldía",                    False, True),
    ("Normativa",     "Convocatoria ampliada · mínimo 2 sesiones públicas",          False, True),
    ("Financiero",    "Estado de ejecución presupuestaria actualizado al Q2-2026",   False, True),
    ("Financiero",    "Salud presupuestaria regularizada ≥ 25% (avance) antes de RDC",               False, True),
    ("Financiero",    "Informe deuda y coactivas con plan de pago",                  False, False),
    ("PDOT",          "Avance de metas PDOT 2023-2027 con indicadores verificables", False, True),
    ("PDOT",          "4 metas con alerta regularizadas (PAC + SHA-256)",                 False, True),
    ("PDOT",          "Fidelidad actualizada · 48/66 promesas con estado Q2",            True,  False),
    ("Participación", "7/7 parroquias con asamblea previa a RDC",                    False, True),
    ("Participación", "Actas firmadas y digitalizadas · Isabel Muentes + Aníbal SA", False, True),
    ("Participación", "Presupuesto participativo rendido por parroquia",              False, False),
    ("Transparencia", "21 artículos LOTAIP completos y actualizados",                False, True),
    ("Transparencia", "Opacidad informativa < 10% (actual 17.71%)",               False, False),
    ("Transparencia", "Estadísticas quejas/denuncias publicadas (Art. 7r)",          False, False),
    ("Género",        "Presupuesto de género ≥ 20% documentado y certificado (actual 12.83%)",         False, False),
    ("Género",        "Plan género aprobado · Patronato alineado",                   False, False),
    ("Holding",       "Informes EP Aseo, Bomberos, Patronato consolidados",          True,  False),
    ("Holding",       "Score holding ≥ 65% con evidencias por entidad",              False, False),
    ("CPCCS",         "Nota CPCCS previa a RDC · mínimo V=1 en proceso",            False, True),
]

_FASES = [
    {
        "fase": "FASE 1 · Preparación",
        "periodo": "Mayo–Junio 2026",
        "color": "amber",
        "hitos": [
            "Regularizar alertas: 4 metas PAC + 24 SHA-256",
            "Convocar asambleas Isabel Muentes y Aníbal San Andrés",
            "Publicar 4 artículos LOTAIP faltantes",
            "Actualizar informe gestión con indicadores PDOT",
        ],
    },
    {
        "fase": "FASE 2 · Convocatoria",
        "periodo": "Julio 2026",
        "color": "cyan",
        "hitos": [
            "Publicar resolución de convocatoria RDC",
            "Difundir en medios locales y redes institucionales",
            "Confirmar sede y logística 2 sesiones",
            "Preparar informe ejecutivo ciudadano (lenguaje accesible)",
        ],
    },
    {
        "fase": "FASE 3 · Ejecución RDC",
        "periodo": "Agosto 2026",
        "color": "green",
        "hitos": [
            "Sesión 1: informe de gestión + metas PDOT",
            "Sesión 2: respuesta compromisos + participación ciudadana",
            "Recoger actas y compromisos formalizados",
            "Enviar informe al CPCCS con evidencias",
        ],
    },
    {
        "fase": "FASE 4 · Cierre",
        "periodo": "Sep. 2026",
        "color": "purple",
        "hitos": [
            "Publicar informe completo en portal (LOTAIP)",
            "Subir al CPCCS sistema SIGPC",
            "Obtener calificación V≥70",
            "Incorporar compromisos en POA Q4-2026",
        ],
    },
]


def _semaforo_badge(semaforo: str) -> str:
    """Traduce semáforo interno → badge HTML Bloomberg-safe."""
    mapa = {
        "VERDE":    ("var(--green)",  "rgba(0,200,83,.15)",  "CUMPLE"),
        "ROJO":     ("var(--red)",    "rgba(255,77,109,.15)","BRECHA"),
        "AMARILLO": ("var(--amber)",  "rgba(255,184,0,.15)", "RIESGO"),
        "PENDIENTE":("var(--muted)",  "rgba(120,120,120,.15)","PENDIENTE"),
    }
    color, bg, label = mapa.get(semaforo.upper(), mapa["PENDIENTE"])
    return (
        f'<span style="font-size:9px;font-weight:700;color:{color};'
        f'background:{bg};border-radius:4px;padding:2px 7px">{label}</span>'
    )


def _render_crdc_bloque() -> str:
    """
    Bloque HTML con el estado live del Circuito C-RDC.
    Solo lenguaje de gobernanza (Bloomberg-safe).
    Retorna '' si el conector no está disponible.
    """
    if not _CRDC_AVAILABLE:
        return ""

    try:
        state = get_crdc_state()
    except Exception as exc:
        logger.warning(f"get_crdc_state() falló: {exc}")
        return ""

    estado         = state.get("estado", "BLOQUEADO")
    pct_ok         = state.get("pct_ok", 0.0)
    nodos_ok       = state.get("nodos_ok", 0)
    nodos_total    = state.get("nodos_total", 6)
    nodos_pend     = state.get("nodos_pendientes", 0)
    impacto_usd    = state.get("impacto_d02_usd", 0)
    narrativa      = state.get("narrativa", "")
    fuente_neo4j   = state.get("fuente_neo4j", False)
    fecha_corte    = state.get("fecha_corte", "2026")
    nodos          = state.get("nodos", [])

    # ── color por estado ──
    _COLORES = {
        "PREPARADO":   ("var(--green)",  "rgba(0,200,83,.08)",  "rgba(0,200,83,.25)"),
        "CON_BRECHAS": ("var(--amber)",  "rgba(255,184,0,.07)", "rgba(255,184,0,.25)"),
        "BLOQUEADO":   ("var(--red)",    "rgba(255,77,109,.08)","rgba(255,77,109,.25)"),
    }
    col, bg, border = _COLORES.get(estado, _COLORES["BLOQUEADO"])

    # ── fuente badge ──
    fuente_badge = (
        '<span style="font-size:8px;color:var(--cyan);background:rgba(0,212,255,.1);'
        'border-radius:4px;padding:1px 5px;margin-left:6px">● Datos en vivo</span>'
        if fuente_neo4j else
        '<span style="font-size:8px;color:var(--muted);background:rgba(120,120,120,.1);'
        'border-radius:4px;padding:1px 5px;margin-left:6px">◌ Fallback local</span>'
    )

    # ── barra progreso ──
    barra = f"""
<div style="height:6px;background:var(--divider);border-radius:3px;
            overflow:hidden;margin:8px 0 14px">
  <div style="height:6px;width:{pct_ok:.0f}%;background:{col};
              border-radius:3px;transition:width .4s"></div>
</div>"""

    # ── nodos ──
    nodos_html = ""
    for nodo in nodos:
        nombre    = nodo.get("nombre", "")
        indicador = nodo.get("indicador", "")
        valor     = nodo.get("valor_actual")
        umbral    = nodo.get("umbral")
        semaforo  = nodo.get("semaforo", "PENDIENTE")
        brecha    = nodo.get("brecha_pp")
        es_crit   = nodo.get("es_critico", False)

        val_txt = f"{valor:.1f}%" if valor is not None else "Pendiente"
        umb_txt = f"/ req. {umbral:.0f}%" if umbral else ""
        brecha_txt = ""
        if brecha is not None:
            signo = "+" if brecha >= 0 else ""
            brecha_txt = (
                f'<span style="font-size:8px;color:{"var(--muted)" if brecha>=0 else "var(--red)"};">'
                f'  {signo}{brecha:.1f}pp</span>'
            )
        crit_badge = (
            '<span style="font-size:8px;font-weight:700;color:var(--red);'
            'background:rgba(255,77,109,.1);border-radius:3px;'
            'padding:1px 5px;margin-left:4px">CRÍTICO</span>'
            if es_crit and semaforo != "VERDE" else ""
        )

        nodos_html += f"""
<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
            background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:3px">
  <div style="flex:1;font-size:10px;color:var(--white)">{nombre}{crit_badge}</div>
  <div style="font-size:9px;color:var(--muted);font-family:var(--mono)">
    {val_txt} {umb_txt}
  </div>
  {brecha_txt}
  <div>{_semaforo_badge(semaforo)}</div>
</div>"""

    # ── impacto D02 ──
    impacto_html = ""
    if impacto_usd > 0:
        impacto_html = f"""
<div style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);
            border-radius:8px;padding:10px 14px;margin-top:12px">
  <div style="font-size:9px;font-weight:700;color:var(--amber);margin-bottom:3px">
    ⚡ IMPACTO EN FINANCIAMIENTO INTERNACIONAL (D02)
  </div>
  <div style="font-size:11px;font-weight:900;color:var(--amber);font-family:var(--mono)">
    ${impacto_usd:,.0f} bloqueados
  </div>
  <div style="font-size:9px;color:var(--muted);margin-top:4px">
    {state.get('impacto_descripcion',
      'Las brechas del circuito bloquean acceso a fondos internacionales.')}
  </div>
</div>"""

    return f"""
<div style="background:{bg};border:1px solid {border};
            border-radius:12px;padding:16px;margin-bottom:16px">
  <div style="display:flex;align-items:center;justify-content:space-between;
              flex-wrap:wrap;gap:8px;margin-bottom:4px">
    <div>
      <span style="font-size:11px;font-weight:700;color:var(--white)">
        CIRCUITO CONVERGENTE · RENDICIÓN DE CUENTAS
      </span>
      {fuente_badge}
    </div>
    <div style="display:flex;align-items:center;gap:10px">
      <span style="font-size:9px;color:var(--muted)">{fecha_corte}</span>
      <span style="font-size:10px;font-weight:700;color:{col};
                   background:{bg};border:1px solid {border};
                   border-radius:6px;padding:3px 10px">{estado}</span>
      <span style="font-size:10px;font-weight:900;color:{col};
                   font-family:var(--mono)">{nodos_ok}/{nodos_total}
        <span style="font-size:8px;font-weight:400;color:var(--muted)"> nodos</span>
        &nbsp;{pct_ok:.0f}%
      </span>
    </div>
  </div>
  {barra}
  <div style="font-size:9px;color:var(--muted);margin-bottom:12px;
              line-height:1.5;border-left:2px solid {border};
              padding-left:10px;font-style:italic">
    {narrativa[:320]}{'…' if len(narrativa)>320 else ''}
  </div>
  <div style="font-size:9px;font-weight:700;color:var(--cyan);
              text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">
    Estado por área
  </div>
  {nodos_html}
  {impacto_html}
</div>"""


def _check_row(cat: str, item: str, ok: bool, urgente: bool) -> str:
    ico    = "✅" if ok else ("🔴" if urgente else "⬜")
    col    = "green" if ok else "red" if urgente else "muted"
    badge  = ('<span style="font-size:8px;font-weight:700;color:var(--red);'
              'background:rgba(255,77,109,.15);border-radius:4px;padding:1px 5px;'
              'margin-left:5px">URGENTE</span>' if urgente and not ok else "")
    return (
        f'<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;'
        f'background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:3px">'
        f'<span style="font-size:13px">{ico}</span>'
        f'<div style="flex:1;font-size:10px;color:var(--{"white" if not ok else "muted"})">'
        f'{item}{badge}</div>'
        f'<span style="font-size:9px;color:var(--muted);flex-shrink:0">{cat}</span>'
        f'</div>'
    )


def _fase_card(f: dict) -> str:
    col = f["color"]
    items_html = "".join(
        f'<div style="font-size:10px;color:var(--white);padding:4px 8px;'
        f'background:rgba(255,255,255,.03);border-radius:5px;margin-bottom:3px">▸ {h}</div>'
        for h in f["hitos"]
    )
    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-top:3px solid var(--{col});border-radius:10px;padding:14px">
  <div style="font-size:10px;font-weight:700;color:var(--{col});margin-bottom:2px">
    {f["fase"]}
  </div>
  <div style="font-size:9px;color:var(--muted);margin-bottom:8px">{f["periodo"]}</div>
  {items_html}
</div>"""


def _render_verificabilidad(show_tech: bool) -> None:
    """VERIFICABILIDAD PÚBLICA DEL DISCURSO (Motor Narrativo) — 2024 y 2025 en secciones separadas
    (Javo · 2026-07-10). Snapshot → HTML → iframe auto-resize (render_page, la convención del app).
    Regla 1: la app NO corre el motor. Cada dominio trabaja su universo completo (prospectivo incluido)."""
    import json
    from pathlib import Path
    try:
        from app.viz.render.html_render import cajon_verificabilidad
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"cajón de verificabilidad no disponible: {exc}")
        return
    base = Path(__file__).resolve().parents[1] / "data" / "motor_narrativo" / "snapshots"

    def _load(a):
        p = base / f"verificabilidad_{a}.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    s24, s25 = _load("2024"), _load("2025")
    if not (s24 or s25):
        return
    # re-reporta la altura del iframe al plegar/desplegar el marco legal (details no burbujea → capture)
    toggle_js = ("<script>document.addEventListener('toggle',function(){var h=Math.max("
                 "document.body.scrollHeight,document.documentElement.scrollHeight);"
                 "window.parent.postMessage({isStreamlitMessage:true,"
                 "type:'streamlit:setFrameHeight',height:h},'*');},true);</script>")
    for año, snap, serie, h0 in (("2024", s24, [s24] if s24 else [], 2200),
                                 ("2025", s25, [x for x in (s24, s25) if x], 2600)):
        if not snap:
            continue
        st.markdown(
            f'<div style="font-family:monospace;font-size:11px;letter-spacing:.16em;'
            f'text-transform:uppercase;color:#7E8BA3;margin:16px 0 4px;text-align:center">'
            f'Rendición de Cuentas · Ejercicio {año}</div>', unsafe_allow_html=True)
        render_page(cajon_verificabilidad(snap, serie) + toggle_js, show_tech=show_tech, height=h0)


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    _render_verificabilidad(show_tech)   # Motor Narrativo — cajones 2024 + 2025 (sección líder)
    st.markdown("---")

    n_ok   = sum(1 for _, _, ok, _ in CHECKLIST_RDC if ok)
    n_tot  = len(CHECKLIST_RDC)
    n_urg  = sum(1 for _, _, ok, urg in CHECKLIST_RDC if urg and not ok)
    pct_ok = (n_ok / n_tot) * 100

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">V=0</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">CPCCS RDC 2025</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">No validado · riesgo 2026</div>
  </div>
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{pct_ok:.0f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">CHECKLIST LISTO</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">{n_ok}/{n_tot} ítems OK</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">{n_urg}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">URGENTES</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Sin estos → RDC en riesgo</div>
  </div>
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--cyan);font-family:var(--mono)">AGO-2026</div>
    <div style="font-size:10px;font-weight:700;color:var(--cyan);margin-top:4px">PRÓXIMA RDC</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Convocatoria Julio · CPCCS</div>
  </div>
</div>"""

    checklist_by_cat: dict = {}
    for cat, item, ok, urg in CHECKLIST_RDC:
        checklist_by_cat.setdefault(cat, []).append((item, ok, urg))

    cats_html = ""
    for cat, items in checklist_by_cat.items():
        rows = "".join(_check_row(cat, i, ok, urg) for i, ok, urg in items)
        cats_html += f"""
  <div style="margin-bottom:12px">
    <div style="font-size:9px;font-weight:700;color:var(--cyan);text-transform:uppercase;
                letter-spacing:.08em;margin-bottom:6px">{cat}</div>
    {rows}
  </div>"""

    checklist_html = f"""
<div class="card">
  <div class="card-title">✅ CHECKLIST RDC 2026 · {n_ok}/{n_tot} ítems completados</div>
  <div style="height:6px;background:var(--divider);border-radius:3px;
              overflow:hidden;margin-bottom:14px">
    <div style="height:6px;width:{pct_ok:.0f}%;background:var(--amber);border-radius:3px"></div>
  </div>
  {cats_html}
</div>"""

    fases_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">📅 TIMELINE RDC 2026 · 4 fases · Mayo → Septiembre</div>
  <div class="grid-4" style="gap:12px">
    {"".join(_fase_card(f) for f in _FASES)}
  </div>
</div>"""

    # ── C-RDC live circuit ──────────────────────────────────────────────────
    crdc_html = _render_crdc_bloque()

    hdr = page_header(
        "⑬ RENDICIÓN DE CUENTAS",
        "RDC 2026 · CPCCS · Checklist · Circuito Convergente",
        f"CPCCS V=0 RDC 2025 · {n_ok}/{n_tot} ítems listos · {n_urg} urgentes · RDC Agosto 2026",
        '<span class="badge badge-red">🔴 RDC en preparación</span>',
    )

    render_page(
        hdr + resumen_html + crdc_html + checklist_html + fases_html,
        show_tech=show_tech,
        height=1650,
    )

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Plan RDC 2026", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "Montecristi tuvo CPCCS V=0 en la RDC 2025. "
                f"El checklist RDC 2026 muestra {n_ok}/{n_tot} ítems listos y {n_urg} urgentes. "
                "La RDC está programada para Agosto 2026. "
                "¿Qué debo hacer en los próximos 90 días para garantizar V≥70 en el CPCCS, "
                "cuáles son los errores más comunes que invalidan una RDC y "
                "qué documentos específicos exige el CPCCS en el sistema SIGPC?"
            )
            st.rerun()
    with c2:
        if st.button("🗳️ Ver Confianza Ciudadana", use_container_width=True):
            st.session_state["page"] = "confianza"
            st.rerun()
    with c3:
        if st.button("⑪ Ver Transparencia LOTAIP", use_container_width=True):
            st.session_state["page"] = "transparencia"
            st.rerun()
