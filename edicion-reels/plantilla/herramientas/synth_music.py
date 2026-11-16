"""Genera una pista de fondo oscura estilo "slowed + reverb" (~27 s).

Uso: python synth_music.py salida.wav [duracion_segundos]
Requiere numpy y scipy.
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
OUT = sys.argv[1]
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 27.0
BPM = 68
BEAT = 60 / BPM
BAR = BEAT * 4
N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def env_adsr(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def place(buf, sig, start):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


# Progresion en Re menor: Dm - Bb - Gm - A (un compas por acorde)
chords = [
    [50, 53, 57, 62],  # Dm
    [46, 50, 53, 58],  # Bb
    [43, 50, 55, 58],  # Gm
    [45, 49, 52, 57],  # A
]
roots = [38, 34, 31, 33]

pad = np.zeros(N)
bass = np.zeros(N)
bell = np.zeros(N)
drums = np.zeros(N)

n_bars = int(np.ceil(DUR / BAR))
for b in range(n_bars):
    start = b * BAR
    ch = chords[b % 4]
    n = int(BAR * SR * 1.15)
    tt = np.arange(n) / SR
    # Pad: sierras desafinadas, filtradas
    s = np.zeros(n)
    for note in ch:
        for det in (-0.12, 0.0, 0.11):
            f = midi(note + det)
            ph = rng.uniform(0, 1)
            s += 2 * ((tt * f + ph) % 1) - 1
    s = lp(s, 900, 4) * env_adsr(n, 0.9, 1.0) / 12
    place(pad, s, start)
    # Sub bajo con ligero glide
    f0 = midi(roots[b % 4])
    sb = np.sin(2 * np.pi * f0 * tt) + 0.25 * np.sin(4 * np.pi * f0 * tt)
    sb *= env_adsr(n, 0.05, 0.5) * 0.55
    place(bass, sb, start)

# Melodia de campana (arpegio lento, una nota por negra con huecos)
mel = [74, 69, 72, 65, 70, 69, 65, 62, 67, 70, 74, 72, 69, 73, 76, 69]
for k in range(int(DUR / BEAT)):
    if k % 8 in (3, 7):
        continue
    note = mel[k % len(mel)]
    n = int(SR * 2.5)
    tt = np.arange(n) / SR
    f = midi(note)
    s = (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2.01 * f * tt)
         + 0.12 * np.sin(2 * np.pi * 3.0 * f * tt))
    s *= np.exp(-tt * 2.2) * np.minimum(1, tt / 0.01) * 0.16
    place(bell, s, k * BEAT)

# Bateria: kick grave + clap/snare lavado, entra tras el compas 1
def kick():
    n = int(SR * 0.9)
    tt = np.arange(n) / SR
    f = 42 + 110 * np.exp(-tt * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-tt * 4.0) * 0.9


def clap():
    n = int(SR * 0.5)
    tt = np.arange(n) / SR
    nz = rng.standard_normal(n)
    nz = hp(lp(nz, 5000), 900)
    e = np.exp(-tt * 14)
    for d in (0.0, 0.012, 0.024):
        e += np.exp(-np.maximum(0, tt - d) * 60) * (tt >= d) * 0.6
    return nz * e * 0.35


def hat():
    n = int(SR * 0.08)
    tt = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-tt * 60) * 0.07


K, C, H = kick(), clap(), hat()
for k in range(int(DUR / BEAT)):
    t0 = k * BEAT
    if t0 < BAR:  # primer compas sin bateria
        continue
    beat_in_bar = k % 4
    if beat_in_bar == 0:
        place(drums, K, t0)
    if beat_in_bar == 2:
        place(drums, C, t0)
    if k % 8 == 6:
        place(drums, K * 0.7, t0 + BEAT * 0.5)
    place(drums, H, t0 + BEAT * 0.5)

# Reverb: impulso de ruido con caida exponencial (~4 s)
def reverb(x, secs=4.0, wet=0.5, damp=3500):
    n = int(SR * secs)
    tt = np.arange(n) / SR
    ir = rng.standard_normal(n) * np.exp(-tt * 6.9 / secs)
    ir = lp(ir, damp)
    ir /= np.sqrt(np.sum(ir ** 2))
    pre = int(0.03 * SR)
    w = fftconvolve(np.concatenate([np.zeros(pre), x]), ir)[: len(x)]
    return (1 - wet) * x + wet * w * 2.2


bus = pad * 1.0 + bell * 0.9 + drums * 0.8
bus = reverb(bus, secs=4.5, wet=0.55)
mix = bus + lp(bass, 180) * 0.9
# Ruido de vinilo suave
mix += lp(rng.standard_normal(N), 3000) * 0.004
# Tono "slowed": oscurecer agudos
mix = lp(mix, 7000)
# Fade in / out
fi, fo = int(1.2 * SR), int(2.5 * SR)
mix[:fi] *= np.linspace(0, 1, fi) ** 2
mix[-fo:] *= np.linspace(1, 0, fo) ** 1.5
# Normalizar y estereo con leve ensanchado
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89
d = int(0.012 * SR)
left = mix
right = np.concatenate([np.zeros(d), mix[:-d]]) * 0.5 + mix * 0.5
stereo = np.stack([left, right], axis=1)
wavfile.write(OUT, SR, (stereo * 32767).astype(np.int16))
print("ok", OUT, DUR)
