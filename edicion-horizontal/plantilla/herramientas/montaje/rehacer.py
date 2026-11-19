"""rehacer.py guardar | borrar: tras cambiar plan.py o edl.py, rehace SOLO los tramos y capas que cambian.
  1) ANTES de paso3_plan.py:  rehacer.py guardar   (copia trabajo/video.json y capas.json a trabajo/antes_*.json)
  2) paso3_plan.py  (y se comprueba como siempre: ver.py, hojas)
  3) rehacer.py borrar        (borra los trabajo/tramos/tNNN.* que cambian y las capas trabajo/capas/c<a>.mov cuyo rango
                               cambia, queda huérfano o contiene un gráfico nuevo, quitado o cambiado)
  4) paso3_plan.py && render_todo.py ../AAAA-MM-DD_<slug>_v2.mp4: reanuda y solo hace lo borrado; el audio (paso5/6) y
     unir se rehacen siempre.
Un tramo se rehace si cambia algún plano suyo o alguna capa que cae en él. Lo que este script NO ve: parches de
tapar.py / tapar_persona.py / foco.py rehechos (borra a mano los tramos de esos planos) y cambios en un gráfico de
Remotion (.tsx) sin cambiar capas.json (borra esas capas a mano).
Por qué: SKILL.md decía «compara video.json con el anterior y borra esos tramos» sin herramienta; en las tres
correcciones de vaciamos-estanque (2026-11-19) se hizo con un script de usar y tirar, que es este."""
import glob, json, os, shutil, sys
from comun import CAPAS_JSON, TRABAJO

VJ = f"{TRABAJO}/video.json"; A_V, A_C = f"{TRABAJO}/antes_video.json", f"{TRABAJO}/antes_capas.json"
orden = sys.argv[1] if len(sys.argv) > 1 else ""
if orden == "guardar":
    shutil.copy(VJ, A_V); shutil.copy(CAPAS_JSON, A_C); raise SystemExit("guardado: ahora cambia plan.py/edl.py, lanza paso3_plan.py y luego rehacer.py borrar")
if orden != "borrar": raise SystemExit(__doc__)
if not (os.path.exists(A_V) and os.path.exists(A_C)): raise SystemExit("falta trabajo/antes_*.json: «rehacer.py guardar» se lanza ANTES de paso3_plan.py")
if os.path.getmtime(VJ) <= os.path.getmtime(A_V): raise SystemExit("video.json no ha cambiado desde «guardar»: lanza antes paso3_plan.py")
s = lambda x: json.dumps(x, sort_keys=True)
V1, V2 = json.load(open(A_V)), json.load(open(VJ))
C1, C2 = json.load(open(A_C, encoding="utf-8")), json.load(open(CAPAS_JSON, encoding="utf-8"))
glob_cambia = any(s(C1.get(k)) != s(C2.get(k)) for k in ("marca", "creador", "ancho", "alto", "fps"))
it1 = {s(i) for i in C1["items"]}; it2 = {s(i) for i in C2["items"]}
cambian = [(i["f0"], i["f1"]) for i in C2["items"] if s(i) not in it1] + [(i["f0"], i["f1"]) for i in C1["items"] if s(i) not in it2]   # nuevos o cambiados + quitados
cruza = lambda a, b: any(x < b and y > a for x, y in cambian)
rangos_viejos = {r[0]: r[1] for r in V1["rangos"]}; rangos_nuevos = {(a, b) for a, b in V2["rangos"]}
borrados, capas_fuera = [], []
for f in glob.glob(f"{TRABAJO}/capas/c*.mov"):
    if f.endswith(".tmp.mov"): continue
    try: a = int(os.path.basename(f)[1:-4])
    except ValueError: continue
    b = rangos_viejos.get(a)
    if glob_cambia or b is None or (a, b) not in rangos_nuevos or cruza(a, b):
        os.remove(f); borrados.append(f); capas_fuera.append((a, b if b is not None else a))
for k, tr in enumerate(V2["tramos"]):
    o0, o1 = tr[0]["o"], tr[-1]["o"] + tr[-1]["n"]
    if k >= len(V1["tramos"]) or s(V1["tramos"][k]) != s(tr) or cruza(o0, o1) or any(a < o1 and b > o0 for a, b in capas_fuera) \
       or any(a < o1 and b > o0 and (a, b) not in {tuple(r) for r in V1["rangos"]} for a, b in V2["rangos"]):
        for f in glob.glob(f"{TRABAJO}/tramos/t{k:03d}.*"): os.remove(f); borrados.append(f)
for f in glob.glob(f"{TRABAJO}/tramos/t*.*"):            # tramos que ya no existen (el montaje tiene menos)
    try: k = int(os.path.basename(f)[1:4])
    except ValueError: continue
    if k >= len(V2["tramos"]): os.remove(f); borrados.append(f)
if glob_cambia: print("cambió la marca o el lienzo: se rehacen TODAS las capas")
print(len(borrados), "archivos borrados:", ", ".join(sorted(os.path.basename(f) for f in borrados)[:40]) + (" …" if len(borrados) > 40 else ""))
print("lanza render_todo.py con una salida nueva (_v2): solo hace lo borrado")
