#!/usr/bin/env python3
"""Posición de la cara a lo largo de un bruto (para centrar punch-ins). YuNet (OpenCV), 5 muestras por segundo.
Uso: caras.py VIDEO SALIDA.json [TOPE_SEG]  ->  {"paso": 0.2, "ancho": W, "alto": H, "caras": [[cx, cy, w] | null, ...]} en px del vídeo.
Con TOPE_SEG (segundos de reloj) es reanudable: al pasar el tope guarda SALIDA.json.parcial y sale con código 3; al
relanzarlo sigue donde lo dejó (brutos de media hora en equipos con poca memoria o con límite de tiempo por orden)."""
import json, subprocess, sys, os, time
import numpy as np, cv2
v, out = sys.argv[1:3]; TOPE = float(sys.argv[3]) if len(sys.argv) > 3 else 0; PASO = 0.2; AW, AH = 640, 360
W, H = [int(x) for x in subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.split()[0].strip(",").split(",")[:2]]      # los .MOV de iPhone devuelven «3840,2160,» y más líneas
det = cv2.FaceDetectorYN.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos", "face_detection_yunet_2023mar.onnx"), "", (AW, AH), 0.75, 0.3, 50)
parcial = out + ".parcial"
caras = json.load(open(parcial)) if os.path.exists(parcial) else []
ss = ["-ss", f"{len(caras) * PASO:.3f}"] if caras else []
p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-hwaccel", "auto", *ss, "-i", v, "-vf", f"fps={1 / PASO},scale={AW}:{AH}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
t0 = time.time()
while True:
    b = p.stdout.read(AW * AH * 3)
    if len(b) < AW * AH * 3: break
    _, f = det.detect(np.frombuffer(b, np.uint8).reshape(AH, AW, 3))
    if f is None: caras.append(None)
    else:
        x, y, w, h = max(f, key=lambda r: r[2] * r[3])[:4]; k = W / AW
        caras.append([round(float((x + w / 2) * k)), round(float((y + h / 2) * k)), round(float(w * k))])
    if TOPE and time.time() - t0 > TOPE:
        p.kill(); json.dump(caras, open(parcial, "w"))
        print(parcial, len(caras), "muestras; sigue al relanzar"); sys.exit(3)
json.dump({"paso": PASO, "ancho": W, "alto": H, "caras": caras}, open(out, "w"))
if os.path.exists(parcial): os.remove(parcial)
print(out, len(caras), "muestras,", sum(c is not None for c in caras), "con cara")
