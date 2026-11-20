const {chromium}=require(process.env.PLAYWRIGHT_LIB||process.env.USERPROFILE+'/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const assert=require('node:assert/strict');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:1050}});const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  const base=process.argv[2]||'http://127.0.0.1:37846/';await page.goto(base);await page.getByText('Sẵn sàng. 130').waitFor();
  await page.locator('#count').fill('1');await page.locator('#seed').fill('92731');await page.locator('#exclusion').uncheck();await page.locator('#room').selectOption('bedroom');
  await page.locator('#templateMode').click();await page.locator('#moveAnchor').click();await page.locator('#canvas').click({position:{x:215,y:340}});
  await page.getByText('Đã dời điểm vắt.',{exact:false}).waitFor();
  await page.locator('#drawZone').click();await page.locator('#zoneName').fill('Góc thử');
  for(const [x,y] of [[90,410],[160,428],[100,482]])await page.locator('#canvas').click({position:{x,y}});
  await page.locator('#saveZone').click();await page.getByText('Đã thêm vùng.',{exact:false}).waitFor();
  await page.locator('summary').click();assert.ok((await page.locator('#template').inputValue()).includes('Góc thử'));
  await page.locator('#reset').click();await page.getByText('Đã khôi phục nền mẫu.').waitFor();
  await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(__dirname,'template-preview.png'),fullPage:true});
  await page.locator('#startJob').click();await page.getByText('Hoàn tất: 1/1 màn đạt.',{exact:false}).waitFor({timeout:45000});
  await page.getByText('Tải level JSON').waitFor();await page.locator('#stepNext').click();await page.getByText('1/26 lần lấy').waitFor();
  assert.match(await page.locator('#metrics').innerText(),/26 \/ 5 \/ 5/);
  await page.locator('#resetSteps').click();await page.getByText('0/26 lần lấy').waitFor();
  await page.locator('#play').click();await page.locator('#hud').getByText('Khay 0/5',{exact:true}).waitFor();
  const href=await page.getByText('Lời giải + thông số').getAttribute('href');
  const content=(await (await page.request.get(new URL(href,base).href)).json()).records[0];
  const {Game}=await import('./core/game.js');const shapes=(await (await page.request.get(new URL('data/art.json',base).href)).json()).items;const game=new Game(content.level,shapes);
  for(const uid of content.path){const it=game.items.find(x=>x.uid===uid),b=it.aabb;let found;
    for(let i=0;i<121;i++){const x=b.minX+(b.maxX-b.minX)*((i%11)+.5)/11,y=b.minY+(b.maxY-b.minY)*(Math.floor(i/11)+.5)/11;if(game.pickAt(x,y)===uid){found=[x,y];break;}}assert.ok(found);
    const box=await page.locator('#canvas').boundingBox();await page.locator('#canvas').click({position:{x:(.5+found[0]/content.level.width)*box.width,y:(.5-found[1]/content.level.height)*box.height}});game.tapAt(...found);
  }
  await page.getByText('Đã dọn sạch!',{exact:true}).waitFor();await page.locator('#play').click();
  await page.locator('summary').click();await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(__dirname,'studio-preview.png'),fullPage:true});
  await page.locator('#start').fill('3');await page.locator('#count').fill('8');await page.locator('#seed').fill('92732');await page.locator('#startJob').click();await page.locator('#stop').click();await page.getByText('Đã dừng:',{exact:false}).waitFor({timeout:60000});
  assert.deepEqual(errors,[]);console.log('PASS: launch, draw, add zone, move and restore anchor, generate, download availability, replay step, interactive pointer win, cancel.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
