"""frases.py: ¿alguna pieza de habla del EDL empieza o acaba A MEDIA FRASE?
Al elegir frases por texto es fácil coger solo el trozo «bueno» y dejar fuera el principio (el sujeto, el «hay que…»,
el «vamos a…») o el final (el remate, el verbo, de quién se habla). En el vídeo eso suena a frase cortada.

Para cada pieza T mira qué se dice justo ANTES y justo DESPUÉS en el bruto y MIDE en el audio si hay pausa en el corte
(los tiempos de Whisper no sirven: da las palabras pegadas aunque haya silencio, y no pone puntos). Avisa si:
  EMPIEZA A MEDIAS: en los VENTANA s de antes del corte hay voz casi sin pausa (venía hablando del tirón),
                    o la pieza arranca con una palabra que cuelga de lo anterior (porque, que, y, pero, además…);
  ACABA A MEDIAS:   en los VENTANA s de después sigue la voz sin pausa,
                    o la pieza termina en una palabra que pide continuación (que, para, de, el, y, porque…).

No decide: enseña. Cada aviso se LEE con su contexto y se resuelve en edl.py de una de estas tres maneras:
  - se alarga la pieza hasta el principio o el final de la frase (lo normal);
  - se deja, si lo que queda fuera es una muletilla («vale», «o sea»), una retoma o un arranque y lo de dentro se
    entiende solo: se apunta en OK_A_MEDIAS de edl.py ({"tag o primeras palabras": "por qué"}) y deja de avisar;
  - se quita la pieza, si entera no merece la pena.
Los cortes del tráiler (golpes sueltos a propósito) se listan aparte: se revisan, pero un golpe corto vale.

Uso (desde out/<slug>/, después de paso1_alinear.py):  frases.py      -> trabajo/frases.md
Sale con código 1 si queda algún aviso sin resolver."""
import json, os, re, sys
import numpy as np, soundfile as sf
from comun import FPS, IDIOMA, TRABAJO, norm, palabras
import edl      # después de comun

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(errors="replace")
VENTANA = 0.45       # s de audio que se miran a cada lado del corte
VOZ_DB = 12          # dB por encima del fondo del bruto para contar un instante como voz
PEGADO = 0.62        # parte de la ventana con voz a partir de la cual «va pegado»
CONTEXTO = 9         # palabras de antes y de después que se enseñan
# palabras que, al PRINCIPIO de una pieza, cuelgan de algo dicho antes (por idioma; se suman las que falten)
CUELGA = {"es": "porque que y pero ademas o ni sino pues entonces tambien tampoco aunque cuando donde como para de del al con sin por en a",
          "en": "because that and but or nor so then also though although when where which who to of with for at in"}
# palabras que, al FINAL de una pieza, piden que la frase siga
PIDE = {"es": "que para de del el la los las un una unos unas y o e ni porque a al en con por sin sobre como si pero es son estan se lo le me te nos mi tu su mis sus este ese muy mas tan cuando donde hay he ha han voy vas va vamos van ser estar",
        "en": "that to of the a an and or because for with in on at by as if but is are was were its my your his her our their these those very more so when where i you he she we they have has had will would can"}
cuelga = set(CUELGA.get(IDIOMA or "es", CUELGA["es"]).split()); pide = set(PIDE.get(IDIOMA or "es", PIDE["es"]).split())
OK = getattr(edl, "OK_A_MEDIAS", {})
mmss = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"

if not os.path.exists(f"{TRABAJO}/linea.json"): raise SystemExit("Falta trabajo/linea.json: lanza antes paso1_alinear.py")
linea = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8"))["piezas"]
borde = {}                               # item del EDL -> (segundo del bruto donde empieza, donde acaba)
for q in linea:
    if q["k"] == "T": x = borde.get(q["item"]); borde[q["item"]] = (min(x[0], q["in"]) if x else q["in"], max(x[1], q["out"]) if x else q["out"])

_env = {}
def voz(c, t0, t1):
    """Parte de [t0, t1] (s del bruto) en la que hay voz: instantes de 20 ms por encima del fondo del bruto."""
    if c not in _env:
        y = sf.read(f"{TRABAJO}/{c}.16k.wav", dtype="float32")[0]; n = len(y) // 320
        db = 10 * np.log10((y[:n * 320].reshape(n, 320) ** 2).mean(1) + 1e-10); _env[c] = (db, np.percentile(db, 20))
    db, fondo = _env[c]; x = db[max(0, int(t0 * 50)):max(0, int(t1 * 50))]
    return float((x > fondo + VOZ_DB).mean()) if len(x) else 0.0

zona = "cuerpo"; zonas = {}              # el tráiler se trata aparte
for i, p in enumerate(edl.EDL):
    if p["k"] == "X": zona = p["tag"]
    elif p["k"] == "S": zona = "cuerpo"
    zonas[i] = zona

out = ["# Frases a medias: piezas de habla que empiezan o acaban en mitad de una frase\n",
       "Formato: `antes` (voz antes del corte) «**LO QUE SUENA**» (voz después) `después`. 0 % = silencio, 100 % = sigue hablando.\n"]
avisos = vistos = 0; trailer = []; W = {}
_ts = [(i, p) for i, p in enumerate(edl.EDL) if p["k"] == "T"]
inicios = {(q["c"], q["a"]) for (i, p), (j, q) in zip(_ts, _ts[1:]) if q["c"] == p["c"] and q["a"] == p["b"] + 1 and zonas[i] == zonas[j]}
fines = {(p["c"], p["b"]) for (i, p), (j, q) in zip(_ts, _ts[1:]) if q["c"] == p["c"] and q["a"] == p["b"] + 1 and zonas[i] == zonas[j]}
for i, p in enumerate(edl.EDL):
    if p["k"] != "T" or i not in borde: continue
    c = p["c"]
    if c not in W: W[c] = palabras(c)
    w = W[c]; a, b = p["a"], p["b"]; txt = " ".join(x["p"].strip() for x in w[a:b + 1]); pri = norm(w[a]["p"]); ult = norm(w[b]["p"])
    t0, t1 = borde[i][0] / FPS, borde[i][1] / FPS
    va = voz(c, t0 - VENTANA, t0 - 0.03) if a > 0 else 0.0; vd = voz(c, t1 + 0.03, t1 + VENTANA) if b < len(w) - 1 else 0.0
    motivos = []
    sigue_de = (c, a - 1) in fines; sigue_en = (c, b + 1) in inicios      # el borde continúa en la pieza vecina: no es un corte
    if sigue_de: pass
    elif va >= PEGADO: motivos.append("EMPIEZA A MEDIAS (venía hablando)")
    elif pri in cuelga: motivos.append(f"EMPIEZA A MEDIAS (arranca con «{pri}»)")
    if sigue_en: pass
    elif vd >= PEGADO: motivos.append("ACABA A MEDIAS (sigue hablando)")
    elif ult in pide: motivos.append(f"ACABA A MEDIAS (termina en «{ult}»)")
    if not motivos: continue
    if any(k == p.get("tag") or norm(txt).startswith(norm(k)) for k in OK): vistos += 1; continue
    ant = " ".join(x["p"].strip() for x in w[max(0, a - CONTEXTO):a]); des = " ".join(x["p"].strip() for x in w[b + 1:b + 1 + CONTEXTO])
    lin = (f"- **{c}** {mmss(t0)} (palabra {a}){' · tag ' + p['tag'] if p.get('tag') else ''} · {'; '.join(motivos)}\n"
           f"  `…{ant}` ({round(100 * va)} %) «**{txt}**» ({round(100 * vd)} %) `{des}…`")
    if zonas[i] == "trailer": trailer.append(lin)
    else: avisos += 1; out.append(lin)
if trailer: out += ["\n## Tráiler (golpes sueltos: revisar que cada uno se entienda solo)\n"] + trailer
grises = len(trailer)
out.append(f"\n{avisos} avisos por resolver, {grises} del tráiler (golpes sueltos: revisar), {vistos} ya vistos y dados por buenos (OK_A_MEDIAS).")
open(f"{TRABAJO}/frases.md", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[2:]))
print(f"\n{TRABAJO}/frases.md: {len(borde)} piezas de habla; {avisos} avisos por resolver")
sys.exit(1 if avisos else 0)
