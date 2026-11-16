"""capitulos.py: imprime los capítulos del vídeo con sus tiempos, listos para pegar en la descripción de YouTube.
Salen de las marcas S(n, ...) del EDL ya alineado (trabajo/linea.json): el minuto es el del vídeo final, no el del bruto.
YouTube exige que el primero sea 0:00, al menos 3 capítulos y 10 s como mínimo cada uno (avisa si no se cumple).
Los títulos salen en MAYÚSCULAS como en el rótulo: escríbelos en la descripción como frase normal, en el idioma del vídeo."""
import json
from comun import FPS, TRABAJO

L = json.load(open(f"{TRABAJO}/linea.json", encoding="utf-8"))
caps = [(0, "Intro")] + [(s["o"], s["titulo"].capitalize()) for s in L["secciones"]]
if "cierre" in L["marcas"]: caps.append((L["marcas"]["cierre"], "Cierre"))
for i, (f, t) in enumerate(caps):
    s = f // FPS; fin = caps[i + 1][0] if i + 1 < len(caps) else L["total"]
    print(f"{s // 60}:{s % 60:02d} {t}" + ("    <- dura menos de 10 s: únelo al anterior" if (fin - f) / FPS < 10 else ""))
if len(caps) < 3: print("(menos de 3 capítulos: YouTube no los mostrará)")
