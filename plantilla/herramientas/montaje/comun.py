"""Común del montaje horizontal. Todo se ejecuta DESDE la carpeta del vídeo (out/<slug>/), que tiene proyecto.py,
edl.py y plan.py; los pasos viven en herramientas/montaje/ y son iguales para todos los vídeos:

    cd out/<slug> && ../../herramientas/.venv/Scripts/python ../../herramientas/montaje/paso1_alinear.py   (macOS: .venv/bin/python)

proyecto.py (lo crea nuevo_video.py) dice dónde están los brutos, el lienzo y el idioma. Aquí se lee una sola vez."""
import glob, json, os, re, sys, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
for p in (AQUI, os.getcwd()):
    if p not in sys.path: sys.path.insert(0, p)
try:
    import proyecto as _p
except ModuleNotFoundError:
    raise SystemExit("Ejecuta desde la carpeta del vídeo (out/<slug>/): aquí no hay proyecto.py. Créala con herramientas/montaje/nuevo_video.py")

_g = lambda n, d=None: getattr(_p, n, d)
SLUG = _p.SLUG
COMP = _g("COMP") or (lambda c: ("V" + c) if c[0].isdigit() else c)("".join(x.capitalize() for x in re.split(r"[^a-zA-Z0-9]+", SLUG) if x) + "Capas")   # id de la composición Remotion (nunca empieza por cifra)
BRUTOS = [_p.BRUTOS] if isinstance(_p.BRUTOS, str) else list(_p.BRUTOS)       # carpeta(s) con los brutos
ANALISIS = _g("ANALISIS", f"../../bruto/{SLUG}-analisis")                    # transcripciones, hojas y registro visual
TRANSCRIPCIONES = _g("TRANSCRIPCIONES", f"{ANALISIS}/transcripcion")         # <clip>.json, <clip>.txt, <clip>.w.json
FPS = _g("FPS", 25)
ANCHO, ALTO = _g("ANCHO", 3840), _g("ALTO", 2160)                            # lienzo = el del mejor bruto (nunca menos)
IDIOMA = _g("IDIOMA")                                                        # idioma HABLADO (lo detecta paso0); nunca supuesto
NUMEROS = _g("NUMEROS", {})                                                  # cifras -> como se dicen, para alinear: {"100": "onehundred"}
ESTUDIO = os.path.abspath(_g("ESTUDIO", "../../estudio"))
TRABAJO = "trabajo"
CAPAS_JSON = f"{ESTUDIO}/src/videos/{SLUG}/capas.json"
PY = sys.executable
F = lambda s: int(round(s * FPS))                                            # segundos -> frames
os.makedirs(TRABAJO, exist_ok=True)

# Personalización del CREADOR: personal/<creador>/ de la carpeta de edición (local, nunca en la skill).
# Orden: estándar de la skill < personal/<creador>/ajustes.py < plan.py del vídeo.
# El creador de un vídeo es CREADOR en su proyecto.py; si en personal/ solo hay uno, es ese.
RAIZ = os.path.dirname(os.path.dirname(AQUI)).replace("\\", "/")
_cre = sorted(d for d in (os.listdir(f"{RAIZ}/personal") if os.path.isdir(f"{RAIZ}/personal") else []) if os.path.isdir(f"{RAIZ}/personal/{d}") and not d.startswith(("_", ".")))
CREADOR = _g("CREADOR") or (_cre[0] if len(_cre) == 1 else None)
if CREADOR is None and len(_cre) > 1: raise SystemExit(f"Hay varios creadores en personal/ ({', '.join(_cre)}): pon CREADOR = '...' en proyecto.py")
if CREADOR and CREADOR not in _cre: raise SystemExit(f"No existe personal/{CREADOR}/ (créalo con herramientas/montaje/nuevo_creador.py {CREADOR})")
PERSONAL = f"{RAIZ}/personal/{CREADOR}" if CREADOR else None
# TODO el material del creador está en su carpeta, ordenado por subcarpetas: marca/ (intro, outro, logos), temas (clips de
# archivo y b-roll), fotos/, mapas/, musica/, sonidos/.
RECURSOS = f"{PERSONAL}/recursos" if PERSONAL else None
MUSICA = _g("MUSICA") or (f"{RECURSOS}/musica" if RECURSOS else None)
_aj = {}
_pa = f"{PERSONAL}/ajustes.py" if PERSONAL else ""
if _pa and os.path.exists(_pa): exec(compile(open(_pa, encoding="utf-8").read(), _pa, "exec"), _aj)


def ajuste(nombre, defecto):
    """Valor que el creador ha puesto en personal/<creador>/ajustes.py o, si no lo define, el estándar."""
    return _aj.get(nombre, defecto)


def marca():
    """personal/<creador>/marca.json (color de acento, canal, @, código, logo): paso3 la mete en capas.json para Remotion.
    Si el creador tiene una marca distinta por idioma (un canal en español y otro en inglés), marca.json lleva
    "idiomas": {"en": {"canal": "...", "handle": "...", "logo": "..."}}: los campos del IDIOMA del vídeo tapan a los generales."""
    f = f"{PERSONAL}/marca.json" if PERSONAL else ""
    m = json.load(open(f, encoding="utf-8")) if f and os.path.exists(f) else {}
    return {**{k: v for k, v in m.items() if k != "idiomas"}, **m.get("idiomas", {}).get(IDIOMA or "", {})}


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(s):
    """Palabra normalizada para comparar texto con transcripción: minúsculas, sin tildes ni signos."""
    return re.sub(r"[^a-z0-9%']", "", sin_tildes(s.lower()))


_brutos = {}
def bruto(clip):
    """Ruta del bruto de un clip (nombre sin extensión), buscándolo en BRUTOS."""
    if clip not in _brutos:
        # además de los brutos, valen como piezas los clips del creador, estén en la carpeta que estén de
        # personal/<creador>/recursos/ (marca/intro.mp4, <tema>/<clip de archivo>…). Si el nombre se repite, manda el bruto.
        dirs = BRUTOS + ([RECURSOS] if RECURSOS else [])
        hits = [f for d in BRUTOS for f in glob.glob(os.path.join(d, clip + ".*"))]
        if RECURSOS: hits += sorted(glob.glob(os.path.join(glob.escape(RECURSOS), "**", glob.escape(clip) + ".*"), recursive=True))
        hits = [f for f in hits if f.lower().endswith((".mp4", ".mov", ".m4v", ".mxf", ".mkv"))]
        if not hits: raise SystemExit(f"No encuentro el bruto {clip} en {dirs}")
        _brutos[clip] = hits[0].replace("\\", "/")
    return _brutos[clip]


def clips():
    """Todos los brutos (nombre sin extensión), en orden."""
    fs = [f for d in BRUTOS for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith((".mp4", ".mov", ".m4v", ".mxf", ".mkv"))]
    return sorted({os.path.splitext(os.path.basename(f))[0] for f in fs})


# Brutos HDR (iPhone HLG, PQ). ffmpeg NO convierte HDR al leer: la imagen sale pálida y lavada. La IMAGEN de un bruto
# se lee siempre con fuente(); el SONIDO, del original con bruto(). sdr.py hace copias SDR solo de los trozos que usa el
# montaje (trabajo/sdr/<clip>/<a>_<b>.mp4, a y b en frames del proyecto contados sobre el bruto).
LIBPLACEBO = "libplacebo=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv:format=yuv420p"   # el motor de mpv; nunca zscale+tonemap
_hdr = None
def es_hdr(clip):
    """¿El bruto es HDR? Se mira una vez por clip y se apunta en trabajo/hdr.json."""
    global _hdr
    if _hdr is None:
        try: _hdr = json.load(open(f"{TRABAJO}/hdr.json", encoding="utf-8"))
        except (FileNotFoundError, ValueError): _hdr = {}
    if clip not in _hdr:
        import subprocess
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=color_transfer", "-of", "default=nw=1:nk=1", bruto(clip)], capture_output=True, text=True).stdout.split()
        _hdr[clip] = bool(r) and r[0].strip(",") in ("arib-std-b67", "smpte2084")
        json.dump(_hdr, open(f"{TRABAJO}/hdr.json", "w", encoding="utf-8"), ensure_ascii=False)
    return _hdr[clip]


_seg = {}
def segmentos(clip, releer=False):
    """Copias SDR que ya hay de un bruto HDR: [(a, b, ruta)], en frames del proyecto sobre el bruto."""
    if releer or clip not in _seg:
        _seg[clip] = sorted((int(os.path.basename(f)[:-4].split("_")[0]), int(os.path.basename(f)[:-4].split("_")[1]), f.replace("\\", "/"))
                            for f in glob.glob(f"{TRABAJO}/sdr/{glob.escape(clip)}/*.mp4"))
    return _seg[clip]


def fuente(clip, t, dur=0.0, exigir=False):
    """De dónde leer la IMAGEN de un bruto entre t y t + dur (s): devuelve (entrada, pre), donde `entrada` son los
    argumentos de ffmpeg («-ss … -i …») y `pre` lo que hay que poner al PRINCIPIO de la cadena de filtros de esa entrada.
    Bruto SDR: el original. Bruto HDR: su copia SDR (sdr.py) si hay una que cubra el trozo; si no, el original convertido
    al vuelo con libplacebo (vale para sacar fotogramas sueltos; para renderizar, exigir=True: sin copia no se sigue)."""
    if not es_hdr(clip): return ["-ss", f"{t:.3f}", "-i", bruto(clip)], ""
    for a, b, f in segmentos(clip):
        if a / FPS <= t + 1e-6 and t + dur <= b / FPS + 1e-6: return ["-ss", f"{max(0, t - a / FPS):.3f}", "-i", f], ""
    if exigir: raise SystemExit(f"{clip} es HDR y no hay copia SDR de {t:.2f}-{t + dur:.2f} s: lanza antes sdr.py")
    return ["-init_hw_device", "vulkan", "-ss", f"{t:.3f}", "-i", bruto(clip)], LIBPLACEBO + ","


_pal = {}
def palabras(clip):
    """Palabras de la transcripción de un bruto: [{p, t, fin, prob}] (las escribe paso0_preparar.py)."""
    if clip not in _pal:
        ruta = f"{TRANSCRIPCIONES}/{clip}.w.json"
        if not os.path.exists(ruta): raise SystemExit(f"Falta {ruta}: lanza antes paso0_preparar.py")
        _pal[clip] = json.load(open(ruta, encoding="utf-8"))
    return _pal[clip]


def buscar(W, clip, frase, n):
    """Índices (primera, última) de una frase literal dentro de las palabras del MONTAJE (linea.json).
    n = 0 primera vez que suena (p. ej. en el tráiler), -1 la última, 1 la segunda…"""
    q = [norm(x) for x in frase.split()]; q = [x for x in q if x]
    idx = [i for i, w in enumerate(W) if w["clip"] == clip and norm(w["w"])]
    hits = [idx[j] for j in range(len(idx) - len(q) + 1) if [norm(W[i]["w"]) for i in idx[j:j + len(q)]] == q]
    if not hits: raise SystemExit(f"frase no encontrada en el montaje: {clip} {frase!r}")
    i = hits[n]; return i, idx[idx.index(i) + len(q) - 1]


def texto_dicho(W, txt, f0, f1):
    """Hasta cuándo tiene que aguantar un texto (Lucas, 2026-11-14: «aparecen en buen timing pero desaparecen antes de que
    la persona acabe de decirlo, por lo que no te da tiempo ni a leerlo»). Devuelve (frame mínimo de salida, última palabra
    del texto que suena en la voz o None):
      - la ÚLTIMA palabra del texto que se dice (casadas en orden, cada una una vez, sin más de 1,5 s entre una y otra), y de
        ahí +0,5 s; si la frase sigue sin pausa, hasta la pausa (como mucho 0,8 s más);
      - y como mínimo el tiempo de leerlo: 0,6 s + 0,3 s por palabra, nunca menos de 1,2 s."""
    pal = [norm(p) for p in re.split(r"[\s|/·:,.!?¡¿*'\"()+«»…-]+", str(txt)) if norm(p)]
    ks = [p for p in pal if len(p) >= 4 or any(c.isdigit() for c in p)] or list(pal)
    def es(n, k): return n == k or (len(n) >= 5 and len(k) >= 5 and (n.startswith(k[:5]) or k.startswith(n[:5])))
    ult, j = None, 0                  # cada palabra del texto se casa UNA vez y en orden (lo que repite después no cuenta)
    for w in W:
        if j >= len(ks): break
        if w["o0"] < f0 - 0.3 * FPS: continue
        if ult is None and w["o0"] > f1 + 0.5 * FPS: break
        if ult is not None and w["o0"] - ult["o1"] > 1.5 * FPS: break
        n = norm(w["w"]); m = next((i for i in range(j, len(ks)) if es(n, ks[i])), None)
        if m is not None: ult, j = w, m + 1
    fin = f0 + max(F(1.2), F(0.6 + 0.3 * len(pal)))
    if ult is not None:
        fin = max(fin, int(round(ult["o1"])) + F(0.5)); k = W.index(ult)
        while k + 1 < len(W) and W[k + 1]["o0"] - W[k]["o1"] < 0.3 * FPS and W[k + 1]["o1"] - ult["o1"] <= 0.8 * FPS: k += 1
        fin = max(fin, int(round(W[k]["o1"])) + F(0.2))
    return fin, ult


class Linea:
    """trabajo/linea.json + resolución de anclas. Un ancla dice DÓNDE del montaje cae algo, siempre colgado de lo que se
    dice o de una marca del EDL, nunca de un número de frame puesto a mano:
        (clip, "frase literal", n)        frame en que empieza esa frase (n = 0 primera vez, -1 la última)
        ((clip, "frase", n), segundos)    lo mismo, desplazado
        ("@marca", segundos)              marca del EDL (tag de una pieza, X("…") o "s3" = sección 3) + segundos
        "inicio" / "fin"
    """
    def __init__(self):
        if not os.path.exists(f"{TRABAJO}/linea.json"): raise SystemExit("Falta trabajo/linea.json: lanza antes paso1_alinear.py")
        d = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8"))
        self.piezas, self.palabras, self.marcas, self.secciones, self.total = d["piezas"], d["palabras"], d["marcas"], d["secciones"], d["total"]

    def ancla(self, a):
        if a == "inicio": return 0
        if a == "fin": return self.total
        if isinstance(a[0], str) and a[0].startswith("@"):
            if a[0][1:] not in self.marcas: raise SystemExit(f"marca desconocida {a[0]}; hay: {sorted(self.marcas)}")
            return self.marcas[a[0][1:]] + F(a[1] if len(a) > 1 else 0)
        if isinstance(a[0], (tuple, list)): return self.ancla(tuple(a[0])) + F(a[1])
        return int(round(self.palabras[buscar(self.palabras, *a)[0]]["o0"])) - 1

    def fin_frase(self, a):
        """Frame en que acaba la frase de un ancla de frase."""
        return int(round(self.palabras[buscar(self.palabras, *a)[1]]["o1"]))


def video():
    """Planos del montaje (trabajo/video.json), en una lista plana."""
    return [v for t in json.load(open(f"{TRABAJO}/video.json"))["tramos"] for v in t]
