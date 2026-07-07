# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — v0.3 (Fase A3, suma la capa PAC/SERCOP · R7)
Dylus Lab © 2026 · doctrina: PCD-MN01 §15 (roadmap con efecto medido por regla).

Hereda v0.2 (filtro proceso R1 + validación de eje R2) y añade la 3.ª capa:

  CAPA PAC/SERCOP [R7] — el "detector de paja" que pidió Javo. Una unidad que NO
  tiene correlato en el POA (ejecución) se cruza contra el PAC (contratación). Si
  aparece como proceso SERCOP con eje coincidente → clase NUEVA "en_contratacion"
  (real, verificable, aún no ejecutada). Si NO aparece en POA NI en PAC →
  "sin_correlato" = candidata a paja (anunciada sin respaldo documental).

El cruce del PAC barre el PERIODO (2024+2025+2026), no solo el año del discurso:
una obra anunciada en la rendición 2024 puede contratarse en 2025 (validado con
el alcantarillado de Eloy Alfaro). Mismo criterio de ventana que los aportes.

v0.1 LOCKED (benchmark) · v0.2 intacto (benchmark) · esto es la versión nueva.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))
sys.path.insert(0, str(_HERE.parent / "normativa"))
import identidad as _id
import ingest as _ing
from extract_poa_pdf import extract_poa
from extract_pac_docx import extract_pac
from extract_informe_docx import extract_informe
from extract_cedula_xls import ejecucion_gastos
# reutiliza los helpers del v0.2 (no se duplican): filtro proceso + eje + embed
from motor_v2 import TH, POA_AÑOS, _proc, _eje_de, _embed

TH_PAC = 0.45  # mismo umbral; el guard real es la coincidencia de eje (R2)
TH_INF = 0.50  # corroboración CPCCS: el informe es la voz ESCRITA del mismo actor
TOL_EJEC = 2.0  # tolerancia (puntos %) para dar por coincidente la ejecución declarada

# R4 · claim financiero (agregado): ejecución/ingresos/deuda. NO cifras de obra
# (esas van al POA/PAC). El % afirmado se extrae para contrastar con la cédula.
_FIN = re.compile(r"\b(ejecuci[oó]n|ingresos?|recaud|deuda|equidad\s+territorial|presupuestari)\b", re.I)
_PCT = re.compile(r"(\d+(?:[.,]\d+)?)\s*%")
_CIFRA = re.compile(r"\d\s*%|millones?|mill[oó]n|d[oó]lares|\$\s*\d", re.I)  # el claim trae cifra financiera
_HIST = re.compile(r"\b(2019|2020|2021|2022|2023)\b")  # año histórico (fuera de la cédula del discurso)

# tokens genéricos de gobierno/obra (no distinguen una obra de otra) — se ignoran
# para el match por NOMBRE de obra (el embedding diluye los nombres propios).
_GENERIC = {"canton", "montecristi", "parroquia", "comuna", "gobierno", "autonomo",
            "descentralizado", "municipal", "provincia", "manabi", "sector", "barrio",
            "proceso", "contratacion", "adquisicion", "construccion", "sistema",
            "servicio", "servicios", "proyecto", "inversion", "valor", "obra", "obras",
            "cantonal", "ciudad", "mejoramiento", "general", "fiscalizacion"}


def _strip(s: str) -> str:
    return (s or "").lower().translate(str.maketrans("áéíóúñ", "aeioun"))


def _sig_tokens(txt: str) -> set[str]:
    """tokens significativos (≥5 letras, sin acentos, no genéricos) = nombre de obra."""
    return {w for w in re.findall(r"[a-z]{5,}", _strip(txt)) if w not in _GENERIC}


def _r4(texto: str, ced: dict | None) -> dict:
    """CAPA R4 · claim financiero. La ejecución presupuestaria GENERAL del año se
    verifica DOCUMENTALMENTE contra la cédula oficial de gastos (no contra el canon:
    su PSG_EJECUCION es otra métrica). Ingresos/deuda/histórico → requiere_registro
    (sin fuente aún). Cifras públicas de presupuesto, no métricas del Gold Master."""
    t = texto.lower()
    m = _PCT.search(texto)
    es_ejec_gral = ("egreso" in t or "presupuestari" in t or ("ejecuci" in t and "ingreso" not in t))
    if m and ced and es_ejec_gral and not _HIST.search(t):
        claimed = float(m.group(1).replace(",", "."))
        oficial = ced["ratio"] * 100
        if abs(claimed - oficial) <= TOL_EJEC:
            return {"clase": "verif_ejecucion",
                    "evidencia": f"cédula oficial de gastos {ced['año']}: ejecución {oficial:.2f}% (dijo {claimed:g}%)"}
        return {"clase": "discrepa_ejecucion",
                "evidencia": f"dijo {claimed:g}% · cédula oficial {oficial:.2f}%"}
    return {"clase": "sin_evidencia_publica",
            "evidencia": "ingresos/deuda: la DPE no publica cédula de ingresos → el ciudadano no puede comprobarlo"}


def _nivel_evidencia(res: dict) -> str:
    """Taxonomía de VERIFICABILIDAD PÚBLICA (asesor 2026-07-07). QUIRA no certifica
    verdad: certifica el NIVEL de evidencia pública de cada afirmación. Inexpugnable —
    cada veredicto se ancla a un documento o a la AUSENCIA documentada de uno (Regla 3).
    El nivel se DERIVA de qué capa la respaldó (no es un juicio nuevo)."""
    cl = res["clase"]
    if cl in ("coherente", "en_contratacion", "verif_ejecucion"):
        return "independiente"      # registro administrativo EXTERNO (POA/PAC/cédula/SERCOP)
    if cl == "discrepa_ejecucion":
        return "contradiccion"      # hay evidencia pública y CONTRADICE lo declarado
    if res.get("en_informe"):
        return "institucional"      # solo en el documento del PROPIO actor (informe CPCCS)
    return "sin_evidencia_publica"  # ni externo ni institucional (incl. documento no publicado)


def clasificar(video_id: str, año: str = "2024") -> list[dict]:
    d = _id.BASE / video_id
    unidades = json.loads((d / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    model = _ing._get_model()
    U = _embed(model, [u.get("texto", "") for u in unidades])

    poa = {y: extract_poa(str(y)) for y in POA_AÑOS}
    P = {y: _embed(model, [p["desc"] for p in poa[y]]) for y in poa if poa[y]}
    pac = {y: extract_pac(str(y)) for y in POA_AÑOS}
    PA = {y: _embed(model, [p["desc"] for p in pac[y]]) for y in pac if pac[y]}
    # CAPA CPCCS (evidencia): el informe ESCRITO de la misma rendición (voz escrita
    # del actor). Corrobora lo que DIJO en el video con lo que DECLARÓ por escrito.
    inf = list(extract_informe(año, "GAD"))
    INF = _embed(model, inf) if inf else None
    ced = ejecucion_gastos(año)  # cédula oficial de gastos (capa R4 · ejecución)

    def _mejor(vec, banco_emb, banco_txt, eje_u, th, tipos=None):
        """mejor match del banco con eje coincidente (R2). -> (score, evidencia).
        tipos: si se pasa, solo considera procesos de esos tipos de compra (guard
        de integridad del PAC: una obra anunciada se verifica con un proceso de
        Obra/Consultoría, NO con una compra de insumos Bien/Servicio)."""
        best, best_ev = 0.0, ""
        for y in banco_emb:
            s = vec @ banco_emb[y].T
            for j in np.argsort(-s)[:8]:
                if float(s[j]) < th:
                    break
                item = banco_txt[y][int(j)]
                if tipos and item.get("tipo") not in tipos:
                    continue
                if not eje_u or (_eje_de(item["desc"]) & eje_u):
                    if float(s[j]) > best:
                        best, best_ev = float(s[j]), f"{y}·{item['desc'][:70]}"
                    break
        return best, best_ev

    poa_txt = {y: poa[y] for y in P}
    pac_txt = {y: pac[y] for y in PA}
    def _corrobora(vec):
        """capa CPCCS: ¿la unidad aparece en el informe escrito? -> (bool, evidencia)."""
        if INF is None:
            return False, ""
        si = vec @ INF.T
        k = int(np.argmax(si))
        return (float(si[k]) >= TH_INF), (inf[k][:70] if float(si[k]) >= TH_INF else "")

    out = []
    for i, u in enumerate(unidades):
        texto = u.get("texto", "")
        if _proc(texto):                                        # R1 · filtro proceso
            out.append({"clase": "proceso"}); continue
        eje_u = _eje_de(texto) | ({u.get("eje")} if u.get("eje") else set())
        best, ev = _mejor(U[i], P, poa_txt, eje_u, TH)          # R2 · cruce POA
        if best >= TH:
            res = {"clase": "coherente", "score": round(best, 3), "evidencia": ev}
        else:
            # sin correlato en POA → CAPA PAC (R7 · ¿tiene proceso de contratación?)
            bp, evp = _mejor(U[i], PA, pac_txt, eje_u, TH_PAC, tipos={"Obra", "Consultoría"})
            if bp < TH_PAC:
                # override por NOMBRE de obra: el embedding diluye nombres propios (ej.
                # "Parque La Huella"). Si el PAC nombra la MISMA obra (≥2 tokens propios
                # compartidos) con eje y tipo Obra/Consultoría coincidentes → match.
                ut = _sig_tokens(texto)
                if len(ut) >= 2:
                    for y in pac_txt:
                        for it in pac_txt[y]:
                            if it.get("tipo") not in ("Obra", "Consultoría"):
                                continue
                            comun = ut & _sig_tokens(it["desc"])
                            if len(comun) >= 2 and (not eje_u or (_eje_de(it["desc"]) & eje_u)):
                                bp = max(bp, TH_PAC)
                                evp = f"{y}·{it['desc'][:60]} [nombre:{','.join(sorted(comun))}]"
                                break
                        if bp >= TH_PAC:
                            break
            if bp >= TH_PAC:
                res = {"clase": "en_contratacion", "score": round(bp, 3), "evidencia": f"PAC {evp}"}
            elif _FIN.search(texto) and _CIFRA.search(texto):   # R4 · claim financiero (cédula)
                res = _r4(texto, ced)
            else:
                res = {"clase": "sin_correlato", "score": round(max(best, bp), 3)}
        # capa CPCCS (evidencia · aditiva, no cambia la clase de verificación)
        res["en_informe"], inf_ev = _corrobora(U[i])
        if inf_ev:
            res["informe_ev"] = inf_ev
        res["nivel_evidencia"] = _nivel_evidencia(res)   # taxonomía de verificabilidad pública
        out.append(res)
    return out


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    v3 = clasificar(vid, año)
    banco = json.loads((_id.BASE / "banco_casos" / f"MN{año}.json").read_text(encoding="utf-8"))["casos"]

    # ── scoring HONESTO v0.3 ──
    #   proceso->proceso · OK->coherente · (falso_positivo, cifra, cobertura, meta)->sin_correlato
    #   verificar_pac -> VERIFICADA en POA (coherente) O en PAC (en_contratacion): ambas
    #   significan "es real, no paja". Solo sin_correlato = el motor no pudo verificarla.
    ok = 0
    aciertos_pac = []
    for c, p in zip(banco, v3):
        h = c["correccion_humana"]
        cl = p["clase"]
        if (h == "proceso_rendicion" and cl == "proceso") \
           or (h == "OK" and cl == "coherente") \
           or (h == "verificar_pac" and cl in ("en_contratacion", "coherente")) \
           or (h == "cifra_financiera" and cl in ("verif_ejecucion", "sin_evidencia_publica", "discrepa_ejecucion", "sin_correlato")) \
           or (h in ("falso_positivo_evidencia", "logro_cobertura", "meta_narrativa") and cl == "sin_correlato"):
            ok += 1
        if h == "verificar_pac":
            aciertos_pac.append((c["id"], cl, p.get("evidencia", "")))
    N = len(banco)
    print(f"MOTOR v0.3 · corpus RDC {año} ({N} casos · verdad humana)")
    print(f"   aciertos: {ok}/{N} = {100 * ok // N}%")
    print("   distribución por clase:", dict(Counter(p['clase'] for p in v3)))
    print("   CAPA PAC · los 3 casos R7 (¿es paja o está en contratación?):")
    for cid, cl, ev in aciertos_pac:
        print(f"      {cid} -> {cl}   {ev[:80]}")
    # CAPA CPCCS · corroboración por el informe escrito (evidencia aditiva)
    corr = sum(1 for p in v3 if p.get("en_informe"))
    print(f"   CAPA CPCCS · {corr}/{N} unidades corroboradas por el informe escrito. "
          "Declaradas por escrito en las categorías que el POA/PAC no cubren:")
    for tipo in ("cifra_financiera", "logro_cobertura"):
        ct = [(c, p) for c, p in zip(banco, v3) if c["correccion_humana"] == tipo]
        n = sum(1 for _, p in ct if p.get("en_informe"))
        print(f"      {tipo}: {n}/{len(ct)} declaradas en el informe (R4/R6)")
    # CAPA R4 · verificación de cifras financieras contra la cédula oficial de gastos
    r4d = Counter(p["clase"] for c, p in zip(banco, v3) if c["correccion_humana"] == "cifra_financiera")
    print(f"   CAPA R4 · 13 cifras financieras · distribución: {dict(r4d)}")
    for c, p in zip(banco, v3):
        if c["correccion_humana"] == "cifra_financiera" and p["clase"] in ("verif_ejecucion", "discrepa_ejecucion"):
            print(f"      {c['id']} -> {p['clase']}: {p.get('evidencia', '')[:78]}")
    # TAXONOMÍA DE EVIDENCIA PÚBLICA (asesor) — el veredicto inexpugnable: no certifica
    # verdad, certifica el NIVEL de respaldo público de cada afirmación sustantiva.
    niv = Counter(p.get("nivel_evidencia") for p in v3 if p.get("nivel_evidencia"))
    print("   NIVEL DE EVIDENCIA PÚBLICA (afirmaciones sustantivas · no-proceso):")
    for k in ("independiente", "institucional", "contradiccion", "sin_evidencia_publica"):
        if niv.get(k):
            print(f"      {k}: {niv[k]}")
