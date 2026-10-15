(() => {
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.gift-card')];
  const count = document.getElementById('gift-count');
  function applyFilter() {
    const requested = location.hash.slice(1);
    const filter = buttons.some(b => b.dataset.filter === requested) ? requested : 'alle';
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === filter)));
    let total = 0;
    cards.forEach(card => {
      card.hidden = filter !== 'alle' && !card.dataset.occasions.split(' ').includes(filter);
      if (!card.hidden) total++;
    });
    if (count) count.textContent = total + (total === 1 ? ' Geschenkidee' : ' Geschenkideen');
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    history.replaceState(null, '', location.pathname + location.search + (button.dataset.filter === 'alle' ? '' : '#' + button.dataset.filter));
    applyFilter();
  }));
  window.addEventListener('hashchange', applyFilter);
  applyFilter();
})();