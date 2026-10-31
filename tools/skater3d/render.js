const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const pg=await b.newPage({viewport:{width:1100,height:1100}}); pg.on('pageerror',e=>console.log('ERR',e.message)); pg.on('console',m=>{if(m.type()==='error')console.log('C',m.text())});
await pg.goto('http://localhost:8810/pose2.html'); await pg.waitForFunction('window.ready',{timeout:60000});
const dirs={S:0,SE:Math.PI/4,E:Math.PI/2,NE:3*Math.PI/4,N:Math.PI};
const meta={}; fs.mkdirSync('fr3d',{recursive:true});
const jobs=JSON.parse(process.argv[2]);
for(const j of jobs){ const o=await pg.evaluate(([p,y,u,l,w])=>window.shot({phi:p,yaw:y,u,lean:l,low:w}),[j.phi,dirs[j.dir],j.u,j.lean,j.low]);
  fs.writeFileSync(`fr3d/${j.name}.png`,Buffer.from(o.img.split(',')[1],'base64')); meta[j.name]={anchor:o.anchor,puck:o.puck}; }
fs.writeFileSync('fr3d/meta.json',JSON.stringify(meta)); await b.close();})();
