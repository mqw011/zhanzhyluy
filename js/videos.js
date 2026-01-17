document.addEventListener('DOMContentLoaded', function(){
  // Delegate clicks on placeholders to replace them with an iframe
  function createIframe(src){
    const ifr = document.createElement('iframe');
    ifr.setAttribute('allow','accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
    ifr.setAttribute('allowfullscreen','');
    ifr.setAttribute('loading','lazy');
    ifr.src = src + '?rel=0&modestbranding=1';
    ifr.style.position = 'absolute';
    ifr.style.top = '0';
    ifr.style.left = '0';
    ifr.style.width = '100%';
    ifr.style.height = '100%';
    ifr.style.border = '0';
    return ifr;
  }

  document.body.addEventListener('click', function(e){
    const ph = e.target.closest('.video-placeholder');
    if(!ph) return;
    const src = ph.dataset.src;
    if(!src) return;
    const parent = ph.parentElement;
    const wrap = parent.closest('.video-wrap') || parent;
    // remove placeholder and append iframe
    const iframe = createIframe(src);
    ph.remove();
    wrap.appendChild(iframe);
  });

  // keyboard activation (Enter / Space)
  document.body.addEventListener('keydown', function(e){
    if(e.key === 'Enter' || e.key === ' '){
      const active = document.activeElement;
      if(active && active.classList && active.classList.contains('video-placeholder')){
        active.click();
        e.preventDefault();
      }
    }
  });
});
