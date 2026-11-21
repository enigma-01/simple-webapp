import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

MESSAGE = "Hello! Version 2 - 2D animated web app deployed with CI/CD"   # change this and push to show an update

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CI/CD Animated Web App</title>
<style>
  html, body { margin: 0; height: 100%; overflow: hidden; background: #070b1a; font-family: system-ui, sans-serif; }
  canvas { display: block; }
  .card { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); text-align: center;
          color: #e8eefc; background: rgba(15, 23, 48, .75); border: 1px solid #2c3d6b;
          border-radius: 14px; padding: 14px 26px; max-width: 90vw; }
  .card h1 { margin: 0 0 6px; font-size: 1.35rem; }
  .card p { margin: 2px 0; font-size: .9rem; color: #9fb0d8; }
  code { color: #7ee2b8; }
</style>
</head>
<body>
<div class="card">
  <h1>{{ message }}</h1>
  <p>Commit: <code>{{ commit }}</code></p>
  <p>Click anywhere for fireworks</p>
</div>
<canvas id="c"></canvas>
<script>
const canvas = document.getElementById("c");
const ctx = canvas.getContext("2d");
let W, H;
function resize() { W = canvas.width = innerWidth; H = canvas.height = innerHeight; }
addEventListener("resize", resize);
resize();

// Twinkling stars
const stars = Array.from({ length: 160 }, () => ({
  x: Math.random(), y: Math.random(), r: Math.random() * 1.6 + 0.3, p: Math.random() * Math.PI * 2
}));

// Pipeline stages
const stages = ["Commit", "Test", "Build", "Push", "Deploy"];
const colors = ["#60a5fa", "#a78bfa", "#f472b6", "#fbbf24", "#34d399"];
const glow = stages.map(() => 0);
function stageX(i) { return W * (0.12 + i * 0.19); }
function stageY() { return H * 0.6; }

// Packets travelling through the pipeline
const packets = [];
function addPacket() { packets.push({ t: 0, speed: 0.0025 + Math.random() * 0.002 }); }
setInterval(addPacket, 900);
addPacket();

// Click fireworks
const sparks = [];
canvas.addEventListener("click", e => {
  for (let i = 0; i < 60; i++) {
    const a = Math.random() * Math.PI * 2, s = Math.random() * 5 + 1;
    sparks.push({ x: e.clientX, y: e.clientY, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
                  life: 1, c: colors[i % colors.length] });
  }
});

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
}

function frame(time) {
  // Sky
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, "#070b1a"); g.addColorStop(1, "#16204a");
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);

  for (const s of stars) {
    ctx.globalAlpha = 0.5 + 0.5 * Math.sin(time / 600 + s.p);
    ctx.fillStyle = "#ffffff";
    ctx.beginPath(); ctx.arc(s.x * W, s.y * H, s.r, 0, Math.PI * 2); ctx.fill();
  }
  ctx.globalAlpha = 1;

  // Pipeline line
  const y = stageY();
  ctx.strokeStyle = "#2c3d6b"; ctx.lineWidth = 6; ctx.lineCap = "round";
  ctx.beginPath(); ctx.moveTo(stageX(0), y); ctx.lineTo(stageX(4), y); ctx.stroke();

  // Stage boxes
  const bw = Math.min(130, W * 0.15), bh = 56;
  stages.forEach((name, i) => {
    const x = stageX(i) - bw / 2, top = y - bh / 2;
    glow[i] *= 0.95;
    ctx.shadowColor = colors[i]; ctx.shadowBlur = 10 + glow[i] * 35;
    ctx.fillStyle = "#0f1730"; roundRect(x, top, bw, bh, 12); ctx.fill();
    ctx.shadowBlur = 0;
    ctx.strokeStyle = colors[i]; ctx.lineWidth = 2 + glow[i] * 3; roundRect(x, top, bw, bh, 12); ctx.stroke();
    ctx.fillStyle = "#e8eefc"; ctx.font = "600 " + Math.max(12, Math.min(17, W / 60)) + "px system-ui";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText(name, stageX(i), y);
  });

  // Packets
  for (let i = packets.length - 1; i >= 0; i--) {
    const p = packets[i];
    p.t += p.speed;
    if (p.t >= 1) { glow[4] = 1; packets.splice(i, 1); continue; }
    const pos = p.t * 4, idx = Math.floor(pos);
    if (pos - idx < 0.03) glow[idx] = 1;
    const x = stageX(0) + (stageX(4) - stageX(0)) * p.t;
    const bob = Math.sin(time / 150 + p.t * 20) * 4;
    ctx.fillStyle = colors[idx];
    ctx.shadowColor = colors[idx]; ctx.shadowBlur = 18;
    ctx.beginPath(); ctx.arc(x, y + bob, 9, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  }

  // Fireworks
  for (let i = sparks.length - 1; i >= 0; i--) {
    const s = sparks[i];
    s.x += s.vx; s.y += s.vy; s.vy += 0.06; s.life -= 0.015;
    if (s.life <= 0) { sparks.splice(i, 1); continue; }
    ctx.globalAlpha = s.life; ctx.fillStyle = s.c;
    ctx.beginPath(); ctx.arc(s.x, s.y, 2.5, 0, Math.PI * 2); ctx.fill();
  }
  ctx.globalAlpha = 1;

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
</script>
</body>
</html>"""


@app.get("/")
def home():
    return render_template_string(PAGE, message=MESSAGE, commit=os.getenv("GIT_SHA", "local"))


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/api/info")
def info():
    return jsonify(message=MESSAGE, commit=os.getenv("GIT_SHA", "local"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
