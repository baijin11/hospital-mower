import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# === 1. 替换 drawDecorations 为更丰富的版本 ===
old_dec = '''function drawDecorations(cx,cy,lv){
  ctx.save();
  // hospital signs along walls
  ctx.font='bold 14px sans-serif';ctx.textAlign='center';
  let signs=['放射科','CT室','MRI室','超声科','挂号处','药房','检验科','急诊','门诊','住院部'];
  ctx.fillStyle='rgba(0,0,0,0.1)';
  for(let i=0;i<10;i++){
    let sx=i*300+150-cx,sy=30-cy;
    if(sx>-50&&sx<canvas.width+50&&sy>-50&&sy<canvas.height+50){
      ctx.fillRect(sx-35,sy-10,70,20);ctx.strokeStyle='rgba(0,0,0,0.1)';ctx.strokeRect(sx-35,sy-10,70,20);
      ctx.fillStyle='rgba(0,0,0,0.2)';ctx.fillText(signs[i],sx,sy+4);ctx.fillStyle='rgba(0,0,0,0.1)';
    }
  }
  // floor tiles pattern
  ctx.fillStyle=lv.gridColor;ctx.globalAlpha=0.15;
  for(let x=0;x<G.mapSize;x+=200){
    for(let y=0;y<G.mapSize;y+=200){
      let dx=x-cx,dy=y-cy;
      if(dx>-10&&dx<canvas.width+10&&dy>-10&&dy<canvas.height+10){
        ctx.fillRect(dx-1,dy-1,2,2);
      }
    }
  }
  ctx.globalAlpha=1;
  ctx.restore();
}'''

new_dec = '''function drawDecorations(cx,cy,lv){
  ctx.save();
  // Hospital signs along walls
  ctx.font='bold 13px Microsoft YaHei,sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';
  let signs=['放射科','CT室','MRI室','超声科','挂号处','药房','检验科','急诊','门诊','住院部'];
  for(let i=0;i<10;i++){
    let sx=i*320+160-cx,sy=30-cy;
    if(sx>-50&&sx<canvas.width+50&&sy>-50&&sy<canvas.height+50){
      ctx.fillStyle='rgba(255,255,255,0.9)';
      ctx.strokeStyle=lv.accent+'88';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.roundRect(sx-38,sy-13,76,26,5);ctx.fill();ctx.stroke();
      ctx.fillStyle=lv.accent;ctx.fillText(signs[i],sx,sy+1);
    }
  }
  // Bottom wall signs
  for(let i=0;i<10;i++){
    let sx=i*320+160-cx,sy=lv.mapSize-30-cy;
    if(sx>-50&&sx<canvas.width+50&&sy>-50&&sy<canvas.height+50){
      ctx.fillStyle='rgba(255,255,255,0.9)';
      ctx.strokeStyle=lv.accent+'88';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.roundRect(sx-38,sy-13,76,26,5);ctx.fill();ctx.stroke();
      ctx.fillStyle=lv.accent;ctx.fillText(signs[i],sx,sy+1);
    }
  }
  // Left wall signs
  let vsigns=['ICU','NICU','B超室','VIP','抢救室'];
  for(let i=0;i<vsigns.length;i++){
    let sx=30-cx,sy=i*400+200-cy;
    if(sx>-50&&sx<canvas.width+50&&sy>-50&&sy<canvas.height+50){
      ctx.fillStyle='rgba(255,255,255,0.9)';
      ctx.strokeStyle=lv.accent+'88';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.roundRect(sx-24,sy-14,48,28,4);ctx.fill();ctx.stroke();
      ctx.fillStyle=lv.accent;ctx.fillText(vsigns[i],sx,sy+1);
    }
  }
  // Floor objects (deterministic)
  for(let x=100;x<G.mapSize;x+=250){
    for(let y=100;y<G.mapSize;y+=250){
      let dx=x-cx,dy=y-cy;
      if(dx<-40||dx>canvas.width+40||dy<-40||dy>canvas.height+40)continue;
      let seed=Math.abs(Math.sin(x*0.0031)*99999+Math.cos(y*0.0031)*99999)%5;
      ctx.globalAlpha=0.5;
      drawFloorObj(dx,dy,seed);
      ctx.globalAlpha=1;
    }
  }
  ctx.restore();
}

function drawFloorObj(x,y,seed){
  ctx.save();ctx.translate(x,y);
  ctx.strokeStyle='rgba(0,0,0,0.12)';ctx.fillStyle='rgba(0,0,0,0.08)';ctx.lineWidth=1.5;
  if(seed<1){
    ctx.fillRect(-8,-5,16,4);ctx.strokeRect(-8,-5,16,4);
    ctx.fillRect(-8,0,3,9);ctx.fillRect(5,0,3,9);ctx.fillRect(-8,9,16,2);
  }else if(seed<2){
    ctx.fillRect(-14,-7,28,14);ctx.strokeRect(-14,-7,28,14);
    ctx.fillStyle='rgba(255,255,255,0.1)';ctx.fillRect(-13,-6,26,4);
  }else if(seed<3){
    ctx.strokeStyle='#888';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(0,-18);ctx.lineTo(0,6);ctx.stroke();
    ctx.fillStyle='#4488ff';ctx.fillRect(-4,-22,8,6);
    ctx.beginPath();ctx.moveTo(-7,0);ctx.lineTo(7,0);ctx.stroke();
  }else if(seed<4){
    ctx.fillStyle='#666';
    ctx.beginPath();ctx.moveTo(-5,6);ctx.lineTo(-4,-5);ctx.lineTo(4,-5);ctx.lineTo(5,6);ctx.closePath();ctx.fill();
  }else{
    ctx.strokeStyle='rgba(0,0,0,0.05)';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(0,-5);ctx.lineTo(0,5);ctx.moveTo(-5,0);ctx.lineTo(5,0);ctx.stroke();
  }
  ctx.restore();
}'''

if old_dec in c:
    c = c.replace(old_dec, new_dec)
    print('drawDecorations replaced')
else:
    print('drawDecorations NOT found - trying regex')
    # fallback
    pat = r'function drawDecorations\(cx,cy,lv\)\{.*?ctx\.restore\(\);\n\}'
    m = re.search(pat, c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_dec + c[m.end():]
        print('drawDecorations replaced via regex')

# === 2. Replace drawPatient ===
old_draw = '''function drawPatient(c,x,y,size,color,type){
  c.save();c.translate(x,y);
  // body
  c.fillStyle=color;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  // face
  c.fillStyle='#fff';c.beginPath();c.arc(-size*0.25,-size*0.15,size*0.18,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.25,-size*0.15,size*0.18,0,Math.PI*2);c.fill();
  c.fillStyle='#333';
  c.beginPath();c.arc(-size*0.22,-size*0.12,size*0.08,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.28,-size*0.12,size*0.08,0,Math.PI*2);c.fill();
  // mouth
  if(type==='angry'){
    c.strokeStyle='#333';c.lineWidth=1.5;c.beginPath();
    c.arc(0,size*0.25,size*0.25,0.2,Math.PI-0.2);c.stroke();
    // angry brows
    c.lineWidth=2;c.beginPath();c.moveTo(-size*0.4,-size*0.35);c.lineTo(-size*0.1,-size*0.25);c.stroke();
    c.beginPath();c.moveTo(size*0.4,-size*0.35);c.lineTo(size*0.1,-size*0.25);c.stroke();
    // phone
    c.fillStyle='#333';c.fillRect(size*0.6,-size*0.3,size*0.25,size*0.4);
    c.fillStyle='#666';c.fillRect(size*0.63,-size*0.22,size*0.19,size*0.25);
  }else if(type==='fast'){
    c.strokeStyle='#333';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.2,size*0.2,0,Math.PI);c.stroke();
  }else if(type==='family'){
    c.strokeStyle='#333';c.lineWidth=1;c.beginPath();c.arc(0,size*0.2,size*0.15,0,Math.PI);c.stroke();
    // extra person
    c.fillStyle=color;c.globalAlpha=0.5;c.beginPath();c.arc(-size*0.5,size*0.3,size*0.5,0,Math.PI*2);c.fill();
    c.globalAlpha=1;
  }else if(type==='admin'){
    // tie
    c.fillStyle='#c0392b';c.beginPath();c.moveTo(0,-size*0.1);c.lineTo(-size*0.1,size*0.4);c.lineTo(0,size*0.3);c.lineTo(size*0.1,size*0.4);c.closePath();c.fill();
    c.strokeStyle='#333';c.lineWidth=1.5;c.beginPath();c.moveTo(-size*0.15,size*0.2);c.lineTo(size*0.15,size*0.2);c.stroke();
  }else{
    c.strokeStyle='#333';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.2,size*0.15,0,Math.PI);c.stroke();
  }
  // outline
  c.strokeStyle='rgba(0,0,0,0.3)';c.lineWidth=1.5;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  c.restore();
}'''

new_draw = '''function drawPatient(c,x,y,size,color,type,el){
  c.save();c.translate(x,y);
  let anim=Date.now()/180;
  // shadow
  c.fillStyle='rgba(0,0,0,0.18)';c.beginPath();c.ellipse(0,size*0.72,size*0.9,size*0.22,0,0,Math.PI*2);c.fill();
  // elite glow
  if(el){c.shadowColor='#f39c12';c.shadowBlur=12+Math.sin(anim*2)*4}
  // body with gradient
  let bg=c.createRadialGradient(-size*0.15,-size*0.15,size*0.05,0,0,size);
  bg.addColorStop(0,'rgba(255,255,255,0.6)');bg.addColorStop(0.55,color);bg.addColorStop(1,'rgba(0,0,0,0.35)');
  c.fillStyle=bg;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  c.shadowBlur=0;
  // outline
  c.strokeStyle='rgba(0,0,0,0.2)';c.lineWidth=1.5;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  // hospital gown detail
  c.fillStyle='rgba(255,255,255,0.1)';c.beginPath();c.arc(0,size*0.05,size*0.65,Math.PI,0);c.fill();
  // face
  c.fillStyle='#ffe0c0';c.beginPath();c.arc(0,-size*0.12,size*0.38,0,Math.PI*2);c.fill();
  let eOff=size*0.14;
  if(type==='angry'){
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.fillStyle='#cc0000';
    c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.strokeStyle='#993300';c.lineWidth=2;
    c.beginPath();c.moveTo(-eOff-size*0.12,-size*0.28);c.lineTo(-eOff+size*0.08,-size*0.2);c.stroke();
    c.beginPath();c.moveTo(eOff+size*0.12,-size*0.28);c.lineTo(eOff-size*0.08,-size*0.2);c.stroke();
    c.beginPath();c.arc(0,size*0.2,size*0.15,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
    c.fillStyle='#1a1a2e';c.fillRect(size*0.5,-size*0.28,size*0.25,size*0.38);
    c.fillStyle='#4488ff';c.fillRect(size*0.53,-size*0.21,size*0.19,size*0.23);
  }else if(type==='fast'){
    c.fillStyle='#333';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.strokeStyle='#bb8866';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.18,size*0.12,Math.PI+0.2,Math.PI*2-0.2);c.stroke();
    // speed lines
    c.strokeStyle='rgba(231,76,60,0.3)';c.lineWidth=1;
    for(let i=0;i<3;i++){c.beginPath();c.moveTo(-size*1.1,-size*0.3+i*size*0.3);c.lineTo(-size*0.7,-size*0.3+i*size*0.3);c.stroke()}
  }else if(type==='family'){
    c.fillStyle='#333';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.strokeStyle='#bb8866';c.lineWidth=1;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
    // extra person behind
    c.fillStyle=color;c.globalAlpha=0.4;c.beginPath();c.arc(-size*0.45,size*0.3,size*0.5,0,Math.PI*2);c.fill();c.globalAlpha=1;
  }else if(type==='admin'){
    c.fillStyle='#333';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    // tie
    c.fillStyle='#c0392b';c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(-size*0.08,size*0.35);c.lineTo(0,size*0.25);c.lineTo(size*0.08,size*0.35);c.closePath();c.fill();
    // suit line
    c.strokeStyle='rgba(0,0,0,0.2)';c.lineWidth=1;c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(0,size*0.3);c.stroke();
    // glasses
    c.strokeStyle='#222';c.lineWidth=1.5;c.beginPath();c.arc(-eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.moveTo(-eOff+size*0.1,-size*0.14);c.lineTo(eOff-size*0.1,-size*0.14);c.stroke();
    // frown
    c.strokeStyle='#555';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.22,size*0.1,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
  }else{
    c.fillStyle='#333';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.strokeStyle='#bb8866';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
  }
  c.restore();
}'''

if old_draw in c:
    c = c.replace(old_draw, new_draw)
    print('drawPatient replaced')
else:
    print('drawPatient NOT found - trying regex')
    pat = r'function drawPatient\(c,x,y,size,color,type\)\{.*?c\.restore\(\);\n\}'
    m = re.search(pat, c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_draw + c[m.end():]
        print('drawPatient replaced via regex')

# === 3. Replace drawBoss ===
old_boss = '''function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){
  c.save();c.translate(x,y);
  // glow
  if(raging){
    c.shadowColor='#e74c3c';c.shadowBlur=25;
  }
  // body
  let grad=c.createRadialGradient(0,0,size*0.3,0,0,size);
  grad.addColorStop(0,color);grad.addColorStop(1,'#333');
  c.fillStyle=grad;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  c.shadowBlur=0;
  // face
  c.fillStyle='#fff';c.beginPath();c.arc(-size*0.22,-size*0.15,size*0.16,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.22,-size*0.15,size*0.16,0,Math.PI*2);c.fill();
  c.fillStyle='#e74c3c';
  c.beginPath();c.arc(-size*0.19,-size*0.12,size*0.07,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.25,-size*0.12,size*0.07,0,Math.PI*2);c.fill();
  // angry mouth
  c.fillStyle='#c0392b';c.beginPath();c.arc(0,size*0.15,size*0.2,0,Math.PI);c.fill();
  c.fillStyle='#fff';c.fillRect(-size*0.12,size*0.15,size*0.24,size*0.06);
  // angry brows
  c.strokeStyle='#c0392b';c.lineWidth=3;
  c.beginPath();c.moveTo(-size*0.4,-size*0.35);c.lineTo(-size*0.05,-size*0.22);c.stroke();
  c.beginPath();c.moveTo(size*0.4,-size*0.35);c.lineTo(size*0.05,-size*0.22);c.stroke();
  // phone
  c.fillStyle='#333';c.fillRect(size*0.5,-size*0.4,size*0.3,size*0.5);
  c.fillStyle='#4488ff';c.fillRect(size*0.53,-size*0.32,size*0.24,size*0.3);
  // shield
  if(shielded){
    c.strokeStyle='rgba(68,136,255,0.6)';c.lineWidth=3;
    c.beginPath();c.arc(0,0,size+6,0,Math.PI*2);c.stroke();
  }
  // name tag
  c.fillStyle='rgba(0,0,0,0.7)';
  let tw=c.measureText(bossName).width+16;
  c.fillRect(-tw/2,-size-22,tw,18);
  c.fillStyle='#ff6b6b';c.font='bold 11px sans-serif';c.textAlign='center';
  c.fillText(bossName,0,-size-8);
  // hp bar
  let bw=size*2,bh=6;
  c.fillStyle='#333';c.fillRect(-bw/2,size+8,bw,bh);
  c.fillStyle='#e74c3c';c.fillRect(-bw/2,size+8,bw*(hp/maxHp),bh);
  c.strokeStyle='#888';c.lineWidth=1;c.strokeRect(-bw/2,size+8,bw,bh);
  c.restore();
}'''

new_boss = '''function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){
  c.save();c.translate(x,y);
  let anim=Date.now()/150;
  // outer aura ring (pulsing)
  let auraR=size+15+Math.sin(anim*2)*5;
  c.strokeStyle=raging?'rgba(255,0,0,0.3)':'rgba(255,68,68,0.2)';
  c.lineWidth=3;c.beginPath();c.arc(0,0,auraR,0,Math.PI*2);c.stroke();
  // second aura
  c.strokeStyle=raging?'rgba(255,0,0,0.15)':'rgba(255,100,100,0.1)';
  c.lineWidth=2;c.beginPath();c.arc(0,0,auraR+8+Math.sin(anim*3)*3,0,Math.PI*2);c.stroke();
  // shadow
  c.fillStyle='rgba(0,0,0,0.25)';c.beginPath();c.ellipse(0,size*0.8,size*1.1,size*0.3,0,0,Math.PI*2);c.fill();
  // glow
  if(raging){c.shadowColor='#ff0000';c.shadowBlur=35+Math.sin(anim*4)*10}
  else{c.shadowColor='#ff4444';c.shadowBlur=20}
  // body with gradient
  let grad=c.createRadialGradient(-size*0.2,-size*0.2,size*0.1,0,0,size);
  grad.addColorStop(0,raging?'#ff6666':'#ff8888');grad.addColorStop(0.5,color);grad.addColorStop(1,'#1a0000');
  c.fillStyle=grad;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  c.shadowBlur=0;
  // body outline
  c.strokeStyle='rgba(0,0,0,0.3)';c.lineWidth=2;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  // face
  c.fillStyle='#ffe0c0';c.beginPath();c.arc(0,-size*0.1,size*0.5,0,Math.PI*2);c.fill();
  // angry eyes
  c.fillStyle='#fff';c.beginPath();c.arc(-size*0.18,-size*0.18,size*0.13,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.18,-size*0.18,size*0.13,0,Math.PI*2);c.fill();
  c.fillStyle=raging?'#ff0000':'#cc0000';
  c.beginPath();c.arc(-size*0.16,-size*0.16,size*0.07,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.2,-size*0.16,size*0.07,0,Math.PI*2);c.fill();
  // angry brows
  c.strokeStyle=raging?'#ff0000':'#cc0000';c.lineWidth=3.5;
  c.beginPath();c.moveTo(-size*0.35,-size*0.38);c.lineTo(-size*0.05,-size*0.24);c.stroke();
  c.beginPath();c.moveTo(size*0.35,-size*0.38);c.lineTo(size*0.05,-size*0.24);c.stroke();
  // angry mouth (teeth)
  c.fillStyle='#880000';c.beginPath();c.arc(0,size*0.12,size*0.18,0,Math.PI);c.fill();
  c.fillStyle='#fff';
  for(let i=-2;i<=2;i++){c.fillRect(i*size*0.07-2,size*0.12,4,size*0.06)}
  // phone
  c.fillStyle='#1a1a2e';c.fillRect(size*0.55,-size*0.4,size*0.3,size*0.48);
  c.fillStyle='#4488ff';c.fillRect(size*0.58,-size*0.33,size*0.24,size*0.3);
  // shield effect
  if(shielded){
    c.strokeStyle='rgba(68,136,255,'+(0.5+Math.sin(anim*5)*0.2)+')';c.lineWidth=4;
    c.beginPath();c.arc(0,0,size+8,0,Math.PI*2);c.stroke();
    c.fillStyle='rgba(68,136,255,0.1)';c.beginPath();c.arc(0,0,size+8,0,Math.PI*2);c.fill();
  }
  // name tag (beautified)
  c.font='bold 12px Microsoft YaHei,sans-serif';c.textAlign='center';
  let tw=c.measureText(bossName).width+20;
  c.fillStyle='rgba(0,0,0,0.8)';
  c.beginPath();c.roundRect(-tw/2,-size-25,tw,20,5);c.fill();
  c.strokeStyle='rgba(255,68,68,0.5)';c.lineWidth=1;c.beginPath();c.roundRect(-tw/2,-size-25,tw,20,5);c.stroke();
  c.fillStyle='#ff6b6b';c.fillText(bossName,0,-size-10);
  // hp bar
  let bw=size*2.2,bh=7;
  c.fillStyle='rgba(0,0,0,0.6)';c.beginPath();c.roundRect(-bw/2,size+10,bw,bh,3);c.fill();
  let hpFill=bw*(hp/maxHp);
  c.fillStyle=hp/maxHp>0.5?'#e74c3c':hp/maxHp>0.25?'#ff8800':'#ff0000';
  c.shadowColor=c.fillStyle;c.shadowBlur=5;
  c.beginPath();c.roundRect(-bw/2,size+10,Math.max(0,hpFill),bh,3);c.fill();
  c.shadowBlur=0;
  c.restore();
}'''

if old_boss in c:
    c = c.replace(old_boss, new_boss)
    print('drawBoss replaced')
else:
    print('drawBoss NOT found - trying regex')
    pat = r'function drawBoss\(c,x,y,size,bossName,hp,maxHp,color,shielded,raging\)\{.*?c\.restore\(\);\n\}'
    m = re.search(pat, c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_boss + c[m.end():]
        print('drawBoss replaced via regex')

# === 4. Replace drawPlayer ===
old_player = '''function drawPlayer(c,x,y,size,hp,maxHp,invincible){
  c.save();c.translate(x,y);
  if(invincible&&Math.floor(Date.now()/80)%2===0){c.globalAlpha=0.4}
  // shadow
  c.fillStyle='rgba(0,0,0,0.2)';c.beginPath();c.ellipse(0,size*0.7,size*0.8,size*0.3,0,0,Math.PI*2);c.fill();
  // body (white coat)
  c.fillStyle='#ecf0f1';c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  // coat details
  c.fillStyle='#bdc3c7';c.beginPath();c.moveTo(-2,-size);c.lineTo(2,-size);c.lineTo(2,size);c.lineTo(-2,size);c.closePath();c.fill();
  // green cap
  c.fillStyle='#27ae60';c.beginPath();c.arc(0,-size*0.2,size*0.7,Math.PI,0);c.fill();
  // face
  c.fillStyle='#fad7a0';c.beginPath();c.arc(0,size*0.1,size*0.5,0,Math.PI*2);c.fill();
  // glasses
  c.strokeStyle='#333';c.lineWidth=1.5;
  c.beginPath();c.arc(-size*0.15,size*0.05,size*0.12,0,Math.PI*2);c.stroke();
  c.beginPath();c.arc(size*0.15,size*0.05,size*0.12,0,Math.PI*2);c.stroke();
  c.beginPath();c.moveTo(-size*0.03,size*0.05);c.lineTo(size*0.03,size*0.05);c.stroke();
  // eyes
  c.fillStyle='#333';
  c.beginPath();c.arc(-size*0.15,size*0.05,size*0.04,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.15,size*0.05,size*0.04,0,Math.PI*2);c.fill();
  // mouth
  c.strokeStyle='#333';c.lineWidth=1;c.beginPath();c.arc(0,size*0.2,size*0.1,0.2,Math.PI-0.2);c.stroke();
  // stethoscope
  c.strokeStyle='#3498db';c.lineWidth=2;
  c.beginPath();c.arc(size*0.3,size*0.3,size*0.15,0,Math.PI);c.stroke();
  // outline
  c.strokeStyle='#2c3e50';c.lineWidth=2;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  // glow
  c.shadowColor='#3498db';c.shadowBlur=12;
  c.strokeStyle='rgba(52,152,219,0.3)';c.lineWidth=2;c.beginPath();c.arc(0,0,size+2,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;
  c.globalAlpha=1;
  c.restore();
}'''

new_player = '''function drawPlayer(c,x,y,size,hp,maxHp,invincible){
  c.save();c.translate(x,y);
  let anim=Date.now()/200;
  if(invincible&&Math.floor(Date.now()/80)%2===0){c.globalAlpha=0.4}
  // shadow
  c.fillStyle='rgba(0,0,0,0.22)';c.beginPath();c.ellipse(0,size*0.75,size*0.9,size*0.28,0,0,Math.PI*2);c.fill();
  // white coat body with gradient
  let bodyG=c.createRadialGradient(-size*0.2,-size*0.2,size*0.05,0,0,size);
  bodyG.addColorStop(0,'#ffffff');bodyG.addColorStop(0.6,'#ecf0f1');bodyG.addColorStop(1,'#bdc3c7');
  c.fillStyle=bodyG;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  // coat center line
  c.fillStyle='#d5d8dc';c.beginPath();c.moveTo(-2,-size*0.9);c.lineTo(2,-size*0.9);c.lineTo(2,size*0.9);c.lineTo(-2,size*0.9);c.closePath();c.fill();
  // coat lapels
  c.fillStyle='#bdc3c7';
  c.beginPath();c.moveTo(-size*0.4,-size*0.3);c.lineTo(-2,size*0.2);c.lineTo(-size*0.5,size*0.4);c.closePath();c.fill();
  c.beginPath();c.moveTo(size*0.4,-size*0.3);c.lineTo(2,size*0.2);c.lineTo(size*0.5,size*0.4);c.closePath();c.fill();
  // green surgical cap
  c.fillStyle='#27ae60';c.beginPath();c.arc(0,-size*0.15,size*0.72,Math.PI,0);c.fill();
  c.fillStyle='#2ecc71';c.beginPath();c.arc(0,-size*0.15,size*0.65,Math.PI,0);c.fill();
  // cap band
  c.fillStyle='#1e8449';c.fillRect(-size*0.65,-size*0.18,size*1.3,size*0.08);
  // face
  c.fillStyle='#fad7a0';c.beginPath();c.arc(0,size*0.1,size*0.45,0,Math.PI*2);c.fill();
  // glasses
  c.strokeStyle='#2c3e50';c.lineWidth=2;
  c.beginPath();c.arc(-size*0.16,size*0.05,size*0.13,0,Math.PI*2);c.stroke();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.13,0,Math.PI*2);c.stroke();
  c.beginPath();c.moveTo(-size*0.03,size*0.05);c.lineTo(size*0.03,size*0.05);c.stroke();
  // glasses lens tint
  c.fillStyle='rgba(100,180,255,0.12)';
  c.beginPath();c.arc(-size*0.16,size*0.05,size*0.11,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.11,0,Math.PI*2);c.fill();
  // eyes
  c.fillStyle='#2c3e50';
  c.beginPath();c.arc(-size*0.16,size*0.05,size*0.04,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.04,0,Math.PI*2);c.fill();
  // eye shine
  c.fillStyle='#fff';
  c.beginPath();c.arc(-size*0.14,size*0.03,size*0.018,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.18,size*0.03,size*0.018,0,Math.PI*2);c.fill();
  // mouth (slight smile)
  c.strokeStyle='#a0522d';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.2,size*0.1,0.2,Math.PI-0.2);c.stroke();
  // stethoscope
  c.strokeStyle='#2c3e50';c.lineWidth=2.5;
  c.beginPath();c.moveTo(-size*0.2,-size*0.05);c.quadraticCurveTo(-size*0.4,size*0.3,-size*0.15,size*0.5);c.stroke();
  c.beginPath();c.moveTo(size*0.2,-size*0.05);c.quadraticCurveTo(size*0.4,size*0.3,size*0.15,size*0.5);c.stroke();
  // stethoscope head
  c.fillStyle='#c0392b';c.beginPath();c.arc(size*0.15,size*0.52,size*0.08,0,Math.PI*2);c.fill();
  // outline
  c.strokeStyle='rgba(44,62,80,0.4)';c.lineWidth=2;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  // glow (animated)
  let glowI=0.3+Math.sin(anim*2)*0.1;
  c.shadowColor='#3498db';c.shadowBlur=15;
  c.strokeStyle='rgba(52,152,219,'+glowI+')';c.lineWidth=2.5;c.beginPath();c.arc(0,0,size+3,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;
  // ID badge
  c.fillStyle='rgba(255,255,255,0.8)';
  c.beginPath();c.roundRect(-size*0.55,-size*0.15,size*0.25,size*0.35,2);c.fill();
  c.strokeStyle='rgba(0,0,0,0.2)';c.lineWidth=0.5;c.beginPath();c.roundRect(-size*0.55,-size*0.15,size*0.25,size*0.35,2);c.stroke();
  c.fillStyle='#3498db';c.fillRect(-size*0.53,-size*0.13,size*0.21,size*0.06);
  c.globalAlpha=1;
  c.restore();
}'''

if old_player in c:
    c = c.replace(old_player, new_player)
    print('drawPlayer replaced')
else:
    print('drawPlayer NOT found - trying regex')
    pat = r'function drawPlayer\(c,x,y,size,hp,maxHp,invincible\)\{.*?c\.restore\(\);\n\}'
    m = re.search(pat, c, re.DOTALL)
    if m:
        c = c[:m.start()] + new_player + c[m.end():]
        print('drawPlayer replaced via regex')

# === 5. Update drawPatient call to pass elite flag ===
c = c.replace('drawPatient(ctx,ex,ey,e.size,e.color,e.draw);',
              'drawPatient(ctx,ex,ey,e.size,e.color,e.draw,e.elite);')
print('drawPatient call updated')

# === 6. Enhance XP orbs ===
old_xp = '''  // XP orbs
  ctx.fillStyle='#2ecc71';
  for(let o of G.xpOrbs){
    let ox=o.x-cx,oy=o.y-cy;
    if(ox<-20||ox>canvas.width+20||oy<-20||oy>canvas.height+20)continue;
    ctx.globalAlpha=0.6+Math.sin(Date.now()/300)*0.3;
    ctx.beginPath();ctx.arc(ox,oy,o.size,0,Math.PI*2);ctx.fill();
    ctx.globalAlpha=1;
    ctx.strokeStyle='rgba(46,204,113,0.4)';ctx.lineWidth=1;ctx.stroke();
  }'''

new_xp = '''  // XP orbs (beautified)
  for(let o of G.xpOrbs){
    let ox=o.x-cx,oy=o.y-cy;
    if(ox<-20||ox>canvas.width+20||oy<-20||oy>canvas.height+20)continue;
    let pulse=0.6+Math.sin(Date.now()/250+o.x*0.1)*0.35;
    // glow
    ctx.shadowColor='#2ecc71';ctx.shadowBlur=8;
    ctx.globalAlpha=pulse*0.5;ctx.fillStyle='#2ecc71';
    ctx.beginPath();ctx.arc(ox,oy,o.size+3,0,Math.PI*2);ctx.fill();
    // main orb
    ctx.globalAlpha=pulse;ctx.fillStyle='#44ff88';
    ctx.beginPath();ctx.arc(ox,oy,o.size,0,Math.PI*2);ctx.fill();
    // inner highlight
    ctx.globalAlpha=pulse*0.8;ctx.fillStyle='#aaffcc';
    ctx.beginPath();ctx.arc(ox-o.size*0.2,oy-o.size*0.2,o.size*0.35,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
  }'''

if old_xp in c:
    c = c.replace(old_xp, new_xp)
    print('XP orbs beautified')

# === 7. Enhance particles (bigger, more colorful) ===
old_spawn = '''function spawnParticles(x,y,count,color){
  for(let i=0;i<count;i++){
    G.particles.push({x,y,vx:rand(-2,2),vy:rand(-2,2),life:rand(200,500),maxLife:500,size:rand(2,5),color});
  }
}'''

new_spawn = '''function spawnParticles(x,y,count,color){
  for(let i=0;i<count;i++){
    G.particles.push({x,y,vx:rand(-3,3),vy:rand(-3,3),life:rand(300,600),maxLife:600,size:rand(2,6),color});
  }
}'''

if old_spawn in c:
    c = c.replace(old_spawn, new_spawn)
    print('Particles enhanced')

# === 8. Enhance minimap ===
old_mm = '''function drawMinimap(){
  let ms=110,mScale=ms/G.mapSize;
  mmCtx.fillStyle='rgba(0,0,0,0.7)';mmCtx.fillRect(0,0,ms,ms);
  // enemies
  mmCtx.fillStyle='#e74c3c';
  for(let e of G.enemies){mmCtx.fillRect(e.x*mScale-1,e.y*mScale-1,e.isBoss?4:2,e.isBoss?4:2)}
  // xp orbs
  mmCtx.fillStyle='rgba(46,204,113,0.5)';
  for(let o of G.xpOrbs){mmCtx.fillRect(o.x*mScale,o.y*mScale,1,1)}
  // player
  mmCtx.fillStyle='#f1c40f';mmCtx.fillRect(G.player.x*mScale-2,G.player.y*mScale-2,4,4);
  // viewport
  mmCtx.strokeStyle='#fff';mmCtx.lineWidth=0.5;
  mmCtx.strokeRect(G.camera.x*mScale,G.camera.y*mScale,canvas.width*mScale,canvas.height*mScale);
  // border
  mmCtx.strokeStyle='#555';mmCtx.lineWidth=1;mmCtx.strokeRect(0,0,ms,ms);
}'''

new_mm = '''function drawMinimap(){
  let ms=120,mScale=ms/G.mapSize;
  mmCtx.fillStyle='rgba(0,0,0,0.8)';mmCtx.fillRect(0,0,ms,ms);
  // map border on minimap
  mmCtx.strokeStyle='rgba(255,255,255,0.15)';mmCtx.lineWidth=1;mmCtx.strokeRect(0,0,ms,ms);
  // enemies (color coded)
  for(let e of G.enemies){
    mmCtx.fillStyle=e.isBoss?'#ff0000':e.elite?'#ff8800':'#ff4444';
    let s=e.isBoss?4:e.elite?3:2;
    mmCtx.beginPath();mmCtx.arc(e.x*mScale,e.y*mScale,s,0,Math.PI*2);mmCtx.fill();
  }
  // xp orbs
  mmCtx.fillStyle='rgba(46,204,113,0.6)';
  for(let o of G.xpOrbs){mmCtx.fillRect(o.x*mScale,o.y*mScale,1,1)}
  // player (pulsing)
  let pPulse=0.7+Math.sin(Date.now()/300)*0.3;
  mmCtx.fillStyle='#ffdd44';
  mmCtx.shadowColor='#ffdd44';mmCtx.shadowBlur=4;
  mmCtx.beginPath();mmCtx.arc(G.player.x*mScale,G.player.y*mScale,3,0,Math.PI*2);mmCtx.fill();
  mmCtx.shadowBlur=0;
  // viewport
  mmCtx.strokeStyle='rgba(255,255,255,'+pPulse+')';mmCtx.lineWidth=1;
  mmCtx.strokeRect(G.camera.x*mScale,G.camera.y*mScale,canvas.width*mScale,canvas.height*mScale);
  // border
  mmCtx.strokeStyle='rgba(255,255,255,0.25)';mmCtx.lineWidth=2;mmCtx.strokeRect(0,0,ms,ms);
}'''

if old_mm in c:
    c = c.replace(old_mm, new_mm)
    print('Minimap enhanced')

# === 9. Enhance boss speech ===
old_speech = '''function showBossSpeech(text){
  let el=document.getElementById('boss-speech');
  el.textContent=text;el.style.opacity='1';
  setTimeout(()=>{el.style.opacity='0'},2500);
}'''

new_speech = '''function showBossSpeech(text){
  let el=document.getElementById('boss-speech');
  el.textContent=text;el.style.opacity='1';el.style.transform='translate(-50%,-50%) scale(1.2)';
  setTimeout(()=>{el.style.transform='translate(-50%,-50%) scale(1)'},100);
  setTimeout(()=>{el.style.opacity='0'},3000);
}'''

if old_speech in c:
    c = c.replace(old_speech, new_speech)
    print('Boss speech enhanced')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('\nAll beautifications applied!')
