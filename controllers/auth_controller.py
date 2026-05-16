"""
QUIRA OS — Controller: Auth (Seguridad v2)
Orquesta View + Model. Muestra errores de rate limiting y sesión.
Dylus Lab © 2026
"""
import streamlit as st
from config import GAD_NOMBRE, CORTE
from models.auth import validate, rol_options, AuthError, LockedError, is_locked
from utils.session import set_user
from utils.audit_log import log_login_ok, log_login_fail, log_lockout
from views.login_view import CSS, splash_top, splash_bottom


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(splash_top(CORTE), unsafe_allow_html=True)

    _, col, _ = st.columns([0.05, 1, 0.05])
    with col:
        # Mostrar estado de bloqueo ANTES del formulario
        locked, secs_left = is_locked()
        if locked:
            mins = secs_left // 60
            segs = secs_left % 60
            st.error(
                f"🔒 Demasiados intentos fallidos. "
                f"Espera **{mins}m {segs}s** antes de volver a intentarlo."
            )
            st.markdown(splash_bottom(GAD_NOMBRE, CORTE), unsafe_allow_html=True)
            return  # No mostrar el formulario mientras esté bloqueado

        opts = rol_options()
        with st.form("login_form", border=False):
            rol_display = st.selectbox("ROL DE ACCESO", list(opts.keys()))
            password    = st.text_input("CONTRASEÑA", type="password", placeholder="••••••••")
            submitted   = st.form_submit_button("ACCEDER →", use_container_width=True)

    if submitted:
        rol_key = opts[rol_display]
        try:
            user = validate(rol_key=rol_key, password=password)
            log_login_ok(rol_key)
            set_user(usuario=user.key, rol=user.rol, emoji=user.emoji)
            st.rerun()
        except LockedError as e:
            log_lockout(rol_key)
            st.error(f"🔒 Cuenta bloqueada temporalmente. Espera {e.seconds_left // 60}m.")
        except AuthError as e:
            log_login_fail(rol_key, motivo=str(e))
            st.warning(str(e))

    st.markdown(splash_bottom(GAD_NOMBRE, CORTE), unsafe_allow_html=True)
