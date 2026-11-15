# Ajustes PERSONALES de la base de edición (LOCAL: no sale de tu ordenador y la skill no lo pisa al actualizarse).
#
# La skill trae unas bases de edición y efectos iguales para todos (los números de herramientas/montaje/).
# Aquí cambias esas bases A TU GUSTO para TODOS tus vídeos, sin tocar la skill ni las herramientas.
# Orden (lo de la derecha manda):   estándar de la skill  <  este archivo  <  plan.py de cada vídeo
#
# Todo va comentado = estándar. Quita el "#" de lo que quieras cambiar. Si no sabes qué número poner, díselo a Claude
# con tus palabras ("zooms más suaves", "menos efectos", "la música más baja") y lo apunta aquí por ti.

# ---------- Ritmo y zooms (dinamica.py) ----------
# Escalas por las que va alternando el plano a cámara en cada corte de escala (1.0 = plano entero).
# Más suave: [1.0, 1.15, 1.0, 1.25, 1.1]      Más agresivo: [1.0, 1.4, 1.0, 1.6, 1.2, 1.0, 1.5]
# ESCALAS = [1.0, 1.3, 1.0, 1.45, 1.15, 1.0, 1.35, 1.12, 1.5, 1.0, 1.25]

# Segundos (mínimo, máximo) entre un cambio de escala y el siguiente mientras hablas. Más alto = más calmado.
# CAMBIO_CADA = (2.48, 4.48)

# Escala del golpe de zoom en las frases fuertes.
# Z_FUERTE = 1.65

# Altura a la que queda la cara en un zoom (0 = arriba, 1 = abajo).
# CARA_Y = 0.38

# ---------- Efectos de sonido (paso5_audio.py) ----------
# Sonido y volumen de cada tipo de gráfico. Solo pon los que cambies; None = ese gráfico va sin sonido.
# Sonidos disponibles: estudio/public/sonidos/ (los tuyos, en personal/<creador>/recursos/sonidos/ y copiados ahí).
# Tipos: titulo, seccion, trk (rótulo con seguimiento), mapa, suscribe, dato, golpe.
# SFX = {"dato": None, "seccion": ("whoosh-short", 0.15)}

# ---------- Música y volumen final (paso5_audio.py, paso6_musica.py) ----------
# dB de la música en cada momento (sobre la pista normalizada). Más negativo = más baja. Solo pon los que cambies.
# Estándar: BASE -24 (bajo la voz), TRAILER -16, TITULO -6, SECCION -15, MAPA -19, SINVOZ -13, CIERRE -20.
# MUSICA_NIVELES = {"BASE": -26.0}
# Segundos máximos sin voz y sin música (estándar 1,0): un respiro más largo donde no se habla se rellena solo.
# MUSICA_HUECO_MAX = 1.0
# Si este creador lleva música en casi todo el vídeo (no «solo donde toca»), eso no es un número: se apunta en su
# preferencias.md y se hace con una ventana por capítulo en el plan.py de cada vídeo. Aquí, solo el nivel bajo la voz.

# Sonoridad final del vídeo en LUFS (YouTube normaliza a -14).
# LUFS = -14
