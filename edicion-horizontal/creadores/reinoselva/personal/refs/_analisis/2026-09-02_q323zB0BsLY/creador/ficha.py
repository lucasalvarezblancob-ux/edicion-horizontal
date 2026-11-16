# Genera la ficha JSON del vídeo. Uso (desde refs/): python _analisis/<VIDEO>/creador/ficha.py
import json

V = "2026-09-02_q323zB0BsLY"
F = "_analisis/%s/creador/" % V
BARRA = "Abajo al centro, x 23–76 %, y 76–91 %"

d = {
    "video": V,
    "titulo": "Un hallazgo inesperado en el estanque: la vida encontró un camino",
    "duracion_s": 1314,
    "estructura": {
        "gancho": {
            "t0": 0, "t1": 16.2,
            "que": "Tráiler de 7 planos (cortes en 1,53 / 3,37 / 5,72 / 6,58 / 8,65 / 9,53; 2,3 s de media) con frases "
                   "sacadas del propio vídeo: grito con los brazos abiertos, «¿Ves? Por eso dejo margen aquí» (sale del "
                   "min 2:24), mano en la fuga, «Esta planta va a necesitar mucho sol y que Ragnar no la reviente» "
                   "(min 4:29) con el perro escarbando, y cierra con «Ya estamos aquí, el momento del secreto "
                   "desvelado» (min 13:58, porche con Guille). Promete la sorpresa del final sin enseñarla. Música "
                   "desde el segundo 1."},
        "intro": {
            "t0": 16.2, "t1": 20.95,
            "antes": "Último plano del gancho (porche, «el momento del secreto desvelado»); entra con desenfoque de "
                     "zoom de 0,1 s (16,10–16,20).",
            "encima": "Clip del dron recortado a 4,75 s: vuelo entre árboles 16,3–17,0 y sube sobre las copas con el "
                      "río a la izquierda. Logo «Reino Selva» con letras (tortuga dorada con corona y hojas + REINO "
                      "SELVA en verde oscuro, halo claro) centrado; aparece en 18,1 (fundido de ~0,1 s) y queda fijo "
                      "hasta 20,9; caja aprox. x 37–64 %, y 17–83 %. Sin título ni otro texto. Sale con desenfoque de "
                      "zoom en 20,9 y corte a «¿Qué pasa, familia?» (21,0).",
            "audio": "Sin voz. La música del gancho sigue y sube a tope (−14 dB, frente a −30 bajo la voz del gancho); "
                     "audio.json no detecta cambio de pista en 16 ni en 21. Al volver la voz baja a −24 y luego a "
                     "−38 dB. Sonido propio del clip: no comprobado."},
        "secciones": [
            {"t0": 0, "titulo": "Gancho / tráiler"},
            {"t0": 16.2, "titulo": "Intro (dron + logo)"},
            {"t0": 20.95, "titulo": "Saludo y problema: el estanque amanece vacío por una fuga (rótulo TOTALMENTE VACÍO, broma en blanco y negro)"},
            {"t0": 95.5, "titulo": "«Estanque samurái»: pide nombre en comentarios (barra de suscripción + tortuga samurái)"},
            {"t0": 110, "titulo": "Charla a cámara sobre la lona, el margen y lo que cuesta un estanque (tortuga Goku pidiendo likes)"},
            {"t0": 211.9, "titulo": "Reparación de la fuga: montaje sin voz con la música alta"},
            {"t0": 258.5, "titulo": "«AL OTRO DÍA...»: estanque lleno, plan de plantar y promesa de la sorpresa final"},
            {"t0": 320, "titulo": "Piscina de emergencia, plantas y Ragnar; «suscribiros» (barra 2)"},
            {"t0": 424, "titulo": "Trasplante y plantación (Instagram, FRAGANCIA A FRAGANCIA, MÁS PLANTAS, GUILLE, «¿Crías?»)"},
            {"t0": 732, "titulo": "Estanque plantado: PONTEDERIA CORDATA, llenado y resultado"},
            {"t0": 838.7, "titulo": "La sorpresa: explicación en el porche con Guille (45 s sin música)"},
            {"t0": 885, "titulo": "Huevos y crías de tortuga: hallazgo, «6 CRÍAS - DOS PUESTAS», saco vitelino"},
            {"t0": 1022, "titulo": "Buscar la cría enterrada, hidratarlas y pasarlas al terrario (barra 3)"},
            {"t0": 1209.4, "titulo": "Despedida a cámara (pide adivinar la especie y suscribirse)"},
            {"t0": 1254, "titulo": "Escena extra sin voz: las crías en el terrario (rótulo SACO VITELINO)"},
            {"t0": 1294.05, "titulo": "Outro"}],
        "outro": {
            "t0": 1294.05, "t1": 1314.05,
            "encima": "Nada: ni logo, ni texto, ni botones, ni pantalla final incrustada (20 s de imagen limpia para las "
                      "tarjetas de YouTube). Entra con desenfoque de zoom de un fotograma (1294,02). El clip de 8 s va "
                      "en vaivén: 8,0 s hacia delante, 8 s marcha atrás y ~4 s otra vez hacia delante (19,97 s). Acaba "
                      "en corte, sin fundido a negro.",
            "audio": "Sin voz. Sigue la misma música que ya sonaba alta en la escena del terrario desde ~1252 (−14 dB, "
                     "pulso continuo a través del corte); baja a −19 dB en el último segundo. Sonido propio del clip: "
                     "no comprobado."}},
    "tortuga": [
        {"t0": 107.5, "t1": 109.55,
         "animacion": "No encaja con ninguna: tortuga disfrazada de samurái (casco, armadura verde y dorada, abanico, katana), ilustración estática; solo se desliza",
         "texto": "",
         "tipo": "broma o reacción (ilustra «el estanque samurái»)",
         "voz": "«Yo he pensado en llamarlo el estanque samurai.» (la palabra, en 107,3)",
         "caja_tortuga_pct": [64, 33, 100, 100], "caja_burbuja_pct": [],
         "entrada": "Se desliza desde el borde derecho en 0,3 s (107,5–107,8), 0,2 s después de la palabra «samurái»; queda a la derecha de la barra de suscripción",
         "salida": "Corte seco con el cambio de plano (109,6)",
         "sonido": "Ningún transitorio en audio.json entre 100 y 112 s",
         "fotograma": F + "tortuga_01-48.jpg"},
        {"t0": 198.6, "t1": 201.65,
         "animacion": "No encaja con ninguna: tortuga disfrazada de Goku (pelo negro de punta, traje naranja, brazos arriba), estática",
         "texto": "Enviad vuestras energías con un like",
         "tipo": "llamada a dar me gusta, en clave de broma",
         "voz": "«mando toda mi energía, bueno no, que no me queda, dejadme un poco a mí porque a mí me hace falta»",
         "caja_tortuga_pct": [1.5, 34, 26, 97], "caja_burbuja_pct": [15.5, 64.5, 48.5, 80],
         "entrada": "Se desliza desde el borde izquierdo en 0,2 s (198,6–198,8); la burbuja nace después: pequeña en 198,8, vacía a tamaño completo en 198,9, texto en fundido 199,0–199,2",
         "salida": "Tortuga y burbuja se deslizan juntas hacia la izquierda (201,6–201,7); aguanta un corte de plano (~201,0)",
         "sonido": "Transitorio en 198,39, pero es el pulso de la música (uno cada 1,0 s); sin efecto claro",
         "fotograma": F + "tortuga_03-20.jpg"},
        {"t0": 397.0, "t1": 398.97,
         "animacion": "No encaja con ninguna: llorando de risa con los dos brazos arriba, medio cuerpo, contorno negro; estática",
         "texto": "",
         "tipo": "broma o reacción (celebra)",
         "voz": "«lo hemos conseguido, lo hemos conseguido, hemos tenido que deshacer el estanque dos o tres veces»",
         "caja_tortuga_pct": [2, 43.5, 35, 100], "caja_burbuja_pct": [],
         "entrada": "Sube desde abajo en 0,3 s con un pequeño rebote (397,0–397,4), justo con el corte a un primer plano ampliado en posproducción (396,97)",
         "salida": "Corte seco con el cambio de plano (398,97)",
         "sonido": "Sin transitorio en la entrada (el más cercano, 398,62)",
         "fotograma": F + "tortuga_06-38.jpg"},
        {"t0": 532.0, "t1": 536.65,
         "animacion": "Señalando con el índice hacia la burbuja, guiña y levanta el dedo en bucle de ~1 s (lo más parecido: encogiendo_hombros / explicando); medio cuerpo",
         "texto": "Recuerda que puedes ver todos los procesos y consejos para tus hábitats en Instagram (Link en la descripción)",
         "tipo": "aviso (promoción de Instagram)",
         "voz": "«lo pusimos todo, lo que pasa que a partir de ahora no será así» (sin relación: es un aviso del editor)",
         "caja_tortuga_pct": [9, 60, 36, 100], "caja_burbuja_pct": [27, 50.5, 62.5, 67.5],
         "entrada": "Sube desde abajo en 0,3 s (532,0–532,3); la burbuja nace después: vacía en 532,4, texto en fundido 532,5, completa 532,6",
         "salida": "Tortuga y burbuja bajan juntas y salen por abajo (536,4–536,7); aguanta un corte de plano (535,88)",
         "sonido": "Ningún transitorio entre 528 y 540 s",
         "fotograma": F + "tortuga_08-54.jpg"},
        {"t0": 691.8, "t1": 695.25,
         "animacion": "Señala y levanta el índice, y acaba pensativa con la mano en la barbilla mirando arriba (693,8–694,9); no encaja del todo: lo más parecido es encogiendo_hombros",
         "texto": "¿Crías?",
         "tipo": "broma o reacción (repite la palabra clave como pregunta y crea intriga)",
         "voz": "«Las crías no las has visto, ¿no? Las crías. Haremos un vídeo ahora.»",
         "caja_tortuga_pct": [15, 65.5, 33, 100], "caja_burbuja_pct": [27.5, 54, 53.5, 70],
         "entrada": "Sube desde abajo en 0,4 s (691,8–692,2), 0,4 s después de «¿no?»; burbuja vacía en 692,3–692,4, texto en fundido 692,5, completa 692,6",
         "salida": "Baja con la burbuja y sale por abajo (695,0–695,3)",
         "sonido": "Sin transitorio en la entrada (694,37 y 694,9 son pulso de la música)",
         "fotograma": F + "tortuga_11-33.jpg"},
        {"t0": 1003.0, "t1": 1011.55,
         "animacion": "Señalando con el índice hacia la burbuja, guiña y levanta el dedo en bucle (lo más parecido: explicando / encogiendo_hombros); medio cuerpo",
         "texto": "El saco vitelino es una estructura membranosa unida al abdomen de la tortuga recién nacida que contiene la yema de su huevo. // Funciona como una reserva nutritiva mientras la cría sale del nido y comienza a alimentarse por sus propios medios:",
         "tipo": "dato curioso (define el término técnico que acaba de decir)",
         "voz": "«Ya ha absorbido el saco vitelino, aún no lo ha absorbido del todo, pero bueno, ya casi lo tiene, ya casi lo tiene. Hay que dejarlas como una semana incubando»",
         "caja_tortuga_pct": [0, 69, 16, 100], "caja_burbuja_pct": [11.5, 60, 40, 73],
         "entrada": "Sube desde abajo en 0,3 s (1003,0–1003,3); burbuja vacía en 1003,4–1003,5 y con texto en 1003,6",
         "salida": "El texto cambia en seco en 1008,0 (primer texto 4,4 s, segundo 3,5 s) sin mover la burbuja; baja con la burbuja y sale por abajo (1011,4–1011,6). Aguanta tres cortes de plano",
         "sonido": "Sin transitorio en la entrada (el más cercano, 1011,21, en la salida; dudoso)",
         "fotograma": F + "tortuga_16-45.jpg"}],
    "burbujas_sin_tortuga": [
        {"t0": 275.3, "t1": 277.03, "texto": "Oí que me llamabais",
         "habla": "el perro Ragnar al entrar en plano",
         "voz": "«que Ragnar no la reviente, así que vamos a plantarlas»",
         "caja_burbuja_pct": [10, 51.5, 40, 68],
         "entrada": "Nace pequeña y vacía (275,3–275,4), texto en fundido 275,5",
         "salida": "Corte seco con el cambio de plano",
         "fotograma": F + "burbuja_04-36.jpg"},
        {"t0": 618.8, "t1": 621.55, "texto": "Por favor, traigan un abogado-sastre",
         "habla": "el pantalón (se lo está subiendo); va dentro de un zoom de ×2,4 hacia el pantalón y se encoge con el plano al abrir",
         "voz": "«me voy a subir los pantalones... los he lavado, están limpios, relativamente»",
         "caja_burbuja_pct": [13.5, 34, 42.5, 45.5],
         "entrada": "Nace pequeña y vacía (618,8–618,9), texto en fundido 619,0",
         "salida": "Se encoge con el zoom de salida y desaparece en 621,6, justo antes del barrido",
         "fotograma": F + "burbuja_10-19.jpg"}],
    "rotulos": {
        "tipos": [
            {"tipo": "Frase subrayada o remate de lo que dice (2–3 palabras)",
             "fuente": "Condensada gruesa en mayúsculas, parecida a Bebas Neue / Anton",
             "color": "Blanco con contorno negro fino y sombra negra suave, sin caja",
             "posicion": "Centrado en el tercio inferior (centro a y 73–83 %)", "alto_pct": 11,
             "ejemplos": [{"t": 26.6, "texto": "TOTALMENTE VACÍO"}, {"t": 564, "texto": "FRAGANCIA A FRAGANCIA"}]},
            {"tipo": "Salto de tiempo o título de paso", "fuente": "La misma", "color": "El mismo",
             "posicion": "Centrado abajo (y ~82 %)", "alto_pct": 11,
             "ejemplos": [{"t": 258.5, "texto": "AL OTRO DÍA..."}, {"t": 622.4, "texto": "MÁS PLANTAS"}]},
            {"tipo": "Nombre de especie (científico) y cifra", "fuente": "La misma", "color": "El mismo",
             "posicion": "Centrado abajo (y ~80 %), ancho 62–64 % del cuadro", "alto_pct": 11,
             "ejemplos": [{"t": 757.5, "texto": "PONTEDERIA CORDATA"}, {"t": 992, "texto": "6 CRÍAS - DOS PUESTAS"}]},
            {"tipo": "Etiqueta con flecha roja curva (borde blanco) que señala a una persona o un detalle",
             "fuente": "La misma", "color": "Texto blanco con contorno; flecha roja",
             "posicion": "Junto a lo señalado (GUILLE a y ~42 %; SACO VITELINO a y ~76 %)", "alto_pct": 11,
             "ejemplos": [{"t": 649.5, "texto": "GUILLE"}, {"t": 1275.5, "texto": "SACO VITELINO"}]},
            {"tipo": "Círculo de línea discontinua blanca que resalta un animal, sin texto", "fuente": "",
             "color": "Blanco", "posicion": "Centro (x 27–73 %, y 2–80 %)", "alto_pct": 0,
             "ejemplos": [{"t": 797, "texto": ""}]}],
        "por_minuto": 0.4},
    "musica": {
        "pct_con_musica": 96,
        "tramos": [
            {"t0": 1, "t1": 16, "nota": "Gancho: −14 dB en los huecos, ~−30 bajo la voz"},
            {"t0": 16, "t1": 21, "nota": "Intro: la misma música a tope (−14 dB), sin voz"},
            {"t0": 21, "t1": 212, "nota": "Fondo bajo la voz a −38 dB (unos 18 dB por debajo)"},
            {"t0": 212, "t1": 261, "nota": "Reparación sin voz: música protagonista a −13 dB; corta en 260–261"},
            {"t0": 266, "t1": 840, "nota": "Fondo a −36 dB bajo la voz, sube a −20 en los huecos; cambios de pista en 292, 466, 766 y 790"},
            {"t0": 840, "t1": 885, "nota": "SIN música (−60 dB): los 45 s de explicación previa a la sorpresa van solo con voz"},
            {"t0": 885, "t1": 1085, "nota": "La música vuelve (−23 dB) justo al enseñar huevos y crías; luego fondo a −40"},
            {"t0": 1093, "t1": 1252, "nota": "Fondo a −38 dB; cambio de pista en 1102"},
            {"t0": 1252, "t1": 1314, "nota": "Terrario sin voz y outro: música alta a −14 dB, continua a través del corte al outro"}],
        "nivel_vs_voz_db": -16.9,
        "pistas": 9,
        "tipo": "Instrumental de fondo con pulso marcado (transitorios cada 0,5–1,0 s); sube cuando no hay voz. Género y si lleva letra: no comprobado"},
    "sfx": {
        "por_minuto": 0.3,
        "usos": [
            {"t": 31.9, "con": "Plano en blanco y negro sobre «tiro la toalla»: el nivel sin voz sube de −38 a −23 dB (efecto probable)"},
            {"t": 211.9, "con": "Transición borrosa a la reparación: sube a −25 dB (silbido de barrido probable)"},
            {"t": 621.7, "con": "Barrido antes del rótulo MÁS PLANTAS: transitorio 621,67 y subida a −23 dB"},
            {"t": 634.9, "con": "Transición con giro: transitorio 634,95 y subida a −23 dB"},
            {"t": 818.7, "con": "Transición con giro al resultado: transitorio 818,69 y subida a −23 dB"},
            {"t": 838.7, "con": "Barrido fuerte a la sección de la sorpresa: subida a −19 dB"}]},
    "ritmo": {
        "plano_medio_s": 4.96, "plano_mediana_s": 3.18, "pct_a_camara": 42,
        "zooms": "Pocos y puntuales, para el chiste: punch-in a primer plano al entrar el rótulo TOTALMENTE VACÍO "
                 "(26,4–26,8), primer plano ampliado ~×2 durante 2 s con la tortuga que ríe (396,97–398,97), zoom "
                 "continuo ×2,41 en 1,5 s hacia el pantalón y vuelta (617,15–621,5), y zoom de apertura ×1→×0,67 al "
                 "volver de la intro (21,9–23,6; probable posproducción). Los planos a cámara largos van fijos "
                 "(×0,99 en 62–67 y 920–930).",
        "transiciones": "Corte seco casi siempre (264 cortes). 10 transiciones borrosas: zoom desenfocado al entrar y "
                        "salir de la intro (16,1 y 20,9) y al entrar al outro (1294,0); barridos o giros en 211,9, "
                        "524,35, 621,7, 634,9, 727,85, 818,7 y 838,7, en cambios de lugar o de sección. Sin fundidos "
                        "a negro.",
        "velocidades": "Cámara rápida probable en algún plano de acción (622,0–623,7, se incorpora muy deprisa); el "
                       "clip del outro va marcha atrás 8 s; la tercera barra de suscripción va al doble de velocidad. "
                       "Cámara lenta: no vista. Sin pantalla partida. Insertos: imagen de sus «clones» a pantalla "
                       "completa (59,55–61,97) y material de otro día (hallazgo de los huevos, ~878 y 900–916)."},
    "botones": [
        {"t0": 101.42, "t1": 110.85,
         "que": "Barra animada: botón de YouTube + me gusta + SUSCRÍBETE→SUSCRITO + campana, con cursor que pulsa los tres (9,43 s). Sale cuando pide dejar un comentario, no al decir «suscribiros»",
         "posicion": BARRA},
        {"t0": 419.18, "t1": 428.62,
         "que": "La misma barra (9,43 s) sobre «si os mola todo esto, suscribiros al canal»; aguanta 4–5 cortes de plano",
         "posicion": BARRA},
        {"t0": 1125.55, "t1": 1130.25,
         "que": "La misma barra al doble de velocidad (4,70 s) sobre «suscribiros, subiros al canal»",
         "posicion": BARRA}],
    "logo": "No hay marca de agua fija. El logo solo sale centrado sobre la intro (18,1–20,9).",
    "color_formato": "16:9 a pantalla completa, sin bandas ni viñeta ni subtítulos incrustados. Color natural de móvil "
                     "o cámara de acción, sin filtro evidente. Un único efecto de color: 0,7 s en blanco y negro "
                     "(31,9–32,5) para la broma «tiro la toalla».",
    "no_comprobado": [
        "Qué suena exactamente (no se oye): género de la música, si la intro y el outro llevan sonido propio y si las transiciones llevan silbido; se deduce de los niveles de audio.json",
        "Si la tortuga o la burbuja llevan un efecto de sonido suave al aparecer: no hay transitorio ni subida de nivel en ninguna de las 6 entradas, pero un «pop» bajo no se distinguiría",
        "Rótulos de menos de 2 s en la mitad superior del cuadro: el repaso segundo a segundo cubre solo la mitad inferior; la superior, cada 2 s",
        "Ocho candidatos a transición borrosa sin mirar (10,75, 656,45, 685,2, 1051,7, 1079,45, 1254,05, 1268,7 y 1275,5)",
        "El % a cámara (42 %) es una suma a ojo sobre hojas de un fotograma cada 2 s",
        "Tiempos de entrada y salida de los rótulos, salvo TOTALMENTE VACÍO y MÁS PLANTAS, con ±0,5 s",
        "Número real de pistas de música (audio.json detecta 9 cambios)",
        "Si el zoom de apertura de 21,9–23,6 es de posproducción o del brazo",
        "Pantalla final y vídeos sugeridos de YouTube: no están en el archivo"]}

json.dump(d, open(V + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", V + ".json")
