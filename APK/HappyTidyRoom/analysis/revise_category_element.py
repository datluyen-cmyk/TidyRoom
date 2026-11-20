import pathlib, json, re

r=pathlib.Path(r'D:\APK Works\HappyTidyRoom\analysis')
p=r/'build_original_format.mjs'
s=p.read_text(encoding='utf8')
s=s.replace("'ScoreCombo Text','VFXanim'", "'Category Object','VFXanim'")
start=s.index("const sh=sheets.Overview;")
end=s.index('\n}',start)
s=s[:start]+"""const sh=sheets.Overview;const rows=byName.Overview.rows.slice(0,12).map(r=>[r[0],r[1]]);base(sh,'A1:B13');widths(sh,[160,815]);put(sh,'B1',[['HAPPY TIDY ROOM']]);header(sh,'B1');table(sh,2,rows,[160,815]);sh.getRange('A2:A13').format.font={name:'Arial',size:12,bold:true};sh.getRange('A2:A13').format.horizontalAlignment='center';border(sh,'A2:B13');renders.push(['Overview','A1:B13']);"""+s[end:]
start=s.index("{\nconst labels=['Lớp đồ chồng nhau'")
end=s.index("\n}\n",start)+3
s=s[:start]+"""{
const sh=initTable('Element',['STT','Tên element','Mô tả chi tiết','Mô tả chức năng','Hình ảnh tham khảo','','Unlock'],[
['—','Chưa ghi nhận','Chưa xác nhận cơ chế đặc biệt đang hoạt động trong Happy Tidy Room.','Không đưa khay chờ, hộp thu gom, cảnh báo, độ khó hoặc trợ giúp vào danh sách Element. Danh sách cơ chế đặc biệt đóng gói đang rỗng.','','','—']
],[55,185,290,470,200,20,120]);
put(sh,'A5',[['TÀI NGUYÊN CƠ CHẾ ẨN CÒN TRONG APK — CHƯA XÁC NHẬN SỬ DỤNG']]);sh.getRange('A5:G5').merge();header(sh,'A5:G5');
base(sh,'A6:G7');put(sh,'B6',[['HiddenPassenger','Có icon và tiêu đề cơ chế ẩn trong tài nguyên. Hình ảnh dùng nhân vật hành khách, không phải đồ vật Happy Tidy Room.','Chưa đủ bằng chứng để coi đây là cơ chế của bản game này. Không xác định luật chơi, hiệu ứng hay mốc mở từ tên asset.','','','Chưa xác nhận']]);sh.getRange('A6:G6').format.rowHeightPx=170;
await imageAt(sh,'Icon_HiddenPassenger',5,4,150,150);
await imageAt(sh,'Unlock_Booster_Text_HiddenPassenger',6,4,190,28);sh.getRange('A7:G7').format.rowHeightPx=45;
renders[renders.length-1]=['Element','A1:G7'];
}
"""+s[end:]
needle="initTable('Booster',['STT','Tên booster','Des','Flow','Giá','Unlock','Ảnh','REF'],rows,[50,140,240,400,170,125,100,150]);"
assert needle in s
s=s.replace(needle,"""const sh=initTable('Booster',['STT','Tên booster','Des','Flow','Giá','Unlock','Ảnh','REF'],rows,[50,140,240,400,170,125,180,150]);
for(const row of [2,3,4,5,6])sh.getRange(`A${row}:H${row}`).format.rowHeightPx=Math.max(165,heightFor(rows[row-2],[50,140,240,400,170,125,180,150]));
await imageAt(sh,'NewBooster_Icon_Vaccum',1,6,150,145);
await imageAt(sh,'NewBooster_Icon_Clear',2,6,150,145);
await imageAt(sh,'GP_Box_Unlock',3,6,155,145);
await imageAt(sh,'AddSlot_Img',4,6,165,50);
await imageAt(sh,'GP_Slot_Unlock',4,6,70,70);
put(sh,'G6',[['Gợi ý bằng viền vàng quanh đồ vật; không có icon booster riêng được xác nhận.']]);""")
start=s.index("{\nconst sh=sheets['ScoreCombo Text'];")
end=s.index('\n}\n',start)+3
s=s[:start]+"""{
const sh=sheets['Category Object'];
const inventory=JSON.parse(await fs.readFile(path.join(root,'analysis/category-object.json'),'utf8'));
const groupVi={'Bowling':'Bowling','Restaurant':'Nhà hàng','Art class':'Lớp mỹ thuật','Bakery':'Tiệm bánh','Basketball court':'Sân bóng rổ','Bathroom':'Phòng tắm','Boutique':'Cửa hàng thời trang','Cafe':'Quán cà phê','Classroom':'Lớp học','Common assets':'Đồ dùng chung','Dentist':'Phòng khám nha khoa','Dining':'Phòng ăn','Flower shop':'Cửa hàng hoa','Garage':'Gara','Hair salon':'Tiệm tóc','Kitchen':'Nhà bếp','Laundry':'Phòng giặt','Music studio':'Phòng nhạc','Nail salon':'Tiệm nail','Office & Study room':'Phòng làm việc / học tập','Pet room':'Phòng thú cưng','Pool':'Hồ bơi','Sport':'Thể thao','Tailor shop':'Tiệm may','Toy shop & Playroom':'Cửa hàng đồ chơi / phòng chơi','Arcade':'Khu trò chơi','Christmas':'Giáng sinh','Cinema':'Rạp phim','Circus':'Rạp xiếc','Hotel Lobby':'Sảnh khách sạn','Ice Cream Shop':'Tiệm kem','Lab':'Phòng thí nghiệm','Museum':'Bảo tàng','Riverside':'Ven sông','Sushi Bar':'Quán sushi','Wedding Hall':'Sảnh tiệc cưới','Airport':'Sân bay','Birthday':'Sinh nhật','Garden':'Sân vườn','Magic':'Phép thuật','Photo Studio':'Studio ảnh','Plane Cabin':'Khoang máy bay','Sauna':'Phòng xông hơi','Street Food Stall':'Quầy đồ ăn đường phố'};
const headers=['STT','Nhóm bối cảnh','Category Object','Số asset','Ảnh đại diện','Asset dùng trong dữ liệu màn','Mã category','Ví dụ asset'];
const ws=[60,230,240,100,160,145,130,280];
const n=inventory.categories.length;const last=n+4;
base(sh,`A1:H${last+2}`);widths(sh,ws);
put(sh,'A1',[['CATEGORY OBJECT']]);sh.getRange('A1:H1').merge();header(sh,'A1:H1');
put(sh,'A2',[[`${n} loại đồ vật thuộc ${inventory.groups} nhóm bối cảnh, tổng ${inventory.total.toLocaleString('en-US')} asset sprite. Mỗi asset được đếm một lần theo ID riêng, không đếm số bản sao đặt trong màn. Cột “Asset dùng trong dữ liệu màn” đếm các ID đã xuất hiện trong 65 file màn đóng gói: tổng ${inventory.used.toLocaleString('en-US')} asset. Tên category giữ nguyên theo dữ liệu game để dễ tra cứu. Nguồn: S05, S11.`]]);sh.getRange('A2:H2').merge();sh.getRange('A2:H2').format.rowHeightPx=85;
put(sh,'A4',[headers]);header(sh,'A4:H4');
const rows=inventory.categories.map((x,i)=>[i+1,groupVi[x.group]??x.group,x.category,x.count,'',x.used,x.id,x.example]);
put(sh,'A5',rows);sh.getRange(`A5:H${last}`).format.rowHeightPx=112;sh.getRange(`D5:D${last}`).setNumberFormat('#,##0');sh.getRange(`F5:G${last}`).setNumberFormat('0');
for(let i=0;i<n;i++)await imageAt(sh,`category_${inventory.categories[i].id}`,i+4,4,120,110);
put(sh,`B${last+1}`,[['TỔNG','',null,'',null]]);sh.getRange(`D${last+1}`).formulas=[[`=SUM(D5:D${last})`]];sh.getRange(`F${last+1}`).formulas=[[`=SUM(F5:F${last})`]];header(sh,`A${last+1}:H${last+1}`);sh.freezePanes.freezeRows(4);
renders.push(['Category Object','A1:H14'],['Category Object','A140:H149'],['Category Object',`A${last-8}:H${last+1}`]);
}
"""+s[end:]
s=s.replace("for(const range of ['A1:C1','A11:C11','A20:C20'])sheets['ScoreCombo Text'].getRange(range).merge();\n",'')
# Only changed views need fresh visual verification.
s=s.replace("for(let i=0;i<renders.length;i++){\n const [name,range]=renders[i];", "for(let i=0;i<renders.length;i++){\n const [name,range]=renders[i];if(!['Overview','Element','Booster','Category Object'].includes(name))continue;")
s=s.replace("analysis/original-format-previews/${String(i+1).padStart(2,'0')}.png", "analysis/revision-previews/${String(i+1).padStart(2,'0')}.png")
s=s.replace("await fs.mkdir(path.join(root,'analysis/original-format-previews'),{recursive:true});", "await fs.mkdir(path.join(root,'analysis/revision-previews'),{recursive:true});")
p.write_text(s,encoding='utf8')

# Keep the editable content source aligned with the workbook changes.
cp=r/'gdd-content.json';d=json.loads(cp.read_text(encoding='utf8'))
for sh in d['sheets']:
 if sh['name']=='Overview':sh['rows']=[x for x in sh['rows'] if x[0] not in ['Phạm vi tài liệu','Cách đọc']]
 if sh['name']=='Element':sh['rows']=[['Cơ chế đặc biệt','Chưa xác nhận cơ chế đặc biệt đang hoạt động. Danh sách MechanicDatabase trong APK hiện rỗng. Không liệt kê các thành phần cơ bản hoặc trợ giúp trong mục này.','Chưa ghi nhận','S07'],['Tài nguyên còn sót','Có icon HiddenPassenger và tiêu đề tương ứng, nhưng không đủ bằng chứng xác nhận được dùng trong Happy Tidy Room.','Tài nguyên chưa xác nhận sử dụng','S07']]
 if sh['name']=='ScoreCombo Text':
  inv=json.loads((r/'category-object.json').read_text(encoding='utf8'));sh.update(name='Category Object',title='Category Object — Các loại đồ vật và số asset',rows=[[f'{x["group"]} / {x["category"]}',f'{x["count"]} asset; {x["used"]} asset xuất hiện trong dữ liệu màn. Mã category: {x["id"]}.','Đếm ID sprite riêng biệt','S05, S11'] for x in inv['categories']])
 if sh['name']=='Nguồn & Xác minh':sh['rows'].append(['S11','Thống kê Category Object — analysis/category-object.json. Đối chiếu 2.863 ID catalog với Sprite trong APK: 356 category thuộc 44 nhóm bối cảnh. 2.638 ID được sử dụng trong 65 file dữ liệu màn. Đếm theo ID asset, không đếm bản sao xuất hiện.','Đối chiếu catalog + Sprite + dữ liệu màn','S11'])
cp.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print('Updated builder and document source.')
