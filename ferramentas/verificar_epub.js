// Verifica se algum elemento passa da largura de uma tela de e-reader (380px).
// Uso: node ferramentas/verificar_epub.js <pasta-do-epub-descompactado>
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
(async () => {
  const raiz = process.argv[2];
  const dir = fs.existsSync(path.join(raiz, 'EPUB', 'text')) ? path.join(raiz, 'EPUB', 'text') : raiz;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 380, height: 700 } });
  let total = 0;
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.xhtml')).sort()) {
    await p.goto('file://' + path.join(dir, f));
    await p.waitForTimeout(50);
    const r = await p.evaluate(() => {
      const W = document.documentElement.clientWidth;
      return [...document.querySelectorAll('pre, code, table, img, p, li, blockquote, details')]
        .filter(e => e.getBoundingClientRect().right > W + 2)
        .map(e => e.tagName + ': ' + (e.textContent || e.getAttribute('src') || '').trim().slice(0, 60));
    });
    if (r.length) { total += r.length; console.log(f); r.slice(0, 5).forEach(x => console.log('   ' + x)); }
  }
  console.log(total === 0 ? 'OK: nada passa da largura da tela.' : `${total} elemento(s) passam da largura.`);
  await b.close();
  process.exit(total === 0 ? 0 : 1);
})();
