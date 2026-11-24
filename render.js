// Usage: node render.js [preview t1,t2,...]  |  node render.js  (full render to frames via ffmpeg pipe)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const FPS = 30, DUR = 30;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, 'video.html'));
  await page.evaluate(async () => {
    const f = ['500','600','700','800','900'].map(w => document.fonts.load(w + ' 40px P'));
    f.push(document.fonts.load('italic 800 40px P'), document.fonts.load('italic 900 40px P'));
    await Promise.all(f); await window.ready;
  });
  if (process.argv[2] === 'preview') {
    for (const t of process.argv[3].split(',')) {
      await page.evaluate(t => window.seek(t), +t);
      await page.screenshot({ path: `${process.argv[4]}/p_${t}.png` });
    }
  } else {
    const out = process.argv[2] || 'out/silent.mp4';
    const ff = spawn('ffmpeg', ['-y','-f','image2pipe','-framerate',String(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium',out], { stdio: ['pipe','ignore','inherit'] });
    for (let i = 0; i < FPS * DUR; i++) {
      await page.evaluate(t => window.seek(t), i / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 150 === 0) console.log('frame', i);
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
