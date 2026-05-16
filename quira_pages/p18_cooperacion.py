"""
QUIRA OS v0.1 — P-18 Cooperación Internacional
Fondos disponibles · BID · CAF · PNUD · ONU Mujeres · GEF
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── PORTAFOLIO DE COOPERACIÓN ─────────────────────────────────────────────────
FONDOS = [
    {
        "fondo": "PNUD Agua Rural",
        "cooperante": "PNUD Ecuador",
        "monto": 2_400_000,
        "ods": ["ODS 6", "ODS 10"],
        "estado": "ELEGIBLE",
        "color": "cyan",
        "req_pendiente": "Calificación ≥ 55% (actual 53.56%) · brecha: 1.44 pts",
        "deadline": "Q3-2026",
        "score_elegib": 81,
        "descripcion": "Sistema integral agua potable Isabel Muentes · 3,488 hab.",
        "contraparte": "Infraestructura hidráulica + diseño + fiscalización GAD",
    },
    {
        "fondo": "GEF Fondo Verde Clima",
        "cooperante": "GEF / MAATE Ecuador",
        "monto": 180_000,
        "ods": ["ODS 13", "ODS 15"],
        "estado": "LISTO",
        "color": "green",
        "req_pendiente": "Ninguno · elegible ahora · dMRV preparado",
        "deadline": "Q2-2026",
        "score_elegib": 94,
        "descripcion": "Reforestación 500 ha laderas Colorado · carbono dMRV",
        "contraparte": "Plantas nativas + técnico forestal + transporte GAD",
    },
    {
        "fondo": "BID Lab Gender Bond",
        "cooperante": "BID Lab",
        "monto": 95_000,
        "ods": ["ODS 5", "ODS 11"],
        "estado": "BLOQUEADO",
        "color": "red",
        "req_pendiente": "PSG ≥ 30% (actual 12.83%) · brecha: 17.17 pts",
        "deadline": "Q3-2026 (vence)",
        "score_elegib": 38,
        "descripcion": "Luminarias seguridad · Aníbal San Andrés · Pin Morado activo",
        "contraparte": "Postes + instalación eléctrica + diseño GAD",
    },
    {
        "fondo": "CAF Ciudades Sostenibles",
        "cooperante": "CAF Banco Desarrollo",
        "monto": 1_200_000,
        "ods": ["ODS 11", "ODS 9"],
        "estado": "EN GESTIÓN",
        "color": "amber",
        "req_pendiente": "ISP ≥ 40% + ITAM ≥ 65% + carta intención Alcaldía",
        "deadline": "Q4-2026",
        "score_elegib": 52,
        "descripcion": "Vialidad urbana + digitalización trámites + smart city básico",
        "contraparte": "Cofinanciamiento 30% GAD + plan mantenimiento 5 años",
    },
    {
        "fondo": "ONU Mujeres · Municipio Igualitario",
        "cooperante": "ONU Mujeres Ecuador",
        "monto": 65_000,
        "ods": ["ODS 5", "ODS 16"],
        "estado": "BLOQUEADO",
        "color": "red",
        "req_pendiente": "PSG ≥ 25% + Plan género aprobado + designar punto focal",
        "deadline": "Permanente · convocatoria anual",
        "score_elegib": 31,
        "descripcion": "Sellos igualdad · formación funcionarios · presupuesto sensible",
        "contraparte": "Designar coordinadora género + 0.5 FTE Patronato",
    },
    {
        "fondo": "BDE Crédito Reactivación",
        "cooperante": "Banco Desarrollo Ecuador",
        "monto": 3_500_000,
        "ods": ["ODS 11", "ODS 8"],
        "estado": "BLOQUEADO",
        "color": "red",
        "req_pendiente": "ISP ≥ 65% (actual 14.58%) · sin deuda coactiva pendiente",
        "deadline": "Permanente · ventanilla abierta",
        "score_elegib": 18,
        "descripcion": "Crédito inversión infraestructura 10 años · tasa preferencial",
        "contraparte": "Garantía soberana + plan pago certificado DAF",
    },
]

_total_disponible = sum(f["monto"] for f in FONDOS if f["estado"] == "LISTO")
_total_elegible   = sum(f["monto"] for f in FONDOS if f["estado"] in ("ELEGIBLE", "LISTO"))
_total_bloqueado  = sum(f["monto"] for f in FONDOS if f["estado"] == "BLOQUEADO")
_total_gestion    = sum(f["monto"] for f in FONDOS if f["estado"] == "EN GESTIÓN")


def _fondo_card(f: dict) -> str:
    col   = f["color"]
    estado_map = {
        "LISTO":      '<span class="badge badge-green">✅ LISTO</span>',
        "ELEGIBLE":   '<span class="badge badge-cyan">🔵 ELEGIBLE</span>',
        "EN GESTIÓN": '<span class="badge badge-amber">⏳ EN GESTIÓN</span>',
        "BLOQUEADO":  '<span class="badge badge-red">🔴 BLOQUEADO</span>',
    }
    badge    = estado_map.get(f["estado"], "")
    ods_tags = " ".join(
        f'<span style="font-size:8px;color:var(--cyan);background:rgba(0,212,255,.1);'
        f'border-radius:4px;padding:2px 5px">{o}</span>'
        for o in f["ods"]
    )
    pct = min(f["score_elegib"], 100)

    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-left:4px solid var(--{col});border-radius:12px;
            padding:16px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;
              margin-bottom:8px;gap:10px">
    <div style="flex:1">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px">
        <span style="font-size:12px;font-weight:800;color:var(--white)">{f["fondo"]}</span>
        {badge}
      </div>
      <div style="font-size:10px;color:var(--muted)">{f["cooperante"]} · {ods_tags}</div>
    </div>
    <div style="text-align:right;flex-shrink:0">
      <div style="font-size:20px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">${f["monto"]/1000:.0f}K</div>
      <div style="font-size:9px;color:var(--muted)">Plazo: {f["deadline"]}</div>
    </div>
  </div>

  <!-- Elegibilidad bar -->
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">
    <div style="font-size:9px;color:var(--muted);min-width:75px">Elegibilidad</div>
    <div style="flex:1;height:5px;background:var(--divider);border-radius:3px;overflow:hidden">
      <div style="height:5px;width:{pct:.0f}%;background:var(--{col});border-radius:3px"></div>
    </div>
    <div style="font-size:11px;font-weight:700;color:var(--{col});
                font-family:var(--mono);min-width:32px">{pct}%</div>
  </div>

  <div style="font-size:10px;color:var(--muted);margin-bottom:5px">{f["descripcion"]}</div>
  <div style="font-size:10px;color:var(--{'red' if f['estado']=='BLOQUEADO' else 'amber' if f['estado']=='EN GESTIÓN' else 'cyan'})">
    {'🔴' if f['estado']=='BLOQUEADO' else '⚠️' if f['estado']=='EN GESTIÓN' else '🔵'}
    {f["req_pendiente"]}
  </div>
</div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--green);
                font-family:var(--mono)">${_total_disponible/1000:.0f}K</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">DISPONIBLE HOY</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">GEF elegible ahora</div>
  </div>
  <div style="background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--cyan);
                font-family:var(--mono)">${_total_elegible/1_000_000:.1f}M</div>
    <div style="font-size:10px;font-weight:700;color:var(--cyan);margin-top:4px">POTENCIAL Q3</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Elegible + listo</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--red);
                font-family:var(--mono)">${_total_bloqueado/1_000_000:.1f}M</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">BLOQUEADO</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">ISP + PSG críticos</div>
  </div>
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">${(_total_disponible+_total_elegible+_total_bloqueado+_total_gestion)/1_000_000:.1f}M</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">PORTAFOLIO TOTAL</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">6 fuentes identificadas</div>
  </div>
</div>"""

    desbloqueo_html = """
<div style="background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.2);
            border-radius:12px;padding:14px 16px;margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:var(--cyan);margin-bottom:10px">
    🔑 LLAVES MAESTRAS · 2 acciones desbloquean $3.76M
  </div>
  <div class="grid-2" style="gap:12px">
    <div style="padding:10px;background:rgba(255,77,109,.06);border-radius:8px">
      <div style="font-size:10px;font-weight:700;color:var(--red);margin-bottom:4px">
        ISP 14.58% → 65% (umbral COOTAD)
      </div>
      <div style="font-size:10px;color:var(--muted)">
        Desbloquea: BDE $3.5M · mejora perfil CAF · permite crédito reactivación
      </div>
    </div>
    <div style="padding:10px;background:rgba(124,92,252,.08);border-radius:8px">
      <div style="font-size:10px;font-weight:700;color:var(--purple);margin-bottom:4px">
        PSG 12.83% → 30% (meta PDOT)
      </div>
      <div style="font-size:10px;color:var(--muted)">
        Desbloquea: Gender Bond $95K · ONU Mujeres $65K · sellos igualdad
      </div>
    </div>
  </div>
</div>"""

    fondos_html = f"""
<div class="card">
  <div class="card-title">💸 PORTAFOLIO DE COOPERACIÓN · 6 FUENTES · ene–mar 2026</div>
  {"".join(_fondo_card(f) for f in FONDOS)}
</div>"""

    hdr = page_header(
        "⑭ COOPERACIÓN INTERN.",
        "Fondos Internacionales",
        f"${(_total_disponible+_total_elegible)/1_000_000:.1f}M elegibles · ${_total_bloqueado/1_000_000:.1f}M bloqueados · 6 fuentes",
        '<span class="badge badge-green">✅ GEF listo ahora</span>',
    )

    render_page(hdr + resumen_html + desbloqueo_html + fondos_html,
                show_tech=show_tech, height=1300)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Estrategia de fondos",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "Montecristi tiene un portafolio de cooperación de $7.44M. "
                "El GEF $180K está listo ya. El PNUD $2.4M requiere ICGI-T ≥55% (brecha 1.44 pts). "
                "El Gender Bond $95K y ONU Mujeres $65K requieren PSG ≥25-30% (actual 12.83%). "
                "El BDE $3.5M requiere ISP ≥65% (actual 14.58%). "
                "¿Cuál es la hoja de ruta de 6 meses para maximizar el monto captado, "
                "en qué orden priorizar las gestiones y qué unidad interna debe liderar cada fondo?"
            )
            st.rerun()
    with c2:
        if st.button("🌐 Ver Agenda 2030 · ODS", use_container_width=True):
            st.session_state["page"] = "ods"
            st.rerun()
    with c3:
        if st.button("💰 Ver Inversión por Habitante", use_container_width=True):
            st.session_state["page"] = "inversion"
            st.rerun()
