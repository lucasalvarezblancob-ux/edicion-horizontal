"""Comprueba el montaje de la voz: transcribe trabajo/voz.wav y lo compara palabra a palabra con lo que pedía el EDL.
Cada diferencia sale con su minuto: mira si es un corte que se come o repite una palabra (arréglalo en edl.py) o solo
Whisper oyendo otra cosa. Objetivo: ratio >= 0,97 y ninguna diferencia en un borde de corte.
Al final, HUECO (silencio de más de 1,5 s dentro de lo hablado) y VOZ SIN TEXTO (voz que Whisper no transcribe: casi
siempre quien graba): cada uno se corta, se tapa con lo que pasa (con su sonido) o se apunta por qué se queda."""
import difflib, json, os, subprocess
from comun import AQUI, FPS, IDIOMA, PY, TRABAJO, norm
v, j = f"{TRABAJO}/voz.wav", f"{TRABAJO}/voz.json"
if not os.path.exists(j) or os.path.getmtime(j) < os.path.getmtime(v):
    subprocess.run([PY, f"{os.path.dirname(AQUI)}/transcribir.py", v, j, "--idioma", IDIOMA or "auto"], check=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
L = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8")); V = json.load(open(j, encoding="utf-8"))
a = [(norm(p["w"]), p["o0"] / FPS) for p in L["palabras"] if norm(p["w"])]
b = [(norm(w["p"]), w["t"]) for f in V["frases"] for w in f["palabras"] if norm(w["p"])]
sm = difflib.SequenceMatcher(None, [x[0] for x in a], [x[0] for x in b], autojunk=False); bad = 0
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal": continue
    bad += 1; t = a[min(i1, len(a) - 1)][1]
    print(f"{int(t // 60)}:{t % 60:04.1f}  quería: {' '.join(x[0] for x in a[i1:i2])!r:40}  se oye: {' '.join(x[0] for x in b[j1:j2])!r}")
print(bad, "diferencias; ratio", round(sm.ratio(), 3))

# ---- huecos sin voz y voz sin texto, en lo que SUENA ----
# Lucas, 2026-11-17 (alimentacion): «en el 1:50, tras "les pongo un poquito de agua", hay como un segundo muerto en el que
# pone el agua y está muteado el audio» y «"ahora vámonos a la várzea" lo repite dos veces y se oye al cámara decirle que
# lo diga». Causa: el EDL y las comprobaciones leen el TEXTO; un silencio de 2 s dentro de una pieza (vertiendo el agua,
# tapado además con un recurso mudo) y la voz de quien graba que Whisper no transcribe no aparecen en ningún texto.
#   HUECO          >= 1,5 s sin palabras (HUECO=1.2 para afinar) dentro de lo hablado: se corta, o se enseña LO QUE PASA con su sonido (V(…) con el
#                  gesto, a ser posible más cerca) y la frase siguiente entra por encima del final.
#   VOZ SIN TEXTO  >= 0,4 s de voz sin ninguna palabra transcrita: casi siempre otra persona (quien graba dando
#                  indicaciones: «dilo otra vez»). Se mira en el bruto: indicaciones fuera; si es parte del momento, a VOZ_DISFRAZ.
import numpy as np, soundfile as sf
y, sr = sf.read(v, dtype="float32"); y = y.mean(1) if y.ndim > 1 else y; h = sr // 50; nf = len(y) // h
db = 10 * np.log10((y[:nf * h].reshape(nf, h) ** 2).mean(1) + 1e-10); fondo = np.percentile(db[db > -90], 20) if (db > -90).any() else -60
hay = db > fondo + 12
cuerpo = L["marcas"].get("cuerpo", 0) / FPS
habla = sorted((p["o"] / FPS, (p["o"] + p["n"]) / FPS, p) for p in L["piezas"] if p["k"] == "T" and p["o"] / FPS >= cuerpo)
oidas = [(w["t"], w["fin"]) for f in V["frases"] for w in f["palabras"]]
tramos_ = []
for a0, a1, p in habla:      # pieces T seguidas = un tramo hablado
    if tramos_ and a0 - tramos_[-1][1] < 0.05: tramos_[-1][1] = a1
    else: tramos_.append([a0, a1])
mm = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"; nh = nv = 0
def corridas(m, t0, t1):
    i0, i1 = int(t0 * 50), int(t1 * 50); out = []; k = i0
    while k < i1:
        if m[k]:
            j = k
            while j < i1 and m[j]: j += 1
            out.append((k / 50, j / 50)); k = j
        else: k += 1
    return out
hueco = float(os.environ.get("HUECO", 1.5))
for a0, a1 in tramos_:
    ws = sorted((a, b) for a, b in oidas if a0 <= a < a1)          # huecos ENTRE palabras oídas (un golpe o un chorro de agua no son voz)
    for (x0, x1), (y0, _) in zip(ws, ws[1:]):
        if y0 - x1 >= hueco:
            nh += 1; print(f"HUECO {mm(x1)}: {y0 - x1:.1f} s sin palabras dentro de lo hablado (¿se corta, o se enseña lo que pasa con su sonido?)")
    for s0, s1 in corridas(db > fondo + 8, a0, a1):
        if s1 - s0 >= 0.4 and not any(min(s1, b) - max(s0, a) > 0.05 for a, b in oidas):
            nv += 1; print(f"VOZ SIN TEXTO {mm(s0)}: {s1 - s0:.1f} s de sonido de voz sin palabras transcritas (¿otra persona dando indicaciones? míralo en el bruto)")
print(f"{nh} huecos y {nv} voces sin texto por revisar: cada uno se corta, se tapa con lo que pasa (con su sonido) o se apunta por qué se deja")
