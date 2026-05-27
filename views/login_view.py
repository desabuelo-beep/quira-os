"""
QUIRA OS — View: Landing + Login
Landing pública con 3 plataformas + formulario de acceso institucional.
Responsabilidad única: HTML/CSS listos para renderizar.
Sin imports de Streamlit. Sin lógica de negocio. Solo presentación.
Dylus Lab © 2026
"""
from __future__ import annotations

# ── SVG del logo QUIRA ────────────────────────────────────────────────────────
QUIRA_SVG = (
    '<svg viewBox="0 0 100 118" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" style="width:60px;height:71px">'
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400&display=swap');

/* Chrome */
[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer { display:none !important }

/* Fondo */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 50% at 50% -10%,
        rgba(0,212,255,.08) 0%, transparent 55%),
        #09101F !important;
    min-height:100vh;
}
[data-testid="stMain"] .block-container {
    padding:0 !important; max-width:100% !important;
}

/* ── HERO ── */
.ql-hero {
    display:flex; flex-direction:column; align-items:center;
    padding:52px 20px 36px; text-align:center;
}
.ql-logo { color:#00D4FF; margin-bottom:16px;
    animation:ql-glow 2.6s ease-in-out infinite; }
@keyframes ql-glow {
    0%,100%{filter:drop-shadow(0 0 18px rgba(0,212,255,.45))}
    50%{filter:drop-shadow(0 0 38px rgba(0,212,255,.85))} }
.ql-brand   { font:800 32px/1 'Inter',sans-serif; color:#F0F4FF;
    letter-spacing:-.02em; margin-bottom:6px }
.ql-pow     { font:700 10px/1 'Inter',sans-serif; color:#00D4FF;
    letter-spacing:.12em; text-transform:uppercase; margin-bottom:10px }
.ql-tagline { font:500 14px/1.4 'Inter',sans-serif; color:#8892B0; margin-bottom:0 }

/* ── PLATAFORMAS ── */
.ql-platforms {
    display:grid; grid-template-columns:repeat(3,1fr);
    gap:14px; max-width:860px; margin:0 auto; padding:0 20px 32px;
}
.ql-card {
    background:rgba(13,22,56,.65);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px; padding:28px 22px 24px;
    backdrop-filter:blur(10px);
    transition:border-color .2s, transform .2s;
    cursor:pointer; text-align:center;
}
.ql-card:hover { border-color:rgba(0,212,255,.3); transform:translateY(-2px) }
.ql-card.active  {
    border-color:rgba(0,212,255,.5) !important;
    background:rgba(0,212,255,.06) !important;
}
.ql-card.disabled { opacity:.45; cursor:default }
.ql-card.disabled:hover { transform:none; border-color:rgba(255,255,255,.08) }

.ql-card-icon { font-size:34px; margin-bottom:12px; display:block }
.ql-card-name { font:700 15px/1 'Inter',sans-serif; color:#F0F4FF;
    margin-bottom:7px; letter-spacing:-.01em }
.ql-card-desc { font:400 11px/1.5 'Inter',sans-serif; color:#8892B0;
    margin-bottom:16px }
.ql-card-btn {
    display:inline-block; border-radius:8px; padding:7px 18px;
    font:700 11px/1 'Inter',sans-serif; letter-spacing:.05em;
    text-transform:uppercase; border:1px solid;
}
.ql-card-btn.btn-cyan {
    background:rgba(0,212,255,.12); border-color:rgba(0,212,255,.35);
    color:#00D4FF;
}
.ql-card-btn.btn-green {
    background:rgba(0,224,150,.12); border-color:rgba(0,224,150,.35);
    color:#00E096;
}
.ql-card-btn.btn-gray {
    background:rgba(255,255,255,.05); border-color:rgba(255,255,255,.15);
    color:#8892B0;
}

/* ── FORM de login (dentro del stForm) ── */
div[data-testid="stForm"] {
    background: rgba(10,17,40,.85) !important;
    border: 1px solid rgba(0,212,255,.2) !important;
    border-radius: 16px !important;
    padding: 26px 30px 22px !important;
    backdrop-filter: blur(16px) !important;
    margin-top:0 !important;
}
.ql-form-title {
    font:700 11px/1 'Inter',sans-serif; color:#8892B0;
    text-transform:uppercase; letter-spacing:.1em;
    text-align:center; margin-bottom:12px;
}
.ql-badge {
    display:block; width:fit-content; margin:0 auto 20px;
    background:rgba(0,212,255,.08); border:1px solid rgba(0,212,255,.22);
    border-radius:20px; padding:4px 14px;
    font:500 10px/1 'JetBrains Mono',monospace; color:#00D4FF;
}

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-baseweb="select"] > div {
    background:#060E1C !important; border:1px solid #1A2844 !important;
    color:#F0F4FF !important; border-radius:8px !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-baseweb="select"] > div:focus-within { border-color:#00D4FF !important }
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"]  label {
    color:#8892B0 !important; font-size:10px !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:.08em !important;
}
div[data-baseweb="select"] svg { color:#8892B0 !important }

/* Botón login */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg,#00D4FF,#7C5CFC) !important;
    color: #09101F !important; font-weight:800 !important;
    font-size:12px !important; border:none !important;
    border-radius:10px !important; letter-spacing:.06em !important;
    width:100% !important;
}
div[data-testid="stForm"] button:hover { opacity:.88 !important }

/* ── TRUST BADGES ── */
.ql-trust {
    display:grid; grid-template-columns:1fr 1fr; gap:8px;
    max-width:390px; margin:0 auto 16px;
}
.ql-trust-item {
    display:flex; align-items:center; gap:8px;
    background:rgba(255,255,255,.03);
    border:1px solid rgba(255,255,255,.07);
    border-radius:8px; padding:8px 10px;
}
.ql-trust-label { font:700 9px/1 'Inter',sans-serif;
    text-transform:uppercase; letter-spacing:.05em }
.ql-trust-sub   { font:400 9px/1 'Inter',sans-serif; color:#8892B0 }

/* ── FOOTER ── */
.ql-footer {
    text-align:center; padding:16px 20px 32px;
    font:400 10px/1.8 'JetBrains Mono',monospace;
    color:rgba(136,146,176,.25);
}
.ql-gad { font:400 11px/1 'Inter',sans-serif;
    color:rgba(240,244,255,.4); text-align:center; margin-bottom:8px; }

/* ── MOBILE ── */
@media(max-width:680px) {
    .ql-platforms { grid-template-columns:1fr; max-width:380px; gap:10px }
    .ql-brand { font-size:26px }
    .ql-hero { padding:36px 16px 24px }
    div[data-testid="stForm"] { padding:20px 16px !important }
}

/* ── COOPERACIÓN btn ── */
.ql-card-btn.btn-purple {
    background:rgba(124,92,252,.1);border-color:rgba(124,92,252,.28);
    color:#9B79FF;
}

/* ── ACCESO OPERACIONAL ghost btn ── */
.ql-ops-section { display:flex;justify-content:center; }
.ql-ops-btn {
    background:transparent !important;
    border:1px solid rgba(255,255,255,.06) !important;
    color:rgba(136,146,176,.26) !important;
    font:500 9px/1 'JetBrains Mono',monospace !important;
    letter-spacing:.07em !important;
    border-radius:6px !important;
    padding:5px 14px !important;
    transition:color .2s,border-color .2s,background .2s !important;
}
.ql-ops-btn:hover {
    border-color:rgba(249,115,22,.28) !important;
    color:rgba(249,115,22,.55) !important;
    background:rgba(249,115,22,.03) !important;
}
</style>

<script>
(function(){
  var o=new MutationObserver(function(){
    var p=document.querySelector('input[type=password]');
    if(p){p.autocomplete='current-password';o.disconnect();}
  });
  o.observe(document.body,{childList:true,subtree:true});
})();
(function(){
  function _tagOps(){
    document.querySelectorAll('[data-testid="stButton"] button').forEach(function(b){
      if((b.innerText||'').trim().toLowerCase().indexOf('acceso operacional')!==-1){
        b.classList.add('ql-ops-btn');
        var w=b.closest('[data-testid="stButton"]');if(w)w.classList.add('ql-ops-section');
      }
    });
  }
  var _o2=new MutationObserver(_tagOps);
  _o2.observe(document.body,{childList:true,subtree:true});
})();
</script>"""


def landing_hero() -> str:
    """Bloque hero: logo + marca + tagline."""
    return f"""
<div class="ql-hero">
  <div class="ql-logo">{QUIRA_SVG}</div>
  <div class="ql-brand">QUIRA Intelligence</div>
  <div class="ql-pow">Powered by Dylus Lab</div>
  <div class="ql-tagline">Inteligencia Territorial · Gobernanza con evidencia · Decisiones con territorio</div>
</div>"""


def platform_cards(selected: str = "") -> str:
    """Tres cajas de plataforma. selected: '' | 'institucional' | 'ciudadano' | 'cooperacion'."""
    def _active(key: str) -> str:
        return "active" if selected == key else ""

    return f"""
<div class="ql-platforms">

  <div class="ql-card {_active('institucional')}">
    <span class="ql-card-icon">🏛</span>
    <div class="ql-card-name">QUIRA Institucional</div>
    <div class="ql-card-desc">Dashboard de gobernanza municipal.<br>
      Indicadores ICPI · Alertas SAT · Trazabilidad evidencial.</div>
    <span class="ql-card-btn btn-cyan">Acceso restringido</span>
  </div>

  <div class="ql-card {_active('ciudadano')}">
    <span class="ql-card-icon">🌎</span>
    <div class="ql-card-name">QUIRA Ciudadano</div>
    <div class="ql-card-desc">Transparencia activa y rendición<br>
      de cuentas para toda la ciudadanía.</div>
    <span class="ql-card-btn btn-green">Acceso público</span>
  </div>

  <div class="ql-card {_active('cooperacion')}">
    <span class="ql-card-icon">📑</span>
    <div class="ql-card-name">QUIRA Cooperación</div>
    <div class="ql-card-desc">Para academia, ONGs y cooperación<br>
      internacional. Datos longitudinales.</div>
    <span class="ql-card-btn btn-purple">Solicitar acceso</span>
  </div>

</div>"""


def form_header(corte: str) -> str:
    """Badge + etiqueta dentro del card de login."""
    return (
        f'<div class="ql-form-title">Acceso institucional</div>'
        f'<div style="text-align:center">'
        f'<span class="ql-badge">Acceso Restringido · {corte}</span>'
        f'</div>'
    )


def trust_badges() -> str:
    """Mini-badges de seguridad debajo del formulario."""
    badges = [
        ("#00E096", "ACCESO PROTEGIDO", "Cifrado institucional"),
        ("#00D4FF", "SESIÓN TEMPORAL",  "Expira en 60 minutos"),
        ("#7C5CFC", "INTENTOS MONITOREADOS", "Bloqueo tras 3 fallos"),
        ("#FFB800", "ACTIVIDAD AUDITADA", "Registro de accesos"),
    ]
    items = ""
    for color, label, sub in badges:
        items += (
            f'<div class="ql-trust-item">'
            f'<div><div class="ql-trust-label" style="color:{color}">{label}</div>'
            f'<div class="ql-trust-sub">{sub}</div></div>'
            f'</div>'
        )
    return f'<div class="ql-trust">{items}</div>'


def footer(gad: str, corte: str) -> str:
    """Footer institucional."""
    return f"""
<div class="ql-footer">
  <div class="ql-gad">&#127963; {gad}</div>
  QUIRA Intelligence · Dylus Lab © 2026<br>
  Gold Master v5.5_TGI · Corte {corte}<br>
  <span style="color:rgba(255,184,0,.3)">Acceso institucional restringido</span>
</div>"""


# ── Compatibilidad con código anterior (splash_top / splash_bottom) ───────────

def splash_top(corte: str) -> str:
    """Alias de landing_hero() para compatibilidad."""
    return landing_hero()


def splash_bottom(gad: str, corte: str) -> str:
    """Alias de footer() para compatibilidad."""
    return footer(gad, corte)


def error_html(msg: str) -> str:
    return (
        f'<div style="background:rgba(255,77,109,.1);border:1px solid rgba(255,77,109,.3);'
        f'border-radius:8px;padding:10px 14px;color:#FF8FA3;font-size:12px;'
        f'font-family:Inter,sans-serif;margin-top:4px">'
        f'⚠️ {msg}</div>'
    )
