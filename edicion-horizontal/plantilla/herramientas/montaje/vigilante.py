"""vigilante.py: el VIGILANTE de la edición. Se lanza al empezar a editar un vídeo y se queda en segundo plano hasta la
entrega; cada 10 minutos:
  1. busca procesos de la edición COLGADOS (Remotion, esbuild, ffmpeg, los pasos de herramientas/…: vivos pero sin gastar
     CPU desde la pasada anterior) y los cierra con todo lo que cuelga de ellos;
  2. si había un render pedido (render_todo.py deja trabajo/render_pedido.json) y se ha muerto o se ha colgado, lo
     RELANZA (retoma donde se quedó; como mucho 3 veces);
  3. LIBERA MEMORIA: cierra los navegadores de Remotion y los servicios de esbuild que se han quedado huérfanos y, en
     Windows con poca memoria, recorta lo que no es de la edición (vigilar_render.py). Nunca cierra nada del usuario.
Todo lo que hace va a trabajo/vigilante.log.

Por qué existe (Lucas, 2026-11-17, alimentacion): «sobre el parón de casi 3 h, quiero que cuando estés editando un vídeo
haya un agente que cada 10 min revise si hay algún proceso parado y lo relance… y de paso, que libere algo de RAM».
Causa del parón: una orden de Remotion en PRIMER PLANO se colgó (el servicio de esbuild se quedó con la salida abierta) y
la herramienta Bash esperó 2 h 40 min sin devolver nada. Con la sesión bloqueada no salta ningún cron de la sesión: la
vigilancia que había (vigilar_render.py, solo durante el render) no podía ni empezar. Por eso este vigilante es un
PROCESO APARTE: al cerrar lo colgado, la orden que esperaba vuelve y la sesión sigue sola.

Uso (desde out/<slug>/):
  vigilante.py               bucle (lánzalo en segundo plano al empezar: SKILL.md § 2, paso 0)
  vigilante.py estado        una pasada sin cerrar nada: qué hay en marcha y lo último que ha hecho el vigilante
  vigilante.py parar         lo para (al entregar)
Opciones: --cada SEG (600), --colgado SEG (sin CPU durante ese tiempo = colgado; 600). No cambia el montaje ni el resultado."""
import json, os, re, signal, subprocess, sys, time
from datetime import datetime
from vigilar_render import WIN, memoria, procesos, recortar, tramos, NO

T = "trabajo"; LOG, EST, STOP, PED = f"{T}/vigilante.log", f"{T}/vigilante.json", f"{T}/vigilante.parar", f"{T}/render_pedido.json"
NUESTRO = re.compile(r"herramientas[/\\]|remotion|esbuild|chrome-headless-shell|whisper|ffmpeg|ffprobe", re.I)
RENDER = re.compile(r"render_todo|paso4_render|paso5_audio|paso6_musica")
args = sys.argv[1:]; op = lambda k, d: float(args[args.index(k) + 1]) if k in args else d
CADA, COLGADO = op("--cada", 600), op("--colgado", 600)
AQUI = os.path.dirname(os.path.abspath(__file__))


def log(m):
    l = f"{datetime.now():%H:%M} {m}"; print(l, flush=True); open(LOG, "a", encoding="utf-8").write(l + "\n")


def cpu():
    """{pid: segundos de CPU acumulados} de todos los procesos."""
    out = {}
    if WIN:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", "Get-CimInstance Win32_Process | ForEach-Object { \"$($_.ProcessId) $($_.KernelModeTime + $_.UserModeTime)\" }"], capture_output=True, text=True).stdout
        for l in r.split("\n"):
            c = l.split()
            if len(c) == 2 and c[0].isdigit() and c[1].isdigit(): out[int(c[0])] = int(c[1]) / 1e7
        return out
    for l in subprocess.run(["ps", "-axo", "pid=,time="], capture_output=True, text=True).stdout.splitlines():
        c = l.split()
        if len(c) != 2: continue
        d, _, hms = c[1].rpartition("-"); p = [float(x) for x in hms.split(":")]
        while len(p) < 3: p.insert(0, 0)
        out[int(c[0])] = (int(d) if d else 0) * 86400 + p[0] * 3600 + p[1] * 60 + p[2]
    return out


def grupos(ps):
    """Procesos de la edición agrupados por su raíz (el más alto de la cadena que es nuestro). {raíz: [pids]}"""
    yo = set(); x = os.getpid(); padre = {p[0]: p[3] for p in ps}
    while x and x not in yo: yo.add(x); x = padre.get(x, 0)
    nuestro = {p[0] for p in ps if NUESTRO.search(p[2]) and p[0] not in yo and "vigilante" not in p[2]}
    hijos = {}
    for pid, _, _, pp in ps: hijos.setdefault(pp, []).append(pid)
    def todos(r):
        out, pila = [], [r]
        while pila: q = pila.pop(); out.append(q); pila += hijos.get(q, [])
        return out
    raices = [p for p in nuestro if padre.get(p) not in nuestro]
    return {r: todos(r) for r in raices}


def cerrar(pids):
    for sig in (signal.SIGTERM, getattr(signal, "SIGKILL", signal.SIGTERM)):
        for p in reversed(pids):
            try: os.kill(p, sig)
            except OSError: pass
        time.sleep(4)


def pasada(actuar=True):
    ps = procesos(); cmd = {p[0]: p[2] for p in ps}; c = cpu(); g = grupos(ps); ahora = time.time()
    est = json.load(open(EST)) if os.path.exists(EST) else {"muestras": {}, "relanzados": 0}
    est.setdefault("muestras", {}); est.setdefault("relanzados", 0)
    previa = {int(k): v for k, v in est.get("cpu", {}).items()}; nuevas = {}; colgados = []
    log_render = os.path.getmtime(f"{T}/render_todo.log") if os.path.exists(f"{T}/render_todo.log") else 0
    for r, pids in g.items():
        # ACTIVIDAD = CPU gastada desde la pasada anterior, proceso a proceso (un proceso nuevo cuenta entero). NO la suma
        # del grupo: el render lanza un ffmpeg por tramo y, al acabar uno y empezar otro, la suma BAJA aunque avance
        # (2026-11-17, alimentacion: el vigilante cerró el render bueno en el tramo 46 por eso).
        gasto = sum(max(0.0, c.get(p, 0) - previa[p]) if p in previa else c.get(p, 0) for p in pids)
        es_render = any(RENDER.search(cmd.get(p, "")) for p in pids)
        if es_render and ahora - log_render < COLGADO: gasto = max(gasto, 99)    # el registro del render se mueve: avanza
        clave = f"{r}|{cmd.get(r, '')[:120]}"; m = est["muestras"].get(clave)
        quieto = gasto < 2
        nuevas[clave] = m if (m and quieto) else [0, ahora]                     # desde cuándo NO gasta CPU
        if m and quieto and ahora - m[1] >= COLGADO: colgados.append((r, pids, (ahora - m[1]) / 60))
    est["muestras"] = nuevas; est["cpu"] = {str(p): c.get(p, 0) for pids in g.values() for p in pids}
    render_vivo = any(RENDER.search(cmd.get(p, "")) for pids in g.values() for p in pids)
    if actuar:
        for r, pids, mins in colgados:
            log(f"COLGADO: «{cmd.get(r, '')[:110]}» ({len(pids)} procesos) sin gastar CPU desde hace {mins:.0f} min -> cerrado")
            cerrar(pids); render_vivo = render_vivo and not any(RENDER.search(cmd.get(p, "")) for p in pids)
        # memoria: navegadores de Remotion y servicios de esbuild huérfanos (su padre ya no existe) si nadie está pintando
        pintando = any(re.search(r"remotion (render|still|bundle)", cmd.get(p, "")) for pids in g.values() for p in pids)
        huerf = [p[0] for p in ps if (p[1].startswith("chrome-headless-shell") and "remotion" in p[2].lower() or "esbuild" in p[2] and "--service" in p[2])
                 and (p[3] in (0, 1) or p[3] not in cmd)]
        if huerf and not pintando: cerrar(huerf); log(f"MEMORIA: cerrados {len(huerf)} navegadores/esbuild huérfanos")
        libre, total = memoria()
        if WIN and libre < max(3.0, total * 0.2):
            n = recortar([pid for pid, nom, _, _ in ps if nom not in NO and not nom.startswith("chrome-headless-shell") and pid not in (0, 4, os.getpid())]); log(f"MEMORIA: {libre:.1f} GB libres: recortados {n} procesos")
        # render pedido que ya no corre: se relanza
        if os.path.exists(PED) and not render_vivo:
            ped = json.load(open(PED)); sal = ped["salida"]
            if os.path.exists(sal): os.remove(PED)
            elif est["relanzados"] < 3:
                est["relanzados"] += 1; py = ped.get("py", sys.executable)
                subprocess.Popen([py, f"{AQUI}/render_todo.py", *ped["args"]], stdout=open(f"{T}/render_todo.log", "a"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=not WIN)
                log(f"RENDER parado sin terminar -> relanzado ({est['relanzados']}/3): render_todo.py {' '.join(ped['args'])}")
            elif est["relanzados"] == 3: est["relanzados"] += 1; log("RENDER: ya se ha relanzado 3 veces y vuelve a pararse: mira el final de trabajo/render_todo.log")
    if actuar: est["ultima"] = ahora; json.dump(est, open(EST, "w"))
    return g, cmd, colgados


if __name__ == "__main__":
    if not os.path.isdir(T): raise SystemExit("Ejecuta desde out/<slug>/ (no hay trabajo/)")
    if args[:1] == ["parar"]: open(STOP, "w").write("1"); print("El vigilante se para en su próxima pasada."); sys.exit()
    if args[:1] == ["estado"]:
        g, cmd, colg = pasada(actuar=False); libre, total = memoria()
        print(f"MEMORIA: {libre:.1f} GB libres de {total:.1f}")
        for r, pids in g.items(): print(f"EN MARCHA: «{cmd.get(r, '')[:110]}» ({len(pids)} procesos)")
        if not g: print("NADA EN MARCHA de la edición")
        rv = any(RENDER.search(cmd.get(p, "")) for pids in g.values() for p in pids)
        if os.path.exists(PED): print(f"RENDER: {'EN MARCHA' if rv else 'PARADO (el vigilante lo relanza en su pasada)'} ({tramos()}) -> {json.load(open(PED))['salida']}")
        else: print("RENDER: TERMINADO o sin render pedido" + (" (pero hay procesos de render vivos)" if rv else ""))
        for r, _, mins in colg: print(f"POSIBLE COLGADO: «{cmd.get(r, '')[:110]}» sin CPU desde hace {mins:.0f} min (el vigilante lo cerrará en su pasada)")
        est = json.load(open(EST)) if os.path.exists(EST) else {}
        vivo = est.get("ultima") and time.time() - est["ultima"] < CADA * 1.6
        if os.path.exists(LOG) and open(LOG, encoding="utf-8").read().rstrip().endswith("vigilante parado"): vivo = False
        print("VIGILANTE: " + ("en marcha" if vivo else "NO está en marcha: lánzalo en segundo plano (vigilante.py)"))
        if os.path.exists(LOG): print("Últimas acciones:\n" + "".join(open(LOG, encoding="utf-8").readlines()[-6:]).rstrip())
        sys.exit()
    if os.path.exists(STOP): os.remove(STOP)
    log(f"vigilante en marcha (cada {CADA / 60:.0f} min; colgado = {COLGADO / 60:.0f} min sin CPU)")
    t0 = time.time()
    while not os.path.exists(STOP) and time.time() - t0 < 16 * 3600:
        try: pasada()
        except Exception as e: log(f"error en la pasada: {e}")
        for _ in range(int(CADA // 5)):
            if os.path.exists(STOP): break
            time.sleep(5)
    if os.path.exists(STOP): os.remove(STOP)
    log("vigilante parado")
