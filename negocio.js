/* Glysf · demo de pádel: el scroll mueve la historia.
   - Cada [data-scene] recibe --p (0→1) según cuánto se ha recorrido su altura.
   - Dentro de una escena, todo [data-at] se activa (.on) cuando p ≥ data-at.
   - data-swap/data-to cambian un texto; data-fill llena una barra; data-count cuenta un número. */
(() => {
  'use strict';
  const IMG = id => `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${innerWidth > 900 ? 1920 : 1080}&q=70`;
  const red = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Fotos: se cargan de a una y aparecen con fundido cuando ya llegaron.
  document.querySelectorAll('[data-src]').forEach(n => {
    const url = n.classList.contains('c-img') ? IMG(n.dataset.src).replace(/w=\d+/, 'w=800') : IMG(n.dataset.src);
    const im = new Image();
    im.onload = () => { n.style.backgroundImage = `url("${url}")`; n.classList.add('loaded'); };
    im.src = url;
  });

  const cur = document.querySelector('.biztabs [aria-current]'); if (cur) cur.scrollIntoView({ inline: 'center', block: 'nearest' });

  const scenes = [...document.querySelectorAll('[data-scene]')].map(s => ({
    el: s,
    at: [...s.querySelectorAll('[data-at]')],
    swap: [...s.querySelectorAll('[data-swap]')],
    count: [...s.querySelectorAll('[data-count]')],
    p: -1
  }));

  function paint(sc, p) {
    sc.el.style.setProperty('--p', p.toFixed(4));
    for (const n of sc.at) {
      const on = p >= Number(n.dataset.at);
      if (on === n.classList.contains('on')) continue;
      n.classList.toggle('on', on);
      const f = n.dataset.fill;
      if (f !== undefined) { n.style.width = on ? f + '%' : '100%'; n.classList.toggle('low', on && Number(f) <= 25); }
    }
    for (const n of sc.swap) {
      if (!n.dataset.from) n.dataset.from = n.textContent;
      const on = p >= Number(n.dataset.swap);
      const txt = on ? n.dataset.to : n.dataset.from;
      if (n.textContent !== txt) { n.textContent = txt; if (n.classList.contains('warn') && on) { n.classList.replace('warn', 'ok'); } else if (!on && n.dataset.from === 'Pendiente') n.classList.replace('ok', 'warn'); }
    }
    for (const n of sc.count) n.textContent = Math.round(Number(n.dataset.count) * Math.min(1, Math.max(0, (p - .1) / .6)));
  }

  function tick() {
    const vh = innerHeight;
    for (const sc of scenes) {
      const r = sc.el.getBoundingClientRect();
      const total = r.height - vh;
      const p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      if (Math.abs(p - sc.p) > 0.001) { sc.p = p; paint(sc, p); }
    }
  }

  if (red) {
    // Sin animaciones: todo se ve completo desde el inicio.
    for (const sc of scenes) paint(sc, 1);
    return;
  }
  let raf = 0;
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; tick(); }); }, { passive: true });
  addEventListener('resize', tick);
  tick();
})();
