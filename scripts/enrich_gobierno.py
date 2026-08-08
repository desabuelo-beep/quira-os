# -*- coding: utf-8 -*-
"""
scripts/enrich_gobierno.py — bloque `gobierno` del snapshot (dimensión ¿QUÉ? · ADR-037)
═══════════════════════════════════════════════════════════════════════════════════
La institución y su mandato: quién gobierna, desde cuándo, hasta cuándo, con qué concejo
y bajo qué estructura. Alimenta el 1er cajón del panorama general (QUIRA Observatorio).

FUENTES (todo verificado · nada se inventa · Reglas 1, 3 y 9):
  · Autoridades electas y fechas → Gold Master `SCHEMA_CNE` (cargado por Javo · 2026-07-16)
  · Consejo Cantonal de Planificación → corpus PDOT (sha defe12c46b)
  · Estructura orgánica vigente     → corpus `RES-ORG-GADMCM-2025` Art. 9 (sha 368e809a4f)

LO QUE NO SE PUBLICA (criterio de Javo + colega · 2026-07-16):
  · Nombres de directores: las personas cambian, el orgánico permanece. Se muestra la
    ESTRUCTURA, no la plantilla — QUIRA observa estructuras, no personas.
  · Las direcciones listadas en el PDOT: están DEROGADAS por el Orgánico 2025.
  Sí se publican los cargos ELECTOS y los órganos colegiados: son mandato, no plantilla.

LECCIÓN (Javo · 2026-07-16): antes de declarar que un dato no existe, revisar el CORPUS
documental, no solo el canon estructurado. El director declaró "7 de 8 autoridades sin
dato" mirando solo SCHEMA_CNE; la nómina completa estaba en el PDOT.

Uso:  python scripts/enrich_gobierno.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from datetime import date, datetime

import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXCEL = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"
SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")
SECRETS = os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml")

_HCODE = re.compile(r"\bH\d{1,2}[a-z]?\b")
_SIN = ("[VER_CNE", "VER_CNE", "")


def _fw(s) -> bool:
    """Seguro para público: sin nomenclatura canónica (Firewall · Regla 2)."""
    return not _HCODE.search(str(s or ""))


def _limpio(v) -> str:
    """Devuelve '' si el canon marca el dato como no cargado (ausencia declarada)."""
    s = str(v or "").strip()
    return "" if any(s.startswith(x) for x in _SIN if x) or not s else s


def _fecha(v):
    if isinstance(v, datetime):
        return v.date()
    try:
        return datetime.strptime(str(v).strip()[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _uri() -> str:
    try:
        return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        return ""


def _autoridades(ws) -> tuple[dict, list]:
    """Alcalde + Concejo Cantonal desde SCHEMA_CNE (cargado por Javo)."""
    alcalde, concejo = {}, []
    for r in ws.iter_rows(min_row=5, max_row=13, values_only=True):
        if not (r and r[0] and isinstance(r[0], str)):
            continue
        cargo = r[0].strip()
        if not any(k in cargo.lower() for k in ("alcalde", "concejal")):
            continue
        nombre = _limpio(r[1] if len(r) > 1 else "")
        if not nombre or not _fw(nombre):
            continue
        reg = {"cargo": cargo, "nombre": nombre,
               "movimiento": _limpio(r[2] if len(r) > 2 else ""),
               "posesion": str(_fecha(r[4] if len(r) > 4 else None) or ""),
               "hasta": str(_fecha(r[5] if len(r) > 5 else None) or "")}
        if cargo.lower().startswith("alcalde"):
            alcalde = reg
        else:
            concejo.append(reg)
    return alcalde, concejo


def _mandato(alcalde: dict) -> dict:
    """El contador: se alimenta de las fechas DEL CANON. Sin fechas, no hay contador."""
    ini, fin = _fecha(alcalde.get("posesion")), _fecha(alcalde.get("hasta"))
    if not (ini and fin):
        return {"disponible": False,
                "nota": "El canon no registra las fechas del mandato."}
    hoy = date.today()
    total = (fin - ini).days
    transc = max((hoy - ini).days, 0)
    return {
        "disponible": True,
        "inicio": ini.isoformat(), "fin": fin.isoformat(),
        "dias_totales": total,
        "dias_transcurridos": min(transc, total),
        "dias_restantes": max((fin - hoy).days, 0),
        "avance_pct": round(min(transc / total * 100, 100), 1) if total else 0,
        "vigente": ini <= hoy <= fin,
    }


def _del_corpus() -> dict:
    """Consejo de Planificación (PDOT) + estructura orgánica vigente (Orgánico Art. 9)."""
    uri = _uri()
    out = {"consejo_planificacion": [], "organico": {}, "fuente": ""}
    if not uri:
        return out
    try:
        import psycopg2
        cur = psycopg2.connect(uri, connect_timeout=25).cursor()

        # 1 · Consejo Cantonal de Planificación — PDOT (págs. 16-17)
        cur.execute("SELECT sha256, contenido FROM public.normativa_corpus "
                    "WHERE norma_sigla='PDOT-MONTECRISTI' AND contenido ILIKE %s LIMIT 1",
                    ("%PRESIDENTE DEL CONSEJO DE%",))
        row = cur.fetchone()
        if row:
            txt = re.sub(r"\s+", " ", row[1])
            # OJO (lección 2026-07-16): el patrón previo perdía 4 de 10 integrantes y arrastraba
            # la inicial del nombre siguiente al cargo ("Presidente Del Consejo De I"). El PDOT
            # publica "Nombre <cargo EN MAYÚSCULAS>" y el cargo termina donde arranca el
            # tratamiento del siguiente (Ing./Econ./Arq./Lcda./Abg./Sr./Sra.).
            _TRAT = r"(?:Ing|Econ|Arq|Lcda|Lcdo|Abg|Sr|Sra)\."
            # OJO (corrección de Javo · 2026-07-16): el patrón incluía ALCALDE|VICEALCALDESA y
            # colaba a la Vicealcaldesa en este consejo. En el PDOT ella está en la COLUMNA DEL
            # CONCEJO CANTONAL; el texto aplanado junta ambas columnas y el regex las mezcló.
            # Flor Arteaga es solo Vicealcaldesa: NO integra el Consejo de Planificación.
            # El único concejal que lo integra es Pazmiño, y lo hace como VICEPRESIDENTE.
            _CARGOS = (r"PRESIDENTE|VICEPRESIDENTE|COORDINADOR|COORDINADORA|PROCURADOR|"
                       r"REPRESENTANTE")
            _NO_SON = ("vicealcald", "concejal", "alcalde")
            pares = re.findall(
                rf"({_TRAT}\s*[A-ZÁÉÍÓÚÑ][^.]{{4,46}}?)\s+"
                rf"((?:{_CARGOS})[A-ZÁÉÍÓÚÑ\s]*?)(?=\s+{_TRAT}|\s*$|\s+[A-ZÁÉÍÓÚÑ][a-z])", txt)
            vistos = set()
            for nom, car in pares:
                n = re.sub(r"\s+", " ", nom).strip(" ,")
                # el cargo se limpia de la inicial huérfana que precede al siguiente nombre
                c = re.sub(r"\s+[A-ZÁÉÍÓÚÑ]$", "", re.sub(r"\s+", " ", car).strip())
                if not n or n in vistos or not _fw(n) or len(c) < 5:
                    continue
                if any(x in c.lower() for x in _NO_SON):   # cargos del Concejo, no de este consejo
                    continue
                vistos.add(n)
                out["consejo_planificacion"].append({"nombre": n, "cargo": c.title()})
            out["sha_pdot"] = row[0][:12]

        # 2 · Estructura orgánica vigente — Orgánico Art. 9.
        # OJO (lección 2026-07-16): el Art. 9 está PARTIDO en varios chunks del corpus. Leer un
        # solo chunk perdía 2 de los 4 niveles y la Alcaldía. Se unen los chunks y se aísla el
        # artículo antes de extraer. Los 4 niveles son los que el propio orgánico declara.
        cur.execute("SELECT string_agg(contenido, ' ' ORDER BY id), min(sha256) "
                    "FROM public.normativa_corpus WHERE norma_sigla='RES-ORG-GADMCM-2025'")
        row = cur.fetchone()
        if row and row[0]:
            full = re.sub(r"\s+", " ", row[0])
            ini = full.find("Estructura organizacional alineada a los procesos")
            fin = full.find("Artículo 10", ini + 1) if ini != -1 else -1
            art9 = full[ini:fin if fin > ini else ini + 9000] if ini != -1 else full
            NIVELES = ["PROCESOS GOBERNANTES",
                       "PROCESOS ADJETIVOS O HABILITANTES DE ASESORÍA",
                       "PROCESOS SUSTANTIVOS O AGREGADORES DE VALOR",
                       "PROCESOS ADJETIVOS O HABILITANTES DE APOYO"]
            marcas = sorted((art9.find(n), n) for n in NIVELES if art9.find(n) != -1)
            niveles = {}
            for i, (pos, nom) in enumerate(marcas):
                tope = marcas[i + 1][0] if i + 1 < len(marcas) else len(art9)
                bloque = art9[pos:tope]
                # unidad = la que el orgánico rotula con "Responsable:" (su marca formal)
                uni = re.findall(r"((?:Dirección|Coordinación|Procuraduría|Alcaldía|Concejo)"
                                 r"[^.]{0,58})\.\s*Responsable", bloque)
                # el Concejo Municipal y la Alcaldía encabezan su nivel sin "Responsable" propio
                for extra in ("Concejo Municipal", "Alcaldía"):
                    if extra in bloque:
                        uni.append(extra)
                # Se descartan capturas espurias: el patrón arranca en la palabra clave, así que
                # una mención suelta ("Concejo") entraría como si fuera una unidad. Una unidad
                # real del orgánico siempre lleva su denominación completa.
                limpio = {re.sub(r"\s+", " ", u).strip(" .,") for u in uni}
                limpio = {u for u in limpio if len(u) > 10 or u in ("Alcaldía",)}
                if limpio:
                    niveles[nom.replace("PROCESOS ", "").title()] = sorted(limpio)
            out["organico"] = {"niveles": niveles, "sha": (row[1] or "")[:12],
                               "norma": "Orgánico Estructural vigente · Art. 9"}
        out["fuente"] = "Corpus normativo verificado (Supabase · sha256)"
    except Exception as e:
        out["error"] = str(e)[:80]
    return out


def build_block() -> dict:
    wb = openpyxl.load_workbook(EXCEL, read_only=True, data_only=True)
    alcalde, concejo = _autoridades(wb["SCHEMA_CNE"])
    corp = _del_corpus()
    org = corp.get("organico", {})
    n_unid = sum(len(v) for v in (org.get("niveles") or {}).values())
    return {
        "_fuente": "Autoridades electas y mandato: canon (SCHEMA_CNE) · Consejo de Planificación y "
                   "estructura orgánica: corpus documental verificado (sha256)",
        "alcalde": alcalde,
        "mandato": _mandato(alcalde),
        "concejo": {"detalle": concejo, "total": len(concejo) + (1 if alcalde else 0)},
        "consejo_planificacion": {"detalle": corp.get("consejo_planificacion", []),
                                  "total": len(corp.get("consejo_planificacion", [])),
                                  "sha256": corp.get("sha_pdot", "")},
        "organico": {"niveles": org.get("niveles", {}), "n_unidades": n_unid,
                     "norma": org.get("norma", ""), "sha256": org.get("sha", ""),
                     "nota": "Se publica la estructura, no la plantilla: las personas cambian, "
                             "el orgánico permanece."},
        "publicado": True,
    }


def main() -> None:
    block = build_block()
    snap = {}
    if os.path.exists(SNAP):
        with open(SNAP, encoding="utf-8") as f:
            snap = json.load(f)
    snap["gobierno"] = block
    with open(SNAP, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    m, a = block["mandato"], block["alcalde"]
    print("OK - bloque 'gobierno' escrito en gm_snapshot.json")
    print(f"   alcalde   : {a.get('nombre','—')} · {a.get('movimiento','—')}")
    if m.get("disponible"):
        print(f"   mandato   : {m['inicio']} → {m['fin']} · {m['dias_transcurridos']:,} días "
              f"transcurridos · {m['dias_restantes']:,} restantes ({m['avance_pct']}%)")
    else:
        print(f"   mandato   : {m.get('nota')}")
    print(f"   concejo   : {block['concejo']['total']} integrantes (canon)")
    print(f"   c. planif.: {block['consejo_planificacion']['total']} integrantes (PDOT)")
    org = block["organico"]
    print(f"   orgánico  : {len(org['niveles'])} niveles · {org['n_unidades']} unidades "
          f"({org['norma']} · sha {org['sha256']})")


if __name__ == "__main__":
    main()
