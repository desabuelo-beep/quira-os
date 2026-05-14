"""
QUIRA OS v0.1 — Lector estructural Excel SIAP-ICPI
Lee metadatos desde el Excel; valores Q1-2026 vienen de demo_data.py
Dylus Lab © 2026
"""
import pandas as pd
import streamlit as st
from typing import Optional
from config import get_siap_path, PDOT_PATH, AVEP
from data.demo_data import (
    ICGIT_Q1_2026, INDICES, CONGRUENCIAS,
    SAT_ACTIVAS, HOLDING, PARROQUIAS,
)


# ── AVEP ENGINE ────────────────────────────────────────────────────────────────
def classify_avep(score: float) -> dict:
    """Clasifica un score 0-100 en la escala AVEP canónica (H01)."""
    ratio = score / 100.0
    for band in AVEP:
        if band["min"] <= ratio <= band["max"]:
            return band
    # fallback Ruptura Sistémica
    return AVEP[-1]


def avep_badge(score: Optional[float]) -> tuple[str, str, str]:
    """Devuelve (emoji, label, color) para un score. None → '⏳ En construcción'."""
    if score is None:
        return "⏳", "En construcción", "#7C5CFC"
    band = classify_avep(score)
    return band["emoji"], band["label"], band["color"]


# ── LECTOR EXCEL ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _load_excel_sheet(sheet_name: str) -> Optional[pd.DataFrame]:
    """Lee una hoja del Excel SIAP-ICPI. Retorna None si falla."""
    try:
        path = get_siap_path()
        df = pd.read_excel(path, sheet_name=sheet_name, header=None)
        return df
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def _load_pdot_sheet(sheet_name: str) -> Optional[pd.DataFrame]:
    """Lee una hoja del Excel PDOT_KB. Retorna None si falla."""
    try:
        df = pd.read_excel(PDOT_PATH, sheet_name=sheet_name, header=None)
        return df
    except Exception:
        return None


# ── ENTIDADES (H71) ────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_entidades() -> list[dict]:
    """
    Intenta leer nombres de entidades desde H71_EP_ADSCRITAS.
    Si falla o está vacío, usa HOLDING demo.
    """
    df = _load_excel_sheet("H71")
    if df is not None and not df.empty:
        # H71 estructura esperada: col-0=id, col-1=nombre, col-2=tipo
        try:
            rows = []
            for _, row in df.iterrows():
                nombre = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
                if nombre and nombre not in ("nan", ""):
                    rows.append({"nombre": nombre})
            if rows:
                # Merge con HOLDING para scores (Excel no tiene scores calculados)
                merged = []
                for i, entity in enumerate(HOLDING["entidades"]):
                    if i < len(rows):
                        entity = dict(entity)
                        entity["nombre"] = rows[i]["nombre"]
                    merged.append(entity)
                return merged
        except Exception:
            pass
    return HOLDING["entidades"]


# ── PARROQUIAS (PDOT_KB) ───────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_parroquias() -> list[dict]:
    """
    Intenta leer metadatos de parroquias desde PDOT_KB.
    Usa PARROQUIAS demo como fuente de scores y participación (Excel = estructural).
    """
    # Scores y participación siempre vienen de demo_data (sellado Q1-2026)
    return PARROQUIAS


# ── LOADER PRINCIPAL ───────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_all() -> dict:
    """
    Devuelve el estado completo del sistema QUIRA OS.
    Estrategia híbrida:
      - Estructura/metadatos → Excel (cuando disponible)
      - Valores calculados Q1-2026 → demo_data.py (sellado, verificado)
    """
    entidades = load_entidades()
    parroquias = load_parroquias()

    # Enriquecer ICGI-T con bandas AVEP
    icgit = dict(ICGIT_Q1_2026)
    band = classify_avep(icgit["score"])
    icgit["color"]       = band["color"]
    icgit["avep_color"]  = band["color"]
    icgit["nivel"]       = band["nivel"]

    # Enriquecer índices con band fallback
    indices = {}
    for key, idx in INDICES.items():
        idx = dict(idx)
        if idx["valor"] is not None:
            b = classify_avep(idx["valor"])
            idx.setdefault("color", b["color"])
            idx.setdefault("emoji", b["emoji"])
        indices[key] = idx

    # Enriquecer congruencias
    congruencias = {}
    for key, c in CONGRUENCIAS.items():
        c = dict(c)
        b = classify_avep(c["score"])
        c.setdefault("color_avep", b["color"])
        congruencias[key] = c

    # Enriquecer holding
    holding = dict(HOLDING)
    holding["entidades"] = []
    for e in entidades:
        e = dict(e)
        b = classify_avep(e["score"])
        e["color"]  = b["color"]
        e["emoji"]  = b["emoji"]
        e["avep"]   = b["label"]
        holding["entidades"].append(e)

    return {
        "icgit":        icgit,
        "indices":      indices,
        "congruencias": congruencias,
        "sat":          SAT_ACTIVAS,
        "holding":      holding,
        "parroquias":   parroquias,
        "excel_ok":     _excel_available(),
    }


def _excel_available() -> bool:
    """Verifica si el Excel SIAP-ICPI está accesible."""
    try:
        get_siap_path()
        return True
    except FileNotFoundError:
        return False


# ── HELPERS GLOBALES ───────────────────────────────────────────────────────────
def get_sat_counts(data: dict) -> dict:
    """Cuenta SATs por nivel."""
    sat = data.get("sat", [])
    return {
        "criticos":    sum(1 for s in sat if s["nivel"] == "CRÍTICO"),
        "alertas":     sum(1 for s in sat if s["nivel"] == "ALERTA"),
        "total":       len(sat),
        "activas":     sum(1 for s in sat if s["estado"] == "ACTIVA"),
        "preventivas": sum(1 for s in sat if s["estado"] == "PREVENTIVA"),
    }


def get_parroquia_by_nombre(data: dict, nombre: str) -> Optional[dict]:
    """Busca una parroquia por nombre (case-insensitive)."""
    for p in data.get("parroquias", []):
        if p["nombre"].lower() == nombre.lower():
            return p
    return None


def get_zonas_sin_voz(data: dict) -> list[dict]:
    """Retorna parroquias con participación en estado 'Sin voz'."""
    return [
        p for p in data.get("parroquias", [])
        if p.get("participacion", {}).get("estado") == "Sin voz"
    ]


def format_currency(value: int | float, symbol: "$") -> str:
    """Formatea un valor monetario con separador de miles."""
    return f"{symbol}{value:,.0f}"


def delta_vs_meta(score: float, meta: float) -> tuple[float, str]:
    """Retorna (delta, color) respecto a una meta."""
    delta = score - meta
    color = "#38A169" if delta >= 0 else "#E53E3E"
    return delta, color
