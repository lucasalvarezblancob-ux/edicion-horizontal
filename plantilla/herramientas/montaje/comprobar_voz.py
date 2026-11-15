"""Comprueba el montaje de la voz: transcribe trabajo/voz.wav y lo compara palabra a palabra con lo que pedía el EDL.
Cada diferencia sale con su minuto: mira si es un corte que se come o repite una palabra (arréglalo en edl.py) o solo
Whisper oyendo otra cosa. Objetivo: ratio >= 0,97 y ninguna diferencia en un borde de corte."""
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
