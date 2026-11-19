"""retranscribir.py <clip> <t0> <t1> [--prompt "texto"] [--escribir]: vuelve a transcribir un trozo del bruto SIN filtro de
silencios (VAD), para oír lo que Whisper se saltó (órdenes de rodaje: «corta», «ven», «graba»; respuestas de quien graba).
Desde out/<slug>/. Imprime cada palabra con su segundo del bruto.
  --prompt    palabras que se espera oír (initial_prompt de Whisper), p. ej. --prompt "Corta. Graba. Ven."
  --escribir  cambia en <clip>.w.json las palabras de ese tramo por las nuevas (copia del original en <clip>.w.json.antes);
              después, en edl.py, parte el T() para dejar fuera la orden y repite desde paso1_alinear.py.
Cuándo: un AVISO ESTIRADA de paso1_alinear.py (una palabra alineada que dura demasiado: encima suena algo no transcrito).
Por qué: vaciamos-estanque (Reino Selva, 2026-11-19), «digo "corta" eso sobra»: «Ven, corta.» no estaba en la
transcripción (con VAD) y quedó dentro de la frase; sin VAD y con initial_prompt sí se oye."""
import json, os, shutil, subprocess, sys
import numpy as np
from comun import IDIOMA, TRANSCRIPCIONES, bruto

a = sys.argv[1:]
if len(a) < 3: raise SystemExit(__doc__)
clip, t0, t1 = a[0], float(a[1]), float(a[2])
prompt = a[a.index("--prompt") + 1] if "--prompt" in a else None
pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t0), "-to", str(t1), "-i", bruto(clip), "-ar", "16000", "-ac", "1", "-f", "f32le", "-"],
                     check=True, capture_output=True).stdout
from faster_whisper import WhisperModel
m = WhisperModel(os.environ.get("WHISPER_MODELO", "large-v3-turbo"), device="cpu", compute_type="int8")
segs, _ = m.transcribe(np.frombuffer(pcm, np.float32), language=None if IDIOMA in (None, "", "auto") else IDIOMA, word_timestamps=True,
                       vad_filter=False, initial_prompt=prompt, condition_on_previous_text=False)
nuevas = [{"t": round(t0 + w.start, 2), "fin": round(t0 + w.end, 2), "p": w.word.strip(), "prob": round(w.probability, 2)} for s in segs for w in s.words]
for w in nuevas: print(f"{w['t']:8.2f}-{w['fin']:7.2f}  {w['prob']:.2f}  {w['p']}")
if "--escribir" in a:
    ruta = f"{TRANSCRIPCIONES}/{clip}.w.json"
    if not os.path.exists(ruta + ".antes"): shutil.copy(ruta, ruta + ".antes")
    W = [w for w in json.load(open(ruta, encoding="utf-8")) if w["fin"] <= t0 or w["t"] >= t1] + nuevas
    json.dump(sorted(W, key=lambda w: w["t"]), open(ruta, "w", encoding="utf-8"), ensure_ascii=False)
    print("escrito", ruta, "(original en .antes). Parte el T() en edl.py y repite desde paso1_alinear.py")
