"""descartes.py: TODO lo que se ha quedado FUERA del montaje, para repasarlo antes de dar el vídeo por bueno.
Compara los brutos con el EDL y el plan y escribe trabajo/descartes.md con dos listas por bruto:

  HABLA que no está en el vídeo: cada tramo de la transcripción que ninguna pieza T usa, con sus tiempos, cuántas
  palabras son y cuánto se parece a algo que SÍ está («repetido»: casi siempre una retoma o la misma idea dicha otra vez).
  Lo marcado NUEVO (poco repetido y con chicha) es lo que hay que leer con lupa: puede ser una explicación, un dato, una
  anécdota, un chiste o una reacción que el vídeo no cuenta.

  IMAGEN que no está en el vídeo: los «mejores recursos» y los tramos con nota alta del registro visual que no salen
  ni como plano de recurso ni dentro de una pieza (un animal haciendo algo, una reacción, un momento sin palabras).
  Primero, los MOMENTOS sin usar (fallos, caídas, sustos, lo que hace el animal: «momentos» del registro): van en el
  vídeo aunque el plano sea feo, y si el creador lo cuenta después, el momento va antes que la frase que lo cuenta.

Uso (desde out/<slug>/, después de paso3_plan.py):  descartes.py
Obligatorio antes de entregar (SKILL.md § 2, paso 5): leer el archivo ENTERO y decidir cada NUEVO y cada imagen sin usar
con base/preferencias.md -> «Que el vídeo lo cuente todo». Lo que le da toque al vídeo y se haya quedado fuera SE METE
antes de renderizar (no se presenta como «descarte» algo que ya se sabe que vale); a quien edita se le cuenta al entregar
qué entró y qué se dejó fuera a propósito. Se pregunta antes solo lo dudoso (terceros, vida privada, promociones)."""
import glob, json, os, sys
from comun import ANALISIS, FPS, TRABAJO, norm, palabras
import edl      # después de comun

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(errors="replace")
PAUSA = 2.0          # s de silencio que parten un tramo descartado en dos
MIN_PAL = 5          # los tramos más cortos solo se cuentan
NUEVO = (0.40, 10)   # «NUEVO»: menos de ese parecido con lo usado y al menos esas palabras
mmss = lambda s: f"{int(s // 60)}:{s % 60:04.1f}"
tri = lambda ws: {tuple(ws[i:i + 3]) for i in range(len(ws) - 2)}

T = [p for p in edl.EDL if p["k"] == "T"]; clips = sorted({p["c"] for p in T})
W = {c: palabras(c) for c in clips}; N = {c: [norm(x["p"]) for x in W[c]] for c in clips}
usado = {c: set() for c in clips}
for p in T: usado[p["c"]].update(range(p["a"], p["b"] + 1))
dicho = set()        # trigramas de todo lo que SÍ suena en el vídeo
for c in clips:
    idx = sorted(usado[c]); ini = 0
    for k in range(1, len(idx) + 1):
        if k == len(idx) or idx[k] != idx[k - 1] + 1: dicho |= tri([N[c][i] for i in idx[ini:k] if N[c][i]]); ini = k

# qué trozos de cada bruto se VEN (piezas y planos de recurso), en segundos del bruto
visto = {}
try:
    for v in [x for t in json.load(open(f"{TRABAJO}/video.json"))["tramos"] for x in t]:
        visto.setdefault(v["clip"], []).append((v["in"] / FPS, (v["in"] + v["n"] * v["speed"]) / FPS))
except (OSError, ValueError, KeyError): print("AVISO: sin trabajo/video.json (lanza antes paso3_plan.py): la lista de imagen cuenta solo las piezas V del EDL")
for p in edl.EDL:
    if p["k"] == "V": visto.setdefault(p["c"], []).append((p["t0"], p["t1"]))
solape = lambda c, a, b: sum(max(0, min(b, y) - max(a, x)) for x, y in visto.get(c, []))

out = [f"# Descartes de «{edl.__name__}» — lo que hay en los brutos y NO está en el vídeo\n",
       "Leer entero antes de entregar. NUEVO = no se parece a nada que suene en el vídeo: decidir uno a uno.\n"]
res = []
for c in clips:
    w, n = W[c], N[c]; runs = []; ini = None
    for i in range(len(w) + 1):
        fuera = i < len(w) and i not in usado[c]
        corta = ini is not None and (not fuera or w[i]["t"] - w[i - 1]["fin"] > PAUSA)
        if corta: runs.append((ini, i - 1)); ini = None
        if fuera and ini is None: ini = i
    tot = len(w); us = len(usado[c]); res.append((c, tot, us))
    out.append(f"\n## {c} — habla: {us} de {tot} palabras en el vídeo ({100 * us // max(tot, 1)} %)\n")
    cortos = 0
    for a, b in runs:
        ws = [x for x in n[a:b + 1] if x]
        if len(ws) < MIN_PAL: cortos += 1; continue
        t3 = tri(ws); rep = len(t3 & dicho) / max(len(t3), 1); nuevo = rep < NUEVO[0] and len(ws) >= NUEVO[1]
        txt = " ".join(x["p"].strip() for x in w[a:b + 1])
        out.append(f"- {'**NUEVO** ' if nuevo else ''}{mmss(w[a]['t'])}–{mmss(w[b]['fin'])} · {len(ws)} pal · repetido {round(100 * rep)} % · {txt}")
    if cortos: out.append(f"- (+ {cortos} trozos de menos de {MIN_PAL} palabras: muletillas, arranques)")

out.append("\n\n# Imagen del registro visual que no sale en el vídeo\n")
for f in sorted(glob.glob(f"{ANALISIS}/visual/*.json")):
    d = json.load(open(f, encoding="utf-8")); c = d.get("clip") or os.path.basename(f).split("_")[0].split(".")[0]; lin = []
    for r in d.get("momentos", []):
        if solape(c, r["t0"], r["t1"]) < 0.5: lin.append(f"- **MOMENTO sin usar** [{r.get('tipo', '')}] {mmss(r['t0'])}–{mmss(r['t1'])} · {r.get('que', '')}" + (f" · luego dice: {r['luego_dice']}" if r.get("luego_dice") else "") + " → MÉTELO (preferencias → Que el vídeo lo cuente todo)")
    for r in d.get("mejores_recursos", []):
        if solape(c, r["t0"], r["t1"]) < 0.3: lin.append(f"- **MEJOR RECURSO sin usar** {mmss(r['t0'])}–{mmss(r['t1'])} · {r.get('que', '')} · para: {r.get('para', '')}")
    for r in d.get("tramos", []):
        if r.get("recurso", 0) >= 2 and solape(c, r["t0"], r["t1"]) < 0.3:
            lin.append(f"- tramo con nota {r['recurso']} sin usar {mmss(r['t0'])}–{mmss(r['t1'])} · [{r.get('tipo', '')}] {r.get('que', '')}" + (f" · dice: {r['dice']}" if r.get("dice") else ""))
    if lin: out.append(f"\n## {os.path.basename(f)}\n"); out += lin

open(f"{TRABAJO}/descartes.md", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
for c, tot, us in res: print(f"{c}: {us}/{tot} palabras en el vídeo ({100 * us // max(tot, 1)} %)")
print(f"{TRABAJO}/descartes.md ({sum(1 for l in out if '**NUEVO**' in l)} tramos de habla NUEVOS, {sum(1 for l in out if 'sin usar' in l)} imágenes sin usar, {sum(1 for l in out if 'MOMENTO sin usar' in l)} MOMENTOS sin usar): LÉELO ENTERO")
