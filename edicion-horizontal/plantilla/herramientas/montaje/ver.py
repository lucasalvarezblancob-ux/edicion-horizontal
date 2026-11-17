"""ver.py F [F ...]: compone el fotograma F del montaje (bruto + escala y encuadre) con su capa gráfica, a media resolución,
en trabajo/still/v<F>.jpg. Para comprobar ANTES de renderizar: cada texto (en el frame anterior a su palabra no debe estar;
en el de la palabra, sí), cada cifra junto a la cara, cada zoom (¿apunta a la cara o al sujeto, o a una pared?).
F = frame de salida; con mm:ss.d también vale (ver.py 4:18.2)."""
import json, os, shutil, subprocess, sys
from comun import ALTO, ANCHO, COMP, ESTUDIO, FPS, TRABAJO, fuente, video
from dinamica import CARA_Y, encuadre

os.makedirs(f"{TRABAJO}/still", exist_ok=True); NPX = shutil.which("npx") or "npx"; GL = ["--gl=angle"] if os.name == "nt" else []
vid = video(); rangos = json.load(open(f"{TRABAJO}/video.json"))["rangos"]
for arg in sys.argv[1:]:
    F_ = round((int(arg.split(":")[0]) * 60 + float(arg.split(":")[1])) * FPS) if ":" in arg else int(arg)
    v = next(v for v in vid if v["o"] <= F_ < v["o"] + v["n"]); k = F_ - v["o"]
    if v.get("t"): z = v["z1"] + (v["z0"] - v["z1"]) * max(0, 1 - k / v["t"]) ** 3
    else: z = v["z0"] + (v["z1"] - v["z0"]) * k / max(v["n"], 1)
    t = (v["in"] + k * v["speed"]) / FPS; w, h, x, y = encuadre(z, v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", CARA_Y))
    png = os.path.abspath(f"{TRABAJO}/still/s{F_}.png"); sal = f"{TRABAJO}/still/v{F_}.jpg"
    ent, pre = fuente(v["clip"], t); base = ["ffmpeg", "-nostdin", "-v", "error", "-y", *ent]
    if v.get("bn"): pre += "hue=s=0,"          # el fail (FALLOS) va en blanco y negro, como en el render
    capa = any(a <= F_ < b for a, b in rangos)
    if capa:
        if os.path.exists(png): os.remove(png)
        # con tope de tiempo: un Remotion colgado no puede bloquear la sesión (el parón de 2 h 40 min de alimentacion)
        try: r = subprocess.run([NPX, "remotion", "still", COMP, png, f"--frame={F_}", *GL, "--scale=0.5", "--timeout=60000"], cwd=ESTUDIO, capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=240)
        except subprocess.TimeoutExpired: r = None; print("AVISO: Remotion lleva 4 min sin sacar el fotograma: colgado (¿una fuente que no carga? quita los gráficos del creador para acotarlo)")
        if not os.path.exists(png): print("AVISO: Remotion no ha sacado la capa; va sin gráficos.", ((r.stderr or r.stdout)[-300:] if r else "")); capa = False
    if capa:
        fc = f"[0:v]{pre}scale={w}:{h},crop={ANCHO}:{ALTO}:{x}:{y},scale={ANCHO // 2}:{ALTO // 2}[b];[b][1:v]overlay"
        subprocess.run([*base, "-i", png, "-filter_complex", fc, "-frames:v", "1", "-q:v", "3", sal], check=True)
    else:
        subprocess.run([*base, "-vf", f"{pre}scale={w}:{h},crop={ANCHO}:{ALTO}:{x}:{y},scale={ANCHO // 2}:{ALTO // 2}", "-frames:v", "1", "-q:v", "3", sal], check=True)
    print(F_, v["clip"], f"{t:.2f} s del bruto", "x", round(z, 3), "recurso" if v["b"] else "", "->", sal)
