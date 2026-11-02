// Renders the app icons into /icons with Playwright:  node src/tools/make_icons.js
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, '..', '..', 'icons') + path.sep;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'icon.html')); await p.evaluate(() => document.fonts.ready);
  const jobs = [['icon-512.png', 512, .12, .66], ['icon-192.png', 192, .12, .66], ['icon-maskable-512.png', 512, .2, .5],
    ['icon-maskable-192.png', 192, .2, .5], ['apple-touch-icon.png', 180, .12, .66], ['favicon-32.png', 32, .1, .74]];
  for (const [name, s, inset, fs] of jobs) {
    await p.setViewportSize({ width: s, height: s });
    await p.evaluate(([s, inset, fs]) => { const e = document.getElementById('ic'); e.style.setProperty('--s', s + 'px'); e.style.setProperty('--in', (s * inset) + 'px'); e.style.setProperty('--fs', (s * fs) + 'px'); }, [s, inset, fs]);
    await p.waitForTimeout(50);
    await p.locator('#ic').screenshot({ path: OUT + name });
  }
  await b.close();
})();
