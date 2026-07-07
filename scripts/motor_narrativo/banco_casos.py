# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — BANCO DE CASOS (fase de calibración · Fase A)
Dylus Lab © 2026 · doctrina: PCD-MN01 §6/§11 (asesor 2026-07-06).

El activo científico del motor — el equivalente de H10c para los aportes. No es una
base de datos: es la **jurisprudencia algorítmica** de QUIRA. Cada caso validado
responde ¿qué es una promesa? ¿qué es evidencia suficiente? ¿cuándo hay contradicción?

Estructura de caso (11 campos · asesor):
  id · versión_algoritmo · narrativa_original · unidad_narrativa · claims ·
  evidencia_encontrada · relaciones_encontradas · resultado_automático ·
  corrección_humana · explicación · regla_aprendida

Genera el banco desde unidades.json + cruce.json (mismo orden). Los tres últimos
campos quedan VACÍOS: los llena la corrección humana (calibración), sin sobre-
escribir (idempotente: preserva correcciones ya hechas). Salida: banco_casos/MN{año}.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import identidad as _id

VERSION_ALGO = "mn-v0.1"


def construir(video_id: str, año: str) -> dict:
    d = _id.BASE / video_id
    unidades = json.loads((d / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    cruce = json.loads((d / "cruce.json").read_text(encoding="utf-8"))["detalle"]

    banco_dir = _id.BASE / "banco_casos"
    banco_dir.mkdir(parents=True, exist_ok=True)
    out_path = banco_dir / f"MN{año}.json"

    # correcciones humanas: archivo trazable (Fase A) + preservar las ya hechas (idempotente)
    corr_path = banco_dir / f"correcciones_MN{año}.json"
    corr = json.loads(corr_path.read_text(encoding="utf-8")) if corr_path.exists() else {}
    reglas = corr.get("_reglas", {})
    corr_casos = corr.get("casos", {})
    previo = {}
    if out_path.exists():
        for c in json.loads(out_path.read_text(encoding="utf-8")).get("casos", []):
            previo[c["id"]] = {k: c.get(k) for k in ("correccion_humana", "explicacion", "regla_aprendida")}

    casos = []
    for i, (u, c) in enumerate(zip(unidades, cruce)):
        cid = f"MN{año}-{i + 1:03d}"
        prev = previo.get(cid, {})
        cc = corr_casos.get(cid, {})
        regla_cod = cc.get("regla")
        casos.append({
            "id": cid,
            "version_algoritmo": VERSION_ALGO,
            "narrativa_original": {"t_seg": u.get("t"), "texto": u.get("texto")},
            "unidad_narrativa": {k: u.get(k, "") for k in
                                 ("tipo", "obra", "objetivo", "causalidad", "magnitud", "eje")},
            "claims": [u.get("texto")],                       # etapa 4 (descomposición) pendiente
            "evidencia_encontrada": {
                "plan": c.get("plan", {}),
                "promesa": c.get("promesa", {}),
            },
            "relaciones_encontradas": c.get("relacion"),
            "resultado_automatico": c.get("relacion"),
            # ── corrección humana (calibración · Fase A) ──
            "correccion_humana": cc.get("correccion") or prev.get("correccion_humana"),
            "explicacion": cc.get("explicacion") or prev.get("explicacion"),
            "regla_aprendida": (reglas.get(regla_cod, regla_cod) if regla_cod else prev.get("regla_aprendida")),
        })

    n_corr = sum(1 for c in casos if c["correccion_humana"])
    banco = {
        "motor": "Motor Narrativo (MIN/MCN)", "fuente": f"RDC {año}", "video_id": video_id,
        "version_algoritmo": VERSION_ALGO, "n_casos": len(casos), "n_corregidos": n_corr,
        "_nota": "Jurisprudencia algorítmica de QUIRA. correccion_humana/explicacion/regla_aprendida "
                 "se llenan uno por uno (Fase A calibración). NO exponer resultados hasta cerrar la matriz FP/FN.",
        "casos": casos,
    }
    out_path.write_text(json.dumps(banco, ensure_ascii=False, indent=2), encoding="utf-8")
    return banco


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    b = construir(vid, año)
    print(f"BANCO DE CASOS · {año}: {b['n_casos']} casos · {b['n_corregidos']} corregidos por humano")
    print(f"   {_id.BASE / 'banco_casos' / f'MN{año}.json'}")
    from collections import Counter
    dist = Counter(c["resultado_automatico"] for c in b["casos"])
    print("   distribución automática (interna, NO exponer):", dict(dist))
