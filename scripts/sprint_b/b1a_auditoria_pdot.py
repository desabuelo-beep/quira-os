# -*- coding: utf-8 -*-
"""
B.1A — Auditoría temática del corpus PDOT (Sprint B · QUIRA OS)

Responde, por tema: ¿la información territorial existe en el PDOT narrativo
(corpus Supabase) o realmente falta? Distingue gap de DATOS vs gap de EXTRACCIÓN.

Temas: Género · Ambiente · Movilidad · Juventud · Cooperación
Fuentes: normativa_corpus → PDOT-MONTECRISTI · PLAN-BICENTENARIO-MCR · PAI-PLURIANUAL-GAD

Uso:  python scripts/sprint_b/b1a_auditoria_pdot.py
"""
from __future__ import annotations

import sys
import tomllib

import psycopg2

sys.stdout.reconfigure(encoding="utf-8")

SIGLAS_PDOT = ("PDOT-MONTECRISTI", "PLAN-BICENTENARIO-MCR", "PAI-PLURIANUAL-GAD")

PARROQUIAS = [
    "Isabel Muentes", "La Pila", "Colorado", "Eloy Alfaro",
    "Leónidas Plaza", "Leonidas Proaño", "Aníbal San Andrés", "San Andrés",
]

TEMAS: dict[str, list[str]] = {
    "GENERO": [
        "violencia intrafamiliar", "violencia de género", "embarazo adolescente",
        "jefatura femenina", "jefas de hogar", "femicidio", "equidad de género",
        "mujeres rurales", "brecha de género",
    ],
    "AMBIENTE": [
        "deforestación", "áreas protegidas", "contaminación", "cuenca",
        "recurso hídrico", "erosión", "cambio climático", "bosque seco",
        "remediación", "pasivo ambiental",
    ],
    "MOVILIDAD": [
        "transporte público", "tránsito", "vialidad", "movilidad",
        "vías rurales", "conectividad vial", "transporte intracantonal",
    ],
    "JUVENTUD": [
        "jóvenes", "juventud", "empleo juvenil", "desempleo juvenil",
        "primer empleo", "adolescentes",
    ],
    "COOPERACION": [
        "cooperación internacional", "organismos internacionales",
        "convenio internacional", "ONG", "PNUD", "cooperación técnica",
    ],
}


def _conn():
    with open(".streamlit/secrets.toml", "rb") as f:
        s = tomllib.load(f)
    return psycopg2.connect(s["database"]["supabase_uri"])


def auditar() -> None:
    conn = _conn()
    cur = conn.cursor()
    siglas = "', '".join(SIGLAS_PDOT)

    print("=" * 72)
    print("B.1A — AUDITORÍA TEMÁTICA PDOT · corpus narrativo Supabase")
    print("=" * 72)

    for tema, terminos in TEMAS.items():
        like_tema = " OR ".join(f"contenido ILIKE '%{t}%'" for t in terminos)
        like_parr = " OR ".join(f"contenido ILIKE '%{p}%'" for p in PARROQUIAS)

        # 1. total chunks del tema
        cur.execute(
            f"SELECT COUNT(*) FROM normativa_corpus "
            f"WHERE norma_sigla IN ('{siglas}') AND ({like_tema})"
        )
        total = cur.fetchone()[0]

        # 2. cruce tema × parroquia nombrada
        cur.execute(
            f"SELECT COUNT(*) FROM normativa_corpus "
            f"WHERE norma_sigla IN ('{siglas}') AND ({like_tema}) AND ({like_parr})"
        )
        cruce_parr = cur.fetchone()[0]

        # 3. cruce tema × mención genérica 'parroquia' o 'rural'
        cur.execute(
            f"SELECT COUNT(*) FROM normativa_corpus "
            f"WHERE norma_sigla IN ('{siglas}') AND ({like_tema}) "
            f"AND (contenido ILIKE '%parroquia%' OR contenido ILIKE '%rural%')"
        )
        cruce_terr = cur.fetchone()[0]

        print(f"\n### {tema}")
        print(f"  chunks con tema:                    {total}")
        print(f"  tema × parroquia NOMBRADA:          {cruce_parr}")
        print(f"  tema × territorio (parroquia/rural): {cruce_terr}")

        # 4. muestras del cruce más valioso
        if cruce_parr > 0:
            cur.execute(
                f"SELECT norma_sigla, chunk_seq, LEFT(contenido, 320) "
                f"FROM normativa_corpus "
                f"WHERE norma_sigla IN ('{siglas}') AND ({like_tema}) AND ({like_parr}) "
                f"ORDER BY palabras DESC LIMIT 3"
            )
            for sigla, seq, frag in cur.fetchall():
                frag1 = " ".join(frag.split())
                print(f"  ── [{sigla} #{seq}] {frag1[:300]}")

    conn.close()
    print("\n" + "=" * 72)
    print("Fin auditoría B.1A")


if __name__ == "__main__":
    auditar()
