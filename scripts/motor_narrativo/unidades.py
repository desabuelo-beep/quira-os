# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — Etapa 3 · UNIDADES NARRATIVAS
Dylus Lab © 2026 · doctrina: MOTOR_NARRATIVO_QUIRA.md §3 (asesor 2026-07-04).

NO extrae "claims" sueltos: extrae UNIDADES NARRATIVAS. Una frase de la autoridad
("Construimos tres parques para mejorar la seguridad") contiene obra + objetivo +
causalidad + promesa implícita. La normalización (etapa 4) la descompone luego en
claims verificables.

Modelo: Haiku 4.5 (operativo, volumen). La transcripción (auto-captions con ruido)
se trocea en ventanas con marcas de tiempo; Haiku limpia e identifica lo verificable.
Salida: data/motor_narrativo/{video_id}/unidades.json.
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
SEGS_POR_CHUNK = 140          # (legacy) — ahora se chunkea por caracteres
OVERLAP = 10
CHARS_POR_CHUNK = 4000        # presupuesto por ventana · robusto a la granularidad del
                              # segmento (captions cortos vs Whisper largos). Haiku extrae a fondo.

_SYS = (
    "Eres analista de rendición de cuentas públicas en Ecuador. De la transcripción "
    "(automática, con ruido) del discurso de una autoridad, extraes solo las AFIRMACIONES "
    "VERIFICABLES: obras ejecutadas, cifras, montos, coberturas, compromisos y promesas. "
    "IGNORAS saludos, agradecimientos, muletillas, aplausos y frases sin contenido verificable. "
    "Cada afirmación es una UNIDAD NARRATIVA que puede contener obra + objetivo + causalidad + "
    "promesa implícita. Respondes ÚNICAMENTE con un array JSON válido, sin texto adicional."
)

_INSTR = (
    'Extrae las unidades narrativas de este fragmento. Devuelve un array JSON; cada elemento:\n'
    '{"t": <segundos aprox. de la marca [t=Ns] más cercana>, "texto": "<afirmación limpia y '
    'concisa>", "tipo": "logro|cifra|compromiso|promesa", "obra": "<qué obra/acción, o \'\'>", '
    '"objetivo": "<para qué, o \'\'>", "causalidad": "<relación causal declarada, o \'\'>", '
    '"magnitud": "<cifra/monto/porcentaje si lo hay, o \'\'>", "eje": "<tema: agua|vías|salud|'
    'ambiente|seguridad|cultura|economía|institucional|otro>"}\n'
    'Si el fragmento no tiene afirmaciones verificables, devuelve [].\n\nFragmento:\n'
)


def _chunks(segs: list[dict]) -> list[tuple[float, str]]:
    """Chunks por PRESUPUESTO DE CARACTERES (~CHARS_POR_CHUNK). Robusto a la granularidad:
    con captions (segmentos cortos) o Whisper (segmentos largos) da ventanas del mismo
    tamaño, para que Haiku extraiga a fondo y no resuma. Solape de 1 segmento."""
    out, i = [], 0
    while i < len(segs):
        partes, last_t, chars, j = [], None, 0, i
        while j < len(segs) and chars < CHARS_POR_CHUNK:
            s = segs[j]
            if last_t is None or s["t"] - last_t >= 12:   # marca de tiempo cada ~12s
                partes.append(f'[t={int(s["t"])}s]')
                last_t = s["t"]
            partes.append(s["texto"])
            chars += len(s["texto"]) + 1
            j += 1
        out.append((segs[i]["t"], " ".join(partes)))
        i = max(j - 1, i + 1)   # solape de 1 segmento
    return out


def _parse_json(txt: str) -> list[dict]:
    m = re.search(r"\[.*\]", txt, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _client():
    import toml, anthropic
    sec = toml.load(str(_id._ROOT / ".streamlit" / "secrets.toml"))
    def _find(d):
        for k, v in d.items():
            if isinstance(v, dict):
                r = _find(v)
                if r:
                    return r
            elif isinstance(v, str) and v.startswith("sk-ant-"):
                return v
        return sec.get("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=_find(sec))


def extraer(video_id: str, max_chunks: int | None = None) -> dict:
    d = _id.BASE / video_id
    trans = json.loads((d / "transcripcion.json").read_text(encoding="utf-8"))
    chunks = _chunks(trans["segmentos"])
    if max_chunks:
        chunks = chunks[:max_chunks]
    client = _client()
    unidades, uso_in, uso_out = [], 0, 0
    for k, (t0, texto) in enumerate(chunks):
        r = client.messages.create(
            model=MODEL, max_tokens=1500, system=_SYS,
            messages=[{"role": "user", "content": _INSTR + texto}])
        uso_in += r.usage.input_tokens
        uso_out += r.usage.output_tokens
        for u in _parse_json(r.content[0].text):
            if isinstance(u, dict) and u.get("texto"):
                u["_chunk"] = k
                unidades.append(u)
        print(f"  chunk {k+1}/{len(chunks)} [t={int(t0)}s] → {len(_parse_json(r.content[0].text))} unidades")
    out = {
        "video_id": video_id, "modelo": MODEL, "n_chunks": len(chunks),
        "n_unidades": len(unidades),
        "tokens": {"in": uso_in, "out": uso_out},
        "unidades": unidades,
    }
    (d / "unidades.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    mc = int(sys.argv[2]) if len(sys.argv) > 2 else None      # limitar chunks (prueba)
    vid = _id._video_id(_id.PILOTO[año]["url"])
    res = extraer(vid, max_chunks=mc)
    print(f"\nUNIDADES · {año}: {res['n_unidades']} de {res['n_chunks']} chunks · "
          f"tokens {res['tokens']['in']}in/{res['tokens']['out']}out")
    for u in res["unidades"][:8]:
        print(f"  [{u.get('t')}s · {u.get('tipo')}·{u.get('eje')}] {u.get('texto','')[:70]}")
