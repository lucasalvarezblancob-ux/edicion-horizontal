// Rótulos SIN pastilla (2026-11-01): texto como el "BLACK FRIDAY" del gancho —
// línea pequeña en crema (Inter 600) + texto grande en Anton mayúsculas en el ACENTO, con sombra.
// Sustituyen a las pastillas de color (código de descuento y @ de Instagram). Ver preferencias.md → Estilo.
import React from "react";
import { ACENTO, CODIGO, CREMA, F_FUERTE, F_RELLENO, HANDLE } from "./marca";

export const SOMBRA_ROTULO = "0 4px 22px rgba(0,0,0,0.55), 0 2px 4px rgba(0,0,0,0.5)";

export const IconoInstagram: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2.3}>
    <rect x={2.5} y={2.5} width={19} height={19} rx={5.5} />
    <circle cx={12} cy={12} r={4.3} />
    <circle cx={17.4} cy={6.6} r={1} fill={color} stroke="none" />
  </svg>
);

// Línea pequeña opcional encima + texto grande en acento.
export const Rotulo: React.FC<{ arriba?: string; texto: string; size?: number; icono?: boolean }> = ({ arriba, texto, size = 150, icono = false }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
    {arriba ? (
      <div style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: size * 0.41, color: CREMA, letterSpacing: -1, lineHeight: 1.05, textShadow: SOMBRA_ROTULO }}>
        {arriba}
      </div>
    ) : null}
    <div style={{ display: "flex", alignItems: "center", gap: size * 0.19 }}>
      {icono ? (
        <div style={{ display: "flex", filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.6))" }}>
          <IconoInstagram size={size * 0.92} color={ACENTO} />
        </div>
      ) : null}
      <div style={{ fontFamily: F_FUERTE, fontSize: size, color: ACENTO, textTransform: "uppercase", lineHeight: 0.95, whiteSpace: "nowrap", textShadow: SOMBRA_ROTULO }}>
        {texto}
      </div>
    </div>
  </div>
);

export const RotuloCodigo: React.FC<{ size?: number }> = ({ size = 150 }) => <Rotulo arriba="código de descuento" texto={CODIGO} size={size} />;

export const RotuloHandle: React.FC<{ size?: number }> = ({ size = 104 }) => <Rotulo texto={HANDLE} size={size} icono />;
