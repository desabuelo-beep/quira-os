"""
QUIRA OS v0.1 — P-17 Rendición de Cuentas
RDC 2026 · CPCCS · Checklist preparación · Timeline
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── CHECKLIST RDC 2026 ────────────────────────────────────────────────────────
CHECKLIST_RDC = [
    # (categoría, item, ok, urgente)
    ("Normativa",     "Resolución de convocatoria publicada 30 días antes",          False, True),
    ("Normativa",     "Informe de gestión aprobado por Alcaldía",                    False, True),
    ("Normativa",     "Convocatoria ampliada · mínimo 2 sesiones públicas",          False, True),
    ("Financiero",    "Estado de ejecución presupuestaria actualizado al Q2-2026",   False, True),
    ("Financiero",    "ISP regularizado ≥ 25% (avance) antes de RDC",               False, True),
    ("Financiero",    "Informe deuda y coactivas con plan de pago",                  False, False),
    ("PDOT",          "Avance de metas PDOT 2023-2027 con indicadores verificables", False, True),
    ("PDOT",          "4 metas SAT-0 regularizadas (PAC + SHA-256)",                 False, True),
    ("PDOT",          "IFE-A actualizado · 48/66 promesas con estado Q2",            True,  False),
    ("Participación", "7/7 parroquias con asamblea previa a RDC",                    False, True),
    ("Participación", "Actas firmadas y digitalizadas · Isabel Muentes + Aníbal SA", False, True),
    ("Participación", "Presupuesto participativo rendido por parroquia",              False, False),
    ("Transparencia", "21 artículos LOTAIP completos y actualizados",                False, True),
    ("Transparencia", "IOC < 10% (actual 17.71%) · reducir opacidad",               False, False),
    ("Transparencia", "Estadísticas quejas/denuncias publicadas (Art. 7r)",          False, False),
    ("Género",        "PSG ≥ 20% documentado y certificado (actual 12.83%)",         False, False),
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
            "Regularizar SAT-0: 4 metas PAC + 24 SHA-256",
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


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

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

    hdr = page_header(
        "⑬ RENDICIÓN DE CUENTAS",
        "RDC 2026 · CPCCS · Checklist",
        f"CPCCS V=0 RDC 2025 · {n_ok}/{n_tot} ítems listos · {n_urg} urgentes · RDC Agosto 2026",
        '<span class="badge badge-red">🔴 RDC en preparación</span>',
    )

    render_page(hdr + resumen_html + checklist_html + fases_html,
                show_tech=show_tech, height=1400)

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
