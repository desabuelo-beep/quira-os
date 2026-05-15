"""
QUIRA OS v0.1 — Sentinel · Agente de Gobernanza Territorial
Powered by Groq · Llama 3.3 70B (free tier)
Arquitectura: sentinel/ package (tools · policies · audit · prompts)
Fase: READER v0.1 — Lee H73/H99, explica, alerta, sugiere. No actúa de forma autónoma.
Doctrina: "La IA opera. La autoridad pública decide."
Dylus Lab © 2026
"""
import streamlit as st
import os
from data.loader import load_all
from data.pdot_context import build_pdot_context, pdot_context_stats
from utils.session import get_rol, is_tecnico
from sentinel.prompts  import build_system_prompt
from sentinel.policies import evaluar_seguridad, sugerir_pantallas
from sentinel.audit    import log_interaction, get_audit_stats


# ── COMPONENTE PRINCIPAL ──────────────────────────────────────────────────────
def render_sentinel(
    pregunta_inicial: str = "",
    compact: bool = False,
) -> None:
    """Renderiza el chat Sentinel con Groq · Llama 3.3."""
    if "sentinel_messages" not in st.session_state:
        st.session_state["sentinel_messages"] = []

    data     = load_all()
    pdot_ctx = build_pdot_context()
    rol      = get_rol()

    # ── Sistema de prompt v2 (sentinel.prompts) ────────────────────────────────
    system_prompt = build_system_prompt(data, pdot_ctx, rol)

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
            f"   |   {pdot_status}   |   ⚡ Groq · Llama 3.3 70B"
        )
        if is_tecnico():
            with st.expander("🔧 Debug Sentinel — Solo Técnico", expanded=False):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.caption("PDOT Knowledge Base")
                    st.json(pdot_stats)
                with col_d2:
                    st.caption("Audit Log Stats")
                    st.json(get_audit_stats())
                st.text_area(
                    "System prompt preview (primeros 2000 chars):",
                    system_prompt[:2000],
                    height=200,
                )
                # Pantallas sugeridas por política
                pantallas_sug = st.session_state.get("sentinel_pantallas_sugeridas", [])
                if pantallas_sug:
                    st.caption(f"Pantallas sugeridas por política: {pantallas_sug}")

    # ── API KEY CHECK ──────────────────────────────────────────────────────────
    api_key = _get_api_key()
    if not api_key:
        st.error("🔑 **Groq API Key no configurada** — Sentinel requiere una Groq API Key (gratis, sin tarjeta).")
        with st.expander("Ver instrucciones"):
            st.markdown("""
**Cómo obtener la API Key (100% gratis, sin tarjeta de crédito):**
1. Ve a [console.groq.com](https://console.groq.com) → crea cuenta → **API Keys** → **Create API Key**
2. Copia la clave (empieza con `gsk_`)

**Configura en Streamlit Cloud:**
En tu app → ⋮ → **Settings → Secrets** → agrega:
```toml
GROQ_API_KEY = "gsk_..."
```
            """)
        temp_key = st.text_input(
            "O ingresa la API Key para esta sesión:",
            type="password",
            placeholder="gsk_...",
        )
        if temp_key and temp_key.startswith("gsk_"):
            st.session_state["temp_groq_key"] = temp_key
            st.rerun()
        return

    # ── PREGUNTA INICIAL AUTO-INJECT ───────────────────────────────────────────
    # Recoge pregunta inyectada desde otras páginas (Holding, GeoTwin, etc.)
    if not pregunta_inicial:
        pregunta_inicial = st.session_state.pop("sentinel_pregunta_auto", "")

    if pregunta_inicial and not st.session_state["sentinel_messages"]:
        st.session_state["sentinel_messages"].append({
            "role": "user",
            "content": pregunta_inicial,
        })
        _run_sentinel(api_key, system_prompt)

    # ── HISTORIAL ─────────────────────────────────────────────────────────────
    _render_chat_history()

    # ── PENDING RESPONSE ──────────────────────────────────────────────────────
    # Si el último mensaje es del usuario (sin respuesta aún), genera la respuesta.
    # Esto cubre el caso de los botones de sugerencia que hacen st.rerun() sin
    # llamar a _run_sentinel(), dejando la pregunta "huérfana" en el historial.
    _msgs = st.session_state["sentinel_messages"]
    if _msgs and _msgs[-1]["role"] == "user":
        _run_sentinel(
            api_key, system_prompt,
            pagina_origen=st.session_state.get("page"),
        )
        st.rerun()

    # ── SUGERENCIAS ───────────────────────────────────────────────────────────
    if not st.session_state["sentinel_messages"]:
        _render_suggestions()

    # ── INPUT ──────────────────────────────────────────────────────────────────
    if user_input := st.chat_input("Pregunta sobre el cantón, el PDOT, las brechas, las parroquias…"):
        # Policy check antes de procesar
        seguridad = evaluar_seguridad(user_input)
        if not seguridad["permitido"]:
            st.warning(
                f"🛡️ **Sentinel (Reader) no puede ejecutar esa acción.**\n\n"
                f"{seguridad['motivo']}\n\n"
                f"El funcionario responsable debe confirmar y ejecutar esta acción en el sistema correspondiente."
            )
        else:
            # Sugerir pantallas relacionadas (sidebar context)
            pantallas = sugerir_pantallas(user_input)
            if pantallas:
                st.session_state["sentinel_pantallas_sugeridas"] = pantallas

            st.session_state["sentinel_messages"].append({
                "role": "user",
                "content": user_input,
            })
            _run_sentinel(
                api_key, system_prompt,
                modo_seguro=seguridad.get("modo_seguro", False),
                pagina_origen=st.session_state.get("page"),
            )
            st.rerun()

    # ── CONTROLES ─────────────────────────────────────────────────────────────
    if st.session_state["sentinel_messages"]:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑 Limpiar conversación", use_container_width=True):
                st.session_state["sentinel_messages"] = []
                st.rerun()


# ── HELPERS ────────────────────────────────────────────────────────────────────
# Groq: free tier real (sin billing), OpenAI-compatible, ~30 RPM, 6k TPM
_GROQ_URL        = "https://api.groq.com/openai/v1/chat/completions"
_GROQ_MODELS     = [
    "llama-3.3-70b-versatile",   # Llama 3.3 70B — calidad alta, free
    "llama-3.1-8b-instant",      # fallback: más rápido si el anterior falla
]
# Máximo de mensajes del historial enviados a la API (evita 413 por acumulación)
_MAX_HISTORY_MSG = 6


def _run_sentinel(
    api_key:       str,
    system_prompt: str,
    modo_seguro:   bool = False,
    pagina_origen: str | None = None,
) -> None:
    """Llama a Groq (Llama 3.3) con streaming, fallback de modelos y audit log."""
    import requests
    import json as _json

    messages = st.session_state["sentinel_messages"]
    pregunta = messages[-1]["content"] if messages else ""

    with st.chat_message("assistant", avatar="🔮"):
        placeholder = st.empty()
        with st.spinner("Sentinel analizando…"):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                }

                # Solo los últimos _MAX_HISTORY_MSG mensajes para no superar el TPM limit
                recent    = messages[-_MAX_HISTORY_MSG:] if len(messages) > _MAX_HISTORY_MSG else messages
                groq_msgs = [{"role": "system", "content": system_prompt}]
                for msg in recent:
                    groq_msgs.append({"role": msg["role"], "content": msg["content"]})

                full_response = ""
                last_err      = ""
                model_usado   = None

                for model_name in _GROQ_MODELS:
                    payload = {
                        "model":       model_name,
                        "messages":    groq_msgs,
                        "max_tokens":  900,
                        "temperature": 0.65,
                        "stream":      True,
                    }
                    try:
                        with requests.post(
                            _GROQ_URL, headers=headers, json=payload,
                            stream=True, timeout=45
                        ) as resp:
                            if resp.status_code != 200:
                                last_err = (
                                    f"HTTP {resp.status_code} [{model_name}]: "
                                    f"{resp.text[:300]}"
                                )
                                continue

                            for line in resp.iter_lines():
                                if not line:
                                    continue
                                decoded = line.decode("utf-8")
                                if decoded == "data: [DONE]":
                                    break
                                if decoded.startswith("data: "):
                                    try:
                                        chunk = _json.loads(decoded[6:])
                                        delta = (
                                            chunk["choices"][0]["delta"]
                                            .get("content", "")
                                        )
                                        if delta:
                                            full_response += delta
                                            placeholder.markdown(full_response + "▌")
                                    except (_json.JSONDecodeError, KeyError):
                                        pass
                        if full_response:
                            model_usado = model_name
                            break  # éxito con este modelo
                    except Exception as ex:
                        last_err = f"{model_name}: {ex}"

                if not full_response:
                    raise RuntimeError(last_err or "Sin respuesta de Groq")

                placeholder.markdown(full_response)
                st.session_state["sentinel_messages"].append({
                    "role": "assistant",
                    "content": full_response,
                })

                # ── Audit log ─────────────────────────────────────────────────
                log_interaction(
                    pregunta=pregunta,
                    respuesta=full_response,
                    tool_usado=model_usado,
                    confianza="baja" if modo_seguro else "media",
                    modo_seguro=modo_seguro,
                    pagina_origen=pagina_origen,
                )

            except Exception as e:
                err = str(e)
                if "401" in err or "invalid_api_key" in err.lower() or "authentication" in err.lower():
                    error_msg = "⚠️ **Groq API Key inválida.** Verifica en [console.groq.com/keys](https://console.groq.com/keys)."
                elif "429" in err or "rate_limit" in err.lower():
                    error_msg = "⚠️ **Límite de Groq alcanzado.** Espera unos segundos e intenta de nuevo."
                else:
                    error_msg = f"⚠️ **Error Sentinel:**\n```\n{err[:500]}\n```"
                placeholder.markdown(error_msg)
                st.session_state["sentinel_messages"].append({
                    "role": "assistant",
                    "content": error_msg,
                })


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
    Obtiene Groq API Key en orden de prioridad:
    1. session_state (ingresada temporalmente en UI)
    2. Streamlit secrets: GROQ_API_KEY
    3. Variables de entorno
    """
    if "temp_groq_key" in st.session_state:
        return st.session_state["temp_groq_key"]
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("GROQ_API_KEY", "")
