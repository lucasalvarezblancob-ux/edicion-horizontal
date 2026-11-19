"""palabrotas.py: palabrotas que suenan en el montaje (texto del EDL alineado, trabajo/linea.json) y si ya están en PITIDOS.
Desde out/<slug>/, después de paso1_alinear.py. Imprime las que faltan como líneas listas para pegar en PITIDOS de plan.py
(paso5_audio.py pone encima de cada una un pitido de 1 kHz).
Ojo: solo ve lo que está en el texto del EDL; lo que dice quien graba ENTRE frases está en trabajo/voz.json (voces.py):
léelo también buscando estas palabras.
Por qué: Reino Selva, 2026-11-19 (vaciamos-estanque): «digo "jodido" poner un pitido o algo en cada ocasión» y, en la
corrección siguiente, «pita también los hostia y cojones y demás palabrotas». Se pitó solo la palabra que dijo."""
import re
from comun import FPS, Linea, buscar, norm
import plan      # después de comun: es quien mete la carpeta del vídeo en el path

# raíces (sin tildes) y palabras enteras: norm() pasa «coño» a «cono», que como raíz cazaría «conoce»
MAL = re.compile(r"^(hostia|ostia|cojon|joder|jodid|jodo|jode|mierda|puta|puto|cabron|gilipoll|capull|imbecil|polla|carajo|cago)|^(cono|conos|leches)$")
W = Linea().palabras
hechos = set()
for a in getattr(plan, "PITIDOS", []):
    try: i, j = buscar(W, *a); hechos.update(range(i, j + 1))
    except (Exception, SystemExit): pass
vistas, faltan = {}, 0
for k, w in enumerate(W):
    p = norm(w["w"])
    if not p: continue
    n = vistas.get((w["clip"], p), 0); vistas[(w["clip"], p)] = n + 1      # n-ésima vez que suena ESA palabra de ESE clip
    if not MAL.match(p): continue
    t = w["o0"] / FPS; ya = k in hechos; faltan += not ya
    print(f"{int(t // 60)}:{t % 60:05.2f}  {'ya   ' if ya else 'FALTA'}  ({w['clip']!r}, {w['w']!r}, {n}),")
print(faltan, "palabrotas sin pitido (mira también trabajo/voz.json: lo que dice quien graba entre frases)")
