#!/usr/bin/env python3
"""Libera espacio: borra los INTERMEDIOS de los edits cuyo render en out/ tiene más de N días (30 por defecto):
  - out/<slug>/trabajo/        (audios, capas ProRes, tramos de vídeo, stills: lo que más pesa)
  - estudio/public/<slug>/     (mapas, fotos y audios copiados para ese vídeo)
  - estudio/build-<slug>/      (bundle de Remotion)
Si el creador ha borrado el render de out/, cuenta igual: N días desde que el script vio por primera vez que ya no estaba
(fecha guardada en herramientas/limpieza-estado.json).

NUNCA toca: el código del edit (out/<slug>/proyecto.py, edl.py, plan.py y estudio/src/videos/<slug>/: sirven de plantilla y
con ellos se rehace todo), los renders de out/, personal/ (con los recursos de cada creador), bruto/, bruto terminado/, refs/ ni la skill.
Para volver a renderizar un edit limpiado: relanza los pasos 1 a 6 desde out/<slug>/ (los brutos tienen que seguir donde
dice proyecto.py).

Salta un edit si se ha tocado algo suyo en los últimos N días. Lo borrado se apunta en herramientas/limpieza.log.

Uso: limpiar_renders.py [--dias 30] [--simular]
Lo lanza solo el hook SessionStart (comprobar.sh de la skill).
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PUBLIC = RAIZ / "estudio" / "public"
VIDEOS = RAIZ / "estudio" / "src" / "videos"
OUT = RAIZ / "out"
LOG = RAIZ / "herramientas" / "limpieza.log"
ESTADO = RAIZ / "herramientas" / "limpieza-estado.json"  # slug -> epoch en que se vio sin render
NO_SON_EDITS = {"sonidos"}  # carpetas compartidas de public/


def ultimo_cambio(carpeta: Path) -> float:
    m = 0.0
    if carpeta.exists():
        for p in carpeta.rglob("*"):
            if p.is_file() and p.name != ".DS_Store":
                m = max(m, p.stat().st_mtime)
    return m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=float, default=30)
    ap.add_argument("--simular", action="store_true", help="solo dice qué borraría")
    a = ap.parse_args()
    limite = time.time() - a.dias * 86400

    def carpetas(slug):   # lo que se borra de un edit
        return [PUBLIC / slug, OUT / slug / "trabajo", RAIZ / "estudio" / f"build-{slug}"]

    slugs = set()
    if PUBLIC.exists(): slugs |= {d.name for d in PUBLIC.iterdir() if d.is_dir() and d.name not in NO_SON_EDITS}
    if OUT.exists(): slugs |= {d.name for d in OUT.iterdir() if d.is_dir() and (d / "trabajo").is_dir()}
    slugs = sorted(slugs)

    # render más reciente de cada slug: out/**/AAAA-MM-DD_<slug>[_-…].mp4, asignado al slug más largo que encaje
    render: dict[str, float] = {}
    for f in OUT.rglob("*.mp4"):
        if "trabajo" in f.relative_to(OUT).parts:   # los tramos intermedios no son renders
            continue
        m = re.match(r"\d{4}-\d{2}-\d{2}_(.+)\.mp4$", f.name)
        if not m:
            continue
        nombre = m.group(1)
        cand = [s for s in slugs if nombre == s or nombre.startswith(s + "_") or nombre.startswith(s + "-")]
        if cand:
            s = max(cand, key=len)
            render[s] = max(render.get(s, 0), f.stat().st_mtime)

    # sin render en out/: la fecha de referencia es la primera vez que se vio así
    try:
        estado = json.loads(ESTADO.read_text())
    except (OSError, ValueError):
        estado = {}
    ahora = time.time()
    estado = {s: v for s, v in estado.items() if s in slugs and s not in render}
    for s in slugs:
        if s not in render:
            estado.setdefault(s, ahora)
    if not a.simular:
        ESTADO.write_text(json.dumps(estado, indent=1, sort_keys=True) + "\n")
    ref = {s: render.get(s, estado.get(s, ahora)) for s in slugs}

    borrados = []
    for s in slugs:
        if ref[s] > limite:
            continue
        codigo = [VIDEOS / s] + [p for p in (OUT / s).glob("*.py")] if (OUT / s).exists() else [VIDEOS / s]
        tocado = max([ultimo_cambio(c) for c in carpetas(s)] + [ultimo_cambio(c) if c.is_dir() else c.stat().st_mtime for c in codigo if c.exists()] + [0.0])
        if tocado > limite:
            continue
        n_arch, tam = 0, 0
        for carpeta in carpetas(s):
            # seguridad: solo carpetas reales dentro de la carpeta de edición, nunca enlaces
            if not carpeta.is_dir() or carpeta.is_symlink() or RAIZ.resolve() not in carpeta.resolve().parents:
                continue
            archivos = [p for p in carpeta.rglob("*") if p.is_file() and not p.is_symlink()]
            n_arch += len(archivos); tam += sum(p.stat().st_size for p in archivos)
            if not a.simular:
                shutil.rmtree(carpeta)
        if n_arch:
            borrados.append((s, n_arch, tam, ref[s], s in render))

    if not borrados:
        return 0
    total = sum(b[2] for b in borrados)
    verbo = "Borraría" if a.simular else "Borrados"
    lineas = [
        f"- {s} (out/{s}/trabajo, estudio/public/{s}, estudio/build-{s}): {n} archivos, {t / 1e9:.2f} GB ("
        + ("render del " if hay else "render borrado de out/, visto sin él desde el ")
        + f"{dt.date.fromtimestamp(r).isoformat()})"
        for s, n, t, r, hay in borrados
    ]
    resumen = f"{verbo} los intermedios de edits con render de hace más de {a.dias:g} días ({total / 1e9:.2f} GB):\n" + "\n".join(lineas)
    print(resumen)
    if not a.simular:
        with open(LOG, "a", encoding="utf-8") as log:
            log.write(f"## {dt.datetime.now():%Y-%m-%d %H:%M}\n{resumen}\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
