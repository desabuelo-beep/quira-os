# -*- coding: utf-8 -*-
"""
scripts/normativa/cruce_poa_cedula.py — la cadena meta → partida → devengado
════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). `V_eSIGEF` se derivaba preguntándole al POA si la
meta estaba planificada. Esa no es la pregunta: **`V_eSIGEF` pregunta si hay
devengado certificado**. Planificar y ejecutar son cosas distintas y ninguna
prueba la otra.

La cadena real tiene dos saltos, y **cada fuente prueba sólo el suyo**:

    meta PDOT  ──POA──▶  partida  ──cédula──▶  devengado
               (planificación)      (ejecución)

CAPA DERIVADA, NO SUSTITUTIVA. Este módulo **no reescribe ninguna fuente**.
Produce un tercer archivo donde cada vínculo conserva de dónde salió —archivo,
hoja, fila, partida, período— para que cualquier `V_eSIGEF` pueda reconstruirse
hasta el documento que lo sostiene. Si mañana una partida cambia por reforma, o
una cédula mensual difiere de la de diciembre, se puede ver por qué el derivador
dijo lo que dijo.

ESTADOS, NO BINARIOS. Un `0/1` no distingue «no ejecutó» de «no encontré», y esa
confusión es la que la Regla de Oro 3 prohíbe. Por eso cada dimensión conserva su
propio estado y **`no_hallado` nunca significa `no existe`**.

ALCANCE: 2025 en adelante. El POA 2023 y 2024 no traen columnas de alineación al
PDOT (OBS-027) y por tanto no pueden acreditar nada sobre estas 66 metas.

QUÉ NO HACE: no suma, no prorratea, no imputa devengado a una meta cuando la
partida sirve a varias. Declara que no es atribuible y se detiene.

Uso:  python scripts/normativa/cruce_poa_cedula.py [--anio 2025] [--escribir]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from extraer_cedula import extraer_todo                      # noqa: E402
from extraer_poa_xlsx import extraer as extraer_poa          # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = RAIZ / "data" / "pdot" / "registro_maestro_metas.json"
SALIDA = RAIZ / "data" / "pdot" / "cruce_poa_cedula.json"

POA_POR_ANIO = {2025: "GAD Monteristi POA 2025.xlsx",
                2026: "GAD Montecristi POA 2026.xlsx"}

# El registro maestro guarda la meta recortada a 70 caracteres. Reconciliar por
# prefijo exacto normalizado NO es el emparejamiento por palabras que OBS-026
# descartó: aquí se exige que N caracteres seguidos coincidan letra a letra.
#
# 30, no 50. Con el umbral en 50 se rechazaron cuatro metas cuyo enunciado
# COMPLETO mide 33 y 41 caracteres normalizados: coincidían enteras y se
# descartaron por cortas. Un piso absoluto castiga a la meta de enunciado breve,
# que no es menos identificable — es más breve.
UMBRAL_PREFIJO = 30


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s))
                if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]", "", s)


# ══════════════════════════════════════════════════════════════════════════════
# DIMENSIÓN 1 · ARTICULACIÓN — el POA declara (o no) su vínculo con el PDOT
# ══════════════════════════════════════════════════════════════════════════════
def reconciliar_metas(filas_poa: list[dict], registro: list[dict]) -> dict[str, dict]:
    """Texto de meta del POA → meta del registro maestro, por prefijo exacto.

    Devuelve para cada texto del POA el `id` alcanzado y **cuántos caracteres
    normalizados coincidieron**, que es la medida de la evidencia. Sin ese dato
    el vínculo no sería auditable: se sabría que casó, no con qué fuerza."""
    idx = [(_norm(m["meta"]), m) for m in registro]
    fuera: dict[str, dict] = {}
    for texto in {f["campos"].get("meta_pdot", "") for f in filas_poa}:
        if not texto:
            continue
        n = _norm(texto)
        candidatos: list[tuple[int, dict]] = []
        for clave, meta in idx:
            if not clave:
                continue
            comun = len(clave) if (n.startswith(clave) or clave.startswith(n)) else 0
            if comun >= UMBRAL_PREFIJO:
                candidatos.append((comun, meta))
        if not candidatos:
            fuera[texto] = {"id": None, "caracteres_coincidentes": 0,
                            "estado": "declarada_sin_reconciliar"}
            continue
        chars = max(c for c, _ in candidatos)
        empatados = [m for c, m in candidatos if c == chars]
        # M002 y M018 comparten enunciado literal en el PDOT. Ninguna
        # reconciliación por texto puede separarlas, y fingir que eligió bien
        # sería inventar. Se marca el empate y se conserva a quién alcanzó.
        fuera[texto] = {
            "id": empatados[0]["id"], "caracteres_coincidentes": chars,
            "estado": ("declarada_y_reconciliada" if len(empatados) == 1
                       else "reconciliacion_ambigua"),
            **({"empatan_con": [m["id"] for m in empatados]} if len(empatados) > 1 else {}),
        }
    return fuera


# ══════════════════════════════════════════════════════════════════════════════
# DIMENSIÓN 2 · VÍNCULO PRESUPUESTARIO — a cuántas metas sirve cada partida
# ══════════════════════════════════════════════════════════════════════════════
def exclusividad(filas_poa: list[dict]) -> dict[str, set]:
    """Una partida que financia 16 metas no puede acreditar ejecución de una.

    El clasificador presupuestario es un ÍTEM DE GASTO («consultoría»,
    «edificios»), no un identificador de meta. Que varias metas compartan uno es
    normal en la técnica presupuestaria — lo que no es admisible es tratar el
    devengado de ese ítem como prueba de una meta en particular."""
    mapa: dict[str, set] = {}
    for f in filas_poa:
        p, m = f["campos"].get("partida"), f["campos"].get("meta_pdot")
        if p and m:
            mapa.setdefault(p, set()).add(m)
    return mapa


# ══════════════════════════════════════════════════════════════════════════════
# DIMENSIÓN 3 · EVIDENCIA FINANCIERA — qué dice la cédula de esa partida
# ══════════════════════════════════════════════════════════════════════════════
ORDEN_MES = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "septiembre", "octubre", "noviembre", "diciembre"], 1)}


def corte_anual(cedulas: list[dict], entidad: str, anio: int) -> tuple[dict, str | None]:
    """El corte más reciente del año. Las cifras de la cédula son ACUMULADAS
    —verificado: entre octubre y diciembre de 2025, 69 partidas suben, 68 quedan
    igual y ninguna baja—, de modo que el último mes disponible contiene el año.
    Se devuelve también cuál es, porque un corte de marzo no prueba lo mismo que
    uno de diciembre."""
    delaño = [c for c in cedulas if c["entidad"] == entidad and c["anio"] == anio]
    if not delaño:
        return {}, None
    mes = max((c["mes"] for c in delaño if c["mes"]), key=lambda m: ORDEN_MES.get(m, 0),
              default=None)
    return {c["partida"]: c for c in delaño if c["mes"] == mes}, mes


def estado_financiero(reg: dict | None) -> dict:
    if reg is None:
        return {"estado": "partida_no_hallada_en_cedula", "devengado": None,
                "codificado": None,
                "advertencia": "no hallada NO significa inexistente: significa "
                               "sin evidencia en las fuentes consultadas"}
    dev, cod, mod = reg.get("devengado"), reg.get("codificado"), reg.get("modificado")
    if dev and dev > 0:
        est = "devengado_positivo"
    elif cod and cod > 0:
        est = "codificado_sin_devengado"
    else:
        est = "sin_codificado"
    return {"estado": est, "devengado": dev, "codificado": cod, "modificado": mod,
            "reformada": bool(mod), "procedencia": reg["_procedencia"],
            "corte": {"entidad": reg["entidad"], "anio": reg["anio"], "mes": reg["mes"]}}


# ══════════════════════════════════════════════════════════════════════════════
# DERIVACIÓN DE V_eSIGEF — con el criterio literal de H13, y con su límite
# ══════════════════════════════════════════════════════════════════════════════
def derivar(partidas: list[dict], reconciliada: bool) -> dict:
    """H13 fija: 1,0 devengado certificado · 0,5 codificado sin devengado ·
    0,0 sin registro presupuestario.

    Se añade lo que H13 no contempla porque nunca se derivó automáticamente:
    **`null` cuando el dato no alcanza para decidir**. Un `null` no es un cero
    disfrazado — es la ausencia de evidencia declarada como resultado, que es
    justamente lo que el principio rector exige."""
    if not partidas:
        # DOS CASOS DISTINTOS, y colapsarlos afirma una ausencia que nadie probó.
        # `no_reconciliado` dice lo que de verdad ocurrió: EL PROCEDIMIENTO no
        # alcanzó la meta. `sin_partida_declarada` sí es un hecho del documento:
        # el POA la trae y no le ancla partida. Sólo el segundo habla de la
        # fuente; el primero habla de nosotros.
        if not reconciliada:
            return {"valor": None, "estado": "no_reconciliado",
                    "razon": "el procedimiento de reconciliación vigente no vinculó "
                             "esta meta con ninguna actividad del POA. NO significa "
                             "que el POA no la contemple"}
        return {"valor": None, "estado": "sin_partida_declarada",
                "razon": "el POA declara esta meta y no le ancla ninguna partida"}

    # ── SE EVALÚAN TODAS LAS PARTIDAS DE LA META, no un subconjunto.
    # Una versión previa se quedaba sólo con las exclusivas cuando existía
    # alguna, y con eso llegó a declarar `sin_registro_presupuestario` en metas
    # que tenían $187.200 devengados en otra de sus partidas. La exclusividad
    # sirve para ATRIBUIR UN MONTO; para responder «¿hay devengado?» descartar
    # partidas es fabricar una ausencia estrechando la mirada.
    estados = {p["cedula"]["estado"] for p in partidas}
    if "devengado_positivo" in estados:
        valor, est = 1.0, "devengado_certificado"
    elif "codificado_sin_devengado" in estados:
        valor, est = 0.5, "codificado_sin_devengado"
    elif estados == {"partida_no_hallada_en_cedula"}:
        return {"valor": None, "estado": "sin_evidencia_recuperada",
                "razon": "ninguna partida del POA para esta meta aparece en la "
                         "cédula consultada"}
    else:
        valor, est = 0.0, "sin_registro_presupuestario"

    # La atribución califica la evidencia que decidió, no la meta entera: es
    # unívoca si alguna partida EXCLUSIVA sostiene ese mismo estado.
    decisivas = [p for p in partidas if p["cedula"]["estado"] == (
        "devengado_positivo" if valor == 1.0 else
        "codificado_sin_devengado" if valor == 0.5 else p["cedula"]["estado"])]
    exclusivas = [p for p in decisivas
                  if p["exclusividad"]["estado"] == "partida_exclusiva"]
    atribucion = "univoca" if exclusivas else "compartida"

    r = {"valor": valor, "estado": est, "atribucion": atribucion,
         "partidas_decisivas": [p["partida"] for p in decisivas],
         "partidas_evaluadas": [p["partida"] for p in partidas]}
    if atribucion == "compartida":
        n = max(p["exclusividad"]["metas_que_la_usan"] for p in decisivas)
        r["razon"] = (f"ninguna partida exclusiva sostiene este estado; la más "
                      f"compartida sirve a {n} metas. Hay ejecución en la línea que "
                      f"financia esta meta, pero el monto no le es atribuible")
    return r


def construir(anio: int) -> dict:
    registro = json.loads(REGISTRO.read_text(encoding="utf-8"))["metas"]
    filas = extraer_poa(POA_POR_ANIO[anio])
    cedulas = extraer_todo(anio)
    corte, mes = corte_anual(cedulas, "GAD Montecristi", anio)

    recon = reconciliar_metas(filas, registro)
    comparte = exclusividad(filas)

    # meta del registro → filas del POA que la declaran
    por_meta: dict[str, list[dict]] = {}
    for f in filas:
        t = f["campos"].get("meta_pdot", "")
        mid = recon.get(t, {}).get("id")
        if mid:
            por_meta.setdefault(mid, []).append(f)

    vinculos = []
    for m in registro:
        fpoa = por_meta.get(m["id"], [])
        objetivos = {f["campos"].get("objetivo_estrategico", "") for f in fpoa} - {""}

        partidas = []
        for p in sorted({f["campos"].get("partida") for f in fpoa if f["campos"].get("partida")}):
            usan = len(comparte.get(p, set()))
            fila = next(f for f in fpoa if f["campos"].get("partida") == p)
            partidas.append({
                "partida": p,
                "exclusividad": {
                    "estado": "partida_exclusiva" if usan == 1 else "partida_compartida",
                    "metas_que_la_usan": usan},
                "poa": {"archivo": POA_POR_ANIO[anio], "fila": fila["fila"],
                        "actividad": fila["campos"].get("actividad", "")[:120],
                        "monto": fila["campos"].get("monto", ""),
                        "partida_completa": fila["campos"].get("partida_completa", "")},
                "cedula": estado_financiero(corte.get(p)),
            })

        vinculos.append({
            "meta": {"id": m["id"], "sistema": m.get("sistema"),
                     "texto_registro": m["meta"], "ejecutor": m.get("tipo_ejecutor")},
            "articulacion": {
                "estrategica": {
                    "estado": "declarada" if objetivos else "no_declarada",
                    "objetivos": sorted(objetivos)[:3]},
                "operacional": {
                    "estado": "declarada_y_reconciliada" if fpoa else "no_reconciliado",
                    "filas_poa": len(fpoa),
                    "caracteres_coincidentes": max(
                        (recon[f["campos"]["meta_pdot"]]["caracteres_coincidentes"]
                         for f in fpoa), default=0)},
            },
            "partidas": partidas,
            "V_eSIGEF_derivado": derivar(partidas, bool(fpoa)),
        })

    # La otra dirección: ejecución sin meta demostrable. No es un sobrante del
    # cruce — es un resultado: dinero devengado cuya trazabilidad hacia el plan
    # no puede reconstruirse desde los instrumentos publicados.
    en_poa = set(comparte)
    huerfanas = [{"partida": p, "descripcion": c.get("descripcion", "")[:80],
                  "devengado": c.get("devengado"),
                  "procedencia": c["_procedencia"]}
                 for p, c in corte.items()
                 if p not in en_poa and (c.get("devengado") or 0) > 0]

    return {
        "_meta": {
            "generado": _dt.date.today().isoformat(), "anio": anio,
            "capa": "DERIVADA · no sustituye ninguna fuente",
            "poa": POA_POR_ANIO[anio], "corte_cedula": mes,
            "umbral_prefijo": UMBRAL_PREFIJO,
            "alcance": "PDOT vigente · el POA 2023-2024 no declara alineación (OBS-027)",
            "regla": "no_hallado ≠ no existe · ausencia de evidencia es un resultado",
        },
        "vinculos": vinculos,
        "ejecucion_sin_meta_demostrable": sorted(
            huerfanas, key=lambda x: -(x["devengado"] or 0)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", type=int, default=2025)
    ap.add_argument("--escribir", action="store_true", help="vuelca la capa derivada")
    args = ap.parse_args()

    d = construir(args.anio)
    v = d["vinculos"]
    print(f"CRUCE POA {args.anio} ↔ CÉDULA (corte {d['_meta']['corte_cedula']})\n")

    def cuenta(f):
        from collections import Counter
        return Counter(f(x) for x in v)

    print("  ARTICULACIÓN OPERACIONAL (meta declarada en el POA)")
    for k, n in cuenta(lambda x: x["articulacion"]["operacional"]["estado"]).most_common():
        print(f"     {k:32} {n:3}/66")
    print("\n  V_eSIGEF DERIVADO")
    for k, n in cuenta(lambda x: x["V_eSIGEF_derivado"]["estado"]).most_common():
        print(f"     {k:32} {n:3}/66")
    atr = cuenta(lambda x: x["V_eSIGEF_derivado"].get("atribucion", "—"))
    print(f"\n  ATRIBUCIÓN: unívoca {atr.get('univoca',0)} · compartida "
          f"{atr.get('compartida',0)} · sin partida {atr.get('—',0)}")

    h = d["ejecucion_sin_meta_demostrable"]
    print(f"\n  EJECUCIÓN SIN META DEMOSTRABLE: {len(h)} partidas · "
          f"${sum(x['devengado'] or 0 for x in h):,.2f}")
    for x in h[:5]:
        print(f"     {x['partida']}  {x['descripcion'][:44]:46} ${x['devengado']:>14,.2f}")

    if args.escribir:
        SALIDA.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
