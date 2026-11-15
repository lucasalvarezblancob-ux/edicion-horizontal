#!/usr/bin/env python3
"""Mide el zoom/movimiento de cámara virtual dentro de un plano (punch-ins, zooms lentos, paneos).

Uso: medir_zoom.py VIDEO INICIO FIN [--paso 0.1]
Compara cada fotograma con el primero del tramo (puntos ORB + transformación afín parcial) e imprime
la escala acumulada y el desplazamiento. Escala 1.08 = 8 % de zoom de entrada. Úsalo DENTRO de un plano
(entre dos cortes); si el tramo cruza un corte el resultado no vale.
Salida JSON: escala_final, duracion, velocidad (% por segundo), tipo (fijo | zoom lento | punch-in | paneo).
"""
import argparse, json, subprocess
import numpy as np, cv2

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("ini", type=float); ap.add_argument("fin", type=float)
ap.add_argument("--paso", type=float, default=0.1)
a = ap.parse_args()
W, H = 640, 360
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a.ini), "-t", str(a.fin - a.ini), "-i", a.video,
                      "-vf", f"fps={1 / a.paso},scale={W}:{H}", "-pix_fmt", "gray", "-f", "rawvideo", "-"],
                     check=True, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W)
orb = cv2.ORB_create(1500); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
esc, dx, dy = [1.0], [0.0], [0.0]
for i in range(1, len(fr)):                       # encadenado fotograma a fotograma (aguanta mejor el movimiento)
    k1, d1 = orb.detectAndCompute(fr[i - 1], None); k2, d2 = orb.detectAndCompute(fr[i], None)
    s, tx, ty = 1.0, 0.0, 0.0
    if d1 is not None and d2 is not None and len(k1) > 20 and len(k2) > 20:
        m = bf.match(d1, d2)
        if len(m) > 15:
            p1 = np.float32([k1[x.queryIdx].pt for x in m]); p2 = np.float32([k2[x.trainIdx].pt for x in m])
            M, _ = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=2)
            if M is not None:
                s = float(np.hypot(M[0, 0], M[0, 1])); tx, ty = float(M[0, 2]), float(M[1, 2])
    esc.append(esc[-1] * s); dx.append(dx[-1] + tx / W); dy.append(dy[-1] + ty / H)
esc = np.array(esc); dur = (len(fr) - 1) * a.paso
paso_max = float(np.max(np.abs(np.diff(esc)))) if len(esc) > 1 else 0
total = float(esc[-1] - 1)
if abs(total) < 0.015 and abs(dx[-1]) < 0.03 and abs(dy[-1]) < 0.03: tipo = "fijo"
elif paso_max > 0.04: tipo = "punch-in/out (salto)"
elif abs(total) >= 0.015: tipo = "zoom lento" if abs(total) / max(dur, 0.1) < 0.05 else "zoom rápido"
else: tipo = "paneo/movimiento"
print(json.dumps({"ini": a.ini, "fin": a.fin, "duracion": round(dur, 2), "escala_final": round(float(esc[-1]), 3),
                  "escala_max": round(float(esc.max()), 3), "escala_min": round(float(esc.min()), 3),
                  "pct_por_segundo": round(total * 100 / max(dur, 0.1), 2), "salto_max_entre_muestras": round(paso_max, 3),
                  "desplazamiento_x": round(dx[-1], 3), "desplazamiento_y": round(dy[-1], 3), "tipo": tipo,
                  "curva": [round(float(e), 3) for e in esc[::max(1, len(esc) // 20)]]}, ensure_ascii=False))
