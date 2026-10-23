import re,json,html,sys
book=json.load(open('/mnt/user-data/outputs/NEW-version/compass-book.json'))
H3=set()
for e in book['editions']:
    for m in re.finditer(r'<h3 class="sec" data-sec="([^"]*)"',e['html']): H3.add(html.unescape(m.group(1)))
def conv(path,num):
    h=open(path,encoding='utf-8').read()
    h=h.replace('\n</li>','</li>')
    paras=re.split(r'(?<=>)\n(?=<)',h)
    # drop the 3 title lines
    out=[];n=0
    def nid():
        nonlocal n; n+=1; return f'e{num}-{n}'
    started=False
    for blk in paras:
        m=re.fullmatch(r'<p><strong><u>(.*?)</u></strong></p>',blk,re.S)
        if m:
            started=True
            t=m.group(1); plain=html.unescape(re.sub(r'<[^>]+>','',t)).strip()
            if plain in H3 or plain.startswith('Special Mention'):
                ds=plain.split(':')[0] if plain.startswith('Special Mention') else plain
                out.append(f'<h3 class="sec" data-sec="{html.escape(ds,quote=False).replace(chr(34),"&quot;")}" id="{nid()}">{t}</h3>')
            else:
                out.append(f'<h4 class="item" id="{nid()}">{t}</h4>')
            continue
        if not started: continue
        m2=re.fullmatch(r'<p><strong>(.*?)</strong></p>',blk,re.S)
        if m2 and html.unescape(re.sub(r'<[^>]+>','',m2.group(1))).strip() not in ('Prepared by',):
            out.append(f'<h4 class="item" id="{nid()}">{m2.group(1)}</h4>'); continue
        out.append(blk.replace('<br />','<br/>'))
    r='\n'.join(out)
    # The Compass Book no longer carries the 'Previously Featured / Still Recommended' list: those venues live in Concierge Quick Reference.
    r=re.sub(r'<h3 class="sec" data-sec="Previously Featured[^>]*>.*?(?=<h3 class="sec"|$)','',r,flags=re.S)
    r=re.sub(r'<h3 class="sec" data-sec="Unique Locations[^>]*>.*?</ul>\n?','',r,count=1,flags=re.S)
    return r
if __name__=='__main__':
    num=sys.argv[2]; r=conv(sys.argv[1],num); open(sys.argv[3],'w',encoding='utf-8').write(r); print(len(r))
