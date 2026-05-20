"""
scripts/seed_demo.py
Sembrador de datos de demostración — RC-1.C

Crea un escenario institucional controlado en Supabase:
  · monthly_kpis    — ejecución Q1 2026 para 4 entidades
  · alerts_history  — 10 alertas en estados variados
  · alert_timeline  — bitácora de 8 alertas procesadas
  · resolution_patterns — 3 patrones históricos

Uso:
    python scripts/seed_demo.py            # insertar (idempotente)
    python scripts/seed_demo.py --reset    # borrar demo y reinsertar

Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


# ── Leer secrets.toml sin Streamlit ──────────────────────────────────────────

def _read_supabase_uri() -> str:
    toml_path = Path(__file__).parent.parent / ".streamlit" / "secrets.toml"
    if not toml_path.exists():
        sys.exit(f"No se encontró {toml_path}. Ejecutar desde la raíz del proyecto.")
    content = toml_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if "supabase_uri" in line and "=" in line:
            _, val = line.split("=", 1)
            return val.strip().strip('"').strip("'")
    sys.exit("supabase_uri no encontrado en secrets.toml")


def _parse_pg_uri(uri: str) -> dict:
    uri = uri.strip()
    _, rest = uri.split("://", 1)
    creds, hostpart = rest.rsplit("@", 1)
    user, password  = creds.split(":", 1)
    host_port, dbname = hostpart.split("/", 1)
    if ":" in host_port:
        host, port = host_port.rsplit(":", 1)
    else:
        host, port = host_port, "5432"
    return dict(host=host.strip(), port=int(port.strip()),
                dbname=dbname.strip(), user=user.strip(), password=password.strip())


def _connect():
    import psycopg2
    import psycopg2.extras
    uri = _read_supabase_uri()
    kw  = _parse_pg_uri(uri)
    conn = psycopg2.connect(**kw, cursor_factory=psycopg2.extras.RealDictCursor)
    conn.autocommit = False
    return conn


# ── Datos de demostración ─────────────────────────────────────────────────────

_UPLOADS = [
    # (document_type, period_year, period_month, entidad, file_name, sha256)
    ("CEDULA_PRESUPUESTARIA", 2026, 1, "GAD",       "gad_presupuesto_202601.xlsx",       "demo_gad_202601"),
    ("CEDULA_PRESUPUESTARIA", 2026, 2, "GAD",       "gad_presupuesto_202602.xlsx",       "demo_gad_202602"),
    ("CEDULA_PRESUPUESTARIA", 2026, 3, "GAD",       "gad_presupuesto_202603.xlsx",       "demo_gad_202603"),
    ("CEDULA_PRESUPUESTARIA", 2026, 1, "BOMBEROS",  "bomberos_presupuesto_202601.xlsx",  "demo_bomberos_202601"),
    ("CEDULA_PRESUPUESTARIA", 2026, 2, "BOMBEROS",  "bomberos_presupuesto_202602.xlsx",  "demo_bomberos_202602"),
    ("CEDULA_PRESUPUESTARIA", 2026, 3, "BOMBEROS",  "bomberos_presupuesto_202603.xlsx",  "demo_bomberos_202603"),
    ("CEDULA_PRESUPUESTARIA", 2026, 1, "EMAI-EP",   "emaiep_presupuesto_202601.xlsx",    "demo_emaiep_202601"),
    ("CEDULA_PRESUPUESTARIA", 2026, 2, "EMAI-EP",   "emaiep_presupuesto_202602.xlsx",    "demo_emaiep_202602"),
    ("CEDULA_PRESUPUESTARIA", 2026, 3, "EMAI-EP",   "emaiep_presupuesto_202603.xlsx",    "demo_emaiep_202603"),
    ("CEDULA_PRESUPUESTARIA", 2026, 1, "PATRONATO", "patronato_presupuesto_202601.xlsx", "demo_patronato_202601"),
    ("CEDULA_PRESUPUESTARIA", 2026, 2, "PATRONATO", "patronato_presupuesto_202602.xlsx", "demo_patronato_202602"),
    ("CEDULA_PRESUPUESTARIA", 2026, 3, "PATRONATO", "patronato_presupuesto_202603.xlsx", "demo_patronato_202603"),
]

_KPIS = [
    # (period_year, period_month, entidad, ti_mensual_pct, devengado_inv, codificado_inv)
    (2026, 1, "GAD",        8.5,  85000,  1000000),
    (2026, 1, "BOMBEROS",  22.3,  89200,   400000),
    (2026, 1, "EMAI-EP",   41.2, 206000,   500000),
    (2026, 1, "PATRONATO", 12.1,  36300,   300000),
    (2026, 2, "GAD",       12.8, 128000,  1000000),
    (2026, 2, "BOMBEROS",  28.7, 114800,   400000),
    (2026, 2, "EMAI-EP",   38.5, 192500,   500000),
    (2026, 2, "PATRONATO", 19.4,  58200,   300000),
    (2026, 3, "GAD",       18.2, 182000,  1000000),
    (2026, 3, "BOMBEROS",  35.8, 143200,   400000),
    (2026, 3, "EMAI-EP",   44.1, 220500,   500000),
    (2026, 3, "PATRONATO", 28.3,  84900,   300000),
]

_ALERTS = [
    # (detected_at, period_year, period_month, entidad, tipo, status, severidad,
    #  titulo, detalle, accion, valor, estado,
    #  resolucion, owner_actual, escalada, nivel_escalamiento)
    (
        "2026-01-18T08:30:00", 2026, 1, "GAD", "ejecucion", "error", "CRITICA",
        "Ejecución de inversión crítica — GAD Enero 2026",
        "La Tasa de Inversión del GAD Municipal se ubica en 8.5%, muy por debajo del umbral mínimo institucional del 15%.",
        "Iniciar proceso de reforma presupuestaria urgente y certificar partidas comprometidas.",
        8.5, "archivada",
        "Se realizó reforma presupuestaria con Resolución Administrativa N° 045-2026-GAD. Se certificaron partidas por $185.000 en obras de infraestructura vial. Ejecutado conforme al Plan Anual de Inversiones.",
        "Econ. Javier Mendoza", 0, "director",
    ),
    (
        "2026-01-20T09:15:00", 2026, 1, "BOMBEROS", "ejecucion", "warning", "ADVERTENCIA",
        "Ejecución de inversión baja — Bomberos Enero 2026",
        "La Tasa de Inversión del Cuerpo de Bomberos es del 22.3%, por debajo del umbral verde del 35%.",
        "Revisar procesos de contratación y acelerar desembolsos comprometidos.",
        22.3, "en_revision",
        None,
        "Lic. Carmen Suárez", 0, "analista",
    ),
    (
        "2026-01-22T10:00:00", 2026, 1, "EMAI-EP", "cobertura", "warning", "ADVERTENCIA",
        "Documentación presupuestaria pendiente — EMAI-EP Enero 2026",
        "La Empresa Municipal de Aseo Integral no subió la cédula presupuestaria de enero en la fecha establecida.",
        "Solicitar a la Dirección Financiera de EMAI-EP subir la cédula en el plazo de 48 horas.",
        None, "validada",
        "Cédula presupuestaria de enero subida el 24/01/2026 por el Ing. Roberto Paz. Se verificó integridad del documento. Resolución institucional completada.",
        "Ing. Roberto Paz", 0, "analista",
    ),
    (
        "2026-01-25T11:00:00", 2026, 1, "PATRONATO", "ejecucion", "error", "CRITICA",
        "Ejecución de inversión crítica — Patronato Enero 2026",
        "El Patronato Municipal registra una Tasa de Inversión del 12.1%, que no alcanza el umbral mínimo del 15%.",
        "Convocar reunión urgente con la Presidenta del Patronato y la Dirección Financiera.",
        12.1, "pendiente",
        None,
        None, 0, None,
    ),
    (
        "2026-02-17T08:45:00", 2026, 2, "GAD", "cobertura", "warning", "ADVERTENCIA",
        "Retraso en entrega documental — GAD Febrero 2026",
        "La cédula presupuestaria del GAD Municipal de febrero se recibió fuera del plazo institucional de 10 días hábiles.",
        "Registrar el incumplimiento en la bitácora y solicitar informe de justificación al Departamento de Presupuesto.",
        None, "resuelta",
        "Se recibió informe de justificación del Director Financiero. El retraso se debió a migración de sistema ESIGEF. Se registró en la bitácora institucional. Resolución aceptada.",
        "Dr. Luis Torres", 0, "director",
    ),
    (
        "2026-02-19T09:30:00", 2026, 2, "BOMBEROS", "cobertura", "warning", "ADVERTENCIA",
        "Documentación presupuestaria pendiente — Bomberos Febrero 2026",
        "El Cuerpo de Bomberos no presentó la cédula presupuestaria de febrero en el sistema.",
        "Contactar al Comandante del Cuerpo de Bomberos para regularizar la presentación.",
        None, "derivada",
        None,
        "Crnl. Marco Alvarado", 0, "director",
    ),
    (
        "2026-02-21T10:15:00", 2026, 2, "EMAI-EP", "ejecucion", "warning", "ADVERTENCIA",
        "Ejecución de inversión por debajo del umbral — EMAI-EP Febrero 2026",
        "La Tasa de Inversión de EMAI-EP en febrero es del 38.5%, cayendo respecto al mes anterior.",
        "Verificar el estado de contratos vigentes y solicitar informe de ejecución parcial.",
        38.5, "observada",
        "La Dirección de EMAI-EP presentó informe de ejecución. Sin embargo, no se adjuntaron los contratos vigentes requeridos. Resolución insuficiente — devuelta para complementación.",
        "Ing. Patricia Vera", 0, "analista",
    ),
    (
        "2026-02-24T11:30:00", 2026, 2, "PATRONATO", "cobertura", "error", "CRITICA",
        "Documentación crítica faltante — Patronato Febrero 2026",
        "El Patronato Municipal no presentó documentación presupuestaria por segundo mes consecutivo. Reincidencia detectada.",
        "Escalar a nivel de Alcaldía para intervención directa.",
        None, "en_revision",
        None,
        "Econ. Javier Mendoza", 1, "alcalde",
    ),
    (
        "2026-03-18T08:00:00", 2026, 3, "GAD", "ejecucion", "warning", "ADVERTENCIA",
        "Ejecución de inversión en zona amarilla — GAD Marzo 2026",
        "La Tasa de Inversión del GAD en marzo es del 18.2%, dentro de la zona de advertencia (15%-35%).",
        "Monitorear la trayectoria y verificar el avance de proyectos comprometidos.",
        18.2, "pendiente",
        None,
        None, 0, None,
    ),
    (
        "2026-03-20T09:00:00", 2026, 3, "BOMBEROS", "ejecucion", "error", "CRITICA",
        "Ejecución de inversión crítica — Bomberos Marzo 2026",
        "La Tasa de Inversión del Cuerpo de Bomberos es del 35.8%. Se detectó irregularidad en partidas de equipamiento.",
        "Solicitar informe urgente al Comandante y revisar el PAC del Cuerpo de Bomberos.",
        35.8, "pendiente",
        None,
        None, 0, None,
    ),
]

_TIMELINE = [
    # alert identified by (period_year, period_month, entidad, tipo)
    # events: list of (timestamp, actor, evento, estado_desde, estado_hasta, nota, nivel)
    (2026, 1, "GAD", "ejecucion", [
        ("2026-01-18T08:30:00", "sistema",          "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-01-19T09:00:00", "Econ. Javier Mendoza", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se asignó responsable y se revisaron los contratos vigentes.", "director"),
        ("2026-01-23T14:30:00", "Econ. Javier Mendoza", "Resolución registrada",
         "en_revision", "resuelta",    "Reforma presupuestaria con Resolución N° 045-2026-GAD aprobada.", "director"),
        ("2026-01-24T10:00:00", "Dr. Luis Torres",       "Resolución validada",
         "resuelta",    "validada",    "Se verificó la Resolución y los anexos presupuestarios. Conforme.", "director"),
        ("2026-01-28T08:00:00", "Dr. Luis Torres",       "Alerta archivada — cierre institucional",
         "validada",    "archivada",   "Caso cerrado. Documentación archivada en expediente N° 2026-01-GAD.", "director"),
    ]),
    (2026, 1, "BOMBEROS", "ejecucion", [
        ("2026-01-20T09:15:00", "sistema",           "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-01-21T08:30:00", "Lic. Carmen Suárez", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se contactó a la Dirección Financiera del Cuerpo de Bomberos.", "analista"),
    ]),
    (2026, 1, "EMAI-EP", "cobertura", [
        ("2026-01-22T10:00:00", "sistema",         "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-01-22T11:00:00", "Lic. Carmen Suárez", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se notificó a EMAI-EP para regularizar la entrega.", "analista"),
        ("2026-01-25T16:00:00", "Ing. Roberto Paz",   "Resolución registrada",
         "en_revision", "resuelta",    "Cédula presupuestaria entregada y verificada.", "analista"),
        ("2026-01-27T09:00:00", "Dr. Luis Torres",    "Resolución validada",
         "resuelta",    "validada",    "Documento verificado. Integridad conforme. Caso cerrado.", "director"),
    ]),
    (2026, 2, "GAD", "cobertura", [
        ("2026-02-17T08:45:00", "sistema",          "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-02-17T10:00:00", "Dr. Luis Torres",   "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se solicitó informe de justificación al Dpto. de Presupuesto.", "director"),
        ("2026-02-19T14:00:00", "Dr. Luis Torres",   "Resolución registrada",
         "en_revision", "resuelta",    "Justificación aceptada. Retraso por migración de sistema ESIGEF.", "director"),
    ]),
    (2026, 2, "BOMBEROS", "cobertura", [
        ("2026-02-19T09:30:00", "sistema",            "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-02-19T11:00:00", "Lic. Carmen Suárez", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se contactó al Comandante del Cuerpo de Bomberos.", "analista"),
        ("2026-02-20T09:00:00", "Dr. Luis Torres",    "Alerta derivada a dirección de área",
         "en_revision", "derivada",    "Caso requiere intervención de Dirección para agilizar respuesta.", "director"),
    ]),
    (2026, 2, "EMAI-EP", "ejecucion", [
        ("2026-02-21T10:15:00", "sistema",            "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-02-22T09:00:00", "Ing. Patricia Vera", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Se revisó el estado de contratos con la Dirección de EMAI-EP.", "analista"),
        ("2026-02-26T15:00:00", "Ing. Patricia Vera", "Resolución registrada",
         "en_revision", "resuelta",    "Informe de ejecución parcial recibido.", "analista"),
        ("2026-02-27T10:00:00", "Dr. Luis Torres",    "Resolución observada — insuficiente",
         "resuelta",    "observada",   "Faltan contratos vigentes. Se devuelve para complementación.", "director"),
    ]),
    (2026, 2, "PATRONATO", "cobertura", [
        ("2026-02-24T11:30:00", "sistema",              "Alerta detectada automáticamente",
         None,          "pendiente",   None, "analista"),
        ("2026-02-24T13:00:00", "Econ. Javier Mendoza", "Alerta tomada en revisión",
         "pendiente",   "en_revision", "Segunda alerta de Patronato en 2 meses. Se requiere escalamiento.", "analista"),
        ("2026-02-25T09:00:00", "Econ. Javier Mendoza", "Alerta escalada a nivel superior",
         "en_revision",  "en_revision", "Escalado a Despacho del Alcalde por reincidencia crítica.", "alcalde"),
    ]),
]

_PATTERNS = [
    # (categoria, label_display, frecuencia, tiempo_promedio_dias, entidades_afectadas, ejemplos)
    (
        "reforma_presupuestaria",
        "Reforma Presupuestaria",
        3, 4.2,
        '["GAD", "PATRONATO"]',
        '["Resolución Administrativa N° 045-2026-GAD", "Reforma por subejecución Q1 2025"]',
    ),
    (
        "retraso_documental",
        "Retraso en Entrega Documental",
        2, 2.8,
        '["GAD", "BOMBEROS"]',
        '["Retraso por migración ESIGEF feb-2026", "Cédula entregada fuera de plazo ene-2026"]',
    ),
    (
        "certificacion_presupuestaria",
        "Certificación Presupuestaria",
        1, 6.0,
        '["EMAI-EP"]',
        '["Certificación de contratos de aseo ene-2026"]',
    ),
]


# ── Lógica de inserción ───────────────────────────────────────────────────────

def _seed(conn, verbose: bool = True) -> None:
    cur = conn.cursor()

    def log(msg: str) -> None:
        if verbose:
            print(f"  {msg}")

    # 1. document_uploads (semilla — para FK de monthly_kpis)
    log("Insertando document_uploads semilla...")
    upload_map: dict[tuple, int] = {}
    for doc_type, yr, mo, ent, fname, sha in _UPLOADS:
        cur.execute(
            """INSERT INTO document_uploads
               (document_type, period_year, period_month, entidad, file_name,
                sha256, size_bytes, uploaded_by, uploaded_at,
                validation_status, sentinel_version)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT DO NOTHING
               RETURNING id""",
            (doc_type, yr, mo, ent, fname, sha, 0, "seed_demo",
             f"{yr}-{mo:02d}-15T00:00:00", "VALIDADO", "2.9A-RC1"),
        )
        row = cur.fetchone()
        if row:
            upload_map[(yr, mo, ent)] = row["id"]
        else:
            # already existed — fetch id
            cur.execute(
                "SELECT id FROM document_uploads WHERE sha256=%s", (sha,)
            )
            existing = cur.fetchone()
            if existing:
                upload_map[(yr, mo, ent)] = existing["id"]

    conn.commit()
    log(f"  {len(upload_map)} uploads referenciados.")

    # 2. monthly_kpis
    log("Insertando monthly_kpis...")
    inserted_kpis = 0
    for yr, mo, ent, ti, dev_inv, cod_inv in _KPIS:
        uid = upload_map.get((yr, mo, ent))
        if uid is None:
            log(f"  SKIP kpi {ent} {yr}/{mo} — sin upload_id")
            continue
        cur.execute(
            """INSERT INTO monthly_kpis
               (upload_id, period_year, period_month, entidad,
                ti_mensual_pct, ti_acumulado_pct,
                devengado_inv, codificado_inv,
                devengado_total, codificado_total,
                calculated_at, sentinel_version)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (uid, yr, mo, ent, ti, ti,
             dev_inv, cod_inv, dev_inv * 2, cod_inv * 2,
             f"{yr}-{mo:02d}-18T12:00:00", "2.9A-RC1"),
        )
        inserted_kpis += 1
    conn.commit()
    log(f"  {inserted_kpis} filas de kpis insertadas.")

    # 3. alerts_history
    log("Insertando alerts_history...")
    alert_id_map: dict[tuple, int] = {}
    inserted_alerts = 0
    for row in _ALERTS:
        (det, yr, mo, ent, tipo, status, sev,
         titulo, detalle, accion, valor, estado,
         resolucion, owner, escalada, nivel) = row

        cur.execute(
            """INSERT INTO alerts_history
               (detected_at, period_year, period_month, entidad, tipo,
                status, severidad, titulo, detalle, accion, valor,
                estado, resolucion, owner_actual, escalada, nivel_escalamiento)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (period_year, period_month, entidad, tipo)
               DO UPDATE SET
                 estado=EXCLUDED.estado,
                 resolucion=EXCLUDED.resolucion,
                 owner_actual=EXCLUDED.owner_actual,
                 escalada=EXCLUDED.escalada,
                 nivel_escalamiento=EXCLUDED.nivel_escalamiento
               RETURNING id""",
            (det, yr, mo, ent, tipo, status, sev,
             titulo, detalle, accion, valor,
             estado, resolucion, owner, 1 if escalada else 0, nivel),
        )
        res = cur.fetchone()
        if res:
            alert_id_map[(yr, mo, ent, tipo)] = res["id"]
            inserted_alerts += 1

    conn.commit()
    log(f"  {inserted_alerts} alertas insertadas/actualizadas.")

    # Re-fetch IDs for alerts that already existed (ON CONFLICT doesn't always RETURN)
    for yr, mo, ent, tipo in [r[1:5] for r in _ALERTS]:
        key = (yr, mo, ent, tipo)
        if key not in alert_id_map:
            cur.execute(
                "SELECT id FROM alerts_history WHERE period_year=%s AND period_month=%s "
                "AND entidad=%s AND tipo=%s",
                (yr, mo, ent, tipo),
            )
            row = cur.fetchone()
            if row:
                alert_id_map[key] = row["id"]

    # 4. alert_timeline
    log("Insertando alert_timeline...")
    inserted_events = 0
    for yr, mo, ent, tipo, events in _TIMELINE:
        alert_id = alert_id_map.get((yr, mo, ent, tipo))
        if alert_id is None:
            log(f"  SKIP timeline {ent} {yr}/{mo} {tipo} — alerta no encontrada")
            continue
        # Delete existing timeline for this alert (idempotent reset)
        cur.execute("DELETE FROM alert_timeline WHERE alert_id=%s", (alert_id,))
        for ts, actor, evento, desde, hasta, nota, nivel in events:
            cur.execute(
                """INSERT INTO alert_timeline
                   (alert_id, timestamp, actor, evento,
                    estado_desde, estado_hasta, nota, nivel)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (alert_id, ts, actor, evento, desde, hasta, nota, nivel),
            )
            inserted_events += 1

    conn.commit()
    log(f"  {inserted_events} eventos de timeline insertados.")

    # 5. resolution_patterns
    log("Insertando resolution_patterns...")
    inserted_patterns = 0
    for cat, label, freq, dias, ents, ejemplos in _PATTERNS:
        cur.execute(
            """INSERT INTO resolution_patterns
               (categoria, label_display, frecuencia, tiempo_promedio_dias,
                entidades_afectadas, ejemplos, primera_vez, ultima_vez, updated_at)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (categoria) DO UPDATE SET
                 frecuencia=EXCLUDED.frecuencia,
                 tiempo_promedio_dias=EXCLUDED.tiempo_promedio_dias,
                 entidades_afectadas=EXCLUDED.entidades_afectadas,
                 ejemplos=EXCLUDED.ejemplos,
                 ultima_vez=EXCLUDED.ultima_vez,
                 updated_at=EXCLUDED.updated_at""",
            (cat, label, freq, dias, ents, ejemplos,
             "2026-01-18T00:00:00", "2026-03-18T00:00:00", "2026-03-20T00:00:00"),
        )
        inserted_patterns += 1
    conn.commit()
    log(f"  {inserted_patterns} patrones insertados/actualizados.")


def _reset(conn, verbose: bool = True) -> None:
    cur = conn.cursor()
    if verbose:
        print("  Eliminando datos de demostración...")

    # Borrar timeline de alertas demo
    for yr, mo, ent, tipo, _ in _TIMELINE:
        cur.execute(
            "DELETE FROM alert_timeline WHERE alert_id IN ("
            "  SELECT id FROM alerts_history "
            "  WHERE period_year=%s AND period_month=%s AND entidad=%s AND tipo=%s"
            ")",
            (yr, mo, ent, tipo),
        )

    # Borrar alertas demo
    for row in _ALERTS:
        _, yr, mo, ent, tipo, *_ = row
        cur.execute(
            "DELETE FROM alerts_history "
            "WHERE period_year=%s AND period_month=%s AND entidad=%s AND tipo=%s",
            (yr, mo, ent, tipo),
        )

    # Borrar kpis demo
    for yr, mo, ent, *_ in _KPIS:
        cur.execute(
            "DELETE FROM monthly_kpis "
            "WHERE period_year=%s AND period_month=%s AND entidad=%s "
            "  AND sentinel_version='2.9A-RC1'",
            (yr, mo, ent),
        )

    # Borrar uploads semilla
    for *_, sha in _UPLOADS:
        cur.execute("DELETE FROM document_uploads WHERE sha256=%s", (sha,))

    # Borrar patrones demo
    for cat, *_ in _PATTERNS:
        cur.execute("DELETE FROM resolution_patterns WHERE categoria=%s", (cat,))

    conn.commit()
    if verbose:
        print("  Reset completo.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Sembrador de datos de demostración QUIRA OS")
    parser.add_argument("--reset", action="store_true",
                        help="Eliminar datos de demo existentes antes de reinsertar")
    parser.add_argument("--only-reset", action="store_true",
                        help="Solo eliminar datos de demo, sin reinsertar")
    args = parser.parse_args()

    print("QUIRA OS — Sembrador de Datos Demo (RC-1.C)")
    print("Conectando a Supabase...")
    try:
        conn = _connect()
    except Exception as e:
        sys.exit(f"Error de conexión: {e}")
    print("Conexión establecida.")

    if args.reset or args.only_reset:
        print("\nReset de datos demo...")
        _reset(conn)

    if not args.only_reset:
        print("\nInsertando datos demo...")
        _seed(conn)

    conn.close()
    print("\nSembrador completado.")


if __name__ == "__main__":
    main()
