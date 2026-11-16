// monkey-branching — voz en off de Lucas (su propia voz) calcando el edit de diegosicrex_De9bqPnNY8y
// (https://www.instagram.com/p/De9bqPnNY8y/): b-roll cinematográfico con cortes secos, Tarzán en las "lianas",
// gancho de texto en 2 líneas al principio y subtítulos pequeños blancos en el centro. Música: "Restless" (UntitledRockBand,
// sello GoodTalk) — la misma que la ref (Shazam en 4 tramos tras separar la voz con demucs), versión instrumental oficial
// (YouTube siCXPkX1AaI) porque la cantada mete voz desde el s 20.
// Voz: bruto/Passeig de la Marina, 27.m4a → retoma "miedo al silencio, a mirar el móvil" quitada → aislar-voz (ElevenLabs)
// → apretar_voz.py ×1,12 → public/monkey-branching/voz.mp3 (32,7 s). Tiempos por palabra: Scribe sobre voz.mp3.
// Clips: recursos/ (proxies 2160×3840 con herramientas/proxy.sh … 2160). cbarras (pasamanos, HDR exterior con sol) salía ~8 niveles
// más claro que el bruto en QuickTime → corrección medida pasamanos-pantalla.cube (capturas QuickTime en 4/13/18 s, validada en 9 y 15 s:
// 2,8–3,0 niveles) aplicada encima del proxy.
// Tarzán (recortado a 9:16, 2160×3840): t3/t4/t5 de la persecución de los babuinos en 4K (YouTube m6BHrxXrlgY, "4K IMAX Remaster",
// 119,6 / 127,0 / 129,0 s) y t1/t2/t6/t7 del "Tree Surfing Chase Scene" 1080p (YouTube L84eXSuuAH8, 148,0 / 151,3 / 147,0 / 154,8 s,
// con unsharp). La 1.ª versión salía de un vídeo de 720p y se veía mal (corrección de Lucas). Render con --scale=2 (hay brutos 4K).
// ⚠️ t1–t7 BORRADOS el 2026-11-03 al cerrar el vídeo (Lucas: lo descargado para un vídeo se borra al acabar). Para re-renderizar,
// rehazlos desde esas fuentes: recorte crop=ih*9/16:ih:x:0 + scale 2160:3840 lanczos (+ unsharp=5:5:0.6 en los 1080p).
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, Freeze, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { F_RELLENO, Sfx } from "../../comun/hablando";
import { Rotulo, RotuloHandle } from "../../comun/Rotulos";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import palabras from "./voz-palabras.json";

const S = "monkey-branching";
const FPS = 30;
const PALABRAS = palabras as Palabra[];
const FIN_VOZ = PALABRAS[PALABRAS.length - 1].end;
// Cierre sin CTA hablado → el último plano sigue 2 s más con la música y sale el rótulo "SÍGUEME PARA MÁS" (Lucas, 2026-11-02)
const EXTRA_CIERRE = 2;
const DUR = Math.round((FIN_VOZ + 0.75 + EXTRA_CIERRE) * FPS);
const CTA_EN = FIN_VOZ + 0.5; // cuando se va el último subtítulo
const f = (s: number) => Math.round(s * FPS);

// Cada plano empieza en `en` (s del edit) y dura hasta el siguiente. desde = s del clip. zoom/origen solo si hace falta encuadrar.
type Plano = { en: number; clip: string; desde: number; nota: string; zoom?: number; origen?: string; vel?: number; exposicion?: number };
// exposicion: <1 baja la exposición (CSS brightness() multiplica toda la imagen = exposición; 0,85 ≈ −0,5 pasos) del plano para que el subtítulo blanco se lea sobre fondos claros (Lucas, 2026-11-02).
// Criterio: p90 de luminancia en la franja del subtítulo ≥ 145 → 0,85; ≥ 175 → 0,80.
const PLANOS: Plano[] = [
  { en: 0, clip: "cgarrafa", desde: 0.2, nota: "GANCHO · ¿Conocéis a esa gente que lo deja… alguien nuevo? (Devant, manga larga gris)" },
  { en: 3.86, clip: "cplaya", desde: 4.0, exposicion: 0.85, nota: "Porque mientras estaban contigo (playa, run club)" },
  { en: 5.52, clip: "ccafe", desde: 5.8, exposicion: 0.8, nota: "ya estaban hablando con el siguiente (chiringuito)" },
  { en: 7.66, clip: "t1", desde: 0, nota: "Esto se llama (Tarzán)" },
  { en: 8.88, clip: "t2", desde: 0, nota: "monkey branching (Tarzán)" },
  { en: 10.04, clip: "t3", desde: 0, nota: "porque no sueltan una liana (Tarzán agarrado a la liana, 4K)" },
  { en: 11.6, clip: "t4", desde: 0, exposicion: 0.85, nota: "hasta tener la siguiente (salto con Jane contra el cielo, 4K)" },
  { en: 13.12, clip: "t5", desde: 0, exposicion: 0.8, nota: "bien agarrada (Tarzán agarrando a Jane, 4K)" },
  { en: 14.16, clip: "ccharcos", desde: 0.2, nota: "Pero en el fondo es miedo a estar solo (corriendo solo, charcos)" },
  { en: 16.98, clip: "ccajon", desde: 9.6, nota: "miedo al silencio (sentado, Nike Strength)", zoom: 1.7, origen: "50% 60%" },
  { en: 18.32, clip: "csaco", desde: 8.5, nota: "a mirar el móvil y que no haya nada (Devant, oliva, mira a un lado)" },
  { en: 20.9, clip: "t6", desde: 0, nota: "Así que cuando lo dejes (Tarzán)" },
  { en: 22.44, clip: "t7", desde: 0, nota: "no corras a otra liana (Tarzán)" },
  { en: 24.04, clip: "csuelo", desde: 5.0, nota: "Quédate en el suelo (tumbado tras el WOD)" },
  { en: 25.48, clip: "cneon", desde: 7.0, zoom: 1.1, origen: "50% 100%", nota: "Usa el silencio (Devant, curl con neón; subido para que el texto quede bajo la barbilla)" },
  { en: 26.5, clip: "cducha", desde: 1.0, nota: "para limpiarte (ducha del spa)" },
  { en: 27.6, clip: "cbarras", desde: 12.0, nota: "en vez de saltar a la siguiente persona (pasamanos, playa)" },
  { en: 29.7, clip: "cmar", desde: 7.9, vel: 0.6, exposicion: 0.85, nota: "con la misma herida, pero con distinto nombre (mar, mirando abajo, cámara lenta; 7,2–7,9 saca la lengua → desde 7,9)" },
];
const CORTES = PLANOS.slice(1).map((p) => p.en);
// El clip del mar se acaba (10 s) → el último plano se congela en su último fotograma (<Freeze>, mismo vídeo = mismo color y
// encuadre) con un zoom lento hasta el final, bajo el rótulo "SÍGUEME PARA MÁS". (Se probó estirarlo con minterpolate: deformaba la cara.)
const CONGELA_EN = 29.7 + (9.93 - 7.9) / 0.6;
const ULTIMO = PLANOS[PLANOS.length - 1].en;

// Congela al llegar a `congelaEn` (frame local del plano) y hace un zoom lento hasta el final
const CongelaFinal: React.FC<{ congelaEn: number; children: React.ReactNode }> = ({ congelaEn, children }) => {
  const frame = useCurrentFrame();
  const z = interpolate(frame, [congelaEn, congelaEn + 2.2 * FPS], [1, 1.05], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: "50% 40%" }}>
      <Freeze frame={congelaEn} active={(fr) => fr >= congelaEn}>
        {children}
      </Freeze>
    </AbsoluteFill>
  );
};

const Planos: React.FC = () => (
  <>
    {PLANOS.map((p, i) => {
      const ini = f(p.en);
      const fin = i < PLANOS.length - 1 ? f(PLANOS[i + 1].en) : DUR;
      return (
        <Sequence key={i} name={p.nota} from={ini} durationInFrames={fin - ini} premountFor={FPS}>
          <AbsoluteFill style={{ transform: `scale(${p.zoom ?? 1})`, transformOrigin: p.origen ?? "50% 50%", filter: p.exposicion ? `brightness(${p.exposicion})` : undefined }}>
            {i === PLANOS.length - 1 ? (
              <CongelaFinal congelaEn={f(CONGELA_EN) - ini}>
                <Video src={staticFile(`${S}/${p.clip}.mp4`)} trimBefore={f(p.desde)} playbackRate={p.vel ?? 1} muted style={{ width: "100%", height: "100%" }} />
              </CongelaFinal>
            ) : (
              <Video src={staticFile(`${S}/${p.clip}.mp4`)} trimBefore={f(p.desde)} playbackRate={p.vel ?? 1} muted style={{ width: "100%", height: "100%" }} />
            )}
          </AbsoluteFill>
        </Sequence>
      );
    })}
  </>
);

// Gancho: 2 líneas, letra sencilla blanca (como la ref), quieto mientras dura el primer plano
const Gancho: React.FC = () => (
  <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", paddingBottom: 60 }}>
    <div
      style={{
        fontFamily: F_RELLENO,
        fontWeight: 600,
        fontSize: 50,
        lineHeight: 1.2,
        color: "white",
        textAlign: "center",
        maxWidth: 1000,
        letterSpacing: -0.5,
        textShadow: "0 2px 10px rgba(0,0,0,0.55)",
      }}
    >
      La gente que lo deja y a la semana
      <br />
      ya está con alguien nuevo.
    </div>
  </AbsoluteFill>
);

// CTA final (Lucas, 2026-11-02): rótulo de la casa — Anton mayúsculas en el ACENTO con sombra (comun/Rotulos.tsx), centrado,
// encima de la cabeza sobre el mar (en el centro exacto taparía la cara). Entra con pop suave + pop.mp3.
// Debajo, el @lucasalvarez.x con icono de Instagram (RotuloHandle), con su propio pop HANDLE_TRAS después (Lucas, 2026-11-03).
const HANDLE_TRAS = 0.4;
const Pop: React.FC<{ desde: number; children: React.ReactNode }> = ({ desde, children }) => {
  const frame = useCurrentFrame() - desde;
  const o = interpolate(frame, [0, 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sc = interpolate(frame, [0, 8], [0.8, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return <div style={{ opacity: o, transform: `scale(${sc})` }}>{children}</div>;
};
const CtaSigueme: React.FC = () => (
  <AbsoluteFill style={{ alignItems: "center", paddingTop: 430, gap: 22 }}>
    <Pop desde={0}>
      <Rotulo texto="SÍGUEME PARA MÁS" size={112} />
    </Pop>
    <Pop desde={Math.round(HANDLE_TRAS * FPS)}>
      <RotuloHandle size={72} />
    </Pop>
  </AbsoluteFill>
);

const MonkeyBranching: React.FC = () => {
  const frame = useCurrentFrame();
  const musica = interpolate(frame, [0, DUR - 30, DUR], [0.4, 0.4, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Planos />
      <Sequence name="Gancho" durationInFrames={f(PLANOS[1].en)}>
        <Gancho />
      </Sequence>
      {/* Subtítulos desde "Porque" (durante el gancho no hay: como en la ref). Centro de la pantalla, Inter 600 blanco. */}
      <Subtitulos
        palabras={PALABRAS.filter((p) => p.start >= PLANOS[1].en - 0.05 && p.start < ULTIMO - 0.05)}
        offset={0}
        top={905}
        claves={/^$/}
        cortes={CORTES}
        maxHueco={0.6}
        fuente={{ family: F_RELLENO, weight: 600, tracking: 0 }}
      />
      {/* Último plano: la cabeza queda en el centro → subtítulos arriba, sobre el mar */}
      <Subtitulos
        palabras={PALABRAS.filter((p) => p.start >= ULTIMO - 0.05)}
        offset={0}
        top={640}
        claves={/^$/}
        fuente={{ family: F_RELLENO, weight: 600, tracking: 0 }}
      />
      <Sequence name="CTA · SÍGUEME PARA MÁS + @" from={f(CTA_EN)}>
        <CtaSigueme />
      </Sequence>
      <Sfx en={f(CTA_EN)} src="pop.mp3" volumen={0.35} />
      <Sfx en={f(CTA_EN + HANDLE_TRAS)} src="pop.mp3" volumen={0.25} />
      <Audio src={staticFile(`${S}/voz.mp3`)} />
      <Audio src={staticFile(`${S}/musica.mp3`)} volume={() => musica} />
      <Sfx en={0} src="sparkle.mp3" volumen={0.12} />
    </AbsoluteFill>
  );
};

export const MonkeyBranchingComp: React.FC = () => (
  <Composition id="MonkeyBranching" component={MonkeyBranching} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
