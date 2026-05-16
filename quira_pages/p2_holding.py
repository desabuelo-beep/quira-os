"""
QUIRA OS v0.1 — P-02 Holding Sandbox (HPT-M)
Fiel al DEMO.html P-07 · st.components.v1.html() render
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header


# ── helpers ──────────────────────────────────────────────────────────────────
def _rgb(h: str) -> str:
    h = h.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,255,255"


def _mini_score_node(score: float, color: str, label: str, note: str) -> str:
    border_color = _rgb(color)
    return (
        f'<div style="padding:20px 14px;background:var(--navy-card);border-radius:12px;'
        f'border:1px solid rgba({border_color},.25);text-align:center">'
        f'<div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;'
        f'letter-spacing:.1em;margin-bottom:8px">{label}</div>'
        f'<div style="font-size:34px;font-weight:900;font-family:var(--mono);'
        f'color:{color};line-height:1">{score:.1f}%</div>'
        f'<div style="font-size:10px;color:var(--muted);margin-top:6px">{note}</div>'
        f'<div style="margin-top:10px;height:5px;background:var(--divider);border-radius:3px">'
        f'<div style="height:100%;width:{min(score,100):.1f}%;background:{color};border-radius:3px"></div>'
        f'</div></div>'
    )


def _entity_drawer(idx: int, emoji: str, nombre: str, tipo: str,
                   score: float, score_color: str, badge_class: str, badge_text: str,
                   what: str, why: str, impact: str, fix: str,
                   alert_html: str, sentinel_q: str) -> str:
    border_c = _rgb(score_color)
    arrow_color = "var(--amber)" if "amber" in badge_class else "var(--muted)"
    return f"""
<div style="margin-bottom:10px;border:1px solid rgba({border_c},.25);border-radius:12px;
            overflow:hidden;background:var(--navy-card)">
  <div onclick="var d=document.getElementById('hpt-{idx}');
                d.style.display=d.style.display==='none'?'block':'none';
                this.querySelector('.arrow-{idx}').textContent=d.style.display==='none'?'▼':'▲'"
       style="padding:14px 16px;cursor:pointer;display:flex;justify-content:space-between;
              align-items:center">
    <div style="display:flex;align-items:center;gap:16px;flex:1">
      <div style="font-size:28px">{emoji}</div>
      <div style="flex:1">
        <div style="font-size:15px;font-weight:800;color:var(--white)">{nombre}</div>
        <div style="font-size:11px;color:var(--muted);margin-top:3px">{tipo}</div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;min-width:220px">
        <div style="flex:1;height:8px;background:var(--divider);border-radius:4px">
          <div style="height:100%;width:{min(score,100):.1f}%;background:{score_color};border-radius:4px"></div>
        </div>
        <div style="font-size:18px;font-weight:900;font-family:var(--mono);
                    color:{score_color};min-width:52px;text-align:right">{score:.1f}%</div>
        <span class="badge {badge_class}" style="font-size:10px;padding:3px 9px">{badge_text}</span>
      </div>
    </div>
    <span class="arrow-{idx}" style="color:{arrow_color};font-size:11px;margin-left:12px">▼</span>
  </div>
  <div id="hpt-{idx}" style="display:none;padding:0 16px 16px">
    {alert_html}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px">
      <div style="padding:12px;background:rgba(0,224,150,.05);border-radius:8px;
                  border:1px solid rgba(0,224,150,.15)">
        <div style="font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;
                    letter-spacing:.1em;margin-bottom:6px">① ¿Qué pasó?</div>
        <div style="font-size:12px;color:var(--white);line-height:1.6">{what}</div>
      </div>
      <div style="padding:12px;background:rgba(0,212,255,.05);border-radius:8px;
                  border:1px solid rgba(0,212,255,.12)">
        <div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;
                    letter-spacing:.1em;margin-bottom:6px">② ¿Por qué pasó?</div>
        <div style="font-size:12px;color:var(--white);line-height:1.6">{why}</div>
      </div>
      <div style="padding:12px;background:rgba(124,92,252,.05);border-radius:8px;
                  border:1px solid rgba(124,92,252,.15)">
        <div style="font-size:10px;font-weight:700;color:var(--purple);text-transform:uppercase;
                    letter-spacing:.1em;margin-bottom:6px">③ ¿Qué impacto genera?</div>
        <div style="font-size:12px;color:var(--white);line-height:1.6">{impact}</div>
      </div>
      <div style="padding:12px;background:rgba(255,183,0,.05);border-radius:8px;
                  border:1px solid rgba(255,183,0,.12)">
        <div style="font-size:10px;font-weight:700;color:var(--amber);text-transform:uppercase;
                    letter-spacing:.1em;margin-bottom:6px">④ ¿Cómo {fix[0]}?</div>
        <div style="font-size:12px;color:var(--white);line-height:1.6">{fix[1]}</div>
      </div>
    </div>
    <div style="display:inline-block;margin-top:12px;padding:8px 12px;
                background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
                border-radius:8px;font-size:12px;color:var(--cyan)">
      💬 {sentinel_q}
    </div>
  </div>
</div>"""


# ── MAIN RENDER ───────────────────────────────────────────────────────────────
def render() -> None:
    data      = load_all()
    holding   = data["holding"]
    show_tech = is_tecnico()
    icgit     = holding.get("icgit_global", 53.56)

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑤ HOLDING SANDBOX",
        "Holding Sandbox · Operadores Públicos",
        "Dónde se degrada el holding, por qué, y cómo recuperarlo · HPT-M Q1-2026",
    )

    # ── DOCTRINA QUIRA ────────────────────────────────────────────────────────
    doctrina = """
<div style="padding:16px 20px;
            background:linear-gradient(135deg,rgba(0,212,255,.07) 0%,rgba(124,92,252,.04) 100%);
            border:1px solid rgba(0,212,255,.22);border-radius:12px;margin-bottom:16px">
  <div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;
              letter-spacing:.12em;margin-bottom:10px">⚡ Doctrina QUIRA · Holding Público Territorial</div>
  <div style="font-size:15px;font-weight:800;color:var(--white);line-height:1.65;
              font-style:italic;border-left:3px solid var(--cyan);padding-left:14px">
    "Una alcaldía puede ejecutar bien y aun así fallar si sus operadores degradan el territorio."
  </div>
  <div style="font-size:11px;color:var(--muted);margin-top:10px;line-height:1.6">
    QUIRA Gov no audita solo al GAD — audita el
    <strong style="color:var(--white)">Holding Público Territorial</strong> completo.
    Expandir cada operador para ver la causalidad institucional:
    qué pasó, cómo pasó y cómo corregirlo.
  </div>
</div>"""

    # ── 4-NODE SUMMARY GRID ───────────────────────────────────────────────────
    grid4 = (
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px">'
        + _mini_score_node(58.3,  "#FFB800", "GOBIERNO",    "GAD · Concejo")
        + _mini_score_node(71.7,  "#FFB800", "OPERADORES",  "3 entidades ↓ detalle")
        + _mini_score_node(44.8,  "#FF4D6D", "TERRITORIO",  "7 parroquias")
        + _mini_score_node(61.1,  "#FFB800", "ECOSISTEMA",  "ODS · BID · CAF")
        + '</div>'
    )

    # ── SECTION HEADER ────────────────────────────────────────────────────────
    sec_hdr = """
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <div style="font-size:13px;font-weight:700;color:var(--white)">Nodo Operadores · Diagnóstico por entidad</div>
  <span class="badge badge-cyan">Sandbox HPT-M · Haz clic para expandir</span>
</div>
<div style="font-size:11px;color:var(--muted);margin-bottom:10px">
  Cada entidad responde a su propia lógica de gobernanza. Expandir para ver:
  <strong style="color:var(--white)">qué pasó · por qué pasó · qué impacto genera · cómo corregir</strong>.
</div>"""

    # ── PRINCIPIO HOLDING STRIP ───────────────────────────────────────────────
    principio = """
<div style="display:flex;align-items:center;justify-content:center;gap:6px;
            padding:9px 14px;background:rgba(255,183,0,.05);
            border:1px solid rgba(255,183,0,.18);border-radius:8px;
            margin-bottom:14px;flex-wrap:wrap">
  <span style="font-size:10px;font-weight:700;color:var(--amber)">⚡ Principio del Holding:</span>
  <span style="font-size:10px;color:var(--muted)">
    Una entidad bajo umbral arrastra el Nodo completo, que arrastra el ICGI-T global.
  </span>
  <span style="font-size:11px;color:var(--white);font-family:var(--mono);
               background:rgba(0,0,0,.2);padding:3px 10px;border-radius:4px;white-space:nowrap">
    Entidad ↓ → Nodo ↓ → ICGI-T ↓
  </span>
</div>"""

    # ── ENTITY DRAWERS ────────────────────────────────────────────────────────
    bomberos = _entity_drawer(
        idx=1, emoji="🚒",
        nombre="Cuerpo de Bomberos",
        tipo="Seguridad y prevención de incendios · Entidad adscrita GAD",
        score=82.7, score_color="var(--green)",
        badge_class="badge-green", badge_text="✅ Referente",
        what="Bomberos lidera el Nodo Operadores con 82.7%, el único operador en nivel Gestión por Mandato. Ejecución presupuestaria al 78% a mayo 2026.",
        why="Estructura de mando único y planificación operativa propia. El POA institucional está alineado al PDOT y con PAC completo y registrado en el sistema.",
        impact="Jala el consolidado del Nodo hacia arriba. Es el modelo de referencia interna. Su gestión documenta 3 de los 5 indicadores verificables del ICGI-T.",
        fix=("capitalizar", "Replicar el modelo PAC-POA de Bomberos en EP Aseo. Documentar su metodología como estándar interno del Holding y usarla como evidencia ante BID/PNUD."),
        alert_html="",
        sentinel_q="Preguntar a SENTINEL sobre Bomberos",
    )

    patronato = _entity_drawer(
        idx=2, emoji="🤝",
        nombre="Patronato Municipal",
        tipo="Servicios sociales, discapacidad, adulto mayor · Entidad adscrita GAD",
        score=74.1, score_color="var(--green)",
        badge_class="badge-green", badge_text="✅ Gestión",
        what="Patronato mantiene 74.1% en nivel Gestión por Mandato. Ejecución del programa social al 68% con foco en grupos vulnerables y adulto mayor.",
        why="Gestión social con métricas de cobertura bien documentadas. Sin embargo, el indicador de Equidad en el Gasto (PSG) arrastra el score: género representa solo el 1% del devengado real.",
        impact="La brecha PSG del Patronato bloquea directamente los $95,000 del BID Lab Gender Bond. El holding pierde elegibilidad para ese fondo por una entidad que debería liderar la equidad.",
        fix=("corregir", "Reclasificar el presupuesto operativo del Patronato con marcadores de género. Activar el protocolo de devengado PSG-30% antes de agosto 2026 para acceder al Gender Bond en Q4."),
        alert_html="",
        sentinel_q="Preguntar a SENTINEL sobre Patronato",
    )

    ep_alerta = """
<div style="margin-top:12px;padding:10px 14px;background:rgba(255,183,0,.08);
            border-radius:8px;border-left:3px solid var(--amber);
            font-size:11px;color:var(--amber);margin-bottom:12px">
  ⚠️ <strong>Alerta activa:</strong> EP Aseo arrastra el Nodo Operadores 13.4 puntos
  por debajo de Bomberos. Es la brecha operativa más costosa del holding.
</div>"""

    ep_aseo = _entity_drawer(
        idx=3, emoji="🗑️",
        nombre="EP Aseo Municipal",
        tipo="Recolección, tratamiento y disposición final de residuos · Empresa pública",
        score=58.4, score_color="var(--amber)",
        badge_class="badge-amber", badge_text="⚠️ Alerta",
        what="EP Aseo registra 58.4%, límite inferior del nivel Transición Crítica. Ejecución presupuestaria al 42%, la más baja de todos los operadores del Holding.",
        why="Tres causas convergentes: (1) retrasos en certificación presupuestaria Q4-2025, (2) 4 procesos PAC no iniciados para equipamiento, (3) rotación de director técnico sin protocolo de transferencia.",
        impact="Riesgo de discontinuidad en cobertura de recolección en parroquias rurales. Deprime el Nodo Operadores y arrastra la Congruencia Operativa al 47.2%. Bloquea elegibilidad para Fondo Verde GEF.",
        fix=("corregir", "Pasos inmediatos: (1) Certificar presupuesto retenido antes del 30-jun, (2) iniciar los 4 procesos PAC en SERCOP esta semana, (3) aplicar protocolo de gestión por continuidad del cargo técnico."),
        alert_html=ep_alerta,
        sentinel_q="Preguntar a SENTINEL sobre EP Aseo",
    )

    # ── RESUMEN OPERATIVO ─────────────────────────────────────────────────────
    resumen = """
<div style="padding:12px 16px;background:rgba(0,212,255,.04);border-radius:10px;
            border:1px solid rgba(0,212,255,.12);display:flex;gap:14px;align-items:flex-start">
  <div style="font-size:20px;flex-shrink:0">🧭</div>
  <div style="flex:1">
    <div style="font-size:12px;font-weight:700;color:var(--cyan);margin-bottom:6px">
      Resumen del Nodo Operadores · Q1-2026
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px">
      <div style="text-align:center;padding:6px;background:rgba(34,197,94,.06);border-radius:6px">
        <div style="font-size:14px;font-weight:800;color:var(--green)">82.7%</div>
        <div style="font-size:10px;color:var(--muted)">🚒 Bomberos</div>
        <div style="font-size:9px;color:var(--green)">▲ Referente</div>
      </div>
      <div style="text-align:center;padding:6px;background:rgba(34,197,94,.06);border-radius:6px">
        <div style="font-size:14px;font-weight:800;color:var(--green)">74.1%</div>
        <div style="font-size:10px;color:var(--muted)">🤝 Patronato</div>
        <div style="font-size:9px;color:var(--amber)">→ PSG pendiente</div>
      </div>
      <div style="text-align:center;padding:6px;background:rgba(255,183,0,.05);border-radius:6px">
        <div style="font-size:14px;font-weight:800;color:var(--amber)">58.4%</div>
        <div style="font-size:10px;color:var(--muted)">🗑️ EP Aseo</div>
        <div style="font-size:9px;color:var(--red)">▼ Arrastra</div>
      </div>
    </div>
    <div style="font-size:11px;color:var(--muted);line-height:1.6">
      El promedio consolidado de <strong style="color:var(--amber)">71.7% oculta la tensión interna</strong>:
      Bomberos hala hacia arriba, EP Aseo arrastra hacia abajo.
      La causalidad institucional explicable — no el promedio — es lo que convierte datos en acción de gobierno.
    </div>
  </div>
</div>"""

    # ── CAUSALIDAD SISTÉMICA ──────────────────────────────────────────────────
    causalidad = f"""
<div style="margin-top:14px;padding:14px;background:var(--navy-card);
            border-radius:10px;border:1px solid rgba(0,212,255,.12)">
  <div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;
              letter-spacing:.1em;margin-bottom:12px">
    🔗 Causalidad sistémica · Cómo cada entidad impacta el ICGI-T
  </div>
  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:14px">
    <div style="padding:14px 16px;background:rgba(34,197,94,.08);border-radius:10px;
                border:1px solid rgba(34,197,94,.2);text-align:center;min-width:100px">
      <div style="font-size:10px;color:var(--muted)">🚒 Bomberos</div>
      <div style="font-size:24px;font-weight:900;color:var(--green);font-family:var(--mono)">82.7%</div>
      <div style="font-size:9px;color:var(--green)">▲ referente</div>
    </div>
    <div style="color:var(--muted);font-size:20px;padding:0 2px">+</div>
    <div style="padding:14px 16px;background:rgba(34,197,94,.08);border-radius:10px;
                border:1px solid rgba(34,197,94,.2);text-align:center;min-width:100px">
      <div style="font-size:10px;color:var(--muted)">🤝 Patronato</div>
      <div style="font-size:24px;font-weight:900;color:var(--green);font-family:var(--mono)">74.1%</div>
      <div style="font-size:9px;color:var(--amber)">→ PSG gap</div>
    </div>
    <div style="color:var(--muted);font-size:20px;padding:0 2px">+</div>
    <div style="padding:14px 16px;background:rgba(255,183,0,.08);border-radius:10px;
                border:1px solid rgba(255,183,0,.3);text-align:center;min-width:100px">
      <div style="font-size:10px;color:var(--muted)">🗑️ EP Aseo</div>
      <div style="font-size:24px;font-weight:900;color:var(--amber);font-family:var(--mono)">58.4%</div>
      <div style="font-size:9px;color:var(--red)">▼ arrastra</div>
    </div>
    <div style="color:var(--muted);font-size:22px;padding:0 8px;font-weight:300">→</div>
    <div style="padding:14px 16px;background:rgba(255,183,0,.06);border-radius:10px;
                border:1px solid rgba(255,183,0,.2);text-align:center;min-width:116px">
      <div style="font-size:10px;color:var(--muted)">Nodo Operadores</div>
      <div style="font-size:24px;font-weight:900;color:var(--amber);font-family:var(--mono)">71.7%</div>
      <div style="font-size:9px;color:var(--muted)">promedio ocultador</div>
    </div>
    <div style="color:var(--muted);font-size:22px;padding:0 8px;font-weight:300">→</div>
    <div style="padding:14px 16px;background:rgba(255,77,109,.06);border-radius:10px;
                border:1px solid rgba(255,77,109,.2);text-align:center;min-width:106px">
      <div style="font-size:10px;color:var(--muted)">ICGI-T Global</div>
      <div style="font-size:24px;font-weight:900;color:var(--red);font-family:var(--mono)">{icgit:.2f}%</div>
      <div style="font-size:9px;color:var(--red)">Transición Crítica</div>
    </div>
  </div>
  <div style="font-size:11px;color:var(--muted);line-height:1.6;padding-top:8px;
              border-top:1px solid rgba(255,255,255,.05)">
    Si EP Aseo sube de 58.4% → 70%: el Nodo Operadores pasa a 75.6%, con
    <strong style="color:var(--white)">impacto positivo en el ICGI-T global</strong> —
    acercando Montecristi al umbral de
    <em style="color:var(--amber)">Gestión por Mandato (69.93%)</em> exigido por el PDOT al 2027.
  </div>
</div>
<div style="display:inline-block;margin-top:12px;padding:8px 12px;
            background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.15);
            border-radius:8px;font-size:12px;color:var(--cyan)">
  🤖 Analizar todo el Holding con SENTINEL
</div>"""

    # ── FICHA POR ENTIDAD · H71 Gold Master ──────────────────────────────────
    def _ep_card(emoji, nombre, cod, icgi, icgi_color, icgi_c,
                 impacto_pct, ejecutado_k, tiene_pei, pei_nota, avep_label) -> str:
        pei_color = "green" if tiene_pei else "red"
        pei_icon  = "✅" if tiene_pei else "❌"
        bar_w     = min(icgi, 100)
        bar_clr   = icgi_color
        return (
            f'<div style="background:var(--navy-card);border-radius:14px;padding:16px 18px;'
            f'border:1px solid rgba({icgi_c},.22);position:relative;overflow:hidden">'
            f'<div style="position:absolute;top:0;left:0;width:100%;height:3px;'
            f'background:linear-gradient(90deg,{icgi_color},{icgi_color}44)"></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">'
            f'<div>'
            f'<div style="font-size:13px;font-weight:800;color:var(--white)">{emoji} {nombre}</div>'
            f'<div style="font-size:10px;color:var(--muted);margin-top:2px">{cod}</div>'
            f'</div>'
            f'<div style="text-align:right">'
            f'<div style="font-size:28px;font-weight:900;font-family:var(--mono);'
            f'color:{icgi_color};line-height:1">{icgi:.1f}%</div>'
            f'<div style="font-size:9px;color:var(--muted);margin-top:1px">ICGI-T</div>'
            f'</div>'
            f'</div>'
            f'<div style="height:5px;background:rgba(255,255,255,.07);border-radius:3px;margin-bottom:12px">'
            f'<div style="height:100%;width:{bar_w:.1f}%;background:{bar_clr};border-radius:3px;opacity:.85"></div>'
            f'</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'
            f'<div style="text-align:center;background:rgba(255,255,255,.04);border-radius:8px;padding:8px 4px">'
            f'<div style="font-size:15px;font-weight:800;color:var(--cyan)">{impacto_pct}%</div>'
            f'<div style="font-size:9px;color:var(--muted);margin-top:2px">Impacto Territorial</div>'
            f'</div>'
            f'<div style="text-align:center;background:rgba(255,255,255,.04);border-radius:8px;padding:8px 4px">'
            f'<div style="font-size:15px;font-weight:800;color:var(--amber)">${ejecutado_k}K</div>'
            f'<div style="font-size:9px;color:var(--muted);margin-top:2px">Ejecutado Q1</div>'
            f'</div>'
            f'<div style="text-align:center;background:rgba(255,255,255,.04);border-radius:8px;padding:8px 4px">'
            f'<div style="font-size:15px;font-weight:800;color:var(--{pei_color})">{pei_icon}</div>'
            f'<div style="font-size:9px;color:var(--muted);margin-top:2px">PEI {pei_nota}</div>'
            f'</div>'
            f'</div>'
            f'<div style="margin-top:10px;font-size:10px;color:var(--{pei_color});font-weight:700">'
            f'AVEP: {avep_label}'
            f'</div>'
            f'</div>'
        )

    ficha = (
        '<div style="margin-top:18px">'
        '<div style="font-size:10px;font-weight:700;color:var(--cyan);text-transform:uppercase;'
        'letter-spacing:.12em;margin-bottom:12px">'
        '📊 Radar por Entidad · H71 Gold Master · Q1-2026</div>'
        '<div class="grid-2" style="gap:12px">'
        + _ep_card("🚒", "Cuerpo de Bomberos", "CB-01 · Emergencias · COESCOP",
                   82.7, "#38A169", "56,161,105",
                   78, 178, True, "vigente", "✅ Gestión por Mandato")
        + _ep_card("🤝", "Patronato Municipal", "AD-01 · Desarrollo Social · LOSEP",
                   74.1, "#38A169", "56,161,105",
                   92, 312, True, "vigente", "✅ Gestión por Mandato")
        + _ep_card("🗑️", "EP Aseo Municipal", "EP-01 · Residuos Sólidos · LOEP",
                   58.4, "#D69E2E", "214,158,46",
                   85, 245, True, "vigente", "⚡ Transición Crítica — arrastra nodo")
        + _ep_card("🏛️", "GAD Central", "ALC-01 · 12 Direcciones · COOTAD",
                   61.2, "#D69E2E", "214,158,46",
                   100, 5147, False, "N/A — gobierno",  "⚡ Transición Crítica")
        + '</div>'
        '<div style="margin-top:10px;font-size:10px;color:var(--muted);line-height:1.5;'
        'padding:8px 12px;background:rgba(255,255,255,.03);border-radius:8px">'
        '💡 <strong style="color:var(--white)">Lectura HPT-M:</strong> '
        'Impacto Territorial = % de metas PDOT con trazabilidad en territorio · '
        'Ejecutado Q1 = devengado eSIGEF corte 2026-04-30 · '
        'PEI = Plan Estratégico Institucional activo · '
        'Fuente: H71_EP_ADSCRITAS · H90_PRESUPUESTO_CONSOLIDADO'
        '</div>'
        '</div>'
    )

    # ── TECH NOTE ─────────────────────────────────────────────────────────────
    tech = ""
    if show_tech:
        tech = """
<div style="margin-top:16px;font-size:9px;color:rgba(255,255,255,.2);
            border-top:1px solid rgba(255,255,255,.04);padding-top:8px">
  🔧 Fuente: SIAP-ICPI H71 · H71b · H90 · HPT-M canónico · Corte Q1-2026
</div>"""

    # ── ASSEMBLE & RENDER ─────────────────────────────────────────────────────
    html = (
        hdr + doctrina + grid4
        + sec_hdr + principio
        + bomberos + patronato + ep_aseo
        + resumen + causalidad + ficha + tech
    )
    render_page(html, show_tech=show_tech, height=2400)

    # Native Streamlit CTA after iframe
    c1, c2 = st.columns(2, gap="small")
    with c1:
        if st.button("🔮 Analizar Holding con Sentinel", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                "¿Cómo están funcionando las empresas del Holding Municipal "
                "(Bomberos, Patronato, EP Aseo) y cuáles representan mayor riesgo "
                "de gobernanza para el GAD de Montecristi?"
            )
            st.rerun()
    with c2:
        if st.button("📊 Ver Tablero Ejecutivo", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
