"""Converte a exportação HTML de um curso do Notion em Markdown para a Biblioteca de Estudos.

Uso: python3 -I ferramentas/notion2md.py <pasta-da-exportacao> <pasta-do-curso>
Gera <pasta-do-curso>/aulas/NN-<slug>.md e copia as imagens para <pasta-do-curso>/img/.
"""
import os, re, sys, shutil, unicodedata, urllib.parse
from bs4 import BeautifulSoup, NavigableString, Tag

SRC = sys.argv[1]          # pasta da exportação
OUT = sys.argv[2]          # pasta do curso no repo
PERSONAL = [("Josue B. Almeida", "Ana Souza"), ("Josué B. Almeida", "Ana Souza")]

def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii','ignore').decode()
    t = re.sub(r'[^a-zA-Z0-9]+', '-', t.lower()).strip('-')
    if len(t) > 48:
        t = t[:48].rsplit('-', 1)[0]
    return t

def inline(el):
    if isinstance(el, NavigableString):
        return str(el).replace('\u00a0', ' ')
    name = el.name
    inner = ''.join(inline(c) for c in el.children)
    if name in ('strong','b'):
        return f'**{inner}**' if inner.strip() else inner
    if name in ('em','i'):
        return f'*{inner}*' if inner.strip() else inner
    if name == 'code':
        t = el.get_text()
        tick = '``' if '`' in t else '`'
        return f'{tick}{t}{tick}'
    if name == 'a':
        href = el.get('href','')
        if href.startswith('http'):
            return f'[{inner}]({href})'
        return inner
    if name == 'br':
        return '<br>'
    if name == 'span' and 'icon' in (el.get('class') or []):
        return el.get('data-emoji','')
    return inner

def reindentar(code):
    """Recuo de 4 espaços vira 2 (mais espaço útil na tela do e-reader)."""
    linhas = code.split('\n')
    recuos = [len(l) - len(l.lstrip(' ')) for l in linhas if l.strip() and l.startswith(' ')]
    if not recuos or any(r % 4 for r in recuos):
        return code
    return '\n'.join(' ' * ((len(l) - len(l.lstrip(' '))) // 2) + l.lstrip(' ') if l.strip() else l for l in linhas)

def esc_cell(s):
    return s.replace('|', '\\|').replace('\n',' ').strip()

class Conv:
    def __init__(self, is_list, imgdir):
        self.is_list = is_list
        self.imgdir = imgdir
        self.last_h2 = ''
        self.images = []
        self.shift = False
    def blocks(self, parent):
        out = []
        for c in parent.children:
            if isinstance(c, NavigableString):
                if c.strip(): out.append(c.strip())
                continue
            r = self.block(c)
            if not r: continue
            islist = lambda x: bool(re.match(r'(- |\d+\. )', x))
            if out and c.name in ('ul','ol') and islist(out[-1]) and getattr(self,'_prev_list',False):
                out[-1] += '\n' + r
            else:
                out.append(r)
            self._prev_list = c.name in ('ul','ol')
        return out
    def block(self, el):
        n = el.name; cls = el.get('class') or []
        if n in ('script','link','style'): return ''
        if n == 'nav': return ''  # table-of-contents do Notion
        if n in ('h1','h2','h3'):
            t = inline(el).strip()
            t = re.sub(r'\*\*(.*?)\*\*', r'\1', t)
            if n in ('h1', 'h2', 'h3'): self.last_h2 = t
            if self.shift:
                lvl = {'h1':'##','h2':'###','h3':'####'}[n]
            else:
                lvl = {'h1':'##','h2':'##','h3':'###'}[n]
            return f'{lvl} {t}'
        if n == 'p':
            t = inline(el).strip()
            return t
        if n == 'ul':
            return '\n'.join('- ' + self.li(li) for li in el.find_all('li', recursive=False))
        if n == 'ol':
            start = int(el.get('start', 1))
            return '\n'.join(f'{start+i}. ' + self.li(li) for i, li in enumerate(el.find_all('li', recursive=False)))
        if n == 'pre':
            lang = el.get('data-notion-code-syntax','') or ''
            lang = {'plain text':'text','txt':'text','shell':'bash'}.get(lang.lower(), lang.lower())
            code = el.get_text().replace('\t', '  ')
            code = re.sub(r'(\S) {3,}(//|\.\.\. |# |←|→)', r'\1  \2', code)
            code = reindentar(code)  # alinhamento de comentários estoura a largura em e-readers
            return f'```{lang}\n{code.rstrip()}\n```'
        if n == 'figure':
            if 'image' in cls:
                img = el.find('img')
                if not img: return ''
                src = urllib.parse.unquote(img['src'])
                base = os.path.basename(src)
                self.images.append(src)
                cap = el.find('figcaption')
                cap = inline(cap).strip() if cap else ''
                return f'![{cap}](../img/{base})'
            if 'link-to-page' in cls: return ''
            a = el.find('a', class_='bookmark')
            if a:
                title = el.find(class_='bookmark-title')
                t = title.get_text().strip() if title else a['href']
                return f'🔗 [{t or a["href"]}]({a["href"]})'
            return ''   # pdf / file blocks não são publicados
        if n == 'aside':
            icon = el.get('data-notion-callout-icon','')
            body = el.find_all('div', recursive=False)[-1]
            parts = self.blocks(body)
            if not parts: return ''
            first = parts[0]
            lines = [f'{icon} {first}'] + parts[1:]
            txt = '\n\n'.join(lines)
            return '\n'.join('> ' + l if l else '>' for l in txt.split('\n'))
        if n == 'details':
            summ = el.find('summary')
            stext = inline(summ).strip() if summ else ''
            stext_plain = re.sub(r'\*\*(.*?)\*\*', r'\1', stext)
            body = el.find('div', class_='indented')
            parts = self.blocks(body) if body else []
            if not parts: return ''
            content = '\n\n'.join(parts)
            h = self.last_h2.lower()
            answer = (self.is_list or h.startswith('desafio') or 'exercício' in h
                      or stext_plain.lower().startswith('resolução'))
            if answer:
                low = stext_plain.lower()
                if low in ('resolução', 'código', 'código resposta', 'resposta'):
                    label = 'Ver resposta'
                elif low.startswith('resolução'):
                    label = 'Ver resposta ' + stext_plain[len('Resolução'):].strip()
                else:
                    label = 'Ver resposta: ' + stext_plain
                return f'<details>\n<summary>{label}</summary>\n\n{content}\n\n</details>'
            return f'**{stext_plain}**\n\n{content}'
        if n == 'table':
            rows = el.find_all('tr')
            if not rows: return ''
            m = [[esc_cell(inline(td)) for td in r.find_all(['td','th'])] for r in rows]
            w = max(len(r) for r in m)
            m = [r + ['']*(w-len(r)) for r in m]
            out = ['| ' + ' | '.join(m[0]) + ' |', '| ' + ' | '.join(['---']*w) + ' |']
            out += ['| ' + ' | '.join(r) + ' |' for r in m[1:]]
            return '\n'.join(out)
        if n == 'blockquote':
            return '> ' + inline(el).strip()
        if n == 'hr': return '---'
        if n == 'div':
            return '\n\n'.join(self.blocks(el))
        return inline(el).strip()
    def li(self, li):
        txt = ''
        subs = []
        for c in li.children:
            if isinstance(c, Tag) and c.name in ('ul','ol'):
                subs.append(self.block(c))
            else:
                txt += inline(c)
        res = txt.strip()
        for s in subs:
            res += '\n' + '\n'.join('  ' + l for l in s.split('\n'))
        return res

def polir_summaries(s):
    s = s.replace('<summary>Ver resposta direta</summary>', '<summary>Ver resposta</summary>')
    def ext(m):
        resto = m.group(2)
        if not resto: return '<summary>Ver versão estendida</summary>'
        if resto.startswith('('): return f'<summary>Ver versão estendida {resto}</summary>'
        return f'<summary>Ver versão estendida: {resto}</summary>'
    return re.sub(r'<summary>Ver resposta: (Versão estendida original|Versão estendida|Variação original):? ?(.*?)</summary>', ext, s)

def convert_page(path, is_list, imgdir):
    soup = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    title = soup.find('h1', class_='page-title').get_text().strip()
    body = soup.find('div', class_='page-body')
    c = Conv(is_list, imgdir)
    c.shift = body.find('h1') is not None
    parts = c.blocks(body)
    md = f'# {title}\n\n' + '\n\n'.join(p for p in parts if p.strip()) + '\n'
    for a,b in PERSONAL: md = md.replace(a,b)
    md = md.replace(' Cada um traz o enunciado, a resolução e o arquivo `.por` original.', ' Cada um traz o enunciado e a resolução, que fica recolhida: tente resolver antes de abrir.')
    md = re.sub(r'\n{3,}', '\n\n', md)
    # copia imagens
    for src in c.images:
        p = os.path.join(os.path.dirname(path), src)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(imgdir, os.path.basename(src)))
        else:
            print('IMAGEM FALTANDO', p)
    return title, md

if __name__ == '__main__':
    idx = [f for f in os.listdir(SRC) if f.endswith('.html')][0]
    soup = BeautifulSoup(open(os.path.join(SRC, idx), encoding='utf-8').read(), 'html.parser')
    os.makedirs(os.path.join(OUT,'img'), exist_ok=True)
    os.makedirs(os.path.join(OUT,'aulas'), exist_ok=True)
    order = []
    for fig in soup.select('figure.link-to-page a'):
        order.append(urllib.parse.unquote(fig['href']))
    pages = []
    for i, rel in enumerate(order, start=1):
        title = None
        is_list = 'Lista de exerc' in rel or os.path.basename(rel).startswith('Desafio')
        t, md = convert_page(os.path.join(SRC, rel), is_list, os.path.join(OUT,'img'))
        fn = f'{i:02d}-{slug(t)}.md'
        md = polir_summaries(md)
        open(os.path.join(OUT, 'aulas', fn), 'w', encoding='utf-8').write(md)
        pages.append((fn, t))
        print(fn)
    print(f'{len(pages)} aulas convertidas em {OUT}/aulas')
