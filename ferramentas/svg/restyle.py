import re,sys
sys.path.insert(0,__import__('os').path.dirname(__file__)); from lib import STYLE,DEFS
def conv(s):
    s=re.sub(r'<style>.*?</style>',f'<style>{STYLE}</style>',s,1,flags=re.S)
    s=re.sub(r'<defs>.*?</defs>',f'<defs>{DEFS}</defs>',s,1,flags=re.S)
    # sublinhado colorido sob o título
    s=re.sub(r'(<text x="([\d.]+)" y="30" class="t c">.*?</text>)',
      lambda m:m.group(1)+f'<rect x="{float(m.group(2))-40}" y="38" width="80" height="4" rx="2" fill="url(#gT0)"/>',s,1)
    # sombra + cantos maiores nas caixas
    def sh(m):
        x,y,w,h,cls=m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
        sd='' if float(h)<26 else f'<rect x="{float(x)+2}" y="{float(y)+3}" width="{w}" height="{h}" rx="8" class="sh"/>'
        return sd+f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{cls}"/>'
    s=re.sub(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="6" class="(x[A-Z])"/>',sh,s)
    return s
for f in sys.argv[1:]:
    open('conv/'+f.split('/')[-1],'w').write(conv(open(f).read()))
