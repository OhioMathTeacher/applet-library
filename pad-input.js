/* PAD-INPUT v1 BEGIN -------------------------------------------------------
   Shared gamepad reader for the retro games. This file in applet-library is
   the canonical copy; each game pastes it in whole, between the BEGIN and END
   lines, so the games stay single files. Change it here first, then paste.

   Why: the Gamepad API only fixes button numbers when a pad reports
   mapping:"standard" (Xbox, PlayStation, 8BitDo in X-input). Cheap USB pads
   don't, and they put A, B, Select and Start wherever their firmware likes.
   So a non-standard pad gets a one-time prompt, PRESS A, PRESS B, PRESS
   SELECT, PRESS START, and the answer is kept in localStorage under the pad's
   id. Every game on the same site shares that key, so it is asked once per
   pad per browser, not once per game.

   The d-pad needs no prompt: it is read from buttons 12-15 (standard), axes
   0/1 (cheap pads that wire it as a stick), or a hat-switch axis (pads that
   report all eight directions on one axis, which rests above 1).

   ?padsetup in the URL asks again for every pad. Esc skips a prompt and keeps
   the standard numbers.

   PadInput.poll() returns {up, down, left, right, a, b, select, start, count}.
   While a prompt is up every button reads false, so the game ignores it.
   ------------------------------------------------------------------------- */
const PadInput = (() => {
  const OK = typeof window !== 'undefined' && typeof document !== 'undefined';
  const STEPS = ['a', 'b', 'select', 'start'];
  const NAME = {a: 'A', b: 'B', select: 'SELECT', start: 'START'};
  const STD = {a: 0, b: 1, select: 8, start: 9};
  const STORE = 'padinput-v1';
  const redo = OK && /[?&]padsetup\b/.test(location.search);
  let maps = {};
  try { maps = JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) {}
  const asked = new Set();      // ids already re-asked under ?padsetup
  const hats = {};              // id -> axis indices seen resting above 1
  const settle = new Set();     // ids that must let go of every button first
  let cal = null, box = null;

  const isDown = btn => !!btn && (btn.pressed || btn.value > 0.5);
  const held = p => { const s = new Set(); p.buttons.forEach((b, i) => { if (isDown(b)) s.add(i); }); return s; };
  const save = () => { try { localStorage.setItem(STORE, JSON.stringify(maps)); } catch (e) {} };

  function show() {
    if (!box) {
      box = document.createElement('div');
      box.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;' +
        'justify-content:center;background:rgba(0,0,0,.75);color:#fff;text-align:center;' +
        'font:bold 18px/1.7 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em';
      document.body.appendChild(box);
    }
    box.innerHTML = '<div style="border:3px solid #fff;background:#000;padding:22px 30px">' +
      'NEW CONTROLLER<br><br>PRESS ' + NAME[STEPS[cal.step]] +
      '<br><br><span style="font-size:12px;font-weight:normal;color:#aaa">' +
      (cal.step + 1) + ' OF 4 &middot; ESC SKIPS</span></div>';
    box.style.display = 'flex';
  }
  function finish(map) {
    maps[cal.id] = map; save(); settle.add(cal.id); cal = null;
    if (box) box.style.display = 'none';
  }
  if (OK) addEventListener('keydown', e => {
    if (cal && e.key === 'Escape') { e.preventDefault(); e.stopImmediatePropagation(); finish(Object.assign({}, STD)); }
  }, true);

  function needsAsking(p) {
    if (redo && !asked.has(p.id)) return true;
    if (maps[p.id]) return false;
    return p.mapping !== 'standard';
  }

  function hatDirs(v) {
    // Hat axes step through -1 .. 1 in sevenths: up, up-right, right ... up-left.
    const k = ((Math.round((v + 1) * 3.5) % 8) + 8) % 8;
    return {up: k === 7 || k <= 1, right: k >= 1 && k <= 3, down: k >= 3 && k <= 5, left: k >= 5};
  }

  function poll() {
    const out = {up: false, down: false, left: false, right: false,
                 a: false, b: false, select: false, start: false, count: 0};
    if (!OK || !navigator.getGamepads) return out;
    let pads = [];
    try { pads = navigator.getGamepads() || []; } catch (e) { return out; }
    const live = [];
    for (const p of pads) {
      if (!p || p.connected === false) continue;
      live.push(p); out.count++;
      const hs = hats[p.id] || (hats[p.id] = new Set());
      p.axes.forEach((v, i) => { if (Math.abs(v) > 1.05) hs.add(i); });
    }
    if (cal) {
      const p = live.find(q => q.id === cal.id);
      if (!p) { cal = null; if (box) box.style.display = 'none'; return out; }
      const now = held(p), used = Object.values(cal.map);
      for (const i of now) {
        if (cal.prev.has(i) || used.includes(i)) continue;
        cal.map[STEPS[cal.step++]] = i;
        if (cal.step === STEPS.length) { finish(cal.map); return out; }
        show(); break;
      }
      if (cal) cal.prev = now;
      return out;                                  // nothing reaches the game mid-prompt
    }
    for (const p of live) {
      if (needsAsking(p)) {
        if (redo) asked.add(p.id);
        cal = {id: p.id, step: 0, map: {}, prev: held(p)};
        show(); return out;
      }
    }
    for (const p of live) {
      if (settle.has(p.id)) { if (held(p).size) continue; settle.delete(p.id); }
      const m = maps[p.id] || STD;
      const mapped = new Set(Object.values(m));
      const btn = i => i != null && isDown(p.buttons[i]);
      const pad = i => !mapped.has(i) && btn(i);   // 12-15 as d-pad unless taken
      const hs = hats[p.id];
      const ax = hs.has(0) ? 0 : (p.axes[0] || 0), ay = hs.has(1) ? 0 : (p.axes[1] || 0);
      let h = {};
      for (const i of hs) { const v = p.axes[i]; if (Math.abs(v) <= 1.05) h = hatDirs(v); }
      out.up    = out.up    || pad(12) || ay < -0.5 || !!h.up;
      out.down  = out.down  || pad(13) || ay >  0.5 || !!h.down;
      out.left  = out.left  || pad(14) || ax < -0.5 || !!h.left;
      out.right = out.right || pad(15) || ax >  0.5 || !!h.right;
      out.a      = out.a      || btn(m.a);
      out.b      = out.b      || btn(m.b);
      out.select = out.select || btn(m.select);
      out.start  = out.start  || btn(m.start);
    }
    return out;
  }

  return {
    poll,
    get asking() { return !!cal; },
    forget() { maps = {}; save(); }               // from the console: PadInput.forget()
  };
})();
/* PAD-INPUT v1 END --------------------------------------------------------- */
