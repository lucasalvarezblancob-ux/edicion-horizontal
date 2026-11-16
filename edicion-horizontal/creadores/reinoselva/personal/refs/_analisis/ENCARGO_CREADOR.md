# Encargo: estudiar cómo edita REINO SELVA un vídeo suyo (personalización del creador)

Eres un analista de edición. Vas a estudiar **un** vídeo publicado del canal de YouTube «Reino Selva» (naturaleza,
estanques, tortugas, reptiles; vídeo horizontal en español). No se juzga la calidad de imagen ni el contenido: solo
**cómo está editado**, para que otra persona pueda editar un vídeo nuevo «a su manera». Lo que saques va a la carpeta
de personalización del creador. Las bases de edición (ritmo, zooms, planos de recurso) ya existen y NO se cambian:
aquí interesa lo **propio del creador**.

Todo en español de España. No ves movimiento ni oyes: trabajas con fotogramas y con los datos de audio ya medidos.
Dilo así cuando algo no lo puedas comprobar («no comprobado»), no lo inventes.

## Material (ya calculado; NO lo recalcules)

Carpeta de trabajo: `C:/Users/Lucas/Desktop/Horizontal/personal/reinoselva/refs/`
- Vídeo: `<VIDEO>.mp4` (1280×720). Título y fecha en `VIDEOS.tsv`.
- `_analisis/<VIDEO>/hojas/`: `intro_NN.jpg` (primeros 60 s, denso), `min_NN.jpg` (una hoja por minuto), `final_NN.jpg`.
- `_analisis/<VIDEO>/cortes.json`: cortes detectados (tiempos). `transcripcion.json`/`.txt`: lo que se dice, con tiempos.
- `_analisis/<VIDEO>/audio.json`: por tramos, nivel de voz y de música (stems ya separados), entradas y salidas de
  música, transitorios (posibles efectos de sonido).
- Método general de medida (léelo antes de empezar, es corto):
  `C:/Users/Lucas/Projects/skills/edicion-horizontal/base/refs/dinamicos/_analisis/METODO.md`

Python con OpenCV: `C:/Users/Lucas/Desktop/Horizontal/herramientas/.venv/Scripts/python.exe`. `ffmpeg` y `ffprobe` en el PATH.
Usa Bash (Git Bash). **No uses `drawtext` de ffmpeg** (falla en este equipo). Heredocs cortos; nada de scripts enormes.

## Reglas

- **Poca memoria (16 GB compartidos con otros procesos): un solo ffmpeg a la vez**, nunca en paralelo; nada de demucs,
  whisper ni modelos; fotogramas a 720p o menos. No lances subagentes.
- Escribe solo dentro de `_analisis/<VIDEO>/` (tus fotogramas y hojas, en `_analisis/<VIDEO>/creador/`) y tus dos
  archivos de salida. No toques nada más, no borres nada, no descargues nada, no subas nada, nada de git.
- Mira las imágenes de verdad (herramienta Read sobre los .jpg). Cada dato de la ficha tiene que salir de un fotograma
  que has mirado o de un número de `audio.json`/`cortes.json`/`transcripcion.json`.

## Recursos propios del creador que debes reconocer

- **Intro** (cabecera): clip de ~8 s, vuelo de dron por la selva entre árboles que acaba en una vista aérea de un río.
  El archivo original no tiene sonido. Puede llevar encima logo o título.
- **Outro** (cierre): clip de ~8 s de selva con hojas en primer plano, con su propio sonido.
- **Logo** «Reino Selva» (con y sin letras): puede ir pequeño en la esquina inferior derecha, o en intro y outro.
- **La tortuga** (mascota en pixel-art, verde, de dibujos): sale normalmente **abajo a la derecha** con una **burbuja de
  texto** (bocadillo blanco con borde negro y cola hacia la tortuga, texto negro en mayúsculas, 2–4 líneas) comentando
  un dato, una aclaración o una broma. Animaciones que existen (anota cuál es cada vez; si no encaja, descríbela):
  `andando` (camina contenta), `explicando` (de pie, brazos abiertos), `de_espaldas` (se gira y queda de espaldas),
  `preocupada` (mira arriba, preocupada), `reportero` (con micrófono; hay dos variantes), `cera` (con esponja o pastilla
  amarilla, frotando), `observando` (con prismáticos, sorprendida), `encogiendo_hombros` (señala o se encoge de hombros),
  `buceando` (con tubo de buceo y burbujas).
- **Botones de YouTube** (suscríbete, me gusta, campana): animaciones de pantalla verde superpuestas.

## Qué hay que sacar

1. **Estructura del vídeo**: gancho o tráiler inicial (qué dura, qué enseña), dónde entra la **intro** (segundo exacto,
   qué va antes y después, si lleva logo, título o texto encima, si la música cambia ahí: míralo en `audio.json`),
   secciones, cierre y **outro** (segundo exacto, qué lleva encima: pantalla final, logo, texto, vídeos sugeridos).
2. **La tortuga: TODAS sus apariciones.** Para cada una: `t0`, `t1` (segundos, afinando a ±0,2 s con fotogramas
   seguidos), animación, **texto literal de la burbuja**, posición y tamaño en pantalla (en % del ancho y alto del
   cuadro: caja de la tortuga y caja de la burbuja), cómo entra y sale (corte seco, se desliza, aparece la burbuja
   después que la tortuga…: mira fotogramas a 0,1 s en la entrada y la salida), qué se está diciendo en la voz en ese
   momento (cita de la transcripción) y **tipo de comentario** (dato curioso, aclaración o corrección, nombre de
   especie, broma o reacción, aviso, llamada a suscribirse, otro). Mira también si coincide con un transitorio de
   `audio.json` (efecto de sonido al aparecer).
   Para no saltarte ninguna, repasa el vídeo entero con hojas del cuadrante inferior derecho a 1 fotograma por segundo:
   `ffmpeg -nostdin -v error -y -i <VIDEO>.mp4 -vf "fps=1,crop=640:360:640:360,scale=192:108,tile=10x6" -q:v 3 _analisis/<VIDEO>/creador/bd_%02d.jpg`
   (cada hoja = 60 s, de izquierda a derecha y de arriba abajo). Luego confirma cada aparición con fotogramas a tamaño
   completo. Guarda un fotograma completo de cada aparición en `creador/tortuga_<mm-ss>.jpg`.
3. **Rótulos y textos**: tipos (título, nombres de especie, cifras, aclaraciones, subtítulos), fuente parecida, color,
   borde o caja, posición, tamaño (% del alto), animación de entrada si se aprecia, cuántos por minuto.
4. **Música**: en qué tramos hay música y en cuáles no (de `audio.json`), % del vídeo con música, nivel respecto a la
   voz, cuántas pistas distintas parece haber, y qué tipo de música dirías por contexto (lo que no puedas saber del
   género, di «no comprobado»). Si la intro y el outro tienen música propia.
5. **Efectos de sonido**: transitorios de `audio.json` que coinciden con cortes, rótulos o apariciones de la tortuga;
   cuántos por minuto.
6. **Ritmo y planos**: duración media y mediana de plano, % de voz a cámara frente a planos de recurso, zooms o
   reencuadres en posproducción (compara fotogramas del mismo plano), transiciones (corte seco, fundidos…),
   velocidades (cámara rápida o lenta), pantalla partida, imágenes o vídeos de archivo insertados.
7. **Botones y llamadas**: suscripción, me gusta, campana: segundo, qué botón, posición, tamaño, duración.
8. **Logo o marca de agua** fijo: dónde, tamaño, todo el vídeo o a ratos.
9. **Color y formato**: bandas, viñeta, filtros evidentes, subtítulos incrustados.

## Salida

1. `C:/Users/Lucas/Desktop/Horizontal/personal/reinoselva/refs/<VIDEO>.json` con esta forma (campos vacíos si no hay):
```json
{"video": "<VIDEO>", "titulo": "", "duracion_s": 0,
 "estructura": {"gancho": {"t0": 0, "t1": 0, "que": ""}, "intro": {"t0": 0, "t1": 0, "antes": "", "encima": "", "audio": ""},
                "secciones": [{"t0": 0, "titulo": ""}], "outro": {"t0": 0, "t1": 0, "encima": "", "audio": ""}},
 "tortuga": [{"t0": 0, "t1": 0, "animacion": "", "texto": "", "tipo": "", "voz": "", "caja_tortuga_pct": [0, 0, 0, 0],
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
   («la tortuga sale cada X min, siempre cuando…, con frases de N palabras…»).

Tu respuesta final: 15 líneas como mucho con lo esencial (intro y outro, nº de apariciones de la tortuga y cuándo las
usa, música, botones) y lo que no has podido comprobar.
