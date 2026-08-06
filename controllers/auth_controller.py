"""
QUIRA OS — Controller: Auth  (Sprint Landing v3 · 2026-05-27)
4 cajones iguales, clic directo = acción, sin botones redundantes.
Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st

from models.auth      import validate_any, AuthError, LockedError, is_locked
from utils.session    import set_user
from utils.audit_log  import log_login_ok, log_login_fail, log_lockout
from views.login_view import (CSS, landing_hero, que_es, como_funciona, ecosistema,
                              form_header, trust_badges, footer)


def _st_key(name: str) -> str:
    return f"_ql_{name}"


# Acceso al trabajo vivo. La etiqueta pública cambia —antes "QUIRA Institucional", que era
# justo el error que Javo señaló ("al observatorio entramos por institucional")—; el ruteo
# interno NO se toca: sigue entrando al ambiente `gov`. Es la distinción producto/ambiente
# de ADR-041 §2 aplicada: cambia lo que el mundo ve, no la maquinaria.
_LABEL_ACCESO = "🔭\n\nEntrar al Observatorio\n\nAcceso al Centro de Inteligencia Territorial\nDylus Lab · equipo autorizado"


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(landing_hero(), unsafe_allow_html=True)
    st.markdown(que_es(), unsafe_allow_html=True)
    st.markdown(como_funciona(), unsafe_allow_html=True)
    st.markdown(ecosistema(), unsafe_allow_html=True)

    _SEL = _st_key("platform_selected")
    if _SEL not in st.session_state:
        st.session_state[_SEL] = ""
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
            st.session_state[_SEL] = "institucional"
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FORMULARIO DE LOGIN (aparece bajo los cajones cuando INSTITUCIONAL activo)
    # ══════════════════════════════════════════════════════════════════════════
    if selected == "institucional":
        locked, secs_left = is_locked()
        _, col_form, _ = st.columns([1, 3, 1])
        with col_form:
            if locked:
                mins = secs_left // 60
                segs = secs_left % 60
                st.error(
                    f"🔒 Demasiados intentos. Espera **{mins}m {segs}s**."
                )
            else:
                submitted = False
                with st.form("login_form", border=False):
                    st.markdown(form_header(), unsafe_allow_html=True)
                    password  = st.text_input(
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
                        st.rerun()
                    except LockedError as e:
                        log_lockout("unknown")
                        st.error(f"🔒 Bloqueado. Espera {e.seconds_left // 60}m.")
                    except AuthError as e:
                        log_login_fail("unknown", motivo=str(e))
                        st.warning(str(e))

    # ══════════════════════════════════════════════════════════════════════════
    # CONTACTO — vía abierta para quien quiera sumarse antes de la Fase 2
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown(
        '<div style="max-width:820px;margin:14px auto 0;padding:13px 18px;text-align:center;'
        'border:1px solid rgba(124,92,252,.14);border-radius:10px;'
        'background:rgba(124,92,252,.045);font-family:Inter,sans-serif">'
        '<div style="font:400 10.5px/1.6 Inter,sans-serif;color:#8892B0">'
        'Universidades, organismos bilaterales, ONG y equipos de investigación: '
        'la evidencia territorial verificada se abre en la Fase 2. Para conversar antes — '
        '<span style="font:600 10.5px/1 \'JetBrains Mono\',monospace;color:#9B79FF;'
        'letter-spacing:.03em">acceso@quira.ec</span></div></div>',
        unsafe_allow_html=True,
    )

    # ── Trust badges + footer ─────────────────────────────────────────────────
    st.markdown(trust_badges(), unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)

    # ── Acceso operacional ghost (equipo Dylus Lab) ───────────────────────────
    st.markdown(
        '<div style="text-align:center;padding:2px 0 4px;'
        "font:400 8px/1 'JetBrains Mono',monospace;"
        'color:rgba(136,146,176,.08);letter-spacing:.1em">· · ·</div>',
        unsafe_allow_html=True,
    )
    _, col_ops, _ = st.columns([4, 1, 4])
    with col_ops:
        if st.button(
            "⚙ acceso operacional",
            key="btn_ops_access",
            use_container_width=True,
            help="Acceso exclusivo Dylus Lab",
        ):
            st.session_state[_SEL] = "institucional"
            st.rerun()
