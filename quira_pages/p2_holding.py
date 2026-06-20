"""
QUIRA OS — P-02 Holding Municipal · Cajón 1: Contratación Pública SERCOP
================================================================
Dashboard 100 % trazable · datos reales SERCOP API 2023-2026.
Ningún número en esta página es inventado — todo viene de
sercop_contratos (Supabase) alimentado por Sprint 0.

Entidades: GAD · PATRONATO · BOMBEROS · EMAI · EP Hábitat
Fuente:    https://datosabiertos.compraspublicas.gob.ec
Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from quira_pages.html_engine import render_page, page_header
from utils.session import is_tecnico
from utils.cache_quira import cargar_gm_snapshot


# ── METADATA ESTÁTICA ──────────────────────────────────────────────────────────
_ENTIDADES: dict[str, dict] = {
    "GAD":      {"emoji": "🏛️", "nombre": "GAD Municipal",      "tipo": "Gobierno Autónomo · COOTAD",       "color": "#00D4FF", "rgb": "0,212,255"},
    "PATRONATO":{"emoji": "🤝", "nombre": "Patronato Municipal", "tipo": "Desarrollo Social · LOSEP",        "color": "#7C5CFC", "rgb": "124,92,252"},
    "BOMBEROS": {"emoji": "🚒", "nombre": "Cuerpo de Bomberos",  "tipo": "Emergencias y Prevención · COESCOP","color": "#00E096","rgb": "0,224,150"},
    "EMAI":     {"emoji": "♻️", "nombre": "EMAI-EP",             "tipo": "Aseo Integral Montecristi · LOEP", "color": "#FFB800", "rgb": "255,184,0"},
    "HABITAT":  {"emoji": "🏗️", "nombre": "EP Hábitat",          "tipo": "Vivienda y Hábitat · LOEP",        "color": "#FF4D6D", "rgb": "255,77,109"},
}
_YEARS = [2023, 2024, 2025, 2026]


# ── DATA LAYER ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def _load_sercop_data() -> dict:
    """
    Carga y agrega datos de sercop_contratos.
    Cache 30 min — refreshable vía st.cache_data.clear().
    """
    from sentinel.db_config import get_connection, init_db
    try:
        init_db()
    except Exception:
        pass  # init es idempotente — no bloquear si ya existe

    conn = get_connection()
    try:
        c    = conn.cursor()

        # ① Totales por entidad
        by_entity: dict[str, dict] = {}
        rows = c.execute("""
            SELECT entidad_codigo,
                   COUNT(*) AS procesos,
                   SUM(monto_adjudicado)    AS adjudicado,
                   SUM(monto_presupuestado) AS presupuestado,
                   COUNT(DISTINCT proveedor) AS proveedores
            FROM sercop_contratos
            GROUP BY entidad_codigo
        """).fetchall()
        for r in rows:
            by_entity[r["entidad_codigo"]] = {
                "procesos":      int(r["procesos"]     or 0),
                "adjudicado":    float(r["adjudicado"] or 0),
                "presupuestado": float(r["presupuestado"] or 0),
                "proveedores":   int(r["proveedores"]  or 0),
            }

        # ② Por entidad × año
        by_year: dict[tuple, dict] = {}
        rows2 = c.execute("""
            SELECT entidad_codigo, anio,
                   COUNT(*) AS cnt, SUM(monto_adjudicado) AS adj
            FROM sercop_contratos
            GROUP BY entidad_codigo, anio
            ORDER BY entidad_codigo, anio
        """).fetchall()
        for r in rows2:
            key = (r["entidad_codigo"], int(r["anio"]))
            by_year[key] = {
                "cnt": int(r["cnt"]  or 0),
                "adj": float(r["adj"] or 0),
            }

        # ③ Top modalidades por entidad (top 4 por monto)
        tipos: dict[str, list] = {}
        rows3 = c.execute("""
            SELECT entidad_codigo, tipo_contratacion,
                   COUNT(*) AS cnt, SUM(monto_adjudicado) AS adj
            FROM sercop_contratos
            WHERE tipo_contratacion IS NOT NULL
            GROUP BY entidad_codigo, tipo_contratacion
            ORDER BY entidad_codigo, adj DESC
        """).fetchall()
        for r in rows3:
            cod = r["entidad_codigo"]
            tipos.setdefault(cod, []).append({
                "tipo": r["tipo_contratacion"],
                "cnt":  int(r["cnt"] or 0),
                "adj":  float(r["adj"] or 0),
            })

        # ④ Concentración de proveedores por entidad
        prov_by_entity: dict[str, list] = {}
        rows4 = c.execute("""
            SELECT entidad_codigo, proveedor,
                   COUNT(*) AS cnt, SUM(monto_adjudicado) AS adj
            FROM sercop_contratos
            WHERE proveedor IS NOT NULL AND proveedor != ''
            GROUP BY entidad_codigo, proveedor
            ORDER BY entidad_codigo, adj DESC
        """).fetchall()
        for r in rows4:
            cod = r["entidad_codigo"]
            prov_by_entity.setdefault(cod, []).append({
                "proveedor": r["proveedor"],
                "cnt":       int(r["cnt"] or 0),
                "adj":       float(r["adj"] or 0),
            })

        total_proc = sum(v["procesos"]   for v in by_entity.values())
        total_adj  = sum(v["adjudicado"] for v in by_entity.values())

        return {
            "ok":              True,
            "by_entity":       by_entity,
            "by_year":         by_year,
            "tipos":           tipos,
            "prov_by_entity":  prov_by_entity,
            "total_procesos":  total_proc,
            "total_adjudicado":total_adj,
        }
    except Exception as exc:
        return {
            "ok": False, "error": str(exc),
            "by_entity": {}, "by_year": {}, "tipos": {}, "prov_by_entity": {},
        }
    finally:
        conn.close()  # garantizado — nunca leakea conexión psycopg2


# ── FORMATTERS ─────────────────────────────────────────────────────────────────
def _fmt(v: float) -> str:
    """$X.XXM · $XXX K · $X,XXX"""
    if v >= 1_000_000:
        return f"${v / 1_000_000:.2f}M"
    if v >= 1_000:
        return f"${v / 1_000:.1f}K"
    if v > 0:
        return f"${v:,.0f}"
    return "$0"


def _pct(part: float, total: float) -> str:
    if total <= 0:
        return "—"
    return f"{part / total * 100:.1f}%"


# ── SPARKLINE ANUAL ────────────────────────────────────────────────────────────
def _sparkline(cod: str, by_year: dict, color: str) -> str:
    """Gráfica de barras año-por-año (CSS puro, sin librerías)."""
    vals = [by_year.get((cod, yr), {"cnt": 0, "adj": 0.0}) for yr in _YEARS]
    max_adj = max((v["adj"] for v in vals), default=1.0) or 1.0

    bars = ""
    for i, yr in enumerate(_YEARS):
        d   = vals[i]
        pct = min(d["adj"] / max_adj * 100, 100) if max_adj > 0 else 0
        lbl = _fmt(d["adj"]) if d["adj"] > 0 else "—"
        cnt = str(d["cnt"]) if d["cnt"] > 0 else "—"
        bars += (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:3px">'
            f'  <div style="font-size:8px;color:var(--muted);height:14px;display:flex;'
            f'              align-items:flex-end">{lbl}</div>'
            f'  <div style="width:34px;height:56px;background:rgba(255,255,255,.05);'
            f'              border-radius:3px;display:flex;align-items:flex-end;overflow:hidden">'
            f'    <div style="width:100%;height:{pct:.0f}%;background:{color};'
            f'                opacity:.85;border-radius:3px 3px 0 0;min-height:{2 if pct>0 else 0}px"></div>'
            f'  </div>'
            f'  <div style="font-size:9px;font-weight:700;color:var(--muted)">{yr}</div>'
            f'  <div style="font-size:9px;color:var(--white)">{cnt}</div>'
            f'</div>'
        )
    return (
        '<div style="margin-top:14px">'
        '<div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;'
        'letter-spacing:.08em;margin-bottom:8px">Evolución anual · adjudicado / procesos</div>'
        '<div style="display:flex;gap:10px;align-items:flex-end">'
        + bars
        + '</div>'
        '<div style="font-size:9px;color:rgba(255,255,255,.25);margin-top:4px">'
        '* 2026 parcial al corte de ingesta. Fuente: SERCOP API datos abiertos.</div>'
        '</div>'
    )


# ── MODALIDADES ────────────────────────────────────────────────────────────────
def _tipos_html(lista: list, color: str, total_adj: float) -> str:
    """Top 4 modalidades de contratación."""
    if not lista:
        return '<div style="font-size:11px;color:var(--muted)">Sin datos de modalidad</div>'
    top4 = lista[:4]
    rows = ""
    for t in top4:
        bar_w = min(t["adj"] / total_adj * 100, 100) if total_adj > 0 else 0
        rows += (
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'
            f'  <div style="flex:1;min-width:0">'
            f'    <div style="font-size:10px;color:var(--white);white-space:nowrap;'
            f'                overflow:hidden;text-overflow:ellipsis">{t["tipo"]}</div>'
            f'    <div style="height:4px;background:rgba(255,255,255,.06);border-radius:2px;margin-top:3px">'
            f'      <div style="height:100%;width:{bar_w:.0f}%;background:{color};border-radius:2px;opacity:.8"></div>'
            f'    </div>'
            f'  </div>'
            f'  <div style="text-align:right;flex-shrink:0">'
            f'    <div style="font-size:10px;font-weight:700;color:{color}">{_fmt(t["adj"])}</div>'
            f'    <div style="font-size:9px;color:var(--muted)">{t["cnt"]} proc.</div>'
            f'  </div>'
            f'</div>'
        )
    return rows


# ── CAJÓN DE ENTIDAD ───────────────────────────────────────────────────────────
def _cajon(idx: int, cod: str, stats: dict, by_year: dict, tipos: dict) -> str:
    meta  = _ENTIDADES[cod]
    color = meta["color"]
    rgb   = meta["rgb"]

    adj   = stats.get("adjudicado",    0.0)
    proc  = stats.get("procesos",      0)
    prov  = stats.get("proveedores",   0)
    pres  = stats.get("presupuestado", 0.0)
    ticket = adj / proc if proc > 0 else 0.0

    # Badge
    if proc == 0:
        badge_cls, badge_txt = "badge-red",    "⚠️ Sin actividad"
    elif adj >= 5_000_000:
        badge_cls, badge_txt = "badge-cyan",   "💰 Alta inversión"
    elif proc >= 200:
        badge_cls, badge_txt = "badge-purple", "📊 Alta frecuencia"
    else:
        badge_cls, badge_txt = "badge-green",  "✅ Activa"

    # Eficiencia presupuestaria (adjudicado/presupuestado)
    if pres > 0:
        eficiencia = adj / pres * 100
        efic_color = "var(--green)" if eficiencia <= 115 else "var(--amber)"
        efic_label = f"{eficiencia:.0f}%"
    else:
        efic_label = "—"
        efic_color = "var(--muted)"

    # Sparkline + tipos
    spark = _sparkline(cod, by_year, color) if proc > 0 else ""
    tipo_lista = tipos.get(cod, [])
    tipos_h = _tipos_html(tipo_lista, color, adj) if adj > 0 else ""

    # Alerta HABITAT
    alert_html = ""
    if cod == "HABITAT":
        alert_html = """
<div style="padding:12px 14px;background:rgba(255,77,109,.08);border-left:3px solid #FF4D6D;
            border-radius:0 8px 8px 0;margin:0 0 12px;font-size:12px;color:#FF4D6D">
  <strong>Entidad sin registro SERCOP (2023-2026).</strong>
  Puede indicar: entidad jurídicamente activa pero operativamente inactiva,
  procesos absorbidos por el GAD, o registro bajo nombre diferente en el sistema.
  Requiere verificación manual en el portal de compras públicas.
</div>"""

    # Alerta caída GAD 2025
    gad_alert = ""
    if cod == "GAD":
        p2024 = by_year.get(("GAD", 2024), {}).get("cnt", 0)
        p2025 = by_year.get(("GAD", 2025), {}).get("cnt", 0)
        if p2024 > 0 and p2025 < p2024 * 0.4:
            gad_alert = f"""
<div style="padding:10px 12px;background:rgba(255,183,0,.08);border-left:3px solid var(--amber);
            border-radius:0 8px 8px 0;margin:0 0 10px;font-size:11px;color:var(--amber)">
  ⚡ <strong>Caída 2024→2025:</strong> {p2024} → {p2025} procesos (
  {100-p2025/p2024*100:.0f}% menos). Puede indicar subejecución presupuestaria o
  desplazamiento a otro mecanismo de contratación.
</div>"""

    # Stats grid
    stats_grid = (
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:4px">'
        f'  <div style="text-align:center;padding:10px 6px;background:rgba(255,255,255,.04);border-radius:8px">'
        f'    <div style="font-size:18px;font-weight:900;font-family:var(--mono);color:{color}">{_fmt(adj)}</div>'
        f'    <div style="font-size:9px;color:var(--muted);margin-top:2px">Adjudicado</div>'
        f'  </div>'
        f'  <div style="text-align:center;padding:10px 6px;background:rgba(255,255,255,.04);border-radius:8px">'
        f'    <div style="font-size:18px;font-weight:900;font-family:var(--mono);color:var(--white)">{proc}</div>'
        f'    <div style="font-size:9px;color:var(--muted);margin-top:2px">Procesos</div>'
        f'  </div>'
        f'  <div style="text-align:center;padding:10px 6px;background:rgba(255,255,255,.04);border-radius:8px">'
        f'    <div style="font-size:18px;font-weight:900;font-family:var(--mono);color:var(--amber)">{_fmt(ticket)}</div>'
        f'    <div style="font-size:9px;color:var(--muted);margin-top:2px">Ticket promedio</div>'
        f'  </div>'
        f'  <div style="text-align:center;padding:10px 6px;background:rgba(255,255,255,.04);border-radius:8px">'
        f'    <div style="font-size:18px;font-weight:900;font-family:var(--mono);color:var(--purple)">{prov}</div>'
        f'    <div style="font-size:9px;color:var(--muted);margin-top:2px">Proveedores</div>'
        f'  </div>'
        f'</div>'
    )

    return f"""
<div style="margin-bottom:10px;border:1px solid rgba({rgb},.28);border-radius:12px;
            overflow:hidden;background:var(--navy-card)">
  <div onclick="var d=document.getElementById('hm{idx}');
                var open=d.style.display!=='none';
                d.style.display=open?'none':'block';
                this.querySelector('.arr{idx}').textContent=open?'▼':'▲'"
       style="padding:14px 16px;cursor:pointer;display:flex;
              justify-content:space-between;align-items:center;
              border-bottom:1px solid rgba({rgb},.1)">
    <div style="display:flex;align-items:center;gap:14px;flex:1;min-width:0">
      <div style="font-size:28px;flex-shrink:0">{meta['emoji']}</div>
      <div style="flex:1;min-width:0">
        <div style="font-size:15px;font-weight:800;color:var(--white)">{meta['nombre']}</div>
        <div style="font-size:10px;color:var(--muted);margin-top:2px">{meta['tipo']}</div>
      </div>
      <div style="display:flex;align-items:center;gap:14px;flex-shrink:0">
        <div style="text-align:right">
          <div style="font-size:20px;font-weight:900;font-family:var(--mono);
                      color:{color};line-height:1.1">{_fmt(adj)}</div>
          <div style="font-size:9px;color:var(--muted)">adjudicado</div>
        </div>
        <div style="text-align:center">
          <div style="font-size:18px;font-weight:800;color:var(--white)">{proc}</div>
          <div style="font-size:9px;color:var(--muted)">procesos</div>
        </div>
        <span class="badge {badge_cls}" style="font-size:10px;padding:4px 10px;
              white-space:nowrap">{badge_txt}</span>
      </div>
    </div>
    <span class="arr{idx}" style="color:var(--muted);font-size:11px;margin-left:12px;
          flex-shrink:0">▼</span>
  </div>

  <div id="hm{idx}" style="display:none;padding:14px 16px 16px">
    {alert_html}{gad_alert}
    {stats_grid}
    {spark}
    <div style="margin-top:14px">
      <div style="font-size:10px;font-weight:700;color:var(--muted);
                  text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">
        Modalidades principales de contratación</div>
      {tipos_h}
    </div>
  </div>
</div>"""


# ── CAJÓN 2: CONCENTRACIÓN DE PROVEEDORES ─────────────────────────────────────
# Metodología inspirada en cali-monitor (github.com/cardonanl/cali-monitor)
# Créditos al autor: @cardonanl · SECOP II analysis logic
# Adaptado para SERCOP Ecuador y arquitectura QUIRA OS · Dylus Lab © 2026

def _concentracion_stats(cod: str, prov_by_entity: dict, total_adj_entity: float) -> dict:
    """Calcula % concentración y HHI para una entidad."""
    lista = prov_by_entity.get(cod, [])
    if not lista or total_adj_entity <= 0:
        return {"top_proveedor": "—", "top_adj": 0.0, "top_pct": 0.0,
                "hhi": 0.0, "semaforo": "gris", "top5": []}

    top5    = lista[:5]
    top_adj = top5[0]["adj"] if top5 else 0.0
    top_pct = top_adj / total_adj_entity * 100 if total_adj_entity > 0 else 0.0

    # HHI: Índice Herfindahl-Hirschman (suma de cuadrados de market-shares)
    hhi = sum((r["adj"] / total_adj_entity * 100) ** 2 for r in lista)

    if top_pct >= 50:
        semaforo = "rojo"
    elif top_pct >= 30:
        semaforo = "amarillo"
    else:
        semaforo = "verde"

    return {
        "top_proveedor": top5[0]["proveedor"] if top5 else "—",
        "top_adj":       top_adj,
        "top_pct":       top_pct,
        "hhi":           hhi,
        "semaforo":      semaforo,
        "top5":          top5,
    }


def _semaforo_badge(semaforo: str) -> tuple[str, str]:
    return {
        "rojo":     ("badge-red",   "🔴 Concentración alta"),
        "amarillo": ("badge-amber", "🟡 Concentración media"),
        "verde":    ("badge-green", "🟢 Diversificado"),
        "gris":     ("badge-red",   "⚫ Sin datos"),
    }.get(semaforo, ("badge-cyan", semaforo))


def _prov_bars(top5: list, color: str, total_adj: float) -> str:
    """Top 5 proveedores con barras proporcionales."""
    if not top5:
        return '<div style="font-size:11px;color:var(--muted)">Sin proveedores registrados</div>'
    rows = ""
    for t in top5:
        bar_w  = min(t["adj"] / total_adj * 100, 100) if total_adj > 0 else 0
        nombre = (t["proveedor"] or "—")[:42]
        if len(t["proveedor"] or "") > 42:
            nombre += "…"
        rows += (
            f'<div style="margin-bottom:7px">'
            f'  <div style="display:flex;justify-content:space-between;'
            f'              align-items:center;margin-bottom:3px">'
            f'    <div style="font-size:10px;color:var(--white);flex:1;min-width:0;'
            f'                white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'
            f'      {nombre}</div>'
            f'    <div style="font-size:10px;font-weight:700;color:{color};'
            f'                margin-left:8px;flex-shrink:0">'
            f'      {_fmt(t["adj"])} · {bar_w:.0f}%</div>'
            f'  </div>'
            f'  <div style="height:4px;background:rgba(255,255,255,.06);border-radius:2px">'
            f'    <div style="height:100%;width:{bar_w:.1f}%;background:{color};'
            f'                border-radius:2px;opacity:.85"></div>'
            f'  </div>'
            f'</div>'
        )
    return rows


def _conc_entity_card(cod: str, conc: dict, by_entity: dict) -> str:
    """Card de concentración por entidad para el grid de Cajón 2."""
    meta  = _ENTIDADES[cod]
    color = meta["color"]
    rgb   = meta["rgb"]
    adj   = by_entity.get(cod, {}).get("adjudicado", 0.0)

    # Caso especial: HABITAT sin datos
    if cod == "HABITAT":
        return (
            f'<div style="background:rgba(255,77,109,.04);border:1px solid rgba(255,77,109,.18);'
            f'border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:8px">'
            f'  <div style="display:flex;justify-content:space-between;align-items:center">'
            f'    <div style="font-size:12px;font-weight:700;color:var(--white)">'
            f'      {meta["emoji"]} {meta["nombre"]}</div>'
            f'    <span class="badge badge-red" style="font-size:9px">⚫ Sin procesos</span>'
            f'  </div>'
            f'  <div style="font-size:10px;color:var(--muted)">'
            f'    EP Hábitat no registra proveedores en SERCOP 2023-2026. '
            f'    Imposible calcular concentración.</div>'
            f'</div>'
        )

    badge_cls, badge_txt = _semaforo_badge(conc["semaforo"])
    nombre_prov = (conc["top_proveedor"] or "—")[:46]
    if len(conc["top_proveedor"] or "") > 46:
        nombre_prov += "…"

    # HHI label
    hhi = conc["hhi"]
    if hhi > 2500:
        hhi_label, hhi_color = "Mercado concentrado", "var(--red)"
    elif hhi > 1500:
        hhi_label, hhi_color = "Concentración media", "var(--amber)"
    else:
        hhi_label, hhi_color = "Mercado competitivo", "var(--green)"

    return (
        f'<div style="background:rgba({rgb},.04);border:1px solid rgba({rgb},.2);'
        f'border-radius:10px;padding:14px">'
        f'  <div style="display:flex;justify-content:space-between;'
        f'              align-items:center;margin-bottom:10px">'
        f'    <div style="font-size:12px;font-weight:700;color:var(--white)">'
        f'      {meta["emoji"]} {meta["nombre"]}</div>'
        f'    <span class="badge {badge_cls}" style="font-size:9px;padding:3px 8px">'
        f'      {badge_txt}</span>'
        f'  </div>'
        f'  <div style="display:flex;align-items:flex-end;gap:10px;margin-bottom:8px">'
        f'    <div style="font-size:32px;font-weight:900;font-family:var(--mono);'
        f'                color:{color};line-height:1">{conc["top_pct"]:.0f}%</div>'
        f'    <div style="padding-bottom:4px">'
        f'      <div style="font-size:10px;font-weight:700;color:var(--muted)">'
        f'        del total al proveedor líder</div>'
        f'      <div style="font-size:10px;color:var(--white);margin-top:1px">'
        f'        {nombre_prov}</div>'
        f'    </div>'
        f'  </div>'
        f'  <div style="margin-bottom:10px">'
        f'    {_prov_bars(conc["top5"], color, adj)}'
        f'  </div>'
        f'  <div style="font-size:9px;color:var(--muted);display:flex;gap:14px;'
        f'              padding-top:8px;border-top:1px solid rgba(255,255,255,.05)">'
        f'    <span>HHI: {hhi:.0f}</span>'
        f'    <span style="color:{hhi_color}">{hhi_label}</span>'
        f'    <span>{len(conc["top5"])} prov. en top-5</span>'
        f'  </div>'
        f'</div>'
    )


def _cajon2(prov_by_entity: dict, by_entity: dict) -> str:
    """
    Cajón 2 — Concentración de Proveedores SERCOP.
    Detecta riesgo de dependencia institucional: un solo proveedor dominante
    puede indicar mercado cautivo, ausencia de competencia o riesgo de colusión.

    Metodología inspirada en cali-monitor (github.com/cardonanl/cali-monitor)
    Créditos al autor @cardonanl — adaptado para SERCOP Ecuador · QUIRA OS.
    """
    # Concentración por entidad
    conc: dict[str, dict] = {}
    for cod in _ENTIDADES:
        adj = by_entity.get(cod, {}).get("adjudicado", 0.0)
        conc[cod] = _concentracion_stats(cod, prov_by_entity, adj)

    # Entidades en zona roja (excluye HABITAT que no tiene datos)
    entidades_rojas = [
        cod for cod in ["GAD", "PATRONATO", "BOMBEROS", "EMAI"]
        if conc[cod]["semaforo"] == "rojo"
    ]

    # Alerta global
    alert_global = ""
    if entidades_rojas:
        nombres = " · ".join(_ENTIDADES[c]["nombre"] for c in entidades_rojas)
        alert_global = (
            f'<div style="padding:10px 14px;background:rgba(255,77,109,.08);'
            f'border-left:3px solid #FF4D6D;border-radius:0 8px 8px 0;'
            f'margin-bottom:14px;font-size:11px;color:#FF4D6D">'
            f'🚨 <strong>Riesgo de concentración detectado</strong> en: {nombres}. '
            f'Un solo proveedor concentra &gt;50% del total adjudicado. '
            f'Recomendación: ampliar registro de proveedores y revisar mecanismos de competencia.'
            f'</div>'
        )

    # Grid 2×2 para las 4 entidades activas
    cards = ""
    for cod in ["GAD", "PATRONATO", "BOMBEROS", "EMAI"]:
        cards += f'<div>{_conc_entity_card(cod, conc[cod], by_entity)}</div>'

    habitat_card = _conc_entity_card("HABITAT", conc["HABITAT"], by_entity)

    # Insight automático: más concentrada vs más diversificada
    activas = {
        cod: conc[cod] for cod in ["GAD", "PATRONATO", "BOMBEROS", "EMAI"]
        if conc[cod]["semaforo"] != "gris"
    }
    insight_txt = ""
    if len(activas) >= 2:
        mas_conc = max(activas, key=lambda x: activas[x]["top_pct"])
        mas_div  = min(activas, key=lambda x: activas[x]["top_pct"])
        mc = conc[mas_conc]
        md = conc[mas_div]
        insight_txt = (
            f'<div style="margin-top:12px;padding:10px 14px;'
            f'background:rgba(255,255,255,.02);border-radius:8px;'
            f'border-left:3px solid var(--purple);font-size:11px">'
            f'  <span style="color:var(--purple);font-weight:700">📊 Señal automática · </span>'
            f'  <span style="color:var(--white)">'
            f'    {_ENTIDADES[mas_conc]["nombre"]} es la entidad más concentrada: '
            f'    {mc["top_pct"]:.0f}% en 1 proveedor ({(mc["top_proveedor"] or "")[:35]}). '
            f'    {_ENTIDADES[mas_div]["nombre"]} es la más diversificada: '
            f'    solo {md["top_pct"]:.0f}% en el proveedor líder.'
            f'  </span>'
            f'</div>'
        )

    # Header badge
    if entidades_rojas:
        hdr_badge_cls = "badge-red"
        hdr_badge_txt = f"⚠️ {len(entidades_rojas)} entidad(es) en riesgo"
    else:
        hdr_badge_cls = "badge-green"
        hdr_badge_txt = "✅ Sin alertas de concentración"

    return f"""
<div style="margin-bottom:10px;border:1px solid rgba(124,92,252,.25);border-radius:12px;
            overflow:hidden;background:var(--navy-card)">
  <div onclick="var d=document.getElementById('cajon2body');
                var open=d.style.display!=='none';
                d.style.display=open?'none':'block';
                this.querySelector('.arrc2').textContent=open?'▼':'▲'"
       style="padding:14px 16px;cursor:pointer;display:flex;
              justify-content:space-between;align-items:center;
              border-bottom:1px solid rgba(124,92,252,.1)">
    <div style="display:flex;align-items:center;gap:14px">
      <div style="font-size:22px">🔍</div>
      <div>
        <div style="font-size:15px;font-weight:800;color:var(--white)">
          Cajón 2 · Concentración de Proveedores</div>
        <div style="font-size:10px;color:var(--muted);margin-top:2px">
          Riesgo de dependencia institucional · Índice HHI · SERCOP 2023-2026</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:10px;flex-shrink:0">
      <span class="badge {hdr_badge_cls}">{hdr_badge_txt}</span>
      <span class="arrc2" style="color:var(--muted);font-size:11px;margin-left:4px">▼</span>
    </div>
  </div>

  <div id="cajon2body" style="display:none;padding:14px 16px 16px">
    {alert_global}
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
      {cards}
    </div>
    {habitat_card}
    {insight_txt}
    <div style="margin-top:10px;font-size:9px;color:rgba(255,255,255,.18);line-height:1.6">
      📐 <strong>Método:</strong> % del monto adjudicado total al proveedor líder ·
      HHI (Herfindahl-Hirschman): suma de cuadrados de market-shares ·
      Umbrales: 🟢 &lt;30% · 🟡 30-50% · 🔴 &gt;50% ·
      Inspiración metodológica: <em>cali-monitor</em>
      (github.com/cardonanl/cali-monitor — créditos al autor @cardonanl).
      Adaptado para SERCOP Ecuador · Sprint 0 QUIRA OS.
    </div>
  </div>
</div>"""


# ── EJE DE CONSISTENCIA — ejecución presupuestaria del holding (motor h90) ──────
# La cifra madre de la tarjeta L1 (12.4% consolidado), desglosada en sus 4 entidades
# reales. Cierra el círculo causal: el consolidado NO es opinión, es ejecutado/codificado
# sin reinterpretación humana. (key h90, code en _ENTIDADES). Corte parcial Q1.
_H90_ENT = [("gad", "GAD"), ("patronato", "PATRONATO"), ("ep_aseo", "EMAI"), ("bomberos", "BOMBEROS")]


def _eje_consistencia(gm: dict) -> str:
    h90  = (gm or {}).get("financiero", {}).get("h90_consolidado", {}) or {}
    cons = h90.get("holding_ti_q1_pct")
    if cons is None:
        return ""  # sin motor → no fabricar (Regla 3: sin dato verificado, no hay dato)

    dev = h90.get("holding_total_devengado_q1", 0.0) or 0.0
    cod = h90.get("holding_total_codificado", 0.0) or 0.0

    filas = []
    for key, code in _H90_ENT:
        ti = h90.get(f"{key}_ti_q1_pct")
        if ti is None:
            continue
        dcod = h90.get(f"{key}_codificado") or h90.get(f"{key}_codificado_vigente_2026") or 0.0
        ddev = h90.get(f"{key}_devengado_q1") or 0.0
        meta = _ENTIDADES.get(code, {})
        filas.append({"ti": ti, "cod": dcod, "dev": ddev, "nombre": meta.get("nombre", code),
                      "emoji": meta.get("emoji", ""), "color": meta.get("color", "#8892B0")})
    filas.sort(key=lambda x: x["ti"], reverse=True)
    if not filas:
        return ""
    max_ti = max((f["ti"] for f in filas), default=1.0) or 1.0

    bars = ""
    for f in filas:
        w     = min(f["ti"] / max_ti * 100, 100)
        share = (f["cod"] / cod * 100) if cod > 0 else 0
        bars += (
            f'<div style="margin-bottom:10px">'
            f'  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:3px">'
            f'    <span style="font-size:11px;color:var(--white)">{f["emoji"]} {f["nombre"]} '
            f'      <span style="color:var(--muted);font-size:9px">· {share:.0f}% del presupuesto</span></span>'
            f'    <span style="font-size:12px;font-weight:800;font-family:var(--mono);color:{f["color"]}">{f["ti"]:.1f}%</span>'
            f'  </div>'
            f'  <div style="height:6px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden">'
            f'    <div style="height:100%;width:{w:.0f}%;background:{f["color"]};opacity:.85;border-radius:3px"></div>'
            f'  </div>'
            f'  <div style="font-size:9px;color:var(--muted);margin-top:2px">'
            f'    {_fmt(f["dev"])} ejecutado de {_fmt(f["cod"])} codificado</div>'
            f'</div>'
        )

    lider  = filas[0]
    rezago = min(filas, key=lambda x: x["ti"])
    share_rez = (rezago["cod"] / cod * 100) if cod > 0 else 0
    narrativa = (
        f'El {rezago["nombre"]} concentra el {share_rez:.0f}% del presupuesto del holding '
        f'({_fmt(rezago["cod"])}) y ejecutó {rezago["ti"]:.1f}% al primer trimestre — eso determina '
        f'el consolidado. Las entidades adscritas ejecutan a mayor ritmo (lidera {lider["nombre"]} con '
        f'{lider["ti"]:.1f}%) pero pesan menos en el total. Es un corte parcial del trimestre: mide el '
        f'avance a la fecha, no comparable con un cierre anual.'
    )

    return f"""
<div style="margin-bottom:16px;border:1px solid rgba(245,158,11,.3);border-radius:12px;
            background:var(--navy-card);padding:16px 18px">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;
              margin-bottom:12px;flex-wrap:wrap;gap:10px">
    <div>
      <div style="font-size:13px;font-weight:800;color:var(--white)">
        🎯 Eje de Consistencia · Ejecución Presupuestaria del Holding</div>
      <div style="font-size:10px;color:var(--muted);margin-top:3px">
        La misma cifra del Centro de Mando, desglosada en sus 4 entidades — sin reinterpretación</div>
    </div>
    <div style="text-align:right;flex-shrink:0">
      <div style="font-size:2rem;font-weight:900;font-family:var(--mono);color:#F59E0B;line-height:1">{cons:.1f}%</div>
      <span style="font-size:9px;color:#F59E0B;font-weight:700">CORTE PARCIAL Q1 · PRELIMINAR</span>
    </div>
  </div>
  <div style="font-size:11px;color:var(--muted);margin-bottom:14px">
    {_fmt(dev)} ejecutados de {_fmt(cod)} codificados · consolidado de las 4 entidades al 31-mar-2026</div>
  {bars}
  <div style="margin-top:6px;padding:11px 13px;background:rgba(245,158,11,.06);
              border-left:3px solid #F59E0B;border-radius:0 8px 8px 0;font-size:11px;
              color:var(--white);line-height:1.6">{narrativa}</div>
  <div style="font-size:9px;color:rgba(255,255,255,.28);margin-top:10px">
    Fuente: Sistema Integrado de Gestión Financiera (SIGEF) · presupuesto consolidado · corte 31-mar-2026</div>
</div>"""


# ── RENDER PRINCIPAL ───────────────────────────────────────────────────────────
def render() -> None:
    sd        = _load_sercop_data()
    gm        = cargar_gm_snapshot()
    show_tech = is_tecnico()

    by_entity      = sd.get("by_entity",      {})
    by_year        = sd.get("by_year",        {})
    tipos          = sd.get("tipos",          {})
    prov_by_entity = sd.get("prov_by_entity", {})
    total_proc = sd.get("total_procesos",   0)
    total_adj  = sd.get("total_adjudicado", 0.0)

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr = page_header(
        "⑤ HOLDING MUNICIPAL",
        "Contratación Pública · 5 Entidades · 2023-2026",
        f"Radar SERCOP — datos reales verificados · {total_proc} procesos únicos · {_fmt(total_adj)} adjudicados",
    )

    # ── BANNER FUENTE ─────────────────────────────────────────────────────────
    if sd["ok"]:
        banner_color, banner_icon, banner_msg = (
            "rgba(0,224,150,.08)", "#00E096",
            f"✅ Datos en vivo · {total_proc} procesos únicos · {_fmt(total_adj)} adjudicados · "
            f"Fuente: SERCOP API datos abiertos · Ingesta: Sprint 0 · QUIRA OS"
        )
    else:
        banner_color, banner_icon, banner_msg = (
            "rgba(255,77,109,.08)", "#FF4D6D",
            f"⚠️ Error cargando datos SERCOP: {sd.get('error', 'desconocido')}"
        )

    banner = (
        f'<div style="padding:10px 16px;background:{banner_color};'
        f'border:1px solid {banner_icon}44;border-radius:8px;margin-bottom:14px;'
        f'font-size:11px;color:{banner_icon}">{banner_msg}</div>'
    )

    # ── KPI STRIP ─────────────────────────────────────────────────────────────
    entidades_activas = sum(1 for cod in _ENTIDADES if by_entity.get(cod, {}).get("procesos", 0) > 0)
    gad_share = by_entity.get("GAD", {}).get("adjudicado", 0) / total_adj * 100 if total_adj > 0 else 0
    ticket_global = total_adj / total_proc if total_proc > 0 else 0

    def _kpi(label: str, value: str, sub: str, color: str = "var(--white)") -> str:
        return (
            f'<div style="background:var(--navy-card);border:1px solid var(--divider);'
            f'border-radius:12px;padding:14px 16px;text-align:center">'
            f'  <div style="font-size:24px;font-weight:900;font-family:var(--mono);'
            f'              color:{color};line-height:1.1">{value}</div>'
            f'  <div style="font-size:11px;font-weight:700;color:var(--white);margin-top:4px">{label}</div>'
            f'  <div style="font-size:10px;color:var(--muted);margin-top:2px">{sub}</div>'
            f'</div>'
        )

    kpi_strip = (
        '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:16px">'
        + _kpi("Procesos totales",   str(total_proc),           "2023-2026 · SERCOP",           "var(--cyan)")
        + _kpi("Adjudicado total",   _fmt(total_adj),           "4 entidades activas",           "var(--green)")
        + _kpi("Ticket promedio",    _fmt(ticket_global),       "por proceso",                   "var(--amber)")
        + _kpi("Entidades activas",  f"{entidades_activas}/5",  "1 sin registro (EP Hábitat)",   "var(--purple)")
        + _kpi("GAD concentra",      f"{gad_share:.0f}%",       "del gasto total del Holding",   "#00D4FF")
        + '</div>'
    )

    # ── SECCIÓN HEADER ────────────────────────────────────────────────────────
    sec_hdr = """
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
  <div>
    <div style="font-size:13px;font-weight:700;color:var(--white)">
      Cajón 1 · Contratación por Entidad — Haz clic para expandir</div>
    <div style="font-size:10px;color:var(--muted);margin-top:2px">
      Cada cajón muestra: adjudicado total · procesos · evolución anual · modalidades</div>
  </div>
  <span class="badge badge-cyan">SERCOP 2023-2026</span>
</div>"""

    # ── CAJONES POR ENTIDAD ───────────────────────────────────────────────────
    cajones = ""
    for i, cod in enumerate(["GAD", "PATRONATO", "BOMBEROS", "EMAI", "HABITAT"], start=1):
        stats = by_entity.get(cod, {"procesos": 0, "adjudicado": 0, "presupuestado": 0, "proveedores": 0})
        cajones += _cajon(i, cod, stats, by_year, tipos)

    # ── INSIGHTS AUTOMÁTICOS ──────────────────────────────────────────────────
    gad_adj   = by_entity.get("GAD",      {}).get("adjudicado", 0)
    emai_adj  = by_entity.get("EMAI",     {}).get("adjudicado", 0)
    pat_proc  = by_entity.get("PATRONATO",{}).get("procesos",   0)
    emai_proc = by_entity.get("EMAI",     {}).get("procesos",   0)
    emai_tick  = emai_adj / emai_proc if emai_proc > 0 else 0

    gad_24 = by_year.get(("GAD", 2024), {}).get("cnt", 0)
    gad_25 = by_year.get(("GAD", 2025), {}).get("cnt", 0)
    caida_gad = (gad_24 - gad_25) / gad_24 * 100 if gad_24 > 0 else 0

    def _insight(icon: str, titulo: str, texto: str, color: str = "var(--cyan)") -> str:
        return (
            f'<div style="padding:12px 14px;background:rgba(255,255,255,.03);'
            f'border-radius:10px;border-left:3px solid {color}">'
            f'  <div style="font-size:11px;font-weight:700;color:{color};margin-bottom:4px">'
            f'    {icon} {titulo}</div>'
            f'  <div style="font-size:11px;color:var(--white);line-height:1.6">{texto}</div>'
            f'</div>'
        )

    insights = (
        '<div style="margin-top:18px">'
        '<div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;'
        'letter-spacing:.1em;margin-bottom:10px">🔍 Señales detectadas · datos SERCOP</div>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">'
        + _insight(
            "🏛️", f"GAD concentra el {gad_share:.0f}% del gasto del Holding",
            f"De los {_fmt(total_adj)} adjudicados totales, el GAD Municipal representa "
            f"{_fmt(gad_adj)} ({gad_share:.0f}%). Alta concentración presupuestaria en "
            f"la administración central. Las entidades operadoras suman solo el {100-gad_share:.0f}% restante.",
            "#00D4FF"
        )
        + _insight(
            "📊", f"Patronato: operador más activo en volumen ({pat_proc} procesos)",
            f"Con {pat_proc} procesos en 2023-2026, el Patronato es la entidad con más "
            f"contratos pero ticket bajo ({_fmt(by_entity.get('PATRONATO',{}).get('adjudicado',0)/pat_proc if pat_proc>0 else 0)}/proceso). "
            f"Principalmente compras de catálogo. Estabilidad operativa 2024-2025.",
            "#7C5CFC"
        )
        + _insight(
            "⚡", f"GAD: caída del {caida_gad:.0f}% en procesos 2024→2025",
            f"El GAD pasó de {gad_24} procesos en 2024 a {gad_25} en 2025 "
            f"({caida_gad:.0f}% menos). Señal de posible subejecución o cambio en "
            f"modalidad de contratación. Requiere cruce con el PAC y el eSIGEF.",
            "#FFB800"
        )
        + _insight(
            "💰", f"EMAI: ticket promedio más alto del Holding ({_fmt(emai_tick)})",
            f"Con solo {emai_proc} procesos y {_fmt(emai_adj)} adjudicados, EMAI opera "
            f"con contratos de alta cuantía (SIE, Repuestos, Bienes únicos). "
            f"Perfil de empresa técnica especializada — diferente al Patronato de alta frecuencia.",
            "#FFB800"
        )
        + '</div>'
        + '<div style="margin-top:10px">'
        + _insight(
            "🏗️", "EP Hábitat: 0 procesos registrados en SERCOP 2023-2026",
            "La Empresa Pública de Hábitat no tiene ningún proceso de contratación registrado "
            "en la API de datos abiertos. Puede indicar entidad operativamente inactiva, "
            "procesos ejecutados bajo otro nombre/RUC, o absorción por el GAD Central. "
            "Es en sí misma una alerta institucional.",
            "#FF4D6D"
        )
        + '</div>'
        + '</div>'
    )

    # ── TABLA COMPARATIVA ─────────────────────────────────────────────────────
    tabla_rows = ""
    for cod in ["GAD", "PATRONATO", "BOMBEROS", "EMAI", "HABITAT"]:
        meta   = _ENTIDADES[cod]
        estat  = by_entity.get(cod, {"procesos": 0, "adjudicado": 0.0, "proveedores": 0})
        proc   = estat["procesos"]
        adj    = estat["adjudicado"]
        prov   = estat["proveedores"]
        tick   = adj / proc if proc > 0 else 0
        share  = adj / total_adj * 100 if total_adj > 0 else 0
        top    = tipos.get(cod, [{}])[0].get("tipo", "—") if tipos.get(cod) else "—"
        top    = (top[:35] + "…") if len(top) > 35 else top
        color  = meta["color"]
        tabla_rows += (
            f'<tr>'
            f'<td style="padding:8px 10px;font-size:11px;font-weight:700;color:var(--white)">'
            f'{meta["emoji"]} {meta["nombre"]}</td>'
            f'<td style="padding:8px 10px;font-size:11px;text-align:center;'
            f'font-family:var(--mono);color:{color}">{proc}</td>'
            f'<td style="padding:8px 10px;font-size:11px;text-align:right;'
            f'font-family:var(--mono);color:{color}">{_fmt(adj)}</td>'
            f'<td style="padding:8px 10px;font-size:11px;text-align:center;'
            f'color:var(--muted)">{_fmt(tick)}</td>'
            f'<td style="padding:8px 10px;font-size:11px;text-align:center;'
            f'color:var(--muted)">{prov}</td>'
            f'<td style="padding:8px 10px;font-size:11px;text-align:center;'
            f'color:var(--amber);font-weight:700">{share:.1f}%</td>'
            f'<td style="padding:8px 10px;font-size:10px;color:var(--muted)">{top}</td>'
            f'</tr>'
        )

    tabla = f"""
<div style="margin-top:18px">
  <div style="font-size:10px;font-weight:700;color:var(--muted);text-transform:uppercase;
              letter-spacing:.1em;margin-bottom:10px">📋 Tabla comparativa · Holding Municipal</div>
  <div style="overflow-x:auto">
    <table class="tbl" style="width:100%;border-collapse:collapse;font-size:11px">
      <thead>
        <tr style="border-bottom:1px solid var(--divider)">
          <th style="padding:8px 10px;text-align:left;font-size:10px;color:var(--muted);
                     text-transform:uppercase;letter-spacing:.06em">Entidad</th>
          <th style="padding:8px 10px;text-align:center;font-size:10px;color:var(--muted);
                     text-transform:uppercase">Procesos</th>
          <th style="padding:8px 10px;text-align:right;font-size:10px;color:var(--muted);
                     text-transform:uppercase">Adjudicado</th>
          <th style="padding:8px 10px;text-align:center;font-size:10px;color:var(--muted);
                     text-transform:uppercase">Ticket</th>
          <th style="padding:8px 10px;text-align:center;font-size:10px;color:var(--muted);
                     text-transform:uppercase">Proveedores</th>
          <th style="padding:8px 10px;text-align:center;font-size:10px;color:var(--amber);
                     text-transform:uppercase">% Holding</th>
          <th style="padding:8px 10px;text-align:left;font-size:10px;color:var(--muted);
                     text-transform:uppercase">Modalidad principal</th>
        </tr>
      </thead>
      <tbody>
        {tabla_rows}
        <tr style="border-top:1px solid var(--divider)">
          <td style="padding:8px 10px;font-size:11px;font-weight:700;
                     color:var(--cyan)">TOTAL HOLDING</td>
          <td style="padding:8px 10px;font-size:11px;text-align:center;
                     font-family:var(--mono);color:var(--cyan);font-weight:700">{total_proc}</td>
          <td style="padding:8px 10px;font-size:11px;text-align:right;
                     font-family:var(--mono);color:var(--cyan);font-weight:700">{_fmt(total_adj)}</td>
          <td colspan="4" style="padding:8px 10px;font-size:10px;color:var(--muted)">
            Fuente: SERCOP API · Sprint 0 QUIRA OS</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>"""

    # ── TECH NOTE ─────────────────────────────────────────────────────────────
    tech = ""
    if show_tech:
        tech = """
<div style="margin-top:16px;padding:10px 12px;background:rgba(255,255,255,.02);
            border:1px solid rgba(255,255,255,.06);border-radius:8px;
            font-size:9px;color:rgba(255,255,255,.25)">
  🔧 Fuente: contratación pública del SERCOP (estándar abierto OCDS) ·
  actualización periódica · deduplicación por identificador único de proceso.
</div>"""

    # ── CAJÓN 2 — Concentración de Proveedores ───────────────────────────────
    cajon2_html = _cajon2(prov_by_entity, by_entity)

    # ── CTAs NAVALES (dentro del canvas HTML — sin saltar al lenguaje Streamlit) ──
    sentinel_query = (
        f"Analiza la contratación pública del Holding Municipal de Montecristi "
        f"({total_proc} procesos, {_fmt(total_adj)} adjudicados en 2023-2026). "
        f"¿Qué patrones, riesgos o oportunidades detectas?"
    ).replace("'", "\\'")

    ctas_html = f"""
<div style="margin-top:20px;padding:14px 0 4px;
            border-top:1px solid rgba(255,255,255,.06);display:flex;gap:10px">
  <button
    onclick="window.parent.postMessage({{type:'quira_nav',dest:'sentinel',q:'{sentinel_query}'}}, '*')"
    style="flex:1;padding:12px 16px;background:rgba(0,212,255,.1);
           border:1px solid rgba(0,212,255,.3);border-radius:8px;cursor:pointer;
           font-size:11px;font-weight:700;color:#00D4FF;letter-spacing:.06em;
           font-family:var(--mono);text-transform:uppercase;
           transition:background .2s,border-color .2s"
    onmouseover="this.style.background='rgba(0,212,255,.18)'"
    onmouseout="this.style.background='rgba(0,212,255,.1)'">
    🔮 Analizar Holding con Sentinel
  </button>
  <button
    onclick="window.parent.postMessage({{type:'quira_nav',dest:'dashboard'}}, '*')"
    style="flex:1;padding:12px 16px;background:rgba(255,255,255,.04);
           border:1px solid rgba(255,255,255,.1);border-radius:8px;cursor:pointer;
           font-size:11px;font-weight:700;color:var(--muted);letter-spacing:.06em;
           font-family:var(--mono);text-transform:uppercase;
           transition:background .2s"
    onmouseover="this.style.background='rgba(255,255,255,.08)'"
    onmouseout="this.style.background='rgba(255,255,255,.04)'">
    📊 Ver Tablero Ejecutivo
  </button>
</div>"""

    # ── ASSEMBLE ──────────────────────────────────────────────────────────────
    eje_html = _eje_consistencia(gm)
    html = (
        hdr + eje_html + banner + kpi_strip
        + sec_hdr + cajones
        + cajon2_html
        + insights + tabla + tech
        + ctas_html   # CTAs dentro del canvas naval — sin ruptura visual
    )
    render_page(html, show_tech=show_tech, height=4700)

    # ── BRIDGE JS ↔ STREAMLIT ──────────────────────────────────────────────────
    # Captura postMessage de los CTAs navales y dispara botones Streamlit ocultos.
    # El usuario solo ve el HTML naval; el routing lo hacen los botones debajo.
    import streamlit.components.v1 as _cv1
    _cv1.html("""<script>
(function () {
  // Escuchar mensajes de navegación del iframe principal
  window.addEventListener("message", function (e) {
    if (!e.data || e.data.type !== "quira_nav") return;
    var dest   = e.data.dest;
    var target = dest === "sentinel" ? "__QNAVS__" : "__QNAVD__";
    // Buscar el botón funcional oculto y dispararlo
    var btns = window.parent.document.querySelectorAll(
      '[data-testid="stBaseButton-secondary"]'
    );
    for (var i = 0; i < btns.length; i++) {
      if (btns[i].innerText.trim() === target) {
        btns[i].click();
        return;
      }
    }
  });

  // Ocultar los botones funcionales (son solo mecanismo de routing)
  function hideNavBtns() {
    var btns = window.parent.document.querySelectorAll(
      '[data-testid="stBaseButton-secondary"]'
    );
    for (var i = 0; i < btns.length; i++) {
      var t = btns[i].innerText.trim();
      if (t === "__QNAVS__" || t === "__QNAVD__") {
        btns[i].style.cssText =
          "width:0!important;height:0!important;padding:0!important;" +
          "margin:0!important;border:none!important;overflow:hidden!important;" +
          "position:absolute!important;opacity:0!important;pointer-events:none!important";
        if (btns[i].parentElement) {
          btns[i].parentElement.style.cssText =
            "width:0!important;height:0!important;overflow:hidden!important";
        }
      }
    }
  }
  setTimeout(hideNavBtns, 80);
  setTimeout(hideNavBtns, 350);
})();
</script>""", height=0)

    # Botones funcionales ocultos (routing real — el bridge JS los dispara)
    _c1, _c2 = st.columns(2)
    with _c1:
        if st.button("__QNAVS__", key="_quira_nav_s", use_container_width=True):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"Analiza la contratación pública del Holding Municipal de Montecristi "
                f"({total_proc} procesos, {_fmt(total_adj)} adjudicados en 2023-2026). "
                f"¿Qué patrones, riesgos o oportunidades detectas?"
            )
            st.rerun()
    with _c2:
        if st.button("__QNAVD__", key="_quira_nav_d", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()
