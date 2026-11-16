# Referencias de títulos, miniaturas y descripciones — CONTEXTO

Evidencia de `base/titulos-miniaturas.md` y `base/descripciones.md`. No es un tipo de vídeo (por eso el guion bajo):
es el estudio de cómo **empaquetan** sus vídeos quince canales. Datos bajados con `herramientas/canal_youtube.py`
(yt-dlp), en idioma original y con la miniatura original.

- **Primera pasada, 2026-11-13**: los diez primeros canales; 13 agentes los miraron uno a uno (uno por canal para las
  miniaturas, uno por idioma para los títulos y uno para las descripciones).
- **Estudio al detalle, 2026-11-14**: se repitió con `ENCARGO_DETALLE.md` (un agente por canal, vídeo a vídeo: recorrido
  del ojo, cara, manos, instante, texto, encaje, segunda lectura) sobre los diez de antes y cinco nuevos en inglés. En
  total, 19 informes: 15 análisis de canal, 3 segundas miradas a los extremos y un estudio de títulos en inglés; los cruza
  `SINTESIS_2026-11-14.md`. Unos 850 vídeos.

| Canal | Idioma | Vídeos | Periodo | Suscriptores | Mediana de visitas | Duración mediana | Título (car.) | De qué va |
|---|---|---|---|---|---|---|---|---|
| rubenholg (Rubén Holgado) | es | 48 | 2 años | 1,0 M | 1,13 M | 24 min | 39 | viajes a sitios extremos |
| HiClavero | es | 48 | 1 año | 2,4 M | 1,61 M | 20 min | 48 | sitios raros y su historia |
| nilojeda (Nil Ojeda) | es | 79 | 2 años | 4,9 M | 1,17 M | 50 min | 52 | series de retos, lujo |
| losviajesdenicovilla | es (Argentina) | 64 | 1 año | 1,0 M | 0,37 M | 31 min | 55 | viajes país a país |
| byCalitos79 | es | 40 | 2 años | 1,0 M | 0,34 M | 33 min | 50 | vlog, coches, relojes |
| MrBeast | en | 49 | 2 años | 526 M | 181 M | 26 min | 37 | retos con premio |
| paulcuffaro (Paul Cuffaro) | en | 150 | 1 año | 4,3 M | 0,40 M | 32 min | 46 | estanques, acuarios, granja |
| Sidemen | en (Reino Unido) | 53 | 1 año | 23,4 M | 6,7 M | 87 min | 41 | retos en grupo |
| ChandlersWildLife | en | 54 | 1 año | 2,9 M | 0,17 M | 23 min | 31 | reptiles y su parque |
| BraveWilderness | en | 46 | 1 año | 21,8 M | 0,26 M | 13 min | 43 | mordeduras y picaduras |
| benmorris (Ben Morris) | en | 36 | 3 años | 1,07 M | 0,63 M | 20 min | 43 | viajes en solitario |
| BacktoBasics (Back to Basics) | en | 59 | 2 años | 1,5 M | 0,48 M | 34 min | 55 | supervivencia, pesca y caza |
| colsonscritters (Colson's Critters) | en | 45 | 1 año | 82 k | 27.461 | 24 min | 49 | canal pequeño de animales |
| ForrestGalante (Forrest Galante) | en | 41 | 1 año | 3,06 M | 2,04 M | 19 min | 46 | biólogo: visitas y listas |
| biaheza | en | 42 | 7 años | 1,57 M | 0,85 M | 12 min | 37 | dinero y coches |
| LaGranjadelBorrego (GB) | es (Colombia) | 46 | 2 años | 30,2 M | 2,30 M | 25 min | 42 | granja, cuidar fauna, aventura (solo títulos) |
| fielddaysenespanol (FD) | es (traducido) | 64 | 2 años | 694 k | 0,62 M | 39 min | 74 | supervivencia, pesca y caza (solo títulos) |
| AntsCanada (AC) | en | 86 | 2 años | 7,06 M | 0,79 M | 25 min | 67 | recintos-ecosistema en casa (solo títulos) |
| WickensWickedReptiles (WW) | en | 219 | 2 años | 447 k | 34.034 | 13 min | 42 | reptiles en cautividad (solo títulos) |
| JacobFeder (JF) | en | 141 | 2 años | 2,44 M | 0,15 M | 18 min | 43 | zoo en el patio y rescates (solo títulos) |

**Tanda de títulos de animales, 2026-11-14** (los cinco últimos): un agente por canal con `ENCARGO_TITULOS_NICHO.md`
(el título y cómo lo acompaña la miniatura, no el diseño de la miniatura), cruzados con los seis canales de animales de
antes en `animales_titulos_2026-11-14.md`. Lo mismo sirve para afinar otros tipos de título más adelante.

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| `SINTESIS_2026-11-14.md` | **Empieza por aquí.** El cruce de los 19 informes regla a regla: veredicto de cada regla de la guía, reglas nuevas con su fuerza, diferencias por idioma y tipo de canal, contradicciones sin resolver, lista de comprobación y cambios en el prompt. |
| `animales_titulos_2026-11-14.md` | **Títulos de animales**: qué se desviaba en los títulos de la skill, lo que se repite en once canales de animales, cómo acompaña la miniatura y qué pasa al español. |
| `canales/<canal>_titulos.md` | Los cinco análisis de títulos de animales (GB, FD, AC, WW, JF): moldes con recuento, sujeto y forma de nombrar al animal, encaje con la miniatura en las 10 mejores y peores, parejas, plantillas. |
| `canales/<canal>.md` | Los análisis completos nuevos (2026-11-14, `ENCARGO_DETALLE.md`), uno por canal: tabla de todos los vídeos, anatomía de miniatura y título, encaje, mecanismos, mejores frente a peores, recetas y contraste con la guía. |
| `canales/_primera_pasada/<canal>.md` | Los análisis del 2026-11-13 (`ENCARGO_CANAL.md`) de los diez primeros canales. Algunas de sus cifras las corrige la síntesis. |
| `segundas/` | Tres segundas miradas a los extremos (vlog en español, viajes en español, retos en inglés). |
| `titulos_es.md`, `titulos_en.md` | Los títulos de la primera tanda (cinco canales por idioma): medidas, moldes con recuento, gramática, palancas, malas prácticas, 15 plantillas. |
| `titulos_en_2.md` | Los títulos en inglés de la segunda tanda (FG, BM, BB, CC, BZ). |
| `descripciones.md` | Las 631 descripciones de la primera tanda: ficha por canal, primera línea clasificada, español frente a inglés, si importa, plantillas. |
| `datos/<canal>.tsv` | Todos los títulos con fecha, visitas, ratio, minutos y caracteres. |
| `hojas/<canal>.jpg` | Las 8 miniaturas de mayor ratio (dos filas de arriba) y las 8 de menor, con su título. Míralas antes de proponer una miniatura de ese estilo. |
| `METODO.md`, `ENCARGO_*.md` | Cómo repetir el estudio con otro canal (el del creador, un nicho nuevo). `ENCARGO_DETALLE.md` es el análisis fino. |

Dentro de los análisis de la primera pasada, las rutas `tablas/<canal>_titulos.tsv`, `hojas/<canal>_extremos.jpg` y
`miniaturas/<id>.jpg` son las del trabajo original; en los informes nuevos, las rutas `RAIZ\<canal>\…` (`titulos.tsv`,
`detalle/NN.jpg`, `hojas/NN.jpg`, `miniaturas/<id>.jpg`) también son las de trabajo. Aquí son `datos/<canal>.tsv` y
`hojas/<canal>.jpg`; las miniaturas sueltas y las hojas `detalle/` no se guardan (se vuelven a sacar con
`canal_youtube.py`). `#n` es el número de vídeo de ese canal (1 = el más reciente en la fecha de la bajada).

## Cómo leer el ratio (y sus trampas)

`ratio` = visitas del vídeo / mediana del canal con los vídeos de más de 21 días. **No es el CTR.** Lo que se vio:
- **En los 15 canales** el ratio lo explica antes el tema, la serie, la época o el invitado que el empaquetado.
- **La antigüedad sesga**: en MrBeast y Sidemen los vídeos viejos acumulan más; en Chandler, que crece, al revés.
  Compara cada vídeo con la mediana de sus 8–10 vecinos en el tiempo.
- **La serie manda** en Nil Ojeda (el peor episodio de «Entre Millonarios» supera al mejor de las otras dos) y cada
  episodio cae un 2–3 % respecto al anterior.
- **Quién sale manda** en byCalitos (Leto en 3 de las 4 mejores) y en Sidemen (x3,24 con Haaland).
- **El tema manda** en Paul Cuffaro (visitas x1,40 y nutrias x1,42; compras x0,88), Brave (mordeduras x1,36 frente a
  x0,74), Back to Basics («SURVIVAL CHALLENGE» 9/9 ≥ x1,75) y biaheza (época de coches 5/5 ≥ x2,7).
- **El país manda** en Nico Villa (China x3,16; Francia x0,28).
- **Los «me gusta» por visita** van al revés que el ratio en 11 canales: los éxitos llegan a gente que no sigue el canal.
Por eso las reglas de la skill se apoyan en lo que se repite en varios canales y en parejas casi iguales con resultado
distinto, no en una mediana suelta. Quince canales no son una muestra: son quince casos bien mirados.

## Lo que se repite en varios canales (resumen; el detalle, en la síntesis)

- **La segunda lectura** es lo más fuerte (11 canales): la imagen sola dice una cosa y con el título otra que sube lo
  que está en juego, en un solo paso. También: polos opuestos (el título quita, la imagen da), repartir la cifra.
- La imagen nunca enseña el después (9 canales); el instante es el antes (si el desenlace es incierto) o el durante
  (si el formato promete el daño).
- Ilustrar el título hunde cuando la imagen no añade prueba ni nada en juego; vale cuando la imagen es el morbo.
- Esconder sin ancla apaga; con ancla (forma visible, precio, peligro, juego) funciona.
- La expresión necesita su causa en el cuadro; ante lo enorme, la calma gana al grito (5 canales).
- El objeto en la mano es un suelo, no un éxito; el brazo que señala, en las peores.
- Llevar texto o no es estilo; lo que separa es qué dice: el dato que choca con la foto funciona, el eco y la
  respuesta no. Repetir el título vale si nombra el formato o pone las dos cifras del versus.
- Flechas que señalan lo ya visible, no; la raya que une dos cosas, sí (6 canales).
- Callar el nombre pequeño y decir el rasgo o el arquetipo; nombrar lo famoso. Empaquetar para quien no conoce el canal.
- En títulos, el verbo con resultado, coste o cuerpo (8 canales); paradoja dentro del título (6); la fórmula ganadora
  rinde la mitad la segunda vez (7); las secuelas y las recopilaciones, al fondo.
- Inventar el decorado o el símbolo no se castiga en el ratio (12 canales); inventar el suceso, la emoción o el animal,
  sí. La norma de la casa (nada que no esté en el vídeo) se queda igual.
- Mucho de lo que parecía de idioma es de género: los viajeros en inglés escriben como los viajeros en español.
- La descripción no se relaciona con el ratio en ningún canal; su primera línea es comercial en el 43 % de los vídeos
  (primera tanda). En español no hay capítulos automáticos (0 de 279); en inglés, 218 de 352.

## Correcciones
(Lo que Lucas corrija sobre títulos, miniaturas o descripciones y valga para todos, con fecha y motivo.)
