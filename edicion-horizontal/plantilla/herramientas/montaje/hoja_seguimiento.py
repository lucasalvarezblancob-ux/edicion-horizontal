"""hoja_seguimiento.py: por cada rótulo con flecha (TRK) de capas.json, 8 fotogramas DEL MONTAJE repartidos por todo su
tramo (con el recurso, la escala y el encuadre que haya debajo), recortados alrededor del punto seguido y con ese punto en
rojo -> trabajo/trk_N.jpg. OBLIGATORIO mirarla después de paso3_plan.py: el punto rojo ENCIMA del sujeto en los 8 y,
en el primero, ya el plano del sujeto (no el recurso de antes). Si no: t0 al primer segundo del plano y caja medida con
rejilla.py en ese segundo, con medio lado ≈ medio tamaño del sujeto.
Por qué: planto-estanque (2026-11-17), «UN VISITANTE»: entraba 1,1 s antes, sobre otro plano, y la flecha apuntaba a
las hojas; hoja_textos.py solo enseña 2 fotogramas por texto, y recortados a 640 px el punto no se distingue.
Viene del informe de Reino (planto-estanque); integrado en la skill el 2026-11-17.
Uso (desde out/<slug>/): hoja_seguimiento.py"""
import json, subprocess
import numpy as np, cv2
from comun import ALTO, ANCHO, CAPAS_JSON, FPS, TRABAJO, bruto, fuente, video
from dinamica import CARA_Y, encuadre

vid = video(); RW, RH = 1600, 900          # recorte alrededor del punto, en px del lienzo
trks = [it for it in json.load(open(CAPAS_JSON, encoding="utf-8"))["items"] if it["t"] == "trk"]


def fotograma(F_):      # el fotograma F_ del montaje a resolución de lienzo (como hoja_textos.fotograma, sin reducir)
    v = next((v for v in vid if v["o"] <= F_ < v["o"] + v["n"]), vid[-1]); k = F_ - v["o"]
    if v.get("t"): z = v["z1"] + (v["z0"] - v["z1"]) * max(0, 1 - k / v["t"]) ** 3
    else: z = v["z0"] + (v["z1"] - v["z0"]) * k / max(v["n"], 1)
    W2, H2, x, y = encuadre(z, v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", CARA_Y if not v["b"] else 0.5))
    ent, pre = fuente(v["clip"], (v["in"] + k * v["speed"]) / FPS)
    if v.get("bn"): pre += "hue=s=0,"          # el fail (FALLOS) va en blanco y negro, como en el render
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(raw) != ANCHO * ALTO * 3:          # HDR sin copia SDR en un ffmpeg sin libplacebo (Homebrew): sin convertir, se ve lavado pero vale para mirar el punto
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{(v['in'] + k * v['speed']) / FPS:.3f}", "-i", bruto(v["clip"]), "-frames:v", "1", "-vf", f"scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(ALTO, ANCHO, 3).copy() if len(raw) == ANCHO * ALTO * 3 else np.zeros((ALTO, ANCHO, 3), np.uint8)
    return im, v


for n, it in enumerate(trks, 1):
    ims = []
    for F_ in np.linspace(it["f0"], it["f1"] - 1, 8).round().astype(int):
        im, v = fotograma(int(F_)); px, py = it["pos"][min(F_ - it["f0"], len(it["pos"]) - 1)]
        x0 = int(min(max(px - RW / 2, 0), ANCHO - RW)); y0 = int(min(max(py - RH / 2, 0), ALTO - RH))
        r = im[y0:y0 + RH, x0:x0 + RW].copy(); cv2.circle(r, (int(px - x0), int(py - y0)), 14, (0, 0, 255), -1)
        s = F_ / FPS; lab = f"{int(s // 60)}:{s % 60:05.2f}  {v['clip']} {(v['in'] + (F_ - v['o']) * v['speed']) / FPS:.2f}s {'RECURSO' if v['b'] else 'principal'}"
        cv2.rectangle(r, (0, 0), (RW, 56), (0, 0, 0), -1); cv2.putText(r, lab, (12, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (80, 240, 240), 3)
        ims.append(cv2.resize(r, (800, 450)))
    hoja = np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, 8, 2)])
    cv2.putText(hoja, it["grande"], (12, 440), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    cv2.imwrite(f"{TRABAJO}/trk_{n}.jpg", hoja, [cv2.IMWRITE_JPEG_QUALITY, 82]); print(f"{TRABAJO}/trk_{n}.jpg", it["grande"])
