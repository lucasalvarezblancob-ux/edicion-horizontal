// "Si te estás preparando para una maratón o una media y no quieres desmayarte en las tiradas largas,
//  este es el consejo que a mí me ha servido más como principiante. Desayuna fuerte."
// Hablando a cámara, plano fijo (trípode), Lucas sentado delante de la estantería, micro de solapa.
// Bruto: bruto terminado/2026-11-01_desayuna-fuerte_01-sentado-estanteria.MOV (antes bruto/IMG_1084.MOV) → public/desayuna-fuerte/proxy.mp4 (proxy.sh, colores del bruto sin tocar).
// Una sola voz (sin apuntador): Scribe → tomas.json (frases buenas; fuera las repeticiones "a mitad de la…" y
// "y te lo digo por experiencia, porque…") → montar_tomas.py → montaje.json / tramos.json.
// Audio: voz del bruto normalizada (highpass + loudnorm −14 LUFS) → public/desayuna-fuerte/voz.wav.
// Fotos (Wikimedia Commons, ver recursos/fotos/CREDITS.md): tortitas de maíz (tachadas), plátano, tortitas con miel.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { ACENTO, Bloque, CamaraVirtual, Encuadre, Sfx, TextoBloques } from "../../comun/hablando";
import { Subtitulos } from "../../comun/Subtitulos";
import { RotuloHandle } from "../../comun/Rotulos";
import montaje from "./montaje.json";
import tramos from "./tramos.json";

const S = "desayuna-fuerte";
const FPS = 30;
const SRC = staticFile(`${S}/proxy.mp4`);
const VOZ = staticFile(`${S}/voz.wav`);

const TRAMOS = tramos as { desde: number; dur: number; nota: string }[];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
const INI = TRAMOS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 0 : acc[i - 1] + TRAMOS[i - 1].dur], []);
// INI = [0, 240, 293, 367, 436, 503, 700]

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

// ------------------------------------------------------------------ cámara
// Cara en x≈590, coronilla en y≈410 del proxy. Centro del zoom por ENCIMA de la cabeza (cy=300): el zoom se mete en la
// cara sin subir la cabeza hacia el texto de arriba (la coronilla se queda en y≈380–410 con cualquier escala).
const C = { cx: 590, cy: 300 };
const ENC: Encuadre[] = [
  { desde: 0, escala: 1.0, ...C },
  { desde: 2, escala: 1.15, suave: 27, empuje: 0.01, ...C }, // zoom de entrada + whoosh
  { desde: 76, escala: 1.1, empuje: 0.03, ...C }, // y no quieres desmayarte…
  { desde: 145, escala: 1.14, empuje: 0.02, ...C }, // este es el consejo…
  { desde: INI[1], escala: 1.06, ...C },
  { desde: 249, escala: 1.34, suave: 24, ...C }, // zoom largo que aterriza en "FUERTE" (273)
  { desde: INI[2], escala: 1.08, empuje: 0.03, ...C }, // No vale con… tortitas de maíz
  { desde: INI[3], escala: 1.12, empuje: 0.02, ...C }, // Métete un plátano…
  { desde: INI[4], escala: 1.1, empuje: 0.02, ...C }, // para que no te dé un chungo…
  { desde: 450, escala: 1.24, suave: 10, empuje: 0.01, ...C }, // golpe corto en "chungo" (459)
  { desde: INI[5], escala: 1.08, empuje: 0.03, ...C }, // Y te lo digo por experiencia…
  { desde: 599, escala: 1.12, empuje: 0.02, ...C }, // en el kilómetro 11…
  { desde: 622, escala: 1.36, suave: 22, ...C }, // zoom largo que aterriza en "desmayo" (644)
  { desde: INI[6], escala: 1.04, ...C },
  { desde: INI[6] + 2, escala: 1.2, suave: 27, ...C }, // punch-in del CTA
];

// ------------------------------------------------------------------ textos
const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });
const Y_ARRIBA = 0.155; // franja entre la UI de arriba y la coronilla
const GANCHO: Bloque[] = [
  { desde: 0, hasta: 76, y: Y_ARRIBA, palabras: [P("si", 2), P("te", 5), P("estás", 7), P("preparando", 14), P("MARATÓN", 40, "fuerte", true), P("o una media", 58, "remate")] },
  { desde: 76, hasta: 107, y: Y_ARRIBA, palabras: [P("y no quieres", 76), P("DESMAYARTE", 91, "fuerte", true)] },
  { desde: 107, hasta: 145, y: Y_ARRIBA, palabras: [P("en las", 107), P("TIRADAS", 116, "fuerte", true), P("LARGAS", 128, "fuerte")] },
  { desde: 145, hasta: 208, y: Y_ARRIBA, palabras: [P("este es el", 145), P("consejo", 157), P("que más me ha servido", 190, "remate", true)] },
  { desde: 208, hasta: INI[1], y: Y_ARRIBA, palabras: [P("como", 208), P("PRINCIPIANTE", 215, "fuerte", true)] },
];
// el consejo, grande sobre el pecho
const CONSEJO: Bloque[] = [{ desde: INI[1], hasta: INI[2], y: 0.5, palabras: [P("desayuna", 243, "clave"), P("FUERTE", 273, "fuerte", true)] }];
// cifras de la anécdota, arriba
const CIFRAS: Bloque[] = [
  { desde: 563, hasta: 605, y: Y_ARRIBA, palabras: [P("26", 566, "fuerte"), P("KM", 581, "fuerte")] },
  { desde: 605, hasta: INI[6], y: Y_ARRIBA, palabras: [P("KM", 605, "fuerte"), P("11", 620, "fuerte")] },
];

// degradado oscuro arriba (estantería clara): solo mientras hay texto arriba
const Sombra: React.FC<{ tramos: [number, number][] }> = ({ tramos: t }) => {
  const frame = useCurrentFrame();
  const o = Math.max(
    ...t.map(([a, b]) => interpolate(frame, [a, a + 6, b - 6, b], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })),
  );
  return o ? (
    <AbsoluteFill style={{ opacity: o, background: "linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.55) 16%, rgba(0,0,0,0) 24%)" }} />
  ) : null;
};

// ------------------------------------------------------------------ fotos de comida (pequeñas, a los lados de la cabeza, con pop)
type Foto = { src: string; entra: number; sale: number; cx: number; cy: number; ancho: number; giro: number; marca: "no" | "si"; tacha?: number };
const FOTOS: Foto[] = [
  { src: "tortitas-maiz_recorte.png", entra: 334, sale: INI[4], cx: 220, cy: 540, ancho: 290, giro: -6, marca: "no", tacha: 352 },
  { src: "platano_recorte.png", entra: 385, sale: INI[4], cx: 870, cy: 450, ancho: 300, giro: 6, marca: "si" },
  { src: "tortitas-miel_recorte.png", entra: 413, sale: INI[4], cx: 880, cy: 630, ancho: 320, giro: -3, marca: "si" },
];

const FotoComida: React.FC<{ f: Foto }> = ({ f }) => {
  const frame = useCurrentFrame();
  const sale = f.sale - 6; // la salida acaba en el corte
  if (frame < f.entra - 1 || frame > sale + 6) return null;
  const e = interpolate(frame, [f.entra - 1, f.entra + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const k = e * s;
  const flota = Math.sin((frame - f.entra) / 9) * 6;
  const t = f.tacha !== undefined ? interpolate(frame, [f.tacha, f.tacha + 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
  const badge = interpolate(frame, [f.entra + 4, f.entra + 11], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(3)) });
  const barra = (giro: number): React.CSSProperties => ({
    position: "absolute", left: "50%", top: "50%", width: f.ancho * 1.05 * t, height: 22, borderRadius: 11, background: "white",
    transform: `translate(-50%, -50%) rotate(${giro}deg)`, boxShadow: "0 4px 14px rgba(0,0,0,0.7)",
  });
  return (
    <div
      style={{
        position: "absolute", left: f.cx, top: f.cy + flota, width: f.ancho,
        transform: `translate(-50%, -50%) scale(${k}) rotate(${f.giro + (1 - e) * -10}deg)`, opacity: Math.min(1, k * 1.6),
      }}
    >
      <Img
        src={staticFile(`${S}/fotos/${f.src}`)}
        style={{
          width: "100%",
          filter: `grayscale(${t}) brightness(${1 - 0.25 * t}) drop-shadow(0 0 3px rgba(0,0,0,0.9)) drop-shadow(0 16px 26px rgba(0,0,0,0.7))`,
        }}
      />
      {t > 0 ? (
        <>
          <div style={barra(35)} />
          <div style={barra(-35)} />
        </>
      ) : null}
      {f.marca === "si" ? (
        <div
          style={{
            position: "absolute", right: -18, top: -22, width: 64, height: 64, borderRadius: 32, background: ACENTO,
            display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${badge})`, boxShadow: "0 6px 16px rgba(0,0,0,0.45)",
          }}
        >
          <svg width={38} height={38} viewBox="0 0 24 24" fill="none" stroke="#141414" strokeWidth={3.4} strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12.5l4.5 4.5L19 7.5" />
          </svg>
        </div>
      ) : null}
    </div>
  );
};

// @ de Instagram en "Sígueme" (debajo de los subtítulos, hasta el final)
const EN_SIGUEME = 745;
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

// ------------------------------------------------------------------ subtítulos (después de "Desayuna fuerte", que va en grande)
// "plato": Scribe y Whisper lo oyen así; en el guion es "plátano" (y la foto es un plátano).
const ARREGLOS: Record<string, string> = { plato: "plátano", veintiséis: "26", once: "11" };
const PALABRAS = (montaje.palabras as { w: string; start: number; end: number }[]).map((p) => ({ ...p, w: ARREGLOS[p.w] ?? p.w }));
const DESDE_SUBS = INI[2];
const CLAVES = /^(tortitas|maíz|plátano|miel|chungo|26|11|desmayo|poco|sígueme)$/i;

export const DesayunaFuerte: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    {/* colores originales del bruto: sin etalonado */}
    <CamaraVirtual encuadres={ENC} shake={[{ desde: 273, hasta: 283, px: 6 }, { desde: 644, hasta: 654, px: 6 }]}>
      <Base />
    </CamaraVirtual>
    <Sombra tramos={[[0, INI[1]], [563, INI[6]]]} />
    <TextoBloques bloques={GANCHO} pop escala={0.82} />
    <TextoBloques bloques={CONSEJO} pop escala={1.25} sombra="0 6px 30px rgba(0,0,0,0.75), 0 2px 6px rgba(0,0,0,0.7)" />
    <TextoBloques bloques={CIFRAS} pop escala={0.9} />
    {FOTOS.map((f) => (
      <FotoComida key={f.src} f={f} />
    ))}
    <Subtitulos palabras={PALABRAS.filter((p) => p.start * FPS >= DESDE_SUBS - 1)} offset={0} claves={CLAVES} maxHueco={0.6} />
    <Handle en={EN_SIGUEME} />
    {/* sonido con moderación: entrada, título, remates, una foto = un pop, cifra y CTA */}
    <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25} />
    <Sfx en={1} src="whoosh-short.mp3" volumen={0.45} />
    <Sfx en={2} src="sparkle.mp3" volumen={0.22} />
    <Sfx en={273} src="impact-bass-1.mp3" volumen={0.45} />
    {FOTOS.map((f) => (
      <Sfx key={f.src} en={f.entra} src="pop.mp3" volumen={0.45} />
    ))}
    <Sfx en={352} src="click-soft.mp3" volumen={0.4} />
    <Sfx en={566} src="pop.mp3" volumen={0.3} />
    <Sfx en={644} src="impact-bass-1.mp3" volumen={0.45} />
    <Sfx en={EN_SIGUEME} src="pop.mp3" volumen={0.35} />
  </AbsoluteFill>
);

export const DesayunaFuerteComp = () => (
  <Composition id="DesayunaFuerte" component={DesayunaFuerte} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
