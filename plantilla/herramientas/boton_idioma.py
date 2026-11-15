"""boton_idioma.py: hace la versión en OTRO IDIOMA del botón 2 de la skill (barra de YouTube con me gusta, «SUSCRÍBETE» ->
«SUSCRITO» y campana), que viene con el texto en español. La animación es la misma: solo cambian las dos palabras.

  boton_idioma.py en SUBSCRIBE SUBSCRIBED [--prueba HOJA.jpg]
  boton_idioma.py fr "S'ABONNER" "ABONNÉ"

Deja estudio/public/botones/b02_<idioma>.webm y .json. paso3_plan.py lo coge solo cuando proyecto.py dice IDIOMA = "<idioma>"
(BOTONES = [(ancla, 2)]); el sonido es el mismo b02.mp3.

Cómo lo hace, fotograma a fotograma: borra el texto original (rojo o gris oscuro) de la zona central de la barra y lo rellena
con lo de alrededor; mide del original la opacidad, el tamaño y el sitio del texto (entra subiendo, hace un «pop» al pulsar,
se va con la barra) y escribe la palabra nueva igual; y vuelve a pintar encima la mano del cursor, que pasa por delante.
MIRA la hoja de --prueba: letras que no caben entre el pulgar y la campana, restos del texto viejo, mano cortada.
Solo vale para el botón 2 (las medidas de abajo son suyas)."""
import argparse, json, os, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("idioma"); ap.add_argument("pide"); ap.add_argument("hecho")
ap.add_argument("--botones", default=os.path.join(os.path.dirname(AQUI), "estudio", "public", "botones"))
ap.add_argument("--fuente", help="la .ttf de las letras; de serie, Century Gothic Bold (la del original)")
ap.add_argument("--prueba"); ap.add_argument("--mide", action="store_true", help="solo imprime lo medido en cada fotograma")
a = ap.parse_args()
fuente = a.fuente or next((f for f in ("C:/Windows/Fonts/GOTHICB.TTF", "/Library/Fonts/Century Gothic Bold.ttf", "/System/Library/Fonts/Supplemental/Century Gothic Bold.ttf",
                                       "/Library/Fonts/Microsoft/Century Gothic Bold.ttf") if os.path.exists(f)), None)
if not fuente: raise SystemExit("No encuentro Century Gothic Bold: pasa --fuente con una .ttf geométrica en negrita (Montserrat ExtraBold, League Spartan)")
j = json.load(open(f"{a.botones}/b02.json")); W, H, N = j["w"], j["h"], j["frames"]
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-c:v", "libvpx-vp9", "-i", f"{a.botones}/b02.webm", "-pix_fmt", "bgra", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 4); N = len(fr)

# Medidas del botón 2 (lienzo recortado de 1912x504)
X0, X1, Y0, Y1 = 764, 1562, 85, 322      # zona del texto, entre el pulgar y la campana
BORDE = 1858                             # borde derecho de la barra desplegada: cuando se recoge, el texto se va con él
TOPE = 432                               # borde derecho del cuadrado rojo: el texto se esconde debajo
ROJO, GRIS = (10, 24, 247), (52, 52, 52)      # BGR de «SUSCRÍBETE» y de «SUSCRITO»
CX, CY, ALTO, ANCHO = 1172, 183.5, 97, 740    # centro del texto, alto de las mayúsculas y ancho que cabe
REF = 147                                # fotograma con la mano quieta, entera y sobre texto rojo (de ahí se saca su dibujo)


def partes(f):
    b, g, r, al = (f[..., k].astype(np.int16) for k in range(4)); v = np.maximum(np.maximum(r, g), b); n = np.minimum(np.minimum(r, g), b)
    return b, g, r, al, v, n


def caja(m):
    ys, xs = np.where(m)
    return None if len(xs) < 40 else (int(xs.min()), int(xs.max()) + 1, int(ys.min()), int(ys.max()) + 1)


def mano_caja(f):      # la mano es lo único negro puro del botón (a la derecha del cuadrado rojo)
    b, g, r, al, v, n = partes(f); m = (al > 128) & (v < 25); m[:, :TOPE + 8] = False
    return caja(m)


# El dibujo de la mano: contorno negro (lo oscuro) y relleno blanco (lo que encierra), con su borde suave
f = fr[REF]; mx0, mx1, my0, my1 = mano_caja(f); PAD = 8
rec = f[my0 - PAD:my1 + PAD, mx0 - PAD:mx1 + PAD]; b, g, r, al, v, n = partes(rec)
dentro = cv2.morphologyEx(((al > 128) & (r < 128)).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
dentro = cv2.morphologyEx(dentro, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))      # el contorno es grueso: lo fino son filos del texto
nc, lab, st, _ = cv2.connectedComponentsWithStats(dentro, connectivity=8); dentro = (lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.uint8)      # solo la mano: fuera los filos oscuros del texto de ese fotograma
relleno = dentro.copy(); cv2.floodFill(relleno, None, (0, 0), 2); silueta = (relleno != 2)      # contorno + lo que encierra
cob = np.clip(1 - r / 250.0, 0, 1) * (al > 128)                                                  # cuánto contorno negro hay en cada píxel
abajo = np.zeros(silueta.shape, bool); abajo[324 - (my0 - PAD):] = True                             # por debajo de la barra, la mano está sobre transparente
cerca = cv2.dilate(silueta.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0      # el borde suave del contorno, y nada más (lo de alrededor es el texto de ese fotograma)
alfa = np.where(abajo, al / 255.0, np.where(silueta, 1.0, cob * cerca)); gris = np.where(abajo, v, 255 * (1 - cob))
MANO = np.dstack([gris * alfa, alfa]).astype(np.float32)      # gris premultiplicado + alfa
MW = mx1 - mx0
BLANCO = np.median(fr[100][30:80, 900:1500, :3].reshape(-1, 3), 0).astype(np.float32)      # el blanco de la barra


def pinta_mano(img, f):      # img: BGR float de la barra ya retocada; f: el fotograma original (para saber dónde está la mano)
    c = mano_caja(f)
    if not c or c[1] < X0 or c[0] > X1: return False      # no hay mano o no pasa por el texto: no se toca
    s = (c[1] - c[0]) / MW; m = cv2.resize(MANO, None, fx=s, fy=s, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LINEAR)
    x = int(round((c[0] + c[1]) / 2 - m.shape[1] / 2)); y = int(round(c[2] - PAD * s))
    h = min(m.shape[0], min(324, img.shape[0]) - y); w = min(m.shape[1], img.shape[1] - x)      # solo hasta el borde de abajo de la barra: lo de fuera ya está bien
    al = m[:h, :w, 1:2]; img[y:y + h, x:x + w] = img[y:y + h, x:x + w] * (1 - al) + m[:h, :w, 0:1]
    return True


def letras(txt, color, alto):      # la palabra en un lienzo propio con transparencia, a 4x para que el borde salga fino
    k = 4; f = ImageFont.truetype(fuente, 400); t0 = f.getbbox("H"); f = ImageFont.truetype(fuente, int(round(400 * alto * k / (t0[3] - t0[1]))))
    x0, y0, x1, y1 = f.getbbox(txt); hx0, hy0, hx1, hy1 = f.getbbox("H")
    im = Image.new("L", (x1 - x0 + 8 * k, hy1 - hy0 + 8 * k + (hy0 - y0)), 0); ImageDraw.Draw(im).text((4 * k - x0, 4 * k - y0), txt, 255, font=f)
    m = cv2.resize(np.array(im), None, fx=1 / k, fy=1 / k, interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    return m, (hy0 - y0) / k + 4 + alto / 2      # máscara y fila del centro de las mayúsculas dentro de ella (los acentos sobresalen por arriba)


alto = ALTO
while max(letras(t, ROJO, alto)[0].shape[1] - 8 for t in (a.pide, a.hecho)) > ANCHO: alto -= 1      # las dos palabras al mismo tamaño y que quepan
PAL = {"rojo": (*letras(a.pide, ROJO, alto), ROJO), "gris": (*letras(a.hecho, GRIS, alto), GRIS)}
print(f"Letras a {alto} px de alto (original {ALTO}); «{a.pide}» {PAL['rojo'][0].shape[1] - 8} px, «{a.hecho}» {PAL['gris'][0].shape[1] - 8} px; caben {ANCHO}")


def mide(f, i):
    """Qué texto hay y cómo: (palabra, opacidad, escala, bajada en px, desplazamiento con la barra) y la máscara de lo que hay que borrar."""
    b, g, r, al, v, n = partes(f); fila = np.where(al[170] > 128)[0]; des = min(0, (int(fila.max()) if len(fila) else BORDE) - BORDE)
    z = np.zeros(al.shape, bool); z[Y0:Y1, max(TOPE, X0 + des):X1 + des] = True; z &= al > 128
    roj = z & (r - g > 14) & (r > 150); osc = z & (v - n < 26) & (v < 215)
    fondo = (v - n < 26) & (v > 215); azul = b - r > 30      # lo que NO es texto: el blanco de la barra, el círculo gris del clic y el icono azul
    borrar = cv2.dilate((z & ~fondo & ~azul).astype(np.uint8), np.ones((13, 13), np.uint8)) & z.astype(np.uint8)
    if i < 110: borrar = (z | (cv2.dilate(z.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0) & (al > 0) & (np.arange(al.shape[1])[None, :] > X0) & (np.arange(al.shape[1])[None, :] < X1)).astype(np.uint8)      # mientras entra (medio transparente) se limpia la zona entera: ahí no hay nada más
    cr = caja(z & (r - g > 60)); arriba = np.zeros(al.shape, bool); arriba[:193] = True      # el gris se mide por encima de la mano
    cg = caja(osc & arriba & (v < 140))
    if cr and (not cg or (cr[1] - cr[0]) * (cr[3] - cr[2]) > 3000 and i < 156):
        op = float(np.clip(np.percentile((r - g)[roj], 97) / 223.0, 0, 1))
        if i < 110: return ("rojo", op, 1.0, cr[2] - 103, des), borrar            # entra subiendo desde abajo
        return ("rojo", op, min(1.0, (cr[1] - cr[0]) / 776.0), 0, des), borrar    # «pop» al pulsar
    if cg:
        w = cg[1] - cg[0]; s = 1.0 if des else min(1.0, w / 663.0)                 # recogiéndose, el cuadrado rojo tapa parte: no es un cambio de tamaño
        op = float(np.clip((255 - np.percentile(v[osc & arriba], 3)) / 203.0, 0, 1))
        return ("gris", op, s, 0, des), borrar
    return None, borrar


def hace(i):
    f = fr[i]; m, borrar = mide(f, i)
    if not borrar.any(): return f, m
    if i < 110: bgr = f[..., :3].astype(np.float32); bgr[borrar > 0] = BLANCO
    else: bgr = cv2.inpaint(np.ascontiguousarray(f[..., :3]), borrar, 4, cv2.INPAINT_TELEA).astype(np.float32)
    if m:
        pal, op, s, baja, des = m; msk, fc, color = PAL[pal]
        if s != 1: msk = cv2.resize(msk, None, fx=s, fy=s, interpolation=cv2.INTER_AREA); fc *= s
        x = int(round(CX + des - msk.shape[1] / 2)); y = int(round(CY + baja - fc))
        x0 = max(x, TOPE); y1 = min(y + msk.shape[0], 323); mm = msk[:y1 - y, x0 - x:] * op      # se esconde bajo el cuadrado rojo y no se sale de la barra por abajo
        if mm.size: bgr[y:y1, x0:x0 + mm.shape[1]] = bgr[y:y1, x0:x0 + mm.shape[1]] * (1 - mm[..., None]) + np.array(color, np.float32) * mm[..., None]
    pinta_mano(bgr, f)
    return np.dstack([np.clip(bgr, 0, 255).astype(np.uint8), f[..., 3]]), m


if a.mide:
    for i in range(N):
        m, bo = mide(fr[i], i)
        if m or bo.any(): print(i, m and (m[0], round(m[1], 2), round(m[2], 3), m[3], m[4]), int(bo.sum()), mano_caja(fr[i]))
    raise SystemExit
sal = f"{a.botones}/b02_{a.idioma}"
p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", f"{j['fps']:.5f}", "-i", "-",
                      "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "22", "-row-mt", "1", "-auto-alt-ref", "0", "-an", sal + ".webm"], stdin=subprocess.PIPE)
hoja = []; ver = (78, 82, 86, 90, 100, 132, 138, 144, 150, 153, 155, 156, 158, 160, 165, 170, 174, 200, 240, 256, 259, 262)
for i in range(N):
    o, m = hace(i); p.stdin.write(o.tobytes())
    if a.prueba and i in ver:
        def sobre(q): al = q[:340, 420:, 3:4] / 255.0; return (q[:340, 420:, :3] * al + np.array((138, 90, 58)) * (1 - al)).astype(np.uint8)
        c = np.vstack([sobre(fr[i]), sobre(o)]); cv2.putText(c, str(i), (1300, 60), 0, 1.6, (255, 255, 255), 4); hoja.append(cv2.resize(c, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA))
p.stdin.close(); p.wait()
json.dump({**j, "idioma": a.idioma, "texto": [a.pide, a.hecho]}, open(sal + ".json", "w"), ensure_ascii=False)
print(sal + ".webm", f"({N} fotogramas)")
if a.prueba:
    while len(hoja) % 2: hoja.append(np.zeros_like(hoja[0]))
    cv2.imwrite(a.prueba, np.vstack([np.hstack(hoja[k:k + 2]) for k in range(0, len(hoja), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
