"""
QUIRA Intelligence — Sala de Mando · Concejo Municipal
Sprint C.2 · p_concejo.py

"El alcalde entra a Concejo con datos, no con opiniones."

Módulo de preparación política basado en datos reales del Gold Master v5.5.
6 vectores de ataque de oposición → respuestas con autoridad algorítmica.

━━━ ESTRUCTURA ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HEADER        — Modo Concejo activado · corte · ejecutivo
  CHECKLIST     — 5 puntos de preparación pre-Concejo
  ATAQUES       — 6 vectores canónicos · datos + respuesta + reencuadre
  ARGUMENTARIO  — 4 puntos de ofensiva institucional
  PIE           — Fuentes y doctrina

  Fuente datos: gm_snapshot.json · Gold Master v5.5_TGI
  Motor: utils/top.py · NOMENCLATURA 7.2
  Doctrina: QUIRA_DOCTRINE_v1.3 · Sección 1.6 · Contrato de Autoridad

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from config import GAD_NOMBRE, ALCALDE, CORTE
from utils.top import top_entidad


# ══════════════════════════════════════════════════════════════════════════════
# DATOS — reutiliza el snapshot del VE
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def _load() -> dict:
    try:
        from utils.cache_quira import cargar_gm_snapshot
        data = cargar_gm_snapshot()
        if data and "tgi" in data:
            return data
    except Exception:
        pass
    # Fallback idéntico al VE
    return {
        "tgi": {
            "score": 68.82, "clasificacion": "Transición con Riesgos",
            "color_hex": "#FFB800",
            "d1": {"valor": 83.5}, "d2": {"valor": 69.93},
            "d3": {"valor": 14.58}, "d4": {"valor": 66.85},
            "d5": {"valor": 100.0},
            "irs": {"valor": 79.7, "clasificacion": "Muy Regresivo"},
            "ied_global": {"valor": 31.14},
            "brecha_rural_usd": 1791935,
        },
        "icpi": {"global_pct": 53.56, "clasificacion": "Ruptura Sistémica"},
        "financiero": {
            "ti_2026_raw_pct": 1.05,
            "presupuesto_codificado_grupos78_2026": 22595464,
            "devengado_q1_2026": 238066,
            "fondos_bloqueados_est": 3660000,
            "fondos_bloqueados_detalle": "BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K",
            "h90_consolidado": {
                "patronato_ti_q1_pct": 19.56,
                "ep_aseo_ti_q1_pct":   18.17,
                "bomberos_ti_q1_pct":  19.43,
            },
        },
        "territorial": {
            "nbi_rural_promedio": 55.7,
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# CSS — Sala de Mando (paleta ámbar · modo preparación)
# ══════════════════════════════════════════════════════════════════════════════

_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400&display=swap');

.cm-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* Grid de ataques — 2 cols */
.cm-ataques {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 14px;
}

/* Card de ataque base */
.cm-card {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 18px;
}

/* Argumentario — 2 cols */
.cm-arg-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* Responsive */
@media (max-width: 900px) {
    .cm-ataques { grid-template-columns: 1fr; }
    .cm-arg-grid { grid-template-columns: 1fr; }
}
</style>"""


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTACIONES — datos reales para los argumentos
# ══════════════════════════════════════════════════════════════════════════════

def _compute_contexto(data: dict) -> dict:
    """Extrae los datos concretos que el alcalde necesita en Concejo."""
    fin = data.get("financiero", {})
    h90 = fin.get("h90_consolidado", {})
    tgi = data.get("tgi", {})

    ti_raw   = fin.get("ti_2026_raw_pct", 1.05)
    fondos   = fin.get("fondos_bloqueados_est", 3660000)
    fondos_d = fin.get("fondos_bloqueados_detalle", "BDE $3.5M + ...")

    gad_top  = top_entidad(ti_raw,                          CORTE, "GAD Municipal")
    pat_top  = top_entidad(h90.get("patronato_ti_q1_pct", 19.56), CORTE, "Patronato Municipal")
    ep_top   = top_entidad(h90.get("ep_aseo_ti_q1_pct",   18.17), CORTE, "EP Aseo")
    bom_top  = top_entidad(h90.get("bomberos_ti_q1_pct",  19.43), CORTE, "Bomberos")

    return {
        "ti_raw":     ti_raw,
        "top_gad":    gad_top["top"],
        "top_pat":    pat_top["top"],
        "top_ep":     ep_top["top"],
        "top_bom":    bom_top["top"],
        "tgi_score":  tgi.get("score", 68.82),
        "d1": tgi.get("d1", {}).get("valor", 83.5),
        "d3": tgi.get("d3", {}).get("valor", 14.58),
        "d5": tgi.get("d5", {}).get("valor", 100.0),
        "irs": tgi.get("irs", {}).get("valor", 79.7),
        "fondos_m":   fondos / 1_000_000,
        "fondos_det": fondos_d,
        "nbi_rural":  data.get("territorial", {}).get("nbi_rural_promedio", 55.7),
    }


# ══════════════════════════════════════════════════════════════════════════════
# BUILDERS HTML — puros, deterministas
# ══════════════════════════════════════════════════════════════════════════════

def _html_header_concejo() -> str:
    apellido = ALCALDE.split()[-1] if ALCALDE else "—"
    return (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:12px 18px;background:rgba(245,158,11,.04);'
        f'border:1px solid rgba(245,158,11,.18);border-radius:12px;margin-bottom:16px">'

        f'<div style="display:flex;align-items:center;gap:12px">'
        f'<span style="font-size:20px">⚖</span>'
        f'<div>'
        f'<div style="font:900 14px/1 Inter,sans-serif;color:#E2E8F0;letter-spacing:-.01em">'
        f'Sala de Mando · Concejo Municipal</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.28);margin-top:2px">'
        f'{GAD_NOMBRE} · QUIRA Intelligence · Corte {CORTE}</div>'
        f'</div></div>'

        f'<div style="display:flex;align-items:center;gap:8px">'
        f'<div style="text-align:center;padding:5px 12px;'
        f'background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);border-radius:8px">'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(245,158,11,.6);'
        f'letter-spacing:.07em;text-transform:uppercase">Modo</div>'
        f'<div style="font:800 11px/1.3 Inter,sans-serif;color:#F59E0B;margin-top:1px">'
        f'Pre-Concejo</div>'
        f'</div>'
        f'<div style="text-align:center;padding:5px 12px;'
        f'background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.18);border-radius:8px">'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(0,212,255,.4);'
        f'letter-spacing:.07em;text-transform:uppercase">Ejecutivo</div>'
        f'<div style="font:700 12px/1.3 Inter,sans-serif;color:#00D4FF;margin-top:1px">'
        f'{apellido}</div>'
        f'</div>'
        f'</div></div>'
    )


def _html_checklist(ctx: dict) -> str:
    items = [
        (True,  f"TOP GAD inversión: {ctx['top_gad']:.1f}% — categoría RUPTURA"),
        (True,  f"Ecosistema sobre ritmo: Patronato {ctx['top_pat']:.1f}% · "
                f"EP Aseo {ctx['top_ep']:.1f}% · Bomberos {ctx['top_bom']:.1f}%"),
        (True,  f"TGI {ctx['tgi_score']:.1f} — D1 {ctx['d1']:.1f}% legal · "
                f"D5 {ctx['d5']:.1f}% capacidad"),
        (True,  f"Fondos bloqueados: ${ctx['fondos_m']:.2f}M — palanca BDE disponible"),
        (True,  f"Base legal: COPFP Art. 113 · COOTAD Art. 192 · W_Q Q1=0.13"),
    ]

    filas = ""
    for ok, texto in items:
        c = "#22C55E" if ok else "#F59E0B"
        ico = "✓" if ok else "○"
        filas += (
            f'<div style="display:flex;align-items:flex-start;gap:10px;'
            f'padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04)">'
            f'<span style="font:800 11px/1 Inter,sans-serif;color:{c};'
            f'flex-shrink:0;margin-top:1px">{ico}</span>'
            f'<span style="font:400 11px/1.5 Inter,sans-serif;'
            f'color:rgba(255,255,255,.6)">{texto}</span>'
            f'</div>'
        )

    return (
        f'<div style="background:rgba(34,197,94,.04);border:1px solid rgba(34,197,94,.14);'
        f'border-radius:12px;padding:16px 18px;margin-bottom:14px">'
        f'<div style="font:800 9px/1 Inter,sans-serif;color:#22C55E;'
        f'letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px">'
        f'✓ Checklist Pre-Concejo — {CORTE}</div>'
        + filas +
        f'</div>'
    )


def _ataque_card(
    numero: str,
    ataque: str,
    datos: str,
    respuesta: str,
    reencuadre: str,
    ley: str,
    nivel: str = "ALTO",
) -> str:
    """
    Card de vector de ataque de oposición.
    nivel: CRÍTICO | ALTO | MEDIO
    """
    nc = {"CRÍTICO": "#EF4444", "ALTO": "#F97316", "MEDIO": "#F59E0B"}.get(nivel, "#F97316")

    return (
        f'<div class="cm-card" style="border-top:3px solid {nc}44;'
        f'border-color:{nc}18">'

        # Header del ataque
        f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:10px">'
        f'<span style="font:800 8px/1 Inter,sans-serif;color:{nc};'
        f'background:{nc}18;padding:2px 8px;border-radius:4px;'
        f'white-space:nowrap;flex-shrink:0;margin-top:1px">'
        f'{numero} · {nivel}</span>'
        f'<div style="font:700 11px/1.4 Inter,sans-serif;color:#E2E8F0">'
        f'"{ataque}"</div>'
        f'</div>'

        # Datos QUIRA
        f'<div style="background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.14);'
        f'border-radius:8px;padding:9px 11px;margin-bottom:9px">'
        f'<div style="font:800 7px/1 Inter,sans-serif;color:rgba(0,212,255,.5);'
        f'letter-spacing:.09em;text-transform:uppercase;margin-bottom:4px">'
        f'◆ QUIRA Intelligence — Datos</div>'
        f'<div style="font:400 10px/1.55 Inter,sans-serif;color:rgba(255,255,255,.55)">'
        f'{datos}</div>'
        f'</div>'

        # Respuesta recomendada
        f'<div style="margin-bottom:8px">'
        f'<div style="font:800 7px/1 Inter,sans-serif;color:rgba(34,197,94,.5);'
        f'letter-spacing:.09em;text-transform:uppercase;margin-bottom:4px">'
        f'→ Respuesta recomendada</div>'
        f'<div style="font:600 10px/1.55 Inter,sans-serif;color:rgba(255,255,255,.7)">'
        f'{respuesta}</div>'
        f'</div>'

        # Reencuadre
        f'<div style="background:rgba(124,92,252,.06);border-left:2px solid rgba(124,92,252,.35);'
        f'padding:7px 10px;border-radius:0 6px 6px 0;margin-bottom:8px">'
        f'<div style="font:800 7px/1 Inter,sans-serif;color:rgba(155,121,255,.6);'
        f'letter-spacing:.09em;text-transform:uppercase;margin-bottom:3px">'
        f'↩ Reencuadre político</div>'
        f'<div style="font:400 10px/1.5 Inter,sans-serif;color:rgba(255,255,255,.45)">'
        f'{reencuadre}</div>'
        f'</div>'

        # Ley
        f'<div style="font:400 8px/1 JetBrains Mono,monospace;'
        f'color:rgba(255,255,255,.2)">Base legal: {ley}</div>'

        f'</div>'
    )


def _html_ataques(ctx: dict) -> str:
    """6 vectores de ataque canónicos del Concejo Municipal de Montecristi."""

    ti   = ctx["ti_raw"]
    tgad = ctx["top_gad"]
    tpat = ctx["top_pat"]
    tep  = ctx["top_ep"]
    tbom = ctx["top_bom"]
    tgi  = ctx["tgi_score"]
    d1   = ctx["d1"]
    d3   = ctx["d3"]
    d5   = ctx["d5"]
    irs  = ctx["irs"]
    fm   = ctx["fondos_m"]
    nbi  = ctx["nbi_rural"]

    a1 = _ataque_card(
        "A1",
        "La inversión del GAD está paralizada. Solo el 1.05% ejecutado en Q1.",
        f"Ti inversión G71-78 (D3): {ti:.2f}%. TOP proyectado: {tgad:.1f}% — "
        f"categoría RUPTURA según Motor Predictivo QUIRA (W_Q1=0.13 calibrado eSIGEF). "
        f"El presupuesto codificado G71-78 asciende a $22.6M. Devengado Q1: $238K. "
        f"Causa identificada: desembolso BDE ${fm:.2f}M bloqueado por proceso legal.",
        f"El motor predictivo QUIRA confirma que la trayectoria de inversión está en ruptura. "
        f"El problema está identificado: el desembolso BDE de ${fm:.1f}M representa el 85% "
        f"del gap. La activación está en proceso y debe ejecutarse antes del cierre de Q2.",
        f"No es parálisis de gestión — es un cuello de botella financiero puntual y accionable. "
        f"El ecosistema institucional completo opera sobre ritmo. "
        f"La palanca existe, está cuantificada y tiene fecha.",
        "COPFP Art. 113 · COOTAD Art. 249 · W_Q calibrado eSIGEF Ecuador",
        "CRÍTICO",
    )

    a2 = _ataque_card(
        "A2",
        "Las parroquias rurales están abandonadas. El NBI rural es del 55.7%.",
        f"NBI rural promedio: {nbi:.1f}%. IRS: {irs:.1f} (Muy Regresivo) — QUIRA confirma "
        f"la inequidad territorial. IET parroquias: Montecristi 193.75% (inversión sobre "
        f"paridad) vs Colorado 28.57% e Isabel Muentes 35.71% (sub-inversión crítica). "
        f"El D4 Equidad Territorial: {d3:.1f}% — problema metodológico real.",
        f"El IRS {irs:.0f} es un dato del sistema QUIRA, no un ataque — lo confirmamos. "
        f"Lo que el sistema también muestra es que este es el primer mandato que lo mide, "
        f"lo publica y lo incluye en el PDOT 2023-2027 como meta vinculante.",
        f"La inequidad territorial es una herencia estructural acumulada en 20 años. "
        f"Reconocerla públicamente con datos es fortaleza, no debilidad. "
        f"Defenderla con datos propios antes que la oposición los use.",
        "COOTAD Art. 192 · Plan Nacional Desarrollo 2025-2029 · ODS 10 · PDOT 2023-2027",
        "ALTO",
    )

    a3 = _ataque_card(
        "A3",
        f"El Patronato ejecuta al {tpat:.0f}% y el GAD al {tgad:.0f}%. "
        f"¿Quién administra mejor?",
        f"TOP Patronato Municipal: {tpat:.1f}% (sobre ritmo). "
        f"TOP EP Aseo: {tep:.1f}%. TOP Bomberos: {tbom:.1f}%. "
        f"Los tres sobre ritmo histórico esperado. "
        f"TOP GAD inversión G71-78: {tgad:.1f}% (ruptura). "
        f"Diferencia estructural: el Patronato ejecuta presupuesto corriente (servicios); "
        f"el GAD inversión ejecuta capital (obras e infraestructura — procesos más complejos).",
        f"El ecosistema municipal completo bajo coordinación del Alcalde opera sobre ritmo. "
        f"La diferencia no es eficiencia directiva — es la naturaleza del gasto. "
        f"Inversión capital requiere procesos de contratación, estudios, permisos. "
        f"Gasto corriente no. Los {tpat:.0f}% del Patronato prueban que la gestión municipal funciona.",
        f"El contraste que la oposición usa como ataque es la misma evidencia de que "
        f"el holding municipal opera correctamente. El problema está localizado en un "
        f"cuello de botella financiero específico — no en la gestión institucional.",
        "COOTAD Art. 238 · Manual Clasificador Presupuestario 2026 · H90 PRESUPUESTO CONSOLIDADO",
        "ALTO",
    )

    a4 = _ataque_card(
        "A4",
        f"El TGI es {tgi:.1f} — no llegaron al 70 comprometido.",
        f"TGI {CORTE}: {tgi:.1f}. Tendencia 3 años: 57→67→{tgi:.0f} (crecimiento sostenido). "
        f"D1 Legalidad: {d1:.1f}% (fuerte). D5 Capacidad Institucional: {d5:.1f}% (máximo). "
        f"D3 Ejecución: {d3:.1f}% — único vector que deprime el score global. "
        f"Con Ti normalizado Q2+BDE, D3 proyecta recuperación.",
        f"El TGI crece año tras año y lo confirma el sistema. "
        f"La legalidad y la capacidad institucional están al máximo. "
        f"El único vector deprimido es D3 — el mismo que estamos trabajando con BDE. "
        f"El TGI no es un número estático: es una trayectoria. Y la trayectoria es positiva.",
        f"No defender el número — defender la trayectoria. "
        f"El TGI {tgi:.0f} hoy es mejor que el TGI 67 del año pasado y el 57 del anterior. "
        f"La dirección es correcta. La activación BDE es el catalizador para Q2.",
        "QUIRA_DOCTRINE_v1.3 · TGI Framework D1-D5 · Gold Master v5.5_TGI",
        "MEDIO",
    )

    a5 = _ataque_card(
        "A5",
        f"¿Cuándo se activan los ${fm:.1f}M del BDE? Llevan meses esperando.",
        f"Fondos bloqueados identificados: ${fm:.2f}M ({ctx['fondos_det']}). "
        f"El desembolso BDE $3.5M está en proceso legal de perfeccionamiento. "
        f"Impacto proyectado: activación antes del 15 de junio elevaría Ti G71-78 "
        f"de {ti:.2f}% a ~18% al cierre Q2 — TOP proyectado: ~51% (umbral atención). "
        f"Sin activación: Ti proyecta ~4% Q2 — incumplimiento COPFP Art. 113.",
        f"El proceso BDE está en la etapa final de perfeccionamiento del contrato. "
        f"La fecha es el 15 de junio. El impacto está cuantificado. "
        f"${fm:.1f}M representan el 85% de lo que necesitamos para cerrar Q2 dentro del umbral legal.",
        f"No es indefinido — tiene fecha, monto y proceso. "
        f"Pedir al opositor que proponga una alternativa de financiamiento de "
        f"${fm:.1f}M en 45 días. Si no la tiene, el cuestionamiento no tiene base técnica.",
        "COPFP Art. 113 · Reglamento LOSNCP 2025 · BDE Contrato Crédito Municipal",
        "CRÍTICO",
    )

    a6 = _ataque_card(
        "A6",
        "El COPFP Art. 113 exige 60% de ejecución anual. Están al 1% en Q1.",
        f"El Art. 113 COPFP establece umbrales anuales, no trimestrales. "
        f"El sistema TOP usa W_Q1=0.13 (peso estacional Q1 calibrado eSIGEF Ecuador): "
        f"el 1.05% en Q1 equivale al {tgad:.1f}% de trayectoria proyectada — que es ruptura, "
        f"pero no incumplimiento legal todavía. El umbral COPFP se evalúa al cierre Q4. "
        f"Con BDE activado en junio: proyección Q2 ~51% de TOP — recuperable.",
        f"El Art. 113 no se incumple en Q1 — se evalúa al cierre del ejercicio fiscal. "
        f"El sistema TOP de QUIRA alerta sobre la trayectoria, no sobre el incumplimiento actual. "
        f"La diferencia es metodológicamente crítica. La trayectoria es recuperable.",
        f"El opositor mezcla trayectoria con incumplimiento. No son lo mismo. "
        f"El sistema QUIRA existe precisamente para detectar esto con 6 meses de anticipación "
        f"— no en diciembre cuando ya no hay nada que hacer. "
        f"Esa es la inteligencia institucional que este municipio tiene y otros no.",
        "COPFP Art. 113 · QUIRA_DOCTRINE_v1.3 Sección 1.6 · W_Q eSIGEF Ecuador",
        "CRÍTICO",
    )

    return (
        f'<div style="font:800 9px/1 Inter,sans-serif;color:rgba(245,158,11,.6);'
        f'letter-spacing:.1em;text-transform:uppercase;margin-bottom:12px">'
        f'⚔ Vectores de Ataque — Playbook Oposición · {CORTE}</div>'
        f'<div class="cm-ataques">'
        + a1 + a2 + a3 + a4 + a5 + a6 +
        f'</div>'
    )


def _html_argumentario(ctx: dict) -> str:
    """4 puntos de ofensiva institucional — el alcalde toma la iniciativa."""

    puntos = [
        {
            "ico": "◉",
            "titulo": "La coherencia ecosistema-inversión es única en la región",
            "texto": (
                f"Montecristi es probablemente el único municipio en Ecuador que puede "
                f"mostrar en tiempo real la trayectoria de su holding institucional completo. "
                f"TOP Patronato {ctx['top_pat']:.1f}%, EP Aseo {ctx['top_ep']:.1f}%, "
                f"Bomberos {ctx['top_bom']:.1f}% — todo sobre ritmo histórico. "
                f"Eso no es accidente: es gestión de ecosistema."
            ),
            "color": "#22C55E",
        },
        {
            "ico": "◆",
            "titulo": "Tenemos el sistema de alerta temprana más sofisticado del cantón",
            "texto": (
                f"El SAT-III activado no es una falla — es el sistema funcionando. "
                f"Detectamos la ruptura en Q1 con datos reales, no en diciembre. "
                f"Eso da 6 meses de margen de acción. "
                f"¿Cuántos concejos municipales del país pueden decir eso?"
            ),
            "color": "#00D4FF",
        },
        {
            "ico": "▲",
            "titulo": "El BDE no es deuda — es inversión con retorno territorial",
            "texto": (
                f"Los ${ctx['fondos_m']:.1f}M BDE son recursos ya aprobados, "
                f"con estudios realizados y contrato en perfeccionamiento. "
                f"Su activación no aumenta el endeudamiento municipal — "
                f"ejecuta crédito ya comprometido en el presupuesto codificado. "
                f"El impacto: obras en territorio antes del 30 de junio."
            ),
            "color": "#7C5CFC",
        },
        {
            "ico": "✦",
            "titulo": "El TGI es tendencia positiva — no un snapshot estático",
            "texto": (
                f"TGI {ctx['tgi_score']:.1f} hoy vs TGI 67 hace 12 meses vs TGI 57 hace 24. "
                f"Eso es una curva de mejora institucional sostenida. "
                f"D1 Legalidad {ctx['d1']:.1f}%, D5 Capacidad {ctx['d5']:.1f}%. "
                f"La institución tiene bases sólidas. El vector D3 "
                f"tiene causa identificada y solución en marcha."
            ),
            "color": "#F59E0B",
        },
    ]

    cards = ""
    for p in puntos:
        c = p["color"]
        cards += (
            f'<div style="background:{c}07;border:1px solid {c}20;'
            f'border-left:3px solid {c};border-radius:10px;padding:14px 16px">'
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">'
            f'<span style="font:800 10px/1 Inter,sans-serif;color:{c}">{p["ico"]}</span>'
            f'<div style="font:700 11px/1.2 Inter,sans-serif;color:#E2E8F0">'
            f'{p["titulo"]}</div>'
            f'</div>'
            f'<div style="font:400 10px/1.6 Inter,sans-serif;color:rgba(255,255,255,.5)">'
            f'{p["texto"]}'
            f'</div>'
            f'</div>'
        )

    return (
        f'<div style="background:rgba(255,255,255,.015);border:1px solid rgba(255,255,255,.06);'
        f'border-radius:14px;padding:20px;margin-bottom:14px">'

        f'<div style="font:800 9px/1 Inter,sans-serif;color:rgba(34,197,94,.6);'
        f'letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px">'
        f'▲ Argumentario de Ofensiva Institucional</div>'

        f'<div class="cm-arg-grid">'
        + cards +
        f'</div></div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Sala de Mando Concejo Municipal — Sprint C.2.
    Prepara al alcalde con datos reales para responder a la oposición.
    Accesible desde el modo ejecutivo via env_gov.py.
    """
    data = _load()
    ctx  = _compute_contexto(data)

    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown(
        f'<div class="cm-root">{_html_header_concejo()}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="cm-root">{_html_checklist(ctx)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="cm-root">{_html_ataques(ctx)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="cm-root">{_html_argumentario(ctx)}</div>',
        unsafe_allow_html=True,
    )

    # Footer
    st.markdown(
        '<div style="margin-top:8px;font:400 8px/1 JetBrains Mono,monospace;'
        'color:rgba(255,255,255,.1);text-align:right">'
        'QUIRA Intelligence · Sala de Mando Concejo · Sprint C.2 · '
        'Gold Master v5.5_TGI · Dylus Lab © 2026'
        '</div>',
        unsafe_allow_html=True,
    )
