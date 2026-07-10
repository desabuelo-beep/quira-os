# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — CAPA 0 · RELEVANCIA ONTOLÓGICA
Dylus Lab © 2026 · doctrina: PCD-MN01 §22 (Javo + asesor · 2026-07-10).

Antes de verificar, QUIRA decide si una afirmación MERECE análisis. La pregunta NO es
lingüística, es ONTOLÓGICA: ¿pertenece al dominio de la rendición de cuentas de GESTIÓN
pública? No elimina — CLASIFICA en 4 niveles (A estratégica · B programática · C
administrativa · D protocolaria). Se analizan A/B/C; la D se archiva y se cuenta
(transparencia: no se esconde, se explica por qué no entra). Los expedientes salen solo de A.

Pasada de clasificación sobre las unidades ya extraídas (respeta el Banco de Casos y los
IDs · costo mínimo). Salida: data/motor_narrativo/{video_id}/relevancia.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import identidad as _id

MODEL = "claude-haiku-4-5-20251001"
LOTE = 24                       # afirmaciones por llamada
_NIVEL = {"A": "estrategica", "B": "programatica", "C": "administrativa",
          "E": "prospectiva", "D": "protocolaria"}
_DEFECTO = "administrativa"      # ante fallo del clasificador: se queda EN el análisis (no se archiva)

_SYS = (
    "Eres analista de rendición de cuentas de gobiernos locales en Ecuador. Clasificas cada "
    "afirmación del discurso de la autoridad por su RELEVANCIA ONTOLÓGICA: si pertenece al "
    "dominio de la GESTIÓN pública verificable o es discurso protocolario. NO juzgas si es "
    "verdad; solo si MERECE verificarse como acto de gestión. Respondes ÚNICAMENTE con un "
    "array JSON válido, sin texto adicional."
)

_INSTR = (
    "Clasifica cada afirmación en UN nivel. Distingue lo YA HECHO (A/B/C · verificable hoy) de "
    "la PROMESA a futuro (E · se rastrea, no se verifica hoy) y del DISCURSO ceremonial (D · ruido):\n"
    "A · ESTRATÉGICA — obra, sistema, infraestructura o inversión estructural YA realizada o en "
    "curso, con magnitud. Ej: 'ejecutamos 28 millones en el sistema de agua', 'intervención en la "
    "Vía Lategadora con 53% de inversión municipal', 'recuperación del parque con 84 mil dólares'.\n"
    "B · PROGRAMÁTICA — línea de gestión o servicio recurrente YA operando: programa, "
    "mantenimiento, cobertura, catastro, ordenanzas. Ej: 'el patronato atendió a 3.000 personas', "
    "'catastro actualizado del 0% al 64%', 'se intervinieron 35 parques'.\n"
    "C · ADMINISTRATIVA — acto de gestión menor YA realizado: convenios, capacitaciones, "
    "adquisiciones, comisiones, talleres. Ej: 'firmamos un convenio', 'se conformó la comisión'.\n"
    "E · PROSPECTIVA — COMPROMISO o PROMESA a futuro sobre una gestión CONCRETA aún NO ejecutada: "
    "'se compromete a', 'se construirá', 'proyecto de', 'para 2027', 'contrapartida de 7 millones'. "
    "Es real y se RASTREA entre años, pero no es verificable hoy. Ej: 'se comprometió rehabilitar "
    "el sistema de agua', 'promesa de 5 parques en 2025', 'solución definitiva de agua a 2028'.\n"
    "D · PROTOCOLARIA — discurso ceremonial SIN gestión: agradecimientos, saludos, felicitaciones, "
    "celebraciones, menciones culturales o simbólicas, definiciones conceptuales. Ej: 'agradezco a "
    "la ciudadanía', 'el sombrero será lucido por los jugadores', 'la rendición incluye informar'.\n"
    "Regla de duda: entre A y B usa B; una promesa CONCRETA a futuro es E, no D; solo lo ceremonial "
    "sin gestión es D.\n\n"
    'Devuelve un array JSON, un elemento por afirmación, con el índice que se te da:\n'
    '{"i": <índice>, "n": "A|B|C|E|D", "motivo": "<3 a 6 palabras>"}\n\nAfirmaciones:\n'
)


def _client():
    import toml
    import anthropic
    sec = toml.load(str(_id._ROOT / ".streamlit" / "secrets.toml"))

    def _find(d):
        for v in d.values():
            if isinstance(v, dict):
                r = _find(v)
                if r:
                    return r
            elif isinstance(v, str) and v.startswith("sk-ant-"):
                return v
        return sec.get("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=_find(sec))


def _parse(txt: str) -> list[dict]:
    m = re.search(r"\[.*\]", txt, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def clasificar_relevancia(video_id: str) -> dict:
    d = _id.BASE / video_id
    unidades = json.loads((d / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    client = _client()
    niveles: dict[int, str] = {}
    motivos: dict[int, str] = {}
    uso_in = uso_out = 0
    for base in range(0, len(unidades), LOTE):
        lote = unidades[base:base + LOTE]
        cuerpo = "\n".join(f'{base + k}. "{u.get("texto", "")}"' for k, u in enumerate(lote))
        r = client.messages.create(
            model=MODEL, max_tokens=1600, system=_SYS,
            messages=[{"role": "user", "content": _INSTR + cuerpo}])
        uso_in += r.usage.input_tokens
        uso_out += r.usage.output_tokens
        for item in _parse(r.content[0].text):
            if isinstance(item, dict) and "i" in item:
                i = int(item["i"])
                niveles[i] = _NIVEL.get(str(item.get("n", "")).strip().upper(), _DEFECTO)
                motivos[i] = str(item.get("motivo", ""))[:60]
        print(f"  lote {base}-{base + len(lote) - 1} → {len(lote)} afirmaciones")

    items = []
    for i, u in enumerate(unidades):
        items.append({"i": i, "relevancia": niveles.get(i, _DEFECTO),
                      "motivo": motivos.get(i, ""), "texto": u.get("texto", "")[:80]})
    from collections import Counter
    dist = dict(Counter(it["relevancia"] for it in items))
    out = {"video_id": video_id, "modelo": MODEL, "n": len(items),
           "tokens": {"in": uso_in, "out": uso_out}, "distribucion": dist, "items": items}
    (d / "relevancia.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def cargar(video_id: str) -> list[str]:
    """Lista de niveles de relevancia alineada por índice (para el snapshot). '' si no hay pasada."""
    p = _id.BASE / video_id / "relevancia.json"
    if not p.exists():
        return []
    items = json.loads(p.read_text(encoding="utf-8")).get("items", [])
    return [it.get("relevancia", "estrategica") for it in items]


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2025"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    res = clasificar_relevancia(vid)
    print(f"\nRELEVANCIA ONTOLÓGICA · {año}: {res['n']} afirmaciones · {res['distribucion']}")
    print(f"   tokens {res['tokens']['in']}in/{res['tokens']['out']}out")
    for et, tag in (("prospectiva", "E seguimiento"), ("protocolaria", "D archivada")):
        for it in res["items"]:
            if it["relevancia"] == et:
                print(f"   [{tag}] {it['texto'][:62]}  · {it['motivo']}")
