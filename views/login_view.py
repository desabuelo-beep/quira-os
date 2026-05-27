"""
QUIRA OS — View: Login
Responsabilidad única: devolver strings HTML/CSS listos para renderizar.
Sin imports de Streamlit. Sin lógica de negocio. Solo presentación.
Dylus Lab © 2026
"""
from __future__ import annotations

# ── SVG del logo QUIRA (igual al DEMO.html) ───────────────────────────────────
QUIRA_SVG = (
    '<svg viewBox="0 0 100 118" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" style="width:72px;height:85px">'
    '<rect x="6"  y="107" width="88" height="11" rx="4"/>'
    '<rect x="44" y="75"  width="12" height="32" rx="3"/>'
    '<path d="M14,80 L14,44 A36,36 0 0,1 86,44 L86,80 L74,80 L74,44 A24,24 0 0,0 26,44 L26,80 Z"/>'
    '<path d="M50,26 A12,12 0 0,1 62,38 Q62,56 50,74 Q38,56 38,38 A12,12 0 0,1 50,26 Z"/>'
    '<path d="M14,80 Q14,60 0,60 L0,70 Q8,70 8,80 Z M0,60 L0,107 L8,107 L8,60 Z"/>'
    '<path d="M86,80 Q86,60 100,60 L100,70 Q92,70 92,80 Z M100,60 L100,107 L92,107 L92,60 Z"/>'
    '</svg>'
)

# ── CSS mínimo: 4 reglas base + tema inputs + mobile ─────────────────────────
# No sobreescribe estilos internos de React/Streamlit — solo el shell exterior.
CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@600;700;800&family=JetBrains+Mono:wght@400&display=swap');

[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer { display:none !important }

/* Fondo de página con gradiente — sin min-height en bloques hijos */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 70% 40% at 50% 0%, rgba(0,212,255,.09) 0%, transparent 60%), #0A1128 !important;
    min-height: 100vh;
}
[data-testid="stMain"] .block-container { padding:0 !important; max-width:100% !important }

/* Bloque header: logo + títulos — solo padding, sin capturar altura */
.ql-wrap {
    display:flex; flex-direction:column; align-items:center;
    padding:48px 16px 24px; gap:0;
    text-align:center;
}

.ql-logo  { color:#00D4FF; animation:ql-glow 2.4s ease-in-out infinite; margin-bottom:18px; }
@keyframes ql-glow { 0%,100%{filter:drop-shadow(0 0 20px rgba(0,212,255,.5))}
                     50%{filter:drop-shadow(0 0 42px rgba(0,212,255,.9))} }

.ql-title { font:800 34px/1 'Inter',sans-serif; color:#F0F4FF; letter-spacing:-.02em;
  white-space:nowrap; margin-bottom:6px }
.ql-pow   { font:700 11px/1 'Inter',sans-serif; color:#00D4FF; letter-spacing:.1em;
  text-transform:uppercase; margin-bottom:16px }
.ql-tag1  { font:700 15px/1 'Inter',sans-serif; color:#F0F4FF; white-space:nowrap }
.ql-tag2  { font:400 13px/1 'Inter',sans-serif; color:#8892B0; margin-bottom:16px }
.ql-div   { width:260px; height:1px; background:#1E2D50; margin:8px auto 12px }
.ql-loc   { font:400 11px/1 'JetBrains Mono',monospace; color:#8892B0; letter-spacing:.1em;
  text-transform:uppercase; }

/* El form de Streamlit ES el card de acceso */
div[data-testid="stForm"] {
    background: rgba(13,22,56,.8) !important;
    border: 1px solid rgba(0,212,255,.18) !important;
    border-radius: 16px !important;
    padding: 24px 28px 20px !important;
    backdrop-filter: blur(12px) !important;
    margin-top: 0 !important;
}

/* Etiqueta y badge dentro del form */
.ql-clbl  { font:700 10px/1 'Inter',sans-serif; color:#8892B0; text-transform:uppercase;
  letter-spacing:.1em; text-align:center; margin-bottom:14px }
.ql-badge { display:inline-block; background:rgba(0,212,255,.08); border:1px solid rgba(0,212,255,.2);
  border-radius:20px; padding:3px 12px; font:500 10px/1 'JetBrains Mono',monospace;
  color:#00D4FF; margin:0 auto 20px; display:block; width:fit-content; }
.ql-gad   { font:400 11px/1 'Inter',sans-serif; color:rgba(240,244,255,.5);
  text-align:center; border-top:1px solid rgba(255,255,255,.05); padding-top:14px; margin-top:4px }

/* inputs Streamlit — solo colores, sin tocar layout */
div[data-testid="stTextInput"] input,
div[data-baseweb="select"] > div { background:#070E20 !important; border:1px solid #1E2D50 !important;
  color:#F0F4FF !important; border-radius:8px !important }
div[data-testid="stTextInput"] input:focus,
div[data-baseweb="select"] > div:focus-within { border-color:#00D4FF !important }
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"]  label { color:#8892B0 !important; font-size:10px !important;
  font-weight:700 !important; text-transform:uppercase !important; letter-spacing:.08em !important }
div[data-baseweb="select"] svg { color:#8892B0 !important }

/* botón login */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"] {
    background: linear-gradient(135deg,#00D4FF,#7C5CFC) !important;
    color: #0A1128 !important; font-weight:800 !important; font-size:13px !important;
    border:none !important; border-radius:10px !important; padding:.6rem 1rem !important;
    width:100% !important; letter-spacing:.05em !important;
}
div[data-testid="stForm"] button:hover { opacity:.88 !important }

/* footer */
.ql-foot { margin-top:24px; font:400 10px/1.8 'JetBrains Mono',monospace;
  color:rgba(136,146,176,.28); text-align:center }

@media(max-width:600px) {
  .ql-title { font-size:26px } .ql-tag1 { white-space:normal; font-size:14px }
  div[data-testid="stForm"] { padding:20px 16px !important }
  .ql-div { width:180px }
}
</style>

<script>
/* autocomplete fix — se desconecta en cuanto encuentra el input */
(function(){
  var o=new MutationObserver(function(){
    var p=document.querySelector('input[type=password]');
    if(p){p.autocomplete='current-password';o.disconnect();}
  });
  o.observe(document.body,{childList:true,subtree:true});
})();
</script>"""


def splash_top(corte: str) -> str:
    """Bloque superior: logo + títulos — completamente auto-contenido.
    El card visual es el propio stForm, estilado via CSS.
    """
    return f"""
<div class="ql-wrap">
  <div class="ql-logo">{QUIRA_SVG}</div>
  <div class="ql-title">QUIRA Intelligence</div>
  <div class="ql-pow">Powered by Dylus Lab</div>
  <div class="ql-tag1">Territorial Governance Intelligence</div>
  <div class="ql-tag2">Gobernar con evidencia · Decidir con territorio</div>
  <div class="ql-div"></div>
  <div class="ql-loc">Montecristi · Manabi · Ecuador · {corte}</div>
</div>"""


def splash_bottom(gad: str, corte: str) -> str:
    """Trust signals + footer — completamente auto-contenido."""
    return f"""
<div style="max-width:390px;margin:0 auto;padding:0 4px">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:12px 0 14px">
    <div style="display:flex;align-items:center;gap:6px;background:rgba(0,224,150,.06);
                border:1px solid rgba(0,224,150,.15);border-radius:8px;padding:7px 10px">
      <span style="font-size:14px">&#128274;</span>
      <div>
        <div style="font-size:9px;font-weight:700;color:#00E096;letter-spacing:.05em">ACCESO PROTEGIDO</div>
        <div style="font-size:9px;color:#8892B0">Cifrado institucional</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;background:rgba(0,212,255,.06);
                border:1px solid rgba(0,212,255,.15);border-radius:8px;padding:7px 10px">
      <span style="font-size:14px">&#128338;</span>
      <div>
        <div style="font-size:9px;font-weight:700;color:#00D4FF;letter-spacing:.05em">SESION TEMPORAL</div>
        <div style="font-size:9px;color:#8892B0">Expira en 60 minutos</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;background:rgba(124,92,252,.06);
                border:1px solid rgba(124,92,252,.15);border-radius:8px;padding:7px 10px">
      <span style="font-size:14px">&#128737;</span>
      <div>
        <div style="font-size:9px;font-weight:700;color:#7C5CFC;letter-spacing:.05em">INTENTOS MONITOREADOS</div>
        <div style="font-size:9px;color:#8892B0">Bloqueo tras 3 fallos</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:6px;background:rgba(255,184,0,.06);
                border:1px solid rgba(255,184,0,.15);border-radius:8px;padding:7px 10px">
      <span style="font-size:14px">&#128203;</span>
      <div>
        <div style="font-size:9px;font-weight:700;color:#FFB800;letter-spacing:.05em">ACTIVIDAD AUDITADA</div>
        <div style="font-size:9px;color:#8892B0">Registro de accesos</div>
      </div>
    </div>
  </div>
  <div class="ql-gad">&#127963; {gad}</div>
  <div class="ql-foot">
    QUIRA Intelligence · Dylus Lab © 2026<br>
    Gold Master v5.5_TGI · Corte {corte}<br>
    <span style="color:rgba(255,184,0,.35)">Acceso institucional restringido</span>
  </div>
</div>"""


def error_html(msg: str) -> str:
    return (
        f'<div style="background:rgba(255,77,109,.1);border:1px solid rgba(255,77,109,.3);'
        f'border-radius:8px;padding:10px 14px;color:#FF8FA3;font-size:12px;'
        f'font-family:Inter,sans-serif;margin-top:4px">'
        f'⚠️ {msg}</div>'
    )
