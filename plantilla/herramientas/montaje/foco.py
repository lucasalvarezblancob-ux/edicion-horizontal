"""foco.py: RESALTA algo importante dentro del plano: todo el cuadro pasa a blanco y negro (y algo más oscuro) MENOS el
sujeto, que se queda en color dentro de una elipse de borde suave que lo sigue. Para lo que hay que ver y se pierde en
el plano: un animal pequeño haciendo algo, un detalle, un objeto, una persona entre varias.
Con criterio y sin abusar (base/preferencias.md -> «Resaltar»): uno o dos por vídeo, de 2 a 5 s, y solo donde el
espectador no sabría dónde mirar. Combina con un corte de escala hacia el sujeto (BROLL con zoom) y, si hace falta decir
qué es, con un rótulo con flecha (TRK) en el mismo tramo.

En plan.py:
  FOCOS = [(clip, t0, t1, [cx, cy, rx, ry], {opciones}?), ...]
    t0-t1     tramo del BRUTO (s) con el resalte. Entra y sale con un fundido de 0,25 s; para que ya esté puesto en el
              primer fotograma de un plano, empieza t0 0,3 s antes del corte (y lo mismo t1 con el final)
    elipse    centro y radios del sujeto en t0, en píxeles del bruto (míralo en un recorte a tamaño real): holgada, que
              quepa entero con lo que hace (la presa, la mano, la herramienta)
    opciones  "gris": 1.0 (cuánto se va el color de fuera; 0 = nada), "oscuro": 0.35 (cuánto se oscurece lo de fuera),
              "borde": 0.45 (anchura del borde suave, en radios), "fijo": True (no seguir: sujeto y cámara quietos),
              "en": ancla (solo en el plano que suena en ese frame: ("@marca", s) o (clip, "frase", n). Sin "en", el
              resalte sale en TODOS los planos que usen ese trozo de bruto: también el tráiler y la ráfaga)

Uso (desde out/<slug>/, después de paso3_plan.py):
  foco.py parches   sigue al sujeto y hace, por cada plano del montaje que lo enseña, un vídeo con alfa del tamaño de lo
                    que se ve en ese plano -> trabajo/foco/p<o>.mov + .json; paso4_render.py lo pone encima del bruto
                    ANTES del zoom (igual que los parches de tapar.py). Si cambia un parche, borra su tramo.
  foco.py hoja      trabajo/foco/hoja.jpg: cada plano tal como saldrá, cada 0,4 s. OBLIGATORIO mirarla: el sujeto entero
                    y en color en TODOS los fotogramas (si la elipse se va: tramo más corto, elipse mayor o "fijo")."""
import json, os, subprocess, sys
import numpy as np, cv2
from comun import ALTO, ANCHO, FPS, TRABAJO, Linea, bruto, video, fuente
from dinamica import CARA_Y, encuadre
import plan      # después de comun

FOCOS = getattr(plan, "FOCOS", [])
D = f"{TRABAJO}/foco"; os.makedirs(D, exist_ok=True)
RAMPA = 0.25      # s de fundido de entrada y de salida


def medidas(f):
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", f], capture_output=True, text=True).stdout)["streams"][0]
    return s["width"], s["height"]


def leer(clip, t, n, speed=1.0, ancho=None, gris=False):
    """Fotogramas del bruto tal como los lee paso4 (misma búsqueda y mismo fps)."""
    w, h = medidas(bruto(clip)); w2, h2 = (ancho, 2 * round(ancho * h / w / 2)) if ancho else (w, h)
    vf = f"setpts=(PTS-STARTPTS)/{speed},fps={FPS}" + (f",scale={w2}:{h2}:flags=area" if ancho else "")
    ent, pre = fuente(clip, t, n * speed / FPS)          # bruto HDR: su copia SDR (sdr.py), para que el parche tenga el color del montaje
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", *ent[:-2], "-t", f"{n * speed / FPS + 0.5:.3f}", *ent[-2:], "-vf", pre + vf, "-frames:v", str(n),
                          "-pix_fmt", "gray" if gris else "bgr24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    tam = w2 * h2 * (1 if gris else 3)
    for _ in range(n):
        b = p.stdout.read(tam)
        if len(b) < tam: break
        yield np.frombuffer(b, np.uint8).reshape((h2, w2) if gris else (h2, w2, 3))
    p.stdout.close(); p.wait()


def seguir(clip, t0, t1, el, fijo):
    """Centro de la elipse en cada fotograma del bruto de t0 a t1 (puntos de Lucas-Kanade dentro de la elipse + mediana)."""
    n = round((t1 - t0) * FPS) + 1; cx, cy, rx, ry = el
    if fijo: return [[cx, cy]] * n
    w, _ = medidas(bruto(clip)); sw = 960; k = w / sw; x, y = cx / k, cy / k; pos = [[x, y]]; ant = None
    for g in leer(clip, t0, n, ancho=sw, gris=True):
        if ant is not None:
            m = np.zeros(g.shape, np.uint8); cv2.ellipse(m, (int(x), int(y)), (max(6, int(rx / k)), max(6, int(ry / k))), 0, 0, 360, 255, -1)
            p0 = cv2.goodFeaturesToTrack(ant, 80, 0.01, 3, mask=m)
            if p0 is not None:
                p1, st, _ = cv2.calcOpticalFlowPyrLK(ant, g, p0, None, winSize=(31, 31), maxLevel=3); ok = st.ravel() == 1
                if ok.sum() >= 4: d = np.median((p1 - p0)[ok].reshape(-1, 2), axis=0); x += float(d[0]); y += float(d[1])
            pos.append([x, y])
        ant = g.copy()
    pos = np.array(pos) * k; q = np.ones(7) / 7
    sm = np.stack([np.convolve(np.pad(pos[:, j], 3, mode="edge"), q, "valid") for j in (0, 1)], 1)      # suavizado: la elipse no tiembla
    return sm.round(1).tolist()


def afectados():
    out = []
    for i, (c, t0, t1, el, *op) in enumerate(FOCOS):
        en = (op[0] if op else {}).get("en"); fe = Linea().ancla(en) if en else None
        for v in video():
            if fe is not None and not v["o"] <= fe < v["o"] + v["n"]: continue
            if v["clip"] == c and v["in"] / FPS < t1 and (v["in"] + v["n"] * v["speed"]) / FPS > t0: out.append((i, v))
        if not any(j == i for j, _ in out): print(f"AVISO: el foco {i} ({c} {t0}-{t1} s) no cae en ningún plano" + (" en ese ancla" if en else ""))
    return out


def ventana(v):
    """Trozo del bruto que se ve en el plano (con su zoom más abierto), en píxeles del bruto y con medidas pares."""
    z = min(v["z0"], v["z1"]); w, h, x, y = encuadre(z, v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", CARA_Y))
    x0 = max(0, int(x / z) - 8); y0 = max(0, int(y / z) - 8); x1 = min(ANCHO, int((x + ANCHO) / z) + 9); y1 = min(ALTO, int((y + ALTO) / z) + 9)
    x0 -= x0 % 2; y0 -= y0 % 2; x1 -= (x1 - x0) % 2; y1 -= (y1 - y0) % 2
    return x0, y0, x1, y1


def cuadros(i, v, pos):
    """(fotograma del bruto, alfa del velo, color del velo) de cada fotograma del plano."""
    c, t0, t1, el, *op = FOCOS[i]; o = op[0] if op else {}; gris, osc, borde = o.get("gris", 1.0), o.get("oscuro", 0.35), o.get("borde", 0.45)
    x0, y0, x1, y1 = ventana(v); yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    for k, im in enumerate(leer(c, v["in"] / FPS, v["n"], v["speed"])):
        tb = (v["in"] + k * v["speed"]) / FPS; s = float(np.clip((tb - t0) / RAMPA, 0, 1) * np.clip((t1 - tb) / RAMPA, 0, 1))
        rec = im[y0:y1, x0:x1].astype(np.float32)
        if s <= 0: yield rec, None, None; continue
        m = min(max(round((tb - t0) * FPS), 0), len(pos) - 1); cx, cy = pos[m]
        d = np.sqrt(((xx - cx) / el[2]) ** 2 + ((yy - cy) / el[3]) ** 2); u = np.clip((d - 1) / borde, 0, 1); fuera = u * u * (3 - 2 * u)      # 0 dentro, 1 fuera
        g = cv2.cvtColor(rec, cv2.COLOR_BGR2GRAY)[..., None]; velo = (rec + (g - rec) * gris) * (1 - osc)
        yield rec, fuera * s, velo


def parches():
    for f in os.listdir(D):
        if f.startswith("p") and f.endswith((".mov", ".json")): os.remove(f"{D}/{f}")
    segs = {}
    for i, v in afectados():
        c, t0, t1, el, *op = FOCOS[i]
        if i not in segs: segs[i] = seguir(c, t0, t1, el, (op[0] if op else {}).get("fijo", False)); print(f"foco {i} ({c} {t0}-{t1} s): el sujeto se mueve", np.ptp(np.array(segs[i]), axis=0).round().tolist(), "px")
        x0, y0, x1, y1 = ventana(v); w, h = x1 - x0, y1 - y0; o = f"{D}/p{v['o']}"; n = 0
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", o + ".mov"], stdin=subprocess.PIPE)
        for rec, al, velo in cuadros(i, v, segs[i]):
            fr = np.zeros((h, w, 4), np.uint8)
            if al is not None: fr[..., :3] = np.clip(velo, 0, 255); fr[..., 3] = np.clip(al * 255, 0, 255); n += 1
            p.stdin.write(fr.tobytes())
        p.stdin.close(); p.wait()
        json.dump({"x": x0, "y": y0, "w": w, "h": h, "visibles": n, "n": v["n"], "foco": i}, open(o + ".json", "w"))
        print(f"plano o={v['o']} ({v['clip']} {v['in'] / FPS:.1f} s, {v['n']} f): resaltado en {n} fotogramas; parche {w}x{h} en ({x0},{y0})")
    json.dump(segs, open(f"{D}/seguimiento.json", "w"))
    if not segs: print("Ningún plano del montaje enseña los tramos de FOCOS (¿clip o segundos mal?)")


def hoja():
    segs = {int(k): v for k, v in json.load(open(f"{D}/seguimiento.json")).items()}; cel = []; paso = max(1, round(0.4 * FPS))
    for i, v in afectados():
        el = FOCOS[i][3]
        for k, (rec, al, velo) in enumerate(cuadros(i, v, segs[i])):
            if k % paso: continue
            im = rec if al is None else rec * (1 - al[..., None]) + velo * al[..., None]
            im = cv2.resize(np.clip(im, 0, 255).astype(np.uint8), (640, round(640 * im.shape[0] / im.shape[1])), interpolation=cv2.INTER_AREA)
            cv2.putText(im, f"o={v['o']} +{k / FPS:.1f}s", (8, 24), 0, 0.7, (0, 255, 255), 2); cel.append(im)
    if not cel: print("Nada que enseñar"); return
    h = max(c.shape[0] for c in cel); cel = [cv2.copyMakeBorder(c, 0, h - c.shape[0], 0, 0, cv2.BORDER_CONSTANT) for c in cel]
    while len(cel) % 4: cel.append(np.zeros_like(cel[0]))
    cv2.imwrite(f"{D}/hoja.jpg", np.vstack([np.hstack(cel[r:r + 4]) for r in range(0, len(cel), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 88]); print(f"{D}/hoja.jpg ({len(cel)} celdas): MÍRALA")


if __name__ == "__main__":
    orden = sys.argv[1] if len(sys.argv) > 1 else ""
    if not FOCOS: raise SystemExit("plan.py no tiene FOCOS")
    if orden == "parches": parches()
    elif orden == "hoja": hoja()
    else: raise SystemExit(__doc__)
