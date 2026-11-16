"""Plan del anuncio meta-ads: planos (cámara frente/lado), cámara virtual que casa la cabeza en cada corte,
palabras en tiempo de salida y voz. Uso: herramientas/.venv/bin/python estudio/src/videos/meta-ads/plan.py CABEZAS.json
Tiempos en segundos del bruto de FRENTE (IMG_1163); lado = frente + OFF (sincronía por audio)."""
import json, sys, os
D = os.path.dirname(os.path.abspath(__file__))
OFF = 7.454
K = {"frente": 1.0, "lado": 1.10}  # la cabeza sale ~10 % más pequeña en el lateral
FPS = 30
cab = json.load(open(sys.argv[1]))
def head(cam, t):
    # medida más cercana
    ks = [k for k in cab if k.startswith(cam + "@")]
    k = min(ks, key=lambda k: abs(float(k.split("@")[1]) - t))
    return cab[k]["cx"], cab[k]["top"]
# (cámara, desde, hasta, zoom inicio, zoom fin) — zoom "efectivo" (tamaño de cabeza relativo al frente sin zoom)
PLANOS = [
    ("frente", 21.50, 22.95, 1.00, 1.16),  # ¿Tu web es muy antigua
    ("lado",   22.95, 24.83, 1.10, 1.17),  # y llevas tiempo pensando en cambiarla?
    ("frente", 32.30, 33.50, 1.06, 1.12),  # Pues no lo pienses más.
    ("frente", 33.50, 35.25, 1.30, 1.36),  # Este Black Friday te la rediseñamos
    ("frente", 35.25, 36.86, 1.06, 1.12),  # por menos de seiscientos euros
    ("lado",   36.86, 38.55, 1.12, 1.20),  # y solo pagas si te gusta.
    ("lado",   60.80, 63.30, 1.06, 1.12),  # Y como un buen diseño no trae clientes por sí solo,
    ("frente", 63.62, 65.48, 1.14, 1.20),  # además la posicionamos
    ("frente", 65.48, 66.80, 1.34, 1.40),  # en Google y ChatGPT.
    ("frente", 76.70, 79.17, 1.04, 1.12),  # Para que los clientes que hoy se van a tu competencia
    ("lado",   79.17, 80.35, 1.15, 1.22),  # te encuentren a ti.
    ("lado",   85.45, 86.97, 1.06, 1.12),  # Solo hasta el 1 de diciembre.
    ("frente", 86.97, 89.75, 1.12, 1.24),  # Déjanos tu web en el formulario.
]
W, H = 1080, 1920
CENTRO = (540, 450)  # adonde tiende la cabeza (cx, top) durante el plano

def clamp(s, A, T):
    x0, x1 = W - s * (W - A[0]), s * A[0]
    y0, y1 = H - s * (H - A[1]), s * A[1]
    return [min(max(T[0], x0), x1), min(max(T[1], y0), y1)]

out = []; t_out = 0.0; prev_end = None
for i, (cam, a, b, z0, z1) in enumerate(PLANOS):
    s0, s1 = z0 * K[cam], z1 * K[cam]
    A = head(cam, a); He = head(cam, b)
    if prev_end is None:
        T0 = [A[0], A[1]]
    else:
        T0 = prev_end
    T0 = clamp(s0, A, T0)
    T1 = [T0[0] + 0.5 * (CENTRO[0] - T0[0]), T0[1] + 0.5 * (CENTRO[1] - T0[1])]
    T1 = clamp(s1, A, T1)
    prev_end = [s1 * (He[0] - A[0]) + T1[0], s1 * (He[1] - A[1]) + T1[1]]
    f0 = round(t_out * FPS); dur = b - a; t_out += dur; f1 = round(t_out * FPS)
    out.append(dict(cam=cam, desde=a, hasta=b, f0=f0, f1=f1, s0=round(s0, 4), s1=round(s1, 4),
                    A=[round(v, 1) for v in A], T0=[round(v, 1) for v in T0], T1=[round(v, 1) for v in T1],
                    cabeza_fin=[round(v, 1) for v in prev_end]))
    print(f"{i:2d} {cam:6s} {a:6.2f}-{b:6.2f} f{f0}-{f1} s {s0:.2f}->{s1:.2f} cabeza ini {T0[0]:.0f},{T0[1]:.0f} fin {prev_end[0]:.0f},{prev_end[1]:.0f}")
total = round(t_out * FPS)
# palabras en tiempo de salida (solo las de cada plano)
pal = json.load(open(os.path.join(D, "palabras-frente.json")))
words = []
for p in out:
    base = p["f0"] / FPS - p["desde"]
    for w in pal:
        if p["desde"] - 0.02 <= w["start"] < p["hasta"] and w.get("hablante") == "speaker_0":
            words.append({"w": w["w"], "start": round(w["start"] + base, 3), "end": round(min(w["end"], p["hasta"]) + base, 3)})
json.dump({"fps": FPS, "total": total, "off": OFF, "planos": out, "palabras": words}, open(os.path.join(D, "plan.json"), "w"), indent=1, ensure_ascii=False)
print("total", total, "frames", total / FPS, "s ·", len(words), "palabras")
print(" ".join(f"{w['w']}@{w['start']:.2f}" for w in words))
