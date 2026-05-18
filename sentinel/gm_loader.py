"""
sentinel/gm_loader.py
Gold Master Snapshot Loader — Sprint 2.4

Carga el snapshot de outputs verificados del Gold Master (data/gm_snapshot.json).
El Excel SIAP-ICPI es propiedad exclusiva de Dylus Lab y NUNCA se lee directamente
desde la aplicación. Solo se expone este snapshot con los outputs institucionales públicos.

Garantías:
  - Si el archivo no existe → retorna estructura vacía con flag valid=False
  - Si el archivo está corrupto → retorna estructura vacía con flag valid=False
  - Los datos son de solo lectura desde la app; se actualizan manualmente desde el Excel

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import datetime
from pathlib import Path
from typing import Optional

# ── RUTA AL SNAPSHOT ──────────────────────────────────────────────────────────
_SNAPSHOT_PATH = Path(__file__).parent.parent / "data" / "gm_snapshot.json"


# ── CARGA PRINCIPAL ───────────────────────────────────────────────────────────
def load() -> dict:
    """
    Carga el snapshot del Gold Master.

    Returns:
        dict con las claves: _meta, gad, tgi, financiero, territorial
        Incluye siempre: _loaded=True/False, _error=str|None
    """
    if not _SNAPSHOT_PATH.exists():
        return {"_loaded": False, "_error": "Snapshot no encontrado. Contactar analista Dylus Lab."}
    try:
        with _SNAPSHOT_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data["_loaded"] = True
        data["_error"]  = None
        return data
    except json.JSONDecodeError as e:
        return {"_loaded": False, "_error": f"Error parsing snapshot: {e}"}
    except Exception as e:
        return {"_loaded": False, "_error": f"Error inesperado: {e}"}


# ── ACCESORES TIPADOS ─────────────────────────────────────────────────────────
def get_gad(gm: dict) -> dict:
    return gm.get("gad", {})


def get_tgi(gm: dict) -> dict:
    return gm.get("tgi", {})


def get_financiero(gm: dict) -> dict:
    return gm.get("financiero", {})


def get_territorial(gm: dict) -> dict:
    return gm.get("territorial", {})


def get_parroquias(gm: dict) -> list[dict]:
    return get_territorial(gm).get("parroquias", [])


def get_parroquia_critica(gm: dict) -> Optional[dict]:
    """Retorna los datos de la parroquia con mayor necesidad (composite_need)."""
    nombre = get_territorial(gm).get("parroquia_critica", "")
    for p in get_parroquias(gm):
        if p.get("nombre") == nombre:
            return p
    return None


def get_dim(gm: dict, codigo: str) -> dict:
    """Retorna los datos de una dimensión TGI (D1–D5)."""
    tgi = get_tgi(gm)
    key = codigo.lower()   # "d1", "d2", etc.
    return tgi.get(key, {})


# ── CÁLCULOS EN TIEMPO REAL ───────────────────────────────────────────────────
def mandato_progress(gm: dict) -> dict:
    """
    Calcula el progreso del mandato en tiempo real.

    Returns:
        pct_ejecutado: porcentaje completado (0-100)
        dias_restantes: días hasta el fin del mandato
        dias_totales: duración total del mandato
        dias_transcurridos: días desde el inicio
    """
    gad = get_gad(gm)
    try:
        inicio = datetime.date.fromisoformat(gad.get("inicio_mandato", "2023-05-23"))
        fin    = datetime.date.fromisoformat(gad.get("fin_mandato",   "2027-05-23"))
        hoy    = datetime.date.today()

        totales      = (fin - inicio).days
        transcurridos = max(0, (hoy - inicio).days)
        restantes    = max(0, (fin - hoy).days)
        pct          = round(min(100.0, (transcurridos / totales) * 100), 1) if totales > 0 else 0.0

        return {
            "pct_ejecutado":    pct,
            "dias_restantes":   restantes,
            "dias_transcurridos": transcurridos,
            "dias_totales":     totales,
            "inicio":           gad.get("inicio_mandato", ""),
            "fin":              gad.get("fin_mandato",    ""),
        }
    except Exception:
        return {
            "pct_ejecutado":    0.0,
            "dias_restantes":   0,
            "dias_transcurridos": 0,
            "dias_totales":     1461,
            "inicio":           "",
            "fin":              "",
        }


def tgi_color(valor: float) -> str:
    """Retorna color hexadecimal según el rango TGI."""
    if valor >= 85: return "#00D4FF"   # Excelencia — azul
    if valor >= 75: return "#00E096"   # Gobernanza Inteligente — verde
    if valor >= 65: return "#FFB800"   # Transición con Riesgos — ámbar
    if valor >= 50: return "#FF7800"   # Inequidad Estructural — naranja
    return "#FF4D6D"                   # Emergencia Territorial — rojo


def dim_color(valor: float) -> str:
    """Retorna color según umbral de dimensión (distinto a TGI global)."""
    if valor >= 75: return "#00E096"
    if valor >= 55: return "#FFB800"
    return "#FF4D6D"


def tgi_clasificacion_emoji(clasificacion: str) -> str:
    return {
        "Excelencia Territorial":    "🔵",
        "Gobernanza Inteligente":    "🟢",
        "Transición con Riesgos":    "🟡",
        "Inequidad Estructural":     "🟠",
        "Emergencia Territorial":    "🔴",
    }.get(clasificacion, "•")


def meta_info(gm: dict) -> dict:
    """Snapshot date and version for audit display."""
    meta = gm.get("_meta", {})
    return {
        "fecha_corte":      meta.get("fecha_corte", "–"),
        "version_excel":    meta.get("version_excel", "–"),
        "proxima_actualizacion": meta.get("proxima_actualizacion", "–"),
    }


# ── RANGOS DE EQUIDAD PARROQUIAL ──────────────────────────────────────────────
def iet_color(iet_local_pct: float) -> str:
    """Color semáforo por IET local de parroquia."""
    if iet_local_pct >= 90: return "#00E096"
    if iet_local_pct >= 60: return "#FFB800"
    if iet_local_pct >= 40: return "#FF7800"
    return "#FF4D6D"


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    gm = load()
    if not gm.get("_loaded"):
        print(f"ERROR: {gm.get('_error')}")
    else:
        gad  = get_gad(gm)
        tgi  = get_tgi(gm)
        prog = mandato_progress(gm)
        critica = get_parroquia_critica(gm)

        print("=" * 60)
        print(f"  GAD   : {gad.get('nombre')}")
        print(f"  Alcalde: {gad.get('alcalde')}")
        print(f"  Mandato: {prog['pct_ejecutado']}% · {prog['dias_restantes']} días restantes")
        print(f"  TGI    : {tgi.get('score')} — {tgi.get('clasificacion')}")
        print(f"  IRS    : {tgi.get('irs', {}).get('valor')} ({tgi.get('irs', {}).get('clasificacion')})")
        if critica:
            print(f"  Crítica: {critica.get('nombre')} NBI={critica.get('nbi_pct')}% IET={critica.get('iet_local_pct')}%")
        print(f"  Fuente : {gm.get('_meta', {}).get('version_excel')} · {gm.get('_meta', {}).get('fecha_corte')}")
        print("=" * 60)
