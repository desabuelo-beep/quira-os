"""
QUIRA OS — Controller: Auth  (Sprint Landing v2 · 2026-05-27)
Landing pública con 4 plataformas + formulario de acceso institucional.

Layout v2:
  · QUIRA Institucional — card dominante (primer plano visual)
  · QUIRA Ciudadano / Cooperación / Operations — grid secundario
  · Sin botones flotantes redundantes: cada card tiene su propio CTA integrado
  · Login form aparece en la zona dominante al activar Institucional

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st

from models.auth      import validate_any, AuthError, LockedError, is_locked
from utils.session    import set_user
from utils.audit_log  import log_login_ok, log_login_fail, log_lockout
from views.login_view import (
    CSS,
    landing_hero,
    card_institucional_html,
    card_ciudadano_html,
    card_cooperacion_html,
    card_operations_html,
    form_header,
    trust_badges,
    footer,
)


def _st_key(name: str) -> str:
    return f"_ql_{name}"


def run() -> None:
    st.markdown(CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(landing_hero(), unsafe_allow_html=True)

    # ── Estado del flow ───────────────────────────────────────────────────────
    _SEL = _st_key("platform_selected")
    if _SEL not in st.session_state:
        st.session_state[_SEL] = ""
    selected = st.session_state[_SEL]

    # ══════════════════════════════════════════════════════════════════════════
    # QUIRA INSTITUCIONAL — card dominante
    # Ocupa una columna central amplia; el CTA es parte de la card.
    # ══════════════════════════════════════════════════════════════════════════
    _, col_inst, _ = st.columns([1, 5, 1])
    with col_inst:
        st.markdown(
            card_institucional_html(active=(selected == "institucional")),
            unsafe_allow_html=True,
        )
        if st.button(
            "⬡  ENTRAR AL SISTEMA",
            key="btn_institucional",
            use_container_width=True,
            type="primary",
        ):
            st.session_state[_SEL] = "institucional"
            st.rerun()

    # ── Login form ────────────────────────────────────────────────────────────
    if selected == "institucional":
        locked, secs_left = is_locked()
        _, col_form, _ = st.columns([1, 5, 1])
        with col_form:
            if locked:
                mins = secs_left // 60
                segs = secs_left % 60
                st.error(
                    f"🔒 Demasiados intentos fallidos. "
                    f"Espera **{mins}m {segs}s** antes de volver a intentarlo."
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
                        st.error(
                            f"🔒 Cuenta bloqueada temporalmente. "
                            f"Espera {e.seconds_left // 60}m."
                        )
                    except AuthError as e:
                        log_login_fail("unknown", motivo=str(e))
                        st.warning(str(e))

    # ── Divisor visual ────────────────────────────────────────────────────────
    st.markdown(
        '<div style="max-width:900px;margin:10px auto 6px;'
        'border-top:1px solid rgba(255,255,255,.04)"></div>',
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════════
    # GRID SECUNDARIO — 3 módulos en fila
    # ══════════════════════════════════════════════════════════════════════════
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            card_ciudadano_html(active=(selected == "ciudadano")),
            unsafe_allow_html=True,
        )
        if st.button(
            "Explorar Transparencia →",
            key="btn_ciudadano",
            use_container_width=True,
        ):
            st.session_state[_SEL] = "ciudadano"
            st.session_state["civic_direct"] = True
            st.rerun()

    with c2:
        st.markdown(
            card_cooperacion_html(active=(selected == "cooperacion")),
            unsafe_allow_html=True,
        )
        if st.button(
            "Solicitar Acceso Institucional",
            key="btn_cooperacion",
            use_container_width=True,
        ):
            st.session_state[_SEL] = "cooperacion"
            st.rerun()

    with c3:
        st.markdown(card_operations_html(), unsafe_allow_html=True)
        st.button(
            "⚡  En construcción",
            key="btn_ops_future",
            use_container_width=True,
            disabled=True,
        )

    # ── Cooperación: datos de contacto ────────────────────────────────────────
    if selected == "cooperacion":
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        _, col_coop, _ = st.columns([1, 2, 1])
        with col_coop:
            st.markdown(
                """<div style="background:rgba(124,92,252,.06);
                              border:1px solid rgba(124,92,252,.15);
                              border-radius:12px;padding:18px 22px;text-align:center;
                              font-family:Inter,sans-serif">
  <div style="font-size:20px;margin-bottom:8px">📑</div>
  <div style="font:700 12px/1.2 Inter,sans-serif;color:#E2E8F0;margin-bottom:6px">
    Acceso para cooperación e investigación</div>
  <div style="font:400 10px/1.6 Inter,sans-serif;color:#8892B0;margin-bottom:12px">
    Disponible para academia, ONGs y organismos de cooperación internacional.
    Datos longitudinales verificados.</div>
  <div style="font:600 11px/1 'JetBrains Mono',monospace;
              color:#9B79FF;letter-spacing:.04em">acceso@quira.ec</div>
</div>""",
                unsafe_allow_html=True,
            )

    # ── Trust badges + footer ─────────────────────────────────────────────────
    st.markdown(trust_badges(), unsafe_allow_html=True)
    st.markdown(footer(), unsafe_allow_html=True)

    # ── Acceso operacional (ghost link — solo equipo Dylus Lab) ───────────────
    st.markdown(
        '<div style="text-align:center;padding:2px 0 6px;'
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
            type="secondary",
            help="Acceso exclusivo Dylus Lab — Equipo operativo",
        ):
            st.session_state[_SEL] = "institucional"
            st.rerun()
