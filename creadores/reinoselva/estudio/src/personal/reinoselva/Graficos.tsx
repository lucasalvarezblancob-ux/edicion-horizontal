import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useVideoConfig } from "remotion";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import { loadFont as loadMontserrat } from "@remotion/google-fonts/Montserrat";
import { borde, Clip, Item, pop } from "../../comun/Graficos";
import { ACENTO, F_ANCHA, F_TXT } from "../../comun/marca";

// Gráficos PROPIOS de Reino Selva (LOCAL: la skill no los pisa). Se piden en plan.py con
//   PROPIOS = [(ancla, segundos, "tortuga", {"anim": "senalando", "txt": "…"}), (ancla, segundos, "logo_intro")]
// Qué es cada uno, qué animación va con qué comentario y cuándo se usa: personal/reinoselva/recursos.md.
// Archivos: estudio/public/personal/reinoselva/ (animaciones sin fondo hechas con herramientas/quitar_fondo.py).
const F_IMPACTO = loadAnton("normal", { weights: ["400"], subsets: ["latin", "latin-ext"] }).fontFamily;
const F_REDONDA = loadMontserrat("normal", { weights: ["800"], subsets: ["latin", "latin-ext"] }).fontFamily;
const DIR = "personal/reinoselva/";

// Animaciones de la tortuga. caja = lo que deja quitar_fondo.py; lienzo = [x, y, lado] del cuadrado original en que se
// mueve; desde = segundo en que ya ha dejado la pose inicial (todas arrancan sentadas y se transforman en ~1 s);
// baja = parte del lienzo que queda por debajo del borde de la pantalla (asoma desde abajo, como en sus vídeos).
type Anim = { caja: { w: number; h: number; x: number; y: number }; lienzo: [number, number, number]; desde: number; vel?: number; baja?: number };
export const TORTUGA: Record<string, Anim> = {
  // senalando: el original señala (0–1 s), bota un balón que le rebota en la cabeza (1–4,75 s) y luego se encoge de hombros y
  // guiña, ya sin balón. Solo vale ese final (4,85–8 s): se pasa algo más lento (0,62) para que dé para 4,9 s de burbuja.
  senalando: { caja: { w: 604, h: 624, x: 348, y: 46 }, lienzo: [328, 46, 624], desde: 4.85, vel: 0.62, baja: 0.3 },   // brazos abiertos, se encoge de hombros y guiña: dato, aclaración
  explicando: { caja: { w: 522, h: 530, x: 38, y: 30 }, lienzo: [0, 0, 560], desde: 1.0 },                       // brazos abiertos: explica, enumera
  preocupada: { caja: { w: 520, h: 516, x: 31, y: 44 }, lienzo: [0, 0, 560], desde: 1.0 },                       // mira arriba con apuro: aviso, riesgo
  observando: { caja: { w: 554, h: 482, x: 6, y: 78 }, lienzo: [0, 0, 560], desde: 1.6, baja: 0.26 },            // prismáticos: avistamiento, «fíjate en…»
  reportero1: { caja: { w: 514, h: 494, x: 42, y: 66 }, lienzo: [0, 0, 560], desde: 1.0 },                       // micrófono en alto: novedad, cifra, cita
  reportero2: { caja: { w: 482, h: 412, x: 58, y: 148 }, lienzo: [0, 0, 560], desde: 1.0, baja: 0.22 },          // micrófono al pecho: pregunta al espectador
  cera: { caja: { w: 502, h: 414, x: 58, y: 146 }, lienzo: [0, 0, 560], desde: 1.0, baja: 0.22 },                // esponja: limpieza, mantenimiento, trabajo
  andando: { caja: { w: 534, h: 432, x: 26, y: 128 }, lienzo: [0, 0, 560], desde: 1.2, baja: 0.2 },              // camina contenta: «vamos a…», traslado
  de_espaldas: { caja: { w: 524, h: 482, x: 35, y: 78 }, lienzo: [0, 0, 560], desde: 0.9 },                      // se gira y da la espalda: broma, «yo no he sido»
  buceando: { caja: { w: 708, h: 642, x: 308, y: 70 }, lienzo: [264, 15, 752], desde: 0.4, vel: 0.75, baja: 0.12 }, // tubo y burbujas: agua, estanque, peces
};

// Parte el texto en líneas parecidas (2–5), como las burbujas del canal: frases de 8–21 palabras.
const partir = (txt: string): string[] => {
  const n = Math.max(1, Math.min(5, Math.ceil(txt.length / 31))), tope = txt.length / n + 4;
  const out: string[] = []; let cur = "";
  for (const p of txt.split(/\s+/)) {
    if (cur && (cur + " " + p).length > tope && out.length < n - 1) { out.push(cur); cur = p; } else cur = cur ? cur + " " + p : p;
  }
  if (cur) out.push(cur);
  return out;
};

// Burbuja dibujada con el diseño de la suya (personal/reinoselva/recursos/marca/tortuga/burbuja_original.png): blanca, borde negro grueso, lados algo
// abombados y cola hacia la tortuga. Se dibuja a la medida del texto. forma: "habla" (dato, aclaración, lo normal),
// "grito" (sorpresa, aviso fuerte: borde en picos) o "piensa" (duda, ironía: nube con bolitas).
const Burbuja: React.FC<{ x1: number; y1: number; px: number; py: number; lineas: string[]; fs: number; forma: string; fuente: string; esc: number; texto: number; izq: boolean; W: number; H: number }> = ({ x1, y1, px, py, lineas, fs, forma, fuente, esc, texto, izq, W, H }) => {
  const ancho = fuente === F_IMPACTO ? 0.46 : 0.6;
  const largo = Math.max(...lineas.map((l) => l.length));
  const bw = largo * fs * ancho + fs * (forma === "grito" ? 3.4 : 2.2), bh = lineas.length * fs * 1.2 + fs * (forma === "grito" ? 2.6 : 1.5);
  const x0 = x1 - bw, y0 = y1 - bh, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, r = Math.min(bw, bh) * 0.34, b = Math.min(bw, bh) * 0.035, sw = H * 0.0075;
  const m = (x: number) => (izq ? W - x : x);                 // a la izquierda, todo en espejo
  const P = (x: number, y: number) => m(x).toFixed(1) + " " + y.toFixed(1);
  let d = "";
  const bolas: [number, number, number][] = [];
  if (forma === "grito") {
    const n = 22, pts: string[] = [];
    for (let i = 0; i < n * 2; i++) {
      const a = (i / (n * 2)) * Math.PI * 2, k = i % 2 ? 0.86 : 1.0 + 0.06 * Math.sin(i * 2.7);
      pts.push(P(cx + Math.cos(a) * (bw / 2) * 1.02 * k, cy + Math.sin(a) * (bh / 2) * 1.08 * k));
    }
    d = "M " + pts.join(" L ") + " Z M " + P(x1 - bw * 0.3, y1 - bh * 0.06) + " L " + P(px, py) + " L " + P(x1 - bw * 0.16, y1 - bh * 0.12) + " Z";
  } else {
    const cola = forma === "piensa" ? "" : " L " + P(x1 - bw * 0.2, y1) + " L " + P(px, py) + " L " + P(x1 - bw * 0.36, y1);
    d = "M " + P(x0 + r, y0) + " Q " + P(cx, y0 - b) + " " + P(x1 - r, y0) + " Q " + P(x1, y0) + " " + P(x1, y0 + r) + " Q " + P(x1 + b, cy) + " " + P(x1, y1 - r) +
      " Q " + P(x1, y1) + " " + P(x1 - r, y1) + cola + " L " + P(x0 + r, y1) + " Q " + P(x0, y1) + " " + P(x0, y1 - r) + " Q " + P(x0 - b, cy) + " " + P(x0, y0 + r) + " Q " + P(x0, y0) + " " + P(x0 + r, y0) + " Z";
    if (forma === "piensa") for (let i = 0; i < 3; i++) { const t = 0.25 + i * 0.3; bolas.push([x1 - bw * 0.26 + (px - (x1 - bw * 0.26)) * t, y1 + (py - y1) * t, fs * (0.42 - i * 0.11)]); }
  }
  return (
    <AbsoluteFill style={{ transform: "scale(" + esc + ")", transformOrigin: m(px) + "px " + py + "px", opacity: esc > 0.01 ? 1 : 0 }}>
      <svg width={W} height={H} style={{ position: "absolute", filter: "drop-shadow(0 " + H * 0.005 + "px " + H * 0.008 + "px rgba(0,0,0,.4))" }}>
        <path d={d} fill="#fff" stroke="#000" strokeWidth={sw} strokeLinejoin="round" fillRule="nonzero" />
        {forma === "grito" ? <ellipse cx={m(cx)} cy={cy} rx={bw * 0.4} ry={bh * 0.36} fill="#fff" /> : null}
        {bolas.map(([bx, by, br], i) => <circle key={i} cx={m(bx)} cy={by} r={br} fill="#fff" stroke="#000" strokeWidth={sw * 0.8} />)}
      </svg>
      <div style={{ position: "absolute", left: Math.min(m(x0), m(x1)), top: y0, width: bw, height: bh, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", opacity: texto,
        fontFamily: fuente, fontWeight: fuente === F_IMPACTO ? 400 : 800, fontSize: fs, lineHeight: 1.2, color: "#000", textAlign: "center" }}>
        {lineas.map((l, i) => <div key={i} style={{ whiteSpace: "nowrap" }}>{l}</div>)}
      </div>
    </AbsoluteFill>
  );
};

// La tortuga comenta: asoma desde abajo en una esquina (derecha de serie), la burbuja aparece 0,4 s después y se van
// juntas. it: anim, txt (una frase o una lista de frases que se reparten el tiempo), lado ("der" | "izq"),
// forma ("habla" | "grito" | "piensa"), fuente ("impacto" | "redonda"), tam (tamaño de la tortuga, 1 = el suyo).
export const Tortuga: React.FC<{ it: Item; f: number; dur: number }> = ({ it, f, dur }) => {
  const { height: H, width: W, fps } = useVideoConfig();
  const A = TORTUGA[it.anim] ?? TORTUGA.senalando, izq = it.lado === "izq";
  const T = H * 0.56 * (it.tam ?? 1), k = T / A.lienzo[2], baja = A.baja ?? 0.31;
  const cxc = W * 0.835, arriba = H - T * (1 - baja);                       // centro y borde superior del lienzo de la tortuga
  const entra = interpolate(f, [0, fps * 0.4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const sale = interpolate(f, [dur - fps * 0.22, dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.quad) });
  const dy = (entra + sale) * (H - arriba + H * 0.02);
  const x = cxc - T / 2 + (A.caja.x - A.lienzo[0]) * k, w = A.caja.w * k;
  const frases: string[] = Array.isArray(it.txt) ? it.txt : [String(it.txt ?? "")];
  const t0 = fps * 0.4, cada = (dur - t0 - fps * 0.2) / frases.length, i = Math.max(0, Math.min(frases.length - 1, Math.floor((f - t0) / cada))), fb = f - t0 - i * cada;
  const lineas = partir(frases[i]);
  const esc = f < t0 ? 0 : interpolate(fb, [0, 6], [0.5, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) * interpolate(f, [dur - fps * 0.2, dur], [1, 0.4], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const texto = fb >= fps * 0.12 && f < dur - fps * 0.12 ? 1 : 0;
  const arribaVisible = arriba + (A.caja.y - A.lienzo[1]) * k;                 // por dónde asoma la cabeza
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, transform: "translateY(" + dy + "px)" }}>
        <Clip it={it} src={DIR + "tortuga/" + (TORTUGA[it.anim] ? it.anim : "senalando") + ".webm"} caja={A.caja} w={w} x={izq ? W - x - w : x} y={arriba + (A.caja.y - A.lienzo[1]) * k} desde={A.desde} vel={A.vel ?? 1} espejo={izq}
          estilo={{ filter: "drop-shadow(0 0 " + H * 0.004 + "px rgba(0,0,0,.55))" }} />
      </div>
      {frases[i] ? <Burbuja x1={W * 0.772} y1={Math.max(arribaVisible + H * 0.005, H * 0.3)} px={W * 0.765} py={arribaVisible + H * 0.075} lineas={lineas} fs={H * (lineas.length > 3 ? 0.033 : 0.036)}
        forma={it.forma ?? "habla"} fuente={it.fuente === "redonda" ? F_REDONDA : F_IMPACTO} esc={esc} texto={texto} izq={izq} W={W} H={H} /> : null}
    </AbsoluteFill>
  );
};

// Logo con letras sobre la intro: destello blanco y el logo centrado hasta el corte (así abre todos sus vídeos).
// El .png va SIN su fondo crema (herramientas/quitar_fondo_imagen.py) y con un resplandor claro detrás, como el suyo:
// las letras son verde oscuro y sin él no se leen sobre la selva.
// El logo es el de la marca en el idioma del vídeo (marca.json: Reino Selva en español, RayWild en inglés); lo manda
// paso3 en it.logo. Si el de ese idioma no está preparado llega "" y no se pinta nada: nunca el logo del otro canal.
export const LogoIntro: React.FC<{ f: number; dur: number; logo?: string }> = ({ f, dur, logo }) => {
  const { height: H } = useVideoConfig();
  const destello = interpolate(f, [0, 3, 12], [0, 0.9, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const esc = interpolate(f, [0, dur], [1.0, 1.05]);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <Img src={staticFile(DIR + (logo || "logo_con_letra.png"))} style={{ height: H * 0.72, opacity: f >= 3 ? 1 : 0, transform: "scale(" + esc + ")", filter: "drop-shadow(0 0 " + H * 0.012 + "px rgba(255,236,170,.75)) drop-shadow(0 0 " + H * 0.03 + "px rgba(255,236,170,.45))" }} />
      <AbsoluteFill style={{ backgroundColor: "#fff", opacity: destello }} />
    </AbsoluteFill>
  );
};

// Rótulo de IDEA CLAVE, su costumbre: lo que acaba de decir y no debe perderse (nombre científico de la especie, término,
// decisión, frase resumen) escrito grande abajo, en el momento en que lo dice. Él lo pone en blanco con contorno fino; aquí
// va con la letra y las reglas de la skill: blanco = información, línea pequeña en el acento, entra de golpe y crece
// despacio y seguido, se va por corte. PROPIOS = [(ancla, segundos, "rotulo", {"txt": "TESTUDO KLEINMANNI", "sub": "Egyptian tortoise"})]
// "txt" admite dos líneas con "|"; "lado": "izq" | "der" si en el centro tapa algo; "y": altura de la base (0,1 = abajo).
export const Rotulo: React.FC<{ it: Item; f: number; dur: number }> = ({ it, f, dur }) => {
  const { height: H, width: W, fps } = useVideoConfig();
  const fSub = f - Math.round(Number(it.subEn ?? 0) * fps);   // subEn: la segunda línea entra cuando se DICE, no antes
  const lineas = String(it.txt).split("|");
  const largo = Math.max(...lineas.map((l) => l.length));
  const fs = Math.min(H * 0.08, (W * 0.7) / (largo * 0.82));
  const esc = pop(f) * interpolate(f, [0, dur], [1, 1.08], { extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  const x = it.lado === "izq" ? 0.28 : it.lado === "der" ? 0.72 : 0.5;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: W * x, bottom: H * (it.y ?? 0.1), transform: "translateX(-50%) scale(" + esc + ")", transformOrigin: "50% 100%", textAlign: "center", whiteSpace: "nowrap" }}>
        <div style={{ fontFamily: F_ANCHA, fontWeight: 900, fontSize: fs, lineHeight: 1.12, color: "white", textShadow: borde(H * 0.005) }}>
          {lineas.map((l, i) => (
            <div key={i}>{l}</div>
          ))}
        </div>
        {it.sub ? <div style={{ fontFamily: F_TXT, fontWeight: 800, fontSize: Math.max(H * 0.04, fs * 0.55), color: ACENTO, textShadow: borde(H * 0.004), marginTop: H * 0.004, opacity: fSub >= 0 ? 1 : 0, transform: "scale(" + pop(Math.max(0, fSub)) + ")", transformOrigin: "50% 0%" }}>{it.sub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

export const propios = (it: Item, f: number, dur: number): React.ReactNode | undefined => {
  if (it.t === "tortuga") return <Tortuga it={it} f={f} dur={dur} />;
  if (it.t === "logo_intro") return it.logo === "" ? null : <LogoIntro f={f} dur={dur} logo={it.logo} />;
  if (it.t === "rotulo") return <Rotulo it={it} f={f} dur={dur} />;
  return undefined;
};
