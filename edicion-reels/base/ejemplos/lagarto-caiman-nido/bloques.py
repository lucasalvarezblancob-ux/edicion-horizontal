# Genera tiempos.json (bloques palabra a palabra + momentos clave) desde palabras-alineadas.json (alineación forzada MMS_FA).
# Cada palabra entra en el frame EXACTO en que se dice; cada bloque dura hasta que empieza a decirse el siguiente.
# Uso: herramientas/.venv/bin/python src/videos/lagarto-caiman-nido/bloques.py   (desde estudio/)
import json, os, re
D = os.path.dirname(os.path.abspath(__file__)); FPS = 30
A = json.load(open(os.path.join(D, "palabras-alineadas.json"), encoding="utf-8"))
f = lambda i: round(A[i]["start"] * FPS)
# Esquema: bloques → líneas (estilo, índices de palabra). r = relleno (crema), f = fuerte (Anton lima), m = remate (cursiva)
Y, Y_CTA = 0.665, 0.6
ESQ = [
    (Y, [("r", [0, 1, 2, 3]), ("f", [4, 5])]),                              # casi nadie ha visto / UN NIDO
    (Y, [("r", [6, 7, 8]), ("m", [9, 10, 11])]),                            # de esta especie / en la naturaleza
    (Y, [("r", [12, 13, 14, 15, 16]), ("r", [17, 18, 19, 20]), ("f", [21])]),  # y el que se encontró / estaba dentro de un / TERMITERO
    (Y, [("r", [22, 23]), ("m", [24])]),                                    # dos huevos / escondidos
    (Y, [("r", [25, 26, 27, 28, 29]), ("f", [30])]),                        # dentro de un nido de / TERMITAS
    (Y, [("r", [31, 32, 33, 34]), ("m", [35, 36]), ("m", [37, 38])]),       # de este lagarto sabemos / cómo come, / cómo nada
    (Y, [("r", [39, 40]), ("f", [41, 42]), ("m", [43, 44])]),               # pero casi / NO SABEMOS / cómo nace
    (Y, [("r", [45]), ("f", [46]), ("r", [47, 48, 49, 50])]),               # en / ECUADOR / se registró un caso
    (Y, [("r", [51, 52, 53, 54]), ("m", [55]), ("r", [56, 57]), ("f", [58])]),  # dos huevos en una / cavidad / de un / TERMITERO
    (Y, [("r", [59, 60, 61]), ("r", [62, 63]), ("f", [64])]),               # a las orillas / de un / RÍO
    (Y, [("r", [65, 66, 67]), ("f", [68]), ("r", [69])]),                   # es de los / POQUÍSIMOS / datos
    (Y, [("r", [70, 71, 72]), ("m", [73, 74])]),                            # de cómo crían / en libertad
    (Y, [("m", [75, 76]), ("f", [77, 78, 79])]),                            # en cautividad / SE SABE MÁS
    (Y, [("r", [80, 81]), ("f", [82, 83, 84]), ("m", [85])]),               # ponen entre / 4 Y 7 / huevos
    (Y, [("r", [86, 87, 88]), ("f", [89, 90, 91, 92]), ("m", [93, 94])]),   # y tardan unos / 5 MESES Y MEDIO / en nacer
    (Y, [("r", [95, 96, 97]), ("r", [98, 99, 100]), ("f", [101])]),         # pero la selva / sigue siendo un / MISTERIO
    (Y, [("r", [102, 103]), ("r", [104, 105]), ("m", [106, 107]), ("f", [108])]),  # ¿te imaginas / encontrar esto / en el / AMAZONAS?
    (Y_CTA, [("m", [109]), ("r", [110, 111, 112])]),                        # cuéntamelo / en comentarios y
    (Y_CTA, [("f", [113]), ("r", [114, 115, 116, 117]), ("m", [118])]),     # SÍGUEME / para conocer mejor a / Zafira
]
TEXTO = {30: "termitas"}   # lo que se escribe distinto de la transcripción
ESTILO = {"r": "relleno", "f": "fuerte", "m": "remate"}
usados = [i for _, ls in ESQ for _, ids in ls for i in ids]
assert usados == list(range(len(A))), "el esquema tiene que usar todas las palabras, en orden"
def txt(i, est):
    t = TEXTO.get(i, A[i]["w"]).replace(".", "").lower()
    if i == 118: t = "Zafira"
    return t.upper() if est == "f" else t
bloques = []
for k, (y, lineas) in enumerate(ESQ):
    pal = []
    for est, ids in lineas:
        for n, i in enumerate(ids):
            pal.append({"texto": txt(i, est), "desde": f(i), "estilo": ESTILO[est], "salto": n == 0 and bool(pal)})
    bloques.append({"desde": pal[0]["desde"], "hasta": 0, "y": y, "palabras": pal})
for k in range(len(bloques)): bloques[k]["hasta"] = bloques[k + 1]["desde"] if k + 1 < len(bloques) else 99999
momentos = {"especie": f(8), "termitero": f(21), "nace": f(44), "poquisimos": f(68), "misterio": f(101), "sigueme": f(113)}
json.dump({"bloques": bloques, "momentos": momentos}, open(os.path.join(D, "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(bloques), "bloques ·", momentos)
