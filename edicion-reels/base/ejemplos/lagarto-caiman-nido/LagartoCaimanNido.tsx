// "Casi nadie ha visto un nido de esta especie" — lagarto caimán (Dracaena guianensis). @reinoselva hablando a cámara en un terrario.
// Bruto: bruto terminado/2026-11-11_lagarto-caiman-nido_01-terrario-a-camara.MOV (antes bruto/IMG_2662.MOV) (4K HDR 60 fps, 2:23) → public/lagarto-caiman-nido/proxy.mp4 (2160×3840, 30 fps)
//   ⚠️ Proxy hecho en Windows: sin avconvert → herramientas/proxy.sh usa libplacebo (color validado en mpv: +2,5 niveles). NO zscale+mobius (+20).
// ⚠️ Bruto con APUNTADOR: otra persona dicta cada frase en voz baja (≈ −34 dB) y él la repite (≈ −22 dB).
//   Sin Scribe (clave de ElevenLabs inválida) → Whisper large-v3 local por tramos fuertes + herramientas/cortar_tomas_energia.py (revisado con revisar_cortes.py).
//   tomas.json = la toma buena de cada frase; montaje.json = tramos + palabras recolocadas. Ninguna palabra del apuntador entra.
//   voz.wav = tramos concatenados (fundido 15 ms) + highpass 80 Hz, sin compresión; la ganancia final va sobre el mp4.
// Estilo por defecto hablando a cámara: gancho tipográfico arriba + bloques palabra a palabra + zooms a los remates.
// Foto: "Gfp-northern-caiman-lizard.jpg" (Wikimedia Commons, dominio público), recortada con rembg.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, Sequence, Series, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Bloque, CamaraVirtual, Encuadre, F_REMATE, Sfx, TextoBloques } from "../../comun/hablando";
import { RotuloHandle } from "../../comun/Rotulos";
import cara from "./cara.json";
import montaje from "./montaje.json";
import tiempos from "./tiempos.json";

const SRC = staticFile("lagarto-caiman-nido/proxy.mp4");
const VOZ = staticFile("lagarto-caiman-nido/voz.wav");
const CARAS = cara.caras as number[][];

// Tramos del bruto (frames a 30 fps) en orden de montaje
const TRAMOS = montaje.tramos.map((t) => ({ desde: Math.round(t.desde * 30), dur: Math.round(t.hasta * 30) - Math.round(t.desde * 30), nota: t.nota }));
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0);
const INICIOS = TRAMOS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 0 : acc[i - 1] + TRAMOS[i - 1].dur], []);
// Centro de cara FIJO por tramo (mediana): el detector mete temblor.
const med = (xs: number[]) => [...xs].sort((a, b) => a - b)[Math.floor(xs.length / 2)];
const C = TRAMOS.map((t) => {
  const r = CARAS.slice(t.desde, t.desde + t.dur);
  return { cx: med(r.map((c) => c[0])), cy: med(r.map((c) => c[1])) };
});

const Base: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      {TRAMOS.map((t, i) => (
        <Series.Sequence key={i} name={`${i + 1} ${t.nota.slice(0, 36)}`} durationInFrames={t.dur} premountFor={fps}>
          <Video src={SRC} trimBefore={t.desde} muted style={{ width: "100%", height: "100%" }} />
        </Series.Sequence>
      ))}
    </Series>
  );
};

// Doble flash de sección: 4 f blanco · 1 f imagen · 3 f blanco
const DobleFlash: React.FC<{ en: number }> = ({ en }) => {
  const d = useCurrentFrame() - en;
  return (d >= 0 && d < 4) || (d >= 5 && d < 8) ? <AbsoluteFill style={{ backgroundColor: "white" }} /> : null;
};

// Foto pequeña recortada junto a la cabeza: pop en la palabra, etiqueta debajo, se va al cambiar de tema.
const Foto: React.FC<{ src: string; entra: number; sale: number; cx: number; cy: number; ancho: number; giro: number; etiqueta?: { texto: string; desde: number } }> = ({ src, entra, sale, cx, cy, ancho, giro, etiqueta }) => {
  const frame = useCurrentFrame();
  if (frame < entra - 1 || frame > sale + 6) return null;
  const e = interpolate(frame, [entra - 1, entra + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const k = e * s;
  const flota = Math.sin((frame - entra) / 9) * 6;
  return (
    <div style={{ position: "absolute", left: cx, top: cy + flota, width: ancho, transform: `translate(-50%, -50%) scale(${k}) rotate(${giro + (1 - e) * -10}deg)`, opacity: Math.min(1, k * 1.6) }}>
      <Img src={staticFile(src)} style={{ width: "100%", filter: "drop-shadow(0 0 3px rgba(0,0,0,0.9)) drop-shadow(0 16px 26px rgba(0,0,0,0.7))" }} />
      {etiqueta && frame >= etiqueta.desde ? (
        <div
          style={{
            position: "absolute", left: "50%", top: "100%", whiteSpace: "nowrap", fontFamily: F_REMATE, fontStyle: "italic", fontSize: 58, color: "white",
            lineHeight: 1, textShadow: "0 4px 22px rgba(0,0,0,0.8), 0 2px 4px rgba(0,0,0,0.7)",
            transform: `translate(-50%, 4px) rotate(${-giro}deg) scale(${interpolate(frame - etiqueta.desde, [0, 3], [0.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) })})`,
          }}
        >
          {etiqueta.texto}
        </div>
      ) : null}
    </div>
  );
};

const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });

// ------------------------------------------------------------------ gancho (texto): dice de qué animal habla desde el frame 0
// El bruto dice "un nido de esta especie" sin nombrarla → el título da el contexto. Encima de la cabeza, sobre el techo oscurecido.
const FIN_GANCHO = INICIOS[1]; // 108
const GANCHO: Bloque[] = [{ desde: 0, hasta: FIN_GANCHO, y: 0.165, palabras: [P("el nido del", 0), P("LAGARTO CAIMÁN", 8, "fuerte", true)] }];

// ------------------------------------------------------------------ lo que dice, palabra a palabra, sobre las piernas (banda oscura suave detrás)
// tiempos.json lo genera bloques.py desde palabras-alineadas.json (alineación forzada MMS_FA sobre voz.wav, ~20 ms):
// cada palabra entra en el frame exacto en que se dice. Whisper solo adelantaba los textos 0,17 s de media (hasta 0,8 s).
const BLOQUES = tiempos.bloques as Bloque[];
const M = tiempos.momentos;

// ------------------------------------------------------------------ cámara (trípode): entrada, empuje lento, reset seco en cada jump cut, zooms a los remates
const ARRIBA = (c: { cx: number; cy: number }) => ({ cx: c.cx, cy: c.cy - 300 }); // gancho: la cabeza baja para dejar sitio al título
const REMATE_1 = M.nace;
const REMATE_2 = M.misterio;
const ENC: Encuadre[] = [
  { desde: 0, escala: 1.0, ...ARRIBA(C[0]) },
  { desde: 2, escala: 1.2, suave: 27, empuje: 0.012, ...ARRIBA(C[0]) }, // zoom de entrada 1,00→1,20 en 27 f + whoosh
  { desde: INICIOS[1], escala: 1.1, empuje: 0.03, ...C[1] }, // jump cut → reset
  { desde: M.termitero - 6, escala: 1.24, suave: 10, empuje: 0.01, ...C[1] }, // golpe corto que aterriza en "TERMITERO"
  { desde: INICIOS[2], escala: 1.08, empuje: 0.03, ...C[2] },
  { desde: INICIOS[3], escala: 1.12, empuje: 0.03, ...C[3] },
  { desde: INICIOS[4], escala: 1.08, empuje: 0.02, ...C[4] },
  { desde: REMATE_1 - 24, escala: 1.38, suave: 24, empuje: 0.006, ...C[4] }, // zoom largo que aterriza en "nace"
  { desde: INICIOS[6], escala: 1.08, empuje: 0.03, ...C[6] }, // doble flash: de pie, otro plano
  { desde: INICIOS[7], escala: 1.14, empuje: 0.03, ...C[7] },
  { desde: INICIOS[8], escala: 1.08, empuje: 0.03, ...C[8] },
  { desde: M.poquisimos - 6, escala: 1.24, suave: 10, empuje: 0.01, ...C[8] }, // golpe corto que aterriza en "POQUÍSIMOS"
  { desde: INICIOS[9], escala: 1.12, empuje: 0.03, ...C[9] },
  { desde: INICIOS[10], escala: 1.08, empuje: 0.03, ...C[10] },
  { desde: INICIOS[11], escala: 1.14, empuje: 0.02, ...C[11] },
  { desde: INICIOS[12], escala: 1.08, empuje: 0.01, ...C[12] },
  { desde: REMATE_2 - 22, escala: 1.34, suave: 22, empuje: 0.006, ...C[12] }, // zoom largo que aterriza en "misterio"
  { desde: INICIOS[13], escala: 1.12, empuje: 0.03, ...C[13] },
  { desde: INICIOS[14], escala: 1.0, ...C[14] }, // CTA
  { desde: INICIOS[14] + 1, escala: 1.2, suave: 27, empuje: 0.005, ...C[14] }, // punch-in del CTA
];

// SFX: la voz va a ≈ −22 LUFS en el render y la ganancia final (+8 dB) se aplica sobre el mp4 → SFX escalados igual.
const K = 0.4;

export const LagartoCaimanNido: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <CamaraVirtual encuadres={ENC} shake={[{ desde: REMATE_1, hasta: REMATE_1 + 11, px: 8 }]}>
      <Base />
    </CamaraVirtual>
    {/* Techo blanco oscurecido arriba solo durante el gancho (se desvanece antes de la cabeza) */}
    <Sequence durationInFrames={FIN_GANCHO} layout="none" name="Gancho">
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.62) 0%, rgba(0,0,0,0.45) 16%, rgba(0,0,0,0) 26%)" }} />
      <TextoBloques bloques={GANCHO} pop escala={0.78} interlinea={22} />
    </Sequence>
    {/* Banda oscura suave detrás del texto: camisa y pantalón beige → el crema no se leía */}
    <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 48%, rgba(0,0,0,0.42) 60%, rgba(0,0,0,0.42) 74%, rgba(0,0,0,0) 84%)" }} />
    <Foto src="lagarto-caiman-nido/lagarto.png" entra={M.especie} sale={INICIOS[2]} cx={240} cy={560} ancho={400} giro={-5} etiqueta={{ texto: "Dracaena guianensis", desde: M.especie + 8 }} />
    <TextoBloques bloques={BLOQUES} pop escala={0.88} interlinea={10} />
    <Sequence from={M.sigueme} layout="none" name="Sígueme → @">
      <AbsoluteFill style={{ justifyContent: "flex-start", alignItems: "center", paddingTop: 1330, scale: interpolate(useCurrentFrame() - M.sigueme, [0, 4], [0.6, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) }) }}>
        <RotuloHandle />
      </AbsoluteFill>
    </Sequence>
    <DobleFlash en={INICIOS[6] - 3} />
    <Audio src={VOZ} />
    {/* Sonido con moderación: entrada, título, foto, remate 1, cambio de plano, remate 2, @ */}
    <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25 * K} />
    <Sfx en={1} src="whoosh.mp3" volumen={0.45 * K} />
    <Sfx en={8} src="sparkle.mp3" volumen={0.22 * K} />
    <Sfx en={M.especie} src="pop.mp3" volumen={0.5 * K} />
    <Sfx en={REMATE_1 - 1} src="impact-bass-1.mp3" volumen={0.5 * K} />
    <Sfx en={INICIOS[6] - 5} src="whoosh.mp3" volumen={0.4 * K} />
    <Sfx en={INICIOS[6] - 3} src="impact-bass-2.mp3" volumen={0.3 * K} />
    <Sfx en={REMATE_2 - 1} src="impact-bass-1.mp3" volumen={0.35 * K} />
    <Sfx en={M.sigueme} src="pop.mp3" volumen={0.45 * K} />
  </AbsoluteFill>
);

export const LagartoCaimanNidoComp = () => (
  <Composition id="LagartoCaimanNido" component={LagartoCaimanNido} durationInFrames={DUR} fps={30} width={1080} height={1920} />
);
