// Shared site header for the Applet Library. Any page in it can include it:
//   <script src="../site-header.js" data-current="games" defer></script>
// The library on GitHub is the only home: every menu item is one of its own sections.
// data-current names the item to underline: home, talks, teaching, games, utilities or
// research ("auto" reads ?section= on the library page itself).
// Skipped inside an iframe, so a page embedded elsewhere does not show two headers.
(function () {
  if (window.top !== window.self) return;

  const me = document.currentScript;
  // The library's root is wherever this script lives, so links work live and from a local copy.
  const ROOT = new URL('./', (me && me.src) || location.href).href;
  const MENU = [
    ['Home', 'home', ''],
    ['Talks', 'talks', '?section=talks'],
    ['Teaching & Learning', 'teaching', '?section=teaching'],
    ['Games', 'games', '?section=games'],
    ['Utilities', 'utilities', '?section=utilities'],
    ['Research', 'research', '?section=research'],
  ];
  const OLD = { 'teaching-learning': 'teaching' };   // the name pages used before

  let current = (me && me.dataset.current) || '';
  if (current === 'auto') current = new URLSearchParams(location.search).get('section') || 'home';
  current = OLD[current] || current;

  const style = document.createElement('style');
  style.textContent = `
    .sh { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 12px 24px;
          border-bottom: 1px solid #e8e8e8; background: #fff; font-family: "Libre Franklin", system-ui, sans-serif; }
    .sh-brand { display: flex; align-items: center; gap: 12px; color: #212121; text-decoration: none; font-size: 20px; }
    .sh-brand svg { width: 40px; height: 40px; flex-shrink: 0; }
    .sh-nav { display: flex; flex-wrap: wrap; gap: 4px 24px; }
    .sh-nav a { color: #6b6b6b; text-decoration: none; font-size: 15px; padding: 6px 0; border-bottom: 2px solid transparent; }
    .sh-nav a:hover { color: #212121; }
    .sh-nav a[aria-current="page"] { color: #212121; border-bottom-color: #212121; }
    @media (max-width: 760px) {
      .sh { flex-direction: column; align-items: flex-start; gap: 6px; padding: 10px 16px; }
      .sh-nav { gap: 2px 16px; }
      .sh-nav a { font-size: 14px; }
    }
    @media print { .sh { display: none; } }
  `;

  const header = document.createElement('header');
  header.className = 'sh';
  header.innerHTML = `
    <a class="sh-brand" href="${ROOT}">
      <svg viewBox="0 0 64 64" aria-hidden="true">
        <g stroke="#121212" stroke-linejoin="round" stroke-linecap="round">
          <rect x="4" y="4" width="56" height="56" rx="8" fill="#fff" stroke-width="3.5"/>
          <path d="M32 4 V60 M4 32 H60" fill="none" stroke-width="2.5"/>
          <circle cx="18" cy="18" r="7.5" fill="#f7da21" stroke-width="2.5"/>
          <rect x="39" y="11" width="14" height="14" fill="#5cc4b8" stroke-width="2.5"/>
          <path d="M18 38 L26 51 H10 Z" fill="#f39b4a" stroke-width="2.5"/>
          <path d="M46 37 L54 45 L46 53 L38 45 Z" fill="#6f95e8" stroke-width="2.5"/>
        </g>
      </svg>
      <span>Applet Library</span>
    </a>
    <nav class="sh-nav" aria-label="Applet Library">
      ${MENU.map(([label, id, q]) =>
        `<a href="${ROOT}${q}"${id === current ? ' aria-current="page"' : ''}>${label.replace('&', '&amp;')}</a>`).join('')}
    </nav>`;

  document.head.appendChild(style);
  document.body.prepend(header);
})();
