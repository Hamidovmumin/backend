
/* Custom cursor */
const cur = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; cur.style.left = mx+'px'; cur.style.top = my+'px'; });
(function animRing() {
rx += (mx - rx) * .14; ry += (my - ry) * .14;
ring.style.left = rx+'px'; ring.style.top = ry+'px';
requestAnimationFrame(animRing);
})();
document.querySelectorAll('a,button,.cat-item,.book-card,.news-card').forEach(el => {
el.addEventListener('mouseenter', () => { ring.style.width='56px'; ring.style.height='56px'; ring.style.opacity='1'; cur.style.transform='translate(-50%,-50%) scale(1.6)'; });
el.addEventListener('mouseleave', () => { ring.style.width='36px'; ring.style.height='36px'; ring.style.opacity='.55'; cur.style.transform='translate(-50%,-50%) scale(1)'; });
});

/* Scroll reveal */
const io = new IntersectionObserver(entries => {
entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

/* Cart counter */
let count = 0;
const badge = document.getElementById('cartCount');
document.querySelectorAll('.btn-add').forEach(btn => {
btn.addEventListener('click', function() {
  count++;
  badge.textContent = count;
  this.classList.add('added');
  this.innerHTML = '<i class="bi bi-check2"></i> Əlavə edildi';
  setTimeout(() => {
    this.classList.remove('added');
    this.innerHTML = '<i class="bi bi-plus-lg"></i> Əlavə et';
  }, 1400);
});
});

/* Wishlist toggle */
document.querySelectorAll('.wish-btn').forEach(btn => {
btn.addEventListener('click', function() {
  this.classList.toggle('active');
  const ic = this.querySelector('i');
  ic.classList.toggle('bi-heart');
  ic.classList.toggle('bi-heart-fill');
});
});

