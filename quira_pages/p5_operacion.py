"""
QUIRA OS v0.1 — P-05 Operación Técnica (HITL)
Ingesta de cumplimiento · Validador cruzado · Auditor HITL
Solo accesible en rol Técnico
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from components.kpi_card import section_header, info_box
from utils.session import is_tecnico, get_rol


def render() -> None:
    # ── ACCESS CONTROL ─────────────────────────────────────────────────────────
    if not is_tecnico():
        st.html("""
        <div style="background:rgba(229,62,62,0.08);border:1px solid rgba(229,62,62,0.25);
                    border-radius:12px;padding:32px;text-align:center;margin-top:40px">
            <div style="font-size:2rem;margin-bottom:12px">🔒</div>
            <div style="font-size:14px;font-weight:700;color:#FC8181;margin-bottom:8px">
                Acceso Restringido
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4)">
                Esta sección es exclusiva del rol Técnico.<br>
                Rol actual: <strong style="color:#FFB700">{}</strong>
            </div>
        </div>
        """.format(get_rol()))
        return

    data = load_all()

    # ── HEADER ─────────────────────────────────────────────────────────────────
    st.html("""
    <div style="margin-bottom:20px">
        <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0">
            ⚙️ Operación Técnica · HITL
        </h1>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:4px">
            Human-in-the-Loop · Ingesta · Validación cruzada · Auditoría
        </div>
    </div>
    """)

    # ── TABS ───────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        "📥 Ingesta de Cumplimiento",
        "🔀 Validador Cruzado",
        "🔍 Auditor HITL",
    ])

    with tab1:
        _render_ingesta(data)

    with tab2:
        _render_validador(data)

    with tab3:
        _render_auditor(data)


# ── P-17: INGESTA DE CUMPLIMIENTO ──────────────────────────────────────────────
def _render_ingesta(data: dict) -> None:
    section_header("Ingesta de Cumplimiento", "Carga manual de evidencias por período", "📥")

    info_box(
        "🔧 Este módulo permite cargar evidencias de cumplimiento (SHA-256) para los "
        "procesos PAC/POA. En PMV v0.1, funciona como simulador de interfaz — "
        "la carga real se activará con el conector eSIGEF en Q2-2026.",
        level="warning",
    )

    st.html("<div style='height:10px'></div>")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        _ingesta_form()
    with col2:
        _ingesta_status(data)


def _ingesta_form() -> None:
    st.html("""
    <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.5);
                letter-spacing:0.06em;margin-bottom:12px">
        FORMULARIO DE CARGA
    </div>
    """)

    with st.form("ingesta_form"):
        proceso_id = st.text_input("ID Proceso PAC/POA", placeholder="PAC-2026-001")
        tipo = st.selectbox(
            "Tipo de Evidencia",
            ["Contrato firmado", "Acta de entrega", "Factura", "Resolución", "Otro"],
        )
        descripcion = st.text_area("Descripción", placeholder="Descripción del hito de cumplimiento...", height=80)
        monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
        fecha = st.date_input("Fecha de hito")
        archivo = st.file_uploader("Evidencia (PDF/imagen)", type=["pdf", "png", "jpg"])

        submitted = st.form_submit_button("📤 Registrar Evidencia")
        if submitted:
            if proceso_id:
                st.success(f"✓ Evidencia '{proceso_id}' registrada en modo simulación · SHA-256 pendiente")
            else:
                st.error("Debe ingresar el ID del proceso.")


def _ingesta_status(data: dict) -> None:
    st.html("""
    <div style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.5);
                letter-spacing:0.06em;margin-bottom:12px">
        ESTADO GENERAL · SAT-0
    </div>
    """)

    # SAT-0 info
    sat0 = next((s for s in data["sat"] if s["id"] == "SAT-0"), None)
    if sat0:
        st.html(f"""
        <div style="background:rgba(229,62,62,0.08);border:1px solid rgba(229,62,62,0.25);
                    border-left:4px solid #E53E3E;border-radius:10px;padding:14px">
            <div style="font-size:12px;font-weight:700;color:#FC8181;margin-bottom:8px">
                🔴 {sat0['nombre']}
            </div>
            <div style="font-size:10px;color:rgba(255,255,255,0.6);margin-bottom:8px;line-height:1.5">
                {sat0['descripcion']}
            </div>
            <div style="font-size:10px;color:rgba(255,255,255,0.5);line-height:1.5">
                <strong style="color:#FC8181">Impacto:</strong> {sat0['impacto']}<br>
                <strong style="color:#FC8181">Acción:</strong> {sat0['accion']}
            </div>
        </div>
        """)

    st.html("<div style='height:10px'></div>")

    # Estadísticas rápidas
    stats = [
        ("Procesos sin evidencia", "24", "#E53E3E"),
        ("Procesos con evidencia", "18", "#38A169"),
        ("Pendientes revisión", "6",  "#E67E22"),
        ("Tasa cobertura",       "43%","#D69E2E"),
    ]
    for label, val, color in stats:
        st.html(f"""
        <div style="display:flex;justify-content:space-between;padding:6px 0;
                    border-bottom:1px solid rgba(255,255,255,0.05)">
            <span style="font-size:10px;color:rgba(255,255,255,0.55)">{label}</span>
            <span style="font-size:11px;font-weight:700;color:{color}">{val}</span>
        </div>
        """)


# ── P-18: VALIDADOR CRUZADO ────────────────────────────────────────────────────
def _render_validador(data: dict) -> None:
    section_header("Validador Cruzado", "POA → PAC → SERCOP → eSIGEF · cortes de trazabilidad", "🔀")

    info_box(
        "🔧 El validador cruzado detecta inconsistencias entre capas de la cadena de ejecución. "
        "En PMV v0.1, muestra los 4 cortes identificados en Q1-2026.",
        level="warning",
    )

    st.html("<div style='height:10px'></div>")

    # 4 cortes detectados
    cortes = [
        {
            "id": "C1",
            "capa_origen": "POA 2026",
            "capa_destino": "PAC Q1",
            "descripcion": "12 metas POA sin correlato en PAC Q1",
            "impacto": "Desconexión planificación-contratación",
            "estado": "CRÍTICO",
            "color": "#E53E3E",
        },
        {
            "id": "C2",
            "capa_origen": "PAC Q1",
            "capa_destino": "SERCOP",
            "descripcion": "24 procesos PAC sin registro en portal SERCOP",
            "impacto": "SAT-0 activa · riesgo observación Contraloría",
            "estado": "CRÍTICO",
            "color": "#E53E3E",
        },
        {
            "id": "C3",
            "capa_origen": "SERCOP",
            "capa_destino": "eSIGEF",
            "descripcion": "8 contratos adjudicados sin devengamiento eSIGEF",
            "impacto": "Gasto no reflejado en ejecución presupuestal",
            "estado": "ALERTA",
            "color": "#E67E22",
        },
        {
            "id": "C4",
            "capa_origen": "eSIGEF",
            "capa_destino": "Informes",
            "descripcion": "Discrepancia $320K entre eSIGEF e informe alcaldía",
            "impacto": "Riesgo reputacional · auditoría interna recomendada",
            "estado": "ALERTA",
            "color": "#E67E22",
        },
    ]

    col1, col2 = st.columns(2, gap="medium")
    for i, corte in enumerate(cortes):
        with (col1 if i % 2 == 0 else col2):
            st.html(f"""
            <div style="background:rgba(255,255,255,0.03);
                        border:1px solid rgba({_rgb(corte['color'])},0.25);
                        border-left:4px solid {corte['color']};
                        border-radius:10px;padding:14px;margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                    <div style="font-size:12px;font-weight:700;color:#E2E8F0">
                        Corte {corte['id']} · {corte['capa_origen']} → {corte['capa_destino']}
                    </div>
                    <span style="font-size:9px;background:rgba({_rgb(corte['color'])},0.15);
                                 border-radius:20px;padding:2px 10px;
                                 color:{corte['color']};font-weight:700">
                        {corte['estado']}
                    </span>
                </div>
                <div style="font-size:10px;color:rgba(255,255,255,0.6);margin-bottom:6px">
                    {corte['descripcion']}
                </div>
                <div style="font-size:9px;color:rgba(255,255,255,0.4)">
                    ⚠ {corte['impacto']}
                </div>
            </div>
            """)

    # Resumen de cadena
    st.html("<div style='height:10px'></div>")
    section_header("Cadena de Trazabilidad", "Estado actual Q1-2026", "🔗")

    cadena = [
        ("POA 2026",  "🟡 Parcial",  "#D69E2E", "12 metas sin correlato PAC"),
        ("PAC Q1",    "🔴 Crítico",  "#E53E3E", "24 procesos sin evidencia"),
        ("SERCOP",    "🟠 Alerta",   "#E67E22", "8 contratos sin devengamiento"),
        ("eSIGEF",    "🟠 Alerta",   "#E67E22", "Discrepancia $320K"),
        ("Informes",  "🟡 Revisión", "#D69E2E", "Pendiente reconciliación"),
    ]

    cols = st.columns(len(cadena))
    for col, (capa, estado, color, nota) in zip(cols, cadena):
        with col:
            st.html(f"""
            <div style="background:rgba({_rgb(color)},0.08);border:1px solid rgba({_rgb(color)},0.25);
                        border-radius:8px;padding:10px;text-align:center">
                <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.7)">{capa}</div>
                <div style="font-size:10px;color:{color};font-weight:700;margin-top:4px">{estado}</div>
                <div style="font-size:8px;color:rgba(255,255,255,0.35);margin-top:4px">{nota}</div>
            </div>
            """)


# ── P-19: AUDITOR HITL ────────────────────────────────────────────────────────
def _render_auditor(data: dict) -> None:
    section_header("Auditor HITL", "Human-in-the-Loop · validación de hallazgos", "🔍")

    info_box(
        "🔧 El Auditor HITL permite al equipo técnico validar, rechazar o escalar hallazgos "
        "del motor QUIRA. En PMV v0.1, funciona como panel de revisión simulado.",
        level="warning",
    )

    st.html("<div style='height:10px'></div>")

    # Hallazgos pendientes
    hallazgos = [
        {
            "id": "HLL-001",
            "tipo": "Fragmentación",
            "descripcion": "Patrón de partición de contratos DAPS-01 detectado por motor QUIRA",
            "confianza": 87,
            "sat": "SAT-I",
            "estado": "PENDIENTE",
        },
        {
            "id": "HLL-002",
            "tipo": "Brecha Participación",
            "descripcion": "2 parroquias sin asambleas ni presupuesto participativo documentado",
            "confianza": 95,
            "sat": "SAT-V",
            "estado": "PENDIENTE",
        },
        {
            "id": "HLL-003",
            "tipo": "Catastro Desactualizado",
            "descripcion": "ISP 14.58% — Coactivas no iniciadas para recuperación ingresos propios",
            "confianza": 91,
            "sat": "SAT-IV",
            "estado": "VALIDADO",
        },
    ]

    for h in hallazgos:
        conf_color = "#38A169" if h["confianza"] >= 90 else "#D69E2E"
        estado_color = {
            "PENDIENTE": "#E67E22",
            "VALIDADO":  "#38A169",
            "RECHAZADO": "#E53E3E",
        }.get(h["estado"], "#D69E2E")

        col_info, col_action = st.columns([3, 1])
        with col_info:
            st.html(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                        border-radius:10px;padding:14px;margin-bottom:4px">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                        <div style="font-size:11px;font-weight:700;color:#E2E8F0">
                            {h['id']} · {h['tipo']}
                        </div>
                        <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">
                            Vinculado a {h['sat']}
                        </div>
                    </div>
                    <div style="display:flex;gap:8px;align-items:center">
                        <span style="font-size:9px;color:{conf_color};font-weight:700">
                            ⚡ {h['confianza']}% confianza
                        </span>
                        <span style="font-size:9px;background:rgba({_rgb(estado_color)},0.15);
                                     border-radius:20px;padding:2px 10px;
                                     color:{estado_color};font-weight:700">
                            {h['estado']}
                        </span>
                    </div>
                </div>
                <div style="font-size:10px;color:rgba(255,255,255,0.6);margin-top:8px">
                    {h['descripcion']}
                </div>
            </div>
            """)

        with col_action:
            if h["estado"] == "PENDIENTE":
                st.html("<div style='height:4px'></div>")
                if st.button("✓ Validar", key=f"val_{h['id']}"):
                    st.success("Validado")
                if st.button("✗ Rechazar", key=f"rec_{h['id']}"):
                    st.error("Rechazado")
                if st.button("↑ Escalar", key=f"esc_{h['id']}"):
                    st.warning("Escalado al Alcalde")

        st.html("<div style='height:4px'></div>")

    # Log técnico
    st.html("<div style='height:16px'></div>")
    section_header("Log de Auditoría", "Acciones técnicas registradas", "📋")
    st.html("""
    <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.07);
                border-radius:10px;padding:14px;font-family:monospace">
        <div style="font-size:10px;color:#38A169">[2026-03-31 14:22] HLL-003 VALIDADO · usuario:tecnico</div>
        <div style="font-size:10px;color:#D69E2E">[2026-03-28 10:15] SAT-IV activada · ISP=14.58 umbral=65</div>
        <div style="font-size:10px;color:#E53E3E">[2026-03-25 09:05] SAT-0 activada · 24 procesos sin SHA-256</div>
        <div style="font-size:10px;color:#7C5CFC">[2026-03-20 16:40] Motor QUIRA v0.1 inicializado · SIAP-ICPI cargado</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.3)">[2026-03-01 08:00] Corte Q1-2026 abierto · marzo 2026</div>
    </div>
    """)


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,255,255"
