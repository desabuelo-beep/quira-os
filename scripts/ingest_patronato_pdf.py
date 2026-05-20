# -*- coding: utf-8 -*-
"""
scripts/ingest_patronato_pdf.py
Ingesta de cédulas PATRONATO 2025 en formato PDF
Ene, Mayo, Dic — extraídas con pdfplumber, convertidas a xlsx temporal.

Pipeline:
  PDF → pdfplumber → DataFrame limpio → xlsx en memoria → parse_cedula → ingest_cedula

Dylus Lab © 2026
"""
import sys, os, io, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# ── st.secrets fuera de Streamlit ─────────────────────────────────────────────
import toml
_secrets_path = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml")
_raw_secrets  = toml.load(_secrets_path)
import streamlit as st
class _FakeSecrets:
    def get(self, k, d=None): return _raw_secrets.get(k, d)
    def __getitem__(self, k):  return _raw_secrets[k]
st.secrets = _FakeSecrets()

import pdfplumber
import pandas as pd
import openpyxl
from openpyxl import Workbook

from sentinel.cedula_parser import parse_cedula
from sentinel.db_ops        import ingest_cedula, get_existing_hashes

# ── RUTAS ─────────────────────────────────────────────────────────────────────
BASE_PATRONATO = (
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Obsidian"
    r"\GAD Montecritis\Holding Municipal MOntecristi\Presupuesto 2025\Patronato"
)

MANIFEST_PDF = [
    (2025,  1, "2025-Enero-Numeral 6-CONJUNTO DE DATOS (28).csv.pdf"),
    (2025,  5, "2025-Mayo-Numeral 6-CONJUNTO DE DATOS.csv.pdf"),
    (2025, 12, "2025-Diciembre-Numeral 6-CONJUNTO DE DATOS  PRESUPUESTO.csv (1).pdf"),
]

MESES_ES = {
    1:"Ene", 2:"Feb", 3:"Mar", 4:"Abr", 5:"May", 6:"Jun",
    7:"Jul", 8:"Ago", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dic",
}

# ── LIMPIEZA DE NÚMERO ────────────────────────────────────────────────────────
_RE_NUM = re.compile(r'[\$\s\n\r]')
_RE_EUR = re.compile(r'^-?[\d\.]+,\d+$')   # formato europeo: 1.234,56

def _clean_num(val: str) -> str:
    """
    Limpia valores numéricos del PDF:
      '$ 303.192,00'  →  '303.192,00'
      '$\n303.192,00' →  '303.192,00'
    """
    if val is None:
        return ""
    v = _RE_NUM.sub("", str(val)).strip()
    return v


# ── EXTRACCIÓN PDF → DataFrame ────────────────────────────────────────────────
def extract_pdf_to_df(path: str) -> pd.DataFrame:
    """
    Extrae todas las tablas del PDF y devuelve un DataFrame limpio
    con las columnas originales de la cédula eSIGEF.
    """
    header   = None
    rows_all = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or row[0] is None:
                        continue
                    cell0 = str(row[0]).strip()
                    # Skip encabezados institucionales
                    if cell0.startswith("PATRONATO"):
                        continue
                    if cell0.startswith("2025-"):
                        continue
                    # Fila de columnas
                    if cell0 == "Cuenta":
                        if header is None:
                            header = [
                                (c or "").replace("\n", " ").strip()
                                for c in row
                            ]
                        continue
                    # Fila de datos (debe tener al menos un valor no vacío)
                    if any(c for c in row if c and str(c).strip()):
                        rows_all.append(row)

    if not header or not rows_all:
        raise ValueError("No se pudo extraer tabla de cédula del PDF")

    df = pd.DataFrame(rows_all, columns=header)

    # ── Limpiar columnas numéricas ─────────────────────────────────────────────
    numeric_cols = [
        "Asignado", "Modificado", "Codificado", "Monto certificado",
        "Comprometido", "Devengado", "Pagado",
        "Saldo por comprometer", "Saldo por devengar", "Saldo por pagar",
        "Porcentaje de ejecucion",
    ]
    # También acepta variantes con salto de línea en el header
    col_map_clean = {c.replace("\n", " ").strip(): c for c in df.columns}

    for target in numeric_cols:
        # Buscar la columna real (puede tener espacios o saltos de línea)
        real_col = None
        for col in df.columns:
            if col.replace("\n", " ").strip().lower() == target.lower():
                real_col = col
                break
        if real_col is None:
            continue
        df[real_col] = df[real_col].apply(_clean_num)

    return df


# ── DataFrame → xlsx en memoria ───────────────────────────────────────────────
def df_to_xlsx_bytes(df: pd.DataFrame, sheet_name: str = "Hoja1") -> bytes:
    """
    Convierte el DataFrame a bytes de un archivo .xlsx compatible con openpyxl.
    Los números europeos (1.234,56) se escriben como texto para que
    cedula_parser los interprete con su lógica de detección de formato.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    # Cabecera
    ws.append(list(df.columns))

    # Datos
    for _, row in df.iterrows():
        ws.append([str(v) if v is not None else "" for v in row])

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── PIPELINE PRINCIPAL ────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print("  QUIRA OS — Ingesta PATRONATO PDF (Ene, Mayo, Dic 2025)")
    print(f"  Archivos: {len(MANIFEST_PDF)}")
    print("=" * 65)

    print("\n[1/3] Cargando hashes existentes...")
    existing_hashes = get_existing_hashes()
    print(f"      {len(existing_hashes)} cedulas ya registradas.")

    print("\n[2/3] Extrayendo y procesando PDFs...\n")
    results = []

    for year, month, fname in MANIFEST_PDF:
        filepath  = os.path.join(BASE_PATRONATO, fname)
        mes_lbl   = MESES_ES.get(month, str(month))
        tag       = f"PATRONATO  {year}-{mes_lbl}"

        if not os.path.exists(filepath):
            print(f"  [MISSING]  {tag} — archivo no encontrado")
            print(f"             {fname}")
            results.append((tag, "MISSING", 0.0, ""))
            continue

        # Extraer PDF → DataFrame
        try:
            df = extract_pdf_to_df(filepath)
        except Exception as e:
            print(f"  [ERROR-PDF] {tag} — {e}")
            results.append((tag, "ERROR-PDF", 0.0, str(e)[:50]))
            continue

        print(f"  [PDF-OK]   {tag}  {len(df)} filas extraídas del PDF")

        # DataFrame → xlsx bytes
        try:
            xlsx_bytes = df_to_xlsx_bytes(df)
        except Exception as e:
            print(f"  [ERROR-XLSX] {tag} — {e}")
            results.append((tag, "ERROR-XLSX", 0.0, str(e)[:50]))
            continue

        # Parsear con pipeline estándar
        result = parse_cedula(
            xlsx_bytes, year, month,
            existing_hashes=existing_hashes,
            existing_periods=[],
        )

        # G4: duplicado
        if not result.ok and any(
            v.guardrail == "G4" and not v.passed
            for v in result.validations
        ):
            print(f"  [SKIP-DUP] {tag}  (ya registrado)")
            results.append((tag, "DUP", 0.0, result.sha256[:12]))
            continue

        # Error de parsing
        if not result.ok:
            print(f"  [ERROR]    {tag}  — {result.error}")
            # Mostrar detalles de validación
            for v in result.validations:
                if not v.passed:
                    print(f"             G{v.guardrail}: {v.message}")
            results.append((tag, "ERROR", 0.0, result.error[:50]))
            continue

        # Ingestar
        ir = ingest_cedula(
            result, year, month, fname,
            uploaded_by="bulk_ingest_pdf_2025",
            notes=f"Ingesta PDF PATRONATO 2025 — mes {month}",
            entidad="PATRONATO",
        )

        if ir["ok"]:
            ti  = ir["ti_mensual_pct"]
            sem = "ROJO" if ti < 15 else ("AMARILLO" if ti < 35 else "VERDE")
            print(f"  [OK]       {tag}  Ti={ti:6.2f}%  [{sem}]"
                  f"  lines={result.total_rows}  id={ir['upload_id']}")
            results.append((tag, "OK", ti, sem))
            existing_hashes.append(result.sha256)
        else:
            print(f"  [FAIL]     {tag}  — {ir.get('error', '?')}")
            results.append((tag, "FAIL", 0.0, ""))

    # ── RESUMEN ────────────────────────────────────────────────────────────────
    ok_count    = sum(1 for _, e, _, __ in results if e == "OK")
    skip_count  = sum(1 for _, e, _, __ in results if e == "DUP")
    error_count = sum(1 for _, e, _, __ in results if e not in ("OK", "DUP"))

    print("\n[3/3] Resumen:")
    print(f"  Ingresadas : {ok_count}")
    print(f"  Duplicadas : {skip_count}")
    print(f"  Errores    : {error_count}")
    print()
    for tag, estado, ti, extra in results:
        ti_str = f"{ti:.2f}%" if estado == "OK" else "–"
        sem    = extra if estado == "OK" else estado
        print(f"  {tag:22s}  {ti_str:>7}  {sem}")
    print()
    print("=" * 65)
    print("  Listo. PATRONATO 2025 completo 12/12.")
    print("=" * 65)


if __name__ == "__main__":
    main()
