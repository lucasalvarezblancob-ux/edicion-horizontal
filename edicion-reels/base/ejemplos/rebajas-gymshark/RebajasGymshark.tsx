// "Cómo ahorrar en las rebajas de GYMSHARK" — hablando a cámara, selfie en casa (interior, luz de día).
// Pedido de Lucas (2026-11-15): solo subtítulos, cortes para quitar las retomas (se equivoca varias veces) y que sea
// dinámico pero natural; gancho de texto simple los primeros segundos; ALVAREZ10 resaltado cuando lo dice.
// Luego: 5 variantes para trials (distinto gancho/encuadre/ritmo, para que no se detecte como duplicado); la V1 con un
// título en cada uno de los 3 puntos. Una composición, versión como parámetro (VERSIONES).
// Bruto: bruto terminado/2026-11-15_rebajas-gymshark_01-selfie-casa.MOV (antes bruto/IMG_1466.MOV) (iPhone 4K HDR 60 fps)
// → public/rebajas-gymshark/proxy.mp4 (proxy.sh … 2160 + casa-pantalla.cube: el proxy salía ~12 niveles más claro que
// el bruto en QuickTime; curva medida en 3 instantes con curva.py y validada en otros 2 → 2,1–2,2 niveles).
// Montaje: montaje.json (tramos.py: última toma buena de cada frase, cortes en el silencio medido, pausas ≤ 0,4 s).
// Audio: voz del bruto (≈ 37 dB sobre el ruido) solo highpass 80 → voz.wav ya cortada; −14 LUFS sobre el mp4.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { ACENTO, CREMA, F_FUERTE, F_RELLENO, Sfx } from "../../comun/hablando";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import { Rotulo, RotuloCodigo, SOMBRA_ROTULO } from "../../comun/Rotulos";
import palabrasBruto from "./palabras.json";
import montaje from "./montaje.json";

const S = "rebajas-gymshark";
const FPS = 30;
const SRC = staticFile(`${S}/proxy.mp4`);

const TRAMOS = (montaje.frames as number[][]).map(([desde, dur]) => ({ desde, dur }));
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
const INICIOS = TRAMOS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 0 : acc[i - 1] + TRAMOS[i - 1].dur], []);
const aSalida = (t: number) => {
  for (let i = 0; i < TRAMOS.length; i++) {
    const ini = TRAMOS[i].desde / FPS, fin = (TRAMOS[i].desde + TRAMOS[i].dur) / FPS;
    if (t >= ini - 0.3 && t < fin) return INICIOS[i] / FPS + Math.max(0, t - ini);
  }
  return -1;
};

const W = palabrasBruto as { w: string; start: number; end: number }[];
const CODIGO = 96; // ALVAREZ10
const f = (i: number) => Math.round(aSalida(W[i].start) * FPS);
const EN_CODIGO = f(CODIGO);
const FIN_CODIGO = Math.round(aSalida(W[131].end) * FPS) + 6; // "…ahorraros un diez por ciento extra."
const EN_CODIGO_FINAL = f(311); // "con mi código" (cierre) → hasta el final
const FIN_GANCHO = TRAMOS[0].dur; // toda la 1.ª frase (~7 s): "…al mejor precio posible"
// Los 3 puntos (V1): "Primero…" · "Segundo…" · "Tercero…" (hasta "Mucha suerte").
const PUNTOS = [
  { desde: f(58), hasta: EN_CODIGO, arriba: "primero", texto: "hasta un 60 %" },
  { desde: f(162), hasta: f(217), arriba: "segundo", texto: "restock" },
  { desde: f(217), hasta: f(306), arriba: "tercero", texto: "vuelan las tallas" },
];

type Gancho = { arriba: string; grande: string; de?: string; acento: string };
type Version = {
  gancho: Gancho;
  zoom: "alterna" | "lento" | "entrada";
  base: number; // encuadre base (1 = el del bruto)
  titulos?: boolean;
  subTop: number;
  claves: RegExp;
};
const NADA: RegExp = /(?!)/;
const CIFRAS = /^(cincuenta|sesenta|diez)$/;
export const VERSIONES: Record<string, Version> = {
  v0: { gancho: { arriba: "cómo ahorrar en las", grande: "Rebajas", de: "de", acento: "Gymshark" }, zoom: "alterna", base: 1, subTop: 1300, claves: NADA },
  // V1: un título por cada punto (pedido de Lucas).
  v1: { gancho: { arriba: "cómo ahorrar en las", grande: "Rebajas", de: "de", acento: "Gymshark" }, zoom: "alterna", base: 1, titulos: true, subTop: 1300, claves: NADA },
  v2: { gancho: { arriba: "así puedes ahorrar", grande: "hasta un 60 %", de: "en", acento: "Gymshark" }, zoom: "lento", base: 1.04, subTop: 1320, claves: CIFRAS },
  v3: { gancho: { arriba: "rebajas de gymshark:", grande: "3 cosas", de: "que debes", acento: "saber" }, zoom: "alterna", base: 1.08, subTop: 1340, claves: NADA },
  v4: { gancho: { arriba: "que no te quedes sin", grande: "tu talla", de: "en", acento: "Gymshark" }, zoom: "entrada", base: 1, subTop: 1280, claves: /^(restock|talla|tallas)$/ },
  v5: { gancho: { arriba: "rebajas de gymshark", grande: "+10 % extra", de: "con mi", acento: "código" }, zoom: "lento", base: 1.06, subTop: 1310, claves: CIFRAS },
};

const Pop: React.FC<{ children: React.ReactNode; top: number; dur?: number }> = ({ children, top, dur }) => {
  const frame = useCurrentFrame();
  const s = interpolate(frame, [0, 7], [0.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const oIn = interpolate(frame, [0, 4], [0, 1], { extrapolateRight: "clamp" });
  const oOut = dur ? interpolate(frame, [dur - 5, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top }}>
      <div style={{ transform: `scale(${s})`, opacity: oIn * oOut }}>{children}</div>
    </AbsoluteFill>
  );
};

// Gancho simple, estático encima de la cabeza.
const GanchoTexto: React.FC<{ g: Gancho }> = ({ g }) => {
  const grande: React.CSSProperties = { fontFamily: F_FUERTE, fontSize: 132, textTransform: "uppercase", lineHeight: 0.95, whiteSpace: "nowrap", textShadow: SOMBRA_ROTULO };
  const peque: React.CSSProperties = { fontFamily: F_RELLENO, fontWeight: 600, fontSize: 58, color: CREMA, letterSpacing: -1, textShadow: SOMBRA_ROTULO };
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div style={{ ...peque, marginBottom: 8 }}>{g.arriba}</div>
      <div style={{ ...grande, color: "white" }}>{g.grande}</div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 22, marginTop: 6 }}>
        {g.de ? <span style={peque}>{g.de}</span> : null}
        <span style={{ ...grande, color: ACENTO }}>{g.acento}</span>
      </div>
    </div>
  );
};

const Tramo: React.FC<{ i: number; v: Version; dur: number }> = ({ i, v, dur }) => {
  const frame = useCurrentFrame();
  let s = v.base;
  if (v.zoom === "alterna") s *= i % 2 === 1 ? 1.1 : 1; // salto ×1,1 en cada jump cut (lo esconde)
  if (v.zoom === "lento") s *= interpolate(frame, [0, dur], [1, 1 + 0.012 * (dur / FPS)], { extrapolateRight: "clamp" }); // acercamiento lento, reset en el corte
  if (v.zoom === "entrada") {
    s *= i % 2 === 1 ? 1.08 : 1;
    if (i === 0) s *= interpolate(frame, [0, 27], [1, 1.12], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }) / 1; // zoom de entrada
    if (i === 0) s = Math.max(s, 1);
  }
  return (
    <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: "50% 38%" }}>
      <Video src={SRC} trimBefore={TRAMOS[i].desde} muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

export const RebajasGymshark: React.FC<{ version: string }> = ({ version }) => {
  const v = VERSIONES[version];
  const PALABRAS: Palabra[] = (montaje.keep as number[]).map((i) => {
    const s = aSalida(W[i].start);
    const e = aSalida(W[i].end);
    return { w: W[i].w, start: s, end: e < s ? s + 0.2 : e, clave: i === CODIGO, mayus: i === CODIGO };
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {TRAMOS.map((t, i) => (
        <Sequence key={t.desde} name={`tramo ${i + 1}`} from={INICIOS[i]} durationInFrames={t.dur} premountFor={FPS}>
          <Tramo i={i} v={v} dur={t.dur} />
        </Sequence>
      ))}
      <Audio src={staticFile(`${S}/voz.wav`)} />

      <Sequence name="gancho" from={0} durationInFrames={FIN_GANCHO}>
        <Pop top={250} dur={FIN_GANCHO}>
          <GanchoTexto g={v.gancho} />
        </Pop>
      </Sequence>
      {v.titulos
        ? PUNTOS.map((p) => (
            <Sequence key={p.arriba} name={`título ${p.arriba}`} from={p.desde} durationInFrames={p.hasta - p.desde}>
              <Pop top={300} dur={p.hasta - p.desde}>
                <Rotulo arriba={p.arriba} texto={p.texto} size={140} />
              </Pop>
            </Sequence>
          ))
        : null}
      <Sequence name="código" from={EN_CODIGO} durationInFrames={FIN_CODIGO - EN_CODIGO}>
        <Pop top={300} dur={FIN_CODIGO - EN_CODIGO}>
          <RotuloCodigo />
        </Pop>
      </Sequence>
      <Sequence name="código cierre" from={EN_CODIGO_FINAL}>
        <Pop top={300}>
          <RotuloCodigo />
        </Pop>
      </Sequence>

      <Subtitulos palabras={PALABRAS} offset={0} claves={v.claves} top={v.subTop} />

      <Sfx en={2} src="sparkle.mp3" volumen={0.22} />
      {v.zoom === "entrada" ? <Sfx en={0} src="whoosh-short.mp3" volumen={0.3} /> : null}
      {v.titulos ? PUNTOS.map((p) => <Sfx key={p.arriba} en={p.desde} src="pop.mp3" volumen={0.35} />) : null}
      <Sfx en={EN_CODIGO} src="pop.mp3" volumen={0.45} />
      <Sfx en={EN_CODIGO_FINAL} src="pop.mp3" volumen={0.4} />
    </AbsoluteFill>
  );
};

export const RebajasGymsharkComp: React.FC = () => (
  <>
    {Object.keys(VERSIONES).map((k) => (
      <Composition
        key={k}
        id={k === "v0" ? "RebajasGymshark" : `RebajasGymshark-${k}`}
        component={RebajasGymshark}
        defaultProps={{ version: k }}
        durationInFrames={DUR}
        fps={FPS}
        width={1080}
        height={1920}
      />
    ))}
  </>
);
