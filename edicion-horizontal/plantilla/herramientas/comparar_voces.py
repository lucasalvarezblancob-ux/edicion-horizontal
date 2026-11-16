"""Compara voces candidatas con una voz de referencia (tono, entonación, timbre, duración).

Para que sea justo, genera con cada candidata EL MISMO TEXTO que dice la referencia
y recorta la referencia a ese tramo.

Uso:
  herramientas/.venv/bin/python herramientas/comparar_voces.py REF.wav CAND1.mp3 CAND2.mp3 ...
Menor puntuación = más parecida.
  f0   = tono medio (Hz). Hombre ~85-155, mujer ~165-255.
  sd   = variación de entonación (semitonos). Bajo = plano/monótono.
  timbre = distancia de MFCC (color de la voz).
  dur  = duración sin silencios de los extremos (velocidad, si el texto es el mismo).
"""
import sys, os, warnings
import numpy as np, librosa

warnings.filterwarnings("ignore")


def feats(p):
    y, sr = librosa.load(p, sr=16000, mono=True)
    y, _ = librosa.effects.trim(y, top_db=35)
    rms = librosa.feature.rms(y=y)[0]
    k = rms > np.percentile(rms, 40)
    f0, v, _ = librosa.pyin(y, fmin=60, fmax=400, sr=sr, frame_length=1024)
    x = f0[v]
    m = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)[:, k].mean(axis=1)
    return dict(f0=float(np.median(x)), sd=float(np.std(12 * np.log2(x / np.median(x)))),
                mfcc=m, dur=len(y) / sr)


ref = feats(sys.argv[1])
print(f"REF  f0={ref['f0']:.0f} sd={ref['sd']:.1f} dur={ref['dur']:.2f}s")
rows = []
for p in sys.argv[2:]:
    f = feats(p)
    timbre = float(np.linalg.norm(f["mfcc"][1:] - ref["mfcc"][1:]))
    score = (timbre / 10) ** 2 + (12 * np.log2(f["f0"] / ref["f0"]) / 2) ** 2 + (f["sd"] - ref["sd"]) ** 2
    rows.append((score, os.path.basename(p), f, timbre))
for s, n, f, t in sorted(rows, key=lambda r: r[0]):
    print(f"{s:6.2f} {n:32s} f0={f['f0']:.0f} sd={f['sd']:.1f} timbre={t:.1f} dur={f['dur']:.2f}s "
          f"(x{f['dur'] / ref['dur']:.2f} vs ref)")
