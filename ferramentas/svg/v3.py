# Design system v3: "cheat sheet" (fundo creme, cards brancos, acentos pastel,
# setas pontilhadas, código em caixa cinza). Usado por restyle() e cheatsheet().
import re, html, sys
sys.path.insert(0, '/tmp/ss')
from lib import PAL

BG = '#FAF9F6'
FONT = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "'Courier New',Menlo,Consolas,monospace"
# acentos pastel do design system (preenchimento claro, borda, tom forte p/ texto)
ACC = {
 'B': ('#E3EEFF', '#9DBEF5', '#2F5FB3'),  # azul claro
 'C': ('#FFE7E0', '#F5AE9B', '#B4472B'),  # coral
 'G': ('#DDF5EA', '#94D8B8', '#21835A'),  # verde menta
 'P': ('#EEE6FB', '#C3ADEE', '#6B44B8'),  # lilás
 'Y': ('#FFF4CC', '#EBCF6E', '#8A6A00'),  # amarelo pastel
 'T': ('#DDF3F3', '#93D2D2', '#1C7A7A'),  # água
}

# ---------------------------------------------------------------- restyle
# Mapeia as classes antigas (lib.PAL) para os pastéis novos.
OLD2NEW = {'B': 'B', 'G': 'G', 'O': 'Y', 'P': 'P', 'R': 'C', 'T': 'T', 'K': 'C', 'Y': None, 'W': None, 'Z': 'P', 'V': None}

def _style():
    s = (f"text{{white-space:pre;font-family:{FONT};font-size:14px;fill:#2B2B2B}}"
         ".t{font-size:18px;font-weight:800;fill:#1E1E1E;letter-spacing:.2px}.b{font-weight:700}"
         f".m{{font-family:{MONO};font-size:13.5px;font-weight:600}}"
         ".s{font-size:12.5px;fill:#55555F}.n{font-size:13px;font-style:italic;fill:#55555F}"
         ".c{text-anchor:middle}.r{text-anchor:end}.w{fill:#fff}")
    for k, (f, st, dk) in PAL.items():
        n = OLD2NEW.get(k)
        if n:
            fill, stroke, dark = ACC[n]
        elif k in ('W', 'V'):
            fill, stroke, dark = '#FFFFFF', '#E4DED3', '#8A8478'
        else:  # Y: neutro
            fill, stroke, dark = '#F3F0EA', '#D9D2C5', '#6F685C'
        s += f".x{k}{{fill:{fill};stroke:{stroke}}}.h{k}{{fill:{dark};stroke:{dark}}}.f{k}{{fill:{dark}}}"
    s += ("rect,ellipse,polygon,circle{stroke-width:2}"
          ".l{stroke:#7A7F8C;stroke-width:2.4;fill:none;stroke-dasharray:1.5 6;stroke-linecap:round;stroke-linejoin:round}"
          ".d{stroke-dasharray:9 6;stroke-linecap:butt}"
          ".sh{fill:#3A3226;opacity:.07;stroke:none}")
    return s

def _defs():
    return ('<linearGradient id="gT0" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#9DBEF5"/><stop offset=".33" stop-color="#C3ADEE"/>'
            '<stop offset=".66" stop-color="#F5AE9B"/><stop offset="1" stop-color="#EBCF6E"/></linearGradient>'
            '<marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            'orient="auto-start-reverse"><path d="M1,1L9,5L1,9" fill="none" stroke="#7A7F8C" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></marker>')

def restyle(s):
    s = re.sub(r'<style>.*?</style>', f'<style>{_style()}</style>', s, 1, flags=re.S)
    s = re.sub(r'<defs>.*?</defs>', f'<defs>{_defs()}</defs>', s, 1, flags=re.S)
    s = s.replace('<rect width="100%" height="100%" fill="#fff"/>', f'<rect width="100%" height="100%" fill="{BG}"/>', 1)
    # cantos mais arredondados e sombra mais suave nas caixas
    s = re.sub(r'(<rect [^>]*?) rx="8" class="(x[A-Z])"', r'\1 rx="12" class="\2"', s)
    s = re.sub(r'(<rect [^>]*?) rx="8" class="sh"', r'\1 rx="12" class="sh"', s)
    # caixas de código: fundo cinza claro
    s = s.replace('fill="#F8FAFC"', 'fill="#F0F0F0"').replace('stroke="#94A3B8"', 'stroke="#D6D2CA"')
    # setas desenhadas sem classe (cores fixas antigas) passam a pontilhadas
    s = s.replace('stroke="#475569"', 'stroke="#7A7F8C"')
    return s

# ---------------------------------------------------------------- cheat sheet
def esc(t): return html.escape(t, quote=False)

def _check(x, y, k, warn=False):
    f, st, dk = ACC[k]
    if warn:
        return (f'<circle cx="{x}" cy="{y}" r="10" fill="{ACC["C"][0]}" stroke="{ACC["C"][1]}" stroke-width="1.6"/>'
                f'<path d="M{x-3.5},{y-3.5} l7,7 M{x+3.5},{y-3.5} l-7,7" stroke="{ACC["C"][2]}" stroke-width="2.4" stroke-linecap="round"/>')
    return (f'<circle cx="{x}" cy="{y}" r="10" fill="{f}" stroke="{st}" stroke-width="1.6"/>'
            f'<path d="M{x-4.5},{y} l3,3.2 l6,-6.4" fill="none" stroke="{dk}" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round"/>')

def _wrap(t, n):
    out, cur = [], ''
    for w in t.split(' '):
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur: out.append(cur)
    return out

W_SCALE=[1.0]
def card(x, y, w, h, n, c, k):
    """c: dict(t=titulo, i=icone (texto curto), b=[bullets], code=[linhas], tags=[...])"""
    f, st, dk = ACC[k]
    o = [f'<!-- Card {n}: {esc(c["t"])} -->', '<g>',
         f'<rect x="{x}" y="{y+5}" width="{w}" height="{h}" rx="16" fill="#3A3226" opacity=".07"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fff" stroke="{st}" stroke-width="2.2"/>',
         f'<rect x="{x+18}" y="{y+18}" width="58" height="58" rx="14" fill="{f}" stroke="{st}" stroke-width="1.6"/>',
         f'<text x="{x+47}" y="{y+56}" text-anchor="middle" style="font-family:{MONO};font-size:{24 if len(c["i"])<3 else 19}px;font-weight:700;fill:{dk}">{esc(c["i"])}</text>']
    tl = _wrap(f'{n}. {c["t"]}', int(19*W_SCALE[0]))
    for i, l in enumerate(tl):
        o.append(f'<text x="{x+90}" y="{y+(44 if len(tl)>1 else 56)+i*28}" style="font-size:24px;font-weight:800;fill:#1E1E1E">{esc(l)}</text>')
    yy = y + 104
    for b in c.get('b', []):
        ls = _wrap(b, int(29*W_SCALE[0]))
        o.append(_check(x + 34, yy - 7, k, c['i'] == '!' and 'rmadilh' in c['t']))
        for j, l in enumerate(ls):
            o.append(f'<text x="{x+54}" y="{yy+j*25}" style="font-size:20px;fill:#3A3A44">{esc(l)}</text>')
        yy += 25 * len(ls) + 12
    if c.get('tags'):
        tx = x + 20
        for tg in c['tags']:
            tw = 13 * len(tg) + 24
            if tx + tw > x + w - 16: tx = x + 20; yy += 40
            o.append(f'<rect x="{tx}" y="{yy-6}" width="{tw}" height="32" rx="16" fill="{f}" stroke="{st}" stroke-width="1.4"/>')
            o.append(f'<text x="{tx+tw/2}" y="{yy+16}" text-anchor="middle" style="font-family:{MONO};font-size:17px;font-weight:700;fill:{dk}">{esc(tg)}</text>')
            tx += tw + 10
        yy += 44
    if c.get('code'):
        ch = 27 * len(c['code']) + 18
        o.append(f'<rect x="{x+18}" y="{yy-8}" width="{w-36}" height="{ch}" rx="10" fill="#F0F0F0" stroke="#D6D2CA" stroke-width="1.4"/>')
        for j, l in enumerate(c['code']):
            o.append(f'<text x="{x+32}" y="{yy+18+j*27}" style="font-family:{MONO};font-size:17.5px;font-weight:700;fill:#2B2B2B;white-space:pre">{esc(l)}</text>')
        yy += ch + 6
    o.append('</g>')
    return o, yy - y

def cheatsheet(cards, titulo, sub, cols=3, W=1200, tag='', out=None, rows_per_part=None, part_header=True):
    """Gera a folha. cols=3 → 1200x1600 (Notion/GitHub); cols=2 → versão e-reader."""
    ks = ['B', 'C', 'G', 'P', 'Y', 'T']
    m, g = 36, 26
    cw = (W - 2 * m - (cols - 1) * g) / cols
    rows = (len(cards) + cols - 1) // cols
    # altura de cada linha = maior card da linha (ordem: coluna por coluna)
    order = [[None] * cols for _ in range(rows)]
    for i in range(len(cards)):
        order[i % rows][i // rows] = i
    hs = []
    for r in range(rows):
        hh = 0
        for cidx in order[r]:
            if cidx is None: continue
            _, h = card(0, 0, cw, 10, cidx + 1, cards[cidx], 'B')
            hh = max(hh, h + 14)
        hs.append(max(hh, 250))
    top = 196 if part_header else 40
    def header():
        return [f'<text x="{W/2}" y="86" text-anchor="middle" style="font-size:{54 if cols==3 else 40}px;font-weight:900;fill:#1E1E1E;letter-spacing:1px">{esc(titulo.upper())}</text>',
                f'<text x="{W/2}" y="128" text-anchor="middle" style="font-size:{23 if cols==3 else 19}px;fill:#55555F">{esc(sub)}</text>',
                f'<rect x="{W/2-90}" y="146" width="180" height="6" rx="3" fill="url(#gT0)"/>']
    def build(rr, with_header):
        y0 = top if with_header else 40
        H = y0 + sum(hs[r] for r in rr) + g * (len(rr) - 1) + 40
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{int(H)}" viewBox="0 0 {W} {int(H)}" font-family="{FONT}">',
             '<defs>' + _defs() + '</defs>',
             f'<rect width="100%" height="100%" fill="{BG}"/>']
        if with_header: o += header()
        ys = {}
        y = y0
        for r in rr:
            ys[r] = y; y += hs[r] + g
        # conectores pontilhados entre cards da mesma coluna (ordem de leitura)
        for ci in range(cols):
            x = m + ci * (cw + g)
            colk = None
            for a, b in zip(rr, rr[1:]):
                if order[a][ci] is None or order[b][ci] is None: continue
                k = ks[order[a][ci] % len(ks)]
                cx = x + cw - 40
                y1, y2 = ys[a] + hs[a] - 14, ys[b]
                o.append(f'<path d="M{cx},{y1} C{cx+34},{y1+4} {cx+34},{y2-4} {cx+4},{y2-3}" fill="none" stroke="{ACC[k][2]}" '
                         'stroke-width="3" stroke-dasharray="1.5 7" stroke-linecap="round" opacity=".75" marker-end="url(#a)"/>')
        for r in rr:
            for ci in range(cols):
                i = order[r][ci]
                if i is None: continue
                el, _ = card(m + ci * (cw + g), ys[r], cw, hs[r] - 14, i + 1, cards[i], ks[i % len(ks)])
                o += el
        if tag:
            o.append(f'<text x="{W-m}" y="{H-14}" text-anchor="end" style="font-size:15px;fill:#8A8478">{esc(tag)}</text>')
        o.append('</svg>')
        return '\n'.join(o)
    if rows_per_part:
        parts = []
        for p in range(0, rows, rows_per_part):
            parts.append(build(list(range(p, min(rows, p + rows_per_part))), part_header and p == 0))
        return parts
    return build(list(range(rows)), True)

def gerar(nome, cards, titulo, sub, destino):
    """Grava nome.svg (3x4) e epub/nome-1.svg, -2.svg (2 colunas, e-reader)."""
    import os
    assert len(cards) == 12, (nome, len(cards))
    open(f'{destino}/{nome}.svg', 'w').write(cheatsheet(cards, titulo, sub))
    os.makedirs(f'{destino}/epub', exist_ok=True)
    # e-reader: 2 colunas x 6 linhas, em 2 imagens de 3 linhas
    # (ordem coluna a coluna dentro de cada parte)
    for p, sub_cards in enumerate([cards[:6], cards[6:]]):
        svg = cheatsheet(sub_cards, titulo, sub if p == 0 else f'{sub} (continuação)', cols=2, W=800,
                         part_header=True)
        # renumera para manter 7..12 na segunda parte
        if p == 1:
            for i in range(6, 0, -1):
                svg = svg.replace(f'>{i}. ', f'>{i+6}. ').replace(f'Card {i}:', f'Card {i+6}:')
        open(f'{destino}/epub/{nome}-{p+1}.svg', 'w').write(svg)
