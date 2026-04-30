#!/usr/bin/env python3
"""
upgrade_3d_humanoid.py — 将"发不出绩效的医院"从渐变球体升级为3D骨骼人形
所有角色将拥有：头部、躯干、双臂（上臂+前臂）、双腿（大腿+小腿）
通过sin/cos驱动的关节角度实现行走动画
"""
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. 在 "3D RENDERING HELPERS" 段落前插入骨骼人形系统
# ============================================================
humanoid_system = '''
// ==================== 3D SKELETAL HUMANOID SYSTEM ====================
// 通用3D人形绘制 — 骨骼动画驱动，所有角色共用
// 骨骼：head, neck, torso, upperArmL/R, foreArmL/R, upperLegL/R, lowerLegL/R

function drawLimb(c, x1, y1, x2, y2, thickness, color, highlight) {
  // 绘制3D肢体（带渐变圆角效果）
  let dx = x2 - x1, dy = y2 - y1;
  let len = Math.hypot(dx, dy);
  if (len < 1) return;
  let angle = Math.atan2(dy, dx);
  c.save();
  c.translate(x1, y1);
  c.rotate(angle);
  // 主体（线性渐变模拟圆柱体3D感）
  let r = thickness / 2;
  let grad = c.createLinearGradient(0, -r, 0, r);
  grad.addColorStop(0, highlight || lightenColor(color, 50));
  grad.addColorStop(0.3, color);
  grad.addColorStop(0.7, darkenColor(color, 30));
  grad.addColorStop(1, darkenColor(color, 60));
  c.fillStyle = grad;
  c.beginPath();
  c.moveTo(r, 0);
  c.lineTo(len - r, 0);
  c.arc(len - r, 0, r, 0, Math.PI);
  c.lineTo(r, r);
  c.arc(r, 0, r, Math.PI, 0);
  c.closePath();
  c.fill();
  // 高光条
  c.fillStyle = 'rgba(255,255,255,0.18)';
  c.beginPath();
  c.moveTo(r, -r * 0.4);
  c.lineTo(len - r, -r * 0.4);
  c.lineTo(len - r, -r * 0.1);
  c.lineTo(r, -r * 0.1);
  c.closePath();
  c.fill();
  c.restore();
}

function walkCycle(t, speed) {
  // 返回行走周期各关节角度（弧度）
  // t: 时间(秒), speed: 速度倍率
  let phase = t * speed * 6;
  return {
    upperArmL: Math.sin(phase) * 0.6,
    foreArmL: -0.3 + Math.sin(phase + 0.5) * 0.4,
    upperArmR: Math.sin(phase + Math.PI) * 0.6,
    foreArmR: -0.3 + Math.sin(phase + Math.PI + 0.5) * 0.4,
    upperLegL: Math.sin(phase + Math.PI) * 0.5,
    lowerLegL: Math.max(0, Math.sin(phase + Math.PI + 0.8)) * 0.7,
    upperLegR: Math.sin(phase) * 0.5,
    lowerLegR: Math.max(0, Math.sin(phase + 0.8)) * 0.7,
    bodyBob: Math.abs(Math.sin(phase * 2)) * 2,  // 身体上下弹跳
    bodyTilt: Math.sin(phase) * 0.03  // 身体微倾
  };
}

function idleCycle(t) {
  // 静止站立时的呼吸动画
  let phase = t * 1.5;
  return {
    upperArmL: 0.05 + Math.sin(phase) * 0.03,
    foreArmL: -0.2,
    upperArmR: -0.05 + Math.sin(phase + 1) * 0.03,
    foreArmR: -0.2,
    upperLegL: 0,
    lowerLegL: 0,
    upperLegR: 0,
    lowerLegR: 0,
    bodyBob: Math.sin(phase * 2) * 1,
    bodyTilt: 0
  };
}

function drawHumanoid(c, x, y, scale, bones, opts) {
  // 通用3D骨骼人形绘制
  // opts: { skinColor, shirtColor, pantsColor, shoeColor, headRadius, torsoH, torsoW,
  //         upperArmLen, foreArmLen, upperLegLen, lowerLegLen,
  //         upperArmW, foreArmW, upperLegW, lowerLegW,
  //         headExtra, bodyExtra, drawFace, faceType, moving, isMoving }
  opts = opts || {};
  let skin = opts.skinColor || '#f0c898';
  let shirt = opts.shirtColor || '#3498db';
  let pants = opts.pantsColor || '#2c3e50';
  let shoe = opts.shoeColor || '#1a1a2e';

  // 比例参数（相对于scale）
  let headR = (opts.headRadius || 0.38) * scale;
  let torsoH = (opts.torsoH || 0.65) * scale;
  let torsoW = (opts.torsoW || 0.5) * scale;
  let uaLen = (opts.upperArmLen || 0.38) * scale;
  let faLen = (opts.foreArmLen || 0.35) * scale;
  let ulLen = (opts.upperLegLen || 0.45) * scale;
  let llLen = (opts.lowerLegLen || 0.4) * scale;
  let uaW = (opts.upperArmW || 0.14) * scale;
  let faW = (opts.foreArmW || 0.11) * scale;
  let ulW = (opts.upperLegW || 0.18) * scale;
  let llW = (opts.lowerLegW || 0.14) * scale;
  let neckLen = scale * 0.1;

  c.save();
  c.translate(x, y + (bones.bodyBob || 0));
  c.rotate(bones.bodyTilt || 0);

  // 关键位置
  let neckX = 0, neckY = -torsoH / 2 + neckLen;
  let headX = neckX, headY = neckY - headR - 2;
  let shoulderY = neckY;
  let hipY = torsoH / 2;
  let shoulderW = torsoW * 0.85;

  // === 后面的手臂（先画，被身体遮挡） ===
  // 左上臂
  let luaAngle = -Math.PI/2 + bones.upperArmL;
  let luaEndX = -shoulderW + Math.cos(luaAngle) * uaLen;
  let luaEndY = shoulderY + Math.sin(luaAngle) * uaLen;
  drawLimb(c, -shoulderW, shoulderY, luaEndX, luaEndY, uaW, shirt, lightenColor(shirt, 40));
  // 左前臂
  let lfaAngle = luaAngle + bones.foreArmL;
  let lfaEndX = luaEndX + Math.cos(lfaAngle) * faLen;
  let lfaEndY = luaEndY + Math.sin(lfaAngle) * faLen;
  drawLimb(c, luaEndX, luaEndY, lfaEndX, lfaEndY, faW, skin, lightenColor(skin, 40));
  // 左手（小圆球）
  let handGrad = c.createRadialGradient(lfaEndX - 1, lfaEndY - 1, 0, lfaEndX, lfaEndY, faW * 0.5);
  handGrad.addColorStop(0, lightenColor(skin, 30));
  handGrad.addColorStop(1, darkenColor(skin, 20));
  c.fillStyle = handGrad;
  c.beginPath(); c.arc(lfaEndX, lfaEndY, faW * 0.45, 0, Math.PI * 2); c.fill();

  // === 后面的腿 ===
  // 左大腿
  let lulAngle = Math.PI/2 + bones.upperLegL;
  let lulEndX = -torsoW * 0.3 + Math.cos(lulAngle) * ulLen;
  let lulEndY = hipY + Math.sin(lulAngle) * ulLen;
  drawLimb(c, -torsoW * 0.3, hipY, lulEndX, lulEndY, ulW, pants, lightenColor(pants, 30));
  // 左小腿
  let lllAngle = lulAngle + bones.lowerLegL;
  let lllEndX = lulEndX + Math.cos(lllAngle) * llLen;
  let lllEndY = lulEndY + Math.sin(lllAngle) * llLen;
  drawLimb(c, lulEndX, lulEndY, lllEndX, lllEndY, llW, pants, lightenColor(pants, 20));
  // 左脚（椭圆）
  c.fillStyle = shoe;
  c.beginPath(); c.ellipse(lllEndX + 3, lllEndY, llW * 0.7, llW * 0.4, 0.2, 0, Math.PI * 2); c.fill();
  c.fillStyle = 'rgba(255,255,255,0.15)';
  c.beginPath(); c.ellipse(lllEndX + 2, lllEndY - 1, llW * 0.4, llW * 0.2, 0.2, 0, Math.PI * 2); c.fill();

  // === 躯干（3D立体感） ===
  // 身体主形状（圆角矩形渐变）
  let bodyGrad = c.createLinearGradient(-torsoW, 0, torsoW, 0);
  bodyGrad.addColorStop(0, darkenColor(shirt, 40));
  bodyGrad.addColorStop(0.2, shirt);
  bodyGrad.addColorStop(0.45, lightenColor(shirt, 30));
  bodyGrad.addColorStop(0.55, lightenColor(shirt, 30));
  bodyGrad.addColorStop(0.8, shirt);
  bodyGrad.addColorStop(1, darkenColor(shirt, 40));
  c.fillStyle = bodyGrad;
  c.beginPath();
  let bodyTop = neckY - 2, bodyBot = hipY;
  let bw = torsoW, br = torsoW * 0.25;
  c.moveTo(-bw + br, bodyTop);
  c.lineTo(bw - br, bodyTop);
  c.quadraticCurveTo(bw, bodyTop, bw, bodyTop + br);
  c.lineTo(bw, bodyBot - br);
  c.quadraticCurveTo(bw, bodyBot, bw - br, bodyBot);
  c.lineTo(-bw + br, bodyBot);
  c.quadraticCurveTo(-bw, bodyBot, -bw, bodyBot - br);
  c.lineTo(-bw, bodyTop + br);
  c.quadraticCurveTo(-bw, bodyTop, -bw + br, bodyTop);
  c.closePath();
  c.fill();
  // 身体中线
  c.strokeStyle = darkenColor(shirt, 20);
  c.lineWidth = 1;
  c.globalAlpha = 0.3;
  c.beginPath(); c.moveTo(0, bodyTop + 3); c.lineTo(0, bodyBot - 2); c.stroke();
  c.globalAlpha = 1;
  // 身体高光
  c.fillStyle = 'rgba(255,255,255,0.1)';
  c.beginPath();
  c.moveTo(-bw * 0.6 + br, bodyTop);
  c.lineTo(-bw * 0.1, bodyTop);
  c.lineTo(-bw * 0.1, bodyBot - br);
  c.lineTo(-bw * 0.6 + br, bodyBot);
  c.quadraticCurveTo(-bw * 0.6, bodyBot, -bw * 0.6, bodyBot - br);
  c.lineTo(-bw * 0.6, bodyTop + br);
  c.quadraticCurveTo(-bw * 0.6, bodyTop, -bw * 0.6 + br, bodyTop);
  c.closePath();
  c.fill();

  // === 前面的手臂 ===
  // 右上臂
  let ruaAngle = -Math.PI/2 + bones.upperArmR;
  let ruaEndX = shoulderW + Math.cos(ruaAngle) * uaLen;
  let ruaEndY = shoulderY + Math.sin(ruaAngle) * uaLen;
  drawLimb(c, shoulderW, shoulderY, ruaEndX, ruaEndY, uaW, shirt, lightenColor(shirt, 40));
  // 右前臂
  let rfaAngle = ruaAngle + bones.foreArmR;
  let rfaEndX = ruaEndX + Math.cos(rfaAngle) * faLen;
  let rfaEndY = ruaEndY + Math.sin(rfaAngle) * faLen;
  drawLimb(c, ruaEndX, ruaEndY, rfaEndX, rfaEndY, faW, skin, lightenColor(skin, 40));
  // 右手
  let handGrad2 = c.createRadialGradient(rfaEndX - 1, rfaEndY - 1, 0, rfaEndX, rfaEndY, faW * 0.5);
  handGrad2.addColorStop(0, lightenColor(skin, 30));
  handGrad2.addColorStop(1, darkenColor(skin, 20));
  c.fillStyle = handGrad2;
  c.beginPath(); c.arc(rfaEndX, rfaEndY, faW * 0.45, 0, Math.PI * 2); c.fill();

  // === 前面的腿 ===
  // 右大腿
  let rulAngle = Math.PI/2 + bones.upperLegR;
  let rulEndX = torsoW * 0.3 + Math.cos(rulAngle) * ulLen;
  let rulEndY = hipY + Math.sin(rulAngle) * ulLen;
  drawLimb(c, torsoW * 0.3, hipY, rulEndX, rulEndY, ulW, pants, lightenColor(pants, 30));
  // 右小腿
  let rllAngle = rulAngle + bones.lowerLegR;
  let rllEndX = rulEndX + Math.cos(rllAngle) * llLen;
  let rllEndY = rulEndY + Math.sin(rllAngle) * llLen;
  drawLimb(c, rulEndX, rulEndY, rllEndX, rllEndY, llW, pants, lightenColor(pants, 20));
  // 右脚
  c.fillStyle = shoe;
  c.beginPath(); c.ellipse(rllEndX + 3, rllEndY, llW * 0.7, llW * 0.4, 0.2, 0, Math.PI * 2); c.fill();
  c.fillStyle = 'rgba(255,255,255,0.15)';
  c.beginPath(); c.ellipse(rllEndX + 2, rllEndY - 1, llW * 0.4, llW * 0.2, 0.2, 0, Math.PI * 2); c.fill();

  // === 脖子 ===
  c.fillStyle = skin;
  c.fillRect(-scale * 0.06, neckY - 2, scale * 0.12, neckLen + 2);
  c.fillStyle = 'rgba(255,255,255,0.12)';
  c.fillRect(-scale * 0.02, neckY - 2, scale * 0.04, neckLen + 2);

  // === 头部（3D球面） ===
  let headGrad = c.createRadialGradient(headX - headR * 0.3, headY - headR * 0.3, headR * 0.1, headX, headY, headR);
  headGrad.addColorStop(0, lightenColor(skin, 50));
  headGrad.addColorStop(0.5, skin);
  headGrad.addColorStop(1, darkenColor(skin, 50));
  c.fillStyle = headGrad;
  c.beginPath(); c.arc(headX, headY, headR, 0, Math.PI * 2); c.fill();
  // 头部高光
  c.fillStyle = 'rgba(255,255,255,0.2)';
  c.beginPath(); c.arc(headX - headR * 0.25, headY - headR * 0.25, headR * 0.4, 0, Math.PI * 2); c.fill();
  // 头部阴影（下巴下方）
  c.fillStyle = 'rgba(0,0,0,0.08)';
  c.beginPath(); c.arc(headX + headR * 0.1, headY + headR * 0.5, headR * 0.6, 0, Math.PI); c.fill();

  // === 脸部 ===
  if (opts.drawFace !== false) {
    let ft = opts.faceType || 'normal';
    let eOff = headR * 0.35;
    let eY = headY - headR * 0.1;

    if (ft === 'angry') {
      // 愤怒脸
      c.fillStyle = '#fff';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.18, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.18, 0, Math.PI * 2); c.fill();
      c.fillStyle = '#cc0000';
      c.beginPath(); c.arc(headX - eOff, eY + 1, headR * 0.1, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY + 1, headR * 0.1, 0, Math.PI * 2); c.fill();
      // 眉毛
      c.strokeStyle = '#993300'; c.lineWidth = 2.5; c.lineCap = 'round';
      c.beginPath(); c.moveTo(headX - eOff - headR * 0.22, eY - headR * 0.28); c.lineTo(headX - eOff + headR * 0.12, eY - headR * 0.18); c.stroke();
      c.beginPath(); c.moveTo(headX + eOff + headR * 0.22, eY - headR * 0.28); c.lineTo(headX + eOff - headR * 0.12, eY - headR * 0.18); c.stroke();
      c.lineCap = 'butt';
      // 嘴
      c.fillStyle = '#660000';
      c.beginPath(); c.arc(headX, headY + headR * 0.4, headR * 0.22, 0, Math.PI); c.fill();
      // 牙齿
      c.fillStyle = '#eee';
      for (let i = -2; i <= 2; i++) {
        c.fillRect(headX + i * headR * 0.08 - 1.5, headY + headR * 0.4 - 1, 3, headR * 0.1);
      }
    } else if (ft === 'glasses') {
      // 戴眼镜
      c.fillStyle = '#333';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.1, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.1, 0, Math.PI * 2); c.fill();
      // 眼镜框
      c.strokeStyle = '#1a1a2e'; c.lineWidth = 1.8;
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.17, 0, Math.PI * 2); c.stroke();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.17, 0, Math.PI * 2); c.stroke();
      c.beginPath(); c.moveTo(headX - eOff + headR * 0.17, eY); c.lineTo(headX + eOff - headR * 0.17, eY); c.stroke();
      c.fillStyle = 'rgba(100,180,255,0.15)';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.15, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.15, 0, Math.PI * 2); c.fill();
      // 微笑
      c.strokeStyle = '#a05030'; c.lineWidth = 1.5;
      c.beginPath(); c.arc(headX, headY + headR * 0.35, headR * 0.15, 0.2, Math.PI - 0.2); c.stroke();
    } else if (ft === 'bloodshot') {
      // 血丝眼
      c.fillStyle = '#fff';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.16, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.16, 0, Math.PI * 2); c.fill();
      c.fillStyle = '#cc2222';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.08, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.08, 0, Math.PI * 2); c.fill();
      // 张嘴
      c.fillStyle = '#882200';
      c.beginPath(); c.arc(headX, headY + headR * 0.4, headR * 0.12, 0, Math.PI); c.fill();
    } else {
      // 普通脸
      c.fillStyle = '#333';
      c.beginPath(); c.arc(headX - eOff, eY, headR * 0.1, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff, eY, headR * 0.1, 0, Math.PI * 2); c.fill();
      // 眼白高光
      c.fillStyle = '#fff';
      c.beginPath(); c.arc(headX - eOff + 2, eY - 2, headR * 0.04, 0, Math.PI * 2); c.fill();
      c.beginPath(); c.arc(headX + eOff + 2, eY - 2, headR * 0.04, 0, Math.PI * 2); c.fill();
      // 微笑
      c.strokeStyle = '#bb8866'; c.lineWidth = 1.5;
      c.beginPath(); c.arc(headX, headY + headR * 0.35, headR * 0.15, 0.15, Math.PI - 0.15); c.stroke();
    }
  }

  // === 头部额外装饰 ===
  if (opts.headExtra) opts.headExtra(c, x, y, headX, headY, headR, scale);
  // === 身体额外装饰 ===
  if (opts.bodyExtra) opts.bodyExtra(c, x, y, torsoW, neckY, hipY, shoulderW, scale);

  c.restore();
}

'''

# 插入到 "// ==================== 3D RENDERING HELPERS ====================" 之前
insert_marker = "// ==================== 3D RENDERING HELPERS ===================="
if insert_marker in html:
    html = html.replace(insert_marker, humanoid_system + "\n" + insert_marker)
    print("✅ 插入骨骼人形系统成功")
else:
    print("❌ 未找到插入标记")


# ============================================================
# 2. 替换 drawPlayer 函数
# ============================================================
old_drawPlayer = '''function drawPlayer(c,x,y,size,hp,maxHp,invincible){
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
}'''

new_drawPlayer = '''function drawPlayer(c,x,y,size,hp,maxHp,invincible){
  c.save();c.translate(x,y);
  let anim=Date.now()/1000;
  if(invincible&&Math.floor(Date.now()/80)%2===0){c.globalAlpha=0.4}
  // 地面阴影
  c.fillStyle='rgba(0,0,0,0.18)';
  c.beginPath();c.ellipse(0,size*0.85,size*0.9,size*0.25,0,0,Math.PI*2);c.fill();
  // 呼吸发光环
  let glowI=0.25+Math.sin(anim*4.4)*0.12;
  c.strokeStyle='rgba(52,152,219,'+glowI+')';c.lineWidth=3;
  c.shadowColor='#3498db';c.shadowBlur=18+Math.sin(anim*4)*5;
  c.beginPath();c.arc(0,size*0.1,size*1.3+Math.sin(anim*4)*1.5,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;
  // 判断是否在移动
  let p=G.player, dx=0, dy=0;
  if(keys['w']||keys['arrowup'])dy-=1;
  if(keys['s']||keys['arrowdown'])dy+=1;
  if(keys['a']||keys['arrowleft'])dx-=1;
  if(keys['d']||keys['arrowright'])dx+=1;
  if(touch.active){dx+=touch.dx;dy+=touch.dy}
  let moving = Math.hypot(dx,dy)>0.1;
  let bones = moving ? walkCycle(anim, 1.0) : idleCycle(anim);
  // 绘制3D骨骼人形 — 医生
  drawHumanoid(c, 0, 0, size*1.1, bones, {
    skinColor:'#f0c898',
    shirtColor:'#ecf0f1',
    pantsColor:'#2c3e50',
    shoeColor:'#1a1a2e',
    headRadius: 0.36,
    torsoH: 0.7,
    torsoW: 0.48,
    upperArmLen: 0.36,
    foreArmLen: 0.32,
    upperLegLen: 0.42,
    lowerLegLen: 0.38,
    upperArmW: 0.13,
    foreArmW: 0.1,
    upperLegW: 0.17,
    lowerLegW: 0.13,
    faceType: 'glasses',
    headExtra: function(c, ox, oy, hx, hy, hr, sc) {
      // 绿色手术帽
      let capG=c.createRadialGradient(hx-hr*0.3,hy-hr*0.5,hr*0.1,hx,hy,hr*1.15);
      capG.addColorStop(0,'#3dce78');capG.addColorStop(0.6,'#27ae60');capG.addColorStop(1,'#1a7a42');
      c.fillStyle=capG;
      c.beginPath();c.arc(hx,hy,hr*1.1,Math.PI+0.3,-0.3);c.fill();
      // 帽子高光
      c.fillStyle='rgba(255,255,255,0.2)';
      c.beginPath();c.arc(hx-hr*0.3,hy-hr*0.55,hr*0.4,Math.PI+0.2,-0.2);c.fill();
      // 帽沿
      c.fillStyle='#1a7a42';
      c.beginPath();c.ellipse(hx,hy+hr*0.05,hr*1.12,hr*0.12,0,0,Math.PI*2);c.fill();
      c.fillStyle='rgba(255,255,255,0.15)';
      c.beginPath();c.ellipse(hx,hy+hr*0.01,hr*1.1,hr*0.06,0,0,Math.PI*2);c.fill();
    },
    bodyExtra: function(c, ox, oy, tw, ny, hy2, sw, sc) {
      // 听诊器
      c.strokeStyle='#2c3e50';c.lineWidth=2.5;
      c.shadowColor='rgba(0,0,0,0.3)';c.shadowBlur=2;
      c.beginPath();c.moveTo(-sw*0.6,ny+3);c.quadraticCurveTo(-tw*1.1,hy2*0.5,-tw*0.4,hy2+2);c.stroke();
      c.shadowBlur=0;
      // 听诊器头
      let sG=c.createRadialGradient(-tw*0.42,hy2+3,0,-tw*0.4,hy2+4,sc*0.07);
      sG.addColorStop(0,'#e74c3c');sG.addColorStop(0.5,'#c0392b');sG.addColorStop(1,'#7b241c');
      c.fillStyle=sG;c.beginPath();c.arc(-tw*0.4,hy2+4,sc*0.06,0,Math.PI*2);c.fill();
      // ID牌
      c.fillStyle='rgba(255,255,255,0.85)';
      c.beginPath();c.roundRect(-tw-4,ny+5,sc*0.2,sc*0.28,2);c.fill();
      c.fillStyle='rgba(52,152,219,0.6)';
      c.fillRect(-tw-3,ny+6,sc*0.18,sc*0.06);
      c.strokeStyle='rgba(52,152,219,0.3)';c.lineWidth=0.5;
      c.beginPath();c.roundRect(-tw-4,ny+5,sc*0.2,sc*0.28,2);c.stroke();
      // 领带
      let tG=c.createLinearGradient(0,ny,0,ny+sc*0.25);
      tG.addColorStop(0,'#3498db');tG.addColorStop(1,'#1a5276');
      c.fillStyle=tG;
      c.beginPath();c.moveTo(-3,ny+3);c.lineTo(3,ny+3);c.lineTo(2,ny+sc*0.25);c.lineTo(-2,ny+sc*0.25);c.closePath();c.fill();
    }
  });
  c.globalAlpha=1;
  c.restore();
}'''

if old_drawPlayer in html:
    html = html.replace(old_drawPlayer, new_drawPlayer)
    print("✅ 替换 drawPlayer 成功")
else:
    print("❌ 未找到 drawPlayer")


# ============================================================
# 3. 替换 drawPatient 函数
# ============================================================
old_drawPatient = '''function drawPatient(c,x,y,size,color,type,el){
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

new_drawPatient = '''function drawPatient(c,x,y,size,color,type,el){
  c.save();c.translate(x,y);
  let anim=Date.now()/1000;
  // elite 光晕
  if(el){
    c.shadowColor='#f39c12';c.shadowBlur=14+Math.sin(anim*4)*5;
    c.strokeStyle='rgba(243,156,18,0.6)';c.lineWidth=2.5;
    c.beginPath();c.arc(0,0,size*1.2+Math.sin(anim*4)*2,0,Math.PI*2);c.stroke();
    c.shadowBlur=0;
  }
  // 地面阴影
  c.fillStyle='rgba(0,0,0,0.15)';
  c.beginPath();c.ellipse(0,size*0.8,size*0.75,size*0.2,0,0,Math.PI*2);c.fill();

  // 所有敌人都在移动（向玩家走来）
  let bones = walkCycle(anim, type==='fast' ? 1.8 : 1.0);

  // 根据类型配置人形参数
  let opts;
  if(type==='angry'){
    opts = {
      skinColor:'#f0c898', shirtColor:'#e67e22', pantsColor:'#8b4513', shoeColor:'#2c1810',
      headRadius:0.38, torsoH:0.6, torsoW:0.5,
      upperArmLen:0.35, foreArmLen:0.3, upperLegLen:0.4, lowerLegLen:0.36,
      upperArmW:0.14, foreArmW:0.11, upperLegW:0.16, lowerLegW:0.12,
      faceType:'angry',
      headExtra: function(c,ox,oy,hx,hy,hr,sc){
        // 怒发冲冠效果
        c.fillStyle='rgba(231,76,60,0.6)';
        for(let i=0;i<5;i++){
          let a=Math.PI+0.4+i*0.3;
          c.beginPath();c.moveTo(hx+Math.cos(a)*hr*0.7,hy+Math.sin(a)*hr*0.7);
          c.lineTo(hx+Math.cos(a)*hr*1.4+rand(-2,2),hy+Math.sin(a)*hr*1.4);
          c.lineTo(hx+Math.cos(a+0.15)*hr*0.7,hy+Math.sin(a+0.15)*hr*0.7);
          c.closePath();c.fill();
        }
      },
      bodyExtra: function(c,ox,oy,tw,ny,hy2,sw,sc){
        // 手中举着手机
        c.fillStyle='#0a0a1e';
        c.beginPath();c.roundRect(sw+sc*0.15,ny+sc*0.05,sc*0.2,sc*0.3,2);c.fill();
        c.fillStyle='rgba(68,136,255,0.85)';
        c.beginPath();c.roundRect(sw+sc*0.17,ny+sc*0.08,sc*0.16,sc*0.22,1);c.fill();
      }
    };
  }else if(type==='admin'){
    opts = {
      skinColor:'#e8c090', shirtColor:'#2c3e50', pantsColor:'#1a1a2e', shoeColor:'#0a0a14',
      headRadius:0.38, torsoH:0.65, torsoW:0.52,
      upperArmLen:0.34, foreArmLen:0.3, upperLegLen:0.42, lowerLegLen:0.38,
      upperArmW:0.14, foreArmW:0.11, upperLegW:0.18, lowerLegW:0.14,
      faceType:'glasses',
      headExtra: function(c,ox,oy,hx,hy,hr,sc){
        // 秃头高光
        let baldG=c.createRadialGradient(hx-hr*0.2,hy-hr*0.4,0,hx,hy-hr*0.3,hr*0.8);
        baldG.addColorStop(0,'rgba(255,255,255,0.15)');baldG.addColorStop(1,'rgba(255,255,255,0)');
        c.fillStyle=baldG;c.beginPath();c.arc(hx,hy-hr*0.3,hr*0.8,Math.PI+0.3,-0.3);c.fill();
      },
      bodyExtra: function(c,ox,oy,tw,ny,hy2,sw,sc){
        // 领带
        let tG=c.createLinearGradient(0,ny,0,ny+sc*0.3);
        tG.addColorStop(0,'#e74c3c');tG.addColorStop(1,'#7b241c');
        c.fillStyle=tG;
        c.beginPath();c.moveTo(-4,ny+5);c.lineTo(4,ny+5);c.lineTo(3,ny+sc*0.3);c.lineTo(-3,ny+sc*0.3);c.closePath();c.fill();
        c.fillStyle='rgba(255,255,255,0.2)';
        c.beginPath();c.moveTo(-3,ny+5);c.lineTo(0,ny+sc*0.15);c.lineTo(-1,ny+sc*0.3);c.closePath();c.fill();
      }
    };
  }else if(type==='fast'){
    opts = {
      skinColor:'#e8c090', shirtColor:'#e74c3c', pantsColor:'#555', shoeColor:'#333',
      headRadius:0.35, torsoH:0.7, torsoW:0.4,
      upperArmLen:0.38, foreArmLen:0.34, upperLegLen:0.48, lowerLegLen:0.44,
      upperArmW:0.1, foreArmW:0.08, upperLegW:0.13, lowerLegW:0.1,
      faceType:'bloodshot',
      headExtra: null, bodyExtra: null
    };
  }else if(type==='family'){
    opts = {
      skinColor:'#f0c898', shirtColor:'#f39c12', pantsColor:'#8b6914', shoeColor:'#5a3e0a',
      headRadius:0.4, torsoH:0.55, torsoW:0.55,
      upperArmLen:0.3, foreArmLen:0.26, upperLegLen:0.35, lowerLegLen:0.32,
      upperArmW:0.15, foreArmW:0.12, upperLegW:0.18, lowerLegW:0.14,
      faceType:'normal',
      headExtra: null,
      bodyExtra: function(c,ox,oy,tw,ny,hy2,sw,sc){
        // 背后的人影（矮小半透明）
        c.globalAlpha=0.4;
        let bBones = walkCycle(anim, 0.8);
        drawHumanoid(c, -sc*0.6, sc*0.15, sc*0.65, bBones, {
          skinColor:'#e8c090', shirtColor:color, pantsColor:'#555', shoeColor:'#333',
          headRadius:0.38, torsoH:0.55, torsoW:0.48,
          upperArmLen:0.28, foreArmLen:0.24, upperLegLen:0.32, lowerLegLen:0.28,
          upperArmW:0.12, foreArmW:0.09, upperLegW:0.14, lowerLegW:0.11,
          faceType:'normal', drawFace:true
        });
        c.globalAlpha=1;
      }
    };
  }else{
    // patient - 普通患者
    opts = {
      skinColor:'#f0c898', shirtColor:color, pantsColor:'#34495e', shoeColor:'#2c3e50',
      headRadius:0.38, torsoH:0.62, torsoW:0.48,
      upperArmLen:0.35, foreArmLen:0.3, upperLegLen:0.42, lowerLegLen:0.38,
      upperArmW:0.13, foreArmW:0.1, upperLegW:0.16, lowerLegW:0.12,
      faceType:'normal',
      headExtra: null, bodyExtra: null
    };
  }

  drawHumanoid(c, 0, 0, size*1.1, bones, opts);

  c.restore();
}'''

if old_drawPatient in html:
    html = html.replace(old_drawPatient, new_drawPatient)
    print("✅ 替换 drawPatient 成功")
else:
    print("❌ 未找到 drawPatient")


# ============================================================
# 4. 替换 drawBoss 函数
# ============================================================
old_drawBoss_start = '''function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){
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
}'''

new_drawBoss = '''function drawBoss(c,x,y,size,bossName,hp,maxHp,color,shielded,raging){
  c.save();c.translate(x,y);
  let anim=Date.now()/1000;
  // 地面阴影（大椭圆）
  c.fillStyle='rgba(0,0,0,0.3)';
  c.beginPath();c.ellipse(0,size*1.0,size*1.3,size*0.35,0,0,Math.PI*2);c.fill();
  // 外层脉冲光环（双环）
  let auraR1=size+18+Math.sin(anim*3.6)*7;
  let auraR2=size+32+Math.sin(anim*4.6)*5;
  let auraA=raging?0.5:0.25;
  let auraC=raging?'255,0,0':'255,68,68';
  c.strokeStyle='rgba('+auraC+','+auraA+')';c.lineWidth=3;
  c.shadowColor='rgba('+auraC+',0.6)';c.shadowBlur=raging?20:10;
  c.beginPath();c.arc(0,size*0.1,auraR1,0,Math.PI*2);c.stroke();
  c.strokeStyle='rgba('+auraC+','+(auraA*0.5)+')';c.lineWidth=2;
  c.beginPath();c.arc(0,size*0.1,auraR2,0,Math.PI*2);c.stroke();
  c.shadowBlur=0;

  // Boss骨骼人形 — 夸张比例的大块头
  let bones = walkCycle(anim, raging ? 1.5 : 0.8);
  // 暴怒时加大动作幅度
  if(raging){
    bones.upperArmL *= 1.5; bones.upperArmR *= 1.5;
    bones.foreArmL *= 1.3; bones.foreArmR *= 1.3;
    bones.upperLegL *= 1.3; bones.upperLegR *= 1.3;
    bones.lowerLegL *= 1.2; bones.lowerLegR *= 1.2;
    bones.bodyBob *= 1.5;
  }

  let bossSkin = raging ? '#e8a080' : '#e8c090';
  let bossShirt = raging ? '#cc2200' : color;

  drawHumanoid(c, 0, 0, size*1.2, bones, {
    skinColor: bossSkin,
    shirtColor: bossShirt,
    pantsColor: raging ? '#330000' : '#440000',
    shoeColor: '#1a0000',
    headRadius: 0.42,
    torsoH: 0.75,
    torsoW: 0.6,
    upperArmLen: 0.42,
    foreArmLen: 0.38,
    upperLegLen: 0.48,
    lowerLegLen: 0.44,
    upperArmW: 0.2,
    foreArmW: 0.16,
    upperLegW: 0.22,
    lowerLegW: 0.18,
    faceType: 'angry',
    headExtra: function(c,ox,oy,hx,hy,hr,sc){
      // 怒发冲冠（更夸张）
      c.fillStyle = raging ? 'rgba(255,50,0,0.7)' : 'rgba(200,50,30,0.5)';
      for(let i=0;i<7;i++){
        let a=Math.PI+0.3+i*0.25;
        let len=raging?hr*1.8:hr*1.5;
        c.beginPath();c.moveTo(hx+Math.cos(a)*hr*0.8,hy+Math.sin(a)*hr*0.8);
        c.lineTo(hx+Math.cos(a)*len+rand(-3,3),hy+Math.sin(a)*len);
        c.lineTo(hx+Math.cos(a+0.12)*hr*0.8,hy+Math.sin(a+0.12)*hr*0.8);
        c.closePath();c.fill();
      }
      // 暴怒光环
      if(raging){
        c.shadowColor='#ff2200';c.shadowBlur=15;
        c.strokeStyle='rgba(255,34,0,0.5)';c.lineWidth=2;
        c.beginPath();c.arc(hx,hy,hr*1.3,0,Math.PI*2);c.stroke();
        c.shadowBlur=0;
      }
    },
    bodyExtra: function(c,ox,oy,tw,ny,hy2,sw,sc){
      // Boss手机（更大的3D手机）
      c.fillStyle='#0a0a1e';
      c.beginPath();c.roundRect(sw+sc*0.1,ny+sc*0.1,sc*0.22,sc*0.35,3);c.fill();
      let phoneG=c.createLinearGradient(sw+sc*0.1,ny+sc*0.1,sw+sc*0.32,ny+sc*0.1);
      phoneG.addColorStop(0,'rgba(255,255,255,0.15)');phoneG.addColorStop(1,'rgba(255,255,255,0)');
      c.fillStyle=phoneG;c.beginPath();c.roundRect(sw+sc*0.1,ny+sc*0.1,sc*0.22,sc*0.35,3);c.fill();
      c.fillStyle='rgba(68,136,255,0.9)';
      c.beginPath();c.roundRect(sw+sc*0.13,ny+sc*0.14,sc*0.16,sc*0.25,2);c.fill();
      c.fillStyle='rgba(255,255,255,0.3)';
      c.beginPath();c.moveTo(sw+sc*0.13,ny+sc*0.14);c.lineTo(sw+sc*0.29,ny+sc*0.14);
      c.lineTo(sw+sc*0.13,ny+sc*0.3);c.closePath();c.fill();
      // 肩章（Boss标识）
      c.fillStyle='rgba(255,215,0,0.6)';
      c.beginPath();c.roundRect(-sw-tw*0.1,ny-2,tw*0.2,sc*0.06,2);c.fill();
      c.beginPath();c.roundRect(sw-tw*0.1,ny-2,tw*0.2,sc*0.06,2);c.fill();
    }
  });

  // 护盾特效
  if(shielded){
    let shieldA=0.5+Math.sin(anim*10)*0.25;
    c.strokeStyle='rgba(68,136,255,'+shieldA+')';c.lineWidth=4;
    c.shadowColor='rgba(68,136,255,0.8)';c.shadowBlur=16;
    c.beginPath();
    for(let i=0;i<6;i++){
      let a=i*Math.PI/3+anim*0.2;
      let r2=size*1.2+10;
      if(i===0)c.moveTo(Math.cos(a)*r2,Math.sin(a)*r2+size*0.1);
      else c.lineTo(Math.cos(a)*r2,Math.sin(a)*r2+size*0.1);
    }
    c.closePath();c.stroke();
    c.fillStyle='rgba(68,136,255,0.08)';c.beginPath();
    for(let i=0;i<6;i++){
      let a=i*Math.PI/3+anim*0.2;let r2=size*1.2+10;
      if(i===0)c.moveTo(Math.cos(a)*r2,Math.sin(a)*r2+size*0.1);
      else c.lineTo(Math.cos(a)*r2,Math.sin(a)*r2+size*0.1);
    }
    c.closePath();c.fill();
    c.shadowBlur=0;
  }
  // 名牌（玻璃感）
  c.font='bold 13px Microsoft YaHei,sans-serif';c.textAlign='center';
  let tw2=c.measureText(bossName).width+24;
  let txL=-tw2/2, tyL=-size*1.2-28;
  let tagG=c.createLinearGradient(txL,tyL,txL,tyL+22);
  tagG.addColorStop(0,'rgba(20,0,0,0.9)');tagG.addColorStop(1,'rgba(60,0,0,0.85)');
  c.fillStyle=tagG;c.beginPath();c.roundRect(txL,tyL,tw2,22,5);c.fill();
  c.fillStyle='rgba(255,255,255,0.08)';c.beginPath();c.roundRect(txL,tyL,tw2,10,5);c.fill();
  c.strokeStyle='rgba(255,68,68,0.6)';c.lineWidth=1.2;c.beginPath();c.roundRect(txL,tyL,tw2,22,5);c.stroke();
  c.fillStyle='#ff7777';c.shadowColor='#ff4444';c.shadowBlur=6;
  c.fillText(bossName,0,tyL+14);
  c.shadowBlur=0;
  // 血条（3D凸起感）
  let bw=size*2.4,bh=8;
  let barY=size*1.2+12;
  c.fillStyle='rgba(0,0,0,0.7)';c.beginPath();c.roundRect(-bw/2,barY,bw,bh,4);c.fill();
  let hpRatio=hp/maxHp;
  let hpFill=bw*hpRatio;
  let hpColor=hpRatio>0.5?'#e74c3c':hpRatio>0.25?'#ff6600':'#ff0000';
  let hpGrad=c.createLinearGradient(-bw/2,barY,-bw/2,barY+bh);
  hpGrad.addColorStop(0,lightenColor(hpColor,40));
  hpGrad.addColorStop(0.4,hpColor);
  hpGrad.addColorStop(1,darkenColor(hpColor,30));
  c.fillStyle=hpGrad;
  c.shadowColor=hpColor;c.shadowBlur=6;
  c.beginPath();c.roundRect(-bw/2,barY,Math.max(0,hpFill),bh,4);c.fill();
  c.shadowBlur=0;
  c.fillStyle='rgba(255,255,255,0.2)';
  c.beginPath();c.roundRect(-bw/2,barY,Math.max(0,hpFill),bh*0.4,4);c.fill();
  c.restore();
}'''

if old_drawBoss_start in html:
    html = html.replace(old_drawBoss_start, new_drawBoss)
    print("✅ 替换 drawBoss 成功")
else:
    print("❌ 未找到 drawBoss")


# ============================================================
# 5. 写出文件
# ============================================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 统计行数
lines = html.count('\n') + 1
print(f"\n📝 文件写入完成，共 {lines} 行")
