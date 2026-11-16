// bicep-fah — sketch de humor (Lucas + chica en el gym). "¿Qué estás haciendo con ella?" → "Bíceps." + sonido FAH.
// Bruto: bruto terminado/2026-11-01_bicep-fah_01-sketch-mancuerna.MOV (era IMG_1077, 20,5 s, HDR 4K 60 fps).
// Proxy 4K con `herramientas/proxy.sh BRUTO proxy-4k.mp4 2160` (conversión de Apple + hdr-pantalla.cube). Render con --scale=2 → 2160×3840.
// Audio: diálogo del bruto (highpass + loudnorm −14 LUFS) → public/bicep-fah/voz.wav. FAH: YouTube -vH2b55TSHI → fah.wav.
// Montaje: un solo corte (pausa 3,32–3,82 s). Planos = cámara virtual que enfoca a quien habla/reacciona.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Series, staticFile, useCurrentFrame } from "remotion";
import { ACENTO, Encuadre, F_FUERTE, F_RELLENO, Sfx } from "../../comun/hablando";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import palabras from "./palabras.json";

const S = "bicep-fah";
const FPS = 30;
const SRC = staticFile(`${S}/proxy-4k.mp4`);
const VOZ = staticFile(`${S}/voz.wav`);

// Tramos del bruto (frames a 30 fps)
const TRAMOS = [
  { desde: 35, dur: 65, nota: "Perdona, ¿la estás usando? · Sí, ¿por?" },
  { desde: 115, dur: 498, nota: "¿Qué estás haciendo con ella? · Bíceps (FAH) · … se sienta en la mancuerna" },
];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
// segundo del bruto → frame del edit
const ed = (s: number) => Math.round(s < 3.5 ? s * 30 - 35 : s * 30 - 50);

const Base: React.FC = () => (
  <Series>
    {TRAMOS.map((t) => (
      <Series.Sequence key={t.desde} name={t.nota} durationInFrames={t.dur} premountFor={FPS}>
        <Video src={SRC} trimBefore={t.desde} muted style={{ width: "100%", height: "100%" }} />
        <Audio src={VOZ} trimBefore={t.desde} />
      </Series.Sequence>
    ))}
  </Series>
);

// ------------------------------------------------------------------ cámara (coordenadas en px 1080×1920)
// Caras medidas con rejilla: Lucas a la izquierda (x≈280–390, y≈720), ella a la derecha (x≈700–765, y≈830 de pie;
// y≈1090–1120 sentada en la mancuerna). La cámara va a pulso y deriva un poco a la izquierda → centros por tramo.
const ENC: Encuadre[] = [
  { desde: 0, escala: 1.0, cx: 500, cy: 760 },
  { desde: 2, escala: 1.22, suave: 27, empuje: 0.01, cx: 500, cy: 760 }, // zoom de entrada + whoosh (los dos)
  { desde: ed(3.82), escala: 1.85, empuje: 0.025, cx: 390, cy: 730 }, // ÉL: "Pero ¿qué estás haciendo con ella?"
  { desde: ed(5.3), escala: 2.0, cx: 765, cy: 830 }, // ELLA: "Bíceps."
  { desde: ed(5.6), escala: 2.8, suave: 4, empuje: 0.02, cx: 765, cy: 820 }, // golpe de zoom con el FAH
  { desde: ed(6.55), escala: 2.0, empuje: 0.03, cx: 355, cy: 725 }, // ÉL: "¿Cómo que bíceps?"
  { desde: ed(7.55), escala: 2.0, empuje: 0.02, cx: 700, cy: 825 }, // ELLA: "Sí. ¿Qué pasa?"
  { desde: ed(8.32), escala: 1.9, empuje: 0.03, cx: 330, cy: 712 }, // ÉL: "Pero si eso no lo levanto yo."
  { desde: ed(9.62), escala: 1.5, empuje: 0.02, cx: 560, cy: 860 }, // ELLA: "¿No te lo crees? Ya verás."
  { desde: ed(10.68), escala: 1.05, empuje: 0.02, cx: 470, cy: 900 }, // abierto: se sienta en la mancuerna
  { desde: ed(13.3), escala: 1.8, empuje: 0.02, cx: 520, cy: 1150 }, // ELLA: "Vamos" + curl con la mancuernita
  { desde: ed(14.3), escala: 2.2, empuje: 0.02, cx: 125, cy: 740 }, // ÉL: facepalm
  { desde: ed(16.1), escala: 1.8, empuje: 0.02, cx: 620, cy: 1130 }, // ELLA: sigue con el curl
  { desde: ed(17.3), escala: 1.15, empuje: 0.015, cx: 430, cy: 900 }, // él se va
  { desde: ed(19.0), escala: 1.6, cx: 780, cy: 1080 }, // ella se ríe → zoom final (lo lleva FINAL) + "SÍGUENOS"
];

// Cámara que CENTRA a la persona: lleva (cx,cy) a (540, Y_CARA) — CamaraVirtual de comun/ hace zoom HACIA el punto
// pero lo deja donde está, y aquí las caras están en los lados del plano. Recorta sin dejar bordes vacíos.
const Y_CARA = 700;
// Zoom final continuo a su cara mientras se ríe (la cámara a pulso se mueve: el centro sigue su cara, medida a 19,0/19,5/20,0/20,4 s)
const FIN_DESDE = ed(19.0);
const FINAL = (f: number) => ({
  s: interpolate(f, [FIN_DESDE, DUR], [1.6, 2.6], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.sin) }),
  cx: interpolate(f, [ed(19.0), ed(19.5), ed(20.0), ed(20.4)], [780, 780, 810, 730], { extrapolateRight: "clamp" }),
  cy: interpolate(f, [ed(19.0), ed(20.0), ed(20.4)], [1080, 1080, 1110], { extrapolateRight: "clamp" }),
});

const Camara: React.FC<{ encuadres: Encuadre[]; children: React.ReactNode }> = ({ encuadres, children }) => {
  const frame = useCurrentFrame();
  let i = 0;
  for (let k = 0; k < encuadres.length; k++) if (frame >= encuadres[k].desde) i = k;
  const e = encuadres[i];
  const prev = encuadres[Math.max(0, i - 1)];
  const k = e.suave && i > 0 ? interpolate(frame, [e.desde, e.desde + e.suave], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }) : 1;
  const mezcla = (a: number, b: number) => a + (b - a) * k;
  const fin = frame >= FIN_DESDE ? FINAL(frame) : null;
  const s = fin ? fin.s : mezcla(prev.escala, e.escala) * (1 + (e.empuje ?? 0) * (frame - e.desde) / 30);
  const cx = fin ? fin.cx : mezcla(prev.cx ?? 540, e.cx ?? 540);
  const cy = fin ? fin.cy : mezcla(prev.cy ?? 960, e.cy ?? 960);
  const lim = (v: number, m: number) => Math.max(-m, Math.min(m, v));
  const tx = lim(-(cx - 540) * s, (s - 1) * 540);
  const ty = lim(Y_CARA - 960 - (cy - 960) * s, (s - 1) * 960);
  return <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${s})` }}>{children}</AbsoluteFill>;
};

// ------------------------------------------------------------------ subtítulos (tiempo del edit)
// Sin los gruñidos del final ("uah", "bah"…). palabras.json = Scribe re-pasado POR TRAMOS (1,3–7,4 · 7,3–9,8 · 8,1–11,1):
// el pase entero (palabras-scribe.json) ponía "¿Qué pasa?" pegado a "Sí" (7,78 en vez de 8,16), metía un "Pero" y amontonaba
// "¿No te lo crees?" en 10,22. Retocado a mano: "Bíceps" con tilde, "¿Cómo" en 6,62 (energía; Scribe lo estiraba desde 5,76).
const PALABRAS: Palabra[] = (palabras as Palabra[])
  .filter((p) => p.start < 10.6 || /vamos/i.test(p.w))
  .map((p) => ({ w: p.w, start: ed(p.start) / FPS, end: ed(p.end) / FPS }));

// Volumen del FAH: entero mientras nadie habla y baja cuando él contesta "¿Cómo que bíceps?" (≈ 1 s después)
const volFah = (f: number) => interpolate(f, [0, 26, 34, 78], [1, 1, 0.4, 0.4], { extrapolateRight: "clamp" });

// ------------------------------------------------------------------ cierre: "SÍGUENOS" (pedido por Lucas) encima de su cabeza
// mientras la cámara se acerca a ella riéndose. Fuera de la cámara: no crece con el zoom.
const SIGUENOS_DESDE = ed(19.3);
const Siguenos: React.FC<{ desde: number }> = ({ desde }) => {
  const frame = useCurrentFrame();
  const t = frame - desde;
  if (t < 0) return null;
  const pop = interpolate(t, [0, 6, 10], [0.6, 1.08, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const op = interpolate(t, [0, 3], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 330 }}>
      <div
        style={{
          fontFamily: F_FUERTE,
          fontSize: 170,
          letterSpacing: 2,
          color: ACENTO,
          opacity: op,
          transform: `scale(${pop * (1 + t * 0.002)})`,
          textShadow: "0 6px 24px rgba(0,0,0,0.75), 0 2px 6px rgba(0,0,0,0.9)",
        }}
      >
        SÍGUENOS
      </div>
    </AbsoluteFill>
  );
};

export const BicepFah: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Camara encuadres={ENC}>
      <Base />
    </Camara>
    <Subtitulos palabras={PALABRAS} offset={0} maxHueco={0.6} fuente={{ family: F_RELLENO, weight: 600, tracking: 0 }} /> {/* Lucas: palabra a palabra y letra sencilla tipo "Classic" de Instagram (Inter 600), solo en este vídeo */}
    <Sfx en={0} src="whoosh-short.mp3" volumen={0.35} />
    <Siguenos desde={SIGUENOS_DESDE} />
    <Sfx en={SIGUENOS_DESDE} src="pop.mp3" volumen={0.45} />
    <Series>
      <Series.Sequence offset={ed(5.6)} durationInFrames={80} name="FAH">
        <Audio src={staticFile(`${S}/fah.wav`)} volume={volFah} />
      </Series.Sequence>
    </Series>
  </AbsoluteFill>
);

export const BicepFahComp: React.FC = () => (
  <Composition id="BicepFah" component={BicepFah} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
