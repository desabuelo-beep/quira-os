# -*- coding: utf-8 -*-
"""
bulk_ingest_2025.py
Ingesta masiva de cédulas presupuestarias 2025 — Holding Municipal Montecristi

Procesa 35 archivos disponibles (de 48 totales):
  BOMBEROS  : 12/12 completo
  EMAI-EP   : 11/12 (falta Marzo — no disponible en LOTAIP)
  GAD       : 3/12  (solo Oct-Dic — los 9 restantes pendientes de obtener)
  PATRONATO : 9/12  (Ene=PDF, Mayo=Metadatos, Dic=Auditoría → omitidos)

Fuente: C:\\...\\Presupuesto 2025\\ (LOTAIP eSIGEF descargado)
Destino: Supabase PostgreSQL (modo producción, misma DB que QUIRA OS)

Idempotente: re-ejecutar no duplica — G4 (SHA256) omite ya ingestados.
Auditable:  imprime tabla de resultados con Ti% por mes/entidad.

Dylus Lab © 2026
"""
import sys
import os

try:
    from config import DATOS_DIR as _DATOS
except Exception:                                        # noqa: BLE001
    import os as _os
    from pathlib import Path as _P
    _DATOS = _P(_os.environ.get("QUIRA_DATOS", "."))

# ── Path setup — apunta al root del proyecto QUIRA OS ─────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── Parchear st.secrets para ejecutar fuera de Streamlit ──────────────────────
import toml
_secrets_path = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml")
_raw_secrets  = toml.load(_secrets_path)

import streamlit as st
class _FakeSecrets:
    def get(self, k, d=None): return _raw_secrets.get(k, d)
    def __getitem__(self, k): return _raw_secrets[k]
st.secrets = _FakeSecrets()

# ── Imports QUIRA OS ──────────────────────────────────────────────────────────
from sentinel.cedula_parser import parse_cedula
from sentinel.db_ops        import ingest_cedula, get_existing_hashes

# ── CONSTANTES ────────────────────────────────────────────────────────────────
BASE = (
    str(_DATOS / "Obsidian" / "GAD Montecritis" / "Holding Municipal MOntecristi" / "Presupuesto 2025")
)

MESES_NUM = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}

# ── MANIFIESTO EXPLÍCITO ──────────────────────────────────────────────────────
# Mapeo directo: (entidad, año, mes) → archivo relativo al BASE.
# Solo incluye archivos que son cédulas presupuestarias válidas.
# Archivos excluidos explícitamente con la razón:
#   PATRONATO Enero  → PDF (no Excel)
#   PATRONATO Mayo   → Metadatos institucionales (7 filas, sin partidas)
#   PATRONATO Dic    → Informe de auditoría Contraloría (no cédula presupuestaria)
#   EMAI-EP Marzo    → No disponible en LOTAIP
#   GAD Ene-Sep      → No disponibles (pendientes de obtener)

MANIFEST = [
    # ── BOMBEROS (12/12) ──────────────────────────────────────────────────────
    ("BOMBEROS", 2025,  1, r"BOmberos\2025-Enero-Numeral 6-6-Conjuntodedatos-Enero-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  2, r"BOmberos\2025-Febrero-Numeral 6-6-Conjuntodedatos-Febrero-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  3, r"BOmberos\2025-Marzo-Numeral 6-6-Conjuntodedatos-Marzo-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  4, r"BOmberos\2025-Abril-Numeral 6-6-Conjuntodedatos-Abril-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  5, r"BOmberos\2025-Mayo-Numeral 6-6-Conjuntodedatos-Mayo-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  6, r"BOmberos\2025-Junio-Numeral 6-6-Conjuntodedatos-Junio-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  7, r"BOmberos\2025-Julio-Numeral 6-6-Conjuntodedatos-Julio-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  8, r"BOmberos\2025-Agosto-Numeral 6-6-Conjuntodedatos-Agosto-2025.csv.xlsx"),
    ("BOMBEROS", 2025,  9, r"BOmberos\2025-Septiembre-Numeral 6-6-Conjuntodedatos-Septiembre-2025.csv.xlsx"),
    ("BOMBEROS", 2025, 10, r"BOmberos\2025-Octubre-Numeral 6-6-Conjuntodedatos-Octubre-2025-1.csv.xlsx"),
    ("BOMBEROS", 2025, 11, r"BOmberos\2025-Noviembre-Numeral 6-6-Conjuntodedatos-Noviembre-2025.csv.xlsx"),
    ("BOMBEROS", 2025, 12, r"BOmberos\2025-Diciembre-Numeral 6-6-Conjuntodedatos-Diciembre-2025.csv.xlsx"),

    # ── EMAI-EP / EP Aseo (11/12 — falta Marzo) ──────────────────────────────
    ("EMAI-EP", 2025,  1, r"EP Aseo\2025-Enero-Numeral 6-Numeral 6- Conjunto de datos.csv.xlsx"),
    ("EMAI-EP", 2025,  2, r"EP Aseo\2025-Febrero-Numeral 6-Numeral 6- Conjunto de datos FEBRERO.csv.xlsx"),
    # Marzo no disponible — omitido intencionalmente
    ("EMAI-EP", 2025,  4, r"EP Aseo\2025-Abril-Numeral 6-Numeral 6- Conjunto de datos ABRIL.csv.xlsx"),
    ("EMAI-EP", 2025,  5, r"EP Aseo\2025-Mayo-Numeral 6-Numeral 6- Conjunto de datos MAYO.csv.xlsx"),
    ("EMAI-EP", 2025,  6, r"EP Aseo\2025-Junio-Numeral 6-Numeral 6- Conjunto de datos JUNIO.csv.xlsx"),
    ("EMAI-EP", 2025,  7, r"EP Aseo\2025-Julio-Numeral 6-Numeral 6- Conjunto de datos JULIO.csv.xlsx"),
    ("EMAI-EP", 2025,  8, r"EP Aseo\2025-Agosto-Numeral 6-Numeral 6- Conjunto de datos AGOSTO.csv.xlsx"),
    ("EMAI-EP", 2025,  9, r"EP Aseo\2025-Septiembre-Numeral 6-Numeral 6- Conjunto de datos.csv.xlsx"),
    ("EMAI-EP", 2025, 10, r"EP Aseo\2025-Octubre-Numeral 6-Numeral 6- Conjunto de datos.csv.xlsx"),
    ("EMAI-EP", 2025, 11, r"EP Aseo\2025-Noviembre-Numeral 6-Numeral 6- Conjunto de datos.csv.xlsx"),
    ("EMAI-EP", 2025, 12, r"EP Aseo\2025-Diciembre-Numeral 6-Numeral 6- Conjunto de datos Dic.csv.xlsx"),

    # ── GAD Montecristi (3/12 — solo Oct-Dic disponibles) ────────────────────
    # Ene-Sep: no disponibles — pendientes de gestionar ante el GAD
    ("GAD", 2025, 10, r"GAD Montecristi\2025-Octubre-Numeral 6-6. Conjunto de datos.csv.xlsx"),
    ("GAD", 2025, 11, r"GAD Montecristi\2025-Noviembre-Numeral 6-6. Conjunto de datos_nov.csv.xlsx"),
    ("GAD", 2025, 12, r"GAD Montecristi\2025-Diciembre-Numeral 6-6. Conjunto de datos_nov.csv.xlsx"),

    # ── PATRONATO (9/12) ──────────────────────────────────────────────────────
    # Enero:  PDF — sin estructura Excel procesable
    # Mayo:   Metadatos institucionales — no es cédula presupuestaria
    # Diciembre: Informe de auditoría Contraloría — no es cédula presupuestaria
    ("PATRONATO", 2025,  2, r"Patronato\2025-Febrero-Numeral 6-CONJUNTO DE DATOS .csv.xlsx"),
    ("PATRONATO", 2025,  3, r"Patronato\2025-Marzo-Numeral 6-CONJUNTO DE DATOS.csv.xlsx"),
    ("PATRONATO", 2025,  4, r"Patronato\2025-Abril-Numeral 6-CONJUNTO DE DATOS (9).csv.xlsx"),
    ("PATRONATO", 2025,  6, r"Patronato\2025-Junio-Numeral 6-CONJUNTO DE DATOS PRUEBA 15.07.2025.csv.xlsx"),
    ("PATRONATO", 2025,  7, r"Patronato\2025-Julio-Numeral 6-CONJUNTO DE DATOS.csv.xlsx"),
    # Agosto: 2 archivos — usar el sin sufijo "(1)"
    ("PATRONATO", 2025,  8, r"Patronato\2025-Agosto-Numeral 6-CONJUNTO DE DATOS.csv.xlsx"),
    ("PATRONATO", 2025,  9, r"Patronato\2025-Septiembre-Numeral 6-2025-9-Numeral 6-CONJUNTO DE DATOS .csv (1).csv.xlsx"),
    ("PATRONATO", 2025, 10, r"Patronato\2025-Octubre-Numeral 6-CONJUNTO DE DATOS.csv.xlsx"),
    ("PATRONATO", 2025, 11, r"Patronato\2025-Noviembre-Numeral 6-CONJUNTO DE DATOS.csv.xlsx"),
]

MESES_ES = {
    1:"Ene", 2:"Feb", 3:"Mar", 4:"Abr", 5:"May", 6:"Jun",
    7:"Jul", 8:"Ago", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic",
}


# ── PIPELINE ──────────────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print("  QUIRA OS — Ingesta Masiva Historico 2025")
    print(f"  Total archivos en manifiesto: {len(MANIFEST)}")
    print("=" * 65)

    # Obtener hashes ya en DB para detectar duplicados (G4)
    print("\n[1/3] Cargando hashes existentes de Supabase...")
    existing_hashes = get_existing_hashes()
    print(f"      {len(existing_hashes)} cedulas ya registradas en la DB.")

    # Procesar cada archivo
    print("\n[2/3] Procesando cedulas...\n")
    results = []
    ok_count    = 0
    skip_count  = 0
    error_count = 0

    for entidad, year, month, rel_path in MANIFEST:
        filepath = os.path.join(BASE, rel_path)
        fname    = os.path.basename(filepath)
        mes_lbl  = MESES_ES.get(month, str(month))
        tag      = f"{entidad:10s} {year}-{mes_lbl}"

        # Verificar que el archivo existe
        if not os.path.exists(filepath):
            print(f"  [MISSING] {tag}  — archivo no encontrado")
            print(f"             {rel_path}")
            results.append((tag, "MISSING", 0.0, ""))
            error_count += 1
            continue

        # Leer bytes
        with open(filepath, "rb") as f:
            content = f.read()

        # Parsear
        result = parse_cedula(content, year, month,
                              existing_hashes=existing_hashes,
                              existing_periods=[])  # no bloquear por período

        # G4: duplicado por hash
        if not result.ok and any(
            v.guardrail == "G4" and not v.passed
            for v in result.validations
        ):
            print(f"  [SKIP-DUP] {tag}  (SHA256 ya registrado)")
            results.append((tag, "DUP", 0.0, result.sha256[:12]))
            skip_count += 1
            continue

        # Error de parsing no recuperable
        if not result.ok:
            print(f"  [ERROR]    {tag}  — {result.error}")
            results.append((tag, "ERROR", 0.0, result.error[:50]))
            error_count += 1
            continue

        # Ingestar
        ir = ingest_cedula(
            result,
            year, month,
            fname,
            uploaded_by="bulk_ingest_2025",
            notes=f"Ingesta masiva historico 2025 — {entidad}",
            entidad=entidad,
        )

        if ir["ok"]:
            ti = ir["ti_mensual_pct"]
            # Semaforo Ti
            sem = "ROJO" if ti < 15 else ("AMARILLO" if ti < 35 else "VERDE")
            print(f"  [OK]       {tag}  Ti={ti:6.2f}%  [{sem}]"
                  f"  lines={result.total_rows}  id={ir['upload_id']}")
            results.append((tag, "OK", ti, sem))
            # Añadir hash para no procesar duplicados en este mismo batch
            existing_hashes.append(result.sha256)
            ok_count += 1
        else:
            print(f"  [FAIL]     {tag}  — {ir.get('error','?')}")
            results.append((tag, "FAIL", 0.0, ""))
            error_count += 1

    # ── RESUMEN FINAL ─────────────────────────────────────────────────────────
    print("\n[3/3] Resumen de ingesta:")
    print(f"  Procesadas correctamente : {ok_count}")
    print(f"  Omitidas (duplicado)     : {skip_count}")
    print(f"  Errores/faltantes        : {error_count}")
    print(f"  Total                    : {len(MANIFEST)}")
    print()

    # Tabla de Ti por entidad/mes
    print("  Ti por entidad y mes (% inversion devengado/codificado):")
    print("  " + "-" * 61)
    print(f"  {'Entidad-Mes':20s}  {'Ti%':>6}  {'Semaforo':10s}  {'Estado':8s}")
    print("  " + "-" * 61)
    for tag, estado, ti, extra in results:
        ti_str = f"{ti:.2f}%" if estado == "OK" else "–"
        sem    = extra if estado == "OK" else ""
        print(f"  {tag:20s}  {ti_str:>6}  {sem:10s}  {estado}")
    print("  " + "-" * 61)

    # Cobertura por entidad
    print()
    print("  Cobertura por entidad:")
    for ent in ["BOMBEROS", "EMAI-EP", "GAD", "PATRONATO"]:
        ent_ok = sum(1 for t, e, _, __ in results if t.startswith(ent) and e == "OK")
        ent_tot = sum(1 for t, _, __, ___ in results if t.startswith(ent))
        print(f"    {ent:10s}: {ent_ok}/{ent_tot} meses ingestados")
    print()
    print("=" * 65)
    print("  Ingesta completada. Datos disponibles en Supabase.")
    print("=" * 65)


if __name__ == "__main__":
    main()
