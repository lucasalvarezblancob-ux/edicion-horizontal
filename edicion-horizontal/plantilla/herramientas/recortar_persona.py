"""Recorta a la persona fotograma a fotograma (máscara) para poner texto DETRÁS del sujeto.

Uso:
  herramientas/.venv/bin/python herramientas/recortar_persona.py VIDEO CARPETA_SALIDA [--ancho 540] [--desde s] [--hasta s]
Escribe CARPETA_SALIDA/f00000.png … (RGBA: la persona con fondo transparente, al tamaño --ancho).
En Remotion: encima del texto, <Img src={staticFile(`<slug>/persona/f${pad(frame)}.png`)} /> escalado a 1080.
Modelo: rembg u2net_human_seg (CPU, ~0,2–0,5 s por frame).
"""
import argparse, os
import cv2
import numpy as np
from rembg import new_session, remove

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("salida")
ap.add_argument("--ancho", type=int, default=540)
ap.add_argument("--desde", type=float, default=0); ap.add_argument("--hasta", type=float, default=1e9)
a = ap.parse_args()
os.makedirs(a.salida, exist_ok=True)
ses = new_session("u2net_human_seg")
cap = cv2.VideoCapture(a.video)
fps = cap.get(cv2.CAP_PROP_FPS)
i = 0
while True:
    ok, fr = cap.read()
    if not ok:
        break
    t = i / fps
    if a.desde <= t <= a.hasta:
        h, w = fr.shape[:2]
        fr = cv2.resize(fr, (a.ancho, int(h * a.ancho / w)))
        rgba = remove(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB), session=ses, post_process_mask=True)
        cv2.imwrite(os.path.join(a.salida, f"f{i:05d}.png"), cv2.cvtColor(np.asarray(rgba), cv2.COLOR_RGBA2BGRA))
    i += 1
    if i % 60 == 0:
        print(f"{i} frames", flush=True)
print("listo", i, "frames")
