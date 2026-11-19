"""tapar_persona.py: difumina a una PERSONA del fondo que no debe reconocerse (Reino Selva, 2026-11-19, vaciamos-estanque:
«blur a la persona que sale de fondo, no puede saberse quien es»). Desde out/<slug>/, después de paso3_plan.py.
tapar.py sigue matrículas por su forma; una persona que se agacha, se gira y queda medio tapada no se sigue así. Aquí la
caja se da a mano en fotogramas clave (medidos con rejilla.py sobre la copia SDR, cada 0,125 s mientras se mueve) y se
interpola; la zona difuminada sobresale MARGEN px por cada lado para cubrir el error entre claves.
En plan.py:  TAPAR_PERSONAS = [(clip, [(t_bruto, x0, y0, x1, y1), ...]), ...]   (px del bruto; fuera de las claves no se toca)
  tapar_persona.py          -> trabajo/tapado/p<o>.mov + .json (paso4_render.py los pone encima del bruto ANTES del zoom)
  tapar_persona.py hoja     -> trabajo/tapado/persona_N.jpg: el montaje con el parche cada 3 fotogramas. MIRARLAS TODAS.
Si en el mismo vídeo hay matrículas (tapar.py): primero tapar.py parches y DESPUÉS tapar_persona.py (tapar.py no borra los
parches de persona, pero sí los suyos al rehacerlos). Dos cosas que tapar en el mismo plano no se pueden: se para.
Probado en vaciamos-estanque: 22 claves para los 2,7 s del operario, MARGEN 70 px en un bruto 3840x2160, bien a la primera."""
import json, os, subprocess, sys
import numpy as np, cv2
from comun import FPS, TRABAJO, bruto, video
from tapar import leer, leerp, medidas
import plan

D = f"{TRABAJO}/tapado"; os.makedirs(D, exist_ok=True)
MARGEN = 70
PERSONAS = getattr(plan, "TAPAR_PERSONAS", [])


def caja(claves, t):
    if t < claves[0][0] - 0.05 or t > claves[-1][0] + 0.05: return None
    if len(claves) == 1: return list(claves[0][1:5])
    ts = [c[0] for c in claves]; i = int(np.clip(np.searchsorted(ts, t) - 1, 0, len(claves) - 2))
    a, b = claves[i], claves[i + 1]; u = float(np.clip((t - a[0]) / (b[0] - a[0]), 0, 1))
    return [a[k] + (b[k] - a[k]) * u for k in range(1, 5)]


def planos():
    for v in video():
        for clip, claves in PERSONAS:
            if v["clip"] != clip: continue
            t0, t1 = v["in"] / FPS, (v["in"] + v["n"] * v["speed"]) / FPS
            if t1 > claves[0][0] and t0 < claves[-1][0]: yield v, sorted(claves)


def parches():
    for f in os.listdir(D):          # los parches de persona de la vez anterior (los de matrícula, de tapar.py, se quedan)
        if f.startswith("p") and f.endswith(".json") and json.load(open(f"{D}/{f}")).get("persona"):
            for e in (".json", ".mov"):
                if os.path.exists(f"{D}/{f[:-5]}{e}"): os.remove(f"{D}/{f[:-5]}{e}")
    hechos = {}
    for v, claves in planos():
        o = f"{D}/p{v['o']}"
        if v["o"] in hechos or os.path.exists(o + ".json"):
            raise SystemExit(f"plano o={v['o']}: ya hay otra cosa tapada (otra persona o una matrícula); junta las cajas en una")
        AN, AL = medidas(bruto(v["clip"]))
        cajas = [caja(claves, (v["in"] + k * v["speed"]) / FPS) for k in range(v["n"])]
        cajas = [None if c is None else (max(0, int(c[0] - MARGEN)), max(0, int(c[1] - MARGEN)), min(AN, int(c[2] + MARGEN)), min(AL, int(c[3] + MARGEN))) for c in cajas]
        vis = [c for c in cajas if c]
        if not vis: continue
        X0, Y0 = min(c[0] for c in vis), min(c[1] for c in vis); X1, Y1 = max(c[2] for c in vis), max(c[3] for c in vis)
        X0 -= X0 % 2; Y0 -= Y0 % 2; X1 = min(AN, X1 + (X1 - X0) % 2); Y1 = min(AL, Y1 + (Y1 - Y0) % 2); w, h = X1 - X0, Y1 - Y0
        p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", "-c:v", "qtrle", o + ".mov"], stdin=subprocess.PIPE)
        for im, c in zip(leer(v["clip"], v["in"] / FPS, v["n"], v["speed"]), cajas):
            fr = np.zeros((h, w, 4), np.uint8)
            if c:
                reg = im[Y0:Y1, X0:X1]
                bl = cv2.resize(cv2.resize(reg, (max(1, w // 24), max(1, h // 24)), interpolation=cv2.INTER_AREA), (w, h), interpolation=cv2.INTER_LINEAR)
                bl = cv2.GaussianBlur(bl, (0, 0), 18)
                m = np.zeros((h, w), np.float32); cv2.rectangle(m, (c[0] - X0, c[1] - Y0), (c[2] - X0 - 1, c[3] - Y0 - 1), 1.0, -1)
                m = np.clip(cv2.GaussianBlur(m, (0, 0), 14) * 1.6, 0, 1)      # borde suave, centro opaco
                fr[..., :3] = bl; fr[..., 3] = (m * 255).astype(np.uint8)
            p.stdin.write(fr.tobytes())
        p.stdin.close(); p.wait()
        json.dump({"x": X0, "y": Y0, "w": w, "h": h, "visibles": len(vis), "n": v["n"], "persona": True}, open(o + ".json", "w"))
        hechos[v["o"]] = 1
        print(f"plano o={v['o']} ({v['o'] / FPS:.2f} s del montaje; {v['clip']} {v['in'] / FPS:.2f} s): persona difuminada en {len(vis)}/{v['n']} fotogramas; parche {w}x{h} en ({X0},{Y0})")
    if not hechos: print("ningún plano del montaje enseña los tramos de TAPAR_PERSONAS")


def hoja():
    filas = []
    for v, claves in planos():
        pj = f"{D}/p{v['o']}.json"
        if not os.path.exists(pj): continue
        P = json.load(open(pj)); pf = leerp(f"{D}/p{v['o']}.mov", P)
        for k, (im, fr) in enumerate(zip(leer(v["clip"], v["in"] / FPS, v["n"], v["speed"]), pf)):
            if k % 3: continue
            AL, AN = im.shape[:2]
            d = im.copy(); al = fr[..., 3:4].astype(np.float32) / 255; reg = d[P["y"]:P["y"] + P["h"], P["x"]:P["x"] + P["w"]]
            reg[:] = (reg * (1 - al) + fr[..., :3] * al).astype(np.uint8)
            X0, Y0 = max(0, P["x"] - 200), max(0, P["y"] - 150); rec = d[Y0:min(AL, P["y"] + P["h"] + 150), X0:min(AN, P["x"] + P["w"] + 200)]
            rec = cv2.resize(rec, (480, int(rec.shape[0] * 480 / rec.shape[1])))
            cv2.putText(rec, f"o={v['o'] + k} ({(v['o'] + k) / FPS:.1f}s) bruto {(v['in'] + k * v['speed']) / FPS:.2f}", (4, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            filas.append(rec)
    n = 0
    for i in range(0, len(filas), 24):
        g = filas[i:i + 24]; h = max(x.shape[0] for x in g); g = [cv2.copyMakeBorder(x, 0, h - x.shape[0], 0, 0, cv2.BORDER_CONSTANT) for x in g]
        while len(g) % 4: g.append(np.zeros_like(g[0]))
        cv2.imwrite(f"{D}/persona_{n}.jpg", np.vstack([np.hstack(g[j:j + 4]) for j in range(0, len(g), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); n += 1
    print(n, f"hojas en {D}/persona_N.jpg: mira que en TODAS la persona no se reconoce y no se tapa nada más")


if __name__ == "__main__":
    if not PERSONAS: raise SystemExit("plan.py no define TAPAR_PERSONAS: nada que difuminar.")
    hoja() if sys.argv[1:] == ["hoja"] else parches()
