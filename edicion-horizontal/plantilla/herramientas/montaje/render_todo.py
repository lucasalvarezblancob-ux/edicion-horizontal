"""render_todo.py SALIDA.mp4 [--hilos N] [--paralelo N] [--enc auto|nvenc|x264|videotoolbox]: el render entero, de un tirón y
REANUDABLE: capas (Remotion) -> tramos (ffmpeg) -> audio (paso 5 y, si hay música, paso 6) -> unir.

Es lo mismo que lanzar los pasos a mano (SKILL.md § 2, paso 6), con tres cosas más:
  - retoma donde se quedó: no repite las capas ni los tramos que ya existen, y limpia los restos a medias de un proceso
    que murió (trabajo/capas/*.tmp.mov, trabajo/tramos/*.tmp.mp4);
  - si algo falla (casi siempre, por memoria), lo reintenta hasta tres veces con menos carga: la mitad de navegadores
    para las capas y los tramos de uno en uno;
  - el vídeo se escribe con otro nombre y solo al final pasa a llamarse SALIDA: si SALIDA existe, está entero.
No rehace nada que haya CAMBIADO en el plan: eso sigue siendo cosa tuya (borrar o apartar los tramos y capas afectados
antes de lanzarlo). No pisa una SALIDA que ya existe.

Uso (desde out/<slug>/, después de paso3_plan.py y de comprobarlo todo con ver.py), en segundo plano:
  render_todo.py ../AAAA-MM-DD_<slug>.mp4
y, mientras dura, vigilar_render.py cada 5-10 minutos (libera memoria y avisa si se ha parado)."""
import glob, json, os, subprocess, sys
from comun import PY, TRABAJO
import plan      # después de comun
from vigilar_render import render_vivo

AQUI = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(errors="replace")
args = sys.argv[1:]; op = lambda k, d: args[args.index(k) + 1] if k in args else d
libres = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--hilos", "--paralelo", "--enc"))]
if not libres: raise SystemExit(__doc__)
salida = libres[0]; hilos = int(op("--hilos", os.environ.get("CAPAS_HILOS", "6"))); par = int(op("--paralelo", "2")); enc = op("--enc", "auto")

if os.path.exists(salida): raise SystemExit(f"{salida} ya existe: no se pisa. Si quieres rehacerlo, dale otro nombre a la salida o aparta ese archivo.")
otros = render_vivo()
if otros: raise SystemExit(f"Ya hay un render en marcha (procesos {[p[0] for p in otros]}): no se lanza otro encima.")
for f in glob.glob(f"{TRABAJO}/capas/*.tmp.mov") + glob.glob(f"{TRABAJO}/tramos/*.tmp.mp4"): os.remove(f)      # restos de un proceso muerto

paso = lambda nombre, *a, **env: subprocess.run([PY, f"{AQUI}/{nombre}", *a], env={**os.environ, **{k: str(v) for k, v in env.items()}}).returncode
N = len(json.load(open(f"{TRABAJO}/video.json"))["tramos"])
faltan = lambda: [i for i in range(N) if not os.path.exists(f"{TRABAJO}/tramos/t{i:03d}.mp4")]

for intento in (1, 2, 3):
    print(f"== intento {intento}: capas ({hilos} navegadores a la vez)", flush=True)
    ok = paso("paso4_render.py", "capas", CAPAS_HILOS=hilos) == 0
    if ok and faltan():
        print(f"== tramos: faltan {len(faltan())} de {N} ({par} a la vez)", flush=True)
        paso("paso4_render.py", "tramos", enc, str(par), *map(str, faltan()))
    if ok and not faltan(): break
    hilos = max(2, hilos // 2); par = 1
else:
    raise SystemExit(f"No se ha podido terminar tras tres intentos; faltan los tramos {faltan()}. Mira el error de arriba.")

print("== audio", flush=True)
if paso("paso5_audio.py"): raise SystemExit("paso5_audio.py ha fallado")
if getattr(plan, "PISTAS", None) and getattr(plan, "VENTANAS", None) and paso("paso6_musica.py"): raise SystemExit("paso6_musica.py ha fallado")
print("== unir", flush=True)
base, ext = os.path.splitext(salida); parcial = f"{base}.parcial{ext}"
if paso("paso4_render.py", "unir", parcial) or not os.path.exists(parcial): raise SystemExit("la unión ha fallado")
os.replace(parcial, salida); print(f"LISTO: {salida} ({os.path.getsize(salida) / 2**30:.2f} GB). Falta comprobar el archivo final (SKILL.md § 2, paso 7).")
