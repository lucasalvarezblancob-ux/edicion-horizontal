"""Encuentra los puntos donde el movimiento se para (arriba/abajo de cada rep).

Sirve para cortar entre ángulos justo en los extremos del ejercicio (match cut):
en esos instantes la barra/el cuerpo está casi quieto y el cambio de plano casa.

Uso:
  herramientas/.venv/bin/python herramientas/puntos_movimiento.py VIDEO INICIO_S FIN_S [--zona 0.6]
    --zona: fracción superior del encuadre que se analiza (0.6 = 60% de arriba, donde
            están brazos y barra). Usa 1.0 para el encuadre entero.

Imprime la energía de movimiento cada 0,1 s y la lista de mínimos (= paradas).
Luego confirma visualmente con herramientas/hoja_contactos.sh en ese tramo.
"""
import argparse, subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("inicio", type=float); ap.add_argument("fin", type=float)
ap.add_argument("--zona", type=float, default=0.6)
ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()

W, H = 72, 128
raw = subprocess.run(
    ["ffmpeg", "-v", "error", "-ss", str(a.inicio), "-t", str(a.fin - a.inicio), "-i", a.video,
     "-vf", f"fps={a.fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
    capture_output=True, check=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(float)[:, : int(H * a.zona), :]
d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
d = np.convolve(d, np.ones(5) / 5, mode="same")
t = a.inicio + (np.arange(len(d)) + 1) / a.fps

print("energía de movimiento (t: valor) — valores bajos = quieto")
row = []
for i in range(0, len(d), 3):
    row.append(f"{t[i]:6.1f}:{d[i]:4.1f}")
    if len(row) == 10:
        print(" ".join(row)); row = []
if row:
    print(" ".join(row))
k = 3
mins = [i for i in range(k, len(d) - k) if d[i] == d[i - k:i + k + 1].min()]
print("\nparadas (t, energía, frame a 30fps):")
for i in mins:
    print(f"  {t[i]:.2f}s  {d[i]:.1f}  f{round(t[i] * 30)}")
