"""hoja_recursos.py: hoja de contactos de TODOS los planos de recurso del montaje, con su escala y encuadre aplicados
(3 fotogramas de cada uno: 10 %, 50 % y 90 %) -> trabajo/recursos_N.jpg.
OBLIGATORIO mirarlas antes de renderizar: un recurso sobre la voz tiene que enseñar aquello de lo que se habla, desde el
primer fotograma. Si se ve una pared, un barrido o el sujeto muy pequeño, cambia el tramo (tira.py) o ponle zoom al sujeto."""
import subprocess
import numpy as np, cv2
from comun import ALTO, ANCHO, FPS, TRABAJO, fuente, video
from dinamica import RECORTE_169, encuadre

# ---- proporción: un recurso que no es 16:9 (stock DCI 4096x2160, vertical) se recorta al centro (dinamica.RECORTE_169) ----
# vaciamos-estanque-2 (2026-11-19): de 14 clips de Shutterstock, 4 en 4096x2160 y 1 vertical. En un vertical el centro casi
# nunca es el sujeto: mejor una copia _h recortada a mano a su altura (base/recursos.md § 5 bis).
import json as _j
from comun import bruto as _bruto
for _c in sorted({v["clip"] for v in video() if v["b"]}):
    try:
        _s = _j.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation:stream_tags=rotate",
                                      "-of", "json", _bruto(_c)], capture_output=True, text=True).stdout)["streams"][0]
    except (Exception, SystemExit): continue
    _w, _h = _s["width"], _s["height"]
    _rot = abs(int(float(_s.get("tags", {}).get("rotate", 0) or next((d.get("rotation", 0) for d in _s.get("side_data_list", []) if "rotation" in d), 0))))
    if _rot in (90, 270): _w, _h = _h, _w
    if _h > _w: print(f"AVISO PROPORCIÓN: {_c} es VERTICAL ({_w}x{_h}): se recorta al centro; mejor una copia _h recortada a la altura del sujeto")
    elif abs(_w / _h - ANCHO / ALTO) > 0.01 * ANCHO / ALTO: print(f"AVISO PROPORCIÓN: {_c} es {_w}x{_h}: se recorta al centro a 16:9")

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
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}{RECORTE_169}scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y},scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        fila.append(np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy() if len(raw) == w * h * 3 else np.zeros((h, w, 3), np.uint8))
    im = np.hstack(fila); s = o0 / FPS; v = pl[0]
    esc = "/".join("%g" % p["z1"] for p in pl)
    txt = f"{i} {v['clip']} {v['in'] / FPS:.0f}s  dur {n / FPS:.1f}s  x{esc}  sale en {int(s // 60)}:{int(s % 60):02d}"
    cv2.rectangle(im, (0, 0), (700, 30), (0, 0, 0), -1); cv2.putText(im, txt, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 240, 240), 2)
    filas.append(im)
for k in range(0, len(filas), 9): cv2.imwrite(f"{TRABAJO}/recursos_{k // 9 + 1}.jpg", np.vstack(filas[k:k + 9]), [cv2.IMWRITE_JPEG_QUALITY, 80])
print(len(g), "recursos ->", ", ".join(f"{TRABAJO}/recursos_{k // 9 + 1}.jpg" for k in range(0, len(filas), 9)))

# ---- el tráiler, plano a plano: que no salga dos veces el mismo animal o el mismo momento ----
# Lucas, 2026-11-17 (alimentacion): «se repite el clip de la terrapene en la intro: está bien cuando la menciona, pero el de
# antes aprovecharía y pondría otro animal». En un tráiler-resumen cada plano enseña algo DISTINTO y llamativo (el animal
# más espectacular, una acción, una reacción). Esta tira tiene un fotograma de cada plano del tráiler, en orden: mírala.
import json as _j
_m = _j.load(open(f"{TRABAJO}/linea.json", encoding="utf-8"))["marcas"]; _fin = _m.get("cuerpo", 0); tr = []
for v in video():
    if v["o"] >= _fin: break
    f = v["o"] + v["n"] // 2; W2, H2, x, y = encuadre(v["z1"], v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", 0.5)); ent, pre = fuente(v["clip"], (v["in"] + v["n"] // 2 * v["speed"]) / FPS)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}{RECORTE_169}scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y},scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy() if len(raw) == w * h * 3 else np.zeros((h, w, 3), np.uint8)
    s = v["o"] / FPS; cv2.rectangle(im, (0, 0), (w, 30), (0, 0, 0), -1)
    cv2.putText(im, f"{int(s // 60)}:{s % 60:04.1f} {v['clip']} {v['n'] / FPS:.1f}s {'REC' if v['b'] else ''}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 240, 240), 2); tr.append(im)
if tr:
    while len(tr) % 4: tr.append(np.zeros_like(tr[0]))
    cv2.imwrite(f"{TRABAJO}/trailer.jpg", np.vstack([np.hstack(tr[k:k + 4]) for k in range(0, len(tr), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 80]); print(f"tráiler plano a plano -> {TRABAJO}/trailer.jpg")
