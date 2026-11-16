"""Monta las tomas buenas de un bruto con repeticiones (alguien dicta el guion, se equivoca…).

Uso:
  herramientas/.venv/bin/python herramientas/montar_tomas.py VIDEO PALABRAS.json TOMAS.json SALIDA.json [--hablante speaker_1]

  PALABRAS.json: Scribe con diarización (`estudio/scripts/transcribir-scribe.mjs`), con "hablante".
  TOMAS.json: [{"desde": s, "hasta": s, "nota": "frase…"}, …] en el orden del montaje; desde/hasta =
              inicio de la primera palabra y fin de la última que quieres (aprox., de la transcripción).
  --hablante: quien sale a cámara (el resto de voces se considera "apuntador" y nunca entra).
              `--hablante todos`: varias personas hablan y todas cuentan (vlogs, retos).
  Por toma (opcional): "vel": 2.5 → tramo de acción acelerado y sin audio (llenar, beber…), no se ajusta a silencios;
              "pausa": s → umbral propio de pausas internas (0 = no recortar; p. ej. para dejar ver una báscula).

Las pausas internas > --pausa se recortan. Cada corte se lleva al punto más silencioso cercano (hasta 0,15 s fuera de la palabra) sin pisar
palabras del apuntador ni de otras tomas. Salida igual que cortar_pausas.py:
  {"fps":30,"tramos":[{"desde","hasta","inicio_edit","nota"}],"palabras":[{w,start,end}],"duracion"}
"""
import argparse, json, subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("palabras"); ap.add_argument("tomas"); ap.add_argument("salida")
ap.add_argument("--hablante", default="speaker_1")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--margen", type=float, default=0.15)
ap.add_argument("--pausa", type=float, default=0.3, help="pausas internas más largas se recortan (0 = no)")
a = ap.parse_args()

SR = 16000
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32)
hop = int(0.005 * SR)
e = np.convolve(y ** 2, np.ones(hop * 4) / (hop * 4), mode="same")[::hop]  # energía cada 5 ms
E = lambda t: e[min(len(e) - 1, max(0, int(t / 0.005)))]

pal = json.load(open(a.palabras))
TODOS = a.hablante == "todos"
es_mia = lambda p: TODOS or p.get("hablante", a.hablante) == a.hablante
otros = [p for p in pal if not es_mia(p)]
tomas = json.load(open(a.tomas))
f = a.fps


def punto_silencio(t0, t1):
    """t con menor energía en [t0, t1]"""
    ts = np.arange(t0, t1, 0.005)
    return float(ts[np.argmin([E(t) for t in ts])]) if len(ts) else t0


tramos, acc, out_pal = [], 0.0, []
for tm in tomas:
    vel = tm.get("vel", 1)
    if vel != 1:  # acción acelerada, muda
        s0, s1 = round(tm["desde"] * f) / f, round(tm["hasta"] * f) / f
        tramos.append({"desde": s0, "hasta": s1, "vel": vel, "inicio_edit": round(acc, 4), "nota": tm.get("nota", "")})
        acc += (s1 - s0) / vel
        continue
    pausa = tm.get("pausa", a.pausa)
    mias = [p for p in pal if es_mia(p) and tm["desde"] - 0.05 <= p["start"] < tm["hasta"]]
    if not mias:  # sin palabras: tramo tal cual
        s0, s1 = round(tm["desde"] * f) / f, round(tm["hasta"] * f) / f
        tramos.append({"desde": s0, "hasta": s1, "inicio_edit": round(acc, 4), "nota": tm.get("nota", "")})
        acc += s1 - s0
        continue
    w0, w1 = mias[0]["start"], mias[-1]["end"]
    # límites: no pisar al apuntador
    prev_otro = max([o["end"] for o in otros if o["end"] <= w0 + 0.01] or [w0 - a.margen])
    next_otro = min([o["start"] for o in otros if o["start"] >= w1 - 0.01] or [w1 + a.margen])
    ini = punto_silencio(max(w0 - a.margen, prev_otro + 0.01), w0 - 0.01)
    fin = punto_silencio(w1 + 0.03, min(w1 + a.margen, next_otro - 0.01) + 0.005)
    if tm.get("fijo"):  # bordes exactos de la toma (planos que hay que ver enteros)
        ini, fin = tm["desde"], tm["hasta"]
    if tramos and tramos[-1]["hasta"] > ini and tramos[-1]["hasta"] - ini < 0.5:
        ini = tramos[-1]["hasta"]  # tomas seguidas: no repetir frames
    # sub-tramos: corta pausas internas largas (en silencio real)
    cortes = [ini]
    for p0, p1 in zip(mias, mias[1:]):
        if pausa and p1["start"] - p0["end"] > pausa:
            cortes += [punto_silencio(p0["end"] + 0.04, p0["end"] + 0.12), punto_silencio(p1["start"] - 0.1, p1["start"] - 0.03)]
    cortes.append(fin)
    for k in range(0, len(cortes), 2):
        s0, s1 = round(cortes[k] * f) / f, round(cortes[k + 1] * f) / f
        if k + 2 == len(cortes) and s1 * f > (next_otro - 0.005) * f:
            s1 -= 1 / f
        if s1 - s0 < 2 / f:
            continue
        tramos.append({"desde": s0, "hasta": s1, "inicio_edit": round(acc, 4), "nota": tm.get("nota", "") if k == 0 else "…"})
        for p in mias:
            if s0 - 0.02 <= p["start"] < s1:
                out_pal.append({"w": p["w"], "start": round(acc + p["start"] - s0, 3), "end": round(acc + min(p["end"], s1) - s0, 3)})
        acc += s1 - s0

json.dump({"fps": f, "tramos": tramos, "palabras": out_pal, "duracion": round(acc, 3)},
          open(a.salida, "w"), ensure_ascii=False, indent=1)
print(f"{len(tramos)} tomas -> {acc:.2f} s")
for t in tramos:
    print(f"  {t['desde']:7.2f}-{t['hasta']:7.2f} ({(t['hasta']-t['desde'])/t.get('vel',1):.2f}s{' x'+str(t['vel']) if t.get('vel') else ''}, edit {t['inicio_edit']:.2f})  {t['nota']}")
