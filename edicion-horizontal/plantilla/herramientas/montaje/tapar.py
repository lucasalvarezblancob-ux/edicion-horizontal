"""tapar.py: difumina una MATRÍCULA (o un cartel o pantalla pequeños) SOLO en su sitio, fotograma a fotograma.
Regla de la base: toda matrícula legible se difumina siempre, ajustada a la matrícula y sin tapar nada más.

En plan.py:
  TAPAR = [(clip, t0, t1, [(t_ref, (x0, y0, x1, y1), a, b), ...]), ...]
    t0-t1   tramo del BRUTO (s) en que la matrícula puede verse (aunque sea a ratos o medio tapada)
    t_ref   un instante en que se ve nítida, al menos en parte
    caja    la matrícula ENTERA en ese fotograma, en píxeles del bruto, ajustada a sus bordes (si algo tapa un trozo,
            la caja abarca igualmente la matrícula completa; mírala en un recorte a tamaño real)
    a, b    qué fracción del ancho de la caja se ve LIMPIA en ese fotograma (0-1). Entera: 0, 1. Si un retrovisor tapa
            el centro, da dos referencias: (t, caja, 0, 0.4) y (t, caja, 0.75, 1). Cuantas más partes limpias, mejor.

Uso (desde out/<slug>/, después de paso3_plan.py):
  tapar.py seguir     busca la matrícula en cada fotograma del tramo -> trabajo/tapado/<clip>_<f0>.json
  tapar.py parches    por cada plano del montaje que la enseña, un vídeo pequeño con alfa (solo el trozo difuminado)
                      -> trabajo/tapado/p<o>.mov + .json; paso4_render.py lo pone encima del bruto ANTES del zoom
  tapar.py hoja       trabajo/tapado/hoja_N.jpg: antes y después, cada 0,2 s. OBLIGATORIO mirarlas todas.
Cómo funciona: busca en cada fotograma los trozos limpios de las referencias (a varios tamaños); de ahí sale el rectángulo
de la matrícula. Dentro de ese rectángulo solo se difuminan las franjas en que hay algo que leer: lo que la tapa (un
hombro, una sudadera) no se toca.
Cuando algo la tapa casi entera ya no se encuentra así, pero puede ASOMAR UNA ESQUINA (la banda azul y una cifra: se
lee). Para eso hay una segunda pasada: lo que rodea a la matrícula (pilotos, emblema, portón) se sigue fotograma a
fotograma desde la última vez que se vio y desde la siguiente, y donde eso dice que estaría se busca un EXTREMO de la
matrícula con su borde de coche. Si aparece, ese fotograma también se difumina, pero solo lo que TOCA esa esquina; si
no aparece, no se toca nada (un pliegue de la sudadera no es una matrícula).
Si en la hoja queda un fotograma legible: añade una referencia de ese momento (mejor una en que se vea un extremo
limpio: a = 0 o b = 1). En la hoja, los fotogramas sin matrícula localizada salen con el campo ABIERTO al doble, por si
asoma por otro lado: se miran igual que los demás, y los dudosos, además, a tamaño real.
Límite: una matrícula de menos de ~24 px de alto en el bruto (un coche lejos, al fondo de la calle) no se sigue; a ese
tamaño tampoco se lee. Compruébalo en un recorte a tamaño real y, si ampliada se intuyen cifras, dilo al entregar."""
import json, os, subprocess, sys
import numpy as np, cv2
from comun import FPS, TRABAJO, bruto, video, fuente
import plan      # después de comun

TAPAR = getattr(plan, "TAPAR", [])
D = f"{TRABAJO}/tapado"; os.makedirs(D, exist_ok=True)
NF = 12            # franjas verticales de la matrícula: se difuminan solo las que tienen algo legible
UMBRAL = 0.90      # parecido mínimo de un trozo con su referencia para dar la matrícula por ENCONTRADA (las falsas se quedan en ~0,86)
ESC = (0.6, 1.7)   # tamaños admitidos respecto a la referencia (más pequeña que 0,6 ya no se lee; evita falsos positivos)
MARGEN = 0.12      # la zona difuminada sobresale un 12 % del alto de la matrícula por cada lado, no más
TROZO = 0.80       # parecido mínimo de una ESQUINA de la matrícula (con su borde de coche) para darla por vista cuando el resto está tapado
TROZO_FINO = 0.60  # lo mismo cuando su sitio se sabe con seguridad (vecinos validados): se busca en +-7 px y basta con menos (tapada del todo no pasa de ~0,56)
COLA = 3           # fotogramas que se alarga cada aparición por delante y por detrás (entradas y salidas borrosas)


def medidas(f):
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", f], capture_output=True, text=True).stdout)["streams"][0]
    return s["width"], s["height"]


def leer(clip, t, n, speed=1.0, escala=1, gris=False):
    """Fotogramas del bruto tal como los lee paso4 (misma búsqueda y mismo fps), como generador de matrices."""
    w, h = medidas(bruto(clip)); w2, h2 = w // escala, h // escala
    vf = f"setpts=(PTS-STARTPTS)/{speed},fps={FPS}" + (f",scale={w2}:{h2}:flags=area" if escala > 1 else "")
    ent, pre = fuente(clip, t, n * speed / FPS)          # bruto HDR: su copia SDR (sdr.py), para que el parche tenga el color del montaje
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", *ent[:-2], "-t", f"{n * speed / FPS + 0.5:.3f}", *ent[-2:], "-vf", pre + vf, "-frames:v", str(n),
                          "-pix_fmt", "gray" if gris else "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    tam = w2 * h2 * (1 if gris else 3)
    for _ in range(n):
        b = p.stdout.read(tam)
        if len(b) < tam: break
        yield np.frombuffer(b, np.uint8).reshape((h2, w2) if gris else (h2, w2, 3))
    p.stdout.close(); p.wait()


def plantillas(clip, refs):
    """Trozos limpios de cada referencia, a media resolución: (imagen, desplazamiento x dentro de la caja, ancho y alto de la caja)."""
    T = []
    for tr, caja, *ab in refs:
        a, b = ab if ab else (0.0, 1.0)
        g = next(leer(clip, round(tr * FPS) / FPS, 1, escala=2, gris=True)); x0, y0, x1, y1 = [v // 2 for v in caja]; bw, bh = x1 - x0, y1 - y0
        trozos = [(a, b)] + ([(a, (a + b) / 2), ((a + b) / 2, b)] if b - a > 0.6 else [])
        for c, d in trozos: T.append((g[y0:y1, x0 + int(c * bw):x0 + int(d * bw)].copy(), int(c * bw), bw, bh))
    return T


def buscar(g, T, escalas, zona):
    X0, Y0, X1, Y1 = zona; reg = g[Y0:Y1, X0:X1]; mejor = (0.0, None)
    for tpl, dx, bw, bh in T:
        for s in escalas:
            t = cv2.resize(tpl, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
            if s < ESC[0] or s > ESC[1] or t.shape[0] < 12 or t.shape[1] < 20 or t.shape[0] >= reg.shape[0] or t.shape[1] >= reg.shape[1]: continue
            r = cv2.matchTemplate(reg, t, cv2.TM_CCOEFF_NORMED); _, v, _, p = cv2.minMaxLoc(r)
            if v > mejor[0]: mejor = (v, (X0 + p[0] - dx * s, Y0 + p[1], bw * s, bh * s, s))
    return mejor


def esquinas(clip, refs):
    """Trozos pequeños de los EXTREMOS limpios de la matrícula, con un margen del coche alrededor (el borde oscuro contra
    la chapa clara los hace inconfundibles): (imagen, dx y dy del trozo respecto a la caja, ancho y alto de la caja)."""
    E = []
    for tr, caja, *ab in refs:
        a, b = ab if ab else (0.0, 1.0)
        g = next(leer(clip, round(tr * FPS) / FPS, 1, escala=2, gris=True)); x0, y0, x1, y1 = [v // 2 for v in caja]; bw, bh = x1 - x0, y1 - y0; mg = int(round(bh * 0.3))
        for lado in ("izq", "der"):
            if (lado == "izq" and a > 0.02) or (lado == "der" and b < 0.98): continue        # solo extremos de verdad: llevan el borde
            for fr in (0.17, 0.26, 0.36):
                if fr > b - a + 0.01: continue
                c, d = (a, a + fr) if lado == "izq" else (b - fr, b)
                X0, X1 = x0 + int(c * bw) - (mg if lado == "izq" else 0), x0 + int(d * bw) + (mg if lado == "der" else 0); Y0, Y1 = y0 - mg, y1 + mg
                if X0 >= 0 and Y0 >= 0 and X1 <= g.shape[1] and Y1 <= g.shape[0]: E.append((g[Y0:Y1, X0:X1].copy(), X0 - x0, Y0 - y0, bw, bh, c, d))
    return E


def vecinos(g, r):
    """Trozos con dibujo ALREDEDOR de la matrícula (pilotos, emblema, portón): dicen dónde está cuando algo la tapa."""
    x, y, w, h = r; out = []
    for ox in (-1.15, 0.0, 1.15):
        for oy in (-2.3, 0.0, 2.3):
            if not ox and not oy: continue
            c, a = int(round(x + ox * w)), int(round(y + oy * h - h / 2)); d, b = c + int(w), a + int(2 * h)
            if a < 0 or c < 0 or b > g.shape[0] or d > g.shape[1]: continue
            t = g[a:b, c:d]
            if float(t.std()) >= 18: out.append((t.copy(), c - x, a - y))
    return out


def arrastrar(G, Rh, i0, sg):
    """Desde i0 (matrícula encontrada) hacia sg (+1 o -1), mientras siga perdida: cada vecino se sigue POR SU CUENTA y
    propone dónde estaría la matrícula. Unos vecinos son coche y otros son el hombro que la tapa (y se mueven con él):
    un vecino queda VALIDADO si llega vivo a la siguiente aparición y acierta dónde está (es coche). Devuelve una lista
    de (validado, {índice: (x, y, w, h)}). Un vecino sin encontrar 8 fotogramas se abandona."""
    x, y, w, h = Rh[i0]; A = [[t, x + dx, y + dy, dx, dy, 0, {}] for t, dx, dy in vecinos(G[i0], Rh[i0])]; i = i0 + sg
    while 0 <= i < len(G) and Rh[i] is None and any(q[5] <= 8 for q in A):
        g = G[i]
        for q in A:
            t, px, py, dx, dy, fallos, tr = q
            if fallos > 8: continue
            m = 24 + 8 * fallos; X0, Y0 = int(max(px - m, 0)), int(max(py - m, 0)); reg = g[Y0:int(py + t.shape[0] + m), X0:int(px + t.shape[1] + m)]
            if reg.shape[0] <= t.shape[0] or reg.shape[1] <= t.shape[1]: q[5] += 1; continue
            _, v, _, pt = cv2.minMaxLoc(cv2.matchTemplate(reg, t, cv2.TM_CCOEFF_NORMED))
            if v >= 0.8: q[1], q[2], q[5] = X0 + pt[0], Y0 + pt[1], 0; tr[i] = (q[1] - dx, q[2] - dy, w, h)
            else: q[5] += 1
        i += sg
    fin = Rh[i] if 0 <= i < len(G) else None; out = []
    for t, px, py, dx, dy, fallos, tr in A:
        ok = fin is not None and fallos <= 2 and abs(px - dx - fin[0]) <= 10 and abs(py - dy - fin[1]) <= 10
        if tr: out.append((ok, tr))
    return out


def por_esquina(clip, f0, R, refs):
    """Segunda pasada sobre los huecos de R (matrícula perdida): donde sus vecinos dicen que estaría, se busca una esquina.
    Con vecinos validados (coche seguro) se busca justo ahí (+-7 px, umbral TROZO_FINO); con los demás, en +-22 px y con
    TROZO. Devuelve {índice: [x, y, w, h, parecido]} a tamaño real de los fotogramas en que la esquina aparece, y
    {-índice-1: parecido} de los que no (para el informe)."""
    N = len(R); idx = [i for i in range(N) if R[i]]; E = esquinas(clip, refs)
    if not idx or len(idx) == N or not E: return {}
    xs = [R[i][0] / 2 for i in idx]; ys = [R[i][1] / 2 for i in idx]; w = max(R[i][2] / 2 for i in idx); h = max(R[i][3] / 2 for i in idx)
    cx0, cy0, cx1, cy1 = int(max(min(xs) - 2.8 * w - 60, 0)), int(max(min(ys) - 5.5 * h - 60, 0)), int(max(xs) + 3.8 * w + 60), int(max(ys) + 6.5 * h + 60)
    G = [g[cy0:cy1, cx0:cx1].copy() for g in leer(clip, f0 / FPS, N, escala=2, gris=True)]; Rh = [None] * len(G); C = {}
    for i in idx:
        if i < len(G): Rh[i] = (R[i][0] / 2 - cx0, R[i][1] / 2 - cy0, R[i][2] / 2, R[i][3] / 2)
    for i in idx:
        if i >= len(G): continue
        for sg in (1, -1):
            if 0 <= i + sg < len(G) and Rh[i + sg] is None:
                for ok, tr in arrastrar(G, Rh, i, sg):
                    for k, c in tr.items(): C.setdefault(k, {True: [], False: []})[ok].append(c)
    out = {}
    for k, cc in C.items():
        fino = bool(cc[True]); cand = cc[True] or cc[False]; m = 7 if fino else 22
        g = G[k]; vistos = []; mejor = (0.0, None)
        for x, y, w, h in cand:
            if any(abs(x - a) <= 4 and abs(y - b) <= 4 for a, b in vistos): continue
            vistos.append((x, y))
            for tpl, ex, ey, bw, bh, fc, fd in E:
                for sc in (0.94 * w / bw, w / bw, 1.06 * w / bw):
                    t = cv2.resize(tpl, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_LINEAR)
                    X0, Y0 = int(max(x + ex * sc - m, 0)), int(max(y + ey * sc - m, 0)); reg = g[Y0:int(y + ey * sc + t.shape[0] + m), X0:int(x + ex * sc + t.shape[1] + m)]
                    if reg.shape[0] <= t.shape[0] or reg.shape[1] <= t.shape[1]: continue
                    _, v, _, pt = cv2.minMaxLoc(cv2.matchTemplate(reg, t, cv2.TM_CCOEFF_NORMED))
                    if v > mejor[0]: mejor = (v, (X0 + pt[0] - ex * sc, Y0 + pt[1] - ey * sc, bw * sc, bh * sc), (round(fc, 2), round(fd, 2)))
        if mejor[0] >= (TROZO_FINO if fino else TROZO):
            x, y, w, h = mejor[1]; out[k] = [round((x + cx0) * 2, 1), round((y + cy0) * 2, 1), round(w * 2, 1), round(h * 2, 1), round(mejor[0], 2), int(fino), mejor[2]]
        elif mejor[1] is not None: out[-k - 1] = [round(mejor[0], 2), int(fino)]
    return out


def seguir():
    for clip, t0, t1, refs in TAPAR:
        f0, f1 = round(t0 * FPS), round(t1 * FPS); T = plantillas(clip, refs); R = []; ult = None; hace = 99
        clave = json.dumps([clip, t0, t1, refs, UMBRAL, ESC]); cache = f"{D}/{clip}_{f0}.busqueda.json"      # la primera pasada es la lenta: no se repite si nada cambia
        if os.path.exists(cache) and json.load(open(cache)).get("clave") == clave: R = json.load(open(cache))["R"]
        for i, g in enumerate(leer(clip, f0 / FPS, f1 - f0, escala=2, gris=True) if not R else ()):
            H, W = g.shape
            if ult is not None and hace <= 12:        # cerca de donde estaba
                x, y, w, h, s = ult; m = 70 + 14 * hace
                zona = (int(max(x - m, 0)), int(max(y - m, 0)), int(min(x + w + m, W)), int(min(y + h + m, H))); esc = [s * k for k in (0.9, 0.95, 1.0, 1.05, 1.1)]
            else:                                     # perdida: todo el fotograma, todos los tamaños
                zona = (0, 0, W, H); esc = [ESC[0] * 1.07 ** k for k in range(16)]
            v, r = buscar(g, T, esc, zona)
            if v >= UMBRAL: ult = r; hace = 0; R.append([round(c * 2, 1) for c in r[:4]] + [round(v, 2)])
            else: hace += 1; R.append(None)
        json.dump({"clave": clave, "R": R}, open(cache, "w"))
        # huecos cortos: se interpola; cada aparición se alarga COLA fotogramas con la última posición y velocidad
        N = len(R); P = [r[:4] if r else None for r in R]; V = por_esquina(clip, f0, P, refs)
        casid = {str(-k - 1): v for k, v in V.items() if k < 0}; casi = sorted(v[0] for v in casid.values()); V = {k: v for k, v in V.items() if k >= 0}
        for k, r in V.items(): P[k] = r[:4]
        idx = [i for i in range(N) if P[i]]
        for a, b in zip(idx, idx[1:]):
            if 1 < b - a <= 10:
                for k in range(a + 1, b): P[k] = [P[a][j] + (P[b][j] - P[a][j]) * (k - a) / (b - a) for j in range(4)]
        Q = list(P)
        for i in range(N):
            if P[i] is None: continue
            for sg in (1, -1):
                if 0 <= i + sg < N and P[i + sg] is None:
                    vel = [P[i][j] - P[i - sg][j] for j in range(2)] if 0 <= i - sg < N and P[i - sg] else [0, 0]
                    for k in range(1, COLA + 1):
                        if 0 <= i + sg * k < N and Q[i + sg * k] is None: Q[i + sg * k] = [P[i][0] + vel[0] * k, P[i][1] + vel[1] * k, P[i][2], P[i][3]]
        # suavizado ligero de la posición (la búsqueda baila 1-2 px)
        S = [None if q is None else list(q) for q in Q]
        for i in range(N):
            if Q[i] is None: continue
            vec = [Q[k] for k in range(max(i - 2, 0), min(i + 3, N)) if Q[k] is not None and abs(Q[k][0] - Q[i][0]) < 40]
            S[i] = [float(np.mean([q[j] for q in vec])) for j in range(4)]
        claro = float(np.mean([(np.percentile(t[0], 10) + np.percentile(t[0], 90)) / 2 for t in T]))
        json.dump({"clip": clip, "f0": f0, "claro": claro, "R": S, "puntos": [r[4] if r else V[i][4] if i in V else 0 for i, r in enumerate(R)], "esquina": sorted(V), "seguro": sorted(k for k, v in V.items() if v[5]), "ancla": {str(k): v[6] for k, v in V.items()}, "casi": casid},
                  open(f"{D}/{clip}_{f0}.json", "w"))
        print(f"{clip} {t0}-{t1} s: matrícula encontrada en {len(idx) - len(V)} de {N} fotogramas, y solo su esquina en {len(V)} más"
              + (f" (parecido {min(v[4] for v in V.values()):.2f}-{max(v[4] for v in V.values()):.2f})" if V else "")
              + (f"; sin esquina en {len(casi)} (lo que más se pareció: {casi[-1]:.2f}; umbrales {TROZO_FINO} con su sitio seguro y {TROZO} sin él)" if casi else "") + f"; se tapa en {sum(s is not None for s in S)}")


def mascara(im, r, claro=128.0, ancla=None):
    """Máscara 0-1 (a tamaño real) de lo que hay que difuminar dentro del rectángulo r, o None si no hay nada legible.
    `ancla` = (c, d): fracción del ancho en que se ha visto la esquina; solo se difumina lo que la toca."""
    Hh, Ww = im.shape[:2]; x, y, w, h = r; g = h * MARGEN
    xa, xb, ya, yb = int(round(x - g)), int(round(x + w + g)), int(round(y - g)), int(round(y + h + g))
    xa2, xb2, ya2, yb2 = max(xa, 0), min(xb, Ww), max(ya, 0), min(yb, Hh)
    if xb2 - xa2 < 8 or yb2 - ya2 < 8: return None
    reg = im[ya2:yb2, xa2:xb2]; gris = cv2.cvtColor(reg, cv2.COLOR_BGR2GRAY).astype(np.float32); hsv = cv2.cvtColor(reg, cv2.COLOR_BGR2HSV)
    piel = ((hsv[..., 0] >= 2) & (hsv[..., 0] <= 24) & (hsv[..., 1] > 75) & (hsv[..., 2] > 70))
    msk = np.zeros((Hh, Ww), np.float32); cortes = np.linspace(xa, xb, NF + 1).round().astype(int); vis = []
    for k in range(NF):
        c0, c1 = max(cortes[k], xa2) - xa2, min(cortes[k + 1], xb2) - xa2
        if c1 - c0 < 2: vis.append(False); continue
        vis.append(float(gris[:, c0:c1].std()) >= 17 and float(piel[:, c0:c1].mean()) < 0.5)
    if not any(vis): return None
    for k in range(NF):
        if vis[k]: msk[ya2:yb2, max(cortes[k], xa2):min(cortes[k + 1], xb2)] = 1
    msk[ya2:yb2, xa2:xb2][cv2.dilate(piel.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0      # la piel que asoma no se toca
    # lo que TAPA la matrícula (un retrovisor, una sudadera): zona clara y lisa que entra desde fuera del rectángulo -> fuera
    e = int(h * 0.7); ea, eb, ec, ed = max(ya2 - e, 0), min(yb2 + e, Hh), max(xa2 - e, 0), min(xb2 + e, Ww)
    G = cv2.cvtColor(im[ea:eb, ec:ed], cv2.COLOR_BGR2GRAY).astype(np.float32); mu = cv2.blur(G, (7, 7))
    sd = np.sqrt(np.maximum(cv2.blur(G * G, (7, 7)) - mu * mu, 0)); liso = ((G > claro) & (sd < 10)).astype(np.uint8)
    k = max(5, int(h * 0.16)) | 1; grueso = cv2.morphologyEx(liso, cv2.MORPH_OPEN, np.ones((k, k), np.uint8))   # sin hilos finos: el blanco entre letras no cuenta
    _, lab = cv2.connectedComponents(grueso, connectivity=4); fuera = np.ones(liso.shape, bool); fuera[ya2 - ea:yb2 - ea, xa2 - ec:xb2 - ec] = False
    ids = np.unique(lab[fuera & (grueso > 0)]); O = cv2.dilate((np.isin(lab, ids) & (grueso > 0)).astype(np.uint8), np.ones((7, 7), np.uint8))
    msk[ea:eb, ec:ed][O > 0] = 0
    # los huecos estrechos entre lo que queda (el blanco entre letras) se tapan igual: si no, las letras se adivinan
    k2 = max(9, int(h * 0.45)) | 1; caja = msk[ya2:yb2, xa2:xb2]
    cerr = cv2.morphologyEx(cv2.copyMakeBorder((caja > 0.5).astype(np.uint8), k2, k2, k2, k2, cv2.BORDER_CONSTANT), cv2.MORPH_CLOSE, np.ones((k2, k2), np.uint8))[k2:-k2, k2:-k2]
    cerr[O[ya2 - ea:yb2 - ea, xa2 - ec:xb2 - ec] > 0] = 0; cerr[cv2.dilate(piel.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0] = 0
    cerr = cv2.morphologyEx(cerr, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); n, lab2 = cv2.connectedComponents(cerr, connectivity=8)
    for c in range(1, n):          # un trozo sin nada oscuro dentro (ni letras ni chapa) es un pliegue de ropa, no matrícula
        if float((gris[lab2 == c] < claro - 35).mean()) < 0.06: cerr[lab2 == c] = 0
    if ancla is not None:          # solo se vio una esquina: lo que no la toca es otra cosa (la ropa que tapa el resto)
        a0, a1 = int(round(x + ancla[0] * w - g)) - xa2, int(round(x + ancla[1] * w + g)) - xa2; n3, lab3 = cv2.connectedComponents(cerr, connectivity=8)
        for c in range(1, n3):
            if not (lab3[:, max(a0, 0):max(a1, 0)] == c).any(): cerr[lab3 == c] = 0
    caja[:] = cerr
    if msk[ya2:yb2, xa2:xb2].mean() < 0.04: return None
    return cv2.GaussianBlur(msk, (0, 0), max(1.5, h * 0.05))


def difuminar(im, msk, bh):
    ys, xs = np.where(msk > 0.004)
    if len(ys) == 0: return None
    a, b, c, d = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1; p = int(bh * 1.8)
    A, B, C, Dd = max(a - p, 0), min(b + p, im.shape[0]), max(c - p, 0), min(d + p, im.shape[1])
    reg = im[A:B, C:Dd].astype(np.float32); mm = msk[A:B, C:Dd]; s = bh * 0.5
    # se difumina SOLO con lo de dentro (media ponderada por la máscara): no se cuela el color de alrededor ni sale halo
    num = cv2.GaussianBlur(reg * mm[..., None], (0, 0), s); den = cv2.GaussianBlur(mm, (0, 0), s)[..., None]
    bl = num / np.maximum(den, 1e-3)
    return (int(a), int(b), int(c), int(d)), bl[a - A:b - A, c - C:d - C], msk[a:b, c:d]


def planos_afectados():
    out = []
    for S in [json.load(open(f"{D}/{c}_{round(t0 * FPS)}.json")) for c, t0, *_ in TAPAR]:
        fa, fb = S["f0"], S["f0"] + len(S["R"])
        for v in video():
            if v["clip"] == S["clip"] and v["in"] < fb and v["in"] + v["n"] * v["speed"] > fa: out.append((S, v))
    return out


def rect(S, v, k):
    m = v["in"] + round(k * v["speed"]) - S["f0"]
    return S["R"][m] if 0 <= m < len(S["R"]) else None


def ancla(S, v, k):
    """Si en este fotograma (o, en uno interpolado o de cola, en el más cercano) solo se vio una esquina: su fracción."""
    m = v["in"] + round(k * v["speed"]) - S["f0"]; A = S.get("ancla", {})
    if str(m) in A: return A[str(m)]
    if not A or not 0 <= m < len(S["puntos"]) or S["puntos"][m]: return None       # encontrada entera: sin restricción
    j = min((int(q) for q in A), key=lambda q: abs(q - m))
    return A[str(j)] if abs(j - m) <= 12 else None


def parches():
    for f in os.listdir(D):          # los parches de persona (tapar_persona.py, "persona": true en su .json) no se tocan
        if f.startswith("p") and f.endswith(".json") and not json.load(open(f"{D}/{f}")).get("persona"):
            for e in (".json", ".mov"):
                if os.path.exists(f"{D}/{f[:-5]}{e}"): os.remove(f"{D}/{f[:-5]}{e}")
    for S, v in planos_afectados():
        res = []; caja = None
        for k, im in enumerate(leer(v["clip"], v["in"] / FPS, v["n"], v["speed"])):
            r = rect(S, v, k); msk = mascara(im, r, S.get("claro", 128.0), ancla(S, v, k)) if r else None
            q = difuminar(im, msk, r[3]) if msk is not None else None; res.append(q)
            if q: a, b, c, d = q[0]; caja = (a, b, c, d) if caja is None else (min(caja[0], a), max(caja[1], b), min(caja[2], c), max(caja[3], d))
        nvis = sum(q is not None for q in res)
        if not nvis: continue
        a, b, c, d = caja; a -= a % 2; c -= c % 2; b += (b - a) % 2; d += (d - c) % 2; h, w = b - a, d - c
        o = f"{D}/p{v['o']}"
        if os.path.exists(o + ".json"): raise SystemExit(f"plano o={v['o']}: ya tiene un parche (una persona de tapar_persona.py u otra matrícula); no se pueden tapar dos cosas en el mismo plano")
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", o + ".mov"], stdin=subprocess.PIPE)
        for q in res:
            fr = np.zeros((h, w, 4), np.uint8)
            if q:
                (a2, b2, c2, d2), bl, mk = q
                fr[a2 - a:b2 - a, c2 - c:d2 - c, :3] = np.clip(bl, 0, 255); fr[a2 - a:b2 - a, c2 - c:d2 - c, 3] = np.clip(mk * 255, 0, 255)
            p.stdin.write(fr.tobytes())
        p.stdin.close(); p.wait()
        json.dump({"x": int(c), "y": int(a), "w": int(w), "h": int(h), "visibles": nvis, "n": len(res)}, open(o + ".json", "w"))
        print(f"plano o={v['o']} ({v['clip']} {v['in'] / FPS:.1f} s, {v['n']} f): difuminada en {nvis} fotogramas; parche {w}x{h} en ({c},{a})")


def leerp(f, P):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", f, "-pix_fmt", "bgra", "-f", "rawvideo", "-"], stdout=subprocess.PIPE); tam = P["w"] * P["h"] * 4
    while True:
        b = p.stdout.read(tam)
        if len(b) < tam: break
        yield np.frombuffer(b, np.uint8).reshape(P["h"], P["w"], 4)
    p.stdout.close(); p.wait()


def hoja():
    filas = []; k0 = 0; paso = max(1, round(0.2 * FPS)); centro = None
    for S, v in planos_afectados():
        pj = f"{D}/p{v['o']}.json"; P = json.load(open(pj)) if os.path.exists(pj) else None
        pf = leerp(f"{D}/p{v['o']}.mov", P) if P else iter(())
        tam = next((r for r in S["R"] if r), [0, 0, 300, 70]); W2, H2 = int(tam[2] * 2.4), int(tam[3] * 4.5)
        for k, im in enumerate(leer(v["clip"], v["in"] / FPS, v["n"], v["speed"])):
            fr = next(pf, None); r = rect(S, v, k)
            if r: centro = (r[0] + r[2] / 2, r[1] + r[3] / 2)
            if k % paso or centro is None: continue
            Wc, Hc = (W2, H2) if r else (min(W2 * 2, im.shape[1]), min(H2 * 2, im.shape[0]))      # sin localizar: campo abierto, por si asoma por otro lado
            X = int(np.clip(centro[0] - Wc / 2, 0, im.shape[1] - Wc)); Y = int(np.clip(centro[1] - Hc / 2, 0, im.shape[0] - Hc))
            antes = im[Y:Y + Hc, X:X + Wc].copy(); desp = im.copy()
            if fr is not None:
                al = fr[..., 3:4].astype(np.float32) / 255; reg = desp[P["y"]:P["y"] + P["h"], P["x"]:P["x"] + P["w"]]
                reg[:] = (reg * (1 - al) + fr[..., :3] * al).astype(np.uint8)
            par = np.hstack([antes, desp[Y:Y + Hc, X:X + Wc]]); par = cv2.resize(par, (600, int(par.shape[0] * 600 / par.shape[1])))
            m = v["in"] + round(k * v["speed"]) - S["f0"]; como = " (esquina)" if r and m in S.get("esquina", []) else "" if r else " (SIN LOCALIZAR, campo x2)"
            cv2.putText(par, f"o={v['o'] + k} {(v['in'] + k * v['speed']) / FPS:.1f}s" + como, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1); filas.append(par)
    for i in range(0, len(filas), 30):
        g = filas[i:i + 30]; h = max(x.shape[0] for x in g); g = [cv2.copyMakeBorder(x, 0, h - x.shape[0], 0, 0, cv2.BORDER_CONSTANT) for x in g]
        while len(g) % 3: g.append(np.zeros_like(g[0]))
        cv2.imwrite(f"{D}/hoja_{k0}.jpg", np.vstack([np.hstack(g[j:j + 3]) for j in range(0, len(g), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); k0 += 1
    print(k0, f"hojas en {D}/hoja_N.jpg (izquierda: bruto; derecha: como queda). Míralas TODAS: ninguna matrícula legible, nada más tapado.")


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if not TAPAR: raise SystemExit("plan.py no define TAPAR: nada que difuminar.")
    if orden == "seguir": seguir()
    elif orden == "parches": parches()
    elif orden == "hoja": hoja()
    else: print(__doc__)
