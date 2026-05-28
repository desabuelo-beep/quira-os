"""
QUIRA OS — View: Landing + Login  (Sprint Landing v2 · 2026-05-27)
Pantalla cero: identidad institucional, jerarquía doctrinal, sin ruido visual.

Cambios v2:
  · Tagline → "Sistema Operativo de Coherencia Institucional"
  · QUIRA Institucional: card dominante (visual primer plano)
  · QUIRA Operations: 4to módulo (sala situacional, En construcción)
  · Sin botones redundantes — cada card es su propio CTA
  · Lenguaje institucional (Bloomberg / Palantir gov / Centro de Mando)

Sin imports de Streamlit. Sin lógica de negocio. Solo presentación.
Dylus Lab © 2026
"""
from __future__ import annotations

# ── SVG del logo QUIRA ────────────────────────────────────────────────────────
QUIRA_SVG = (
    '<svg viewBox="0 0 100 118" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" style="width:56px;height:66px">'
    '<rect x="6"  y="107" width="88" height="11" rx="4"/>'
    '<rect x="44" y="75"  width="12" height="32" rx="3"/>'
    '<path d="M14,80 L14,44 A36,36 0 0,1 86,44 L86,80 L74,80 L74,44 A24,24 0 0,0 26,44 L26,80 Z"/>'
    '<path d="M50,26 A12,12 0 0,1 62,38 Q62,56 50,74 Q38,56 38,38 A12,12 0 0,1 50,26 Z"/>'
    '<path d="M14,80 Q14,60 0,60 L0,70 Q8,70 8,80 Z M0,60 L0,107 L8,107 L8,60 Z"/>'
    '<path d="M86,80 Q86,60 100,60 L100,70 Q92,70 92,80 Z M100,60 L100,107 L92,107 L92,60 Z"/>'
    '</svg>'
)


# ── CSS landing + login ───────────────────────────────────────────────────────
CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CHROME HIDE ── */
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer { display:none !important }

/* ── FONDO ── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 45% at 50% -5%,
            rgba(0,212,255,.065) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 82% 85%,
            rgba(124,92,252,.04) 0%, transparent 60%),
        #080F1E !important;
    min-height:100vh;
}
[data-testid="stMain"] .block-container {
    padding:0 !important; max-width:100% !important;
}

/* ── HERO ── */
.ql-hero {
    display:flex; flex-direction:column; align-items:center;
    padding:48px 20px 26px; text-align:center;
}
.ql-logo {
    color:#00D4FF; margin-bottom:14px;
    animation:ql-glow 2.8s ease-in-out infinite;
}
@keyframes ql-glow {
    0%,100%{filter:drop-shadow(0 0 16px rgba(0,212,255,.4))}
    50%{filter:drop-shadow(0 0 34px rgba(0,212,255,.78))}
}
.ql-brand {
    font:900 34px/1 'Inter',sans-serif;
    color:#F0F4FF; letter-spacing:-.03em; margin-bottom:7px;
}
.ql-os {
    font:600 15px/1.3 'Inter',sans-serif;
    color:rgba(240,244,255,.72);
    letter-spacing:-.005em; margin-bottom:6px;
}
.ql-pow {
    font:500 8px/1 'JetBrains Mono',monospace;
    color:rgba(0,212,255,.5);
    letter-spacing:.14em; text-transform:uppercase; margin-bottom:10px;
}
.ql-tagline {
    font:400 11px/1.5 'Inter',sans-serif;
    color:rgba(136,146,176,.6); margin-bottom:0;
}

/* ── CARD DOMINANTE — INSTITUCIONAL ── */
.ql-card-inst {
    background:linear-gradient(135deg,
        rgba(0,212,255,.032) 0%, rgba(8,15,35,.8) 100%);
    border:1px solid rgba(0,212,255,.18);
    border-left:3px solid rgba(0,212,255,.52);
    border-radius:16px;
    padding:24px 26px 18px;
    margin-bottom:0;
    transition:border-color .2s, box-shadow .2s;
}
.ql-card-inst:hover {
    border-color:rgba(0,212,255,.3);
    box-shadow:0 0 28px rgba(0,212,255,.06);
}
.ql-card-inst.active {
    border-color:rgba(0,212,255,.45) !important;
    background:rgba(0,212,255,.05) !important;
}
.ql-card-inst-badge {
    display:inline-block;
    font:700 7px/1 'JetBrains Mono',monospace;
    color:rgba(0,212,255,.48); letter-spacing:.12em;
    text-transform:uppercase;
    background:rgba(0,212,255,.06);
    border:1px solid rgba(0,212,255,.13);
    border-radius:4px; padding:3px 8px; margin-bottom:12px;
}
.ql-card-inst-icon { font-size:38px; display:block; margin-bottom:8px; }
.ql-card-inst-name {
    font:800 21px/1 'Inter',sans-serif;
    color:#F0F4FF; letter-spacing:-.02em; margin-bottom:7px;
}
.ql-card-inst-desc {
    font:400 12px/1.55 'Inter',sans-serif;
    color:rgba(240,244,255,.62); margin-bottom:6px;
}
.ql-card-inst-meta {
    font:500 9px/1 'JetBrains Mono',monospace;
    color:rgba(0,212,255,.35); letter-spacing:.06em;
}

/* ── DIVIDER INSTITUCIONAL / SECUNDARIO ── */
.ql-divider {
    border:none;
    border-top:1px solid rgba(255,255,255,.04);
    margin:10px 0 6px;
}

/* ── CARDS SECUNDARIAS ── */
.ql-card {
    background:rgba(8,14,32,.75);
    border:1px solid rgba(255,255,255,.07);
    border-radius:14px;
    padding:20px 16px 16px;
    text-align:center;
    margin-bottom:0;
    min-height:132px;
    transition:border-color .2s;
}
.ql-card:hover { border-color:rgba(255,255,255,.13); }
.ql-card.active {
    border-color:rgba(0,212,255,.3) !important;
    background:rgba(0,212,255,.04) !important;
}
.ql-card.ops {
    border-color:rgba(249,115,22,.1) !important;
    background:rgba(249,115,22,.02) !important;
}
.ql-card-icon { font-size:28px; margin-bottom:9px; display:block; }
.ql-card-name {
    font:700 13px/1 'Inter',sans-serif;
    color:#F0F4FF; margin-bottom:6px; letter-spacing:-.01em;
}
.ql-card-desc {
    font:400 10px/1.5 'Inter',sans-serif;
    color:rgba(136,146,176,.7);
}

/* ── BOTONES ── */

/* Primary — ENTRAR AL SISTEMA */
[data-testid="stButton"] button[kind="primary"],
[data-testid="stButton"] button[data-testid="baseButton-primary"] {
    background:linear-gradient(135deg,
        rgba(0,6,20,1) 0%, rgba(0,212,255,.08) 100%) !important;
    border:1px solid rgba(0,212,255,.3) !important;
    color:#00D4FF !important;
    font:800 11px/1 'Inter',sans-serif !important;
    border-radius:10px !important;
    letter-spacing:.08em !important;
    padding:15px 20px !important;
    height:auto !important;
    text-transform:uppercase !important;
    transition:all .2s ease !important;
    width:100% !important;
}
[data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stButton"] button[data-testid="baseButton-primary"]:hover {
    background:linear-gradient(135deg,
        rgba(0,212,255,.13) 0%, rgba(124,92,252,.13) 100%) !important;
    border-color:rgba(0,212,255,.6) !important;
    box-shadow:0 0 22px rgba(0,212,255,.1) !important;
}

/* Secondary — card CTAs */
[data-testid="stButton"] button[kind="secondary"],
[data-testid="stButton"] button[data-testid="baseButton-secondary"] {
    background:rgba(255,255,255,.04) !important;
    border:1px solid rgba(255,255,255,.09) !important;
    color:rgba(240,244,255,.48) !important;
    font:600 10px/1 'Inter',sans-serif !important;
    border-radius:8px !important;
    letter-spacing:.04em !important;
    padding:10px 14px !important;
    height:auto !important;
    transition:all .2s !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background:rgba(255,255,255,.08) !important;
    border-color:rgba(255,255,255,.18) !important;
    color:rgba(240,244,255,.82) !important;
}
[data-testid="stButton"] button:disabled {
    opacity:.28 !important;
    cursor:default !important;
}

/* Ops ghost button override (JS adds .ql-ops-btn) */
button.ql-ops-btn,
.ql-ops-section button {
    background:transparent !important;
    border:1px solid rgba(255,255,255,.05) !important;
    color:rgba(136,146,176,.18) !important;
    font:500 8px/1 'JetBrains Mono',monospace !important;
    letter-spacing:.07em !important;
    border-radius:5px !important;
    padding:5px 12px !important;
}
button.ql-ops-btn:hover,
.ql-ops-section button:hover {
    border-color:rgba(249,115,22,.22) !important;
    color:rgba(249,115,22,.42) !important;
    background:transparent !important;
}

/* ── FORM DE LOGIN ── */
div[data-testid="stForm"] {
    background:rgba(6,12,26,.92) !important;
    border:1px solid rgba(0,212,255,.17) !important;
    border-radius:16px !important;
    padding:22px 26px 18px !important;
    backdrop-filter:blur(16px) !important;
    margin-top:0 !important;
}
.ql-form-title {
    font:700 10px/1 'Inter',sans-serif; color:rgba(136,146,176,.7);
    text-transform:uppercase; letter-spacing:.1em;
    text-align:center; margin-bottom:10px;
}
.ql-badge {
    display:block; width:fit-content; margin:0 auto 16px;
    background:rgba(0,212,255,.06); border:1px solid rgba(0,212,255,.18);
    border-radius:20px; padding:4px 14px;
    font:500 8px/1 'JetBrains Mono',monospace; color:rgba(0,212,255,.7);
}

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-baseweb="select"] > div {
    background:#030A18 !important;
    border:1px solid rgba(255,255,255,.1) !important;
    color:#F0F4FF !important; border-radius:8px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:rgba(0,212,255,.5) !important;
    box-shadow:0 0 0 1px rgba(0,212,255,.15) !important;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    color:rgba(136,146,176,.7) !important; font-size:10px !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:.08em !important;
}
div[data-baseweb="select"] svg { color:#8892B0 !important }

/* Botón submit del form */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"] {
    background:linear-gradient(135deg,#00D4FF 0%,#7C5CFC 100%) !important;
    color:#060E1C !important; font-weight:900 !important;
    font-size:12px !important; border:none !important;
    border-radius:10px !important; letter-spacing:.07em !important;
    width:100% !important; padding:14px !important;
    text-transform:uppercase !important;
}
div[data-testid="stForm"] button:hover { opacity:.88 !important }

/* ── TRUST BADGES ── */
.ql-trust {
    display:grid; grid-template-columns:1fr 1fr; gap:6px;
    max-width:370px; margin:14px auto 12px;
}
.ql-trust-item {
    display:flex; align-items:center; gap:7px;
    background:rgba(255,255,255,.02);
    border:1px solid rgba(255,255,255,.06);
    border-radius:8px; padding:7px 10px;
}
.ql-trust-label {
    font:700 8px/1 'Inter',sans-serif;
    text-transform:uppercase; letter-spacing:.05em;
}
.ql-trust-sub { font:400 8px/1 'Inter',sans-serif; color:#8892B0; }

/* ── FOOTER ── */
.ql-footer {
    text-align:center; padding:10px 20px 26px;
    font:400 9px/1.8 'JetBrains Mono',monospace;
    color:rgba(136,146,176,.18);
}

/* ── MOBILE ── */
@media(max-width:680px){
    .ql-brand { font-size:26px }
    .ql-os { font-size:13px }
    .ql-hero { padding:30px 16px 18px }
    div[data-testid="stForm"] { padding:18px 14px !important }
    .ql-card-inst { padding:18px 18px 14px }
    .ql-card { min-height:auto }
}

/* ── STRIP GAPS ── */
[data-testid="stVerticalBlock"]>[data-testid="stVerticalBlockBorderWrapper"] {
    gap:0 !important;
}
</style>

<script>
(function(){
  /* autocomplete password */
  var _o1=new MutationObserver(function(){
    var p=document.querySelector('input[type=password]');
    if(p){p.autocomplete='current-password';_o1.disconnect();}
  });
  _o1.observe(document.body,{childList:true,subtree:true});
})();
(function(){
  /* tag ops ghost button so CSS can target it */
  function _tagOps(){
    document.querySelectorAll('[data-testid="stButton"] button').forEach(function(b){
      if((b.innerText||'').trim().toLowerCase().indexOf('acceso operacional')!==-1){
        b.classList.add('ql-ops-btn');
        var w=b.closest('[data-testid="stButton"]');
        if(w) w.classList.add('ql-ops-section');
      }
    });
  }
  var _o2=new MutationObserver(_tagOps);
  _o2.observe(document.body,{childList:true,subtree:true});
})();
</script>"""


# ── Hero ─────────────────────────────────────────────────────────────────────

def landing_hero() -> str:
    """Bloque hero: logo + marca + OS tagline institucional."""
    return (
        f'<div class="ql-hero">'
        f'<div class="ql-logo">{QUIRA_SVG}</div>'
        f'<div class="ql-brand">QUIRA Intelligence</div>'
        f'<div class="ql-os">Sistema Operativo de Coherencia Institucional</div>'
        f'<div class="ql-pow">Development by Dylus Lab</div>'
        f'<div class="ql-tagline">'
        f'Observabilidad territorial · Riesgo institucional · Decisión ejecutiva'
        f'</div>'
        f'</div>'
    )


# ── Cards individuales ────────────────────────────────────────────────────────

def card_institucional_html(active: bool = False) -> str:
    """Card dominante — QUIRA Institucional (primer plano visual)."""
    cls = "ql-card-inst" + (" active" if active else "")
    return (
        f'<div class="{cls}">'
        f'<div class="ql-card-inst-badge">Sistema activo · Acceso restringido</div>'
        f'<div class="ql-card-inst-icon">🏛</div>'
        f'<div class="ql-card-inst-name">QUIRA Institucional</div>'
        f'<div class="ql-card-inst-desc">'
        f'Centro de comando institucional para Alcaldía y Holding Municipal. '
        f'Observabilidad ejecutiva para decisión pública en tiempo real.'
        f'</div>'
        f'<div class="ql-card-inst-meta">'
        f'TGI · ICPI · SAT · POA · PAC · LOTAIP · Holding Municipal'
        f'</div>'
        f'</div>'
    )


def card_ciudadano_html(active: bool = False) -> str:
    """Card secundaria — QUIRA Ciudadano."""
    cls = "ql-card" + (" active" if active else "")
    return (
        f'<div class="{cls}">'
        f'<span class="ql-card-icon">🌎</span>'
        f'<div class="ql-card-name">QUIRA Ciudadano</div>'
        f'<div class="ql-card-desc">'
        f'Transparencia territorial, ejecución pública y seguimiento ciudadano.'
        f'</div>'
        f'</div>'
    )


def card_cooperacion_html(active: bool = False) -> str:
    """Card secundaria — QUIRA Cooperación."""
    cls = "ql-card" + (" active" if active else "")
    return (
        f'<div class="{cls}">'
        f'<span class="ql-card-icon">📑</span>'
        f'<div class="ql-card-name">QUIRA Cooperación</div>'
        f'<div class="ql-card-desc">'
        f'Datos longitudinales y evidencia territorial para investigación y cooperación.'
        f'</div>'
        f'</div>'
    )


def card_operations_html() -> str:
    """Card secundaria — QUIRA Operations (en construcción)."""
    return (
        f'<div class="ql-card ops">'
        f'<span class="ql-card-icon">⚡</span>'
        f'<div class="ql-card-name">QUIRA Operations</div>'
        f'<div class="ql-card-desc">'
        f'Monitoreo institucional en tiempo real y gestión situacional.'
        f'</div>'
        f'</div>'
    )


# ── Form + Badges + Footer ────────────────────────────────────────────────────

def form_header() -> str:
    """Badge + etiqueta dentro del card de login."""
    return (
        '<div class="ql-form-title">Acceso Institucional</div>'
        '<div style="text-align:center">'
        '<span class="ql-badge">Acceso Restringido · QUIRA Institucional</span>'
        '</div>'
    )


def trust_badges() -> str:
    """Mini-badges de seguridad."""
    badges = [
        ("#00E096", "ACCESO PROTEGIDO",        "Cifrado institucional"),
        ("#00D4FF", "SESIÓN TEMPORAL",          "Expira en 60 minutos"),
        ("#7C5CFC", "INTENTOS MONITOREADOS",    "Bloqueo tras 3 fallos"),
        ("#FFB800", "ACTIVIDAD AUDITADA",       "Registro de accesos"),
    ]
    items = "".join(
        f'<div class="ql-trust-item">'
        f'<div><div class="ql-trust-label" style="color:{c}">{lbl}</div>'
        f'<div class="ql-trust-sub">{sub}</div></div>'
        f'</div>'
        for c, lbl, sub in badges
    )
    return f'<div class="ql-trust">{items}</div>'


def footer() -> str:
    """Footer institucional genérico (multi-GAD)."""
    return (
        '<div class="ql-footer">'
        'QUIRA Intelligence · Dylus Lab © 2026<br>'
        '<span style="color:rgba(255,184,0,.22)">Infraestructura de gobernanza pública</span>'
        '</div>'
    )


# ── Backward compat ───────────────────────────────────────────────────────────

def platform_cards(selected: str = "") -> str:
    """Deprecated — usar card_*_html() individuales. Retorna vacío."""
    return ""


def splash_top(corte: str = "") -> str:
    return landing_hero()


def splash_bottom(gad: str = "", corte: str = "") -> str:
    return footer()


def error_html(msg: str) -> str:
    return (
        f'<div style="background:rgba(255,77,109,.1);border:1px solid rgba(255,77,109,.3);'
        f'border-radius:8px;padding:10px 14px;color:#FF8FA3;font-size:12px;'
        f'font-family:Inter,sans-serif;margin-top:4px">⚠️ {msg}</div>'
    )
