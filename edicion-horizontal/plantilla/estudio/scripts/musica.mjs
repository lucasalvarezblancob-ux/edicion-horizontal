// Genera una canción instrumental con ElevenLabs Music.
// Para fondos de vídeo cuando Lucas pide música y no hay canción suya (luego: herramientas/slowed-reverb.sh).
//
// Uso (desde estudio/):
//   node --env-file=.env.local scripts/musica.mjs "prompt en inglés" salida.mp3 [duración_s=30]
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import fs from "node:fs";
import { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";

const [prompt, salida, dur] = process.argv.slice(2);
if (!prompt || !salida) throw new Error('Uso: scripts/musica.mjs "prompt" salida.mp3 [duración_s]');

const client = new ElevenLabsClient();
const stream = await client.music.compose({
  prompt,
  musicLengthMs: Math.round((dur ? Number(dur) : 30) * 1000),
  forceInstrumental: true,
});
await pipeline(Readable.fromWeb(stream), fs.createWriteStream(salida));
console.log(`ok: ${salida}`);
