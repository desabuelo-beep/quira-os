"""
QUIRA OS v0.1 — P-19 Género y Equidad
PSG 12.83% · ODS 5 · Gender Bond · Pin Morado · Plan género
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# ── PROGRAMAS POA CON PERSPECTIVA DE GÉNERO ───────────────────────────────────
PROGRAMAS_GENERO = [
    {
        "programa": "Patronato Municipal · Grupos vulnerables",
        "monto": 380_000, "pct_genero": 100, "vinculo_psg": True,
        "estado": "OK",
        "nota": "Programas mujer-jefe-hogar, adulto mayor, discapacidad",
    },
    {
        "programa": "Luminarias seguridad Aníbal San Andrés",
        "monto": 95_000, "pct_genero": 80, "vinculo_psg": True,
        "estado": "BLOQUEADO",
        "nota": "Gov Twin activo · requiere PSG ≥30% para Gender Bond",
    },
    {
        "programa": "Formación liderazgo femenino parroquial",
        "monto": 18_000, "pct_genero": 100, "vinculo_psg": True,
        "estado": "PARCIAL",
        "nota": "2 de 7 parroquias · Isabel Muentes y Aníbal SA sin cobertura",
    },
    {
        "programa": "Infraestructura agua Isabel Muentes",
        "monto": 140_000, "pct_genero": 60, "vinculo_psg": True,
        "estado": "CRÍTICO",
        "nota": "Mujeres rurales = 68% de la carga de acarreo de agua",
    },
    {
        "programa": "Espacios seguros niñez y adolescencia",
        "monto": 45_000, "pct_genero": 70, "vinculo_psg": True,
        "estado": "PARCIAL",
        "nota": "Centro cabecera operativo · parroquias rurales sin cobertura",
    },
    {
        "programa": "Vialidad Av. Eloy Alfaro (tramo 3)",
        "monto": 210_000, "pct_genero": 20, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Vinculable a género si incluye iluminación y accesibilidad",
    },
    {
        "programa": "Residuos sólidos EP Aseo",
        "monto": 480_000, "pct_genero": 15, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Potencial: empleo femenino + separación en origen domiciliario",
    },
    {
        "programa": "Digitalización trámites DTIC",
        "monto": 85_000, "pct_genero": 10, "vinculo_psg": False,
        "estado": "NORMAL",
        "nota": "Potencial: trámites accesibles desde hogar para cuidadoras",
    },
]

_total_poa = 26_689_147
_total_genero_actual = sum(
    p["monto"] * (p["pct_genero"] / 100) for p in PROGRAMAS_GENERO if p["vinculo_psg"]
)
_psg_actual  = 12.83
_psg_meta    = 30.0
_psg_brecha  = _psg_meta - _psg_actual

# Proyección si se reclasifican los programas potenciales
_total_genero_potencial = sum(
    p["monto"] * (p["pct_genero"] / 100) for p in PROGRAMAS_GENERO
)
_psg_potencial = (_total_genero_potencial / _total_poa) * 100


def _prog_row(p: dict) -> str:
    col = {"OK": "green", "PARCIAL": "amber", "BLOQUEADO": "red", "CRÍTICO": "red", "NORMAL": "muted"}.get(p["estado"], "muted")
    badge = {
        "OK":       '<span class="badge badge-green">OK</span>',
        "PARCIAL":  '<span class="badge badge-amber">PARCIAL</span>',
        "BLOQUEADO":'<span class="badge badge-red">BLOQUEADO</span>',
        "CRÍTICO":  '<span class="badge badge-red">CRÍTICO</span>',
        "NORMAL":   '<span class="badge badge-cyan">POTENCIAL</span>',
    }.get(p["estado"], "")
    aporte = p["monto"] * (p["pct_genero"] / 100)
    pct_bar = min(p["pct_genero"], 100)
    psg_ico = "💜" if p["vinculo_psg"] else "⬜"
    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:9px;
              padding:11px 13px;margin-bottom:7px">
    <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:5px;gap:8px">
      <div style="display:flex;align-items:center;gap:6px;flex:1;flex-wrap:wrap">
        <span style="font-size:12px">{psg_ico}</span>
        <span style="font-size:11px;font-weight:700;color:var(--white)">{p["programa"]}</span>
        {badge}
      </div>
      <div style="text-align:right;flex-shrink:0">
        <div style="font-size:13px;font-weight:800;color:var(--{'purple' if p['vinculo_psg'] else 'muted'});
                    font-family:var(--mono)">${aporte:,.0f}</div>
        <div style="font-size:8px;color:var(--muted)">{p["pct_genero"]}% género</div>
      </div>
    </div>
    <div style="height:4px;background:var(--divider);border-radius:2px;
                overflow:hidden;margin-bottom:5px">
      <div style="height:4px;width:{pct_bar:.0f}%;
                  background:{'#7C5CFC' if p['vinculo_psg'] else '#444'};
                  border-radius:2px"></div>
    </div>
    <div style="font-size:9px;color:var(--muted)">{p["nota"]}</div>
  </div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    indices   = data["indices"]
    psg_val   = indices.get("PSG", {}).get("valor", _psg_actual)

    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(124,92,252,.1);border:1px solid rgba(124,92,252,.35);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--purple);
                font-family:var(--mono)">{psg_val:.2f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--purple);margin-top:4px">PSG ACTUAL</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Ruptura Sistémica</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{_psg_meta:.0f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">META PDOT 2027</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Desbloquea Gender Bond</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{_psg_brecha:.2f}<span style="font-size:18px">pts</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">BRECHA PSG</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Vs meta mínima 30%</div>
  </div>
  <div style="background:rgba(124,92,252,.08);border:1px solid rgba(124,92,252,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--purple);
                font-family:var(--mono)">${(_total_genero_potencial/1000):.0f}K</div>
    <div style="font-size:10px;font-weight:700;color:var(--purple);margin-top:4px">POA RECLASIFICABLE</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">PSG potencial {_psg_potencial:.1f}%</div>
  </div>
</div>"""

    gender_bond_html = f"""
<div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.3);
            border-radius:12px;padding:14px 16px;margin-bottom:16px;
            display:flex;align-items:flex-start;gap:14px">
  <div style="font-size:32px;flex-shrink:0">💜</div>
  <div style="flex:1">
    <div style="font-size:12px;font-weight:700;color:var(--purple);margin-bottom:6px">
      BID Lab GENDER BOND · $95,000 · BLOQUEADO · Vence Q3-2026
    </div>
    <div style="font-size:11px;color:var(--muted);line-height:1.7;margin-bottom:8px">
      El Gender Bond financia luminarias de seguridad en Aníbal San Andrés
      (Pin Morado activo · Gov Twin aprobado). Está <strong style="color:var(--red)">bloqueado</strong>
      porque el BID Lab exige PSG ≥ 30%. Con PSG actual 12.83%, la brecha es
      <strong style="color:var(--purple)">{_psg_brecha:.2f} puntos</strong>.
      Si no se alcanza antes de Q3-2026, el fondo <strong style="color:var(--red)">vence</strong>
      y debe recompetir en la siguiente convocatoria (2027).
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <div style="padding:6px 12px;background:rgba(124,92,252,.12);border-radius:7px;
                  font-size:10px;color:var(--purple)">
        Reclasificar 3 programas POA → PSG sube a ~{_psg_potencial:.1f}%
      </div>
      <div style="padding:6px 12px;background:rgba(0,212,255,.08);border-radius:7px;
                  font-size:10px;color:var(--cyan)">
        Acción legal bajo COOTAD Art. 55 lit. c · no requiere reforma presupuestaria
      </div>
    </div>
  </div>
</div>"""

    plan_reclasificacion_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">💜 PLAN RECLASIFICACIÓN POA · PSG {psg_val:.2f}% → {_psg_potencial:.1f}%</div>
  <div style="font-size:10px;color:var(--muted);margin-bottom:10px;
              padding:6px 10px;background:rgba(124,92,252,.05);
              border-radius:6px;border:1px solid rgba(124,92,252,.15)">
    La reclasificación de partidas presupuestarias con perspectiva de género
    no requiere reforma presupuestaria — solo un informe técnico DAF + resolución Alcaldía.
    El PDOT ya vincula estos programas con ODS 5. Plazo estimado: 15 días hábiles.
  </div>
  {"".join(_prog_row(p) for p in PROGRAMAS_GENERO)}
  <div style="margin-top:10px;padding:8px 10px;
              background:rgba(124,92,252,.05);border:1px solid rgba(124,92,252,.15);
              border-radius:7px;font-size:10px;color:var(--purple)">
    💜 PSG actual: {psg_val:.2f}% ·
    Con reclasificación potencial: {_psg_potencial:.1f}% ·
    Meta Gender Bond: ≥30% · Meta ONU Mujeres: ≥25%
  </div>
</div>"""

    hoja_ruta_html = """
<div class="grid-2">
  <div style="background:rgba(124,92,252,.06);border:1px solid rgba(124,92,252,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--purple);margin-bottom:8px">
      💜 HOJA DE RUTA PSG · 30 DÍAS
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 1-5:</strong> Informe técnico DAF · identificar partidas reclasificables
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 6-10:</strong> Resolución Alcaldía · reforma interna POA
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 11-15:</strong> Registro eSIGEF · PSG recalculado ≥20%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        <strong style="color:var(--purple)">Días 16-30:</strong> Ampliar programas género · PSG ≥30% · Gender Bond
      </div>
    </div>
  </div>
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:8px">
      ✅ BENEFICIOS DE ALCANZAR PSG ≥ 30%
    </div>
    <div style="display:flex;flex-direction:column;gap:5px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        💜 Gender Bond BID Lab $95K · luminarias Aníbal San Andrés desbloqueadas
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        🌐 ONU Mujeres Municipio Igualitario $65K · elegibilidad activa
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        📈 ODS 5 pasa de CRÍTICO a PARCIAL · ICODS sube a ~90%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        🏆 Sello igualdad ONU Mujeres · diferenciador político para 2027
      </div>
    </div>
  </div>
</div>"""

    hdr = page_header(
        "⑮ GÉNERO Y EQUIDAD",
        "PSG · ODS 5 · Gender Bond",
        f"PSG {psg_val:.2f}% · Brecha {_psg_brecha:.2f} pts · Gender Bond $95K bloqueado · ONU Mujeres",
        '<span class="badge badge-red">💜 PSG Ruptura Sistémica</span>',
    )

    render_page(
        hdr + resumen_html + gender_bond_html + plan_reclasificacion_html + hoja_ruta_html,
        show_tech=show_tech, height=1400,
    )

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Plan reclasificación PSG",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El PSG de Montecristi es 12.83%. El Gender Bond BID Lab $95K "
                "y ONU Mujeres $65K están bloqueados por este indicador. "
                "La reclasificación de partidas en el POA podría elevar el PSG a ~16%. "
                "¿Cuál es el procedimiento legal exacto bajo COOTAD y el reglamento SINFÍN "
                "para reclasificar partidas presupuestarias con perspectiva de género, "
                "quién firma la resolución y cuánto tiempo toma el registro en eSIGEF?"
            )
            st.rerun()
    with c2:
        if st.button("💸 Ver Cooperación Internacional", use_container_width=True):
            st.session_state["page"] = "cooperacion"
            st.rerun()
    with c3:
        if st.button("🌐 Ver ODS Tracker", use_container_width=True):
            st.session_state["page"] = "ods"
            st.rerun()
