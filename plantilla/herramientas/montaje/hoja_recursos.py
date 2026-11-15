"""hoja_recursos.py: hoja de contactos de TODOS los planos de recurso del montaje, con su escala y encuadre aplicados
(3 fotogramas de cada uno: 10 %, 50 % y 90 %) -> trabajo/recursos_N.jpg.
OBLIGATORIO mirarlas antes de renderizar: un recurso sobre la voz tiene que enseñar aquello de lo que se habla, desde el
primer fotograma. Si se ve una pared, un barrido o el sujeto muy pequeño, cambia el tramo (tira.py) o ponle zoom al sujeto."""
import subprocess
import numpy as np, cv2
from comun import ALTO, ANCHO, FPS, TRABAJO, fuente, video
from dinamica import encuadre

g = []      # un recurso = planos seguidos del mismo tramo de bruto (un recurso largo va partido en dos escalas)
for v in video():
    if not v["b"]: continue
    if g and g[-1][-1]["clip"] == v["clip"] and g[-1][-1]["o"] + g[-1][-1]["n"] == v["o"] and g[-1][-1]["in"] + g[-1][-1]["n"] == v["in"]: g[-1].append(v)
    else: g.append([v])
w = 480; h = 2 * round(w * ALTO / ANCHO / 2); filas = []
for i, pl in enumerate(g):
    fila = []; o0 = pl[0]["o"]; n = sum(v["n"] for v in pl)
    for fr in (0.1, 0.5, 0.9):
        f = o0 + int(n * fr); v = next(v for v in pl if v["o"] <= f < v["o"] + v["n"]); t = (v["in"] + f - v["o"]) / FPS
        W2, H2, x, y = encuadre(v["z1"], v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", 0.5))
        ent, pre = fuente(v["clip"], t)
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y},scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        fila.append(np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy() if len(raw) == w * h * 3 else np.zeros((h, w, 3), np.uint8))
    im = np.hstack(fila); s = o0 / FPS; v = pl[0]
    esc = "/".join("%g" % p["z1"] for p in pl)
    txt = f"{i} {v['clip']} {v['in'] / FPS:.0f}s  dur {n / FPS:.1f}s  x{esc}  sale en {int(s // 60)}:{int(s % 60):02d}"
    cv2.rectangle(im, (0, 0), (700, 30), (0, 0, 0), -1); cv2.putText(im, txt, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 240, 240), 2)
    filas.append(im)
for k in range(0, len(filas), 9): cv2.imwrite(f"{TRABAJO}/recursos_{k // 9 + 1}.jpg", np.vstack(filas[k:k + 9]), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(len(g), "recursos ->", ", ".join(f"{TRABAJO}/recursos_{k // 9 + 1}.jpg" for k in range(0, len(filas), 9)))
