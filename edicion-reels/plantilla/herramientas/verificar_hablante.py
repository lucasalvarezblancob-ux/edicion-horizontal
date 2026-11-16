"""¿Quién dice cada frase del montaje? Para brutos con APUNTADOR (alguien dicta y el creador repite a cámara): la voz del
que dicta NUNCA puede quedar en el vídeo. Sobre todo sin Scribe (sin diarización), pásalo SIEMPRE antes de renderizar,
junto a revisar_cortes.py, y mira las tiras a ojo. (2026-11-16: se colaron frases del apuntador pegadas a una buena.)

Uso:
  herramientas/.venv/bin/python herramientas/verificar_hablante.py VIDEO montaje.json [--salida CARPETA]
  VIDEO: el proxy del bruto (estudio/public/<slug>/proxy.mp4) o el bruto: los tiempos de montaje.json son del bruto.
  montaje.json: el de montar_tomas.py / cortar_tomas_energia.py / cortar_pausas.py ({"tramos":[{desde,hasta,nota}]}).
  Sin montaje.json, revisa el vídeo entero.

Qué hace:
  1. Parte cada tramo en FRASES en los silencios cortos (≥ 0,15 s), no solo en los largos, y además donde el volumen
     cambia de golpe y se mantiene (≥ 8 dB durante ≥ 0,3 s): el apuntador suele dictar la frase siguiente pegada a la
     buena del creador, a veces sin ningún silencio, pero más bajo (gymbro-black-friday: 0 s de silencio, ~14 dB menos).
     Se decide frase a frase, nunca por tramo (la parte del creador "tapaba" la del apuntador).
  2. PRUEBA PRINCIPAL, la boca: a 8 fps, puntos de los labios con MediaPipe (modelo de 3,7 MB que se baja solo a
     herramientas/modelos/ la primera vez) y apertura = labio interior arriba–abajo / ancho de boca. Medido en
     gymbro-black-friday: mientras dicta el apuntador, 0,05 de media (boca cerrada, sonriendo); el creador hablando,
     0,11–0,26. Frase SOSPECHOSA si su apertura media es < --umbral × la mediana del montaje (que es del creador) o si
     casi no se ve la cara (mira abajo o al apuntador). La diferencia entre fotogramas o lo oscuro de la boca NO sirven
     (se probaron: los mueve cualquier gesto de cabeza o la luz).
  3. Apoyo: volumen y tono (librosa.pyin) frente a la mediana. Solos no prueban nada (el creador dicho más bajo o más
     rápido puede dar el tono del apuntador), pero si los dos se apartan a la vez (≥ 8 dB más baja y ≥ 4 semitonos) la
     frase también sale SOSPECHOSA, para mirarla en la tira.
  4. Tiras: en CARPETA (por defecto, verificar_hablante/ junto a montaje.json), una imagen por frase con la cara
     recortada a lo largo de la frase (fNN_*.jpg; las sospechosas empiezan por "SOSPECHOSA_") y todas juntas en
     tiras.jpg. Míralas: si la boca no acompaña a la frase, esa frase es del apuntador.
Termina con código 1 si hay alguna sospechosa. Una sospechosa no se entrega: se vuelve a montar (partir el tramo en el
corte medido entre las dos frases y quitar la del apuntador) o se confirma a ojo con la tira que es del creador.
"""
import argparse, glob, json, os, subprocess, sys, tempfile, urllib.request
import cv2, librosa, numpy as np
from scipy.signal import butter, sosfilt
sys.stdout.reconfigure(encoding="utf-8")
os.environ.setdefault("GLOG_minloglevel", "2"); os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("montaje", nargs="?")
ap.add_argument("--salida"); ap.add_argument("--silencio", type=float, default=0.15)
ap.add_argument("--umbral", type=float, default=0.45, help="sospechosa si la apertura media < umbral × la mediana")
a = ap.parse_args()

# ── Modelo de puntos de la cara (MediaPipe) ──
MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos", "face_landmarker.task")
URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
except ImportError:
    sys.exit("Falta mediapipe en la .venv: lanza bash .claude/skills/edicion-reels/actualizar.sh (o .venv/bin/pip install mediapipe).")
if not os.path.exists(MODELO):
    os.makedirs(os.path.dirname(MODELO), exist_ok=True); print("Bajando el modelo de la cara (3,7 MB)…")
    urllib.request.urlretrieve(URL, MODELO + ".part"); os.replace(MODELO + ".part", MODELO)
puntos = vision.FaceLandmarker.create_from_options(
    vision.FaceLandmarkerOptions(base_options=BaseOptions(model_asset_path=MODELO), num_faces=1))
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ── Audio: voz (mismo criterio que revisar_cortes.py) ──
SR = 16000; W = 0.01; hop = int(W * SR); FPS = 8; ANCHO = 1080
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, dtype=np.float32)
hf = sosfilt(butter(4, 3000, "highpass", fs=SR, output="sos"), y)
rms = lambda x: np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
db, dbh = rms(y), rms(hf)
voz = (db > -40) | (dbh > np.percentile(dbh, 20) + 8)
T = lambda t: max(0, min(len(voz), int(round(t / W))))

if a.montaje:
    tramos = [t for t in json.load(open(a.montaje, encoding="utf-8"))["tramos"] if not t.get("vel")]  # acelerados: sin audio
else:
    tramos = [{"desde": 0.0, "hasta": len(y) / SR, "nota": "vídeo entero"}]
sal = a.salida or os.path.join(os.path.dirname(os.path.abspath(a.montaje or a.video)), "verificar_hablante")
os.makedirs(sal, exist_ok=True)
for f in glob.glob(os.path.join(sal, "*.jpg")): os.remove(f)

# ── 1. Frases ──
frases = []
for it, t in enumerate(tramos):
    base = T(t["desde"]); v = voz[base:T(t["hasta"])]; trozos = []; ini = None; sil = 0; fin = 0
    for k, s in enumerate(v):                                  # silencios ≥ --silencio
        if s:
            if ini is None: ini = k
            sil = 0; fin = k + 1
        elif ini is not None:
            sil += 1
            if sil * W >= a.silencio: trozos.append([ini, fin]); ini = None
    if ini is not None: trozos.append([ini, fin])
    partidos = []                                              # saltos de volumen ≥ 8 dB mantenidos ≥ 0,3 s
    for ini, fin in trozos:
        d = db[base + ini:base + fin]
        mm = np.array([np.median(d[max(0, k - 10):k + 10]) for k in range(len(d))])
        a0 = 0; k = 30
        while k < len(mm):
            ref = np.median(mm[a0:k])
            if k + 30 <= len(mm) and np.all(np.abs(mm[k:k + 30] - ref) >= 8):
                partidos.append([ini + a0, ini + k]); a0 = k; k += 30
            else: k += 1
        partidos.append([ini + a0, fin])
    juntos = []
    for tr in partidos:
        # cola de palabra: < 0,5 s pegada sin silencio a lo anterior ("Pum-pers": las consonantes finales bajan de volumen
        # y cierran la boca; gymbro-black-friday). Una frase dictada nunca es tan corta; con silencio delante se mira sola.
        cola = juntos and tr[0] == juntos[-1][1] and (tr[1] - tr[0]) * W < 0.5
        # trocitos (< 0,3 s) con el de al lado si suenan igual
        trocito = juntos and ((tr[1] - tr[0]) * W < 0.3 or (juntos[-1][1] - juntos[-1][0]) * W < 0.3) and \
            abs(np.median(db[base + tr[0]:base + tr[1]]) - np.median(db[base + juntos[-1][0]:base + juntos[-1][1]])) < 8
        if cola or trocito: juntos[-1][1] = tr[1]
        else: juntos.append(tr)
    for ini, fin in juntos:
        frases.append({"tramo": it, "desde": round(t["desde"] + ini * W, 2), "hasta": round(t["desde"] + fin * W, 2),
                       "nota": t.get("nota", "")})

# ── Cara del creador ──
def fotogramas(desde, hasta, fps=FPS):   # ffmpeg ya aplica la rotación del iPhone/Sony
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{desde:.3f}", "-i", a.video, "-t", f"{max(hasta - desde, 0.15):.3f}",
                        "-vf", f"fps={fps},scale={ANCHO}:-2", os.path.join(d, "%04d.jpg")], check=True)
        return [cv2.imread(p) for p in sorted(glob.glob(os.path.join(d, "*.jpg")))]
def haar(fr):
    return casc.detectMultiScale(cv2.equalizeHist(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)), 1.1, 6, minSize=(80, 80))
# referencia (centro y tamaño medianos): descarta falsas caras de Haar (ropa oscura, murales…)
mu = [(r[0] + r[2] / 2, r[1] + r[3] / 2, r[2]) for f in frases for fr in fotogramas(f["desde"], min(f["hasta"], f["desde"] + 0.6), 3)
      for r in haar(fr)]
REF = None
if mu:
    md = np.median(np.array(mu), axis=0)
    REF = tuple(np.median(np.array([m for m in mu if np.hypot(m[0] - md[0], m[1] - md[1]) < 0.5 * md[2]] or mu), axis=0))
def cara(fr):
    """Caja de la cara del creador en este fotograma (o la de referencia si Haar no la ve) y apertura de la boca."""
    det = [r for r in haar(fr) if REF is None or (0.6 <= r[2] / REF[2] <= 1.6 and
           np.hypot(r[0] + r[2] / 2 - REF[0], r[1] + r[3] / 2 - REF[1]) < 0.8 * REF[2])]
    if det: x, yy, w, _ = max(det, key=lambda r: r[2]); cx, cy, s = x + w / 2, yy + w / 2, w
    elif REF is not None: cx, cy, s = REF
    else: cx, cy, s = fr.shape[1] / 2, fr.shape[0] / 3, fr.shape[1] / 3
    h = int(s * 1.5); x0, y0 = int(max(0, cx - h)), int(max(0, cy - h))
    rec = np.ascontiguousarray(fr[y0:y0 + 2 * h, x0:x0 + 2 * h])
    r = puntos.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(rec, cv2.COLOR_BGR2RGB))) if rec.size else None
    if not r or not r.face_landmarks: return rec, None
    p = r.face_landmarks[0]; dist = lambda i, j: np.hypot(p[i].x - p[j].x, p[i].y - p[j].y)
    return rec, dist(13, 14) / max(dist(78, 308), 1e-6)       # labio interior sup–inf / comisura–comisura

# ── 2–3. Boca (prueba principal), volumen y tono (apoyo) ──
for f in frases:
    res = [cara(fr) for fr in fotogramas(f["desde"], f["hasta"])]
    aps = [x for _, x in res if x is not None]
    f["_rec"] = [rc for rc, _ in res]
    f["cara"] = round(len(aps) / max(len(res), 1), 2)
    f["boca"] = round(float(np.mean(aps)), 3) if aps else None
    d = db[T(f["desde"]):T(f["hasta"])]; vv = voz[T(f["desde"]):T(f["hasta"])]
    f["vol_db"] = round(float(np.median(d[vv] if vv.any() else d)), 1) if len(d) else None
    try:
        f0 = librosa.pyin(y[int(f["desde"] * SR):int(f["hasta"] * SR)], fmin=60, fmax=400, sr=SR, frame_length=1024)[0]
        f["tono_hz"] = round(float(np.nanmedian(f0)), 1) if np.any(~np.isnan(f0)) else None
    except Exception:
        f["tono_hz"] = None

med = lambda k: float(np.median([f[k] for f in frases if f.get(k) is not None] or [0]))
mb, mv, mt = med("boca"), med("vol_db"), med("tono_hz")
print(f"{len(frases)} frases. Mediana del montaje: apertura de boca {mb:.3f} · volumen {mv:.1f} dB · tono {mt:.0f} Hz\n")
sosp = 0; filas = []
for i, f in enumerate(frases):
    motivo, apoyo = [], []
    if f["cara"] < 0.5: motivo.append(f"casi no se ve la cara ({int(f['cara'] * 100)} %): ¿mira abajo o al apuntador?")
    if f["boca"] is not None and mb and f["boca"] < a.umbral * mb:
        motivo.append(f"boca casi cerrada ({f['boca']:.2f} frente a {mb:.2f})")
    if f["vol_db"] is not None and f["vol_db"] < mv - 8: apoyo.append(f"volumen {f['vol_db'] - mv:+.0f} dB")
    if f["tono_hz"] and mt and abs(12 * np.log2(f["tono_hz"] / mt)) > 4: apoyo.append(f"tono {f['tono_hz']:.0f} Hz")
    if len(apoyo) == 2: motivo.append("otra voz: más baja y con otro tono (" + ", ".join(apoyo) + ")"); apoyo = []
    f["sospechosa"] = bool(motivo); f["motivo"] = motivo; sosp += bool(motivo)
    print(f"{i:2d} t{f['tramo']:<2d} {f['desde']:7.2f}-{f['hasta']:7.2f}  "
          f"{'⚠ SOSPECHOSA: ' + '; '.join(motivo) if motivo else 'OK'}{'   (apoyo: ' + ', '.join(apoyo) + ')' if apoyo else ''}"
          f"   {f['nota'][:40]}")
    # ── 4. Tira: hasta 10 caras repartidas a lo largo de la frase ──
    recs = [r for r in f.pop("_rec") if r.size]
    sel = [recs[int(k)] for k in np.linspace(0, len(recs) - 1, min(10, len(recs)))] if recs else []
    fila = np.hstack([cv2.resize(r, (160, 160)) for r in sel]) if sel else np.zeros((160, 160, 3), np.uint8)
    fila = np.hstack([fila, np.zeros((160, 1600 - fila.shape[1], 3), np.uint8)]) if fila.shape[1] < 1600 else fila[:, :1600]
    cab = np.full((26, 1600, 3), (0, 0, 160) if f["sospechosa"] else (40, 40, 40), np.uint8)
    cv2.putText(cab, f"{i:02d}  {f['desde']:.2f}-{f['hasta']:.2f} s  boca {f['boca'] if f['boca'] is not None else '-'}"
                     f"  cara {int(f['cara'] * 100)}%{'  SOSPECHOSA' if f['sospechosa'] else ''}",
                (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    fila = np.vstack([cab, fila]); filas.append(fila)
    cv2.imwrite(os.path.join(sal, f"{'SOSPECHOSA_' if f['sospechosa'] else ''}f{i:02d}_{f['desde']:.2f}-{f['hasta']:.2f}.jpg"), fila)
if filas: cv2.imwrite(os.path.join(sal, "tiras.jpg"), np.vstack(filas))
json.dump(frases, open(os.path.join(sal, "frases.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n{sosp} frases sospechosas. Tiras en {sal}/ (tiras.jpg = todas). Míralas antes de renderizar.")
sys.exit(1 if sosp else 0)
