"""
QUIRA OS — Análisis de Brechas (d06 · pestaña Brechas)
6 vectores causales REALES desde el snapshot local · lenguaje de gobernanza (frontera Regla 2).
Cero demo_data · cero hardcodes · sin narrativa de "caída" (el corte parcial NO es comparable al cierre anual).
Dylus Lab © 2026
"""
import streamlit as st
from utils.cache_quira import cargar_gm_snapshot
from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

# Orden de despliegue + polaridad (opacidad: menor es mejor; el resto: mayor es mejor)
_VEC_ORDER   = ["isp", "ied", "igp", "ioc", "iet", "psg"]
_VEC_INVERSE = {"ioc"}


def _vec_color(key: str, val: float) -> str:
    bueno = (100 - val) if key in _VEC_INVERSE else val
    return "green" if bueno >= 55 else "amber" if bueno >= 30 else "red"


def render() -> None:
    gm        = cargar_gm_snapshot()
    show_tech = is_tecnico()

    if not gm or not gm.get("icpi"):
        st.info(
            "💡 Sin datos del período disponibles. El análisis de brechas se "
            "habilitará una vez cargada la información del corte."
        )
        return

    icpi  = gm.get("icpi", {})
    vec   = gm.get("vectores", {})
    hist  = icpi.get("historico", {})
    score = icpi.get("global_pct", 0.0)

    # ── EVOLUCIÓN: cierres anuales reales + corte parcial (sin narrativa de caída) ──
    timeline_items = [
        ("2023", hist.get("2023", 0.0), "amber", "Cierre anual"),
        ("2024", hist.get("2024", 0.0), "green", "Cierre anual"),
        ("2025", hist.get("2025", 0.0), "green", "Cierre anual"),
        ("Abril 2026", score,           "amber", "Corte parcial"),
    ]

    def _tl_item(label, val, col, nota):
        return f"""
  <div style="text-align:center;flex:1;min-width:90px">
    <div style="font-size:10px;color:var(--muted);font-weight:700;
                text-transform:uppercase;margin-bottom:6px">{label}</div>
    <div style="font-size:28px;font-weight:900;color:var(--{col});
                font-family:var(--mono);line-height:1">{val:.2f}<span style="font-size:13px">%</span></div>
    <div style="font-size:9px;color:var(--muted);margin-top:4px">{nota}</div>
    <div style="height:3px;background:var(--{col});border-radius:2px;margin-top:8px"></div>
  </div>"""

    timeline_html = f"""
<div class="card" style="margin-bottom:16px">
  <div class="card-title">📈 EVOLUCIÓN DEL CUMPLIMIENTO INSTITUCIONAL</div>
  <div style="display:flex;gap:8px;align-items:flex-end;padding:8px 0">
    {"".join(_tl_item(*t) for t in timeline_items)}
  </div>
  <div style="margin-top:14px;padding:10px 12px;background:rgba(0,212,255,.05);
              border:1px solid rgba(0,212,255,.15);border-radius:8px;
              font-size:11px;color:var(--muted);line-height:1.6">
    Los valores 2023–2025 son <strong style="color:var(--white)">cierres anuales</strong> (tendencia al alza).
    El valor de abril 2026 es un <strong style="color:var(--white)">corte parcial</strong> del año en curso:
    una lectura preliminar del avance del período, <strong style="color:var(--white)">no comparable</strong>
    con un cierre anual. Mide qué tanto se ha ejecutado a la fecha, no el total que se ejecutará en el año.
  </div>
</div>"""

    # ── 6 VECTORES CAUSALES (valores reales del snapshot · etiquetas públicas) ──
    def _vector_row(key: str) -> str:
        v     = vec.get(key, {})
        val   = v.get("valor", 0.0) or 0.0
        label = v.get("label", key)
        col   = _vec_color(key, val)
        pct   = min(val, 100)
        return f"""
  <div style="background:var(--navy-card);border:1px solid var(--divider);
              border-left:3px solid var(--{col});border-radius:10px;padding:14px 16px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <span style="font-size:12px;font-weight:700;color:var(--white)">{label}</span>
      <span style="font-size:18px;font-weight:900;color:var(--{col});font-family:var(--mono)">{val:.2f}%</span>
    </div>
    <div style="height:6px;background:var(--divider);border-radius:3px;overflow:hidden">
      <div style="height:6px;width:{pct:.0f}%;background:var(--{col});border-radius:3px"></div>
    </div>
  </div>"""

    vectores_html = f"""
<div class="card">
  <div class="card-title">🔍 VECTORES DEL CUMPLIMIENTO INSTITUCIONAL · CORTE ABRIL 2026</div>
  <div style="font-size:11px;color:var(--muted);margin-bottom:14px;padding:0 4px">
    Cada vector sale directamente de la evidencia del período. La lectura de cuál pesa más en el
    resultado la emite la capa de razonamiento de QUIRA (pendiente análisis contextual).</div>
  {"".join(_vector_row(k) for k in _VEC_ORDER)}
</div>"""

    # ── HEADER ─────────────────────────────────────────────────────────────────
    hdr = page_header(
        "② ANÁLISIS DE BRECHAS",
        "Análisis de Brechas",
        f"Cumplimiento institucional al corte de abril 2026: {score:.2f}% · {icpi.get('clasificacion', '')}",
        '<span class="badge badge-amber">Corte parcial</span>',
    )

    render_page(hdr + timeline_html + vectores_html, show_tech=show_tech, height=1100)

    # ── CTAs ───────────────────────────────────────────────────────────────────
    st.markdown("---")
    # Vectores con mayor rezago (real) para la pregunta a la IA
    rezago = sorted(
        [(vec[k].get("label", k), vec[k].get("valor", 0.0)) for k in _VEC_ORDER if k not in _VEC_INVERSE and k in vec],
        key=lambda x: x[1],
    )[:2]
    rezago_txt = " y ".join(f"{lbl.lower()} ({val:.1f}%)" for lbl, val in rezago) if rezago else "los vectores de menor avance"

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔮 Analizar con IA", use_container_width=True, type="primary", key="brecha_ia"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"Al corte de abril 2026, el cumplimiento institucional de Montecristi es {score:.1f}%. "
                f"Los vectores con mayor rezago son {rezago_txt}. "
                f"¿Cuáles son las acciones prioritarias del trimestre para fortalecerlos?"
            )
            st.rerun()
    with c2:
        if st.button("⚡ Ver pulso institucional", use_container_width=True, key="brecha_pulso"):
            st.session_state["page"] = "pulso"
            st.rerun()
    with c3:
        if st.button("🎯 Ver metas del plan cantonal", use_container_width=True, key="brecha_metas"):
            st.session_state["page"] = "metas"
            st.rerun()
