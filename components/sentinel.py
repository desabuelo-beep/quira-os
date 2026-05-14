"""
QUIRA OS v0.1 — Sentinel · Asistente de Gobernanza
Powered by Google Gemini 1.5 Flash (free tier) + PDOT_KB + SIAP-ICPI Q1-2026

Sentinel es el componente conversacional de QUIRA OS. Su carácter:
  · Analítico: razona con los datos reales del ICGI-T y el PDOT
  · Prospectivo: conecta situación actual con metas 2023-2027
  · Territorial: conoce los 7 parroquias, NBI, riesgos, brechas
  · Institucional: sabe de SATs, congruencias y obligaciones legales
  · Directo: no da respuestas genéricas; siempre ancla al cantón

Dylus Lab © 2026
"""
import streamlit as st
import os
import google.generativeai as genai
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
- Responde siempre en español.

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
    """Renderiza el chat Sentinel con Google Gemini Flash."""
    if "sentinel_messages" not in st.session_state:
        st.session_state["sentinel_messages"] = []

    data     = load_all()
    pdot_ctx = build_pdot_context()
    rol      = get_rol()

    system_prompt = _build_system_prompt(data, pdot_ctx, rol)

    # ── HEADER ─────────────────────────────────────────────────────────────────
    if not compact:
        pdot_stats = pdot_context_stats()
        pdot_status = (
            f"⚡ PDOT KB activo · ~{pdot_stats['tokens_aprox']:,} tokens"
            if pdot_stats["disponible"] else "⚠ PDOT KB no disponible"
        )
        st.subheader("🔮 Sentinel · Asistente de Gobernanza")
        st.caption(
            f"Análisis territorial · Prospectiva · PDOT 2023-2027 · ICGI-T Q1-2026"
            f"   |   {pdot_status}   |   ✨ Gemini 1.5 Flash"
        )
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
        st.error("🔑 **Gemini API Key no configurada** — Sentinel requiere una Google AI API Key.")
        with st.expander("Ver instrucciones"):
            st.markdown("""
**Cómo obtener la API Key (gratis):**
1. Ve a [aistudio.google.com](https://aistudio.google.com) → **Get API Key**
2. Crea una clave (plan gratuito: 15 RPM, 1M tokens/mes)

**Configura en Streamlit Cloud:**
En tu app → ⋮ → **Settings → Secrets** → agrega:
```toml
GEMINI_API_KEY = "AIza..."
```
            """)
        temp_key = st.text_input(
            "O ingresa la API Key para esta sesión:",
            type="password",
            placeholder="AIza...",
        )
        if temp_key and temp_key.startswith("AIza"):
            st.session_state["temp_gemini_key"] = temp_key
            st.rerun()
        return

    # ── PREGUNTA INICIAL AUTO-INJECT ───────────────────────────────────────────
    if pregunta_inicial and not st.session_state["sentinel_messages"]:
        st.session_state["sentinel_messages"].append({
            "role": "user",
            "content": pregunta_inicial,
        })
        _run_sentinel(api_key, system_prompt)

    # ── HISTORIAL ─────────────────────────────────────────────────────────────
    _render_chat_history()

    # ── SUGERENCIAS ───────────────────────────────────────────────────────────
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
    """Llama a Gemini Flash con el historial actual y agrega la respuesta."""
    messages = st.session_state["sentinel_messages"]

    with st.chat_message("assistant", avatar="🔮"):
        with st.spinner("Sentinel analizando…"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=system_prompt,
                )

                # Convertir historial al formato Gemini (user/model, no user/assistant)
                gemini_history = []
                for msg in messages[:-1]:  # Todos menos el último (el nuevo)
                    gemini_role = "user" if msg["role"] == "user" else "model"
                    gemini_history.append({
                        "role": gemini_role,
                        "parts": [msg["content"]],
                    })

                chat = model.start_chat(history=gemini_history)
                user_msg = messages[-1]["content"]

                full_response = ""
                response_placeholder = st.empty()

                response = chat.send_message(user_msg, stream=True)
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)

                st.session_state["sentinel_messages"].append({
                    "role": "assistant",
                    "content": full_response,
                })

            except Exception as e:
                err = str(e)
                if "API_KEY_INVALID" in err or "API key" in err.lower():
                    st.error("⚠ API Key de Gemini inválida. Verifica en Google AI Studio.")
                elif "quota" in err.lower() or "429" in err:
                    st.error("⚠ Límite de cuota alcanzado. Intenta en unos segundos.")
                else:
                    st.error(f"⚠ Error Sentinel: {err[:200]}")
                if st.session_state["sentinel_messages"]:
                    st.session_state["sentinel_messages"].pop()


def _render_chat_history() -> None:
    for msg in st.session_state["sentinel_messages"]:
        role   = msg["role"]
        avatar = "🔮" if role == "assistant" else "👤"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])


def _render_suggestions() -> None:
    sugerencias = [
        "¿Cuáles son las parroquias con mayor urgencia de inversión?",
        "¿Por qué el ICGI-T bajó de 69.93 en 2025 a 53.56 en Q1-2026?",
        "¿Qué riesgos territoriales tiene mayor prioridad según el PDOT?",
        "¿Cómo afecta la paradoja democrática de Isabel Muentes a la gobernanza?",
        "¿Qué debería hacer el GAD para alcanzar la meta de 70 al cierre 2026?",
        "¿Cuáles son las potencialidades económicas más relevantes del cantón?",
    ]
    st.caption("💬 PREGUNTAS SUGERIDAS")
    cols = st.columns(2)
    for i, sug in enumerate(sugerencias):
        with cols[i % 2]:
            if st.button(f"💬 {sug}", key=f"sug_{i}", use_container_width=True):
                st.session_state["sentinel_messages"].append({
                    "role": "user",
                    "content": sug,
                })
                st.rerun()


def _get_api_key() -> str:
    """
    Obtiene Gemini API Key en orden de prioridad:
    1. session_state (ingresada temporalmente en UI)
    2. Streamlit secrets: GEMINI_API_KEY o GOOGLE_API_KEY
    3. Variables de entorno
    """
    if "temp_gemini_key" in st.session_state:
        return st.session_state["temp_gemini_key"]
    try:
        key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return (
        os.environ.get("GEMINI_API_KEY", "")
        or os.environ.get("GOOGLE_API_KEY", "")
    )
