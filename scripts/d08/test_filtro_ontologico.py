# -*- coding: utf-8 -*-
"""
scripts/d08/test_filtro_ontologico.py — Regresión del Filtro Ontológico QUIRA
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 3, 9]
  type: TECNICA

POR QUÉ EXISTE ESTE ARCHIVO
El cruce se ha roto CUATRO veces por la misma clase de error: **metadato de la
ficha POA leído como contenido sustantivo**.

  1. Membretes  — "GOBIERNO AUTONOMO DESCENTRALIZADO..." emparejaba con todo.
  2. Carnaval   — un rubro de festejos capturaba demandas de infraestructura.
  3. REGLA 0    — la dirección ejecutora ("Obras Públicas") figuraba como rubro
                  compatible de tres familias, y todo proyecto suyo heredaba
                  afinidad temática: "INUNDACIONES" ↔ "Arriendo de parqueaderos".
  4. Homógrafo  — "Parqueaderos" contiene "parque"; un estacionamiento no es
                  un área verde. Coincidir letras no es reconocer un rubro.

Que cada capa filtrada destape la siguiente NO es casualidad: es una propiedad
del documento (OBS-020 · la ficha POA mezcla partida·programa·actividad·unidad
en una sola fila). El motor se corrige aquí; el instrumento se mide allá.

Este archivo convierte esos hallazgos en verificación permanente: si alguien
vuelve a meter una unidad administrativa en una whitelist, falla antes de llegar
al expediente.

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
    # ★ CAMBIADO tras la validación de campo (2026-07-29): antes se esperaba `no-nula`.
    # La demanda se ancla en BARRIO SANTA ANA y el proyecto no dice dónde se ejecuta →
    # inverificable. Criterio de Javo: "si no se sabe dónde fue hecha la obra... esa
    # opacidad hace que no se pueda determinar si las peticiones fueron atendidas".
    ("ELIMINACION DE LETRINAS POZO SEPTICO (BARRIO SANTA ANA)",
     "Mantenimiento, operación y tratamientos de las Plantas de Tratamiento de "
     "aguas servidas y alcantarillado",
     "nula"),
    # …pero SÍ pasa cuando ambos lados declaran el MISMO lugar (caso 5 de la validación,
    # el único `directa` que Javo confirmó):
    ("MANTENIMIENTO DE TAPAS DE ALCANTARILLADO PARROQUIA LA PILA",
     "Crédito BDE - Construcción Sistema de Alcantarillado Sanitario Parroquia La Pila",
     "directa"),

    # ── Estructural = complementaria, nunca directa (se evalúa ANTES que incompatibles)
    ("MEJORA DEL PARQUE",
     "Actualizacion del catastro predial urbano y rural del canton",
     "complementaria"),

    # ── REGLA T1 · territorios distintos no se sustituyen ─────────────────────
    # Javo (2026-07-29): Las Paolas es zona urbana de la parroquia Colorado;
    # Las Pampas es comuna rural. El emparejador las cruzó por la palabra "parque".
    # Canon territorial §IX: "parroquia → parroquia: PROHIBIDO".
    ("MEJORA DEL PARQUE. (LAS PAOLAS)",
     "Construccción parque las Pampas · Urbanización y Embellecimiento",
     "nula"),
    # ★ CAMBIADO tras la validación de campo: un proyecto CANTONAL genérico NO acredita
    # atención a una demanda de barrio. La regla T1 ("cantón → parroquia: PERMITIDO")
    # habilita PROXIES ESTADÍSTICOS (NBI, cobertura), no la acreditación de que una
    # petición concreta fue atendida. Eran dos cosas distintas y estaban mezcladas.
    ("MEJORA DEL PARQUE. (LAS PAOLAS)",
     "Construcción y regeneración de parques del cantón",
     "nula"),

    # ── Homógrafos administrativos: coincidir letras ≠ reconocer un rubro ─────
    # "parqueadero" contiene "parque" pero un estacionamiento no es un área verde.
    ("MEJORA DEL PARQUE. (LAS PAOLAS)",
     "Edificios, Locales y Residencias, Parqueaderos, Casilleros Judiciales (Arrendamientos)",
     "nula"),
    # "plantas de tratamiento" contiene "planta" pero no es arborización
    ("CREAR AREAS VERDES EN EL BARRIO",
     "Mantenimiento y operación de las Plantas de Tratamiento de aguas servidas",
     "nula"),

    # ── Satisfacción FUNCIONAL entre familias · exige declaración técnica ─────
    # Criterio fijado por Javo: reforestación NO se presume mitigación de riesgo.
    # Sin propósito declarado en la ficha → nula.
    ("DAR PROTECCION A LAS QUEBRADAS MITIGANDO RIESGO",
     "Adquisicion de plantas para siembra de arboles en sectores identificados",
     "nula"),
    # Con propósito declarado → funcional. La diferencia la hace el expediente.
    ("DAR PROTECCION A LAS QUEBRADAS MITIGANDO RIESGO",
     "Siembra de arboles para estabilizacion de taludes y control de erosion en quebradas",
     "funcional"),
    # Declaración de ornato NO acredita mitigación
    ("DAR PROTECCION A LAS QUEBRADAS MITIGANDO RIESGO",
     "Siembra de plantas ornamentales para embellecimiento de aceras",
     "nula"),
]


def _ok(tipo: str, esperado: str) -> bool:
    if esperado == "nula":
        return tipo == "nula"
    if esperado == "no-nula":
        return tipo != "nula"
    return tipo == esperado


def main() -> int:
    print("=== REGRESIÓN · Filtro Ontológico QUIRA v3 · MRSPP ===\n")
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
