"""
QUIRA OS — View: Landing + Login  (Sprint Landing v3 · 2026-05-27)
Pantalla cero limpia: 4 cajones iguales, clic directo, sin botones extra.
Dylus Lab © 2026
"""
from __future__ import annotations

QUIRA_SVG = (
    '<svg viewBox="0 0 100 118" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" style="width:52px;height:62px">'
    '<rect x="6"  y="107" width="88" height="11" rx="4"/>'
    '<rect x="44" y="75"  width="12" height="32" rx="3"/>'
    '<path d="M14,80 L14,44 A36,36 0 0,1 86,44 L86,80 L74,80 L74,44 A24,24 0 0,0 26,44 L26,80 Z"/>'
    '<path d="M50,26 A12,12 0 0,1 62,38 Q62,56 50,74 Q38,56 38,38 A12,12 0 0,1 50,26 Z"/>'
    '<path d="M14,80 Q14,60 0,60 L0,70 Q8,70 8,80 Z M0,60 L0,107 L8,107 L8,60 Z"/>'
    '<path d="M86,80 Q86,60 100,60 L100,70 Q92,70 92,80 Z M100,60 L100,107 L92,107 L92,60 Z"/>'
    '</svg>'
)

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer { display:none !important }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 45% at 50% -5%,
            rgba(0,212,255,.065) 0%, transparent 55%),
        #080F1E !important;
    min-height:100vh;
}
[data-testid="stMain"] .block-container {
    padding:0 !important; max-width:100% !important;
}

/* ── HERO ── */
.ql-hero {
    display:flex; flex-direction:column; align-items:center;
    padding:46px 20px 28px; text-align:center;
}
.ql-logo { color:#00D4FF; margin-bottom:14px;
    animation:ql-glow 2.8s ease-in-out infinite; }
@keyframes ql-glow {
    0%,100%{filter:drop-shadow(0 0 16px rgba(0,212,255,.38))}
    50%{filter:drop-shadow(0 0 32px rgba(0,212,255,.75))} }
.ql-brand { font:900 34px/1 'Inter',sans-serif;
    color:#F0F4FF; letter-spacing:-.03em; margin-bottom:7px; }
.ql-os { font:600 15px/1.3 'Inter',sans-serif;
    color:rgba(240,244,255,.72); margin-bottom:6px; }
.ql-pow { font:500 8px/1 'JetBrains Mono',monospace;
    color:rgba(0,212,255,.48); letter-spacing:.14em;
    text-transform:uppercase; margin-bottom:10px; }
.ql-tagline { font:400 11px/1.5 'Inter',sans-serif;
    color:rgba(136,146,176,.6); }

/* ── CARD-BUTTONS (los 4 cajones) ── */
[data-testid="stButton"] button {
    background: rgba(8,13,30,.88) !important;
    border: 1px solid rgba(255,255,255,.09) !important;
    border-radius: 14px !important;
    min-height: 174px !important;
    height: auto !important;
    white-space: pre-line !important;
    text-align: center !important;
    padding: 26px 16px 22px !important;
    font-family: 'Inter',sans-serif !important;
    color: rgba(240,244,255,.72) !important;
    font-size: 11px !important;
    line-height: 1.65 !important;
    letter-spacing: .01em !important;
    transition: border-color .2s, background .2s !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: flex-start !important;
    cursor: pointer !important;
    width: 100% !important;
}
[data-testid="stButton"] button p,
[data-testid="stButton"] button span {
    white-space: pre-line !important;
}
[data-testid="stButton"] button:hover {
    color: #F0F4FF !important;
}
[data-testid="stButton"] button:disabled {
    opacity: .35 !important;
    cursor: default !important;
}

/* Colores por columna — JS agrega .ql-col-* al stColumn */
.ql-col-inst .stButton button {
    border-color: rgba(0,212,255,.25) !important;
}
.ql-col-inst .stButton button:hover {
    border-color: rgba(0,212,255,.52) !important;
    background: rgba(0,212,255,.04) !important;
}
.ql-col-civ .stButton button {
    border-color: rgba(34,197,94,.2) !important;
}
.ql-col-civ .stButton button:hover {
    border-color: rgba(34,197,94,.45) !important;
    background: rgba(34,197,94,.04) !important;
}
.ql-col-coop .stButton button {
    border-color: rgba(124,92,252,.2) !important;
}
.ql-col-coop .stButton button:hover {
    border-color: rgba(124,92,252,.45) !important;
    background: rgba(124,92,252,.04) !important;
}
.ql-col-ops .stButton button {
    border-color: rgba(249,115,22,.16) !important;
}
.ql-col-ops .stButton button:hover {
    border-color: rgba(249,115,22,.38) !important;
    background: rgba(249,115,22,.03) !important;
}

/* ── FORM ── */
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
div[data-testid="stTextInput"] input {
    background:#030A18 !important;
    border:1px solid rgba(255,255,255,.1) !important;
    color:#F0F4FF !important; border-radius:8px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:rgba(0,212,255,.5) !important;
}
div[data-testid="stTextInput"] label {
    color:rgba(136,146,176,.7) !important; font-size:10px !important;
    font-weight:700 !important; text-transform:uppercase !important;
    letter-spacing:.08em !important;
}

/* Botón ACCEDER (form submit) — override del card-style general */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"] {
    background:linear-gradient(135deg,#00D4FF 0%,#7C5CFC 100%) !important;
    color:#060E1C !important; font-weight:900 !important;
    font-size:12px !important; border:none !important;
    border-radius:10px !important; letter-spacing:.07em !important;
    min-height: auto !important; height: auto !important;
    padding:14px !important; white-space: normal !important;
    flex-direction: row !important;
}
div[data-testid="stForm"] button:hover { opacity:.88 !important }

/* ── TRUST BADGES ── */
.ql-trust {
    display:grid; grid-template-columns:1fr 1fr; gap:6px;
    max-width:370px; margin:16px auto 12px;
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

/* ── QUÉ ES · las tres negaciones + la cadena madre ── */
.ql-que { max-width:820px; margin:0 auto 6px; padding:0 20px; text-align:center }
.ql-no-row { display:flex; flex-wrap:wrap; gap:7px; justify-content:center; margin-bottom:14px }
.ql-no { font:500 9px/1 'JetBrains Mono',monospace; color:rgba(255,109,128,.55);
    border:1px solid rgba(255,109,128,.18); border-radius:11px; padding:4px 11px;
    letter-spacing:.03em; white-space:nowrap }
.ql-que-t { font:400 13px/1.7 'Inter',sans-serif; color:rgba(216,224,240,.82) }
.ql-que-t b { color:#F0F4FF; font-weight:700 }
.ql-cadena { display:flex; flex-wrap:wrap; gap:0; justify-content:center; align-items:center;
    margin:15px 0 12px }
.ql-esl { font:600 9.5px/1 'JetBrains Mono',monospace; color:rgba(0,212,255,.62);
    border:1px solid rgba(0,212,255,.16); border-radius:5px; padding:5px 9px; margin:3px }
.ql-que-s { font:400 11px/1.65 'Inter',sans-serif; color:rgba(136,146,176,.72) }
.ql-que-s b { color:rgba(216,224,240,.9) }

/* ── CÓMO FUNCIONA ── */
.ql-flow-t, .ql-eco-t { font:700 9px/1 'JetBrains Mono',monospace; letter-spacing:.16em;
    text-transform:uppercase; color:rgba(0,212,255,.42); text-align:center; margin:26px 0 12px }
.ql-flow { display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:8px;
    max-width:820px; margin:0 auto 4px; padding:0 20px }
.ql-fin, .ql-fm, .ql-fc { display:flex; flex-direction:column; align-items:center; gap:3px;
    border:1px solid rgba(255,255,255,.08); border-radius:10px; padding:11px 15px;
    background:rgba(8,13,30,.6) }
.ql-fin { gap:5px }
.ql-fe { font:600 11px/1 'Inter',sans-serif; color:#00E096 }
.ql-fmt { font:700 12px/1 'Inter',sans-serif; color:#FFB800 }
.ql-fct { font:700 12px/1.3 'Inter',sans-serif; color:#00D4FF; text-align:center }
.ql-fl { font:400 8.5px/1.3 'Inter',sans-serif; color:rgba(136,146,176,.6); text-align:center }
.ql-fa { color:rgba(0,212,255,.3); font-size:15px }

/* ── ECOSISTEMA ── */
.ql-eco-s { font:400 11px/1.6 'Inter',sans-serif; color:rgba(136,146,176,.7);
    text-align:center; max-width:640px; margin:0 auto 14px; padding:0 20px }
.ql-prods { display:flex; flex-direction:column; gap:8px; max-width:820px;
    margin:0 auto 4px; padding:0 20px }
.ql-prod { border:1px solid rgba(255,255,255,.07); border-left:2px solid var(--pc);
    border-radius:9px; padding:12px 16px; background:rgba(8,13,30,.55) }
.ql-prod-h { display:flex; align-items:baseline; justify-content:space-between; gap:12px;
    flex-wrap:wrap; margin-bottom:4px }
.ql-prod-n { font:700 13px/1.3 'Inter',sans-serif; color:#F0F4FF }
.ql-prod-e { font:700 7.5px/1 'JetBrains Mono',monospace; letter-spacing:.09em;
    color:var(--pc); white-space:nowrap; opacity:.85 }
.ql-prod-d { font:400 10.5px/1.6 'Inter',sans-serif; color:rgba(136,146,176,.82) }

/* ── FOOTER ── */
.ql-footer {
    text-align:center; padding:10px 20px 24px;
    font:400 9px/1.8 'JetBrains Mono',monospace;
    color:rgba(136,146,176,.18);
}

/* Ops ghost — JS agrega .ql-ops-btn */
button.ql-ops-btn, .ql-ops-section button {
    background:transparent !important;
    border:1px solid rgba(255,255,255,.05) !important;
    color:rgba(136,146,176,.18) !important;
    font:500 8px/1 'JetBrains Mono',monospace !important;
    letter-spacing:.07em !important;
    border-radius:5px !important;
    min-height: auto !important;
    height: auto !important;
    padding:5px 12px !important;
    white-space: normal !important;
    flex-direction: row !important;
}
button.ql-ops-btn:hover, .ql-ops-section button:hover {
    border-color:rgba(249,115,22,.22) !important;
    color:rgba(249,115,22,.4) !important;
}

@media(max-width:680px){
    .ql-brand{font-size:26px} .ql-os{font-size:13px}
    .ql-hero{padding:30px 16px 18px}
    div[data-testid="stForm"]{padding:18px 14px !important}
    [data-testid="stButton"] button { min-height:150px !important; padding:18px 12px !important; }
}
</style>

<script>
(function(){
    /* autocomplete */
    var _o1=new MutationObserver(function(){
        var p=document.querySelector('input[type=password]');
        if(p){p.autocomplete='current-password';_o1.disconnect();}
    });
    _o1.observe(document.body,{childList:true,subtree:true});
})();
(function(){
    /* Tag columnas del primer bloque horizontal para colorear cada card */
    var _tagged=false;
    var _CLASSES=['ql-col-inst','ql-col-civ','ql-col-coop','ql-col-ops'];
    function _tag(){
        if(_tagged) return;
        var blocks=document.querySelectorAll('[data-testid="stHorizontalBlock"]');
        if(!blocks.length) return;
        var cols=blocks[0].querySelectorAll('[data-testid="stColumn"]');
        if(cols.length<2) return;
        cols.forEach(function(c,i){ if(_CLASSES[i]) c.classList.add(_CLASSES[i]); });
        _tagged=true;
    }
    var _o2=new MutationObserver(function(){ _tag(); });
    _o2.observe(document.body,{childList:true,subtree:true});
    setTimeout(_tag,300);
})();
(function(){
    /* Tag ops ghost button */
    function _tagOps(){
        document.querySelectorAll('[data-testid="stButton"] button').forEach(function(b){
            if((b.innerText||'').trim().toLowerCase().indexOf('acceso operacional')!==-1){
                b.classList.add('ql-ops-btn');
                var w=b.closest('[data-testid="stButton"]');
                if(w) w.classList.add('ql-ops-section');
            }
        });
    }
    var _o3=new MutationObserver(_tagOps);
    _o3.observe(document.body,{childList:true,subtree:true});
})();
</script>"""


def landing_hero() -> str:
    """La identidad, según CONSTITUCION-001 (raíz del árbol de autoridad).

    La versión anterior decía "Sistema Operativo de Coherencia Institucional" y las tarjetas
    presentaban a QUIRA como cuatro productos sueltos, uno de ellos interno. Javo (2026-08-05):
    "es una versión muy muy antigua y no representa nada de lo que tenemos ahora". Se
    reconstruye sobre la Constitución Institucional y ADR-041."""
    return (
        f'<div class="ql-hero">'
        f'<div class="ql-logo">{QUIRA_SVG}</div>'
        f'<div class="ql-brand">QUIRA</div>'
        f'<div class="ql-os">Plataforma de Inteligencia Pública</div>'
        f'<div class="ql-pow">Development by Dylus Lab</div>'
        f'<div class="ql-tagline">'
        f'Infraestructura de conocimiento verificable para gobiernos,<br>'
        f'ciudadanía, academia y cooperación internacional'
        f'</div>'
        f'</div>'
    )


def que_es() -> str:
    """Qué es y qué NO es. Las tres negaciones son las tres reducciones que el propio canon
    de arranque inducía y que Javo corrigió: auditoría (función menor), observatorio
    (producto) y software municipal (contra la Tesis: el GAD es sujeto observado)."""
    noes = "".join(
        f'<span class="ql-no">{t}</span>' for t in
        ("no es un software municipal", "no es una auditoría", "no es solo un observatorio"))
    return (
        '<div class="ql-que">'
        f'<div class="ql-no-row">{noes}</div>'
        '<div class="ql-que-t">QUIRA convierte la evidencia pública dispersa en '
        '<b>conocimiento verificable</b>. No mide trámites ni obras aisladas: sigue la cadena '
        'que va de la <b>promesa</b> al <b>territorio</b> —plan, presupuesto, ejecución, '
        'resultado— y muestra <b>dónde se rompe y por qué</b>.</div>'
        '<div class="ql-cadena">'
        + "".join(f'<span class="ql-esl">{e}</span>' for e in
                  ("Promesa", "Plan", "Presupuesto", "Ejecución", "Resultado", "Territorio"))
        + '</div>'
        '<div class="ql-que-s">Cada afirmación se ancla a un documento — o a la ausencia '
        '<b>documentada</b> de uno. QUIRA no certifica la verdad: certifica qué puede '
        'comprobar el ciudadano y qué no.</div>'
        '</div>')


def como_funciona() -> str:
    """Dos entradas · un motor · un núcleo (ADR-041 §3). El motor NO se salta: la primera
    versión del ADR ponía los productos escribiendo directo al núcleo, contra ADR-023."""
    return (
        '<div class="ql-flow-t">Cómo funciona</div>'
        '<div class="ql-flow">'
        '<div class="ql-fin">'
        '<span class="ql-fe">Observatorio</span>'
        '<span class="ql-fe">Ciudadanía</span>'
        '<span class="ql-fl">dos entradas de evidencia</span></div>'
        '<span class="ql-fa">→</span>'
        '<div class="ql-fm"><span class="ql-fmt">Motor</span>'
        '<span class="ql-fl">calcula</span></div>'
        '<span class="ql-fa">→</span>'
        '<div class="ql-fc"><span class="ql-fct">Centro de Inteligencia Territorial</span>'
        '<span class="ql-fl">núcleo único · todo converge aquí</span></div>'
        '</div>')


# (fase, clave, nombre, qué hace, estado, color)
_ECOSISTEMA = [
    ("1", "obs", "Observatorio Nacional de Integridad Territorial",
     "Monitorea los 222 municipios del país de forma progresiva. Agentes de inteligencia "
     "artificial revisan los sistemas públicos —transparencia, contratación, rendición de "
     "cuentas, portales institucionales— y la evidencia se valida antes de publicarse.",
     "ACTIVO · producto principal", "#00D4FF"),
    ("1", "civ", "QUIRA Ciudadana",
     "La puerta del control social que manda la Constitución. Cualquier persona puede aportar "
     "documentos que falten y construir solicitudes de acceso a información pública con ayuda "
     "del sistema. Alcance nacional.",
     "EN CONSTRUCCIÓN", "#00E096"),
    ("2", "coop", "QUIRA Cooperación",
     "Evidencia territorial verificada para universidades, organismos bilaterales y ONG. "
     "Requiere la cobertura nacional que producen las dos entradas.",
     "FASE 2", "#7C5CFC"),
    ("2", "inst", "QUIRA Institucional",
     "Inteligencia para el propio gobierno local. Llega después, y no antes: el municipio es "
     "sujeto observado, no cliente.",
     "FASE 2", "#FFB800"),
    ("3", "econ", "QUIRA Economic",
     "Inteligencia económica del territorio: inversión y desarrollo económico local.",
     "FASE 3", "#8892B0"),
]


def ecosistema() -> str:
    """Los productos. Operaciones NO aparece: es mantenimiento del ecosistema, no producto
    (Javo · ADR-041 §2) — y NOMENCLATURA_CANONICA ya prohibía publicarlo en la landing."""
    filas = ""
    for fase, k, nombre, desc, estado, col in _ECOSISTEMA:
        filas += (
            f'<div class="ql-prod ql-p-{k}" style="--pc:{col}">'
            f'<div class="ql-prod-h">'
            f'<span class="ql-prod-n">{nombre}</span>'
            f'<span class="ql-prod-e">{estado}</span></div>'
            f'<div class="ql-prod-d">{desc}</div></div>')
    return (
        '<div class="ql-eco-t">El ecosistema</div>'
        '<div class="ql-eco-s">QUIRA es la plataforma. Estos son sus productos — cada uno con '
        'una misión distinta, todos sobre el mismo núcleo de conocimiento.</div>'
        f'<div class="ql-prods">{filas}</div>')


def form_header() -> str:
    return (
        '<div class="ql-form-title">Acceso Institucional</div>'
        '<div style="text-align:center">'
        '<span class="ql-badge">Acceso Restringido · QUIRA Institucional</span>'
        '</div>'
    )


def trust_badges() -> str:
    badges = [
        ("#00E096", "ACCESO PROTEGIDO",     "Cifrado institucional"),
        ("#00D4FF", "SESIÓN TEMPORAL",       "Expira en 60 minutos"),
        ("#7C5CFC", "INTENTOS MONITOREADOS", "Bloqueo tras 3 fallos"),
        ("#FFB800", "ACTIVIDAD AUDITADA",    "Registro de accesos"),
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
    # BUILD_STAMP visible pre-auth: permite verificar QUÉ commit corre el
    # deploy SIN credenciales (Playwright/director) + la VERSIÓN del runtime
    # Streamlit del servidor (diagnóstico de features no soportadas).
    # Lección 2026-06-11: fin de los deploys a ciegas.
    import streamlit as _st_v
    return (
        '<div class="ql-footer">'
        'QUIRA · Dylus Lab © 2026<br>'
        # "de gobernanza pública" era casi correcto pero no es lo que dice la Constitución
        # Institucional: infraestructura de CONOCIMIENTO VERIFICABLE (Art. 1-5).
        '<span style="color:rgba(255,184,0,.2)">Infraestructura de conocimiento verificable</span><br>'
        '<span style="color:rgba(255,255,255,.18);font-family:monospace;font-size:9px">'
        f'build cc-v2-r2 · 2026-06-11 · st {_st_v.__version__}</span>'
        '</div>'
    )


# ── Backward compat ───────────────────────────────────────────────────────────
def platform_cards(selected: str = "") -> str: return ""
def card_institucional_html(active: bool = False) -> str: return ""
def card_ciudadano_html(active: bool = False) -> str: return ""
def card_cooperacion_html(active: bool = False) -> str: return ""
def card_operations_html() -> str: return ""
def splash_top(corte: str = "") -> str: return landing_hero()
def splash_bottom(gad: str = "", corte: str = "") -> str: return footer()
def error_html(msg: str) -> str:
    return (
        f'<div style="background:rgba(255,77,109,.1);border:1px solid rgba(255,77,109,.3);'
        f'border-radius:8px;padding:10px 14px;color:#FF8FA3;font-size:12px;'
        f'font-family:Inter,sans-serif;margin-top:4px">⚠️ {msg}</div>'
    )
