"""Quita los silencios de la voz (sin comerse letras) y la acelera sin cambiar el tono.
Uso: python apretar_voz.py entrada.mp3 entrada-palabras.json salida.mp3 salida-palabras.json [tempo]

Los cortes se hacen donde el audio es silencio real (medido por energía), no en las
marcas de tiempo de ElevenLabs, que a veces terminan antes de la última consonante.
"""
import json, subprocess, sys, tempfile, os
import numpy as np, soundfile as sf, librosa

src, words_in, out, words_out = sys.argv[1:5]
TEMPO = float(sys.argv[5]) if len(sys.argv) > 5 else 1.14
# Se pueden cambiar con variables de entorno (APRETAR_HUECO, APRETAR_MARGEN, APRETAR_TOPDB).
# 2026-11-05 (fisico-redes): con la voz REAL de Lucas los valores por defecto (pensados para la voz IA) "traban el final de
# las palabras" → para su voz: APRETAR_HUECO=0.14 APRETAR_MARGEN=0.15 APRETAR_TOPDB=45 y tempo 1.0.
KEEP_GAP = float(os.environ.get("APRETAR_HUECO", 0.07))   # silencio que se deja entre frases (s)
MARGIN = float(os.environ.get("APRETAR_MARGEN", 0.06))    # margen de audio que se conserva a cada lado del sonido
TOP_DB = float(os.environ.get("APRETAR_TOPDB", 38))       # umbral de silencio respecto al pico
MIN_GAP = max(0.12, 2 * MARGIN + 0.02)    # solo se recortan silencios más largos que esto

y, sr = librosa.load(src, sr=44100, mono=True)
words = json.load(open(words_in))

# Tramos con sonido, con margen generoso para no cortar colas de consonantes
iv = librosa.effects.split(y, top_db=TOP_DB, frame_length=1024, hop_length=128) / sr
blocks = []
for s, e in iv:
    s, e = max(0.0, s - MARGIN), min(len(y) / sr, e + MARGIN)
    if blocks and s - blocks[-1][1] < MIN_GAP:
        blocks[-1][1] = e
    else:
        blocks.append([s, e])

fade = int(0.012 * sr)
pieces, mapping, t_out = [], [], 0.0
for i, (s, e) in enumerate(blocks):
    seg = y[int(s * sr):int(e * sr)].copy()
    seg[:fade] *= np.linspace(0, 1, fade)
    seg[-fade:] *= np.linspace(1, 0, fade)
    mapping.append((s, e, t_out))
    pieces.append(seg)
    t_out += len(seg) / sr
    if i < len(blocks) - 1:
        pieces.append(np.zeros(int(KEEP_GAP * sr)))
        t_out += KEEP_GAP
audio = np.concatenate(pieces)


def remap(t):
    for s, e, o in mapping:
        if s <= t <= e:
            return (o + t - s) / TEMPO
    # dentro de un silencio recortado: se pega al siguiente bloque
    nxt = [m for m in mapping if m[0] > t]
    return (nxt[0][2] if nxt else t_out) / TEMPO


tmp = tempfile.mktemp(suffix=".wav")
sf.write(tmp, audio, sr)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                f"atempo={TEMPO},loudnorm=I=-14:TP=-1.5", "-ar", "44100", "-b:a", "192k", out],
               check=True)
os.remove(tmp)
new = [{"w": w["w"], "start": round(remap(w["start"]), 3), "end": round(remap(w["end"]), 3)}
       for w in words]
json.dump(new, open(words_out, "w"), ensure_ascii=False, indent=1)
print(f"original {len(y)/sr:.2f}s -> {len(audio)/sr/TEMPO:.2f}s, {len(blocks)} bloques")
