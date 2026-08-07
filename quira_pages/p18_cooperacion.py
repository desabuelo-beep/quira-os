"""
QUIRA OS — P-18 Cooperación Internacional · D02 Motor de Elegibilidad Financiera
=================================================================================
REWRITE COMPLETO 2026-06-09 · ADR-026 §D02 Consecuencia · Dylus Lab © 2026

ARQUITECTURA (ADR-026 §D02):
    Renderer puro — lee únicamente desde:
        Supabase: fondos_elegibilidad → fondos_convocatorias → fondos_emisores
        fondos_simulator.simulate_unlock() para el tab Simulador
    NUNCA hardcodea fondos, montos, umbrales ni estados.

BLOOMBERG FIREWALL:
    Lenguaje de gobernanza, nunca metodología interna.
    ❌ PROHIBIDO en UI: ICPI · TGI · Ti · QTMP · H73 · H99 · Gold Master
    ✅ PERMITIDO: PSG · ISP · ITAM · IGP · IFE_A (indicadores públicos de gestión)

4 SECCIONES:
    1. Disponible hoy   — elegible_hoy
    2. Bloqueado        — no_elegible + brechas (elegible_con_brecha)
    3. Simulador        — "¿qué se desbloquea si mejoro X?"
    4. Por emisor       — vista Emisor-first (Colega v3)

MANTENIMIENTO:
    Agregar fondos → fondos_emisores + fondos_convocatorias (Supabase)
    Actualizar elegibilidad → python -m app.engines.fondos_matcher
    Agregar fuentes → fondos_requisitos (Supabase) + fuente_quira en Matcher
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

import streamlit as st

from utils.session import is_tecnico
from quira_pages.html_engine import render_page, page_header

logger = logging.getLogger(__name__)

GAD_ID = "MCR-001"

# ── Nombres públicos de indicadores (Bloomberg-safe) ──────────────────────────
_IND_PUBLICO: dict[str, str] = {
    "PSG":   "Presupuesto Sensible al Género",
    "ISP":   "Salud Presupuestaria",
    "IGP":   "Gestión Participativa",
    "IOC":   "Observancia Contractual",
    "IET":   "Inversión por Habitante",
    "IED":   "Equidad Territorial",
    "IFE_A": "Fidelidad del Mandato Electoral",
    "ITAM":  "Acceso a Información Pública",
    "RDC_PRESENTADA":       "Rendición de Cuentas presentada",
    "PAC_APROBADO":         "PAC publicado",
    "POA_APROBADO":         "POA aprobado",
    "CPCCS_SIN_OBS":        "Sin observaciones CPCCS",
    "LOTAIP_VIGENTE":       "LOTAIP vigente",
    "PORTAL_OPERATIVO":     "Portal de transparencia operativo",
    "META_PDOT_ASOCIADA":   "Meta PDOT asociada",
    "PDOT_ALINEADO":        "Proyecto alineado al PDOT",
    "PROMESA_CNE":          "Promesa electoral asociada",
    "META_INST_FORMALIZADA":"Meta institucional formalizada",
    "EVIDENCIA_EJECUCION":  "Evidencia de ejecución documentada",
    "PRIORIDAD_TERRITORIAL":"Área territorial priorizada",
    "PARROQUIA_PRIORIZADA": "Parroquia priorizada beneficiada",
}

# Valores actuales en escala porcentual (para display) — demo_data como fuente
def _indicadores_display() -> dict[str, float | None]:
    """Retorna valores actuales en escala porcentual para mostrar en UI."""
    try:
        from data.demo_data import INDICES
        return {
            "PSG":   INDICES.get("PSG",   {}).get("valor"),
            "ISP":   INDICES.get("ISP",   {}).get("valor"),
            "IGP":   INDICES.get("IGP",   {}).get("valor"),
            "IOC":   INDICES.get("IOC",   {}).get("valor"),
            "IET":   INDICES.get("IET",   {}).get("valor"),
            "IED":   INDICES.get("IED",   {}).get("valor"),
            "IFE_A": INDICES.get("IFE-A", {}).get("valor"),
            "ITAM":  INDICES.get("ITAM",  {}).get("valor"),
        }
    except Exception:
        return {}


# ── Carga desde Supabase ──────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner="Consultando inteligencia financiera…")
def _load_elegibilidad() -> list[dict]:
    """Lee fondos_elegibilidad + convocatorias + emisores desde Supabase.

    Cache TTL=5 min. Retorna lista vacía si Supabase no disponible.
    """
    try:
        import psycopg2
        import psycopg2.extras

        try:
            uri = st.secrets.get("database", {}).get("supabase_uri", "")
        except Exception:
            uri = ""
        if not uri:
            import config as cfg
            uri = getattr(cfg, "SUPABASE_URI", "")

        # El puerto del pooler se normaliza: esta página abre su propia
        # conexión sin pasar por `get_connection()`, así que no heredaba el fix.
        from sentinel.db_config import normalizar_uri
        conn = psycopg2.connect(normalizar_uri(uri), sslmode="require",
                                connect_timeout=10)
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            SELECT
                e.estado_quira,
                e.brechas_json,
                e.potencial_usd,
                e.monto_confianza,
                e.computed_at,
                c.codigo        AS conv_codigo,
                c.nombre        AS conv_nombre,
                c.monto_min_usd,
                c.monto_max_usd,
                c.temas,
                c.elegibles     AS conv_elegibles,
                c.url,
                c.fecha_cierre,
                em.nombre       AS emisor_nombre,
                em.tipo_emisor,
                em.naturaleza,
                em.pais_origen,
                em.temas        AS emisor_temas,
                em.web          AS emisor_web
            FROM fondos_elegibilidad e
            JOIN fondos_convocatorias c  ON c.id = e.convocatoria_id
            JOIN fondos_emisores em      ON em.id = c.emisor_id
            WHERE e.gad_id = %s
              AND c.estado IN ('abierta', 'recurrente')
            ORDER BY
                CASE e.estado_quira
                    WHEN 'elegible_hoy'        THEN 1
                    WHEN 'elegible_con_brecha' THEN 2
                    WHEN 'pendiente_datos'     THEN 3
                    WHEN 'no_elegible'         THEN 4
                END,
                e.potencial_usd DESC NULLS LAST
        """, (GAD_ID,))

        rows = [dict(r) for r in cur.fetchall()]
        cur.close()
        conn.close()
        return rows

    except Exception as exc:
        logger.error(f"[p18] registros no disponibles: {exc}")
        return []


# ── HTML helpers ──────────────────────────────────────────────────────────────

def _estado_badge(estado: str) -> str:
    mapa = {
        "elegible_hoy":        '<span class="badge badge-green">✅ ELEGIBLE</span>',
        "elegible_con_brecha": '<span class="badge badge-amber">⚠️ CON BRECHA</span>',
        "pendiente_datos":     '<span class="badge badge-cyan">⏳ PENDIENTE</span>',
        "no_elegible":         '<span class="badge badge-red">🔴 BLOQUEADO</span>',
    }
    return mapa.get(estado, "")


def _color_estado(estado: str) -> str:
    return {
        "elegible_hoy":        "green",
        "elegible_con_brecha": "amber",
        "no_elegible":         "red",
        "pendiente_datos":     "cyan",
    }.get(estado, "muted")


def _conv_card(row: dict, ind_display: dict) -> str:
    """Card de convocatoria para Tab Disponible + Tab Bloqueado."""
    estado  = row["estado_quira"]
    color   = _color_estado(estado)
    badge   = _estado_badge(estado)
    monto   = row.get("potencial_usd") or row.get("monto_max_usd") or 0
    brechas = row.get("brechas_json") or {}
    temas   = row.get("temas") or []

    temas_html = " ".join(
        f'<span style="font-size:8px;color:var(--cyan);background:rgba(0,212,255,.1);'
        f'border-radius:4px;padding:2px 5px">{t.replace("_", " ")}</span>'
        for t in (temas[:3] if temas else [])
    )

    # Brechas en lenguaje de gobernanza (Bloomberg-safe)
    brechas_html = ""
    if brechas:
        items = []
        for cod, gap in brechas.items():
            nombre = _IND_PUBLICO.get(cod, cod)
            actual = ind_display.get(cod)
            actual_str = f"{actual:.1f}%" if actual is not None else "—"
            items.append(
                f'<span style="color:var(--red);font-size:9px">'
                f'{nombre}: {actual_str} → brecha {abs(gap):.1f}pp</span>'
            )
        brechas_html = (
            '<div style="margin-top:6px">' +
            " · ".join(items) +
            "</div>"
        )

    naturaleza_label = (
        "No reembolsable" if row.get("naturaleza") == "no_reembolsable"
        else "Reembolsable" if row.get("naturaleza") == "reembolsable"
        else "Mixto"
    )

    monto_display = (
        f"${monto/1_000_000:.1f}M" if monto >= 1_000_000
        else f"${monto/1_000:.0f}K" if monto >= 1_000
        else f"${monto:,.0f}"
    )

    fecha = ""
    if row.get("fecha_cierre"):
        fecha = f'<div style="font-size:9px;color:var(--muted)">Cierre: {row["fecha_cierre"]}</div>'

    return f"""
<div style="background:var(--navy-card);border:1px solid var(--divider);
            border-left:4px solid var(--{color});border-radius:12px;
            padding:14px 16px;margin-bottom:10px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px">
    <div style="flex:1">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px">
        <span style="font-size:12px;font-weight:800;color:var(--white)">{row["conv_nombre"]}</span>
        {badge}
      </div>
      <div style="font-size:10px;color:var(--muted);margin-bottom:4px">
        {row["emisor_nombre"]} · {naturaleza_label} · {temas_html}
      </div>
      {brechas_html}
    </div>
    <div style="text-align:right;flex-shrink:0">
      <div style="font-size:22px;font-weight:900;color:var(--{color});
                  font-family:var(--mono)">{monto_display}</div>
      {fecha}
    </div>
  </div>
</div>"""


# ── KPI summary cards (HTML) ──────────────────────────────────────────────────

def _kpi_html(rows: list[dict]) -> str:
    hoy    = [r for r in rows if r["estado_quira"] == "elegible_hoy"]
    brecha = [r for r in rows if r["estado_quira"] == "elegible_con_brecha"]
    bloq   = [r for r in rows if r["estado_quira"] == "no_elegible"]

    usd_hoy    = sum(r.get("potencial_usd") or 0 for r in hoy)
    usd_brecha = sum(r.get("potencial_usd") or 0 for r in brecha)
    usd_bloq   = sum(r.get("monto_max_usd") or 0 for r in bloq)
    usd_total  = usd_hoy + usd_brecha + usd_bloq

    def _fmt(v):
        return f"${v/1_000_000:.1f}M" if v >= 1_000_000 else f"${v/1_000:.0f}K"

    computed = ""
    if rows and rows[0].get("computed_at"):
        ct = rows[0]["computed_at"]
        if isinstance(ct, datetime):
            computed = ct.strftime("%Y-%m-%d %H:%M UTC")
        else:
            computed = str(ct)[:16]

    return f"""
<div class="grid-4" style="margin-bottom:16px">
  <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--green);
                font-family:var(--mono)">{_fmt(usd_hoy)}</div>
    <div style="font-size:10px;font-weight:700;color:var(--green);margin-top:4px">ELEGIBLE HOY</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">{len(hoy)} convocatoria(s)</div>
  </div>
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--amber);
                font-family:var(--mono)">{_fmt(usd_brecha) if usd_brecha else "—"}</div>
    <div style="font-size:10px;font-weight:700;color:var(--amber);margin-top:4px">CON BRECHA</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">{len(brecha)} convocatoria(s)</div>
  </div>
  <div style="background:rgba(255,77,109,.07);border:1px solid rgba(255,77,109,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--red);
                font-family:var(--mono)">{_fmt(usd_bloq) if usd_bloq else "—"}</div>
    <div style="font-size:10px;font-weight:700;color:var(--red);margin-top:4px">COSTO OPORTUNIDAD</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">{len(bloq)} bloqueada(s)</div>
  </div>
  <div style="background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.25);
              border-radius:12px;padding:16px;text-align:center">
    <div style="font-size:28px;font-weight:900;color:var(--cyan);
                font-family:var(--mono)">{_fmt(usd_total)}</div>
    <div style="font-size:10px;font-weight:700;color:var(--cyan);margin-top:4px">UNIVERSO MAPEADO</div>
    <div style="font-size:9px;color:var(--muted);margin-top:3px">Actualizado: {computed}</div>
  </div>
</div>"""


# ── Render principal ──────────────────────────────────────────────────────────

def render() -> None:
    show_tech = is_tecnico()
    rows      = _load_elegibilidad()
    ind_disp  = _indicadores_display()

    # ── Header + KPIs ────────────────────────────────────────────────────
    hoy_count = sum(1 for r in rows if r["estado_quira"] == "elegible_hoy")
    bloq_usd  = sum(
        (r.get("monto_max_usd") or 0)
        for r in rows if r["estado_quira"] == "no_elegible"
    )
    usd_elegible = sum(
        (r.get("potencial_usd") or 0)
        for r in rows if r["estado_quira"] in ("elegible_hoy", "elegible_con_brecha")
    )

    bloq_fmt = (
        f"${bloq_usd/1_000_000:.1f}M" if bloq_usd >= 1_000_000
        else f"${bloq_usd/1_000:.0f}K"
    )
    hdr = page_header(
        "⑭ COOPERACIÓN INTERN.",
        "Motor de Elegibilidad Financiera",
        f"{hoy_count} disponibles ahora · ${usd_elegible/1_000:.0f}K potencial · {bloq_fmt} costo oportunidad",
        '<span class="badge badge-green">✅ Motor activo</span>',
    )

    if not rows:
        st.warning(
            "Sin datos de elegibilidad. "
            "Ejecuta `python -m app.engines.fondos_matcher` para calcular."
        )
        render_page(hdr, show_tech=show_tech, height=200)
        return

    render_page(hdr + _kpi_html(rows), show_tech=show_tech, height=240)

    # ── 4 Tabs ────────────────────────────────────────────────────────────
    tab_hoy, tab_bloq, tab_sim, tab_emisor = st.tabs([
        "✅ Disponible hoy",
        "🔴 Bloqueado / Brechas",
        "🔮 Simulador",
        "🏛️ Por emisor",
    ])

    # ── TAB 1: Disponible hoy ─────────────────────────────────────────────
    with tab_hoy:
        elegibles = [r for r in rows if r["estado_quira"] == "elegible_hoy"]
        if not elegibles:
            st.info("No hay convocatorias en estado elegible hoy. "
                    "Consulta la pestaña Simulador para ver cómo desbloquear oportunidades.")
        else:
            total_hoy = sum(r.get("potencial_usd") or 0 for r in elegibles)
            st.markdown(
                f"**{len(elegibles)} convocatoria(s) accesibles ahora** — "
                f"Potencial: **${total_hoy:,.0f}**"
            )
            html_cards = "".join(_conv_card(r, ind_disp) for r in elegibles)
            st.markdown(
                f'<div style="margin-top:12px">{html_cards}</div>',
                unsafe_allow_html=True,
            )

        # Elegibles con brecha (secundario en este tab)
        con_brecha = [r for r in rows if r["estado_quira"] == "elegible_con_brecha"]
        if con_brecha:
            st.markdown("---")
            st.markdown("**Elegibles con brecha menor** — cercanas a desbloquearse:")
            html_brecha = "".join(_conv_card(r, ind_disp) for r in con_brecha)
            st.markdown(
                f'<div style="margin-top:8px">{html_brecha}</div>',
                unsafe_allow_html=True,
            )

    # ── TAB 2: Bloqueado / Brechas ────────────────────────────────────────
    with tab_bloq:
        no_elegibles = [r for r in rows if r["estado_quira"] == "no_elegible"]
        if not no_elegibles:
            st.success("No hay convocatorias completamente bloqueadas.")
        else:
            total_bloq = sum(r.get("monto_max_usd") or 0 for r in no_elegibles)
            st.markdown(
                f"**{len(no_elegibles)} convocatoria(s) bloqueadas** — "
                f"Costo de oportunidad: **${total_bloq:,.0f}**"
            )

            # Llaves maestras: indicadores que más USD desbloquean
            _llaves: dict[str, int] = {}
            for r in no_elegibles:
                brechas = r.get("brechas_json") or {}
                monto   = r.get("monto_max_usd") or 0
                for cod in brechas:
                    _llaves[cod] = _llaves.get(cod, 0) + monto

            if _llaves:
                top_llaves = sorted(_llaves.items(), key=lambda x: -x[1])[:3]
                llave_items = []
                for cod, usd in top_llaves:
                    nombre  = _IND_PUBLICO.get(cod, cod)
                    actual  = ind_disp.get(cod)
                    act_str = f"{actual:.1f}%" if actual is not None else "—"
                    fmt_usd = f"${usd/1_000_000:.1f}M" if usd >= 1_000_000 else f"${usd/1_000:.0f}K"
                    llave_items.append(
                        f"<div style='padding:10px;background:rgba(255,77,109,.06);"
                        f"border-radius:8px;border-left:3px solid var(--red)'>"
                        f"<div style='font-size:10px;font-weight:700;color:var(--red)'>"
                        f"{nombre}: {act_str}</div>"
                        f"<div style='font-size:9px;color:var(--muted)'>Mejorar desbloquea {fmt_usd}</div>"
                        f"</div>"
                    )
                llaves_html = (
                    '<div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);'
                    'border-radius:12px;padding:14px;margin-bottom:14px">'
                    '<div style="font-size:11px;font-weight:700;color:var(--red);margin-bottom:10px">'
                    '🔑 Indicadores clave — mejorarlos desbloquea más financiamiento</div>'
                    f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px">'
                    + "".join(llave_items) +
                    "</div></div>"
                )
                st.markdown(llaves_html, unsafe_allow_html=True)

            html_cards = "".join(_conv_card(r, ind_disp) for r in no_elegibles)
            st.markdown(
                f'<div style="margin-top:8px">{html_cards}</div>',
                unsafe_allow_html=True,
            )

    # ── TAB 3: Simulador ─────────────────────────────────────────────────
    with tab_sim:
        st.markdown(
            "**¿Cuánto dinero se desbloquea si el municipio mejora un indicador?**"
        )

        # Indicadores simulables (los que tienen valor actual conocido)
        sim_opciones = {
            nombre: (cod, val)
            for cod, val in ind_disp.items()
            if val is not None and (nombre := _IND_PUBLICO.get(cod, cod))
        }
        sim_opciones_ordered = dict(
            sorted(sim_opciones.items(), key=lambda x: x[0])
        )

        if not sim_opciones_ordered:
            st.warning("Sin datos de indicadores disponibles para simular.")
        else:
            col_sel, col_val = st.columns([2, 1])

            with col_sel:
                ind_label = st.selectbox(
                    "Indicador a mejorar",
                    options=list(sim_opciones_ordered.keys()),
                    help="Selecciona qué indicador quieres proyectar",
                )
            ind_cod, val_actual = sim_opciones_ordered[ind_label]

            with col_val:
                nuevo_val = st.number_input(
                    "Valor objetivo (%)",
                    min_value=float(val_actual or 0),
                    max_value=100.0,
                    value=min(float(val_actual or 0) + 20.0, 100.0),
                    step=5.0,
                    help="Ingresa el valor objetivo en escala 0-100%",
                )

            st.markdown(
                f"*Actual: **{val_actual:.2f}%** → Objetivo: **{nuevo_val:.1f}%***"
            )

            if st.button("🔮 Simular desbloqueo", type="primary", use_container_width=True):
                try:
                    from app.engines.fondos_simulator import simulate_unlock
                    with st.spinner("Calculando…"):
                        result = simulate_unlock(ind_cod, nuevo_val)

                    desbl = result.get("desbloqueadas", [])
                    ya    = result.get("ya_elegibles", [])
                    no    = result.get("no_mejora", [])

                    # Resultado principal
                    if desbl:
                        total_desbl = result["total_usd_desbloqueado"]
                        fmt = (f"${total_desbl/1_000_000:.1f}M"
                               if total_desbl >= 1_000_000
                               else f"${total_desbl/1_000:.0f}K")
                        st.success(
                            f"✅ **{len(desbl)} convocatoria(s) se desbloquean** "
                            f"→ {fmt} adicionales"
                        )
                        for e in desbl:
                            st.markdown(
                                f"- **{e['conv_nombre']}** · "
                                f"{e['emisor_nombre']} · "
                                f"${e['potencial_usd']:,.0f}"
                            )
                    else:
                        st.info(
                            "Con ese valor objetivo, ninguna convocatoria adicional "
                            "cambia de estado. Prueba con un objetivo más alto."
                        )

                    # Ya elegibles
                    if ya:
                        total_ya = result["total_ya_elegible_usd"]
                        st.markdown(
                            f"*Ya elegibles (sin cambio): "
                            f"{len(ya)} convocatoria(s) · ${total_ya:,.0f}*"
                        )

                    # Aún bloqueadas
                    if no:
                        costo = result["costo_oportunidad_usd"]
                        fmt_c = (f"${costo/1_000_000:.1f}M"
                                 if costo >= 1_000_000
                                 else f"${costo/1_000:.0f}K")
                        st.warning(
                            f"Aún bloqueadas con este cambio: "
                            f"{len(no)} convocatoria(s) · {fmt_c} costo de oportunidad restante"
                        )

                except Exception as exc:
                    st.error(f"Error en simulación: {exc}")

            # Escenarios preset
            with st.expander("📋 Escenarios de mejora institucional"):
                escenarios = [
                    ("PSG",   30.0, "Meta PDOT género — desbloquea ONU Mujeres"),
                    ("ISP",   65.0, "Umbral COOTAD — desbloquea crédito BDE"),
                    ("ITAM",  75.0, "Meta transparencia plena"),
                    ("IGP",   50.0, "Participación ciudadana robusta"),
                    ("IFE_A", 90.0, "Fidelidad mandato electoral alta"),
                ]
                for cod_e, val_e, desc_e in escenarios:
                    nombre_e = _IND_PUBLICO.get(cod_e, cod_e)
                    actual_e = ind_disp.get(cod_e)
                    act_str  = f"{actual_e:.1f}% →" if actual_e is not None else "→"
                    st.markdown(f"**{nombre_e}**: {act_str} {val_e}% — *{desc_e}*")

    # ── TAB 4: Por emisor ─────────────────────────────────────────────────
    with tab_emisor:
        st.markdown("**Vista por organización financiadora** — modelo Emisor-first")

        # Agrupar por emisor
        from collections import defaultdict
        emisor_map: dict[str, list[dict]] = defaultdict(list)
        for r in rows:
            emisor_map[r["emisor_nombre"]].append(r)

        for emisor_nombre, conv_list in sorted(emisor_map.items()):
            tipos = {r["tipo_emisor"] for r in conv_list}
            nats  = {r["naturaleza"] for r in conv_list}
            nat_label = "No reembolsable" if "no_reembolsable" in nats else "Reembolsable"

            estados = [r["estado_quira"] for r in conv_list]
            mejor   = min(estados, key=lambda s: {
                "elegible_hoy": 0, "elegible_con_brecha": 1,
                "pendiente_datos": 2, "no_elegible": 3
            }.get(s, 3))
            color_emisor = _color_estado(mejor)

            with st.expander(
                f"**{emisor_nombre}** · {nat_label} · "
                f"{', '.join(t.replace('_', ' ').title() for t in tipos)}"
            ):
                for r in conv_list:
                    badge = _estado_badge(r["estado_quira"])
                    monto = r.get("potencial_usd") or r.get("monto_max_usd") or 0
                    monto_str = (
                        f"${monto/1_000_000:.1f}M" if monto >= 1_000_000
                        else f"${monto/1_000:.0f}K" if monto > 0
                        else "—"
                    )
                    brechas = r.get("brechas_json") or {}
                    brecha_str = ""
                    if brechas:
                        items = [
                            f"{_IND_PUBLICO.get(k, k)}: {abs(v):.1f}pp"
                            for k, v in brechas.items()
                        ]
                        brecha_str = f" · Brecha: {', '.join(items)}"

                    web = r.get("emisor_web") or r.get("url") or ""
                    web_link = f" · [Web]({web})" if web else ""

                    st.markdown(
                        f"{badge} **{r['conv_nombre']}** — {monto_str}{brecha_str}{web_link}"
                    )

    # ── Navegación ────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    with c1:
        # Prompt Bloomberg-safe: sin ICGI-T, sin H73, sin Gold Master
        sentinel_prompt = (
            "Montecristi tiene un portafolio de cooperación activo. "
            f"Elegible hoy: {hoy_count} convocatorias. "
            "Las principales brechas son: "
            f"Salud Presupuestaria ({ind_disp.get('ISP', 0):.1f}%) y "
            f"Presupuesto Género ({ind_disp.get('PSG', 0):.1f}%). "
            "¿Cuál es la hoja de ruta de 6 meses para maximizar el monto captado, "
            "en qué orden priorizar las gestiones y qué unidad interna debe liderar cada fondo?"
        )
        if st.button("🔮 Estrategia de fondos", use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = sentinel_prompt
            st.rerun()

    with c2:
        if st.button("🌐 Ver Agenda 2030 · ODS", use_container_width=True):
            st.session_state["page"] = "ods"
            st.rerun()

    with c3:
        if st.button("💰 Ver Inversión por Habitante", use_container_width=True):
            st.session_state["page"] = "inversion"
            st.rerun()

    # Actualizar Matcher (solo técnicos)
    if show_tech:
        st.markdown("---")
        st.caption("Panel técnico")
        if st.button("🔄 Recalcular elegibilidad (Matcher)", use_container_width=True):
            try:
                from app.engines.fondos_matcher import run_matcher
                with st.spinner("Ejecutando Matcher…"):
                    summary = run_matcher(GAD_ID)
                _load_elegibilidad.clear()
                b = summary.get("breakdown", {})
                st.success(
                    f"Matcher OK — "
                    f"{b.get('elegible_hoy', 0)} elegibles · "
                    f"{b.get('elegible_con_brecha', 0)} brechas · "
                    f"{b.get('no_elegible', 0)} bloqueadas · "
                    f"USD {summary.get('total_potencial_usd', 0):,}"
                )
            except Exception as exc:
                st.error(f"Error Matcher: {exc}")
