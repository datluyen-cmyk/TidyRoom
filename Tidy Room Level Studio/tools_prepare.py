from pathlib import Path
import sys, json, hashlib, collections, re
H=Path(r'D:/APK Works/HappyTidyRoom'); T=Path(r'D:/APK Works/Tidy Room/analysis'); R=Path(r'D:/APK Works/RoomSort/analysis'); O=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'analysis/vendor'))
import UnityPy
from PIL import Image

def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,d):(O/'data'/p).write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf8')
# Coordinates are in normalized canvas units (left/top = 0, right/bottom = 1).
common=[1,2,3,6,9,11,12,13,14,16,17,18,21,23,24,25,26,27,28,29,30,31,32,33,39,47,49,50,52,53,54,55,58,62,72,74,75,100,101,102,103,104,105,106,107,108,109,111]
bed_floor=[(.06,.65),(.32,.58),(.48,.65),(.75,.57),(.94,.55),(.96,.92),(.08,.93)]
living_floor=[(.08,.60),(.24,.55),(.53,.55),(.93,.58),(.96,.92),(.06,.93)]
kid_floor=[(.08,.63),(.39,.60),(.52,.67),(.82,.55),(.95,.59),(.95,.91),(.07,.92)]
clothes=[1,11,12,14,23,24,28,31,74,103,105,106,107]
small=[13,17,18,21,25,26,27,29,33,39,53,54,58,72,75,101,102,104]
rooms={
 'bedroom':{'label':'Phòng ngủ','types':common,'zones':[{'label':'Sàn và thảm','poly':bed_floor},{'label':'Mặt giường','poly':[(.43,.46),(.59,.37),(.84,.47),(.67,.59)],'types':clothes+[3,17]},{'label':'Mặt tủ','poly':[(.10,.486),(.25,.425),(.37,.46),(.21,.525)],'types':small}], 'anchors':[{'name':'Mép trước giường','u':.612,'v':.61,'pose':'drape','choices':[{'id':'12-4','angle':-12,'scale':.68},{'id':'1-4','angle':-5,'scale':.57},{'id':'24-10','angle':-8,'scale':.72},{'id':'107-6','angle':-12,'scale':.65}]}]},
 'kids_bedroom':{'label':'Phòng giường tầng','types':common,'zones':[{'label':'Sàn và thảm','poly':kid_floor},{'label':'Mặt giường tầng','poly':[(.52,.29),(.63,.265),(.80,.323),(.71,.367)],'types':clothes+[3,17,32]},{'label':'Mặt bàn','poly':[(.12,.481),(.26,.426),(.37,.464),(.23,.517)],'types':small+[2,32]}], 'anchors':[{'name':'Lan can giường tầng','u':.704,'v':.41,'pose':'drape','choices':[{'id':'12-4','angle':-13,'scale':.55},{'id':'24-10','angle':-14,'scale':.6},{'id':'1-4','angle':-15,'scale':.50}]}]},
 'living_room':{'label':'Phòng khách','types':common,'zones':[{'label':'Sàn và thảm','poly':living_floor},{'label':'Mặt bàn','poly':[(.32,.49),(.49,.414),(.64,.472),(.48,.547)],'types':small+[2,3,12,32]},{'label':'Đệm ghế dài','poly':[(.61,.39),(.70,.35),(.86,.455),(.78,.489)],'types':clothes+[3,17]}], 'anchors':[{'name':'Lưng ghế','u':.76,'v':.361,'pose':'drape','choices':[{'id':'12-4','angle':12,'scale':.62},{'id':'1-4','angle':13,'scale':.54},{'id':'24-10','angle':12,'scale':.61}]}]}
}
for room in rooms.values():
 room['zones'][0]['weight']=.68
 room['zones'][1]['weight']=.22
 room['zones'][2]['weight']=.10
 room['zones'][0]['maxInset']=.49

idx=read(T/'unity-index.json'); shapes=read(T/'RoomItemShapes.txt'); ref=read(R/'room-content-expanded.json'); loc=read(R/'vi.json'); en=read(R/'en.json')
explicit_drape={'1-4','1-11','1-15','1-19','1-20','12-1','12-4','24-10','107-6','103-1','103-2'}
# Do not scatter unreviewed alternates from categories with multiple poses onto the floor.
flat_groups={1:{'1-3','1-5','1-16','1-17','1-18','1-22'},12:{'12-2','12-3'},24:{f'24-{i}' for i in [1,2,3,4,5,6,7,8,9,11,12,13,14,15,18,19]},103:{'103-3','103-6'},107:{'107-2','107-3','107-4'},74:set()}
selected={x['id']:x['name'] for x in idx if x['type']=='Sprite' and x['file']=='resources.assets' and (x['name'] in rooms or re.fullmatch(r'\d+-\d+',x['name']) and x['name'] in shapes and int(x['name'].split('-')[0]) in common)}
bundle=T/'art-Tidy-Room_57_apkcube/datapack.unity3d'; env=UnityPy.load(str(bundle)); items={}
for o in env.objects:
 if o.type.name!='Sprite' or o.assets_file.name!='resources.assets' or o.path_id not in selected: continue
 name=selected[o.path_id]; d=o.read(); assert d.m_Name==name; im=d.image.convert('RGBA'); w,h=im.size
 if name in rooms:
  im.save(O/'art'/f'{name}.webp',quality=92,method=4); rooms[name].update(w=w,h=h,src=f'art/{name}.webp'); continue
 typ=int(name.split('-')[0]); poly=shapes[name]['Img']
 if not poly or len(poly)<3:continue
 pose='drape' if name in explicit_drape else 'flat' if typ not in flat_groups or name in flat_groups[typ] else 'restricted'
 if pose=='restricted':continue
 im.thumbnail((220,220),Image.Resampling.LANCZOS); im.save(O/'art'/f'{name}.webp',lossless=True,method=2)
 items[name]={'w':w,'h':h,'poly':poly,'type':typ,'pose':pose,'src':f'art/{name}.webp'}
for bg in rooms.values():
 bg['types']=[t for t in bg['types'] if any(i['type']==t and i['pose']=='flat' for i in items.values())]; assert bg['w']
for t in (13,17,18,101): print(t,loc.get(f'type.{t}'),en.get(f'type.{t}'))
types={str(t):loc.get(f'type.{t}',en.get(f'type.{t}',ref['base']['types'].get(str(t),str(t)))) for t in common}
write('art.json',{'items':items,'rooms':rooms,'types':types})
levels=ref['base']['levels']; rshapes=ref['expanded']['catalog']['items']; used={x['id'] for l in levels for x in l['content']}; odds={int(k):int(v) for k,v in re.findall(r'(\d+):(\d+)',(R/'level-odds.js').read_text(encoding='utf8'))}; write('references.json',{'levels':levels,'shapes':{id:rshapes[id] for id in sorted(used)},'sequence':ref['base']['levelSequence'],'odds':odds})
print('art',len(items),'rooms',len(rooms),'flat types',len(rooms['bedroom']['types']),'ref',len(levels))
