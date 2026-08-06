"""
QUIRA OS — View: Landing + Acceso  ·  v7 "Papel de plano"  ·  2026-08-06

Identidad cerrada (Javo · 2026-08-05/06). Este archivo NO redibuja la marca: consume el
SVG aprobado desde `assets/marca/`. Si hace falta cambiar el logo, se cambia el activo.

LA MARCA
  · Q manteña: espiral cuadrada de dos trazos + chaquira central. Geometría intocable
    (`assets/marca/_ORIGINAL_APROBADO.svg` es la referencia).
  · Coral Spondylus #C1392B — el color de la concha que da nombre al proyecto.
    Único acento identitario: una marca con un color es más reconocible que con dos.
  · Nombre en Archivo, mayúsculas, tracking amplio: no compite con la Q.
  · Promesa: «Evidencia que transforma». Categoría: «Inteligencia pública».

POR QUÉ FONDO CLARO — y no es estética.
Un fondo oscuro es literalmente opaco, y toda la tesis del proyecto es que la información
pública debe poder verse. El registro del documento y el archivo DICE lo que QUIRA hace.
Dos registros, cada uno en su contexto (precedente exacto: la terminal de Bloomberg es
negra, el sitio de Bloomberg es blanco):
  · PAPEL DE PLANO → landing, informes, fichas, QUIRA Ciudadana. Todo lo público.
  · VOLCÁNICO      → Centro de Inteligencia Territorial, cajones, panel del Observatorio.

UN SOLO ACENTO. El jade salió del sistema: rojo + verde es un SEMÁFORO, y un semáforo
dicta «bueno / malo» — QUIRA certifica verificabilidad, no verdad. Y la escala del canon
tiene CINCO niveles (independiente · institucional · parcial · sin evidencia ·
contradicción): dos colores opuestos solo pueden expresar dos. Se resuelve con una RAMPA
del Spondylus a la ausencia, donde la intensidad indica cuánto sostiene el documento y la
falta de color indica falta de evidencia — nunca un suspenso.

Contenido: ADR-041 (arquitectura de productos) + CONSTITUCION-001 (identidad) +
Constitución Ontológica (la cadena madre). La Tesis se respeta íntegra y se EXPLICA
(§independencia): «no cliente de la observación» — la licencia de gestión sí es posible.
Dylus Lab © 2026
"""
from __future__ import annotations

import re
from pathlib import Path

_MARCA = Path(__file__).resolve().parents[1] / "assets" / "marca"


#: El logo NO es cuadrado — su lienzo es 150×160 (relación 0,9375). Forzar width=height
#: lo estiraría, así que la altura manda y el ancho se deriva.
_ASPECTO = 150 / 160


def _logo(variante: str = "coral", px: int = 96) -> str:
    """Inserta el SVG aprobado tal cual, ajustando solo su tamaño de render.

    La geometría NO se reconstruye: se lee el activo de `assets/marca/`, que proviene de la
    vectorización que aportó Javo (2026-08-06) con dos artefactos retirados — el contorno
    duplicado del trazado y el destello decorativo que las herramientas de IA añaden a sus
    salidas, y que se habría publicado como parte de la marca.

    Historial de esta función, porque el error se repitió dos veces:
      1ª · redibujé la Q con paths propios → no era el logo de Javo.
      2ª · usé un SVG de conversión automática que solo tenía 2 paths y perdía los niveles
           interiores → se publicó una versión pobre.
    Regla: si el logo cambia, se cambia el ARCHIVO. Aquí nunca se dibuja."""
    try:
        svg = (_MARCA / f"quira_{variante}.svg").read_text(encoding="utf-8")
        return re.sub(r"<svg ", f'<svg width="{round(px * _ASPECTO)}" height="{px}" ', svg, count=1)
    except Exception:  # noqa: BLE001
        return f'<div style="font:800 {px//2}px Archivo,sans-serif;color:#C1392B">Q</div>'


CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root{
  /* ── SISTEMA VISUAL v1.1 · UN SOLO ACENTO ───────────────────────────────────
     El marfil cálido salió: estaba a Δ=7 del fondo de Anthropic y a Δ=15 de su
     texto — se distinguía el acento y no lo que ocupa el 90% de la pantalla.
     Base nueva: el gris-azul del PAPEL DE PLANO, el del levantamiento
     topográfico y del plano de ordenamiento territorial. Baja 7 puntos de
     luminosidad y voltea la temperatura a frío, que es lo que el ojo distingue.

     Y el jade salió también, por una razón doctrinal: rojo + verde es un
     SEMÁFORO, y un semáforo dicta «bueno / malo». QUIRA certifica
     verificabilidad, no verdad. Además la escala del canon tiene CINCO niveles
     y dos colores opuestos solo pueden expresar dos: hace falta una RAMPA.
     Un solo acento identitario, además, es más reconocible que dos. */
  --coral:#C1392B;        /* Spondylus · LA marca. Único acento identitario   */
  --coral-cl:#D4715F;     /* Spondylus claro · verificabilidad parcial        */
  --coral-dp:#8E2419;     /* Spondylus profundo · verificabilidad independiente */
  --coral-bg:rgba(193,57,43,.06);
  --plano:#D9E0E5;        /* base · papel de levantamiento                    */
  --sup:#F3F6F7;          /* superficie de tarjeta — se levanta del plano     */
  --carril:#C2CDD4;       /* ausencia de evidencia · fondo de barra           */
  --pizarra:#4E6674;      /* dato sin evidencia · 4,53:1 sobre el plano (AA)  */
  --tx:#18232B;           /* tinta · azul-pizarra profundo                    */
  --tx2:#52616B;
  --tx3:#8296A2;
  --bd:#B9C6CD;
  --sf:#F3F6F7;
}

[data-testid="stHeader"],[data-testid="stToolbar"],
[data-testid="stDecoration"],footer{display:none !important}

[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(ellipse 58% 34% at 50% -8%, rgba(193,57,43,.055) 0%, transparent 60%),
    var(--plano) !important;
  min-height:100vh;
}
[data-testid="stMain"] .block-container{padding:0 !important;max-width:100% !important}

/* textura de papel — no un degradado digital */
[data-testid="stAppViewContainer"]::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)' opacity='.03'/%3E%3C/svg%3E");
}

.qw{max-width:880px;margin:0 auto;padding:0 26px;position:relative;z-index:1}

/* ═══ HERO ═══ */
.q-hero{display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:64px 26px 26px;position:relative;z-index:1}
.q-hero svg{animation:q-in 1s cubic-bezier(.2,.7,.3,1) both}
@keyframes q-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.q-name{font:600 54px/1 'Archivo',sans-serif;letter-spacing:.19em;color:var(--tx);
  margin:24px 0 0;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .1s both}
.q-promesa{font:500 11.5px/1 'JetBrains Mono',monospace;letter-spacing:.26em;
  color:var(--coral);margin-top:15px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .2s both}
.q-cat{font:400 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.22em;color:var(--tx3);
  margin-top:7px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .26s both}
.q-tag{font:400 16.5px/1.75 'Inter',sans-serif;color:var(--tx2);max-width:600px;
  margin-top:26px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .34s both}
.q-tag b{color:var(--tx);font-weight:600}

/* ═══ GRECA · separador manteño ═══ */
.q-greca{max-width:880px;margin:46px auto 0;padding:0 26px;position:relative;z-index:1}

/* ═══ SECCIONES ═══ */
.q-sec{margin:44px auto 0;max-width:880px;padding:0 26px;position:relative;z-index:1}
.q-kick{font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.2em;text-transform:uppercase;
  color:var(--coral);margin-bottom:12px;display:flex;align-items:center;gap:11px}
.q-kick::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--bd),transparent)}
.q-h2{font:600 31px/1.2 'Fraunces',Georgia,serif;color:var(--tx);letter-spacing:-.015em;
  margin-bottom:15px}
.q-p{font:400 15.5px/1.78 'Inter',sans-serif;color:var(--tx2);max-width:730px}
.q-p b{color:var(--tx);font-weight:600}
.q-p+.q-p{margin-top:13px}
.q-cap{font:400 13px/1.7 'Inter',sans-serif;color:var(--tx3);max-width:730px;margin-top:12px}
.q-cap b{color:var(--tx2)}

/* ═══ ORIGEN ═══ */
.q-origen{border:1px solid var(--bd);border-left:3px solid var(--coral);border-radius:13px;
  padding:26px 30px;background:linear-gradient(102deg,var(--coral-bg),transparent 66%),var(--sf)}
.q-quote{font:400 20px/1.6 'Fraunces',Georgia,serif;color:var(--tx);font-style:italic;
  margin-bottom:14px}
.q-quote em{color:var(--coral);font-style:italic}
.q-txt{font:400 14.5px/1.76 'Inter',sans-serif;color:var(--tx2)}
.q-txt b{color:var(--tx);font-weight:600}

/* ═══ NEGACIONES ═══ */
.q-nos{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:19px}
.q-no{font:500 12.5px/1 'JetBrains Mono',monospace;color:var(--coral);
  border:1px solid rgba(193,57,43,.26);border-radius:15px;padding:8px 16px;
  background:var(--coral-bg);white-space:nowrap}

/* ═══ CADENA ═══ */
.q-cad{display:flex;flex-wrap:wrap;align-items:center;margin:18px 0 4px}
.q-link{font:600 12px/1 'JetBrains Mono',monospace;color:var(--tx2);border:1px solid var(--bd);
  border-radius:6px;padding:10px 13px;margin:4px;background:var(--sf)}
.q-link.on{color:var(--pizarra);border-color:rgba(78,102,116,.4);background:rgba(78,102,116,.09)}
.q-link small{display:block;font:400 9px/1 'JetBrains Mono';color:var(--tx3);
  margin-top:4px;letter-spacing:.03em}
.q-cut{color:var(--coral);font-size:16px;margin:0 4px}
.q-arw{color:var(--tx3);font-size:13px;margin:0 2px}

/* ═══ FLUJO ═══ */
.q-flow{display:flex;flex-wrap:wrap;gap:11px;margin:20px 0 6px}
.q-node{flex:1 1 178px;border:1px solid var(--bd);border-top:2px solid var(--nc,var(--coral));
  border-radius:11px;padding:16px 18px;background:var(--sf)}
.q-node-k{font:700 8.5px/1 'JetBrains Mono',monospace;letter-spacing:.13em;text-transform:uppercase;
  color:var(--nc,var(--coral));display:block;margin-bottom:7px}
.q-node-t{font:700 14.5px/1.3 'Inter',sans-serif;color:var(--tx);margin-bottom:4px}
.q-node-d{font:400 12px/1.6 'Inter',sans-serif;color:var(--tx2)}

/* ═══ PRODUCTOS ═══ */
.q-prods{display:flex;flex-direction:column;gap:10px;margin-top:17px}
.q-prod{border:1px solid var(--bd);border-left:3px solid var(--pc,var(--coral));border-radius:11px;
  padding:19px 23px;background:var(--sf);transition:transform .25s,background .25s}
.q-prod:hover{background:rgba(255,255,255,.85);transform:translateX(3px)}
.q-prod-h{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  flex-wrap:wrap;margin-bottom:3px}
.q-prod-n{font:600 19px/1.3 'Fraunces',Georgia,serif;color:var(--tx)}
.q-prod-e{font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.11em;
  color:var(--pc,var(--coral));white-space:nowrap}
.q-prod-r{font:500 11.5px/1 'Inter',sans-serif;color:var(--pc,var(--coral));margin-bottom:9px;opacity:.92}
.q-prod-d{font:400 13.8px/1.72 'Inter',sans-serif;color:var(--tx2)}
.q-prod-d b{color:var(--tx);font-weight:600}

/* ═══ MÉTODO ═══ */
.q-duo{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.q-duo-c{border:1px solid var(--bd);border-radius:11px;padding:18px 21px;background:var(--sf)}
.q-duo-t{font:700 13px/1.3 'Inter',sans-serif;margin-bottom:6px}
.q-duo-d{font:400 13px/1.68 'Inter',sans-serif;color:var(--tx2)}
.q-cierre{font:400 17.5px/1.6 'Fraunces',Georgia,serif;color:var(--tx);font-style:italic;
  text-align:center;margin-top:19px;padding-top:17px;border-top:1px solid var(--bd)}

/* ═══ LA LÍNEA ═══ */
.q-linea{border:1px solid var(--bd);border-radius:12px;padding:20px 23px;margin:19px 0;background:var(--sf)}
.q-linea-t{font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.17em;text-transform:uppercase;
  color:var(--tx3);margin-bottom:13px}
.q-linea-g{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.q-linea-c{border-radius:9px;padding:15px 18px;font:400 13.2px/1.68 'Inter',sans-serif;color:var(--tx2)}
.q-linea-c b{color:var(--tx);font-weight:600}
.q-linea-c.no{border:1px solid rgba(193,57,43,.26);background:var(--coral-bg)}
.q-linea-c.si{border:1px solid rgba(78,102,116,.3);background:rgba(78,102,116,.07)}
.q-linea-k{display:block;font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.12em;
  text-transform:uppercase;margin-bottom:7px}
.q-linea-c.no .q-linea-k{color:var(--coral)}
.q-linea-c.si .q-linea-k{color:var(--pizarra)}

/* ═══ ACCESO ═══ */
[data-testid="stButton"] button{
  background:var(--coral-bg) !important;border:1px solid rgba(193,57,43,.3) !important;
  border-radius:12px !important;min-height:auto !important;height:auto !important;
  white-space:pre-line !important;text-align:center !important;padding:19px 22px !important;
  font-family:'Inter',sans-serif !important;color:var(--tx) !important;font-size:15px !important;
  font-weight:600 !important;line-height:1.6 !important;transition:all .22s !important;
  display:flex !important;flex-direction:column !important;align-items:center !important;
  cursor:pointer !important;width:100% !important}
[data-testid="stButton"] button:hover{border-color:var(--coral) !important;
  background:rgba(193,57,43,.1) !important;transform:translateY(-1px) !important}
[data-testid="stButton"] button p,[data-testid="stButton"] button span{white-space:pre-line !important}

div[data-testid="stForm"]{background:var(--sup) !important;
  border:1px solid rgba(193,57,43,.2) !important;border-radius:14px !important;
  padding:24px 28px 20px !important;backdrop-filter:blur(10px) !important}
.q-form-t{font:700 10.5px/1 'JetBrains Mono',monospace;color:var(--tx3);text-transform:uppercase;
  letter-spacing:.15em;text-align:center;margin-bottom:12px}
.q-badge{display:block;width:fit-content;margin:0 auto 18px;background:var(--coral-bg);
  border:1px solid rgba(193,57,43,.24);border-radius:18px;padding:6px 16px;
  font:500 10.5px/1 'JetBrains Mono',monospace;color:var(--coral)}
div[data-testid="stTextInput"] input{background:#FFF !important;border:1px solid var(--bd) !important;
  color:var(--tx) !important;border-radius:8px !important;font-size:15px !important}
div[data-testid="stTextInput"] input:focus{border-color:var(--coral) !important}
div[data-testid="stTextInput"] label{color:var(--tx3) !important;font-size:10.5px !important;
  font-weight:700 !important;text-transform:uppercase !important;letter-spacing:.1em !important}
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[data-testid="baseButton-primaryFormSubmit"]{
  background:var(--coral) !important;color:#FFF !important;font-weight:700 !important;
  font-size:13px !important;border:none !important;border-radius:9px !important;
  letter-spacing:.09em !important;min-height:auto !important;padding:15px !important;
  white-space:normal !important;flex-direction:row !important}
div[data-testid="stForm"] button:hover{opacity:.9 !important}

/* ═══ CONFIANZA ═══ */
.q-trust{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:24px auto 12px}
.q-trust-i{border:1px solid var(--bd);border-radius:10px;padding:12px 14px;background:var(--sf)}
.q-trust-l{font:700 10.5px/1.3 'Inter',sans-serif;text-transform:uppercase;letter-spacing:.06em}
.q-trust-s{font:400 11px/1.45 'Inter',sans-serif;color:var(--tx3);margin-top:3px}

/* ═══ FOOTER ═══ */
.q-footer{text-align:center;padding:26px 24px 32px;font:400 11.5px/1.95 'JetBrains Mono',monospace;
  color:var(--tx3);border-top:1px solid var(--bd);margin-top:36px;position:relative;z-index:1}
.q-footer b{color:var(--tx2)}

button.q-ops,.q-ops-w button{background:transparent !important;
  border:1px solid var(--bd) !important;color:var(--tx3) !important;
  font:500 9.5px/1 'JetBrains Mono',monospace !important;letter-spacing:.09em !important;
  border-radius:6px !important;padding:7px 14px !important;opacity:.5 !important;
  white-space:normal !important;flex-direction:row !important;font-weight:500 !important}
button.q-ops:hover,.q-ops-w button:hover{opacity:.85 !important;transform:none !important;
  border-color:rgba(193,57,43,.3) !important}

@media(max-width:720px){
  .q-name{font-size:38px;letter-spacing:.14em}.q-h2{font-size:24px}
  .q-tag{font-size:14.5px}.q-p{font-size:14.5px}.q-quote{font-size:17px}
  .q-prod-n{font-size:17px}.q-duo,.q-trust,.q-linea-g{grid-template-columns:1fr}
  .q-hero{padding:42px 18px 20px}.q-sec{margin-top:34px}
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
      b.classList.add('q-ops');
      var w=b.closest('[data-testid="stButton"]'); if(w) w.classList.add('q-ops-w');}});}
  new MutationObserver(t).observe(document.body,{childList:true,subtree:true});})();
</script>"""


def _sec(kick: str, h2: str, cuerpo: str) -> str:
    return (f'<div class="q-sec"><div class="q-kick">{kick}</div>'
            f'<div class="q-h2">{h2}</div>{cuerpo}</div>')


def greca() -> str:
    """Separador con la greca escalonada manteña — la pirámide que 'comunica la idea de
    montaña o cerro'. Aquí sí entra: como sistema gráfico, no cargando el logotipo."""
    return ('<div class="q-greca"><svg width="100%" height="16" viewBox="0 0 880 16" '
            'preserveAspectRatio="none">'
            '<path d="M0 13 L60 13 L60 8 L120 8 L120 3 L180 3 L180 8 L240 8 L240 13 L300 13 '
            'L300 8 L360 8 L360 3 L420 3 L420 8 L480 8 L480 13 L540 13 L540 8 L600 8 L600 3 '
            'L660 3 L660 8 L720 8 L720 13 L780 13 L780 8 L840 8 L840 3 L880 3" '
            'fill="none" stroke="#C1392B" stroke-width="1.6" opacity=".3"/></svg></div>')


# ══════════════════════════ HERO ══════════════════════════
def landing_hero() -> str:
    return (
        f'<div class="q-hero">{_logo("coral", 88)}'
        f'<div class="q-name">QUIRA</div>'
        f'<div class="q-promesa">EVIDENCIA QUE TRANSFORMA</div>'
        f'<div class="q-cat">INTELIGENCIA PÚBLICA · DYLUS LAB · ECUADOR</div>'
        f'<div class="q-tag">Infraestructura de <b>conocimiento verificable</b> sobre la gestión '
        f'del territorio, al servicio de gobiernos, ciudadanía, academia y cooperación '
        f'internacional.</div></div>')


# ══════════════════════════ ORIGEN ══════════════════════════
def origen() -> str:
    return _sec("El origen", "Una chaquira a la vez",
        '<div class="q-origen">'
        '<div class="q-quote">QUIRA viene de <em>chaquira</em>, del antiguo dialecto manteño de '
        'Cancebí: fragmentos de la concha <em>Spondylus</em> con los que los pueblos manteños y '
        'huancavilcas labraban los collares de su élite.</div>'
        '<div class="q-txt">Para esos pueblos el <b>Spondylus</b> era reserva de valor e '
        'intercambio entre territorios — la estructura madre de la que todo se desprende, y de '
        'la que este laboratorio toma su nombre: spon<b>·DYLUS</b>. Cada fragmento labrado con '
        'paciencia era una <b>chaquira</b>: la unidad indivisible de valor.<br><br>'
        'Un collar de chaquiras no era un adorno: era <b>símbolo de autoridad y de acuerdo entre '
        'comunidades</b>. Aquí cada dato, cada documento y cada aporte ciudadano es una chaquira; '
        'QUIRA las enhebra hasta formar un <b>collar de integridad para el territorio</b>. '
        'Ninguna pieza sostiene sola el conjunto, y el conjunto no existe sin cada pieza.<br><br>'
        'El símbolo que ves arriba es la <b>espiral cuadrada</b> manteña, que los señores de la '
        'Ciudad de los Cerros reservaban para la autoridad legítima. Es una línea que se recorre '
        'hasta su origen — y en su centro, la chaquira.</div></div>')


# ══════════════════════════ QUÉ ES ══════════════════════════
def que_es() -> str:
    nos = "".join(f'<span class="q-no">{t}</span>' for t in
                  ("no es un software municipal", "no es una auditoría",
                   "no es solo un observatorio"))
    return _sec("Qué es", "Conocimiento verificable, no opinión",
        f'<div class="q-nos">{nos}</div>'
        '<p class="q-p">QUIRA convierte <b>evidencia pública dispersa</b> en conocimiento que '
        'puede comprobarse. No mide trámites ni obras aisladas: sigue la cadena que va de la '
        '<b>promesa</b> al <b>territorio</b> y muestra dónde se interrumpe.</p>'
        '<p class="q-p">Cada afirmación se ancla a un documento — o a la ausencia '
        '<b>documentada</b> de uno. QUIRA <b>no sustituye a los órganos de control ni determina '
        'responsabilidades</b>: establece el <b>nivel de verificabilidad</b> de la evidencia '
        'disponible. Qué existe, qué puede comprobarse y qué permanece sin demostrar.</p>')


# ══════════════════════════ PROBLEMA ══════════════════════════
_CADENA = [("Promesa", "plan de gobierno"), ("Plan", "PDOT"), ("Presupuesto", "asignación"),
           ("Ejecución", "contratación"), ("Resultado", "bienes y servicios"),
           ("Territorio", "impacto en la gente")]


def problema() -> str:
    nodos = ""
    for i, (t, s) in enumerate(_CADENA):
        if i:
            nodos += ('<span class="q-cut">✕</span>' if i == 3 else '<span class="q-arw">→</span>')
        nodos += (f'<span class="q-link{" on" if i < 3 else ""}">{t}<small>{s}</small></span>')
    return _sec("El problema", "La información existe. La trazabilidad, no siempre",
        '<p class="q-p">Un compromiso de campaña puede no aparecer en la planificación. La '
        'planificación puede no reflejarse en el presupuesto. El presupuesto puede ejecutarse sin '
        'que conste <b>dónde</b> ni <b>sobre quién</b>. Cada eslabón vive en un sistema distinto '
        'del Estado, y ninguno fue diseñado para hablar con los otros.</p>'
        f'<div class="q-cad">{nodos}</div>'
        '<p class="q-p">El problema rara vez es la falta de datos: es que <b>la cadena se corta</b> '
        'en algún punto y nadie puede señalar dónde. QUIRA la reconstruye documento por documento '
        'y, cuando encuentra el corte, <b>lo nombra</b>.</p>')


# ══════════════════════════ CÓMO FUNCIONA ══════════════════════════
def como_funciona() -> str:
    n = [("var(--pizarra)", "Entrada", "Observatorio Nacional",
          "Monitorea de forma progresiva los sistemas públicos de los 222 municipios."),
         ("var(--pizarra)", "Entrada", "QUIRA Ciudadana",
          "Incorpora la evidencia que la ciudadanía aporta desde el territorio."),
         ("var(--coral)", "Proceso", "Sistema de inteligencia",
          "Contrasta ambas fuentes contra la norma y reconstruye la cadena."),
         ("var(--tx)", "Núcleo", "Centro de Inteligencia Territorial",
          "Donde la evidencia se vuelve conocimiento consultable. Único: todo converge aquí.")]
    nodos = "".join(
        f'<div class="q-node" style="--nc:{c}"><span class="q-node-k">{k}</span>'
        f'<div class="q-node-t">{t}</div><div class="q-node-d">{d}</div></div>'
        for c, k, t, d in n)
    return _sec("Cómo funciona", "Dos fuentes, un solo cuerpo de conocimiento",
        f'<div class="q-flow">{nodos}</div>'
        '<p class="q-p" style="margin-top:14px">Las dos entradas son <b>distintas por '
        'naturaleza</b>: una detecta la evidencia que ya existe en los sistemas del Estado; la '
        'otra ayuda a producir la que falta. Ninguna sustituye a la otra, y ambas alimentan el '
        'mismo cuerpo de conocimiento — no bases separadas que después se contradicen.</p>')


# ══════════════════════════ ECOSISTEMA ══════════════════════════
_PRODUCTOS = [
    ("Observatorio Nacional de Integridad Territorial",
     "Evidencia institucional · escala nacional",
     "Monitoreo progresivo de los <b>222 municipios</b> del país, incorporados según su "
     "disponibilidad documental y su ciclo administrativo. Agentes de inteligencia artificial "
     "revisan los sistemas públicos —transparencia, contratación, rendición de cuentas, portales "
     "institucionales— y <b>toda captura se valida antes de publicarse</b>.",
     "FASE 1 · ACTIVO", "var(--coral)"),
    ("QUIRA Ciudadana",
     "CivicTech · evidencia social · capilaridad territorial",
     "Una <b>comunidad de control social</b> que nace en Ecuador para crecer hacia América "
     "Latina. Personas, organizaciones comunitarias y academia aportan la evidencia que falta "
     "—actas, informes, fotografías de obra— y la inteligencia artificial <b>acompaña y "
     "enseña</b>: explica qué acredita cada documento, qué norma lo respalda y cómo encaja en el "
     "mapa de su territorio. No reemplaza al ciudadano: <b>lo fortalece para incidir</b>.",
     "FASE 1 · EN CONSTRUCCIÓN", "var(--pizarra)"),
    ("QUIRA Cooperación",
     "Universidades · organismos bilaterales · ONG",
     "Evidencia territorial verificada para investigación, cooperación e inversión basada en "
     "datos. Llega después por una razón práctica: <b>su valor es la cobertura nacional</b>, y "
     "esa cobertura la construyen antes las dos entradas.",
     "FASE 2", "var(--tx2)"),
    ("QUIRA Institucional",
     "Gobiernos locales · licencia independiente",
     "Herramientas para que el propio gobierno local <b>gestione lo suyo</b> con la evidencia ya "
     "publicada: ver dónde se corta su cadena documental y corregirlo. Licencia independiente, "
     "con soporte de Dylus Lab y bajo una regla explícita — <b>contratarla no modifica nada de lo "
     "que el Observatorio publica</b> sobre ese municipio.",
     "FASE 2", "var(--tx2)"),
    ("QUIRA Economic",
     "Inversión y desarrollo económico local",
     "Inteligencia económica del territorio sobre la misma base de evidencia verificada.",
     "FASE 3", "var(--tx3)"),
]


def ecosistema() -> str:
    filas = "".join(
        f'<div class="q-prod" style="--pc:{col}">'
        f'<div class="q-prod-h"><span class="q-prod-n">{n}</span>'
        f'<span class="q-prod-e">{e}</span></div>'
        f'<div class="q-prod-r">{r}</div><div class="q-prod-d">{d}</div></div>'
        for n, r, d, e, col in _PRODUCTOS)
    return _sec("El ecosistema", "Un sistema, varias puertas",
        '<p class="q-p">QUIRA no es un conjunto de aplicaciones independientes: es <b>un solo '
        'cuerpo de conocimiento</b> al que se entra por puertas distintas. Cada producto cumple '
        'una función propia dentro del mismo ecosistema.</p>'
        f'<div class="q-prods">{filas}</div>')


# ══════════════════════════ MÉTODO ══════════════════════════
def humano() -> str:
    cols = [("var(--coral)", "La máquina encuentra",
             "Procesa volúmenes de documentos que ninguna persona podría revisar, detecta "
             "patrones y señala dónde la evidencia falta o no concuerda."),
            ("var(--pizarra)", "Las personas deciden",
             "Interpretan el contexto, conocen el territorio y validan cada hallazgo. Ninguna "
             "afirmación pública se publica sin ese paso.")]
    return _sec("El método", "Inteligencia aumentada, no automatización ciega",
        '<div class="q-duo">' + "".join(
            f'<div class="q-duo-c"><div class="q-duo-t" style="color:{c}">{t}</div>'
            f'<div class="q-duo-d">{d}</div></div>' for c, t, d in cols) + '</div>'
        '<div class="q-cierre">La inteligencia artificial no constituye fuente de verdad '
        'institucional.<br>Encuentra patrones; el significado lo aportan las personas.</div>')


# ══════════════════════════ INDEPENDENCIA ══════════════════════════
def independencia() -> str:
    return _sec("Una aclaración necesaria", "Independencia y servicio no se estorban",
        '<p class="q-p">Conviene decirlo con franqueza, porque suele malinterpretarse: <b>el '
        'municipio es sujeto observado, no cliente de la observación</b>. Nadie paga por ser '
        'observado, ni por cómo resulta observado. Y esa regla no nace de desconfianza hacia los '
        'gobiernos locales — nace de lo que hace falta para que la evidencia <b>sirva de '
        'algo</b>.</p>'
        '<p class="q-p">Un informe que un municipio encarga y paga vale poco ante un banco de '
        'desarrollo, una agencia de cooperación o una universidad: procede de la parte interesada. '
        'En cambio, un registro <b>reconstruido de forma independiente a partir de fuentes '
        'públicas</b> resiste esa pregunta. <b>La independencia no está dirigida contra el '
        'municipio: es justamente lo que vuelve utilizable su evidencia.</b> Un gobierno con buena '
        'gestión sale <b>beneficiado</b>, porque por primera vez alguien puede demostrar su '
        'trazabilidad sin que la afirmación provenga de él mismo.</p>'
        '<div class="q-linea"><div class="q-linea-t">Dónde está la línea</div>'
        '<div class="q-linea-g">'
        '<div class="q-linea-c no"><span class="q-linea-k">Nunca</span>'
        'Pagar por ser observado, por la evaluación o por lo que se publica. La observación no se '
        'contrata, no se negocia y no se retira.</div>'
        '<div class="q-linea-c si"><span class="q-linea-k">Sí, y con gusto</span>'
        'Licenciar herramientas para <b>gestionar lo propio</b> con la evidencia ya publicada, con '
        'soporte de Dylus Lab. Contratarlas <b>no cambia una sola línea</b> de lo que el '
        'Observatorio dice de ese municipio.</div></div></div>'
        '<p class="q-p">Es la misma distinción de siempre: nadie le paga al instituto de '
        'estadística para que le cambie el censo, pero cualquiera puede usar herramientas para '
        'trabajar con esos datos. Aquí igual — <b>la observación es pública e independiente; las '
        'herramientas de gestión son otra cosa</b>, y separarlas explícitamente es lo que permite '
        'ofrecer ambas sin que una contamine a la otra.</p>'
        '<p class="q-cap">Por eso el lenguaje de este sistema es deliberadamente preciso: nunca '
        'dice que alguien incumplió. Dice qué <b>puede</b> comprobarse con los documentos '
        'disponibles y qué <b>no</b>. Y cuando encuentra un corte en la cadena, lo que señala casi '
        'nunca es una falta: es un <b>instrumento de registro que no fue diseñado para dejar '
        'rastro</b> — algo que se corrige con una decisión administrativa, no con un proceso.</p>')


# ══════════════════════════ ACCESO ══════════════════════════
def form_header() -> str:
    return ('<div class="q-form-t">Acceso restringido</div><div style="text-align:center">'
            '<span class="q-badge">Observatorio Nacional · Dylus Lab</span></div>')


def trust_badges() -> str:
    badges = [("var(--pizarra)", "ACCESO PROTEGIDO", "Credencial cifrada"),
              ("var(--coral)", "SESIÓN TEMPORAL", "Expira en 60 minutos"),
              ("var(--tx2)", "INTENTOS LIMITADOS", "Bloqueo tras 3 fallos"),
              ("var(--tx2)", "ACTIVIDAD REGISTRADA", "Trazabilidad de accesos")]
    items = "".join(f'<div class="q-trust-i"><div class="q-trust-l" style="color:{c}">{l}</div>'
                    f'<div class="q-trust-s">{s}</div></div>' for c, l, s in badges)
    return f'<div class="qw"><div class="q-trust">{items}</div></div>'


def footer() -> str:
    import streamlit as _st_v
    return (f'<div class="q-footer">{_logo("coral", 26)}<br>'
            f'<b>QUIRA</b> · Dylus Lab © 2026 · Ecuador<br>'
            f'Infraestructura de conocimiento verificable<br>'
            f'<span style="opacity:.5">build v6-marfil · st {_st_v.__version__}</span></div>')


# ── Compatibilidad hacia atrás ────────────────────────────────────────────────
def platform_cards(selected: str = "") -> str: return ""
def card_institucional_html(active: bool = False) -> str: return ""
def card_ciudadano_html(active: bool = False) -> str: return ""
def card_cooperacion_html(active: bool = False) -> str: return ""
def card_operations_html() -> str: return ""
def splash_top(corte: str = "") -> str: return landing_hero()
def splash_bottom(gad: str = "", corte: str = "") -> str: return footer()
def error_html(msg: str) -> str:
    return (f'<div style="background:rgba(193,57,43,.08);border:1px solid rgba(193,57,43,.28);'
            f'border-radius:9px;padding:11px 15px;color:#A83226;font-size:13px;'
            f'font-family:Inter,sans-serif;margin-top:5px">⚠️ {msg}</div>')
