(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reduce.matches) return;

  const canvas = document.getElementById('atmosphere');
  const ctx = canvas.getContext('2d');
  let w = 0, h = 0;

  const snow = [];
  const wisps = [];

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function spawnSnow(randomY = true) {
    return {
      x: Math.random() * w,
      y: randomY ? Math.random() * h : -10,
      r: 0.9 + Math.random() * 2.1,
      vy: 0.25 + Math.random() * 0.55,
      drift: (Math.random() - 0.5) * 0.3,
      phase: Math.random() * Math.PI * 2,
      alpha: 0.2 + Math.random() * 0.55
    };
  }

  function spawnWisp(randomY = true) {
    return {
      x: Math.random() * w,
      y: randomY ? Math.random() * h : h + 15,
      r: 1.5 + Math.random() * 3.5,
      vy: -(0.18 + Math.random() * 0.42),
      drift: (Math.random() - 0.5) * 0.25,
      phase: Math.random() * Math.PI * 2,
      maxAlpha: 0.22 + Math.random() * 0.4
    };
  }

  resize();
  window.addEventListener('resize', resize);

  for (let i = 0; i < 48; i++) snow.push(spawnSnow(true));
  for (let i = 0; i < 28; i++) wisps.push(spawnWisp(true));

  let t = 0;
  let raf = 0;
  function tick() {
    t += 0.012;
    ctx.clearRect(0, 0, w, h);

    // Falling icy snow
    for (const p of snow) {
      p.y += p.vy;
      p.x += p.drift + Math.sin(t + p.phase) * 0.22;
      if (p.y > h + 10) Object.assign(p, spawnSnow(false));
      if (p.x < -10) p.x = w + 10;
      if (p.x > w + 10) p.x = -10;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(215, 245, 255, ${p.alpha})`;
      ctx.fill();
    }

    // Rising glowing cyan smoke wisps
    for (const e of wisps) {
      e.y += e.vy;
      e.x += e.drift + Math.cos(t * 0.8 + e.phase) * 0.3;
      const progress = 1 - e.y / h;
      const fade = Math.sin(Math.max(0, Math.min(1, progress)) * Math.PI);

      if (e.y < -20) Object.assign(e, spawnWisp(false));

      const grad = ctx.createRadialGradient(e.x, e.y, 0, e.x, e.y, e.r * 3.2);
      grad.addColorStop(0, `rgba(110, 242, 255, ${e.maxAlpha * fade})`);
      grad.addColorStop(1, 'rgba(34, 211, 238, 0)');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(e.x, e.y, e.r * 3.2, 0, Math.PI * 2);
      ctx.fill();
    }

    raf = requestAnimationFrame(tick);
  }

  // If the user turns reduced motion on mid-session, stop and clear the canvas.
  reduce.addEventListener('change', () => {
    if (reduce.matches) { cancelAnimationFrame(raf); ctx.clearRect(0, 0, w, h); }
  });

  tick();
})();
