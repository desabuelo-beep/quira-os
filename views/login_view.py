"""
QUIRA OS — View: Landing + Acceso  ·  v7 "Papel de plano"  ·  2026-08-06

Identidad cerrada (Javo · 2026-08-05/06). Este archivo NO redibuja la marca: consume el
SVG aprobado desde `assets/marca/`. Si hace falta cambiar el logo, se cambia el activo.

LA MARCA
  · Q manteña: espiral cuadrada de dos trazos + nodo central. Geometría intocable
    (`assets/marca/_ORIGINAL_APROBADO.svg` es la referencia).

REGISTRO DEL ORIGEN (Javo · 2026-08-06). La sección "origen" NO folcloriza. En español
moderno «chaquira» significa bisutería: usarla como titular o como metáfora repetida
—«cada dato es una chaquira»— hace leer QUIRA como proyecto patrimonial y MINUSVALORA el
dato ante un ministro o un director de banca de desarrollo. La palabra aparece UNA vez,
como etimología explicada, y el vocabulario de la sección es el de arquitectura de datos:
unidad de evidencia · cadena verificable · nodo de integridad. El origen manteño se queda
porque respalda soberanía, no porque decore.
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

# La marca vive en `utils/marca.py` — un solo módulo toca los activos, y ahí
# está escrito por qué (la Q se redibujó dos veces y las dos veces salió mal).
# El Centro de Inteligencia usa la misma función con la variante marfil: si el
# acceso a la marca estuviera duplicado, una de las dos copias envejecería.
from utils.marca import logo as _logo


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

/* ═══ ANCHOS ═══════════════════════════════════════════════════════════════
   Javo (2026-08-07): «todo está comprimido en el centro y hay espacios de los
   lados sin aprovechar». Correcto, pero la solución NO es ensanchar el texto:
   una línea de más de ~75 caracteres cuesta más de leer porque el ojo pierde
   el salto de renglón. Es tipografía, no gusto.

   Primera versión: contenedor ancho y texto a 74ch. Javo lo revisó en pantalla
   grande y volvió a señalar lo mismo — «se siguen viendo muchas partes
   recogidas a la izquierda dejando espacios inmensos; el texto debe llegar de
   extremo a extremo». Es su decisión, tomada con el argumento delante.

   Se compensa con INTERLINEADO: a línea larga, más aire entre renglones, que es
   lo que sostiene el salto de línea cuando la medida crece. */
:root{--ancho:1180px; --lectura:100%}

.qw{max-width:var(--ancho);margin:0 auto;padding:0 34px;position:relative;z-index:1}

/* ═══ HERO ═══ */
.q-hero{display:flex;flex-direction:column;align-items:center;text-align:center;
  padding:64px 26px 26px;position:relative;z-index:1}
.q-hero svg{animation:q-in 1s cubic-bezier(.2,.7,.3,1) both}
@keyframes q-in{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.q-name{font:600 54px/1 'Archivo',sans-serif;letter-spacing:.19em;color:var(--tx);
  margin:24px 0 0;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .1s both}
.q-promesa{font:500 11.5px/1 'JetBrains Mono',monospace;letter-spacing:.26em;
  color:var(--coral-dp);margin-top:15px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .2s both}
.q-cat{font:400 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.22em;color:var(--tx3);
  margin-top:7px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .26s both}
.q-tag{font:400 17px/1.8 'Inter',sans-serif;color:var(--tx2);max-width:760px;
  margin-top:26px;animation:q-in 1s cubic-bezier(.2,.7,.3,1) .34s both}
.q-tag b{color:var(--tx);font-weight:600}

/* ═══ GRECA · separador manteño ═══ */
.q-greca{max-width:var(--ancho);margin:46px auto 0;padding:0 34px;position:relative;z-index:1}

/* ═══ SECCIONES ═══ */
.q-sec{margin:52px auto 0;max-width:var(--ancho);padding:0 34px;position:relative;z-index:1}
/* ═══ KICKER CON ESCALERA MANTEÑA ══════════════════════════════════════════
   Javo (2026-08-07): la greca vivía en un separador aparte y el encabezado de
   sección usaba «una simple línea recta sosa». Se integra el patrón geométrico
   en el propio título: la escalera sale a IZQUIERDA y DERECHA del texto y lo
   contiene, en vez de decorar por su cuenta a varios centímetros de distancia.

   El patrón es el mismo escalonado del separador, reducido a un módulo de 34×9
   que se repite. Va en `background-image` con un SVG en línea —sin peticiones
   externas— y se recorta al ancho disponible a cada lado. */
/* Encabezado de sección — ver `_sec()` para el porqué.

   EL TRAZO NO SE INTERRUMPE (Javo · 2026-08-07): «si no, no hay trazabilidad,
   no hay cadena». La versión anterior repetía el motivo desde el borde exterior
   y quedaba cortado justo donde debía tocar el título — el punto que importa.

   Dos correcciones: el módulo empieza y termina a la MISMA altura (y=8), así
   cualquier repetición empalma sin escalón; y cada lado se ancla HACIA EL
   CENTRO —el izquierdo alineado a la derecha, el derecho a la izquierda—, de
   modo que el trazo llegue entero al título y el recorte quede en el extremo
   exterior, donde no se lee como rotura. */
.q-kick{margin-bottom:18px;display:flex;align-items:center;justify-content:center}
.q-kick::before,.q-kick::after{content:"";flex:1;height:16px;opacity:.55;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='16' viewBox='0 0 64 16'%3E%3Cpath d='M0 8H8V13H24V3H40V13H56V8H64' fill='none' stroke='%23C1392B' stroke-width='1.5' stroke-linejoin='miter'/%3E%3C/svg%3E");
  background-repeat:repeat-x}
.q-kick::before{background-position:right center}
.q-kick::after{background-position:left center}
/* El título enhebrado en el hilo: el trazo entra por ambos bordes. */
.q-kick-t{flex:0 0 auto;font:700 10px/1 'JetBrains Mono',monospace;
  letter-spacing:.2em;text-transform:uppercase;color:var(--coral-dp);
  border:1px solid rgba(193,57,43,.34);border-radius:20px;padding:7px 18px;
  background:var(--sup);white-space:nowrap;position:relative}
@media(max-width:620px){
  .q-kick-t{font-size:9px;padding:6px 11px;letter-spacing:.13em}
}
.q-h2{font:600 31px/1.2 'Fraunces',Georgia,serif;color:var(--tx);letter-spacing:-.015em;
  margin-bottom:15px}
/* Texto a todo el ancho, con el interlineado subido para sostener la medida. */
.q-p{font:400 15.5px/1.92 'Inter',sans-serif;color:var(--tx2);max-width:var(--lectura)}
.q-p b{color:var(--tx);font-weight:600}
.q-p+.q-p{margin-top:15px}
.q-cap{font:400 13px/1.85 'Inter',sans-serif;color:var(--tx3);max-width:var(--lectura);margin-top:14px}
.q-cap b{color:var(--tx2)}

/* ═══ ORIGEN ═══ */
.q-origen{border:1px solid var(--bd);border-left:3px solid var(--coral);border-radius:13px;
  padding:26px 30px;background:linear-gradient(102deg,var(--coral-bg),transparent 66%),var(--sf)}
.q-quote{font:400 20px/1.6 'Fraunces',Georgia,serif;color:var(--tx);font-style:italic;
  margin-bottom:14px}
.q-quote em{color:var(--coral-dp);font-style:italic}
.q-txt{font:400 14.5px/1.76 'Inter',sans-serif;color:var(--tx2)}
.q-txt b{color:var(--tx);font-weight:600}

/* ═══ NEGACIONES ═══ */
.q-nos{display:flex;flex-wrap:wrap;gap:9px;margin-bottom:19px}
.q-no{font:500 12.5px/1 'JetBrains Mono',monospace;color:var(--coral-dp);
  border:1px solid rgba(193,57,43,.26);border-radius:15px;padding:8px 16px;
  background:var(--coral-bg);white-space:nowrap}

/* ═══ CADENA ═══════════════════════════════════════════════════════════════
   Javo (2026-08-07): «los bloques deberían ser una sola línea de cadena, no dos
   niveles, para visualizar la trazabilidad».

   Se rehace como RIEL CONTINUO: los seis eslabones en una fila, unidos por un
   trazo que no se interrumpe. Así la línea ES la trazabilidad —se lee de un
   vistazo, sin leer las etiquetas— y su ROTURA es el problema del que habla la
   sección. Antes, con `flex-wrap`, la cadena caía en dos filas y el corte
   quedaba a mitad de la primera: la metáfora se perdía justo donde importaba.

   En pantalla estrecha el riel gira a vertical, que es la única forma de
   mantener seis eslabones legibles sin encogerlos hasta lo ilegible. */
/* Seis eslabones en un riel. La corrección de Javo (2026-08-07) era de
   proporción: al ensanchar el contenedor los nodos quedaron anchos y bajos, con
   texto de 8,5 px aplastado en la esquina y aire muerto alrededor. Ahora son
   TARJETAS DE PROCESO —altura propia, número de paso legible y tipografía que
   se lee sin acercarse—. */
.q-cad{display:flex;align-items:stretch;margin:28px 0 8px}
.q-link{flex:1 1 0;min-width:0;min-height:104px;border:1px solid var(--bd);
  border-radius:9px;padding:13px 14px;background:var(--sf);
  display:flex;flex-direction:column;gap:7px}
.q-link.on{border-color:rgba(78,102,116,.42);background:rgba(78,102,116,.08)}
/* El número del paso: ordena la lectura sin competir con el nombre. */
.q-num{font:700 10px/1 'JetBrains Mono',monospace;letter-spacing:.1em;
  color:var(--tx3);opacity:.75}
.q-link.on .q-num{color:var(--pizarra);opacity:1}
.q-link b{font:600 12.5px/1.32 'Inter',sans-serif;color:var(--tx2);
  letter-spacing:0;display:block}
.q-link.on b{color:var(--tx)}
.q-link small{display:block;font:400 10.5px/1.42 'Inter',sans-serif;
  color:var(--tx3);margin-top:auto}

/* Unión entre eslabones: un trazo continuo, no una flecha suelta. */
.q-join{flex:0 0 30px;position:relative;display:flex;align-items:center}
.q-join::before{content:"";position:absolute;left:0;right:0;height:2px;
  background:rgba(78,102,116,.42)}
.q-join::after{content:"›";position:absolute;left:50%;transform:translateX(-50%);
  color:var(--pizarra);font:700 15px/1 'Inter',sans-serif;
  background:var(--plano);padding:0 4px}

/* La rotura: el trazo se parte y el corte queda en el acento. */
.q-join.rota::before{background:linear-gradient(90deg,
  rgba(78,102,116,.42) 0 30%, transparent 30% 70%, var(--bd) 70% 100%)}
/* Coral PROFUNDO: el glifo es texto de 15 px y el pleno da 4,05:1 sobre el
   plano — no alcanza AA. El gate del sistema visual lo detectó. */
.q-join.rota::after{content:"✕";color:var(--coral-dp);font:700 16px/1 'Inter',sans-serif}

@media(max-width:900px){
  .q-cad{flex-wrap:wrap;gap:10px}
  .q-link{flex:1 1 calc(33.333% - 30px);min-height:96px}
  .q-join{flex:0 0 18px}
}
@media(max-width:620px){
  .q-cad{flex-direction:column}
  .q-link{flex:1 1 auto;min-height:0}
  .q-join{flex:0 0 24px;justify-content:center}
  .q-join::before{left:50%;right:auto;top:0;bottom:0;height:auto;width:2px}
  .q-join::after{content:"⌄"}
  .q-join.rota::before{background:linear-gradient(180deg,
    rgba(78,102,116,.42) 0 30%, transparent 30% 70%, var(--bd) 70% 100%)}
  .q-join.rota::after{content:"✕"}
}

/* ═══ FLUJO ═══ */
/* Los cuatro pasos del flujo tenían aspecto de cajas sueltas, sin dirección
   (Javo · 2026-08-07). Se numeran y se les añade un conector, para que se lea
   que uno lleva al siguiente y no que están puestos uno al lado del otro. */
.q-flow{display:flex;flex-wrap:wrap;gap:11px;margin:24px 0 6px;counter-reset:paso}
.q-node{flex:1 1 178px;border:1px solid var(--bd);border-top:2px solid var(--nc,var(--coral));
  border-radius:11px;padding:16px 18px;background:var(--sf);position:relative;
  counter-increment:paso}
.q-node:not(:last-child)::after{content:"›";position:absolute;right:-13px;top:50%;
  transform:translateY(-50%);color:var(--tx3);font:700 17px/1 'Inter',sans-serif;z-index:2}
.q-node-k{font:700 8.5px/1 'JetBrains Mono',monospace;letter-spacing:.13em;text-transform:uppercase;
  color:var(--nc,var(--coral));display:flex;align-items:center;gap:7px;margin-bottom:8px}
.q-node-k::before{content:counter(paso,decimal-leading-zero);
  font:700 9px/1 'JetBrains Mono',monospace;color:var(--tx3);
  border:1px solid var(--bd);border-radius:4px;padding:3px 5px;letter-spacing:.06em}
.q-node-t{font:700 14.5px/1.3 'Inter',sans-serif;color:var(--tx);margin-bottom:4px}
.q-node-d{font:400 12px/1.6 'Inter',sans-serif;color:var(--tx2)}
@media(max-width:900px){.q-node:not(:last-child)::after{display:none}}

/* ═══ PRODUCTOS ═══ */
/* También en hileras de tres: cinco tarjetas apiladas eran cinco pantallas de
   texto seguidas. En rejilla se comparan de un vistazo, que es justo lo que se
   quiere de una familia de productos. */
.q-prods{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:17px}
.q-prod{border:1px solid var(--bd);border-left:3px solid var(--pc,var(--coral));border-radius:11px;
  padding:18px 20px;background:var(--sf);transition:transform .25s,background .25s;
  display:flex;flex-direction:column}
.q-prod:hover{background:rgba(255,255,255,.85);transform:translateY(-2px)}
@media(max-width:1000px){.q-prods{grid-template-columns:1fr 1fr}}
.q-prod-h{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  flex-wrap:wrap;margin-bottom:3px}
.q-prod-n{font:600 19px/1.3 'Fraunces',Georgia,serif;color:var(--tx)}
/* Lo que está activo se distingue de lo que aún no existe: un sello lleno para
   la Fase 1 y uno atenuado para lo que todavía no se puede sostener. Antes
   compartían la misma intensidad y parecían igual de disponibles. */
.q-prod-e{font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.11em;
  color:var(--pc,var(--coral));white-space:nowrap;border:1px solid currentColor;
  border-radius:20px;padding:4px 11px;opacity:.55}
.q-prod-e.activo{background:var(--coral);border-color:var(--coral);
  color:#FFF;opacity:1}
.q-prod-r{font:500 11.5px/1 'Inter',sans-serif;color:var(--pc,var(--coral));margin-bottom:9px;opacity:.92}
.q-prod-d{font:400 13.8px/1.72 'Inter',sans-serif;color:var(--tx2)}
.q-prod-d b{color:var(--tx);font-weight:600}

/* ═══ MÉTODO ═══ */
.q-duo{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.q-duo-c{border:1px solid var(--bd);border-radius:11px;padding:18px 21px;background:var(--sf)}
.q-duo-t{font:700 13px/1.3 'Inter',sans-serif;margin-bottom:6px}
.q-duo-d{font:400 13px/1.68 'Inter',sans-serif;color:var(--tx2)}
/* ═══ DOMINIOS ═══ Hileras de tres (Javo · 2026-08-10, viendo la propuesta): doce
   en dos columnas eran seis filas de scroll; en tres son cuatro, y la retícula
   se lee como una tabla de contenidos en vez de como una lista larga. */
.q-doms{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:17px}
.q-dom{border:1px solid var(--bd);border-radius:10px;padding:14px 16px;background:var(--sf);
  display:flex;flex-direction:column;transition:background .22s,border-color .22s}
.q-dom:hover{background:rgba(255,255,255,.8);border-color:rgba(193,57,43,.24)}
.q-dom-n{font:700 9.5px/1 'JetBrains Mono',monospace;letter-spacing:.12em;color:var(--tx3)}
.q-dom-t{font:600 13.5px/1.32 'Inter',sans-serif;color:var(--tx);margin:6px 0 5px}
.q-dom-d{font:400 12.2px/1.58 'Inter',sans-serif;color:var(--tx2)}
@media(max-width:1000px){.q-doms{grid-template-columns:1fr 1fr}}

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
.q-linea-c.no .q-linea-k{color:var(--coral-dp)}
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

/* ═══ BARRA SUPERIOR ═══════════════════════════════════════════════════════
   Javo (2026-08-07): «la entrada al observatorio está hasta el final, no es
   cómodo bajar para ingresar». No solo no es atentatorio: obligar a recorrer
   toda la página para entrar castiga justamente a quien ya conoce el sitio y
   vuelve a diario.

   Se resuelve con las DOS cosas, que es el patrón habitual: un acceso discreto
   arriba para quien ya sabe a qué viene, y el formulario completo al final para
   quien llega por primera vez y necesita entender antes de que le pidan una
   contraseña. La portada sigue explicando; deja de obligar. */
/* FIXED, no sticky (Javo · 2026-08-10: «debe bajar todo»). Era sticky y aun asi
   se quedaba arriba: Streamlit envuelve cada bloque en contenedores propios, y
   basta que UNO tenga overflow para que `position:sticky` deje de pegar — no
   falla, simplemente no hace nada. Con `fixed` la barra sale del flujo y el
   botón, que ya era fixed, viaja alineado con ella en vez de solo. */
.q-top{position:fixed;top:0;left:0;right:0;z-index:55;background:rgba(217,224,229,.94);
  backdrop-filter:blur(11px);border-bottom:1px solid var(--bd)}
/* La barra ya no ocupa sitio: se lo devolvemos al contenido. */
[data-testid="stMainBlockContainer"],div.block-container{padding-top:52px !important}
.q-top-in{max-width:var(--ancho);margin:0 auto;padding:9px 34px;display:flex;
  align-items:center;gap:11px}
.q-top-n{font:600 13px/1 'Archivo',sans-serif;letter-spacing:.17em;color:var(--tx)}
.q-top-s{font:400 9px/1 'JetBrains Mono',monospace;letter-spacing:.13em;
  color:var(--tx3);margin-left:2px}
/* El botón de acceso VIAJA CON LA BARRA (Javo · 2026-08-10, comparando con la
   propuesta). `.q-top` ya era sticky, pero el botón nunca estuvo dentro de ella
   en el DOM: la barra la pinta `st.markdown` y el botón es un widget que va
   después, así que el selector `.q-top .st-key-top_acceso` no aplicaba nunca y
   el acceso se perdía al bajar. Se saca del flujo y se ancla al borde derecho
   del área de lectura, a la altura de la barra. */
/* Dentro del recuadro, no encima (Javo · 2026-08-10). Sobresalía por arriba y
   pesaba más que la marca: un acceso no puede gritar más fuerte que el nombre
   del proyecto. Se alinea al eje de la barra —39 px de alto: 9 + 21 del logo +
   9— y baja al cuerpo del subtítulo que acompaña al logotipo. */
.st-key-top_acceso{position:fixed;z-index:60;width:auto;
  top:8px;right:max(16px,calc((100vw - var(--ancho))/2 + 34px))}
.st-key-top_acceso button{background:var(--sf) !important;
  border:1px solid rgba(193,57,43,.38) !important;color:var(--coral-dp) !important;
  font:700 9px/1 'JetBrains Mono',monospace !important;letter-spacing:.13em !important;
  padding:6px 15px !important;border-radius:18px !important;min-height:0 !important;
  height:23px !important;box-shadow:0 1px 5px rgba(193,57,43,.07);
  transition:background .25s,color .25s,border-color .25s,transform .25s}
.st-key-top_acceso button::before{content:"";width:5px;height:5px;border-radius:50%;
  background:currentColor;margin-right:7px;flex:0 0 auto}
.st-key-top_acceso button:hover{background:var(--coral) !important;color:#FFF !important;
  border-color:var(--coral) !important;transform:translateY(-1px);
  box-shadow:0 4px 14px rgba(193,57,43,.25)}
@media(max-width:720px){.q-top-s{display:none}
  .st-key-top_acceso{top:6px;right:12px}
  .st-key-top_acceso button{font-size:9px !important;padding:8px 13px !important}}

div[data-testid="stForm"]{background:var(--sup) !important;
  border:1px solid rgba(193,57,43,.2) !important;border-radius:14px !important;
  padding:24px 28px 20px !important;backdrop-filter:blur(10px) !important}
.q-form-t{font:700 10.5px/1 'JetBrains Mono',monospace;color:var(--tx3);text-transform:uppercase;
  letter-spacing:.15em;text-align:center;margin-bottom:12px}
.q-badge{display:block;width:fit-content;margin:0 auto 18px;background:var(--coral-bg);
  border:1px solid rgba(193,57,43,.24);border-radius:18px;padding:6px 16px;
  font:500 10.5px/1 'JetBrains Mono',monospace;color:var(--coral-dp)}
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
  .q-prod-n{font-size:17px}
  .q-duo,.q-trust,.q-linea-g,.q-doms,.q-prods{grid-template-columns:1fr}
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
    """Una sección: la greca corre de lado a lado y el título va enhebrado.

    Idea de Javo (2026-08-07): cada encabezado es **un eslabón del collar**. La
    greca manteña recorre el ancho completo y el título queda ensartado en el
    centro, igual que la pieza labrada en el hilo. No es adorno — es la misma
    figura que da nombre al proyecto: unidades indivisibles unidas en una cadena
    cuya integridad depende de que ninguna falte.

    Sustituye dos elementos que se estorbaban: el separador suelto y un kicker
    con línea recta. Quedaban duplicados y ninguno conectaba nada.

    (La explicación vive aquí y no en el CSS porque los comentarios de la hoja
    de estilos SÍ viajan al navegador — y el gate de la portada cuenta cuántas
    veces aparece la palabra del origen en lo que se sirve.)"""
    return (f'<div class="q-sec">'
            f'<div class="q-kick"><span class="q-kick-t">{kick}</span></div>'
            f'<div class="q-h2">{h2}</div>{cuerpo}</div>')


def greca() -> str:
    """RETIRADA como separador suelto (Javo · 2026-08-07): «debe dejar una sola
    greca, no duplicados».

    El motivo manteño vive ahora en el encabezado de cada sección —donde el
    título va enhebrado y el trazo lo conecta—, que es donde comunica algo. Como
    banda independiente entre bloques solo repetía el dibujo sin unir nada, y
    aparecía dos veces seguidas junto al encabezado.

    Se conserva la función devolviendo vacío porque el controlador podría
    seguir invocándola: es preferible una llamada inocua a un error de import."""
    return ""


# ══════════════════════════ HERO ══════════════════════════
def landing_hero() -> str:
    return (
        f'<div class="q-hero">{_logo("coral", 88)}'
        f'<div class="q-name">QUIRA</div>'
        f'<div class="q-promesa">EVIDENCIA QUE TRANSFORMA</div>'
        f'<div class="q-cat">INTELIGENCIA PÚBLICA · DYLUS LAB · ECUADOR</div>'
        # Terminaba en «al servicio de gobiernos, ciudadanía, academia y cooperación
        # internacional». Son DESTINATARIOS, y enumerarlos aquí desplaza la
        # definición: lo primero que se lee deja de decir qué es QUIRA y pasa a
        # decir para quién. Se sustituye por lo que hace, y por la frase que cierra
        # la puerta al malentendido que Javo lleva meses corrigiendo.
        f'<div class="q-tag">Infraestructura de <b>conocimiento verificable</b> para la gestión '
        f'pública territorial. Integra evidencia institucional y ciudadana, la relaciona y la '
        f'contrasta para reconstruir cómo se enlazan el mandato, la planificación, el '
        f'presupuesto, la ejecución y el territorio.<br><br>'
        f'<b>QUIRA no administra el territorio. Lo hace observable.</b></div></div>')


# ══════════════════════════ ORIGEN ══════════════════════════
def origen() -> str:
    return _sec("El origen", "El estándar de valor territorial",
        '<div class="q-origen">'
        '<div class="q-quote">QUIRA toma su nombre de la raíz manteña de Cancebí asociada al '
        '<em>Spondylus princeps</em>: la estructura de intercambio y reserva de valor sobre la que '
        'se articulaban los acuerdos entre territorios.</div>'
        '<div class="q-txt">Para la cultura manteño-huancavilca, la pieza labrada de esa concha '
        '—la <i>chaquira</i>— no era ornamento: era la <b>unidad indivisible de valor</b>. Un '
        'collar de esas piezas constituía un <b>instrumento de autoridad y de compromiso entre '
        'comunidades</b>, y su integridad dependía de que ninguna faltara. De la concha entera '
        'toma su nombre este laboratorio: spon<b>·DYLUS</b>.<br><br>'
        'QUIRA traslada esa lógica al entorno digital. Cada documento público, cada registro de '
        'ejecución presupuestaria y cada aporte ciudadano constituye una <b>unidad de '
        'evidencia</b>; el sistema las enhebra en una <b>cadena verificable de integridad '
        'territorial</b>. Ningún dato aislado sostiene el control social, y la trazabilidad del '
        'Estado no existe sin la suma de todos.<br><br>'
        'El isotipo integra la <b>espiral cuadrada manteña</b>, geometría que el registro '
        'arqueológico asocia a quienes ejercían autoridad en la Ciudad de los Cerros. Su trazado '
        'continuo en ángulo recto representa el <b>recorrido auditable de la evidencia hasta su '
        'origen</b>; en el núcleo, el nodo central concentra la unidad indivisible de integridad '
        'del dato.</div></div>')


# ══════════════════════════ QUÉ ES ══════════════════════════
def que_es() -> str:
    nos = "".join(f'<span class="q-no">{t}</span>' for t in
                  # «no es solo un observatorio» salió con ADR-045: el producto
                  # ahora SE LLAMA Observatorio, y negarlo en la misma página
                  # dejaba al lector sin saber qué está entrando a usar.
                  ("no es un software municipal", "no es una auditoría",
                   "no es un ranking"))
    # La negación se queda, pero como FRONTERA, no como identidad. Reducir QUIRA a
    # una auditoría es el malentendido que Javo lleva meses corrigiendo y que
    # reaparece cada vez que la definición se deja implícita: si no se dice qué ES,
    # el lector completa el hueco con la categoría que ya conoce. Por eso ahora la
    # definición positiva va PRIMERO y la negación después.
    return _sec("Qué es", "Una infraestructura, no una herramienta de control",
        '<p class="q-p"><b>QUIRA es una infraestructura de conocimiento verificable para la '
        'gestión pública territorial.</b> Articula fuentes, evidencia, reglas normativas, un '
        'motor de cálculo y validación humana para convertir documentación dispersa en '
        'conocimiento sobre el territorio que cualquiera puede comprobar hasta su origen.</p>'
        f'<div class="q-nos">{nos}</div>'
        '<p class="q-p">La diferencia con una auditoría no es de alcance: es de pregunta. Una '
        'auditoría pregunta <i>¿cumplió?</i> y termina en un dictamen. QUIRA pregunta <b>¿qué '
        'puede demostrarse sobre lo que ocurrió?</b> y transforma esa evidencia en conocimiento '
        'verificable para que otros decidan. No mide trámites ni obras aisladas: recorre el <b>ciclo completo de la '
        'gestión pública</b> —del mandato electoral al impacto territorial— y muestra dónde se '
        'interrumpe la trazabilidad.</p>'
        # Declaración de objeto. Faltaba, y es lo que distingue una infraestructura
        # de observación de un software de control: decir a quién NO se dirige.
        '<p class="q-p">Su objeto no es auditar al ciudadano ni administrar al municipio. '
        '<b>Es hacer observable la gestión pública territorial</b> — que es el paso previo a '
        'cualquier decisión informada sobre ella, la tome quien la tome.</p>'
        '<p class="q-p">Cada afirmación se ancla a un documento — o a la ausencia '
        '<b>documentada</b> de uno. QUIRA <b>no sustituye a los órganos de control ni determina '
        'responsabilidades</b>: establece el <b>nivel de verificabilidad</b> de la evidencia '
        'disponible. Qué existe, qué puede comprobarse y qué permanece sin demostrar — insumo '
        'para el monitoreo, la evaluación y la toma de decisiones basada en evidencia.</p>')


# ══════════════════════════ PROBLEMA ══════════════════════════
# La cadena madre del canon es PROMESA·PLAN·PRESUPUESTO·EJECUCIÓN·RESULTADO·TERRITORIO
# (Constitución Ontológica). Aquí se presenta con el vocabulario de la administración
# pública —el que usan las secretarías de planificación, la banca de desarrollo y los
# órganos de control—, con el sistema del Estado que custodia cada eslabón. El canon NO
# cambia: cambia el registro, igual que se dice "participación ciudadana" en superficie y
# no el nombre interno del índice. (Javo · 2026-08-06.)
# LA CADENA MADRE — SEIS ESLABONES, y son los del canon.
#
# `CONSTITUCION_ONTOLOGICA_QUIRA.md §La cadena madre` la fija literalmente:
#
#     PROMESA → PLAN → PRESUPUESTO → EJECUCIÓN → RESULTADO → TERRITORIO
#      (CNE)   (PDOT)   (cédula)    (devengado)  (cobertura)  (GeoTwin)
#
# ⚠️ EL PRESUPUESTO NO SE LEE DEL eSIGEF (Javo · 2026-08-07, corrección de raíz
# aplicada también a la Constitución Ontológica). QUIRA **no tiene acceso** a
# ese sistema: es interno de las entidades públicas. El dato sale de la cédula
# presupuestaria publicada en el portal de transparencia, o de documentos
# obtenidos por solicitud de acceso a la información que la ciudadanía aporta.
# Publicar lo contrario describiría una capacidad que el proyecto no tiene.
#
# ⚠️ ERROR DE MÉTODO CORREGIDO (2026-08-07). El director la reconstruyó a partir
# de `plan_render.py`, que es el detalle operativo de UN dominio, y le salieron
# ocho eslabones inventando pasos que el canon no tiene. La cadena madre es
# TRANSVERSAL al ecosistema y vive en la Constitución Ontológica, no en d01.
# Antes de reconstruir algo, se busca en el canon transversal.
#
# LOS SISTEMAS NO SON ESLABONES. La Constitución es explícita: «cada eslabón
# vive en un sistema distinto del Estado, y QUIRA verifica que la integridad se
# sostenga AL CRUZARLOS» — todos ellos de ACCESO PÚBLICO.
# Poner Transparencia o SERCOP como pasos diría que el Estado hace transparencia
# después de contratar, cuando son los registros donde cada paso se comprueba —
# la misma separación de ADR-042: la cadena es el objeto observado, los silos la
# alimentan.
#
# POA Y PAC SON INSTRUMENTOS DENTRO DE SU ESLABÓN, no eslabones aparte: el POA
# es la bajada del plan plurianual a operación anual (vive en PLAN) y el PAC
# pertenece a EJECUCIÓN. Ahí se disuelve la discusión de orden que abrió el
# director — ambos viven en eslabones distintos y no compiten.
#
# Corrección de dato de Javo, esa sí de fondo: «PNBV» es de períodos anteriores.
# El vigente es el **Plan Nacional de Desarrollo** (CE Art. 280 · COOTAD
# Art. 215, ambos en el corpus con su huella).
_CADENA = [("Mandato electoral", "plan de trabajo inscrito · CNE"),
           ("Planificación territorial", "PDOT · POA · Plan Nacional de Desarrollo"),
           ("Asignación presupuestaria", "cédula presupuestaria publicada"),
           ("Contratación y ejecución", "PAC · SERCOP · devengado"),
           ("Bienes y servicios", "resultado entregado · rendición de cuentas"),
           ("Impacto territorial", "cobertura verificable en el territorio")]


def problema() -> str:
    # DÓNDE SE CORTA. Los sistemas del Estado documentan el ciclo hasta la
    # ejecución financiera: hay contratos, hay devengado, hay registro. Lo que
    # no queda recorrible es qué se entregó y a quién llegó — el hallazgo de
    # d01 §05: el instrumento declara el 100 % de QUÉ se hace, el 1,1 % de
    # DÓNDE y el 3,5 % de SOBRE QUIÉN.
    #
    # Por eso el corte va antes de «Bienes y servicios» y no antes: sostener que
    # la cadena se rompe en el presupuesto sería afirmar algo que la evidencia
    # no dice.
    _CORTE = 4
    nodos = ""
    for i, (t, s) in enumerate(_CADENA):
        if i:
            nodos += f'<span class="q-join{" rota" if i == _CORTE else ""}"></span>'
        nodos += (f'<span class="q-link{" on" if i < _CORTE else ""}">'
                  f'<span class="q-num">{i + 1:02d}</span>'
                  f'<b>{t}</b><small>{s}</small></span>')
    return _sec("El problema", "La información existe. La trazabilidad, no siempre",
        '<p class="q-p">Un compromiso inscrito ante la autoridad electoral puede no incorporarse '
        'al plan de desarrollo. La planificación puede no reflejarse en la asignación '
        'presupuestaria. El presupuesto puede ejecutarse sin que conste <b>dónde</b> ni '
        '<b>sobre qué población</b>. Cada eslabón del ciclo de la gestión pública vive en un '
        '<b>sistema distinto del Estado</b>, y ninguno fue diseñado para interoperar con los '
        'otros.</p>'
        f'<div class="q-cad">{nodos}</div>'
        '<p class="q-p">El problema rara vez es la ausencia de datos: es que <b>la cadena de '
        'valor público se interrumpe</b> en algún punto y nadie puede señalar dónde. QUIRA la '
        'reconstruye documento por documento y, cuando encuentra el corte, <b>lo nombra</b> — '
        'que es la condición para que el monitoreo y la evaluación dejen de depender de la '
        'declaración de la propia entidad.</p>')


# ══════════════════════════ EL MOTOR ══════════════════════════
def motor() -> str:
    """El diferenciador que faltaba (Javo · 2026-08-06): QUIRA calcula con un motor
    DETERMINISTA, no generativo. En 2026 todo proyecto dice «usamos IA»; poder decir que
    la cifra NO la produce la IA es lo que un evaluador de banca de desarrollo necesita
    oír, porque es lo que hace la métrica reproducible y auditable.

    Fundamento canónico: ADR-023 (arquitectura de tres niveles, inmutable) y Reglas 1 y 4
    — «si un número existe en el motor, ningún proceso lo recalcula fuera»."""
    # Coral PROFUNDO, no el pleno: este color pinta el título de la fila, y el
    # coral pleno sobre el plano da 4,05:1 — no alcanza AA para texto (gate
    # `check_sistema_visual.py`). El pleno queda para marca, greca y bordes.
    filas = [("La inteligencia artificial", "#8E2419",
              "Lee documentos, extrae, clasifica y <b>propone</b> correspondencias. Trabaja "
              "sobre volúmenes que ninguna persona podría revisar."),
             ("El motor de cálculo", "#18232B",
              "<b>No es un modelo de lenguaje.</b> Es un motor matemático determinista: mismas "
              "entradas, mismo resultado, siempre. Cada indicador tiene su fórmula explícita y "
              "su fuente declarada."),
             ("La validación humana", "#4E6674",
              "Contrasta cada propuesta automatizada contra la fuente documental y la acepta o "
              "la descarta. Ninguna cifra publicada existe sin ese paso.")]
    cards = "".join(
        f'<div class="q-duo-c" style="border-left:3px solid {c}">'
        f'<div class="q-duo-t" style="color:{c}">{t}</div><div class="q-duo-d">{d}</div></div>'
        for t, c, d in filas)
    return _sec("El cálculo", "La cifra no la produce la inteligencia artificial",
        '<p class="q-p">Conviene precisarlo, porque hoy casi todo sistema declara usar '
        'inteligencia artificial y eso ha vuelto la afirmación poco informativa. En QUIRA la IA '
        'cumple una función acotada —<b>leer, extraer y proponer</b>— y <b>ninguna cifra publicada '
        'proviene de ella</b>.</p>'
        f'<div class="q-duo" style="grid-template-columns:1fr">{cards}</div>'
        '<p class="q-p" style="margin-top:16px">De esa separación dependen dos propiedades que un '
        'modelo generativo no puede ofrecer. La primera es la <b>reproducibilidad</b>: un tercero '
        'con las mismas fuentes obtiene exactamente el mismo número. La segunda es la '
        '<b>auditabilidad</b>: cada resultado se rastrea hasta su fórmula y hasta el documento que '
        'lo sostiene. Un modelo de lenguaje puede responder distinto a la misma pregunta, y no '
        'deja forma de reconstruir cómo llegó a lo que dijo.</p>'
        '<p class="q-cap">Por eso el modelo de cálculo es <b>inspeccionable</b> y sus fórmulas '
        'permanecen estables: si una cifra cambia, es porque cambió la evidencia — nunca porque '
        'cambió el modelo. Es el requisito mínimo para que una medición sirva ante un órgano de '
        'control, una entidad de financiamiento o una revisión académica.</p>')


# ══════════════════════════ CÓMO FUNCIONA ══════════════════════════
def como_funciona() -> str:
    # ADR-045: eran dos «Entradas» —Observatorio y Ciudadana— y un «Núcleo» que
    # publicaba el nombre interno del Centro. Ahora son las TRES VÍAS DE
    # ADQUISICIÓN, que es lo que de verdad se distingue, y una sola superficie.
    n = [("var(--pizarra)", "Captura", "Sistemas públicos",
          "Revisa de forma progresiva los portales oficiales de los 222 municipios."),
         ("var(--pizarra)", "Solicitud", "Oficio de acceso",
          "Cuando el dato no está publicado, se pide por escrito y la entidad responde firmando."),
         ("var(--pizarra)", "Aporte", "Evidencia del territorio",
          "Actas, facturas y fotografías que la ciudadanía entrega y el sistema corrobora."),
         ("var(--coral)", "Proceso", "Contraste contra la norma",
          "Cada pieza se confronta con la ley y con las demás, y se reconstruye la cadena."),
         ("var(--tx)", "Superficie", "QUIRA Observatorio",
          "Donde la evidencia se vuelve conocimiento consultable. Único: todo converge aquí.")]
    nodos = "".join(
        f'<div class="q-node" style="--nc:{c}"><span class="q-node-k">{k}</span>'
        f'<div class="q-node-t">{t}</div><div class="q-node-d">{d}</div></div>'
        for c, k, t, d in n)
    return _sec("Cómo funciona", "Tres vías, un solo cuerpo de conocimiento",
        f'<div class="q-flow">{nodos}</div>'
        '<p class="q-p" style="margin-top:14px">Las tres vías no son intercambiables, y por eso '
        'se distinguen: la primera <b>encuentra</b> la evidencia que el Estado ya publicó; la '
        # «obliga a producirla» atribuía a QUIRA una potestad que no tiene: quien
        # obliga es la ley, no el sistema. QUIRA solicita, documenta y sigue el
        # plazo — y esa distinción importa más aquí que en cualquier otra frase.
        'segunda la <b>solicita y documenta su entrega</b> cuando falta; la tercera <b>recoge</b> lo que el '
        'territorio ya tiene en la mano. Cada pieza conserva el registro de por dónde entró, y '
        'todas alimentan el mismo cuerpo de conocimiento — no bases separadas que después se '
        'contradicen.</p>'
        # ADR-046 §1: el techo lo fija el documento, no la vía. Antes esta misma
        # frase decía que de la vía «depende cuánto puede afirmarse», que es
        # justamente el error que el ADR corrigió.
        '<p class="q-cap">Lo que determina cuánto puede afirmarse no es <i>quién trajo</i> el '
        'documento, sino <b>qué acredita el documento</b>. Un acto de la administración firmado '
        '—electrónicamente o de puño y sello— no deja de serlo porque lo entregue un vecino: '
        '<b>se verifica el certificado, no el portador</b>.</p>')


# ══════════════════════════ LOS 12 DOMINIOS ══════════════════════════
# Faltaban en la portada, y era el hueco más grande: la página explicaba cómo
# funciona QUIRA sin decir NUNCA qué mira. Alguien terminaba de leerla sin saber
# qué iba a encontrar adentro.
#
# Cada uno responde «qué inteligencia aporta», no «qué audita» — corrección de
# Javo (2026-08-10). La diferencia no es de estilo: la portada ya afirma que
# QUIRA «no sustituye a los órganos de control ni determina responsabilidades»,
# y anunciarse como auditor la contradiría en la misma página. Además invitaría
# justo la lectura que ADR-045 §6 recomienda no invitar frente al art. 79 LOPC.
_DOMINIOS = [
    ("01", "Planificación estratégica territorial",
     "Dónde una prioridad del plan deja de tener correspondencia con la programación, el "
     "presupuesto asignado y lo efectivamente ejecutado."),
    ("02", "Presupuesto y financiamiento",
     "Qué distancia hay entre lo codificado y lo devengado, y qué señales anticipan "
     "subejecución o desfinanciamiento de una meta."),
    ("03", "Gobernanza del mandato electoral",
     "Qué compromisos del plan inscrito ante el CNE sobreviven al ciclo administrativo y "
     "cuáles pierden rastro por el camino."),
    ("04", "Holding e integración municipal",
     "Cómo se comportan juntos el municipio y sus entidades adscritas: transferencias, "
     "dependencia y presión sobre el conjunto."),
    ("05", "Desarrollo económico territorial",
     "Dónde se localiza la inversión de fomento productivo y qué intervenciones generan "
     "continuidad económica en el territorio."),
    ("06", "Salud institucional",
     "Si el aparato administrativo puede sostener su operación en el tiempo, y qué "
     "condiciones comprometen esa continuidad."),
    ("07", "Transparencia activa",
     "Si lo publicado permite reconstruir el ciclo administrativo — que es distinto de "
     "haber cumplido formalmente con publicarlo."),
    ("08", "Participación ciudadana",
     "Qué separa la participación procedimental de la incidencia real sobre decisiones y "
     "presupuesto."),
    ("09", "Rendición de cuentas",
     "Qué queda en pie al contrastar lo declarado en el informe anual con los registros "
     "presupuestarios y de contratación."),
    ("10", "Servicios e infraestructura",
     "Dónde se concentra la inversión y dónde persiste el déficit de cobertura, leído "
     "sobre el territorio y no sobre el total."),
    ("11", "Inclusión, equidad y género",
     "Si las políticas dirigidas a grupos de atención prioritaria producen ejecución "
     "verificable o se quedan en el enunciado."),
    ("12", "Sostenibilidad y resiliencia",
     "Qué brecha hay entre la vulnerabilidad del territorio y la capacidad institucional "
     "de prevenir y responder."),
]


def dominios() -> str:
    cards = "".join(
        f'<div class="q-dom"><div class="q-dom-n">{n}</div>'
        f'<div class="q-dom-t">{t}</div><div class="q-dom-d">{d}</div></div>'
        for n, t, d in _DOMINIOS)
    # «Qué se observa» devolvía a QUIRA a la categoría observatorio/auditor. Los
    # dominios son mayores que eso: son la ESTRUCTURA con la que se organiza el
    # conocimiento del territorio, no una lista de cosas que se revisan.
    return _sec("La estructura", "Doce dominios de conocimiento territorial",
        '<p class="q-p">La gestión de un municipio no se lee en un indicador único. QUIRA la '
        'recorre por <b>doce dominios</b>, y en cada uno busca lo mismo: <b>dónde se interrumpe '
        'la correspondencia</b> entre lo que se prometió, lo que se planificó, lo que se '
        'presupuestó y lo que llegó al territorio.</p>'
        f'<div class="q-doms">{cards}</div>')


# ══════════════════════════ LA CAPA CIUDADANA ══════════════════════════
# ADR-046 §2: la capa cívica tiene nombre y lugar propios DENTRO del Observatorio.
# No es una puerta —eso ya se probó vacío— pero tampoco un renglón dentro de «cómo
# funciona»: es el propósito con el que nació el proyecto.
#
# El enganche es la precisión de Javo (§2.4): quien aporta no ayuda al sistema,
# ENCIENDE SU PROPIO TERRITORIO. Y §2.5 obliga a decir lo otro — que suplir al GAD
# no lo absuelve—, porque callarlo convertiría el trabajo ciudadano en un servicio
# gratuito al que incumple.
_CAPACIDADES = [
    ("Evidencia territorial",
     "Actas, informes, facturas, fotografías de obra. El sistema las estructura, registra su "
     "procedencia y explica qué acredita cada una."),
    ("Exigibilidad asistida",
     "Redacta la solicitud de acceso con su fundamento legal, lleva la cuenta del plazo y "
     "prepara el paso siguiente si la entidad no responde."),
    ("Inteligencia cívica",
     "Los doce dominios legibles sin jerga: qué dice cada cifra, de qué documento sale y qué "
     "norma la respalda."),
    ("Acción territorial",
     "Control social e incidencia con expediente. Es la capacidad que el proyecto reconoce y "
     "todavía no ha construido — y lo dice en vez de anunciarla."),
]


def ciudadana() -> str:
    cards = "".join(
        f'<div class="q-duo-c"><div class="q-duo-t" style="color:var(--coral-dp)">{t}</div>'
        f'<div class="q-duo-d">{d}</div></div>' for t, d in _CAPACIDADES)
    # Precisión de Javo (2026-08-10): «los dominios no se encienden solo con la
    # labor de la ciudadanía, también el Observatorio; ambas encienden con la
    # información que se va captando». El texto anterior podía leerse como si
    # encender fuera privilegio de la capa cívica. No lo es: enciende la EVIDENCIA,
    # venga por donde venga. Lo propio de esta vía es llegar donde la otra no.
    return _sec("La capa ciudadana", "Donde la publicación no llega, llega el territorio",
        '<p class="q-p">Un dominio se enciende cuando entra evidencia — <b>por cualquiera de las '
        'tres vías</b>. El Observatorio enciende todo lo que el Estado publica, y lo hace mes a '
        'mes sobre los 222 municipios. Pero <b>solo puede calcular sobre lo que existe</b>: donde '
        'un municipio no publica, esos dominios se quedan en blanco por más que se los revise.</p>'
        '<p class="q-p">Ahí empieza esta vía. Y de ahí sale la razón concreta por la que alguien '
        'aportaría evidencia de su cantón: <b>no es ayudar al sistema, es poder ver el propio '
        'territorio</b> cuando nadie más lo va a encender.</p>'
        f'<div class="q-duo">{cards}</div>'
        '<p class="q-cap">Y una regla que conviene decir en voz alta: <b>que la ciudadanía llene '
        'el hueco no absuelve al municipio de haberlo dejado</b>. La obligación de publicar es de '
        'la entidad, no de sus habitantes. El dominio se enciende; el incumplimiento queda '
        'registrado igual.</p>')


# ══════════════════════════ ECOSISTEMA ══════════════════════════
_PRODUCTOS = [
    # ADR-045: «QUIRA Ciudadana» era la segunda entrada de esta lista. Deja de
    # ser una puerta aparte —no lo era: detrás solo había un cartel de «próxi-
    # mamente»— y la participación ciudadana pasa a describirse donde de verdad
    # ocurre, dentro del Observatorio. La capacidad no se pierde; pierde el
    # portal propio, que es lo que nunca debió tener.
    ("QUIRA Observatorio",
     "Superficie pública · evidencia institucional y ciudadana · escala nacional",
     "Monitoreo progresivo de los <b>222 municipios</b> del país, incorporados según su "
     "disponibilidad documental y su ciclo administrativo. Agentes de inteligencia artificial "
     "revisan los sistemas nacionales de información —transparencia activa, contratación "
     "pública, rendición de cuentas, portales institucionales— y <b>toda captura se valida "
     # Decía «el oficio que obliga a entregarlo» — contradecía, en la misma
     # página, la corrección de `como_funciona`: quien obliga es la ley.
     "antes de publicarse</b>. Cuando un dato no está publicado, el sistema <b>prepara la "
     "solicitud de acceso</b> con su fundamento legal y lleva la cuenta del plazo. Y cuando la evidencia "
     "está en el territorio y no en un portal, la aportan quienes la tienen: personas, "
     "organizaciones comunitarias y academia suben actas, informes y fotografías de obra, y el "
     "sistema explica qué acredita cada documento y qué norma lo respalda. <b>No reemplaza al "
     "ciudadano: lo fortalece para incidir.</b>",
     "", "var(--coral)"),
    ("QUIRA Cooperación",
     "Multilaterales · banca de desarrollo · cooperación bilateral · academia",
     "Evidencia territorial verificada para <b>organismos multilaterales y banca de desarrollo</b> "
     "(CAF, BID, Banco Mundial, PNUD), <b>agencias de cooperación bilateral</b> (GIZ, AECID, JICA, "
     "KOICA), universidades, centros de investigación, fundaciones y organizaciones de la sociedad "
     "civil. Insumo para inversión basada en evidencia y para gestión por resultados. Llega después "
     "por una razón práctica: <b>su valor es la cobertura nacional</b>, y esa cobertura la "
     "construyen antes las dos entradas.",
     "", "var(--tx2)"),
    ("QUIRA Institucional",
     "Gobiernos locales · licencia independiente",
     "Herramientas para que el propio gobierno local <b>gestione lo suyo</b> con la evidencia ya "
     "publicada: ver dónde se corta su cadena documental y corregirlo. Licencia independiente, "
     "con soporte de Dylus Lab y bajo una regla explícita — <b>contratarla no modifica nada de lo "
     "que el Observatorio publica</b> sobre ese municipio.",
     "", "var(--tx2)"),
    ("QUIRA Impact",
     "Universidades · observatorios · centros de investigación",
     "El conocimiento abierto para que <b>terceros lo verifiquen</b>: conjuntos de datos, "
     "series históricas, metodología documentada y trazabilidad de cada afirmación hasta su "
     "fuente. No entrega interpretaciones ni recomendaciones —<b>el mérito y la "
     "responsabilidad de una investigación son de quien la firma</b>—; entrega las "
     "condiciones para producirla y para comprobarla. Es donde QUIRA demuestra, fuera de "
     "QUIRA, que lo que afirma resiste el escrutinio.",
     "", "var(--tx2)"),
    ("QUIRA Economic",
     "Inversión y desarrollo económico local",
     "Inteligencia económica del territorio sobre la misma base de evidencia verificada. "
     "Se mantiene declarada como <b>línea futura</b> y no como producto disponible: su "
     "modelo de operación todavía no está definido, y anunciar lo que aún no puede "
     "sostenerse sería prometer de más.",
     "", "var(--tx3)"),
]


def ecosistema() -> str:
    filas = "".join(
        f'<div class="q-prod" style="--pc:{col}">'
        f'<div class="q-prod-h"><span class="q-prod-n">{n}</span>'
        f'{f"<span class=\"q-prod-e activo\">{e}</span>" if e else ""}</div>'
        f'<div class="q-prod-r">{r}</div><div class="q-prod-d">{d}</div></div>'
        for n, r, d, e, col in _PRODUCTOS)
    # «Una superficie, varios destinatarios» dejaba a QUIRA a la altura del
    # Observatorio, como si fueran lo mismo. QUIRA es la infraestructura; el
    # Observatorio, la superficie pública donde se consulta.
    return _sec("El ecosistema", "Una infraestructura, distintas superficies de uso",
        '<p class="q-p">Se entra por un solo lugar. El <b>Observatorio</b> es la superficie '
        'pública donde la evidencia converge y se consulta; las demás leen esa misma '
        'infraestructura para responder preguntas distintas — una universidad no necesita lo '
        'mismo que un banco de desarrollo. Ninguna construye una verdad aparte: <b>hay un solo '
        'cuerpo de conocimiento</b>, y lo que cambia de una a otra es qué entregan y a quién.</p>'
        f'<div class="q-prods">{filas}</div>'
        '<p class="q-cap">Dos capacidades recorren el ecosistema entero sin constituir productos '
        'aparte: la inteligencia artificial, que explica en lenguaje natural lo que la evidencia '
        'sostiene y nunca produce las cifras, y la representación territorial, que sitúa cada '
        'hallazgo en el mapa del cantón.</p>')


# ══════════════════════════ MÉTODO ══════════════════════════
def humano() -> str:
    cols = [("var(--coral)", "La máquina encuentra",
             "Procesa volúmenes documentales que ninguna persona podría revisar, detecta patrones "
             "y señala dónde la evidencia falta o no concuerda entre sistemas."),
            ("var(--pizarra)", "Las personas deciden",
             "Interpretan el contexto normativo, conocen el territorio y validan cada hallazgo. "
             "Ninguna afirmación pública se publica sin ese paso.")]
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
        '<p class="q-p">Un informe que el propio municipio encarga y paga tiene poco peso ante un '
        'banco de desarrollo, una agencia de cooperación o una universidad, porque procede de la '
        'parte interesada. Un registro reconstruido desde fuentes públicas resiste esa pregunta. '
        'Y ahí está el punto que suele malinterpretarse: la independencia beneficia sobre todo al '
        'gobierno con buena gestión, que por primera vez cuenta con alguien capaz de demostrar su '
        'trazabilidad sin que la afirmación salga de él mismo.</p>'
        '<div class="q-linea"><div class="q-linea-t">Dónde está la línea</div>'
        '<div class="q-linea-g">'
        '<div class="q-linea-c no"><span class="q-linea-k">Nunca</span>'
        'Pagar por ser observado, por la evaluación o por lo que se publica. La observación no se '
        'contrata, no se negocia y no se retira.</div>'
        '<div class="q-linea-c si"><span class="q-linea-k">Sí, y con gusto</span>'
        'Licenciar herramientas para <b>gestionar lo propio</b> con la evidencia ya publicada, con '
        'soporte de Dylus Lab. Contratarlas <b>no cambia una sola línea</b> de lo que el '
        'Observatorio dice de ese municipio.</div></div></div>'
        '<p class="q-p">El principio rige en cualquier sistema de información pública: una '
        'evidencia sirve en la medida en que puede verificarse sin que la entidad observada '
        'intervenga en su producción, su evaluación o su publicación. Se trata de una condición '
        'técnica antes que de una postura.</p>'
        '<p class="q-p">Con un ejemplo cercano: ningún gobierno local financia al <b>INEC</b> '
        'para modificar una cifra censal, y sin embargo todos usan esa estadística para planificar '
        'y para sustentar sus proyectos ante quien los financia. <b>La estadística es independiente; '
        'las herramientas para trabajar con ella son otra cosa.</b> Separar ambas explícitamente es '
        'lo que permite ofrecer las dos sin que una contamine a la otra.</p>'
        '<p class="q-cap">De ahí que el lenguaje del sistema sea deliberadamente medido. Nunca '
        'afirma que alguien incumplió; dice qué puede comprobarse con los documentos disponibles '
        'y qué no. Y cuando aparece un corte en la cadena, lo que suele haber detrás es un '
        'instrumento de registro que nadie diseñó para dejar rastro — algo que se corrige con una '
        'decisión administrativa y rara vez con un proceso.</p>')


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


def barra_superior() -> str:
    """Cabecera fija con la marca. El botón de acceso lo pone el controlador,
    porque tiene que ser un componente real de Streamlit para poder navegar."""
    return ('<div class="q-top"><div class="q-top-in">'
            f'<span style="line-height:0">{_logo("coral", 21)}</span>'
            '<span class="q-top-n">QUIRA</span>'
            '<span class="q-top-s">INTELIGENCIA PÚBLICA</span>'
            '</div></div>')


def footer() -> str:
    """Pie institucional.

    Sale el sello técnico —«build v6-marfil · st 1.55.0»— por dos razones
    (Javo · 2026-08-07): no dice nada a un interlocutor institucional, y publica
    qué versión de qué componente corre en el servidor, que es información que
    no conviene ofrecer sin necesidad."""
    return (f'<div class="q-footer">{_logo("coral", 26)}<br>'
            f'<b>QUIRA</b> · Dylus Lab © 2026 · Ecuador<br>'
            f'Infraestructura de conocimiento verificable</div>')


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
