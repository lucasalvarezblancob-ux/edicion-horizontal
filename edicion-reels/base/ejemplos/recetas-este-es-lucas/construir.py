# Construye versiones.json (formato de ../rutinas-este-es-lucas/Rutinas.tsx) a partir de guiones.json + el reparto de tomas.
# Toma: "clip a b [z] [origen] [fijo] [r=0.75]"; los clips de stock van en stock/<nombre>.
import json, re
g = json.load(open("guiones.json"))
PEXP = {"r1847": 0.85, "r8005": 0.85, "r5007": 0.85}  # clips de Lucas con cielo/sol bajo los subtítulos (p90 145–174)
EXP = json.load(open("exposicion.json"))  # medida en la franja de subtítulos (p90 ≥145 → 0,85; ≥175 → 0,80)
cab = {}
def T(spec):
    out = []
    for x in spec.split(","):
        p = x.split(); c = p[0]
        t = {"c": c if re.match(r"^[a-z]\d{4}$", c) else "stock/" + c, "a": float(p[1]), "b": float(p[2])}
        for q in p[3:]:
            if q == "fijo": t["fijo"] = True
            elif q.startswith("r="): t["r"] = float(q[2:])
            elif q.startswith("z="): t["z"] = float(q[2:])
            elif q.startswith("o="): t["o"] = q[2:].replace("_", " ")
        if t["c"].startswith("stock/") and c in EXP: t["exp"] = EXP[c]
        if c in PEXP: t["exp"] = PEXP[c]
        out.append(t)
    return out
G1 = "este es lucas y hoy te va a enseñar".split()
R = {
 "r01-tortitas-avena-platano": ((560,540), ["l2880 0.6 2.6 fijo", "tortitas-miel-1 5 25,frutos-rojos-1 8 30",
   "avena-vertiendo-1 0.3 6,platano-cortando-2 0.5 11,huevo-rompiendo-1 0.5 9.5", "batidora-masa-1 3 14",
   "aceite-oliva-1 0.5 13,tortita-sarten-1 5 20,tortita-sarten-2 3.8 8", "frutos-rojos-1 5 30,tortitas-miel-1 5 25",
   "tortitas-miel-1 12 25,r8005 3.8 6.2 fijo", "l2880 5.8 8.0 r=0.75"]),
 "r02-bowl-pollo-teriyaki": ((420,800), ["f6116 4.0 5.6 fijo", "arroz-2 0 6,c1086 10.5 17 z=1.1,bowl-emplatado-1 2 8",
   "pollo-cortando-2 0 12,pollo-sarten-2 0 14,pollo-cortando-1 0 6", "soja-vertiendo-2 0 15,miel-vertiendo-1 4 10,ajo-cebolla-1 0 20",
   "arroz-1 0 4,brocoli-2 0 58", "bowl-emplatado-1 2 8,sesamo-1 0 10.8,arroz-2 0 6,soja-vertiendo-1 1 3.7",
   "arroz-2 0 6,f6116 13.4 14.6 fijo", "f6116 18.3 20.3 r=0.8"]),
 "r03-avena-nocturna": ((240,760), ["r5007 2.0 3.8 fijo", "avena-tarro-1 2 11,yogur-cuchara-2 2 12",
   "avena-tarro-2 4 11,yogur-cuchara-1 0 10,leche-vertiendo-1 5 25", "chia-1 4 14", "avena-tarro-1 3 11,nevera-abriendo-1 0 3",
   "frutos-rojos-1 5 30,yogur-cuchara-2 2 12", "r5007 8 10 fijo,yogur-cuchara-2 4 12", "r5007 2.0 3.8 r=0.75"]),
 "r04-pasta-atun-tomate": ((300,420), ["r1847 2.2 4.2 fijo", "tomate-salsa-2 28 35,r1847 5 13,plato-pasta-1 0 8.8",
   "pasta-hirviendo-1 0 8", "ajo-cebolla-2 0 10,aceite-oliva-1 0 13", "tomate-salsa-1 0 7,atun-lata-1 0 21",
   "tomate-salsa-2 0 25,queso-rallando-1 0 14,plato-pasta-1 0 8.8", "r1847 8 13,plato-pasta-2 0 10", "r8005 3.8 6.2 r=0.75"]),
 "r05-tortilla-claras-espinacas": ((420,800), ["f6116 9.0 10.6 fijo", "tortilla-francesa-1 0 12,c1048 8 9.2 fijo",
   "claras-separando-1 0 8,batir-huevos-2 0 12,claras-separando-2 0 17", "cocina-ambiente-1 0 15,aceite-oliva-1 0 13",
   "tortilla-francesa-2 0 6,tortilla-francesa-1 0 12,tostada-pan-2 3 6", "tortilla-francesa-1 2 12,c1048 8 9.2 fijo z=1.1",
   "c1048 12 14.5 r=0.8"]),
 "r06-salmon-al-horno": ((570,560), ["c1037 1.27 2.9 fijo", "salmon-emplatado-1 0 30,c1086 10.5 17 z=1.1",
   "patata-cortando-2 0 37", "salmon-crudo-1 1 4,limon-1 0 46,salmon-crudo-2 0 4",
   ("Unos espárragos al lado, aceite de oliva por encima y todo a la bandeja.", "bowl-emplatado-1 2 8,aceite-oliva-1 0 13,horno-bandeja-1 3 10"),
   ("Veinte minutos a doscientos grados, que es justo lo que tarda en ducharse.", "horno-bandeja-2 3 10,k1020 1 9"),
   "salmon-emplatado-1 5 30,c1037 5.27 9.5", "c1037 6.57 9.6 r=0.75"]),
 "r07-batido-post-entreno": ((600,580), ["r0313 0.8 2.6 fijo", "batido-vertiendo-1 5 20,chia-1 4 14",
   "platano-batidora-1 0 10,proteina-cacito-1 0 6,leche-vertiendo-2 2 7", "crema-cacahuete-1 0 10",
   "batidora-masa-2 0 12,batido-vertiendo-1 5 20,d2019 15 19 fijo", "d2019 15.5 19.5 fijo,r0313 3 8", "r0313 8 11 r=0.75"]),
 "d01-dia-maraton": ((450,600), ["p7629 0.2 2.6 fijo", "p7629 8 30 z=1.1",
   "tostada-pan-2 3 6,huevos-revueltos-2 0 10,cafe-cafetera-2 0 10", "platano-cortando-1 0 12,datiles-1 0.5 4.8,c1086 0.5 8",
   "pasta-hirviendo-1 0 8,tomate-salsa-2 0 25,plato-pasta-2 0 10", "yogur-cuchara-2 2 12,frutos-rojos-1 5 30",
   "salmon-emplatado-1 0 30,patata-cortando-1 0 21", "c1092 1 9.5,p7629 15 30 z=1.1", "c1092 10.3 11.26 r=0.45"]),
 "d02-dia-definir-sin-hambre": ((550,590), ["c1048 2.9 4.3 fijo", "c1048 13.3 14.7 fijo z=1.35 o=50%_62%,claras-separando-2 0 17",
   "claras-separando-2 0 17,tortilla-francesa-1 0 12,tostada-pan-1 1 4", "kiwi-1 3 15,frutos-secos-1 3 15",
   "ensalada-pollo-1 0 11,pollo-sarten-1 0 12", "yogur-cuchara-2 2 12,frutos-rojos-1 5 30", "salmon-emplatado-1 0 30,bowl-emplatado-1 2 8",
   "agua-vaso-1 4 9,f6116 13.4 14.6 fijo,agua-vaso-2 0 6", "c1048 8 9.2 fijo z=1.1,c1048 12 14.5", "c1048 12 14.8 r=0.75"]),
 "d03-dia-menos-de-5-euros": ((420,800), ["f6116 4.0 5.6 fijo", "bolsa-compra-2 0 17,supermercado-carro-1 0 10",
   "avena-vertiendo-1 0.3 6,platano-cortando-2 0.5 11,leche-vertiendo-1 5 25", "arroz-1 0 4,huevo-rompiendo-2 0 13,atun-lata-1 0 21",
   "yogur-cuchara-1 0 10,fruta-cortando-1 0 10.9", "batir-huevos-1 0 10,tortilla-francesa-1 0 12,tostada-pan-2 3 6",
   "supermercado-carro-1 0 10,bolsa-compra-1 0 13", "f6116 8.5 12.5,tupper-meal-prep-1 0 13", "f6116 18.3 20.3 r=0.8"]),
 "d04-dia-entreno-doble": ((810,640), ["c1085 1.0 2.6 fijo", "r1847 5 13,c1086 10.5 17 z=1.1",
   "avena-tarro-1 2 11,frutos-rojos-1 5 30", "c1092 1 9.5,batido-vertiendo-1 5 20", "pollo-sarten-2 0 14,arroz-1 0 4,brocoli-2 0 58",
   "tostada-pan-1 1 4,miel-vertiendo-1 4 10,r1847 2 13", "pasta-hirviendo-1 0 8,plato-pasta-1 0 8.8",
   "r8005 3.8 6.2 fijo,c1085 22 32", "c1092 10.3 11.26 r=0.45"]),
 "d05-dia-de-descanso": ((560,540), ["l2880 0.6 2.6 fijo", "cafe-cafetera-1 0 17,l2880 3 5.5 fijo",
   "tostada-aguacate-2 3 20,cafe-cafetera-2 0 10,l2880 5.8 8 fijo", "arroz-2 0 6,pollo-cortando-1 0 6,brocoli-1 20 45",
   "tortita-sarten-1 5 20,tortitas-miel-1 5 25", "salmon-crudo-1 1 4,ensalada-pollo-2 0 11,salmon-emplatado-1 5 30",
   "k1020 0.5 11", "l2880 3 5.5 fijo,cafe-cafetera-2 0 10", "l2880 5.8 8.0 r=0.75"]),
}
out = {}
for k, ver in g.items():
    (cx, cy), specs = R[k]
    segs = []
    s0 = ver["segs"][0]["txt"].split()
    assert [w.lower().strip(",") for w in s0[:9]] == G1, k
    segs.append({"txt": " ".join(s0[:9]), "tomas": T(specs[0]), "dur": 2.0})
    segs.append({"txt": " ".join(s0[9:]), "tomas": T(specs[1]), "titulo": True, "dur": 1.4})
    si = 2
    for s in ver["segs"][1:]:
        sp = specs[si]
        if isinstance(sp, tuple):  # segmento partido en varios
            partes = [specs[si]]
            while si + 1 < len(specs) and isinstance(specs[si + 1], tuple): si += 1; partes.append(specs[si])
            assert " ".join(p[0] for p in partes) == s["txt"], (k, s["txt"])
            for txt, spec in partes:
                d = {"txt": txt, "tomas": T(spec)}
                if "b" in s: d["b"] = s["b"]
                segs.append(d)
        else:
            d = {"txt": s["txt"], "tomas": T(sp)}
            for f in ("b", "cierre"):
                if f in s: d[f] = s[f]
            if s is ver["segs"][-2] and "b" not in s: d["dur"] = 1.6
            segs.append(d)
        si += 1
    assert si == len(specs), (k, si, len(specs))
    assert " ".join(x["txt"] for x in segs) == " ".join(x["txt"] for x in ver["segs"]), k
    out[k] = {"titulo": ver["titulo"], "cabeza": {"x": cx, "y": cy}, "claves": ver["claves"], "bloques": ver["bloques"], "segs": segs, "dur": 1.5}
json.dump(out, open("versiones.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(out))
