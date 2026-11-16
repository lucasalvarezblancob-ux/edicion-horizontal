# Encargo: estudiar cómo edita <CREADOR> un vídeo suyo (personalización del creador)

> PLANTILLA de la skill `edicion-horizontal`. Antes de pasársela a un agente, **rellena los huecos** `<…>` (quién es, la
> carpeta y, sobre todo, la lista de sus recursos propios) y guarda la copia en `personal/<creador>/refs/_analisis/`.
> Un agente por vídeo, **de dos en dos**. Antes hay que tener calculado el material de cada vídeo (hojas, cortes,
> transcripción, audio) con el método de `<skill>/base/refs/dinamicos/_analisis/METODO.md`.

Eres un analista de edición. Vas a estudiar **un** vídeo publicado del canal de YouTube «<CANAL>» (<de qué va, idioma>;
vídeo horizontal). No se juzga la calidad de imagen ni el contenido: solo
**cómo está editado**, para que otra persona pueda editar un vídeo nuevo «a su manera». Lo que saques va a la carpeta
de personalización del creador. Las bases de edición (ritmo, zooms, planos de recurso) ya existen y NO se cambian:
aquí interesa lo **propio del creador**.

Todo en español de España. No ves movimiento ni oyes: trabajas con fotogramas y con los datos de audio ya medidos.
Dilo así cuando algo no lo puedas comprobar («no comprobado»), no lo inventes.

## Material (ya calculado; NO lo recalcules)

Carpeta de trabajo: `<CARPETA>/personal/<creador>/refs/`
- Vídeo: `<VIDEO>.mp4` (1280×720). Título y fecha en `VIDEOS.tsv`.
- `_analisis/<VIDEO>/hojas/`: `intro_NN.jpg` (primeros 60 s, denso), `min_NN.jpg` (una hoja por minuto), `final_NN.jpg`.
- `_analisis/<VIDEO>/cortes.json`: cortes detectados (tiempos). `transcripcion.json`/`.txt`: lo que se dice, con tiempos.
- `_analisis/<VIDEO>/audio.json`: por tramos, nivel de voz y de música (stems ya separados), entradas y salidas de
  música, transitorios (posibles efectos de sonido).
- Método general de medida (léelo antes de empezar, es corto):
  `<skill>/base/refs/dinamicos/_analisis/METODO.md`

Python con OpenCV: `<CARPETA>/herramientas/.venv/Scripts/python.exe`. `ffmpeg` y `ffprobe` en el PATH.
Usa Bash (Git Bash). **No uses `drawtext` de ffmpeg** (falla en este equipo). Heredocs cortos; nada de scripts enormes.

## Reglas

- **Poca memoria (16 GB compartidos con otros procesos): un solo ffmpeg a la vez**, nunca en paralelo; nada de demucs,
  whisper ni modelos; fotogramas a 720p o menos. No lances subagentes.
- Escribe solo dentro de `_analisis/<VIDEO>/` (tus fotogramas y hojas, en `_analisis/<VIDEO>/creador/`) y tus dos
  archivos de salida. No toques nada más, no borres nada, no descargues nada, no subas nada, nada de git.
- Mira las imágenes de verdad (herramienta Read sobre los .jpg). Cada dato de la ficha tiene que salir de un fotograma
  que has mirado o de un número de `audio.json`/`cortes.json`/`transcripcion.json`.

## Recursos propios del creador que debes reconocer

<Describe aquí, uno por uno, los archivos que ha pasado, tal como se VEN (míralos antes: no te fíes del nombre).>
- **Intro** (cabecera): <qué se ve, cuánto dura el archivo, si tiene sonido>. Puede llevar encima logo o título.
- **Outro** (cierre): <qué se ve, cuánto dura, si tiene sonido>.
- **Logo**: <cómo es; variantes>. Puede ir fijo en una esquina, o solo en intro y outro.
- **Mascota o personaje** (si tiene): <cómo es: colores, estilo>, normalmente con una **burbuja de texto**. Animaciones
  que existen (anota cuál es cada vez; si no encaja con ninguna, descríbela): <lista con una frase por animación>.
- **Botones de YouTube** (suscríbete, me gusta, campana): animaciones superpuestas.

Si el creador no tiene mascota, cambia «la mascota» de abajo por su recurso más característico (una cortinilla, un
sonido, una coletilla rotulada) o quita el punto 2.

## Qué hay que sacar

1. **Estructura del vídeo**: gancho o tráiler inicial (qué dura, qué enseña), dónde entra la **intro** (segundo exacto,
   qué va antes y después, si lleva logo, título o texto encima, si la música cambia ahí: míralo en `audio.json`),
   secciones, cierre y **outro** (segundo exacto, qué lleva encima: pantalla final, logo, texto, vídeos sugeridos).
2. **La mascota: TODAS sus apariciones.** Para cada una: `t0`, `t1` (segundos, afinando a ±0,2 s con fotogramas
   seguidos), animación, **texto literal de la burbuja**, posición y tamaño en pantalla (en % del ancho y alto del
   cuadro: caja de la mascota y caja de la burbuja), cómo entra y sale (corte seco, se desliza, aparece la burbuja
   después que la mascota…: mira fotogramas a 0,1 s en la entrada y la salida), qué se está diciendo en la voz en ese
   momento (cita de la transcripción) y **tipo de comentario** (dato curioso, aclaración o corrección, nombre de
   especie, broma o reacción, aviso, llamada a suscribirse, otro). Mira también si coincide con un transitorio de
   `audio.json` (efecto de sonido al aparecer).
   Para no saltarte ninguna, repasa el vídeo entero con hojas del cuadrante donde suele salir (aquí, el inferior derecho;
   **mira también el izquierdo**: a veces va en espejo) a 1 fotograma por segundo:
   `ffmpeg -nostdin -v error -y -i <VIDEO>.mp4 -vf "fps=1,crop=640:360:640:360,scale=192:108,tile=10x6" -q:v 3 _analisis/<VIDEO>/creador/bd_%02d.jpg`
   (cada hoja = 60 s, de izquierda a derecha y de arriba abajo). Luego confirma cada aparición con fotogramas a tamaño
   completo. Guarda un fotograma completo de cada aparición en `creador/mascota_<mm-ss>.jpg`.
3. **Rótulos y textos**: tipos (título, nombres de especie, cifras, aclaraciones, subtítulos), fuente parecida, color,
   borde o caja, posición, tamaño (% del alto), animación de entrada si se aprecia, cuántos por minuto.
4. **Música**: en qué tramos hay música y en cuáles no (de `audio.json`), % del vídeo con música, nivel respecto a la
   voz, cuántas pistas distintas parece haber, y qué tipo de música dirías por contexto (lo que no puedas saber del
   género, di «no comprobado»). Si la intro y el outro tienen música propia.
5. **Efectos de sonido**: transitorios de `audio.json` que coinciden con cortes, rótulos o apariciones de la mascota;
   cuántos por minuto.
6. **Ritmo y planos**: duración media y mediana de plano, % de voz a cámara frente a planos de recurso, zooms o
   reencuadres en posproducción (compara fotogramas del mismo plano), transiciones (corte seco, fundidos…),
   velocidades (cámara rápida o lenta), pantalla partida, imágenes o vídeos de archivo insertados.
7. **Botones y llamadas**: suscripción, me gusta, campana: segundo, qué botón, posición, tamaño, duración.
8. **Logo o marca de agua** fijo: dónde, tamaño, todo el vídeo o a ratos.
9. **Color y formato**: bandas, viñeta, filtros evidentes, subtítulos incrustados.

## Salida

1. `<CARPETA>/personal/<creador>/refs/<VIDEO>.json` con esta forma (campos vacíos si no hay):
```json
{"video": "<VIDEO>", "titulo": "", "duracion_s": 0,
 "estructura": {"gancho": {"t0": 0, "t1": 0, "que": ""}, "intro": {"t0": 0, "t1": 0, "antes": "", "encima": "", "audio": ""},
                "secciones": [{"t0": 0, "titulo": ""}], "outro": {"t0": 0, "t1": 0, "encima": "", "audio": ""}},
 "mascota": [{"t0": 0, "t1": 0, "animacion": "", "texto": "", "tipo": "", "voz": "", "caja_mascota_pct": [0, 0, 0, 0],
              "caja_burbuja_pct": [0, 0, 0, 0], "entrada": "", "salida": "", "sonido": "", "fotograma": ""}],
 "rotulos": {"tipos": [{"tipo": "", "fuente": "", "color": "", "posicion": "", "alto_pct": 0, "ejemplos": [{"t": 0, "texto": ""}]}], "por_minuto": 0},
 "musica": {"pct_con_musica": 0, "tramos": [{"t0": 0, "t1": 0, "nota": ""}], "nivel_vs_voz_db": 0, "pistas": 0, "tipo": ""},
 "sfx": {"por_minuto": 0, "usos": [{"t": 0, "con": ""}]},
 "ritmo": {"plano_medio_s": 0, "plano_mediana_s": 0, "pct_a_camara": 0, "zooms": "", "transiciones": "", "velocidades": ""},
 "botones": [{"t0": 0, "t1": 0, "que": "", "posicion": ""}],
 "logo": "", "color_formato": "", "no_comprobado": [""]}
```
   Las cajas van como `[x0, y0, x1, y1]` en % del cuadro. Comprueba que el JSON es válido (`python -m json.tool`).
2. `…/refs/<VIDEO>.md`: media página con lo más característico de este vídeo y **reglas prácticas** para imitarlo
   («la mascota sale cada X min, siempre cuando…, con frases de N palabras…»).

Tu respuesta final: 15 líneas como mucho con lo esencial (intro y outro, nº de apariciones de la mascota y cuándo las
usa, música, botones) y lo que no has podido comprobar.
