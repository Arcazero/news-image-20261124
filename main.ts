// main.ts — entry point for the make.fun news-image-20261124 entry.
// Copies the finished entry.png (drawn by draw.py) into the grader's
// output directory, byte for byte. Node 22, standard library only.
//
// The grader runs this as `node /bot/main.ts` with the container image's
// working directory — never the repository — so the image path must NOT be
// resolved against process.cwd(). It is resolved against this file's own
// location (import.meta.url), the same way the kit's starter does, with
// $MAKEFUN_BOT_DIR (/bot in the grader) as a fallback. A bare relative
// "entry.png" fails run_completes from the grader's cwd.
//
// Usage:
//   python3 draw.py
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// The image sits beside this file; resolve it from the module location,
// not from the working directory (the grader's cwd is not the repo).
const fromModule = fileURLToPath(new URL("entry.png", import.meta.url));
const botDir = process.env.MAKEFUN_BOT_DIR || "";
const fromBotDir = botDir ? join(botDir, "entry.png") : "";
const SRC = existsSync(fromModule)
  ? fromModule
  : fromBotDir && existsSync(fromBotDir)
    ? fromBotDir
    : null;

if (SRC === null) {
  fail("entry.png not found beside main.ts or under $MAKEFUN_BOT_DIR — run `python3 draw.py` first.");
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });

const dest = join(outDir, "entry.png");
copyFileSync(SRC, dest);

// Confirm the grader receives the exact bytes draw.py produced: compare
// the full bytes, not just the size, so a corrupted copy can never pass.
if (!readFileSync(dest).equals(readFileSync(SRC))) {
  fail(`copied file bytes differ: ${SRC} vs ${dest}`);
}
console.log(`main.ts: copied ${SRC} -> ${dest}`);
