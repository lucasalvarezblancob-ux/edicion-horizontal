"""quitar_fondo_imagen.py: quita el fondo LISO (blanco, crema, negro, un color) de un logo o un dibujo y lo deja en un
.png con transparencia, listo para superponer en Remotion (<Img src={staticFile("…")} />).

  quitar_fondo_imagen.py ENTRADA SALIDA.png [--rampa 45] [--todo] [--prueba HOJA.jpg]

El color del fondo se mide en el borde de la imagen. Se quita el fondo de fuera y también los huecos cerrados que son
del mismo color (el interior de una O); lo que es de OTRO color aunque se parezca (el blanco de un ojo sobre fondo crema)
se queda. Los bordes se «desmezclan» del fondo para que no quede un halo de su color.
  --rampa   distancia de color en la que el borde pasa de transparente a opaco (más alto = borde más blando)
  --todo    quita cualquier píxel parecido al fondo, esté donde esté (también ese blanco del ojo)
  --prueba  hoja sobre oscuro, sobre claro y sobre verde: MÍRALA (halo del fondo, trozos comidos, motas sueltas)
Para animaciones con fondo verde (botones, mascotas): quitar_fondo.py."""
import argparse
import numpy as np, cv2

ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("salida")
ap.add_argument("--rampa", type=float, default=45); ap.add_argument("--todo", action="store_true"); ap.add_argument("--prueba")
a = ap.parse_args()
im = cv2.imread(a.entrada, cv2.IMREAD_COLOR).astype(np.float32); H, W = im.shape[:2]; b = max(4, min(H, W) // 80)
borde = np.concatenate([im[:b].reshape(-1, 3), im[-b:].reshape(-1, 3), im[:, :b].reshape(-1, 3), im[:, -b:].reshape(-1, 3)])
fondo = np.median(borde, 0); tol = float(np.percentile(np.linalg.norm(borde - fondo, axis=1), 99.9)) + 6     # el fondo y lo que varía (papel, ruido de compresión)
dist = np.linalg.norm(cv2.GaussianBlur(im, (0, 0), 0.7) - fondo, axis=2)
al = np.clip((dist - tol) / a.rampa, 0, 1)
if not a.todo:      # una zona parecida al fondo solo se quita si de verdad es fondo: tiene bastantes píxeles de su color exacto
    n, lab, st, _ = cv2.connectedComponentsWithStats((al < 1).astype(np.uint8), connectivity=8)
    nucleo = np.bincount(lab.ravel(), weights=(dist <= tol).ravel(), minlength=n)
    for i in range(1, n):
        x, y, w, h = st[i, :4]; fuera = x == 0 or y == 0 or x + w == W or y + h == H; m = lab == i
        # un hueco cerrado solo es fondo si su color es EL del fondo (no un blanco parecido: el ojo, un brillo)
        if nucleo[i] < 0.3 * st[i, cv2.CC_STAT_AREA] or (not fuera and np.linalg.norm(np.median(im[m & (al < 0.5)].reshape(-1, 3), 0) - fondo) > 14): al[m] = 1
al = cv2.erode(al, np.ones((3, 3), np.uint8))      # un píxel menos de borde: ahí es donde queda el halo del fondo
n, lab, st, _ = cv2.connectedComponentsWithStats((al > 0.5).astype(np.uint8), connectivity=8)      # motas sueltas del papel
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] < max(20, H * W // 20000): al[lab == i] = 0
A = al[..., None]; col = np.where(A > 0.02, (im - (1 - A) * fondo) / np.maximum(A, 0.02), im)      # desmezcla: el color del dibujo sin el del fondo
out = np.dstack([np.clip(col, 0, 255), al * 255]).astype(np.uint8)
cv2.imwrite(a.salida, out)
print(f"{a.salida}: {W}x{H}, fondo BGR {fondo.round().astype(int).tolist()}, tolerancia {tol:.0f}, opaco {100 * (al > 0.98).mean():.0f} %, transparente {100 * (al < 0.02).mean():.0f} %")
if a.prueba:
    hoja = [(col * A + np.array(c, np.float32) * (1 - A)) for c in ((25, 25, 25), (240, 240, 240), (40, 110, 50))]
    hoja = np.clip(np.hstack(hoja), 0, 255).astype(np.uint8); k = min(1.0, 2400 / hoja.shape[1])
    cv2.imwrite(a.prueba, cv2.resize(hoja, None, fx=k, fy=k, interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 90])
