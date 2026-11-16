#!/usr/bin/env python3
"""Transcribe con faster-whisper (local; usa la gráfica NVIDIA si hay, si no CPU).

Uso: transcribir.py MEDIA SALIDA.json [--idioma auto|es|en] (por defecto auto: detecta el idioma; nunca forzarlo sin comprobar) [--modelo large-v3-turbo]
Escribe frases con su confianza (avg_logprob, no_speech_prob) y palabras con tiempo y probabilidad,
más SALIDA.txt con una línea por frase ([mm:ss.s] texto) para leer rápido.
La confianza por frase/palabra es la base de tramos_ruidosos.py (subtítulos solo donde se oye mal).
"""
import argparse, json, os, subprocess, sys
import numpy as np
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("media"); ap.add_argument("salida")
ap.add_argument("--idioma", default="auto"); ap.add_argument("--modelo", default="large-v3-turbo")
a = ap.parse_args()

disp, tipo = "cpu", "int8"
try:                                   # las DLL de CUDA vienen con torch: se las prestamos a ctranslate2
    import torch
    if torch.cuda.is_available():
        lib = Path(torch.__file__).parent / "lib"
        if os.name == "nt":
            os.add_dll_directory(str(lib)); os.environ["PATH"] = str(lib) + os.pathsep + os.environ["PATH"]
        disp, tipo = "cuda", "float16"
except Exception:
    pass
from faster_whisper import WhisperModel

try:
    m = WhisperModel(a.modelo, device=disp, compute_type=tipo)
except Exception as e:
    print("sin GPU:", e, file=sys.stderr); disp = "cpu"
    m = WhisperModel(a.modelo, device="cpu", compute_type="int8")
# el audio lo decodifica ffmpeg (16 kHz mono): evita depender de la versión de PyAV
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", a.media, "-ar", "16000", "-ac", "1", "-f", "f32le", "-"],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
segs, info = m.transcribe(audio, language=None if a.idioma == "auto" else a.idioma, word_timestamps=True,
                          vad_filter=True, vad_parameters={"min_silence_duration_ms": 400},
                          condition_on_previous_text=False)
frases = []
for s in segs:
    frases.append({"desde": round(s.start, 2), "hasta": round(s.end, 2), "texto": s.text.strip(),
                   "avg_logprob": round(s.avg_logprob, 3), "no_speech_prob": round(s.no_speech_prob, 3),
                   "palabras": [{"t": round(w.start, 2), "fin": round(w.end, 2), "p": w.word.strip(), "prob": round(w.probability, 2)}
                                for w in (s.words or [])]})
sal = Path(a.salida); sal.parent.mkdir(parents=True, exist_ok=True)
sal.write_text(json.dumps({"media": a.media, "idioma": info.language, "duracion": round(info.duration, 2),
                           "dispositivo": disp, "modelo": a.modelo, "frases": frases}, ensure_ascii=False), encoding="utf-8")
sal.with_suffix(".txt").write_text("\n".join(f'[{int(f["desde"]//60):02d}:{f["desde"]%60:04.1f}] {f["texto"]}' for f in frases), encoding="utf-8")
print(f"{len(frases)} frases, {sum(len(f['palabras']) for f in frases)} palabras, {disp}, {sal}")
