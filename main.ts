import { copyFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

const sourceImage = new URL("./entry.png", import.meta.url);
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || "/output";

await mkdir(outputDirectory, { recursive: true });
await copyFile(sourceImage, join(outputDirectory, "entry.png"));
