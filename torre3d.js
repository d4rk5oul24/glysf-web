// Torre Roble en 3D: render propio en canvas (sin librerías), se gira arrastrando
// y cada apartamento se ilumina al pasar por encima y se selecciona al tocarlo.
(() => {
  const stage = document.querySelector('.pj-stage');
  const cv = stage && stage.querySelector('.pj-3d');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Datos de los apartamentos (vienen de los botones de la página)
  const unidades = {};
  document.querySelectorAll('.pj-units .apt').forEach(b => {
    unidades[b.dataset.apto] = { piso: +b.dataset.piso, u: +b.dataset.apto % 100, estado: b.dataset.estado };
  });

  // ---------- Geometría (metros) ----------
  const W = 28, D = 12, PB = 3.6, HP = 3.1, PISOS = [2, 3, 4, 5, 6, 7, 8];
  const H = PB + PISOS.length * HP;
  const X0 = -W / 2, X1 = W / 2, Z0 = -D / 2, Z1 = D / 2;
  const SOL = norm([-0.55, 0.75, 0.62]);
  const C = {
    muro: [242, 240, 234], muroSombra: [214, 212, 206], antepecho: [126, 134, 146], losa: [228, 226, 220],
    vidrio: [52, 72, 98], vidrioLuz: [150, 180, 205], marco: [70, 74, 82], lobby: [196, 170, 120],
    techo: [204, 200, 192], maquinas: [180, 178, 172], tierra: [96, 84, 70]
  };
  const quads = [];
  function q(p, color, extra) { const n = normalOf(p); quads.push(Object.assign({ p, n, color }, extra || {})); }
  function box(x0, x1, y0, y1, z0, z1, color, extra, skip) {
    skip = skip || '';
    if (!skip.includes('f')) q([[x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], color, extra);
    if (!skip.includes('b')) q([[x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0]], color, extra);
    if (!skip.includes('l')) q([[x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0]], color, extra);
    if (!skip.includes('r')) q([[x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1]], color, extra);
    if (!skip.includes('t')) q([[x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [x0, y1, z0]], color, extra);
    if (!skip.includes('d')) q([[x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1]], color, extra);
  }
  // volumen principal
  box(X0, X1, 0, H, Z0, Z1, C.muro, { kind: 'muro', base: true }, 'd');
  // primer piso: lobby acristalado al frente
  q([[X0 + 2, 0.2, Z1 + .02], [X1 - 2, 0.2, Z1 + .02], [X1 - 2, PB - .5, Z1 + .02], [X0 + 2, PB - .5, Z1 + .02]], C.lobby, { kind: 'vidrio', lit: true });
  box(-4, 4, PB - .45, PB - .2, Z1, Z1 + 2.2, C.losa);
  // cubierta: antepecho y cuarto de máquinas
  box(X0, X1, H, H + .9, Z1 - .3, Z1, C.muro); box(X0, X1, H, H + .9, Z0, Z0 + .3, C.muro);
  box(X0, X0 + .3, H, H + .9, Z0 + .3, Z1 - .3, C.muro); box(X1 - .3, X1, H, H + .9, Z0 + .3, Z1 - .3, C.muro);
  box(-5, 3, H, H + 2.6, -3, 2, C.maquinas);
  // aletas blancas entre apartamentos (como en la foto de referencia)
  const UW = W / 4;
  for (let k = 0; k <= 4; k++) { const x = X0 + k * UW; box(x - .18, x + .18, PB, H, Z1, Z1 + 1.75, C.muro, { kind: 'aleta' }, 'd'); }
  // pisos de apartamentos
  PISOS.forEach((piso, i) => {
    const y0 = PB + i * HP, y1 = y0 + HP;
    for (let u = 1; u <= 4; u++) {
      const id = String(piso * 100 + u);
      const ux0 = X0 + (u - 1) * UW, ux1 = ux0 + UW;
      const luz = ((piso * 7 + u * 3) % 5) === 0;
      // frente: ventanal + balcón con antepecho gris
      q([[ux0 + .5, y0 + .25, Z1 + .02], [ux1 - .5, y0 + .25, Z1 + .02], [ux1 - .5, y1 - .4, Z1 + .02], [ux0 + .5, y1 - .4, Z1 + .02]], C.vidrio, { kind: 'vidrio', lit: luz, unit: id });
      for (let m = 1; m < 4; m++) { const x = ux0 + .5 + (UW - 1) * m / 4; q([[x - .04, y0 + .25, Z1 + .03], [x + .04, y0 + .25, Z1 + .03], [x + .04, y1 - .4, Z1 + .03], [x - .04, y1 - .4, Z1 + .03]], C.marco, { unit: id }); }
      box(ux0 + .18, ux1 - .18, y0, y0 + .22, Z1, Z1 + 1.7, C.losa, { unit: id }, 'b');
      q([[ux0 + .18, y0 + .22, Z1 + 1.7], [ux1 - .18, y0 + .22, Z1 + 1.7], [ux1 - .18, y0 + 1.1, Z1 + 1.7], [ux0 + .18, y0 + 1.1, Z1 + 1.7]], C.antepecho, { unit: id, kind: 'antepecho' });
      q([[ux1 - .18, y0 + .22, Z1 + 1.7], [ux0 + .18, y0 + .22, Z1 + 1.7], [ux0 + .18, y0 + 1.1, Z1 + 1.7], [ux1 - .18, y0 + 1.1, Z1 + 1.7]], C.antepecho, { unit: id, kind: 'antepecho' });
      // panel de selección al frente y atrás (transparente salvo resaltado)
      q([[ux0 + .2, y0 + .05, Z1 + 1.74], [ux1 - .2, y0 + .05, Z1 + 1.74], [ux1 - .2, y1 - .05, Z1 + 1.74], [ux0 + .2, y1 - .05, Z1 + 1.74]], null, { panel: id });
      q([[ux1 - .2, y0 + .05, Z0 - .04], [ux0 + .2, y0 + .05, Z0 - .04], [ux0 + .2, y1 - .05, Z0 - .04], [ux1 - .2, y1 - .05, Z0 - .04]], null, { panel: id });
      // atrás: dos ventanas por apartamento
      for (const [a, b] of [[.12, .42], [.58, .88]]) {
        const xa = ux1 - UW * a, xb = ux1 - UW * b;
        q([[xa, y0 + .9, Z0 - .02], [xb, y0 + .9, Z0 - .02], [xb, y1 - .5, Z0 - .02], [xa, y1 - .5, Z0 - .02]], C.vidrio, { kind: 'vidrio', lit: luz && a < .5, unit: id });
      }
      // costados: ventanas de los apartamentos de esquina
      if (u === 1) for (const [a, b] of [[.15, .4], [.6, .85]]) q([[X0 - .02, y0 + .9, Z0 + D * a], [X0 - .02, y0 + .9, Z0 + D * b], [X0 - .02, y1 - .5, Z0 + D * b], [X0 - .02, y1 - .5, Z0 + D * a]], C.vidrio, { kind: 'vidrio', unit: id });
      if (u === 4) for (const [a, b] of [[.15, .4], [.6, .85]]) q([[X1 + .02, y0 + .9, Z1 - D * a], [X1 + .02, y0 + .9, Z1 - D * b], [X1 + .02, y1 - .5, Z1 - D * b], [X1 + .02, y1 - .5, Z1 - D * a]], C.vidrio, { kind: 'vidrio', unit: id });
      if (u === 1) q([[X0 - .05, y0 + .05, Z0 + .3], [X0 - .05, y0 + .05, Z1 - .3], [X0 - .05, y1 - .05, Z1 - .3], [X0 - .05, y1 - .05, Z0 + .3]], null, { panel: id });
      if (u === 4) q([[X1 + .05, y0 + .05, Z1 - .3], [X1 + .05, y0 + .05, Z0 + .3], [X1 + .05, y1 - .05, Z0 + .3], [X1 + .05, y1 - .05, Z1 - .3]], null, { panel: id });
    }
  });
  const arboles = [[-19, 9], [-17, -9], [18, 10], [20, -6], [-8, 13], [9, 14], [0, -14], [-22, 1]];

  // ---------- Cámara ----------
  let yaw = -0.55, pitch = 0.32, dist = 62, auto = !reduce;
  let hover = null, sel = (document.querySelector('.pj-units .apt.sel') || {}).dataset?.apto || null, estados = false, sucio = true;
  let w = 0, h = 0, dpr = 1, fov = 1, vc = .47, cam, R, U, F, centro;
  function medir() {
    const r = cv.getBoundingClientRect(); dpr = Math.min(devicePixelRatio || 1, 2);
    w = r.width; h = r.height; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    fov = Math.min(w, h * 1.1) * 1.15; dist = w < 600 ? 60 : 62; vc = w < 600 ? 0.33 : 0.47; sucio = true;
  }
  function camara() {
    centro = [0, H * 0.42, 0];
    cam = [centro[0] + dist * Math.cos(pitch) * Math.sin(yaw), centro[1] + dist * Math.sin(pitch), centro[2] + dist * Math.cos(pitch) * Math.cos(yaw)];
    F = norm(sub(centro, cam)); R = norm(cross(F, [0, 1, 0])); U = cross(R, F);
  }
  function proy(p) {
    const v = sub(p, cam), z = dot(v, F);
    return [w / 2 + fov * dot(v, R) / z, h * vc - fov * dot(v, U) / z, z];
  }

  // ---------- Dibujo ----------
  const rgb = (c, a) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a == null ? 1 : a})`;
  const tono = (c, k) => [Math.min(255, c[0] * k), Math.min(255, c[1] * k), Math.min(255, c[2] * k)];
  const ESTADO = { disponible: [114, 220, 166], separado: [242, 196, 107], vendido: [40, 46, 64] };
  function suelo(x0, x1, z0, z1, color, y) {
    const pts = [[x0, y || 0, z0], [x1, y || 0, z0], [x1, y || 0, z1], [x0, y || 0, z1]].map(proy);
    if (pts.some(p => p[2] < 1)) return;
    ctx.beginPath(); pts.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath(); ctx.fillStyle = color; ctx.fill();
  }
  function dibujar() {
    camara();
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    // terreno
    suelo(-60, 60, -60, 60, '#5f7a4e');
    suelo(-26, 26, -16, 20, '#6d8a58');
    suelo(-17, 17, -9, 11.5, '#cfc8bb');
    suelo(-3, 3, 11.5, 40, '#cfc8bb');
    // sombra del edificio sobre el piso
    const sh = [];
    for (const x of [X0 - .2, X1 + .2]) for (const z of [Z0, Z1 + 1.8]) for (const y of [0, H]) sh.push([x - SOL[0] * y / SOL[1], 0, z - SOL[2] * y / SOL[1]]);
    const hull = casco(sh.map(proy).filter(p => p[2] > 1));
    if (hull.length > 2) {
      ctx.save(); ctx.filter = 'blur(6px)'; ctx.beginPath(); hull.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
      ctx.closePath(); ctx.fillStyle = 'rgba(20,28,24,.32)'; ctx.fill(); ctx.restore();
    }
    // lista de cosas a pintar, de atrás hacia adelante
    const items = [];
    for (const qq of quads) {
      const c = [0, 0, 0]; qq.p.forEach(p => { c[0] += p[0] / 4; c[1] += p[1] / 4; c[2] += p[2] / 4; });
      if (dot(qq.n, sub(cam, c)) <= 0) continue;
      const pp = qq.p.map(proy); if (pp.some(p => p[2] < 1)) continue;
      items.push({ t: 'q', q: qq, pp, z: qq.base ? 1e9 : dot(sub(c, cam), F) - (qq.panel ? 0.6 : 0) });
    }
    for (const [x, z] of arboles) { const p = proy([x, 0, z]); if (p[2] > 1) items.push({ t: 'a', x, z, p, z2: p[2], z: p[2] }); }
    items.sort((a, b) => b.z - a.z);
    const marcar = id => id === sel || id === hover;
    for (const it of items) {
      if (it.t === 'a') { arbol(it); continue; }
      const qq = it.q, pp = it.pp;
      let fill;
      if (qq.panel) {
        const id = qq.panel, un = unidades[id];
        if (!un) continue;
        if (id === sel) fill = 'rgba(255,255,255,.42)';
        else if (id === hover) fill = rgb(ESTADO[un.estado], .55);
        else if (estados) fill = rgb(ESTADO[un.estado], .48);
        else continue;
      } else {
        const luz = 0.7 + 0.38 * Math.max(0, dot(qq.n, SOL)) + (qq.n[1] > .5 ? .06 : 0);
        let col = tono(qq.color, luz);
        if (qq.kind === 'vidrio') {
          const vista = norm(sub(cam, qq.p[0]));
          const refl = Math.pow(1 - Math.max(0, dot(vista, qq.n)), 2);
          col = qq.lit ? [236, 196, 138] : mezcla(tono(C.vidrio, .9 + .2 * Math.max(0, dot(qq.n, SOL))), C.vidrioLuz, .25 + .55 * refl);
        }
        fill = rgb(col);
      }
      ctx.beginPath(); pp.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])); ctx.closePath();
      ctx.fillStyle = fill; ctx.fill();
      if (qq.panel && marcar(qq.panel)) { ctx.lineWidth = qq.panel === sel ? 2.5 : 1.5; ctx.strokeStyle = '#fff'; ctx.stroke(); }
      else if (!qq.panel && qq.kind !== 'vidrio') { ctx.lineWidth = .5; ctx.strokeStyle = 'rgba(0,0,0,.08)'; ctx.stroke(); }
      if (qq.kind === 'vidrio' && !qq.lit) {
        // reflejo diagonal suave en el vidrio
        const [a, b, c2, d] = pp;
        const g = ctx.createLinearGradient(a[0], c2[1], c2[0], a[1]);
        g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(.48, 'rgba(255,255,255,.16)'); g.addColorStop(.56, 'rgba(255,255,255,0)');
        ctx.fillStyle = g; ctx.fill();
      }
    }
    sucio = false; ultimos = items;
  }
  function arbol(it) {
    const base = proy([it.x, 0, it.z]), copa = proy([it.x, 4.2, it.z]);
    const r = fov * 2.4 / it.z2;
    ctx.fillStyle = 'rgba(30,40,30,.25)'; ctx.beginPath(); ctx.ellipse(base[0] + r * .4, base[1], r * 1.1, r * .38, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#5a4634'; ctx.lineWidth = Math.max(1, r * .18); ctx.beginPath(); ctx.moveTo(base[0], base[1]); ctx.lineTo(copa[0], copa[1]); ctx.stroke();
    const g = ctx.createRadialGradient(copa[0] - r * .35, copa[1] - r * .5, r * .1, copa[0], copa[1] - r * .2, r * 1.2);
    g.addColorStop(0, '#8fb06c'); g.addColorStop(.6, '#4f7440'); g.addColorStop(1, '#30492a');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(copa[0], copa[1] - r * .3, r, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(copa[0] + r * .55, copa[1] + r * .1, r * .72, 0, Math.PI * 2); ctx.fill();
  }

  // ---------- Selección con el puntero ----------
  let ultimos = [];
  function elegir(x, y) {
    for (let i = ultimos.length - 1; i >= 0; i--) {
      const it = ultimos[i]; if (it.t !== 'q') continue;
      if (dentro(x, y, it.pp)) {
        if (it.q.panel) return it.q.panel;
        if (it.q.unit) return it.q.unit;
        if (it.q.kind === 'aleta' || it.q.kind === 'muro') {
          // muro: deducir el apartamento por la posición sobre la fachada
          continue;
        }
      }
    }
    return null;
  }
  let arrastre = null, movido = 0;
  cv.addEventListener('pointerdown', e => { arrastre = { x: e.clientX, y: e.clientY }; movido = 0; auto = false; });
  addEventListener('pointerup', e => {
    if (arrastre && movido < 6 && e.target === cv) {
      const r = cv.getBoundingClientRect(); const id = elegir(e.clientX - r.left, e.clientY - r.top);
      if (id) stage.dispatchEvent(new CustomEvent('pj:pick', { detail: id, bubbles: true }));
    }
    arrastre = null;
  });
  cv.addEventListener('pointermove', e => {
    const r = cv.getBoundingClientRect();
    if (arrastre) {
      const dx = e.clientX - arrastre.x, dy = e.clientY - arrastre.y; movido += Math.abs(dx) + Math.abs(dy);
      yaw -= dx * 0.008; pitch = Math.min(0.85, Math.max(0.08, pitch + dy * 0.004));
      arrastre = { x: e.clientX, y: e.clientY }; sucio = true; return;
    }
    const id = elegir(e.clientX - r.left, e.clientY - r.top);
    if (id !== hover) { hover = id; sucio = true; cv.style.cursor = id ? 'pointer' : 'grab'; }
  });
  cv.addEventListener('pointerleave', () => { if (hover) { hover = null; sucio = true; } });
  stage.querySelectorAll('[data-girar]').forEach(b => b.addEventListener('click', () => { auto = false; giro = +b.dataset.girar * Math.PI / 4; }));
  let giro = 0;
  stage.addEventListener('pj:sel', e => { sel = e.detail; sucio = true; });
  stage.addEventListener('pj:estados', e => { estados = e.detail; sucio = true; });

  // ---------- Bucle ----------
  let visible = true;
  new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(cv);
  function frame() {
    if (visible) {
      if (auto) { yaw += 0.0016; sucio = true; }
      if (Math.abs(giro) > 0.001) { const d = giro * 0.12; yaw += d; giro -= d; sucio = true; }
      if (sucio) dibujar();
    }
    requestAnimationFrame(frame);
  }
  addEventListener('resize', medir);
  medir(); dibujar(); requestAnimationFrame(frame);

  // ---------- Utilidades ----------
  function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function norm(a) { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; }
  function normalOf(p) { return norm(cross(sub(p[1], p[0]), sub(p[3], p[0]))); }
  function mezcla(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  function dentro(x, y, pts) {
    let c = false;
    for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
      const [xi, yi] = pts[i], [xj, yj] = pts[j];
      if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c;
    }
    return c;
  }
  function casco(ps) {
    ps = ps.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
    const cr = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
    const lo = [], up = [];
    for (const p of ps) { while (lo.length >= 2 && cr(lo[lo.length - 2], lo[lo.length - 1], p) <= 0) lo.pop(); lo.push(p); }
    for (const p of ps.slice().reverse()) { while (up.length >= 2 && cr(up[up.length - 2], up[up.length - 1], p) <= 0) up.pop(); up.push(p); }
    return lo.slice(0, -1).concat(up.slice(0, -1));
  }
})();
