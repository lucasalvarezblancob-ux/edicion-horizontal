"""Deja en cada PNG de recortar_persona.py solo la mancha más grande (la persona),
quitando objetos sueltos que el modelo confunde (pósters, muebles…).
Uso: herramientas/.venv/bin/python herramientas/limpiar_mascara.py CARPETA
"""
import sys, glob
import cv2
import numpy as np

for p in sorted(glob.glob(sys.argv[1] + "/f*.png")):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    a = im[:, :, 3]
    n, lab, st, _ = cv2.connectedComponentsWithStats((a > 40).astype(np.uint8), 8)
    if n <= 2:
        continue
    keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    m = (lab == keep).astype(np.uint8)
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    im[:, :, 3] = a * m
    cv2.imwrite(p, im)
print("ok")
