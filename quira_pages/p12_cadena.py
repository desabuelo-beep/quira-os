"""
QUIRA OS v0.1 — P-12 Cadena POA·PAC
Trazabilidad operativa · POA→PAC→SERCOP→eSIGEF · SAT-0
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── 4 METAS SIN CONTRATO PAC (SAT-0) ─────────────────────────────────────────
METAS_SIN_PAC = [
    {
        "id": "POA-06-12",
        "nombre": "Red agua potable Isabel Muentes · Fase 1",
        "eje": "Servicios Básicos",
        "presupuesto": "$380,000",
        "poa_ok": True, "pac_ok": False, "sercop_ok": False, "esigef_ok": False,
        "corte": "Alerta operativa activa · sin proceso SERCOP publicado",
        "riesgo": "Riesgo observación Contraloría + bloqueo PNUD",
    },
    {
        "id": "POA-03-07",
        "nombre": "Mejoramiento vial Av. Eloy Alfaro – tramo 3",
        "eje": "Vialidad",
        "presupuesto": "$210,000",
        "poa_ok": True, "pac_ok": False, "sercop_ok": False, "esigef_ok": False,
        "corte": "PAC aprobado sin adjudicación · proceso desierto Q1",
        "riesgo": "Meta PDOT M-03 en riesgo · vías 53% sin avance",
    },
    {
        "id": "POA-09-04",
        "nombre": "Luminarias seguridad Aníbal San Andrés",
        "eje": "Seguridad",
        "presupuesto": "$95,000",
        "poa_ok": True, "pac_ok": False, "sercop_ok": False, "esigef_ok": False,
        "corte": "Proceso detenido · vinculado a Gender Bond pendiente",
        "riesgo": "ODS 5 + ODS 16 en riesgo · brecha significativa en equidad de gasto",
    },
    {
        "id": "POA-11-02",
        "nombre": "Centro comunitario La Pila – ampliación",
        "eje": "Equipamiento",
        "presupuesto": "$145,000",
        "poa_ok": True, "pac_ok": True, "sercop_ok": False, "esigef_ok": False,
        "corte": "Especificaciones técnicas en revisión · no publicado SERCOP",
        "riesgo": "Desvío de meta participativa · alerta relacionada",
    },
]

# ── 24 PROCESOS SIN SHA-256 (Gasto Ciego C4) ─────────────────────────────────
GASTO_CIEGO = [
    {"dir": "DOBS (Obras)",       "procesos": 8, "monto": "$1,240,000"},
    {"dir": "DAPS (Servicios)",   "procesos": 6, "monto": "$890,000"},
    {"dir": "DAF (Financiero)",   "procesos": 5, "monto": "$620,000"},
    {"dir": "DPM (Planificación)","procesos": 3, "monto": "$410,000"},
    {"dir": "Otras 8 dirs.",      "procesos": 2, "monto": "$280,000"},
]


def _nodo(label: str, ok: bool, alert: bool = False) -> str:
    if ok:
        bg  = "rgba(0,224,150,.12)"
        brd = "rgba(0,224,150,.4)"
        col = "var(--green)"
        ico = "✅"
    elif alert:
        bg  = "rgba(255,184,0,.1)"
        brd = "rgba(255,184,0,.4)"
        col = "var(--amber)"
        ico = "⚠️"
    else:
        bg  = "rgba(255,77,109,.1)"
        brd = "rgba(255,77,109,.4)"
        col = "var(--red)"
        ico = "❌"
    return (
        f'<div style="background:{bg};border:2px solid {brd};border-radius:12px;'
        f'padding:14px 18px;text-align:center;min-width:120px">'
        f'<div style="font-size:22px">{ico}</div>'
        f'<div style="font-size:13px;font-weight:800;color:{col};margin-top:5px'
        f';letter-spacing:.04em">{label}</div>'
        f'</div>'
    )


def _arrow(broken: bool = False) -> str:
    col = "rgba(255,77,109,.5)" if broken else "rgba(255,255,255,.2)"
    txt = "✂" if broken else "→"
    return (
        f'<div style="display:flex;align-items:center;justify-content:center;'
        f'min-width:32px;font-size:18px;color:{col};font-weight:900">{txt}</div>'
    )


def _meta_cadena(m: dict) -> str:
    """Cadena visual POA→PAC→SERCOP→eSIGEF para una meta."""
    poa_n  = _nodo("POA",    m["poa_ok"])
    pac_n  = _nodo("PAC",    m["pac_ok"],    alert=m["poa_ok"] and not m["pac_ok"])
    ser_n  = _nodo("SERCOP", m["sercop_ok"], alert=m["pac_ok"] and not m["sercop_ok"])
    sig_n  = _nodo("eSIGEF", m["esigef_ok"], alert=m["sercop_ok"] and not m["esigef_ok"])
    a1 = _arrow(broken=not m["pac_ok"])
    a2 = _arrow(broken=not m["sercop_ok"])
    a3 = _arrow(broken=not m["esigef_ok"])

    return f"""
  <div style="background:var(--navy-card);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:14px 16px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                margin-bottom:10px;gap:10px">
      <div>
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:9px;font-weight:700;color:var(--muted);
                       background:rgba(255,255,255,.05);border-radius:4px;
                       padding:2px 6px">{m["id"]}</span>
          <span style="font-size:9px;color:var(--cyan)">{m["eje"]}</span>
        </div>
        <div style="font-size:12px;font-weight:700;color:var(--white);
                    margin-top:3px">{m["nombre"]}</div>
      </div>
      <div style="font-size:12px;font-weight:700;color:var(--amber);
                  font-family:var(--mono);flex-shrink:0">{m["presupuesto"]}</div>
    </div>
    <!-- Cadena visual -->
    <div style="display:flex;align-items:center;gap:4px;margin-bottom:10px;
                overflow-x:auto;padding-bottom:4px">
      {poa_n}{a1}{pac_n}{a2}{ser_n}{a3}{sig_n}
    </div>
    <!-- Estado y riesgo -->
    <div style="font-size:10px;color:var(--amber);padding:5px 8px;
                background:rgba(255,184,0,.06);border-radius:5px;margin-bottom:5px">
      ⚠️ {m["corte"]}
    </div>
    <div style="font-size:10px;color:var(--red)">
      🔴 Riesgo: {m["riesgo"]}
    </div>
  </div>"""


def _gc_row(g: dict) -> str:
    pct = min((g["procesos"] / 24) * 100, 100)
    return f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
  <div style="min-width:130px;font-size:10px;color:var(--white)">{g["dir"]}</div>
  <div style="flex:1;height:6px;background:var(--divider);border-radius:3px;overflow:hidden">
    <div style="height:6px;width:{pct:.0f}%;background:var(--red);border-radius:3px"></div>
  </div>
  <div style="font-size:11px;font-weight:700;color:var(--red);
              font-family:var(--mono);min-width:25px">{g["procesos"]}</div>
  <div style="font-size:10px;color:var(--muted);min-width:70px;
              text-align:right">{g["monto"]}</div>
</div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    # ── FLUJO MASTER ──────────────────────────────────────────────────────────
    flujo_html = """
<div class="card" style="margin-bottom:16px">
  <div class="card-title">🔗 CADENA OPERATIVA COMPLETA · POA → PAC → SERCOP → eSIGEF</div>
  <div style="display:flex;align-items:center;gap:6px;padding:12px 0;
              overflow-x:auto;flex-wrap:nowrap">

    <div style="background:rgba(0,212,255,.1);border:2px solid rgba(0,212,255,.4);
                border-radius:12px;padding:16px 22px;text-align:center;min-width:130px;flex-shrink:0">
      <div style="font-size:26px">📋</div>
      <div style="font-size:14px;font-weight:800;color:var(--cyan);margin-top:4px">POA</div>
      <div style="font-size:10px;color:var(--muted)">Plan Operativo</div>
      <div style="font-size:10px;color:var(--green);margin-top:4px">48 metas activas</div>
    </div>

    <div style="font-size:22px;color:rgba(255,255,255,.3);font-weight:900;flex-shrink:0">→</div>

    <div style="background:rgba(255,184,0,.1);border:2px solid rgba(255,77,109,.5);
                border-radius:12px;padding:16px 22px;text-align:center;min-width:130px;
                position:relative;flex-shrink:0">
      <div style="position:absolute;top:-11px;left:50%;transform:translateX(-50%);
                  background:var(--red);color:white;font-size:9px;font-weight:700;
                  padding:2px 8px;border-radius:4px;white-space:nowrap">4 cortes con alerta</div>
      <div style="font-size:26px">📁</div>
      <div style="font-size:14px;font-weight:800;color:var(--amber);margin-top:4px">PAC</div>
      <div style="font-size:10px;color:var(--muted)">Plan Anual Compras</div>
      <div style="font-size:10px;color:var(--red);margin-top:4px">4 metas sin contrato</div>
    </div>

    <div style="font-size:22px;color:rgba(255,77,109,.5);font-weight:900;flex-shrink:0">✂</div>

    <div style="background:rgba(255,77,109,.08);border:2px solid rgba(255,77,109,.3);
                border-radius:12px;padding:16px 22px;text-align:center;min-width:130px;
                position:relative;flex-shrink:0">
      <div style="position:absolute;top:-11px;left:50%;transform:translateX(-50%);
                  background:var(--red);color:white;font-size:9px;font-weight:700;
                  padding:2px 8px;border-radius:4px;white-space:nowrap">24 sin SHA-256</div>
      <div style="font-size:26px">🔍</div>
      <div style="font-size:14px;font-weight:800;color:var(--red);margin-top:4px">SERCOP</div>
      <div style="font-size:10px;color:var(--muted)">Contratación pública</div>
      <div style="font-size:10px;color:var(--red);margin-top:4px">Gasto Ciego C4</div>
    </div>

    <div style="font-size:22px;color:rgba(255,77,109,.5);font-weight:900;flex-shrink:0">✂</div>

    <div style="background:rgba(255,77,109,.06);border:2px solid rgba(255,77,109,.2);
                border-radius:12px;padding:16px 22px;text-align:center;min-width:130px;flex-shrink:0">
      <div style="font-size:26px">💳</div>
      <div style="font-size:14px;font-weight:800;color:var(--red);margin-top:4px">eSIGEF</div>
      <div style="font-size:10px;color:var(--muted)">Devengado MF</div>
      <div style="font-size:10px;color:var(--red);margin-top:4px">No alcanzado</div>
    </div>

    <div style="font-size:22px;color:rgba(255,255,255,.3);font-weight:900;flex-shrink:0">→</div>

    <div style="background:rgba(255,77,109,.06);border:2px solid rgba(255,77,109,.2);
                border-radius:12px;padding:16px 22px;text-align:center;min-width:130px;flex-shrink:0">
      <div style="font-size:26px">📊</div>
      <div style="font-size:14px;font-weight:800;color:var(--red);margin-top:4px">Contraloría</div>
      <div style="font-size:10px;color:var(--muted)">Auditoría externa</div>
      <div style="font-size:10px;color:var(--red);margin-top:4px">Riesgo observación</div>
    </div>

  </div>

  <div style="margin-top:10px;padding:10px 12px;
              background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:8px;font-size:10px;color:var(--muted);line-height:1.6">
    🔴 <strong style="color:var(--red)">Alerta operativa activa:</strong>
    La cadena operativa tiene dos puntos de corte críticos:
    (1) <strong style="color:var(--white)">4 metas</strong> con POA aprobado pero
    sin contrato PAC activo · (2)
    <strong style="color:var(--white)">24 procesos</strong> sin evidencia digital
    SHA-256 = "Gasto Ciego C4" · riesgo de observación Contraloría.
  </div>
</div>"""

    # ── 4 METAS SIN PAC ───────────────────────────────────────────────────────
    metas_html = f"""
<div class="card">
  <div class="card-title">⚠️ 4 METAS PDOT SIN CONTRATO PAC · Alerta operativa · Detalle</div>
  {"".join(_meta_cadena(m) for m in METAS_SIN_PAC)}
</div>"""

    # ── GASTO CIEGO C4 ────────────────────────────────────────────────────────
    gc_rows = "".join(_gc_row(g) for g in GASTO_CIEGO)
    gc_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">🔴 GASTO CIEGO C4 · 24 procesos sin evidencia SHA-256</div>
  <div style="padding:10px 12px;background:rgba(255,77,109,.06);
              border:1px solid rgba(255,77,109,.2);border-radius:8px;
              font-size:11px;color:var(--muted);line-height:1.6;margin-bottom:12px">
    Cada proceso contractual debe tener un <strong style="color:var(--white)">hash SHA-256</strong>
    de las evidencias cargadas en el portal SERCOP (actas, especificaciones, informes).
    Sin este hash, el proceso no es auditable digitalmente — es "Gasto Ciego".
    El sistema detectó <strong style="color:var(--red)">24 procesos sin evidencia</strong>
    distribuidos en 5 direcciones.
  </div>
  {gc_rows}
  <div style="margin-top:10px;padding:8px 10px;
              background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.15);
              border-radius:7px;font-size:10px;color:var(--cyan)">
    ▶ Acción: Cargar evidencias digitales en SERCOP con SHA-256 verificable ·
    Plazo: 48h · Responsable: Director DAPS + DAF + DOBS
  </div>
</div>"""

    # ── PROTOCOLO REGULARIZACIÓN ──────────────────────────────────────────────
    protocolo_html = """
<div class="grid-2" style="margin-top:16px">
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:10px">
      ✅ PROTOCOLO DESACTIVACIÓN DE ALERTA
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">DÍA 1-2:</strong> Subir evidencias SHA-256 · 24 procesos DOBS+DAPS+DAF
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">DÍA 3-5:</strong> Publicar procesos POA-06-12 y POA-03-07 en SERCOP
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">DÍA 6-10:</strong> Adjudicar contratos pendientes · notificar eSIGEF
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.07);border-radius:6px">
        <strong style="color:var(--green)">DÍA 15:</strong> la alerta se desactiva automáticamente · mejora proyectada en eficiencia
      </div>
    </div>
  </div>
  <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:10px">
      ⚠️ CONSECUENCIAS SI NO SE ACTÚA (PRÓXIMO TRIMESTRE)
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        🔴 Observación formal Contraloría · posible glosa contable $830K
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        🔴 Bloqueo desembolso PNUD Agua Rural $2.4M · requiere cadena limpia
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        🔴 La eficiencia direccional se mantiene en 33.99% · calificación no supera 55% al cierre del semestre
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.07);border-radius:6px">
        🔴 4 metas PDOT sin avance → riesgo rendición de cuentas 2027
      </div>
    </div>
  </div>
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑧ CADENA POA·PAC",
        "Trazabilidad Operativa",
        "POA → PAC → SERCOP → eSIGEF · Alerta operativa activa · 4 cortes · 24 procesos sin SHA-256",
        '<span class="badge badge-red">🔴 ALERTA ACTIVA</span>',
    )

    html = hdr + flujo_html + metas_html + gc_html + protocolo_html

    render_page(html, show_tech=show_tech, height=1900)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Protocolo de alerta",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "Alerta operativa activa en Montecristi: 4 metas PDOT sin contrato PAC "
                "(agua Isabel Muentes $380K, vialidad Eloy Alfaro $210K, "
                "luminarias Aníbal San Andrés $95K, centro La Pila $145K) "
                "y 24 procesos sin evidencia SHA-256 en SERCOP. "
                "¿Cuál es el protocolo legal exacto bajo LOSNCP y COOTAD "
                "para regularizar cada proceso sin incurrir en responsabilidad administrativa?"
            )
            st.rerun()
    with c2:
        if st.button("🚨 Ver Señales de Alerta", use_container_width=True):
            st.session_state["page"] = "sat"
            st.rerun()
    with c3:
        if st.button("🎯 Ver Metas del Plan Cantonal", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
