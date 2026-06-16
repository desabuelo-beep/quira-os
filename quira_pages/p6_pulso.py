"""
QUIRA OS — Pulso Institucional (d06 · pestaña Pulso)
Lee del snapshot local (cargar_gm_snapshot) · lenguaje de gobernanza (frontera Regla 2).
Cero demo_data · cero hardcodes. Dylus Lab © 2026
"""
import streamlit as st
from utils.cache_quira import cargar_gm_snapshot
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# Entidades del grupo municipal → clave en el snapshot (h90 consolidado)
_ENTIDADES_HOLDING = [
    ("gad",       "GAD Municipal"),
    ("patronato", "Patronato Municipal"),
    ("ep_aseo",   "EP Aseo"),
    ("bomberos",  "Cuerpo de Bomberos"),
]
# Las 4 coherencias de gobernanza — juicio de la capa de razonamiento (pendiente)
_COHERENCIAS = [
    "Coherencia política", "Coherencia operativa",
    "Coherencia territorial", "Coherencia ecosistémica",
]


def render() -> None:
    gm        = cargar_gm_snapshot()
    show_tech = is_tecnico()

    if not gm or not gm.get("icpi"):
        st.info(
            "💡 Sin datos del período disponibles. El pulso institucional se "
            "habilitará una vez cargada la información del corte."
        )
        return

    icpi = gm.get("icpi", {})
    sat  = gm.get("sat_gm", {})
    vec  = gm.get("vectores", {})
    terr = gm.get("territorial", {})
    h90  = gm.get("financiero", {}).get("h90_consolidado", {})

    score   = icpi.get("global_pct", 0.0)
    clasif  = icpi.get("clasificacion", "—")
    n_crit  = int(sat.get("activas_count", 0))
    psg_val = vec.get("psg", {}).get("valor", 0.0)

    # Parroquia crítica + per cápita real (del snapshot territorial)
    parr_crit = terr.get("parroquia_critica", "—")
    parroquias = terr.get("parroquias", [])
    pc     = next((p for p in parroquias if p.get("nombre") == parr_crit), {})
    pc_pc  = pc.get("inv_percapita_q1", 0)
    cab_pc = next((p.get("inv_percapita_q1", 0) for p in parroquias if p.get("tipo") == "Urbana"), 0)

    # ── ALERTAS (real) ─────────────────────────────────────────────────────────
    alertas_html = f"""
<div class="grid-3" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">{n_crit}</div>
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-top:4px">ALERTAS ACTIVAS</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">Requieren atención del concejo</div>
  </div>
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">${pc_pc:.0f}</div>
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-top:4px">/HAB · {str(parr_crit).upper()}</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">vs ${cab_pc:.0f}/hab en la cabecera cantonal</div>
  </div>
  <div style="background:rgba(124,92,252,.08);border:1px solid rgba(124,92,252,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--purple);font-family:var(--mono)">{psg_val:.1f}%</div>
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-top:4px">PRESUPUESTO CON ENFOQUE DE GÉNERO</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">Limita el financiamiento con enfoque de género</div>
  </div>
</div>"""

    # ── GRUPO MUNICIPAL · ejecución presupuestaria por entidad (real) ──────────
    def _ent_row(key: str, nombre: str) -> str:
        ti  = h90.get(f"{key}_ti_q1_pct", 0.0) or 0.0
        col = "green" if ti >= 35 else "amber" if ti >= 15 else "red"
        pct = min(ti, 100)
        return f"""
  <div style="display:flex;align-items:center;gap:10px;padding:10px;
              background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:6px">
    <div style="min-width:150px">
      <div style="font-size:11px;font-weight:700;color:var(--white)">{nombre}</div>
      <div style="font-size:9px;color:var(--muted)">Ejecución presupuestaria Q1</div>
    </div>
    <div style="flex:1">
      <div style="height:4px;background:var(--divider);border-radius:2px;overflow:hidden">
        <div style="height:4px;width:{pct:.0f}%;background:var(--{col});border-radius:2px"></div>
      </div>
    </div>
    <div style="font-size:14px;font-weight:800;color:var(--{col});
                font-family:var(--mono);min-width:50px;text-align:right">{ti:.1f}%</div>
  </div>"""

    holding_html = f"""
<div class="card">
  <div class="card-title">🏛️ GRUPO MUNICIPAL · EJECUCIÓN POR ENTIDAD</div>
  {''.join(_ent_row(k, n) for k, n in _ENTIDADES_HOLDING)}
</div>"""

    # ── COHERENCIAS DE GOBERNANZA → capa de razonamiento (pendiente) ───────────
    def _coh_card(nombre: str) -> str:
        return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-top:3px solid var(--muted);border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;
                letter-spacing:.08em;margin-bottom:8px">{nombre}</div>
    <div style="font-size:22px;font-weight:800;color:var(--muted);font-family:var(--mono)">—</div>
    <div style="font-size:10px;color:var(--muted);margin-top:6px">Pendiente análisis contextual</div>
  </div>"""

    cong_html = f"""
<div class="card">
  <div class="card-title">🎯 COHERENCIA DE GOBERNANZA</div>
  <div class="grid-4">{''.join(_coh_card(n) for n in _COHERENCIAS)}</div>
  <div style="font-size:11px;color:var(--muted);margin-top:10px;padding:0 4px">
    El análisis de coherencia entre planificación, ejecución y territorio lo emite la capa de
    razonamiento de QUIRA cuando la evidencia del período está completa.</div>
</div>"""

    # ── HEADER ─────────────────────────────────────────────────────────────────
    hdr = page_header(
        "① PULSO INSTITUCIONAL",
        "Pulso Institucional",
        f"Cumplimiento institucional: {score:.2f}% · {clasif}",
        '<span class="badge badge-amber">Corte parcial</span>',
    )

    render_page(hdr + alertas_html + holding_html + cong_html, show_tech=show_tech, height=900)

    # ── CTAs ───────────────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 ¿Qué hacemos esta semana?", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"Soy el alcalde de Montecristi. Al corte de abril el cumplimiento institucional es "
                f"{score:.1f}%, con {n_crit} alertas activas y el presupuesto con enfoque de género en "
                f"{psg_val:.1f}%. ¿Cuáles son las 3 acciones más urgentes esta semana?"
            )
            st.rerun()
    with c2:
        if st.button("📊 Ver causas (brechas)", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c3:
        if st.button("🎯 Ver metas del plan cantonal", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
