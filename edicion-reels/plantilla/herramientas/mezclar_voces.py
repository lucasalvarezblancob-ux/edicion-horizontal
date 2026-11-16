"""Audio limpio para brutos con ruido de fondo y varias personas hablando.

Mezcla la voz aislada (ElevenLabs Voice Isolator, `estudio/scripts/aislar-voz.mjs`) con un poco del audio
original SOLO mientras habla alguien (ventanas sacadas de las palabras de Scribe). Fuera de esas ventanas: silencio
(se va el ambiente y la gente de fondo). En las frases que el aislador debilita (voces lejanas: pierde > --umbral dB
respecto al original) se sube la parte del original para que no desaparezcan. Resultado normalizado a −14 LUFS,
misma duración y tiempos que el original.

Uso:
  herramientas/.venv/bin/python herramientas/mezclar_voces.py ORIGINAL AISLADO PALABRAS.json SALIDA.wav \
      [--hablantes speaker_0,speaker_1] [--orig 0.3] [--orig-debil 0.8] [--umbral 4] [--margen 0.12]
"""
import argparse, json, subprocess
import numpy as np
import soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("original"); ap.add_argument("aislado"); ap.add_argument("palabras"); ap.add_argument("salida")
ap.add_argument("--hablantes", default="", help="lista separada por comas; vacío = todos")
ap.add_argument("--orig", type=float, default=0.3, help="cuánto original se mezcla mientras hablan")
ap.add_argument("--orig-debil", type=float, default=0.8, help="original en frases que el aislador debilita")
ap.add_argument("--umbral", type=float, default=4.0, help="dB perdidos para considerar una frase debilitada")
ap.add_argument("--margen", type=float, default=0.12, help="s de aire antes/después de cada frase")
ap.add_argument("--fundido", type=float, default=0.06)
a = ap.parse_args()

SR = 48000
def carga(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()
o, s = carga(a.original), carga(a.aislado)
n = min(len(o), len(s)); o, s = o[:n], s[:n]

pal = json.load(open(a.palabras))
quien = set(filter(None, a.hablantes.split(",")))
pal = [p for p in pal if not quien or p.get("hablante") in quien]

# frases: palabras seguidas con huecos < 0.35 s
frases = []
for p in pal:
    if frases and p["start"] - frases[-1][1] < 0.35:
        frases[-1][1] = max(frases[-1][1], p["end"])
    else:
        frases.append([p["start"], p["end"]])

db = lambda x: 10 * np.log10(np.mean(x ** 2) + 1e-12)
voz = np.zeros(n, np.float32)      # 1 dentro de una frase
gan_o = np.zeros(n, np.float32)    # cuánto original
for t0, t1 in frases:
    i0, i1 = int(max(0, t0 - a.margen) * SR), int(min(n / SR, t1 + a.margen) * SR)
    i1 = max(i1, i0 + int(0.1 * SR))
    perdida = db(o[i0:i1]) - db(s[i0:i1])
    voz[i0:i1] = 1
    gan_o[i0:i1] = np.maximum(gan_o[i0:i1], a.orig_debil if perdida > a.umbral else a.orig)

# fundidos suaves en los bordes (media móvil)
k = max(1, int(a.fundido * SR))
suave = lambda x: np.convolve(x, np.ones(k) / k, mode="same").astype(np.float32)
voz, gan_o = suave(voz), suave(gan_o)
mezcla = voz * s + gan_o * o

tmp = a.salida + ".tmp.wav"
sf.write(tmp, mezcla, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), a.salida], check=True)
subprocess.run(["rm", tmp])
debiles = sum(1 for t0, t1 in frases if db(o[int(t0*SR):int(t1*SR)+1]) - db(s[int(t0*SR):int(t1*SR)+1]) > a.umbral)
print(f"{len(frases)} frases ({debiles} reforzadas con original) -> {a.salida}")
