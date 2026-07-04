# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — Etapa 1-2 · ADQUISICIÓN + TRANSCRIPCIÓN
Dylus Lab © 2026 · doctrina: MOTOR_NARRATIVO_QUIRA.md §2.

Vía elegida: `youtube-transcript-api` — toma los subtítulos que YouTube ya generó
(auto-captions con timestamps). Reemplaza la descarga de audio (yt-dlp, bloqueado
por DRM/PO-tokens en este entorno) y el STT local (faster-whisper/av, cuya DLL
bloquea el Control de Aplicaciones de Windows). YouTube ya transcribió; QUIRA lo
audita. Limitación: sin diarización (en una RDC habla casi siempre la autoridad).

Salida: data/motor_narrativo/{video_id}/transcripcion.json (segmentos + texto).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import identidad as _id

_LANGS = ["es", "es-ES", "es-419"]


def _segmentos(video_id: str) -> list[dict]:
    from youtube_transcript_api import YouTubeTranscriptApi
    try:                                             # API nueva (>=1.0)
        api = YouTubeTranscriptApi()
        f = api.fetch(video_id, languages=_LANGS)
        raw = f.to_raw_data() if hasattr(f, "to_raw_data") else list(f)
    except Exception:                                # API antigua
        raw = YouTubeTranscriptApi.get_transcript(video_id, languages=_LANGS)
    out = []
    for s in raw:
        t = s["start"] if isinstance(s, dict) else s.start
        txt = s["text"] if isinstance(s, dict) else s.text
        txt = " ".join(str(txt).split())
        if txt and txt not in ("[Música]", "[Aplausos]"):
            out.append({"t": round(float(t), 1), "texto": txt})
    return out


def transcribir(video_id: str) -> dict:
    segs = _segmentos(video_id)
    dur = (segs[-1]["t"] if segs else 0)
    trans = {
        "video_id": video_id,
        "fuente": "youtube-transcript-api (auto-captions de YouTube)",
        "n_segmentos": len(segs),
        "duracion_seg": dur,
        "palabras": sum(len(s["texto"].split()) for s in segs),
        "segmentos": segs,
        "texto_completo": " ".join(s["texto"] for s in segs),
    }
    d = _id.BASE / video_id
    d.mkdir(parents=True, exist_ok=True)
    (d / "transcripcion.json").write_text(json.dumps(trans, ensure_ascii=False, indent=2), encoding="utf-8")
    # completar la identidad con la duración
    ident = _id.cargar(video_id)
    if ident:
        ident["duracion_seg"] = dur
        (d / "identidad.json").write_text(json.dumps(ident, ensure_ascii=False, indent=2), encoding="utf-8")
    return trans


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    if not _id.cargar(vid):
        _id.registrar(**_id.PILOTO[año])
    tr = transcribir(vid)
    m = int(tr["duracion_seg"] // 60)
    print(f"TRANSCRIPCIÓN · {año} ({vid}): {tr['n_segmentos']} segmentos · {tr['palabras']:,} palabras · ~{m} min")
    print(f"   {_id.BASE / vid / 'transcripcion.json'}")
    print("   muestra:", " ".join(s["texto"] for s in tr["segmentos"][:8])[:150])
