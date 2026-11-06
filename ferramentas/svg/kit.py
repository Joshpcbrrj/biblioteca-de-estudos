import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from lib import *

def tabela(d, y, ws, cab, linhas, x0=20, h=34, cls=None, mono=None):
    xs=[x0]
    for w in ws: xs.append(xs[-1]+w)
    d.rect(x0,y,sum(ws),h+(len(linhas))*h,'xW',shadow=True)
    d.rect(x0,y,sum(ws),h,'hP',rx=6)
    for i,c in enumerate(cab): d.text(xs[i]+ws[i]/2,y+22,c,'b c w')
    for r,l in enumerate(linhas):
        yy=y+h*(r+1)
        k=(cls[r] if cls else ('xV' if r%2==0 else 'xZ'))
        d.rect(x0,yy,sum(ws),h,k,rx=3)
        for i,c in enumerate(l):
            m = 'm c' if (mono is None or i in mono) else 'c'
            d.text(xs[i]+ws[i]/2,yy+22,c,m)
    return y+h*(len(linhas)+1)

def dia(d,cx,y,t,w=200,h=60,k='xO'):
    d.raw(f'<polygon points="{cx},{y} {cx+w/2},{y+h/2} {cx},{y+h} {cx-w/2},{y+h/2}" class="{k}"/>'); d.text(cx,y+h/2+5,t,'m b c')

def vstack(d,y,itens,x=60,w=360,h=52,gap=18,num=False):
    """itens: (titulo, sub, classe, [tcls])"""
    for i,it in enumerate(itens):
        t,s,k=it[:3]; tc=it[3] if len(it)>3 else 'b c'
        d.box(x,y,w,h,k,t,s,tcls=tc,scls='m c' if tc.startswith('m') else 's c')
        if num:
            d.raw(f'<circle cx="{x-22}" cy="{y+h/2}" r="12" class="h{k[1]}"/>'); d.text(x-22,y+h/2+5,str(i+1),'b c w')
        if i: d.arrow([(x+w/2,y-gap),(x+w/2,y)])
        y+=h+gap
    return y

def nota(d,y,linhas):
    for i,l in enumerate(linhas): d.text(W/2,y+i*20,l,'n c')
    return y+len(linhas)*20

CODIGO_BAR=[False]
def codigo(d,x,y,w,linhas,k='xW',dy=21,bar=None):
    bar=CODIGO_BAR[0] if bar is None else bar
    acc=k[1] if k!='xW' else 'B'
    if bar:
        h=len(linhas)*dy+20+20
        d.rect(x,y,w,h,'xW',shadow=True)
        a2=k[1] if k!='xW' else 'Y'
        d.raw(f'<path d="M{x+8},{y} h{w-16} a8,8 0 0 1 8,8 v12 h-{w} v-12 a8,8 0 0 1 8,-8z" class="f{a2}" opacity="{1 if a2!='Y' else .55}"/>')
        for i,c in enumerate(['#EF4444','#F59E0B','#22C55E']): d.raw(f'<circle cx="{x+14+i*14}" cy="{y+10}" r="4" fill="{c}" stroke="#fff" stroke-width="1"/>')
        d.raw(f'<rect x="{x}" y="{y+20}" width="{w}" height="{h-20}" fill="#F8FAFC" stroke="none" rx="0"/>')
        d.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="#94A3B8" stroke-width="1.8"/>')
        d.lines(x+14,y+44,linhas,'m',dy=dy)
        return y+h
    h=len(linhas)*dy+20
    d.rect(x,y,w,h,'xW',shadow=True)
    d.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.8"/>')
    d.raw(f'<path d="M{x+8},{y} a8,8 0 0 0 -8,8 v{h-16} a8,8 0 0 0 8,8 h-2 v-{h} z" class="f{acc}"/>')
    d.raw(f'<rect x="{x}" y="{y+6}" width="6" height="{h-12}" class="f{acc}"/>')
    d.lines(x+18,y+24,linhas,'m',dy=dy)
    return y+h

def lado(d,y,esq,dir_,h=None):
    """duas colunas: (titulo, classe, [linhas])"""
    hh=h or max(len(esq[2]),len(dir_[2]))*22+50
    for x,(t,k,ls) in [(20,esq),(250,dir_)]:
        d.rect(x,y,210,hh,k); d.text(x+105,y+26,t,'b c')
        d.lines(x+14,y+54,ls,'s',dy=22)
    return y+hh
