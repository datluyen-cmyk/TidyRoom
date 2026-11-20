import fs from 'node:fs/promises';
import {Workbook,SpreadsheetFile,FileBlob} from '@oai/artifact-tool';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load('D:/[Rotate Rings] GDD.xlsx'));
for(const name of ['Overview','Ring Object','Booster','Economy']){
const blob=await wb.render({sheetName:name,range:name==='Economy'?'A1:L9':name==='Overview'?'A1:B13':name==='Booster'?'A1:H4':'A1:F5',scale:1,format:'png'});await fs.writeFile(`D:/APK Works/HappyTidyRoom/analysis/previews/ref-${name}.png`,new Uint8Array(await blob.arrayBuffer()));}
console.log((await wb.inspect({kind:'computedStyle',sheetId:'Booster',range:'A1:H2',maxChars:2000})).ndjson);
