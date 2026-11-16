# Encargo: analizar la edición de UN vídeo de referencia

Eres editor de vídeo profesional. Analiza **cómo está editado** el vídeo que se te indica (YouTube horizontal,
vlog dinámico). El resultado alimenta una guía de edición: hacen falta hechos con tiempos y números, no opiniones.

1. Lee `refs/dinamicos/_analisis/METODO.md` (qué hay ya calculado, herramientas y los 12 puntos a cubrir).
2. Lee de la carpeta del vídeo: el resumen de `cortes.json` (campos `global`, `tramos`; la lista `cortes` cuando
   necesites tiempos exactos), `audio.json` (todo menos `por_segundo`/`acentos`, que consultas con un script
   corto cuando haga falta) y `transcripcion.txt` entera.
3. Mira TODAS las hojas `hojas/intro_*.jpg` (intro cada 0,25 s) y TODAS las `hojas/min_*.jpg` del tramo asignado.
4. Donde importe, baja al detalle: hojas cada 0,1 s alrededor de transiciones, fotogramas completos y recortes
   de cada tipo de rótulo (guárdalos en `<carpeta>/rotulos/`), `medir_zoom.py` en al menos 8 planos.
5. Cruza imagen con transcripción y audio: b-roll sobre voz, J/L cuts, entradas de música, acentos en cortes.

No juzgues la calidad de imagen. No modifiques nada fuera de la carpeta de análisis del vídeo y del archivo de
ficha. No uses git ni subas nada. No lances procesos pesados (nada de demucs/whisper: ya está hecho).

## Entrega
Escribe la ficha en la ruta que se te indica (JSON válido, UTF-8, en español) con estas claves:
`video` {archivo, creador, url, titulo, duracion, publicado, tramo_analizado},
`resumen` (5–8 frases), `estructura` [{desde, hasta, parte, que_pasa}],
`ritmo` {s_por_plano por parte, jump_cuts, j_l_cuts, match_cuts},
`intro` {cold_open, recap {existe, desde, hasta, n_planos, s_por_plano, de_donde_salen, frase}, titulo_cabecera,
 motion_graphics, musica_entra_s, linea_de_tiempo [{t, que}]},
`broll` {proporcion_sobre_voz, origenes {mismo_video, recursos, stock_archivo}, duracion_tipica_s, vuelta_a_camara, ejemplos},
`voz_en_off` {uso, guion, mezcla}, `transiciones` [{tipo, veces, donde, ejemplos_t}],
`zooms` {mediciones [{t, escala, duracion_s, tipo}], patron},
`tipografia` [{tipo, fuente_parecida_google, peso, tamano_rel, posicion, color, borde_sombra, entrada, salida, duracion_s, ejemplos_t, recorte}],
`motion_graphics` [{tipo, t, duracion_s, como_entra, estilo}],
`musica` {tramos_resumen, voz_menos_musica_db, cambia_por_secciones, a_ritmo_de_cortes, silencios_intencionados},
`sfx` {por_minuto_estimado, tipos, donde, ejemplos_t}, `subtitulos` {hay, cuando, estilo},
`cierre` {como_acaba, cta, pantalla_final}, `para_copiar` [ideas concretas aplicables], `dudas` [lo que no se pudo determinar].

Tu respuesta final: 15–25 líneas con lo más importante y los números clave (la ficha tiene el detalle).
