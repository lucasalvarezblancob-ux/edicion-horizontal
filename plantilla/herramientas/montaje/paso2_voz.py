"""Paso 2: monta el audio de la línea (48 kHz estéreo) tal como queda cortado -> trabajo/voz.wav.
Luego comprobar_voz.py lo vuelve a transcribir y dice si se oye lo que se quería (palabras comidas o repetidas en los cortes)."""
import json, os, subprocess, numpy as np, soundfile as sf
from comun import FPS, TRABAJO, bruto
L = json.load(open(f"{TRABAJO}/linea.json")); SR = 48000
cache = {}
def wav(c):
    if c not in cache:
        p = f"{TRABAJO}/{c}.48k.wav"
        if not os.path.exists(p): subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", bruto(c), "-ac", "2", "-ar", str(SR), p], check=True)
        cache[c] = sf.read(p, dtype="float32")[0]
    return cache[c]
out = np.zeros((L["total"] * SR // FPS, 2), dtype="float32"); f = int(0.008 * SR); r = np.linspace(0, 1, f)[:, None]
for p in L["piezas"]:
    if p["speed"] != 1 or p["vol"] == 0: continue   # planos acelerados o con vol=0 (una intro muda): sin sonido original
    y = wav(p["clip"]); a = p["in"] * SR // FPS; n = p["n"] * SR // FPS
    s = y[a:a + n].copy() * p["vol"]; s[:f] *= r; s[-f:] *= r[::-1]     # fundido de 8 ms en cada borde: sin clics
    o = p["o"] * SR // FPS; out[o:o + len(s)] += s
sf.write(f"{TRABAJO}/voz.wav", out, SR); print(f"voz.wav {len(out) / SR:.1f} s")
