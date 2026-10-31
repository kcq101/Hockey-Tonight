const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage({viewport:{width:900,height:900}}); pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.goto('http://localhost:8811/fight.html'); await pg.waitForFunction('window.ready',{timeout:60000});
await pg.evaluate('window.DIST=0.85');
const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const out=process.argv[3]; fs.mkdirSync(out,{recursive:true}); const meta={};
for(const j of jobs){ const o=await pg.evaluate(([a,t,g])=>shot(a,t,{grab:g}),[j.anim,j.t,j.grab]);
  fs.writeFileSync(`${out}/${j.name}.png`,Buffer.from(o.img.split(',')[1],'base64')); meta[j.name]={anchor:o.anchor,hand:o.hand,head:o.head}; }
fs.writeFileSync(`${out}/meta.json`,JSON.stringify(meta)); await b.close(); console.log('done',jobs.length);})();
