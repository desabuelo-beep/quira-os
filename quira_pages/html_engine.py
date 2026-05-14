"""
QUIRA OS v0.1 — HTML Rendering Engine
Renderiza páginas vía st.components.v1.html() — iframe real, siempre funciona.
CSS/diseño basado en QUIRA_Gov_v1.1_DEMO.html (aprobado).
Dylus Lab © 2026
"""
import streamlit.components.v1 as components

# ── CSS COMPARTIDO (igual al DEMO.html aprobado) ──────────────────────────────
DEMO_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --navy-deep:#0A1128; --navy-mid:#0D1638; --navy-light:#162040;
  --navy-card:#111830; --cyan:#00D4FF; --cyan-dim:#00A8CC;
  --green:#00E096; --amber:#FFB800; --red:#FF4D6D;
  --purple:#7C5CFC; --pink:#FF6EA0;
  --white:#F0F4FF; --muted:#8892B0; --divider:#1E2D50;
  --font:'Inter',sans-serif; --mono:'JetBrains Mono',monospace;
}
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html, body {
  background: var(--navy-deep);
  color: var(--white);
  font-family: var(--font);
  font-size: 14px;
}
body { padding: 2px 2px 24px; }

/* CARDS */
.card {
  background: var(--navy-card);
  border: 1px solid var(--divider);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}
.card-title {
  font-size: 12px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: 10px;
}

/* GRIDS */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.grid-4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; }

/* GAUGE */
.gauge-label {
  font-size: 13px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .06em;
}
.tech-label { font-size: 10px; color: #4A5568; margin-top: 3px; display: none; }
body.tecnico .tech-label { display: block; }
.td-tech { display: none; }
body.tecnico .td-tech { display: table-cell; }

/* BADGES */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 8px; border-radius: 8px; font-size: 11px; font-weight: 600;
}
.badge-amber { background:rgba(255,183,0,.12); color:var(--amber); border:1px solid rgba(255,183,0,.25); }
.badge-green { background:rgba(0,224,150,.1);  color:var(--green); border:1px solid rgba(0,224,150,.2); }
.badge-red   { background:rgba(255,77,109,.1); color:var(--red);   border:1px solid rgba(255,77,109,.2); }
.badge-cyan  { background:rgba(0,212,255,.1);  color:var(--cyan);  border:1px solid rgba(0,212,255,.2); }
.badge-real  { background:rgba(0,224,150,.1);  color:var(--green); border:1px solid rgba(0,224,150,.2); }
.badge-proj  { background:rgba(255,183,0,.1);  color:var(--amber); border:1px solid rgba(255,183,0,.2); }

/* PROGRESS */
.prog-wrap { margin-bottom: 12px; }
.prog-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px; }
.prog-name { font-size: 13px; font-weight: 600; color: var(--white); }
.prog-val  { font-size: 14px; font-weight: 700; font-family: var(--mono); }
.prog-bar  { height: 6px; background: var(--divider); border-radius: 3px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 3px; transition: width 1s ease; }
.prog-fill.cyan   { background: var(--cyan); }
.prog-fill.green  { background: var(--green); }
.prog-fill.amber  { background: var(--amber); }
.prog-fill.red    { background: var(--red); }
.prog-fill.purple { background: var(--purple); }
.prog-sub { font-size: 11px; color: var(--muted); margin-top: 4px; line-height: 1.5; }

/* DUAL PANEL */
.dp-value { font-size: 36px; font-weight: 800; font-family: var(--mono); }
.dp-label { font-size: 12px; font-weight: 600; color: var(--muted); margin-top: 2px; }

/* PAGE TITLES */
.page-title { font-size: 22px; font-weight: 800; color: var(--white); margin-bottom: 4px; }
.page-sub   { font-size: 13px; color: var(--muted); margin-bottom: 20px; }
.section-lbl { font-size: 10px; font-weight: 700; color: var(--muted); margin-bottom: 6px; }

/* SECTION HEADER */
.section-hdr { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.section-hdr h3 { font-size: 14px; font-weight: 700; color: var(--white); }

/* TABLE */
.tbl { width:100%; border-collapse:collapse; font-size:12px; }
.tbl th {
  text-align:left; color:var(--muted); font-size:10px;
  text-transform:uppercase; letter-spacing:.08em;
  padding:8px 10px; border-bottom:1px solid var(--divider);
}
.tbl td { padding:8px 10px; border-bottom:1px solid rgba(30,45,80,.5); color:var(--white); }
.tbl tr:hover td { background:rgba(255,255,255,.02); }
.td-num { font-family:var(--mono); font-weight:700; }

/* CONGRUENCIA SEMÁFORO */
.cong-card {
  background:var(--navy-card); border:1px solid var(--divider);
  border-radius:12px; padding:16px 18px; margin-bottom:12px;
}

/* GT PIN MAP */
.gt-map {
  position:relative; background:var(--navy-light);
  border-radius:12px; height:260px; overflow:hidden;
  border:1px solid var(--divider);
}
.gt-parroquia {
  position:absolute; display:flex; flex-direction:column;
  align-items:center; gap:2px;
}
.gt-pin-dot {
  width:16px; height:16px; border-radius:50%;
  border:2px solid var(--navy-deep); transition:transform .2s;
  box-shadow:0 0 8px currentColor;
}
.gt-pin-label {
  font-size:9px; font-weight:600; color:var(--white);
  background:rgba(10,17,40,.8); padding:1px 5px;
  border-radius:4px; white-space:nowrap;
}

/* SENTINEL BUBBLE */
.sentinel-bubble {
  background:rgba(0,212,255,.04); border:1px solid rgba(0,212,255,.2);
  border-radius:12px; padding:14px 16px; margin-bottom:12px;
}

/* ANIMATIONS */
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:.4;} }
@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none} }
"""


def page_frame(content: str, show_tech: bool = False, extra_css: str = "") -> str:
    """
    Envuelve el contenido en un documento HTML completo con el CSS del DEMO.html.
    """
    body_class = "tecnico" if show_tech else ""
    return (
        "<!DOCTYPE html><html lang='es'><head>"
        "<meta charset='UTF-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<style>{DEMO_CSS}{extra_css}</style>"
        "</head>"
        f"<body class='{body_class}'>"
        f"<div style='animation:fadeIn .25s ease'>{content}</div>"
        "</body></html>"
    )


def render_page(content: str, show_tech: bool = False, height: int = 900) -> None:
    """
    Renderiza una sección de página vía st.components.v1.html().
    SIEMPRE funciona en Streamlit Cloud (iframe real).
    """
    html = page_frame(content, show_tech)
    components.html(html, height=height, scrolling=True)


# ── BLOQUES REUTILIZABLES ─────────────────────────────────────────────────────

def page_header(section_label: str, title: str, subtitle: str,
                badge_html: str = "") -> str:
    return (
        f'<div style="margin-bottom:6px;font-size:11px;color:var(--muted)">{section_label}</div>'
        f'<div class="page-title">{title}</div>'
        f'<div class="page-sub">{subtitle} {badge_html}</div>'
    )


def prog_bar(name: str, pct: float, color_class: str,
             value_str: str, sub: str, tech_label: str = "") -> str:
    tech = f'<div class="tech-label">↳ {tech_label}</div>' if tech_label else ""
    return (
        f'<div class="prog-wrap">'
        f'<div class="prog-header">'
        f'<div><div class="prog-name">{name}</div>{tech}</div>'
        f'<div class="prog-val" style="color:var(--{color_class})">{value_str}</div>'
        f'</div>'
        f'<div class="prog-bar"><div class="prog-fill {color_class}" style="width:{pct:.1f}%"></div></div>'
        f'<div class="prog-sub">{sub}</div>'
        f'</div>'
    )


def sentinel_cta(text: str) -> str:
    """Botón decorativo (sin onclick real en iframe — usar Streamlit button fuera)."""
    return (
        f'<div style="display:inline-block;margin-top:10px;padding:8px 14px;'
        f'background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.2);'
        f'border-radius:8px;font-size:11px;font-weight:600;color:var(--cyan)">'
        f'💬 {text}</div>'
    )
