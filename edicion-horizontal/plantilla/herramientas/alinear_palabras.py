"""Alineación forzada palabra a palabra (sin Scribe): coloca cada palabra de un texto YA CONOCIDO sobre el audio con
wav2vec2 multilingüe (torchaudio MMS_FA). Mucho más preciso que los tiempos de Whisper local (que desfasan 0,3–0,7 s).

Uso: herramientas/.venv/bin/python herramientas/alinear_palabras.py VOZ.wav PALABRAS.json SALIDA.json
  PALABRAS.json: lista [{w, start, end}] (p. ej. "palabras" de montaje.json) o {"palabras": [...]}; solo se usa el TEXTO y el orden.
  SALIDA.json: misma lista con start/end alineados (s, en el tiempo de VOZ.wav) + "dif" = start nuevo − start viejo.
Necesita torch + torchaudio (CPU): pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
(2026-11-11, lagarto-caiman-nido: "el timing audio–letras tiene que ser más perfecto")
"""
import json, re, sys, unicodedata
import numpy as np, soundfile as sf, torch, torchaudio
sys.stdout.reconfigure(encoding="utf-8")
NUM = {"0": "cero", "1": "uno", "2": "dos", "3": "tres", "4": "cuatro", "5": "cinco", "6": "seis", "7": "siete", "8": "ocho", "9": "nueve", "10": "diez"}
def norm(w):
    w = NUM.get(re.sub(r"[^\w]", "", w), w).lower()
    w = unicodedata.normalize("NFD", w); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z']", "", w)
voz, pal_f, out_f = sys.argv[1:4]
pal = json.load(open(pal_f, encoding="utf-8")); pal = pal["palabras"] if isinstance(pal, dict) else pal
y, sr = sf.read(voz, dtype="float32")
if y.ndim > 1: y = y.mean(1)
wav = torchaudio.functional.resample(torch.from_numpy(y)[None], sr, 16000)
b = torchaudio.pipelines.MMS_FA
model, tok, aligner = b.get_model(with_star=False), b.get_tokenizer(), b.get_aligner()
textos = [norm(p["w"]) for p in pal]
assert all(textos), [p["w"] for p, t in zip(pal, textos) if not t]
with torch.inference_mode():
    em, _ = model(wav)
spans = aligner(em[0], tok(textos))
k = wav.shape[1] / em.shape[1] / 16000
out = []
for p, sp in zip(pal, spans):
    s, e = sp[0].start * k, sp[-1].end * k
    out.append({"w": p["w"], "start": round(s, 3), "end": round(e, 3), "dif": round(s - p["start"], 3)})
json.dump(out, open(out_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
d = np.array([o["dif"] for o in out])
print(f"{len(out)} palabras alineadas. Desfase Whisper→alineado: medio {np.mean(np.abs(d))*1000:.0f} ms, máx {np.max(np.abs(d))*1000:.0f} ms")
for o in out:
    if abs(o["dif"]) > 0.1: print(f"  {o['w']:<14} {o['start']:6.2f}  ({o['dif']*1000:+.0f} ms)")
