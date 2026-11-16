"""Revisa TODOS los cortes de un montaje (montaje.json de montar_tomas.py / cortar_tomas_energia.py / cortar_pausas.py):
cada borde tiene que caer en silencio y sin voz pegada al otro lado (≥ 0,14 s). Detecta letras comidas al final o al
principio de una toma ("FIN corta voz") y palabras ajenas que se cuelan.

Uso: herramientas/.venv/bin/python herramientas/revisar_cortes.py AUDIO_BRUTO.wav montaje.json [ruido_desde ruido_hasta]
  ruido_desde/hasta: segundos de un tramo SIN voz del bruto para medir el ruido de agudos (por defecto, el 20 % más bajo de todo).
Lee cada aviso: "corta voz" = falta un trozo → corrígelo; "voz N ms después/antes" = hay algo al otro lado separado por un
silencio corto: escúchalo/transcríbelo (apuntador, respiración, retoma descartada…) y decide. (2026-11-11, lagarto-caiman-nido)
"""
import sys, json, numpy as np, librosa
from scipy.signal import butter, sosfilt
sys.stdout.reconfigure(encoding="utf-8")
y, sr = librosa.load(sys.argv[1], sr=48000); m = json.load(open(sys.argv[2], encoding="utf-8"))
W = 0.01; hop = int(W*sr)
hf = sosfilt(butter(4, 3000, "highpass", fs=sr, output="sos"), y)
rms = lambda x: np.array([20*np.log10(np.sqrt(np.mean(x[i:i+hop]**2))+1e-9) for i in range(0, len(x)-hop, hop)])
db, dbh = rms(y), rms(hf); ruido_h = np.percentile(dbh[int(float(sys.argv[3])/W):int(float(sys.argv[4])/W)] if len(sys.argv) > 4 else dbh, 20)
voz = (db > -40) | (dbh > ruido_h + 8); T = lambda t: int(round(t/W))
malos = 0
for i, t in enumerate(m["tramos"]):
    a, b = t["desde"], t["hasta"]
    en_ini = voz[T(a):T(a)+3].any(); en_fin = voz[T(b)-3:T(b)].any()       # ¿el corte cae encima de voz?
    antes = np.where(voz[T(a-0.14):T(a)])[0]; despues = np.where(voz[T(b):T(b+0.14)])[0]  # ¿voz pegada al otro lado?
    msg = []
    if en_ini: msg.append("INICIO corta voz")
    if en_fin: msg.append("FIN corta voz")
    if len(antes): msg.append(f"voz {int((0.14-antes[-1]*W)*1000)} ms ANTES del inicio")
    if len(despues): msg.append(f"voz {int(despues[0]*W*1000)} ms DESPUÉS del fin")
    malos += bool(msg)
    print(f"{i:2d} {a:7.2f}-{b:7.2f}  {'OK' if not msg else '⚠ ' + '; '.join(msg)}   {t['nota'][:40]}")
print(f"{malos} tramos con aviso")
