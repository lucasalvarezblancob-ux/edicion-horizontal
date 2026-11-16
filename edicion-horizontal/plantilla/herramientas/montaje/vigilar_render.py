"""vigilar_render.py [SALIDA.mp4] [--siempre]: UNA pasada de vigilancia mientras dura un render largo. Hace dos cosas:

1. LIBERA MEMORIA sin tocar el render ni cerrar nada del usuario:
   - cierra los navegadores sin cabeza de Remotion que se hayan quedado colgados (solo si no hay ningún render de capas
     vivo; nunca un navegador del usuario);
   - en Windows, si queda poca memoria libre (menos de 3 GB o del 20 %; con --siempre, siempre), pide al sistema que
     recorte la memoria de trabajo de los procesos que NO son del render: no se cierra nada, lo que no están usando pasa
     a la lista de espera o al archivo de paginación y vuelve solo cuando lo necesitan. Nunca se toca ffmpeg, python,
     node, el navegador de Remotion, la terminal ni Claude;
   - en macOS y Linux no se recorta nada: el sistema ya comprime la memoria solo, y `purge` pide contraseña de
     administrador y vacía la caché de disco que el render está usando. Solo se cierran los navegadores colgados.
2. DICE CÓMO VA EL RENDER (última línea):  RENDER: EN MARCHA | PARADO | TERMINADO | SIN RENDER.
   PARADO = no hay ningún proceso de render vivo y SALIDA no existe: se ha muerto (casi siempre, por memoria).
   Se relanza con  render_todo.py SALIDA  (retoma donde se quedó; no repite capas ni tramos ya hechos).

Uso, desde out/<slug>/, cada 5-10 minutos mientras dure el render (SKILL.md § 2, paso 6: con un cron de la sesión):
  vigilar_render.py ../AAAA-MM-DD_<slug>.mp4
No cambia nada del montaje ni del resultado: el render sale idéntico con vigilancia o sin ella.
macOS: escrito con las órdenes de serie (vm_stat, ps), SIN PROBAR por Lucas."""
import glob, json, os, re, signal, subprocess, sys, time

WIN = os.name == "nt"
RENDER = re.compile(r"paso4_render|paso5_audio|paso6_musica|render_todo")
# procesos que nunca se recortan: el render, sus herramientas, la terminal y el propio Claude
NO = {"ffmpeg", "ffprobe", "python", "pythonw", "node", "npx", "bash", "sh", "zsh", "cmd", "conhost", "powershell", "pwsh", "mintty", "git-bash",
      "windowsterminal", "openconsole", "claude", "system", "idle", "registry", "memory compression", "secure system"}
UMBRAL_GB, UMBRAL_PARTE = 3.0, 0.20


def memoria():
    """(libre, total) en GB. Libre = lo que el sistema puede dar ya sin paginar."""
    if WIN:
        import ctypes
        class M(ctypes.Structure):
            _fields_ = [("n", ctypes.c_ulong), ("carga", ctypes.c_ulong), ("total", ctypes.c_ulonglong), ("libre", ctypes.c_ulonglong), ("tp", ctypes.c_ulonglong),
                        ("lp", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("lv", ctypes.c_ulonglong), ("ex", ctypes.c_ulonglong)]
        m = M(); m.n = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); return m.libre / 2**30, m.total / 2**30
    if sys.platform == "darwin":
        v = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout; pag = int(re.search(r"page size of (\d+)", v).group(1))
        n = lambda k: int(m.group(1)) if (m := re.search(rf"{k}:\s+(\d+)", v)) else 0
        total = int(subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True).stdout)
        return (n("Pages free") + n("Pages inactive") + n("Pages speculative") + n("Pages purgeable")) * pag / 2**30, total / 2**30
    d = dict(l.split(":") for l in open("/proc/meminfo")); kb = lambda k: int(d[k].split()[0])
    return kb("MemAvailable") / 2**20, kb("MemTotal") / 2**20


def procesos():
    """[(pid, nombre sin extensión en minúsculas, línea de órdenes, pid del padre)] de todo lo que el usuario puede ver."""
    if WIN:
        ps = "[Console]::OutputEncoding=[Text.Encoding]::UTF8; Get-CimInstance Win32_Process | Select-Object ProcessId,Name,CommandLine,ParentProcessId | ConvertTo-Json -Compress"
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        try: lista = json.loads(r)
        except ValueError: return []
        return [(p["ProcessId"], os.path.splitext(p["Name"] or "")[0].lower(), p["CommandLine"] or "", p.get("ParentProcessId") or 0) for p in (lista if isinstance(lista, list) else [lista])]
    out = []
    for l in subprocess.run(["ps", "-axo", "pid=,ppid=,args="], capture_output=True, text=True, errors="replace").stdout.splitlines():
        c = l.split(None, 2)
        if len(c) == 3 and c[0].isdigit(): out.append((int(c[0]), os.path.basename(c[2].split(" ")[0]).lower(), c[2], int(c[1])))
    return out


def recortar(pids):
    """Windows: pide al sistema que recorte la memoria de trabajo de esos procesos. Devuelve cuántos ha podido."""
    import ctypes
    from ctypes import wintypes
    k, ps = ctypes.windll.kernel32, ctypes.windll.psapi
    k.OpenProcess.restype = wintypes.HANDLE; k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    ps.EmptyWorkingSet.argtypes = [wintypes.HANDLE]; k.CloseHandle.argtypes = [wintypes.HANDLE]; n = 0
    for pid in pids:
        h = k.OpenProcess(0x0100 | 0x1000, False, pid)      # PROCESS_SET_QUOTA | PROCESS_QUERY_LIMITED_INFORMATION
        if not h: continue                                   # de otro usuario o del sistema: se deja
        n += bool(ps.EmptyWorkingSet(h)); k.CloseHandle(h)
    return n


def render_vivo(ps=None):
    """Procesos de render vivos, sin contar este ni sus padres (en Windows el python de la venv es un lanzador: hay dos con
    la misma línea de órdenes)."""
    ps = procesos() if ps is None else ps; padre = {p[0]: p[3] for p in ps}; mios = set(); x = os.getpid()
    while x and x not in mios: mios.add(x); x = padre.get(x, 0)
    return [p for p in ps if p[0] not in mios and RENDER.search(p[2]) and "vigilar_render" not in p[2]]


def tramos():
    try: total = len(json.load(open("trabajo/video.json"))["tramos"])
    except (OSError, ValueError, KeyError): return ""
    return f"tramos {len([f for f in glob.glob('trabajo/tramos/t*.mp4') if '.tmp' not in f])}/{total}"


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(errors="replace")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; salida = args[0] if args else None; siempre = "--siempre" in sys.argv
    libre0, total = memoria(); ps = procesos(); vivos = render_vivo(ps)
    # 1) navegadores sin cabeza de Remotion colgados: solo si nadie está pintando capas ni sacando un fotograma
    pintando = [p for p in ps if "remotion" in p[2].lower() and not p[1].startswith("chrome")]
    huerf = 0
    if not pintando:
        for pid, nom, cmd, _ in ps:
            if nom.startswith("chrome-headless-shell") and "remotion" in cmd.lower():
                try: os.kill(pid, signal.SIGTERM); huerf += 1
                except OSError: pass
    # 2) Windows: recortar lo que no es del render, solo si hace falta
    n = 0; hecho = "no hace falta: hay memoria de sobra"
    if WIN and (siempre or libre0 < max(UMBRAL_GB, total * UMBRAL_PARTE)):
        n = recortar([pid for pid, nom, cmd, _ in ps if nom not in NO and not nom.startswith("chrome-headless-shell") and pid not in (0, 4, os.getpid())])
        time.sleep(2); hecho = f"recortados {n} procesos"
    elif not WIN: hecho = "en este sistema no se recorta: lo gestiona él"
    libre1, _ = memoria()
    print(f"MEMORIA: {libre0:.1f} GB libres de {total:.1f} -> {libre1:.1f} GB ({hecho}; navegadores de Remotion colgados cerrados: {huerf})")
    if libre1 < 1.5 and vivos: print("AVISO: queda muy poca memoria. Si el render se para: render_todo.py lo retoma con menos navegadores a la vez; cierra programas que no uses.")
    # 3) estado del render
    t = tramos()
    if vivos: print(f"RENDER: EN MARCHA ({t}; procesos: {', '.join(sorted({re.search(RENDER, p[2]).group(0) for p in vivos}))})")
    elif salida and os.path.exists(salida): print(f"RENDER: TERMINADO ({salida}, {os.path.getsize(salida) / 2**30:.2f} GB) -> quita la vigilancia y comprueba el archivo")
    elif salida: print(f"RENDER: PARADO sin terminar ({t}) -> relánzalo: render_todo.py {salida}")
    else: print(f"RENDER: SIN RENDER en marcha ({t})")
