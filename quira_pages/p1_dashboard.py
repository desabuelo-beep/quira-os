"""
QUIRA OS v0.1 — P-01 Tablero Ejecutivo · ICGI-T
Diseño fiel a QUIRA_Gov_v1.1_DEMO.html (pantalla p01)
Renderizado vía st.components.v1.html() — iframe real, siempre funciona.
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all, get_sat_counts
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header, prog_bar, sentinel_cta


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    icgit  = data["icgit"]
    score  = icgit["score"]            # 53.56
    color  = icgit.get("color", "#FFB800")

    # ── AVEP color → CSS class ────────────────────────────────────────────────
    _color_map = {
        "#E53E3E": "red", "#E67E22": "amber", "#D69E2E": "amber",
        "#38A169": "green", "#3182CE": "cyan", "#FFB800": "amber",
        "#FF4D6D": "red",  "#00E096": "green", "#00D4FF": "cyan",
    }
    color_cls = _color_map.get(color, "amber")  # noqa — kept for future use

    # ── Investment numbers ────────────────────────────────────────────────────
    ppto    = icgit.get("presupuesto_total", 26_689_147)
    inv     = icgit.get("inversion_ejecutada", 7_820_000)
    ti_raw  = icgit.get("ti_raw", 23.75)
    ti_norm = icgit.get("ti_norm", 70.0)
    proj    = icgit.get("proyeccion", 65.77)
    inv_m   = inv / 1_000_000
    ppto_m  = ppto / 1_000_000

    # ── Historical scores ─────────────────────────────────────────────────────
    hist  = icgit.get("historico", {})
    h2023 = hist.get("2023", 57.36)
    h2024 = hist.get("2024", 67.11)
    h2025 = hist.get("2025", 69.93)
    h2026 = hist.get("2026_q1", 53.56)
    h2027 = hist.get("2026_proj", 65.77)

    # ── Brechas indices ───────────────────────────────────────────────────────
    indices = data["indices"]
    isp_v   = (indices.get("ISP",  {}).get("valor") or 14.58)
    ied_v   = (indices.get("IED",  {}).get("valor") or 33.99)
    psg_v   = (indices.get("PSG",  {}).get("valor") or 12.83)

    # ── AVEP label ────────────────────────────────────────────────────────────
    avep_label = icgit.get("avep", "Transición Crítica")
    avep_emoji = icgit.get("avep_emoji", "🟠")

    # ── SAT data ──────────────────────────────────────────────────────────────
    tech = show_tech

    color_rgb = _hex_rgb(color)

    # ── Gauge arc length (semicircle r=88 → π*88 ≈ 276.5) ────────────────────
    arc = 276.5
    arc_score = arc * (1.0 - score / 100.0)
    arc_meta  = arc * (1.0 - 70.0  / 100.0)

    # ══════════════════════════════════════════════════════════════════════════
    html = f"""
{page_header("I · ENTENDER", "Dashboard Gobernanza",
             "GAD Montecristi · Q1-2026 ·",
             '<span class="badge badge-real">REAL Q1-2026</span>')}

<!-- GAUGE + DOBLE LENTE -->
<div class="grid-2" style="align-items:start;gap:20px;margin-bottom:16px">

  <!-- Gauge card -->
  <div class="card" style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:24px">
    <div class="gauge-label">Gobernanza Territorial</div>
    <div class="tech-label">&#8618; ICGI-T · Motor: ICPI canónico</div>

    <svg width="220" height="130" viewBox="0 0 220 130" style="overflow:visible">
      <!-- Track -->
      <path d="M 22 115 A 88 88 0 0 1 198 115"
            fill="none" stroke="rgba(30,45,80,.9)" stroke-width="14" stroke-linecap="round"/>
      <!-- AVEP bands (subtle) -->
      <path d="M 22 115 A 88 88 0 0 1 198 115"
            fill="none" stroke="rgba(229,62,62,.18)" stroke-width="14" stroke-linecap="butt"
            stroke-dasharray="{arc*0.20:.1f} {arc:.1f}" stroke-dashoffset="0"/>
      <!-- Score arc -->
      <path d="M 22 115 A 88 88 0 0 1 198 115"
            fill="none" stroke="{color}" stroke-width="14" stroke-linecap="round"
            stroke-dasharray="{arc:.1f}" stroke-dashoffset="{arc_score:.1f}"/>
      <!-- Meta 70% marker -->
      <path d="M 22 115 A 88 88 0 0 1 198 115"
            fill="none" stroke="#00D4FF" stroke-width="3" stroke-linecap="butt" opacity=".8"
            stroke-dasharray="1 {arc:.1f}" stroke-dashoffset="{arc_meta:.1f}"/>
      <!-- Score text -->
      <text x="110" y="96" text-anchor="middle" fill="{color}"
            font-size="32" font-weight="800" font-family="JetBrains Mono,monospace">{score:.2f}%</text>
      <text x="110" y="116" text-anchor="middle" fill="#8892B0"
            font-size="10" font-family="Inter,sans-serif">ICGI-T · Montecristi 2026</text>
    </svg>

    <div style="background:rgba({color_rgb},.12);border:1px solid rgba({color_rgb},.3);
                border-radius:8px;padding:8px 20px;font-size:13px;font-weight:700;color:{color}">
      {avep_emoji} {avep_label}
    </div>
    <div style="font-size:11px;color:var(--muted);text-align:center">
      Mayo 2026 · FT={ti_raw:.2f}% · Mandato 2023-2027
    </div>
    <div style="display:flex;gap:8px;justify-content:center;margin-top:2px;flex-wrap:wrap">
      <div style="font-size:10px;padding:3px 8px;border-radius:10px;
                  background:rgba(245,158,11,.1);color:var(--amber)">2025 ref: {h2025:.2f}% ✅</div>
      <div style="font-size:10px;padding:3px 8px;border-radius:10px;
                  background:rgba(0,212,255,.08);color:var(--cyan)">&#8987; Q1 parcial · proj: {proj:.2f}%</div>
    </div>
    {sentinel_cta("Preguntar a SENTINEL")}
    {'<div style="font-size:9px;color:var(--muted);margin-top:4px">&#8618; ICGI-T · ICPI canónico · SIAP v1.0222</div>' if tech else ''}
  </div>

  <!-- Doble lente + Brechas -->
  <div style="display:flex;flex-direction:column;gap:12px">
    <div class="card" style="padding:14px">
      <div style="font-size:10px;font-weight:700;color:var(--muted);
                  text-transform:uppercase;margin-bottom:10px">Doble Lente · Inversión Q1-2026</div>
      <div class="grid-2" style="gap:10px">
        <div style="text-align:center;padding:10px;background:var(--navy-light);border-radius:8px">
          <div class="dp-value" style="font-size:28px;color:var(--muted)">{ti_raw:.1f}%</div>
          <div class="dp-label">Inversión Ejecutada</div>
          <div class="tech-label">&#8618; Ti_raw · ancla auditora</div>
          <div style="font-size:10px;color:var(--muted);margin-top:4px">${inv_m:.2f}M de ${ppto_m:.1f}M</div>
        </div>
        <div style="text-align:center;padding:10px;background:rgba(0,224,150,.05);
                    border-radius:8px;border:1px solid rgba(0,224,150,.15)">
          <div class="dp-value" style="font-size:28px;color:var(--green)">{ti_norm:.1f}%</div>
          <div class="dp-label">Ritmo de Inversión</div>
          <div class="tech-label">&#8618; Ti_norm · semáforo temporal</div>
          <div style="font-size:10px;color:var(--green);margin-top:4px">&#10003; Ritmo correcto para mayo</div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Brechas Estructurales · Causa Real</div>
      {prog_bar("Salud Financiera", isp_v, "red",
                f"{isp_v:.2f}%", "Impacto estimado: −8.2 pts en Gobernanza",
                "ISP · peso estructural" if tech else "")}
      {prog_bar("Eficiencia Operacional", ied_v, "amber",
                f"{ied_v:.2f}%", "Bajo umbral operativo · 12 direcciones evaluadas",
                "IED · rendimiento direcciones" if tech else "")}
      {prog_bar("Equidad en el Gasto", psg_v, "red",
                f"{psg_v:.2f}%", "Pinkwashing detectado · acceso a Gender Bond bloqueado",
                "PSG · mandato de género" if tech else "")}
      <!-- IGP — calibrando -->
      <div class="prog-wrap" style="border-top:1px solid rgba(124,92,252,.15);padding-top:10px;margin-top:2px">
        <div class="prog-header">
          <div>
            <div class="prog-name">Gobernanza Participativa</div>
            <div class="tech-label">&#8618; IGP · CPCCS / LOPC</div>
          </div>
          <div class="prog-val" style="color:var(--purple)">calibrando</div>
        </div>
        <div class="prog-bar">
          <div style="width:100%;height:100%;border-radius:4px;
                      background:repeating-linear-gradient(45deg,rgba(124,92,252,.18),rgba(124,92,252,.18) 3px,transparent 3px,transparent 7px);
                      border:1px dashed rgba(124,92,252,.35)"></div>
        </div>
        <div class="prog-sub" style="color:rgba(124,92,252,.75)">
          Componente ICGI-T en validación · asambleas · presupuesto participativo · activo Q2-2026
        </div>
      </div>
    </div>
  </div>
</div>

<!-- SENTINEL CTA -->
<div class="card" style="background:rgba(0,224,150,.04);border-color:rgba(0,224,150,.2);margin-bottom:14px">
  <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
    <div style="font-size:12px;color:var(--green);font-weight:600">&#127963; SENTINEL recomienda:</div>
    <div style="font-size:12px;color:var(--muted);flex:1">
      3 acciones de palanca para Q2 &#8594; proyección {proj:.2f}% ({proj - score:+.1f} pts)
    </div>
    {sentinel_cta("Ver plan Q2")}
  </div>
</div>

<!-- CURVA DEL MANDATO 2023-2027 -->
<div class="card">
  <div style="display:flex;align-items:center;justify-content:space-between;
              margin-bottom:14px;flex-wrap:wrap;gap:8px">
    <div>
      <div style="font-size:11px;font-weight:700;color:var(--cyan);
                  text-transform:uppercase;letter-spacing:.1em">
        &#128200; Curva del Mandato 2023-2027 · ICGI-T Serie Histórica
      </div>
      <div style="font-size:11px;color:var(--muted);margin-top:2px">
        Trayectoria de Gobernanza · GAD Montecristi · Evidencia institucional auditada
      </div>
    </div>
    <div style="font-size:10px;padding:3px 10px;border-radius:10px;
                background:rgba(34,197,94,.1);color:var(--green);font-weight:700">
      +{h2025 - h2023:.2f} pp · 2023&#8594;2025 &#9650;
    </div>
  </div>

  <!-- 2023 -->
  <div style="margin-bottom:10px">
    <div style="display:flex;align-items:center;gap:8px">
      <div style="width:60px;font-size:11px;color:var(--muted);font-weight:600;flex-shrink:0">2023</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
        <div style="width:{h2023:.2f}%;background:linear-gradient(90deg,rgba(245,158,11,.35),rgba(245,158,11,.55));height:100%;border-radius:4px"></div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--amber);text-align:right;flex-shrink:0">{h2023:.2f}%</div>
      <div style="font-size:10px;color:var(--muted);width:88px;flex-shrink:0">proxy eSIGEF</div>
    </div>
  </div>

  <!-- 2024 -->
  <div style="margin-bottom:10px">
    <div style="display:flex;align-items:center;gap:8px">
      <div style="width:60px;font-size:11px;color:var(--muted);font-weight:600;flex-shrink:0">2024</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
        <div style="width:{h2024:.2f}%;background:linear-gradient(90deg,rgba(245,158,11,.5),rgba(245,158,11,.7));height:100%;border-radius:4px"></div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--amber);text-align:right;flex-shrink:0">{h2024:.2f}%</div>
      <div style="font-size:10px;color:var(--green);width:88px;flex-shrink:0">&#9650; +{h2024 - h2023:.2f} pp</div>
    </div>
  </div>

  <!-- 2025 auditado -->
  <div style="margin-bottom:10px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
      <div style="width:60px;font-size:11px;color:var(--white);font-weight:700;flex-shrink:0">2025</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
        <div style="width:{h2025:.2f}%;background:linear-gradient(90deg,rgba(34,197,94,.5),rgba(34,197,94,.75));height:100%;border-radius:4px"></div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--green);text-align:right;flex-shrink:0">{h2025:.2f}%</div>
      <div style="font-size:10px;color:var(--green);width:88px;flex-shrink:0">&#9650; +{h2025 - h2024:.2f} pp &#9733;</div>
    </div>
    <div style="margin-left:68px;font-size:10px;color:var(--cyan)">
      &#9733; Primer ICPI canónico auditado (metodología SIAP-ICPI completa)
    </div>
  </div>

  <!-- 2026 Q1 en curso -->
  <div style="margin-bottom:10px;padding:8px;background:rgba(0,212,255,.04);
              border:1px solid rgba(0,212,255,.15);border-radius:8px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
      <div style="width:60px;font-size:11px;color:var(--cyan);font-weight:700;flex-shrink:0">2026-Q1</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden;position:relative">
        <div style="width:{h2026:.2f}%;background:linear-gradient(90deg,rgba(0,212,255,.3),rgba(0,212,255,.5));height:100%;border-radius:4px;position:relative">
          <div style="position:absolute;right:0;top:0;height:100%;width:3px;
                      background:rgba(0,212,255,.9);animation:pulse 1.5s infinite"></div>
        </div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--cyan);text-align:right;flex-shrink:0">{h2026:.2f}%</div>
      <div style="font-size:10px;color:var(--cyan);width:88px;flex-shrink:0">&#8987; en curso</div>
    </div>
    <div style="margin-left:68px;font-size:10px;color:var(--muted);line-height:1.5">
      Solo marzo (Ti={ti_raw:.2f}%) — <strong style="color:var(--cyan)">normal para Q1.</strong>
      No comparable con cierres anuales.<br>
      Proyección anual 2026: <strong style="color:var(--cyan)">{proj:.2f}%</strong>
    </div>
  </div>

  <!-- 2027 proyección -->
  <div style="margin-bottom:4px">
    <div style="display:flex;align-items:center;gap:8px">
      <div style="width:60px;font-size:11px;color:var(--muted);font-weight:600;flex-shrink:0">2027</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
        <div style="width:{h2027:.2f}%;height:100%;border-radius:4px;
                    background:repeating-linear-gradient(45deg,rgba(34,197,94,.15),rgba(34,197,94,.15) 4px,transparent 4px,transparent 8px);
                    border:1px dashed rgba(34,197,94,.3)"></div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--muted);text-align:right;flex-shrink:0">~{h2027:.2f}%</div>
      <div style="font-size:10px;color:var(--muted);width:88px;flex-shrink:0">proyección</div>
    </div>
    <div style="margin-left:68px;font-size:10px;color:var(--muted);margin-top:2px">
      Meta cierre de mandato: &#8805;70% &#128994; Gestión por Mandato
    </div>
  </div>

  <!-- Leyenda -->
  <div style="margin-top:12px;padding-top:10px;border-top:1px solid var(--divider);
              display:flex;align-items:center;gap:12px;flex-wrap:wrap">
    <span style="font-size:10px;color:var(--muted)">
      <span style="display:inline-block;width:10px;height:10px;background:rgba(245,158,11,.5);border-radius:2px;margin-right:3px;vertical-align:middle"></span>Proxy eSIGEF
    </span>
    <span style="font-size:10px;color:var(--muted)">
      <span style="display:inline-block;width:10px;height:10px;background:rgba(34,197,94,.6);border-radius:2px;margin-right:3px;vertical-align:middle"></span>Canónico auditado
    </span>
    <span style="font-size:10px;color:var(--muted)">
      <span style="display:inline-block;width:10px;height:10px;background:rgba(0,212,255,.4);border-radius:2px;margin-right:3px;vertical-align:middle"></span>Parcial Q1
    </span>
    <span style="font-size:10px;color:var(--muted)">
      <span style="display:inline-block;width:10px;height:10px;border:1px dashed rgba(34,197,94,.4);border-radius:2px;margin-right:3px;vertical-align:middle"></span>Proyección
    </span>
  </div>
</div>

<!-- SAT RESUMEN -->
{_sat_table(data)}
"""

    render_page(html, show_tech=show_tech, height=1000)

    # ── Botones nativos Streamlit (fuera del iframe) ──────────────────────────
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💬 Preguntar a Sentinel sobre el ICGI-T",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.rerun()
    with col2:
        if st.button("📊 Ver Congruencias de Gobernanza", use_container_width=True):
            st.session_state["page"] = "congruencias"
            st.rerun()


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _hex_rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,183,0"


def _sat_table(data: dict) -> str:
    sats = data.get("sats", [])
    if not sats:
        return ""
    rows = ""
    for s in sats[:5]:
        c = s.get("color", "#D69E2E")
        rows += (
            f'<tr><td style="white-space:nowrap">{s.get("emoji","⚠")} '
            f'<strong>{s.get("sat_id","")}</strong></td>'
            f'<td>{s.get("nombre","")}</td>'
            f'<td><span style="color:{c};font-weight:600">{s.get("nivel","")}</span></td>'
            f'<td style="font-size:11px;color:var(--muted)">{s.get("impacto","")}</td></tr>'
        )
    return (
        '<div class="card" style="margin-top:4px">'
        '<div class="card-title">&#128680; Sistema de Alertas Tempranas (SAT) · Activas</div>'
        '<table class="tbl"><thead><tr>'
        '<th>ID</th><th>Alerta</th><th>Nivel</th><th>Impacto cuantificado</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
    )
