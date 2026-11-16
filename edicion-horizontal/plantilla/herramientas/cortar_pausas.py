"""Jump cuts para vídeos hablando a cámara: detecta pausas por energía del audio y
devuelve los tramos que se conservan + los tiempos de cada palabra ya recolocados.

Uso:
  herramientas/.venv/bin/python herramientas/cortar_pausas.py VIDEO WHISPER.json SALIDA.json
      [--pausa 0.22] [--margen 0.07] [--db 34] [--desde 0] [--hasta fin]

  PALABRAS.json: mejor de Scribe (`estudio/scripts/transcribir-scribe.mjs`, preciso) o de
  `herramientas/transcribir.sh VIDEO salida` (Whisper local, tiempos aproximados).
  SALIDA.json:
    {"fps":30, "tramos":[{"desde":s,"hasta":s,"inicio_edit":s}, ...],
     "palabras":[{"w":..., "start":t_edit, "end":t_edit}], "duracion": s}
  En Remotion: un <Series.Sequence> por tramo con trimBefore = round(desde*fps) y
  durationInFrames = round((hasta-desde)*fps). Las palabras ya están en tiempo del edit.

Corta solo en silencio real (con margen a cada lado), nunca encima de una consonante.
"""
import argparse, json, subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("whisper"); ap.add_argument("salida")
ap.add_argument("--pausa", type=float, default=0.22, help="silencios más largos que esto se quitan")
ap.add_argument("--margen", type=float, default=0.07, help="audio que se conserva a cada lado")
ap.add_argument("--db", type=float, default=34, help="umbral de silencio bajo el pico (dB)")
ap.add_argument("--desde", type=float, default=0.0)
ap.add_argument("--hasta", type=float, default=None)
ap.add_argument("--quitar", type=str, default="", help="tramos a eliminar aunque haya voz: '19.3-20.35,…'")
ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()

SR = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
y = np.frombuffer(raw, np.float32)
hop = int(0.01 * SR)
rms = np.sqrt(np.convolve(y ** 2, np.ones(hop * 2) / (hop * 2), mode="same")[::hop] + 1e-12)
db = 20 * np.log10(rms / rms.max())
voz = db > -a.db
t = np.arange(len(db)) * 0.01
fin = a.hasta if a.hasta is not None else len(y) / SR

# tramos con voz
tramos, dentro = [], False
for i, v in enumerate(voz):
    if v and not dentro:
        ini, dentro = t[i], True
    elif not v and dentro:
        tramos.append([ini, t[i]]); dentro = False
if dentro:
    tramos.append([ini, t[-1]])
tramos = [[max(a.desde, s - a.margen), min(fin, e + a.margen)] for s, e in tramos if e > a.desde and s < fin]
for q in filter(None, a.quitar.split(",")):
    qa, qb = map(float, q.split("-"))
    nuevo = []
    for s, e in tramos:
        if e <= qa or s >= qb:
            nuevo.append([s, e])
        else:
            if s < qa: nuevo.append([s, qa])
            if e > qb: nuevo.append([qb, e])
    tramos = nuevo
# fusiona tramos separados por menos de la pausa permitida
fus = []
for s, e in tramos:
    if fus and s - fus[-1][1] < a.pausa:
        fus[-1][1] = max(fus[-1][1], e)
    else:
        fus.append([s, e])
# cuantiza a frames
f = a.fps
fus = [[round(s * f) / f, round(e * f) / f] for s, e in fus if e - s > 1.5 / f]

out_tramos, acc = [], 0.0
for s, e in fus:
    out_tramos.append({"desde": s, "hasta": e, "inicio_edit": round(acc, 4)})
    acc += e - s

# palabras: lista [{w,start,end}] (Scribe, estudio/scripts/transcribir-scribe.mjs — preferido)
# o salida de whisper.cpp -ojf con -ml 1 -sow (junta tokens en palabras)
d = json.load(open(a.whisper))
if isinstance(d, list):
    palabras = d
    toks = []
else:
  toks = [(tk["text"], tk["offsets"]["from"] / 1000, tk["offsets"]["to"] / 1000)
        for seg in d["transcription"] for tk in seg.get("tokens", [])
        if tk["text"].strip() and not tk["text"].strip().startswith("[_")]
  palabras = []
for txt, s, e in toks:
    if txt.startswith(" ") or not palabras or txt.strip() in "¿¡":
        palabras.append({"w": txt.strip(), "start": s, "end": e})
    else:
        palabras[-1]["w"] += txt.strip(); palabras[-1]["end"] = e
palabras = [p for p in palabras if p["w"] and p["w"] not in "¿¡"]


def remap(x):
    for tr in out_tramos:
        if tr["desde"] <= x <= tr["hasta"]:
            return tr["inicio_edit"] + x - tr["desde"]
    sig = [tr for tr in out_tramos if tr["desde"] > x]
    return sig[0]["inicio_edit"] if sig else acc


pal = [{"w": p["w"], "start": round(remap(p["start"]), 3), "end": round(remap(p["end"]), 3)}
       for p in palabras if a.desde <= p["start"] < fin
       and not any(float(q.split("-")[0]) <= p["start"] < float(q.split("-")[1])
                   for q in filter(None, a.quitar.split(",")))]
json.dump({"fps": f, "tramos": out_tramos, "palabras": pal, "duracion": round(acc, 3)},
          open(a.salida, "w"), ensure_ascii=False, indent=1)
print(f"{len(out_tramos)} tramos · {fin - a.desde:.2f}s -> {acc:.2f}s · {len(pal)} palabras")
for tr in out_tramos:
    print(f"  {tr['desde']:6.2f}-{tr['hasta']:6.2f}  (edit {tr['inicio_edit']:.2f})")
