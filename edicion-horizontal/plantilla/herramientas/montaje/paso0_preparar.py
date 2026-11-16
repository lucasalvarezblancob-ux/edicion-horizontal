"""Paso 0: prepara los brutos de un vídeo. Por cada bruto:
  1. ficha técnica (resolución, fps, duración, giro, HDR) -> avisa del lienzo y los fps que tocan;
  2. transcripción con tiempos por palabra (faster-whisper, local) -> ANALISIS/transcripcion/<clip>.json, .txt y .w.json;
     el IDIOMA se DETECTA (nunca se supone): si proyecto.py no lo fija, se imprime el detectado en cada bruto;
  3. posición de la cara 5 veces por segundo (para centrar los zooms) -> trabajo/caras_<clip>.json;
  4. hojas densas, un fotograma por segundo, para el REGISTRO VISUAL -> ANALISIS/visual/hojas/<clip>_NN.jpg.
Lo ya hecho no se repite. Uso: paso0_preparar.py [clip ...]   (sin argumentos: todos los brutos)"""
import json, os, subprocess, sys
from comun import ALTO, ANALISIS, ANCHO, AQUI, BRUTOS, FPS, IDIOMA, PY, TRABAJO, TRANSCRIPCIONES, bruto, clips

H = os.path.dirname(AQUI)   # herramientas/
os.makedirs(TRANSCRIPCIONES, exist_ok=True); os.makedirs(f"{ANALISIS}/visual/hojas", exist_ok=True)
lista = sys.argv[1:] or clips()
if not lista: raise SystemExit(f"No hay brutos en {BRUTOS}")
idiomas = {}
print(f"{'clip':14} {'tamaño':>11} {'fps':>6} {'dur':>8}  notas")
for c in lista:
    f = bruto(c)
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,color_transfer:stream_side_data=rotation:format=duration", "-of", "json", f], capture_output=True, text=True).stdout)
    st = s["streams"][0]; a, b = st["r_frame_rate"].split("/"); fps = float(a) / float(b); dur = float(s["format"]["duration"])
    rot = next((abs(int(float(x["rotation"]))) for x in st.get("side_data_list", []) if "rotation" in x), 0)
    w, h = (st["height"], st["width"]) if rot in (90, 270) else (st["width"], st["height"])
    notas = []
    if st.get("color_transfer") in ("arib-std-b67", "smpte2084"): notas.append("HDR: no hace falta proxy del bruto entero; tras paso3_plan.py, sdr.py convierte a SDR solo los trozos que se usan (comprueba el color de alguno con comparar_color.sh)")
    if h > w: notas.append("VERTICAL (irá con bordes o recortado)")
    if abs(fps - FPS) > 0.5: notas.append(f"fps distintos del proyecto ({FPS})")
    if (w, h) != (ANCHO, ALTO): notas.append(f"tamaño distinto del lienzo ({ANCHO}x{ALTO})")
    print(f"{c:14} {w:>5}x{h:<5} {fps:6.2f} {dur:7.1f}s  {'; '.join(notas)}", flush=True)
    j = f"{TRANSCRIPCIONES}/{c}.json"
    if not os.path.exists(j):
        subprocess.run([PY, f"{H}/transcribir.py", f, j, "--idioma", IDIOMA or "auto"], check=True, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    d = json.load(open(j, encoding="utf-8")); idiomas[c] = d.get("idioma")
    wj = f"{TRANSCRIPCIONES}/{c}.w.json"
    if not os.path.exists(wj) or os.path.getmtime(wj) < os.path.getmtime(j):
        json.dump([p for fr in d["frases"] for p in fr["palabras"]], open(wj, "w", encoding="utf-8"), ensure_ascii=False)
    cj = f"{TRABAJO}/caras_{c}.json"
    if not os.path.exists(cj): subprocess.run([PY, f"{H}/caras.py", f, cj], check=True)
for d in BRUTOS: subprocess.run([PY, f"{H}/hojas_bruto.py", d, f"{ANALISIS}/visual/hojas"], check=True)
print("\nIdioma detectado por bruto:", idiomas)
if not IDIOMA:
    print("-> Pon IDIOMA en proyecto.py con el idioma HABLADO (mira los .txt: si un bruto corto sale en otro idioma, suele ser un error de detección:")
    print("   bórrale el .json y relanza con IDIOMA fijado). Rótulos, título y descripción van en ese idioma.")
print(f"Siguiente: REGISTRO VISUAL de cada bruto (qué se ve en cada momento) con {ANALISIS}/visual/hojas y herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md;")
print("luego escribe edl.py leyendo los .txt de la transcripción.")
