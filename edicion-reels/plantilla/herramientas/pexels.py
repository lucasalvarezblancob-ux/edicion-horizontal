"""Clips libres de Pexels (verticales) para tapar huecos de b-roll: frases sobre algo que el creador no tiene grabado,
o una carpeta recién instalada con recursos/ vacío. Licencia de Pexels: uso libre, sin atribución obligatoria.

Uso (desde la carpeta de edición):
  python3 -I herramientas/pexels.py buscar "bodybuilder posing stage" [--n 10] [--miniaturas DIR] [--horizontal]
      Lista resultados (id, duración, resolución, autor, página). Con --miniaturas guarda la portada de cada uno
      (pexels_<id>.jpg) para mirarlas antes de bajar: comprueba que enseña lo que dice la frase (especie, ejercicio…).
  python3 -I herramientas/pexels.py bajar ID SALIDA.mp4
      Baja el mejor archivo de ese vídeo (vertical, la máxima resolución hasta 2160×3840).
Busca en inglés: da muchos más resultados.

Necesita PEXELS_API_KEY (gratis en https://www.pexels.com/api/) en el entorno o en estudio/.env.local. Sin clave sale
con código 2 y explica el método del navegador (base/preferencias.md → Recursos, 2026-11-05).
Solo usa la biblioteca estándar de Python: no depende de la .venv.
"""
import argparse, json, os, sys, urllib.error, urllib.parse, urllib.request

API = "https://api.pexels.com/videos"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) edicion-reels"}
AQUI = os.path.dirname(os.path.abspath(__file__))


def clave():
    if os.environ.get("PEXELS_API_KEY", "").strip():
        return os.environ["PEXELS_API_KEY"].strip()
    for env in (os.path.join(AQUI, "..", "estudio", ".env.local"), os.path.join(os.getcwd(), "estudio", ".env.local")):
        try:
            for linea in open(env, encoding="utf-8"):
                k, _, v = linea.strip().partition("=")
                if k.strip() == "PEXELS_API_KEY" and v.strip().strip("'\""):
                    return v.strip().strip("'\"")
        except OSError:
            pass
    return None


def sin_clave():
    sys.stderr.write(
        "No hay PEXELS_API_KEY (ni en el entorno ni en estudio/.env.local).\n"
        "  · Con clave (gratis, https://www.pexels.com/api/): añade la línea PEXELS_API_KEY=… a estudio/.env.local.\n"
        "  · Sin clave: busca en el navegador https://www.pexels.com/search/videos/<búsqueda>/?orientation=portrait,\n"
        "    abre el vídeo, saca de su página la URL del CDN videos.pexels.com/video-files/<id>/…_2160_3840_….mp4\n"
        "    (la de SU id) y bájala con curl. pexels.com/download/video/<id>/ da 403 con curl.\n")
    sys.exit(2)


def pedir(url, k):
    req = urllib.request.Request(url, headers={**UA, "Authorization": k})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            sys.exit(f"Pexels rechaza la clave (HTTP {e.code}): revisa PEXELS_API_KEY en estudio/.env.local.")
        if e.code == 429:
            sys.exit("Pexels: límite de peticiones alcanzado (200/h, 20.000/mes). Espera o usa el método del navegador.")
        sys.exit(f"Pexels: HTTP {e.code} en {url}")
    except urllib.error.URLError as e:
        sys.exit(f"Sin conexión con Pexels: {e.reason}")


def descargar(url, destino):
    os.makedirs(os.path.dirname(os.path.abspath(destino)) or ".", exist_ok=True)
    tmp = destino + ".part"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(tmp, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            f.write(b)
    os.replace(tmp, destino)


def mejor_archivo(v, vertical=True):
    """El mp4 de mayor resolución que no pase de 2160×3840 (en la orientación pedida si la hay)."""
    fs = [f for f in v.get("video_files", []) if f.get("link") and f.get("width") and f.get("height")
          and f.get("file_type", "video/mp4") == "video/mp4"]
    if not fs:
        return None
    misma = [f for f in fs if (f["height"] >= f["width"]) == vertical] or fs
    validos = [f for f in misma if max(f["width"], f["height"]) <= 3840] or misma
    return max(validos, key=lambda f: f["width"] * f["height"])


def main():
    ap = argparse.ArgumentParser(description="Clips libres de Pexels")
    sub = ap.add_subparsers(dest="orden", required=True)
    b = sub.add_parser("buscar"); b.add_argument("consulta"); b.add_argument("--n", type=int, default=10)
    b.add_argument("--miniaturas"); b.add_argument("--horizontal", action="store_true")
    d = sub.add_parser("bajar"); d.add_argument("id"); d.add_argument("salida")
    a = ap.parse_args()
    k = clave() or sin_clave()

    if a.orden == "buscar":
        q = urllib.parse.urlencode({"query": a.consulta, "per_page": max(1, min(a.n, 80)),
                                    "orientation": "landscape" if a.horizontal else "portrait"})
        vs = pedir(f"{API}/search?{q}", k).get("videos", [])
        if not vs:
            print("Sin resultados: prueba otra búsqueda (en inglés, más general)."); return
        for v in vs:
            f = mejor_archivo(v, not a.horizontal)
            res = f"{f['width']}×{f['height']}" if f else "—"
            print(f"{v['id']:>10}  {v.get('duration', 0):>3} s  {res:>10}  {v.get('user', {}).get('name', '')[:24]:<24}  {v.get('url', '')}")
            if a.miniaturas and v.get("image"):
                try:
                    descargar(v["image"], os.path.join(a.miniaturas, f"pexels_{v['id']}.jpg"))
                except Exception as e:
                    print(f"            (no se pudo bajar la portada: {e})")
        if a.miniaturas:
            print(f"Portadas en {a.miniaturas}/ — míralas antes de bajar.")
    else:
        v = pedir(f"{API}/videos/{urllib.parse.quote(a.id)}", k)
        f = mejor_archivo(v, True)
        if not f:
            sys.exit(f"El vídeo {a.id} no tiene archivos mp4 descargables.")
        descargar(f["link"], a.salida)
        print(f"✓ {a.salida}  ({f['width']}×{f['height']}, {v.get('duration', '?')} s, de {v.get('user', {}).get('name', '?')}, {v.get('url', '')})")
        if max(f["width"], f["height"]) < 3840:
            print("  Menos de 2160×3840: escálalo con lanczos + unsharp (preferencias → Recursos).")


if __name__ == "__main__":
    main()
