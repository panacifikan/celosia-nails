(function () {
  document.querySelectorAll('[data-celosia-vibe-strip]').forEach(function (strip) {
    var section = strip.closest('.celosia-showcase');
    if (!section) return;
    var grid = section.querySelector('[data-celosia-grid]');
    var bestseller = section.querySelector('[data-celosia-bestseller]');
    var heading = section.querySelector('.celosia-showcase__vibe-heading');
    var sub = section.querySelector('.celosia-showcase__vibe-sub');
    var defaultHeading = heading ? heading.textContent : '';
    var defaultSub = sub ? sub.textContent : '';

    strip.addEventListener('click', function (e) {
      var card = e.target.closest('.celosia-vibe-card');
      if (!card) return;
      var vibe = card.getAttribute('data-vibe');

      strip.querySelectorAll('.celosia-vibe-card').forEach(function (c) {
        c.classList.toggle('is-active', c === card);
      });

      var cards = grid ? grid.querySelectorAll('.celosia-product-card') : [];
      var visibleCount = 0;

      if (vibe === 'all') {
        cards.forEach(function (p) { p.hidden = false; });
        if (bestseller) bestseller.hidden = false;
        if (heading) heading.textContent = defaultHeading;
        if (sub) sub.textContent = defaultSub;
      } else {
        cards.forEach(function (p) {
          var match = p.getAttribute('data-vibe') === vibe;
          p.hidden = !match;
          if (match) visibleCount++;
        });
        if (bestseller) bestseller.hidden = true;
        if (heading) heading.textContent = card.querySelector('.celosia-vibe-card__label').textContent;
        if (sub) sub.textContent = visibleCount + ' designs · $59 each';
      }
    });
  });
})();
