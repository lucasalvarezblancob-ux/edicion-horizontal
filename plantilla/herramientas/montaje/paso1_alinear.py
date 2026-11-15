"""Paso 1: del EDL a la línea de tiempo en frames, con los bordes de cada frase afinados por ALINEACIÓN FORZADA.
Los tiempos por palabra de Whisper van ~0,17 s adelantados (hasta 0,8 s): no valen para cortar ni para colgar rótulos.
Aquí cada tramo de habla se alinea contra su audio con torchaudio MMS_FA (~20 ms de error) y de ahí salen:
  - el principio y el final de cada pieza (con LEAD/TAIL de aire, sin pisar la palabra vecina);
  - el frame de salida de CADA palabra (o0/o1), del que cuelgan zooms, rótulos, recursos, música y subtítulos.
Salida: trabajo/linea.json = {fps, total, piezas:[{clip,in,out,o,n,item,k,vol,speed,tag}], palabras:[{w,clip,idx,o0,o1,s0,dif}],
marcas:{tag:frame}, secciones:[...]}. `in/out` = frames del bruto (a FPS del proyecto); `o` = frame de salida."""
import json, math, os, re, subprocess
import numpy as np, soundfile as sf, torch, torchaudio
from comun import FPS, NUMEROS, TRABAJO, bruto, palabras, sin_tildes
from edl import EDL

LEAD, TAIL = 0.07, 0.14          # aire antes de la primera palabra y después de la última (s)
MIN_TROZO = 0.6                  # nada de trozos de habla de menos de 0,6 s: se pegan al vecino


def norm(w):
    """Palabra tal como la espera MMS_FA: letras a-z sin tildes; las cifras, como se dicen (NUMEROS de proyecto.py)."""
    w = w.strip().lower(); w = NUMEROS.get(re.sub(r"[^\w]", "", w), w)
    return re.sub(r"[^a-z']", "", sin_tildes(w)).strip("'")


dev = "cuda" if torch.cuda.is_available() else "cpu"
b = torchaudio.pipelines.MMS_FA
model, tok, aligner = b.get_model(with_star=False).to(dev), b.get_tokenizer(), b.get_aligner()
wavs = {}
def wav(c):
    if c not in wavs:
        p = f"{TRABAJO}/{c}.16k.wav"
        if not os.path.exists(p):
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", bruto(c), "-ac", "1", "-ar", "16000", p], check=True)
        wavs[c] = sf.read(p, dtype="float32")[0]
    return wavs[c]


def alinear(c, a, b_):
    w = palabras(c); y = wav(c); n = len(w)
    ca, cb = a, b_   # contexto: hasta 2 palabras vecinas, sin cruzar silencios
    while ca > max(0, a - 2) and w[ca]["t"] - w[ca - 1]["fin"] < 0.5: ca -= 1
    while cb < min(n - 1, b_ + 2) and w[cb + 1]["t"] - w[cb]["fin"] < 0.5: cb += 1
    t0, t1 = max(0, w[ca]["t"] - 0.6), min(len(y) / 16000, w[cb]["fin"] + 0.9)
    seg = torch.from_numpy(y[int(t0 * 16000):int(t1 * 16000)])[None].to(dev)
    txt = [norm(x["p"]) for x in w[ca:cb + 1]]; idx = [i for i, t in enumerate(txt) if t]
    with torch.inference_mode(): em, _ = model(seg)
    spans = aligner(em[0], tok([txt[i] for i in idx])); k = seg.shape[1] / em.shape[1] / 16000
    res = [None] * len(txt)
    for i, sp in zip(idx, spans): res[i] = [t0 + sp[0].start * k, t0 + sp[-1].end * k]
    for i in range(len(res)):   # palabras sin letras (cifras sin traducir, signos): se quedan pegadas a la anterior
        if res[i] is None: res[i] = [res[i - 1][1], res[i - 1][1]] if i and res[i - 1] else [w[ca + i]["t"], w[ca + i]["fin"]]
    prev = res[a - ca - 1][1] if a > ca else None; nxt = res[b_ - ca + 1][0] if b_ < cb else None
    return res[a - ca:b_ - ca + 1], prev, nxt


piezas, pal, marcas, secciones = [], [], {}, []
o = 0
for n_it, it in enumerate(EDL):
    if it["k"] == "X": marcas[it["tag"]] = o; continue
    if it["k"] == "S": secciones.append({**it, "o": o}); marcas[f"s{it['n']}"] = o; continue
    if it.get("tag"): marcas[it["tag"]] = o
    if it["k"] == "V":
        i0, i1 = round(it["t0"] * FPS), round(it["t1"] * FPS); n = round((i1 - i0) / it["speed"])
        piezas.append({"clip": it["c"], "in": i0, "out": i1, "o": o, "n": n, "item": n_it, "k": "V", "vol": it["vol"], "speed": it["speed"], "tag": it.get("tag")}); o += n; continue
    c, a, b_ = it["c"], it["a"], it["b"]
    al, prev, nxt = alinear(c, a, b_); w = palabras(c)
    grupos = [[0]]
    for i in range(1, len(al)):
        if al[i][0] - al[i - 1][1] > it["gap"]: grupos.append([i])
        else: grupos[-1].append(i)
    dur = lambda g: al[g[-1]][1] - al[g[0]][0]
    cambio = True
    while cambio and len(grupos) > 1:   # trozos demasiado cortos: se pegan al vecino más cercano (se conserva la pausa)
        cambio = False
        for gi, g in enumerate(grupos):
            if dur(g) < MIN_TROZO:
                izq = al[g[0]][0] - al[grupos[gi - 1][-1]][1] if gi else 1e9
                der = al[grupos[gi + 1][0]][0] - al[g[-1]][1] if gi < len(grupos) - 1 else 1e9
                if min(izq, der) > 3.0: continue
                if izq <= der: grupos[gi - 1] += g
                else: grupos[gi + 1] = g + grupos[gi + 1]
                del grupos[gi]; cambio = True; break
    for gi, g in enumerate(grupos):
        s, e = al[g[0]][0] - LEAD, al[g[-1]][1] + TAIL
        if gi == 0 and prev is not None: s = max(s, min(prev + 0.02, al[g[0]][0] - 0.02))            # sin pisar la palabra de antes
        if gi == len(grupos) - 1 and nxt is not None: e = min(e, max(nxt - 0.02, al[g[-1]][1] + 0.03))   # ni la de después
        i0, i1 = max(0, math.floor(s * FPS)), min(math.ceil(e * FPS), len(wav(c)) * FPS // 16000)   # sin salirse del bruto (frase en el segundo 0 o en el último)
        piezas.append({"clip": c, "in": i0, "out": i1, "o": o, "n": i1 - i0, "item": n_it, "k": "T", "vol": 1.0, "speed": 1.0, "tag": it.get("tag") if gi == 0 else None})
        for i in g:
            pal.append({"w": w[a + i]["p"].strip(), "clip": c, "idx": a + i, "o0": round(o + al[i][0] * FPS - i0, 2), "o1": round(o + al[i][1] * FPS - i0, 2), "s0": round(al[i][0], 3), "dif": round(al[i][0] - w[a + i]["t"], 3)})
        o += i1 - i0
json.dump({"fps": FPS, "total": o, "piezas": piezas, "palabras": pal, "marcas": marcas, "secciones": secciones}, open(f"{TRABAJO}/linea.json", "w", encoding="utf-8"), indent=0)
d = np.array([p["dif"] for p in pal]) if pal else np.zeros(1)
print(f"total {o} frames = {o / FPS / 60:.2f} min; {len(piezas)} piezas; {len(pal)} palabras; desfase de Whisper medio {np.mean(d) * 1000:+.0f} ms, |máx| {np.max(np.abs(d)):.2f} s ({dev})")
for k, v in marcas.items(): print(f"  {k:14} {v / FPS / 60:5.2f} min")
big = [p for p in pal if abs(p["dif"]) > 0.5]
if big: print("desfases > 0,5 s (revisa esos bordes en comprobar_voz.py):", [(p["clip"], p["idx"], p["w"], p["dif"]) for p in big][:40])
