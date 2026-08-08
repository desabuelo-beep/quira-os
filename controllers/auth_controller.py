"""
QUIRA OS — Controller: Acceso  ·  landing v7 "Papel de plano"  ·  2026-08-06
La portada EXPLICA (origen · qué es · problema · cómo · ecosistema · método ·
independencia) y luego deja entrar por una sola puerta: el Observatorio.
Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st

from models.auth      import validate_any, AuthError, LockedError, is_locked
from utils.session    import set_user
from utils.audit_log  import log_login_ok, log_login_fail, log_lockout
from views.login_view import (CSS, landing_hero, origen, que_es, problema, como_funciona,
                              motor, ecosistema, humano, independencia, greca,
                              form_header, trust_badges, footer, barra_superior)


def _st_key(name: str) -> str:
    return f"_ql_{name}"


# Acceso al trabajo vivo. La etiqueta pública cambia —antes "QUIRA Institucional", que era
# justo el error que Javo señaló ("al observatorio entramos por institucional")—; el ruteo
# interno NO se toca: sigue entrando al ambiente `gov`. Es la distinción producto/ambiente
# de ADR-041 §2 aplicada: cambia lo que el mundo ve, no la maquinaria.
# Decía «Entrar al Observatorio · Centro de Inteligencia Territorial» — los dos
# nombres en una sola cadena, que es el síntoma que destapó ADR-045: cuando hace
# falta un segundo nombre para decir una cosa, sobra uno de los dos.
_LABEL_ACCESO = "Entrar al Observatorio\n\nAcceso con credenciales · equipo Dylus Lab"


def _formulario_acceso(_SEL: str) -> None:
    """Formulario de acceso al Observatorio.

    Vive en una función porque se dibuja en DOS sitios según cómo llegó el
    usuario: al pie para quien recorrió la página, y arriba para quien usó el
    atajo de la barra (ver el comentario del bug en `run`). Nunca en ambos a la
    vez — comparten `key` y Streamlit levantaría DuplicateWidgetID."""
    locked, secs_left = is_locked()
    _, col_form, _ = st.columns([1, 3, 1])
    with col_form:
        if locked:
            mins = secs_left // 60
            segs = secs_left % 60
            st.error(f"🔒 Demasiados intentos. Espera **{mins}m {segs}s**.")
            return
        submitted = False
        with st.form("login_form", border=False):
            st.markdown(form_header(), unsafe_allow_html=True)
            password = st.text_input(
                "CONTRASEÑA", type="password", placeholder="••••••••"
            )
            submitted = st.form_submit_button(
                "ACCEDER →", use_container_width=True, type="primary"
            )
        if submitted:
            try:
                user = validate_any(password=password)
                log_login_ok(user.key)
                set_user(usuario=user.key, rol=user.rol, emoji=user.emoji)
                st.session_state[_SEL] = ""
                st.session_state.pop(_st_key("acceso_arriba"), None)
                st.rerun()
            except LockedError as e:
                log_lockout("unknown")
                st.error(f"🔒 Bloqueado. Espera {e.seconds_left // 60}m.")
            except AuthError as e:
                log_login_fail("unknown", motivo=str(e))
                st.warning(str(e))


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)

    _SEL = _st_key("platform_selected")
    if _SEL not in st.session_state:
        st.session_state[_SEL] = ""
    _ARRIBA = _st_key("acceso_arriba")

    # ── Barra superior con acceso ─────────────────────────────────────────────
    # El formulario sigue al final —quien llega por primera vez merece entender
    # antes de que le pidan una contraseña—, pero obligar a recorrer la página
    # entera castigaba a quien ya conoce el sitio y vuelve a diario (Javo ·
    # 2026-08-07).
    #
    # BUG (Javo · 2026-08-08): «el acceso superior no abre nada». Sí abría — el
    # botón fijaba el estado y recargaba—, pero el formulario aparecía seis
    # pantallas más abajo y al recargar uno queda arriba: se abría sin que se
    # viera. El comentario anterior decía que el atajo «lo desplaza a la vista»
    # y no había nada que lo desplazara; describía la intención, no el hecho.
    # Streamlit no ejecuta <script> en markdown, así que no hay scroll que
    # inyectar: en vez de llevar al usuario al formulario, se trae el formulario
    # a donde el usuario está mirando.
    st.markdown(barra_superior(), unsafe_allow_html=True)
    _, col_top = st.columns([5, 1.15])
    with col_top:
        if st.button("Acceder →", key="top_acceso", use_container_width=True,
                     help="Entrar al Observatorio · equipo Dylus Lab"):
            st.session_state[_SEL] = "observatorio"
            st.session_state[_ARRIBA] = True
            st.rerun()

    if st.session_state.get(_ARRIBA) and st.session_state[_SEL] == "observatorio":
        _formulario_acceso(_SEL)
    # Orden narrativo: quién soy → de dónde vengo → qué hago → qué problema resuelvo →
    # cómo → con qué productos → con qué método → y la aclaración que evita el malentendido.
    # Greca manteña entre bloques: el sistema gráfico secundario. La pirámide
    # escalonada —"la idea de montaña o cerro"— entra aquí, no en el logotipo.
    # `motor` va justo tras `como_funciona`: primero se ve el flujo, después se
    # aclara QUIÉN calcula — que es lo que sostiene la reproducibilidad del dato.
    # El separador de greca suelto SE RETIRA (Javo · 2026-08-07): la greca pasó
    # al encabezado de cada sección, donde el título va enhebrado como una
    # chaquira en el hilo. Mantener las dos duplicaba el motivo y dejaba dos
    # grecas seguidas sin nada entre ellas.
    for bloque in (landing_hero, origen, que_es, problema, como_funciona,
                   motor, ecosistema, humano, independencia):
        st.markdown(bloque(), unsafe_allow_html=True)

    selected = st.session_state[_SEL]

    # ══════════════════════════════════════════════════════════════════════════
    # ACCESO — un solo punto de entrada real
    #
    # Antes había cuatro tarjetas-botón, una de ellas "QUIRA Operations", que
    # NOMENCLATURA_CANONICA prohíbe expresamente publicar: "OPS no es una plataforma
    # pública. No aparece como tarjeta en la landing". Operaciones es mantenimiento del
    # ecosistema, no producto (Javo · ADR-041 §2) — sale de la portada; su acceso sigue
    # siendo el enlace discreto del pie, que no es una tarjeta.
    #
    # Los productos ahora se EXPLICAN en el ecosistema (arriba) en vez de fingir cuatro
    # accesos donde solo uno existe. Cooperación mantiene su vía de contacto abajo.
    # ══════════════════════════════════════════════════════════════════════════
    _, col_acc, _ = st.columns([1, 2, 1])
    with col_acc:
        if st.button(_LABEL_ACCESO, key="card_acceso", use_container_width=True):
            st.session_state[_SEL] = "observatorio"
            # Simétrico al atajo de arriba: el formulario aparece donde se pulsó.
            # Sin esto, quien primero usó la barra y luego bajó hasta aquí no
            # veía nada — el formulario seguía anclado arriba, fuera de vista.
            st.session_state.pop(_ARRIBA, None)
            st.rerun()

    # El formulario del pie solo si NO se dibujó ya arriba: dos formularios en la
    # misma página comparten `key` y Streamlit levanta DuplicateWidgetID.
    if selected == "observatorio" and not st.session_state.get(_ARRIBA):
        _formulario_acceso(_SEL)

    # ══════════════════════════════════════════════════════════════════════════
    # CONTACTO — vía abierta para quien quiera sumarse antes de la Fase 2
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div style="max-width:900px;margin:26px auto 0;padding:18px 24px;text-align:center;'
        'border:1px solid rgba(78,102,116,.26);border-radius:12px;'
        'background:rgba(78,102,116,.07);font-family:Inter,sans-serif">'
        '<div style="font:400 13.5px/1.7 Inter,sans-serif;color:#52616B">'
        # Diferenciado por tipo de actor (Javo · 2026-08-06): "organismos bilaterales" metía
        # en un mismo saco a la banca de desarrollo, las agencias de cooperación y la
        # academia, que son interlocutores distintos con mandatos distintos.
        '<b style="color:#18232B">Organismos multilaterales y banca de desarrollo · agencias de '
        'cooperación bilateral · universidades y centros de investigación · fundaciones y '
        'organizaciones de la sociedad civil:</b> la evidencia territorial verificada se abre '
        'en la Fase 2. Para conversar antes — '
        # Correo real de Javo (2026-08-05); "acceso@quira.ec" no existía y una dirección
        # que rebota en una landing institucional cuesta más que no poner ninguna.
        # NO se publica su teléfono: un número personal en una página pública queda
        # expuesto a rastreo automatizado y no se puede retirar de donde ya se copió.
        # El correo basta para abrir conversación; el teléfono se comparte en privado.
        '<a href="mailto:javodesantana@gmail.com" '
        'style="font:600 11.5px/1 \'JetBrains Mono\',monospace;color:#4E6674;'
        'letter-spacing:.03em;text-decoration:none">javodesantana@gmail.com</a>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    # ── Trust badges + footer ─────────────────────────────────────────────────
    st.markdown(trust_badges(), unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)

    # ── Acceso operacional ghost (equipo Dylus Lab) ───────────────────────────
    st.markdown(
        '<div style="text-align:center;padding:2px 0 4px;'
        "font:400 8px/1 'JetBrains Mono',monospace;"
        'color:rgba(24,35,43,.16);letter-spacing:.1em">· · ·</div>',
        unsafe_allow_html=True,
    )
    _, col_ops, _ = st.columns([4, 1, 4])
    with col_ops:
        if st.button(
            "⚙ mantenimiento del ecosistema",
            key="btn_ops_access",
            use_container_width=True,
            help="Mantenimiento del ecosistema — uso interno Dylus Lab. No es un producto.",
        ):
            st.session_state[_SEL] = "observatorio"
            st.rerun()
