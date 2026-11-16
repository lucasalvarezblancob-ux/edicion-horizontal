// "Si fuera tu gym bro, estas son las prendas que te recomendaría comprarte en el Black Friday de Gymshark."
// Hablando a cámara, plano fijo (trípode), Lucas sentado en un banco delante del mural del culturista.
// Bruto: bruto terminado/2026-11-01_gymbro-black-friday_banco-mural-apuntadora.MOV (antes bruto/IMG_1081.MOV) → public/gymbro-black-friday/proxy.mp4 (proxy.sh, colores del bruto sin tocar).
// ⚠️ Con APUNTADORA: una chica le dicta el guion fuera de plano. Scribe diarizado (speaker_1 = Lucas, ≈20 dB más fuerte;
// arreglos a mano en palabras.json: "Primero," y "Y sígueme para más." eran de Lucas) → tomas.json → montar_tomas.py
// --hablante speaker_1 → montaje.json / tramos.json. Audio: aislar-voz.mjs + mezclar_voces.py --hablantes speaker_1
// → voz.wav (misma duración que el bruto, solo la voz de Lucas, −14 LUFS).
// Prendas: best sellers de hombre de eu.gymshark.com/es-ES (2026-11-01). Fichas SIN precio (aún no se saben los del Black Friday).
// Código ALVAREZ10 en "código" y @lucasalvarez.x en "sígueme".
// Música (pedida por Lucas): ElevenLabs Music (scripts/musica.mjs, trap chill 90 BPM) → loudnorm −14 LUFS → musica.mp3.
// Fondo bajo (0,1), hueco de ~0,35 s antes de los remates "de cerca" y "doble", fundido al final.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { ACENTO, Bloque, CamaraVirtual, Encuadre, F_FUERTE, F_RELLENO, Sfx, TextoBloques } from "../../comun/hablando";
import { Subtitulos } from "../../comun/Subtitulos";
import { RotuloCodigo, RotuloHandle } from "../../comun/Rotulos";
import montaje from "./montaje.json";
import tramos from "./tramos.json";

const S = "gymbro-black-friday";
const FPS = 30;
const SRC = staticFile(`${S}/proxy.mp4`);
const VOZ = staticFile(`${S}/voz.wav`);
const MUSICA = staticFile(`${S}/musica.mp3`);

const TRAMOS = tramos as { desde: number; dur: number; nota: string }[];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
const INI = TRAMOS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 0 : acc[i - 1] + TRAMOS[i - 1].dur], []);

// Cara de Lucas (px del proxy): está sentado quieto → centro fijo.
const CARA = { cx: 560, cy: 680 };

const Base: React.FC = () => (
  <Series>
    {TRAMOS.map((t) => (
      <Series.Sequence key={t.desde} name={t.nota.slice(0, 40)} durationInFrames={t.dur} premountFor={FPS}>
        <Video src={SRC} trimBefore={t.desde} muted />
        <Audio src={VOZ} trimBefore={t.desde} />
      </Series.Sequence>
    ))}
  </Series>
);

// ------------------------------------------------------------------ cámara: entrada, empuje lento, reset en cada jump cut, zooms a los remates
const C = CARA;
const ENC: Encuadre[] = [
  { desde: 0, escala: 1.0, ...C },
  { desde: 2, escala: 1.2, suave: 27, empuje: 0.012, ...C }, // zoom de entrada + whoosh
  { desde: INI[1], escala: 1.1, empuje: 0.03, ...C }, // Primero…
  { desde: INI[2], escala: 1.16, empuje: 0.02, ...C },
  { desde: INI[3], escala: 1.08, empuje: 0.02, ...C }, // camuflaje…
  { desde: 386, escala: 1.38, suave: 24, ...C }, // zoom largo que aterriza en "de cerca" (~410)
  { desde: INI[4], escala: 1.08, empuje: 0.03, ...C }, // Segundo…
  { desde: INI[5], escala: 1.15, empuje: 0.02, ...C },
  { desde: INI[6], escala: 1.1, empuje: 0.03, ...C },
  { desde: INI[7], escala: 1.12, empuje: 0.02, ...C }, // Pantalón de culturismo…
  { desde: 601, escala: 1.26, suave: 10, empuje: 0.01, ...C }, // golpe corto en "culturismo" (611)
  { desde: INI[8], escala: 1.08, empuje: 0.03, ...C }, // Y por último…
  { desde: INI[9], escala: 1.1, empuje: 0.02, ...C }, // hombro caído…
  { desde: 786, escala: 1.36, suave: 24, ...C }, // zoom largo que aterriza en "doble" (810)
  { desde: INI[10], escala: 1.1, empuje: 0.03, ...C }, // oferta + código
  { desde: 909, escala: 1.24, suave: 10, empuje: 0.01, ...C }, // golpe en "ALVAREZ10" (919)
  { desde: INI[11], escala: 1.04, ...C },
  { desde: INI[11] + 2, escala: 1.2, suave: 27, ...C }, // punch-in del CTA
];

// ------------------------------------------------------------------ gancho (texto arriba, sobre el mural oscurecido; la cabeza nunca lo tapa)
const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });
const FIN_GANCHO = INI[1];
const GANCHO: Bloque[] = [
  { desde: 0, hasta: 31, y: 0.19, palabras: [P("si fuera tu", 1), P("GYM BRO", 15, "fuerte", true)] },
  { desde: 31, hasta: 108, y: 0.19, palabras: [P("estas son las", 31), P("PRENDAS", 51, "fuerte", true), P("que te recomendaría", 60, "relleno", true), P("comprarte", 88, "remate")] },
  { desde: 108, hasta: FIN_GANCHO, y: 0.19, palabras: [P("en el", 108), P("BLACK FRIDAY", 114, "fuerte", true), P("de Gymshark", 131, "remate", true)] },
];

// degradado oscuro arriba (pared blanca): solo mientras hay texto arriba
const Sombra: React.FC<{ tramos: [number, number][] }> = ({ tramos: t }) => {
  const frame = useCurrentFrame();
  const o = Math.max(
    ...t.map(([a, b]) => interpolate(frame, [a, a + 6, b - 6, b], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })),
  );
  return o ? (
    <AbsoluteFill style={{ opacity: o, background: "linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.55) 22%, rgba(0,0,0,0) 36%)" }} />
  ) : null;
};

// ------------------------------------------------------------------ fichas de producto (foto oficial de Gymshark, sin precio)
type Ficha = { nombre: string; info: string; img: string; img2?: { src: string; en: number }; en: number; sale: number; lado: "izq" | "der"; giro: number; n: string };
const FICHAS: Ficha[] = [
  { nombre: "Geo Seamless T-Shirt", info: "Black/Charcoal Grey", img: "geo-seamless-tshirt-black", img2: { src: "geo-seamless-tshirt-black-detalle", en: 365 }, en: 199, sale: INI[4], lado: "izq", giro: -3, n: "1" },
  { nombre: "Pumper Pants", info: "Black", img: "pumper-pants-black", img2: { src: "pumper-pants-black-parche", en: 554 }, en: 451, sale: INI[8], lado: "der", giro: 3, n: "2" },
  { nombre: "Crest Oversized Hoodie", info: "Black", img: "crest-oversized-hoodie-black", en: 702, sale: INI[10], lado: "izq", giro: -3, n: "3" },
];

const ANCHO = 290;
const FichaProducto: React.FC<{ f: Ficha }> = ({ f }) => {
  const frame = useCurrentFrame();
  const sale = f.sale - 6; // la salida acaba en el corte
  if (frame < f.en || frame > sale + 6) return null;
  const e = interpolate(frame, [f.en, f.en + 7], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const k = e * s;
  const flota = Math.sin((frame - f.en) / 10) * 5;
  // cambio a la foto de detalle (camuflaje / parche): fundido + pequeño rebote
  const d = f.img2 ? interpolate(frame, [f.img2.en, f.img2.en + 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const rebote = f.img2 ? 1 + 0.05 * Math.sin(Math.PI * interpolate(frame, [f.img2.en, f.img2.en + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })) : 1;
  const cx = f.lado === "izq" ? 172 : 908; // pegadas al borde: la cabeza nunca queda debajo, ni con el zoom de 1,38
  const alto = Math.round(ANCHO * 1.19);
  const foto: React.CSSProperties = { position: "absolute", inset: 0, width: ANCHO, height: alto, objectFit: "cover", display: "block" };
  return (
    <div
      style={{
        position: "absolute", left: cx, top: 420 + flota, width: ANCHO,
        transform: `translateX(-50%) scale(${k * rebote}) rotate(${f.giro + (1 - e) * -8}deg)`, transformOrigin: "50% 40%",
        opacity: Math.min(1, k * 1.6), background: "white", borderRadius: 22, overflow: "hidden",
        boxShadow: "0 18px 40px rgba(0,0,0,0.5), 0 0 0 3px rgba(255,255,255,0.9)",
      }}
    >
      <div style={{ position: "relative", width: ANCHO, height: alto }}>
        <Img src={staticFile(`${S}/prendas/${f.img}.jpg`)} style={foto} />
        {f.img2 ? <Img src={staticFile(`${S}/prendas/${f.img2.src}.jpg`)} style={{ ...foto, opacity: d }} /> : null}
      </div>
      <div style={{ padding: "12px 16px 14px", color: "#111" }}>
        <div style={{ fontFamily: F_FUERTE, fontSize: 32, lineHeight: 1.02, textTransform: "uppercase", letterSpacing: 0.3 }}>{f.nombre}</div>
        <div style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: 20, color: "#8a8a8a", marginTop: 4 }}>{f.info}</div>
        {/* sin precio: aún no se saben los del Black Friday (Lucas, 2026-11-01) */}
      </div>
      <div style={{ position: "absolute", left: 12, top: 12, fontFamily: F_FUERTE, fontSize: 20, letterSpacing: 2, color: "#111", background: "white", padding: "4px 10px", borderRadius: 6 }}>
        GYMSHARK
      </div>
      <div
        style={{
          position: "absolute", right: 12, top: 10, width: 72, height: 72, borderRadius: 36, background: ACENTO, color: "#111",
          display: "flex", alignItems: "center", justifyContent: "center", fontFamily: F_FUERTE, fontSize: 44,
          transform: `scale(${interpolate(frame, [f.en + 7, f.en + 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(3)) })})`,
          boxShadow: "0 6px 16px rgba(0,0,0,0.4)",
        }}
      >
        {f.n}
      </div>
    </div>
  );
};

// ------------------------------------------------------------------ código de descuento (arriba, encima de la cabeza; se queda hasta el final)
const EN_CODIGO = 903; // "código"
const Codigo: React.FC<{ en: number }> = ({ en }) => {
  const frame = useCurrentFrame();
  if (frame < en) return null;
  const e = interpolate(frame, [en, en + 8], [0.4, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.6)) });
  const o = interpolate(frame, [en, en + 3], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 300, opacity: o }}>
      <div style={{ transform: `scale(${e})` }}>
        <RotuloCodigo />
      </div>
    </AbsoluteFill>
  );
};

// @ de Instagram en "Sígueme" (debajo de los subtítulos, hasta el final)
const EN_SIGUEME = 947;
const Handle: React.FC<{ en: number }> = ({ en }) => {
  const frame = useCurrentFrame();
  if (frame < en) return null;
  const s = interpolate(frame - en, [0, 7], [0.5, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.6)) });
  const o = interpolate(frame - en, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 1300, opacity: o }}>
      <div style={{ transform: `scale(${s})` }}>
        <RotuloHandle />
      </div>
    </AbsoluteFill>
  );
};

// ------------------------------------------------------------------ subtítulos (después del gancho)
const ARREGLOS: Record<string, string> = { "Pamper": "Pumper", "gymbro,": "gym bro," };
const PALABRAS = (montaje.palabras as { w: string; start: number; end: number }[]).map((p) => ({ ...p, w: ARREGLOS[p.w] ?? p.w }));
const CLAVES = /^(geo|seamless|pumper|pants|crest|oversized|camuflaje|parche|culturista|doble|alvarez10)$/i;

// Música de fondo baja: se corta ~0,35 s antes de cada remate y vuelve justo después; fundido de salida.
const REMATES = [407, 810]; // "de cerca", "doble"
const volMusica = (f: number) => {
  let v = 0.1;
  for (const r of REMATES) {
    v = Math.min(v, interpolate(f, [r - 13, r - 10, r + 2, r + 10], [0.1, 0.015, 0.015, 0.1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  }
  return v * interpolate(f, [DUR - 24, DUR], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

export const GymbroBlackFriday: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* colores originales del bruto: sin etalonado */}
      <CamaraVirtual encuadres={ENC} shake={[{ desde: 810, hasta: 820, px: 7 }]}>
        <Base />
      </CamaraVirtual>
      <Sombra tramos={[[0, FIN_GANCHO], [EN_CODIGO, DUR + 6]]} />
      <TextoBloques bloques={GANCHO} pop escala={0.8} />
      {FICHAS.map((f) => (
        <FichaProducto key={f.n} f={f} />
      ))}
      <AbsoluteFill style={{ opacity: frame >= FIN_GANCHO ? 1 : 0 }}>
        <Subtitulos palabras={PALABRAS.filter((p) => p.start * FPS >= FIN_GANCHO - 1)} offset={0} claves={CLAVES} maxHueco={0.6} />
      </AbsoluteFill>
      <Codigo en={EN_CODIGO} />
      <Handle en={EN_SIGUEME} />
      {/* sonido con moderación: entrada, título, una ficha por prenda, remates, código y CTA */}
      <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25} />
      <Sfx en={1} src="whoosh-short.mp3" volumen={0.45} />
      <Sfx en={15} src="sparkle.mp3" volumen={0.22} />
      {FICHAS.map((f) => (
        <Sfx key={f.n} en={f.en} src="pop.mp3" volumen={0.5} />
      ))}
      {FICHAS.filter((f) => f.img2).map((f) => (
        <Sfx key={`d${f.n}`} en={f.img2!.en} src="click-soft.mp3" volumen={0.35} />
      ))}
      <Sfx en={810} src="impact-bass-1.mp3" volumen={0.45} />
      <Sfx en={EN_CODIGO} src="pop.mp3" volumen={0.45} />
      <Sfx en={EN_SIGUEME} src="pop.mp3" volumen={0.35} />
      <Audio src={MUSICA} volume={volMusica} />
    </AbsoluteFill>
  );
};

export const GymbroBlackFridayComp = () => (
  <Composition id="GymbroBlackFriday" component={GymbroBlackFriday} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
