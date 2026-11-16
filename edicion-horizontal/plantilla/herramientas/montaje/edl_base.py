"""Piezas del EDL (lista de decisiones de montaje). El edl.py de cada vídeo hace `from edl_base import T, V, S, X` y
define EDL = [...] de arriba abajo, en el orden en que sale en el vídeo.

T = HABLA, elegida por su TEXTO LITERAL en la transcripción del bruto (no por tiempos: los tiempos de Whisper bailan
    ~0,2 s y hasta 0,8 s; el texto no). `pista` = índice aproximado de la primera palabra, solo para desempatar cuando
    la frase se repite. paso1_alinear.py afina luego el principio y el final con alineación forzada.
    gap = pausa (s) a partir de la cual la frase se parte en dos trozos y se quita el silencio de en medio.
V = PLANO con su sonido (tiempos del bruto en segundos): acción sin habla, ráfagas, fondo del título.
S = marca de SECCIÓN/capítulo (rótulo n/total + marca "s<n>").
X = marca sin duración ("trailer", "titulo", "cuerpo", "cierre"…), para colgar de ella música y gráficos.
tag = nombre de la pieza, para anclar cosas a ella con ("@tag", segundos)."""
from comun import norm, palabras

_w = {}


def T(clip, pista, texto, gap=0.75, tag=None):
    if clip not in _w: _w[clip] = [norm(x["p"]) for x in palabras(clip)]
    w = _w[clip]; q = [norm(x) for x in texto.split()]
    hits = [i for i in range(len(w) - len(q) + 1) if w[i:i + len(q)] == q]
    assert hits, f"no encuentro en {clip}: {texto!r} (cópialo tal cual de la transcripción, erratas incluidas)"
    a = min(hits, key=lambda i: abs(i - pista))
    return {"k": "T", "c": clip, "a": a, "b": a + len(q) - 1, "gap": gap, "tag": tag}


def V(clip, t0, t1, vol=1.0, tag=None, speed=1.0):
    return {"k": "V", "c": clip, "t0": t0, "t1": t1, "vol": vol, "tag": tag, "speed": speed}


def S(n, titulo, sub=""):
    return {"k": "S", "n": n, "titulo": titulo, "sub": sub}


def X(tag):
    return {"k": "X", "tag": tag}
