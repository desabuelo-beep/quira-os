"""
QUIRA Intelligence — Módulo de Narrativa Institucional
Sprint D.3 · Modularización Narrativa

Doctrina: "QUIRA no improvisa el lenguaje.
           QUIRA tiene un sistema narrativo con 4 voces distintas."

━━━ ARQUITECTURA NARRATIVA ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  VEZ_BRIEFING   — 2 oraciones, briefing strip, 0-3s lectura ejecutiva
  VOZ_IA         — análisis preventivo completo, 3-5 párrafos, Z6
  VOZ_CONCEJO    — respuesta política, datos primero, lenguaje confrontacional
  VOZ_ARGUMENTO  — ofensiva institucional, puntos de ataque propios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reglas del sistema narrativo:
  1. QUIRA no es chatbot. Tono ejecutivo institucional. Sin ambigüedad.
  2. Los datos preceden a la argumentación. Siempre.
  3. El briefing no puede tener más de 280 caracteres (2 oraciones).
  4. La voz Concejo es política, no técnica — usa datos como armas.
  5. Cada voz tiene su contexto. No mezclar.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
from config import CORTE


# ══════════════════════════════════════════════════════════════════════════════
# VOZ 1 — BRIEFING EJECUTIVO (Z header, capa 0-3s)
# ══════════════════════════════════════════════════════════════════════════════

def briefing_strip(narrative: str, max_chars: int = 280) -> str:
    """
    Extrae las 2 primeras oraciones del análisis completo.
    Máximo 280 caracteres — lectura de 8-15s, sala de mando.
    Sin chatbot. Sin relleno. Situación + palanca.

    Args:
        narrative: texto completo de _compose_quira_ia
        max_chars: límite de caracteres (default 280)

    Returns:
        str con máximo 2 oraciones y max_chars caracteres
    """
    partes = re.split(r'(?<=\.)\s+', narrative.strip())
    texto  = " ".join(partes[:2])
    return texto if len(texto) <= max_chars else texto[:max_chars - 3] + "…"


# ══════════════════════════════════════════════════════════════════════════════
# VOZ 2 — ANÁLISIS IA PREVENTIVO (Z6, capa 15-30s)
# ══════════════════════════════════════════════════════════════════════════════

def narrativa_ejecutiva(eco: list[dict], data: dict) -> str:
    """
    Brief ejecutivo institucional completo para Z6 (QUIRA IA).
    Lenguaje autoritario, preciso. No es chatbot. No es resumen.
    Es análisis preventivo institucional.

    Estructura:
      1. Estado del GAD (ruptura o trayectoria)
      2. Contraste ecosistema (sobre-ritmo vs atención)
      3. Palanca crítica (BDE u otra acción inmediata)

    Args:
        eco: lista de 4 dicts del ecosistema [GAD, Patronato, EP Aseo, Bomberos]
        data: snapshot dict completo

    Returns:
        str — 3-5 oraciones, español institucional
    """
    from utils.top import narrativa_ia

    gad_e   = eco[0]
    otros   = eco[1:]
    fin     = data.get("financiero", {})
    fondos  = fin.get("fondos_bloqueados_est", 3_660_000)
    fondos_m = fondos / 1_000_000

    gad_brief = narrativa_ia(gad_e)

    sobre_ritmo = [e["nombre"] for e in otros if e.get("categoria") == "sostenible"]
    atencion    = [e["nombre"] for e in otros if e.get("categoria") != "sostenible"]

    partes = [gad_brief]

    if sobre_ritmo:
        lista = (
            ", ".join(sobre_ritmo[:-1]) + " y " + sobre_ritmo[-1]
            if len(sobre_ritmo) > 1 else sobre_ritmo[0]
        )
        partes.append(
            f"En contraste, {lista} mantienen trayectoria sobre el ritmo histórico "
            f"esperado para {CORTE}. El ecosistema municipal opera de forma saludable "
            "fuera del núcleo de inversión del GAD."
        )

    if atencion:
        partes.append(
            f"Entidades con atención requerida: {', '.join(atencion)}. "
            "Monitorear Q siguiente."
        )

    partes.append(
        f"La palanca de mayor impacto disponible ahora mismo es el desembolso BDE "
        f"(${fondos_m:.1f}M en fondos bloqueados). Su activación antes de mediados de "
        "junio determina si Q2 cierra dentro o fuera del umbral COPFP Art. 113."
    )

    return " ".join(partes)


# ══════════════════════════════════════════════════════════════════════════════
# VOZ 3 — RESPUESTA CONCEJO (Sala de Mando, modo político)
# ══════════════════════════════════════════════════════════════════════════════

def respuesta_concejo(vector: str, ctx: dict) -> dict[str, str]:
    """
    Genera la respuesta institucional a un vector de ataque del Concejo.
    Lenguaje político: datos primero, reencuadre después, ley al final.

    Args:
        vector: código del ataque ("A1" | "A2" | "A3" | "A4" | "A5" | "A6")
        ctx: dict con métricas computadas (_compute_contexto en p_concejo.py)

    Returns:
        dict con keys: ataque, datos, respuesta, reencuadre, ley, nivel
    """
    ti  = ctx.get("ti_raw", 1.05)
    top = ctx.get("top_gad", 8.1)
    tgi = ctx.get("tgi_score", 68.82)
    d3  = ctx.get("d3", 14.58)
    d5  = ctx.get("d5", 100.0)
    irs = ctx.get("irs", 79.7)
    nbi = ctx.get("nbi_rural", 55.7)
    fon = ctx.get("fondos_m", 3.66)
    fon_det = ctx.get("fondos_det", "BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K")

    _VECTORES: dict[str, dict] = {
        "A1": {
            "nivel":      "CRÍTICO",
            "ataque":     f'"Con {ti:.2f}% de inversión en Q1, este gobierno '
                          f'está paralizado. ¿En qué se gastó el presupuesto?"',
            "datos":      f"TOP: {top:.1f}% vs W_Q esperado de 13% en Q1. "
                          f"D3 (ejecución) = {d3:.1f}/100 — presupuesto codificado, no bloqueado. "
                          f"TGI global: {tgi:.1f}/100.",
            "respuesta":  f"La inversión en Q1 es del {ti:.2f}% sobre presupuesto de inversión "
                          f"(G71-78). El ritmo histórico Q1 en Ecuador es entre 5-15%. "
                          f"No estamos paralizados — estamos en fase de planificación y licitación.",
            "reencuadre": f"Los fondos bloqueados ({fon_det}) representan ${fon:.2f}M listos para "
                          f"activar. El cuello de botella es contractual, no político.",
            "ley":        "COPFP Art. 113 · W_Q calibrado eSIGEF Q1=0.13",
        },
        "A2": {
            "nivel":      "ALTO",
            "ataque":     f'"Las parroquias rurales tienen NBI promedio de {nbi:.1f}%. '
                          f'Este gobierno abandonó el campo."',
            "datos":      f"IRS: {irs:.0f}/100 (Muy Regresivo) — dato estructural heredado. "
                          f"IET parroquias críticas: Colorado 28.6%, Isabel Muentes 35.7%, "
                          f"Leónidas Proaño 42.9%.",
            "respuesta":  f"El IRS de {irs:.0f} es estructural — refleja décadas de inversión "
                          f"concentrada en el área urbana. Este gobierno lo está midiendo y "
                          f"visibilizando por primera vez con metodología QUIRA.",
            "reencuadre": "Medir el problema no es el problema. El problema es no medirlo "
                          "y pretender que no existe. El D4 actual de 66.85 es bajo, "
                          "y lo sabemos porque tenemos el sistema para saberlo.",
            "ley":        "COOTAD Art. 192 · PDOT Parroquial 2021-2025",
        },
        "A3": {
            "nivel":      "ALTO",
            "ataque":     f'"El Patronato ejecuta {ctx.get("top_pat", 150.5):.0f}% '
                          f'de TOP mientras el GAD apenas {top:.1f}%. '
                          f'¿Por qué el GAD no puede hacer lo mismo?"',
            "datos":      f"Patronato: Ti {ctx.get('ti_pat', 19.56):.2f}% (todos grupos H90). "
                          f"GAD: Ti {ti:.2f}% (solo G71-78 inversión estricta D3). "
                          f"Diferentes universos presupuestales — no son comparables directamente.",
            "respuesta":  "La comparación mezcla metodologías. El GAD mide solo inversión de "
                          "infraestructura (grupos 71-78). El Patronato incluye gasto corriente "
                          "de programas sociales. Es como comparar litros de agua con kilómetros.",
            "reencuadre": "Que el Patronato esté en sobre-ritmo valida que el ecosistema "
                          "municipal funciona. Las 4 entidades del Holding son un sistema "
                          "complementario, no competidores.",
            "ley":        "NOMENCLATURA_CANONICA QUIRA §7.2 · H90_PRESUPUESTO_CONSOLIDADO",
        },
        "A4": {
            "nivel":      "MEDIO",
            "ataque":     f'"El TGI no llegó al 70. Prometieron gobernanza, '
                          f'y estamos en {tgi:.1f}."',
            "datos":      f"TGI {tgi:.1f}/100 — Transición con Riesgos. "
                          f"D1 Legalidad: {ctx.get('d1', 83.5):.1f}/100 ✅. "
                          f"D5 Capacidad: {d5:.1f}/100 ✅. "
                          f"D3 Ejecución: {d3:.1f}/100 — el único en ruptura.",
                "respuesta": f"TGI {tgi:.1f} significa que 4 de 5 dimensiones están en "
                          f"trayectoria positiva. El único foco de atención es D3 "
                          f"(ejecución de inversión), que tiene causa clara y solución "
                          f"identificada: activar desembolso BDE.",
            "reencuadre": "La tendencia TGI es ascendente desde 2023. El piso institucional "
                          "es sólido — D1 y D5 al máximo. No estamos cayendo. "
                          "Estamos subiendo con un cuello de botella financiero temporal.",
            "ley":        "TGI Framework QUIRA · 5 dimensiones COOTAD",
        },
        "A5": {
            "nivel":      "CRÍTICO",
            "ataque":     f'"Hay ${fon:.2f}M parados. ¿Por qué no activan esos fondos?"',
            "datos":      f"Fondos bloqueados: {fon_det}. "
                          f"BDE: proceso de desembolso activo — requiere firma del Alcalde + "
                          f"Director Financiero + validación BDE.",
            "respuesta":  f"Los ${fon:.2f}M no están perdidos. Están en proceso de desembolso "
                          f"con documentación completa. El BDE tiene tiempos de proceso "
                          f"de 45-60 días. La activación está en agenda prioritaria.",
            "reencuadre": "Que tengamos identificados los fondos bloqueados con nombre, "
                          "monto y estado es evidencia de gestión activa. "
                          "Municipios sin QUIRA no saben que tienen estos fondos parados.",
            "ley":        "COPFP Art. 113 · BDE Convenio vigente",
        },
        "A6": {
            "nivel":      "CRÍTICO",
            "ataque":     '"COPFP Art. 113 exige 60% de ejecución al cierre de año. '
                          '¿Cómo van a llegar del 1% al 60%?"',
            "datos":      f"Inversión requerida residual: ~58.95% del codificado en Q2-Q4. "
                          f"Fondos activables: ${fon:.2f}M = palanca inmediata. "
                          f"Plazo: cierre Q2 en ~45 días — primer checkpoint crítico.",
            "respuesta":  "El plan de cierre tiene 3 palancas: (1) activación BDE $3.5M "
                          "en junio, (2) concurso de precios obras menores Q2, "
                          "(3) reprogramación POA con Director de Obras. "
                          "Los números son alcanzables con ejecución disciplinada.",
            "reencuadre": "El Art. 113 no prohíbe empezar despacio — prohíbe terminar "
                          "despacio. Q1 es de planificación; Q3-Q4 son de ejecución. "
                          "Estamos exactamente donde debe estar un gobierno que planifica.",
            "ley":        "COPFP Art. 113 · PAC publicado · COOTAD Art. 227",
        },
    }

    return _VECTORES.get(vector, {})


# ══════════════════════════════════════════════════════════════════════════════
# VOZ 4 — ARGUMENTARIO OFENSIVO (Concejo — puntos de ataque propios)
# ══════════════════════════════════════════════════════════════════════════════

def argumentario_ofensivo(ctx: dict) -> list[dict[str, str]]:
    """
    Genera los puntos de ofensiva institucional para el Concejo.
    El ejecutivo no solo defiende — ataca desde sus fortalezas.

    Args:
        ctx: dict con métricas computadas

    Returns:
        list de dicts con keys: titulo, dato, argumento, color
    """
    top_pat = ctx.get("top_pat", 150.5)
    top_ep  = ctx.get("top_ep", 139.8)
    top_bom = ctx.get("top_bom", 149.5)
    d1      = ctx.get("d1", 83.5)
    d5      = ctx.get("d5", 100.0)
    fon_m   = ctx.get("fondos_m", 3.66)

    return [
        {
            "titulo":    "Ecosistema municipal en sobre-ritmo",
            "dato":      f"Patronato {top_pat:.0f}% · EP Aseo {top_ep:.0f}% · Bomberos {top_bom:.0f}%",
            "argumento": "3 de 4 entidades del Holding Municipal están por encima del ritmo "
                         "histórico esperado. El ejecutivo no gerencia solo el GAD — "
                         "gerencia un ecosistema institucional.",
            "color":     "#22C55E",
        },
        {
            "titulo":    "Marco legal impecable",
            "dato":      f"D1 Legalidad: {d1:.0f}/100 · D5 Capacidad: {d5:.0f}/100",
            "argumento": "PAC publicado, SIGAD certificado, SNP al 100%. "
                         "El marco normativo está completamente alineado. "
                         "El Concejo no puede cuestionar la legalidad de este gobierno.",
            "color":     "#00D4FF",
        },
        {
            "titulo":    "Fondos activables identificados",
            "dato":      f"${fon_m:.2f}M listos para ejecutar — no perdidos",
            "argumento": "Municipios sin sistema de inteligencia institucional no saben "
                         "que tienen fondos bloqueados. QUIRA los identificó, los cuantificó "
                         "y tiene un plan de activación. Eso es gestión, no parálisis.",
            "color":     "#C084FC",
        },
        {
            "titulo":    "Sistema de medición propio",
            "dato":      "TGI · TOP · SAT · IRS · IET — metodología QUIRA única en la región",
            "argumento": "Este gobierno es el único en Ecuador que puede medir su propia "
                         "gobernanza en tiempo real. El Concejo critica con opiniones; "
                         "el ejecutivo responde con datos.",
            "color":     "#F59E0B",
        },
    ]


# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES NARRATIVAS
# ══════════════════════════════════════════════════════════════════════════════

def clasificar_nivel(nivel: str) -> dict[str, str]:
    """
    Retorna colores y label para un nivel de ataque del Concejo.

    Args:
        nivel: "CRÍTICO" | "ALTO" | "MEDIO" | "BAJO"

    Returns:
        dict con keys: color, bg, label
    """
    _MAP = {
        "CRÍTICO": {"color": "#EF4444", "bg": "rgba(239,68,68,.08)",  "label": "🔴 CRÍTICO"},
        "ALTO":    {"color": "#F97316", "bg": "rgba(249,115,22,.07)", "label": "🟠 ALTO"},
        "MEDIO":   {"color": "#F59E0B", "bg": "rgba(245,158,11,.06)", "label": "🟡 MEDIO"},
        "BAJO":    {"color": "#22C55E", "bg": "rgba(34,197,94,.05)",  "label": "🟢 BAJO"},
    }
    return _MAP.get(nivel, _MAP["MEDIO"])
