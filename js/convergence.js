/* Live hero: measurements streaming in and converging on a point.
 *
 * This is the Convergence mark made literal and moving — the same idea as the
 * logo (data flowing together and igniting), run as a particle simulation at
 * full width. Particles ride curved trajectories toward a focus, brighten as
 * they approach, and are recycled at the left edge; every so often the focus
 * takes an ember. Honors prefers-reduced-motion by drawing a single static
 * frame instead.
 */
(function () {
  var canvas = document.getElementById("convergence");
  if (!canvas || !canvas.getContext) return;

  var ctx = canvas.getContext("2d");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var CARDINAL = [178, 58, 58];
  var EMBER = [233, 160, 62];

  var W = 0, H = 0, dpr = 1;
  var focus = { x: 0, y: 0 };
  var particles = [];
  var embers = [];
  var STREAMS = 7;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = canvas.clientWidth;
    H = canvas.clientHeight;
    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    focus.x = W * 0.76;
    focus.y = H * 0.5;
    seed();
  }

  function makeParticle(atStart) {
    var lane = Math.floor(Math.random() * STREAMS);
    var spread = H * 0.42;
    var y0 = focus.y + (lane / (STREAMS - 1) - 0.5) * 2 * spread;
    return {
      t: atStart ? Math.random() : 0,
      speed: 0.00042 + Math.random() * 0.00075,
      y0: y0 + (Math.random() - 0.5) * 26,
      x0: -W * 0.06 + Math.random() * W * 0.22,
      bow: (Math.random() - 0.5) * 0.55,
      size: 0.7 + Math.random() * 1.7
    };
  }

  function seed() {
    particles = [];
    var n = Math.round(Math.min(340, Math.max(120, W / 4.4)));
    for (var i = 0; i < n; i++) particles.push(makeParticle(true));
    embers = [];
  }

  function positionOf(p) {
    // quadratic bow from the entry point to the focus
    var t = p.t;
    var mx = (p.x0 + focus.x) / 2;
    var my = p.y0 + (focus.y - p.y0) * 0.15 + p.bow * H * 0.5;
    var u = 1 - t;
    return {
      x: u * u * p.x0 + 2 * u * t * mx + t * t * focus.x,
      y: u * u * p.y0 + 2 * u * t * my + t * t * focus.y
    };
  }

  function rgba(c, a) {
    return "rgba(" + c[0] + "," + c[1] + "," + c[2] + "," + a.toFixed(3) + ")";
  }

  function drawFrame(dt) {
    ctx.clearRect(0, 0, W, H);

    // faint trajectory guides
    ctx.lineWidth = 1;
    for (var s = 0; s < STREAMS; s++) {
      var y0 = focus.y + (s / (STREAMS - 1) - 0.5) * 2 * (H * 0.42);
      ctx.beginPath();
      ctx.moveTo(-20, y0);
      ctx.quadraticCurveTo((focus.x - 20) / 2, y0 + (focus.y - y0) * 0.15, focus.x, focus.y);
      ctx.strokeStyle = rgba(CARDINAL, 0.07);
      ctx.stroke();
    }

    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];
      p.t += p.speed * dt;
      if (p.t >= 1) {
        if (embers.length < 26 && Math.random() < 0.5) {
          embers.push({ a: Math.random() * Math.PI * 2, r: 6, life: 1,
                        speed: 0.35 + Math.random() * 0.7 });
        }
        particles[i] = makeParticle(false);
        continue;
      }
      var pos = positionOf(p);
      // brighten and warm as the measurement approaches the focus
      var near = Math.pow(p.t, 2.4);
      var col = [
        Math.round(CARDINAL[0] + (EMBER[0] - CARDINAL[0]) * near),
        Math.round(CARDINAL[1] + (EMBER[1] - CARDINAL[1]) * near),
        Math.round(CARDINAL[2] + (EMBER[2] - CARDINAL[2]) * near)
      ];
      var alpha = 0.16 + 0.72 * near;
      var r = p.size * (1 + near * 1.5);
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, r, 0, Math.PI * 2);
      ctx.fillStyle = rgba(col, alpha);
      ctx.fill();
    }

    // embers thrown off by the focus
    for (var e = embers.length - 1; e >= 0; e--) {
      var em = embers[e];
      em.r += em.speed * dt * 0.05;
      em.life -= dt * 0.0011;
      if (em.life <= 0) { embers.splice(e, 1); continue; }
      var ex = focus.x + Math.cos(em.a) * em.r;
      var ey = focus.y + Math.sin(em.a) * em.r;
      ctx.beginPath();
      ctx.arc(ex, ey, 1.6, 0, Math.PI * 2);
      ctx.fillStyle = rgba(EMBER, Math.max(0, em.life) * 0.6);
      ctx.fill();
    }

    // the focus itself
    var glow = ctx.createRadialGradient(focus.x, focus.y, 0, focus.x, focus.y, 84);
    glow.addColorStop(0, rgba(EMBER, 0.34));
    glow.addColorStop(1, rgba(EMBER, 0));
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(focus.x, focus.y, 84, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.arc(focus.x, focus.y, 7, 0, Math.PI * 2);
    ctx.fillStyle = rgba(EMBER, 0.95);
    ctx.fill();
  }

  var last = 0;
  function loop(now) {
    var dt = Math.min(48, now - last || 16);
    last = now;
    drawFrame(dt);
    requestAnimationFrame(loop);
  }

  window.addEventListener("resize", resize);
  resize();

  if (reduced) {
    // one settled frame, no motion
    for (var k = 0; k < 260; k++) {
      particles.forEach(function (p) { p.t += p.speed * 16; });
    }
    drawFrame(0);
  } else {
    requestAnimationFrame(loop);
  }
})();
