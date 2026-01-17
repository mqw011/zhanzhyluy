document.addEventListener('DOMContentLoaded', function(){
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if(!toggle || !nav) return;
  toggle.addEventListener('click', ()=> nav.classList.toggle('open'));
  // close when a link is clicked
  nav.querySelectorAll('a').forEach(a=> a.addEventListener('click', ()=> nav.classList.remove('open')));
  // close on Escape
  document.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') nav.classList.remove('open'); });
});
