import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
const source = new URL('./entry.png', import.meta.url);
const destination = join(outputDir, 'entry.png');
copyFileSync(source, destination);
