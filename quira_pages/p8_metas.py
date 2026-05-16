"""
QUIRA OS v0.1 — P-03 Metas PDOT
Trazabilidad Promesa → Meta → Ejecución · Fiel al DEMO.html P-03
FUENTE DATOS:
  - "avance" = línea base PDOT GAD Municipal Montecristi (documento oficial publicado)
  - "avance" M-06 (PSG 12.83%) = H73_OUTPUT_API / Gold Master v4.1
  - "avance" M-07 (IET $40/hab) = H99_ENGINE_CORE parroquias / Gold Master v4.1
  - Presupuestos = POA/PAC GAD Montecristi (documento público)
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── METAS PDOT SELLADAS Q1-2026 ───────────────────────────────────────────────
METAS_PDOT = [
    {
        "id": "M-01",
        "eje": "Servicios Básicos",
        "meta": "Cobertura red pública agua 34.9% → 65% al 2027",
        "indicador": "% viviendas con conexión agua pública",
        "avance": 34.9,
        "meta_val": 65.0,
        "estado": "CRÍTICO",
        "presupuesto": "$2,400,000",
        "sat": "SAT activa · Isabel Muentes 1.02%",
        "color": "red",
    },
    {
        "id": "M-02",
        "eje": "Servicios Básicos",
        "meta": "Cobertura alcantarillado 43.5% → 70% al 2027",
        "indicador": "% viviendas conectadas red alcantarillado",
        "avance": 43.5,
        "meta_val": 70.0,
        "estado": "CRÍTICO",
        "presupuesto": "$1,800,000",
        "sat": "Sin contrato PAC activo",
        "color": "red",
    },
    {
        "id": "M-03",
        "eje": "Vialidad",
        "meta": "Vías con tratamiento: 53% → 75% al 2027 (casco urbano)",
        "indicador": "% longitud vial con capa de rodadura",
        "avance": 53.0,
        "meta_val": 75.0,
        "estado": "ALERTA",
        "presupuesto": "$3,200,000",
        "sat": "Avance bajo ritmo requerido",
        "color": "amber",
    },
    {
        "id": "M-04",
        "eje": "Residuos Sólidos",
        "meta": "Reducir residuos sin gestión: 47.9 ton/día → 30 ton/día",
        "indicador": "Toneladas/día sin reciclaje ni clasificación",
        "avance": 47.9,
        "meta_val": 30.0,
        "estado": "ALERTA",
        "presupuesto": "$480,000",
        "sat": "EP Aseo bajo umbral · score 58.4%",
        "color": "amber",
    },
    {
        "id": "M-05",
        "eje": "Gobernanza Participativa",
        "meta": "Unidades territoriales activas: 50 → 75 al 2027",
        "indicador": "Número de UT con acta de participación Q1",
        "avance": 50.0,
        "meta_val": 75.0,
        "estado": "ALERTA",
        "presupuesto": "$95,000",
        "sat": "CPCCS V=0 en RDC 2026",
        "color": "amber",
    },
    {
        "id": "M-06",
        "eje": "Género y Equidad",
        "meta": "Presupuesto género PSG: 12.83% → 30% al 2027",
        "indicador": "% POA con perspectiva de género",
        "avance": 12.83,
        "meta_val": 30.0,
        "estado": "CRÍTICO",
        "presupuesto": "$0 (bloqueo Gender Bond)",
        "sat": "Bloquea Gender Bond $95K · ONU Mujeres",
        "color": "red",
    },
    {
        "id": "M-07",
        "eje": "Equidad Territorial",
        "meta": "Inversión mínima parroquias rurales: $40 → $80/hab",
        "indicador": "$ inversión per cápita parroquias rurales",
        "avance": 40.0,
        "meta_val": 80.0,
        "estado": "CRÍTICO",
        "presupuesto": "$1,200,000",
        "sat": "Isabel Muentes: $40/hab · brecha 2.8×",
        "color": "red",
    },
    {
        "id": "M-08",
        "eje": "Transparencia",
        "meta": "ITAM transparencia municipal: 56% → 75% al 2027",
        "indicador": "Índice LOTAIP · publicaciones actualizadas",
        "avance": 56.0,
        "meta_val": 75.0,
        "estado": "NORMAL",
        "presupuesto": "$45,000",
        "sat": "Portal parcialmente actualizado",
        "color": "amber",
    },
    {
        "id": "M-09",
        "eje": "Turismo y Economía",
        "meta": "Plan turismo municipal operativo al Q3-2026",
        "indicador": "Plan aprobado + presupuesto asignado",
        "avance": 0.0,
        "meta_val": 100.0,
        "estado": "ALERTA",
        "presupuesto": "$120,000",
        "sat": "Sin plan formal · UNESCO ciudad creativa sin activar",
        "color": "amber",
    },
    {
        "id": "M-10",
        "eje": "Fidelidad Electoral",
        "meta": "IFE-A fidelidad: 72.73% · formalizar 18 promesas restantes",
        "indicador": "Promesas CNE con meta PDOT formal",
        "avance": 72.73,
        "meta_val": 100.0,
        "estado": "NORMAL",
        "presupuesto": "Planificación",
        "sat": "18 promesas sin respaldo PDOT · riesgo 2027",
        "color": "amber",
    },
]

# ── RESUMEN POR ESTADO ────────────────────────────────────────────────────────
_RESUMEN = {
    "CRÍTICO": {"count": 0, "color": "red",    "icon": "🔴", "label": "CRÍTICAS"},
    "ALERTA":  {"count": 0, "color": "amber",  "icon": "🟠", "label": "EN ALERTA"},
    "NORMAL":  {"count": 0, "color": "green",  "icon": "🟢", "label": "NORMALES"},
    "SIN_PAC": {"count": 0, "color": "purple", "icon": "🟣", "label": "SIN CONTRATO PAC"},
}
for _m in METAS_PDOT:
    if _m["estado"] in _RESUMEN:
        _RESUMEN[_m["estado"]]["count"] += 1
# SAT-0: 4 metas sin contrato PAC (dato fijo del SIAP)
_RESUMEN["SIN_PAC"]["count"] = 4


def _meta_row(m: dict) -> str:
    """Fila HTML para una meta PDOT."""
    pct = min((m["avance"] / m["meta_val"]) * 100, 100) if m["meta_val"] > 0 else 0
    col = m["color"]
    badge_map = {
        "CRÍTICO": '<span class="badge badge-red">CRÍTICO</span>',
        "ALERTA":  '<span class="badge badge-amber">ALERTA</span>',
        "NORMAL":  '<span class="badge badge-green">NORMAL</span>',
    }
    badge = badge_map.get(m["estado"], "")

    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:10px;
              padding:14px 16px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                margin-bottom:8px;gap:12px">
      <div style="flex:1">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
          <span style="font-size:9px;font-weight:700;color:var(--muted);
                       background:rgba(255,255,255,.05);border-radius:4px;
                       padding:2px 6px">{m["id"]}</span>
          <span style="font-size:9px;color:var(--cyan);font-weight:600">{m["eje"]}</span>
          {badge}
        </div>
        <div style="font-size:12px;font-weight:700;color:var(--white);line-height:1.4">
          {m["meta"]}
        </div>
      </div>
      <div style="text-align:right;flex-shrink:0">
        <div style="font-size:22px;font-weight:900;color:var(--{col});
                    font-family:var(--mono)">{pct:.0f}<span style="font-size:11px">%</span></div>
        <div style="font-size:9px;color:var(--muted)">avance</div>
      </div>
    </div>
    <!-- Barra progreso -->
    <div style="height:5px;background:var(--divider);border-radius:3px;
                overflow:hidden;margin-bottom:8px">
      <div style="height:5px;width:{pct:.0f}%;background:var(--{col});
                  border-radius:3px"></div>
    </div>
    <!-- Detalles -->
    <div style="display:flex;justify-content:space-between;align-items:center;
                gap:12px;flex-wrap:wrap">
      <div style="font-size:10px;color:var(--muted)">
        📊 {m["indicador"]} ·
        <span style="color:var(--amber)">{m["avance"]} → {m["meta_val"]}</span>
      </div>
      <div style="font-size:10px;color:var(--red);background:rgba(255,77,109,.06);
                  border-radius:5px;padding:3px 8px">⚠ {m["sat"]}</div>
    </div>
  </div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    n_crit  = _RESUMEN["CRÍTICO"]["count"]
    n_alert = _RESUMEN["ALERTA"]["count"]
    n_norm  = _RESUMEN["NORMAL"]["count"]
    n_pac   = _RESUMEN["SIN_PAC"]["count"]

    # ── RESUMEN CARDS ─────────────────────────────────────────────────────────
    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{n_crit}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">METAS CRÍTICAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Requieren acción inmediata</div>
  </div>
  <div style="background:rgba(255,184,0,.08);border:1px solid rgba(255,184,0,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{n_alert}</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">EN ALERTA</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Bajo ritmo requerido</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{n_norm}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">NORMALES</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">En ritmo adecuado</div>
  </div>
  <div style="background:rgba(124,92,252,.08);border:1px solid rgba(124,92,252,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--purple);
                font-family:var(--mono)">{n_pac}</div>
    <div style="font-size:10px;font-weight:700;color:var(--purple);margin-top:4px">SIN CONTRATO PAC</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">SAT-0 · riesgo Contraloría</div>
  </div>
</div>"""

    # ── IFE BARRA PROMESAS ────────────────────────────────────────────────────
    ife_html = """
<div class="card" style="margin-bottom:16px">
  <div class="card-title">🗳️ IFE-A · TRAZABILIDAD PROMESA → PDOT · 66 compromisos CNE</div>
  <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
    <div style="flex:1;min-width:200px">
      <div style="display:flex;height:24px;border-radius:8px;overflow:hidden;
                  border:1px solid rgba(255,255,255,.1)">
        <div style="width:72.73%;background:var(--green);display:flex;
                    align-items:center;justify-content:center;
                    font-size:10px;font-weight:700;color:#0A1628">
          48 con meta PDOT
        </div>
        <div style="width:27.27%;background:rgba(255,77,109,.4);display:flex;
                    align-items:center;justify-content:center;
                    font-size:10px;font-weight:700;color:var(--red)">
          18 sin meta
        </div>
      </div>
      <div style="display:flex;justify-content:space-between;
                  font-size:9px;color:var(--muted);margin-top:4px">
        <span>72.73% IFE-A · Gestión por Mandato ✅</span>
        <span>27.27% · Riesgo cierre 2027</span>
      </div>
    </div>
    <div style="text-align:center;min-width:80px">
      <div style="font-size:28px;font-weight:900;color:var(--amber);
                  font-family:var(--mono)">72.73<span style="font-size:12px">%</span></div>
      <div style="font-size:9px;color:var(--muted)">Gestión por Mandato</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:10px;color:var(--muted);
              padding:8px 10px;background:rgba(255,184,0,.04);
              border:1px solid rgba(255,184,0,.15);border-radius:7px">
    💡 Mayo 2023: el <strong style="color:var(--white)">Ing. Jonathan Toro Largacha</strong>
    asumió 66 compromisos CNE ante 101,181 ciudadanos.
    18 sin respaldo PDOT generan riesgo político al cierre del mandato 2027.
  </div>
</div>"""

    # ── LISTA DE METAS ────────────────────────────────────────────────────────
    metas_list = f"""
<div class="card">
  <div class="card-title">📋 10 METAS DEL PLAN 2023-2027 · Estado ene–mar 2026</div>
  {"".join(_meta_row(m) for m in METAS_PDOT)}
  <div style="font-size:9px;color:var(--muted);margin-top:8px;padding-top:8px;
              border-top:1px solid rgba(255,255,255,.05)">
    📌 Fuente: PDOT Montecristi 2023-2027 · POA-PAC ene–mar 2026 · SIAP-ICPI v1.0222
    · Corte sellado ene–mar 2026
  </div>
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "③ METAS DEL PLAN",
        "Plan Cantonal 2023-2027",
        "Promesa → Meta → POA → PAC → eSIGEF · 66 compromisos CNE · Corte ene–mar 2026",
        '<span class="badge badge-real">Plan 2023-2027</span>',
    )

    html = hdr + resumen_html + ife_html + metas_list

    render_page(html, show_tech=show_tech, height=2500)

    # ── CTAs Streamlit ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Analizar Metas", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "Mirando las metas PDOT 2023-2027 de Montecristi, "
                "hay 4 metas críticas (agua, alcantarillado, género, inversión per cápita rural) "
                "y 4 metas sin contrato PAC activo (SAT-0). "
                "¿Cuáles son las 3 acciones más urgentes para regularizar el avance "
                "antes del cierre del primer semestre 2026?"
            )
            st.rerun()
    with c2:
        if st.button("📉 Ver Causas de la Brecha", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c3:
        if st.button("⚡ Ver Pulso Ejecutivo", use_container_width=True):
            st.session_state["page"] = "pulso"
            st.rerun()
