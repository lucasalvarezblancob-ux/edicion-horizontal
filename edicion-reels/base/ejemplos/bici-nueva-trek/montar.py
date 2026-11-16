# bici-nueva-trek — construye la pista de voz (voz.wav) y montaje.json (tramos + palabras en tiempo del edit).
# Uso: herramientas/.venv/bin/python estudio/src/videos/bici-nueva-trek/montar.py <carpeta wav 48k mono por clip> <carpeta json Scribe por clip> [v2]
# v1 = corta (59 s) → voz.wav + montaje.json · v2 = larga (saludo a Álvaro + "no tengo ni idea… que me asesoren… he elegido venir aquí") → voz-v2.wav + montaje-v2.json
# Cada tramo: (id, clip, desde, hasta) en s del BRUTO; None en clip = hueco solo con música (dur = hasta).
import json, sys, os, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
WAV, TX = sys.argv[1], sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.join(AQUI, "../../../public/bici-nueva-trek")
TRAMOS = [
 ("hook", "1349", 5.80, 8.55),       # Acompañadme a buscar mi bici nueva a Trek.
 ("venido", "1349", 20.08, 22.85),   # He venido a por la bici, que no la he visto aún.
 ("ensenas", "1349", 27.36, 29.55),  # ¿Me la enseñas? — Claro. ¿Preparado para conocerla?
 ("paseo", None, 0, 1.7),            # música: andando por la tienda
 ("presento", "1307", 55.70, 56.78), # Pues te presento
 ("domane", "1307", 58.58, 61.00),   # la nueva Domane, ¿vale? Que es tu bici,
 ("project", "1307", 61.95, 64.40),  # un Project One con ruedas de carbono.
 ("locura", "1307", 67.10, 68.34),   # Es una locura, tío
 ("mia", "1307", 72.56, 75.15),      # ¿Esta es la mía? — Esta es la tuya. — Buah.
 ("pintaza", "1307", 77.34, 79.92),  # yo no tengo ni idea de bicis, pero tiene una pintaza.
 ("historicos", "1307", 90.04, 92.24), # uno de los modelos históricos de la marca Trek,
 ("sram", "1307", 95.48, 98.52),     # cambio SRAM Force electrónico.
 ("comodo", "1307", 101.64, 104.00), # muy cómodo para estar muchas horas en bici,
 ("ideal", "1307", 104.20, 104.60),  # ideal
 ("empezando", "1307", 104.98, 106.32), # para gente que está empezando
 ("derecha", "1309", 78.40, 80.84),  # Aquí ves como la derecha es para subir
 ("izquierda", "1309", 81.22, 83.76),# y la izquierda para bajar. Y si aprietas los dos,
 ("plato", "1309", 85.40, 86.28),    # cambias el plato.
 ("pedales", "1320", 26.58, 29.62),  # le están montando los pedales y ahora nos subiremos
 ("caigo", "1320", 30.32, 31.46),    # a ver si no me caigo, ¿no?
 ("bidon", None, 0, 0.9),            # música: portabidones
 ("calas", "1321", 7.14, 9.26),      # La primera vez que me pongo unas calas.
 ("casco", None, 0, 0.9),            # música: casco
 ("verdad", "1337", 12.56, 13.54),   # Y ahora la hora de la verdad
 ("casi", "1337", 18.60, 20.56),     # ¿Eh? Uy, ves, casi.
 ("vuelta", None, 0, 1.3),           # música: rodando por la tienda
 ("conseguido", "1339", 18.08, 20.64), # he conseguido subir y dar la primera vuelta
 ("nocaido", "1340", 14.28, 15.13),  # No me he caído, ¿eh?
 ("tenemos", "1359", 8.78, 12.02),   # Bueno, pues ya tenemos bici nueva gracias a Trek Barcelona Centre.
 ("seguidme", "1362", 1.88, 4.20),   # Y si queréis ver mis próximas salidas, seguidme
]
COLA = 1.9  # 2026-11-10: Lucas pidió 1 s más al final para que se vea el cartel de TREK y la tienda
V2 = len(sys.argv) > 3 and sys.argv[3] == "v2"
if V2:
    def cambia(id_, nuevos):
        i = next(k for k, t in enumerate(TRAMOS) if t[0] == id_); TRAMOS[i:i + 1] = nuevos
    cambia("venido", [
        ("saludo", "1349", 15.48, 17.40),    # ¿Qué pasa, Álvaro? ¿Cómo estamos? — ¿Qué tal? — Bien.
        ("venido", "1349", 20.08, 22.85),    # He venido a por la bici… (2026-11-10: fuera "estoy aquí con Álvaro", ya lo saluda antes)
    ])
    cambia("pintaza", [("pintaza", "1307", 78.78, 79.92)])  # tiene una pintaza (2026-11-10: sin el "pero", pedido por Lucas) (el "no tengo ni idea" lo dice después, una sola vez)
    cambia("empezando", [
        ("empezando", "1307", 104.98, 106.32),
        ("niidea", "1309", 4.24, 5.90),      # como ya sabéis, no tengo ni idea de ciclismo
        ("asesoraran", "1309", 6.92, 8.18),  # quería que me asesoraran.
        ("contodo", "1309", 22.38, 24.58),   # me van a asesorar pues con todo.
        ("elegido", "1309", 31.00, 33.14),   # es una de las razones por las que he elegido venir aquí
        ("aconsejar", "1309", 43.10, 45.30), # Sí, claro, nosotros te aconsejaremos en todo.
    ])
# Palabras que Scribe estiró (empezaban tras una pausa larga): se ponen a mano con el inicio medido por energía.
PARCHES = [{"clip": "1349", "w": "¿Qué", "start": 15.52, "end": 15.68}, {"clip": "1349", "w": "¿Me", "start": 27.40, "end": 27.56}, {"clip": "1307", "w": "¿Esta", "start": 72.58, "end": 72.80}]
QUITAR = {("1307", "de,", 91.20)}  # tartamudeo "de, de la marca": en el subtítulo solo una vez
SR = 48000; OBJ = -17.0  # p90 de cada tramo (ventanas 40 ms) → mismo nivel para los dos (Álvaro va ~6 dB más bajo en su micro)
sos = butter(2, 80, "hp", fs=SR, output="sos")
cache = {}
def wav(n):
    if n not in cache:
        y, sr = sf.read(f"{WAV}/{n}.wav"); assert sr == SR; cache[n] = sosfilt(sos, y)
    return cache[n]
def limitar(y, techo=10 ** (-3 / 20), v=int(0.004 * SR)):
    # limitador de picos con anticipación (solo toca transitorios: golpes en el micro de corbata); devuelve nº de muestras tocadas
    from scipy.ndimage import maximum_filter1d, uniform_filter1d
    env = maximum_filter1d(np.abs(y), 2 * v + 1); g = uniform_filter1d(np.minimum(1.0, techo / np.maximum(env, 1e-9)), v)
    return y * g, int((g < 0.999).sum())
pista = []; segs = []; palabras = []; t = 0.0
for id_, clip, a, b in TRAMOS:
    if clip is None:
        pista.append(np.zeros(int(round(b * SR)))); segs.append({"id": id_, "clip": None, "a": 0, "b": b, "t": round(t, 4)}); t += b; continue
    n = int(round((b - a) * SR)); y = wav(clip)[int(round(a * SR)):][:n].copy()
    fr = [20 * np.log10(np.sqrt(np.mean(y[i:i + 1920] ** 2)) + 1e-9) for i in range(0, len(y) - 1920, 1920)]
    g = float(np.clip(OBJ - np.percentile(fr, 90), -8, 10)); y *= 10 ** (g / 20)
    y, tocadas = limitar(y)
    k = int(0.015 * SR); y[:k] *= np.linspace(0, 1, k); y[-k:] *= np.linspace(1, 0, k)
    pista.append(y); segs.append({"id": id_, "clip": clip, "a": a, "b": b, "t": round(t, 4), "ganancia_db": round(g, 1), "limitadas": tocadas})
    for p in json.load(open(f"{TX}/IMG_{clip}.json")) + [x for x in PARCHES if x["clip"] == clip]:
        if p["end"] - p["start"] > 1.5 or (clip == "1349" and 16.8 < p["start"] < 17.0 and p["hablante"] == "speaker_1") or (clip, p["w"], p["start"]) in QUITAR: continue  # Scribe estira la palabra que sigue a un silencio largo
        if a - 0.03 <= p["start"] < b - 0.05:
            palabras.append(  # noqa
                {"w": p["w"], "start": round(max(p["start"], a) - a + t, 3), "end": round(min(p["end"], b) - a + t, 3), "seg": id_})
    t += n / SR
palabras.sort(key=lambda p: p["start"])
pista.append(np.zeros(int(COLA * SR))); y = np.concatenate(pista)
print("dur", round(t + COLA, 2), "pico", round(20 * np.log10(np.abs(y).max()), 1))
sf.write(os.path.join(PUB, "voz-v2.wav" if V2 else "voz.wav"), y, SR, subtype="PCM_16")
json.dump({"dur": round(t + COLA, 3), "segs": segs, "palabras": palabras}, open(os.path.join(AQUI, "montaje-v2.json" if V2 else "montaje.json"), "w"), ensure_ascii=False, indent=1)
for s in segs: print(s)
print(" ".join(p["w"] for p in palabras))
