"""
QUIRA OS v0.1 — P-03 Congruencias · HPT-M
Fiel al DEMO.html P-05 · st.components.v1.html() render
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


def _cong_card(numero: str, nombre: str, subtitulo: str, score: float,
               color: str, fill_class: str, detalle: str, pregunta: str,
               sentinel_txt: str) -> str:
    return f"""
<div class="card" style="border-left:3px solid var(--{color})">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
    <div>
      <div style="font-size:13px;font-weight:700">{numero} {nombre}</div>
      <div style="font-size:11px;color:var(--muted)">{subtitulo}</div>
    </div>
    <div style="font-size:24px;font-weight:800;font-family:var(--mono);
                color:var(--{color})">{score:.1f}%</div>
  </div>
  <div class="prog-bar"><div class="prog-fill {fill_class}" style="width:{score:.1f}%"></div></div>
  <div style="font-size:11px;color:var(--muted);margin-top:6px">{detalle}</div>
  <div style="font-size:11px;color:var(--cyan);font-style:italic;margin-top:7px;
              padding:5px 9px;border-left:2px solid rgba(14,165,233,.4);
              background:rgba(14,165,233,.05);border-radius:0 6px 6px 0">{pregunta}</div>
  <div style="display:inline-block;margin-top:12px;padding:8px 12px;
              background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
              border-radius:8px;font-size:12px;color:var(--cyan)">
    💬 {sentinel_txt}
  </div>
</div>"""


def _nodo_card(nodo: str, nombre: str, entidades: str, score: float, color: str) -> str:
    return (
        f'<div style="text-align:center;padding:12px;background:var(--navy-light);border-radius:8px">'
        f'<div style="font-size:10px;font-weight:700;color:var(--muted);margin-bottom:4px">{nodo}</div>'
        f'<div style="font-size:13px;font-weight:700">{nombre}</div>'
        f'<div style="font-size:11px;color:var(--muted);margin:4px 0">{entidades}</div>'
        f'<div style="font-size:20px;font-weight:800;color:var(--{color})">{score:.1f}%</div>'
        f'</div>'
    )


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr = page_header(
        "② FIDELIDAD POLÍTICA",
        "Fidelidad Electoral · HPT-M · 4 Congruencias",
        "Plan de Gobierno 2023 → PDOT 2023-2027 → POA → Territorio · Fidelidad de Mandato",
        '<span class="badge badge-real">REAL</span>',
    )

    # ── IFE HERO CARD ─────────────────────────────────────────────────────────
    ife_hero = """
<div class="card" style="margin-bottom:14px;border-left:4px solid var(--cyan);padding:14px 16px;
     background:linear-gradient(135deg,rgba(14,165,233,.06) 0%,rgba(0,0,0,0) 100%)">
  <div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;
              letter-spacing:.12em;margin-bottom:10px">
    🗳️ Fidelidad Electoral · IFE · Promesa → Planificación → Ejecución ·
    <span class="badge badge-real">REAL</span>
  </div>
  <div style="display:grid;grid-template-columns:auto 1fr 1fr;gap:16px;align-items:center">

    <!-- IFE-A número -->
    <div style="text-align:center;min-width:110px">
      <div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;
                  letter-spacing:.08em;margin-bottom:2px">IFE-A · Alineación</div>
      <div style="font-size:42px;font-weight:800;color:var(--white);line-height:1">72.73%</div>
      <div style="font-size:10px;color:var(--amber);font-weight:700;margin-top:3px">
        Gestión por Mandato ✅
      </div>
      <div class="prog-bar" style="margin-top:6px;height:6px">
        <div class="prog-fill amber" style="width:72.73%"></div>
      </div>
      <div style="font-size:9px;color:var(--muted);margin-top:3px">AVEP ≥ 70%</div>
    </div>

    <!-- Promesas counts -->
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.22);
                  border-radius:7px;padding:8px 10px">
        <div style="font-size:10px;font-weight:700;color:var(--green)">✅ Con meta PDOT formal</div>
        <div style="font-size:22px;font-weight:800;color:var(--green)">
          48 <span style="font-size:11px;font-weight:400;color:var(--muted)">/ 66 CNE</span>
        </div>
        <div style="font-size:9px;color:var(--muted)">Meta · indicador · presupuesto en PDOT 2023-2027</div>
      </div>
      <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.22);
                  border-radius:7px;padding:8px 10px">
        <div style="font-size:10px;font-weight:700;color:var(--red)">⚠️ Sin meta PDOT formal</div>
        <div style="font-size:22px;font-weight:800;color:var(--red)">
          18 <span style="font-size:11px;font-weight:400;color:var(--muted)">promesas · 27.27%</span>
        </div>
        <div style="font-size:9px;color:var(--muted)">Riesgo político cierre mandato 2027</div>
      </div>
    </div>

    <!-- IFE-E + interpretación -->
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.28);
                  border-radius:7px;padding:8px 10px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
          <div style="font-size:10px;font-weight:700;color:var(--purple)">IFE-E · Ejecución</div>
          <div style="font-size:9px;font-weight:700;color:var(--purple);
                      background:rgba(124,92,252,.15);border-radius:4px;padding:2px 6px">
            IFE-E · v1.2
          </div>
        </div>
        <div style="font-size:10px;color:var(--muted);line-height:1.5">
          PDOT→POA→PAC→eSIGEF ·
          <span style="color:var(--red);font-weight:700">⚡ SAT-0:</span>
          4 metas sin contrato PAC
        </div>
      </div>
      <div style="font-size:10px;color:var(--muted);line-height:1.5;padding:0 2px">
        💡 Mayo 2023: el <strong style="color:var(--white)">Ing. Jonathan Toro Largacha</strong>
        asumió 66 compromisos CNE ante 101,181 ciudadanos.
        IFE-A = <strong style="color:var(--amber)">48/66 formalizados</strong>.
        18 sin respaldo PDOT.
      </div>
      <div style="display:inline-block;padding:8px 12px;
                  background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
                  border-radius:8px;font-size:12px;color:var(--cyan)">
        💬 SENTINEL · IFE
      </div>
    </div>
  </div>
</div>"""

    # ── PDOT FRASE RECTORA ────────────────────────────────────────────────────
    pdot_frase = """
<div style="padding:8px 12px;margin-bottom:14px;background:rgba(14,165,233,.04);
            border-radius:8px;border-left:3px solid rgba(14,165,233,.3);
            font-size:11px;color:var(--muted);line-height:1.6">
  📌 <strong style="color:var(--cyan)">El PDOT sigue siendo el instrumento rector.</strong>
  El IFE mide la fidelidad del mandato dentro de él: cuántas promesas electorales se convirtieron
  en metas formales <strong style="color:var(--white)">(IFE-A)</strong> y cuántas de esas metas
  tienen trazabilidad operativa completa hasta el devengado eSIGEF
  <strong style="color:var(--white)">(IFE-E)</strong>.
</div>"""

    # ── 4 CONGRUENCIAS GRID ───────────────────────────────────────────────────
    cong_label = """
<div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;
            letter-spacing:.12em;margin-bottom:10px">
  🔗 Las 4 congruencias del HPT-M · cadena de integridad política
</div>"""

    cong_politica = _cong_card(
        "①", "Congruencia Política",
        "Promesa electoral → Meta PDOT → COOTAD",
        58.4, "amber", "amber",
        "IFE-A 72.73% mide la promesa → plan (48/66 CNE). El 58.4% incorpora la ejecución: 4 metas sin contrato PAC activo",
        "¿Estamos gobernando lo que prometimos?",
        "Analizar Congruencia Política",
    )

    cong_operativa = _cong_card(
        "②", "Congruencia Operativa",
        "POA ↔ PAC ↔ eSIGEF ↔ EP",
        47.2, "red", "red",
        "Cadena POA-PAC-SERCOP-eSIGEF · 4 cortes detectados · SAT-0 activo",
        "¿Lo planificado se está contratando y ejecutando?",
        "Analizar Cadena Operativa",
    )

    cong_territorial = _cong_card(
        "③", "Congruencia Territorial",
        "Inversión ↔ Parroquias ↔ NBI ↔ TPS",
        44.8, "red", "red",
        "Isabel Muentes (TPS 77.94) recibe solo $140K · brecha territorial crítica",
        "¿La inversión llega donde más se necesita?",
        "Analizar Brecha Territorial",
    )

    cong_ecosistemica = _cong_card(
        "④", "Congruencia Ecosistémica",
        "GAD ↔ Operadores ↔ Ciudadanía ↔ Cooperación",
        61.1, "amber", "amber",
        "Bomberos y Patronato bien alineados · EP Aseo bajo umbral",
        "¿Todo el holding municipal está alineado?",
        "Analizar Holding Municipal",
    )

    cong_grid = (
        f'<div class="grid-2" style="gap:16px;align-items:start">'
        f'<div style="display:flex;flex-direction:column;gap:12px">'
        f'{cong_politica}{cong_operativa}'
        f'</div>'
        f'<div style="display:flex;flex-direction:column;gap:12px">'
        f'{cong_territorial}{cong_ecosistemica}'
        f'</div>'
        f'</div>'
    )

    # ── ÁRBOL HPT-M ───────────────────────────────────────────────────────────
    arbol = (
        '<div class="card" style="margin-top:4px">'
        '<div class="card-title">Árbol HPT-M · 4 Nodos institucionales</div>'
        '<div class="grid-4">'
        + _nodo_card("NODO 1", "GOBIERNO",    "GAD Central · Alcaldía · Concejo",     61.2, "amber")
        + _nodo_card("NODO 2", "OPERADORES",  "EP Aseo · Bomberos · Patronato",        71.7, "amber")
        + _nodo_card("NODO 3", "TERRITORIO",  "7 parroquias · 101,181 hab.",           44.8, "red")
        + _nodo_card("NODO 4", "ECOSISTEMA",  "ODS · BID/CAF · CPCCS",                61.1, "amber")
        + '</div></div>'
    )

    # ── TECH NOTE ─────────────────────────────────────────────────────────────
    tech = ""
    if show_tech:
        tech = """
<div style="margin-top:16px;font-size:9px;color:rgba(255,255,255,.2);
            border-top:1px solid rgba(255,255,255,.04);padding-top:8px">
  🔧 Fuente: SIAP-ICPI H16 · H24 · IFE-A auditado CNE · IFE-E en construcción · Q1-2026
</div>"""

    # ── ASSEMBLE & RENDER ─────────────────────────────────────────────────────
    html = (
        hdr + ife_hero + pdot_frase
        + cong_label + cong_grid + arbol + tech
    )
    render_page(html, show_tech=show_tech, height=1350)

    # Native CTA
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("🗺️ Ver GeoTwin · Territorio", use_container_width=True):
            st.session_state["page"] = "geotwin"
            st.rerun()
    with c2:
        if st.button("🔮 Analizar con Sentinel", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "¿Qué congruencias de gobernanza están más críticas y qué acciones "
                "concretas debe tomar el GAD de Montecristi para mejorarlas "
                "antes del cierre 2026?"
            )
            st.rerun()
