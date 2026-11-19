"""hoja_textos.py: hoja de contactos de TODOS los textos y gráficos del montaje, cada uno sobre el plano que tiene debajo
(con su escala y encuadre), con la caja que ocupa dibujada encima (comun.caja_texto) -> trabajo/textos_N.jpg.
Dos fotogramas por texto: al entrar y al irse (por debajo puede haber un corte de escala o un recurso distinto).

OBLIGATORIO mirarlas antes de renderizar (después de paso3_plan.py): un texto no tapa lo que se está enseñando en ese
momento (el animal comiendo, la cara, la mano que hace algo). Si tapa:
  - el rótulo va a otro sitio: "lado" (izq/der) o "y" (más arriba) en su R(...)/gráfico;
  - si lo que se enseña se mueve (come, camina) y hay que nombrarlo: rótulo con FLECHA que lo sigue (TRK), no un texto fijo;
  - o el recurso de debajo se cambia (o su zoom: BROLL con (None, cx, cy) para que el corte de escala vaya al sujeto).
Por qué: Lucas, 2026-11-17 (alimentacion): «"agua de ósmosis": el texto tapa a la tortuga, que es el foco del clip… tiene
que tener en cuenta que el texto no tape lo importante en el momento que aparece» y «"¡cazado! un caracol vivo" tapa
cómo come el caracol: ahí una flecha con el texto trackeando». Causa: había 46 rótulos y solo se miraron con ver.py las
burbujas y los botones; cada fotograma de ver.py tarda en salir (Remotion) y nadie veía todos los textos juntos.
Esta hoja sale en segundos (sin Remotion: la caja es una estimación del sitio que ocupa; el aspecto final se ve con ver.py).
Uso (desde out/<slug>/):  hoja_textos.py [tipo ...]   (sin tipos: todos menos el título)"""
import json, subprocess, sys
import numpy as np, cv2
from comun import ALTO, ANCHO, CAPAS_JSON, FPS, TRABAJO, caja_texto, fuente, video
from dinamica import CARA_Y, RECORTE_169, encuadre

tipos = set(sys.argv[1:]); vid = video(); w = 640; h = 2 * round(w * ALTO / ANCHO / 2)
items = [it for it in json.load(open(CAPAS_JSON, encoding="utf-8"))["items"] if (it["t"] in tipos if tipos else it["t"] != "titulo") and caja_texto(it)]


def fotograma(F_):
    v = next((v for v in vid if v["o"] <= F_ < v["o"] + v["n"]), vid[-1]); k = F_ - v["o"]
    if v.get("t"): z = v["z1"] + (v["z0"] - v["z1"]) * max(0, 1 - k / v["t"]) ** 3
    else: z = v["z0"] + (v["z1"] - v["z0"]) * k / max(v["n"], 1)
    W2, H2, x, y = encuadre(z, v.get("cx"), v.get("cy"), v.get("ax", 0.5), v.get("ay", CARA_Y if not v["b"] else 0.5))
    ent, pre = fuente(v["clip"], (v["in"] + k * v["speed"]) / FPS)
    bn = "hue=s=0," if v.get("bn") else ""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", *ent, "-frames:v", "1", "-vf", f"{pre}{bn}{RECORTE_169}scale={W2}:{H2},crop={ANCHO}:{ALTO}:{x}:{y},scale={w}:{h}", "-pix_fmt", "bgr24", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).copy() if len(raw) == w * h * 3 else np.zeros((h, w, 3), np.uint8), v


filas = []
for it in items:
    fila = []
    for F_ in (it["f0"] + 3, max(it["f0"] + 3, it["f1"] - 3)):
        im, v = fotograma(F_); capa = im.copy()
        for x0, y0, x1, y1 in caja_texto(it):
            cv2.rectangle(capa, (int(x0 * w), int(y0 * h)), (int(x1 * w), int(y1 * h)), (40, 220, 255), -1)
            cv2.rectangle(im, (int(x0 * w), int(y0 * h)), (int(x1 * w), int(y1 * h)), (40, 220, 255), 2)
        im = cv2.addWeighted(capa, 0.35, im, 0.65, 0)
        if it["t"] == "trk" and it.get("pos"):
            px, py = it["pos"][min(F_ - it["f0"], len(it["pos"]) - 1)]; cv2.circle(im, (int(px / ANCHO * w), int(py / ALTO * h)), 7, (0, 0, 255), -1)
        fila.append(im)
    im = np.hstack(fila); s = it["f0"] / FPS
    txt = " ".join(str(it.get(k, "")) for k in ("txt", "grande", "titulo", "sub") if it.get(k) and isinstance(it.get(k), str))[:60]
    lab = f"{int(s // 60)}:{s % 60:04.1f} {it['t']} {it['f1'] / FPS - s:.1f}s  {txt}"
    cv2.rectangle(im, (0, 0), (2 * w, 30), (0, 0, 0), -1); cv2.putText(im, lab, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (80, 240, 240), 2)
    filas.append(im)
for k in range(0, len(filas), 8): cv2.imwrite(f"{TRABAJO}/textos_{k // 8 + 1}.jpg", np.vstack(filas[k:k + 8]), [cv2.IMWRITE_JPEG_QUALITY, 78])
print(len(filas), "textos ->", ", ".join(f"{TRABAJO}/textos_{k // 8 + 1}.jpg" for k in range(0, len(filas), 8)))
