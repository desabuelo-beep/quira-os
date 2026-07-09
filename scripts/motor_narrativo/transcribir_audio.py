# -*- coding: utf-8 -*-
"""
Motor Narrativo — TRANSCRIPCIÓN DE AUDIO (audiovisual → texto · escalable).
Dylus Lab © 2026 · doctrina PCD-MN01. El diferenciador NLP debe funcionar para
CUALQUIER autoridad (alcalde → presidente), no de forma manual.

Arquitectura pluggable, a prueba de DRM:
  ENTRADA:  (a) un ARCHIVO local de audio/video (mp3/mp4/wav/m4a…) — a prueba de DRM,
            (b) una URL de YouTube — descarga automática (yt-dlp, multi-cliente) cuando
                el video NO está protegido.
  MOTOR:    openai-whisper (local, CPU) decodificando con ffmpeg PORTÁTIL
            (`imageio-ffmpeg`) — esquiva la DLL `av` que Windows Application Control
            bloquea (por eso falla faster-whisper). Sin dependencia del PATH del sistema.
  SALIDA:   transcript.json {segmentos:[{t, texto}], texto} — mismo formato que la vía
            de subtítulos, para que `unidades.py` lo consuma igual.

Escala a la nube: cambiar `_whisper_local` por una API STT (Groq/OpenAI) sin tocar el
resto. El motor nunca sabe de dónde vino el texto.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

_SR = 16000
_MODELO = "base"  # base ~140MB · multilingüe · CPU. Subir a "small"/"medium" si hace falta.


def _ffmpeg() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def _cargar_audio(path: str, sr: int = _SR) -> np.ndarray:
    """Decodifica cualquier audio/video a PCM mono 16k con el ffmpeg PORTÁTIL (no la DLL)."""
    cmd = [_ffmpeg(), "-nostdin", "-threads", "0", "-i", str(path),
           "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr), "-"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(out, np.int16).astype(np.float32) / 32768.0


def descargar_audio(url: str, destino: Path) -> Path | None:
    """Descarga el bestaudio de una URL (yt-dlp multi-cliente). None si está protegido (DRM)."""
    import yt_dlp
    salida = destino / "audio_fuente.%(ext)s"
    opts = {"format": "bestaudio/best", "outtmpl": str(salida), "quiet": True,
            "no_warnings": True, "noplaylist": True,
            "extractor_args": {"youtube": {"player_client": ["tv", "web_safari", "ios", "mweb", "web"]}}}
    try:
        with yt_dlp.YoutubeDL(opts) as y:
            info = y.extract_info(url, download=True)
            return Path(y.prepare_filename(info))
    except Exception as e:
        print(f"  ⚠ descarga automática no disponible ({str(e)[:70]}). Usa un ARCHIVO local.")
        return None


def transcribir_archivo(path: str, modelo: str = _MODELO, idioma: str = "es") -> dict:
    """Archivo de audio/video → {segmentos:[{t,texto}], texto}. Motor: Whisper local."""
    import whisper
    audio = _cargar_audio(path)
    m = whisper.load_model(modelo)
    r = m.transcribe(audio, language=idioma, fp16=False, verbose=False)
    segs = [{"t": round(s["start"], 1), "texto": s["text"].strip()} for s in r.get("segments", [])]
    return {"segmentos": segs, "texto": r.get("text", "").strip(), "motor": f"whisper-{modelo}"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python transcribir_audio.py <archivo|url|año> [modelo]")
        sys.exit(1)
    arg = sys.argv[1]
    modelo = sys.argv[2] if len(sys.argv) > 2 else _MODELO
    import identidad as _id

    if arg in _id.PILOTO:  # año del PILOTO → resuelve URL y guarda en el dir del video
        vid = _id._video_id(_id.PILOTO[arg]["url"])
        outdir = _id.BASE / vid
        outdir.mkdir(parents=True, exist_ok=True)
        fuente = descargar_audio(_id.PILOTO[arg]["url"], outdir)
        if not fuente:
            print(f"  → El video {arg} está protegido. Coloca el archivo de audio/video en:\n     {outdir}\\audio_fuente.*\n     y corre: python transcribir_audio.py \"<ruta_del_archivo>\" [modelo]  (se guardará el transcript)")
            sys.exit(2)
        tr = transcribir_archivo(str(fuente), modelo)
        (outdir / "transcript.json").write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"transcript.json guardado · {len(tr['segmentos'])} segmentos · {outdir}")
    else:  # ruta de archivo local
        p = Path(arg)
        tr = transcribir_archivo(str(p), modelo)
        out = p.with_suffix(".transcript.json")
        out.write_text(json.dumps(tr, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"TRANSCRIPCIÓN ({tr['motor']}) · {len(tr['segmentos'])} segmentos → {out}")
        print("  primeros 300 chars:", tr["texto"][:300])
