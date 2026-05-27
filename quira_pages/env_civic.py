"""
QUIRA Intelligence — Ambiente 🌎 Civic  (PLACEHOLDER)
Vista pública participativa — Ciudadanía comprende, compara y aporta evidencia.

Estado PMV: FUTURO — no construir hasta que GOV esté estable en producción.
Activa en roadmap cuando existan al menos 6 meses de datos longitudinales.

Ref: docs/QUIRA_INTELLIGENCE.md § Civic
Dylus Lab © 2026
"""
import streamlit as st


def render() -> None:
    st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
            min-height:60vh;text-align:center;padding:2rem">
    <div style="font-size:3rem;margin-bottom:1rem">🌎</div>
    <div style="font-size:1.5rem;font-weight:800;color:#22C55E;margin-bottom:8px">
        QUIRA Civic
    </div>
    <div style="font-size:13px;color:rgba(255,255,255,.6);max-width:480px;line-height:1.7;
                margin-bottom:20px">
        Vista pública participativa. Ciudadanía comprende la trayectoria institucional
        del municipio, compara períodos y aporta evidencia documental faltante
        (PAC, POA, rendiciones de cuentas).
    </div>
    <div style="padding:8px 20px;background:rgba(34,197,94,.1);
                border:1px solid rgba(34,197,94,.25);border-radius:8px;
                font-size:11px;font-weight:700;color:#22C55E;letter-spacing:.06em">
        PRÓXIMAMENTE — EN ROADMAP
    </div>
    <div style="margin-top:24px;padding:12px 16px;background:rgba(255,255,255,.04);
                border:1px solid rgba(255,255,255,.08);border-radius:10px;
                font-size:11px;color:rgba(255,255,255,.4);max-width:420px;line-height:1.6">
        <strong style="color:rgba(255,255,255,.6)">Condición de activación:</strong>
        GOV estable en producción + 6 meses de datos longitudinales.
        Evidencia ciudadana entra como
        <code style="background:rgba(255,255,255,.08);padding:1px 5px;border-radius:3px">
        evidence_source = citizen_uploaded</code>
        con reliability_score propio.
    </div>
</div>
    """, unsafe_allow_html=True)
