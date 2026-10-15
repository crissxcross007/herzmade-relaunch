(() => {
  const buttons = document.querySelectorAll('[data-filter]');
  const cards = document.querySelectorAll('.gift-card');
  const count = document.getElementById('gift-count');
  buttons.forEach(button => button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let total = 0;
    cards.forEach(card => {
      const show = filter === 'alle' || card.dataset.occasions.split(' ').includes(filter);
      card.hidden = !show;
      if (show) total++;
    });
    count.textContent = total + (total === 1 ? ' Geschenkidee' : ' Geschenkideen');
  }));
})();