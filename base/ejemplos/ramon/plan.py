# Plan de imagen, textos y música de "ramon". EJEMPLO de la skill (formato: herramientas/montaje/plantilla_video/plan.py).
# Es la versión SOLO CON LAS BASES. La del creador (su intro, su outro, su mascota con burbuja, música en todo el vídeo)
# añade PROPIOS, dos piezas V en el EDL y otras VENTANAS: eso es personalización y vive en la carpeta de edición (SKILL.md § 4).
# Todo cuelga de frases literales: (clip, "frase", n) con n = 0 primera vez que suena (tráiler), -1 la última.
A, B_, C, D, E_, F = "C0246", "C0247", "C0248", "C0251", "C0253", "C0254"

# ---- Planos de recurso sobre la voz ----
# (ancla, clip origen, segundo origen, duración s | None = hasta el final de la pieza)
# REGLA (Lucas, 2026-11-11): cada recurso se elige MIRANDO sus fotogramas (tira.py) y se revisa con hoja_recursos.py:
# tiene que verse aquello de lo que se habla desde el primer fotograma; nada de barridos, paredes ni arranques de cámara.
BROLL = [
 # Elegidos con el registro visual (bruto/ramon-analisis/visual/<clip>.json): solo tramos marcados como buen recurso,
 # con inicio y final donde el sujeto ya está en imagen y la cámara quieta. 5.º elemento opcional: (zoom, cx, cy) en 3840x2160.
 # Ancla ("@tag", s): frame de la marca del EDL + s segundos (para tapar un plano V conservando su sonido).
 ((A, "the most endangered tortoise", 0), A, 230.0, 2.6),
 ((B_, "they are eating like piranha", 0), B_, 293.0, None, (1.5, 1780, 1060)),
 ((F, "two of our huge tortoises", 0), E_, 26.8, None),
 ((A, "He comes from Egypt", -1), A, 177.5, 3.8),
 ((A, "we're gonna put him back here", -1), A, 274.0, 3.2),
 ((B_, "put a potus plant", -1), B_, 320.0, 3.3),
 ((B_, "it's zero toxic", -1), B_, 327.0, 3.0),
 ((B_, "we're gonna throw a few crickets", -1), B_, 10.2, 3.6),
 (("@caza", 0), B_, 292.0, 1.3, (1.35, 1780, 1060)),
 (("@caza", 1.3), B_, 293.3, 3.7, (2.0, 1790, 950)),       # corte a la tortuga con el grillo en la boca: va con FOCOS y su rótulo
 (("@caza", 5.0), B_, 297.0, None, (1.35, 1780, 1060)),
 ((B_, "like they need a lot of protein", -1), B_, 300.6, 3.0, (1.4, 1780, 1060)),
 ((B_, "they are eating like piranha", -1), B_, 333.0, None, (1.45, 3020, 1480)),
 ((B_, "when they came", -1), B_, 505.0, 4.0),
 ((B_, "the Russian tortoise it's", -1), B_, 540.8, 4.2),
 ((B_, "you shouldn't be maintaining", -1), B_, 645.8, 3.6),
 ((B_, "at least a pair of them", -1), B_, 542.2, 2.8, (1.35, 2020, 1190)),
 ((C, "this initially was going to be", -1), C, 312.6, 5.0),
 ((C, "all of those plants here", -1), C, 297.0, 3.6),
 ((C, "we've got tanictis", -1), C, 264.0, 3.0),
 ((C, "we're going to move all the plants", -1), C, 270.8, 4.5),
 ((D, "since we planted all these", -1), D, 28.6, 2.7),
 ((D, "what we have here is sapphire", -1), D, 40.9, 3.5),
 ((D, "because we've got heating system", -1), D, 469.6, 3.0),
 ((D, "all of them are doing great", -1), D, 561.7, 2.9, (1.6, 1820, 1160)),
 ((D, "now we have to move all the fish", -1), D, 967.8, 4.0),
 ((D, "also hillary our argentinian", -1), D, 972.2, 3.6),
 ((D, "also the corridoras are breeding", -1), D, 32.4, 2.9),
 ((E_, "African desert tortoises", -1), E_, 26.8, 3.5),
 ((E_, "everything started because of the rains", -1), E_, 147.4, 5.5),
 ((E_, "i had to take the tortoises out", -1), "C0252", 4.2, 3.0),
 ((F, "it was brutus and gold digger", -1), E_, 152.5, 2.6),
 ((F, "we're putting a drainage", -1), F, 130.4, 3.8),
]
# Rótulos con seguimiento: (clip, t0, t1 del bruto, caja inicial [cx, cy, medio lado] en 3840x2160, texto grande, texto pequeño, lado del texto)
TRK = [
 (A, 65.0, 67.15, [3040, 440, 300], "RAGNAR", "head of security", "izq"),
 (A, 229.4, 232.6, [1805, 1190, 220], "ANUBIS", "Egyptian tortoise", "der"),
 (A, 392.1, 395.6, [1843, 1444, 200], "SIEBENROCK'S", "snake-necked turtle", "der"),
 (D, 36.2, 40.9, [1843, 1137, 200], "SAPPHIRE", "northern caiman lizard", "izq"),
 (B_, 293.7, 296.8, [1800, 905, 200], "GOT IT!", "a cricket in its mouth", "der", ("@caza", 1.7)),      # 8.º elemento: sobre un plano de recurso
]
# Resalte (herramientas/montaje/foco.py): todo en blanco y negro menos el sujeto, que se sigue. (clip, t0, t1 del bruto,
# [cx, cy, rx, ry] del sujeto en t0, {opciones}). Aquí: la tortuga con el grillo en la boca, que en el plano es diminuta.
# Con criterio: es el único del vídeo (base/preferencias.md -> Resaltar).
FOCOS = [(B_, 293.45, 297.0, [1805, 925, 170, 190], {"en": ("@caza", 2.0)})]      # "en": solo en ese plano (el mismo bruto sale en el tráiler)
# Mapas a pantalla completa: (ancla, duración s, regiones encendidas, la que se presenta)
MAPAS = [
 ((D, "we have the choco", -1), 4.5, ["choco"], "choco"),
 ((D, "we get the amazon rainforest", -1), 5.5, ["choco", "amazon"], "amazon"),
 ((D, "then we get the atlantic forest", -1), 5.0, ["choco", "amazon", "atlantic"], "atlantic"),
 ((D, "the dry diagonal", -1), 5.5, ["choco", "amazon", "atlantic", "chaco"], "chaco"),
]
# Subtítulos (solo donde no se entiende: charla en español fuera de cámara, en un vídeo en inglés). (ancla, duración s, texto)
SUBS = [
 (("@caza", 1.3), 3.0, "Look, look, look! It's catching one!"),
 (("@caza", 5.0), 1.5, "It got scared."),
 (("@caza", 6.7), 1.3, "It was hunting!"),
]
TITULO = {"arriba": "NEW ANIMALS · NEW ECOSYSTEMS", "grande": "8 SURPRISES", "abajo": "everything that changed here, in one video", "dur": 4.0}
# Petición de suscripción: el botón ANIMADO de la skill (el 2, en su versión en inglés), abajo en el centro. Empieza con la
# despedida y va un 25 % más rápido para que el clic en «SUBSCRIBE» caiga cuando lo dice y la barra se recoja antes del final.
BOTONES = [(((F, "subscribe to my channel", -1), -4.12), 2, {"vel": 1.25})]
DETALLE = {"ANUBIS"}     # tras este rótulo se cierra x1,6 sobre la tortuga (seguimiento comprobado a ojo)

# ---- Dinamismo y textos ----
# Frase fuerte: punch-in de golpe x1,65 centrado en la cara mientras dura la frase, y vuelta por corte.
FUERTES = [
 (A, "but it actually happened", -1), (A, "can you guess", -1), (A, "this is an extraordinary creature", -1), (A, "something unique", -1),
 (A, "something even stranger", -1), (B_, "I want to see them hunt", -1), (B_, "eating like maniacs", -1),
 (B_, "their main problem is humidity", -1), (B_, "just in case", -1), (C, "I've got something to tell you", -1),
 (C, "but what if now we open that", -1), (D, "I've got good news", -1), (D, "even crazier", -1),
 (D, "The male is even crying", -1), (D, "That would be like incredible", -1), (D, "except for the humans", -1),
 (D, "this is gonna be amazing", -1), (D, "be a disaster", -1),
 (E_, "crazy and astonishing", -1), (E_, "this isn't working", -1), (F, "would be drowned", -1),
 (F, "as dry as they can possibly be", -1), (F, "love you guys", -1),
]
# Zoom-in animado (8 f, con frenada) hasta la escala dada; se queda hasta el siguiente corte.
ENTRADAS = [
 (A, "look at this look at this", -1, 1.5), (A, "His name is Anubis", -1, 1.4), (C, "the first idea usually is the best one", -1, 1.4),
 (D, "Winter is starting here", -1, 1.4), (E_, "this is my dream becoming true", -1, 1.5), (F, "so this is everything for today", -1, 1.35),
 (A, "big surprises", -1, 1.4), (B_, "look at that again", -1, 1.45),
]
# Cifra junto a la cara: plano x1,3 con la cara a un tercio y el dato al otro lado. (ancla, grande, pequeño, duración mínima s)
DATOS = [
 ((A, "the most endangered tortoise in Africa", -1), "#1", "most endangered tortoise in Africa", 2.2),
 ((A, "the five species of testudo", -1), "5 / 5", "Testudo species, all here", 2.0),
 ((A, "only a few weeks old", -1), "1 MONTH", "old, more or less", 1.8),
 ((B_, "up to three eggs per season", -1), "3 EGGS", "per season, at most", 2.2),
 ((D, "100 %", -1), "100%", "the whole Amazon biome", 1.8),
 ((D, "for a decade already", -1), "10 YEARS", "living together", 1.8),
 ((D, "a 15 percent", -1), "15%", "of the animals here", 2.0),
 ((D, "maybe five years", -1), "5 YEARS", "...or a whole life", 2.0),
 ((D, "a four meter enclosure", -1), "4 m", "high, fully closed", 2.0),
 ((F, "10 more enclosures", -1), "+10", "new enclosures", 2.0),
]
# Palabra-golpe: texto grande amarillo abajo, entra de golpe y crece de forma continua y suave. (ancla, duración s, texto)
GOLPES = [
 ((A, "the most endangered tortoise", 0), 2.6, "THE MOST ENDANGERED|TORTOISE IN AFRICA"),
 ((B_, "like piranha", 0), 1.6, "LIKE PIRANHA"),
 ((D, "the four ecosystems", 0), 2.4, "4 ECOSYSTEMS"),
 ((F, "would be drowned", 0), 1.4, "DROWNED"),
 ((E_, "my dream becoming true", -1), 2.0, "MY DREAM"),
 ((B_, "like piranha", -1), 1.6, "LIKE PIRANHA"),
]
# Comentario del editor: minúsculas, blanco, entre asteriscos, de golpe. (ancla, retardo s, duración s, texto). PROPUESTAS a validar.
NOTAS = [
 ((B_, "are the crickets playing dead", -1), 0.2, 1.8, "*crickets: playing dead*"),
 ((D, "except for the humans", -1), 0.3, 2.0, "*humans: not thriving*"),
 ((D, "maybe a whole life", -1), 1.0, 1.6, "*no pressure*"),
]

# Música SOLO donde toca (36 % del vídeo): gancho y título; entrada de cada capítulo; secuencias de planos; mapas; la frase
# emotiva; cierre. Cuatro pistas de Shutterstock (personal/<creador>/recursos/musica/CATALOGO.md), una por «clima» del vídeo.
PISTAS = {"boost": ("boost-me_black-rhomb_154bpm.wav", 154), "feel": ("feel-good-days_mvmt-music_97bpm.wav", 97),
          "journey": ("a-hopeful-journey_kozy-sounds_118bpm.wav", 118), "hope": ("pieces-of-hope_luminbird_80bpm.wav", 80)}
VENTANAS = [
 ("boost", "inicio", ("@s1", 8.0)),
 ("feel", ("@s2", -0.4), ("@s2", 14.0)), ("feel", ("@grillos", -1.0), ("@piranha", 5.0)), ("feel", ("@s3", -0.4), ("@s3", 12.0)),
 ("journey", ("@s4", -0.4), ("@s4", 14.0)), ("journey", ((C, "this initially was going to be", -1), -1.0), ((C, "we're going to move all the plants", -1), 6.5)),
 ("journey", ("@paseo", -0.4), ("@s5", 14.0)), ("journey", ((D, "we have the choco", -1), -1.0), ((D, "the dry diagonal", -1), 9.5)),
 ("feel", ("@s6", -0.4), ("@s6", 18.0)),
 ("hope", ("@s7", -0.4), ("@s7", 14.0)), ("hope", ((E_, "this is my dream becoming true", -1), -1.0), ((E_, "this is my dream becoming true", -1), 10.0)),
 ("hope", ("@s8", -0.4), ("@s8", 13.0)),
 ("hope", ("@cierre", -2.0), "fin"),
]

# Matrículas: SIEMPRE difuminadas y ajustadas (herramientas/montaje/tapar.py). El BMW del fondo en C0246: nunca se ve
# entera (retrovisor de la moto en medio), por eso las referencias son los trozos limpios.
_M447, _M440 = (1038, 1228, 1345, 1295), (965, 1360, 1272, 1430)
TAPAR = [("C0246", 437.0, 458.0, [(447.0, _M447, 0.0, 0.48), (440.0, _M440, 0.0, 0.36), (440.0, _M440, 0.78, 1.0)])]
