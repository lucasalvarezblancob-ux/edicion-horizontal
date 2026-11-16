"""¿Se oye ENTERA la última palabra de cada toma? Transcribe con Whisper (local) el final de cada toma tal como queda
cortada y otra vez con 0,7 s más de margen, y compara la última palabra con la de la nota de la toma. Si la palabra solo
aparece con el margen, el corte se la come: FINAL CORTADO. (2026-11-16: "construimos" quedó en "construyo" por un
fin_max puesto antes de la sílaba final, nasal y floja, que parecía otro sonido; el render decía "construyo" y se tomó
por un error de Whisper.)

Uso: herramientas/.venv/bin/python herramientas/revisar_finales.py AUDIO_O_VIDEO_DEL_BRUTO montaje.json [--modelo ggml.bin]
  montaje.json: el de cortar_tomas_energia.py / montar_tomas.py (tramos con desde, hasta y nota). Una toma partida en
  varios tramos (los siguientes con nota "…") se revisa al final de su último tramo.
Resultado por toma:
  OK              la última palabra sale en el final cortado.
  FINAL CORTADO   solo sale con el margen → alarga el corte (o quita el fin_max) y vuelve a pasarlo.
  REVISAR         Whisper no la reconoce ni con margen (nombres de marca, palabra rara…) → escúchalo o transcribe el
                  trozo aislado. Si está entera, anótalo en la toma de tomas.json: "fin_revisado": "<qué has comprobado>"
                  (cortar_tomas_energia.py lo pasa al montaje y aquí sale como revisado).
Termina con código 1 si queda algún FINAL CORTADO o REVISAR sin "fin_revisado". Pásalo antes de renderizar, junto a
revisar_cortes.py. Ningún aviso se ignora: una palabra distinta en la transcripción es un corte hasta demostrar lo contrario.
"""
import argparse, difflib, json, os, re, subprocess, sys, tempfile, unicodedata
import numpy as np
from scipy.signal import butter, sosfilt
sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("audio"); ap.add_argument("montaje")
ap.add_argument("--modelo", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos", "ggml-small.bin"))
ap.add_argument("--margen", type=float, default=0.7)
a = ap.parse_args()
if not os.path.exists(a.modelo): sys.exit(f"Falta el modelo de Whisper ({a.modelo}): lanza actualizar.sh de la skill.")

# Voz por energía, como revisar_cortes.py. Umbral de banda completa pegado al ruido de fondo (ruido + 6 dB, no un −40
# fijo: en una habitación callada (ruido ~−60) el −40 se perdía las colas flojas; en un gym (ruido ~−40) veía voz en todo
# el ruido). Las sílabas finales nasales y flojas ("construi-MOS", -mon, -n, -m) son graves (~80 Hz) y bajas (−32 a −40 dB)
# y parecen otro sonido, pero son la palabra. El final es el primer silencio real, no donde baja el tono o el volumen.
SR = 16000; W = 0.01; hop = int(W * SR)
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.audio, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, dtype=np.float32)
rms = lambda x: np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(x) - hop, hop)])
db, dbh = rms(y), rms(sosfilt(butter(4, 3000, "highpass", fs=SR, output="sos"), y))
voz = (db > np.percentile(db, 20) + 6) | (dbh > np.percentile(dbh, 20) + 8)
T = lambda t: max(0, min(len(voz) - 1, int(round(t / W))))
corta_voz = lambda b: bool(voz[T(b) - 3:T(b)].any() and voz[T(b):T(b) + 3].any())   # hay voz a los dos lados del corte

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return [w for w in re.sub(r"[^a-zñ0-9 ]", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).split() if w]
RUIDO = re.compile(r"amara|subt[ií]tulos|gracias por ver|suscr[ií]bete", re.I)   # alucinaciones típicas en trozos cortos

def oir(desde, hasta):
    """Texto de Whisper para [desde, hasta] del bruto, con 0,4 s de silencio a cada lado (en trozos cortos alucina menos)."""
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, "t.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(desde, 0):.3f}", "-to", f"{hasta:.3f}", "-i", a.audio,
                        "-ac", "1", "-ar", "16000", "-af", "adelay=400,apad=pad_dur=0.4", w], check=True)
        r = subprocess.run(["whisper-cli", "-m", a.modelo, "-l", "es", "-nt", "-np", "-f", w], capture_output=True, text=True)
        return " ".join(l.strip() for l in r.stdout.splitlines() if l.strip() and not RUIDO.search(l))

sim = lambda x, y: difflib.SequenceMatcher(None, x, y).ratio()
m = json.load(open(a.montaje, encoding="utf-8"))
tomas = []                                                     # [primer tramo, último tramo]
for t in m["tramos"]:
    if t.get("vel"): continue
    if tomas and t.get("nota", "").strip() in ("…", "..."): tomas[-1][1] = t
    else: tomas.append([t, t])
def veredicto(wc, wl, exp, corte_en_voz):
    """OK / FINAL CORTADO / REVISAR comparando la toma cortada (wc) con la misma toma con margen (wl)."""
    sale = any(sim(w, exp) >= 0.75 for w in wc[-3:])
    if sale and not corte_en_voz: return "OK", "sale la palabra"
    if sale: return "⚠ REVISAR", "se reconoce, pero el corte cae sobre voz: ¿falta la cola (-s, -mos, -n) o es una respiración?"
    k = len(wc) - 1; cola = wl                                 # lo que hay en wl desde la posición de la última de wc
    if k >= 0:
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wc, wl, autojunk=False).get_opcodes():
            if i1 <= k < i2:
                cola = wl[j1 + (k - i1):] if tag == "equal" else wl[j1:]
                igual = tag == "equal"; break
        else: igual = False
    else: igual = False
    if any(sim(w, exp) >= 0.75 for w in cola[:3]): return "⚠ FINAL CORTADO", "con margen sí sale"
    if igual and len(wc) >= 2 and not corte_en_voz:
        return "OK", "mismo final con y sin margen y el corte cae en silencio (Whisper escribe distinto la palabra)"
    return "⚠ REVISAR", "no la reconoce ni con margen"

malos = 0
for i, (t0, t1) in enumerate(tomas):
    esperada = [w for w in norm(t0.get("nota", "")) if len(w) >= 3]
    if not esperada:
        print(f"{i:2d} {t1['hasta']:7.2f}  (sin nota: no puedo comparar)"); continue
    exp = esperada[-1]
    # la toma entera (hasta 8 s antes del final) da contexto a Whisper: en trozos de 1–2 s alucina ("segundo segundo")
    ini = max(t0["desde"], t1["hasta"] - 8.0)
    wc, wl = norm(oir(ini, t1["hasta"])), norm(oir(ini, t1["hasta"] + a.margen))
    estado, por = veredicto(wc, wl, exp, corta_voz(t1["hasta"]))
    rev = t1.get("fin_revisado") or t0.get("fin_revisado")
    if estado != "OK" and rev: estado += " → revisado"; por = rev
    elif estado != "OK": malos += 1
    print(f"{i:2d} {t1['hasta']:7.2f}  {estado:<16} espera «{exp}» · cortado: «{' '.join(wc[-3:])}»"
          f"{'' if estado == 'OK' and por == 'sale la palabra' else ' · con margen: «' + ' '.join(wl[-4:]) + '» (' + por + ')'}"
          f"   {t0.get('nota', '')[:40]}")
print(f"{malos} tomas por resolver (alarga el corte, o escúchalo y anota fin_revisado en tomas.json).")
sys.exit(1 if malos else 0)
