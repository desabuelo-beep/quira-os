# -*- coding: utf-8 -*-
"""
scripts/brn_catalogo.py — BRN · Biblioteca de Reglas Normativas (ADR-035)
═══════════════════════════════════════════════════════════════════════════════════
Cataloga las reglas que YA OPERAN en el sistema, dándoles lo que hoy les falta: un
IDENTIFICADOR propio, un TIPO y su HUELLA del corpus verificado.

QUÉ ES (y qué NO es) — ADR-035, ratificado:
  · La BRN es una BIBLIOTECA, no un motor. NO calcula, NO evalúa, NO dispara alertas.
  · El GOLD MASTER es el único motor: calcula los SAT. La BRN prueba de qué ley nacieron.
  · Cadena: Ley → BRN → Gold Master (único motor) → QUIRA (explica y traza).

EL HUECO QUE LLENA (diagnóstico 2026-07-16):
  · d02 tiene la REGLA operacional ("la inversión no debe caer bajo el 65%") pero SIN sha:
    la redactó el director en el enricher.
  · d01/d03 tienen el SHA verificado del corpus pero SIN la regla: solo la cita del artículo.
  Nadie tenía las dos mitades juntas. La BRN las une y las hace trazables.

REGLA CONSTITUCIONAL (ADR-035 §5): la IA JAMÁS deriva reglas por su cuenta.
  Ley → Extracción → PROPUESTA → VALIDACIÓN HUMANA → BRN → Gold Master → SAT
  Toda regla nace con estado `propuesta`. Solo Javo la promueve a `vigente`.

CLASIFICACIÓN (ADR-035 §4 · anti-alucinación): no todo artículo produce control.
  SATizable:  obligación · prohibición · límite · plazo
  NO:         principio · definición · competencia (indirecta)

Uso:  python scripts/brn_catalogo.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
import sys
import tomllib
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
SECRETS = REPO / ".streamlit" / "secrets.toml"

# Tipos de regla (ADR-035 §4) — el tipo decide si la norma puede producir un control
TIPOS = {
    "limite":     ("Límite", True, "fija un piso o techo cuantitativo"),
    "obligacion": ("Obligación", True, "manda hacer algo verificable"),
    "prohibicion": ("Prohibición", True, "veda una conducta"),
    "plazo":      ("Plazo", True, "fija una fecha o periodicidad"),
    "competencia": ("Competencia", False, "asigna atribuciones — control indirecto"),
    "principio":  ("Principio", False, "declara un valor — NO SATizable"),
}

# ── EL CATÁLOGO · reglas que YA operan, con su origen exacto ──────────────────
# `sat` = la señal que el Gold Master YA calcula sobre esta regla (si la hay).
# Nada se inventa: la condición sale del enricher que ya opera; el sha, del corpus.
REGLAS = [
    # ── financieras · las 3 que d02 ya publica con su norma ───────────────────
    {"norma": "COPLAFIP", "art": "115", "tipo": "limite", "dom": "d02",
     "nombre": "Reforma presupuestaria significativa",
     "condicion": "las reformas no deben superar el 5% del presupuesto anual",
     "sat": "Reforma presupuestaria tardía", "kw": "%reforma%"},
    {"norma": "COPLAFIP", "art": "113", "tipo": "limite", "dom": "d02",
     "nombre": "Ejecución mínima de la meta",
     "condicion": "ninguna meta debe ejecutar menos del 10% de lo asignado",
     "sat": "Parálisis presupuestaria", "kw": "%devengad%"},
    {"norma": "COOTAD", "art": "192", "tipo": "limite", "dom": "d02",
     "nombre": "Inversión mínima frente al gasto corriente",
     "condicion": "la inversión no debe caer bajo el 65% del presupuesto",
     "sat": "Alerta fiscal · estructura COOTAD", "kw": "%inversión%"},
    # ── mandato electoral · la cadena que d03 verifica ────────────────────────
    {"norma": "COD", "art": "97", "tipo": "obligacion", "dom": "d03",
     "nombre": "Plan de Trabajo ante el CNE",
     "condicion": "todo candidato debe inscribir su Plan de Trabajo al presentar la candidatura",
     "sat": "", "kw": "%plan de trabajo%"},
    {"norma": "COPLAFIP", "art": "34", "tipo": "obligacion", "dom": "d03",
     "nombre": "Traducción del mandato al plan",
     "condicion": "el plan local debe recoger las propuestas que justificaron la elección",
     "sat": "", "kw": "%plan de desarrollo%"},
    {"norma": "COPLAFIP", "art": "41", "tipo": "obligacion", "dom": "d03",
     "nombre": "Formulación del plan de desarrollo",
     "condicion": "el GAD debe formular o actualizar su plan al inicio de la gestión",
     "sat": "", "kw": "%formular%"},
    {"norma": "LOPC", "art": "89", "tipo": "plazo", "dom": "d09",
     "nombre": "Rendición de cuentas anual",
     "condicion": "la rendición se realiza cada año frente al Plan de Trabajo del CNE",
     "sat": "", "kw": "%rendición de cuentas%"},
    {"norma": "CE", "art": "105", "tipo": "obligacion", "dom": "d03",
     "nombre": "Revocatoria por incumplir el Plan de Trabajo",
     "condicion": "el electorado puede revocar el mandato por incumplir el Plan de Trabajo",
     "sat": "", "kw": "%revocar%"},
    # ── planificación · los eslabones que d01 ya cita ─────────────────────────
    {"norma": "CE", "art": "241", "tipo": "obligacion", "dom": "d01",
     "nombre": "Planificación obligatoria del territorio",
     "condicion": "la planificación del ordenamiento territorial es obligatoria",
     "sat": "", "kw": "%planificación%"},
    {"norma": "COOTAD", "art": "233", "tipo": "plazo", "dom": "d01",
     "nombre": "Plazo del plan operativo anual",
     "condicion": "el POA debe formularse en el plazo que fija la norma",
     "sat": "", "kw": "%operativo anual%"},
    {"norma": "COOTAD", "art": "215", "tipo": "obligacion", "dom": "d02",
     "nombre": "Presupuesto del GAD",
     "condicion": "el presupuesto se sujeta al plan de desarrollo del GAD",
     "sat": "", "kw": "%presupuesto%"},
    {"norma": "LOSNCP", "art": "22", "tipo": "obligacion", "dom": "d01",
     "nombre": "Plan Anual de Contratación",
     "condicion": "toda entidad debe publicar su PAC conforme al plan y al presupuesto",
     "sat": "", "kw": "%plan anual%"},
    {"norma": "COOTAD", "art": "238", "tipo": "obligacion", "dom": "d08",
     "nombre": "Participación en la formulación del presupuesto",
     "condicion": "el presupuesto se formula con participación ciudadana",
     "sat": "", "kw": "%participación%"},
]

_DISP = {"CE": "Constitución", "COD": "Código de la Democracia", "COOTAD": "COOTAD",
         "COPLAFIP": "COPLAFIP", "LOPC": "L.O. Participación Ciudadana",
         "LOSNCP": "L.O. Contratación Pública"}


def _uri() -> str:
    try:
        return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        return ""


def main() -> int:
    uri = _uri()
    if not uri:
        print("[skip] sin supabase_uri — la BRN no puede verificar sus reglas")
        return 0
    import psycopg2
    cur = psycopg2.connect(uri, connect_timeout=25).cursor()

    catalogo, sin_verificar = [], []
    for r in REGLAS:
        # el artículo DEBE existir en el corpus, o la regla no entra (Regla 3)
        cur.execute("SELECT sha256, contenido FROM public.normativa_corpus "
                    "WHERE norma_sigla=%s AND articulo_num=%s LIMIT 1", (r["norma"], r["art"]))
        row = cur.fetchone()
        if not row:
            sin_verificar.append(f'{r["norma"]} Art. {r["art"]}')
            continue
        sha, cont = (row[0] or "")[:16], re.sub(r"\s+", " ", row[1] or "").strip()
        m = re.match(r"Art\.\s*[\d.]+\.-\s*([^.\-]{3,70})", cont)
        tipo_lbl, satizable, _ = TIPOS[r["tipo"]]
        catalogo.append({
            "id": f'{r["norma"]}-{r["art"]}-R01',      # ID propio (ADR-035 §3)
            "norma": r["norma"], "norma_nombre": _DISP.get(r["norma"], r["norma"]),
            "articulo": r["art"], "sumilla": (m.group(1).strip() if m else ""),
            "nombre": r["nombre"], "condicion": r["condicion"],
            "tipo": tipo_lbl, "satizable": satizable,
            "señal": r["sat"], "opera_en": r["dom"],
            "sha256": sha, "verbatim": cont[:300],
            "estado": "propuesta",     # ADR-035 §5 — solo Javo la promueve a "vigente"
        })

    con_sat = sum(1 for r in catalogo if r["señal"])
    bloque = {
        "_fuente": "Corpus normativo verificado (Supabase · pgvector · sha256)",
        "_doctrina": "La BRN organiza; el Gold Master calcula; QUIRA explica. La IA propone, "
                     "el humano valida (ADR-035).",
        "fecha": date.today().isoformat(),
        "total": len(catalogo), "con_señal_activa": con_sat,
        "estado_catalogo": "propuesta · pendiente de validación humana",
        "reglas": catalogo,
    }
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    snap["brn"] = bloque
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK — BRN catalogada: {len(catalogo)} reglas verificadas contra el corpus")
    print(f"   con señal que el motor ya calcula : {con_sat}")
    print(f"   sin señal (norma trazada, aún sin control): {len(catalogo) - con_sat}")
    if sin_verificar:
        print(f"   NO ENTRAN (sin respaldo en el corpus): {sin_verificar}")
    print()
    for r in catalogo:
        s = f' → señal: {r["señal"]}' if r["señal"] else ""
        print(f'   {r["id"]:20} [{r["tipo"]:11}] {r["opera_en"]} · sha {r["sha256"][:10]}{s}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
