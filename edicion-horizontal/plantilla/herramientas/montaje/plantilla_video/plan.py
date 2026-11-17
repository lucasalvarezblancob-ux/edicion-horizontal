# Plan de imagen, textos y música del vídeo "__SLUG__". Lo leen paso3_plan.py, paso5_audio.py y paso6_musica.py.
# TODO es opcional: lo que no definas, no se pone. Ejemplo completo: skill → base/ejemplos/ramon/plan.py.
#
# ANCLAS: nada se coloca con un número de frame a mano; todo cuelga de lo que se dice o de una marca del EDL:
#   (clip, "frase literal", n)      frame en que empieza esa frase (n = 0 la primera vez que suena, -1 la última)
#   ((clip, "frase", n), segundos)  lo mismo, desplazado
#   ("@marca", segundos)            marca del EDL: tag de una pieza, X("…") o "s3" (capítulo 3)
#   "inicio" / "fin"
# TIMING: un texto se ancla a la PALABRA que escribe ("iberian pond"), no al principio de la frase ("it turned to be an
# iberian pond"); dura hasta que acaba la frase que resume y sale con el corte. Se mide con timing_textos.py después de
# paso3_plan.py (base/preferencias.md -> Timing de los textos).
# Coordenadas (cx, cy, cajas): píxeles del lienzo (ANCHO x ALTO de proyecto.py).
A = "C0001"

# ---- Planos de recurso sobre la voz: (ancla, clip origen, segundo origen, duración s | None = hasta el final de la pieza[, (zoom, cx, cy)])
# REGLA: se eligen del registro visual (mejores_recursos) y MIRANDO sus fotogramas (tira.py); después se revisan TODOS con
# hoja_recursos.py. Tiene que verse aquello de lo que se habla desde el primer fotograma: nada de paredes, barridos ni arranques.
# Si el sujeto queda pequeño, 5.º elemento (zoom, cx, cy) para cerrar sobre él. ("@tag", s) tapa un plano V conservando su sonido.
# (None, cx, cy): un recurso largo (> 3,2 s) hace su corte de escala x1,25 hacia ese punto (el sujeto), no al centro.
# Varios planos seguidos sobre una misma voz (tráiler-resumen: 1,5-2,5 s cada uno, un animal o momento distinto por plano):
#   ((A, "más de 100 animales", 0), [(B, 15.5, 2.0), (C, 768.0, 1.9, (1.6, 1900, 1200))])
# Nunca de la MISMA toma que la frase que tapa ni un trozo que ya sale: paso3 se para con REPETIDO (REPETIR_OK si es a propósito).
BROLL = [
    # ((A, "de lo que se habla", -1), A, 230.0, 2.6),
]

# ---- Rótulo anclado a un sujeto que se mueve: (clip, t0, t1 del bruto, [cx, cy, medio lado] de la caja inicial, "GRANDE", "pequeño", "izq"|"der")
# Con un 8.º elemento, ancla del frame de salida, el rótulo va sobre un plano de RECURSO (BROLL con zoom fijo) que enseña ese
# trozo de bruto: (clip, t0, t1, [cx, cy, medio lado], "GRANDE", "pequeño", "izq"|"der", ("@marca", s)).
TRK = []             # coordenadas: rejilla.py CLIP t (píxeles del lienzo). Varias cosas que se nombran: un TRK por cosa, cada uno en su segundo
DETALLE = set()      # rótulos de TRK ("GRANDE") tras los que se cierra x1,6 sobre el sujeto; solo si has comprobado que el seguimiento aguanta

# ---- Fails (se cae la cámara, se va la luz): blanco y negro y voz algo saturada hasta que se recupera. Con criterio: 1-2 por vídeo.
FALLOS = []          # [(ancla de inicio, ancla de fin)], p. ej. [(((A, "Uy", -1), -0.3), (A, "Hemos vuelto", -1))]
REPETIR_OK = []      # [(clip, segundo)]: tramos de bruto que salen dos veces A PROPÓSITO

# ---- Mapa de satélite a pantalla completa: (ancla, duración s, [regiones encendidas], la que se presenta). Regiones: Capas.tsx
MAPAS = []

# ---- Subtítulos, SOLO donde se oye mal (ruido, voz lejana, otro idioma): (ancla, duración s, "texto"[, color])
SUBS = []

# ---- Título sobre la marca "titulo" y botón de suscripción cuando se dice. Textos en el IDIOMA del vídeo.
TITULO = None        # {"arriba": "LÍNEA PEQUEÑA", "grande": "PALABRA ENORME", "abajo": "línea pequeña", "dur": 4.0}
BOTONES = []         # [(ancla, nº[, {"vel": 1.25, "esc": 0.34}])]: SIEMPRE que pide suscribirse, like o campana: botón ANIMADO de la
                     # skill (1-16), abajo en el centro. Ej.: [(((A, "suscríbete al canal", -1), -4.1), 2, {"vel": 1.25})]. Si el vídeo no
                     # es en español coge solo la versión en su idioma (b02_en…). Cuál, encaje con la voz e idiomas: base/recursos.md § 9.

# ---- Gráficos PROPIOS del creador (su mascota, su logo sobre la intro…): (ancla, segundos, "tipo"[, {datos}]).
# Qué tipos hay y qué datos lleva cada uno: personal/<creador>/recursos.md. Los pinta estudio/src/personal/<creador>/Graficos.tsx
# (hay que importarlo en el Capas.tsx de este vídeo). "snd": ["pop", 0.18] en los datos = con ese sonido.
PROPIOS = []
# RETARDO_TEXTO = {"tipo": 0.5}   # si un gráfico tarda en poder LEERSE desde que empieza (una mascota que asoma y luego saca
#                                 # la burbuja): timing_textos.py cuenta desde ahí

# ---- Matrículas: SIEMPRE difuminadas y ajustadas (herramientas/montaje/tapar.py: ahí está cómo se rellena).
TAPAR = []           # [(clip, t0, t1, [(t_ref, (x0, y0, x1, y1), a, b), ...])]

# ---- Resaltar algo importante que se pierde en el plano: todo en blanco y negro MENOS el sujeto, que se sigue
# (herramientas/montaje/foco.py: ahí están las opciones). Con criterio: 1-2 por vídeo, 2-5 s (base/preferencias.md -> Resaltar).
FOCOS = []           # [(clip, t0, t1 del bruto, [cx, cy, rx, ry] del sujeto en t0[, {"en": ancla del plano, "fijo": True}])]

# ---- Dinamismo (los cortes de escala alternos los pone solo dinamica.py; aquí va lo que se elige a mano)
FUERTES = []         # (clip, "frase", n): punch-in de golpe x1,65 a la cara mientras dura la frase. 1-2 por minuto.
ENTRADAS = []        # (clip, "frase", n, escala): zoom-in animado rápido con frenada («mira», el nombre del animal, el remate). Pocos.
DATOS = []           # (ancla de frase, "CIFRA", "qué es", duración mínima s): cifra junto a la cara, en el instante en que se dice
GOLPES = []          # (ancla, duración s, "PALABRA|SEGUNDA LÍNEA"[, {"y": 0.62}]): palabra-golpe grande abajo (o más arriba, si abajo está lo que se enseña)
NOTAS = []           # (ancla, retardo s, duración s, "*comentario del editor*"): PROPUESTAS, se validan con el creador

# ---- Efectos de sonido: por defecto, uno suave por gráfico (paso5_audio.py). Para cambiarlos o quitarlos: SFX = {"dato": ("pop", 0.2)}

# ---- Música: SOLO donde toca (30-40 % del vídeo) salvo que el creador la lleve seguida (su preferencias.md): entonces,
# una ventana por capítulo, de ("@sN", -0.4) a ("@sN+1", -4.0). Pistas de personal/<creador>/recursos/musica/ (CATALOGO.md): las descarga el creador.
PISTAS = {
    # "alegre": ("feel-good-days_mvmt-music_97bpm.wav", 97),
}
VENTANAS = [
    # ("alegre", "inicio", ("@s1", 8.0)),            gancho + título + arranque
    # ("alegre", ("@s2", -0.4), ("@s2", 14.0)),      entrada de un capítulo
    # ("alegre", ("@cierre", -2.0), "fin"),          cierre: usa el final real de la canción
]
