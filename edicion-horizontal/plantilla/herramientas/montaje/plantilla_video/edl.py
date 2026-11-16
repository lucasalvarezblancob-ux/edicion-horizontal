# EDL del vídeo "__SLUG__": la lista de decisiones de montaje, de arriba abajo, en el orden en que sale.
# Se escribe LEYENDO las transcripciones (bruto/__SLUG__-analisis/transcripcion/<clip>.txt) y el registro visual
# (…/visual/<clip>.json). Qué es cada pieza: herramientas/montaje/edl_base.py. Ejemplo completo: skill → base/ejemplos/ramon/edl.py.
#
#   T(clip, pista, "texto literal de la transcripción", gap=0.75, tag=None)   habla, elegida por su TEXTO (erratas incluidas)
#   V(clip, t0, t1, vol=1.0, tag=None, speed=1.0)                             plano con su sonido (segundos del bruto)
#   S(n, "TÍTULO DEL CAPÍTULO", "línea pequeña")                              capítulo n (rótulo n/total y marca "s<n>")
#   X("marca")                                                                marca sin duración
#
# Estructura que funciona (skill → base/intros.md):
#   X("trailer")  recap de 15-25 s: las 4-6 mejores frases del propio vídeo, una idea por plano
#   ráfaga        3-5 planos V de ~0,6 s (la primera lleva tag="rafaga")
#   X("titulo")   + un plano V de 4 s como fondo del título (tag="titulo_fondo")
#   X("cuerpo")   arranque y capítulos S(1…n)
#   X("cierre")   despedida corta con el único CTA
from edl_base import S, T, V, X

A = "C0001"   # un nombre corto por clip ahorra escribir

EDL = [
    # ---------- TRÁILER EN FRÍO ----------
    X("trailer"),
    # T(A, 0, "la mejor frase del vídeo", tag="tr1"),
    # V(A, 12.0, 12.6, vol=0.5, tag="rafaga"), V(A, 40.0, 40.6, vol=0.5), V(A, 71.2, 71.8, vol=0.5),
    X("titulo"),
    # V(A, 100.0, 104.0, vol=0.5, tag="titulo_fondo"),
    # ---------- CUERPO ----------
    X("cuerpo"),
    # S(1, "PRIMER CAPÍTULO", "línea pequeña"),
    # T(A, 20, "frase tal cual sale en la transcripción"),
    X("cierre"),
    # T(A, 900, "y esto es todo por hoy"),
]
