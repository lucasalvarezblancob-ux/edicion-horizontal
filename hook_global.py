"""Añade a ~/.claude/settings.json el hook que, al abrir Claude Code en cualquier carpeta, pone al día las Skills de
Reino Selva e instala las nuevas (sincronizar.sh; como mucho cada 6 h). Si ya está, no hace nada. Lo lanza el instalador.
    python hook_global.py <ruta del repo>"""
import json, os, sys

repo = os.path.abspath(sys.argv[1]).replace("\\", "/")
cmd = f'bash "{repo}/sincronizar.sh"'
base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.environ.get("HOME") or os.path.expanduser("~"), ".claude")
ruta = os.path.join(base, "settings.json")
os.makedirs(os.path.dirname(ruta), exist_ok=True)
cfg = {}
if os.path.exists(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read().strip()
    if texto:
        cfg = json.loads(texto)
inicio = cfg.setdefault("hooks", {}).setdefault("SessionStart", [])
if any("sincronizar.sh" in h.get("command", "") and "publiqo-edicion" in h.get("command", "")
       for g in inicio for h in g.get("hooks", [])):
    print("Hook de actualización automática: ya estaba.")
    sys.exit()
inicio.append({"matcher": "startup", "hooks": [{"type": "command", "command": cmd, "timeout": 60}]})
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("Hook de actualización automática: añadido a ~/.claude/settings.json")
