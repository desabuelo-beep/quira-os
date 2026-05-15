"""
QUIRA OS v0.1 — P-02 Causas de la Brecha
¿Por qué ICGI-T bajó? · Vectores causales · Fiel al DEMO.html P-02
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    icgit     = data["icgit"]
    score     = icgit["score"]
    proj      = icgit.get("proyeccion", 65.77)
    hist      = icgit.get("historico", {})
    indices   = data["indices"]

    # ── VECTORES CAUSALES (datos sellados SIAP-ICPI) ─────────────────────────
    VECTORES = [
        {
            "codigo": "ISP",
            "nombre": "Salud Presupuestaria",
            "impacto": -8.2,
            "valor": 14.58,
            "color": "red",
            "descripcion": "ISP 14.58% · muy por debajo del umbral COOTAD 65%",
            "accion": "Activar coactivas + actualizar catastro predial",
        },
        {
            "codigo": "IED",
            "nombre": "Eficiencia de Direcciones",
            "impacto": -6.8,
            "valor": 33.99,
            "color": "red",
            "descripcion": "SAT-0: 4 metas PDOT sin contrato PAC activo · 24 procesos sin SHA-256",
            "accion": "Publicar evidencias PAC en SERCOP · plazo 48h",
        },
        {
            "codigo": "IGP",
            "nombre": "Gobernanza Participativa",
            "impacto": -4.1,
            "valor": 27.98,
            "color": "amber",
            "descripcion": "CPCCS V=0 en RDC 2026 · 50 UT activas vs meta 75",
            "accion": "Convocar asambleas Aníbal San Andrés e Isabel Muentes",
        },
        {
            "codigo": "IOC",
            "nombre": "Opacidad Crítica",
            "impacto": -3.1,
            "valor": 17.71,
            "color": "amber",
            "descripcion": "LOTAIP parcial · portal desactualizado · índice invertido",
            "accion": "Actualizar portal transparencia · publicar POA/PAC",
        },
        {
            "codigo": "IET",
            "nombre": "Equidad Territorial",
            "impacto": -2.8,
            "valor": 44.80,
            "color": "amber",
            "descripcion": "Isabel Muentes $40/hab vs cabecera $113/hab · brecha 2.8×",
            "accion": "Redirigir inversión Q2 · mínimo $80/hab parroquias críticas",
        },
        {
            "codigo": "PSG",
            "nombre": "Presupuesto de Género",
            "impacto": -2.4,
            "valor": 12.83,
            "color": "purple",
            "descripcion": "12.83% vs meta 30% · bloquea Gender Bond $95K",
            "accion": "Reclasificar programas género en POA-Q2 para alcanzar 20%",
        },
    ]

    total_impacto = sum(v["impacto"] for v in VECTORES)

    # ── LÍNEA DE TIEMPO ICGI-T ────────────────────────────────────────────────
    timeline_items = [
        ("2023", hist.get("2023", 57.36), "amber", "Línea base"),
        ("2024", hist.get("2024", 67.11), "green",  "Mejora sostenida"),
        ("2025", hist.get("2025", 69.93), "green",  "Casi Gestión por Mandato"),
        ("Q1-2026", score,                 "red",    "Caída · Transición Crítica"),
        ("Proj 2026", proj,                "amber",  "Proyección cierre"),
    ]

    def _tl_item(label, val, col, nota):
        is_proj = label.startswith("Proj")
        border_style = "dashed" if is_proj else "solid"
        return f"""
  <div style="text-align:center;flex:1;min-width:90px">
    <div style="font-size:10px;color:var(--muted);font-weight:700;
                text-transform:uppercase;margin-bottom:6px">{label}</div>
    <div style="font-size:28px;font-weight:900;color:var(--{col});
                font-family:var(--mono);line-height:1">{val:.2f}<span style="font-size:13px">%</span></div>
    <div style="font-size:9px;color:var(--muted);margin-top:4px">{nota}</div>
    <div style="height:3px;background:var(--{col});border-radius:2px;
                margin-top:8px;opacity:{'0.5' if is_proj else '1'};
                border-style:{border_style}"></div>
  </div>"""

    timeline_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">📈 EVOLUCIÓN ICGI-T · 2023 → Q1-2026</div>
  <div style="display:flex;gap:8px;align-items:flex-end;padding:8px 0">
    {"".join(_tl_item(*t) for t in timeline_items)}
  </div>
  <div style="margin-top:14px;padding:10px 12px;background:rgba(255,77,109,.06);
              border:1px solid rgba(255,77,109,.2);border-radius:8px;
              font-size:11px;color:var(--muted);line-height:1.6">
    ⚠️ El ICGI-T subió consistentemente 2023→2025 (+12.57 pts).
    La caída Q1-2026 (−16.37 pts vs 2025) se explica por
    <strong style="color:var(--white)">6 vectores causales identificados</strong>,
    no por deterioro estructural del GAD. La proyección {proj:.2f}%
    es alcanzable si se activan las acciones correctoras en Q2-2026.
  </div>
</div>"""

    # ── VECTORES CAUSALES (barras horizontales) ───────────────────────────────
    def _vector_row(v):
        width_pct = min(abs(v["impacto"]) / 10.0 * 100, 100)
        col = v["color"]
        return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:10px;
              padding:14px 16px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div>
        <span style="font-size:11px;font-weight:700;color:var(--white)">{v["codigo"]} · {v["nombre"]}</span>
        <span style="font-size:10px;color:var(--muted);margin-left:8px">({v["valor"]:.2f}%)</span>
      </div>
      <div style="font-size:18px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">{v["impacto"]:.1f} pts</div>
    </div>
    <div style="height:6px;background:var(--divider);border-radius:3px;overflow:hidden;margin-bottom:8px">
      <div style="height:6px;width:{width_pct:.0f}%;background:var(--{col});
                  border-radius:3px;transition:width .4s ease"></div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px">
      <div style="font-size:10px;color:var(--muted);flex:1">{v["descripcion"]}</div>
      <div style="font-size:10px;color:var(--cyan);background:rgba(0,212,255,.06);
                  border:1px solid rgba(0,212,255,.15);border-radius:6px;
                  padding:4px 8px;white-space:nowrap;flex-shrink:0">
        ▶ {v["accion"]}
      </div>
    </div>
  </div>"""

    vectores_html = f"""
<div class="card">
  <div class="card-title">🔍 6 VECTORES CAUSALES · Impacto en ICGI-T Q1-2026</div>
  <div style="display:flex;justify-content:space-between;align-items:center;
              margin-bottom:14px;padding:8px 12px;
              background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:8px">
    <div style="font-size:11px;color:var(--muted)">Impacto acumulado de los 6 vectores</div>
    <div style="font-size:22px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{total_impacto:.1f} pts</div>
  </div>
  {"".join(_vector_row(v) for v in VECTORES)}
</div>"""

    # ── ESCALA AVEP ───────────────────────────────────────────────────────────
    avep_scale = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">🎯 ESCALA AVEP · Posición actual y meta mandato</div>
  <div style="position:relative;height:50px;background:linear-gradient(90deg,
    #E53E3E 0%,#E67E22 25%,#D69E2E 45%,#38A169 65%,#00D4FF 85%,#7C5CFC 100%);
    border-radius:10px;overflow:visible;margin:8px 0 30px">
    <!-- Marcadores de escala -->
    <div style="position:absolute;top:0;left:0%;height:100%;border-left:2px solid rgba(255,255,255,.3)"></div>
    <div style="position:absolute;top:0;left:25%;height:100%;border-left:2px solid rgba(255,255,255,.3)"></div>
    <div style="position:absolute;top:0;left:50%;height:100%;border-left:2px solid rgba(255,255,255,.3)"></div>
    <div style="position:absolute;top:0;left:70%;height:100%;border-left:2px solid rgba(255,255,255,.3)"></div>
    <div style="position:absolute;top:0;left:85%;height:100%;border-left:2px solid rgba(255,255,255,.3)"></div>
    <!-- Score actual -->
    <div style="position:absolute;top:-10px;left:{score:.1f}%;
                transform:translateX(-50%);white-space:nowrap">
      <div style="background:var(--red);color:white;font-size:10px;font-weight:800;
                  padding:3px 8px;border-radius:6px">▼ {score:.2f}%</div>
    </div>
    <!-- Meta -->
    <div style="position:absolute;top:-10px;left:70%;
                transform:translateX(-50%);white-space:nowrap">
      <div style="background:var(--green);color:white;font-size:10px;font-weight:800;
                  padding:3px 8px;border-radius:6px">🎯 70%</div>
    </div>
    <!-- Etiquetas -->
    <div style="position:absolute;bottom:-22px;left:0%;font-size:9px;color:var(--muted)">Ruptura</div>
    <div style="position:absolute;bottom:-22px;left:23%;font-size:9px;color:var(--muted)">Ocurrencia</div>
    <div style="position:absolute;bottom:-22px;left:48%;font-size:9px;color:var(--muted)">Transición</div>
    <div style="position:absolute;bottom:-22px;left:68%;font-size:9px;color:var(--muted)">Mandato</div>
    <div style="position:absolute;bottom:-22px;left:83%;font-size:9px;color:var(--muted)">Excelencia</div>
  </div>
</div>"""

    # ── DESMITIFICACIÓN ───────────────────────────────────────────────────────
    mitos_html = """
<div class="grid-2" style="margin-top:16px">
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:10px">
      ✅ LO QUE SÍ FUNCIONA
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 Ti_norm 70% · ritmo inversión adecuado
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 IFE-A 72.73% · 48/66 promesas en PDOT
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 Bomberos 82.7% · Patronato 74.1% · bien alineados
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.08);border-radius:6px">
        🔵 ICODS 87.5% · 14 ODS vinculados con metas PDOT
      </div>
    </div>
  </div>
  <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:10px">
      ⚠️ ACCIONES URGENTES Q2-2026
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.08);border-radius:6px">
        🔴 ISP · Activar coactivas + actualizar catastro predial
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.08);border-radius:6px">
        🔴 IED · Publicar evidencias PAC en SERCOP · 48h
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,184,0,.08);border-radius:6px">
        🟡 IGP · Convocar asambleas parroquiales pendientes
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.08);border-radius:6px">
        🟣 PSG · Reclasificar programas género en POA-Q2
      </div>
    </div>
  </div>
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "② CAUSAS DE LA BRECHA",
        "Análisis Causal",
        f"¿Por qué ICGI-T bajó de 69.93% (2025) a {score:.2f}% (Q1-2026)? · 6 vectores identificados",
        f'<span class="badge badge-red">−{abs(score - 69.93):.2f} pts vs 2025</span>',
    )

    html = hdr + timeline_html + vectores_html + avep_scale + mitos_html

    render_page(html, show_tech=show_tech, height=1800)

    # ── CTAs Streamlit ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Analizar con IA", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El ICGI-T de Montecristi bajó de 69.93% en 2025 a 53.56% en Q1-2026. "
                "Los 6 vectores causales suman −27.4 pts: ISP −8.2 pts, IED −6.8 pts, "
                "IGP −4.1 pts, IOC −3.1 pts, IET −2.8 pts, PSG −2.4 pts. "
                "¿Cuál es el vector más urgente de atacar para recuperar la proyección de 65.77% al cierre 2026?"
            )
            st.rerun()
    with c2:
        if st.button("⚡ Ver Pulso Ejecutivo", use_container_width=True):
            st.session_state["page"] = "pulso"
            st.rerun()
    with c3:
        if st.button("🎯 Ver Metas PDOT", use_container_width=True):
            st.session_state["page"] = "metas"
            st.rerun()
