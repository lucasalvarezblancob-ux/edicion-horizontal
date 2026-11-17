"""hojas_bruto.py CARPETA_BRUTOS|BRUTO CARPETA_SALIDA [paso_s=1]: hojas de contactos DENSAS de cada bruto (un fotograma por segundo,
6x6 por hoja, con el segundo rotulado) para hacer el registro visual: qué se ve en cada momento.
Rápido: solo decodifica fotogramas clave (-skip_frame nokey). Con un ARCHIVO en vez de una carpeta, solo ese bruto
(paso0_preparar.py lanza uno por bruto, varios a la vez). Las extensiones no distinguen mayúsculas: en Mac, «*.mov» no
encontraba los .MOV del iPhone y esos brutos se quedaban sin hojas."""
import sys, os, glob, subprocess, numpy as np, cv2
src, dst = sys.argv[1], sys.argv[2]; paso = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
os.makedirs(dst, exist_ok=True); W, H, COLS, FILAS = 480, 270, 6, 6
EXT = (".mp4", ".mov", ".m4v", ".mxf", ".mkv")
for f in [src] if os.path.isfile(src) else sorted(f for f in glob.glob(os.path.join(glob.escape(src), "*")) if f.lower().endswith(EXT)):
    clip = os.path.splitext(os.path.basename(f))[0]
    if glob.glob(os.path.join(glob.escape(dst), glob.escape(clip) + "_*.jpg")): continue
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-skip_frame", "nokey", "-i", f, "-vf", f"fps={1 / paso},scale={W}:{H}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    ims = []; n = 0; k = 0
    def volcar():
        global ims, k
        while len(ims) % COLS: ims.append(np.zeros((H, W, 3), np.uint8))
        cv2.imwrite(os.path.join(dst, f"{clip}_{k:02d}.jpg"), np.vstack([np.hstack(ims[i:i + COLS]) for i in range(0, len(ims), COLS)]), [cv2.IMWRITE_JPEG_QUALITY, 80]); k += 1; ims = []
    while True:
        raw = p.stdout.read(W * H * 3)
        if len(raw) < W * H * 3: break
        im = np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy(); t = n * paso
        cv2.rectangle(im, (0, 0), (150, 30), (0, 0, 0), -1); cv2.putText(im, f"{t:g} s", (6, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (80, 240, 240), 2)
        ims.append(im); n += 1
        if len(ims) == COLS * FILAS: volcar()
    if ims: volcar()
    print(clip, n, "fotogramas,", k, "hojas", flush=True)
