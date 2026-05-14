"""
QUIRA OS v0.1 — P-14 Eficiencia por Dirección
IED 33.99% · 12 Direcciones GAD · Ranking operativo
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── 12 DIRECCIONES GAD · SIAP-ICPI Q1-2026 ───────────────────────────────────
DIRECCIONES = [
    {"id": "DJUR",  "nombre": "Dirección Jurídica",             "score": 68.4, "sat": False, "procesos": 18, "nota": "Contratos revisados · asesoría legal activa"},
    {"id": "DSOC",  "nombre": "Dirección Desarrollo Social",    "score": 62.1, "sat": False, "procesos": 24, "nota": "Patronato alineado · programas vulnerables OK"},
    {"id": "DAF",   "nombre": "Dirección Administrativa Fin.",  "score": 55.3, "sat": True,  "procesos": 31, "nota": "ISP 14.58% · coactivas pendientes · 5 sin SHA-256"},
    {"id": "DPM",   "nombre": "Dirección de Planificación",     "score": 51.2, "sat": True,  "procesos": 22, "nota": "4 metas PDOT sin PAC · PDOT actualización pendiente"},
    {"id": "DGA",   "nombre": "Dirección Gestión Ambiental",    "score": 48.7, "sat": False, "procesos": 12, "nota": "GEF elegible · plan residuos sin aprobar"},
    {"id": "DGOV",  "nombre": "Dirección de Gobernanza",        "score": 41.5, "sat": False, "procesos": 9,  "nota": "IGP 27.98% · 2 parroquias sin voz activa"},
    {"id": "DAPS",  "nombre": "Dir. Administrativa y Servicios","score": 38.2, "sat": True,  "procesos": 28, "nota": "6 procesos sin SHA-256 · PAC desactualizado"},
    {"id": "DCOM",  "nombre": "Dirección de Comunicación",      "score": 35.7, "sat": False, "procesos": 8,  "nota": "LOTAIP parcial · portal 48% contenido desactualizado"},
    {"id": "DGAD",  "nombre": "Dir. Atención Ciudadana",        "score": 29.8, "sat": False, "procesos": 15, "nota": "Tiempo respuesta 8.2 días vs meta 3 días"},
    {"id": "DOBS",  "nombre": "Dirección de Obras Públicas",    "score": 26.5, "sat": True,  "procesos": 42, "nota": "8 procesos sin SHA-256 · Isabel Muentes paralizada"},
    {"id": "DTUR",  "nombre": "Dirección Turismo y Cultura",    "score": 22.4, "sat": False, "procesos": 6,  "nota": "Sin plan turismo · UNESCO sin activar · presupuesto 0"},
    {"id": "DTIC",  "nombre": "Dirección TIC",                  "score": 18.3, "sat": False, "procesos": 5,  "nota": "Digitalización trámites 12% · portal offline 18%"},
]

# Ordenar de mayor a menor score
DIRECCIONES_SORTED = sorted(DIRECCIONES, key=lambda x: x["score"], reverse=True)


def _dir_row(d: dict, rank: int) -> str:
    s   = d["score"]
    col = "green" if s >= 60 else "amber" if s >= 40 else "red"
    pct = min(s, 100)
    sat_badge = (
        '<span style="font-size:8px;font-weight:700;color:var(--red);'
        'background:rgba(255,77,109,.15);border:1px solid rgba(255,77,109,.3);'
        'border-radius:4px;padding:1px 5px;margin-left:6px">SAT</span>'
        if d["sat"] else ""
    )
    rank_col = "cyan" if rank <= 3 else "muted" if rank <= 8 else "red"
    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:9px;
              padding:12px 14px;margin-bottom:8px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
      <div style="font-size:11px;font-weight:900;color:var(--{rank_col});
                  font-family:var(--mono);min-width:22px">#{rank}</div>
      <div style="flex:1">
        <span style="font-size:11px;font-weight:700;color:var(--white)">{d["id"]}</span>
        <span style="font-size:10px;color:var(--muted);margin-left:6px">{d["nombre"]}</span>
        {sat_badge}
      </div>
      <div style="font-size:16px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">{s:.1f}%</div>
    </div>
    <div style="height:5px;background:var(--divider);border-radius:3px;
                overflow:hidden;margin-bottom:6px">
      <div style="height:5px;width:{pct:.0f}%;background:var(--{col});border-radius:3px"></div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div style="font-size:9px;color:var(--muted)">{d["nota"]}</div>
      <div style="font-size:9px;color:var(--muted);flex-shrink:0;margin-left:8px">
        {d["procesos"]} procesos
      </div>
    </div>
  </div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    indices   = data["indices"]
    ied_val   = indices.get("IED", {}).get("valor", 33.99)

    n_crit = sum(1 for d in DIRECCIONES if d["score"] < 30)
    n_ok   = sum(1 for d in DIRECCIONES if d["score"] >= 60)
    n_sat  = sum(1 for d in DIRECCIONES if d["sat"])

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{ied_val:.1f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">IED GLOBAL</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Gestión por Ocurrencia</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{n_ok}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">DIRS. SOBRE 60%</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Gestión por Mandato</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{n_crit}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">DIRS. CRÍTICAS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Bajo 30% · riesgo alto</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{n_sat}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">DIRS. CON SAT</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Alerta activa en dirección</div>
  </div>
</div>"""

    ranking_html = f"""
<div class="card">
  <div class="card-title">📋 RANKING 12 DIRECCIONES GAD · IED Q1-2026 (mayor→menor)</div>
  {"".join(_dir_row(d, i+1) for i, d in enumerate(DIRECCIONES_SORTED))}
  <div style="font-size:9px;color:var(--muted);margin-top:8px;padding-top:8px;
              border-top:1px solid rgba(255,255,255,.05)">
    📌 IED = Índice de Eficiencia Direccional · Modelo SIAP-ICPI v1.0222
    · SAT = Dirección con alerta activa vinculada · 12 dirs. evaluadas Q1-2026
  </div>
</div>"""

    plan_html = """
<div class="grid-2" style="margin-top:16px">
  <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:8px">
      🔴 FOCO INMEDIATO · Direcciones críticas
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(255,77,109,.07);border-radius:6px;margin-bottom:5px">
      DOBS 26.5% → Regularizar 8 SHA-256 + desbloquear Isabel Muentes
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(255,77,109,.07);border-radius:6px;margin-bottom:5px">
      DTUR 22.4% → Activar plan turismo UNESCO · presupuesto Q2
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(255,77,109,.07);border-radius:6px">
      DTIC 18.3% → Priorizar digitalización trámites · portal online 100%
    </div>
  </div>
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:8px">
      ✅ MEJOR PRÁCTICA · Replicar en todo el GAD
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(0,224,150,.07);border-radius:6px;margin-bottom:5px">
      DJUR 68.4% → Modelo de revisión contractual · exportar a DOBS
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(0,224,150,.07);border-radius:6px;margin-bottom:5px">
      DSOC 62.1% → Patronato alineado · protocolo de seguimiento mensual
    </div>
    <div style="font-size:11px;color:var(--white);padding:6px 10px;
                background:rgba(0,224,150,.07);border-radius:6px">
      Meta IED Q3-2026: 50% → requiere +16 pts · plan 90 días activado
    </div>
  </div>
</div>"""

    hdr = page_header(
        "⑩ EFICIENCIA DIRECCIONAL",
        "Ranking 12 Direcciones · IED",
        f"IED Global {ied_val:.2f}% · {n_ok} dirs sobre 60% · {n_crit} críticas · {n_sat} con SAT activa",
        '<span class="badge badge-amber">Gestión por Ocurrencia</span>',
    )

    render_page(hdr + resumen_html + ranking_html + plan_html,
                show_tech=show_tech, height=1200)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Plan 90 días IED", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El IED de Montecristi es 33.99%. Las 3 direcciones más críticas son "
                "DTIC 18.3% (digitalización), DTUR 22.4% (turismo UNESCO sin activar) "
                "y DOBS 26.5% (obras bloqueadas, 8 procesos sin SHA-256). "
                "¿Qué plan de 90 días con acciones semanales específicas elevaría "
                "el IED global a 50% antes del cierre Q3-2026?"
            )
            st.rerun()
    with c2:
        if st.button("🔗 Ver Cadena POA·PAC", use_container_width=True):
            st.session_state["page"] = "cadena"
            st.rerun()
    with c3:
        if st.button("🚨 Ver Alertas SAT", use_container_width=True):
            st.session_state["page"] = "sat"
            st.rerun()
