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
from views.login_view import CSS, landing_hero, form_header, trust_badges, footer


def _st_key(name: str) -> str:
    return f"_ql_{name}"


# Labels de los 4 cajones — pre-line rendering en el button
_LABEL_INST = "🏛\n\nQUIRA Institucional\n\nCentro de comando institucional\npara Alcaldía y Holding Municipal."
_LABEL_CIV  = "🌎\n\nQUIRA Ciudadano\n\nTransparencia territorial y\nseguimiento ciudadano."
_LABEL_COOP = "📑\n\nQUIRA Cooperación\n\nEvidencia territorial para\ninvestigación y cooperación."
_LABEL_OPS  = "⚡\n\nQUIRA Operations\n\nMonitoreo institucional en\ntiempo real — En construcción."


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(landing_hero(), unsafe_allow_html=True)

    _SEL = _st_key("platform_selected")
    if _SEL not in st.session_state:
        st.session_state[_SEL] = ""
    selected = st.session_state[_SEL]

    # ══════════════════════════════════════════════════════════════════════════
    # 4 CAJONES IGUALES — clic = acción directa
    # ══════════════════════════════════════════════════════════════════════════
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button(_LABEL_INST, key="card_inst", use_container_width=True):
            st.session_state[_SEL] = "institucional"
            st.rerun()

    with c2:
        if st.button(_LABEL_CIV, key="card_civ", use_container_width=True):
            st.session_state[_SEL] = "ciudadano"
            st.session_state["civic_direct"] = True
            st.rerun()

    with c3:
        if st.button(_LABEL_COOP, key="card_coop", use_container_width=True):
            st.session_state[_SEL] = "cooperacion"
            st.rerun()

    with c4:
        # Operations: sin acción — cajón visual, en construcción
        st.button(_LABEL_OPS, key="card_ops", use_container_width=True, disabled=True)

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
    # COOPERACIÓN: datos de contacto
    # ══════════════════════════════════════════════════════════════════════════
    if selected == "cooperacion":
        _, col_coop, _ = st.columns([1, 2, 1])
        with col_coop:
            st.markdown(
                '<div style="background:rgba(124,92,252,.06);'
                'border:1px solid rgba(124,92,252,.15);'
                'border-radius:12px;padding:18px 22px;text-align:center;'
                'font-family:Inter,sans-serif;margin-top:8px">'
                '<div style="font-size:20px;margin-bottom:8px">📑</div>'
                '<div style="font:700 12px/1.2 Inter,sans-serif;color:#E2E8F0;margin-bottom:6px">'
                'Acceso para cooperación e investigación</div>'
                '<div style="font:400 10px/1.6 Inter,sans-serif;color:#8892B0;margin-bottom:12px">'
                'Academia, ONGs y organismos de cooperación internacional. '
                'Datos longitudinales verificados.</div>'
                '<div style="font:600 11px/1 JetBrains Mono,monospace;color:#9B79FF;letter-spacing:.04em">'
                'acceso@quira.ec</div>'
                '</div>',
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
