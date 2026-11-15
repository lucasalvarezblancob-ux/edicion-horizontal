# ChandlersWildLife — detalle fino de títulos y miniaturas

Fuentes: `titulos.tsv`, `videos.json`, `descripciones.txt`, las 14 hojas de `detalle/`, las 4 de `hojas/` y 14 miniaturas a
tamaño completo (#25, #40, #22, #11, #7, #36 = 6 de mayor ratio; #48, #43, #44 = 3 de menor; #35, #18, #31, #16, #4 =
dudosas). Hechos los recuentos con un script propio sobre `videos.json` más mi codificación a mano de cada miniatura.

Nota de método: el ratio depende mucho de la fecha (ver 1). Además del ratio bruto doy a veces el **ratio ajustado**
(«adj») = ratio del vídeo / mediana del ratio de sus 10 vecinos en el tiempo (5 antes, 5 después). adj 1,0 = lo normal
EN SU MOMENTO del canal.

## 1. Ficha

- **Idioma**: inglés (EE. UU., Florida). Títulos y miniaturas en inglés.
- **De qué va**: Chandler, cuidador de reptiles con su propio parque/zoo («Chandler's Wild World», Florida): cocodrilos
  y caimanes, cobras reales y serpientes venenosas (taipanes, mambas, víboras), y una pequeña «troupe» de mascotas
  carismáticas (nutria Kaido, búho real). Episodios tipo diario: dar de comer, mover animales, obras del recinto,
  sustos, alguna visita a otro zoo o santuario.
- **Vídeos y periodo**: 54 vídeos, del 2025-11-04 al 2026-11-10 (371 días).
- **Cadencia**: 1 cada ~7 días de media, irregular: racha de 4 vídeos en 10 días en julio (#19, #18, #17, #16) y huecos
  de 2–3 semanas (sep.–oct., 10 oct.→1 nov.).
- **Duración**: mediana 22 min (de 11 a 42). Los antiguos (nov.–dic. 2025) son más cortos (11–20 min).
- **Quién sale**: Chandler solo, casi siempre. Invitados: Tyler Nolan (#41, #46), «Santa» (otro señor, en #44), el
  equipo de WildFlorida (#31, no sale en la miniatura). 52/54 miniaturas llevan la cara de Chandler; las otras dos son
  #16 (de espaldas) y #44 (Papá Noel, que no es él).
- **Suscriptores**: 2,94 M. **Mediana de visitas** (vídeos >21 días): 173.367.

**Qué explica el ratio aparte del empaquetado (comprobado antes de nada):**
1. **Antigüedad (lo más fuerte)**. Rho de Spearman días↔ratio = **−0,49**: cuanto más reciente, más ratio. Por tercios
   cronológicos (vídeos >21 días): nov. 25–ene. 26 mediana **0,70**; feb.–jun. **1,03**; jun.–oct. **1,38**. Los
   vídeos de los dos primeros meses tienen casi todos ratio rojo (#43 0,47, #44 0,48, #48 0,43, #51 0,58…) porque el
   canal era más pequeño, no necesariamente por su miniatura. Por eso uso «adj».
2. **Duración y capítulos**: no explican nada una vez ajustada la fecha (rho duración↔adj = 0,09; capítulos↔adj =
   −0,05).
3. **Tema**: el más claro es «animales comiendo» (ver 3 y 7). Las **visitas a felinos** (fuera de lo habitual del canal)
   dan 2 de 3 altísimos: #47 «Feeding BIG CATS!» 2,16 (adj 3,46) y #40 «Modern day Saber-Toothed Tiger?!» 3,17 (adj
   4,59); la tercera, #44 «Santa FEEDS BIG CATS!» 0,48, salió el 24 de diciembre.
4. **Fechas señaladas**: los 2 vídeos temáticos de fiesta rinden poco: #49 Thanksgiving 0,75 y #44 Navidad 0,48.
5. **Segundas partes**: la continuación rinde menos que la primera: #28 «I Can't Believe this Happened!» 0,99 →
   #27 «SURGERY on ALLIGATOR'S BROKEN JAW!» 0,76; inundación #2 2,06* → #1 1,03*.
6. **Invitado**: Tyler Nolan no suma (#41 0,74, #46 0,68; adj 1,12 y 1,09 → normales para su época).
7. **Saturación**: la racha de julio (4 vídeos en 10 días) deja 3 por debajo de 1 (#17 0,64, #18 0,66, #19 0,96; adj
   0,57–0,83).
8. **Indicio de público ajeno**: los éxitos tienen la **mitad de «me gusta» por visita**: #11 12 likes/1000 visitas, #7
   13, #22 19, #25 20, #14 20, #40 25, #36 26, frente a 45–69 en los flojos (#48 69, #43 60, #39 58, #37 58). O sea, los
   que se disparan llegan a gente que no es seguidora (portada/sugeridos), que es justo donde manda el empaquetado.
9. **Un falso experimento natural**: #3 «DISASTER Strikes! *UNCENSORED*» (4 nov., 23 min) y #2 «My Wildlife Park
   Flooded…» (5 nov., 19 min) cubren la misma inundación con casi la misma descripción y casi la misma plantilla de
   miniatura; #2 tiene 4 veces las visitas de #3 con un día menos. Pero en `videos.json` #3 figura como
   `availability: needs_auth` (restringido por edad: es la versión «sin censura»), y eso basta para hundir su alcance.
   **No vale como prueba de empaquetado** (lo vi al contrastar con el análisis anterior; ver 9).

## 2. Tabla de TODOS los vídeos

Orden: de mayor a menor ratio (como `detalle/`); los de `*` al final. «IA» = escena fotorrealista generada o rehecha con
IA; «collage» = recortes pegados sobre fondo; «foto» = fotograma real. «Grito» = boca abierta en O, ojos muy abiertos,
cejas arriba. Flecha = flecha roja salvo que diga otra cosa.

| n | ratio | ojo: 1.º → 2.º → 3.º | cara | manos y cuerpo | sujeto y qué se le ha hecho | texto literal + cómo es | recursos gráficos | instante | gatillo del título | pregunta abierta |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 3.43 | texto amarillo/blanco → cara gritando → cocodrilo y cobra a punto de morder | grito, ~1/6 del alto, sombrero vaquero, mira a cámara | brazos en alto en «Y», sostiene carne cruda (izq.) y pitón (der.) como cebos | IA: cocodrilo saltando del agua, cobra con la boca abierta, búho con alas abiertas, nutria con un pez, uno por esquina; todo en HDR | «FEEDING ALL OF MY ZOO ANIMALS!» (6 palabras), blanco con «ALL» y «ZOO» en amarillo, borde negro, ~25 % del alto, arriba | flecha curva hacia la pitón | ANTES: los dos depredadores a un palmo del cebo | CRAZIEST | ¿qué pasa cuando suelta los cebos? ¿cómo da de comer a todo eso? |
| 40 | 3.17 | colmillos gigantes de la derecha → gato con colmillos en brazos → cara riendo | risa con dientes, ojos hacia el animal (no a cámara), sin sombrero, chaqueta de cuero | sostiene en brazos al felino como a un gato doméstico | IA: un felino moteado con colmillos de dientes de sable (no existe) y su cabeza ampliada rugiendo a la derecha, ~60 % del alto | «PRIVATE ZOO!» (2), blanco, borde negro, ~13 % del alto, arriba al centro | flecha recta a los colmillos | DURANTE (lo sostiene) | Saber-Toothed Tiger?! | ¿existe de verdad? ¿quién tiene esto en casa? |
| 22 | 3.12 | cabeza de cobra enorme tragando pitón → cuerpo amarillo de la pitón → Chandler pequeño | sonrisa tranquila, ~1/7 del alto, sin sombrero, mira a cámara | agachado, relajado, junto a los animales | IA: cobra con la cabeza más grande que el torso de Chandler engullendo una pitón real; 2 cobras más alzadas a la izq. y 1 a la der.; luz dramática oscura | sin texto | ninguno | DURANTE (la está tragando) | Giant Hungry KING COBRAS | ¿cómo de grande es? ¿se la come entera? |
| 11 | 2.94 | cara gritando al centro → cobra (izq.) con la pitón en la boca → cocodrilo (der.) mordiendo la otra pitón | grito, ~1/6, sombrero, mira a cámara | guantes negros, una pitón albina en cada mano, por encima de los hombros | IA: composición simétrica, cobra gigante a la izq., cocodrilo a la der., las pitones amarillas unen a los tres; fondo selva claro | sin texto | flecha curva hacia la boca de la cobra | DURANTE (los dos muerden a la vez) | EAT Pythons | ¿quién se la come antes? ¿está loco? |
| 7 | 2.35 | fauces del cocodrilo → pitón tensada → cara gritando | grito, ~1/4, sombrero, mira a cámara | tira de la pitón con las dos manos, cuerpo echado atrás (tira y afloja) | IA: cocodrilo enorme mordiendo el otro extremo de la pitón, salpicaduras, barro; brazos de culturista | sin texto | ninguno | DURANTE (tira y afloja) | EAT Big Python | ¿quién gana? ¿le muerde a él? |
| 36 | 2.32 | «ANIMALS!» rojo-naranja → cara sonriente → fauces de cocodrilo/búho | sonrisa con ojos entornados, selfie, sin sombrero, cara real | sujeta un trozo de carne a cámara; está en el agua | collage: 2 cobras casi iguales (duplicadas), nutria enseñando dientes, cocodrilo, hocico de gavial, búho; recortes sin contorno | «FEEDING ALL OF MY ANIMALS!» (5): «FEEDING» amarillo, «ALL OF MY» blanco, «ANIMALS!» degradado rojo-naranja enorme, borde negro grueso, ~35 % del alto | ninguno | ANTES (carne en la mano) | Venomous Snakes & Crocodiles | ¿cómo da de comer a todos sin que le muerdan? |
| 14 | 2.21 | cara embarrada gritando → dedo señalando el charco → criaturas del barro | grito, ~1/4, sombrero, cara llena de barro | señala con el guante el estanque | IA: estanque medio vacío con caimán, siluro, tortuga mordedora con la boca abierta y nutria; tubo de desagüe | sin texto | dedo como flecha | DURANTE (vaciando) | Mystery Pond?? | ¿qué más vive ahí abajo? |
| 47 | 2.16 | cara gritando al centro → tigre rugiendo (izq.) → león (der.) | grito, ~1/3, sombrero, mira a cámara | solo el busto | collage: tigre, león, pantera negra y jaguar rodeándole, recortes grandes | sin texto | flecha roja a mano alzada, fina, hacia el león | estático | BIG CATS | ¿qué come un león? ¿cómo se acerca a ellos? |
| 9 | 2.13 | «BIG NEWS!» amarillo → cara gritando → cocodrilo bajando del remolque | grito, ~1/3, sombrero | señala con el índice al cocodrilo | IA: 3 cocodrilos saliendo de un remolque por la rampa | «BIG NEWS!» (2), amarillo con borde negro, ~20 % del alto, arriba a la izq. | dedo como flecha | DURANTE (llegando) | RESCUING 3 | ¿de dónde vienen? ¿por qué los rescata? |
| 35 | 1.84 | cara triste → ojos amarillos brillando en la sombra → «???» | tristeza: cejas en ángulo, boca hacia abajo, cerrada; sin sombrero; cara real | brazos caídos, camiseta de su merch «Be chill like Ziggy» | IA: de noche, apagado; cocodrilo tumbado (muerto/herido) y un animal negro de lobo o felino, solo silueta y ojos encendidos | «MYSTERY ANIMAL» blanco en caja roja + «BROKE IN!» blanco + «???» blanco/amarillo/blanco + «WHAT HAPPENED» amarillo (8 en total) | interrogaciones, caja roja | DESPUÉS (ya ha pasado) | WORST Nightmare | ¿qué animal entró? ¿murió el cocodrilo? |
| 6 | 1.61 | cara gritando → dedo → recinto acabado con cocodrilos | grito, ~1/5, sombrero | lleva los planos bajo el brazo y señala | IA: el recinto soñado YA TERMINADO (pasarelas, agua azul, excavadora, atardecer) | «MY DREAM EXHIBIT!» (3), amarillo, borde negro, arriba a la der. | dedo | futuro imaginado | DREAM | ¿cómo va a quedar? ¿cuánto cuesta? |
| 10 | 1.56 | boca abierta de la cobra → cara gritando detrás → manos abiertas | grito, ~1/6, sombrero | agachado, manos abiertas a los lados (sorpresa) | IA: cobra alzada de frente con la boca abierta hacia el espectador, recinto frondoso | sin texto | flecha curva a la cabeza de la cobra | ANTES (cobra amenazando) | MASSIVE Makeover | ¿cómo es el nuevo recinto? ¿le ataca? |
| 20 | 1.47 | colmillos en la mejilla → cara gritando → «CLOSE CALL!» | grito de dolor, ~1/4, sombrero | brazo extendido (selfie) | IA: taipán mordiendo / a punto de morder la cara, tierra saltando | «EXTREMELY» blanco + «CLOSE CALL!» amarillo + «COASTAL TAIPAN» blanco en brochazo rojo + placa «WORLD'S MOST VENOMOUS SNAKE!» con calavera (10) | flecha al punto de la mordida, triángulo de peligro con calavera | DURANTE (la mordida) | Close CALL / MOST Venomous | ¿le mordió de verdad? ¿sobrevivió? |
| 34 | 1.44 | fauces del komodo → cara gritando → tigre al fondo | grito, ~1/4, sombrero | busto | IA: 2 dragones de Komodo (uno con la boca de par en par) y un tigre entre humo; fuego al fondo | «NEW MYSTERY ANIMAL?!» (3), amarillo/blanco; «??» blanco | flecha al komodo, «??» | ANTES | THIS Animal… | ¿cuál de ellos es el nuevo? |
| 8 | 1.39 | cobra con corona dorada → mirada fija de Chandler → mano | ceño fruncido, boca cerrada, mirada intensa a cámara; sombrero | a gatas, mano abierta a la der. como para cogerla | IA: cobra real coronada (juego de palabras «king»; la corona es la de su logo) | sin texto | flecha a la cobra, corona | ANTES | needs HELP | ¿qué le pasa a la cobra? |
| 16 | 1.36 | cocodrilo saltando con la boca abierta → ciervo en el aire → Chandler de espaldas | sin cara (de espaldas) | lanza un cervato entero con un brazo | FOTO real sin retocar (luz plana, móvil) | sin texto | ninguno | ANTES (el ciervo en el aire) | WHOLE DEER | ¿se lo traga entero? |
| 32 | 1.34 | fauces con el ciervo → cara riendo → tira y afloja | risa amplia, ~1/6, sombrero | agachado tirando de la pata del ciervo | IA: cocodrilo con el ciervo en la boca, salpicaduras | sin texto | ninguno | DURANTE | WHOLE DEER | ¿quién gana? |
| 15 | 1.27 | ojo de reptil en la caja → «DANGER» → cobra y tigre | grito, ~1/6, sombrero | sostiene la caja de madera con guantes | IA: caja con un agujero por el que asoma un ojo amarillo; cobra (izq.) y tigre (der.) rugiendo; cartel «CHANDLER'S WILD WORLD ZOO» | solo texto dentro de la escena: «DANGER» estampado, el cartel | flecha al ojo | ANTES (sin abrir) | NEW ANIMAL | ¿qué hay en la caja? |
| 26 | 1.2 | capucha de la cobra con lengua azul → cara → tigre entre la maleza | sorpresa suave, boca entreabierta; sin sombrero; cara real | sujeta otra serpiente rayada al cuello | IA: cobra enorme con lengua azul eléctrico; tigre de adorno (el título no habla de él) | sin texto | ninguno | ANTES | WILD KING COBRAS | ¿dónde las busca? |
| 53 | 1.18 | «NOT HAPPY!» → flecha → boa | sonrisa, gorra, sin sombrero | sostiene una boa que le lanza la cabeza; otra mano sostiene una cobra | collage de época antigua: recortes sobre verde desenfocado | «NOT HAPPY!» (2), blanco, borde negro | flecha a mano alzada roja fina | ANTES (la boa a punto de morder) | NOT Friendly | ¿le muerde? |
| 38 | 1.14 | cara escarchada gritando → cocodrilos helados → búho y nutria | grito, ~1/3, sombrero cubierto de nieve | busto | IA: todo azul, nieve; cocodrilos, nutria, búho y serpiente con escarcha | sin texto | ninguno | DURANTE (helada) | FREEZING COLD | ¿se mueren de frío? |
| 5 | 1.1 | cara gritando → víbora del Gabón con colmillos → cobra amarilla | grito, ~1/6, sombrero | da un ratón con pinzas | IA: 6 serpientes de colores alrededor (víbora del Gabón, cobra del Cabo, víbora azul, verde, mamba, etc.) | sin texto | ninguno | ANTES | CLOSE CALL | ¿cuál casi le muerde? (la imagen no lo muestra) |
| 23 | 1.03 | cara de susto → cocodrilo tapado con sábana azul → nido con huevos | susto y pena: ojos muy abiertos, boca abierta, mano en el sombrero | mano en la cabeza (gesto de «no puede ser») | IA: cocodrilo inerte sobre una mesa medio tapado; al fondo, madre sobre un nido | «HEARTBREAKING NEWS...» (2), blanco sobre brochazo rojo | flecha al cocodrilo | DESPUÉS | Heartbreaking | ¿ha muerto? ¿y los huevos? |
| 24 | 1.03 | texto en 4 renglones → cocodrilo albino → fauces de la der. | grito, ~1/7, sombrero | abraza al cocodrilo albino | IA: cocodrilo blanco, gavial, otro cocodrilo con la boca abierta, cuidador con cubo al fondo | «VISITING THE RAREST CROCODILES IN THE WORLD!» (7) blanco/amarillo/blanco/amarillo, efecto de cartel de madera + «GHARIAL» pequeño | flecha, flechita a «GHARIAL» | estático | RAREST | ¿cuáles son? |
| 29 | 1.01 | fauces del cocodrilo → cara sonriente gritando → obra al fondo | grito alegre, ~1/5, sombrero; selfie | señala al cocodrilo | IA: cocodrilo en la orilla, pasarela en obras, excavadora, gente | «My BIGGEST Project Yet!» (4), blanco con «BIGGEST» amarillo, abajo a la izq., inclinado | dedo | futuro / obra | Finally Happening | ¿qué proyecto? |
| 28 | 0.99 | cara de susto → mandíbula rota sangrando → «EMERGENCY!» | susto, ~1/3, sombrero | busto | IA: cabeza de cocodrilo con la mandíbula inferior partida y sangre | «EMERGENCY!» (1), blanco en caja roja, arriba a la der. | flecha curva a la herida | DESPUÉS (la herida ya está) | Can't Believe | ¿qué le pasó? ¿se salva? |
| 30 | 0.99 | cara gritando muy cerca → boca de cobra → carne | grito, ~1/3, sombrero | pinzas con carne a cámara | IA: cocodrilo (izq.), cobra enorme (der.), nutria con pez; todo apretado y solapado | «FEEDING EVERYTHING!» blanco + «DON'T TRY THIS!» naranja degradado (5) | flecha a la cobra | ANTES | FEEDING ALL MY ZOO ANIMALS (todo en mayúsculas) | ninguna fuerte |
| 19 | 0.96 | boca negra de la mamba → cara → texto | grito alegre, ~1/5, sombrero; logo de corona en la camiseta | sostiene la mamba con un gancho | IA: mamba negra con la boca abierta (interior negro) | «WORLD'S MOST DANGEROUS SNAKE!» (4), blanco con «DANGEROUS» amarillo, abajo a la izq. | flecha a la boca | ANTES | MOST DANGEROUS | ¿por qué es la más peligrosa? |
| 13 | 0.94 | cara gritando → víbora azul comiendo → víboras de colores | grito/sonrisa, ~1/5, sombrero | da carne con pinzas, guante negro | IA: cobra con dibujo de anteojos, nutria al hombro, víbora azul, 2 víboras de arbusto amarilla y naranja | sin texto | ninguno | DURANTE (la víbora muerde la carne) | VENOMOUS SNAKES | débil: es otro día de comida |
| 12 | 0.9 | boca abierta de la cobra → «NOT HAPPY!» → Chandler mirándola | medio sonriente, boca entreabierta, mira a la cobra; sin sombrero; camiseta de su merch | sujeta el cuerpo de la cobra | IA/retocada: cobra enorme a la der. | «NOT HAPPY!» (2), blanco, borde negro | flecha a la cobra | ANTES | NOT Happy | ¿le ataca? |
| 50 | 0.78 | serpientes por todas partes → Chandler pequeño | sonrisa, gafas de sol en la cabeza, sin sombrero | agachado, serpiente al hombro | collage antiguo sobre fondo verde liso: cascabel, mamba negra, taipán, cobra, víbora amarilla | sin texto | flecha a mano alzada fina | estático | MOST VENOMOUS | ninguna fuerte |
| 21 | 0.77 | «RAIDING A CROCODILE NEST!» → mano con huevos → madre atacando | grito, ~1/6, sombrero | mano embarrada cogiendo huevos | IA: nido lleno de huevos, cocodrilo madre saliendo del agua con la boca abierta | «RAIDING A CROCODILE NEST!» blanco/amarillo + «COLLECTING THE EGGS!» en brochazo rojo (7) | flecha a los huevos | ANTES (la madre llega) | Finally laid EGGS | ¿le pilla la madre? |
| 37 | 0.77 | fauces atravesando la valla → cara gritando → mano | grito, ~1/5, sombrero | mano abierta, retrocede | IA: cocodrilo rompiendo una valla metálica, restos volando | sin texto | ninguno | DURANTE (rompiendo) | NOT SUPPOSED TO HAPPEN (todo mayúsculas) | ¿se escapó? (la imagen ya lo cuenta) |
| 27 | 0.76 | cara de cirujano asustado → mandíbula partida → texto | susto, ~1/4, sombrero, mascarilla bajada | bisturí en la mano, guante azul, fonendo | IA: caimán en mesa de quirófano con la mandíbula partida en dos | «EMERGENCY» blanco en caja roja + «JAW SURGERY!» blanco de brocha (3) | flecha | DURANTE | SURGERY / BROKEN JAW | ¿sale bien? (segunda parte) |
| 33 | 0.75 | cara gritando → lector «Microchip Detected» → fauces | grito, ~1/3, sombrero | jeringa en una mano, lector en la otra | IA: cocodrilo con la boca abierta; pantalla con número inventado | «MICROCHIPPING A CROCODILE!» (3), amarillo, borde negro | ninguno | ANTES | RAREST | el título habla de otra cosa que la imagen |
| 49 | 0.75 | pavo crudo → fauces → cara | mueca/grito con un ojo guiñado, sin sombrero | sostiene el pavo en alto | collage: cocodrilo, cobra, nutria sobre verde desenfocado | «CROCODILE THANKSGIVING!» (2), blanco, borde negro; «!!» amarillos | signos «!!» | ANTES | THANKSGIVING | ninguna |
| 41 | 0.74 | mapache en la cabeza → invitado sonriente → cobra albina | ojos cerrados, risa/mueca, mano en alto; sin sombrero | un mapache sobre su cabeza, sujetado por otro | collage: Tyler Nolan, cobra albina enorme, víbora, gallina de Guinea | «TYLER NOLAN'S!» (2), amarillo, borde negro | flecha al mapache | estático | Crazy ANIMALS / @TylerNolan | ¿qué tiene Tyler Nolan? |
| 54 | 0.72 | cara gritando muy grande → 6 serpientes alrededor | grito, ~1/2, sombrero | busto | collage antiguo: víbora azul, culebra verde, cascabel albina, cobra, taipán… sobre verde | sin texto | flecha, «!!» amarillos | estático | VENOMOUS | ninguna |
| 52 | 0.71 | cara gritando → cobra saliendo de una caja roja → «NEW SNAKE!» | grito, ~1/2, sombrero | busto | collage: caimán (izq.), cobra saliendo de una caja de regalo con calavera | «NEW SNAKE!» (2), blanco, borde negro | calavera, «?» amarillo pixelado | DURANTE (sale de la caja) | NEW VENOMOUS SNAKE | ¿cuál es? (pero ya se ve) |
| 46 | 0.68 | mamba en el gancho → Chandler → invitado | concentración, sin gesto; sin sombrero | sujeta el gancho en alto | FOTO real + 2 mambas recortadas añadidas a los lados | sin texto | flecha a mano alzada | DURANTE (manejo) | BLACK MAMBA / NEW HOME | ninguna |
| 18 | 0.66 | cara gritando → cobra tragando pitón → flecha | grito, ~1/4, sombrero | apoyado tras el tronco | IA: UNA cobra tragando pitón, a escala grande pero creíble | sin texto | flecha de brocha a la cabeza | DURANTE | EATS Huge Python | ninguna nueva (ya visto en #22) |
| 17 | 0.64 | boca negra de la mamba → cobra y taipán → cara | grito, ~1/4, sombrero | sostiene la mamba con gancho | IA/collage: cobra, mamba negra, taipán con la boca abierta | sin texto | ninguno | estático | MOST Dangerous Snakes | ¿cuál es la peor? (lista) |
| 42 | 0.64 | «NEW VENOMOUS SNAKE!» → cara → serpiente enroscada | grito, ~1/3, sombrero | busto | collage: serpiente rayada naranja enroscada, cobra al fondo con la boca abierta | «NEW VENOMOUS SNAKE!» (3), amarillo, borde negro, franja superior | flecha grande, triángulo con calavera, «?» rojo, «!!» amarillos | estático | NEW Venomous | ¿qué especie? |
| 45 | 0.61 | fauces con la carne → «BULL GATOR!» → Chandler pequeño al fondo | sonrisa, ~1/8, sin sombrero | agachado, da carne con la mano, cubo azul | IA: caimán enorme en primer plano, atardecer dorado, salpicaduras | «FEEDING MY BULL GATOR!» (4), blanco + amarillo-naranja de brocha | flecha a la carne | DURANTE | trust again | ninguna (título suave) |
| 51 | 0.58 | cara gritando → cobra albina con ojos rojos brillantes → otras cobras | grito, ~1/2, sombrero | busto | collage: 5 cobras; a la albina le han puesto ojos rojos de LED | sin texto | flecha a mano alzada, «!!» amarillos, ojos brillantes | estático | FULL COBRA TOUR | ninguna |
| 31 | 0.55 | 3 bocas abiertas iguales → cara gritando → brazos abiertos | grito, ~1/6, sombrero | brazos abiertos de par en par | IA: el MISMO cocodrilo clonado 3 veces, de frente y simétrico; cascada y fuego de fondo | sin texto | ninguno | estático | RARE CROCODILES | ninguna (visita a otro parque) |
| 39 | 0.52 | cara gritando → tarántula con etiqueta «FOR SALE!» → tití e iguana | grito, ~1/3, sombrero | busto | IA/collage: tití, iguana, tarántula; estanterías de tienda de fondo | «FOR SALE!» en etiqueta amarilla de precio (2) | flecha, etiqueta de precio | estático | won't BELIEVE | ¿qué venden? (lo enseña) |
| 44 | 0.48 | Papá Noel saludando → tigre rugiendo → león | Papá Noel (otro señor), sonrisa; Chandler no sale | saluda con la mano | collage: león, tigre, tigre blanco, cerdo hormiguero, ciervo | «BIG CAT SANCTUARY» (3), blanco + «SANCTUARY» amarillo | ninguno | estático | Santa FEEDS | ninguna |
| 43 | 0.47 | fauces naranjas → cara riendo con gafas → nutria | risa, ojos TAPADOS con gafas de espejo, sin sombrero | sujeta al cocodrilo por la cabeza | IA/collage: boca iluminada en naranja, nutria sacando la lengua | «CROCODILE ROUNDUP!» (2), blanco + amarillo | flecha a mano alzada | DURANTE | before the Cold Snap | ninguna |
| 48 | 0.43 | fauces del caimán → texto de 7 palabras → Chandler pequeño tirando | grito, ~1/8, sombrero y gafas de espejo con frontal | tira de una cuerda atada al hocico | IA: noche, remolque, valla; caimán en primer plano | «MOVING A HUGE ALLIGATOR TO MY FACILITY!» (7), blanco con «HUGE ALLIGATOR» amarillo | flecha (señala a la valla, a nada) | DURANTE | NEW BULL GATOR | ninguna |
| 2 | 2.06* | cara gritando → nutria abrazada → caimán en el agua y tigre suelto | grito, ~1/3, sombrero mojado | ABRAZA a la nutria (la protege) | IA: parque inundado, caimán y pitón nadando, tigre sobre un montículo | «WATER IS RISING!» (3), amarillo, borde negro | flecha a la valla | DURANTE (sube el agua) | Flooded… | ¿se escapan los animales? ¿la salva? |
| 1 | 1.03* | cara gritando → pollo crudo → caimán saltando | grito, ~1/4, sombrero | sostiene un pollo en alto | IA: parque embarrado, caimán, búho, nutria, cobra | «AFTER THE FLOOD» (3), amarillo | flecha al pollo | DESPUÉS | Finally Dropped… What We Found | ¿qué encontraron? |
| 4 | 0.54* | boca de cobra tragando (primerísimo plano) → cara seria detrás | serio, mirada fija, sin sombrero, camiseta gris | brazo extendido (selfie) | IA: macro de cobra tragando pitón, muy cerca | sin texto | flecha | DURANTE | Eats Python | ninguna nueva (cuarta vez) |
| 3 | 0.5* | cara gritando → dedo → pitón nadando y caimán | grito, ~1/3, sombrero mojado | metido en el agua hasta el pecho, señala | IA: parque inundado, pitón y caimán | «WE FLOODED!» (2), amarillo, borde negro | flecha a la pitón | DESPUÉS / durante | DISASTER / *UNCENSORED* | ¿qué desastre? (vago) |

## 3. Anatomía de la miniatura (con recuento)

Recuentos sobre los 54 salvo que diga «sin `*`» (50). Las comparaciones de ratio dentro de la **época IA** (#5–#40, 36
vídeos, feb.–oct. 2026 y los de enero que ya son IA) evitan mezclar con los meses antiguos de ratio bajo.

### Jerarquía
- **Lo primero que se ve** casi nunca es la cara: es **una boca abierta con dientes** (de cocodrilo, cobra, felino o
  komodo) en primer plano. Hay fauces abiertas de animal en 49/54 (no en #9, #23, #26, #35, #46). La cara de Chandler
  suele ser el segundo golpe, y el texto, el tercero. Lo primero es la cara en unas 15 (casi todas de la época collage,
  con cara de 1/3–1/2 del alto, o primeros planos como #28, #30, #33, #38).
- **Por qué**: las fauces van en el tercio más cercano a cámara, nítidas, con el interior rosa/naranja (el color más
  cálido y claro del cuadro) y dientes blancos con mucho microcontraste. La cara de Chandler, aun gritando, queda más
  atrás y más pequeña.
- **Nº de elementos con significado**: lo normal es 4–7 (cara + 2–6 animales + texto + flecha). Las más sencillas son
  3: #7 (Chandler, pitón, cocodrilo), #16 (Chandler, ciervo, cocodrilo), #18, #37. Las más cargadas: #20 (4 bloques de
  texto + calavera + flecha), #24 (4 renglones de texto + 4 cocodrilos + 2 flechas), #5 (6 serpientes + ratón).
- **¿Se entiende sin leer?** En 49/54, sí: el texto casi nunca hace falta para saber «hombre + bicho peligroso + algo
  pasa». Solo cambia el sentido si lees en #35 («MYSTERY ANIMAL BROKE IN!»), #9 («BIG NEWS!»), #40 («PRIVATE ZOO!»),
  #39 («FOR SALE!») y #28 («EMERGENCY!»).
- **Qué se pierde en pequeño** (hojas de 16): los textos largos (#24, #48, #21, #20: la placa «WORLD'S MOST VENOMOUS
  SNAKE!» y «COASTAL TAIPAN» son ilegibles); la lengua azul de #26; el tigre del fondo de #26 y #34; el ojo del agujero
  de #15 (se ve, pero no se entiende); los animales pequeños de #5 y #13 (parece un muestrario). Sobrevive siempre: una
  boca abierta grande, la cara gritando, la flecha roja y 2–3 palabras grandes («BIG NEWS!», «WE FLOODED!», «PRIVATE
  ZOO!»). Las de collage antiguo con fondo verde liso (#50–#54) se leen bien en pequeño, pero son todas iguales entre sí.

### Cara y cuerpo
- **Expresión** (54): **grito** 34 (boca en O, ojos muy abiertos con blanco alrededor del iris, cejas arriba, dientes
  de arriba visibles); **sonrisa o risa** 9 (#22, #32, #36, #40, #41, #43, #45, #50, #53); **neutra o intensa** 5 (#4, #8,
  #12, #26, #46); **triste o asustada** 4 (#23, #27, #28, #35); **sin cara de Chandler** 2 (#16, #44).
- **El grito no es lo que rinde.** En la época IA, con grito: 24 vídeos, mediana 1,06 (adj 1,00); sin grito: 12, mediana
  **1,35** (adj **1,28**). Los dos mejores sin grito: #40 (risa, mira al animal) 3,17 y #22 (sonrisa tranquila, de
  cuerpo entero, pequeño) 3,12. Y la única cara triste de verdad (#35, cejas en ángulo, boca hacia abajo) da 1,84.
- **Sombrero vaquero** en 38/54. Las 7 de la época IA sin sombrero (#12, #16, #22, #26, #35, #36, #40) tienen mediana
  **1,84** (adj 1,73) frente a 1,03 (adj 1,01) de las 29 con sombrero. Ojo: casi todas las de sin sombrero son la **cara
  real** de Chandler (pelo rizado suelto, sin el «personaje»), y la cara con sombrero, gritando y con brazos de
  culturista parece la versión generada (comparar #7 con #22 o #36 a tamaño completo: la de #7 tiene piel lisa en HDR,
  hombros hinchados y tatuajes inventados). Es un indicio con n=7, pero muy marcado.
- **Tamaño de la cabeza**: época collage (nov.–dic.) 1/3–1/2 del alto (#54, #52, #51, #47); época IA 1/6–1/4, porque
  se enseña el cuerpo y la acción. Cabeza pequeña (≤1/7) en 4: #22 3,12, #24 1,03, #45 0,61, #48 0,43: el tamaño no
  decide; lo que importa es lo que hace el animal.
- **Mirada**: a cámara en 47. Mira al animal en 3 (#12 0,9, #40 3,17, #46 0,68); ojos cerrados #41; ojos tapados por
  gafas de espejo #43 (0,47, ratio casi mínimo); #48 lleva las gafas en la frente. La mirada casi nunca lleva a nada:
  el que lleva el ojo es la flecha.
- **Manos** (54): sujeta al animal o el cebo 22 (pitones #11 y #25, ciervo #32, carne con pinzas #13, #30, #5, pollo #1,
  pavo #49, caja #15, gato de dientes de sable #40, cocodrilo #24 y #43, huevos #21, jeringa y lector #33); señala con el
  dedo 5 (#3, #6, #9, #14, #29); manos abiertas de susto 3 (#10, #31, #37); mano en la cabeza 1 (#23); tira de algo 3
  (#7, #32, #48); nada (busto) 20.
- **Ropa**: camiseta negra sin mangas casi siempre en la IA (el «uniforme» del personaje); camiseta de su merch «Be
  chill like Ziggy» en #12 y #35; disfraces: cirujano (#27), escarcha (#38), Papá Noel (#44, otro señor).
- **¿Es la emoción que tocaría?** El grito es igual ante una cobra que traga (#18), un recinto nuevo (#6), un microchip
  (#33) o un pavo (#49): no informa. Las caras que **sí** cuadran con la escena (calma junto a monstruos en #22, risa
  con un gato imposible en #40, pena ante una pérdida en #35) son justo las que más rinden.

### Sujeto
- **Escala**: en la época IA el animal se agranda sistemáticamente. Casos extremos: la cobra de #22 tiene la cabeza más
  grande que el torso de Chandler; el cocodrilo de #7 ocupa medio cuadro; el caimán de #48 y #45 va en primer plano con
  Chandler al fondo (gran angular forzado). Exageración que funciona: #22 3,12, #7 2,35. Que no: #48 0,43, #45 0,61 (ahí
  el animal grande está solo «siendo grande», sin comerse nada).
- **Acercado a cámara**: la boca del animal casi siempre va hacia el espectador (cobra de frente #10, #12; cocodrilos
  de frente #31; komodo #34).
- **Duplicados y clones**: #31 el mismo cocodrilo 3 veces, simétrico (0,55); #36 2 cobras casi iguales (2,32); #22 3
  cobras más la que traga (3,12); #46 dos mambas recortadas añadidas a la foto real (0,68).
- **Qué parte se enseña**: la boca abierta, siempre; los cuerpos se cortan con el borde del cuadro (cobra de #11 y #25,
  cocodrilo de #7) para que parezcan no acabar nunca.
- **Animal que come o va a comer** (presa o cebo a la vista): 15/54. Sin `*`: 13, mediana **1,34** (adj 1,35), frente a
  0,96 (adj 1,01) de las 37 sin presa. En la época IA: 11 con presa, adj 1,43 frente a 1,02.

### Lo que NO se enseña
- Lo normal es enseñarlo TODO: al menos 45/54 muestran el animal, la acción y hasta el desenlace.
- **Ocultación de verdad**, solo en 3: #15 (un ojo dentro de una caja con «DANGER», 1,27), #35 (un animal en silueta
  negra con ojos amarillos, 1,84) y #23 (cocodrilo medio tapado con una sábana, 1,03). Mediana 1,27, todas ≥1. Casi
  ocultación: #14 (estanque turbio del que asoman cabezas, 2,21).
- **Falsa ocultación** (pone «?» o «MYSTERY» pero enseña al animal): #34 «NEW MYSTERY ANIMAL?!» con el komodo a la vista
  (1,44); #42 «?» junto a la serpiente ya visible (0,64); #52 la cobra ya fuera de la caja de regalo (0,71). La caja
  CERRADA de #15 (1,27) contra la caja ABIERTA de #52 (0,71) es la diferencia en pequeño.
- **Censura o difuminado**: ninguno. El «*UNCENSORED*» de #3 está en el título y no se refleja en la imagen (0,5*).

### El instante
- **Antes** (amenaza a un palmo, cebo ofrecido, caja sin abrir): 16. Mediana 1,19 (adj 1,07).
- **Durante** (traga, tira, muerde, rompe): 20 (18 sin `*`). Mediana 1,04 (adj **1,22**). Aquí están 5 de los 6 mejores
  (#40, #22, #11, #7, #14).
- **Después** (herida, cadáver, «AFTER»): 5 (3 sin `*`): #35 1,84, #23 1,03, #28 0,99.
- **Futuro imaginado** (el recinto ya acabado): 2: #6 1,61, #29 1,01.
- **Estático** (posa rodeado de animales sin que pase nada): 11. Mediana **0,64** (adj 0,90). Es el peor grupo: #17, #31,
  #39, #41, #42, #44, #50, #51, #54, #24 (1,03), y la única excepción, #47 2,16 (felinos, tema raro en el canal).
- **Desequilibrio implícito** frecuente: tira y afloja (#7, #32, #48), algo a punto de morder la cara (#20, #10, #53),
  depredador que salta (#16, #25), valla que se rompe (#37).

### Fondo y profundidad
- **Época IA**: fondos reales «de catálogo», hiperdetallados: selva, recinto con valla, serpentario con terrarios, obra
  con excavadora. Tres capas casi siempre: fauces en primer plano / Chandler / fondo verde. El fondo cuenta algo en 10
  (parque inundado #1–#3, obra #6 y #29, remolque #9 y #48, quirófano #27, tienda #39, nieve #38, noche de #35). En el
  resto es solo verde.
- **Época collage**: verde liso o desenfocado (#49–#54, #47, #41), sin profundidad.
- **Oscuros**: solo 3: #22 (serpentario en penumbra con luz de recorte, 3,12), #35 (noche desaturada, 1,84), #48 (noche
  con focos, 0,43). Sobre el verde-amarillo dominante, lo oscuro destaca: 2 de 3 altas.

### Color y luz
- **Mandan**: verde selva (fondo), dorado/oliva/ocre de las pieles de reptil (sujeto), negro de la camiseta, rosa-naranja
  del interior de las bocas, y el amarillo/blanco del texto con la flecha roja. Saturación y microcontraste muy altos
  (aspecto HDR), piel de Chandler naranja tostada.
- **Lo más claro**: los dientes y el interior de la boca, o el texto amarillo.
- **Contraste frío/cálido** buscado solo en #38 (todo azul helado, 1,14) y #35 (gris-azulado con ojos amarillos, 1,84).
- **Contornos y halos**: casi no se usan. En los collages los recortes van sin borde (se nota el corte en #36 y #44); en
  la IA no hay recorte. No he visto contorno blanco en ninguna.

### Texto
- **En cuántas**: 31/54 (contando la etiqueta «FOR SALE!» de #39). Sin texto: 23. Además, texto dentro de la escena en
  4: «DANGER» y el cartel del zoo (#15), la pantalla «Microchip Detected» (#33), la camiseta de su merch (#12, #35).
- **Más texto no ayuda**: en la época IA, con texto 19 vídeos, mediana 1,03 (adj 1,01); sin texto 17, mediana 1,27 (adj
  1,09). 4 de los 6 mejores no llevan texto (#22, #11, #7, #14).
- **Nº de palabras**: mediana 3; de 1 («EMERGENCY!») a 10 (#20).
- **Función** (lo más útil que he encontrado sobre el texto):
  - **Nombre de la tarea** (gerundio o etiqueta de actividad): 12 — «FEEDING ALL OF MY ZOO ANIMALS!» #25 3,43, «FEEDING
    ALL OF MY ANIMALS!» #36 2,32, «FEEDING EVERYTHING! DON'T TRY THIS!» #30 0,99, «VISITING THE RAREST CROCODILES IN THE
    WORLD!» #24 1,03, «RAIDING A CROCODILE NEST!» #21 0,77, «EMERGENCY JAW SURGERY!» #27 0,76, «MICROCHIPPING A
    CROCODILE!» #33 0,75, «CROCODILE THANKSGIVING!» #49 0,75, «FEEDING MY BULL GATOR!» #45 0,61, «BIG CAT SANCTUARY» #44
    0,48, «CROCODILE ROUNDUP!» #43 0,47, «MOVING A HUGE ALLIGATOR TO MY FACILITY!» #48 0,43. Mediana **0,76** (adj 0,80).
    Solo se salvan los dos «FEEDING ALL».
  - **Noticia o acontecimiento** (algo ha pasado o está pasando): 8 sin `*` — «BIG NEWS!» #9 2,13, «MYSTERY ANIMAL BROKE
    IN! ??? WHAT HAPPENED» #35 1,84, «MY DREAM EXHIBIT!» #6 1,61, «EXTREMELY CLOSE CALL!» #20 1,47, «NEW MYSTERY
    ANIMAL?!» #34 1,44, «HEARTBREAKING NEWS...» #23 1,03, «My BIGGEST Project Yet!» #29 1,01, «EMERGENCY!» #28 0,99 (+
    «WATER IS RISING!» #2 2,06*, «AFTER THE FLOOD» #1 1,03*, «WE FLOODED!» #3 0,5*). Mediana **1,46** (adj 1,26).
  - **Etiqueta del animal o de su estado**: 8 — «PRIVATE ZOO!» #40 3,17, «NOT HAPPY!» #53 1,18 y #12 0,9, «WORLD'S MOST
    DANGEROUS SNAKE!» #19 0,96, «TYLER NOLAN'S!» #41 0,74, «NEW SNAKE!» #52 0,71, «NEW VENOMOUS SNAKE!» #42 0,64, «FOR
    SALE!» #39 0,52. Mediana 0,82.
- **Relación con el título**: repite palabras del título (eco) en 9 (#6, #12, #19, #20, #23, #24, #27, #42, #52;
  mediana 0,96); dice otra cosa en 19 (mediana 0,99). Aquí no hay diferencia por eco/no eco; la hay por función (arriba).
  Caso a mirar: el texto de #25 («FEEDING ALL OF MY ZOO ANIMALS!») es casi literal el **título** de #30 («FEEDING ALL MY
  ZOO ANIMALS!»), y en #25 el título dice otra cosa («Feeding My CRAZIEST ANIMALS!»): el título promete un adjetivo, y la
  imagen, la lista.
- **Tipografía**: palo seco condensada muy gruesa (tipo Anton/Bebas), relleno blanco o amarillo, **borde negro grueso
  + sombra**; en 6, una segunda letra de brocha cursiva («CLOSE CALL!» #20, «JAW SURGERY!» #27, «BULL GATOR!» #45,
  «A CROCODILE» #21, «HUGE ALLIGATOR» #48, «RAREST» #24). Tamaño: 13–35 % del alto. Posición: arriba en 28/31; abajo solo en
  #19, #29 y la etiqueta de #39; #35 reparte arriba y abajo. Inclinación ligera hacia arriba en
  6 (#20, #21, #24, #29, #45, #48).
- **Palabra en otro color** (amarillo sobre blanco) en 13: lo resaltado es el adjetivo de tamaño o rareza («BIGGEST»,
  «HUGE ALLIGATOR», «RAREST», «DANGEROUS»), la cantidad («ALL») o el lugar («ZOO», «SANCTUARY»). En #36 cada línea
  tiene un color (amarillo / blanco / degradado rojo-naranja).
- **Caja de fondo**: caja o brochazo rojo en 6 (#20, #21, #23, #27, #28, #35; mediana 1,01): siempre para alarma
  («EMERGENCY», «HEARTBREAKING», «MYSTERY ANIMAL»).

### Recursos gráficos
- **Flecha roja**: 33/54. De tres tipos: a mano alzada fina (época collage: #41, #46, #47, #50, #51, #53), de brocha con
  borde negro (IA: #18, #20, #30), y curva gruesa limpia (#10, #11, #25, #28). En la época IA: con flecha 18 (mediana
  1,03, adj 1,01), sin flecha 18 (mediana **1,27**, adj **1,28**). En los 10 peores hay 7 flechas; en los 10 mejores, 4.
  A veces señala lo que ya se ve sin ayuda (la boca abierta de #18, #10, #12) o a nada (#48 a la valla, #2 a la valla).
- **Dedo que señala** (la flecha hecha con el cuerpo): 5 (#3, #6, #9, #14, #29): 2,13, 2,21, 1,61, 1,01, 0,5*.
- **Interrogaciones**: 4 (#34 1,44, #35 1,84, #42 0,64, #52 0,71): rinden cuando lo de dentro está oculto (#35) o es
  dudoso (#34), no cuando el animal ya se ve.
- **«!!» amarillos de cómic**: 4 (#42, #49, #51, #54), todos ≤0,75 y de la época antigua. Abandonados después.
- **Calavera / triángulo de peligro**: 3 (#20 1,47, #42 0,64, #52 0,71).
- **Etiqueta de precio**: 1 (#39 «FOR SALE!», 0,52). **Corona dorada** sobre la cobra: 1 (#8, 1,39; la corona es el
  logo del canal, que también va en la camiseta en #10, #17, #19, #47).
- **Ojos brillantes**: 2 (#35 ojos amarillos del intruso, 1,84; #51 ojos rojos de LED en la cobra albina, 0,58).
- **Partida, antes/después, capturas, logos de terceros, emojis**: ninguno.

### Marca
- Lo reconocerías sin el nombre por: **sombrero vaquero marrón + camiseta negra sin mangas + rizos y barba + grito**,
  **boca de reptil abierta**, la **flecha roja** y el texto amarillo/blanco con borde negro. Paleta verde selva + dorado.
- **Evolución**: (1) nov.–dic. 2025: **collage** de recortes sobre verde liso, cara enorme (1/3–1/2), flechas finas a
  mano, «!!» y «?» de cómic, a veces gorra o gafas de sol (#49–#54, #47, #41, #46). (2) desde dic. 2025 (#48 el 2 dic.,
  #45, #43) y del todo desde feb. 2026: **escena fotorrealista hecha con IA**, Chandler de cuerpo entero como héroe de
  acción, animal enorme, acción en curso; fondos con historia (obra, inundación, quirófano). (3) Saltan del patrón, sin
  sombrero y con cara real: #40, #36, #35, #22, #26, #12, #4*, y son mayoría entre los mejores.

### Realidad
- **Generada o rehecha con IA**: 41/54. **Collage de fotos**: 11. **Foto tal cual**: 2 (#16, y #46 con mambas añadidas).
- **Inventado respecto a lo que promete el título**: un felino de dientes de sable que no existe (#40; el título lo
  matiza con «?!»); una cobra más grande que un hombre (#22); 3 cocodrilos clonados (#31); tigres que el título no
  menciona (#15, #26, #34, #2*); animales escarchados en Florida (#38); el recinto aún sin construir, ya acabado (#6,
  #29); Chandler de cirujano (#27); un taipán mordiéndole la cara (#20); un «animal misterioso» de lobo (#35). Cuanto
  más imposible es lo inventado (#40, #22), mejor rinde; cuando lo inventado es solo «más bonito» (#29, #31, #45), no.

## 4. Anatomía del título (con recuento)

Sobre los 54 (ratios sin `*` salvo aviso).

- **Longitud**: mediana 31 caracteres y 5 palabras (16–49). La longitud no separa: los 10 mejores, mediana 28; los 10
  peores, 28,5.
- **Primera palabra**: «Feeding/FEEDING» 9, «My» 6, «NEW» 4, «King/KING» 4, «The» 2, «I» 2, «Catching» 2; el resto, una
  vez cada una. Empezar por **Feeding**: 9 vídeos, mediana **1,34** (adj 1,35), frente a 0,99 del resto.
- **Palabra-gatillo y dónde va**: casi siempre en MAYÚSCULAS y en la segunda mitad: «Feeding My **CRAZIEST** ANIMALS!»,
  «Crocodiles **EAT** Big Python!», «My King Cobra Was **NOT** Happy Today!», «This Is Every Keeper's **WORST**
  Nightmare». Las mayúsculas caen sobre: el animal (KING COBRA(S), CROCODILES, SNAKES, BIG CATS, BULL GATOR) unas 22
  veces; un adjetivo de grado (CRAZIEST, RAREST, MOST, MASSIVE, DREAM, WORST, WHOLE) unas 14; el verbo de comer (EAT,
  EATS, FEEDS) 4; la negación (NOT) 3; la emoción (BELIEVE, CLOSE CALL, DISASTER) 4. 42/50 llevan 1–3 palabras en
  mayúsculas. **Todo en mayúsculas**: 5 (#9 2,13, #30 0,99, #37 0,77, #51 0,58, #52 0,71; mediana 0,77): gritar el título
  entero no ayuda.
- **Signos**: termina en «!» 46/54. **Sin exclamación**: 5 sin `*`, mediana **1,44**: «This Is Every Keeper's WORST
  Nightmare» #35 1,84, «What's in my Mystery Pond??» #14 2,21, «I Wasn't Expecting THIS Animal…» #34 1,44, «Heartbreaking
  News…» #23 1,03, «Earning my Alligator's trust again» #45 0,61. Los puntos suspensivos (4: #1, #2, #23, #34) van en
  frases de historia. Interrogación: 2 (#14 «??» 2,21, #40 «?!» 3,17), las dos altas.
- **Cifras**: casi no hay: 1 (#9 «RESCUING **3** CROCODILES!», 2,13). Ningún precio, tamaño, peso ni tiempo.
- **Persona y tiempo**: primera persona (My/I/We) en 19/50, sin efecto claro (adj 1,08 frente a 1,01). Presente casi
  siempre; pasado en 6 (#12, #21, #28, #34, #37, #2*), mediana 0,9.
- **Qué se nombra con exactitud**: la especie (cobra real, cocodrilo, pitón, mamba, ciervo) en 37/50. **Qué se deja
  vago a propósito**: el suceso, con un deíctico o una emoción: «THIS Animal», «this Happened», «What's in», «Here's What
  We Found», «Heartbreaking News», «WORST Nightmare», «NOT SUPPOSED TO HAPPEN», «DISASTER Strikes», «what this Pet Shop
  sells» (9; sin `*` 7, mediana 1,03, de 0,52 a 2,21). Lo vago funciona cuando la imagen TAMBIÉN calla (#35, #14, #34) y
  falla cuando la imagen lo resuelve (#37: el cocodrilo ya rompió la valla; #39: ya se ve lo que venden).
- **Qué tipo de pregunta deja**: «¿cómo se lo come?» (banquetes), «¿qué es / quién fue?» (misterio), «¿le muerde?»
  (amenaza), «¿qué le ha pasado?» (pérdida). Las dos primeras son las que mejor rinden (ver 6).

### Moldes (con huecos)
1. **«Feeding [cuantificador/adjetivo] [ANIMALES en plural]!»** — 9: #25 «Feeding My CRAZIEST ANIMALS!» 3,43; #36
   «Feeding My Venomous Snakes & Crocodiles!» 2,32; #47 «Feeding BIG CATS!» 2,16; #16 «Feeding WHOLE DEER to my
   Crocodiles!» 1,36; #32 1,34; #30 «FEEDING ALL MY ZOO ANIMALS!» 0,99; #13 «Feeding my VENOMOUS SNAKES!» 0,94; #49
   0,75; #54 «Feeding VENOMOUS Snakes!» 0,72. Mediana 1,34. Cuando lo que come son serpientes venenosas, baja (#13,
   #54); cuando es un banquete de bestias (cocodrilos, felinos, «craziest»), sube.
2. **«[Depredador(es)] EAT(S) [presa]!»** — 4: #11 «King Cobras & Crocodile EAT Pythons!» 2,94; #7 «Crocodiles EAT Big
   Python!» 2,35; #18 «King Cobra EATS Huge Python!» 0,66; #4 «King Cobra Eats Python!» 0,54*. (Y #22 «Giant Hungry KING
   COBRAS!» 3,12, que es lo mismo sin el verbo.) **Depredador en plural: 3/3 altos** (3,12, 2,94, 2,35; adj 3,14, 1,99,
   1,59); **en singular: 2/2 bajos** (0,66, 0,54*; adj 0,57, 0,36).
3. **«NEW [animal]…!»** — 6: #15 «NEW ANIMAL Joins the ZOO!» 1,27; #53 «NEW Snake is NOT Friendly!» 1,18; #52 «NEW
   VENOMOUS SNAKE!» 0,71; #46 «BLACK MAMBA gets NEW HOME!» 0,68; #42 «NEW Venomous Snakes!» 0,64; #48 «Bringing NEW BULL
   GATOR HOME!» 0,43. Mediana **0,70**. Solo se salva con conflicto («is NOT Friendly») o con la caja cerrada de #15.
4. **Superlativo de catálogo («World's MOST…», «RAREST…», «MOST DANGEROUS…»)** — 6: #20 1,47; #24 1,03; #19 0,96; #50
   0,78; #33 0,75; #17 0,64. Mediana **0,87**. «RARE/RAREST» 3/3 ≤1,03.
5. **Gerundio de faena («Catching / Training / Bringing / Earning / Searching / Saving / Building / Rescuing…»)** — 9:
   #9 «RESCUING 3 CROCODILES!» 2,13; #6 «Building my DREAM Crocodile Exhibit!» 1,61; #26 1,2; #38 1,14; #33 0,75; #45
   0,61; #31 «Training RARE CROCODILES!» 0,55; #43 «Catching Crocs before the Cold Snap!» 0,47; #48 0,43. Mediana
   **0,75**. Contar una tarea no engancha; un rescate o un sueño, sí.
6. **Frase de historia con hueco (sin animal)** — 7 sin `*`: #14 2,21, #35 1,84, #34 1,44, #23 1,03, #28 0,99, #37
   0,77, #39 0,52. Mediana 1,03, muy repartida (ver «vago a propósito»).
7. **«My [cosa] [cambio]»** (proyecto personal) — #6 1,61; #10 «My King Cobra's Enclosure Got a MASSIVE Makeover!» 1,56;
   #29 «My Dream Crocodile Exhibit Is Finally Happening!» 1,01; #12 0,9; #21 «My Crocodile Finally laid EGGS!» 0,77.
   Mediana 1,01.

### Palabras que se repiten y con qué ratio van
- Más frecuentes: my 17, feeding 10, king 8, venomous 8, crocodiles 8, cobra(s) 8, snakes 7, new 6, animals 5, most 4.
- Con los altos: **EAT/Feeding/Hungry** (comer: 6 de los 10 mejores, 2 de los 10 peores), plurales de bestias con «&»
  (los 2 títulos con «&» son altos: #11 2,94, #36 2,32), CRAZIEST, Giant, Mystery, WORST.
- Con los bajos: **NEW** (mediana 0,70), **RARE/RAREST** (≤1,03), **VENOMOUS** (8 títulos, mediana 0,86), **MOST**
  (0,64–0,96 salvo #20), gerundios de faena (Catching, Training, Bringing, Earning), fiestas (THANKSGIVING, Santa).

### Tono
Asombro ante el tamaño o la voracidad (CRAZIEST, Giant Hungry, Saber-Toothed) y amenaza (CLOSE CALL, DANGEROUS) son
los más usados. Drama o pérdida en 4 (Heartbreaking, WORST Nightmare, DISASTER, Can't Believe). Humor casi nunca
(«Santa FEEDS BIG CATS!», 0,48). Ternura nunca en el título (las nutrias solo salen en la imagen).

## 5. El encaje: qué pasa en la cabeza de quien lo ve

### Reparto
- **Solo el título dice**: la especie concreta y el verbo (EAT, Feeding), el «my» (es su zoo), el matiz de duda («?!»).
- **Solo la imagen dice**: la escala (todo es enorme), la cara del presentador, el peligro físico, los animales extra
  (nutria, búho, tigre) y, casi siempre, el desenlace.
- **Repiten los dos**: el animal y el acto en los banquetes; el texto copia el título en 8.
- **Callan los dos**: qué pasa al final (si le muerde, si el animal vive) solo en unos 8; en el resto la imagen ya lo
  enseña todo y la pregunta que queda es «¿cómo?», no «¿qué?».

### Tipos de encaje (50 sin `*`, cada vídeo en uno)
| tipo (nombre mío) | qué hace | n | mediana | vídeos |
|---|---|---|---|---|
| C. Imposible con duda | la imagen inventa un animal; el título pregunta si existe | 1 | 3,17 | #40 |
| F. Adjetivo + muestrario | el título da una palabra colectiva o de grado (CRAZIEST, ALL, BIG CATS); la imagen, el inventario de bestias | 6 | 1,65 | #25, #36, #47, #38, #30, #49 |
| B. Doble silencio | la imagen esconde (caja, silueta, sábana, barro) y el título lo subraya sin decirlo | 5 | 1,44 | #14, #35, #34, #15, #23 |
| A. Banquete agigantado | el título nombra quién come qué; la imagen lo enseña a escala imposible, sin texto | 7 | 1,36 | #22, #11, #7, #16, #32, #13, #18 |
| I. Complemento | el título dice qué; la imagen añade la escala o la emoción (o al revés) | 8 | 1,10 | #9, #10, #8, #53, #29, #21, #46, #48 |
| D. Eco | el texto de la miniatura repite el título | 8 | 0,93 | #6, #20, #24, #19, #12, #27, #52, #42 |
| E. Título que intriga, imagen que lo resuelve | el título calla («NOT SUPPOSED TO HAPPEN»), la imagen lo cuenta | 3 | 0,77 | #28, #37, #39 |
| G. Desencaje | título e imagen hablan de cosas distintas | 7 | 0,74 | #26, #5, #33, #41, #45, #44, #43 |
| H. Posado + categoría | Chandler rodeado de bichos quietos y un título de catálogo | 5 | 0,64 | #50, #54, #17, #51, #31 |

Ejemplos del desencaje (G): #33, título «Catching the RAREST Crocodiles on Earth!» y miniatura «MICROCHIPPING A
CROCODILE!»; #45, «Earning my Alligator's trust again» y «FEEDING MY BULL GATOR!»; #5, «CLOSE CALL…» sin ningún casi
accidente en la imagen; #26, «Searching for WILD KING COBRAS!» con un tigre que no viene a cuento.

### La segunda lectura
7 casos en que el título le da la vuelta a la imagen (mediana 1,39):
- #8 1,39: imagen = cobra con corona (gracioso, «el rey»); título «KING COBRA needs HELP!» → el rey está en apuros.
- #40 3,17: imagen = bestia de fantasía, se lee como montaje; título «Modern day Saber-Toothed Tiger?!» → ¿y si existe?
- #35 1,84: imagen = sombra de lobo y cocodrilo tumbado (de miedo); título «Every Keeper's WORST Nightmare» → una muerte.
- #14 2,21: imagen = charco con bichos; título «Mystery Pond??» → el estanque de casa escondía todo eso.
- #23 1,03: imagen = cocodrilo que podría estar dormido; título «Heartbreaking News…» → ha muerto (la sábana ya lo
  insinuaba).
- #31 0,55: imagen = tres cocodrilos amenazando; título «Training…» → son dóciles. Le quita el peligro: no funciona.
- #44 0,48: imagen = Papá Noel con felinos; título «Santa FEEDS BIG CATS!» → solo lo confirma, sin giro real.
La segunda lectura funciona cuando SUMA misterio o peligro (#40, #35, #14, #8) y no cuando lo quita (#31).

### 10 parejas diseccionadas
1. **#25 «Feeding My CRAZIEST ANIMALS!» (3,43)** — Chandler con los brazos en alto, carne en una mano y pitón en la otra;
   un cocodrilo salta a por la carne y una cobra a por la pitón; búho y nutria arriba. *Primer segundo*: ve dos bocas a
   punto de cerrarse sobre sus manos. *Siguiente*: lee «FEEDING ALL OF MY ZOO ANIMALS!» y, en el título, «CRAZIEST».
   *Pregunta*: ¿qué pasa cuando suelta los cebos, y cuál de estos es el más loco? *Por qué no puede contestarla sin
   entrar*: la imagen congela el instante anterior a dos mordiscos a la vez.
2. **#40 «Modern day Saber-Toothed Tiger?!» (3,17)** — un hombre que ríe sujetando un felino con colmillos de sable; la
   cabeza ampliada rugiendo al lado. *Primer segundo*: unos colmillos imposibles. *Siguiente*: «PRIVATE ZOO!» y el
   título con «?!». *Pregunta*: ¿existe hoy un animal así, y alguien lo tiene en casa? *Por qué entra*: lo imposible
   viene con una pista de que es real (una persona tranquila lo abraza), y el título no lo afirma: lo pregunta.
3. **#22 «Giant Hungry KING COBRAS!» (3,12)** — cobra gigante tragando una pitón; otras tres cobras alzadas; Chandler
   pequeño, agachado, sonriendo. *Primer segundo*: la cabeza de la cobra, más grande que un hombre. *Siguiente*: el
   hombre sonríe; «Giant Hungry». *Pregunta*: ¿cómo de grandes son, y por qué este tío está tan tranquilo? *Por qué
   entra*: el contraste calma/monstruo no se resuelve en la imagen.
4. **#11 «King Cobras & Crocodile EAT Pythons!» (2,94)** — Chandler en el centro con dos pitones; a un lado una cobra
   muerde una, al otro un cocodrilo muerde la otra. *Primer segundo*: un grito entre dos depredadores. *Siguiente*: «EAT
   Pythons». *Pregunta*: ¿quién se la come antes? *Por qué entra*: es un duelo de depredadores con árbitro humano, y el
   resultado no está en la imagen.
5. **#7 «Crocodiles EAT Big Python!» (2,35)** — tira y afloja: Chandler tira de una pitón cuyo otro extremo muerde un
   cocodrilo. *Primer segundo*: la fila de dientes cerrada sobre la serpiente. *Siguiente*: «EAT Big Python». *Pregunta*:
   ¿gana el cocodrilo, le arrastra a él? *Por qué entra*: congela el forcejeo en su punto medio.
6. **#36 «Feeding My Venomous Snakes & Crocodiles!» (2,32)** — selfie sonriente en el agua con carne en la mano, rodeado
   de cobras, nutria, cocodrilos y búho; texto de tres colores. *Primer segundo*: «ANIMALS!» en rojo enorme y bocas por
   todas partes. *Siguiente*: el título concreta «Venomous Snakes & Crocodiles». *Pregunta*: ¿cómo da de comer a todo
   esto, y a quién primero? *Por qué entra*: la sonrisa tranquila frente a tanta boca abierta.
7. **#48 «Bringing NEW BULL GATOR HOME!» (0,43, la peor)** — de noche, Chandler pequeño al fondo tira de una cuerda atada
   al hocico de un caimán que ocupa el primer plano; texto de 7 palabras. *Primer segundo*: un caimán con la boca
   abierta, como tantos otros. *Siguiente*: tiene que leer «MOVING A HUGE ALLIGATOR TO MY FACILITY!». *Pregunta*: casi
   ninguna: ya sabe lo que pasa (lo traslada). *Por qué no engancha*: imagen y texto cuentan la tarea entera; «NEW» y
   «HOME» son palabras de trámite. (Además es de la época de ratios bajos: adj 0,62.)
8. **#44 «Santa FEEDS BIG CATS!» (0,48)** — un Papá Noel (que no es Chandler) saluda entre leones y tigres; «BIG CAT
   SANCTUARY». *Primer segundo*: un señor disfrazado. *Siguiente*: un nombre de lugar. *Pregunta*: ninguna; es una
   postal. *Por qué no engancha*: falta la cara conocida, no pasa nada y el gancho es de calendario (salió el 24 de
   diciembre). Comparar con #47 «Feeding BIG CATS!» (2,16), tres semanas antes.
9. **#35 «This Is Every Keeper's WORST Nightmare» (1,84, rara)** — Chandler triste, de noche, con un cocodrilo tumbado y
   un animal negro de ojos amarillos; «MYSTERY ANIMAL BROKE IN! ??? WHAT HAPPENED». *Primer segundo*: unos ojos que
   brillan en la sombra. *Siguiente*: la cara triste y «BROKE IN». *Pregunta*: ¿qué animal entró y qué le hizo al
   cocodrilo? *Por qué entra*: es la única miniatura «de crimen»: hay víctima, hay sospechoso sin cara y no hay
   respuesta. Rompe todas las normas del canal (sin grito, sin sombrero, oscura) y es de las mejores.
10. **#16 «Feeding WHOLE DEER to my Crocodiles!» (1,36, rara)** — fotograma real: Chandler de espaldas lanza un cervato
   y un cocodrilo salta con la boca abierta. *Primer segundo*: el cocodrilo en vertical. *Siguiente*: el ciervo en el
   aire; «WHOLE DEER». *Pregunta*: ¿se lo traga entero? *Por qué entra*: el instante justo antes del bocado, real. Sin
   cara, sin texto, sin flecha y sin IA, rinde igual que #32 (1,34), que tiene todo eso y el mismo título.

## 6. Mecanismos psicológicos (con recuento)

Un mecanismo dominante por vídeo (50 sin `*`), agrupados:

| mecanismo | n | mediana | vídeos (ratio) |
|---|---|---|---|
| Imposible / fantasía (un animal que no puede existir) | 1 (+#22 como segundo) | 3,17 | #40 |
| Rescate o gran noticia | 2 | 1,76 | #9 2,13, #8 1,39 |
| Misterio / hueco (qué hay dentro, quién fue) | 4 | **1,64** | #14 2,21, #35 1,84, #34 1,44, #15 1,27 |
| Espectáculo de comer (ver a una fiera devorar algo) | 7 | **1,34** | #22 3,12, #11 2,94, #7 2,35, #16 1,36, #32 1,34, #13 0,94, #18 0,66 |
| Proyecto / transformación (el recinto soñado) | 2 | 1,31 | #6 1,61, #29 1,01 |
| Búsqueda / expedición | 1 | 1,2 | #26 |
| Arca o abundancia (todos sus animales a la vez) | 10 | 1,05 | #25 3,43, #36 2,32, #47 2,16, #38 1,14, #5 1,1, #30 0,99, #50 0,78, #49 0,75, #54 0,72, #51 0,58 |
| Amenaza al presentador (le va a morder / le ataca) | 6 | 1,04 | #10 1,56, #20 1,47, #53 1,18, #12 0,9, #37 0,77, #21 0,77 |
| Pérdida / emergencia de un animal suyo | 3 | 0,99 | #23 1,03, #28 0,99, #27 0,76 |
| Récord de peligrosidad («el más peligroso») | 2 | 0,80 | #19 0,96, #17 0,64 |
| Rareza / novedad («nuevo», «el más raro», «se vende») | 7 | **0,68** | #24 1,03, #52 0,71, #33 0,75, #46 0,68, #42 0,64, #31 0,55, #39 0,52 |
| Invitado o fecha señalada | 2 | 0,61 | #41 0,74, #44 0,48 |
| Manejo del animal (domarlo, moverlo, sujetarlo) | 3 | **0,47** | #45 0,61, #43 0,47, #48 0,43 |

- **Funcionan**: el misterio con algo realmente oculto, lo imposible, y ver comer a una fiera **cuando hay más de un
  depredador o la escala es absurda**. El «arca» funciona solo con una presentación clara (cada animal en su sitio,
  cebos en la mano) y falla como muestrario plano (#50, #51, #54).
- **Se intentan y NO funcionan aquí**: rareza/novedad (7 casos, mediana 0,68: «NEW», «RAREST», «FOR SALE»); el récord
  de peligrosidad (#17, #19); el manejo (moverlo, cogerlo: #43, #45, #48); el humor o la fiesta (#44, #49); el
  invitado (#41, #46). La amenaza al presentador solo funciona si la imagen la enseña (#20 1,47 con el taipán en la
  cara, frente a #5 1,1 con «CLOSE CALL» y nada en la imagen; adj 1,43 frente a 0,71).
- **Ternura**: las nutrias salen en 10 miniaturas (mediana 1,07 sin `*`), siempre de adorno, nunca como mecanismo. El
  único abrazo de verdad (#2, la nutria protegida de la riada) es el mejor de los recientes (2,06*).

## 7. Las que más y las que menos rinden, al detalle

**Top 10** (sin `*`): #25 3,43, #40 3,17, #22 3,12, #11 2,94, #7 2,35, #36 2,32, #14 2,21, #47 2,16, #9 2,13, #35 1,84.
**Bottom 10**: #48 0,43, #43 0,47, #44 0,48, #39 0,52, #31 0,55, #51 0,58, #45 0,61, #17 0,64, #42 0,64, #18 0,66.

| rasgo | top 10 | bottom 10 |
|---|---|---|
| animal comiendo o cebo a la vista | 5 (#25, #22, #11, #7, #36) | 2 (#45, #18) |
| más de un depredador en acción | 5 (#25, #22, #11, #36, #47) | 0 (en #17 y #51 hay varios, pero quietos) |
| cara SIN grito (calma, risa, pena) | 4 (#40, #22, #36, #35) | 3 (#43 con gafas, #45 pequeña, #44 no es él) |
| sin sombrero | 4 (#40, #22, #36, #35) | 3 (#43, #44, #45) |
| algo oculto o imposible | 4 (#40, #22, #14, #35) | 0 |
| flecha roja | 4 | 7 |
| texto | 5 (de noticia o de lista) | 6 (de tarea o lugar: ROUNDUP, SANCTUARY, BULL GATOR, MOVING…; y FOR SALE, NEW VENOMOUS SNAKE) |
| instante estático (posado) | 1 (#47) | 6 (#44, #39, #31, #51, #17, #42) |
| título con verbo o idea de comer (EAT, Feeding, Hungry) | 6 | 2 («Santa FEEDS», #18 «EATS») |
| título con NEW / RARE / MOST | 0 | 4 (#48, #42, #31, #17) |
| título con gerundio de faena | 1 (#9 Rescuing) | 4 (Bringing, Catching, Training, Earning) |
| época antigua (nov. 25–ene. 26) | 2 (#47, #40) | 7 (#48, #43, #44, #39, #51, #45, #42) |

**Otra explicación**: la fecha pesa: 7 de los 10 peores son de los tres primeros meses (canal más pequeño). Pero los
otros 3 (#31 marzo, #17 y #18 julio) son de la época buena, y los tres comparten miniatura estática o repetida y título
de catálogo. Los felinos (#47, #40) son tema raro en el canal; #9 («RESCUING 3 CROCODILES!») y #35 son historias con
algo en juego. Que los dos de felinos estén arriba con miniaturas de época antigua dice que ahí pesó el tema.

### Parejas casi iguales con resultado muy distinto
1. **#22 (3,12) / #11 (2,94) / #18 (0,66) / #4 (0,54*)** — la misma escena: cobra real tragando una pitón, en IA. Cambia:
   #22 tiene **cuatro cobras** y la que traga es más grande que Chandler, que está tranquilo y pequeño; #11 tiene **dos
   depredadores** (cobra y cocodrilo); #18 y #4 tienen **una sola cobra**, a escala creíble, y Chandler grita (#18) o
   mira serio (#4). Títulos en plural («KING COBRAS», «King Cobras & Crocodile») frente a singular («King Cobra EATS Huge
   Python!», «King Cobra Eats Python!»). Además #18 sale un mes después de #22 (repetición) y dentro de la racha de julio.
   Regla que sale: **la segunda vez que enseñas el mismo banquete, multiplica a los comensales**.
2. **#2 (2,06*) / #3 (0,5*) / #1 (1,03*)** — la misma inundación, la misma plantilla (IA, agua marrón, caimán y pitón
   nadando, Chandler mojado gritando, texto amarillo de 2–3 palabras arriba a la der.). Cambia: título «My Wildlife Park
   Flooded…» (concreto, «my», puntos suspensivos) frente a «DISASTER Strikes! *UNCENSORED*» (vago, de cebo); texto «WATER
   IS RISING!» (está pasando) frente a «WE FLOODED!» (ya pasó) y «AFTER THE FLOOD» (después); en #2 **abraza a la
   nutria** y hay un **tigre suelto** en un montículo; en #3 solo señala una pitón. Resultado: 4 veces las visitas con un
   día menos. **Pero #3 está restringido por edad** (`needs_auth`, es la versión «UNCENSORED»): eso explica su caída
   mejor que cualquier diferencia de título o miniatura. Lo único utilizable es #2 frente a #1 (1,03*, «AFTER THE
   FLOOD», el después), y con muy pocos días.
3. **#25 (3,43) / #36 (2,32) / #30 (0,99)** — dar de comer a todo el zoo. #30 lleva justo el título que en #25 es el
   texto de la miniatura. Cambia: #25 enseña a Chandler de medio cuerpo con los cebos en alto y cada animal en su
   cuadrante (se lee en pequeño); #30 es un primer plano apretado, con los animales solapados y el texto genérico «DON'T
   TRY THIS!». El título de #30 va todo en mayúsculas y describe; el de #25 promete un adjetivo («CRAZIEST»). #36
   (collage, sonrisa) también funciona. Fechas: #36 feb., #30 mar., #25 may. (adj 2,43 / 0,90 / 3,36): no es la fecha.
4. **#47 (2,16) / #44 (0,48)** — felinos de un santuario, collage, mismo mes. #47: Chandler gritando en el centro, cuatro
   felinos encima, sin texto. #44: Papá Noel (otro señor), texto «BIG CAT SANCTUARY», 24 de diciembre.
5. **#32 (1,34) / #16 (1,36)** — mismo título («Feeding WHOLE DEER to my CROCODILES!») con 4 meses de diferencia. #32: IA,
   Chandler riendo con sombrero, tira y afloja. #16: foto real, de espaldas, sin texto ni flecha. **Mismo resultado**: el
   estilo (IA o real, cara o sin cara) no decidió; el tema y el instante (el bocado), sí.
6. **#53 (1,18) / #52 (0,71) / #42 (0,64)** — serpiente nueva, collage sobre verde, misma época. #53 añade conflicto en el
   título («is NOT Friendly») y en la imagen (la boa lanza la cabeza hacia él, «NOT HAPPY!»). #52 y #42 solo dicen «NEW
   (VENOMOUS) SNAKE!» y enseñan al animal quieto con iconos de «?», «!!» y calavera.
7. **#20 (1,47) / #5 (1,10)** — los dos con «CLOSE CALL» en el título y serpientes venenosas. #20 ENSEÑA el casi
   accidente (el taipán en la mejilla); #5 enseña un muestrario de 6 serpientes y un ratón: el «close call» no aparece.
   Adj 1,43 frente a 0,71.
8. **#19 (0,96) / #17 (0,64)** — mamba negra en el gancho con Chandler gritando, a 8 días. #19: una sola serpiente, texto
   «WORLD'S MOST DANGEROUS SNAKE!», título personal «…Snake I Own!». #17: tres serpientes, sin texto, título de lista
   «World's MOST Dangerous Snakes!». Ganó la versión singular y personal (aquí el singular gana porque es «la peor de
   todas», no un banquete).
9. **#35 (1,84) / #23 (1,03)** — la pérdida de un cocodrilo. #23 la anuncia («HEARTBREAKING NEWS…», cocodrilo bajo una
   sábana): la noticia ya está dada. #35 la plantea como misterio («MYSTERY ANIMAL BROKE IN!», un culpable en silueta):
   la noticia está por descubrir.
10. **#15 (1,27) / #52 (0,71)** — animal nuevo en una caja. #15: caja de madera cerrada, solo se ve un ojo. #52: caja de
   regalo abierta con la cobra fuera.
11. **#6 (1,61) / #29 (1,01)** — el recinto soñado, IA del recinto acabado, mismo molde de texto. Adj 1,09 / 1,00: aquí la
   diferencia la explica la fecha (abril frente a octubre), no el empaquetado.
12. **#28 (0,99) / #27 (0,76)** — mandíbula rota, primera y segunda parte. La segunda ya cuenta el desenlace («SURGERY»).

## 8. Trucos de oficio y recetas

### Lista de trucos (veces · ejemplo)
- Boca abierta del animal hacia cámara en primer plano, con el interior rosa como lo más claro del cuadro · 49/54 · #10.
- Escena entera hecha con IA alrededor de la cara del presentador (fotorrealismo HDR) · 41 · #7.
- Sombrero vaquero marrón y camiseta negra sin mangas como uniforme del personaje · 38 · #11.
- Cara de grito: boca en O, blanco del ojo alrededor del iris, cejas arriba · 34 · #47.
- Flecha roja hacia la boca o la presa (aunque ya se vea) · 33 · #18.
- Cebo en la mano del presentador, a un palmo de la boca del depredador · 9 · #25.
- Composición en «Y»: brazos en alto, un depredador por cada mano · 2 · #25, #11.
- Animal agrandado hasta ser más grande que el presentador, que está pequeño y tranquilo · 1 · #22.
- Clonar al mismo animal (2–4 copias) · 4 · #31, #36, #22, #46.
- Animal de adorno que el título no menciona (tigre, búho, nutria) · ~14 · #26.
- Texto amarillo y blanco de palo seco condensado con borde negro grueso, la palabra de grado en amarillo · 31 · #24.
- Caja o brochazo rojo detrás de la palabra de alarma (EMERGENCY, HEARTBREAKING, MYSTERY ANIMAL) · 6 · #28.
- Dedo que señala en lugar de flecha · 5 · #9.
- Algo escondido a la vista: ojo en un agujero, silueta con ojos brillantes, sábana · 3 · #15, #35, #23.
- Texto dentro de la escena (cartel, caja estampada «DANGER», pantalla de aparato, camiseta de su merch) · 4 · #15, #33.
- Corona del logo del canal puesta sobre el animal (juego con «King Cobra») · 1 · #8.
- Disfraz de situación (cirujano con mascarilla bajada y bisturí; escarcha en la cara) · 2 · #27, #38.
- Fondo que cuenta el suceso (inundación, obra con excavadora, quirófano, remolque) · 10 · #2.
- Interrogaciones gigantes de tres colores (blanco-amarillo-blanco) · 1 · #35.
- Iconos de cómic «!!», «?» pixelado, calavera en triángulo (época antigua, luego abandonados) · 7 · #42.
- Etiqueta de precio amarilla «FOR SALE!» · 1 · #39.
- Ojos de LED rojos añadidos a una cobra albina · 1 · #51.

### Recetas (los 5 tipos que rinden y el que no)
1. **Banquete agigantado** (#22, #11, #7; con depredadores en plural, 2,35–3,12). 16:9. Depredador(es) en primer plano
   ocupando el 50–70 % del cuadro, boca abierta CON la presa dentro (pitón amarilla/naranja que contraste con el reptil
   oliva); si la escena ya se usó, 2–4 depredadores. El presentador en el 30–40 % del lado contrario, de cuerpo entero o
   medio cuerpo, cabeza de 1/6–1/7 del alto; o agarrando el otro extremo de la presa (tira y afloja). Expresión: calma
   sonriente si el animal es monstruoso, grito si está en pleno forcejeo. Fondo real oscuro de serpentario o selva
   desenfocada. Sin texto. Flecha opcional (no suma). Título: «[Depredadores en plural] EAT [presa]!» o «Giant Hungry
   [DEPREDADORES]!».
2. **Arca con cebos** (#25, #36; 3,43 y 2,32). Presentador centrado, de medio cuerpo, brazos en alto en «Y» con un cebo en
   cada mano (carne cruda, pitón, pescado). Cuatro animales, uno por esquina, cada uno con la boca hacia su cebo:
   cocodrilo saltando del agua (abajo izq.), cobra alzada (abajo der.), búho con alas abiertas (arriba izq.), nutria con
   un pez (arriba der.). Texto arriba, 5–6 palabras, 25–35 % del alto: «FEEDING ALL OF MY [ZOO] ANIMALS!» con «ALL» o la
   última palabra en otro color. Título: «Feeding My [ADJETIVO DE GRADO] ANIMALS!».
3. **Doble silencio / misterio** (#35, #14, #15; 1,27–2,21). Cara real del presentador SIN grito: preocupado o atónito,
   mirando a cámara. A su lado, la víctima (animal tumbado) o el contenedor (caja con «DANGER», estanque turbio). El
   culpable o el contenido, solo en silueta negra con ojos amarillos, o un ojo en un agujero. Luz baja, desaturada, fría.
   Texto: «MYSTERY ANIMAL» en caja roja + «BROKE IN!» + «???» blanco-amarillo-blanco + «WHAT HAPPENED» en amarillo abajo.
   Título sin exclamación, frase de historia: «This Is Every Keeper's WORST Nightmare», «What's in my Mystery Pond??».
4. **Imposible creíble** (#40; 3,17). Un animal real con un rasgo exagerado hasta lo fantástico (colmillos de sable), en
   brazos del presentador, que ríe mirándolo (la normalidad da credibilidad). A la derecha, la cabeza del animal
   ampliada, 60 % del alto, rugiendo con el rasgo en primer plano. Fondo verde desenfocado. 2 palabras arriba que den
   contexto («PRIVATE ZOO!»). Título que pregunta, no afirma: «Modern day [criatura extinta]?!».
5. **Noticia con prueba** (#9, #6; 2,13 y 1,61). Presentador gritando de alegría a un lado, señalando con el índice; al
   otro, la prueba (cocodrilos bajando del remolque; el recinto ya acabado). Texto amarillo de 2–3 palabras, de
   acontecimiento: «BIG NEWS!», «MY DREAM EXHIBIT!». Título con cifra o con «DREAM»: «RESCUING 3 CROCODILES!».
6. **La que NO**: el **posado-catálogo** (#50, #51, #54, #17, #31; mediana 0,64): presentador gritando rodeado de bichos
   quietos, sin presa ni acción, título «World's MOST…», «NEW…», «FULL … TOUR!». Y el **manejo**: el presentador pequeño
   sujetando o arrastrando al animal, con texto largo de tarea (#48, #43, #45; 0,43–0,61).

### Las 6 mejores, una a una
1. **#25 · 3,43 · «Feeding My CRAZIEST ANIMALS!»** — Chandler (sombrero vaquero marrón, camiseta negra sin mangas, boca
   en O, ojos muy abiertos) en el centro, cabeza ~1/6 del alto, brazos en alto: carne cruda goteando en la izquierda,
   una pitón real en la derecha. Abajo izquierda, cocodrilo saltando del agua entre salpicaduras, boca abierta hacia la
   carne; abajo derecha, cobra alzada con la boca abierta hacia la pitón; arriba izquierda, búho real con las alas
   abiertas; arriba derecha, nutria con un pez en la boca. Fondo: recinto de valla y troncos, luz cálida de tarde, HDR.
   Texto arriba, dos líneas, ~25 % del alto: «FEEDING ALL OF MY / ZOO ANIMALS!», blanco con «ALL» y «ZOO» en amarillo de
   brocha, borde negro. Flecha roja curva desde la nutria hacia la pitón. Escena generada.
2. **#40 · 3,17 · «Modern day Saber-Toothed Tiger?!»** — Chandler real (rizos sueltos, sin sombrero, chaqueta de cuero
   marrón, riendo con dientes mientras mira al animal) a la izquierda, con un felino moteado de colmillos de sable en
   brazos. Derecha: la cabeza del mismo felino ampliada, ~60 % del alto, rugiendo con la boca de par en par y los
   colmillos amarillentos. Fondo de selva verde muy desenfocado. Texto «PRIVATE ZOO!» blanco con borde negro, ~13 % del
   alto, arriba al centro. Flecha roja recta y gruesa desde abajo hacia los colmillos. Felino inventado con IA.
3. **#22 · 3,12 · «Giant Hungry KING COBRAS!»** — Cobra real enorme en el centro-izquierda, cabeza más grande que el
   torso de Chandler, tragando una pitón amarilla y negra que cae en curva hasta el suelo; dos cobras alzadas a la
   izquierda (una con la boca abierta) y otra a la derecha; cuerpos enroscados por todo el suelo. Chandler real a la
   derecha, agachado, camiseta negra, sin sombrero, sonrisa tranquila, cabeza ~1/7 del alto. Fondo: serpentario oscuro
   con terrarios iluminados y un mural de serpiente. Luz de recorte dura, ambiente oscuro. Sin texto ni flecha.
4. **#11 · 2,94 · «King Cobras & Crocodile EAT Pythons!»** — Composición simétrica. Centro: Chandler (sombrero, camiseta
   negra sin mangas, guantes negros, grito) con una pitón albina amarilla en cada mano, por encima de los hombros.
   Izquierda: cobra real alta, cortada por el borde, mordiendo una pitón. Abajo a la derecha: cocodrilo con la boca
   abierta mordiendo la otra. Fondo de selva tropical luminosa. Flecha roja curva desde abajo hacia la boca de la
   cobra. Sin texto. Generada.
5. **#7 · 2,35 · «Crocodiles EAT Big Python!»** — Izquierda: Chandler (sombrero, camiseta negra mojada, brazos de
   culturista, tatuaje, grito) tirando con las dos manos de una pitón que cruza el cuadro en diagonal. Derecha: un
   cocodrilo enorme, con la cabeza ocupando ~50 % del cuadro, mordiendo el otro extremo; salpicaduras y barro. Fondo:
   valla y palmeras desenfocadas. Sin texto ni flecha. Generada.
6. **#36 · 2,32 · «Feeding My Venomous Snakes & Crocodiles!»** — Selfie de Chandler real (sin sombrero, sonrisa con ojos
   entornados) en el agua, con un trozo de carne cruda en la mano hacia cámara. Alrededor, recortes: dos cobras casi
   iguales con la boca abierta (izq.), nutria enseñando los dientes (delante), un cocodrilo en el agua con la boca
   abierta y el hocico de un gavial en primer plano (der.), búho real (arriba der.). Texto arriba en tres líneas:
   «FEEDING» amarillo, «ALL OF MY» blanco, «ANIMALS!» enorme en degradado rojo-naranja, todo con borde negro grueso, ~35 %
   del alto. Collage sin contornos.

## 9. Contraste con la guía (hecho al final)

Guía: `base/titulos-miniaturas.md`, apartados 1, 3, 5, 6 y 7. Análisis anterior: `base/refs/_youtube/canales/ChandlersWildLife.md`.

### Lo que este canal confirma
- **§1.2 Se deja fuera el desenlace.** Cuando el título intriga y la imagen ya lo resuelve, cae: #37 (el cocodrilo ya
  atravesó la valla) 0,77, #39 (ya se ve lo que venden) 0,52, #28 0,99; tipo E, mediana 0,77.
- **§1.4 y §5 «NEW», «You won't BELIEVE», superlativo sin prueba no suben.** NEW: 6 títulos, mediana 0,70 (máx. 1,27);
  «You won't BELIEVE…» #39 0,52; «RARE/RAREST» 3/3 ≤1,03; «World's MOST…» 0,64–0,96 salvo #20, que enseña la prueba.
- **§1.6 El tema pesa más que el diseño.** #32 (IA, cara, riendo) 1,34 y #16 (foto real, de espaldas, sin nada) 1,36 con el
  mismo título; los felinos (#47, #40) arriba con miniaturas de época antigua.
- **§3 TODO EN MAYÚSCULAS, no**: 5 títulos, mediana 0,77. **Longitud corta**: mediana 31 caracteres.
- **§6.1 Se entiende sin leer**: 49/54; 4 de los 6 mejores sin texto (#22, #11, #7, #14).
- **§6.4 La boca en «o» genérica es la que peor sale.** En la época IA, grito 24 casos, mediana 1,06 (adj 1,00), frente
  a sin grito 12 casos, mediana 1,35 (adj 1,28). La guía ya lo intuía («cuatro de las diez mejores rompen su boca
  abierta»); con la fecha ajustada, la diferencia es clara.
- **§6.5 El texto no sube por sí solo**: época IA con texto 1,03 (adj 1,01), sin texto 1,27 (adj 1,09).
- **§6.6 La etiqueta de precio como gancho no levanta**: #39 «FOR SALE!» 0,52.
- **§6.7 Flechas no suman**, y ajustando la fecha, más claro que en la guía: época IA con flecha 1,03 (adj 1,01), sin
  flecha 1,27 (adj 1,28); 7 flechas en los 10 peores, 4 en los 10 mejores.
- **§6.8 El objeto-prueba en la mano**: los cebos en las manos de #25 (3,43), el felino en brazos de #40 (3,17), las
  pitones de #11 (2,94).
- **§6.12 Varias cosas, con orden**: #25 (3,43) frente a #30 (0,99), confirmado; y lo mismo #36 (2,32) frente a los
  muestrarios planos #50, #51, #54 (0,58–0,78).

### Lo que contradice o matiza
1. **§1.3 «Se calla el final, nunca el sujeto; siluetas con «?» y cajas misterio apagan».** Aquí, **esconder de verdad
   funciona**: #35 silueta con ojos amarillos 1,84, #15 caja cerrada con un ojo 1,27 (adj 1,09), #23 cocodrilo bajo una
   sábana 1,03, #14 estanque turbio 2,21: 4/4 ≥1,03 y mediana 1,55. Lo que falla es la **falsa ocultación**: «?» junto
   a un animal que ya se ve (#42 0,64; #52 0,71, caja ABIERTA con la cobra fuera). Matiz para la regla: esconder apaga
   cuando es un producto («¿qué serpiente nueva?»); enciende cuando es el **culpable o el contenido de una historia con
   algo en juego** (una víctima, un «DANGER», la cara de pena del dueño). El análisis anterior metió #15 con #42 y #52 y
   concluyó «caja misterio: ninguna pasa de 1,27»; con la fecha ajustada, #15 está en la media y #35 entre las 10 mejores.
2. **§1.8 y §6.10 «Los escenarios fabricados quedan por debajo; la foto creíble gana».** Aquí no: 41/54 son escenas
   generadas o rehechas, y entre las mejores hay invenciones imposibles: un felino de dientes de sable que no existe
   (#40, 3,17), una cobra mayor que un hombre (#22, 3,12), Chandler en un tira y afloja que según la descripción fue
   entre dos cocodrilos (#7, 2,35). Real frente a IA con el mismo tema: empate (#16 1,36 / #32 1,34). Lo que el ratio no
   mide es el coste en confianza: los éxitos tienen la mitad de «me gusta» por visita (12–26 por mil frente a 45–69 en
   los flojos). Puede ser solo público nuevo, o algo de decepción; no lo puedo separar. La regla ética de la guía
   (no prometer lo que no sale) sigue valiendo como norma de la casa, pero no hay que justificarla con el ratio en
   canales de este tipo: aquí la exageración imposible rinde.
3. **§1 tabla «¿Qué le pasa?» y §6.4 «la expresión reacciona a la escena».** Las dos mejores sin grito hacen lo
   contrario: **infrarreaccionan**. Calma sonriente junto a una cobra gigante (#22, 3,12), risa con un felino imposible
   en brazos (#40, 3,17), sonrisa entre bocas abiertas (#36, 2,32). La incongruencia (está tranquilo, ¿por qué?) es el
   gancho. Reaccionar con el gesto «correcto» (susto ante el peligro) es justo el grito que menos rinde.
4. **§3 «Una sola idea. Si necesita "y", son dos títulos».** Los 2 títulos con «&» son altos: «King Cobras & Crocodile
   EAT Pythons!» 2,94, «Feeding My Venomous Snakes & Crocodiles!» 2,32. Cuando el «&» suma un segundo depredador a la
   misma escena, no son dos ideas: es una escalada.
5. **§3 «Títulos que no dicen nada sin la miniatura» (no).** Aquí, frases de historia sin animal y **sin exclamación**:
   «This Is Every Keeper's WORST Nightmare» 1,84, «What's in my Mystery Pond??» 2,21, «I Wasn't Expecting THIS Animal…»
   1,44. Funcionan cuando la miniatura lleva el contenido y guarda el secreto; fallan cuando la imagen lo resuelve
   (#37, #39). Los 5 títulos sin «!» tienen mediana 1,44 frente a ~0,99 de los 45 con «!»: el «!» final que la guía da
   por norma en animales (§5) no es lo que rinde aquí.
6. **§5 «Gerundio inicial para el vlog (Building, Feeding, Rescuing, Moving…)».** Separar: «Feeding» funciona (9,
   mediana 1,34), pero el **gerundio de faena** no: Catching, Training, Bringing, Earning, Searching, Saving, Building,
   Rescuing → 9 casos, mediana 0,75; solo se salvan «RESCUING 3 CROCODILES!» (2,13) y «Building my DREAM…» (1,61), que
   llevan cifra o sueño. Moving en miniatura (#48 «MOVING A HUGE ALLIGATOR…») 0,43.
7. **§5 molde «[PREDATORS] EAT [BIG PREY]!»**: hace falta el **plural**. Plural 3/3 altos (#22 3,12, #11 2,94, #7 2,35);
   singular 2/2 bajos (#18 «King Cobra EATS Huge Python!» 0,66, #4 «King Cobra Eats Python!» 0,54*).
8. **§6.2 «El creador diminuto en un plano general, lo peor»** y **§6.3 cabeza entre 1/4 y 40 %**: #22 tiene la cabeza a
   1/7 y es el tercero mejor, porque el creador pequeño y tranquilo da la escala del monstruo; #25 a 1/6, el mejor. Lo
   pequeño falla cuando además no pasa nada (#48 1/8, 0,43; #45 1/8, 0,61). El tamaño de la cabeza no separa en este canal.
9. **§6 plantilla D «Recinto lleno: creador en el centro, brazos abiertos, 8–15 animales enteros, sin texto»**. Aquí,
   tal cual, falla: #31 (brazos abiertos, 3 cocodrilos de frente) 0,55; los muestrarios de 5–7 serpientes (#5, #50, #51,
   #54) 0,58–1,1. Lo que funcionó (#25) tiene **4 animales, cada uno haciendo algo hacia el creador** (saltando a por
   el cebo que sostiene) y texto de 6 palabras. El número de animales no importa; importa que no estén quietos.
10. **§1.8 «Un animal que no está en el vídeo, nunca»**: el canal mete animales de adorno que el título no nombra (tigre en
   #2, #15, #26, #34; búho y nutria en muchas) sin castigo visible en el ratio (#34 1,44, #15 1,27, #26 1,2, #2 2,06*).
   No puedo comprobar si salen en el vídeo. Como en el punto 2, el ratio no lo castiga; la norma, si se mantiene, es
   por honestidad.
11. **§6.9 «Nada importante en la esquina inferior derecha»**: 3 de los 6 mejores tienen un animal clave ahí (cocodrilo
   de #11, cobra de #25, pitón de #22). No he podido comprobar si la marca de duración les tapa algo.

### Lo que la guía NO dice y aquí se ve (lo más importante), dicho como regla
1. **Texto de acontecimiento, sí; texto de tarea, no.** En la miniatura, la palabra que anuncia que algo ha pasado o
   está pasando («BIG NEWS!», «MYSTERY ANIMAL BROKE IN!», «EXTREMELY CLOSE CALL!», «NEW MYSTERY ANIMAL?!», «MY DREAM
   EXHIBIT!») rinde: 8 casos, mediana 1,46 (adj 1,26). El nombre de la faena que se ve («MICROCHIPPING A CROCODILE!»,
   «MOVING A HUGE ALLIGATOR TO MY FACILITY!», «CROCODILE ROUNDUP!», «FEEDING MY BULL GATOR!», «RAIDING A CROCODILE
   NEST!», «BIG CAT SANCTUARY») se hunde: 12 casos, mediana 0,76 (adj 0,80); solo se salva «FEEDING ALL OF MY…» (la
   promesa de totalidad). Regla: **el texto de la miniatura nunca describe la tarea; anuncia el suceso.**
2. **Cuando repites una escena que ya funcionó, multiplica.** La segunda o tercera vez que se enseña «cobra se come una
   pitón» solo funcionó al añadir comensales o escala (#22 cuatro cobras 3,12 → #11 cobra + cocodrilo 2,94); repetida tal
   cual, con una sola cobra, se hundió (#18 0,66 un mes después; #4 0,54*). Regla: **un motivo repetido necesita un
   depredador más, una escala mayor o un giro; nunca la misma imagen otra vez**, y el título, en plural.
3. **Infrarreacción: calma ante lo monstruoso.** Ver «contradice» 3. Regla: **si la escena ya da miedo o asombro por sí
   sola, la cara va tranquila o sonriente** (el contraste es el gancho); el grito solo cuando la imagen no tiene peligro
   propio... y ni así suma.
4. **Lo peor es el posado; lo mejor, el «durante».** Instante estático (el creador gritando entre animales quietos): 11
   casos, mediana 0,64 (adj 0,90). Durante (traga, tira, muerde): adj 1,22, 5 de los 6 mejores. Antes (cebo a un palmo):
   adj 1,07. Regla: **cada animal de la miniatura tiene que estar haciendo algo** (morder, saltar a por el cebo, tragar);
   un animal posando es decorado.
5. **Si escondes, esconde de verdad y pon algo en juego.** Ver «contradice» 1. Regla: **silueta o caja cerrada solo con
   una víctima o un peligro a la vista y la cara del creador con la emoción real; nunca un «?» encima de un animal que
   ya se ve.**
6. **El adjetivo al título, la lista a la miniatura.** En #25 el título promete un grado («CRAZIEST») y el texto de la
   imagen da la lista («FEEDING ALL OF MY ZOO ANIMALS!»): 3,43. En #30 el título ES la lista («FEEDING ALL MY ZOO
   ANIMALS!»): 0,99. Regla de reparto: **la palabra de grado o de juicio va en el título; el inventario, en la imagen.**
7. **La amenaza que nombra el título tiene que verse.** «CLOSE CALL» con el taipán en la mejilla (#20) 1,47 (adj 1,43);
   «CLOSE CALL» con un muestrario de serpientes (#5) 1,1 (adj 0,71). Los desencajes (título y miniatura de cosas
   distintas, 7 casos) tienen mediana 0,74. Regla: **si el título nombra un riesgo, la miniatura congela ese riesgo, no otro.**
8. **Cara real mejor que «personaje» generado.** Con miniaturas hechas con IA, las 7 de la época IA sin el uniforme
   (sin sombrero: cara real con el pelo suelto en #40, #22, #36, #35, #26, #12; de espaldas en #16) tienen mediana 1,84 frente a 1,03 de las
   29 con el Chandler de sombrero, piel HDR y brazos hinchados (n pequeño, pero 4 de ellas están entre las 10 mejores).
   La guía pide «do not beautify» en el prompt; aquí se ve el porqué en ratio. Regla: **que la IA no convierta al
   creador en un muñeco de acción; su cara real, con su gesto real.**
9. **Segundas partes, fiestas e invitados no tiran.** La continuación rinde menos (#28 0,99 → #27 0,76, que ya dice el
   desenlace: «SURGERY»); las fiestas (#44 Navidad 0,48, #49 Thanksgiving 0,75); el invitado (Tyler Nolan, adj ~1,1, ni
   sube ni baja). Regla: **la segunda parte se vende con un ángulo nuevo y sin contar en el título cómo acabó la
   primera; la fecha señalada no es gancho.**
10. **El «&» que escala** y **la frase de historia sin «!»** (ver «contradice» 4 y 5) como moldes en inglés:
    `[PREDATORS] & [OTHER PREDATOR] EAT [PREY]!` y `This Is Every [ROLE]'s WORST Nightmare` / `What's in my [PLACE]??`.
11. **Medir contra los vecinos en el tiempo.** En un canal que crece (aquí rho −0,49 entre antigüedad y ratio), comparar
    medianas brutas esconde efectos: el análisis anterior no vio diferencias por grito, sombrero o instante, y con el
    ratio ajustado por los 10 vecinos aparecen. Regla de método para `METODO.md`: **antes de comparar rasgos, divide el
    ratio por la mediana de sus vecinos, o compara solo dentro de una misma época.**
12. **Señal de público ajeno.** Los éxitos tienen la mitad de «me gusta» por visita (#11 12 por mil, #7 13, #22 19,
    frente a 45–69 de los flojos): el empaquetado los llevó fuera de los suscriptores. Regla para leer un test:
    **que la variante ganadora tenga menos «me gusta» por visita es lo esperable, no una alarma.**

### El análisis anterior: qué se le escapó, en qué se equivocó y qué sigue en pie
- **Sigue en pie**: la ficha; la tabla (salvo matices de clasificación); fauces abiertas en ~49/54; texto y flecha sin
  efecto positivo; la pareja #25/#30 (orden frente a amontonado); «añadir un segundo elemento al motivo repetido»
  (#22/#11/#7 frente a #18/#4); #16/#32 (manda el tema); visitas y logística abajo salvo felinos; #44 sin el creador;
  «NEW» flojo; y **#3 restringido por edad** (`needs_auth`), que yo había pasado por alto y que invalida la pareja
  #2/#3 como prueba de título: lo he corregido en mis apartados 1 y 7.
- **Se equivocó**:
  - **Caja misterio**: junta #15 (caja cerrada, 1,27, adj 1,09) con #42 y #52 (falsa ocultación) y concluye que esconder
    falla; pone #35 (silueta, 1,84) en otro grupo. Con eso alimentó la regla §1.3 de la guía, que aquí no se cumple.
  - **«La expresión no separa» (boca abierta 1,00 frente a 1,04)** y **«el sombrero no distingue»**: lo midió sobre el
    año entero, mezclando la época collage (ratios bajos, muchas sonrisas y sin sombrero) con la IA. Dentro de la época
    IA: grito adj 1,00 frente a 1,28; sin sombrero 1,84 frente a 1,03.
  - **#14 «responde la pregunta del título»**: la imagen enseña un charco turbio con cabezas asomando, no el inventario;
    la pregunta sigue viva («¿qué más hay?»).
  - Clasificación de realidad: llama collage a #40 y retoque a #12, #26, #53; a mi juicio #40 es un felino generado (no
    existe un animal así), aunque admito que no se puede comprobar.
- **Se le escapó**: el ajuste por fecha (lo avisa pero no lo hace); la función del texto (suceso frente a tarea); el
  plural del molde EAT y los títulos con «&»; los títulos sin «!»; el instante estático como el peor grupo; la
  infrarreacción como gancho; ocultación real frente a falsa; que la amenaza del título tenga que verse (#20/#5); el
  reparto adjetivo-título / lista-miniatura (#25 lleva en la imagen el título de #30); el gerundio de faena; la racha
  de julio (4 vídeos en 10 días) como explicación de #17, #18 y #19; las segundas partes; y la señal de los «me gusta»
  por visita.

## 10. Límites

- No he visto los vídeos: lo «inventado» se contrasta solo con la descripción, que en #40–#54 no tiene resumen. No puedo
  confirmar si el tigre de #2, #15, #26 y #34 sale en el vídeo ni qué animal real hay detrás del felino de #40.
- «Generada con IA» es lo que aparenta (piel HDR, anatomía imposible, clones); no hay forma de comprobar cómo se hizo
  cada una ni qué parte es foto real. Lo mismo para «cara real» frente a «cara generada» del creador.
- He abierto a tamaño completo 14 miniaturas (#25, #40, #22, #11, #7, #36, #48, #43, #44, #35, #18, #31, #16, #4); el
  resto, en las hojas de detalle (4 por hoja, bastante grandes) y de contacto. Tamaños de cabeza y % de texto, a ojo.
- El ratio no es CTR y está muy ligado a la fecha. El «adj» (ratio frente a sus 10 vecinos) corrige la tendencia, pero
  en los extremos del periodo usa menos vecinos, y con grupos de 3–12 casos todo son indicios, no estadística.
- #1–#4 tienen menos de 21 días; #3, además, está restringido por edad.
- Mi codificación (grito/no grito, instante, tipo de texto, encaje, mecanismo) es un juicio mío y otra persona podría
  clasificar algún caso al revés; los casos están citados para que se pueda revisar.
- Las miniaturas pueden haberse cambiado después de publicarse: lo analizado es la que había al descargar.
