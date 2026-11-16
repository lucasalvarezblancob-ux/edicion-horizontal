# Encargo: medir el DINAMISMO y los TEXTOS de un vídeo de referencia (tanda 2, 2026-11-11)

Eres editor de vídeo profesional. Lucas vio nuestro primer montaje (3,5 s/plano, punch-in ×1,12 alterno, zoom lento
1,5 %/s, cartelas sobrias) y dijo: «no me parecen lo suficientemente dinámicos, falta algo de juego con zooms y
cortes» y «para los textos y títulos guíate en Xokas y Plex». Este vídeo es una de las referencias que sí le parecen
dinámicas. Hay que sacar **números y recetas copiables**, no opiniones. Solo edición: no juzgues la calidad de imagen.

1. Lee `refs/dinamicos/_analisis/METODO.md` (herramientas). En la carpeta del vídeo hay `cortes.json`,
   `transcripcion.txt/.json`, `hojas/intro_*.jpg` (0–60 s cada 0,25 s) y `hojas/min_MM.jpg` (todo, cada 2 s).
   NO hay `audio.json` (no se separó la música): música y efectos solo los puedes deducir de lo que se ve.
2. Mira todas las hojas `intro_*` y todas las `min_*`. Después elige **al menos 6 tramos de 10–15 s** repartidos
   (2 del principio, 2 del medio, 2 del final; que incluyan habla a cámara, acción y un chiste/reacción) y míralos
   **cada 0,1 s** (`hoja_contactos.sh VIDEO SALIDA.jpg 0.1 INICIO DUR 10 256`), guardando en `<carpeta>/detalle/`.
   Ahí es donde se ven los zooms rápidos, los temblores, los cortes de 2–3 fotogramas y cómo entra el texto.
3. Mide zooms con `medir_zoom.py VIDEO INI FIN` cuando el plano lo permita y, cuando no, a ojo comparando el tamaño
   de la cara/objeto entre el primer y el último fotograma (escala = tamaño final / inicial).

## Qué hay que entregar medido
- **Cortes**: s/plano por parte; % de planos < 1 s; ráfagas (≥ 3 cortes en 2 s): cuántas por minuto, dónde y con qué
  material; jump cuts al hablar (cada cuántas palabras o segundos); cortes a mitad de frase; insertos de 0,2–0,6 s
  (memes, reacciones, planos repetidos); cámara rápida/lenta, congelados, rebobinados, repeticiones.
- **Zooms** (lo más importante): por cada TIPO que veas, una fila con: nombre, escala inicial→final, duración en
  fotogramas o s, curva (lineal, golpe seco, con rebote), centro (cara, objeto, texto), qué lo dispara (palabra
  clave, remate del chiste, reacción, silencio, presentación de persona/objeto), si lleva temblor/blur/sonido
  visible, cuántos por minuto, y 3 ejemplos con tiempo exacto. Tipos a buscar: punch-in en el corte; zoom rápido
  animado dentro del plano («snap zoom»); zoom lento sostenido; zoom-out; zoom + temblor; zoom a cámara lenta;
  reencuadre a un detalle; pantalla partida; cámara virtual que sigue a alguien.
- **Textos y títulos** (segundo punto más importante): cada tipo (título del vídeo, cabecera/intro, «día N»,
  lugar, nombre de persona, precio/dato, comentario del editor, texto-chiste, subtítulos, cuenta atrás, listas)
  con: fuente más parecida de Google Fonts, peso, mayúsculas o no, color y borde/sombra, tamaño (alto de mayúscula ÷
  alto de pantalla), posición, animación de entrada y de salida (en fotogramas), duración, cuántos por minuto y
  3 ejemplos con tiempo. Recorta al menos un ejemplo de cada tipo a `<carpeta>/rotulos/` y dí qué palabra los
  dispara. ¿Subtitulan todo, solo a otras personas, solo frases sueltas?
- **Otros recursos de dinamismo**: stickers/emojis/memes, flechas y círculos, imágenes superpuestas, mapas,
  transiciones (tipo, duración, cuántas), efectos de color o blanco y negro, barras de cine, marcos.
- **Estructura** en 6–10 líneas: gancho/intro (qué pasa en los primeros 30 s), capítulos, cierre.
- **Receta**: 10–15 reglas numéricas listas para programar (p. ej. «punch-in ×1,25 de golpe en la palabra fuerte,
  1 cada 6–8 s; vuelve a ×1,0 en el siguiente corte»).

No modifiques nada fuera de la carpeta de análisis del vídeo y del archivo de ficha. No uses git, no subas nada, no
descargues nada. No lances demucs ni whisper. Trabaja desde la raíz de la carpeta de edición (en Windows, con Git Bash);
Python: `herramientas/.venv/Scripts/python.exe` (macOS: `herramientas/.venv/bin/python`). Mira las imágenes con Read.

## Entrega
Ficha JSON (UTF-8, español) en la ruta indicada con claves: `video` {archivo, creador, url, titulo, duracion,
publicado}, `resumen`, `estructura`, `cortes` {...}, `zooms` [{tipo, escala, duracion, curva, centro, disparador,
extras, por_minuto, ejemplos_t}], `textos` [{tipo, fuente_parecida_google, peso, caja, color, borde_sombra,
tamano_rel, posicion, entrada, salida, duracion_s, por_minuto, disparador, ejemplos_t, recorte}], `subtitulos`,
`otros_recursos`, `transiciones`, `receta` [reglas], `dudas`.
Respuesta final: 20–30 líneas con los números clave y la receta (la ficha tiene el detalle).
