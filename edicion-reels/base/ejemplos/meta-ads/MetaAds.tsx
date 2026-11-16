// Anuncio Meta Ads (2026-11-05): rediseño web por Black Friday. Hablando a cámara con DOS ángulos del mismo momento.
// Brutos: bruto terminado/2026-11-05_meta-ads-rediseno-web_01-frente.MOV (era IMG_1163, iPhone 4K HDR) y
// …_02-lateral.MOV (era IMG_9085, iPhone 1080p HDR).
// Sincronía por audio: tiempo del lateral = frente + 7,454 s. Proxies 2160×3840 con herramientas/proxy.sh … 2160
// + encima frente-pantalla.cube / lado-pantalla.cube (curva_qt.py: capturas QuickTime bruto vs proxy; el proxy salía
// 11 y 18 niveles más claro → 1,9 y 1,6–2,5 en validación).
// En cada frase se usa la cámara a la que MIRA Lucas (giro de cabeza = corte). Cámara virtual por plano (plan.py):
// la cabeza cae en el mismo sitio de la pantalla a ambos lados de cada corte (el lateral sale más a la izquierda,
// más abajo y ~10 % más pequeño → se compensa con escala + desplazamiento) y empuje lento dentro del plano.
// Voz: solo las tomas de Lucas (speaker_0; el apuntador fuera), audio del frente, highpass 80, ganancia fija.
// Letra comercial (pedido de Lucas, SOLO para este tipo de vídeo): Host Grotesk.
import { Audio, Video } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/HostGrotesk";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Sfx } from "../../comun/hablando";
import { ACENTO, Subtitulos } from "../../comun/Subtitulos";
import plan from "./plan.json";

const S = "meta-ads";
const FPS = 30;
const DUR = plan.total;
const { fontFamily: FUENTE } = loadFont("normal", { weights: ["500", "600", "700", "800"], subsets: ["latin", "latin-ext"] });
const TINTA = "#121212";
// voz mono a −22 LUFS (pico −4 dBFS) → en el render estéreo +3 dB; MEZCLA deja margen y el volumen final (−14 LUFS) va después con ganancia fija + limitador
const VOZ_VOL = 0.7;

type Plano = (typeof plan.planos)[number];

const limpia = (w: string) => w.replace(/[¿?¡!.,:]/g, "").toLowerCase();
// fotograma en que empieza la n-ésima vez que se dice `texto`
const en = (texto: string, n = 0) => {
  const ws = plan.palabras.filter((p) => limpia(p.w) === texto);
  return Math.round(ws[n].start * FPS);
};

// ---------- cámara ----------
const PlanoCam: React.FC<{ p: Plano; i: number }> = ({ p, i }) => {
  const f = useCurrentFrame();
  const len = p.f1 - p.f0;
  // primer plano: punch-in de entrada 27 f + empuje; resto: empuje lineal
  const k = i === 0
    ? 0.75 * interpolate(f, [0, 27], [0, 1], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }) + 0.25 * (f / len)
    : f / len;
  const s = p.s0 + (p.s1 - p.s0) * k;
  const tx = p.T0[0] + (p.T1[0] - p.T0[0]) * k;
  const ty = p.T0[1] + (p.T1[1] - p.T0[1]) * k;
  const src = p.cam === "frente" ? p.desde : p.desde + plan.off;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "black" }}>
      <div
        style={{
          position: "absolute", left: 0, top: 0, width: 1080, height: 1920, transformOrigin: "0 0",
          transform: `translate(${tx - s * p.A[0]}px, ${ty - s * p.A[1]}px) scale(${s})`,
        }}
      >
        <Video src={staticFile(`${S}/${p.cam}.mp4`)} trimBefore={Math.round(src * FPS)} muted style={{ width: "100%", height: "100%" }} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- tipografía ----------
// aparece en su fotograma: fundido + sube + desenfoque (5 f)
const useEntrada = (desde: number, dur = 5) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [desde, desde + dur], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return { opacity: p, transform: `translateY(${(1 - p) * 18}px)`, filter: `blur(${(1 - p) * 8}px)` } as React.CSSProperties;
};

const Pal: React.FC<{ t: string; desde: number; size: number; peso?: number; color?: string }> = ({ t, desde, size, peso = 600, color = TINTA }) => (
  <span style={{ display: "inline-block", fontSize: size, fontWeight: peso, color, marginRight: size * 0.24, ...useEntrada(desde) }}>{t}</span>
);

// texto grande con marcador de acento que se pinta de izquierda a derecha
const Marcado: React.FC<{ t: string; desde: number; size: number; peso?: number }> = ({ t, desde, size, peso = 800 }) => {
  const f = useCurrentFrame();
  const w = interpolate(f, [desde + 2, desde + 10], [0, 100], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <span style={{ position: "relative", display: "inline-block", fontSize: size, fontWeight: peso, color: TINTA, padding: `0 ${size * 0.14}px`, ...useEntrada(desde) }}>
      <span style={{ position: "absolute", left: 0, bottom: size * 0.08, height: size * 0.62, width: `${w}%`, background: ACENTO, borderRadius: size * 0.1, zIndex: 0 }} />
      <span style={{ position: "relative", zIndex: 1 }}>{t}</span>
    </span>
  );
};

// bloque en la franja superior (encima de la cabeza; la cabeza queda en y ≈ 430–470)
const Arriba: React.FC<{ desde: number; hasta: number; children: React.ReactNode; top?: number }> = ({ desde, hasta, children, top = 232 }) => {
  const f = useCurrentFrame();
  if (f < desde || f >= hasta) return null;
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top, fontFamily: FUENTE, letterSpacing: "-0.035em", lineHeight: 1 }}>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 6, textAlign: "center", maxWidth: 980 }}>{children}</div>
    </AbsoluteFill>
  );
};
const Linea: React.FC<{ children: React.ReactNode }> = ({ children }) => <div style={{ display: "flex", alignItems: "baseline", justifyContent: "center", flexWrap: "nowrap" }}>{children}</div>;

const Pop: React.FC<{ desde: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ desde, children, style }) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [desde, desde + 7], [0.6, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const o = interpolate(f, [desde, desde + 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <div style={{ transform: `scale(${s})`, opacity: o, ...style }}>{children}</div>;
};

const Etiqueta: React.FC<{ desde: number; children: React.ReactNode }> = ({ desde, children }) => (
  <Pop desde={desde}>
    <div style={{ display: "flex", alignItems: "center", gap: 14, background: TINTA, color: "white", borderRadius: 999, padding: "12px 28px 12px 22px", fontSize: 40, fontWeight: 800, letterSpacing: "0.04em" }}>
      <span style={{ width: 16, height: 16, borderRadius: 99, background: ACENTO }} />
      {children}
    </div>
  </Pop>
);

const Check: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <circle cx="24" cy="24" r="24" fill={ACENTO} />
    <path d="M14 24.5l6.5 6.5L34 17.5" stroke={TINTA} strokeWidth="5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const LogoGoogle: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
    <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
    <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
    <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
  </svg>
);
// logo de OpenAI (simple-icons 13.21.0)
const LogoOpenAI: React.FC<{ size: number }> = ({ size }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <path fill={TINTA} d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z" />
  </svg>
);

const TarjetaLogo: React.FC<{ desde: number; logo: React.ReactNode; nombre: string }> = ({ desde, logo, nombre }) => (
  <Pop desde={desde}>
    <div style={{ display: "flex", alignItems: "center", gap: 16, background: "white", borderRadius: 26, padding: "16px 30px 16px 20px", boxShadow: "0 10px 30px rgba(0,0,0,0.14)", fontSize: 52, fontWeight: 700, color: TINTA }}>
      {logo}
      {nombre}
    </div>
  </Pop>
);

// formulario: escribe "tuweb.com" y pulsa Enviar
const Formulario: React.FC<{ desde: number; escribe: number; pulsa: number }> = ({ desde, escribe, pulsa }) => {
  const f = useCurrentFrame();
  const URL = "www.tuweb.com";
  const n = Math.round(interpolate(f, [escribe, escribe + 16], [0, URL.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const cursor = Math.floor(f / 8) % 2 === 0 || (f >= escribe && f < escribe + 16);
  const press = interpolate(f, [pulsa, pulsa + 3, pulsa + 9], [1, 0.9, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ok = f >= pulsa + 3;
  return (
    <Pop desde={desde}>
      <div style={{ display: "flex", alignItems: "center", gap: 14, background: "white", borderRadius: 30, padding: 14, boxShadow: "0 12px 34px rgba(0,0,0,0.16)" }}>
        <div style={{ width: 520, height: 92, borderRadius: 20, background: "#F2F2F0", display: "flex", alignItems: "center", padding: "0 26px", fontSize: 42, fontWeight: 500, color: n ? TINTA : "#9A9A9A", letterSpacing: "-0.02em" }}>
          {n ? URL.slice(0, n) : "Tu web"}
          {cursor ? <span style={{ width: 3, height: 46, background: TINTA, marginLeft: 3 }} /> : null}
        </div>
        <div style={{ height: 92, borderRadius: 20, background: ACENTO, display: "flex", alignItems: "center", gap: 10, padding: "0 30px", fontSize: 42, fontWeight: 800, color: TINTA, transform: `scale(${press})` }}>
          {ok ? "Enviado" : "Enviar"}
          {ok ? <Check size={40} /> : <span style={{ fontSize: 44 }}>→</span>}
        </div>
      </div>
    </Pop>
  );
};

const Graficos: React.FC = () => {
  const B = (n: number) => plan.planos[n].f0; // inicio del plano n
  return (
    <>
      {/* 1 · ¿Tu web es muy antigua? */}
      <Arriba desde={0} hasta={B(1)}>
        <Linea><Pal t="¿Tu" desde={en("tu", 0)} size={74} /><Pal t="web" desde={en("web", 0)} size={74} /><Pal t="es" desde={en("es")} size={74} /></Linea>
        <Linea><Pal t="muy" desde={en("muy")} size={120} peso={800} /><Marcado t="antigua?" desde={en("antigua")} size={120} /></Linea>
      </Arriba>
      {/* 2 · ¿Llevas tiempo pensando en cambiarla? */}
      <Arriba desde={B(1)} hasta={B(2)}>
        <Linea><Pal t="¿Llevas" desde={en("llevas")} size={66} /><Pal t="tiempo" desde={en("tiempo")} size={66} /><Pal t="pensando" desde={en("pensando")} size={66} /><Pal t="en" desde={en("en", 0)} size={66} /></Linea>
        <Linea><Marcado t="cambiarla?" desde={en("cambiarla")} size={120} /></Linea>
      </Arriba>
      {/* 3 · BLACK FRIDAY · rediseño · menos de 600 € · solo pagas si te gusta */}
      <Arriba desde={en("black")} hasta={B(6)} top={226}>
        <Etiqueta desde={en("black")}>BLACK FRIDAY</Etiqueta>
      </Arriba>
      <Arriba desde={en("rediseñamos")} hasta={B(4)} top={310}>
        <Linea><Pal t="Rediseño" desde={en("rediseñamos")} size={100} peso={800} /><Pal t="web" desde={en("rediseñamos") + 3} size={100} peso={800} /></Linea>
      </Arriba>
      <Arriba desde={B(4)} hasta={B(5)} top={300}>
        <Linea><Pal t="por menos de" desde={B(4)} size={62} /><Marcado t="600 €" desde={en("seiscientos")} size={124} /></Linea>
      </Arriba>
      <Arriba desde={B(5)} hasta={B(6)} top={310}>
        <Pop desde={en("solo", 0)} style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <Check size={84} />
          <span style={{ fontSize: 76, fontWeight: 800, color: TINTA }}>Solo pagas si te gusta</span>
        </Pop>
      </Arriba>
      {/* 4 · Un buen diseño no trae clientes por sí solo */}
      <Arriba desde={B(6)} hasta={B(7)}>
        <Linea><Pal t="Un" desde={en("un")} size={64} /><Pal t="buen" desde={en("buen")} size={64} /><Pal t="diseño" desde={en("diseño")} size={64} /><Pal t="no" desde={en("no", 1)} size={64} /><Pal t="trae" desde={en("trae")} size={64} /><Pal t="clientes" desde={en("clientes", 0)} size={64} /></Linea>
        <Linea><Marcado t="por sí solo" desde={en("por", 1)} size={120} /></Linea>
      </Arriba>
      {/* 5 · Te posicionamos en Google y ChatGPT */}
      <Arriba desde={en("posicionamos")} hasta={B(9)} top={226}>
        <Linea><Pal t="Te posicionamos en" desde={en("posicionamos")} size={60} /></Linea>
        <div style={{ display: "flex", gap: 22, marginTop: 14 }}>
          <TarjetaLogo desde={en("google")} logo={<LogoGoogle size={58} />} nombre="Google" />
          <TarjetaLogo desde={en("chatgpt")} logo={<LogoOpenAI size={58} />} nombre="ChatGPT" />
        </div>
      </Arriba>
      {/* 6 · los clientes que hoy se van a tu competencia → te encuentren a ti */}
      <Arriba desde={B(9)} hasta={B(10)}>
        <Linea><Pal t="Los" desde={en("los")} size={64} /><Pal t="clientes" desde={en("clientes", 1)} size={64} /><Pal t="que" desde={en("que", 1)} size={64} /><Pal t="hoy" desde={en("hoy")} size={64} /><Pal t="se" desde={en("se")} size={64} /><Pal t="van" desde={en("van")} size={64} /><Pal t="a" desde={en("a", 0)} size={64} /></Linea>
        <Linea><Pal t="tu competencia" desde={en("competencia")} size={120} peso={800} /></Linea>
      </Arriba>
      <Arriba desde={B(10)} hasta={B(11)}>
        <Linea><Pal t="te" desde={en("te", 2)} size={66} /><Pal t="encuentren" desde={en("encuentren")} size={66} /></Linea>
        <Linea><Marcado t="a ti" desde={en("a", 1)} size={112} /></Linea>
      </Arriba>
      {/* 7 · Solo hasta el 1 de diciembre */}
      <Arriba desde={B(11)} hasta={B(12)}>
        <Linea><Pal t="Solo" desde={en("solo", 2)} size={66} /><Pal t="hasta" desde={en("hasta")} size={66} /><Pal t="el" desde={en("el", 0)} size={66} /></Linea>
        <Linea><Pal t="1" desde={en("1")} size={120} peso={800} /><Pal t="de" desde={en("de", 1)} size={120} peso={800} /><Marcado t="diciembre" desde={en("diciembre")} size={120} /></Linea>
      </Arriba>
      {/* 8 · Déjanos tu web en el formulario */}
      <Arriba desde={B(12)} hasta={DUR} top={226}>
        <Linea><Pal t="Déjanos tu web aquí" desde={B(12) + 2} size={60} /></Linea>
        <div style={{ marginTop: 14 }}>
          <Formulario desde={B(12) + 4} escribe={en("web", 1)} pulsa={en("formulario") + 14} />
        </div>
      </Arriba>
    </>
  );
};

const CLAVES = /^(antigua|cambiarla|black|friday|seiscientos|euros|gusta|google|chatgpt|competencia|ti|diciembre|formulario)$/i;

export const MetaAds: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {plan.planos.map((p, i) => (
        <Sequence key={i} from={p.f0} durationInFrames={p.f1 - p.f0} name={`${i + 1} ${p.cam} ${p.desde}`}>
          <PlanoCam p={p} i={i} />
        </Sequence>
      ))}
      <Graficos />
      <Subtitulos palabras={plan.palabras} offset={0} claves={CLAVES} top={1180} fuente={{ family: FUENTE, weight: 800, tracking: -1 }} />
      <Audio src={staticFile(`${S}/voz.wav`)} volume={VOZ_VOL} />
      <Sfx en={0} src="whoosh.mp3" volumen={0.45} />
      <Sfx en={en("tu", 0)} src="sparkle.mp3" volumen={0.22} />
      <Sfx en={en("seiscientos")} src="pop.mp3" volumen={0.3} />
      <Sfx en={en("google")} src="pop.mp3" volumen={0.3} />
      <Sfx en={en("chatgpt")} src="pop.mp3" volumen={0.3} />
      <Sfx en={en("web", 1)} src="typing.mp3" volumen={0.18} />
      <Sfx en={en("formulario") + 14} src="click-soft.mp3" volumen={0.4} />
    </AbsoluteFill>
  );
};

export const MetaAdsComp: React.FC = () => (
  <Composition id="MetaAds" component={MetaAds} durationInFrames={DUR} fps={FPS} width={1080} height={1920} />
);
