// "Black Friday de GYMSHARK" — hablando a cámara, selfie andando por la calle (exterior, sol).
// Edición MUY SIMPLE pedida por Lucas (2026-11-06): sin cortes salvo UNO (fuera la retoma "y id guardando,"
// entre "guárdaos este vídeo" e "y id guardándoos…"), gancho de texto ESTÁTICO encima de la cabeza los 5 primeros
// segundos, subtítulos palabra a palabra con la FECHA y el CÓDIGO resaltados (acento + rótulo arriba).
// Bruto: bruto terminado/2026-11-06_black-friday-gymshark_01-selfie-andando-calle.MOV (antes bruto/IMG_1191.MOV) (iPhone 4K HDR 60 fps) → public/black-friday-gymshark/proxy.mp4 (proxy.sh … 2160).
// Color medido en QuickTime bruto vs proxy: 3,7–5,4 niveles → sin corrección extra.
// Audio: su voz del bruto, solo highpass 80 (voz ≈ 18 dB sobre el ruido de calle), → voz.wav ya con el corte;
// volumen final −14 LUFS con ganancia fija + limitador sobre el mp4.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { ACENTO, CREMA, F_FUERTE, F_RELLENO, Sfx } from "../../comun/hablando";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import { RotuloCodigo, SOMBRA_ROTULO } from "../../comun/Rotulos";
import palabrasBruto from "./palabras.json";

const S = "black-friday-gymshark";
const FPS = 30;
const SRC = staticFile(`${S}/proxy.mp4`);

// Dos tramos del bruto (frames a 30 fps). El corte quita "y id guardando," (palabras 99–101).
const TRAMOS = [
  { desde: 15, dur: 886, nota: "intro → guárdaos este vídeo" }, // 0,50 → 30,03 s
  { desde: 992, dur: 142, nota: "y id guardándoos → nada" }, // 33,07 → 37,80 s
];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
const aSalida = (t: number) => {
  let acc = 0;
  for (const tr of TRAMOS) {
    const ini = tr.desde / FPS, fin = (tr.desde + tr.dur) / FPS;
    if (t >= ini - 0.3 && t < fin + 0.3) return acc + (t - ini);
    acc += tr.dur / FPS;
  }
  return -1;
};

const FECHA = [45, 55]; // "15 de noviembre a las cinco de la tarde, hora española"
const CODIGO = 93; // ALVAREZ10
const QUITAR = [99, 100, 101];
const W = palabrasBruto as { w: string; start: number; end: number }[];
const PALABRAS: Palabra[] = W.map((p, i) => ({
  w: p.w,
  start: aSalida(p.start),
  end: aSalida(p.end),
  clave: (i >= FECHA[0] && i <= FECHA[1]) || i === CODIGO,
  mayus: i === CODIGO,
})).filter((_, i) => !QUITAR.includes(i));

const f = (i: number) => Math.round(aSalida(W[i].start) * FPS);
const EN_FECHA = f(45);
const EN_HORA = f(50); // "cinco"
const FIN_FECHA = Math.round(aSalida(W[66].end) * FPS) + 8; // tras "año."
const EN_CODIGO = f(CODIGO);
// 2026-11-07: el gancho aparece después de "…las fechas de las rebajas", justo en "del Black Friday de Gymshark"
// (Lucas: "que aparezca un poco más tarde"). Sigue quitándose a los 5 s.
const EN_GANCHO = f(9); // "del"
const FIN_GANCHO = 5 * FPS;

const NADA: RegExp = /(?!)/;

const Pop: React.FC<{ children: React.ReactNode; top: number }> = ({ children, top }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const o = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top }}>
      <div style={{ transform: `scale(${s})`, opacity: o }}>{children}</div>
    </AbsoluteFill>
  );
};

// Gancho estático encima de la cabeza (la cabeza no sube de y ≈ 650 en los 5 primeros s).
const Gancho: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [FIN_GANCHO - EN_GANCHO - 5, FIN_GANCHO - EN_GANCHO], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const grande: React.CSSProperties = { fontFamily: F_FUERTE, fontSize: 132, textTransform: "uppercase", lineHeight: 0.95, whiteSpace: "nowrap", textShadow: SOMBRA_ROTULO };
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 300, opacity: o }}>
      <div style={{ ...grande, color: "white" }}>Black Friday</div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 22, marginTop: 6 }}>
        <span style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: 58, color: CREMA, letterSpacing: -1, textShadow: SOMBRA_ROTULO }}>de</span>
        <span style={{ ...grande, color: ACENTO }}>Gymshark</span>
      </div>
    </AbsoluteFill>
  );
};

const RotuloFecha: React.FC = () => {
  const frame = useCurrentFrame();
  const oh = interpolate(frame, [EN_HORA - EN_FECHA, EN_HORA - EN_FECHA + 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Pop top={320}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ fontFamily: F_FUERTE, fontSize: 138, color: ACENTO, textTransform: "uppercase", lineHeight: 0.95, whiteSpace: "nowrap", textShadow: SOMBRA_ROTULO }}>
          15 de noviembre
        </div>
        <div style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: 56, color: CREMA, letterSpacing: -1, marginTop: 10, opacity: oh, textShadow: SOMBRA_ROTULO }}>
          17:00 h · hora española
        </div>
      </div>
    </Pop>
  );
};

export const BlackFridayGymshark: React.FC = () => {
  let acc = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {TRAMOS.map((t) => {
        const from = acc;
        acc += t.dur;
        return (
          <Sequence key={t.desde} name={t.nota} from={from} durationInFrames={t.dur} premountFor={FPS}>
            <Video src={SRC} trimBefore={t.desde} muted style={{ width: "100%", height: "100%" }} />
          </Sequence>
        );
      })}
      <Audio src={staticFile(`${S}/voz.wav`)} />

      <Sequence name="gancho" from={EN_GANCHO} durationInFrames={FIN_GANCHO - EN_GANCHO}>
        <Gancho />
      </Sequence>
      <Sequence name="fecha" from={EN_FECHA} durationInFrames={FIN_FECHA - EN_FECHA}>
        <RotuloFecha />
      </Sequence>
      <Sequence name="código" from={EN_CODIGO}>
        <Pop top={330}>
          <RotuloCodigo />
        </Pop>
      </Sequence>

      {/* top 1420 (no 1180): en este selfie la cara es grande y a 1180 el subtítulo caía en boca/barbilla.
          Lucas: "baja un poco los subtítulos, que no me tapen la cara". Por debajo de la barbilla y encima de la UI (1500). */}
      <Subtitulos palabras={PALABRAS} offset={0} claves={NADA} top={1420} />

      <Sfx en={EN_GANCHO} src="sparkle.mp3" volumen={0.22} />
      <Sfx en={EN_FECHA} src="pop.mp3" volumen={0.4} />
      <Sfx en={EN_CODIGO} src="pop.mp3" volumen={0.45} />
    </AbsoluteFill>
  );
};

export const BlackFridayGymsharkComp: React.FC = () => (
  <Composition id="BlackFridayGymshark" component={BlackFridayGymshark} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
