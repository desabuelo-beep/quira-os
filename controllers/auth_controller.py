"""
QUIRA OS — Controller: Auth (Seguridad v2 · Landing v1)
Landing pública con 3 plataformas + formulario de acceso institucional.
Orquesta View + Model. Muestra errores de rate limiting y sesión.
Dylus Lab © 2026
"""
import streamlit as st
from config import GAD_NOMBRE, CORTE
from models.auth import validate, rol_options, AuthError, LockedError, is_locked
from utils.session import set_user
from utils.audit_log import log_login_ok, log_login_fail, log_lockout
from views.login_view import (
    CSS, landing_hero, platform_cards, form_header,
    trust_badges, footer,
)


def _st_key(name: str) -> str:
    """Genera key único para session_state de auth flow."""
    return f"_ql_{name}"


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)

    # ── Hero: logo + marca ────────────────────────────────────────────────────
    st.markdown(landing_hero(), unsafe_allow_html=True)

    # ── Estado del flow: qué plataforma seleccionó el usuario ────────────────
    _SEL = _st_key("platform_selected")
    if _SEL not in st.session_state:
        st.session_state[_SEL] = ""   # '' | 'institucional' | 'ciudadano'

    selected = st.session_state[_SEL]

    # ── Cajas de plataforma ───────────────────────────────────────────────────
    st.markdown(platform_cards(selected=selected), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Acceder →", key="btn_institucional",
                     use_container_width=True, type="primary"):
            st.session_state[_SEL] = "institucional"
            st.rerun()

    with col2:
        if st.button("Explorar →", key="btn_ciudadano",
                     use_container_width=True):
            # Ciudadano: marcamos como seleccionado pero no requiere auth.
            # app.py deberá detectar este estado y redirigir a Civic.
            st.session_state[_SEL] = "ciudadano"
            st.session_state["civic_direct"] = True
            st.rerun()

    with col3:
        st.button("Próximamente", key="btn_cooperacion",
                  use_container_width=True, disabled=True)

    # ── Si seleccionó INSTITUCIONAL: mostrar formulario de login ─────────────
    if selected == "institucional":
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Verificar bloqueo por rate limiting
        locked, secs_left = is_locked()
        if locked:
            mins = secs_left // 60
            segs = secs_left % 60
            st.error(
                f"🔒 Demasiados intentos fallidos. "
                f"Espera **{mins}m {segs}s** antes de volver a intentarlo."
            )
        else:
            _, col_form, _ = st.columns([1, 2, 1])
            with col_form:
                opts = rol_options()
                with st.form("login_form", border=False):
                    st.markdown(form_header(CORTE), unsafe_allow_html=True)
                    rol_display = st.selectbox("ROL DE ACCESO", list(opts.keys()))
                    password    = st.text_input(
                        "CONTRASEÑA", type="password", placeholder="••••••••"
                    )
                    submitted = st.form_submit_button(
                        "ACCEDER →", use_container_width=True, type="primary"
                    )

            if submitted:
                rol_key = opts[rol_display]
                try:
                    user = validate(rol_key=rol_key, password=password)
                    log_login_ok(rol_key)
                    set_user(usuario=user.key, rol=user.rol, emoji=user.emoji)
                    st.session_state[_SEL] = ""  # limpiar estado de landing
                    st.rerun()
                except LockedError as e:
                    log_lockout(rol_key)
                    st.error(f"🔒 Cuenta bloqueada temporalmente. Espera {e.seconds_left // 60}m.")
                except AuthError as e:
                    log_login_fail(rol_key, motivo=str(e))
                    st.warning(str(e))

    # ── Trust badges + footer ─────────────────────────────────────────────────
    st.markdown(trust_badges(), unsafe_allow_html=True)
    st.markdown(footer(GAD_NOMBRE, CORTE), unsafe_allow_html=True)
