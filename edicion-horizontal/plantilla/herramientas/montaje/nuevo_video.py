"""nuevo_video.py SLUG CARPETA_DE_BRUTOS [CREADOR]: prepara un vídeo nuevo (CREADOR = carpeta de personal/; sobra si solo hay uno). Se lanza desde la raíz de la carpeta de edición.
Crea out/<slug>/ (proyecto.py, edl.py y plan.py desde herramientas/montaje/plantilla_video/), la composición de capas
estudio/src/videos/<slug>/Capas.tsx (+ capas.json vacío) y la registra en estudio/src/Root.tsx. No pisa nada que exista.
Mide los brutos para proponer lienzo y fps: el lienzo es el del MEJOR bruto (3840x2160, 2560x1440 o 1920x1080, nunca menos)."""
import glob, json, os, re, subprocess, sys

if len(sys.argv) not in (3, 4): raise SystemExit(__doc__)
slug, brutos = sys.argv[1], os.path.abspath(sys.argv[2]).replace("\\", "/")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug): raise SystemExit("SLUG en minúsculas con guiones: mi-video")
if not os.path.isdir("estudio/src") or not os.path.isdir("herramientas/montaje"): raise SystemExit("Lánzalo desde la raíz de la carpeta de edición")
AQUI = os.path.dirname(os.path.abspath(__file__)); PL = f"{AQUI}/plantilla_video"
comp = "".join(x.capitalize() for x in slug.split("-")) + "Capas"
if comp[0].isdigit(): comp = "V" + comp      # un identificador de JS no puede empezar por una cifra (slug "1311" -> V1311Capas)

# lienzo y fps: los del mejor bruto / los más frecuentes
fs = [f for f in glob.glob(f"{brutos}/*") if f.lower().endswith((".mp4", ".mov", ".m4v", ".mxf", ".mkv"))]
if not fs: raise SystemExit(f"No hay vídeos en {brutos}")
alto, fps_n = 0, {}
for f in fs:
    s = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration", "-of", "json", f], capture_output=True, text=True).stdout)
    st = s["streams"][0]; a, b = st["r_frame_rate"].split("/"); fps = round(float(a) / float(b))
    rot = next((abs(int(float(x["rotation"]))) for x in st.get("side_data_list", []) if "rotation" in x), 0)
    w, h = (st["height"], st["width"]) if rot in (90, 270) else (st["width"], st["height"])
    if w > h: alto = max(alto, h)
    fps_n[fps] = fps_n.get(fps, 0) + float(s["format"]["duration"])
alto = 2160 if alto >= 2160 else 1440 if alto >= 1440 else 1080; ancho = alto * 16 // 9
fps = max(fps_n, key=fps_n.get)
if fps > 30: fps //= 2      # brutos a 50/60 fps: el vídeo sale a 25/30

d = f"out/{slug}"; os.makedirs(f"{d}/trabajo", exist_ok=True)
def copia(origen, destino, cambios):
    if os.path.exists(destino): print("ya existe, no se toca:", destino); return
    t = open(origen, encoding="utf-8").read()
    for k, v in cambios.items(): t = t.replace(k, str(v))
    os.makedirs(os.path.dirname(destino), exist_ok=True); open(destino, "w", encoding="utf-8", newline="\n").write(t); print("+", destino)
cres = sorted(x for x in os.listdir("personal") if os.path.isdir(f"personal/{x}") and not x.startswith(("_", "."))) if os.path.isdir("personal") else []
creador = sys.argv[3] if len(sys.argv) == 4 else (cres[0] if len(cres) == 1 else "")
if creador and creador not in cres: raise SystemExit(f"No existe personal/{creador}/: créalo con herramientas/montaje/nuevo_creador.py {creador}")
if not creador: print("AVISO: " + ("hay varios creadores: pon CREADOR en proyecto.py" if cres else "no hay ningún creador en personal/: créalo con nuevo_creador.py (o el vídeo saldrá solo con las bases)"))
cambios = {"__CREADOR__": creador, "__SLUG__": slug, "__COMP__": comp, "__BRUTOS__": brutos, "__FPS__": fps, "__ANCHO__": ancho, "__ALTO__": alto}
for n in ("proyecto.py", "edl.py", "plan.py"): copia(f"{PL}/{n}", f"{d}/{n}", cambios)
v = f"estudio/src/videos/{slug}"
copia(f"{PL}/Capas.tsx", f"{v}/Capas.tsx", cambios)
if not os.path.exists(f"{v}/capas.json"):
    json.dump({"fps": fps, "total": 1, "ancho": ancho, "alto": alto, "items": [], "rangos": []}, open(f"{v}/capas.json", "w"))
root = "estudio/src/Root.tsx"; t = open(root, encoding="utf-8").read()
if f"./videos/{slug}/Capas" not in t:
    imp = f'import * as {comp} from "./videos/{slug}/Capas";\n'
    linea = f'      <Composition id="{comp}" component={{{comp}.Capas}} width={{{comp}.ANCHO}} height={{{comp}.ALTO}} fps={{{comp}.FPS}} durationInFrames={{{comp}.TOTAL}} />\n'
    m1 = re.search(r"// IMPORTS-VIDEOS.*\n", t); m2 = re.search(r" *\{/\* COMPOSICIONES.*\n", t)
    if not m1 or not m2: print(f"AVISO: no encuentro los marcadores en {root}; añade a mano:\n{imp}{linea}")
    else:
        t = t[:m2.end()] + linea + t[m2.end():]; t = t[:m1.end()] + imp + t[m1.end():]
        open(root, "w", encoding="utf-8", newline="\n").write(t); print("+ composición", comp, "en", root)
print(f"\nLienzo {ancho}x{alto} a {fps} fps (revísalo en {d}/proyecto.py). Siguiente:\n  cd {d} && <python de herramientas/.venv> ../../herramientas/montaje/paso0_preparar.py")
