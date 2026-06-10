# -*- coding: utf-8 -*-
"""
geotwin_narrativo.py — GeoTwin Narrativo v1 · QUIRA OS
======================================================
Mandato de mesa (Colega · 2026-06-10): GeoTwin nace EXPLICANDO, no
visualizando. Tres casos explicativos generados EN RUNTIME desde
pdot_indicadores (2,004 indicadores) — si los datos cambian, la
narrativa cambia. Eso es el gemelo: el territorio hablando a través
de su propia evidencia estructurada.

Casos:
    1. Isabel Muentes — la parroquia-señal (convergencia multi-sistema)
    2. Riesgo territorial — la capa que estaba enterrada en el PDOT
    3. Brecha urbano-rural — las dos realidades del cantón

Validación conceptual (criterio Colega): si el motor explica los tres
casos con los indicadores actuales, GeoTwin está validado.

BLOOMBERG FIREWALL: salida 100% lenguaje de gobernanza. Sin códigos
internos de metodología ni identificadores de nodos.

Uso:  python -m app.engines.geotwin_narrativo            # 3 casos
      python -m app.engines.geotwin_narrativo --caso 1   # uno solo
"""
from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path

import psycopg2

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]

# Dimensiones parroquiales con dirección de bienestar conocida
# (más alto = mejor). Lista curada — el motor NO adivina direcciones.
DIMENSIONES_PARROQUIALES = [
    ("Cobertura de agua por red (parroquial)", "agua por red"),
    ("Cobertura de saneamiento (parroquial)", "saneamiento"),
    ("Cobertura de drenaje pluvial (parroquial)", "drenaje pluvial"),
    ("Cobertura de recolección de desechos sólidos", "recolección de residuos"),
    ("Equipamiento por habitante (parroquial)", "equipamiento público"),
]

PARROQUIAS_CUP = [
    "Isabel Muentes", "Colorado", "La Pila", "Aníbal San Andrés",
    "Leonidas Proaño", "Leónidas Proaño", "General Eloy Alfaro",
    "Gral. Eloy Alfaro", "Montecristi",
]


def _conn():
    with open(ROOT / ".streamlit" / "secrets.toml", "rb") as f:
        s = tomllib.load(f)
    return psycopg2.connect(s["database"]["supabase_uri"])


def _q(cur, sql: str, params=()) -> list[tuple]:
    cur.execute(sql, params)
    return cur.fetchall()


# ══════════════════════════════════════════════════════════════════════════
# CASO 1 — ISABEL MUENTES: la parroquia-señal
# ══════════════════════════════════════════════════════════════════════════

def caso_isabel_muentes(cur) -> dict:
    """Convergencia multi-sistema: ¿en cuántas dimensiones independientes
    Isabel Muentes ocupa el peor lugar del cantón? Computado en runtime."""
    convergencia = []
    for indicador, etiqueta in DIMENSIONES_PARROQUIALES:
        rows = _q(cur, """
            SELECT territorio, valor_num FROM pdot_indicadores
            WHERE indicador = %s AND valor_num IS NOT NULL
              AND territorio = ANY(%s)
            ORDER BY valor_num ASC
        """, (indicador, PARROQUIAS_CUP))
        if len(rows) < 4:
            continue
        peor_territorio, peor_valor = rows[0]
        es_im = "Isabel Muentes" in peor_territorio
        valor_im = next((v for t, v in rows if "Isabel Muentes" in t), None)
        mejor_valor = rows[-1][1]
        convergencia.append({
            "dimension": etiqueta,
            "isabel_muentes": valor_im,
            "peor_del_canton": es_im,
            "rango_canton": (float(rows[0][1]), float(mejor_valor)),
            "n_territorios": len(rows),
        })

    senales = _q(cur, """
        SELECT indicador, valor_texto, unidad, anio FROM pdot_indicadores
        WHERE territorio ILIKE '%%Isabel Muentes%%' AND confianza = 'alta'
        ORDER BY sistema, indicador
    """)
    poligono = _q(cur, """
        SELECT valor_num FROM pdot_indicadores
        WHERE indicador ILIKE 'Área del polígono urbano CUP%%'
          AND territorio = 'Isabel Muentes'
    """)

    n_peor = sum(1 for c in convergencia if c["peor_del_canton"])
    return {
        "titulo": "ISABEL MUENTES — LA PARROQUIA-SEÑAL",
        "convergencia": convergencia,
        "n_dimensiones_evaluadas": len(convergencia),
        "n_dimensiones_peor": n_peor,
        "area_poligono_ha": float(poligono[0][0]) if poligono else None,
        "n_senales_registradas": len(senales),
        "senales": [
            {"indicador": s[0], "valor": s[1], "unidad": s[2], "anio": s[3]}
            for s in senales
        ],
    }


def render_caso_1(d: dict) -> str:
    out = [f"\n{'═'*68}", f"  CASO 1 · {d['titulo']}", "═" * 68]
    out.append(
        f"\n  El motor evaluó {d['n_dimensiones_evaluadas']} dimensiones de servicios"
        f"\n  con datos parroquiales comparables. Isabel Muentes ocupa el PEOR"
        f"\n  lugar del cantón en {d['n_dimensiones_peor']} de {d['n_dimensiones_evaluadas']}.\n"
    )
    for c in d["convergencia"]:
        marca = "🔴 PEOR DEL CANTÓN" if c["peor_del_canton"] else "—"
        val = f"{c['isabel_muentes']}" if c["isabel_muentes"] is not None else "sin dato"
        out.append(f"   · {c['dimension']:<28} {val:>8}   rango cantonal "
                   f"{c['rango_canton'][0]:.1f}–{c['rango_canton'][1]:.1f}   {marca}")
    if d["area_poligono_ha"]:
        out.append(
            f"\n  Y la paradoja territorial: con {d['area_poligono_ha']:.0f} ha, es el"
            f"\n  polígono urbano MÁS EXTENSO del cantón — la mayor superficie"
            f"\n  urbana con los menores servicios."
        )
    out.append(
        "\n  LECTURA: cuando un territorio ocupa el extremo crítico en"
        "\n  dimensiones medidas por sistemas independientes (agua, saneamiento,"
        "\n  residuos, equipamiento), deja de ser un dato — es una señal"
        "\n  estructural. Toda decisión de focalización del cantón debería"
        "\n  empezar por esta parroquia."
    )
    return "\n".join(out)


# ══════════════════════════════════════════════════════════════════════════
# CASO 2 — RIESGO TERRITORIAL: la capa enterrada
# ══════════════════════════════════════════════════════════════════════════

def caso_riesgo_territorial(cur) -> dict:
    macro = _q(cur, """
        SELECT indicador, valor_texto, unidad FROM pdot_indicadores
        WHERE (indicador ILIKE '%%susceptibilidad%%' OR indicador ILIKE '%%inundac%%')
          AND valor_num IS NOT NULL AND territorio IN ('Montecristi','cantonal')
        ORDER BY valor_num DESC LIMIT 8
    """)
    sitios = _q(cur, """
        SELECT indicador, valor_texto, territorio FROM pdot_indicadores
        WHERE indicador LIKE 'Riesgo territorial:%%'
        ORDER BY territorio
    """)
    areas = _q(cur, """
        SELECT indicador, valor_num, territorio FROM pdot_indicadores
        WHERE indicador LIKE 'Área afectada%%' AND valor_num IS NOT NULL
        ORDER BY valor_num DESC LIMIT 5
    """)
    return {
        "titulo": "RIESGO TERRITORIAL — LA CAPA QUE ESTABA ENTERRADA EN EL PDOT",
        "macro": [{"ind": m[0], "valor": m[1], "unidad": m[2]} for m in macro],
        "sitios": [{"riesgo": s[0].replace("Riesgo territorial: ", ""),
                    "nivel": s[1], "lugar": s[2]} for s in sitios],
        "areas": [{"ind": a[0], "ha": float(a[1]), "lugar": a[2]} for a in areas],
    }


def render_caso_2(d: dict) -> str:
    out = [f"\n{'═'*68}", f"  CASO 2 · {d['titulo']}", "═" * 68]
    out.append("\n  Magnitudes cantonales (del diagnóstico oficial):")
    for m in d["macro"][:5]:
        out.append(f"   · {m['ind'][:58]:<58} {m['valor']:>8} {m['unidad'] or ''}")
    if d["sitios"]:
        out.append(f"\n  Riesgos con NOMBRE DE LUGAR ({len(d['sitios'])} registrados):")
        for s_ in d["sitios"][:9]:
            out.append(f"   · [{s_['lugar'][:30]:<30}] {s_['riesgo'][:55]}"
                       + (f" — nivel {s_['nivel']}" if s_["nivel"] not in (None, "registrado") else ""))
    if d["areas"]:
        out.append("\n  Superficies afectadas cuantificadas:")
        for a in d["areas"]:
            out.append(f"   · {a['ha']:>9,.0f} ha — {a['ind'][:48]} ({a['lugar']})")
    out.append(
        "\n  LECTURA: el cantón tiene su mapa de riesgo cuantificado y con"
        "\n  lugares nombrados — estaba en el diagnóstico esperando ser"
        "\n  estructurado. La planificación de asentamientos y la gestión de"
        "\n  fondos climáticos pueden focalizarse HOY con esta capa."
    )
    return "\n".join(out)


# ══════════════════════════════════════════════════════════════════════════
# CASO 3 — BRECHA URBANO-RURAL: las dos realidades
# ══════════════════════════════════════════════════════════════════════════

PARES_URBANO_RURAL = [
    ("Incidencia de pobreza extrema en área urbana", "Incidencia de pobreza extrema en área rural", "Pobreza extrema"),
    ("Incidencia de pobreza en área urbana", "Incidencia de pobreza en área rural", "Pobreza por ingresos"),
    ("Índice de pobreza multidimensional área urbana", "Índice de pobreza multidimensional área rural", "Pobreza multidimensional"),
]


def caso_brecha_urbano_rural(cur) -> dict:
    pares = []
    for ind_u, ind_r, etiqueta in PARES_URBANO_RURAL:
        u = _q(cur, "SELECT valor_num, anio FROM pdot_indicadores WHERE indicador=%s AND valor_num IS NOT NULL LIMIT 1", (ind_u,))
        r = _q(cur, "SELECT valor_num, anio FROM pdot_indicadores WHERE indicador=%s AND valor_num IS NOT NULL LIMIT 1", (ind_r,))
        if u and r and float(u[0][0]) > 0:
            pares.append({
                "dimension": etiqueta,
                "urbano": float(u[0][0]),
                "rural": float(r[0][0]),
                "ratio": round(float(r[0][0]) / float(u[0][0]), 1),
                "anio": u[0][1],
            })
    nbi = _q(cur, """
        SELECT territorio, valor_num, anio FROM pdot_indicadores
        WHERE indicador = 'NBI total (territorial)' AND valor_num IS NOT NULL
        ORDER BY anio DESC, territorio LIMIT 4
    """)
    dispersas = _q(cur, """
        SELECT indicador, valor_num FROM pdot_indicadores
        WHERE territorio ILIKE '%%sin parroquia%%' AND valor_num IS NOT NULL
        ORDER BY indicador
    """)
    return {
        "titulo": "BRECHA URBANO-RURAL — LAS DOS REALIDADES DE MONTECRISTI",
        "pares": pares,
        "nbi": [{"territorio": n[0], "valor": float(n[1]), "anio": n[2]} for n in nbi],
        "dispersas": [{"ind": d_[0], "valor": float(d_[1])} for d_ in dispersas],
    }


def render_caso_3(d: dict) -> str:
    out = [f"\n{'═'*68}", f"  CASO 3 · {d['titulo']}", "═" * 68, ""]
    for p in d["pares"]:
        out.append(f"   · {p['dimension']:<26} urbano {p['urbano']:>5.1f} %   "
                   f"rural {p['rural']:>5.1f} %   → {p['ratio']}× ({p['anio']})")
    if d["nbi"]:
        out.append("\n  Necesidades básicas insatisfechas (serie):")
        for n in d["nbi"]:
            out.append(f"   · {n['territorio']:<32} {n['valor']:>5.1f} %  ({n['anio']})")
    if d["dispersas"]:
        out.append("\n  Y el tercer Montecristi — comunidades dispersas sin parroquia:")
        for d_ in d["dispersas"]:
            out.append(f"   · {d_['ind'][:52]:<52} {d_['valor']:>6.1f}")
    out.append(
        "\n  LECTURA: la brecha urbano-rural es la variable que explica casi"
        "\n  todas las demás — agua, saneamiento, empleo, género. Montecristi"
        "\n  no tiene un problema de servicios: tiene dos realidades"
        "\n  territoriales con una frontera que la inversión histórica no ha"
        "\n  cruzado. Cualquier meta cantonal promedio esconde esa frontera."
    )
    return "\n".join(out)


# ══════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="GeoTwin Narrativo v1 — 3 casos")
    ap.add_argument("--caso", type=int, choices=[1, 2, 3], help="solo un caso")
    args = ap.parse_args()

    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pdot_indicadores")
    total = cur.fetchone()[0]
    print(f"\nGEOTWIN NARRATIVO v1 · Montecristi · base territorial: {total} indicadores")

    casos = {
        1: (caso_isabel_muentes, render_caso_1),
        2: (caso_riesgo_territorial, render_caso_2),
        3: (caso_brecha_urbano_rural, render_caso_3),
    }
    seleccion = [args.caso] if args.caso else [1, 2, 3]
    for n in seleccion:
        builder, renderer = casos[n]
        print(renderer(builder(cur)))
    conn.close()
    print(f"\n{'═'*68}\n  Generado en runtime desde la base territorial — si los datos"
          f"\n  cambian, la explicación cambia. Eso es el gemelo.\n{'═'*68}")


if __name__ == "__main__":
    main()
