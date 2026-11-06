# Componentes extras: diagramas de sequência, UML, pilhas e tabelas de banco.
from kit import *
AZ,VE,LA,RO,VM='#2563EB','#16A34A','#D97706','#7C3AED','#DC2626'
CODIGO_BAR[0]=True

def atores(d,y,nomes,xs,ks,w=130):
    for n,x,k in zip(nomes,xs,ks):
        d.box(x-w/2,y,w,44,'h'+k[1],n,tcls='b c w')
    return y+44

def vida(d,y0,y1,xs):
    for x in xs: d.raw(f'<path d="M{x},{y0} L{x},{y1}" class="l d" style="stroke:#94A3B8"/>')

def msg(d,y,x1,x2,txt,sub=None,cor='#475569',mono=True):
    d.raw(f'<path d="M{x1},{y} L{x2},{y}" style="stroke:{cor};stroke-width:2.4;fill:none" marker-end="url(#a)"/>')
    cx=(x1+x2)/2
    d.text(cx,y-8,txt,('m b c' if mono else 'b c'))
    if sub: d.text(cx,y+18,sub,'s c')

def seq(d,y,nomes,ks,msgs,gap=62,xs=None):
    xs=xs or ([85,395] if len(nomes)==2 else [80,240,400])
    w=130 if len(nomes)==2 else 110
    y=atores(d,y,nomes,xs,ks,w=w)
    yy=y+36
    pos=[]
    for m in msgs:
        pos.append(yy); yy+=gap
    vida(d,y,yy-gap+30,xs)
    for (a,b,txt,*r),py in zip(msgs,pos):
        sub=r[0] if r else None; cor=r[1] if len(r)>1 else '#475569'
        x1,x2=xs[a],xs[b]
        off=8 if x2>x1 else -8
        msg(d,py,x1+off,x2-off,txt,sub,cor)
    return yy-gap+40

def faixa(d,x,y,w,h,k,txt,cls='m s c'):
    d.rect(x,y,w,h,k,rx=4); d.text(x+w/2,y+h/2+5,txt,cls)

def uml(d,x,y,w,nome,attrs,mets,k='xB',ster=None):
    hh=34+(18 if ster else 0)
    h=hh+len(attrs)*20+len(mets)*20+16
    d.rect(x,y,w,h,k,shadow=True); d.rect(x,y,w,hh,'h'+k[1])
    if ster: d.text(x+w/2,y+18,ster,'s c w'); d.text(x+w/2,y+40,nome,'b c w')
    else: d.text(x+w/2,y+22,nome,'b c w')
    yy=y+hh+20
    for a in attrs: d.text(x+10,yy,a,'m s'); yy+=20
    if attrs and mets: d.raw(f'<line x1="{x}" y1="{yy-12}" x2="{x+w}" y2="{yy-12}" stroke="#9CA3AF" stroke-width="1.5"/>'); yy+=4
    for m in mets: d.text(x+10,yy,m,'m s'); yy+=20
    return y+h

def secao(d,y,h,k,titulo):
    d.rect(20,y,440,h,k,shadow=True); d.text(240,y+24,titulo,'b c')

def pilha(d,y,itens,x=80,w=320,h=50,gap=26,rotulos=None):
    for i,(t,s,k) in enumerate(itens):
        d.box(x,y,w,h,k,t,s,tcls=('b c w' if k[0]=='h' else 'b c'),scls=('s c w' if k[0]=='h' else 's c'))
        if i:
            d.arrow([(x+w/2,y-gap),(x+w/2,y)])
            if rotulos and rotulos[i-1]: d.text(x+w/2+10,y-gap/2+5,rotulos[i-1],'m s')
        y+=h+gap
    return y-gap

def tab(d,x,y,w,nome,cols,k='xB'):
    """tabela de banco: nome + linhas (marca, coluna)"""
    h=34+len(cols)*22+8
    d.rect(x,y,w,h,k,shadow=True); d.rect(x,y,w,32,'h'+k[1]); d.text(x+w/2,y+22,nome,'m b c w')
    yy=y+52
    for m,c in cols:
        if m: d.text(x+10,yy,m,'s b')
        d.text(x+58,yy,c,'m s'); yy+=22
    return y+h
