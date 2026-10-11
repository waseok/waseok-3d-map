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
json.dump(out,open('data/rooms.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
for g in out:
    if re.fullmatch(r'[24]-[1-4]',g['l']): print(g['f']+1,g['l'],[(b[0],b[2]) for b in g['b']], round(sum(b[2] for b in g['b']),1))
