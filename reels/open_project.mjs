// Point the flow-mcp Chrome window back at a Flow project. Usage: node open_project.mjs <project-url>
import { createRequire } from "node:module";
const require = createRequire("C:/Users/Anojan/flow-mcp/package.json");
const { chromium } = require("playwright-core");
const browser = await chromium.connectOverCDP("http://127.0.0.1:9333");
const page = browser.contexts()[0].pages().find((p) => p.url().includes("flow.google")) ?? browser.contexts()[0].pages()[0];
await page.goto(process.argv[2] + "?hl=en", { waitUntil: "domcontentloaded" });
await page.waitForTimeout(4000);
console.log(page.url());
process.exit(0);
