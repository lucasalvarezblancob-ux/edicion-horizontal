"""Estabiliza un vídeo grabado a pulso (selfie, cámara en mano) siguiendo el FONDO.

Uso:
  herramientas/.venv/bin/python herramientas/estabilizar.py ENTRADA.mp4 SALIDA.mp4 [--radio 20] [--zoom 1.08]
      [--cara cara.json] [--seguir fondo|persona] [--desde s]
  Selfie a pulso → --seguir persona (con --cara): lo que tiene que quedarse quieto es la cara, no la pared.   (seguir_cara.py: excluye a la persona del seguimiento → se estabiliza contra la pared)

- Sigue puntos del fondo fotograma a fotograma (flujo óptico + transformación parcial afín: desplazamiento,
  giro y escala), suaviza la trayectoria con una media móvil de ±radio frames y aplica la diferencia.
  Con radio 20 (≈0,7 s a 30 fps) se quita el temblor y se mantienen los movimientos lentos.
- `--zoom` recorta un poco para que no se vean bordes negros (1,06–1,10).
- Copia el audio tal cual. La salida tiene el mismo tamaño, fps y número de fotogramas.
"""
import argparse, json, subprocess, tempfile, os
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("entrada"); ap.add_argument("salida")
ap.add_argument("--radio", type=int, default=20)
ap.add_argument("--zoom", type=float, default=1.08)
ap.add_argument("--cara", default=None)
ap.add_argument("--seguir", choices=["fondo", "persona"], default="fondo",
                help="fondo: quieta la pared (vlog, cámara en trípode que se mueve). persona: quieta la cara (selfie a pulso)")
ap.add_argument("--desde", type=float, default=0.0, help="s: antes de esto no se toca (p. ej. colocando el móvil)")
a = ap.parse_args()

caras = json.load(open(a.cara))["caras"] if a.cara else None
cap = cv2.VideoCapture(a.entrada)
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
n = len(frames)
S = 0.5  # análisis a media resolución

def mascara(i):
    m = np.full((int(H * S), int(W * S)), 255, np.uint8)
    c = caras[min(i, len(caras) - 1)] if caras else None
    if c and a.seguir == "persona":
        cx, cy, w = c[0] * S, c[1] * S, c[2] * S
        m[:] = 0  # solo la cara (ojos, cejas, nariz): si entra pared, el seguimiento se mezcla con el fondo
        cv2.rectangle(m, (max(0, int(cx - w * 0.3)), max(0, int(cy - w * 0.35))), (min(m.shape[1], int(cx + w * 0.3)), min(m.shape[0], int(cy + w * 0.4))), 255, -1)
        return m
    if c:
        cx, cy, w = c[0] * S, c[1] * S, c[2] * S
        # la persona: de la cabeza hacia abajo, ancho creciente (hombros/brazo)
        x0, x1 = int(cx - w * 0.75), int(cx + w * 0.75)
        cv2.rectangle(m, (max(0, x0), max(0, int(cy - w * 0.75))), (min(m.shape[1], x1), m.shape[0]), 0, -1)
        cv2.rectangle(m, (0, int(cy + w * 0.6)), (m.shape[1], m.shape[0]), 0, -1)
    else:
        cv2.rectangle(m, (int(m.shape[1] * 0.2), int(m.shape[0] * 0.3)), (int(m.shape[1] * 0.8), m.shape[0]), 0, -1)
    return m

gris = [cv2.cvtColor(cv2.resize(f, None, fx=S, fy=S), cv2.COLOR_BGR2GRAY) for f in frames]
tray = np.zeros((n, 4))  # dx, dy, ángulo, log(escala) acumulados
acc = np.zeros(4)
i0 = int(round(a.desde * fps))
for i in range(i0 + 1, n):
    p0 = cv2.goodFeaturesToTrack(gris[i - 1], 300, 0.01, 12, mask=mascara(i - 1))
    d = np.zeros(4)
    if p0 is not None and len(p0) >= 8:
        p1, st, _ = cv2.calcOpticalFlowPyrLK(gris[i - 1], gris[i], p0, None)
        ok = st.ravel() == 1
        if ok.sum() >= 8:
            M, _ = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=2.0)
            if M is not None:
                s = np.hypot(M[0, 0], M[1, 0])
                # desplazamiento DEL CENTRO de la imagen (no de la esquina: si no, un giro mínimo parece un gran salto)
                c0 = np.array([W * S / 2, H * S / 2])
                tc = M[:, :2] @ c0 + M[:, 2] - c0
                d = np.array([tc[0] / S, tc[1] / S, np.arctan2(M[1, 0], M[0, 0]), np.log(s)])
    acc = acc + d
    tray[i] = acc

r = a.radio
pad = np.pad(tray[i0:], ((r, r), (0, 0)), mode="edge")
suave = np.array([pad[i:i + 2 * r + 1].mean(axis=0) for i in range(n - i0)])
corr = np.zeros_like(tray)
corr[i0:] = suave - tray[i0:]
# nunca más que el margen del recorte (si no, se verían bordes reflejados)
lim = np.array([(a.zoom - 1) * W / 2, (a.zoom - 1) * H / 2]) / a.zoom * 0.92
corr[:, :2] = np.clip(corr[:, :2], -lim, lim)

tmp = tempfile.mkdtemp()
silencioso = os.path.join(tmp, "v.mp4")
out = cv2.VideoWriter(silencioso, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
for i, f in enumerate(frames):
    dx, dy, da, ds = corr[i]
    s = np.exp(ds) * a.zoom
    # p' = c + s·R(da)·(p − c) + zoom·(dx, dy)   (misma convención que estimateAffinePartial2D)
    A = s * np.array([[np.cos(da), -np.sin(da)], [np.sin(da), np.cos(da)]])
    c = np.array([W / 2, H / 2])
    t = c - A @ c + a.zoom * np.array([dx, dy])
    M = np.hstack([A, t[:, None]])
    out.write(cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT))
out.release()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silencioso, "-i", a.entrada, "-map", "0:v", "-map", "1:a?",
                "-c:v", "libx264", "-crf", "17", "-g", "15", "-pix_fmt", "yuv420p", "-c:a", "copy", a.salida], check=True)
mov = np.abs(np.diff(tray[i0:, :2], axis=0)).mean(axis=0)
quedan = np.abs(np.diff((tray + corr)[i0:, :2], axis=0)).mean(axis=0)
tope = (np.abs(corr[i0:, :2]) >= lim * 0.999).mean(axis=0) * 100
print(f"corrección limitada por el margen en {tope.round(0)} % de frames (x, y)")
print(f"{a.salida}: {n} frames · movimiento medio por frame {mov.round(2)} px → {quedan.round(2)} px")
