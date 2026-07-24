/**
 * Genera iconos PWA a partir del logo SVG de Grupo Cotorreo.
 * Requiere sharp (npm install sharp).
 */
const sharp = require('C:/Users/vicente benitez2/cotorreo-rewards/tools/node_modules/sharp');
const path = require('path');
const fs = require('fs');

const ROOT = 'C:/Users/vicente benitez2/cotorreo-rewards/frontend/assets';
const SRC = path.join(ROOT, 'logo-vertical.svg');
const BG = { r: 5, g: 150, b: 105, alpha: 1 }; // emerald-600

const sizes = [
  { size: 192, name: 'icon-192.png' },
  { size: 512, name: 'icon-512.png' },
  { size: 180, name: 'apple-touch-icon.png' },
  { size: 32,  name: 'favicon-32.png' },
  { size: 16,  name: 'favicon-16.png' },
];

async function main() {
  for (const { size, name } of sizes) {
    // Renderizar SVG a un logo del tamano interior (75% del canvas)
    const innerSize = Math.floor(size * 0.72);
    const logoBuf = await sharp(SRC)
      .resize(innerSize, innerSize, { fit: 'inside' })
      .png()
      .toBuffer();

    // Metadata para saber tamano real
    const meta = await sharp(logoBuf).metadata();
    const offsetX = Math.floor((size - meta.width) / 2);
    const offsetY = Math.floor((size - meta.height) / 2);

    // Canvas cuadrado verde emerald + logo centrado
    const out = path.join(ROOT, name);
    await sharp({
      create: { width: size, height: size, channels: 4, background: BG }
    })
      .composite([{ input: logoBuf, left: offsetX, top: offsetY }])
      .png()
      .toFile(out);

    console.log(`  ${name}: ${size}x${size}`);
  }
  console.log('OK todos los iconos generados');
}

main().catch(e => { console.error(e); process.exit(1); });
