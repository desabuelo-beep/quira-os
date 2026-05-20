"""
sentinel/report_engine.py
Motor de Reportes Institucionales Mensuales — Sprint 2.6.3

Genera el PDF ejecutivo mensual del estado institucional del Holding Municipal.
Pieza oficial de corte de período: portada, resumen ejecutivo, estado del
holding, alertas con resoluciones humanas, congruencia e integridad semántica.

Diseño: institucional, limpio, auditable.
NO futurista, NO startup SaaS. Estilo: Contraloría, BID, planificación pública.

Apto para: alcalde, concejales, dirección financiera, auditoría, Contraloría.
Usos: rendición de cuentas, LOTAIP, transición administrativa.

Dylus Lab © 2026
"""
from __future__ import annotations

import io
from datetime import datetime

from sentinel.db_config import get_connection

MESES_ES = {
    1: "Enero",  2: "Febrero", 3: "Marzo",     4: "Abril",
    5: "Mayo",   6: "Junio",   7: "Julio",     8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

ENTITY_LABELS = {
    "GAD":       "GAD Municipal de Montecristi",
    "BOMBEROS":  "Cuerpo de Bomberos de Montecristi",
    "EMAI-EP":   "Empresa Municipal de Aseo Integral",
    "PATRONATO": "Patronato Municipal de Amparo Social",
}

_STATUS_LABEL = {
    "ok":      "ESTABLE",
    "warning": "REQUIERE ATENCIÓN",
    "error":   "CRÍTICO",
}

_ESTADO_LABEL = {
    "pendiente":   "Abierta",
    "en_revision": "En Revisión",
    "resuelta":    "Resuelta",
}

_ENTITIES_ORDER = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]


# ── RECOPILACIÓN DE DATOS ─────────────────────────────────────────────────────

def _get_holding_kpis(year: int, month: int) -> dict:
    """Ti ejecución por entidad para el período."""
    try:
        conn = get_connection()
        c    = conn.cursor()
        rows = c.execute(
            "SELECT entidad, ti_mensual_pct FROM monthly_kpis "
            "WHERE period_year=? AND period_month=?",
            (year, month),
        ).fetchall()
        conn.close()
        return {r["entidad"]: r["ti_mensual_pct"] for r in rows}
    except Exception:
        return {}


def build_report_data(period_year: int, period_month: int) -> dict:
    """
    Agrega todos los datos del período para el reporte.
    Retorna dict con toda la información necesaria para generate_pdf_bytes().
    """
    from sentinel.parity_engine    import get_congruencia_status
    from sentinel.integrity_engine import run_integrity_check
    from sentinel.alert_engine     import (
        get_alert_kpis, get_alerts_history, get_tendencias,
        get_aging_report, get_reincidencia,
        ESTADO_ABIERTA, ESTADO_EN_REVISION, ESTADO_RESUELTA,
        ERROR, WARNING, OK,
    )

    period_label = f"{MESES_ES.get(period_month, str(period_month))} {period_year}"

    # Congruencia
    try:
        cong = get_congruencia_status()
    except Exception:
        cong = {
            "global_status": "error", "global_label": "No disponible",
            "fuente":  {"status": "error"},
            "memoria": {"status": "error"},
            "motor":   {"status": "error"},
        }

    # Integridad semántica
    try:
        integ = run_integrity_check()
    except Exception:
        integ = {"status": "error", "label": "No disponible",
                 "n_ok": 0, "n_total": 0, "checks": []}

    # KPIs de alertas
    kpis = get_alert_kpis()

    # Alertas del período específico + globales
    all_alerts     = get_alerts_history(limit=150)
    period_alerts  = [
        a for a in all_alerts
        if a.get("period_year") == period_year and a.get("period_month") == period_month
    ]
    criticas   = [a for a in period_alerts if a.get("status") == ERROR
                  and a.get("estado") != ESTADO_RESUELTA]
    en_rev     = [a for a in period_alerts if a.get("estado") == ESTADO_EN_REVISION]
    resueltas  = [a for a in period_alerts if a.get("estado") == ESTADO_RESUELTA]
    pendientes = [a for a in all_alerts   if a.get("estado") == ESTADO_ABIERTA]

    # Estado global
    if kpis["criticas_activas"] > 0:
        global_status, global_label = "error",   "CRÍTICO"
    elif kpis["advertencias_activas"] > 0:
        global_status, global_label = "warning",  "REQUIERE ATENCIÓN"
    else:
        global_status, global_label = "ok",       "ESTABLE"

    return {
        "period_year":   period_year,
        "period_month":  period_month,
        "period_label":  period_label,
        "generated_at":  datetime.now().isoformat(),
        "global_status": global_status,
        "global_label":  global_label,
        "congruencia":   cong,
        "integridad":    integ,
        "kpis":          kpis,
        "holding_kpis":  _get_holding_kpis(period_year, period_month),
        "tendencias":    get_tendencias(),
        "aging":         get_aging_report(),
        "reincidencia":  get_reincidencia(min_meses=2),
        "criticas":      criticas,
        "en_revision":   en_rev,
        "resueltas":     resueltas,
        "pendientes":    pendientes,
        "summary":       _build_executive_summary(
            kpis=kpis,
            tendencias=get_tendencias(),
            resueltas=resueltas,
            pendientes=pendientes,
        ),
    }


def _build_executive_summary(
    kpis: dict,
    tendencias: list,
    resueltas: list,
    pendientes: list,
) -> dict:
    """Resumen ejecutivo por reglas determinísticas. Sin ML ni modelos probabilísticos."""
    n_crit   = kpis.get("criticas_activas", 0)
    n_warn   = kpis.get("advertencias_activas", 0)
    n_res    = kpis.get("resueltas_este_mes", 0)
    dias_max = kpis.get("dias_abierta_max", 0)

    # ¿Cómo está el municipio?
    if n_crit > 2:
        estado = "El período registra múltiples alertas críticas activas que requieren atención institucional inmediata."
    elif n_crit > 0:
        estado = "El período presenta nivel de ejecución presupuestaria bajo con alertas críticas activas en el Holding Municipal."
    elif n_warn > 0:
        estado = "El período presenta advertencias en proceso de seguimiento institucional."
    else:
        estado = "El período se encuentra dentro de los parámetros institucionales establecidos."

    # ¿Qué preocupa?
    if n_crit > 0:
        preocupa = (
            f"{n_crit} entidad{'es' if n_crit > 1 else ''} del Holding Municipal "
            f"con alerta{'s' if n_crit > 1 else ''} crítica{'s' if n_crit > 1 else ''} activa{'s' if n_crit > 1 else ''}."
        )
    elif n_warn > 0:
        preocupa = f"{n_warn} advertencia{'s' if n_warn > 1 else ''} activa{'s' if n_warn > 1 else ''} en seguimiento."
    else:
        preocupa = "Sin alertas críticas ni advertencias activas en el período."

    # ¿Qué mejoró?
    mejoras = [t for t in tendencias if t.get("tipo") == "mejora"]
    if mejoras:
        mejoro = f"{mejoras[0].get('entidad_label', '')} muestra tendencia positiva sostenida en el período."
    elif n_res > 0:
        mejoro = (
            f"{n_res} alerta{'s' if n_res > 1 else ''} resuelta{'s' if n_res > 1 else ''} "
            f"con justificación institucional registrada en el período."
        )
    else:
        mejoro = "Sin variaciones positivas significativas en el período analizado."

    # ¿Qué está pendiente?
    n_pend = len(pendientes)
    if n_pend > 0:
        pendiente = (
            f"{n_pend} alerta{'s' if n_pend > 1 else ''} sin resolución institucional registrada. "
            f"Alerta más antigua: {dias_max} días sin atención."
        )
    else:
        pendiente = "Todas las alertas del período cuentan con seguimiento registrado."

    # ¿Acción recomendada?
    if n_crit > 0:
        accion = "Registrar resoluciones institucionales para alertas críticas. Priorizar ejecución presupuestaria de inversión."
    elif n_warn > 0:
        accion = "Mantener seguimiento de advertencias activas hasta su resolución documentada."
    else:
        accion = "Continuar con el ritmo de ingesta mensual y verificación de indicadores operativos."

    return {
        "estado":    estado,
        "preocupa":  preocupa,
        "mejoro":    mejoro,
        "pendiente": pendiente,
        "accion":    accion,
    }


# ── GENERACIÓN PDF ─────────────────────────────────────────────────────────────

def generate_pdf_bytes(data: dict) -> bytes:
    """
    Genera el PDF ejecutivo institucional mensual con reportlab.
    Diseño: blanco, limpio, institucional — apto para Contraloría y rendición de cuentas.
    Retorna bytes vacíos si reportlab no está disponible.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units     import cm
        from reportlab.lib.colors    import HexColor, white, black
        from reportlab.lib.styles    import ParagraphStyle
        from reportlab.lib.enums     import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
        from reportlab.platypus      import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak,
        )
    except ImportError:
        return b""

    # ── Paleta institucional (blanco / azul marino / colores de estado) ────
    C_NAVY   = HexColor("#0D1F3C")
    C_BLUE   = HexColor("#1A4A8C")
    C_GREEN  = HexColor("#006B3C")
    C_AMBER  = HexColor("#8C5A00")
    C_RED    = HexColor("#8C1515")
    C_LGRAY  = HexColor("#F5F7FA")
    C_MGRAY  = HexColor("#6B7A90")
    C_DGRAY  = HexColor("#374151")
    C_DIVID  = HexColor("#D1D9E6")
    C_BG_OK  = HexColor("#EFF7F2")
    C_BG_WN  = HexColor("#FFF8EC")
    C_BG_ER  = HexColor("#FFF0F0")

    _CLR = {"ok": C_GREEN, "warning": C_AMBER, "error": C_RED}
    _BG  = {"ok": C_BG_OK, "warning": C_BG_WN, "error": C_BG_ER}

    # ── Estilos de párrafo ─────────────────────────────────────────────────
    def _s(name, font="Helvetica", size=9.5, color=None, align=TA_LEFT,
           leading=14, space_before=0, space_after=0, bold=False):
        if bold:
            font = "Helvetica-Bold"
        return ParagraphStyle(
            name, fontName=font, fontSize=size,
            textColor=color or C_DGRAY,
            alignment=align, leading=leading,
            spaceBefore=space_before, spaceAfter=space_after,
        )

    s_body      = _s("body",     leading=14,  align=TA_JUSTIFY)
    s_body_c    = _s("body_c",   leading=14,  align=TA_CENTER)
    s_label     = _s("label",    size=8.5, color=C_MGRAY, bold=True)
    s_value     = _s("value",    size=9.5, leading=14)
    s_note      = _s("note",     size=8, color=C_MGRAY, align=TA_CENTER,
                     font="Helvetica-Oblique")
    s_th        = _s("th",       size=9, color=white, bold=True, align=TA_CENTER)
    s_th_l      = _s("th_l",     size=9, color=white, bold=True, align=TA_LEFT)
    s_td        = _s("td",       size=9, leading=12)
    s_td_c      = _s("td_c",     size=9, leading=12, align=TA_CENTER)
    s_ok        = _s("s_ok",     size=9, color=C_GREEN,  bold=True, align=TA_CENTER)
    s_warn      = _s("s_warn",   size=9, color=C_AMBER,  bold=True, align=TA_CENTER)
    s_err       = _s("s_err",    size=9, color=C_RED,    bold=True, align=TA_CENTER)
    s_hdr_white = _s("hdr_w",    size=13, color=white, bold=True)
    s_hdr_sub   = _s("hdr_sub",  size=8,  color=HexColor("#A0B4CC"), font="Helvetica")

    def _status_p(st: str) -> Paragraph:
        lbl  = {"ok": "✓ ESTABLE", "warning": "⚠ ATENCIÓN", "error": "✗ CRÍTICO"}.get(st, "–")
        styl = {"ok": s_ok, "warning": s_warn, "error": s_err}.get(st, s_td_c)
        return Paragraph(lbl, styl)

    # ── Helper: encabezado de sección ─────────────────────────────────────
    def _section(title: str, subtitle: str = "") -> list:
        rows = [[Paragraph(title, s_hdr_white)]]
        if subtitle:
            rows.append([Paragraph(subtitle, s_hdr_sub)])
        t = Table(rows, colWidths=[W])
        ts = [
            ("BACKGROUND",    (0, 0), (-1, -1), C_NAVY),
            ("LEFTPADDING",   (0, 0), (-1, -1), 12),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
            ("TOPPADDING",    (0, 0), (0, 0),   10),
            ("BOTTOMPADDING", (0, -1), (0, -1), 10 if not subtitle else 8),
        ]
        if subtitle:
            ts.extend([
                ("TOPPADDING",    (0, 1), (0, 1), 3),
                ("BOTTOMPADDING", (0, 1), (0, 1), 8),
            ])
        t.setStyle(TableStyle(ts))
        return [t, Spacer(1, 0.3 * cm)]

    # ── Helper: tabla base ────────────────────────────────────────────────
    def _ts_base(n_rows: int, alt: bool = True) -> list:
        ts = [
            ("BACKGROUND",    (0, 0), (-1, 0),  C_BLUE),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, 0),  9),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  white),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("GRID",          (0, 0), (-1, -1), 0.5, C_DIVID),
        ]
        if alt:
            for i in range(1, n_rows, 2):
                ts.append(("BACKGROUND", (0, i), (-1, i), C_LGRAY))
        return ts

    # ── Documento ─────────────────────────────────────────────────────────
    buf = io.BytesIO()
    page_w, page_h = A4
    mg = 2 * cm
    W  = page_w - 2 * mg   # ancho útil ≈ 17 cm

    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=mg, rightMargin=mg,
        topMargin=mg, bottomMargin=mg,
        title=f"Estado Institucional {data['period_label']}",
        author="QUIRA OS · Dylus Lab",
        subject=f"Informe ejecutivo mensual — GAD Montecristi",
    )

    story = []
    g_st  = data["global_status"]
    g_lbl = data["global_label"]
    g_clr = _CLR.get(g_st, C_MGRAY)
    g_bg  = _BG.get(g_st, C_LGRAY)

    # ═══════════════════════════════════════════════════════════════════════
    # PORTADA
    # ═══════════════════════════════════════════════════════════════════════

    # Banda de identidad superior
    id_band = Table([
        [Paragraph("QUIRA OS · Sistema Integral de Gobernanza", _s("id1", size=9, color=HexColor("#7A9CC4"), align=TA_CENTER))],
        [Paragraph("GAD MUNICIPAL DE MONTECRISTI", _s("id2", size=20, color=white, bold=True, align=TA_CENTER))],
        [Paragraph("Holding Municipal · Ecuador", _s("id3", size=11, color=HexColor("#7A9CC4"), align=TA_CENTER))],
    ], colWidths=[W])
    id_band.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), C_NAVY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
    ]))
    story.append(id_band)
    story.append(Spacer(1, 2.5 * cm))

    story.append(Paragraph(
        "Estado Institucional Mensual",
        _s("cov_title", size=28, color=C_NAVY, bold=True, align=TA_CENTER),
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(
        f"Período: {data['period_label']}",
        _s("cov_per", size=16, color=C_BLUE, align=TA_CENTER),
    ))
    story.append(Spacer(1, 2 * cm))

    # Badge de estado global (box centrado)
    icon_map = {"ok": "✓", "warning": "⚠", "error": "✗"}
    status_box = Table([
        [Paragraph(icon_map.get(g_st, ""), _s("sticon", size=28, color=g_clr, bold=True, align=TA_CENTER))],
        [Paragraph(g_lbl, _s("stlbl", size=16, color=g_clr, bold=True, align=TA_CENTER))],
        [Paragraph("Estado global del período", _s("stsub", size=10, color=C_MGRAY, align=TA_CENTER))],
    ], colWidths=[W * 0.5])
    status_box.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), g_bg),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("BOX",           (0, 0), (-1, -1), 1, g_clr),
    ]))
    wrapper = Table([[status_box]], colWidths=[W])
    wrapper.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    story.append(wrapper)
    story.append(Spacer(1, 2.5 * cm))

    # Metadatos
    meta = Table([
        ["Generado por:",       "QUIRA OS · Sentinel · Dylus Lab"],
        ["Fecha:",              datetime.now().strftime("%d de %B de %Y, %H:%M")],
        ["Municipio:",          "GAD Municipal de Montecristi — Manabí, Ecuador"],
        ["Clasificación:",      "Documento institucional oficial — uso administrativo"],
    ], colWidths=[4.5 * cm, W - 4.5 * cm])
    meta.setStyle(TableStyle([
        ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",      (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",     (0, 0), (-1, -1), C_DGRAY),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW",     (0, -1), (-1, -1), 0.5, C_DIVID),
    ]))
    story.append(meta)
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        "Documento generado automáticamente a partir de datos verificados del sistema QUIRA OS. "
        "Apto para rendición de cuentas, LOTAIP, auditoría interna y transición administrativa.",
        s_note,
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # RESUMEN EJECUTIVO
    # ═══════════════════════════════════════════════════════════════════════
    story.extend(_section("Resumen Ejecutivo", data["period_label"]))
    sm = data["summary"]
    for question, answer in [
        ("¿Cómo está el municipio?",   sm["estado"]),
        ("¿Qué preocupa?",             sm["preocupa"]),
        ("¿Qué mejoró?",               sm["mejoro"]),
        ("¿Qué está pendiente?",       sm["pendiente"]),
        ("Acción recomendada",         sm["accion"]),
    ]:
        row_t = Table(
            [[Paragraph(question, s_label), Paragraph(answer, s_value)]],
            colWidths=[4.5 * cm, W - 4.5 * cm],
        )
        row_t.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
            ("LINEBELOW",     (0, 0), (-1, -1), 0.5, C_DIVID),
        ]))
        story.append(row_t)

    story.append(Spacer(1, 0.6 * cm))

    # KPI metrics
    kpis = data["kpis"]
    kpi_data = [
        [Paragraph("Alertas críticas activas", s_th),
         Paragraph("Advertencias activas", s_th),
         Paragraph("Resueltas en el período", s_th),
         Paragraph("Días sin resolver (máx.)", s_th)],
        [Paragraph(str(kpis.get("criticas_activas", 0)),
                   _s("kv1", size=22, bold=True, align=TA_CENTER,
                      color=C_RED if kpis.get("criticas_activas", 0) > 0 else C_GREEN)),
         Paragraph(str(kpis.get("advertencias_activas", 0)),
                   _s("kv2", size=22, bold=True, align=TA_CENTER,
                      color=C_AMBER if kpis.get("advertencias_activas", 0) > 0 else C_GREEN)),
         Paragraph(str(kpis.get("resueltas_este_mes", 0)),
                   _s("kv3", size=22, bold=True, align=TA_CENTER, color=C_GREEN)),
         Paragraph(f"{kpis.get('dias_abierta_max', 0)}d",
                   _s("kv4", size=22, bold=True, align=TA_CENTER, color=C_DGRAY))],
    ]
    kpi_t = Table(kpi_data, colWidths=[W / 4] * 4)
    kpi_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLUE),
        ("BACKGROUND",    (0, 1), (-1, 1),  C_LGRAY),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, C_DIVID),
    ]))
    story.append(kpi_t)
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # ESTADO DEL HOLDING MUNICIPAL
    # ═══════════════════════════════════════════════════════════════════════
    story.extend(_section(
        "Estado del Holding Municipal",
        "Ti inversión — Devengado / Codificado × 100",
    ))

    hkpis = data["holding_kpis"]
    holding_rows = [[
        Paragraph("Institución", s_th_l),
        Paragraph("Ti Ejecución", s_th),
        Paragraph("Estado", s_th),
        Paragraph("Umbral", s_th),
    ]]
    for ent in _ENTITIES_ORDER:
        ti = hkpis.get(ent)
        if ti is None:
            ti_str = "Sin datos"
            st_v   = "error"
        else:
            ti_str = f"{ti:.2f}%"
            st_v   = "ok" if ti >= 35 else ("warning" if ti >= 15 else "error")
        umb = {"ok": "≥ 35%", "warning": "15–35%", "error": "< 15%"}[st_v]
        holding_rows.append([
            Paragraph(ENTITY_LABELS.get(ent, ent), s_td),
            Paragraph(ti_str, _s(f"ti{ent}", size=12, bold=True, align=TA_CENTER,
                                 color=_CLR[st_v])),
            _status_p(st_v),
            Paragraph(umb, s_td_c),
        ])
    holding_t = Table(holding_rows, colWidths=[8 * cm, 3 * cm, 3.5 * cm, 2.5 * cm])
    ts = _ts_base(len(holding_rows))
    ts.append(("ALIGN", (0, 1), (0, -1), "LEFT"))
    holding_t.setStyle(TableStyle(ts))
    story.append(holding_t)
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph(
        "Fuente: registros eSIGEF verificados. Umbrales: Estable ≥ 35% · Atención 15–35% · Crítico < 15%.",
        s_note,
    ))
    story.append(Spacer(1, 0.6 * cm))

    # Reincidencia (si existe)
    reinc = data.get("reincidencia", [])
    if reinc:
        story.extend(_section("Reincidencia de Alertas", "Patrones de alerta repetidos en múltiples períodos"))
        reinc_rows = [[
            Paragraph("Institución", s_th_l),
            Paragraph("Tipo", s_th),
            Paragraph("Períodos", s_th),
            Paragraph("Clasificación", s_th),
        ]]
        _tipo_lbl = {"ejecucion": "Ejecución", "cobertura": "Cobertura"}
        for r in reinc[:6]:
            reinc_rows.append([
                Paragraph(r["entidad_label"], s_td),
                Paragraph(_tipo_lbl.get(r["tipo"], r["tipo"].title()), s_td_c),
                Paragraph(str(r["n_periodos"]), s_td_c),
                Paragraph(
                    "Patrón Estructural" if r["es_patron"] else "Repetido",
                    s_err if r["es_patron"] else s_warn,
                ),
            ])
        reinc_t = Table(reinc_rows, colWidths=[7.5 * cm, 3 * cm, 3 * cm, 3.5 * cm])
        reinc_t.setStyle(TableStyle(_ts_base(len(reinc_rows))))
        story.append(reinc_t)
        story.append(Spacer(1, 0.4 * cm))

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # ALERTAS INSTITUCIONALES
    # ═══════════════════════════════════════════════════════════════════════
    story.extend(_section("Alertas Institucionales", f"Período: {data['period_label']}"))

    def _alert_table(alerts: list, cols: list, bg_clr, label: str) -> None:
        if not alerts:
            story.append(Paragraph(
                f"✓ Sin {label.lower()} en el período.", s_ok,
            ))
            story.append(Spacer(1, 0.3 * cm))
            return
        story.append(Paragraph(label, s_label))
        story.append(Spacer(1, 0.15 * cm))
        header = [Paragraph(c[0], s_th_l if i == 0 else s_th) for i, c in enumerate(cols)]
        rows   = [header]
        for a in alerts[:10]:
            row = []
            for _, field, _w in cols:
                val = a.get(field, "")
                if val is None:
                    val = "–"
                row.append(Paragraph(str(val)[:120], s_td if len(rows) == 0 else s_td))
            rows.append(row)
        col_w = [cols[i][2] for i in range(len(cols))]
        tbl   = Table(rows, colWidths=col_w)
        ts    = _ts_base(len(rows), alt=False)
        ts.extend([("BACKGROUND", (0, i), (-1, i), bg_clr) for i in range(1, len(rows))])
        tbl.setStyle(TableStyle(ts))
        story.append(tbl)
        story.append(Spacer(1, 0.4 * cm))

    _alert_table(
        alerts=data["criticas"],
        cols=[("Institución", "entidad", 5*cm), ("Alerta", "titulo", 9*cm), ("Severidad", "severidad", 3*cm)],
        bg_clr=C_BG_ER, label="Alertas Críticas",
    )

    en_rev_full = []
    for a in data["en_revision"]:
        a2 = dict(a)
        a2["entidad_lbl"] = ENTITY_LABELS.get(a.get("entidad", ""), a.get("entidad", ""))
        a2["resolucion_display"] = (a.get("resolucion") or "Pendiente de registro.")[:120]
        en_rev_full.append(a2)
    if en_rev_full:
        story.append(Paragraph("Alertas en Revisión", s_label))
        story.append(Spacer(1, 0.15 * cm))
        rev_rows = [[
            Paragraph("Institución", s_th_l),
            Paragraph("Alerta", s_th),
            Paragraph("Justificación / Resolución", s_th),
        ]]
        for a in en_rev_full[:8]:
            rev_rows.append([
                Paragraph(a["entidad_lbl"], s_td),
                Paragraph(a.get("titulo", ""), s_td),
                Paragraph(a["resolucion_display"],
                          _s("res", size=8.5, font="Helvetica-Oblique", leading=12)),
            ])
        rev_t = Table(rev_rows, colWidths=[5*cm, 6*cm, 6*cm])
        ts2   = _ts_base(len(rev_rows), alt=False)
        ts2.extend([("BACKGROUND", (0, i), (-1, i), C_BG_WN) for i in range(1, len(rev_rows))])
        rev_t.setStyle(TableStyle(ts2))
        story.append(rev_t)
        story.append(Spacer(1, 0.4 * cm))
    else:
        story.append(Paragraph("Sin alertas en revisión.", s_ok))
        story.append(Spacer(1, 0.3 * cm))

    res_full = []
    for a in data["resueltas"]:
        a2 = dict(a)
        a2["entidad_lbl"] = ENTITY_LABELS.get(a.get("entidad", ""), a.get("entidad", ""))
        a2["resolucion_display"] = (a.get("resolucion") or "Resuelta automáticamente.")[:120]
        res_full.append(a2)
    if res_full:
        story.append(Paragraph("Alertas Resueltas en el Período", s_label))
        story.append(Spacer(1, 0.15 * cm))
        res_rows = [[
            Paragraph("Institución", s_th_l),
            Paragraph("Alerta", s_th),
            Paragraph("Resolución institucional", s_th),
        ]]
        for a in res_full[:8]:
            res_rows.append([
                Paragraph(a["entidad_lbl"], s_td),
                Paragraph(a.get("titulo", ""), s_td),
                Paragraph(a["resolucion_display"],
                          _s("res2", size=8.5, font="Helvetica-Oblique", leading=12)),
            ])
        res_t = Table(res_rows, colWidths=[5*cm, 6*cm, 6*cm])
        ts3   = _ts_base(len(res_rows), alt=False)
        ts3.extend([("BACKGROUND", (0, i), (-1, i), C_BG_OK) for i in range(1, len(res_rows))])
        res_t.setStyle(TableStyle(ts3))
        story.append(res_t)
    else:
        story.append(Paragraph("Sin alertas resueltas en el período.", s_ok))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CONGRUENCIA E INTEGRIDAD
    # ═══════════════════════════════════════════════════════════════════════
    story.extend(_section(
        "Congruencia e Integridad Institucional",
        "Coherencia entre las tres capas del sistema",
    ))

    cong  = data["congruencia"]
    integ = data["integridad"]

    # Congruencia 3 capas
    _CONG_DESC = {
        "fuente":  ("Fuente Operativa",      "Registros eSIGEF y documentos mensuales."),
        "memoria": ("Memoria Institucional",  "Cédulas presupuestarias en archivo verificado."),
        "motor":   ("Motor Analítico",        "Indicadores procesados para análisis institucional."),
    }
    cong_rows = [[
        Paragraph("Componente", s_th_l),
        Paragraph("Estado", s_th),
        Paragraph("Descripción", s_th_l),
    ]]
    for key in ("fuente", "memoria", "motor"):
        lbl, desc = _CONG_DESC[key]
        st = (cong.get(key) or {}).get("status", "error")
        cong_rows.append([
            Paragraph(lbl, s_td),
            _status_p(st),
            Paragraph(desc, s_td),
        ])
    cong_t = Table(cong_rows, colWidths=[5 * cm, 3 * cm, 9 * cm])
    cong_t.setStyle(TableStyle(_ts_base(len(cong_rows))))
    story.append(cong_t)
    story.append(Spacer(1, 0.25 * cm))
    g_cong = cong.get("global_status", "error")
    story.append(Paragraph(
        f"Estado global de congruencia: {_STATUS_LABEL.get(g_cong, '–')}. "
        "Los indicadores publicados mantienen coherencia entre las tres capas institucionales verificadas.",
        s_note,
    ))
    story.append(Spacer(1, 0.6 * cm))

    # Integridad semántica
    story.extend(_section("Integridad Semántica", "Verificación de valores numéricos entre capas"))
    integ_ok    = integ.get("n_ok", 0)
    integ_total = integ.get("n_total", 0)
    integ_st    = integ.get("status", "error")

    isummary = Table([[
        Paragraph("Indicadores verificados", s_th),
        Paragraph("Resultado", s_th),
        Paragraph("Estado", s_th),
    ],[
        Paragraph(f"{integ_ok} de {integ_total}", _s("iok", size=16, bold=True, align=TA_CENTER, color=C_NAVY)),
        Paragraph(integ.get("label", "–"), s_td_c),
        _status_p(integ_st),
    ]], colWidths=[W / 3] * 3)
    isummary.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  C_BLUE),
        ("BACKGROUND",    (0, 1), (-1, 1),  C_LGRAY),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("GRID",          (0, 0), (-1, -1), 0.5, C_DIVID),
    ]))
    story.append(isummary)

    # Checks individuales
    checks = integ.get("checks", [])
    if checks:
        story.append(Spacer(1, 0.35 * cm))
        ch_rows = [[
            Paragraph("Entidad · Indicador", s_th_l),
            Paragraph("DB", s_th),
            Paragraph("Documento", s_th),
            Paragraph("Delta", s_th),
            Paragraph("Resultado", s_th),
        ]]
        for ch in checks:
            ch_rows.append([
                Paragraph(f"{ch.get('entidad','')} · {ch.get('kpi','')}", s_td),
                Paragraph(str(ch.get("val_db", "–")), s_td_c),
                Paragraph(str(ch.get("val_md", "–")), s_td_c),
                Paragraph(str(ch.get("delta", "–")), s_td_c),
                _status_p(ch.get("status", "error")),
            ])
        ch_t = Table(ch_rows, colWidths=[6.5*cm, 2*cm, 2.5*cm, 2.5*cm, 3.5*cm])
        ch_t.setStyle(TableStyle(_ts_base(len(ch_rows))))
        story.append(ch_t)

    story.append(Spacer(1, 0.6 * cm))

    # Nota metodológica final
    story.extend(_section("Nota Metodológica"))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        "Las alertas de este informe han sido generadas mediante reglas determinísticas auditables — "
        "no se emplea aprendizaje automático ni modelos probabilísticos. "
        "Las resoluciones institucionales corresponden a justificaciones ingresadas manualmente por "
        "funcionarios autorizados y forman parte de la memoria operativa oficial del municipio. "
        "Este documento es apto para procesos de rendición de cuentas, LOTAIP, auditoría interna "
        "y transición administrativa.",
        s_body,
    ))
    story.append(Spacer(1, 0.5 * cm))
    story.append(HRFlowable(width=W, thickness=0.5, color=C_DIVID))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(
        f"QUIRA OS v0.1 · Dylus Lab © 2026 · GAD Municipal de Montecristi · "
        f"Generado: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        s_note,
    ))

    doc.build(story)
    return buf.getvalue()
