// Renders each .dc.html artboard to a 1080x1920 PNG, and reports any slide
// whose content is taller than the frame (which would clip on export).
import { chromium } from 'playwright-core';
import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { basename } from 'path';

const ORDER = ['Main', 'Minneapolis', 'Ice', 'WestBank', 'Turn', 'Idea', 'Proof', 'Means', 'NoServer', 'Cta'];
const images = {};
for (const f of readdirSync('.').filter((f) => /\.(png|jpg)$/.test(f) && !f.startsWith('slide-'))) {
  const mime = f.endsWith('.jpg') ? 'image/jpeg' : 'image/png';
  images[f] = `data:${mime};base64,` + readFileSync(f).toString('base64');
}

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });

let n = 0;
for (const stem of ORDER) {
  n += 1;
  let src = readFileSync(`${stem}.dc.html`, 'utf8');
  const style = (src.match(/<helmet>\s*<style>([\s\S]*?)<\/style>/) || [, ''])[1];
  const body = src.slice(src.indexOf('</helmet>') + 9, src.indexOf('</x-dc>'));
  let html = `<!doctype html><meta charset="utf-8"><style>${style}</style>${body}`;
  for (const [name, uri] of Object.entries(images)) html = html.split(`"${name}"`).join(`"${uri}"`);

  await page.setContent(html, { waitUntil: 'load' });
  const frame = page.locator('body > div').first();
  const fit = await frame.evaluate((el) => {
    const h = el.style.height, o = el.style.overflow;
    el.style.height = 'auto'; el.style.overflow = 'visible';
    const natural = el.getBoundingClientRect().height;
    el.style.height = h; el.style.overflow = o;
    return { scroll: Math.round(natural), client: 1920 };
  });
  const out = `slide-${String(n).padStart(2, '0')}-${stem.toLowerCase()}.png`;
  await frame.screenshot({ path: out });
  const flag = fit.scroll > fit.client ? `  *** OVERFLOWS by ${fit.scroll - fit.client}px ***` : '';
  console.log(`${out}  content ${fit.scroll}px / frame ${fit.client}px${flag}`);
}
await browser.close();
