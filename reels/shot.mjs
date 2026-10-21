// Screenshot the flow-mcp Chrome window. Usage: node shot.mjs <out.png>
import { createRequire } from "node:module";
const require = createRequire("C:/Users/Anojan/flow-mcp/package.json");
const { chromium } = require("playwright-core");
const browser = await chromium.connectOverCDP("http://127.0.0.1:9333");
const pages = browser.contexts()[0].pages();
for (const p of pages) console.log(p.url());
const page = pages.find((p) => p.url().includes("flow.google")) ?? pages[0];
await page.screenshot({ path: process.argv[2] });
process.exit(0);
