"""Cortes de tomas SIN Scribe (sin clave de ElevenLabs): Whisper local da tiempos desfasados (hasta 0,7 s), así que cada borde
se ajusta a la ENERGÍA real del audio. Probado en lagarto-caiman-nido (2026-11-11, bruto con apuntador).

Uso:
  herramientas/.venv/bin/python herramientas/cortar_tomas_energia.py AUDIO.wav TOMAS.json PALABRAS.json SALIDA.json
  AUDIO: el audio del bruto (ffmpeg -i BRUTO -vn -ac 1 -ar 48000 audio.wav).
  TOMAS: [{"desde": s, "hasta": s, "nota": "frase", "fin_max"?: s, "ini_min"?: s}, …] en orden de montaje
         (desde/hasta ≈ primera y última palabra de la toma buena). fin_max/ini_min: tope manual cuando justo al lado
         empieza algo que NO debe entrar (p. ej. el "y" de una retoma descartada pegado a 0,1 s). ⚠️ Un fin_max SOLO después de
         transcribir el trozo con el tope y sin él y comprobar que la palabra sigue entera: la sílaba final nasal y floja
         ("construi-MOS") parece otro sonido y el tope se la comía. Si el tope corta voz medida, el script avisa.
         "fin_revisado": "<qué comprobaste>": final revisado a mano (pasa al montaje; revisar_cortes/revisar_finales lo respetan).
  PALABRAS: [{"desde","hasta","palabras":[{w,start,end}]}] (Whisper por tramos) o lista plana de palabras.
Salida igual que montar_tomas.py: {"fps":30,"tramos":[{desde,hasta,inicio_edit,nota}],"palabras":[…],"duracion"}.

⚠️ La regla que evita comerse letras: el final de la toma es el primer SILENCIO ≥ 0,14 s, NO el primer hueco bajo el
umbral. En español las consonantes finales flojas (z/c = θ, s, f, j) hacen un hueco de 50–120 ms DENTRO de la palabra:
cortando en el primer hueco se perdían "naturalez|a", "termi|tas", "na|ce", "cas|o". La voz se mide en banda completa
(> −40 dB) Y en agudos > 3 kHz (> ruido + 8 dB) para no perder las "s". El final se redondea al frame hacia ARRIBA.
Después, pasa SIEMPRE herramientas/revisar_cortes.py y herramientas/revisar_finales.py.
"""
import sys, json, numpy as np, librosa
from scipy.signal import butter, sosfilt
sys.stdout.reconfigure(encoding="utf-8")
y, sr = librosa.load(sys.argv[1], sr=48000)
tomas = json.load(open(sys.argv[2], encoding="utf-8")); regs = json.load(open(sys.argv[3], encoding="utf-8"))
F = 30; W = 0.01; hop = int(W*sr)
hf = sosfilt(butter(4, 3000, "highpass", fs=sr, output="sos"), y)
rms = lambda x: np.array([20*np.log10(np.sqrt(np.mean(x[i:i+hop]**2))+1e-9) for i in range(0, len(x)-hop, hop)])
db, dbh = rms(y), rms(hf)
ruido_h = np.percentile(dbh, 20)
# banda completa: −40 o el ruido + 6 dB si la sala es más callada (las colas nasales "-mos", "-n" van a −32/−40 dB, graves
# y sin agudos: son la palabra, no otro sonido; 2026-11-16 "construimos" → "construyo")
voz = (db > min(-40, np.percentile(db, 20) + 6)) | (dbh > ruido_h + 8)
T = lambda t: int(round(t/W)); SIL = 0.14
words = [w for r in regs for w in r["palabras"]] if regs and "palabras" in regs[0] else regs
tramos=[]; pal=[]; acc=0.0; usadas=set()
for tm in tomas:
    a, b = tm["desde"], tm["hasta"]
    i = T(a); ult = i                      # inicio: retrocede hasta un silencio ≥ SIL (máx 0,45 s)
    for k in range(T(a), T(a-0.45), -1):
        if voz[k-1]: ult = k-1
        elif (ult - k)*W > SIL: break
    ini = ult*W - 0.05
    j = T(b); ult = j                      # fin: avanza hasta un silencio ≥ SIL (máx 0,6 s)
    for k in range(T(b), T(b+0.6)):
        if voz[k]: ult = k
        elif (k - ult)*W > SIL: break
    fin = (ult+1)*W + 0.10
    if "fin_max" in tm:
        if tm["fin_max"] < fin - 0.05:
            print(f"⚠ fin_max {tm['fin_max']:.2f} corta {fin - tm['fin_max']:.2f} s de voz medida al final de «{tm['nota'][-30:]}»: "
                  "transcribe el trozo con el tope y sin él (revisar_finales.py) y comprueba que la última palabra sigue entera.")
        fin = min(fin, tm["fin_max"])
    if "ini_min" in tm: ini = max(ini, tm["ini_min"])
    seg = [ini]; k = T(ini+0.1)            # pausas internas > 0,35 s → dejar 0,10 a cada lado
    while k < T(fin-0.1):
        if not voz[k]:
            m = k
            while m < T(fin) and not voz[m]: m += 1
            if (m-k)*W > 0.35: seg += [k*W+0.10, m*W-0.10]
            k = m
        else: k += 1
    seg.append(fin)
    ws = [w for w in words if a-0.35 <= w["start"] < b-0.05]
    for n, (s0, s1) in enumerate(zip(seg[::2], seg[1::2])):
        s0 = round(s0*F)/F; s1 = round(s1*F + 0.49)/F   # el final se redondea hacia ARRIBA (nunca recortar la cola)
        tramos.append({"desde": s0, "hasta": s1, "inicio_edit": round(acc,4), "nota": tm["nota"] if n == 0 else "…"})
        if "fin_revisado" in tm and n == len(seg)//2 - 1: tramos[-1]["fin_revisado"] = tm["fin_revisado"]
        for w in ws:
            if id(w) in usadas: continue
            if s0-0.15 <= w["start"] < s1-0.02 or (w["start"] < s0 and w["end"] > s0 + 0.03):   # la 1.ª palabra: Whisper le da un inicio anterior al corte
                usadas.add(id(w))
                pal.append({"w": w["w"], "start": round(acc + max(w["start"], s0) - s0, 3), "end": round(acc + min(w["end"], s1) - s0, 3)})
        acc += s1 - s0
json.dump({"fps":F,"tramos":tramos,"palabras":pal,"duracion":round(acc,3)}, open(sys.argv[4],"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(tramos)} tramos -> {acc:.2f} s")
for t in tramos: print(f"  {t['desde']:7.2f}-{t['hasta']:7.2f} (edit {t['inicio_edit']:6.2f} = f{round(t['inicio_edit']*30)}) {t['nota'][:50]}")
