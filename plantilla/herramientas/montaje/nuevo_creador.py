"""nuevo_creador.py NOMBRE: crea la personalización de un creador. Se lanza desde la raíz de la carpeta de edición.

Lo normal es UN creador por carpeta; si editas para varios, cada uno tiene la suya dentro de personal/:
  personal/<nombre>/           perfil.md, preferencias.md, recursos.md, marca.json, ajustes.py (copiados de personal/_plantilla/)
  personal/<nombre>/recursos/  TODO su material (no hay recursos/ en la raíz), ordenado por carpetas: marca/ (sus fijos
                               ORIGINALES: intro, outro, logos, mascota, cortinillas), una carpeta por tema para sus clips
                               de archivo y b-roll (se crean según su nicho), creador/, fotos/, mapas/, sonidos/ y
                               musica/ (+ CATALOGO.md); la ficha de cada archivo, en INDICE.md
  personal/<nombre>/refs/      vídeos suyos de ejemplo y sus fichas (cómo edita él)
  estudio/src/personal/<nombre>/Graficos.tsx      sus gráficos propios (Remotion): función `propios`
  estudio/public/personal/<nombre>/               sus recursos ya preparados para superponer (.webm con transparencia, .png)
No pisa nada que exista. El vídeo elige creador con CREADOR = "<nombre>" en out/<slug>/proyecto.py (si solo hay uno, es ese)."""
import os, re, shutil, sys

if len(sys.argv) != 2: raise SystemExit(__doc__)
n = sys.argv[1]
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n): raise SystemExit("NOMBRE en minúsculas, sin espacios: reinoselva, mi-canal")
if not os.path.isdir("personal/_plantilla") or not os.path.isdir("estudio/src"): raise SystemExit("Lánzalo desde la raíz de la carpeta de edición (falta personal/_plantilla o estudio/src)")
d = f"personal/{n}"
for sub in ("", "/recursos", "/refs"): os.makedirs(d + sub, exist_ok=True)
for raiz, _, fs in os.walk("personal/_plantilla"):       # los archivos vacíos y recursos/ con su índice, su catálogo y sus carpetas
    dst = d + raiz.replace("\\", "/")[len("personal/_plantilla"):]; os.makedirs(dst, exist_ok=True)
    for f in sorted(fs):
        if f != ".gitkeep" and not os.path.exists(f"{dst}/{f}"): shutil.copy(f"{raiz}/{f}", f"{dst}/{f}"); print("+", f"{dst}/{f}")
os.makedirs(f"estudio/public/personal/{n}", exist_ok=True); g = f"estudio/src/personal/{n}/Graficos.tsx"
if not os.path.exists(g):
    os.makedirs(os.path.dirname(g), exist_ok=True)
    open(g, "w", encoding="utf-8", newline="\n").write(f'''import React from "react";
import {{ Item }} from "../../comun/Graficos";

// Gráficos PROPIOS de {n} (LOCAL: la skill no los pisa). Cada tipo que pongas en PROPIOS de plan.py
// ([(ancla, segundos, "tipo", {{datos}})]) se pinta aquí. Sus archivos, en estudio/public/personal/{n}/.
// Qué es cada uno y cuándo se usa: personal/{n}/recursos.md.
export const propios = (it: Item, f: number, dur: number): React.ReactNode | undefined => {{
  // if (it.t === "cabecera") return <Cabecera it={{it}} f={{f}} dur={{dur}} />;
  void it; void f; void dur;
  return undefined;
}};
''')
    print("+", g)
print(f"\nCreador «{n}» listo. Rellena con él {d}/perfil.md y {d}/marca.json; sus reglas van a {d}/preferencias.md.")
print(f"Sus recursos van en {d}/recursos/, por carpetas: crea las de tema de su nicho y apúntalas en su INDICE.md (base/recursos.md § 2).")
