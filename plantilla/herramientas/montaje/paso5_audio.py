"""Paso 5: audio final SIN música = voz montada + efectos de sonido puntuales, filtrado suave y -14 LUFS.
Efectos: SOLO pegados a gráficos (título, capítulo, rótulo, mapa, cifra…), nunca en cada corte («a veces»).
El mapa tipo -> (sonido, ganancia) se puede cambiar o vaciar en plan.py con SFX = {...}; los sonidos están en
estudio/public/sonidos/. Salida: trabajo/mezcla.wav (sin normalizar, para el paso 6) y trabajo/audio_final.wav."""
import json, subprocess
import numpy as np, soundfile as sf
from comun import CAPAS_JSON, ESTUDIO, FPS, TRABAJO, ajuste
import plan      # después de comun: es quien mete la carpeta del vídeo en el path

SR = 48000; SND = f"{ESTUDIO}/public/sonidos"
SFX = {"titulo": ("impact-bass-1", 0.30), "seccion": ("whoosh-short", 0.22), "trk": ("pop", 0.25), "mapa": ("click-soft", 0.30),
       "suscribe": ("pop", 0.25), "dato": ("pop", 0.2), "golpe": ("whoosh-short", 0.16)}
SFX = {**SFX, **ajuste("SFX", {})}                 # personal/<creador>/ajustes.py: cambia o quita (None) el de un tipo
SFX = {k: v for k, v in getattr(plan, "SFX", SFX).items() if v}   # plan.py del vídeo: sustituye el mapa entero
LUFS = ajuste("LUFS", -14)


def normalizar(entrada, salida):
    """-14 LUFS integrados (o el LUFS de personal/<creador>/ajustes.py), pico real -1,5 dB, en dos pasadas (medir y aplicar lineal)."""
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", entrada, "-af", f"loudnorm=I={LUFS}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", entrada, "-af",
                    f"loudnorm=I={LUFS}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
                    "-ar", str(SR), salida], check=True)
    return m


if __name__ == "__main__":
    C = json.load(open(CAPAS_JSON, encoding="utf-8"))
    y, _ = sf.read(f"{TRABAJO}/voz.wav", dtype="float32")
    # ---- voz disfrazada: lo que dice alguien que no quiere que se le reconozca (quien graba, un tercero) ----
    # plan.py: VOZ_DISFRAZ = [(clip, "frase literal", n), …] -> de la primera a la última palabra de esa frase, tono arriba
    # sin cambiar la duración (voz de pitufo). Cuánto: VOZ_DISFRAZ_TONO en personal/<creador>/ajustes.py (1,45 ≈ +6 semitonos).
    # Lucas, 2026-11-14 (prueba-3): «cuando habla el cámara (señor misterio) […] distorsiona un poco la voz para que no se le
    # reconozca, puede ser como una voz de pitufo».
    disfraz = getattr(plan, "VOZ_DISFRAZ", [])
    if disfraz:
        from comun import Linea, buscar
        Lv, tono = Linea(), float(ajuste("VOZ_DISFRAZ_TONO", 1.45)); xf = int(0.02 * SR)
        for a in disfraz:
            i, j = buscar(Lv.palabras, *a)
            a0 = max(0, int(Lv.palabras[i]["o0"] * SR / FPS) - int(0.08 * SR)); a1 = min(len(y), int(Lv.palabras[j]["o1"] * SR / FPS) + int(0.12 * SR))
            seg = np.ascontiguousarray(y[a0:a1], dtype=np.float32).reshape(a1 - a0, -1)
            raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(seg.shape[1]), "-i", "-", "-af",
                                  f"asetrate={int(SR * tono)},aresample={SR},atempo={1 / tono:.5f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout
            pr = np.frombuffer(raw, np.float32).reshape(-1, seg.shape[1])[:len(seg)]
            pr = np.vstack([pr, np.zeros((len(seg) - len(pr), seg.shape[1]), np.float32)])
            w = np.ones(len(seg), np.float32); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
            y[a0:a1] = (seg * (1 - w[:, None]) + pr * w[:, None]).reshape(y[a0:a1].shape)
            print(f"voz disfrazada {a0 / SR:.2f}-{a1 / SR:.2f} s: «{a[1]}»")
    cache = {}
    def snd(n, vel=1.0):      # vel: el clip al que acompaña va a esa velocidad (un botón acelerado para que quepa); el tono no cambia
        if (n, vel) not in cache:
            ruta = f"{ESTUDIO}/public/{n}" if "/" in n else f"{SND}/{n}.mp3"      # con barra: archivo propio dentro de estudio/public/
            raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", ruta, *(["-af", f"atempo={vel:.4f}"] if abs(vel - 1) > 0.001 else []), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
            cache[(n, vel)] = np.frombuffer(raw, np.float32).reshape(-1, 2)
        return cache[(n, vel)]
    fx = np.zeros_like(y); n = 0
    for it in C["items"]:
        if it.get("snd") or it["t"] in SFX:      # "snd": [archivo, ganancia, velocidad?] en el item (botones, gráficos propios) manda sobre el mapa por tipo
            nombre, g, *v = it.get("snd") or SFX[it["t"]]; s = snd(nombre, float(v[0]) if v else 1.0) * g; o = it["f0"] * SR // FPS; s = s[:len(fx) - o]; fx[o:o + len(s)] += s; n += 1
    sf.write(f"{TRABAJO}/voz_fx_pre.wav", y, SR); sf.write(f"{TRABAJO}/fx.wav", fx, SR)
    # voz: paso alto 80 Hz + compresión suave; luego mezcla con efectos
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", f"{TRABAJO}/voz_fx_pre.wav", "-i", f"{TRABAJO}/fx.wav", "-filter_complex",
                    "[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=160:makeup=2[v];[v][1:a]amix=inputs=2:normalize=0[m]", "-map", "[m]", f"{TRABAJO}/mezcla.wav"], check=True)
    m = normalizar(f"{TRABAJO}/mezcla.wav", f"{TRABAJO}/audio_final.wav")
    print(f"{n} efectos; entrada {m['input_i']} LUFS, LRA {m['input_lra']}")
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", f"{TRABAJO}/audio_final.wav", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    print(r[r.rindex("Summary"):][:400])
