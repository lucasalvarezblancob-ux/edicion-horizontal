"""mover_recursos.py [CREADOR] [--simular]: pasa la carpeta recursos/ de la raíz a personal/<creador>/recursos/.

Los recursos son de cada creador (su intro y sus logos, pero también sus clips de archivo, b-roll, fotos, mapas y música):
ya no hay recursos/ en la raíz de la carpeta de edición. Se lanza desde la raíz, una vez. No borra ni pisa nada: lo que ya
exista en el destino se queda donde está y se lista (salvo el índice y el catálogo vacíos de la plantilla, que se
sustituyen por los tuyos). Si hay varios creadores, di de cuál es el material; el de los demás se reparte luego a mano."""
import filecmp, os, shutil, sys

args = [a for a in sys.argv[1:] if a != "--simular"]; SIM = "--simular" in sys.argv
if not os.path.isdir("personal"): raise SystemExit("Lánzalo desde la raíz de la carpeta de edición (falta personal/)")
if not os.path.isdir("recursos"): raise SystemExit("No hay recursos/ en la raíz: nada que mover.")
cre = sorted(d for d in os.listdir("personal") if os.path.isdir(f"personal/{d}") and not d.startswith(("_", ".")))
c = args[0] if args else (cre[0] if len(cre) == 1 else None)
if c is None: raise SystemExit(f"Di de qué creador es el material: mover_recursos.py <creador>   (hay: {', '.join(cre) or 'ninguno; créalo con nuevo_creador.py'})")
if c not in cre: raise SystemExit(f"No existe personal/{c}/ (créalo con herramientas/montaje/nuevo_creador.py {c})")
dst = f"personal/{c}/recursos"; movidos, quedan = 0, []
for raiz, _, fs in os.walk("recursos"):
    raiz = raiz.replace("\\", "/"); rel = raiz[len("recursos"):]
    for f in sorted(fs):
        o, d, t = f"{raiz}/{f}", f"{dst}{rel}/{f}", f"personal/_plantilla/recursos{rel}/{f}"
        if f in (".gitkeep", ".DS_Store"):
            if not SIM: os.remove(o)
            continue
        if os.path.exists(d) and not (os.path.exists(t) and filecmp.cmp(d, t, shallow=False)): quedan.append(o); continue
        print(("mover  " if not SIM else "movería  ") + f"{o}  ->  {d}"); movidos += 1
        if not SIM: os.makedirs(os.path.dirname(d), exist_ok=True); os.replace(o, d) if os.path.exists(d) else shutil.move(o, d)
if not SIM:
    for raiz, ds, fs in os.walk("recursos", topdown=False):      # las carpetas que se han quedado vacías
        if os.path.isdir(raiz) and not os.listdir(raiz):
            if raiz != "recursos": os.makedirs(dst + raiz.replace("\\", "/")[len("recursos"):], exist_ok=True)
            os.rmdir(raiz)
print(f"\n{movidos} archivos {'se moverían' if SIM else 'movidos'} a {dst}/")
if quedan: print("Ya existían en el destino y NO se han tocado (compáralos y decide):", *quedan, sep="\n  ")
elif not SIM: print("recursos/ de la raíz ya no existe. Repasa las rutas de personal/%s/recursos/INDICE.md y de recursos.md." % c)
