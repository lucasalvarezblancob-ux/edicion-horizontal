// Config para renderizar SOLO capas gráficas con transparencia (ProRes 4444), que luego ffmpeg superpone al montaje.
// Uso: npx remotion render <Comp> salida.mov --config=remotion.capas.config.ts --frames=A-B
import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva444p10le");
Config.setCodec("prores");
Config.setProResProfile("4444");
Config.setOverwriteOutput(true);
