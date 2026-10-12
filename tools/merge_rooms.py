import json,re
G=json.load(open('data/groups.json',encoding='utf-8'))
out=[];gym=None;pil=None;kid=None
for g in G:
    l=g['l']
    if g['f']==0 and g['c']=='#ffffff' and not l and g['b'][0][1]>60: continue
    if g['f']==3 and l in('체','육','관'):
        if gym: gym['b']+=g['b']; continue
        g['l']='체육관'; gym=g
    if g['f']==0 and (l=='(주차장)' or (l=='필로티' and g['b'][0][0]<200)):
        if pil: pil['b']+=g['b']; continue
        g['l']='필로티(주차장)'; pil=g
    if g['f']==1 and l in('꿈반 병설유치원','5세'):
        if kid: kid['b']+=g['b']; continue
        g['l']='꿈반(5세)'; kid=g
    g['l']=re.sub(r'^(\d)연구실$',r'\1학년 연구실',g['l'])
    out.append(g)
# 1F 로비(분실물·녹색폴리스)와 중앙현관은 배치도에서 회색(복도색)이라 따로 실로 만든다
LOBBY='#f6cfdc'
lob=[g for g in out if g['f']==0 and g['c']=='#d8d8d8' and (g['l']=='로비' or '분실물' in g['l'])]
if lob:
    keep=lob[0]; keep.update(c=LOBBY,l='로비',s='',n='분실물 보관함 · 녹색어머니·폴리스')
    for g in lob[1:]:
        keep['b']+=g['b']; out.remove(g)
for g in out:
    if g['f']==0 and g['c']=='#d8d8d8':
        hall=[b for b in g['b'] if abs(b[0]-272.9)<1 and b[1]>-1]
        if hall:
            g['b']=[b for b in g['b'] if b not in hall]
            out.append(dict(f=0,c=LOBBY,l='중앙현관',s='',n='현관② · 운동장 쪽 출입구',b=hall))
            break
json.dump(out,open('data/rooms.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for g in out:
    if re.fullmatch(r'[24]-[1-4]',g['l']): print(g['f']+1,g['l'],[(b[0],b[2]) for b in g['b']], round(sum(b[2] for b in g['b']),1))
