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
      if (sc.el.classList.contains('flow')) continue;
      const r = sc.el.getBoundingClientRect();
      const total = r.height - vh;
      const p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      if (Math.abs(p - sc.p) > 0.001) { sc.p = p; paint(sc, p); }
    }
  }

  // Escenas "flow": sin scroll fijo; cuando aparecen, su historia se reproduce sola en ~2,5 s
  const flows = scenes.filter(sc => sc.el.classList.contains('flow'));
  const play = sc => { if (sc.played) return; sc.played = true; const t0 = performance.now();
    const f = t => { const k = Math.min(1, (t - t0) / 2500); sc.p = k; paint(sc, k); if (k < 1) requestAnimationFrame(f); }; requestAnimationFrame(f); };
  if ('IntersectionObserver' in window && !red) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const sc = flows.find(x => x.el === e.target); if (sc) { play(sc); io.unobserve(e.target); } } }), { threshold: .25 });
    flows.forEach(sc => io.observe(sc.el));
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

// Panel de muestra: el menú lateral y las tarjetas cambian de sección, como en el panel real.
(() => {
  document.querySelectorAll('.cp').forEach(cp => {
    const views = [...cp.querySelectorAll('.cp-view')];
    const navs = [...cp.querySelectorAll('.cp-nav [data-v]')];
    const h = cp.querySelector('.cp-h');
    const show = (v, foco) => {
      views.forEach(x => { x.hidden = x.dataset.view !== v; if (!x.hidden) h.textContent = x.dataset.title; });
      navs.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v)));
      const nb = navs.find(b => b.dataset.v === v);
      if (nb && matchMedia('(max-width:860px)').matches) nb.scrollIntoView({ inline: 'center', block: 'nearest' });
      if (foco) h.focus?.();
    };
    // Misma altura en todas las secciones, para que la página no salte al cambiar.
    const main = cp.querySelector('.cp-main');
    const fija = () => { main.style.minHeight = ''; main.style.minHeight = main.offsetHeight + 'px'; };
    if (!views[0].hidden) fija(); addEventListener('resize', () => { if (!views[0].hidden) fija(); });
    cp.addEventListener('click', e => { const b = e.target.closest('button[data-v]'); if (b) show(b.dataset.v); });
  });
})();

// Torre del proyecto (constructora): elegir piso y apartamento, ver plano y fotos.
(() => {
  const pj = document.querySelector('.pj');
  if (!pj) return;
  const card = pj.querySelector('.pj-card');
  const f = k => pj.querySelector(`[data-f="${k}"]`);
  const apts = [...pj.querySelectorAll('.apt')];
  const floors = [...pj.querySelectorAll('.pj-floor')];
  const rows = [...pj.querySelectorAll('.pj-units')];
  const cta = card.querySelector('.pj-cta'), note = card.querySelector('.pj-note');
  const foto = card.querySelector('.pj-photo');
  const ponerFoto = id => { foto.style.backgroundImage = `url('https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=1000&q=70')`; };
  const stage = pj.querySelector('.pj-stage');
  let tipoActual = null;
  const ver = el => {
    apts.forEach(a => a.classList.toggle('sel', a === el));
    stage.dispatchEvent(new CustomEvent('pj:sel', { detail: el.dataset.apto }));
    const d = el.dataset;
    f('apto').textContent = d.apto; f('piso').textContent = d.piso; f('vista').textContent = d.vista;
    f('area').textContent = d.area; f('hab').textContent = d.hab; f('banos').textContent = d.banos; f('precio').textContent = d.precio;
    const est = f('estado'); est.textContent = d.estado[0].toUpperCase() + d.estado.slice(1); est.className = 'pj-pill ' + d.estado;
    card.querySelectorAll('.pj-plan').forEach(p => p.toggleAttribute('hidden', p.dataset.plan !== d.tipo));
    if (d.tipo !== tipoActual) {
      tipoActual = d.tipo;
      card.querySelectorAll('.pj-thumbs').forEach(g => { g.hidden = g.dataset.tipo !== d.tipo; });
      const g = card.querySelector(`.pj-thumbs[data-tipo="${d.tipo}"]`);
      g.querySelectorAll('[data-img]').forEach((x, i) => x.setAttribute('aria-pressed', String(i === 0)));
      ponerFoto(g.querySelector('[data-img]').dataset.img);
    }
    cta.disabled = d.estado !== 'disponible';
    cta.textContent = d.estado === 'disponible' ? 'Separar este apto' : (d.estado === 'separado' ? 'Ya está separado' : 'Vendido');
    note.hidden = true;
  };
  const piso = (p, elegir) => {
    floors.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.floor === String(p))));
    rows.forEach(r => { r.hidden = r.dataset.units !== String(p); });
    f('pisolbl').textContent = 'piso ' + p;
    if (elegir) { const fila = rows.find(r => !r.hidden); ver(fila.querySelector('.apt.disponible') || fila.querySelector('.apt')); }
  };
  floors.forEach(b => b.addEventListener('click', () => piso(b.dataset.floor, true)));
  apts.forEach(a => a.addEventListener('click', () => ver(a)));
  stage.addEventListener('pj:pick', e => { const a = apts.find(x => x.dataset.apto === e.detail); if (a) { piso(a.dataset.piso, false); ver(a); } });
  const tg = pj.querySelector('.pj-toggle');
  if (tg) tg.addEventListener('click', () => { const on = tg.getAttribute('aria-pressed') !== 'true'; tg.setAttribute('aria-pressed', String(on)); stage.dispatchEvent(new CustomEvent('pj:estados', { detail: on })); });
  card.querySelectorAll('.pj-tabs [data-pt]').forEach(b => b.addEventListener('click', () => {
    card.querySelectorAll('.pj-tabs [data-pt]').forEach(x => x.setAttribute('aria-selected', String(x === b)));
    card.querySelectorAll('.pj-view').forEach(v => { v.hidden = v.dataset.pv !== b.dataset.pt; });
  }));
  card.querySelectorAll('.pj-thumbs [data-img]').forEach(b => b.addEventListener('click', () => {
    card.querySelectorAll('.pj-thumbs [data-img]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    ponerFoto(b.dataset.img);
  }));
  cta.addEventListener('click', () => { note.hidden = false; });
  piso(6, true);
})();
