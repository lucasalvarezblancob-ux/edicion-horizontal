"""quitar_fondo.py: quita el fondo verde de una animación (botón, mascota, logo animado) y la deja lista para superponer
en Remotion: un .webm (VP9 con transparencia) recortado a lo que se mueve + un .json con sus medidas.

  quitar_fondo.py ENTRADA SALIDA.webm [--t0 S] [--t1 S] [--modo croma|mate] [--caja x0,y0,x1,y1] [--audio SALIDA.mp3] [--prueba HOJA.jpg]

  --modo croma  pantalla verde pura (por defecto): botones de YouTube, cromas de banco
  --modo mate   fondo verde apagado con dibujo de contorno oscuro (mascotas generadas): mide el verde del borde en cada fotograma
  --caja        recorta ANTES la zona útil del original (si lleva bandas negras u otros elementos)
  --audio       guarda además el sonido de ese tramo (para ponerlo como efecto)
  --prueba      hoja con 6 fotogramas sobre damero y sobre negro: MÍRALA (halo verde, contorno comido, restos de fondo)
Uso en Remotion: <OffthreadVideo transparent src={staticFile("…/x.webm")} />. Regla: nunca se superpone un clip con su
fondo verde ni con un halo verde alrededor."""
import argparse, json, subprocess
import numpy as np, cv2

ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("salida")
ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float); ap.add_argument("--modo", default="croma")
ap.add_argument("--caja"); ap.add_argument("--audio"); ap.add_argument("--prueba")
a = ap.parse_args()
st = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:format=duration", "-of", "json", a.entrada], capture_output=True, text=True).stdout)
W, H = st["streams"][0]["width"], st["streams"][0]["height"]; n, d = st["streams"][0]["r_frame_rate"].split("/"); fps = float(n) / float(d)
t1 = a.t1 if a.t1 else float(st["format"]["duration"]); X0, Y0, X1, Y1 = [int(v) for v in a.caja.split(",")] if a.caja else (0, 0, W, H)
def fotogramas():
    """Los fotogramas del tramo, de uno en uno (un botón a 1080p entero en memoria son varios GB)."""
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{a.t0:.3f}", "-t", f"{t1 - a.t0:.3f}", "-i", a.entrada, "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)[Y0:Y1, X0:X1]
    p.stdout.close(); p.wait()


def alfa(im):
    b, g, r = [im[..., i].astype(np.float32) for i in range(3)]; verde = g - np.maximum(r, b); v = np.maximum(np.maximum(r, g), b)
    if a.modo == "croma":
        al = np.clip((110 - verde) / 70, 0, 1)
        if al.mean() > 0.5: al[:] = 0          # un fotograma sin verde (cartela, fundido a negro) no es del clip: transparente
    else:
        borde = np.concatenate([verde[:6].ravel(), verde[-6:].ravel(), verde[:, :6].ravel(), verde[:, -6:].ravel()]); vb = float(np.median(borde))
        luz = float(np.median(np.concatenate([v[:6].ravel(), v[-6:].ravel(), v[:, :6].ravel(), v[:, -6:].ravel()])))
        al = np.maximum(np.clip((0.78 * vb - verde) / (0.45 * vb), 0, 1), np.clip((0.72 * luz - v) / (0.22 * luz), 0, 1))    # ni verde como el fondo, o bien oscuro (contorno)
    al = cv2.medianBlur((al * 255).astype(np.uint8), 3).astype(np.float32) / 255
    al = np.minimum(al, cv2.erode(al, np.ones((3, 3), np.uint8)) * 0.5 + al * 0.5)                # el borde, medio píxel hacia dentro: sin halo
    out = im.copy(); tope = np.maximum(r, b) + (0 if a.modo == "croma" else 10)
    sucio = (al < 0.999) | (verde > 12); out[..., 1] = np.where(sucio, np.minimum(g, tope), g).astype(np.uint8)   # el verde derramado en los bordes, fuera
    return out, al


vis = None; N = 0
for f in fotogramas():                                   # 1ª pasada: qué zona se usa
    al = alfa(f)[1] > 0.06; vis = al if vis is None else (vis | al); N += 1
ys, xs = np.where(vis)
y0, y1, x0, x1 = max(ys.min() - 6, 0), min(ys.max() + 7, vis.shape[0]), max(xs.min() - 6, 0), min(xs.max() + 7, vis.shape[1])
y1 -= (y1 - y0) % 2; x1 -= (x1 - x0) % 2; w, h = x1 - x0, y1 - y0
p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", f"{fps:.5f}", "-i", "-",
                      "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "22", "-row-mt", "1", "-auto-alt-ref", "0", "-an", a.salida], stdin=subprocess.PIPE)
ks = set(np.linspace(0, N - 1, 6).astype(int).tolist()); muestra = []
for k, f in enumerate(fotogramas()):                     # 2ª pasada: escribir
    im, al = alfa(f); im = im[y0:y1, x0:x1]; al = al[y0:y1, x0:x1]
    p.stdin.write(np.dstack([im, (al * 255).astype(np.uint8)]).tobytes())
    if k in ks: muestra.append((im.astype(np.float32), al[..., None]))
p.stdin.close(); p.wait()
info = {"w": int(w), "h": int(h), "x": int(X0 + x0), "y": int(Y0 + y0), "ancho_original": W, "alto_original": H, "fps": round(fps, 3), "frames": N, "dur": round(N / fps, 3)}
json.dump(info, open(a.salida.rsplit(".", 1)[0] + ".json", "w")); print(a.salida, info)
if a.audio:
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a.t0:.3f}", "-t", f"{t1 - a.t0:.3f}", "-i", a.entrada, "-vn", "-ac", "2", "-ar", "48000", "-b:a", "192k", a.audio], check=True)
if a.prueba:
    tiras = []
    for fondo in ("damero", "negro", "blanco"):
        fila = []
        for im, al in muestra:
            if fondo == "damero": yy, xx = np.mgrid[0:h, 0:w]; bg = np.where(((yy // 16 + xx // 16) % 2)[..., None] == 0, 200.0, 120.0) * np.array([1.0, 0.6, 1.0])
            else: bg = np.full((h, w, 3), 0.0 if fondo == "negro" else 255.0)
            fila.append((im * al + bg * (1 - al)).astype(np.uint8))
        tiras.append(np.hstack(fila))
    hoja = np.vstack(tiras); esc = min(1.0, 2400 / hoja.shape[1]); cv2.imwrite(a.prueba, cv2.resize(hoja, None, fx=esc, fy=esc, interpolation=cv2.INTER_AREA), [cv2.IMWRITE_JPEG_QUALITY, 90])
