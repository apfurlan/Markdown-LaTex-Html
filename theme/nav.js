const slides  = document.querySelectorAll('.slide-wrap');
let current   = 0;
const counter = document.getElementById('slide-counter');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const navEl   = document.getElementById('nav');

// Design dimensions — must match --slide-w / --slide-h in CSS
const SLIDE_W = 800;
const SLIDE_H = 600;

// ── Slide navigation ──────────────────────────────────────────────────────

function changeSlide(dir) {
  resetScale(slides[current]);
  slides[current].classList.remove('active');
  current = Math.max(0, Math.min(slides.length - 1, current + dir));
  slides[current].classList.add('active');
  counter.textContent = `${current + 1} / ${slides.length}`;
  prevBtn.disabled = current === 0;
  nextBtn.disabled = current === slides.length - 1;
  if (window.MathJax) MathJax.typesetPromise([slides[current]]);
  applyScale();
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') changeSlide(1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   changeSlide(-1);
});

// ── Fullscreen scaling ────────────────────────────────────────────────────

function isFullscreen() {
  // Covers both programmatic fullscreen and F11 in Chromium
  return !!(document.fullscreenElement || document.webkitFullscreenElement)
      || window.innerHeight >= window.screen.height * 0.95;
}

function resetScale(el) {
  if (el) el.removeAttribute('style');
}

function applyScale() {
  const el = slides[current];
  if (!el) return;

  if (!isFullscreen()) {
    resetScale(el);
    navEl.style.display          = '';
    document.body.style.overflow = '';
    document.body.style.background = '';
    return;
  }

  const vw    = window.innerWidth;
  const vh    = window.innerHeight;
  const scale = Math.min(vw / SLIDE_W, vh / SLIDE_H);
  const left  = (vw - SLIDE_W * scale) / 2;
  const top   = (vh - SLIDE_H * scale) / 2;

  el.style.cssText = `
    position: fixed;
    left: ${left}px;
    top: ${top}px;
    width: ${SLIDE_W}px;
    transform: scale(${scale});
    transform-origin: top left;
    box-shadow: none;
    z-index: 9999;
    display: block;
  `;

  navEl.style.display          = 'none';
  document.body.style.overflow = 'hidden';
  document.body.style.background = '#000';
}

window.addEventListener('resize', applyScale);
document.addEventListener('fullscreenchange', applyScale);
document.addEventListener('webkitfullscreenchange', applyScale);
