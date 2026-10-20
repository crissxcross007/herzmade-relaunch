/* Small progressive enhancements. Content, images and navigation are static HTML. */
document.documentElement.classList.add('js');
(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.getElementById('main-nav');
  const closeMenu = () => {
    if (!menuButton || !nav) return;
    menuButton.setAttribute('aria-expanded','false');
    nav.classList.remove('is-open');
  };
  if (menuButton && nav) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded',String(open));
      nav.classList.toggle('is-open',open);
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click',closeMenu));
    window.addEventListener('resize', () => { if (window.innerWidth > 1050) closeMenu(); });
  }
  document.querySelectorAll('.submenu-toggle').forEach(button => {
    button.addEventListener('click', () => {
      const group = button.closest('.nav-group');
      const open = button.getAttribute('aria-expanded') !== 'true';
      button.setAttribute('aria-expanded',String(open));
      group.classList.toggle('open',open);
    });
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      const wasOpen = nav && nav.classList.contains('is-open');
      closeMenu();
      document.querySelectorAll('.nav-group.open').forEach(group => {
        group.classList.remove('open');
        group.querySelector('button').setAttribute('aria-expanded','false');
      });
      if (wasOpen) menuButton.focus();
    }
  });
  document.addEventListener('click', e => {
    if (!e.target.closest('.site-header')) closeMenu();
  });
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const products = [...document.querySelectorAll('.product')];
  const count = document.getElementById('gift-count');
  function filterProducts() {
    const raw = location.hash.slice(1);
    const wanted = raw==='andenken'?'gedenken':raw;
    const active = filterButtons.some(b=>b.dataset.filter===wanted) ? wanted : 'alle';
    filterButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===active)));
    let visible=0;
    products.forEach(p=>{
      p.hidden=active!=='alle' && !p.dataset.occasions.split(' ').includes(active);
      if (!p.hidden) visible++;
    });
    if (count) count.textContent=visible+(visible===1?' Beispiel':' Beispiele');
    const heading=document.getElementById('ideas-title');
    const chosen=filterButtons.find(b=>b.dataset.filter===active);
    if (heading) heading.textContent=active==='alle'?'Echte Arbeiten als Inspiration.':chosen.textContent+' – echte Beispiele.';
    const remembrance=active==='gedenken';
    const copy={
      'ideas-eyebrow':remembrance?'Erinnern & Gedenken':'Echte Arbeiten. Persönliche Anlässe.',
      'ideas-heading-main':remembrance?'Was bleibt,':'Für deinen Anlass.',
      'ideas-heading-accent':remembrance?'ist die Erinnerung.':'Persönlich gestaltet.',
      'ideas-intro':remembrance?'Ein vertrautes Foto, ein Name oder Worte, die verbinden. Wir gestalten persönliche Erinnerungsstücke an Menschen und Tiere – behutsam und nach deinen Wünschen.':'Entdecke Einzelstücke, die wir für besondere Anlässe und persönliche Erinnerungen gestaltet haben. Wähle deinen Anlass und lass dich von den passenden Arbeiten inspirieren.',
      'ideas-context-text':remembrance?'Hier zeigen wir Arbeiten, die als Erinnerungsstücke entstanden sind. Größe, Material und Gestaltung besprechen wir in Ruhe mit dir.':'Jedes gezeigte Werk ist dem tatsächlichen Anlass seines Auftrags zugeordnet.'
    };
    Object.entries(copy).forEach(([id,text])=>{const node=document.getElementById(id);if(node)node.textContent=text});
    if(remembrance&&heading)heading.textContent='Persönliche Erinnerungsstücke.';
    document.querySelectorAll('[data-gift-cta]').forEach(node=>{node.hidden=remembrance});
    document.querySelectorAll('[data-remembrance-cta]').forEach(node=>{node.hidden=!remembrance});
    const empty=document.getElementById('empty-results');
    if (empty) empty.hidden=visible!==0;
    document.querySelectorAll('[data-only-filter]').forEach(note=>{note.hidden=note.dataset.onlyFilter!==active});
  }
  if (filterButtons.length) {
    filterButtons.forEach(button=>button.addEventListener('click',()=>{
      history.replaceState(null,'',location.pathname+location.search+(button.dataset.filter==='alle'?'':'#'+button.dataset.filter));
      filterProducts();
    }));
    window.addEventListener('hashchange',filterProducts);
    filterProducts();
  }
  const dialog=document.querySelector('dialog.lightbox');
  const allGallery=[...document.querySelectorAll('[data-lightbox]')];
  let gallery=allGallery;
  let current=0, returnFocus=null;
  if (dialog && typeof dialog.showModal==='function') {
    const image=dialog.querySelector('img');
    const caption=dialog.querySelector('figcaption');
    const show=i=>{
      current=(i+gallery.length)%gallery.length;
      const item=gallery[current];
      const crop=item.querySelector('svg.gallery-crop');
      dialog.querySelector('.lightbox-crop')?.remove();
      image.style.display=crop?'none':'';
      if (crop) {
        image.removeAttribute('src');
        const preview=crop.cloneNode(true);
        preview.classList.add('lightbox-crop');
        const box=crop.viewBox.baseVal;
        preview.style.width=`min(80vw, ${75*box.width/box.height}vh)`;
        image.after(preview);
      } else {
        image.src=item.href;
        image.alt=item.querySelector('img').alt;
      }
      caption.textContent=item.dataset.caption+' · '+(current+1)+' / '+gallery.length;
    };
    allGallery.forEach(link=>link.addEventListener('click',event=>{
      event.preventDefault();returnFocus=link;
      gallery=allGallery.filter(item=>!item.closest('[hidden]'));
      show(gallery.indexOf(link));dialog.showModal();document.body.style.overflow='hidden';
    }));
    dialog.querySelector('.lightbox-close').addEventListener('click',()=>dialog.close());
    dialog.querySelector('.lightbox-prev').addEventListener('click',()=>show(current-1));
    dialog.querySelector('.lightbox-next').addEventListener('click',()=>show(current+1));
    dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
    dialog.addEventListener('keydown',e=>{
      if(e.key==='ArrowLeft'){e.preventDefault();show(current-1)}
      if(e.key==='ArrowRight'){e.preventDefault();show(current+1)}
    });
    dialog.addEventListener('close',()=>{document.body.style.overflow='';image.removeAttribute('src');dialog.querySelector('.lightbox-crop')?.remove();if(returnFocus)returnFocus.focus()});
  }
  const select=document.getElementById('product');
  const requested=new URLSearchParams(location.search).get('produkt');
  if(select && requested){const option=[...select.options].find(o=>o.textContent===requested);if(option)select.value=option.value}
})();
