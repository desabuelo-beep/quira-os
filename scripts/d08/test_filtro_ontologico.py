# -*- coding: utf-8 -*-
"""
scripts/d08/test_filtro_ontologico.py — Regresión del Filtro Ontológico QUIRA
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 3, 9]
  type: TECNICA

POR QUÉ EXISTE ESTE ARCHIVO
El filtro se ha roto TRES veces por la misma clase de error: **metadato
institucional leído como contenido sustantivo**.

  1. Membretes  — "GOBIERNO AUTONOMO DESCENTRALIZADO..." emparejaba con todo.
  2. Carnaval   — un rubro de festejos capturaba demandas de infraestructura.
  3. REGLA 0    — la dirección ejecutora ("Obras Públicas") figuraba como rubro
                  compatible de tres familias, y todo proyecto suyo heredaba
                  afinidad temática: "INUNDACIONES" ↔ "Arriendo de parqueaderos".

Cada vez se detectó por muestreo manual, tarde. Este archivo convierte esos
hallazgos en verificación permanente: si alguien vuelve a meter el nombre de una
unidad administrativa en una whitelist, esto falla antes de llegar al expediente.

Uso:  python scripts/d08/test_filtro_ontologico.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import filtro_ontologico as fo  # noqa: E402

# (demanda, texto POA, esperado)
#   esperado = tipo exacto | "nula" | "no-nula"
CASOS: list[tuple[str, str, str]] = [
    # ── REGLA 0 · la unidad ejecutora NO acredita el objeto del gasto ──────────
    ("INUNDACIONES- MANANTIALES",
     "Edificios, Locales y Residencias, Parqueaderos, Casilleros Judiciales "
     "(Arrendamientos) · DIRECCION DE OBRAS PUBLICAS",
     "nula"),
    ("MEJORAR LA VIA DEL BARRIO",
     "Adquisicion de mobiliario de oficina · DIRECCION DE OBRAS PUBLICAS",
     "nula"),
    # el mismo proyecto CON rubro técnico real sí debe pasar
    ("MEJORAMIENTO VIAL BARRIO X",
     "Adoquinado de calles del sector · DIRECCION DE OBRAS PUBLICAS",
     "directa"),

    # ── Rubro de eventos jamás satisface infraestructura (hallazgo de Javo) ────
    ("RECOLECCION DE BASURA",
     "Feriado carnaval 2024 · Espectaculos culturales · 730207",
     "nula"),
    # …salvo que la demanda sea explícitamente cultural
    ("APOYO A LAS FIESTAS PATRONALES DEL BARRIO",
     "Feriado carnaval 2024 · Espectaculos culturales · 730207",
     "no-nula"),

    # ── Correspondencias legítimas que NO deben perderse ──────────────────────
    ("AREAS VERDES",
     "Construccción parque las Pampas · Urbanización y Embellecimiento",
     "directa"),
    ("ELIMINACION DE LETRINAS POZO SEPTICO (BARRIO SANTA ANA)",
     "Mantenimiento, operación y tratamientos de las Plantas de Tratamiento de "
     "aguas servidas y alcantarillado",
     "no-nula"),

    # ── Estructural = indirecta, nunca directa (evaluado ANTES que incompatibles)
    ("MEJORA DEL PARQUE",
     "Actualizacion del catastro predial urbano y rural del canton",
     "indirecta"),

    # ── CUESTIÓN ABIERTA PARA JAVO (2026-07-29) ───────────────────────────────
    # ¿La siembra de árboles es instrumento FUNCIONAL de mitigación de riesgo en
    # quebradas? Técnicamente la reforestación estabiliza taludes. Hoy el filtro
    # dice `nula` de forma CONSERVADORA: no hay rubro técnico que lo acredite, y
    # `sin_correlato` no afirma que no se atendió (Principio de No-Inferencia).
    # Antes daba `funcional`, pero por el bug de REGLA 0 — no por conocimiento.
    # Si Javo confirma la relación, se añade el rubro; no se infiere sin él.
    ("DAR PROTECCION A LAS QUEBRADAS MITIGANDO RIESGO",
     "Adquisicion de plantas para siembra de arboles en sectores identificados",
     "nula"),
]


def _ok(tipo: str, esperado: str) -> bool:
    if esperado == "nula":
        return tipo == "nula"
    if esperado == "no-nula":
        return tipo != "nula"
    return tipo == esperado


def main() -> int:
    print("=== REGRESIÓN · Filtro Ontológico QUIRA v2 ===\n")
    fallos = 0
    for demanda, poa, esperado in CASOS:
        tipo, razon = fo.evaluar_relacion(demanda, poa)
        ok = _ok(tipo, esperado)
        fallos += not ok
        print(f"  {'OK   ' if ok else 'FALLA'} {tipo:12} (esperado {esperado:9}) ← {demanda[:46]}")
        if not ok:
            print(f"          motivo: {razon}")

    # invariante estructural: ninguna whitelist puede nombrar una unidad administrativa
    print("\n--- INVARIANTE · ninguna whitelist nombra unidades administrativas ---")
    intrusos = {fam: [t for t in toks if any(u in t for u in fo.UNIDADES_EJECUTORAS)]
                for fam, toks in fo.RUBROS_COMPATIBLES.items()}
    intrusos = {k: v for k, v in intrusos.items() if v}
    if intrusos:
        fallos += 1
        print(f"  FALLA — unidades ejecutoras usadas como rubro técnico: {intrusos}")
    else:
        print("  OK    — todos los rubros describen el OBJETO del gasto, no quién lo ejecuta")

    print(f"\n{'TODO OK' if not fallos else f'{fallos} FALLO(S)'} · {len(CASOS)} casos")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
