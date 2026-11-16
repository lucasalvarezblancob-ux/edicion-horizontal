"""Sigue la cara fotograma a fotograma (para centrar zooms en la cara y para
textos que siguen la cabeza).

Uso:
  herramientas/.venv/bin/python herramientas/seguir_cara.py VIDEO SALIDA.json [--fps 30]
Salida: {"ancho":W,"alto":H,"fps":f,"caras":[[cx,cy,w,h] por frame, en px del vídeo]}
(suavizado; si un frame no detecta cara, se interpola).
"""
import argparse, json
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("salida")
a = ap.parse_args()

cap = cv2.VideoCapture(a.video)
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
esc = 480 / W
caras = []
prev = None
while True:
    ok, fr = cap.read()
    if not ok:
        break
    g = cv2.cvtColor(cv2.resize(fr, None, fx=esc, fy=esc), cv2.COLOR_BGR2GRAY)
    det = casc.detectMultiScale(g, 1.1, 5, minSize=(40, 40))
    if len(det):
        # la más grande / la más cercana a la anterior
        cand = [(x + w / 2, y + h / 2, w, h) for x, y, w, h in det]
        if prev is not None:
            cand.sort(key=lambda c: (c[0] - prev[0]) ** 2 + (c[1] - prev[1]) ** 2)
        else:
            cand.sort(key=lambda c: -c[2])
        c = cand[0]
        prev = c
        caras.append([v / esc for v in c])
    else:
        caras.append(None)
n = len(caras)
arr = np.full((n, 4), np.nan)
for i, c in enumerate(caras):
    if c:
        arr[i] = c
for k in range(4):
    col = arr[:, k]; ok = ~np.isnan(col)
    arr[:, k] = np.interp(np.arange(n), np.flatnonzero(ok), col[ok])
# suavizado (media móvil de 7 frames)
ker = np.ones(7) / 7
sm = np.vstack([np.convolve(np.pad(arr[:, k], 3, mode="edge"), ker, mode="valid") for k in range(4)]).T
json.dump({"ancho": W, "alto": H, "fps": fps, "caras": np.round(sm, 1).tolist()}, open(a.salida, "w"))
det = sum(c is not None for c in caras)
print(f"{n} frames, cara detectada en {det} ({100*det/n:.0f} %). Media: cx={sm[:,0].mean():.0f} cy={sm[:,1].mean():.0f} w={sm[:,2].mean():.0f}")
