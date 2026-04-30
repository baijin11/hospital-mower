#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D 全面升级脚本 - 发不出绩效的医院
通过 Canvas 多层渐变、高光、投影技术模拟3D效果
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. CSS 全面升级为3D玻璃质感
# ============================================================
old_style = '''<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;overflow:hidden;font-family:\'Segoe UI\',\'Microsoft YaHei\',sans-serif;touch-action:none;user-select:none}
canvas{display:block}
#ui{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:10}
#hud{position:absolute;top:10px;left:10px;color:#fff;font-size:13px;text-shadow:0 0 4px #000}
.bar{width:180px;height:14px;background:#333;border-radius:7px;margin:3px 0;overflow:hidden;border:1px solid #555}
.bar-hp .fill{height:100%;background:linear-gradient(90deg,#e74c3c,#c0392b);border-radius:7px;transition:width .3s}
.bar-xp .fill{height:100%;background:linear-gradient(90deg,#2ecc71,#27ae60);border-radius:7px;transition:width .3s}
#hud-timer{position:absolute;top:10px;right:10px;color:#f1c40f;font-size:20px;font-weight:bold;text-shadow:0 0 8px #000}
#hud-level{position:absolute;top:10px;left:50%;transform:translateX(-50%);color:#f39c12;font-size:17px;font-weight:bold;text-shadow:0 0 8px #000}
#hud-wave{position:absolute;top:36px;left:50%;transform:translateX(-50%);color:#aaa;font-size:12px;text-shadow:0 0 4px #000}
#hud-kills{position:absolute;top:58px;left:10px;color:#e74c3c;font-size:12px;text-shadow:0 0 4px #000}
#hud-weapons{position:absolute;top:80px;left:10px;font-size:11px;color:#3498db;text-shadow:0 0 4px #000}
#hud-weapons div{margin:1px 0}
#boss-hp-bar{position:absolute;bottom:60px;left:50%;transform:translateX(-50%);width:300px;height:18px;background:#333;border-radius:9px;border:2px solid #c0392b;display:none}
#boss-hp-bar .fill{height:100%;background:linear-gradient(90deg,#c0392b,#e74c3c);border-radius:7px;transition:width .2s}
#boss-hp-bar .name{text-align:center;color:#fff;font-size:12px;font-weight:bold;margin-top:2px;text-shadow:0 0 6px #000}
#boss-speech{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#ff6b6b;font-size:28px;font-weight:bold;text-shadow:0 0 20px #000,2px 2px 0 #000;opacity:0;transition:opacity .3s;pointer-events:none;text-align:center;white-space:nowrap}
#minimap{position:absolute;bottom:10px;right:10px;border:1px solid #555;border-radius:4px}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:100;pointer-events:auto}
#menu{background:radial-gradient(ellipse at center,#1a1a2e 0%,#0a0a0a 70%)}
#menu h1{font-size:36px;color:#f1c40f;text-shadow:0 0 20px #f39c12;margin-bottom:8px;text-align:center}
#menu .sub{color:#aaa;font-size:14px;margin-bottom:24px}
.btn{padding:12px 44px;font-size:18px;border:none;border-radius:10px;cursor:pointer;margin:6px;font-weight:bold;pointer-events:auto;transition:transform .15s}
.btn:hover{transform:scale(1.05)}
.btn:active{transform:scale(.95)}
.btn-start{background:linear-gradient(135deg,#e74c3c,#c0392b);color:#fff}
.btn-retry{background:linear-gradient(135deg,#3498db,#2980b9);color:#fff}
.btn-back{background:linear-gradient(135deg,#555,#333);color:#aaa;font-size:14px;padding:8px 24px;margin-top:12px}
#levelup{background:rgba(0,0,0,.88);display:none}
#levelup h2{color:#f1c40f;font-size:28px;margin-bottom:16px;text-shadow:0 0 10px #f39c12}
#levelup-cards{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;pointer-events:auto}
.card{background:linear-gradient(145deg,#1e2a3a,#162030);border:2px solid #3498db;border-radius:14px;padding:16px;width:185px;cursor:pointer;transition:all .2s;text-align:center;color:#fff;pointer-events:auto}
.card:hover{transform:translateY(-6px) scale(1.02);border-color:#f1c40f;box-shadow:0 6px 24px rgba(241,196,15,.3)}
.card .icon{font-size:36px;margin-bottom:8px}
.card .name{font-size:14px;font-weight:bold;margin-bottom:4px}
.card .desc{font-size:11px;color:#aaa}
.card .lv{font-size:11px;color:#2ecc71;margin-top:6px}
#gameover{background:rgba(0,0,0,.9);display:none}
#gameover h2{color:#e74c3c;font-size:32px;margin-bottom:16px;text-shadow:0 0 10px #c0392b}
#gameover.victory h2{color:#f1c40f;text-shadow:0 0 10px #f39c12}
.stat{color:#ccc;font-size:15px;margin:4px 0}
.stat span{color:#f1c40f;font-weight:bold}
#controls-hint{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);color:#666;font-size:11px;text-shadow:0 0 4px #000}
</style>'''

new_style = '''<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#060612;overflow:hidden;font-family:'Segoe UI','Microsoft YaHei',sans-serif;touch-action:none;user-select:none}
canvas{display:block}
#ui{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:10}
#hud{position:absolute;top:12px;left:12px;color:#fff;font-size:13px}
.hud-panel{background:rgba(0,0,0,0.55);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:8px 12px;margin-bottom:4px;box-shadow:0 4px 16px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.08)}
.bar{width:180px;height:14px;background:rgba(0,0,0,0.6);border-radius:7px;margin:3px 0;overflow:hidden;border:1px solid rgba(255,255,255,0.1);box-shadow:inset 0 2px 4px rgba(0,0,0,0.5)}
.bar-hp .fill{height:100%;background:linear-gradient(90deg,#ff6b6b,#e74c3c,#c0392b);border-radius:7px;transition:width .3s;box-shadow:0 0 8px rgba(231,76,60,0.7),inset 0 1px 0 rgba(255,255,255,0.3)}
.bar-xp .fill{height:100%;background:linear-gradient(90deg,#55efc4,#2ecc71,#27ae60);border-radius:7px;transition:width .3s;box-shadow:0 0 8px rgba(46,204,113,0.7),inset 0 1px 0 rgba(255,255,255,0.3)}
#hud-timer{position:absolute;top:12px;right:12px;color:#f1c40f;font-size:22px;font-weight:bold;text-shadow:0 0 16px rgba(241,196,15,0.9),0 2px 4px rgba(0,0,0,0.8);background:rgba(0,0,0,0.55);backdrop-filter:blur(8px);border:1px solid rgba(241,196,15,0.25);border-radius:10px;padding:6px 14px;box-shadow:0 4px 16px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.08)}
#hud-level{position:absolute;top:12px;left:50%;transform:translateX(-50%);color:#f39c12;font-size:18px;font-weight:bold;text-shadow:0 0 16px rgba(243,156,18,0.9);background:rgba(0,0,0,0.55);backdrop-filter:blur(8px);border:1px solid rgba(243,156,18,0.25);border-radius:10px;padding:5px 18px;box-shadow:0 4px 16px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.08)}
#hud-wave{position:absolute;top:44px;left:50%;transform:translateX(-50%);color:#ccc;font-size:12px;text-shadow:0 1px 3px rgba(0,0,0,0.8);background:rgba(0,0,0,0.4);backdrop-filter:blur(4px);border-radius:8px;padding:3px 12px}
#hud-kills{position:absolute;top:62px;left:12px;color:#ff6b6b;font-size:12px;text-shadow:0 0 6px rgba(231,76,60,0.8)}
#hud-weapons{position:absolute;top:82px;left:12px;font-size:11px;color:#74b9ff;text-shadow:0 0 4px rgba(52,152,219,0.8)}
#hud-weapons div{margin:2px 0;background:rgba(0,0,0,0.3);border-radius:4px;padding:1px 6px}
#boss-hp-bar{position:absolute;bottom:60px;left:50%;transform:translateX(-50%);width:320px;background:rgba(0,0,0,0.7);backdrop-filter:blur(8px);border-radius:12px;border:2px solid rgba(192,57,43,0.6);display:none;padding:4px 6px;box-shadow:0 0 20px rgba(192,57,43,0.4),inset 0 1px 0 rgba(255,255,255,0.05)}
#boss-hp-bar .fill-wrap{height:16px;background:rgba(0,0,0,0.5);border-radius:8px;overflow:hidden;border:1px solid rgba(0,0,0,0.3)}
#boss-hp-bar .fill{height:100%;background:linear-gradient(90deg,#7b0000,#c0392b,#e74c3c,#ff6b6b);border-radius:7px;transition:width .2s;box-shadow:0 0 10px rgba(255,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.2)}
#boss-hp-bar .name{text-align:center;color:#ff8888;font-size:12px;font-weight:bold;margin-top:3px;text-shadow:0 0 8px rgba(255,100,100,0.8)}
#boss-speech{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#ff6b6b;font-size:30px;font-weight:bold;text-shadow:0 0 30px rgba(255,0,0,0.9),0 0 60px rgba(255,0,0,0.4),2px 2px 0 #000;opacity:0;transition:opacity .3s;pointer-events:none;text-align:center;white-space:nowrap}
#minimap{position:absolute;bottom:12px;right:12px;border:1px solid rgba(255,255,255,0.2);border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.05)}
.overlay{position:fixed;top:0;left:0;width:100%;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:100;pointer-events:auto}
#menu{background:radial-gradient(ellipse at 50% 40%,#12122a 0%,#08081a 50%,#030308 100%)}
#menu h1{font-size:42px;color:#f1c40f;text-shadow:0 0 30px rgba(241,196,15,0.9),0 0 60px rgba(255,150,0,0.5),0 0 90px rgba(255,100,0,0.3);margin-bottom:8px;text-align:center;letter-spacing:2px}
#menu .sub{color:#888;font-size:14px;margin-bottom:28px;text-shadow:0 1px 3px rgba(0,0,0,0.8)}
.btn{padding:13px 48px;font-size:18px;border:none;border-radius:12px;cursor:pointer;margin:6px;font-weight:bold;pointer-events:auto;transition:all .2s;position:relative;overflow:hidden}
.btn::before{content:'';position:absolute;top:0;left:0;right:0;height:40%;background:rgba(255,255,255,0.12);border-radius:12px 12px 0 0;pointer-events:none}
.btn:hover{transform:scale(1.06) translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.4)}
.btn:active{transform:scale(.96)}
.btn-start{background:linear-gradient(145deg,#e74c3c,#c0392b,#a0281d);color:#fff;box-shadow:0 4px 16px rgba(192,57,43,0.5),inset 0 1px 0 rgba(255,255,255,0.15)}
.btn-retry{background:linear-gradient(145deg,#3498db,#2980b9,#1a6fa0);color:#fff;box-shadow:0 4px 16px rgba(52,152,219,0.5),inset 0 1px 0 rgba(255,255,255,0.15)}
.btn-back{background:linear-gradient(145deg,#555,#333);color:#aaa;font-size:14px;padding:9px 28px;margin-top:12px}
#levelup{background:rgba(0,0,0,.9);backdrop-filter:blur(12px);display:none}
#levelup h2{color:#f1c40f;font-size:30px;margin-bottom:18px;text-shadow:0 0 20px rgba(241,196,15,0.9),0 0 40px rgba(255,150,0,0.4)}
#levelup-cards{display:flex;gap:16px;flex-wrap:wrap;justify-content:center;pointer-events:auto}
.card{background:linear-gradient(145deg,rgba(30,42,58,0.9),rgba(22,32,48,0.95));border:1px solid rgba(52,152,219,0.5);border-radius:16px;padding:18px;width:190px;cursor:pointer;transition:all .25s;text-align:center;color:#fff;pointer-events:auto;box-shadow:0 8px 24px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.06);backdrop-filter:blur(6px)}
.card:hover{transform:translateY(-8px) scale(1.03);border-color:rgba(241,196,15,0.7);box-shadow:0 12px 36px rgba(241,196,15,0.25),inset 0 1px 0 rgba(255,255,255,0.1)}
.card .icon{font-size:38px;margin-bottom:10px;filter:drop-shadow(0 0 8px rgba(255,255,255,0.3))}
.card .name{font-size:14px;font-weight:bold;margin-bottom:5px;text-shadow:0 1px 3px rgba(0,0,0,0.5)}
.card .desc{font-size:11px;color:#99aabb}
.card .lv{font-size:11px;color:#2ecc71;margin-top:8px;text-shadow:0 0 8px rgba(46,204,113,0.5)}
#gameover{background:rgba(0,0,0,.92);backdrop-filter:blur(12px);display:none}
#gameover h2{color:#e74c3c;font-size:34px;margin-bottom:18px;text-shadow:0 0 20px rgba(192,57,43,0.9)}
#gameover.victory h2{color:#f1c40f;text-shadow:0 0 20px rgba(241,196,15,0.9)}
.stat{color:#ccc;font-size:15px;margin:5px 0}
.stat span{color:#f1c40f;font-weight:bold;text-shadow:0 0 8px rgba(241,196,15,0.5)}
#controls-hint{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);color:#555;font-size:11px;background:rgba(0,0,0,0.4);border-radius:6px;padding:3px 10px}
</style>'''

content = content.replace(old_style, new_style)

# ============================================================
# 2. HTML HUD 结构升级（血条包装）
# ============================================================
old_hud = '''  <div id="hud">
    <div>❤️ <span id="hp-text">100/100</span></div>
    <div class="bar bar-hp"><div class="fill" id="hp-bar"></div></div>
    <div>⭐ <span id="xp-text">0/10</span></div>
    <div class="bar bar-xp"><div class="fill" id="xp-bar"></div></div>
  </div>'''

new_hud = '''  <div id="hud">
    <div class="hud-panel">
      <div style="font-size:11px;color:#ff8888;margin-bottom:2px">❤️ <span id="hp-text">100/100</span></div>
      <div class="bar bar-hp"><div class="fill" id="hp-bar"></div></div>
      <div style="font-size:11px;color:#55efc4;margin-bottom:2px;margin-top:4px">⭐ <span id="xp-text">0/10</span></div>
      <div class="bar bar-xp"><div class="fill" id="xp-bar"></div></div>
    </div>
  </div>'''

content = content.replace(old_hud, new_hud)

# ============================================================
# 3. Boss HP bar HTML 内层结构升级
# ============================================================
old_boss_bar = '  <div id="boss-hp-bar"><div class="fill" id="boss-hp-fill"></div><div class="name" id="boss-name"></div></div>'
new_boss_bar = '  <div id="boss-hp-bar"><div class="fill-wrap"><div class="fill" id="boss-hp-fill"></div></div><div class="name" id="boss-name"></div></div>'
content = content.replace(old_boss_bar, new_boss_bar)

# ============================================================
# 4. 3D 渲染辅助函数 - 注入到 DRAWING HELPERS 之前
# ============================================================
old_drawing_comment = '// ==================== DRAWING HELPERS ===================='
new_drawing_helpers = '''// ==================== 3D RENDERING HELPERS ====================
// 绘制3D球体（多层渐变+高光+投影）
function draw3DSphere(c, x, y, r, baseColor, opts){
  opts = opts || {};
  let lightX = opts.lightX !== undefined ? opts.lightX : -0.35;
  let lightY = opts.lightY !== undefined ? opts.lightY : -0.35;
  let shadowColor = opts.shadowColor || 'rgba(0,0,0,0.4)';
  let glowColor = opts.glowColor || null;
  let glowBlur = opts.glowBlur || 0;
  // 落地阴影
  c.save();
  if(!opts.noShadow){
    c.fillStyle = 'rgba(0,0,0,0.22)';
    c.beginPath();
    c.ellipse(x + r*0.1, y + r*0.75, r*0.85, r*0.22, 0, 0, Math.PI*2);
    c.fill();
  }
  // 环境光晕
  if(glowColor && glowBlur > 0){
    c.shadowColor = glowColor;
    c.shadowBlur = glowBlur;
  }
  // 主体径向渐变（模拟3D球面光照）
  let hx = x + lightX*r, hy = y + lightY*r;
  let grad = c.createRadialGradient(hx, hy, r*0.05, x, y, r*1.05);
  if(opts.gradStops){
    for(let s of opts.gradStops) grad.addColorStop(s[0], s[1]);
  } else {
    grad.addColorStop(0, lightenColor(baseColor, 80));
    grad.addColorStop(0.35, baseColor);
    grad.addColorStop(0.75, darkenColor(baseColor, 40));
    grad.addColorStop(1.0, darkenColor(baseColor, 80));
  }
  c.fillStyle = grad;
  c.beginPath();
  c.arc(x, y, r, 0, Math.PI*2);
  c.fill();
  c.shadowBlur = 0;
  // 轮廓（深色边缘增强3D感）
  let edgeG = c.createRadialGradient(x, y, r*0.6, x, y, r);
  edgeG.addColorStop(0, 'rgba(0,0,0,0)');
  edgeG.addColorStop(1, 'rgba(0,0,0,0.35)');
  c.fillStyle = edgeG;
  c.beginPath();
  c.arc(x, y, r, 0, Math.PI*2);
  c.fill();
  // 高光斑（镜面反射）
  let hlGrad = c.createRadialGradient(hx, hy, 0, hx, hy, r*0.45);
  hlGrad.addColorStop(0, 'rgba(255,255,255,0.65)');
  hlGrad.addColorStop(0.4, 'rgba(255,255,255,0.15)');
  hlGrad.addColorStop(1, 'rgba(255,255,255,0)');
  c.fillStyle = hlGrad;
  c.beginPath();
  c.arc(x, y, r, 0, Math.PI*2);
  c.fill();
  // 次级高光（小亮点）
  c.fillStyle = 'rgba(255,255,255,0.5)';
  c.beginPath();
  c.arc(hx + r*0.05, hy + r*0.05, r*0.1, 0, Math.PI*2);
  c.fill();
  c.restore();
}

// 颜色处理工具
function lightenColor(hex, amt){
  let r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  r = Math.min(255, r+amt); g = Math.min(255, g+amt); b = Math.min(255, b+amt);
  return '#'+[r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('');
}
function darkenColor(hex, amt){
  // 支持 rgba 字符串
  if(hex.startsWith('rgba')||hex.startsWith('rgb')) return hex;
  if(hex.length < 4) return hex;
  let r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  r = Math.max(0, r-amt); g = Math.max(0, g-amt); b = Math.max(0, b-amt);
  return '#'+[r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('');
}

// ==================== DRAWING HELPERS ===================='''

content = content.replace(old_drawing_comment, new_drawing_helpers)

# ============================================================
# 5. 替换 drawPatient 函数 - 真3D球体角色
# ============================================================
old_drawPatient = '''function drawPatient(c,x,y,size,color,type,el){
  c.save();c.translate(x,y);
  let anim=Date.now()/180;
  // shadow
  c.fillStyle=\'rgba(0,0,0,0.18)\';c.beginPath();c.ellipse(0,size*0.72,size*0.9,size*0.22,0,0,Math.PI*2);c.fill();
  // elite glow
  if(el){c.shadowColor=\'#f39c12\';c.shadowBlur=12+Math.sin(anim*2)*4}
  // body with gradient
  let bg=c.createRadialGradient(-size*0.15,-size*0.15,size*0.05,0,0,size);
  bg.addColorStop(0,\'rgba(255,255,255,0.6)\');bg.addColorStop(0.55,color);bg.addColorStop(1,\'rgba(0,0,0,0.35)\');
  c.fillStyle=bg;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.fill();
  c.shadowBlur=0;
  // outline
  c.strokeStyle=\'rgba(0,0,0,0.2)\';c.lineWidth=1.5;c.beginPath();c.arc(0,0,size,0,Math.PI*2);c.stroke();
  // hospital gown detail
  c.fillStyle=\'rgba(255,255,255,0.1)\';c.beginPath();c.arc(0,size*0.05,size*0.65,Math.PI,0);c.fill();
  // face
  c.fillStyle=\'#ffe0c0\';c.beginPath();c.arc(0,-size*0.12,size*0.38,0,Math.PI*2);c.fill();
  let eOff=size*0.14;
  if(type===\'angry\'){
    c.fillStyle=\'#fff\';c.beginPath();c.arc(-eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.fillStyle=\'#cc0000\';
    c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.strokeStyle=\'#993300\';c.lineWidth=2;
    c.beginPath();c.moveTo(-eOff-size*0.12,-size*0.28);c.lineTo(-eOff+size*0.08,-size*0.2);c.stroke();
    c.beginPath();c.moveTo(eOff+size*0.12,-size*0.28);c.lineTo(eOff-size*0.08,-size*0.2);c.stroke();
    c.beginPath();c.arc(0,size*0.2,size*0.15,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
    c.fillStyle=\'#1a1a2e\';c.fillRect(size*0.5,-size*0.28,size*0.25,size*0.38);
    c.fillStyle=\'#4488ff\';c.fillRect(size*0.53,-size*0.21,size*0.19,size*0.23);
  }else if(type===\'fast\'){
    c.fillStyle=\'#333\';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.fillStyle=\'#fff\';c.beginPath();c.arc(-eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.strokeStyle=\'#bb8866\';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.18,size*0.12,Math.PI+0.2,Math.PI*2-0.2);c.stroke();
    // speed lines
    c.strokeStyle=\'rgba(231,76,60,0.3)\';c.lineWidth=1;
    for(let i=0;i<3;i++){c.beginPath();c.moveTo(-size*1.1,-size*0.3+i*size*0.3);c.lineTo(-size*0.7,-size*0.3+i*size*0.3);c.stroke()}
  }else if(type===\'family\'){
    c.fillStyle=\'#333\';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.strokeStyle=\'#bb8866\';c.lineWidth=1;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
    // extra person behind
    c.fillStyle=color;c.globalAlpha=0.4;c.beginPath();c.arc(-size*0.45,size*0.3,size*0.5,0,Math.PI*2);c.fill();c.globalAlpha=1;
  }else if(type===\'admin\'){
    c.fillStyle=\'#333\';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    // tie
    c.fillStyle=\'#c0392b\';c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(-size*0.08,size*0.35);c.lineTo(0,size*0.25);c.lineTo(size*0.08,size*0.35);c.closePath();c.fill();
    // suit line
    c.strokeStyle=\'rgba(0,0,0,0.2)\';c.lineWidth=1;c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(0,size*0.3);c.stroke();
    // glasses
    c.strokeStyle=\'#222\';c.lineWidth=1.5;c.beginPath();c.arc(-eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.moveTo(-eOff+size*0.1,-size*0.14);c.lineTo(eOff-size*0.1,-size*0.14);c.stroke();
    // frown
    c.strokeStyle=\'#555\';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.22,size*0.1,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
  }else{
    c.fillStyle=\'#333\';c.beginPath();c.arc(-eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.06,0,Math.PI*2);c.fill();
    c.fillStyle=\'#fff\';c.beginPath();c.arc(-eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.strokeStyle=\'#bb8866\';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
  }
  c.restore();
}'''

new_drawPatient = '''function drawPatient(c,x,y,size,color,type,el){
  c.save();c.translate(x,y);
  let anim=Date.now()/180;
  // elite 光晕
  if(el){
    c.shadowColor='#f39c12';c.shadowBlur=14+Math.sin(anim*2)*5;
    c.strokeStyle='rgba(243,156,18,0.6)';c.lineWidth=2.5;
    c.beginPath();c.arc(0,0,size+5+Math.sin(anim*2)*2,0,Math.PI*2);c.stroke();
    c.shadowBlur=0;
  }
  // 3D球体主体
  let glowCol = el ? '#f39c12' : (type==='angry' ? '#e74c3c' : null);
  let glowAmt = el ? (10+Math.sin(anim*2)*4) : 0;
  let gradStops;
  if(type==='angry'){
    gradStops=[[0,'#ffaa88'],[0.35,color],[0.75,darkenColor(color,50)],[1,'#1a0000']];
  }else if(type==='admin'){
    gradStops=[[0,'#8899aa'],[0.35,color],[0.75,darkenColor(color,40)],[1,'#0a0a14']];
  }else if(type==='fast'){
    gradStops=[[0,'#ff9999'],[0.35,color],[0.75,darkenColor(color,40)],[1,'#1a0000']];
  }else{
    gradStops=[[0,lightenColor(color,70)],[0.35,color],[0.75,darkenColor(color,40)],[1,darkenColor(color,90)]];
  }
  draw3DSphere(c, 0, 0, size, color, {gradStops, glowColor:glowCol, glowBlur:glowAmt, noShadow:true});
  // 脸部区域
  let fr=size*0.38, fy=-size*0.12;
  let faceG=c.createRadialGradient(-fr*0.2,fy-fr*0.25,fr*0.05,0,fy,fr);
  faceG.addColorStop(0,'#ffe8cc');faceG.addColorStop(0.6,'#f0c898');faceG.addColorStop(1,'#d4a070');
  c.fillStyle=faceG;c.beginPath();c.arc(0,fy,fr,0,Math.PI*2);c.fill();
  // 脸部高光
  c.fillStyle='rgba(255,255,255,0.25)';c.beginPath();c.arc(-fr*0.2,fy-fr*0.25,fr*0.35,0,Math.PI*2);c.fill();
  let eOff=size*0.14;
  if(type==='angry'){
    // 愤怒眼
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.16,size*0.1,0,Math.PI*2);c.fill();
    c.fillStyle='#cc0000';
    c.beginPath();c.arc(-eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    // 愤怒眉
    c.strokeStyle='#993300';c.lineWidth=2.5;
    c.beginPath();c.moveTo(-eOff-size*0.14,-size*0.3);c.lineTo(-eOff+size*0.08,-size*0.2);c.stroke();
    c.beginPath();c.moveTo(eOff+size*0.14,-size*0.3);c.lineTo(eOff-size*0.08,-size*0.2);c.stroke();
    // 嘴
    c.strokeStyle='#882200';c.lineWidth=2;c.beginPath();c.arc(0,size*0.2,size*0.15,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
    // 手机（3D感）
    c.fillStyle='#0a0a1e';c.beginPath();c.roundRect(size*0.48,-size*0.32,size*0.28,size*0.42,2);c.fill();
    c.fillStyle='rgba(68,136,255,0.85)';c.beginPath();c.roundRect(size*0.51,-size*0.28,size*0.22,size*0.3,1);c.fill();
    c.fillStyle='rgba(255,255,255,0.2)';c.beginPath();c.moveTo(size*0.51,-size*0.28);c.lineTo(size*0.73,-size*0.28);c.lineTo(size*0.51,-size*0.1);c.closePath();c.fill();
  }else if(type==='fast'){
    // 急诊患者眼（血丝）
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff,-size*0.15,size*0.085,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.15,size*0.085,0,Math.PI*2);c.fill();
    c.fillStyle='#cc2222';c.beginPath();c.arc(-eOff,-size*0.15,size*0.04,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.15,size*0.04,0,Math.PI*2);c.fill();
    // 速度线（发光）
    c.strokeStyle='rgba(231,76,60,0.5)';c.lineWidth=1.5;
    for(let i=0;i<3;i++){
      let iy=-size*0.3+i*size*0.32;
      c.shadowColor='rgba(231,76,60,0.4)';c.shadowBlur=3;
      c.beginPath();c.moveTo(-size*1.1,iy);c.lineTo(-size*0.7,iy);c.stroke();
    }
    c.shadowBlur=0;
    c.strokeStyle='#bb8866';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.18,size*0.12,Math.PI+0.2,Math.PI*2-0.2);c.stroke();
  }else if(type==='family'){
    c.fillStyle='#444';c.beginPath();c.arc(-eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.strokeStyle='#bb8866';c.lineWidth=1.2;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
    // 背后的人（半透明3D小球）
    c.globalAlpha=0.45;
    draw3DSphere(c,-size*0.5,size*0.35,size*0.5,color,{noShadow:true});
    c.globalAlpha=1;
  }else if(type==='admin'){
    // 行政人员 - 西装领带
    c.fillStyle='#333';c.beginPath();c.arc(-eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    // 3D领带
    let tG=c.createLinearGradient(0,-size*0.05,0,size*0.35);
    tG.addColorStop(0,'#e74c3c');tG.addColorStop(1,'#7b241c');
    c.fillStyle=tG;c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(-size*0.09,size*0.35);c.lineTo(0,size*0.25);c.lineTo(size*0.09,size*0.35);c.closePath();c.fill();
    c.fillStyle='rgba(255,255,255,0.2)';c.beginPath();c.moveTo(0,-size*0.05);c.lineTo(-size*0.03,size*0.15);c.lineTo(0,size*0.08);c.closePath();c.fill();
    // 眼镜（3D感）
    c.strokeStyle='#1a1a2e';c.lineWidth=1.8;
    c.beginPath();c.arc(-eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.1,0,Math.PI*2);c.stroke();
    c.beginPath();c.moveTo(-eOff+size*0.1,-size*0.14);c.lineTo(eOff-size*0.1,-size*0.14);c.stroke();
    c.fillStyle='rgba(100,180,255,0.2)';c.beginPath();c.arc(-eOff,-size*0.14,size*0.09,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.09,0,Math.PI*2);c.fill();
    c.strokeStyle='#555';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.22,size*0.1,Math.PI+0.3,Math.PI*2-0.3);c.stroke();
  }else{
    // 普通患者
    c.fillStyle='#444';c.beginPath();c.arc(-eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff,-size*0.14,size*0.065,0,Math.PI*2);c.fill();
    c.fillStyle='#fff';c.beginPath();c.arc(-eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.beginPath();c.arc(eOff+size*0.02,-size*0.16,size*0.025,0,Math.PI*2);c.fill();
    c.strokeStyle='#bb8866';c.lineWidth=1.5;c.beginPath();c.arc(0,size*0.15,size*0.12,0.1,Math.PI-0.1);c.stroke();
  }
  c.restore();
}'''

content = content.replace(old_drawPatient, new_drawPatient)

# ============================================================
# 6. 替换 drawBoss 函数 - 全3D超级Boss
# ============================================================
old_drawBoss_start = 'function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){'
old_drawBoss_end = '  c.restore();\n}'

# 找到 drawBoss 函数完整内容
boss_start_idx = content.find(old_drawBoss_start)
# 找到函数结束位置（在 drawPlayer 函数之前）
player_func_idx = content.find('\nfunction drawPlayer(')
old_drawBoss = content[boss_start_idx:player_func_idx]

new_drawBoss = '''function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){
  c.save();c.translate(x,y);
  let anim=Date.now()/150;
  // 地面阴影（大椭圆）
  c.fillStyle='rgba(0,0,0,0.3)';
  c.beginPath();c.ellipse(0,size*0.85,size*1.15,size*0.32,0,0,Math.PI*2);c.fill();
  // 外层脉冲光环（双环）
  let auraR1=size+18+Math.sin(anim*1.8)*7;
  let auraR2=size+32+Math.sin(anim*2.3)*5;
  let auraA=raging?0.5:0.25;
  let auraC=raging?'255,0,0':'255,68,68';
  c.strokeStyle='rgba('+auraC+','+auraA+')';c.lineWidth=3;
  c.shadowColor='rgba('+auraC+',0.6)';c.shadowBlur=raging?20:10;
  c.beginPath();c.arc(0,0,auraR1,0,Math.PI*2);c.stroke();
  c.strokeStyle='rgba('+auraC+','+(auraA*0.5)+')';c.lineWidth=2;
  c.beginPath();c.arc(0,0,auraR2,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;
  // 3D主体球
  let bossGlowAmt = raging ? 40+Math.sin(anim*4)*12 : 22+Math.sin(anim*2)*6;
  let bossGlow = raging ? '#ff2200' : '#ff4444';
  let gradStops = raging
    ? [[0,'#ff9966'],[0.3,'#ff4422'],[0.65,color],[0.9,'#330000'],[1,'#1a0000']]
    : [[0,'#ff8888'],[0.3,'#ff4444'],[0.65,color],[0.9,'#440000'],[1,'#1a0000']];
  draw3DSphere(c, 0, 0, size, color, {
    gradStops, glowColor:bossGlow, glowBlur:bossGlowAmt, noShadow:true,
    lightX:-0.3, lightY:-0.35
  });
  // 愤怒脸部
  let fr=size*0.5, fy=-size*0.1;
  let faceG=c.createRadialGradient(-fr*0.2,fy-fr*0.2,fr*0.05,0,fy,fr);
  faceG.addColorStop(0,'#ffe0c0');faceG.addColorStop(0.6,'#e8c0a0');faceG.addColorStop(1,'#c09070');
  c.fillStyle=faceG;c.beginPath();c.arc(0,fy,fr,0,Math.PI*2);c.fill();
  c.fillStyle='rgba(255,255,255,0.2)';c.beginPath();c.arc(-fr*0.25,fy-fr*0.3,fr*0.35,0,Math.PI*2);c.fill();
  // 白眼
  c.fillStyle='#fff';c.beginPath();c.arc(-size*0.18,-size*0.18,size*0.14,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.18,-size*0.18,size*0.14,0,Math.PI*2);c.fill();
  // 眼球（愤怒红）
  let eyeC=raging?'#ff0000':'#cc0000';
  c.fillStyle=eyeC;
  c.shadowColor=eyeC;c.shadowBlur=raging?10:4;
  c.beginPath();c.arc(-size*0.16,-size*0.16,size*0.08,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.2,-size*0.16,size*0.08,0,Math.PI*2);c.fill();
  c.shadowBlur=0;
  c.fillStyle='#111';c.beginPath();c.arc(-size*0.15,-size*0.14,size*0.035,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.21,-size*0.14,size*0.035,0,Math.PI*2);c.fill();
  // 眼白亮点
  c.fillStyle='rgba(255,255,255,0.7)';c.beginPath();c.arc(-size*0.12,-size*0.17,size*0.02,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.24,-size*0.17,size*0.02,0,Math.PI*2);c.fill();
  // 眉毛（粗愤怒眉）
  let browC=raging?'#ff2200':'#cc0000';
  c.strokeStyle=browC;c.lineWidth=4.5;c.lineCap='round';
  c.shadowColor=browC;c.shadowBlur=6;
  c.beginPath();c.moveTo(-size*0.38,-size*0.4);c.lineTo(-size*0.04,-size*0.26);c.stroke();
  c.beginPath();c.moveTo(size*0.38,-size*0.4);c.lineTo(size*0.04,-size*0.26);c.stroke();
  c.shadowBlur=0;c.lineCap='butt';
  // 嘴（咆哮嘴）
  c.fillStyle='#660000';c.beginPath();c.arc(0,size*0.12,size*0.2,0,Math.PI);c.fill();
  c.fillStyle='#220000';c.beginPath();c.arc(0,size*0.15,size*0.15,0.1,Math.PI-0.1);c.fill();
  // 牙齿
  c.fillStyle='#eee';
  for(let i=-2;i<=2;i++){
    let tx=i*size*0.08;
    c.beginPath();c.roundRect(tx-3,size*0.12,5.5,size*0.07,1);c.fill();
  }
  // 3D手机
  c.fillStyle='#0a0a1e';c.beginPath();c.roundRect(size*0.52,-size*0.42,size*0.32,size*0.52,3);c.fill();
  let phoneG=c.createLinearGradient(size*0.52,-size*0.42,size*0.84,-size*0.42);
  phoneG.addColorStop(0,'rgba(255,255,255,0.15)');phoneG.addColorStop(1,'rgba(255,255,255,0)');
  c.fillStyle=phoneG;c.beginPath();c.roundRect(size*0.52,-size*0.42,size*0.32,size*0.52,3);c.fill();
  c.fillStyle='rgba(68,136,255,0.9)';c.beginPath();c.roundRect(size*0.55,-size*0.36,size*0.25,size*0.35,2);c.fill();
  c.fillStyle='rgba(255,255,255,0.3)';c.beginPath();c.moveTo(size*0.55,-size*0.36);c.lineTo(size*0.8,-size*0.36);c.lineTo(size*0.55,-size*0.16);c.closePath();c.fill();
  // 护盾特效
  if(shielded){
    let shieldA=0.5+Math.sin(anim*5)*0.25;
    // 六边形护盾
    c.strokeStyle='rgba(68,136,255,'+shieldA+')';c.lineWidth=4;
    c.shadowColor='rgba(68,136,255,0.8)';c.shadowBlur=16;
    c.beginPath();
    for(let i=0;i<6;i++){
      let a=i*Math.PI/3+anim*0.1;
      let r2=size+10;
      if(i===0)c.moveTo(Math.cos(a)*r2,Math.sin(a)*r2);
      else c.lineTo(Math.cos(a)*r2,Math.sin(a)*r2);
    }
    c.closePath();c.stroke();
    c.fillStyle='rgba(68,136,255,0.08)';c.beginPath();
    for(let i=0;i<6;i++){
      let a=i*Math.PI/3+anim*0.1;let r2=size+10;
      if(i===0)c.moveTo(Math.cos(a)*r2,Math.sin(a)*r2);
      else c.lineTo(Math.cos(a)*r2,Math.sin(a)*r2);
    }
    c.closePath();c.fill();
    c.shadowBlur=0;
  }
  // 名牌（玻璃感）
  c.font='bold 13px Microsoft YaHei,sans-serif';c.textAlign='center';
  let tw=c.measureText(bossName).width+24;
  let txL=-tw/2, tyL=-size-28;
  // 玻璃背景
  let tagG=c.createLinearGradient(txL,tyL,txL,tyL+22);
  tagG.addColorStop(0,'rgba(20,0,0,0.9)');tagG.addColorStop(1,'rgba(60,0,0,0.85)');
  c.fillStyle=tagG;c.beginPath();c.roundRect(txL,tyL,tw,22,5);c.fill();
  c.fillStyle='rgba(255,255,255,0.08)';c.beginPath();c.roundRect(txL,tyL,tw,10,5);c.fill();
  c.strokeStyle='rgba(255,68,68,0.6)';c.lineWidth=1.2;c.beginPath();c.roundRect(txL,tyL,tw,22,5);c.stroke();
  c.fillStyle='#ff7777';c.shadowColor='#ff4444';c.shadowBlur=6;
  c.fillText(bossName,0,-size-12);
  c.shadowBlur=0;
  // 血条（3D凸起感）
  let bw=size*2.4,bh=8;
  c.fillStyle='rgba(0,0,0,0.7)';c.beginPath();c.roundRect(-bw/2,size+12,bw,bh,4);c.fill();
  let hpRatio=hp/maxHp;
  let hpFill=bw*hpRatio;
  let hpColor=hpRatio>0.5?'#e74c3c':hpRatio>0.25?'#ff6600':'#ff0000';
  let hpGrad=c.createLinearGradient(-bw/2,size+12,-bw/2,size+12+bh);
  hpGrad.addColorStop(0,lightenColor(hpColor,40));
  hpGrad.addColorStop(0.4,hpColor);
  hpGrad.addColorStop(1,darkenColor(hpColor,30));
  c.fillStyle=hpGrad;
  c.shadowColor=hpColor;c.shadowBlur=6;
  c.beginPath();c.roundRect(-bw/2,size+12,Math.max(0,hpFill),bh,4);c.fill();
  c.shadowBlur=0;
  c.fillStyle='rgba(255,255,255,0.2)';
  c.beginPath();c.roundRect(-bw/2,size+12,Math.max(0,hpFill),bh*0.4,4);c.fill();
  c.restore();
}
'''

content = content[:boss_start_idx] + new_drawBoss + content[player_func_idx:]

# ============================================================
# 7. 替换 drawPlayer 函数 - 3D医生角色
# ============================================================
old_drawPlayer_start = 'function drawPlayer(c,x,y,size,hp,maxHp,invincible){'
player_func_idx2 = content.find(old_drawPlayer_start)
# 找到下一个顶级函数
next_func_idx = content.find('\n// ==================== START GAME ====================')
old_drawPlayer = content[player_func_idx2:next_func_idx]

new_drawPlayer = '''function drawPlayer(c,x,y,size,hp,maxHp,invincible){
  c.save();c.translate(x,y);
  let anim=Date.now()/200;
  if(invincible&&Math.floor(Date.now()/80)%2===0){c.globalAlpha=0.4}
  // 呼吸发光环
  let glowI=0.25+Math.sin(anim*2.2)*0.12;
  c.strokeStyle='rgba(52,152,219,'+glowI+')';c.lineWidth=3;
  c.shadowColor='#3498db';c.shadowBlur=18+Math.sin(anim*2)*5;
  c.beginPath();c.arc(0,0,size+5+Math.sin(anim*2)*1.5,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;
  // 白大褂3D球体
  draw3DSphere(c, 0, 0, size, '#ecf0f1', {
    gradStops:[
      [0,'#ffffff'],[0.3,'#f5f7f8'],[0.65,'#dde1e3'],[0.9,'#bfc3c7'],[1,'#9da2a6']
    ],
    glowColor:'#3498db', glowBlur:0, noShadow:true,
    lightX:-0.28, lightY:-0.32
  });
  // 大褂中线
  c.fillStyle='rgba(180,185,188,0.6)';
  c.beginPath();c.moveTo(-2,-size*0.95);c.lineTo(2,-size*0.95);c.lineTo(2,size*0.95);c.lineTo(-2,size*0.95);c.closePath();c.fill();
  // 领角
  let lapG=c.createLinearGradient(0,-size*0.3,0,size*0.4);
  lapG.addColorStop(0,'rgba(190,195,200,0.8)');lapG.addColorStop(1,'rgba(160,165,170,0.4)');
  c.fillStyle=lapG;
  c.beginPath();c.moveTo(-size*0.42,-size*0.32);c.lineTo(-2,size*0.2);c.lineTo(-size*0.5,size*0.4);c.closePath();c.fill();
  c.beginPath();c.moveTo(size*0.42,-size*0.32);c.lineTo(2,size*0.2);c.lineTo(size*0.5,size*0.4);c.closePath();c.fill();
  c.fillStyle='rgba(255,255,255,0.25)';
  c.beginPath();c.moveTo(-size*0.42,-size*0.32);c.lineTo(-size*0.2,-size*0.2);c.lineTo(-2,size*0.0);c.lineTo(-2,size*0.2);c.lineTo(-size*0.5,size*0.4);c.closePath();c.fill();
  // 手术帽（3D感）
  let capG=c.createRadialGradient(-size*0.2,-size*0.6,size*0.05,0,-size*0.15,size*0.75);
  capG.addColorStop(0,'#3dce78');capG.addColorStop(0.5,'#27ae60');capG.addColorStop(1,'#1a7a42');
  c.fillStyle=capG;c.beginPath();c.arc(0,-size*0.15,size*0.72,Math.PI,0);c.fill();
  c.fillStyle='rgba(255,255,255,0.2)';c.beginPath();c.arc(-size*0.2,-size*0.55,size*0.3,Math.PI,0);c.fill();
  // 帽沿
  let bandG=c.createLinearGradient(0,-size*0.2,0,-size*0.1);
  bandG.addColorStop(0,'#1a7a42');bandG.addColorStop(1,'#145c30');
  c.fillStyle=bandG;c.fillRect(-size*0.68,-size*0.2,size*1.36,size*0.09);
  c.fillStyle='rgba(255,255,255,0.15)';c.fillRect(-size*0.68,-size*0.2,size*1.36,size*0.03);
  // 脸（3D球面）
  let fG=c.createRadialGradient(-size*0.08,size*0.02,size*0.02,0,size*0.1,size*0.48);
  fG.addColorStop(0,'#fce4c0');fG.addColorStop(0.5,'#f0c898');fG.addColorStop(1,'#d4a070');
  c.fillStyle=fG;c.beginPath();c.arc(0,size*0.1,size*0.45,0,Math.PI*2);c.fill();
  c.fillStyle='rgba(255,255,255,0.2)';c.beginPath();c.arc(-size*0.1,size*0.0,size*0.2,0,Math.PI*2);c.fill();
  // 眼镜（金属感）
  let glassG=c.createLinearGradient(0,size*0.02,0,size*0.1);
  glassG.addColorStop(0,'#4a4a5a');glassG.addColorStop(1,'#2c2c3e');
  c.strokeStyle=glassG;c.lineWidth=2.2;
  c.beginPath();c.arc(-size*0.16,size*0.05,size*0.13,0,Math.PI*2);c.stroke();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.13,0,Math.PI*2);c.stroke();
  c.beginPath();c.moveTo(-size*0.03,size*0.05);c.lineTo(size*0.03,size*0.05);c.stroke();
  c.beginPath();c.moveTo(-size*0.29,size*0.05);c.lineTo(-size*0.35,size*0.02);c.stroke();
  c.beginPath();c.moveTo(size*0.29,size*0.05);c.lineTo(size*0.35,size*0.02);c.stroke();
  // 镜片折射
  c.fillStyle='rgba(100,180,255,0.18)';c.beginPath();c.arc(-size*0.16,size*0.05,size*0.11,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.11,0,Math.PI*2);c.fill();
  c.fillStyle='rgba(255,255,255,0.35)';c.beginPath();c.arc(-size*0.2,size*0.01,size*0.04,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.12,size*0.01,size*0.04,0,Math.PI*2);c.fill();
  // 瞳孔
  c.fillStyle='#1a1a2e';
  c.beginPath();c.arc(-size*0.16,size*0.05,size*0.045,0,Math.PI*2);c.fill();
  c.beginPath();c.arc(size*0.16,size*0.05,size*0.045,0,Math.PI*2);c.fill();
  // 微笑
  c.strokeStyle='#a05030';c.lineWidth=1.8;c.beginPath();c.arc(0,size*0.2,size*0.1,0.15,Math.PI-0.15);c.stroke();
  // 听诊器（3D曲线）
  c.strokeStyle='#2c3e50';c.lineWidth=3;
  c.shadowColor='rgba(0,0,0,0.3)';c.shadowBlur=3;
  c.beginPath();c.moveTo(-size*0.22,-size*0.05);c.quadraticCurveTo(-size*0.42,size*0.3,-size*0.16,size*0.52);c.stroke();
  c.beginPath();c.moveTo(size*0.22,-size*0.05);c.quadraticCurveTo(size*0.42,size*0.3,size*0.16,size*0.52);c.stroke();
  c.shadowBlur=0;
  // 听诊器头（3D金属）
  let sG=c.createRadialGradient(size*0.12,size*0.5,0,size*0.15,size*0.52,size*0.1);
  sG.addColorStop(0,'#e74c3c');sG.addColorStop(0.5,'#c0392b');sG.addColorStop(1,'#7b241c');
  c.fillStyle=sG;c.beginPath();c.arc(size*0.15,size*0.52,size*0.09,0,Math.PI*2);c.fill();
  c.fillStyle='rgba(255,255,255,0.4)';c.beginPath();c.arc(size*0.11,size*0.49,size*0.03,0,Math.PI*2);c.fill();
  // ID牌（玻璃感）
  let badgeG=c.createLinearGradient(-size*0.55,-size*0.16,-size*0.3,-size*0.16);
  badgeG.addColorStop(0,'rgba(255,255,255,0.88)');badgeG.addColorStop(1,'rgba(220,230,240,0.75)');
  c.fillStyle=badgeG;c.beginPath();c.roundRect(-size*0.56,-size*0.16,size*0.26,size*0.37,3);c.fill();
  c.fillStyle='rgba(255,255,255,0.4)';c.beginPath();c.roundRect(-size*0.56,-size*0.16,size*0.26,size*0.1,3);c.fill();
  c.strokeStyle='rgba(52,152,219,0.4)';c.lineWidth=0.8;c.beginPath();c.roundRect(-size*0.56,-size*0.16,size*0.26,size*0.37,3);c.stroke();
  // 牌子上的蓝条（医生标识）
  let blueG=c.createLinearGradient(-size*0.54,-size*0.14,-size*0.54,-size*0.08);
  blueG.addColorStop(0,'#5dade2');blueG.addColorStop(1,'#2980b9');
  c.fillStyle=blueG;c.fillRect(-size*0.54,-size*0.14,size*0.22,size*0.07);
  c.globalAlpha=1;
  c.restore();
}

'''

content = content[:player_func_idx2] + new_drawPlayer + content[player_func_idx2 + len(old_drawPlayer):]

print('角色替换完成')

# ============================================================
# 8. 升级 render 函数 - 背景3D地板 + 子弹3D + XP宝石3D
# ============================================================

# 8a. 背景渲染升级（3D透视地板效果）
old_bg = '''  // background
  let lv=G.levelData;
  ctx.fillStyle=lv.bgColor;ctx.fillRect(0,0,canvas.width,canvas.height);
  // grid
  ctx.strokeStyle=lv.gridColor;ctx.lineWidth=0.5;
  let gs=80,sx=-(cx%gs),sy=-(cy%gs);
  for(let x=sx;x<canvas.width;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke()}
  for(let y=sy;y<canvas.height;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke()}'''

new_bg = '''  // background - 3D地板效果
  let lv=G.levelData;
  // 深色渐变背景
  let bgGrad=ctx.createRadialGradient(canvas.width/2,canvas.height/2,0,canvas.width/2,canvas.height/2,Math.max(canvas.width,canvas.height)*0.8);
  let bgC1=lv.bgColor,bgC2=darkenColor(lv.bgColor.length===7?lv.bgColor:'#f0f0e8',25)||'#c8c8b8';
  bgGrad.addColorStop(0,bgC1);
  bgGrad.addColorStop(0.6,bgC2||bgC1);
  bgGrad.addColorStop(1,darkenColor(bgC2||bgC1,20)||bgC1);
  ctx.fillStyle=bgGrad;ctx.fillRect(0,0,canvas.width,canvas.height);
  // 主网格（瓷砖感）
  let gs=80,sx=-(cx%gs),sy=-(cy%gs);
  ctx.strokeStyle=lv.gridColor;ctx.lineWidth=0.7;
  for(let x=sx;x<canvas.width;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke()}
  for(let y=sy;y<canvas.height;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke()}
  // 瓷砖高光（每隔一块绘制高光角）
  let gs2=gs*2,sx2=-(cx%gs2),sy2=-(cy%gs2);
  ctx.fillStyle='rgba(255,255,255,0.04)';
  for(let tx=sx2;tx<canvas.width;tx+=gs2){
    for(let ty=sy2;ty<canvas.height;ty+=gs2){
      ctx.fillRect(tx,ty,gs,gs);
    }
  }
  // 大格子（区域感）
  let gs3=gs*5,sx3=-(cx%gs3),sy3=-(cy%gs3);
  ctx.strokeStyle='rgba(0,0,0,0.06)';ctx.lineWidth=1.5;
  for(let x=sx3;x<canvas.width;x+=gs3){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke()}
  for(let y=sy3;y<canvas.height;y+=gs3){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke()}'''

content = content.replace(old_bg, new_bg)

# 8b. XP 球升级为3D宝石
old_xp = '''  // XP orbs (beautified)
  for(let o of G.xpOrbs){
    let ox=o.x-cx,oy=o.y-cy;
    if(ox<-20||ox>canvas.width+20||oy<-20||oy>canvas.height+20)continue;
    let pulse=0.6+Math.sin(Date.now()/250+o.x*0.1)*0.35;
    // glow
    ctx.shadowColor=\'#2ecc71\';ctx.shadowBlur=8;
    ctx.globalAlpha=pulse*0.5;ctx.fillStyle=\'#2ecc71\';
    ctx.beginPath();ctx.arc(ox,oy,o.size+3,0,Math.PI*2);ctx.fill();
    // main orb
    ctx.globalAlpha=pulse;ctx.fillStyle=\'#44ff88\';
    ctx.beginPath();ctx.arc(ox,oy,o.size,0,Math.PI*2);ctx.fill();
    // inner highlight
    ctx.globalAlpha=pulse*0.8;ctx.fillStyle=\'#aaffcc\';
    ctx.beginPath();ctx.arc(ox-o.size*0.2,oy-o.size*0.2,o.size*0.35,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
  }'''

new_xp = '''  // XP orbs - 3D发光宝石
  for(let o of G.xpOrbs){
    let ox=o.x-cx,oy=o.y-cy;
    if(ox<-20||ox>canvas.width+20||oy<-20||oy>canvas.height+20)continue;
    let pulse=0.65+Math.sin(Date.now()/220+o.x*0.09)*0.32;
    let r=o.size;
    // 外层大光晕
    ctx.globalAlpha=0.18*pulse;
    ctx.fillStyle='#2ecc71';
    ctx.shadowColor='#2ecc71';ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(ox,oy,r*2.2,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
    // 3D 宝石主体
    draw3DSphere(ctx, ox, oy, r, '#2ecc71', {
      gradStops:[
        [0,'#88ffcc'],[0.3,'#2ecc71'],[0.65,'#1a8f50'],[1,'#0a3020']
      ],
      glowColor:'#2ecc71', glowBlur:8*pulse,
      lightX:-0.3, lightY:-0.35
    });
    // 宝石切面反光
    ctx.globalAlpha=0.6*pulse;
    ctx.fillStyle='rgba(200,255,230,0.7)';
    ctx.beginPath();
    ctx.moveTo(ox,oy-r*0.8);
    ctx.lineTo(ox+r*0.6,oy);
    ctx.lineTo(ox,oy+r*0.2);
    ctx.lineTo(ox-r*0.6,oy);
    ctx.closePath();
    ctx.fill();
    ctx.globalAlpha=1;
  }'''

content = content.replace(old_xp, new_xp)

# 8c. 子弹升级为3D金属球
old_proj = '''  // projectiles
  for(let pr of G.projectiles){
    let px=pr.x-cx,py=pr.y-cy;
    if(px<-20||px>canvas.width+20||py<-20||py>canvas.height+20)continue;
    ctx.fillStyle=pr.color;
    if(pr.aoe){
      ctx.globalAlpha=0.3;ctx.beginPath();ctx.arc(px,py,pr.aoeSize/2,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
      ctx.beginPath();ctx.arc(px,py,pr.size,0,Math.PI*2);ctx.fill();
    }else if(pr.isEnemy){
      ctx.fillStyle=pr.color||\'#ff4444\';ctx.beginPath();ctx.arc(px,py,pr.size,0,Math.PI*2);ctx.fill();
      ctx.fillStyle=\'#ff8888\';ctx.beginPath();ctx.arc(px,py,pr.size*0.5,0,Math.PI*2);ctx.fill();
    }else{
      ctx.shadowColor=pr.color;ctx.shadowBlur=8;
      ctx.beginPath();ctx.arc(px,py,pr.size,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;
      // trail
      ctx.globalAlpha=0.3;ctx.beginPath();ctx.arc(px-pr.vx*1.5,py-pr.vy*1.5,pr.size*0.6,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
    }
  }'''

new_proj = '''  // projectiles - 3D金属球体
  for(let pr of G.projectiles){
    let px=pr.x-cx,py=pr.y-cy;
    if(px<-20||px>canvas.width+20||py<-20||py>canvas.height+20)continue;
    if(pr.aoe){
      // AOE脉冲环
      ctx.globalAlpha=0.2;
      ctx.fillStyle=pr.color;
      ctx.shadowColor=pr.color;ctx.shadowBlur=20;
      ctx.beginPath();ctx.arc(px,py,pr.aoeSize/2,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;ctx.globalAlpha=1;
      draw3DSphere(ctx,px,py,pr.size,pr.color,{noShadow:true,glowColor:pr.color,glowBlur:6});
    }else if(pr.isEnemy){
      // 敌方弹幕 - 红色警告球
      draw3DSphere(ctx,px,py,pr.size,pr.color||'#ff4444',{
        gradStops:[[0,'#ff9999'],[0.4,pr.color||'#ff4444'],[1,'#440000']],
        glowColor:'#ff0000',glowBlur:8,noShadow:true
      });
    }else{
      // 玩家子弹 - 彩色3D球+尾迹
      let trailAlpha=0.25;
      // 尾迹（多段渐隐）
      for(let t=1;t<=3;t++){
        ctx.globalAlpha=trailAlpha*(1-t*0.28);
        ctx.fillStyle=pr.color;
        ctx.shadowColor=pr.color;ctx.shadowBlur=4;
        ctx.beginPath();ctx.arc(px-pr.vx*t*1.2,py-pr.vy*t*1.2,pr.size*(1-t*0.22),0,Math.PI*2);ctx.fill();
        ctx.shadowBlur=0;
      }
      ctx.globalAlpha=1;
      // 主弹体3D球
      draw3DSphere(ctx,px,py,pr.size,pr.color,{noShadow:true,glowColor:pr.color,glowBlur:10});
    }
  }'''

content = content.replace(old_proj, new_proj)

# 8d. 轨道武器（铅衣护盾）升级
old_orbital = '''  // orbitals
  for(let o of G.orbitals){
    let ox=p.x+Math.cos(o.angle)*o.dist-cx;
    let oy=p.y+Math.sin(o.angle)*o.dist-cy;
    ctx.fillStyle=o.color;ctx.shadowColor=o.color;ctx.shadowBlur=6;
    ctx.beginPath();ctx.arc(ox,oy,o.size,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  }'''

new_orbital = '''  // orbitals - 3D护盾球
  for(let o of G.orbitals){
    let ox=p.x+Math.cos(o.angle)*o.dist-cx;
    let oy=p.y+Math.sin(o.angle)*o.dist-cy;
    // 轨道连线
    ctx.strokeStyle='rgba(127,140,141,0.2)';ctx.lineWidth=1;ctx.setLineDash([3,5]);
    ctx.beginPath();ctx.moveTo(p.x-cx,p.y-cy);ctx.lineTo(ox,oy);ctx.stroke();
    ctx.setLineDash([]);
    draw3DSphere(ctx,ox,oy,o.size,'#7f8c8d',{
      gradStops:[[0,'#bdc3c7'],[0.35,'#95a5a6'],[0.7,'#5d6d7e'],[1,'#1c2833']],
      glowColor:o.color,glowBlur:8,noShadow:true
    });
  }'''

content = content.replace(old_orbital, new_orbital)

# 8e. 粒子升级（有深度感的菱形/星形）
old_particles = '''  // particles
  for(let pt of G.particles){
    let ptx=pt.x-cx,pty=pt.y-cy;
    ctx.globalAlpha=pt.life/pt.maxLife;ctx.fillStyle=pt.color;
    ctx.beginPath();ctx.arc(ptx,pty,pt.size*(pt.life/pt.maxLife),0,Math.PI*2);ctx.fill();
  }
  ctx.globalAlpha=1;'''

new_particles = '''  // particles - 3D深度感粒子
  for(let pt of G.particles){
    let ptx=pt.x-cx,pty=pt.y-cy;
    let a=pt.life/pt.maxLife;
    let r=pt.size*a;
    if(r<0.3)continue;
    ctx.globalAlpha=a;
    // 大粒子用3D球，小的用菱形
    if(pt.size>4){
      ctx.shadowColor=pt.color;ctx.shadowBlur=4*a;
      draw3DSphere(ctx,ptx,pty,r,pt.color,{noShadow:true});
      ctx.shadowBlur=0;
    }else{
      // 菱形粒子（快速绘制）
      ctx.fillStyle=pt.color;
      ctx.shadowColor=pt.color;ctx.shadowBlur=3*a;
      ctx.beginPath();
      ctx.moveTo(ptx,pty-r);ctx.lineTo(ptx+r*0.7,pty);
      ctx.lineTo(ptx,pty+r);ctx.lineTo(ptx-r*0.7,pty);
      ctx.closePath();ctx.fill();
      // 高光
      ctx.fillStyle='rgba(255,255,255,'+(0.4*a)+')';
      ctx.beginPath();ctx.arc(ptx-r*0.2,pty-r*0.3,r*0.25,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;
    }
  }
  ctx.globalAlpha=1;'''

content = content.replace(old_particles, new_particles)

# 8f. 伤害数字升级（3D立体感）
old_dmgtxt = '''  // damage texts
  for(let t of G.damageTexts){
    let tx=t.x-cx,ty=t.y-cy;
    ctx.globalAlpha=t.life/t.maxLife;ctx.fillStyle=t.color;
    ctx.font=\'bold \'+(t.text.includes(\'!\')? \'18\':\'14\')+\'px sans-serif\';ctx.textAlign=\'center\';
    ctx.fillText(t.text,tx,ty);
  }
  ctx.globalAlpha=1;'''

new_dmgtxt = '''  // damage texts - 3D立体数字
  for(let t of G.damageTexts){
    let tx=t.x-cx,ty=t.y-cy;
    let a=t.life/t.maxLife;
    let isBig=t.text.includes('!');
    let fs=isBig?20:15;
    let scale=isBig?(1.2+0.3*(1-a)):1;
    ctx.save();
    ctx.translate(tx,ty);ctx.scale(scale,scale);
    ctx.globalAlpha=a;
    ctx.font='bold '+fs+'px "Segoe UI",sans-serif';ctx.textAlign='center';
    // 阴影层（3D感）
    ctx.fillStyle='rgba(0,0,0,0.6)';
    ctx.fillText(t.text,2,2);
    // 主文字
    ctx.fillStyle=t.color;
    ctx.shadowColor=t.color;ctx.shadowBlur=isBig?12:6;
    ctx.fillText(t.text,0,0);
    // 高光（亮色顶部）
    ctx.fillStyle='rgba(255,255,255,0.35)';
    ctx.shadowBlur=0;
    ctx.fillText(t.text,0,-1);
    ctx.restore();
  }
  ctx.globalAlpha=1;'''

content = content.replace(old_dmgtxt, new_dmgtxt)

# 8g. 闪电效果升级
old_lightning = '''  // lightnings
  for(let l of G.lightnings){
    ctx.globalAlpha=l.life/300;ctx.strokeStyle=\'#fff\';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(l.x1-cx,l.y1-cy);
    let mx=(l.x1+l.x2)/2+rand(-20,20),my=(l.y1+l.y2)/2+rand(-20,20);
    ctx.lineTo(mx-cx,my-cy);ctx.lineTo(l.x2-cx,l.y2-cy);ctx.stroke();
  }
  ctx.globalAlpha=1;'''

new_lightning = '''  // lightnings - 3层发光
  for(let l of G.lightnings){
    let la=l.life/300;
    let mx=(l.x1+l.x2)/2+rand(-20,20),my=(l.y1+l.y2)/2+rand(-20,20);
    // 外层宽光晕
    ctx.globalAlpha=la*0.3;ctx.strokeStyle='rgba(100,180,255,0.6)';ctx.lineWidth=8;
    ctx.shadowColor='#4af';ctx.shadowBlur=15;
    ctx.beginPath();ctx.moveTo(l.x1-cx,l.y1-cy);ctx.lineTo(mx-cx,my-cy);ctx.lineTo(l.x2-cx,l.y2-cy);ctx.stroke();
    // 中层
    ctx.globalAlpha=la*0.7;ctx.strokeStyle='rgba(150,220,255,0.8)';ctx.lineWidth=3;ctx.shadowBlur=8;
    ctx.beginPath();ctx.moveTo(l.x1-cx,l.y1-cy);ctx.lineTo(mx-cx,my-cy);ctx.lineTo(l.x2-cx,l.y2-cy);ctx.stroke();
    // 内层白芯
    ctx.globalAlpha=la;ctx.strokeStyle='#ffffff';ctx.lineWidth=1.5;ctx.shadowBlur=4;
    ctx.beginPath();ctx.moveTo(l.x1-cx,l.y1-cy);ctx.lineTo(mx-cx,my-cy);ctx.lineTo(l.x2-cx,l.y2-cy);ctx.stroke();
    ctx.shadowBlur=0;
  }
  ctx.globalAlpha=1;'''

content = content.replace(old_lightning, new_lightning)

# ============================================================
# 9. 地图边界升级（3D厚度感）
# ============================================================
old_border = '''  // map border
  ctx.strokeStyle=lv.wallColor;ctx.lineWidth=4;
  ctx.strokeRect(-cx,-cy,G.mapSize,G.mapSize);'''

new_border = '''  // map border - 3D厚壁
  // 外墙厚度阴影
  ctx.fillStyle='rgba(0,0,0,0.3)';
  ctx.fillRect(-cx-8,-cy-8,G.mapSize+16,8); // 上
  ctx.fillRect(-cx-8,-cy-8,8,G.mapSize+16); // 左
  ctx.fillRect(-cx,-cy+G.mapSize,G.mapSize+8,8); // 下
  ctx.fillRect(-cx+G.mapSize,-cy,8,G.mapSize+8); // 右
  // 主墙壁
  ctx.strokeStyle=lv.wallColor;ctx.lineWidth=6;
  ctx.shadowColor='rgba(0,0,0,0.5)';ctx.shadowBlur=8;
  ctx.strokeRect(-cx,-cy,G.mapSize,G.mapSize);
  ctx.shadowBlur=0;
  // 内侧高光
  ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=2;
  ctx.strokeRect(-cx+3,-cy+3,G.mapSize-6,G.mapSize-6);'''

content = content.replace(old_border, new_border)

# ============================================================
# 10. 摇杆升级（3D质感）
# ============================================================
old_joystick = '''  // joystick
  if(touch.active){
    ctx.globalAlpha=0.3;ctx.fillStyle=\'#fff\';
    ctx.beginPath();ctx.arc(touch.sx,touch.sy,50,0,Math.PI*2);ctx.fill();
    ctx.globalAlpha=0.6;ctx.fillStyle=\'#3498db\';
    ctx.beginPath();ctx.arc(touch.sx+touch.dx*50,touch.sy+touch.dy*50,22,0,Math.PI*2);ctx.fill();
    ctx.globalAlpha=1;
  }'''

new_joystick = '''  // joystick - 3D质感
  if(touch.active){
    // 底座
    let jbG=ctx.createRadialGradient(touch.sx,touch.sy,0,touch.sx,touch.sy,50);
    jbG.addColorStop(0,'rgba(255,255,255,0.12)');jbG.addColorStop(1,'rgba(255,255,255,0.02)');
    ctx.fillStyle=jbG;ctx.beginPath();ctx.arc(touch.sx,touch.sy,50,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.25)';ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(touch.sx,touch.sy,50,0,Math.PI*2);ctx.stroke();
    // 圆心十字
    ctx.strokeStyle='rgba(255,255,255,0.15)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(touch.sx-20,touch.sy);ctx.lineTo(touch.sx+20,touch.sy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(touch.sx,touch.sy-20);ctx.lineTo(touch.sx,touch.sy+20);ctx.stroke();
    // 3D摇杆球
    let jx=touch.sx+touch.dx*50, jy=touch.sy+touch.dy*50;
    draw3DSphere(ctx,jx,jy,22,'#3498db',{
      gradStops:[[0,'#74b9ff'],[0.4,'#3498db'],[0.8,'#1a5276'],[1,'#0a2030']],
      glowColor:'rgba(52,152,219,0.5)',glowBlur:8,noShadow:true
    });
  }'''

content = content.replace(old_joystick, new_joystick)

# ============================================================
# 11. 小地图升级（3D立体感）
# ============================================================
old_minimap = '''function drawMinimap(){
  let ms=120,mScale=ms/G.mapSize;
  mmCtx.fillStyle=\'rgba(0,0,0,0.8)\';mmCtx.fillRect(0,0,ms,ms);
  // map border on minimap
  mmCtx.strokeStyle=\'rgba(255,255,255,0.15)\';mmCtx.lineWidth=1;mmCtx.strokeRect(0,0,ms,ms);
  // enemies (color coded)
  for(let e of G.enemies){
    mmCtx.fillStyle=e.isBoss?\'#ff0000\':e.elite?\'#ff8800\':\'#ff4444\';
    let s=e.isBoss?4:e.elite?3:2;
    mmCtx.beginPath();mmCtx.arc(e.x*mScale,e.y*mScale,s,0,Math.PI*2);mmCtx.fill();
  }
  // xp orbs
  mmCtx.fillStyle=\'rgba(46,204,113,0.6)\';
  for(let o of G.xpOrbs){mmCtx.fillRect(o.x*mScale,o.y*mScale,1,1)}
  // player (pulsing)
  let pPulse=0.7+Math.sin(Date.now()/300)*0.3;
  mmCtx.fillStyle=\'#ffdd44\';
  mmCtx.shadowColor=\'#ffdd44\';mmCtx.shadowBlur=4;
  mmCtx.beginPath();mmCtx.arc(G.player.x*mScale,G.player.y*mScale,3,0,Math.PI*2);mmCtx.fill();
  mmCtx.shadowBlur=0;
  // viewport
  mmCtx.strokeStyle=\'rgba(255,255,255,\'+pPulse+\')\';mmCtx.lineWidth=1;
  mmCtx.strokeRect(G.camera.x*mScale,G.camera.y*mScale,canvas.width*mScale,canvas.height*mScale);
  // border
  mmCtx.strokeStyle=\'rgba(255,255,255,0.25)\';mmCtx.lineWidth=2;mmCtx.strokeRect(0,0,ms,ms);
}'''

new_minimap = '''function drawMinimap(){
  let ms=120,mScale=ms/G.mapSize;
  // 3D玻璃背景
  let mmBG=mmCtx.createRadialGradient(ms/2,ms/2,0,ms/2,ms/2,ms*0.8);
  mmBG.addColorStop(0,'rgba(10,10,30,0.85)');
  mmBG.addColorStop(1,'rgba(0,0,5,0.92)');
  mmCtx.fillStyle=mmBG;mmCtx.fillRect(0,0,ms,ms);
  // 网格
  mmCtx.strokeStyle='rgba(255,255,255,0.04)';mmCtx.lineWidth=0.5;
  for(let i=10;i<ms;i+=10){
    mmCtx.beginPath();mmCtx.moveTo(i,0);mmCtx.lineTo(i,ms);mmCtx.stroke();
    mmCtx.beginPath();mmCtx.moveTo(0,i);mmCtx.lineTo(ms,i);mmCtx.stroke();
  }
  // enemies (3D点)
  for(let e of G.enemies){
    let ex=e.x*mScale, ey=e.y*mScale;
    if(e.isBoss){
      mmCtx.fillStyle='#ff2200';mmCtx.shadowColor='#ff0000';mmCtx.shadowBlur=6;
      mmCtx.beginPath();mmCtx.arc(ex,ey,4.5,0,Math.PI*2);mmCtx.fill();
      mmCtx.fillStyle='#ff8866';mmCtx.shadowBlur=0;
      mmCtx.beginPath();mmCtx.arc(ex-1,ey-1,2,0,Math.PI*2);mmCtx.fill();
    }else{
      let ec=e.elite?'#ff8800':'#ff5555';
      mmCtx.fillStyle=ec;mmCtx.shadowColor=ec;mmCtx.shadowBlur=3;
      let s=e.elite?3:2;
      mmCtx.beginPath();mmCtx.arc(ex,ey,s,0,Math.PI*2);mmCtx.fill();
      mmCtx.shadowBlur=0;
    }
  }
  // xp orbs
  mmCtx.fillStyle='rgba(46,204,113,0.7)';mmCtx.shadowColor='#2ecc71';mmCtx.shadowBlur=2;
  for(let o of G.xpOrbs){mmCtx.fillRect(o.x*mScale,o.y*mScale,1.5,1.5)}
  mmCtx.shadowBlur=0;
  // 玩家（3D发光）
  let pPulse=0.7+Math.sin(Date.now()/300)*0.3;
  let px=G.player.x*mScale, py=G.player.y*mScale;
  mmCtx.fillStyle='rgba(255,220,50,0.2)';mmCtx.beginPath();mmCtx.arc(px,py,6,0,Math.PI*2);mmCtx.fill();
  mmCtx.fillStyle='#ffdd44';mmCtx.shadowColor='#ffcc00';mmCtx.shadowBlur=8*pPulse;
  mmCtx.beginPath();mmCtx.arc(px,py,3.5,0,Math.PI*2);mmCtx.fill();
  mmCtx.fillStyle='rgba(255,255,200,0.8)';mmCtx.shadowBlur=0;
  mmCtx.beginPath();mmCtx.arc(px-1,py-1,1.2,0,Math.PI*2);mmCtx.fill();
  // 视口
  mmCtx.strokeStyle='rgba(255,255,255,'+(pPulse*0.4)+')';mmCtx.lineWidth=1;
  mmCtx.setLineDash([3,3]);
  mmCtx.strokeRect(G.camera.x*mScale,G.camera.y*mScale,canvas.width*mScale,canvas.height*mScale);
  mmCtx.setLineDash([]);
  // 外边框（3D斜切感）
  let mmEdge=mmCtx.createLinearGradient(0,0,ms,ms);
  mmEdge.addColorStop(0,'rgba(255,255,255,0.3)');
  mmEdge.addColorStop(0.5,'rgba(255,255,255,0.1)');
  mmEdge.addColorStop(1,'rgba(255,255,255,0.05)');
  mmCtx.strokeStyle=mmEdge;mmCtx.lineWidth=2;mmCtx.strokeRect(0,0,ms,ms);
}'''

content = content.replace(old_minimap, new_minimap)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ 3D全面升级完成！')
print('升级内容：')
print('  1. CSS 全面3D玻璃质感UI')
print('  2. draw3DSphere() 通用3D球体函数')
print('  3. drawPatient() 3D球体敌人')
print('  4. drawBoss() 全3D超级Boss（双光环+六边形护盾）')
print('  5. drawPlayer() 3D医生角色（白大褂/听诊器/ID牌）')
print('  6. 背景3D透视地板（瓷砖高光）')
print('  7. XP球 → 3D发光宝石（切面反光）')
print('  8. 子弹 → 3D金属球+多段尾迹')
print('  9. 粒子 → 3D球+菱形深度感粒子')
print('  10. 伤害数字 → 3D立体文字')
print('  11. 闪电 → 3层发光效果')
print('  12. 地图边界 → 3D厚壁')
print('  13. 摇杆 → 3D球体质感')
print('  14. 小地图 → 3D玻璃面板')
