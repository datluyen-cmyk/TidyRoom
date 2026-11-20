import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const root = 'D:/APK Works/HappyTidyRoom';
const outputDir = path.join(root, 'outputs/happy-tidy-room-gdd');
const data = JSON.parse(await fs.readFile(path.join(root,'analysis/gdd-content.json'),'utf8'));
const wb = Workbook.create();
const palette = {text:'#24313A', title:'#254F62', rule:'#B9C9CE', header:'#315A6A', light:'#F1F5F6', muted:'#67747B'};

function lines(text, chars) {
  return String(text).split('\n').reduce((sum, s)=> {
    let n=1,len=0;
    for(const word of s.split(/\s+/)){ if(len+word.length+1>chars){n++;len=word.length;}else len+=word.length+1; }
    return sum+n;
  },0);
}

for(const spec of data.sheets) {
  const sh=wb.worksheets.add(spec.name);
  sh.showGridLines=false;
  const end=spec.rows.length+4;
  const area=sh.getRange(`B2:E${end}`);
  area.format.font={name:'Arial',size:11,color:palette.text};
  area.format.verticalAlignment='top';
  sh.getRange(`A1:A${end}`).format.columnWidthPx=22;
  sh.getRange(`B2:B${end}`).format.columnWidthPx=210;
  sh.getRange(`C2:C${end}`).format.columnWidthPx=680;
  sh.getRange(`D2:D${end}`).format.columnWidthPx=174;
  sh.getRange(`E2:E${end}`).format.columnWidthPx=110;
  sh.getRange('B2').values=[[spec.title]];
  sh.getRange('B2').format.font={name:'Arial',size:16,bold:true,color:palette.title};
  sh.getRange('B2:E2').format.rowHeightPx=34;
  sh.getRange('B3:E3').format.borders={bottom:{style:'thin',color:palette.rule}};
  sh.getRange('B3:E3').format.rowHeightPx=10;
  const heads=sh.getRange('B4:E4');
  heads.values=[['Hạng mục','Mô tả thiết kế','Mức xác minh','Nguồn']];
  heads.format.fill=palette.header;
  heads.format.font={name:'Arial',size:11,bold:true,color:'#FFFFFF'};
  heads.format.rowHeightPx=30;
  heads.format.horizontalAlignment='center';
  heads.format.verticalAlignment='center';
  sh.getRange(`B5:E${end}`).values=spec.rows;
  sh.getRange(`B5:E${end}`).format.wrapText=true;
  for(let i=0;i<spec.rows.length;i++) {
    const row=i+5;
    const values=spec.rows[i];
    const height=Math.max(64, Math.max(lines(values[0],24),lines(values[1],85),lines(values[2],19),lines(values[3],12))*18+20);
    sh.getRange(`B${row}:E${row}`).format.rowHeightPx=height;
    if(i%2===1) sh.getRange(`B${row}:E${row}`).format.fill=palette.light;
    sh.getRange(`B${row}`).format.font={name:'Arial',size:11,bold:true,color:palette.text};
    sh.getRange(`D${row}:E${row}`).format.font={name:'Arial',size:11,color:palette.muted};
  }
  if(spec.name==='Overview') sh.tabColor=palette.title;
  if(spec.name==='Nguồn & Xác minh') sh.tabColor='#A7B2B6';
  if(spec.rows.length>8) sh.freezePanes.freezeRows(4);
  if(spec.name==='Đồ vật & Hộp') {
    const img = await fs.readFile(path.join(root,'analysis/visuals/asset-contact-sheet.png'));
    sh.images.add({dataUrl:`data:image/png;base64,${img.toString('base64')}`,anchor:{from:{row:end+2,col:1},extent:{widthPx:1000,heightPx:540}}});
    sh.getRange(`B${end+2}`).values=[['Ví dụ tài nguyên trích từ APK. Không phải ảnh gameplay đang chạy.']];
    sh.getRange(`B${end+2}`).format.font={name:'Arial',size:11,italic:true,color:palette.muted};
  }
}
wb.recalculate();
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:3000})).ndjson);
console.log((await wb.inspect({kind:'table',range:"Booster!B5:E12",tableMaxRows:2,tableMaxCols:4,maxChars:1500})).ndjson);
const xlsx=await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(path.join(outputDir,'Happy Tidy Room - GDD.xlsx'));
await fs.mkdir(path.join(root,'analysis/previews'),{recursive:true});
for(let i=0;i<data.sheets.length;i++){
  const spec=data.sheets[i];
  const blob=await wb.render({sheetName:spec.name,range:`B2:E${spec.rows.length+4}`,scale:1,format:'png'});
  await fs.writeFile(path.join(root,`analysis/previews/${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
  console.log('Rendered',spec.name);
}
console.log('Saved workbook',path.join(outputDir,'Happy Tidy Room - GDD.xlsx'));
