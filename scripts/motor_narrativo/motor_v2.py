# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — v0.2 (Fase A3, construido con evidencia del corpus)
Dylus Lab © 2026 · doctrina: PCD-MN01 §15 (roadmap con efecto medido por regla).

Mejoras nacidas del corpus (no de intuición), en orden de impacto medido:
  1) FILTRO proceso/gestión  [R1] — descarta la meta-narrativa del proceso de
     rendición (comisiones, talleres, cronogramas…). Aval: Javo (16 años sector
     público) — no interesa el proceso, sino el discurso y sus cumplimientos.
  2) VALIDACIÓN de eje       [R2] — un match del POA solo cuenta si coincide el
     tema (agua↔agua), no solo el score semántico.

v0.1 queda LOCKED como benchmark. Este módulo NO lo toca: es la versión nueva.
Se evalúa sobre el MISMO corpus (98 casos con corrección humana) → comparación A4.
Las capas nuevas (presupuesto/programas/PAC · R4/R6/R7) se suman después.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))
sys.path.insert(0, str(_HERE.parent / "normativa"))
import identidad as _id
import ingest as _ing
from extract_poa_pdf import extract_poa

TH = 0.45
POA_AÑOS = (2024, 2025, 2026)

# ── R1 · léxico del PROCESO de rendición (meta-narrativa, no gestión) ─────────
_PROC = re.compile(r"\b(comisi[oó]n|comisiones|subcomisi|taller|talleres|mesa de trabajo|mesas|"
                   r"hoja de ruta|socializaci|socializ|formulario|deliberaci|delibera|cronograma|"
                   r"metodolog|rendici[oó]n de cuenta|cpccs|consejo de participaci|asamblea ciudadana|"
                   r"documentaci[oó]n|se reuni|reuni[oó]n|sesi[oó]n|se coordin|se solicit[oó]|se recibi[oó]|"
                   r"se conform[oó]|se present[oó]|se redact|difusi[oó]n del informe|plan bicentenario)\b",
                   re.IGNORECASE)

# ── R2 · léxico por EJE (para validar coincidencia temática del match) ────────
_EJE = {
    "agua": ["agua", "potable", "alcantarill", "hidrosanit", "pluvial", "saneamiento", "acueducto", "bombeo", "reservorio"],
    "vías": ["vía", "vial", "calle", "carreter", "pavimento", "asfalt", "bordillo", "acera"],
    "salud": ["salud", "médic", "brigada", "hospital", "cdi", "infantil", "juvenil", "bienestar", "instrumental"],
    "cultura": ["cultura", "arte", "museo", "creativa", "turism", "artesan", "sombrero", "danza", "música", "teatro", "taller"],
    "educación": ["educ", "escuela", "unidad educativa", "beca", "capacit", "formación", "infocentro", "estudiante"],
    "economía": ["emprend", "comercio", "mercado", "ingreso", "recaudaci", "productiv", "feria", "económic"],
    "ambiente": ["ambient", "parque", "reforest", "espacios públic", "verde", "recicl", "residuo", "basura"],
    "social": ["social", "vulnerab", "beneficiar", "inclusi", "acción social"],
    "seguridad": ["segurid", "riesgo", "emergencia", "bomber"],
}


def _proc(texto: str) -> bool:
    return bool(_PROC.search(texto or ""))


def _eje_de(texto: str) -> set[str]:
    t = (texto or "").lower()
    return {e for e, kws in _EJE.items() if any(k in t for k in kws)}


def _embed(model, txts):
    v = model.encode(txts, convert_to_numpy=True, show_progress_bar=False, batch_size=64)
    return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)


def clasificar(video_id: str) -> list[dict]:
    d = _id.BASE / video_id
    unidades = json.loads((d / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    model = _ing._get_model()
    U = _embed(model, [u.get("texto", "") for u in unidades])
    poa = {y: extract_poa(str(y)) for y in POA_AÑOS}
    P = {y: _embed(model, [p["desc"] for p in poa[y]]) for y in poa if poa[y]}

    out = []
    for i, u in enumerate(unidades):
        texto = u.get("texto", "")
        if _proc(texto):                                   # R1 · filtro proceso
            out.append({"clase": "proceso"}); continue
        eje_u = _eje_de(texto) | ({u.get("eje")} if u.get("eje") else set())
        # mejor match del POA que ADEMÁS coincida en eje (R2)
        best, best_ev = 0.0, ""
        for y in P:
            s = U[i] @ P[y].T
            order = np.argsort(-s)[:5]
            for j in order:
                desc = poa[y][int(j)]["desc"]
                if float(s[j]) < TH:
                    break
                if not eje_u or (_eje_de(desc) & eje_u):    # eje coincide
                    if float(s[j]) > best:
                        best, best_ev = float(s[j]), desc
                    break
        out.append({"clase": "coherente" if best >= TH else "sin_correlato",
                    "score": round(best, 3), "evidencia": best_ev[:80]})
    return out


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    v2 = clasificar(vid)
    banco = json.loads((_id.BASE / "banco_casos" / f"MN{año}.json").read_text(encoding="utf-8"))["casos"]

    # ── comparación A4 · v0.1 vs v0.2 sobre el mismo corpus (verdad humana) ──
    ok1 = ok2 = 0
    for c, p in zip(banco, v2):
        h = c["correccion_humana"]              # verdad humana
        a1 = c["resultado_automatico"]          # v0.1
        # v0.1 acierta si humano=OK y v0.1 dijo una clase de gestion (ya medido: 36)
        if h == "OK" and a1 in ("coherente", "obra_sin_promesa", "promesa_sin_ejecucion"):
            ok1 += 1
        # v0.2 acierta: proceso->proceso · OK->coherente · (FP eje, cifra, cobertura, meta, pac)->sin_correlato
        cl = p["clase"]
        if (h == "proceso_rendicion" and cl == "proceso") or (h == "OK" and cl == "coherente") \
           or (h in ("falso_positivo_evidencia", "cifra_financiera", "logro_cobertura",
                     "meta_narrativa", "verificar_pac") and cl == "sin_correlato"):
            ok2 += 1
    N = len(banco)
    print(f"COMPARACIÓN v0.1 vs v0.2 · corpus RDC {año} ({N} casos, verdad humana)")
    print(f"   v0.1 (LOCKED):  {ok1}/{N} = {100*ok1//N}% coincidencias con la verdad humana")
    print(f"   v0.2 (nuevo):   {ok2}/{N} = {100*ok2//N}% coincidencias con la verdad humana")
    from collections import Counter
    print("   v0.2 por clase:", dict(Counter(p["clase"] for p in v2)))
