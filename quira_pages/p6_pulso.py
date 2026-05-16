"""
QUIRA OS v0.1 — P-00 Pulso Ejecutivo
Executive Pulse · KPIs críticos en un vistazo · Fiel a DEMO.html P-00
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    icgit        = data["icgit"]
    score        = icgit["score"]
    proj         = icgit.get("proyeccion", 65.77)
    congruencias = data["congruencias"]
    sat          = data["sat"]
    holding      = data["holding"]
    indices      = data["indices"]

    n_crit   = sum(1 for s in sat if s["nivel"] == "CRÍTICO")
    n_alerta = sum(1 for s in sat if s["nivel"] == "ALERTA")

    cpol = congruencias["politica"]
    cope = congruencias["operativa"]
    cter = congruencias["territorial"]
    ceco = congruencias["ecosistemica"]
    psg  = indices.get("PSG", {}).get("valor", 12.83)
    iet  = indices.get("IET", {}).get("valor", 44.80)

    def _cong_color(s):
        if s >= 70: return "green"
        if s >= 50: return "amber"
        return "red"

    def _cong_badge(s, avep):
        col = _cong_color(s)
        return f'<span class="badge badge-{"green" if col=="green" else "red" if col=="red" else "amber"}">{avep}</span>'

    # ── ALERTAS CRÍTICAS ──────────────────────────────────────────────────────
    alertas_html = f"""
<div class="grid-3" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">{n_crit}</div>
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-top:4px">SEÑALES CRÍTICAS ACTIVAS</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">Requieren acción inmediata</div>
  </div>
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);font-family:var(--mono)">$40</div>
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-top:4px">/HAB · ISABEL MUENTES</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">vs $217/hab cabecera · brecha 5.4× · H99</div>
  </div>
  <div style="background:rgba(124,92,252,.08);border:1px solid rgba(124,92,252,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--purple);font-family:var(--mono)">{psg:.0f}%</div>
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-top:4px">PRESUPUESTO GÉNERO</div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">Bloquea Gender Bond · ONU Mujeres</div>
  </div>
</div>"""

    # ── 4 CONGRUENCIAS SEMÁFORO ───────────────────────────────────────────────
    def _cong_card(c, key):
        s = c["score"]
        col = _cong_color(s)
        col_css = f"var(--{col})"
        return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-top:3px solid {col_css};border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;
                letter-spacing:.08em;margin-bottom:8px">{c["nombre"]}</div>
    <div style="font-size:38px;font-weight:900;color:{col_css};font-family:var(--mono)">{s:.1f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;color:var(--muted);margin-top:4px">{c["avep"]}</div>
    <div style="font-size:10px;color:rgba(255,255,255,.35);margin-top:6px">{c.get("pregunta","")}</div>
  </div>"""

    cong_html = f"""
<div class="card">
  <div class="card-title">🎯 4 CONGRUENCIAS DE GOBERNANZA · GRUPO MUNICIPAL</div>
  <div class="grid-4">
    {_cong_card(cpol, "politica")}
    {_cong_card(cope, "operativa")}
    {_cong_card(cter, "territorial")}
    {_cong_card(ceco, "ecosistemica")}
  </div>
</div>"""

    # ── RIESGO vs OPORTUNIDAD Q2 ──────────────────────────────────────────────
    riesgo_op = """
<div class="grid-2" style="margin-bottom:16px">
  <div style="background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:12px;font-weight:700;color:var(--red);margin-bottom:10px">
      ⚠️ RIESGOS PRÓXIMO TRIMESTRE — Sin acción inmediata
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.08);border-radius:6px">
        🔴 ISP 14.58% → bloquea perfil BDE y crédito municipal
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.08);border-radius:6px">
        🔴 4 metas PDOT sin ruta → Contraloría podría objetar ejecución
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.1);border-radius:6px">
        🟣 PSG 12.83% → Gender Bond $95K bloqueado, vence Q3-2026
      </div>
    </div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:12px;font-weight:700;color:var(--green);margin-bottom:10px">
      ✅ OPORTUNIDADES PRÓXIMO TRIMESTRE — Acción disponible
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 Ti_norm 70% → ritmo inversión adecuado si se mantiene
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 IFE-A 72.73% → 48/66 promesas en PDOT, base política sólida
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.08);border-radius:6px">
        🔵 ICODS 87.5% → 14 ODS vinculados, proyectos alineables
      </div>
    </div>
  </div>
</div>"""

    # ── HOLDING RADAR RÁPIDO ──────────────────────────────────────────────────
    def _holding_mini(e):
        s   = e.get("score", 0)
        col = "green" if s >= 70 else "amber" if s >= 50 else "red"
        pct = min(s, 100)
        return f"""
  <div style="display:flex;align-items:center;gap:10px;padding:10px;
              background:rgba(255,255,255,.03);border-radius:8px;margin-bottom:6px">
    <div style="min-width:110px">
      <div style="font-size:11px;font-weight:700;color:var(--white)">{e["nombre"]}</div>
      <div style="font-size:9px;color:var(--muted)">{e.get("avep","")}</div>
    </div>
    <div style="flex:1">
      <div style="height:4px;background:var(--divider);border-radius:2px;overflow:hidden">
        <div style="height:4px;width:{pct:.0f}%;background:var(--{col});border-radius:2px"></div>
      </div>
    </div>
    <div style="font-size:14px;font-weight:800;color:var(--{col});
                font-family:var(--mono);min-width:50px;text-align:right">{s:.1f}%</div>
  </div>"""

    holding_rows = "".join(_holding_mini(e) for e in holding.get("entidades", []))
    holding_html = f"""
<div class="card">
  <div class="card-title">🏛️ GRUPO MUNICIPAL · RADAR RÁPIDO</div>
  {holding_rows}
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "① PULSO EJECUTIVO",
        "Pulso Ejecutivo",
        f"Calificación actual: {score:.2f}% · {icgit.get('avep','Transición Crítica')} · Proyección 2026: {proj:.2f}% · Corte ene–mar 2026",
        f'<span class="badge badge-{"green" if score>=70 else "amber" if score>=50 else "red"}">{icgit.get("avep_emoji","🟡")} {icgit.get("avep","")}</span>',
    )

    html = hdr + alertas_html + cong_html + riesgo_op + holding_html

    render_page(html, show_tech=show_tech, height=950)

    # ── CTAs Streamlit ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · ¿Qué hacemos esta semana?",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "Soy el alcalde de Montecristi. Mirando el pulso ejecutivo Q1-2026 "
                "(ICGI-T 53.56%, 2 SATs críticas, PSG 12.83%), "
                "¿cuáles son las 3 acciones más urgentes que debo tomar esta semana?"
            )
            st.rerun()
    with c2:
        if st.button("📊 Ver Causas de la Brecha", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c3:
        if st.button("🎯 Ver Metas del Plan Cantonal", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
