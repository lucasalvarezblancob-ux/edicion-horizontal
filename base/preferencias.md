# Preferencias ESTÁNDAR — las bases de edición (valen para todos los vídeos horizontales)

**Estándar mínimo de `edicion-horizontal`.** Son las bases: salen de las referencias medidas y de las correcciones de
Lucas, autor de la skill, y solo él las cambia. Donde una regla dice «Lucas», léelo como **el creador que edita en esta
carpeta**. **Lo que el creador tenga en su carpeta de personalización (`personal/`) manda sobre estas reglas** cuando
chocan, salvo COLOR (que el bruto no se toque es el estándar; si quiere otra cosa, la pide en ese vídeo).

Los números de ritmo, zooms, textos y mapas, con su origen, están en `base/refs/dinamicos/CONTEXTO.md`; aquí va la regla.
`ramon` = el primer edit de prueba (23 min, 11 brutos Sony 4K 25 fps, hablado en inglés); su código está en
`base/ejemplos/ramon/` (sin media).

Formato: `- AAAA-MM-DD — regla. Por qué. (vídeo)`. Si una regla nueva contradice otra, sustituye la vieja.

## ⚠️ COLOR — regla fija (heredada de reels; manda sobre todo lo demás)
- **El color del bruto NO se toca nunca, salvo que el creador lo pida expresamente en ese vídeo.** Prohibido por
  defecto: etalonado, gamma, curvas, contraste, brillo, saturación, viñeta, LUT creativas y «mejorar» por iniciativa
  propia. Por qué: «que se mantenga, nada de tocarlo a no ser que te lo diga».
- **Bruto SDR (Sony y la mayoría de cámaras): no pasa por ningún proxy.** El paso 4 monta desde el archivo original con
  ffmpeg, sin filtros de color, y etiqueta la salida bt709 limitado. Medido en `ramon`: 0,3–0,7 niveles de diferencia
  media con el bruto.
- **Bruto HDR (iPhone HLG/PQ): se convierten a SDR SOLO los trozos que usa el montaje**, con
  `herramientas/montaje/sdr.py` (desde `out/<slug>/`, después de `paso3_plan.py`; `paso4_render.py tramos` lo llama
  solo si falta algo). Deja `trabajo/sdr/<clip>/<a>_<b>.mp4` (libplacebo, x264 CRF 14, a los fps del proyecto) y todos
  los pasos leen la imagen con `comun.fuente()`, que elige el original (SDR) o la copia (HDR); el sonido sale siempre
  del original. Vale igual para los clips de archivo del creador que sean HDR. **Nunca `zscale` + `tonemap` a mano**
  (sale ~20 niveles más claro y cálido). Por qué por trozos: convertir los brutos enteros cuesta ~2 s por segundo de
  bruto en 4K; en `1311` (83 min de iPhone 4K 60 fps) habrían sido unas 3 h y se convirtieron 151 trozos (24 GB) en
  una fracción. `herramientas/proxy.sh` (el bruto entero; en macOS, avconvert + `hdr-pantalla.cube`) queda para
  cuando se quiere un archivo SDR suelto. Medido en `1311`: +0,3 a +1,2 niveles las copias y +0,8 a +1,1 el render.
- **Comprobación obligatoria, dos veces**: una copia SDR de cada bruto HDR contra el bruto antes de montar
  (`comparar_color.sh BRUTO trabajo/sdr/<clip>/<a>_<b>.mp4 "<t>" <a / FPS>`), y el render contra el bruto antes
  de entregar. macOS: QuickTime en el mismo instante + captura. Windows/Linux: `herramientas/comparar_color.sh` (mpv,
  `winget install shinchiro.mpv`). Diferencia media ≤ 5 niveles en zonas sin texto ni movimiento. Un fotograma sacado
  con ffmpeg de un bruto HDR no vale como referencia. Di el resultado al entregar.
- **Etiquetas**: todo lo que sale va `bt709/bt709/bt709`, rango `tv`, `yuv420p`. Si un bruto viene etiquetado
  `iec61966-2-4` (xvYCC, lo hace la Sony), el concat sin recodificar hereda la etiqueta: el paso `unir` la corrige con
  `-bsf:v h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1`. Comprueba el archivo final con ffprobe.
- Las capas de Remotion se renderizan aparte (ProRes 4444 con alfa, `remotion.capas.config.ts`) y solo llevan gráficos:
  el vídeo nunca pasa por Chrome, así que Remotion no puede cambiarle el color.
- Plano muy claro con texto encima que no se lee → sombra más fuerte en el texto o moverlo; bajar la exposición de ese
  plano solo si el creador lo pide.

## Marca y estilo
- Acento, canal y @: `personal/<creador>/marca.json`; fuentes: `estudio/src/comun/marca.ts` (todo local). De serie: amarillo-lima
  `#E6EC52`, **Unbounded 900** para todo lo grande, **Lexend** para lo pequeño. Nada de rosa. Un solo acento y una
  familia grande por vídeo.
- **Color por función**: acento = dato, número, énfasis; blanco = información; blanco en minúsculas entre *asteriscos* =
  comentario del editor. Contorno negro + sombra corta; sin cajas ni pastillas.
- **Idioma: el del vídeo, SIEMPRE detectado del audio** (`paso0_preparar.py` lo imprime por bruto), nunca supuesto por el
  nombre del creador, el país ni el idioma en que te escriben. Transcripción, rótulos, título, capítulos y descripción
  van en ese idioma. Por qué: «ten en cuenta el idioma del vídeo siempre» (el primer bruto estaba en inglés y Lucas
  escribe en español). (ramon)

## Ritmo, cortes y zooms
- 2026-11-11 — **Dinamismo con juego de escala.** A cámara, un cambio visual cada 2,5–4,5 s: corte de escala DE GOLPE en
  un límite de frase, escalas alternas ×1,0 ↔ ×1,12–1,5; frase fuerte ×1,65 mientras dura (1–2 por minuto); pocos zooms
  animados (entrada rápida con frenada). **Nada de zoom lento sostenido.** Lo hace `dinamica.py`; lo elegido a mano va en
  `FUERTES` y `ENTRADAS` de `plan.py`; el gusto de cada creador, en `personal/<creador>/ajustes.py`. Objetivo en vídeo hablado:
  mediana de plano ~2,2 s y 22–27 cambios/min. Por qué: «no me parecen lo suficientemente dinámicos, falta algo de juego
  con zooms y cortes» (refs: Plex, Grefg, Xokas, Lucas Valero). (ramon v1 → v2)
- 2026-11-11 — **Los zooms tienen que apuntar bien.** Un punch-in contiene la cara durante TODO el plano (no vale centrar
  en la mediana si la persona se mueve); si no cabe, se cierra menos. Con detección de cara floja (< 85 % de muestras),
  máximo ×1,2 y centrado. Un zoom a un objeto o animal lleva su centro a mano (`(zoom, cx, cy)`) y se comprueba con
  `ver.py`. Por qué: había zooms que acababan en una pared. (ramon v2)
- **Se corta por el texto, no por tiempos.** El EDL elige cada frase por su texto literal en la transcripción y
  `paso1_alinear.py` afina los bordes con alineación forzada (los tiempos de Whisper van ~0,17 s adelantados, hasta
  0,8 s). Después `comprobar_voz.py`: ratio ≥ 0,97 y ninguna palabra comida o repetida en un borde.
- 2026-11-14 — **Las frases, ENTERAS: no se corta a media frase.** Una pieza `T(…)` empieza donde empieza la frase (con
  su sujeto, su «hay que…», su «vamos a…») y acaba donde acaba (con su remate, su verbo, su «porque…» si lo lleva).
  El fallo típico es copiar de la transcripción solo el trozo «bueno» y dejar fuera dos palabras de delante o la
  coletilla de detrás: en el vídeo suena cortado («…que mirar que no haya nadie» por «hay que mirar…»; «a meter aquí
  la pala» por «vamos a meter…»; «porque no va a invadir…» sin lo que explica; una frase que acaba en «para que»).
  Se comprueba SIEMPRE con `frases.py` (después de `paso1_alinear.py`): enseña cada pieza con lo que se dice justo
  antes y justo después en el bruto y si hay pausa real en el corte, y avisa de las que arrancan con una palabra que
  cuelga de lo anterior (porque, que, y, además, a…) o terminan en una que pide continuación (que, para, de, y…).
  Cada aviso se lee y se resuelve: **alargar hasta el borde de la frase** (lo normal), dejarlo si lo de fuera es
  muletilla o retoma y lo de dentro se entiende solo (se apunta en `OK_A_MEDIAS` del `edl.py` con el porqué), o quitar
  la pieza. Solo valen golpes sueltos en el **tráiler**, y aun así cada uno tiene que entenderse solo. Tampoco se
  empalman dos mitades de frases distintas para «fabricar» una. Si el creador se interrumpe él mismo (le corta el
  perro, se le cae algo), eso no es un corte: es el momento, y se deja con lo que pasa después.
  Por qué: Lucas, «y hay veces que cortas frases a medias» (v1 de `1311`: de 113 piezas de habla, una docena
  empezaban o acababan a media frase). (vídeo: 1311)
- Fuera: retomas, muletillas largas, esperas, colocar la cámara. Dentro: reacciones, risas y los silencios que cuentan,
  y **todo lo que le da toque al vídeo** (ver «Que el vídeo lo cuente todo»).
- Límite de calidad: con bruto y salida a la misma resolución todo punch es ampliación. Hasta ×1,3–1,4 no se nota;
  ×1,6–1,7 solo en golpes cortos; más de ×2 solo para un detalle que lo merezca.
- No se monta a ritmo de la música, salvo ráfagas y montajes sin voz.
- 2026-11-14 — **Vídeos lo más dinámicos posible, SIEMPRE, y una versión nueva nunca menos dinámica que la anterior.**
  Al alargar un montaje (más frases, más toque) el dinamismo no se diluye: se mide y se iguala o se supera, antes de
  renderizar, con `paso3_plan.py` y `video.json` frente a la versión anterior (o, en un vídeo nuevo, frente a los
  objetivos de aquí):
  - cortes por minuto (≥ 22–27) y mediana de plano (≤ ~2,2 s);
  - **% del tiempo con texto o gráfico en pantalla** (rangos de gráficos ÷ duración; en Reino Selva, ≥ 20 %);
  - planos de archivo por minuto sobre las menciones (especie, recinto, el pasado, el perro…);
  - **huecos sin ningún texto de más de ~25 s**: se buscan (rangos de `video.json`) y en cada uno se rotula lo que da
    juego en ese tramo (una salida graciosa, una reacción, la idea del momento, un aparte al perro), con su timing medido.
  Por qué: Lucas, al pedir la v2 de `1311`, «la v2 tiene que ser igual de dinámica a ser posible, eso siempre, vídeos
  lo más dinámicos posibles». La v2 (22 min, con todo el toque) cortaba igual que la v1 (27,7 frente a 26,8 cortes/min),
  pero tenía texto solo el 14 % del tiempo frente al 20 % de la v1, con huecos de hasta 94 s sin nada: se añadieron 45
  textos y 3 planos de archivo hasta el 20,1 %. (vídeo: 1311)

## Orden y continuidad
- 2026-11-12 — **Un plano de desplazamiento (andar, bajar escaleras, entrar, conducir) va en el momento del vídeo en que
  ocurre ese desplazamiento**, nunca como «transición genérica» en otro cambio de sección. Un clip sin habla se sitúa por
  **orden de grabación** (número de archivo y hora) y por lo último que se dijo antes de él: si el bruto anterior acaba
  en «vamos a la várzea» y el siguiente empieza ya en la várzea, el clip de en medio ES la bajada a la várzea. Por qué:
  «cuando baja las escaleras va justo en el momento que baja a la várzea, no después… lo has pasado al punto 6». El
  fallo: se trató el clip como un «paseo» suelto y se colocó en el siguiente cambio de sección. (ramon v3 → v4)
- **Antes de escribir el EDL, la cronología**: lista de brutos en orden de grabación con dónde está el creador en cada
  uno, de dónde viene y a dónde dice que va (`paso0_preparar.py` da la tabla; el registro visual, el campo
  `desplazamiento`). Si se cambia el orden de las secciones respecto al rodaje, los desplazamientos se quedan con SU
  trayecto o no se usan.
- **Continuidad**: un recurso o un plano de acción no puede enseñar un sitio, una ropa o una luz que contradiga el
  momento en que se pone (el creador aparece en un sitio al que aún no ha llegado).
- Al mover una pieza del EDL, revisa todo lo que cuelga de su marca (ventanas de música, recursos, rótulos).

## Que el vídeo lo cuente todo (repaso de descartes)
- 2026-11-12 — **Antes de dar un montaje por bueno, repasa TODO lo que se ha quedado fuera.** Al escribir el EDL se
  eligen frases y se descarta más de la mitad del bruto; ahí se pierden cosas buenas sin darse cuenta. Después de
  `paso3_plan.py`: `descartes.py` → `trabajo/descartes.md` (cada tramo de habla que no suena en el vídeo, marcado
  NUEVO si no se parece a nada de lo que sí suena, y cada «mejor recurso» del registro visual que no sale). **Se lee
  entero**, y cada NUEVO se mira con su contexto (qué se dice justo antes y después).
- **Qué se busca** (lista viva: se afina con cada «sí» y cada «no» de quien edita, abajo):
  - el **porqué** de algo que el vídeo afirma sin explicar (la causa, el mecanismo, «porque…»);
  - una **anécdota** o historia con principio y final (cómo pasó algo, un error, un susto);
  - un **chiste**, una salida graciosa o un momento con un animal o una persona que hace gracia, y su plano;
  - una **frase con fuerza** (rotunda, emocionante, que valdría para el tráiler);
  - un **ejemplo concreto**: el nombre de una especie, un sitio, una cifra, una comparación;
  - **qué va a pasar**: planes, lo próximo que hará, el vídeo que anuncia;
  - un momento **sincero** (lo que cuesta, lo que sale mal, una confesión);
  - **imagen**: un «mejor recurso» sin usar, un animal haciendo algo, una acción que abre o cierra una escena.
  No es recuperable: retomas y la misma idea dicha otra vez, arranques, instrucciones al cámara o al editor, y lo que
  se dice sin que se vea nada que lo sostenga.
- 2026-11-14 — **Lo que le da TOQUE al vídeo se queda, desde el primer EDL.** El toque es la personalidad del creador:
  el humor y las salidas, lo que le dice al perro, al animal o a quien graba, las reacciones (un «¡guau!», un susto,
  un «pobrecilla»), las anécdotas, las explicaciones y los porqués, lo que siente por lo que hace (le sabe mal
  estropear una planta, se alegra de salvarla), las manías y las frases con gracia aunque «no hagan avanzar» el
  vídeo. **Eso no es relleno ni charla de rodaje: es el vídeo.** Solo se corta: la retoma, el arranque, la misma idea
  dicha otra vez, el tiempo muerto, las instrucciones a quien graba o edita y lo privado (terceros con nombre,
  llamadas, datos personales). **La duración no es motivo** para quitar nada de lo otro, ni hay que apretar hacia un
  vídeo corto: se monta con lo que hay de bueno y sale lo que salga (dentro de lo que publica el creador).
  Regla de mano al escribir el EDL: ante la duda entre dejar una frase con gracia o quitarla, **se deja**.
- **El repaso de descartes es para cazar lo que se escapó, no para aplazar decisiones.** Si al leer
  `trabajo/descartes.md` algo «a lo mejor no se tenía que haber descartado», ya está decidido: **se mete antes de
  renderizar** y no se le presenta a quien edita como «descarte». Al entregar se le cuenta qué entró en ese repaso y
  qué se ha dejado fuera a propósito y por qué (lista corta). **Se pregunta antes solo lo de verdad dudoso**: lo que
  toca a terceros o a su vida privada, promociones, lo que deja mal al creador, o lo que cambia la estructura del
  vídeo. Él dice sí o no; entonces se aplica.
  Por qué: Lucas, tras la v1 de `1311` (13:55, un tercio de lo hablado; en la lista de descartes iban cuatro momentos
  que yo mismo marcaba como buenos): «añade todo lo que has descartado, y no descartes tanta cosa, que son cosas
  interesantes, que le dan su toque a los vídeos; está bien descartar, pero tienes que aprender que lo que le da toque
  al vídeo tiene que quedarse; de hecho me lo has presentado como "descarte" ya sabiendo que a lo mejor no se tenía
  que haber descartado». El fallo fue triple: montar apretando hacia un vídeo corto, tratar la personalidad como
  relleno, y escudarse en «no meter nada sin preguntar» con cosas que ya se sabía que valían. Esta regla sustituye a
  la de 2026-11-12 («lo que falte no se mete por cuenta propia»), que queda solo para lo dudoso. (vídeo: 1311)
- 2026-11-14 — **Sin pasarse al otro lado: lo que sí sobra, sobra.** Meter el toque no es meterlo todo. Se siguen
  cortando la **narración de colocación** («esta la voy a poner aquí… no, aquí»), la **logística** (ir a por la pala,
  buscar la manguera), la **misma idea dicha otra vez** y las retomas, aunque estén enteras y bien dichas. Orientación,
  no tope: un vídeo del creador que pasa de unos 13 min a 28 por meter el toque se ha pasado; lo que queda sin logística
  ni repeticiones ronda los 20–22 min (de 83 min de bruto en `1311`). Si al meter el toque la duración se dobla, se
  repasa el EDL buscando colocación, logística y repeticiones antes de enseñarlo.
  Por qué: Lucas, al ver la versión intermedia de la v2 de `1311`: «¿cómo ha pasado la v2 de 13 min a 28? ¿No es
  demasiado?». Se dejó en 22:20 quitando eso, sin tocar humor, reacciones ni explicaciones. (vídeo: 1311)
- **Cada decisión se apunta** (aquí si vale para todos; en `personal/<creador>/preferencias.md` si es de su gusto), con
  el tipo de momento y el porqué, para detectar mejor la próxima vez.
  Por qué: Lucas, «revisa siempre que el vídeo cuente todo lo importante, que no quede nada eliminado de tomas… y si
  detectas que falta algo, me dices antes de ponerlo, para yo decirte si sí o si no, y así lo aplicamos a la skill
  general, que sepa mejor detectar todas las partes interesantes, buenas, graciosas, impactantes». Y por qué hacía
  falta: en `ramon` se usó el 45–65 % de lo hablado de cada bruto y nadie había repasado el resto. (vídeo: ramon)
- **Decisiones de Lucas sobre descartes** (para aprender qué entra y qué no):
  - 2026-11-12 (`ramon` v6 → v7; lista de 17, alargó el vídeo de 16:46 a ~18:40 y no le importó: **la duración no
    es motivo para dejar fuera algo bueno**). Literal: «añade todo menos el 11, el 12, 13, 14. Apunta qué tipo de
    cosas no hay que excluir… el 16 y 17 los quiero dentro».
  - **SÍ entra (no lo vuelvas a excluir):**
    - la **frase rotunda** que abre un bloque («…once it is built, there's no way back»);
    - el **chiste con un animal** y SU plano (el perro mirando a las tortugas: «he's also not having the fun that
      tortoises have»): sin el plano no hay chiste, van juntos;
    - la **anécdota de cómo pasó algo** (las medakas entraron con una planta que cambió de estanque);
    - el **porqué** de una afirmación que el vídeo dejaba sin explicar (por qué la tortuga rusa acabará siendo rara:
      las crían cogiendo huevos del campo);
    - **planes y vídeos anunciados** (va a criar grillos y lo enseñará) y **lo que significa en concreto** una
      decisión (qué especies caben al abrir el bioma, qué peces podrá meter);
    - el **ejemplo concreto** de especie al explicar algo general (la rana de ojos rojos al hablar del Chocó);
    - el **plan para el animal protagonista** de un capítulo (qué será de él en verano);
    - una **curiosidad breve aunque no haya imagen** (las ranas se han enterrado hasta el año que viene): si son 5–8 s
      y cierran una idea, entran a cámara;
    - la **salida graciosa** sobre un nombre («we called it bunker… it's not a bunker, it's a den»);
    - la **acción que abre una escena** (abre con llave la puerta del bioma antes de «I've got good news»);
    - los **«mejores recursos» sin usar**, para tapar voz que ya estaba (16 y 17 «los quiero dentro»).
  - 2026-11-14 (`1311` v1 → v2; el vídeo pasó de 13:55 a bastante más y era lo que quería). Literal, arriba. **SÍ
    entra, y desde el principio** (todo esto se había quedado fuera en la v1):
    - los **apartes al perro o al animal** que se mete en medio («déjame, pesado», «Ragnar, stop», «deja la tortuga,
      tío», «¿las vas a destrozar o no?») y lo que pasa con él a lo largo del día (le roba un calcetín, hay que
      quitárselo para que no se lo trague): es el **hilo cómico** del vídeo, se sigue entero;
    - el **cuidado por los animales y las plantas** («hay que mirar siempre, cuidar bien con los animales», «me sabe
      mal fastidiar plantas que ya están enraizando», «a esta la hemos salvado», «pobrecilla», «reanimación»);
    - la **explicación completa** de algo que el vídeo dejaba a medias (la luna creciente y decreciente cada quince
      días, después de nombrar el calendario biodinámico);
    - las **frases con gracia o de carácter** («eficiencia pura», «¿por qué? porque sí», «como ya tengo una edad», «con
      esto te pones fuerte», «a por el gordo, el gordo de Navidad», «el que mejor se lo pasa aquí es el que me graba,
      que le gusta verme sufrir»);
    - las **reacciones** a lo que sale bien o mal («toda de una, ¡guau!», «no había ni enraizado, sorprendente», «no
      entiendo nada») con su imagen;
    - los **consejos y avisos** de pasada («con estos zapatos no recomiendo que hagáis nada», «lo pondré veinte
      minutos a regar», «echarle ese abono») y lo que **anuncia** que hará o explicará;
    - las **pequeñas derrotas** («un pequeño fallo, la voy a intentar rescatar», «no me quiero mojar los pies otra vez»).
    Fuera se quedó solo lo privado: una pregunta sobre el examen de un familiar y una llamada de teléfono.
  - **NO entra** (los cuatro que quitó en `ramon`; el motivo no lo dijo, la lectura es mía):
    - hablar del **dinero** que le cuesta («a lot of money that I am putting in here»);
    - hablar de su **poca audiencia** o de cómo va el canal («I don't have much audience in English»);
    - **promoción** de otro canal y **calendario** de episodios («check my Spanish channel», «every week»): eso va en
      la descripción, no en el montaje;
    - una **explicación en la que duda o no recuerda el dato** (la diferencia entre dos especies cuyo nombre no le
      sale): resta autoridad y no enseña nada.
    Mi lectura: fuera lo que habla del canal y del negocio en vez del tema, y lo que deja al creador en mal lugar.
    Si en otro vídeo dice que sí a algo de esto, corrige esta lista.

## Planos de recurso (sobre la voz)
- 2026-11-11 — **Un recurso tiene que enseñar aquello de lo que se habla desde su primer fotograma.** Nada de paredes,
  barridos de cámara, arranques de plano ni el sujeto diminuto. Por qué: «elige los planos de recurso con criterio» (en
  la v2 había recursos donde solo se veía pared). (ramon v2 → v3)
- **Antes de montar, registro visual de TODOS los brutos** (qué se ve en cada segundo): hojas densas del paso 0 + un
  agente por bruto con `herramientas/montaje/ENCARGO_REGISTRO_VISUAL.md`, **de dos en dos** con 16 GB de RAM. Sin
  registro no se eligen recursos. Por qué: «estudia a fondo los brutos».
- Se eligen de `mejores_recursos` del registro, **se miran** (`tira.py`) y, con el plan hecho, **se revisan todos** con
  `hoja_recursos.py` antes de renderizar. Si el sujeto queda pequeño, zoom al sujeto; si no hay imagen de algo que se
  nombra, **no se inventa**: se queda el plano a cámara (con texto o zoom) y se le dice al creador qué falta (foto de
  banco, grabación suya).
- Duración 1,5–4 s; si pasa de ~3 s, corte de escala a la mitad. No se repite un tramo en el mismo vídeo.
- 2026-11-12 — **Lo que se nombra y no está en los brutos del día se tapa con archivo, cuando lo haya.** El pasado
  («cuando empezamos a construir…»), otra época del año, una especie, un sitio, una planta: si en sus `recursos/` hay un
  clip clasificado de eso, va sobre su voz en el momento en que lo nombra (1,5–4 s, como cualquier recurso), aunque
  haya plano a cámara que valga. Da ritmo y enseña lo que se cuenta. Cómo se busca y qué hacer si no lo hay:
  `base/recursos.md` § 5. Por qué: Lucas, «habla del pasado de cuando empezaron la construcción…, de los peces, de
  la várzea, de plantas… en un futuro en recursos habrá vídeos de todo eso clasificados, para que puedas ir poniendo
  planos de vez en cuando cuando los menciona, con su voz de fondo, para que sea también más dinámico». (vídeo: ramon)
- 2026-11-13 — **Todo recurso es de un creador**: sus fijos, sus clips de archivo y b-roll, fotos, mapas y música van
  en `personal/<creador>/recursos/`, **ordenados por carpetas de tema como en `edicion-reels`** (nada suelto, todo con
  ficha en su `INDICE.md`); no hay `recursos/` en la raíz. Por qué: Lucas, «los recursos tienen que ir ligados a la
  personalización; recursos estará dentro del perfil de creador» y «se tienen que ordenar por carpetas como hacíamos
  en los recursos de la skill de reels».
- Material de `personal/<creador>/recursos/`: cómo catalogarlo y elegirlo, en `base/recursos.md`. Los recursos fijos del
  creador (cabecera, cortinillas, logos) y cuándo van: `personal/<creador>/recursos.md`.

## Textos y gráficos
- 2026-11-11 — **Guía: Plex y Xokas.** Una familia ancha y negra para lo grande; entran de golpe (pop en 5–6 f) y salen
  por corte; pocos y con función. Tipos de serie (`estudio/src/comun/Graficos.tsx`): título, capítulo (n/total), cifra
  junto a la cara, palabra-golpe, nota del editor, rótulo con seguimiento, subtítulo. La suscripción no es un rótulo:
  es un botón animado (abajo, «Clips y gráficos superpuestos»).
- 2026-11-11 — **Texto que crece: zoom continuo y suave, nunca a escalones.** Pop de entrada y luego ×1 → ×1,22 con
  frenada. Por qué: «se zumea a trozos, no es suave». (ramon v2)
  - 2026-11-14 — **La escala de un texto nunca baja: ni rebote al entrar ni pasarse de tamaño.** El pop de entrada va de
    ×0,86 a ×1 frenando hasta parar (`pop()` en `Graficos.tsx`) y por encima solo sigue el crecimiento continuo. Por qué:
    Lucas, «los textos grandes aún parece que rebotan un poco al aparecer: aparecen, se encogen un poco y luego se
    zoomean». Causa: el pop antiguo (×0,8 → ×1,06 → ×1) se multiplicaba por el crecimiento, que en esos 6 fotogramas sube
    un 1 %: el texto se encogía un 5 % justo después de aparecer. Al arreglar lo de los escalones se miró el crecimiento y
    no la entrada. Cualquier animación de escala nueva (también en los gráficos de un creador): monótona. (vídeo: 1311)
- **Nunca un texto antes de que se diga.** Todo cuelga de anclas (frase o marca), no de frames a mano; compruébalo con
  `timing_textos.py` (abajo, «Timing de los textos») y con `ver.py` en el frame anterior y en el de la palabra.
- **Subtítulos solo donde se oye mal** (ruido, viento, voz lejana, otro idioma): abajo, una línea, 3–6 palabras, de
  golpe. Nunca continuos. Los tramos se proponen con la transcripción (palabras con poca confianza, frases que Whisper
  no entiende) y, como Claude no oye, **se confirman con el creador**.
- **Nombres, cifras y especies: literales.** Lo que no salga en la transcripción o no te lo haya dicho el creador
  (nombres científicos, datos) va marcado como pendiente de validar. Las **notas del editor** son propuestas: se le
  enseñan antes de darlas por buenas.
- Nada tapa la cara ni el sujeto. En los últimos 20 s deja libres las zonas de las tarjetas de YouTube si hay pantalla final.

### Timing de los textos (cuándo entra y cuándo se va cada uno)
- 2026-11-12 — **Cada texto entra EN su palabra, aguanta la frase que resume y sale con el corte.** Se mide, no se
  estima: después de `paso3_plan.py`, `timing_textos.py` (desde `out/<slug>/`) enseña cada texto frente a la voz (el
  desfase de cada palabra respecto a la entrada del texto) y a los planos que tiene debajo, con avisos. Se arregla en
  `plan.py` y se repite hasta que los avisos que queden sean a propósito.
  - **Entra en la palabra que escribe**, no al principio de la frase: el ancla es ESA palabra (`"siebenrocki"`, no
    `"the name is siebenrocki"`; `"iberian pond"`, no `"an iberian pond"`). Una décima no se nota; medio segundo antes,
    sí, y además le pisa el remate a quien habla. Un nombre que no se dice (el científico) entra con el nombre común.
  - **La segunda línea, cuando se dice.** Si la línea pequeña repite algo que él dice un par de segundos después
    («FLOODED» … «after very heavy rains»), entra con su propio retraso (en el rótulo de un creador, p. ej. `subEn`) y
    el texto aguanta hasta que acaba de decirlo. Si es solo el pie de un nombre (nombre común), entra con él.
  - **Aguanta la frase.** Si al irse el texto a la frase le quedan una, dos o tres palabras, se alarga hasta la pausa.
    Y no se va antes de que se diga algo que lleva escrito («…or a whole life» se iba justo al decir «life»).
  - 2026-11-14 — **Ningún texto se va antes de que se haya DICHO entero y se pueda leer.** Aguanta hasta 0,5 s después
    de su última palabra (o hasta la pausa) y nunca menos que el tiempo de leerlo: 0,6 s + 0,3 s por palabra, mínimo
    1,2 s. Lo hace solo `paso3_plan.py` (`comun.texto_dicho`: casa las palabras del texto con la voz, en orden) e
    imprime lo que alarga; `timing_textos.py` avisa con `CORTO` si el texto siguiente no le deja sitio. Por qué: Lucas,
    «aparecen en buen timing pero desaparecen antes de que la persona acabe de decirlo, por lo que no te da tiempo ni a
    leerlo». Causa: la duración de cada texto se ponía a ojo en `plan.py` (0,8–1,6 s para un golpe) y la comprobación
    solo miraba la entrada y si a la frase le quedaban 1–3 palabras, no si el propio texto ya se había dicho. En la v3
    de `1311` hubo que alargar 64 de los 103 textos (de +0,1 a +2 s). (vídeo: 1311)
  - **Con los cortes.** Un texto acaba en un corte o pisa el plano siguiente medio segundo o más; nunca 1–7 fotogramas
    de cola, ni se va 3 fotogramas antes del corte (esto lo ajusta solo `paso3_plan.py`). Y no se queda encima de un
    recurso que enseña OTRA cosa (los nombres de dos tortugas sobre un plano de obra): se acorta o se mueve el recurso.
  - **Cifra junto a la cara:** su plano corta en el número («three eggs per season»), no en la muletilla de antes
    («up to…»): el corte de escala en la cifra es el golpe.
  - **Comentario del editor: DESPUÉS de lo que comenta.** Es una reacción; si sale antes del remate, lo destripa
    («*humans: not thriving*» salía 0,9 s antes de que dijera «humans»).
  - **Gráficos que tardan en leerse** (una mascota que asoma y luego saca la burbuja): lo que tiene que caer en la
    palabra es el momento en que el texto SE LEE, no el arranque de la animación. En `plan.py`,
    `RETARDO_TEXTO = {"tipo": segundos}` para que la herramienta lo cuente.
  - **Tiempo de lectura:** como mucho 4 palabras por segundo en pantalla. Si no cabe, se acorta el texto; no se pone
    más rápido ni se alarga sobre otra idea.
  - **Un gráfico grande se mira en TODOS los planos que pisa:** los cortes de escala cambian el encuadre por debajo
    (una burbuja que con el plano general caía en el pecho, en el corte a ×1,45 le tapaba la boca).
  Por qué: Lucas, «aprovecha para revisar el timing de los textos, a ver si se puede mejorar un poco alguno», «al
  revisar textos, ¿has revisado también el timing de aparición de la tortuga que va apareciendo hablando?» y «el tema
  de los timings, aprende y apúntalo en la skill general». **Por qué fallaba:** cada texto se colgaba de la frase tal
  cual estaba copiada en el EDL (o sea, de su primera palabra), las duraciones se ponían a ojo y `ver.py` solo enseña
  un fotograma: nada medía el texto contra la voz ni contra los cortes. Y las burbujas las di por buenas sin medirlas
  hasta que preguntó. En `ramon` v6 se retocaron 36 de sus 49 textos: «IBERIAN POND» 0,6 s antes de la palabra,
  dos burbujas 2–3 s antes de nombrar al animal, cinco textos con 1–7 fotogramas de cola. (vídeo: ramon v6 → v7)

### Resaltar algo importante dentro del plano (foco)
- 2026-11-12 — **Cuando lo importante se pierde en el plano, se resalta**: todo el cuadro en **blanco y negro (y algo
  más oscuro) menos el sujeto**, que se queda en color dentro de una elipse de borde suave que lo sigue
  (`FOCOS` en `plan.py` + `herramientas/montaje/foco.py`), y/o un **rótulo con flecha** pegado a él (`TRK`). Sirve para
  cualquier cosa importante que el espectador no sabría dónde mirar: un animal pequeño haciendo algo, un detalle, un
  objeto, una persona entre varias, el resultado de algo. Referencia: la intro de «la isla de los monos» de Rubén
  Holgado (`refs/dinamicos/CONTEXTO.md` → gráficos con seguimiento).
  **Con criterio y sin abusar**: uno o dos por vídeo (tres en uno largo), 2–5 s cada uno, y solo donde de verdad no se
  ve; si el sujeto ya llena el plano o basta un corte de escala, no hace falta. Nunca sobre la cara del creador
  hablando, ni dos seguidos, ni como adorno.
  Receta: corte de escala hacia el sujeto (`BROLL` con zoom, partiendo el recurso en abierto → cerrado → abierto) +
  `FOCOS` durante el plano cerrado + `TRK` de 2–3 palabras si hay que decir qué pasa. Con `"en": ancla` el foco sale
  solo en ese plano (el mismo trozo de bruto suele estar también en el tráiler y en la ráfaga). Después de
  `paso3_plan.py`: `foco.py parches` y `foco.py hoja`, y **mira la hoja**: el sujeto entero y en color en todos los
  fotogramas. El color del sujeto no se toca (regla de COLOR): solo se apaga lo de alrededor.
  Por qué: Lucas, «se podría poner una flecha o algo que resalte un poco más al animal comiendo, o blanco y negro todo
  menos la tortuga comiendo… como la intro de Rubén Holgado de los monos (esto último se puede usar en la skill en
  general a lo mejor, con criterio y sin abusar)» y «eso del resalte es para resaltar cosas importantes en general a
  veces, no aplicado solo a una tortuga comiendo». (vídeo: ramon, v6)

### Clips y gráficos superpuestos (botones, mascotas, logos)
- 2026-11-12 — **Nunca se superpone un clip con su fondo, con halo del fondo o con objetos raros.** Los botones y las
  mascotas vienen sobre verde y los logos sobre un color liso: se les quita con `quitar_fondo.py` /
  `quitar_fondo_imagen.py` y se **mira** la hoja de prueba sobre oscuro y sobre claro. Las animaciones generadas traen
  sorpresas (en `ramon`, la tortuga botaba un balón a mitad del clip): mira una hoja con **todos** los fotogramas del
  tramo que vas a usar, no seis sueltos. Por qué: se vio en la prueba de render, no en la hoja de seis fotogramas.
- 2026-11-12 — Un gráfico superpuesto **no tapa la cara ni el sujeto y no pisa otro gráfico** (rótulo, cifra, mapa).
  Compruébalo con `ver.py` en dos momentos: por debajo hay cortes de escala y el encuadre cambia. Si tapa, al otro lado
  (`lado`), más pequeño (`tam`) o un segundo más tarde. Por qué: la burbuja tapaba la boca en un plano con la cara a la derecha.
- 2026-11-12 — **Pedir suscripción, me gusta o campana = botón ANIMADO de la skill, abajo en el CENTRO.** Siempre que
  el creador lo pide con la voz va uno de los 16 botones (`BOTONES` en `plan.py`; catálogo y encaje con la voz:
  `base/recursos.md` § 9), en su sitio de serie. Nunca a un lado, y nunca un texto o un botón dibujado en su lugar.
  Por qué: Lucas, «no seguiste la norma de suscribir, al final pone subscribe en texto en vez de usar lo que te dije» y
  «cuando se ponga suscribir, lo ponemos abajo en medio con las animaciones estas, no en un lado». (vídeo: ramon, v5)
- 2026-11-14 — **El botón de suscribir va solo en pantalla: ningún texto ni gráfico comparte tiempo con él.** El texto
  que caería encima se cuelga de después del botón (la repetición de su frase o la frase siguiente), o el botón se cuelga
  de otra frase. `paso3_plan.py` se para con `CHOQUE: …` si coinciden. Por qué: Lucas, en 8:51 de `prueba-3`, «se
  solapan el botón de suscribir y el texto de "soltar cable"». Causa: el botón se cuelga ~4 s antes de «suscribiros» y
  dura ~8 s, así que pisa la frase de después; el rótulo de esa frase («Soltar cable es mi deporte preferido») cayó
  dentro, los dos abajo en el centro, y nada comparaba los tiempos del botón con los de los textos. (vídeo: prueba-3)
- 2026-11-12 — **El texto de un botón o de una burbuja va en el idioma del vídeo.** Los 16 botones de serie están en
  español: en un vídeo en otro idioma va la versión traducida del botón (`herramientas/boton_idioma.py`; el 2 en inglés
  ya está), no el español ni un texto dibujado. Lo que afirme un texto añadido (un dato de la
  mascota, una nota del editor) tiene que ser **cierto** —se busca o se sabe, y se comprueba— y tiene que ver con **lo
  que se está diciendo en ese momento** o se acaba de decir, no con otra parte del vídeo. Por qué: Lucas, «tienen que
  ver con lo que habla en el momento que lo pone».

## Mapas
- 2026-11-11 — **Mapa de satélite animado** cuando se nombran regiones, países o rutas: la cámara vuela a la zona, el
  borde se dibuja, llega el relleno y salta la etiqueta; las regiones anteriores quedan encendidas más tenues. Nada de
  mapa vectorial plano con fundidos. Por qué: «la animación del mapa no me gusta» (v1) → el de satélite gustó y «va a la
  skill». Base con `herramientas/mapa_satelite.py` (NASA Blue Marble, dominio público) → `personal/<creador>/recursos/mapas/`; componente
  `estudio/src/comun/MapaSatelite.tsx`; ejemplo en `base/ejemplos/ramon/Capas.tsx`. 3–6 s, solo cuando sitúa.

## Audio
- **La voz del bruto es el audio.** Proceso mínimo: paso alto suave y ganancia; sin compresión fuerte ni reducción de
  ruido que la deje enlatada. Fundido de 8 ms en cada corte.
- **Mezcla final −14 LUFS integrados, pico real ≤ −1,5 dB**, en dos pasadas (`paso5_audio.py`). Mide el archivo final.
- 2026-11-11 — **Música solo cuando toca**, no cama continua: gancho + título + arranque, entrada de cada sección (rótulo
  + ~10–14 s), secuencias de planos sin voz, mapas, la frase emotiva y el cierre. Orientación: **30–40 % del vídeo,
  14–17 dB bajo la voz**, entrada rápida y salida de 3 s; en planos sin voz sube. Por qué: «no hace falta que la pongas
  en cada momento, solo cuando toque, a veces poniendo planos». (ramon v2)
- **La música la descarga el creador** de su banco con licencia y la deja en `personal/<creador>/recursos/musica/` (catálogo en
  `CATALOGO.md`). Claude no descarga nada de un banco sin confirmación pista a pista y **no puede escucharla**: elige por
  ficha (BPM, etiquetas) y lo dice; el creador confirma de oído.
- **Efectos de sonido «a veces»**: uno suave pegado a cada gráfico (título, capítulo, rótulo, mapa, cifra), nunca en cada
  corte. Se cambian o quitan con `SFX` en `plan.py` (un vídeo) o en `personal/<creador>/ajustes.py` (todos los del creador).
- 2026-11-14 — **Quien no quiere que se le reconozca (quien graba, un tercero que lo pide): voz disfrazada y fuera de
  imagen.** Su voz, en `VOZ_DISFRAZ = [(clip, "frase literal", n), …]` de `plan.py`: `paso5_audio.py` sube el tono de
  esas frases sin cambiar la duración (voz de pitufo; cuánto: `VOZ_DISFRAZ_TONO` en `ajustes.py`, 1,45 de serie). Su
  imagen: cara pixelada o el plano fuera; si solo asoma (una mano, un brazo), se tapa con un recurso. Para encontrarlo:
  el registro visual anota cada vez que asoma alguien que no es el creador, y la voz de quien graba se distingue por el
  texto (le pregunta, le pide cosas, el creador le contesta) y porque llega más baja y lejana al micro del creador.
  Claude no oye: al entregar se dice qué frases se han disfrazado y cuáles quedan en duda. Por qué: Lucas, «cuando
  habla el cámara (señor misterio) […] distorsiona un poco la voz para que no se le reconozca, puede ser como una voz de
  pitufo; […] no debe de salir en los vídeos, o se le pixela la cara o se elimina cuando salga». Quién es ese tercero,
  en `personal/<creador>/preferencias.md`. (vídeo: prueba-3)
- Nunca huecos mudos: un plano sin voz lleva su sonido original bajo o música.
  - 2026-11-14 — **Ningún plano sin voz se queda sin música** (él andando, mirando, un recurso sin habla): los respiros
    de música entre ventanas solo caen donde se habla, y en todo rato de más de 1,5 s sin palabras la música sube
    (nivel `SINVOZ`). Lo hace solo `paso6_musica.py`: si un hueco de más de 1 s queda sin voz y sin música, adelanta la
    ventana siguiente (la canción nueva entra con el plano sin voz) o alarga la anterior, e imprime `puente: …`. Por qué:
    Lucas, en 1:46 de `1311` v2, «cuando dice "vámonos" hay un plano en el que sale caminando y no habla ni nada y no
    hay música; ponle música a eso». Causa: las ventanas acababan a −3,5/−4 s fijos de cada capítulo para dejar un
    respiro antes del rótulo, sin mirar si ahí se hablaba, y la subida «sin voz» solo se aplicaba a los recursos, no a
    un plano suyo en el que no habla. Pasaba en dos cambios de capítulo. (vídeo: 1311)

## Entrega
- **Horizontal 16:9, H.264, a la mejor resolución que haya en los brutos** (3840×2160, 2560×1440 o 1920×1080; nunca se
  amplía por encima del mejor bruto ni se entrega por debajo) y a los fps del bruto principal (Sony 25, iPhone 30). No
  se mezclan fps: el lienzo manda y lo demás se convierte.
- Salida: `out/AAAA-MM-DD_<slug>.mp4` (bt709, `faststart`) + línea en `out/REGISTRO.md`. Peso orientativo: 4K a calidad
  alta ≈ 350 MB/min; si el creador necesita menos, se recodifica al final, no se baja la calidad del montaje.
- **Antes de entregar**: duración y número de frames (ffprobe), color contra el bruto, sonoridad, y fotogramas del archivo
  final en cada gráfico y en cada plano de recurso. Di qué se ha comprobado y qué no (Claude no ve el movimiento ni oye).
- 2026-11-12 — **Matrículas: SIEMPRE difuminadas, y solo la matrícula.** Toda matrícula que se pueda leer en el
  vídeo final (coche aparcado al fondo incluido) se difumina con `herramientas/montaje/tapar.py` (`TAPAR` en
  `plan.py`): el borrón va **ajustado a la matrícula** fotograma a fotograma y no tapa nada más (ni el coche, ni lo que
  pase por delante: una mano, un retrovisor). Se buscan al hacer el registro visual y se comprueban en el archivo
  final. Por qué: Lucas, «las matrículas difuminadas siempre, y ajustado solo a la matrícula». Un rectángulo fijo
  grande no vale: tapaba el retrovisor y el brazo. (vídeo: ramon)
  - 2026-11-12 — **También cuando solo asoma una esquina.** Si alguien pasa por delante y la tapa casi entera, lo que
    asoma (la banda azul y la primera cifra) se lee igual y también va borroso; `tapar.py` lo hace con una segunda
    pasada (sigue lo que rodea a la matrícula y busca su esquina). **Se comprueba en el archivo final, a tamaño real y
    cada 2–3 fotogramas, en TODO el tramo en que el coche está en plano**, no solo donde la matrícula se ve entera: las
    entradas y salidas detrás de un hombro son donde falla. Por qué: Lucas preguntó «¿has ocultado la matrícula en el
    último vídeo?» y en la v7 asomaban la banda y el «1» durante 1,8 s (3:40–3:42). Causa del fallo: el seguimiento
    solo reconocía trozos grandes de la matrícula, la daba por tapada, y la hoja de comprobación enseñaba esos
    fotogramas en pequeño y con el recorte donde la matrícula había estado antes, así que se dieron por buenos sin
    verla. (vídeo: ramon)
  - 2026-11-14 — **Buscarlas: cualquier coche en una muestra = el plano entero a tamaño real.** Una muestra cada
    ~2,5 s en hoja pequeña no basta para saber si la matrícula se lee: con la cámara en movimiento el coche cruza el
    cuadro en menos de un segundo. Si en una muestra hay un coche (aunque sea un trozo, un techo, una rueda), se saca
    ese plano en el archivo, a tamaño real y fotograma a fotograma en la zona del coche. Por qué: en la v2 de `1311` la
    muestra cogía el todoterreno entrando, de techo, y en la hoja no se veía nada; 0,7 s después se leía la matrícula
    entera (se vio en el repaso final, y hubo que tapar y rehacer el tramo). Descubierto en el repaso; no lo pidió Lucas. (vídeo: 1311)
- **Avisa de lo que el creador debe decidir**: caras de terceros, menores, pantallas con datos, marcas. Eso no se tapa
  ni se publica por iniciativa propia.
- Con el vídeo, siempre, el **paquete de YouTube**: 5 parejas de título + miniatura para test A/B (cada una con su
  prompt para ChatGPT y su fotograma de referencia), descripción, capítulos y etiquetas, en el idioma del vídeo
  (`base/titulos-miniaturas.md`, `base/descripciones.md`).
- **No se sube nada a ningún sitio** (YouTube, nubes, repos) salvo que el creador lo pida en ese momento.
- Cierre y limpieza a los 30 días: `SKILL.md` § 2.

## Lecciones técnicas (para no repetirlas)
- **Render híbrido**: todo en Remotion a 4K tarda ×14 la duración; capas en Remotion + vídeo con ffmpeg, ×2,7 (medido en
  i7-13700HX, 16 GB). Por eso Remotion solo hace gráficos.
- **ffmpeg, zoom animado**: `crop` no actualiza `iw/ih` cuando `scale` cambia de tamaño en cada fotograma
  (`eval=frame`). El recorte se calcula con la misma expresión Z(t) que la escala, no con `iw`. Ya está en `filtro_zoom`.
- **NVENC** (`h264_nvenc`) acelera los tramos en Windows con NVIDIA; ffmpeg 8 exige controlador ≥ 610. `auto` lo prueba
  y, si no va, usa x264. No actualices controladores sin permiso. `videotoolbox` (macOS) está escrito pero sin probar:
  compara un tramo con x264 antes de fiarte.
- 2026-11-12 — **Memoria durante el render: se vigila y se libera, sin tocar el render.** Un render 4K con 16 GB se
  queda sin memoria con facilidad (Remotion abre varios navegadores; ffmpeg usa 3–4 GB por tramo) y el proceso muere
  sin avisar. Mientras dura un render: `vigilar_render.py <salida>` cada 6–8 min con un cron de la sesión (SKILL.md § 2,
  paso 6). Qué hace y qué NO hace: cierra navegadores de Remotion colgados; en Windows, si queda poca memoria (< 3 GB o
  < 20 %), recorta la memoria de trabajo de los procesos que no son del render (no cierra nada); en macOS no recorta
  (el sistema comprime solo; `purge` pide contraseña y vacía la caché de disco que usa el render). **Nunca** toca
  ffmpeg, python, node ni el navegador de Remotion, no cierra programas del usuario, no cambia la calidad, el
  codificador ni el número de hilos de un render en marcha. Si el render se para: `render_todo.py <salida>` lo retoma
  (con la mitad de navegadores y los tramos de uno en uno a partir del segundo intento: más lento, mismo resultado).
  Por qué: Lucas, «cuando se estén haciendo renders liberar ram cuando sea posible, tanto en mac como en windows si
  esto no afecta al render ni a nada, no queremos que joda el funcionamiento de la skill, que edite peor o renderice
  peor». En macOS está escrito pero sin probar. (vídeo: ramon, v6)
- **Filtros largos**: pásalos por archivo (`-/filter_complex archivo`), no por la línea de comandos (límite de Windows).
- **`-nostdin`** en todo ffmpeg lanzado desde un bucle o un script.
- **Git Bash en Windows**: un comando con un heredoc largo puede fallar («unexpected EOF»): escribe el script o el
  documento en un archivo. Rutas con `/`. Python: `herramientas/.venv/Scripts/python.exe` (macOS: `.venv/bin/python`).
- **Listas de archivos** (`VIDEOS.txt`, `SKILLS.txt`): se leen quitando el retorno de carro (`tr -d '\r'`); la skill fija
  `eol=lf` en `.gitattributes`.
- **`drawtext` de ffmpeg** no vale para rótulos (sin fuentes de marca, escapes frágiles): los textos van en Remotion.
- **Música en casi todo el vídeo** (creadores que la llevan seguida): una ventana por capítulo; si la ventana es más
  larga que la canción, `paso6_musica.py` vuelve al compás 8 con un cruce de medio segundo. La base sigue siendo «solo
  donde toca»; la música seguida es una preferencia de creador (`personal/<creador>/preferencias.md`).
- **Vídeo con transparencia en Remotion**: `.webm` VP9 `yuva420p` con `<OffthreadVideo transparent>` (componente `Clip`
  de `Graficos.tsx`); comprobado en el render de capas ProRes 4444. Para leerlo con ffmpeg hay que forzar
  `-c:v libvpx-vp9` antes de `-i` (el decodificador nativo pierde el alfa).
- **16 GB de RAM**: agentes de dos en dos; no lances demucs, whisper y un render a la vez. Si el sistema mata un proceso
  en segundo plano por memoria, no lo relances sin preguntar.
- **Claude in Chrome**: si hay varios navegadores conectados, elige el del equipo del creador antes de abrir pestañas.
- MapLibre dentro de Remotion no cargó en render (timeout de `delayRender`): mapas con imagen estática + SVG.

## Lo que funciona (aprobado)
- 2026-11-11 — El mapa de satélite animado de `ramon` («va a la skill»).
- 2026-11-12 — Primer visto bueno de Lucas a la base de edición tras `ramon` v3.
