import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Sequence,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACENTO, Clave, Palabra, Subtitulos, Titulo, TITLE_FONT } from "../../comun/Subtitulos";
import { RotuloHandle } from "../../comun/Rotulos";
import palabras from "./voz-palabras.json";

// Rutina de movilidad de hombro con banda elástica. 2 ángulos de la misma rutina (brutos en
// "recursos/gym/hombro/2026-11-01_movilidad-hombro-banda_de-espaldas.MOV" y "…_de-frente.MOV"):
//   E = de espaldas (IMG_0467) · F = de frente (IMG_0468)
// Cada clip: dislocaciones (0–11 s) → diagonales (11/12–23 s) → aperturas (22/23–31 s).
// Se alterna E/F cortando en los extremos de cada repetición (arriba / abajo / abierto).
const clip = (c: "E" | "F") => staticFile(`movilidad-hombro/c${c === "E" ? "0467" : "0468"}.mp4`);
const VOZ = staticFile("movilidad-hombro/voz.mp3"); // Alberto Rodríguez ×1,25 sin silencios
const VOZ_DESDE = 3;
const DURACION = 909;

type Plano = {
  name: string;
  c: "E" | "F";
  t: number;
  d: number;
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
};

const PLANOS: Plano[] = [
  // ── Gancho: "Si estabas buscando una rutina de movilidad para tus hombros, la acabas de encontrar."
  { name: "Gancho · F banda arriba", c: "F", t: 7.9, d: 37, punch: 0.18 },
  { name: "Gancho · E bajando por detrás", c: "E", t: 0.5, d: 35, zoom: 1.1 },
  { name: "Gancho · F diagonal", c: "F", t: 12.0, d: 35, zoom: 1.15, origen: "50% 35%" },
  // "Solo necesitas una banda elástica."
  { name: "Banda · F cerrado al pecho", c: "F", t: 28.1, d: 47, zoom: 1.4, origen: "50% 22%" },
  // ── 1 · Dislocaciones (cortes en arriba/abajo)
  { name: "Disloc · F sube", c: "F", t: 1.17, d: 37 },
  { name: "Disloc · E baja", c: "E", t: 3.07, d: 35 },
  { name: "Disloc · F sube (por encima de la cabeza)", c: "F", t: 3.33, d: 39 },
  { name: "Disloc · E baja por detrás de la espalda", c: "E", t: 5.63, d: 38, zoom: 1.15, origen: "50% 40%" },
  { name: "Disloc · F codos estirados", c: "F", t: 5.5, d: 45, zoom: 1.25, origen: "50% 30%" },
  { name: "Disloc · E baja (no es un remo)", c: "E", t: 8.2, d: 42 },
  { name: "Disloc · F manos", c: "F", t: 9.8, d: 31, zoom: 1.35, origen: "50% 40%" },
  // ── 2 · Diagonales
  { name: "Diag · E tira a un lado", c: "E", t: 15.0, d: 34 },
  { name: "Diag · F mano detrás de la cabeza", c: "F", t: 14.3, d: 36, zoom: 1.4, origen: "50% 25%" },
  { name: "Diag · E tira abajo y fuera", c: "E", t: 17.5, d: 49 },
  { name: "Diag · F cambia de lado", c: "F", t: 16.6, d: 25 },
  { name: "Diag · E se abre el pecho", c: "E", t: 20.0, d: 40, zoom: 1.2, origen: "50% 35%" },
  // ── 3 · Aperturas
  { name: "Apert · E cerrado → abierto", c: "E", t: 23.5, d: 45 },
  { name: "Apert · F pecho", c: "F", t: 24.9, d: 42, zoom: 1.25, origen: "50% 35%" },
  { name: "Apert · E escápulas (te debieran dinero)", c: "E", t: 27.0, d: 31, zoom: 1.45, origen: "50% 30%" },
  // ── "Diez repeticiones de cada, dos rondas antes de entrenar"
  { name: "Cifra 10 · E dislocación", c: "E", t: 9.6, d: 38, zoom: 1.1 },
  { name: "Cifra 2 · F diagonal", c: "F", t: 18.0, d: 41, zoom: 1.1 },
  // "y tus hombros te lo van a agradecer" — ráfaga de repaso
  { name: "Repaso · F dislocación arriba", c: "F", t: 4.6, d: 16, zoom: 1.15 },
  { name: "Repaso · E diagonal", c: "E", t: 21.4, d: 16, zoom: 1.15 },
  { name: "Repaso · F apertura", c: "F", t: 27.0, d: 11, zoom: 1.15 },
  // ── Cierre: "Sígueme para más, perra." — cara a cámara, lento
  { name: "Cierre · F cara", c: "F", t: 22.0, d: DURACION - 845, zoom: 1.45, origen: "50% 26%", punch: 0.2, rate: 0.75 },
];

// Transiciones solo en cada cambio de ejercicio (con whoosh)
type Tipo = "pan" | "zoom" | "giro";
const TRANS: [number, Tipo][] = [
  [154, "pan"],
  [421, "giro"],
  [605, "zoom"],
  [802, "pan"],
];
const FLASH = 845;

const CIFRAS: [number, number, string, string][] = [
  [723, 38, "10", "repeticiones de cada"],
  [761, 41, "×2", "rondas antes de entrenar"],
];

const Cifra: React.FC<{ valor: string; texto: string; top?: number }> = ({ valor, texto, top = 250 }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.5, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(2.6)),
  });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top, opacity: o }}>
      <div style={{ transform: `scale(${s})`, textAlign: "center", fontFamily: TITLE_FONT }}>
        <div
          style={{
            fontWeight: 700,
            fontSize: 150,
            lineHeight: 1,
            color: ACENTO,
            letterSpacing: -3,
            textShadow: "0 6px 30px rgba(0,0,0,0.7)",
          }}
        >
          {valor}
        </div>
        <div
          style={{
            fontWeight: 700,
            fontSize: 56,
            color: "white",
            marginTop: 4,
            textShadow: "0 3px 16px rgba(0,0,0,0.85)",
          }}
        >
          {texto}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// "@lucasalvarez.x" con icono de Instagram: entra con pop cuando la voz dice "Sígueme"
const SIGUEME = 846;
export const Handle: React.FC = () => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.5, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.back(2.6)),
  });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 1300, opacity: o }}>
      <div style={{ transform: `scale(${s})` }}>
        <RotuloHandle />
      </div>
    </AbsoluteFill>
  );
};

// Cada plano entra con punch-in y sigue empujando despacio: nunca está quieto.
const Shot: React.FC<{ children: React.ReactNode; punch?: number; zoom?: number; origen?: string }> = ({
  children,
  punch = 0.07,
  zoom = 1,
  origen = "50% 45%",
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 7], [punch, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const drift = frame * 0.0007;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom + p + drift})`, transformOrigin: origen }}>{children}</AbsoluteFill>
  );
};

const efectoTransicion = (frame: number) => {
  let blur = 0;
  let scale = 0;
  let tx = 0;
  let rot = 0;
  for (const [c, tipo] of TRANS) {
    const d = frame - c + 0.5;
    const ad = Math.abs(d);
    const R = 5;
    if (ad >= R) continue;
    const k = 1 - ad / R;
    const k2 = k * k;
    if (tipo === "zoom") {
      blur = Math.max(blur, 16 * k);
      scale = Math.max(scale, 0.16 * k);
    } else if (tipo === "pan") {
      blur = Math.max(blur, 18 * k);
      tx = Math.sign(-d) * -170 * k2;
      scale = Math.max(scale, 0.34 * k);
    } else {
      blur = Math.max(blur, 14 * k);
      rot = Math.sign(d) * 9 * k2;
      scale = Math.max(scale, 0.3 * k);
    }
  }
  return { blur, scale, tx, rot };
};

export const MovilidadHombro: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame);

  const flash = interpolate(frame, [FLASH - 1, FLASH, FLASH + 6], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill
        style={{
          opacity: fadeOut,
          filter: `contrast(1.12) saturate(0.82) brightness(0.96) blur(${blur}px)`,
          transform: `translateX(${tx}px) rotate(${rot}deg) scale(${1 + scale})`,
        }}
      >
        <Series>
          {PLANOS.map((p) => (
            <Series.Sequence key={p.name} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.zoom} origen={p.origen}>
                <Video src={clip(p.c)} trimBefore={Math.round(p.t * fps)} playbackRate={p.rate ?? 1} muted />
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      {/* Viñeta */}
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos */}
      <Sequence name="Título" from={8} durationInFrames={99} layout="none">
        <Titulo titulo="movilidad de hombro" sub="rutina con banda · 3 ejercicios" top={240} />
      </Sequence>
      <Sequence name="1 · dislocaciones" from={154} durationInFrames={267} layout="none">
        <Clave n={1} texto="dislocaciones" />
      </Sequence>
      <Sequence name="2 · diagonales" from={421} durationInFrames={184} layout="none">
        <Clave n={2} texto="diagonales" />
      </Sequence>
      <Sequence name="3 · aperturas" from={605} durationInFrames={118} layout="none">
        <Clave n={3} texto="aperturas" />
      </Sequence>
      {CIFRAS.map(([from, d, valor, texto]) => (
        <Sequence key={from} name={`${valor} · ${texto}`} from={from} durationInFrames={d} layout="none">
          <Cifra valor={valor} texto={texto} />
        </Sequence>
      ))}

      <Sequence name="@lucasalvarez.x" from={SIGUEME} layout="none">
        <Handle />
      </Sequence>

      <Subtitulos
        palabras={palabras as Palabra[]}
        offset={VOZ_DESDE / fps}
        claves={/^(movilidad|hombros|encontrar|banda|dislocaciones|codos|remo|diagonales|cabeza|pecho|aperturas|escápulas|dinero|10|2|agradecer)$/i}
      />

      {/* Audio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={VOZ} volume={1} />
      </Sequence>
      <Sequence name="sfx título" from={6} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      {CIFRAS.map(([from]) => (
        <Sequence key={`pop${from}`} name={`pop ${from}`} from={from} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
        </Sequence>
      ))}
      <Sequence name="pop @" from={SIGUEME} durationInFrames={20} layout="none">
        <Audio src={staticFile("sonidos/pop.mp3")} volume={0.2} />
      </Sequence>
      {TRANS.map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const MovilidadHombroComp = () => (
  <Composition
    id="MovilidadHombro"
    component={MovilidadHombro}
    durationInFrames={DURACION}
    fps={30}
    width={1080}
    height={1920}
  />
);
