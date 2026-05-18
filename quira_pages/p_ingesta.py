"""
QUIRA OS · p_ingesta.py
Centro de Ingesta Mensual — Sprint 2.5A

Flujo:
  1. Analista sube la cédula presupuestaria (.xlsx/.xls) desde eSIGEF/LOTAIP
  2. Parser valida (G1–G5), calcula Ti mensual y totales
  3. Analista revisa los resultados y confirma ingesta a la base de datos
  4. Sistema registra SHA256, versiona si ya existe el período, actualiza historial

Fuente de datos: solo cédula real del GAD. Nada se inventa.

Sprint 2.5A · Dylus Lab © 2026
"""
from __future__ import annotations

import calendar
import io
import time

import streamlit as st
import streamlit.components.v1 as components

from quira_pages.html_engine import DEMO_CSS, page_frame
from sentinel.cedula_parser import parse_cedula, format_result, CedulaParseResult
from sentinel.db_config import db_info
from sentinel.db_ops import (
    get_existing_hashes,
    get_existing_periods,
    get_upload_history,
    get_kpi_history,
    get_last_kpi,
    get_cedulas_count,
    ingest_cedula,
)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo",    4: "Abril",
    5: "Mayo",  6: "Junio",   7: "Julio",    8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

EXTRA_CSS = """
.ing-label {
  font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--cyan);
  border-left: 3px solid var(--cyan); padding-left: 9px;
  margin-bottom: 10px;
}
.stat-num {
  font-family: var(--mono); font-size: 28px; font-weight: 800;
  color: var(--white); line-height: 1;
}
.stat-lbl {
  font-size: 10px; color: var(--muted); font-weight: 600;
  text-transform: uppercase; letter-spacing: .06em; margin-top: 4px;
}
.val-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 7px 0; border-bottom: 1px solid var(--divider);
  font-size: 12px;
}
.val-row:last-child { border-bottom: none; }
.val-label { color: var(--muted); }
.val-ok   { color: var(--green); font-weight: 700; }
.val-err  { color: var(--red);   font-weight: 700; }
.val-warn { color: var(--amber); font-weight: 700; }
.kpi-box {
  background: var(--navy-light); border: 1px solid var(--divider);
  border-radius: 10px; padding: 14px 16px; text-align: center;
}
.kpi-num {
  font-family: var(--mono); font-size: 22px; font-weight: 800;
  color: var(--cyan);
}
.kpi-lbl { font-size: 10px; color: var(--muted); margin-top: 4px; }
.hist-row { display:flex; justify-content:space-between; align-items:center;
            padding:8px 0; border-bottom:1px solid rgba(30,45,80,.5);
            font-size:12px; }
.hist-row:last-child { border-bottom:none; }
.pill {
  display:inline-block; padding:2px 8px; border-radius:6px;
  font-size:10px; font-weight:700;
}
.pill-ok   { background:rgba(0,224,150,.1); color:var(--green); }
.pill-err  { background:rgba(255,77,109,.1); color:var(--red); }
.pill-v2   { background:rgba(0,212,255,.1);  color:var(--cyan); }
"""


# ── HELPERS HTML ─────────────────────────────────────────────────────────────
def _panel_status(info: dict, n_cedulas: int, last_kpi: dict | None) -> str:
    """Panel superior: estado de la base de datos."""
    ti_val  = f"{last_kpi['ti_mensual_pct']:.1f}%" if last_kpi else "–"
    ti_mes  = f"{MESES.get(last_kpi['period_month'], '?')} {last_kpi['period_year']}" if last_kpi else "sin datos"
    db_kb   = info.get("size_kb", 0)
    n_total = info.get("uploads", 0)

    return f"""
<div class="card">
  <div class="ing-label">Estado de la base de datos</div>
  <div class="grid-4">
    <div class="kpi-box">
      <div class="kpi-num">{n_cedulas}</div>
      <div class="kpi-lbl">Cédulas ingresadas</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{ti_val}</div>
      <div class="kpi-lbl">Ti último mes ({ti_mes})</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{n_total}</div>
      <div class="kpi-lbl">Documentos totales</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{db_kb:.0f} KB</div>
      <div class="kpi-lbl">Tamaño base de datos</div>
    </div>
  </div>
</div>
"""


def _panel_validations(result: CedulaParseResult) -> str:
    """Panel de guardrails G1–G5."""
    rows = ""
    for v in result.validations:
        if v.passed:
            icon  = "✓"
            cls   = "val-ok"
            # G5 con versionado → ámbar informativo
            if v.guardrail == "G5" and "v2+" in v.mensaje:
                cls = "val-warn"
        else:
            # G4 (duplicado) no bloquea pero es advertencia
            icon = "✗" if v.guardrail != "G4" else "⚠"
            cls  = "val-err" if v.guardrail != "G4" else "val-warn"
        rows += f"""
<div class="val-row">
  <span class="val-label">{v.guardrail} · {v.mensaje[:60]}</span>
  <span class="{cls}">{icon}</span>
</div>"""
    return f"""
<div class="card">
  <div class="ing-label">Guardrails de validación</div>
  {rows}
</div>
"""


def _panel_kpis(result: CedulaParseResult, year: int, month: int) -> str:
    """Panel de indicadores calculados desde la cédula."""
    color = "#00E096" if result.ti_mensual_pct >= 60 else \
            "#FFB800" if result.ti_mensual_pct >= 40 else "#FF4D6D"

    pct_total = (result.devengado_total / result.codificado_total * 100
                 if result.codificado_total > 0 else 0)

    return f"""
<div class="card">
  <div class="ing-label">Indicadores calculados · {MESES.get(month, '?')} {year}</div>
  <div class="grid-3">
    <div class="kpi-box">
      <div class="kpi-num" style="color:{color}">{result.ti_mensual_pct:.1f}%</div>
      <div class="kpi-lbl">Ti mensual (Dev.Inv / Cod.Inv)</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">${result.devengado_inv:,.0f}</div>
      <div class="kpi-lbl">Devengado Inversión (Gr. 7+8)</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">${result.codificado_inv:,.0f}</div>
      <div class="kpi-lbl">Codificado Inversión</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">${result.codificado_total:,.0f}</div>
      <div class="kpi-lbl">Codificado total</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">${result.devengado_total:,.0f}</div>
      <div class="kpi-lbl">Devengado total</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{pct_total:.1f}%</div>
      <div class="kpi-lbl">Ejecución total</div>
    </div>
  </div>
  <div style="margin-top:10px;font-size:11px;color:var(--muted)">
    Hoja detectada: <b style="color:var(--white)">{result.sheet_name}</b> ·
    {result.total_rows} filas de datos ·
    SHA256: <span style="font-family:var(--mono);font-size:10px">{result.sha256[:20]}…</span>
  </div>
</div>
"""


def _panel_history(history: list[dict], kpis: list[dict]) -> str:
    """Panel de historial de cédulas + Ti por mes."""
    # Build Ti lookup
    ti_lookup = {(k["period_year"], k["period_month"]): k["ti_mensual_pct"] for k in kpis}

    if not history:
        return """
<div class="card">
  <div class="ing-label">Historial de cédulas</div>
  <div style="color:var(--muted);font-size:13px;text-align:center;padding:20px 0">
    No hay cédulas registradas todavía
  </div>
</div>
"""
    rows = ""
    for h in history[:10]:
        mes_str  = f"{MESES.get(h.get('period_month'), '?')[:3]} {h.get('period_year', '–')}"
        version  = h.get("version", 1)
        status   = h.get("validation_status", "")
        pill_cls = "pill-ok" if status == "OK" else "pill-err"
        v_cls    = "pill-v2" if version > 1 else ""
        v_str    = f'<span class="pill {v_cls}">v{version}</span>' if version > 1 else ""
        ti_val   = ti_lookup.get((h.get("period_year"), h.get("period_month")))
        ti_str   = f"Ti {ti_val:.1f}%" if ti_val is not None else ""
        fname    = h.get("file_name", "–")[:32]
        ts       = h.get("uploaded_at", "–")[:16]

        rows += f"""
<div class="hist-row">
  <div>
    <b style="color:var(--white)">{mes_str}</b> {v_str}
    <span style="color:var(--muted);margin-left:8px">{fname}</span>
  </div>
  <div style="display:flex;gap:8px;align-items:center">
    <span style="color:var(--cyan);font-family:var(--mono);font-size:11px">{ti_str}</span>
    <span class="pill {pill_cls}">{status}</span>
    <span style="color:var(--muted);font-size:10px">{ts}</span>
  </div>
</div>"""

    return f"""
<div class="card">
  <div class="ing-label">Historial de cédulas ({len(history)} registros)</div>
  {rows}
</div>
"""


def _build_status_html(info: dict, n_cedulas: int, last_kpi: dict | None,
                       history: list[dict], kpis: list[dict]) -> str:
    """HTML completo del panel de estado (sin resultado de parse)."""
    body = (
        _panel_status(info, n_cedulas, last_kpi)
        + _panel_history(history, kpis)
    )
    return page_frame(DEMO_CSS + EXTRA_CSS, body)


def _build_result_html(result: CedulaParseResult, year: int, month: int) -> str:
    """HTML completo del panel de resultado de validación."""
    body = (
        _panel_validations(result)
        + _panel_kpis(result, year, month)
    )
    return page_frame(DEMO_CSS + EXTRA_CSS, body)


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
def render() -> None:
    # ── Título ───────────────────────────────────────────────────────────────
    st.markdown("""
<div style="padding:12px 0 8px">
  <div style="font-size:18px;font-weight:800;color:#00D4FF;letter-spacing:-.02em">
    Centro de Ingesta Mensual
  </div>
  <div style="font-size:12px;color:rgba(255,255,255,0.45);margin-top:2px">
    Cédula presupuestaria · Pipeline SHA256 + validación + base de datos
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Estado actual de la DB ────────────────────────────────────────────────
    info      = db_info()
    n_cedulas = get_cedulas_count()
    last_kpi  = get_last_kpi()
    history   = get_upload_history(20)
    kpis      = get_kpi_history()

    status_html = _build_status_html(info, n_cedulas, last_kpi, history, kpis)
    components.html(status_html, height=420, scrolling=False)

    st.divider()

    # ── Formulario de ingesta ────────────────────────────────────────────────
    st.markdown("""
<div style="font-size:11px;font-weight:700;color:#00D4FF;text-transform:uppercase;
            letter-spacing:.1em;margin-bottom:8px">
  Nueva ingesta
</div>
""", unsafe_allow_html=True)

    col_f, col_y, col_m, col_u = st.columns([3, 1, 1.5, 1.5])

    with col_f:
        uploaded_file = st.file_uploader(
            "Cédula presupuestaria (.xlsx)",
            type=["xlsx", "xls"],
            label_visibility="collapsed",
            help="Archivo oficial eSIGEF/LOTAIP — cédula presupuestaria mensual",
        )

    with col_y:
        year = st.number_input(
            "Año", min_value=2020, max_value=2035,
            value=2026, step=1, label_visibility="visible",
        )

    with col_m:
        mes_opciones = [f"{n:02d} — {MESES[n]}" for n in range(1, 13)]
        mes_sel = st.selectbox(
            "Mes", mes_opciones,
            index=4,  # Mayo por defecto
            label_visibility="visible",
        )
        month = int(mes_sel.split(" — ")[0])

    with col_u:
        notas = st.text_input("Notas (opcional)", value="", placeholder="v2 / corrección…")

    # ── Procesar al subir archivo ─────────────────────────────────────────────
    if uploaded_file is not None:
        content = uploaded_file.read()

        # Cachear resultado en session para no re-parsear
        cache_key = f"parse_{uploaded_file.name}_{year}_{month}"
        if st.session_state.get("_ingesta_cache_key") != cache_key:
            with st.spinner("Analizando cédula…"):
                result = parse_cedula(
                    content           = content,
                    year              = int(year),
                    month             = month,
                    existing_hashes   = get_existing_hashes(),
                    existing_periods  = get_existing_periods(),
                )
            st.session_state["_ingesta_result"]    = result
            st.session_state["_ingesta_content"]   = content
            st.session_state["_ingesta_cache_key"] = cache_key

        result:  CedulaParseResult = st.session_state["_ingesta_result"]
        content: bytes             = st.session_state["_ingesta_content"]

        # Mostrar resultado de validación
        result_html = _build_result_html(result, int(year), month)
        components.html(result_html, height=400, scrolling=False)

        # Botones de acción
        col_ok, col_cancel, _ = st.columns([1.5, 1, 4])

        # Determinar si hay duplicado (G4 fallido)
        g4 = next((v for v in result.validations if v.guardrail == "G4"), None)
        is_duplicate = g4 and not g4.passed
        btn_label = "Guardar en base de datos" if not is_duplicate else "Guardar de todos modos (duplicado)"

        with col_ok:
            can_save = result.ok   # solo si G1/G2/G3/G5 pasaron
            if st.button(
                btn_label,
                disabled=not can_save,
                type="primary" if can_save else "secondary",
                use_container_width=True,
            ):
                usuario = st.session_state.get("usuario", "analista")
                with st.spinner("Guardando…"):
                    ingesta = ingest_cedula(
                        result      = result,
                        year        = int(year),
                        month       = month,
                        file_name   = uploaded_file.name,
                        uploaded_by = usuario,
                        notes       = notas,
                    )

                if ingesta["ok"]:
                    st.success(
                        f"✓ Cédula guardada · "
                        f"ID #{ingesta['upload_id']} · "
                        f"{ingesta['lines_inserted']} líneas · "
                        f"Ti = {ingesta['ti_mensual_pct']:.1f}%"
                    )
                    # Limpiar caché para refrescar vista
                    st.session_state.pop("_ingesta_cache_key", None)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error al guardar: {ingesta.get('error', '–')}")

        with col_cancel:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.pop("_ingesta_cache_key", None)
                st.session_state.pop("_ingesta_result", None)
                st.session_state.pop("_ingesta_content", None)
                st.rerun()

        # Si hay error bloqueante, mostrar detalle
        if not result.ok:
            st.error(f"Ingesta bloqueada: {result.error}")

    # ── Guía de uso ──────────────────────────────────────────────────────────
    else:
        st.markdown("""
<div style="background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.15);
            border-radius:10px;padding:14px 18px;margin-top:8px">
  <div style="font-size:11px;font-weight:700;color:#00D4FF;margin-bottom:8px">
    ¿Cómo usar este módulo?
  </div>
  <ol style="font-size:12px;color:rgba(255,255,255,0.6);line-height:2;padding-left:20px">
    <li>Descarga la cédula presupuestaria mensual desde <b style="color:#E2E8F0">eSIGEF</b> o <b style="color:#E2E8F0">LOTAIP</b></li>
    <li>Selecciona el año y mes que corresponde al archivo</li>
    <li>Sube el archivo Excel (.xlsx) — el sistema valida automáticamente</li>
    <li>Revisa los guardrails G1–G5 y los indicadores calculados (Ti mensual)</li>
    <li>Confirma la ingesta si todo está correcto</li>
  </ol>
  <div style="font-size:11px;color:rgba(255,255,255,0.35);margin-top:8px;border-top:1px solid rgba(255,255,255,0.07);padding-top:8px">
    Cada archivo queda registrado con SHA256 · Los duplicados se detectan automáticamente ·
    Si el período ya existe se versiona (v2, v3…)
  </div>
</div>
""", unsafe_allow_html=True)
