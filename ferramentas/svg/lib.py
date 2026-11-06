# Biblioteca mínima para diagramas legíveis em e-reader (largura 480).
import html, os
W=480
PAL={'B':('#EFF6FF','#BFDBFE','#2563EB'),'G':('#F0FDF4','#BBF7D0','#16A34A'),'O':('#FFFBEB','#FDE68A','#D97706'),
'P':('#F5F3FF','#DDD6FE','#7C3AED'),'R':('#FEF2F2','#FECACA','#DC2626'),'Y':('#F9FAFB','#E5E7EB','#6B7280'),
'T':('#F0FDFA','#99F6E4','#0D9488'),'K':('#FDF2F8','#FBCFE8','#DB2777'),'W':('#FFFFFF','#FFFFFF','#9CA3AF'),'Z':('#F5F3FF','#F5F3FF','#DDD6FE'),'V':('#FFFFFF','#FFFFFF','#E5E7EB')}
STYLE=("text{white-space:pre;font-family:Helvetica,Arial,sans-serif;font-size:14px;fill:#1F2937}"
".t{font-size:17px;font-weight:bold;fill:#111827}.b{font-weight:bold}.m{font-family:Menlo,Consolas,monospace;font-size:13px}"
".s{font-size:12.5px;fill:#4B5563}.n{font-size:13px;font-style:italic;fill:#4B5563}.c{text-anchor:middle}.r{text-anchor:end}.w{fill:#fff}"
+''.join(f".x{k}{{fill:url(#g{k});stroke:{c[2]}}}.h{k}{{fill:{c[2]};stroke:{c[2]}}}.f{k}{{fill:{c[2]}}}" for k,c in PAL.items())+
"rect,ellipse,polygon,circle{stroke-width:2}.l{stroke:#475569;stroke-width:2.2;fill:none}.d{stroke-dasharray:6 4}.sh{fill:#0F172A;opacity:.10;stroke:none}")
DEFS=(''.join(f'<linearGradient id="g{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>' for k,c in PAL.items())
+'<linearGradient id="gT0" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2563EB"/><stop offset=".33" stop-color="#7C3AED"/><stop offset=".66" stop-color="#DB2777"/><stop offset="1" stop-color="#F59E0B"/></linearGradient>'
+'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#475569"/></marker>')
class D:
    def __init__(s,h,title=None):
        s.h=h; s.el=[]
        if title:
            s.text(W/2,30,title,'t c'); s.e(f'<rect x="{W/2-40}" y="38" width="80" height="4" rx="2" fill="url(#gT0)"/>')
    def e(s,x): s.el.append(x)
    def text(s,x,y,t,cls='',style=''):
        st=f' style="{style}"' if style else ''
        s.e(f'<text x="{x}" y="{y}" class="{cls}"{st}>{html.escape(t,quote=False)}</text>')
    def lines(s,x,y,ts,cls='',dy=18):
        for i,t in enumerate(ts): s.text(x,y+i*dy,t,cls)
    def rect(s,x,y,w,h,cls='xW',rx=8,shadow=False):
        if shadow: s.e(f'<rect x="{x+2}" y="{y+3}" width="{w}" height="{h}" rx="{rx}" class="sh"/>')
        s.e(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')
    def box(s,x,y,w,h,cls,title,sub=None,tcls='b c',scls='s c'):
        s.rect(x,y,w,h,cls,shadow=True)
        if isinstance(sub,str): sub=[sub] if sub else []
        sub=sub or []
        n=1+len(sub); tot=17+16*(n-1); y0=y+h/2-tot/2+13
        s.text(x+w/2,y0,title,tcls)
        for i,t in enumerate(sub): s.text(x+w/2,y0+18+i*16,t,scls)
    def arrow(s,pts,cls='l',end=True,start=False):
        d='M'+' L'.join(f'{a},{b}' for a,b in pts)
        me=' marker-end="url(#a)"' if end else ''
        ms=' marker-start="url(#a)"' if start else ''
        s.e(f'<path d="{d}" class="{cls}"{me}{ms}/>')
    def raw(s,x): s.e(x)
    def fit(s):
        import re
        m=0
        for e in s.el:
            for y,h in re.findall(r'y="([\d.]+)"(?: width="[\d.]+" height="([\d.]+)")?',e):
                v=float(y)+(float(h) if h else 6); m=max(m,v)
            for pts in re.findall(r'd="M([^"]+)"',e):
                for p in re.findall(r'[\d.]+,([\d.]+)',pts): m=max(m,float(p))
        s.h=int(m+18)
    def svg(s):
        s.fit()
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{s.h}" viewBox="0 0 {W} {s.h}">'
        f'<style>{STYLE}</style><defs>{DEFS}</defs>'
        f'<rect width="100%" height="100%" fill="#fff"/>'+''.join(s.el)+'</svg>')
    def save(s,name):
        open(os.path.join(os.environ.get('SVG_OUT','out'),name),'w').write(s.svg())

def timeline(d,y,items,cls_cycle=('xB','xG','xO','xP')):
    # items: (data, titulo, [linhas])
    x=90; y0=y
    for i,(dt,t,ls) in enumerate(items):
        h=28+16*len(ls)
        d.raw(f'<circle cx="{x}" cy="{y+16}" r="7" fill="#374151"/>')
        d.text(x-14,y+21,dt,'s b r')
        d.rect(x+22,y,W-x-42,h,cls_cycle[i%len(cls_cycle)]); d.text(x+34,y+20,t,'b')
        d.lines(x+34,y+38,ls,'s',dy=16)
        y+=h+10
    d.e(f'<path d="M{x},{y0+16} L{x},{y-26}" class="l"/>')
    d.el.insert(len(d.el)-1-0, '')
    return y
