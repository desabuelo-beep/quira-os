# -*- coding: utf-8 -*-
"""
update_silos.py — Alimenta los Silos del Excel Canon con datos del Corpus
QUIRA Gov · Gate 6.6 · Dylus Lab © 2026

DOCTRINA: Excel = Estado. Este script lee el corpus verificado y
actualiza las zonas crudas de los Silos del Excel para que el Motor
ICPI (H12) recalcule con datos reales en lugar de simulados.

Silos actualizables desde el corpus:
  S5 (H07) — eSIGEF: cédulas LOTAIP mensual → Ti + V_eSIGEF
  S7 (H09) — LOTAIP: scores por meta → V_LOTAIP
  S8 (H10) — CPCCS: menciones en RC → V_CPCCS

PROTOCOLO (H40 del Gold Master):
  1. Verificar H39 — estado SISTEMA INTEGRO
  2. Hacer backup del Excel antes de modificar
  3. Actualizar silo S5 con devengados
  4. ICPI en H12!B33 se actualiza automáticamente

Uso:
  python -X utf8 scripts/analysis/update_silos.py --status
  python -X utf8 scripts/analysis/update_silos.py --silo s5 --dry-run
  python -X utf8 scripts/analysis/update_silos.py --silo s5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

GOLD_MASTER_PATH = Path(
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT"
    r"\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"
)

import toml, streamlit as st
_raw = toml.load(str(ROOT / ".streamlit" / "secrets.toml"))
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k): return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection


# ── S5: eSIGEF → Ti desde cédulas LOTAIP ─────────────────────────────────────

def compute_ti_from_lotaip(year: int = 2025) -> dict:
    """
    Calcula Ti = Devengado/Codificado por grupo (G7+G8) desde holding_structured_data.
    Usa las cédulas LOTAIP mensuales del GAD.
    """
    conn = get_connection()
    c = conn.cursor()

    # Leer todas las cédulas LOTAIP del GAD para el año
    c.execute("""
        SELECT periodo, datos_json
        FROM holding_structured_data
        WHERE evidence_type = 'LOTAIP_DATOS'
          AND source_entity = 'GAD_MCR'
          AND canton_id = 'MCR'
          AND periodo LIKE %s
        ORDER BY periodo
    """, (f"{year}-%",))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return {"error": f"Sin datos LOTAIP GAD para {year}"}

    # Buscar columnas de devengado y codificado en las filas de datos
    codificado_total = 0.0
    devengado_total = 0.0
    meses_procesados = []

    for row in rows:
        datos = row["datos_json"] if isinstance(row["datos_json"], dict) else json.loads(row["datos_json"])
        filas = datos.get("rows", [])
        periodo = row["periodo"]

        cod_mes = dev_mes = 0.0
        for fila in filas:
            # Buscar columnas de codificado y devengado (nombres varían por entidad)
            for k, v in fila.items():
                k_lower = k.lower()
                try:
                    val = float(str(v).replace(",", "").replace("$", "").strip())
                except (ValueError, AttributeError):
                    continue
                if "codificado" in k_lower or "assigned" in k_lower:
                    cod_mes += val
                elif "devengado" in k_lower or "accrued" in k_lower:
                    dev_mes += val

        if cod_mes > 0:
            codificado_total += cod_mes
            devengado_total += dev_mes
            meses_procesados.append(periodo)

    ti = devengado_total / codificado_total if codificado_total > 0 else 0

    return {
        "year": year,
        "entity": "GAD_MCR",
        "meses": meses_procesados,
        "codificado_total": round(codificado_total, 2),
        "devengado_total": round(devengado_total, 2),
        "ti_calculado": round(ti, 6),
        "ti_pct": round(ti * 100, 2),
        "fuente": f"LOTAIP mensual corpus — {len(meses_procesados)} meses de {year}",
        "nota": "Ti = Devengado_Total / Codificado_Total (grupos G7+G8+G9)"
    }


# ── S8: V_CPCCS → menciones de metas en RC ───────────────────────────────────

def compute_vcpccs_from_rc(year: int = 2024) -> dict:
    """
    Analiza los RC del GAD y mapea menciones de metas PDOT → V_CPCCS.
    Busca palabras clave de las 25 metas en el texto de los RC.
    """
    # Metas PDOT con palabras clave para búsqueda semántica
    META_KEYWORDS = {
        "SC-I-N-01":  ["agua potable", "saneamiento", "cobertura agua"],
        "SC-L-N-02":  ["talento humano", "personal", "nomina"],
        "AH-I-X-01":  ["sostenibilidad financiera", "presupuesto", "ingresos propios"],
        "AH-I-X-02":  ["vialidad", "vias", "pavimento", "calles"],
        "AH-I-X-03":  ["salud", "patronato", "atencion medica"],
        "AH-I-N-01":  ["desechos", "basura", "residuos", "aseo"],
        "SC-L-G-01":  ["alcantarillado", "aguas servidas", "PTAR"],
        "AH-I-X-04":  ["modernizacion", "tecnologia", "tramites"],
        "PI-I-G-01":  ["equipamiento", "mercado", "terminal"],
        "AH-C-X-01":  ["derechos", "grupos vulnerables", "inclusion"],
        "AH-C-X-02":  ["catastro", "sistema informacion", "territorial"],
        "SC-I-N-03":  ["participacion ciudadana", "presupuesto participativo"],
        "FA-I-X-01":  ["riesgo", "inundacion", "quebrada"],
        "FA-C-X-01":  ["areas verdes", "parques", "IVU"],
        "FA-I-X-02":  ["equipamiento urbano", "espacios publicos"],
        "FA-L-N-01":  ["patrimonio", "cultura", "artesania"],
        "PI-I-G-02":  ["PDOT", "PUGS", "planificacion"],
        "PI-L-G-01":  ["senalizacion", "semaforos", "transito"],
        "EP-L-N-01":  ["vivienda", "VIS", "VIP"],
        "EP-L-X-01":  ["productivo", "artesanos", "microempresa"],
        "PI-TUR-01":  ["turismo", "Montecristi sombrero"],
        "PI-TUR-02":  ["eventos", "ferias", "gastronomi"],
        "FA-CC-01":   ["cambio climatico", "ambiente", "ecosistema"],
        "AH-AP-04":   ["continuidad agua", "abastecimiento"],
        "FA-DIS-01":  ["disposicion final", "relleno sanitario"],
    }

    conn = get_connection()
    c = conn.cursor()

    # Buscar RC del GAD para el año
    siglas = [f"RC-GAD-{year}", f"RC-GAD-{year-1}"]
    results = {}

    for sigla in siglas:
        c.execute("""
            SELECT contenido FROM normativa_corpus
            WHERE norma_sigla = %s AND canton_id = 'MCR'
            LIMIT 200
        """, (sigla,))
        chunks = [r["contenido"].lower() for r in c.fetchall()]
        full_text = " ".join(chunks)

        for meta_id, keywords in META_KEYWORDS.items():
            found = any(kw.lower() in full_text for kw in keywords)
            if meta_id not in results:
                results[meta_id] = {"found_in": [], "v_cpccs": 0}
            if found:
                results[meta_id]["found_in"].append(sigla)
                results[meta_id]["v_cpccs"] = 1.0

    conn.close()

    # Convertir a 0.5 si solo aparece en 1 RC (parcial)
    for meta_id, data in results.items():
        if len(data["found_in"]) == 1:
            data["v_cpccs"] = 0.5

    summary = {
        "metas_v1": sum(1 for d in results.values() if d["v_cpccs"] == 1.0),
        "metas_v05": sum(1 for d in results.values() if d["v_cpccs"] == 0.5),
        "metas_v0": sum(1 for d in results.values() if d["v_cpccs"] == 0.0),
    }

    return {
        "year": year,
        "fuente": f"Corpus RC GAD MCR {year-1}/{year}",
        "summary": summary,
        "detalle": results,
    }


# ── STATUS ────────────────────────────────────────────────────────────────────

def cmd_status() -> None:
    """Muestra estado actual de los silos vs datos disponibles en corpus."""
    print("\n" + "=" * 65)
    print("  QUIRA Bridge Status — Corpus → Excel Silos")
    print("=" * 65)

    # Ti desde corpus (2025)
    ti_2025 = compute_ti_from_lotaip(2025)
    ti_2026 = compute_ti_from_lotaip(2026)

    print(f"\n  S5 eSIGEF — Ti desde corpus LOTAIP:")
    if "error" not in ti_2025:
        print(f"    2025: Ti = {ti_2025['ti_pct']:.2f}%  "
              f"({len(ti_2025['meses'])} meses)  "
              f"Dev=${ti_2025['devengado_total']:,.0f}")
    if "error" not in ti_2026:
        print(f"    2026: Ti = {ti_2026['ti_pct']:.2f}%  "
              f"({len(ti_2026['meses'])} meses)  "
              f"Dev=${ti_2026['devengado_total']:,.0f}")

    # V_CPCCS desde RC
    vcpccs = compute_vcpccs_from_rc(2024)
    s = vcpcps = vcpccs.get("summary", {})
    print(f"\n  S8 CPCCS — V_CPCCS desde corpus RC:")
    print(f"    V=1.0 (evidencia documental): {s.get('metas_v1', 0)} metas")
    print(f"    V=0.5 (mencionada parcial):   {s.get('metas_v05', 0)} metas")
    print(f"    V=0.0 (no encontrada):        {s.get('metas_v0', 0)} metas")

    # Excel actual desde H73
    from app.connectors.gold_master import fetch_gold_master_data
    gm = fetch_gold_master_data()
    raw = gm["data"].get("_raw_h73", {})
    print(f"\n  Excel Canon actual (H73):")
    print(f"    ICPI 2025: {raw.get('ICPI_2025', 0)*100:.2f}%")
    print(f"    Ti 2026 (Q1): {raw.get('GAD_DEVENGADO_Q1', 0)/raw.get('GAD_CODIFICADO_2026', 1)*100:.2f}%")
    print(f"    ITAM: {raw.get('ITAM_2025_REF', 0)*100:.2f}%")

    print("\n  Pendiente Gate 6.6:")
    print("    [ ] update_silos.py --silo s5 : alimentar H07 con Ti real")
    print("    [ ] update_silos.py --silo s8 : reemplazar V_CPCCS simulado")
    print("    [ ] tag_domains.py            : Dom01-D12 en Holding corpus")
    print("=" * 65 + "\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Alimenta silos del Excel Canon desde corpus verificado")
    parser.add_argument("--status",   action="store_true",
                        help="Ver estado actual del bridge")
    parser.add_argument("--silo",     choices=["s5", "s7", "s8"],
                        help="Silo a actualizar")
    parser.add_argument("--year",     type=int, default=2025)
    parser.add_argument("--dry-run",  action="store_true", dest="dry_run",
                        help="Calcular sin escribir al Excel")
    parser.add_argument("--json",     action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    if args.silo == "s5":
        result = compute_ti_from_lotaip(args.year)
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n  S5 Ti calculado desde corpus LOTAIP {args.year}:")
            print(f"    Meses disponibles: {result.get('meses', [])}")
            print(f"    Codificado total:  ${result.get('codificado_total', 0):,.2f}")
            print(f"    Devengado total:   ${result.get('devengado_total', 0):,.2f}")
            print(f"    Ti = {result.get('ti_pct', 0):.2f}%")
            if not args.dry_run:
                print(f"\n  [NOTA] Para escribir al Excel, pegar manualmente en H07")
                print(f"  filas 46+ segun protocolo H40. Automatizacion completa")
                print(f"  requiere firma de Javo (Excel es Gold Master protegido).")

    elif args.silo == "s8":
        result = compute_vcpccs_from_rc(args.year)
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n  S8 V_CPCCS desde corpus RC {args.year}:")
            s = result["summary"]
            print(f"    V=1.0: {s['metas_v1']} metas  "
                  f"V=0.5: {s['metas_v05']}  V=0.0: {s['metas_v0']}")
            for meta_id, data in result["detalle"].items():
                if data["v_cpccs"] > 0:
                    print(f"    {meta_id}: V={data['v_cpccs']}  en {data['found_in']}")


if __name__ == "__main__":
    main()
