import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const root='D:/APK Works/HappyTidyRoom';
const out=path.join(root,'outputs/happy-tidy-room-gdd');
const payload=JSON.parse(await fs.readFile(path.join(root,'analysis/gdd-content.json'),'utf8'));
const byName=Object.fromEntries(payload.sheets.map(s=>[s.name,s]));
const wb=Workbook.create();
const sheetNames=['Overview','Gameplay','Object','Element','Booster','Level Progress','Category Object','VFXanim','SFX','Economy','Tutorial','Haptic','UIUX','Nguồn & Xác minh'];
const sheets=Object.fromEntries(sheetNames.map(n=>[n,wb.worksheets.add(n)]));
const green='#B7E1CD';
const renders=[];
function get(name,label){return byName[name].rows.find(r=>r[0]===label)?.[1]??'';}
function put(sh,cell,matrix){sh.getRange(cell).write(matrix);}
function base(sh,range){const r=sh.getRange(range);r.format.font={name:'Arial',size:12,color:'#000000'};r.format.wrapText=true;r.format.verticalAlignment='center';}
function widths(sh,arr){arr.forEach((w,i)=>sh.getRangeByIndexes(0,i,100,1).format.columnWidthPx=w);}
function header(sh,range){const r=sh.getRange(range);r.format.fill=green;r.format.horizontalAlignment='center';r.format.rowHeightPx=30;}
function heightFor(row,widthArr){return Math.ceil(1.28*Math.max(48,...row.map((x,i)=>{let lines=0;for(const s of String(x??'').split('\n')){let len=0;lines++;for(const w of s.split(/\s+/)){const n=w.length*7.2;if(len+n>widthArr[i]-18){lines++;len=n;}else len+=n+4;}}return lines*19+14;})));}
function table(sh,start,rows,widthArr){const sr=start-1;put(sh,`A${start}`,rows);rows.forEach((r,i)=>sh.getRangeByIndexes(sr+i,0,1,r.length).format.rowHeightPx=heightFor(r,widthArr));}
function initTable(name,headers,rows,widthArr){const sh=sheets[name];base(sh,`A1:${String.fromCharCode(64+headers.length)}${rows.length+1}`);widths(sh,widthArr);put(sh,'A1',[headers]);header(sh,`A1:${String.fromCharCode(64+headers.length)}1`);table(sh,2,rows,widthArr);sh.freezePanes.freezeRows(1);renders.push([name,`A1:${String.fromCharCode(64+headers.length)}${rows.length+1}`]);return sh;}
function border(sh,range){sh.getRange(range).format.borders={preset:'all',style:'thin',color:'#999999'};}
async function imageAt(sh,name,row,col,width,height){const bytes=await fs.readFile(path.join(root,`analysis/visuals/${name}.png`));sh.images.add({dataUrl:'data:image/png;base64,'+bytes.toString('base64'),anchor:{from:{row,col},extent:{widthPx:width,heightPx:height}}});}

// OVERVIEW: giữ cột nhãn A và mô tả B, đúng thứ tự của bản mẫu.
{
const sh=sheets.Overview;const rows=byName.Overview.rows.slice(0,12).map(r=>[r[0],r[1]]);base(sh,'A1:B13');widths(sh,[160,815]);put(sh,'B1',[['HAPPY TIDY ROOM']]);header(sh,'B1');table(sh,2,rows,[160,815]);sh.getRange('A2:A13').format.font={name:'Arial',size:12,bold:true};sh.getRange('A2:A13').format.horizontalAlignment='center';border(sh,'A2:B13');renders.push(['Overview','A1:B13']);
}

// GAMEPLAY: bốn dòng Core gameplay / Win / Lose / Revive như mẫu.
{
const sh=sheets.Gameplay;base(sh,'A1:B4');widths(sh,[150,975]);
const core='Chạm item để dọn vào hộp chứa đúng nhóm.\n\nItem chưa có hộp nhận sẽ vào slot chờ và chuyển vào hộp khi có nhóm phù hợp.\n\nĐồ vật xếp theo layer; đồ bị đè chưa lấy được, cần dọn đồ phía trên trước.';
const rows=[['Core gameplay',core],['Win','Khi toàn bộ item trên level được dọn sạch vào các hộp chứa.'],['Lose','Khi đầy hết slot chờ mà vẫn còn item trên màn chơi, các hộp chứa chưa được đầy hết.'],['Revive','Dùng coin hoặc xem quảng cáo để dọn slot chờ và tiếp tục chơi.']];table(sh,1,rows,[150,975]);sh.getRange('A1:A4').format.font={name:'Arial',size:12,bold:true};sh.getRange('A1:A4').format.horizontalAlignment='center';sh.getRange('B1:B4').format.verticalAlignment='top';renders.push(['Gameplay','A1:B4']);
}

{
const labels=['Đồ vật thu gom','Hộp đang mở','Hộp khóa','Khay chờ','Kho tạm','Phông phòng'];
const note=[get('Đồ vật & Hộp','Nhóm và biến thể'),get('Đồ vật & Hộp','Ví dụ yêu cầu hộp'),'Hiệu lực mở hộp qua màn sau: cần chơi xác nhận.','Mặc định 5 ô; scene còn 2 ô bổ sung.','Giới hạn kho và thứ tự trả đồ: cần chơi xác nhận.',get('Đồ vật & Hộp','Quy mô thư viện')];
const rows=labels.map((l,i)=>[i+1,l,get('Đồ vật & Hộp',l),'','',note[i]]);
const sh=initTable('Object',['STT','Tên hình dạng','Mô tả chi tiết','Ảnh','','LƯU Ý'],rows,[65,170,370,190,25,340]);
await imageAt(sh,'Hanger_3',1,3,150,115);
await imageAt(sh,'GP_Box0',2,3,150,125);
await imageAt(sh,'GP_Box_Unlock',3,3,150,125);
await imageAt(sh,'WaitingSlots_Reference',4,3,180,42);
await imageAt(sh,'GP_Icon_RainbowBox',5,3,150,125);
await imageAt(sh,'HT_BG_01',6,3,130,160);
for(const r of [2,3,4,5,6,7])sh.getRange(`A${r}:F${r}`).format.rowHeightPx=Math.max(r===7?175:140,heightFor(rows[r-2],[65,170,370,190,25,340]));
}

{
const sh=initTable('Element',['STT','Tên element','Mô tả chi tiết','Mô tả chức năng','Hình ảnh tham khảo','','Unlock'],[
['—','Chưa ghi nhận','Chưa xác nhận cơ chế đặc biệt đang hoạt động trong Happy Tidy Room.','Không đưa khay chờ, hộp thu gom, cảnh báo, độ khó hoặc trợ giúp vào danh sách Element. Danh sách cơ chế đặc biệt đóng gói đang rỗng.','','','—']
],[55,185,290,470,200,20,120]);
put(sh,'A5',[['TÀI NGUYÊN CƠ CHẾ ẨN CÒN TRONG APK — CHƯA XÁC NHẬN SỬ DỤNG']]);sh.getRange('A5:G5').merge();header(sh,'A5:G5');
base(sh,'A6:G7');put(sh,'B6',[['HiddenPassenger','Có icon và tiêu đề cơ chế ẩn trong tài nguyên. Hình ảnh dùng nhân vật hành khách, không phải đồ vật Happy Tidy Room.','Chưa đủ bằng chứng để coi đây là cơ chế của bản game này. Không xác định luật chơi, hiệu ứng hay mốc mở từ tên asset.','','','Chưa xác nhận']]);sh.getRange('A6:G6').format.rowHeightPx=170;
await imageAt(sh,'Icon_HiddenPassenger',5,4,150,150);
await imageAt(sh,'Unlock_Booster_Text_HiddenPassenger',6,4,190,28);sh.getRange('A7:G7').format.rowHeightPx=45;
renders[renders.length-1]=['Element','A1:G7'];
}

{
const rows=[
[1,'Vacuum','Hoàn tất ngay 1 hộp. Chưa chốt quy tắc chọn hộp mục tiêu.','Bấm Vacuum → dùng lượt hiện có hoặc mở popup mua → phát hiệu ứng hút → hoàn tất 1 hộp. Nếu không có đích, báo “No box can be filled”.','Coin / Ads; giá hiệu lực chưa xác minh','Level 3','','S04, S07, S08'],
[2,'Broom','Chuyển toàn bộ đồ từ khay chờ sang kho tạm, giải phóng chỗ trống.','Bấm Broom → dùng lượt hoặc mua → quét các món từ khay sang kho → tiếp tục thu gom. Khay trống sẽ báo “No items in the waiting slots”.','Coin / Ads; giá hiệu lực chưa xác minh','Level 6','','S04, S07, S08'],
[3,'Extra Box','Mở thêm 1 hộp đang khóa, tối đa 3 hộp cùng lúc.','Chạm hộp khóa → chọn cách mở → hộp được thêm vào hàng đang nhận đồ. Hiệu lực qua màn sau chưa xác minh.','Có luồng mua; chưa chốt giá','Chưa xác minh','','S02, S04, S07'],
[4,'Extra Slot','Mở thêm chỗ chứa trong khay. Scene có 2 ô bổ sung.','Chạm ô khóa → mở popup → nhận thêm chỗ chứa. Cần xác minh số ô được mở mỗi lần và hiệu lực qua màn.','Có luồng mua; chưa chốt giá','Chưa xác minh','','S04, S07'],
[5,'Hint','Gợi ý đồ phù hợp bằng viền vàng và nhịp phóng nhẹ.','Không thao tác 7 giây → hiện gợi ý. Có điều khiển khả dụng từ Remote Config.','Chưa thấy giá mua','Bật trong cấu hình','','S02, S09']];
const sh=initTable('Booster',['STT','Tên booster','Des','Flow','Giá','Unlock','Ảnh','REF'],rows,[50,140,240,400,170,125,180,150]);
for(const row of [2,3,4,5,6])sh.getRange(`A${row}:H${row}`).format.rowHeightPx=Math.max(165,heightFor(rows[row-2],[50,140,240,400,170,125,180,150]));
await imageAt(sh,'NewBooster_Icon_Vaccum',1,6,150,145);
await imageAt(sh,'NewBooster_Icon_Clear',2,6,150,145);
await imageAt(sh,'GP_Box_Unlock',3,6,155,145);
await imageAt(sh,'ExtraSlot_Reference',4,6,170,145);
put(sh,'G6',[['Gợi ý bằng viền vàng quanh đồ vật; không có icon booster riêng được xác nhận.']]);
}

initTable('Level Progress',['Level','Name File','Độ khó'],[['Chưa viết','Theo yêu cầu, tạm thời chưa biên soạn Level Progress.','']],[110,640,180]);

{
const sh=sheets['Category Object'];
const inventory=JSON.parse(await fs.readFile(path.join(root,'analysis/category-object.json'),'utf8'));
const groupVi={'Bowling':'Bowling','Restaurant':'Nhà hàng','Art class':'Lớp mỹ thuật','Bakery':'Tiệm bánh','Basketball court':'Sân bóng rổ','Bathroom':'Phòng tắm','Boutique':'Cửa hàng thời trang','Cafe':'Quán cà phê','Classroom':'Lớp học','Common assets':'Đồ dùng chung','Dentist':'Phòng khám nha khoa','Dining':'Phòng ăn','Flower shop':'Cửa hàng hoa','Garage':'Gara','Hair salon':'Tiệm tóc','Kitchen':'Nhà bếp','Laundry':'Phòng giặt','Music studio':'Phòng nhạc','Nail salon':'Tiệm nail','Office & Study room':'Phòng làm việc / học tập','Pet room':'Phòng thú cưng','Pool':'Hồ bơi','Sport':'Thể thao','Tailor shop':'Tiệm may','Toy shop & Playroom':'Cửa hàng đồ chơi / phòng chơi','Arcade':'Khu trò chơi','Christmas':'Giáng sinh','Cinema':'Rạp phim','Circus':'Rạp xiếc','Hotel Lobby':'Sảnh khách sạn','Ice Cream Shop':'Tiệm kem','Lab':'Phòng thí nghiệm','Museum':'Bảo tàng','Riverside':'Ven sông','Sushi Bar':'Quán sushi','Wedding Hall':'Sảnh tiệc cưới','Airport':'Sân bay','Birthday':'Sinh nhật','Garden':'Sân vườn','Magic':'Phép thuật','Photo Studio':'Studio ảnh','Plane Cabin':'Khoang máy bay','Sauna':'Phòng xông hơi','Street Food Stall':'Quầy đồ ăn đường phố'};
const categoriesByName=new Map();
for(const x of inventory.categories){
 let row=categoriesByName.get(x.category);
 if(!row){row={category:x.category,contexts:[],ids:[],count:0,used:0,example:x.example,imageId:x.id};categoriesByName.set(x.category,row);}
 const context=groupVi[x.group]??x.group;if(!row.contexts.includes(context))row.contexts.push(context);
 row.ids.push(x.id);row.count+=x.count;row.used+=x.used;
}
const boxCategories=[...categoriesByName.values()].sort((a,b)=>a.contexts.join(' / ').localeCompare(b.contexts.join(' / '),'vi')||a.category.localeCompare(b.category,'en'));
const headers=['STT','Nhóm đồ hộp nhận','Bối cảnh trong catalog','Số asset','Ảnh đại diện','Asset dùng trong dữ liệu màn','Mã category','Ví dụ asset'];
const ws=[60,240,230,100,160,145,150,280];
const n=boxCategories.length;const last=n+4;
base(sh,`A1:H${last+2}`);widths(sh,ws);
put(sh,'A1',[['CATEGORY OBJECT']]);sh.getRange('A1:H1').merge();header(sh,'A1:H1');
put(sh,'A2',[[`${n} tên nhóm đồ hộp nhận, ứng với ${inventory.categories.length} mã category và ${inventory.total.toLocaleString('en-US')} asset. order.type trong dữ liệu màn trỏ tới mã category; tên nhóm giữ nguyên theo catalog. Các category cùng tên được gộp và cộng số asset (Gift box: 2 mã, 13 asset). Bối cảnh là nhóm tài nguyên trong catalog, dùng tham khảo khi chọn bộ đồ cho level; không giới hạn nơi đồ vật được xuất hiện. Mỗi asset tính một lần theo ID, không tính số bản sao đặt trong màn. Cột asset dùng trong dữ liệu màn đếm ID xuất hiện trong 65 file màn: ${inventory.used.toLocaleString('en-US')}. Nguồn: S05, S11.`]]);sh.getRange('A2:H2').merge();sh.getRange('A2:H2').format.rowHeightPx=112;
put(sh,'A4',[headers]);header(sh,'A4:H4');sh.getRange('A4:H4').format.rowHeightPx=58;
const rows=boxCategories.map((x,i)=>[i+1,x.category,x.contexts.join(' / '),x.count,'',x.used,x.ids.join(', '),x.example]);
put(sh,'A5',rows);sh.getRange(`A5:H${last}`).format.rowHeightPx=112;sh.getRange(`D5:D${last}`).setNumberFormat('#,##0');sh.getRange(`F5:G${last}`).setNumberFormat('0');
for(let i=0;i<n;i++)await imageAt(sh,`category_${boxCategories[i].imageId}`,i+4,4,120,110);
border(sh,`A4:H${last+1}`);
const contextColors=['#F1F7FC','#F4F8EF','#FCF4EE','#F6F1FA','#EDF8F6','#FCF2F5'];
for(let start=0,groupIndex=0;start<n;groupIndex++){
 const context=boxCategories[start].contexts.join(' / ');let end=start+1;
 while(end<n&&boxCategories[end].contexts.join(' / ')===context)end++;
 sh.getRange(`A${start+5}:H${end+4}`).format.fill=contextColors[groupIndex%contextColors.length];
 for(let chunk=start;chunk<end;chunk+=10){
  const chunkEnd=Math.min(chunk+10,end);
  if(chunkEnd-chunk>1){
   sh.getRange(`C${chunk+6}:C${chunkEnd+4}`).write(Array.from({length:chunkEnd-chunk-1},()=>['']));
   sh.getRange(`C${chunk+5}:C${chunkEnd+4}`).merge();
  }
  const groupRange=sh.getRange(`C${chunk+5}:C${chunkEnd+4}`);
  groupRange.format.horizontalAlignment='center';groupRange.format.verticalAlignment='center';
 }
 start=end;
}
put(sh,`B${last+1}`,[['TỔNG','',null,'',null]]);sh.getRange(`D${last+1}`).formulas=[[`=SUM(D5:D${last})`]];sh.getRange(`F${last+1}`).formulas=[[`=SUM(F5:F${last})`]];header(sh,`A${last+1}:H${last+1}`);sh.freezePanes.freezeRows(4);
renders.push(['Category Object','A1:H15'],['Category Object','A140:H149'],['Category Object',`A${last-8}:H${last+1}`]);
}

{
const rows=[
['V_01','Đồ vật','Click / Select / Collect','Khi chọn và thu gom món đồ',get('VFXanim','Chạm chọn đồ'),'Có tham chiếu hiệu ứng; cần xem runtime.','S02'],
['V_02','Đồ vật','Fly / Hop','Khi món được gửi đến đích',get('VFXanim','Đồ bay vào đích'),'Thông số preset đóng gói.','S02'],
['V_03','Hộp','Box_start / Box_idle / Box_action','Hộp vào màn, chờ hoặc nhận đồ',get('VFXanim','Hộp bắt đầu / chờ'),'','S07, S10'],
['V_04','Hộp','Box_Com / Box_com_idle','Hộp nhận đủ đồ',get('VFXanim','Hoàn thành hộp'),'Chưa đo tổng thời gian chuỗi hoàn tất.','S02, S10'],
['V_05','Kho','Storage_start / idle / Action / end','Kho xuất hiện, nhận hoặc trả đồ',get('VFXanim','Kho tạm'),'','S02, S07, S10'],
['V_06','Booster','Broom / vacuum','Sử dụng trợ giúp',get('VFXanim','Broom / Vacuum'),'','S02, S07, S10'],
['V_07','Hint','Outline / Scale','Không thao tác 7 giây',get('VFXanim','Gợi ý'),'','S02'],
['V_08','Khay','LastSlotWarning','Khay còn 1 ô trống',get('VFXanim','Cảnh báo khay'),'','S02'],
['V_09','Kết quả','Win / Lose','Kết màn',get('VFXanim','Thắng / thua'),'','S02, S07, S10'],
['V_10','Trợ giúp','Box_AddSlot / AnimAddSlots / Revive','Mở hộp, thêm ô hoặc hồi sinh',get('VFXanim','Mở hộp / thêm ô / hồi sinh'),'','S10']];
initTable('VFXanim',['ID','Type','VFX Name','Trigger','Visual Description','Note','REF'],rows,[70,100,205,230,500,190,120]);
}

{
const defs=[['UI','Bấm nút','Button click'],['Ingame','Chọn đồ đúng','Bubble tap 2 (1)'],['Ingame','Tap bổ sung; trigger cần xác minh','Bubble tap 1'],['Ingame','Chạm không hợp lệ','tap_wrong'],['Ingame','Đồ rơi vào hộp','Item Drop Into Box'],['Ingame','Hộp xuất hiện','sfx_box_in'],['Ingame','Hộp đóng','box_close'],['Ingame','Hộp rời đi','Box Disappears'],['Ingame','Bắt đầu màn','Start level'],['Ingame','Kết màn','sfx_level_end'],['Ingame','Thắng','win_sfx'],['Ingame','Thua','lose_sfx'],['Booster','Dùng Broom','Broom booster'],['Booster','Dùng Vacuum','Vaccum booster'],['Hint','Gợi ý','sfx_hint'],['Economy','Nhận coin','coin_sfx'],['Shop','Mua hàng','purchase_sfx']];
const sh=initTable('SFX',['STT','Page','Mô tả','Tên File','Done'],defs.map((r,i)=>[i+1,...r,'']),[65,135,500,260,75]);put(sh,'A21',[['Lưu ý',get('SFX','Nhạc nền / âm còn thiếu')]]);sh.getRange('B21:D22').format.wrapText=true;sh.getRange('A21:E21').format.rowHeightPx=125;renders[renders.length-1]=['SFX','A1:E21'];
}

// ECONOMY: giữ ba cụm ngang No Ads / Booster / Win level và khối IAP phía dưới.
{
const sh=sheets.Economy;base(sh,'A1:L29');widths(sh,[28,130,130,200,160,24,180,160,165,160,170,185]);
put(sh,'B3',[['No Ads']]);header(sh,'B3:C3');put(sh,'D3',[['Mặc định giới thiệu từ level 6; lịch còn phụ thuộc điều kiện.']]);sh.getRange('B3:L3').format.rowHeightPx=65;
put(sh,'B4',[['Tên gói','No Ads'],['Số lần mua',1],['Giá tiền',7.99]]);sh.getRange('C6').setNumberFormat('"$"0.00');border(sh,'B3:C6');
put(sh,'G3',[['Booster','Value (Coin)','Ads for x1','Win level','Value (Coin)','Reward Ads']]);header(sh,'G3:L3');
put(sh,'G4',[['Vacuum','Chưa chốt',1,'Easy',20,'Chưa chốt'],['Broom','Chưa chốt',1,'Hard',40,'Chưa chốt'],['Extra Box','Chưa chốt','Chưa chốt','Super Hard',60,'Chưa chốt'],['Extra Slot','Chưa chốt','Chưa chốt','','','']]);border(sh,'G3:L7');sh.getRange('G4:G7').format.fill='#E69138';sh.getRange('I4:I5').format.fill='#FFFF00';sh.getRange('J4:K4').format.fill='#F4CCCC';sh.getRange('J5:K5').format.fill='#EAD1DC';sh.getRange('J6:K6').format.fill='#D5A6BD';
for(let row=4;row<=7;row++)sh.getRange(`G${row}:L${row}`).format.rowHeightPx=48;
put(sh,'G9',[['Thưởng cần xác nhận','Các số 20/40/60 là hằng số theo độ khó. WinPopup còn lưu 30/60. Chưa chốt giá trị thực nhận / hệ số quảng cáo.']]);sh.getRange('H9').format.columnWidthPx=240;sh.getRange('G9:L9').format.rowHeightPx=165;
put(sh,'B9',[['IAP Coin','Số coin','Giá mặc định (USD)']]);header(sh,'B9:D9');
const packs=[['coin1',500,1.99],['coin2',5000,7.99],['coin3',10000,14.99],['coin4',25000,29.99],['coin5',50000,49.99],['coin6',100000,99.99]];put(sh,'B10',packs);sh.getRange('C10:C15').setNumberFormat('#,##0');sh.getRange('D10:D15').setNumberFormat('"$"0.00');border(sh,'B9:D15');
put(sh,'G12',[['Tài nguyên','Giá trị','Đơn vị / ghi chú']]);header(sh,'G12:I12');put(sh,'G13',[['Coin ban đầu',600,'Preset code'],['Coin shop miễn phí',50,'Điều kiện / cooldown chưa chốt'],['Hồi sinh',800,'Coin, có nút Ads'],['Nạp tim',700,'Coin; lượng tim nhận chưa chốt'],['Hồi 1 tim',30,'Phút; số tim tối đa chưa chốt']]);border(sh,'G12:I17');sh.getRange('G13:I17').format.rowHeightPx=52;
put(sh,'B19',[['Ghi chú',get('Economy','Giá booster')],['Giá cửa hàng','Giá IAP trên là giá catalog đóng gói, có thể khác giá theo vùng / thời điểm. Phạm vi No Ads cần chơi xác nhận.']]);sh.getRange('B19:C20').format.rowHeightPx=160;
put(sh,'G19',[['Quảng cáo',get('Economy','Rewarded Ads')],['Interstitial / Banner',get('Economy','Interstitial / Banner')]]);sh.getRange('G19:H20').format.rowHeightPx=215;
renders.push(['Economy','A1:L20']);
}

{
const sh=sheets.Tutorial;base(sh,'A1:C21');widths(sh,[75,250,850]);
function block(row,title,steps){put(sh,`A${row}`,[[title]]);header(sh,`A${row}:C${row}`);put(sh,`A${row+1}`,[['Step','Trigger','Mô tả']]);header(sh,`A${row+1}:C${row+1}`);table(sh,row+2,steps,[75,250,850]);}
block(1,'Level 1',[[1,'Vừa vào Level 1','Hiển thị “Tap items that MATCH a box to tidy up!” và bàn tay chỉ item cần chọn.'],[2,'Giới thiệu hộp','Hiển thị “Check the category label!” và làm nổi bật nhãn nhóm trên hộp.'],[3,'Hướng dẫn kéo màn hình','Hiển thị “Swipe left to find the last one!” và bàn tay chỉ hướng kéo.']]);
block(8,'Level 3: Booster Vacuum tutorial',[[1,'Mở khóa Vacuum tại Level 3','Hiển thị “Fill a box instantly!” và bàn tay chỉ nút Vacuum.']]);
block(13,'Level 6: Booster Broom tutorial',[[1,'Mở khóa Broom tại Level 6','Đặt 3 item vào slot chờ. Hiển thị “Clear all waiting items!” và bàn tay chỉ nút Broom.']]);
block(18,'Extra Box: chưa xác nhận level',[[1,'Giới thiệu Extra Box','Hiển thị “Tap a locked box to add one more!” và bàn tay chỉ hộp khóa.']]);
for(const row of [6,11,16,21])sh.getRange(`A${row}:C${row}`).format.rowHeightPx=220;
for(const row of [7,12,17])sh.getRange(`A${row}:C${row}`).format.rowHeightPx=20;
await imageAt(sh,'Tutorial_core_Reference',5,1,800,210);
await imageAt(sh,'Tutorial_vacuum_Reference',10,1,800,210);
await imageAt(sh,'Tutorial_broom_Reference',15,1,800,210);
await imageAt(sh,'Tutorial_extra_Reference',20,1,800,210);
renders.push(['Tutorial','A1:C11'],['Tutorial','A13:C21']);
}

initTable('Haptic',['STT','Trigger','Mô tả','Thông số','Lưu ý'],[
[1,'Cài đặt Haptic',get('Haptic','Cài đặt'),'Bật / tắt',''],
[2,'Cảnh báo độ khó','Hai mốc rung cấu hình: 0,2 giây và 1,3 giây.','Hard: 150; Very Hard: 190; duration 300 ms','Preset scene, chưa đo trên thiết bị.'],
[3,'Các thao tác gameplay',get('Haptic','Điểm gọi rung'),'Chưa xác minh',get('Haptic','Các tình huống khác')]
],[60,200,430,280,360]);

{
const sh=sheets.UIUX;base(sh,'A1:D18');widths(sh,[65,220,720,300]);put(sh,'A1',[['MOCKUP UI']]);header(sh,'A1:D1');put(sh,'A2',[['','Mô tả màn hình và luồng tương tác. Ảnh tài nguyên gốc ở cuối sheet, không phải ảnh gameplay chạy trực tiếp.']]);sh.getRange('A2:D2').format.rowHeightPx=70;put(sh,'A3',[['STT','Màn hình / Luồng','Mô tả','Lưu ý']]);header(sh,'A3:D3');
const rows=byName.UIUX.rows.map((r,i)=>[i+1,r[0],r[1],r[2].includes('chưa')?'Cần chơi xác nhận':'']);table(sh,4,rows,[65,220,720,300]);await imageAt(sh,'asset-contact-sheet',19,1,1000,540);renders.push(['UIUX','A1:D17']);
}

{
const rows=byName['Nguồn & Xác minh'].rows.map(r=>[r[0],r[1]]);rows.unshift(['Phạm vi xác minh','Phân tích tĩnh APK 0.9, versionCode 9. Chưa chạy game. Các thông số chưa chốt được ghi trong nội dung. Không dùng cơ chế / giá Rotate Rings làm dữ liệu Happy Tidy Room.']);
initTable('Nguồn & Xác minh',['ID','Nguồn và ghi chú'],rows,[130,1150]);
}

// Dùng các ô gộp cho tiêu đề / ghi chú giống cấu trúc mẫu, để đoạn mô tả không bị ép vào một cột hẹp.
for(const row of [1,8,13,18])sheets.Tutorial.getRange(`A${row}:C${row}`).merge();
sheets.SFX.getRange('B21:E21').merge();
sheets.SFX.getRange('A21:E21').format.rowHeightPx=90;
sheets.UIUX.getRange('A1:D1').merge();
sheets.UIUX.getRange('B2:D2').merge();
{
const sh=sheets.Economy;
sh.getRange('B3:L3').format.rowHeightPx=65;
sh.getRange('B3:C3').merge();
sh.getRange('D3:E3').merge();
sh.getRange('H9:L9').merge();
sh.getRange('G9:L9').format.rowHeightPx=90;
for(const r of [19,20]){
 sh.getRange(`C${r}:E${r}`).merge();
 sh.getRange(`H${r}:L${r}`).merge();
 sh.getRange(`B${r}:L${r}`).format.rowHeightPx=145;
}
}
wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:2300})).ndjson);
const target=path.join(out,'[Tidy Room Sort] GDD.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(target);
await fs.mkdir(path.join(root,'analysis/revision-previews'),{recursive:true});
for(let i=0;i<renders.length;i++){
const [name,range]=renders[i];if(name!=='Tutorial')continue;const blob=await wb.render({sheetName:name,range,scale:1,format:'png'});await fs.writeFile(path.join(root,`analysis/revision-previews/tutorial-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
console.log('Saved original sheet format:',target);

