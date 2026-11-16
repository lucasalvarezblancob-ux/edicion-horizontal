"""Corrección medida proxy→bruto (como se ven en QuickTime). Uso:
curva_qt.py CARPETA PREFIJO "t1 t2 t3" t_validar SALIDA.cube
Capturas: CARPETA/<P>b_<t>.png (bruto) y <P>p_<t>.png (proxy). Curva por canal con bloques de 6×6 y medianas por tramos de 8 niveles."""
import sys, numpy as np, cv2
D, P, ts, tv, out = sys.argv[1], sys.argv[2], sys.argv[3].split(), sys.argv[4], sys.argv[5]
def L(p): return cv2.imread(p)[:, :, ::-1].astype(np.float32)
def blk(X, k=6):
    X = X[60:-60, 20:-20]
    n0 = (X.shape[0] // k) * k; n1 = (X.shape[1] // k) * k
    B = X[:n0, :n1].reshape(n0 // k, k, n1 // k, k, 3)
    return B.mean((1, 3)).reshape(-1, 3), B.std((1, 3)).mean(-1).reshape(-1)
def pares(t):
    b, sb = blk(L(f"{D}/{P}b_{t}.png")); p, sp = blk(L(f"{D}/{P}p_{t}.png"))
    ok = (sb < 3) & (sp < 3)  # bloques lisos
    return p[ok], b[ok]
Pp = []; Bb = []
for t in ts:
    p, b = pares(t); d = np.abs(p - b).mean()
    print("captura", t, "dif media", round(float(d), 1))
    Pp.append(p); Bb.append(b)
Pp = np.concatenate(Pp); Bb = np.concatenate(Bb)
x = np.arange(256, dtype=np.float32); curvas = []
for c in range(3):
    cx = []; cy = []
    for lo in range(0, 256, 8):
        m = (Pp[:, c] >= lo) & (Pp[:, c] < lo + 8)
        if m.sum() >= 15: cx.append(np.median(Pp[m, c])); cy.append(np.median(Bb[m, c]))
    cx = [0.0] + cx + [255.0]; cy = [0.0] + cy + [255.0]
    y = np.interp(x, cx, cy)
    y = np.maximum.accumulate(y)  # monótona
    y = np.convolve(np.pad(y, 4, mode="edge"), np.ones(9) / 9, mode="valid")
    curvas.append(y)
    print("canal", "RGB"[c], "puntos", len(cx), "64→", round(float(y[64]), 1), "128→", round(float(y[128]), 1), "200→", round(float(y[200]), 1))
# validar
p, b = pares(tv)
pc = np.stack([np.interp(p[:, c], x, curvas[c]) for c in range(3)], -1)
print("validación", tv, "antes", round(float(np.abs(p - b).mean()), 1), "después", round(float(np.abs(pc - b).mean()), 1))
N = 33
with open(out, "w") as f:
    f.write(f"LUT_3D_SIZE {N}\n")
    g = np.linspace(0, 255, N)
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                r = np.interp(g[ri], x, curvas[0]); gg = np.interp(g[gi], x, curvas[1]); bb = np.interp(g[bi], x, curvas[2])
                f.write(f"{r/255:.6f} {gg/255:.6f} {bb/255:.6f}\n")
print("→", out)
