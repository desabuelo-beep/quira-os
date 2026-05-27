"""
QUIRA OS — Controller: Auth (Seguridad v2 · Landing v1)
Landing pública con 3 plataformas + formulario de acceso institucional.
Orquesta View + Model. Muestra errores de rate limiting y sesión.
Dylus Lab © 2026
"""
import streamlit as st
from models.auth import validate_any, AuthError, LockedError, is_locked
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
        st.session_state[_SEL] = ""   # '' | 'institucional' | 'ciudadano' | 'cooperacion'

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
        if st.button("Solicitar acceso", key="btn_cooperacion",
                     use_container_width=True):
            st.session_state[_SEL] = "cooperacion"
            st.rerun()

    # ── Si seleccionó COOPERACIÓN: mostrar contacto ───────────────────────────
    if selected == "cooperacion":
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        _, col_coop, _ = st.columns([1, 2, 1])
        with col_coop:
            st.markdown("""
<div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.18);
            border-radius:12px;padding:20px 24px;text-align:center;
            font-family:Inter,sans-serif;margin-bottom:4px">
  <div style="font-size:22px;margin-bottom:10px">📑</div>
  <div style="font:700 13px/1.2 Inter,sans-serif;color:#E2E8F0;margin-bottom:8px">
    Acceso para cooperación e investigación</div>
  <div style="font:400 11px/1.6 Inter,sans-serif;color:#8892B0;margin-bottom:14px">
    Disponible para academia, ONGs y organismos<br>de cooperación internacional.
    Datos longitudinales verificados.</div>
  <div style="font:600 11px/1 'JetBrains Mono',monospace;
              color:#9B79FF;letter-spacing:.04em">acceso@quira.ec</div>
</div>""", unsafe_allow_html=True)

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
                    st.session_state[_SEL] = ""  # limpiar estado de landing
                    st.rerun()
                except LockedError as e:
                    log_lockout("unknown")
                    st.error(f"🔒 Cuenta bloqueada temporalmente. Espera {e.seconds_left // 60}m.")
                except AuthError as e:
                    log_login_fail("unknown", motivo=str(e))
                    st.warning(str(e))

    # ── Trust badges + footer ─────────────────────────────────────────────────
    st.markdown(trust_badges(), unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)

    # ── Acceso operacional (link discreto — solo equipo Dylus Lab) ─────────────
    st.markdown(
        '<div style="text-align:center;padding:4px 0 6px;'
        "font:400 9px/1 'JetBrains Mono',monospace;"
        'color:rgba(136,146,176,.12);letter-spacing:.1em">· · ·</div>',
        unsafe_allow_html=True,
    )
    _, col_ops, _ = st.columns([4, 1, 4])
    with col_ops:
        if st.button(
            "⚙ acceso operacional",
            key="btn_ops_access",
            use_container_width=True,
            type="secondary",
            help="Acceso exclusivo Dylus Lab — Equipo operativo",
        ):
            st.session_state[_SEL] = "institucional"
            st.rerun()
