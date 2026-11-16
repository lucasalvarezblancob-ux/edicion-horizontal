# Nil Ojeda (nilojeda) — detalle fino de títulos y miniaturas

Segunda pasada, fina. Datos: `nilojeda/titulos.tsv`, `videos.json`, `descripciones.txt`, las 20 hojas de `detalle/`,
las 5 de `hojas/` + `extremos.jpg` y miniaturas a tamaño completo. Ratio = visitas / mediana del canal (1.170.476).

## 1. Ficha

- **Idioma**: español de España (Nil es catalán; dos piezas en catalán: #44 «guanyar se va.» y #66
  «MANGAENCATALÁN (Official Music Video)»). Las series se dirigen a España + Latinoamérica (Argentina, México,
  Colombia…), con invitados latinos.
- **De qué va**: series diarias de «21 días» con reto y dinero de por medio, con su grupo de amigos (Misho, Guanyar,
  Soul): **21 Días Escapando con 100.000€** (huir con un maletín), **21 Días Entre Millonarios** (Miami, Dubái, Mónaco,
  Argentina: lujo y millonarios), **El Mejor País de LATAM** (10 países puntuando gastronomía, territorio y
  experiencia, con el rapero YSY A). Sueltos: películas-recopilación (#33, #34, #36), Apple Park (#35), regalar un coche
  (#32), Porsche (#1), dos «concursos» (#59, #68), dos piezas raras (#40, #44, #66).
- **Nº y periodo**: 79 vídeos del 27-04-2025 (#79) al 15-10-2026 (#1). Solo #1 tiene menos de 21 días (29 días: ya
  cuenta, sin `*`).
- **Cadencia**: a **ráfagas**. Un episodio al día durante la serie (20 en Escapando, 20 en Millonarios, 30 en LATAM, a
  veces dos el mismo día) y luego meses de silencio con un suelto cada 1–3 meses. Esto es clave: el canal funciona
  como una **temporada de televisión**, no como un canal de vídeos sueltos.
- **Duración**: episodios de 35–70 min (mediana ~50); películas de 177–220 min; sueltos de 27–63 min. Nada corto
  salvo #40 (7 min) y #66 (1 min).
- **Quién sale**: Nil siempre, casi siempre con 1–3 amigos; invitados famosos en Millonarios (Coscu, Duki, Lola
  Lolita, Abraham Mateo, Fernando Alonso) y en LATAM (WestCOL, Ovy, Pablo Chill-E, Rubius, J Balvin aludido).
- **Suscriptores**: 4.930.000. **Mediana**: 1.170.476 visitas.

### Qué explica el ratio aparte del empaquetado (comprobado antes de nada)

| Grupo | n | mediana ratio | mín–máx |
|---|---|---|---|
| 21 Días Entre Millonarios (#37–58 sin #40, #44) | 20 | **2,41** | 1,66–4,26 |
| Sueltos | 11 | 1,09 | 0,40–2,01 |
| El Mejor País de LATAM (#2–31) | 30 | **0,87** | 0,51–1,50 |
| 21 Días Escapando con 100.000€ (#60–79 sin #66, #68) | 18 | **0,855** | 0,70–1,52 |

1. **La serie lo es casi todo.** El peor episodio de Millonarios (#47, 1,66) supera al mejor de LATAM y de Escapando
   (1,50 y 1,52). Ninguna diferencia de miniatura dentro de una serie mueve tanto como el cambio de serie. Comparar
   una miniatura de Millonarios con una de LATAM no dice nada del empaquetado.
2. **No es la antigüedad.** Escapando y Millonarios son de las mismas semanas (abril–junio 2025, 520–565 días) y una
   tiene mediana 0,86 y la otra 2,41. LATAM (160–188 días) está en 0,87: más joven, pero su curva interna ya está
   asentada.
3. **Caída dentro de la serie.** El episodio 1 es el más visto o casi (Escapando #79 = 1,52, el máximo de la serie;
   LATAM #31 = 1,50, el máximo; Millonarios #58 = 3,78, tercero). Ajustando log(ratio) contra el nº de episodio:
   Escapando pierde ~2,9 % por episodio (1,52 → 0,7–0,8), LATAM ~1,5 % (1,50 → 0,5–0,7), **Millonarios no cae**
   (‑0,2 %): ahí cada episodio vive de su invitado o de su tema. Por eso, en este informe, además del ratio bruto
   doy el **residuo** = ratio / lo esperado por su posición en la serie (1,00 = lo normal para ese episodio).
4. **Invitado famoso** (dentro de Millonarios): Coscu #52 (residuo 1,65), Lola Lolita #41 (1,30), Duki #49 (1,10)
   arriba; pero Abraham Mateo #38 (0,80) y Fernando Alonso #54 (0,78) abajo. En LATAM, WestCOL #18 (1,57) y Ovy #19
   (1,17) arriba; Rubius #11 (0,87) y J Balvin #17 (0,87, que no sale: «Nos Trajo Hasta Aquí») abajo. El famoso
   ayuda cuando es del público joven latino/streamer, no cuando es una estrella «de la tele» española.
5. **Formato largo «película»**: #33 (0,53) y #34 (0,40), de 178 min, son los dos peores del canal; #36 (220 min)
   llega a 1,09 porque la serie original («21 Días Sin Gastar Dinero») no está en estos datos.
6. **Piezas no estándar**: #40 «Hola Lola» (7 min, 1,38), #44 «guanyar se va.» (36 min, 1,77, 16 % de likes/visita:
   despedida de un amigo, consumo de comunidad), #66 videoclip en catalán (0,47). No son comparables.
7. **Comentarios por visita** (videos.json) altísimos en #46 (11,8 por mil; sorteo de reloj probable) y en #40/#41
   (5,6 y 5,2 por mil): son vídeos de comunidad, el ratio no viene del empaquetado.
8. Las **descripciones** no venden: casi todas son plantilla (episodio anterior, primer episodio, publi, «Sígueme en
   Insta» con un emoji que cambia, «Suscribete si lees esto :)»). Solo #1, #31, #32, #39, #56–58 tienen una frase de
   gancho. No explican el ratio.

Corrección posterior (al ver las miniaturas): #68 y #59 llevan la moneda de Escapando con los números 13 y 21: son
episodios de esa serie publicados sin sufijo. Con ellos, Escapando tiene 20 episodios, mediana ~0,84 y cae ~2,7 % por
episodio; los residuos de los apartados 2–9 están calculados así (cambian en ±0,02 respecto a la primera cuenta).

Conclusión de partida: el empaquetado se juzga **dentro de cada serie y contra la caída por episodio**. Las
diferencias de residuo dentro de una serie van de 0,57 a 1,83: ahí está lo que el título y la miniatura pueden hacer.

## 2. Tabla de todos los vídeos

Orden de las hojas de detalle (mayor a menor ratio). `res` = residuo dentro de su serie (ratio / lo esperado por la
posición del episodio; 1,00 = normal). Serie: **M** = Entre Millonarios, **E** = Escapando, **L** = LATAM, **S** = suelto.
Texto: «"…"» = cita entre comillas tipográficas con rayita de bocadillo; «Bloque.» = palabra blanca gruesa con borde
negro y punto final (la plantilla de 2025).

| n | ratio (res) | ojo 1.º → 2.º → 3.º | cara | manos y cuerpo | sujeto y retoque | texto literal + cómo | recursos | instante | gatillo título | pregunta abierta |
|---|---|---|---|---|---|---|---|---|---|---|
| 52 M | 4,26 (1,65) | dos caras grandes a la izq. → mansión de cristal → canasta y pista azul | Coscu y Nil, cabezas ~45 % del alto; cejas alzadas, ojos muy abiertos, bocas entreabiertas; **los dos miran fuera de cuadro arriba-izq.**, no a cámara | Nil señala/gesticula con la mano abierta hacia atrás (a la casa) | mansión y pista hiperlimpias, cielo perfecto: fondo rehecho (aspecto de IA); caras recortadas y nítidas sobre él | ninguno | camisetas de baloncesto (Celtics) que «riman» con la pista | durante: acaban de llegar | «Lujosa Vida» + nombre (Coscu) | ¿qué están viendo que no vemos? ¿cómo vive Coscu? |
| 43 M | 3,97 (1,56) | móvil enorme en primer plano → dos caras sonrientes → botella de Moët gigante a la dcha. | dos chicos, cabezas ~20 %; sonrisa de selfi, mirada a cámara | Nil (izq.) sujeta el móvil hacia cámara = selfi; el «niño» levanta copa de champán | bandeja de canapés en primer plano y botella **agrandada** (más alta que una persona sentada); interior de jet cálido y pulido | «Jet Privado.» arriba dcha., blanco borde negro, punto, ~8 % alto | logo Moët legible | durante: ya están dentro | «Niño Millonario» + «Me Invita» | ¿un niño con jet propio? ¿quién es y cuánto tiene? |
| 58 M | 3,78 (1,45) | cara de Nil sonriendo → tarjeta roja hacia cámara → cita «compra un coche» | amigo barbudo (Misho) serio, ceja alzada, mirada a cámara; Nil sonrisa de dientes, ojos muy abiertos | Nil tiende la tarjeta Mastercard a cámara con las dos manos | concesionario blanco con fila de deportivos de colores (Ferrari, Porsche azul, Lambo verde) | «"compra un coche"» arriba centro, blanco borde negro, entre comillas, rayita al amigo | tarjeta como objeto-promesa | antes: la orden, aún no han comprado | título = nombre de la serie | ¿de verdad le dejan comprar un coche con esa tarjeta? ¿de quién es el dinero? |
| 41 M | 3,30 (1,30) | Lola Lolita sonriendo → bolso LV → tienda Louis Vuitton | solo ella (Nil no sale); cabeza ~12 %, sonrisa cerrada, mirada a cámara | sostiene el bolso hacia cámara con una mano, móvil en la otra | fachada LV limpísima, palmeras: escena rehecha; bolso adelantado y grande | ninguno | logos LV ×3 | durante: de compras | solo el nombre «Lola Lolita» | ¿cuánto se gasta? (débil: la imagen vive de la invitada) |
| 39 M | 2,99 (1,18) | cara de Nil con gafas → avioneta dorada → «1 Billón.» | Nil selfi, cabeza ~35 %, sonrisa abierta de dientes, gafas de sol | mano abierta presentando el avión | jet Cirrus **dorado** (color irreal, pintado), cielo azul | «1 Billón.» arriba dcha., blanco borde negro, punto | cifra | antes: a punto de subir | «Billonario» | ¿qué es tener 1 billón? ¿de quién es ese avión dorado? |
| 57 M | 2,84 (1,09) | cara de Nil girada → ventanilla con Burj Khalifa entre nubes → mano de guante blanco con plato | Nil cabeza ~20 %, ojos abiertos de lado, boca cerrada, mira por la ventanilla (sorpresa contenida) | sentado, mano en la mesa; camarero solo como brazo con guante | ventanilla con skyline de Dubái sobre nubes, imposible a esa altura: montaje | «Primera Clase» arriba dcha., blanco borde negro (sin punto) | guante blanco = servicio de lujo | durante: le sirven | «Todo Pagado» | ¿quién paga y por qué? ¿cómo es primera clase? |
| 49 M | 2,83 (1,10) | Duki sonriendo → Nil de perfil → luces rojas de escenario | Duki sonrisa amplia mirando a Nil; Nil de perfil, boca fruncida, le mira a él | cuerpos enfrentados, muy cerca | foto real de backstage con luz roja; cadena de oro de Duki | ninguno | — | durante | solo el nombre «DUKI» | ¿qué se dicen? (vive del nombre) |
| 51 M | 2,66 (1,03) | cara de Nil, ojos como platos → llave Rolls-Royce → chico sonriente | Nil cabeza ~30 %, ojos muy abiertos, boca cerrada (incredulidad); niño sonríe con mano en la barbilla | Nil enseña la llave RR a cámara entre dos dedos | techo de estrellas del Rolls (el detalle que lo identifica) | ninguno | logo RR en la llave | durante | «Niños Millonarios» | ¿ese chaval tiene un Rolls? |
| 42 M | 2,65 (1,04) | «Secuestro.» → encapuchados con bate y pistola → Nil pequeño en el sofá | caras tapadas; Nil diminuto, casi no se ve; hombre de gafas señala | encapuchados en carrera, bate en alto | escena (real o puesta en escena) en piso de lujo; nada agrandado | «Secuestro.» arriba izq., blanco borde negro, punto | — | durante: el asalto | «Nadie Esperaba» + «Robo» | ¿es real? ¿qué les pasa? (título dice «robo», imagen dice «secuestro»: escala) |
| 37 M | 2,54 (1,01) | tarjeta dorada → Nil con traje sonriendo → 6 caras alrededor | Nil sonrisa grande, selfi; amigos con ojos abiertos, uno con boca abierta | amigo tatuado señala la tarjeta con el índice; Nil la sostiene | mansión + helicóptero detrás (montaje); tarjeta dorada Visa | ninguno | dedo que señala la tarjeta | antes: van a gastar | «Todo Lo Que Quieras» + «24 Horas» | ¿qué compran con barra libre? |
| 53 M | 2,28 (0,88) | cara seria de Nil → yate con helicóptero → grupo serio | todos serios, mirada a cámara, cejas planas; Nil boca entreabierta | Nil con las dos manos en el pecho («¿yo?») | yate gigante con helipuerto detrás: fondo pegado | ninguno | — | antes | «Billonario?» (pregunta absurda) | ¿por qué le preguntan si es billonario? |
| 56 M | 2,25 (0,87) | 7 estrellas amarillas → Burj Al Arab → Nil asomado del Ferrari rojo señalando | Nil ojos muy abiertos, boca entreabierta, mira a cámara | se asoma por la ventanilla y **señala el hotel** con el índice | Burj Al Arab limpio, palmeras; Ferrari rojo cortado (solo puerta) | ninguno (las estrellas hacen de texto) | 7 estrellas gráficas = la cifra del título | antes: llegando | «Único» + «7 Estrellas» | ¿cómo es un hotel de 7 estrellas? |
| 46 M | 2,24 (0,88) | «"Te lo regalo"» → «$50.000» amarillo junto al reloj → joyero de coleta | Nil pequeño en el centro, sonrisa ladeada; Torete con sonrisa de suficiencia, brazos cruzados; joyero mira el reloj | joyero le ajusta el reloj en la muñeca | escena de joyería real, mostradores llenos | «"Te lo regalo"» (blanco borde negro, rayita a Torete) + «$50.000» (amarillo borde negro) | etiqueta de precio en amarillo | durante: se lo están poniendo | «Joyería Más Viral» | ¿de verdad le regala un reloj de 50.000 $? |
| 48 M | 2,20 (0,86) | cara de Nil sonrisa forzada → torres con piscinas → avenida | Nil cabeza ~30 %, sonrisa enorme de dientes, cejas arriba, mirada a cámara | apoyado en la barandilla, brazos sobre ella | Miami desde arriba con piscinas en cada azotea: vista rehecha, saturada | ninguno | — | durante | «20.000.000$» | ¿cómo es un piso de 20 millones? |
| 55 M | 2,16 (0,83) | cara con ojos enormes → curva de Mónaco con F1 → mono Red Bull | Nil ojos desorbitados (blanco alrededor del iris), boca entreabierta, mirada lateral a cámara | lleva mono Red Bull y cascos con micro | circuito de Mónaco con 4 F1 en curva (montaje/IA); mar | ninguno | logos Red Bull, Tag | durante | «País Más Rico del Mundo» | ¿qué hace Nil en un equipo de F1? |
| 50 M | 2,14 (0,83) | cara sonriente de Nil → amigo que le susurra → «ROLEX» verde | Nil selfi sonrisa de dientes; amigo (gorra) boca abierta, mano haciendo bocina | amigo se tapa la boca para cuchichear | tienda Rolex verde y oro, vitrina | ninguno | logo Rolex ×2 | antes | «Millonarios Del Barrio» | ¿qué le cuenta? ¿quién es millonario de barrio? |
| 45 M | 2,09 (0,82) | Nil con exoesqueleto → escalera blanca | Nil sonrisa, mira arriba-dcha. (fuera de cuadro) | baja la escalera agarrado a la barandilla con brazo robótico | exoesqueleto estilo Iron Man con núcleo azul que brilla; fondo blanco liso que lo hace saltar | ninguno | brillo azul en el pecho | durante | «JUGUETES» (mayúsculas) | ¿es real ese traje? |
| 54 M | 2,03 (0,78) | Alonso mirando de reojo → «No» amarillo → Nil con el móvil | Nil cejas arriba, boca entreabierta, mira a Alonso; Alonso de perfil, ceño, mira de reojo hacia Nil | Nil sostiene el móvil (pedir foto) | Mónaco y puerto detrás, saturado | «una foto?» (blanco borde negro, rayita a Nil) + «No» (amarillo borde negro, rayita a Alonso) | diálogo de dos bocadillos | durante: el rechazo | «Me Partió el Corazón» | ninguna: la imagen ya cuenta el chiste entero |
| 38 M | 2,02 (0,80) | dos caras mirándose de reojo → restaurante cálido | Abraham Mateo y Nil, miradas de sospecha laterales, bocas cerradas | Abraham pone la mano en el brazo de Nil | foto real con luz cálida | ninguno | — | durante | solo el nombre | ¿por qué se miran así? (débil) |
| 35 S | 2,01 | cara seria de Nil → «5 Billones.» → Apple Park con logo | Nil cabeza ~35 %, serio, ceja levemente alzada, mirada a cámara (duda) | — | Apple Park con manzana gigante en el cristal (añadida), césped y camino perfectos | «5 Billones.» arriba dcha., blanco borde negro, punto | cifra + logo Apple | antes: delante de la puerta | «Más Misterioso» | ¿qué hay dentro? ¿le dejan entrar? |
| 44 S | 1,77 | Guanyar con brazos cruzados → Nil explicando → peluche verde | Guanyar serio, mira fuera; Nil explica, cejas tristes, boca abierta | Guanyar brazos cruzados (cerrado); Nil manos abiertas | sofá de casa, foto real sin retoque | ninguno | — | durante: la conversación | «se va.» (minúsculas, punto) | ¿por qué se va Guanyar? (vídeo de comunidad) |
| 47 M | 1,66 (0,65) | burbuja de mensaje → Nil con mueca → interior rojo de Lamborghini | Nil labios apretados en sonrisa forzada, ojos de lado (incomodidad) | sujeta el móvil leyendo | asiento Lamborghini rojo y negro; burbuja tipo iMessage | «No voy a grabar con ustedes» en burbuja gris; foto y nombre del remitente **pixelados** | censura (pixelado), captura de chat | después: ya les ha dado plantón | «Nos Engañó» | ¿quién les engañó? (el pixelado lo esconde, pero el millonario anónimo no es nadie para el público) |
| 79 E | 1,52 (1,31) | moneda dorada con $ → cara de Nil maníaca → muchedumbre de manos | Nil boca abierta en mueca de dientes, ojos muy abiertos; amigo boca abierta | Nil levanta la moneda; decenas de manos se lanzan hacia él | multitud apretada (montaje o IA), todos mirando a la moneda | ninguno | moneda dorada = el dinero | antes: a punto de que le alcancen | título = nombre de la serie | ¿le quitarán los 100.000 €? ¿cómo se escapa? |
| 1 S | 1,50 | Porsche rojo polvoriento → «Nuevo coche» con flecha → Nil levantando la persiana | Nil boca en «o», cejas arriba, mira a cámara | agachado, levanta la persiana con un brazo (descubre) | Porsche 964 cubierto de polvo en garaje lleno de cajas (efecto «coche encontrado») | «Nuevo coche» blanco **sin borde**, letra fina moderna, ~10 % alto + flecha dibujada a mano | flecha curva blanca | antes: abriendo el garaje | «No Sé Si Funciona...» | ¿arranca? ¿está muerto? |
| 31 L | 1,50 (1,37) | cara de Nil con ojos de búho → dardo junto a la cara → mapa «LATAM 🏆» | Nil cabeza ~35 %, cejas muy alzadas, ojos redondos, boca cerrada, mirada a cámara; YSY A sonrisa de lado mirándole | Nil sostiene un dardo junto a la oreja; YSY A sujeta el mapa en alto | mapa de Latinoamérica verde sobre azul (atrezo/añadido), skyline detrás | «LATAM» rojo + copa, impreso **en el mapa** (texto diegético) | dardo + mapa = «al azar» | antes: va a lanzar | «¿Cuál…?» pregunta directa | ¿cuál gana? ¿a dónde le toca? |
| 12 L | 1,49 (1,83) | millonario sonriente en la puerta → «Déjame Entrar» → Nil fuera, preocupado | anfitrión sonrisa de dientes, mirada a cámara; Nil cejas arriba de súplica, boca entreabierta, mira a cámara | anfitrión hace gesto de «pasa» con las dos manos; Nil quieto, fuera | entrada de mansión con lámpara de araña y bandera dominicana; jardín tropical; muy pulido | «Déjame Entrar» blanco borde negro, rayita a Nil | mapa rojo con «20» abajo izq. | antes: en la puerta | «Vida de Un Millonario» | ¿qué hay dentro? ¿le deja entrar? |
| 18 L | 1,40 (1,57) | apretón de manos tipo pulso → dos sonrisas → ciudad de noche | Nil y WestCOL cabezas ~25 %, sonrisas de complicidad, se miran entre ellos | manos entrelazadas en alto (pulso/saludo) en el centro exacto | balcón con Medellín iluminado de noche (azul) contra luz cálida | ninguno | mapa «14» | durante | «24 Horas Con» + nombre | ¿cómo es pasar un día con WestCOL? (vive del nombre) |
| 40 S | 1,38 | cuatro personas sentadas → Lola hablando → Nil con la mano en la boca | todos serios o tristes; Nil pensativo, mano en la boca; nadie mira a cámara | cuerpos encogidos en un banco | fotograma real, sin retoque, luz plana gris | ninguno | — | durante: conversación seria | «Hola Lola» (2 palabras) | ¿qué ha pasado? (vídeo de comunidad, 7 min) |
| 32 S | 1,33 | cara de Nil sonriendo con llave → coche tapado con funda de cigarrillo gigante → «Su nuevo coche» | Nil sonrisa de dientes, ojos muy abiertos, mirada a cámara; Soul con las **manos en la cabeza**, boca abierta (shock) | Nil enseña la llave a cámara | funda del coche impresa como paquete de tabaco «SOULCAMEL NO FILTER / KIA-SOULONER», cigarrillo enorme en el techo: broma interna | «Su nuevo coche» blanco sin borde, letra moderna + flecha a mano; en la funda «Fumar mata, sacar fotos no» | flecha | antes: el coche aún tapado | «Coche de Sus Sueños» | ¿qué coche hay debajo? ¿le gusta? |
| 78 E | 1,28 (1,14) | cara de Nil escondido bajo el suelo → botas sobre la paja → horca | Nil ojos muy abiertos mirando arriba, boca entreabierta (miedo contenido) | encogido bajo las tablas, mano en la madera, la otra sujeta la moneda | granero: paja, botas de alguien de pie encima y una horca; telarañas | ninguno | moneda dorada con «2» abajo izq.; moneda $ en la mano | antes: a punto de que le encuentren | «Estoy a Salvo» (contradice la imagen) | ¿le pillan? ¿quién está encima? |
| 28 L | 1,24 (1,19) | dos chicos sentados en un bordillo → YSY A encogiéndose de hombros → bandera chilena | YSY A cejas arriba, boca abierta («¿qué?»); Nil mira de lado, preocupado, mano en la oreja | YSY A brazos abiertos; Nil se toca la cara | calle oficial de Santiago, real; **no hay ningún policía en la imagen** | ninguno | mapa «4» | después: comentan lo que han visto | «Nunca Había Visto» + «Así» | ¿cómo son esos policías? (la imagen los esconde por completo) |
| 30 L | 1,20 (1,12) | dos caras sonrientes → bandera argentina → Obelisco | selfi; YSY A sonrisa ladeada, Nil sonrisa enorme | YSY A hace un gesto con los dedos y anillos | Obelisco + bandera: postal, cielo limpio | ninguno | mapa «2» | durante | «Entendí Por Qué» | ¿por qué es especial? |
| 27 L | 1,15 (1,12) | tres trofeos dorados en forma de gaviota → abuela en el centro → Pablo Chill-E abrazándola | todos sonríen; abuela con gafas, mirada tierna | cada uno sostiene una gaviota (trofeo de Viña) | Valparaíso de colores + bandera chilena + cordillera nevada | ninguno | mapa «5» | después: les han dado el premio | «24 Horas Con» + nombre | ¿por qué tienen gaviotas? ¿quién es la abuela? |
| 36 S | 1,09 | billete de 5 € ardiendo → cara de Nil asustada → amigos | estilo ilustración/caricatura (pintado o IA): Nil ojos grandes asustado; amigo de rojo con gesto chulo | amigo quema un billete de 5 €; otro alarga la mano para agarrarlo | todo dibujado: ciudad, avión, edificio con logo «Schweppes» | «sin dinero.» blanco borde negro, minúsculas, punto | billete ardiendo | durante | «Sobreviví» + «Sin Gastar» | ¿cómo se sobrevive 21 días sin dinero? |
| 7 L | 1,06 (1,41) | presos tatuados en fila → Nil con cámara → cartel «EL SALVADOR» | Nil serio, cejas planas, mirada a cámara (grave); presos con la cabeza gacha | Nil sujeta la cámara con micro hacia nosotros y se apoya en el cartel | fila de pandilleros del CECOT con soldados y alambradas (montaje, imagen de prensa recreada) | «No Entré.» negro **sin borde**, letra moderna, punto, arriba izq.; cartel «EL SALVADOR» en la escena | mapa «25» | antes/no-pasa: delante de la cárcel | «Por Esta Razón» | ¿por qué no entró? |
| 19 L | 1,06 (1,17) | sonrisa de Nil sin camiseta → Ovy al volante con gafas → mansiones en el lago | selfi, los dos sonríen | Ovy le pasa el brazo por el hombro | lancha, estela, bandera colombiana, casas de lujo en Guatapé: saturado | ninguno | mapa «13» | durante | «Lujosa Vida» + nombre | ¿cómo vive Ovy? (molde de #52) |
| 77 E | 1,06 (0,97) | cara de Nil mirando atrás → hatillo con bolsa verde → medallón $ | Nil cejas juntas, mira por encima del hombro (le siguen) | lleva un palo al hombro con una bolsa de basura verde (hatillo de vagabundo) y un medallón $ colgando | desierto rojo tipo Gran Cañón, carretera: fondo pegado | ninguno | moneda «3»; medallón $ | durante: huyendo | «Solo en el Desierto» | ¿le alcanzan? |
| 26 L | 1,05 (1,04) | cara sonriente al volante → volante → ciudad borrosa | sonrisa de dientes, mira al frente | conduce con una mano, la otra en el techo | interior de Porsche GT con jaula; fondo con desenfoque de velocidad | ninguno | mapa «6»; logo Porsche en la gorra | durante | «24 Horas Con Millonarios» | ¿de quién es el coche? (débil) |
| 74 E | 1,02 (1,02) | bola transparente gigante → Nil dentro → dos amigos cruzando el paso de cebra | caras pequeñas, de perfil | Nil empuja la bola por dentro | paso de cebra estilo **Abbey Road** (guiño a los Beatles), bola agrandada | ninguno | moneda «7» | durante | «Imposible de Atrapar» | ¿por qué va en una bola? |
| 76 E | 1,00 (0,94) | cara con dientes apretados → moneda $ → moto persiguiendo | Nil dientes apretados en mueca (miedo-euforia), ojos muy abiertos, a cámara | asomado por la ventanilla, enseña la moneda | furgoneta, carretera con desenfoque de movimiento, motorista con casco detrás | «120km/h» blanco borde negro, arriba dcha. | moneda «5»; cifra de velocidad | durante: la persecución | «Persecución Extrema» | ¿le pillan? |
| 13 L | 0,98 (1,19) | cara de asco de Nil → mitad izq. barrio con bidón ardiendo → mitad dcha. calle colonial | Nil dientes apretados en mueca de asco, ojos muy abiertos, cejas arriba | — | **imagen partida en dos** con Nil en el eje; su ropa también partida (camiseta / traje); fuego, basura, bandera | ninguno | partida mejor/peor; mapa «19» | durante | «"MEJOR" y el "PEOR"» | ¿tan grande es la diferencia? |
| 16 L | 0,97 (1,12) | tarjeta dorada → cara seria de Nil con gorro → Pagani rojo | Nil serio, cejas planas, mirada a cámara | enseña la tarjeta «GOLD / EXPLORE THE AMERICAS» | rascacielos de Panamá, Pagani rojo brillante, bandera | ninguno | tarjeta; mapa «16» | durante | «País Más Rico» | ¿cuál es? (el título no dice el país; la bandera sí) |
| 73 E | 0,97 (1,00) | cara de Nil asomando del arbusto → dos amigos buscando con la mano en la frente | Nil dientes apretados, ojos muy abiertos (escondido); amigos boca entreabierta, oteando | amigos con la mano de visera (gesto de buscar) | arbusto verde tapando a Nil; ciudad mediterránea detrás | ninguno | moneda «8» | antes: no le han visto aún | «Esto No Es Un Juego» | ¿le encuentran? |
| 75 E | 0,97 (0,94) | «YO» gigante → flecha roja → islote rodeado de cientos de kayaks | Nil diminuto (círculo rojo), sin cara | — | isla vista desde arriba rodeada de kayaks y barcas (imagen generada/montada) | «YO» blanco borde negro, enorme (~20 % alto) | flecha roja + círculo rojo | durante: rodeado | «Aislados» | ¿cómo sale de ahí? |
| 9 L | 0,93 (1,20) | mural de Bad Bunny → tres hombres hablando → casas de colores | caras pequeñas, de perfil, sin expresión marcada | Nil brazos cruzados, escucha | foto real de calle en Puerto Rico; bandera; **sin número de episodio** | ninguno (el nombre está en el mural) | — | durante | «Barrio de Bad Bunny» | ¿cómo es su barrio? |
| 68 E | 0,90 (1,05) | cifras de pi en blanco → chico de rojo recitando → Nil con micro asombrado | concursante mira abajo, concentrado; Nil cejas arriba, boca entreabierta | Nil le tiende el micro | calle con vegetación, real | «3,14159265358979 / 3238462…383279 / 502884…9937510» blanco borde negro, tres líneas que **se desvanecen** y tapadas por las cabezas | moneda «13» (es episodio de Escapando aunque el título no lo diga) | durante: está recitando | «Ganó 100.000€» | ¿llega? ¿cuántas cifras? |
| 14 L | 0,88 (1,05) | «"Ven aquí si tienes huev*s"» amarillo → chico de blanco gesticulando → Mercedes negro | caras pequeñas; el chico grita con la mano abierta; Nil de espaldas en primer plano | Nil de espaldas, cuerpo tenso | coche negro de lujo, portal | «"Ven aquí si tienes huev*s"» amarillo grande (~25 % del alto en dos líneas), comillas, asterisco de censura, rayita amarilla al chico | asterisco; mapa «18» | durante: el encontronazo | «Se Enfrentó» | ¿se pegan? |
| 22 L | 0,88 (0,93) | «Peligroso?» → cara de Nil asomando por la esquina → favela de noche con bandera | Nil cejas arriba, mirada de reojo a cámara (miedo cómico) | se asoma agarrado a la esquina | callejón de favela nocturno, moto, perro, bandera: escena muy construida | «Peligroso?» blanco sin borde, letra moderna, arriba izq. | mapa «10» | antes | «Realmente Es Tan Peligroso?» | ¿lo es? |
| 25 L | 0,88 (0,88) | cara de Nil desconfiada → cartel «Bienvenido a Perú» → bandera | Nil cejas juntas, mirada de reojo a cámara, boca cerrada | mochilero: agarra las correas, bandera clavada en la mochila | carretera de extrarradio con skyline: montaje limpio | cartel «Bienvenido a Perú» (texto diegético) | mapa «7» | antes: llegando | «Mi Primera Vez» | ¿qué se encuentra? (floja) |
| 62 E | 0,88 (1,19) | cifras «"3.1415926535 897…846…"» → Nil sonriendo mirando arriba → chico con camiseta de Chile | concursante serio; Nil sonrisa, mira hacia las cifras | — | noche, fotograma real | «"3.1415926535 / 897…846…"» blanco borde negro, entre comillas, tapado por las cabezas | moneda «18» | durante | «Lo Siento Mucho» (no tiene que ver con la imagen) | ¿qué siente? ¿qué pasó? (título-confesión) |
| 65 E | 0,87 (1,07) | tres caras de abuelo de látex → Nil en el centro con «shh» → medallón $ | ojos muy abiertos, Nil dedo en los labios, mirada a cámara | uno señala a cámara, otro mano al pecho | maquillaje de anciano (prótesis), paisaje de río | ninguno | moneda «15»; medallón $ | durante: disfrazados | «DE INCÓGNITO» | ¿les reconocen? |
| 4 L | 0,86 (1,20) | cara preocupada de Nil → trofeo del Mundial gigante → acampada de protesta ante el Azteca | Nil cejas arriba de preocupación, boca entreabierta, a cámara | mano abierta señalando el campamento («mira esto») | Estadio Azteca, trofeo enorme, tiendas y pancartas «NO AL DESALOJO», «JUSTICIA SOCIAL»: escena generada | pancartas (diegético) | mapa «28» | después/durante | «No Es Como Esperaba» | ¿qué pasa en México? |
| 10 L | 0,86 (1,09) | AK-47 en alto → cara de Nil asustada → segundo fusil | Nil ojos muy abiertos, boca entreabierta, mirada lateral a cámara (miedo) | sostiene un AK-47 con una mano, otro fusil a la espalda | Puerto Rico (bandera en la gorra y al fondo), palmeras: rehecho | ninguno | mapa «22» | durante | «Armas Son Obligatorias» (afirmación chocante) | ¿qué país es? ¿de verdad? |
| 69 E | 0,84 (0,98) | mano arrancándole la cadena → cara de dientes apretados → patinete | Nil mueca de dientes, ojos desorbitados, a cámara; ladrón con ceño | el ladrón tira de la cadena con el medallón $ desde un patinete | aparcamiento de camiones | ninguno | moneda «12»; medallón $ | durante: el tirón | «El Peor Día...» | ¿le roban el dinero? |
| 24 L | 0,83 (0,85) | cara llorando → lágrimas → ventanilla de avión | Nil llorando: ojos rojos, lágrimas, cejas de pena, pelo mojado; a cámara | sentado | avión; lágrimas y enrojecimiento muy marcados (retoque o IA) | ninguno | mapa «8» | después | «ME TRAUMÓ» (mayúsculas) | ¿qué le pasó en Perú? |
| 29 L | 0,83 (0,78) | «Vale la pena?» → cara escéptica → bandeja de carnes | Nil ceja alzada, boca torcida (escepticismo), a cámara | cuchillo y tenedor en alto | placa «DON JULIO / MEJOR RESTAURANTE ARGENTINA» con sello (inventada), carnes perfectas | «Vale la pena?» blanco sin borde + raya vertical hacia el plato | mapa «3» | antes: va a probar | «Más FAMOSO» + «¿Sobrevalorado?» | ¿lo está? |
| 72 E | 0,83 (0,88) | cara con dientes apretados → moneda $ → bosque desde arriba | Nil mueca de esfuerzo/miedo, ojos muy abiertos, a cámara | abrazado al tronco, enseña la moneda | vista cenital del bosque (vértigo) | «12 Horas.» blanco borde negro, punto | moneda «9» | durante | «Supervivencia Extrema» | ¿aguanta 12 horas ahí? |
| 21 L | 0,82 (0,88) | Nil agachado señalando → favela → niños en la pista | Nil cejas arriba, a cámara | **señala** la favela con el índice | favela vista desde arriba, mar al fondo; camiseta de Brasil | «📍Favelas» blanco sin borde con icono de ubicación | icono de pin; mapa «11» | durante | «DENTRO DE» (mayúsculas) | ¿qué hay dentro? |
| 60 E | 0,81 (1,16) | cara seria de Nil → manos contra los cristales → gente gritando | Nil serio, cejas algo alzadas, boca entreabierta (shock contenido); fuera, bocas gritando | gente apoyando las manos en las ventanillas | coche rodeado; medallón con **π** | «atrapado.» blanco sin borde, minúsculas, punto | moneda «20» | durante: rodeado | «No Podemos Escapar» | ¿cómo salen? |
| 61 E | 0,78 (1,09) | Nil con sombrero y manos abiertas → amigos serios a los lados → mesa | Nil cejas planas, «tengo que explicaros»; amigos serios, uno brazos cruzados | manos abiertas a cámara | mesa de jardín; medallón «21» | ninguno | moneda «19» | antes: la charla | «Tenemos Que Hablar...» | ¿qué tiene que decir? |
| 70 E | 0,78 (0,88) | cabeza enterrada → gaviota enorme → pala | Nil mueca de asco/duda, boca torcida | solo la cabeza fuera de la arena | gaviota agrandada (casi del tamaño de la cabeza), estrella de mar, pala: playa limpia | «Enterrado.» blanco sin borde, letra fina, punto | moneda «11» | durante | «La Playa» (neutro) | ¿por qué está enterrado? |
| 17 L | 0,76 (0,87) | J Balvin → Nil mirándole de reojo → plato enorme con bocado diminuto | los dos de reojo, bocas cerradas (desconcierto) | Nil con tenedor en alto | restaurante de alta cocina dorado; plato con ración mínima | ninguno; **sin número de episodio** | — | antes: van a comer | «JBalvin Nos Trajo» | ¿Balvin come con ellos? (la imagen promete más que el título) |
| 67 E | 0,76 (0,91) | móvil con «-100.000€» → cara de labios apretados → medallón $ | Nil labios apretados (sonrisa forzada, «ups»), ojos abiertos | enseña el móvil con una mano y el medallón con la otra | cielo y ciudad lisos | «-100.000€» en una notificación tipo PayPal en la pantalla | moneda «14»; captura de app | después | «-100.000€» | ¿ha perdido el dinero? |
| 64 E | 0,75 (0,95) | cara de labios apretados → medallón $ → mansión vigilada de noche | Nil labios apretados, ojos abiertos, a cámara | selfi enseñando el medallón | mansión con cámaras, guardias con linterna: nocturno, azul | ninguno | moneda «16» | antes | «¿EL FINAL?» | ¿le pillan? ¿se acaba? |
| 15 L | 0,74 (0,87) | Nil sin camiseta serio → remo → playa de catálogo | Nil serio, mirada a cámara | sostiene un remo de paddle | playa perfecta con cabañas y tumbonas (generada); **nada dice «falso»** | ninguno | mapa «17» | durante | «FALSO» (mayúsculas) | ¿por qué falso? (la imagen no ayuda) |
| 71 E | 0,72 (0,79) | maletín con «?» enorme → cara de duda → medallón $ | Nil ceja alzada, labios fruncidos (duda) | un brazo con el medallón, el otro con el maletín: **balanza** | paseo marítimo | «?» negro gigante pintado en el maletín | moneda «10» | antes: la elección | «El Maletín o El Dinero» | ¿qué elige? |
| 11 L | 0,70 (0,87) | «"Me has estafado"» → móvil con videollamada «Rubius» → cara de Nil de reojo | Nil cejas arriba, mira de reojo a cámara (pillado) | enseña el móvil a cámara | playa dominicana, bandera; pantalla de llamada entrante con la cara de Rubius | «"Me has estafado"» blanco sin borde, comillas, rayita al móvil | captura de llamada; mapa «21» | durante | «RUBIUS?» (nombre + interrogación) | ¿qué le ha hecho a Rubius? |
| 63 E | 0,70 (0,92) | selfi de tres caras → Dua Lipa en el escenario → flecha amarilla | Nil sonrisa de dientes, ojos muy abiertos; dos señoras sonrientes | selfi | escenario morado con Dua Lipa de amarillo flúor (pegada) | «dua lipa» blanco sin borde, minúsculas | flecha amarilla a la cantante; moneda «17» | durante | «Dua Lipa» | ¿quiénes son las señoras? (floja) |
| 2 L | 0,69 (0,99) | rótulo rojo de noticiario → Nil con la mano en el pecho → gente evacuada | Nil mira fuera de cuadro, boca entreabierta, mano al pecho (susto) | mano en el pecho | calle de CDMX con gente fuera; **rótulo falso de TV** «ÚLTIMA HORA / SE REGISTRA SISMO DE MAGNITUD 5.6 / EPICENTRO EN OMETEPEC, GUERRERO» + «EN DIRECTO» | el rótulo de noticiario (~20 % del alto) | mapa «30» | durante/después | «Sismo de 5.6» | ¿cómo lo vivieron? (el rótulo lo cuenta todo) |
| 59 E | 0,69 (1,00) | cifras de pi → policía nacional haciendo un «2» → amigos con móviles | policía habla; amigos concentrados en el móvil, uno mano en la barbilla | policía con dos dedos, botella de agua | uniforme de Policía Nacional | cifras de pi en tres líneas que se desvanecen (blanco borde negro) | moneda «21» = **final de Escapando** con título suelto | durante | «Ganó 25.000€» | ¿cuántos números? (poco claro qué pinta el policía) |
| 3 L | 0,66 (0,93) | dos chicos mirando arriba → «Extraño.» → Zócalo con bandera | miran fuera de cuadro arriba-izq.; Nil brazos cruzados, recelo | brazos cruzados | Zócalo y catedral, bandera mexicana: limpio | «Extraño.» blanco borde negro, punto | mapa «29» | durante | «No Es Como Lo Imaginábamos» | ¿qué es extraño? |
| 20 L | 0,64 (0,70) | cara de Nil → mano adelantada hacia cámara → «amenazados.» | Nil cejas arriba, boca entreabierta, a cámara | mano abierta adelantada («espera») | noche, portátil; fondo oscuro | «amenazados.» blanco sin borde, minúsculas, punto | **sin número** | después: lo cuenta | «Nos Amenazan» | ¿quién? (pero la imagen es «un chico hablando») |
| 6 L | 0,59 (0,80) | plato de vieiras → Nil colocándolo → amigo mirando fuera | sin expresión marcada; amigo mira fuera de cuadro | Nil sostiene el plato | restaurante con vistas a San Salvador, real y bonito | ninguno | mapa «26» | durante | «LUJO» (mayúsculas) | ninguna fuerte |
| 23 L | 0,55 (0,57) | Nil tumbado en el césped → piernas de alguien de pie → botella | Nil mira arriba a quien está de pie, agotado | tumbado, manos tras la nuca | **la persona que «aparece» está cortada a la altura de las rodillas** (solo pantalón blanco y zapatillas) | ninguno; sin número | — | después | «Apareció» | ¿quién apareció? (oculto… y aun así el peor residuo de LATAM) |
| 8 L | 0,54 (0,71) | cara de Nil con la boca abierta → amigo serio → interior de buggy | Nil boca abierta, cejas arriba, a cámara; amigo serio | Nil sujeta algo pequeño roto en la mano | buggy, calle de Puerto Rico; foto real | ninguno; sin número | — | después | «No Esperábamos Un Accidente» | ¿qué accidente? (no se ve ninguno) |
| 33 S | 0,53 | **la misma miniatura que #37** (tarjeta dorada, grupo, mansión y helicóptero) | igual que #37 | igual | igual | ninguno | — | antes | «(mala idea)» | ninguna nueva: ya se vio |
| 5 L | 0,51 (0,70) | Nil hablando a cámara → volcán humeante → flecha roja | Nil cejas de preocupación, boca abierta hablando | amigo sostiene una roca volcánica | volcán con humo, lava negra | ninguno | flecha roja al cráter; mapa «27» | durante | «Más Catastrófico» | ¿por qué catastrófico? (imagen de vlog normal) |
| 66 S | 0,47 | tres ancianos de látex → barriga → logo vevo | caras de concentración | tocan la barriga del grande | campo deportivo; los disfraces de #65 | logo «vevo» | — | — | «(Official Music Video)» | ninguna |
| 34 S | 0,40 | prismáticos → «21 DÍAS» en un cristal → MrBeast dibujado en el otro | dibujo: boca abierta enorme | sujeta prismáticos | ilustración de dibujos animados, ciudad de NY | «21 DÍAS» dentro de la lente | MrBeast caricaturizado | antes | «Conocer a MrBeast - La Película» | ¿lo conoce? (pero es una recopilación de 178 min) |

Nota de conteo: 79 filas, en el orden de las hojas de detalle. Dos
hallazgos de la tabla que no salen en el título: **#68 y #59 son episodios de Escapando** (moneda «13» y «21», el
segundo es el final: su descripción dice «Se acabó, gracias a todxs») publicados **sin el sufijo de la serie**, y
**#33 es la miniatura de #37 volteada en espejo** (la tarjeta pone «ASIV»; misma foto, 2,54 frente a 0,53).

## 3. Anatomía de la miniatura

Recuentos sobre los 79 salvo que diga «series» (los 70 episodios de las tres series, que son los que tienen residuo).

### Jerarquía
- **Lo primero que se ve** (mi primera parada del ojo en la tabla): la cara de Nil u otra cara en 47; un objeto de lujo
  o de dinero (tarjeta, moneda, llave, móvil, botella, avión, maletín, coche) en 14; un texto en 8 («Secuestro.»,
  «YO», «"Ven aquí si tienes huev*s"», las cifras de pi ×3, el rótulo del sismo, la burbuja de #47); una escena sin cara
  dominante en 10 (#42, #74, #75, #9, #27 los trofeos, #17, #66, #34, #23, #40).
- **Por qué**: la cara gana por tamaño (en las de un solo protagonista la cabeza ocupa ~25–40 % del alto) y por estar
  casi siempre en el tercio derecho o centro-derecha con la mirada a cámara (44 de 70 en series). Cuando el objeto gana
  es porque está **en primer plano, más cerca de cámara que la cara** (tarjeta #58 y #16, móvil #43 y #11, moneda #79,
  llave #51, botella #43, maletín #71) o porque es dorado/rojo sobre azul.
- **Nº de elementos con significado**: 2–3 casi siempre (cara + escenario de lujo, o cara + objeto + texto). Con 4 o
  más: #46 (joyero, Nil, Torete, reloj, «$50.000», cita) y #13 (dos barrios, ropa partida, fuego, bandera). Las de un
  solo elemento (cara hablando sin contexto: #20, #5, #8) están entre las peores de LATAM.
- **¿Se entiende sin leer?** Sí en ~60: el escenario cuenta el tema (jet, mansión, favela, cárcel, desierto). No en
  #28 (dos chicos en un bordillo), #20, #8, #23, #61, #62, #68, #59, #40, #44: ahí la imagen es «gente hablando» y el
  título lo es todo. De esas 10, las de series tienen residuo mediano ~1,0, pero con extremos: #28 (1,19) y #62 (1,18)
  funcionan porque el título abre un hueco; #23 (0,57), #20 (0,69), #8 (0,71) no.
- **Qué se pierde en pequeño** (hojas de 16): sobreviven las caras, los textos de 1–2 palabras en bloque («Jet
  Privado.», «1 Billón.», «YO», «Secuestro.»), el número de episodio y las banderas. Se pierden: la burbuja de chat de
  #47 (ilegible), las cifras de pi (se leen como «muchos números», que basta), el letrero «DON JULIO» de #29, la
  funda «SOULCAMEL» de #32 (el chiste desaparece), los presos de #7 (se ven como fila blanca), el bocado diminuto de
  #17 (el gag del plato enorme no se ve).

### Cara y cuerpo
- **Quién**: Nil sale reconocible en ~73 de 79 (no en #41, sola Lola Lolita; #34 dibujo; #66 videoclip; casi
  invisible en #42 y #75). Solo: 32 de 70 en series; con 1 persona más: 24; con 3+: 14. **Residuo: solo 0,90,
  con otra persona 1,06, con grupo 1,03**: en este canal la cara de Nil a solas rinde menos que Nil con alguien.
- **Mirada**: a cámara 44 de 70 (residuo mediano 0,95); fuera de cuadro 19 (1,02); entre ellos 6 (0,99). La mirada
  a cámara es la norma y no da ventaja. La mirada fuera de cuadro que **señala algo que no vemos** está en la nº 1
  (#52: los dos miran arriba-izquierda) y en #57 (mira por la ventanilla al Burj Khalifa: aquí sí lo vemos).
- **Ojos**: muy abiertos (blanco visible alrededor del iris) en 26 de 70; residuo 1,00 frente a 0,98: **la cara de
  «ojos como platos» no separa nada**. En LATAM, 6 casos con 1,14; en Escapando, 11 casos con 0,96.
- **Boca**: sonrisa de dientes 17 (residuo **1,12**), entreabierta 20 (1,02), mueca de dientes apretados 7 (0,96),
  cerrada 23 (**0,92**). La boca cerrada abarca la cara seria-plana (#16, #15, #7), labios apretados de «ups»
  (#47, #64, #67) y la ceja escéptica (#29, #71): todas por debajo de la sonrisa.
- **Cejas**: alzadas casi siempre que hay sorpresa; juntas/fruncidas solo en #77 (huye), #25 (desconfía), #5 (habla
  preocupado) y #13 (asco). Ceja única alzada (escepticismo) en #29, #71, #58 (el amigo): 2 de 3 abajo.
- **Manos**: sujetan un objeto hacia cámara en 19 (tarjeta, moneda, llave, móvil, plato, trofeo, fusil, dardo);
  señalan con el índice en 4 (#56 al hotel, #21 a la favela, #37 a la tarjeta, #65 a cámara); mano abierta de
  «mira esto» en 5 (#52, #39, #4, #12 el anfitrión, #20); manos al pecho 2 (#53, #2); «shh» 1 (#65); manos en la
  cabeza 1 (#32, Soul); brazos cruzados (cierre, enfado) 4 (#44, #61, #46, #9). Que alguien **señale** no da ventaja
  (residuo 1,01 con, 0,99 sin).
- **¿La emoción es la que tocaría?** Casi siempre sí y exagerada un grado: miedo cómico al esconderse (#73, #78),
  dientes apretados en la persecución (#76), asco en el barrio pobre (#13), llanto en «ME TRAUMÓ» (#24). Las
  discordantes son a propósito y son las de segunda lectura: #78 cara de pánico con título «Estoy a Salvo»; #12 Nil
  preocupado mientras el millonario le invita a pasar con «Déjame Entrar».
- **Ropa**: funciona como bandera: camiseta de Argentina (#30), de Brasil (#21, #22), de México (#4), mono de Red
  Bull (#55), traje para el lujo (#37), media camiseta-medio traje para el «MEJOR y PEOR» (#13), jersey rojo o azul
  liso en Escapando (color plano que se recorta solo). La ropa de Nil casi siempre es lisa y saturada.

### Sujeto
- Exagerado por **tamaño** en 8: botella de Moët más alta que una persona sentada (#43), maletín con «?» enorme
  (#71), gaviota casi del tamaño de su cabeza (#70), trofeo del Mundial gigante (#4), bola transparente (#74), bolso
  LV adelantado (#41), móvil en primer plano (#43, #11). Por **color irreal**: avión dorado (#39), coin dorada (#79 y
  todo Escapando). Por **imposible**: el Burj Khalifa asomando entre nubes junto a la ventanilla (#57), la isla
  rodeada de cientos de kayaks (#75), la muchedumbre de manos (#79), la ciudad de Panamá con un Pagani a la puerta
  (#16).
- **Nitidez**: todo nítido de borde a borde, sin desenfoque de fondo salvo el de velocidad en #26 y #76. Caras
  suavizadas y muy enfocadas; dientes y ojos aclarados (visible a tamaño completo en #39 y #41).
- **Contornos**: **ninguna** miniatura lleva contorno blanco ni halo visible alrededor de las personas. Los
  recortes están fundidos con el fondo (la luz casa más o menos; en #41 y #12 se nota algo el pegado por la luz
  distinta entre persona y fondo, no por un borde).

### Lo que NO se enseña
- **Ocultado a propósito** en 9: el remitente pixelado de #47 (0,65), las piernas sin cuerpo de quien «apareció» en
  #23 (0,57), los policías que no salen en #28 (1,19), lo que miran Coscu y Nil en #52 (1,65), el coche bajo la funda en
  #32 (1,33), el contenido del maletín «?» en #71 (0,78), quién está encima de las tablas en #78 (1,15), la cara de
  quien busca en #73 (0,99), el interior del CECOT en #7 (1,41).
- Mediana de esas 8 en series: ~1,07, pero **partida en dos**: cuando lo oculto es **una persona desconocida** (el
  millonario que les deja plantados, el que «apareció») el residuo es el peor de su serie; cuando lo oculto es **un
  lugar, un objeto o una escena** (policías, cárcel, lo que hay delante de la mansión, quién pisa encima) va por
  encima de 1,1. Esconder a alguien que el público no conoce no crea curiosidad: no hay a quién imaginar.
- El censurado de palabras (asterisco en «huev*s», #14) es de tono, no de misterio: 1,05.

### El instante
- **Antes** de que pase: 19 de 70 (residuo 0,99); **durante**: 43 (1,02); **después**: 8 (**0,78**). Las de
  «después» son #47 (ya les dieron plantón), #67 (ya perdió el dinero), #24 (ya llora), #23 (ya está tirado), #20 (ya
  le amenazaron, lo cuenta), #8 (ya pasó el accidente), #28 (ya vieron a los policías) y #27 (ya tienen el premio). Las
  dos que se salvan son las que no cuentan una desgracia (#28 y #27). **Enseñar la consecuencia en vez del suceso
  es lo que peor funciona aquí.**
- **Amenaza inminente** dibujada (alguien a punto de alcanzarle, encontrarle o quitarle algo): 11 (#79, #78, #77,
  #76, #73, #69, #60, #64, #42, #22, #10). Residuo 0,99: en Escapando, donde es la plantilla, no distingue un
  episodio de otro.

### Fondo y profundidad
- Fondo **que cuenta** (localiza o es el lujo mismo) en ~70: mansión, jet, Burj Al Arab, Mónaco, Apple Park,
  favela, cárcel, Obelisco, Zócalo, desierto. Fondo solo de color: #48 y #67 (cielo), #45 (escalera blanca, para
  que el exoesqueleto salte), #20 (noche).
- **Tres capas** casi siempre: objeto en primer plano (comida #43, tarjeta, móvil, plato #29) / cara / escenario
  limpio. Horizonte bajo, cielo azul que ocupa el tercio superior y deja sitio para el texto arriba a la derecha.
- **Rehecho**: en ~45 el fondo tiene aspecto de imagen generada o recompuesta (arquitectura perfecta, cielos sin
  defecto, piscinas en cada azotea, logos limpísimos). En ~25 es fotograma real retocado (#49, #50, #18, #19, #28, #9,
  #6, #5, #2, #62, #68…). En 8 es fotograma casi bruto (#23, #8, #40, #44, #66, #28, #6, #9).

### Color y luz
- Mandan **azul cielo + piel cálida + un acento saturado** (rojo: coche, tarjeta, camiseta; dorado: avión, moneda,
  tarjeta; verde: camiseta Celtics, Rolex, bandera). Luz de día, alta, sin sombras duras, saturación alta y
  contraste local fuerte (aspecto «HDR» limpio). Nocturnas solo 6 (#18, #22, #20, #64, #49, #60 a medias).
- **El oro es el código del dinero**: monedas y medallones $ (10 en Escapando + el distintivo del episodio en 19),
  tarjeta dorada (#37, #33, #16), avión dorado (#39), trofeos dorados (#27), estrellas amarillas (#56), «$50.000» en
  amarillo (#46), «No» de Alonso en amarillo (#54), «Ven aquí…» en amarillo (#14). El amarillo de texto solo aparece
  en 4 y siempre para la palabra que pica (precio, negativa, insulto, flecha a la famosa).
- Lo más claro de la imagen es casi siempre el cielo o la ropa blanca de Nil; no hay viñeta marcada.

### Texto
- **Texto añadido** (no del escenario) en 32 de 79; sin texto añadido 47. Residuo en series: con texto 0,94 (32
  casos contando los diegéticos), sin texto 1,01. **Poner texto no ayuda ni estorba.**
- **Palabras**: 1–3 en 24 de 32 («Jet Privado.», «1 Billón.», «Secuestro.», «YO», «atrapado.», «No Entré.»). Las
  citas llegan a 5 («"Ven aquí si tienes huev*s"»). Las cifras de pi son la excepción (texto como textura).
- **Cuatro estilos**, con fecha:
  1. **Bloque**: blanco, grueso, borde negro de ~4–5 px a 1280, casi siempre con **punto final**, arriba a la
     derecha, ~8–10 % del alto (#43, #39, #42, #35, #36, #3, #72, #76 sin punto, #75 «YO» enorme). Es el de 2025.
  2. **Limpio**: blanco sin borde, letra geométrica moderna, a veces en minúsculas con punto («atrapado.»,
     «amenazados.», «dua lipa», «Enterrado.», «Peligroso?», «Vale la pena?», «No Entré.» en negro). Aparece ya en
     Escapando (#70, #60, #63) y domina en 2026.
  3. **Cita con rayita**: entre comillas tipográficas, con una raya fina que apunta a quien habla («"compra un
     coche"», «"Te lo regalo"», «una foto?» / «No», «"Ven aquí si tienes huev*s"», «Déjame Entrar», «"Me has
     estafado"»). 7 casos, residuo mediano 1,05; los dos mejores (#12 1,83 y #58 1,45) son citas.
  4. **Interfaz**: burbuja de chat (#47), llamada entrante con la cara de Rubius (#11), notificación de app con
     «-100.000€» (#67), rótulo de telediario «ÚLTIMA HORA» (#2). 4 casos, residuo mediano ~0,9.
- **El punto final** («Jet Privado.», «Secuestro.», «No Entré.», «atrapado.»…): 11 casos. En series, con punto
  mediana 1,04 (n=9); textos sin punto 0,93 (n=7). Indicio débil, pero el punto convierte la etiqueta en veredicto.
- **Relación con el título** (32 con texto): eco literal de una palabra 7 (#20 «amenazados.» / «Nos Amenazan»,
  #22, #21, #63, #36, #67, #7) → mediana ~0,92; paráfrasis o sinónimo 7 (#43 «Jet Privado.» / «Avión Privado», #39
  «1 Billón.» / «Billonario», #3, #60, #29, #1, #32) → ~1,15; complemento que añade un dato (cifra, lugar, escalada:
  #57 «Primera Clase», #42 «Secuestro.» sobre «Robo», #35 «5 Billones.», #72, #76, #75, #70) → ~0,94; cita 7 → 1,05;
  interfaz 4 → ~0,9. **Repetir la palabra exacta del título es lo que menos rinde; decir lo mismo con otra palabra,
  lo que más.**

### Recursos gráficos
- **Marcador de episodio** abajo a la izquierda: silueta roja de Sudamérica con el número de episodio en blanco en
  LATAM (24 de 30; faltan #31 el primero, #9, #8, #17, #20, #23) y moneda dorada con el número en Escapando (19 de 20;
  falta el primero). Millonarios no lleva ninguno. En LATAM, los 5 episodios sin número tienen residuo mediano
  **0,71** (#9 1,20, #17 0,87, #8 0,71, #20 0,69, #23 0,57) frente a ~1,05 de los numerados: no creo que el número
  sea la causa, sino que son las miniaturas hechas con menos cuidado (#8 y #23 son fotogramas con barra negra o sin
  retocar).
- Flechas 5 (#1 y #32 blancas dibujadas a mano, #75 y #5 rojas, #63 amarilla); círculo 1 (#75); rayitas de cita 7;
  cifras en imagen 11; pixelado 1 (#47); asterisco 1 (#14); imagen partida 1 (#13, 1,19); icono de ubicación 1 (#21);
  capturas de interfaz 4; logos de marca de lujo ~12 (Moët, LV, Rolex, Rolls-Royce, Red Bull, Apple, Porsche,
  Lamborghini, Mastercard/Visa, Mercedes); banderas en ~15 de 30 de LATAM + camisetas de selección en 4; ilustración
  2 (#34, #36); «?» pintado 1 (#71, 0,78, el peor de Escapando).
- Ningún recurso gráfico concreto separa los mejores de los peores dentro de su serie.

### Marca
- Reconocible sin nombre por: **Nil centrado-derecha con cara expresiva y ropa lisa**, escena de lujo o de reto
  hiperlimpia y saturada, cielo azul, objeto de dinero dorado y el marcador de episodio abajo a la izquierda.
- **Evolución**: Escapando (abr–may 2025): todo construido, amenaza + moneda, la más «MrBeast»; Millonarios (may–jun
  2025): lujo real o rehecho, invitados, texto en bloque con punto; sueltos de 2025: ilustración para las películas
  (#36, #34); LATAM (may–jun 2026): más fotogramas reales, banderas, mapa numerado, texto limpio, escenas generadas de
  emoción (#24 llorando, #10 con fusiles); #1 (oct 2026): texto limpio + flecha dibujada a mano, como #32.

### Realidad
- Foto casi tal cual: ~8. Foto retocada (color, nitidez, cielo): ~25. Montaje o escena con aspecto de generada:
  ~44. Ilustración: 2.
- **Inventado o exagerado respecto a lo que pasa**: el Burj Khalifa a la altura de la ventanilla (#57); la isla con
  cientos de kayaks (#75); la muchedumbre de manos (#79); el Azteca con el trofeo del Mundial y una acampada de
  protesta (#4); la fila de presos del CECOT a la que Nil, según el título, **no entró** (#7); Nil llorando con
  lágrimas en un avión (#24); Nil con un AK-47 (#10); la placa «DON JULIO / MEJOR RESTAURANTE ARGENTINA» con sello
  (#29); el rótulo de telediario (#2); J Balvin cenando con ellos cuando el título dice que solo «Nos Trajo Hasta
  Aquí» (#17, no lo puedo comprobar). La exageración no se castiga ni se premia en el ratio: lo construido tiene
  residuo 0,96 y lo real 1,03 (en Millonarios gana lo construido, 1,02 frente a 0,85; en LATAM y Escapando, lo real).

## 4. Anatomía del título

Recuentos sobre la **cabeza** del título (lo que va antes de « | Serie»); residuos de los 70 episodios.

- **Estructura**: 62 de 79 llevan « | Nombre de la serie» detrás. La cabeza crece con el tiempo: Escapando 20
  caracteres / 3,5 palabras de media, Millonarios 30 / 5,3, LATAM 34 / 6,3. El sufijo se come la mitad del título y
  en el móvil se corta: lo que vende es la cabeza.
- **Sin sufijo** van los primeros episodios (#79, #58, #31: el título ES el nombre de la serie o su pregunta) y 5
  episodios camuflados de vídeo suelto (#4, #10, #29 en LATAM; #68 y #59 en Escapando). Residuo de los 8: 1,14; de los
  5 camuflados: #4 1,20, #10 1,09, #68 1,05, #59 1,00, #29 0,79 → mediana 1,05. Quitar el sufijo no hunde el episodio y
  parece ayudar algo (indicio débil, n=5).
- **Primera palabra**: «Visité» 6, «Así» 4, «La» 4 (La Lujosa Vida…, La Situación…, La Playa), «No» 3, «Pasé» 3, «24»
  2, «21» 2, «Ganó» 2; nombres propios en cabeza 6 (DUKI, Lola Lolita, Abraham Mateo, RUBIUS?, JBalvin, Fernando
  Alonso).
- **Persona**: 1.ª del singular (Visité, Pasé, Me Invita, Entendí, PERÚ ME TRAUMÓ, Estoy a Salvo…) 17 → residuo
  **1,09**; 1.ª del plural (Nos Amenazan, Nos Engañó, No Esperábamos, Lo Imaginábamos, Nos Trajo, Tenemos, Podemos)
  9 → **0,93**, y ahí están tres de los cinco peores del canal: #47 «Este Millonario Nos Engañó» (0,65), #20 «Nos
  Amenazan en Brasil» (0,69), #8 «No Esperábamos Un Accidente» (0,71). El «yo» invita a ponerse en su piel; el
  «nosotros» al que le pasa algo malo suena a crónica de grupo.
- **Cifras** en 12 cabezas: dinero (100.000€, 25.000€, 20.000.000$, -100.000€), tiempo (24 Horas ×4, 21 Días ×2),
  escala (sismo de 5.6, 7 Estrellas). Residuo 1,02 frente a 0,96: neutras. «24 Horas Con» funciona por lo que va
  detrás (un nombre), no por la cifra.
- **Mayúsculas** de palabra entera en 16 (sin contar LATAM): MÉXICO, LUJO, FALSO, FAMOSO, TRAUMÓ, «MEJOR»/«PEOR»,
  DENTRO DE LAS FAVELAS…, BRASIL:, RUBIUS?, JUGUETES PARA MILLONARIOS, MÓNACO:, DUKI, ABUELOS DE INCÓGNITO, ¿EL
  FINAL?. Residuo **0,88** frente a 1,01. Caen sobre el país o sobre el adjetivo de juicio; no levantan nada.
- **Signos**: «?» en 6 (0,90; la buena es #31 «¿Cuál Es el Mejor País de LATAM?», que es el episodio 1); «!» en 3
  (1,12: #12, #16, #27); «...» en 3 (sin efecto; #1 «No Sé Si Funciona...» 1,50 en suelto); comillas de ironía
  en #13 («"MEJOR" y el "PEOR"», 1,19); emoji de bandera en 7 (0,89); dos puntos de titular en 2 (BRASIL:, MÓNACO:).
- **Superlativos** (Más, Mejor, Peor, Único, Extrema): 12 → **0,88**. «El Lugar Más Catastrófico» (#5, 0,70),
  «El Único Hotel de 7 Estrellas» (#56, 0,86), «Supervivencia Extrema» (#72, 0,87): el superlativo está gastado.
- **Lo vago a propósito, y qué vago funciona**: el canal deja vago o **el porqué / el cómo** o **el quién**.
  - Porqué/cómo escondido: #7 «No Visité el CECOT **Por Esta Razón**» (1,41), #4 «La Situación en MÉXICO No Es Como
    Esperaba» (1,20), #28 «Nunca Había Visto Policías **Así**» (1,19), #62 «Lo Siento Mucho» (1,18), #30 «Entendí
    Por Qué Argentina Es Especial» (1,12), #61 «Tenemos Que Hablar...» (1,07), #3 «México No Es Como Lo
    Imaginábamos» (0,93) → mediana **1,18**.
  - Quién escondido (un desconocido): #23 «**Apareció** Cuando Más Lo Necesitaba» (0,57), #47 «**Este
    Millonario** Nos Engañó» (0,65), #20 «Nos Amenazan en Brasil» (0,69), #42 «Nadie Esperaba Un Robo» (1,04),
    #14 «**Se** Enfrentó a Nosotros» (1,05) → mediana **0,69**.
  - Regla que sale: **esconder la razón o la manera tira; esconder a una persona que nadie conoce, no.**
- **Desgracia contada en el título** (el daño ya está dicho: engañó, amenazan, accidente, traumó, partió el corazón,
  apareció cuando más lo necesitaba, sismo, catastrófico): 8–10 casos, mediana ~0,75. Es el grupo más flojo del canal
  (ver apartado 6).
- **Palabra-gatillo y posición**: casi siempre al final de la cabeza («…Por Esta Razón», «…Así», «…No Sé Si
  Funciona...», «…(mala idea)», «…Con Todo Pagado», «…Su Avión Privado») o es el nombre propio del principio
  («Coscu», «DUKI», «WestCOL»).
- **Moldes** (con ejemplos y residuo):
  1. «[Nombre del famoso]» a secas: DUKI (1,10), Lola Lolita (1,30), Abraham Mateo (0,80), RUBIUS? (0,87).
     Funciona según el famoso (ver apartado 1).
  2. «La Lujosa Vida de [famoso] en [país]»: #52 Coscu (1,65), #19 Ovy (1,17). 2 de 2 por encima en dos series.
  3. «(Pasé) 24 Horas Con [nombre]»: #18 WestCOL (1,57), #27 Pablo Chill-E! (1,12), #26 «Millonarios en Chile»
     (1,04). Mejor con nombre que con genérico.
  4. «Millonario Me Invita/Invitó a [lujo]»: #43 «Niño Millonario Me Invita a Su Avión Privado» (1,56), #57
     «Millonario Me Invitó a Dubai con Todo Pagado» (1,09).
  5. «Visité [lugar con calificativo]»: #9 «El Barrio de Bad Bunny» (1,20), #13 «el "MEJOR" y el "PEOR" Barrio en RD»
     (1,19), #16 «el País Más Rico de Latinoamérica!» (1,12), #10 «el País Donde las Armas Son Obligatorias» (1,09),
     #56 «el Único Hotel de 7 Estrellas del Mundo» (0,86), #5 «el Lugar Más Catastrófico de El Salvador» (0,70).
     Mediana 1,11; los dos de superlativo puro, abajo.
  6. «Así es [la vida / el lujo / vivir] en X»: #12 (1,83), #48 (0,86), #6 (0,80). Depende de la imagen (ver 7).
  7. «[Lugar] No Es Como [esperaba]» / «No [hice X] Por Esta Razón» / «Nunca Había Visto X Así»: #7, #4, #28, #3 →
     1,41 / 1,20 / 1,19 / 0,93. La negación con hueco es el molde más fuerte de LATAM.
  8. «[Alguien] Nos [daño]»: #47, #20, #8, #17 → 0,65 / 0,69 / 0,71 / 0,86. El más flojo.
  9. Escapando: frase corta de situación o de emoción, 1–3 palabras: «Estoy a Salvo» (1,15), «Lo Siento Mucho»
     (1,18), «Tenemos Que Hablar...» (1,07), «Aislados» (0,94), «La Playa» (0,87), «El Maletín o El Dinero» (0,78);
     «[X] Extrema»: Persecución Extrema (0,94), Supervivencia Extrema (0,87).
  10. «Ganó [cifra]€ Por [proeza]»: #68 (1,05), #59 (1,00): el concurso dentro de la serie, vendido como suelto.
- **Palabras que acompañan a los altos**: nombre de famoso latino/streamer (12 → 1,11), Millonario/Lujosa/Rico en
  LATAM (5 → 1,12), «Visité» (1,11), «No/Nunca» con hueco. **A los bajos**: «Nos», MAYÚSCULAS, superlativos,
  interrogación de veredicto («¿Sobrevalorado?», «Peligroso?»), emoji de bandera.
- **Tono**: envidia y asombro (Millonarios), amenaza y huida (Escapando, con giro a confesión en los últimos:
  «Lo Siento Mucho», «Tenemos Que Hablar...», «No Podemos Escapar», los tres por encima de su tendencia), juicio de
  viajero (LATAM: Mejor/Peor, Más Rico, FALSO, Sobrevalorado) y queja (Nos Amenazan, Accidente, TRAUMÓ).
- **Qué pregunta deja**: ¿cómo es por dentro? (lujo), ¿por qué? (negación con hueco), ¿le pillan? (Escapando),
  ¿quién? (desconocido), ¿cuál / vale la pena? (veredicto). Por residuo: por qué > cómo es > le pillan ≈ veredicto >
  quién.

## 5. El encaje: qué pasa en la cabeza de quien lo ve

### Reparto
- **Solo el título dice**: el nombre del invitado (Coscu, Duki, WestCOL: en la imagen no hay rótulo, hay que
  reconocerle), la razón escondida («Por Esta Razón»), el país cuando no hay bandera, el giro emocional («Lo Siento
  Mucho»), el número de la serie.
- **Solo la imagen dice**: el lujo concreto (jet, mansión, Rolls, Burj), el peligro concreto (la muchedumbre, el
  motorista, las botas encima), la emoción de Nil, el número de episodio y, en LATAM, el país (bandera).
- **Repiten los dos**: la palabra exacta en 7 (amenazados., Peligroso?, Favelas, dua lipa, sin dinero., -100.000€,
  No Entré.).
- **Callan los dos**: qué pasa al final (si le pillan, si le dejan entrar, si funciona el Porsche), qué hay dentro
  (CECOT, Apple Park, el coche tapado), por qué (CECOT, «Lo Siento Mucho»).

### Tipos de encaje (nombres míos), recuento y residuo
| Tipo | Qué es | Casos | Residuo mediano |
|---|---|---|---|
| **Escaparate + nombre** | la imagen enseña el lujo o al famoso; el título solo nombra | #52, #41, #49, #38, #18, #19, #27, #9, #48, #6, #55, #50, #45, #26, #30… (~22) | ~1,05 (depende del famoso) |
| **Escena + giro** | la imagen enseña una situación y el título le da un sentido que no tenía | #78, #12, #62, #28, #10, #61 (6) | **~1,16** |
| **Escena + desinflado** | el título explica la imagen hacia abajo (ya pasó algo malo, es falso, era un desplante) | #54, #23, #17, #15, #47, #33 (6, sin #33: 5) | **~0,78** |
| **Eco** | texto de la imagen = palabra del título | #20, #22, #21, #63, #36, #67, #7 (7) | ~0,92 |
| **Paráfrasis** | texto de la imagen dice lo mismo con otra palabra | #43, #39, #3, #60, #29, #1, #32 (7) | ~1,15 |
| **Diálogo** | la imagen pone una frase en boca de alguien y el título la sitúa | #58, #46, #54, #14, #12, #11, #62 (7) | ~1,05 |
| **Amenaza ilustrada** | la imagen dibuja el peligro y el título lo nombra seco | #79, #77, #76, #73, #69, #72, #64, #60, #22 (9) | ~0,95 |
| **Testimonio** | cara de Nil contando algo, sin la cosa | #20, #8, #5, #2, #24 (5) | **~0,70** |

### La segunda lectura
12 casos en que la imagen sola parece una cosa y con el título pasa a ser otra: #78 (pánico + «Estoy a Salvo»), #12
(le invitan a pasar + «Déjame Entrar»), #62 (concurso de pi + «Lo Siento Mucho»), #28 (charla + «Nunca Había Visto
Policías Así»), #10 (susto con fusiles + «País Donde las Armas Son Obligatorias»), #61 (charla + «Tenemos Que
Hablar...»), #54 (foto con Alonso + «Me Partió el Corazón»), #23 (siesta + «Apareció Cuando Más Lo Necesitaba»), #17
(cena con Balvin + «Nos Trajo Hasta Aquí»), #15 (paraíso + «FALSO Maldivas»), #47 (Lamborghini + «Nos Engañó»), #33
(fiesta con tarjeta + «(mala idea)»). Mediana en series 1,07, pero partida: cuando el giro **añade** un misterio
(los 6 primeros) ~1,16; cuando el giro **resta** (desplante, falso, ya pasó, mala idea) ~0,78.

### 10 parejas diseccionadas

1. **#52 · 4,26 (res 1,65)** · «La Lujosa Vida de Coscu en Argentina | 21 Días Entre Millonarios». Se ve: dos caras
   enormes con camiseta de baloncesto, pasmadas, mirando arriba a la izquierda; detrás, mansión de cristal con pista
   azul y canasta. Primer segundo: ve dos caras de asombro y una casa irreal. Siguiente: lee «Lujosa Vida de Coscu».
   Pregunta: ¿qué están mirando que les deja así, si ya tiene esa casa? Por qué no puede contestar sin entrar: la cosa
   que miran está fuera del cuadro; la casa es solo el principio.
2. **#43 · 3,97 (1,56)** · «Niño Millonario Me Invita a Su Avión Privado». Se ve: dos chavales en un jet, uno hace un
   selfi, el otro brinda; bandeja de canapés y una botella de Moët gigante; «Jet Privado.». Primer segundo: jet, comida,
   champán, gente joven feliz. Siguiente: «Niño Millonario». Pregunta: ¿un niño con jet propio? ¿quién es y de dónde
   sale el dinero? No puede contestar: el título no da el nombre ni la edad y la imagen solo enseña el festín.
3. **#58 · 3,78 (1,45)** · «21 Días Entre Millonarios». Se ve: Nil enseña una tarjeta roja con una sonrisa de oreja a
   oreja; a su lado un amigo serio con la ceja alzada; detrás, fila de deportivos; «"compra un coche"». Primer
   segundo: tarjeta + coches. Siguiente: la orden entre comillas. Pregunta: ¿de verdad le dejan comprar un coche?
   ¿cuál elige? ¿quién paga? La cara del amigo (no se ríe) siembra la duda de que haya truco.
4. **#41 · 3,30 (1,30)** · «Lola Lolita». Se ve: ella sola sonriendo ante una tienda Louis Vuitton con un bolso LV
   adelantado. Primer segundo: famosa + lujo. Siguiente: su nombre. Pregunta: ¿cuánto se gasta? ¿qué hace con Nil?
   Débil como hueco: funciona por la invitada (comentarios por visita 5,2 por mil, de los más altos: tirón de fans).
5. **#39 · 2,99 (1,18)** · «Billonario Por Un Día». Se ve: Nil con gafas de sol, sonrisa total, presentando con la
   mano una avioneta dorada; «1 Billón.». Primer segundo: avión de oro. Siguiente: «Billonario Por Un Día». Pregunta:
   ¿qué hace un billonario en un día y qué le deja hacer a Nil? El «Por Un Día» promete vivirlo en primera persona.
6. **#57 · 2,84 (1,09)** · «Millonario Me Invitó a Dubai con Todo Pagado». Se ve: Nil en un asiento de primera, un
   guante blanco le sirve un plato y él mira por la ventanilla el Burj Khalifa entre nubes; «Primera Clase». Primer
   segundo: ventanilla imposible + servicio. Siguiente: «Todo Pagado». Pregunta: ¿quién paga y qué quiere a cambio?
7. **#23 · 0,55 (0,57, el peor de LATAM)** · «Apareció Cuando Más Lo Necesitaba». Se ve: Nil tumbado en el césped
   mirando a alguien de quien solo vemos pantalón blanco y zapatillas. Primer segundo: un chico tirado en la hierba.
   Siguiente: «Apareció». Pregunta posible: ¿quién? Por qué no tira: el que aparece es un desconocido cortado por las
   rodillas; no hay nadie a quien imaginar, el «cuando más lo necesitaba» ya cuenta que se arregló, y la foto es un
   fotograma sin retocar ni número.
8. **#47 · 1,66 (0,65, el peor de Millonarios)** · «Este Millonario Nos Engañó». Se ve: Nil en un Lamborghini leyendo
   en el móvil «No voy a grabar con ustedes», remitente pixelado, sonrisa de labios apretados. Primer segundo:
   Lamborghini + chat. Siguiente: «Nos Engañó». Pregunta: ¿quién? Pero el quién es un desconocido; el desenlace (no
   graba) ya está dicho dos veces, en la burbuja y en el título. En una serie de lujo, es el episodio en que **no** hay
   lujo.
9. **#12 · 1,49 (1,83, el mejor residuo del canal)** · «Así es la Vida de Un Millonario en República Dominicana! 🇩🇴».
   Se ve: un anfitrión sonriente en la puerta de una mansión con lámpara de araña y bandera dominicana, haciendo el
   gesto de «pasa»; a su lado Nil, fuera, cara de súplica, y «Déjame Entrar». Primer segundo: mansión + choque de caras
   (uno feliz, otro preocupado). Siguiente: «Déjame Entrar» (contradice el gesto de invitar) y «Vida de Un
   Millonario». Pregunta: ¿le deja o no? ¿qué hay dentro? Es el molde ganador de Millonarios trasplantado a LATAM, con
   una contradicción interna.
10. **#28 · 1,24 (1,19)** · «Nunca Había Visto Policías Así». Se ve: dos chicos sentados en un bordillo de Santiago,
    uno con los brazos abiertos («¿has visto eso?»), Nil con la mano en la cara, bandera chilena. Ni un policía.
    Primer segundo: charla. Siguiente: «Policías Así». Pregunta: ¿así cómo? No puede contestar porque el objeto del
    título está fuera de la imagen entera: la imagen es la reacción, el título nombra la causa y calla el «cómo».

## 6. Mecanismos psicológicos

Mecanismo dominante de cada vídeo (uno; el segundo entre paréntesis). Residuo en series; ratio bruto en sueltos.

- **Lujo vicario / envidia («vivirlo a través de él»)** — 17: #52 (famoso), #43 (incongruencia: un niño con jet),
  #58 (ganancia: barra libre), #39 (récord: 1 billón), #57 (acceso gratis), #51 (incongruencia: niños), #37
  (ganancia), #56 (récord), #46 (regalo), #48, #55, #50, #26, #19 (famoso), #16, #12 (acceso: «Déjame Entrar»), #6.
  **Mediana 1,04** (Millonarios 1,02; LATAM 1,12). Dentro de Millonarios no separa (todos son lujo); en LATAM es lo
  que mejor funciona después del hueco.
- **Famoso** — 10: #41, #49, #54 (humor: el «No»), #38, #63, #27, #18, #17, #11 (conflicto), #9 (lugar del famoso).
  **Mediana 1,01**, muy desigual: streamers y raperos latinos arriba (Coscu, WestCOL, Lola, Duki, Ovy, Pablo Chill-E),
  famosos españoles «de tele» y desplantes abajo (Abraham Mateo 0,80, Alonso 0,78, Rubius 0,87, Balvin que no está
  0,86).
- **Hueco de información (el porqué o el cómo)** — 12: #7, #4, #28, #30, #31, #62, #61, #3, #29 (veredicto), #15
  (veredicto: FALSO), #71 (dilema), #53 (incongruencia). **Mediana 1,10** (LATAM 1,15). Dentro, las de veredicto o
  dilema van abajo (#29 0,79, #15 0,87, #71 0,78): **preguntar «¿vale la pena?» no es un hueco, es un examen**.
- **Amenaza o daño inminente** — 11: #42, #79, #78, #77, #76, #73, #69, #64, #60, #22, #10. **Mediana 0,99**.
- **Rareza / récord / extremo** — 10: #45, #75, #74, #72, #70, #68, #65, #59, #13 (contraste), #25 (novedad).
  **Mediana 0,97**.
- **Desgracia contada (el daño ya ocurrió y se dice)** — 8: #47, #67, #24, #23, #20, #8, #2, #5. **Mediana 0,70**
  (LATAM 0,70 con 6 casos). Es el único grupo claramente por debajo, y lo forman los peores del canal.
- **Conflicto** — 2: #14 (1,05), #21 (peligro del lugar, 0,88).
- Sueltos (ratio bruto): acceso a lo vedado #35 Apple Park (2,01); comunidad/confesión #44 «guanyar se va.» (1,77),
  #40 «Hola Lola» (1,38); sueño cumplido + duda #1 Porsche (1,50); regalo + sorpresa #32 (1,33); reto de privación
  #36 (1,09); recopilación #33 (0,53), #34 (0,40); videoclip #66 (0,47).

**Qué se intenta y no funciona aquí**:
1. La **amenaza ilustrada** es la plantilla entera de Escapando (persecución, escondite, tirón, rodeado) y la serie
   queda en 0,86 de mediana; dentro de ella, los residuos van de 0,78 a 1,32, el rango más estrecho de las tres
   series. La miniatura de peligro, por muy construida que esté, no distingue un episodio de otro cuando todos la
   llevan.
2. **El signo de interrogación como objeto** (#71, maletín con «?» gigante): el peor de Escapando (0,78).
3. **La rareza visual** (bola transparente, exoesqueleto, isla de kayaks, enterrado en la arena): 0,97. Llama la
   vista pero no promete nada que interese saber.
4. **El misterio de persona** (pixelado, cortado por las rodillas): 0,57–0,65.
5. **El testimonio de la desgracia** (cara contando lo que pasó): 0,70.
6. **El superlativo** («Más Catastrófico», «Único Hotel de 7 Estrellas», «Extrema»): 0,88.

## 7. Las que más y las que menos rinden, al detalle

### Por ratio bruto (lo que pide el encargo)
- **10 de mayor ratio**: #52 4,26 · #43 3,97 · #58 3,78 · #41 3,30 · #39 2,99 · #57 2,84 · #49 2,83 · #51 2,66 · #42 2,65 ·
  #37 2,54. **Las 10 son de 21 Días Entre Millonarios.**
- **10 de menor**: #34 0,40 · #66 0,47 · #5 0,51 · #33 0,53 · #8 0,54 · #23 0,55 · #6 0,59 · #20 0,64 · #3 0,66 · #2 y #59
  0,69. Tres son formatos que no son episodio (dos películas-recopilación de 178 min y un videoclip); siete son de los
  últimos días de LATAM (episodios 24–30, salvo #20, ep. 12) y uno el final de Escapando.
- Lo que les separa es **la serie y el formato**, no la miniatura. Aun así, diferencias visibles: arriba, 10 de 10
  enseñan un lujo concreto o un famoso; 7 de 10 tienen una escena construida e impoluta; 6 de 10 llevan sonrisa.
  Abajo, 5 son fotogramas casi brutos (#5, #8, #23, #6, #2), 4 cuentan una desgracia ya ocurrida (#5, #8, #20, #2) o
  un después (#23), ninguna lleva una sonrisa franca.

### Por residuo dentro de su serie (lo que de verdad mide el empaquetado)
- **Arriba**: #12 1,83 · #52 1,65 · #18 1,57 · #43 1,56 · #58 1,45 · #7 1,41 · #31 1,38 · #79 1,32 · #41 1,30 · #9 y #4 1,20.
- **Abajo**: #23 0,57 · #47 0,65 · #20 0,69 · #5 0,70 · #8 0,71 · #54 0,78 · #71 0,78 · #29 0,79 · #6 0,80 · #38 0,80.
- **Qué les separa**:
  - Persona con Nil: 8 de 11 de arriba tienen a otra persona con peso (anfitrión, Coscu, WestCOL, el niño, Misho,
    YSY A, Lola sola, la muchedumbre); abajo, 5 de 10 son Nil solo o con una persona sin papel.
  - **Sonrisa**: 6 de 11 arriba; 0 de 10 abajo (labios apretados #47, ceja escéptica #29 y #71, cara de cansancio
    #23, hablando #5 y #20, nervios #54, sospecha #38).
  - **Desgracia o desplante dicho**: 0 arriba; 6 abajo (#23, #47, #20, #5, #8, #54).
  - **Episodio 1**: 3 arriba (#58, #31, #79): el primer episodio se lleva un extra que la tendencia no recoge.
  - Texto: 5 de 11 arriba y 5 de 10 abajo. No separa. Escena construida: 8 de 11 arriba y 4 de 10 abajo; separa algo,
    pero dentro de LATAM los fotogramas reales con famoso (#18, #9) están arriba.
  - Título: arriba dominan nombre de famoso o «Lujosa Vida / Millonario» (6) y negación con hueco (#7, #4); abajo,
    «Nos…» y desgracia (#47, #20, #8, #23), veredicto («¿Sobrevalorado?», «El Maletín o El Dinero») y nombre de famoso
    con desplante (#54, #38).
- **Otras explicaciones posibles**: en LATAM el país pesa: los tres de Brasil están por debajo de su tendencia (#20
  0,69, #21 0,88, #22 0,93) y los de El Salvador también salvo el CECOT (#5 0,70, #6 0,80; #7 1,41); Puerto Rico va
  mezclado (#8 0,71, #9 1,20, #10 1,09) y República Dominicana arriba (#12 1,83, #13 1,19; #11 0,87). El residuo no
  puede separar país de miniatura. En Millonarios, el invitado.

### Parejas casi iguales con resultado distinto
1. **#37 vs #33 — misma foto (volteada), 2,54 frente a 0,53.** Final de Millonarios frente a la película-recopilación
   de 178 min de la misma serie, con «(mala idea)». La miniatura no puede vender dos veces lo mismo; y el espejo
   delata el reciclaje (la tarjeta pone «ASIV»).
2. **#12 vs #6 — «Así es [lujo] en [país latino]»**: 1,83 frente a 0,80. #12: escena construida, un anfitrión con
   gesto de «pasa», Nil fuera suplicando, cita «Déjame Entrar», exclamación. #6: fotograma real de un plato de
   vieiras, nadie mira a cámara, sin texto, «LUJO» en mayúsculas. Lo que cambia: **una persona que da acceso y una
   puerta por cruzar** frente a un plato.
3. **#4 vs #3 — «México No Es Como…», días consecutivos**: 1,20 frente a 0,93. #4 enseña «la situación» (acampada de
   protesta delante del Azteca con el trofeo del Mundial: contraste) y habla en «yo» («Esperaba»), sin sufijo. #3
   enseña a dos chicos mirando fuera de cuadro con «Extraño.» y habla en «nosotros» («Imaginábamos»). Lo que cambia:
   **la imagen enseña la contradicción en vez de una reacción**, y el «yo».
4. **#18 vs #27 vs #26 — «24 Horas Con…»**: WestCOL 1,57, Pablo Chill-E 1,12, «Millonarios en Chile» 1,04. Mismo molde;
   el famoso con más tirón joven gana, y el genérico es el más flojo. Miniaturas: pulso de manos entre risas (#18),
   abuela con trofeos (#27), conduciendo un Porsche (#26).
5. **#52 vs #19 — «La Lujosa Vida de [famoso] en [país]»**: 1,65 y 1,17, dos series distintas, los dos por encima. En
   #52 miran algo fuera de cuadro con asombro; en #19 sonríen al selfi en una lancha. El molde aguanta; el asombro
   suma.
6. **#43 vs #57 — «Millonario Me Invita/Invitó»**: 1,56 frente a 1,09. #43 añade la incongruencia («Niño») y una escena
   compartida y abundante (dos personas, comida, champán, selfi); #57 es Nil solo, sorprendido, y un brazo de camarero.
   Texto con punto («Jet Privado.») frente a sin punto («Primera Clase»).
7. **#62 vs #68 vs #59 — la misma imagen de pi** (cifras que se desvanecen + concursante + Nil): «Lo Siento Mucho»
   1,18, «Ganó 100.000€ Por Responder Una Pregunta» 1,05, «Ganó 25.000€ Por Memorizar 350 Números» 1,00. **El título
   que no explica la imagen (y añade una disculpa) gana a los que la explican con cifra.**
8. **#49 vs #38 vs #54 — famoso a solas con Nil en Millonarios**: Duki 1,10 (complicidad, risa), Abraham Mateo 0,80
   (miradas de sospecha), Alonso 0,78 (le dice «No»). La cara del famoso cuenta: **la complicidad vende, el desplante
   no**.
9. **#1 vs #32 — coche + «(Su) Nuevo coche» + flecha a mano**: 1,50 y 1,33 (sueltos). Plantilla idéntica; los dos por
   encima. El Porsche añade la duda en el título («No Sé Si Funciona...») y el polvo del garaje.
10. **#76 vs #72 — «[X] Extrema» + cifra en bloque**: «120km/h» 0,94, «12 Horas.» 0,87. Iguales y planos.
11. **#22 vs #21 vs #20 — Brasil**: «Peligroso?» 0,93, «📍Favelas» 0,88, «amenazados.» 0,69. La que enseña el lugar
    (favela de noche, favela de día) aguanta; la que enseña a Nil contándolo, se hunde.

## 8. Trucos de oficio y recetas

### Lista de trucos (veces · ejemplo)
- Marcador de episodio fijo abajo a la izquierda (silueta roja del continente con el número, o moneda dorada con el
  número) para que la serie se lea como temporada · 43 · #12, #78.
- El primer episodio sin marcador y con el nombre de la serie como título · 3 · #79, #58, #31.
- Episodio camuflado de vídeo suelto: sin sufijo de serie, título de concurso o de país · 5 · #68, #59, #4, #10, #29.
- Objeto de dinero en primer plano, más cerca de cámara que la cara, sostenido hacia el espectador (tarjeta, moneda,
  llave, billete) · 16 · #58, #51.
- Todo el dinero en dorado (moneda, tarjeta, avión, medallón, estrellas) · ~20 · #39, #79.
- Objeto de marca de lujo con el logo legible y entero (Moët, LV, Rolex, Rolls-Royce) · ~12 · #43, #41.
- Objeto agrandado respecto a la persona (botella, gaviota, maletín, trofeo) · 8 · #43, #70.
- Vista imposible pegada en una ventana o detrás (Burj entre nubes, Pagani en la puerta de un banco) · ~6 · #57, #16.
- Mirada de los dos fuera de cuadro hacia lo mismo, sin enseñarlo · 2 · #52, #3 (funciona solo con algo que imaginar:
  1,65 frente a 0,93).
- Cita entre comillas tipográficas con una rayita fina hacia quien la dice · 7 · #58, #12.
- Diálogo de dos bocadillos, la respuesta en amarillo («una foto?» / «No») · 1 · #54.
- Palabra o cifra en bloque blanco con borde negro y **punto final**, arriba a la derecha · 9 · #43 «Jet Privado.»,
  #39 «1 Billón.».
- Texto blanco limpio sin borde, en minúsculas y con punto («atrapado.», «amenazados.») · 6 · #60.
- Amarillo solo para la palabra que pica (precio, negativa, insulto) · 4 · #46 «$50.000».
- Flecha dibujada a mano, blanca y curva, del texto al objeto · 2 · #1, #32.
- Captura de interfaz como prueba (chat, llamada, notificación, rótulo de telediario) · 4 · #47, #11, #67, #2.
- Pixelar al remitente de un mensaje · 1 · #47 (0,65: no lo repetiría).
- Imagen partida con la persona en el eje y la ropa partida igual (mitad camiseta, mitad traje) · 1 · #13.
- Bandera del país en un mástil o colgada al fondo, o camiseta de la selección · ~19 · #30, #22.
- Cartel o letrero del lugar dentro de la escena en vez de texto añadido («Bienvenido a Perú», «EL SALVADOR», «DON
  JULIO») · 4 · #25, #7.
- Grupo en selfi con la cara de Nil delante y los demás alrededor con caras de pasmo · 4 · #37, #53.
- Amenaza a la espalda: alguien acercándose o encima (botas, motorista, manos en el cristal, muchedumbre) · 8 · #78,
  #76.
- Escondido con solo la cara asomando (arbusto, suelo, esquina, arena) · 4 · #73, #78, #22, #70.
- Disfraz completo (látex de anciano) · 2 · #65, #66.
- Referencia visual conocida reinterpretada (paso de cebra de Abbey Road, prismáticos de dibujos) · 2 · #74, #34.
- Reciclar la miniatura de otro vídeo volteada en espejo · 1 · #33 (0,53).
- Ilustración de dibujos para las películas-recopilación · 2 · #36, #34.
- Escena emocional generada (lágrimas, fusiles, Mundial con protesta) · ~4 · #24, #10, #4.
- Ningún contorno ni halo en los recortes; fusión limpia · 79 · —.

### Recetas (los 5 tipos del canal)

**A. Escaparate de lujo con invitado** (Millonarios; la que más rinde en bruto). Encuadre 16:9 a la altura de los
ojos, gran angular moderado. Una o dos caras en el tercio izquierdo-centro, cabezas de 35–45 % del alto, cortadas por
los hombros o el pecho. Expresión: asombro (cejas arriba, boca entreabierta) o sonrisa de dientes; mirada a cámara o,
mejor, los dos mirando lo mismo fuera de cuadro. Detrás, el lujo entero y nítido ocupando la mitad derecha: mansión de
cristal, jet, superdeportivos, tienda con el logo legible; cielo azul limpio. Objeto en primer plano opcional (tarjeta,
bolso, botella) hacia cámara. Ropa lisa saturada que rime con el fondo (camiseta de baloncesto delante de una pista).
Texto: nada, o 1–2 palabras en bloque blanco con borde negro y punto arriba a la derecha que digan el lujo con otra
palabra que el título («Jet Privado.»). Saturación alta, sin viñeta, sin contorno. Título: «La Lujosa Vida de
[famoso] en [país]» o «[Alguien] Me Invita a [lujo]».

**B. La puerta (acceso con choque de caras)** (#12, #58). Dos personas de cuerpo medio: quien da acceso (anfitrión,
amigo con la tarjeta) feliz y abierto, y Nil con una cara que no casa (súplica, duda, sonrisa excesiva). Entre ellos o
detrás, la puerta o el objeto que hay que cruzar o usar (entrada de mansión, tarjeta, concesionario). Cita entre
comillas con rayita hacia quien la dice: la orden o la petición («"compra un coche"», «Déjame Entrar»). Marcador de
episodio abajo a la izquierda si es serie. Título: «Así es la Vida de Un Millonario en [país]!» o el nombre de la serie.

**C. Amenaza a la espalda** (Escapando). Nil en primer plano a un lado, cabeza ~30 %, ojos muy abiertos y dientes
apretados, enseñando la moneda dorada a cámara; detrás, la amenaza en movimiento (motorista, muchedumbre, alguien
encima, mano que arranca la cadena) con desenfoque de velocidad si procede. Escenario temático limpio (desierto,
granero, carretera). Cifra o palabra seca en bloque arriba a la derecha («120km/h», «12 Horas.», «atrapado.»). Moneda
con el nº de episodio abajo a la izquierda. Título de 1–3 palabras. **Aviso**: es la receta más vistosa y la que menos
diferencia un episodio de otro (residuos 0,78–1,32).

**D. El sitio que no se ve / el porqué** (LATAM, la mejor de esa serie). Nil serio o preocupado mirando a cámara,
cuerpo medio, delante de la puerta del lugar (cárcel, estadio, barrio), con un elemento que diga el lugar sin texto
(cartel «EL SALVADOR», bandera, camiseta) y, al otro lado, la prueba del contraste (fila de presos, acampada delante
del Mundial). Texto limpio de 2 palabras con punto arriba a la izquierda que niegue o resuma («No Entré.»). Título con
negación y hueco: «No Visité [X] Por Esta Razón», «La Situación en [país] No Es Como Esperaba», «Nunca Había Visto [X]
Así».

**E. Reacción sin la causa** (#28, #62, #61). Fotograma real de una conversación: dos o tres personas, una gesticula
(brazos abiertos, «¿has visto eso?»), Nil escucha con la mano en la cara; ningún texto o una cifra-textura. La causa
(los policías, lo que se disculpa, lo que hay que hablar) no sale. Funciona **solo** si el título nombra una causa
concreta y esconde el cómo o el porqué («Nunca Había Visto Policías Así», «Lo Siento Mucho»); con desgracia contada
o con un desconocido («Nos Amenazan», «Apareció…») es lo peor del canal.

### Las 6 mejores, una a una
1. **#52 · 4,26** · «La Lujosa Vida de Coscu en Argentina | 21 Días Entre Millonarios». Dos cabezas a la izquierda que
   ocupan casi todo el alto (la de la izquierda cortada por el borde, con gorra del revés y cinta de Jordan; la de la
   derecha con collar de perlas y camiseta de los Celtics); los dos con las cejas alzadas y la boca entreabierta,
   mirando arriba a la izquierda, fuera del cuadro; la mano derecha de uno a medio gesto, abierta. Detrás, mansión de
   hormigón y cristal de dos plantas con listones de madera, césped perfecto y una pista de baloncesto azul con canasta
   de cristal que corta el cielo a la derecha. Cielo azul con una nube. Sin texto, sin marcador. Saturación alta, caras
   muy enfocadas y suavizadas; la casa tiene aspecto de rehecha.
2. **#43 · 3,97** · «Niño Millonario Me Invita a Su Avión Privado | 21 Días Entre Millonarios». Interior cálido de jet
   (cuero beige, luz de techo). Un chaval con camiseta negra sostiene un iPhone en alto (se ve la parte trasera,
   cámaras incluidas) haciendo un selfi; a su lado Nil con camiseta roja brinda con una copa de champán, los dos
   sonriendo a cámara. En primer plano, una bandeja de cristal con sándwiches, tostas y tartaletas que cruza la imagen,
   y a la derecha una botella de Moët & Chandon enorme, más alta que ellos sentados. «Jet Privado.» blanco con borde
   negro y punto arriba a la derecha.
3. **#58 · 3,78** · «21 Días Entre Millonarios». Dos medios cuerpos: a la izquierda un chico con barba y camisa
   vaquera, serio, ceja algo alzada, mirando a cámara; a la derecha Nil con camiseta negra, ojos muy abiertos y sonrisa
   de todos los dientes. Entre los dos sostienen hacia cámara una tarjeta Mastercard roja (número inventado). Detrás,
   un concesionario blanco con focos en el techo y una fila de deportivos de colores (rojo, morado, blanco, verde, azul
   Porsche, rojo Ferrari). Arriba al centro-derecha, «"compra un coche"» en blanco con borde negro y comillas
   tipográficas, con una rayita diagonal hacia el de la barba.
4. **#41 · 3,30** · «Lola Lolita | 21 Días Entre Millonarios». Lola Lolita sola a la derecha, de cintura para arriba,
   vestido marrón de un hombro, sonrisa cerrada con dientes, mirada a cámara, sosteniendo hacia cámara un bolso Louis
   Vuitton beige con el monograma y un móvil en la otra mano. A la izquierda, la fachada de piedra clara de una tienda
   Louis Vuitton con el logo LV gigante y el rótulo; palmeras, cielo azul, calle vacía. Sin texto. Recorte pegado con
   luz algo distinta a la del fondo.
5. **#39 · 2,99** · «Billonario Por Un Día | 21 Días Entre Millonarios». Selfi de Nil a la izquierda con gafas de sol
   negras y sonrisa abierta, mochila; con la otra mano abierta presenta una avioneta monomotor a reacción pintada
   entera de dorado, con la puerta y la escalera abiertas, sobre la pista con líneas amarillas. Cielo azul con nubes.
   «1 Billón.» en bloque blanco con borde negro y punto arriba a la derecha.
6. **#57 · 2,84** · «Millonario Me Invitó a Dubai con Todo Pagado | 21 Días Entre Millonarios». Nil sentado en un
   asiento de cuero crema de primera clase, camiseta marrón, cuerpo hacia cámara y cabeza girada hacia la derecha,
   ojos abiertos y boca entreabierta (asombro contenido); a la izquierda, un camarero de chaqué del que solo se ve el
   brazo con guante blanco sirviendo un sándwich en plato de borde dorado; en la mesa, tartar, panecillo, salsas y
   agua. A la derecha, la ventanilla con el Burj Khalifa y los rascacielos de Dubái saliendo de un mar de nubes.
   «Primera Clase» en bloque blanco con borde negro (sin punto) arriba, a la izquierda de la ventanilla.

## 9. Contraste con la guía

Leídos al terminar 1–8: `base/titulos-miniaturas.md` (§ 1, 3, 4, 6, 7), el análisis anterior
`base/refs/_youtube/canales/nilojeda.md` y la parte A de `_analisis/segunda_es_vlog.md`.

### Lo que este canal confirma
- **§ 1.6 «El tema pesa más que el diseño»**: el peor episodio de Millonarios (1,66) supera al mejor de las otras dos
  series (1,50 y 1,52). Es la confirmación más fuerte de toda la guía.
- **§ 1.5 «Las recopilaciones son lo peor»**: #34 (0,40) y #33 (0,53), las dos últimas del canal salvo el videoclip.
- **§ 6.5 «Texto: la mayoría no lleva y ponerlo no sube»**: 32 de 79 con texto añadido; residuo 0,94 con texto y 1,01
  sin él.
- **§ 6.5 / § 7 «El texto nunca repite el título»**: eco literal ~0,92 (n=7: «amenazados.» con «Nos Amenazan» 0,69,
  «Peligroso?» con «Tan Peligroso?» 0,93, «dua lipa» con «Dua Lipa» 0,91…) frente a paráfrasis ~1,15.
- **§ 6.7 «Flechas y círculos no suman»**: #75 (flecha + círculo + «YO», 0,94), #5 (flecha roja, 0,70), #63 (flecha
  amarilla, 0,91).
- **§ 6.6 «La etiqueta de precio como único gancho no levanta»**: #46 «$50.000» (0,88), #67 «-100.000€» (0,92).
- **§ 6.4 «La cara seria neutra rinde menos que la que reacciona»**: boca cerrada 0,92 frente a sonrisa 1,12 y
  entreabierta 1,02.
- **§ 6 tono en español «ni un grito en 79 de Nil Ojeda»**: cierto, ni uno.
- **§ 4 «Verbo en 1.ª persona en pasado, sin sujeto»**: «Visité…» 1,11 (n=6); 1.ª del singular 1,09 (n=17).
- **§ 4 molde «[PLAN] con [FAMOSO]»**: «Pasé 24 Horas Con WestCOL» 1,57; «La Lujosa Vida de Coscu…» 1,65.
- **§ 4 molde «[SITIO] No Es Como [Me Contaron]»**: #4 «La Situación en MÉXICO No Es Como Esperaba» 1,20.
- **§ 1.2 «Entre los dos dejan fuera el desenlace»**: las 6 mejores en bruto congelan un antes o un durante; ninguna
  enseña el final.

### Lo que contradice o matiza
- **§ 1.7 «Tensión, no final feliz… lo caro, 3 de 3 por debajo (Rubén)… el benefactor sonriente es lo más bajo de
  MrBeast»** → aquí **al revés**: la serie del lujo es la que más rinde y dentro de cada serie la sonrisa va mejor
  (1,12) que la boca cerrada (0,92). La clave que la guía no recoge: el lujo **no es del creador, se lo dan** (le
  invitan, le prestan la tarjeta, «con Todo Pagado»). El benefactor que funciona es el que da a Nil, no el que da a
  otros. Y la tensión pura (Escapando entera) es la serie que peor rinde.
- **§ 1.3 «Se calla el final, nunca el sujeto»** → matiz: ocultar **a una persona** hunde (#23 0,57, #47 0,65), pero
  dejar fuera de la imagen **la cosa que el título nombra con su sustantivo** funciona: #28 «Nunca Había Visto Policías
  Así» sin ningún policía (1,19); #52, los dos mirando algo fuera del cuadro (1,65); #7, el interior del CECOT (1,41).
  La regla útil es: se puede sacar el sujeto de la imagen si el título lo nombra concreto y la imagen enseña la
  reacción; nunca se puede dejar sin nombre ni sin cara a una persona.
- **§ 3 «No: títulos que no dicen nada sin la miniatura ("Lo Siento Mucho")»** → el propio ejemplo de la guía está mal
  leído. #62 «Lo Siento Mucho» tiene 0,88 en bruto, pero es el episodio 18 de una serie que pierde un 2,7 % por
  episodio: su residuo es **1,18**, el segundo mejor de Escapando, y con la **misma imagen** (cifras de pi + concursante)
  gana a «Ganó 100.000€ Por Responder Una Pregunta» (1,05) y a «Ganó 25.000€ Por Memorizar 350 Números» (1,00). En
  una serie que el público ya sigue, la frase de confesión sin objeto funciona.
- **§ 6.10 «El fotograma sin preparar queda al fondo (6 de 6 en Nil Ojeda)»** → la prueba está inflada: de esos 6,
  #40 y #44 no son episodios de Millonarios (son vídeos de comunidad sin sufijo) y #66 es un videoclip. Dentro de LATAM,
  los fotogramas reales tienen residuo mediano 1,015 y las escenas construidas 1,01: **lo mismo**. #18 (real, 1,57),
  #9 (real, 1,20) y #28 (real, 1,19) están arriba. Lo que se hunde es el fotograma **sin famoso y sin hueco**: #23,
  #8, #5, #6, #20.
- **§ 1.8 / § 6.10 «Los escenarios fabricados quedan por debajo»** → en el ratio no se ve: construido 0,96, real 1,03
  (en Millonarios gana lo construido, 1,02 frente a 0,85). #7 enseña la fila de presos que, según su propio texto, no
  vio («No Entré.») y es la 3.ª de LATAM ajustada (1,41). La regla de no inventar sigue en pie por honradez y por
  desgaste del creador, pero no tiene aquí apoyo en el ratio.
- **§ 4 «Superlativo con artículo… el molde más usado»** → aquí el superlativo va abajo: 0,88 (n=12); «Visité el
  Lugar Más Catastrófico de El Salvador» 0,70, «Visité el Único Hotel de 7 Estrellas del Mundo» 0,86 (por debajo de
  la tendencia de Millonarios).
- **§ 4 molde «Así es Vivir en [SITIO] de [DATO IMPOSIBLE]» (5 de 5 en HiClavero)** → «Así es Vivir en un Piso de
  20.000.000$ en Miami» 0,86 (con su cifra imposible); el que funciona es «Así es la Vida de Un Millonario en
  República Dominicana!» (1,83), sin cifra y con una persona que da acceso en la imagen.
- **§ 4 «Sin "¡!" (0 de 279)», «"Billonario" suena traducido», «mayúscula también a Un/Es/Lo es calco»** → Nil usa «!»
  en 4 (#12 1,83, #16 1,12, #27 1,12, #32 1,33), «Billonario» (#39, 1,18) y «Así es la Vida de Un Millonario». Son
  normas de corrección, no de rendimiento: a su público no le restan.
- **§ 3 «El número de episodio no va en la miniatura (0 de 15 en byCalitos)»** → Nil lo pone en 43 de 51 episodios de
  dos series (silueta roja con número, moneda con número). No hay forma de medir su efecto aquí (casi todos lo llevan;
  los 5 de LATAM sin número van peor, 0,71, pero son además los menos trabajados). La regla de la guía sale de un canal
  que no lo usa: no tiene prueba ni a favor ni en contra.
- **§ 6.8 «El objeto-prueba en la mano hacia cámara es la plantilla más segura»** → con dinero en la mano, 0,98 frente a
  0,99; en Escapando, la moneda en 10 episodios, 0,95. Cuando el objeto es el **atrezo fijo de la serie**, deja de ser
  prueba de nada.

### Lo que la guía NO dice y aquí se ve
1. **En series diarias, juzga cada miniatura contra la caída por episodio, no contra la mediana.** Escapando pierde
   ~2,7 % por episodio, LATAM ~1,5 %; Millonarios, nada. Sin ajustar, los episodios tardíos parecen fracasos (#7 1,06 →
   residuo 1,41; #4 0,86 → 1,20; #62 0,88 → 1,18) y los primeros parecen aciertos de miniatura. Dos análisis anteriores
   y la propia guía han sacado reglas de esa lectura. *Regla: compara un episodio con sus vecinos o con la tendencia
   de su serie.*
2. **Lo vago funciona si es el porqué o el cómo; falla si es el quién.** Porqué/cómo escondido («Por Esta Razón», «No
   Es Como Esperaba», «Policías Así», «Lo Siento Mucho»): mediana 1,18 (n=7). Quién escondido («Apareció…», «Este
   Millonario Nos Engañó», «Nos Amenazan», «Se Enfrentó a Nosotros»): 0,69 (n=5). *Regla: calla la razón, nunca a la
   persona; si la persona no es conocida, nómbrala por lo que es («Niño Millonario»).*
3. **La desgracia contada en pasado es lo peor del canal.** Título con el daño ya ocurrido + imagen de la consecuencia
   o de Nil contándolo: mediana 0,70 (n=8: #23, #47, #20, #8, #5, #2, #24, #67). Instante «después»: 0,78 frente a 1,02
   de «durante». *Regla: un contratiempo se vende en el instante en que pasa o con su porqué escondido («No Visité el
   CECOT Por Esta Razón»), nunca como parte de daños («Nos Amenazan en Brasil»).*
4. **«Yo» mejor que «nosotros» cuando a quien le pasa algo es el creador.** 1.ª del singular 1,09 (n=17), 1.ª del plural
   0,93 (n=9), con tres de los cinco peores del canal en plural. *Regla: «Me…» / «Visité…», no «Nos…» / «No
   Esperábamos…».*
5. **El texto de la miniatura, mejor como sinónimo más corto o más fuerte que como palabra nueva o eco.** Paráfrasis
   («Avión Privado» → «Jet Privado.», «Billonario» → «1 Billón.», «No Podemos Escapar» → «atrapado.») ~1,15 frente a eco
   ~0,92 y complemento ~0,94. La guía dice «no repitas»; aquí se ve **qué** poner en su lugar.
6. **El punto final en el texto de miniatura** convierte la etiqueta en veredicto («Jet Privado.», «Secuestro.», «No
   Entré.»): 1,04 frente a 0,93 sin punto (n=9 y 7; indicio). La guía solo habla del punto en los títulos.
7. **El mecanismo «invitado al lujo ajeno».** Le invitan, le dan la tarjeta, se lo pagan: #43 «Me Invita» (1,56), #58
   «"compra un coche"» (1,45), #57 «Todo Pagado» (1,09), #12 «Déjame Entrar» (1,83). El espectador va de invitado sin
   envidiar al creador. *Regla: si el vídeo tiene lujo, que sea de otro y que se lo den al creador, y dilo en el
   título («Me Invita», «Todo Pagado»).*
8. **La cara del invitado decide.** Famoso con complicidad: Duki 1,10, WestCOL 1,57, Coscu 1,65. Famoso con desplante o
   sospecha: Alonso «No» 0,78, Abraham Mateo de reojo 0,80, Balvin serio 0,86. *Regla: con famoso, la miniatura enseña
   la relación buena; el desplante va dentro.*
9. **El creador con alguien rinde más que solo.** Nil solo 0,90 (n=32), con una persona 1,06 (n=24), con grupo 1,03.
10. **Choque de caras dentro de la imagen.** Quien da acceso, feliz; el creador, con una cara que no casa (súplica, duda);
    y una cita entre comillas que contradice el gesto (#12 «Déjame Entrar» mientras le invitan a pasar, 1,83; #58 amigo
    serio + Nil eufórico, 1,45). La guía habla de «la expresión reacciona a la escena», no de **dos expresiones
    opuestas** como motor.
11. **La cita con rayita** (comillas tipográficas + raya fina hacia quien habla) es el formato de texto que mejor sale
    (mediana 1,05; las dos mejores de su serie son citas). No está en la guía.
12. **Una plantilla fija para todos los episodios aplana el efecto de la miniatura.** Escapando lleva amenaza + moneda
    en todos: rango de residuos 0,78–1,32, el más estrecho. *Regla: en una serie, cambia de mecanismo de un episodio a
    otro (amenaza, famoso, confesión, rareza) para que la miniatura pueda distinguir.*
13. **Episodio camuflado de vídeo suelto.** 5 episodios sin sufijo y con título de vídeo independiente (#4, #10, #68,
    #59, #29): mediana 1,05, sin hundirse. *Regla: el episodio con un gancho propio puede titularse como vídeo
    independiente para llegar a quien no sigue la serie.*
14. **El episodio 1 se titula con la premisa (o su pregunta) y se lleva un extra** que ninguna miniatura iguala:
    #79 (1,32), #58 (1,45), #31 (1,38) de residuo, los tres sin marcador de episodio y con objeto en la mano (moneda,
    tarjeta, dardo).
15. **El veredicto en pregunta no es un hueco**: «¿Sobrevalorado?» + «Vale la pena?» (0,79), «FALSO Maldivas» (0,87),
    «El Maletín o El Dinero» con «?» pintado (0,78). Mayúsculas de palabra entera (0,88) y emoji de bandera (0,89),
    tampoco.
16. **En series de viaje, el país pesa** (Brasil y El Salvador, todos por debajo de su tendencia salvo el CECOT;
    República Dominicana, arriba): antes de culpar a la miniatura, mira el país.

### Qué se les escapó a los análisis anteriores, en qué se equivocaron y qué sigue en pie
- **Se les escapó**: la caída por episodio como medida (los dos la nombran, ninguno la descuenta); el reparto
  quién/porqué de lo vago; «yo» frente a «nosotros»; el instante «después»; eco frente a paráfrasis con números; que la
  sonrisa gana a la boca cerrada dentro de cada serie; que #68 y #59 son episodios de Escapando con título de suelto
  (el anterior lo intuye por la insignia pero no lo saca como recurso).
- **Se equivocaron** (por leer ratios brutos en series que caen o por mezclar series):
  - el análisis anterior: «fotograma sin preparar, seis de seis al fondo» (incluye #40 y #44, que no son episodios de
    Millonarios, y #66, un videoclip); «cifras de pi que no se leen» como mala práctica (las tres de pi están en
    1,00–1,18 de residuo); «demasiados elementos: #4» (#4 es 1,20 ajustado, 3.ª–6.ª de LATAM);
  - la segunda mirada: «los títulos que callan el sujeto o la causa rinden por debajo», con «Lo Siento Mucho»,
    «Tenemos Que Hablar...» y «No Visité el CECOT Por Esta Razón» como ejemplos (ajustados: 1,18, 1,07 y 1,41: callar
    la causa funciona; lo que falla es callar a la persona); «superlativo contable y verificable» (#56) como lo que
    separa (#56 está por debajo de la tendencia de Millonarios, 0,86); el «asombro con la boca cerrada» como rasgo del
    top (#51 1,03, #56 0,86, #53 0,88: en la media o por debajo de su serie);
  - la guía: el ejemplo «Lo Siento Mucho» como título que no funciona, y el «6 de 6» del fotograma.
- **Sigue en pie**: la serie lo explica casi todo; el lujo de otro que se le da al creador (la segunda mirada lo vio
  bien: 8 de 9 del top); el texto que no repite la palabra del título; la cita con raya; que esconder a un desconocido
  no abre curiosidad (#23); que las emociones positivas van mejor en LATAM (el anterior: 5 alegres ≥ 1,05); que reciclar
  la miniatura para la película no sirve (#33); que la cara del famoso y la relación cuentan (#18 frente a #17).

## 10. Límites

- Vistas las 20 hojas de detalle (4 por hoja), las 5 hojas cronológicas, la de extremos y 15 miniaturas a tamaño
  completo (#52, #43, #58, #41, #39, #57, #23, #8, #5, #47, #28, #12, #33, #24, #10). Las otras 64, a ~960 px en las
  hojas de detalle: bien para expresión, texto y composición; menos seguro para retoques finos (halos, piel).
- «Construida», «con aspecto de generada» y «real retocada» son juicios por el aspecto; no puedo saber con qué se hizo
  cada imagen. Tampoco sé si alguna miniatura se cambió después de publicar (los cinco episodios de LATAM sin número
  podrían ser cambios posteriores).
- El residuo sale de un ajuste lineal de log(ratio) contra el orden de publicación dentro de cada serie: simple, sin
  separar país, invitado ni día de la semana. En Escapando falta el episodio 4 y dos salieron el mismo día; en
  Millonarios no hay marcador y el orden es el de fecha. Los «casos» de cada rasgo son pocos (5–20): son indicios.
- La codificación (sonrisa, instante, mecanismo, tipo de encaje) es mía; otra persona movería algunos casos de grupo.
- No identifico a los invitados por la cara: los nombres salen de títulos, descripciones y tags. Quién es quién en
  #52 y #43 (Nil o el invitado) no lo afirmo.
- No he podido comprobar si lo que enseñan las miniaturas inventadas (#7, #17, #24, #10, #4) sale o no en el vídeo.
- No he hecho ninguna petición a internet.
