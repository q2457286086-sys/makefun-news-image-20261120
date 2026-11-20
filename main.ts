// Entry point for the news-image-20261120 bounty (Node 22, stdlib only).
// The image is entry.png beside this file; the program copies it to the
// output directory the grader provides (/output, or MAKEFUN_OUTPUT_DIR
// when set) so the judge sees exactly those bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
process.stdout.write(`news-image-20261120: copied entry.png to ${join(outDir, "entry.png")}\n`);
