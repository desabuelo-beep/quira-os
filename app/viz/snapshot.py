# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico — SNAPSHOT del cajón de Verificabilidad.
Dylus Lab © 2026 · doctrina: SISTEMA_VISUALIZACION_CANONICO.md + CONSTITUCION_VISUAL_QUIRA.md.

Corre el motor UNA vez y empaqueta TODO lo que el renderer necesita (evidencias, resumen,
expedientes, marco legal, síntesis, meta) en un JSON. Patrón QUIRA: motor→snapshot→UI, la
app nunca corre el motor en vivo (Regla 1). El renderer consume el snapshot, no el motor.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_ROOT / "scripts" / "motor_narrativo"))
from evidence import GRAMATICA, RELEVANCIA, analiza_relevancia
from analytics import a_evidencias, resumen as _resumen, _sustantiva

# etiquetas públicas del espectro (Constitución Visual §3) — orden de lectura
_ESPECTRO = [
    ("independiente", "Prueba independiente", "registro externo"),
    ("institucional", "Autocertificación", "solo su informe"),
    ("parcial", "Prueba parcial", "ventana / cobertura"),
    ("sin_evidencia_publica", "Sin respaldo público", "no publicado"),
    ("contradiccion", "Prueba en contrario", ""),
]
# config por entidad (genérico para 221 GAD; hoy Montecristi = Municipio 001)
_ENTIDAD = {
    "GAD Montecristi": {"autoridad": "alcalde Jonathan Toro", "cargo": "Alcalde",
                        "canton": "Montecristi", "provincia": "Manabí", "municipio": "001"},
}


def _marco_legal() -> dict:
    p = _ROOT / "data" / "motor_narrativo" / "base_normativa_rdc.json"
    return json.loads(p.read_text(encoding="utf-8")).get("marco_por_seccion", {}) if p.exists() else {}


# resultado por defecto cuando el motor no deja glosa (lenguaje de administración pública)
_FALLBACK = {
    "institucional": "Consta en su propio informe de rendición; sin registro externo que lo corrobore.",
    "sin_evidencia_publica": "No se localizó publicación en las fuentes oficiales consultadas.",
    "parcial": "Verificado solo en parte de la ventana temporal o de la cobertura declarada.",
    "contradiccion": "La evidencia documental difiere de lo afirmado.",
    "independiente": "Corroborado en un registro público independiente del emisor.",
}


# fuente del motor → nodo de la cadena documental donde se corroboró (mini-cadena del expediente)
_STAGE = {"POA (planificación)": "poa", "PAC / SERCOP": "sercop", "Cédula presupuestaria": "cedula",
          "Literal D (patronato)": "registro", "Informe CPCCS (propia entidad)": "informe"}
_RO = {"estrategica": 0, "programatica": 1, "administrativa": 2, "protocolaria": 3}


def _stage(fuente: str) -> str:
    return _STAGE.get((fuente or "").strip(), "discurso")


# VALOR DEMOSTRATIVO (asesor · 2026-07-10) — no "EQS": lo entiende cualquier funcionario y no
# parece métrica inventada. Mide cuánto DEMUESTRA el método un expediente (0-100): nivel de prueba
# + profundidad de la cadena documental + peso estratégico + magnitud + confianza del cruce.
_FIG = re.compile(r"\$|\d\s*%|mill|\bmil\b|\d[.,]\d|\d{3,}", re.I)
_VD_NIVEL = {"independiente": 40, "contradiccion": 38, "parcial": 24, "institucional": 20, "sin_evidencia_publica": 10}
_VD_CADENA = {"cedula": 25, "sercop": 22, "registro": 18, "poa": 15, "informe": 8, "discurso": 3}
_VD_BADGE_NIVEL = {"independiente": "Registro independiente", "contradiccion": "Contradice la evidencia",
                   "parcial": "Cobertura parcial", "institucional": "Autocertificado", "sin_evidencia_publica": "Sin respaldo público"}
_VD_BADGE_CADENA = {"cedula": "Cadena completa", "sercop": "En contratación", "registro": "Registro de cobertura",
                    "poa": "En planificación", "informe": "Solo en informe", "discurso": "Solo en el discurso"}


def _valor_demostrativo(e) -> tuple:
    """Puntaje 0-100 + hasta 3 sellos cualitativos. El expediente debe ser una demostración del método."""
    cad = _stage(e.fuente)
    mag = 10 if _FIG.search(e.afirmacion or "") else 0
    vd = min(_VD_NIVEL.get(e.nivel_evidencia, 10) + _VD_CADENA.get(cad, 3)
             + (20 if e.relevancia == "estrategica" else 12) + mag
             + round(min(max(e.confianza, 0.0), 1.0) * 5), 100)
    badges = [_VD_BADGE_NIVEL.get(e.nivel_evidencia, ""), _VD_BADGE_CADENA.get(cad, "")]
    if mag:
        badges.append("Impacto cuantificado")
    return vd, [b for b in badges if b][:3]


def _expedientes(evs: list, k: int = 4) -> list[dict]:
    """Expedientes SOLO de afirmaciones estratégicas/programáticas (Capa 0 · JAMÁS protocolarias):
    una afirmación de valor público, no discurso ceremonial. Guarda el texto COMPLETO (el renderer
    trunca) y la CADENA documental donde se corroboró (mini-demostración por expediente)."""
    base = [e for e in evs if _sustantiva(e) and e.relevancia in ("estrategica", "programatica")]
    quiere = ["independiente", "independiente", "institucional", "sin_evidencia_publica", "parcial"]
    porn: dict[str, list] = {}
    for e in base:
        porn.setdefault(e.nivel_evidencia, []).append(e)
    for v in porn.values():
        v.sort(key=lambda e: -_valor_demostrativo(e)[0])   # el más demostrativo primero (Valor Demostrativo)
    out, usados = [], Counter()
    for nivel in quiere:
        pool = porn.get(nivel, [])
        if usados[nivel] < len(pool):
            e = pool[usados[nivel]]; usados[nivel] += 1
            vd, badges = _valor_demostrativo(e)
            out.append({"id": e.id, "estado": e.estado, "aseveracion": (e.afirmacion or "").strip(),
                        "fuente": e.fuente or "—",
                        "resultado": (e.explicacion or "").strip() or _FALLBACK.get(e.nivel_evidencia, "—"),
                        "nivel": e.nivel_evidencia, "color": e.color, "vd": vd, "badges": badges,
                        "relevancia": e.relevancia, "eje": e.eje or "otro", "cadena": _stage(e.fuente)})
        if len(out) >= k + 1:
            break
    return out[:k + 1]


def construir(año: str, entidad: str = "GAD Montecristi") -> dict:
    import identidad as _id
    import motor_v3
    vid = _id._video_id(_id.PILOTO[año]["url"])
    unidades = json.loads((_id.BASE / vid / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    banco_p = _id.BASE / "banco_casos" / f"MN{año}.json"
    if banco_p.exists():
        for u, c in zip(unidades, json.loads(banco_p.read_text(encoding="utf-8"))["casos"]):
            u["id"] = c["id"]
    import relevancia as _rel
    meta_e = _ENTIDAD.get(entidad, _ENTIDAD["GAD Montecristi"])
    rels = _rel.cargar(vid)                               # Capa 0 · relevancia ontológica (A/B/C/D)
    evs = a_evidencias(unidades, motor_v3.clasificar(vid, año), año, entidad=entidad, relevancias=rels)
    res = _resumen(evs)                                   # conteo por nivel · solo A/B/C (con valor público)
    n_sust = sum(res.values()) or 1
    n_proc = sum(1 for e in evs if e.tipo == "proceso")
    # EMBUDO de relevancia (Capa 0) — prueba de rigor: cuántas afirmaciones entran al análisis
    no_proc = [e for e in evs if e.tipo != "proceso"]
    emb = Counter(e.relevancia for e in no_proc)
    embudo = {
        "extraidas": len(evs), "proceso": n_proc, "con_gestion": len(no_proc), "analizadas": n_sust,
        "niveles": [{"clave": kk, "nivel": v["nivel"], "label": v["label"], "sub": v["sub"],
                     "n": emb.get(kk, 0), "pct": round(100 * emb.get(kk, 0) / (len(no_proc) or 1)),
                     "color": v["color"], "analiza": v["analiza"]}
                    for kk, v in sorted(RELEVANCIA.items(), key=lambda x: x[1]["orden"])],
    }
    # corte por EJE temático — insumo de la sección longitudinal (cruce entre años)
    por_eje: dict[str, dict] = {}
    for e in evs:
        if not _sustantiva(e):
            continue
        dd = por_eje.setdefault(e.eje or "otro", {"n": 0, "independiente": 0})
        dd["n"] += 1
        if e.nivel_evidencia == "independiente":
            dd["independiente"] += 1
    espectro = [{"nivel": nv, "label": lb, "sub": sub, "n": res.get(nv, 0),
                 "pct": round(100 * res.get(nv, 0) / n_sust), "color": GRAMATICA[nv]["color"]}
                for nv, lb, sub in _ESPECTRO]
    ind = res.get("independiente", 0); sinp = res.get("sin_evidencia_publica", 0)
    return {
        "dominio": "Verificabilidad Pública del Discurso",
        "meta": {**meta_e, "año": año, "evento": "Rendición de Cuentas", "n_afirmaciones": len(evs)},
        "resumen": {"sustantivas": n_sust, "proceso": n_proc,
                    "pct_independiente": round(100 * ind / n_sust),
                    "pct_sin_evidencia": round(100 * sinp / n_sust), **res},
        "embudo": embudo,
        "espectro": espectro,
        "por_eje": por_eje,
        "expedientes": _expedientes(evs),
        "marco_legal": _marco_legal(),
        "sintesis": {
            "hallazgos": [
                ("independiente", f"{round(100 * ind / n_sust)}%", "del discurso se sostiene en registros externos e independientes."),
                ("sin_evidencia_publica", f"{round(100 * sinp / n_sust)}%", "sin respaldo público verificable."),
                ("independiente", f"{res.get('contradiccion', 0)}", "aseveraciones contradichas por la evidencia documental."),
            ],
            "fuentes": ["Discurso RDC (audiovisual)", "POA", "Contratación (SERCOP)",
                        "Cédula presupuestaria", "Literal D — patronato", "Informe CPCCS", "Transparencia (LOTAIP)"],
        },
    }


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2025"
    snap = construir(año)
    outdir = _ROOT / "data" / "motor_narrativo" / "snapshots"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"verificabilidad_{año}.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    r = snap["resumen"]
    print(f"SNAPSHOT verificabilidad {año} → {out}")
    print(f"   {r['sustantivas']} sustantivas · {r.get('independiente',0)} indep · "
          f"{r.get('institucional',0)} inst · {r.get('parcial',0)} parc · {r.get('sin_evidencia_publica',0)} sin · "
          f"{len(snap['expedientes'])} expedientes")
