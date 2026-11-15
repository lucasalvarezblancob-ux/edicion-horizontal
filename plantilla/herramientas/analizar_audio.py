#!/usr/bin/env python3
"""Mapa de voz, música y efectos de un vídeo (referencias o un montaje propio).

Uso: analizar_audio.py VIDEO SALIDA.json [--cortes cortes.json] [--stems DIR] [--sin-demucs]
  1) separa voz / resto con demucs (htdemucs, 4 pistas) -> DIR/vocals.wav, DIR/no_vocals.wav y DIR/ritmo.wav (batería+bajo)
     (se reutilizan si existen). Con --sin-demucs usa HPSS de librosa sobre la mezcla (menos fiable).
  2) por ventana de 1 s: nivel de voz y de resto (dBFS), proporción armónica del resto
  3) música = batería+bajo por encima de -52 dBFS (el ambiente y los efectos no tienen), sostenido >= 4 s
     -> tramos de música con nivel medio y diferencia voz-música mientras se habla
  4) cambios de pista: salto de timbre/tonalidad (MFCC+croma) entre ventanas de 8 s dentro de la música
  5) acentos de sonido: ataques fuertes del resto; cuántos caen a ±0,15 s de un corte (--cortes)
"""
import argparse, json, subprocess, sys, tempfile, os
from pathlib import Path
import numpy as np, librosa, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("video"); ap.add_argument("salida")
ap.add_argument("--cortes"); ap.add_argument("--stems"); ap.add_argument("--sin-demucs", action="store_true")
a = ap.parse_args()
sal = Path(a.salida); stems = Path(a.stems) if a.stems else sal.parent / "stems"
SR = 22050
UMBRAL_RITMO = -52.0

def db(x): return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9))

TROZO = 600   # la separación va por tramos de 10 min: un vídeo largo entero no cabe en 16 GB de RAM
if not a.sin_demucs and not (stems / "ritmo.wav").exists():
    stems.mkdir(parents=True, exist_ok=True)
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                                 capture_output=True, text=True, check=True).stdout.strip())
    acc = {"vocals": [], "ritmo": [], "no_vocals": []}
    t0 = 0.0
    while t0 < total:
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "m.wav")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t0), "-t", str(TROZO), "-i", a.video,
                            "-vn", "-ar", "44100", "-ac", "2", wav], check=True)
            subprocess.run([sys.executable, "-m", "demucs", "-n", "htdemucs", "--segment", "7", "-o", tmp, wav],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            pista = {}
            for nm in ("vocals", "drums", "bass", "other"):
                y, sr = sf.read(os.path.join(tmp, "htdemucs", "m", nm + ".wav"), dtype="float32")
                pista[nm] = librosa.resample(y.mean(axis=1), orig_sr=sr, target_sr=SR)
            acc["vocals"].append(pista["vocals"])
            acc["ritmo"].append(pista["drums"] + pista["bass"])        # bombo/bajo: solo hay con música
            acc["no_vocals"].append(pista["drums"] + pista["bass"] + pista["other"])
        t0 += TROZO
    for nm, v in acc.items(): sf.write(stems / (nm + ".wav"), np.concatenate(v), SR)
    del acc

if a.sin_demucs:
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "m.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-ar", str(SR), "-ac", "1", wav], check=True)
        mix, _ = librosa.load(wav, sr=SR)
    voz, resto, ritmo = mix, mix, None
else:
    voz, _ = librosa.load(stems / "vocals.wav", sr=SR)
    resto, _ = librosa.load(stems / "no_vocals.wav", sr=SR)
    ritmo, _ = librosa.load(stems / "ritmo.wav", sr=SR)
n = min(len(voz), len(resto)) // SR
voz_db = np.array([db(voz[i * SR:(i + 1) * SR]) for i in range(n)])
res_db = np.array([db(resto[i * SR:(i + 1) * SR]) for i in range(n)])

# proporción armónica del resto por segundo (música = tonal y sostenida; ambiente = ruido)
S = np.abs(librosa.stft(resto, n_fft=2048, hop_length=512))
fps = SR / 512
if a.sin_demucs:
    H, P = librosa.decompose.hpss(S, margin=2.0)
    arm = np.array([H[:, int(i * fps):int((i + 1) * fps)].sum() / (S[:, int(i * fps):int((i + 1) * fps)].sum() + 1e-9) for i in range(n)])
    del H, P
else:
    arm = np.zeros(n)

habla = voz_db > -38
if ritmo is not None:
    rit_db = np.array([db(ritmo[i * SR:(i + 1) * SR]) for i in range(n)])
    es_mus = rit_db > UMBRAL_RITMO
else:
    rit_db = res_db
    es_mus = (res_db > -45) & (arm > 0.45)
k = np.ones(5) / 5                                   # suavizar 5 s
es_mus = np.convolve(es_mus.astype(float), k, "same") > 0.5
tramos, i = [], 0
while i < n:
    if es_mus[i]:
        j = i
        while j < n and es_mus[j]: j += 1
        if j - i >= 4:
            h = habla[i:j]
            tramos.append({"desde": i, "hasta": j, "nivel_db": round(float(res_db[i:j].mean()), 1),
                           "con_voz": round(float(h.mean()), 2),
                           "voz_menos_musica_db": round(float((voz_db[i:j][h] - res_db[i:j][h]).mean()), 1) if h.any() else None,
                           "nivel_sin_voz_db": round(float(res_db[i:j][~h].mean()), 1) if (~h).any() else None})
        i = j
    else: i += 1

# cambios de pista dentro de la música
mf = librosa.feature.mfcc(S=librosa.power_to_db(librosa.feature.melspectrogram(S=S ** 2, sr=SR)), n_mfcc=13)
ch = librosa.feature.chroma_stft(S=S ** 2, sr=SR)
def vec(t0, t1):
    s0, s1 = int(t0 * fps), int(t1 * fps)
    return np.concatenate([mf[1:, s0:s1].mean(1) / 20, ch[:, s0:s1].mean(1)])
cambios = []
for t in range(8, n - 8, 2):
    if es_mus[t - 8:t + 8].mean() < 0.9: continue
    u, v = vec(t - 8, t), vec(t, t + 8)
    d = 1 - float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-9))
    cambios.append((t, d))
cp = []
if cambios:
    ds = np.array([d for _, d in cambios]); thr = max(np.percentile(ds, 97), 0.08)
    for t, d in cambios:
        if d >= thr and (not cp or t - cp[-1]["t"] > 12): cp.append({"t": t, "distancia": round(d, 3)})

# acentos de sonido (posibles SFX) y coincidencia con cortes
env = librosa.onset.onset_strength(S=librosa.power_to_db(S ** 2), sr=SR, hop_length=512)
pk = librosa.util.peak_pick(env, pre_max=8, post_max=8, pre_avg=40, post_avg=40, delta=float(np.percentile(env, 99)) * 0.6, wait=10)
acentos = [round(float(p / fps), 2) for p in pk]
info = {}
if a.cortes:
    cj = json.load(open(a.cortes, encoding="utf-8")); ct = np.array([c["t"] for c in cj["cortes"]])
    ac = np.array(acentos) if acentos else np.array([1e9])
    con = [float(c) for c in ct if np.abs(ac - c).min() <= 0.15]
    info = {"cortes": len(ct), "cortes_con_acento": len(con), "proporcion": round(len(con) / max(1, len(ct)), 2),
            "cortes_con_acento_t": [round(c, 2) for c in con]}
    # ¿la música va a ritmo de los cortes? cortes que caen a ±0,08 s de un beat
    tempo, beats = librosa.beat.beat_track(onset_envelope=env, sr=SR, hop_length=512)
    bt = librosa.frames_to_time(beats, sr=SR, hop_length=512)
    enm = [c for c in ct if int(c) < n and es_mus[int(c)]]
    info["cortes_en_musica"] = len(enm)
    info["cortes_en_beat"] = round(sum(np.abs(bt - c).min() <= 0.08 for c in enm) / max(1, len(enm)), 2) if len(bt) else None

dur = n
out = {"video": a.video, "duracion": dur,
       "habla_proporcion": round(float(habla.mean()), 2),
       "musica_proporcion": round(float(es_mus.mean()), 2),
       "primera_musica_s": tramos[0]["desde"] if tramos else None,
       "voz_db_media": round(float(voz_db[habla].mean()), 1) if habla.any() else None,
       "voz_menos_musica_db_mediana": round(float(np.median([t["voz_menos_musica_db"] for t in tramos if t["voz_menos_musica_db"] is not None])), 1) if any(t["voz_menos_musica_db"] is not None for t in tramos) else None,
       "tramos_musica": tramos, "cambios_de_pista": cp,
       "acentos_por_minuto": round(len(acentos) / dur * 60, 1), "acentos": acentos, "acentos_y_cortes": info,
       "por_segundo": {"voz_db": [round(float(x), 1) for x in voz_db], "resto_db": [round(float(x), 1) for x in res_db],
                       "ritmo_db": [round(float(x), 1) for x in rit_db]}}
sal.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k not in ("por_segundo", "acentos", "tramos_musica")}, ensure_ascii=False)[:1500])
print("tramos de música:", len(tramos))
for t in tramos[:40]: print(f'  {t["desde"]//60:02d}:{t["desde"]%60:02d}-{t["hasta"]//60:02d}:{t["hasta"]%60:02d} nivel={t["nivel_db"]} voz-mus={t["voz_menos_musica_db"]} sin_voz={t["nivel_sin_voz_db"]}')
