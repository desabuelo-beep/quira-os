"""
utils/snapshot_io.py — QUIRA OS v0.1
Lectura y escritura del snapshot maestro de municipios (municipality_snapshots).

Jerarquía de carga (para cualquier municipio):
  1. Supabase municipality_snapshots (is_active=TRUE, más reciente)
  2. data/gm_snapshot.json (fallback estático del repo — Montecristi)
  3. {} (vacío — la página mostrará empty_notice)

Uso:
    from utils.snapshot_io import load_snapshot, save_snapshot, validate_snapshot
    snap, meta = load_snapshot(municipio_code="130801")

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

# ── CLAVES OBLIGATORIAS en un gm_snapshot.json válido ────────────────────────
_REQUIRED_TOP_KEYS = {"_meta", "gad", "tgi", "financiero", "series_longitudinal", "territorial"}
_REQUIRED_META     = {"fecha_corte", "version_excel"}
_REQUIRED_GAD      = {"codigo", "nombre"}
_REQUIRED_TGI      = {"score"}


# ══════════════════════════════════════════════════════════════════════════════
# 1. VALIDACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def validate_snapshot(data: dict) -> tuple[bool, list[str]]:
    """Valida la estructura de un gm_snapshot.json candidato a subir.

    Args:
        data: dict cargado del JSON.

    Returns:
        (ok: bool, errors: list[str]) — errors vacío si ok=True.
    """
    errors: list[str] = []

    missing_top = _REQUIRED_TOP_KEYS - set(data.keys())
    if missing_top:
        errors.append(f"Claves de primer nivel faltantes: {sorted(missing_top)}")
        return False, errors  # no continuar — estructura incompleta

    meta = data.get("_meta", {})
    for k in _REQUIRED_META:
        if not meta.get(k):
            errors.append(f"_meta.{k} ausente o vacío")

    gad = data.get("gad", {})
    for k in _REQUIRED_GAD:
        if not gad.get(k):
            errors.append(f"gad.{k} ausente o vacío")

    codigo = gad.get("codigo", "")
    if codigo and (not str(codigo).isdigit() or len(str(codigo)) != 6):
        errors.append(f"gad.codigo debe ser 6 dígitos numéricos (recibido: '{codigo}')")

    tgi = data.get("tgi", {})
    score = tgi.get("score")
    # tgi.score puede ser None en snapshots Q1 (pipeline sin Gold Master TGI calculado).
    # Solo es error si tiene valor pero está fuera de rango.
    # Si fuente="pendiente" → snapshot Q1, score null es esperado.
    tgi_fuente = tgi.get("fuente", "")
    if score is None and tgi_fuente not in ("pendiente", "gold_master_h73"):
        errors.append("tgi.score ausente")
    elif score is not None and (not isinstance(score, (int, float)) or not (0 <= float(score) <= 100)):
        errors.append(f"tgi.score debe ser número 0-100 (recibido: {score})")

    return (len(errors) == 0), errors


# ══════════════════════════════════════════════════════════════════════════════
# 2. ESCRITURA EN SUPABASE
# ══════════════════════════════════════════════════════════════════════════════

def save_snapshot(
    conn,
    data: dict,
    uploaded_by: str = "tecnico",
    notas: str = "",
) -> tuple[bool, str]:
    """Guarda un snapshot validado en municipality_snapshots.

    Desactiva el snapshot anterior del mismo municipio y activa el nuevo.
    Si ya existe (mismo municipio_code + version), actualiza en lugar de insertar.

    Args:
        conn:        DbConn de sentinel.db_config.
        data:        dict validado con validate_snapshot().
        uploaded_by: usuario que realiza la carga.
        notas:       comentario libre del analista.

    Returns:
        (success: bool, mensaje: str)
    """
    try:
        ok, errors = validate_snapshot(data)
        if not ok:
            return False, f"Validación fallida: {'; '.join(errors)}"

        municipio_code = str(data["gad"]["codigo"])
        municipio_name = data["gad"]["nombre"]
        version        = data["_meta"]["version_excel"]
        fecha_corte    = data["_meta"]["fecha_corte"]
        json_str       = json.dumps(data, ensure_ascii=False)
        checksum       = hashlib.sha256(json_str.encode("utf-8")).hexdigest()[:20]
        uploaded_at    = datetime.now(timezone.utc).isoformat()

        c = conn.cursor()

        # Desactivar snapshot previo activo de este municipio
        c.execute(
            "UPDATE municipality_snapshots SET is_active=FALSE WHERE municipio_code=? AND is_active=TRUE",
            (municipio_code,),
        )

        if conn.mode == "supabase":
            # PostgreSQL: INSERT ... ON CONFLICT DO UPDATE
            c.execute("""
                INSERT INTO municipality_snapshots
                    (municipio_code, municipio_name, version, fecha_corte,
                     uploaded_at, uploaded_by, is_active, snapshot_json, checksum_sha256, notas)
                VALUES (%s,%s,%s,%s,%s,%s,TRUE,%s,%s,%s)
                ON CONFLICT (municipio_code, version)
                DO UPDATE SET
                    snapshot_json   = EXCLUDED.snapshot_json,
                    is_active       = TRUE,
                    uploaded_at     = EXCLUDED.uploaded_at,
                    uploaded_by     = EXCLUDED.uploaded_by,
                    checksum_sha256 = EXCLUDED.checksum_sha256,
                    notas           = EXCLUDED.notas
            """, (municipio_code, municipio_name, version, fecha_corte,
                  uploaded_at, uploaded_by, json_str, checksum, notas or ""))
        else:
            # SQLite: INSERT OR REPLACE
            c.execute("""
                INSERT OR REPLACE INTO municipality_snapshots
                    (municipio_code, municipio_name, version, fecha_corte,
                     uploaded_at, uploaded_by, is_active, snapshot_json, checksum_sha256, notas)
                VALUES (?,?,?,?,?,?,1,?,?,?)
            """, (municipio_code, municipio_name, version, fecha_corte,
                  uploaded_at, uploaded_by, json_str, checksum, notas or ""))

        conn.commit()
        return True, f"Snapshot v{version} de {municipio_name} guardado (SHA256: {checksum})"

    except Exception as exc:
        return False, f"Error al guardar: {exc}"


# ══════════════════════════════════════════════════════════════════════════════
# 3. LECTURA DESDE SUPABASE
# ══════════════════════════════════════════════════════════════════════════════

def load_snapshot(
    conn=None,
    municipio_code: str = "130801",
) -> tuple[dict | None, dict | None]:
    """Carga el snapshot activo de un municipio.

    Jerarquía:
      1. Supabase municipality_snapshots (is_active=TRUE)
      2. data/gm_snapshot.json (fallback estático)

    Args:
        conn:            DbConn (opcional — si None se abre y cierra internamente).
        municipio_code:  Código de 6 dígitos del municipio.

    Returns:
        (snapshot_dict, meta_dict) o (None, None) si no hay datos.
        meta_dict contiene: uploaded_at, version, uploaded_by, source.
    """
    # ── Intento 1: Supabase ───────────────────────────────────────────────────
    close_after = False
    if conn is None:
        try:
            from sentinel.db_config import get_connection
            conn = get_connection()
            close_after = True
        except Exception:
            conn = None

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(
                """SELECT snapshot_json, uploaded_at, version, uploaded_by
                   FROM municipality_snapshots
                   WHERE municipio_code=? AND is_active=TRUE
                   ORDER BY uploaded_at DESC LIMIT 1""",
                (municipio_code,),
            )
            row = c.fetchone()
            if close_after:
                conn.close()
            if row:
                data = json.loads(row["snapshot_json"])
                meta = {
                    "uploaded_at": row["uploaded_at"],
                    "version":     row["version"],
                    "uploaded_by": row["uploaded_by"],
                    "source":      "supabase",
                }
                return data, meta
        except Exception:
            if close_after and conn:
                try:
                    conn.close()
                except Exception:
                    pass

    # ── Intento 2: JSON estático del repo ────────────────────────────────────
    # Solo aplica para Montecristi (municipio_code 130801 = código canónico)
    if municipio_code == "130801":
        try:
            import os
            json_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "data", "gm_snapshot.json"
            )
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            meta = {
                "uploaded_at": data.get("_meta", {}).get("sincronizado", "desconocido"),
                "version":     data.get("_meta", {}).get("version_excel", "static"),
                "uploaded_by": "repo-estático",
                "source":      "json_file",
            }
            return data, meta
        except Exception:
            pass

    return None, None


def list_snapshots(conn=None) -> list[dict]:
    """Lista todos los snapshots en Supabase (activos e inactivos), más recientes primero."""
    close_after = False
    if conn is None:
        try:
            from sentinel.db_config import get_connection
            conn = get_connection()
            close_after = True
        except Exception:
            return []
    try:
        c = conn.cursor()
        c.execute(
            """SELECT municipio_code, municipio_name, version, fecha_corte,
                      uploaded_at, uploaded_by, is_active, checksum_sha256, notas
               FROM municipality_snapshots
               ORDER BY uploaded_at DESC LIMIT 50"""
        )
        rows = c.fetchall()
        if close_after:
            conn.close()
        return rows
    except Exception:
        if close_after and conn:
            try:
                conn.close()
            except Exception:
                pass
        return []
