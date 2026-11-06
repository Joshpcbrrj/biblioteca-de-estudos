// renderiza cada svg em 380px de largura (como no e-reader) numa folha
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const dir=process.env.SVG_OUT||'out';const files=process.argv.slice(2);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
const html='<body style="margin:0;display:flex;flex-wrap:wrap;gap:10px;background:#999;align-items:flex-start">'+files.map(f=>`<div style="background:#fff;width:380px"><div style="font:10px sans-serif">${f}</div><img src="file://${require('path').resolve(dir)}/${f}" style="width:380px"></div>`).join('')+'</body>';
const hp=require('path').resolve('prev.html');fs.writeFileSync(hp,html);await p.goto('file://'+hp);await p.waitForTimeout(300);await p.screenshot({path:'prev.png',fullPage:true});await b.close()})()
