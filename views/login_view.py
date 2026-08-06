"""
QUIRA OS — View: Landing + Acceso  ·  v5 "Chaquira"  ·  2026-08-05

Reescrita sobre `identity/CONSTITUCION_INSTITUCIONAL.md` (CONSTITUCION-001, raíz del árbol
de autoridad) y ADR-041. La versión anterior era del modelo "software municipal": cuatro
tarjetas-producto, una de ellas interna, y una identidad —"Sistema Operativo de Coherencia
Institucional"— que el propio canon había dejado atrás.

QUÉ CAMBIA, Y POR QUÉ (Javo · 2026-08-05):
  · EL ORIGEN. La chaquira manteña entra como sección propia. Es lo que vuelve a QUIRA
    originaria en vez de una plataforma que podría ser de cualquier país — y explica de paso
    el nombre del laboratorio: spon·DYLUS.
  · QUIRA CIUDADANA es CIVICTECH, no una mesa de partes. Comunidad que crece de Ecuador a
    LAC, con IA que acompaña y educa para que el humano incida.
  · LA TESIS SE RESPETA, SE EXPLICA MEJOR. "El municipio es sujeto observado, no cliente"
    permanece —es doctrina congelada— pero deja de leerse como reproche: se muestra POR QUÉ
    esa independencia le sirve al propio municipio (evidencia que un tercero respalda vale
    ante banca y cooperación; evidencia de su proveedor, no).
  · Tipografía con carácter (Fraunces para titulares) y el logo real del proyecto.

Paleta: azul manteño del logo · coral Spondylus · cian de datos. El coral es nuevo y es
deliberado — es el color de la concha de la que viene el nombre.
Dylus Lab © 2026
"""
from __future__ import annotations

from pathlib import Path

# Logo real (assets/quira_logo_b64.txt). Se lee UNA vez por proceso, no por render.
try:
    _LOGO_B64 = (Path(__file__).resolve().parents[1] / "assets" / "quira_logo_b64.txt"
                 ).read_text(encoding="utf-8").strip()
except Exception:  # noqa: BLE001
    _LOGO_B64 = ""

QUIRA_SVG = (
    f'<img src="data:image/png;base64,{_LOGO_B64}" alt="QUIRA" class="ql-mark">'
    if _LOGO_B64 else
    '<div style="font:900 42px \'Fraunces\',serif;color:#4A7BD4">⬡</div>'
)

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,700;9..144,900&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
  --azul:#3A62B8;        /* azul manteño del logo */
  --azul-cl:#6E97E8;
  --coral:#E8734A;       /* Spondylus — el color de la concha */
  --cian:#00D4FF;        /* dato verificado */
  --verde:#00E096;       /* evidencia ciudadana */
  --tx:#EDF1FA;
  --tx2:#96A1BE;
  --tx3:#5E6A85;
  --bg:#070C16;
  --sf:rgba(255,255,255,.026);
  --bd:rgba(255,255,255,.085);
}

[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer { display:none !important }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 62% 38% at 50% -6%, rgba(58,98,184,.19) 0%, transparent 62%),
        radial-gradient(ellipse 42% 26% at 88% 12%, rgba(232,115,74,.07) 0%, transparent 60%),
        var(--bg) !important;
    min-height:100vh;
}
[data-testid="stMain"] .block-container { padding:0 !important; max-width:100% !important }

/* grano sutil — evita el plano digital perfecto */
[data-testid="stAppViewContainer"]::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.5;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.028'/%3E%3C/svg%3E");
}

.ql-wrap{max-width:900px;margin:0 auto;padding:0 24px;position:relative;z-index:1}

/* ══ HERO ══ */
.ql-hero{display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:62px 24px 30px;position:relative;z-index:1}
.ql-mark{width:96px;height:auto;margin-bottom:20px;
  filter:drop-shadow(0 0 30px rgba(58,98,184,.5));
  animation:ql-rise 1.1s cubic-bezier(.2,.7,.3,1) both}
@keyframes ql-rise{from{opacity:0;transform:translateY(16px) scale(.94)}to{opacity:1;transform:none}}
.ql-brand{font:900 74px/.92 'Fraunces',Georgia,serif;color:var(--tx);
  letter-spacing:-.035em;margin-bottom:6px;
  animation:ql-rise 1.1s cubic-bezier(.2,.7,.3,1) .1s both}
.ql-os{font:400 21px/1.35 'Fraunces',Georgia,serif;color:var(--azul-cl);
  letter-spacing:.005em;margin-bottom:16px;font-style:italic;
  animation:ql-rise 1.1s cubic-bezier(.2,.7,.3,1) .18s both}
.ql-tagline{font:400 15.5px/1.7 'Inter',sans-serif;color:var(--tx2);max-width:600px;
  animation:ql-rise 1.1s cubic-bezier(.2,.7,.3,1) .26s both}
.ql-tagline b{color:var(--tx);font-weight:600}
.ql-pow{font:500 10px/1 'JetBrains Mono',monospace;color:var(--tx3);
  letter-spacing:.2em;text-transform:uppercase;margin-top:18px;
  animation:ql-rise 1.1s cubic-bezier(.2,.7,.3,1) .34s both}

/* ══ SECCIONES ══ */
.ql-sec{margin:52px auto 0;max-width:900px;padding:0 24px;position:relative;z-index:1}
.ql-kicker{font:700 10.5px/1 'JetBrains Mono',monospace;letter-spacing:.19em;
  text-transform:uppercase;color:var(--tx3);margin-bottom:13px;display:flex;
  align-items:center;gap:11px}
.ql-kicker::after{content:"";flex:1;height:1px;
  background:linear-gradient(90deg,var(--bd),transparent)}
.ql-h2{font:600 30px/1.22 'Fraunces',Georgia,serif;color:var(--tx);
  letter-spacing:-.015em;margin-bottom:14px}
.ql-p{font:400 15.5px/1.78 'Inter',sans-serif;color:var(--tx2);max-width:760px}
.ql-p b{color:var(--tx);font-weight:600}
.ql-p + .ql-p{margin-top:13px}

/* ══ ORIGEN · chaquira ══ */
.ql-origen{border:1px solid var(--bd);border-left:3px solid var(--coral);
  border-radius:14px;padding:26px 30px;background:
    linear-gradient(105deg,rgba(232,115,74,.055),rgba(232,115,74,0) 62%),var(--sf)}
.ql-quote{font:400 19.5px/1.62 'Fraunces',Georgia,serif;color:var(--tx);
  font-style:italic;margin-bottom:15px}
.ql-quote em{color:var(--coral);font-style:italic}
.ql-collar{display:flex;align-items:center;gap:7px;margin:19px 0 15px;flex-wrap:wrap}
.ql-bead{width:15px;height:15px;border-radius:50%;
  background:radial-gradient(circle at 32% 30%,#F4A183,var(--coral) 55%,#A83F22);
  box-shadow:0 0 12px rgba(232,115,74,.42);flex:none;
  animation:ql-bead 3.4s ease-in-out infinite}
.ql-bead:nth-child(2){animation-delay:.18s}.ql-bead:nth-child(3){animation-delay:.36s}
.ql-bead:nth-child(4){animation-delay:.54s}.ql-bead:nth-child(5){animation-delay:.72s}
.ql-bead:nth-child(6){animation-delay:.9s}.ql-bead:nth-child(7){animation-delay:1.08s}
@keyframes ql-bead{0%,100%{opacity:.55;transform:scale(.9)}50%{opacity:1;transform:scale(1.06)}}
.ql-thread{flex:1;height:1px;background:linear-gradient(90deg,var(--coral),transparent);
  min-width:40px;opacity:.4}
.ql-origen-p{font:400 14.5px/1.75 'Inter',sans-serif;color:var(--tx2)}
.ql-origen-p b{color:var(--tx);font-weight:600}

/* ══ NEGACIONES ══ */
.ql-nos{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px}
.ql-no{font:500 13px/1 'JetBrains Mono',monospace;color:var(--azul-cl);
  border:1px solid rgba(110,151,232,.28);border-radius:16px;padding:9px 17px;
  background:rgba(58,98,184,.075);white-space:nowrap}

/* ══ PROBLEMA · cadena rota ══ */
.ql-rota{display:flex;flex-wrap:wrap;align-items:center;gap:0;margin:18px 0 6px}
.ql-link{font:600 12.5px/1 'JetBrains Mono',monospace;color:var(--tx2);
  border:1px solid var(--bd);border-radius:7px;padding:10px 14px;margin:4px;
  background:var(--sf);transition:all .25s}
.ql-link.on{color:var(--cian);border-color:rgba(0,212,255,.35);
  background:rgba(0,212,255,.07)}
.ql-cut{color:var(--coral);font-size:17px;margin:0 3px;opacity:.85}
.ql-arrow{color:var(--tx3);font-size:14px;margin:0 2px}
.ql-syst{font:400 9.5px/1 'JetBrains Mono',monospace;color:var(--tx3);
  display:block;margin-top:4px;letter-spacing:.04em}

/* ══ FLUJO ══ */
.ql-flow{display:flex;flex-wrap:wrap;align-items:stretch;justify-content:center;
  gap:12px;margin:22px 0 8px}
.ql-node{flex:1 1 190px;border:1px solid var(--bd);border-radius:13px;padding:17px 19px;
  background:var(--sf);position:relative}
.ql-node.entrada{border-top:2px solid var(--verde)}
.ql-node.motor{border-top:2px solid var(--coral)}
.ql-node.centro{border-top:2px solid var(--cian);background:rgba(0,212,255,.045)}
.ql-node-t{font:700 14.5px/1.3 'Inter',sans-serif;color:var(--tx);margin-bottom:5px}
.ql-node-d{font:400 12px/1.6 'Inter',sans-serif;color:var(--tx2)}
.ql-node-k{font:700 8.5px/1 'JetBrains Mono',monospace;letter-spacing:.13em;
  text-transform:uppercase;margin-bottom:7px;display:block}

/* ══ PRODUCTOS ══ */
.ql-prods{display:flex;flex-direction:column;gap:11px;margin-top:18px}
.ql-prod{border:1px solid var(--bd);border-left:3px solid var(--pc,var(--azul));
  border-radius:12px;padding:19px 23px;background:var(--sf);transition:all .3s}
.ql-prod:hover{background:rgba(255,255,255,.045);transform:translateX(3px)}
.ql-prod-h{display:flex;align-items:baseline;justify-content:space-between;
  gap:15px;flex-wrap:wrap;margin-bottom:4px}
.ql-prod-n{font:600 19px/1.28 'Fraunces',Georgia,serif;color:var(--tx)}
.ql-prod-e{font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.11em;
  color:var(--pc,var(--azul));white-space:nowrap}
.ql-prod-r{font:500 11.5px/1 'Inter',sans-serif;color:var(--pc,var(--azul));
  margin-bottom:9px;opacity:.9}
.ql-prod-d{font:400 13.8px/1.72 'Inter',sans-serif;color:var(--tx2)}
.ql-prod-d b{color:var(--tx);font-weight:600}

/* ══ LA LÍNEA · qué se puede contratar y qué no ══ */
.ql-linea{border:1px solid var(--bd);border-radius:13px;padding:20px 23px;margin:20px 0;
  background:var(--sf)}
.ql-linea-t{font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.17em;
  text-transform:uppercase;color:var(--tx3);margin-bottom:14px}
.ql-linea-g{display:grid;grid-template-columns:1fr 1fr;gap:13px}
.ql-linea-c{border-radius:10px;padding:15px 18px;font:400 13.2px/1.68 'Inter',sans-serif;
  color:var(--tx2)}
.ql-linea-c b{color:var(--tx);font-weight:600}
.ql-linea-c.no{border:1px solid rgba(232,115,74,.26);background:rgba(232,115,74,.055)}
.ql-linea-c.si{border:1px solid rgba(0,224,150,.24);background:rgba(0,224,150,.05)}
.ql-linea-k{display:block;font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.12em;
  text-transform:uppercase;margin-bottom:7px}
.ql-linea-c.no .ql-linea-k{color:var(--coral)}
.ql-linea-c.si .ql-linea-k{color:var(--verde)}

/* ══ HUMAN IN THE LOOP ══ */
.ql-hil{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:16px}
.ql-hil-c{border:1px solid var(--bd);border-radius:12px;padding:18px 21px;background:var(--sf)}
.ql-hil-t{font:700 13px/1.3 'Inter',sans-serif;margin-bottom:6px}
.ql-hil-d{font:400 13px/1.68 'Inter',sans-serif;color:var(--tx2)}
.ql-hil-cierre{font:400 17px/1.6 'Fraunces',Georgia,serif;color:var(--tx);
  font-style:italic;text-align:center;margin-top:19px;padding-top:17px;
  border-top:1px solid var(--bd)}

/* ══ ACCESO ══ */
[data-testid="stButton"] button{
  background:rgba(58,98,184,.09) !important;
  border:1px solid rgba(110,151,232,.3) !important;
  border-radius:14px !important;min-height:auto !important;height:auto !important;
  white-space:pre-line !important;text-align:center !important;
  padding:20px 22px !important;font-family:'Inter',sans-serif !important;
  color:var(--tx) !important;font-size:15px !important;font-weight:600 !important;
  line-height:1.6 !important;transition:all .25s !important;
  display:flex !important;flex-direction:column !important;align-items:center !important;
  cursor:pointer !important;width:100% !important}
[data-testid="stButton"] button:hover{
  border-color:rgba(110,151,232,.62) !important;
  background:rgba(58,98,184,.16) !important;transform:translateY(-1px) !important}
[data-testid="stButton"] button p,[data-testid="stButton"] button span{white-space:pre-line !important}

div[data-testid="stForm"]{background:rgba(7,12,22,.93) !important;
  border:1px solid rgba(110,151,232,.22) !important;border-radius:16px !important;
  padding:24px 28px 20px !important;backdrop-filter:blur(18px) !important}
.ql-form-title{font:700 10.5px/1 'JetBrains Mono',monospace;color:var(--tx3);
  text-transform:uppercase;letter-spacing:.15em;text-align:center;margin-bottom:12px}
.ql-badge{display:block;width:fit-content;margin:0 auto 18px;
  background:rgba(58,98,184,.1);border:1px solid rgba(110,151,232,.24);
  border-radius:20px;padding:6px 16px;
  font:500 10.5px/1 'JetBrains Mono',monospace;color:var(--azul-cl)}
div[data-testid="stTextInput"] input{background:#040910 !important;
  border:1px solid var(--bd) !important;color:var(--tx) !important;
  border-radius:9px !important;font-size:15px !important}
div[data-testid="stTextInput"] input:focus{border-color:rgba(110,151,232,.6) !important}
div[data-testid="stTextInput"] label{color:var(--tx3) !important;font-size:10.5px !important;
  font-weight:700 !important;text-transform:uppercase !important;letter-spacing:.1em !important}
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"]{
  background:linear-gradient(135deg,var(--azul) 0%,#2A3F7A 100%) !important;
  color:#FFF !important;font-weight:800 !important;font-size:13px !important;
  border:none !important;border-radius:10px !important;letter-spacing:.09em !important;
  min-height:auto !important;padding:15px !important;white-space:normal !important;
  flex-direction:row !important}
div[data-testid="stForm"] button:hover{opacity:.9 !important}

/* ══ CONFIANZA ══ */
.ql-trust{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:26px auto 14px}
.ql-trust-item{border:1px solid var(--bd);border-radius:10px;padding:12px 14px;
  background:var(--sf)}
.ql-trust-label{font:700 10.5px/1.3 'Inter',sans-serif;text-transform:uppercase;
  letter-spacing:.06em}
.ql-trust-sub{font:400 11px/1.45 'Inter',sans-serif;color:var(--tx3);margin-top:3px}

/* ══ FOOTER ══ */
.ql-footer{text-align:center;padding:26px 24px 30px;
  font:400 11.5px/1.95 'JetBrains Mono',monospace;color:var(--tx3);
  border-top:1px solid var(--bd);margin-top:34px;position:relative;z-index:1}
.ql-footer b{color:var(--tx2)}

button.ql-ops-btn,.ql-ops-section button{background:transparent !important;
  border:1px solid rgba(255,255,255,.05) !important;color:var(--tx3) !important;
  font:500 9.5px/1 'JetBrains Mono',monospace !important;letter-spacing:.09em !important;
  border-radius:6px !important;padding:7px 14px !important;opacity:.4 !important;
  white-space:normal !important;flex-direction:row !important}
button.ql-ops-btn:hover,.ql-ops-section button:hover{opacity:.75 !important;
  border-color:rgba(232,115,74,.25) !important;transform:none !important}

@media(max-width:720px){
  .ql-brand{font-size:48px}.ql-os{font-size:17px}.ql-h2{font-size:24px}
  .ql-tagline{font-size:14px}.ql-p{font-size:14.5px}
  .ql-quote{font-size:17px}.ql-prod-n{font-size:17px}
  .ql-hil,.ql-trust,.ql-linea-g{grid-template-columns:1fr}
  .ql-hero{padding:40px 18px 22px}.ql-sec{margin-top:40px}
}
</style>

<script>
(function(){var o=new MutationObserver(function(){
  var p=document.querySelector('input[type=password]');
  if(p){p.autocomplete='current-password';o.disconnect();}});
  o.observe(document.body,{childList:true,subtree:true});})();
(function(){function t(){
  document.querySelectorAll('[data-testid="stButton"] button').forEach(function(b){
    if((b.innerText||'').trim().toLowerCase().indexOf('mantenimiento')!==-1){
      b.classList.add('ql-ops-btn');
      var w=b.closest('[data-testid="stButton"]'); if(w) w.classList.add('ql-ops-section');}});}
  new MutationObserver(t).observe(document.body,{childList:true,subtree:true});})();
</script>"""


def _sec(kicker: str, h2: str, cuerpo: str) -> str:
    return (f'<div class="ql-sec"><div class="ql-kicker">{kicker}</div>'
            f'<div class="ql-h2">{h2}</div>{cuerpo}</div>')


# ══════════════════════════════ HERO ══════════════════════════════
def landing_hero() -> str:
    return (
        f'<div class="ql-hero">{QUIRA_SVG}'
        f'<div class="ql-brand">QUIRA</div>'
        f'<div class="ql-os">Plataforma de Inteligencia Pública</div>'
        f'<div class="ql-tagline">Infraestructura de <b>conocimiento verificable</b> sobre la '
        f'gestión del territorio, al servicio de gobiernos, ciudadanía, academia y '
        f'cooperación internacional.</div>'
        f'<div class="ql-pow">Dylus Lab · Ecuador</div></div>')


# ══════════════════════════════ ORIGEN ══════════════════════════════
def origen() -> str:
    """La chaquira manteña (Javo · 2026-08-05). Es lo que ancla QUIRA en un territorio y una
    historia concretos, y de paso explica el nombre del laboratorio: spon·DYLUS."""
    collar = ('<div class="ql-collar">' + '<span class="ql-bead"></span>' * 7 +
              '<span class="ql-thread"></span></div>')
    return _sec("El origen", "Una chaquira a la vez",
        '<div class="ql-origen">'
        '<div class="ql-quote">QUIRA viene de <em>chaquira</em>, del antiguo dialecto manteño '
        'de Cancebí. Las chaquiras eran fragmentos de la concha <em>Spondylus</em> con los que '
        'los pueblos manteños y huancavilcas labraban los collares de su élite.</div>'
        + collar +
        '<div class="ql-origen-p">Para esos pueblos, el <b>Spondylus</b> era reserva de valor '
        'e intercambio entre territorios —la estructura madre de la que todo se desprende, y de '
        'la que este laboratorio toma su nombre: spon<b>·DYLUS</b>—. Cada fragmento labrado con '
        'paciencia era una <b>chaquira</b>: la unidad indivisible de valor.<br><br>'
        'Un collar de chaquiras no era un adorno. Era <b>símbolo de autoridad y acuerdo entre '
        'comunidades</b>. Aquí cada dato, cada documento y cada aporte ciudadano es una '
        'chaquira; QUIRA las enhebra hasta formar un <b>collar de integridad para el '
        'territorio</b>: ninguna pieza sostiene sola el conjunto, pero el conjunto no existe '
        'sin cada pieza.</div></div>')


# ══════════════════════════════ QUÉ ES ══════════════════════════════
def que_es() -> str:
    nos = "".join(f'<span class="ql-no">{t}</span>' for t in
                  ("no es un software municipal", "no es una auditoría",
                   "no es solo un observatorio"))
    return _sec("Qué es", "Conocimiento verificable, no opinión",
        f'<div class="ql-nos">{nos}</div>'
        '<p class="ql-p">QUIRA convierte <b>evidencia pública dispersa</b> en conocimiento '
        'que puede comprobarse. No mide trámites ni obras aisladas: sigue la cadena que va '
        'de la <b>promesa</b> al <b>territorio</b> y muestra dónde se interrumpe.</p>'
        '<p class="ql-p">Cada afirmación se ancla a un documento —o a la ausencia '
        '<b>documentada</b> de uno. QUIRA <b>no sustituye a los órganos de control ni '
        'determina responsabilidades</b>: establece el <b>nivel de verificabilidad</b> de la '
        'evidencia disponible. Qué existe, qué puede comprobarse y qué permanece sin '
        'demostrar.</p>')


# ══════════════════════════════ PROBLEMA ══════════════════════════════
_CADENA = [("Promesa", "plan de gobierno"), ("Plan", "PDOT"), ("Presupuesto", "asignación"),
           ("Ejecución", "contratación"), ("Resultado", "bienes y servicios"),
           ("Territorio", "impacto en la gente")]


def problema() -> str:
    """La cadena madre (Constitución Ontológica). NO se renombra ni se marca: cada eslabón
    está atado a un sistema distinto del Estado, y ahí reside su verificabilidad."""
    nodos = ""
    for i, (t, s) in enumerate(_CADENA):
        if i:
            nodos += ('<span class="ql-cut">✕</span>' if i == 3
                      else '<span class="ql-arrow">→</span>')
        nodos += (f'<span class="ql-link{" on" if i < 3 else ""}">{t}'
                  f'<span class="ql-syst">{s}</span></span>')
    return _sec("El problema", "La información existe. La trazabilidad, no siempre",
        '<p class="ql-p">Un compromiso de campaña puede no aparecer en la planificación. La '
        'planificación puede no reflejarse en el presupuesto. El presupuesto puede ejecutarse '
        'sin que conste <b>dónde</b> ni <b>sobre quién</b>. Cada eslabón vive en un sistema '
        'distinto del Estado, y ninguno fue diseñado para hablar con los otros.</p>'
        f'<div class="ql-rota">{nodos}</div>'
        '<p class="ql-p">El problema rara vez es la falta de datos: es que <b>la cadena se '
        'corta</b> en algún punto y nadie puede señalar dónde. QUIRA reconstruye esa cadena '
        'documento por documento, y cuando encuentra el corte, <b>lo nombra</b>.</p>')


# ══════════════════════════════ CÓMO FUNCIONA ══════════════════════════════
def como_funciona() -> str:
    """Dos entradas · un sistema · un núcleo (ADR-041 §3). El motor no se salta y tampoco se
    detalla: la portada responde QUÉ ES, no cómo está implementado."""
    n = [("entrada", "var(--verde)", "Entrada", "Observatorio Nacional",
          "Monitorea de forma progresiva los sistemas públicos de los 222 municipios."),
         ("entrada", "var(--verde)", "Entrada", "QUIRA Ciudadana",
          "Incorpora la evidencia que la ciudadanía aporta desde el territorio."),
         ("motor", "var(--coral)", "Proceso", "Sistema de inteligencia",
          "Contrasta ambas fuentes contra la norma y reconstruye la cadena."),
         ("centro", "var(--cian)", "Núcleo", "Centro de Inteligencia Territorial",
          "Donde la evidencia se vuelve conocimiento consultable. Único: todo converge aquí.")]
    nodos = "".join(
        f'<div class="ql-node {c}"><span class="ql-node-k" style="color:{col}">{k}</span>'
        f'<div class="ql-node-t">{t}</div><div class="ql-node-d">{d}</div></div>'
        for c, col, k, t, d in n)
    return _sec("Cómo funciona", "Dos fuentes, un solo cuerpo de conocimiento",
        f'<div class="ql-flow">{nodos}</div>'
        '<p class="ql-p" style="margin-top:14px">Las dos entradas son <b>distintas por '
        'naturaleza</b>: una detecta la evidencia que ya existe en los sistemas del Estado; la '
        'otra ayuda a producir la que falta. Ninguna sustituye a la otra, y ambas alimentan '
        'el mismo cuerpo de conocimiento — no bases separadas que después se contradicen.</p>')


# ══════════════════════════════ ECOSISTEMA ══════════════════════════════
# (clave, nombre, rótulo, descripción, estado, color)
_PRODUCTOS = [
    ("obs", "Observatorio Nacional de Integridad Territorial",
     "Evidencia institucional · escala nacional",
     "Monitoreo progresivo de los <b>222 municipios</b> del país, incorporados según su "
     "disponibilidad documental y su ciclo administrativo. Agentes de inteligencia artificial "
     "revisan los sistemas públicos —transparencia, contratación, rendición de cuentas, "
     "portales institucionales— y <b>toda captura se valida antes de publicarse</b>.",
     "FASE 1 · ACTIVO", "var(--cian)"),
    ("civ", "QUIRA Ciudadana",
     "CivicTech · evidencia social · capilaridad territorial",
     "Una <b>comunidad de control social</b> que nace en Ecuador para crecer hacia América "
     "Latina. Personas, organizaciones comunitarias y academia aportan la evidencia que falta "
     "—actas, informes, fotografías de obra— y la inteligencia artificial <b>acompaña y "
     "enseña</b>: explica qué acredita cada documento, qué norma lo respalda y cómo encaja en "
     "el mapa de su territorio. No reemplaza al ciudadano: <b>lo fortalece para incidir</b>.",
     "FASE 1 · EN CONSTRUCCIÓN", "var(--verde)"),
    ("coop", "QUIRA Cooperación",
     "Universidades · organismos bilaterales · ONG",
     "Evidencia territorial verificada para investigación, cooperación e inversión basada en "
     "datos. Llega después por una razón práctica: <b>su valor es la cobertura nacional</b>, y "
     "esa cobertura la construyen antes las dos entradas.",
     "FASE 2", "var(--azul-cl)"),
    ("inst", "QUIRA Institucional",
     "Gobiernos locales · licencia independiente",
     "Herramientas para que el propio gobierno local <b>gestione lo suyo</b> con la evidencia "
     "ya publicada: ver dónde se corta su cadena documental y corregirlo. Licencia "
     "independiente, con soporte de Dylus Lab y <b>bajo una regla explícita: contratarla no "
     "modifica nada de lo que el Observatorio publica</b> sobre ese municipio.",
     "FASE 2", "var(--coral)"),
    ("econ", "QUIRA Economic",
     "Inversión y desarrollo económico local",
     "Inteligencia económica del territorio sobre la misma base de evidencia verificada.",
     "FASE 3", "var(--tx3)"),
]


def ecosistema() -> str:
    filas = "".join(
        f'<div class="ql-prod" style="--pc:{col}">'
        f'<div class="ql-prod-h"><span class="ql-prod-n">{n}</span>'
        f'<span class="ql-prod-e">{e}</span></div>'
        f'<div class="ql-prod-r">{r}</div><div class="ql-prod-d">{d}</div></div>'
        for _, n, r, d, e, col in _PRODUCTOS)
    return _sec("El ecosistema", "Un sistema, varias puertas",
        '<p class="ql-p">QUIRA no es un conjunto de aplicaciones independientes: es <b>un solo '
        'cuerpo de conocimiento</b> al que se entra por puertas distintas. Cada producto cumple '
        'una función propia dentro del mismo ecosistema.</p>'
        f'<div class="ql-prods">{filas}</div>')


# ══════════════════════════════ HUMAN IN THE LOOP ══════════════════════════════
def humano() -> str:
    cols = [("var(--coral)", "La máquina encuentra",
             "Procesa volúmenes de documentos que ninguna persona podría revisar, detecta "
             "patrones y señala dónde la evidencia falta o no concuerda."),
            ("var(--verde)", "Las personas deciden",
             "Interpretan el contexto, conocen el territorio y validan cada hallazgo. "
             "Ninguna afirmación pública se publica sin ese paso.")]
    return _sec("El método", "Inteligencia aumentada, no automatización ciega",
        '<div class="ql-hil">' + "".join(
            f'<div class="ql-hil-c"><div class="ql-hil-t" style="color:{c}">{t}</div>'
            f'<div class="ql-hil-d">{d}</div></div>' for c, t, d in cols) + '</div>'
        '<div class="ql-hil-cierre">La inteligencia artificial no constituye fuente de verdad '
        'institucional.<br>Encuentra patrones; el significado lo aportan las personas.</div>')


# ══════════════════════════════ INDEPENDENCIA ══════════════════════════════
def independencia() -> str:
    """La Tesis, íntegra pero EXPLICADA (Javo · 2026-08-05: "respetemos la tesis, pero
    mejoremos el texto para que no suene chocante con los políticos").

    No se suaviza la doctrina —"sujeto observado, no cliente" permanece—: se muestra que la
    independencia es lo que vuelve útil la evidencia PARA el propio municipio. Una evidencia
    que respalda un tercero independiente sirve ante banca y cooperación; la que emite un
    proveedor contratado por el observado, no. Deja de ser un reproche y pasa a ser una
    propuesta de valor, sin ceder nada."""
    return _sec("Una aclaración necesaria", "Independencia y servicio no se estorban",
        '<p class="ql-p">Conviene decirlo con franqueza, porque suele malinterpretarse: '
        '<b>el municipio es sujeto observado, no cliente de la observación</b>. Nadie paga '
        'por ser observado, ni por cómo resulta observado. Y esa regla no nace de desconfianza '
        'hacia los gobiernos locales — nace de lo que hace falta para que la evidencia '
        '<b>sirva de algo</b>.</p>'
        '<p class="ql-p">Un informe que un municipio encarga y paga vale poco ante un banco '
        'de desarrollo, una agencia de cooperación o una universidad: procede de la parte '
        'interesada. En cambio, un registro <b>reconstruido de forma independiente a partir de '
        'fuentes públicas</b> resiste esa pregunta. <b>La independencia no está dirigida contra '
        'el municipio: es justamente lo que vuelve utilizable su evidencia.</b> Un gobierno con '
        'buena gestión sale <b>beneficiado</b>, porque por primera vez alguien puede demostrar '
        'su trazabilidad sin que la afirmación provenga de él mismo.</p>'
        '<div class="ql-linea"><div class="ql-linea-t">Dónde está la línea</div>'
        '<div class="ql-linea-g">'
        '<div class="ql-linea-c no"><span class="ql-linea-k">Nunca</span>'
        'Pagar por ser observado, por la evaluación o por lo que se publica. '
        'La observación no se contrata, no se negocia y no se retira.</div>'
        '<div class="ql-linea-c si"><span class="ql-linea-k">Sí, y con gusto</span>'
        'Licenciar herramientas para <b>gestionar lo propio</b> con la evidencia ya publicada, '
        'con soporte de Dylus Lab. Contratarlas <b>no cambia una sola línea</b> de lo que el '
        'Observatorio dice de ese municipio.</div></div></div>'
        '<p class="ql-p">Es la misma distinción de siempre: nadie le paga al instituto de '
        'estadística para que le cambie el censo, pero cualquiera puede usar herramientas para '
        'trabajar con esos datos. Aquí igual — <b>la observación es pública e independiente; '
        'las herramientas de gestión son otra cosa</b>, y separarlas explícitamente es lo que '
        'permite ofrecer ambas sin que una contamine a la otra.</p>'
        '<p class="ql-p">Por eso el lenguaje de este sistema es deliberadamente preciso: '
        'nunca dice que alguien incumplió. Dice qué <b>puede</b> comprobarse con los '
        'documentos disponibles y qué <b>no</b>. Y cuando encuentra un corte en la cadena, lo '
        'que señala casi nunca es una falta: es un <b>instrumento de registro que no fue '
        'diseñado para dejar rastro</b> — algo que se corrige con una decisión administrativa, '
        'no con un proceso.</p>')


# ══════════════════════════════ ACCESO ══════════════════════════════
def form_header() -> str:
    return ('<div class="ql-form-title">Acceso restringido</div>'
            '<div style="text-align:center">'
            '<span class="ql-badge">🔭 Observatorio Nacional · Dylus Lab</span></div>')


def trust_badges() -> str:
    badges = [("var(--verde)", "ACCESO PROTEGIDO", "Credencial cifrada"),
              ("var(--cian)", "SESIÓN TEMPORAL", "Expira en 60 minutos"),
              ("var(--azul-cl)", "INTENTOS LIMITADOS", "Bloqueo tras 3 fallos"),
              ("var(--coral)", "ACTIVIDAD REGISTRADA", "Trazabilidad de accesos")]
    items = "".join(
        f'<div class="ql-trust-item"><div class="ql-trust-label" style="color:{c}">{l}</div>'
        f'<div class="ql-trust-sub">{s}</div></div>' for c, l, s in badges)
    return f'<div class="ql-wrap"><div class="ql-trust">{items}</div></div>'


def footer() -> str:
    import streamlit as _st_v
    return ('<div class="ql-footer">'
            '<b>QUIRA</b> · Dylus Lab © 2026 · Ecuador<br>'
            'Infraestructura de conocimiento verificable<br>'
            f'<span style="opacity:.45">build v5-chaquira · st {_st_v.__version__}</span></div>')


# ── Compatibilidad hacia atrás ────────────────────────────────────────────────
def platform_cards(selected: str = "") -> str: return ""
def card_institucional_html(active: bool = False) -> str: return ""
def card_ciudadano_html(active: bool = False) -> str: return ""
def card_cooperacion_html(active: bool = False) -> str: return ""
def card_operations_html() -> str: return ""
def splash_top(corte: str = "") -> str: return landing_hero()
def splash_bottom(gad: str = "", corte: str = "") -> str: return footer()
def error_html(msg: str) -> str:
    return (f'<div style="background:rgba(232,115,74,.1);border:1px solid rgba(232,115,74,.3);'
            f'border-radius:9px;padding:11px 15px;color:#F0A184;font-size:13px;'
            f'font-family:Inter,sans-serif;margin-top:5px">⚠️ {msg}</div>')
