"""voces.py: frases del montaje que dice OTRA persona (quien graba, un amigo), no el creador. Se lanza desde out/<slug>/.
Para quien no quiere que se le reconozca (VOZ_DISFRAZ en plan.py: voz de pitufo) y para revisar los diálogos.

Cómo: transcribe trabajo/voz.wav (lo que de verdad suena, también lo que NO está en el texto del EDL: las respuestas de
quien graba se cuelan entre las palabras de una pieza) y mide en cada frase el tono (pyin) y el nivel. El creador lleva
el micro puesto: su voz llega fuerte y a su tono de siempre; quien graba suena más bajo (está lejos del micro) y con
otro tono, que puede ser MÁS AGUDO o MÁS GRAVE (quien edita no sabe de antemano cuál): se miran las dos direcciones.
Candidata = (tono >= 1,38 x el del creador Y nivel >= 2,5 dB por debajo del suyo) O (tono MEDIBLE <= el del creador / 1,15
Y nivel >= 6 dB por debajo) (medianas de todo el vídeo). Aparte, DUDOSAS: frases >= 12 dB por debajo de su nivel, sea
cual sea su tono; casi siempre son el creador hablando bajo o de espaldas, así que solo se listan para leerlas por el
sentido (no dan AVISO VOZ en paso5_audio.py).
Medido en prueba-3 (Reino Selva, 2026-11-15): las 6 frases conocidas del cámara salen todas, y 3 más que se habían
escapado; ninguna del creador. En vaciamos-estanque (2026-11-19) quien grababa iba a ~95 Hz y el creador a ~116 Hz
(x1,22 más grave) y a -40/-51 dB: solo con «más aguda» salía 1 de 5. En alimentacion, la voz del creador va de 91 a
148 Hz (percentiles 10-90): con «más grave» y solo -2,5 dB salían 72 frases suyas; por eso lo grave pide 6 dB, y por
eso pyin en su suelo (70 Hz: tono no medido) no cuenta como grave. Ajustables en ajustes.py: TONO_OTRA, DB_OTRA,
TONO_GRAVE, DB_GRAVE, DB_LEJOS (si salen frases del creador, sube TONO_GRAVE o baja DB_GRAVE).
Es orientativo: Claude no oye. Las candidatas se confirman por el sentido (¿responde al creador? ¿le habla de tú?) y,
las dudosas, se preguntan.

  voces.py            lista las candidatas, marcando las que ya están en VOZ_DISFRAZ
Desde código: candidatas() -> [(t0, t1, texto, tono, dB)];  buscar_oido(frase, n) -> (t0, t1) en segundos de salida."""
import difflib, json, os, subprocess, sys
import numpy as np
from comun import AQUI, IDIOMA, PY, TRABAJO, ajuste, norm

VOZ, VJ, CACHE = f"{TRABAJO}/voz.wav", f"{TRABAJO}/voz.json", f"{TRABAJO}/voces.npz"
# La otra voz puede ser MÁS AGUDA o MÁS GRAVE que la del creador: se miran las dos direcciones a la vez.
# vaciamos-estanque (2026-11-19): quien grababa iba a ~95 Hz y el creador a ~116 Hz (x1,22 más grave) y muy lejos del micro.
TONO_OTRA = float(ajuste("TONO_OTRA", 1.38))      # más aguda: tono >= creador x TONO_OTRA
TONO_GRAVE = float(ajuste("TONO_GRAVE", 1.15))    # más grave: tono <= creador / TONO_GRAVE
if TONO_OTRA < 1: TONO_OTRA, TONO_GRAVE = 99.0, 1 / TONO_OTRA      # compatibilidad con quien ya puso TONO_OTRA = 0.72
DB_OTRA = float(ajuste("DB_OTRA", -2.5))          # cuánto más baja llega la voz más aguda (lejos del micro)
DB_GRAVE = float(ajuste("DB_GRAVE", -6.0))        # la más grave tiene que llegar bastante más baja: el creador también baja de tono
DB_LEJOS = float(ajuste("DB_LEJOS", -12.0))       # DUDOSAS: muy bajas, sea cual sea su tono (se listan, no avisan)
TONO_MIN = 75.0                                   # pyin mide desde 70 Hz: por debajo de esto el tono no está medido


def oido():
    """Transcripción de lo que suena en voz.wav (la rehace si voz.wav es más nueva: voz.json viejo = tiempos falsos)."""
    if not os.path.exists(VJ) or os.path.getmtime(VJ) < os.path.getmtime(VOZ):
        subprocess.run([PY, f"{os.path.dirname(AQUI)}/transcribir.py", VOZ, VJ, "--idioma", IDIOMA or "auto"], check=True,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    return json.load(open(VJ, encoding="utf-8"))["frases"]


def buscar_oido(frase, n=-1, cerca=None):
    """La frase en lo que SUENA (voz.json), por parecido de palabras (Whisper oye «toca» por «toque»). Devuelve (t0, t1)
    en segundos, o None si nada se parece lo bastante.
    cerca: segundo donde la pone la línea del EDL (si la frase está en su texto): se coge la más parecida a ±8 s de ahí.
    Sin cerca (lo que dice quien graba entre palabras del EDL): entre las que se parecen casi tanto como la mejor, la n
    (0 la primera vez, -1 la última). Lección: con un umbral fijo de 0,6 una frase corta («¿Qué ha pasado?») casaba con
    otra parecida un minuto después."""
    W = [(norm(w["p"]), w["t"], w["fin"]) for f in oido() for w in f["palabras"] if norm(w["p"])]
    q = [norm(x) for x in frase.split() if norm(x)]; L = len(q); hall = []     # norm() quita los espacios: palabra a palabra
    for i in range(len(W)):
        if cerca is not None and abs(W[i][1] - cerca) > 8: continue
        best = None
        for k in (L - 2, L - 1, L, L + 1, L + 2):
            if k < max(1, L - 2) or i + k > len(W): continue
            r = difflib.SequenceMatcher(None, q, [w[0] for w in W[i:i + k]], autojunk=False).ratio()
            if best is None or r > best[0]: best = (r, k)
        if best and best[0] >= 0.6: hall.append((best[0], i, best[1]))
    if not hall: return None
    top = max(h[0] for h in hall)
    if cerca is not None: r, i, k = max(hall, key=lambda h: (h[0], -abs(W[h[1]][1] - cerca)))
    else:
        hall = [h for h in hall if h[0] >= top - 0.08]
        hall.sort(key=lambda h: -h[0]); elegidas = []          # quita solapes: de las ventanas que se pisan, la más parecida
        for r, i, k in hall:
            if all(i + k <= j or j + m <= i for _, j, m in elegidas): elegidas.append((r, i, k))
        elegidas.sort(key=lambda h: h[1]); r, i, k = elegidas[n]
    return W[i][1], W[i + k - 1][2]


def medidas():
    import librosa
    if os.path.exists(CACHE) and os.path.getmtime(CACHE) > os.path.getmtime(VOZ):
        d = np.load(CACHE); return d["f0"], d["rms"]
    y, sr = librosa.load(VOZ, sr=16000, mono=True)
    f0, _, _ = librosa.pyin(y, fmin=70, fmax=400, sr=sr, frame_length=1024, hop_length=160)
    rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=160)[0]
    np.savez(CACHE, f0=f0, rms=rms); return f0, rms


def candidatas():
    F, V = oido(), None
    f0, rms = medidas(); fr = []
    for f in F:
        a, b = int(f["desde"] * 100), int(f["hasta"] * 100) + 1
        p, e = f0[a:b], rms[a:b]; ok = ~np.isnan(p)
        if ok.sum() < 5: continue
        fr.append((f["desde"], f["hasta"], f["texto"].strip(), float(np.nanmedian(p)), float(20 * np.log10(np.median(e[ok]) + 1e-9)), b - a))
    tono = np.median([x[3] for x in fr]); nivel = np.median([x[4] for x in fr])
    aguda = lambda x: x[3] >= TONO_OTRA * tono and x[4] <= nivel + DB_OTRA
    grave = lambda x: TONO_MIN <= x[3] <= tono / TONO_GRAVE and x[4] <= nivel + DB_GRAVE
    return [x[:5] for x in fr if aguda(x) or grave(x)], tono, nivel


def dudosas():
    """Frases muy por debajo del nivel del creador (DB_LEJOS) que no son candidatas: para leerlas por el sentido."""
    C, tono, nivel = candidatas(); ya = {x[0] for x in C}; f0, rms = medidas(); out = []
    for f in oido():
        a, b = int(f["desde"] * 100), int(f["hasta"] * 100) + 1; p, e = f0[a:b], rms[a:b]; ok = ~np.isnan(p)
        if ok.sum() < 5 or f["desde"] in ya: continue
        db = float(20 * np.log10(np.median(e[ok]) + 1e-9))
        if db <= nivel + DB_LEJOS: out.append((f["desde"], f["hasta"], f["texto"].strip(), float(np.nanmedian(p)), db))
    return out


if __name__ == "__main__":
    sys.path.insert(0, os.getcwd()); import plan
    hechas = []
    from comun import Linea, buscar, FPS
    Lv = Linea()
    for c, frase, n in getattr(plan, "VOZ_DISFRAZ", []):
        try: i, j = buscar(Lv.palabras, c, frase, n); cerca = Lv.palabras[i]["o0"] / FPS
        except (Exception, SystemExit): cerca = None
        r = buscar_oido(frase, n, cerca) or ((cerca, Lv.palabras[j]["o1"] / FPS) if cerca is not None else None)
        if r: hechas.append(r)
    C, tono, nivel = candidatas()
    print(f"creador: tono {tono:.0f} Hz, nivel {nivel:.1f} dB. Otra voz = (tono >= {TONO_OTRA * tono:.0f} Hz y nivel <= {nivel + DB_OTRA:.1f} dB) "
          f"o ({TONO_MIN:.0f}-{tono / TONO_GRAVE:.0f} Hz y nivel <= {nivel + DB_GRAVE:.1f} dB)")
    for t0, t1, txt, p, db in C:
        ya = any(min(t1, b) - max(t0, a) > 0.3 * (t1 - t0) for a, b in hechas)
        print(f"{int(t0 // 60)}:{t0 % 60:05.2f}  {p:4.0f} Hz {db:6.1f} dB  {'(en VOZ_DISFRAZ) ' if ya else 'FALTA            '} «{txt}»")
    print(len(C), "candidatas;", sum(1 for c in C if not any(min(c[1], b) - max(c[0], a) > 0.3 * (c[1] - c[0]) for a, b in hechas)), "sin disfrazar")
    D = dudosas()
    if D:
        print(f"\nDUDOSAS (nivel <= {nivel + DB_LEJOS:.1f} dB, cualquier tono; casi siempre el creador hablando bajo): léelas por el sentido")
        for t0, t1, txt, p, db in D:
            ya = any(min(t1, b) - max(t0, a) > 0.3 * (t1 - t0) for a, b in hechas)
            print(f"{int(t0 // 60)}:{t0 % 60:05.2f}  {p:4.0f} Hz {db:6.1f} dB  {'(en VOZ_DISFRAZ) ' if ya else '                 '} «{txt}»")
