"""
QUIRA OS v0.1 — P-15 Transparencia LOTAIP
ITAM 56% · IOC 17.71% · 21 artículos LOTAIP · Portal Municipal
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── 21 ARTÍCULOS LOTAIP · Estado Q1-2026 ─────────────────────────────────────
LOTAIP_ARTS = [
    {"art": "Art. 7a",  "desc": "Estructura orgánica y funcional",          "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7b",  "desc": "Objetivos y metas institucionales",        "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7c",  "desc": "Nómina de servidores públicos y remuneraciones", "estado": "OK","puntaje": 1.0},
    {"art": "Art. 7d",  "desc": "Servicios que ofrece y cómo acceder a ellos",   "estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7e",  "desc": "Texto íntegro de contratos colectivos",    "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7f",  "desc": "Formularios y solicitudes que puede usar el ciudadano","estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7g",  "desc": "Información sobre el presupuesto anual",   "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7h",  "desc": "Resultados de auditorías internas y externas",   "estado": "NO","puntaje": 0.0},
    {"art": "Art. 7i",  "desc": "Procesos precontractuales y contractuales","estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7j",  "desc": "Plan de compras públicas (PAC)",           "estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7k",  "desc": "Viajes internacionales de servidores públicos",  "estado": "OK", "puntaje": 1.0},
    {"art": "Art. 7l",  "desc": "Comisiones de servicio realizadas",        "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7m",  "desc": "Remuneraciones adicionales / viáticos",    "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7n",  "desc": "Subsidios o becas otorgadas",              "estado": "NO",      "puntaje": 0.0},
    {"art": "Art. 7o",  "desc": "Contratos de crédito externo",             "estado": "OK",      "puntaje": 1.0},
    {"art": "Art. 7p",  "desc": "Resoluciones de trámites administrativos", "estado": "NO",      "puntaje": 0.0},
    {"art": "Art. 7q",  "desc": "Información estadística de la institución","estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7r",  "desc": "Estadísticas de quejas y reclamos",        "estado": "NO",      "puntaje": 0.0},
    {"art": "Art. 7s",  "desc": "Acceso a información pública por solicitud","estado": "OK",     "puntaje": 1.0},
    {"art": "Art. 7t",  "desc": "Mecanismos de rendición de cuentas",       "estado": "PARCIAL","puntaje": 0.5},
    {"art": "Art. 7u",  "desc": "Viáticos y gastos de viaje nacionales",    "estado": "OK",      "puntaje": 1.0},
]

_cumplidos = sum(1 for a in LOTAIP_ARTS if a["estado"] == "OK")
_parciales = sum(1 for a in LOTAIP_ARTS if a["estado"] == "PARCIAL")
_faltantes = sum(1 for a in LOTAIP_ARTS if a["estado"] == "NO")
_puntaje_total = sum(a["puntaje"] for a in LOTAIP_ARTS)
_itam_calc = (_puntaje_total / len(LOTAIP_ARTS)) * 100  # ≈ 56%


def _art_row(a: dict) -> str:
    estado_map = {
        "OK":      ("green", "✅", "PUBLICADO"),
        "PARCIAL": ("amber", "⚠️", "PARCIAL"),
        "NO":      ("red",   "❌", "FALTANTE"),
    }
    col, ico, lbl = estado_map[a["estado"]]
    badge_cls = {"OK": "badge-green", "PARCIAL": "badge-amber", "NO": "badge-red"}[a["estado"]]
    return (
        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;'
        f'background:rgba(255,255,255,.02);border-radius:6px;margin-bottom:4px">'
        f'<div style="font-size:9px;font-weight:700;color:var(--muted);min-width:52px">{a["art"]}</div>'
        f'<div style="flex:1;font-size:10px;color:var(--white)">{a["desc"]}</div>'
        f'<span class="badge {badge_cls}" style="flex-shrink:0">{ico} {lbl}</span>'
        f'</div>'
    )


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    indices   = data["indices"]
    itam_val  = indices.get("ITAM", {}).get("valor", 56.0)
    ioc_val   = indices.get("IOC",  {}).get("valor", 17.71)

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{itam_val:.0f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">ITAM · SCORE</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Transición Crítica · meta 75%</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);font-family:var(--mono)">{_cumplidos}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">ARTS. PUBLICADOS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">de 21 LOTAIP</div>
  </div>
  <div style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);font-family:var(--mono)">{_parciales}</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">ARTS. PARCIALES</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Publicación incompleta</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">{_faltantes}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">ARTS. FALTANTES</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">IOC {ioc_val:.2f}% · Opacidad</div>
  </div>
</div>"""

    ioc_html = f"""
<div style="background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
            border-radius:12px;padding:14px 16px;margin-bottom:16px;
            display:flex;align-items:center;gap:16px">
  <div style="text-align:center;min-width:90px">
    <div style="font-size:10px;font-weight:700;color:var(--red);text-transform:uppercase;
                letter-spacing:.08em;margin-bottom:4px">IOC · Opacidad</div>
    <div style="font-size:36px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{ioc_val:.2f}<span style="font-size:14px">%</span></div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Ruptura Sistémica</div>
  </div>
  <div style="flex:1;font-size:11px;color:var(--muted);line-height:1.7">
    ⚠️ El <strong style="color:var(--white)">IOC (Índice de Opacidad Crítica)</strong> es
    un índice <strong style="color:var(--red)">invertido</strong>: mayor valor = mayor opacidad.
    El 17.71% representa el porcentaje de procesos clasificados como opacos
    (sin trazabilidad, sin publicación, sin evidencia digital). Impacta directamente en el ITAM
    y puede derivar en observación de la Contraloría o del CPCCS en la RDC.
  </div>
</div>"""

    lotaip_html = f"""
<div class="card">
  <div class="card-title">📋 21 ARTÍCULOS LOTAIP · Estado portal Q1-2026</div>
  {"".join(_art_row(a) for a in LOTAIP_ARTS)}
  <div style="margin-top:10px;padding:8px 10px;
              background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.12);
              border-radius:7px;font-size:10px;color:var(--cyan)">
    ▶ Acción prioritaria: publicar Art. 7h (auditorías), 7n (becas/subsidios),
    7p (resoluciones), 7r (estadísticas quejas) · 4 artículos faltantes = +19% ITAM
  </div>
</div>"""

    portal_html = """
<div class="grid-2" style="margin-top:16px">
  <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:8px">
      🔴 PROBLEMAS DETECTADOS EN PORTAL
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        48% del contenido publicado con más de 90 días sin actualizar
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        PAC 2026 publicado sin vinculación a POA ni indicadores PDOT
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        Formularios ciudadanos en PDF estático · sin sistema de trámites online
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        0 estadísticas de quejas y reclamos publicadas (Art. 7r incumplido)
      </div>
    </div>
  </div>
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:8px">
      ✅ PLAN RÁPIDO · ITAM 56% → 75%
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">Semana 1:</strong> Publicar 4 artículos faltantes (+19% ITAM)
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">Semana 2:</strong> Actualizar 5 artículos parciales (+12% ITAM)
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">Mes 2:</strong> Portal renovado con trámites online DTIC
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">Meta:</strong> ITAM 75% → Gestión por Mandato · RDC 2026 OK
      </div>
    </div>
  </div>
</div>"""

    hdr = page_header(
        "⑪ TRANSPARENCIA",
        "LOTAIP · ITAM · Opacidad IOC",
        f"ITAM {itam_val:.0f}% · IOC {ioc_val:.2f}% · {_cumplidos}/21 arts. LOTAIP · Portal Q1-2026",
        '<span class="badge badge-amber">Transición Crítica</span>',
    )

    render_page(hdr + resumen_html + ioc_html + lotaip_html + portal_html,
                show_tech=show_tech, height=1300)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Plan LOTAIP urgente", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El ITAM de Montecristi es 56%. Hay 4 artículos LOTAIP incumplidos "
                "(7h auditorías, 7n becas, 7p resoluciones, 7r quejas) y 5 parciales. "
                "El IOC es 17.71% (opacidad crítica). "
                "¿Cuál es el plan de acción semana a semana para llevar el ITAM a 75% "
                "antes de la Rendición de Cuentas Q3-2026, cumpliendo LOTAIP sin "
                "exceder la capacidad operativa de la Dirección TIC?"
            )
            st.rerun()
    with c2:
        if st.button("⚙️ Ver Operación Técnica", use_container_width=True):
            st.session_state["page"] = "operacion"
            st.rerun()
    with c3:
        if st.button("📊 Ver Tablero Ejecutivo", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
