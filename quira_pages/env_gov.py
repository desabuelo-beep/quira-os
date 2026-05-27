"""
QUIRA Intelligence — Ambiente 🏛 GOV
El producto hoy. Monitoreo institucional preventivo para GADs del Ecuador.

6 tabs:
  Estado Municipal     → ICPI, TGI 5D, clasificación, riesgo SAT
  RC-M Longitudinal    → Tabla RC-M + gráfico tendencia ICPI
  Alertas SAT          → SAT activas, triple ancla, protocolo
  Comparación          → Diff Engine: MEJORA / DETERIORO / RUPTURA / RECUPERACIÓN
  Ejecución Presup.    → D3 Ti, devengado, Holding consolidado
  Trazabilidad         → Fuentes, reliability scores, cadena evidencial

Doctrina: el dashboard es la interfaz. El ciclo mensual es el producto.
Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

_MUNICIPIO = "130801"

# ── Colores doctrinales ────────────────────────────────────────────────────────
_RIESGO_COLOR = {
    "BAJO":     "#22C55E",
    "MEDIO":    "#F59E0B",
    "ALTO":     "#F97316",
    "CRÍTICO":  "#EF4444",
    "CRITICO":  "#EF4444",
}
_ICPI_COLOR = {
    "Excelente":               "#22C55E",
    "Saludable":               "#84CC16",
    "En Construcción":         "#F59E0B",
    "Transición con Riesgos":  "#FFB800",
    "Ruptura Sistémica":       "#EF4444",
}
_DIM_LABELS = {
    "d1": ("D1", "Legalidad y Coherencia"),
    "d2": ("D2", "Fidelidad de Planificación"),
    "d3": ("D3", "Ejecución Presupuestaria"),
    "d4": ("D4", "Equidad Territorial"),
    "d5": ("D5", "Capacidad Institucional"),
}
_SAT_CATALOG_NAMES = {
    "SAT-0":    "Coherencia POA-PAC",
    "SAT-I":    "Fragmentación Selectiva",
    "SAT-II":   "Reforma Significativa Tardía",
    "SAT-III":  "Parálisis Presupuestaria",
    "SAT-IV":   "Alerta Fiscal COOTAD",
    "SAT-V":    "Brecha Compromiso CPCCS",
    "SAT-VI":   "Desvío Presupuesto Participativo",
    "SAT-VII":  "Pulso Sináptico",
    "SAT-VIII": "Equidad Territorial",
}
_SAT_BASE_LEGAL = {
    "SAT-0":    "LOSNCP Art. 22",
    "SAT-I":    "COPFP Art. 54",
    "SAT-II":   "COPFP Art. 115",
    "SAT-III":  "COPFP Art. 113",
    "SAT-IV":   "COOTAD Art. 192",
    "SAT-V":    "COOTAD Art. 302",
    "SAT-VI":   "COOTAD Art. 238",
    "SAT-VII":  "—",
    "SAT-VIII": "COOTAD Art. 238 / 247",
}
_SAT_TIPO_COLOR = {
    "critica":      "#EF4444",
    "crítica":      "#EF4444",
    "alerta":       "#F97316",
    "preventiva":   "#F59E0B",
    "legal":        "#DC2626",
    "informacional":"#64748B",
}


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _load() -> tuple[dict | None, dict | None]:
    """Carga snapshot activo con cache de 5 minutos (evita re-lectura Supabase)."""
    from utils.cache_quira import cargar_snapshot
    return cargar_snapshot(municipio_code=_MUNICIPIO)


def _icpi_color(nivel: str) -> str:
    return _ICPI_COLOR.get(nivel, "#94A3B8")


def _riesgo_color(riesgo: str) -> str:
    return _RIESGO_COLOR.get(riesgo.upper() if riesgo else "", "#94A3B8")


def _badge_html(text: str, color: str) -> str:
    return (
        f'<span style="background:{color}22;color:{color};border:1px solid {color}44;'
        f'border-radius:4px;padding:2px 8px;font-size:11px;font-weight:700;'
        f'letter-spacing:.05em">{text}</span>'
    )


def _metric_card(label: str, value: str, color: str = "#00D4FF", sub: str = "") -> str:
    sub_html = f'<div style="font-size:10px;color:rgba(255,255,255,.4);margin-top:2px">{sub}</div>' if sub else ""
    return f"""
<div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
            border-radius:10px;padding:14px 16px">
  <div style="font-size:10px;color:rgba(255,255,255,.4);letter-spacing:.06em;
              text-transform:uppercase;margin-bottom:4px">{label}</div>
  <div style="font-size:1.6rem;font-weight:800;color:{color};line-height:1">{value}</div>
  {sub_html}
</div>"""


def _no_snapshot_notice() -> None:
    st.warning(
        "⚠️ No hay snapshot activo para Montecristi. "
        "Ejecuta el pipeline desde **Ops → Pipeline** para generar los datos institucionales."
    )


# ══════════════════════════════════════════════════════════════════════════════
# Tab 1 — Estado Municipal
# ══════════════════════════════════════════════════════════════════════════════

def _tab_estado(snap: dict, meta: dict | None) -> None:
    if not snap:
        _no_snapshot_notice()
        return

    # Valores clave — tolerante a ambos formatos de snapshot (pipeline + Gold Master)
    icpi_pct  = (snap.get("icpi") or {}).get("global_pct") or snap.get("tgi", {}).get("score")
    nivel     = ((snap.get("icpi") or {}).get("clasificacion")
                 or snap.get("tgi", {}).get("clasificacion", "—"))
    tgi_score = snap.get("tgi", {}).get("score") or icpi_pct
    sat_obj   = snap.get("sat") or {}
    riesgo    = sat_obj.get("clasif_riesgo") or sat_obj.get("riesgo") or "—"
    n_activas = len(sat_obj.get("activas") or sat_obj.get("alertas_activas") or [])
    fecha     = snap.get("_meta", {}).get("fecha_corte", "—")
    version   = snap.get("_meta", {}).get("version_excel", "—")

    # ── Header ──
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
    <span style="font-size:1.2rem;font-weight:800;color:#E2E8F0">Estado Institucional</span>
    <span style="font-size:9px;color:rgba(255,255,255,.3);margin-left:4px">Corte {fecha}</span>
</div>
    """, unsafe_allow_html=True)

    # ── Métricas principales ──
    c1, c2, c3, c4 = st.columns(4)
    icpi_color = _icpi_color(nivel) if nivel != "—" else "#94A3B8"
    riesgo_color = _riesgo_color(riesgo)

    with c1:
        st.markdown(_metric_card(
            "ICPI Global",
            f"{icpi_pct:.1f}%" if icpi_pct is not None else "—",
            icpi_color,
            nivel,
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(_metric_card(
            "TGI Score",
            f"{tgi_score:.1f}%" if tgi_score is not None else "—",
            "#00D4FF",
            "TGI Territorial",
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(_metric_card(
            "Riesgo SAT",
            riesgo,
            riesgo_color,
            f"{n_activas} alerta{'s' if n_activas != 1 else ''} activa{'s' if n_activas != 1 else ''}",
        ), unsafe_allow_html=True)
    with c4:
        traz = snap.get("traceability_score")
        st.markdown(_metric_card(
            "Trazabilidad",
            f"{traz:.0%}" if traz is not None else "—",
            "#22C55E" if traz and traz >= 0.85 else "#F59E0B",
            version,
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TGI 5 dimensiones ──
    st.markdown("**TGI — 5 Dimensiones**")
    tgi = snap.get("tgi", {})
    dims_data = []
    for key, (cod, nombre) in _DIM_LABELS.items():
        dim = tgi.get(key) or {}
        val = dim.get("valor") if isinstance(dim, dict) else None
        peso = dim.get("peso", 0) if isinstance(dim, dict) else 0
        dims_data.append((cod, nombre, val, peso))

    for cod, nombre, val, peso in dims_data:
        col_l, col_r = st.columns([3, 1])
        val_str = f"{val:.1f}%" if val is not None else "—"
        color = ("#22C55E" if val and val >= 70 else
                 "#F59E0B" if val and val >= 50 else
                 "#EF4444" if val is not None else "#64748B")
        with col_l:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;padding:4px 0">'
                f'<span style="font-size:10px;font-weight:700;color:#00D4FF;min-width:28px">{cod}</span>'
                f'<span style="font-size:12px;color:#E2E8F0">{nombre}</span>'
                f'<span style="font-size:10px;color:rgba(255,255,255,.35)">'
                f'({int(peso*100)}% peso)</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if val is not None:
                st.progress(min(val / 100, 1.0))
        with col_r:
            st.markdown(
                f'<div style="text-align:right;padding:4px 0;font-size:14px;'
                f'font-weight:800;color:{color}">{val_str}</div>',
                unsafe_allow_html=True,
            )

    # ── Nota doctrinal ──
    st.markdown("""
<div style="margin-top:16px;padding:10px 14px;background:rgba(0,212,255,.05);
            border-left:3px solid rgba(0,212,255,.3);border-radius:0 8px 8px 0;
            font-size:11px;color:rgba(255,255,255,.55)">
    <strong style="color:rgba(0,212,255,.8)">Doctrina TGI:</strong>
    D1(20%) + D2(20%) + D3(25%) + D4(25%) + D5(10%)
    — Fuente: Gold Master Excel canónico · Validación analítica Dylus Lab
</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 2 — RC-M Longitudinal
# ══════════════════════════════════════════════════════════════════════════════

def _tab_rcm() -> None:
    try:
        from app.services.longitudinal_engine import get_longitudinal_summary
        summary = get_longitudinal_summary(_MUNICIPIO)
    except Exception as exc:
        st.error(f"No se pudo cargar el historial longitudinal: {exc}")
        return

    if summary.get("error"):
        st.info(
            "📭 Aún no hay historial longitudinal. El RC-M se construirá a partir del "
            "segundo snapshot mensual ejecutado. Ejecuta el pipeline mensualmente desde **Ops → Pipeline**."
        )
        return

    n = summary.get("n_periodos", 0)
    trend = summary.get("icpi_trend", "INSUFICIENTE_DATOS")
    last_icpi = summary.get("last_icpi_pct")
    last_riesgo = summary.get("last_riesgo", "—")
    rcm_table = summary.get("rcm_table", [])
    icpi_series = summary.get("icpi_series", [])

    # ── Header métricas ──
    c1, c2, c3 = st.columns(3)
    trend_colors = {"MEJORA": "#22C55E", "DETERIORO": "#EF4444", "ESTABLE": "#F59E0B",
                    "INSUFICIENTE_DATOS": "#64748B"}
    with c1:
        st.markdown(_metric_card("Períodos", str(n), "#00D4FF", "historial RC-M"), unsafe_allow_html=True)
    with c2:
        st.markdown(_metric_card(
            "Tendencia ICPI", trend,
            trend_colors.get(trend, "#94A3B8"),
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(_metric_card(
            "Último ICPI",
            f"{last_icpi:.1f}%" if last_icpi is not None else "—",
            _riesgo_color(last_riesgo),
            f"Riesgo {last_riesgo}",
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabla RC-M ──
    if rcm_table:
        st.markdown("**Tabla RC-M Canónica**")
        import pandas as pd
        df = pd.DataFrame(rcm_table)
        rename = {
            "periodo": "Período",
            "icpi_pct": "ICPI (%)",
            "d3_ti_pct": "D3 Ti (%)",
            "sat_iv": "SAT-IV",
            "riesgo": "Riesgo",
        }
        cols = [c for c in rename if c in df.columns]
        df_show = df[cols].rename(columns=rename)

        def _style_riesgo(v):
            colors = {"ALTO": "#F97316", "CRÍTICO": "#EF4444", "MEDIO": "#F59E0B",
                      "BAJO": "#22C55E"}
            c = colors.get(str(v).upper(), "")
            return f"color:{c};font-weight:700" if c else ""

        def _style_sat_iv(v):
            return "color:#EF4444;font-weight:700" if str(v) == "ACTIVA" else "color:#94A3B8"

        try:
            styled = (df_show.style
                      .applymap(_style_riesgo, subset=["Riesgo"])
                      .applymap(_style_sat_iv, subset=["SAT-IV"])
                      .format({"ICPI (%)": "{:.1f}", "D3 Ti (%)": "{:.2f}"}, na_rep="—"))
            st.dataframe(styled, use_container_width=True, hide_index=True)
        except Exception:
            st.dataframe(df_show, use_container_width=True, hide_index=True)

    # ── Gráfico ICPI ──
    if len(icpi_series) >= 2:
        st.markdown("**Evolución ICPI**")
        try:
            import plotly.graph_objects as go
            periodos = [p for p, _ in icpi_series]
            valores = [v for _, v in icpi_series]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=periodos, y=valores, mode="lines+markers",
                line=dict(color="#00D4FF", width=2),
                marker=dict(size=8, color="#00D4FF"),
                name="ICPI",
            ))
            fig.add_hline(y=65, line_dash="dot", line_color="#22C55E",
                          annotation_text="Meta 65%", annotation_position="bottom right")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0", size=11),
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(gridcolor="rgba(255,255,255,.06)"),
                yaxis=dict(gridcolor="rgba(255,255,255,.06)", range=[0, 100]),
                showlegend=False, height=260,
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as exc:
            st.warning(f"Gráfico no disponible: {exc}")

    st.markdown("""
<div style="margin-top:12px;padding:10px 14px;background:rgba(0,212,255,.05);
            border-left:3px solid rgba(0,212,255,.3);border-radius:0 8px 8px 0;
            font-size:11px;color:rgba(255,255,255,.55)">
    <strong style="color:rgba(0,212,255,.8)">RC-M:</strong>
    Registro Canónico Mensual — trayectoria longitudinal del ICPI, D3 y SAT.
    Detecta deterioro, mejora y reincidencia a lo largo del tiempo.
</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 3 — Alertas SAT
# ══════════════════════════════════════════════════════════════════════════════

def _tab_sat(snap: dict | None) -> None:
    if not snap:
        _no_snapshot_notice()
        return

    sat = snap.get("sat") or {}
    alertas = sat.get("alertas") or []
    activas_codes = set(sat.get("activas") or sat.get("alertas_activas") or [])
    riesgo = sat.get("clasif_riesgo") or sat.get("riesgo") or "—"

    # ── Nivel riesgo global ──
    riesgo_color = _riesgo_color(riesgo)
    st.markdown(
        f'<div style="margin-bottom:16px">'
        f'{_badge_html(f"RIESGO PONDERADO: {riesgo}", riesgo_color)}'
        f'&nbsp;&nbsp;'
        f'{_badge_html(f"{len(activas_codes)} SEÑALES ACTIVAS", "#EF4444" if activas_codes else "#22C55E")}'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not alertas and not activas_codes:
        st.info(
            "📭 No hay datos SAT en el snapshot activo. "
            "Ejecuta el pipeline con evaluación SAT para generar alertas."
        )
        # Mostrar qué se evaluaría
        st.markdown("**Catálogo SAT — Señales que se evaluarán:**")
        for cod, nombre in _SAT_CATALOG_NAMES.items():
            ley = _SAT_BASE_LEGAL.get(cod, "—")
            st.markdown(
                f'<div style="padding:6px 0;border-bottom:1px solid rgba(255,255,255,.06)'
                f';font-size:12px">'
                f'<span style="color:#00D4FF;font-weight:700">{cod}</span>'
                f' — {nombre}'
                f'<span style="color:rgba(255,255,255,.35);font-size:10px;margin-left:8px">{ley}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        return

    # ── Alertas activas primero, luego el resto ──
    def _sort_key(a: dict) -> int:
        return 0 if a.get("estado") == "ACTIVA" else 1

    for alerta in sorted(alertas, key=_sort_key):
        codigo = alerta.get("codigo", "?")
        nombre = alerta.get("nombre") or _SAT_CATALOG_NAMES.get(codigo, codigo)
        estado = alerta.get("estado", "—")
        tipo   = alerta.get("tipo", "")
        ley    = alerta.get("base_legal_art") or _SAT_BASE_LEGAL.get(codigo, "—")
        desc_legal = alerta.get("base_legal_desc", "")
        doctrinal  = alerta.get("base_doctrinal", "")
        val_obs    = alerta.get("valor_observado")

        is_activa = estado == "ACTIVA"
        card_color = "#EF444433" if is_activa else "rgba(255,255,255,.03)"
        border_color = "#EF4444" if is_activa else "rgba(255,255,255,.08)"
        tipo_color = _SAT_TIPO_COLOR.get(tipo.lower(), "#64748B")

        val_str = ""
        if val_obs is not None:
            val_str = (f'<span style="font-size:11px;color:rgba(255,255,255,.5);margin-left:8px">'
                       f'Observado: {val_obs}</span>')

        with st.expander(
            f"{'🔴' if is_activa else '⚪'} {codigo} — {nombre}",
            expanded=is_activa,
        ):
            st.markdown(
                f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">'
                f'{_badge_html(estado, "#EF4444" if is_activa else "#64748B")}'
                f'{_badge_html(tipo.upper() if tipo else "—", tipo_color)}'
                f'{_badge_html(ley, "#00D4FF")}'
                f'</div>',
                unsafe_allow_html=True,
            )
            if desc_legal:
                st.markdown(
                    f'<div style="font-size:11px;color:rgba(255,255,255,.6);margin-bottom:4px">'
                    f'<strong>Base legal:</strong> {desc_legal}</div>',
                    unsafe_allow_html=True,
                )
            if doctrinal:
                st.markdown(
                    f'<div style="font-size:11px;color:rgba(255,255,255,.6);">'
                    f'<strong>Base doctrinal:</strong> {doctrinal}</div>',
                    unsafe_allow_html=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# Tab 4 — Comparación de Períodos
# ══════════════════════════════════════════════════════════════════════════════

def _tab_diff() -> None:
    st.markdown("**Diff Engine — Comparación entre Períodos**")

    try:
        from utils.cache_quira import cargar_historial_snapshots
        history = cargar_historial_snapshots(municipio_code=_MUNICIPIO, limite=12)
    except Exception as exc:
        st.error(f"Error al cargar historial: {exc}")
        return

    if len(history) < 2:
        st.info(
            "📭 Se necesitan al menos **2 períodos** en el historial para comparar. "
            "El Diff Engine se activará con el segundo snapshot mensual."
        )
        return

    # Selector de períodos
    from app.services.longitudinal_engine import _period_label, _get_nested  # type: ignore
    labels = [_period_label(s) for s in history]

    col1, col2 = st.columns(2)
    with col1:
        idx_a = st.selectbox("Período base (A)", range(len(labels)),
                             format_func=lambda i: labels[i], index=0)
    with col2:
        idx_b = st.selectbox("Período comparado (B)", range(len(labels)),
                             format_func=lambda i: labels[i], index=min(1, len(labels)-1))

    if idx_a == idx_b:
        st.warning("Selecciona dos períodos distintos para comparar.")
        return

    snap_a = history[idx_a]
    snap_b = history[idx_b]

    # Historial D3 previo para detección SAT-III
    d3_history = []
    for s in history[:min(idx_b, len(history))]:
        raw = _get_nested(s, "financiero.isp_salud_presup")
        if raw is not None:
            try:
                d3_history.append(float(raw) * 100)
            except (ValueError, TypeError):
                pass

    try:
        from app.services.snapshot_diff import compare_snapshots
        result = compare_snapshots(snap_a, snap_b, historial_d3=d3_history or None)
    except Exception as exc:
        st.error(f"Error en Diff Engine: {exc}")
        return

    # ── Clasificación ──
    clasif = result.clasificacion
    clasif_colors = {
        "MEJORA":              "#22C55E",
        "DETERIORO":           "#EF4444",
        "ESTABLE":             "#94A3B8",
        "RUPTURA":             "#DC2626",
        "RECUPERACION":        "#84CC16",
        "RECUPERACIÓN":        "#84CC16",
        "REINCIDENCIA":        "#F97316",
        "INSUFICIENTE_DATOS":  "#64748B",
    }
    c_color = clasif_colors.get(clasif, "#94A3B8")
    st.markdown(
        f'<div style="text-align:center;margin:16px 0">'
        f'<span style="font-size:1.8rem;font-weight:900;color:{c_color}">'
        f'{clasif}</span></div>',
        unsafe_allow_html=True,
    )

    # ── Delta ICPI ──
    delta = result.delta_icpi
    if delta is not None:
        sign = "+" if delta >= 0 else ""
        d_color = "#22C55E" if delta > 0 else "#EF4444" if delta < 0 else "#94A3B8"
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(_metric_card("ICPI (A)", f"{result.icpi_a:.1f}%" if result.icpi_a is not None else "—", "#94A3B8"), unsafe_allow_html=True)
        with c2:
            st.markdown(_metric_card("ICPI (B)", f"{result.icpi_b:.1f}%" if result.icpi_b is not None else "—", "#00D4FF"), unsafe_allow_html=True)
        with c3:
            st.markdown(_metric_card("Delta ICPI", f"{sign}{delta:.1f}pp", d_color), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Campos cambiados ──
    if result.campos_cambiados:
        st.markdown(f"**{len(result.campos_cambiados)} campos cambiados**")
        for fc in result.campos_cambiados[:10]:
            dir_color = "#22C55E" if fc.direccion == "MEJORA" else "#EF4444" if fc.direccion == "DETERIORO" else "#94A3B8"
            st.markdown(
                f'<div style="padding:4px 0;font-size:11px;border-bottom:1px solid rgba(255,255,255,.05)">'
                f'<span style="color:#00D4FF">{fc.campo}</span>'
                f' → <span style="color:{dir_color}"><strong>{fc.direccion}</strong></span>'
                f'  <span style="color:rgba(255,255,255,.4)">{fc.valor_a} → {fc.valor_b}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── SAT-III reincidencia ──
    if result.sat_reincidencia:
        st.error("🔴 SAT-III REINCIDENTE — D3 < 60% por 3 períodos consecutivos (COPFP Art. 113)")

    # ── Notas ──
    if result.notas:
        with st.expander("📋 Notas del análisis"):
            for nota in result.notas:
                st.markdown(f"• {nota}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 5 — Ejecución Presupuestaria
# ══════════════════════════════════════════════════════════════════════════════

def _tab_ejecucion(snap: dict | None) -> None:
    if not snap:
        _no_snapshot_notice()
        return

    fin = snap.get("financiero") or {}
    tgi = snap.get("tgi") or {}
    d3  = tgi.get("d3") or {}

    # D3 Ti — intentar múltiples rutas
    d3_val = d3.get("valor") or fin.get("ti_2025_pct")
    d3_raw = fin.get("ti_2026_raw_pct")
    d3_norm = fin.get("ti_2026_normalizada_pct")
    fecha_corte = fin.get("corte_datos", snap.get("_meta", {}).get("fecha_corte", "—"))

    # Consolidado Holding
    h90 = fin.get("h90_consolidado") or {}

    st.markdown("**Ejecución Presupuestaria — D3 Territorial**")

    c1, c2, c3 = st.columns(3)
    d3_color = ("#22C55E" if d3_val and d3_val >= 70 else
                "#F59E0B" if d3_val and d3_val >= 50 else
                "#EF4444" if d3_val is not None else "#94A3B8")
    with c1:
        st.markdown(_metric_card("D3 Ti 2025", f"{d3_val:.1f}%" if d3_val is not None else "—",
                                 d3_color, "Grupos G71-78 eSIGEF"), unsafe_allow_html=True)
    with c2:
        st.markdown(_metric_card("D3 Ti Q1-2026 (raw)", f"{d3_raw:.2f}%" if d3_raw is not None else "—",
                                 "#F97316", "Sin normalizar"), unsafe_allow_html=True)
    with c3:
        st.markdown(_metric_card("D3 Ti Q1-2026 (norm)", f"{d3_norm:.2f}%" if d3_norm is not None else "—",
                                 "#F59E0B", "Fondos bloqueados ajustados"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Holding consolidado ──
    if h90:
        st.markdown(f"**Holding Municipal Consolidado** — Corte {fecha_corte}")

        entities = [
            ("GAD Municipal",  h90.get("gad_codificado_vigente_2026"),   h90.get("gad_devengado_q1"),   h90.get("gad_ti_q1_pct")),
            ("Patronato",      h90.get("patronato_codificado"),           h90.get("patronato_devengado_q1"), h90.get("patronato_ti_q1_pct")),
            ("EP Aseo",        h90.get("ep_aseo_codificado"),             h90.get("ep_aseo_devengado_q1"),   h90.get("ep_aseo_ti_q1_pct")),
            ("Bomberos",       h90.get("bomberos_codificado"),            h90.get("bomberos_devengado_q1"),  h90.get("bomberos_ti_q1_pct")),
        ]
        holding_cod  = h90.get("holding_total_codificado")
        holding_dev  = h90.get("holding_total_devengado_q1")
        holding_ti   = h90.get("holding_ti_q1_pct")

        for entidad, cod, dev, ti in entities:
            if cod is None:
                continue
            ti_color = ("#22C55E" if ti and ti >= 70 else
                        "#F59E0B" if ti and ti >= 40 else
                        "#EF4444" if ti is not None else "#94A3B8")
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:8px 0;border-bottom:1px solid rgba(255,255,255,.06)">'
                f'<span style="font-size:12px;color:#E2E8F0;min-width:120px">{entidad}</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,.45)">'
                f'Cod: ${cod:,.0f}</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,.45)">'
                f'Dev: ${dev:,.0f}</span>'
                f'<span style="font-size:13px;font-weight:700;color:{ti_color}">'
                f'{ti:.1f}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            ) if dev is not None and ti is not None else None

        if holding_ti is not None:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'margin-top:4px;padding:8px 0;background:rgba(0,212,255,.06);'
                f'border-radius:6px;padding:8px 10px">'
                f'<span style="font-size:13px;font-weight:700;color:#00D4FF">HOLDING TOTAL</span>'
                f'<span style="font-size:11px;color:rgba(255,255,255,.45)">'
                f'Dev: ${holding_dev:,.0f}</span>'
                f'<span style="font-size:14px;font-weight:800;color:#F59E0B">'
                f'{holding_ti:.2f}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Fondos bloqueados ──
    fondos = fin.get("fondos_bloqueados_est")
    if fondos:
        st.markdown(
            f'<div style="margin-top:12px;padding:10px 14px;background:rgba(239,68,68,.05);'
            f'border-left:3px solid rgba(239,68,68,.4);border-radius:0 8px 8px 0;'
            f'font-size:11px;color:rgba(255,255,255,.6)">'
            f'<strong style="color:#EF4444">Fondos bloqueados estimados:</strong> '
            f'${fondos:,.0f} — {fin.get("fondos_bloqueados_detalle", "")}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Referencia doctrinal D3 ──
    st.markdown("""
<div style="margin-top:12px;padding:10px 14px;background:rgba(0,212,255,.05);
            border-left:3px solid rgba(0,212,255,.3);border-radius:0 8px 8px 0;
            font-size:11px;color:rgba(255,255,255,.55)">
    <strong style="color:rgba(0,212,255,.8)">SAT-III:</strong>
    Si D3 Ti &lt; 60% por 3 períodos consecutivos → Parálisis Presupuestaria (COPFP Art. 113).
    Umbral de alerta: 60%. Peso D3 en TGI: 25%.
</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 6 — Trazabilidad
# ══════════════════════════════════════════════════════════════════════════════

def _tab_trazabilidad(snap: dict | None) -> None:
    if not snap:
        _no_snapshot_notice()
        return

    sources = snap.get("sources") or {}
    traz_score = snap.get("traceability_score")
    cov_score  = snap.get("coverage_score")
    src_conf   = snap.get("source_confidence")
    version    = snap.get("_meta", {}).get("version_excel", "—")
    fecha_corte = snap.get("_meta", {}).get("fecha_corte", "—")
    gm_ok      = snap.get("_meta", {}).get("gold_master_ok", False)

    st.markdown("**Trazabilidad Evidencial — Fuentes Institucionales**")

    c1, c2, c3 = st.columns(3)
    with c1:
        t_color = "#22C55E" if traz_score and traz_score >= 0.85 else "#F59E0B"
        st.markdown(_metric_card("Trazabilidad", f"{traz_score:.0%}" if traz_score else "—",
                                 t_color, "score ponderado"), unsafe_allow_html=True)
    with c2:
        st.markdown(_metric_card("Cobertura", f"{cov_score:.0%}" if cov_score else "—",
                                 "#00D4FF", "dimensiones con datos"), unsafe_allow_html=True)
    with c3:
        st.markdown(_metric_card("Conf. Fuentes", f"{src_conf:.0%}" if src_conf else "—",
                                 "#84CC16", "weighted reliability"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fuentes del snapshot ──
    static_sources = {
        "gold_master": {"name": "Gold Master Excel",   "reliability": 0.99, "icon": "📋"},
        "dpe":         {"name": "DPE API",             "reliability": 0.95, "icon": "📊"},
        "sercop":      {"name": "SERCOP OCDS",         "reliability": 0.95, "icon": "📝"},
        "cpccs":       {"name": "CPCCS RdC",           "reliability": 0.80, "icon": "🏛"},
    }

    st.markdown("**Cadena Evidencial por Fuente**")
    for src_key, src_meta in static_sources.items():
        snap_src = sources.get(src_key) or {}
        status = snap_src.get("status", "—")
        rel = snap_src.get("reliability") or src_meta["reliability"]
        error = snap_src.get("error")

        s_color = "#22C55E" if status == "ok" else "#F97316" if status else "#64748B"
        r_color = "#22C55E" if rel >= 0.90 else "#F59E0B" if rel >= 0.70 else "#EF4444"

        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0;'
            f'border-bottom:1px solid rgba(255,255,255,.06)">'
            f'<span style="font-size:16px">{src_meta["icon"]}</span>'
            f'<div style="flex:1">'
            f'<div style="font-size:12px;color:#E2E8F0;font-weight:600">{src_meta["name"]}</div>'
            f'{"<div style=\"font-size:10px;color:#EF4444\">" + str(error) + "</div>" if error else ""}'
            f'</div>'
            f'<span style="font-size:11px;color:{s_color};font-weight:700">{status.upper() if status else "—"}</span>'
            f'<span style="font-size:12px;color:{r_color};font-weight:800;min-width:40px;'
            f'text-align:right">{rel:.0%}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── Gold Master info ──
    st.markdown(
        f'<div style="margin-top:16px;padding:10px 14px;'
        f'background:rgba({"0,212,255" if gm_ok else "239,68,68"},.05);'
        f'border-left:3px solid rgba({"0,212,255" if gm_ok else "239,68,68"},.4);'
        f'border-radius:0 8px 8px 0;font-size:11px;color:rgba(255,255,255,.6)">'
        f'<strong style="color:rgba({"0,212,255" if gm_ok else "239,68,68"},.9)">'
        f'Gold Master:</strong> {version} · Corte {fecha_corte} · '
        f'{"✅ Verificado" if gm_ok else "⚠️ No verificado"}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Dimensiones faltantes ──
    missing = snap.get("missing_dimensions") or []
    if missing:
        st.warning(f"⚠️ Dimensiones sin datos: {', '.join(missing)}")


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    snap, meta = _load()

    t1, t2, t3, t4, t5, t6 = st.tabs([
        "🏛 Estado Municipal",
        "📈 RC-M Longitudinal",
        "🚨 Alertas SAT",
        "🔍 Comparación",
        "💰 Ejecución Presup.",
        "🔗 Trazabilidad",
    ])

    with t1:
        _tab_estado(snap, meta)
    with t2:
        _tab_rcm()
    with t3:
        _tab_sat(snap)
    with t4:
        _tab_diff()
    with t5:
        _tab_ejecucion(snap)
    with t6:
        _tab_trazabilidad(snap)
