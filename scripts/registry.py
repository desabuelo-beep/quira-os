#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/registry.py — QUIRA OS
Módulo CRUD para el registro canónico de municipios.

Proporciona acceso tipado a data/municipality_registry.json y funciones
auxiliares para el RC-PIPELINE. Evita búsquedas O(n) en cada paso del pipeline
usando los índices lookup del registro.

Uso:
    from scripts.registry import get_by_ruc, get_by_code, get_all_active

    m = get_by_ruc("1360000980001")   # → dict de Manta
    m = get_by_code("130901")          # → mismo dict
    m = get_by_dpe_id(936)             # → mismo dict

    all_active = get_all_active()      # → lista de dicts

    # Actualizar campo en el registro (persiste en JSON)
    update_field("130901", "youtube_channel", "UCxxxxx")
    update_field("130901", "cpccs_slug", "gad-manta")

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

# ── Ruta canónica del registro ────────────────────────────────────────────────
_REGISTRY_PATH = Path(__file__).parent.parent / "data" / "municipality_registry.json"

# ── Cache en memoria (cargado una vez por proceso) ───────────────────────────
_cache: dict | None = None


# ══════════════════════════════════════════════════════════════════════════════
# CARGA Y PERSISTENCIA
# ══════════════════════════════════════════════════════════════════════════════

def _load() -> dict:
    """Carga el registro desde disco. Cachea en memoria."""
    global _cache
    if _cache is None:
        with open(_REGISTRY_PATH, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def _save(data: dict) -> None:
    """Persiste el registro en disco y actualiza el cache."""
    global _cache
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    _cache = data


def reload() -> None:
    """Fuerza recarga desde disco (útil en scripts que modifican el archivo)."""
    global _cache
    _cache = None
    _load()


# ══════════════════════════════════════════════════════════════════════════════
# CONSULTAS (READ)
# ══════════════════════════════════════════════════════════════════════════════

def get_all() -> list[dict]:
    """Retorna todos los municipios del registro (activos e inactivos)."""
    return deepcopy(_load()["municipios"])


def get_all_active() -> list[dict]:
    """Retorna solo municipios con is_active=True."""
    return [deepcopy(m) for m in _load()["municipios"] if m.get("is_active")]


def get_primary() -> dict | None:
    """Retorna el municipio primario (Gold Master — Montecristi)."""
    for m in _load()["municipios"]:
        if m.get("is_primary"):
            return deepcopy(m)
    return None


def get_by_code(municipio_code: str) -> dict | None:
    """Busca un municipio por su código de 6 dígitos (gad.codigo)."""
    for m in _load()["municipios"]:
        if m["municipio_code"] == str(municipio_code):
            return deepcopy(m)
    return None


def get_by_ruc(ruc: str) -> dict | None:
    """Busca un municipio por RUC (13 dígitos). Usa índice O(1)."""
    data = _load()
    code = data["lookup"]["por_ruc"].get(str(ruc))
    if code:
        return get_by_code(code)
    return None


def get_by_dpe_id(dpe_id: int | str) -> dict | None:
    """Busca un municipio por DPE establishment_id. Usa índice O(1)."""
    data = _load()
    code = data["lookup"]["por_dpe_id"].get(str(dpe_id))
    if code:
        return get_by_code(code)
    return None


def get_by_canton(canton: str) -> dict | None:
    """Busca por nombre de cantón (case-insensitive, sin tildes opcionales)."""
    canton_norm = canton.strip().lower()
    for m in _load()["municipios"]:
        if m["canton"].lower() == canton_norm:
            return deepcopy(m)
    return None


def list_summary() -> list[dict]:
    """Retorna resumen tabular de todos los municipios (para logs y CLI)."""
    rows = []
    for m in _load()["municipios"]:
        rows.append({
            "code":       m["municipio_code"],
            "canton":     m["canton"],
            "ruc":        m["ruc"],
            "dpe_id":     m.get("dpe_establishment_id"),
            "is_active":  m.get("is_active", False),
            "is_primary": m.get("is_primary", False),
            "score":      m.get("scouting_score"),
            "snap_ver":   m.get("snapshot_version"),
        })
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# ESCRITURA (UPDATE)
# ══════════════════════════════════════════════════════════════════════════════

def update_field(municipio_code: str, field: str, value: Any) -> bool:
    """Actualiza un campo en el registro y persiste en JSON.

    Args:
        municipio_code: código de 6 dígitos del municipio.
        field: nombre del campo a actualizar (top-level del dict).
        value: nuevo valor.

    Returns:
        True si el municipio fue encontrado y actualizado, False si no existe.

    Ejemplo:
        update_field("130901", "youtube_channel", "UCxxxx")
        update_field("130901", "cpccs_slug", "gad-manta-2024")
        update_field("130901", "is_active", True)
    """
    data = _load()
    for m in data["municipios"]:
        if m["municipio_code"] == municipio_code:
            m[field] = value
            _save(data)
            return True
    return False


def update_snapshot_version(municipio_code: str, version: str) -> bool:
    """Actualiza snapshot_version en el registro."""
    return update_field(municipio_code, "snapshot_version", version)


def activate(municipio_code: str) -> bool:
    """Marca un municipio como activo en QUIRA."""
    return update_field(municipio_code, "is_active", True)


def deactivate(municipio_code: str) -> bool:
    """Marca un municipio como inactivo en QUIRA."""
    return update_field(municipio_code, "is_active", False)


def update_social_links(
    municipio_code: str,
    youtube_channel: str | None = None,
    facebook_page: str | None = None,
) -> bool:
    """Actualiza los enlaces de redes sociales de un municipio."""
    data = _load()
    found = False
    for m in data["municipios"]:
        if m["municipio_code"] == municipio_code:
            if youtube_channel is not None:
                m["youtube_channel"] = youtube_channel
            if facebook_page is not None:
                m["facebook_page"] = facebook_page
            found = True
            break
    if found:
        _save(data)
    return found


def update_cpccs_slug(municipio_code: str, slug: str) -> bool:
    """Actualiza el CPCCS slug (identificador en portal rendiciondecuentas.cpccs.gob.ec)."""
    return update_field(municipio_code, "cpccs_slug", slug)


def update_alcalde(
    municipio_code: str,
    alcalde: str,
    email: str | None = None,
) -> bool:
    """Actualiza el nombre del alcalde/alcaldesa en el registro."""
    data = _load()
    for m in data["municipios"]:
        if m["municipio_code"] == municipio_code:
            m["alcalde_actual"] = alcalde
            if email:
                m["email_alcalde"] = email
            _save(data)
            return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
# LOOKUP REBUILD (mantenimiento)
# ══════════════════════════════════════════════════════════════════════════════

def rebuild_lookup() -> None:
    """Reconstruye los índices lookup a partir de los municipios actuales.

    Llamar si se agregan municipios manualmente o se cambian RUCs/DPE IDs.
    """
    data = _load()
    por_ruc: dict[str, str] = {}
    por_dpe: dict[str, str] = {}

    for m in data["municipios"]:
        code = m["municipio_code"]
        ruc  = m.get("ruc")
        dpe  = m.get("dpe_establishment_id")
        if ruc:
            por_ruc[ruc] = code
        if dpe:
            por_dpe[str(dpe)] = code

    data["lookup"]["por_ruc"] = por_ruc
    data["lookup"]["por_dpe_id"] = por_dpe
    data["_meta"]["lookup_rebuilt"] = date.today().isoformat()
    _save(data)
    print(f"[OK] Lookup reconstruido: {len(por_ruc)} RUCs, {len(por_dpe)} DPE IDs")


# ══════════════════════════════════════════════════════════════════════════════
# CLI (modo standalone)
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    import argparse
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Consulta y actualiza el registro de municipios QUIRA OS",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list
    p_list = sub.add_parser("list", help="Listar todos los municipios")
    p_list.add_argument("--active", action="store_true", help="Solo activos")

    # get
    p_get = sub.add_parser("get", help="Obtener municipio")
    grp = p_get.add_mutually_exclusive_group(required=True)
    grp.add_argument("--code",   help="municipio_code (6 dígitos)")
    grp.add_argument("--ruc",    help="RUC (13 dígitos)")
    grp.add_argument("--dpe-id", type=int, help="DPE establishment_id")
    grp.add_argument("--canton", help="Nombre del cantón")

    # set
    p_set = sub.add_parser("set", help="Actualizar campo de un municipio")
    p_set.add_argument("--code",  required=True, help="municipio_code (6 dígitos)")
    p_set.add_argument("--field", required=True, help="Campo a actualizar")
    p_set.add_argument("--value", required=True, help="Nuevo valor")

    # activate / deactivate
    p_act = sub.add_parser("activate", help="Activar municipio en QUIRA")
    p_act.add_argument("--code", required=True)

    p_deact = sub.add_parser("deactivate", help="Desactivar municipio en QUIRA")
    p_deact.add_argument("--code", required=True)

    # rebuild-lookup
    sub.add_parser("rebuild-lookup", help="Reconstruir índices de búsqueda")

    args = parser.parse_args()

    if args.cmd == "list":
        rows = get_all_active() if args.active else get_all()
        for m in rows:
            marker = "(PRIMARY)" if m.get("is_primary") else ""
            active = "[ACTIVO]" if m.get("is_active") else "[inactivo]"
            print(f"  {m['municipio_code']}  {m['canton']:<20}  RUC:{m['ruc']}  "
                  f"DPE:{m.get('dpe_establishment_id','?')}  "
                  f"score:{m.get('scouting_score','—')}  {active} {marker}")

    elif args.cmd == "get":
        if args.code:
            m = get_by_code(args.code)
        elif args.ruc:
            m = get_by_ruc(args.ruc)
        elif args.dpe_id:
            m = get_by_dpe_id(args.dpe_id)
        else:
            m = get_by_canton(args.canton)

        if m:
            print(json.dumps(m, ensure_ascii=False, indent=2))
        else:
            print("[XX] Municipio no encontrado")
            sys.exit(1)

    elif args.cmd == "set":
        # Intentar parsear value como JSON (para booleans, nums, null)
        try:
            value = json.loads(args.value)
        except json.JSONDecodeError:
            value = args.value  # string literal

        ok = update_field(args.code, args.field, value)
        if ok:
            print(f"[OK] {args.code}.{args.field} = {value!r}")
        else:
            print(f"[XX] Municipio {args.code} no encontrado")
            sys.exit(1)

    elif args.cmd == "activate":
        ok = activate(args.code)
        print(f"[OK] {args.code} activado" if ok else f"[XX] {args.code} no encontrado")

    elif args.cmd == "deactivate":
        ok = deactivate(args.code)
        print(f"[OK] {args.code} desactivado" if ok else f"[XX] {args.code} no encontrado")

    elif args.cmd == "rebuild-lookup":
        rebuild_lookup()


if __name__ == "__main__":
    main()
