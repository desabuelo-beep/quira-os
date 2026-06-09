"""
QUIRA OS v0.1 — P-10 Inversión per Cápita
Equidad territorial · $/hab por parroquia · Fiel al DEMO.html P-10
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── EJE SECTORIAL DE INVERSIÓN ────────────────────────────────────────────────
EJES_INVERSION = [
    {"eje": "Agua y Saneamiento",      "monto": 4_200_000, "pct": 15.7, "color": "cyan",   "meta": "Cobertura agua 65%"},
    {"eje": "Vialidad Cantonal",       "monto": 6_800_000, "pct": 25.5, "color": "amber",  "meta": "Vías 75% con tratamiento"},
    {"eje": "Educación y Cultura",     "monto": 2_100_000, "pct":  7.9, "color": "green",  "meta": "Infraestructura escolar"},
    {"eje": "Salud Comunitaria",       "monto": 1_450_000, "pct":  5.4, "color": "green",  "meta": "Centros salud rurales"},
    {"eje": "Gestión Ambiental",       "monto": 1_200_000, "pct":  4.5, "color": "green",  "meta": "Residuos 30 ton/día"},
    {"eje": "Seguridad Ciudadana",     "monto":   980_000, "pct":  3.7, "color": "purple", "meta": "Luminarias + CCTV"},
    {"eje": "Administración y Apoyo",  "monto": 5_959_147, "pct": 22.3, "color": "muted",  "meta": "Gasto corriente"},
    {"eje": "Otros / Sin asignar",     "monto": 4_000_000, "pct": 15.0, "color": "muted",  "meta": "Planificación Q2-Q4"},
]


def _parroquia_bar(p: dict, max_cap: float) -> str:
    """Barra horizontal de inversión per cápita para una parroquia."""
    cap   = p["per_capita"]
    pct   = min((cap / max_cap) * 100, 100)
    col   = "green" if cap >= 100 else "amber" if cap >= 70 else "red"
    gap   = max(80 - cap, 0)   # brecha vs meta $80/hab
    estado_map = {
        "EMERGENCIA": '<span class="badge badge-red">EMERGENCIA</span>',
        "PRIORIDAD":  '<span style="display:inline-block;padding:2px 8px;border-radius:8px;'
                      'font-size:10px;font-weight:600;background:rgba(124,92,252,.15);'
                      'color:#7C5CFC;border:1px solid rgba(124,92,252,.3)">PRIORIDAD</span>',
        "ALERTA":     '<span class="badge badge-amber">ALERTA</span>',
        "NORMAL":     '<span class="badge badge-cyan">NORMAL</span>',
        "OK":         '<span class="badge badge-green">OK</span>',
    }
    badge = estado_map.get(p["estado"], "")

    gap_html = (
        f'<span style="font-size:9px;color:var(--red);margin-left:8px">'
        f'−${gap}/hab bajo meta</span>'
        if gap > 0 else
        f'<span style="font-size:9px;color:var(--green);margin-left:8px">✅ sobre meta</span>'
    )

    return f"""
<div style="margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:center;
              margin-bottom:4px">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="font-size:11px;font-weight:700;color:var(--white)">{p["emoji"]} {p["nombre"]}</span>
      {badge}
      {gap_html}
    </div>
    <div style="font-size:16px;font-weight:900;color:var(--{col});
                font-family:var(--mono)">${cap}</div>
  </div>
  <div style="position:relative;height:8px;background:var(--divider);
              border-radius:4px;overflow:hidden">
    <div style="height:8px;width:{pct:.1f}%;background:var(--{col});
                border-radius:4px;transition:width .4s ease"></div>
    <!-- Meta $80 marcador -->
    <div style="position:absolute;top:0;left:{min(80/max_cap*100,100):.1f}%;
                height:8px;width:2px;background:rgba(255,255,255,.5)"></div>
  </div>
  <div style="display:flex;justify-content:space-between;
              font-size:9px;color:var(--muted);margin-top:2px">
    <span>{p["habitantes"]:,} hab · ${p["inversion"]:,} total</span>
    <span>TPS {p["tps"]:.1f}% vulnerabilidad</span>
  </div>
</div>"""


def _eje_row(e: dict) -> str:
    col = e["color"] if e["color"] != "muted" else "white"
    pct_bar = min(e["pct"], 100)
    return f"""
<div style="display:flex;align-items:center;gap:10px;
            padding:8px;background:rgba(255,255,255,.02);
            border-radius:7px;margin-bottom:6px">
  <div style="min-width:160px;font-size:11px;font-weight:600;
              color:var(--{'muted' if e['color']=='muted' else 'white'})">{e["eje"]}</div>
  <div style="flex:1">
    <div style="height:6px;background:var(--divider);border-radius:3px;overflow:hidden">
      <div style="height:6px;width:{pct_bar:.1f}%;background:var(--{e['color'] if e['color']!='muted' else 'divider'});
                  border-radius:3px;opacity:{'.4' if e['color']=='muted' else '1'}"></div>
    </div>
  </div>
  <div style="min-width:55px;text-align:right;font-size:12px;font-weight:700;
              color:var(--{col});font-family:var(--mono)">{e["pct"]:.1f}%</div>
  <div style="min-width:90px;text-align:right;font-size:10px;
              color:var(--muted)">${e["monto"]/1_000_000:.2f}M</div>
</div>"""


def render() -> None:
    data       = load_all()
    show_tech  = is_tecnico()
    parroquias = data.get("parroquias", [])
    icgit      = data["icgit"]

    presupuesto_total = icgit.get("presupuesto_total", 26_689_147)
    inversion_ejec    = icgit.get("inversion_ejecutada", 7_820_000)
    pct_ejec          = (inversion_ejec / presupuesto_total) * 100 if presupuesto_total else 0
    total_hab         = sum(p["habitantes"] for p in parroquias)
    cap_prom          = presupuesto_total / total_hab if total_hab else 0

    # Ordenar parroquias por per_capita asc (las más rezagadas primero)
    sorted_par = sorted(parroquias, key=lambda x: x["per_capita"])
    max_cap    = max(p["per_capita"] for p in parroquias)

    # ── MACRO CARDS ───────────────────────────────────────────────────────────
    macro_html = f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:11px;font-weight:700;color:var(--cyan);margin-bottom:4px">
      PRESUPUESTO TOTAL 2026
    </div>
    <div style="font-size:28px;font-weight:900;color:var(--white);
                font-family:var(--mono)">${presupuesto_total/1_000_000:.2f}M</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">101,318 hab · Montecristi</div>
  </div>
  <div style="background:rgba(0,224,150,.06);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:4px">
      EJECUTADO ene–mar 2026
    </div>
    <div style="font-size:28px;font-weight:900;color:var(--green);
                font-family:var(--mono)">${inversion_ejec/1_000_000:.2f}M</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Ritmo de ejecución Q1 adecuado</div>
  </div>
  <div style="background:rgba(255,184,0,.06);border:1px solid rgba(255,184,0,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:11px;font-weight:700;color:var(--amber);margin-bottom:4px">
      PROMEDIO CANTONAL
    </div>
    <div style="font-size:28px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">${cap_prom:.0f}<span style="font-size:13px">/hab</span></div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Meta mínima rural $80/hab</div>
  </div>
  <div style="background:rgba(255,77,109,.06);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:4px">
      BRECHA MAYOR
    </div>
    <div style="font-size:28px;font-weight:900;color:var(--red);
                font-family:var(--mono)">5.4×</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Cabecera $217 vs Isabel M. $40 · datos Q1-2026</div>
  </div>
</div>"""

    # ── BARRAS PER CÁPITA ─────────────────────────────────────────────────────
    bars_html = f"""
<div class="card">
  <div class="card-title">💰 INVERSIÓN POR HABITANTE · 7 PARROQUIAS · ene–mar 2026</div>
  <div style="font-size:10px;color:var(--muted);margin-bottom:12px;
              padding:6px 10px;background:rgba(255,255,255,.03);border-radius:6px">
    🎯 Meta mínima rural: <strong style="color:var(--amber)">$80/hab</strong>
    · Línea blanca = umbral · Barras ordenadas de mayor brecha a menor
  </div>
  {"".join(_parroquia_bar(p, max_cap) for p in sorted_par)}
  <div style="margin-top:12px;font-size:9px;color:var(--muted);
              border-top:1px solid rgba(255,255,255,.05);padding-top:8px">
    📌 Inversión total cantonal estimada por parroquia basada en SIAP-ICPI ene–mar 2026
    · TPS = Tasa de Pobreza por Sistema (mayor TPS = mayor vulnerabilidad)
  </div>
</div>"""

    # ── DISTRIBUCIÓN SECTORIAL ────────────────────────────────────────────────
    ejes_html = f"""
<div class="card" style="margin-top:16px">
  <div class="card-title">📊 DISTRIBUCIÓN SECTORIAL DEL PRESUPUESTO · 2026</div>
  {"".join(_eje_row(e) for e in EJES_INVERSION)}
  <div style="margin-top:10px;padding:8px 12px;
              background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.15);
              border-radius:7px;font-size:10px;color:var(--muted);line-height:1.6">
    ⚠️ <strong style="color:var(--red)">Agua y Saneamiento (15.7%)</strong> recibe $4.2M
    para cubrir brecha del 34.9% de cobertura.
    Isabel Muentes, la parroquia más vulnerable (TPS 77.94%, NBI 61.2%), recibe $228K total —
    insuficiente para alcanzar la meta de cobertura al 2027 sin financiamiento externo.
  </div>
</div>"""

    # ── ANÁLISIS EQUIDAD ──────────────────────────────────────────────────────
    equidad_html = """
<div class="grid-2" style="margin-top:16px">
  <div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:10px">
      🔴 PARROQUIAS BAJO META $80/hab
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,77,109,.08);border-radius:6px">
        🚨 Isabel Muentes · $40/hab · TPS 77.94 · agua 1.02% — EMERGENCIA
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(124,92,252,.1);border-radius:6px">
        💜 Aníbal San Andrés · $61/hab · TPS 62.34 · sin voz participativa
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,184,0,.08);border-radius:6px">
        🟠 Colorado · $94/hab · TPS 58.67 · agua 34.7% — cerca de meta
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(255,184,0,.08);border-radius:6px">
        🟡 La Pila · $93/hab · TPS 41.23 · agua 51.2% — cerca de meta
      </div>
    </div>
  </div>
  <div style="background:rgba(0,224,150,.05);border:1px solid rgba(0,224,150,.2);
              border-radius:12px;padding:16px">
    <div style="font-size:11px;font-weight:700;color:var(--green);margin-bottom:10px">
      ✅ ACCIONES PARA REDUCIR BRECHA · PRÓXIMO TRIMESTRE
    </div>
    <div style="display:flex;flex-direction:column;gap:6px">
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 Redirigir $280K adicionales a Isabel Muentes en Q2 POA
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,224,150,.08);border-radius:6px">
        🟢 Activar Gov Twin PNUD Agua Rural $2.4M · requiere calificación ≥55%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.08);border-radius:6px">
        🔵 Gender Bond $95K para luminarias Aníbal San Andrés · requiere PSG ≥30%
      </div>
      <div style="font-size:11px;color:var(--white);padding:6px 10px;
                  background:rgba(0,212,255,.08);border-radius:6px">
        🔵 Fondo Verde Clima GEF $180K · reforestación Colorado · elegible
      </div>
    </div>
  </div>
</div>"""

    # ── ASSEMBLER ─────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑥ INVERSIÓN POR HABITANTE",
        "Equidad Territorial · $/hab",
        f"Presupuesto total ${presupuesto_total/1_000_000:.2f}M · Brecha 2.8× · IET 44.80% · Corte ene–mar 2026",
        '<span class="badge badge-red">Brecha 2.8× Isabel Muentes</span>',
    )

    html = hdr + macro_html + bars_html + ejes_html + equidad_html

    render_page(html, show_tech=show_tech, height=1350)

    # ── CTAs Streamlit ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Sentinel · Estrategia de equidad territorial",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "El IET (Equidad Territorial) de Montecristi es 44.80%. "
                "La brecha per cápita es 5.4×: cabecera $217/hab vs Isabel Muentes $40/hab (H99 Q1-2026). "
                "El PDOT tiene como meta subir la inversión rural mínima a $80/hab al 2027. "
                "¿Qué mecanismo de redistribución presupuestaria es viable en Q2-2026 "
                "sin incumplir el equilibrio fiscal del COOTAD?"
            )
            st.rerun()
    with c2:
        if st.button("🗺️ Ver Territorio Digital", use_container_width=True):
            st.session_state["page"] = "geotwin"
            st.rerun()
    with c3:
        if st.button("🚨 Ver Señales de Alerta", use_container_width=True):
            st.session_state["page"] = "sat"
            st.rerun()
