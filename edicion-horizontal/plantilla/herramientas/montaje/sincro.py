"""sincro.py <clip de la voz> <clip de la otra cámara> [desfase aproximado en s]: mide por correlación del audio el desfase
entre dos cámaras que grabaron a la vez (segundo de la otra = segundo de la voz + desfase) e imprime la línea de SINCRO
para proyecto.py. Desde out/<slug>/. Mide en 5 puntos repartidos por el tramo común: si varían más de 1 fotograma hay
deriva (mide por tramos y usa @sync solo dentro de cada uno).
Sin desfase aproximado, primero lo busca en todo el clip (a 4 kHz) y luego lo afina a 16 kHz en cada punto.
Por qué: vaciamos-estanque-2 (Reino Selva, 2026-11-19), «hay lag con mi voz y mis labios»: la Sony puesta a ojo iba 0,47 s
adelantada. Medido así: iPhone -> Sony 2,817-2,823 s en todo el clip, sin deriva."""
import subprocess, sys
import numpy as np
from comun import FPS, bruto


def pcm(f, t=None, d=None, sr=16000):
    a = ["ffmpeg", "-nostdin", "-v", "error"] + (["-ss", f"{max(0.0, t):.3f}"] if t is not None else []) + (["-t", f"{d:.3f}"] if d else [])
    return np.frombuffer(subprocess.run(a + ["-i", f, "-ar", str(sr), "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


def corr(y, x):
    """Correlación de x (corto) a lo largo de y (largo), por FFT: (posición del mejor, nitidez del pico)."""
    n = 1 << int(np.ceil(np.log2(len(y) + len(x))))
    c = np.fft.irfft(np.fft.rfft(y, n) * np.conj(np.fft.rfft(x, n)), n)[:len(y) - len(x) + 1]
    c = np.abs(c); k = int(np.argmax(c)); return k, float(c[k] / (np.median(c) + 1e-9))


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())


a = sys.argv[1:]
if len(a) < 2: raise SystemExit(__doc__)
voz, otra = bruto(a[0]), bruto(a[1]); Dv, Do = dur(voz), dur(otra)
if len(a) > 2: aprox = float(a[2])
else:      # 20 s del centro de la voz, buscados en toda la otra cámara
    t = Dv / 2 - 10; k, nit = corr(pcm(otra, sr=4000), pcm(voz, t, 20, 4000)); aprox = k / 4000 - t
    print(f"aproximado: {aprox:+.2f} s (nitidez del pico {nit:.0f}; por debajo de ~8 puede ser falso: pásale tú el aproximado)")
t0, t1 = max(0.0, -aprox) + 6, min(Dv, Do - aprox) - 14
if t1 <= t0: raise SystemExit("las dos cámaras no tienen tramo común con ese desfase")
med = []
for t in np.linspace(t0, t1, 5):
    x = pcm(voz, t, 8); y = pcm(otra, t + aprox - 2, 12)
    if len(y) < len(x): continue
    k, nit = corr(y, x); d = aprox - 2 + k / 16000; med.append(d)
    print(f"  voz {t:7.1f} s -> desfase {d:+.3f} s  (nitidez {nit:.0f})")
if not med: raise SystemExit("no se pudo medir")
m = float(np.median(med)); var = max(med) - min(med)
print(f"desfase {m:+.3f} s; variación {var * 1000:.0f} ms" + ("  ¡DERIVA o algún punto falso (más de 1 fotograma)!" if var > 1 / FPS else "  (sin deriva)"))
print(f'SINCRO = {{"{a[1]}": ("{a[0]}", {m:.3f})}}')
