import re
import fitz, json, sys
p=fitz.open(sys.argv[1])[0]
bands={4:(82,140),3:(150,385),2:(390,650),1:(655,915),0:(920,1185)}
anc={4:114,3:207,2:472,1:735,0:1004}
def floor(y):
    for k,(a,b) in bands.items():
        if a<=y<=b: return k
cells=[]
for d in p.get_drawings():
    if d['type']!='f' or len(d['items'])!=4: continue
    r=d['rect']; f=floor((r.y0+r.y1)/2)
    if f is None: continue
    col='#%02x%02x%02x'%tuple(int(v*255) for v in d['fill'])
    if col in('#d9dad9','#d8d9d8'): col='#d8d8d8'
    cells.append(dict(f=f,r=r,c=col,t=[]))
for b in p.get_text('dict')['blocks']:
    for l in b.get('lines',[]):
        for s in l['spans']:
            t=s['text'].strip()
            if not t or '===' in t: continue
            bb=fitz.Rect(s['bbox']); cx,cy=(bb.x0+bb.x1)/2,(bb.y0+bb.y1)/2
            f=floor(cy)
            best=None
            for c in cells:
                if c['f']!=f: continue
                r=c['r']; dx=max(r.x0-cx,0,cx-r.x1); dy=max(r.y0-cy,0,cy-r.y1); dist=(dx*dx+dy*dy)**.5
                key=(round(dist,1),r.width*r.height)
                if best is None or key<best[0]: best=(key,c)
            if best and best[0][0]<4: best[1]['t'].append((round(bb.y0),bb.x0,t,s['color'],bb.x1))
            else: print('skip',t,f)
# union-find merge
n=len(cells); par=list(range(n))
def find(i):
    while par[i]!=i: par[i]=par[par[i]]; i=par[i]
    return i
def touch(a,b):
    A,B=a['r'],b['r'];e=0.8
    if abs(A.x1-B.x0)<e or abs(B.x1-A.x0)<e: return min(A.y1,B.y1)-max(A.y0,B.y0)>2
    if abs(A.y1-B.y0)<e or abs(B.y1-A.y0)<e: return min(A.x1,B.x1)-max(A.x0,B.x0)>2
    return False
lab=[bool(c['t']) for c in cells]
for i in range(n):
    for j in range(i+1,n):
        a,b=cells[i],cells[j]
        if a['f']==b['f'] and a['c']==b['c'] and a['c'] not in ('#9ae4c7','#41c7f1','#ffb589') and touch(a,b):
            ri,rj=find(i),find(j)
            if ri!=rj and not (lab[ri] and lab[rj]):
                par[ri]=rj; lab[rj]=lab[rj] or lab[ri]
# unlabeled classroom cell joins the labelled classroom in the same row whose label text is nearest
# (e.g. 4-2 and 4-1 each span three narrow grid cells, centred on their label)
def lc(c): return sum((t[1]+t[4])/2 for t in c['t'])/len(c['t'])
for i in range(n):
    a=cells[i]
    if a['c']=='#9ae4c7' and not a['t']:
        acx=(a['r'].x0+a['r'].x1)/2
        cand=[j for j in range(n) if cells[j]['f']==a['f'] and cells[j]['c']=='#9ae4c7' and cells[j]['t'] and abs(cells[j]['r'].y0-a['r'].y0)<1]
        if cand:
            j=min(cand,key=lambda j:abs(lc(cells[j])-acx))
            par[find(i)]=find(j)
groups={}
for i,c in enumerate(cells): groups.setdefault(find(i),[]).append(c)
out=[]
extra=[(0,494.1,-32.4,64.6,22.5,'슬기반(4세)'),(0,494.1,-0.2,64.0,23.3,'바른반(3세)'),(1,470.2,-30.8,48.6,21.2,'자람반(유)'),(2,543.4,-30.5,15.9,18.2,'상담실1'),(2,543.4,0.2,15.9,22.3,'원무실')]
for f,x,z,w,dd,l in extra: out.append(dict(f=f,c='#ffffff',l=l,s='',b=[[x,z,w,dd]]))
fix={'체 육 관 공조기':'체육관','2 5 연구실 연구실':'2·5학년 연구실','늘봄 전담실':'늘봄전담실','방송 실':'방송실','스튜 디오':'스튜디오','시설관 리실':'시설관리실','문서 고':'문서고','Wee 클래스':'Wee클래스','꿈반 병설유치원 5세':'꿈반(5세)','자료실 .유':'자료실(유)','돌봄 준비실':'돌봄준비실','필로티 (주차장)':'필로티(주차장)','로 비 (분실물, 녹색폴리스)':'로비','창 고':'창고'}
for g in groups.values():
    ts=sorted(t for c in g for t in c['t'])
    lab=' '.join(t[2] for t in ts if t[3]!=0xff0000)
    red=' '.join(t[2] for t in ts if t[3]==0xff0000)
    f=g[0]['f']
    lab=fix.get(lab,lab)
    if re.fullmatch(r'[^ ]{1,4}( [^ ]{1,4})*',lab) and not re.search(r'\d-\d',lab): lab=lab.replace(' ','')
    out.append(dict(f=f,c=g[0]['c'],l=lab,s=red,b=[[round(c['r'].x0,1),round(c['r'].y0-anc[f],1),round(c['r'].width,1),round(c['r'].height,1)] for c in g]))
json.dump(out,open('data/groups.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
with open('data/labels.txt','w',encoding='utf-8') as fh:
    for o in out:
        if o['c']!='#d8d8d8': fh.write(f"{o['f']+1}F {o['c']} [{o['l']}] {o['s']} cells={len(o['b'])}\n")
print(len(out))
