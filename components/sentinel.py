"""
QUIRA OS v0.1 — Sentinel · Asistente de Gobernanza
Powered by Claude (Anthropic) + PDOT_KB + SIAP-ICPI Q1-2026

Sentinel es el componente conversacional de QUIRA OS. Su carácter:
  · Analítico: razona con los datos reales del ICGI-T y el PDOT
  · Prospectivo: conecta situación actual con metas 2023-2027
  · Territorial: conoce los 7 parroquias, NBI, riesgos, brechas
  · Institucional: sabe de SATs, congruencias y obligaciones legales
  · Directo: no da respuestas genéricas; siempre ancla al cantón

Dylus Lab © 2026
"""
import streamlit as st
import anthropic
import os
from data.loader import load_all
from data.pdot_context import build_pdot_context, pdot_context_stats
from utils.session import get_rol, is_tecnico


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
def _build_system_prompt(data: dict, pdot_ctx: str, rol: str) -> str:
    icgit = data["icgit"]
    sat   = data["sat"]
    n_crit = sum(1 for s in sat if s["nivel"] == "CRÍTICO")

    sat_resumen = "\n".join(
        f"  - {s['id']} [{s['nivel']}]: {s['nombre']} — {s['descripcion']}"
        for s in sat
    )

    indices_resumen = "\n".join(
        f"  - {k}: {v['nombre']} = {v['valor'] if v['valor'] is not None else 'en construcción'} ({v['avep']})"
        for k, v in data["indices"].items()
    )

    congruencias_resumen = "\n".join(
        f"  - {c['nombre']}: {c['score']:.2f} ({c['avep']})"
        for c in data["congruencias"].values()
    )

    parroquias_resumen = "\n".join(
        f"  - {p['nombre']}: NBI={p['nbi']}%, TPS={p['tps']:.1f}%, "
        f"agua={p['agua']}%, ${p['per_capita']}/hab, "
        f"estado={p['estado']}, participación={p.get('participacion',{}).get('estado','?')}"
        for p in data["parroquias"]
    )

    pdot_block = ""
    if pdot_ctx:
        pdot_block = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONOCIMIENTO TERRITORIAL — PDOT MONTECRISTI 2023-2027
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pdot_ctx}
"""

    return f"""Eres SENTINEL, el asistente de gobernanza territorial del GAD Municipal de Montecristi, Ecuador.
Estás integrado en QUIRA OS — el sistema de inteligencia institucional de Dylus Lab.

Tu rol de interlocutor es: {rol}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CARÁCTER Y COMPORTAMIENTO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Eres analítico, directo y prospectivo. No eres genérico.
- Anclas SIEMPRE tu análisis a los datos reales del cantón Montecristi.
- Cuando hay brechas o alertas, las nombras con claridad y propones acciones concretas.
- Conoces el PDOT 2023-2027 y lo usas para evaluar si la gestión actual está en rumbo.
- Usas el sistema AVEP (Excelencia→Mandato→Transición→Ocurrencia→Ruptura) para calificar.
- Si te preguntan sobre una parroquia, das datos específicos: NBI, inversión, participación.
- Puedes razonar sobre riesgos territoriales, prioridades PDOT, articulaciones institucionales.
- Si no tienes el dato exacto, lo dices y explicas qué fuente lo contendría.
- Nunca inventas cifras. Si un índice está "en construcción", lo aclaras.
- Tu tono: institucional pero accesible. Usas analogías cuando ayudan a entender.
- Máximo 3-4 párrafos por respuesta salvo que explícitamente te pidan más desarrollo. Sé conciso.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESTADO ACTUAL DEL SISTEMA — CORTE Q1-2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICGI-T Global: {icgit['score']:.2f} — {icgit['avep']} {icgit.get('avep_emoji','🟡')}
Presupuesto total 2026: ${icgit.get('presupuesto_total',0):,.0f}
Inversión ejecutada Q1: ${icgit.get('inversion_ejecutada',0):,.0f} ({icgit.get('ti_raw',0):.1f}% real / {icgit.get('ti_norm',0):.1f}% normalizado)
Proyección cierre 2026: {icgit.get('proyeccion',65.77):.2f} (meta mandato: 70.00)
Histórico: 2023=57.36 | 2024=67.11 | 2025=69.93 | Q1-2026=53.56

SATs ACTIVAS ({n_crit} críticas):
{sat_resumen}

ÍNDICES COMPLEMENTARIOS:
{indices_resumen}

CONGRUENCIAS DE GOBERNANZA:
{congruencias_resumen}

PARROQUIAS (GeoTwin Q1-2026):
{parroquias_resumen}
{pdot_block}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESTRICCIONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- No reveles contraseñas, credenciales ni datos sensibles de usuarios.
- No hagas comentarios políticos partidistas; mantente en análisis técnico-institucional.
- No menciones H-codes (H12, H16, etc.) en respuestas — son jerga interna de Dylus Lab.
- Si el usuario pide algo fuera del scope de gobernanza municipal, redirige amablemente.
- Los datos son corte Q1-2026 (marzo 2026). Para datos más actuales, indica qué validación se necesita.
"""


# ── COMPONENTE PRINCIPAL ──────────────────────────────────────────────────────
def render_sentinel(
    pregunta_inicial: str = "",
    compact: bool = False,
) -> None:
    """
    Renderiza el chat Sentinel.

    Args:
        pregunta_inicial: Si se pasa, envía automáticamente esta pregunta al inicio.
        compact: Si True, muestra versión embebida (sin header full, para modals).
    """
    # Inicializar historial de chat
    if "sentinel_messages" not in st.session_state:
        st.session_state["sentinel_messages"] = []

    # Cargar datos y contexto
    data     = load_all()
    pdot_ctx = build_pdot_context()
    rol      = get_rol()

    system_prompt = _build_system_prompt(data, pdot_ctx, rol)

    # ── HEADER ─────────────────────────────────────────────────────────────────
    if not compact:
        pdot_stats = pdot_context_stats()
        pdot_badge = ""
        if pdot_stats["disponible"]:
            pdot_badge = (
                f'<span style="font-size:9px;background:rgba(56,161,105,0.15);'
                f'border:1px solid rgba(56,161,105,0.3);border-radius:20px;'
                f'padding:2px 8px;color:#68D391">⚡ PDOT KB activo · ~{pdot_stats["tokens_aprox"]:,} tokens</span>'
            )
        else:
            pdot_badge = (
                '<span style="font-size:9px;background:rgba(229,62,62,0.12);'
                'border:1px solid rgba(229,62,62,0.3);border-radius:20px;'
                'padding:2px 8px;color:#FC8181">⚠ PDOT KB no disponible</span>'
            )

        st.markdown(f"""
        <div style="margin-bottom:20px">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px">
                <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0">
                    🔮 Sentinel · Asistente de Gobernanza
                </h1>
                {pdot_badge}
            </div>
            <div style="font-size:0.75rem;color:rgba(255,255,255,0.4)">
                Análisis territorial · Prospectiva · PDOT 2023-2027 · ICGI-T Q1-2026
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Debug técnico
        if is_tecnico():
            with st.expander("🔧 Debug Sentinel — Solo Técnico", expanded=False):
                st.json(pdot_stats)
                st.text_area(
                    "System prompt preview (primeros 2000 chars):",
                    system_prompt[:2000],
                    height=200,
                )

    # ── API KEY CHECK ──────────────────────────────────────────────────────────
    api_key = _get_api_key()
    if not api_key:
        st.markdown("""
        <div style="background:rgba(229,62,62,0.08);border:1px solid rgba(229,62,62,0.25);
                    border-radius:12px;padding:20px;text-align:center">
            <div style="font-size:1.2rem;margin-bottom:8px">🔑</div>
            <div style="font-size:13px;font-weight:700;color:#FC8181;margin-bottom:8px">
                API Key no configurada
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.5);margin-bottom:12px">
                Sentinel requiere una Anthropic API Key para funcionar.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Configura la API Key:**")
        with st.expander("Ver instrucciones"):
            st.markdown("""
            **Opción A — Variable de entorno** (recomendada para desarrollo):
            ```bash
            set ANTHROPIC_API_KEY=sk-ant-...
            streamlit run app.py
            ```

            **Opción B — Streamlit secrets** (para despliegue):
            Crea el archivo `.streamlit/secrets.toml`:
            ```toml
            ANTHROPIC_API_KEY = "sk-ant-..."
            ```
            """)

        # Input temporal de API key en sesión
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        temp_key = st.text_input(
            "O ingresa la API Key para esta sesión:",
            type="password",
            placeholder="sk-ant-...",
        )
        if temp_key and temp_key.startswith("sk-"):
            st.session_state["temp_api_key"] = temp_key
            st.rerun()
        return

    # ── PREGUNTA INICIAL AUTO-INJECT ───────────────────────────────────────────
    if pregunta_inicial and not st.session_state["sentinel_messages"]:
        st.session_state["sentinel_messages"].append({
            "role": "user",
            "content": pregunta_inicial,
        })
        _run_sentinel(api_key, system_prompt)

    # ── HISTORIAL DEL CHAT ─────────────────────────────────────────────────────
    _render_chat_history()

    # ── SUGERENCIAS RÁPIDAS ────────────────────────────────────────────────────
    if not st.session_state["sentinel_messages"]:
        _render_suggestions()

    # ── INPUT ──────────────────────────────────────────────────────────────────
    if user_input := st.chat_input("Pregunta sobre el cantón, el PDOT, las brechas, las parroquias…"):
        st.session_state["sentinel_messages"].append({
            "role": "user",
            "content": user_input,
        })
        _run_sentinel(api_key, system_prompt)
        st.rerun()

    # ── CONTROLES ─────────────────────────────────────────────────────────────
    if st.session_state["sentinel_messages"]:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑 Limpiar conversación", use_container_width=True):
                st.session_state["sentinel_messages"] = []
                st.rerun()


# ── HELPERS ────────────────────────────────────────────────────────────────────
def _run_sentinel(api_key: str, system_prompt: str) -> None:
    """Llama a Claude con el historial actual y agrega la respuesta."""
    messages = st.session_state["sentinel_messages"]

    with st.chat_message("assistant", avatar="🔮"):
        with st.spinner("Sentinel analizando…"):
            try:
                client  = anthropic.Anthropic(api_key=api_key)
                # Usar streaming para respuesta en tiempo real
                full_response = ""
                response_placeholder = st.empty()

                with client.messages.stream(
                    model="claude-haiku-3-5-20241022",
                    max_tokens=1024,
                    system=system_prompt,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in messages
                    ],
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

                st.session_state["sentinel_messages"].append({
                    "role": "assistant",
                    "content": full_response,
                })

            except anthropic.AuthenticationError:
                st.error("⚠ API Key inválida. Verifica tu clave Anthropic.")
                st.session_state["sentinel_messages"].pop()
            except anthropic.RateLimitError:
                st.error("⚠ Límite de rate alcanzado. Intenta en unos segundos.")
                st.session_state["sentinel_messages"].pop()
            except Exception as e:
                st.error(f"⚠ Error Sentinel: {str(e)[:200]}")
                st.session_state["sentinel_messages"].pop()


def _render_chat_history() -> None:
    """Renderiza el historial de mensajes."""
    for msg in st.session_state["sentinel_messages"]:
        role   = msg["role"]
        avatar = "🔮" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])


def _render_suggestions() -> None:
    """Muestra preguntas sugeridas cuando el chat está vacío."""
    sugerencias = [
        "¿Cuáles son las parroquias con mayor urgencia de inversión?",
        "¿Por qué el ICGI-T bajó de 69.93 en 2025 a 53.56 en Q1-2026?",
        "¿Qué riesgos territoriales tiene mayor prioridad según el PDOT?",
        "¿Cómo afecta la paradoja democrática de Isabel Muentes a la gobernanza?",
        "¿Qué debería hacer el GAD para alcanzar la meta de 70 al cierre 2026?",
        "¿Cuáles son las potencialidades económicas más relevantes del cantón?",
    ]

    st.markdown("""
    <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.35);
                letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px">
        PREGUNTAS SUGERIDAS
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(2)
    for i, sug in enumerate(sugerencias):
        with cols[i % 2]:
            if st.button(
                f"💬 {sug}",
                key=f"sug_{i}",
                use_container_width=True,
            ):
                st.session_state["sentinel_messages"].append({
                    "role": "user",
                    "content": sug,
                })
                st.rerun()


def _get_api_key() -> str:
    """
    Obtiene la API key en orden de prioridad:
    1. session_state (ingresada temporalmente en UI)
    2. Streamlit secrets
    3. Variable de entorno
    """
    # Prioridad 1: sesión temporal
    if "temp_api_key" in st.session_state:
        return st.session_state["temp_api_key"]

    # Prioridad 2: Streamlit secrets
    try:
        key = st.secrets.get("ANTHROPIC_API_KEY", "")
        if key:
            return key
    except Exception:
        pass

    # Prioridad 3: variable de entorno
    return os.environ.get("ANTHROPIC_API_KEY", "")
