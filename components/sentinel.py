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
from utils.audit_log import log_sentinel_query
from utils.input_guard import is_safe_query, check_rate_limit
from utils.session import get_rol, is_tecnico
from sentinel.prompts       import build_system_prompt
from sentinel.policies      import evaluar_seguridad, sugerir_pantallas
from sentinel.audit         import log_interaction, get_audit_stats
from sentinel.renderer      import parse_response, render_visual
from sentinel               import charts as _charts
from sentinel.legal_router      import build_legal_prompt_block, find_legal_refs, has_legal_refs
from sentinel.trust_engine      import calculate_trust, context_from_query
from sentinel.coherencia_engine import evaluate as _coh_eval, detect_coherencia_intent
from sentinel.ui_components     import trust_badge, legal_card, coherencia_card


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
            f"   |   {pdot_status}   |   ⚡ Claude Haiku · Anthropic"
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
        st.error("🔑 **Anthropic API Key no configurada** — Sentinel requiere una API Key de Anthropic.")
        with st.expander("Ver instrucciones"):
            st.markdown("""
**Cómo obtener la API Key:**
1. Ve a [console.anthropic.com](https://console.anthropic.com) → **API Keys** → **Create Key**
2. Copia la clave (empieza con `sk-ant-`)

**Configura en Streamlit Cloud:**
En tu app → ⋮ → **Settings → Secrets** → agrega:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

**En desarrollo local:** crea `.streamlit/secrets.toml` con la misma clave.
            """)
        temp_key = st.text_input(
            "O ingresa la API Key para esta sesión:",
            type="password",
            placeholder="sk-ant-...",
        )
        if temp_key and temp_key.startswith("sk-ant-"):
            st.session_state["temp_claude_key"] = temp_key
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
        # Capa 1: sanitización y anti-injection
        _safe, _clean_or_reason = is_safe_query(user_input)
        if not _safe:
            st.warning("🛡️ Input bloqueado por seguridad. Reformula tu consulta.")
            st.stop()
        user_input = _clean_or_reason  # texto limpio y truncado

        # Capa 2: rate limiting por usuario
        _allowed, _rate_msg = check_rate_limit()
        if not _allowed:
            st.warning(f"⏱️ {_rate_msg}")
            st.stop()

        # Capa 3: Policy check antes de procesar
        seguridad = evaluar_seguridad(user_input)
        if not seguridad["permitido"]:
            st.warning(
                f"🛡️ **Sentinel (Reader) no puede ejecutar esa acción.**\n\n"
                f"{seguridad['motivo']}\n\n"
                f"El funcionario responsable debe confirmar y ejecutar esta acción en el sistema correspondiente."
            )
        else:
            log_sentinel_query(
                module=st.session_state.get("page", "sentinel"),
                query_len=len(user_input),
            )
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
    # ── INDICADOR CONTEXTO ACTIVO ──────────────────────────────────────────────
    from sentinel import state_memory as _mem
    if _mem.has_context():
        ctx  = _mem.get_context()
        tags = []
        if ctx["ultima_parroquia"]:
            tags.append(f"📍 {_mem.get_parroquia_display()}")
        if ctx["ultimo_indicador"]:
            tags.append(f"📊 {ctx['ultimo_indicador']}")
        if ctx["ultimo_modo"]:
            tags.append(f"🎯 {ctx['ultimo_modo']}")
        if tags:
            st.caption(f"Contexto activo: {' · '.join(tags)}")

    if st.session_state["sentinel_messages"]:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑 Limpiar conversación", use_container_width=True):
                st.session_state["sentinel_messages"] = []
                _mem.reset()   # Sprint 3: limpia memoria junto con historial
                st.rerun()


# ── HELPERS ────────────────────────────────────────────────────────────────────
# Claude Haiku — motor LLM de QUIRA OS · Anthropic API
_CLAUDE_MODEL    = "claude-haiku-4-5"          # rápido · gobernanza · Dylus Lab 2026
_CLAUDE_FALLBACK = "claude-3-5-haiku-20241022" # fallback si haiku-4-5 no disponible
_MAX_HISTORY_MSG = 6    # Claude gestiona contexto mayor que Groq free tier
_MAX_TOKENS      = 1200


def _run_sentinel(
    api_key:       str,
    system_prompt: str,
    modo_seguro:   bool = False,
    pagina_origen: str | None = None,
) -> None:
    """Llama a Claude Haiku (Anthropic) con streaming y audit log. Dylus Lab 2026."""
    import anthropic

    messages = st.session_state["sentinel_messages"]
    pregunta = messages[-1]["content"] if messages else ""

    # ── Detección temprana de visualización (omite llamada al LLM) ────────────
    template_text = _charts.get_template_text(pregunta)
    if template_text:
        # Detectar tipo de chart para seleccionar perfil de trust
        from sentinel.simulate_policy import detect_simulation_intent
        _sim_intent  = detect_simulation_intent(pregunta)
        _chart_hit   = ""
        _q_norm      = pregunta.lower()
        if "nbi"        in _q_norm: _chart_hit = "nbi"
        elif "agua"     in _q_norm: _chart_hit = "agua"
        elif "inversion" in _q_norm or "inversión" in _q_norm: _chart_hit = "inversion"
        elif "icgi"     in _q_norm or "icgit"    in _q_norm: _chart_hit = "icgit"
        elif "indices"  in _q_norm or "índices"  in _q_norm: _chart_hit = "indices"

        _trust_ctx   = context_from_query(
            pregunta,
            chart_hit = _chart_hit,
            sim_policy= _sim_intent["policy_type"] if _sim_intent else "",
        )
        _legal_refs  = find_legal_refs(pregunta)
        _trust_res   = calculate_trust(
            _trust_ctx,
            legal_boost=bool(_legal_refs),
        )

        with st.chat_message("assistant", avatar="🔮"):
            st.markdown(template_text)
            _charts.detect_and_render(pregunta)
            trust_badge(_trust_res, _legal_refs)
            if _legal_refs:
                legal_card(_legal_refs)
        st.session_state["sentinel_messages"].append({
            "role":    "assistant",
            "content": template_text,
            "visual":  {"renderType": "intent_chart", "query": pregunta},
        })
        log_interaction(pregunta, template_text, "charts_engine_v1.1", "alta", False, pagina_origen)
        return

    with st.chat_message("assistant", avatar="🔮"):
        placeholder = st.empty()
        with st.spinner("Sentinel analizando…"):
            try:
                # Solo los últimos _MAX_HISTORY_MSG mensajes del historial
                recent = messages[-_MAX_HISTORY_MSG:] if len(messages) > _MAX_HISTORY_MSG else messages

                # Sprint 3: inyectar contexto conversacional activo en el system prompt
                from sentinel import state_memory as _mem
                ctx_block    = _mem.build_context_prompt()
                # Sprint Legal (P3): inyectar marco normativo cuando la query toca leyes
                legal_block  = build_legal_prompt_block(pregunta)
                effective_prompt = system_prompt
                if ctx_block:
                    effective_prompt += "\n\n" + ctx_block
                if legal_block:
                    effective_prompt += "\n\n" + legal_block

                # Construir historial para Claude — solo roles user/assistant (sin system)
                claude_msgs = []
                for msg in recent:
                    if msg["role"] in ("user", "assistant"):
                        claude_msgs.append({
                            "role":    msg["role"],
                            "content": msg["content"],
                        })

                # Asegurar que el historial empiece con un mensaje user
                if claude_msgs and claude_msgs[0]["role"] != "user":
                    claude_msgs = claude_msgs[1:]

                full_response = ""
                model_usado   = None

                # Intentar con modelo primario, fallback si falla
                for model_name in [_CLAUDE_MODEL, _CLAUDE_FALLBACK]:
                    try:
                        client = anthropic.Anthropic(api_key=api_key)
                        with client.messages.stream(
                            model      = model_name,
                            max_tokens = _MAX_TOKENS,
                            system     = effective_prompt,
                            messages   = claude_msgs,
                        ) as stream:
                            for text in stream.text_stream:
                                full_response += text
                                placeholder.markdown(full_response + "▌")
                        if full_response:
                            model_usado = model_name
                            break
                    except anthropic.AuthenticationError:
                        raise RuntimeError("API Key de Anthropic inválida o expirada.")
                    except anthropic.RateLimitError:
                        raise RuntimeError("Límite de Claude alcanzado — intenta en unos segundos.")
                    except anthropic.APIStatusError as ex:
                        if model_name == _CLAUDE_FALLBACK:
                            raise RuntimeError(f"Error Claude API: {ex.message[:300]}")
                        continue  # intenta fallback

                if not full_response:
                    raise RuntimeError("Sin respuesta de Claude — revisa la API Key.")

                # ── Sentinel v1.1 — Generative UI ─────────────────────────────
                # 1. Parsea si el LLM emitió JSON (fallback/futuro)
                clean_text, visual_data = parse_response(full_response)
                placeholder.markdown(clean_text)

                # 2. Si el LLM emitió JSON válido → renderízalo
                if visual_data:
                    render_visual(visual_data)
                # 3. Si no → intent-based chart desde demo_data (100% fiable)
                elif _charts.detect_and_render(pregunta):
                    visual_data = {"renderType": "intent_chart", "query": pregunta}

                st.session_state["sentinel_messages"].append({
                    "role":    "assistant",
                    "content": clean_text,
                    "visual":  visual_data,
                })

                # Sprint 3: actualizar memoria conversacional tras respuesta LLM
                _mem.update_state(pregunta)

                # Sprint 5/Legal: trust badge + marco normativo bajo la respuesta LLM
                _legal_refs_llm = find_legal_refs(pregunta)
                _trust_res_llm  = calculate_trust(
                    context_from_query(pregunta),
                    legal_boost=bool(_legal_refs_llm),
                )
                trust_badge(_trust_res_llm, _legal_refs_llm)
                if _legal_refs_llm:
                    legal_card(_legal_refs_llm)

                # Fase 3: coherencia_card para queries de viabilidad/simulación/evaluación
                if detect_coherencia_intent(pregunta):
                    _coh_res = _coh_eval(
                        query      = pregunta,
                        data       = data,
                        legal_refs = _legal_refs_llm,
                        territory  = _mem.get_context().get("ultima_parroquia"),
                    )
                    coherencia_card(_coh_res)

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
                if "API Key de Anthropic" in err or "authentication" in err.lower():
                    error_msg = (
                        "⚠️ **API Key de Anthropic inválida.** "
                        "Configura `ANTHROPIC_API_KEY` en Streamlit Secrets o como variable de entorno."
                    )
                elif "Límite de Claude" in err or "rate_limit" in err.lower() or "overloaded" in err.lower():
                    error_msg = "⚠️ **Claude temporalmente ocupado.** Espera unos segundos e intenta de nuevo."
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
            visual = msg.get("visual")
            if visual:
                if visual.get("renderType") == "intent_chart":
                    _charts.detect_and_render(visual["query"])
                else:
                    render_visual(visual)


def _render_suggestions() -> None:
    st.caption("💬 ANÁLISIS DE TEXTO")
    sugerencias_texto = [
        "¿Qué debería hacer el GAD para alcanzar la meta de 70 al cierre 2026?",
        "¿Cómo afecta la paradoja democrática de Isabel Muentes a la gobernanza?",
        "¿Qué riesgos territoriales tiene mayor prioridad según el PDOT?",
        "¿Cuáles son las potencialidades económicas más relevantes del cantón?",
    ]
    cols_t = st.columns(2)
    for i, sug in enumerate(sugerencias_texto):
        with cols_t[i % 2]:
            if st.button(f"💬 {sug}", key=f"sug_t_{i}", use_container_width=True):
                st.session_state["sentinel_messages"].append({"role": "user", "content": sug})
                st.rerun()

    st.caption("📊 VISUALIZACIONES (Sentinel v1.1)")
    sugerencias_viz = [
        "Muéstrame el NBI por parroquia en gráfico",
        "Compara la inversión per cápita entre las 7 parroquias",
        "Grafica la evolución del ICGI-T de 2023 a Q1-2026",
        "Muéstrame los índices complementarios del cantón en tabla",
    ]
    cols_v = st.columns(2)
    for i, sug in enumerate(sugerencias_viz):
        with cols_v[i % 2]:
            if st.button(f"📊 {sug}", key=f"sug_v_{i}", use_container_width=True):
                st.session_state["sentinel_messages"].append({"role": "user", "content": sug})
                st.rerun()


def _get_api_key() -> str:
    """
    Obtiene Anthropic API Key en orden de prioridad:
    1. session_state (ingresada temporalmente en UI)
    2. st.secrets["ANTHROPIC_API_KEY"] (recomendado para Streamlit Cloud)
    3. Variable de entorno ANTHROPIC_API_KEY
    """
    if "temp_claude_key" in st.session_state:
        return st.session_state["temp_claude_key"]
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY", "")
