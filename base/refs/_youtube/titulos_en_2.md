# Títulos en inglés, segunda tanda: ForrestGalante, colsonscritters, benmorris, BacktoBasics, biaheza

Base: los 223 títulos de `<canal>/titulos.tsv` (ForrestGalante 41, colsonscritters 45, benmorris 36, BacktoBasics 59,
biaheza 42), leídos todos y clasificados uno a uno. Recuentos con script (`.venv`, `-I`) y revisados a mano; los de
`resumen.json` no se han usado. `xN` = ratio dentro del canal; `*` = vídeo de menos de 21 días: cuenta en medidas y
moldes, **nunca** en medianas de ratio. Maduros: Forrest 39 (#1, #2 son `*`), colson 39 (#1–#6 son `*`), benmorris 36,
BacktoBasics 57 (#1, #2), biaheza 42. Miré las cinco `hojas/extremos.jpg` y, para una pareja de títulos idénticos,
`ForrestGalante/hojas/02.jpg`; el resto es solo texto.

Abreviaturas de canal: **FG** (Forrest Galante), **CC** (Colson's Critters), **BM** (Ben Morris), **BB** (Back to
Basics), **BZ** (biaheza). «Alto» = x1,5 o más; «bajo» = x0,6 o menos.

---

## 1. Medidas por canal

### Longitud

| Canal | Caracteres: mediana (rango) | Palabras: mediana (rango) | ≤30 | 31–40 | 41–50 | 51–60 | >60 |
|---|---|---|---|---|---|---|---|
| FG | 46 (31–79) | 8 (6–11) | 0 | 11 | 16 | 10 | 4 |
| CC | 49 (27–73) | 9 (4–13) | 1 | 5 | 19 | 16 | 4 |
| BM | 43 (34–59) | 8 (6–11) | 0 | 13 | 16 | 7 | 0 |
| BB | **55** (29–92) | 8 (5–12) | 1 | 4 | 17 | 24 | **13** |
| BZ | 37 (25–67) | 7 (4–11) | 2 | 29 | 7 | 3 | 1 |

- Palabras = piezas con alguna letra o cifra (`$10M`, `&` aparte). El más largo: `SURVIVAL CHALLENGE: Australia's Most
  Controversial Shipwreck (No Food, No Water, No Shelter)` (BB #45, 92 car.), que es además el ratio más alto de los 223
  (x14,91). El más corto: `The YouTube Hamster Wheel` (BZ #10, 25 car., x0,39).
- BB es el único canal que vive por encima de 55: 37 de 59 títulos pasan de 50. Le sobra el paréntesis aclaratorio
  (29 títulos) y la etiqueta de serie `🇵🇬[EP:N]` (8).
- BZ escribe corto desde siempre: 31 de 42 entre 25 y 40 caracteres.

### Mayúsculas

| Canal | Title Case limpio (0 palabras en mayúsculas) | Title Case + palabras EN MAYÚSCULAS | TODO MAYÚSCULAS | Frase normal |
|---|---|---|---|---|
| FG | **41** | 0 | 0 | 0 |
| CC | 5 (#3, #8, #21, #35, #40) | **36** (1 palabra: 7; 2: 5; 3: 7; 4: 9; 5: 7; 6: 1) | 4 (#10, #31, #43, #44) | 0 |
| BM | **36** | 0 | 0 | 0 |
| BB | 28 (+ 7 que solo llevan `EP`, `PNG`, `RAW & UNCUT` como sigla) | 24 reales (10 `SURVIVAL CHALLENGE`/`SURVIVAL`, 5 `GIANT`…) | 0 | 0 |
| BZ | 40 (las `EP.` de serie no cuentan) | 1 (`ZERO`, #8) | 0 | 1 (`Some books that are pretty good`, #27) |

- **FG y BM no gritan ni una palabra en 77 títulos** (BZ, una en 42); son, con BZ, los tres canales con más visitas de
  la tanda (medianas de 2,04 M, 630 k y 848 k; BB 480 k, CC 27 k). Title Case de periódico: `of`, `the`, `a`, `in`, `with`, `this`, `or` en minúscula (`Why No Bird, Fish
  or Mammal Will Cross this Invisible Line`, FG #5). BM no es constante (`the Town That Sells…` #4 / `the Town that
  Pays…` #10; `Nobody's Heard of` #5 / `Nobody’s Heard Of` #26).
- CC grita sustantivos y el verbo de compra: `FISH` 12, `INSANE` 7 (+ asteriscos), `BUYING` 6, `AQUARIUM` 5, `NEW` 5,
  `SALTWATER` 4, `EXOTIC` 4, `MYSTERY` 3, `STINGRAY` 3. Es la escuela de Paul Cuffaro (al que nombra en #44).
- BB grita la etiqueta de formato (`SURVIVAL CHALLENGE:`), el tamaño (`GIANT` 5, `RARE`, `ONE`) y los avisos de
  montaje (`THE MOVIE`, `UNCUT`, `RAW`).

### Signos

| Canal | `?` | `!` | `!!` (o más) | `…`/`...` | `( )` | `:` | ` – `/`—` | `&` | `*` | `\|` | `/` | coma |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FG | 1 (#20) | **0** | 0 | 0 | 3 (#12, #24, #35) | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| CC | 1 (#45) | 40 | 32 | 7 | 1 | 0 | 1 (` - `, #28) | 0 | 5 (`*INSANE*`, `**INSANE**`) | 0 | 0 | 4 |
| BM | 1 (#35) | **0** | 0 | 0 | 1 (#12) | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| BB | 1 (`!?`, #32) | 11 | 0 | 2 | **29** | **22** | 2 | **19** | 0 | 0 | 0 | 6 |
| BZ | 1 (`?!`, #34) | 1 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 1 (#42) | 1 (`$500/Day`) | 3 |

- Un canal de animales (FG) y uno de viajes (BM) con **cero exclamaciones** en 77 títulos. CC, en cambio, las pone en
  40 de 45 (y `!!` en 32): es estilo de casa, no del género «animales».
- Los dos puntos de BB son de dos tipos: etiqueta de formato delante (`SURVIVAL CHALLENGE:` ×9, `[EP:N]` ×8) y
  subtítulo (`Surviving Like Our Ancestors: 48hrs with the Hadza Tribe`, `30 Days Surviving The Pacific: THE MOVIE`).
- Paréntesis de BB (29): aclaración del contenido 13 (`(Living & Foraging for Food)`, `(Catch, Clean & Cook)`), aviso de
  montaje 6 (`(THE MOVIE!)`, `(FULL MOVIE)`, `(RAW & UNCUT)`, `(AFRICA UNCUT)`), episodio 3 (`(Ep1)`, `(ep2)`,
  `(Part 2)`), autenticidad o emoción 5 (`(Real Life Story!)` ×2, `(My honest thoughts)`, `(Anxious & Excited)`,
  `(Broken down & Need Food)`), privación 2 (`(No Food, No Water, No Shelter)`).

### Cifras, dinero, emojis, hashtags

| Canal | Con algún dígito | Con dinero | Emojis | Hashtags |
|---|---|---|---|---|
| FG | 23 (19 son el número de una lista: `5 …`, `6 …`) | 6: `$10M` ×2, `$1M`, `Billionaire’s` ×3 | 0 | 0 |
| CC | 11 | 2 (`$1,500`, `$15,000`) | 1 (`🦈`, #26) | 0 |
| BM | 6 | 7: `€1`, `£9.50`, `£100`, `$50,000`, `$15 Billion`, `$100 Billion Dollar`, `Billionaires` | 0 | 0 |
| BB | 29 (21 son días o semanas) | 1 (`Money Doesn't Matter`) | **12** (8 banderas `🇵🇬`, `⚡`, `🏝️`, `🛩️🔥`, `☠️`) | 0 |
| BZ | 12 | **18** (5 con `$`; `Millionaire` ×5, `Millions`, `Rich`, `Money` ×4, `Profit`, `Budget`) | 0 | 0 |

- **Abreviaturas de dinero**: FG escribe `$10M` y `$1M` (3 títulos, x0,91–2,53); BM, la palabra (`$15 Billion`, `$100
  Billion Dollar`, con `Dollar` redundante). BZ escribe todos los ceros (`$15,000`, `$50,000`).
- Moneda según país: BM (británico) usa `£` para lo suyo (`£9.50 Holiday`, `£100`), `€` para Italia (`Houses for €1`)
  y `$` para lo de fuera (`$50,000 to Move There`, `$100 Billion`).
- Hashtags: 0 de 223. Emojis: solo BB (ver apartado 10).

---

## 2. Moldes de título (lo más importante)

Cada título está en un solo molde (el de su estructura principal). Códigos por canal: F (Forrest), C (Colson), B (Ben),
K (Back to Basics), Z (biaheza). Mediana y recuentos, solo sobre maduros.

### Reparto

| Molde | n | maduros | mediana | altos | bajos |
|---|---|---|---|---|---|
| **F1** `Private Tour of [OWNER’S] [Secret / $N / Best] [PLACE]` (+ `Face to Face with…`, `Staying Overnight Inside…`) | 14 | 13 | **1,42** | 5 | **0** |
| **F2** Lista: `[N] [ADJ] Animals That [HECHO]` | 19 | 18 | **0,65** | 1 | **9** |
| **F3** Misterio científico: `Why [LEY IMPOSIBLE]` / `Scientists Found…` | 4 | 4 | 1,19 | 1 | 1 |
| F4 Récord animal: `The Deadliest Man Eater to Ever Exist (436 Kills)` | 1 | 1 | 1,33 | 0 | 0 |
| F5 Riesgo propio o reacción | 3 | 3 | 0,78 | 0 | 1 |
| **C1** `Buying / I Bought [ANIMAL] for My [Backyard / Saltwater] Tide Pool!!` | 12 | 11 | 0,79 | 2 | 1 |
| **C2** Feria: `BUYING Reptiles at [World’s Largest] Reptile Expo!!` / `Touring…` | 7 | 7 | **1,81** | 4 | 0 |
| C3 Visita: `Exploring PRIVATE Backyard FULL of EXOTIC ANIMALS!` / `Touring my DREAM AQUARIUM…` | 5 | 4 | **0,45** | 0 | 3 |
| C4 Obra con plazo: `I Built [THING] for [ANIMALS] in [N] Days!!` / `Building…` | 6 | 6 | 1,12 | 1 | 1 |
| C5 Sorpresa a otro creador: `SURPRISING [CREATOR] with [ANIMAL]!!` | 5 | 3 | 1,46 | 1 | 0 |
| C6 Caja misterio con precio: `I UNBOXED $[N] Worth of MYSTERY FISH!` | 3 | 3 | 1,21 | 1 | 1 |
| C7 Suceso o teaser: `My Pet SHARK ATE ALL My FISH!` / `NOT Doing THIS…` | 4 | 3 | 0,67 | 0 | 1 |
| C8 Otros | 3 | 2 | 0,73 | 0 | 1 |
| **B1** `I Visited the [World’s SUPERLATIVE] [PLACE]` | 11 | 11 | 0,99 | 2 | 3 |
| **B2** `[I Visited / Visiting] the [PLACE] [that / where] [HECHO INSÓLITO]` | 8 | 8 | **1,46** | 3 | 1 |
| B3 `…Nobody’s Heard of` / `…Nobody Talks About` | 2 | 2 | 0,36 | 0 | 2 |
| **B4** `I Took a Sleeper [Train / Bus] Across [REGION]` | 4 | 4 | **5,01** | **4** | 0 |
| **B5** `I Stayed [at/in] Cheapest vs Most Expensive Hotel in [PLACE]` | 3 | 3 | 1,84 | 2 | 0 |
| B6 `[$N Billion] [Failed / Fake] City` | 2 | 2 | 2,22 | 1 | 1 |
| B7 Con una persona (`Asking a Complete Stranger…`, `…with Prime Minister of UK`, `Living with Bajau People…`) | 3 | 3 | **0,21** | 0 | **3** |
| B8 Presupuesto mínimo (`£9.50 Holiday`, `for £100?`) | 2 | 2 | 0,60 | 0 | 1 |
| B9 Otros | 1 | 1 | 0,45 | 0 | 1 |
| **K1** `SURVIVAL CHALLENGE: [ESCENARIO DE PELÍCULA]` | 11 | 11 | **2,75** | **10** | **0** |
| **K2** `[N] Days [Living / Surviving / Camping] [with / in] [X] (aclaración)` | 21 | 19 | **0,74** | 4 | 6 |
| K3 Catch & cook / cazar para comer | 9 | 9 | 0,82 | 4 | 2 |
| K4 Supervivencia sin reto / forrajeo | 6 | 6 | 0,90 | 2 | 1 |
| K5 El lugar o el pueblo como gancho | 10 | 10 | 1,00 | 3 | 4 |
| K6 Familia / casa | 2 | 2 | 0,43 | 0 | 2 |
| Z1 `I Tried [SIDE HUSTLE] (for a Week)` | 8 | 8 | **0,65** | 2 | 4 |
| Z2 `I Tested [Every Budget of / Buy it For Life] [X]` | 2 | 2 | 1,86 | 1 | 0 |
| **Z3** `I Bought a [Crashed / Failed / Abandoned X] [to Make a Profit / and…]` | 4 | 4 | **2,73** | 2 | 0 |
| **Z4** `I [Built / Turned / Rebuilt] [X] [Into Y]` | 6 | 6 | **2,36** | 4 | 1 |
| Z5 Que otro trabaje por mí: `I Paid Fiverr to Day Trade for Me` | 3 | 3 | 1,89 | 2 | 0 |
| Z6 `I Spent 8 Hours [Using X]` | 2 | 2 | 2,25 | 2 | 0 |
| Z7 `Millionaire Starts From Scratch EP. N` | 5 | 5 | 0,69 | 1 | 1 |
| Z8 `How to…` / imperativo | 4 | 4 | 1,20 | 0 | 1 |
| Z9 Meta del canal (Q&A, especial, libros) | 4 | 4 | **0,33** | 0 | **4** |
| Z0 Otros | 4 | 4 | 0,93 | 0 | 0 |

Solo 11 títulos (5 %) quedan en «otros». Cada canal vive de 2–3 moldes: FG F1+F2 = 80 %; CC C1+C2+C4 = 56 %; BM B1+B2 =
53 %; BB K1+K2 = 54 %; BZ Z1+Z3+Z4 = 43 % (y cambia de molde con cada época).

### ForrestGalante

**F1 · `Private Tour of [OWNER’S] [Secret / $N / Best] [KIND OF PLACE]`** (14, con sus dos variantes).
- `Private Tour of an Indian Billionaire’s Secret Bird Sanctuary` (#13, x4,24) · `Face to Face with India’s Deadliest
  Animals (Private Tour)` (#35, x3,28) · `Private Tour of Florida's $1M Crocodile Facility` (#23, x2,53) · `Private Tour of
  Texas' $10M Backyard Zoo` (#8, x1,57) · `Staying Overnight Inside an Indian Billionaire’s Private Wildlife Rescue
  Center` (#33, x1,49) · `Private Tour of California's Wildest Beach Zoo` (#18, x0,69).
- Curiosidad: **acceso**. Dice de quién es (un milmillonario, un estado, «Forrest Galante’s Home Zoo») y qué tipo de
  sitio, y calla lo que hay dentro. La pregunta: «¿cómo es por dentro algo que yo no puedo visitar?». El hueco lo
  agranda un cualificador en el centro del título: `Secret` (4), `$10M`/`$1M` (3), `Billionaire’s` (3), `Best` (2),
  `Wildest`/`Craziest` (2). Promete cantidad de animales y lujo; se guarda la pieza estrella.
- Es el mejor molde del canal: 13 maduros, ninguno bajo, mediana x1,42.

**F2 · Lista: `[N] [ADJ] Animals That [HECHO]`** (19). Variantes: `… That Actually Exist` (4), `[N] Extinct Animals…` (7),
`[N] More…` (3), `[N] Terrifying…` (2), personal (`I Met 6 Extinct Animals in Real Life`, `3 Closest Calls I've Had With
Death`).
- `5 Animals That Have Only Been Seen Once` (#21, x3,43; mismo título en #32, x1,36) · `I Met 6 Extinct Animals in Real
  Life` (#27, x1,39) · `6 Deadly Sea Monsters That Actually Exist` (#41, x1,36) · `6 Extinct Animals Found in 2025`
  (#30, x1,29) · `5 Animals That Survived The Ice Age` (#9, x0,33) · `5 More Extinct Animals I Believe Could Still Be
  Alive` (#37, x0,27).
- Curiosidad: «¿cuáles son?». Promete un catálogo; se guarda los nombres. Funciona cuando la relativa del final es
  una paradoja (`Only Been Seen Once`, `Met … Extinct … in Real Life`, `Found` junto a `Extinct`); cae cuando es un
  adjetivo de emoción (`Terrifying`, `Mysterious`), una categoría (`of the Rarest Animals on Earth`) o un hecho que no
  sorprende (`Survived The Ice Age`). 9 de los 18 maduros son bajos.

**F3 · Misterio científico: `Why [LEY QUE PARECE IMPOSIBLE]` / `Scientists Found [X]`** (4).
- `Why No Bird, Fish or Mammal Will Cross this Invisible Line` (#5, x4,21) · `Scientists Found a Rainforest Frozen Under
  Antarctica` (#4, x1,27) · `Why Are Deep Sea Creatures Evolving Into Giants?` (#20, x1,11) · `Why Nature Always Kills
  Its Largest Animals First` (#16, x0,42).
- Curiosidad: **expectativa rota**: una regla de la naturaleza que contradice lo que el lector cree. `Why` sin signo de
  interrogación (2 de 3) suena a respuesta prometida, no a duda. Se guarda la explicación. Partido: va bien cuando la
  ley se puede ver (`this Invisible Line`) y mal cuando es abstracta (`Nature Always Kills…`).

**F4/F5** · `The Deadliest Man Eater to Ever Exist (436 Kills)` (#12, x1,33): récord con la cifra en paréntesis.
`The Closest Call I’ve Ever Had With Death` (#11, x0,78), `I Tried America’s Most Dangerous Wildlife Job` (#15, x0,78),
`Wildlife Expert Reacts To Terrifying Animal Encounters` (#25, x0,30). El riesgo en primera persona, que es lo mejor de
Brave Wilderness en la primera tanda, aquí queda en la media o por debajo.

### colsonscritters

**C1 · `[Buying / I Bought] [ADJ] [ANIMAL] for My [Backyard / Saltwater] Tide Pool!!`** (12).
- `Buying FISH for My NEW Freshwater STINGRAY Pond!!` (#14, x5,66) · `Buying FISH That WALK ON LAND For My Backyard Tide
  Pool!!` (#29, x2,44) · `I BOUGHT a SHARK for My Saltwater Tide Pool!!` (#34, x1,3) · `BUYING the World’s RAREST STINGRAY
  for my Backyard Tide Pool!!` (#41, x0,79) · `BUYING NEW FISH for My BACKYARD SALTWATER Tide Pool!!` (#17, x0,64) · `I
  Added the FIRST Fish to My Backyard Tide Pool!!` (#42, x0,6).
- Curiosidad: baja; es el capítulo de la semana («hoy entra esto en el estanque»). El hueco lo pone un rasgo del animal
  (`That WALK ON LAND`) o un sitio nuevo (`NEW … STINGRAY Pond`). Los 10 maduros que acaban en `Tide Pool` tienen
  mediana x0,78. Es el molde M12 de Paul Cuffaro copiado casi palabra por palabra, y rinde igual de plano.

**C2 · Feria: `BUYING Reptiles at [World’s Largest / This INSANE] Reptile [Expo / Show]!!`** (7).
- `BUYING Reptiles at World's Largest Reptile Expo!! **INSANE**` (#36, x7,11) · `BUYING Reptiles At This INSANE REPTILE
  SHOW!!` (#38, x3,65) · `Touring America's Largest Reptile EXPO!! *INSANE*` (#16, x2,9) · `TOURING THIS HUGE REPTILE
  EXPO!!! *INSANE*` (#43, x1,81) · `BUYING Reptiles at this INSANE REPTILE EXPO!!` (#24, x1,05) · `I Bought FISH at a LIVE
  AQUARIUM AUCTION…` (#7, x0,71) · `BUYING SEA CREATURES At This INSANE AQUARIUM SHOW!!` (#33, x0,68).
- Curiosidad: **escala y escaparate**. «¿Qué hay, cuánto cuesta y qué se lleva?». Promete cientos de animales con precio
  (las miniaturas llevan etiquetas `$1.2K`, `$800`). Con reptiles: 5 de 5 por encima de x1, mediana x2,9. Con peces o
  «sea creatures»: x0,68 y x0,71.

**C3 · Visita: `Exploring [PRIVATE Backyard / an INSANE ZOO] FULL of EXOTIC ANIMALS!!`** (5).
- `Exploring PRIVATE Backyard FULL of EXOTIC ANIMALS! **INSANE**` (#12, x0,88) · `The Secrets to My DAD'S 150G SALTWATER
  AQUARIUM!! - 10 YEAR OLD Reef Tank` (#28, x0,59) · `Exploring an INSANE ZOO Full of EXOTIC ANIMALS!!` (#19, x0,31) ·
  `Touring my DREAM AQUARIUM with OVER 5,000 SEA CREATURES!!` (#22, x0,28) · `I Entered a PRIVATE Alligator Facility…`
  (#4, x0,47*).
- Curiosidad: la misma que el M15 de Paul (acceso), pero sin dueño ni cifra: «un zoo», «un jardín privado». Es el peor
  molde del canal. #12 es, letra por letra, el `Exploring PRIVATE BackYard FULL of EXOTIC ANIMALS!!` que en Paul Cuffaro
  hizo x2,68.

**C4 · Obra con plazo: `I Built a [THING] for [ANIMALS] in [N] Days!!`** (6).
- `I Built a Tide Pool for Sea Creatures in 100 days!!` (#40, x5,8) · `I Built a Rainforest Ecosystem for Reptiles in 100
  Days!!` (#35, x1,31) · `Building a MUD BATH For My Pet WALKING FISH!!` (#27, x1,3) · `I Built a Tide Pool for Sea
  Creatures for 365 days!!` (#8, x0,95) · `I Rescued a RARE Freshwater STINGRAY and Built It a POND!!` (#18, x0,64) ·
  `Building a ENCLOSURE for My NEW PET!!` (#23, x0,26).
- Curiosidad: **transformación**: «¿cómo queda?». El plazo `in 100 Days` comprime un antes y un después en un vídeo. Se
  guarda el resultado (que la miniatura enseña: `DAY 100`).

**C5 · Sorpresa a otro creador: `SURPRISING [CREATOR] with [ANIMAL] for [HIS PLACE]!!`** (5).
- `I GAVE HIM 25 NEW ANIMALS!!` (#31, x2,5) · `SURPRISING FINATIC with DREAM FISH for 2,000G Aquarium!!` (#15, x1,46) ·
  `SURPRISING PAUL CUFFARO WITH SHARKS FOR HIS POND!!!` (#44, x1,46) · `I Secretly Stayed in Finatic’s Warehouse for 24
  HOURS…` (#6, x1,18*) · `I SURPRISED FINATIC with a MAN EATING FISH!!` (#5, x1,15*).
- Curiosidad: «¿cómo reacciona?». **Autoridad prestada**: el nombre de un creador más grande trae su público. Ninguno
  bajo (3 maduros). En #31 el nombre se calla (`HIM`) y lo pone la miniatura.

**C6 · Caja misterio con precio** (3): `I UNBOXED $15,000 Worth of EXOTIC MYSTERY FISH! + GIVEAWAY` (#11, x1,7) · `I WAS
SENT A $1,500 FISH MYSTERY BOX!! *INSANE*` (#10, x1,21) · `I BOUGHT a Live Fish MYSTERY BOX! (What’s Inside?)` (#45,
x0,36). Curiosidad: «¿qué toca?». Sube con la cifra (sin cifra x0,36, $1.500 x1,21, $15.000 + sorteo x1,7).

**C7 · Suceso o teaser** (4): `I Bought My Fish a Girlfriend… And It Might’ve Been a MISTAKE!` (#13, x1,07) · `My Pet
SHARK ATE ALL My FISH! 🦈 ...Sad` (#26, x0,67) · `NOT Doing THIS Almost Ruined My Tide Pool…` (#25, x0,51) · `The
Hardest Video I've Ever Had to Make…Goodbye Freckles` (#3, x0,52*). Curiosidad: «¿qué pasó?». Ninguno alto.

**C8 · Otros**: `Budget Walmart Aquarium Challenge!` (#21, x1,03), `FEEDING My FISH a SEAFOOD PLATTER!!` (#30, x0,44),
`CATCHING Sea Creatures for My BEACH AQUARIUM!` (#1, x0,11*).

### benmorris

**B1 · `I Visited the [World’s SUPERLATIVE] [PLACE]`** (11).
- `I Visited the World's Biggest City Nobody’s Heard Of` (#26, x3,47) · `I Visited the World’s Hottest City` (#31, x1,75)
  · `I Visited the Most Hated City in Europe` (#32, x1,46) · `I Visited the World’s Most Polluted City` (#28, x1,04) ·
  `I Visited the Strictest Country in the World` (#27, x0,75) · `I Visited the Rudest City in the World` (#20, x0,28) ·
  `I Visited the World's Emptiest Country` (#18, x0,17).
- Curiosidad: «¿cuál es y cómo es estar ahí?». El nombre del sitio se calla siempre (lo da la miniatura: torre Eiffel
  en #20). Promete un extremo; se guarda si es para tanto. Molde central y plano (mediana x0,99): depende del
  superlativo (apartado 5).

**B2 · `[I Visited / Visiting / I Investigated] the [Town / City / Island] [that / where] [HECHO INSÓLITO]`** (8).
- `Visiting the Town Where the Sun Doesn’t Set` (#29, x6,88) · `I Stayed in Hotels that Broke the Internet` (#3, x5,02) ·
  `Visiting the Town that’s Always Dark (No Sunlight)` (#12, x2,4) · `I Visited the Secret Island Where Billionaires
  Holiday` (#36, x1,48) · `I Investigated the Town that Pays You $50,000 to Move There` (#10, x1,43) · `I Investigated
  the Town That Sells Houses for €1` (#4, x1,0) · `I Visited the City that Hates Tourists` (#25, x0,47).
- Curiosidad: **expectativa rota** sin nombre propio: se calla el sitio y se dice su rasgo imposible. «¿Dónde está y
  cómo se vive así?». Es la misma regla que la guía tiene para el español («el País que te Paga por Visitarlo»), aquí en
  inglés y con recuento: mediana x1,46; con `Town`, 4 de 4 por encima de x1.

**B3 · `…Nobody’s Heard of` / `…Nobody Talks About`** (2): `The Side of Tokyo Nobody Talks About` (#19, x0,42) · `I
Visited Italy’s Secret Island Nobody’s Heard of` (#5, x0,3). Curiosidad: «¿qué es lo que nadie sabe?». Hueco puro sin
rasgo: no rinde.

**B4 · `I Took a Sleeper [Train / Bus] Across [REGION]`** (4): `I Took a Sleeper Train Across Europe` (#17, x6,67) · `I
Took a Sleeper Train Across the UK` (#7, x6,06) · `I Took a Sleeper Train Across Japan` (#1, x3,96) · `I Took a First Class
Sleeper Bus Across Europe` (#11, x3,68).
- Curiosidad: **«¿y si lo hiciera yo?»**. Es una experiencia que el espectador podría comprar: ¿cómo es dormir en
  un tren cruzando un continente?, ¿merece la pena? Sin adjetivo, sin cifra, sin mayúsculas, 35–46 caracteres. Promete
  la experiencia entera; se guarda el veredicto. 4 de 4 altos, mediana x5,01: el mejor molde de la tanda.

**B5 · `I Stayed [at / in] Cheapest vs Most Expensive Hotel in [PLACE]`** (3): `…in Bali` (#14, x3,46) · `…in the Alps`
(#8, x1,84) · `…in London` (#2, x1,19). Curiosidad: **contraste de precio sin cifras**: «¿cuánto cambia y cuál
compensa?». Se guarda el veredicto. Se come el artículo (`Cheapest vs Most Expensive Hotel`, sin `the`).

**B6 · Megaproyecto** (2): `I Visited a Failed $100 Billion Dollar Ghost City` (#34, x3,98) · `I Visited China’s $15
Billion Fake Cities` (#13, x0,46). Curiosidad: **pérdida a lo grande**: «¿cómo se tiran 100.000 millones?».

**B7 · Con una persona** (3): `I Went on Holiday with Prime Minister of UK` (#16, x0,36) · `Asking a Complete Stranger to Go
on Holiday` (#15, x0,21) · `Living with Bajau People for a Week` (#22, x0,19). Los tres bajos.

**B8 · Presupuesto mínimo** (2): `I Took the £9.50 Holiday No One Dares to Take` (#6, x0,66) · `How Many Countries Can I
Visit for £100?` (#35, x0,54). **B9**: `This Small Country is the Gambling Capital of the World` (#33, x0,45).

### BacktoBasics

**K1 · `SURVIVAL CHALLENGE: [ESCENARIO DE PELÍCULA]`** (9 con la etiqueta delante + 2 con `Survival Challenge` dentro).
- `SURVIVAL CHALLENGE: Australia's Most Controversial Shipwreck (No Food, No Water, No Shelter)` (#45, x14,91) ·
  `SURVIVAL CHALLENGE: Shipwrecked on Ancient Coastline` (#7, x4,73) · `SURVIVAL CHALLENGE: Castaway on Tropical Island`
  (#22, x4,06) · `SURVIVAL CHALLENGE: The Real Crocodile Dundee!` (#5, x3,77) · `SURVIVAL CHALLENGE: Plane Crash In
  Forbidden Jungle 🛩️🔥` (#41, x3,33) · `SURVIVAL CHALLENGE: Australia's Most Scandalous Shipwreck` (#42, x1,75) · `Nuclear
  Island Survival Challenge (GIANT LOBSTER!)` (#44, x1,0).
- Curiosidad: **amenaza + historia**: la etiqueta dice el género (reto de supervivencia) y lo de detrás de los dos
  puntos es un argumento de película: naufragio, náufrago, avioneta estrellada, el Cocodrilo Dundee de verdad. «¿Sale
  de esta?, ¿qué pasó allí?». Se guarda cómo aguanta. Los 9 con la etiqueta delante, **9 de 9 altos**, mediana x3,33.

**K2 · `[N] Days [Living / Surviving / Camping] [with / in / on] [X] (aclaración)`** (21).
- `10 Days Living with The Worlds Oldest Living Culture (Ep1)` (#54, x4,83) · `71 Days Surviving The Australian Outback (No
  Food, No Water, No Shelter)` (#48, x1,96) · `30 Days Camping & Spearfishing in Remote PNG` (#27, x1,87) · `3 Weeks
  Fishing, Camping & Cooking what we Catch with Dad` (#14, x1,83) · `14 Days Living with Vanuatu Island Hunters` (#6,
  x0,71) · `10 Days Living with Worlds Oldest Living Culture (The Movie)` (#13, x0,47) · `500miles in 7 Days (Australia's
  Wildest Coastline)` (#16, x0,29).
- Curiosidad: **inmersión**: «¿cómo se vive ahí tanto tiempo?». Es un diario; la cifra mide la duración, no lo que está
  en juego. Se guarda poco. Mediana x0,74, 6 bajos.

**K3 · Catch & cook / cazar para comer** (9): `We Caught & Ate Flying Fox on a Remote Island` (#10, x4,31) · `Kangaroo Catch &
Cook in Remote Australia (ep2)` (#53, x3,1) · `He Fed an Entire Village With ONE Giant Fish (Volcano Island)` (#9, x2,77) ·
`RARE GIANT CRAB Catch & Cook!` (#11, x2,5) · `GIANT TUNA CATCH & COOK (14 Days on Tropical Island)` (#33, x0,63) · `GIANT
CRAB HUNTING & Spearfishing to feed whole village` (#35, x0,49) · `Self Sufficient Living: Lobsters & Coconuts for
Christmas` (#55, x0,35). Curiosidad: «¿se come eso?» (**tabú**) o «¿cuánto da de sí?» (escala). Partido: 4 altos y 2
bajos.

**K4 · Supervivencia sin reto / forrajeo** (6): `Surviving from Foraged Bushfoods on Rugged Coastline` (#58, x3,62) · `FIND
FOOD ANYWHERE! (Foraging Remote Reefs & Coastline)` (#47, x2,59) · `Annual Solo Survival Trip (Anxious & Excited)` (#59,
x0,96) · `Surviving The Aussie Outback (THE MOVIE!)` (#15, x0,84) · `SURVIVAL IN WEST PAPUA (Broken down & Need Food)` (#17,
x0,71) · `Alone in the Australian Wilderness (My honest thoughts)` (#56, x0,35).

**K5 · El lugar o el pueblo como gancho** (10): `WHAT IS THIS PLACE!? (Fish Grill, Crocodile Lagoon & High on Jungle Seeds)`
(#32, x1,97) · `🇵🇬[EP:1] Welcome to the World’s Most Dangerous Paradise...` (#31, x1,65) · `🇵🇬[EP:3] Boat Leaking, Security
Hired, Fish Everywhere — PNG Unfiltered` (#29, x1,61) · `🇵🇬[EP:6] The Tropical Island Where Everyone Is HIGH` (#25, x1,22) ·
`The Islands Lost in Time (Living on Speared Fish & Coconuts)` (#38, x0,48) · `Head-Hunter Island (The Last Village of
Warriors)` (#34, x0,21).

**K6 · Familia / casa** (2): `The Trip of a Lifetime: Taking our Dad’s fishing in Remote Australia` (#43, x0,58) · `OUR NEW
HOME! (How We Power It⚡)` (#28, x0,29).

### biaheza (por épocas)

| Época | Vídeos (#) | Tema | Molde dominante | Mediana |
|---|---|---|---|---|
| 1 · nov 2019 – oct 2020 | 10 (#33–42) | dropshipping, «side hustles», day trading | `I Tried [X]`, `I Paid Fiverr to…` | 1,10 |
| 2 · dic 2020 – jul 2022 | 19 (#14–32) | bitcoin, bots, serie de millonario, Amazon | `I Tried Mining…`, `Millionaire Starts From Scratch EP. N`, imperativos (`Mine…`, `Turn $1 into…`) | 0,86 |
| 3 · sep 2022 – sep 2024 | 6 (#8–13) | negocio, el propio YouTube | `I Bought a Failed Business…`, `I Made a Secret Youtube Channel…` | 1,04 |
| 4 · nov 2024 – jun 2026 | 7 (#1–7) | coches, camper, producto | `I Bought a Crashed…`, `I Turned… Into…`, `I Tested Every…` | **2,91** |

Ojo: la mediana del canal se calcula con los 42 vídeos de siete años; si el canal ha crecido, lo reciente sale inflado
sin mérito del título. Comparo dentro de cada época siempre que puedo.

**Z1 · `I Tried [SIDE HUSTLE / MÉTODO] (for a Week)`** (8): `I Tried Forex Day Trading for a Week (Complete Beginner)`
(#39, x5,62) · `I Tried Mining Bitcoin For a Week` (#26, x1,74) · `I Tried the Sneaker Reselling Side Hustle` (#38, x1,16) ·
`I Tried Mining Bitcoin on my Phone` (#24, x0,9) · `I Tried the Instacart Side Hustle` (#36, x0,4) · `I Tried to Wheelie With
ZERO Experience` (#8, x0,38) · `I Tried Paying Fiverr to Feature me on Forbes` (#41, x0,36) · `I Tried Making Money With Sports
Cards` (#33, x0,24). Curiosidad: **«¿me serviría a mí?»**: el creador hace de conejillo de un método de ganar dinero.
Se guarda si funciona. Con `for a Week`: x1,74 y x5,62; sin plazo: 6 títulos, mediana x0,39.

**Z3 · `I Bought a [Crashed / Failed / Abandoned X] [to Make a Profit / and Turned it Around / and Made $____]`** (4): `I
Bought a Crashed Supercar to Make a Profit` (#7, x5,54) · `I Bought a Failed Business and Turned it Around` (#11, x4,46) ·
`I Bought an Abandoned Storage Unit and Made $________` (#18, x1,01) · `I Bought $15,000 Worth of Amazon Returns` (#17,
x0,86). Curiosidad: **dinero + transformación**: compra algo roto para sacarle beneficio. «¿Gana o pierde?», «¿cómo?».

**Z4 · `I [Built / Turned / Rebuilt / Made] [X] [Into Y]`** (6): `I Turned a Regular Car Into a Camper` (#5, x4,99) · `I
Rebuilt a Crashed Lamborghini in My Garage` (#6, x4,57) · `I Built a Camper and Got Attacked` (#4, x2,7) · `I Made a Secret
Youtube Channel to Prove it’s Not Luck` (#12, x2,02) · `I Created a Bitcoin Day Trading Bot` (#29, x0,69) · `Building a
$50,000 Crypto Mining Rig` (#20, x0,57). Curiosidad: «¿cómo queda?» y, en #4, «¿quién le ataca?».

**Z2, Z5, Z6** (precio, delegar, maratón): `I Tested Every Budget of Sports Car` (#1, x2,91) · `I Tested Buy it For Life
Products` (#3, x0,82) · `I Paid Fiverr to Day Trade for Me` (#37, x1,99) · `I Used a Bot to Day Trade for Me` (#35, x1,89) ·
`Day Trading Bot Doubled My Money?!` (#34, x1,05) · `I Spent 8 Hours Using Money Making Apps` (#40, x2,98) · `I Spent 8 Hours
Playing Games That Pay Real Money` (#23, x1,53).

**Z7 · `Millionaire Starts From Scratch EP. N`** (5): EP. 1 x1,5 → EP. 2 x0,88 → EP. 3 x0,69 → EP. 4 x0,66 → EP. 5
x0,45. Baja episodio a episodio, sin excepción.

**Z8 · Instrucción** (4): `Mine Bitcoin on a Cheap USB Stick` (#21, x1,38) · `Turn $1 into $5,000 With Binary Options
Trading` (#22, x1,31) · `How to Get Rich Without Getting Lucky` (#13, x1,08) · `How He Made Millions off Amazon at 17`
(#16, x0,37).

**Z9 · Meta del canal** (4, los cuatro bajos): `One Million Subscriber Special` (#19, x0,47) · `The YouTube Hamster Wheel`
(#10, x0,39) · `Some books that are pretty good` (#27, x0,27) · `Your Dropshipping (and Personal) Questions Answered |
Biaheza Q & A` (#42, x0,18).

**Z0 · Otros**: `My One Month Bitcoin Mining Journey` (#25, x1,23), `I Helped a Subscriber Start a Business` (#9, x0,99),
`Scamming a Pyramid Scheme for $500/Day` (#15, x0,86), `I Regret Buying My Rental Property` (#2, x0,65).

### Clasificación título a título
- **FG** — F1: 1, 3, 6, 8, 13, 18, 19, 23, 24, 26, 31, 33, 35, 38 · F2: 2, 7, 9, 10, 14, 17, 21, 22, 27, 28, 29, 30, 32,
  34, 36, 37, 39, 40, 41 · F3: 4, 5, 16, 20 · F4: 12 · F5: 11, 15, 25.
- **CC** — C1: 2, 9, 14, 17, 20, 29, 32, 34, 37, 39, 41, 42 · C2: 7, 16, 24, 33, 36, 38, 43 · C3: 4, 12, 19, 22, 28 · C4:
  8, 18, 23, 27, 35, 40 · C5: 5, 6, 15, 31, 44 · C6: 10, 11, 45 · C7: 3, 13, 25, 26 · C8: 1, 21, 30.
- **BM** — B1: 9, 18, 20, 21, 23, 24, 26, 27, 28, 31, 32 · B2: 3, 4, 10, 12, 25, 29, 30, 36 · B3: 5, 19 · B4: 1, 7, 11,
  17 · B5: 2, 8, 14 · B6: 13, 34 · B7: 15, 16, 22 · B8: 6, 35 · B9: 33.
- **BB** — K1: 5, 7, 18, 19, 22, 39, 41, 42, 44, 45, 49 · K2: 1, 2, 4, 6, 12, 13, 14, 16, 20, 21, 23, 26, 27, 30, 36, 37,
  46, 48, 52, 54, 57 · K3: 9, 10, 11, 33, 35, 40, 50, 53, 55 · K4: 15, 17, 47, 56, 58, 59 · K5: 3, 8, 24, 25, 29, 31, 32,
  34, 38, 51 · K6: 28, 43.
- **BZ** — Z1: 8, 24, 26, 33, 36, 38, 39, 41 · Z2: 1, 3 · Z3: 7, 11, 17, 18 · Z4: 4, 5, 6, 12, 20, 29 · Z5: 34, 35, 37 ·
  Z6: 23, 40 · Z7: 14, 28, 30, 31, 32 · Z8: 13, 16, 21, 22 · Z9: 10, 19, 27, 42 · Z0: 2, 9, 15, 25.

Casos frontera: FG #27 y #36 son listas en primera persona (van a F2, no a F5); BM #3 (`Hotels that Broke the
Internet`) va a B2 por su relativa, aunque empieza por `I Stayed`; BM #26 lleva superlativo y paradoja (va a B1); BB #48
lleva la privación de K1 dentro de un K2; BB #9 (`He Fed an Entire Village…`) va a K3 aunque su gancho es de escala.

---

## 3. Gramática y vocabulario

### Persona y tiempo

| Arranque | FG | CC | BM | BB | BZ | Total |
|---|---|---|---|---|---|---|
| `I` + pasado | 2 | 17 | **28** | 0 | **25** | 72 |
| `We` / `Our` / `He` + verbo | 0 | 0 | 0 | 5 | 0 | 5 |
| Gerundio sin sujeto (`Buying…`, `Visiting…`, `Surviving…`) | 1 | 23 | 5 | 5 | 2 | 36 |
| Número delante (`5 Animals…`, `30 Days…`) | 18 | 0 | 0 | 15 | 0 | 33 |
| Sintagma de acceso (`Private Tour of…`, `Face to Face with…`) | 13 | 0 | 0 | 0 | 0 | 13 |
| Etiqueta de formato o serie (`SURVIVAL CHALLENGE:`, `🇵🇬[EP:N]`, `Millionaire Starts…`) | 0 | 0 | 0 | 17 | 5 | 22 |
| `Why` / `How` (sin o con `?`) | 3 | 0 | 1 | 0 | 2 | 6 |
| Otro sintagma nominal, imperativo o titular en 3.ª persona | 4 | 5 | 2 | 17 | 8 | 36 |

- **La primera persona vuelve**: 72 de 223 títulos (32 %) empiezan por `I`, el doble que en la primera tanda (16 %).
  Son los dos canales de «experiencia propia»: BM (78 %) y BZ (60 %). FG, en cambio, casi nunca dice `I` (2 de 41):
  su voz es la de un presentador que enseña, no la de un protagonista.
- BB habla en plural porque son dos hermanos (`We Caught & Ate…`, `OUR NEW HOME!`, `with Dad`) y usa la tercera persona
  para un personaje (`He Fed an Entire Village…`, #9, x2,77).
- Tiempos: **pasado simple** para lo vivido (`I Visited`, `I Took`, `I Bought`, `I Built`); **gerundio** para la
  actividad (`Buying`, `Visiting`, `Surviving`, `Living`, `Staying Overnight`); **presente de titular** para la ley o
  el hecho (`Why Nature Always Kills…`, `Millionaire Starts From Scratch`, `Wildlife Expert Reacts…`, `the Town That
  Sells Houses`); **perfecto** para el récord (`Have Only Been Seen Once`, `I’ve Ever Had`, `I've Had`); **futuro** una
  vez (`Will Cross this Invisible Line`); **condicional** de duda dos veces (`Could Still Be Alive`, `It Might’ve Been a
  MISTAKE`).

### Verbos de arranque (con recuento)
- BM: `I Visited` 15, `I Took` 5, `I Stayed` 4, `Visiting` 3, `I Investigated` 2, `I Went` 1, `I Attempted` 1, `Asking`
  1, `Living` 1.
- BZ: `I Tried` 8, `I Bought` 4, `I Spent` 2, `I Tested` 2, `I Built`/`Turned`/`Rebuilt`/`Made`/`Created` 5, `I Paid` 1,
  `I Used` 1, `I Regret` 1, `I Helped` 1; imperativos `Mine`, `Turn`; gerundios `Scamming`, `Building`.
- CC: `Buying`/`BUYING` 12, `I Bought`/`I BOUGHT` 5, `I Built` 3, `Touring`/`TOURING` 3, `Exploring` 2, `SURPRISING` 2,
  `Building` 2, `I Rescued`, `I Added`, `I GAVE`, `I UNBOXED`, `I WAS SENT`, `I Entered`, `I Secretly Stayed`, `I
  SURPRISED`, `CATCHING`, `FEEDING`.
- BB: `SURVIVAL CHALLENGE:` 9, `[N] Days Living` 7, `[N] Days Surviving` 3, `[N] Days Camping` 4, `Surviving` 3 (como
  primera palabra), `We Caught`/`We Lived`/`We made` 3.
- FG: `Private Tour of` 11, `Face to Face with` 2, `Why` 3, `Staying Overnight Inside` 1, `Scientists Found` 1, `I
  Tried`, `I Met`.

### Superlativos y extremos (40 títulos)
- BM 14: `World's Biggest`, `World’s Hottest`, `World’s Most Polluted`, `World's Emptiest`, `World’s Most Dangerous Hike`;
  `the Most Isolated Island in Europe`, `the Most Expensive Country on Earth`, `the Most Hated City in Europe`, `the
  Most Dangerous City in the World`, `the Rudest City in the World`, `the Strictest Country in the World`; `Cheapest vs Most
  Expensive` ×3. Forma: `World’s X` (5) y `the X in the World / on Earth / in Europe` (6): conviven.
- FG 12: `Deadliest` ×3 (+ `Deadly` ×2), `Best` ×2, `Closest` ×2 (+ `Ever`), `Rarest`, `Wildest`, `Craziest`, `Most
  Dangerous`, `Largest`.
- BB 10: `Worlds Oldest Living Culture` ×3, `World’s Most Dangerous Paradise` ×2, `Australia's Most INSANE / Scandalous /
  Controversial`, `Wildest`, `Ultimate`.
- CC 4: `World's Largest`, `America's Largest`, `World’s RAREST`, `The Hardest Video I've Ever Had to Make`.
- BZ 0 (solo el totalizador `Every Budget`, y `ZERO Experience` como extremo por abajo).
- Superlativo con dueño-estado propio de FG: `America’s Best…`, `Florida's $1M…`, `Texas' $10M…`, `California's Wildest…`,
  `New York's Secret…`, `India’s Deadliest…`, `Brazil’s Deadliest…` (11 títulos con posesivo de lugar).

### Cifras: cómo se escriben
- **Dinero**: `$10M`, `$1M` (FG, abreviado y sin ceros: la primera tanda decía «nunca»), `$15 Billion`, `$100 Billion
  Dollar` (BM, con la palabra), `$50,000`, `$15,000`, `$1,500` (coma de millar), `£9.50`, `€1`, `$500/Day`, `$1 into
  $5,000`, `$________` (hueco dibujado, BZ #18, x1,01).
- **Tiempo**: `30 Days` (8 en BB), `14 Days` (5), `10 Days` (2), `3 Weeks`, `4 Weeks`, `71 Days`, `48hrs` (pegado),
  `in 100 days` / `in 100 Days` (CC, con las dos grafías), `for 365 days`, `24 HOURS`, `for a Week` (BZ ×2, BM ×1), `8
  Hours` (BZ ×2), `One Month`.
- **Cantidad**: listas de FG con `5` (11 de 19), `6` (4), `3`, `7`, `8`, `25`; `25 NEW ANIMALS`, `50 CLOWN FISH`, `OVER
  5,000 SEA CREATURES`; `(436 Kills)`.
- **Medidas**: `2,000G`, `150G` (galones, CC), `500miles`, `6000ft` (BB, sin espacio ni coma), `10 YEAR OLD`.
- Episodios, cinco grafías en dos canales: `[EP:8]`, `(Ep1)`, `(ep2)`, `ep3`, `EP. 5`, `(Part 2)`.

### Artículos y palabras que se comen
- Artículo: `I Stayed at Cheapest vs Most Expensive Hotel in Bali` (BM ×3), `I Went on Holiday with Prime Minister of UK`
  (BM #16: falta `the` dos veces y suena a no nativo), `SURVIVAL CHALLENGE: Castaway on Tropical Island`, `Shipwrecked on
  Ancient Coastline`, `to feed whole village` (BB), `Exploring PRIVATE Backyard FULL of…` (CC).
- Apóstrofo: `Worlds Oldest Living Culture` (BB #13, #54) y `the Worlds Most Dangerous Paradise` (#26) frente a `World’s`
  en #31 y #52. `Building a ENCLOSURE` (CC #23) es una errata.
- FG conserva los artículos casi siempre (`Private Tour of an Indian Billionaire’s…`, `The Deadliest Man Eater…`): su
  registro es de documental, no de pie de foto.

### Nombres propios
- Lugares como dueño o escenario: FG `India`/`Indian` ×4, `Florida` ×2, `California` ×2, `America` ×2, `Texas`, `New
  York`, `Brazil`, `Antarctica`; BM `Europe` ×4, `UK` ×2, `Japan`, `London`, `Alps`, `Bali`, `Italy`, `China`, `Tokyo`;
  BB `Australia(n)` ×8 + `Aussie`, `Pacific` ×2, `Vanuatu` ×2, `West Papua` ×2, `PNG`/`Papua New Guinea` ×9 con las
  banderas, `Tanzania`, `Africa`.
- Pueblos: `Hadza`, `Maasai`, `Bajau`, `Aboriginal`, `Worlds Oldest Living Culture` (sin nombrarla).
- Marcas: BZ `Lamborghini`, `Fiverr` ×2, `Forbes`, `Amazon` ×2, `Instacart`, `Bitcoin` ×5, `Forex`, `YouTube` ×2; CC
  `Walmart`.
- Personas: CC `FINATIC` ×3 (+ `Finatic’s`), `PAUL CUFFARO`, `Freckles` (su mascota); FG `Forrest Galante’s` (él mismo);
  BB `Crocodile Dundee` (personaje de cine).

### Palabras que más se repiten (en todos los títulos)
(títulos que contienen la palabra, sin distinguir mayúsculas)
- FG: `Animals` 18, `Private` 14, `Tour` 13, `Extinct` 8, `Exist` 5, `Secret` 4, `Sea` 4, `Deadliest` 3, `Billionaire’s` 3.
- CC: `My` 24, `for` 20, `FISH`/`Fish` 18, `Tide Pool` 14, `INSANE` 9, `Saltwater` 8, `Backyard` 7, `AQUARIUM` 7,
  `Reptile(s)` 6, `NEW` 6, `MYSTERY` 4, `EXOTIC` 4.
- BM: `I` 31 (también dentro: `Can I Visit`), `Visited` 15, `World` 9, `Most` 9, `City` 8, `Island` 4, `Town` 4,
  `Holiday` 4, `Europe` 4, `Sleeper` 4, `Across` 4.
- BB: `Days` 19, `Island(s)` 13, `Survival`/`Surviving` 13, `Remote` 12, `Living` 12, `EP`/`ep` 11, `Australia(n)` 10,
  `Food` 9, `Catch` 6, `GIANT` 6, `Spearfishing` 5, `Tropical` 5, `Coastline` 4, `MOVIE` 4.
- BZ: `I` 26, `Tried` 8, `Bitcoin` 5, `Millionaire Starts From Scratch EP.` 5, `Money` 4, `Trading` 4, `Mining` 4, `Bought`
  4, `Bot` 3, `Day Trade` 2.

---

## 4. Psicología

### Palancas por canal (recuento por título; un título puede tirar de varias)

| Palanca | FG (41) | CC (45) | BM (36) | BB (59) | BZ (42) |
|---|---|---|---|---|---|
| Acceso a lo vedado (`Private`, `Secret`, `Inside`, `Billionaire’s`, `Forbidden`) | **14** | 3 | 2 | 1 | 1 |
| Riesgo, muerte o amenaza (`Deadliest`, `Terrifying`, `Death`, `Shipwreck`, `Plane Crash`, `Attacked`) | 12 | 2 | 3 | **18** | 1 |
| Rareza o paradoja natural (`Only Been Seen Once`, `Invisible Line`, `WALK ON LAND`, `Sun Doesn’t Set`) | ≈10 | 3 | 6 | 4 | 0 |
| Extinción o pérdida (`Extinct`, `Failed`, `Ghost`, `Regret`, `Goodbye`, `MISTAKE`) | 9 | 3 | 2 | 0 | 2 |
| Dinero (cifra o palabra) | 6 | 3 | 7 | 1 | **18** |
| Récord o superlativo | 12 | 4 | **14** | 10 | 0 |
| Plazo o duración (`in 100 Days`, `30 Days`, `for a Week`, `Overnight`) | 1 | 4 | 1 | **23** | 4 |
| Transformación (`Built`, `Turned… Into`, `Rebuilt`) | 0 | 6 | 0 | 0 | 6 |
| «Podría ser yo» (`Complete Beginner`, `ZERO Experience`, `Regular Car`, `for Me`, `Money Making Apps`, `Sleeper Train`) | 0 | 1 | 6 | 0 | **10** |
| Contraste de precio (`Cheapest vs Most Expensive`, `Every Budget`) | 0 | 0 | 3 | 0 | 1 |
| Autoridad o invitado (`Scientists`, `Wildlife Expert`, otro creador, `Prime Minister`) | 2 | 4 | 1 | 0 | 0 |
| Hueco explícito (`THIS`, `MYSTERY`, `What’s Inside?`, `…`, `$____`, `HIM`) | 1 | **12** | 0 | 3 | 1 |
| Pertenencia (`My`, `Our`, mascota con nombre, `Dad`, el canal) | 1 | **23** | 0 | 4 | 5 |
| Serie o recopilación (`EP`, `Part 2`, `THE MOVIE`, `More`) | 3 | 0 | 0 | **16** | 5 |
| Pregunta con `?` | 1 | 1 | 1 | 1 | 1 |

Recuento a mano. Las filas de rareza, «podría ser yo», hueco y pertenencia tienen casos frontera (±2).

**La palanca dominante de cada canal:**
- **FG = acceso + rareza.** 16 títulos con acceso; la otra mitad del canal son listas de rarezas. El presentador es la
  llave: entra donde tú no entras (`Private Tour`, `Staying Overnight Inside`) o te enseña lo que nadie ha visto (`Only
  Been Seen Once`).
- **CC = pertenencia + escaparate.** `My` en 23 de 45. Igual que Paul Cuffaro, vende el capítulo de «mi estanque». Sus
  picos son salir de casa (feria de reptiles) o una obra con plazo.
- **BM = expectativa rota sobre un sitio.** El sitio nunca se nombra; se dice su récord o su rareza. El pico absoluto es
  otra cosa: una experiencia comprable (`Sleeper Train`).
- **BB = amenaza + argumento de película.** `SURVIVAL CHALLENGE:` + naufragio/náufrago/avioneta. El resto del canal,
  la duración (`30 Days…`), es su suelo.
- **BZ = dinero + «¿me serviría a mí?».** 18 títulos con dinero; el creador prueba métodos para que el espectador no
  tenga que hacerlo. En la última época cambia a **transformación con dinero en juego** (coche roto → beneficio).

### Mecanismo psicológico dominante de cada título (los 223, uno por título; medianas sobre maduros)

| Mecanismo | n maduros | Mediana | Altos | Bajos | Dónde | Ejemplo |
|---|---|---|---|---|---|---|
| Amenaza o peligro (sobrevivir, morir, animal letal) | 23 | **1,65** | 12 | 5 | FG 8, BB 15 | `SURVIVAL CHALLENGE: Castaway on Tropical Island` (BB #22, x4,06) |
| «Podría ser yo» (experiencia o método al alcance del que mira) | 18 | **1,64** | 10 | 4 | BM 4, BZ 14 | `I Took a Sleeper Train Across Europe` (BM #17, x6,67) |
| Autoridad prestada (otro creador) | 3 | 1,46 | 1 | 0 | CC 3 | `I GAVE HIM 25 NEW ANIMALS!!` (CC #31, x2,5) |
| Expectativa rota (paradoja, ley imposible) | 13 | 1,43 | 5 | 2 | FG 4, BM 9 | `Visiting the Town Where the Sun Doesn’t Set` (BM #29, x6,88) |
| Escala o escaparate | 6 | 1,43 | 3 | 0 | CC 5, BB 1 | `He Fed an Entire Village With ONE Giant Fish` (BB #9, x2,77) |
| Transformación | 13 | 1,31 | 6 | 2 | CC 6, BZ 7 | `I Turned a Regular Car Into a Camper` (BZ #5, x4,99) |
| Autoridad (instrucción, tesis) | 5 | 1,31 | 1 | 1 | BZ 5 | `I Made a Secret Youtube Channel to Prove it’s Not Luck` (BZ #12, x2,02) |
| Acceso a lo vedado | 18 | 1,25 | 5 | 3 | FG 14, CC 4 | `Private Tour of an Indian Billionaire’s Secret Bird Sanctuary` (FG #13, x4,24) |
| Dinero o contraste de precio | 9 | 1,03 | 3 | 1 | BM 5, BZ 3, CC 1 | `I Stayed at Cheapest vs Most Expensive Hotel in Bali` (BM #14, x3,46) |
| Récord o extremo (sin paradoja) | 15 | 0,99 | 3 | 4 | BM 11, CC 3, FG 1 | `I Visited the World’s Hottest City` (BM #31, x1,75) |
| Hueco con dinero (caja misterio, trastero) | 6 | 0,94 | 1 | 1 | CC 4, BZ 2 | `I UNBOXED $15,000 Worth of EXOTIC MYSTERY FISH!` (CC #11, x1,7) |
| Tabú o rareza alimentaria | 8 | 0,81 | 3 | 2 | BB 8 | `We Caught & Ate Flying Fox on a Remote Island` (BB #10, x4,31) |
| Inmersión (vivir N días con / en) | 14 | 0,79 | 3 | 4 | BB 14 | `14 Days Living with Vanuatu Island Hunters` (BB #6, x0,71) |
| Serie, episodio o recopilación | 10 | 0,76 | 1 | 2 | BB 5, BZ 5 | `30 Days Surviving The Pacific: THE MOVIE` (BB #4, x0,63) |
| Pérdida (extinción, error, arrepentimiento) | 13 | 0,65 | 1 | 6 | FG 7, CC 3, BM 2, BZ 1 | `5 More Extinct Animals Found in the Last 15 Years` (FG #10, x0,48) |
| Rareza genérica (categoría: «rarest», «mythical», «lost in time») | 12 | 0,64 | 2 | 6 | FG 5, BB 6, CC 1 | `5 of the Rarest Animals on Earth` (FG #40, x0,35) |
| Pertenencia (mi sitio, mi familia, el canal) | 14 | 0,62 | 1 | 7 | CC 8, BB 2, BZ 4 | `BUYING NEW FISH for My BACKYARD SALTWATER Tide Pool!!` (CC #17, x0,64) |
| Hueco puro («nadie sabe») | 3 | 0,42 | 1 | 2 | BM 2, BB 1 | `The Side of Tokyo Nobody Talks About` (BM #19, x0,42) |
| Gente desconocida | 3 | **0,21** | 0 | 3 | BM 3 | `Asking a Complete Stranger to Go on Holiday` (BM #15, x0,21) |

(Faltan en la tabla 4 de autosuficiencia de BB, mediana 1,77, y 3 sueltos.) La asignación es mía y es una por título;
mezcla canales con públicos distintos, así que vale como orden de magnitud, no como ley. Aun así el orden es claro:
**amenaza, «podría ser yo» y expectativa rota arriba; pertenencia, rareza de categoría, pérdida y gente desconocida
abajo.** La rareza solo sube cuando es concreta y paradójica (está entonces en «expectativa rota»).

### Qué deja SIEMPRE sin decir el título, y cómo
1. **El nombre del sitio** (BM, 36 de 36): ni un título dice la ciudad o el pueblo; se dice su rasgo (`the Town Where the
   Sun Doesn’t Set`, `the City that Hates Tourists`) o su récord (`World’s Hottest City`). La miniatura lo delata a veces
   (torre Eiffel en #20, Big Ben en #7). FG nombra el estado o el país, nunca al dueño; BB nombra la región, nunca el
   barco del naufragio.
2. **El veredicto** de la experiencia (BM `Sleeper Train`, `Cheapest vs Most Expensive`, `Hotels that Broke the Internet`):
   ¿merece la pena?
3. **Los nombres de la lista** (FG F2): se da el número y la propiedad (`Only Been Seen Once`), nunca un animal.
4. **El resultado económico** (BZ): `to Make a Profit` es la meta, no el resultado; `Made $________` dibuja la casilla vacía.
5. **Si sale vivo** (BB K1): la etiqueta y el escenario, nunca cómo acaba.

**Lo que SÍ se adelanta**, y no le va mal:
- El éxito: `I Bought a Failed Business and Turned it Around` (BZ #11, x4,46). La pregunta pasa a ser «¿cómo?», que en un
  canal de negocios es justo lo que se viene a aprender.
- El fracaso de otros: `a Failed $100 Billion Dollar Ghost City` (BM #34, x3,98).
- El incidente: `I Built a Camper and Got Attacked` (BZ #4, x2,7) dice que hubo ataque y calla quién y por qué.
- Los que adelantan un resultado personal flojo quedan en la media o debajo: `Day Trading Bot Doubled My Money?!` (x1,05),
  `I Regret Buying My Rental Property` (x0,65), `I Bought My Fish a Girlfriend… And It Might’ve Been a MISTAKE!` (x1,07).

---

## 5. Qué rinde y qué no (dentro de cada canal)

Todo son indicios: en el ratio van mezclados título, miniatura, tema, fecha y empuje del algoritmo. Las medianas por
molde están en el reparto del apartado 2; aquí van las palabras, los extremos analizados palabra a palabra y las
parejas. «p. N/M» = la palabra-gatillo es la N de un título de M palabras.

### Edad del vídeo, antes de comparar

| Canal | Mitad antigua (mediana) | Mitad reciente (mediana) | Longitud por terciles (corto / medio / largo) |
|---|---|---|---|
| FG | 1,23 | 0,86 | 0,78 / 0,78 / **1,27** |
| CC | **1,30** | 0,82 | 1,05 / 0,76 / 1,00 |
| BM | 0,92 | **1,31** | 0,95 / 0,71 / **1,66** |
| BB | 0,94 | **1,22** | 0,87 / 1,22 / **1,61** |
| BZ | por épocas: 1,10 / 0,86 / 1,04 / **2,91** | | 0,98 / 0,77 / **1,42** |

- La edad empuja en sentidos distintos según el canal: lo viejo sale mejor en FG y CC, lo nuevo en BM, BB y sobre todo
  BZ (época 4). Por eso comparo moldes que conviven en el tiempo: en FG, dentro de la mitad reciente (#3–#22), los `Private Tour`
  siguen en x1,21 de mediana (6) y las listas en x0,54 (7); en CC las ferias de reptiles están repartidas entre
  diciembre de 2025 y julio de 2026; en BB los `SURVIVAL CHALLENGE` van de junio de 2025 a julio de 2026.
- **Los títulos largos no van peor en ningún canal**; en cuatro de cinco, el tercil largo es el mejor. Pero lo largo
  coincide con los moldes buenos (`Staying Overnight Inside an Indian Billionaire’s…`, `SURVIVAL CHALLENGE: …`), así que
  no prueba que alargar ayude: prueba que no castiga.

### Palabras que acompañan a los ratios altos y a los bajos (maduros; n = títulos que la llevan)

| Canal | Con ratio alto (n · mediana · altos/bajos) | Con ratio bajo (n · mediana · altos/bajos) | Otra explicación |
|---|---|---|---|
| FG | `India/Indian` 4 · **2,38** · 2/0; `Deadliest` 3 · 1,99 · 2/0; `Billionaire’s` 3 · 1,49 · 1/0; `$10M`/`$1M` 3 · 1,57 · 2/0; `Private` 13 · 1,42 · 5/0; `Tour` 12 · 1,35 · 5/0 | `Terrifying` 3 · **0,41** · 0/3; `More` 3 · **0,48** · 0/3; `Animals` 17 · 0,74 · 3/8; `That` 8 · 0,72 · 1/3; `Exist` 5 · 0,74; `Extinct` 7 · 0,82 · 0/3 | `Animals`, `That`, `More`, `Terrifying` son marcas del molde lista; `India` puede ser un sitio concreto que interesa (la primera tanda tenía `Private Tour of India’s MOST SECRET AQUARIUM!!`, x3,63, en Paul Cuffaro) |
| CC | `Reptile` 5 · **2,9** · 4/0; `Expo` 4 · 2,35 · 3/0; `Touring` 3 · 1,81; `Days` 3 · 1,31; `INSANE` 9 · 1,21 · 4/1 | `my` 19 · **0,73** · 2/6; `Aquarium` 6 · 0,70 · 0/2; `Backyard` 7 · 0,73; `Saltwater` 7 · 0,76; `Tide Pool` 13 · 0,79; `Bought` 6 · 0,74; `Pet` 3 · 0,67 | `INSANE` sube porque va con las ferias (sin ellas: x0,88 y x1,21); `my`/`Tide Pool` son la rutina de casa |
| BM | `Sleeper` 4 · **5,01** · 4/0; `Took` 5 · 3,96 · 4/0; `Stayed` 4 · 2,65 · 3/0; `Visiting` 3 · 2,4 · 2/0; `Town` 4 · 1,92 · 2/0; `Cheapest`/`vs`/`Hotel` 3 · 1,84 · 2/0 | `Visited` 15 · **0,76** · 3/6; `Holiday` (sustantivo) 3 · 0,36 · 0/2; `Nobody`/`No One` 4 · 0,54 · 1/2; `Island` 4 · 0,63 · 0/2; `Country` 4 · 0,60 · 0/2 | lo de `Took`/`Stayed` es reciente (2025–26) y el canal crece; pero `Visiting the Town Where the Sun Doesn’t Set` (sep 2024, x6,88) y `…Ghost City` (may 2024, x3,98) son viejos y están arriba |
| BB | `SURVIVAL`/`CHALLENGE` 11 · **2,75** · 10/0; `Coastline` 4 · 3,1; `Real` 3 · 2,52 · 3/0; `Story` 3 · 2,05 · 3/0; `Island` (singular) 10 · 1,87 · 5/1; `Food` 8 · 1,66 · 4/0; `Catch` 5 · 1,83 | `Islands` (plural) 3 · **0,48**; `village` 3 · 0,49; `Worlds` 3 · 0,51; `our` 3 · 0,58; `Camping` 5 · 0,66; `Days` 18 · 0,72 · 4/5; `MOVIE` 4 · 0,73; `Living` 12 · 0,78 · 1/4; `Remote` 12 · 0,85 · 4/4 | `Real`, `Story` van dentro de `SURVIVAL CHALLENGE`; `Remote` está en todo y es neutro |
| BZ | `Bought` 4 · **2,73** · 2/0; `for` 6 · 1,81 · 4/0 (`for a Week`, `for Me`, `For Life`); `I` 25 · 1,53 · 13/4; `Day` 6 · 1,47 · 3/0 | `Tried` 8 · **0,65** · 2/4; `with` 3 · 0,38; `Millionaire … EP.` 5 · 0,69 | `Bought` y `I` pesan en la época 4 (crecimiento); `Tried` es sobre todo de las épocas 1–2 |

**Singular contra plural (BB)**: `Island` en singular, 10 títulos, mediana x1,87; `Islands` en plural, 3, x0,48. Una
isla es un náufrago; varias islas son un itinerario.

### ForrestGalante (39 maduros; 7 altos, 11 bajos)

**Los 10 mejores, palabra a palabra**

| # | Título | x | Gatillo (posición) | Se nombra exacto | Se deja vago a propósito | Pregunta que deja |
|---|---|---|---|---|---|---|
| 13 | `Private Tour of an Indian Billionaire’s Secret Bird Sanctuary` | 4,24 | `Billionaire’s` (p. 6/9), con `Secret` (7) | nacionalidad, tipo de dueño, aves | quién es, qué aves | ¿qué pájaros guarda en secreto un milmillonario? (miniatura: picozapato y casuario en un pasillo de cristal) |
| 5 | `Why No Bird, Fish or Mammal Will Cross this Invisible Line` | 4,21 | `Invisible Line` (p. 10–11/11), preparado por `No` (2) | tres clases de animales: totalidad | dónde está; `this` remite a la miniatura (río con raya roja) | ¿qué línea frena a todos y qué pasa si la cruzan? |
| 21 | `5 Animals That Have Only Been Seen Once` | 3,43 | `Only … Once` (p. 5 y 8/8) | número, propiedad | qué animales | ¿cómo sabemos que existe algo visto una vez? (miniatura: espécimen en mesa de laboratorio, `ONLY ONE FOUND`) |
| 35 | `Face to Face with India’s Deadliest Animals (Private Tour)` | 3,28 | `Face to Face` (p. 1–3/9) + `Deadliest` (6) | país | qué animales | ¿hasta dónde se acerca? (miniatura: cobra a un palmo, cartel `DEADLY SNAKE`) |
| 23 | `Private Tour of Florida's $1M Crocodile Facility` | 2,53 | `$1M` (p. 5/7) | estado, precio, animal exacto | dueño | ¿qué compra un millón en cocodrilos? |
| 24 | `Face to Face with Brazil’s Deadliest Animals (Private Tour)` | 1,99 | igual que #35 | país | qué animales | la misma; Brasil rinde 0,6 veces lo que India |
| 8 | `Private Tour of Texas' $10M Backyard Zoo` | 1,57 | `$10M Backyard` (p. 5–6/7): precio de zoo en un jardín | estado, precio | dueño, animales | ¿cómo cabe un zoo de 10 millones en un patio? |
| 33 | `Staying Overnight Inside an Indian Billionaire’s Private Wildlife Rescue Center` | 1,49 | `Overnight Inside` (p. 2–3/10) | dueño-tipo, nacionalidad | qué pasa de noche | ¿qué ocurre ahí de noche? 79 caracteres, pero el gatillo va delante y sobrevive al corte |
| 19 | `Private Tour of an Indian Billionaire's Secret Elephant Sanctuary` | 1,42 | `Billionaire's` + `Secret` (p. 6–7/9) | animal | cuántos, cómo | ¿cómo es un santuario privado de elefantes? (respuesta intuible: India + elefante es esperable) |
| 27 | `I Met 6 Extinct Animals in Real Life` | 1,39 | `Extinct` (p. 4/8) contra `in Real Life` (6–8) | número | cómo (¿réplicas?, ¿redescubiertos?) | ¿cómo se conoce en persona a un animal extinto? |

**Los 8 peores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 37 | `5 More Extinct Animals I Believe Could Still Be Alive` | 0,27 | `Still Be Alive` (p. 8–10/10), amortiguado por `More` (2), `I Believe` (5–6) y `Could` (7) | número | todo | «¿él cree que…?»: pide fe en una opinión, y `More` avisa de que es la segunda parte |
| 25 | `Wildlife Expert Reacts To Terrifying Animal Encounters` | 0,30 | `Terrifying` (p. 5/7) | nada | quién, qué encuentros | ninguna concreta; `Reacts` = vídeos ajenos (miniatura: elefante en un aeropuerto, cámara de seguridad) |
| 9 | `5 Animals That Survived The Ice Age` | 0,33 | `Survived` (p. 4/7) | número, época | cuáles | «¿y?»: que haya animales que sobrevivieron a la glaciación no sorprende; la miniatura promete más (`STILL ALIVE?`, bestia en el hielo) |
| 40 | `5 of the Rarest Animals on Earth` | 0,35 | `Rarest` (p. 4/7) | nada | cuáles | superlativo de categoría: ninguna |
| 14 | `5 Terrifying Animals Only Found in Caves` | 0,41 | `Terrifying` (p. 2/7) | lugar | cuáles | el adjetivo dice qué sentir en vez de dar el hecho |
| 39 | `7 Mysterious Animals Caught on Trail Camera` | 0,41 | `Mysterious` (p. 2/7) | soporte | cuáles | «misterioso» + cámara trampa = imagen borrosa (miniatura: `PROOF OF CHUPACABRA?`) |
| 16 | `Why Nature Always Kills Its Largest Animals First` | 0,42 | `Always Kills` (p. 3–4/8) | nada visible | qué animales | ley abstracta; la miniatura (`LAST PHOTO EVER?`) no la enseña |
| 10 | `5 More Extinct Animals Found in the Last 15 Years` | 0,48 | `Found` junto a `Extinct` (p. 3 y 5/10) | ventana de tiempo | cuáles | la paradoja se diluye en «15 años» y `More` la marca como secuela |

Hipótesis: arriba, 7 de 10 son acceso con un cualificador de estatus o de precio (`Billionaire’s`, `$1M`, `$10M`,
`Deadliest`) y 3 son paradojas que se pueden ver (`Invisible Line`, `Only Been Seen Once`, `Extinct … in Real Life`).
Abajo, 7 de 8 son listas, y su palabra fuerte es un adjetivo que ordena la emoción (`Terrifying` ×2, `Mysterious`) o una
categoría (`Rarest`), más `More` dos veces. El adjetivo de emoción no sustituye al objeto.

### colsonscritters (39 maduros; 9 altos, 8 bajos)

**Los 10 mejores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 36 | `BUYING Reptiles at World's Largest Reptile Expo!! **INSANE**` | 7,11 | `World's Largest` (p. 4–5/8) | animal, sitio | qué compra, cuánto | ¿qué hay y qué se lleva de la mayor feria del mundo? (miniatura: precio pegado a cada reptil y una silueta con `?`) |
| 40 | `I Built a Tide Pool for Sea Creatures in 100 days!!` | 5,8 | `in 100 days` (p. 9–11/11) | obra, destinatario, plazo | cómo queda | ¿qué sale de 100 días de obra? (miniatura `DAY 100`, el estanque terminado) |
| 14 | `Buying FISH for My NEW Freshwater STINGRAY Pond!!` | 5,66 | `NEW … STINGRAY Pond` (p. 5–8/8) | el sitio nuevo y su habitante | qué peces | ¿qué peces viven con rayas? Lo nuevo es el mundo, no el pez |
| 38 | `BUYING Reptiles At This INSANE REPTILE SHOW!!` | 3,65 | `INSANE REPTILE SHOW` (p. 5–7/7) | animal | qué feria | la de #36, sin récord |
| 16 | `Touring America's Largest Reptile EXPO!! *INSANE*` | 2,9 | `America's Largest` (p. 2–3/6) | escala | qué hay | ¿cómo es la mayor feria del país? |
| 31 | `I GAVE HIM 25 NEW ANIMALS!!` | 2,5 | `HIM` (p. 3/6) + `25` (4) | cantidad | a quién (lo dice la miniatura: otro creador) y qué animales | ¿a quién y qué? Único título del canal que calla al sujeto, y es colaboración |
| 29 | `Buying FISH That WALK ON LAND For My Backyard Tide Pool!!` | 2,44 | `WALK ON LAND` (p. 4–6/11) | rasgo imposible | nombre de la especie | ¿peces que andan? |
| 43 | `TOURING THIS HUGE REPTILE EXPO!!! *INSANE*` | 1,81 | `HUGE` (p. 3/6) | animal | escala sin medida | menos que «World’s / America's Largest» |
| 11 | `I UNBOXED $15,000 Worth of EXOTIC MYSTERY FISH! + GIVEAWAY` | 1,7 | `$15,000` (p. 3/9) + `GIVEAWAY` (9) | precio | qué peces | ¿qué hay en 15.000 $ de peces?, ¿me puede tocar? |
| 15 | `SURPRISING FINATIC with DREAM FISH for 2,000G Aquarium!!` | 1,46 | `FINATIC` (p. 2/8) | creador, tamaño | qué pez | ¿cómo reacciona? (empata con `SURPRISING PAUL CUFFARO WITH SHARKS FOR HIS POND!!!`, #44) |

**Los 8 peores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 23 | `Building a ENCLOSURE for My NEW PET!!` | 0,26 | ninguno; `NEW PET` (p. 6–7/7) esconde el animal | nada | el animal (miniatura: silueta de camaleón con `?`) | «¿qué mascota?» no basta |
| 22 | `Touring my DREAM AQUARIUM with OVER 5,000 SEA CREATURES!!` | 0,28 | `OVER 5,000` (p. 6–7/9) | cifra | dónde | ninguna: un acuario público se puede visitar; `my DREAM` es opinión |
| 19 | `Exploring an INSANE ZOO Full of EXOTIC ANIMALS!!` | 0,31 | `INSANE` (p. 3/8) | nada | qué zoo, de quién, qué animales | ninguna: tres adjetivos genéricos |
| 45 | `I BOUGHT a Live Fish MYSTERY BOX! (What’s Inside?)` | 0,36 | `MYSTERY` (p. 6/9) | nada | precio y contenido | ¿qué hay? sin magnitud no tira |
| 30 | `FEEDING My FISH a SEAFOOD PLATTER!!` | 0,44 | `SEAFOOD PLATTER` (p. 5–6/6) | comida | nada en juego | chiste visual sin riesgo |
| 25 | `NOT Doing THIS Almost Ruined My Tide Pool…` | 0,51 | `THIS` (p. 3/8) + `Almost` (4) | el sitio | el qué | `Almost` dice que no pasó nada: no hay pérdida |
| 28 | `The Secrets to My DAD'S 150G SALTWATER AQUARIUM!! - 10 YEAR OLD Reef Tank` | 0,59 | `Secrets` (p. 2/13) | dueño, tamaño, edad | qué secretos | tutorial de acuario doméstico; dos títulos pegados por un guion |
| 42 | `I Added the FIRST Fish to My Backyard Tide Pool!!` | 0,60 | `FIRST` (p. 4/9) | hito | qué pez | hito para fieles |

Hipótesis: arriba, salir de casa a un sitio con escala (4 ferias), una obra con plazo, un mundo nuevo, un rasgo
imposible, dos colaboraciones y una cifra. Abajo, el animal escondido (#23, #45), visitas sin dueño ni prueba (#19, #22)
y la rutina de casa (#28, #30, #42, #25). La caída del canal con el tiempo (x1,30 → x0,82) no explica el reparto: las
ferias están en las dos mitades.

### benmorris (36 maduros; 12 altos, 12 bajos)

**Los 10 mejores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 29 | `Visiting the Town Where the Sun Doesn’t Set` | 6,88 | `Sun Doesn’t Set` (p. 6–8/8) | fenómeno | el pueblo (miniatura: `2:17 am` a pleno sol) | ¿cómo se vive sin noche? |
| 17 | `I Took a Sleeper Train Across Europe` | 6,67 | `Sleeper Train` (p. 4–5/7) | vehículo, alcance | ruta, precio, veredicto | ¿cómo es dormir cruzando un continente?, ¿lo haría yo? |
| 7 | `I Took a Sleeper Train Across the UK` | 6,06 | ídem | ídem, en casa | ídem | ídem |
| 3 | `I Stayed in Hotels that Broke the Internet` | 5,02 | `Broke the Internet` (p. 6–8/8) | categoría | cuáles | ¿son como en las fotos virales? (miniatura: piscina en un acantilado y `1.3B ▷`) |
| 34 | `I Visited a Failed $100 Billion Dollar Ghost City` | 3,98 | `Failed` (p. 4/9) + `Ghost` (8) | cifra | el país (la miniatura deja leer `FOREST CITY`) | ¿cómo se tiran 100.000 millones? |
| 1 | `I Took a Sleeper Train Across Japan` | 3,96 | `Sleeper Train` | ídem | ídem | ídem |
| 11 | `I Took a First Class Sleeper Bus Across Europe` | 3,68 | `First Class … Bus` (p. 4–7/9) | clase, vehículo | ídem | ¿un autobús de primera?, ¿cómo es? |
| 26 | `I Visited the World's Biggest City Nobody’s Heard Of` | 3,47 | `Biggest` (p. 5/9) contra `Nobody’s Heard Of` (7–9) | récord | qué ciudad | ¿cómo puede la mayor ciudad ser desconocida? |
| 14 | `I Stayed at Cheapest vs Most Expensive Hotel in Bali` | 3,46 | `Cheapest vs Most Expensive` (p. 4–7/10) | sitio aspiracional | precios, veredicto | ¿cuánto cambia y cuál compensa? |
| 12 | `Visiting the Town that’s Always Dark (No Sunlight)` | 2,4 | `Always Dark` (p. 5–6/8) | fenómeno | el pueblo | ¿cómo se vive sin sol? (el paréntesis repite lo dicho) |

**Los 8 peores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 18 | `I Visited the World's Emptiest Country` | 0,17 | `Emptiest` (p. 5/6) | récord de ausencia | país | «¿qué hay?» → nada |
| 22 | `Living with Bajau People for a Week` | 0,19 | `Bajau` (p. 3/7) | pueblo, plazo | lo extraordinario (aguantan bajo el agua: `13 Minutes` solo en la miniatura) | ninguna para quien no sabe quiénes son |
| 15 | `Asking a Complete Stranger to Go on Holiday` | 0,21 | `Complete Stranger` (p. 3–4/8) | nada | adónde | experimento social sin sitio en un canal de sitios |
| 20 | `I Visited the Rudest City in the World` | 0,28 | `Rudest` (p. 4/8) | opinión | ciudad (miniatura: torre Eiffel, reseña de 1 estrella) | «París es borde» es tópico: no hay sorpresa |
| 5 | `I Visited Italy’s Secret Island Nobody’s Heard of` | 0,30 | `Secret` + `Nobody’s Heard of` (p. 4 y 6–8/8) | país | isla | redundante: secreta y desconocida dicen lo mismo (miniatura `0 VISITORS`) |
| 16 | `I Went on Holiday with Prime Minister of UK` | 0,36 | `Prime Minister` (p. 6–7/9) | cargo | quién | promesa difícil de creer (y sin `the`) |
| 9 | `I Visited the Most Isolated Island in Europe` | 0,41 | `Most Isolated` (p. 4–5/8) | región | isla | otra vez ausencia |
| 19 | `The Side of Tokyo Nobody Talks About` | 0,42 | `Nobody Talks About` (p. 5–7/7) | ciudad | qué «lado» | fórmula gastada sobre la ciudad más vista |

Hipótesis: arriba, 6 de 10 son una experiencia con duración que el espectador podría comprar (`Took`, `Stayed`), 2 un
fenómeno físico imposible y 2 una paradoja o una pérdida gigante. Abajo, 4 de 8 prometen ausencia (`Emptiest`, `Most
Isolated`, `Secret … Nobody’s Heard of`, `Nobody Talks About`), 3 van de personas que el público no conoce y 1 es un
tópico. `I Visited` está en 4 de los 8 peores y en 2 de los 10 mejores.

### BacktoBasics (57 maduros; 23 altos, 15 bajos)

**Los 10 mejores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 45 | `SURVIVAL CHALLENGE: Australia's Most Controversial Shipwreck (No Food, No Water, No Shelter)` | 14,91 | `Controversial` (p. 5/12) + `(No Food, No Water, No Shelter)` (7–12) | género, país, «naufragio», las tres reglas | qué naufragio y qué pasó | ¿qué pasó allí, y aguanta él donde otros no? (miniatura: langosta gigante, cofre, fuego) |
| 54 | `10 Days Living with The Worlds Oldest Living Culture (Ep1)` | 4,83 | `Oldest Living Culture` (p. 7–9/10) | plazo, récord humano | qué cultura | ¿cómo vive el pueblo más antiguo del mundo? `(Ep1)` = empieza una historia |
| 7 | `SURVIVAL CHALLENGE: Shipwrecked on Ancient Coastline` | 4,73 | `Shipwrecked` (p. 3/6) | papel (náufrago) | dónde | ¿sale de ahí? |
| 10 | `We Caught & Ate Flying Fox on a Remote Island` | 4,31 | `Ate Flying Fox` (p. 3–5/9) | animal exacto | sabor, cómo | ¿se come un murciélago? (tabú) |
| 22 | `SURVIVAL CHALLENGE: Castaway on Tropical Island` | 4,06 | `Castaway` (p. 3/6) | papel | dónde | ¿sobrevive como en la película? |
| 5 | `SURVIVAL CHALLENGE: The Real Crocodile Dundee!` | 3,77 | `Real Crocodile Dundee` (p. 4–6/6) | referente de cine | quién es | ¿quién es el Cocodrilo Dundee de verdad? |
| 58 | `Surviving from Foraged Bushfoods on Rugged Coastline` | 3,62 | sin gatillo claro (`Bushfoods`, p. 4/7) | | | hipótesis: lo empuja la miniatura (un cangrejo enorme en la mano); el título solo describe |
| 41 | `SURVIVAL CHALLENGE: Plane Crash In Forbidden Jungle 🛩️🔥` | 3,33 | `Plane Crash` (p. 3–4/7) + `Forbidden` (6) | escenario | | ¿cómo se sobrevive a eso? |
| 53 | `Kangaroo Catch & Cook in Remote Australia (ep2)` | 3,10 | `Kangaroo` (p. 1/7) | animal | | ¿se come el canguro? (tabú del animal símbolo) |
| 9 | `He Fed an Entire Village With ONE Giant Fish (Volcano Island)` | 2,77 | `ONE` (p. 6/10) contra `Entire Village` (3–5) | escala | quién es «él» | ¿cómo da un pez para un pueblo? |

**Los 8 peores**

| # | Título | x | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|
| 34 | `Head-Hunter Island (The Last Village of Warriors)` | 0,21 | `Head-Hunter` (p. 1/7) | etiqueta | qué hacen ellos allí | ninguna acción: cartel de documental |
| 16 | `500miles in 7 Days (Australia's Wildest Coastline)` | 0,29 | ninguno: cifras sin riesgo | distancia, plazo | en qué | «¿y?»: 800 km sin peligro ni meta |
| 28 | `OUR NEW HOME! (How We Power It⚡)` | 0,29 | `NEW HOME` | | | fuera del tema del canal |
| 55 | `Self Sufficient Living: Lobsters & Coconuts for Christmas` | 0,35 | `Christmas` | comida | | especial de fecha; langosta y coco = paraíso, no apuro |
| 56 | `Alone in the Australian Wilderness (My honest thoughts)` | 0,35 | `Alone` (p. 1/8) | | | `(My honest thoughts)` anuncia charla, no acción |
| 36 | `14 Days Living in Remote Islands Learning Bush Medicine` | 0,41 | `Learning` (p. 6/9) | plazo, tema | | documental educativo, sin riesgo |
| 46 | `2 Days Camping on Remote Reefs (Catch, Clean & Cook)` | 0,43 | ninguno; el paréntesis es un menú | plazo | | dos días no son reto |
| 51 | `We made Hand Spears with Aboriginal Hunters... Then Tested Them` | 0,44 | `Then Tested Them` (final) | | si funcionan | respuesta obvia; el `...` promete un giro que no hay |

Hipótesis: arriba, 5 de 10 son `SURVIVAL CHALLENGE` con escenario de película, 2 un tabú alimentario, 1 una
desproporción de escala, 1 un récord humano en su episodio 1 y 1 sin gatillo en el texto. Abajo, ninguno tiene
amenaza: 4 son procesos o aprendizaje, 2 son personales, 1 es especial de fecha y 1 es una etiqueta sin verbo.

### biaheza (42; comparar por épocas)

**Los 10 mejores**

| # | Título | x | Época | Gatillo (posición) | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|---|
| 39 | `I Tried Forex Day Trading for a Week (Complete Beginner)` | 5,62 | 1 | `(Complete Beginner)` (p. 9–10/10) + `for a Week` (6–8) | método, plazo, nivel | resultado | ¿gana o pierde un novato en una semana? (la miniatura adelanta `$1,000` → `$3.58`: la pregunta pasa a «¿cómo?») |
| 7 | `I Bought a Crashed Supercar to Make a Profit` | 5,54 | 4 | `Crashed Supercar` (p. 4–5/9) | objeto, meta | si lo consigue | ¿se gana dinero con un coche destrozado? |
| 5 | `I Turned a Regular Car Into a Camper` | 4,99 | 4 | `Regular … Into` (p. 4 y 6/8) | antes y después | cómo | ¿mi coche podría ser un camper? |
| 6 | `I Rebuilt a Crashed Lamborghini in My Garage` | 4,57 | 4 | `Lamborghini` (p. 5/8) contra `My Garage` (7–8) | marca exacta | cómo | ¿puede uno solo rehacer un Lamborghini en casa? |
| 11 | `I Bought a Failed Business and Turned it Around` | 4,46 | 3 | `Failed` (p. 4/9) | antes y después, contado | cómo | ¿cómo se resucita un negocio? (miniatura: cheque de `$1,000,000`) |
| 40 | `I Spent 8 Hours Using Money Making Apps` | 2,98 | 1 | `Money Making Apps` (p. 6–8/8) | plazo | cuánto saca | ¿cuánto se gana de verdad con esas apps? |
| 1 | `I Tested Every Budget of Sports Car` | 2,91 | 4 | `Every Budget` (p. 4–5/8) | categoría | precios, veredicto | ¿qué deportivo da más por su precio? (miniatura: escalera `$60K`…`$10K`) |
| 4 | `I Built a Camper and Got Attacked` | 2,70 | 4 | `Got Attacked` (p. 6–7/7) | suceso | quién, por qué | ¿quién le atacó? |
| 12 | `I Made a Secret Youtube Channel to Prove it’s Not Luck` | 2,02 | 3 | `Secret` (p. 4/11) + `Prove it’s Not Luck` (8–11) | tesis | qué canal, si lo logra | ¿se puede crecer sin suerte? |
| 37 | `I Paid Fiverr to Day Trade for Me` | 1,99 | 1 | `for Me` (p. 7–8/8) | servicio exacto | resultado | ¿puede un desconocido de cinco dólares ganar dinero por mí? |

**Los 8 peores**

| # | Título | x | Época | Gatillo | Exacto | Vago | Pregunta que deja |
|---|---|---|---|---|---|---|---|
| 42 | `Your Dropshipping (and Personal) Questions Answered \| Biaheza Q & A` | 0,18 | 1 | ninguno | formato | | para fieles |
| 33 | `I Tried Making Money With Sports Cards` | 0,24 | 1 | `Sports Cards` (p. 6–7/7) | tema | cuánto | `Tried` + `Making Money` vago, sin cifra ni plazo |
| 27 | `Some books that are pretty good` | 0,27 | 2 | ninguno (antititular irónico) | | | ninguna |
| 41 | `I Tried Paying Fiverr to Feature me on Forbes` | 0,36 | 1 | `Forbes` (p. 8/8) | marcas | | vanidad: el premio no es dinero ni algo que el que mira quiera |
| 16 | `How He Made Millions off Amazon at 17` | 0,37 | 2 | `Millions … at 17` | edad, cifra | quién | historia de otro: el «podría ser yo» necesita al creador delante |
| 8 | `I Tried to Wheelie With ZERO Experience` | 0,38 | 3 | `ZERO Experience` (p. 5–6/7) | nivel | | el molde del novato sin dinero y fuera del tema |
| 10 | `The YouTube Hamster Wheel` | 0,39 | 3 | metáfora | | | meta del canal |
| 36 | `I Tried the Instacart Side Hustle` | 0,40 | 1 | `Instacart` (p. 4/6) | marca | cuánto | respuesta previsible: repartir no hace rico a nadie |

Hipótesis: arriba, 7 de 10 llevan un verbo de compromiso (`Bought`, `Turned`, `Rebuilt`, `Built`, `Made`, `Paid`,
`Tested`) con dinero o transformación en juego. Abajo, 3 son del canal hablando de sí mismo, 3 son `I Tried` y 1 es la
historia de otro. 5 de los 10 mejores son de la época 4 (el crecimiento del canal puede explicar parte); dentro de la
época 1, que es comparable consigo misma, también ganan el plazo y el novato (#39 x5,62, #40 x2,98) frente al «side
hustle» sin plazo (#36 x0,40, #41 x0,36).

### Parejas casi iguales con resultado muy distinto

| Pareja (mismo molde) | Ratios | Qué palabra cambia | Qué hace el cambio |
|---|---|---|---|
| FG #13 `…Indian Billionaire’s Secret Bird Sanctuary` / #19 `…Secret Elephant Sanctuary` | 4,24 / 1,42 | `Bird` ↔ `Elephant` | elefantes en India es lo esperable; un santuario secreto de **aves** de un milmillonario no lo es (y la miniatura enseña aves rarísimas). El sustantivo inesperado triplica |
| FG #23 `Private Tour of Florida's $1M Crocodile Facility` / #3 `Private Tour of Florida’s Best Backyard Animal Sanctuary` | 2,53 / 1,00 | `$1M Crocodile` ↔ `Best Backyard Animal` | precio + animal exacto frente a opinión + categoría |
| FG #8 `Private Tour of Texas' $10M Backyard Zoo` / #6 `Private Tour of New York's Secret $10M Reptile Basement` | 1,57 / 0,91 | `Backyard Zoo` ↔ `Secret … Reptile Basement` | mismo precio; «zoo» agranda, «sótano» encoge. `Secret` no salva un sitio pequeño |
| FG #35 `Face to Face with India’s Deadliest Animals (Private Tour)` / #24 `…Brazil’s…` | 3,28 / 1,99 | el país | `India`/`Indian` en 4 títulos de FG, los 4 por encima de x1,4 (mediana x2,38) |
| FG #21 / #32 `5 Animals That Have Only Been Seen Once` (títulos **idénticos**) | 3,43 / 1,36 | ninguna: cambia la miniatura | #21: espécimen monstruoso sobre mesa de laboratorio, `ONLY ONE FOUND`; #32: un pez pequeño en la arena, `ONLY PHOTO EVER?`. El título fija el techo; la miniatura decide cuánto se acerca a él |
| FG #41 `6 Deadly Sea Monsters That Actually Exist` / #7 `5 Deadly Sea Monsters That Actually Exist` | 1,36 / 0,70 | `6` ↔ `5` (y 10 meses después) | repetir el título entero a la mitad. No es el número: es la repetición |
| FG #30 `6 Extinct Animals Found in 2025` / #10 `5 More Extinct Animals Found in the Last 15 Years` | 1,29 / 0,48 | `More` + `in 2025` ↔ `in the Last 15 Years` | noticia fresca frente a secuela con ventana de 15 años. `More`: 3 títulos, los 3 bajos |
| FG #5 `Why No Bird, Fish or Mammal Will Cross this Invisible Line` / #16 `Why Nature Always Kills Its Largest Animals First` | 4,21 / 0,42 | ley visible (`this Invisible Line`) ↔ ley abstracta (`Nature`) | el demostrativo señala algo que está en la miniatura; `Nature` no se puede fotografiar |
| FG #11 `The Closest Call I’ve Ever Had With Death` / #36 `3 Closest Calls I've Had With Death` | 0,78 / 0,59 | `The … Ever` ↔ `3` | uno solo, el peor, gana a la lista (diferencia pequeña, mismo sentido que en todo el canal) |
| CC #38 `BUYING Reptiles At This INSANE REPTILE SHOW!!` / #33 `BUYING SEA CREATURES At This INSANE AQUARIUM SHOW!!` | 3,65 / 0,68 | `Reptiles … REPTILE` ↔ `SEA CREATURES … AQUARIUM` | misma frase; el animal decide (×5). El tema pesa más que la forma |
| CC #36 `…at World's Largest Reptile Expo!!` / #16 `Touring America's Largest Reptile EXPO!!` / #43 `TOURING THIS HUGE REPTILE EXPO!!!` / #24 `…at this INSANE REPTILE EXPO!!` | 7,11 / 2,90 / 1,81 / 1,05 | el dueño del superlativo | `World's` > `America's` > `THIS HUGE` > `this INSANE`: cuanto más grande el mundo del récord, más sube; el adjetivo sin medida, lo último |
| CC #40 `I Built a Tide Pool for Sea Creatures in 100 days!!` / #8 `…for 365 days!!` | 5,80 / 0,95 | `in 100` ↔ `for 365` | `in` = plazo con resultado (antes y después); `for` = duración (aniversario). Además #8 es la secuela y dura 83 minutos |
| CC #14 `Buying FISH for My NEW Freshwater STINGRAY Pond!!` / #17 `BUYING NEW FISH for My BACKYARD SALTWATER Tide Pool!!` | 5,66 / 0,64 | `NEW` va con el sitio ↔ con el pez | un estanque nuevo con rayas es un mundo nuevo; un pez nuevo en el estanque de siempre es rutina |
| CC #27 `Building a MUD BATH For My Pet WALKING FISH!!` / #23 `Building a ENCLOSURE for My NEW PET!!` | 1,30 / 0,26 | `WALKING FISH` ↔ `NEW PET` | nombrar un rasgo imposible frente a esconder el animal |
| CC #29 `Buying FISH That WALK ON LAND For My Backyard Tide Pool!!` / #32 `Buying EXOTIC SALTWATER FISH for My Backyard Tide Pool!!` | 2,44 / 0,72 | `That WALK ON LAND` ↔ `EXOTIC SALTWATER` | rasgo frente a adjetivo genérico |
| CC #11 `I UNBOXED $15,000 Worth of…` / #10 `I WAS SENT A $1,500 FISH MYSTERY BOX!!` / #45 `I BOUGHT a Live Fish MYSTERY BOX! (What’s Inside?)` | 1,70 / 1,21 / 0,36 | la cifra | sin precio el misterio no tira; la cifra le da magnitud (y `GIVEAWAY` mete al que mira) |
| CC #12 `Exploring PRIVATE Backyard FULL of EXOTIC ANIMALS! **INSANE**` / Paul Cuffaro #113 `Exploring PRIVATE BackYard FULL of EXOTIC ANIMALS!!` (primera tanda) | 0,88 / 2,68 | ninguna: otro canal | copiar el molde no copia el resultado: el acceso funciona si el que entra tiene fama de entrar donde otros no |
| BM #26 `I Visited the World's Biggest City Nobody’s Heard Of` / #5 `I Visited Italy’s Secret Island Nobody’s Heard of` | 3,47 / 0,30 | `World's Biggest City` ↔ `Italy’s Secret Island` | con «la mayor», `Nobody’s Heard Of` es una paradoja; con «secreta», es una redundancia |
| BM #34 `I Visited a Failed $100 Billion Dollar Ghost City` / #13 `I Visited China’s $15 Billion Fake Cities` | 3,98 / 0,46 | `a Failed … Ghost City` ↔ `China’s … Fake Cities` | un sitio, una historia de fracaso y vacío, frente a varias copias en plural; y el país nombrado quita el hueco |
| BM #29 `Visiting the Town Where the Sun Doesn’t Set` / #12 `Visiting the Town that’s Always Dark (No Sunlight)` | 6,88 / 2,40 | día eterno ↔ noche eterna | las dos funcionan (fenómeno físico); la luz es más vendible que la oscuridad y el paréntesis de #12 repite |
| BM #31 `I Visited the World’s Hottest City` / #20 `I Visited the Rudest City in the World` / #18 `I Visited the World's Emptiest Country` | 1,75 / 0,28 / 0,17 | `Hottest` ↔ `Rudest` ↔ `Emptiest` | superlativo físico que se siente, frente a opinión y frente a ausencia |
| BM #32 `I Visited the Most Hated City in Europe` / #25 `I Visited the City that Hates Tourists` | 1,46 / 0,47 | `Most Hated` ↔ `Hates Tourists` | ser odiada (¿por qué?) abre una historia; odiar al turista es contra el que mira |
| BM sleeper: #17 Europe / #7 UK / #1 Japan / #11 `First Class Sleeper Bus Across Europe` | 6,67 / 6,06 / 3,96 / 3,68 | el sitio y el vehículo | el molde aguanta cuatro veces seguidas porque cada vez la promesa es nueva (otro país, otro vehículo), no «más de lo mismo» |
| BM hoteles: #14 Bali / #8 Alps / #2 London | 3,46 / 1,84 / 1,19 | el sitio (y el orden: ene → may → ago 2026) | lo aspiracional rinde más que la ciudad de casa; puede ser también desgaste |
| BB #45 `SURVIVAL CHALLENGE: Australia's Most Controversial Shipwreck (No Food, No Water, No Shelter)` / #42 `SURVIVAL CHALLENGE: Australia's Most Scandalous Shipwreck` | 14,91 / 1,75 | `Controversial` ↔ `Scandalous` y el paréntesis triple, que desaparece | la regla de tres negaciones convierte un relato en un reto que el que mira mide contra sí mismo; #42 es además la continuación, dos meses después |
| BB #54 `10 Days Living with The Worlds Oldest Living Culture (Ep1)` / #13 `10 Days Living with Worlds Oldest Living Culture (The Movie)` | 4,83 / 0,47 | `(Ep1)` ↔ `(The Movie)` | el mismo viaje montado como película 14 meses después: «ya lo vi». Las recopilaciones `MOVIE` de BB: mediana x0,84 |
| BB #9 `He Fed an Entire Village With ONE Giant Fish (Volcano Island)` / #35 `GIANT CRAB HUNTING & Spearfishing to feed whole village` | 2,77 / 0,49 | `ONE … Entire` ↔ lista de dos actividades | la desproporción (uno contra todos) es el gancho; la lista de tareas lo apaga |
| BB #11 `RARE GIANT CRAB Catch & Cook!` / #33 `GIANT TUNA CATCH & COOK (14 Days on Tropical Island)` | 2,50 / 0,63 | `RARE … CRAB` ↔ `TUNA` | el atún es comida de supermercado; un cangrejo raro no |
| BB #22 `SURVIVAL CHALLENGE: Castaway on Tropical Island` / #18 `SURVIVAL CHALLENGE: Hand Catching Food On Tropical Island` | 4,06 / 2,75 | `Castaway` ↔ `Hand Catching Food` | un papel de película frente a una tarea |
| BB #31 `🇵🇬[EP:1] Welcome to the World’s Most Dangerous Paradise...` / #26 `🇵🇬[EP:5] 4 Weeks in the Worlds Most Dangerous Paradise` | 1,65 / 0,51 | el número de episodio | la misma frase gancho rinde la tercera parte cuando se repite a mitad de serie |
| BB #27 `🇵🇬[EP:4] 30 Days Camping & Spearfishing in Remote PNG` / #30 `🇵🇬[EP:2] 30 Days Camping & Fishing in Remote Papua New Guinea` | 1,87 / 0,51 | `Spearfishing` ↔ `Fishing` (y `PNG` ↔ nombre entero) | pescar con arpón es acción; pescar, a secas, no. Indicio débil: en una serie pesa mucho el número de episodio |
| BZ #40 `I Spent 8 Hours Using Money Making Apps` / #23 `I Spent 8 Hours Playing Games That Pay Real Money` | 2,98 / 1,53 | `Using Money Making Apps` ↔ `Playing Games That Pay Real Money` | `Real` es defensivo (sugiere que se duda); además es la segunda vez |
| BZ #26 `I Tried Mining Bitcoin For a Week` / #24 `I Tried Mining Bitcoin on my Phone` | 1,74 / 0,90 | `For a Week` ↔ `on my Phone` | el plazo promete un resultado medible; «en el móvil» se responde solo (no) |
| BZ #37 `I Paid Fiverr to Day Trade for Me` / #41 `I Tried Paying Fiverr to Feature me on Forbes` | 1,99 / 0,36 | `Paid … to Day Trade for Me` ↔ `Tried Paying … Forbes` | el premio que quiere el que mira (dinero) frente a vanidad; `Paid` (hecho) frente a `Tried Paying` (intento) |
| BZ #7 `I Bought a Crashed Supercar to Make a Profit` / #17 `I Bought $15,000 Worth of Amazon Returns` | 5,54 / 0,86 | `a Crashed Supercar to Make a Profit` ↔ `$15,000 Worth of Amazon Returns` | un objeto que se transforma y una meta, frente a un lote misterioso |
| BZ Millionaire EP. 1 → EP. 5 | 1,50 → 0,88 → 0,69 → 0,66 → 0,45 | el número | la serie numerada pierde en cada entrega |

### Lo que se repite en más de un canal (con cautela)
- **El verbo decide**: `I Took` (5, x3,96), `I Stayed` (4, x2,65), `I Bought` en BZ (4, x2,73) y los de obra de BZ
  (`Built`, `Turned … Into`, `Rebuilt`) frente a `I Visited` (15, x0,76) e `I Tried` (8, x0,65). Los primeros cuentan una
  experiencia con duración, dinero o resultado; los segundos, una presencia o un intento.
- **Secuela anunciada = bajada**: `More` (FG, 3 de 3 bajos), `(The Movie)` frente a `(Ep1)` (BB), EP. 1 → EP. 5 (BZ), EP:1
  → EP:5 con la misma frase (BB), `for 365 days` tras `in 100 days` (CC). Contraejemplo: repetir el molde con un
  sustantivo nuevo sí aguanta (los cuatro trenes de BM, las ferias de CC, `Only Been Seen Once` que subió la segunda vez).
- **Adjetivo de emoción o de categoría sin objeto** (`Terrifying`, `Mysterious`, `Rarest`, `INSANE ZOO`, `EXOTIC
  SALTWATER`, `my DREAM`): abajo en FG y CC.
- **La ausencia no se vende**: `Emptiest`, `Most Isolated`, `Secret … Nobody’s Heard of`, `Nobody Talks About` (BM, los 4
  por debajo de x0,45 salvo cuando la ausencia choca con un récord: `World's Biggest City Nobody’s Heard Of`, x3,47).
- **Gente que el público no conoce** baja (BM B7, 3 de 3; BZ `How He Made Millions…`); gente que el público conoce sube
  (CC con Finatic y Paul Cuffaro, ninguno bajo).
- **Lo que el canal hace de sí mismo** (Q&A, especial del millón, `OUR NEW HOME!`, reflexiones, la familia): siempre abajo.

---

## 6. Lo propio de ESTE idioma

**Cómo suena natural en estos cinco:**
- **`I` + pasado simple es natural y nada «traducido»** cuando el vídeo es una experiencia propia: `I Took a Sleeper
  Train Across Europe`, `I Bought a Crashed Supercar to Make a Profit`. Siete palabras, sujeto, verbo, objeto,
  complemento. La versión telegráfica de la primera tanda (`BITTEN by…`) es propia de animales y retos, no del inglés
  en general.
- **El sitio sin nombre + relativa**: `the Town Where the Sun Doesn’t Set`, `the Town that Pays You $50,000 to Move There`,
  `the Island Run by the Mafia`, `Hotels that Broke the Internet`. Es el giro más rentable de BM y suena muy idiomático
  (`Run by`, `Broke the Internet`).
- **Paradoja con `Nobody’s Heard Of`** pegado a un récord. Solo funciona si choca (`World's Biggest City Nobody’s Heard Of`).
- **Etiqueta de género + dos puntos** (`SURVIVAL CHALLENGE: Castaway on Tropical Island`): sintaxis de cartel de serie
  de televisión; se come los artículos detrás de los dos puntos.
- **Superlativo con dueño-lugar**: `Florida's $1M Crocodile Facility`, `Australia's Most Controversial Shipwreck`,
  `America's Largest Reptile EXPO`, `India’s Deadliest Animals`. Y genitivo de persona-tipo: `an Indian Billionaire’s
  Secret Bird Sanctuary`.
- **Adjetivos apilados delante**: `Indian Billionaire’s Private Wildlife Rescue Center` (cinco modificadores),
  `NEW Freshwater STINGRAY Pond`, `Crashed Lamborghini`, `First Class Sleeper Bus`.
- **Coletillas de documental**: `That Actually Exist`, `in Real Life`, `to Ever Exist`, `on Earth`, `in the World`.

**Mayúsculas reales**: Title Case con palabras función en minúscula es la norma de FG, BM y BZ (118 de 119 títulos sin
gritar nada; la excepción es `ZERO`). CC grita sustantivos (Paul Cuffaro como modelo). BB grita etiquetas (`SURVIVAL CHALLENGE`, `THE MOVIE`,
`GIANT`). Nadie escribe todo en mayúsculas como norma; los 4 de CC son excepciones.

**Giros y palabras de moda (con recuento)**: `Private Tour` 13 (FG) · `Face to Face` 2 · `That Actually Exist` 4 · `Only
Been Seen Once` 2 · `Nobody’s Heard Of`/`Nobody Talks About`/`No One Dares` 4 (BM) · `Cheapest vs Most Expensive` 3 ·
`Broke the Internet` 1 · `Sleeper Train/Bus` 4 · `SURVIVAL CHALLENGE` 11 · `Catch & Cook` 4 · `(THE MOVIE)`/`(FULL
MOVIE)` 4 · `(Real Life Story!)` 2 · `UNCUT`/`Unfiltered` 3 · `Side Hustle` 2 · `Day Trade/Trading` 6 · `Buy it For Life`
1 · `Complete Beginner`/`ZERO Experience` 2 · `Turned it Around` 1 · `*INSANE*`/`**INSANE**` 5 · `MYSTERY BOX` 3 · `DREAM
[X]` 3 · `+ GIVEAWAY` 1.

**Registro**: FG, documental (`Scientists Found…`, `Ancient Explorers Couldn't Explain`); BM, crónica de viaje en
primera persona; BB, aventura familiar (`with Dad`, `Our`); BZ, emprendedor de internet (`Side Hustle`, `Hamster Wheel`,
`Get Rich Without Getting Lucky`); CC, adolescente entusiasta (`INSANE`, `!!`, `My Fish a Girlfriend`). El `You`
aparece una vez (`the Town that Pays You $50,000`, BM #10) y `Your` una (`Your … Questions Answered`, BZ #42): la
apelación directa es casi nula en esta tanda.

**Cifras y moneda**: `$` delante con coma de millar (`$15,000`); FG abrevia (`$10M`, `$1M`); BM escribe la palabra
(`$15 Billion`, `$100 Billion Dollar`) y usa `£` para lo británico y `€` para Italia; unidades pegadas en BB (`500miles`,
`48hrs`, `6000ft`) y en CC (`2,000G`, `150G`).

**EE. UU., Reino Unido, Australia:**
- **Reino Unido (BM)**: `Holiday` ×4 (en EE. UU. sería *vacation*), `£9.50`, `£100`, `Prime Minister of UK`; el país de
  casa como destino (`Across the UK`, x6,06).
- **Australia (BB)**: `Aussie Outback`, `Bushfoods`, `Bush Medicine`, `Crocodile Dundee`, `Shark Alley`, `with Dad`,
  `our Dad’s fishing`; el país como escenario y como dueño de récords (`Australia's Most Controversial Shipwreck`). Ortografía
  floja (`Worlds` sin apóstrofo ×3, `500miles`).
- **EE. UU. (FG, CC, BZ)**: `Backyard`, `Walmart`, galones (`G`), estados como dueños (`Florida's`, `Texas'`), `Side Hustle`.

**Qué sonaría raro o traducido**: `with Prime Minister of UK` (falta `the`: así suena a no nativo); `Building a
ENCLOSURE` (`an`); `Taking our Dad’s fishing` (`Dads`); `The Secrets to My DAD'S 150G SALTWATER AQUARIUM!! - 10 YEAR OLD
Reef Tank` (dos títulos con guion); `Some books that are pretty good` es ironía deliberada, no error, pero en un título se
lee como desgana.

---

## 7. Malas prácticas y contraejemplos

**Títulos que no dicen nada sin la miniatura**: `The YouTube Hamster Wheel` (BZ #10, x0,39) · `NOT Doing THIS Almost Ruined
My Tide Pool…` (CC #25, x0,51) · `Building a ENCLOSURE for My NEW PET!!` (CC #23, x0,26; el animal solo es una silueta) ·
`The Side of Tokyo Nobody Talks About` (BM #19, x0,42) · `The Ultimate Adventure! (AFRICA UNCUT)` (BB #3, x1,13: sale
en la media gracias al canal, pero no dice qué).

**Relleno o desgaste**:
- `!!` en 32 de 45 títulos de CC y `*INSANE*` en 5: firma, no énfasis (`INSANE` fuera de las ferias, x0,88 y x1,21).
- `Remote` en 12 títulos de BB (mediana x0,85, 4 altos y 4 bajos): ya no distingue.
- `for My [Backyard / Saltwater] Tide Pool` en 10 de CC (mediana x0,78).
- Paréntesis que repiten el título: `Visiting the Town that’s Always Dark (No Sunlight)`; o que son un menú: `(Catch,
  Clean & Cook)`, `(Living & Foraging for Food)`.
- La etiqueta de serie delante: `🇵🇬[EP:N]` ocupa 8–9 caracteres antes del gancho en 8 títulos (mediana x0,94, plano).

**Clickbait de cumplimiento dudoso** (no he visto los vídeos; señalo la promesa): `I Went on Holiday with Prime Minister of
UK` (BM #16, x0,36; la miniatura enseña a alguien parecido a un primer ministro en bañador) · `Wildlife Expert Reacts To
Terrifying Animal Encounters` (FG #25, x0,30; la miniatura, un elefante en un aeropuerto, parece fabricada) · `5 Animals
That Survived The Ice Age` con una bestia gigante en el hielo y `STILL ALIVE?` (FG #9, x0,33) · `7 Mysterious Animals
Caught on Trail Camera` con `PROOF OF CHUPACABRA?` (FG #39, x0,41) · `SURVIVAL CHALLENGE: Plane Crash In Forbidden Jungle`
(BB #41, x3,33: si es una recreación, el título no lo dice). Cuatro de los cinco quedan muy abajo: las miniaturas de FG
con criatura imposible y pregunta (`STILL ALIVE?`, `PROOF OF CHUPACABRA?`, `SHOULDN'T EXIST?`, `LAST PHOTO EVER?`) están
todas en sus 8 peores.

**Demasiado largos**: BB tiene 13 títulos de más de 60 caracteres (mediana de los 12 maduros x1,26, del x0,44 al
x14,91). Funcionan cuando el gancho cabe en los primeros ~60 (`SURVIVAL CHALLENGE: Australia's Most Controversial
Shipwreck` = 60) y lo que se corta es un paréntesis. Fallan cuando el principio es la etiqueta y el gancho va al final
(`🇵🇬[EP:8] 30 Days in Remote PNG (Camping & Spearfishing Our Food)`, 64, x0,66). FG #33 (79 car., x1,49) también pone el
gatillo delante. No puedo ver dónde corta cada pantalla.

**Descuidos**: `Building a ENCLOSURE` (CC #23) · `Worlds Oldest` / `the Worlds Most Dangerous Paradise` sin apóstrofo (BB
#13, #26, #54) · `in 100 days` / `in 100 Days` (CC) · `Nobody's Heard of` / `Nobody’s Heard Of` (BM) · `Prime Minister of
UK` · `Taking our Dad’s fishing` · cinco grafías de episodio entre BB y BZ.

**Repetirse**: FG publica dos veces `5 Animals That Have Only Been Seen Once` (x1,36 y x3,43: la segunda subió) y casi dos
veces `… Deadly Sea Monsters That Actually Exist` (x1,36 → x0,70); BB vuelve a montar como `The Movie` un viaje ya
publicado por episodios (x4,83 → x0,47); BZ numera una serie que cae en cada entrega.

**Los que rompen los patrones y aun así funcionan**:
- `I Took a Sleeper Train Across Europe` (BM #17, x6,67): empieza por `I`, ni cifra ni adjetivo ni mayúsculas ni signo;
  36 caracteres. Todo el peso lo lleva un sustantivo compuesto (`Sleeper Train`).
- `SURVIVAL CHALLENGE: Australia's Most Controversial Shipwreck (No Food, No Water, No Shelter)` (BB #45, x14,91): 92
  caracteres, etiqueta delante, mayúsculas, paréntesis largo. Lo contrario de «corto y una idea».
- `I Bought a Failed Business and Turned it Around` (BZ #11, x4,46): cuenta el final feliz y lleva `and`.
- `Why No Bird, Fish or Mammal Will Cross this Invisible Line` (FG #5, x4,21): una pregunta sin `?` con un `this` que
  remite a la miniatura, la forma que la primera tanda señalaba como floja.
- `I GAVE HIM 25 NEW ANIMALS!!` (CC #31, x2,5): calla al sujeto y lleva `NEW`; lo salva que el sujeto es un creador conocido
  que sale en la miniatura.
- `Buying FISH for My NEW Freshwater STINGRAY Pond!!` (CC #14, x5,66): `NEW` y `for My … Pond`, las dos palabras de relleno
  de la guía, en el tercer mejor vídeo del canal.

---

## 8. Plantillas listas para usar

En Title Case limpio salvo que el creador grite por estilo. Cada una sale de un título real de esta tanda.

### Viaje
1. **`I Took a [Sleeper Train / Night Ferry / First Class Bus] Across [REGION]`** — de `I Took a Sleeper Train Across
   Europe` (BM #17, x6,67; molde 4 de 4 altos). Cuando el vídeo es una experiencia que el espectador podría comprar y se
   mide en una noche o un trayecto. Sin adjetivos: el vehículo es el gancho.
2. **`Visiting the [Town / Island] Where [HECHO FÍSICO IMPOSIBLE]`** — de `Visiting the Town Where the Sun Doesn’t Set`
   (BM #29, x6,88). Cuando el sitio tiene un rasgo que el que mira no ha vivido nunca. El nombre del sitio, a la descripción.
3. **`I Visited the World's [BIGGEST / HOTTEST] [PLACE] Nobody’s Heard Of`** — de BM #26 (x3,47). Solo si las dos mitades
   chocan (récord + desconocido). Con `Secret` en vez del récord, cae (`Italy’s Secret Island Nobody’s Heard of`, x0,3).
4. **`I Stayed at Cheapest vs Most Expensive [Hotel] in [ASPIRATIONAL PLACE]`** — de BM #14 (x3,46). Contraste sin cifras;
   mejor con un destino de deseo que con la ciudad de casa.
5. **`I Visited a Failed $[N] Billion Dollar [Ghost City / Resort]`** — de BM #34 (x3,98). Una pérdida enorme de otros, en
   singular y con la cifra.

### Reto
6. **`SURVIVAL CHALLENGE: [Castaway / Shipwrecked / Plane Crash] on [PLACE]`** — de `SURVIVAL CHALLENGE: Castaway on
   Tropical Island` (BB #22, x4,06). Etiqueta de género delante y un papel de película detrás (9 de 9 altos).
7. **`[ETIQUETA]: [COUNTRY]'s Most [Controversial / Infamous] [EVENT] (No Food, No Water, No Shelter)`** — de BB #45
   (x14,91; la triple privación también en #48, x1,96). Cuando el reto recrea un suceso real; las tres reglas en
   negativo al final.
8. **`I Tried [SKILL / METHOD] for a Week (Complete Beginner)`** — de BZ #39 (x5,62). Para el «lo pruebo por ti» con plazo
   y nivel cero; sin plazo, el `I Tried` cae (x0,39 de mediana).

### Visita a un sitio
9. **`Private Tour of [a / an NATIONALITY] Billionaire’s Secret [UNEXPECTED ANIMAL] Sanctuary`** — de FG #13 (x4,24).
   Acceso con estatus del dueño y un animal que no se espera en ese sitio. Requiere que el que entra tenga crédito
   (CC copió el molde de acceso y se quedó en x0,45).
10. **`Private Tour of [STATE]'s $[N]M [EXACT ANIMAL] [Facility / Backyard Zoo]`** — de FG #23 (x2,53) y #8 (x1,57). Precio
    + animal exacto; nunca `Best` ni `Wildest`.

### Animales
11. **`Face to Face with [COUNTRY]'s Deadliest Animals (Private Tour)`** — de FG #35 (x3,28). Peligro + acceso en una línea.
12. **`Why No [A], [B] or [C] Will Cross this [VISIBLE THING]`** — de FG #5 (x4,21). Misterio natural cuando la cosa se
    puede enseñar en la miniatura (el `this` la señala). Con una ley abstracta, cae (x0,42).
13. **`Buying [ANIMAL] That [IMPOSSIBLE TRAIT] for My [PLACE]`** — de `Buying FISH That WALK ON LAND For My Backyard Tide
    Pool!!` (CC #29, x2,44). Rasgo en vez de adjetivo genérico.
14. **`We Caught & Ate [ANIMAL THE VIEWER WOULDN’T EAT] on a Remote Island`** — de BB #10 (x4,31; también `Kangaroo Catch &
    Cook…`, x3,1). Tabú alimentario con el animal nombrado.

### Construcción o proyecto
15. **`I Built a [THING] for [ANIMALS] in [N] Days`** — de CC #40 (x5,8). Plazo con `in` (antes y después), nunca `for [N]
    days` (aniversario, x0,95).
16. **`I Turned a Regular [THING] Into a [THING]`** / **`I Bought a Crashed [THING] to Make a Profit`** — de BZ #5 (x4,99) y
    #7 (x5,54). Transformación con algo corriente o roto al principio y una meta medible al final.

### Compra o precio
17. **`I Tested Every Budget of [THING]`** — de BZ #1 (x2,91). La escalera de precios sin cifras en el título (la cifra la
    pone la miniatura).

---

## 9. Límites

- **El ratio no es el CTR.** En cada vídeo van juntos título, miniatura, tema, invitado, duración, fecha y algoritmo. La
  pareja de títulos idénticos de FG (#21 x3,43 y #32 x1,36) lo demuestra: con el mismo título, el resultado cambia ×2,5.
- **Edad y crecimiento**: BZ tiene siete años y la mediana se calcula sobre todo el periodo; la época 4 (x2,91) puede
  estar inflada por el crecimiento del canal. BM y BB también suben con el tiempo; FG y CC bajan. He comparado dentro de
  épocas y entre moldes que conviven, pero el sesgo no se elimina.
- **Muestras pequeñas**: muchos moldes tienen 2–5 casos; con eso una mediana es un indicio. Las palabras con n = 3 (`More`,
  `Terrifying`, `Holiday`) son llamativas, no concluyentes.
- **Valores extremos**: BB #45 (x14,91) se sale de escala; por eso uso medianas y recuentos de altos/bajos.
- **Tema confundido con forma**: `Reptile` contra `AQUARIUM` en CC, `India` en FG, `SURVIVAL CHALLENGE` en BB: no puedo
  separar si sube la palabra o el contenido que la palabra anuncia. Probablemente es lo segundo, y por eso la regla útil
  es «nombra lo que de verdad atrae», no «usa esta palabra».
- **Moldes y mecanismos son clasificación mía**, uno por título. Otra persona movería quizá 10–15 títulos; el orden de los
  mecanismos (amenaza y «podría ser yo» arriba, pertenencia y gente desconocida abajo) no cambiaría.
- **Las parejas las he buscado después de ver los ratios**: es lectura a posteriori. Valen como hipótesis que explican una
  diferencia, no como experimento.
- **No he visto los vídeos**: en clickbait dudoso señalo la promesa, no afirmo que no se cumpla. Miniaturas: solo las de
  `extremos.jpg` y la hoja 02 de FG.
- **Cinco canales, tres países, géneros muy distintos.** «Lo propio del inglés» es lo propio de estos cinco.
- `*`: 10 vídeos de menos de 21 días (FG 2, CC 6, BB 2) cuentan en medidas y moldes, fuera de toda mediana.

---

## 10. Contraste con la guía

Contra `base/titulos-miniaturas.md` (§ 1, § 3, § 5) y `base/refs/_youtube/titulos_en.md` (primera tanda: MrBeast, Paul
Cuffaro, Sidemen, Chandler, Brave). La primera tanda era tres canales de animales y dos de retos; esta añade viajes,
supervivencia y negocio, y varias reglas «del inglés» resultan ser reglas de un género.

### Se confirma

| Regla de la guía | Evidencia aquí |
|---|---|
| § 1.4 Concreto gana a genérico | `Private Tour of Florida's $1M Crocodile Facility` x2,53 frente a `…Florida’s Best Backyard Animal Sanctuary` x1,00 (FG); `WALKING FISH` x1,30 frente a `NEW PET` x0,26 y `That WALK ON LAND` x2,44 frente a `EXOTIC SALTWATER` x0,72 (CC); `5 of the Rarest Animals on Earth` x0,35 |
| § 1.3 Se calla el final, nunca el sujeto (en el título) | `Building a ENCLOSURE for My NEW PET!!` x0,26; `I BOUGHT a Live Fish MYSTERY BOX! (What’s Inside?)` x0,36. Excepción con sentido: `I GAVE HIM 25 NEW ANIMALS!!` x2,5, porque el «él» es un creador conocido que está en la miniatura |
| § 1.5 Recopilaciones y «mejores momentos», lo peor; vender el bloque, no la lista | `(The Movie)` frente a `(Ep1)` del mismo viaje: x0,47 frente a x4,83 (BB); recopilaciones `MOVIE` de BB, mediana x0,84; listas de FG, mediana x0,65 y 9 de 18 bajas; meta del canal en BZ, 4 de 4 bajas |
| § 1.6 El tema pesa más que el diseño | la misma frase con `Reptiles` o con `SEA CREATURES`: x3,65 frente a x0,68 (CC); `India` 4 de 4 por encima de x1,4 en FG |
| § 1.8 Lo fabricado queda abajo | las miniaturas de FG con criatura imposible y pregunta (`STILL ALIVE?`, `PROOF OF CHUPACABRA?`, `SHOULDN'T EXIST?`, `LAST PHOTO EVER?`) están las cuatro en sus 8 peores |
| Hueco «¿Cómo es por dentro? (de quién es, privado, secreto)» | FG F1: 13 maduros, mediana x1,42, ninguno bajo; con `Billionaire’s`, 3 de 3 por encima de x1,4 |
| Hueco «¿De verdad es tan…?» | `I Stayed in Hotels that Broke the Internet` x5,02 (BM) |
| § 3 Sin hashtags; frase en minúsculas floja | 0 hashtags en 223; `Some books that are pretty good` x0,27 (n = 1) |
| § 5 «vs» abreviado | `Cheapest vs Most Expensive` ×3 |
| § 5 `THIS` sin nombre no sube | `NOT Doing THIS Almost Ruined My Tide Pool…` x0,51. Con nombre detrás funciona: `this Invisible Line` x4,21 |
| § 5 `for My POND` en todos no distingue | `for My … Tide Pool`, 10 maduros, mediana x0,78 (CC) |
| Primera tanda: repetir la premisa va a menos | `… Deadly Sea Monsters That Actually Exist` x1,36 → x0,70; hoteles x3,46 → x1,84 → x1,19; Millionaire EP. 1 → EP. 5 |

### Se contradice o hay que matizar

| Regla de la guía | Lo que se ve aquí | Cómo reescribirla |
|---|---|---|
| § 3 «Objetivo ≤ 55 caracteres; nunca más de 60» | BB tiene 13 de más de 60, mediana x1,26 (12 maduros); el récord de la tanda mide 92 (x14,91); el tercil largo es el mejor en FG (x1,27), BM (x1,66), BB (x1,61) y BZ (x1,42), y ningún canal castiga lo largo | «El **gancho** cabe en los primeros 55 caracteres; detrás puede ir lo que sobre (paréntesis, reglas). Lo que falla es la etiqueta o el episodio delante y el gancho al final» |
| § 3 «Empieza por lo que engancha» | en títulos cortos la posición da igual: el gatillo de los mejores de BM va al final (`…Where the Sun Doesn’t Set`, `…that Broke the Internet`); en largos sí importa (FG #33, 79 car., gatillo en p. 2–3) | «En títulos de más de ~50 caracteres, el gatillo antes del corte; en cortos, donde suene natural» |
| § 3 «Una sola idea. Si necesita "y", son dos títulos» | `I Bought a Failed Business and Turned it Around` x4,46; `I Built a Camper and Got Attacked` x2,7; `We Caught & Ate Flying Fox…` x4,31. Falla el `&` que suma tareas: `GIANT CRAB HUNTING & Spearfishing…` x0,49, `(Catch, Clean & Cook)` x0,43 | «`and` de consecuencia (hice X **y** pasó Y) sí; `&` de lista de actividades, no» |
| § 3 «Cifras con dígitos y que midan algo (plazo, precio, cantidad…)» | con dígito rinden **menos** que sin él en FG (x0,78 / x1,23), BB (x0,84 / x1,44), BM (x0,83 / x1,02) y BZ (x0,86 / x1,06); solo CC al revés. Lo que baja es la cifra que mide **cuánto contenido** hay (`5 Animals…`, `30 Days Living…`) | «La cifra tiene que medir **lo que está en juego** (precio, desproporción, plazo con resultado: `$1M`, `$100 Billion`, `in 100 Days`), no la cantidad de contenido (`5 …`, `14 Days …`)» |
| § 3 «Sin emojis» (0 en 352) | BB lleva 12: 8 banderas de serie (mediana x0,94, neutro) y 4 sueltos (x2,52, x3,33, x1,98, x0,29), todos sobre moldes que ya rinden | regla por defecto, pero sin evidencia de que un emoji castigue; no es «nunca» |
| § 3 «Series: el nombre de la serie detrás, nunca delante» | `SURVIVAL CHALLENGE:` delante, 9 de 9 altos; `🇵🇬[EP:N]` delante, plano (x0,94) | «Delante puede ir una **etiqueta de género** que promete (`SURVIVAL CHALLENGE:`); el número de episodio, detrás o fuera». Añadir: la serie numerada cae entrega a entrega (BZ, BB) |
| § 3 «No se adelanta quién gana ni cómo termina» | `…and Turned it Around` (éxito contado) x4,46; la miniatura de `I Tried Forex Day Trading…` (x5,62) enseña la pérdida | «En contenido de **método** (negocio, aprender algo) se puede contar el resultado: la pregunta pasa a ser "¿cómo?", que es lo que ese público viene a buscar» |
| § 1.7 «Lo barato o gratis gana; lo caro, abajo» | los presupuestos mínimos de BM caen (`£9.50 Holiday` x0,66, `for £100?` x0,54); el contraste barato/caro sube (x1,84) y lo carísimo sube si es una pérdida (`Failed $100 Billion…` x3,98) o un objeto roto (`Crashed Supercar`, `Crashed Lamborghini`, x5,54 y x4,57) | «Barato vende como **objeto** (un coche, un hotel); como presupuesto abstracto, no. Caro vende como **pérdida** o como **transformación**» |
| Hueco «Enséñamelo… (no hay nadie)» | la ausencia hunde en BM: `World's Emptiest Country` x0,17, `Most Isolated Island…` x0,41, `Italy’s Secret Island Nobody’s Heard of` x0,3 (miniatura `0 VISITORS`), `…Nobody Talks About` x0,42 | «El vacío solo vende si contradice algo famoso (Qatar tras el Mundial) o un récord (`World's Biggest City Nobody’s Heard Of`, x3,47). Vacío a secas = nada que ver» |
| Hueco «¿Cuál gana? con cifra (1 $ contra 1.000 $)» y primera tanda: «sin cifras, la más baja» | `I Stayed at Cheapest vs Most Expensive Hotel in…`, sin una cifra, 3 de 3 por encima de x1,19; `I Tested Every Budget of Sports Car` x2,91 | «Con un objeto concreto (hotel, deportivo) los superlativos `Cheapest`/`Most Expensive` hacen el trabajo de las cifras; la cifra puede ir en la miniatura» |
| § 5 «Telegráfico… Solo el 16 % empieza por I» (y en MrBeast `I` rinde menos) | BM: 28 de 36 empiezan por `I`, mediana x1,11 frente a x0,49 del resto; BZ: 25 de 42, x1,53 frente a x0,69 | «En canales de experiencia propia (viaje, prueba, compra-reventa) `I` + pasado es lo natural y lo que mejor sale; lo telegráfico es de animales y concursos. **Lo que decide es el verbo**, no el pronombre» (ver nuevas reglas) |
| § 5 «Title Case + una o dos palabras EN MAYÚSCULAS» | FG, BM y BZ: 118 de 119 sin una palabra gritada (son los tres canales con más visitas de la tanda: medianas de 2,04 M, 848 k y 630 k); en CC, Title Case + mayúsculas x0,76 (31) frente a limpio x1,17 (4); en BB, palabras gritadas fuera de `SURVIVAL CHALLENGE`, x1,06 (16), igual que el canal | «Title Case limpio por defecto; las mayúsculas, solo si son el estilo del creador. No hay evidencia en ninguna de las dos tandas de que gritar suba» |
| § 5 «Un "!" al final en vídeos de animales (87–90 %)» | FG, canal de animales, 0 de 41; BM, 0 de 36. CC lo pone en 40 de 45 | «El "!" es estilo de casa, no del género. Sin él no se pierde nada» |
| § 5 «Paréntesis final con el giro, la magnitud o el aviso» | BB: 28 maduros con paréntesis, x0,94, frente a x1,22 sin él. Suben los que añaden algo nuevo: `(No Food, No Water, No Shelter)` x14,91 y x1,96, `(436 Kills)` x1,33, `(Complete Beginner)` x5,62, `(Private Tour)` x3,28 y x1,99; bajan los que dan el menú o el formato: `(Catch, Clean & Cook)` x0,43, `(My honest thoughts)` x0,35, `(THE MOVIE!)` x0,84 | «El paréntesis tiene que añadir una regla, una cifra de riesgo o un nivel; nunca el menú del vídeo ni cómo está montado» |
| § 5 «Cifras: todos los ceros, nunca `$250K` ni `$1M`» | FG: `$10M` ×2 y `$1M` (x1,57, x0,91, x2,53) | «Abreviar está bien (y ahorra caracteres); lo que cuenta es que la cifra esté y sea desproporcionada» |
| § 5 «Relleno que no sube nunca: `NEW`» | CC: `Buying FISH for My NEW Freshwater STINGRAY Pond!!` x5,66; `I GAVE HIM 25 NEW ANIMALS!!` x2,5; mediana de `NEW` en CC x1,06 (6) | «`NEW` pegado al animal (`NEW FISH`, `NEW PET`) no vende; pegado a un **sitio nuevo** o a una cantidad, no estorba. Nunca es el gancho» |
| Molde `Exploring [PLACE] FULL of [CATEGORY]!!` (Paul x3,42) | CC: `Exploring an INSANE ZOO Full of EXOTIC ANIMALS!!` x0,31; la copia literal del título de Paul, x0,88 frente a x2,68 | «El acceso necesita dueño con estatus o cifra (`Billionaire’s`, `$1M`) y un presentador con crédito para entrar. Sin eso es una visita a un zoo» |
| Tabla español/inglés: «Qué se calla — ES: el nombre del sitio; EN: el resultado» | BM, en inglés, no nombra el sitio en 36 de 36 y su molde de rasgo (B2) es de los mejores (x1,46) | «Callar el nombre y decir el rasgo es regla del **viaje**, no del español». Pasarla también al § 5 |
| Tabla español/inglés: «Palanca más usada en EN: la cifra y el riesgo en carne propia» | el riesgo personal no destaca aquí (`The Closest Call I’ve Ever Had With Death` x0,78, `I Tried America’s Most Dangerous Wildlife Job` x0,78, `3 Closest Calls…` x0,59); la amenaza que sube es **escenario** (náufrago, avioneta) o **animal** (`Deadliest`) | «El riesgo vende como situación que el que mira se imagina viviendo, más que como herida del presentador (eso es la marca de Brave)» |
| § 1.3 Siluetas con «?» en la miniatura no pasan de x1,26 (Paul) | las tres mejores de CC (x7,11, x5,66, x3,65) llevan silueta con `?`; también la peor (x0,26) | «La silueta puede ser **una** pieza entre muchas que sí se ven y con precio (la feria); como contenido único, no» (es de miniatura, lo apunto porque choca) |

### Lo que NO está en la guía y se ve aquí (reglas aplicables, con evidencia)

1. **El verbo decide: experiencia con duración o compromiso, no presencia ni intento.** `I Took` (5, x3,96, 4 altos, 0
   bajos), `I Stayed` (4, x2,65), `I Bought` en BZ (4, x2,73), `Turned … Into`/`Rebuilt`/`Built` en BZ (x4,99, x4,57,
   x2,70) frente a `I Visited` (15, x0,76, 6 bajos) e `I Tried` (8, x0,65, 4 bajos). Regla: antes de escribir `Visited`
   o `Tried`, busca el verbo de lo que de verdad hiciste (dormir, comprar, reconstruir, cruzar).
2. **Paradoja dentro del propio título**: dos mitades que chocan. `World's Biggest City` + `Nobody’s Heard Of` (x3,47),
   `Extinct` + `in Real Life` (x1,39), `$10M` + `Backyard Zoo` (x1,57), `First Class` + `Bus` (x3,68), `Lamborghini` +
   `My Garage` (x4,57), `Regular Car` + `Into a Camper` (x4,99), `ONE Giant Fish` + `Entire Village` (x2,77), `FISH` +
   `WALK ON LAND` (x2,44): 8 de 8 por encima de x1,39 (seleccionados por mí, a posteriori). La versión redundante, en la
   que las dos mitades dicen lo mismo, cae: `Secret Island` + `Nobody’s Heard of` (x0,30). Regla: si las dos mitades del
   título dicen lo mismo, cambia una hasta que se contradigan.
3. **Superlativo físico o visible, nunca de ausencia ni de opinión.** Suben `Hottest` (x1,75), `Biggest` (x3,47),
   `Deadliest` (3, x1,99), `World's Largest` (x7,11); caen `Emptiest` (x0,17), `Most Isolated` (x0,41), `Rudest`
   (x0,28), `Strictest` (x0,75), `Rarest` (x0,35), `Wildest` (x0,69), `Best` (x1,00). La guía dice «superlativo sin prueba
   abajo»; falta decir qué superlativo es una prueba en sí.
4. **El dueño del superlativo marca la escala**: `World's Largest Reptile Expo` x7,11 > `America's Largest…` x2,90 >
   `THIS HUGE…` x1,81 > `this INSANE…` x1,05 (CC). En FG, `Billionaire’s` (3, x1,49, ninguno bajo) > posesivo de estado
   (`Florida's`, `California's`…: 7, x1,00).
5. **Etiqueta de género + papel de película** (`SURVIVAL CHALLENGE: Castaway / Shipwrecked / Plane Crash / The Real
   Crocodile Dundee`): 9 de 9 altos, mediana x3,33. El papel (`Castaway`, x4,06) gana a la tarea (`Hand Catching Food`,
   x2,75). Plantilla para cualquier reto de aguante.
6. **La regla en tríada negativa**: `(No Food, No Water, No Shelter)`, 2 de 2 altos (x14,91 y x1,96). Tres negaciones
   cortas hacen de la regla un reto medible contra uno mismo.
7. **Adjetivo que ordena la emoción = abajo**: `Terrifying` 3 de 3 bajos (FG), `Mysterious` x0,41, `INSANE ZOO` x0,31,
   `my DREAM AQUARIUM` x0,28. El adjetivo dice qué sentir en vez de dar el hecho que lo provoca.
8. **Secuela anunciada = bajada; molde repetido con sustantivo nuevo = aguanta.** `More` 3 de 3 bajos (FG); `(The Movie)`
   x0,47 tras `(Ep1)` x4,83; `Millionaire … EP. 1 → 5` de x1,50 a x0,45; la misma frase en EP:1 y EP:5 (x1,65 → x0,51);
   `for 365 days` tras `in 100 days` (x0,95 tras x5,80). En cambio los cuatro trenes de BM (x3,68–6,67), las ferias de CC y
   `Only Been Seen Once` (que subió la segunda vez) se repiten sin decir que son repetición. Regla: nunca `More`, `Part 2`,
   `The Movie` ni número en el título; repite el molde con otro país, otro vehículo, otro animal.
9. **Plazo de transformación, no de estancia.** `in 100 Days` (x5,80 y x1,31), `for a Week` con un resultado que medir
   (x1,74 y x5,62) frente a `[N] Days Living with / in` (BB K2: 19 maduros, x0,74). La guía tiene en español `[N] Días
   [Entre / Con] [X]` como molde bueno («21 Días Entre Millonarios», x3,78): aquí es el suelo del canal, salvo cuando el
   «con quién» es un récord o un mundo deseado (`…The Worlds Oldest Living Culture (Ep1)`, x4,83). Matizarlo.
10. **Tabú alimentario**: comer lo que el que mira no comería. `We Caught & Ate Flying Fox…` x4,31, `Kangaroo Catch &
    Cook…` x3,10, `RARE GIANT CRAB…` x2,50 frente a `GIANT TUNA…` x0,63 y `Lobsters & Coconuts for Christmas` x0,35.
11. **«Lo pruebo por ti»**: el creador como conejillo de algo que el espectador podría hacer, con plazo y nivel cero.
    `(Complete Beginner)` x5,62, `Regular Car` x4,99, `Money Making Apps` x2,98, `… for Me` x1,99 y x1,89, `Sleeper
    Train` (BM). Mecanismo con mediana x1,64 en 18 maduros. Falla fuera del tema del canal (`ZERO Experience` en moto,
    x0,38) y sin plazo (`I Tried the Instacart Side Hustle`, x0,40). La guía solo tiene la apelación directa (`You`), que
    aquí casi no aparece (2 títulos).
12. **Gente desconocida baja; creador conocido sube.** BM con personas (`Complete Stranger`, `Prime Minister of UK`,
    `Bajau People`): 3 de 3 por debajo de x0,4. CC con otros creadores (`FINATIC`, `PAUL CUFFARO`, `HIM`): 3 maduros, ninguno
    por debajo de x1,46. La guía habla de famosos; falta: un desconocido en el título resta, y en un canal pequeño el
    nombre de un creador mayor es autoridad prestada.
13. **Copiar un molde de otro canal no copia el resultado.** CC usa el `Buying … for My [PLACE]!!` y el `Exploring PRIVATE
    … FULL of EXOTIC ANIMALS` de Paul Cuffaro: x0,79 y x0,45 de mediana (el segundo, letra por letra, x0,88 frente a x2,68).
    Las plantillas del § 8 son puntos de partida, no fórmulas: el acceso exige crédito; la rutina exige un público que ya
    quiere al animal.
14. **El mismo título puede dar ×2,5**: `5 Animals That Have Only Been Seen Once` (FG #32 x1,36, #21 x3,43; cambia la
    miniatura). Una buena regla de título pone el techo; no garantiza llegar a él.
15. **Singular gana a plural** (indicio débil): `Island` x1,87 (10) frente a `Islands` x0,48 (3) en BB; `a Failed … Ghost
    City` x3,98 frente a `China’s … Fake Cities` x0,46 en BM. Un sitio es una historia; varios, un itinerario.
16. **Prueba social** (un solo caso, apuntarlo como hipótesis): `I Stayed in Hotels that Broke the Internet` x5,02. Lo viral
    como garantía de interés y con la duda «¿es para tanto?» incluida.

### Lo que habría que cambiar en la guía, en corto
- § 3: la longitud se mide por la posición del gancho, no por el total; la cifra mide lo que está en juego, no la
  cantidad de contenido; `and` de consecuencia sí; etiqueta de género delante sí; emojis «no aportan», no «nunca».
- § 5: separar «inglés de animales y concursos» (telegráfico, gerundio, `!`) de «inglés de experiencia propia» (`I` +
  verbo de compromiso, sitio sin nombre + relativa, Title Case limpio, sin `!`). Quitar el «nunca» de `NEW` y de `$1M`.
  Añadir los moldes `I Took a [VEHICLE] Across [REGION]`, `Visiting the Town Where [IMPOSSIBLE]`, `I Stayed at Cheapest vs
  Most Expensive [X] in [Y]`, `SURVIVAL CHALLENGE: [ROLE] on [PLACE]`, `Private Tour of [a NATIONALITY] Billionaire’s
  Secret [UNEXPECTED ANIMAL] Sanctuary`, `I Bought a Crashed [X] to Make a Profit`, `I Tried [X] for a Week (Complete
  Beginner)`.
- § 1 (huecos): añadir «¿Me serviría a mí?» (el creador lo prueba por ti) y «¿Cómo puede ser?» (paradoja en el propio
  título); matizar «Enséñamelo (no hay nadie)».
- Lista de prohibidos nueva: `More`, `Part 2`, `(The Movie)`, `Terrifying`/`Mysterious` como gancho, superlativos de
  ausencia (`Emptiest`, `Most Isolated`) y de opinión (`Best`, `Rudest`), `I Visited`/`I Tried` cuando hay un verbo mejor,
  personas que el público no conoce como sujeto.

