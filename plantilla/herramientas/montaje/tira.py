"""tira.py CLIP t0 t1 paso [CLIP t0 t1 paso ...]: tira de fotogramas del bruto con el segundo rotulado -> trabajo/tira.jpg
Para ELEGIR planos de recurso MIRÁNDOLOS (regla de Lucas: un recurso tiene que enseñar aquello de lo que se habla desde el
primer fotograma; nada de paredes, barridos ni arranques de cámara). Ejemplo: tira.py C0247 120 140 1 C0251 466 480 0.5"""
import subprocess, sys
import numpy as np, cv2
from comun import ALTO, ANCHO, TRABAJO, fuente

a = sys.argv[1:]; ims = []; w = 384; h = 2 * round(w * ALTO / ANCHO / 2)
if not a or len(a) % 4: raise SystemExit(__doc__)
for i in range(0, len(a), 4):
    c, t0, t1, paso = a[i], float(a[i + 1]), float(a[i + 2]), float(a[i + 3])
    for t in np.arange(t0, t1 + 1e-6, paso):
        ent, pre = fuente(c, float(t))
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
        if len(raw) < w * h * 3: continue
        im = np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy()
        cv2.rectangle(im, (0, 0), (190, 26), (0, 0, 0), -1); cv2.putText(im, f"{c[-4:]} {t:g}s", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 240, 240), 2); ims.append(im)
while len(ims) % 6: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f"{TRABAJO}/tira.jpg", np.vstack([np.hstack(ims[k:k + 6]) for k in range(0, len(ims), 6)]), [cv2.IMWRITE_JPEG_QUALITY, 78]); print(len(ims), f"fotogramas -> {TRABAJO}/tira.jpg")
