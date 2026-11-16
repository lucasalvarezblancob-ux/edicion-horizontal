#!/usr/bin/env python3
"""Libera espacio: borra la carpeta entera estudio/public/<slug>/ (proxies, clips, voz, música, audio, LUTs…)
de los edits cuyo render en out/ tiene más de N días (30 por defecto). Si Lucas ha borrado el render de out/, cuenta
igual: N días desde que el script vio por primera vez que ya no estaba (fecha guardada en herramientas/limpieza-estado.json).

NUNCA toca nada fuera de estudio/public/<slug>/: se quedan el código (estudio/src/videos/<slug>/), los renders de
out/, recursos/, bruto terminado/, refs/ y la skill. Para volver a renderizar un edit limpiado hay que rehacer sus
archivos (proxies con herramientas/proxy.sh desde recursos/ o bruto terminado/, voz, música…), y las rutas están
en el comentario de cada composición.

Salta un edit si hay algo tocado en los últimos N días en public/<slug>/ o en src/videos/<slug>/ (se está trabajando en él). Lo borrado se apunta en herramientas/limpieza.log.

Uso: limpiar_renders.py [--dias 30] [--simular]
Lo lanza solo el hook SessionStart de .claude/settings.json.
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

    slugs = sorted(d.name for d in PUBLIC.iterdir() if d.is_dir() and d.name not in NO_SON_EDITS)

    # render más reciente de cada slug: out/**/AAAA-MM-DD_<slug>[_-…].mp4, asignado al slug más largo que encaje
    render: dict[str, float] = {}
    for f in OUT.rglob("*.mp4"):
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
        if max(ultimo_cambio(PUBLIC / s), ultimo_cambio(VIDEOS / s)) > limite:
            continue
        carpeta = PUBLIC / s
        # seguridad: solo una carpeta real directamente dentro de estudio/public/
        if carpeta.is_symlink() or carpeta.resolve().parent != PUBLIC.resolve():
            continue
        archivos = [p for p in carpeta.rglob("*") if p.is_file() and not p.is_symlink()]
        tam = sum(p.stat().st_size for p in archivos)
        if not a.simular:
            shutil.rmtree(carpeta)
        borrados.append((s, len(archivos), tam, ref[s], s in render))

    if not borrados:
        return 0
    total = sum(b[2] for b in borrados)
    verbo = "Borraría" if a.simular else "Borrados"
    lineas = [
        f"- estudio/public/{s}/: {n} archivos, {t / 1e9:.2f} GB ("
        + ("render del " if hay else "render borrado de out/, visto sin él desde el ")
        + f"{dt.date.fromtimestamp(r).isoformat()})"
        for s, n, t, r, hay in borrados
    ]
    resumen = f"{verbo} las carpetas de edits con render de hace más de {a.dias:g} días ({total / 1e9:.2f} GB):\n" + "\n".join(lineas)
    print(resumen)
    if not a.simular:
        with open(LOG, "a") as log:
            log.write(f"## {dt.datetime.now():%Y-%m-%d %H:%M}\n{resumen}\n\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
