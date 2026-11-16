// "¿Cuál es tu prenda favorita de Gymshark de hombre?" — Lucas pregunta a creadoras de contenido en el gym.
// Brutos: GS/prenda fav/IMG_10xx.MOV (1071 = gancho V1; 1078 = gancho V2 → bruto terminado/2026-11-01_prenda-fav-gymshark_01-gancho-v2-lucas.MOV) → public/prenda-fav/IMG_10xx.mp4 (proxy SDR 30 fps)
// Audio: voz aislada (ElevenLabs) + mezclar_voces.py → public/prenda-fav/IMG_10xx-voz.wav (intro: solo loudnorm).
// Palabras: Scribe → public/prenda-fav/IMG_10xx-palabras.json.
// Código de descuento ALVAREZ10 en "Creo que está ganando Vengeance".
// Peticiones de Lucas: empieza por Susie; cuando dicen la prenda, sale la foto del e-commerce de Gymshark con pop;
// cuando dice el nombre de la chica, su @ encima de la cabeza ~1,5 s (si no se dice el nombre: al empezar su toma).
// Fotos de producto: eu.gymshark.com/es-ES (precios a 2026-11-01) → recursos/fotos/gymshark/ y public/prenda-fav/prendas/.
import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  Img,
  interpolate,
  Series,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { ACENTO, Bloque, F_FUERTE, F_RELLENO, Sfx, TextoBloques } from "../../comun/hablando";
import { Subtitulos, TITLE_FONT } from "../../comun/Subtitulos";
import { RotuloCodigo } from "../../comun/Rotulos";

import p1057 from "../../../public/prenda-fav/IMG_1057-palabras.json";
import p1058 from "../../../public/prenda-fav/IMG_1058-palabras.json";
import p1059 from "../../../public/prenda-fav/IMG_1059-palabras.json";
import p1060 from "../../../public/prenda-fav/IMG_1060-palabras.json";
import p1061 from "../../../public/prenda-fav/IMG_1061-palabras.json";
import p1063 from "../../../public/prenda-fav/IMG_1063-palabras.json";
import p1065 from "../../../public/prenda-fav/IMG_1065-palabras.json";
import p1066 from "../../../public/prenda-fav/IMG_1066-palabras.json";
import p1067 from "../../../public/prenda-fav/IMG_1067-palabras.json";
import p1068 from "../../../public/prenda-fav/IMG_1068-palabras.json";

const FPS = 30;
type W = { w: string; start: number; end: number };
const PAL: Record<string, W[]> = {
  "1057": p1057, "1058": p1058, "1059": p1059, "1060": p1060, "1061": p1061,
  "1063": p1063, "1065": p1065, "1066": p1066, "1067": p1067, "1068": p1068,
};

// ------------------------------------------------------------------ montaje (s del bruto)
// cara = punto que queda fijo al hacer zoom (cabeza de la chica / de Lucas), px del proxy 1080×1920.
type Seg = {
  clip: string; desde: number; hasta: number; nombre: string;
  nueva?: boolean; // primera toma de una chica (punch-in de entrada)
  zoom?: number; cara: [number, number];
  zoomA?: { en: number; a: number }; // zoom largo que aterriza en el s `en` del bruto
  intro?: boolean; // gancho de Lucas a cámara (zoom de entrada 1,00 → 1,20)
};

// ------------------------------------------------------------------ ganchos (una versión por gancho, para trials)
// Todo lo demás (entrevistas, fichas, @, subtítulos, código) es común a todas las versiones.
type Intro = {
  clip: string; desde: number; hasta: number; nombre: string; cara: [number, number];
  sparkle: number; // s del bruto donde entra la primera palabra del gancho
  bloques: (I: (t: number) => number, finIntro: number) => Bloque[];
};
const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });
const INTROS: Record<"v1" | "v2", Intro> = {
  // V1 (IMG_1071): "Hoy les voy a preguntar a tus creadoras de contenido favoritas cuál es su prenda favorita de Gymshark"
  v1: {
    clip: "1071", desde: 1.3, hasta: 6.62, nombre: "Intro: hoy les voy a preguntar…", cara: [567, 535], sparkle: 1.4,
    bloques: (I, fin) => [
      { desde: 0, hasta: I(4.0), y: 0.7, palabras: [P("hoy les voy a", I(1.4)), P("preguntar a", I(1.86)), P("CREADORAS", I(2.5), "fuerte", true), P("de contenido", I(2.88), "relleno", true), P("favoritas", I(3.48), "remate")] },
      { desde: I(4.0), hasta: fin, y: 0.7, palabras: [P("cuál es su", I(4.06)), P("PRENDA FAVORITA", I(4.74), "fuerte", true), P("de", I(5.78), "relleno", true), P("Gymshark", I(5.94), "remate")] },
    ],
  },
  // V2 (IMG_1078): "¿Qué prendas de Gymshark son las favoritas de las mujeres?"
  v2: {
    clip: "1078", desde: 0.42, hasta: 4.1, nombre: "Intro: ¿qué prendas de Gymshark…?", cara: [540, 700], sparkle: 0.52,
    bloques: (I, fin) => [
      { desde: 0, hasta: I(1.72), y: 0.7, palabras: [P("qué prendas de", I(0.52)), P("GYMSHARK", I(1.1), "fuerte", true)] },
      { desde: I(1.72), hasta: fin, y: 0.7, palabras: [P("son las", I(1.74)), P("FAVORITAS", I(2.32), "fuerte", true), P("de las", I(3.06), "relleno", true), P("mujeres?", I(3.34), "remate")] },
    ],
  },
};

// tomas de cada chica (s del bruto), en el orden en que salen dentro de su bloque
const CHICAS: Record<string, Seg[]> = {
  susie: [{ clip: "1061", desde: 0.08, hasta: 7.5, nombre: "Susie: tank top", nueva: true, cara: [340, 745] }],
  andrea: [
    { clip: "1058", desde: 5.8, hasta: 6.2, nombre: "Andrea,", nueva: true, cara: [687, 760] },
    { clip: "1058", desde: 8.68, hasta: 14.0, nombre: "Andrea: Element Baselayer Tank", zoom: 1.1, cara: [687, 760] },
    { clip: "1058", desde: 15.82, hasta: 16.68, nombre: "Andrea: así que esa es", cara: [687, 760] },
  ],
  lourdes: [{ clip: "1060", desde: 3.05, hasta: 9.1, nombre: "Lourdes: Element Baselayer (gains)", nueva: true, cara: [690, 760] }],
  inma: [
    { clip: "1057", desde: 13.78, hasta: 14.08, nombre: "Inma.", nueva: true, cara: [770, 780] },
    { clip: "1057", desde: 17.46, hasta: 21.62, nombre: "Inma: colección Sam Sulek", zoom: 1.1, cara: [770, 780] },
  ],
  lucia: [
    { clip: "1065", desde: 0.55, hasta: 0.96, nombre: "Lucía,", nueva: true, cara: [729, 665] },
    { clip: "1065", desde: 3.05, hasta: 5.95, nombre: "Lucía: Shadow negra", zoom: 1.08, cara: [729, 665] },
    { clip: "1065", desde: 7.66, hasta: 8.8, nombre: "Me la voy a tener que comprar", cara: [420, 560] },
  ],
  paula: [
    { clip: "1059", desde: 0.45, hasta: 0.8, nombre: "Paula,", nueva: true, cara: [616, 700] },
    { clip: "1059", desde: 2.4, hasta: 7.55, nombre: "Paula: compresivas Shadow con degradado", zoom: 1.08, cara: [616, 700] },
  ],
  vivi: [
    { clip: "1063", desde: 2.25, hasta: 4.88, nombre: "Vivi: Vengeance azul y gris", nueva: true, cara: [560, 700] },
    { clip: "1063", desde: 5.62, hasta: 6.25, nombre: "Muy top", zoom: 1.08, cara: [400, 650] },
  ],
  marina: [{ clip: "1066", desde: 2.3, hasta: 11.08, nombre: "Marina: chaqueta Vengeance + pumper", nueva: true, cara: [463, 680] }],
  olaia: [
    { clip: "1067", desde: 0.0, hasta: 0.3, nombre: "Olaia,", nueva: true, cara: [719, 760] },
    { clip: "1067", desde: 3.62, hasta: 8.4, nombre: "Olaia: compresivas, Vengeance", zoom: 1.08, cara: [719, 760] },
    { clip: "1067", desde: 8.8, hasta: 10.68, nombre: "Olaia: o las Onyx", cara: [719, 760] },
  ],
  jas: [
    { clip: "1068", desde: 1.9, hasta: 7.78, nombre: "Jas: oversized Vengeance + está ganando", nueva: true, cara: [560, 650], zoomA: { en: 6.56, a: 1.18 } },
    { clip: "1068", desde: 8.35, hasta: 9.03, nombre: "Sí", zoom: 1.12, cara: [560, 650] },
  ],
};

// cierre de cada versión: dónde sale el código ALVAREZ10, tomas extra y remate
type Final = {
  extra?: Seg[]; // tomas que se añaden al final
  hasta?: number; // alarga la última toma de la última chica hasta este s del bruto
  codigo: [string, number]; // clip + s del bruto donde entra el código
  remate?: (F: (clip: string, t: number) => number, dur: number) => Bloque[];
  golpe?: [string, number]; // impacto de sonido en el remate
};
const FINALES: Record<string, Final> = {
  // "Creo que está ganando Vengeance" (Lucas, en la toma de Jas) + VENGEANCE 4 de 10
  jas: {
    codigo: ["1068", 5.04], golpe: ["1068", 6.56],
    remate: (F, dur) => [{ desde: F("1068", 6.56), hasta: dur, y: 0.2, palabras: [P("VENGEANCE", F("1068", 6.56), "fuerte"), P("4 de 10", F("1068", 7.46), "remate", true)] }],
  },
  // Vivi: "Muy top" y se quedan sonriendo a cámara (a los 7 s ella se va)
  vivi: { hasta: 6.9, codigo: ["1063", 5.62] },
  // Marina: "Top." + Lucas señalando a cámara "Apunten, apunten" → código
  marina: { extra: [{ clip: "1066", desde: 13.76, hasta: 16.0, nombre: "Top. Apunten, apunten (código)", zoom: 1.08, cara: [840, 640] }], codigo: ["1066", 14.6] },
};

type Version = { intro: Intro; chicas: string[]; final: string };
const VERSIONES: Record<string, Version> = {
  v1: { intro: INTROS.v1, chicas: ["susie", "andrea", "lourdes", "inma", "lucia", "paula", "vivi", "marina", "olaia", "jas"], final: "jas" },
  v2: { intro: INTROS.v2, chicas: ["susie", "andrea", "lourdes", "inma", "lucia", "paula", "vivi", "marina", "olaia", "jas"], final: "jas" },
  // 2026-11-01: Lucas pide 4 versiones más (mismo orden con los dos ganchos), 6 chicas
  v3: { intro: INTROS.v1, chicas: ["susie", "paula", "inma", "lucia", "olaia", "vivi"], final: "vivi" },
  v4: { intro: INTROS.v2, chicas: ["susie", "paula", "inma", "lucia", "olaia", "vivi"], final: "vivi" },
  v5: { intro: INTROS.v1, chicas: ["susie", "paula", "inma", "lucia", "olaia", "marina"], final: "marina" },
  v6: { intro: INTROS.v2, chicas: ["susie", "paula", "inma", "lucia", "olaia", "marina"], final: "marina" },
};

type SegF = Seg & { ini: number; from: number; dur: number };
const ARREGLOS: Record<string, string> = {
  "Sule.": "Sulek.", "pamper": "pumper", "pamper.": "pumper.", "Laia,": "Olaia,", "vengeance": "Vengeance",
};

// montaje completo de una versión: gancho + entrevistas
const montar = (v: Version) => {
  const { intro } = v;
  const final = FINALES[v.final];
  const resto = v.chicas.flatMap((c) => CHICAS[c]);
  if (final.hasta) resto[resto.length - 1] = { ...resto[resto.length - 1], hasta: final.hasta };
  resto.push(...(final.extra ?? []));
  let ini = 0;
  const SEGS: SegF[] = [{ ...intro, intro: true }, ...resto].map((s) => {
    const from = Math.round(s.desde * FPS);
    const dur = Math.round(s.hasta * FPS) - from;
    const r = { ...s, ini, from, dur };
    ini += dur;
    return r;
  });
  const DUR = SEGS.reduce((a, s) => a + s.dur, 0);

  // s del bruto de un clip → frame del edit (null si ese momento no está en el montaje)
  const enEdit = (clip: string, t: number): number | null => {
    const f = Math.round(t * FPS);
    const s =
      SEGS.find((x) => x.clip === clip && f >= x.from && f < x.from + x.dur) ??
      SEGS.find((x) => x.clip === clip && f >= x.from && f <= x.from + x.dur + 1); // fin de toma (para "hasta")
    return s ? Math.min(s.ini + f - s.from, s.ini + s.dur - 1) : null;
  };
  const F = (clip: string, t: number) => {
    const r = enEdit(clip, t);
    if (r === null) throw new Error(`${clip}@${t} fuera del montaje`);
    return r;
  };

  // subtítulos (sin la intro: ahí va el gancho)
  const PALABRAS = SEGS.filter((s) => !s.intro).flatMap((s) =>
    PAL[s.clip]
      .filter((p) => p.start * FPS >= s.from - 2 && p.start * FPS < s.from + s.dur - 3) // sin palabras cortadas al final de la toma
      .map((p) => {
        const d = (s.ini - s.from) / FPS;
        return { w: ARREGLOS[p.w] ?? p.w, start: Math.max(s.ini / FPS, p.start + d), end: Math.min((s.ini + s.dur) / FPS, p.end + d) };
      })
      // la última palabra de cada toma cierra el bloque (nunca se mezclan palabras de dos tomas)
      .map((p, i, arr) => (i === arr.length - 1 && !/[.,?!:]$/.test(p.w) ? { ...p, w: p.w + "," } : p)),
  );
  // cambio de chica = el subtítulo se va con el corte
  const CORTES = SEGS.filter((s, i) => i > 0 && s.clip !== SEGS[i - 1].clip).map((s) => s.ini / FPS);

  const I = (t: number) => F(intro.clip, t);
  const FIN_INTRO = SEGS[1].ini;
  const BLOQUES: Bloque[] = [...intro.bloques(I, FIN_INTRO), ...(final.remate?.(F, DUR) ?? [])];
  const CLIPS = new Set(SEGS.map((x) => x.clip));
  return { intro, final, SEGS, DUR, F, PALABRAS, CORTES, I, FIN_INTRO, BLOQUES, CLIPS };
};
type Montaje = ReturnType<typeof montar>;
const MONTAJES = Object.fromEntries(Object.entries(VERSIONES).map(([k, v]) => [k, montar(v)])) as Record<keyof typeof VERSIONES, Montaje>;

const CLAVES = /^(vengeance|element|base|layer|baselayer|shadow|sulek|tank|top|onyx|oversized|oversize|pumper|chaqueta|compresiva|compresivas|tirantes|gains|gymshark)$/i;

// ------------------------------------------------------------------ plano: punch-in de entrada + empuje lento (nunca quieto)
const Plano: React.FC<{ s: SegF; children?: React.ReactNode }> = ({ s, children }) => {
  const frame = useCurrentFrame();
  let z = s.zoom ?? 1;
  if (s.intro) {
    // zoom de entrada 1,00 → 1,20 en 27 f centrado en la cara
    z = interpolate(frame, [1, 28], [1, 1.2], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  }
  if (s.zoomA) {
    const en = Math.round(s.zoomA.en * FPS) - s.from;
    z *= interpolate(frame, [en - 26, en], [1, s.zoomA.a], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  }
  const empuje = 1 + 0.012 * (frame / FPS);
  const punch = s.nueva ? interpolate(frame, [0, 7], [0.06, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 0;
  return (
    <AbsoluteFill style={{ transform: `scale(${z * empuje + punch})`, transformOrigin: `${s.cara[0]}px ${s.cara[1]}px` }}>
      {children}
    </AbsoluteFill>
  );
};

// @ de la chica encima de su cabeza (vive dentro del plano: sigue el zoom)
const Arroba: React.FC<{ handle: string; x: number; y: number; en: number; dur?: number }> = ({ handle, x, y, en, dur = 40 }) => {
  const frame = useCurrentFrame();
  if (frame < en || frame > en + dur + 6) return null;
  const e = interpolate(frame, [en, en + 7], [0.4, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.6)) });
  const sale = interpolate(frame, [en + dur, en + dur + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const o = interpolate(frame, [en, en + 3], [0, 1], { extrapolateRight: "clamp" }) * sale;
  return (
    <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%, -100%) scale(${e * (0.6 + 0.4 * sale)})`, transformOrigin: "50% 100%", opacity: o }}>
      <div
        style={{
          display: "flex", alignItems: "center", gap: 12, background: "white", color: "#141414", borderRadius: 50,
          padding: "12px 28px 12px 16px", fontFamily: TITLE_FONT, fontWeight: 700, fontSize: 46, whiteSpace: "nowrap",
          boxShadow: "0 8px 26px rgba(0,0,0,0.45)",
        }}
      >
        <svg width={46} height={46} viewBox="0 0 24 24" fill="none" stroke="#141414" strokeWidth={2.2}>
          <rect x={2.5} y={2.5} width={19} height={19} rx={5.5} />
          <circle cx={12} cy={12} r={4.3} />
          <circle cx={17.4} cy={6.6} r={0.9} fill="#141414" stroke="none" />
        </svg>
        @{handle}
      </div>
      {/* piquito hacia la cabeza */}
      <div style={{ width: 0, height: 0, margin: "-1px auto 0", borderLeft: "16px solid transparent", borderRight: "16px solid transparent", borderTop: "18px solid white" }} />
    </div>
  );
};

const ARROBAS: Record<string, { handle: string; x: number; y: number; t: number }> = {
  "1061": { handle: "susiiigs", x: 340, y: 640, t: 0.22 },
  "1058": { handle: "andreea_garci", x: 687, y: 610, t: 5.84 },
  "1057": { handle: "inmagonzx", x: 770, y: 640, t: 13.8 },
  "1065": { handle: "luciadelcantox", x: 729, y: 500, t: 0.58 },
  "1059": { handle: "pauladelpalaciox", x: 616, y: 545, t: 0.48 },
  "1066": { handle: "marinafonsx", x: 463, y: 500, t: 2.45 },
  "1067": { handle: "olaiasalbide", x: 719, y: 610, t: 0.02 },
  // sin nombre dicho: el @ sale al empezar su toma (Lucas dio quién es quién con capturas)
  "1060": { handle: "lourdesgix", x: 697, y: 610, t: 3.12 },
  "1063": { handle: "vivieonx", x: 655, y: 615, t: 2.32 },
  "1068": { handle: "jascastellx", x: 638, y: 615, t: 1.97 },
};

// código de descuento de Lucas (rótulo sin pastilla, comun/Rotulos.tsx, entra con pop y se queda hasta el final)
const Codigo: React.FC<{ en: number }> = ({ en }) => {
  const frame = useCurrentFrame();
  if (frame < en) return null;
  const e = interpolate(frame, [en, en + 8], [0.4, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.6)) });
  const o = interpolate(frame, [en, en + 3], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 1120, opacity: o }}>
      <div style={{ transform: `scale(${e})` }}>
        <RotuloCodigo size={124} />
      </div>
    </AbsoluteFill>
  );
};

const Base: React.FC<{ m: Montaje }> = ({ m }) => (
  <Series>
    {m.SEGS.map((s, i) => {
      const voz = staticFile(`prenda-fav/IMG_${s.clip}-voz.wav`);
      return (
        <Series.Sequence key={i} name={s.nombre} durationInFrames={s.dur} premountFor={FPS}>
          <Plano s={s}>
            <Video src={staticFile(`prenda-fav/IMG_${s.clip}.mp4`)} trimBefore={s.from} muted style={{ width: "100%", height: "100%" }} />
          </Plano>
          <Audio src={voz} trimBefore={s.from} />
        </Series.Sequence>
      );
    })}
  </Series>
);

// ------------------------------------------------------------------ ficha de producto (como en la web de Gymshark)
type Prenda = { img: string; nombre: string; info: string; precio: string };
const PRENDAS: Record<string, Prenda> = {
  tank: { img: "critical-drop-arm-tank", nombre: "Critical Drop Arm Tank", info: "Black", precio: "28 €" },
  elementTank: { img: "element-baselayer-tank", nombre: "Element Baselayer Tank", info: "Black", precio: "22 €" },
  elementTee: { img: "element-baselayer-tshirt", nombre: "Element Baselayer T-Shirt", info: "Black", precio: "25 €" },
  sulek: { img: "sam-sulek-tank", nombre: "Gymshark x Sam Sulek Tank", info: "Colección Sam Sulek", precio: "35 €" },
  shadowTee: { img: "shadow-seamless-tee-green", nombre: "Shadow Seamless T-Shirt", info: "Track Green", precio: "" },
  shadow: { img: "shadow-seamless-ls", nombre: "Shadow Seamless Long Sleeve", info: "Black", precio: "40 €" },
  vengLs: { img: "vengeance-ls-onyx-blue", nombre: "Vengeance Long Sleeve T-Shirt", info: "Onyx Grey/Brand Blue", precio: "50 €" },
  vengJacket: { img: "vengeance-jacket-onyx-blue", nombre: "Vengeance Full Zip Jacket", info: "Onyx Grey/Brand Blue", precio: "55 €" },
  pumperPants: { img: "straight-leg-pumper-pants", nombre: "Straight Leg Pumper Pants", info: "Black", precio: "65 €" },
  pumperShorts: { img: "pumper-shorts", nombre: 'Pumper Shorts 5"', info: "Oversized Fit", precio: "40 €" },
  vengTee: { img: "vengeance-tshirt-black-red", nombre: "Vengeance T-Shirt", info: "Black/Carmine Red", precio: "42 €" },
  vengTeeOnyx: { img: "vengeance-tshirt-onyx-blue", nombre: "Vengeance T-Shirt", info: "Onyx Grey/Brand Blue", precio: "42 €" },
  vengOversized: { img: "vengeance-graphic-oversized-8", nombre: "Vengeance Graphic T-Shirt", info: "Oversized Fit", precio: "40 €" },
};

// Cada ficha entra con pop en la palabra exacta y se queda hasta la siguiente o hasta que acaba la chica.
// lado: encima del cuerpo de Lucas (la cara de los dos se sigue viendo).
type Ficha = { p: string; clip: string; t: number; hasta: { clip: string; t: number }; lado: "izq" | "der"; giro: number; badge?: string };
const FICHAS: Ficha[] = [
  { p: "tank", clip: "1061", t: 4.28, hasta: { clip: "1061", t: 7.49 }, lado: "der", giro: 3 },
  { p: "elementTank", clip: "1058", t: 11.98, hasta: { clip: "1058", t: 16.67 }, lado: "izq", giro: -3 },
  { p: "elementTee", clip: "1060", t: 3.28, hasta: { clip: "1060", t: 9.09 }, lado: "izq", giro: -3 },
  { p: "sulek", clip: "1057", t: 19.48, hasta: { clip: "1057", t: 21.61 }, lado: "izq", giro: -3 },
  { p: "shadow", clip: "1065", t: 3.2, hasta: { clip: "1065", t: 8.79 }, lado: "izq", giro: -3 },
  { p: "vengLs", clip: "1063", t: 2.48, hasta: { clip: "1063", t: 6.24 }, lado: "izq", giro: -3 },
  { p: "vengJacket", clip: "1066", t: 3.44, hasta: { clip: "1066", t: 6.26 }, lado: "der", giro: 3 },
  { p: "pumperPants", clip: "1066", t: 6.26, hasta: { clip: "1066", t: 10.74 }, lado: "der", giro: -2 },
  { p: "pumperShorts", clip: "1066", t: 10.74, hasta: { clip: "1066", t: 11.07 }, lado: "der", giro: 3 },
  { p: "vengTee", clip: "1067", t: 8.88, hasta: { clip: "1067", t: 10.32 }, lado: "izq", giro: -3 },
  { p: "vengTeeOnyx", clip: "1067", t: 10.32, hasta: { clip: "1067", t: 10.67 }, lado: "izq", giro: 2 },
  { p: "shadowTee", clip: "1059", t: 4.0, hasta: { clip: "1059", t: 7.54 }, lado: "izq", giro: -3 },
  { p: "vengOversized", clip: "1068", t: 2.82, hasta: { clip: "1068", t: 5.24 }, lado: "izq", giro: 3 },
];

const ANCHO = 320;
const FichaProducto: React.FC<{ f: Ficha; m: Montaje }> = ({ f, m }) => {
  const frame = useCurrentFrame();
  const { F } = m;
  const en = F(f.clip, f.t) - 1; // 1 frame antes: el pop llega justo con la palabra
  const sale = F(f.hasta.clip, f.hasta.t) - 6; // la salida acaba en el corte, no se cuela en la toma siguiente
  if (frame < en || frame > sale + 6) return null;
  const p = PRENDAS[f.p];
  const e = interpolate(frame, [en, en + 7], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const k = e * s;
  const flota = Math.sin((frame - en) / 10) * 5;
  const cx = f.lado === "izq" ? 270 : 810;
  return (
    <div
      style={{
        position: "absolute", left: cx, top: 800 + flota, width: ANCHO,
        transform: `translateX(-50%) scale(${k}) rotate(${f.giro + (1 - e) * -8}deg)`, transformOrigin: "50% 40%",
        opacity: Math.min(1, k * 1.6), background: "white", borderRadius: 22, overflow: "hidden",
        boxShadow: "0 18px 40px rgba(0,0,0,0.55), 0 0 0 3px rgba(255,255,255,0.9)",
      }}
    >
      <Img src={staticFile(`prenda-fav/prendas/${p.img}.jpg`)} style={{ width: ANCHO, height: Math.round(ANCHO * 1.1), objectFit: "cover", objectPosition: "50% 20%", display: "block" }} />
      <div style={{ padding: "14px 18px 16px", color: "#111" }}>
        <div style={{ fontFamily: F_FUERTE, fontSize: 34, lineHeight: 1.02, textTransform: "uppercase", letterSpacing: 0.3 }}>{p.nombre}</div>
        <div style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: 21, color: "#8a8a8a", marginTop: 4 }}>{p.info}</div>
        {/* sin precio: Lucas no quiere que se vean (2026-11-01) */}
      </div>
      <div style={{ position: "absolute", left: 14, top: 14, fontFamily: F_FUERTE, fontSize: 22, letterSpacing: 2, color: "#111", background: "white", padding: "4px 10px", borderRadius: 6 }}>
        GYMSHARK
      </div>
      {f.badge ? (
        <div
          style={{
            position: "absolute", right: 14, top: 12, width: 84, height: 84, borderRadius: 42, background: ACENTO, color: "#111",
            display: "flex", alignItems: "center", justifyContent: "center", fontFamily: F_FUERTE, fontSize: 46,
            transform: `scale(${interpolate(frame, [en + 8, en + 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(3)) })})`,
            boxShadow: "0 6px 16px rgba(0,0,0,0.4)",
          }}
        >
          {f.badge}
        </div>
      ) : null}
    </div>
  );
};

// doble flash en el paso de la intro a las entrevistas: 4 f blanco · 1 f plano nuevo · 3 f blanco
const DobleFlash: React.FC<{ en: number }> = ({ en }) => {
  const frame = useCurrentFrame();
  const d = frame - en;
  let o = 0;
  if (d >= -4 && d < 0) o = interpolate(d, [-4, -1], [0.5, 1]);
  if (d >= 1 && d <= 3) o = interpolate(d, [1, 3], [0.9, 0.2]);
  return o ? <AbsoluteFill style={{ background: "white", opacity: o }} /> : null;
};

export const PrendaFav: React.FC<{ v: keyof typeof MONTAJES }> = ({ v }) => {
  const frame = useCurrentFrame();
  const m = MONTAJES[v];
  // solo fichas y @ de las chicas que salen en esta versión
  const fichas = FICHAS.filter((f) => m.CLIPS.has(f.clip));
  const arrobas = Object.entries(ARROBAS).filter(([c]) => m.CLIPS.has(c));
  const [cc, ct] = m.final.codigo;
  const { F, I, FIN_INTRO } = m;
  const pops = [
    ...fichas.map((f) => ({ en: F(f.clip, f.t) - 1, v: 0.5 })),
    ...arrobas.map(([c, a]) => ({ en: F(c, a.t), v: 0.35 })),
  ];
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* colores originales del bruto: sin etalonado (Lucas, 2026-11-01) */}
      <Base m={m} />
      {/* @ en su propia capa: dura lo mismo para todas aunque la toma del nombre sea muy corta (el zoom va centrado en su cabeza) */}
      {arrobas.map(([c, a]) => (
        <Arroba key={c} handle={a.handle} x={a.x} y={a.y} en={F(c, a.t)} />
      ))}
      {fichas.map((f, i) => (
        <FichaProducto key={i} f={f} m={m} />
      ))}
      <TextoBloques bloques={m.BLOQUES} pop escala={0.82} />
      <AbsoluteFill style={{ opacity: frame >= FIN_INTRO ? 1 : 0 }}>
        <Subtitulos palabras={m.PALABRAS} offset={0} claves={CLAVES} maxHueco={0.6} top={1390} cortes={m.CORTES} />
      </AbsoluteFill>
      <Codigo en={F(cc, ct)} />
      <DobleFlash en={FIN_INTRO} />
      {/* sonido: entrada (golpe + whoosh), sparkle del título, doble flash, pops de fichas y @, golpe en el remate */}
      <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25} />
      <Sfx en={1} src="whoosh-short.mp3" volumen={0.45} />
      <Sfx en={I(m.intro.sparkle)} src="sparkle.mp3" volumen={0.22} />
      <Sfx en={FIN_INTRO - 4} src="whoosh.mp3" volumen={0.4} />
      <Sfx en={FIN_INTRO} src="impact-bass-1.mp3" volumen={0.3} />
      {pops.map((p, i) => (
        <Sfx key={i} en={p.en} src="pop.mp3" volumen={p.v} />
      ))}
      <Sfx en={F(cc, ct)} src="pop.mp3" volumen={0.45} />
      {m.final.golpe ? <Sfx en={F(...m.final.golpe)} src="impact-bass-1.mp3" volumen={0.45} /> : null}
    </AbsoluteFill>
  );
};

// V1/V3/V5 = gancho IMG_1071 ("creadoras") · V2/V4/V6 = gancho IMG_1078 ("favoritas de las mujeres")
// V1/V2: 10 chicas, cierre Jas · V3/V4: 6 chicas, cierre Vivi · V5/V6: 6 chicas, cierre Marina "apunten"
export const PrendaFavComp = () => (
  <>
    {Object.keys(VERSIONES).map((v) => (
      <Composition key={v} id={v === "v1" ? "PrendaFav" : `PrendaFav${v.toUpperCase()}`} component={PrendaFav} defaultProps={{ v }} durationInFrames={MONTAJES[v].DUR} fps={FPS} width={1080} height={1920} />
    ))}
  </>
);
