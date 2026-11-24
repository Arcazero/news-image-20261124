// main.ts — deliver entry.png to the grader's output directory.
//
// The finished image is drawn by draw.py and committed beside this file.
// This program only moves those exact bytes into $MAKEFUN_OUTPUT_DIR
// (or /output), then proves the copy is byte-identical before exiting.
//
// Why the path is built this way: the grader starts the program as
// `node /bot/main.ts` from the container image's working directory, which
// is never the repository, so a plain relative "entry.png" would resolve
// against the wrong directory and the run would fail. The image is
// therefore located from this module's own URL, with $MAKEFUN_BOT_DIR
// (/bot in the grader) as a second place to look.
//
// Node 22, standard library only. Run it with:
//   python3 draw.py
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const IMAGE_NAME = "entry.png";

function die(reason: string): never {
  console.error(`main.ts: ${reason}`);
  process.exit(1);
}

function locateImage(): string {
  const here = dirname(fileURLToPath(import.meta.url));
  const nextToModule = join(here, IMAGE_NAME);
  if (existsSync(nextToModule)) return nextToModule;
  const botDir = process.env.MAKEFUN_BOT_DIR;
  if (botDir) {
    const underBotDir = join(botDir, IMAGE_NAME);
    if (existsSync(underBotDir)) return underBotDir;
  }
  die(
    `${IMAGE_NAME} not found beside main.ts or under $MAKEFUN_BOT_DIR ` +
      `— run \`python3 draw.py\` first.`,
  );
}

function deliver(): void {
  const source = locateImage();
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outputDir, { recursive: true });
  const destination = join(outputDir, IMAGE_NAME);
  const bytes = readFileSync(source);
  writeFileSync(destination, bytes);
  const delivered = readFileSync(destination);
  if (!delivered.equals(bytes)) {
    die(`copied bytes differ: ${source} vs ${destination}`);
  }
  console.log(
    `main.ts: delivered ${bytes.length} bytes ${source} -> ${destination}`,
  );
}

deliver();
