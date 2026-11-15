# Recursos fijos de Reino Selva (LOCAL)

> **Dónde está** (Lucas, 2026-11-13): la carpeta `recursos/` está en el disco externo **D:** (My Passport), en
> `D:\Horizontal\personal\reinoselva\recursos`; aquí queda un enlace (junction) con su mismo nombre, así que las rutas
> de abajo valen igual. Con el disco desconectado no hay intro, outro, música ni archivo.

Lo que usa **siempre o casi siempre** y cuándo. **Todo su material está en `personal/reinoselva/recursos/`, ordenado
por carpetas** (Lucas, 2026-11-13; fichas en `recursos/INDICE.md`): los originales fijos en `recursos/marca/`, el
archivo por `recintos/`, `especies/`, `plantas/` y `obras/`, y `fotos/`, `mapas/`, `musica/`, `sonidos/`. Lo ya preparado para
superponer, en `estudio/public/personal/reinoselva/`; sus gráficos, en `estudio/src/personal/reinoselva/Graficos.tsx`.

## Cabecera, cortinillas y cierre
- **Intro** — archivo: `recursos/marca/intro.mp4` (dron sobre la selva, 8 s, 1280×720, 24 fps, muda) — va **tras el tráiler y
  antes del título**, recortada a 4,8 s (del segundo 1,9 al 6,7), sin voz, con la música del tráiler. Encima, su logo
  con letras desde el segundo 1,75 hasta el corte. En el EDL: `V("intro", 1.9, 6.7, vol=0, tag="intro")`; en `plan.py`:
  `PROPIOS = [(("@intro", 1.75), 3.05, "logo_intro"), …]` — desde 2026-11-12. Por qué: así abre todos sus vídeos.
  *El original es 720p: en un vídeo 4K se ve blando. Pedirle la intro en 4K si la tiene.*
- **Outro** — archivo: `recursos/marca/outro_largo.mp4` (24 s: su clip de 8 s hacia delante, marcha atrás y otra vez hacia
  delante, como lo monta él; el clip suelto es `recursos/marca/outro.mp4`) — va **al final, tras la despedida**, unos 20 s,
  sin nada encima y con la música alta hasta que acaba. En el EDL: `V("outro_largo", 0.0, 20.0, vol=0, tag="outro")` y
  la última ventana de música hasta `"fin"` — desde 2026-11-12. Por qué: así cierra todos sus vídeos.
- `recursos/marca/logo_animado.mp4` y `recursos/marca/secundaria.mov`: los tiene, pero no salen en los vídeos analizados. No usar sin pedirlo.

## Logos, marcas de agua y rótulos propios
- **Qué logo va: el del idioma del vídeo.** Español → Reino Selva (`logo_con_letra.png`). Inglés → **RayWild**
  (`logo_raywild.png`). Lo elige `marca.json`; el gráfico `logo_intro` pinta el que le llega.
- **Logo de RayWild** (Lucas, 2026-11-12; canal en inglés **@raywild10**) — original: `recursos/marca/logo_raywild.png`
  (1920×1080, la tortuga con corona y «RAYWILD» sobre NEGRO, con un resplandor crema alrededor) → preparado:
  `estudio/public/personal/reinoselva/logo_raywild.png` (889×830, hecho con `herramientas/quitar_fondo_resplandor.py`:
  el resplandor queda crema y translúcido; con `quitar_fondo_imagen.py` dejaba un cerco oscuro). Mismo uso que el de
  Reino Selva: solo sobre la intro.
- **Logo con letras (Reino Selva)** — original: `recursos/marca/logo_con_letra.png` (fondo crema, opaco) → preparado sin fondo:
  `estudio/public/personal/reinoselva/logo_con_letra.png` (hecho con `herramientas/quitar_fondo_imagen.py`). Solo sobre
  la intro (gráfico `logo_intro`: destello blanco y logo centrado al 72 % del alto con un resplandor claro detrás). Sin
  logo fijo en el resto del vídeo.
- `recursos/marca/logo_sin_letra.png`, `recursos/marca/logo_solo_letras.png`, `recursos/marca/TIK TOK*.png/jpg`: variantes, sin uso en YouTube.

## Rótulo de idea clave (`rotulo`)
Su manera de resaltar con texto: blanco, mayúsculas anchas con borde negro, en el tercio inferior y centrado; debajo,
más pequeño y en su dorado, la explicación. Entra de golpe con la palabra y crece despacio (×1 → ×1,08). Sin sonido.
Componente `Rotulo` en `estudio/src/personal/reinoselva/Graficos.tsx`. Qué se rotula y cuánto: `preferencias.md` →
Textos y gráficos.

Se pide en `plan.py`. **El ancla es la PALABRA que se escribe** (no el principio de la frase: `-1` = la última vez que
suena), y dura hasta que acaba la frase:
```python
R = lambda ancla, dur, txt, sub=None, **k: (ancla, dur, "rotulo", {"txt": txt, **({"sub": sub} if sub else {}), **k})
ROTULOS = [
 R((A, "siebenrocki", -1), 2.4, "CHELODINA SIEBENROCKI", "from southern New Guinea"),   # especie: científico + común
 R((D, "things take time", -1), 1.6, "THINGS TAKE TIME"),                               # frase resumen, un nivel
 R((C, "asian pond it turned", -1), 1.3, "ASIAN POND"), R((C, "iberian pond", -1), 1.5, "IBERIAN POND"),   # contraste en dos pasos
 R((E_, "flooded because we", -1), 3.15, "FLOODED", "after very heavy rains", subEn=2.1),   # la 2.ª línea entra cuando la dice
]
PROPIOS = ROTULOS + [ ...intro, tortugas... ]
```
`subEn` (segundos): la línea pequeña entra más tarde, con su propio golpe y sin mover la grande. Úsalo cuando la
línea pequeña es algo que él dice un par de segundos después; si es el nombre común de una especie, entra con ella.
Después de `paso3_plan.py`: `timing_textos.py` (base → Timing de los textos).
Opciones: `lado` (centrado de serie | `"izq"` | `"der"`, si él o el animal ocupan el centro abajo), `y` (altura de la
base del bloque sobre el borde inferior, de serie `0.1` = 10 % del alto), `txt` con `|` para partir en dos líneas. Máximo ~24 letras por línea en `txt` y ~40 en
`sub`. Duración: 1,5–2 s una frase corta; 2,4–3,4 s con segundo nivel. Después de `paso3_plan.py`, `ver.py` en el
frame anterior (no está), a mitad y casi al final de cada uno.

## La tortuga (su mascota) con burbuja
Dibujo amarillo y naranja con contorno verde oscuro (la del logo). Diez animaciones sin fondo en
`estudio/public/personal/reinoselva/tortuga/<anim>.webm` (originales con fondo verde en `recursos/marca/tortuga/`; se
prepararon con `herramientas/quitar_fondo.py --modo mate`). Cuándo y cuántas: `preferencias.md` → Textos y gráficos.

Se pide en `plan.py`:
```python
PROPIOS = [(ancla, 4.8, "tortuga", {"anim": "senalando", "txt": "La frase de la burbuja."})]
RETARDO_TEXTO = {"tortuga": 0.5}      # para timing_textos.py: la burbuja se lee 0,5 s después de que asome
```
**Timing (Lucas, 2026-11-12):** la burbuja se lee 0,5 s después de que la tortuga empiece a asomar. Se ancla para que
ESE momento caiga en la palabra de la que habla la burbuja (el nombre del animal: `((E_, "for the uromastics", -1), -0.1)`),
no al principio de la frase: en la v6 de `ramon` dos burbujas salían 2–3 s antes de que nombrara al animal. No pegada a
otro rótulo (medio segundo de aire). Y se mira con `ver.py` en **cada plano que pisa**: en un corte a ×1,45 la burbuja
sube hasta la boca; si pasa, `"tam": 0.72` (más pequeña, la burbuja baja) o `"lado": "izq"`.
Opciones: `lado` (`"der"` de serie | `"izq"`, en espejo), `forma` de la burbuja (`"habla"` de serie | `"grito"` para
sorpresa o aviso fuerte | `"piensa"` para duda o ironía), `fuente` (`"impacto"` de serie, como la suya | `"redonda"`),
`tam` (1 = su tamaño), `txt` como lista de dos frases = dos burbujas seguidas (él lo hace con los avisos).

| `anim` | Qué hace | Para qué comentario |
|---|---|---|
| `senalando` | brazos abiertos, se encoge de hombros y guiña (la que más usa) | dato, aclaración, llamada a comentarios o listas |
| `explicando` | brazos abiertos | explica un proceso, enumera |
| `preocupada` | mira arriba con apuro | aviso, riesgo, «no hagáis esto en casa» |
| `observando` | prismáticos | avistamiento, «fíjate en…» |
| `reportero1` | micrófono en alto | novedad, cifra, cita |
| `reportero2` | micrófono al pecho | pregunta al espectador |
| `cera` | pasa la esponja | limpieza, mantenimiento, trabajo; algo de «dar cera» |
| `andando` | camina contenta | «vamos a…», traslado |
| `de_espaldas` | se gira y da la espalda | broma, «yo no he sido» |
| `buceando` | tubo y burbujas | agua, estanque, peces |

Su burbuja original (`recursos/marca/tortuga/burbuja_original.png`) es blanca con borde negro grueso y cola hacia la tortuga; aquí se
**dibuja** con ese diseño a la medida del texto (no se estira la imagen). `recursos/marca/tortuga/tortuga_hd.png`: la tortuga quieta.

Ojo con los originales: son animaciones generadas y traen cosas raras. En `senalando` la tortuga bota un balón que le
rebota en la cabeza hasta el segundo 4,75: solo se usa el final (4,85–8 s, algo más lento). Como dura poco, la burbuja
de `senalando` no puede pasar de 5 s. Antes de usar una animación nueva, mirar una hoja con TODOS sus fotogramas.

## Sonidos propios
- Ninguno comprobado. La tortuga asoma **sin sonido** (así va en sus vídeos); si algún día lo quiere: `"snd": ["pop", 0.18]` en sus datos.

## Música habitual
- Pistas alegres y tranquilas de Shutterstock, una por capítulo (`recursos/musica/CATALOGO.md`). En `ramon`: «Boost Me»
  para el tráiler; «Feel Good Days», «A Hopeful Journey» y «Pieces of Hope» alternándose. Cómo va: `preferencias.md`.
- Desde 2026-11-14 hay 19 pistas (acústicas alegres, indie y rock de garaje a tempo medio): ninguna se repite dentro de un
  vídeo. En `1311` v2: «Boost Me» en el tráiler y 12 distintas por mitades de capítulo (reparto en su `plan.py`).

## Botones
- Barra de suscripción animada (YouTube + me gusta + campana) abajo en el centro al pedirlo. Son recurso de la **skill**
  (`base/recursos.md` → Botones de YouTube): `BOTONES = [(ancla, 2)]`; en un vídeo en inglés coge sola `b02_en`
  («SUBSCRIBE» → «SUBSCRIBED»). En `ramon`: `(((F, "subscribe to my channel", -1), -4.12), 2, {"vel": 1.25})`, para que
  el clic caiga en la palabra y la barra se recoja antes del outro.

## Material de archivo
Lucas (2026-11-12): «el creador habla del pasado de cuando empezaron la construcción del asian…, habla de los peces, várzea, en la
várzea habla de plantas, etc. Esto en un futuro en recursos habrá vídeos de todo eso clasificados, para que puedas ir
poniendo planos de vez en cuando cuando los menciona, con su voz de fondo, para que sea también más dinámico».

**Ya hay archivo de especies** (2026-11-14): el Drive «2_ANIMALES POR ESPECIE», solo los vídeos horizontales
(237 clips, 256 GB), en `recursos/horizontales/especies/<especie>/`, renombrados `AAAA-MM-DD_<que-se-ve>.ext` y con ficha.
- **Cómo se busca**: `recursos/INDICE.md` (tabla: qué hay de cada especie) → `horizontales/especies/<especie>/INDICE.md`
  (una línea por clip: qué se ve, tramos útiles con tiempos —en negrita los de nota 3—, vibe, avisos) →
  `horizontales/_analisis/<especie>/FICHAS.md` y `fichas/<nombre original>.json` (todo, segundo a segundo) y
  `hojas/` (un fotograma por segundo, 6×6: la hoja NN empieza en NN × 36 s). El nombre original del Drive (IMG_…, C0…)
  va entre paréntesis en cada línea y en `_analisis/<especie>/nombres.json`.
- **Qué hay** (clips): lagarto caimán 30 · erizo europeo «Sonic» 21 · rosella común 4 · tortugas bebés (mora y de caja) 14 ·
  tortuga de caja 27 · tortuga leopardo 14 · tortuga sulcata 21 · uromastyx 14 · tortuga radiada «Kowalski» 1 ·
  tortuga morrocoy «Cherry» 10 · rana mono encerada (Phyllomedusa) 35 · rana de lluvia (Breviceps) 45 · sin clasificar 1.
- **Antes de usar un clip**: casi todos los de iPhone son HDR (HLG) → `herramientas/proxy.sh`; mira el tramo con
  fotogramas (los tiempos de las hojas bailan ±0,5 s y los de las frases, 1–3 s); muchos llevan charla de rodaje: se
  usan **sin su sonido** salvo las frases marcadas como limpias; vigila lo apuntado en «Avisos» de cada ficha (fachadas
  y coches al fondo, marcas a la vista —Warmtec, Sika, Tukan, DJI—, terceros nombrados).
- **Ojo**: en `tortuga-sulcata/` hay dos clips que NO son tortugas (IMG_0401 e IMG_0403: lagarto claro bajo lluvia
  artificial, mal archivados en el Drive); en `erizo-europeo/` hay tres duplicados exactos (los «…-2»); en
  `tortuga-de-caja/` hay un clip de la tortuga acuática «Hillary» y otro del lagarto «Safira». No se bajaron: los
  verticales (89), las fotos, los .docx (11) y los .XML (24).
- **Lo que sigue sin haber** (carpetas creadas y vacías: `recintos/<recinto>/` —`varzea`, `estanque-asiatico`,
  `grandes-lagos`, `kalahari`, `sabana-africana`—, `obras/`, `plantas/`, `creador/`): cría de grillos (el proceso);
  rana de ojos rojos (*Agalychnis callidryas*) y el Chocó; peces de la Várzea de cerca: corydoras y sus crías, medakas,
  neones chinos (*Tanichthys*); el estanque cuando era «ibérico» y su construcción como asiático; plantas de la Várzea
  de cerca y cuando se plantaron; ríos de aguas negras (igapó); tortuga caimán (para «Grandes Lagos»); loros
  africanos; la inundación de los refugios de las sulcatas (solo hay el después). Del Kalahari hay planos generales
  en `tortuga-leopardo/` y `tortuga-sulcata/` (mayo de 2026) y del recinto viejo de tierra (enero de 2026).
- Regla de uso: `preferencias.md` → Planos de recurso. Material nuevo: a su carpeta, con ficha (base/recursos.md § 2–4).

## Fotos, mapas y otros
- Mapa de los ecosistemas de Sudamérica: `recursos/mapas/sudamerica_bluemarble.jpg` (NASA Blue Marble), con sus regiones en
  `estudio/src/videos/ramon/Capas.tsx`. Reutilizable en cualquier vídeo de la Várzea o el Chaco. Usado en: `ramon`, `1311`.
- Mapa de Asia oriental: `recursos/mapas/asia_oriental_bluemarble.jpg` (NASA Blue Marble), con Japón (medaka) y el sur
  de China (tetra chino) en `estudio/src/videos/1311/Capas.tsx`. Para cualquier vídeo del estanque asiático. Usado en: `1311`.
- **Archivo de especies usado en `1311`** (2026-11-14, primer vídeo que lo aprovecha): de `horizontales/especies/tortuga-de-caja/`,
  `2026-09-10_tortuga-motas-amarillas-enterrada-pinaza` (18,6 s sobre «brumar» y 9,2 s sobre «a ver si habrá alguien
  aquí abajo») y `2026-09-05_estanque-tortuga-acuatica-hillary-comida` (267,2 s: el estanque chaqueño con sus plantas;
  304,0 s: Hillary bajo el agua, sobre el rótulo PHRYNOPS HILARII). Lo que este vídeo pedía y el archivo NO tiene:
  medakas y tetras chinos de cerca, las plantas (iris, menta acuática, alocasias, nenúfar) en buen estado o en flor,
  el estanque asiático en otra época, y el recinto del Gran Chaco entero.
