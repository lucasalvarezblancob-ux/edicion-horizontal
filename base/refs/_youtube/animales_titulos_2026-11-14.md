# Títulos de animales, wildlife y aventura con animales — cruce del 2026-11-14

Por qué existe: Lucas notó que los títulos de vídeos de animales «se desviaban» frente a los demás. Se estudiaron cinco
canales nuevos con `ENCARGO_TITULOS_NICHO.md` (un agente por canal; el foco, el texto del título y cómo lo acompaña la
miniatura) y se cruzaron con los seis canales de animales que ya estaban (PC, CW, BW, FG, CC, BB). Las reglas que salen
están en `base/titulos-miniaturas.md` § 1 («Animales: qué se vende») y § 4–5.

| Canal | Abrev. | Idioma | Vídeos | Subs | Qué hace de verdad | Ojo |
|---|---|---|---|---|---|---|
| La Granja del Borrego | GB | es (Colombia) | 46 | 30,2 M | granja, cuidar fauna en parques, aventura | se apaga (mediana por semestre 5,3 M → 1,1 M) |
| Field Days en español | FD | es (latino neutro, **traducido** del inglés) | 64 | 694 k | supervivencia, pesca y caza para cocinar (Australia) | se apaga; títulos calcados del original |
| AntsCanada | AC | en | 86 | 7,1 M | recintos-ecosistema gigantes en casa, serie por temporadas | finales de temporada inflados |
| Wickens Wicked Reptiles | WW | en (EE. UU.) | 219 | 447 k | reptiles en cautividad: listas, guías, opinión | las guías («Care Guide 2025») viven de búsqueda |
| Jacob Feder | JF | en (EE. UU.) | 141 | 2,4 M | zoo en el patio de casa + rescates | se apaga; no es «field herping» |

Todos los ratios de abajo son **corregidos por época** (cada vídeo frente a la mediana de sus ~10 vecinos en el tiempo)
salvo que se diga. Informes completos: `canales/<canal>_titulos.md`; títulos: `datos/<canal>.tsv`; hojas: `hojas/<canal>.jpg`.

## 1. La desviación: qué hacía mal en los títulos de animales

Mirado contra los títulos propuestos hasta ahora (`1311`, los 10 de animales de `conceptos_r3.json` de Reino Selva):

1. **Gramática de viajero o de reto aplicada a animales.** «Me Di 1 Hora para Decorar un Estanque Entero», «Dormí 24h en
   la Jaula de un Lagarto Gigante», «Me Dejé una Barba de 10.000 Abejas»: el protagonista es la hazaña del creador con una
   condición inventada. En los canales de animales **el producto son los animales** (o la colección, o el recinto), y la
   hazaña del creador sin animal delante rinde por debajo: JF «I + verbo» 0,79 frente a «My [animal] + suceso» 1,58; WW
   sujeto «I/My» 0,72 frente a nominal 1,17 (20 de 49 por debajo de x0,6); WW «I Held a $50,000 Lizard!» x0,39, «Reptiles
   Made Me a Millionaire!» x0,44. En GB el «yo» rinde (1,08) **porque siempre va con un animal grande en un papel**
   («CUIDANDO LEONES RECIEN NACIDOS POR 1 DIA», «ENCONTRE EL OSO MÁS GRANDE DE LOS ANDES»).
2. **Animales pequeños, vagos o sin nombre fuerte de protagonistas.** «Un Pájaro Salvaje Estrenó Mi Estanque Nuevo»,
   «Mi Ajolote», «la Rana Más Pequeña del Mundo». Lo pequeño rinde menos en cuatro canales (AC invertebrados 0,87 frente a
   vertebrados 1,12, hormigas 0,76 en un canal que se llama AntsCanada; JF animales pequeños o comunes por debajo; GB rata
   0,44; FD truchas 0,38–0,54) y «pájaro» a secas hunde el mismo molde que con «oso» sube (GB #10 0,76 frente a #18 1,73).
3. **Títulos de un canal de animales sin animal.** «Intenté Salvar Plantas de una Tierra de Cemento»: obra o jardín sin
   destinatario. AC «Forming The Trees in My New Giant…» 0,49; JF obras 0,67; PC obras ~x0,90.
4. **Rareza como gancho.** «La Rana Más Pequeña del Mundo», «Huevo Gigante». La rareza o «nunca has oído hablar de…»
   rinde por debajo en tres canales (WW 0,81; GB misterio sin respuesta en la imagen 0,69; FG «Rarest» x0,35).
5. **Faltaban los moldes nativos del nicho**: meter un animal en el recinto, el nacimiento, el cuidador por un día, la
   ventana documental, la colección entera, la pérdida en la colección, el veredicto para quien quiere tener uno (§ 3).

**Y el exceso contrario** (visto al rehacer `1311` y `prueba-3` con estas reglas): meter un animal en todos los títulos.
En un vídeo de obra, el animal va en el título solo si sale y está en juego; si no, manda el gancho propio del vídeo
(«Me Di 1 Hora para Decorar un Estanque Entero» ganaba a «…el Estanque de Mis Peces»; «Intenté Salvar Plantas de una
Tierra de Cemento» ganaba a «El Recinto de Mis Tortugas se Ha Vuelto Cemento», con unas tortugas que no salen). Y el
título dice siempre de qué va el vídeo; el animal se suma a ese tema, no lo sustituye (Lucas: «si no, la persona va a
entrar y el vídeo no tiene nada que ver»).

Lo que ya iba bien y se queda: la paradoja con la propiedad del animal («The "Easy" Pet Tortoise That Keeps Dying»), el
animal de sujeto con una propiedad que se ve («Baby Snake-Necked Turtles Eat Like Piranhas»), el superlativo físico con
dueño («Africa's Most Endangered Tortoise Fits in One Hand»), el suceso en el recinto («Giant Tortoises' House Flooded…»).

## 2. Lo que se repite en varios canales

| Regla | Apoyo | Contraejemplo o matiz |
|---|---|---|
| **El animal que nombra el título sale en la miniatura, grande y haciendo algo** | AC 5/5 en las mejores frente a 0/6 en las peores (en tarrina o demasiado pequeño); GB, JF, WW y FD igual («DEEP-SEA MONSTERS» con un dorado, JF x0,22; trucha que no sale, FD 0,38) | — |
| **Nombra la especie si tiene nombre fuerte** (pitón, jaguar, oso, cocodrilo, hipopótamo, león) | AC «a PYTHON» 2,56 frente a «a Green Predator» 0,72, mismo molde y recinto; GB oso 1,73 frente a pájaro 0,76; AC aves 2/2 altas | la categoría vaga vale si la imagen la concreta (AC «Exotic Creatures» con la langosta, 0,98; JF «BLOOD SUCKING CREATURES» x9,26 con la garrapata de cerca); doble ocultación (título y foto), lo peor (AC #54 0,59) |
| **El animal pequeño se agranda en la imagen o no es el gancho** | AC araña y termita gigantes de montaje en las mejores (2,40, 2,03); a escala real, un escarabajo no se ve (0,40) | GB terror inventado (ojos rojos, nictibio-bruja) 0,77: agrandar sí, convertir en monstruo no |
| **Crías y nacimientos, el primer capítulo** | GB crías 1,72 (5 casos); JF «My AFRICAN WILDCAT is ABOUT TO GIVE BIRTH!!» x3,99, «…FINALLY GAVE BIRTH!!» x4,50, «I had MORE Newborn WILDCATS…» x4,82; AC «Baby Goat» 1,95 | los hitos de crianza siguientes vuelven a ~x1 (JF «Finally WALKING» x1,21) |
| **La colección entera vende más que un animal suelto** | JF recopilatorios de la colección 4,00 local (8 casos: «FEEDING MY EXOTIC ANIMALS !» x9,15, «I BUILT a ZOO In My BACKYARD… Now I'm Giving You the Full Tour!» x6,59); WW «Unboxing 80 Pet Reptiles» x6,86, «My FINAL Reptile Room Tour» x4,96; PC «ALL of My…» x4,6 | solo «mi» colección: el zoo ajeno cae (JF Cuba x0,32; AC visitas 0,42); una vez y con miniatura-catálogo ordenada |
| **La pérdida en la colección, dicha sin decir cuál** | JF «Saving My ZOO From FLOODING… We Lost Animals !» x6,20; WW «I Euthanized My Snakes. Heartbroken!» x9,24; AC «A Tragic Mass Extinction Has Happened…» 1,19; CW «My Wildlife Park Flooded…» x2,06 | la secuela cae (JF «The AFTERMATH of The FLOOD…» x0,97); el recuerdo con nombre propio y emoción entre paréntesis, no («My First Pet Snake Died, RIP Ekans (Emotional)» x0,52, misma miniatura que x9,24) |
| **Rescate: emoción en el título, víctima en la imagen; nunca el rescate resuelto** | JF «This Was the SADDEST RESCUE I've Ever Done…» x12,7 (sin nombrar el animal; madre herida con crías en la foto); GB rescate 1,35 | rescate como tema, mediana baja (JF 0,85); «How I Stopped…», «Here's How We Saved Him!», «Successfully» bajan (AC 0,76) |
| **El título no cuenta el final** | GB «NO PUDE ATRAPAR UN COCODRILO» 0,67, «(Salió Mal)»; JF «(we got stung)» x0,55; AC «How I Stopped…» 0,55, «I Successfully Grew…» 0,87 frente a «First in the World to…» 2,03 | «FINALLY» funciona cuando cierra una espera que el público siguió (JF 8 → 1,43) y la imagen pone el durante («SHE'S GIVING BIRTH!») |
| **Obra: solo con superlativo cierto o desproporción para un animal** | AC obra superlativa ≥1,7 en 6/6 («Building the Ultimate Lagoon…» 3,55, «The World's Largest Home Ecosystem Setup - 2 YRS Later» 3,85); GB «CONSTRUI UN ESTANQUE PARA MI EJERCITO DE RANAS» 2,11; JF «I BUILT a GIANT WATERSLIDE for My PET JAGUAR!» x3,06 | obra a secas o paso intermedio, por debajo (AC 0,49; JF 0,67; JF «…BIGGEST ANIMAL ENCLOSURES I've Ever Made» x0,39 con «ANIMAL» genérico) |
| **Palabras de fuera del nicho ganan a la jerga** | AC «Giant Indoor Lagoon Beach» 2,28 frente a «Giant Lagoon Ecosystem Vivarium» 1,14 dos semanas después; «Home Ecosystem Setup» en su mejor revisión | — |
| **Rutina y novedad sin consecuencia, abajo** | WW «Feeding», «Slept» 0,47; AC «UPDATE on…» 0,68; JF «Buying LIVE FISH…» x0,44 | «Feeding» de la colección entera con un depredador en contacto sí (JF) |
| **Repetir un éxito lo hunde** | JF garrapatas x9,26 → x0,31–0,55; huevos misteriosos x4,52 → x0,47–0,68; GB serie del Amazonas 2,34 → 0,36; FD lista de carencias gastada desde 2026 | ya estaba en la guía (§ 3, fórmula ganadora) |
| **Herramienta que no le pega a un animal grande: «cómo lo caza» > «cómo se lo come»** | FD «Pesqué un CANGREJO GIGANTE con solo un ARCO y una FLECHA» 5,67 frente a «CANGREJOS GIGANTES - ¡El Festín Definitivo…!» 0,64 (misma miniatura buena); arco 2,31 (5 casos) | un canal |
| **Cuidador por un día con un animal grande** | GB «CUIDANDO LEONES RECIEN NACIDOS POR 1 DIA (COMEN BORREGOS)» 2,95, «PASO 24 HORAS CUIDANDO ANIMALES SILVESTRES» 2,42, «CUIDANDO TIGRES POR 1 DIA!» 1,53 | un canal; repetido en 2026 se queda en ~1 |
| **Ventana documental: «Así Viven los [X] en [lugar con noticia]»** | GB «ASÍ VIVEN LOS HIPOPÓTAMOS EN COLOMBIA» 3,99 (el mejor del canal: sin «!», sin cifra, sin «yo»); M2 1,28 | con un lugar corriente (acuario) 0,87; el peligro lo pone la imagen (la boca abierta con la mano dentro) |
| **Veredicto para quien quiere tener uno** (canales de cría o de consejo) | WW superlativo de categoría amplia 16/28 ≥ x1,5; «Top 5 WORST Beginner Reptiles \| Get These Instead!» x4,02; «5 Reptiles You THINK You Want But Definitely DON'T!» x5,85 frente a su versión positiva x1,49; callar la alternativa x3,65 frente a nombrarla x0,79 | lo negativo no basta: «…That NEVER Bond…» x0,65 frente a «…That Bond…» x8,65 (gana lo que sirve a la decisión); el «YOU» que riñe 0,55; la categoría estrecha baja |
| **Consecuencia global sin decir cuál**, una vez | AC «I Connected My Three Giant Vivariums Together and It Changed Everything» x10,47 (final de temporada) | copiada en la siguiente, 1,07 |

## 3. Cómo acompaña la miniatura al título en animales

Los cinco informes dicen lo mismo con palabras distintas:

- **Reparto de papeles**: el título pone **el marco o la causa** (el plazo, el lugar, la regla, lo que ha metido en el
  recinto, la tragedia); la miniatura pone **el animal grande en el instante anterior a la consecuencia** o **el incidente
  que el título calla** (la jaula abierta con los pájaros dentro, el tanque vacío con él dentro para dar escala, la boca del
  hipopótamo con su mano dentro, el cachorro rugiendo y su brazo vendado, el pez enorme bajo «SIN COMIDA»). GB: 10/10 de las
  mejores añaden por los dos lados; 0/10 se repiten. AC: 6/10 mejores, la imagen trae lo que el título calla (tiburones,
  enjambre, araña gigante).
- **En las peores se dice lo mismo tres veces** (título, rótulo e imagen): GB 6/10, JF 5/10, WW 5/10. O se cuentan dos
  historias que no se tocan (WW «Your Reptile Room Will NEVER Be Finished» + «I FAILED»).
- **Si el título calla al animal**, la imagen lo resuelve tierno y de cerca (GB la cría de jaguar con chupete, 1,72), herido
  junto al creador afectado (JF x12,7), o medio escondido con ancla (GB la zarpa saliendo del transportín, 1,35).
- **Contradicción productiva** (polos opuestos, ya en la guía): FD título «SIN COMIDA, SIN AGUA, SIN FUEGO» y foto con
  pez y parrilla (x11). Improductiva cuando lo que falta es lo prometido (trucha que no sale).
- **El rótulo no decide**: AC con texto 0,98 frente a sin él 1,11 (mezclado con la época); JF ninguna diferencia; FD 0/10
  de las mejores lo llevan. Cuando el rótulo dice otra cosa que el título, puede sumar (JF «SHE'S GIVING BIRTH!» bajo
  «FINALLY GAVE BIRTH», x4,50; AC «FOR BABY SHARKS» que el título no nombra).
- **Lista que no se resuelve**: la miniatura enseña 1 de 5, nunca la respuesta obvia (WW la tortuga de 175 años bajo «5
  Reptiles That Live Forever», x0,38).

## 4. En español (lo que aportan los dos canales en español)

No hay en la muestra un canal de animales en español de España. GB es colombiano y FD es una traducción literal de un canal
australiano; de los dos sale qué moldes se pueden pasar y qué delata el origen:

- **Se trasladan**: «24 Horas Cuidando [ANIMAL GRANDE o CRÍAS] ([giro])», «Así Viven los [ANIMALES] en [LUGAR CON NOTICIA]»,
  «Encontré el [ANIMAL IMPONENTE] Más Grande de [REGIÓN]» (si es verdad), «¡Ha Roto el Huevo! (así nace el…)», «Construí un
  [OBRA] para Mi Ejército de [ANIMALES]» con la cifra en la imagen, la regla «Si No lo Pesco, No Como», la lista de carencias
  con lugar, «Cazo un [ANIMAL GRANDE] con [HERRAMIENTA QUE NO LE PEGA]».
- **España**: «¡» de apertura si hay «!»; tildes también en mayúsculas; **perfecto para lo que acaba de pasar en la colección**
  («Me Han Robado la Vaca», «Se Me Ha Escapado…», «Mi Sulcata Ha Puesto Huevos») e indefinido para la hazaña terminada
  («Construí», «Metí», «Encontré»); léxico de aquí: león marino (no lobo marino), cebo (no carnada), hoguera (no fogata),
  reto (no desafío), acampada (no camping), madre (no mamá), animales salvajes (no silvestres).
- **Delata la traducción**: el gerundio de titular («Atrapando y cocinando…»), «Atrapé y cociné» (*catch and cook*),
  «hambriento y sediento», «…y esto pasó», «(Crudo y sin editar)», «Viviendo de la tierra», «tanque de agua» por balsa,
  «vivario» o «ecosistema» como jerga (mejor «terrario», «estanque», «mi selva», «una selva en casa»).

## 5. Lo que este estudio no resuelve

- **Sujeto «yo» o animal**: JF y WW, el animal o lo nominal ganan; GB, el «yo» con papel gana al animal salvaje como sujeto
  de un suceso (0,79). Lectura: el animal **de la casa** con un suceso de su vida, sí; el animal salvaje que «me persiguió»,
  no; el «yo» solo funciona haciendo algo **con un animal grande**. Es una lectura, no un recuento.
- **Nombre común o genérico**: GB «animales» 1,28 frente a especie 0,87; WW «Reptiles» genérico, lo mejor; AC especie
  carismática, lo mejor. El genérico gana cuando promete **totalidad** («ANIMALES SALVAJES», «Every Reptile»); la especie,
  cuando es grande o peligrosa y la imagen la enseña.
- **Tres de los cinco canales se apagan** y uno vive en parte de búsqueda: todo va corregido por época, pero son indicios.
- **Sin canal de animales en español de España**: lo de § 4 es adaptación con dos canales de otra variante.
