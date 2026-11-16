"""canal_youtube.py @canal [--meses 12] [--salida refs/_youtube/<canal>]: baja de un canal de YouTube, para ESTUDIAR sus
títulos, miniaturas y descripciones (método: <skill>/base/refs/_youtube/METODO.md):

    <salida>/crudo.jsonl        metadatos de cada vídeo largo del periodo, en su idioma ORIGINAL (no la traducción de YouTube)
    <salida>/videos.json        lo mismo, ordenado, con n (1 = el más reciente), días y ratio
    <salida>/titulos.tsv        n, fecha, visitas, ratio, minutos, caracteres, título
    <salida>/descripciones.txt  la descripción de cada vídeo (recortada a 1100 caracteres; entera en videos.json)
    <salida>/resumen.json       medidas automáticas (longitudes, % con cifra…): orientan, hay que comprobarlas leyendo
    <salida>/miniaturas/<id>.jpg   la miniatura original de cada vídeo
    <salida>/hojas/NN.jpg       hojas de contacto de 16 miniaturas con n, fecha, ratio y título; extremos.jpg = las 8 de
                                mayor ratio y las 8 de menor
    <salida>/detalle/NN.jpg     las mismas miniaturas en GRANDE (4 por hoja), de mayor a menor ratio: para ver los
                                retoques, el texto fino y hacia dónde va el ojo (ENCARGO_DETALLE.md)

ratio = visitas del vídeo / mediana del canal (calculada con los vídeos de más de 21 días; los más recientes llevan *).
No es el CTR: sirve para comparar vídeos DENTRO del mismo canal. Necesita yt-dlp (winget install yt-dlp, brew install
yt-dlp o pip install yt-dlp en la .venv). Se lanza desde la raíz de la carpeta de edición. Solo lee datos públicos."""
import argparse, concurrent.futures as cf, datetime as dt, json, os, re, shutil, statistics as st, subprocess, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("canal", help="@handle o URL del canal"); ap.add_argument("--meses", type=int, default=12)
ap.add_argument("--salida"); ap.add_argument("--solo-tablas", action="store_true", help="no vuelve a bajar: rehace tablas y hojas")
a = ap.parse_args()
url = a.canal if a.canal.startswith("http") else f"https://www.youtube.com/{a.canal if a.canal.startswith('@') else '@' + a.canal}"
nombre = re.sub(r"[^A-Za-z0-9_-]", "", url.rstrip("/").split("/")[-1].lstrip("@")) or "canal"
if not url.rstrip("/").endswith("/videos"): url = url.rstrip("/") + "/videos"                    # solo vídeos largos, no Shorts ni directos
SAL = a.salida or f"refs/_youtube/{nombre}"; MIN, HOJ, DET = f"{SAL}/miniaturas", f"{SAL}/hojas", f"{SAL}/detalle"
for d in (SAL, MIN, HOJ, DET): os.makedirs(d, exist_ok=True)
HOY = dt.date.today(); desde = (HOY - dt.timedelta(days=round(a.meses * 30.44))).strftime("%Y%m%d")
CAMPOS = "id,title,description,upload_date,view_count,like_count,comment_count,duration,language,tags,chapters,channel,channel_follower_count,availability,live_status"

# ---------- 1. metadatos ----------
if not a.solo_tablas:
    ytdlp = [shutil.which("yt-dlp")] if shutil.which("yt-dlp") else [sys.executable, "-m", "yt_dlp"]
    if os.path.exists(f"{SAL}/crudo.jsonl"): os.remove(f"{SAL}/crudo.jsonl")
    print(f"Bajando metadatos de {url} desde {desde} (unos 3 s por vídeo)…", flush=True)
    r = subprocess.run([*ytdlp, "--skip-download", "--no-warnings", "--ignore-errors", "--ignore-no-formats-error", "--lazy-playlist",
                        "--dateafter", desde, "--break-on-reject", "--extractor-args", "youtube:player_skip=js,configs;player_client=web",
                        "--print-to-file", "%(.{" + CAMPOS + "})j", f"{SAL}/crudo.jsonl", url], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if not os.path.exists(f"{SAL}/crudo.jsonl"): raise SystemExit("yt-dlp no ha devuelto nada:\n" + (r.stderr or r.stdout)[-800:])   # 101 = corte por fecha: normal

# ---------- 2. tablas ----------
V = [json.loads(l) for l in open(f"{SAL}/crudo.jsonl", encoding="utf-8") if l.strip()]
V = [v for v in V if v.get("upload_date") and v.get("view_count") and v.get("live_status") in (None, "not_live", "was_live")]
V = sorted({v["id"]: v for v in V}.values(), key=lambda v: v["upload_date"], reverse=True)
if not V: raise SystemExit("Ningún vídeo en el periodo.")
for v in V: v["dias"] = (HOY - dt.date(int(v["upload_date"][:4]), int(v["upload_date"][4:6]), int(v["upload_date"][6:]))).days
M = st.median([v["view_count"] for v in V if v["dias"] > 21] or [v["view_count"] for v in V])
for i, v in enumerate(V, 1): v["n"] = i; v["ratio"] = round(v["view_count"] / M, 2)
json.dump(V, open(f"{SAL}/videos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
with open(f"{SAL}/titulos.tsv", "w", encoding="utf-8") as o:
    o.write(f"# {nombre} — {len(V)} vídeos desde {V[-1]['upload_date']} — mediana {int(M):,} visitas (vídeos de >21 días)\n")
    o.write("n\tfecha\tvisitas\tratio\tmin\tcar\ttítulo\n")
    for v in V: o.write(f"{v['n']}\t{v['upload_date']}\t{v['view_count']}\t{v['ratio']}{'*' if v['dias'] <= 21 else ''}\t{round((v.get('duration') or 0) / 60)}\t{len(v['title'])}\t{v['title']}\n")
with open(f"{SAL}/descripciones.txt", "w", encoding="utf-8") as o:
    for v in V:
        d = (v.get("description") or "").strip()
        o.write(f"=== {v['n']} | {v['upload_date']} | x{v['ratio']} | {v['title']}\n[{len(d)} car, {d.count(chr(10)) + 1} líneas]\n{d[:1100]}{' […]' if len(d) > 1100 else ''}\n\n")
T = [v["title"] for v in V]; D = [(v.get("description") or "") for v in V]
med = lambda xs: round(st.median(xs), 1) if xs else 0
pct = lambda xs: round(100 * sum(1 for x in xs if x) / max(len(xs), 1))
mayus = lambda t: (lambda w: sum(1 for x in w if x.isupper()) / max(len(w), 1))(re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]{3,}", t))
json.dump({
    "canal": nombre, "videos": len(V), "mediana_visitas": int(M), "suscriptores": V[0].get("channel_follower_count"),
    "duracion_mediana_min": med([(v.get("duration") or 0) / 60 for v in V]), "titulo_car_mediana": med([len(t) for t in T]),
    "titulo_palabras_mediana": med([len(t.split()) for t in T]), "%_con_cifra": pct([re.search(r"\d", t) for t in T]),
    "%_con_dinero": pct([re.search(r"[$€£]", t) for t in T]), "%_con_?": pct(["?" in t for t in T]), "%_con_!": pct(["!" in t for t in T]),
    "%_todo_mayusculas": pct([mayus(t) > 0.9 for t in T]), "%_alguna_palabra_en_mayusculas": pct([0 < mayus(t) <= 0.9 for t in T]),
    "%_con_parentesis": pct(["(" in t for t in T]), "desc_car_mediana": med([len(d) for d in D]),
    "%_desc_con_capitulos_escritos": pct([len(re.findall(r"^\s*\d?\d:\d\d", d, re.M)) >= 3 for d in D]), "%_desc_con_enlaces": pct(["http" in d for d in D]),
    "%_desc_con_hashtags": pct([re.search(r"#\w", d) for d in D]),
    "top5": [(v["ratio"], v["title"]) for v in sorted(V, key=lambda v: -v["ratio"])[:5]],
    "bottom5": [(v["ratio"], v["title"]) for v in sorted([v for v in V if v["dias"] > 21], key=lambda v: v["ratio"])[:5]],
}, open(f"{SAL}/resumen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 3. miniaturas y hojas ----------
W, H, PIE, COLS, FILAS = 480, 270, 62, 4, 4
def fuente(negrita, tam=17):
    for f in (("C:/Windows/Fonts/segoeuib.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf") if negrita else ("C:/Windows/Fonts/segoeui.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf")):
        if os.path.exists(f): return ImageFont.truetype(f, tam)
    return ImageFont.load_default()
FU, FB = fuente(False), fuente(True)


def bajar(vid):
    dst = f"{MIN}/{vid}.jpg"
    if os.path.exists(dst) and os.path.getsize(dst) > 2000: return
    for n in ("maxresdefault", "hq720", "sddefault", "hqdefault"):                                  # la miniatura por defecto es la original
        try:
            d = urllib.request.urlopen(urllib.request.Request(f"https://i.ytimg.com/vi/{vid}/{n}.jpg", headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read()
            if len(d) > 2000: open(dst, "wb").write(d); return
        except Exception: pass


def hoja(vs, sal, W=W, H=H, PIE=PIE, COLS=COLS, visitas=False):
    """Hoja de contacto. Por defecto 4 columnas de 480 px; con W=960, COLS=2 es la hoja de detalle."""
    k = W / 480; fu, fb = fuente(False, round(17 * k ** 0.5)), fuente(True, round(17 * k ** 0.5)); alto = round(20 * k ** 0.5)
    im = Image.new("RGB", (COLS * W, ((len(vs) + COLS - 1) // COLS) * (H + PIE)), (18, 18, 18)); d = ImageDraw.Draw(im)
    for i, v in enumerate(vs):
        x, y = (i % COLS) * W, (i // COLS) * (H + PIE); p = f"{MIN}/{v['id']}.jpg"
        if os.path.exists(p):
            t = Image.open(p).convert("RGB"); tw, th = t.size
            if tw / th < 1.7: nh = int(tw * 9 / 16); t = t.crop((0, (th - nh) // 2, tw, (th - nh) // 2 + nh))     # 4:3 con bandas -> 16:9
            im.paste(t.resize((W - 4, H - 4), Image.LANCZOS), (x + 2, y + 2))
        r = v["ratio"]; col = (120, 230, 120) if r >= 1.5 else (240, 120, 120) if r <= 0.6 else (230, 230, 230)
        d.text((x + 6, y + H), f"#{v['n']} · {v['upload_date'][2:]} · x{r}{'*' if v['dias'] <= 21 else ''}" + (f" · {v['view_count']:,} visitas" if visitas else ""), font=fb, fill=col)
        lin, out = "", []
        for w in v["title"].split():
            if d.textlength((lin + " " + w).strip(), font=fu) <= W - 12: lin = (lin + " " + w).strip()
            else: out.append(lin); lin = w
        for n, l in enumerate((out + [lin])[:2]): d.text((x + 6, y + H + alto * (n + 1)), l, font=fu, fill=(235, 235, 235))
    im.save(sal, quality=88)


with cf.ThreadPoolExecutor(12) as ex: list(ex.map(bajar, [v["id"] for v in V]))
for k in range(0, len(V), COLS * FILAS): hoja(V[k:k + COLS * FILAS], f"{HOJ}/{k // (COLS * FILAS) + 1:02d}.jpg")
madur = [v for v in V if v["dias"] > 21]
hoja(sorted(madur, key=lambda v: -v["ratio"])[:8] + sorted(madur, key=lambda v: v["ratio"])[:8], f"{HOJ}/extremos.jpg")
orden = sorted(madur, key=lambda v: -v["ratio"]) + [v for v in V if v["dias"] <= 21]                 # detalle: 4 grandes por hoja, de mayor a menor ratio
for f in os.listdir(DET): os.remove(f"{DET}/{f}")
for k in range(0, len(orden), 4): hoja(orden[k:k + 4], f"{DET}/{k // 4 + 1:02d}.jpg", W=960, H=540, PIE=96, COLS=2, visitas=True)
faltan = sum(1 for v in V if not os.path.exists(f"{MIN}/{v['id']}.jpg"))
print(f"{nombre}: {len(V)} vídeos · mediana {int(M):,} visitas · {(len(V) + 15) // 16} hojas + extremos + {(len(V) + 3) // 4} de detalle · miniaturas que faltan: {faltan} -> {SAL}/")
