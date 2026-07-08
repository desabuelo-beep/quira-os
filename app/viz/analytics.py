# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico — capa ANALYTICS del Motor Narrativo.
Dylus Lab © 2026 · doctrina: docs/architecture/SISTEMA_VISUALIZACION_CANONICO.md.

Transforma la salida CRUDA del motor en objetos `NarrativeEvidence` (datos, NO dibujo).
El renderer consume el resultado de aquí; jamás importa el motor. canon → datos → render.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ROOT / "scripts" / "motor_narrativo"))
from evidence import GRAMATICA, NarrativeEvidence, estado_fuente_tipo


def a_evidencias(unidades: list[dict], resultados: list[dict], periodo: str,
                 entidad: str = "GAD Montecristi") -> list[NarrativeEvidence]:
    """Motor (unidades + resultados de `clasificar`) → objetos canónicos. Solo datos."""
    out = []
    for i, (u, r) in enumerate(zip(unidades, resultados)):
        clase = r.get("clase", "sin_correlato")
        estado, fuente, tipo = estado_fuente_tipo(clase)
        nivel = r.get("nivel_evidencia") or "sin_evidencia_publica"  # proceso → gris (no sustantivo)
        # el estado se ALINEA con el nivel final (no con la clase cruda): una unidad sin
        # correlato en POA/PAC pero corroborada por el informe es "Declarada", no "Sin correlato".
        if tipo != "proceso":
            if nivel == "institucional":
                estado, fuente = "Declarado institucionalmente", (fuente or "Informe CPCCS (propia entidad)")
            elif nivel == "sin_evidencia_publica":
                estado = "Sin evidencia pública"
        out.append(NarrativeEvidence(
            id=u.get("id") or f"MN{periodo}-{i + 1:03d}",
            afirmacion=u.get("texto", ""),
            estado=estado, nivel_evidencia=nivel, fuente=fuente, tipo=tipo,
            explicacion=r.get("evidencia", ""), periodo=str(periodo),
            entidad=entidad, confianza=float(r.get("score", 0.0) or 0.0),
        ))
    return out


def resumen(evidencias: list[NarrativeEvidence]) -> dict:
    """Conteo por nivel de evidencia (el veredicto agregado del cajón)."""
    return dict(Counter(e.nivel_evidencia for e in evidencias if e.tipo != "proceso"))


if __name__ == "__main__":
    import json
    import identidad as _id
    import motor_v3
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    unidades = json.loads((_id.BASE / vid / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    banco_p = _id.BASE / "banco_casos" / f"MN{año}.json"
    if banco_p.exists():
        for u, c in zip(unidades, json.loads(banco_p.read_text(encoding="utf-8"))["casos"]):
            u["id"] = c["id"]
    ev = a_evidencias(unidades, motor_v3.clasificar(vid, año), año)
    print(f"NarrativeEvidence · RDC {año}: {len(ev)} afirmaciones · resumen sustantivo: {resumen(ev)}")
    for e in ev[:8]:
        n = GRAMATICA.get(e.nivel_evidencia, {}).get("nombre", "?")
        print(f"  [{n:5}] {e.id} · {e.estado:22} · {e.fuente[:22]:22} · {e.afirmacion[:44]}")
