#!/usr/bin/env python3
"""Gera o EPUB de um curso localmente, com os mesmos passos da Action
(.github/workflows/gerar-epubs.yml), e roda a checagem de e-reader.

Uso:  python3 -I ferramentas/gerar_epub_local.py programacao/<slug> [saida.epub]

Passos (determinísticos):
 1. copia o curso para uma pasta temporária;
 2. troca cada cheat sheet pela versão em 2 partes de img/epub/;
 3. converte SVG -> PNG 2x (rsvg-convert; sem ele, Playwright/Chromium);
 4. troca .svg) por .png) nas aulas;
 5. pandoc com metadata.yaml, epub/estilo.css, capa e --mathml;
 6. descompacta e roda ferramentas/verificar_epub.js (se o Node existir).
Saída JSON: caminho do EPUB, nº de PNGs, imagens faltando e o resultado
da checagem de transbordo (precisa ser zero).
"""
import glob, json, os, re, shutil, subprocess, sys, tempfile, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JS = r"""
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const f of process.argv.slice(2)){
 await p.goto('file://'+f);const s=await p.$('svg');const bb=await s.boundingBox();
 await p.setViewportSize({width:Math.ceil(bb.width),height:Math.ceil(bb.height)});
 await p.goto('file://'+f);
 await (await p.$('svg')).screenshot({path:f.replace(/\.svg$/,'.png'),scale:'device'});}
await b.close()})();
"""


def svg_para_png(svgs):
    if shutil.which('rsvg-convert'):
        for s in svgs:
            subprocess.run(['rsvg-convert', '-z', '2', '-b', 'white', '-o',
                            s[:-4] + '.png', s], check=True)
        return 'rsvg-convert'
    js = os.path.join(tempfile.gettempdir(), 'svg2png.js')
    open(js, 'w').write(JS.replace("newPage()", "newPage({deviceScaleFactor:2})"))
    env = dict(os.environ)
    if 'NODE_PATH' not in env and shutil.which('npm'):
        env['NODE_PATH'] = subprocess.run(['npm', 'root', '-g'], capture_output=True,
                                          text=True).stdout.strip()
    for i in range(0, len(svgs), 40):
        subprocess.run(['node', js, *svgs[i:i + 40]], check=True,
                       cwd=os.path.dirname(js), env=env)
    return 'playwright'


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    curso = os.path.abspath(sys.argv[1].rstrip('/'))
    nome = os.path.basename(curso)
    saida = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else f'/tmp/{nome}.epub'
    tmp = tempfile.mkdtemp()
    shutil.copytree(curso, tmp, dirs_exist_ok=True)
    aulas = sorted(glob.glob(f'{tmp}/aulas/[0-9]*.md'))
    # 2. cheat sheets -> 2 partes
    for e in glob.glob(f'{tmp}/img/epub/*-1.svg'):
        n = os.path.basename(e)[:-6]
        for a in aulas:
            s = open(a, encoding='utf-8').read()
            s2 = re.sub(rf'!\[([^\]]*)\]\(\.\./img/{re.escape(n)}\.svg\)',
                        rf'![\1](../img/epub/{n}-1.svg)\n\n![](../img/epub/{n}-2.svg)', s)
            if s2 != s:
                open(a, 'w', encoding='utf-8').write(s2)
    # 3-4. svg -> png
    svgs = glob.glob(f'{tmp}/img/*.svg') + glob.glob(f'{tmp}/img/epub/*.svg')
    motor = svg_para_png(svgs) if svgs else None
    faltando = []
    for a in aulas:
        s = open(a, encoding='utf-8').read()
        s = re.sub(r'(\.\./img/[^)]+)\.svg\)', r'\1.png)', s)
        open(a, 'w', encoding='utf-8').write(s)
        for ref in re.findall(r'\]\(\.\./img/([^)]+)\)', s):
            if not os.path.exists(f'{tmp}/img/{ref}'):
                faltando.append(ref)
    # 5. pandoc
    cmd = ['pandoc', f'--metadata-file={curso}/metadata.yaml', f'--resource-path={tmp}/aulas',
           f'--css={RAIZ}/epub/estilo.css', '--toc', '--toc-depth=2', '--split-level=1',
           '--mathml', '-o', saida, *aulas]
    if os.path.exists(f'{curso}/capa.png'):
        cmd.insert(1, f'--epub-cover-image={curso}/capa.png')
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = {'epub': saida if r.returncode == 0 else None, 'pandoc_erro': r.stderr[-800:] or None,
           'pngs': len(svgs), 'conversor': motor, 'img_faltando': sorted(set(faltando))}
    # 6. checagem de e-reader
    if r.returncode == 0 and shutil.which('node'):
        dz = tempfile.mkdtemp()
        zipfile.ZipFile(saida).extractall(dz)
        v = subprocess.run(['node', f'{RAIZ}/ferramentas/verificar_epub.js', dz],
                           capture_output=True, text=True)
        out['verificar_epub'] = (v.stdout + v.stderr)[-1500:]
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
