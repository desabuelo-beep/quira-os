"""
QUIRA OS v0.1 — P-11 ODS Tracker
Agenda 2030 · Vinculación PDOT ↔ ODS · ICODS 87.5%
FUENTE DATOS: SIAP-ICPI_GOLD_MASTER_v4.1 (H73_OUTPUT_API)
Metodología de scores ODS:
  4 ODS con score derivado directamente de H73_OUTPUT_API:
    ODS  5 → PSG_EJECUCION  = 12.83% → score 13
    ODS  6 → Cobertura agua = 34.9%  → score 35  (PDOT diagnóstico)
    ODS 10 → IET_PERCAPITA  = 44.80% → score 45
    ODS 16 → IGP_REF_2025   = 27.98% → score 28
  Resto (13 ODS): score indicativo basado en estado cualitativo PDOT
  → no confundir con medición oficial ODS SNP/ONU
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── CATÁLOGO 17 ODS CON ESTADO MONTECRISTI ───────────────────────────────────
ODS_CATALOGO = [
    {
        "num": 1, "nombre": "Fin de la Pobreza",
        "estado": "VINCULADO", "color": "#E5243B",
        "vinculo": "Prioridad territorial rural · NBI parroquias · inversión per cápita mínima $80/hab",
        "meta_pdot": "Reducir la prioridad territorial promedio rural de 48.4% → 35% al 2027",
        "score": 72,
    },
    {
        "num": 2, "nombre": "Hambre Cero",
        "estado": "PARCIAL", "color": "#DDA63A",
        "vinculo": "Patronato Municipal · programas alimentarios grupos vulnerables",
        "meta_pdot": "Cobertura Patronato 60% familias vulnerables",
        "score": 55,
    },
    {
        "num": 3, "nombre": "Salud y Bienestar",
        "estado": "VINCULADO", "color": "#4C9F38",
        "vinculo": "Centros de salud rurales · Patronato · agua potable",
        "meta_pdot": "4 centros salud rurales operativos al 2027",
        "score": 68,
    },
    {
        "num": 4, "nombre": "Educación de Calidad",
        "estado": "VINCULADO", "color": "#C5192D",
        "vinculo": "Infraestructura escolar cantonal · 48/66 promesas CNE",
        "meta_pdot": "12 UE con infraestructura adecuada al 2027",
        "score": 74,
    },
    {
        "num": 5, "nombre": "Igualdad de Género",
        "estado": "CRÍTICO", "color": "#FF3A21",
        "vinculo": "Presupuesto de género 12.83% · bloquea Gender Bond $95K · ONU Mujeres",
        "meta_pdot": "Presupuesto de género ≥ 30% al 2027 · luminarias seguridad Aníbal San Andrés",
        "score": 13,          # PSG_EJECUCION=12.83% · fuente H73_OUTPUT_API (redondeado)
    },
    {
        "num": 6, "nombre": "Agua Limpia y Saneamiento",
        "estado": "CRÍTICO", "color": "#26BDE2",
        "vinculo": "Isabel Muentes 1.02% agua · cobertura cantonal 34.9% · PNUD Agua Rural",
        "meta_pdot": "Cobertura agua 65% · alcantarillado 70% al 2027",
        "score": 35,          # Cobertura agua cantonal=34.9% · fuente PDOT diagnóstico
    },
    {
        "num": 7, "nombre": "Energía Asequible",
        "estado": "PARCIAL", "color": "#FCC30B",
        "vinculo": "Luminarias solares · eficiencia energética edificios GAD",
        "meta_pdot": "Luminarias LED en vías principales al Q4-2026",
        "score": 48,
    },
    {
        "num": 8, "nombre": "Trabajo Decente",
        "estado": "VINCULADO", "color": "#A21942",
        "vinculo": "Turismo UNESCO · artesanía paja toquilla · EP Aseo",
        "meta_pdot": "Plan turismo operativo Q3-2026 · 200 empleos formales",
        "score": 61,
    },
    {
        "num": 9, "nombre": "Industria e Innovación",
        "estado": "PARCIAL", "color": "#FD6925",
        "vinculo": "QUIRA OS · plataforma digital GAD · cooperativas financieras",
        "meta_pdot": "Sistema digitalización trámites municipales Q2-2026",
        "score": 52,
    },
    {
        "num": 10, "nombre": "Reducción Desigualdades",
        "estado": "VINCULADO", "color": "#DD1367",
        "vinculo": "Equidad territorial 44.80% · Gov Twin · brecha territorial $40→$217/hab · Q1-2026",
        "meta_pdot": "Equidad territorial ≥ 60% · inversión mínima rural $80/hab al 2027",
        "score": 45,          # IET_PERCAPITA=44.80% · fuente H73_OUTPUT_API (redondeado)
    },
    {
        "num": 11, "nombre": "Ciudades Sostenibles",
        "estado": "VINCULADO", "color": "#FD9D24",
        "vinculo": "Vialidad 53%→75% · UNESCO ciudad creativa · ordenamiento territorial",
        "meta_pdot": "Plan ordenamiento urbano cantonal aprobado Q2-2026",
        "score": 66,
    },
    {
        "num": 12, "nombre": "Producción Responsable",
        "estado": "VINCULADO", "color": "#BF8B2E",
        "vinculo": "EP Aseo 47.9 ton/día → 30 ton/día · reciclaje · clasificación",
        "meta_pdot": "Sistema clasificación residuos 6 parroquias al 2027",
        "score": 58,
    },
    {
        "num": 13, "nombre": "Acción por el Clima",
        "estado": "VINCULADO", "color": "#3F7E44",
        "vinculo": "Fondo Verde GEF $180K · reforestación Colorado · dMRV",
        "meta_pdot": "500 ha reforestadas · carbono secuestrado medido",
        "score": 70,
    },
    {
        "num": 14, "nombre": "Vida Submarina",
        "estado": "PARCIAL", "color": "#0A97D9",
        "vinculo": "Costa Manabí · pesca artesanal · manejo litoral",
        "meta_pdot": "Plan manejo costero coordinado con Ministerio del Ambiente",
        "score": 42,
    },
    {
        "num": 15, "nombre": "Vida de Ecosistemas",
        "estado": "VINCULADO", "color": "#56C02B",
        "vinculo": "Reforestación laderas · biodiversidad · áreas protegidas",
        "meta_pdot": "300 ha en conservación · corredor biológico activo",
        "score": 71,
    },
    {
        "num": 16, "nombre": "Paz, Justicia e Instituciones",
        "estado": "VINCULADO", "color": "#00689D",
        "vinculo": "CPCCS · Participación 27.98% · rendición de cuentas · LOTAIP",
        "meta_pdot": "Participación ≥ 60% · 75 UT activas · RDC validado CPCCS",
        "score": 28,          # IGP_REF_2025=27.98% · fuente H73_OUTPUT_API (redondeado)
    },
    {
        "num": 17, "nombre": "Alianzas para los Objetivos",
        "estado": "VINCULADO", "color": "#19486A",
        "vinculo": "BID Lab · PNUD · ONU Mujeres · CAF · GEF · Fondo Verde",
        "meta_pdot": "$3.2M fondos no reembolsables gestionados al 2027",
        "score": 82,
    },
]


def _ods_chip(o: dict) -> str:
    """Chip cuadrado para cada ODS en el grid."""
    estado_map = {
        "VINCULADO": ("green",  "✅"),
        "PARCIAL":   ("amber",  "🟡"),
        "CRÍTICO":   ("red",    "🔴"),
    }
    col, ico = estado_map.get(o["estado"], ("muted", "⏳"))
    bg_alpha = ".12" if o["estado"] == "CRÍTICO" else ".06"
    return (
        f'<div style="background:rgba(255,255,255,{bg_alpha});'
        f'border:2px solid {o["color"]}55;border-radius:12px;'
        f'padding:14px 10px;text-align:center;position:relative">'
        f'<div style="position:absolute;top:6px;right:8px;font-size:12px">{ico}</div>'
        f'<div style="font-size:28px;font-weight:900;color:{o["color"]};'
        f'font-family:var(--mono);line-height:1">{o["num"]}</div>'
        f'<div style="font-size:10px;color:rgba(255,255,255,.7);margin-top:5px;'
        f'line-height:1.3;font-weight:600">{o["nombre"]}</div>'
        f'<div style="height:5px;background:rgba(255,255,255,.1);border-radius:3px;'
        f'margin-top:8px;overflow:hidden">'
        f'<div style="height:5px;width:{o["score"]}%;background:{o["color"]};'
        f'border-radius:3px;opacity:.9"></div></div>'
        f'</div>'
    )


def _ods_detail_row(o: dict) -> str:
    """Fila detallada para los ODS críticos/parciales."""
    estado_map = {
        "VINCULADO": ("green",  "badge-green",  "VINCULADO"),
        "PARCIAL":   ("amber",  "badge-amber",  "PARCIAL"),
        "CRÍTICO":   ("red",    "badge-red",    "CRÍTICO"),
    }
    col, badge_cls, label = estado_map.get(o["estado"], ("muted", "", o["estado"]))
    return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid {o["color"]};border-radius:9px;
              padding:12px 14px;margin-bottom:8px">
    <div style="display:flex;justify-content:space-between;align-items:center;
                margin-bottom:5px">
      <div style="display:flex;align-items:center;gap:8px">
        <span style="font-size:11px;font-weight:900;color:{o["color"]};
                     font-family:var(--mono)">ODS {o["num"]}</span>
        <span style="font-size:11px;font-weight:700;color:var(--white)">{o["nombre"]}</span>
        <span class="badge {badge_cls}">{label}</span>
      </div>
      <div style="font-size:16px;font-weight:900;color:var(--{col});
                  font-family:var(--mono)">{o["score"]}%</div>
    </div>
    <div style="height:4px;background:var(--divider);border-radius:2px;
                overflow:hidden;margin-bottom:6px">
      <div style="height:4px;width:{o["score"]}%;background:{o["color"]};
                  border-radius:2px"></div>
    </div>
    <div style="font-size:10px;color:var(--muted)">{o["vinculo"]}</div>
    <div style="font-size:10px;color:var(--cyan);margin-top:3px">
      📋 Meta PDOT: {o["meta_pdot"]}
    </div>
  </div>"""


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()
    indices   = data["indices"]
    icods_val = indices.get("ICODS", {}).get("valor", 87.50)

    n_vinculado = sum(1 for o in ODS_CATALOGO if o["estado"] == "VINCULADO")
    n_parcial   = sum(1 for o in ODS_CATALOGO if o["estado"] == "PARCIAL")
    n_critico   = sum(1 for o in ODS_CATALOGO if o["estado"] == "CRÍTICO")

    criticos  = [o for o in ODS_CATALOGO if o["estado"] == "CRÍTICO"]
    parciales = [o for o in ODS_CATALOGO if o["estado"] == "PARCIAL"]
    vinculados_top = sorted(
        [o for o in ODS_CATALOGO if o["estado"] == "VINCULADO"],
        key=lambda x: x["score"], reverse=True
    )[:5]

    # ── RESUMEN HEADER ────────────────────────────────────────────────────────
    resumen_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{icods_val:.1f}<span style="font-size:18px">%</span></div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">Cumplimiento ODS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Gestión por Mandato ✅</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{n_vinculado}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">ODS VINCULADOS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Con meta PDOT + indicador</div>
  </div>
  <div style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{n_parcial}</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">ODS PARCIALES</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Vinculación incompleta</div>
  </div>
  <div style="background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.3);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:42px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{n_critico}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">ODS CRÍTICOS</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Requieren acción urgente</div>
  </div>
</div>"""

    # ── GRID 17 ODS ──────────────────────────────────────────────────────────
    chips = "".join(_ods_chip(o) for o in ODS_CATALOGO)
    grid_html = f"""
<div class="card">
  <div class="card-title">🌐 17 ODS · AGENDA 2030 · Estado Montecristi ene–mar 2026</div>
  <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(115px,1fr));
              gap:10px;margin-bottom:14px">
    {chips}
  </div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:9px;color:var(--muted);
              padding-top:8px;border-top:1px solid rgba(255,255,255,.05)">
    <span>✅ Vinculado = meta PDOT + indicador + presupuesto</span>
    <span>🟡 Parcial = vinculación incompleta o en proceso</span>
    <span>🔴 Crítico = brecha severa · riesgo mandato 2027</span>
    <span style="color:rgba(255,184,0,.7)">
      ⚠ Barra inferior: ODS 5/6/10/16 con dato derivado · Resto indicativo PDOT · Pendiente medición oficial SNP
    </span>
  </div>
</div>"""

    # ── ODS CRÍTICOS DETALLADOS ───────────────────────────────────────────────
    criticos_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">🔴 ODS CRÍTICOS · Acción urgente requerida</div>
  {"".join(_ods_detail_row(o) for o in criticos)}
</div>"""

    # ── FONDOS DESBLOQUEABLES ─────────────────────────────────────────────────
    fondos_html = """
<div class="card" style="margin-top:16px">
  <div class="card-title">💸 FONDOS INTERNACIONALES ALINEABLES · ODS como palanca</div>
  <div class="grid-2" style="gap:12px">
    <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
                border-radius:10px;padding:14px">
      <div style="font-size:11px;font-weight:700;color:var(--cyan);margin-bottom:8px">
        🔵 DESBLOQUEABLES INMEDIATO
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.06);border-radius:6px;margin-bottom:6px">
        🌿 GEF Fondo Verde Clima · $180K · ODS 13+15 · Elegible ahora
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.06);border-radius:6px">
        🌐 PNUD Agua Rural · $2.4M · ODS 6 · Requiere calificación ≥ 55%
      </div>
    </div>
    <div style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);
                border-radius:10px;padding:14px">
      <div style="font-size:11px;font-weight:700;color:var(--amber);margin-bottom:8px">
        ⏳ REQUIEREN MEJORA PREVIA
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,184,0,.06);border-radius:6px;margin-bottom:6px">
        💜 BID Lab Gender Bond · $95K · ODS 5 · Requiere presupuesto de género ≥ 30% (actual 12.83%)
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,184,0,.06);border-radius:6px">
        🏦 BDE Crédito Municipal · ODS 11 · Requiere salud presupuestaria ≥ 65% (actual 14.58%)
      </div>
    </div>
  </div>
</div>"""

    # ── TOP 5 VINCULADOS ──────────────────────────────────────────────────────
    top5_rows = "".join(_ods_detail_row(o) for o in vinculados_top)
    top5_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">✅ TOP 5 ODS MEJOR VINCULADOS · Fortalezas del GAD</div>
  {top5_rows}
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑦ AGENDA 2030 · ODS",
        "Agenda 2030 · Vinculación al Plan Cantonal",
        f"Cumplimiento ODS {icods_val:.1f}% · {n_vinculado} ODS vinculados · {n_critico} críticos · Corte ene–mar 2026",
        '<span class="badge badge-green">✅ Gestión por Mandato</span>',
    )

    html = hdr + resumen_html + grid_html + criticos_html + fondos_html + top5_html

    render_page(html, show_tech=show_tech, height=3500)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Estrategia ODS + fondos",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El GAD de Montecristi tiene un cumplimiento ODS de 87.5% con 14 ODS vinculados al PDOT. "
                "Los ODS 5 (Género, presupuesto de género 12.83%) y ODS 6 (Agua, cobertura 34.9%) están críticos. "
                "Hay $2.68M en fondos internacionales disponibles (GEF, PNUD, BID Gender Bond). "
                "¿Cuál es la secuencia óptima de acciones para desbloquear estos fondos "
                "usando los ODS como palanca política ante cooperantes?"
            )
            st.rerun()
    with c2:
        if st.button("💰 Ver Inversión por Habitante", use_container_width=True):
            st.session_state["page"] = "inversion"
            st.rerun()
    with c3:
        if st.button("🗺️ Ver Territorio Digital", use_container_width=True):
            st.session_state["page"] = "geotwin"
            st.rerun()
