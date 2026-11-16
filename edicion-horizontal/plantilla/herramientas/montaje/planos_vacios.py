"""planos_vacios.py: PAREDES en el plano principal. Se lanza desde out/<slug>/ después de paso3_plan.py (antes de renderizar).
Busca los planos que NO son recurso, en los que no hay cara, y que el registro visual describe como pared, techo,
barrido, giro, cámara pegada al cuerpo, de espaldas sin sujeto o caminando sin nada que enseñar: mientras suena la voz,
el espectador ve una pared porque quien graba está cambiando de sitio o de foco. Lección de Lucas en prueba-3 v2
(2026-11-15): siete de diez correcciones eran esto («no puede ser que se vea una pared así; al menos un plano que tenga
que ver con lo que habla, de los mismos brutos o de recursos»).

Para cada uno imprime el minuto, el bruto, lo que dice el registro y LO QUE SE DICE encima, y hace la hoja
trabajo/vacios.jpg (inicio, medio y final de cada plano). Mírala y decide cada uno (base/preferencias.md -> «Paredes»):
  - no se dice nada que importe (reencuadres, «ahora sí», «no sé si va») -> FUERA del EDL (se acorta la pieza);
  - se dice algo -> BROLL de AQUELLO de lo que habla (el animal, la planta, el pez, lo que señala), de los mismos brutos
    (registro visual: mejores_recursos) o del archivo del creador; si no hay nada de eso, un plano bonito del sitio;
  - es un desplazamiento con sentido (va al cuadro eléctrico) -> se queda, pero sin zoom y corto.
Lo que se deje a propósito se apunta en plan.py: VACIOS_OK = {"m:ss": "por qué"} (por minuto de salida, redondeado)."""
import glob, json, os, re, subprocess, sys
import numpy as np, cv2
from comun import ANALISIS, ALTO, ANCHO, FPS, TRABAJO, Linea, fuente, video
from dinamica import Caras

sys.path.insert(0, os.getcwd()); import plan
# qué cuenta como «pared»: tramos de transición o barrido; «lugar» cuyo sujeto es una pared o el techo; y los «evitar» del
# registro por pared, barrido, giro, cámara movida o pegada al cuerpo. NO cuentan los tramos en que hace algo (accion,
# manos, a_camara): ahí hay sujeto aunque no se le vea la cara.
PARED = re.compile(r"pared|techo|suelo", re.I)
MALO = re.compile(r"pared|barrido|giro|movid|borros|pegada al|torso|hombro|piernas|sin sujeto|caminata|desenfoc|se aparta", re.I)
PEGADA = re.compile(r"pegada|contra su (torso|cuerpo|pecho)|barrido|tapa(da)? la (cámara|lente)", re.I)
def es_malo(x):
    tipo, que, suj = x[2], x[3], x[4]
    if tipo in ("transicion", "barrido") or PEGADA.search(que): return True   # también un «accion» que acaba con la cámara contra el torso
    if tipo == "lugar": return bool(PARED.search(suj or que[:40]))
    if tipo == "evitar": return bool(MALO.search(que))
    return False
OK = getattr(plan, "VACIOS_OK", {})
reg = {}
for p in glob.glob(f"{ANALISIS}/visual/*.json"):
    d = json.load(open(p, encoding="utf-8")); r = reg.setdefault(d["clip"], [])
    r += [(t["t0"], t["t1"], t.get("tipo", ""), t.get("que", ""), t.get("sujeto", "")) for t in d.get("tramos", [])]
    r += [(t["t0"], t["t1"], "evitar", t.get("por_que", ""), "") for t in d.get("evitar", [])]
caras, W = Caras(TRABAJO), Linea().palabras
mm = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"
hall, ims = [], []
for v in video():
    if v["b"] or v["n"] < round(0.5 * FPS): continue
    c = v["clip"]; t0 = v["in"] / FPS; t1 = t0 + v["n"] * v["speed"] / FPS
    if c not in reg: continue
    tapa = [x for x in reg[c] if min(t1, x[1]) - max(t0, x[0]) > 0]
    malos = [x for x in tapa if min(t1, x[1]) - max(t0, x[0]) >= 0.4 * (t1 - t0) and es_malo(x)]
    # con la cámara pegada al cuerpo o en una transición, el detector ve media cara en el borde: no vale como «hay cara»
    if caras.en(c, v["in"], v["n"]) and not any(x[2] in ("transicion", "barrido") or PEGADA.search(x[3]) for x in malos): continue
    # sin nada del registro encima (el agente no describió ese trozo): no se sabe qué se ve -> a la hoja también
    # (prueba-3 v3, 12:55: pared mientras se mete al agua y el registro no tenía ese tramo)
    if not malos and sum(min(t1, x[1]) - max(t0, x[0]) for x in tapa) < 0.3 * (t1 - t0) and v["n"] >= FPS:
        malos = [(t0, t1, "sin registro", "el registro visual no describe este trozo: mírala", "")]
    if not malos: continue
    s = v["o"] / FPS; clave = f"{int(s // 60)}:{int(s % 60):02d}"
    if clave in OK: continue
    dicho = " ".join(w["w"] for w in W if v["o"] <= w["o0"] < v["o"] + v["n"])
    hall.append((s, c, t0, t1, malos, dicho))
    for t in (t0 + 0.1, (t0 + t1) / 2, t1 - 0.1):
        ent, pre = fuente(c, t); w, h = 384, 2 * round(384 * ALTO / ANCHO / 2)
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
        im = np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy() if len(raw) >= w * h * 3 else np.zeros((h, w, 3), np.uint8)
        cv2.rectangle(im, (0, 0), (250, 26), (0, 0, 0), -1); cv2.putText(im, f"{mm(s)} {c[-4:]} {t:.1f}s", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (80, 240, 240), 2); ims.append(im)
for s, c, t0, t1, malos, dicho in hall:
    print(f"{mm(s)}  {c} {t0:.1f}-{t1:.1f} ({t1 - t0:.1f} s)  registro: {malos[0][2]}: {malos[0][3][:90]}")
    print(f"        se dice: «{dicho[:140]}»")
if ims:
    while len(ims) % 6: ims.append(np.zeros_like(ims[0]))
    cv2.imwrite(f"{TRABAJO}/vacios.jpg", np.vstack([np.hstack(ims[k:k + 6]) for k in range(0, len(ims), 6)]), [cv2.IMWRITE_JPEG_QUALITY, 75])
print(len(hall), "planos sin cara sobre pared/movimiento ->", f"{TRABAJO}/vacios.jpg" if ims else "nada")
