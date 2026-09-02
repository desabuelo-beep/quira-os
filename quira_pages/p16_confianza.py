"""
QUIRA OS — P-16 Participación Ciudadana (cajón d08)
Headline = participación del snapshot vivo (`cargar_gm_snapshot` · `vectores.igp`), coherente con la tarjeta L1.
NO se escribe el valor aquí: era 48,33 y el motor calcula 27,00 desde que Javo retiró IGP_3 (2026-07-29).
Mecanismos = hechos cuantitativos reales (actas PP, CPCCS, veedurías): textura cualitativa, NO aritmética del headline.
Scores de mecanismos derivados de hechos cuantitativos en "avance":
  Asambleas:   2/7   × 100 = 28.6% → 29
  Presupuesto: 7/7   × 100 = 100%  → 100 (PP 2026: 6 talleres, 149 fichas, ACTA N°007-2025 agosto)
  UT:          50/75 × 100 = 66.7% → 67
  RDC:         CPCCS V=0  → 0
  Veedurías:   3/6   × 100 = 50.0% → 50
  Portal:      0 publicados → 0
Fuente PP 2026: INFORME PP 2026 GAD Montecristi · $20,982,884.47 estimación ingresos
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header
from utils.cache_quira import cargar_gm_snapshot

# ── MECANISMOS DE PARTICIPACIÓN · Estado Q1-2026 ──────────────────────────────
# score = derivado del hecho cuantitativo declarado en "avance" (ver docstring módulo)
MECANISMOS = [
    {
        "nombre": "Asambleas Parroquiales",
        "estado": "CRÍTICO", "color": "red",
        "avance": "2 de 7 realizadas · Isabel Muentes y Aníbal San Andrés sin convocar",
        "meta": "7/7 al Q2-2026 · COOTAD Art. 304",
        "score": 29,          # 2/7 × 100 = 28.6% → 29
        "formula": "2/7 asambleas",
    },
    {
        "nombre": "Presupuesto Participativo",
        "estado": "NORMAL", "color": "green",
        "avance": "7/7 parroquias con acta · PP 2026: 6 talleres, 149 fichas · $20.98M estimación ingresos · ACTA N°007-2025 (15 ago 2025)",
        "meta": "Mantener 7/7 · ≥$80K inversión ejecutada por zona rural · vinculación POA 2026",
        "score": 100,         # 7/7 parroquias con acta PP 2026 × 100 = 100% (fuente: Informe PP GAD)
        "formula": "7/7 parroquias con acta PP 2026",
    },
    {
        "nombre": "Unidades Territoriales (UT)",
        "estado": "ALERTA", "color": "amber",
        "avance": "50 activas vs meta 75 · 2 parroquias sin UT activa",
        "meta": "75 UT activas con acta Q1-2026 vigente",
        "score": 67,          # 50/75 × 100 = 66.7% → 67  ✓
        "formula": "50/75 UT activas",
    },
    {
        "nombre": "Rendición de Cuentas (RDC)",
        "estado": "CRÍTICO", "color": "red",
        "avance": "CPCCS V=0 en RDC 2025 · calificación no validada",
        "meta": "CPCCS V≥70 en RDC 2026 · convocatoria Q3",
        "score": 0,           # CPCCS V=0 → 0% · fuente: calificación CPCCS oficial
        "formula": "CPCCS V=0/100",
    },
    {
        "nombre": "Veedurías Ciudadanas",
        "estado": "NORMAL", "color": "green",
        "avance": "3 veedurías activas · EP Aseo, vialidad, agua cabecera",
        "meta": "6 veedurías · cobertura inversión social",
        "score": 50,          # 3/6 veedurías meta × 100 = 50%
        "formula": "3/6 veedurías",
    },
    {
        "nombre": "Portal de Denuncias y Quejas",
        "estado": "CRÍTICO", "color": "red",
        "avance": "0 estadísticas publicadas · LOTAIP Art. 7r incumplido",
        "meta": "Sistema activo + reporte mensual ciudadano",
        "score": 0,           # 0 publicaciones = 0% de avance
        "formula": "0 estadísticas publicadas",
    },
]


def _mecanism_row(m: dict) -> str:
    col   = m["color"]
    badge = {
        "CRÍTICO": '<span class="badge badge-red">CRÍTICO</span>',
        "ALERTA":  '<span class="badge badge-amber">ALERTA</span>',
        "NORMAL":  '<span class="badge badge-green">NORMAL</span>',
    }.get(m["estado"], "")
    pct = min(m["score"], 100)
    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:9px;
              padding:12px 14px;margin-bottom:8px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:11px;font-weight:700;color:var(--white)">{m["nombre"]}</span>
        {badge}
      </div>
      <div style="font-size:16px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">{m["score"]}%</div>
    </div>
    <div style="height:4px;background:var(--divider);border-radius:2px;
                overflow:hidden;margin-bottom:6px">
      <div style="height:4px;width:{pct:.0f}%;background:var(--{col});border-radius:2px"></div>
    </div>
    <div style="font-size:10px;color:var(--muted);margin-bottom:3px">{m["avance"]}</div>
    <div style="font-size:10px;color:var(--cyan)">🎯 {m["meta"]}</div>
  </div>"""


def _parroquia_participacion(p: dict) -> str:
    part  = p.get("participacion", {})
    est   = part.get("estado", "Sin datos")
    col_map = {"Activo": "green", "Parcial": "amber", "Bajo": "amber", "Sin voz": "red"}
    col   = col_map.get(est, "muted")
    mesas = part.get("mesas", 0)
    pres  = part.get("presupuesto", 0)
    actas = part.get("actas", 0)
    return (
        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 10px;'
        f'background:rgba(255,255,255,.02);border-radius:7px;margin-bottom:6px">'
        f'<div style="font-size:18px">{p["emoji"]}</div>'
        f'<div style="flex:1">'
        f'<div style="font-size:11px;font-weight:700;color:var(--white)">{p["nombre"]}</div>'
        f'<div style="font-size:9px;color:var(--muted)">'
        f'Mesas: {mesas} · Presupuesto: ${pres:,} · Actas: {actas}'
        f'</div></div>'
        f'<span style="font-size:9px;font-weight:700;padding:3px 8px;border-radius:5px;'
        f'background:rgba(255,255,255,.06);color:var(--{col})">{est}</span>'
        f'</div>'
    )


def render() -> None:
    data       = load_all()
    gm         = cargar_gm_snapshot()
    show_tech  = is_tecnico()
    parroquias = data.get("parroquias", [])
    # Participacion: cifra madre del motor vivo (`vectores.igp`), NO del demo (coherencia tarjeta L1).
    # El valor NO se cita en el comentario: cambió el 2026-08-11 y un comentario no se entera.
    igp_val    = ((gm or {}).get("vectores", {}).get("igp") or {}).get("valor")
    if igp_val is None:
        igp_val = data.get("indices", {}).get("IGP", {}).get("valor", 0.0)

    n_sin_voz = sum(1 for p in parroquias
                    if p.get("participacion", {}).get("estado") == "Sin voz")
    mesas_tot = sum(p.get("participacion", {}).get("mesas", 0) for p in parroquias)
    pres_tot  = sum(p.get("participacion", {}).get("presupuesto", 0) for p in parroquias)

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{igp_val:.2f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">PARTICIPACIÓN</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Mecanismos institucionales</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">{n_sin_voz}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">SIN VOZ</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Parroquias sin participación</div>
  </div>
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--cyan);font-family:var(--mono)">{mesas_tot}</div>
    <div style="font-size:10px;font-weight:700;color:var(--cyan);margin-top:4px">MESAS ACTIVAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">7 parroquias · Q1-2026</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:24px;font-weight:900;color:var(--green);
                font-family:var(--mono)">${pres_tot:,}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">PRESUPUESTO PP</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Participativo asignado</div>
  </div>
</div>"""

    cpccs_html = """
<div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.3);
            border-radius:12px;padding:14px 16px;margin-bottom:16px;
            display:flex;align-items:center;gap:14px">
  <div style="text-align:center;min-width:80px">
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-bottom:4px">CPCCS</div>
    <div style="font-size:36px;font-weight:900;color:var(--red);font-family:var(--mono)">V=0</div>
    <div style="font-size:9px;color:var(--muted)">RDC 2025</div>
  </div>
  <div style="flex:1;font-size:11px;color:var(--muted);line-height:1.7">
    El CPCCS (Consejo de Participación Ciudadana y Control Social) calificó
    con <strong style="color:var(--red)">V=0 la Rendición de Cuentas 2025</strong>
    de Montecristi. Esto significa que el proceso no fue validado por la ciudadanía —
    ni por asistencia, ni por calidad de información, ni por seguimiento de compromisos.
    Si se repite en RDC 2026, el CPCCS puede iniciar proceso de evaluación y control.
    <br><br>
    <strong style="color:var(--cyan)">Próxima RDC: Q3-2026</strong> ·
    Requiere convocatoria ampliada · mínimo 2 sesiones · informe validado por CPCCS.
  </div>
</div>"""

    mecanismos_html = f"""
<div class="card">
  <div class="card-title">🗳️ 6 MECANISMOS DE PARTICIPACIÓN · Estado ene–mar 2026</div>
  <div style="font-size:8px;color:rgba(0,212,255,.7);margin-bottom:10px;
              padding:5px 10px;background:rgba(0,212,255,.05);border-radius:5px;
              border:1px solid rgba(0,212,255,.15)">
    📐 <strong>Avance por mecanismo:</strong>
    cada barra es la razón cuantitativa real del mecanismo
    (2/7 asambleas, 7/7 presupuesto participativo, 50/75 unidades territoriales,
    rendición de cuentas sin validar, 3/6 veedurías, portal sin publicar).
    Fuente: registros institucionales · actas PP 2026 · calificación CPCCS.
  </div>
  {"".join(_mecanism_row(m) for m in MECANISMOS)}
</div>"""

    parroquias_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">🗺️ PARTICIPACIÓN POR PARROQUIA · 7 territorios</div>
  {"".join(_parroquia_participacion(p) for p in parroquias)}
  <div style="margin-top:10px;padding:8px 10px;
              background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.15);
              border-radius:7px;font-size:10px;color:var(--red)">
    ⚠️ <strong>Isabel Muentes</strong> y <strong>Aníbal San Andrés</strong> tienen 0 mesas,
    $0 presupuesto participativo y 0 actas registradas. Sin convocatoria urgente,
    la RDC 2026 no podrá demostrar cobertura territorial completa ante el CPCCS.
  </div>
</div>"""

    _ord    = sorted(MECANISMOS, key=lambda m: m["score"], reverse=True)
    _clean  = lambda n: n.split(" (")[0]
    fuertes = [_clean(m["nombre"]) for m in _ord[:2]]
    debiles = [_clean(m["nombre"]) for m in _ord[-2:]]
    narrativa = (
        f"La participación ciudadana alcanza {igp_val:.2f}% al corte — la misma cifra del Centro de Mando. "
        f"La sostienen los mecanismos fuertes ({fuertes[0]}, {fuertes[1]}) y la frenan los críticos "
        f"({debiles[0]}, {debiles[1]}, sin validación ciudadana). Es una lectura del trimestre, no un cierre anual."
    )
    eje_html = (
        '<div style="margin-bottom:16px;padding:12px 16px;background:rgba(245,158,11,.06);'
        'border-left:3px solid var(--amber);border-radius:0 10px 10px 0">'
        '<div style="font-size:11px;font-weight:700;color:var(--amber);margin-bottom:4px">'
        '🎯 Lectura de la participación al corte</div>'
        f'<div style="font-size:11px;color:var(--white);line-height:1.6">{narrativa}</div>'
        '</div>'
    )

    hdr = page_header(
        "⑧ PARTICIPACIÓN CIUDADANA",
        "Mecanismos · Presupuesto Participativo · CPCCS",
        f"Participación {igp_val:.2f}% · {n_sin_voz} parroquias sin voz · CPCCS V=0 RDC 2025 · ene–mar 2026",
        '<span class="badge badge-red">🔴 CPCCS V=0</span>',
    )

    render_page(hdr + resumen_html + eje_html + cpccs_html + mecanismos_html + parroquias_html,
                show_tech=show_tech, height=1480)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Estrategia CPCCS + Participación",
                     use_container_width=True, type="primary", key="conf_sentinel"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"La participación ciudadana de Montecristi es {igp_val:.2f}%. El CPCCS calificó V=0 la RDC 2025. "
                "Isabel Muentes y Aníbal San Andrés tienen 0 mesas participativas y $0 "
                "en presupuesto participativo. La próxima RDC es Q3-2026. "
                "¿Cuál es la estrategia concreta para obtener V≥70 en la RDC 2026, "
                "qué documentación exige el CPCCS y cómo se convocan las asambleas "
                "en las dos parroquias sin voz antes de Q2-2026?"
            )
            st.rerun()
    with c2:
        if st.button("🗺️ Ver Territorio Digital", use_container_width=True, key="conf_geotwin"):
            st.session_state["page"] = "geotwin"
            st.rerun()
    with c3:
        if st.button("🎯 Ver Metas del Plan Cantonal", use_container_width=True, key="conf_metas"):
            st.session_state["page"] = "metas"
            st.rerun()
