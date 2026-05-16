"""
QUIRA OS — View: Dashboard
Responsabilidad única: generar el HTML del tablero ejecutivo.
Sin Streamlit. Sin cálculos. Solo presentación.
Dylus Lab © 2026
"""
from __future__ import annotations
from models.dashboard import DashboardData
from views.html_engine import page_header, prog_bar, sentinel_cta


def gauge_card(d: DashboardData, show_tech: bool) -> str:
    tech = lambda t: f'<div class="tech-label">↳ {t}</div>' if show_tech else ""
    return f"""
<div class="card" style="display:flex;flex-direction:column;align-items:center;gap:10px;padding:24px">
  <div class="gauge-label">Gobernanza Territorial</div>
  {tech("ICGI-T · Motor: ICPI canónico")}

  <svg width="220" height="130" viewBox="0 0 220 130" style="overflow:visible">
    <path d="M 22 115 A 88 88 0 0 1 198 115"
          fill="none" stroke="rgba(30,45,80,.9)" stroke-width="14" stroke-linecap="round"/>
    <path d="M 22 115 A 88 88 0 0 1 198 115"
          fill="none" stroke="rgba(229,62,62,.18)" stroke-width="14" stroke-linecap="butt"
          stroke-dasharray="{d.arc*0.20:.1f} {d.arc:.1f}" stroke-dashoffset="0"/>
    <path d="M 22 115 A 88 88 0 0 1 198 115"
          fill="none" stroke="{d.color}" stroke-width="14" stroke-linecap="round"
          stroke-dasharray="{d.arc:.1f}" stroke-dashoffset="{d.arc_score:.1f}"/>
    <path d="M 22 115 A 88 88 0 0 1 198 115"
          fill="none" stroke="#00D4FF" stroke-width="3" stroke-linecap="butt" opacity=".8"
          stroke-dasharray="1 {d.arc:.1f}" stroke-dashoffset="{d.arc_meta:.1f}"/>
    <text x="110" y="96"  text-anchor="middle" fill="{d.color}"
          font-size="32" font-weight="800" font-family="JetBrains Mono,monospace">{d.score:.2f}%</text>
    <text x="110" y="116" text-anchor="middle" fill="#8892B0"
          font-size="10" font-family="Inter,sans-serif">Calificación · Montecristi 2026</text>
  </svg>

  <div style="background:rgba({d.color_rgb},.12);border:1px solid rgba({d.color_rgb},.3);
              border-radius:8px;padding:8px 20px;font-size:13px;font-weight:700;color:{d.color}">
    {d.avep_emoji} {d.avep_label}
  </div>
  <div style="font-size:11px;color:var(--muted);text-align:center">
    Mayo 2026 · FT={d.ti_raw:.2f}% · Mandato 2023-2027
  </div>
  <div style="display:flex;gap:8px;justify-content:center;margin-top:2px;flex-wrap:wrap">
    <div style="font-size:10px;padding:3px 8px;border-radius:10px;
                background:rgba(245,158,11,.1);color:var(--amber)">
      2025 ref: {d.h2025:.2f}% ✅
    </div>
    <div style="font-size:10px;padding:3px 8px;border-radius:10px;
                background:rgba(0,212,255,.08);color:var(--cyan)">
      ⏳ Q1 parcial · proj: {d.proj:.2f}%
    </div>
  </div>
  {sentinel_cta("Preguntar a SENTINEL")}
  {tech("ICGI-T · ICPI canónico · SIAP v1.0222")}
</div>"""


def doble_lente_card(d: DashboardData, show_tech: bool) -> str:
    tech = lambda t: f'<div class="tech-label">↳ {t}</div>' if show_tech else ""
    return f"""
<div class="card" style="padding:14px">
  <div style="font-size:10px;font-weight:700;color:var(--muted);
              text-transform:uppercase;margin-bottom:10px">
    Doble Lente · Inversión Q1-2026
  </div>
  <div class="grid-2" style="gap:10px">
    <div style="text-align:center;padding:10px;background:var(--navy-light);border-radius:8px">
      <div class="dp-value" style="font-size:28px;color:var(--muted)">{d.ti_raw:.1f}%</div>
      <div class="dp-label">Inversión Ejecutada</div>
      {tech("Ti_raw · ancla auditora")}
      <div style="font-size:10px;color:var(--muted);margin-top:4px">
        ${d.inv_m:.2f}M de ${d.ppto_m:.1f}M
      </div>
    </div>
    <div style="text-align:center;padding:10px;background:rgba(0,224,150,.05);
                border-radius:8px;border:1px solid rgba(0,224,150,.15)">
      <div class="dp-value" style="font-size:28px;color:var(--green)">{d.ti_norm:.1f}%</div>
      <div class="dp-label">Ritmo de Inversión</div>
      {tech("Ti_norm · semáforo temporal")}
      <div style="font-size:10px;color:var(--green);margin-top:4px">✓ Ritmo correcto para mayo</div>
    </div>
  </div>
</div>"""


def brechas_card(d: DashboardData, show_tech: bool) -> str:
    t = lambda s: s if show_tech else ""
    return (
        '<div class="card">'
        '<div class="card-title">Brechas Estructurales · Causa Real</div>'
        + prog_bar("Salud Financiera",      d.isp_v, "red",
                   f"{d.isp_v:.2f}%", "Componente crítico · requiere atención prioritaria",
                   t("ISP · peso estructural"))
        + prog_bar("Eficiencia Operacional", d.ied_v, "amber",
                   f"{d.ied_v:.2f}%", "Bajo umbral operativo · 12 direcciones evaluadas",
                   t("IED · rendimiento direcciones"))
        + prog_bar("Equidad en el Gasto",   d.psg_v, "red",
                   f"{d.psg_v:.2f}%", "Pinkwashing detectado · Gender Bond bloqueado",
                   t("PSG · mandato de género"))
        + """
  <div class="prog-wrap" style="border-top:1px solid rgba(124,92,252,.15);padding-top:10px;margin-top:2px">
    <div class="prog-header">
      <div><div class="prog-name">Gobernanza Participativa</div></div>
      <div class="prog-val" style="color:var(--purple)">calibrando</div>
    </div>
    <div class="prog-bar">
      <div style="width:100%;height:100%;border-radius:4px;
                  background:repeating-linear-gradient(45deg,rgba(124,92,252,.18),rgba(124,92,252,.18) 3px,transparent 3px,transparent 7px);
                  border:1px dashed rgba(124,92,252,.35)"></div>
    </div>
    <div class="prog-sub" style="color:rgba(124,92,252,.75)">
      Componente en validación · asambleas · presupuesto participativo · activo Q2-2026
    </div>
  </div>
</div>"""
    )


def sentinel_rec_card(d: DashboardData) -> str:
    return f"""
<div class="card" style="background:rgba(0,224,150,.04);border-color:rgba(0,224,150,.2);margin-bottom:14px">
  <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
    <div style="font-size:12px;color:var(--green);font-weight:600">🏙 SENTINEL recomienda:</div>
    <div style="font-size:12px;color:var(--muted);flex:1">
      3 acciones de palanca para Q2 → proyección {d.proj:.2f}% ({d.proj - d.score:+.1f} pts)
    </div>
    {sentinel_cta("Ver plan Q2")}
  </div>
</div>"""


def mandato_card(d: DashboardData) -> str:
    def bar(year: str, val: float, color: str, nota: str, highlight: bool = False,
            en_curso: bool = False, proyeccion: bool = False) -> str:
        border = "border:1px solid rgba(0,212,255,.15);background:rgba(0,212,255,.04);" if en_curso else ""
        style_bar = (
            f"repeating-linear-gradient(45deg,rgba(34,197,94,.15),rgba(34,197,94,.15) 4px,"
            f"transparent 4px,transparent 8px);border:1px dashed rgba(34,197,94,.3)"
            if proyeccion else
            f"background:linear-gradient(90deg,rgba({color},.35),rgba({color},.55));height:100%;border-radius:4px"
        )
        year_color = "var(--cyan)" if en_curso else ("var(--white)" if highlight else "var(--muted)")
        return f"""
<div style="margin-bottom:10px;padding:{'8px' if en_curso else '0'};border-radius:8px;{border}">
  <div style="display:flex;align-items:center;gap:8px{'margin-bottom:4px' if en_curso else ''}">
    <div style="width:60px;font-size:11px;color:{year_color};font-weight:{'700' if highlight or en_curso else '600'};flex-shrink:0">{year}</div>
    <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
      <div style="width:{val:.2f}%;height:16px;border-radius:4px;{style_bar}"></div>
    </div>
    <div style="width:52px;font-size:12px;font-weight:700;color:var(--{'cyan' if en_curso else ('green' if highlight else 'amber')});text-align:right;flex-shrink:0">{'~' if proyeccion else ''}{val:.2f}%</div>
    <div style="font-size:10px;color:var(--muted);width:88px;flex-shrink:0">{nota}</div>
  </div>
</div>"""

    delta_2524 = d.h2025 - d.h2024
    delta_2423 = d.h2024 - d.h2023
    delta_tot  = d.h2025 - d.h2023

    return f"""
<div class="card">
  <div style="display:flex;align-items:center;justify-content:space-between;
              margin-bottom:14px;flex-wrap:wrap;gap:8px">
    <div>
      <div style="font-size:11px;font-weight:700;color:var(--cyan);text-transform:uppercase;letter-spacing:.1em">
        📈 Curva del Mandato 2023-2027 · Calificación histórica
      </div>
      <div style="font-size:11px;color:var(--muted);margin-top:2px">
        Trayectoria de Gobernanza · GAD Montecristi · Evidencia institucional auditada
      </div>
    </div>
    <div style="font-size:10px;padding:3px 10px;border-radius:10px;
                background:rgba(34,197,94,.1);color:var(--green);font-weight:700">
      +{delta_tot:.2f} pp · 2023→2025 ▲
    </div>
  </div>

  {bar("2023",    d.h2023, "245,158,11", "proxy eSIGEF")}
  {bar("2024",    d.h2024, "245,158,11", f"▲ +{delta_2423:.2f} pp")}
  {bar("2025",    d.h2025, "34,197,94",  f"▲ +{delta_2524:.2f} pp ★", highlight=True)}

  <div style="margin-bottom:10px;padding:8px;background:rgba(0,212,255,.04);
              border:1px solid rgba(0,212,255,.15);border-radius:8px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">
      <div style="width:60px;font-size:11px;color:var(--cyan);font-weight:700;flex-shrink:0">2026-Q1</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden;position:relative">
        <div style="width:{d.h2026:.2f}%;background:linear-gradient(90deg,rgba(0,212,255,.3),rgba(0,212,255,.5));height:100%;border-radius:4px;position:relative">
          <div style="position:absolute;right:0;top:0;height:100%;width:3px;
                      background:rgba(0,212,255,.9);animation:pulse 1.5s infinite"></div>
        </div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--cyan);text-align:right;flex-shrink:0">{d.h2026:.2f}%</div>
      <div style="font-size:10px;color:var(--cyan);width:88px;flex-shrink:0">⏳ en curso</div>
    </div>
    <div style="margin-left:68px;font-size:10px;color:var(--muted);line-height:1.5">
      Solo marzo (Ti={d.ti_raw:.2f}%) — <strong style="color:var(--cyan)">normal para Q1.</strong>
      Proyección anual: <strong style="color:var(--cyan)">{d.proj:.2f}%</strong>
    </div>
  </div>

  <div style="margin-bottom:4px">
    <div style="display:flex;align-items:center;gap:8px">
      <div style="width:60px;font-size:11px;color:var(--muted);font-weight:600;flex-shrink:0">2027</div>
      <div style="flex:1;background:var(--divider);border-radius:4px;height:16px;overflow:hidden">
        <div style="width:{d.h2027:.2f}%;height:16px;border-radius:4px;
                    background:repeating-linear-gradient(45deg,rgba(34,197,94,.15),rgba(34,197,94,.15) 4px,transparent 4px,transparent 8px);
                    border:1px dashed rgba(34,197,94,.3)"></div>
      </div>
      <div style="width:52px;font-size:12px;font-weight:700;color:var(--muted);text-align:right;flex-shrink:0">~{d.h2027:.2f}%</div>
      <div style="font-size:10px;color:var(--muted);width:88px;flex-shrink:0">proyección</div>
    </div>
    <div style="margin-left:68px;font-size:10px;color:var(--muted);margin-top:2px">
      Meta cierre de mandato: ≥70% 🟢 Gestión por Mandato
    </div>
  </div>

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
</div>"""


def sat_card(sats: list) -> str:
    if not sats:
        return ""
    rows = "".join(
        f'<tr>'
        f'<td style="white-space:nowrap">{s.get("emoji","⚠")} <strong>{s.get("sat_id","")}</strong></td>'
        f'<td>{s.get("nombre","")}</td>'
        f'<td><span style="color:{s.get("color","#D69E2E")};font-weight:600">{s.get("nivel","")}</span></td>'
        f'<td style="font-size:11px;color:var(--muted)">{s.get("impacto","")}</td>'
        f'</tr>'
        for s in sats[:5]
    )
    return (
        '<div class="card" style="margin-top:4px">'
        '<div class="card-title">🚨 Señales de Alerta Institucional · Activas</div>'
        '<table class="tbl"><thead><tr>'
        '<th>ID</th><th>Alerta</th><th>Nivel</th><th>Impacto cuantificado</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
    )


def build_html(d: DashboardData, show_tech: bool) -> str:
    """Ensambla el HTML completo del Dashboard."""
    hdr = page_header(
        "I · ENTENDER", "Dashboard Gobernanza",
        "GAD Montecristi · Q1-2026 ·",
        '<span class="badge badge-real">REAL Q1-2026</span>',
    )
    return (
        hdr
        + f'<div class="grid-2" style="align-items:start;gap:20px;margin-bottom:16px">'
        + gauge_card(d, show_tech)
        + f'<div style="display:flex;flex-direction:column;gap:12px">'
        + doble_lente_card(d, show_tech)
        + brechas_card(d, show_tech)
        + '</div></div>'
        + sentinel_rec_card(d)
        + mandato_card(d)
        + sat_card(d.sats)
    )
