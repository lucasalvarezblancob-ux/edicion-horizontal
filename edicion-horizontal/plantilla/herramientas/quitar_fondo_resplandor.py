"""quitar_fondo_resplandor.py ENTRADA SALIDA.png PRUEBA.jpg [FONDO.jpg]: quita el fondo NEGRO de un logo que lleva un
RESPLANDOR claro que se funde con el negro. Con quitar_fondo_imagen.py ese resplandor queda como un cerco oscuro sobre
fondos claros o verdes; aquí pasa a ser su color claro con transparencia, y lo demás (dibujo, letras, contornos oscuros
que no son negro puro) se queda opaco. También se quita el negro puro encerrado entre las letras.
PRUEBA.jpg: el logo sobre oscuro, claro, verde y, si se da FONDO.jpg (un fotograma de donde va a ir), sobre él. MÍRALA."""
import sys
import numpy as np, cv2
ent, sal, prueba = sys.argv[1:4]
im = cv2.imread(ent, cv2.IMREAD_COLOR).astype(np.float32); H, W = im.shape[:2]
lum = im.mean(2); mx, mn = im.max(2), im.min(2); sat = (mx - mn) / np.maximum(mx, 1)
# color del resplandor a plena luz: píxeles claros y poco saturados (la «pegatina» crema del emblema)
m = (lum > 150) & (sat < 0.3); crema = np.median(im[m], 0); u = crema / np.linalg.norm(crema)
k = (im @ u) / np.linalg.norm(crema)                       # cuánto de crema lleva cada píxel (0 negro … 1 crema)
res = np.linalg.norm(im - (im @ u)[..., None] * u, axis=2)   # lo que se aparta de la línea negro→crema
enlinea = (res < 12 + 10 * k) & (k < 0.97)
# solo el resplandor de FUERA: conectado con el borde de la imagen a través de píxeles en esa línea
ff = np.zeros((H + 2, W + 2), np.uint8); lienzo = (enlinea * 255).astype(np.uint8)
fuera = np.zeros((H, W), bool)
for x, y in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1), (W // 2, 0), (W // 2, H - 1), (0, H // 2), (W - 1, H // 2)]:
    if lienzo[y, x] == 255: cv2.floodFill(lienzo, ff, (x, y), 128)
# y los huecos de negro PURO encerrados (entre las letras): también son fondo
n_, lab, st, _c = cv2.connectedComponentsWithStats((im.max(2) < 7).astype(np.uint8), connectivity=4)
for i in range(1, n_):
    if st[i, 4] >= 20:
        ys_, xs_ = np.where(lab == i)
        if lienzo[ys_[0], xs_[0]] == 255: cv2.floodFill(lienzo, ff, (int(xs_[0]), int(ys_[0])), 128)
fuera = lienzo == 128
alfa = np.ones((H, W), np.float32); alfa[fuera] = np.clip(k[fuera] / 0.97, 0, 1)
alfa[fuera & (k < 0.02)] = 0
col = im.copy(); col[fuera] = crema
# borde entre lo opaco y el resplandor: 1 px de suavizado del alfa para no dejar escalón
alfa_s = cv2.GaussianBlur(alfa, (0, 0), 0.6); alfa = np.where(fuera, np.minimum(alfa, np.maximum(alfa_s, alfa)), alfa)
out = np.dstack([np.clip(col, 0, 255), alfa * 255]).astype(np.uint8)
ys, xs = np.where(alfa > 0.02); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; p = 12
out = out[max(0, y0 - p):y1 + p, max(0, x0 - p):x1 + p]
cv2.imwrite(sal, out)
print(f"{sal}: {out.shape[1]}x{out.shape[0]}, crema BGR {crema.round().tolist()}, resplandor {100 * fuera.mean():.0f} % de la imagen, opaco {100 * (alfa > 0.98).mean():.0f} %")
# hoja de prueba: sobre oscuro, claro, verde y (si se da) sobre un fotograma real
h = 540; w = round(out.shape[1] * h / out.shape[0]); lg = cv2.resize(out, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
fondos = [np.full((h + 60, w + 60, 3), c, np.float32) for c in ((28, 28, 28), (238, 238, 238), (45, 110, 50))]
if len(sys.argv) > 4:
    f = cv2.imread(sys.argv[4]).astype(np.float32); f = cv2.resize(f, (round(f.shape[1] * (h + 60) / f.shape[0]), h + 60))
    x = (f.shape[1] - (w + 60)) // 2; fondos.append(f[:, max(0, x):max(0, x) + w + 60].copy())
for f in fondos:
    if f.shape[1] < w + 60: f = cv2.resize(f, (w + 60, h + 60))
    a = lg[..., 3:] / 255; f[30:30 + h, 30:30 + w] = lg[..., :3] * a + f[30:30 + h, 30:30 + w] * (1 - a)
cv2.imwrite(prueba, np.hstack([f[:, :w + 60] for f in fondos]).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 92])
