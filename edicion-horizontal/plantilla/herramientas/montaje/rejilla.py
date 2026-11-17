"""rejilla.py CLIP t [t ...]: fotogramas del bruto con una rejilla rotulada en PÍXELES DEL LIENZO -> trabajo/rejilla.jpg.
Para poner un rótulo con flecha (TRK) sin adivinar: se mira dónde está el sujeto (el perro, la flor, el caracol) y se
copia su centro y medio lado: TRK = [(clip, t0, t1, [cx, cy, medio_lado], "NOMBRE", "pie", "der")]. Luego paso3 lo sigue
solo y hoja_textos.py enseña la flecha (punto rojo = el sujeto seguido) en cada fotograma.
Por qué: el TRK se dejaba sin usar porque había que calcular la caja a ojo; Lucas, 2026-11-17: «le ponía una flecha con
el nombre para resaltarlo» (Ragnar dormido) y «una flecha con el nombre señalando a cada una de las 3 cosas que nombra».
Ejemplo: rejilla.py C0170 41 43.5"""
import subprocess, sys
import numpy as np, cv2
from comun import ALTO, ANCHO, TRABAJO, fuente

a = sys.argv[1:]
if len(a) < 2: raise SystemExit(__doc__)
c = a[0]; w = 960; h = 2 * round(w * ALTO / ANCHO / 2); k = ANCHO / w; ims = []
for t in map(float, a[1:]):
    ent, pre = fuente(c, t)
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    im = np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy(); paso = 240      # cada 240 px del lienzo
    for x in range(0, ANCHO, paso):
        cv2.line(im, (int(x / k), 0), (int(x / k), h), (0, 255, 255) if x % 960 == 0 else (0, 160, 160), 1)
        if x % 480 == 0: cv2.putText(im, str(x), (int(x / k) + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    for y in range(0, ALTO, paso):
        cv2.line(im, (0, int(y / k)), (w, int(y / k)), (0, 255, 255) if y % 960 == 0 else (0, 160, 160), 1)
        if y % 480 == 0: cv2.putText(im, str(y), (2, int(y / k) - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    cv2.rectangle(im, (w - 170, 0), (w, 24), (0, 0, 0), -1); cv2.putText(im, f"{c} {t:g}s", (w - 165, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (80, 240, 240), 2); ims.append(im)
if len(ims) % 2: ims.append(np.zeros_like(ims[0]))
cv2.imwrite(f"{TRABAJO}/rejilla.jpg", np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 82]); print(f"{TRABAJO}/rejilla.jpg")
